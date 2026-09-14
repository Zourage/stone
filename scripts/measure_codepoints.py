#!/usr/bin/env python3
"""Measure token cost and visibility of codepoint blocks (D10, retired by D24).

History: written to assign syllables to the cheapest BMP PUA codepoints. The
measurement showed the BMP PUA is stripped from Claude's input (D20, D21) and
every usable block costs a flat rate (D22), so assignment is by seeded draw
(scripts/assign_codepoints.py) and this script is kept as the measuring tool.

For each codepoint in a block, count how many tokens a run of that glyph costs
and record tokens per glyph. Output goes to spec/codepoints_cost*.json sorted
cheapest first. Cost 0 means stripped: unusable, not cheap.

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

O6 comparison blocks (real BMP scripts with little training data): yi,
syllabics, cherokee, vai, ogham, bamum. Sample a large block with --stride.

--block latin-cv is a control, not a codepoint block: it measures a fixed list
of ASCII consonant+vowel strings so the D5 baseline (Latin transliteration,
~1 token per syllable) is measured with the same method as the glyph blocks.
These strings are tokenizer probes only. They are not words of the language,
not a transliteration of any word, and must never be treated as one (CLAUDE.md
rule 3); the language has no Latin form.

--see-check adds one extra request per run: the first 8 sampled glyphs, one
each, with the question "how many non-ASCII characters are between the
brackets?". D20 used this test to show the BMP PUA never reaches the model.
The reply is recorded verbatim in meta.see_check. Not applicable to latin-cv.

Backends
--------
  --backend anthropic   (default) Messages count_tokens; free; needs ANTHROPIC_API_KEY.
  --backend openrouter  OpenRouter has no count endpoint, so send a 1-token
                        completion with usage accounting on ("usage":
                        {"include": true}); usage.prompt_tokens is then the
                        provider's NATIVE count (verified against
                        /api/v1/generation native_tokens_prompt; without usage
                        accounting OpenRouter reports a normalized count, and
                        the generation endpoint lags the completion by several
                        seconds and 404s until then). Needs OPENROUTER_API_KEY.
                        Whole BMP PUA block on Haiku costs well under a dollar;
                        the tokenizer is shared across Claude models, so
                        Haiku's count is the count.

A cost of 0 means the codepoint was stripped from the input before
tokenization: the model never sees it, so it is unusable, not cheap. The
script counts these in meta.stripped_codepoints and excludes them from the
"costs" table.

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
DEFAULT_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",
    "openrouter": "anthropic/claude-haiku-4.5",
}
# Some endpoints reject an empty message, so every measured string sits after
# this prefix; it is in the baseline too, so it cancels in the difference.
PREFIX = "."

BLOCKS = {
    "pua": (0xE000, 0xF8FF),       # Basic Multilingual Plane Private Use Area
    "pua-a": (0xF0000, 0xFFFFD),   # Supplementary Private Use Area-A (plane 15)
    "pua-b": (0x100000, 0x10FFFD),  # Supplementary Private Use Area-B (plane 16)
    "hangul": (0xAC00, 0xD7A3),    # precomposed Hangul syllables (D6 experiment)
    # O6 comparison points: real BMP scripts with thin training data.
    "yi": (0xA000, 0xA48C),        # Yi Syllables
    "syllabics": (0x1400, 0x167F),  # Unified Canadian Aboriginal Syllabics
    "cherokee": (0x13A0, 0x13F5),  # Cherokee (uppercase block)
    "vai": (0xA500, 0xA62B),       # Vai
    "ogham": (0x1680, 0x169C),     # Ogham
    "bamum": (0xA6A0, 0xA6EF),     # Bamum
}

# Control block: ASCII consonant+vowel strings measured by the same method, so
# the D5 baseline is on the same footing as the glyph blocks. Tokenizer probes
# only; not words, not transliterations of words (CLAUDE.md rule 3).
PROBE_STRINGS = {
    "latin-cv": ["ka", "ti", "mo", "su", "ne", "pa", "ri", "lo", "hu", "me",
                 "ta", "ki", "no", "ru", "se", "ma", "pi", "to", "nu", "le"],
}

SEE_CHECK_PROMPT = ("Between the square brackets on the next line is a string of "
                    "exactly 8 characters. How many of them are non-ASCII characters? "
                    "Reply with a single integer and nothing else.\n[{run}]")

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
        "usage": {"include": True},
    }, retry_on_missing=lambda o: "usage" not in o)
    return int(out["usage"]["prompt_tokens"])


def ask(text, model, api_key, backend):
    """One short completion; returns the reply text (for --see-check)."""
    if backend == "openrouter":
        out = http_json(OPENROUTER_URL, {"authorization": f"Bearer {api_key}"}, {
            "model": model,
            "messages": [{"role": "user", "content": text}],
            "max_tokens": 16,
            "temperature": 0,
        })
        return out["choices"][0]["message"]["content"].strip()
    out = http_json(ANTHROPIC_URL.replace("/count_tokens", ""),
                    {"x-api-key": api_key, "anthropic-version": ANTHROPIC_VERSION},
                    {"model": model, "max_tokens": 16,
                     "messages": [{"role": "user", "content": text}]})
    return "".join(b.get("text", "") for b in out["content"]).strip()


def dry_count(text):
    # Offline stand-in: assume byte-level fallback (1 token per UTF-8 byte)
    # on top of a fixed message overhead. An estimate, never a measurement.
    return 7 + len(text.encode("utf-8"))


def key_of(item):
    """JSON key: hex codepoint for a glyph, the string itself for a probe."""
    return f"{item:04X}" if isinstance(item, int) else item


def item_of(key, block):
    return key if block in PROBE_STRINGS else int(key, 16)


def text_of(item):
    return chr(item) if isinstance(item, int) else item


def load_existing(path, resume):
    if resume and path.exists():
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        block = data.get("meta", {}).get("block")
        costs = {item_of(k, block): v for k, v in data.get("costs", {}).items()}
        costs.update({item_of(k, block): 0.0 for k in data.get("stripped", [])})
        return costs, data.get("meta", {})
    return {}, {}


def write(path, meta, costs):
    ordered = sorted(costs.items(), key=lambda kv: (kv[1], kv[0]))
    stripped = [item for item, cost in ordered if cost <= 0]
    out = {
        "meta": {**meta, "stripped_codepoints": len(stripped),
                 "stripped_note": "cost 0 = removed from the input before tokenization; "
                                  "the model never sees the glyph. Unusable, not cheap."},
        "costs": {key_of(item): cost for item, cost in ordered if cost > 0},
        "stripped": [key_of(item) for item in stripped],
    }
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--block", choices=list(BLOCKS) + list(PROBE_STRINGS), default="pua")
    ap.add_argument("--backend", choices=("anthropic", "openrouter"), default="anthropic")
    ap.add_argument("--model", default=None, help="default depends on --backend")
    ap.add_argument("--repeats", type=int, default=16)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="measure only the first N codepoints (smoke test)")
    ap.add_argument("--stride", type=int, default=1, help="measure every Nth codepoint (sampling a large block)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--no-resume", action="store_true", help="discard an existing output file")
    ap.add_argument("--dry-run", action="store_true", help="no network; byte-count estimate only")
    ap.add_argument("--see-check", action="store_true",
                    help="also ask the model how many non-ASCII characters it sees in a run of "
                         "the first 8 sampled glyphs; reply recorded in meta.see_check")
    args = ap.parse_args()

    if args.block in PROBE_STRINGS:
        codepoints = list(PROBE_STRINGS[args.block])[:: args.stride]
    else:
        lo, hi = BLOCKS[args.block]
        codepoints = list(range(lo, hi + 1, args.stride))
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
                  or meta.get("stride", 1) != args.stride
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
        "stride": args.stride,
        "estimated": args.dry_run,
        "unit": "tokens per glyph, marginal, inside a run of `repeats` copies",
        "baseline_tokens": base,
    }
    if args.block in PROBE_STRINGS:
        meta["probe_note"] = ("ASCII tokenizer probes measured as a control for the glyph blocks. "
                              "Not words, not transliterations of words; the language has no Latin form.")

    if args.see_check:
        if args.block in PROBE_STRINGS or args.dry_run:
            meta["see_check"] = {"applicable": False,
                                 "why": "ASCII probe strings" if args.block in PROBE_STRINGS else "dry run"}
        else:
            probe = codepoints[:8]
            run = "".join(chr(cp) for cp in probe)
            reply = ask(SEE_CHECK_PROMPT.format(run=run), model, api_key, args.backend)
            meta["see_check"] = {"applicable": True, "glyphs": [f"{cp:04X}" for cp in probe],
                                 "question": "how many of these 8 characters are non-ASCII",
                                 "reply": reply}
            print(f"see-check: model reports {reply!r} non-ASCII characters in a run of 8")

    def measure(item):
        return item, (counter(PREFIX + text_of(item) * args.repeats) - base) / args.repeats

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
    print("cost histogram (tokens/glyph: count; 0 = stripped, unusable):")
    for c in sorted(hist):
        print(f"  {c:.3f}: {hist[c]}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
