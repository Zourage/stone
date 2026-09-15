#!/usr/bin/env python3
"""Re-run every check in validate.py against the forms it was built to catch.

D82's lesson is that a check which has never been shown to catch a real
violation is not evidence of anything, and D87 and D94 both answered it by
showing, once, in prose, that the new check fired on the pre-correction forms.
Prose is not a regression test: nothing re-runs it, so a later edit that
weakens a check passes silently and the claim in STATE.md stays standing.

This makes those demonstrations executable. `tests/fixtures/pre_correction.jsonl`
holds the pre-correction form of every corpus line corrected since 855226d,
recovered from git, each with the checks that fire when it is put back into the
current corpus. This script puts each one back, one at a time, and fails if a
check that fired then does not fire now.

The fixtures with an empty `catches` list are recorded too, and they are the
more useful half: they are the corrections no check can see. They are asserted
to stay invisible, so that widening a check shows up here as a failure to fix
rather than as silence.

Usage: regression_test.py [-v]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence  # noqa: E402
from validate import (_fronted_adverbial, gloss_collisions, leak_report,  # noqa: E402
                      rule_errors)

FIXTURES = ROOT / "tests/fixtures/pre_correction.jsonl"


def fired(sents, sid, lx, marks, nums, cases, rel, baseline):
    """Which checks fire on sentence `sid` in this version of the corpus."""
    out = []
    for r in sents:
        if r["id"] != sid:
            continue
        parsed = parse_sentence(r["st"], lx)
        preds = {i for i, t in enumerate(parsed.tokens) if t.affixes}
        if _fronted_adverbial(r["st"].split(), preds, nums, cases, rel, marks):
            out.append("fronted")
    if any(m.startswith(sid + ":") for m in rule_errors(sents, lx)):
        out.append("rules")
    if set(gloss_collisions(sents, lx)) - baseline:
        out.append("collision")
    if sid in leak_report(sents):
        out.append("leak")
    return out


def main():
    verbose = "-v" in sys.argv
    lx = Lexicon()
    corpus = [json.loads(l) for l in
              (ROOT / "corpus/corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    by_id = {r["id"]: r for r in corpus}
    fixtures = [json.loads(l) for l in FIXTURES.read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.startswith("#")]

    g = lambda gloss: next(e["form"] for e in lx.entries if e["gloss"] == gloss)  # noqa: E731
    nums = {e["form"] for e in lx.entries if e["pos"] == "num"}
    cases = {e["form"] for e in lx.entries if e["gloss"].startswith("case")}
    rel = {e["form"] for e in lx.entries if e["gloss"].startswith("relational")}
    marks = (g("subordinator"), g("relational: from"), g("time"),
             {g("case: location"), g("relational: before"), g("relational: after")})
    baseline = set(gloss_collisions(corpus, lx))

    failures, blind = [], []
    for fx in fixtures:
        sid = fx["id"]
        if sid not in by_id:
            failures.append(f"{sid}: fixture line is no longer in the corpus")
            continue
        test = [dict(r) for r in corpus]
        for r in test:
            if r["id"] == sid:
                r.update({k: fx[k] for k in ("st", "en", "features", "split")})
        got = fired(test, sid, lx, marks, nums, cases, rel, baseline)
        want = fx["catches"]
        if not want:
            blind.append(sid)
            if got:
                failures.append(f"{sid}: no check used to see this correction; {got} now does. "
                                f"Widening a check is good — update the fixture and say so in "
                                f"decisions.md")
        elif set(want) - set(got):
            failures.append(f"{sid}: {sorted(set(want) - set(got))} no longer fires on the "
                            f"pre-correction form (it did when the fixture was recorded)")
        elif verbose:
            print(f"  {sid:7} {'+'.join(got)}")

    seen = {}
    for fx in fixtures:
        for c in fx["catches"] or ["--none--"]:
            seen[c] = seen.get(c, 0) + 1
    print(f"regression_test.py: {len(fixtures)} pre-correction forms; "
          + ", ".join(f"{k} {v}" for k, v in sorted(seen.items())))
    print(f"  blind spot: {len(blind)} corrections no check can see: {' '.join(blind)}")
    for f in failures:
        print("FAIL", f)
    if failures:
        print(f"{len(failures)} regressions")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
