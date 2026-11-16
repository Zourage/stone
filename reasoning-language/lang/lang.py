"""Tokenizer, parser and checker for the language (grammar v0.4).

Two spellings of the same token stream:
  native : Hangul forms (what a model writes)
  gloss  : CAPITAL particle names, lowercase root glosses, capital-letter handles, ~loan, name«X»
Both are turned into the same tokens, so one parser serves both.
"""
import re, json, os
import forms as F

HERE = os.path.dirname(os.path.abspath(__file__))
PT = F.particle_table()                      # NAME -> (class, form)
FORM2P = {f: n for n, (c, f) in PT.items()}
CLS = {n: c for n, (c, f) in PT.items()}
SUF2NAME = {v: k for k, v in F.SUFFIX_FORMS.items()}


def load_lexicon(path=None):
    path = path or os.path.join(HERE, 'lexicon.json')
    if not os.path.exists(path):
        return {'roots': {}, 'derived': {}, 'spares': []}
    return json.load(open(path, encoding='utf-8'))


LEX = load_lexicon()
FORM2ROOT = {e['form']: g for g, e in LEX['roots'].items()}


class LangError(Exception):
    pass


# ------------------------------------------------------------------ tokens
def tok(t, v, **kw):
    d = {'t': t, 'v': v}
    d.update(kw)
    return d


PUNCT = '{}().'
_split = re.compile(r'«[^»]*»|[{}()]|[^\s{}()«]+')


def _raw(text):
    out = []
    for m in _split.finditer(text):
        s = m.group(0)
        out.append((s, m.start()))
    return out


def tokens_native(text, lex=None):
    lex = lex or LEX
    f2r = {e['form']: g for g, e in lex['roots'].items()}
    spares = set(lex.get('spares', []))
    out, errs = [], []
    for s, pos in _raw(text):
        if s.startswith('«'):
            out.append(tok('N', s[1:-1])); continue
        if s in '{}()':
            out.append(tok(s, s)); continue
        if s == '.':
            out.append(tok('.', '.')); continue
        if re.fullmatch(r'\d+:', s):
            out.append(tok('LABEL', s[:-1])); continue
        if re.fullmatch(r'-?\d+(\.\d+)?', s):
            out.append(tok('D', s)); continue
        if s.endswith('.') and len(s) > 1:      # full stop glued to a word
            errs.append(f'put a space before the full stop: {s}')
            s = s[:-1]
            more = tokens_native(s, lex)
            out += more[0]; errs += more[1]; out.append(tok('.', '.')); continue
        ps = [F.parts(ch) for ch in s]
        if any(p is None for p in ps):
            errs.append(f'not a word of the language (Latin letters need « »): {s}')
            out.append(tok('BAD', s)); continue
        opens = [p[2] == '' for p in ps]
        if len(s) == 1 and opens[0]:
            if s in FORM2P:
                out.append(tok('P', FORM2P[s]))
            else:
                errs.append(f'unknown particle: {s}'); out.append(tok('BAD', s))
        elif len(s) == 1:
            out.append(tok('H', s))
        elif all(opens):
            try:
                out.append(tok('L', F.loan_dec(s), form=s))
            except ValueError:
                errs.append(f'not a valid loan spelling: {s}'); out.append(tok('BAD', s))
        elif opens[0] and not opens[1]:
            base, rest = s[:2], s[2:]
            sufs = []
            ok = True
            for ch in rest:
                if ch in SUF2NAME:
                    sufs.append(SUF2NAME[ch])
                else:
                    ok = False
            if not ok:
                errs.append(f'bad word shape (after a root only suffix blocks may follow): {s}')
                out.append(tok('BAD', s)); continue
            if base in f2r:
                out.append(tok('R', f2r[base], suf=sufs, form=s))
            elif base in spares:
                out.append(tok('R', 'spare:' + base, suf=sufs, form=s, spare=True))
            else:
                errs.append(f'unknown root (not in the word list, not a spare): {s}')
                out.append(tok('R', '?' + base, suf=sufs, form=s, unknown=True))
        else:
            errs.append(f'bad word shape: {s}'); out.append(tok('BAD', s))
    return out, errs


def tokens_gloss(text, lex=None):
    lex = lex or LEX
    out, errs = [], []
    raw = _raw(text)
    i = 0
    while i < len(raw):
        s, pos = raw[i]; i += 1
        if s.startswith('«'):
            out.append(tok('N', s[1:-1])); continue
        if s in '{}()':
            out.append(tok(s, s)); continue
        if s == '.':
            out.append(tok('.', '.')); continue
        if s == 'name' and i < len(raw) and raw[i][0].startswith('«') and raw[i][1] == pos + 4:
            nm = raw[i][0][1:-1]; i += 1
            out.append(tok('P', 'NAME'))
            if re.fullmatch(r'[A-Za-z]+', nm):
                out.append(tok('L', nm.lower()))
            else:
                out.append(tok('N', nm))
            continue
        if re.fullmatch(r'\d+:', s):
            out.append(tok('LABEL', s[:-1])); continue
        if re.fullmatch(r'-?\d+(\.\d+)?', s):
            out.append(tok('D', s)); continue
        if s.endswith('.') and len(s) > 1 and not re.fullmatch(r'[a-z]+(\.[a-z]+)+', s):
            raw.insert(i, ('.', pos)); raw.insert(i, (s[:-1], pos)); continue
        if s in PT:
            out.append(tok('P', s)); continue
        if re.fullmatch(r'SPARE\d+', s):
            f = lex['spares'][int(s[5:]) - 1]
            out.append(tok('R', 'spare:' + f, suf=[], form=f, spare=True)); continue
        if re.fullmatch(r'[A-Z]\d?', s):
            out.append(tok('H', s)); continue
        if s.startswith('~') and len(s) > 1:
            try: F.loan_enc(s[1:]); out.append(tok('L', s[1:]))
            except ValueError as e: errs.append(str(e)); out.append(tok('BAD', s))
            continue
        m = re.fullmatch(r'([a-z]+)((\.[a-z]+)*)', s)
        if m:
            sufs = [x for x in m.group(2).split('.') if x]
            bad = [x for x in sufs if x not in F.SUFFIXES]
            if bad:
                errs.append(f'unknown suffix in {s}')
            g = m.group(1)
            if lex['roots'] and g not in lex['roots']:
                errs.append(f'unknown root: {g}')
                out.append(tok('R', g, suf=sufs, unknown=True))
            else:
                out.append(tok('R', g, suf=sufs))
            continue
        errs.append(f'unreadable token: {s}'); out.append(tok('BAD', s))
    return out, errs


def to_native(toks, lex=None, hmap=None):
    """tokens -> native text. Handles get suggested blocks in order of appearance."""
    lex = lex or LEX
    hmap = {} if hmap is None else hmap
    out = []
    for t in toks:
        k, v = t['t'], t['v']
        if k == 'P': out.append(PT[v][1])
        elif k == 'R':
            if t.get('spare'): base = v[6:]
            elif v in lex['roots']: base = lex['roots'][v]['form']
            else: raise LangError('no form for root ' + v)
            out.append(base + ''.join(F.SUFFIX_FORMS[s] for s in t.get('suf', [])))
        elif k == 'H':
            if F.parts(v[0]) is not None: out.append(v)
            else:
                if v not in hmap: hmap[v] = F.HANDLE_FORMS[len(hmap)]
                out.append(hmap[v])
        elif k == 'L': out.append(F.loan_enc(v))
        elif k == 'N': out.append('«' + v + '»')
        elif k == 'LABEL': out.append(v + ':')
        else: out.append(v)
    return _join(out)


def _join(words):
    txt, depth = '', 0
    for w in words:
        if w == '{': depth += 1
        elif w == '}': depth -= 1
        txt += w + ('\n' if (w == '.' and depth == 0) else ' ')
    return txt.strip()


def to_gloss(toks):
    hmap, out = {}, []
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    for t in toks:
        k, v = t['t'], t['v']
        if k == 'R' and t.get('spare'): out.append('SPARE' + str(LEX['spares'].index(v[6:]) + 1))
        elif k == 'R': out.append(v + ''.join('.' + s for s in t.get('suf', [])))
        elif k == 'H':
            if F.parts(v[0]) is None: out.append(v)
            else:
                if v not in hmap:
                    n = len(hmap); hmap[v] = letters[n % 24] + (str(n // 24) if n >= 24 else '')
                out.append(hmap[v])
        elif k == 'L': out.append('~' + v)
        elif k == 'N': out.append('«' + v + '»')
        elif k == 'LABEL': out.append(v + ':')
        else: out.append(v)
    return _join(out)


# ------------------------------------------------------------------ parser
PRE_CLASSES = {'time', 'aspect', 'modal', 'strength', 'focus', 'degree'}
HEAD_PARTS = {'ME', 'YOU', 'US', 'WE', 'SELF', 'MUTUAL', 'WHAT', 'THIS', 'THAT', 'NOW', 'YES', 'NO', 'EMPTY', 'STEP', 'NAME'}
SLOTS = ['FIRST', 'SECOND', 'THIRD', 'FOURTH']
PHRASE_CONJ = {'AND', 'OR', 'XOR'}
CLAUSE_CONJ = {'ANDC', 'ORC', 'BUT'}


class Parser:
    def __init__(self, toks):
        out = []; i = 0
        while i < len(toks):                                        # 3 UPTO 7 is one number token, the range 3–7
            t = toks[i]
            if t['t'] == 'D' and i + 2 < len(toks) and toks[i + 1]['t'] == 'P' and toks[i + 1]['v'] == 'UPTO' and toks[i + 2]['t'] == 'D' \
                    and not (out and out[-1]['t'] == 'P' and out[-1]['v'] == 'STEP'):
                out.append(tok('D', t['v'] + '–' + toks[i + 2]['v'])); i += 3; continue
            out.append(t); i += 1
        self.t = out; self.i = 0; self.warn = []; self.fronting = False

    # -- helpers
    def peek(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else tok('EOF', '')

    def isp(self, name=None, cls=None, k=0):
        t = self.peek(k)
        if t['t'] != 'P': return False
        if name is not None: return t['v'] == name if isinstance(name, str) else t['v'] in name
        if cls is not None: return CLS[t['v']] == cls if isinstance(cls, str) else CLS[t['v']] in cls
        return True

    def take(self):
        t = self.peek(); self.i += 1; return t

    def expect(self, kind, what=None):
        t = self.peek()
        if t['t'] != kind:
            self.fail(f'expected {what or kind}')
        return self.take()

    def expectp(self, name):
        if not self.isp(name): self.fail(f'expected {name}')
        return self.take()

    def fail(self, msg):
        ctx = ' '.join(_show(x) for x in self.t[max(0, self.i - 6):self.i]) + '  >>> ' + \
              ' '.join(_show(x) for x in self.t[self.i:self.i + 4])
        raise LangError(f'{msg}; at: {ctx}')

    # -- text
    def text(self):
        out = []
        while self.peek()['t'] != 'EOF':
            out.append(self.sentence())
        return out

    def sentence(self):
        s = self.statement(top=True)
        self.expect('.', 'full stop')
        return s

    def statement(self, top=False):
        s = {'k': 'sent'}
        if self.isp('BY'):
            self.take(); s['by'] = self.unit(simple=self.peek()['t'] == 'H')
            if self.isp('AROUND'): self.take(); s['para'] = True
        if self.peek()['t'] == 'LABEL': s['label'] = self.take()['v']
        early = []                                                  # relations written before the opener
        j = 0
        while self.isp(cls='relation', k=j):
            j += 1
            while self.peek(j)['t'] == 'D': j += 1
        if j and self.isp(cls='opener', k=j):
            while self.isp(cls='relation'):
                r = self.take()['v']; early.append((r, self.labels()))
        if self.isp(cls='opener'):
            s['head'] = self.header()
            s['head']['rels'] = early + s['head']['rels']
        elif top:
            self.fail('a sentence must start with an opener')
        s['body'] = self.body(s.get('head', {}).get('opener'))
        return s

    def header(self):
        h = {'opener': self.take()['v'], 'rels': [], 'att': []}
        op = h['opener']
        if op == 'DERIVED':
            h['basis'] = self.labels()
        if op == 'ASK' and self.isp(('YES', 'NO')):
            h['expect'] = self.take()['v']
        if op == 'TOLD' and self.peek()['t'] == 'H':
            h['source'] = self.take()['v']
        while True:
            if self.isp(cls='relation'):
                r = self.take()['v']; h['rels'].append((r, self.labels()))
            elif self.isp(cls='strength'):
                h['strength'] = self.take()['v']
                if self.peek()['t'] == 'N' or (self.peek()['t'] == 'D' and '.' in self.peek()['v']):
                    h['strength_n'] = self.take()['v']
            elif self.isp(cls='attitude'):
                h['att'].append((None, self.take()['v']))
            elif self.isp(cls='degree') and self.isp(cls='attitude', k=1):
                d = self.take()['v']; h['att'].append((d, self.take()['v']))
            elif self.isp('CALL'):
                self.take(); h['call'] = self.unit(simple=True)
            else:
                break
        return h

    def labels(self):
        out = []
        while self.peek()['t'] == 'D' and '.' not in self.peek()['v']:
            out.append(self.take()['v'])
        return out

    def block(self):
        self.expect('{', '{')
        stmts = [self.statement()]
        while self.peek()['t'] == '.':
            self.take()
            if self.peek()['t'] == '}': break
            stmts.append(self.statement())
        self.expect('}', '}')
        return {'k': 'block', 'stmts': stmts}

    def body(self, opener=None, nochain=False):
        if not nochain and self.isp(('IF', 'EACH', 'WHILE')):
            return self.chain()
        if self.isp('IF'):
            self.take(); c = self.block(); a = self.block()
            b = self.block() if self.peek()['t'] == '{' and True else None
            return {'k': 'if', 'cond': c, 'then': a, 'else': b, 'roles': self.roles()}
        if self.isp('EACH'):
            self.take(); h = self.expect('H', 'handle')['v']; self.expectp('IN')
            return {'k': 'each', 'var': h, 'in': self.phrase(), 'do': self.block()}
        if self.isp('WHILE'):
            self.take(); return {'k': 'while', 'cond': self.block(), 'do': self.block()}
        if self.isp('RETURN'):
            self.take(); return {'k': 'return', 'val': self.phrase()}
        if opener == 'DEFINE':
            term = self.phrase(stop_be=True)
            params = []
            while self.isp(SLOTS):
                self.take(); params.append(self.expect('H', 'handle')['v'])
            self.expectp('BE')
            return {'k': 'define', 'term': term, 'params': params, 'val': self.phrase()}
        if opener in ('IMPORT', 'CODE'):
            if self.peek()['t'] not in ('N', 'L'): self.fail(opener + ' must be followed by a name in « »')
            u = {'k': 'unit', 'pre': [], 'q': [], 'mods': [], 'roles': [], 'head': self.take()}
            if opener == 'IMPORT':
                if not self.isp('NAMED'): self.fail('IMPORT needs NAMED and a handle: the short name the library is used by')
                self.take(); u['named'] = self.expect('H', 'handle')['v']
            return {'k': 'frag', 'phrase': {'k': 'phrase', 'units': [u], 'ops': []}}
        if opener in ('SOCIAL', 'HEAD'):
            ph = self.phrase()
            if opener == 'HEAD' and self.peek()['t'] == 'D':      # "HEAD task 2": a trailing number is the heading's number
                ph['units'][-1].setdefault('mods', []); ph['num'] = self.take()['v']
                self.linkers(ph['units'][-1])
            if opener == 'HEAD' and self.isp('NAME'):
                ph['title'] = self.head(False)
            return {'k': 'frag', 'phrase': ph, 'extra': self.roles()}
        if self.peek()['t'] == 'N' and self.peek(1)['t'] in ('.', '}', 'EOF'):
            return {'k': 'frag', 'phrase': self.phrase()}
        if self.front_start() and not self.isp(cls='role'):
            return self.chain()
        if self.isp(cls='role'):
            save = self.i; self.fronting = True; rs = self.roles(); self.fronting = False
            if self.peek()['t'] in ('.', '}', 'EOF') or not self.starts_clause():
                return {'k': 'frag', 'roles': rs}
            self.i = save                                           # role phrases placed before the predicate
            return self.chain()
        if self.isp(('YES', 'NO')) and self.peek(1)['t'] in ('.', '}'):
            return {'k': 'frag', 'phrase': self.phrase()}
        if self.starts_clause() or self.scope_start():
            return self.chain()
        return {'k': 'frag', 'phrase': self.phrase()}

    def scope_start(self):
        """NOT, a modal, a strength word or a tone word followed (perhaps after more of them) by a block."""
        j = 0
        while self.isp('NOT', k=j) or self.isp(cls=('modal', 'strength', 'attitude'), k=j): j += 1
        return j > 0 and self.peek(j)['t'] == '{'

    def conjunct(self):
        if self.isp(('IF', 'EACH', 'WHILE')): return self.body(nochain=True)
        if self.scope_start():                                      # scope by nesting: the word covers exactly its block
            ops = []
            while self.peek()['t'] != '{': ops.append(self.take()['v'])
            return {'k': 'scoped', 'ops': ops, 'block': self.block()}
        fpre = []; front = []
        if self.front_start():
            while self.isp(cls='focus'): fpre.append((self.take()['v'], None))
            self.fronting = True; front = self.roles(); self.fronting = False
        c = self.clause()
        if front: c['roles'] = front + c['roles']; c['front'] = len(front); c['pre'] = fpre + c['pre']
        return c

    def chain(self):
        c = self.conjunct(); parts_ = [c]; ops = []
        while self.isp(CLAUSE_CONJ):
            op = self.take()['v']; rel = None
            if self.isp(cls='relation'): rel = self.take()['v']
            ops.append((op, rel)); parts_.append(self.conjunct())
        if ops: return {'k': 'cjoin', 'parts': parts_, 'ops': ops}
        return c

    def starts_clause(self):
        """Look past pre-predicate particles for a predicate."""
        j = 0
        while True:
            t = self.peek(j)
            if t['t'] == 'P':
                n = t['v']; c = CLS[n]
                if n in ('NOT', 'NEAR', 'FAR', 'TIMES', 'BE'):
                    if n == 'BE': return True
                    j += 1; continue
                if c in PRE_CLASSES or c in ('nummod',): j += 1; continue
                if c == 'quant' and self.isp('TIMES', k=j + 1): j += 1; continue
                if n == 'ORD' and self.peek(j + 1)['t'] == 'D' and self.isp('TIMES', k=j + 2): j += 1; continue
                if n == 'WHAT' and self.peek(j + 1)['t'] in ('R', 'L') or n == 'WHAT' and self.isp('TIMES', k=j + 1):
                    j += 1; continue
                if (c == 'role' or n in SLOTS) and j > 0 and self.isp(cls='degree', k=j - 1): return True
                return False
            if t['t'] == 'D':
                if self.isp('TIMES', k=j + 1) or self.isp(cls='degree', k=j + 1): j += 1; continue
                return False
            return t['t'] in ('R', 'L', '(')  # a predicate

    def clause(self):
        c = {'k': 'clause', 'pre': [], 'roles': []}
        while True:
            t = self.peek()
            if t['t'] == 'D' and self.isp('TIMES', k=1):
                n = self.take()['v']; self.take(); c['pre'].append(('TIMES', n)); continue
            if t['t'] == 'D' and self.isp(cls='degree', k=1):
                n = self.take()['v']; c['pre'].append(('FACTOR', n)); continue
            if t['t'] != 'P': break
            n = t['v']; cl = CLS[n]
            if n == 'ORD' and self.peek(1)['t'] == 'D' and self.isp('TIMES', k=2):
                self.take(); d = self.take()['v']; self.take(); c['pre'].append(('NTH', d)); continue
            if cl == 'nummod' and self.peek(1)['t'] == 'D' and self.isp('TIMES', k=2):
                m = self.take()['v']; d = self.take()['v']; self.take(); c['pre'].append(('TIMES', m + ' ' + d)); continue
            if (cl == 'quant' or n == 'WHAT') and self.isp('TIMES', k=1):
                q = self.take()['v']; self.take(); c['pre'].append(('TIMES', q)); continue
            if n == 'AROUND' or n == 'NOT' or cl in PRE_CLASSES:
                if n == 'NOW' and self.peek(1)['t'] not in ('R', 'L', '(', 'P'): break
                self.take(); c['pre'].append((n, None)); continue
            if n == 'WHAT' and self.peek(1)['t'] in ('R', 'L'):
                # WHAT in the degree position: "how big"
                self.take(); c['pre'].append(('WHAT', None)); continue
            break
        if c['pre'] and c['pre'][-1][0] in PT and CLS[c['pre'][-1][0]] == 'degree' and self.peek()['t'] not in ('R', 'L', '(', 'N') and not self.isp('BE'):
            c['pred'] = {'k': 'dpred', 'deg': c['pre'].pop()[0]}      # EQUAL / MORE / LESS alone as predicate
        else:
            c['pred'] = self.predicate()
        c['roles'] = self.roles()
        return c

    def predicate(self):
        t = self.peek()
        if self.isp('BE'):
            self.take(); return {'k': 'be'}
        if t['t'] == '(':
            self.take(); p = self.phrase(inpar=True); self.expect(')', ')')
            return {'k': 'ppred', 'phrase': p}
        if t['t'] in ('R', 'L', 'N'):
            self.take()
            u = {'k': 'unit', 'pre': [], 'q': [], 'head': t, 'mods': [], 'roles': []}
            self.linkers(u)
            return {'k': 'rpred', 'unit': u}
        self.fail('expected a predicate (a root, BE, or a phrase in round brackets)')

    def roles(self):
        out = []
        while self.isp(cls='role') or self.isp(SLOTS) or (self.isp(('ONLY', 'EVEN', 'ALSO')) and self.isp(cls='role', k=1)):
            foc = self.take()['v'] if self.isp(('ONLY', 'EVEN', 'ALSO')) else None
            r = self.take()['v']; sub = None
            if r == 'THAN' and self.isp(cls='role'):
                sub = self.take()['v']
            out.append({'role': r, 'sub': sub, 'phrase': self.phrase(), 'focus': foc})
        return out

    def phrase(self, inpar=False, stop_be=False):
        us = [self.unit(inpar=inpar)]; ops = []
        while self.isp(PHRASE_CONJ):
            ops.append(self.take()['v']); us.append(self.unit(inpar=inpar))
        if len(set(ops)) > 1:
            self.warn.append('AND, OR and XOR are mixed at one level; add brackets')
        return {'k': 'phrase', 'units': us, 'ops': ops}

    def head_start(self, k=0):
        t = self.peek(k)
        if t['t'] in ('R', 'L', 'N', '(', 'H'): return True
        return t['t'] == 'P' and (t['v'] in ('NAME',) or CLS[t['v']] in ('quant', 'nummod', 'degree'))

    def unit(self, inpar=False, simple=False):
        u = {'k': 'unit', 'pre': [], 'q': [], 'mods': [], 'roles': []}
        while self.isp(cls=('focus', 'attitude', 'strength')):
            u['pre'].append(self.take()['v'])
        if self.isp('NOT'): self.take(); u['neg'] = True
        # quantifier zone
        while True:
            t = self.peek()
            if t['t'] == 'P':
                n = t['v']; c = CLS[n]
                if n == 'ORD':
                    self.take(); a = self.ordarg()
                    if self.isp('UPTO'):
                        self.take(); u['q'].append(('ORDRANGE', (a, self.ordarg()))); continue
                    u['q'].append(('ORD', a)); continue
                if n in ('THIS', 'THAT'):
                    if self.head_start(1) and not self.isp(cls='nummod', k=1) or self.peek(1)['t'] == 'D':
                        self.take(); u['q'].append((n, None)); continue
                    break
                if n == 'WHAT':
                    if self.peek(1)['t'] in ('R', 'L') or self.isp(('MANY', 'FEW'), k=1):
                        self.take(); u['q'].append(('WHAT', None)); continue
                    break
                if c in ('quant', 'degree') or (c == 'nummod'):
                    self.take(); u['q'].append((n, None)); continue
                break
            if t['t'] == 'N' and self.peek(1)['t'] in ('R', 'L') and not any(q[0] == 'NUM' for q in u['q']) and not self.fronting and not re.search(r'[A-Za-z]{3,}', t['v']):
                u['q'].append(('NUM', self.take()['v'])); continue          # a symbolic count: «n» steps, «2^30» copies
            if t['t'] == 'H' and self.peek(1)['t'] in ('R', 'L') and not u['q'] and not self.fronting and (not simple or getattr(self, 'lk', False)):
                u['q'].append(('NUM', self.take())); continue          # a handle as a count: "n odd numbers"
            if t['t'] == 'D':
                nxt = self.peek(1)
                if self.isp('UPTO', k=1):
                    a = self.take()['v']; self.take(); b = self.take()['v']
                    if self.head_start():
                        u['q'].append(('NUM', a + '–' + b)); continue
                    u['head'] = tok('D', a + '–' + b); break
                if nxt['t'] in ('R', 'L', 'N', '(') or (nxt['t'] == 'P' and (CLS[nxt['v']] == 'degree' or nxt['v'] in ('SAME', 'OTHER', 'SPECIFIC'))):
                    u['q'].append(('NUM', self.take()['v'])); continue
                break
            break
        if 'head' not in u:
            if u['q'] and u['q'][-1][0] in PT and CLS[u['q'][-1][0]] == 'degree' and not self.head_start() \
                    and self.peek()['t'] not in ('{', 'D') and not (self.peek()['t'] == 'P' and (self.peek()['v'] in HEAD_PARTS or CLS[self.peek()['v']] == 'head') and self.peek()['v'] not in SLOTS):
                u['head'] = tok('P', u['q'].pop()[0])                 # a degree word used as a function name
            else:
                u['head'] = self.head(inpar)
        self.tag(u)
        if self.isp('NAMED'):
            self.take(); u['named'] = self.expect('H', 'handle')['v']
        if not simple:
            self.linkers(u)
            if inpar: u['roles'] = self.roles()
        return u

    def tag(self, u):
        """A number or « » straight after a root is that thing's number or name: section 1, year 1919, task «K01»."""
        h = u['head']
        if h.get('t') in ('R', 'L') and self.peek()['t'] in ('D', 'N') and not self.isp('TIMES', k=1):
            u['tag'] = self.take()['v']
        elif h.get('t') == 'R' and self.isp('CODE') and self.peek(1)['t'] == 'N':
            self.take(); u['tag'] = self.take()['v']                # a thing named by code text: function CODE «count_spikes»

    def front_start(self):
        """Role phrases (perhaps after focus words) standing before the predicate."""
        j = 0
        while self.isp(cls='focus', k=j): j += 1
        return self.isp(cls='role', k=j)

    def ordarg(self):
        t = self.peek()
        if t['t'] in ('D', 'N'): return self.take()['v']
        if t['t'] == 'H': return self.take()
        if t['t'] == '(':
            self.take(); p = self.phrase(inpar=True); self.expect(')', ')')
            return {'k': 'paren', 'phrase': p}
        self.fail('expected a number, a handle or a bracket after ORD')

    def linkers(self, u):
        while self.isp(cls='linker'):
            l = self.take()['v']; m = {'link': l}
            if self.isp('NOT'): self.take(); m['neg'] = True
            m['deg'] = []
            while self.isp(cls='degree') or self.isp('AROUND'):
                m['deg'].append(self.take()['v'])
            fpre = []
            while self.isp(cls='focus') and not self.isp(('THIS', 'THAT')): fpre.append(self.take()['v'])
            if self.isp(('THIS', 'THAT')) or self.isp(cls=('quant', 'nummod')) or \
                    (self.peek()['t'] == 'D' and self.peek(1)['t'] in ('R', 'L', 'N')) or \
                    (self.peek()['t'] in ('H', 'N') and self.peek(1)['t'] in ('R', 'L') and not self.fronting):
                self.lk = True; m['unit'] = self.unit(simple=True); self.lk = False
            else:
                m['unit'] = {'k': 'unit', 'pre': [], 'q': [], 'mods': [], 'roles': [], 'head': self.head(False)}
                self.tag(m['unit'])
            m['unit']['pre'] = fpre + m['unit']['pre']
            if True:
                if self.isp('NAMED'):
                    self.take(); m['unit']['named'] = self.expect('H', 'handle')['v']
            u['mods'].append(m)

    def head(self, inpar):
        t = self.peek()
        def short(x): return x['t'] == 'N' and len(x['v']) <= 2 and x['v'].isalnum()
        if t['t'] == 'L' or (short(t) and self.peek(1)['t'] in ('D', 'L') and not self.isp('TIMES', k=2)):
            # a term of several pieces: loans, digits, and one- or two-letter symbols: ~il 4, ~affinity ~maturation, ~hba 1 «c»
            ws = [self.take()['v']]
            while self.peek()['t'] == 'L' or short(self.peek()) or (self.peek()['t'] == 'D' and not self.isp('TIMES', k=1)):
                ws.append(self.take()['v'])
            return t if len(ws) == 1 else tok('L', ' '.join(ws))
        if t['t'] in ('R', 'H', 'N', 'D'):
            return self.take()
        if self.isp('CODE') and self.peek(1)['t'] == 'N':           # code text mentioned in prose
            self.take(); return dict(self.take(), code=True)
        if t['t'] == '{':
            return self.block()
        if t['t'] == '(':
            self.take(); p = self.phrase(inpar=True); self.expect(')', ')')
            return {'k': 'paren', 'phrase': p}
        if t['t'] == 'P':
            n = t['v']
            if n == 'NAME':
                self.take(); x = self.peek()
                if x['t'] in ('L', 'R', 'N'):
                    return {'k': 'name', 'parts': [self.take()]}
                if x['t'] == '(':
                    self.take(); ps = []
                    while self.peek()['t'] in ('L', 'R', 'N', 'D'): ps.append(self.take())
                    self.expect(')', ')'); return {'k': 'name', 'parts': ps}
                self.fail('NAME must be followed by a loan, a root or « »')
            if n == 'STEP':
                self.take(); a = self.expect('D', 'label')['v']; b = None
                if self.isp('UPTO'): self.take(); b = self.expect('D', 'label')['v']
                return {'k': 'step', 'a': a, 'b': b}
            if n in HEAD_PARTS or CLS[n] == 'head':
                return self.take()
        self.fail('expected a head (root, handle, loan, « », number, block or bracket)')


def _show(t):
    if t['t'] == 'R': return t['v']
    if t['t'] == 'N': return '«' + t['v'] + '»'
    if t['t'] == 'L': return '~' + t['v']
    if t['t'] == 'LABEL': return t['v'] + ':'
    return str(t['v'])


def split_sentences(toks):
    """Split a token list at top-level full stops, so one bad sentence does not sink the text."""
    out, cur, depth = [], [], 0
    for t in toks:
        cur.append(t)
        if t['t'] == '{': depth += 1
        elif t['t'] == '}': depth = max(0, depth - 1)
        elif t['t'] == '.' and depth == 0:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out


ELEMENTS = set("""H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo
Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn
Fr Ra Ac Th Pa U Np Pu Am Cm""".split())


def is_formula(s):
    """True for a chemical formula: element symbols, counts, brackets and charges only."""
    parts = re.findall(r'[A-Z][a-z]?|\d+|[()\[\]+\-·.=#]', s)
    return ''.join(parts) == s and all(p in ELEMENTS for p in parts if p[0].isalpha())


def parse(text, mode='native', lex=None):
    """-> dict(sentences=[ast|None], errors=[(sentence_no, msg)], tokens=[...])"""
    toks, errs = (tokens_native if mode == 'native' else tokens_gloss)(text, lex)
    res = {'sentences': [], 'errors': [(0, e) for e in errs], 'tokens': toks, 'chunks': []}
    defined = set()
    all_defined = {t['v'] for ch in split_sentences(toks) if any(x['t'] == 'P' and x['v'] == 'DEFINE' for x in ch[:4]) for t in ch if t.get('spare')}
    for n, chunk in enumerate(split_sentences(toks), 1):
        res['chunks'].append(chunk)
        if chunk[-1]['t'] != '.':
            res['errors'].append((n, 'sentence has no full stop')); chunk = chunk + [tok('.', '.')]
        p = Parser(chunk)
        try:
            s = p.sentence()
            if p.peek()['t'] != 'EOF': p.fail('extra words after the sentence')
            res['sentences'].append(s)
            for w in p.warn: res['errors'].append((n, w))
        except LangError as e:
            res['sentences'].append(None); res['errors'].append((n, str(e)))
        # no English outside code: « » may hold symbols, formulas and units, but a word in Latin letters only in code
        incode = any(t['t'] == 'P' and t['v'] in ('DEFINE', 'IMPORT', 'CODE') for t in chunk[:4])
        for i, t in enumerate(chunk):
            if t['t'] == 'N' and not incode and (re.search(r'[A-Za-z]{4,}', t['v']) or re.fullmatch(r'[A-Za-z]{2,}\d*', t['v'])) and not is_formula(t['v']) and \
                    not (i and chunk[i - 1]['t'] == 'D') and \
                    not (i and chunk[i - 1]['t'] == 'P' and chunk[i - 1]['v'] == 'CODE'):
                res['errors'].append((n, f"Latin-letter word in «{t['v'][:40]}» outside code: spell the term as a loan (or use roots); mark real code text with CODE before the « »"))
        # in code, a library is used only through the short name its IMPORT gave it
        if chunk and any(t['t'] == 'P' and t['v'] == 'DEFINE' for t in chunk[:4]):
            for t in chunk:
                if t['t'] == 'N' and re.fullmatch(r'[A-Za-z_]\w*(\.[A-Za-z_]\w*)+', t['v']):
                    res['errors'].append((n, f"library member «{t['v']}» written with a dot: IMPORT the library NAMED a handle, then write «member» OF that handle"))
        # spares must be defined before use
        is_def = any(t['t'] == 'P' and t['v'] == 'DEFINE' for t in chunk[:4])
        opener_is_head = any(t['t'] == 'P' and t['v'] == 'HEAD' for t in chunk[:3])
        for t in chunk:
            if t.get('spare'):
                if is_def: defined.add(t['v'])
                elif t['v'] not in defined and not (opener_is_head and t['v'] in all_defined):
                    res['errors'].append((n, f"spare word used before any DEFINE: {t.get('form')}"))
    return res


if __name__ == '__main__':
    import sys
    mode = sys.argv[1]; text = open(sys.argv[2], encoding='utf-8').read()
    r = parse(text, mode)
    for n, e in r['errors']: print(f'sentence {n}: {e}')
    print(len(r['sentences']), 'sentences,', sum(1 for s in r['sentences'] if s is None), 'unparsed,', len(r['errors']), 'messages')
