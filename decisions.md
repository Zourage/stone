# Decisions log

Append-only. Newest at the bottom. Each entry: date, decision, why. Reversals are new entries, not edits.

## 2026-09-14 — Founding decisions (from the initial design conversation)

**D1. Purpose.** A language two people learn for real, in their heads. The only durable representation on one side is memory. All files live with the maintainer.

**D2. Corpus-centric structure.** The parallel corpus is the primary artifact and the key. Grammar spec and lexicon are scaffolding used to *build* the corpus with proper coverage; they are not the deliverable. Rationale: an LLM absorbs a language better from applied examples than from stated rules, and one artifact beats three.

**D3. Acceptance test.** Done means: a cold session with only `corpus/` in context translates held-out sentences correctly both directions. Failures point to which words/constructions need more corpus examples. Iterate until pass.

**D4. Script: brand-new glyphs, syllabary, PUA codepoints, read raw.** One glyph per syllable on Unicode Private Use Area codepoints. The LLM reads the glyphs directly; there is no transliteration layer anywhere. Rationale: PUA has zero training-data priors, so no drift in long sessions. Cost accepted: ~2–2.5× the tokens of Latin transliteration.

**D5. Rejected: Latin transliteration as working layer.** It's cheap (~1× tokens) and drift-free, but the ground truth would be Latin strings under a costume. Rejected on purity grounds after the cost of D4 was judged affordable.

**D6. Rejected: hijacking Hangul / CJK codepoints for single-token glyphs.** Cheap, but those codepoints carry sharp priors; in long sessions output drifts toward real Korean/Chinese sequences, and the drift is invisible because the custom font renders it in our glyphs. Shelved as a curiosity; an experiment is described in `scripts/measure_codepoints.py` if ever revisited.

**D7. Syllable inventory ≈ 65.** Proposed default: 12 consonants × 5 vowels + 5 bare vowels. Comparable to learning kana. Fewer → long words; more → memorization cost. Final count is OPEN (see below).

**D8. Phonology is a memory aid only.** Text-only language, but people retain words by subvocalizing, so every syllable must be pronounceable. Inventory kept tiny for that reason.

**D9. Glyph design is componential.** Each glyph visibly composes a consonant element and a vowel element, so 65 glyphs come from 12 + 5 parts. Constraints: distinct at phone-screen size; consistent stroke logic; no resemblance to Latin, Arabic, Cyrillic, or Greek letterforms.

**D10. Codepoint assignment is measured, not guessed.** Before glyphs are assigned, measure which PUA codepoints tokenize as 2 tokens vs 3 and assign syllables to the cheapest. Frequent syllables get the cheapest codepoints.

**D11. Corpus coverage rules.** Every word appears in ≥3 distinct contexts. Every grammatical feature (tense, negation, questions, plural, possession, subordination, evidentiality if adopted) has multiple examples. `scripts/validate.py` enforces coverage; nothing appears once.

**D12. Originality lives in the lexicon, not the corpus.** The corpus is where the language shows up; what makes it a language rather than a cipher is semantic carving: which distinctions it makes that English/Persian don't, and which it collapses. Candidate features to decide: evidentiality (saw / heard / suspect), lexicalized distinctions for kinds of silence, trust, risk.

**D13. Vocabulary strategy.** Zipf: most frequent words are one syllable. Derivation via a small set of suffixes so each memorized root yields several words. Build the core few hundred for actual conversation topics first; coin from use after that. Check every coined word against multilingual wordlists to avoid collisions with real words.

**D14. Workflow.** Git repo is the source of truth. A Claude Project mirrors the spec for design sessions; Claude Code (local or web) works the repo for anything that touches files or runs code. Every session, either surface, reads this file first and appends to it.

**D15. LLM-rot mitigations.** Files are memory, not the model. Lexicon is structured data (JSON), not prose. Validators catch phonotactic violations and duplicate glosses. A fixed translation test suite catches grammar drift. No word enters the lexicon without passing the validator.

**D16. Name.** Repo is `stone` (the Rosetta Stone as the key). Placeholder. The language names itself in its own syllables once it has words; the repo adopts that name then.

### OPEN
- O1. Final syllable count (D7).
- O2. Grammar lean: Persian-shaped or English-shaped morphology/word order.
- O3. Which semantic distinctions to build in (D12).
- O4. Domain and size of the first vocabulary tranche.
- O5. Teaching materials for the learner (what the second person studies from).

## 2026-09-14 — Session 1 (Claude Code)

**D17. Codepoint cost is measured as marginal tokens per glyph inside a run, not tokens of an isolated glyph.** `scripts/measure_codepoints.py` implemented: for each codepoint in U+E000–U+F8FF it sends a run of 16 copies to `count_tokens`, subtracts the empty-message baseline, and divides by 16. One request per codepoint, concurrent, resumable, written to `spec/codepoints_cost.json` cheapest-first. Rationale: BPE merges across neighbours, so a glyph's cost inside a word (the case that matters) differs from its cost alone; a run averages the boundary effects out. Not yet run — no API key in this environment. `--dry-run` produces a byte-count estimate marked `estimated: true` that must never be used for assignment.
