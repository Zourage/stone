#!/usr/bin/env python3
"""Deterministic stone -> English. No model, no key (D106).

The parse side has been deterministic since D72: every sentence reads exactly
one way, and `translate.py gloss` prints the morphemes. What was missing was the
other half of that direction — turning the gloss into English — and it only
became writable now, because generating a sentence needs a total function from
structure to order and the corpus did not have one until word order closed
(D102, D103). Three more things make it tractable and are worth naming, since
each was decided for another reason:

  * the evidential and stance map to a FIXED list of English cues, enforced as a
    hard error (D84, D91, D94, D105), so realising them is a table lookup;
  * 240 of the 243 English terms in the lexicon name exactly one root, so the
    reverse lookup used here is nearly a function;
  * there is no agreement, no plural and no article to generate from, so English
    morphology is the only inflection this has to invent.

What it is for is not translation. `to-english` already does that better with a
model. This is a THIRD CHECK ON THE CORPUS, after the validator and the
acceptance test: an algorithm that cannot decide something is standing on a
place where the corpus does not determine it, and it says so instead of guessing
plausibly, which is what a model does and why a model cannot find these. It does
NOT stand in for the acceptance test, which asks whether a cold reader can
reconstruct the language from the corpus — this was written from the spec, so it
says nothing about that (D94's warning, one level up).

Usage:
  realize.py "<a sentence in the script>"   one sentence
  realize.py --score                        every corpus line, against gold
  realize.py --score --held                 the held split only
  realize.py --score --show N               print the first N mismatches
  realize.py --ambiguous                    every split the corpus leaves undecidable
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import ROOT, Lexicon, parse_sentence  # noqa: E402

# Irregular English verbs, and the few roots whose gloss does not inflect as a
# verb. Everything else is derived from the lexicon: the gloss is the noun and
# the `Verbal:` clause, where there is one, is the verb (D106).
IRREGULAR = {
    "run": "ran", "read": "read", "write": "wrote", "build": "built", "hold": "held",
    "take": "took", "give": "gave", "begin": "began", "do": "did", "say": "said",
    "tell": "told", "know": "knew", "find": "found", "get": "got", "make": "made",
    "put": "put", "keep": "kept", "leave": "left", "send": "sent", "understand": "understood",
    "choose": "chose", "think": "thought", "become": "became", "come": "came", "go": "went",
    "see": "saw", "set": "set", "cost": "cost", "cut": "cut", "let": "let", "meet": "met",
    "lose": "lost", "win": "won", "feel": "felt", "mean": "meant", "spend": "spent",
}
COPULA_PAST = {"is": "was", "are": "were"}

# The fourteen roots whose head gloss is a phrase rather than a word, plus the
# handful whose noun and verb differ. Everything else comes out of the lexicon.
OVERRIDE = {                               # form: (noun, verb)
    "사": ("knowledge", "know"), "세": ("definition", "know"), "시": ("belief", "believe"),
    "차": ("question", "ask"), "체": ("request", "ask for"), "치": ("check", "check"),
    "새루": ("setup", "set up"), "태노": ("light one", "be light"),
    "미예": ("turn", "take a turn"), "레세": ("owner", "be responsible for"),
    "레차": ("handover", "hand over"), "데패": ("open item", "be open"),
    "라태": ("trust", "trust"), "얘": ("truth", "be"), "후태": ("place", "be"),
}

# Roots that English predicates with a copula. Derived once from the corpus:
# a root is here when two or more gold sentences render its predicate use as
# "is <gloss>". The distinction is a fact about English, not about the language,
# which has no copula at all (D56).
COPULA = {"나대", "내", "노", "노대", "대", "도", "두", "두차", "래", "로", "리네", "마소",
          "마수", "매시", "소루", "수초", "수포", "얘하", "초", "코대", "타로", "타리", "태",
          "테", "테해", "테호", "티패", "파수", "파시", "파캐", "패노", "패누", "포하", "포해",
          "푸세", "푸소", "해위"}
COPULA_NOUN = {"내", "노", "대", "도", "두", "두차", "소루", "수포", "티패"}
COMPARATIVE = {"good": "better", "bad": "worse", "far": "further", "many": "more"}


def comparative(adj):
    """English marks comparison on the adjective; the language marks it on the
    standard, with the from word, and has no comparative form at all (D65)."""
    if adj in COMPARATIVE:
        return COMPARATIVE[adj]
    if len(adj.split()) > 1 or len(adj) > 7:
        return "more " + adj
    if adj.endswith("e"):
        return adj + "r"
    if re.fullmatch(r"[a-z]*[aeiou][^aeiouwy]", adj):
        return adj + adj[-1] + "er"          # big -> bigger
    if re.search(r"[^aeiou]y$", adj):
        return adj[:-1] + "ier"
    return adj + "er"

CUE = {                                    # the fixed cues, D94's list, one each
    "evidential: reported": ", I'm told", "evidential: inferred": ", it seems",
    "evidential: general": ", as such", "evidential: direct": "",
    "stance: intend": ", that's the plan", "stance: predict": ", I expect",
    "stance: propose": ", just a proposal", "stance: trust": ", you can count on that",
    "stance: risk": ", that might go wrong", "stance: assert": ", I insist",
}


class English:
    """The English side of the lexicon, derived from it rather than restated."""

    def __init__(self, lx):
        self.lx = lx
        self.noun, self.verb = {}, {}
        for e in lx.entries:
            if e.get("pos") not in ("root", "num"):
                continue
            head = e["gloss"].split(",")[0].strip()
            m = re.search(r"Verbal:\s*([^.]+)\.", e.get("sense_notes", ""))
            v = re.sub(r"^to\s+", "", m.group(1).split(",")[0].strip()) if m else head
            if e["form"] in OVERRIDE:
                head, v = OVERRIDE[e["form"]]
            self.noun[e["form"]], self.verb[e["form"]] = head, v

    def present(self, v):
        if v == "be":
            return "is"
        if v.startswith("be "):
            return "is " + v[3:]
        return v

    def past(self, v):
        if v == "be":
            return "was"
        if v.startswith("be "):
            return "was " + v[3:]
        first, rest = (v.split(" ", 1) + [""])[:2]
        if first in COPULA_PAST:
            p = COPULA_PAST[first]
        elif first in IRREGULAR:
            p = IRREGULAR[first]
        elif first.endswith("e"):
            p = first + "d"
        elif re.search(r"[^aeiou]y$", first):
            p = first[:-1] + "ied"
        else:
            p = first + "ed"
        return (p + " " + rest).strip()


class Realizer:
    def __init__(self):
        self.lx = Lexicon()
        self.en = English(self.lx)
        g = lambda gl: next((e["form"] for e in self.lx.entries if e["gloss"] == gl), None)  # noqa: E731
        self.OBJ, self.LOC, self.POSS = g("case: object"), g("case: location"), g("case: possessor")
        self.WITH, self.FOR, self.FROM = g("relational: with"), g("relational: for"), g("relational: from")
        self.BEF, self.AFT = g("relational: before"), g("relational: after")
        self.I, self.YOU = g("pronoun: I"), g("pronoun: you")
        self.THIS, self.THAT = g("pronoun: this one"), g("pronoun: that one")
        self.Q, self.IF = self.lx.question_particle, g("if")
        self.markers_plus = None
        self.OR, self.BUT = g("or"), g("but")
        self.EVERY, self.NONE = g("every, all"), g("no, none")
        self.WHAT, self.TIME = g("what, which"), g("time")
        self.PERSON, self.THING = g("person"), g("thing")
        self.TRUE = g("true, hold")
        self.MODALS = {g("be able, have the capacity"): "can", g("want"): "want to",
                       g("should, ought"): "should", g("allow, may"): "may"}
        self.markers = self.lx.markers | {self.IF}
        self.HEADS = {e["form"] for e in self.lx.entries if e.get("pos") in ("root", "num")}
        self.ROOTS = {e["form"] for e in self.lx.entries if e.get("pos") == "root"}
        self.pron = {self.I: ("I", "me"), self.YOU: ("you", "you"),
                     self.THIS: ("this one", "this one"), self.THAT: ("it", "it")}

    # ---------- phrases ----------
    def np(self, idx, toks, forms, case=None):
        """Render a bare argument phrase: determiners, numerals, compounds, head."""
        heads = [forms[i] for i in idx]
        if len(heads) == 1 and heads[0] in self.pron:
            return self.pron[heads[0]][1 if case else 0]
        words = []
        for k, f in enumerate(heads):
            last = k == len(heads) - 1
            if f == self.EVERY:
                words.append("every")
            elif f == self.NONE:
                words.append("no")
            elif f == self.WHAT:
                words.append("what" if last else "which")
            elif f in self.pron and not last:
                words.append("this" if f == self.THIS else "that")
            elif f in self.pron:
                words.append(self.pron[f][0])
            else:
                words.append(self.en.noun.get(f, f))
        if not any(w in ("every", "no", "which", "this", "that", "what") for w in words[:-1]):
            if words and not words[0][0].isdigit() and words[0] not in ("I", "you", "it", "this one"):
                words[0] = "the " + words[0]
        return " ".join(words)

    def deictic(self, idx, forms, mark):
        """here/there/now/then, which are a pronoun plus location or time (D48)."""
        heads = [forms[i] for i in idx]
        if mark == self.LOC and len(heads) == 1 and heads[0] in (self.THIS, self.THAT):
            return "here" if heads[0] == self.THIS else "there"
        if mark == self.LOC and len(heads) == 2 and heads[1] == self.TIME:
            if heads[0] == self.THIS:
                return "now"
            if heads[0] == self.THAT:
                return "then"
            if heads[0] == self.WHAT:
                return "when"
        if mark == self.LOC and len(heads) == 1 and heads[0] == self.WHAT:
            return "where"
        if mark == self.FOR and len(heads) == 1 and heads[0] == self.WHAT:
            return "why"
        if mark == self.WITH and len(heads) == 1 and heads[0] == self.WHAT:
            return "how"
        return None

    def adverbial(self, idx, mark, forms):
        d = self.deictic(idx, forms, mark)
        if d:
            return d
        inner = self.np(idx, idx, forms, case=True)
        if mark == self.LOC:
            heads = [forms[i] for i in idx]
            if heads[-1] in self.pron or heads[-1] == self.PERSON:
                return "to " + inner       # a recipient takes the location case (D57)
            return "in " + inner
        if mark == self.WITH:
            return "with " + inner
        if mark == self.FOR:
            return "for " + inner
        if mark == self.FROM:
            return "from " + inner
        if mark == self.BEF:
            return "before " + inner
        if mark == self.AFT:
            return "after " + inner
        return inner

    # ---------- predicates ----------
    def copula(self, form, gs):
        """`is`/`was`/`will be` plus the term. The language has no copula: the
        second term simply takes the verb ending (D56), so English supplies one."""
        verb = self.en.verb.get(form, "")
        if verb.startswith("be "):
            term = verb[3:]                  # the lexicon's own "Verbal: to be faulty"
        else:
            term = self.en.noun.get(form, form)
            if form in COPULA_NOUN:
                term = "the " + term
        neg = "negation" in gs
        if "tense: past" in gs:
            return ("was not " if neg else "was ") + term
        if "tense: future" in gs:
            return ("will not be " if neg else "will be ") + term
        return ("is not " if neg else "is ") + term

    def predicate(self, tok, passive=False):
        """The verb, inflected. An agentless clause keeps its object marker and
        drops the subject (D65), which English can only render as a passive."""
        gs = [a["gloss"] for a in tok.affixes]
        cues = "".join(CUE.get(g, "") for g in gs if g.startswith(("evidential", "stance")))
        if "stance: intend" in gs and "tense: future" in gs:
            cues = cues.replace(CUE["stance: intend"], "")
        if tok.base["form"] in COPULA and not passive:
            return self.copula(tok.base["form"], gs), cues
        base = self.en.verb.get(tok.base["form"], tok.base["form"])
        neg = "negation" in gs
        if passive:
            part = self.en.past(base)
            if "tense: future" in gs:
                body = ("will not be " if neg else "will be ") + part
            elif "tense: past" in gs:
                body = ("was not " if neg else "was ") + part
            else:
                body = ("is not " if neg else "is ") + part
        elif "tense: past" in gs:
            body = ("did not " + base) if neg else self.en.past(base)
        elif "tense: future" in gs:
            body = ("will not " if neg else "will ") + base
        else:
            pres = self.en.present(base)
            body = ("is not " + pres[3:] if pres.startswith("is ") else "does not " + base) \
                if neg else pres
        cues = "".join(CUE.get(g, "") for g in gs if g.startswith(("evidential", "stance")))
        if "stance: intend" in gs and "tense: future" in gs:
            cues = cues.replace(CUE["stance: intend"], "")   # "I'll ..." is the cue
        return body, cues

    # ---------- the sentence ----------
    def clauses(self, parsed, forms):
        """Split into clauses at each predicate; a clause is (constituents, predicate)."""
        # In a question the predicate carries no affix at all — the evidential
        # slot is empty and the answer supplies it (D33) — so the last token
        # before the particle is the verb, and splitting on affixes alone would
        # leave the clause with no predicate at all.
        last = None
        if parsed.is_question and len(parsed.tokens) >= 2:
            last = len(parsed.tokens) - 2
        out, cur = [], []
        for i, tk in enumerate(parsed.tokens):
            if tk.affixes or i == last:
                out.append((cur, tk, i))
                cur = []
            else:
                cur.append(i)
        if cur:
            out.append((cur, None, None))
        return out

    def constituents(self, idx, forms):
        """Group a clause's bare tokens into (indices, marker) phrases.

        A token glues to the next only if the next is a root or numeral and the
        current is not a personal pronoun — the determiner rule and D102's
        correction to it. Splitting on markers alone would read `I it-OBJ` as one
        phrase and lose the subject.

        Two roots in a row are genuinely undecidable — a compound, or a bare
        argument followed by a separate marked phrase — and the corpus leaves it
        to the English (STATE, the fourth standing ambiguity). The subject rule
        breaks the tie: the first bare phrase of a clause is its subject (D78,
        D102), so a root that opens a clause is the subject rather than the head
        of a compound. `--ambiguous` lists every place this had to choose.
        """
        out, k, have_subject = [], 0, False
        while k < len(idx):
            start = k
            while (k + 1 < len(idx) and forms[idx[k + 1]] not in self.markers
                   and forms[idx[k + 1]] in self.HEADS
                   and forms[idx[k]] not in (self.I, self.YOU)
                   and not (forms[idx[k]] in self.ROOTS and not have_subject and k == start)):
                k += 1
            group, mark = idx[start:k + 1], None
            if k + 1 < len(idx) and forms[idx[k + 1]] in self.markers:
                mark = forms[idx[k + 1]]
                k += 1
            if mark is None or mark == self.OBJ:
                have_subject = True
            out.append((group, mark))
            k += 1
        return out

    def insert_modal(self, clause, modal):
        """Put the modal before the inner clause's verb, which is the word after
        its subject. The language stacks a modal root over a subordinate clause
        (D61, D63); English puts the auxiliary inside it."""
        w = clause.split()
        if not w:
            return modal
        i = 1 if w[0].lower() in ("i", "you", "it", "we", "they") else 0
        while i < len(w) and w[i] in ("the", "this", "that", "every", "no"):
            i += 2
        head = w[:i] or []
        verb = w[i] if i < len(w) else ""
        rest = w[i + 1:]
        base = re.sub(r"(ed|s)$", "", verb) if verb not in ("is", "was", "are") else "be"
        return " ".join([x for x in head] + [modal, base] + rest)

    WH = ("what", "which", "where", "when", "why", "how", "who")

    def question(self, clause, subj, body, gs):
        """English needs do-support and inversion; the script needs neither — the
        evidential slot is empty and a final particle marks the question (D33)."""
        words = clause.split()
        wh = next((w for w in words if w.lower().strip(",") in self.WH), None)
        if wh:                                   # a wh-question fronts its word
            i = [w.lower().strip(",") for w in words].index(wh.lower().strip(","))
            rest = words[:i] + words[i + 1:]
            cop = next((k for k, w in enumerate(rest) if w in ("is", "was", "are", "were")), None)
            if cop is not None and cop > 0:   # "where the fault is" -> "where is the fault"
                rest = [rest[cop]] + rest[:cop] + rest[cop + 1:]
            if subj and rest and rest[0] == subj.split()[0] and len(body.split()) == 1:
                v = body.split()[0]
                if v not in ("is", "are", "was", "were"):
                    sp = len(subj.split())
                    aux = "did" if "tense: past" in gs else ("will" if "tense: future" in gs else "does")
                    stem = self.en.verb.get(self._last_root, v)
                    rest = rest[:sp] + [stem] + rest[sp + 1:]
                    rest = [aux] + rest
            return " ".join([words[i].capitalize()] + rest)
        if not subj:
            return clause
        rest = clause[len(subj):].strip()
        verb = body.split()[0]
        if verb in ("is", "are", "was", "were", "will", "can", "may", "should"):
            return f"{verb} {subj} {rest[len(verb):].strip()}".strip()
        if "tense: past" in gs:
            stem = self.en.verb.get("", "")
            return f"did {subj} {rest}".strip()
        if "tense: future" in gs:
            return f"will {subj} {rest[len('will'):].strip()}".strip()
        return f"does {subj} {rest}".strip()

    CONTRACT = [(" i will ", " I'll "), (" it will ", " it'll "), (" you will ", " you'll "),
                (" i am ", " I'm "), (" do not ", " don't "), (" does not ", " doesn't "),
                (" did not ", " didn't "), (" will not ", " won't "), (" is not ", " isn't ")]

    def realize(self, text):
        parsed = parse_sentence(text, self.lx)
        if not parsed.ok:
            return None, parsed.errors
        forms = text.split()
        is_q = parsed.is_question
        parts, carried = [], []
        for idx, tok, _ in self.clauses(parsed, forms):
            idx = [i for i in idx if forms[i] != self.Q]
            lead = None
            while idx and forms[idx[0]] in (self.IF, self.OR, self.BUT):
                lead = forms[idx[0]]
                idx = idx[1:]
            if lead == self.IF and (carried or parts):
                protasis = carried.pop() if carried else parts.pop()
                protasis = protasis.replace(CUE["evidential: general"], "")
                parts.append("__IF__" + protasis)
            elif lead in (self.OR, self.BUT) and parts:
                parts[-1] += " " + ("or" if lead == self.OR else "but")
            phr = self.constituents(idx, forms)
            subj, obj, advs = None, None, []
            pending_poss, conj = None, None
            for group, mark in phr:
                if mark is None and subj is None and group:
                    subj = self.np(group, group, forms)
                    if pending_poss:
                        subj, pending_poss = f"{pending_poss} {re.sub(r'^the ', '', subj)}", None
                elif mark == self.OBJ:
                    obj = self.np(group, group, forms, case=True)
                    if pending_poss:
                        obj, pending_poss = f"{pending_poss} {re.sub(r'^the ', '', obj)}", None
                elif mark == self.POSS:
                    poss = self.np(group, group, forms, case=True)
                    pending_poss = re.sub(r"^the ", "", poss) + "'s"
                elif mark in (self.OR, self.BUT):
                    conj = "or" if mark == self.OR else "but"
                elif mark is not None:
                    advs.append(self.adverbial(group, mark, forms))
                elif group:
                    advs.append(self.np(group, group, forms, case=True))
            if tok is None:
                if advs:
                    carried.extend(advs)
                continue
            gs = [a["gloss"] for a in tok.affixes]
            if tok.base["form"] in self.MODALS and carried:
                _, cues = self.predicate(tok)
                modal = self.MODALS[tok.base["form"]]
                if "negation" in gs:
                    modal = {"can": "cannot", "want to": "do not want to",
                             "should": "should not", "may": "may not"}[modal]
                inner = carried.pop()
                parts.append(self.insert_modal(inner, modal) + cues)
                continue
            # An agentless clause drops the subject and keeps the object marker
            # (D65); English has only the passive for that.
            passive = obj is not None and subj is None and not carried
            self._last_root = tok.base["form"]
            body, cues = self.predicate(tok, passive=passive)
            std = next((a for a in advs if a.startswith("from ")), None)
            if std and tok.base["form"] in COPULA and body.startswith(("is ", "was ")):
                adj = body.split(" ", 1)[1]
                body = body.split(" ", 1)[0] + " " + comparative(adj) + " than " + std[5:]
                advs = [a for a in advs if a is not std]
            head = []
            if passive:
                head += [obj, body]
                obj = None
            else:
                if subj:
                    head.append(subj)
                elif carried:
                    head.append(carried.pop(0))
                head.append(body)
                if obj:
                    head.append(obj)
                    obj = None
            head.extend(advs)
            clause = " ".join(x for x in head if x)
            if is_q and "subordinator" not in gs:
                clause = self.question(clause, subj or (obj or ""), body, gs)
            if "subordinator" in gs:
                carried.append(clause)
                continue
            parts.append(clause + cues)
        if carried:
            parts = [c for c in carried] + parts
        joined = []
        for p in parts:
            if p.startswith("__IF__"):
                joined.append(("if " + p[6:]).rstrip(".") + ",")
            elif joined and joined[-1].endswith(","):
                joined[-1] = joined[-1] + " " + p
            elif joined and joined[-1].endswith((" or", " but")):
                joined[-1] = joined[-1] + " " + p
            else:
                joined.append(p)
        s = "; ".join(p for p in joined if p).strip()
        s = re.sub(r"\s+", " ", s).strip()
        if not s:
            return None, ["nothing realised"]
        padded = " " + s + " "
        for a, b in self.CONTRACT:
            padded = padded.replace(a, b)
        s = padded.strip()
        s = s[0].upper() + s[1:]
        return s + ("?" if is_q else "."), []


def norm(s):
    s = re.sub(r"[^a-z0-9' ]", " ", s.lower())
    return " ".join(s.split())


def content(s):
    stop = {"the", "a", "an", "is", "are", "was", "were", "it", "that", "this", "i", "you",
            "to", "of", "in", "on", "at", "and", "did", "do", "does", "will"}
    return [w for w in norm(s).split() if w not in stop]


def ambiguous(argv):
    """Every place the corpus leaves a split undecidable and this had to choose.

    That list is the point of the tool: an algorithm standing on an ambiguity is
    standing where the corpus does not determine the sentence, and a model would
    have guessed past it plausibly.
    """
    r = Realizer()
    rows = [json.loads(l) for l in (ROOT / "corpus/corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    hits = []
    for x in rows:
        t = x["st"].split()
        parsed = parse_sentence(x["st"], r.lx)
        pred = {i for i, tk in enumerate(parsed.tokens) if tk.affixes}
        for i in range(len(t) - 2):
            if i in pred or i + 1 in pred:
                continue
            if (t[i] in r.ROOTS and t[i + 1] in r.ROOTS and t[i + 2] in r.markers
                    and t[i + 2] != r.Q and (i == 0 or t[i - 1] in r.markers or i - 1 in pred)):
                hits.append((x["id"], x["split"], " ".join(t[i:i + 3]), x["en"]))
                break
    print(f"undecidable [root][root][marker] splits: {len(hits)}/{len(rows)} sentences "
          f"({sum(1 for h in hits if h[1] == 'held')} held)")
    for h in hits:
        print(f"  {h[0]} {h[1]:5} {h[2]:14} | {h[3]}")
    return 0


def score(argv):
    r = Realizer()
    rows = [json.loads(l) for l in (ROOT / "corpus/corpus.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    if "--held" in argv:
        rows = [x for x in rows if x["split"] == "held"]
    show = int(argv[argv.index("--show") + 1]) if "--show" in argv else 0
    exact = near = overlap_ok = failed = 0
    misses = []
    for x in rows:
        out, errs = r.realize(x["st"])
        if out is None:
            failed += 1
            misses.append((x["id"], x["en"], "PARSE/REALIZE FAILED"))
            continue
        if norm(out) == norm(x["en"]):
            exact += 1
            continue
        g, o = content(x["en"]), content(out)
        if g and len(set(g) & set(o)) / len(set(g)) >= 0.8:
            near += 1
        misses.append((x["id"], x["en"], out))
    n = len(rows)
    print(f"realize.py: {n} sentences")
    print(f"  exact (normalised)      : {exact}/{n} = {100*exact/n:.1f}%")
    print(f"  content words >=80% same : {near}/{n} = {100*near/n:.1f}%  (cumulative "
          f"{100*(exact+near)/n:.1f}%)")
    print(f"  produced nothing         : {failed}/{n}")
    for m in misses[:show]:
        print(f"\n  {m[0]}\n    gold {m[1]}\n    got  {m[2]}")
    return 0


def main():
    if "--ambiguous" in sys.argv:
        return ambiguous(sys.argv)
    if "--score" in sys.argv:
        return score(sys.argv)
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    out, errs = Realizer().realize(sys.argv[1])
    for e in errs:
        print("  problem:", e, file=sys.stderr)
    if out:
        print(out)
    return 0 if out else 1


if __name__ == "__main__":
    sys.exit(main())
