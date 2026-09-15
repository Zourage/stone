# Corpus — the Rosetta Stone

The primary artifact (D2). Parallel sentences, English ↔ stone.

`corpus.jsonl`: one object per line:
`{"id": "s0001", "en": "...", "st": "...", "features": ["past", "neg"], "split": "train|held"}`

- `st` is script only.
- `features` tags which grammatical constructions the sentence demonstrates, for coverage checking (D11).
- `split`: `held` sentences are never shown in the acceptance test context (D3). Target ~10% held.

Coverage targets: every lexicon word in ≥3 `train` sentences; every feature in ≥10.

## Writing conventions (D43)
- Affixes are written solid with their root: one predicate is one token, root then negation, tense, evidential, stance, subordinator.
- Function words (case markers, pronouns, relational words, question particle) are separate tokens, after the word they belong to.
- Questions: the evidential slot is empty; the sentence ends in the question particle.
- The English side carries what the stone side marks: evidential and stance show up as natural English cues, never as bracketed labels. A sentence whose English has no cue is direct.

**Every stance must carry its cue in the English** (D84). The imperative counts as the intend cue, so a command needs nothing extra; anything else carrying intend does. The rule exists because a stance the English does not signal makes the sentence undetermined in the English → stone direction, which is what the acceptance test measures. Predict is the one that slips most easily, because English renders both a plain future and a prediction as "will".

**One English sentence must have exactly one rendering in the script** (D83). Where two corpus lines share an English string and differ in the script, one of them is wrong; fix the English or the script so the pair is distinguishable.

**An alternative question coordinates the smallest constituent that differs** (D89). The shared material is stated once: the two alternatives flank the or word and nothing else is repeated. This holds whether the alternation is on the subject, the predicate or a complement.

**Every evidential must carry its English cue** (D79, generalised in D91). A sentence whose English carries no cue is direct; any other evidential needs its cue, or the sentence is undetermined in the English → stone direction. This was the rule all along but the corpus broke it in ten places, which is three of the twenty misses in acceptance test 3 and the only three that changed meaning. For the general evidential it applies to gnomic statements, the ones asserting how things are. It does not apply where the construction supplies the slot instead of the English: the general evidential under the irrealis rule — a condition, or a modal complement — and the inferred evidential under the predict stance, which D88 pins to it. Those two exemptions and the imperative are the whole list; **every other marked slot carries its own cue**, and `scripts/validate.py` checks each one separately. Until D105 it accepted a line where any one marked slot had a cue, which hid s0010. Fixed cues, and `scripts/validate.py` fails on a marked slot whose English carries none of its own (D94): reported "i'm told / i am told / they say / you told me / i was told"; inferred "must / i gather / it seems / seems / i think"; general "how it is / everyone knows / as such / known / by definition / from the definition"; intend "i'll / we'll / i will / we will / that's the plan / that's my intention / going to"; predict "i expect / probably / expect"; propose "just a proposal / just a hypothesis / i suspect / perhaps"; trust "counting on / you can count"; risk "might go wrong / might break / that might"; assert "i insist".
## Feature tags

Taken from the corpus itself. `scripts/validate.py` fails if this list or the total below stops matching the data, and if the cue sentence above stops matching `SLOT_CUES` in that file — D73 and D94 both claimed these could not drift because they were generated, and both drifted, because nothing checked them (D101).

- **evidential**: direct, reported, inferred, general
- **stance**: intend, predict, propose, trust, risk, assert
- **verb ending**: past, future, neg, sub
- **clause type**: question, imperative, conditional, if, equative, agentless, clause-subject, clause-anaphora
- **argument marking**: obj, loc, poss, with, for, from, det, compound, nominal-root, region
- **quantity**: numeral, quantifier, all, none, both, ordinal, n-times, how-often, comparison
- **question words**: q-what, q-which, q-where, q-why, q-how, q-when, q-who
- **other constructions**: modal, able, want, should, allow, manner, because, therefore, become, between, still, not-yet, until, since, while, deadline, ownership, reciprocal, we, we-exclusive, or, but, stative, hold-exist, know, ask
- **corpus bookkeeping**: minimal-evid, minimal-stance
- **domain and uncategorised**: after, before, domain-code, domain-discussion, domain-experiment, domain-physical, domain-time, domain-work, here, now, then, there

Total: 88 distinct tags over 1295 sentences.
