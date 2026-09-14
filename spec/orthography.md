# Orthography

Status: blocked on phonology and codepoint measurement (D10).

## Glyph system (D9)
Consonant components: _TBD_
Vowel components: _TBD_
Composition rule: _TBD_

## Codepoint map
syllable → PUA codepoint, assigned by measured token cost. Costs measured by `scripts/measure_codepoints.py` into `spec/codepoints_cost.json` (needs `ANTHROPIC_API_KEY`); the syllable → codepoint map derived from it is stored in `spec/codepoints.json` once the inventory (O1) is fixed.

## Design constraints
- Distinct at ~16px on a phone screen.
- Consistent stroke logic across the set.
- No resemblance to Latin, Arabic, Cyrillic, Greek letterforms.
