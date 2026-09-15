# Tests

## Acceptance test (D3, bar set in D50)
Protocol: a fresh session with no file access, context = the corpus **train** split only, as `English ||| stone` pairs. No spec, no lexicon, no grammar. Ask it to translate every `held` sentence in both directions and to state the rules it inferred.

The bar that counts as done: **stone → English 100% meaning-correct, English → stone ≥90% exact**, with every miss read by hand and judged grammatical. A miss that is ungrammatical or changes meaning fails the run.

Score exact match first, then read the near-misses. A miss caused by a word that has no train sentence is a corpus gap, not a model failure; fix the corpus and say so in the result file.

Record each run in `results/` as `YYYY-MM-DD.md` with the corpus and lexicon size, both scores, the rules the agent inferred, what it got wrong, and a verdict.

## Drift test (D15) — never yet run
A fixed sentence set translated at turn 1 and again at turn 40 of a long session. Any divergence is a bug. This is the instrument for the priors accepted in D52: it is what would catch output sliding toward Korean over a long session.

## Translation protocol (D72) — not a test
For actually using the language, unlike the acceptance test, give the model everything: `spec/grammar.md`, `lexicon/lexicon.json` and the corpus. Withholding them is a property of the test, not of normal use.

`scripts/translate.py` is the tool. Its `gloss`, `check`, `lookup` and `examples` commands are deterministic and need no key. Its `to-english`, `to-stone` and `roundtrip` commands call a model and need `OPENROUTER_API_KEY`. Anything the tool emits in the script is parsed before you see it, so ill-formed output is retried rather than shown.
