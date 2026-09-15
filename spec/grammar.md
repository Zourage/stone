# Grammar

Status: O2 closed (D26, D29–D33); grammatical pieces coined (D39, see `lexicon/lexicon.json` w0001–w0025). Open: number, derivation suffixes. Scaffolding for corpus construction; the corpus is authoritative.

## Word order (D33, D78, D87, D97, D98, D99)
Subject, object, verb. Subject bare; object case-marked.

**The subject comes first, always.** An adverbial — a time or place phrase, a while-clause, an until- or since-clause, a because-clause — follows the subject. Fronting an adverbial before the subject is not allowed, even though it reads naturally in English. The rule exists because free order made English → stone undetermined and cost six misses in acceptance test 3; the corpus taught both orders and contradicted itself. Exception, and it only looks like one: a pronoun inside an embedded clause may precede the main subject, because it is that clause's subject, not the main one. The rule covers the n-times phrase (a count word plus the repeat root) as well, which D78 left untouched: it follows the subject like any other adverbial. An agentless clause has no subject, so its adverbial stands first with nothing displaced. `scripts/validate.py` counts violations of this on every run and the count is 0, but read that count for what it covers: the detector knows the two shapes D78 and D87 corrected — a subordinate clause closed by the from word or by time plus before/after, and an n-times phrase — and nothing else. **A bare time or place phrase in the location case is invisible to it, and seven train sentences front one before the subject** (s0117, s0628, s0634, s0683, s0773, s0780, s0787), against an overwhelming majority that does not. The corpus contradicts itself on the same construction four times over: s0111 against s0117, s0156 against s0787, s0637 against s0634, s0038 against s0628. Logged as **G32**; the rule below is right, it is the enforcement and those seven lines that are not (D101).

**Below the subject, only two orders are settled.** An n-times phrase precedes the object: 9 train sentences, no counterexample (D97 added three to the 6 it counted). A with-phrase that is a genuine adverbial — comitative, instrument or manner — follows the object in 24 train sentences, and the with word coordinating two arguments into a subject precedes it in 15, because it is part of the subject (D98). **D98 counted 24–0 and 16–0; the true counts are 24–1 and 15, because one of the sixteen is not a coordination.** s0625 "How did you move it out?" puts the manner interrogative before the object, where the six other q-how sentences with an object put it after. One line against six is not a rule taught two ways, but it is a line the corpus will teach, so it is logged as **G33** rather than counted as zero (D101).

**Where a time or place phrase and a while-clause sit relative to the object is G31, open.** Do not read a rule into this section that is not here: the corpus puts a time or place adverbial after the object 22 times and before it 3 times, and splits 5 to 3 on the while-clause, and it contradicts itself on time adverbials of the same kind (s0639 before, s0114 after). Until D78's earlier claim that an adverbial "precedes the object" was removed in D99, this section asserted the minority pattern as the rule. G31 needs the D78 treatment — counts, a chosen rule, every violating line corrected, then a check shown to catch the pre-correction forms — and has not had it.
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

## Morphology (D29, D32, D33)
Verb template: root, negation, tense, evidential, stance, subordinator. Only the evidential is mandatory. Arguments: bare, or root plus one case marker.
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

## Region nominals (D70)
Inside, outside, up and down with the location case, or compounded before a root.

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
