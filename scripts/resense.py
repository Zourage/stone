#!/usr/bin/env python3
"""Change the gloss or sense notes of existing lexicon entries (D140).

`validate.py --add` only appends, `recoin.py` only changes forms and
`correct_corpus.py` only edits corpus lines, so narrowing what a word means had
no reviewed route and would have meant editing `lexicon/lexicon.json` by hand,
which CLAUDE.md rule 4 forbids. This is that route.

Usage: resense.py FILE [--apply]

FILE is a JSON list of objects, each with an existing "id", whichever of
"gloss" and "sense_notes" should change, and a "why". Without --apply it is a
dry run: it prints the before and after of each entry and writes nothing. With
--apply it writes the lexicon, runs validate.py, and restores the old lexicon
if validation fails.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEX = ROOT / "lexicon/lexicon.json"
FIELDS = ("gloss", "sense_notes")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_ = "--apply" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    changes = json.load(open(args[0], encoding="utf-8"))
    if isinstance(changes, dict):
        changes = [changes]
    raw = LEX.read_bytes()
    lex = json.loads(raw)
    by_id = {e["id"]: e for e in lex}

    errors, n = [], 0
    for c in changes:
        e = by_id.get(c.get("id"))
        if e is None:
            errors.append(f"{c.get('id')}: no such lexicon entry")
            continue
        if not c.get("why"):
            errors.append(f"{e['id']}: change has no 'why'")
        if not any(f in c for f in FIELDS) or set(c) - set(FIELDS) - {"id", "why"}:
            errors.append(f"{e['id']}: may change only {FIELDS}")
            continue
        if all(c.get(f, e.get(f)) == e.get(f) for f in FIELDS):
            errors.append(f"{e['id']}: change changes nothing")
            continue
        n += 1
        print(f"{e['id']} {e['form']}  {c.get('why', '')}")
        for f in FIELDS:
            if f in c and c[f] != e.get(f):
                print(f"   {f} was: {e.get(f)}")
                print(f"   {f} now: {c[f]}")
                e[f] = c[f]

    for m in errors:
        print("FAIL", m)
    if errors:
        print(f"{len(errors)} problems; nothing written")
        return 1
    if not apply_:
        print(f"DRY RUN OK: {n} entries would change. Nothing written.")
        return 0
    LEX.write_text(json.dumps(lex, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], capture_output=True, text=True)
    if r.returncode != 0:
        LEX.write_bytes(raw)
        print(r.stdout + r.stderr)
        print("validate.py failed; lexicon restored")
        return 1
    print(f"APPLIED: {n} entries changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
