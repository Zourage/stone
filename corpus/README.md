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

**A general-evidential sentence must carry a general cue in its English** (D79). This was the rule all along but the corpus broke it in ten places, which is three of the twenty misses in acceptance test 3 and the only three that changed meaning. It applies to gnomic statements, the ones asserting how things are. It does not apply where the general evidential follows from the irrealis rule — a condition, or a modal complement — because there the construction supplies it and no cue is needed or wanted. Fixed cues: reported "I'm told / they say"; inferred "must / I gather / it seems"; general "that's just how it is / everyone knows that / as such"; intend "I'll / that's the plan" or an imperative; predict "I expect / probably"; propose "just a proposal / just a hypothesis"; trust "I'm counting on it / you can count on that"; risk "that might go wrong / might break something"; assert "I insist".
## Feature tags

Generated from the corpus itself, so this list cannot drift from the data. Regenerate it whenever tags are added.

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

Total: 88 distinct tags over 865 sentences.
