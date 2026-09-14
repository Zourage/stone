# Tests

## Acceptance test (D3)
Protocol: a fresh session, context = corpus train split only. No spec, no lexicon.
Ask it to translate every `held` sentence both directions. Score exact match, then read near-misses by hand.
Record in `results/` with date and pass rate. The pass rate that counts as done is recorded in decisions.md.

## Drift test (D15)
A fixed sentence set translated at turn 1 and again at turn 40 of a long session. Any divergence is a bug.
