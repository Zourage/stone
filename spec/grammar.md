# Grammar

Status: O2 closed (D26, D29–D33); grammatical pieces coined (D39, see `lexicon/lexicon.json` w0001–w0025). Open: number, derivation suffixes. Scaffolding for corpus construction; the corpus is authoritative.

## Word order (D33, D78, D87, D97, D98, D99, D102, D103) — closed
Subject, object, verb. Subject bare; object case-marked.

**The subject comes first, always.** An adverbial — a time or place phrase, a while-clause, an until- or since-clause, a because-clause, a before- or after-phrase — follows the subject. Fronting an adverbial before the subject is not allowed, even though it reads naturally in English, and the English side of the corpus often does front it: s0109's English is "After the test, it was good" and its script is `that.one test-after good-PAST-DIR`. The rule exists because free order made English → stone undetermined and cost six misses in acceptance test 3. Exception, and it only looks like one: a pronoun inside an embedded clause may precede the main subject, because it is that clause's subject, not the main one. The rule covers the n-times phrase as well. An agentless clause has no subject, so its adverbial stands first with nothing displaced. The corpus is 131 to 13 for it, and the 13 were corrected under D102 and D103; `scripts/validate.py` now **fails** on a violation rather than counting one, and the check knows three shapes, listed in its docstring — read that list before reading its 0. It said 0 through D87 and D101 while eleven lines were wrong, because it only asked about the two shapes D87 had corrected and because a question's predicate carries no affix for it to stop at; D103 found two more, in second clauses it was not walking (D78, D87, D102, D103).

**Below the subject: n-times, object, adverbials, verb.** An n-times phrase precedes the object — 9 train sentences, no counterexample — because it counts the event, and counting material precedes what it counts, as numerals precede the root they count (D48, D97). Its how-often variant, which puts the stretch in the location case (D69), is part of that phrase and goes with it. **Every other adverbial follows the object and stands immediately before the predicate**: a time or place phrase, a while-clause, an until- or since-clause, a because-clause, a before- or after-phrase, a for-phrase of beneficiary, purpose or duration, a from-phrase of source or cause, and the with-phrase of comitative, instrument or manner. The corpus was 100 to 15 for this before D103 corrected the fifteen and two more, and every type is now unanimous: because 0–2, before/after 0–17, for 0–9, from 0–7, while 0–8, until/since 0–2, with 0–25, time or place 0–47 (D103).

The with word coordinating two arguments into a subject is not an adverbial and precedes the object, because it is part of the subject: 15 train sentences, all of the shape pronoun + pronoun + with (D98). A recipient takes the location case and follows the object like any other adverbial, which is what D57 already said.

`scripts/validate.py` **fails** on an adverbial before the object as it does on one before the subject, and both checks are re-proved against the pre-correction forms by `scripts/regression_test.py` on every run (D102, D103).

**Two adverbials in one clause run: with-phrase, then time/place/region/before-after, then the recipient** (D120). The recipient sits immediately before the verb because it is an argument of the verb rather than a circumstance — D57 already made it an argument. Thin evidence, and stated rather than discovered: the corpus had four such clauses and contradicted itself on the only comparable pair (s0685 time-then-recipient against s0456 recipient-then-time, same verb), which cost a miss in acceptance test 7. The rule fits three of the four; s0456 was corrected and eight sentences added. `scripts/validate.py` fails on a recipient standing before another adverbial.
## Word classes
Decided (D26): no adjective class, no adverb class. Property words are stative verbs; manner is a serial verb or a case-marked nominal.
Decided (D29): one open class of content roots. Predicate use takes an obligatory verb ending; argument use is bare, case-marked only when needed.
Decided (D30): four obligatory evidentials on the predicate: direct, reported, inferred, general. Evidential scopes over negation. Stance is a separate slot (D34).
Decided (D31): three-way tense, present unmarked, future strictly temporal (stance carries intention and prediction).
Decided (D32): negation is a piece of the verb ending. Ending order: root, negation, tense, evidential; only the evidential is mandatory.
Decided (D33): closed function-word class: 3 case markers (object, location, possessor), 1 question particle, pronouns, a few relational words. Subordinator is the last piece of the verb ending.

## Determiners (D44, D48)
A pronoun, the interrogative root or a numeral directly before a root restricts it: this test, which machine, three files. Case markers follow the phrase.

## Deixis (D48)
Here = this + location case; there = that + location; now = this + time; then = that + time. Before and after are relational words after their argument.

## Morphology (D29, D32, D33, D104)
Verb template: root, negation, tense, evidential, stance, subordinator. Only the evidential is mandatory. Arguments: bare, or root plus one case marker.

A marker follows the word it marks, so it can neither open a sentence nor follow another marker: the three case markers, the relational words and the question particle all attach leftwards, and or and but stand between the things they join (D59). The parser enforces this, which it did not before D104 — `check` called a sentence opening with a bare relational word well formed, and the translation guardrail would have shown such output as a translation.
## Tense (D31)
Past, present (unmarked), future. Future is temporal only. Aspect: none decided.
## Negation (D32)
Piece of the verb ending, before tense and evidential. Evidential scopes over it.
## Questions (D33, D45)
Sentence-final particle; the evidential slot is empty and the answer supplies it. One interrogative root (w0039) does all question words: bare = what; as determiner = which; + location case = where; + for = why; + with = how; before time = when; before person = who.
## Quantifiers (D62)
Every/all and no/none stand before the root, like numerals. With the thing and person roots they give everything, everyone, nothing, nobody. A negative determiner carries the negation alone: the predicate is not also negated.

## Number (D48, D62)
Bare arguments are number-neutral: no plural marking exists or is needed.

Numerals precede the root they count: three files. One to five and ten are simple; six to nine are five-plus-N; a numeral before ten multiplies, after it adds. Plural marking without a numeral: none, by D62.
## Coordination (D59)
No and: clauses are juxtaposed, arguments joined with the with word. Or and but stand between the things they join.

## Modals (D61, D63)
Four roots share a first syllable and one construction: complement clause with the general evidential and the subordinator, then the modal root as main predicate with its own evidential. Able (capacity, not the risk stance), want (not the intend stance), should (obligation), allow (permission). Each negates normally.

## Manner (D26, D68)
The quality plus the with word: fast-WITH do = do it fast. The how-question has the same shape.

## Because and therefore (D69)
Because: subordinate clause + the from word. Therefore: state the cause clause first and juxtapose.

## Become (D69)
Stative clause + the begin root: cold-GEN-SUB begin-PAST = got cold.

## Ordinals (D69)
A numeral before a root counts it (three steps); after it, identifies it (step three).

## Between, still, both, reciprocals, deadlines, rate (D69)
Between: the interval root over two points joined by with. Still: the continue root over a subordinate clause. Both: the numeral two alone. Reciprocal: a joint with-subject and no object. By a time: before on the time phrase. How often: how many times with the stretch in the location case.

## Clause as an argument (D66, D69)
A subordinate clause fills a subject slot as well as an object slot, so an equative with a clause puts the clause first. A pronoun may take a whole clause as antecedent.

## Until and since (D70)
Subordinate clause + the time root + before = until; + after = since.

## Region nominals (D70, D114)
Inside, outside, up and down with the location case. A region nominal **compounds directly with its landmark and takes no possessor**: `machine outside-LOC`, not `machine-POSS outside-LOC` (8 to 5 in the corpus; D70 already said "compounded"). With no landmark it stands alone: `above-LOC`.

## Locating a thing against saying it exists (D115)
Locating a definite thing takes the **place** root: `fault inside-LOC place-DIRECT` = the fault is inside. Saying something exists takes the **hold** root: `danger here-LOC hold-DIRECT` = there is a danger here. The corpus rendered these two ways until D115; the distinction is not marked in the script, so nothing checks it.

## Possession as a predicate (D69, D116)
The possessor takes the possessor case and comes first, with no leading pronoun: `I-POSS turn-DIRECT` = it is my turn, not `this I-POSS turn-DIRECT`.

## A shared subordinate subject (D117)
A subordinate clause states its own subject even when it is the same as the main clause's: `you you it-OBJ fix-GEN-SUB time LOC alone-NEG-DIRECT-INTEND`. Thin evidence (2 to 1) and unchecked, because an absent subject cannot be told from a legitimately agentless embedded clause.

## Comparison (D65)
The standard takes the from word; the quality is the predicate. This that-FROM big-DIRECT = this is bigger than that. No comparative form.

## Agentless clauses (D65)
No passive. Drop the subject and keep the object marker: line-OBJ remove-PAST-DIRECT = the line was removed.

## We (D64)
I + you + the with word (inclusive); the third party replaces you for the exclusive sense.

## Occurrences (D64)
A numeral before the repeat root: three repeats = three times.

## Compounds (D64)
A root directly before another root modifies it: time limit, failure message.

## Simultaneity (D64)
Subordinate clause with the general evidential, then the time root with the location case: at the time that it runs.

## Irrealis rule (D60, D61)
A clause that is not actual — a condition, an ability complement — carries the general evidential.

## Conditionals (D60)
The condition clause comes first, its predicate carrying the general evidential, followed by the `if` word. Then the main clause, with its own evidential and stance. No word for `then`.

## Recipients (D57)
Content is the object; the recipient takes the location case: result-OBJ me-LOC show. For = beneficiary or purpose only.

## Equatives (D56)
No copula. The second term is the predicate and takes the verb ending: result three-DIRECT = the result is three; this cause-DIRECT = this is the cause. Numerals and pronouns take verb endings in this use.

## Possession and existence (D33, D49)
Possessor case marker on the possessor, before the possessed. No verb have: 'I have a file' is my file + hold. No verb exist: 'there are three files' is three files + hold.
## Subordination (D33)
Subordinator piece on the embedded verb, after its evidential. Covers complement and relative clauses.
## Evidentiality (D30)
Four, obligatory on every predicate: direct, reported, inferred, general. Scopes over negation. Questions ask for the listener's source. Forms: w0001–w0004.
## Imperatives (D46)
Second-person subject with the intend stance. No imperative mood. Requests use the ask-for-action root instead.

## Stance (D34)
Optional, one per predicate, own slot after the evidential and before the subordinator: intend, predict, propose, trust, risk, assert. Forms: w0005–w0010.

## Derivation suffixes (D13)
Open. Decide when the first roots need them. With one open class (D29) the noun/verb pair is already free; suffixes are for further senses.
