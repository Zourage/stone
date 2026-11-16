# A reasoning language for AI models (separate experiment)

This folder is a **separate language** from the one in the rest of this repository. It was designed from scratch and shares nothing with it: not the words, not the grammar, not the rules. The repository's own rules (`CLAUDE.md`, `STATE.md`, `decisions.md`, `scripts/validate.py`) do not describe this folder and this folder's tools do not check the repository's corpus.

One difference matters for readers of the repository rules: this toolchain has an English-gloss input mode (capital particle names, lowercase root glosses) used for testing and for the examples in the rule sheet. It is a debugging notation for this language only.

## The question

Given a language model and a set of instructions, can the model write and reason only in a constructed language, and can that text be turned back into English by a program without much loss? Three parts: everyday language, logic (mathematics and code), technical terms.

## Where to start

| File | What it is |
|---|---|
| `OVERVIEW.md` | Two-page description of the language and where it stands |
| `lang/SPEC.md` | The rule sheet given to models (generated) |
| `lang/WORDS.md` | The word list given to models (generated) |
| `NOTES.md` | Running work log: every design decision and test result, in order |

## The tools (`lang/`)

| File | Job |
|---|---|
| `forms.py` | Word shapes: particles, code keywords, the loan letter table |
| `build_lexicon.py` | Builds `lexicon.json` (1,306 roots, 29 spares) from the `lex_*.tsv` lists |
| `lang.py` | Tokeniser, parser and checker |
| `english.py` | Rule-based translator to literal English, and the code converter (Python, JavaScript) |
| `make_spec.py` | Generates `SPEC.md` and `WORDS.md` from `spec_template.md` and the lexicon |
| `failing.py` | Lists every refused sentence in a set of files |
| `loan_audit.py` | Counts loans, formulas, units and any English left in `« »` |
| `score.py` | Scoring helper for the earlier reading tests |

Typical use, from this folder:

```bash
python3 lang/english.py native test7/C02_fable.txt
```

```bash
python3 lang/failing.py test7/*_*.txt
```

```bash
python3 lang/loan_audit.py test7/*_*.txt
```

## The tests

Each writer was a fresh model instance given only the rule sheet, the word list and one task. It wrote once, with no checker and no revision, then listed what got in its way.

| Folder | What | Size |
|---|---|---|
| `run1`–`run3` | First drafts: encode passages, measure what is lost | 24 + 8 passages |
| `test1`–`test4` | Early write and read tests | small |
| `test5` | Wide scatter: stories, dialogue, proofs, code, medicine, law | 24 writers, 763 sentences |
| `test6` | Science and computing | 20 writers, 746 sentences |
| `test7` | Heavy chemistry, neuroscience and mixed science, under the "no English outside code" rule | 14 files, 573 sentences |
| `runs/` | The batch scripts and each writer's returned notes (`*.journal.jsonl`) |
| `scratch/` | Small hand-written test sentences used while fixing the parser |

Files named `*.oldforms` are the same texts in an earlier spelling of the particles.

### Loanwords: the main result of the last round

Before the rule, writers put technical terms and names in `« »` as plain English. After it, they spelled them as loans.

| Batch | Sentences | Loans used | English words left in `« »` | Abbreviations left in `« »` |
|---|---|---|---|---|
| test5 (old rule) | 763 | 93 | 44 | 0 |
| test6 (old rule) | 746 | 162 | 75 | 28 |
| test7 (new rule) | 573 | 885 | 0 | 6 |

In test7 the 885 loans are 338 distinct terms (for example "substantia nigra pars compacta", "beta hydride elimination", "ser 195", "ssp 5 8.5", "akira suzuki"). In 13 files, 195 of 202 terms named in the tasks can be found again in the machine-made English; the other 7 were expressed with native words instead. One file (N01) has four misspelled loans, all from misreading one vowel in the letter table.

Known costs: capitals and hyphens are lost (IL-4 reads back as "il 4"), and pieces too short for a loan (one letter, or "pi", "ca", "gw") still have to go in `« »`.

### What is missing from test7

Seven of the 21 writers produced nothing: C03, C07, N03, N05, N07, X02 and X06. All seven ran on Opus and were stopped by the provider's safety systems while writing; none were retried. The ten writers on the other model all finished. The cause was not investigated, so nothing can be concluded about why.

## Limits

- Not shown: that a model *thinks* in the language. Only its written output has been tested.
- Tested on two strong models of one family only.
- Text is about 1.5 times as long as English in tokens.
- Readers have not yet been tested on the loan-heavy texts; the term check above is a string match on the machine translation.

## Left out of this folder

Raw third-party downloads used along the way are not included: the source texts the test passages were cut from, the grammar pages and feature tables read for the typology survey, and the concept lists used to check word coverage. `passages.json` holds the passages actually used, and `survey/out_*.json` holds the survey findings.
