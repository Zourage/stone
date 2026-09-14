#!/usr/bin/env python3
"""Validate lexicon + corpus. Run before every commit. Exit 1 on any failure.

Implemented now (spec/codepoints.json exists, D28):
  - every lexicon form and corpus `st` string uses only the 74 codepoints
  - no duplicate forms, no duplicate glosses
  - form length 1-3 syllables (D37)
  - pos is one of the schema enum (D29, D33)
  - no Latin letters anywhere in `form` or `st` (CLAUDE.md rule 3)
  - no form of 2+ syllables is a Korean word (data/ko_frequency.json; D13, D55)

Corpus checks (D11, D15, D25, D43):
  - every `st` token is a known word: a func/root/num word alone, or a root
    followed by affixes in template order (neg, tense, evid, stance, sub);
    the evidential is required unless the sentence ends in the question particle
  - coverage REPORT (not yet a failure while the corpus is small): words with
    <3 train sentences, features with <10, held share, and the share of
    sentences whose stone and English word counts are equal (relexification proxy)

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
KO = json.load(open(ROOT / "data/ko_frequency.json", encoding="utf-8"))


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
        if len(e["form"]) >= 2 and e["form"] in KO:
            errors.append(f"{e['id']}: form {e['form']!r} is a Korean word (frequency {KO[e['form']]}); recoin")
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


def check_corpus(lex, errors):
    by_form = {e["form"]: e for e in lex}
    slot_of = {}
    for e in lex:
        if e["pos"] != "affix":
            continue
        g = e["gloss"]
        slot_of[e["form"]] = (0 if g == "negation" else 1 if g.startswith("tense") else
                              2 if g.startswith("evidential") else 3 if g.startswith("stance") else 4)
    qp = next((e["form"] for e in lex if e["gloss"] == "question particle"), None)
    corpus_path = ROOT / "corpus/corpus.jsonl"
    if not corpus_path.exists():
        return 0
    sents = [json.loads(l) for l in corpus_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    word_count = {e["id"]: 0 for e in lex}
    feat_count = {}
    same_len = 0
    for s in sents:
        check_script(s["st"], s["id"], errors)
        toks = s["st"].split()
        is_q = bool(toks) and toks[-1] == qp
        seen = set()
        for t in toks:
            if t in by_form:
                seen.add(by_form[t]["id"])
                continue
            root = next((t[:k] for k in range(len(t), 0, -1)
                         if t[:k] in by_form and by_form[t[:k]]["pos"] in ("root", "num")
                         or t[:k] in by_form and by_form[t[:k]]["gloss"].startswith("pronoun")), None)
            if root is None:
                errors.append(f"{s['id']}: token {t!r} is not a word (no known root prefix)")
                continue
            rest = t[len(root):]
            seen.add(by_form[root]["id"])
            last, slots = -1, []
            for ch in rest:
                if ch not in slot_of:
                    errors.append(f"{s['id']}: {ch!r} in {t!r} is not an affix")
                    break
                sl = slot_of[ch]
                if sl <= last:
                    errors.append(f"{s['id']}: affixes out of template order in {t!r}")
                    break
                last = sl
                slots.append(sl)
                seen.add(by_form[ch]["id"])
            if 2 not in slots and not is_q:
                errors.append(f"{s['id']}: predicate {t!r} has no evidential and the sentence is not a question")
        if s["split"] == "train":
            for w in seen:
                word_count[w] += 1
            for f in s["features"]:
                feat_count[f] = feat_count.get(f, 0) + 1
        if len(s["en"].replace(".", " ").replace(",", " ").split()) == len(toks):
            same_len += 1
    n = len(sents)
    if n:
        thin = [w for w, c in word_count.items() if c < 3]
        weak = [f for f, c in feat_count.items() if c < 10]
        held = sum(1 for s in sents if s["split"] == "held")
        print(f"coverage: {len(thin)} words under 3 train sentences, {len(weak)} features under 10, "
              f"held {held}/{n}, same-length-as-English {same_len}/{n}")
    return n


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--add":
        return add(sys.argv[2])
    errors = []
    lex = json.load(open(ROOT / "lexicon/lexicon.json"))
    validate_entries(lex, errors)
    n_corpus = check_corpus(lex, errors)
    for err in errors:
        print("FAIL", err)
    print(f"validate.py: {len(lex)} lexicon entries, {n_corpus} corpus lines, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
