import subprocess,sys,random
for x in "abc":
    out=subprocess.run(["python3","english.py","native",f"../test4/T3_{x}.txt","py"],capture_output=True,text=True).stdout
    code=out[out.index("def "):]
    ns={}
    try:
        exec(code,ns)
        fn=[v for k,v in ns.items() if callable(v) and k not in('w1',) ] or [ns.get('w1')]
        names=[k for k in ns if not k.startswith('__')]
        m=[ns[k] for k in names if ns[k].__code__.co_argcount==2][0]
        ok=all(m(sorted(a),sorted(b))==sorted(a+b) for a,b in [([random.randint(0,9) for _ in range(random.randint(0,6))],[random.randint(0,9) for _ in range(random.randint(0,6))]) for _ in range(300)])
        s=[ns[k] for k in names if ns[k].__code__.co_argcount==1]
        sq = all(s[0](n)==n*n for n in range(0,20)) if s else None
        print(x,"defs:",names,"merge correct:",ok,"sum-of-odds == n^2:",sq)
    except Exception as e: print(x,"ERR",repr(e)[:200]); print(code[-400:])
