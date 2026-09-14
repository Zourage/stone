# Font

Glyphs as SVG in `glyphs/`, one file per syllable named by codepoint (e.g. `E000.svg`).
`build.py` assembles them into `stone.ttf` with fontTools, mapping each SVG to its PUA codepoint.

Blocked on spec/orthography.md.
