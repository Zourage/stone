# Orthography

Status: codepoints drawn (D28) and paired to sounds (D37, see phonology.md); glyph design open (D9).

## Codepoint block (D23)
Yi Syllables, U+A000–U+A48C. Three tokens per glyph, flat (D22). Real Yi letterforms are only the fallback rendering; our font maps each codepoint to our own glyph.

## Codepoint map
`spec/codepoints.json`: an ordered list of codepoints drawn from the block by `scripts/assign_codepoints.py` with a fixed seed. Random spread, not contiguous, not in Yi's phonetic order. Generated once O1 fixes the syllable count; regenerating with a different seed or count is a new decision.

The pairing of each codepoint with its sound lives in `spec/phonology.md` (the glyph, then its IPA). That table describes how a glyph is pronounced; it is not a way of writing words (CLAUDE.md rule 3).

## Glyph system (D9)
Consonant components: _TBD_
Vowel components: _TBD_
Composition rule: _TBD_

## Design constraints
- Distinct at ~16px on a phone screen.
- Consistent stroke logic across the set.
- No resemblance to Latin, Arabic, Cyrillic, Greek letterforms, nor to the real Yi glyphs on the same codepoints.

## History
BMP Private Use Area (D4) is stripped from Claude's input before tokenization (D20, D21). Measurement of alternatives: D22.
