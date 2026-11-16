import json
I=[]
def it(source,category,what,example,status,how_now,suggestion,priority):
    I.append(dict(source=source,category=category,what=what,example=example,status=status,how_now=how_now,suggestion=suggestion,priority=priority))

it("2.1.1.2.1.2, 2.1.1.2.2.2 subject that is not an agent","role choice",
 "The spec does not say whether the single argument of an uncontrolled event, or a non-acting transitive subject, is AGENT or THEME.",
 "I fell; the patient died; the wind broke the window; the key opened the door",
 "UNDECIDED","spec has both 'arrive AGENT A' and 'fail THEME test'; states take AGENT for the holder; wind could be AGENT, CAUSE or WITH",
 "One rule: AGENT only for a participant that acts with control (plus experiencers/holders of states); every other sole argument is THEME; forces are CAUSE, instruments WITH. Then fall AGENT x = deliberately, fall THEME x = by accident.",3)
it("2.1.1.2.8, 2.1.1.2.12 objects governed by verbs and adjectives","role frames",
 "No rule or lexicon field fixes which role a root's second argument takes, so writers will pick different roles for the same root.",
 "help him, wait for her, depend on X, afraid of dogs, proud of it, good at chess, different from B",
 "UNDECIDED","help THEME x / help TO x / help FOR x all look legal; different THAN x or FROM x",
 "Give every root in the lexicon a role frame (the roles it takes and what each means), checked by the validator; default second argument = THEME, ABOUT for subject matter.",3)
it("2.1.1.2.9.4 become; 2.1.3.1.2.1; 2.2.2.3 verbs from adjectives","state vs change vs caused change",
 "A property root as predicate can be read as a state, a change into the state, or causing the state, and the spec only defines the first.",
 "the door is open / the door opens / she opens the door; he became a soldier",
 "UNDECIDED","open THEME door (state); BEGIN open THEME door probably = becomes open; open AGENT A THEME door is unlicensed and clashes with 'holder of a state is AGENT'",
 "State it: bare property root = state; BEGIN + root = become; causing needs the cause-to affix (or a CAUSE phrase), never a bare added AGENT. 'Become N' = BEGIN N THEME x.",3)
it("2.1.1.2.10, 2.1.1.2.11 subject- and object-complement","secondary predicate",
 "There is no stated way to give the resulting or attributed property of the THEME in the same clause.",
 "we made him king; they painted the door red; I consider it wrong; she was elected chair",
 "UNDECIDED","block: consider THEME { wrong THEME it }; AS for roles (appoint THEME him AS general); result of 'paint ... red' could be AS, TO or WITH",
 "Rule: attributed or resulting state always goes in AS (paint THEME door AS red; call THEME it AS error); judgements of a whole proposition use a block.",2)
it("2.1.1.3.3-4 gerund and nominalization; 2.1.1.4.8b reference quality; 2.2.1.2, 2.2.1.3","root as head",
 "It is undecided what a non-thing root means in head position (act, result, doer, quality, or the thing that has the quality) and how ( ) with roles differs from a { } block.",
 "John's refusal of the offer; the size of the file; the building; the destruction took three days",
 "UNDECIDED","refuse OF John? (refuse AGENT John THEME offer)? { refuse AGENT John THEME offer }? big OF file = size or 'the big one'?",
 "Rule: an act root as head = the act/event; a property root as head = the property itself; { } = the proposition/fact; all other readings (doer, product, tool, place, dimension) need a derivational affix. 'The big one' = THAT KIND big.",3)
it("2.1.1.4.1, .3, .11, .13, 2.1.1.5 general; rule 'a role may appear once per clause'","merged roles",
 "Several roles each merge two meanings but may occur only once per clause, so a clause that needs both meanings must force them into one AND-phrase.",
 "I bought it for Bill for his birthday; send the file to Ana to Paris; cut it carefully with a knife",
 "CLUMSY","FOR (Bill AND birthday); WITH (knife AND care) - the AND wrongly makes them the same kind of thing",
 "Allow a role to repeat when its fillers are of different sub-kinds, or split the three busiest pairs (beneficiary/purpose, recipient/end point, means/manner).",3)
it("2.1.1.4.3a, 4a, 5a, 11a negative instrumental, comitative, circumstance, manner","without",
 "The meaning 'without X' has no fixed form: NOT before a role's phrase can mean 'without X' or 'with something other than X'.",
 "I hit it without a hammer; I went without Bill; he did it without care",
 "UNDECIDED","WITH NOT hammer / WITH NONE hammer / ALONG NOT Bill",
 "Fix: role + NOT phrase = without (no such participant); role + OTHER ... = a different one.",2)
it("2.1.1.4.5 circumstance; 2.1.1.4.8 quality; 2.2.3.1 adjectives from nouns (having)","having-linker",
 "There is no linker for 'that has X' (the inverse of OF), which technical description uses constantly.",
 "a man with dirty hands; a function with two arguments; a list with no duplicates",
 "CLUMSY","function KIND { have AGENT SELF THEME 2 argument }",
 "Add one linker HAVING (inverse of OF): function HAVING 2 argument; list HAVING NONE duplicate. This also replaces 'having' and 'lacking' affixes.",3)
it("2.1.1.4.6.3 present vs past possession; nominal tense","time on a modifier",
 "Time particles cannot stand in a modifier, so 'former', 'then', 'future' need a full relative clause.",
 "the former owner; my future manager; the old value",
 "CLUMSY","person KIND { PAST own AGENT SELF THEME house }",
 "Let a modifier carry a time particle: owner KIND PAST; value KIND PAST; manager KIND FUTURE.",2)
it("2.1.1.4.9 quantity; 2.1.1.4.21 value; 2.1.1.4.23 extent","measurement statement",
 "There are at least three ways to say that something measures so much, and none is named as the standard one.",
 "the sample weighs 5 kg; a boat of a thousand tons; a table worth five pounds; the run took 3 s",
 "UNDECIDED","heavy THEME S SPAN 5 «kg» / EQUAL THEME weight OF S THAN 5 «kg» / boat KIND (1000 ton)",
 "Canonical: dimension root + SPAN measure (heavy THEME S SPAN 5 «kg»), read as neutral (no claim that S is heavy); attributive: boat KIND (heavy SPAN 1000 ton).",3)
it("2.1.1.4.9a reference quantity","measure of substance",
 "It is unclear whether the unit or the substance is the head in a measured amount.",
 "a pound of sugar; three cups of water; 20 lines of code",
 "UNDECIDED","1 pound KIND sugar / 1 pound sugar (number + unit as quantifier) / sugar KIND (1 pound)",
 "Rule: number + unit is a quantifier, substance is the head: 3 cup water, 5 «ml» acid.",2)
it("2.1.1.4.18 part-whole; REL vs OF","OF vs REL",
 "The spec does not say which roots are relational (take REL) and which take OF, nor the difference between 'top OF tree' and 'top REL tree'.",
 "the top of the tree; Ana's friend; the author of the file; the cause of the error; a member of the set",
 "UNDECIDED","friend REL Ana (spec) but file OF user; top OF tree or top REL tree; cause OF / REL error",
 "Mark relational roots in the lexicon. Rule: OF = a part or possession of the whole; REL = something defined by its relation to a separate landmark (top OF tree = the treetop, top REL tree = the space above it).",3)
it("2.1.1.4.19.1, .3, .5 partitive numeral and quantifier","partitive",
 "Selecting some of an already identified set works only when the selector is a number, because quantifiers cannot be heads.",
 "three of the ten tests; some of the boys; none of them; most of these files",
 "UNDECIDED","3 OF (THAT 10 test) works; SOME OF (THAT boy) is not grammatical; SOME THAT boy has no defined reading",
 "Rule for stacked quantifiers: the left one selects from the set fixed by the rest: SOME THAT boy, 3 THAT 10 test, NONE THAT 2 (neither).",3)
it("2.1.1.4.20 price; 2.1.5.1 other adpositions (instead of, in exchange for)","exchange and substitution",
 "No role marks the thing given in exchange or the thing replaced; INSTEAD marks only the chosen item.",
 "I bought it for two pounds; use tabs instead of spaces; replace X with Y",
 "GAP","cannot in one clause; two clauses: use THEME tab AND NOT use THEME space",
 "Add one role (gloss SWAP): the thing given up, replaced or paid: use THEME tab SWAP space; buy THEME it SWAP 2 pound.",3)
it("2.1.1.4.25 inclusion; 2.1.1.4.26 exclusion","including / such as",
 "A non-exhaustive mention of members inside a phrase is not possible: NOTE means 'namely' (exhaustive), EXAMPLE works only between sentences, and EXCEPT is a clause role, not attached to its phrase.",
 "everyone including John; sugars such as glucose; all tests except login read all files except config",
 "GAP","separate EXAMPLE sentence; NOTE (ALSO John) is a guess; two EXCEPTs in one clause are impossible",
 "Add a linker INCLUDING (non-exhaustive members) and let EXCEPT also be used as a linker after the phrase it limits.",3)
it("2.1.1.4.29 citation form","mention of a word",
 "There is no way to mention a native word or particle as a word rather than use it.",
 "the word 'test' has two senses; the particle NOT comes first",
 "UNDECIDED","« » is for foreign text only; DEFINE takes a term but ordinary mention is unspecified",
 "Parallel to 'name root': a marker meaning 'the word itself', e.g. word root, with « » for longer native quotations.",2)
it("2.1.1.4-6 note (b) copular complement and (c) attributive use; 2.1.1.2.3","locative and possessive predication",
 "With no 'is' and a predicate that must be a root, it is unclear how to predicate a place, time or owner, or how to attach a role phrase to a noun.",
 "the file is in the folder; the meeting is at nine; the book is Ana's; the book on the table",
 "UNDECIDED","exist THEME file AT inside REL folder / (inside REL folder) THEME file; book KIND (top REL table)",
 "Allow a role phrase in ( ) as predicate and as modifier: (AT inside REL folder) THEME file; book KIND (AT top REL table); (OF Ana) THEME book.",3)
it("2.1.1.5 motion to/from; 2.1.3.6.10.7 other directionals","direction without landmark",
 "Direction of motion with no landmark, and 'toward' as opposed to 'as far as', have no stated form.",
 "go up; move back; walk toward the city; scroll down",
 "UNDECIDED","TO up? WITH up? TO toward REL city?",
 "Rule: a relational root with no REL after TO/FROM/VIA is a pure direction (go TO up); TO = reaching the end point, TO (toward REL city) = direction only.",2)
it("2.1.1.4.4 comitative vs 2.1.1.5.21-26 'along'","gloss name",
 "The particle glossed ALONG means companion, while English 'along' is a path, so a writer working from the gloss will misuse it for paths.",
 "walk along the river vs walk with Bill",
 "IDEA","ALONG Bill (companion); VIA along REL river (path)",
 "Rename the gloss to COMPANION (or ACCOMPANY) so no particle gloss collides with a needed relational root.",2)
it("2.1.1.6.1.1-5 clock time, weekday, month, year","dates and times",
 "The notation for clock times and calendar dates is not fixed; the spec's own 'day KIND five' and 'before REL 9' are ambiguous.",
 "at 7 o'clock; on Monday; in January 1976",
 "UNDECIDED","WHEN 9 / WHEN «07:00» / WHEN day KIND five / roots for weekday and month names",
 "Dates and clock times always in « » ISO form (WHEN «1976-01», WHEN «07:00»); weekdays and months as unit root + ORD (weekday ORD 1).",2)
it("2.1.1.6.3, .4, .12, .13 punctual-future, punctual-past, point in period","time distance from now",
 "'Ago', 'in two hours' and 'within the last hour' need a deictic 'now' landmark that the spec does not provide as a head.",
 "I was here two hours ago; back in two hours; five calls in the last hour",
 "UNDECIDED","WHEN (before SPAN 2 hour REL ?now) - NOW is a time particle, not a head; SPAN alone would mean duration",
 "Generalise NEAR/FAR: a measure may follow PAST or FUTURE (PAST 2 hour = two hours ago; FUTURE 2 hour = in two hours; PAST ATMOST 1 hour = within the last hour).",3)
it("2.1.1.6.6-9 until, since, from ... on","temporal bounds",
 "Start and end of a period can be said with WHEN + relational root or with FROM/TO, and the spec does not choose.",
 "since Monday; from Monday to Friday; until the release",
 "UNDECIDED","WHEN since REL monday / FROM monday TO friday / WHEN until REL release",
 "Allow FROM and TO for time bounds as for space, keep WHEN for the point or frame; drop 'since' and 'until' from the relational roots.",2)
it("2.1.1.6 note on tense restrictions; 2.1.3.2.1.1-2 universal and present tense","unmarked tense",
 "Unmarked is defined as timeless, yet the spec's first example uses it for a present observation, and nothing says whether tense is needed when WHEN gives the time or in every STORY sentence.",
 "the login test fails (now) vs login tests fail (always); yesterday he left",
 "UNDECIDED","'GIVEN fail THEME test KIND login' = fails now, contrary to the rule; PAST must be repeated in each narrative sentence",
 "Rule: unmarked = timeless only under RECALLED/RULE/DEFINE and with GENERIC; under GIVEN it is the time of observation; an absolute WHEN makes PAST/FUTURE optional.",3)
it("2.1.1.11 indefiniteness; 2.1.6.6 quantifiers","meaning of SOME",
 "SOME is not defined as 'at least one, possibly all' or 'some but not all', which matters for inference.",
 "some tests fail (do all fail?)",
 "UNDECIDED","SOME test",
 "Define SOME = at least one, no claim about the rest; 'not all' is written NOT ALL; 'a few' is SEVERAL or FEW.",3)
it("2.1.1.12 referential vs nonreferential indefinite","specific vs any",
 "A particular but unidentified referent is not clearly distinguished from 'some or other'.",
 "I am looking for a (certain) book vs any book",
 "UNDECIDED","ANY book (nonspecific) vs SOME book / 1 book / book NAMED B",
 "State that a phrase with NAMED or a number is specific, ANY is nonspecific, bare is open.",2)
it("2.1.2.1.1.1-2 obligatory vs optional pronouns; 2.1.3.1.2.2","omitted role",
 "The spec does not say whether a missing role means 'unspecified someone/something' or 'the one understood from context'.",
 "Has the release been sent? / He ate. / (dialogue) Sent.",
 "UNDECIDED","ASK DONE send THEME release (agent unknown) - but a writer may also drop a known agent",
 "Rule: an omitted role is always unspecified, never a hidden pronoun; known referents need a handle, THAT, ME or YOU. Fragments only after ASK, SOCIAL, HEAD.",3)
it("2.1.2.1.3 inclusive vs exclusive first person","exclusive we",
 "Inclusive 'we' has a form (ME AND YOU) but exclusive 'we' has none.",
 "we (not you) have decided",
 "CLUMSY","ME AND OTHER person / US plus a second clause",
 "Document US EXCEPT YOU (if EXCEPT becomes a linker) or leave as is.",1)
it("2.1.2.2 reflexive; 2.1.2.4.7 reflexive possessive; control complements","reach of SELF",
 "SELF is defined for a role of a main clause with an AGENT and for relative clauses, but not inside a phrase, in a clause with no AGENT, or in a complement block.",
 "the file refers to itself; she washed her own hands; A wants to go; A says he (A) will win",
 "UNDECIDED","refer THEME file TO SELF (no AGENT); hand OF SELF; want AGENT A THEME { go AGENT A } repeats the handle",
 "Rule: outside a modifying clause SELF = the AGENT of the nearest clause, else its THEME, at any depth inside that clause's phrases; in a complement block SELF = that same participant (want AGENT A THEME { go AGENT SELF }).",3)
it("2.1.2.5.1.25 other demonstrative parameters; 2.1.1.2.12","same / different / such",
 "'The same X' and 'such X' as modifiers have no stated form; only OTHER exists.",
 "A and B call the same function; the same error as yesterday; such errors",
 "UNDECIDED","function KIND EQUAL? call THEME 1 function? error KIND (THAN THAT)",
 "Add quantifier SAME as the partner of OTHER (SAME function; SAME error THAN ...); 'such' = KIND THAT.",3)
it("2.1.2.6.1.1.2 selective interrogative; 2.1.2.6.2","which vs how many",
 "WHAT in the quantifier slot means both 'which' and 'how many'.",
 "which tests failed? / how many tests failed?",
 "UNDECIDED","fail THEME WHAT test (both readings)",
 "WHAT before the head = how many only; which = head KIND WHAT (already used in the spec's fragment example).",3)
it("2.1.3.1.2.1 intransitive from transitive by not specifying the subject","spontaneous vs agentless",
 "'It happened by itself' and 'someone unnamed did it' are written the same way.",
 "the water boiled / the water was boiled; the process stopped / was stopped",
 "CLUMSY","boil THEME water for both; add CAUSE SELF or AGENT NONE to force 'by itself'",
 "Falls out of the state/change rule: bare root = happens with no causer implied; root + cause-to with no AGENT = someone did it.",2)
it("2.1.3.1.3 causative of intransitive, transitive, ditransitive","causative by role",
 "The CAUSE role already makes a causative of any clause without a second AGENT, so clause-level causation needs no new device.",
 "the heat melted the ice; the patch made the test fail; I made him eat",
 "IDEA","cause AGENT ME THEME { eat AGENT A THEME fish } or eat AGENT A THEME fish CAUSE ME",
 "Declare CAUSE + phrase the standard causative for events; keep the cause-to affix only for building lexical words (kill, heat, teach, show).",3)
it("2.1.3.2.1.3.2, 2.1.3.2.1.4.3 relative tenses","stacked time particles",
 "Whether two time particles may stack in a main clause for future-in-past or past-in-future is not stated, though the scope rule implies it.",
 "he was going to leave; it will have finished",
 "UNDECIDED","PAST FUTURE leave / FUTURE DONE finish / FUTURE PAST finish - implied only",
 "State it: the first time particle sets the reference time, the next is counted from it.",2)
it("2.1.3.3.1.3.2 experiential perfect; 2.1.3.3.2.1.8-9 iterative, semelfactive; 2.1.6.5 numeral derivatives","number of occurrences",
 "No role or slot gives how many times something happens, nor 'ever / at least once'.",
 "the test failed 3 times out of 10; have you ever seen it; twice a week",
 "GAP","SPAN 3 time (stretching SPAN) or a count predicate on a nominalised event",
 "Let a number + TIMES stand in the aspect group: PAST 3 TIMES fail; ATLEAST 1 TIMES = ever; rates as 2 TIMES SPAN week.",3)
it("2.1.3.3.2.1.3 habitual","usually / typically",
 "'Usually' or 'by default' falls between OFTEN and ALWAYS and it is unclear whether HABIT carries it.",
 "the service usually restarts within a minute",
 "UNDECIDED","HABIT restart / OFTEN restart / GENERIC on the noun",
 "Define HABIT as 'as a rule, exceptions allowed' (the clause partner of GENERIC).",2)
it("2.1.3.4.3.1 imperative persons; 2.1.3.4.10 hortatory","let's / suggestion",
 "A proposal for joint action has no fixed opener.",
 "let's run the tests first; shall we stop here?",
 "UNDECIDED","REQUEST run AGENT (ME AND YOU) / PLAN ... AGENT US / ASK SHOULD ...",
 "State: REQUEST with AGENT (ME AND YOU) = let's; a mere suggestion = CLAIM SHOULD.",2)
it("2.1.3.4.4 optative","hope and wish",
 "A wish or hope needs a full 'hope' clause; the attitude list has GLAD and REGRET, which presuppose the fact.",
 "hopefully the build passes; if only it had worked",
 "CLUMSY","CLAIM hope AGENT ME THEME { FUTURE pass THEME build }",
 "Add attitude HOPE (wanted, not known to be so); with UNREAL it gives 'if only'.",2)
it("2.1.3.4.11 monitory","warning",
 "There is no marked way to warn, which an assistant does often.",
 "careful: this deletes all data; it may break if you upgrade",
 "UNDECIDED","CLAIM EMPHASIS delete ... / REQUEST careful AGENT YOU CAUSE { ... }",
 "Add attitude WARN (the addressee should take care about this), or a relation of the same name.",3)
it("2.1.3.4.6.1 kinds of obligation; 2.1.3.4.7","necessity vs obligation",
 "CAN covers both ability and factual possibility, but MUST is defined only as 'required', so factual or logical necessity has no clear form.",
 "the list must be sorted for binary search to work; a prime above 2 must be odd; the function needs two arguments",
 "UNDECIDED","MUST (rule?) / CERTAIN (writer's confidence) / root need",
 "Define MUST as the dual of CAN: required by a rule or necessary in fact; the source goes in CAUSE or FOR ('needed for').",3)
it("2.1.3.4.9 authority for assertion","appearance",
 "Inference from appearance, with no earlier sentence to cite, fits neither GIVEN nor DERIVED.",
 "it seems the cache is stale; apparently he left",
 "UNDECIDED","LIKELY ... / DERIVED with no labels / root seem with a block",
 "Allow DERIVED with no labels to mean 'inferred from what is seen, grounds unstated'.",2)
it("2.1.3.7 strings of verbs; body = clause AND clause","shared arguments and particle scope",
 "It is undecided whether roles and pre-predicate particles of the first clause carry over to clauses joined by AND/OR/BUT.",
 "A took the file and deleted it; he came, saw and left",
 "UNDECIDED","PAST take AGENT A THEME F AND PAST delete AGENT A THEME F (full repetition) - or does PAST reach across AND?",
 "State that nothing carries across AND between clauses, and that a coordinated predicate shares everything: PAST (take AND delete) AGENT A THEME F (already grammatical).",3)
it("2.1.4.4.3.1 superlative compared to other entities","comparison set",
 "The set a superlative ranges over has no assigned role.",
 "the fastest of the three runs; the largest file in the folder",
 "UNDECIDED","MOST fast THEME R THAN? / OF? / among REL (ALL 3 run)",
 "Rule: with MOST/LEAST, THAN names the comparison set (MOST fast THEME R THAN ALL 3 run); attributive: file KIND (MOST big) OF folder.",3)
it("2.1.4.4.3.4 other kinds of comparison","covariation",
 "'The more X, the more Y' and 'Y grows with X' have no direct form.",
 "the larger the input, the slower the run; pressure rises with temperature",
 "CLUMSY","IF { MORE big THEME input } { MORE slow THEME run }",
 "Bless that IF { MORE } { MORE } pattern as the standard form, with a factor allowed (2 MORE); exact laws go in « ».",3)
it("2.1.4.4.3.4, 2.1.7.1.4 other kinds of comparison","as X as possible",
 "The maximal-degree-within-limits meaning has no stated form.",
 "as soon as possible; as small as it can be",
 "UNDECIDED","MOST early? (EQUAL early THAN { CAN })?",
 "Rule: MOST + root with THAN { CAN } omitted is plain superlative; write CAN MOST early for 'as early as possible'.",2)
it("2.1.4.5.4 other degrees","so ... that",
 "A degree defined by its actual result needs two sentences or loses the degree link.",
 "the file is so big that the upload failed",
 "CLUMSY","VERY big THEME file . RESULT PAST fail THEME upload .",
 "State that ENOUGH/TOO ... FOR { block with real time } asserts the result (ENOUGH big FOR { PAST fail THEME upload }).",2)
it("2.1.5.1 other adpositions","against",
 "Opposition ('against') has no role and FOR has no stated negative.",
 "vote against the plan; protect against loss; lean against the wall",
 "UNDECIDED","FOR NOT plan? THEME? a relational root?",
 "Fix THEME for the thing opposed (oppose THEME plan; protect THEME data FROM loss) and record it in the role frames; no new role.",2)
it("2.1.5.1 other adpositions (of); 2.1.2.7 relative words","content clause on a noun",
 "A block modifier is described only as a relative clause with SELF; the reading with no SELF (content) is not stated.",
 "the assumption that the list is sorted; the fact that it failed; the risk of losing data",
 "UNDECIDED","assume KIND { sorted THEME list }",
 "State: KIND + block with no SELF gives the content of the head.",2)
it("2.1.6.1 numerals; 2.1.6.5 derivatives of numerals","non-integers",
 "number = digits only, so decimals, negatives, fractions and percentages have no defined place in quantifier or number slots.",
 "30% of users; half the files; 3.5 times faster; -2",
 "UNDECIDED","«30%» OF user? «0.5» file? AROUND «3.5»?",
 "Let number include decimal, sign, fraction and percent forms; a fraction or percent before a head is partitive (30% THAT user; 1/2 file).",3)
it("2.1.6.4 ordinals","last, next, nth from the end",
 "ORD n counts only from the start and there is no ordinal for last, next, previous or 'second largest'.",
 "the last line; the next step; the second largest value",
 "UNDECIDED","roots last / next REL x; ORD 2 with (MOST big)?",
 "ORD LAST, ORD LAST 2 (second from end); next/previous as relational roots; ORD 2 before MOST = second largest.",2)
it("2.1.6.6 quantifiers; 2.1.4.4 comparison","degree on a quantity",
 "Degree particles may stand only before a predicate or modifier, so comparative and excessive quantities, 'almost all', and strict 'more than n' cannot be written in the quantifier slot.",
 "more errors than yesterday; too many files; enough memory; almost all tests; more than 5 seconds",
 "GAP","predicate on a count: MORE big THEME count OF error THAN ...; ATLEAST 6 only works for whole numbers",
 "Allow {degree} before a quantifier or number: MORE MANY error THAN ..., TOO MANY file, ENOUGH memory, ALMOST ALL test, MORE 5 second, 2 EQUAL MANY.",3)

counts={"NA":176,"COVERED":202}
for s in ["CLUMSY","GAP","UNDECIDED","IDEA"]:
    counts[s]=sum(1 for x in I if x["status"]==s)

functions=[
 {"q":"2.2.1.1 nouns from nouns","subtypes":"collective (group of), member/unit, person associated with, place of, abstract status (-hood, -ship), diminutive/augmentative, female/male/young, opposite/non-","handled_by":"group-of, one-who, place-of, quality-of, opposite; size and sex by KIND + root; non- by NOT"},
 {"q":"2.2.1.2 nouns from verbs","subtypes":"act/event, doer, thing done or produced, instrument, place, manner","handled_by":"bare root as head = act; one-who, thing-done, tool-for, place-of; manner = way KIND { }"},
 {"q":"2.2.1.2.1 / 2.2.1.3.1 syntax of derived nouns","subtypes":"keeps clause roles or takes noun linkers","handled_by":"undecided: ( root + roles ) keeps roles; affixed words should take OF/KIND only"},
 {"q":"2.2.1.3 nouns from adjectives","subtypes":"abstract quality, neutral dimension (length, age), one that is X","handled_by":"quality-of; 'the X one' = THAT KIND x"},
 {"q":"2.2.1.4-5 nouns from adverbs/other","subtypes":"marginal","handled_by":"none needed (no adverb class)"},
 {"q":"2.2.2.1 verbs from nouns","subtypes":"use as tool, provide with, remove, act as, turn into","handled_by":"no affix: roots are classless (hammer THEME nail); turn into = cause-to; act as = AS"},
 {"q":"2.2.2.2 verbs from verbs","subtypes":"causative, anticausative, reversive, repetitive, reciprocal, reflexive, attempt","handled_by":"cause-to, opposite; AGAIN, MUTUAL, SELF, omission of AGENT, root try"},
 {"q":"2.2.2.3 verbs from adjectives","subtypes":"become X, make X","handled_by":"BEGIN + root; cause-to"},
 {"q":"2.2.2.4-5 verbs from adverbs/other","subtypes":"marginal","handled_by":"none needed"},
 {"q":"2.2.3.1 adjectives from nouns","subtypes":"having, lacking, like, pertaining to, made of","handled_by":"HAVING linker (proposed), NOT, THAN, KIND"},
 {"q":"2.2.3.2 adjectives from verbs","subtypes":"doing, done, able to be done, tending to","handled_by":"KIND { } with ONGOING/DONE/HABIT; can-be for -able"},
 {"q":"2.2.3.3 adjectives from adjectives","subtypes":"opposite, weakened (-ish), intensified","handled_by":"opposite; SLIGHT, VERY"},
 {"q":"2.2.3.4-5, 2.2.4.1-5 adverbs","subtypes":"manner, time, place adverbs from any class","handled_by":"no affix: WITH / WHEN / AT + root"},
 {"q":"2.2.5 other","subtypes":"ordinals, multiplicatives, proper names, word-mention","handled_by":"ORD, number + degree, name root; mention marker undecided"},
 {"q":"2.2.6.1-2 complex and derived adpositions","subtypes":"two adpositions, nominal, verbal, adjectival","handled_by":"role + relational root + REL (FROM behind REL car); no affix"},
 {"q":"2.2.6.3 compounding","subtypes":"all class pairs, recursion","handled_by":"head + KIND + modifier, nested with ( ); fixed terms via DEFINE. Undecided: whether a fixed compound is one lexicon entry and how it differs from a free KIND phrase"},
]

der=[
 {"affix":"opposite","meaning":"The other pole of a scale or state; on an action root, the action that undoes it. Not the same as NOT (NOT big is merely 'not big'). Halves the property vocabulary.","example":"big + opposite = small; tie + opposite = untie; before + opposite = after"},
 {"affix":"cause-to","meaning":"Adds a causer (AGENT) to a state or event root; the former sole argument stays THEME. Repeatable.","example":"die + cause-to = kill; know + cause-to = inform/teach; hot + cause-to = heat"},
 {"affix":"one-who","meaning":"The AGENT participant as a thing-word: the person or thing that does the act, or is characterised by the root.","example":"teach + one-who = teacher; science + one-who = scientist"},
 {"affix":"thing-done","meaning":"The THEME participant or product: what is made, done or undergoes the act.","example":"build + thing-done = building; write + thing-done = text; eat + thing-done = food"},
 {"affix":"tool-for","meaning":"The WITH participant: the instrument or means made for the act.","example":"cut + tool-for = knife; compute + tool-for = computer"},
 {"affix":"place-of","meaning":"The AT participant: the place where the act is done or the thing is kept.","example":"cook + place-of = kitchen; book + place-of = library"},
 {"affix":"quality-of","meaning":"The abstract property or neutral dimension of a property root, or the state of being X for a thing root.","example":"long + quality-of = length; hot + quality-of = temperature; friend + quality-of = friendship"},
 {"affix":"group-of","meaning":"A collection of X taken as one unit (the lexical partner of WHOLE).","example":"tree + group-of = forest; star + group-of = constellation; word + group-of = vocabulary"},
 {"affix":"can-be","meaning":"Optional ninth: the property of being able to undergo the act (short for KIND { CAN ... THEME SELF }); frequent in technical prose.","example":"read + can-be = readable; break + can-be = fragile; see + can-be = visible"},
]

lex=[
 {"field":"5.1.1 kinship","needs_roots":True,"note":"Small core only: parent, child, sibling, spouse, plus male/female as ordinary roots (mother = parent KIND female). All are relational roots (REL). By marriage/adoption/fostering = KIND + root (marry, adopt). No gendered or generational series needed."},
 {"field":"5.1.2 colour","needs_roots":True,"note":"Basic terms only (black, white, red, yellow, green, blue; perhaps brown, grey). Finer shades by KIND, SLIGHT/VERY, or « » codes. 'opposite' could give black from white but is not recommended for hues."},
 {"field":"5.1.3 body parts","needs_roots":True,"note":"Largest closed field in the basic list (about 30: head, eye, ear, nose, mouth, tooth, tongue, neck, hand, foot, leg, knee, back, belly, breast, heart, liver, guts, skin, hair, bone, blood, flesh, fat, tail, wing, horn, claw, feather). Part-whole by OF. Low priority for reasoning, needed for everyday talk."},
 {"field":"5.1.4 cooking","needs_roots":True,"note":"A few roots (cook, bake, fry); boil, heat, cool, dry, freeze come from state roots + BEGIN or cause-to."},
 {"field":"5.1.5 other structured fields: knowing and reasoning","needs_roots":True,"note":"Not in the questionnaire list but the main field for this language: know, think, believe, doubt, prove, infer, assume, mean, cause, result, reason, evidence, true, error. Openers and strength mark the writer's own stance; roots are still needed to talk about others' reasoning."},
 {"field":"5.1.5 other: speech and social acts","needs_roots":True,"note":"say, ask, answer, promise, thank, greet, agree, sorry, ok - needed as fillers of SOCIAL and for reported speech."},
 {"field":"5.1.5 other: generic heads","needs_roots":True,"note":"thing, person, place, time, way, kind, part, amount, number, event - required because WHAT, ANY, NONE, THIS need a head (who = WHAT person, nowhere = AT NONE place, what he said = thing KIND { })."},
 {"field":"5.1.5 other: technical and scientific terms","needs_roots":True,"note":"A general core (data, file, test, value, set, function, measure, force, energy, cell...); the rest by KIND compounds, DEFINE, or « » loans."},
 {"field":"4.1 ideophones","needs_roots":False,"note":"None; sound-symbolic words have no place in a written, sound-free language."},
 {"field":"4.2 interjections","needs_roots":False,"note":"Done by SOCIAL + root, YES/NO fragments and attitude particles (SURPRISE, GLAD, ANNOYED). No irregular forms; needs only the social-act roots above."},
 {"field":"5.2 pronouns (I, thou, he, we, ye, they)","needs_roots":False,"note":"ME, YOU, US; third person by handles, THAT, or repeating the noun; plural 'you' by a quantifier (ALL YOU, 2 YOU)."},
 {"field":"5.2 demonstratives and deictic adverbs (this, that, here, there)","needs_roots":False,"note":"THIS / THAT + generic head (THIS place = here). Open point: today/yesterday/tomorrow and 'now' as a head need either roots or the proposed PAST/FUTURE + measure."},
 {"field":"5.2 question words (what, who, when, where, how)","needs_roots":False,"note":"WHAT in a role or slot: AGENT WHAT person, AT WHAT, WHEN WHAT, WITH WHAT, CAUSE WHAT, degree WHAT."},
 {"field":"5.2 quantifiers and numerals (all, many, few, some, other, one to five)","needs_roots":False,"note":"Quantifier particles and digits; ordinals by ORD. Roots needed only for collective units (pair, dozen) if wanted."},
 {"field":"5.2 grammatical words (and, at, because, if, not, with)","needs_roots":False,"note":"AND, AT, CAUSE, IF, NOT, WITH/ALONG are particles."},
 {"field":"5.2 spatial relations (in, near, far, leftside, rightside, back)","needs_roots":True,"note":"Grammar gives the frame (AT/TO/FROM/VIA + root + REL) but the relational roots must exist: inside, near, top, above, front, side, left, between, among, around, across, along, beyond. With 'opposite', about half suffice (outside, far, below, behind, right). Same roots serve time (before, after, during)."},
 {"field":"5.2 dimension and property words (big, long, wide, thick, heavy, small, short, narrow, thin, new, old, good, bad, warm, cold, wet, dry, full, dirty, sharp, dull, smooth, straight, round, rotten, right/correct)","needs_roots":True,"note":"One pole per scale; the other by 'opposite'; dimension nouns (length, weight, age, temperature) by quality-of. Watch root/particle doublets: full vs FULL, near/far vs NEAR/FAR, other vs OTHER, many/few vs MANY/FEW should not also be roots."},
 {"field":"5.2 people (person, man/male, woman, child, husband, wife, father, mother, name)","needs_roots":True,"note":"person, male, female, child, spouse, parent, name; the gendered items are KIND compounds."},
 {"field":"5.2 animals (animal, bird, dog, fish, louse, snake, worm)","needs_roots":True,"note":"Open class: a handful of life-form roots, the rest as KIND compounds or « » scientific names."},
 {"field":"5.2 plants and plant parts (tree, grass, leaf, root, bark, flower, fruit, seed, stick, woods)","needs_roots":True,"note":"woods = tree + group-of; bark = skin OF tree if wanted."},
 {"field":"5.2 nature, sky, weather, substances (sun, moon, star, sky, cloud, rain, snow, ice, fog, wind, water, sea, lake, river, earth, sand, stone, dust, mountain, fire, smoke, ashes, salt)","needs_roots":True,"note":"Core roots needed; several reducible (ice = water KIND solid, lake/sea by size, ashes = thing-done of burn)."},
 {"field":"5.2 time units (day, night, year)","needs_roots":True,"note":"Unit roots (second ... year, day, night, season); weekday and month names should be unit + ORD, clock times and dates in « », so no name roots."},
 {"field":"5.2 body processes, perception, mind (breathe, eat, drink, bite, suck, spit, vomit, sleep, live, die, laugh, sing, play, see, hear, smell, fear, know, think, say, count, swell)","needs_roots":True,"note":"All need roots; each needs a role frame (experiencer = AGENT). kill = die + cause-to; show = see + cause-to."},
 {"field":"5.2 posture and motion (come, walk, fly, swim, fall, float, flow, turn, lie, sit, stand)","needs_roots":True,"note":"Manner-of-motion roots needed; come/go is one root with TO/FROM (come = move TO ME), up/down by direction roots."},
 {"field":"5.2 handling and impact (give, hold/take, throw, push, pull, hit, cut, split, stab, scratch, rub, wipe, wash, squeeze, tie, sew, dig, hunt, fight, kill, burn, freeze)","needs_roots":True,"note":"Mostly roots. Free role order removes converse pairs (give/receive, buy/sell are one root each); pull = push + opposite; freeze/burn from state roots with BEGIN or cause-to."},
 {"field":"5.2 artefacts (road, rope)","needs_roots":True,"note":"Open class; many derivable with tool-for and place-of."},
]

out={"counts":counts,
 "counting_note":"NA and COVERED count questionnaire functions (leaf questions, with the 26 local-relation rows and their four columns counted as one function per row). CLUMSY/GAP/UNDECIDED/IDEA count the items below; one item often covers several questionnaire functions.",
 "items":I,"derivation_functions":functions,"derivation":der,
 "derivation_note":"Design principle behind one-who / thing-done / tool-for / place-of: each picks out one role of the root (AGENT, THEME, WITH, AT). If more are wanted later (recipient, time, reason) they should follow the same pattern rather than be invented ad hoc. Not needed as affixes because the grammar already does the work: become (BEGIN), again (AGAIN), not/non- (NOT), having/lacking (proposed HAVING linker, NOT), like (THAN), -ish/very (SLIGHT, VERY), reflexive/reciprocal (SELF, MUTUAL), adverb-forming (WITH + root), diminutive/augmentative and sex (KIND + root), act-of (bare root as head, once item 5 is decided).",
 "lexicon_fields":lex}
p="<workdir>/survey/out_q2.json"
json.dump(out,open(p,"w"),ensure_ascii=False,indent=1)
print(counts,len(I))
