# Draft language spec (version 0.1) — for the encoding test

A constructed language meant to be written by a language model and decoded to English by a script.
No real word forms exist yet. You write it in **gloss notation**:

- CAPITALS = a grammatical particle from the closed lists below. You may use ONLY the particles listed here.
- lowercase English word = a native content root. Assume any ordinary, general-vocabulary content word
  exists as a root (run, big, test, sorrow, grape, wife...). A root has no noun/verb/adjective class:
  position decides its use. Do not treat function-like English words as roots to smuggle grammar in
  (no roots for: the, a, very, only, although, would, must, still, already, just, even, than, of...).
- Single capital letters (A, B, S, T...) = handles (short names bound to a thing).
- Latin text in « » = quoted text or foreign notation (code, formulas, units, proper-name originals).
- Proper names: write as name«Darwin» (a sound-borrowed loan).
- Technical terms: build with roots and linkers (store KIND data = database) or define with DEFINE.

## Sentence

```
sentence = [label ":"] opener [relation [label]] [cites] [strength] [attitude] body "."
body     = simple | IF block block [block] | OR block block
simple   = [NOT] [time] [aspect] predicate {role phrase}
block    = "{" body "}"
phrase   = [focus] [quantifier] head {linker modifier} [NAMED handle]
head     = root | handle | loan | «notation» | number | block | "(" phrase ")" | WHAT | SELF | STEP label | ME | YOU
answer   = opener (YES | NO | role phrase) "."
```

Order of the role phrases after the predicate is FREE and carries no meaning.

## Openers (obligatory, exactly one per sentence; clauses inside { } have none)

| Opener | Meaning |
|---|---|
| GIVEN | It is in the context: someone said it, or a document/tool shows it. Also used for direct report of what the writer observes. |
| DERIVED | Follows from earlier sentences; followed by the labels it rests on |
| RECALLED | From the writer's background knowledge |
| ASSUMED | Supposed for argument, not claimed |
| ASK | A question |
| REQUEST | Asks the other party to act |
| PLAN | Commits the writer to act |
| DEFINE | Introduces a definition: DEFINE term BE phrase-or-block |

## Relation to another sentence (optional, after the opener; default target = previous sentence)

CONTRAST, CONCEDE, RESULT, ADD, SEQUENCE, EXAMPLE, RESTATE, BACKGROUND

## Strength (optional): CERTAIN, LIKELY, POSSIBLE

## Attitude (optional): SURPRISE, EMPHASIS, POLITE, REGRET

## Inside the clause

- NOT negates the clause.
- Time: PAST, FUTURE (unmarked = now or timeless).
- Aspect: ONGOING, DONE, HABIT.
- Roles (particle before its phrase): AGENT, THEME, TO, FROM, AT, WHEN, WITH, CAUSE, FOR, THAN.
  - AGENT who acts; THEME what is acted on or described; TO recipient/end point; FROM origin;
    AT place; WHEN time; WITH means or manner; CAUSE cause/reason; FOR purpose/beneficiary;
    THAN standard of comparison.
- There is no "is": `GIVEN big THEME file .` = the file is big. `GIVEN big THEME A THAN B .` = A is bigger than B.

## Inside a phrase

- Linkers after the head: KIND narrows the head (error KIND network); OF marks owner or whole (file OF user).
- All modifiers attach to the head. A modifier needing its own modifier goes in ( ): error KIND (time KIND run).
- A clause can modify; SELF marks the head's place: test KIND { fail THEME SELF } = the test that failed.
- Quantifiers before the head: ALL, SOME, NO, or a number.
- Focus before what it picks out: ONLY, ALSO, EVEN, INSTEAD.
- WHAT stands in the slot a question asks about.
- NAMED binds a handle: setting NAMED S. Afterwards S alone refers to it. No third-person pronouns exist.
- STEP n refers to sentence n as a whole.

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

Question and fragment answer: `ASK fail THEME test KIND WHAT .` / `GIVEN THEME test KIND login .`
