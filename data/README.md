# data

`ko_frequency.json`: Korean word frequency list (OpenSubtitles 2018, top 50k, via hermitdave/FrequencyWords, CC-BY-SA), filtered to pure Hangul forms of 1–4 syllables. Used by `scripts/validate.py` for the D13/D55 collision check: a proposed root of two or more syllables that is a Korean word is rejected. Single syllables are exempt (D39).
