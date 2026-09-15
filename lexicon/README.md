# Lexicon

`lexicon.json` is scaffolding for corpus construction, not the deliverable.

Entry schema: see `schema.json`. `form` is written in script only.
Never edit `lexicon.json` directly — use `scripts/validate.py --add`.

## Semantic carving (D35)
Roots are coined against the carving, not against English headwords. Split: knowing (by test / by definition / by belief); error (mistake / fault / run-time failure); asking (for information / for action / to check an assumption); change (fix / alter / build). Lumped: experiment, test, try = one root. `sense_notes` on every entry must say which side of a carve the root sits on.

## Carving beyond D35
Every entry's `sense_notes` states its own carve; the file is the authority, not this list. The major later ones: capacity (the able root) against warning (the risk stance); wanting against the intend stance, which is commitment; should against both; reason as offered grounds against cause as what acts; message as machine output against the act of telling; condition as a branch in code against a person choosing; take against receive by who initiates; early and late, often and rare, more and less as pairs of roots rather than one plus negation, because not-more is weaker than less. Major lumpings: experiment/test/try; number/count; say/tell; repeat/loop/again; person-ability and thing-capacity; and the one interrogative root that does every English question word.

## Not coined on purpose
Constructions cover these, so no root exists and none should be added: always and never (the every and none determiners before the time root), always-check `spec/grammar.md` before coining anything that looks grammatical. Also soon, already, still, first, last, duration, deadline, fast-as-little-time, both, together, nothing, nobody, everything, everyone, and the ordinals.
