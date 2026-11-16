# The language: rule sheet (version 1)

You write this language directly. A script, not a person, turns it back into English, so the rules are strict:
the script rejects anything that is not exactly in this sheet or in the word list.

In this sheet every example has three lines: the text as you must write it, the same words with their
NAMES (capitals = particle, lowercase = root, `~word` = loan, one capital letter = handle), and the
script's English. The names are only for explaining. You never write them.

## 1. Word shapes

A word is a run of Hangul blocks between spaces. Its shape tells its class.

| Shape | Class | Where it comes from |
|---|---|---|
| one block with no final consonant | particle | the closed lists in section 9. You may not invent one |
| one block with a final consonant | handle | you choose it; a short name for a thing (section 6) |
| open block + closed block | root | the word list only |
| one open block with a w-vowel (ㅘ ㅝ ㅚ ㅟ ㅢ) | code keyword | the 13 keywords in section 10; no other word uses these vowels |
| root + suffix blocks | derived word | section 7 |
| two or more blocks, all without finals | loan | spelled by the letter table (section 8) |
| digits | number, or a sentence label when followed by `:` | |
| `« »` | notation | symbols only: formulas, units, mathematical expressions, clock times; and names inside code. **Never English words** |

Punctuation: ` . ` ends a sentence (with a space before it). `{ }` hold a clause inside another. `( )` group.
Latin letters outside `« »` are an error.

## 2. The sentence

```
[BY speaker] [label:] OPENER [relations] [strength] [attitudes] [CALL person]  body  .
```

Every sentence starts with an opener that says what kind of statement it is. Number your sentences
(`1:` `2:` ...) whenever a later sentence may refer back.

The usual body is a clause: **predicate first, then the participants, each behind a role particle.**
The order of the participants is free and means nothing.

{{ex
1: GIVEN fail THEME test KIND ~login .
2: GIVEN PAST change AGENT YOU THEME configure.made NAMED S .
3: RECALLED HABIT read AGENT ALL test KIND ~login THEME S .
4: DERIVED 1 2 3 LIKELY cause AGENT STEP 2 THEME STEP 1 .
5: ASK PAST change AGENT YOU THEME ONLY S .
6: PLAN do.opp THEME S .
}}

There is no word for "is". A quality, a thing or a relation can be the predicate:

{{ex
GIVEN big THEME file .
CLAIM animal THEME ALL dog .
GIVEN inside REL box THEME key .
GIVEN ( error KIND NOT expect ) THEME E .
CLAIM BE THEME give.made FOR name«Ana» .
}}

### Header

- **Relations** come after the opener. Label numbers after a relation say which sentence it points at; with no
  number it points at the previous sentence. Several relations are allowed.
- **DERIVED** is followed directly by the labels it rests on.
- **Strength** and **attitude** follow. A number in `« »` may follow a strength.
- **CALL** names the person spoken to.
- **BY** before the label says whose words the sentence is (dialogue turns, quotations).

{{ex
7: GIVEN CONTRAST 5 NOT PAST change AGENT name«Ana» THEME S .
8: CLAIM CONCEDE 7 EXPLAIN 1 POSSIBLE SURPRISE new.opp THEME data .
BY A 9: ASK POLITE CALL name«Ben» DONE publish THEME version KIND new .
BY B 10: GIVEN ANSWER 9 NO .
BY A 11: SOCIAL thank .
}}

## 3. Before the predicate

Negation, time, aspect, modal, strength, focus and degree particles stand before the predicate, in any order.
**Each one applies to everything on its right.**

{{ex
CLAIM NOT STILL work AGENT serve.tool .
CLAIM STILL NOT work AGENT serve.tool .
RULE MUST NOT enter AGENT ANY person WHEN before REL 9 .
RULE NOT MUST pay AGENT child .
GIVEN PAST 3 TIMES fail THEME ALMOST ALL test .
CLAIM FUTURE NEAR BEGIN ready THEME report .
CLAIM WANT learn AGENT ME THEME language KIND new .
}}

- No time particle means "time as in the context". Mark a general law with GENERIC on the participant or with ALWAYS.
- Inside a `{ }` block, time is counted from the time of the clause around it.
- BEGIN with a state means "becomes".
- These particles outrank the amount words in the participants. For the other order use EACH (section 5).

## 4. Participants

**Which role?** AGENT is the one who controls the act or brings it about, and the one who knows, sees, wants
or has. THEME is what is acted on or described, and the one a thing merely happens to. The word list marks
each root: [A] roots have an AGENT as main participant, [E] [Q] [T] roots have a THEME.
Adding an AGENT to an [E] or [Q] root means "causes it": `die THEME x` = x dies; `die AGENT y THEME x` = y kills x.

**A role you leave out is unstated ("someone", "something"). It never means "the one mentioned before".**
Two exceptions: in a REQUEST the missing AGENT is the addressee; in a PLAN it is the writer.

{{ex
STORY PAST break THEME cup .
STORY PAST break AGENT child THEME cup .
STORY PAST give AGENT A THEME book TO B CAUSE holiday .
REQUEST bake THEME bread SPAN AROUND 40 minute AT bake.tool KIND ( VERY hot ) .
CLAIM MORE fast THEME A THAN B SPAN 2 second .
CLAIM MORE trust AGENT name«Ana» THEME test THAN AGENT name«Ben» .
CLAIM 2 EQUAL big THEME A THAN B .
CLAIM EQUAL THEME A THAN B .
}}

Any role may take a `{ }` block in place of a phrase: WHEN {…} = when, CAUSE {…} = because, FOR {…} = so that,
EXCEPT {…} = unless, DESPITE {…} = although, THEME {…} = that.

{{ex
CLAIM PAST fail THEME build CAUSE { NOT exist THEME file KIND configure } .
CLAIM know AGENT A THEME { PAST arrive AGENT B } .
CLAIM know AGENT A THEME { ASK PAST take AGENT WHAT person THEME key } .
STORY PAST say AGENT A THEME { BY A PLAN help THEME YOU } .
}}

A block with no opener is a bare statement (reported, not asserted). A block with an opener has its own force
(the third example holds a question). A block with BY holds that speaker's own words: inside it ME is that speaker.

## 5. Inside a phrase

```
[focus] [NOT] [amount words] HEAD [NAMED handle] [linker modifier]...
```

- A bare head says nothing about number or definiteness. Add an amount word only when it matters.
- Degree words may stand before amount words: ALMOST ALL, TOO MANY, MORE (more of), WHAT MANY (how many).
- Linkers attach modifiers to the head. Every modifier attaches to the head, never to the modifier before it.
  A modifier that needs its own modifier goes in `( )`.
- **KIND** narrows. **OF** gives the owner or the whole. **REL** gives the second thing of a relational root
  (marked [R] in the word list): before REL x, cause REL x, part REL x. **HAVING** is what the head has.
  **NOTE** adds a comment or the full list. **SUCHAS** gives examples.
- A `{ }` block after KIND is a relative clause; SELF marks the head's place in it.
- A quality or act root used as a head names the quality or the event: `fail OF test` = the failure of the test.
  "A big one" is `thing KIND big`.

{{ex
GIVEN PAST fail THEME ORD 3 test KIND { PAST write AGENT YOU THEME SELF } .
CLAIM red THEME door OF house KIND ( VERY new.opp ) .
CLAIM need AGENT function HAVING 2 parameter THEME ATLEAST 3 test .
CLAIM use AGENT MANY language SUCHAS ( ~python AND ~rust ) THEME ~llvm .
ASK exist THEME WHAT MANY error AT THIS file .
CLAIM PAST arrive AGENT guest WHEN ago REL 2 day .
CLAIM see AGENT ( A AND B ) THEME MUTUAL .
}}

**Joining.** AND, OR (one or both), XOR (exactly one) join phrases. ANDC, ORC, BUT join whole clauses; a relation
may follow them. Mixing different joiners at one level needs brackets.

{{ex
CLAIM PAST fail THEME test ANDC RESULT PAST STOP build AGENT US .
CLAIM expensive.opp THEME plan.made BUT NOT safe THEME plan.made .
}}

**Conditions and "for each".**

{{ex
CLAIM IF { fall THEME rain } { STILL wet THEME road } .
CLAIM IF { MORE big THEME file } { MORE fast.opp THEME load } .
CLAIM EACH X IN ALL number KIND even { exist THEME SOME number NAMED Y KIND { EQUAL THEME X THAN ( multiply FIRST 2 SECOND Y ) } } .
}}

Two MORE/LESS clauses under IF with no THAN mean "the more ..., the more ...".

**Scope is shown by nesting.** NOT, a modal (MUST, CAN ...), a strength word (LIKELY ...) or a tone word may be followed by a block; it then covers exactly what is in the block. Without a block it covers only its own predicate.

{{ex
1: RULE NOT { use AGENT YOU THEME water KIND hot CAUSE { harm AGENT water KIND hot THEME A } } .
2: CLAIM NOT go AGENT ME CAUSE { rain } .
3: CLAIM IF { increase THEME price } { LIKELY { search AGENT ME THEME house KIND new } } { stay AGENT ME } .
}}

Sentence 1 denies the whole thing, reason included; sentence 2 says the going did not happen, and gives the reason. Amount words (ALL, SOME ...) in one clause make no claim about which is the outer one. When that matters, nest: `EACH A IN ALL person { exist THEME SOME book NAMED B KIND { read AGENT A THEME SELF } }` gives each person their own book; `exist THEME SOME book NAMED B KIND { EACH A IN ALL person { read AGENT A THEME B } }` is one book for all.

**Uncommitted thoughts.** CONSIDER opens a thought the writer is weighing without holding it: not claimed, not supposed for a proof, not proposed as an action. Use it for a position being tried on, one side of an argument, or a guess not yet checked. A sentence that rests on a CONSIDER sentence should itself be CONSIDER, or cite it with UNDER.

{{ex
1: CONSIDER cause AGENT error KIND remember THEME fail OF program .
2: CLAIM NOT ALREADY check AGENT ME THEME STEP 1 .
}}

**Suppositions.** Open one with ASSUMED and a label; mark every step inside it with UNDER and that label;
the conclusion outside lists the labels it rests on.

{{ex
1: ASSUMED infinite.opp THEME number.group KIND prime .
2: DERIVED 1 UNDER 1 exist THEME number NAMED P KIND prime KIND ( MOST big ) .
3: DERIVED 1 2 NOT infinite.opp THEME number.group KIND prime .
}}

**Questions and answers.** WHAT stands where the unknown is. YES and NO answer the question's clause exactly as
it was written, negation included. A fragment (a role phrase, a phrase, YES or NO) may be a whole answer.

{{ex
1: ASK fail THEME test KIND WHAT .
2: GIVEN ANSWER 1 THEME test KIND ~login .
3: ASK YES NOT ALREADY arrive AGENT THAT guest .
4: GIVEN ANSWER 3 YES .
}}

## 6. Handles instead of pronouns

There is no "he", "she", "it" or "they". The first time a thing matters, bind a handle to it with NAMED; after
that the handle alone refers to it, in every later sentence, until you bind the same handle to something else.
A handle is any single block with a final consonant. Suggested: {{handles}}

Use THAT + root ("the test") only when one thing of that kind is in play. STEP + label refers to a whole sentence.

## 7. New words

Take the first of these that works. Never invent a root form.

1. **A root from the word list.**
2. **Root + suffix** (written as one word):

{{suffixes}}

3. **A compound with KIND**: `store KIND data` = database; `parent KIND female` = mother.
4. **A loan** for names and for terms with no good native build (section 8).
5. **A spare word** for a concept you will use many times: pick an unused spare form and define it once.
   The definition sentence is all the script needs.

{{ex
DEFINE SPARE1 BE program KIND { read AGENT SELF THEME code ANDC SEQUENCE execute AGENT SELF THEME code } .
}}

The first spare forms (the full list is at the end of the word list): {{spares}}

When the word list has both a root and a derived word for one meaning, use the root. A derived word that is not in the list is still valid: build it by rule, and the reader takes it apart by rule. A spare word may be defined as a thing, an act or a quality, and may take suffixes.

## 8. Loans, names and notation

A loan spells an English word letter by letter with this table. A consonant letter and the vowel-class letter
right after it share one block; a consonant with no vowel-class letter after it takes the "no vowel" vowel;
a vowel-class letter with no consonant before it takes the empty initial. Loans have no final consonants.

{{loantable}}

Examples: python = {{n:~python}}, test = {{n:~test}}, stack = {{n:~stack}}, linux = {{n:~linux}}, why = {{n:~why}}.
Two vowel-class letters in a row: the second gets its own block with the empty initial: nation = {{n:~nation}}, huxley = {{n:~huxley}}. Check each vowel against the table; do not guess its shape.

- NAME before a loan or root makes it a proper name: {{n:NAME ~Darwin}} = Darwin. A name of several words is
  `NAME ( ... )` with each word a loan: `NAME ( ~Winston ~Churchill )`.
- Prefer roots, suffixes and compounds for ordinary meanings. **For a technical term, an abbreviation or a name that
  no root covers, use a loan. This is the normal, expected way; do not avoid it.**
- **Everything written without a space is one loan word, spelled character by character**, with its capitals,
  digits, hyphens and other signs kept, using the extra blocks below. So IL-4, 5-HT1A, 2,4-dinitrophenol, HbA1c, Hückel
  and β-catenin are each one word.
- **A term of several words** is loans side by side; they form one term: `~affinity ~maturation`,
  `~long-term ~potentiation`, `~Type ~Ia ~supernova`.

Extra blocks inside a loan:

{{loanextra}}

Examples: IL-4 = {{n:~IL-4}}, NMDA = {{n:~NMDA}}, 5-HT1A = {{n:~5-HT1A}}, Hückel = {{n:~Hückel}}, β-catenin = {{n:~β-catenin}},
ΔG = {{n:~ΔG}}, pi = {{n:~pi}}, Okafor-Lindqvist = {{n:~Okafor-Lindqvist}}, CaMKII = {{n:~CaMKII}}.

- **Capitals.** {{capblk}} before a block makes its first letter a capital. {{lockblk}} switches capitals on, and a second
  {{lockblk}} switches them off again (not needed at the end of the word). A consonant and a following vowel-class letter
  share a block only when the vowel-class letter is lower case, or both are inside a capitals stretch.
- **Greek.** {{greekblk}} before a letter makes it Greek: {{greekmap}}. For a capital Greek letter put {{greekblk}} then {{capblk}}.
- **Accents** follow the letter they sit on.
- A loan needs two blocks. If the word would be a single block (pi, c), put {{padblk}} in front of it.
- **No English outside code.** `« »` is not a way to write a word. Outside code it holds only: a chemical formula
  (`«H2SO4»`, `«Ca2+»`), a unit after a number (`30 «km/h»`, `48 «mmol/mol»`), a mathematical expression or a
  one-letter variable (`«v0 - g*t»`, `«x»`), a clock time (`«16:12»`). The checker refuses a word or an abbreviation
  in `« »` outside code: write `~DNA`, `~Km`, `~IL-4`, never `«DNA»`.
- Text of a program mentioned in prose (an identifier, a file name, an error name) is marked with the code word
  before it: `CODE «IndexError»`, `CODE «config.yaml»`.

## 9. The particles

The consonant of a particle shows its slot.

{{alltables}}

## 10. Logic

Logic uses the same clause with numbered slots in place of roles, so it can be turned into code.

```
( function FIRST x SECOND y )        a function call; EQUAL, MORE, LESS and roots such as add, multiply, remainder
DEFINE name FIRST h1 SECOND h2 BE { statement . statement . }      a function
DEFINE handle BE expression          assignment
IF { condition } { then } { else }   EACH h IN expression { ... }   WHILE { condition } { ... }   RETURN expression
```

`DEFINE ( phrase ) BE «identifier»` gives the code name of a native term.

**Code keywords.** DEFINE, BE, RETURN, IMPORT, CODE, IF, EACH, IN, WHILE and the slots FIRST to FOURTH are written with w-vowel blocks, a shape nothing else has. They keep the same shape in prose and proofs.

**All code is written in this form**, never as source text inside `« »`. Only names (identifiers, library members, formulas) go in `« »`.

**Language.** `CODE «python»` on a line of its own names the programming language of the code that follows, until the next CODE line. The converter writes that language (Python and JavaScript so far).

**Libraries.** A library must be imported and given a handle before use: `IMPORT «math» NAMED M`. A member is then written `«sqrt» OF M`. A dotted name such as `«math.sqrt»` is refused in code.

{{ex
CODE «python» .
IMPORT «math» NAMED M .
DEFINE ( long.ness KIND line ) BE «hyp» .
DEFINE ( long.ness KIND line ) FIRST A SECOND B BE ( «sqrt» OF M FIRST ( add FIRST ( multiply FIRST A SECOND A ) SECOND ( multiply FIRST B SECOND B ) ) ) .
}}

{{ex
DEFINE ( add.made KIND even ) BE «sum_even» .
DEFINE ( add.made KIND even ) FIRST L BE { DEFINE T BE 0 . EACH X IN L { IF { EQUAL FIRST ( remainder FIRST X SECOND 2 ) SECOND 0 } { DEFINE T BE ( add FIRST T SECOND X ) } } . RETURN T } .
}}

More logic conventions:

- The function position may hold a root, a bracketed compound `( search KIND half )`, a spare word, or a `« »` name.
- `item FIRST list SECOND n` is the item at position n (counting from 0). `count FIRST list` is the length of the list.
- `quotient FIRST a SECOND b` is whole-number division; `divide` is exact division.
- NOT may stand before a comparison. `RETURN EMPTY` returns nothing. An IF may sit inside any block.
- Statements inside a block are separated by ` . `; none is needed before the closing brace.

{{ex
DEFINE ( item KIND middle ) FIRST L BE { DEFINE N BE ( quotient FIRST ( count FIRST L ) SECOND 2 ) . IF { NOT MORE FIRST N SECOND 0 } { RETURN EMPTY } . RETURN ( item FIRST L SECOND N ) } .
}}

Mathematics:

- **For every.** `EACH x IN set { ... }` may open a sentence, stand inside any block, or follow ANDC, ORC or BUT. Use it for "for all n".
- **The n-th.** ORD takes a number or a handle: `ORD 3 step`, `ORD B number KIND even.opp` (the B-th odd number). A range is `ORD 1 UPTO B` before the head; either end may be a number, a handle or a bracketed expression.
- **n of them.** A handle may stand as a count before a root: `B number` (B numbers).
- **Numbers.** Decimals and negative numbers are written plainly: `9.8`, `-2`, `0.117`. A full stop is a sentence end only when it stands alone between spaces. Clock times go in notation: `«16:12»`.
- **Maps and text.** `«{}»` is the empty map and `«""»` the empty text. `item FIRST map SECOND key` looks a key up. `«put» FIRST map SECOND key THIRD value` is the map with that entry set. `contain FIRST collection SECOND x` tests whether x is in a list or is a key of a map. `«rest» FIRST list` is the list without its first item.
- **Lists.** `«[]»` is the empty list. `«append» FIRST list SECOND item` is the list with the item added at the end.
- **Two-part conditions.** Join comparisons with ANDC or ORC inside the condition block.
- **Proof steps.** Open each step with the evidence particle (GIVEN, ASSUMED, DERIVED with labels) and cite the labels. State what is being supposed with ASSUMED and discharge it with a DERIVED IF sentence.

{{ex
RECALLED EACH B IN ALL integer KIND positive { EQUAL THEME ( ORD B number KIND even.opp ) THAN ( add.opp FIRST ( multiply FIRST 2 SECOND B ) SECOND 1 ) } .
RECALLED IF { true THEME say.made NAMED A ABOUT 1 ANDC EACH B IN ALL integer KIND positive { IF { true THEME A ABOUT B } { true THEME A ABOUT ( add FIRST B SECOND 1 ) } } } { true THEME A ABOUT ALL integer KIND positive } .
DEFINE ( join KIND end ) FIRST C SECOND D BE { WHILE { LESS FIRST 0 SECOND ( count FIRST D ) ANDC LESS FIRST ( count FIRST C ) SECOND 9 } { DEFINE C BE ( «append» FIRST C SECOND ( item FIRST D SECOND 0 ) ) . DEFINE D BE «[]» } . RETURN C } .
}}

## 11. Small conventions

- **Headings.** `HEAD` takes a bare phrase; a number goes after it, and a title may follow with NOTE: `HEAD section 2 NOTE prove.made`.
- **Numbered and named things.** A number or `« »` straight after a root is that thing's number or name: `section 1`, `year 1919`, `task «K01»`. Dates: `WHEN ORD 14 day OF ( month KIND NAME ~june OF year 1919 )`. Money and units: `1200 «EUR»`.
- **Header order.** A relation may stand before or after the opener: `REBUT 24 CLAIM ...` and `CLAIM REBUT 24 ...` are the same. In dialogue the speaker comes first: `BY A 27: CLAIM ...`; the speaker may be described, `BY person NAMED A KIND { ... }`.
- **Focus words** (ONLY, ALSO, EVEN) may stand after a linker (`REL ONLY ( C AND D )`) and before a fronted role phrase (`ALSO AT moon ...`).
- **Order.** The predicate normally comes first, but role phrases (WHEN, AT, PER, IF-like conditions and the rest) may also stand before it. Keep each role phrase next to the clause it belongs to.
- **Days, months, people, places.** `NAME` plus a loan; several words in `NAME ( ... )`. A name that labels a kind goes after KIND.
- **Handles** stay bound for the whole text, across headings. Labels count on through the whole text too.
- **BY** may be followed by a handle, a name, or any phrase.
- **A reply that starts with a number** needs a role particle first, because a number straight after a relation is read as a label.
- **YES and NO** answer the clause exactly as written. To ask "isn't it so?", ask the positive clause with `ASK YES`.
- **Act or product.** An act root used as a head names the act ("the reporting"); add the made-suffix for the thing produced ("the report").
- **Relational roots** (type R, such as part, before, cause) take REL for their second term, never OF.
- **Making someone do something.** For a quality or event root, adding an AGENT means "causes it". For an act root the AGENT is already the doer, so use cause with a block.
- **At the same time.** `ALONG { ... }` means "while ...". **For the first time**: `ORD 1 TIMES`.
- **About, inside a phrase.** Put the role in brackets with its head: `( evidence ABOUT fact )`.
- **SELF** inside a KIND block is the thing that block describes (the nearest one). Anywhere else it is the AGENT of its own clause.
- **We.** US leaves the addressee out; WE includes the addressee.

{{ex
HEAD task 2 .
1: PLAN travel WHEN NAME ~friday .
2: CLAIM cause AGENT rain THEME { fall AGENT ALL leaf } .
3: STORY sing AGENT bird ALONG { rise THEME sun } .
4: GIVEN ORD 1 TIMES fail THEME test ABOUT CODE «User-Agent» .
5: PROPOSE check AGENT WE THEME ( evidence ABOUT THAT fact ) .
}}

### Patterns that writers often ask for

- **A measured value.** `EQUAL THEME ( pressure OF blood ) THAN AROUND 55 «mmHg»`. Above or below a number: `MORE THEME pressure THAN 70 «mmHg»`. A value attached to a noun: `field HAVING strong.ness OF 9.4 «T»`, `signal AT 1.2 «ppm»`.
- **Large and small numbers** go in notation: `«6×10^5»`, `«8.3×10^-11»`; such a symbol may stand as a count before a noun (`«n» step`, `«2^30» cell`).
- **Before, after, until** take a thing, a time or a clause: `WHEN before REL { open AGENT A THEME door }`, `WHEN after REL { ... }`, `WHEN until REL { ... }`. A delay is added with SPAN: `WHEN after REL { inject THEME vaccine } SPAN 5 UPTO 7 day` = 5 to 7 days after the injection.
- **Ranges.** `3 UPTO 7 day`, `year 2000 UPTO 2009`, `50 UPTO 65 «°C»`, `10 UPTO 100 TIMES`. Month and year without a day: `WHEN month 5 OF year 2000`.
- **A common misconception.** State it as what people believe, with TOLD, then rebut that sentence: `7: TOLD believe AGENT MANY person THEME { ... } .` then `8: CLAIM REBUT 7 wrong THEME THAT idea CAUSE { ... } .`
- **Becoming N times as big.** `BEGIN 2 EQUAL big THEME amount PER 8 second` = the amount doubles every 8 seconds.
- **What would happen otherwise** (counterfactual): an IF sentence under the opener ASSUMED or CONSIDER.
- **Only when, even before.** A focus word may stand before any role phrase: `accept AGENT A THEME item ONLY WHEN { ... }`.

## 12. Checklist before you finish a sentence

- It starts with an opener and ends with ` .`
- The predicate comes before its participants, and every participant has a role particle.
- Every root is in the word list (or is root + suffix, or a defined spare). Every particle is in section 9.
- No pronouns: handles, THAT + root, or the noun again.
- Nothing left out that the reader needs: a missing role means "unstated".
- Latin letters only inside `« »`, and no English words there outside code: terms and names are loans.
