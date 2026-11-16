# Loan spelling table

Each English letter maps to one Hangul part. Consonant-class letters map to an initial consonant; vowel-class letters map to a vowel. (Note: w, y and x are in the vowel class.)

Consonant-class letters -> initial:
b=ㅋ, c=ㄴ, d=ㅅ, f=ㅍ, g=ㅂ, h=ㅁ, j=ㅈ, k=ㄷ, l=ㅊ, m=ㄹ, n=ㅌ, p=ㅃ, q=ㄲ, r=ㄱ, s=ㅎ, t=ㅉ, v=ㄸ, z=ㅆ

Vowel-class letters -> vowel:
a=ㅜ, e=ㅣ, i=ㅗ, o=ㅑ, u=ㅔ, w=ㅡ, y=ㅏ, x=ㅐ

No vowel-class letter follows -> vowel ㅓ
No consonant-class letter before -> initial ㅇ

## Encoding rule
Lowercase the word. Scan left to right. A consonant-class letter immediately followed by a vowel-class letter shares ONE block with it (initial + vowel). A consonant-class letter NOT followed by a vowel-class letter gets its own block with the "no vowel" vowel. A vowel-class letter not consumed by a preceding consonant gets its own block with initial ㅇ. Blocks have no final consonant.

## Decoding rule
For each block: write the letter of its initial (nothing for ㅇ), then the letter of its vowel (nothing for the "no vowel" vowel).

Example: "stack" -> 허쭈너더
