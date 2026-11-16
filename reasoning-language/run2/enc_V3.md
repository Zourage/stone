# Encodings V3 (spec 0.2, gloss notation)

Handles are declared with NAMED at first use. Notes in [square brackets] are mine, not part of the encoding.

## D01

**It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife.**

```
1: CLAIM IRONY acknowledge AGENT ALL person AS truth THEME { MUST want AGENT GENERIC man KIND NOT married KIND { own AGENT SELF THEME fortune KIND good } THEME wife } NAMED T .
```
[MUST is "required"; the source "must" is inferential. IRONY covers the whole sentence.]

**However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters.**

```
2: CLAIM IRONY DETAIL 1 VERY fixed THEME T AT mind OF ALL family KIND (around REL neighbourhood KIND { enter AGENT M THEME SELF })
   DESPITE { BARELY know THEME (feeling OR view) OF ANY man KIND (THAT kind) NAMED M WHEN (ORD 1 time KIND { enter AGENT M THEME neighbourhood }) } .
3: CLAIM IRONY RESULT 2 EACH F IN ALL family KIND THAT { consider AGENT F THEME M AS property KIND rightful OF SOME 1 daughter OF F } .
```
["so ... that" split into VERY + a RESULT sentence. M is used in 3 although the spec says a variable bound on a quantified phrase lasts one sentence. "family KIND THAT" is a stretch for "those families".]

**"My dear Mr. Bennet," said his lady to him one day, "have you heard that Netherfield Park is let at last?"**

```
4: STORY PAST say AGENT (wife OF B) NAMED W TO name«Mr. Bennet» NAMED B WHEN SOME day
   THEME { BY W ASK CALL (name«Mr. Bennet» KIND dear OF ME) DONE hear AGENT YOU THEME { FINALLY DONE let THEME name«Netherfield Park» NAMED N } NAMED E } .
```

**Mr. Bennet replied that he had not.**

```
5: STORY SEQUENCE PAST reply AGENT B THEME { NOT PAST hear AGENT B THEME E } .
```
[Indirect speech written as a bare block without BY; the spec does not say this is the convention.]

**"But it is," returned she; "for Mrs. Long has just been here, and she told me all about it."**

```
6: STORY SEQUENCE PAST reply AGENT W THEME (
     { BY W CLAIM CONTRAST EMPHASIS DONE let THEME N }
     AND { BY W GIVEN EVIDENCE PAST NEAR visit AGENT name«Mrs. Long» NAMED L AT THIS place AND PAST tell AGENT L TO ME THEME ALL detail ABOUT E } ) .
```
[The EVIDENCE relation inside the second block has no label to point at; by the default rule it would target sentence 5, not the first block.]

**Mr. Bennet made no answer.**

```
7: STORY SEQUENCE NOT PAST answer AGENT B .
```

**"Do not you want to know who has taken it?" cried his wife, impatiently.**

```
8: STORY SEQUENCE PAST cry AGENT W WITH impatience
   THEME { BY W ASK LIKELY ANNOYED want AGENT YOU THEME { know AGENT YOU THEME { ASK DONE take AGENT WHAT THEME N } } } .
```
[ASK LIKELY: I intend "expects yes"; the spec gives strength no polarity.]

**"_You_ want to tell me, and I have no objection to hearing it."**

```
BY B 9: CLAIM ANSWER 8 JEST want AGENT FOCUS YOU THEME { tell AGENT YOU TO ME THEME THAT news } AND NOT object AGENT ME THEME { hear AGENT ME THEME THAT news } .
```

## D09

**No Person shall be a Representative who shall not have attained to the Age of twenty five Years, and been seven Years a citizen of the United States, and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen.**

```
1: CLAIM MUST NOT (representative) THEME ANY person KIND {
     NOT DONE reach AGENT P THEME age KIND (25 year)
     OR NOT DONE (citizen OF name«United States») THEME P SPAN 7 year
     OR NOT (inhabitant OF state KIND { choose THEME P AT SELF }) THEME P WHEN { elect THEME P } } NAMED P .
```
[CLAIM is the nearest opener; the source enacts a rule rather than asserting one. The source says "not (A and B), and not C"; NOT cannot scope over joined clauses, so I wrote the intended "not A or not B or not C".]

## D11

**3. SHOULD This word, or the adjective "RECOMMENDED", mean that there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course.**

```
3: DEFINE «SHOULD» OR (adjective NOTE «RECOMMENDED») BE {
     MUST (understand AND (weigh KIND careful)) THEME ALL implication WHEN before REL { choose THEME OTHER course }
     DESPITE { CAN exist THEME reason KIND valid FOR { ignore THEME SOME 1 item } AT SOME circumstance } } .
```
[Clause-level "but" does not exist inside a block; DESPITE swaps which half is the main point.]

**4. SHOULD NOT This phrase, or the phrase "NOT RECOMMENDED" mean that there may exist valid reasons in particular circumstances when the particular behavior is acceptable or even useful, but the full implications should be understood and the case carefully weighed before implementing any behavior described with this label.**

```
4: DEFINE «SHOULD NOT» OR (phrase NOTE «NOT RECOMMENDED») BE {
     SHOULD understand THEME ALL implication WHEN before REL { implement THEME ANY behaviour KIND { describe THEME SELF WITH THIS label } }
     AND SHOULD weigh THEME case WITH care WHEN before REL { implement THEME ANY behaviour KIND { describe THEME SELF WITH THIS label } }
     DESPITE { CAN exist THEME reason KIND valid AT SOME circumstance KIND { (acceptable OR EVEN useful) THEME THAT behaviour AT SELF } } } .
```
[The "before" adjunct and the DESPITE block have to be repeated or left attached to one clause only; here DESPITE attaches only to the second clause.]

**5. MAY This word, or the adjective "OPTIONAL", mean that an item is truly optional.**

```
5: DEFINE «MAY» OR (adjective NOTE «OPTIONAL») BE { FULL optional THEME item } .
```

**One vendor may choose to include the item because a particular marketplace requires it or because the vendor feels that it enhances the product while another vendor may omit the same item.**

```
6: CLAIM EXAMPLE 5 CAN choose AGENT 1 vendor NAMED V THEME { include AGENT V THEME THAT item }
   CAUSE ({ require AGENT SOME 1 marketplace THEME THAT item } OR { believe AGENT V THEME { improve AGENT THAT item THEME product } }) .
7: CLAIM CONTRAST 6 CAN omit AGENT OTHER vendor THEME THAT item .
```

## D17

**I was hopeful, and I've tried to just see if this long thread results in anything constructive, but this seems to be going backwards (or at least not forwards).**

```
1: CLAIM PAST hopeful THEME ME AND DONE try AGENT ME THEME { ONLY watch AGENT ME THEME { ASK produce AGENT THIS thread KIND long THEME ANY thing KIND constructive } } .
2: CLAIM CONTRAST 1 ANNOYED seem THEME { ONGOING move THEME THIS thread TO (LIKELY backward OR CERTAIN NOT forward) } .
```
["or at least" approximated by scoping strength to each alternative.]

**The fact is, the pull request you objected to DID NOT TOUCH THE DMA LAYER AT ALL.**

```
3: CLAIM CONTRAST CERTAIN EMPHASIS NOT PAST EVEN SLIGHT touch AGENT (request KIND pull KIND { PAST object AGENT YOU ABOUT SELF }) NAMED R THEME layer KIND «DMA» NAMED D .
```

**It was literally just another user of it, in a completely separate subdirectory, that didn't change the code you maintain in _any_ way, shape, or form.**

```
4: CLAIM DETAIL 3 EMPHASIS PAST (ONLY ALSO 1 user OF D KIND (inside REL subdirectory KIND (FULL separate)) KIND { NOT PAST change AGENT U THEME code KIND { maintain AGENT YOU THEME SELF } WITH FOCUS ANY way } NAMED U) THEME R .
```

**I find it distressing that you are complaining about new users of your code, and then you keep bringing up these kinds of complete garbage arguments.**

```
5: CLAIM ANNOYED distressing AS ME THEME { ONGOING complain AGENT YOU ABOUT user KIND new OF code OF YOU AND OFTEN AGAIN raise AGENT YOU THEME argument KIND (THIS kind) KIND (FULL garbage) } .
```

**Honestly, what you have been doing is basically saying "as a DMA maintainer I control what the DMA code is used for".**

```
6: CLAIM RESTATE 5 EMPHASIS ALMOST (same THAN { say AGENT YOU THEME { BY YOU CLAIM control AGENT ME AS maintainer OF D THEME { ASK use THEME code KIND «DMA» FOR WHAT } } }) THEME (act KIND { DONE ONGOING do AGENT YOU THEME SELF }) .
```
[THAN inside a parenthesised predicate is not licensed by the grammar; I know no licensed way to say "amounts to saying". The BY YOU block reads as a real quotation, which it is not.]

**And that is not how *any* of this works.**

```
7: CLAIM CONTRAST 6 EMPHASIS NOT work THEME FOCUS ANY part OF THIS matter WITH THAT way .
```

## D19

**Recent indicators suggest that economic activity has continued to expand at a solid pace.**

```
1: CLAIM suggest AGENT indicator KIND recent THEME { DONE STILL expand THEME activity KIND economic WITH pace KIND solid } .
```

**Job gains have slowed, and the unemployment rate has moved up but remains low.**

```
2: CLAIM DONE slow THEME gain KIND job .
3: CLAIM ADD DONE rise THEME rate KIND unemployment NAMED U .
4: CLAIM CONCEDE 3 STILL low THEME U .
```

**Inflation has made further progress toward the Committee's 2 percent objective but remains somewhat elevated.**

```
5: CLAIM DONE MORE progress THEME inflation NAMED I TO objective KIND «2 percent» OF committee NAMED C .
6: CLAIM CONCEDE 5 STILL SLIGHT high THEME I .
```

**The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run.**

```
7: CLAIM seek AGENT C THEME { achieve AGENT C THEME ((employment KIND maximum) AND (I KIND (rate KIND «2 percent»))) SPAN run KIND (MORE long) } .
```

**The Committee has gained greater confidence that inflation is moving sustainably toward 2 percent, and judges that the risks to achieving its employment and inflation goals are roughly in balance.**

```
8: CLAIM DONE BEGIN MORE confident THEME C ABOUT { ONGOING move THEME I TO «2 percent» WITH way KIND sustainable }
   AND judge AGENT C THEME { ALMOST balanced THEME risk REL { achieve AGENT C THEME goal OF C KIND (employment AND inflation) } NAMED K } .
```
[ALMOST stands in for "roughly"; it wrongly implies falling short.]

**The economic outlook is uncertain, and the Committee is attentive to the risks to both sides of its dual mandate.**

```
9: CLAIM uncertain THEME outlook KIND economic AND attentive THEME C TO risk REL (ALL 2 side OF mandate KIND dual OF C) .
```

**In light of the progress on inflation and the balance of risks, the Committee decided to lower the target range for the federal funds rate by 1/2 percentage point to 4-3/4 to 5 percent.**

```
10: CLAIM PAST decide AGENT C CAUSE (STEP 5 AND STEP 8)
    THEME { lower AGENT C THEME range KIND target OF rate KIND (fund KIND federal) SPAN «1/2 percentage point» TO «4-3/4 to 5 percent» } .
```

## D20

**A deep upper low in the NE Pacific dives southwards well offshore on Wednesday.**

```
1: CLAIM FUTURE dive THEME low KIND deep KIND upper KIND (inside REL (northeast OF name«Pacific»)) NAMED S TO south AT offshore KIND (VERY far) WHEN wednesday .
```

**The bulk of the energy associated with this system will be focused south of western Washington as the system moves onshore into California on Thursday.**

```
2: CLAIM FUTURE focus THEME MAJOR energy KIND { associate THEME SELF ALONG S } AT south REL (west OF name«Washington»)
   WHEN during REL { move THEME S FROM offshore TO (inside REL name«California») WHEN thursday } .
```

**Precipitation spreads northwards into Washington on Wednesday, however, POPs mainly remain confined south of Seattle, and especially south of WA/OR border due to the trajectory of the system.**

```
3: CLAIM FUTURE spread THEME precipitation VIA north TO (inside REL name«Washington») WHEN wednesday .
4: CLAIM CONTRAST 3 FUTURE STILL confine THEME «POPs» AT (MAINLY south REL name«Seattle» AND MAINLY south REL border REL (name«Washington» AND name«Oregon»)) CAUSE trajectory OF S .
```
[Both "mainly" and "especially" become MAINLY; the grading between them is gone.]

**Easterly winds increase in the Cascade Valleys and gaps early Wednesday for breezy conditions, with NBM probabilities of gusts over 30 MPH in areas around North Bend and Enumclaw around 30-60%.**

```
5: CLAIM FUTURE increase THEME wind KIND (from REL east) AT (valley AND gap) OF name«Cascade» WHEN early OF wednesday .
6: CLAIM RESULT 5 FUTURE breezy THEME condition .
7: GIVEN DETAIL 6 (AROUND 30 UPTO 60 percent) THEME probability KIND «NBM» OF { exist THEME gust KIND { MORE fast THEME SELF THAN «30 MPH» } AT area KIND (around REL (name«North Bend» AND name«Enumclaw»)) } .
```

**Drier conditions by Thursday into Friday.**

```
8: CLAIM SEQUENCE FUTURE BEGIN MORE dry THEME condition WHEN (NOT after REL thursday) SPAN (until REL (SOME part OF friday)) .
```

**Periods of clearing may result in fog development, mainly Friday AM.**

```
9: CLAIM POSSIBLE FUTURE cause AGENT period KIND clearing THEME { develop THEME fog } WHEN MAINLY morning OF friday .
```

**Ensembles suggest troughing deepens again offshore Saturday into next week, with some uncertainty into the exact positioning and depth of the trough.**

```
10: GIVEN suggest AGENT ensemble THEME { FUTURE AGAIN deepen THEME trough NAMED G AT offshore WHEN saturday SPAN (until REL (SOME part OF week KIND next)) } .
11: CLAIM ADD 10 SLIGHT uncertain THEME ((position KIND exact) AND depth) OF G .
```

**Highs remain near normal during this period in upper 40s to low 50s.**

```
12: CLAIM FUTURE STILL (near REL normal) THEME temperature KIND (MOST high) KIND daily NOTE «upper 40s to low 50s» SPAN THIS period .
```

## D23

**A: hey, did the deploy go out?**

```
BY A 1: SOCIAL greet .
BY A 2: ASK DONE release THEME THAT deploy NAMED D .
```

**B: nope, still stuck on the migration**

```
BY B 3: GIVEN ANSWER 2 NO .
BY B 4: GIVEN DETAIL 3 STILL stuck THEME D AT migration .
```

**A: ugh. again?? thought we fixed that last week**

```
BY A 5: SOCIAL ANNOYED dismay .
BY A 6: ASK SURPRISE ANNOYED AGAIN stuck THEME D AT migration .
BY A 7: CLAIM EXPLAIN 6 PAST believe AGENT ME THEME { PAST fix AGENT US THEME THAT problem WHEN week KIND previous } .
```

**B: we fixed *a* migration lol. this one's new**

```
BY B 8: CLAIM CONTRAST 7 JEST PAST fix AGENT US THEME FOCUS SOME 1 migration .
BY B 9: CLAIM DETAIL 8 new THEME THIS migration .
```

**A: ok. need a hand or should I leave you to it**

```
BY A 10: SOCIAL ok .
BY A 11: ASK need AGENT YOU THEME help OR SHOULD leave AGENT ME THEME YOU ALONG THAT task .
```
[Reads equally as a yes/no question over the disjunction.]

**B: nah I'm good, give me like 20 min. will ping you if it blows up**

```
BY B 12: CLAIM ANSWER 11 NOT need AGENT ME THEME help .
BY B 13: REQUEST give AGENT YOU TO ME THEME AROUND 20 minute .
BY B 14: PLAN IF { explode THEME D } { notify AGENT ME THEME YOU } .
```

**A: cool, thanks. no rush btw**

```
BY A 15: SOCIAL agree .
BY A 16: SOCIAL thank .
BY A 17: CLAIM ASIDE NOT MUST hurry AGENT YOU .
```

## D24

**Theorem. There are infinitely many prime numbers.**

```
1: HEAD theorem .
2: CLAIM NOT finite THEME count OF ALL prime .
```
[The spec's own example writes "finite THEME ALL prime", which reads as "every prime is finite"; I added "count OF".]

**Proof. Suppose, for contradiction, that there are only finitely many primes, and call them p1, p2, ..., pn.**

```
3: HEAD proof .
4: ASSUMED finite THEME count OF ALL prime .
5: DEFINE UNDER 4 «p1, p2, ..., pn» BE ALL prime NAMED L .
```
["for contradiction" has no place to go: a FOR role would attach to "finite", not to the act of supposing.]

**Let N = p1 p2 ... pn + 1.**

```
6: DEFINE UNDER 4 N BE «p1 p2 ... pn + 1» .
```

**Since N > 1, some prime q divides N.**

```
7: DERIVED 6 UNDER 4 MORE big THEME N THAN 1 .
8: DERIVED 7 RECALLED UNDER 4 exist THEME SOME prime KIND { divide AGENT SELF THEME N } .
9: DEFINE UNDER 4 Q BE 1 prime KIND { divide AGENT SELF THEME N } .
```
[SOME prime NAMED Q would bind Q for one sentence only, so the witness needs its own DEFINE.]

**But q cannot be any of p1, ..., pn, because dividing N by any pi leaves remainder 1.**

```
10: DERIVED 6 UNDER 4 EACH I IN L { (1) THEME remainder OF { divide THEME N WITH I } } .
11: DERIVED 9 10 UNDER 4 CONTRAST 5 CAN NOT (ANY 1 OF L) THEME Q .
```

**So q is a prime not on our list, contradicting the assumption that the list was complete.**

```
12: DERIVED 9 11 UNDER 4 (prime KIND NOT (inside REL L)) THEME Q .
13: DERIVED 12 5 UNDER 4 contradict AGENT STEP 12 THEME { complete THEME L } .
```

**Hence there are infinitely many primes.**

```
14: DERIVED 4 13 NOT finite THEME count OF ALL prime .
```
