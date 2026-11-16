import lang,sys
tot=0
for f in [a for a in sys.argv[1:] if a!="-q"]:
    r=lang.parse(open(f,encoding="utf-8").read())
    for n,e in r['errors']:
        tot+=1
        if '-q' in sys.argv: continue
        print("==",f.split('/')[-1],n,e[:90]); print("   ",lang.to_gloss(r['chunks'][n-1])[:700] if n else '')
print("total messages",tot)
