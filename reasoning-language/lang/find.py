import json,sys,re
lx=json.load(open(__file__.rsplit('/',1)[0]+'/lexicon.json'))
for w in sys.argv[1:]:
    hits=[f"{g}({e['type']}) {e['def']}" for g,e in lx['roots'].items() if g==w or re.search(r'\b'+w+r'\b',e['def']) or w in (e['noun'],e['adj'])]
    hits+=[f"{k}={v}" for k,v in lx['derived'].items() if re.search(r'\b'+w+r'\b',v)]
    print(w,'->',' ; '.join(hits[:8]) or 'NONE')
