#!/usr/bin/env python3
"""Choose descriptions for missing words by measured decodability (D144).

D140 adopted description, toki pona's way, and D141 found that teaching ten
descriptions taught those ten and not the method. This turns the round trip into
a generator: several models propose descriptions for each concept, other models
translate each candidate blind, a judge checks whether the English names the
concept, and the best-decoded candidate wins. A model that took no part in the
scoring then re-decodes the winners and the losers. If winners still beat losers
there, selection found something real and not one model's taste.

Usage:
  select_descriptions.py run CONCEPTS.json OUT.json
CONCEPTS is a list of {"en": term, "def": one-line definition}. Needs OPENROUTER_API_KEY.
"""
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hashlib  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402

import roundtrip_test  # noqa: E402
from roundtrip_test import CHUNK, context, numbered  # noqa: E402

# Every model call is cached on disk, keyed by model and prompt, so a run that dies
# resumes where it stopped (the first pilot was killed at its time limit with
# nothing saved and no way to tell which stage hung).
_CACHE, _CACHE_PATH, _LOCK = {}, None, threading.Lock()


def call(model, prompt):
    key = hashlib.sha256((model + "\0" + prompt).encode()).hexdigest()
    with _LOCK:
        if key in _CACHE:
            return _CACHE[key]
    t0 = time.time()
    out = roundtrip_test.call(model, prompt)
    print("  call %-28s %5.0fs %s" % (model, time.time() - t0, "ERROR" if out.startswith("ERROR") else "ok"), flush=True)
    if not out.startswith("ERROR"):
        with _LOCK:
            _CACHE[key] = out
            if _CACHE_PATH:
                _CACHE_PATH.write_text(json.dumps(_CACHE), encoding="utf-8")
    return out
from stonelib import ROOT, Lexicon, is_name, parse_sentence  # noqa: E402

GENERATORS = ["google/gemini-3.8-flash", "x-ai/grok-4.6", "z-ai/glm-5.3"]
DECODERS = ["google/gemini-3.8-flash", "x-ai/grok-4.6", "openai/gpt-5.6-luna"]
JUDGE = "anthropic/claude-sonnet-4.5"
HELD_OUT = "deepseek/deepseek-v3.2"      # never generates or scores
CARRIER = "에 %s 파 치카마"              # "Check the X." (imperative, object)

GEN_PROMPT = """The language has no word for each concept below. Name each one by DESCRIPTION, the way
toki pona does, using only words that appear in the sentence pairs above. Two rules:
1. The head is the most specific word for what the thing IS (a number, a program, a file,
   a list, a machine, a message ...), never just "place" or "thing" when a narrower word exists.
2. Attach a modifier with the possessor word, as the corpus does: "the network's storage" for
   a network drive, "the place's name" for a path, "the start's number" for a random seed.
Keep each to a short noun phrase. No Latin letters, no verb endings.

For each concept give THREE different candidate phrases, in this exact format:
N. phrase | phrase | phrase
Output only the numbered lines.

"""

DECODE_PROMPT = "Translate each into English. Output only a numbered list, nothing else."

JUDGE_PROMPT = """Each item gives a CONCEPT with its definition and an English SENTENCE that someone
produced. Answer YES if the sentence refers to that concept: its usual name, or wording a
colleague would immediately take to mean it. Answer NO if it names something more general,
something different, or something vague. Be strict: "the storage" is NO for "network drive".
Answer with one line per item, exactly "N. YES" or "N. NO", nothing else.

"""


def candidates_from(model, ctx, concepts):
    listing = "\n".join("%d. %s: %s" % (i + 1, c["en"], c["def"]) for i, c in enumerate(concepts))
    got = numbered(call(model, ctx + "\n\n" + GEN_PROMPT + listing), len(concepts))
    return {i - 1: [p.strip() for p in line.split("|") if p.strip()] for i, line in got.items()}


def valid_phrase(p, lx):
    """A noun phrase of known words: parses, no verb endings, no names, no final marker."""
    toks = p.split()
    if not toks or len(toks) > 6 or any(is_name(t) for t in toks):
        return False
    s = parse_sentence(CARRIER % p, lx)
    if not s.ok:
        return False
    body = s.tokens[1:1 + len(toks)]
    return all(not t.affixes for t in body) and toks[-1] not in lx.markers


def decode(model, ctx, sentences):
    out = {}
    for start in range(0, len(sentences), CHUNK):
        chunk = sentences[start:start + CHUNK]
        listing = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(chunk))
        got = numbered(call(model, ctx + "\n\n" + DECODE_PROMPT + "\n\n" + listing), len(chunk))
        for i, s in got.items():
            out[start + i - 1] = s
    return out


def judge(items):
    """items: list of (concept, definition, english). Returns list of bool or None."""
    res = [None] * len(items)
    for start in range(0, len(items), CHUNK):
        chunk = items[start:start + CHUNK]
        listing = "\n".join("%d. CONCEPT: %s (%s)\n   SENTENCE: %s" % (k + 1, c, d, e)
                            for k, (c, d, e) in enumerate(chunk))
        got = numbered(call(JUDGE, JUDGE_PROMPT + listing), len(chunk))
        for k in range(len(chunk)):
            v = (got.get(k + 1) or "").strip().upper()
            res[start + k] = True if v.startswith("YES") else False if v.startswith("NO") else None
    return res


def score(cands, concepts, ctx, models, exclude_self=True):
    """Decode every candidate in a shuffled order with each model; judge; return per-candidate hits."""
    order = list(range(len(cands)))
    random.Random(0).shuffle(order)            # siblings never sit next to each other
    sents = [CARRIER % cands[i]["st"] for i in order]
    with ThreadPoolExecutor(len(models)) as ex:
        decoded = dict(zip(models, ex.map(lambda m: decode(m, ctx, sents), models)))
    items, keys = [], []
    for m in models:
        for pos, i in enumerate(order):
            if exclude_self and m in cands[i]["by"] and len(cands[i]["by"]) == 1:
                continue
            c = concepts[cands[i]["concept"]]
            items.append((c["en"], c["def"], decoded[m].get(pos) or "(nothing)"))
            keys.append((i, m))
    verdict = judge(items)
    for (i, m), v, it in zip(keys, verdict, items):
        cands[i].setdefault("decodes", {})[m] = {"en": it[2], "yes": v}
    return cands


def cmd_run(cpath, opath):
    global _CACHE, _CACHE_PATH
    _CACHE_PATH = Path(opath + ".cache.json")
    if _CACHE_PATH.exists():
        _CACHE = json.loads(_CACHE_PATH.read_text(encoding="utf-8"))
        print("resuming with %d cached calls" % len(_CACHE), flush=True)
    lx = Lexicon()
    concepts = json.load(open(cpath, encoding="utf-8"))
    ctx, _ = context()
    with ThreadPoolExecutor(len(GENERATORS)) as ex:
        proposals = dict(zip(GENERATORS, ex.map(lambda m: candidates_from(m, ctx, concepts), GENERATORS)))
    cands, seen = [], {}
    raw = bad = 0
    for m, by in proposals.items():
        for ci, phrases in by.items():
            for p in phrases:
                raw += 1
                p = re.sub(r"\s+", " ", p.strip(" .\"'`"))
                if not valid_phrase(p, lx):
                    bad += 1
                    continue
                key = (ci, p)
                if key in seen:
                    cands[seen[key]]["by"].append(m)
                else:
                    seen[key] = len(cands)
                    cands.append({"concept": ci, "st": p, "by": [m]})
    print("proposed %d, invalid %d, distinct valid %d" % (raw, bad, len(cands)), flush=True)
    score(cands, concepts, ctx, DECODERS)
    for c in cands:
        v = [d["yes"] for d in c["decodes"].values() if d["yes"] is not None]
        c["rate"] = sum(v) / len(v) if v else 0.0
    # winners and the worst candidate per concept, re-decoded by the held-out model
    best, worst = {}, {}
    for i, c in enumerate(cands):
        k = c["concept"]
        if k not in best or c["rate"] > cands[best[k]]["rate"]:
            best[k] = i
        if k not in worst or c["rate"] < cands[worst[k]]["rate"]:
            worst[k] = i
    probe = sorted(set(best.values()) | set(worst.values()))
    sub = [dict(cands[i]) for i in probe]
    score(sub, concepts, ctx, [HELD_OUT], exclude_self=False)
    for i, s in zip(probe, sub):
        cands[i]["held_out"] = s["decodes"][HELD_OUT]
    out = {"concepts": concepts, "candidates": cands, "best": best, "worst": worst,
           "generators": GENERATORS, "decoders": DECODERS, "judge": JUDGE, "held_out": HELD_OUT}
    Path(opath).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    summarise(out)


def summarise(out):
    C, cands = out["concepts"], out["candidates"]
    best = {int(k): v for k, v in out["best"].items()}
    worst = {int(k): v for k, v in out["worst"].items()}
    mean_all = sum(c["rate"] for c in cands) / len(cands)
    mean_best = sum(cands[i]["rate"] for i in best.values()) / len(best)
    print("candidates decoded by other models: mean %.0f%%; best per concept: mean %.0f%%"
          % (100 * mean_all, 100 * mean_best))
    ho = lambda idx: [cands[i]["held_out"]["yes"] for i in idx if cands[i].get("held_out")]  # noqa: E731
    hb = [v for v in ho([best[k] for k in best if best[k] != worst[k]]) if v is not None]
    hw = [v for v in ho([worst[k] for k in worst if best[k] != worst[k]]) if v is not None]
    if hb and hw:
        print("held-out %s: winners decoded %d/%d (%.0f%%), losers %d/%d (%.0f%%)"
              % (out["held_out"], sum(hb), len(hb), 100 * sum(hb) / len(hb), sum(hw), len(hw), 100 * sum(hw) / len(hw)))
    tiers = {"won (>=2/3)": 0, "weak (1/3-2/3)": 0, "none (<1/3)": 0}
    for k in sorted(best):
        r = cands[best[k]]["rate"]
        tiers["won (>=2/3)" if r >= 2 / 3 else "weak (1/3-2/3)" if r >= 1 / 3 else "none (<1/3)"] += 1
    print("concepts:", ", ".join("%s %d" % kv for kv in tiers.items()), "of", len(best))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["run"] and len(a) == 3:
        cmd_run(a[1], a[2])
    elif a[:1] == ["summary"] and len(a) == 2:
        summarise(json.load(open(a[1], encoding="utf-8")))
    else:
        print(__doc__)
        sys.exit(2)
