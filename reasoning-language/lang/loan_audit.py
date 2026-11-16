"""Per file: sentences, refusals, loan terms (decoded), « » items outside code split into allowed kinds and leaks."""
import sys, re, glob, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import lang as L

def audit(f):
    r = L.parse(open(f, encoding='utf-8').read())
    out = collections.defaultdict(list)
    for ch in r['chunks']:
        incode = any(t['t'] == 'P' and t['v'] in ('DEFINE', 'IMPORT', 'CODE') for t in ch[:4])
        i = 0
        while i < len(ch):
            t = ch[i]
            if t['t'] == 'L':
                ws = [t['v']]; j = i + 1
                while j < len(ch) and (ch[j]['t'] in ('L', 'D') or (ch[j]['t'] == 'N' and len(ch[j]['v']) <= 2)): ws.append(ch[j]['v']); j += 1
                out['loan'].append(' '.join(ws)); i = j; continue
            if t['t'] == 'N' and not incode:
                v = t['v']; prev = ch[i - 1] if i else {'t': ''}
                if prev.get('t') == 'P' and prev.get('v') == 'CODE': out['codemention'].append(v)
                elif prev.get('t') == 'D': out['unit'].append(v)
                elif L.is_formula(v) and re.search(r'[A-Z]', v): out['formula'].append(v)
                elif re.search(r'[A-Za-z]{4,}', v): out['LEAK_word'].append(v)
                elif re.fullmatch(r'[A-Z]{2,3}\d*', v): out['leak_abbrev'].append(v)
                else: out['symbol'].append(v)
            i += 1
    return r, out

if __name__ == '__main__':
    T = collections.Counter()
    for f in sorted(sys.argv[1:]):
        r, o = audit(f)
        print(f"== {f.split('/')[-1]}: {len(r['chunks'])} sentences, {len(r['errors'])} refusals; loans {len(o['loan'])} ({len(set(o['loan']))} distinct); "
              f"formula {len(o['formula'])}, unit {len(o['unit'])}, symbol {len(o['symbol'])}, word-leak {len(o['LEAK_word'])}, abbrev-leak {len(o['leak_abbrev'])}")
        for k in ('LEAK_word', 'leak_abbrev'):
            if o[k]: print('   ', k, sorted(set(o[k]))[:25])
        if '-v' in sys.argv[1:]: pass
        T['sent'] += len(r['chunks']); T['refused'] += len(r['errors'])
        for k in o: T[k] += len(o[k])
    print(dict(T))
