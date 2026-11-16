"""Translator: parsed text -> English (deterministic, rule-based) and logic -> Python."""
import re
import lang as L
import forms as F

try:
    from lemminflect import getInflection
except Exception:                                   # pragma: no cover
    getInflection = None

BE = {('pres', '1'): 'am', ('pres', '3'): 'is', ('pres', 'p'): 'are', ('past', '1'): 'was', ('past', '3'): 'was',
      ('past', 'p'): 'were'}


def infl(w, tag):
    """Inflect the first word of w."""
    first, _, rest = w.partition(' ')
    if first == 'be':
        r = {'VBN': 'been', 'VBG': 'being', 'VB': 'be'}.get(tag, 'be')
    elif getInflection:
        r = getInflection(first, tag=tag)
        r = r[0] if r else first
    else:
        r = first
    return r + (' ' + rest if rest else '')


def plural(n):
    ws = n.split(' ')
    if not ws[-1].isalpha() or not ws[-1].islower(): return n      # IL-4, DNA, A2A: no plural ending
    if getInflection:
        r = getInflection(ws[-1], tag='NNS')
        if r: ws[-1] = r[0]
    return ' '.join(ws)


def a_an(s):
    return ('an ' if re.match(r'[aeiou]', s, re.I) else 'a ') + s


OPENER = {'GIVEN': 'given', 'TOLD': 'told', 'DERIVED': 'it follows', 'RECALLED': 'recalled', 'ASSUMED': 'suppose',
          'CLAIM': 'claim', 'STORY': 'story', 'RULE': 'rule', 'ASK': 'question', 'REQUEST': 'request',
          'PROPOSE': 'proposal', 'PLAN': 'plan', 'DEFINE': 'definition', 'SOCIAL': 'social act', 'HEAD': 'heading', 'IMPORT': 'import library', 'CODE': 'code language', 'CONSIDER': 'considering, not committed'}
REL = {'CONTRAST': 'in contrast to', 'CONCEDE': 'even though', 'RESULT': 'as a result of', 'EVIDENCE': 'as evidence for',
       'EXPLAIN': 'explaining', 'ADD': 'adding to', 'SEQUENCE': 'next after', 'EXAMPLE': 'as an example of',
       'DETAIL': 'detailing', 'RESTATE': 'restating', 'BACKGROUND': 'as background to', 'ASIDE': 'as an aside to',
       'UNDER': 'under the supposition of', 'ANSWER': 'answering', 'REBUT': 'rebutting', 'RETRACT': 'retracting'}
STRENGTH = {'CERTAIN': 'certainly', 'LIKELY': 'probably', 'POSSIBLE': 'possibly'}
ATT = {'SURPRISE': 'surprised', 'EMPHASIS': 'emphatic', 'POLITE': 'polite', 'REGRET': 'with regret', 'GLAD': 'glad',
       'ANNOYED': 'annoyed', 'JEST': 'joking', 'IRONY': 'ironic', 'FRANK': 'frankly', 'HOPE': 'hoping', 'FEAR': 'fearing', 'META': "writer's note about this text",
       'SERIOUS': 'in earnest', 'WARM': 'warmly', 'SAD': 'sadly', 'GRATEFUL': 'gratefully', 'RHETORICAL': 'rhetorically', 'HINT': 'hinting',
       'WARNING': 'as a warning', 'RELUCTANT': 'reluctantly', 'PROUD': 'proudly', 'CURIOUS': 'curious', 'EXCITED': 'excited',
       'RESIGNED': 'resigned', 'DISGUST': 'disgusted', 'EMBARRASSED': 'embarrassed', 'COMFORT': 'comforting'}
DEG = {'VERY': 'very', 'SLIGHT': 'slightly', 'FULL': 'fully', 'BARELY': 'barely', 'ALMOST': 'almost', 'AROUND': 'roughly',
       'ENOUGH': 'enough', 'TOO': 'too', 'MORE': 'more', 'LESS': 'less', 'MOST': 'most', 'LEAST': 'least',
       'EQUAL': 'equally', 'WHAT': 'how'}
FOC = {'ONLY': 'only', 'ALSO': 'also', 'EVEN': 'even', 'INSTEAD': 'instead', 'MAINLY': 'mainly', 'FOCUS': 'specifically',
       'TOPIC': 'as for'}
QNT = {'ALL': 'all', 'MAJOR': 'most', 'MANY': 'many', 'SEVERAL': 'several', 'SOME': 'some', 'FEW': 'few', 'NONE': 'no',
       'ANY': 'any', 'GENERIC': '', 'WHOLE': 'the whole set of', 'THAT': 'the', 'THIS': 'this', 'OTHER': 'other',
       'SAME': 'the same', 'SPECIFIC': 'a certain', 'AROUND': 'about', 'EXACT': 'exactly', 'ATLEAST': 'at least',
       'ATMOST': 'at most', 'ABOVE': 'more than', 'BELOW': 'fewer than', 'WHAT': 'which'}
PLURAL_Q = {'ALL', 'MAJOR', 'MANY', 'SEVERAL', 'FEW', 'GENERIC', 'WHOLE'}
ROLE = {'TO': 'to', 'FROM': 'from', 'AT': 'at', 'WHEN': 'at', 'WITH': 'with', 'CAUSE': 'because of', 'FOR': 'for',
        'THAN': 'than', 'ABOUT': 'about', 'AS': 'as', 'ALONG': 'together with', 'SPAN': 'for', 'EXCEPT': 'except',
        'DESPITE': 'despite', 'VIA': 'through', 'PER': 'per', 'SWAP': 'in place of', 'AGENT': 'by', 'THEME': ''}
ROLE_CL = {'TO': 'until', 'FROM': 'from when', 'AT': 'where', 'WHEN': 'when', 'WITH': 'by having it that',
           'CAUSE': 'because', 'FOR': 'so that', 'THAN': 'than that', 'ABOUT': 'about whether', 'AS': 'as',
           'ALONG': 'while', 'SPAN': 'for as long as', 'EXCEPT': 'unless', 'DESPITE': 'although', 'VIA': 'by way of',
           'PER': 'each time', 'SWAP': 'instead of having', 'AGENT': 'by the fact that', 'THEME': 'that'}
ADV = {'HABIT': 'usually', 'STILL': 'still', 'AGAIN': 'again', 'ALREADY': 'already', 'FINALLY': 'finally',
       'OFTEN': 'often', 'RARE': 'rarely', 'SOMETIMES': 'sometimes', 'ALWAYS': 'always', 'NEVER': 'never'}
NOT_ADV = {'STILL': 'no longer', 'ALREADY': 'not yet', 'ALWAYS': 'not always', 'OFTEN': 'not often',
           'AGAIN': 'not again', 'NEVER': 'not never', 'SOMETIMES': 'not even sometimes', 'RARE': 'not rarely',
           'FINALLY': 'not finally', 'HABIT': 'not usually'}
def er(v):
    ws = v.split(' '); w = ws[0]
    if w.endswith('e'): w += 'r'
    elif w.endswith('y') and len(w) > 2 and w[-2] not in 'aeiou': w = w[:-1] + 'ier'
    elif re.search(r'[^aeiou][aeiou][bdgmnprt]$', w) and len(w) <= 4: w += w[-1] + 'er'
    else: w += 'er'
    return ' '.join([w] + ws[1:])


def compar(adj, deg):
    """more big -> bigger, most small -> smallest (short adjectives only)."""
    if getInflection and ' ' not in adj and len(adj) <= 6 and not adj.endswith(('ed', 'ing', 'ful', 'ous', 'al')):
        r = getInflection(adj, tag='JJR' if deg == 'MORE' else 'JJS')
        if r and not r[0].startswith(('more ', 'most ')): return r[0]
    return DEG[deg] + ' ' + adj


NOUN_OF = {'disappointed': 'disappointment', 'unhappy': 'unhappiness', 'absent': 'absence', 'wrong': 'error'}
SUF_T = {'opp': 'opposite of {n}', 'doer': '{V}', 'made': '{v} product', 'tool': '{v} tool', 'place': '{v} place',
         'ness': '{n}ness', 'group': 'group of {ns}', 'able': '{v}able'}
SLOTN = ['FIRST', 'SECOND', 'THIRD', 'FOURTH']
PYOP = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/', 'quotient': '//', 'remainder': '%', 'power': '**', 'EQUAL': '==',
        'MORE': '>', 'LESS': '<', 'equal': '==', 'and': 'and', 'or': 'or'}


TARGETS = {
    'python':     {'and': ' and ', 'or': ' or ', 'xor': ' != ', 'not': 'not ', 'consts': {'YES': 'True', 'NO': 'False', 'EMPTY': 'None'},
                   'ops': {}, 'end': '', 'comment': '# '},
    'javascript': {'and': ' && ', 'or': ' || ', 'xor': ' !== ', 'not': '!', 'consts': {'YES': 'true', 'NO': 'false', 'EMPTY': 'null'},
                   'ops': {'==': '===', 'and': '&&', 'or': '||'}, 'end': ';', 'comment': '// '},
}
TARGET_ALIASES = {'py': 'python', 'python3': 'python', 'js': 'javascript', 'node': 'javascript'}


class Decoder:
    tgt = 'python'
    @property
    def T(self): return TARGETS[self.tgt]
    def blk(self, pad, head, body, cont=False):
        """One block statement in the target's syntax. cont: an else-part follows."""
        if self.tgt == 'python': return [pad + head + ':'] + (body or [pad + '    pass'])
        return [pad + head + ' {'] + body + ([] if cont else [pad + '}'])

    def __init__(self, lex=None, hletter=None):
        self.lex = lex or L.LEX
        self.hletter = dict(hletter or {})       # native handle -> letter
        self.hnoun = {}         # letter -> noun
        self.spare = {}         # spare form -> english

    # ---------------------------------------------------------- words
    def hname(self, h):
        if F.parts(h[0]) is None: return h
        if h not in self.hletter:
            self.hletter[h] = L.handle_letter(h, self.hletter)
        return self.hletter[h]

    def rinfo(self, t):
        """-> dict(type, verb, noun, adj, rel) for a root token (with suffixes)."""
        g = t['v']; e = self.lex['roots'].get(g)
        if t.get('spare') or g.startswith('spare:'):
            if g not in self.spare: self.spare[g] = 'W' + str(len(self.spare) + 1)
            w = self.spare[g]
            return {'type': 'T', 'verb': w, 'noun': w, 'adj': w, 'rel': w + ' of', 'tr': 1}
        if e is None:
            e = {'type': 'A', 'tr': 1}
        d = {'type': e.get('type', 'A'), 'verb': g, 'noun': e.get('noun') or None, 'adj': e.get('adj') or None,
             'rel': e.get('rel') or None, 'tr': int(e.get('tr') or 0), 'gloss': g}
        if d['noun'] is None:
            d['noun'] = g + 'ness' if d['type'] == 'Q' else g
        if d['adj'] is None:
            d['adj'] = g
        cur = g
        for s in t.get('suf', []):
            key = cur + '.' + s
            w = self.lex['derived'].get(key)
            if w is None:
                if s == 'opp' and d['type'] in 'AEQ': w = 'un' + d['verb']
                else: w = SUF_T[s].format(n=d['noun'], v=d['verb'], ns=plural(d['noun']), V=er(d['verb']))
            if s == 'opp':
                d.update(verb=w, noun=NOUN_OF.get(w) or (w if d['type'] in 'TR' else (w + 'ness' if d['type'] == 'Q' else infl(w, 'VBG'))),
                         adj=w if d['type'] in 'QTR' else infl(w, 'VBG'), rel=(('~' if (d.get('rel') or '').startswith('~') else '') + w + (' of' if (d.get('rel') or '').endswith(' of') else '')))
            elif s == 'able':
                d.update(type='Q', verb=w, noun=w + 'ness', adj=w, rel=None)
            else:
                d.update(type='T', verb=w, noun=w, adj=w, rel=w + ' of')
            cur = key
        return d

    # ---------------------------------------------------------- phrases
    def phrase(self, p, case='obj', art='the'):
        """-> (text, plural?, person)"""
        us = [self.unit(u, case, art) for u in p['units']]
        if len(us) == 1: return us[0]
        words = {'AND': 'and', 'OR': 'or', 'XOR': 'or'}
        txt = us[0][0]
        for op, u in zip(p['ops'], us[1:]):
            txt += (', ' if len(us) > 2 else ' ') + words[op] + ' ' + u[0]
        if 'XOR' in p['ops']: txt = 'either ' + txt + ' (not both)'
        return txt, ('AND' in p['ops']), '3'

    def head(self, h, case, u, art):
        """-> (text, kind) kind: noun|pron|other ; sets plural/person on u['_n']"""
        k = h.get('k') or h['t']
        if k == 'R':
            return self.rinfo(h)['noun'], 'noun'
        if k == 'H':
            nm = self.hname(h['v'])
            if nm in self.hnoun and self.hnoun[nm]:
                return self.hnoun[nm] + ' ' + nm, 'other'
            return nm, 'other'
        if k == 'L': return h['v'], 'noun'
        if k == 'N': return h['v'], 'other'
        if k == 'D': return h['v'], 'other'
        if k == 'name':
            ws = []
            for x in h['parts']:
                w = x['v'] if x['t'] != 'R' else self.rinfo(x)['noun']
                ws.append(w if x['t'] == 'N' or not w.islower() else w.capitalize())
            return ' '.join(ws), 'other'
        if k == 'step':
            return 'step ' + h['a'] + (' to ' + h['b'] if h['b'] else ''), 'other'
        if k == 'paren':
            ph = h['phrase']
            sl = [r for u2 in ph['units'] for r in u2.get('roles', []) if r['role'] in SLOTN]
            if len(ph['units']) == 1 and sl:
                u2 = ph['units'][0]; hh = u2['head']
                if hh.get('k') == 'paren':
                    nm = self.unit({'k': 'unit', 'pre': [], 'q': [], 'mods': [], 'roles': [], 'head': hh}, art='')[0]
                else:
                    nm = self.rinfo(hh)['verb'] if hh.get('t') == 'R' else (DEG.get(hh['v'], hh['v']).lower() if hh.get('t') == 'P' else str(hh.get('v')))
                    for m in u2['mods']:
                        if m['link'] == 'OF' and m['unit']['head'].get('t') == 'H': nm = self.hname(m['unit']['head']['v']) + '.' + nm
                return nm + '(' + ', '.join(self.phrase(r['phrase'], art='')[0] for r in sorted(sl, key=lambda r: SLOTN.index(r['role']))) + ')', 'other'
            t3 = self.phrase(ph, case, art)
            u['_pl'] = t3[1]
            return t3[0], 'other'
        if k == 'block':
            return self.block(h, 'that'), 'other'
        if k == 'P':
            v = h['v']
            subj = case == 'subj'
            m = {'ME': 'I' if subj else 'me', 'YOU': 'you', 'US': 'we' if subj else 'us', 'WE': 'we (you and I)' if subj else 'us (you and me)', 'SELF': 'it' if subj else 'itself',
                 'MUTUAL': 'each other', 'WHAT': 'who or what' if subj else 'what', 'THIS': 'this', 'THAT': 'that', 'NOW': 'now', 'YES': 'yes',
                 'NO': 'no', 'EMPTY': 'nothing'}
            if v in m:
                u['_person'] = {'ME': '1', 'YOU': 'p', 'US': 'p', 'WE': 'p'}.get(v, '3')
                return m[v], 'pron'
            return DEG.get(v, v.lower()), 'other'
        return '?', 'other'

    def unit(self, u, case='obj', art='the'):
        u['_person'] = '3'
        htxt, hk = self.head(u['head'], case, u, art)
        pl = False; qs = []; has_det = False
        qn = [q for q, _ in u['q']]
        for i, (q, arg) in enumerate(u['q']):
            if q == 'NUM':
                if isinstance(arg, dict): arg = self.hname(arg['v'])
                qs.append(arg); has_det = True
                pl = pl or arg not in ('1',)
            elif q == 'ORDRANGE':
                f = lambda a: ('(' + self.phrase(a['phrase'], art='')[0] + ')-th' if a.get('k') == 'paren' else self.hname(a['v']) + '-th') if isinstance(a, dict) else a + {'1': 'st', '2': 'nd', '3': 'rd'}.get(a, 'th')
                qs.append(f'the {f(arg[0])} to the {f(arg[1])}'); has_det = True; pl = True
            elif q == 'ORD' and isinstance(arg, dict):
                qs.append('the ' + ('(' + self.phrase(arg['phrase'], art='')[0] + ')' if arg.get('k') == 'paren' else self.hname(arg['v'])) + '-th'); has_det = True
            elif q == 'ORD':
                n = int(arg); sfx = 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
                qs.append(f'the {n}{sfx}'); has_det = True
            elif q == 'WHAT' and i + 1 < len(qn) and qn[i + 1] in ('MANY', 'FEW'):
                qs.append('how')
            elif q in QNT:
                w = QNT[q]
                if q == 'OTHER' and not has_det: w = 'another' if not pl else 'other'
                if w: qs.append(w)
                has_det = True; pl = pl or q in PLURAL_Q
            else:
                qs.append(DEG.get(q, q.lower())); has_det = has_det or q in ('MORE', 'LESS', 'ENOUGH')
                if q in ('MORE', 'LESS', 'MOST', 'ENOUGH', 'TOO'): pl = True
        # modifiers
        pre, post = [], []
        rel_done = False
        hinfo = self.rinfo(u['head']) if u['head'].get('t') == 'R' else None
        for m in u['mods']:
            mu = m['unit']; mh = mu['head']; link = m['link']
            neg = 'not ' if m.get('neg') else ''
            deg = ''.join(DEG[d] + ' ' for d in m.get('deg', []))
            if link == 'KIND':
                if mh.get('t') == 'P' and mh['v'] == 'WHAT':
                    qs.insert(0, 'what kind of'); has_det = True
                elif mh.get('k') == 'block':
                    self._gap_pl = pl
                    post.append(self.relclause(mh))
                elif mh.get('k') == 'name' and not neg and not mu['mods']:
                    pre.append(self.head(mh, 'obj', mu, '')[0])
                elif mh.get('t') == 'L' and not neg:
                    pre.append(deg + mh['v'])
                elif mh.get('t') == 'R' and not mu['q'] and not mu.get('named'):
                    mi = self.rinfo(mh); w = mi['adj']
                    if neg: post.append('that is not ' + deg + (infl(mi['verb'], 'VBN') if mi['type'] in 'AE' and w == mi['verb'] else w))
                    else: pre.append(self.degadj(m.get('deg', []), w))
                elif mh.get('k') == 'paren':
                    inner = mh['phrase']
                    if len(inner['units']) == 1 and inner['units'][0]['head'].get('t') == 'R' and not inner['units'][0]['roles'] \
                            and not inner['units'][0]['mods'] and all(q in DEG for q, _ in inner['units'][0]['q']):
                        iu = inner['units'][0]
                        aw = self.degadj([q for q, _ in iu['q']], self.rinfo(iu['head'])['adj'])
                        if iu.get('neg') or neg: post.append(('that are not ' if pl else 'that is not ') + aw)
                        else: pre.append(aw)
                    else:
                        post.append(('that are ' if pl else 'that is ') + neg + self.predphrase(inner))
                else:
                    post.append('of kind ' + neg + deg + self.unit(mu, 'obj', '')[0])
            elif link == 'OF':
                post.append('of ' + self.unit(mu)[0])
            elif link == 'HAVING':
                post.append(('without ' if neg else 'with ') + self.unit(mu, art='')[0])
            elif link == 'REL':
                lm = self.unit(mu)[0]
                if hinfo and (hinfo.get('rel') or '').startswith('~'):
                    htxt = re.sub(r'^the ', '', lm) + ' ' + hinfo['rel'][1:]; hk = 'rel'
                elif hinfo and hinfo.get('rel'):
                    htxt = hinfo['rel'] + ' ' + lm; rel_done = True
                    if not hinfo['rel'].endswith(' of'): hk = 'rel'
                else:
                    post.append('of ' + lm)
            elif link == 'NOTE':
                if mh.get('k') == 'block': post.append('(' + self.block(mh, '').strip() + ')')
                else: post.append('(namely ' + self.unit(mu, art='')[0] + ')')
            elif link == 'SUCHAS':
                post.append('such as ' + self.unit(mu, art='')[0])
        if hk == 'noun' and pl: htxt = plural(htxt)
        words = []
        if qs: words += qs
        elif hk == 'noun' and art and not u.get('neg'):
            words.append(art if art != 'a' else None)
        if u.get('tag'): htxt += ' ' + u['tag']; words = [w for w in words if w != 'the']
        core = ' '.join(pre + [htxt])
        if art == 'a' and not qs and hk == 'noun': core = a_an(core)
        txt = ' '.join([w for w in words if w] + [core] + post)
        for m in u['mods']:                                   # never lose a number or name attached to a modifier
            tg = m['unit'].get('tag')
            if tg and tg not in txt: txt += ' ' + tg
            for qk, qv in m['unit'].get('q', []):
                qv = qv if isinstance(qv, str) else None
                if qk == 'NUM' and qv and not re.search(r'(?<![\w.])' + re.escape(qv) + r'(?![\w.])', txt): txt += ' (' + qv + ')'
        if u.get('neg'): txt = 'not ' + txt
        for f in reversed(u['pre']):
            txt = (FOC.get(f) or STRENGTH.get(f) or ATT.get(f, f.lower())) + ' ' + txt
        if u.get('named'):
            nm = self.hname(u['named'])
            self.hnoun[nm] = htxt if hk == 'noun' and u['head'].get('t') in ('R', 'L') and not pl else ''
            txt += f' (call it {nm})'
        for r in u.get('roles', []):
            txt += ' ' + self.rolephrase(r)
        return txt, pl or u.get('_pl', False), u['_person']

    def degadj(self, degs, adj):
        degs = list(degs)
        if degs and degs[-1] in ('MORE', 'MOST'):
            return ''.join(DEG[d] + ' ' for d in degs[:-1]) + compar(adj, degs[-1])
        return ''.join(DEG[d] + ' ' for d in degs) + adj

    def predphrase(self, p):
        """Phrase used as a predicate complement: 'an unhandled exception', 'more fast than 30 mph'."""
        us = p['units']
        if len(us) == 1 and us[0]['head'].get('t') == 'R':
            info = self.rinfo(us[0]['head'])
            if info['type'] == 'Q':
                u = us[0]
                t = ''.join((DEG.get(q) or QNT.get(q) or (a or '')) + ' ' for q, a in u['q']) + info['adj']
                for m in u['mods']: t += ' ' + self.unit({'k': 'unit', 'pre': [], 'q': [], 'mods': [m], 'roles': [], 'head': L.tok('N', '')}, art='')[0].strip()
                for r in u['roles']: t += ' ' + self.rolephrase(r)
                return ('not ' if u.get('neg') else '') + t
            if info['type'] == 'R' and any(m['link'] == 'REL' for m in us[0]['mods']) and not (info.get('rel') or '').endswith(' of'):
                return self.unit(us[0], art='')[0]
        return self.phrase(p, art='a')[0]

    def rolephrase(self, r):
        t = self.rolephrase0(r)
        return (r['focus'].lower() + ' ' + t) if r.get('focus') else t

    def rolephrase0(self, r):
        role = r['role']; p = r['phrase']
        if role in SLOTN: return self.phrase(p)[0]
        u0 = p['units'][0]
        if len(p['units']) == 1 and u0['head'].get('k') == 'block' and not u0['q'] and not u0['mods']:
            b = u0['head']
            if role == 'THEME' and len(b['stmts']) == 1 and 'by' in b['stmts'][0]:
                return self.block(b, '')
            return ROLE_CL[role] + ' ' + self.block(b, '')
        prep = ROLE[role]
        if r.get('as'): prep = 'as'
        if r.get('like'): prep = 'like'
        txt = self.phrase(p)[0]
        if r.get('sub'):
            return 'than ' + txt + ' does' if r['sub'] == 'AGENT' else ('than ' + (ROLE[r['sub']] + ' ' if ROLE[r['sub']] else '') + txt)
        h = u0['head']
        if role in ('WHEN', 'AT') and h.get('t') == 'R':
            info = self.rinfo(h)
            if info['type'] == 'R' and any(m['link'] == 'REL' for m in u0['mods']) and not (info.get('rel') or '').endswith(' of'):
                prep = ''
        if role == 'WHEN' and h.get('t') == 'P' and h['v'] == 'NOW': prep = ''
        if role == 'WHEN' and (h.get('k') == 'name'): prep = 'on'
        if role == 'WHEN' and any(q in ('THIS', 'ALL', 'ANY', 'OTHER') for q, _ in u0['q']): prep = ''
        if role == 'WHEN' and h.get('t') == 'R' and h['v'] in ('morning', 'evening', 'afternoon', 'year', 'month', 'week') and prep: prep = 'in'
        if role == 'WHEN' and h.get('t') == 'R' and h['v'] in ('day',) and prep: prep = 'on'
        return (prep + ' ' + txt).strip()

    def relclause(self, b):
        st = b['stmts'][0]; body = st['body']; gp = getattr(self, '_gap_pl', False)
        if body['k'] == 'clause':
            self._gap_now = gp
            subj, pred = self.clause(body, gap=True)
            if subj is None: return 'that ' + pred
            return 'such that ' + subj + ' ' + pred
        if body['k'] == 'cjoin':
            ps = []
            for p in body['parts']:
                self._gap_now = gp; ps.append(self.clause(p, gap=True))
            if all(s is None for s, _ in ps):
                out = 'that ' + ps[0][1]
                for (op, rel), (_, p) in zip(body['ops'], ps[1:]):
                    out += {'ANDC': ' and ', 'ORC': ' or ', 'BUT': ' but '}[op] + ('then ' if rel == 'SEQUENCE' else '') + p
                return out
        return 'such that ' + self.stmt(st)

    def block(self, b, lead='that'):
        outs = []
        for st in b['stmts']:
            self._depth = getattr(self, '_depth', 0) + 1
            t = self.stmt(st)
            self._depth -= 1
            if 'by' in st:
                sp = self.unit(st['by'], 'subj')[0]
                t = (f'{sp} (in other words): ' if st.get('para') else f'{sp}: ') + '“' + t + '”'
            outs.append(t)
        txt = '; '.join(outs)
        if lead and not ('by' in b['stmts'][0]) and not b['stmts'][0].get('head'):
            txt = lead + ' ' + txt
        return txt

    # ---------------------------------------------------------- clauses
    def vg(self, lemma, pre, person='3', plural_=False, passive=False, imperative=False, cop=False):
        """Verb group -> (text_before_complement, tail_adverbs). lemma may be multiword ('put out')."""
        tense = 'pres'; modal = None; neg = False; neg_modal = False; neg_inner = False
        perf = prog = False; phase = None; advs = []; tail = []; degs = []
        near = far = False
        i = 0
        pre = list(pre)
        while i < len(pre):
            n, arg = pre[i]; nxt = pre[i + 1][0] if i + 1 < len(pre) else None
            if n == 'NOT':
                if nxt == 'ALREADY': neg = True; tail.append('yet'); i += 2; continue
                if nxt in NOT_ADV: advs.append(NOT_ADV[nxt]); i += 2; continue
                if nxt in ('MUST', 'SHOULD', 'MAY', 'CAN', 'WANT', 'TRY'): neg_modal = True
                elif modal: neg_inner = True
                else: neg = True
            elif n in ('PAST', 'FUTURE', 'UNREAL'): tense = {'PAST': 'past', 'FUTURE': 'fut', 'UNREAL': 'unreal'}[n]
            elif n == 'NOW': advs.append('currently')
            elif n == 'NEAR': near = True
            elif n == 'FAR': far = True
            elif n == 'ONGOING': prog = True
            elif n == 'DONE': perf = True
            elif n in ('BEGIN', 'STOP'): phase = n
            elif n in ADV: advs.append(ADV[n])
            elif n == 'TIMES':
                a = arg
                for k_, v_ in QNT.items(): a = re.sub(r'\b' + k_ + r'\b', v_, a)
                tail.append('how many times' if arg == 'WHAT' else ('once' if a == '1' else 'twice' if a == '2' else a + ' times'))
            elif n == 'FACTOR': degs.append(arg + ' times')
            elif n == 'NTH':
                k_ = int(arg); tail.append('for the ' + arg + ('th' if 10 <= k_ % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k_ % 10, 'th')) + ' time')
            elif n in ('MUST', 'SHOULD', 'MAY', 'CAN', 'WANT', 'TRY'): modal = n
            elif n in STRENGTH: advs.append(STRENGTH[n])
            elif n in FOC: advs.append(FOC[n])
            elif n in DEG: degs.append(DEG[n])
            i += 1
        if near: advs.append('just' if tense == 'past' else 'soon')
        if far: tail.append('long ago' if tense == 'past' else 'far in the future')
        seq = []
        if modal in ('WANT', 'TRY'): seq.append(({'WANT': 'want', 'TRY': 'try'}[modal], 'to'))
        if phase == 'BEGIN' and lemma == 'be' and not (perf or prog or passive): lemma = 'become'
        elif phase == 'BEGIN': seq.append(('begin', 'to'))
        if phase == 'STOP': seq.append(('stop', 'ing'))
        if perf: seq.append(('have', 'pp'))
        if prog: seq.append(('be', 'ing'))
        if passive: seq.append(('be', 'pp'))
        seq.append((lemma, None))
        aux = None; inner_not = ''
        if modal in ('MUST', 'SHOULD', 'MAY', 'CAN'):
            base = {'MUST': 'must', 'SHOULD': 'should', 'MAY': 'may', 'CAN': 'can'}[modal]
            if neg_modal:
                aux = {'MUST': 'does not have to', 'SHOULD': 'is not advised to', 'MAY': 'may not', 'CAN': 'cannot'}[modal]
                if person != '3' or plural_: aux = aux.replace('does', 'do').replace('is not', 'are not' if person != '1' else 'am not')
            else:
                aux = base
            if tense == 'past':
                aux = {'must': 'had to', 'can': 'could', 'cannot': 'could not', 'does not have to': 'did not have to',
                       'do not have to': 'did not have to'}.get(aux, aux)
                if aux in ('should', 'may', 'may not'): seq.insert(0, ('have', 'pp'))
            elif tense == 'fut':
                aux = {'must': 'will have to', 'can': 'will be able to', 'cannot': 'will not be able to'}.get(aux, aux)
            elif tense == 'unreal':
                aux = {'must': 'would have to', 'can': 'could', 'cannot': 'could not', 'may': 'might'}.get(aux, aux)
            if neg_inner: inner_not = 'not'
        elif tense == 'fut': aux = 'will'
        elif tense == 'unreal': aux = 'would'
        if modal in ('WANT', 'TRY') and neg_inner: seq.insert(1, ('NOT', None))
        words = []
        neg_word = neg or (neg_modal and modal in ('WANT', 'TRY'))
        if imperative:
            words = (['do not'] if neg_word else []) + advs
            link = 'base'
        elif aux:
            words = [aux] + ([inner_not] if inner_not else []) + (['not'] if neg_word else []) + advs
            link = 'base'
        else:
            first, flink = seq[0]
            past = tense == 'past'
            key = ('past' if past else 'pres', 'p' if (plural_ or person == 'p') else person)
            if first == 'be':
                words = [BE[key]] + advs + (['not'] if neg_word else [])
            elif neg_word or False:
                if first == 'have' and flink == 'pp':
                    words = [('had' if past else ('has' if key[1] == '3' else 'have')), 'not'] + advs
                else:
                    words = advs + [('did' if past else ('does' if key[1] == '3' else 'do')), 'not'] + [infl(first, 'VB')]
            else:
                f = infl(first, 'VBD') if past else (infl(first, 'VBZ') if key[1] == '3' else first)
                words = advs + [f]
            seq = seq[1:]; link = flink
        for lem, nl in seq:
            if lem == 'NOT': words.append('not'); continue
            if link == 'to': words.append('to ' + infl(lem, 'VB'))
            elif link == 'pp': words.append(infl(lem, 'VBN'))
            elif link == 'ing': words.append(infl(lem, 'VBG'))
            else: words.append(infl(lem, 'VB'))
            link = nl
        return ' '.join(w for w in words if w), tail, degs

    def clause(self, c, gap=False, mood=None):
        """-> (subject or None, predicate text)."""
        if not gap: self._gap_now = False
        roles = list(c['roles']); pred = c['pred']

        def is_self(r):
            p = r['phrase']
            return len(p['units']) == 1 and p['units'][0]['head'].get('t') == 'P' and p['units'][0]['head']['v'] == 'SELF' \
                and not p['units'][0]['mods'] and not p['units'][0]['q']

        def pop(name):
            for r in roles:
                if r['role'] == name:
                    roles.remove(r); return r
            return None

        agent = pop('AGENT'); theme = pop('THEME')
        comp = ''; lemma = 'be'; passive = False; subj_r = None; obj_r = None; extra = ''
        k = pred['k']
        if k == 'rpred':
            h = pred['unit']['head']
            if h['t'] == 'R':
                info = self.rinfo(h)
            else:
                info = {'type': 'A', 'verb': h['v'], 'noun': h['v'], 'adj': h['v'], 'rel': None, 'tr': 1}
            ty = info['type']
            mods = pred['unit']['mods']
            manner = ''
            relm = [m for m in mods if m['link'] == 'REL']
            for m in mods:
                if m['link'] == 'KIND' and m['unit']['head'].get('t') == 'R':
                    manner += ' in a ' + ''.join(DEG[d] + ' ' for d in m.get('deg', [])) + self.rinfo(m['unit']['head'])['adj'] + ' way'
                elif m['link'] != 'REL':
                    manner += ' ' + self.unit({'k': 'unit', 'pre': [], 'q': [], 'mods': [m], 'roles': [], 'head': L.tok('N', '')}, art='')[0].strip()
            if ty == 'R' and not relm and agent is not None and theme is not None:
                ty = 'A'                                       # cause AGENT x THEME y -> "x causes y"
            if ty in 'AE' and not relm:
                lemma = info['verb']
                if ty == 'A':
                    subj_r, obj_r = agent, theme
                    if agent is None and theme is not None and h['t'] == 'L':
                        subj_r, obj_r = theme, None                      # loan verb with only a THEME: "the server crashed"
                    elif agent is None and theme is not None and mood not in ('REQUEST', 'PLAN', 'PROPOSE'):
                        subj_r, obj_r, passive = theme, None, True
                else:
                    if agent is None: subj_r = theme
                    else:
                        w = self.lex['derived'].get(info.get('gloss', '') + '+agent') if not h.get('suf') else None
                        if w: lemma = w; subj_r, obj_r = agent, theme
                        elif info.get('tr'): subj_r, obj_r = agent, theme        # labile verb: change, break, increase
                        else:
                            subj_r, obj_r = agent, theme; extra = ' ' + lemma; lemma = 'make'
                extra += manner
            else:
                if ty == 'Q' or (ty in 'AE'):
                    comp = info['adj']
                elif ty == 'R' or relm:
                    if relm:
                        lm = self.unit(relm[0]['unit'])[0]
                        rel = info.get('rel') or (info['noun'] + ' of')
                        comp = (a_an(rel) if rel.endswith(' of') else rel) + ' ' + lm
                    else:
                        comp = a_an(info['noun'])
                else:
                    comp = a_an(info['noun'])
                comp += manner
                if agent is not None and theme is not None:
                    w = self.lex['derived'].get(info.get('gloss', '') + '+agent') if (ty == 'Q' and not h.get('suf')) else None
                    subj_r, obj_r = agent, theme
                    if w: lemma = w; extra = manner; comp = ''
                    else: lemma = 'make'; extra = ' ' + (comp if ty != 'T' else 'into ' + comp); comp = ''
                else:
                    subj_r = theme or agent
        elif k == 'ppred':
            comp = self.predphrase(pred['phrase']); subj_r = theme or agent
            if theme and agent: roles.insert(0, agent)
        elif k == 'be':
            subj_r = theme or agent
        elif k == 'dpred':
            d = pred['deg']; subj_r = theme or agent
            comp = {'EQUAL': 'equal to', 'MORE': 'more', 'LESS': 'less'}.get(d, DEG.get(d, d.lower()))
            sl = sorted([r for r in roles if r['role'] in SLOTN], key=lambda r: SLOTN.index(r['role']))
            if len(sl) == 2 and subj_r is None:            # slot form: MORE FIRST a SECOND b
                for r in sl: roles.remove(r)
                subj_r = sl[0]
                comp = {'EQUAL': 'equal to', 'MORE': 'more than', 'LESS': 'less than'}.get(d, comp) + ' ' + self.phrase(sl[1]['phrase'])[0]
            for r in roles:
                if r['role'] == 'THAN' and d == 'EQUAL':
                    roles.remove(r); comp += ' ' + self.phrase(r['phrase'])[0]; break
        # subject
        imperative = False
        if subj_r is None:
            if mood == 'REQUEST' and k == 'rpred': imperative = True; subj = ''
            elif mood == 'PLAN': subj = 'I'; person, pl = '1', False
            elif mood == 'PROPOSE': subj = 'we'; person, pl = 'p', True
            elif k == 'rpred' and lemma != 'be' and not passive: subj = 'someone' if info['type'] == 'A' else 'it'
            else: subj = 'it'
            if subj and mood not in ('PLAN', 'PROPOSE'): person, pl = '3', False
            if imperative: person, pl = 'p', False
        elif gap and is_self(subj_r):
            subj = None; person, pl = '3', getattr(self, '_gap_now', False)
        else:
            subj, pl, person = self.phrase(subj_r['phrase'], 'subj')
            u0 = subj_r['phrase']['units'][0]
            if len(subj_r['phrase']['units']) == 1 and u0['head'].get('k') == 'block':
                person, pl = '3', False
        if not any(x[0] in ('MORE', 'LESS', 'MOST', 'LEAST', 'EQUAL', 'TOO', 'ENOUGH') for x in c['pre']) and k != 'dpred' and 'more' not in comp and 'less' not in comp:
            for r in roles:
                if r['role'] == 'THAN' and not r.get('sub'): r['like'] = True
        if pl and k == 'rpred' and comp.startswith(('a ', 'an ')) and not relm and info['type'] == 'T':
            comp = plural(info['noun']) + manner
        gap_obj = False
        if gap and obj_r is not None and is_self(obj_r) and subj is not None:
            obj_r = None; gap_obj = True
        vgtxt, tail, degs = self.vg(lemma, c['pre'], person, pl, passive, imperative)
        out = vgtxt
        if comp:
            dtxt = ' '.join(degs)
            if 'enough' in degs: dtxt = ' '.join(d for d in degs if d != 'enough'); comp = comp + ' enough'
            if 'equally' in degs:
                dtxt = ' '.join(d for d in degs if d != 'equally') + ' as'
                for r in roles:
                    if r['role'] == 'THAN': r['as'] = True
            if dtxt.split(' ')[-1:] in (['more'], ['most']) and k == 'rpred' and info['type'] == 'Q':
                cw = comp.split(' '); one = compar(cw[0], 'MORE' if dtxt.endswith('more') else 'MOST')
                if not one.startswith(('more ', 'most ')):
                    comp = ' '.join([one] + cw[1:]); dtxt = ' '.join(dtxt.split(' ')[:-1])
            out += ' ' + (dtxt + ' ' if dtxt else '') + comp
            degs = []
        if obj_r is not None:
            o = self.rolephrase({'role': 'THEME', 'phrase': obj_r['phrase'], 'sub': None})
            out += ' ' + o
        out += extra
        if degs: out += ' ' + ' '.join('very much' if d == 'very' else d for d in degs)
        for r in roles:
            out += ' ' + self.rolephrase(r)
        if tail: out += ' ' + ' '.join(tail)
        if gap_obj: return None, (subj + ' ' if subj else '') + re.sub(r'\s+', ' ', out).strip()
        return subj, re.sub(r'\s+', ' ', out).strip()

    def body(self, b, mood=None):
        k = b['k']
        if k == 'clause':
            s, p = self.clause(b, mood=mood)
            return (s + ' ' if s else '') + p
        if k == 'cjoin':
            out = self.body(b['parts'][0], mood)
            for (op, rel), part in zip(b['ops'], b['parts'][1:]):
                w = {'ANDC': 'and', 'ORC': 'or', 'BUT': 'but'}[op]
                if rel: w += {'SEQUENCE': ' then', 'RESULT': ' so', 'CONTRAST': ' in contrast', 'CONCEDE': ' yet',
                              'EXPLAIN': ' this is because', 'ADD': ' also'}.get(rel, ' (' + rel.lower() + ')')
                out += ', ' + w + ' ' + self.body(part, mood)
            return out
        if k == 'scoped':
            W = {'NOT': 'it is not the case that', 'MUST': 'it must be that', 'SHOULD': 'it should be that', 'MAY': 'it is allowed that',
                 'CAN': 'it can be that', 'WANT': 'it is wanted that', 'TRY': 'it is attempted that',
                 'CERTAIN': 'certainly', 'LIKELY': 'probably', 'POSSIBLE': 'possibly'}
            return ' '.join(W.get(o) or '(' + ATT.get(o, o.lower()) + ')' for o in b['ops']) + ' [' + self.block(b['block'], '') + ']'
        if k == 'if':
            t = 'if ' + self.block(b['cond'], '') + ', then ' + self.block(b['then'], '')
            if b['else']: t += '; otherwise ' + self.block(b['else'], '')
            for r in b.get('roles') or []: t += ', ' + self.rolephrase(r)
            return t
        if k == 'each':
            return f"for each {self.hname(b['var'])} in {self.phrase(b['in'])[0]}: " + self.block(b['do'], '')
        if k == 'while':
            return 'while ' + self.block(b['cond'], '') + ': ' + self.block(b['do'], '')
        if k == 'return':
            return 'return ' + self.phrase(b['val'], art='')[0]
        if k == 'define':
            term = self.phrase(b['term'], art='')[0]
            if b['params']:
                return f"{term}({', '.join(self.hname(p) for p in b['params'])}) is defined as: " + self.phrase(b['val'], art='')[0]
            u0 = b['term']['units'][0]
            if u0['head'].get('t') == 'H' and len(b['term']['units']) == 1:
                return f"let {term} be {self.phrase(b['val'], art='')[0]}"
            val = self.phrase(b['val'], art='a')[0]
            return f'“{term}” means {val}'
        if k == 'frag':
            if 'roles' in b: return ' '.join(self.rolephrase(r) for r in b['roles'])
            us = b['phrase']['units']
            if mood == 'SOCIAL' and len(us) == 1 and us[0]['head'].get('t') == 'R' and not us[0]['mods']:
                return self.rinfo(us[0]['head'])['verb']
            return self.phrase(b['phrase'], art='')[0] + (' ' + b['phrase']['num'] if b['phrase'].get('num') else '') + (' ' + self.head(b['phrase']['title'], 'obj', {'q': [], 'mods': []}, '')[0] if b['phrase'].get('title') else '') + ''.join(' ' + self.rolephrase(r) for r in b.get('extra', []))
        return '?'

    def header(self, h):
        tags = []
        op = h['opener']; t = OPENER[op]
        if op == 'DERIVED':
            t = ('it follows from ' + ', '.join(h['basis'])) if h.get('basis') else 'apparently'
        if op == 'TOLD' and h.get('source'): t += ' by ' + self.hname(h['source'])
        if op == 'ASK' and h.get('expect'): t += ', expecting ' + h['expect'].lower()
        tags.append(t)
        for r, ls in h['rels']:
            tags.append(REL[r] + (' ' + ', '.join(ls) if ls else ' the previous sentence') if r != 'ASIDE' or ls else 'aside')
        if h.get('strength'):
            tags.append({'CERTAIN': 'certain', 'LIKELY': 'likely', 'POSSIBLE': 'possible'}[h['strength']] +
                        (' ' + h['strength_n'] if h.get('strength_n') else ''))
        for d, a in h['att']:
            tags.append((DEG[d] + ' ' if d else '') + ATT[a])
        if h.get('call'): tags.append('to ' + self.unit(h['call'], art='')[0])
        return '[' + '; '.join(tags) + ']'

    def stmt(self, s):
        mood = s.get('head', {}).get('opener')
        t = self.body(s['body'], mood)
        if mood == 'ASK': t += '?'
        if s.get('head') and not (getattr(self, '_depth', 0) > 0 and mood == 'DEFINE'): t = self.header(s['head']) + ' ' + t
        return t

    def sentence(self, s):
        t = self.stmt(s)
        m = re.match(r'(\[[^\]]*\] )?(.*)', t, re.S)
        body = m.group(2); body = body[:1].upper() + body[1:]
        t = (m.group(1) or '') + body
        if not t.endswith('?'): t += '.'
        pre = ''
        if 'by' in s:
            pre = self.unit(s['by'], 'subj', art='')[0] + (' (paraphrased)' if s.get('para') else '') + ': '
        lab = s.get('label')
        return (lab + '. ' if lab else '') + pre + t

    # ---------------------------------------------------------- python
    def py_name(self, u):
        h = u['head']; k = h.get('k') or h['t']
        if k == 'H': return self.hname(h['v']).lower()
        if k == 'N': return h['v']
        if k == 'D': return h['v']
        if k == 'R' and (h.get('spare') or h['v'].startswith('spare:')):
            return self.rinfo(h)['noun'].lower()
        if k == 'R':
            parts_ = [self.py_key(h) if h.get('suf') else h['v']]
            for m in u['mods']:
                if m['link'] == 'KIND' and m['unit']['head'].get('t') == 'R': parts_.append(m['unit']['head']['v'])
            return '_'.join(parts_)
        if k == 'L': return re.sub(r'\W+', '_', h['v'])
        if k == 'P': return self.T['consts'].get(h['v'], h['v'])
        if k == 'paren':
            if len(h['phrase']['units']) == 1: return self.py_name(h['phrase']['units'][0])
            return self.py_expr(h['phrase'])
        return '?'

    def py_key(self, h):
        """Operator key of a root token: add.opp -> subtract."""
        if h.get('t') != 'R': return h.get('v')
        cur = h['v']
        for sfx in h.get('suf', []):
            w = self.lex['derived'].get(cur + '.' + sfx)
            cur = w.split(',')[0].split(';')[0].strip().replace(' ', '_') if w else cur + '_' + sfx
        return cur

    def py_call(self, name, key, args):
        js = self.tgt == 'javascript'
        if key in PYOP and len(args) == 2:
            op = PYOP[key]
            if js and op == '//': return f'Math.floor({args[0]} / {args[1]})'
            return f'({args[0]} {self.T["ops"].get(op, op)} {args[1]})'
        if key == 'not' and len(args) == 1: return f'({self.T["not"]}{args[0]})'
        if (key in ('item',) or name in ('getitem', 'item_at', 'at')) and len(args) == 2: return f'{args[0]}[{args[1]}]'
        if key == 'contain' and len(args) == 2:
            return f'(Array.isArray({args[0]}) ? {args[0]}.includes({args[1]}) : ({args[1]} in {args[0]}))' if js else f'({args[1]} in {args[0]})'
        if name == 'put' and len(args) == 3:
            return f'{{...{args[0]}, [{args[1]}]: {args[2]}}}' if js else f'{{**{args[0]}, {args[1]}: {args[2]}}}'
        if name == 'rest' and len(args) == 1: return f'{args[0]}.slice(1)' if js else f'{args[0]}[1:]'
        if key == 'count' and len(args) == 1: return f'{args[0]}.length' if js else f'len({args[0]})'
        if name == 'append' and len(args) == 2: return f'[...{args[0]}, {args[1]}]' if js else f'({args[0]} + [{args[1]}])'
        return f"{name}({', '.join(args)})"

    def py_expr(self, p):
        us = [self.py_unit(u) for u in p['units']]
        out = us[0]
        for op, u in zip(p['ops'], us[1:]):
            out += {'AND': self.T['and'], 'OR': self.T['or'], 'XOR': self.T['xor']}[op] + u
        return out

    def py_unit(self, u):
        h = u['head']; k = h.get('k') or h['t']
        slots = [r for r in u.get('roles', []) if r['role'] in SLOTN]
        if k == 'paren' and not u['mods'] and not slots:
            inner = '(' + self.py_expr(h['phrase']) + ')' if len(h['phrase']['units']) > 1 else self.py_expr(h['phrase'])
            return (self.T['not'] if u.get('neg') else '') + inner
        if k == 'block':
            return self.py_cond(h)
        name = self.py_name(u)
        if getattr(self, 'pynames', None) and name in self.pynames: name = self.pynames[name]
        if slots:
            args = [self.py_expr(r['phrase']) for r in sorted(slots, key=lambda r: SLOTN.index(r['role']))]
            key = self.py_key(h) if k == 'R' else (h['v'] if k == 'P' else None)
            txt = self.py_call(name, key, args)
        else:
            txt = name
        for m in u['mods']:
            if m['link'] == 'OF':
                txt = self.py_unit(m['unit']) + '.' + txt
        return (self.T['not'] if u.get('neg') else '') + txt

    def py_cond(self, b):
        st = b['stmts'][0]; body = st['body']
        if body['k'] == 'frag' and 'phrase' in body: return self.py_expr(body['phrase'])
        if body['k'] == 'clause':
            return self.py_clause(body)
        if body['k'] == 'cjoin' and all(p['k'] == 'clause' for p in body['parts']):
            out = self.py_clause(body['parts'][0])
            for (op, _), p in zip(body['ops'], body['parts'][1:]):
                out += {'ANDC': self.T['and'], 'ORC': self.T['or'], 'BUT': self.T['and']}[op] + self.py_clause(p)
            return '(' + out + ')'
        raise L.LangError('cannot turn this block into a Python expression')

    def py_clause(self, c):
        pred = c['pred']; neg = any(n == 'NOT' for n, _ in c['pre'])
        slots = [r for r in c['roles'] if r['role'] in SLOTN]
        args = [self.py_expr(r['phrase']) for r in sorted(slots, key=lambda r: SLOTN.index(r['role']))]
        if pred['k'] == 'ppred': txt = self.py_expr(pred['phrase'])
        elif pred['k'] == 'dpred':
            a = [r for r in c['roles'] if r['role'] == 'THEME']; b = [r for r in c['roles'] if r['role'] == 'THAN']
            op = PYOP[pred["deg"]]; op = self.T['ops'].get(op, op)
            if args: txt = f'({args[0]} {op} {args[1]})'
            else: txt = f'({self.py_expr(a[0]["phrase"])} {op} {self.py_expr(b[0]["phrase"])})'
        else:
            u = pred['unit']; name = self.py_name(u)
            if getattr(self, 'pynames', None) and name in self.pynames: name = self.pynames[name]
            key = self.py_key(u['head'])
            txt = self.py_call(name, key, args)
            for m in u['mods']:
                if m['link'] == 'OF': txt = self.py_unit(m['unit']) + '.' + txt
        return (self.T['not'] if neg else '') + txt

    def py_stmt(self, s, ind=0):
        pad = '    ' * ind; b = s['body']; k = b['k']; js = self.tgt == 'javascript'; end = self.T['end']
        if k == 'define':
            name = self.py_name(b['term']['units'][0])
            vu = b['val']['units'][0]
            if vu['head'].get('t') == 'N' and not b['params'] and len(b['val']['units']) == 1 and \
                    re.fullmatch(r'[A-Za-z_][\w.]*', vu['head']['v']) and b['term']['units'][0]['head'].get('t') != 'H':
                self.pynames[name] = vu['head']['v']       # naming line: DEFINE (sum KIND even) BE «sum_even»
                return []
            name = self.pynames.get(name, name)
            if b['params'] or vu['head'].get('k') == 'block' and len(vu['head']['stmts']) > 1:
                params = [self.hname(p).lower() for p in b['params']]
                outer = self.declared; self.declared = set(params)
                body = []
                if vu['head'].get('k') == 'block':
                    for st in vu['head']['stmts']: body += self.py_stmt(st, ind + 1)
                else:
                    body.append(pad + '    return ' + self.py_expr(b['val']) + end)
                self.declared = outer
                return self.blk(pad, ('function ' if js else 'def ') + f"{name}({', '.join(params)})", body)
            let = ''
            if js and name not in self.declared: let = 'let '; self.declared.add(name)
            return [f'{pad}{let}{name} = {self.py_expr(b["val"])}{end}']
        if k == 'if':
            then = []; other = []
            for st in b['then']['stmts']: then += self.py_stmt(st, ind + 1)
            if b['else']:
                for st in b['else']['stmts']: other += self.py_stmt(st, ind + 1)
            cond = self.py_cond(b["cond"])
            lines = self.blk(pad, f'if ({cond})' if js else f'if {cond}', then, cont=bool(other))
            if other: lines += self.blk(pad, '} else' if js else 'else', other)
            return lines
        if k == 'each':
            v = self.hname(b['var']).lower(); self.declared.add(v); body = []
            for st in b['do']['stmts']: body += self.py_stmt(st, ind + 1)
            return self.blk(pad, f"for (const {v} of {self.py_expr(b['in'])})" if js else f"for {v} in {self.py_expr(b['in'])}", body)
        if k == 'while':
            body = []; cond = self.py_cond(b["cond"])
            for st in b['do']['stmts']: body += self.py_stmt(st, ind + 1)
            return self.blk(pad, f'while ({cond})' if js else f'while {cond}', body)
        if k == 'return': return [pad + 'return ' + self.py_expr(b['val']) + end]
        if k == 'clause': return [pad + self.py_clause(b) + end]
        if k == 'frag' and 'phrase' in b: return [pad + self.py_expr(b['phrase']) + end]
        raise L.LangError('not a logic statement')

    def head_target(self, s):
        """A heading such as  HEAD code KIND «javascript»  declares the language of the code that follows."""
        b = s['body']
        if s.get('head', {}).get('opener') == 'CODE':
            v = b['phrase']['units'][0]['head']['v'].strip().lower()
            return TARGET_ALIASES.get(v, v)
        if s.get('head', {}).get('opener') != 'HEAD' or b['k'] != 'frag' or 'phrase' not in b: return None
        for u in b['phrase']['units']:
            if u['head'].get('t') == 'R' and u['head']['v'] in ('code', 'program', 'language'):
                for m in u['mods']:
                    h = m['unit']['head']
                    if h.get('t') == 'N':
                        return TARGET_ALIASES.get(h['v'].strip().lower(), h['v'].strip().lower())
        return None

    def python(self, sents, target=None):
        self.pynames = {}; self.declared = set()
        self.tgt = target if target in TARGETS else 'python'
        lines = []
        for s in sents:
            if s is None: continue
            if s.get('head', {}).get('opener') == 'IMPORT':
                u = s['body']['phrase']['units'][0]; lib = u['head']['v']; al = self.hname(u['named']).lower()
                self.declared.add(al)
                lines.append(f"import * as {al} from '{lib}';" if self.tgt == 'javascript' else f'import {lib} as {al}')
                continue
            t = self.head_target(s)
            if t:
                if t in TARGETS:
                    self.tgt = t; lines.append(self.T['comment'] + '--- ' + t + ' ---')
                else:
                    lines.append(self.T['comment'] + f'--- declared language «{t}» has no converter; shown as {self.tgt} ---')
                continue
            if s['body']['k'] != 'define': continue
            b = s['body']; vu = b['val']['units'][0]
            if not (b['params'] or vu['head'].get('t') == 'N' or vu['head'].get('k') == 'block' or b['term']['units'][0]['head'].get('t') == 'H'):
                continue                                   # a prose definition of a word, not logic
            try: lines += self.py_stmt(s)
            except Exception as e: lines.append(self.T['comment'] + 'could not translate one definition: ' + str(e))
        return '\n'.join(lines)


def translate(text, mode='native', lex=None, hletter=None):
    r = L.parse(text, mode, lex)
    d = Decoder(lex, hletter)
    out = []
    for n, (s, chunk) in enumerate(zip(r['sentences'], r['chunks']), 1):
        if s is None:
            out.append('⟨could not parse: ' + ' '.join(L._show(t) for t in chunk) + '⟩')
        else:
            try: out.append(d.sentence(s))
            except Exception as e:      # translator bug: never lose the sentence silently
                out.append('⟨translator error ' + type(e).__name__ + ': ' + ' '.join(L._show(t) for t in chunk) + '⟩')
    return out, r


if __name__ == '__main__':
    import sys
    mode = sys.argv[1]; text = open(sys.argv[2], encoding='utf-8').read()
    out, r = translate(text, mode)
    for o in out: print(o)
    for n, e in r['errors']: print(f'!! sentence {n}: {e}')
    if len(sys.argv) > 3:      # 'py' or a language name: code for the definitions (a heading in the text overrides it)
        print(Decoder().python(r['sentences'], TARGET_ALIASES.get(sys.argv[3], sys.argv[3])))
