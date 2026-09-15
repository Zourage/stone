#!/usr/bin/env python3
"""Validate lexicon + corpus. Run before every commit. Exit 1 on any failure.

Implemented now (spec/codepoints.json exists, D28):
  - every lexicon form and corpus `st` string uses only the 74 codepoints
  - no duplicate forms, no duplicate glosses
  - form length 1-3 syllables (D37)
  - pos is one of the schema enum (D29, D33)
  - no Latin letters anywhere in `form` or `st` (CLAUDE.md rule 3)
  - no form of 2+ syllables is a Korean word (data/ko_frequency.json; D13, D55)
  - no multi-syllable form splits into a shorter root plus a valid run of
    affixes, which would make the word ambiguous with an inflected shorter one

Corpus checks (D11, D15, D25, D43):
  - every `st` token is a known word: a func/root/num word alone, or a root
    followed by affixes in template order (neg, tense, evid, stance, sub);
    the evidential is required unless the sentence ends in the question particle
  - coverage REPORT (not yet a failure while the corpus is small): words with
    <3 train sentences, features with <10, held share, and the share of
    sentences whose stone and English word counts are equal (relexification proxy)
  - convention REPORT, heuristic so not an error: sentences that front an
    adverbial before a pronoun subject (D78 says subject first) and gnomic
    general-evidential sentences whose English carries no general cue (D79)

--add FILE: FILE is a JSON list of entries (or one entry). Each is validated
against the schema and the current lexicon, then appended. Nothing is written
if any entry fails. Ids are assigned here (w0001, ...); `added` defaults to today.
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import Lexicon, check_script as _check_script, parse_sentence, slot_of  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.load(open(ROOT / "lexicon/schema.json"))
POS = set(SCHEMA["properties"]["pos"]["enum"])
KO = json.load(open(ROOT / "data/ko_frequency.json", encoding="utf-8"))
_LX_FOR_SCRIPT = Lexicon()


def check_script(s, where, errors):
    for msg in _check_script(s, _LX_FOR_SCRIPT):
        errors.append(f"{where}: {msg}")


def ambiguous_split(entry, lex):
    """Return the shorter base if this form could be read as base + verb ending."""
    if entry.get("pos") == "affix" or len(entry["form"]) < 2:
        return None
    bases = {e["form"]: e for e in lex
             if e.get("pos") in ("root", "num") or e.get("gloss", "").startswith("pronoun")}
    affixes = {e["form"]: slot_of(e) for e in lex if e.get("pos") == "affix"}
    f = entry["form"]
    for k in range(1, len(f)):
        if f[:k] not in bases:
            continue
        rest = f[k:]
        if not all(ch in affixes for ch in rest):
            continue
        slots = [affixes[ch] for ch in rest]
        if all(a < b for a, b in zip(slots, slots[1:])):
            return f[:k]
    return None


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
        clash = ambiguous_split(e, lex)
        if clash:
            errors.append(f"{e['id']}: form {e['form']!r} reads as {clash} plus a verb ending; recoin")
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


GENERAL_CUES = ("how it is", "everyone knows", "as such", "known", "by definition")


def convention_report(sents, lx):
    """Heuristic counts for the two conventions the corpus has broken before."""
    g = lambda gloss: next(e["form"] for e in lx.entries if e["gloss"] == gloss)  # noqa: E731
    pron = {e["form"] for e in lx.entries if e["gloss"].startswith("pronoun")}
    cases = {e["form"] for e in lx.entries if e["gloss"].startswith("case")}
    rel = {e["form"] for e in lx.entries if e["gloss"].startswith("relational")}
    loc, sub, gen = g("case: location"), g("subordinator"), g("evidential: general")
    fronted = uncued = 0
    for s in sents:
        t = s["st"].split()
        if t and t[0] not in pron:
            for i, tok in enumerate(t):
                if tok in pron and i > 0:
                    if i + 1 < len(t) and t[i + 1] in cases:
                        break
                    pre = t[:i]
                    if loc in pre or any(x in rel for x in pre) or any(x.endswith(sub) for x in pre):
                        fronted += 1
                    break
        parsed = parse_sentence(s["st"], lx)
        preds = [tk for tk in parsed.tokens if tk.affixes]
        if preds and not parsed.is_question:
            forms = [a["form"] for a in preds[-1].affixes]
            if gen in forms and sub not in forms:
                if not any(c in s["en"].lower() for c in GENERAL_CUES):
                    uncued += 1
    return (f"conventions: {fronted} sentences front an adverbial before a pronoun subject (D78), "
            f"{uncued} gnomic general sentences with no English cue (D79)")


def check_corpus(lex, errors):
    """Parse every corpus sentence with stonelib and report coverage."""
    lx = Lexicon(lex)
    corpus_path = ROOT / "corpus/corpus.jsonl"
    if not corpus_path.exists():
        return 0
    sents = [json.loads(l) for l in corpus_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    word_count = {e["id"]: 0 for e in lex}
    feat_count = {}
    same_len = 0
    for s in sents:
        parsed = parse_sentence(s["st"], lx)
        for msg in parsed.errors:
            errors.append(f"{s['id']}: {msg}")
        if s["split"] == "train":
            seen = {e["id"] for t in parsed.tokens
                    for e in ([t.base] if t.base else []) + t.affixes}
            for wid in seen:                      # distinct sentences, not occurrences (D11)
                word_count[wid] = word_count.get(wid, 0) + 1
            for f in s["features"]:
                feat_count[f] = feat_count.get(f, 0) + 1
        if len(s["en"].replace(".", " ").replace(",", " ").split()) == len(s["st"].split()):
            same_len += 1
    conv = convention_report(sents, lx)
    n = len(sents)
    if n:
        print(conv)
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
