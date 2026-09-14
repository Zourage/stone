# STATE — read this first, every session

Current state of the language and the method, kept short on purpose. `decisions.md` is the append-only history with rationale; read the entries cited here when you need the why. When anything changes: append to `decisions.md`, then update this file and the spec it touches.

## The language
- Purpose: asking, code, discussion, engineering and science talk between two people; the corpus is its codex. (D1, D34)
- Script: 74 syllable glyphs on Yi codepoints, `spec/codepoints.json`; sounds in `spec/phonology.md`; own glyphs to be designed, `spec/orthography.md`. 3 tokens per glyph. (D23, D28, D37)
- No Latin form of any word exists anywhere. IPA describes sounds only. (CLAUDE.md rule 3)
- Grammar, `spec/grammar.md`: SOV. One open root class; roots are neither noun nor verb. Verb template: root, negation, tense, evidential, stance, subordinator; only the evidential is mandatory. Arguments bare, or root plus one case marker (object, location, possessor). No adjectives, no adverbs. (D26, D29–D33)
- Evidentials, obligatory: direct, reported, inferred, general. Stance, optional: intend, predict, propose, trust, risk, assert. Tense: past, present unmarked, future (temporal only). (D30, D31, D34)
- Semantic carving, `lexicon/README.md`: knowing ×3, error ×3, asking ×3, change ×3; experiment/test/try = 1. (D35)
- First tranche: ~25 grammatical pieces (one syllable each), then 150 roots in frequency order; ~9 single syllables held in reserve. (D36)

## The method
- `corpus/` is the deliverable; spec and lexicon are scaffolding. Done = a cold session with only the train corpus translates held-out sentences both ways. (D2, D3)
- Words enter only via `scripts/validate.py --add`; run `scripts/validate.py` before every commit. (rules 4, 6)
- Codepoints: BMP PUA is stripped by Claude's input pipeline; never use it. (D20)

## Open
- O5 teaching materials (after corpus). O7 formal code register (later). Number marking and derivation suffixes: decide when roots need them.

## Lexicon
- 25 grammatical pieces coined, `lexicon/lexicon.json` w0001–w0025. Slot = consonant, value = vowel; pronouns = bare vowels. (D39)

## Next
Coin the first roots (D35 carves, then the inquiry core, D36) and write the first corpus sentences as soon as a few roots exist.
