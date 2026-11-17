#!/usr/bin/env python3
"""Free-text round trip: the standing test of whether the language carries meaning (D136).

The acceptance test draws its held sentences from the corpus that supplies the
prompt, and the cue rule puts the evidential in the English, so it measures
corpus self-consistency (D135). This test does not: its sentences were never in
the corpus and were written by someone who never saw the lexicon. Each one goes
out into the language through one model and back into English through another
that never saw the original; independent judges then compare the original with
what came back.

Usage:
  roundtrip_test.py run dev|test TAG      writes tests/results/roundtrip/TAG_SET.json
  roundtrip_test.py calibrate             judges D135's outputs against its hand labels
  roundtrip_test.py compare A.json B.json paired comparison, item by item

Labels: FAITHFUL (same meaning), LOSS (core meaning intact, a nuance gone),
DEGRADED (something that changes what a listener would do is gone), BROKEN
(meaning changed or reversed), MISSING (nothing came back). Usable means
FAITHFUL or LOSS.

The test set (tests/fixtures/roundtrip_test.txt) is SEALED: do not read it while
changing the language, or the next run measures the reading. Report aggregates;
read individual failures only after the change being measured is committed.
Needs OPENROUTER_API_KEY.
"""
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://openrouter.ai/api/v1/chat/completions"
PAIRS = [("google/gemini-3.8-flash", "x-ai/grok-4.6"),
         ("x-ai/grok-4.6", "google/gemini-3.8-flash")]
JUDGES = ["anthropic/claude-sonnet-4.5", "openai/gpt-5.6-luna"]
LABELS = ("FAITHFUL", "LOSS", "DEGRADED", "BROKEN")
USABLE = {"FAITHFUL", "LOSS"}
CHUNK = 40


def call(model, prompt, retries=5):
    """Always returns a string. Reads `content` only: a reasoning model's scratchpad
    is not its answer (D128), and no token cap, which truncated one into silence."""
    key = os.environ["OPENROUTER_API_KEY"]
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0}).encode()
    last = "ERROR: never ran"
    for a in range(retries):
        try:
            req = urllib.request.Request(URL, data=body, method="POST", headers={
                "Authorization": "Bearer " + key, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as f:
                d = json.load(f)
            t = (d["choices"][0]["message"].get("content") or "").strip()
            if t:
                return t
            last = "ERROR: empty content"
        except Exception as e:  # noqa: BLE001 - every failure is retried, then reported
            last = "ERROR: %s" % e
        time.sleep(2 ** a)
    return last


def numbered(text, n):
    out = {}
    for line in (text or "").splitlines():
        m = re.match(r"\s*(\d+)[.)]\s*(.+)", line.strip())
        if m and 1 <= int(m.group(1)) <= n:
            out.setdefault(int(m.group(1)), m.group(2).strip())
    return out


def context():
    rows = [json.loads(l) for l in (ROOT / "corpus/corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return ("Below are sentence pairs from a constructed language, one per line, as\n"
            "`English ||| the language`. Learn the language from them. It is not Korean and\n"
            "no word is borrowed from any language.\n\n"
            + "\n".join("%s ||| %s" % (r["en"], r["st"]) for r in rows)), len(rows)


def translate(model, ctx, items, instruction):
    out = {}
    for start in range(0, len(items), CHUNK):
        chunk = items[start:start + CHUNK]
        listing = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(chunk))
        got = numbered(call(model, ctx + "\n\n" + instruction + "\n\n" + listing), len(chunk))
        for i, s in got.items():
            out[start + i] = s
    return out


JUDGE_PROMPT = """Each item below has an ORIGINAL English sentence and what came RETURNED after it
was translated into another language and back by two different people. Judge whether
someone who only received RETURNED would understand what ORIGINAL meant.

FAITHFUL  same meaning; wording may differ
LOSS      core meaning intact, but a nuance is gone (a hedge, politeness, emphasis)
DEGRADED  something is gone that would change what the listener does or believes
          (a restriction like "only", a quantity, which thing is meant, a condition)
BROKEN    the meaning is different, reversed, or wrong

Answer with one line per item, exactly "N. LABEL", nothing else.

"""


def judge(model, pairs):
    """pairs: list of (original, returned) with returned possibly None."""
    labels = {}
    todo = [(i + 1, o, r) for i, (o, r) in enumerate(pairs) if r]
    for start in range(0, len(todo), CHUNK):
        chunk = todo[start:start + CHUNK]
        listing = "\n".join("%d. ORIGINAL: %s\n   RETURNED: %s" % (k + 1, o, r)
                            for k, (_, o, r) in enumerate(chunk))
        got = numbered(call(model, JUDGE_PROMPT + listing), len(chunk))
        for k, (n, _, _) in enumerate(chunk):
            lab = (got.get(k + 1) or "").upper().split()[0:1]
            labels[n] = lab[0] if lab and lab[0] in LABELS else "UNPARSED"
    for i, (o, r) in enumerate(pairs):
        labels.setdefault(i + 1, "MISSING")
    return labels


def load_set(name):
    p = ROOT / ("tests/fixtures/roundtrip_%s.txt" % name)
    return [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def commit():
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def item_scores(res):
    """Per (pair, item): share of judges calling it usable."""
    sc = {}
    for pname, p in res["pairs"].items():
        for n in range(1, len(res["sentences"]) + 1):
            v = [res["judges"][j][pname].get(str(n)) in USABLE for j in res["judges"]]
            sc[(pname, n)] = sum(v) / len(v)
    return sc


def boot(vals, reps=4000, seed=0):
    rnd = random.Random(seed)
    xs = sorted(sum(rnd.choice(vals) for _ in vals) / len(vals) for _ in range(reps))
    return xs[int(.025 * reps)], xs[int(.975 * reps)]


def summarise(res):
    sc = item_scores(res)
    n = len(res["sentences"])
    per_item = [sum(sc[(p, i)] for p in res["pairs"]) / len(res["pairs"]) for i in range(1, n + 1)]
    lo, hi = boot(per_item)
    print("%s / %s   corpus %d lines at %s   %d sentences x %d pairs x %d judges"
          % (res["tag"], res["set"], res["corpus_lines"], res["commit"], n, len(res["pairs"]), len(res["judges"])))
    for j, by in res["judges"].items():
        labs = [by[p][str(i)] for p in by for i in range(1, n + 1)]
        c = {k: labs.count(k) for k in LABELS + ("MISSING", "UNPARSED")}
        print("  judge %-28s %s" % (j, "  ".join("%s %d" % (k, v) for k, v in c.items() if v)))
    js = list(res["judges"])
    if len(js) == 2:
        pairs_i = [(p, str(i)) for p in res["pairs"] for i in range(1, n + 1)]
        agree = sum((res["judges"][js[0]][p][i] in USABLE) == (res["judges"][js[1]][p][i] in USABLE)
                    for p, i in pairs_i)
        print("  judges agree on usable-or-not: %d/%d" % (agree, len(pairs_i)))
    print("  USABLE %.1f%%  (95%% CI %.1f-%.1f, bootstrap over sentences)" % (100 * sum(per_item) / n, 100 * lo, 100 * hi))


def cmd_run(setname, tag):
    sents = load_set(setname)
    ctx, nlines = context()
    res = {"tag": tag, "set": setname, "commit": commit(), "corpus_lines": nlines,
           "sentences": sents, "pairs": {}, "judges": {}}

    def one_pair(pair):
        out_m, back_m = pair
        st = translate(out_m, ctx, sents, "Translate each into the language. If you cannot say "
                       "something exactly, say the nearest thing you can. Output only a numbered "
                       "list, nothing else.")
        st_list = [st.get(i, "") for i in range(len(sents))]
        back = translate(back_m, ctx, [s or "(empty)" for s in st_list],
                         "Translate each into English. Output only a numbered list, nothing else.")
        return "%s->%s" % (out_m.split("/")[1], back_m.split("/")[1]), [
            {"n": i + 1, "st": st_list[i], "back": back.get(i) if st_list[i] else None}
            for i in range(len(sents))]

    with ThreadPoolExecutor(len(PAIRS)) as ex:
        for name, items in ex.map(one_pair, PAIRS):
            res["pairs"][name] = items

    def one_judge(j):
        return j, {p: {str(k): v for k, v in judge(j, [(sents[it["n"] - 1], it["back"]) for it in items]).items()}
                   for p, items in res["pairs"].items()}
    with ThreadPoolExecutor(len(JUDGES)) as ex:
        for j, by in ex.map(one_judge, JUDGES):
            res["judges"][j] = by
    out = ROOT / ("tests/results/roundtrip/%s_%s.json" % (tag, setname))
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    summarise(res)
    print("  written", out.relative_to(ROOT))


def cmd_calibrate():
    d = json.loads((ROOT / "tests/fixtures/roundtrip_2026-10-09.json").read_text(encoding="utf-8"))
    hand = json.loads((ROOT / "tests/fixtures/roundtrip_dev_hand_labels.json").read_text(encoding="utf-8"))
    pairs = [(r["sent"], r["back"]) for r in d]
    print("judges against the D135 hand labels on the same 20 outputs")
    for j in JUDGES:
        lab = judge(j, pairs)
        exact = sum(lab[i] == hand[str(i)] for i in range(1, 21))
        use = sum((lab[i] in USABLE) == (hand[str(i)] in USABLE) for i in range(1, 21))
        print("  %-28s exact label %2d/20   usable-or-not %2d/20" % (j, exact, use))
        for i in range(1, 21):
            if (lab[i] in USABLE) != (hand[str(i)] in USABLE):
                print("     #%d hand %-9s judge %-9s %s" % (i, hand[str(i)], lab[i], d[i - 1]["sent"]))


def cmd_compare(a, b):
    A, B = (json.loads(Path(x).read_text(encoding="utf-8")) for x in (a, b))
    assert A["sentences"] == B["sentences"], "not the same sentence set: not a paired comparison"
    sa, sb = item_scores(A), item_scores(B)
    keys = [k for k in sa if k in sb]
    diffs = [sb[k] - sa[k] for k in keys]
    lo, hi = boot(diffs)
    up = sum(d > 0 for d in diffs)
    down = sum(d < 0 for d in diffs)
    print("paired: %s (%s) -> %s (%s), %d sentence-pairs" % (A["tag"], A["commit"], B["tag"], B["commit"], len(keys)))
    print("  usable %.1f%% -> %.1f%%   delta %+.1f points (95%% CI %+.1f to %+.1f)"
          % (100 * sum(sa[k] for k in keys) / len(keys), 100 * sum(sb[k] for k in keys) / len(keys),
             100 * sum(diffs) / len(diffs), 100 * lo, 100 * hi))
    print("  items improved %d, worsened %d, unchanged %d" % (up, down, len(keys) - up - down))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["run"] and len(a) == 3:
        cmd_run(a[1], a[2])
    elif a[:1] == ["calibrate"]:
        cmd_calibrate()
    elif a[:1] == ["compare"] and len(a) == 3:
        cmd_compare(a[1], a[2])
    else:
        print(__doc__)
        sys.exit(2)
