# Font

Glyphs as SVG in `glyphs/`, one file per syllable named by codepoint (e.g. `A0C4.svg`; the 74 are in `spec/codepoints.json`).
`build.py` assembles them into `stone.ttf` with fontTools, mapping each SVG to its Yi-block codepoint (D23). The real Yi glyph at that codepoint is only what shows when the font is missing.

Blocked on spec/orthography.md.
