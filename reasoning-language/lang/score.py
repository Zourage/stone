import sys, collections
import lang as L, english as E
def score(path):
    text=open(path,encoding='utf-8').read()
    out,r=E.translate(text,'native')
    n=len(r['sentences']); bad=sum(1 for s in r['sentences'] if s is None)
    toks=r['tokens']; c=collections.Counter(t['t'] for t in toks)
    words=sum(c[k] for k in 'PRHLND')
    ops=collections.Counter(t['v'] for ch in r['chunks'] for t in ch[:3] if t['t']=='P' and L.CLS[t['v']]=='opener')
    print(f'{path.split("/")[-1]}: {n} sentences, {bad} unparsed, {len(r["errors"])} messages; words {words}: particles {c["P"]}, roots {c["R"]}, loans {c["L"]}, notation {c["N"]}, handles {c["H"]}; unknown roots {sum(1 for t in toks if t.get("unknown"))}, bad tokens {c["BAD"]}')
    print('  openers:',dict(ops))
    return out,r
if __name__=='__main__':
    for p in sys.argv[1:]:
        out,r=score(p)
        for n,e in r['errors']: print('   !!',n,e[:200])
        open(p.replace('.txt','.en.txt'),'w').write('\n'.join(out)+'\n')
