#!/usr/bin/env python3
"""Compose the 74 syllable glyphs as Hangul syllable blocks (D52).

Each of our syllables maps to the precomposed Hangul block that spells its
sound: initial consonant + vowel, no final. The block is computed, not drawn,
so the glyph for a sound is fixed by this table and reproducible.

Writes spec/codepoints.json (the 74 codepoints, with the syllable each one
spells, in IPA) and prints the grid. Refuses to overwrite without --force.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "spec" / "codepoints.json"

# Hangul jamo indices (Unicode composition order).
INITIALS = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
VOWELS = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"

# Our consonant -> Hangul initial. /ɾ/ is the flap of "ladder", spelled with
# the d-series; /l/ takes ㄹ. /w/ and /j/ are spelled by the null initial plus
# a w- or y-vowel, so they are handled in VOWEL_MAP below.
INITIAL_MAP = {"p": "ㅍ", "t": "ㅌ", "k": "ㅋ", "m": "ㅁ", "n": "ㄴ", "s": "ㅅ",
               "l": "ㄹ", "ɾ": "ㄷ", "h": "ㅎ", "tʃ": "ㅊ", "": "ㅇ"}
VOWEL_MAP = {"a": "ㅏ", "æ": "ㅐ", "e": "ㅔ", "i": "ㅣ", "o": "ㅗ", "u": "ㅜ",
             "wa": "ㅘ", "wæ": "ㅙ", "we": "ㅞ", "wi": "ㅟ", "wo": "ㅝ",
             "ja": "ㅑ", "jæ": "ㅒ", "je": "ㅖ", "jo": "ㅛ", "ju": "ㅠ"}

CONSONANTS = ["p", "t", "k", "m", "n", "s", "l", "ɾ", "h", "w", "j", "tʃ"]
VOWELS6 = ["a", "æ", "e", "i", "o", "u"]
BARE = ["a", "e", "i", "u"]


def block(initial, vowel):
    return chr(0xAC00 + (INITIALS.index(initial) * 21 + VOWELS.index(vowel)) * 28)


def inventory():
    """Return list of (ipa, glyph) for the 74 syllables (D28, D37)."""
    out = []
    for c in CONSONANTS:
        for v in VOWELS6:
            if (c, v) in (("w", "u"), ("j", "i")):
                continue
            if c in ("w", "j"):
                out.append((c + v, block("ㅇ", VOWEL_MAP[c + v])))
            else:
                out.append((c + v, block(INITIAL_MAP[c], VOWEL_MAP[v])))
    for v in BARE:
        out.append((v, block("ㅇ", VOWEL_MAP[v])))
    assert len(out) == 74 and len({g for _, g in out}) == 74
    return out


def main():
    force = "--force" in sys.argv
    if OUT.exists() and not force:
        print(f"{OUT} exists; changing it is a decision (decisions.md). Use --force.", file=sys.stderr)
        return 2
    inv = inventory()
    OUT.write_text(json.dumps({
        "block": "hangul", "rule": "initial + vowel, no final; see scripts/compose_hangul.py",
        "count": 74,
        "codepoints": [f"{ord(g):04X}" for _, g in inv],
        "syllables": {f"{ord(g):04X}": ipa for ipa, g in inv},
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
