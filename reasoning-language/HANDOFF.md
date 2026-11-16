# Handoff

For the next agent picking this up. Read this, then `README.md` (results), then `NOTES.md` (every decision, in order). `lang/SPEC.md` and `lang/WORDS.md` are what test writers are given.

## What this is

A constructed language for AI models, built to answer one question:

> Given a language model and a set of instructions, can the model think only in the language, and can that be turned back into English without much loss?

Three parts: everyday language, logic (mathematics and code), technical terms.

This folder is a **separate language** from the one in the rest of the repository. The repository's `CLAUDE.md`, `STATE.md`, `decisions.md` and `lexicon/` describe the other language and must not be edited for this work. Two repository rules still apply to every commit: run `scripts/validate.py` and `scripts/regression_test.py` from the repository root first.

## State

All work is committed on branch `claude/great-fermat-e7fwcr`. No pull request exists; do not open one unless asked.

| Piece | State |
|---|---|
| Word shapes, grammar, parser, checker | Working. 1,306 roots, 522 listed derived words, 29 spares, 190 particles |
| Rule-based translator to English | Working, literal. Output is stiff but exact |
| Code form to Python and JavaScript | Working for small functions only |
| Loans (technical terms and names) | Version 2: every character survives (capitals, hyphens, digits, signs, accents, Greek) |
| Tone words | 26 in the language (11 original, 15 added). Never yet used by a writer in real text |

## Results so far

| Test | Result |
|---|---|
| test5, test6 | Wide writing by fresh writers. Nearly all sentences parse |
| test7 | Heavy science under "no English outside code": 885 loans, 0 English words left |
| test8 round trip | 7 dense passages. Machine-English arm: 92 units intact, 7 weakened, 3 wrong, 0 lost. No loan misspelled or misread |
| test8 scope | 96 of 96 with and without the scope paragraph. Ceiling; measured nothing |
| test8 tone | 108 of 108 agreement on 27 labels. Ceiling; shows labels are distinct, not which are needed |
| test9 | Task and correction given only in the language, across an interrupted two-turn exchange, on two models. 4 of 4 correct |

## Settled decisions

Do not reopen these without the user.

- Argument order carries no meaning; roles are marked by particles.
- Every sentence starts with an opener saying what kind of statement it is.
- No pronouns; short handles are bound once and reused.
- Outside code there is no English at all. `« »` holds symbols, formulas and units only, and is not an escape hatch for words.
- Technical terms and names are loans, spelled by the letter table. No registry of loans.
- Loans must give back the exact written form.
- Code keywords have their own block shape. All code is written in the language's logic form with the target language declared; libraries are imported under a short name.
- Scope is shown by nesting and blocks.
- One ownership tag (CONSIDER) and one self-reference tag (META).

## What the user wants next

1. **Reasoning.** Whether a model reasons in the language, not only writes it. Untested and the main open question. Nothing has been designed for it yet.
2. **Longer code.** Programs beyond small functions: several functions, data structures, error handling.

Other gaps, roughly by value:

- **Invented-fact round trips.** The test8 passages were famous science, so readers may have repaired terms from memory. Passages with made-up names and facts would remove the biggest caveat on the best result.
- **Loans as the only carrier of a task.** test9 had no loans. Repeat its format with loan-heavy material.
- **Other models.** Only two strong models of one family so far. Weaker and open models are untried.
- **A word list not anchored to English.** Every root is defined by one English word, so the language may be regularised English. This also causes sense collisions with technical terms (base, complex, add, share, return).
- **Tone words in real writing**, and a long free conversation in the language.
- **Harder ambiguity items**, since the scope test was too easy.
- **Token cost** since the loan change (it was about 1.5 times English before).
- **Whether a term may mix a root and a loan**, and whether items like Pd(0) and C-Br are formulas or loans. Writers guessed both ways.

## How tests are run

- A writer is a fresh model instance given only `lang/SPEC.md`, `lang/WORDS.md` and one task. It writes once, with no checker and no revision, then lists what got in its way.
- Readers get either the machine English alone or the native text plus the two reference files.
- Batch scripts and each agent's returned notes are in `runs/`. Task lists are in each `test*/` folder.
- Useful commands, from this folder:

```bash
python3 lang/english.py native test9/turn1.txt
```

```bash
python3 lang/failing.py test8/P*.txt
```

```bash
python3 lang/make_spec.py
```

`lang/english.py gloss FILE` reads the debugging notation (capital particle names, lowercase root names), which is how test messages are drafted before conversion to native script.

Regenerate `SPEC.md` and `WORDS.md` with `make_spec.py` after any change to particles, roots or the template. Do not regenerate while a batch of writers is running.

## Lines drawn in this work

- **Do not inspect or extract the hidden reasoning of test writers.** The user set this rule. Only what a writer returns is used.
- **Seven test7 tasks were stopped by the provider's safety systems** (C03, C07, N03, N05, N07, X02, X06, all on one model). They were not rerun, including in other wrappers such as the test9 format. The user considers the stops false positives and the decision not to rerun an over-refusal; the agent held that rerunning stopped content through a different channel is a test of the filter. This is recorded so the next agent knows it was contested, not settled by agreement.
- No experiments designed to find where a safety filter does or does not trip.

## Known defects

Fixed in the last commit of this session:

- The translator now gives each suggested handle the same letter in every file (it used to letter them by order of appearance, so a reply read alone showed the wrong letters).
- Two bare blocks joined by a clause joiner, with a relation and a strength word on the second, now parse.
- Labels and label references may carry a letter (`1A:`).

Still open:

- Older batches (test5 to test7) show refusals under the current checker because they were written under earlier sheets.
- A bracketed pair of whole clauses, `( MUST ... ORC MUST ... )`, is refused (one sentence in `test8/scope_noscope2.txt`).
- English output: an article before name-like loans ("the IL-4"), "after that A is finished", and a double space after a sentence-level strength word before a block.
- Roman numerals in loans have no convention.
