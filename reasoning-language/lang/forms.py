"""Form layer: Hangul shapes for every word class, generated deterministically.

Shapes (a word is a run of Hangul blocks between spaces):
  particle : exactly 1 open block  (consonant + vowel)
  handle   : exactly 1 closed block (consonant + vowel + final)
  root     : open block + closed block               e.g. CV CVC
  derived  : root + one or more suffix blocks (closed blocks whose initial is the empty consonant)
  loan     : 2 or more open blocks (spelling cipher of an English word)
Latin letters and digits never appear outside « » except digits as numbers and labels.
"""
import random, json, os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
INI = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
VOW = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
FIN = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
       'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def blk(i, v, f=''):
    return chr(0xAC00 + (INI.index(i) * 21 + VOW.index(v)) * 28 + FIN.index(f))


def parts(ch):
    n = ord(ch) - 0xAC00
    if not 0 <= n < 11172:
        return None
    return INI[n // 588], VOW[n // 28 % 21], FIN[n % 28]


def is_open(ch):
    p = parts(ch)
    return p is not None and p[2] == ''


def is_closed(ch):
    p = parts(ch)
    return p is not None and p[2] != ''


# ---------------------------------------------------------------- particles
# class -> (consonants used, particle names in fixed order)
PART_VOWELS = 'ㅏㅐㅑㅓㅔㅕㅗㅛㅜㅠㅡㅣ'
CLASSES = [
    ('opener', 'ㄱㄲ', 'GIVEN TOLD DERIVED RECALLED ASSUMED CLAIM STORY RULE ASK REQUEST PROPOSE PLAN DEFINE SOCIAL HEAD'),
    ('relation', 'ㄷㄸ', 'CONTRAST CONCEDE RESULT EVIDENCE EXPLAIN ADD SEQUENCE EXAMPLE DETAIL RESTATE BACKGROUND ASIDE UNDER ANSWER REBUT RETRACT'),
    ('strength', 'ㅂ', 'CERTAIN LIKELY POSSIBLE'),
    ('attitude', 'ㅃ', 'SURPRISE EMPHASIS POLITE REGRET GLAD ANNOYED JEST IRONY FRANK HOPE FEAR META'),
    ('time', 'ㅎ', 'NOT PAST FUTURE NOW UNREAL NEAR FAR'),
    ('modal', 'ㅋ', 'MUST SHOULD MAY CAN WANT TRY'),
    ('aspect', 'ㅈㅉ', 'ONGOING DONE HABIT BEGIN STOP STILL AGAIN ALREADY FINALLY OFTEN RARE SOMETIMES ALWAYS NEVER TIMES'),
    ('degree', 'ㅌ', 'VERY SLIGHT FULL BARELY ALMOST ENOUGH TOO MORE LESS MOST LEAST EQUAL'),
    ('focus', 'ㅍ', 'ONLY ALSO EVEN INSTEAD MAINLY FOCUS TOPIC'),
    ('value', 'ㅍ', 'YES NO EMPTY'),
    ('role', 'ㅅㅆ', 'AGENT THEME TO FROM AT WHEN WITH CAUSE FOR THAN ABOUT AS ALONG SPAN EXCEPT DESPITE VIA PER SWAP'),
    ('linker', 'ㄹ', 'KIND OF REL NOTE HAVING SUCHAS'),
    ('conj', 'ㄹ', 'AND OR XOR ANDC ORC BUT'),
    ('struct', 'ㅊ', 'NAMED BY CALL NAME BE IF EACH IN WHILE RETURN STEP UPTO'),
    ('quant', 'ㅁㄴ', 'ALL MAJOR MANY SEVERAL SOME FEW NONE ANY GENERIC WHOLE THAT THIS OTHER SAME SPECIFIC ORD'),
    ('nummod', 'ㄴ', 'AROUND EXACT ATLEAST ATMOST ABOVE BELOW'),
    ('head', 'ㅇ', 'ME YOU US SELF MUTUAL WHAT FIRST SECOND THIRD FOURTH WE'),
    ('opener', 'ㄲ', 'IMPORT CODE CONSIDER'),
    # tone words added later: they take the unused blocks of the strength and modal rows, so no earlier form moves
    ('attitude', 'ㅂㅋ', 'SERIOUS WARM SAD GRATEFUL RHETORICAL HINT WARNING RELUCTANT PROUD CURIOUS EXCITED RESIGNED DISGUST EMBARRASSED COMFORT'),
]

# Code keywords have a shape of their own: an open block whose vowel is one of the seven "w" vowels below.
# Nothing else in the language uses these vowels, so a code keyword can be told from every other word at sight.
CODE_VOWELS = 'ㅘㅝㅚㅟㅢㅙㅞ'
CODE_ROWS = [('ㅎ', 'ㅘㅚㅢㅟㅝ', 'DEFINE BE RETURN IMPORT CODE'),   # naming and structure
             ('ㄷ', 'ㅚㅟㅘㅝ', 'IF EACH IN WHILE'),                # control
             ('ㅇ', 'ㅘㅝㅚㅟ', 'FIRST SECOND THIRD FOURTH')]       # argument slots
CODE_FORMS = {n: blk(c, v) for c, vs, names in CODE_ROWS for n, v in zip(names.split(), vs)}


def particle_table():
    """name -> (class, form). Deterministic: consonant fixed by class, vowels dealt in order."""
    used = {}
    out = {}
    for cls, cons, names in CLASSES:
        names = names.split()
        slots = [blk(c, v) for c in cons for v in PART_VOWELS]
        slots = [s for s in slots if s not in used]
        assert len(slots) >= len(names), cls
        for n, s in zip(names, slots):
            if n in CODE_FORMS: s = CODE_FORMS[n]
            used[s] = n
            out[n] = (cls, s)
    return out


# ---------------------------------------------------------------- roots
ROOT_I1 = INI
ROOT_V1 = 'ㅏㅓㅗㅜㅡㅣㅐㅔ'
ROOT_I2 = 'ㄱㄴㄷㄹㅁㅂㅅㅈㅊㅋㅌㅍㅎ'      # never the empty consonant: that marks a suffix
ROOT_V2 = 'ㅏㅓㅗㅜㅡㅣ'
ROOT_F = 'ㄱㄴㄹㅁㅂㅅㅇ'
SUFFIXES = ['opp', 'doer', 'made', 'tool', 'place', 'ness', 'group', 'able']
SUFFIX_FORMS = dict(zip(SUFFIXES, [blk('ㅇ', v, f) for v, f in
                                   [('ㅏ', 'ㄴ'), ('ㅣ', 'ㄹ'), ('ㅓ', 'ㅁ'), ('ㅗ', 'ㅇ'), ('ㅜ', 'ㄱ'), ('ㅡ', 'ㅁ'), ('ㅔ', 'ㅅ'), ('ㅐ', 'ㅂ')]]))


def root_forms(n, seed=11):
    """n distinct root forms; any two differ in at least 2 of their 5 parts."""
    r = random.Random(seed)
    chosen, seen1 = [], set()
    while len(chosen) < n:
        t = (r.choice(ROOT_I1), r.choice(ROOT_V1), r.choice(ROOT_I2), r.choice(ROOT_V2), r.choice(ROOT_F))
        # all 5 one-part-wildcard keys must be new -> pairwise distance >= 2
        keys = [t[:k] + ('*',) + t[k + 1:] for k in range(5)]
        if any(k in seen1 for k in keys):
            continue
        seen1.update(keys)
        chosen.append(blk(t[0], t[1]) + blk(t[2], t[3], t[4]))
    return chosen


HANDLE_FORMS = [blk(i, v, f) for f in 'ㄱㄴㅁ' for v in 'ㅏㅗㅜㅣ' for i in 'ㄱㄴㄷㅁㅂㅅㅈㅎ']  # 96 suggested handles

# ---------------------------------------------------------------- loans (spelling cipher, fixed table)
_cons = list('bcdfghjklmnpqrstvz'); _vows = list('aeiouwyx')
_r = random.Random(7)
_ci = [c for c in INI if c != 'ㅇ']; _r.shuffle(_ci)
_vi = list('ㅏㅓㅗㅜㅡㅣㅐㅔㅑ'); _r.shuffle(_vi)
LC = dict(zip(_cons, _ci)); LV = dict(zip(_vows + [''], _vi))
LCi = {v: k for k, v in LC.items()}; LVi = {v: k for k, v in LV.items()}


# Beyond a-z: marks, digits, symbols, Greek, accents. They use vowels the letter table leaves free (ㅕ ㅠ ㅛ ㅒ ㅖ).
L_CAP = blk('ㅇ', 'ㅕ')      # the next letter is a capital
L_LOCK = blk('ㅇ', 'ㅠ')     # capitals on / off
L_PAD = blk('ㅇ', 'ㅛ')      # nothing: fills a word that would otherwise be one block
L_GREEK = blk('ㅇ', 'ㅒ')    # the next letter is Greek
L_DIGIT = {str(d): blk(c, 'ㅒ') for d, c in enumerate('ㄱㄴㄷㄹㅁㅂㅅㅈㅊㅋ')}
L_SYM = {ch: blk(c, 'ㅖ') for ch, c in zip("-'.,/+():*°%&_=#@!", 'ㅇㄱㄴㄷㄹㅁㅂㅅㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆ')}
_ACC = [('̈', 'umlaut'), ('́', 'acute'), ('̀', 'grave'), ('̂', 'circumflex'), ('̃', 'tilde'),
        ('̧', 'cedilla'), ('̊', 'ring'), ('̌', 'caron'), ('̸', 'stroke')]
L_ACC = {a: blk(c, 'ㅛ') for (a, _), c in zip(_ACC, 'ㄱㄴㄷㄹㅁㅂㅅㅈㅊ')}
ACC_NAMES = {a: n for a, n in _ACC}
GREEK = dict(zip('abgdezhqiklmncoprstufxyw', 'αβγδεζηθικλμνξοπρστυφχψω'))
GREEKi = {v: k for k, v in GREEK.items()}
_DIGi = {v: k for k, v in L_DIGIT.items()}; _SYMi = {v: k for k, v in L_SYM.items()}; _ACCi = {v: k for k, v in L_ACC.items()}
_STROKE = {'ø': 'o', 'Ø': 'O', 'ł': 'l', 'Ł': 'L', 'đ': 'd', 'Đ': 'D'}


def _units(w):
    """Word -> list of (kind, base letter, is capital, is Greek, accents) or ('x', block)."""
    import unicodedata
    out = []
    for ch in w:
        if ch in _STROKE: out.append(['l', _STROKE[ch].lower(), _STROKE[ch].isupper(), False, ['̸']]); continue
        if ch == 'ς': ch = 'σ'
        if ch.lower() in GREEKi: out.append(['l', GREEKi[ch.lower()], ch != ch.lower(), True, []]); continue
        d = unicodedata.normalize('NFD', ch)
        if d[0].lower() in LC or d[0].lower() in LV:
            if any(a not in L_ACC for a in d[1:]): raise ValueError('loan cannot carry this character: ' + ch)
            out.append(['l', d[0].lower(), d[0].isupper(), False, list(d[1:])]); continue
        if ch in L_DIGIT: out.append(['x', L_DIGIT[ch]]); continue
        if ch in L_SYM or ch in '‐‑–−': out.append(['x', L_SYM.get(ch, L_SYM['-'])]); continue
        raise ValueError('loan cannot carry this character: ' + ch)
    return out


def loan_enc(w):
    us = _units(w); out = []; k = 0; lock = False
    def caps_run(k):                       # how many letters from k on are capitals (digits and symbols do not break the run)
        n = 0; j = k
        while j < len(us) and (us[j][0] == 'x' or (us[j][2] and not us[j][3])):
            n += us[j][0] == 'l'; j += 1
        while j > k and us[j - 1][0] == 'x': j -= 1
        return n, j
    end = -1
    while k < len(us):
        u = us[k]
        if lock and k == end: out.append(L_LOCK); lock = False
        if u[0] == 'x': out.append(u[1]); k += 1; continue
        _, a, cap, greek, acc = u
        if not lock and cap and not greek:
            n, j = caps_run(k)
            if n >= 3 or (n == 2 and j == len(us)): out.append(L_LOCK); lock = True; end = j
        nxt = us[k + 1] if k + 1 < len(us) else None
        pair = (a in LC and not greek and not acc and nxt and nxt[0] == 'l' and nxt[1] in LV and not nxt[3]
                and (nxt[2] == cap if lock else not nxt[2]) and not (lock and k + 1 >= end))
        if greek: out.append(L_GREEK)
        if cap and not lock: out.append(L_CAP)
        if a in LC:
            out.append(blk(LC[a], LV[nxt[1]] if pair else LV['']))
        else:
            out.append(blk('ㅇ', LV[a]))
        out += [L_ACC[x] for x in acc]
        if pair:
            out += [L_ACC[x] for x in nxt[4]]; k += 2
        else:
            k += 1
    s = ''.join(out)
    if lock and end < len(us): s += L_LOCK
    if len(s) < 2: s = L_PAD + s
    return s


def loan_dec(s):
    import unicodedata
    o = []; cap = lock = greek = False
    for ch in s:
        if ch == L_CAP: cap = True; continue
        if ch == L_LOCK: lock = not lock; continue
        if ch == L_PAD: continue
        if ch == L_GREEK: greek = True; continue
        if ch in _DIGi: o.append(_DIGi[ch]); continue
        if ch in _SYMi: o.append(_SYMi[ch]); continue
        if ch in _ACCi:
            if not o: raise ValueError('accent with no letter: ' + ch)
            a = _ACCi[ch]
            if a == '̸': o[-1] = {v: k for k, v in _STROKE.items()}.get(o[-1], o[-1])
            else: o[-1] = unicodedata.normalize('NFC', o[-1] + a)
            continue
        i, v, f = parts(ch)
        if f or v not in LVi or (i != 'ㅇ' and i not in LCi):
            raise ValueError('not a loan block: ' + ch)
        letters = (LCi[i] if i != 'ㅇ' else '') + LVi[v]
        for n, c in enumerate(letters):
            if greek and n == 0: c = GREEK[c]
            if lock or (cap and n == 0): c = c.upper()
            o.append(c)
        cap = greek = False
    return ''.join(o)


def is_loan_block(ch):
    i, v, f = parts(ch)
    return not f and (v in LVi or v in 'ㅕㅠㅛㅒㅖ')


if __name__ == '__main__':
    pt = particle_table()
    print(len(pt), 'particles')
    for cls, cons, names in CLASSES:
        print(f'{cls:9s}', ' '.join(f'{n}={pt[n][1]}' for n in names.split()))
    print('suffixes', SUFFIX_FORMS)
    print('roots', root_forms(8))
    print(loan_enc('python'), loan_dec(loan_enc('kubernetes')))
