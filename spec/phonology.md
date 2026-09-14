# Phonology

Status: decided (D28, D37). Sounds described in IPA. This file describes how each glyph is pronounced; it is not a way of writing words (CLAUDE.md rule 3). Words are written only in the glyphs.

## Purpose (D8)
A memory aid. The language is text-only; sounds exist so that words can be subvocalized and retained. Every sound below already exists in an English speaker's mouth (D40); the descriptions are keyed to English words.

## Consonants (12)
| IPA | say it as | note |
|---|---|---|
| /p/ | p in "spin" | plain p |
| /t/ | t in "stop" | plain t |
| /k/ | k in "skip" | plain k |
| /m/ | m in "me" | |
| /n/ | n in "no" | |
| /s/ | s in "see" | always s, never z |
| /l/ | l in "leaf" | the light l at the start of a word, not the dark l of "full" |
| /ɾ/ | the tt in American "butter", the dd in "ladder" | a single tap of the tongue; not the English r of "red" |
| /h/ | h in "hat" | |
| /w/ | w in "we" | |
| /j/ | y in "yes" | |
| /tʃ/ | ch in "chip" | |

## Vowels (6)
Every vowel is short and pure: one position of the mouth, no glide. This is the main thing an English speaker has to watch, since English "a", "o", "e" tend to slide.
| IPA | say it as | watch for |
|---|---|---|
| /a/ | a in "father" | |
| /æ/ | a in "cat" | |
| /e/ | e in "bet" | not the "ay" of "bay" |
| /i/ | ee in "see" | |
| /o/ | the first part of "go", stopped before the lips close further | not "oh-oo" |
| /u/ | oo in "food" | |

## Syllable structure
CV and V only. No codas, no clusters. Every syllable is one glyph. A word is 1–3 syllables; grammatical pieces and the most frequent roots are 1 syllable (D13, D36).

## Inventory: 74 syllables (D28)
12 × 6 = 72, minus /wu/ and /ji/ (not reliably distinct from /u/ and /i/ when subvocalized), plus 4 bare vowels /a e i u/. The pairing of syllable to glyph is a seeded shuffle (D23, D37): the table is in codepoint order and shows no correlation with the grid.

### Grid: consonant × vowel → glyph
| | /a/ | /æ/ | /e/ | /i/ | /o/ | /u/ |
|---|---|---|---|---|---|---|
| /p/ | ꏡ | ꁇ | ꑚ | ꑅ | ꎏ | ꋁ |
| /t/ | ꋣ | ꃎ | ꄾ | ꑜ | ꊴ | ꐃ |
| /k/ | ꍲ | ꑇ | ꆜ | ꀗ | ꇳ | ꌱ |
| /m/ | ꈷ | ꉇ | ꋴ | ꊓ | ꂅ | ꎽ |
| /n/ | ꏆ | ꊶ | ꋆ | ꉍ | ꄂ | ꊖ |
| /s/ | ꈆ | ꋫ | ꎝ | ꊂ | ꐎ | ꁀ |
| /l/ | ꄩ | ꂂ | ꃃ | ꇲ | ꉉ | ꃿ |
| /ɾ/ | ꅍ | ꍑ | ꃉ | ꁋ | ꏔ | ꈗ |
| /h/ | ꀚ | ꈔ | ꈝ | ꄀ | ꆇ | ꈺ |
| /w/ | ꎵ | ꌇ | ꏇ | ꁺ | ꃘ | — |
| /j/ | ꅽ | ꂸ | ꌑ | — | ꏟ | ꋪ |
| /tʃ/ | ꁽ | ꐾ | ꇏ | ꐼ | ꉏ | ꑈ |
| (bare) | ꀃ | — | ꋌ | ꎿ | — | ꍋ |

### Table: glyph → codepoint → sound
| glyph | codepoint | sound |
|---|---|---|
| ꀃ | U+A003 | /a/ |
| ꀗ | U+A017 | /ki/ |
| ꀚ | U+A01A | /ha/ |
| ꁀ | U+A040 | /su/ |
| ꁇ | U+A047 | /pæ/ |
| ꁋ | U+A04B | /ɾi/ |
| ꁺ | U+A07A | /wi/ |
| ꁽ | U+A07D | /tʃa/ |
| ꂂ | U+A082 | /læ/ |
| ꂅ | U+A085 | /mo/ |
| ꂸ | U+A0B8 | /jæ/ |
| ꃃ | U+A0C3 | /le/ |
| ꃉ | U+A0C9 | /ɾe/ |
| ꃎ | U+A0CE | /tæ/ |
| ꃘ | U+A0D8 | /wo/ |
| ꃿ | U+A0FF | /lu/ |
| ꄀ | U+A100 | /hi/ |
| ꄂ | U+A102 | /no/ |
| ꄩ | U+A129 | /la/ |
| ꄾ | U+A13E | /te/ |
| ꅍ | U+A14D | /ɾa/ |
| ꅽ | U+A17D | /ja/ |
| ꆇ | U+A187 | /ho/ |
| ꆜ | U+A19C | /ke/ |
| ꇏ | U+A1CF | /tʃe/ |
| ꇲ | U+A1F2 | /li/ |
| ꇳ | U+A1F3 | /ko/ |
| ꈆ | U+A206 | /sa/ |
| ꈔ | U+A214 | /hæ/ |
| ꈗ | U+A217 | /ɾu/ |
| ꈝ | U+A21D | /he/ |
| ꈷ | U+A237 | /ma/ |
| ꈺ | U+A23A | /hu/ |
| ꉇ | U+A247 | /mæ/ |
| ꉉ | U+A249 | /lo/ |
| ꉍ | U+A24D | /ni/ |
| ꉏ | U+A24F | /tʃo/ |
| ꊂ | U+A282 | /si/ |
| ꊓ | U+A293 | /mi/ |
| ꊖ | U+A296 | /nu/ |
| ꊴ | U+A2B4 | /to/ |
| ꊶ | U+A2B6 | /næ/ |
| ꋁ | U+A2C1 | /pu/ |
| ꋆ | U+A2C6 | /ne/ |
| ꋌ | U+A2CC | /e/ |
| ꋣ | U+A2E3 | /ta/ |
| ꋪ | U+A2EA | /ju/ |
| ꋫ | U+A2EB | /sæ/ |
| ꋴ | U+A2F4 | /me/ |
| ꌇ | U+A307 | /wæ/ |
| ꌑ | U+A311 | /je/ |
| ꌱ | U+A331 | /ku/ |
| ꍋ | U+A34B | /u/ |
| ꍑ | U+A351 | /ɾæ/ |
| ꍲ | U+A372 | /ka/ |
| ꎏ | U+A38F | /po/ |
| ꎝ | U+A39D | /se/ |
| ꎵ | U+A3B5 | /wa/ |
| ꎽ | U+A3BD | /mu/ |
| ꎿ | U+A3BF | /i/ |
| ꏆ | U+A3C6 | /na/ |
| ꏇ | U+A3C7 | /we/ |
| ꏔ | U+A3D4 | /ɾo/ |
| ꏟ | U+A3DF | /jo/ |
| ꏡ | U+A3E1 | /pa/ |
| ꐃ | U+A403 | /tu/ |
| ꐎ | U+A40E | /so/ |
| ꐼ | U+A43C | /tʃi/ |
| ꐾ | U+A43E | /tʃæ/ |
| ꑅ | U+A445 | /pi/ |
| ꑇ | U+A447 | /kæ/ |
| ꑈ | U+A448 | /tʃu/ |
| ꑚ | U+A45A | /pe/ |
| ꑜ | U+A45C | /ti/ |
