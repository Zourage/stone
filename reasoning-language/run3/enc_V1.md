# Encodings V1 (spec 0.1, gloss notation)

Conventions I had to adopt because the spec is silent (each is logged in `loss_V1.json`):
- Lists and coordinated phrases are split into several sentences joined by ADD (the spec has no phrase coordination).
- Narrative and authorial assertion use GIVEN or RECALLED, the nearest openers.
- A block's unmarked time is read relative to the clause that contains it.
- Dialogue turns are attributed with a frame sentence `say AGENT speaker THEME STEP n`.
- Labels restart at 1 in each passage.

---

## H01 — Fable

**A FAMISHED FOX saw some clusters of ripe black grapes hanging from a trellised vine.**

```
1: GIVEN PAST see AGENT fox KIND famished NAMED F THEME SOME cluster KIND (grape KIND ripe KIND black) KIND { ONGOING hang THEME SELF FROM vine KIND { support AGENT trellis THEME SELF } } NAMED G .
```

**She resorted to all her tricks to get at them, but wearied herself in vain, for she could not reach them.**

```
2: GIVEN SEQUENCE PAST use AGENT F THEME ALL trick OF F FOR { reach AGENT F THEME G } .
3: GIVEN CONTRAST PAST weary AGENT F THEME F WITH futile CAUSE { NOT PAST able THEME F FOR { reach AGENT F THEME G } } .
```

**At last she turned away, hiding her disappointment and saying: "The Grapes are sour, and not ripe as I thought."**

```
4: GIVEN SEQUENCE PAST turn AGENT F FROM G WHEN end WITH { ONGOING hide AGENT F THEME disappointment OF F } .
5: GIVEN ADD PAST say AGENT F THEME { sour THEME G } .
6: GIVEN ADD PAST say AGENT F THEME { NOT ripe THEME G } .
7: GIVEN ADD PAST say AGENT F THEME { PAST think AGENT F THEME { ripe THEME G } } .
```

---

## H02 — Technical standard

**A recipient MUST interpret a received protocol element according to the semantics defined for it by this specification, including extensions to this specification, unless the recipient has determined (through experience or configuration) that the sender incorrectly implements what is implied by those semantics.**

```
1: ASSUMED DONE receive AGENT recipient NAMED R THEME element KIND protocol NAMED E FROM sender NAMED S .
2: GIVEN define AGENT document KIND specification NAMED D THEME meaning OF E NAMED M .
3: GIVEN ADD ALSO define AGENT extension OF D THEME M .
4: GIVEN IF { NOT DONE determine AGENT R THEME { implement AGENT S WITH error THEME thing KIND { imply AGENT M THEME SELF } } } { oblige THEME R TO { interpret AGENT R THEME E WITH M } } .
5: GIVEN BACKGROUND 4 OR { determine AGENT R WITH experience } { determine AGENT R WITH configuration } .
```

**For example, an origin server might disregard the contents of a received Accept-Encoding header field if inspection of the User-Agent header field indicates a specific implementation version that is known to fail on receipt of certain content codings.**

```
6: GIVEN EXAMPLE 4 POSSIBLE IF { indicate AGENT { inspect THEME field KIND header KIND «User-Agent» } THEME version KIND implementation KIND specific NAMED V } { disregard AGENT server KIND origin THEME content OF (field KIND header KIND «Accept-Encoding» KIND { DONE receive THEME SELF }) } .
7: GIVEN BACKGROUND 6 know THEME { HABIT fail THEME V WHEN { receive AGENT V THEME SOME coding KIND content } } .
```

---

## H03 — Research abstract

**Atomistic foundation models have emerged as a promising route to DFT-level accuracy for materials simulation with complex chemical environments.**

```
1: RECALLED DONE become THEME model KIND foundation KIND atomistic NAMED M TO route KIND promising KIND { lead THEME SELF TO accuracy KIND (level OF «DFT») FOR { simulate THEME material KIND { complex THEME environment KIND chemical OF SELF } } } .
```

**However, their reliability across competing bonding regimes and, more importantly, how complex bonding affects predictions of material properties remain unclear.**

```
2: RECALLED CONTRAST NOT ONGOING clear THEME { reliable THEME M AT ALL regime KIND bonding KIND { compete THEME SELF } } .
3: RECALLED ADD NOT ONGOING clear THEME { affect AGENT bonding KIND complex THEME { predict AGENT M THEME property OF material } WITH WHAT } .
4: RECALLED ADD important THEME STEP 3 THAN STEP 2 .
```

**Among materials with competing bonding regimes, sodium storage in hard carbon poses a substantial challenge.**

```
5: RECALLED pose AGENT { store THEME sodium AT inside OF (carbon KIND hard NAMED H) } THEME challenge KIND substantial AT material KIND { compete THEME regime KIND bonding OF SELF } .
```

**Hard carbon features diverse local structural motifs, including defective and curved graphitic regions, amorphous regions, and closed/open pores.**

```
6: RECALLED have THEME H WITH motif KIND structure KIND local KIND diverse NAMED T .
7: RECALLED EXAMPLE 6 include AGENT T THEME region KIND graphite KIND defective .
8: RECALLED EXAMPLE 6 include AGENT T THEME region KIND graphite KIND curved .
9: RECALLED EXAMPLE 6 include AGENT T THEME region KIND amorphous .
10: RECALLED EXAMPLE 6 include AGENT T THEME pore KIND closed .
11: RECALLED EXAMPLE 6 include AGENT T THEME pore KIND open .
```

**Motivated by its importance for Na-ion batteries, we systematically evaluate existing pretrained foundation models based on the MACE architecture across different local Na/C motifs.**

```
12: GIVEN evaluate AGENT ME WITH system THEME model KIND foundation KIND existing KIND pretrained KIND { base THEME SELF AT architecture KIND name«MACE» } NAMED P AT motif KIND local KIND «Na/C» KIND different CAUSE { important THEME H FOR battery KIND (ion KIND «Na») } .
```

**We find that the pretrained models fail to accurately capture Na-Na and Na-C interactions for metallic Na clusters on graphene.**

```
13: GIVEN find AGENT ME THEME { NOT accurate THEME { capture AGENT P THEME interaction KIND «Na-Na» OF (cluster KIND «Na» KIND metal KIND { rest THEME SELF AT surface OF graphene }) } } .
14: GIVEN ADD find AGENT ME THEME { NOT accurate THEME { capture AGENT P THEME interaction KIND «Na-C» OF (cluster KIND «Na» KIND metal KIND { rest THEME SELF AT surface OF graphene }) } } .
```

---

## H04 — Philosophy

Sentence 0 is not in the source. It is added only to bind a handle for "the foregoing" (the relations of ideas discussed before the excerpt).

```
0: GIVEN PAST describe AGENT ME THEME relation OF idea NAMED I .
```

**Matters of fact, which are the second objects of human reason, are not ascertained in the same manner; nor is our evidence of their truth, however great, of a like nature with the foregoing.**

```
1: RECALLED NOT same THEME manner OF { ascertain THEME matter KIND fact NAMED F } THAN manner OF { ascertain THEME I } .
2: RECALLED BACKGROUND 1 equal THEME F TO (object KIND second OF (reason OF human)) .
3: RECALLED ADD 1 IF { great THEME evidence KIND { show AGENT SELF TO human THEME { true THEME F } } NAMED E } { NOT similar THEME nature OF E TO nature OF (evidence KIND { show AGENT SELF TO human THEME { true THEME I } }) } .
```

**The contrary of every matter of fact is still possible; because it can never imply a contradiction, and is conceived by the mind with the same facility and distinctness, as if ever so conformable to reality.**

```
4: RECALLED possible THEME contrary OF (ALL matter KIND fact) NAMED C CAUSE { NOT possible THEME { imply AGENT C THEME contradiction WHEN SOME time } } .
5: RECALLED BACKGROUND 4 same THEME ease OF { conceive AGENT mind THEME C } THAN ease OF { conceive AGENT mind THEME thing KIND { conform THEME SELF TO reality } } .
6: RECALLED BACKGROUND 4 same THEME distinctness OF { conceive AGENT mind THEME C } THAN distinctness OF { conceive AGENT mind THEME thing KIND { conform THEME SELF TO reality } } .
```

---

## H05 — Mailing-list reply

**So let me be very clear: if you as a maintainer feel that you control who or what can use your code, YOU ARE WRONG.**

```
1: RECALLED RESULT EMPHASIS IF { think AGENT YOU KIND { maintain AGENT SELF } THEME { control AGENT YOU THEME { permit THEME { use AGENT WHAT THEME code OF YOU } } } } { wrong THEME YOU } .
```

**I respect you technically, and I like working with you.**

```
2: GIVEN respect AGENT ME THEME YOU AT matter KIND technical .
3: GIVEN ADD like AGENT ME THEME { work AGENT ME WITH YOU } .
```

**And no, I am not looking for yes-men, and I like it when you call me out on my bullshit. I say some stupid things at times**

```
4: GIVEN ADD NOT ONGOING seek AGENT ME THEME person KIND { HABIT say AGENT SELF THEME ONLY «yes» } .
5: GIVEN ADD like AGENT ME THEME { HABIT challenge AGENT YOU THEME ME CAUSE bullshit OF ME } .
6: GIVEN BACKGROUND 5 say AGENT ME THEME SOME thing KIND stupid WHEN SOME time .
```

---

## H06 — Dialogue

Sentence 0 is not in the source. It is added only to bind a handle for the square Socrates points at ("this").

```
0: GIVEN PAST show AGENT name«Socrates» NAMED S TO boy NAMED B THEME square NAMED Q .
```

**SOCRATES: And might there not be another square twice as large as this, and having like this the lines equal?**

```
1: GIVEN PAST say AGENT S TO B THEME STEP 2 .
2: ASK ADD POSSIBLE exist THEME square KIND { NOT same THEME SELF THAN Q } KIND { equal THEME size OF SELF TO (multiply FIRST 2 SECOND size OF Q) } KIND { equal THEME ALL line OF ALSO SELF } NAMED X .
```

**BOY: Yes.**

```
3: GIVEN PAST say AGENT B TO S THEME STEP 4 .
4: GIVEN YES .
```

**SOCRATES: And of how many feet will that be?**

```
5: GIVEN PAST say AGENT S TO B THEME STEP 6 .
6: ASK ADD FUTURE equal THEME size OF X TO (WHAT KIND foot) .
```

**BOY: Of eight feet.**

```
7: GIVEN PAST say AGENT B TO S THEME STEP 8 .
8: GIVEN TO 8 foot .
```

**SOCRATES: And now try and tell me the length of the line which forms the side of that double square: this is two feet--what will that be?**

```
9: GIVEN PAST say AGENT S TO B THEME STEP 10 THEME STEP 11 THEME STEP 12 .
10: REQUEST SEQUENCE try AGENT YOU THEME { tell AGENT YOU TO ME THEME length OF (line KIND { form AGENT SELF THEME side OF X }) NAMED N } .
11: GIVEN BACKGROUND 10 equal THEME length OF (line OF Q NAMED L) TO 2 foot .
12: ASK RESTATE 10 FUTURE equal THEME N TO WHAT .
```

**BOY: Clearly, Socrates, it will be double.**

```
13: GIVEN PAST say AGENT B TO S THEME STEP 14 .
14: DERIVED 11 CERTAIN FUTURE equal THEME N TO (multiply FIRST 2 SECOND length OF L) .
```

---

## H07 — Scientific remark

**How a nerve comes to be sensitive to light, hardly concerns us more than how life itself first originated; but I may remark that several facts make me suspect that any sensitive nerve may be rendered sensitive to light, and likewise to those coarser vibrations of the air which produce sound.**

```
1: RECALLED NOT concern AGENT { become THEME nerve NAMED N TO { sensitive THEME N TO light } WITH WHAT } THEME human THAN { PAST originate THEME EVEN life WITH WHAT } .
2: GIVEN CONTRAST POLITE say AGENT ME THEME { cause AGENT SOME fact THEME { suspect AGENT ME THEME { possible THEME { become THEME ALL nerve KIND sensitive NAMED V TO { sensitive THEME V TO light } } } } } .
3: GIVEN ADD POLITE say AGENT ME THEME { cause AGENT SOME fact THEME { suspect AGENT ME THEME { possible THEME { become THEME V TO { sensitive THEME V TO ALSO vibration OF air KIND { coarse THEME SELF THAN light } KIND { produce AGENT SELF THEME sound } } } } } } .
```

---

## H08 — Central bank statement

**In considering additional adjustments to the target range for the federal funds rate, the Committee will carefully assess incoming data, the evolving outlook, and the balance of risks.**

```
1: PLAN FUTURE assess AGENT committee NAMED C WITH care THEME data KIND { ONGOING arrive THEME SELF } WHEN { consider AGENT C THEME adjustment KIND additional OF (range KIND target OF (rate KIND (fund KIND federal))) } .
2: PLAN ADD FUTURE assess AGENT C WITH care THEME outlook KIND { ONGOING evolve THEME SELF } WHEN { consider AGENT C THEME adjustment KIND additional OF (range KIND target OF (rate KIND (fund KIND federal))) } .
3: PLAN ADD FUTURE assess AGENT C WITH care THEME balance OF risk WHEN { consider AGENT C THEME adjustment KIND additional OF (range KIND target OF (rate KIND (fund KIND federal))) } .
```

**The Committee will continue reducing its holdings of Treasury securities and agency debt and agency mortgage-backed securities.**

```
4: PLAN FUTURE continue AGENT C THEME { reduce AGENT C THEME holding OF C KIND (security OF name«Treasury») } .
5: PLAN ADD FUTURE continue AGENT C THEME { reduce AGENT C THEME holding OF C KIND (debt OF agency) } .
6: PLAN ADD FUTURE continue AGENT C THEME { reduce AGENT C THEME holding OF C KIND (security OF agency KIND { back AGENT mortgage THEME SELF }) } .
```

**The Committee is strongly committed to supporting maximum employment and returning inflation to its 2 percent objective.**

```
7: GIVEN commit THEME C WITH strong TO { support AGENT C THEME employment KIND maximum } .
8: GIVEN ADD commit THEME C WITH strong TO { return AGENT C THEME inflation TO objective OF C KIND (2 «%») } .
```
