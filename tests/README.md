# Tests

## Acceptance test (D3, bar set in D50, directions split in D75)
Protocol: fresh agents with no access to this repo, context = the corpus **train** split only, as `English ||| stone` pairs. No spec, no lexicon, no grammar. Ask for every `held` sentence in both directions, for the rules inferred, and whether the language is a known one.

**The two directions go to different agents** (D75). One agent given both sides of a held sentence has the answer to the English → stone item sitting in its own prompt; tests 1 and 2 were run that way and the leak was real. Split the held set into chunks, give one set of agents only the stone side and another set only the English side, and every sentence still gets both directions with no agent seeing both sides of one sentence. Splitting by chunk also keeps each prompt manageable; total the scores and say in the result file how it was split.

The bar that counts as done: **stone → English 100% meaning-correct, English → stone ≥90% exact**, with every miss read by hand and judged grammatical. A miss that is ungrammatical or changes meaning fails the run.

Score exact match first, then read the near-misses. A miss caused by a word or construction that has no train sentence is a corpus gap, not a model failure; fix the corpus and say so in the result file. A miss caused by the corpus contradicting itself, or by a point the spec never decided, is neither — log it as a grammar gap and say so.

Record each run in `results/` as `YYYY-MM-DD.md` with the corpus and lexicon size, both scores, the rules the agent inferred, what it got wrong, and a verdict.

## Drift test (D15, protocol fixed in D74)
`scripts/drift_test.py` is the executable form of this protocol; the prose here and the script must say the same thing.

Twelve **fixed** probe sentences — the list in the script, spanning all four evidentials, all six stances, negation, past and future, the conditional, all four modals and both quantifiers — are translated at the start of one long model conversation. Forty turns of other, plausible work follow in the same session. Then the same twelve are asked for again, in a different order and without being called repeats. The materials are the full set, per the translation protocol below, not the acceptance-test subset: this measures use, not learning.

Three signals, because the first one alone cannot be read:

1. **Probe divergence.** Early round against late round, token for token. Confounded: at the late round the model can see its own early answers and may simply copy them, so zero divergence here is necessary but not sufficient.
2. **Filler accuracy, early half against late half.** Every filler turn asks for a train sentence the corpus already answers, so each turn is scored. Copying cannot flatter this.
   **This needs the control arm** (`--control`): the same forty sentences, same order, each in its own fresh one-turn conversation. The filler sentences are drawn in corpus order and the newer corpus is harder, so a late-half drop in the long run means nothing until the control shows whether the same drop happens without a long session. Run both; the long run against the control is the measurement.
3. **Korean leakage.** Every token the model emits anywhere in the session, checked against `data/ko_frequency.json`. A token that is a real Korean word and that the parser cannot read as a word of this language is the specific failure D52 left open. A legal inflected form may coincide with a Korean word by accident, so the parser filter is part of the check, not an optimisation.

Record as `results/YYYY-MM-DD-drift.md`. Changing the probe list makes a new test, not a new run of this one.

## Translation protocol (D72) — not a test
For actually using the language, unlike the acceptance test, give the model everything: `spec/grammar.md`, `lexicon/lexicon.json` and the corpus. Withholding them is a property of the test, not of normal use.

`scripts/translate.py` is the tool. Its `gloss`, `check`, `lookup` and `examples` commands are deterministic and need no key. Its `to-english`, `to-stone` and `roundtrip` commands call a model and need `OPENROUTER_API_KEY`. Anything the tool emits in the script is parsed before you see it, so ill-formed output is retried rather than shown.

What the guardrail does **not** catch is worth knowing before trusting it: it checks the verb template and the script, not argument roles or the modal construction, so a wrong case marker or a modal that has lost its subordinator comes back well formed. `check` prints an advisory for the modal case (D76); the rest is on the reader.
