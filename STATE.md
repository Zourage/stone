# STATE — read this first, every session

Current state of the language and the method, kept short on purpose. `decisions.md` is the append-only history with rationale; read the entries cited here when you need the why. When anything changes: append to `decisions.md`, then update this file and the spec it touches.

## The language
- Purpose: asking, code, discussion, engineering and science talk between two people; the corpus is its codex. (D1, D34)
- Script: 74 syllable glyphs as Hangul blocks that spell their own sound (initial + vowel, no final), `spec/codepoints.json` from `scripts/compose_hangul.py`; sounds in `spec/phonology.md`. 1–3 tokens per glyph. Priors accepted in D52 and now tested: acceptance test 3 and the first drift test both found no Korean reading and no slide toward Korean. (D28, D37, D52)
- No Latin form of any word exists anywhere. IPA describes sounds only. (CLAUDE.md rule 3)
- Grammar, `spec/grammar.md`: SOV. One open root class; roots are neither noun nor verb. Verb template: root, negation, tense, evidential, stance, subordinator; only the evidential is mandatory. Arguments bare, or root plus one case marker (object, location, possessor). A pronoun, the interrogative, a numeral or a root before a root is a determiner or compound. No adjectives, no adverbs. (D26, D29–D33, D44, D48, D64)
- Evidentials, obligatory: direct, reported, inferred, general. Stance, optional: intend, predict, propose, trust, risk, assert. Tense: past, present unmarked, future (temporal only). Irrealis clauses (conditions, modal complements) take the general evidential. (D30, D31, D34, D60, D61)
- Four modal roots share a syllable and one construction over a subordinate clause: able, want, should, allow. (D61, D63)
- Semantic carving, `lexicon/README.md`: knowing ×3, error ×3, asking ×3, change ×3; experiment/test/try = 1. (D35)

## Tools
- `scripts/translate.py`: gloss, check, lookup, examples need no key; to-english, to-stone, roundtrip need `OPENROUTER_API_KEY`. `scripts/stonelib.py` holds the parsing both it and the validator use. All three layers have now been run against the live model. (D72, D76)
- `scripts/drift_test.py`: the drift test, both arms. Needs the key. (D74)
- The guardrail is a template check, not a meaning check: it catches a broken verb ending or a non-word, and it does **not** catch a wrong case marker or a modal that has lost its subordinator. `check` prints an advisory for the modal case. Read the parser-produced gloss, not the verdict. (D76)
- See `scripts/README.md` for what each script does.

## The method
- `corpus/` is the deliverable; spec and lexicon are scaffolding. Done = a cold session with only the train corpus translates held-out sentences both ways. (D2, D3)
- Acceptance test: the two directions go to **different** agents, so no agent sees both sides of a held sentence. Tests 1 and 2 had that leak. (D75)
- Drift test: two arms, the long session and the fresh-session control. A run without the control is not interpretable. (D74)
- Words enter only via `scripts/validate.py --add`; run `scripts/validate.py` before every commit. Multi-syllable forms are rejected if they are Korean words (`data/ko_frequency.json`) or if they read as a shorter root plus a verb ending. (rules 4, 6; D55)
- Batches: one subagent per domain with a disjoint first-syllable pool; `scripts/merge_batch.py BATCH_DIR` dry-runs, the maintainer reviews, `--apply` writes. It only appends. (D58, D66)
- Codepoints: BMP PUA is stripped by Claude's input pipeline (D20); Yi Syllables trip a content classifier on the chat surface (D52). Neither is usable.

## Open
- **G27. Where a clause-initial adverbial goes relative to the subject.** Undecided, and the corpus contradicts itself: train s0857 against train s0858, and held s0708 against train s0857. Six of the twenty misses in acceptance test 3. Needs a decision before the next acceptance run; either resolution rewrites existing corpus lines. (D77)
- **G28. The evidential on a generic statement whose English carries no cue.** `corpus/README.md` says direct; the train split has it general in s0029, s0059, s0483, s0714, s0793. Three of the twenty misses, and the only three that change meaning. (D77)
- **O8. No route for correcting an existing corpus line.** `merge_batch.py` only appends and rule 4 forbids hand-editing, so four known-defective held sentences stand uncorrected: s0750 (addressee case, against D67), s0746 (missing future marker), s0860 (causal since written as temporal since), s0532 (comparison written as a time periphrasis). (D77)
- Vocabulary gap for a coining batch: calendar and clock units above the day (D71).
- One language ambiguity left standing: the true/hold root does existence and truth both, so an argument plus that root negated reads as both "there is no X" and "X is not true". (D76)
- O5 teaching materials (after the corpus). O7 formal code register (later). Derivation suffixes: when roots need them.

## Tests
- Test 1 (Yi glyphs): 13/13 comprehension, 12/13 exact production. Test 2 (Hangul): 21/21 and 20/21. Both were run before D75, so both had the direction leak: discount them.
- **Test 3 (2026-09-15, all 107 held, directions split): stone → English 107/107 meaning-correct — passes. English → stone 87/107 = 81.3% exact — fails the ≥90% bar.** Every miss is well formed; 17 of 20 preserve meaning. 11 of the 20 are G27, G28 or a defective held sentence, so the same answers score 98/107 = 91.6% once those are settled. 4 are thin-coverage, now fixed; 4 are real misses; 1 is gold taking a minority form. `tests/results/2026-09-15.md`.
- **Drift test 1 (2026-09-15): no drift on all three signals.** Probe divergence 0/12; filler accuracy 28/40 in the long session against 24/40 in the fresh-session control, with the long session right on all 4 disagreements and never wrong where the control was right; zero Korean leakage in 461 tokens. A long session made output more faithful, not less. It did surface a stable guardrail hole (modal without subordinator) that is now advised on. `tests/results/2026-09-15-drift.md`.
- Bar: 100% / ≥90% with every miss grammatical. (D50)

## Lexicon — 196 entries, target 300 (D54)
- w0001–w0025 grammatical pieces, one syllable, slot = consonant and value = vowel; pronouns are the bare vowels. (D39)
- w0026–w0038 carve roots, each carve a consonant family. (D42)
- w0039–w0058 inquiry core; one interrogative root does every question word. (D45)
- w0059–w0077 statives, numerals 1–10 quinary, before/after; deixis from pronoun + location/time. (D48)
- w0078–w0130 first subagent batch: code, experiments, discussion. (D58)
- w0131–w0139 or, but, if, able, want, should, allow, every/all, no/none. (D59–D63)
- w0140–w0196 second subagent batch: physical handling, time and process, work. (D66)
- Syllable budget: 71 of 74 single syllables used, 3 in reserve. New roots are two syllables unless a reserve syllable is spent by decision.

## Corpus — 889 sentences, 107 held
`corpus/corpus.jsonl`; writing conventions and the English cue phrases in `corpus/README.md`. Constructions decided so far: imperative = you + intend stance; existence and having = the hold root, no have and no exist; equative = second term takes the verb ending, no copula; recipient = location case; and = juxtaposition or the with word, with or and but as words; if follows its clause; quantifiers every/none are determiners and bare arguments are number-neutral; no passive, drop the subject and keep the object marker; comparison uses the from word; manner = quality + the with word; because = clause + the from word; become = stative clause + begin; ordinals = numeral after the root; still = the continue root; until/since = clause + time + before/after. (D43–D49, D51, D56–D70)
- s0866–s0889 added 2026-09-15 for the constructions test 3 found too thin: we-exclusive (which had none), region nominals, how-often, clause-as-subject, causal against temporal since. No new roots. (D77)

## Next
Decide G27 and G28, then build the correction route (O8) and fix the four defective held sentences — those three together are what stands between the current 81.3% and the bar. Then re-run acceptance test 3 on the same held set. After that the third subagent batch toward 300 entries, calendar and clock units among them.

## Editing this file
Rewrite it whole. Patching it by string replacement has silently failed before (D73).
