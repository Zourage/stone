#!/usr/bin/env python3
"""Shared parsing for the language: lexicon access, tokenisation, glossing.

Every sentence parses exactly one way, so this module is deterministic and
needs no model. `validate.py` and `translate.py` both use it, so the rules
live in one place.

Template (D29, D32, D33, D34): root, negation, tense, evidential, stance,
subordinator. Only the evidential is mandatory, and not in a question, where
the slot is empty and the answer supplies it (D33).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LATIN = re.compile(r"[A-Za-z]")

SLOT_NAMES = ["negation", "tense", "evidential", "stance", "subordinator"]
EVIDENTIAL_SLOT = 2

# Compact labels for the gloss line.
LABEL = {
    "negation": "NEG", "subordinator": "SUB",
    "tense: past": "PAST", "tense: future": "FUT",
    "evidential: direct": "DIR", "evidential: reported": "REP",
    "evidential: inferred": "INF", "evidential: general": "GEN",
    "stance: intend": "INTEND", "stance: predict": "PREDICT", "stance: propose": "PROPOSE",
    "stance: trust": "TRUST", "stance: risk": "RISK", "stance: assert": "ASSERT",
    "case: object": "OBJ", "case: location": "LOC", "case: possessor": "POSS",
    "question particle": "Q",
}


def slot_of(entry):
    """Which verb-ending slot an affix fills, or None if it is not an affix."""
    g = entry["gloss"]
    if g == "negation":
        return 0
    if g == "subordinator":
        return 4
    head = g.split(":")[0]
    return SLOT_NAMES.index(head) if head in SLOT_NAMES else None


def label(entry):
    g = entry["gloss"]
    if g in LABEL:
        return LABEL[g]
    if g.startswith("pronoun: "):
        return g[len("pronoun: "):].replace(" ", ".")
    if g.startswith("relational: "):
        return g[len("relational: "):]
    return g.split(",")[0].strip().replace(" ", ".")


class Lexicon:
    def __init__(self, entries=None):
        self.entries = entries if entries is not None else json.load(
            open(ROOT / "lexicon/lexicon.json", encoding="utf-8"))
        self.by_form = {e["form"]: e for e in self.entries}
        self.affixes = {e["form"]: slot_of(e) for e in self.entries if e.get("pos") == "affix"}
        self.bases = {e["form"]: e for e in self.entries
                      if e.get("pos") in ("root", "num") or e.get("gloss", "").startswith("pronoun")}
        self.question_particle = next(
            (e["form"] for e in self.entries if e["gloss"] == "question particle"), None)
        self.codepoints = {int(c, 16) for c in
                           json.load(open(ROOT / "spec/codepoints.json", encoding="utf-8"))["codepoints"]}

    def longest_base(self, token):
        """The longest prefix of `token` that is a root, numeral or pronoun."""
        for k in range(len(token), 0, -1):
            if token[:k] in self.bases:
                return token[:k]
        return None

    def search_english(self, query, limit=12):
        """Lexicon entries whose gloss or sense notes mention `query` as a word.

        The match is on whole words: looking up "fix" must not hit every entry
        whose note contains "affix", and looking up "if" must not hit "Fifteen".
        """
        q = query.strip().lower()
        if not q:
            return []
        word = re.compile(r"(?<!\w)" + re.escape(q) + r"(?!\w)")
        exact, partial = [], []
        for e in self.entries:
            terms = [t.strip().lower() for t in e["gloss"].split(",")]
            if q in terms:
                exact.append(e)
            elif word.search(e["gloss"].lower()) or word.search(e.get("sense_notes", "").lower()):
                partial.append(e)
        return (exact + partial)[:limit]


class Token:
    def __init__(self, surface):
        self.surface = surface
        self.base = None
        self.affixes = []
        self.errors = []

    @property
    def slots(self):
        return [slot_of(a) for a in self.affixes]

    @property
    def is_predicate(self):
        return bool(self.affixes)

    def gloss(self):
        if self.base is None:
            return f"?{self.surface}?"
        parts = [label(self.base)] + [label(a) for a in self.affixes]
        return "-".join(parts)


class Sentence:
    def __init__(self, text, tokens, errors, is_question):
        self.text, self.tokens, self.errors, self.is_question = text, tokens, errors, is_question

    @property
    def ok(self):
        return not self.errors

    def gloss(self):
        return " ".join(t.gloss() for t in self.tokens)


def check_script(s, lx):
    """Errors about characters: Latin letters, or codepoints outside the 74."""
    out = []
    if LATIN.search(s):
        out.append("Latin letters in a script field")
    for ch in s:
        if ch != " " and ord(ch) not in lx.codepoints:
            out.append(f"U+{ord(ch):04X} is not one of the 74 syllables")
    return out


def parse_token(surface, lx, is_question=False):
    t = Token(surface)
    if surface in lx.by_form and surface not in lx.bases:
        t.base = lx.by_form[surface]          # a bare function word
        return t
    base = lx.longest_base(surface)
    if base is None:
        if surface in lx.by_form:
            t.base = lx.by_form[surface]
            return t
        t.errors.append(f"token {surface!r} is not a word (no known root prefix)")
        return t
    t.base = lx.bases[base]
    last = -1
    for ch in surface[len(base):]:
        if ch not in lx.affixes:
            t.errors.append(f"{ch!r} in {surface!r} is not an affix")
            break
        sl = lx.affixes[ch]
        if sl <= last:
            t.errors.append(f"affixes out of template order in {surface!r}")
            break
        last = sl
        t.affixes.append(lx.by_form[ch])
    if t.affixes and EVIDENTIAL_SLOT not in t.slots and not is_question:
        t.errors.append(f"predicate {surface!r} has no evidential and the sentence is not a question")
    return t


def parse_sentence(text, lx):
    errors = list(check_script(text, lx))
    surfaces = text.split()
    is_question = bool(surfaces) and surfaces[-1] == lx.question_particle
    tokens = []
    for s in surfaces:
        t = parse_token(s, lx, is_question)
        tokens.append(t)
        errors.extend(t.errors)
    return Sentence(text, tokens, errors, is_question)
