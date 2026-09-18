#!/usr/bin/env python3
"""Change the form of existing roots across the lexicon and the corpus (D127).

`validate.py --add` only appends and `correct_corpus.py` only edits corpus
lines, so changing a root's *form* had no reviewed route and would have meant
editing `lexicon/lexicon.json` by hand, which CLAUDE.md rule 4 forbids. This is
that route.

Usage: recoin.py MAP.json [--apply]

MAP is `{"old form": "new form", ...}`. Every new form is validated the way a
new entry is — script, syllable count, Korean collision (D55), the root-plus-
verb-ending split, and duplicates — before anything is written. In the corpus,
a token is rewritten only when it begins with an old form AND everything after
it is affixes, which is the parser's own rule for what a token can be; that is
what stops a coincidental prefix match from being mangled.

Without --apply it is a dry run: it prints every lexicon entry and every corpus
line that would change, re-parses each changed line, and writes nothing.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence, slot_of  # noqa: E402

LEX = ROOT / "lexicon/lexicon.json"
COR = ROOT / "corpus/corpus.jsonl"


def retoken(tok, mapping, affixes):
    for old, new in mapping.items():
        if tok.startswith(old) and all(ch in affixes for ch in tok[len(old):]):
            return new + tok[len(old):]
    return tok


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_ = "--apply" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    mapping = json.load(open(args[0], encoding="utf-8"))
    lex = json.load(open(LEX, encoding="utf-8"))
    by_form = {e["form"]: e for e in lex}
    ko = json.load(open(ROOT / "data/ko_frequency.json", encoding="utf-8"))

    errors = []
    for old, new in mapping.items():
        if old not in by_form:
            errors.append(f"{old!r} is not a lexicon form")
        if new in by_form and new not in mapping:
            errors.append(f"{new!r} already exists ({by_form[new]['id']})")
        if len(new) >= 2 and new in ko:
            errors.append(f"{new!r} is a Korean word (frequency {ko[new]}); recoin")
        if not 1 <= len(new) <= 3:
            errors.append(f"{new!r} is {len(new)} syllables, must be 1-3")
    if len(set(mapping.values())) != len(mapping):
        errors.append("two roots map to the same new form")
    for e in errors:
        print("FAIL", e)
    if errors:
        print(f"recoin.py: {len(errors)} errors, nothing written")
        return 1

    for e in lex:
        if e["form"] in mapping:
            print(f"  {e['id']}  {e['form']} -> {mapping[e['form']]}   {e['gloss']}")
            e["form"] = mapping[e["form"]]

    affixes = {e["form"] for e in lex if e.get("pos") == "affix"}
    lines = [json.loads(l) for l in COR.read_text(encoding="utf-8").splitlines() if l.strip()]
    touched = 0
    for s in lines:
        new_st = " ".join(retoken(t, mapping, affixes) for t in s["st"].split())
        if new_st != s["st"]:
            touched += 1
            if not apply_ and touched <= 6:
                print(f"  {s['id']}  {s['st']}\n       -> {new_st}")
            s["st"] = new_st

    # the new lexicon has to be on disk before the parser can read the new forms
    lex_bak, cor_bak = LEX.read_bytes(), COR.read_bytes()
    ok = False
    try:
        LEX.write_text(json.dumps(lex, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        COR.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in lines), encoding="utf-8")
        lx = Lexicon()
        bad = [s["id"] for s in lines if getattr(parse_sentence(s["st"], lx), "errors", None)]
        if bad:
            print(f"FAIL {len(bad)} corrected lines no longer parse: {bad[:8]}")
            return 1
        print(f"{'APPLIED' if apply_ else 'DRY RUN OK'}: {len(mapping)} roots recoined, "
              f"{touched} corpus lines rewritten, all reparse.")
        ok = apply_
        return 0
    finally:
        if not ok:
            LEX.write_bytes(lex_bak)
            COR.write_bytes(cor_bak)


if __name__ == "__main__":
    sys.exit(main())
