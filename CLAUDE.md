# Instructions for Claude Code

1. Read `STATE.md` first, every session; it is the current state and points to the specs. `decisions.md` is the append-only history: read the entries STATE cites when you need the rationale, and the whole file only when reconsidering a decision.
2. Files are the source of truth. Never rely on recall of a rule or word; check the file.
3. Words are written ONLY in the script (the 74 Hangul syllable blocks in `spec/codepoints.json`). No Latin transliteration exists anywhere in this repo, not in comments, not in filenames, not in tests. IPA in `spec/phonology.md` describes sounds; it is not a way of writing words. **Exception, a trial (D142, revertible via `REVERT_D142.md`):** a *name* that is not a word of the language — a file name, format, tool, command, version, error code — is carried in its own spelling as printable-ASCII tokens in an `st` field, directly after the root that says what it is (`file CSV`). A stone word is still never written in Latin, and a foreign name is never respelled in Hangul.
4. New lexicon entries go through `scripts/validate.py`, never straight into `lexicon/lexicon.json`.
5. Any decision that changes the language or the method gets appended to `decisions.md` with a date and a one-line rationale, and `STATE.md` is updated to match.
6. Run `scripts/validate.py` and `scripts/regression_test.py` before every commit. The first checks the corpus; the second checks the checks, against the pre-correction form of every line ever corrected.
