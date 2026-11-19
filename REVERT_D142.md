# How to revert D142 (names in their own spelling)

D142 is a **trial**, adopted on the maintainer's instruction to "try it but keep a note if we want to revert". This file is that note. Delete it when the trial is either reverted or made permanent; record either outcome in `decisions.md`.

## What D142 changed
All of it is in one commit, `D142: names carried in their own spelling (trial)`. Its hash is recorded below once it exists.

| File | Change |
|---|---|
| `CLAUDE.md` | rule 3 gains the name exception (one appended sentence) |
| `scripts/stonelib.py` | `NAME` / `is_name`; `check_script` exempts name tokens; `parse_token` makes a name token; `parse_sentence` requires a root before a name |
| `scripts/realize.py` | renders root + name as *the NAME root*; groups name tokens into their phrase; `marker_after` skips names in the subject rule. **That commit also adds a fix not tied to names: "who" + object no longer glues.** Keep that fix on a revert. |
| `scripts/validate.py` | docstring line only |
| `spec/grammar.md` | the "Names (D142, a trial)" section |
| `corpus/corpus.jsonl` | 18 lines, **s1518–s1535**, feature tag `name` |
| `corpus/README.md` | `name` in the tag list; Total line |
| `decisions.md`, `STATE.md` | D142 entry; STATE line |

## To revert
1. `git revert <hash below>`. That restores every file above, including removing s1518–s1535, because they were the last lines appended. If corpus lines were appended after D142, the revert will conflict in `corpus/corpus.jsonl`. In that case delete exactly s1518–s1535 and renumber nothing: ids are stable, and later lines keep theirs. Then fix the README Total line.
2. Re-apply the "who" grouping fix in `scripts/realize.py`, unless it is wanted gone too.
3. Run `scripts/validate.py`, `scripts/regression_test.py` and `scripts/roundtrip_test.py selftest`.
4. Append a decisions entry saying D142 is reverted and why, and update STATE.

## Commit
- Trial commit: `d126a18` (`git revert d126a18`)
