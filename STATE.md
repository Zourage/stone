# STATE — read this first, every session

Current state of the language and the method, kept short on purpose. `decisions.md` is the append-only history with rationale; read the entries cited here when you need the why. When anything changes: append to `decisions.md`, then update this file and the spec it touches.

## The language
- Purpose: asking, code, discussion, engineering and science talk between two people; the corpus is its codex. (D1, D34)
- Script: 74 syllable glyphs as Hangul blocks that spell their own sound (initial + vowel, no final), `spec/codepoints.json` from `scripts/compose_hangul.py`; sounds in `spec/phonology.md`. 1–3 tokens per glyph. Priors accepted, watched by the drift test. (D28, D37, D52)
- No Latin form of any word exists anywhere. IPA describes sounds only. (CLAUDE.md rule 3)
- Grammar, `spec/grammar.md`: SOV. One open root class; roots are neither noun nor verb. Verb template: root, negation, tense, evidential, stance, subordinator; only the evidential is mandatory. Arguments bare, or root plus one case marker (object, location, possessor). A pronoun, the interrogative, a numeral or a root before a root is a determiner or compound. No adjectives, no adverbs. (D26, D29–D33, D44, D48, D64)
- Evidentials, obligatory: direct, reported, inferred, general. Stance, optional: intend, predict, propose, trust, risk, assert. Tense: past, present unmarked, future (temporal only). Irrealis clauses (conditions, modal complements) take the general evidential. (D30, D31, D34, D60, D61)
- Four modal roots share a syllable and one construction over a subordinate clause: able, want, should, allow. (D61, D63)
- Semantic carving, `lexicon/README.md`: knowing ×3, error ×3, asking ×3, change ×3; experiment/test/try = 1. (D35)

## Tools
- `scripts/translate.py`: gloss, check, lookup, examples need no key; to-english, to-stone, roundtrip need `OPENROUTER_API_KEY`. `scripts/stonelib.py` holds the parsing both it and the validator use. See `scripts/README.md`. (D72)

## The method
- `corpus/` is the deliverable; spec and lexicon are scaffolding. Done = a cold session with only the train corpus translates held-out sentences both ways. (D2, D3)
- Words enter only via `scripts/validate.py --add`; run `scripts/validate.py` before every commit. Multi-syllable forms are rejected if they are Korean words (`data/ko_frequency.json`) or if they read as a shorter root plus a verb ending. (rules 4, 6; D55)
- Batches: one subagent per domain with a disjoint first-syllable pool; `scripts/merge_batch.py BATCH_DIR` dry-runs, the maintainer reviews, `--apply` writes. (D58, D66)
- Codepoints: BMP PUA is stripped by Claude's input pipeline (D20); Yi Syllables trip a content classifier on the chat surface (D52). Neither is usable.

## Open
- No open grammar gaps: G1–G26 all closed (D59–D65, D68–D71). New gaps get logged as G27+.
- Vocabulary gaps for a coining batch: calendar and clock units above the day (D71).
- O5 teaching materials (after the corpus). O7 formal code register (later). Derivation suffixes: when roots need them.

## Tests
- Test 1 (Yi glyphs): 13/13 comprehension, 12/13 exact production. Test 2 (Hangul): 21/21 and 20/21, the miss a corpus gap since fixed; the agent called it constructed, not Korean. Bar: 100% / ≥90% with every miss grammatical. `tests/results/`. (D50, D53)
- Drift test (D15) has never been run. It is the instrument for the priors accepted in D52.

## Lexicon — 196 entries, target 300 (D54)
- w0001–w0025 grammatical pieces, one syllable, slot = consonant and value = vowel; pronouns are the bare vowels. (D39)
- w0026–w0038 carve roots, each carve a consonant family. (D42)
- w0039–w0058 inquiry core; one interrogative root does every question word. (D45)
- w0059–w0077 statives, numerals 1–10 quinary, before/after; deixis from pronoun + location/time. (D48)
- w0078–w0130 first subagent batch: code, experiments, discussion. (D58)
- w0131–w0139 or, but, if, able, want, should, allow, every/all, no/none. (D59–D63)
- w0140–w0196 second subagent batch: physical handling, time and process, work. (D66)
- Syllable budget: 71 of 74 single syllables used, 3 in reserve. New roots are two syllables unless a reserve syllable is spent by decision.

## Corpus — 865 sentences, 107 held
`corpus/corpus.jsonl`; writing conventions and the English cue phrases in `corpus/README.md`. Constructions decided so far: imperative = you + intend stance; existence and having = the hold root, no have and no exist; equative = second term takes the verb ending, no copula; recipient = location case; and = juxtaposition or the with word, with or and but as words; if follows its clause; quantifiers every/none are determiners and bare arguments are number-neutral; no passive, drop the subject and keep the object marker; comparison uses the from word; manner = quality + the with word; because = clause + the from word; become = stative clause + begin; ordinals = numeral after the root; still = the continue root; until/since = clause + time + before/after. (D43–D49, D51, D56–D70)

## Next
Third acceptance test on the 107 held sentences, and the first drift test; both need a container with `OPENROUTER_API_KEY`. Then the third subagent batch toward 300 entries, calendar and clock units among them.

## Editing this file
Rewrite it whole. Patching it by string replacement has silently failed before (D73).
