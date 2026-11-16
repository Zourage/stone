"""Merge the four drafted root lists, assign forms, write lexicon.json."""
import json, collections, sys
import forms as F
RENAME={('B','nail'):'pin',('B','tear'):'rip',('B','load'):'cargo',('D','map'):'assign',('B','step'):'pace',('C','train'):'railway'}
PREFER={'contain':'B','group':'C','sign':'C','limit':'B','range':'B','rate':'B','surface':'B','target':'B','blow':'B','strong':'B','increase':'B','map':'B','nail':'A','tear':'A','load':'D','step':'D','train':'D'}
ORDER='DBCA'
roots={}; src={}
allrows=collections.defaultdict(dict)
for p in 'ABCD':
    for l in open(f'lex_{p}.tsv',encoding='utf-8'):
        c=l.rstrip('\n').split('\t')
        g=RENAME.get((p,c[0]),c[0])
        allrows[g][p]=c
for g,v in allrows.items():
    p=PREFER.get(g) if PREFER.get(g) in v else next(x for x in ORDER if x in v)
    c=v[p]
    roots[g]={'type':c[1],'tr':int(c[2]),'noun':c[3],'adj':c[4],'rel':c[5],'field':c[6],'def':c[7]}
    src[g]=p
EXTRA={ # gloss: type,tr,noun,adj,rel,field,def
 'ago':('R',0,'','','~ago','time','before now by the stated amount: ago REL 2 day'),
 'ok':('Q',0,'','','','speech','acceptable; all right'),
 'clause':('T',0,'','','','writing','part of a sentence with its own predicate'),
 'object':('T',0,'','','','reasoning','a thing; an instance in a program'),
 'position':('T',0,'','','','space','where something is placed; rank'),
 'perform':('A',1,'performance','','','work','carry out; how well something does'),
 'form':('T',0,'','formal','','reasoning','the arrangement or outward pattern of something'),
 'view':('T',0,'','','','reasoning','way of regarding something; opinion; what is seen'),
}
for g,(t,tr,n,a,r,f,d) in EXTRA.items():
    if g not in roots: roots[g]={'type':t,'tr':tr,'noun':n,'adj':a,'rel':r,'field':f,'def':d}
derived={}; conflicts=[]
for p in 'ABCD':
    for l in open(f'der_{p}.tsv',encoding='utf-8'):
        c=l.rstrip('\n').split('\t')
        if len(c)<3: continue
        base=RENAME.get((p,c[0]),c[0]); suf=c[1].lstrip('.'); eng=c[2]
        if base not in roots: conflicts.append(('nobase',p,c)); continue
        key=base+('+agent' if suf=='+agent' else '.'+suf)
        if suf!='+agent' and suf not in F.SUFFIXES: conflicts.append(('badsuf',p,c)); continue
        if key in derived and derived[key]!=eng: conflicts.append(('clash',key,derived[key],eng)); continue
        derived[key]=eng
MANUAL={'serve.tool':'server','serve.doer':'servant','do.opp':'undo','configure.made':'setting','change+agent':'change','open+agent':'open','accept.opp':'reject','work.place':'office','store.place':'storage','normal.opp':'abnormal','increase+agent':'increase','number.group':'set of numbers','ago.opp':'from now','before.opp':'after'}
MANUAL.update({'say.made':'statement','extend.made':'extension','expect.made':'expectation','get.doer':'recipient',
 'execute.doer':'implementer','execute.made':'implementation','report.made':'report','have.made':'holding','specify.made':'specification',
 'maintain.doer':'maintainer','send.doer':'sender','contain.made':'content','mix.made':'mixture','write.made':'text'})
_rootgloss=set(roots)
derived={k:v for k,v in derived.items() if not (v in _rootgloss and not k.startswith(v))}   # a root already says it: prefer the root
derived.update({k:v for k,v in MANUAL.items() if k.split('.')[0].split('+')[0] in roots})
gl=sorted(roots)
fs=F.root_forms(len(gl)+80,seed=11)
import random
random.Random(5).shuffle(fs)
for g,f in zip(gl,fs): roots[g]['form']=f
spares=fs[len(gl):]
LATE2 = """up|Q|0|||space|toward the higher place; against gravity
down|Q|0|||space|toward the lower place; with gravity
earth|T|0|||nature|the planet we live on; also the ground
man|T|0|||person|adult male person
woman|T|0|||person|adult female person
mother|T|0||maternal|person|female parent
father|T|0||paternal|person|male parent
centre|T|0||central|space|the middle point or part
opposite|Q|0|||relation|facing or going the other way; as different as possible
kidney|T|0||renal|body|organ that filters the blood and makes urine
nerve|T|0||neural|body|fibre that carries signals in the body; nerve.ness KIND cell is a neuron
vessel|T|0||vascular|body|tube that carries blood or another fluid in a body
gland|T|0|||body|organ that makes and gives out a substance
hormone|T|0||hormonal|body|signal substance carried in the blood
drug|T|0|||medicine|substance given to treat or to change how the body works
inject|A|1|injection||medicine|push a liquid into a body through a needle
diagnose|A|1|diagnosis||medicine|find out which illness someone has
treat|A|1|treatment||medicine|give care or medicine against an illness
ion|T|0||ionic|science|atom or molecule with an electric charge
bond|T|0|||science|chemical bond: the link holding two atoms together
bind|A|1|binding|bound|science|attach to something and hold it (as a molecule to a receptor)
release|A|1|release||action|let go of something held; set free
attract|A|1|attraction||science|pull toward itself
repel|A|1|repulsion||science|push away from itself
concentrate|Q|0|concentration|concentrated|science|having much of a substance per volume; the noun is the amount per volume
compound|T|0|||science|substance made of two or more elements bonded together
crystal|T|0||crystalline|science|solid whose particles lie in a regular repeating pattern
catalyst|T|0||catalytic|science|substance that speeds a reaction and is not used up
enzyme|T|0||enzymatic|science|protein that works as a catalyst in living things
receptor|T|0|||science|molecule or cell part that a signal substance binds to
membrane|T|0|||science|thin layer that separates two spaces, as around a cell
solvent|T|0|||science|liquid in which something is dissolved
accelerate|A|1|acceleration||science|change the speed of something; without THEME, gain speed
voltage|T|0|||science|difference of electric potential between two points
current|T|0|||science|flow of electric charge (or of a fluid)
spin|T|0|||science|the built-in angular momentum of a particle; not ordinary turning
proportional|Q|0|proportion||mathematics|changing by the same factor as something else (THAN the other quantity)
gradient|T|0|||science|how fast a quantity changes from place to place; a difference across a distance
equilibrium|T|0|||science|state in which opposite processes go on at equal rates, so nothing changes overall
pump|A|1|pump||science|move a fluid or particles by force, often against a gradient
mutation|T|0||mutant|science|change in the sequence of a gene
threshold|T|0|||science|the level a quantity must pass for an effect to happen
inhibit|A|1|inhibition||science|make a process slower or weaker, or stop it
peak|T|0|||shape|the highest point of a curve, signal or hill
crash|A|0|crash||computing|stop working suddenly (of a program or machine)
restart|A|1|restart||computing|stop and start again
after|R|0|||time|later than (after REL x); x may be a thing, a time or a { } clause
until|R|0|||time|up to the time of (until REL x); x may be a time or a { } clause
wrong|Q|0|error||truth|not correct; mistaken
vaccine|T|0|||medicine|substance given to train the immune system against a disease"""
LATE={'quotient':('T',0,'','','','mathematics','whole-number result of a division: quotient FIRST 7 SECOND 2 is 3')}
for _l in LATE2.split('\n'):
    g,t,tr,n,a_,f,d=_l.split('|'); LATE[g]=(t,int(tr),n,a_,{'after':'after','until':'until'}.get(g,''),f,d)
for g,(t,tr,n,a_,r,f,d) in LATE.items():      # added after forms were dealt: take a spare from the end so no existing form moves
    roots[g]={'type':t,'tr':tr,'noun':n,'adj':a_,'rel':r,'field':f,'def':d,'form':spares.pop()}
roots['percent']['noun']='percent'

json.dump({'roots':roots,'derived':derived,'spares':spares},open('lexicon.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(roots),'roots',len(derived),'derived',len(spares),'spares')
print(collections.Counter(r['type'] for r in roots.values()))
if '-v' in sys.argv:
    for c in conflicts: print(c)
    eng=collections.defaultdict(list)
    for k,v in derived.items(): eng[v].append(k)
    print('same english, two derivations:',{k:v for k,v in eng.items() if len(v)>1})
    print('derived word that is also a root:',[ (k,v) for k,v in derived.items() if v in roots])
