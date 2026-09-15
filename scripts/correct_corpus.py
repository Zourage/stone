#!/usr/bin/env python3
"""Correct existing corpus lines (O8).

`merge_batch.py` only appends, and CLAUDE.md rule 4 forbids editing the corpus
by hand, so until now a line that was wrong stayed wrong. This is the reviewed
route: corrections go in a JSON file, every corrected line is re-parsed, and
nothing is written unless all of them are well formed.

Usage: correct_corpus.py FILE [--apply]

FILE is a JSON list of objects, each with an existing "id" and whichever of
"st", "en", "features", "split" should change. Anything not named is left
alone. Without --apply it is a dry run: it prints the before and after of each
line, with the parser's gloss for both, and writes nothing.

Every correction must say why, in a "why" field. The why is not stored in the
corpus; it is printed, so the reviewer sees the reason next to the change, and
it belongs in the decisions entry that accompanies the correction.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence  # noqa: E402

CORPUS = ROOT / "corpus/corpus.jsonl"
FIELDS = ("st", "en", "features", "split")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_ = "--apply" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    corrections = json.load(open(args[0], encoding="utf-8"))
    if isinstance(corrections, dict):
        corrections = [corrections]
    lx = Lexicon()
    lines = [json.loads(l) for l in CORPUS.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_id = {s["id"]: s for s in lines}

    errors, changed = [], 0
    for c in corrections:
        sid = c.get("id")
        if sid not in by_id:
            errors.append(f"{sid}: no such corpus line")
            continue
        if not c.get("why"):
            errors.append(f"{sid}: correction has no 'why'")
        before = dict(by_id[sid])
        after = dict(before)
        for f in FIELDS:
            if f in c:
                after[f] = c[f]
        if after == before:
            errors.append(f"{sid}: correction changes nothing")
            continue
        parsed = parse_sentence(after["st"], lx)
        for msg in parsed.errors:
            errors.append(f"{sid}: corrected line does not parse: {msg}")
        changed += 1
        print(f"{sid}  {c.get('why','')}")
        if before["st"] != after["st"]:
            print(f"   was  {before['st']}")
            print(f"        {parse_sentence(before['st'], lx).gloss()}")
            print(f"   now  {after['st']}")
            print(f"        {parsed.gloss()}")
        if before["en"] != after["en"]:
            print(f"   was  {before['en']}")
            print(f"   now  {after['en']}")
        by_id[sid] = after

    for e in errors:
        print("FAIL", e)
    if errors:
        print(f"{len(errors)} problems; nothing written")
        return 1
    if not apply_:
        print(f"DRY RUN OK: {changed} lines would be corrected. Nothing written.")
        return 0
    with CORPUS.open("w", encoding="utf-8") as f:
        for s in lines:
            f.write(json.dumps(by_id[s["id"]], ensure_ascii=False) + "\n")
    print(f"APPLIED: {changed} lines corrected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
