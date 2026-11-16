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
| `HANDOFF.md` | State, settled decisions and open questions, for whoever continues the work |
| `NOTES.md` | Running work log: every design decision and test result, in order |

## The tools (`lang/`)

| File | Job |
|---|---|
| `forms.py` | Word shapes: particles, code keywords, the loan letter table and its marks for capitals, digits and signs |
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
| `test8` | Three checks: round trip of loan-heavy passages, scope ambiguity, tone labels (`test8/results.json`) | 52 agents |
| `test9` | A task and a correction given only in the language, across an interrupted two-turn exchange, two models | 4 writers |
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

After test7 the loan spelling was extended so that every character survives: capitals, hyphens, digits, signs, accents and Greek letters, plus a filler block for one-block words. IL-4, 5-HT1A, Hückel, β-catenin and "pi" now come back exactly. Texts from test5 to test7 were written under the earlier sheets, so the current checker refuses some of their short `« »` pieces.

### test8: three checks after the loan change

**Round trip.** Seven dense English passages (palladium chemistry, kinetics, the action potential, the Higgs boson, climate sensitivity, Unix history, a neutron-star merger) were translated by fresh writers, then turned back into English by two kinds of reader, and each result was compared with the source by a judge.

| Reader works from | Units intact | Weakened | Wrong | Lost | Terms exact | Terms altered |
|---|---|---|---|---|---|---|
| Machine English only | 92 | 7 | 3 | 0 | 128 | 19 |
| Native text and rule sheet | 96 | 3 | 1 | 0 | 133 | 23 |

No term was missing. Nearly all "altered" terms are a change of form by the reader or translator ("two" to "2", "100 s" to "100 seconds", "gNa = 120" to "gNa is 120 mS/cm²"), and no loan was misspelled or misread. The four wrong units are grammar slips, not loan errors: "north-western Europe" became a region north-west of Europe, "called it just a hobby" became "called himself a hobbyist", a "does not follow" lost its target, and a "may" was dropped. Of 42 sentences, one was refused by the checker.

**Scope.** Twelve English sentences with two readings each (for example "I did not leave because of the rain"). Two writers had the full rule sheet and two had it with the paragraph on scope by nesting cut out. Readers picked the intended reading 96 times out of 96 in each arm. So the test found no difference: writers without the paragraph still separated the readings with clause blocks and brackets, which the rest of the sheet teaches. The paragraph is not shown to be needed; the items may also be too easy, since readers chose between two given readings.

**Tone words.** 27 candidate tone labels (the 11 existing ones and 16 new). Two generators wrote 108 short English messages, four per label; three annotators gave each message one label. All three agreed with the intended label on 108 of 108. This shows the labels are distinct ideas when a writer aims at one. It does not show which are needed, because the messages were written to be recognisable. Fifteen were added as particles (SERIOUS, WARM, SAD, GRATEFUL, RHETORICAL, HINT, WARNING, RELUCTANT, PROUD, CURIOUS, EXCITED, RESIGNED, DISGUST, EMBARRASSED, COMFORT); DOUBT was left out because the strength words already express it.

### What is missing from test7

Seven of the 21 writers produced nothing: C03, C07, N03, N05, N07, X02 and X06. All seven ran on Opus and were stopped by the provider's safety systems while writing; none were retried. The ten writers on the other model all finished. The cause was not investigated, so nothing can be concluded about why.

## Limits

- Not shown: that a model *thinks* in the language. Only its written output has been tested.
- Tested on two strong models of one family only.
- Text is about 1.5 times as long as English in tokens.
- The round-trip readers and judges are the same model family as the writers, and readers may fill gaps from their own knowledge of well-known science even when told not to.
- The scope and tone tests both hit the ceiling, so they rule out a large problem but measure nothing finer.

## Left out of this folder

Raw third-party downloads used along the way are not included: the source texts the test passages were cut from, the grammar pages and feature tables read for the typology survey, and the concept lists used to check word coverage. `passages.json` holds the passages actually used, and `survey/out_*.json` holds the survey findings.
