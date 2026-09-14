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
12 × 6 = 72, minus /wu/ and /ji/ (not reliably distinct from /u/ and /i/ when subvocalized), plus 4 bare vowels /a e i u/. Each syllable is written as the Hangul block that spells it, initial + vowel, no final (D52, `scripts/compose_hangul.py`): the glyph shows its own sound. /ɾ/ is spelled with the d-series (it is the flap of "ladder"); /w/ and /j/ with the null initial and a w- or y-vowel.

### Grid: consonant × vowel → glyph
| | /a/ | /æ/ | /e/ | /i/ | /o/ | /u/ |
|---|---|---|---|---|---|---|
| /p/ | 파 | 패 | 페 | 피 | 포 | 푸 |
| /t/ | 타 | 태 | 테 | 티 | 토 | 투 |
| /k/ | 카 | 캐 | 케 | 키 | 코 | 쿠 |
| /m/ | 마 | 매 | 메 | 미 | 모 | 무 |
| /n/ | 나 | 내 | 네 | 니 | 노 | 누 |
| /s/ | 사 | 새 | 세 | 시 | 소 | 수 |
| /l/ | 라 | 래 | 레 | 리 | 로 | 루 |
| /ɾ/ | 다 | 대 | 데 | 디 | 도 | 두 |
| /h/ | 하 | 해 | 헤 | 히 | 호 | 후 |
| /w/ | 와 | 왜 | 웨 | 위 | 워 | — |
| /j/ | 야 | 얘 | 예 | — | 요 | 유 |
| /tʃ/ | 차 | 채 | 체 | 치 | 초 | 추 |
| (bare) | 아 | — | 에 | 이 | — | 우 |

### Table: glyph → codepoint → sound
| glyph | codepoint | sound |
|---|---|---|
| 나 | U+B098 | /na/ |
| 내 | U+B0B4 | /næ/ |
| 네 | U+B124 | /ne/ |
| 노 | U+B178 | /no/ |
| 누 | U+B204 | /nu/ |
| 니 | U+B2C8 | /ni/ |
| 다 | U+B2E4 | /ɾa/ |
| 대 | U+B300 | /ɾæ/ |
| 데 | U+B370 | /ɾe/ |
| 도 | U+B3C4 | /ɾo/ |
| 두 | U+B450 | /ɾu/ |
| 디 | U+B514 | /ɾi/ |
| 라 | U+B77C | /la/ |
| 래 | U+B798 | /læ/ |
| 레 | U+B808 | /le/ |
| 로 | U+B85C | /lo/ |
| 루 | U+B8E8 | /lu/ |
| 리 | U+B9AC | /li/ |
| 마 | U+B9C8 | /ma/ |
| 매 | U+B9E4 | /mæ/ |
| 메 | U+BA54 | /me/ |
| 모 | U+BAA8 | /mo/ |
| 무 | U+BB34 | /mu/ |
| 미 | U+BBF8 | /mi/ |
| 사 | U+C0AC | /sa/ |
| 새 | U+C0C8 | /sæ/ |
| 세 | U+C138 | /se/ |
| 소 | U+C18C | /so/ |
| 수 | U+C218 | /su/ |
| 시 | U+C2DC | /si/ |
| 아 | U+C544 | /a/ |
| 야 | U+C57C | /ja/ |
| 얘 | U+C598 | /jæ/ |
| 에 | U+C5D0 | /e/ |
| 예 | U+C608 | /je/ |
| 와 | U+C640 | /wa/ |
| 왜 | U+C65C | /wæ/ |
| 요 | U+C694 | /jo/ |
| 우 | U+C6B0 | /u/ |
| 워 | U+C6CC | /wo/ |
| 웨 | U+C6E8 | /we/ |
| 위 | U+C704 | /wi/ |
| 유 | U+C720 | /ju/ |
| 이 | U+C774 | /i/ |
| 차 | U+CC28 | /tʃa/ |
| 채 | U+CC44 | /tʃæ/ |
| 체 | U+CCB4 | /tʃe/ |
| 초 | U+CD08 | /tʃo/ |
| 추 | U+CD94 | /tʃu/ |
| 치 | U+CE58 | /tʃi/ |
| 카 | U+CE74 | /ka/ |
| 캐 | U+CE90 | /kæ/ |
| 케 | U+CF00 | /ke/ |
| 코 | U+CF54 | /ko/ |
| 쿠 | U+CFE0 | /ku/ |
| 키 | U+D0A4 | /ki/ |
| 타 | U+D0C0 | /ta/ |
| 태 | U+D0DC | /tæ/ |
| 테 | U+D14C | /te/ |
| 토 | U+D1A0 | /to/ |
| 투 | U+D22C | /tu/ |
| 티 | U+D2F0 | /ti/ |
| 파 | U+D30C | /pa/ |
| 패 | U+D328 | /pæ/ |
| 페 | U+D398 | /pe/ |
| 포 | U+D3EC | /po/ |
| 푸 | U+D478 | /pu/ |
| 피 | U+D53C | /pi/ |
| 하 | U+D558 | /ha/ |
| 해 | U+D574 | /hæ/ |
| 헤 | U+D5E4 | /he/ |
| 호 | U+D638 | /ho/ |
| 후 | U+D6C4 | /hu/ |
| 히 | U+D788 | /hi/ |
