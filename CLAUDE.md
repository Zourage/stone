# Instructions for Claude Code

1. Read `decisions.md` first, every session. It is the memory of this project.
2. Files are the source of truth. Never rely on recall of a rule or word; check the file.
3. Words are written ONLY in the script (PUA codepoints). No Latin transliteration exists anywhere in this repo, not in comments, not in filenames, not in tests. IPA in `spec/phonology.md` describes sounds; it is not a way of writing words.
4. New lexicon entries go through `scripts/validate.py`, never straight into `lexicon/lexicon.json`.
5. Any decision that changes the language or the method gets appended to `decisions.md` with a date and a one-line rationale.
6. Run `scripts/validate.py` before every commit.
