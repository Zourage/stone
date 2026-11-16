# Brief: drafting the root list for a constructed language

You are drafting part of the ROOT LIST (basic vocabulary) of a constructed language. You only choose
MEANINGS and describe each in English. Word forms are generated later by a script; do not invent forms.

## How the language works (what you need to know)

- A root has no noun/verb/adjective class. The same root can be the predicate of a clause, the head of a
  phrase, or a modifier. `big THEME file` = the file is big. `fail THEME test` = the test fails.
  `error KIND network` = network error. A quality or act root used as a head names the quality or event
  itself (`big OF file` = the size of the file; `fail OF test` = the failure of the test).
- Grammar words are NOT roots. The language already has particles for: pronouns (I, you, we), this/that,
  question words, all quantifiers (all, many, some, few, none, any, other, same, each), numbers (digits),
  ordinals, and/or/but/not/if, tense and aspect (past, future, now, still, already, again, often, always,
  never, begin, stop, finish-as-aspect), modals (must, should, may, can), degree (very, slightly, fully,
  almost, enough, too, more, less, most, least, equal-as-degree), focus (only, also, even, instead),
  and roles (agent, theme, to, from, at-place, at-time, with/by means, because-of, for, than/like, about,
  as, together-with, for-duration, except, despite, through, per, in-exchange-for).
  Do not list roots that only duplicate these. (Roots such as `cause`, `time`, `place`, `reason`,
  `same`... ARE fine when they are content words one talks ABOUT; use judgement.)
- Regular suffixes build words from roots, so DO NOT list a root for something a suffix gives:
  - `.opp`   opposite pole, or the act that undoes: big.opp = small; tie.opp = untie; before.opp = after
  - `.doer`  the one who does it / is characterised by it: teach.doer = teacher; science.doer = scientist
  - `.made`  the product or the thing undergoing it: build.made = building; write.made = text; eat.made = food
  - `.tool`  the instrument made for it: cut.tool = knife; compute.tool = computer
  - `.place` the place where it is done or kept: cook.place = kitchen; book.place = library
  - `.ness`  the abstract state or neutral dimension: friend.ness = friendship; child.ness = childhood
  - `.group` a collection taken as one unit: tree.group = forest; word.group = vocabulary
  - `.able`  able to undergo it: read.able = readable; see.able = visible; break.able = fragile
- Compounds are free: `store KIND data` = database; `parent KIND female` = mother; `water KIND salt`.
  Do not list a root for something an obvious two-root compound says well.
- For antonym pairs list ONE pole as the root (the unmarked or "more" pole: big, long, hot, good, open,
  before, above, inside, give, buy, increase...) and put the other in the derived list with `.opp`.
- Anything rare, culture-specific or highly technical is left out; it will be borrowed as a loan word.

## What to write

Two tab-separated files (UTF-8, no header line, no quotes).

### File 1: roots   (columns separated by TAB)

    gloss  type  tr  noun  adj  rel  field  def

- `gloss`: ONE lowercase English word, letters only (a-z), unique, the commonest plain word for the
  meaning. This is the root's name and its English rendering as a predicate. For T roots it is the noun
  (dog), for A/E roots the base verb (run, fall), for Q roots the adjective (big), for R roots the plain
  word (before, inside, friend, part).
- `type`: exactly one of
    T = thing or substance or person or abstract entity (dog, water, idea, error). As predicate: "is a dog".
    Q = quality or state (big, hot, true, alive, ready). As predicate: "is big".
    A = act or state whose main participant CONTROLS or EXPERIENCES it (run, say, eat, know, see, want,
        give, arrive). Main participant is marked AGENT; what is acted on or perceived is THEME.
    E = event that HAPPENS TO its main participant, not controlled (fall, die, fail, break, grow, burn,
        melt, change, happen, exist). Main participant is THEME. Adding an AGENT means "causes it"
        (die AGENT x THEME y = x kills y; break AGENT x THEME y = x breaks y). So do NOT list separate
        roots for kill, raise, drop etc. when an E root plus an agent says it; put them in the derived
        file with the pseudo-suffix `+agent` if they are common English words (die +agent kill).
    R = relational: it needs a second thing to make sense (before, inside, above, near, between, friend,
        parent, part, cause, result, owner, member, kind, top, edge, middle, size-like nouns are NOT R:
        they are Q/T). The second thing is linked with REL: `before REL meeting`, `parent REL A`.
- `tr`: for A and E roots: 1 if it commonly takes a THEME object besides its main participant
  (eat, see, give, break-with-agent), else 0. For T, Q, R write 0.
- `noun`: the English noun to print when the root is used as a head, ONLY if it differs from gloss
  (fail -> failure; big -> size; know -> knowledge; hot -> heat; true -> truth). Else leave empty.
- `adj`: the English word to print when the root modifies a head with KIND, ONLY if it differs from
  gloss (fail -> failing; science -> scientific; wood -> wooden). Else leave empty.
- `rel`: for R roots only: the English phrase that goes before the second thing
  (before -> "before"; above -> "above"; friend -> "friend of"; part -> "part of"; cause -> "cause of").
- `field`: a short lowercase field name (body, animal, motion, reasoning, computing, ...).
- `def`: a short definition (max 12 words), needed whenever the gloss word has more than one sense in
  English; otherwise may be empty. Say which sense is meant ("right: correct" vs "right: direction").

### File 2: derived words   (TAB separated)

    base  suffix  english  def

One line for each COMMON English word that is covered by a root plus a suffix (or `+agent`), e.g.

    big	opp	small	
    teach	doer	teacher	
    die	+agent	kill	
    long	ness	length	

`base` must be a gloss from YOUR file 1. `english` is one lowercase word (or a two-word phrase).
Aim for 60-150 lines. These are hints for the writer and exact renderings for the translator script.

## Quality rules

- One root per meaning. No synonyms (pick big, not large; begin is a particle, so no start/begin root
  unless you mean something else). Different senses of one English word get different glosses
  (e.g. `right` for correct; the direction gets another gloss such as `rightside`).
- Prefer general meanings over narrow ones: `cut` covers slice/chop/carve; `container` covers
  box/vessel if you do not need both. But keep distinctions people use every day (cup vs pot is fine).
- Every gloss must be a single lowercase word a-z. No spaces, hyphens or digits.
- Stay inside the target count for your part.
- Before finishing, check: no duplicate glosses; every derived `base` exists in your file 1; every line
  has exactly the right number of TAB-separated columns (8 for roots, 4 for derived).

Report back with: number of roots, number of derived lines, and the 10 hardest decisions you made
(which meanings you merged or left out and why). Keep the report short.
