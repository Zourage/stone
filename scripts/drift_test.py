#!/usr/bin/env python3
"""The drift test (D15, protocol fixed in D74).

One long model conversation. Twelve fixed probe sentences are translated at the
start, then forty turns of other, plausible work go by in the same session, then
the same twelve are asked for again. Divergence between the two probe rounds is
drift.

Three signals are recorded, because the first one alone is confounded: at the
late probe round the model can see its own early answers, so it may copy them
and hide a slide that is really there.

  1. PROBE DIVERGENCE. Early round vs late round, token for token. The late
     round asks for the twelve in a different order and does not say they are
     repeats.
  2. FILLER ACCURACY BY TURN. Every one of the forty filler turns asks for a
     held-out-from-nothing train sentence the corpus already answers, so each
     turn is scored against the corpus. Accuracy in the first half against the
     second half is a drift measure that copying cannot flatter.
  2b. THE CONTROL RUN. --control asks the same forty sentences in the same
     order, but each in its own fresh one-turn conversation with the same
     materials. Sentence difficulty is then held constant and session length is
     the only difference, so the long run against the control is what actually
     isolates drift. Without it a second-half drop is unreadable: the filler
     sentences are drawn in corpus order, and the newer corpus is harder.
  3. KOREAN LEAKAGE. Every stone token the model emits anywhere in the session
     is checked against data/ko_frequency.json. A multi-syllable token that is a
     real Korean word and is not in the lexicon is the specific failure D52 left
     open, and it is immune to copying too.

Usage: drift_test.py [--out FILE] [--model MODEL] [--turns N]
Needs OPENROUTER_API_KEY. Writes a JSON record of every turn to --out.
"""
import argparse
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence, parse_token  # noqa: E402
from translate import (DEFAULT_MODEL, call_model, context_block,  # noqa: E402
                       load_corpus, relevant_examples, require_key)

# The twelve probes. Fixed by D74: changing this list makes a new test, not a
# new run of this one. Between them they use all four evidentials, six stances,
# negation, past and future, the conditional, all four modals and both
# quantifiers.
PROBES = [
    ("p01", "I tested the machine."),
    ("p02", "I'm told the file is empty."),
    ("p03", "The data must be faulty."),
    ("p04", "Faults cause failures. Everyone knows that."),
    ("p05", "I'll fix the function; that's the plan."),
    ("p06", "The run will probably be slow."),
    ("p07", "This is the cause. Just a hypothesis."),
    ("p08", "You tested it, I'm told; I'm counting on that."),
    ("p09", "Don't remove the line; that might break something."),
    ("p10", "The plan is not bad. I insist."),
    ("p11", "If every test fails, I can fix it; I want to record the cause."),
    ("p12", "You should not open the machine; nobody may alter it."),
]

# The late round asks for the same twelve in this order, and says nothing about
# them being repeats.
LATE_ORDER = ["p07", "p12", "p03", "p09", "p01", "p06",
              "p11", "p04", "p10", "p02", "p08", "p05"]


def norm(t):
    return " ".join(unicodedata.normalize("NFC", t).split())


def probe_prompt(items):
    lines = "\n".join(f"{i} ||| {en}" for i, en in items)
    return ("Translate each of these English sentences into the language. One line each, "
            "in this exact format and nothing else:\n<id> ||| <the translation>\n\n" + lines)


def parse_reply(reply):
    out = {}
    for line in reply.splitlines():
        if "|||" not in line:
            continue
        i, a = [x.strip() for x in line.split("|||", 1)]
        i = i.replace("LINE1:", "").strip()
        out[i] = norm(a)
    return out


def filler_turns(n):
    """Deterministic filler work: train sentences the corpus already answers."""
    train = [s for s in load_corpus() if s["split"] == "train"]
    step = max(1, len(train) // n)
    picked = [train[(k * step) % len(train)] for k in range(n)]
    return picked


def korean_leaks(tokens, lx, ko):
    """Tokens that are real Korean words and are not forms of this language.

    A legal inflected form can coincide with a Korean word by accident — the
    failure root plus the general evidential is one — so a token only counts as
    leakage if the parser cannot read it as a word of the language at all.
    """
    bad = []
    for t in sorted(set(tokens)):
        t = t.strip(".,;:?!")
        if len(t) < 2 or t in lx.by_form or t not in ko:
            continue
        if parse_token(t, lx).errors:
            bad.append((t, ko[t]))
    return bad


def stone_tokens(text):
    return [t for t in norm(text).split() if any("가" <= c <= "힣" for c in t)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="drift_run.json")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--turns", type=int, default=40, help="filler turns between the probe rounds")
    ap.add_argument("--control", action="store_true",
                    help="run the filler sentences one per fresh conversation, as the control")
    args = ap.parse_args()

    key = require_key()
    lx = Lexicon()
    ko = json.load(open(ROOT / "data/ko_frequency.json", encoding="utf-8"))
    corpus = [s for s in load_corpus() if s["split"] == "train"]

    record = {"model": args.model, "turns": args.turns, "probes": dict(PROBES),
              "control": args.control, "log": []}
    messages = []

    if args.control:
        ctx = context_block(lx, corpus[:250])
        for k, s in enumerate(filler_turns(args.turns), start=2):
            ask = (ctx + "\nAnswer only in the script; never write any word of this language in "
                   "Latin letters.\n\nTranslate this into the language, and reply with the "
                   f"translation on one line and nothing else:\n{s['en']}")
            reply = call_model([{"role": "user", "content": ask}], args.model, key)
            got = norm(reply.splitlines()[0] if reply.strip() else "")
            gold = norm(s["st"])
            entry = {"turn": k, "kind": "filler", "id": s["id"], "en": s["en"], "gold": gold,
                     "got": got, "exact": got == gold, "wellformed": parse_sentence(got, lx).ok}
            record["log"].append(entry)
            print(f"control {k}: {s['id']} exact={entry['exact']}", flush=True)
        f = [e for e in record["log"] if e["kind"] == "filler"]
        half = len(f) // 2
        record["filler_accuracy"] = {
            "first_half": sum(e["exact"] for e in f[:half]), "first_half_n": half,
            "second_half": sum(e["exact"] for e in f[half:]), "second_half_n": len(f) - half,
            "wellformed_first": sum(e["wellformed"] for e in f[:half]),
            "wellformed_second": sum(e["wellformed"] for e in f[half:])}
        toks = []
        for e in record["log"]:
            toks += stone_tokens(e.get("got", ""))
        record["korean_leaks"] = korean_leaks(toks, lx, ko)
        record["tokens_emitted"] = len(toks)
        Path(args.out).write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        fa = record["filler_accuracy"]
        print(f"\ncontrol exact: {fa['first_half']}/{fa['first_half_n']} first half, "
              f"{fa['second_half']}/{fa['second_half_n']} second half")
        print(f"korean leakage: {len(record['korean_leaks'])} of {record['tokens_emitted']} tokens")
        print(f"written to {args.out}")
        return 0

    # ---- turn 1: the materials, then the early probe round.
    ctx = context_block(lx, corpus[:250])
    first = (ctx + "\nYou will be working in this language for a while. Answer only in the "
             "script; never write any word of it in Latin letters.\n\n" + probe_prompt(PROBES))
    messages.append({"role": "user", "content": first})
    reply = call_model(messages, args.model, key)
    messages.append({"role": "assistant", "content": reply})
    early = parse_reply(reply)
    record["early"] = early
    record["early_wellformed"] = {i: parse_sentence(a, lx).ok for i, a in early.items()}
    record["log"].append({"turn": 1, "kind": "probe-early", "reply": reply})
    print(f"turn 1: early probe round, {len(early)}/12 parsed", flush=True)

    # ---- filler turns.
    fillers = filler_turns(args.turns)
    for k, s in enumerate(fillers, start=2):
        ask = (f"Now something else. Translate this into the language, and reply with the "
               f"translation on one line and nothing else:\n{s['en']}")
        messages.append({"role": "user", "content": ask})
        reply = call_model(messages, args.model, key)
        messages.append({"role": "assistant", "content": reply})
        got = norm(reply.splitlines()[0] if reply.strip() else "")
        gold = norm(s["st"])
        parsed = parse_sentence(got, lx)
        entry = {"turn": k, "kind": "filler", "id": s["id"], "en": s["en"],
                 "gold": gold, "got": got, "exact": got == gold, "wellformed": parsed.ok}
        record["log"].append(entry)
        print(f"turn {k}: {s['id']} exact={entry['exact']} wellformed={entry['wellformed']}", flush=True)

    # ---- last turn: the late probe round, reordered, not flagged as a repeat.
    by_id = dict(PROBES)
    late_items = [(i, by_id[i]) for i in LATE_ORDER]
    messages.append({"role": "user", "content": probe_prompt(late_items)})
    reply = call_model(messages, args.model, key)
    messages.append({"role": "assistant", "content": reply})
    late = parse_reply(reply)
    record["late"] = late
    record["late_wellformed"] = {i: parse_sentence(a, lx).ok for i, a in late.items()}
    record["log"].append({"turn": args.turns + 2, "kind": "probe-late", "reply": reply})
    print(f"turn {args.turns + 2}: late probe round, {len(late)}/12 parsed", flush=True)

    # ---- signal 1: probe divergence.
    diverged = [(i, early.get(i), late.get(i)) for i, _ in PROBES
                if early.get(i) != late.get(i)]
    record["diverged"] = diverged

    # ---- signal 2: filler accuracy by half.
    f = [e for e in record["log"] if e["kind"] == "filler"]
    half = len(f) // 2
    record["filler_accuracy"] = {
        "first_half": sum(e["exact"] for e in f[:half]),
        "first_half_n": half,
        "second_half": sum(e["exact"] for e in f[half:]),
        "second_half_n": len(f) - half,
        "wellformed_first": sum(e["wellformed"] for e in f[:half]),
        "wellformed_second": sum(e["wellformed"] for e in f[half:]),
    }

    # ---- signal 3: Korean leakage over the whole session.
    toks = []
    for e in record["log"]:
        toks += stone_tokens(e.get("reply", "") or e.get("got", ""))
    record["korean_leaks"] = korean_leaks(toks, lx, ko)
    record["tokens_emitted"] = len(toks)

    Path(args.out).write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    fa = record["filler_accuracy"]
    print(f"\nprobe divergence: {len(diverged)}/12")
    print(f"filler exact: {fa['first_half']}/{fa['first_half_n']} early, "
          f"{fa['second_half']}/{fa['second_half_n']} late")
    print(f"filler well formed: {fa['wellformed_first']}/{fa['first_half_n']} early, "
          f"{fa['wellformed_second']}/{fa['second_half_n']} late")
    print(f"korean leakage: {len(record['korean_leaks'])} distinct tokens "
          f"out of {record['tokens_emitted']} emitted")
    print(f"written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
