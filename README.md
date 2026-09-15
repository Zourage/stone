# stone

A private constructed language for two people. Working name; the language names itself later.

The primary artifact is `corpus/` — a parallel text (English ↔ stone) that serves as key, test set, and teaching material at once. Everything else is scaffolding to produce it.

**Definition of done:** a fresh model session given only the corpus can translate held-out sentences correctly in both directions.

Read `STATE.md` before doing anything; it points to the specs. `decisions.md` is the append-only history: append to it when you decide anything, then update `STATE.md`.

## Using it
```
python3 scripts/translate.py gloss    "<a sentence in the script>"   # morpheme gloss, no model
python3 scripts/translate.py check    "<a sentence in the script>"   # is it well formed?
python3 scripts/translate.py lookup   fault                          # what words mean this?
python3 scripts/translate.py examples "still"                        # how has this been said?
python3 scripts/translate.py roundtrip "The test failed."            # needs OPENROUTER_API_KEY
```
`scripts/README.md` lists every script. `tests/README.md` has the acceptance protocol and the translation protocol, which are deliberately different.
