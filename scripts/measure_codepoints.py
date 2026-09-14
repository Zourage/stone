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

Requires ANTHROPIC_API_KEY. --dry-run substitutes the UTF-8 byte count for a
network call so the pipeline can be exercised offline; the file it writes is
marked "estimated" and must not be used for assignment.
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

API_URL = "https://api.anthropic.com/v1/messages/count_tokens"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-fable-5-1"

BLOCKS = {
    "pua": (0xE000, 0xF8FF),       # Basic Multilingual Plane Private Use Area
    "hangul": (0xAC00, 0xD7A3),    # precomposed Hangul syllables (D6 experiment)
}

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "spec" / "codepoints_cost.json"


def count_tokens(text, model, api_key, retries=6):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": text}],
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "content-type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": API_VERSION,
    })
    delay = 1.0
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)["input_tokens"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"count_tokens HTTP {e.code}: {e.read().decode('utf-8', 'replace')}")
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


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
    ap.add_argument("--model", default=DEFAULT_MODEL)
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

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not args.dry_run and not api_key:
        print("ANTHROPIC_API_KEY is not set (use --dry-run to exercise the script offline).", file=sys.stderr)
        return 2

    costs, meta = load_existing(args.out, resume=not args.no_resume)
    if costs and (meta.get("block") != args.block or meta.get("model") != args.model
                  or meta.get("repeats") != args.repeats or meta.get("estimated") != args.dry_run):
        print(f"{args.out} was produced with different settings; pass --no-resume or a different --out.",
              file=sys.stderr)
        return 2
    todo = [cp for cp in codepoints if cp not in costs]
    print(f"block {args.block}: {len(codepoints)} codepoints, {len(costs)} done, {len(todo)} to measure")

    if args.dry_run:
        counter = dry_count
    else:
        counter = lambda text: count_tokens(text, args.model, api_key)  # noqa: E731

    base = counter("")
    meta = {
        "block": args.block,
        "model": args.model,
        "repeats": args.repeats,
        "estimated": args.dry_run,
        "unit": "tokens per glyph, marginal, inside a run of `repeats` copies",
        "baseline_tokens": base,
    }

    def measure(cp):
        return cp, (counter(chr(cp) * args.repeats) - base) / args.repeats

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
