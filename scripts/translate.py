#!/usr/bin/env python3
"""Translation tool.

Three layers (D72):
  1. Deterministic parse and gloss. Every sentence parses exactly one way, so
     stone -> morpheme gloss needs no model and is always exact.
  2. The validator as a guardrail. Anything this tool emits in the script is
     parsed before you see it; ill-formed output is rejected and retried, never
     shown as if it were a translation.
  3. A model, for natural English out and for composing in. English -> stone
     can never be mechanical: the English does not say how the speaker knows,
     and every predicate needs an evidential, so something must choose. The
     tool prints the choice instead of hiding it.

Commands (layers 1-2, no network, no key):
  gloss    "<stone>"     morpheme-by-morpheme gloss
  check    "<stone>"     say whether it is well formed, and why not
  lookup   <english>     lexicon entries matching an English word
  examples <english>     corpus sentences whose English contains the word

Commands (layer 3, need OPENROUTER_API_KEY):
  to-english "<stone>"   natural English
  to-stone   "<english>" compose, validate, retry; prints the gloss back
  roundtrip  "<english>" to-stone, then gloss the result so you can see what
                         the language added or dropped

The round trip is the one to use when it matters: the gloss coming back is
produced by layer 1, not by the model, so it cannot flatter the translation.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence  # noqa: E402

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"
RETRY_CODES = (408, 429, 500, 502, 503, 504, 529)


# ---------------------------------------------------------------- layers 1-2

def load_corpus():
    p = ROOT / "corpus/corpus.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_gloss(args, lx):
    s = parse_sentence(args.text, lx)
    print(s.gloss())
    for e in s.errors:
        print("  problem:", e, file=sys.stderr)
    return 0 if s.ok else 1


def cmd_check(args, lx):
    s = parse_sentence(args.text, lx)
    print(s.gloss())
    if s.ok:
        print("well formed" + (" (question: evidential slot correctly empty)" if s.is_question else ""))
        return 0
    for e in s.errors:
        print("FAIL", e)
    return 1


def cmd_lookup(args, lx):
    hits = lx.search_english(args.text)
    if not hits:
        print(f"nothing in the lexicon matches {args.text!r}")
        return 1
    for e in hits:
        print(f"{e['form']}  {e['id']}  {e['pos']:5}  {e['gloss']}")
        if e.get("sense_notes"):
            print(f"      {e['sense_notes']}")
    return 0


def cmd_examples(args, lx):
    q = args.text.lower()
    hits = [s for s in load_corpus() if q in s["en"].lower()]
    if not hits:
        print(f"no corpus sentence's English contains {args.text!r}")
        return 1
    for s in hits[: args.limit]:
        print(f"{s['id']}  {s['st']}")
        print(f"        {s['en']}")
        print(f"        {parse_sentence(s['st'], lx).gloss()}")
    print(f"({len(hits)} matching, showing {min(len(hits), args.limit)})")
    return 0


# ------------------------------------------------------------------ layer 3

def call_model(messages, model, api_key, retries=5):
    body = {"model": model, "messages": messages, "temperature": 0}
    data = json.dumps(body).encode("utf-8")
    delay = 1.0
    for attempt in range(retries):
        req = urllib.request.Request(OPENROUTER_URL, data=data, method="POST", headers={
            "content-type": "application/json", "authorization": f"Bearer {api_key}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                out = json.load(resp)
            return out["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            if e.code in RETRY_CODES and attempt < retries - 1:
                time.sleep(delay); delay *= 2; continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}")
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries - 1:
                time.sleep(delay); delay *= 2; continue
            raise
    raise RuntimeError("gave up calling the model")


def relevant_examples(text, lx, n=40, english_side=True):
    """Corpus sentences that share the most words with `text`."""
    corpus = [s for s in load_corpus() if s["split"] == "train"]
    if english_side:
        want = {w.strip(".,;:?!").lower() for w in text.split()}
        score = lambda s: len(want & {w.strip(".,;:?!").lower() for w in s["en"].split()})
    else:
        want = set(text.replace(" ", ""))
        score = lambda s: len(want & set(s["st"].replace(" ", "")))
    ranked = sorted(corpus, key=score, reverse=True)
    return ranked[:n]


def context_block(lx, examples):
    lexicon = "\n".join(f"{e['form']}\t{e['gloss']}" for e in lx.entries)
    grammar = (ROOT / "spec/grammar.md").read_text(encoding="utf-8")
    ex = "\n".join(f"{s['en']} ||| {s['st']}" for s in examples)
    return (f"GRAMMAR\n{grammar}\n\nLEXICON (glyph\tmeaning)\n{lexicon}\n\n"
            f"CORPUS EXAMPLES (English ||| the language)\n{ex}\n")


def cmd_to_english(args, lx):
    key = require_key()
    ex = relevant_examples(args.text, lx, english_side=False)
    parsed = parse_sentence(args.text, lx)
    if not parsed.ok:
        print("That is not well-formed; fix it first:", file=sys.stderr)
        for e in parsed.errors:
            print("  ", e, file=sys.stderr)
        return 1
    prompt = (context_block(lx, ex) +
              f"\nThe morpheme gloss of the sentence is: {parsed.gloss()}\n"
              f"Sentence: {args.text}\n\n"
              "Give the most natural English. Render the evidential and any stance as the natural "
              "English cue the corpus uses, never as a bracketed label. Reply with the English only.")
    print(call_model([{"role": "user", "content": prompt}], args.model, key))
    return 0


def compose(text, lx, model, key, attempts=3, verbose=True):
    """English -> stone, validated, retried on malformed output."""
    ex = relevant_examples(text, lx, english_side=True)
    base = (context_block(lx, ex) +
            f"\nTranslate this English into the language: {text}\n\n"
            "Rules you must follow: every predicate carries an evidential unless the sentence ends "
            "in the question particle; affixes are written solid with their root in the order "
            "negation, tense, evidential, stance, subordinator; function words are separate. "
            "Use only glyphs from the lexicon above.\n"
            "Reply with two lines and nothing else:\n"
            "LINE1: the translation\n"
            "LINE2: one sentence saying which evidential and stance you chose and why, since the "
            "English does not state them.")
    messages = [{"role": "user", "content": base}]
    for attempt in range(1, attempts + 1):
        reply = call_model(messages, model, key)
        lines = [l for l in reply.splitlines() if l.strip()]
        cand = lines[0].replace("LINE1:", "").strip() if lines else ""
        note = lines[1].replace("LINE2:", "").strip() if len(lines) > 1 else ""
        parsed = parse_sentence(cand, lx)
        if parsed.ok:
            return cand, note, parsed, attempt
        if verbose:
            print(f"attempt {attempt} rejected by the validator:", file=sys.stderr)
            for e in parsed.errors:
                print("  ", e, file=sys.stderr)
        messages += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": "That is not well formed. Problems: "
                      + "; ".join(parsed.errors) + ". Try again, same two-line format."}]
    return None, None, parsed, attempts


def cmd_to_stone(args, lx):
    key = require_key()
    cand, note, parsed, n = compose(args.text, lx, args.model, key)
    if cand is None:
        print("Could not produce a well-formed sentence; last attempt's problems:", file=sys.stderr)
        for e in parsed.errors:
            print("  ", e, file=sys.stderr)
        return 1
    print(cand)
    print(f"  gloss:  {parsed.gloss()}")
    if note:
        print(f"  chose:  {note}")
    if n > 1:
        print(f"  ({n} attempts; earlier ones were rejected by the validator)")
    return 0


def cmd_roundtrip(args, lx):
    key = require_key()
    cand, note, parsed, n = compose(args.text, lx, args.model, key)
    if cand is None:
        print("Could not produce a well-formed sentence.", file=sys.stderr)
        return 1
    ex = relevant_examples(cand, lx, english_side=False)
    back = call_model([{"role": "user", "content": context_block(lx, ex) +
                        f"\nThe morpheme gloss is: {parsed.gloss()}\nSentence: {cand}\n\n"
                        "Give the most natural English. Render evidential and stance as natural "
                        "English cues. Reply with the English only."}], args.model, key)
    print(f"in    : {args.text}")
    print(f"stone : {cand}")
    print(f"gloss : {parsed.gloss()}")
    if note:
        print(f"chose : {note}")
    print(f"back  : {back}")
    print("\nCompare the first and last lines. The gloss between them is produced by the parser, "
          "not the model, so it cannot flatter the translation.")
    return 0


def require_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY is not set; layers 1 and 2 (gloss, check, lookup, examples) "
              "work without it.", file=sys.stderr)
        raise SystemExit(2)
    return key


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default=DEFAULT_MODEL)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, helptext in [
        ("gloss", cmd_gloss, "morpheme gloss of a sentence in the script"),
        ("check", cmd_check, "say whether a sentence is well formed"),
        ("lookup", cmd_lookup, "lexicon entries matching an English word"),
        ("examples", cmd_examples, "corpus sentences whose English contains a word"),
        ("to-english", cmd_to_english, "natural English (needs a key)"),
        ("to-stone", cmd_to_stone, "compose and validate (needs a key)"),
        ("roundtrip", cmd_roundtrip, "compose, then gloss back (needs a key)"),
    ]:
        p = sub.add_parser(name, help=helptext)
        p.add_argument("text")
        if name == "examples":
            p.add_argument("--limit", type=int, default=8)
        p.set_defaults(func=fn)
    args = ap.parse_args()
    return args.func(args, Lexicon())


if __name__ == "__main__":
    sys.exit(main())
