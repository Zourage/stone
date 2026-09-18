# Lexicon

`lexicon.json` is scaffolding for corpus construction, not the deliverable.

Entry schema: see `schema.json`. `form` is written in script only.
Never edit `lexicon.json` directly — use `scripts/validate.py --add`.

## Semantic carving (D35)
Roots are coined against the carving, not against English headwords. Split: knowing (by test / by definition / by belief); error (mistake / fault / run-time failure); asking (for information / for action / to check an assumption); change (fix / alter / build). Lumped: experiment, test, try = one root. `sense_notes` on every entry must say which side of a carve the root sits on.

## Carving beyond D35
Every entry's `sense_notes` states its own carve; the file is the authority, not this list. The major later ones: capacity (the able root) against warning (the risk stance); wanting against the intend stance, which is commitment; should against both; reason as offered grounds against cause as what acts; message as machine output against the act of telling; condition as a branch in code against a person choosing; take against receive by who initiates; early and late, often and rare, more and less as pairs of roots rather than one plus negation, because not-more is weaker than less. Major lumpings: experiment/test/try; number/count; say/tell; repeat/loop/again; person-ability and thing-capacity; and the one interrogative root that does every English question word.

Added in D124: **typical against right/correct** — correct is matching what a thing should be, typical is matching what it usually is, and science talk needs both separately; **similar against same**, which negation cannot reach, since not-same is different, the opposite rather than the middle; **sudden against fast** — fast is how quickly a thing proceeds, sudden is how little warning its onset gave; **lose against failure and remove** — a run-time failure is not a loss and removing is deliberate; **tired against effort**, which is work as a quantity: effort is what was spent, tired is what the spender now is; **free against open and empty**, a door and a container against an unclaimed stretch of time; **meet against join and discuss**, things joining and the activity once met; **eat against drink**, by what is consumed. Lumped, or rather not coined at all: **food**, because a root is neither noun nor verb (D29) and the eat root in argument position already is it; **anomalous**, which is typical negated, unlike not-often against rare where the negation leaves room for a third case (D62); and **the telephone**, because the act of calling is the say/tell root and the device is the physical-object class D34 never claimed.

## Families
A family shares its first syllable and is told apart by the second: the time units on one (hour, minute, week, month, year), the four modals on another (D61), and the six colours on the look syllable, because a colour is a seen quality (D123).

## Not coined on purpose
Constructions cover these, so no root exists and none should be added: always and never (the every and none determiners before the time root), always-check `spec/grammar.md` before coining anything that looks grammatical. Also soon, already, still, first, last, duration, deadline, fast-as-little-time, both, together, nothing, nobody, everything, everyone, and the ordinals. And, since D123: **fractions** (numeral + possessor + the part root), **weekdays** (the week-day compound plus an ordinal, Monday being day one) and **parts of day** (early-day is morning, late-day afternoon). Those three cover twelve concepts between them and cost no roots at all, which is the pattern to reach for first — the dictionary probe found this language solves by construction and almost never by compound (D122).
