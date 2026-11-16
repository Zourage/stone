# Encodings V2 (spec 0.2)

Label form follows the grammar line (`label ":" header`), not the `ASSUMED 1:` example.

## H01

**A FAMISHED FOX saw some clusters of ripe black grapes hanging from a trellised vine.**

```
1: STORY PAST see AGENT 1 fox KIND (VERY hungry) KIND female NAMED F THEME SOME cluster KIND grape KIND ripe KIND black NOTE { ONGOING hang THEME SELF FROM vine KIND trellis } NAMED G .
```

**She resorted to all her tricks to get at them, but wearied herself in vain, for she could not reach them.**

```
2: STORY SEQUENCE PAST use AGENT F THEME ALL trick OF F FOR { reach AGENT F THEME G } .
3: STORY CONTRAST 2 PAST tire AGENT F THEME F WITH futile CAUSE { NOT CAN reach AGENT F THEME G } .
```

**At last she turned away, hiding her disappointment and saying: "The Grapes are sour, and not ripe as I thought."**

```
4: STORY SEQUENCE PAST FINALLY turn AGENT F FROM G WHEN during REL { hide AGENT F THEME disappointment OF F AND say AGENT F THEME { BY F CLAIM sour THEME G AND NOT ripe THEME G DESPITE { PAST think AGENT ME THEME { ripe THEME G } } } } .
```

## H02

**A recipient MUST interpret a received protocol element according to the semantics defined for it by this specification, including extensions to this specification, unless the recipient has determined (through experience or configuration) that the sender incorrectly implements what is implied by those semantics.**

```
1: CLAIM MUST interpret AGENT ANY recipient NAMED R
   THEME ANY element KIND protocol KIND { DONE receive AGENT R THEME SELF } NAMED E
   WITH semantics KIND { define AGENT THIS specification NOTE { include AGENT SELF THEME extension OF THIS specification } THEME SELF FOR E } NAMED M
   EXCEPT { DONE determine AGENT R WITH (experience OR configuration) THEME { implement AGENT sender OF E WITH (NOT correct) THEME thing KIND { imply AGENT M THEME SELF } } } .
```

**For example, an origin server might disregard the contents of a received Accept-Encoding header field if inspection of the User-Agent header field indicates a specific implementation version that is known to fail on receipt of certain content codings.**

```
2: CLAIM EXAMPLE 1 IF
   { indicate AGENT { inspect THEME field KIND header KIND «User-Agent» } THEME 1 version OF implementation KIND specific NAMED V NOTE { know THEME { fail AGENT V WHEN { receive AGENT V THEME SOME coding KIND content } } } }
   { MAY disregard AGENT ANY server KIND origin NAMED O THEME content OF (field KIND header KIND «Accept-Encoding» KIND { DONE receive AGENT O THEME SELF }) } .
```

## H03

**Atomistic foundation models have emerged as a promising route to DFT-level accuracy for materials simulation with complex chemical environments.**

```
1: CLAIM DONE emerge THEME GENERIC model KIND foundation KIND atomistic NAMED M
   AS route KIND promising KIND { reach WITH SELF THEME accuracy KIND (level OF «DFT») ABOUT { simulate THEME material KIND { have AGENT SELF THEME environment KIND chemical KIND complex } } } .
```

**However, their reliability across competing bonding regimes and, more importantly, how complex bonding affects predictions of material properties remain unclear.**

```
2: CLAIM CONTRAST 1 NOW STILL (NOT clear) THEME
   ( { ASK WHAT reliable THEME M ABOUT ALL regime KIND bonding KIND competing }
     AND { ASK affect AGENT bonding KIND complex THEME { predict AGENT M THEME property OF material } WITH WHAT } NOTE { MORE important THEME SELF } ) .
```

**Among materials with competing bonding regimes, sodium storage in hard carbon poses a substantial challenge.**

```
3: CLAIM pose AGENT { store THEME sodium AT inside REL carbon KIND hard NAMED C } THEME 1 challenge KIND (VERY big)
   AT among REL (GENERIC material KIND { have AGENT SELF THEME regime KIND bonding KIND competing }) .
```

**Hard carbon features diverse local structural motifs, including defective and curved graphitic regions, amorphous regions, and closed/open pores.**

```
4: CLAIM have AGENT C THEME MANY motif KIND structure KIND local KIND diverse
   NOTE { include AGENT SELF THEME ( region KIND graphite KIND defective AND region KIND graphite KIND curved AND region KIND amorphous AND pore KIND closed AND pore KIND open ) } .
```

**Motivated by its importance for Na-ion batteries, we systematically evaluate existing pretrained foundation models based on the MACE architecture across different local Na/C motifs.**

```
5: CLAIM evaluate AGENT US WITH systematic
   THEME SEVERAL model KIND foundation KIND pretrained KIND existing KIND { base THEME SELF AT architecture KIND «MACE» } NAMED P
   ABOUT SEVERAL motif KIND local KIND «Na/C» KIND various
   CAUSE { important THEME C FOR battery KIND «Na-ion» } .
```

**We find that the pretrained models fail to accurately capture Na-Na and Na-C interactions for metallic Na clusters on graphene.**

```
6: GIVEN RESULT 5 find AGENT US THEME { fail AGENT P THEME { capture AGENT P WITH accurate THEME (interaction KIND «Na-Na» AND interaction KIND «Na-C») ABOUT cluster KIND «Na» KIND metal KIND (on REL graphene) } } .
```

## H04

**Matters of fact, which are the second objects of human reason, are not ascertained in the same manner; nor is our evidence of their truth, however great, of a like nature with the foregoing.**

```
1: CLAIM CONTRAST NOT ascertain THEME TOPIC GENERIC matter KIND fact NOTE { (ORD 2 object OF reason KIND human) THEME SELF } NAMED F WITH manner KIND same THAN THAT thing KIND previous .
2: CLAIM ADD NOT similar THEME nature OF (evidence OF (ME AND YOU) KIND { show THEME { true THEME F } } NAMED V) THAN nature OF THAT thing KIND previous DESPITE { great THEME V SPAN ANY amount } .
```

**The contrary of every matter of fact is still possible; because it can never imply a contradiction, and is conceived by the mind with the same facility and distinctness, as if ever so conformable to reality.**

```
3: CLAIM EACH X IN ALL matter KIND fact { ALWAYS possible THEME contrary OF X NAMED K
   CAUSE { NEVER CAN imply AGENT K THEME ANY contradiction
           AND conceive AGENT GENERIC mind THEME K WITH manner KIND (EQUAL easy) KIND (EQUAL distinct) THAN { UNREAL VERY conform THEME K TO reality } } } .
```

## H05

**So let me be very clear: if you as a maintainer feel that you control who or what can use your code, YOU ARE WRONG.**

```
1: PLAN RESULT EMPHASIS VERY clear THEME ME ABOUT STEP 2 .
2: CLAIM DETAIL 1 IF { feel AGENT YOU AS maintainer THEME { control AGENT YOU THEME { ASK CAN use AGENT (WHAT person OR WHAT thing) THEME code OF YOU } } } { CLAIM EMPHASIS wrong THEME FOCUS YOU } .
```

**I respect you technically, and I like working with you.**

```
3: CLAIM respect AGENT ME THEME YOU ABOUT technical AND like AGENT ME THEME { work AGENT ME ALONG YOU } .
```

**And no, I am not looking for yes-men, and I like it when you call me out on my bullshit.**

```
4: CLAIM ADD EMPHASIS NOT NOW ONGOING seek AGENT ME THEME person KIND { ALWAYS agree AGENT SELF } AND like AGENT ME THEME { criticise AGENT YOU THEME ME ABOUT nonsense OF ME } WHEN ANY time KIND { criticise AGENT YOU THEME ME } .
```

**I say some stupid things at times**

```
5: CLAIM EXPLAIN 4 say AGENT ME THEME SOME thing KIND stupid WHEN SOME time .
```

## H06

**SOCRATES: And might there not be another square twice as large as this, and having like this the lines equal?**

```
BY name«Socrates» NAMED S 1: ASK ADD LIKELY CAN exist THEME 1 OTHER square
   KIND { (double OF THIS square) THEME SELF ABOUT size }
   KIND { EQUAL long THEME ALL line OF ALSO SELF THAN MUTUAL } NAMED Q .
```

**BOY: Yes.**

```
BY boy NAMED B 2: CLAIM ANSWER 1 YES .
```

**SOCRATES: And of how many feet will that be?**

```
BY S 3: ASK ADD UNDER 1 big THEME Q SPAN WHAT foot .
```

**BOY: Of eight feet.**

```
BY B 4: CLAIM ANSWER 3 SPAN 8 foot .
```

**SOCRATES: And now try and tell me the length of the line which forms the side of that double square: this is two feet--what will that be?**

```
BY S 5: REQUEST SEQUENCE try AGENT YOU THEME { tell AGENT YOU TO ME THEME { ASK long THEME line KIND { form AGENT SELF THEME side OF Q } NAMED L SPAN WHAT } } .
BY S 6: GIVEN BACKGROUND 7 long THEME THIS line SPAN 2 foot .
BY S 7: ASK RESTATE 5 UNDER 1 long THEME L SPAN WHAT .
```

**BOY: Clearly, Socrates, it will be double.**

```
BY B 8: CLAIM ANSWER 7 CERTAIN CALL name«Socrates» (double OF THIS line) THEME L ABOUT length .
```

## H07

**How a nerve comes to be sensitive to light, hardly concerns us more than how life itself first originated; but I may remark that several facts make me suspect that any sensitive nerve may be rendered sensitive to light, and likewise to those coarser vibrations of the air which produce sound.**

```
1: CLAIM MORE concern AGENT { ASK BEGIN sensitive THEME GENERIC nerve TO light WITH WHAT } THEME US
   THAN { ASK PAST FAR BEGIN exist THEME EVEN life WITH WHAT } SPAN amount KIND (BARELY real) .
2: CLAIM CONTRAST 1 POLITE suspect AGENT ME CAUSE SEVERAL fact
   THEME { CAN make THEME { sensitive THEME ANY nerve KIND sensitive TO ( light AND ALSO vibration OF air KIND (MORE coarse) KIND { produce AGENT SELF THEME sound } ) } } .
```

## H08

**In considering additional adjustments to the target range for the federal funds rate, the Committee will carefully assess incoming data, the evolving outlook, and the balance of risks.**

```
1: PLAN assess AGENT THAT committee NAMED C WITH careful
   THEME ( data KIND { FUTURE arrive THEME SELF } AND outlook KIND { ONGOING change THEME SELF } AND balance OF risk )
   WHEN during REL { consider AGENT C THEME { adjust THEME range KIND target OF (rate KIND (fund KIND federal)) } KIND additional } .
```

**The Committee will continue reducing its holdings of Treasury securities and agency debt and agency mortgage-backed securities.**

```
2: PLAN ADD continue AGENT C THEME { reduce AGENT C THEME holding OF C KIND ( security KIND name«Treasury» AND debt KIND agency AND security KIND agency KIND { back THEME SELF WITH mortgage } ) } .
```

**The Committee is strongly committed to supporting maximum employment and returning inflation to its 2 percent objective.**

```
3: CLAIM VERY commit THEME C TO ( { support AGENT C THEME employment KIND maximum } AND { return AGENT C THEME inflation TO objective OF C KIND «2 percent» } ) .
```
