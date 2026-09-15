#!/usr/bin/env python3
"""Validate lexicon + corpus. Run before every commit. Exit 1 on any failure.

Implemented now (spec/codepoints.json exists, D28):
  - every lexicon form and corpus `st` string uses only the 74 codepoints
  - no duplicate forms, no duplicate glosses
  - form length 1-3 syllables (D37)
  - pos is one of the schema enum (D29, D33)
  - no Latin letters anywhere in `form` or `st` (CLAUDE.md rule 3)
  - no form of 2+ syllables is a Korean word (data/ko_frequency.json; D13, D55)
  - no multi-syllable form splits into a shorter root plus a valid run of
    affixes, which would make the word ambiguous with an inflected shorter one

Corpus checks (D11, D15, D25, D43):
  - every `st` token is a known word: a func/root/num word alone, or a root
    followed by affixes in template order (neg, tense, evid, stance, sub);
    the evidential is required unless the sentence ends in the question particle
  - coverage REPORT (not yet a failure while the corpus is small): words with
    <3 train sentences, features with <10, held share, and the share of
    sentences whose stone and English word counts are equal (relexification proxy)
  - ERROR: rules the corpus decided and then broke: a first-person intend
    predicate without the future marker, the predict stance on the direct
    evidential, and any marked evidential or stance whose English carries none
    of its cues (D84, D88, D91, D94)
  - REPORT: English words that name more than one predicate root, which leaves
    English -> stone undetermined (D90, D94)
  - ERROR: a held sentence whose `st` or `en` is verbatim in the train split,
    which would hand the acceptance test that item for free (D93)
  - ERROR: corpus/README.md's cue sentence or feature-tag list out of step with
    the code and the data it claims to be generated from (D101)
  - ERROR: an adverbial standing before the main-clause subject (D78). This was
    a count until D102, and the count read 0 while eleven lines were wrong
  - ERROR: an adverbial standing before the object rather than after it (D103)

--add FILE: FILE is a JSON list of entries (or one entry). Each is validated
against the schema and the current lexicon, then appended. Nothing is written
if any entry fails. Ids are assigned here (w0001, ...); `added` defaults to today.
"""
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stonelib import Lexicon, check_script as _check_script, parse_sentence, slot_of  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.load(open(ROOT / "lexicon/schema.json"))
POS = set(SCHEMA["properties"]["pos"]["enum"])
KO = json.load(open(ROOT / "data/ko_frequency.json", encoding="utf-8"))
_LX_FOR_SCRIPT = Lexicon()


def check_script(s, where, errors):
    for msg in _check_script(s, _LX_FOR_SCRIPT):
        errors.append(f"{where}: {msg}")


def ambiguous_split(entry, lex):
    """Return the shorter base if this form could be read as base + verb ending."""
    if entry.get("pos") == "affix" or len(entry["form"]) < 2:
        return None
    bases = {e["form"]: e for e in lex
             if e.get("pos") in ("root", "num") or e.get("gloss", "").startswith("pronoun")}
    affixes = {e["form"]: slot_of(e) for e in lex if e.get("pos") == "affix"}
    f = entry["form"]
    for k in range(1, len(f)):
        if f[:k] not in bases:
            continue
        rest = f[k:]
        if not all(ch in affixes for ch in rest):
            continue
        slots = [affixes[ch] for ch in rest]
        if all(a < b for a, b in zip(slots, slots[1:])):
            return f[:k]
    return None


def validate_entries(lex, errors):
    forms, glosses = {}, {}
    for e in lex:
        missing = [k for k in SCHEMA["required"] if k not in e]
        if missing:
            errors.append(f"{e.get('id')}: missing {missing}")
            continue
        check_script(e["form"], e["id"], errors)
        if not 1 <= len(e["form"]) <= 3:
            errors.append(f"{e['id']}: form is {len(e['form'])} syllables, must be 1-3")
        clash = ambiguous_split(e, lex)
        if clash:
            errors.append(f"{e['id']}: form {e['form']!r} reads as {clash} plus a verb ending; recoin")
        if len(e["form"]) >= 2 and e["form"] in KO:
            errors.append(f"{e['id']}: form {e['form']!r} is a Korean word (frequency {KO[e['form']]}); recoin")
        if e["pos"] not in POS:
            errors.append(f"{e['id']}: pos {e['pos']!r} not in {sorted(POS)}")
        if e["form"] in forms:
            errors.append(f"{e['id']}: duplicate form of {forms[e['form']]}")
        forms[e["form"]] = e["id"]
        g = e["gloss"].strip().lower()
        if g in glosses:
            errors.append(f"{e['id']}: duplicate gloss of {glosses[g]}")
        glosses[g] = e["id"]


def add(path):
    lex = json.load(open(ROOT / "lexicon/lexicon.json"))
    new = json.load(open(path))
    if isinstance(new, dict):
        new = [new]
    today = datetime.date.today().isoformat()
    n = max((int(e["id"][1:]) for e in lex), default=0)
    for e in new:
        n += 1
        e.setdefault("id", f"w{n:04d}")
        e.setdefault("added", today)
    errors = []
    validate_entries(lex + new, errors)
    for err in errors:
        print("FAIL", err)
    if errors:
        print(f"--add: {len(errors)} errors, nothing written")
        return 1
    with open(ROOT / "lexicon/lexicon.json", "w", encoding="utf-8") as f:
        json.dump(lex + new, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"--add: {len(new)} entries added, lexicon now {len(lex) + len(new)}")
    return 0


def _predicates(parsed, t):
    """Indices of the predicate tokens, questions included.

    A question's predicate carries no affix at all — the evidential slot is
    empty and the answer supplies it (D33) — so counting affix-bearing tokens
    misses it, and any walk that stops at the verb walks straight past it into
    the next clause. That blind spot is why the old version of the check below
    reported 0 while eleven lines were wrong (D102).
    """
    idx = {i for i, tk in enumerate(parsed.tokens) if tk.affixes}
    if parsed.is_question and len(t) >= 2:
        idx.add(len(t) - 2)                   # the token before the question particle
    return idx


def _fronted_adverbial(t, pred_idx, nums, cases, rel, marks, heads, pronouns, closers,
                       with_, interval):
    """True if an adverbial constituent stands before the main-clause subject.

    D78 puts the subject first and the adverbial after it. Three shapes carry an
    adverbial that can be fronted, and in all three the giveaway is the same: a
    BARE argument standing after the adverbial has closed is the main subject,
    and under D78 it should have come first. An argument carrying a case marker
    is an object, so it rightly follows, and reaching the predicate first means
    no subject was displaced.

    Every clause is walked, not only the first: D102 checked the sentence-initial
    phrase alone and so missed s0121 and s0698, where the second clause of a
    juxtaposed pair fronts "then" before its subject (D103).

    The first two shapes are D87's: a subordinate clause closed by the from word
    (because) or by time plus before/after/at (until, since, while), and an
    n-times phrase. The third is D102's, and it is the one the corpus was
    breaking in eleven places while this function reported 0 — a plain phrase
    closed by a case marker or a relational word, standing before the subject:
    "then it failed", "every day the machine stops", "before that, it was
    faulty". The check ran clean for two sessions because it was only ever
    asked about the two shapes D87 had already corrected.

    The possessor case is not a closer for the third shape: it binds to the noun
    after it (D33, D49) rather than ending a phrase. The personal pronouns are
    not determiners either — possession takes the possessor case — so `I` or
    `you` before a root is a subject followed by the next phrase, not one phrase.

    The with word IS a closer here, with one exemption. D102 excluded it
    outright, on the grounds that it coordinates two arguments into a subject
    (D98) and that where an adverbial with-phrase sits was still G33. G33 closed
    in D103, and the exclusion then hid a shape nothing else checked: a fronted
    comitative or manner phrase, `with you, I tested it`, which is a D78
    violation and is not the coordination, because the coordination is two
    juxtaposed pronouns and the walk above stops at the first of them. What does
    need exempting is the between-nominal, `run with run interval`, where the
    with word joins two points inside one subject (D69) — it is recognised by
    the interval root following it (D104).
    """
    sub, frm, time_, loc = marks

    def subject_after(k):
        while k < len(t) - 1:
            if k in pred_idx:           # hit the verb before any bare argument
                return False
            if t[k] in cases or t[k] in rel:
                k += 1
            elif t[k + 1] in cases or t[k + 1] in rel:
                k += 2                  # a case-marked argument: not the subject
            else:
                return True             # a bare argument: the displaced subject
        return False

    for i, tok in enumerate(t):
        if not tok.endswith(sub):
            continue
        if i + 1 < len(t) and t[i + 1] == frm:
            return subject_after(i + 2)
        if i + 2 < len(t) and t[i + 1] == time_ and t[i + 2] in loc:
            return subject_after(i + 3)
    if "메루" in t:                       # the repeat root, as an n-times phrase
        i = t.index("메루")
        start = i - 2 if i >= 2 and t[i - 2] == "야" else i - 1
        if start == 0 and (t[0] in nums or t[0] == "야"):
            return subject_after(i + 1)
    for start in [0] + [k + 1 for k in sorted(pred_idx)]:
        if start >= len(t) or start in pred_idx:
            continue                     # the clause opens with its verb: nothing to displace
        j = start                        # walk the opening phrase: determiners, then the head
        while (j + 1 < len(t) and (j + 1) not in pred_idx
               and t[j + 1] in heads and t[j] not in pronouns):
            j += 1
        if j + 1 < len(t) and t[j + 1] in closers:
            if t[j + 1] == with_ and interval in t[j + 2:]:
                continue                 # the between-nominal, inside one subject (D69)
            if subject_after(j + 2):
                return True
    return False


# The fixed English cues, per evidential and stance slot. The prose list lives in
# corpus/README.md and this must say the same thing (the D73 lesson); a marked
# slot whose English carries none of its cues leaves the sentence undetermined
# in the English -> stone direction, which is what the acceptance test measures.
SLOT_CUES = {
    "evidential: reported": ("i'm told", "i am told", "they say", "you told me", "i was told"),
    "evidential: inferred": ("must", "i gather", "it seems", "seems", "i think"),
    "evidential: general": ("how it is", "everyone knows", "as such", "known", "by definition",
                            "from the definition"),
    "stance: intend": ("i'll", "we'll", "i will", "we will", "that's the plan",
                       "that's my intention", "going to"),
    "stance: predict": ("i expect", "probably", "expect"),
    "stance: propose": ("just a proposal", "just a hypothesis", "i suspect", "perhaps"),
    "stance: trust": ("counting on", "you can count"),
    "stance: risk": ("might go wrong", "might break", "that might"),
    "stance: assert": ("i insist",),
}


def _clauses(sent, lx, pron_i, pron_you, cases, rel):
    """Walk a sentence, yielding (clause subject, predicate token, index, tokens).

    The nearest preceding bare pronoun is that clause's subject; a predicate
    ends its clause. Crude, but enough to tell an imperative from a first-person
    declarative, which is what the two pairing rules below turn on.
    """
    parsed = parse_sentence(sent["st"], lx)
    forms = sent["st"].split()
    subj = None
    for i, tk in enumerate(parsed.tokens):
        if not tk.affixes:
            nxt = forms[i + 1] if i + 1 < len(forms) else None
            if forms[i] in (pron_i, pron_you) and nxt not in cases and nxt not in rel:
                subj = forms[i]
            continue
        yield subj, tk, i, forms
        if not any(a["gloss"] == "subordinator" for a in tk.affixes):
            subj = None        # an embedded clause does not end the main one


def rule_errors(sents, lx):
    """Rules the corpus decided and then broke anyway. Exact, so these are errors.

    Each one cost a miss in acceptance test 4 and each is a rule, not a
    heuristic, so it is checked rather than counted (D94).
    """
    g = lambda gloss: next(e["form"] for e in lx.entries if e["gloss"] == gloss)  # noqa: E731
    pron_i, pron_you, if_w = g("pronoun: I"), g("pronoun: you"), g("if")
    cases = {e["form"] for e in lx.entries if e["gloss"].startswith("case")}
    rel = {e["form"] for e in lx.entries if e["gloss"].startswith("relational")}
    out = []
    for s in sents:
        parsed = parse_sentence(s["st"], lx)
        en = s["en"].lower()
        for subj, tk, i, forms in _clauses(s, lx, pron_i, pron_you, cases, rel):
            gs = [a["gloss"] for a in tk.affixes]
            if "subordinator" in gs:            # embedded clause or modal complement
                continue
            # D88: a first-person intend predicate carries the future marker (train 20:1)
            if ("stance: intend" in gs and subj == pron_i and "tense: future" not in gs):
                out.append(f"{s['id']}: first-person intend predicate without the future "
                           f"marker (D88)")
            # D88: the predict stance does not sit on the direct evidential (train 14:1)
            if "stance: predict" in gs and "evidential: direct" in gs:
                out.append(f"{s['id']}: predict stance on the direct evidential (D88)")
            # D84, D91: every marked evidential and stance carries its English cue
            if parsed.is_question:
                continue
            if "evidential: general" in gs and if_w in forms[i + 1:]:
                continue                        # irrealis protasis: the construction supplies it
            if "stance: intend" in gs and (subj == pron_you or forms[0] == pron_you):
                continue                        # the imperative is the intend cue
            marked = [x for x in gs if x in SLOT_CUES]
            if marked and not any(c in en for m in marked for c in SLOT_CUES[m]):
                out.append(f"{s['id']}: {' and '.join(marked)} with no English cue (D84, D91)")
    return out


def gloss_collisions(sents, lx):
    """English words that are the gloss of more than one root used as a predicate.

    Two roots that one English word can name leave the English -> stone
    direction undetermined: the say/tell root against the message root cost a
    miss in test 4, and the code and experiment senses of "variable" were the
    same defect waiting to happen (D90, D94).
    """
    used = {}
    for s in sents:
        roots = {tk.base["form"] for tk in parse_sentence(s["st"], lx).tokens
                 if tk.affixes and tk.base}
        for w in re.findall(r"[a-z']+", s["en"].lower()):
            used.setdefault(w, set()).update(roots)
    owners = {}
    for e in lx.entries:
        if e["pos"] != "root":
            continue
        for part in e["gloss"].split(","):
            owners.setdefault(part.strip().lower(), set()).add(e["form"])
    return sorted(w for w, roots in used.items() if len(owners.get(w, set()) & roots) > 1)


def readme_sync(sents):
    """corpus/README.md restates two things the data decides; check it still matches.

    D73 and D94 both say a list in the README is generated from the thing it
    describes "so the two cannot drift". Neither was: both were copied by hand
    once, and both did drift — the tag total went stale at the 1019-sentence
    merge, and the cue sentence was reworded in a way that silently broke the
    regex `translate.py` reads it with, so the model was prompted without the
    cue table. A claim of no-drift is worth what checks it, so this checks it.
    """
    txt = (ROOT / "corpus/README.md").read_text(encoding="utf-8")
    out = []

    m = re.search(r"Fixed cues[^:]*:(.*?)(?:\n|$)", txt)
    if not m:
        out.append("corpus/README.md: no 'Fixed cues' sentence; translate.py reads the cue "
                   "table out of it and would prompt the model without one")
    else:
        for slot, cues in SLOT_CUES.items():
            name = slot.split(": ")[1]
            mm = re.search(re.escape(name) + r' "([^"]+)"', m.group(1))
            if not mm:
                out.append(f"corpus/README.md: the cue sentence names no cues for {name}")
            elif tuple(c.strip() for c in mm.group(1).split("/")) != cues:
                out.append(f"corpus/README.md: the {name} cues differ from SLOT_CUES in "
                           f"validate.py; the corpus was written to one of them")

    listed = set()
    for line in txt.split("## Feature tags")[-1].splitlines():
        mm = re.match(r"- \*\*(.+?)\*\*: (.+)", line.strip())
        if mm:
            listed |= {x.strip() for x in mm.group(2).split(",")}
    actual = {f for s in sents for f in s["features"]}
    for f in sorted(actual - listed):
        out.append(f"corpus/README.md: feature tag {f!r} is used in the corpus but not listed")
    for f in sorted(listed - actual):
        out.append(f"corpus/README.md: feature tag {f!r} is listed but no longer used")
    m = re.search(r"Total: (\d+) distinct tags over (\d+) sentences", txt)
    if not m:
        out.append("corpus/README.md: no 'Total: N distinct tags over M sentences' line")
    elif (int(m.group(1)), int(m.group(2))) != (len(actual), len(sents)):
        out.append(f"corpus/README.md: says {m.group(1)} tags over {m.group(2)} sentences; "
                   f"the corpus has {len(actual)} over {len(sents)}")
    return out


def leak_report(sents):
    """Held sentences whose answer sits verbatim in the train split.

    The acceptance test measures whether a cold agent can produce a held
    sentence from the train split alone. A held line whose script is already in
    train hands over the English -> stone answer, and one whose English is
    already in train hands over the other direction; either way the item scores
    a free point and measures nothing. D75 removed the leak between the two
    directions of the test; this is the same leak between the two splits, and
    acceptance test 4 scored two such items before it was caught (D93).
    """
    train_st = {s["st"] for s in sents if s["split"] == "train"}
    train_en = {s["en"] for s in sents if s["split"] == "train"}
    leaked = [s["id"] for s in sents if s["split"] == "held"
              and (s["st"] in train_st or s["en"] in train_en)]
    return leaked


def adverbial_before_object(t, pred_idx, closers, pronouns, obj, with_, repeat):
    """Markers closing an adverbial phrase before the object marker of its own clause.

    D103 puts every adverbial after the object and immediately before the
    predicate: subject, n-times, object, adverbials, verb. Three things that
    stand before the object are not adverbials and are skipped. An n-times
    phrase counts the event and counting material precedes what it counts
    (D48, D97) — it is bare, so only its how-often variant, which puts the
    stretch in the location case (D69), needs the repeat root as its marker.
    The possessor case binds to the noun after it rather than closing a phrase.
    And the with word joining two juxtaposed pronouns coordinates them into a
    subject, so it is part of the subject rather than an adverbial before the
    object (D98).
    """
    out = []
    for i, tok in enumerate(t):
        if tok != obj:
            continue
        start = max([k + 1 for k in pred_idx if k < i - 1] + [0])
        if any(t[k] == repeat and t[k + 1] != obj for k in range(start, i)):
            continue                     # an n-times phrase, not the loop root as the object
        for k in range(start, i):
            if t[k] not in closers:
                continue
            if t[k] == with_ and k >= 2 and t[k - 1] in pronouns and t[k - 2] in pronouns:
                continue
            out.append(t[k])
    return out


def object_order_errors(sents, lx):
    """Sentences putting an adverbial before the object instead of after it (D103)."""
    g = lambda gloss: next(e["form"] for e in lx.entries if e["gloss"] == gloss)  # noqa: E731
    cases = {e["form"] for e in lx.entries if e["gloss"].startswith("case")}
    rel = {e["form"] for e in lx.entries if e["gloss"].startswith("relational")}
    pronouns = {e["form"] for e in lx.entries if e["gloss"].startswith("pronoun")}
    obj, poss, with_ = g("case: object"), g("case: possessor"), g("relational: with")
    closers = (cases | rel) - {obj, poss}
    out = []
    for s in sents:
        parsed = parse_sentence(s["st"], lx)
        t = s["st"].split()
        found = adverbial_before_object(t, _predicates(parsed, t), closers, pronouns,
                                        obj, with_, "메루")
        if found:
            out.append(f"{s['id']}: an adverbial ({' '.join(found)}) stands before the object; "
                       f"every adverbial but the n-times phrase follows it (D103)")
    return out


def fronted_errors(sents, lx):
    """Sentences that put an adverbial before the main-clause subject (D78).

    A count, which is what this was, gets read as coverage: D87 and D101 both
    reported 0 while eleven lines were wrong, because the detector only knew the
    shapes D87 had corrected. It is a decided rule the corpus has now broken
    twice, so by D94's standard it is an error rather than a number (D102).
    """
    g = lambda gloss: next(e["form"] for e in lx.entries if e["gloss"] == gloss)  # noqa: E731
    nums = {e["form"] for e in lx.entries if e["pos"] == "num"}
    cases = {e["form"] for e in lx.entries if e["gloss"].startswith("case")}
    rel = {e["form"] for e in lx.entries if e["gloss"].startswith("relational")}
    sub = g("subordinator")
    marks = (sub, g("relational: from"), g("time"),
             {g("case: location"), g("relational: before"), g("relational: after")})
    heads = {e["form"] for e in lx.entries if e.get("pos") in ("root", "num")}
    pronouns = {g("pronoun: I"), g("pronoun: you")}
    closers = (cases | rel) - {g("case: possessor")}
    with_, interval = g("relational: with"), g("interval, gap between")
    out = []
    for s in sents:
        parsed = parse_sentence(s["st"], lx)
        t = s["st"].split()
        if _fronted_adverbial(t, _predicates(parsed, t), nums, cases, rel, marks,
                              heads, pronouns, closers, with_, interval):
            out.append(f"{s['id']}: an adverbial stands before the main-clause subject; "
                       f"the subject comes first (D78, D102)")
    return out


def check_corpus(lex, errors):
    """Parse every corpus sentence with stonelib and report coverage."""
    lx = Lexicon(lex)
    corpus_path = ROOT / "corpus/corpus.jsonl"
    if not corpus_path.exists():
        return 0
    sents = [json.loads(l) for l in corpus_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    word_count = {e["id"]: 0 for e in lex}
    feat_count = {}
    same_len = 0
    for s in sents:
        parsed = parse_sentence(s["st"], lx)
        for msg in parsed.errors:
            errors.append(f"{s['id']}: {msg}")
        if s["split"] == "train":
            seen = {e["id"] for t in parsed.tokens
                    for e in ([t.base] if t.base else []) + t.affixes}
            for wid in seen:                      # distinct sentences, not occurrences (D11)
                word_count[wid] = word_count.get(wid, 0) + 1
            for f in s["features"]:
                feat_count[f] = feat_count.get(f, 0) + 1
        if len(s["en"].replace(".", " ").replace(",", " ").split()) == len(s["st"].split()):
            same_len += 1
    for msg in fronted_errors(sents, lx):
        errors.append(msg)
    for msg in object_order_errors(sents, lx):
        errors.append(msg)
    for msg in rule_errors(sents, lx):
        errors.append(msg)
    collisions = gloss_collisions(sents, lx)
    errors.extend(readme_sync(sents))
    for sid in leak_report(sents):
        errors.append(f"{sid}: held sentence whose script or English is verbatim in the train "
                      f"split, so the acceptance test would score it for free (D93)")
    n = len(sents)
    if n:
        thin = [w for w, c in word_count.items() if c < 3]
        weak = [f for f, c in feat_count.items() if c < 10]
        held = sum(1 for s in sents if s["split"] == "held")
        print(f"coverage: {len(thin)} words under 3 train sentences, {len(weak)} features under 10, "
              f"held {held}/{n}, same-length-as-English {same_len}/{n}")
        print(f"gloss collisions: {len(collisions)} English words naming more than one "
              f"predicate root ({', '.join(collisions) or 'none'}) (D94)")
    return n


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--add":
        return add(sys.argv[2])
    errors = []
    lex = json.load(open(ROOT / "lexicon/lexicon.json"))
    validate_entries(lex, errors)
    n_corpus = check_corpus(lex, errors)
    for err in errors:
        print("FAIL", err)
    print(f"validate.py: {len(lex)} lexicon entries, {n_corpus} corpus lines, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
