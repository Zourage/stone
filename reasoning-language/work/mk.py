import json, csv, sys
S="<workdir>/survey/"
names={r["ID"]:r["Name"] for r in csv.DictReader(open(S+"wals_parameters.csv"))}
covered="34A 35A 38A 41A 42A 43A 45A 52A 53A 55A 60A 62A 63A 64A 65A 67A 68A 70A 71A 74A 75A 76A 105A 106A 107A 108A 109A 110A 115A 117A 118A 120A 122A 123A 125A 126A 127A 128A".split()
I=[]
def it(fid,cat,what,ex,status,how,sug,pri):
    I.append({"source":f"{fid} {names[fid]}","category":cat,"what":what,"example":ex,"status":status,"how_now":how,"suggestion":sug,"priority":pri})

it("36A","associative plural","A named person plus the people who belong with them, as one group.",
 "Japanese Tanaka-tachi = 'Tanaka and his lot'.","CLUMSY",
 "group OF name«Tanaka», or name«Tanaka» AND (OTHER person KIND { ALONG SELF ... }); US does this for the writer only.",
 "Leave out; state as a rule that 'X and associates' is `group REL X`. Too rare in reasoning text to earn a particle.",1)
it("37A","definiteness","Whether a referent is identifiable to the reader, including things identifiable by uniqueness or shared knowledge and never mentioned before.",
 "English 'the capital of France', 'the root cause' on first mention, against 'a cause'.","UNDECIDED",
 "THAT is defined as 'the one already identified'; a bare head 'says nothing'. One writer uses THAT for a first-mention unique, another leaves it bare, a third uses THIS.",
 "Rule: THAT = identifiable by any means (earlier mention, uniqueness, shared knowledge); a new referent is bare, or SOME/1 when newness matters. The decoder then has a deterministic the/a choice.",2)
it("39A","clusivity","Whether 'we' includes the addressee.",
 "Tok Pisin yumi (you and I) against mipela (we, not you).","CLUMSY",
 "ME AND YOU for the inclusive dual; US is explicitly neutral, so the exclusive ('my side, not you') and the inclusive plural have no fixed form; EXCEPT is a clause role and cannot attach to US.",
 "Change one clarification: US is always exclusive (the writer's group without the addressee); inclusive is US AND YOU or ME AND YOU. No new particle.",2)
it("46A","indefinites and specificity","Whether 'some X' is a particular one the writer has in mind or whichever one satisfies the clause.",
 "Russian koe-kto (a certain person, known to me), kto-to (someone, unknown), kto-nibud' (someone or other); English 'I am looking for a file' in two readings.","CLUMSY",
 "SOME against ANY separates existence from free choice. The particular-one reading under NOT, a modal or want needs `EACH F IN SOME file { ... }`, which reads as 'each of some'.",
 "Add one quantifier, e.g. PARTICULAR (one specific item, taken outside every NOT, modal and block of the sentence), or rule that `SOME x NAMED H` always has that widest reading.",2)
it("47A","reflexive reference","Which participant a reflexive points back to, and the separate emphatic use ('the author herself').",
 "Latin se can point to the subject of a higher clause; English 'A said B hurt himself'; 'X equals itself'; 'the director herself signed'.","UNDECIDED",
 "SELF is the head inside a modifier clause and the AGENT in a main clause. Undefined in a clause with no AGENT (EQUAL THEME x THAN SELF), in a complement block, as a possessor (file OF SELF is not in the modifier rule), and for a reflexive inside a relative clause, where SELF already means the head.",
 "Rule: SELF = the head when inside a modifier block; otherwise the AGENT of its own clause, or the THEME when there is no AGENT; anything further away takes a handle. Add SELF to the modifier rule. The emphatic use is FOCUS and should be stated.",2)
it("49A","role inventory","Roles that languages keep apart are merged in one particle, and a role may occur only once per clause.",
 "English 'cut it carefully with a knife' (manner and instrument); 'bought it for Ana for the trip' (beneficiary and purpose); 'longer by two metres for an hour' (difference and duration).","CLUMSY",
 "WITH (careful AND knife), FOR (name«Ana» AND trip), SPAN (2 metre AND 1 hour): AND joins fillers of unlike meaning and the reader must sort them out.",
 "Either lift the once-per-clause limit for the roles defined with 'or' (WITH, FOR, SPAN, TO, AT, CAUSE), or state that manner always goes in the degree/modifier position of the predicate, e.g. ( cut WITH care ), leaving WITH for means.",2)
it("54A","distributive numerals and rates","A quantity that holds for each member of another set: 'two each', 'three per run'.",
 "Latin bini 'two each'; English 'three retries per request', 'one reviewer per paper'.","CLUMSY",
 "EACH R IN ALL request { have AGENT R THEME 3 retry }, a whole binding construction for one word; rates with units can hide in « » but counts of ordinary things cannot.",
 "Add a role PER: `allow THEME 3 retry PER request`. It also serves ratios and rates in prose (cost SPAN 5 dollar PER hour).",2)
it("59A","possessive classification","Which linker joins two nouns: ownership, part of whole, bearer of an attribute, or the second participant of a relational noun.",
 "Oceanic languages mark inalienable (kin, parts) apart from alienable property; English 'the size of the file', 'the cause of the failure', 'the author of the paper', 'the top of the stack', 'the result of step 2'.","UNDECIDED",
 "OF = owner or whole, REL = landmark of a relational root, KIND = narrowing, content, material. The spec's own example writes count OF prime (neither owner nor whole) beside friend REL name«Ana». For size, name, cause, result, author, top, half, two writers will split between OF and REL.",
 "Rule plus a test: if the head's meaning is incomplete without a second thing (kin, position, time, cause, result, author, part-names such as top or half, measures such as size or count), use REL; OF only for ownership and for a member or piece named by an ordinary root (wheel OF car). Rewrite the count OF prime example to match.",3)
it("61A","property and action roots as heads","Whether a quality or action root standing as a head names the quality or event, or a thing that has or does it.",
 "Spanish el grande 'the big one'; English 'the poor', 'a run', 'the unknown', 'I want a bigger one'.","UNDECIDED",
 "Roots have no class and 'position decides', but nothing says what THEME big or THAT fail denotes (bigness or the big one; failing or the thing that failed). Kind-anaphoric 'one' has no form.",
 "Rule: a quality or action root as head names the quality or the event itself; 'one that is X' is always `thing KIND X` or `person KIND X`, and 'a bigger one' repeats the head root. THAT KIND big = 'that big one'.",2)
it("66A","unmarked tense","What a clause with no time particle means: timeless law, present state, or the time carried over from the previous sentence.",
 "English 'Water boils at 100 degrees' (timeless) against 'The test fails' (right now) against narrative past carried through a paragraph.","UNDECIDED",
 "The spec says unmarked = timeless, yet its examples use unmarked clauses for current states (fail THEME test; STILL SLIGHT high THEME price) and define NOW as 'at present, may change'. Whether each STORY sentence must repeat PAST is not stated.",
 "Rule: unmarked = time not stated, read from context (inside a block, the enclosing clause; in a SEQUENCE or STORY chain, the previous sentence; otherwise the present). A law is marked with GENERIC or ALWAYS. NOW is used only to contrast with another time.",3)
it("72A","hortative and proposal","A proposal for joint action or a suggestion, as distinct from an instruction, a commitment or an offer.",
 "English 'Let's rerun it', 'How about caching the result?', 'Let him wait'; many languages have a first-person-plural hortative and a third-person jussive form.","UNDECIDED",
 "REQUEST instructs, PLAN commits, PLAN IF { want AGENT YOU } offers, CLAIM SHOULD advises. 'Let's' could be REQUEST with AGENT (ME AND YOU), PLAN with AGENT US, or CLAIM SHOULD; the third-person 'let X do it' could be REQUEST with AGENT X or MAY.",
 "Rule: REQUEST with AGENT (ME AND YOU) = 'let's'; REQUEST with a third-person AGENT = 'X is to do it'; a strength particle after REQUEST grades it (REQUEST POSSIBLE = suggestion, 'you could'). Or add one opener PROPOSE. Proposing is the commonest move an assistant makes, so it should not be left to choice.",3)
it("73A","optative and apprehensive","A wish that something be so, or a fear that it may be, marked as the speaker's stance instead of asserted.",
 "English 'May it work', 'Hopefully this fixes it', 'If only we had logged it', 'lest it overflow'; Turkish optative forms; apprehensive moods in many Australian languages.","CLUMSY",
 "CLAIM hope AGENT ME THEME { ... } or REGRET UNREAL for 'if only'. GLAD and REGRET cover what has happened; nothing covers what has not happened yet.",
 "Add two attitudes to the existing list: HOPE and FEAR (FUTURE fix ... with HOPE = hopefully; FEAR POSSIBLE = I am afraid it may). Same slot, no new syntax.",2)
it("77A","evidentiality: reported against witnessed","Whether the writer saw the fact first-hand or was told it by someone.",
 "Quechua -mi (direct) against -si (reported) against -cha (conjecture).","IDEA",
 "GIVEN lumps 'a document, tool or other party shows it' with 'the writer observes it directly'. Hearsay can be kept apart only by BY x { } or say AGENT x, which turns the claim into a quotation and loses the writer's use of it as a premise.",
 "Split GIVEN: keep GIVEN for what the writer itself observes in the context (tool output, file content), and add an opener TOLD [source] for what another party asserts and the writer has not checked. A user's report and a test log are premises of very different weight in a DERIVED chain.",3)
it("80A","event number","How many times an event happens: a counted number of occurrences, or 'repeatedly' on one occasion.",
 "English 'ran the test three times', 'it failed twice', 'knocked repeatedly'; pluractional verb forms, e.g. by reduplication in Hausa.","UNDECIDED",
 "AGAIN = once more, OFTEN and the like = frequency. A count of occurrences has no stated form; candidates are SPAN 3 time, a factor-style number before the predicate, or EACH over runs. 'How many times' likewise.",
 "Add TIMES to the aspect slot, taking a number or quantifier before it: PAST 3 TIMES run, MANY TIMES, WHAT TIMES, ATLEAST 2 TIMES. Keeps counts out of SPAN, which already means duration, extent and difference.",3)
it("90E","comparative correlative","Two quantities vary together: the more of one, the more (or less) of the other.",
 "English 'The hotter the gas, the faster the reaction'; Hindi jitna ... utna correlative clauses.","CLUMSY",
 "Only by paraphrase: cause AGENT { rise THEME heat } THEME { rise THEME speed }, or a formula in « ». The first asserts causation and loses the graded dependence.",
 "Rule, no new particle: IF { MORE a ... } { MORE/LESS b ... } with no THAN phrases means covariation. A number before the second MORE can give the rate. Central to scientific exposition.",3)
it("91A","degree on quantities","Grading or comparing an amount, as opposed to a property: almost all, too many, very few, enough, more of X than of Y.",
 "English 'almost all tests', 'too many files', 'more errors than warnings', 'enough memory', 'far fewer'.","CLUMSY",
 "Degree particles are licensed only before a predicate or a modifier. An amount needs a detour: TOO big THEME count OF file; MORE big THEME count REL error THAN count REL warning; ALL test EXCEPT FEW.",
 "Allow {degree} before a quantifier: ALMOST ALL, TOO MANY, VERY FEW, ENOUGH memory, MORE error THAN warning (MORE before a bare head compares amounts), BARELY ANY. One line in the grammar: unit = ... [NOT] {degree} {quantifier} head.",3)
it("93A","which against how many","Asking for the identity of an item against asking for the number of items.",
 "English 'Which tests failed?' against 'How many tests failed?'.","UNDECIDED",
 "The quantifier WHAT is glossed 'how many / which', so fail THEME WHAT test is both questions.",
 "WHAT as quantifier = which only. How many = WHAT MANY (WHAT in the degree position of a quantifier, parallel to WHAT big = how big), or WHAT TIMES for occurrences. Depends on the 91A fix.",3)
it("98A","semantic alignment of the sole participant","Whether the only participant of a one-place predicate is marked as doing it or as undergoing it, and whether an inanimate cause counts as an actor.",
 "Tsova-Tush 'I fell' takes ergative when it was my doing and absolutive when it happened to me; English 'the test passed', 'the server died', 'A arrived', 'the wind opened the door'.","UNDECIDED",
 "The spec has fail THEME test and arrive AGENT A, and a rule only for states (holder = AGENT). For die, sleep, pass, work, slip, crash, grow writers will split; for 'the timeout killed the job' they will split between AGENT timeout and CAUSE timeout.",
 "Rule: the sole participant is AGENT only if it controls the event (acts, moves under its own power, perceives or holds); otherwise THEME. Where both are possible the choice means control (slip AGENT = on purpose, slip THEME = by accident). An inanimate trigger is CAUSE, never AGENT, unless it is a program or device carrying out an action.",3)
it("101A","omitted participants","Whether a left-out participant means 'unspecified, someone' or 'the one we both know from context'.",
 "Japanese zero subjects are read from context; English agentless passive 'Has the release been sent?' against 'Have you sent the release?'.","UNDECIDED",
 "Roles are freely omitted (ASK DONE send THEME release; REQUEST bake THEME ham) and the spec says nothing about the reading. The decoder must pick a passive or supply a pronoun.",
 "Rule: an omitted role is unspecified, never anaphoric (decode as passive or 'someone'); the one exception is REQUEST, where an omitted AGENT is the addressee. A known participant is always written (YOU, a handle, THAT).",3)
it("111A","causative and inchoative","The same state seen as holding, as coming about, or as brought about by someone.",
 "Turkish ol- 'die' against ol-dur- 'kill'; English 'the door is open / opened / Ana opened the door', 'the file is big / grew / she enlarged it'.","UNDECIDED",
 "Three candidate forms for 'A enlarged the file': big AGENT A THEME file; cause AGENT A THEME { BEGIN big THEME file }; BEGIN big THEME file CAUSE A. The spec licenses none in particular.",
 "Rule: adding an AGENT to a state or change root means 'brings it about' (open AGENT A THEME door; big AGENT A THEME file), BEGIN gives 'comes to be', bare gives the state. The root cause is kept for claims about causation between events (as in example 4).",2)
it("116A","answers to negative questions","Whether 'yes' to a negative question confirms the negative wording or asserts the positive fact.",
 "Japanese hai to 'Didn't you send it?' means 'right, I did not'; English 'yes' means 'I did'; French has a third word, si.","UNDECIDED",
 "ASK NOT send AGENT YOU THEME release answered by GIVEN ANSWER 1 YES is unreadable; the spec defines YES/NO bias on ASK but not the answer rule. Also unstated: how to ask a yes/no question about a disjunction, since OR directly under ASK always means 'which one'.",
 "Rule: YES and NO as answers affirm or deny the clause exactly as written in the question, NOT included (the agree/disagree system, the logical one). A disjunction asked as yes/no is put in ( ): ASK ( a OR b ).",3)
it("119A","locational and existential predication","Saying where a known thing is, as distinct from saying that something exists there, and from saying what it is.",
 "Spanish 'es un libro' (class), 'esta en la caja' (location), 'hay un libro en la caja' (existence).","UNDECIDED",
 "Class and property predication are settled (root or ( phrase ) as predicate). For location there is no rule: ( inside REL box ) THEME key, or exist THEME key AT inside REL box, or a root such as stay or lie.",
 "Rule: location of a known thing uses the relational root as predicate, `inside THEME key REL box` or ( inside REL box ) THEME key; existence uses exist with AT. One sentence in the 'there is no is' paragraph.",2)
it("121A","superlative domain","The set within which something is the most or least.",
 "English 'the largest of the three files', 'the slowest test in the suite'.","UNDECIDED",
 "MOST and LEAST exist, but THAN is defined only for MORE/LESS/EQUAL; the set could go in THAN, FROM, AT, OF or be rephrased as MORE ... THAN ALL OTHER file.",
 "Extend the THAN rule by one clause: with MOST or LEAST the THAN phrase names the set compared (MOST big THEME F THAN ALL 3 file).",2)
it("124A","shared subject in complements","Whether the unstated subject of a complement or purpose clause is the same person as the main-clause subject.",
 "English 'A wants to leave' against 'A wants B to leave'; 'A promised B to go' against 'A told B to go'.","UNDECIDED",
 "want AGENT A THEME { leave } leaves the leaver unstated; writers will variously omit it, repeat A, or write SELF, and SELF inside a non-modifier block is not defined.",
 "Rule following from 101A: nothing is understood. The complement states its AGENT, as the handle or as SELF = AGENT of the enclosing clause; an AGENT-less complement means 'someone'. The modal particles need no subject and are unaffected.",2)

assert len(I)==24 and len({i["source"] for i in I})==24
non={i["source"].split()[0] for i in I}
assert not (non & set(covered))
counts={"NA":len(names)-len(covered)-len(I),"COVERED":len(covered)}
for s in ["CLUMSY","GAP","UNDECIDED","IDEA"]: counts[s]=sum(i["status"]==s for i in I)
assert sum(counts.values())==192, counts
for c in covered: assert c in names
I.sort(key=lambda i:(-i["priority"]))
cn=[
 "34A Occurrence of Nominal Plurality: a bare head is number-neutral; number is added only when it matters (1, SEVERAL = more than one, ALL 2 = both).",
 "52A Comitatives and Instrumentals: kept apart, ALONG for companion and WITH for means.",
 "53A Ordinal Numerals: ORD n is fully regular, and WHAT gives 'which one in order'.",
 "60A Genitives, Adjectives and Relative Clauses: one modifier position for all three, with KIND (narrows) against NOTE (comment, does not narrow) marking restrictive against non-restrictive.",
 "62A Action Nominal Constructions: a block stands as a head with all its roles kept, so no separate nominalised syntax is needed.",
 "63A Noun Phrase Conjunction: AND is distinct from ALONG, and WHOLE against ALL separates 'together' from 'each'.",
 "65A Perfective/Imperfective Aspect: ONGOING, HABIT and DONE plus the phase particles BEGIN, STOP, STILL, ALREADY, with scope fixed by left-to-right order (NOT STILL against STILL NOT).",
 "67A The Future Tense: future time (FUTURE), commitment (PLAN) and prediction (strength) are three separate things; NEAR/FAR give remoteness.",
 "68A The Perfect: DONE = finished and result holds; time in a block counted from the enclosing clause gives 'had done' with no extra form.",
 "71A The Prohibitive: MUST NOT against NOT MUST, the forbidden/not-required contrast settled by position.",
 "76A Overlap between Situational and Epistemic Modal Marking: no overlap by design; MUST/SHOULD/MAY/CAN are about the world, CERTAIN/LIKELY/POSSIBLE about the writer's confidence.",
 "106A Reciprocal Constructions: MUTUAL in a role slot, distinct from reflexive SELF.",
 "120A Zero Copula for Predicate Nominals: no copula; class membership is a ( phrase ) predicate, identity is EQUAL ... THAN, definition is DEFINE ... BE.",
 "123A Relativization on Obliques: SELF marks the head's place in any role, and NAMED handles replace it when clauses nest, so every position can be relativised.",
 "128A Utterance Complement Clauses: BY block = direct speech, plain block = indirect report, BY x AROUND = paraphrase."]
json.dump({"counts":counts,"items":I,"covered_notable":cn,"covered_ids":covered},open(S+"out_wals.json","w"),ensure_ascii=False,indent=1)
print(counts)
