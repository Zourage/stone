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
| root + suffix blocks | derived word | section 7 |
| two or more blocks, all without finals | loan | spelled by the letter table (section 8) |
| digits | number, or a sentence label when followed by `:` | |
| `« »` | notation | anything in Latin letters: code, formulas, units, quoted foreign text |

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

```
1: 가 버닝 새 다롯 라 챠보터 .
    1: GIVEN fail THEME test KIND ~login .
    = 1. [given] The login test fails.

2: 가 해 느참 사 애 새 포점엄 차 각 .
    2: GIVEN PAST change AGENT YOU THEME configure.made NAMED S .
    = 2. [given] You changed the setting (call it S).

3: 거 쟈 스청 사 마 다롯 라 챠보터 새 각 .
    3: RECALLED HABIT read AGENT ALL test KIND ~login THEME S .
    = 3. [recalled] All login tests usually read setting S.

4: 갸 1 2 3 배 파킨 사 츠 2 새 츠 1 .
    4: DERIVED 1 2 3 LIKELY cause AGENT STEP 2 THEME STEP 1 .
    = 4. [it follows from 1, 2, 3; likely] Step 2 causes step 1.

5: 구 해 느참 사 애 새 파 각 .
    5: ASK PAST change AGENT YOU THEME ONLY S .
    = 5. [question] You changed only setting S?

6: 기 깨춘안 새 각 .
    6: PLAN do.opp THEME S .
    = 6. [plan] I undo setting S.
```

There is no word for "is". A quality, a thing or a relation can be the predicate:

```
가 떠못 새 츠춧 .
    GIVEN big THEME file .
    = [given] The file is big.

겨 헤숭 새 마 코롤 .
    CLAIM animal THEME ALL dog .
    = [claim] All dogs are animals.

가 깨믓 랴 케폰 새 캐빔 .
    GIVEN inside REL box THEME key .
    = [given] The key is inside the box.

가 ( 체낫 라 하 까름 ) 새 각 .
    GIVEN ( error KIND NOT expect ) THEME E .
    = [given] E is an error that is not expected.

겨 체 새 뻬찻엄 수 처 우투 .
    CLAIM BE THEME give.made FOR name«Ana» .
    = [claim] The gift is for Ana.
```

### Header

- **Relations** come after the opener. Label numbers after a relation say which sentence it points at; with no
  number it points at the previous sentence. Several relations are allowed.
- **DERIVED** is followed directly by the labels it rests on.
- **Strength** and **attitude** follow. A number in `« »` may follow a strength.
- **CALL** names the person spoken to.
- **BY** before the label says whose words the sentence is (dialogue turns, quotations).

```
7: 가 다 5 하 해 느참 사 처 우투 새 각 .
    7: GIVEN CONTRAST 5 NOT PAST change AGENT name«Ana» THEME S .
    = 7. [given; in contrast to 5] Ana did not change S.

8: 겨 대 7 데 1 뱌 빠 체증안 새 거통 .
    8: CLAIM CONCEDE 7 EXPLAIN 1 POSSIBLE SURPRISE new.opp THEME data .
    = 8. [claim; even though 7; explaining 1; possible; surprised] The data is old.

채 낙 9: 구 뺘 챠 처 키터 재 페튼 새 두깁 라 체증 .
    BY A 9: ASK POLITE CALL name«Ben» DONE publish THEME version KIND new .
    = 9. A: [question; polite; to Ben] The new version has been published?

채 닥 10: 가 때 9 푸 .
    BY B 10: GIVEN ANSWER 9 NO .
    = 10. B: [given; answering 9] No.

채 낙 11: 깨 푸펍 .
    BY A 11: SOCIAL thank .
    = 11. A: [social act] Thank.
```

## 3. Before the predicate

Negation, time, aspect, modal, strength, focus and degree particles stand before the predicate, in any order.
**Each one applies to everything on its right.**

```
겨 하 져 메훌 사 삐필옹 .
    CLAIM NOT STILL work AGENT serve.tool .
    = [claim] The server no longer works.

겨 져 하 메훌 사 삐필옹 .
    CLAIM STILL NOT work AGENT serve.tool .
    = [claim] The server still does not work.

교 카 하 뜨힝 사 묘 쁘칸 셔 노축 랴 9 .
    RULE MUST NOT enter AGENT ANY person WHEN before REL 9 .
    = [rule] Any person must not enter before 9.

교 하 카 째츰 사 으룻 .
    RULE NOT MUST pay AGENT child .
    = [rule] The child does not have to pay.

가 해 3 쨔 버닝 새 테 마 다롯 .
    GIVEN PAST 3 TIMES fail THEME ALMOST ALL test .
    = [given] Almost all tests failed 3 times.

겨 햐 혀 저 으팁 새 뻬갈 .
    CLAIM FUTURE NEAR BEGIN ready THEME report .
    = [claim] The report will soon become ready.

겨 케 머덤 사 아 새 머핏 라 체증 .
    CLAIM WANT learn AGENT ME THEME language KIND new .
    = [claim] I want to learn the new language.
```

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

```
고 해 크헉 새 끼봅 .
    STORY PAST break THEME cup .
    = [story] The cup broke.

고 해 크헉 사 으룻 새 끼봅 .
    STORY PAST break AGENT child THEME cup .
    = [story] The child broke the cup.

고 해 뻬찻 사 각 새 뻬물 샤 낙 쇼 모놀 .
    STORY PAST give AGENT A THEME book TO B CAUSE holiday .
    = [story] A gave the book to B because of the holiday.

규 두멋 새 노손 쌔 네 40 쏘섭 세 두멋옹 라 ( 타 쩌팃 ) .
    REQUEST bake THEME bread SPAN AROUND 40 minute AT bake.tool KIND ( VERY hot ) .
    = [request] Bake the bread for about 40 minutes at the very hot oven.

겨 툐 꺼득 새 각 슈 낙 쌔 2 흐훗 .
    CLAIM MORE fast THEME A THAN B SPAN 2 second .
    = [claim] A is more fast than B for 2 seconds.

겨 툐 드풋 사 처 우투 새 다롯 슈 사 처 키터 .
    CLAIM MORE trust AGENT name«Ana» THEME test THAN AGENT name«Ben» .
    = [claim] Ana trusts the test more than Ben does.

겨 2 티 떠못 새 각 슈 낙 .
    CLAIM 2 EQUAL big THEME A THAN B .
    = [claim] A is 2 times as big as B.

겨 티 새 각 슈 낙 .
    CLAIM EQUAL THEME A THAN B .
    = [claim] A is equal to B.
```

Any role may take a `{ }` block in place of a phrase: WHEN {…} = when, CAUSE {…} = because, FOR {…} = so that,
EXCEPT {…} = unless, DESPITE {…} = although, THEME {…} = that.

```
겨 해 버닝 새 아함 쇼 { 하 헤즌 새 츠춧 라 포점 } .
    CLAIM PAST fail THEME build CAUSE { NOT exist THEME file KIND configure } .
    = [claim] The construction failed because the configure file does not exist.

겨 서맛 사 각 새 { 해 거방 사 낙 } .
    CLAIM know AGENT A THEME { PAST arrive AGENT B } .
    = [claim] A knows that B arrived.

겨 서맛 사 각 새 { 구 해 네절 사 여 쁘칸 새 캐빔 } .
    CLAIM know AGENT A THEME { ASK PAST take AGENT WHAT person THEME key } .
    = [claim] A knows that [question] which person took the key?

고 해 구굴 사 각 새 { 채 각 기 브홍 새 애 } .
    STORY PAST say AGENT A THEME { BY A PLAN help THEME YOU } .
    = [story] A said A: “[plan] I help you”.
```

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

```
가 해 버닝 새 너 3 다롯 라 { 해 오덕 사 애 새 어 } .
    GIVEN PAST fail THEME ORD 3 test KIND { PAST write AGENT YOU THEME SELF } .
    = [given] The 3rd test that you wrote failed.

겨 소솝 새 쪼친 래 비눕 라 ( 타 체증안 ) .
    CLAIM red THEME door OF house KIND ( VERY new.opp ) .
    = [claim] The very old door of the house is red.

겨 노함 사 째블 레 2 러숭 새 노 3 다롯 .
    CLAIM need AGENT function HAVING 2 parameter THEME ATLEAST 3 test .
    = [claim] The function with 2 parameters needs at least 3 tests.

겨 제볼 사 먀 머핏 려 ( 빠쩌먀터 로 게허쩌 ) 새 처처떠러 .
    CLAIM use AGENT MANY language SUCHAS ( ~python AND ~rust ) THEME ~llvm .
    = [claim] Many languages such as python and rust use the llvm.

구 헤즌 새 여 먀 체낫 세 미 츠춧 .
    ASK exist THEME WHAT MANY error AT THIS file .
    = [question] How many errors exist at this file?

겨 해 거방 사 타팅 셔 빠좃 랴 2 츠킁 .
    CLAIM PAST arrive AGENT guest WHEN ago REL 2 day .
    = [claim] The guest arrived 2 days ago.

겨 러존 사 ( 각 로 낙 ) 새 에 .
    CLAIM see AGENT ( A AND B ) THEME MUTUAL .
    = [claim] A and B see each other.
```

**Joining.** AND, OR (one or both), XOR (exactly one) join phrases. ANDC, ORC, BUT join whole clauses; a relation
may follow them. Mixing different joiners at one level needs brackets.

```
겨 해 버닝 새 다롯 류 댜 해 제 아함 사 야 .
    CLAIM PAST fail THEME test ANDC RESULT PAST STOP build AGENT US .
    = [claim] The test failed, and so we stopped building.

겨 거캄안 새 으믹엄 리 하 빠식 새 으믹엄 .
    CLAIM expensive.opp THEME plan.made BUT NOT safe THEME plan.made .
    = [claim] The plan is cheap, but the plan is not safe.
```

**Conditions and "for each".**

```
겨 쳐 { 카든 새 쑤함 } { 져 떠핌 새 어킁 } .
    CLAIM IF { fall THEME rain } { STILL wet THEME road } .
    = [claim] If the rain falls, then the road is still wet.

겨 쳐 { 툐 떠못 새 츠춧 } { 툐 꺼득안 새 캐밧 } .
    CLAIM IF { MORE big THEME file } { MORE fast.opp THEME load } .
    = [claim] If the file is more big, then the load is more slow.

겨 초 각 쵸 마 사툭 라 치팟 { 헤즌 새 메 사툭 차 낙 라 { 티 새 각 슈 ( 서합 오 2 요 낙 ) } } .
    CLAIM EACH X IN ALL number KIND even { exist THEME SOME number NAMED Y KIND { EQUAL THEME X THAN ( multiply FIRST 2 SECOND Y ) } } .
    = [claim] For each X in all even numbers: some number such that X is equal to multiply(2, Y) (call it Y) exists.
```

Two MORE/LESS clauses under IF with no THAN mean "the more ..., the more ...".

**Suppositions.** Open one with ASSUMED and a label; mark every step inside it with UNDER and that label;
the conclusion outside lists the labels it rests on.

```
1: 게 체천안 새 사툭엣 라 히깃 .
    1: ASSUMED infinite.opp THEME number.group KIND prime .
    = 1. [suppose] The prime set of numbers is finite.

2: 갸 1 따 1 헤즌 새 사툭 차 각 라 히깃 라 ( 튜 떠못 ) .
    2: DERIVED 1 UNDER 1 exist THEME number NAMED P KIND prime KIND ( MOST big ) .
    = 2. [it follows from 1; under the supposition of 1] The prime most big number (call it P) exists.

3: 갸 1 2 하 체천안 새 사툭엣 라 히깃 .
    3: DERIVED 1 2 NOT infinite.opp THEME number.group KIND prime .
    = 3. [it follows from 1, 2] The prime set of numbers is not finite.
```

**Questions and answers.** WHAT stands where the unknown is. YES and NO answer the question's clause exactly as
it was written, negation included. A fragment (a role phrase, a phrase, YES or NO) may be a whole answer.

```
1: 구 버닝 새 다롯 라 여 .
    1: ASK fail THEME test KIND WHAT .
    = 1. [question] What kind of test fails?

2: 가 때 1 새 다롯 라 챠보터 .
    2: GIVEN ANSWER 1 THEME test KIND ~login .
    = 2. [given; answering 1] The login test.

3: 구 표 하 죠 거방 사 므 타팅 .
    3: ASK YES NOT ALREADY arrive AGENT THAT guest .
    = 3. [question, expecting yes] The guest does not arrive yet?

4: 가 때 3 표 .
    4: GIVEN ANSWER 3 YES .
    = 4. [given; answering 3] Yes.
```

## 6. Handles instead of pronouns

There is no "he", "she", "it" or "they". The first time a thing matters, bind a handle to it with NAMED; after
that the handle alone refers to it, in every later sentence, until you bind the same handle to something else.
A handle is any single block with a final consonant. Suggested: 각 낙 닥 막 박 삭 작 학 곡 녹 독 목 복 속 족 혹 국 눅 둑 묵 북 숙 죽 훅

Use THAT + root ("the test") only when one thing of that kind is in play. STEP + label refers to a whole sentence.

## 7. New words

Take the first of these that works. Never invent a root form.

1. **A root from the word list.**
2. **Root + suffix** (written as one word):

| Suffix | Name | Meaning | Example |
|---|---|---|---|
| 안 | opp | the opposite pole; the act that undoes | big.opp = small; do.opp = undo |
| 일 | doer | the one who does it or is marked by it | teach.doer = teacher |
| 엄 | made | the product, or the thing it is done to | write.made = text; add.made = sum |
| 옹 | tool | the instrument made for it | cut.tool = knife; compute.tool = computer |
| 욱 | place | the place where it is done or kept | cook.place = kitchen |
| 음 | ness | the abstract state | friend.ness = friendship |
| 엣 | group | a collection taken as one unit | tree.group = forest |
| 앱 | able | able to undergo it | read.able = readable |

3. **A compound with KIND**: `store KIND data` = database; `parent KIND female` = mother.
4. **A loan** for names and for terms with no good native build (section 8).
5. **A spare word** for a concept you will use many times: pick an unused spare form and define it once.
   The definition sentence is all the script needs.

```
까 사붕 체 무섭 라 { 스청 사 어 새 즈밉 류 도 에잔 사 어 새 즈밉 } .
    DEFINE SPARE1 BE program KIND { read AGENT SELF THEME code ANDC SEQUENCE execute AGENT SELF THEME code } .
    = [definition] “W1” means a program that reads the code and then executes the code.
```

Spare forms: 사붕 모민 거뭄 포법 누룰 띠밧 서작 두덜 호쿳 베릉 스폽 패찬 배닷 우는 부난 쭈박 아핀 꾸툭 리김 쑤닛 무톰 추팝 버산 스갈 르근 머훕 싸독 코딤 두닉 추친 페놈 시닥 띠훔 쯔밀 에핌 무홉 우맘 코콘 어슥 하찹

## 8. Loans, names and notation

A loan spells an English word letter by letter with this table. A consonant letter and the vowel-class letter
right after it share one block; a consonant with no vowel-class letter after it takes the "no vowel" vowel;
a vowel-class letter with no consonant before it takes the empty initial. Loans have no final consonants.

Consonant letters: b=ㅋ, c=ㄴ, d=ㅅ, f=ㅍ, g=ㅂ, h=ㅁ, j=ㅈ, k=ㄷ, l=ㅊ, m=ㄹ, n=ㅌ, p=ㅃ, q=ㄲ, r=ㄱ, s=ㅎ, t=ㅉ, v=ㄸ, z=ㅆ

Vowel-class letters (a e i o u and also w y x): a=ㅜ, e=ㅣ, i=ㅗ, o=ㅑ, u=ㅔ, w=ㅡ, y=ㅏ, x=ㅐ

No vowel-class letter follows the consonant: vowel ㅓ. No consonant before the vowel: initial ㅇ.

Examples: python = 빠쩌먀터, test = 찌허쩌, stack = 허쭈너더, linux = 초테애, why = 으마.

- A loan must have at least two blocks. A one-letter word goes in `« »`.
- NAME before a loan or root makes it a proper name: 처 수그오터 = Darwin. Names with spaces, digits or
  punctuation go in `« »` after NAME, or NAME before each word.
- Keep loans rare: prefer roots, suffixes and compounds for ordinary meanings.
- `« »` holds anything that must stay exactly as it is: code, identifiers, file names, formulas (`«H2SO4»`),
  units (`30 «km/h»`), quoted foreign words. Digits are written as digits.

## 9. The particles

The consonant of a particle shows its slot.

### Openers: what kind of statement this is (first word of every sentence)

| Form | Name | Meaning |
|---|---|---|
| 가 | GIVEN | I observe it in the context myself (a file, a tool result, what is in front of me) |
| 개 | TOLD | another party says so and I have not checked; a handle may follow to name who |
| 갸 | DERIVED | follows from earlier sentences; their labels follow. With no labels: inferred from unstated evidence ("apparently") |
| 거 | RECALLED | from my background knowledge |
| 게 | ASSUMED | supposed for the sake of argument, not claimed |
| 겨 | CLAIM | I assert it and give no source (also my own states: I think, I prefer, I do not know) |
| 고 | STORY | narrated as part of a story or scenario, not asserted as fact |
| 교 | RULE | holds because it is laid down here (law, standard, policy) |
| 구 | ASK | a question. YES or NO may follow: the answer expected |
| 규 | REQUEST | asks or instructs someone to act; with no AGENT the addressee acts |
| 그 | PROPOSE | suggests an action without instructing ("let us", "you could") |
| 기 | PLAN | commits to act; with no AGENT the writer acts |
| 까 | DEFINE | DEFINE term BE meaning. Also binds spare words and logic names |
| 깨 | SOCIAL | a social act done by saying it: thanks, greeting, apology, agreement. A bare root follows |
| 꺄 | HEAD | a title or heading; a bare phrase follows |

### Relations: how this sentence relates to another (after the opener; label numbers may follow)

| Form | Name | Meaning |
|---|---|---|
| 다 | CONTRAST | differs from or opposes the target |
| 대 | CONCEDE | holds even though the target holds |
| 댜 | RESULT | is a consequence of the target |
| 더 | EVIDENCE | is my ground for believing the target |
| 데 | EXPLAIN | says why the target is so |
| 뎌 | ADD | a further point alongside the target |
| 도 | SEQUENCE | the next event after the target |
| 됴 | EXAMPLE | an instance of the target |
| 두 | DETAIL | spells out part of the target |
| 듀 | RESTATE | says the target again in other words; sums up |
| 드 | BACKGROUND | sets the scene for the target |
| 디 | ASIDE | off the main line |
| 따 | UNDER | holds only inside the supposition made in the target |
| 때 | ANSWER | answers the question in the target |
| 땨 | REBUT | denies the target, or something the reader is presumed to think |
| 떠 | RETRACT | withdraws or replaces the target: I no longer hold it |

### Strength: how sure the writer is

| Form | Name | Meaning |
|---|---|---|
| 바 | CERTAIN | I am sure |
| 배 | LIKELY | probably |
| 뱌 | POSSIBLE | maybe |

### Attitude

| Form | Name | Meaning |
|---|---|---|
| 빠 | SURPRISE | unexpected to me |
| 빼 | EMPHASIS | stressed |
| 뺘 | POLITE | politely |
| 뻐 | REGRET | I am sorry that |
| 뻬 | GLAD | I am glad that |
| 뼈 | ANNOYED | irritated |
| 뽀 | JEST | said playfully |
| 뾰 | IRONY | meant otherwise than the literal words |
| 뿌 | FRANK | speaking bluntly |
| 쀼 | HOPE | I hope that |
| 쁘 | FEAR | I fear that |

### Negation and time

| Form | Name | Meaning |
|---|---|---|
| 하 | NOT | negates everything to its right in its group |
| 해 | PAST | before the reference time |
| 햐 | FUTURE | after the reference time |
| 허 | NOW | at present (use only to contrast with another time); also a head: "now" |
| 헤 | UNREAL | in a supposed world, not the actual one ("would", "were") |
| 혀 | NEAR | after PAST or FUTURE: just now / soon |
| 호 | FAR | after PAST or FUTURE: long ago / far ahead |

### Modals

| Form | Name | Meaning |
|---|---|---|
| 카 | MUST | required |
| 캐 | SHOULD | advised |
| 캬 | MAY | permitted |
| 커 | CAN | able, or possible in fact |
| 케 | WANT | the AGENT wants to |
| 켜 | TRY | the AGENT tries to |

### Aspect: how the event unfolds

| Form | Name | Meaning |
|---|---|---|
| 자 | ONGOING | in progress |
| 재 | DONE | finished and the result holds |
| 쟈 | HABIT | as a habit or regular practice |
| 저 | BEGIN | starts; with a state: becomes |
| 제 | STOP | ceases |
| 져 | STILL | continues |
| 조 | AGAIN | once more |
| 죠 | ALREADY | by now (NOT ALREADY = not yet) |
| 주 | FINALLY | after a long wait |
| 쥬 | OFTEN | often |
| 즈 | RARE | rarely |
| 지 | SOMETIMES | sometimes |
| 짜 | ALWAYS | always |
| 째 | NEVER | never |
| 쨔 | TIMES | counts occurrences; a number or amount word comes before it: 3 TIMES, MANY TIMES |

### Degree

| Form | Name | Meaning |
|---|---|---|
| 타 | VERY | very |
| 태 | SLIGHT | somewhat |
| 탸 | FULL | completely |
| 터 | BARELY | hardly |
| 테 | ALMOST | almost |
| 텨 | ENOUGH | enough (FOR ...) |
| 토 | TOO | too (FOR ...) |
| 툐 | MORE | more (THAN ...) |
| 투 | LESS | less (THAN ...) |
| 튜 | MOST | most (THAN the set compared) |
| 트 | LEAST | least |
| 티 | EQUAL | as ... as (THAN ...); alone as predicate: is identical to |

### Focus

| Form | Name | Meaning |
|---|---|---|
| 파 | ONLY | only |
| 패 | ALSO | also |
| 퍄 | EVEN | even |
| 퍼 | INSTEAD | instead |
| 페 | MAINLY | mostly, especially |
| 펴 | FOCUS | this one, not another (contrastive stress; "itself") |
| 포 | TOPIC | what the sentence is about |

### Values

| Form | Name | Meaning |
|---|---|---|
| 표 | YES | yes; true |
| 푸 | NO | no; false |
| 퓨 | EMPTY | nothing; the empty value |

### Roles: each stands before its phrase

| Form | Name | Meaning |
|---|---|---|
| 사 | AGENT | who controls the act or brings it about; who knows, sees, wants or has |
| 새 | THEME | what is acted on, perceived or described; what a thing happens to |
| 샤 | TO | recipient, end point, or resulting state |
| 서 | FROM | origin |
| 세 | AT | place |
| 셔 | WHEN | point in time |
| 소 | WITH | means or manner |
| 쇼 | CAUSE | cause or reason |
| 수 | FOR | purpose or beneficiary |
| 슈 | THAN | standard of comparison; with no degree word: "like". A role particle may follow to say which participant is compared |
| 스 | ABOUT | topic, field or respect |
| 시 | AS | capacity, role or viewpoint |
| 싸 | ALONG | companion |
| 쌔 | SPAN | duration, extent, or size of a difference |
| 쌰 | EXCEPT | what the statement does not cover (with a block: unless) |
| 써 | DESPITE | what would have been expected to prevent it (with a block: although) |
| 쎄 | VIA | path or thing passed through |
| 쎠 | PER | for each one of: 3 tries PER request |
| 쏘 | SWAP | what is replaced or given in exchange (instead of; price paid) |

### Linkers: attach a modifier to the word before

| Form | Name | Meaning |
|---|---|---|
| 라 | KIND | narrows the head: type, material, content, quality. After a predicate: manner |
| 래 | OF | owner, or the whole a part belongs to |
| 랴 | REL | the second thing a relational root needs: before REL x, cause REL x, friend REL x |
| 러 | NOTE | adds a comment that does not narrow; with a phrase: "namely" (the full list) |
| 레 | HAVING | what the head has (the reverse of OF): function HAVING 2 parameter |
| 려 | SUCHAS | examples, not a full list |

### Joiners

| Form | Name | Meaning |
|---|---|---|
| 로 | AND | joins phrases: and |
| 료 | OR | joins phrases: or (one or both) |
| 루 | XOR | joins phrases: exactly one of |
| 류 | ANDC | joins clauses: and. A relation may follow it |
| 르 | ORC | joins clauses: or |
| 리 | BUT | joins clauses: but |

### Structure words

| Form | Name | Meaning |
|---|---|---|
| 차 | NAMED | binds the handle that follows to this thing |
| 채 | BY | whose words this sentence or block is |
| 챠 | CALL | in the header: names the person addressed |
| 처 | NAME | the next word is a proper name |
| 체 | BE | in DEFINE: separates term and meaning. As a predicate: empty "is" for role phrases |
| 쳐 | IF | IF {condition} {then} {else} |
| 초 | EACH | EACH handle IN phrase {block}: for each |
| 쵸 | IN | see EACH |
| 추 | WHILE | WHILE {condition} {block} |
| 츄 | RETURN | gives back a value (logic) |
| 츠 | STEP | refers to a numbered sentence: STEP 3 |
| 치 | UPTO | range between two numbers or labels: 3 UPTO 5 |

### Amount and reference words: before the head

| Form | Name | Meaning |
|---|---|---|
| 마 | ALL | every one |
| 매 | MAJOR | most of |
| 먀 | MANY | many; much |
| 머 | SEVERAL | more than one |
| 메 | SOME | at least one; some |
| 며 | FEW | few; little |
| 모 | NONE | no; none |
| 묘 | ANY | whichever (no existence implied) |
| 무 | GENERIC | the kind in general (exceptions allowed) |
| 뮤 | WHOLE | the set taken together, not each member |
| 므 | THAT | the one the reader can identify |
| 미 | THIS | the one present or just pointed at |
| 나 | OTHER | a different one |
| 내 | SAME | the same one |
| 냐 | SPECIFIC | a particular one I have in mind |
| 너 | ORD | ORD 3 = the third |

### Number modifiers

| Form | Name | Meaning |
|---|---|---|
| 네 | AROUND | about, roughly (before a number or a quality) |
| 녀 | EXACT | exactly |
| 노 | ATLEAST | at least |
| 뇨 | ATMOST | at most |
| 누 | ABOVE | more than (a number) |
| 뉴 | BELOW | fewer than (a number) |

### Person and question words, logic slots

| Form | Name | Meaning |
|---|---|---|
| 아 | ME | the writer (inside a BY block: that speaker) |
| 애 | YOU | the addressee |
| 야 | US | the writer's group, without the addressee |
| 어 | SELF | in a modifying block: the head. Elsewhere: the AGENT of its own clause |
| 에 | MUTUAL | each other |
| 여 | WHAT | question word. Before a head: which. WHAT MANY: how many. Before a quality: how |
| 오 | FIRST | first slot of a logic function |
| 요 | SECOND | second slot |
| 우 | THIRD | third slot |
| 유 | FOURTH | fourth slot |

## 10. Logic

Logic uses the same clause with numbered slots in place of roles, so it can be turned into code.

```
( function FIRST x SECOND y )        a function call; EQUAL, MORE, LESS and roots such as add, multiply, remainder
DEFINE name FIRST h1 SECOND h2 BE { statement . statement . }      a function
DEFINE handle BE expression          assignment
IF { condition } { then } { else }   EACH h IN expression { ... }   WHILE { condition } { ... }   RETURN expression
```

`DEFINE ( phrase ) BE «identifier»` gives the code name of a native term. Library and API names stay in `« »`.

```
까 ( 리랄엄 라 치팟 ) 체 «sum_even» .
    DEFINE ( add.made KIND even ) BE «sum_even» .
    = [definition] “even sum” means sum_even.

까 ( 리랄엄 라 치팟 ) 오 각 체 { 까 낙 체 0 . 초 닥 쵸 각 { 쳐 { 티 오 ( 자칵 오 닥 요 2 ) 요 0 } { 까 낙 체 ( 리랄 오 낙 요 닥 ) } } . 츄 낙 } .
    DEFINE ( add.made KIND even ) FIRST L BE { DEFINE T BE 0 . EACH X IN L { IF { EQUAL FIRST ( remainder FIRST X SECOND 2 ) SECOND 0 } { DEFINE T BE ( add FIRST T SECOND X ) } } . RETURN T } .
    = [definition] Even sum(L) is defined as: let T be 0; for each X in L: if it is equal to remainder(X, 2) 0, then let T be add(T, X); return T.
```

## 11. Checklist before you finish a sentence

- It starts with an opener and ends with ` .`
- The predicate comes before its participants, and every participant has a role particle.
- Every root is in the word list (or is root + suffix, or a defined spare). Every particle is in section 9.
- No pronouns: handles, THAT + root, or the noun again.
- Nothing left out that the reader needs: a missing role means "unstated".
- Latin letters only inside `« »`.
