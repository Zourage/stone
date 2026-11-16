# Encodings, passages A (spec 0.1)

Conventions I had to choose because the spec is silent:
- A relation word marks the sentence it sits on; the label after it is the sentence it relates to (so `CONCEDE 4` on sentence 2 = "sentence 2 is conceded against sentence 4").
- Reported speech = `say/ask/answer AGENT x THEME { ... }`, with the speaker's "I/you" replaced by handles, because ME/YOU can only mean the writer and the reader.
- Labels restart at 1 in each passage.

---

## D01

**It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife.**

```
1: RECALLED acknowledge AGENT ALL person THEME { true THEME { need AGENT ALL man KIND single KIND { possess AGENT SELF THEME fortune KIND good } NAMED M THEME wife } } .
```

**However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters.**

```
2: RECALLED CONCEDE 4 POSSIBLE NOT know THEME feeling OF M WHEN { enter AGENT M THEME neighbourhood WITH first } .
3: RECALLED CONCEDE 4 POSSIBLE NOT know THEME view OF M WHEN { enter AGENT M THEME neighbourhood WITH first } .
4: RECALLED fix THEME STEP 1 AT mind OF family KIND { surround AGENT SELF THEME M } NAMED F WITH firm .
5: RECALLED RESULT 4 consider AGENT F THEME { own AGENT 1 daughter OF F THEME M WITH right } .
```

**"My dear Mr. Bennet," said his lady to him one day, "have you heard that Netherfield Park is let at last?"**

```
6: GIVEN PAST ask AGENT wife OF name«Mr. Bennet» NAMED W TO name«Mr. Bennet» NAMED B WHEN 1 day THEME { PAST DONE hear AGENT B THEME { DONE let THEME name«Netherfield Park» NAMED N } } .
```

**Mr. Bennet replied that he had not.**

```
7: GIVEN PAST answer AGENT B TO W THEME { NOT PAST DONE hear AGENT B } .
```

**"But it is," returned she; "for Mrs. Long has just been here, and she told me all about it."**

```
8: GIVEN CONTRAST 7 PAST answer AGENT W TO B THEME { DONE let THEME N } .
9: GIVEN ADD PAST say AGENT W TO B THEME { PAST DONE come AGENT name«Mrs. Long» NAMED L TO house OF W } .
10: GIVEN ADD PAST say AGENT W TO B THEME { PAST tell AGENT L TO W THEME ALL fact KIND { concern AGENT SELF THEME N } } .
```

**Mr. Bennet made no answer.**

```
11: GIVEN NOT PAST answer AGENT B .
```

**"Do not you want to know who has taken it?" cried his wife, impatiently.**

```
12: GIVEN PAST ask AGENT W TO B WITH impatience THEME { NOT want AGENT B THEME { know AGENT B THEME { PAST DONE take AGENT WHAT THEME N } } } .
```

**"_You_ want to tell me, and I have no objection to hearing it."**

```
13: GIVEN PAST say AGENT B TO W THEME { want AGENT INSTEAD W THEME { tell AGENT W TO B THEME { PAST DONE take AGENT WHAT THEME N } } } .
14: GIVEN ADD PAST say AGENT B TO W THEME { NOT object AGENT B TO { hear AGENT B } } .
```

---

## D05

**I am much obliged for your very agreeable letter;**

```
1: GIVEN EMPHASIS oblige THEME ME CAUSE letter OF YOU KIND agreeable NAMED L .
```

**it was very good-natured, in the midst of your scientific and theatrical dissipation, to think of writing so long a letter to me.**

```
2: GIVEN ADD PAST good-natured THEME { think AGENT YOU THEME { write AGENT YOU TO ME THEME letter KIND long } } WHEN dissipation OF YOU KIND scientific KIND theatrical .
```

**I am astonished at your news,**

```
3: GIVEN SURPRISE astonish THEME ME CAUSE news FROM YOU .
```

**and I must condole with you in your PRESENT view of the Professorship**

```
4: GIVEN ADD condole AGENT ME TO YOU CAUSE view OF YOU KIND present KIND { concern AGENT SELF THEME professorship NAMED P } NAMED V .
```

**(Sir J.D. Hooker was a candidate for the Professorship of Botany at Edinburgh University.),**

```
5: GIVEN BACKGROUND 4 PAST candidate THEME name«Sir J.D. Hooker» FOR professorship KIND botany AT name«Edinburgh University» .
```

**and most heartily deplore it on my own account.**

```
6: GIVEN ADD 4 REGRET deplore AGENT ME THEME V FOR ALSO ME WITH heart .
```

**There is something so chilling in a separation of so many hundred miles, though we did not see much of each other when nearer.**

```
7: GIVEN chilling THEME separation KIND (mile KIND (hundred KIND many)) .
8: GIVEN CONCEDE 7 NOT PAST HABIT see AGENT ME THEME YOU WITH frequent WHEN { PAST near THEME home OF ME TO home OF YOU THAN now } .
```

**You will hardly believe how deeply I regret for MYSELF your present prospects.**

```
9: GIVEN REGRET regret AGENT ME THEME prospect OF YOU KIND present NAMED R FOR ME WITH depth .
10: GIVEN ADD LIKELY NOT FUTURE believe AGENT YOU THEME depth OF STEP 9 .
```

**I had looked forward to [our] seeing much of each other during our lives.**

```
11: GIVEN BACKGROUND PAST DONE expect AGENT ME WITH pleasure THEME { FUTURE HABIT see AGENT ME THEME YOU WITH frequent WHEN life OF ME } .
```

**It is a heavy disappointment;**

```
12: GIVEN REGRET heavy THEME disappointment KIND { cause AGENT R THEME SELF } .
```

**and in a mere selfish point of view, as aiding me in my work, your loss is indeed irreparable.**

```
13: GIVEN ADD EMPHASIS irreparable THEME { lose AGENT ME THEME YOU KIND { aid AGENT SELF THEME work OF ME } } WITH ONLY view KIND selfish .
```

---

## D09

**No Person shall be a Representative who shall not have attained to the Age of twenty five Years, and been seven Years a citizen of the United States, and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen.**

```
1: GIVEN IF { OR { NOT DONE reach AGENT person NAMED P THEME age KIND (25 year) } { OR { NOT DONE hold AGENT P THEME citizenship OF name«United States» WHEN 7 year } { NOT inhabit AGENT P THEME state KIND { choose THEME P AT SELF } WHEN { elect THEME P } } } } { NOT representative THEME P } .
```

---

## D13

**Recent advances in speech neuroprostheses have enabled new communication avenues for people who have lost the ability to speak due to neurological illness or injury.**

```
1: RECALLED PAST DONE enable AGENT advance KIND recent KIND { concern AGENT SELF THEME prosthesis KIND nerve KIND speech NAMED S } THEME avenue KIND communication KIND new FOR person KIND { OR { PAST DONE lose AGENT SELF THEME (ability KIND speak) CAUSE illness KIND nerve } { PAST DONE lose AGENT SELF THEME (ability KIND speak) CAUSE injury KIND nerve } } NAMED U .
```

**These systems can decode neural activity during attempted speech into text by relying on language priors to achieve high decoding accuracy.**

```
2: RECALLED capable THEME S FOR { decode AGENT S THEME activity KIND nerve KIND { occur THEME SELF WHEN speech KIND attempt } TO text WITH { rely AGENT S TO prior KIND language FOR { achieve AGENT S THEME accuracy KIND decode KIND high } } } .
```

**This performance currently comes at the cost of using a compute-intensive language modeling stack, presenting a major bottleneck for real-world use.**

```
3: RECALLED CONTRAST cost AGENT STEP 2 THEME { use AGENT S THEME stack KIND (model KIND language) KIND (intense KIND compute) } WHEN now .
4: RECALLED RESULT present AGENT STEP 3 THEME bottleneck KIND major FOR use KIND (world KIND real) .
```

**Further, current language models incur highly variable and disruptive inference latencies, limiting communication throughput and preventing users from reliably participating in natural conversation.**

```
5: RECALLED ADD incur AGENT model KIND language KIND current THEME latency KIND inference KIND variable KIND disrupt NAMED T .
6: RECALLED RESULT 5 limit AGENT T THEME throughput KIND communication .
7: RECALLED RESULT 5 prevent AGENT T THEME { participate AGENT U AT conversation KIND natural WITH reliable } .
```

---

## D17

**I was hopeful, and I've tried to just see if this long thread results in anything constructive, but this seems to be going backwards (or at least not forwards).**

```
1: GIVEN PAST hope AGENT ME .
2: GIVEN ADD PAST DONE try AGENT ME THEME ONLY { watch AGENT ME THEME { OR { result AGENT thread KIND long NAMED T THEME SOME thing KIND constructive } { NOT result AGENT T THEME SOME thing KIND constructive } } } .
3: GIVEN CONTRAST LIKELY OR { ONGOING go THEME T TO backward } { NOT ONGOING go THEME T TO forward } .
```

**The fact is, the pull request you objected to DID NOT TOUCH THE DMA LAYER AT ALL.**

```
4: GIVEN CERTAIN EMPHASIS NOT PAST touch AGENT request KIND pull KIND { PAST object AGENT YOU TO SELF } NAMED R THEME layer KIND «DMA» NAMED D .
```

**It was literally just another user of it, in a completely separate subdirectory, that didn't change the code you maintain in _any_ way, shape, or form.**

```
5: GIVEN RESTATE 4 PAST equal THEME R TO ONLY (user KIND additional OF D) .
6: GIVEN ADD PAST locate THEME R AT directory KIND sub KIND separate .
7: GIVEN ADD EMPHASIS PAST change AGENT R THEME code KIND { maintain AGENT YOU THEME SELF } NAMED C WITH NO way .
```

**I find it distressing that you are complaining about new users of your code, and then you keep bringing up these kinds of complete garbage arguments.**

```
8: GIVEN distress THEME ME CAUSE { ONGOING complain AGENT YOU THEME user KIND new OF C } .
9: GIVEN ADD distress THEME ME CAUSE { HABIT raise AGENT YOU THEME argument KIND garbage KIND complete } .
```

**Honestly, what you have been doing is basically saying "as a DMA maintainer I control what the DMA code is used for".**

```
10: GIVEN EMPHASIS PAST ONGOING equal THEME act OF YOU TO { say AGENT YOU THEME { control AGENT YOU THEME purpose KIND { use THEME code OF D FOR SELF } CAUSE { maintain AGENT YOU THEME D } } NAMED Q } .
```

**And that is not how *any* of this works.**

```
11: GIVEN ADD EMPHASIS work THEME NO part OF (process KIND develop) WITH way KIND { describe AGENT Q THEME SELF } .
```

---

## D21

**Because I could not stop for Death, He kindly stopped for me;**

```
1: GIVEN PAST stop AGENT death NAMED D FOR ME WITH kindness CAUSE { NOT PAST capable THEME ME FOR { stop AGENT ME FOR D } } .
```

**The carriage held but just ourselves And Immortality.**

```
2: GIVEN PAST hold AGENT carriage THEME ONLY (group KIND { member THEME ME AT SELF } KIND { member THEME D AT SELF } KIND { member THEME immortality AT SELF }) .
```

**We slowly drove, he knew no haste,**

```
3: GIVEN PAST drive AGENT ME WITH slow .
4: GIVEN ADD PAST drive AGENT ALSO D WITH slow .
5: GIVEN BACKGROUND NOT PAST know AGENT D THEME haste .
```

**And I had put away My labor, and my leisure too, For his civility.**

```
6: GIVEN ADD PAST DONE discard AGENT ME THEME labor OF ME CAUSE civility OF D .
7: GIVEN ADD PAST DONE discard AGENT ME THEME ALSO leisure OF ME CAUSE civility OF D .
```
