#!/usr/bin/env python3
"""Validate lexicon + corpus. Run before every commit. Exit 1 on any failure.

Implemented now (spec/codepoints.json exists, D28):
  - every lexicon form and corpus `st` string uses only the 74 codepoints
  - no duplicate forms, no duplicate glosses
  - form length 1-3 syllables (D37)
  - pos is one of the schema enum (D29, D33)
  - no Latin letters anywhere in `form` or `st` (CLAUDE.md rule 3)

Still to implement once there is a corpus (D11, D15, D25):
  - every lexicon word appears in >=3 train corpus sentences
  - every feature tag appears in >=10 train sentences
  - every corpus `st` string uses only known words
  - held/train split ratio
  - relexification (D25): flag sentences whose stone side matches the English
    side in word count and order; fail if too many

--add FILE: FILE is a JSON list of entries (or one entry). Each is validated
against the schema and the current lexicon, then appended. Nothing is written
if any entry fails. Ids are assigned here (w0001, ...); `added` defaults to today.
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODEPOINTS = {int(c, 16) for c in json.load(open(ROOT / "spec/codepoints.json"))["codepoints"]}
SCHEMA = json.load(open(ROOT / "lexicon/schema.json"))
POS = set(SCHEMA["properties"]["pos"]["enum"])
LATIN = re.compile(r"[A-Za-z]")


def check_script(s, where, errors):
    if LATIN.search(s):
        errors.append(f"{where}: Latin letters in script field")
    for ch in s:
        if ch != " " and ord(ch) not in CODEPOINTS:
            errors.append(f"{where}: U+{ord(ch):04X} is not one of the 74 syllables")


def validate_entries(lex, errors):
    forms, glosses = {}, {}
    for e in lex:
        missing = [k for k in SCHEMA["required"] if k not in e]
        if missing:
            errors.append(f"{e.get('id')}: missing {missing}")
            continue
        check_script(e["form"], e["id"], errors)
        if not 1 <= len(e["form"]) <= 3:
            errors.append(f"{e['id']}: form is {len(e['form'])} syllables, must be 1-3")
        if e["pos"] not in POS:
            errors.append(f"{e['id']}: pos {e['pos']!r} not in {sorted(POS)}")
        if e["form"] in forms:
            errors.append(f"{e['id']}: duplicate form of {forms[e['form']]}")
        forms[e["form"]] = e["id"]
        g = e["gloss"].strip().lower()
        if g in glosses:
            errors.append(f"{e['id']}: duplicate gloss of {glosses[g]}")
        glosses[g] = e["id"]


def add(path):
    lex = json.load(open(ROOT / "lexicon/lexicon.json"))
    new = json.load(open(path))
    if isinstance(new, dict):
        new = [new]
    today = datetime.date.today().isoformat()
    n = max((int(e["id"][1:]) for e in lex), default=0)
    for e in new:
        n += 1
        e.setdefault("id", f"w{n:04d}")
        e.setdefault("added", today)
    errors = []
    validate_entries(lex + new, errors)
    for err in errors:
        print("FAIL", err)
    if errors:
        print(f"--add: {len(errors)} errors, nothing written")
        return 1
    with open(ROOT / "lexicon/lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lex + new, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"--add: {len(new)} entries added, lexicon now {len(lex) + len(new)}")
    return 0


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--add":
        return add(sys.argv[2])
    errors = []
    lex = json.load(open(ROOT / "lexicon/lexicon.json"))
    validate_entries(lex, errors)
    n_corpus = 0
    corpus_path = ROOT / "corpus/corpus.jsonl"
    if corpus_path.exists():
        for line in corpus_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            s = json.loads(line)
            n_corpus += 1
            check_script(s["st"], s["id"], errors)
    for err in errors:
        print("FAIL", err)
    print(f"validate.py: {len(lex)} lexicon entries, {n_corpus} corpus lines, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
