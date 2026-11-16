# Draft language spec (version 0.2) — for the encoding test

A constructed language meant to be written by a language model and decoded to English by a script.
No real word forms exist yet. You write it in **gloss notation**:

- CAPITALS = a grammatical particle from the closed lists below. You may use ONLY the particles listed here.
- lowercase English word = a native content root. Assume any ordinary, general-vocabulary content word
  exists as a root (run, big, test, sorrow, grape, wife, before, south, inside...). A root has no
  noun/verb/adjective class: position decides its use. Do not treat function-like English words as roots
  to smuggle grammar in (no roots for: the, a, very, only, although, would, must, still, already, just,
  even, than, of, and...).
- Single capital letters (A, B, S, T...) = handles (short names bound to a thing).
- « » = verbatim foreign text or notation (code, formulas, units, numbers with units). Whitespace and
  line breaks inside « » are kept exactly.
- Proper names: name«Darwin». A native root made into a proper name: name death.
- Technical terms: build with roots and linkers (store KIND data = database) or define with DEFINE.

## Grammar

```
text      = { sentence }
sentence  = [BY speaker] [label ":"] header body "."
header    = opener {relation [labels]} [strength] {attitude} [CALL phrase]
block     = "{" [BY speaker] [header] body "}"
body      = clause {(AND | OR) clause}
          | IF block block [block]
          | EACH handle IN phrase block
          | phrase                      (bare phrase: only after SOCIAL, HEAD, or as a fragment answer)
clause    = [NOT] [time] {aspect} [modal [NOT]] [focus] [degree] predicate {role phrase}
predicate = root | "(" phrase ")"
phrase    = unit {(AND | OR) unit}
unit      = [focus] [NOT] {quantifier} head {linker modifier} [NAMED handle]
modifier  = [NOT] [degree] (root | handle | loan | number | block | "(" phrase ")")
head      = root | handle | loan | «notation» | number | block | "(" phrase ")"
          | WHAT | SELF | MUTUAL | ME | YOU | US | STEP label [UPTO label]
number    = [AROUND | EXACT | ATLEAST | ATMOST] digits [UPTO digits]
```

Order of the role phrases after the predicate is FREE and carries no meaning.
AND and OR may join any number of like units. Mixing AND with OR at one level needs ( ) or { }.
A focus particle, NOT, or a quantifier written before a parenthesised group applies to the whole group.

## Header

**Openers** (exactly one per sentence; optional at the start of a block):

| Opener | Meaning |
|---|---|
| GIVEN | It is in the context: a document, tool or other party shows it, or the writer observes it directly |
| DERIVED | Follows from earlier sentences; followed by the labels it rests on (may also list RECALLED) |
| RECALLED | From the writer's background knowledge |
| ASSUMED | Supposed for argument, not claimed |
| CLAIM | The writer asserts it and gives no source |
| STORY | Narrated as part of a story or scenario; not asserted as fact |
| ASK | A question. A strength particle after ASK gives the answer the asker expects |
| REQUEST | Asks or instructs someone to act (a procedure step is a REQUEST with no addressee) |
| PLAN | Commits the writer to act. PLAN IF { want AGENT YOU } ... is an offer |
| DEFINE | DEFINE term [AND/OR term] BE phrase-or-block |
| SOCIAL | A social act done by saying it; takes a bare phrase: SOCIAL thank . SOCIAL greet . SOCIAL agree . |
| HEAD | A title or heading; takes a bare phrase |

A block with no header is a bare proposition (mentioned, not asserted). A block WITH a header carries its
own force: `know AGENT A THEME { ASK take AGENT WHAT THEME house }` = A knows who took the house.
WHAT is a question word only under the nearest enclosing ASK.

**BY** marks whose words a sentence or block is. `BY A 3: ASK ...` = speaker A asks. Inside a BY block or
sentence, ME is that speaker, YOU is their addressee, and openers, strength and attitude are theirs.
Use it for dialogue turns, direct and reported speech, citations and editor's notes:
`STORY PAST say AGENT H THEME { BY H PLAN beat AGENT ME THEME YOU }`.

**Relations** (any number, each optionally followed by target labels; default target = previous sentence;
a target may be a later label):

| Relation | This sentence... |
|---|---|
| CONTRAST | differs from, or opposes, the target |
| CONCEDE | holds even though the target holds (the target is the conceded point) |
| RESULT | is a consequence of the target |
| EVIDENCE | is the writer's ground for believing the target |
| ADD | adds a further point alongside the target |
| SEQUENCE | is the next event after the target |
| EXAMPLE | is an instance of the target |
| RESTATE | says the target again in other words, or sums it up |
| BACKGROUND | sets the scene for the target |
| ASIDE | is off the main line |
| UNDER | holds only inside the supposition or condition made in the target |
| ANSWER | answers the question in the target |
| EXPLAIN | says why the target is so |
| DETAIL | spells out part of the target |

**Strength**: CERTAIN, LIKELY, POSSIBLE. A number may follow: LIKELY «0.3-0.6». Strength may also stand in
the focus slot before one phrase to scope doubt to that phrase.

**Attitude** (any number): SURPRISE, EMPHASIS, POLITE, REGRET, GLAD, ANNOYED, JEST (said playfully),
IRONY (the writer means other than the literal words).

**CALL** phrase names the person addressed: `ASK POLITE CALL name«Bennet» DONE hear AGENT YOU ...`.

## Inside the clause

- **NOT** negates what follows it in its unit: before the clause, before a modal's complement
  (MUST NOT go = forbidden; NOT MUST go = not required), before a phrase, or before a modifier.
- **Time**: PAST, FUTURE, NOW (at present, may change), UNREAL (holds in a supposed world, not the actual
  one: "would", "were"); unmarked = timeless. `IF { UNREAL exist NOT ... } { UNREAL STILL true ... }`. NEAR or FAR may follow PAST or
  FUTURE (PAST NEAR = just now). Time inside a block is counted from the time of the enclosing clause
  (a PAST block under a PAST clause = "had done").
- **Aspect** (any number): ONGOING, DONE (finished, result holds), HABIT, BEGIN, STOP, STILL (continues,
  against expectation of ending), AGAIN, ALREADY (NOT ALREADY = not yet), FINALLY (after a long wait),
  OFTEN, RARE, ALWAYS, NEVER.
- **Modal**: MUST (required), SHOULD (advised), MAY (permitted), CAN (able, or possible in fact).
  These are about the world. How sure the writer is belongs to strength.
- **Degree**, before a predicate or a modifier: VERY, SLIGHT (somewhat), FULL (completely), BARELY (hardly),
  ALMOST, ENOUGH, TOO, MORE, LESS, MOST, LEAST, EQUAL. MORE/LESS/EQUAL take a THAN phrase when the standard
  is stated and stand alone when it is not. ENOUGH and TOO take a FOR phrase. WHAT may stand in the degree
  slot (how much).
- **Focus**, before a phrase or before the predicate: ONLY, ALSO, EVEN, INSTEAD, MAINLY (mostly, especially),
  FOCUS (contrastive stress: this one, not another), TOPIC (what the sentence is about).
- A predicate may be a whole phrase in ( ): `GIVEN (exception KIND NOT handled) THEME E` = E is an unhandled exception.
- There is no "is": `GIVEN big THEME file .` = the file is big.

**Roles** (particle before its phrase):

| Role | Marks | Role | Marks |
|---|---|---|---|
| AGENT | who acts | CAUSE | cause or reason |
| THEME | what is acted on or described | FOR | purpose or beneficiary |
| TO | recipient or end point | THAN | standard of comparison or likeness |
| FROM | origin | ABOUT | topic, field or respect |
| AT | place | AS | capacity, role or viewpoint |
| WHEN | point in time | ALONG | companion |
| WITH | means or manner | SPAN | duration, extent, or size of a difference |
| EXCEPT | what the claim does not cover | DESPITE | what would have been expected to prevent it (a phrase or a block: "although", "even if") |
| VIA | path, or thing passed through | | |

A role may appear once per clause; join several fillers with AND / OR.

## Inside a phrase

- **Linkers** after the head:
  - KIND narrows the head (error KIND network).
  - OF marks owner or whole (file OF user).
  - REL gives the landmark of a relational root: south REL city (south of the city), before REL meeting,
    between REL (A AND B), inside REL box, friend REL name«Ana». Time and place relations are built this
    way: `WHEN before REL { arrive AGENT A }`, `AT south REL S`, `WHEN until REL day KIND five`.
  - NOTE adds a comment that does not narrow: flower NOTE { OFTEN bad THEME SELF }. With a phrase it
    means "namely": 2 kind NOTE (A AND B); substance NOTE (glucose AND starch).
- All modifiers attach to the head. A modifier needing its own modifier goes in ( ).
- A clause can modify; SELF marks the head's place: test KIND { fail THEME SELF }. When clauses nest, bind
  the head with NAMED and use the handle instead of SELF.
- MUTUAL in a role means "each other": see AGENT (A AND B) THEME MUTUAL.
- **Quantifiers** before the head: ALL, MAJOR (most of), MANY, SEVERAL (more than one), SOME, FEW, NONE,
  ANY (whichever; no existence implied), GENERIC (the kind in general, exceptions allowed),
  THAT (the one already identified), THIS (the one present or pointed at), OTHER (a different one from the
  one mentioned), a number, ORD n (the nth), WHAT (how many / which). ALL 2 = both. Two may combine: THAT OTHER side.
  When one clause would hold two quantifiers that depend on each other, use EACH: 
  `EACH X IN ALL value { ... SOME ... }` (for each value there is some ...).
- NAMED binds a handle. After a quantified phrase it binds a variable for the rest of the sentence.
- ME, YOU, US (the writer's group; write ME AND YOU when the addressee is included). ANY person = "one".
- Numbers: AROUND 20, ATLEAST 12, ATMOST 5, 30 UPTO 60.

## Logic (same clause, numbered slots)

```
expression = value | "(" function {slot expression} ")"
statement  = DEFINE name {slot handle} BE (expression | block) | IF block block [block]
           | EACH handle IN expression block | WHILE block block | RETURN expression | expression
```
Slots: FIRST, SECOND, THIRD, FOURTH. Values: handles, digits, « », YES, NO, EMPTY, field OF expression.

## Examples

```
1: GIVEN fail THEME test KIND login .
2: GIVEN PAST change AGENT YOU THEME setting NAMED S .
3: RECALLED HABIT read AGENT ALL test KIND login THEME S .
4: DERIVED 1 2 3 LIKELY cause AGENT STEP 2 THEME STEP 1 .
5: ASK PAST change AGENT YOU THEME ONLY S .
6: GIVEN CONTRAST 2 NOT PAST change AGENT name«Ana» THEME S .
7: PLAN undo AGENT ME THEME S .
```
Decoded: 1 The login test fails. 2 You changed the setting (call it S). 3 All login tests read S.
4 (From 1,2,3; likely) Step 2 causes step 1. 5 Did you change only S? 6 By contrast, Ana did not change S. 7 I will undo S.

More:
- `CLAIM MUST NOT enter AGENT ANY person WHEN before REL 9 .` = No one may enter before nine.
- `GIVEN STILL SLIGHT high THEME price .` = The price remains somewhat high.
- `REQUEST bake THEME ham SPAN AROUND 4 hour AT oven KIND (SLIGHT hot) .` = Bake the ham for about four hours in a moderately hot oven.
- `BY A 1: ASK DONE send THEME release .` / `BY B 2: GIVEN ANSWER 1 NO .` / `BY A 3: SOCIAL ANNOYED ok .`
- `ASSUMED 1: finite THEME ALL prime .` then `DERIVED UNDER 1 2: ...` for each step inside the supposition,
  then `DERIVED 1 5 NOT finite THEME ALL prime .` outside it.
- Fragment answer: `ASK fail THEME test KIND WHAT .` / `GIVEN THEME test KIND login .`
