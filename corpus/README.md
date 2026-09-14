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
- The English side carries what the stone side marks: evidential and stance show up as natural English cues, never as bracketed labels. A sentence whose English has no cue is direct. Fixed cues: reported "I'm told / they say"; inferred "must / I gather / it seems"; general "that's just how it is / everyone knows that / as such"; intend "I'll / that's the plan" or an imperative; predict "I expect / probably"; propose "just a proposal / just a hypothesis"; trust "I'm counting on it / you can count on that"; risk "that might go wrong / might break something"; assert "I insist".
- `features` tags: evidentials and stances by name, past, future, neg, question, q-what/q-which/q-where/q-why/q-how/q-when/q-who, imperative, det, sub, obj, loc, poss, with, for, from, nominal-root (a root used as an argument), stative, numeral, before, after, here, there, now, then, know, ask, minimal-evid, minimal-stance, hold-exist.
