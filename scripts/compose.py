#!/usr/bin/env python3
"""Deterministic English -> stone. No model, no key (D107).

The companion to `realize.py`, and the harder direction, because English has to
be analysed rather than generated. Three of the four steps are close to
mechanical and one is not, which is worth stating plainly since it decides where
a model would go if one is ever added:

  1. EVIDENTIAL AND STANCE — a lookup. Every marked slot carries one of a fixed
     list of English cues, enforced as a hard error (D84, D91, D94, D105), and a
     sentence with no cue is direct. Measured at 91% and 98% from the English
     alone, ~97% once questions are excluded because their slot is empty by rule
     (D33), near 99% with imperative detection (D106).
  2. LEXICAL SELECTION — a lookup. 240 of the 243 English terms naming roots name
     exactly one. The three that do not (`choose`, `hold`, `variable`) are
     flagged rather than guessed.
  3. LINEARISATION — a total function since word order closed: subject, n-times,
     object, adverbials, verb (D102, D103).
  4. ENGLISH PARSING — the real work, and ordinary NLP rather than anything about
     this language. What is here is a shallow pattern analyser: it finds the verb
     through the reverse lexicon and reads the rest off prepositions. It is
     enough for the corpus's register and it will not survive arbitrary English.

Every failure is reported rather than guessed past. `compose()` returns the
script, the parser's gloss of it, and a list of `unresolved` notes; a caller that
wants a model can hand it exactly those. That is the seam, and it is the reason
this is worth having model-free: a model asked to translate will always answer,
and an answer with no confession is unusable as a check.

Usage:
  compose.py "Run the test."                English -> the script
  compose.py --score                        every corpus line, against gold
  compose.py --score --held                 the held split only
  compose.py --score --show N               print the first N mismatches
  compose.py --roundtrip "Run the test."    compose, realise back, report drift
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence  # noqa: E402
from realize import IRREGULAR, OVERRIDE  # noqa: E402
from validate import SLOT_CUES  # noqa: E402

PAST_TO_BASE = {v: k for k, v in IRREGULAR.items()}
# Prepositions map onto the closed set of markers. The location case does double
# duty as the recipient (D57), which is why `to` and `in` land on the same one.
PREP = {"in": "LOC", "at": "LOC", "on": "LOC", "into": "LOC", "to": "LOC", "here": "HERE",
        "there": "THERE", "now": "NOW", "then": "THEN", "with": "WITH", "for": "FOR",
        "from": "FROM", "out": "FROM", "before": "BEF", "by": "BEF", "after": "AFT",
        "since": "AFT", "than": "FROM"}
NEGATORS = {"not", "n't", "no", "never", "cannot", "don't", "doesn't", "didn't",
            "won't", "isn't", "can't"}
# English contractions, expanded before anything is looked up. The corpus English
# uses them everywhere and no root is ever going to be found for "it'll".
CONTRACTIONS = [
    ("i'm", "i am"), ("i'll", "i will"), ("we'll", "we will"), ("you'll", "you will"),
    ("it'll", "it will"), ("that's", "that is"), ("there's", "there is"),
    ("it's", "it is"), ("what's", "what is"), ("don't", "do not"), ("doesn't", "does not"),
    ("didn't", "did not"), ("won't", "will not"), ("isn't", "is not"), ("can't", "cannot"),
    ("i've", "i have"), ("hasn't", "has not"), ("haven't", "have not"),
]
# The interrogative root plus a marker does every question word (D45).
WH_ADVERB = {"how": "WITH", "where": "LOC", "why": "FOR"}
MODAL_WORD = {"can": "be able, have the capacity", "could": "be able, have the capacity",
              "able": "be able, have the capacity", "want": "want", "wants": "want",
              "should": "should, ought", "ought": "should, ought",
              "may": "allow, may", "allowed": "allow, may"}


class Composer:
    def __init__(self):
        self.lx = Lexicon()
        g = lambda gl: next((e["form"] for e in self.lx.entries if e["gloss"] == gl), None)  # noqa: E731
        self.M = {"OBJ": g("case: object"), "LOC": g("case: location"), "POSS": g("case: possessor"),
                  "WITH": g("relational: with"), "FOR": g("relational: for"),
                  "FROM": g("relational: from"), "BEF": g("relational: before"),
                  "AFT": g("relational: after")}
        self.I, self.YOU = g("pronoun: I"), g("pronoun: you")
        self.THIS, self.THAT = g("pronoun: this one"), g("pronoun: that one")
        self.Q, self.IF = self.lx.question_particle, g("if")
        self.OR, self.BUT = g("or"), g("but")
        self.EVERY, self.NONE = g("every, all"), g("no, none")
        self.WHAT, self.TIME, self.PERSON = g("what, which"), g("time"), g("person")
        self.TRUE, self.REPEAT = g("true, hold"), "메루"
        self.AFFIX = {a["gloss"]: a["form"] for a in self.lx.entries if a.get("pos") == "affix"}
        self.NUM = {e["gloss"].split(",")[0].strip(): e["form"]
                    for e in self.lx.entries if e.get("pos") == "num"}
        self.reverse, self.ambiguous = self._reverse_index()

    def _reverse_index(self):
        """English term -> root. The three terms naming two roots are kept apart
        so they can be reported instead of silently resolved (D95, D101)."""
        idx, clash = {}, {}
        for e in self.lx.entries:
            if e.get("pos") not in ("root", "num"):
                continue
            terms = [t.strip().lower() for t in e["gloss"].split(",")]
            m = re.search(r"Verbal:\s*([^.]+)\.", e.get("sense_notes", ""))
            if m:
                terms += [re.sub(r"^to\s+", "", t.strip().lower())
                          for t in m.group(1).split(",")]
            if e["form"] in OVERRIDE:
                terms += [t.lower() for t in OVERRIDE[e["form"]]]
            for t in terms:
                if not t or len(t.split()) > 3:
                    continue
                if t in idx and idx[t] != e["form"]:
                    clash.setdefault(t, {idx[t]}).add(e["form"])
                else:
                    idx[t] = e["form"]
        return idx, clash

    # ---------- English analysis ----------
    def lemma(self, w):
        w = w.lower().strip(".,;:!?")
        if w in self.reverse:
            return w
        if w in PAST_TO_BASE:
            return PAST_TO_BASE[w]
        for cut, add in (("ies", "y"), ("ied", "y"), ("ed", ""), ("ing", ""), ("es", ""), ("s", "")):
            if w.endswith(cut):
                cand = w[: -len(cut)] + add
                if cand in self.reverse:
                    return cand
                if cand + "e" in self.reverse:
                    return cand + "e"
        return w

    def slots(self, en, imperative, question):
        """Evidential and stance from the fixed cues. A question's slot is empty
        (D33); no cue means direct; the predict stance supplies inferred (D88)."""
        low = en.lower()
        ev, stance = None, None
        for slot, cues in SLOT_CUES.items():
            if any(c in low for c in cues):
                if slot.startswith("stance"):
                    stance = slot
                elif ev is None:
                    ev = slot
        if imperative:
            stance = "stance: intend"
        if stance == "stance: predict":
            ev = "evidential: inferred"
        if question:
            return None, stance
        return ev or "evidential: direct", stance

    def strip_cues(self, en):
        low = en
        for cues in SLOT_CUES.values():
            for c in sorted(cues, key=len, reverse=True):
                low = re.sub(r",?\s*" + re.escape(c) + r"\b", " ", low, flags=re.I)
        return re.sub(r"\s+", " ", low).strip(" ,.;")

    def verb_ending(self, root, neg, tense, ev, stance, sub=False):
        out = root
        if neg:
            out += self.AFFIX["negation"]
        if tense:
            out += self.AFFIX[tense]
        if ev:
            out += self.AFFIX[ev]
        if stance:
            out += self.AFFIX[stance]
        if sub:
            out += self.AFFIX["subordinator"]
        return out

    def phrase(self, words, notes):
        """A noun phrase: determiner or numeral, then the head."""
        out = []
        for w in words:
            lw = w.lower().strip(".,;:!?'")
            if lw in ("the", "a", "an", "of") or lw in self.AUX:
                continue
            if lw == "we":
                out += [self.I, self.YOU, self.M["WITH"]]   # I + you + with (D64)
                continue
            if lw in ("i", "me", "my"):
                out.append(self.I)
            elif lw in ("you", "your"):
                out.append(self.YOU)
            elif lw in ("it", "that", "its"):
                out.append(self.THAT)
            elif lw == "this":
                out.append(self.THIS)
            elif lw in ("every", "all", "each"):
                out.append(self.EVERY)
            elif lw in ("no", "nothing", "nobody", "none"):
                out.append(self.NONE)
                if lw == "nothing":
                    out.append(self.lx.by_form.get("토", {}).get("form", "토"))
                if lw == "nobody":
                    out.append(self.PERSON)
            elif lw in self.NUM:
                out.append(self.NUM[lw])
            elif lw in ("what", "which"):
                out.append(self.WHAT)
            elif lw == "who":
                out += [self.WHAT, self.PERSON]
            else:
                lem = self.lemma(lw)
                if lem in self.ambiguous:
                    notes.append(f"{lw!r} names {len(self.ambiguous[lem])} roots; "
                                 f"the corpus does not decide it from the English alone")
                    return None
                if lem not in self.reverse:
                    notes.append(f"no root for {lw!r}")
                    return None
                out.append(self.reverse[lem])
        return out

    AUX = {"did", "does", "do", "will", "is", "are", "was", "were", "be", "been",
           "am", "has", "have", "had", "'ll", "'s"}
    COPULA_WORDS = {"is", "are", "was", "were", "be"}

    def compose(self, english):
        """English -> (script, gloss, notes). `notes` is what it could not settle."""
        notes = []
        text = english.strip()
        low_all = text.lower()
        for a, b in CONTRACTIONS:
            low_all = re.sub(r"\b" + re.escape(a) + r"\b", b, low_all)
        text = low_all
        question = text.rstrip().endswith("?")
        first = re.split(r"[.;?!]", text)[0].strip()
        conditional = bool(re.match(r"^if\b", first, re.I))
        body = self.strip_cues(re.split(r"[.;?!]", text)[0] if not conditional else text)
        body = re.sub(r"^[Ii]f\s+", "", body)
        protasis = None
        if conditional:
            m = re.split(r",", body, 1)
            if len(m) == 2:
                protasis, body = m[0].strip(), m[1].strip()
        words = [w for w in re.findall(r"[A-Za-z']+", body)]
        if not words:
            return None, None, ["nothing to compose"]

        neg = any(w.lower() in NEGATORS or w.lower().endswith("n't") for w in words)
        words = [w for w in words if w.lower() not in NEGATORS and not w.lower().endswith("n't")]
        modal = next((MODAL_WORD[w.lower()] for w in words if w.lower() in MODAL_WORD), None)
        words = [w for w in words if w.lower() not in MODAL_WORD]

        tense = None
        low = [w.lower() for w in words]
        if "will" in low or "'ll" in low:
            tense = "tense: future"
        imperative = (not conditional and not question
                      and low and low[0] not in ("i", "you", "it", "this", "that", "the", "a",
                                                 "an", "there", "every", "no", "nothing", "nobody")
                      and self.lemma(low[0]) in self.reverse)
        words = [w for w in words if w.lower() not in ("will", "'ll")]
        low = [w.lower() for w in words]

        # Possession first: have is an auxiliary everywhere else, so the verb
        # search below would step over it. There is no verb have — possession is
        # the possessor case plus the hold root (D49).
        hi = next((i for i, w in enumerate(low)
                   if w in ("have", "has", "had") and i + 1 < len(low)
                   and low[i + 1] not in ("been", "be")), None)
        if hi is not None and hi > 0:
            owner = self.phrase(words[:hi], notes)
            owned = self.phrase(words[hi + 1:], notes)
            if owner is None or owned is None:
                return None, None, notes
            ev, stance = self.slots(english, False, question)
            pred = self.verb_ending(self.TRUE, neg, "tense: past" if low[hi] == "had" else tense,
                                    ev, stance)
            out = owner + [self.M["POSS"]] + owned + [pred] + ([self.Q] if question else [])
            return self._finish(out, notes)

        # the verb: the first non-auxiliary whose lemma names a root
        vi = None
        for i, w in enumerate(low):
            if w in self.AUX:
                if w == "did":
                    tense = "tense: past"
                continue
            if self.lemma(w) in self.reverse and (i > 0 or imperative):
                vi = i
                break
        if vi is None:
            for i, w in enumerate(low):
                if w in self.COPULA_WORDS:
                    vi = i
                    break
        if vi is None:
            return None, None, ["no verb found in " + repr(body)]
        if low[vi] in self.COPULA_WORDS or (vi and low[vi - 1] in self.COPULA_WORDS):
            if low[min(vi, len(low) - 1)] in ("was", "were") or "was" in low[:vi] or "were" in low[:vi]:
                tense = tense or "tense: past"
        if tense is None and words[vi].lower() in PAST_TO_BASE:
            tense = "tense: past"
        elif tense is None and re.search(r"ed$", words[vi].lower()) and \
                self.lemma(words[vi]) != words[vi].lower():
            tense = "tense: past"

        pre = [w for w in words[:vi] if w.lower() not in self.AUX]
        lead_wh = None
        if pre and pre[0].lower() in WH_ADVERB:
            lead_wh, pre = WH_ADVERB[pre[0].lower()], pre[1:]
        elif pre and pre[0].lower() == "when":
            lead_wh, pre = "WHEN", pre[1:]
        subj_words = pre
        rest = words[vi + 1:]
        if low[vi] in self.COPULA_WORDS and rest:           # equative: no copula (D56)
            head = self.lemma(rest[-1])
            verb_root = self.reverse.get(head)
            if verb_root is None:
                return None, None, [f"no root for the complement {rest[-1]!r}"]
            rest = rest[:-1]
        else:
            verb_root = self.reverse.get(self.lemma(words[vi]))
            if verb_root is None:
                return None, None, [f"no root for the verb {words[vi]!r}"]

        # split what follows the verb into an object and prepositional phrases
        obj_words, advs, cur, prep = [], [], [], None
        for w in rest:
            lw = w.lower().strip(".,")
            if lw in WH_ADVERB:
                advs.append((WH_ADVERB[lw], ["what"]))
                continue
            if lw == "when":
                advs.append(("WHEN", []))
                continue
            if lw in PREP:
                if prep is None and cur:
                    obj_words = cur
                elif prep is not None:
                    advs.append((prep, cur))
                cur, prep = [], PREP[lw]
                if lw in ("here", "there", "now", "then"):
                    advs.append((PREP[lw], []))
                    cur, prep = [], None
                continue
            cur.append(w)
        if prep is None:
            obj_words = obj_words or cur
        else:
            advs.append((prep, cur))

        if subj_words and subj_words[0].lower() == "there":   # existence (D49)
            subj_words, obj_words, verb_root = obj_words or subj_words[1:], [], self.TRUE
        if verb_root == self.reverse.get("have") or (vi < len(low) and low[vi] in ("have", "has", "had")):
            owner = self.phrase(subj_words, notes)
            owned = self.phrase(obj_words, notes)
            if owner is None or owned is None:
                return None, None, notes
            pred = self.verb_ending(self.TRUE, neg, tense, *self.slots(english, False, question))
            out = owner + [self.M["POSS"]] + owned + [pred] + ([self.Q] if question else [])
            return self._finish(out, notes)

        subj = self.phrase(subj_words, notes) if subj_words else []
        obj = self.phrase(obj_words, notes) if obj_words else []
        if subj is None or obj is None:
            return None, None, notes
        if imperative:
            subj = [self.YOU]
        adv_out = []
        for mark, ws in advs:
            if mark == "WHEN":
                adv_out += [self.WHAT, self.TIME, self.M["LOC"]]
                continue
            if mark in ("HERE", "THERE", "NOW", "THEN"):
                dem = self.THIS if mark in ("HERE", "NOW") else self.THAT
                adv_out += [dem] + ([self.TIME] if mark in ("NOW", "THEN") else []) + [self.M["LOC"]]
                continue
            ph = self.phrase(ws, notes)
            if ph is None:
                return None, None, notes
            adv_out += ph + [self.M[mark]]

        if lead_wh == "WHEN":
            adv_out += [self.WHAT, self.TIME, self.M["LOC"]]
        elif lead_wh:
            adv_out += [self.WHAT, self.M[lead_wh]]
        ev, stance = self.slots(english, imperative, question)
        if modal:
            inner = self.verb_ending(verb_root, neg, tense, "evidential: general", None, sub=True)
            modal_root = next(e["form"] for e in self.lx.entries if e["gloss"] == modal)
            pred = self.verb_ending(modal_root, False, None, ev, stance)
            out = subj + (obj + [self.M["OBJ"]] if obj else []) + adv_out + [inner, pred]
        else:
            pred = self.verb_ending(verb_root, neg, tense, ev, stance)
            out = subj + (obj + [self.M["OBJ"]] if obj else []) + adv_out + [pred]
        if protasis:
            p_script, _, p_notes = self.compose(protasis)
            if p_script is None:
                notes += ["the condition: " + "; ".join(p_notes)]
            else:
                cond = p_script.split()
                cond[-1] = self.verb_ending(
                    parse_sentence(p_script, self.lx).tokens[-1].base["form"], False, None,
                    "evidential: general", None)
                out = cond + [self.IF] + out
        if question:
            out += [self.Q]
        return self._finish(out, notes)

    def _finish(self, tokens, notes):
        script = " ".join(tokens)
        parsed = parse_sentence(script, self.lx)
        if not parsed.ok:
            return None, None, notes + parsed.errors
        return script, parsed.gloss(), notes


def roundtrip(english):
    """English -> stone -> English, and how far the return trip drifted.

    With both directions deterministic the framework can check itself: compose,
    realise the result, and compare. Measured over the corpus the signal
    separates — mean similarity 0.69 where the composition was exactly right
    against 0.44 where it was not — but it separates too weakly to gate on, so
    it is reported as a confidence and never as a verdict. It is also the natural
    seam for a model: hand it the low-similarity cases, not the whole corpus.
    """
    from realize import Realizer, content
    script, gloss, notes = Composer().compose(english)
    if script is None:
        return {"script": None, "notes": notes, "similarity": 0.0}
    back, _ = Realizer().realize(script)
    a, b = set(content(english)), set(content(back or ""))
    sim = len(a & b) / max(1, len(a | b))
    return {"script": script, "gloss": gloss, "back": back,
            "similarity": round(sim, 2), "notes": notes}


def score(argv):
    c = Composer()
    rows = [json.loads(l) for l in (ROOT / "corpus/corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    if "--held" in argv:
        rows = [x for x in rows if x["split"] == "held"]
    show = int(argv[argv.index("--show") + 1]) if "--show" in argv else 0
    exact = declined = 0
    misses = []
    for x in rows:
        out, _, notes = c.compose(x["en"])
        if out is None:
            declined += 1
            misses.append((x["id"], x["en"], x["st"], "declined: " + "; ".join(notes)))
        elif out == x["st"]:
            exact += 1
        else:
            misses.append((x["id"], x["en"], x["st"], out))
    n = len(rows)
    print(f"compose.py: {n} sentences")
    print(f"  exact match on the script : {exact}/{n} = {100*exact/n:.1f}%")
    print(f"  declined (said so)        : {declined}/{n} = {100*declined/n:.1f}%")
    print(f"  wrong (did not say so)    : {n-exact-declined}/{n} = {100*(n-exact-declined)/n:.1f}%")
    for m in misses[:show]:
        print(f"\n  {m[0]}  {m[1]}\n    gold {m[2]}\n    got  {m[3]}")
    return 0


def main():
    if "--score" in sys.argv:
        return score(sys.argv)
    if "--roundtrip" in sys.argv:
        r = roundtrip(sys.argv[sys.argv.index("--roundtrip") + 1])
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0 if r["script"] else 1
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    script, gloss, notes = Composer().compose(sys.argv[1])
    for n in notes:
        print("  note:", n, file=sys.stderr)
    if script:
        print(script)
        print("  " + gloss, file=sys.stderr)
    return 0 if script else 1


if __name__ == "__main__":
    sys.exit(main())
