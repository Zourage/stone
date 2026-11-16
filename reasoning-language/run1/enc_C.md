# Encodings, passage set C (spec 0.1, gloss notation)

Labels restart in each passage. Notes in square brackets are mine, not part of the language.

## D03

**A HARE one day ridiculed the short feet and slow pace of the Tortoise, who replied, laughing: "Though you be swift as the wind, I will beat you in a race."**

```
1: GIVEN PAST ridicule AGENT hare NAMED H THEME foot KIND short OF (tortoise NAMED T) WHEN SOME day .
2: GIVEN ADD PAST ridicule AGENT H THEME pace KIND slow OF T .
3: GIVEN SEQUENCE PAST reply AGENT T TO H WITH laugh THEME { IF { equal THEME swiftness OF YOU TO swiftness OF wind } { FUTURE win AGENT ME FROM YOU AT race } } .
```
[No coordination, so "feet and pace" is two sentences. "Though" inside the quote has no home (relations are sentence-level), so it became a plain IF. YOU/ME inside the block are meant as the quoted speaker's, which the spec does not license.]

**The Hare, believing her assertion to be simply impossible, assented to the proposal; and they agreed that the Fox should choose the course and fix the goal.**

```
4: GIVEN PAST believe AGENT H THEME { NOT possible THEME { FUTURE win AGENT T FROM H AT race } } .
5: GIVEN RESULT PAST assent AGENT H TO proposal OF T .
6: DEFINE P BE pair KIND { contain AGENT SELF THEME H } KIND { contain AGENT SELF THEME T } .
7: GIVEN ADD 5 PAST agree AGENT P THEME { FUTURE choose AGENT (fox NAMED F) THEME course } .
8: GIVEN ADD PAST agree AGENT P THEME { FUTURE fix AGENT F THEME goal } .
```

**On the day appointed for the race the two started together.**

```
9: GIVEN SEQUENCE PAST start AGENT P WITH together WHEN day KIND { PAST appoint THEME SELF FOR race } .
```

**The Tortoise never for a moment stopped, but went on with a slow but steady pace straight to the end of the course.**

```
10: GIVEN SEQUENCE PAST stop AGENT T WHEN NO moment .
11: GIVEN CONTRAST PAST ONGOING go AGENT T TO end OF course WITH pace KIND slow KIND steady WITH straight .
```

**The Hare, lying down by the wayside, fell fast asleep.**

```
12: GIVEN CONTRAST PAST lie AGENT H AT side OF way .
13: GIVEN SEQUENCE PAST begin THEME { sleep AGENT H WITH deep } .
```

**At last waking up, and moving as fast as he could, he saw the Tortoise had reached the goal, and was comfortably dozing after her fatigue.**

```
14: GIVEN SEQUENCE PAST wake AGENT H WHEN late .
15: GIVEN SEQUENCE PAST move AGENT H WITH speed KIND greatest KIND { able AGENT H THEME SELF } .
16: GIVEN SEQUENCE PAST see AGENT H THEME { PAST DONE reach AGENT T THEME goal } .
17: GIVEN ADD PAST see AGENT H THEME { PAST ONGOING doze AGENT T WITH comfort CAUSE fatigue OF T } .
```

**Slow but steady wins the race.**

```
18: DERIVED 10 11 16 HABIT win AGENT one KIND slow KIND steady THEME race .
```

## D07

**LAWYER, n. One skilled in circumvention of the law.**

```
1: GIVEN noun THEME «LAWYER» .
2: DEFINE «LAWYER» BE person KIND { skilled THEME SELF FOR { circumvent THEME law } } .
```

**BORE, n. A person who talks when you wish him to listen.**

```
3: GIVEN noun THEME «BORE» .
4: DEFINE «BORE» BE person KIND { HABIT talk AGENT SELF WHEN { wish AGENT YOU THEME { listen AGENT SELF } } } .
```
[The inner SELF is meant as the same person; the spec does not say which head SELF picks in a nested clause.]

**BOTANY, n. The science of vegetables--those that are not good to eat, as well as those that are.**

```
5: GIVEN noun THEME «BOTANY» .
6: DEFINE «BOTANY» BE science KIND vegetable .
7: GIVEN RESTATE study AGENT «BOTANY» THEME ALSO vegetable KIND { NOT good THEME SELF FOR eat } .
8: GIVEN ADD study AGENT «BOTANY» THEME vegetable KIND { good THEME SELF FOR eat } .
```

**It deals largely with their flowers, which are commonly badly designed, inartistic in color, and ill-smelling.**

```
9: GIVEN study AGENT «BOTANY» THEME flower OF vegetable NAMED F WITH part KIND large .
10: GIVEN BACKGROUND HABIT design THEME F WITH bad .
11: GIVEN ADD NOT HABIT artistic THEME color OF F .
12: GIVEN ADD HABIT smell THEME F WITH bad .
```

## D11

**3. SHOULD This word, or the adjective "RECOMMENDED", mean that there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course.**

```
1: DEFINE «SHOULD» BE { possible THEME { exist THEME SOME reason KIND valid FOR { ignore THEME item NAMED I } AT SOME circumstance } } .
2: GIVEN CONTRAST require THEME { DONE understand THEME ALL implication OF { ignore THEME I } } WHEN { NOT DONE choose THEME course KIND different } .
3: GIVEN ADD require THEME { DONE weigh THEME ALL implication OF { ignore THEME I } WITH care } WHEN { NOT DONE choose THEME course KIND different } .
4: DEFINE «RECOMMENDED» BE «SHOULD» .
5: GIVEN adjective THEME «RECOMMENDED» .
```
[Sentences 2 and 3 are part of the definition in the source; here they sit outside the DEFINE.]

**4. SHOULD NOT This phrase, or the phrase "NOT RECOMMENDED" mean that there may exist valid reasons in particular circumstances when the particular behavior is acceptable or even useful, but the full implications should be understood and the case carefully weighed before implementing any behavior described with this label.**

```
6: DEFINE «SHOULD NOT» BE { possible THEME { exist THEME SOME reason KIND valid AT SOME circumstance FOR { OR { acceptable THEME behavior NAMED B } { useful THEME B } } } } .
7: GIVEN CONTRAST recommend THEME { DONE understand THEME ALL implication OF B } WHEN { NOT DONE implement THEME ALL behavior KIND { describe THEME SELF WITH label KIND «SHOULD NOT» } } .
8: GIVEN ADD recommend THEME { DONE weigh THEME case WITH care } WHEN { NOT DONE implement THEME ALL behavior KIND { describe THEME SELF WITH label KIND «SHOULD NOT» } } .
9: DEFINE «NOT RECOMMENDED» BE «SHOULD NOT» .
```

**5. MAY This word, or the adjective "OPTIONAL", mean that an item is truly optional.**

```
10: DEFINE «MAY» BE { optional THEME item NAMED J WITH true } .
11: DEFINE «OPTIONAL» BE «MAY» .
12: GIVEN adjective THEME «OPTIONAL» .
```

**One vendor may choose to include the item because a particular marketplace requires it or because the vendor feels that it enhances the product while another vendor may omit the same item.**

```
13: GIVEN EXAMPLE 10 POSSIBLE OR { choose AGENT (vendor NAMED V) THEME { include AGENT V THEME J } CAUSE { require AGENT SOME market THEME J } } { choose AGENT V THEME { include AGENT V THEME J } CAUSE { feel AGENT V THEME { enhance AGENT J THEME product } } } .
14: GIVEN CONTRAST POSSIBLE omit AGENT vendor KIND other THEME J .
```

## D15

**We prove a conjecture by J. Zhao which states that every finite multiple zeta value associated with a nonempty index is a Q-linear combination of ζ_A(k_1,…,k_r,2,1), where k_i ∈ {2,3}.**

```
1: GIVEN prove AGENT ME THEME conjecture OF name«J. Zhao» NAMED C .
2: GIVEN BACKGROUND state AGENT C THEME { equal THEME ALL value KIND (zeta KIND multiple KIND finite) KIND { associate THEME SELF WITH index KIND { NOT empty THEME SELF } } TO SOME combination KIND (linear KIND «\mathbb{Q}») OF («\zeta_{\mathcal{A}}(k_1,\dots,k_r,2,1)» KIND { satisfy AGENT SELF THEME «k_i\in\{2,3\}» }) } .
```

**Our proof proceeds by constructing a basis for the space of formal multiple zeta values defined by the confluence relations.**

```
3: GIVEN proceed THEME proof OF ME WITH { construct AGENT ME THEME basis OF (space KIND (value KIND formal KIND (zeta KIND multiple)) KIND { define AGENT relation KIND confluence THEME SELF }) } .
```

**This approach also reduces the Kaneko--Zagier conjecture (apart from compatibility with the depth filtration) to linear independence conjectures for ordinary and finite multiple zeta values, without using motivic theory.**

```
4: GIVEN ADD reduce AGENT approach OF STEP 3 THEME (conjecture KIND name«Kaneko--Zagier» NAMED K) TO SOME conjecture KIND (independence KIND linear) KIND { concern AGENT SELF THEME value KIND ordinary KIND (zeta KIND multiple) } TO SOME conjecture KIND (independence KIND linear) KIND { concern AGENT SELF THEME value KIND finite KIND (zeta KIND multiple) } WITH NO theory KIND motivic .
5: GIVEN CONTRAST 4 NOT reduce AGENT approach OF STEP 3 THEME part OF K KIND { concern AGENT SELF THEME { compatible THEME K WITH filtration KIND depth } } .
```
[Two TO phrases stand in for "ordinary and finite"; the spec does not say what a repeated role means.]

## D19

**Recent indicators suggest that economic activity has continued to expand at a solid pace.**

```
1: GIVEN suggest AGENT indicator KIND recent THEME { ONGOING expand THEME activity KIND economy WITH pace KIND solid } .
```

**Job gains have slowed, and the unemployment rate has moved up but remains low.**

```
2: GIVEN DONE slow THEME gain KIND job .
3: GIVEN ADD DONE rise THEME rate KIND unemployment NAMED U .
4: GIVEN CONTRAST ONGOING low THEME U .
```

**Inflation has made further progress toward the Committee's 2 percent objective but remains somewhat elevated.**

```
5: GIVEN DONE progress THEME inflation NAMED N TO objective KIND (2 «percent») OF (committee NAMED C) WITH amount KIND additional .
6: GIVEN CONTRAST ONGOING high THEME N .
```

**The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run.**

```
7: GIVEN seek AGENT C THEME { achieve AGENT C THEME employment KIND maximum } WHEN run KIND long .
8: GIVEN ADD seek AGENT C THEME { equal THEME rate OF N TO 2 «percent» } WHEN run KIND long .
```

**The Committee has gained greater confidence that inflation is moving sustainably toward 2 percent, and judges that the risks to achieving its employment and inflation goals are roughly in balance.**

```
9: GIVEN DONE increase THEME { confident AGENT C THEME { ONGOING move THEME N TO 2 «percent» WITH sustain } } .
10: GIVEN ADD judge AGENT C THEME { balance THEME ALL risk KIND { threaten AGENT SELF THEME goal OF C } } .
```

**The economic outlook is uncertain, and the Committee is attentive to the risks to both sides of its dual mandate.**

```
11: GIVEN uncertain THEME outlook KIND economy .
12: GIVEN ADD attentive AGENT C TO risk KIND { threaten AGENT SELF THEME ALL side OF (mandate KIND dual OF C) } .
```

**In light of the progress on inflation and the balance of risks, the Committee decided to lower the target range for the federal funds rate by 1/2 percentage point to 4-3/4 to 5 percent.**

```
13: GIVEN RESULT PAST decide AGENT C THEME { lower AGENT C THEME range KIND target OF (rate KIND (fund KIND federal)) WITH amount KIND («1/2» point KIND percentage) TO range KIND { span AGENT SELF FROM «4-3/4 percent» TO «5 percent» } } CAUSE STEP 5 CAUSE STEP 10 .
```

## D23

[The language has no way to mark whose turn a sentence is. Speaker letters below are outside the notation; ME and YOU swap silently at each turn.]

**A: hey, did the deploy go out?**

```
1: ASK PAST DONE release THEME deploy NAMED D .
```

**B: nope, still stuck on the migration**

```
2: GIVEN NO .
3: GIVEN ONGOING stick THEME D AT migration NAMED M .
```

**A: ugh. again?? thought we fixed that last week**

```
4: ASK SURPRISE repeat THEME STEP 3 .
5: GIVEN CONTRAST PAST think AGENT ME THEME { PAST DONE fix AGENT ME WITH YOU THEME problem KIND migration WHEN week KIND last } .
```

**B: we fixed *a* migration lol. this one's new**

```
6: GIVEN CONCEDE PAST fix AGENT ME WITH YOU THEME 1 migration KIND { NOT same THEME SELF WITH M } .
7: GIVEN CONTRAST new THEME M .
```

**A: ok. need a hand or should I leave you to it**

```
8: GIVEN YES .
9: ASK OR { need AGENT YOU THEME help } { leave AGENT ME THEME YOU WITH alone } .
```

**B: nah I'm good, give me like 20 min. will ping you if it blows up**

```
10: GIVEN NO .
11: GIVEN fine THEME ME .
12: REQUEST give AGENT YOU TO ME THEME 20 minute .
13: PLAN IF { fail THEME M WITH bad } { ping AGENT ME THEME YOU } .
```

**A: cool, thanks. no rush btw**

```
14: GIVEN YES .
15: GIVEN POLITE thank AGENT ME TO YOU .
16: GIVEN ADD NOT need THEME hurry .
```
