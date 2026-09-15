# scripts

| script | needs a key | what it does |
|---|---|---|
| `validate.py` | no | The gate. Checks the lexicon and corpus; run before every commit. `--add FILE` is the only way words enter the lexicon (CLAUDE.md rules 4 and 6). Also errors on a held sentence copied from train (D93) and on the decided rules the corpus has broken before — the two D88 pairings and the cue rule (D94) — and reports fronted adverbials and gloss collisions. |
| `stonelib.py` | no | Shared parsing: lexicon access, tokenising, glossing. `validate.py` and `translate.py` both use it so the rules live in one place. |
| `translate.py` | partly | The translation tool. `gloss`, `check`, `lookup`, `examples` are deterministic; `to-english`, `to-stone`, `roundtrip` call a model. |
| `drift_test.py` | yes | The drift test (D15), both arms: the long session and the `--control` fresh-session baseline. A run without the control is not interpretable (D74). |
| `correct_corpus.py` | no | Corrects existing corpus lines (O8). Corrections go in a JSON file, each with a `why`; every corrected line is re-parsed and nothing is written unless all are well formed. Dry run by default, `--apply` writes. |
| `merge_batch.py` | no | Dry-runs a proposed batch of roots and sentences through the validator without writing, then `--apply` writes it (D58). |
| `compose_hangul.py` | no | Computes the 74 codepoints from the phonology (D52). Run once; rerunning is a decision. |
| `measure_codepoints.py` | yes | Historic. Measured token cost and visibility of codepoint blocks; produced the evidence for D20–D22. Kept as the measuring tool. |

`OPENROUTER_API_KEY` is the only secret any of these read. None of them writes it anywhere.
