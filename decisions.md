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

**D18. Measurement runs through OpenRouter, on Haiku.** No Anthropic Console account; an OpenRouter key exists. `measure_codepoints.py --backend openrouter` sends a 1-token completion per codepoint and reads Anthropic's native prompt count from OpenRouter's generation-stats endpoint (its completion response reports a normalized count, which is the wrong number). Tokenizer is shared across Claude models, so Haiku's count is the count; whole PUA block costs well under a dollar. The API is used for this measurement only; all language work happens in subscription sessions and bills nothing per token.

## 2026-09-14 — Session 2 (Claude Code, measurement run)

**D19. OpenRouter native count comes from the completion response, not the generation endpoint.** First live run of `--backend openrouter` failed: `/api/v1/generation?id=` returns 404 for several seconds after the completion, and 404 was not a retried status. Fixed by dropping that lookup entirely: sending `"usage": {"include": true}` makes `usage.prompt_tokens` in the completion response the provider's native count (verified equal to `native_tokens_prompt`, 8, while the normalized `tokens_prompt` was 17). One request per codepoint, no lag. D18's claim that the completion response only reports a normalized count was true without usage accounting and is superseded.

**D20. The Basic Multilingual Plane PUA (U+E000–U+F8FF) is stripped from Claude's input before tokenization. D4 cannot stand as written.** Every string tested in that block costs exactly the baseline (a run of 64 glyphs adds 0 tokens) and the model, asked to count the characters it was given, reports none. Identical on the Anthropic, Amazon Bedrock and Google Vertex routes, on Haiku 4.5 and Sonnet 4.5, and in this Claude Code session itself (three PUA glyphs printed between two Latin letters arrive as the two letters alone). OpenRouter is not the cause: the same glyphs reach GPT-4o-mini (2 tokens/glyph) and Llama 3.1 (3 tokens/glyph). Control characters (U+0001) are stripped the same way; U+FFFD, zero-width joiner, unassigned BMP codepoints and every real script tested are not. The glyph must live somewhere else. Measured on the same day, with the same method: Supplementary PUA-A (plane 15, U+F0000–U+FFFFD) and PUA-B (plane 16, U+100000–U+10FFFD) are NOT stripped and cost a flat 4 tokens per glyph (64-codepoint sample at stride 1024 of each plane, `spec/codepoints_cost_pua-a_sample.json`, `spec/codepoints_cost_pua-b_sample.json`; every sample identical, i.e. byte-level fallback on a 4-byte UTF-8 sequence, no merges). That is 4× per syllable glyph where D4 budgeted 2–2.5×, and there is nothing to optimise by assignment: every codepoint in those planes costs the same. Reopened as O6 below; the choice (accept 4 tokens per syllable in plane 15, or revisit D5/D6) is a design decision and is not made here. `measure_codepoints.py` now has `--block pua-a|pua-b`, `--stride`, and reports zero-cost codepoints under `stripped` rather than in `costs`, since cost 0 means unusable, not cheap.

### OPEN (added)
- O6. Where glyphs live now that BMP PUA is invisible to Claude (D20): plane-15/16 PUA at a flat 4 tokens/glyph, or a reversal of D5/D6.

**D21. Full BMP PUA histogram: 6400 of 6400 codepoints at cost 0.** `spec/codepoints_cost.json` now holds the complete measurement of U+E000–U+F8FF on Haiku 4.5 via OpenRouter (16-glyph runs, baseline 8 tokens, one request per codepoint). There is no cheapest range: the whole block, contiguous from U+E000 to U+F8FF with no surviving sub-range, is stripped before tokenization, so the file's `costs` table is empty and all 6400 codepoints sit under `stripped`. Nothing in this block may be used for assignment. The only measured usable PUA is planes 15 and 16 at a flat 4 tokens per glyph (D20); the D10 assignment step is moot there because every codepoint costs the same.

## 2026-09-14 — Session 3 (Claude Code, O6 measurement)

**D22. Data for O6: token cost and visibility of thin-training-data BMP scripts. No choice made; D4, D5, D6 unchanged.** Same method as D20 (`measure_codepoints.py --backend openrouter`, Haiku 4.5, run of 16 copies, marginal tokens per glyph, baseline 8 tokens), one sample file per block under `spec/codepoints_cost_<block>_sample.json`. "Model sees it" is the D20 test: the first 8 sampled glyphs, one each, in brackets, and the question "how many of these 8 characters are non-ASCII?"; the reply is stored verbatim in each file's `meta.see_check`. The Latin row is a control: 20 ASCII consonant+vowel strings measured by the identical method so the D5 figure is on the same footing. Those strings are tokenizer probes, not words, not transliterations of anything; the language has no Latin form (CLAUDE.md rule 3).

| block | range | stride | n | tokens/glyph min / typical / max | stripped? | model sees it (reply of 8) |
|---|---|---|---|---|---|---|
| yi | U+A000–A48C | 18 | 65 | 3.125 / 3.125 / 3.125 | no | 8 |
| syllabics | U+1400–167F | 10 | 64 | 3.000 / 3.125 / 3.125 | no | 8 |
| cherokee | U+13A0–13F5 | 1 (full) | 86 | 3.188 / 3.188 / 3.188 | no | 8 |
| vai | U+A500–A62B | 5 | 60 | 3.000 / 3.125 / 3.125 | no | 8 |
| ogham | U+1680–169C | 1 (full) | 29 | 0.062 / 3.125 / 3.125 | no | 7 |
| bamum | U+A6A0–A6EF | 1 (full) | 80 | 3.125 / 3.125 / 3.125 | no | 8 |
| hangul | U+AC00–D7A3 | 512 | 22 | 1.0 / 2.0 / 3.0 (4 at 1, 12 at 2, 6 at 3) | no | 8 |
| latin-cv (control) | 20 ASCII CV probes | – | 20 | 0.562 / 0.562 / 1.0 | no | n/a (ASCII) |
| pua-a, pua-b (D20, for reference) | planes 15–16 | 1024 | 64 each | 4.0 / 4.0 / 4.0 | no | – |
| pua (D20, for reference) | U+E000–F8FF | 1 | all | 0 | yes | 0 |

Reading the numbers. Every 3-byte block above (yi, syllabics, cherokee, vai, ogham, bamum) costs exactly 3 tokens per glyph plus 2–3 boundary tokens per run of 16: byte-level fallback on the 3-byte UTF-8 sequence, no merges, no codepoint cheaper than any other, so nothing to optimise by assignment inside these blocks either. The single Ogham outlier is U+1680 OGHAM SPACE MARK, a whitespace character: 16 copies collapse to 1 token, and it was among the 8 glyphs of the see-check, whose reply of 7 is consistent with it being read as a space (not stripped: cost is 1 token per run, not 0). Hangul is the only real-script block with merges: 1–3 tokens per syllable depending on the syllable, i.e. the tokenizer has priors on it, which is exactly the D6 concern. The Latin control's typical 0.562 is an artifact of the run method on ASCII: BPE merges repeats of the same pair (16 copies of one pair cost 9–16 tokens). A one-off cross-check with 16 *distinct* probe pairs in one run gave 14 tokens unspaced (0.875 per pair) and 16 tokens space-separated (1.0 per pair), so the D5 baseline for Latin is ~1 token per CV syllable, and the ratios are: Latin 1 : Hangul 1–3 : thin BMP scripts 3 : plane-15/16 PUA 4.

Training-data prior per block, from general knowledge, all estimates: **Yi** (Nuosu syllabary): very little digital text; official use in Liangshan, some government and school material, no substantial web corpus. **Canadian Aboriginal Syllabics**: small but real, the largest of the six; Inuktitut has a sizeable parallel corpus (Nunavut Hansard) and a small Wikipedia, plus Cree and Ojibwe material. **Cherokee**: very little; a small Wikipedia, Cherokee Nation publications, scripture translations. **Vai**: almost none; a few thousand users, a handful of digitised texts. **Ogham**: effectively none as running text, it is a 20-letter alphabet known from ~400 medieval stone inscriptions, and nearly all Ogham online is Unicode charts and transliteration tables. **Bamum**: effectively none; a near-extinct script surviving in a few hundred manuscripts, digitised mostly as images. **Hangul**: enormous (Korean is a top-tier web language), which is the D6 comparison point, not a candidate.

## 2026-09-14 — Session 4 (Claude Code, O6 and part of O2 decided)

**D23. Glyphs live on Yi Syllables codepoints (U+A000–U+A48C), assigned by seeded random draw. Reverses the codepoint choice in D4; the rest of D4 stands.** Chosen over plane-15/16 PUA (4 tokens/glyph, D20) and over Canadian Syllabics (real Inuktitut corpus, D22). Cost accepted: a flat 3 tokens per glyph, 3× Latin, not the 2–2.5× D4 budgeted. Why Yi: not stripped, near-zero training data, 1,165 codepoints for a ~65-syllable inventory, byte-level fallback so the model has no learned representation of the glyphs to carry priors. Assignment is a fixed-seed random spread across the block, never contiguous from U+A000 and never following Yi's own phonetic ordering, so nothing about our syllable structure correlates with Nuosu. `scripts/assign_codepoints.py` does the draw once O1 fixes the count. The real Yi letterforms are fallback rendering only; our font maps each codepoint to our own glyph (D9 unchanged).

**D24. D10 retired.** Every usable block measures flat: nothing to optimise by assignment. Frequency-weighted assignment is dropped.

**D25. The language is not a reskin. Commitments, in force from the first word:** (a) every root is coined, none borrowed (D13 restated); (b) word boundaries must not align with English: some stone words cover an English phrase, some English words split on a distinction English lacks (D12); (c) no bilingual gloss list is a teaching artifact, only the corpus (D2 restated); (d) `validate.py` gets a relexification check: a corpus sentence whose stone side matches its English side in word count and order is flagged, and too many such sentences fail the run. Codepoint choice neither causes nor prevents this; the lexicon and grammar do.

**D26. Word classes: no adjective class, no adverb class.** Property words are stative verbs; manner is a serial verb or a case-marked nominal. First part of O2. `lexicon/schema.json` drops `adj` and `adv`; the remaining enum is provisional until O2 closes.

**D27. Code is a use, not a design target.** Once fluent from the corpus, a model takes instructions in stone and writes code from them; no formal grammar is needed for that and one would hurt the human goal (D1). A small formal register for specs and commands may be added later, on top, without changing anything decided here. Noted as O7.

### OPEN (updated)
- O1. Syllable count. Still open; D23 does not fix it.
- O2, remaining: (i) whether noun/verb is a property of the root or of a suffix (one open class of content roots vs. separate noun and verb classes); (ii) a closed class of obligatory evidential/stance particles; (iii) a closed function-word class for case, subordination, questions. Proposed, not decided.
- O6. Closed by D23.
- O7. A formal code/spec register inside the language (D27). Later.
