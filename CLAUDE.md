# Instructions for Claude Code

1. Read `STATE.md` first, every session; it is the current state and points to the specs. `decisions.md` is the append-only history: read the entries STATE cites when you need the rationale, and the whole file only when reconsidering a decision.
2. Files are the source of truth. Never rely on recall of a rule or word; check the file.
3. Words are written ONLY in the script (the 74 Hangul syllable blocks in `spec/codepoints.json`). No Latin transliteration exists anywhere in this repo, not in comments, not in filenames, not in tests. IPA in `spec/phonology.md` describes sounds; it is not a way of writing words.
4. New lexicon entries go through `scripts/validate.py`, never straight into `lexicon/lexicon.json`.
5. Any decision that changes the language or the method gets appended to `decisions.md` with a date and a one-line rationale, and `STATE.md` is updated to match.
6. Run `scripts/validate.py` before every commit.
