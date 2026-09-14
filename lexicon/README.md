# Lexicon

`lexicon.json` is scaffolding for corpus construction, not the deliverable.

Entry schema: see `schema.json`. `form` is written in script only.
Never edit `lexicon.json` directly — use `scripts/validate.py --add`.

## Semantic carving (D35)
Roots are coined against the carving, not against English headwords. Split: knowing (by test / by definition / by belief); error (mistake / fault / run-time failure); asking (for information / for action / to check an assumption); change (fix / alter / build). Lumped: experiment, test, try = one root. `sense_notes` on every entry must say which side of a carve the root sits on.
