# STATE — read this first, every session

Current state of the language and the method, kept short on purpose. `decisions.md` is the append-only history with rationale; read the entries cited here when you need the why. When anything changes: append to `decisions.md`, then update this file and the spec it touches.

## The language
- Purpose: asking, code, discussion, engineering and science talk between two people; the corpus is its codex. (D1, D34)
- Script: 74 syllable glyphs as Hangul blocks that spell their own sound (initial + vowel, no final), `spec/codepoints.json` from `scripts/compose_hangul.py`; sounds in `spec/phonology.md`. 1–3 tokens per glyph. Priors accepted and to be watched with the drift test. (D28, D37, D52)
- No Latin form of any word exists anywhere. IPA describes sounds only. (CLAUDE.md rule 3)
- Grammar, `spec/grammar.md`: SOV. One open root class; roots are neither noun nor verb. Verb template: root, negation, tense, evidential, stance, subordinator; only the evidential is mandatory. Arguments bare, or root plus one case marker (object, location, possessor). A pronoun, the interrogative or a numeral before a root is a determiner. No adjectives, no adverbs. (D26, D29–D33, D44)
- Evidentials, obligatory: direct, reported, inferred, general. Stance, optional: intend, predict, propose, trust, risk, assert. Tense: past, present unmarked, future (temporal only). (D30, D31, D34)
- Semantic carving, `lexicon/README.md`: knowing ×3, error ×3, asking ×3, change ×3; experiment/test/try = 1. (D35)
- Target: 300 lexicon entries (D54); 196 today: 53 roots from the first subagent batch (code, experiments, discussion), D58. New roots are two syllables, coined from corpus need, checked against Korean for collisions. Corpus grows alongside to ~1000 sentences for coverage.

## The method
- `corpus/` is the deliverable; spec and lexicon are scaffolding. Done = a cold session with only the train corpus translates held-out sentences both ways. (D2, D3)
- Words enter only via `scripts/validate.py --add`; run `scripts/validate.py` before every commit. Multi-syllable forms are rejected if they are Korean words (`data/ko_frequency.json`). (rules 4, 6; D55)
- Codepoints: BMP PUA is stripped by Claude's input pipeline (D20); Yi Syllables trip a content classifier on the chat surface (D52). Neither is usable.

## Open
- Grammar gaps G4, G5, G7–G12 in decisions.md (G1–G3, G6 closed by D59–D62; can, want/should, we, quantifiers, comparison, passives, N times, compounds, while). Decide one at a time; agents leave out sentences that need them.
- O5 teaching materials (after corpus). O7 formal code register (later). Derivation suffixes: when roots need them.

## Tests
- Test 1 (Yi): 13/13, 12/13. Test 2 (Hangul): 21/21, 20/21, the miss a corpus gap since fixed; agent recognised it as constructed, not Korean. Bar: 100% / ≥90% with misses grammatical. `tests/results/`. (D50, D53)

## Lexicon
- 25 grammatical pieces coined, `lexicon/lexicon.json` w0001–w0025. Slot = consonant, value = vowel; pronouns = bare vowels. (D39)
- 13 carve roots coined, w0026–w0038: each carve is a consonant family, members differ by vowel. (D42)
- 20 inquiry-core roots, w0039–w0058: one interrogative root does all question words; number/count is one root. (D45)
- 19 more, w0059–w0077: 7 statives (different/false/broken are negations or fault), before/after, numerals 1–10 with quinary 6–9 and a ten rule. Deixis = pronoun + location/time. (D48)
- Syllable budget: 71 of 74 single syllables used; 3 left, all reserve. Glyph identity changed in D52; every word kept its sound. New roots are two syllables unless a reserve syllable is spent by decision.

## Corpus
- 808 sentences, 94 held, `corpus/corpus.jsonl`; conventions in `corpus/README.md`. Imperative = you + intend stance. Existence and having = the hold root; no have, no exist. Equatives = second term takes the verb ending; no copula. Recipient = location case. Or and but exist; and is juxtaposition or with. If follows its clause; condition first, general evidential on it. Ability is a root over a subordinate clause. Bare arguments are number-neutral; every/all and no/none are determiners. Four modal roots (able, want, should, allow) take a subordinate clause. No passive: drop the subject, keep the object marker. Comparison uses the from word. (D43, D46, D47, D49, D51, D56, D57, D59, D60, D61–D65)

## Next
Close G13 first, then the rest. Next subagent batch: `scripts/merge_batch.py BATCH_DIR` to dry-run, review, `--apply`. Re-test at ~500 sentences. Open grammar: valency (passive), plural marking without a numeral.
