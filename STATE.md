# STATE — read this first, every session

Current state of the language and the method, kept short on purpose. `decisions.md` is the append-only history with rationale; read the entries cited here when you need the why. When anything changes: append to `decisions.md`, then update this file and the spec it touches.

## The language
- Purpose: asking, code, discussion, engineering and science talk between two people; the corpus is its codex. (D1, D34)
- Script: 74 syllable glyphs as Hangul blocks that spell their own sound (initial + vowel, no final), `spec/codepoints.json` from `scripts/compose_hangul.py`; sounds in `spec/phonology.md`. 1–3 tokens per glyph. Priors accepted in D52 and now tested three times: acceptance tests 3 and 4 and the first drift test all found no Korean reading and no slide toward Korean. (D28, D37, D52, D86)
- No Latin form of any word exists anywhere. IPA describes sounds only. (CLAUDE.md rule 3)
- Grammar, `spec/grammar.md`: SOV, and the subject comes first — every adverbial follows it, the n-times phrase included, and an agentless clause has no subject to displace (D78, D87). One open root class; roots are neither noun nor verb. Verb template: root, negation, tense, evidential, stance, subordinator; only the evidential is mandatory. Arguments bare, or root plus one case marker (object, location, possessor). A pronoun, the interrogative, a numeral or a root before a root is a determiner or compound. No adjectives, no adverbs. (D26, D29–D33, D44, D48, D64)
- Evidentials, obligatory: direct, reported, inferred, general. Stance, optional: intend, predict, propose, trust, risk, assert. Tense: past, present unmarked, future (temporal only). Irrealis clauses (conditions, modal complements) take the general evidential. A first-person intend predicate carries the future marker; the predict stance takes the inferred evidential. (D30, D31, D34, D60, D61, D88)
- Four modal roots share a syllable and one construction over a subordinate clause: able, want, should, allow. (D61, D63)
- Semantic carving, `lexicon/README.md`: knowing ×3, error ×3, asking ×3, change ×3; experiment/test/try = 1. Saying is one root; the message root is a noun. Quantified duration takes the measure root, unquantified takes the time root. (D35, D90, D92)

## Tools
- `scripts/translate.py`: gloss, check, lookup, examples need no key; to-english, to-stone, roundtrip need `OPENROUTER_API_KEY`. `scripts/stonelib.py` holds the parsing both it and the validator use. All three layers have been run against the live model. (D72, D76)
- `scripts/drift_test.py`: the drift test, both arms. Needs the key. (D74)
- `scripts/correct_corpus.py`: the reviewed route for correcting an existing corpus line; every correction needs a `why`, dry run by default. (D81)
- The guardrail is a template check, not a meaning check: it catches a broken verb ending or a non-word, and it does **not** catch a wrong case marker or a modal that has lost its subordinator. `check` prints an advisory for the modal case. Read the parser-produced gloss, not the verdict. (D76)
- See `scripts/README.md` for what each script does.

## The method
- `corpus/` is the deliverable; spec and lexicon are scaffolding. Done = a cold session with only the train corpus translates held-out sentences both ways. (D2, D3)
- Acceptance test: the two directions go to **different** agents, so no agent sees both sides of a held sentence (D75). And a held sentence may not be a copy of a train sentence, which is the same leak one level up — the validator now fails on it (D93).
- Drift test: two arms, the long session and the fresh-session control. A run without the control is not interpretable. (D74)
- Words enter only via `scripts/validate.py --add`; run `scripts/validate.py` before every commit. Multi-syllable forms are rejected if they are Korean words (`data/ko_frequency.json`) or if they read as a shorter root plus a verb ending. (rules 4, 6; D55)
- Batches: one subagent per domain with a disjoint first-syllable pool; `scripts/merge_batch.py BATCH_DIR` dry-runs, the maintainer reviews, `--apply` writes. It only appends. (D58, D66)
- A convention that lives only in prose gets broken, so the validator counts both conventions on every run — but **a check that has never been shown to catch a real violation is not evidence of anything.** The D78 check reported 1 while 14 lines were wrong; it now catches 14 of 14 on those forms. **Baseline: 0 for D78, 1 for D79** (s0005, a known false positive). A rise means new drift. (D82, D87)
- Codepoints: BMP PUA is stripped by Claude's input pipeline (D20); Yi Syllables trip a content classifier on the chat surface (D52). Neither is usable.

## Open
- No open grammar gaps: G1–G29 all closed (D59–D65, D68–D71, D78, D79, D89). New gaps get logged as G30+.
- **The acceptance test has not been passed.** Test 4 scored 90.1% on English → stone but 89.9% once its two invalid items were discounted, so the ≥90% bar is not met. Everything it faulted is now corrected; the next run on this corpus is the measurement.
- D11 coverage: every word appears in ≥3 train sentences (met first at D85, still true). 31 features are still under 10; the rarest constructions need more examples.
- One language ambiguity left standing: the true/hold root does existence and truth both, so an argument plus that root negated reads as both "there is no X" and "X is not true". (D76)
- O5 teaching materials (after the corpus). O7 formal code register (later). Derivation suffixes: when roots need them.

## Tests
- Test 1 (Yi glyphs): 13/13 comprehension, 12/13 exact production. Test 2 (Hangul): 21/21 and 20/21. Both were run before D75, so both had the direction leak: discount them.
- Test 3 (2026-09-15, all 107 held, directions split): stone → English 107/107 meaning-correct; English → stone 87/107 = 81.3% exact — **failed** the ≥90% bar. 11 of 20 misses were the corpus declining to decide or contradicting itself; 4 were real model misses; 3 changed meaning. `tests/results/2026-09-15.md`.
- **Test 4 (2026-09-15, all 121 held, 8 agents, directions split): stone → English 121/121 meaning-correct — passes. English → stone 109/121 = 90.1% as scored, 107/119 = 89.9% discounting two leaked items (D93) — does not meet the bar.** On the same 107 sentences test 3 used: 96/107 = 89.7%, up 8.4 points. **Every miss is well formed, every miss preserves meaning, and none is a real model miss** (test 3 had 4 real misses and 3 meaning changes). The general-evidential class that dominated test 3 is gone; the word-order class fell from 6 to 3 only because D78 was under-applied. `tests/results/2026-09-15-b.md`.
- **Drift test 1 (2026-09-15): no drift on all three signals.** Probe divergence 0/12; filler accuracy 28/40 in the long session against 24/40 in the fresh-session control, with the long session right on all 4 disagreements. Zero Korean leakage in 461 tokens. `tests/results/2026-09-15-drift.md`.
- Bar: 100% / ≥90% with every miss grammatical. (D50)

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

## Corpus — 1009 sentences, 121 held
`corpus/corpus.jsonl`; writing conventions and the English cue phrases in `corpus/README.md`. Constructions decided so far: imperative = you + intend stance; existence and having = the hold root, no have and no exist; equative = second term takes the verb ending, no copula; recipient = location case; and = juxtaposition or the with word, with or and but as words; if follows its clause; quantifiers every/none are determiners and bare arguments are number-neutral; no passive, drop the subject and keep the object marker; comparison uses the from word; manner = quality + the with word; because = clause + the from word; become = stative clause + begin; ordinals = numeral after the root; still = the continue root; until/since = clause + time + before/after; an alternative question coordinates the smallest constituent that differs. (D43–D49, D51, D56–D70, D89)
- s0866–s0889 added 2026-09-15 for the constructions test 3 found too thin: we-exclusive, region nominals, how-often, clause-as-subject, causal against temporal since. All four pass in test 4. (D77)
- s0890–s0992 added 2026-09-15 with the ten calendar, clock and utility roots. (D85)
- s0993–s1009 added 2026-09-15 for the three constructions test 4 found too thin: quantified duration with the measure root, a past-marked while-clause, the English perfect of an event, plus subject alternation in an alternative question. No new roots. (D92)
- Thirty lines corrected in the same session through `correct_corpus.py` (D87–D93): fifteen D78 word-order violations D78 itself had left, four on the intend/predict endings, two on the alternative question, two on the say/message carve, four English sides that said something their script did not, and three held-or-train duplicates.

## Editing this file
Rewrite it whole. Patching it by string replacement has silently failed before (D73).
