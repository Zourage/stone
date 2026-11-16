# Encodings, passage set B (spec 0.1, gloss notation)

Conventions I had to assume because the spec is silent:
- A role particle may be repeated in one clause (THEME a THEME b) and is read as "a and b jointly". The spec neither allows nor forbids this; every list below depends on it.
- A relation may be followed by one label (`CONTRAST 3`); DERIVED is followed by its labels.
- Sentence labels are numbers, restarted per passage.
- Strength after ASK is read as "the asker expects this answer" (not defined in the spec).

---

## D02

**He was quick and alert in the things of life, but only in the things, and not in the significances.**

```
1: GIVEN PAST quick THEME man NAMED M AT thing OF life .
2: GIVEN ADD 1 PAST alert THEME M AT ONLY thing OF life .
3: GIVEN CONTRAST 2 NOT PAST alert THEME M AT meaning OF (thing OF life) .
```

**Fifty degrees below zero meant eighty odd degrees of frost.**

```
4: GIVEN PAST mean AGENT (temperature KIND { low THEME SELF THAN 0 WITH 50 degree }) NAMED T THEME (80 degree OF frost) .
```

**Such fact impressed him as being cold and uncomfortable, and that was all.**

```
5: GIVEN PAST seem TO M THEME ONLY { cold THEME T } THEME ONLY { NOT comfort THEME T } .
```

**It did not lead him to meditate upon his frailty as a creature of temperature, and upon man's frailty in general, able only to live within certain narrow limits of heat and cold; and from there on it did not lead him to the conjectural field of immortality and man's place in the universe.**

```
6: GIVEN NOT PAST cause AGENT T THEME { think AGENT M THEME (frail OF M) CAUSE { creature KIND temperature THEME M } } .
7: GIVEN ADD 6 NOT PAST cause AGENT T THEME { think AGENT M THEME frail OF (ALL human KIND { live AGENT SELF AT ONLY (limit KIND narrow OF heat OF cold) }) } .
8: GIVEN SEQUENCE 7 NOT PAST cause AGENT T THEME { think AGENT M THEME (field KIND conjecture OF (life KIND { NOT end THEME SELF })) THEME (place KIND { hold AGENT human THEME SELF AT universe }) } .
```

**Fifty degrees below zero stood for a bite of frost that hurt and that must be guarded against by the use of mittens, ear-flaps, warm moccasins, and thick socks.**

```
9: GIVEN PAST mean AGENT T TO M THEME bite OF frost KIND { hurt AGENT SELF } KIND { necessary THEME { guard FROM SELF WITH { use THEME mitten THEME (flap KIND ear) THEME (moccasin KIND warm) THEME (sock KIND thick) } } } .
```

**Fifty degrees below zero was to him just precisely fifty degrees below zero.**

```
10: GIVEN EMPHASIS PAST mean AGENT T TO M THEME ONLY T .
```

**That there should be anything more to it than that was a thought that never entered his head.**

```
11: GIVEN PAST think AGENT M THEME { mean AGENT T THEME SOME thing KIND { NOT same THEME SELF THAN T } } WHEN NO time .
```

---

## D06

Speaker turns cannot be marked on a sentence, so the turns are encoded as bare sentences 1-21 and two framing sentences (22, 23) assign them to speakers.

**SOCRATES: Tell me, boy, do you know that a figure like this is a square?**

```
1: REQUEST tell AGENT YOU TO ME THEME STEP 2 .
2: ASK know AGENT YOU THEME { square THEME ALL figure KIND { similar THEME SELF THAN (figure KIND { show AGENT ME THEME SELF } NAMED F) } } .
```

**BOY: I do.**

```
3: RECALLED YES .
```

**SOCRATES: And you know that a square figure has these four lines equal?**

```
4: ASK ADD LIKELY know AGENT YOU THEME { equal THEME 4 line OF (ALL figure KIND square) } .
```

**BOY: Certainly.**

```
5: RECALLED CERTAIN know AGENT ME THEME { equal THEME 4 line OF (ALL figure KIND square) } .
```

**SOCRATES: And these lines which I have drawn through the middle of the square are also equal?**

```
6: ASK ADD LIKELY equal THEME ALSO line KIND { DONE draw AGENT ME THEME SELF AT middle OF square } .
```

**BOY: Yes.**

```
7: GIVEN YES .
```

**SOCRATES: A square may be of any size?**

```
8: ASK LIKELY NOT limit THEME size OF (ALL square) .
```

**BOY: Certainly.**

```
9: RECALLED CERTAIN NOT limit THEME size OF (ALL square) .
```

**SOCRATES: And if one side of the figure be of two feet, and the other side be of two feet, how much will the whole be?**

```
10: ASK ADD IF { equal THEME length OF (1 side OF F NAMED A) THAN (2 foot) } { IF { equal THEME length OF (side OF F KIND { NOT same THEME SELF THAN A } NAMED B) THAN (2 foot) } { equal THEME size OF (whole OF F) THAN WHAT } } .
```

**Let me explain: if in one direction the space was of two feet, and in the other direction of one foot, the whole would be of two feet taken once?**

```
11: PLAN POLITE explain AGENT ME THEME STEP 10 .
12: ASK LIKELY IF { long THEME space WITH (2 foot) AT 1 direction NAMED D } { IF { long THEME space WITH (1 foot) AT direction KIND { NOT same THEME SELF THAN D } } { equal THEME size OF (whole OF space) THAN (multiply FIRST (2 foot) SECOND 1) } } .
```

**BOY: Yes.**

```
13: GIVEN YES .
```

**SOCRATES: But since this side is also of two feet, there are twice two feet?**

```
14: ASK CONTRAST 12 LIKELY equal THEME size OF (whole OF F) THAN (multiply FIRST 2 SECOND (2 foot)) CAUSE { equal THEME ALSO (length OF B) THAN (2 foot) } .
```

**BOY: There are.**

```
15: GIVEN YES .
```

**SOCRATES: Then the square is of twice two feet?**

```
16: ASK RESULT 14 LIKELY equal THEME size OF F THAN (multiply FIRST 2 SECOND (2 foot)) .
```

**BOY: Yes.**

```
17: GIVEN YES .
```

**SOCRATES: And how many are twice two feet? count and tell me.**

```
18: ASK ADD equal THEME (multiply FIRST 2 SECOND (2 foot)) THAN WHAT .
19: REQUEST count AGENT YOU .
20: REQUEST SEQUENCE 19 tell AGENT YOU TO ME THEME result OF count .
```

**BOY: Four, Socrates.**

```
21: GIVEN THAN 4 .
```

Speaker frame (not in the source as sentences):

```
22: GIVEN say AGENT name«Socrates» TO boy THEME STEP 1 THEME STEP 2 THEME STEP 4 THEME STEP 6 THEME STEP 8 THEME STEP 10 THEME STEP 11 THEME STEP 12 THEME STEP 14 THEME STEP 16 THEME STEP 18 THEME STEP 19 THEME STEP 20 .
23: GIVEN say AGENT boy TO name«Socrates» THEME STEP 3 THEME STEP 5 THEME STEP 7 THEME STEP 9 THEME STEP 13 THEME STEP 15 THEME STEP 17 THEME STEP 21 .
```

---

## D10

**All the objects of human reason or enquiry may naturally be divided into two kinds, to wit, Relations of Ideas, and Matters of Fact.**

```
1: RECALLED fit THEME { divide THEME ALL object KIND { OR { reason AGENT human THEME SELF } { enquire AGENT human THEME SELF } } TO 2 kind WITH nature } .
2: RECALLED RESTATE 1 name THEME 2 kind TO (relation OF idea NAMED R) TO (matter OF fact NAMED F) .
```

**Of the first kind are the sciences of Geometry, Algebra, and Arithmetic; and in short, every affirmation which is either intuitively or demonstratively certain.**

```
3: RECALLED belong TO R THEME (science KIND geometry) THEME (science KIND algebra) THEME (science KIND arithmetic) .
4: RECALLED RESTATE 3 belong TO R THEME ALL claim KIND { OR { sure THEME SELF WITH intuition } { sure THEME SELF WITH demonstrate } } .
```

**That the square of the hypothenuse is equal to the square of the two sides, is a proposition which expresses a relation between these figures.**

```
5: RECALLED EXAMPLE 4 express AGENT { equal THEME (square OF hypotenuse) THAN (square OF (2 side)) } THEME relation OF figure .
```

**That three times five is equal to the half of thirty, expresses a relation between these numbers.**

```
6: RECALLED EXAMPLE 4 express AGENT { equal THEME (multiply FIRST 3 SECOND 5) THAN (divide FIRST 30 SECOND 2) } THEME relation OF number .
```

**Propositions of this kind are discoverable by the mere operation of thought, without dependence on what is anywhere existent in the universe.**

```
7: RECALLED able THEME { discover THEME ALL claim OF R WITH ONLY (operate OF thought) } .
8: RECALLED ADD 7 depend THEME STEP 7 TO NO thing KIND { exist THEME SELF AT SOME place OF universe } .
```

**Though there never were a circle or triangle in nature, the truths demonstrated by Euclid would for ever retain their certainty and evidence.**

```
9: ASSUMED PAST exist THEME NO shape KIND { OR { circle THEME SELF } { triangle THEME SELF } } AT nature WHEN ALL time .
10: RECALLED CONCEDE 9 CERTAIN keep AGENT (truth KIND { PAST demonstrate AGENT name«Euclid» THEME SELF } NAMED E) THEME (sure OF E) THEME (evident OF E) WHEN ALL time .
```

---

## D14

**TRIBE v2 (d'Ascoli et al., 2026) predicts fMRI responses across the cortical surface from video, audio and text.**

```
1: GIVEN predict AGENT «TRIBE v2» NAMED T THEME response KIND «fMRI» AT ALL surface OF cortex FROM video FROM audio FROM text .
2: GIVEN BACKGROUND 1 PAST describe THEME T AGENT name«d'Ascoli» AGENT SOME person WHEN year KIND «2026» .
```

**Its authors validated it with category-selective localizers (faces, places, bodies, words) and language contrasts, but not with the classic topographic organization of sensory cortex: retinotopy, tonotopy, and motion selectivity in area MT+.**

```
3: GIVEN PAST validate AGENT author OF T THEME T WITH (localize KIND (select KIND category)) WITH (contrast KIND language) .
4: GIVEN BACKGROUND 3 category THEME face THEME place THEME body THEME word .
5: GIVEN CONTRAST 3 NOT PAST validate AGENT author OF T THEME T WITH (organize KIND classic KIND topography OF (cortex KIND sense) NAMED O) .
6: GIVEN RESTATE 5 contain AGENT O THEME (map KIND retina NAMED R) THEME (map KIND tone) THEME (select KIND motion KIND { exist THEME SELF AT area KIND «MT+» }) .
```

**There is a clear architectural reason to expect retinotopy to fail: TRIBE's video features are averaged over space before the response head, which should discard visual-field position.**

```
7: GIVEN exist THEME reason KIND clear KIND architecture FOR { expect THEME { fail THEME R } } .
8: GIVEN RESTATE 7 average THEME feature KIND video OF T AT space WHEN time KIND { early THEME SELF THAN head KIND response } .
9: DERIVED 8 LIKELY discard AGENT STEP 8 THEME position KIND (field KIND vision) .
```

**I present mapping stimuli, a fitting pipeline adapted from standard fMRI mapping analyses, and a stand-in model with known ground truth that serves as a positive and negative control, and apply them to TRIBE v2's predictions, comparing the fitted maps with human atlases using spin tests.**

```
10: GIVEN present AGENT ME THEME (stimulus KIND map NAMED A) THEME (pipe KIND fit KIND { PAST adapt THEME SELF FROM analysis KIND standard KIND (map KIND «fMRI») } NAMED B) THEME (model KIND substitute KIND { know THEME truth OF SELF } KIND { serve AGENT SELF FOR (control KIND positive) FOR (control KIND negative) } NAMED C) .
11: GIVEN ADD 10 apply AGENT ME THEME A THEME B THEME C TO predict OF T .
12: GIVEN ADD 11 compare AGENT ME THEME map KIND fit THAN atlas KIND human WITH test KIND spin .
```

**TRIBE v2 shows a sharp split.**

```
13: GIVEN show AGENT T THEME split KIND sharp .
```

**There is no contralateral hemifield response and no polar-angle map, robustly across stimulus controls.**

```
14: GIVEN EXAMPLE 13 exist THEME NO response KIND (half OF field KIND { opposite THEME SELF }) THEME NO map KIND (angle KIND polar) WITH robust AT ALL control KIND stimulus .
```

---

## D18

**As part of the proposal to enable frame pointers by default in Fedora (URL), we did some benchmarking to figure out the expected performance impact.**

```
1: GIVEN exist THEME propose KIND { enable THEME point KIND frame AT name«Fedora» WITH default } NAMED P AT «https://fedoraproject.org/wiki/Changes/fno-omit-frame-pointer» .
2: GIVEN PAST benchmark AGENT (group OF ME NAMED W) WITH SOME test FOR { find AGENT W THEME effect KIND perform KIND { expect THEME SELF } OF P } .
3: GIVEN BACKGROUND 2 belong THEME STEP 2 TO P .
```

**The performance impact was generally minimal, except for the pyperformance benchmark suite where we noticed a more substantial difference between a system built with frame pointers and a system built without frame pointers.**

```
4: GIVEN PAST small THEME effect KIND perform AT ALL benchmark KIND { NOT belong THEME SELF TO (suite KIND benchmark KIND «pyperformance» NAMED Y) } .
5: GIVEN CONTRAST 4 PAST notice AGENT W AT Y THEME (difference KIND { differ THEME (system KIND { build THEME SELF WITH point KIND frame } NAMED X) THAN (system KIND { NOT build THEME SELF WITH point KIND frame } NAMED N) WITH SELF } NAMED D) .
6: GIVEN ADD 5 PAST big THEME D THAN difference KIND { exist THEME SELF AT ALL benchmark KIND { NOT belong THEME SELF TO Y } } .
```

**The results can be found here: URL (look at the mean difference column for the pyperformance results where the percentage is the slowdown compared to a system built without frame pointers).**

```
7: GIVEN exist THEME result AT «https://github.com/DaanDeMeyer/fpbench» .
8: REQUEST BACKGROUND 7 look AGENT YOU THEME (column KIND (difference KIND mean) NAMED C) FOR result OF Y .
9: DEFINE percent OF C BE slow OF X KIND { measure THEME SELF THAN N } .
```

**One of the biggest slowdowns was on the scimark_sparse_mat_mult benchmark which slowed down 9.5% when the system (including python) was built with frame pointers.**

```
10: GIVEN PAST slow THEME (benchmark KIND «scimark_sparse_mat_mult» NAMED K) WITH «9.5%» WHEN { build THEME system THEME ALSO name«Python» WITH point KIND frame } .
11: GIVEN ADD 10 belong THEME (slow OF K) TO (group KIND small OF slow NAMED Q) .
12: GIVEN ADD 11 big THEME ALL slow KIND { belong THEME SELF TO Q } THAN ALL slow KIND { NOT belong THEME SELF TO Q } .
```

**Note that these benchmarks were run against Python 3.11 on a Fedora 37 x86_64 system (one built with frame pointers, another built without frame pointers).**

```
13: GIVEN EMPHASIS PAST run AGENT W THEME ALL benchmark WITH name«Python» KIND «3.11» AT (2 system KIND (name«Fedora» KIND «37») KIND «x86_64» NAMED Z) .
14: GIVEN BACKGROUND 13 PAST build THEME 1 system OF Z WITH point KIND frame .
15: GIVEN CONTRAST 14 NOT PAST build THEME 1 system OF Z WITH point KIND frame .
```

**The system used to run the benchmarks was an Amazon EC2 machine.**

```
16: GIVEN same THEME machine KIND { PAST run AGENT W THEME benchmark AT SELF } THAN machine KIND «Amazon EC2» .
```

---

## D22

**Photosynthesis is a process in which green plants make their own food from sunlight, using the help of leaves to produce sugar.**

```
1: DEFINE photosynthesis BE process KIND { make AGENT (plant KIND green NAMED G) THEME food OF G FOR G FROM sunlight WITH help OF leaf FOR { produce THEME sugar } AT SELF } NAMED P .
```

**It is the process by which these organisms convert light energy into chemical energy, which is used to produce food.**

```
2: DEFINE RESTATE 1 P BE process KIND { convert AGENT G THEME energy KIND light TO (energy KIND chemistry NAMED E) WITH SELF } .
3: GIVEN ADD 2 use THEME E FOR { produce THEME food } .
```

**Photosynthesis is the process by which plant cells containing chlorophyll produce food substances (glucose and starch) from carbon dioxide and water, and oxygen is released.**

```
4: DEFINE RESTATE 2 P BE process KIND { produce AGENT cell OF plant KIND { contain AGENT SELF THEME chlorophyll } THEME (substance KIND food NAMED U) FROM «carbon dioxide» FROM water WITH SELF } .
5: GIVEN RESTATE 4 same THEME U THAN glucose THAN starch .
6: GIVEN ADD 4 release THEME oxygen WHEN P .
```

**Photosynthesis is not an accident.**

```
7: RECALLED NOT accident THEME P .
```

**It happens because its building blocks occur in space, and get included when planets form.**

```
8: RECALLED happen THEME P CAUSE { exist THEME (block KIND build OF P NAMED L) AT space } CAUSE { HABIT include THEME L TO planet WHEN { form THEME planet } } .
```

**We have no idea as to how common or rare this process is.**

```
9: RECALLED EMPHASIS NOT know AGENT ALL human THEME degree OF { common THEME P } .
```

**We do know that higher elements are formed in supernovae, and that is the origin of all elements higher than helium.**

```
10: RECALLED CONTRAST 9 EMPHASIS know AGENT ALL human THEME { HABIT form THEME element KIND { heavy THEME SELF THAN helium } AT supernova } .
11: RECALLED ADD 10 originate THEME ALL element KIND { heavy THEME SELF THAN helium } FROM supernova .
```
