# Orthography

Status: glyphs are Hangul syllable blocks spelling their own sound (D52). Custom glyph design (D9) is optional and deferred.

## Codepoint block (D52)
Hangul Syllables, U+AC00–U+D7A3, the 74 blocks with our 12 initials × 6 vowels and no final. One to three tokens per glyph (D22). Every device renders them; no font is required.

## Codepoint map
`spec/codepoints.json`: the 74 codepoints with the syllable each spells, computed by `scripts/compose_hangul.py` from the phonology. The glyph for a sound is fixed by that script's table; changing the table is a decision.

The pairing of each codepoint with its sound lives in `spec/phonology.md` (the glyph, then its IPA). That table describes how a glyph is pronounced; it is not a way of writing words (CLAUDE.md rule 3).

## Glyph system (D9)
Hangul is componential by construction: each block shows its initial consonant and its vowel. D9 is satisfied by the script itself. A custom font over the same codepoints remains possible and is not planned.

## Design constraints
- Distinct at ~16px on a phone screen.
- Consistent stroke logic across the set.
- (Custom glyphs only.) No resemblance to Latin, Arabic, Cyrillic, Greek letterforms.

## History
BMP Private Use Area (D4) is stripped from Claude's input before tokenization (D20, D21). Yi Syllables (D23) tripped a content classifier on the chat surface and were unusable in practice (D52). Measurements: D22.
