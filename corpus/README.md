# Corpus — the Rosetta Stone

The primary artifact (D2). Parallel sentences, English ↔ stone.

`corpus.jsonl`: one object per line:
`{"id": "s0001", "en": "...", "st": "...", "features": ["past", "neg"], "split": "train|held"}`

- `st` is script only.
- `features` tags which grammatical constructions the sentence demonstrates, for coverage checking (D11).
- `split`: `held` sentences are never shown in the acceptance test context (D3). Target ~10% held.

Coverage targets: every lexicon word in ≥3 `train` sentences; every feature in ≥10.
