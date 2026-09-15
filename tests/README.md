# Tests

## Acceptance test (D3, bar set in D50, directions split in D75)
Protocol: fresh agents with no access to this repo, context = the corpus **train** split only, as `English ||| stone` pairs. No spec, no lexicon, no grammar. Ask for every `held` sentence in both directions, for the rules inferred, and whether the language is a known one.

**The two directions go to different agents** (D75). One agent given both sides of a held sentence has the answer to the English → stone item sitting in its own prompt; tests 1 and 2 were run that way and the leak was real. Split the held set into chunks, give one set of agents only the stone side and another set only the English side, and every sentence still gets both directions with no agent seeing both sides of one sentence. Splitting by chunk also keeps each prompt manageable; total the scores and say in the result file how it was split.

**A held sentence may not be a copy of a train sentence** (D93). If its script is already in the train split the English → stone item is answered for the agent, and if its English is already there the other direction is; either way the item scores for free and measures nothing. Test 4 scored two such items before this was caught, and discounting them moved the run from just over the bar to just under it. `scripts/validate.py` now fails on any held line whose `st` or `en` is verbatim in train, so the held set is valid by construction.

The bar that counts as done: **stone → English 100% meaning-correct, English → stone ≥90% exact**, with every miss read by hand and judged grammatical. A miss that is ungrammatical or changes meaning fails the run.

Score exact match first, then read the near-misses. A miss caused by a word or construction that has no train sentence is a corpus gap, not a model failure; fix the corpus and say so in the result file. A miss caused by the corpus contradicting itself, or by a point the spec never decided, is neither — log it as a grammar gap and say so.

Record each run in `results/` as `YYYY-MM-DD.md` with the corpus and lexicon size, both scores, the rules the agent inferred, what it got wrong, and a verdict.

## Coverage test (D121) — what the acceptance test cannot measure
The acceptance test scores sentences drawn from the corpus, and every corpus sentence was written by someone with the lexicon open. A thing the language cannot say was never written down, so it is never scored. That test measures whether the corpus teaches the language; it cannot report a gap.

This one inverts the deprivation. The acceptance test starves the **translator**; the coverage test starves the **source** and gives the translator everything, per the translation protocol below.

1. **Blind source.** One cold agent, given a one-paragraph domain description and nothing else — no lexicon, no grammar, no spec, no corpus, and no hint of what the language can do — writes the English sentences. Keep them verbatim in `fixtures/coverage_YYYY-MM-DD.txt`.
2. **Two full-materials translators**, independently, each with `spec/grammar.md`, the complete lexicon as form/pos/gloss/notes, and a sample of train pairs. Paraphrase and compounding encouraged; **stretching a root past its gloss is defined as a block, not a paraphrase**; inventing a form forbidden.
3. **Verdicts:** OK / CLUMSY (said, but lossy — record what is lost) / BLOCKED_WORD (list the words) / BLOCKED_GRAMMAR (describe the construction).
4. **Parse everything produced.** An OK verdict on a string `stonelib.parse_sentence` rejects is not a coverage result.

Two translators and not one, because tolerance for paraphrase *is* the measurement and one agent's tolerance is unfalsifiable. Report their agreement on sayable-against-blocked as the interval; a disagreement that is OK against BLOCKED is a different problem from one on the CLUMSY/BLOCKED line.

**No bar, and none should be set.** It reports where the language ends, not whether it passes. Record as `results/YYYY-MM-DD-<letter>.md` with the band breakdown, the words both arms named, and which blocks are gaps against which are scope boundaries under D1 and D34 — they are not the same finding.

**Re-running it requires a fresh blind draw.** Reusing a source set after coining against it measures the coining, not the language.

## Dictionary probe (D122) — how the language solves ordinary words
The coverage test uses sentences someone wrote to a domain description, so whoever wrote the description shaped the result. A frequency list has no opinion about what the language ought to cover. It also asks the better question: not *is this word missing* but **how is it solved**.

Word list: OpenSubtitles English via hermitdave/FrequencyWords — the same source and license as `data/ko_frequency.json`, and conversational rather than web register. Filter with an **explicit, literal** stop list of function words the grammar handles by construction, and lemmatize mechanically so the probe counts concepts and not English morphology; a language with no inflection must not be charged a miss for `went` and another for `gone`. Give the agents an INFLECTION verdict so what the lemmatizer misses is visible rather than swallowed.

Two independent arms per band, each with `spec/grammar.md`, the complete lexicon, **`lexicon/README.md`** and `corpus/README.md`. The lexicon README is not optional — its "Not coined on purpose" list is what separates a real gap from a concept the constructions cover, and an agent without it calls *always* and *nobody* gaps.

Verdicts: ROOT / DERIVED / CONSTRUCTION / COMPOUND / GAP / INFLECTION, and every GAP takes a scope call against D1 and D34. **Make COMPOUND strict in the prompt** — name an example that is not one (*small machine* is not screwdriver), or the verdict inflates. Without the scope call the number is meaningless: a subtitle corpus is film dialogue and most of what it reports missing was never claimed.

Report the curve by frequency band, not one total. Coverage falling 67% to 27% across 800 words is the finding; the mean of those is not.

**Nothing from this touches the corpus.** The dictionary decides what gets looked at, never what gets added — corpus lines are written deliberately, per D11, for words that were coined by decision. Re-run after any coining round; the list is fixed and the point is that the number moves.

## Drift test (D15, protocol fixed in D74)
`scripts/drift_test.py` is the executable form of this protocol; the prose here and the script must say the same thing.

Twelve **fixed** probe sentences — the list in the script, spanning all four evidentials, all six stances, negation, past and future, the conditional, all four modals and both quantifiers — are translated at the start of one long model conversation. Forty turns of other, plausible work follow in the same session. Then the same twelve are asked for again, in a different order and without being called repeats. The materials are the full set, per the translation protocol below, not the acceptance-test subset: this measures use, not learning.

Three signals, because the first one alone cannot be read:

1. **Probe divergence.** Early round against late round, token for token. Confounded: at the late round the model can see its own early answers and may simply copy them, so zero divergence here is necessary but not sufficient.
2. **Filler accuracy, early half against late half.** Every filler turn asks for a train sentence the corpus already answers, so each turn is scored. Copying cannot flatter this.
   **This needs the control arm** (`--control`): the same forty sentences, same order, each in its own fresh one-turn conversation. The filler sentences are drawn in corpus order and the newer corpus is harder, so a late-half drop in the long run means nothing until the control shows whether the same drop happens without a long session. Run both; the long run against the control is the measurement.
3. **Korean leakage.** Every token the model emits anywhere in the session, checked against `data/ko_frequency.json`. A token that is a real Korean word and that the parser cannot read as a word of this language is the specific failure D52 left open. A legal inflected form may coincide with a Korean word by accident, so the parser filter is part of the check, not an optimisation.

Record as `results/YYYY-MM-DD-drift.md`. Changing the probe list makes a new test, not a new run of this one.

## Regression test of the checks (D101) — not a test of the language
`scripts/regression_test.py`. The acceptance test measures the language; this measures the checks that are supposed to keep the acceptance test from being spent as a linter.

`tests/fixtures/pre_correction.jsonl` holds the pre-correction form of every corpus line corrected since 855226d, recovered from git, each recorded with the checks that fire when it is put back into the current corpus. The script puts each one back, one at a time, and fails if a check that fired then does not fire now. Run it beside `validate.py`. D102 and D103 are what it is for: the fronting check was widened there from two shapes to three and then from one clause to every clause, and the object-order check was added, so the fixture is where the 28 fronting forms and the 17 object-order forms now live and neither widening can quietly come undone.

D82 says a check never shown to catch a real violation is not evidence of anything. D87 and D94 both answered that in prose, once, and prose does not re-run — the demonstrations could not be repeated and nothing failed if an edit weakened a check. This is that answer made executable.

The fixtures with an empty `catches` list are the more useful half: **11 of the 62 corrections are invisible to every check**, including both lines of the D95 choose carve and both of the D90 say/message carve. They are asserted to stay invisible, so a widened check fails here and has to be recorded rather than passing unnoticed.

## Mutation test of a check (D104) — not a test of the language
`regression_test.py` proves a check catches the defects that were once in the corpus. It says nothing about defects nobody happened to write. Mutation testing covers that: take the held sentences that exercise a rule, mutate each into a violation of it, and require the check to fire.

Do it whenever a check is added or widened, and record the score. At D104 the object-order check caught 6 of 8 and the subject check 16 of 16 — the latter only after the mutation test found that a fronted with-phrase was invisible to it.

Read the non-catches before calling them failures. Two of the object check's are correct: sliding the comitative in s0022 across the object produces `아 에 하 우 파 와타카`, which is train line s0515 "We tested it" — not a violation but a different sentence, because position relative to the object is the only thing separating the comitative from the coordination. And a mutation that produces an ill-formed string is not a missed violation; two of those exposed a real gap anyway, since the parser was calling them well formed (D104).

## Translation protocol (D72) — not a test
For actually using the language, unlike the acceptance test, give the model everything: `spec/grammar.md`, `lexicon/lexicon.json` and the corpus. Withholding them is a property of the test, not of normal use.

`scripts/translate.py` is the tool. Its `gloss`, `check`, `lookup` and `examples` commands are deterministic and need no key. Its `to-english`, `to-stone` and `roundtrip` commands call a model and need `OPENROUTER_API_KEY`. Anything the tool emits in the script is parsed before you see it, so ill-formed output is retried rather than shown.

What the guardrail does **not** catch is worth knowing before trusting it: it checks the verb template and the script, not argument roles or the modal construction, so a wrong case marker or a modal that has lost its subordinator comes back well formed. `check` prints an advisory for the modal case (D76); the rest is on the reader.
