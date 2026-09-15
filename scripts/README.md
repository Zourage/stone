# scripts

| script | needs a key | what it does |
|---|---|---|
| `validate.py` | no | The gate. Checks the lexicon and corpus; run before every commit. `--add FILE` is the only way words enter the lexicon (CLAUDE.md rules 4 and 6). Also errors on an adverbial standing before the main-clause subject (D78, D102) or before the object (D103), on a held sentence copied from train (D93), on the decided rules the corpus has broken before — the two D88 pairings and the cue rule (D94) — and on `corpus/README.md` drifting from the cue list in the code or the tags in the corpus (D101); reports gloss collisions. |
| `regression_test.py` | no | Re-runs every check in `validate.py` against the pre-correction form of all 62 corrected corpus lines (`tests/fixtures/pre_correction.jsonl`), and fails if a check that used to fire on one no longer does. It also pins the 11 corrections no check can see, so widening a check shows up as a failure to update rather than as silence (D101). |
| `stonelib.py` | no | Shared parsing: lexicon access, tokenising, glossing. `validate.py` and `translate.py` both use it so the rules live in one place — including the D104 rule that a marker follows the word it marks, so the translation guardrail rejects a stranded or doubled marker instead of calling it well formed. |
| `translate.py` | partly | The translation tool. `gloss`, `check`, `lookup`, `examples` are deterministic; `to-english`, `to-stone`, `roundtrip` call a model. |
| `realize.py` | no | Deterministic stone → English (D106): parse, then generate, with no model. 13.5% exact against the gold English and 16 of 30 meaning-correct by hand, so it is a v1 — but `--ambiguous` is the point of it, listing the 64 sentences where `[root][root][marker]` is structurally undecidable and it had to break the tie. `--score` runs it over the whole corpus. |
| `drift_test.py` | yes | The drift test (D15), both arms: the long session and the `--control` fresh-session baseline. A run without the control is not interpretable (D74). |
| `correct_corpus.py` | no | Corrects existing corpus lines (O8). Corrections go in a JSON file, each with a `why`; every corrected line is re-parsed and nothing is written unless all are well formed. Dry run by default, `--apply` writes. |
| `merge_batch.py` | no | Dry-runs a proposed batch of roots and sentences through the validator without writing, then `--apply` writes it (D58). |
| `compose_hangul.py` | no | Computes the 74 codepoints from the phonology (D52). Run once; rerunning is a decision. |
| `measure_codepoints.py` | yes | Historic. Measured token cost and visibility of codepoint blocks; produced the evidence for D20–D22. Kept as the measuring tool. |

`OPENROUTER_API_KEY` is the only secret any of these read. None of them writes it anywhere.
