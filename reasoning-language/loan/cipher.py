import random,json,sys
INI='ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'; VOW='ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
cons=list('bcdfghjklmnpqrstvz'); vows=list('aeiouwyx')
r=random.Random(7)
ci=[c for c in INI if c!='ㅇ']; r.shuffle(ci)
vi=list('ㅏㅓㅗㅜㅡㅣㅐㅔㅑ'); r.shuffle(vi)
C=dict(zip(cons,ci)); V=dict(zip(vows+[''],vi))
def blk(i,v): return chr(0xAC00+(INI.index(i)*21+VOW.index(v))*28)
def enc(w):
    w=w.lower(); out=[]; k=0
    while k<len(w):
        a=w[k]
        if a in C:
            if k+1<len(w) and w[k+1] in V: out.append(blk(C[a],V[w[k+1]])); k+=2
            else: out.append(blk(C[a],V[''])); k+=1
        else: out.append(blk('ㅇ',V[a])); k+=1
    return ''.join(out)
Ci={v:k for k,v in C.items()}; Vi={v:k for k,v in V.items()}
def dec(s):
    o=''
    for ch in s:
        n=ord(ch)-0xAC00; i=INI[n//28//21]; v=VOW[n//28%21]
        o+=(Ci[i] if i!='ㅇ' else '')+Vi[v]
    return o
if __name__=='__main__':
    E='python kubernetes server database darwin tortoise grape photosynthesis mutex cache linux entropy hooker fedora seattle algorithm json widget quartz xylophone benchmark yield socrates netherfield inflation cascade chromatic zeta rhythm ok'.split()
    D='lambda docker euclid hamlet glucose kernel washington pointer sparse vector oxygen bennet moccasin trellis hypotenuse antiferromagnetic graphene sodium tensor whiskey jazz vortex queue squirrel exception toolkit bayes fjord zebra knight'.split()
    for w in E+D: assert dec(enc(w))==w,w
    t='# Loan spelling table\n\nEach English letter maps to one Hangul part. Consonant-class letters map to an initial consonant; vowel-class letters map to a vowel. (Note: w, y and x are in the vowel class.)\n\n'
    t+='Consonant-class letters -> initial:\n'+', '.join(f'{k}={v}' for k,v in C.items())+'\n\nVowel-class letters -> vowel:\n'+', '.join(f'{k}={v}' for k,v in V.items() if k)+f"\n\nNo vowel-class letter follows -> vowel {V['']}\nNo consonant-class letter before -> initial ㅇ\n\n"
    t+='''## Encoding rule
Lowercase the word. Scan left to right. A consonant-class letter immediately followed by a vowel-class letter shares ONE block with it (initial + vowel). A consonant-class letter NOT followed by a vowel-class letter gets its own block with the "no vowel" vowel. A vowel-class letter not consumed by a preceding consonant gets its own block with initial ㅇ. Blocks have no final consonant.

## Decoding rule
For each block: write the letter of its initial (nothing for ㅇ), then the letter of its vowel (nothing for the "no vowel" vowel).

Example: "'''+'stack'+'" -> '+enc('stack')+'\n'
    open('table.md','w').write(t)
    open('tasks.md','w').write('# Part 1: encode these 30 English words\n'+'\n'.join(E)+'\n\n# Part 2: decode these 30 forms to English letters\n'+'\n'.join(enc(w) for w in D)+'\n')
    json.dump({'E':E,'D':D},open('key.json','w'))
    print(t); print(enc('python'),enc('test'),enc('kubernetes'),len(enc('photosynthesis')))
