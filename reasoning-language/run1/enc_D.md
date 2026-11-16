# Encodings, passage set D (spec 0.1)

Notes on conventions I had to choose because the spec is silent:
- Repeating a role inside one clause (two CAUSE phrases) is read as conjunction. The spec does not say this.
- `south THEME X THAN Y` is used for "X is south of Y", because `south OF Y` would decode as "the southern part of Y".
- `EACH h IN expr { }` from the Logic section is used inside ordinary blocks. The `body` grammar does not strictly allow it.
- Modality is carried by ordinary roots used as predicates over a block (`possible THEME { }`, `need THEME { }`).
- Lines marked `[lost: ...]` name what the encoding drops; details are in loss_D.json.

---

## D04

**S1.** To suppose that the eye, with all its inimitable contrivances for adjusting the focus to different distances, for admitting different amounts of light, and for the correction of spherical and chromatic aberration, could have been formed by natural selection, seems, I freely confess, absurd in the highest possible degree.

```
1: RECALLED have AGENT eye NAMED E THEME ALL contrivance KIND inimitable NAMED C .
2: RECALLED EXAMPLE 1 exist THEME SOME C FOR { adjust THEME focus TO distance KIND different } .
3: RECALLED ADD 2 exist THEME SOME C FOR { admit THEME light KIND (amount KIND different) } .
4: RECALLED ADD 3 exist THEME SOME C FOR { correct THEME aberration KIND sphere } .
5: RECALLED ADD 4 exist THEME SOME C FOR { correct THEME aberration KIND colour } .
6: GIVEN EMPHASIS seem TO ME THEME { absurd THEME { suppose THEME { possible THEME { PAST form AGENT (select KIND nature) THEME E } } } } .
7: GIVEN confess AGENT ME WITH free THEME STEP 6 .
```
[lost: "in the highest possible degree" (only sentence-level EMPHASIS); "with all its" as a concession inside the subject; the list as one phrase; generic "the eye"]

**S2.** Yet reason tells me, that if numerous gradations from a perfect and complex eye to one very imperfect and simple, each grade being useful to its possessor, can be shown to exist; if further, the eye does vary ever so slightly, and the variations be inherited, which is certainly the case; and if any variation or modification in the organ be ever useful to an animal under changing conditions of life, then the difficulty of believing that a perfect and complex eye could be formed by natural selection, though insuperable by our imagination, can hardly be considered real.

```
8: GIVEN CONTRAST 6 tell AGENT reason TO ME THEME {
     IF { possible THEME { show THEME { exist THEME gradation KIND numerous NAMED G
            FROM eye KIND perfect KIND complex TO eye KIND imperfect KIND simple } } }
        { IF { EACH H IN G { useful THEME H TO animal KIND { possess AGENT SELF THEME H } } }
             { IF { vary THEME E WITH slight }
                  { IF { inherit THEME variation OF E }
                       { IF { useful THEME SOME variation OF E TO animal WHEN SOME time WHEN { ONGOING change THEME condition OF life } }
                            { NOT real THEME difficulty NAMED D KIND { believe THEME { possible THEME { form AGENT (select KIND nature) THEME eye KIND perfect KIND complex } } } } } } } } } .
9: RECALLED BACKGROUND 8 CERTAIN vary THEME E WITH slight .
10: RECALLED ADD 9 CERTAIN inherit THEME variation OF E .
11: GIVEN CONCEDE 8 NOT possible THEME { overcome THEME D AGENT imagination OF ALL person } .
```
[lost: "very" imperfect; "ever so"; emphatic "does"; "which is certainly the case" as an aside inside the condition (restated as 9-10); "our"; "hardly" (NOT overstates); "can ... be considered"; the conjunction of conditions as a flat list; "variation or modification" collapsed to one root]

---

## D08

**S0.** Mode.--

```
1: GIVEN title THEME «Mode» .
```

**S1.** As a ham for baking should be well soaked, let it remain in water for at least 12 hours.

```
2: REQUEST remain THEME ham NAMED H AT water WHEN 12 «hour»
     CAUSE { need THEME { soak THEME ALL ham KIND { FUTURE bake THEME SELF } WITH thorough } } .
```
Workaround for "at least": `2b: REQUEST ADD 2 NOT short THEME (time KIND { remain THEME H AT water }) THAN 12 «hour» .`
[lost: duration vs. point of time in WHEN; generic "a ham"; "should" as a modal]

**S2.** Wipe it dry, trim away any rusty places underneath, and cover it with a common crust, taking care that this is of sufficient thickness all over to keep the gravy in.

```
3: REQUEST SEQUENCE wipe AGENT YOU THEME H TO dry .
4: REQUEST SEQUENCE trim AGENT YOU THEME ALL place KIND rust FROM (side KIND under OF H) .
5: REQUEST SEQUENCE cover AGENT YOU THEME H WITH crust KIND common NAMED K .
6: REQUEST ADD 5 ensure AGENT YOU THEME { keep AGENT K THEME gravy AT inside CAUSE { thick THEME ALL part OF K } } .
```
[lost: "sufficient ... to" as a degree-with-result; "any" = if there are any]

**S3.** Place it in a moderately-heated oven, and bake for nearly 4 hours.

```
7: REQUEST SEQUENCE place AGENT YOU THEME H AT oven KIND (heat KIND moderate) .
8: REQUEST SEQUENCE bake AGENT YOU THEME H WHEN 4 «hour» .
```
[lost: "nearly"; duration]

**S4.** Take off the crust, and skin, and cover with raspings, the same as for boiled ham, and garnish the knuckle with a paper frill.

```
9: REQUEST SEQUENCE remove AGENT YOU THEME K .
10: REQUEST SEQUENCE remove AGENT YOU THEME skin OF H .
11: REQUEST SEQUENCE cover AGENT YOU THEME H WITH rasping .
12: RECALLED BACKGROUND 11 same THEME STEP 11 THAN { cover THEME ham KIND boil WITH rasping } .
13: REQUEST SEQUENCE 11 garnish AGENT YOU THEME knuckle OF H WITH frill KIND paper .
```

**S5.** This method of cooking a ham is, by many persons, considered far superior to boiling it, as it cuts fuller of gravy and has a finer flavour, besides keeping a much longer time good.

```
14: GIVEN consider AGENT person KIND many THEME {
      good THEME ham KIND bake NAMED B THAN ham KIND boil NAMED L
      CAUSE { full THEME B THAN L WITH gravy WHEN { cut THEME B } }
      CAUSE { fine THEME flavour OF B THAN flavour OF L }
      CAUSE { long THEME time KIND { remain THEME B WITH good } THAN time KIND { remain THEME L WITH good } } } .
```
[lost: "far", "much"; "many" as a quantifier; "besides" as an added, lower-ranked reason; comparison of methods re-cast as comparison of hams]

---

## D12

**S1.** The try statement works as follows.

```
1: GIVEN describe AGENT STEP 3 THEME way KIND { work AGENT statement KIND «try» NAMED T WITH SELF } .
```
[lost: "as follows" points at sentences 3-11, STEP takes one label]

**S2.** First, the try clause (the statement(s) between the try and except keywords) is executed.

```
2: DEFINE clause KIND «try» NAMED C BE SOME statement KIND { locate THEME SELF FROM keyword KIND «try» TO keyword KIND «except» } .
3: GIVEN execute THEME C .
```

**S3.** If no exception occurs, the except clause is skipped and execution of the try statement is finished.

```
4: GIVEN SEQUENCE 3 IF { occur THEME NO exception WHEN { ONGOING execute THEME C } } { skip THEME clause KIND «except» NAMED X } .
5: GIVEN ADD 4 IF { occur THEME NO exception WHEN { ONGOING execute THEME C } } { DONE execute THEME T } .
```

**S4.** If an exception occurs during execution of the try clause, the rest of the clause is skipped.

```
6: GIVEN CONTRAST 4 IF { occur THEME exception NAMED E WHEN { ONGOING execute THEME C } } { skip THEME rest OF C } .
```

**S5.** Then, if its type matches the exception named after the except keyword, the except clause is executed, and then execution continues after the try/except block.

```
7: GIVEN SEQUENCE 6 IF { match AGENT type OF E THEME exception KIND { name THEME SELF AT place KIND { follow AGENT SELF THEME keyword KIND «except» } } NAMED N } { execute THEME X } .
8: GIVEN SEQUENCE 7 IF { match AGENT type OF E THEME N } { continue THEME execute AT place KIND { follow AGENT SELF THEME T } } .
```
[lost: 7 and 8 hold only inside the case opened by 6; nothing marks that]

**S6.** If an exception occurs which does not match the exception named in the except clause, it is passed on to outer try statements; if no handler is found, it is an unhandled exception and execution stops with an error message.

```
9: GIVEN CONTRAST 7 IF { occur THEME exception KIND { NOT match AGENT SELF THEME exception KIND { name THEME SELF AT X } } NAMED F } { pass THEME F TO ALL statement KIND «try» KIND outer } .
10: GIVEN SEQUENCE 9 IF { find THEME NO handler FOR F } { unhandled THEME F } .
11: GIVEN ADD 10 IF { find THEME NO handler FOR F } { stop THEME execute WITH message KIND error } .
```
[lost: "it is an unhandled exception" is a classification, encoded as a property]

---

## D16

**S1.** Title: What does the "yield" keyword do in Python?

```
title: ASK do AGENT keyword KIND «yield» NAMED Y AT language name«Python» THEME WHAT .
```

**S2.** What functionality does the yield keyword in Python provide?

```
1: ASK RESTATE title provide AGENT Y THEME function KIND WHAT .
```

**S3.** For example, I'm trying to understand this code1: [code]

```
2: GIVEN EXAMPLE 1 ONGOING try AGENT ME THEME { understand AGENT ME THEME code NAMED K } .
3: DEFINE K BE «def _get_child_candidates(self, distance, min_dist, max_dist):
    if self._leftchild and distance - max_dist < self._median:
        yield self._leftchild
    if self._rightchild and distance + max_dist >= self._median:
        yield self._rightchild» .
```

**S4.** And this is the caller: [code, cut off]

```
4: GIVEN ADD 3 call AGENT code NAMED L THEME K .
5: DEFINE L BE «result, candidates = [], [self]
while candidates:
    node = candidates.pop()
    distance = node._get_dist(obj)
    if distance <» .
```
[lost: that the source text is cut off mid-line; the footnote mark "1"; whether « » keeps line breaks and indentation is not stated]

---

## D20

**S1.** A deep upper low in the NE Pacific dives southwards well offshore on Wednesday.

```
1: GIVEN FUTURE dive THEME low KIND deep KIND (air KIND upper) NAMED L FROM ocean name«Pacific» KIND northeast TO south AT offshore KIND far WHEN wednesday .
```

**S2.** The bulk of the energy associated with this system will be focused south of western Washington as the system moves onshore into California on Thursday.

```
2: GIVEN FUTURE focus THEME part KIND main OF (energy OF L) AT place KIND { south THEME SELF THAN name«Washington» KIND west } WHEN { move THEME L FROM offshore TO name«California» WHEN thursday } .
```

**S3.** Precipitation spreads northwards into Washington on Wednesday, however, POPs mainly remain confined south of Seattle, and especially south of WA/OR border due to the trajectory of the system.

```
3: GIVEN FUTURE spread THEME precipitation TO north TO name«Washington» WHEN wednesday .
4: GIVEN CONTRAST 3 FUTURE confine THEME (chance KIND precipitation) NAMED P AT place KIND { south THEME SELF THAN name«Seattle» } CAUSE path OF L .
5: GIVEN ADD 4 EMPHASIS FUTURE confine THEME P AT place KIND { south THEME SELF THAN border KIND («WA/OR») } CAUSE path OF L .
```
[lost: "mainly" (not exclusively); "especially" as a ranking of two places, not sentence emphasis; "remain"]

**S4.** Easterly winds increase in the Cascade Valleys and gaps early Wednesday for breezy conditions, with NBM probabilities of gusts over 30 MPH in areas around North Bend and Enumclaw around 30-60%.

```
6: GIVEN FUTURE increase THEME wind KIND east NAMED W AT valley OF mountain name«Cascade» WHEN wednesday KIND early .
7: GIVEN ADD 6 FUTURE increase THEME W AT gap OF mountain name«Cascade» WHEN wednesday KIND early .
8: GIVEN RESULT 6 FUTURE breeze THEME condition .
9: GIVEN ADD 8 say AGENT model name«NBM» THEME { equal THEME chance KIND { fast THEME gust THAN 30 «MPH» AT area KIND near name«North Bend» } TO «30-60%» } .
10: GIVEN ADD 9 say AGENT model name«NBM» THEME { equal THEME chance KIND { fast THEME gust THAN 30 «MPH» AT area KIND near name«Enumclaw» } TO «30-60%» } .
```
[lost: "around" 30-60%; the range lives only inside « »; one joint probability for both towns is split into two claims]

**S5.** Drier conditions by Thursday into Friday.

```
11: GIVEN SEQUENCE FUTURE dry THEME condition THAN (condition WHEN wednesday) WHEN thursday WHEN friday .
```
[lost: "by" (onset no later than) and "into" (continuing through); the change of state]

**S6.** Periods of clearing may result in fog development, mainly Friday AM.

```
12: GIVEN POSSIBLE FUTURE cause AGENT period KIND clear THEME { develop THEME fog } WHEN morning OF friday .
```
[lost: "mainly"]

**S7.** Ensembles suggest troughing deepens again offshore Saturday into next week, with some uncertainty into the exact positioning and depth of the trough.

```
13: GIVEN suggest AGENT forecast KIND ensemble THEME { FUTURE deepen THEME trough NAMED T AT offshore FROM saturday TO week KIND next } .
14: GIVEN ADD 13 NOT certain THEME position KIND exact OF T .
15: GIVEN ADD 14 NOT certain THEME depth KIND exact OF T .
```
[lost: "again"; "some" uncertainty; FROM/TO reused for a time span]

**S8.** Highs remain near normal during this period in upper 40s to low 50s.

```
16: GIVEN FUTURE remain THEME temperature KIND high KIND day NAMED X AT near KIND normal WHEN { deepen THEME T } .
17: GIVEN RESTATE 16 FUTURE range THEME X FROM (part KIND upper OF «40s») TO (part KIND low OF «50s») .
```

---

## D24

**S1.** Theorem. There are infinitely many prime numbers.

```
theorem: PLAN prove AGENT ME THEME { infinite THEME count OF ALL prime } .
```
[lost: the statement is a claim, not the writer's plan; no opener states "this is asserted and the proof follows"]

**S2.** Proof. Suppose, for contradiction, that there are only finitely many primes, and call them p1, p2, ..., pn.

```
1: ASSUMED finite THEME count OF ALL prime FOR contradict .
2: DEFINE P BE list KIND { contain AGENT SELF THEME ALL prime } .
2b: DEFINE «p1, p2, ..., pn» BE ALL item OF P .
```

**S3.** Let N = p1 p2 ... pn + 1.

```
3: DEFINE N BE (add FIRST (product FIRST P) SECOND 1) .
```

**S4.** Since N > 1, some prime q divides N.

```
4: DERIVED 3 big THEME N THAN 1 .
5: RECALLED EACH M IN number { IF { big THEME M THAN 1 } { divide AGENT SOME prime THEME M } } .
6: DERIVED 4 5 divide AGENT SOME prime NAMED Q THEME N .
```

**S5.** But q cannot be any of p1, ..., pn, because dividing N by any pi leaves remainder 1.

```
7: DERIVED 3 EACH I IN P { (equal FIRST (remainder FIRST N SECOND I) SECOND 1) } .
8: DERIVED CONTRAST 6 6 7 CERTAIN NOT contain AGENT P THEME Q .
```

**S6.** So q is a prime not on our list, contradicting the assumption that the list was complete.

```
9: DERIVED 6 8 exist THEME prime KIND { NOT contain AGENT P THEME SELF } .
10: DERIVED 9 2 contradict AGENT STEP 9 THEME STEP 2 .
```

**S7.** Hence there are infinitely many primes.

```
11: DERIVED 1 10 NOT finite THEME count OF ALL prime .
```
[lost: sentences 2-10 are inside the supposition and 11 is outside it; only the cited labels hint at this]
