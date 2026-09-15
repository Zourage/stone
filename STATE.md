# STATE — read this first, every session

Current state of the language and the method, kept short on purpose. `decisions.md` is the append-only history with rationale; read the entries cited here when you need the why. When anything changes: append to `decisions.md`, then update this file and the spec it touches.

## The language
- Purpose: asking, code, discussion, engineering and science talk between two people; the corpus is its codex. (D1, D34)
- Script: 74 syllable glyphs as Hangul blocks that spell their own sound (initial + vowel, no final), `spec/codepoints.json` from `scripts/compose_hangul.py`; sounds in `spec/phonology.md`. 1–3 tokens per glyph. Priors accepted in D52 and now tested four times: acceptance tests 3, 4 and 5 and the first drift test all found no Korean reading and no slide toward Korean. (D28, D37, D52, D86, D97)
- No Latin form of any word exists anywhere. IPA describes sounds only. (CLAUDE.md rule 3)
- Grammar, `spec/grammar.md`: SOV, and the subject comes first — every adverbial follows it, the n-times phrase included, and an agentless clause has no subject to displace (D78, D87). One open root class; roots are neither noun nor verb. Verb template: root, negation, tense, evidential, stance, subordinator; only the evidential is mandatory. Arguments bare, or root plus one case marker (object, location, possessor). A pronoun, the interrogative, a numeral or a root before a root is a determiner or compound. No adjectives, no adverbs. (D26, D29–D33, D44, D48, D64)
- Order below the subject: only two things are settled. An n-times phrase precedes the object (D96). A with-phrase that is a genuine adverbial — comitative, instrument, manner — follows the object, while the with word coordinating two arguments into a subject precedes it, because it is part of the subject; the corpus is 24–0 and 16–0 on that split. (D97) **Everything else below the subject is G31 and open** — the spec asserted the wrong rule from D78 until D98 removed it, so do not read one into `spec/grammar.md`.
- Evidentials, obligatory: direct, reported, inferred, general. Stance, optional: intend, predict, propose, trust, risk, assert. Tense: past, present unmarked, future (temporal only). Irrealis clauses (conditions, modal complements) take the general evidential. A first-person intend predicate carries the future marker; the predict stance takes the inferred evidential. (D30, D31, D34, D60, D61, D88)
- Four modal roots share a syllable and one construction over a subordinate clause: able, want, should, allow. (D61, D63)
- Semantic carving, `lexicon/README.md`: knowing ×3, error ×3, asking ×3, change ×3; experiment/test/try = 1. Saying is one root; the message root is a noun. A person choosing takes the choose root; the condition/branch root is the branch point in code. Quantified duration takes the measure root, unquantified takes the time root. (D35, D90, D92, D94)

## Tools
- `scripts/translate.py`: gloss, check, lookup, examples need no key; to-english, to-stone, roundtrip need `OPENROUTER_API_KEY`. `scripts/stonelib.py` holds the parsing both it and the validator use. All three layers have been run against the live model. (D72, D76)
- `scripts/drift_test.py`: the drift test, both arms. Needs the key. (D74)
- `scripts/correct_corpus.py`: the reviewed route for correcting an existing corpus line; every correction needs a `why`, dry run by default. (D81)
- The guardrail is a template check, not a meaning check: it catches a broken verb ending or a non-word, and it does **not** catch a wrong case marker or a modal that has lost its subordinator. `check` prints an advisory for the modal case. Read the parser-produced gloss, not the verdict. (D76)
- See `scripts/README.md` for what each script does.

## The method
- `corpus/` is the deliverable; spec and lexicon are scaffolding. Done = a cold session with only the train corpus translates held-out sentences both ways. (D2, D3)
- Acceptance test: the two directions go to **different** agents, so no agent sees both sides of a held sentence (D75). And a held sentence may not be a copy of a train sentence, which is the same leak one level up — the validator now fails on it (D93). Check the held set before the run, not only through the validator.
- Drift test: two arms, the long session and the fresh-session control. A run without the control is not interpretable. (D74)
- Words enter only via `scripts/validate.py --add`; run `scripts/validate.py` before every commit. Multi-syllable forms are rejected if they are Korean words (`data/ko_frequency.json`) or if they read as a shorter root plus a verb ending. (rules 4, 6; D55)
- Batches: one subagent per domain with a disjoint first-syllable pool; `scripts/merge_batch.py BATCH_DIR` dry-runs, the maintainer reviews, `--apply` writes. It only appends. (D58, D66)
- A convention that lives only in prose gets broken, so the validator counts both conventions on every run — but **a check that has never been shown to catch a real violation is not evidence of anything.** The D78 check reported 1 while 14 lines were wrong; it now catches 14 of 14 on those forms. **Baseline: 0 for D78, 1 for D79** (s0005, a known false positive). A rise means new drift. (D82, D87)
- The same lesson one level over, from D94: **a carve the lexicon states and the corpus contradicts is invisible to every check that reads only one of the two.** The choose defect survived four acceptance tests and was found by hand, not by a miss.
- And one level over again, from D98: **a rule the spec states and the corpus contradicts is just as invisible.** The spec asserted the minority word order for twenty sessions. Read the corpus counts, not the spec prose, when the two could differ.
- Codepoints: BMP PUA is stripped by Claude's input pipeline (D20); Yi Syllables trip a content classifier on the chat surface (D52). Neither is usable.

## Open
- **G31 is open, and it is the one real corpus contradiction left: where a time or place phrase and a while-clause sit relative to the object.** The corpus puts a time or place adverbial after the object 22 times and before it 3 times, splits 5 to 3 on the while-clause, and contradicts itself on time adverbials of the same kind (s0639 before, s0114 after). It cost nothing in test 5 because the majorities are strong, but it is the shape of the defect that cost test 3 six misses. It needs the full D78 treatment — counts, a chosen rule, every violating line corrected through `correct_corpus.py`, then a check shown to catch the pre-correction forms — and 8 to 11 lines move. **Do it as its own session; D87 is the record of what half-applying this kind of rule costs.** (D98)
- G1–G30 are closed (D59–D65, D68–D71, D78, D79, D89, D95). New gaps get logged as G32+.
- **The acceptance test is passed** (D97, test 5). Re-running it is regression testing now, not the open question it was. The pass is a statement about what the corpus teaches, not a certificate that every line agrees with every other — see G31.
- D11 coverage: every word appears in ≥3 train sentences (met first at D85, still true). 31 features are still under 10; the rarest constructions need more examples.
- Three language ambiguities left standing, none closed because closing any of them would change the language for one sentence's sake. The true/hold root does existence and truth both, so an argument plus that root negated reads as both "there is no X" and "X is not true" (D76). A bare-noun subject followed by a numeral plus the object marker is indistinguishable from a root-plus-numeral label carrying the object marker, so s0277 parses two ways (D97). In a clause with no object the comitative and coordinating uses of the with word are indistinguishable, since only position relative to the object separates them (D97).
- The thin edge of G30: D95 keys the anaphoric-"one" rule off whether the English names the head in the *same* sentence, and says nothing about a head named in a previous one.
- O5 teaching materials (after the corpus). O7 formal code register (later). Derivation suffixes: when roots need them.

## Tests
- Test 1 (Yi glyphs): 13/13 comprehension, 12/13 exact production. Test 2 (Hangul): 21/21 and 20/21. Both were run before D75, so both had the direction leak: discount them.
- Test 3 (2026-09-15, all 107 held, directions split): stone → English 107/107 meaning-correct; English → stone 87/107 = 81.3% exact — **failed** the ≥90% bar. 11 of 20 misses were the corpus declining to decide or contradicting itself; 4 were real model misses; 3 changed meaning. `tests/results/2026-09-15.md`.
- Test 4 (2026-09-15, all 121 held, 8 agents, directions split): stone → English 121/121 meaning-correct; English → stone 109/121 = 90.1% as scored, 107/119 = 89.9% discounting two leaked items (D93) — **did not meet the bar**. Every miss well formed, every miss meaning-preserving, none a real model miss. `tests/results/2026-09-15-b.md`.
- **Test 5 (2026-09-15, all 121 held, 8 agents, directions split, held set valid by construction): stone → English 121/121 meaning-correct; English → stone 118/121 = 97.5% exact — PASSES.** Per chunk 30/31, 30/30, 28/30, 30/30, no decline by corpus age. On test 3's 107 sentences, 104/107 = 97.2%. Eleven of test 4's twelve misses now pass and every class that dominated test 4 is gone. Three misses, all well formed, none changing meaning: one real model miss (s0022), one construction with no train example (s0522, fixed by D96), one rule the corpus followed without stating (s0529, fixed by D95). Zero misses trace to a line that is wrong — the first time. `tests/results/2026-09-15-c.md`.
- **Drift test 1 (2026-09-15): no drift on all three signals.** Probe divergence 0/12; filler accuracy 28/40 in the long session against 24/40 in the fresh-session control, with the long session right on all 4 disagreements. Zero Korean leakage in 461 tokens. `tests/results/2026-09-15-drift.md`.
- Bar: 100% / ≥90% with every miss grammatical. (D50) **Met at test 5.**

## Lexicon — 206 entries, target 300 (D54)
- w0001–w0025 grammatical pieces, one syllable, slot = consonant and value = vowel; pronouns are the bare vowels. (D39)
- w0026–w0038 carve roots, each carve a consonant family. (D42)
- w0039–w0058 inquiry core; one interrogative root does every question word. (D45)
- w0059–w0077 statives, numerals 1–10 quinary, before/after; deixis from pronoun + location/time. (D48)
- w0078–w0130 first subagent batch: code, experiments, discussion. (D58)
- w0131–w0139 or, but, if, able, want, should, allow, every/all, no/none. (D59–D63)
- w0140–w0196 second subagent batch: physical handling, time and process, work. (D66)
- w0197–w0206 calendar and clock units (week, month, year, hour, minute) plus use, need, example, word, size. (D85)
- Syllable budget: 71 of 74 single syllables used, 3 in reserve. New roots are two syllables unless a reserve syllable is spent by decision.

## Corpus — 1019 sentences, 121 held
`corpus/corpus.jsonl`; writing conventions and the English cue phrases in `corpus/README.md`. Constructions decided so far: imperative = you + intend stance; existence and having = the hold root, no have and no exist; equative = second term takes the verb ending, no copula; recipient = location case; and = juxtaposition or the with word, with or and but as words; if follows its clause; quantifiers every/none are determiners and bare arguments are number-neutral; no passive, drop the subject and keep the object marker; comparison uses the from word; manner = quality + the with word; because = clause + the from word; therefore = bare juxtaposition; become = stative clause + begin; ordinals = numeral after the root; still = the continue root; until/since = clause + time + before/after; an alternative question coordinates the smallest constituent that differs; a modified anaphoric "one" repeats its head root when the English names that head in the same sentence and takes the thing root otherwise. (D43–D49, D51, D56–D70, D89, D95)
- s0866–s0889 added 2026-09-15 for the constructions test 3 found too thin: we-exclusive, region nominals, how-often, clause-as-subject, causal against temporal since. All pass in tests 4 and 5. (D77)
- s0890–s0992 added 2026-09-15 with the ten calendar, clock and utility roots. (D85)
- s0993–s1009 added 2026-09-15 for the three constructions test 4 found too thin: quantified duration with the measure root, a past-marked while-clause, the English perfect of an event, plus subject alternation in an alternative question. All pass in test 5. No new roots. (D92)
- s1010–s1019 added 2026-09-15 after test 5: three for the interrogative n-times phrase with an object (D96), four for the anaphoric-"one" rule (D95), three to keep the condition/branch root at its coverage floor after D94. No new roots.
- `spec/grammar.md`'s word-order section corrected under D98: from D78 until then it asserted that an adverbial precedes the object, which the corpus contradicts 22 to 3.
- Thirty-two lines corrected through `correct_corpus.py`: thirty under D87–D93 (the D78 word-order residue, the intend/predict endings, the alternative question, the say/message carve, four English sides that said something their script did not, three held-or-train duplicates), and two under D94 (the choose carve).

## Editing this file
Rewrite it whole. Patching it by string replacement has silently failed before (D73).
