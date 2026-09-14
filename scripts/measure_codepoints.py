#!/usr/bin/env python3
"""Measure token cost of PUA codepoints (D10).

For each codepoint in a block, ask the Messages count_tokens endpoint how many
tokens a run of that glyph costs, and record tokens per glyph. Output goes to
spec/codepoints_cost.json sorted cheapest first, so syllables can be assigned
to codepoints by frequency (most frequent syllable -> cheapest codepoint).

Method
------
Tokenizers merge adjacent bytes unpredictably, so a single glyph in isolation
is not the number we care about; a glyph inside a word is. We measure each
codepoint as a run of REPEATS copies (default 16) and take

    cost = (tokens(run) - tokens(empty)) / REPEATS

This averages out edge effects at the run boundaries and is close to the
marginal cost of the glyph inside a word. One request per codepoint, sent
concurrently; count_tokens is not billed. Results are written after every
batch, so an interrupted run resumes where it stopped (--no-resume to redo).

Also usable for the shelved Hangul experiment (D6): --block hangul measures
U+AC00-U+D7A3 instead, to cross with a Korean frequency list.

Backends
--------
  --backend anthropic   (default) Messages count_tokens; free; needs ANTHROPIC_API_KEY.
  --backend openrouter  OpenRouter has no count endpoint, so send a 1-token
                        completion and read the NATIVE prompt token count from
                        /api/v1/generation (OpenRouter's completion response
                        reports a normalized count, not Anthropic's). Needs
                        OPENROUTER_API_KEY. Whole PUA block on Haiku costs well
                        under a dollar; the tokenizer is shared across Claude
                        models, so Haiku's count is the count.

--dry-run substitutes the UTF-8 byte count for a network call so the pipeline
can be exercised offline; the file it writes is marked "estimated" and must not
be used for assignment.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages/count_tokens"
ANTHROPIC_VERSION = "2023-06-01"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_GEN_URL = "https://openrouter.ai/api/v1/generation?id="
DEFAULT_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",
    "openrouter": "anthropic/claude-haiku-4.5",
}
# Some endpoints reject an empty message, so every measured string sits after
# this prefix; it is in the baseline too, so it cancels in the difference.
PREFIX = "."

BLOCKS = {
    "pua": (0xE000, 0xF8FF),       # Basic Multilingual Plane Private Use Area
    "hangul": (0xAC00, 0xD7A3),    # precomposed Hangul syllables (D6 experiment)
}

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "spec" / "codepoints_cost.json"


RETRY_CODES = (408, 429, 500, 502, 503, 504, 529)


def http_json(url, headers, body=None, retries=6, retry_on_missing=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    delay = 1.0
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET",
                                     headers={"content-type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                out = json.load(resp)
            if retry_on_missing and retry_on_missing(out) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return out
        except urllib.error.HTTPError as e:
            if e.code in RETRY_CODES and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"HTTP {e.code} from {url}: {e.read().decode('utf-8', 'replace')}")
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError(f"gave up on {url}")


def count_anthropic(text, model, api_key):
    out = http_json(ANTHROPIC_URL, {"x-api-key": api_key, "anthropic-version": ANTHROPIC_VERSION},
                    {"model": model, "messages": [{"role": "user", "content": text}]})
    return out["input_tokens"]


def count_openrouter(text, model, api_key):
    auth = {"authorization": f"Bearer {api_key}"}
    out = http_json(OPENROUTER_URL, auth, {
        "model": model,
        "messages": [{"role": "user", "content": text}],
        "max_tokens": 1,
        "temperature": 0,
    })
    gen_id = out["id"]
    # Generation stats lag the completion by a moment; retry until populated.
    stats = http_json(OPENROUTER_GEN_URL + gen_id, auth,
                      retry_on_missing=lambda o: not (o.get("data") or {}).get("native_tokens_prompt"))
    return int(stats["data"]["native_tokens_prompt"])


def dry_count(text):
    # Offline stand-in: assume byte-level fallback (1 token per UTF-8 byte)
    # on top of a fixed message overhead. An estimate, never a measurement.
    return 7 + len(text.encode("utf-8"))


def load_existing(path, resume):
    if resume and path.exists():
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        return {int(k, 16): v for k, v in data.get("costs", {}).items()}, data.get("meta", {})
    return {}, {}


def write(path, meta, costs):
    ordered = sorted(costs.items(), key=lambda kv: (kv[1], kv[0]))
    out = {
        "meta": meta,
        "costs": {f"{cp:04X}": cost for cp, cost in ordered},
    }
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--block", choices=BLOCKS, default="pua")
    ap.add_argument("--backend", choices=("anthropic", "openrouter"), default="anthropic")
    ap.add_argument("--model", default=None, help="default depends on --backend")
    ap.add_argument("--repeats", type=int, default=16)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="measure only the first N codepoints (smoke test)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--no-resume", action="store_true", help="discard an existing output file")
    ap.add_argument("--dry-run", action="store_true", help="no network; byte-count estimate only")
    args = ap.parse_args()

    lo, hi = BLOCKS[args.block]
    codepoints = list(range(lo, hi + 1))
    if args.limit:
        codepoints = codepoints[: args.limit]

    model = args.model or DEFAULT_MODELS[args.backend]
    key_var = {"anthropic": "ANTHROPIC_API_KEY", "openrouter": "OPENROUTER_API_KEY"}[args.backend]
    api_key = os.environ.get(key_var)
    if not args.dry_run and not api_key:
        print(f"{key_var} is not set (use --dry-run to exercise the script offline).", file=sys.stderr)
        return 2

    costs, meta = load_existing(args.out, resume=not args.no_resume)
    if costs and (meta.get("block") != args.block or meta.get("model") != model
                  or meta.get("repeats") != args.repeats or meta.get("estimated") != args.dry_run
                  or meta.get("backend") != ("dry-run" if args.dry_run else args.backend)):
        print(f"{args.out} was produced with different settings; pass --no-resume or a different --out.",
              file=sys.stderr)
        return 2
    todo = [cp for cp in codepoints if cp not in costs]
    print(f"block {args.block}: {len(codepoints)} codepoints, {len(costs)} done, {len(todo)} to measure")

    if args.dry_run:
        counter = dry_count
    elif args.backend == "anthropic":
        counter = lambda text: count_anthropic(text, model, api_key)  # noqa: E731
    else:
        counter = lambda text: count_openrouter(text, model, api_key)  # noqa: E731

    base = counter(PREFIX)
    meta = {
        "block": args.block,
        "backend": "dry-run" if args.dry_run else args.backend,
        "model": model,
        "repeats": args.repeats,
        "estimated": args.dry_run,
        "unit": "tokens per glyph, marginal, inside a run of `repeats` copies",
        "baseline_tokens": base,
    }

    def measure(cp):
        return cp, (counter(PREFIX + chr(cp) * args.repeats) - base) / args.repeats

    done = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(measure, cp) for cp in todo]
        for fut in as_completed(futures):
            cp, cost = fut.result()
            costs[cp] = cost
            done += 1
            if done % 64 == 0 or done == len(todo):
                write(args.out, meta, costs)
                rate = done / max(time.time() - t0, 1e-9)
                print(f"  {done}/{len(todo)}  ({rate:.1f}/s)")
    write(args.out, meta, costs)

    hist = {}
    for c in costs.values():
        hist[c] = hist.get(c, 0) + 1
    print("cost histogram (tokens/glyph: count):")
    for c in sorted(hist):
        print(f"  {c:.3f}: {hist[c]}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
