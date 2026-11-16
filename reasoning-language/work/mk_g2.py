import json, sys
I = []
def add(source, category, what, example, status, how_now, suggestion, priority):
    I.append(dict(source=source, category=category, what=what, example=example, status=status,
                  how_now=how_now, suggestion=suggestion, priority=priority))

# ---------------- Tamil
add("Tamil", "clause chaining (converb)",
 "The adverbial participle chains several events of one actor into one sentence, stating the subject, tense and mood once on the last verb.",
 "Naan indiyaavukku vantu tamizh paticceen = 'having come to India, I studied Tamil'; a day's routine is one sentence of five or six such links.",
 "CLUMSY",
 "Either separate sentences each repeating everything (1: STORY PAST come AGENT ME TO name«India» . 2: STORY SEQUENCE PAST study AGENT ME THEME name«Tamil» .) or one sentence with WHEN after REL { come AGENT ME TO name«India» }. Body-level AND says nothing about order, and SEQUENCE exists only between sentences.",
 "Add THEN to the body connectives beside AND / OR / BUT ('clause THEN clause' = the next event, same force as SEQUENCE but inside one sentence), plus the inheritance rule proposed under Dyirbal so the actor and time need not be repeated. Also explain BUT, which is in the grammar but nowhere defined.",
 3)
add("Tamil", "definiteness and specificity of objects",
 "Accusative marking on a non-human object means it is definite; leaving it bare means indefinite, so 'I lost the key' and 'I lost a key' differ by one suffix, and the numeral 'one' marks an explicit indefinite.",
 "Naan caaviyai tolaitteen 'I lost the key' / Naan caavi tolaitteen 'I lost a key' / oru caavi 'a (certain) key'.",
 "UNDECIDED",
 "THAT key = the identified one; bare key = unmarked. For a new referent writers will pick among bare key, SOME key, 1 key, key NAMED K. For 'a key, any key' (non-specific) there is ANY, but SOME is not glossed as specific or non-specific, so 'I am looking for a paper on this' (a particular one / any one) is not settled.",
 "One rule in Quantifiers: SOME = a particular one the writer has in mind but has not yet identified to the reader (specific, new); ANY = no particular one; THAT = already identified; bare = unsaid. No new particle needed.",
 2)
add("Tamil", "speaker attitude: apprehension and relief",
 "Auxiliary verbs grammaticalise the speaker's attitude to the event, including apprehension about its eventual result, relief that something unpleasant is over, and a pejorative view.",
 "'He has gone and told her (and I fear what follows)'; 'the exam is finally over (thank goodness)'.",
 "CLUMSY",
 "Relief ~ GLAD FINALLY. Apprehension has no particle: REGRET POSSIBLE fail THEME deploy could be read 'possibly, regrettably, it fails' but REGRET is about something that is the case, not something feared; otherwise fear AGENT ME THEME { FUTURE fail THEME deploy }.",
 "Add one attitude, WORRY (the writer fears this or its consequences), which also gives a compact warning: CLAIM WORRY POSSIBLE delete AGENT command THEME ALL file. Leave the pejorative out (a root does it).",
 2)
add("Tamil", "clusivity",
 "First person plural has separate inclusive (with the listener) and exclusive (without the listener) pronouns; Mohawk does the same in dual and plural, and Piraha builds the two by combining 'I'+'you' versus 'I'+'he'.",
 "naam 'we including you' / naangal 'we, not you'.",
 "CLUMSY",
 "Inclusive: ME AND YOU (but that reads as exactly two; a larger inclusive group must be US AND YOU). Exclusive cannot be said in the pronoun: US is explicitly silent, so 'we (my side, not you) will decide' needs PLAN decide AGENT US EXCEPT YOU, which really says something else (the claim does not cover you).",
 "Change one line: US = the writer's group WITHOUT the addressee; inclusive is always written with YOU (ME AND YOU for two, US AND YOU for more). Both readings then become exact with no new particle, the way Piraha composes them.",
 3)

# ---------------- Dyirbal
add("Dyirbal", "pivot: who is understood when an argument is left out",
 "Dyirbal is syntactically ergative: when clauses are chained and an argument is omitted in the later clause, it is strictly understood as the S/O of the earlier one, so omission is unambiguous. (The supplied text only says 'always syntactically ergative'; the pivot behaviour is from Dixon's description.)",
 "'Father saw mother and returned' must mean mother returned; to say father returned the first clause is antipassivised.",
 "UNDECIDED",
 "STORY PAST see AGENT F THEME M AND PAST return . is grammatical (roles are optional) but the spec does not say whether the missing role of 'return' is unstated, or carried over, or from which role. The same holds for the time particle in the second conjunct and for roles in a later sentence.",
 "State a rule. Safest for a decoder: nothing is ever inherited between clauses, a missing role is simply unsaid; to share material write it once outside a group: PAST ( come AND study ) AGENT ME, and extend the 'applies to the whole group' sentence to time, aspect, modal and to role phrases written after a parenthesised group of predicates.",
 3)
add("Dyirbal", "anticausative vs unspecified agent",
 "The avoidance style derives intransitives from transitives with one suffix (-rri-), keeping 'X broke Y' and 'Y broke' regular, and the grammar always shows whether an agent exists.",
 "yuwa 'break (something)' / yuwa-rri- 'break (of itself)'; English 'the glass broke' vs 'the glass was broken'.",
 "UNDECIDED",
 "GIVEN PAST break THEME glass . covers both 'the glass broke (by itself)' and 'someone broke the glass'; the spec never says whether an omitted AGENT means 'none' or 'not stated'. In experiment reports ('the sample was heated' vs 'the sample heated up') this matters.",
 "Rule: an omitted role is unstated, never denied. To say there was no agent write AGENT NONE; to say there was one but leave it open write AGENT SOME thing/person. Add both to the Clarifications with the glass example.",
 3)
add("Dyirbal", "reduced-lexicon register (Dyalnguy)",
 "The avoidance register kept the full grammar but a quarter of the vocabulary, each generic word standing for several everyday words, with regular derivation and paraphrase filling the gaps.",
 "One avoidance verb 'ask' covers everyday 'ask', 'invite over', 'invite to accompany'; lexical causative pairs are replaced by one root plus a regular suffix.",
 "IDEA",
 "The spec assumes 'any ordinary content word exists as a root' and offers KIND compounds and DEFINE, but sets no core/periphery split, so two writers will choose different roots for the same idea (invite vs ask KIND come).",
 "Fix a small nuclear root list and require every other root to carry a stored DEFINE in nuclear roots plus particles. The decoder and validator can then expand any text to nuclear form to compare two writers' output. Method decision, not a grammar change.",
 2)

# ---------------- Warlpiri
add("Warlpiri", "depictive secondary predication",
 "A second predicate describing a participant's state during the event is tied to that participant by matching case, so 'I ate the meat raw' and 'I ate the meat hungry' cannot be confused. (Not in the supplied text, which covers only verbs, preverbs and the auxiliary; from Hale and Simpson's descriptions.)",
 "'The man-ERG speared the kangaroo-ABS angry-ERG' = he was angry when he speared it; 'small-ABS' on the object = when it was small.",
 "UNDECIDED",
 "Three candidates and the spec picks none: AS (leave AGENT A FROM room AS angry: AS is 'capacity, role or viewpoint' and does not say whose state); NOTE on the phrase (A NOTE angry: timeless comment, not 'at that time'); WHEN { angry THEME A } (exact but heavy).",
 "Rule: a participant's state during the event is KIND or NOTE material only if permanent; a temporary co-occurring state is always WHEN { state THEME handle }. Keep AS for roles and capacities (work AS teacher). One line plus an example.",
 2)
add("Warlpiri", "preverbs and directionals",
 "A productive closed set of preverbs adds direction, manner or result to a small stock of verb roots ('run' + hiding-preverb = 'scurry into hiding'); Mohawk likewise has cislocative and translocative prefixes for 'hither' and 'thither'.",
 "wuruly-parnka- 'run into hiding'; Mohawk TRLOC in 'he will cross over again from here to there'.",
 "CLUMSY",
 "Direction is a role phrase with a relational root: run TO (inside REL shelter); go TO up; 'hither' = TO THIS place, 'away' = FROM THIS place. Works, but 'here' and 'there' have no fixed form (THIS place, root here, AT THIS).",
 "Leave directionals out as particles (roots plus TO/FROM/VIA suffice), but settle the deictic place words: one line saying 'here' = THIS place and 'there' = THAT place, or admit here/there as roots.",
 1)

# ---------------- Greenlandic
add("Greenlandic", "fourth person (reflexive third person, obviation)",
 "A special 'fourth person' marks a possessor or a subordinate-clause argument as the same individual as the main-clause subject; plain third person means somebody else.",
 "illu-ni takuaa 'he saw his own house' / illu-a takuaa 'he saw the other one's house'; Ole oqarpoq tillukkini 'Ole said I hit him (Ole)'.",
 "UNDECIDED",
 "Handles always work (see AGENT A THEME house OF A). But SELF is defined only (a) inside a modifying clause = the head, and (b) 'in a role of a main clause' = that clause's AGENT. Undefined: SELF after a linker (house OF SELF), SELF inside a plain block under say/think (the block's own AGENT or the matrix one?), and a reflexive inside a relative clause, where SELF is already taken by the head (person KIND { blame AGENT SELF THEME SELF }).",
 "Rule: SELF anywhere outside a modifying clause, including after OF / REL and inside non-modifying blocks, means the AGENT of the nearest enclosing clause that has one; inside a modifying clause it is always the head, and anything else there needs NAMED. Add the three cases as examples.",
 3)
add("Greenlandic", "experiential perfect",
 "A suffix (-nikuu-) says the event has occurred at least once in the subject's experience, distinct from a result that still holds; with negation it gives 'has never'.",
 "taku-nikuu-nngila-ra 'I have never seen it'; qia-nikuu-voq 'she has cried (I was there)'.",
 "CLUMSY",
 "'Never' is NEVER. The positive and the question are awkward: 'Have you ever used this tool?' = ASK NOT NEVER use AGENT YOU THEME T, or PAST SOMETIMES use ... DONE is glossed 'finished, result holds', which is a different meaning (I have lost my key).",
 "Add EVER to the frequency members of the aspect list (at least once in the period): ASK PAST EVER use AGENT YOU THEME T. It completes the scale NEVER / EVER / RARE / SOMETIMES / OFTEN / ALWAYS.",
 2)
add("Greenlandic", "counter-expectation inside the clause",
 "Derivational suffixes mark that an event ran against what was planned or expected: -nngitsoor- 'not after all', -galuar-/-aluar- 'was so, but (it came to nothing)'.",
 "tiki-nngitsoor-poq 'he hasn't arrived after all'; angerlar-niar-aluar-punga 'I was planning to go home, though'.",
 "CLUMSY",
 "SURPRISE is the writer's present surprise, not 'contrary to the earlier expectation'. Otherwise CONCEDE to a separately stated sentence, or DESPITE { PAST expect AGENT US THEME { arrive AGENT A } }.",
 "No new particle: add a rule that DESPITE may take the bare root 'plan' or 'expect' with nothing else (GIVEN NOT arrive AGENT A DESPITE expect = 'has not arrived after all'), and say so under DESPITE.",
 2)

# ---------------- Mohawk
add("Mohawk", "active-stative split: role of a sole participant",
 "Pronominal prefixes come in a 'subjective' set for dynamic verbs and an 'objective' set for stative verbs, so the single participant of 'run' and of 'be sick' are marked differently, by meaning.",
 "k-atorats 'I hunt' (agent set) vs sa-natahrune 'you were visiting' (patient set, stative).",
 "UNDECIDED",
 "The spec's examples use AGENT for arrive and enter, THEME for fail, big, finite, and AGENT for the experiencer of see/know/have/feel. Nothing settles die, fall, sleep, grow, wait, happen, cough, stay: die AGENT x or die THEME x? Two writers will split, and a lexicon cannot be validated without a rule.",
 "One rule in Roles: the sole participant is AGENT only if it does or controls the event (run, enter, speak, wait); otherwise THEME (fall, die, grow, exist, be-predicates). Keep the stated exception for perceivers and holders, or better, record the role frame of each root in the lexicon so the validator can check it.",
 3)
add("Mohawk", "noun incorporation",
 "A noun root absorbed into the verb names a kind of activity instead of a particular object; the incorporated noun introduces no referent that later sentences can pick up.",
 "Wa'eksohare' 'she dish-washed'; wa'kenaktahninu' 'I bed-bought'; unincorporated 'the baby ate the meat'.",
 "UNDECIDED",
 "Three renderings with no rule to choose: wash AGENT A THEME dish (bare head, number and definiteness unsaid), wash AGENT A THEME GENERIC dish (a claim about dishes in general, which is wrong here), and the phrase-predicate ( wash KIND dish ) AGENT A, which the grammar allows and is closest.",
 "Rule: an object that is not a referent (naming the activity type) goes inside the predicate with KIND: ( hunt KIND seal ) AGENT A; a THEME phrase always introduces or picks up a referent. Add one example; this also yields compact activity terms for DEFINE.",
 2)
add("Mohawk", "factual / future / optative on every verb",
 "Every event verb must take one of three pre-pronominal prefixes: factual (it happened), future (it will), or optative (it should or might, not asserted as fact).",
 "v-senatara' 'you will make a visit' / a-senatara' 'you should make a visit'.",
 "UNDECIDED",
 "PAST/FUTURE cover the first two. For the non-factual third the spec has UNREAL ('supposed world, not the actual one'), SHOULD, POSSIBLE and bare blocks, but does not say what marks a merely wished or intended event inside a block: want AGENT A THEME { go AGENT A } vs { FUTURE go } vs { UNREAL go }.",
 "Clarification: the complement block of want, hope, try, order, plan takes no time particle (unmarked = relative to the main clause, realisation unsaid); UNREAL is reserved for what is contrary to fact. One line, with want and wish as the contrasting pair.",
 2)

# ---------------- Yoruba
add("Yoruba", "default time reading of an unmarked verb",
 "The bare verb is not timeless: with an action verb it is read as completed, and only marked forms (preverbal particles) give ongoing or anterior readings; Greenlandic and Vietnamese likewise let lexical aspect and the narrative context fix time unless a particle overrides it.",
 "o na Ade 'he beat Ade' (bare = completed); with the particle n = 'is beating'.",
 "UNDECIDED",
 "Spec: unmarked = timeless, NOW = at present, no carry-over between sentences. Yet its own example 1 (GIVEN fail THEME test KIND login . = 'The login test fails') is a present observation written unmarked, and a story needs PAST on every sentence. Writers will drop NOW and PAST inconsistently and the decoder cannot tell a law from an observation.",
 "Either enforce it (a validator warning when GIVEN or STORY has no time particle and no GENERIC/HABIT), or add a frame rule: a time particle on a HEAD line or a BACKGROUND sentence sets the default for following sentences until changed, and unmarked under RECALLED/RULE/DEFINE stays timeless. Decide and fix example 1.",
 3)
add("Yoruba", "associative construction (one linker, many relations)",
 "Plain juxtaposition of two nouns covers possession, part-whole, location, contents and purpose, and the grammar admits that the rare ambiguity is left to context.",
 "fila Akande 'Akande's cap'; inu apoti 'inside of the box'; apoti aso 'box for clothes'.",
 "UNDECIDED",
 "The spec splits this three ways (KIND / OF / REL), which is better, but KIND is told to cover type, content and material at once, and purpose has no linker: 'box for clothes' is box KIND cloth (also = box made of cloth, box containing cloth) or ( box FOR cloth ) using the role inside parentheses.",
 "Rule: purpose is always ( head FOR x ), material and type are KIND, contents-as-quantity use the measure construction (see Vietnamese). If the three-way ambiguity of KIND still hurts in technical terms, split off one linker for material/contents; otherwise leave it, as Yoruba does.",
 2)
add("Yoruba", "serial verbs: result and direction of one event",
 "Several verbs in a row with shared arguments describe one event, the later verbs giving its direction, recipient or resulting state. (The supplied text only notes that serial verbs are common; the pattern is the standard West African one.)",
 "'take book come' = bring the book; 'push door open'; 'pound yam soft'.",
 "UNDECIDED",
 "Direction and recipient map to roles (TO, FROM, FOR). The resulting state has no settled home: paint THEME wall TO red? ( red ) as a second clause with RESULT? change THEME water TO ice? TO is glossed only 'recipient or end point', and naming ('call it X', 'elect her chair') has the same hole.",
 "Extend the gloss of TO: 'recipient, end point, or resulting state or identity' (heat THEME water TO vapor; cut THEME rope TO 3 piece; name THEME file TO «a.txt»). FROM then mirrors it for the starting state (change FROM red TO green).",
 2)

# ---------------- Vietnamese
add("Vietnamese", "measure nouns and classifiers",
 "A quantity is always number + unit-or-classifier + noun, the unit being a class of its own; the classifier can stand alone for the noun afterwards.",
 "mot lang thit 'one tael of meat'; bon con ga 'four (animal) chickens' ... Bon con 'four of them'.",
 "UNDECIDED",
 "A number may be followed by a unit (4 hour), and KIND 'covers content and material', so the likely form is 2 liter KIND water, whose head is 'liter', not 'water'. Rivals: water SPAN 2 liter (only legal inside parentheses), 2 «L» water. Then 'pour it (the water)' has no clean antecedent. 'Four of them' = 4 OF THAT works, since a number can be a head.",
 "Fix one construction and its head: substance stays the head, the amount is a parenthesised SPAN modifier or, simpler, a quantifier group 'number unit' before the head: 2 liter water, 5 «mg» salt, with the rule that a unit directly after a number belongs to the quantifier. State that counted items take no classifier (4 chicken).",
 3)
add("Vietnamese", "adversative vs benefactive passive",
 "The passive particle must say whether the event is good (duoc) or bad (bi) for the subject, a judgement about the affected participant, not the speaker.",
 "Tra duoc trong o Nhat Ban 'tea is grown in Japan' (favourable); Anh ta bi chong mat 'he suffers dizziness'.",
 "CLUMSY",
 "FOR marks a beneficiary. There is nothing for the party harmed or opposed: 'the update broke the build on us', 'argue against X', 'protect the data from/against loss'. GLAD and REGRET are the writer's attitude, not the participant's stake.",
 "Add one role, AGAINST (the party harmed, or what is opposed), the mirror of FOR: PAST fail THEME disk AGAINST US; vote AGAINST plan. It also removes the temptation to write FOR NOT.",
 2)
add("Vietnamese", "exhortative and proposal",
 "A preverbal exhortative particle (hay) turns a statement into an urging, and applies to the speaker's group as well as the addressee ('let's'); Greenlandic has an imperative/optative form for 'let us ..., ok?'.",
 "Anh hay an di 'go ahead and eat'; Greenlandic Qimmiit nerisitigit 'let us feed the dogs, ok?'.",
 "UNDECIDED",
 "'Let's run the tests' could be REQUEST run AGENT ( ME AND YOU ) THEME test, PLAN run AGENT ( ME AND YOU ) ..., CLAIM SHOULD run AGENT US ..., or ASK YES ... The spec defines an offer (PLAN IF { want AGENT YOU }) but not a proposal, and not a suggestion to the addressee weaker than REQUEST.",
 "Clarification, no new opener: REQUEST with an AGENT that includes ME is a proposal ('let's'); REQUEST with strength POSSIBLE is a suggestion ('you could'); PLAN stays a commitment of the writer only.",
 2)

# ---------------- Lhasa Tibetan
add("Lhasa Tibetan", "egophoric (personal) evidential",
 "A 'personal' series marks what the speaker knows from the inside, as their own intention, involvement or state, against 'testimonial' (witnessed) and 'factual' (generally known); volitional verbs take it only for one's own deliberate acts.",
 "V-pa-yin 'I did it (my own deliberate act)' / V-song '(I saw) it happened' / V-pa-red 'it is a fact that it happened'.",
 "UNDECIDED",
 "Intentions are PLAN. For the writer's own states, preferences and ignorance ('I don't know which version is installed', 'I prefer the second design', 'I am unsure') the opener is not fixed: GIVEN (observed directly?), CLAIM (asserted, no source) or RECALLED. A model writes such self-reports constantly and CLAIM wrongly labels them unsupported.",
 "Clarification: statements about the writer's own present state of knowledge, preference or intention take GIVEN ('the writer observes it directly' includes observing oneself); CLAIM is for assertions about the world offered without source. Add one example line.",
 3)
add("Lhasa Tibetan", "volitional vs non-volitional verbs",
 "Verbs divide by whether the participant controls the event, independently of transitivity: 'look' vs 'see', deliberate vs accidental 'break'; only volitional verbs have imperatives. Piraha is reported to use one verb for look/see and for die/kill.",
 "ltos shig 'look!' but no imperative of mthong 'see'; chag 'break' used both ways.",
 "CLUMSY",
 "Roots presumably split look/see, listen/hear. For the rest: 'I deleted the file by accident' = PAST delete AGENT ME THEME file WITH accident, or NOT WITH intent; the experiencer rule (AGENT for see, know, feel) means AGENT does not signal control.",
 "Do not add a particle. Fix the idiom: WITH intent / WITH NOT intent as the standard pair, and note under Roles that AGENT does not imply intention. If the Mohawk item's role rule is adopted (AGENT = controller), revisit the experiencer exception at the same time.",
 2)
add("Lhasa Tibetan", "three-way demonstratives",
 "Demonstratives distinguish near the speaker, near or known to the hearer (also the anaphoric one), and yonder; classical Tamil and Vietnamese have the same three steps.",
 "'di 'this' / de 'that' / pha-gi 'that over there'.",
 "CLUMSY",
 "THIS = present or pointed at; THAT = already identified (anaphoric). In written exchange the useful split is 'this (in my text) / that (in yours)': THIS file OF YOU, THAT line. Remote-but-present has no form.",
 "Leave out a third term (no physical scene in writing). Add only: THIS and THAT may take OF ME / OF YOU or a STEP label to say whose text or which step is meant.",
 1)

# ---------------- Tuyuca
add("Tuyuca", "five-term obligatory evidential",
 "Every statement must choose one of visual, non-visual sensory, apparent (inferred from visible traces), second-hand (told), and assumed (known from how the world generally is).",
 "The standard illustration: 'he played football' has five forms: I saw it / I heard it / I see the traces / I was told / it stands to reason.",
 "CLUMSY",
 "The opener is the same idea and is already obligatory. Mapping: visual and non-visual = GIVEN; apparent = DERIVED; assumed = RECALLED (not ASSUMED, which is supposition). The weak point is second-hand: GIVEN lumps 'a document, tool or other party shows it' with 'the writer observes it directly', so GIVEN fail THEME test cannot distinguish 'I ran it and it failed' from 'you told me it fails'. The long form GIVEN PAST say AGENT YOU THEME { fail THEME test } is exact but will be skipped.",
 "Split GIVEN: keep GIVEN for what the writer itself observes in the context (tool output, the text of a document as text), and add an opener TOLD (optionally followed by a handle for the source) for content taken on another party's word and not checked. This is the distinction a model most needs between verified and merely reported facts.",
 3)
add("Tuyuca", "inference from traces without a stated premise",
 "The 'apparent' evidential asserts something inferred from evidence the speaker perceives but does not spell out; Greenlandic -sima- does the same ('she has cried: her eyes are swollen').",
 "qia-sima-voq 'she (evidently) cried'; Tuyuca apparent form 'he played (I see the boot marks)'.",
 "UNDECIDED",
 "DERIVED is 'followed by the labels it rests on'. The spec does not say whether DERIVED with no labels is allowed (inference from unstated evidence), or whether the writer must fall back on CLAIM LIKELY or first write the evidence as a GIVEN sentence.",
 "Clarification: DERIVED with no labels = inferred from the context as a whole, grounds not listed; with labels = grounds listed. A validator can then flag label-free DERIVED in proofs but accept it in conversation.",
 2)

# ---------------- Piraha
add("Piraha", "frustrative",
 "Verb suffixes mark an action that was attempted without success, separately for failing to start it and failing to complete it; Greenlandic -galuar- is similar.",
 "Glossed in the source as 'frustration in completing an action' and 'frustration in even starting an action'.",
 "CLUMSY",
 "PAST try AGENT ME THEME { open THEME file } BUT NOT succeed ... (two clauses); 'could not even begin' = NOT CAN BEGIN open; 'did not get through' = NOT DONE open. ALMOST gives 'nearly'. No single mark for 'attempted, did not come off', which an agent reports many times a session.",
 "Add one aspect particle, VAIN (attempted; the intended result did not come about): PAST VAIN open AGENT ME THEME file. VAIN BEGIN and VAIN DONE then give the two Piraha grades for free, using the existing scope-to-the-right rule.",
 2)
add("Piraha", "old-information marker",
 "On Everett's later analysis the suffix -sai marks a clause as information already shared, not as subordinate; ASL has a topic marking for a referent 'you know'.",
 "ASL: [JOHN]tm3, IX-3rd LOVE MARY '(you know) John, he loves Mary'.",
 "CLUMSY",
 "Shared status can be shown for a referent (THAT) and for a presupposed property (KIND { }), but not for a whole statement: 'as you know / as noted, the cache is cold' must be know AGENT YOU THEME { ... }, or RESTATE with a label if it was said in this text. BACKGROUND says 'sets the scene', not 'you already have this'.",
 "Add an attitude-slot particle SHARED (the writer takes the addressee to know or accept this already). It is the positive twin of the existing relation REBUT (denies what the addressee is presumed to think) and marks premises that need no defence.",
 2)
add("Piraha", "parataxis instead of embedding",
 "Piraha is claimed to avoid all embedding and recursion: 'John's brother's house' is said as 'John has a brother. This brother has a house.', each clause a separate sentence linked by reference.",
 "'He knows how to talk about making arrows' needs more than one sentence.",
 "IDEA",
 "The spec permits unbounded nesting of { } and ( ), and its own text concedes that SELF breaks down when clauses nest. It also already has everything a flat style needs: labels, STEP n, handles, NAMED.",
 "Add a style rule enforced by the validator: at most two levels of { } in a sentence; a block that would go deeper becomes its own labelled sentence and is referred to as STEP n. Costs nothing in expressive power and makes decoding and checking easier.",
 2)

# ---------------- ASL
add("American Sign Language", "frame-setting topic",
 "A topic can be set up that is not an argument of the clause at all but the frame within which it holds, marked differently from a fronted argument.",
 "[MEAT]topic, I LIKE LAMB 'as for meat, I prefer lamb'; [VEGETABLE]topic, JOHN LIKE CORN.",
 "UNDECIDED",
 "TOPIC is a focus-slot particle and so must sit on a role phrase of the clause. A frame topic has no role unless ABOUT ('topic, field or respect') is used: like AGENT ME THEME lamb ABOUT meat. Whether to write ABOUT meat, ABOUT TOPIC meat, or a BACKGROUND sentence is open.",
 "Rule: TOPIC marks an argument as what the sentence is about; a frame that is not an argument is an ABOUT phrase, with no TOPIC needed. Add the meat/lamb pair as an example.",
 2)
add("American Sign Language", "iteration and verbal number",
 "Verb modulation distinguishes how many times and in what rhythm an event recurs (iterative, frequentative, incessant) and reduplication marks the action as done separately to each of several recipients.",
 "'get sick over and over', 'be sick often'; GIVE repeated across loci = 'give to each of them'.",
 "UNDECIDED",
 "Per-recipient vs joint is covered well by ALL vs WHOLE and EACH. Qualitative frequency is covered (OFTEN, AGAIN ...). An exact count or rate is not: 'ran the test 5 times', 'retry at most 3 times', 'fails about 1 run in 10', 'twice a week' could be SPAN 5 time, a quantified THEME (5 run), or « » notation.",
 "Rule: the number of occurrences is a SPAN phrase with the root 'time' (PAST run AGENT ME THEME test SPAN 5 time; REQUEST retry SPAN ATMOST 3 time); a rate is that phrase plus a second unit inside parentheses or « » ( SPAN «2/week» ). Add 'count of occurrences' to the gloss of SPAN.",
 3)
add("American Sign Language", "dispositional aspects",
 "Separate aspect forms say that the subject is prone to the state or gets into it easily, as distinct from being in it often or habitually.",
 "'to be sickly, prone to get sick' (predispositional); 'to get sick easily' (susceptative) vs 'to be often sick' (frequentative).",
 "CLUMSY",
 "HABIT and OFTEN report occurrences; CAN is 'able, or possible in fact'; LIKELY is the writer's confidence. A disposition that may never have shown itself ('this glass breaks easily', 'the query tends to time out under load', 'sodium reacts readily') has to be CAN break WITH ease or a root (tend AGENT ...).",
 "Add one modal, TEND (disposed to; happens readily when conditions allow), beside CAN. It is about the world, so it fits the modal slot, and it is common in scientific prose.",
 2)
add("American Sign Language", "progressive change of degree",
 "An 'increasing' aspect shows a state intensifying over time, and an inchoative shows entry into the state, both distinct from simply being in it.",
 "'to get more and more sick'; 'to get sick' vs 'to be sick'.",
 "UNDECIDED",
 "Entry into a state is BEGIN sick. 'More and more' is probably ONGOING MORE sick THEME A, but MORE with no THAN is only said to 'stand alone when the standard is not stated'; whether the implied standard is 'than before' or 'than others' is not fixed. 'Rose by 5 percent' = MORE high SPAN 5 «%» has the same doubt.",
 "Clarification: MORE/LESS with a time or aspect particle and no THAN compares with the same thing earlier (ONGOING MORE = increasingly; PAST MORE high SPAN x = rose by x); comparison across things needs THAN or a preceding CONTRAST.",
 2)
add("American Sign Language", "referent loci",
 "A referent is assigned a point in space once and is then referred to by pointing; verbs move between points to show who does what to whom, and in practice signers keep no more than about eight points alive.",
 "Set up DOG on the left and CAT on the right; SEE moving left-to-right = 'the dog sees the cat'.",
 "IDEA",
 "Handles with NAMED are the same device and are the spec's answer to third-person pronouns, obviation and logophoricity. The spec lets handles 'live until rebound' with no limit and no way to end one, and offers THAT as a looser alternative that fails with two candidates.",
 "Two usage rules from signing practice: (1) when more than one referent of a kind is active, THAT is not allowed, use handles; (2) keep few handles live and re-anchor a handle (phrase NAMED X again) after a long gap or a new HEAD. Both are validator-checkable.",
 2)

# ---------------- Hungarian
add("Hungarian", "answers to yes-no questions",
 "A yes-no question is normally answered by repeating the verb or its particle, or by negating the questioned part, not by a bare yes or no, so the polarity of the answer is never in doubt.",
 "Elment? - El. 'Has he left? - (He has) left.' / Nem ment el. 'He has not left.'",
 "UNDECIDED",
 "ANSWER n YES / NO are bare fragments. After a negative or biased question (ASK NOT PAST send AGENT YOU THEME file . or ASK NO ...) the spec does not say whether YES means 'the sentence as written is true' (I did not send it) or 'the positive is true' (I did send it). English itself wavers, so the decoder will too.",
 "Rule: YES and NO always answer the body exactly as written, negation included (YES to ASK NOT send = it was not sent). Recommend the Hungarian habit for negated questions: answer with the predicate fragment (ANSWER 1 NOT send).",
 3)
add("Hungarian", "interrogative paradigm",
 "Question words form a regular grid: who, what, which, what kind of, how many, how much, where / where to / where from, each taking the ordinary case endings.",
 "ki 'who', mi 'what', milyen 'what kind', hany 'how many', mennyi 'how much', hol / hova / honnan.",
 "UNDECIDED",
 "Mostly covered and regular: WHAT person, WHAT thing, AT WHAT / TO WHAT / FROM WHAT, x KIND WHAT (what kind), WHAT in the degree slot (how much). But the quantifier-slot WHAT is glossed 'how many / which', so ASK fail THEME WHAT test . is both 'which test fails?' and 'how many tests fail?'. Bare WHAT also does not separate who from what.",
 "Rule: quantifier WHAT = which; how many = WHAT MANY (WHAT as degree on the quantifier, parallel to its degree-slot use); how much of a substance = WHAT MUCH or WHAT before the unit (WHAT liter water). Bare WHAT = what; who = WHAT person.",
 3)
add("Hungarian", "time distance and deadlines",
 "Dedicated endings and postpositions give 'ago', 'in ... time', 'by (a deadline)', 'within', and 'for ... up to now', each distinct from plain duration.",
 "10 evvel ezelott 'ten years ago'; 2 het mulva 'in two weeks'; -ra 'by (a time)'; -n belul 'within'; 3 eve lakom itt 'I have lived here for 3 years'.",
 "UNDECIDED",
 "PAST NEAR / FAR are only qualitative. 'Ten years ago' needs WHEN ( before REL now SPAN 10 year ), but NOW is a time particle, not a legal head, and a clause-level SPAN would instead mean the event lasted ten years. 'By Friday' is WHEN before REL friday (loses 'at the latest'); 'within 2 hours' collides with duration SPAN ATMOST 2 hour.",
 "Let a measure follow PAST or FUTURE where NEAR / FAR go: PAST ( 10 year ) move AGENT A = moved ten years ago; FUTURE ( 2 week ) = in two weeks. Admit NOW as a head for REL (before REL NOW). Rule: deadline = WHEN ATMOST x ('no later than'), reusing the number bound particles on time points.",
 3)
add("Hungarian", "contrastive topic vs exhaustive focus",
 "The slot before the verb is an exhaustive focus ('X and nothing else'), a fronted phrase is a topic, and a stressed topic implies a contrast with other topics left open; a sentence may have several topics but one focus.",
 "A viragokat EVA szereti 'flowers: it is Eve who likes them (others may like other things)'; Ket konyvet tegnap elvitt Janos 'two books he did take (whatever else he did not)'.",
 "CLUMSY",
 "TOPIC, FOCUS and ONLY exist and can sit on different phrases of one clause, and FOCUS before the predicate with REBUT gives verum focus ('she DOES like them'): well covered. Missing: the unit takes only one focus-slot particle, so a contrastive topic (TOPIC + FOCUS on the same phrase) cannot be written, and nothing limits a clause to one FOCUS.",
 "Allow TOPIC to combine with one other focus particle on the same unit (TOPIC FOCUS book = 'the books, at least'); state that a clause has at most one FOCUS or ONLY outside parentheses. Low cost; mainly for careful hedged claims.",
 1)

for it in I:
    assert it["status"] in ("CLUMSY","GAP","UNDECIDED","IDEA")
    assert it["priority"] in (1,2,3)
out = sys.argv[1]
json.dump({"items": I}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(I), Counter(i["status"] for i in I), Counter(i["source"] for i in I), Counter(i["priority"] for i in I))
