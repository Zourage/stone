"""Generate the model-facing rule sheet (SPEC.md) and word list (WORDS.md) from the data,
so every form and every example in them is correct by construction."""
import re, json
import forms as F, lang as L, english as E

PT = L.PT
lex = L.LEX

MEAN = {
 # openers
 'GIVEN': 'I observe it in the context myself (a file, a tool result, what is in front of me)',
 'TOLD': 'another party says so and I have not checked; a handle may follow to name who',
 'DERIVED': 'follows from earlier sentences; their labels follow. With no labels: inferred from unstated evidence ("apparently")',
 'RECALLED': 'from my background knowledge',
 'ASSUMED': 'supposed for the sake of argument, not claimed',
 'CLAIM': 'I assert it and give no source (also my own states: I think, I prefer, I do not know)',
 'STORY': 'narrated as part of a story or scenario, not asserted as fact',
 'RULE': 'holds because it is laid down here (law, standard, policy)',
 'ASK': 'a question. YES or NO may follow: the answer expected',
 'REQUEST': 'asks or instructs someone to act; with no AGENT the addressee acts',
 'PROPOSE': 'suggests an action without instructing ("let us", "you could")',
 'PLAN': 'commits to act; with no AGENT the writer acts',
 'DEFINE': 'DEFINE term BE meaning. Also binds spare words and logic names',
 'SOCIAL': 'a social act done by saying it: thanks, greeting, apology, agreement. A bare root follows',
 'HEAD': 'a title or heading; a bare phrase follows',
 'CONSIDER': 'a thought being weighed; the writer does not commit to it being true or false',
 'IMPORT': 'code: bring in a library and give it a handle, `IMPORT «numpy» NAMED N`',
 'CODE': 'code: the programming language of the code that follows, `CODE «python»`',
 # relations
 'CONTRAST': 'differs from or opposes the target', 'CONCEDE': 'holds even though the target holds',
 'RESULT': 'is a consequence of the target', 'EVIDENCE': 'is my ground for believing the target',
 'EXPLAIN': 'says why the target is so', 'ADD': 'a further point alongside the target',
 'SEQUENCE': 'the next event after the target', 'EXAMPLE': 'an instance of the target',
 'DETAIL': 'spells out part of the target', 'RESTATE': 'says the target again in other words; sums up',
 'BACKGROUND': 'sets the scene for the target', 'ASIDE': 'off the main line',
 'UNDER': 'holds only inside the supposition made in the target', 'ANSWER': 'answers the question in the target',
 'REBUT': 'denies the target, or something the reader is presumed to think',
 'RETRACT': 'withdraws or replaces the target: I no longer hold it',
 'CERTAIN': 'I am sure', 'LIKELY': 'probably', 'POSSIBLE': 'maybe',
 'SURPRISE': 'unexpected to me', 'EMPHASIS': 'stressed', 'POLITE': 'politely', 'REGRET': 'I am sorry that',
 'GLAD': 'I am glad that', 'ANNOYED': 'irritated', 'JEST': 'said playfully', 'IRONY': 'meant otherwise than the literal words',
 'META': 'a note about this text itself, not about its subject (the writer stepping outside)',
 'FRANK': 'speaking bluntly', 'HOPE': 'I hope that', 'FEAR': 'I fear that',
 'NOT': 'negates everything to its right in its group', 'PAST': 'before the reference time', 'FUTURE': 'after the reference time',
 'NOW': 'at present (use only to contrast with another time); also a head: "now"', 'UNREAL': 'in a supposed world, not the actual one ("would", "were")',
 'NEAR': 'after PAST or FUTURE: just now / soon', 'FAR': 'after PAST or FUTURE: long ago / far ahead',
 'MUST': 'required', 'SHOULD': 'advised', 'MAY': 'permitted', 'CAN': 'able, or possible in fact',
 'WANT': 'the AGENT wants to', 'TRY': 'the AGENT tries to',
 'ONGOING': 'in progress', 'DONE': 'finished and the result holds', 'HABIT': 'as a habit or regular practice',
 'BEGIN': 'starts; with a state: becomes', 'STOP': 'ceases', 'STILL': 'continues', 'AGAIN': 'once more',
 'ALREADY': 'by now (NOT ALREADY = not yet)', 'FINALLY': 'after a long wait', 'OFTEN': 'often', 'RARE': 'rarely',
 'SOMETIMES': 'sometimes', 'ALWAYS': 'always', 'NEVER': 'never',
 'TIMES': 'counts occurrences; a number or amount word comes before it: 3 TIMES, MANY TIMES',
 'VERY': 'very', 'SLIGHT': 'somewhat', 'FULL': 'completely', 'BARELY': 'hardly', 'ALMOST': 'almost',
 'ENOUGH': 'enough (FOR ...)', 'TOO': 'too (FOR ...)', 'MORE': 'more (THAN ...)', 'LESS': 'less (THAN ...)',
 'MOST': 'most (THAN the set compared)', 'LEAST': 'least', 'EQUAL': 'as ... as (THAN ...); alone as predicate: is identical to',
 'ONLY': 'only', 'ALSO': 'also', 'EVEN': 'even', 'INSTEAD': 'instead', 'MAINLY': 'mostly, especially',
 'FOCUS': 'this one, not another (contrastive stress; "itself")', 'TOPIC': 'what the sentence is about',
 'YES': 'yes; true', 'NO': 'no; false', 'EMPTY': 'nothing; the empty value',
 'AGENT': 'who controls the act or brings it about; who knows, sees, wants or has',
 'THEME': 'what is acted on, perceived or described; what a thing happens to',
 'TO': 'recipient, end point, or resulting state', 'FROM': 'origin', 'AT': 'place', 'WHEN': 'point in time',
 'WITH': 'means or manner', 'CAUSE': 'cause or reason', 'FOR': 'purpose or beneficiary',
 'THAN': 'standard of comparison; with no degree word: "like". A role particle may follow to say which participant is compared',
 'ABOUT': 'topic, field or respect', 'AS': 'capacity, role or viewpoint', 'ALONG': 'companion',
 'SPAN': 'duration, extent, or size of a difference', 'EXCEPT': 'what the statement does not cover (with a block: unless)',
 'DESPITE': 'what would have been expected to prevent it (with a block: although)', 'VIA': 'path or thing passed through',
 'PER': 'for each one of: 3 tries PER request', 'SWAP': 'what is replaced or given in exchange (instead of; price paid)',
 'KIND': 'narrows the head: type, material, content, quality. After a predicate: manner',
 'OF': 'owner, or the whole a part belongs to', 'REL': 'the second thing a relational root needs: before REL x, cause REL x, friend REL x',
 'NOTE': 'adds a comment that does not narrow; with a phrase: "namely" (the full list)',
 'HAVING': 'what the head has (the reverse of OF): function HAVING 2 parameter', 'SUCHAS': 'examples, not a full list',
 'AND': 'joins phrases: and', 'OR': 'joins phrases: or (one or both)', 'XOR': 'joins phrases: exactly one of',
 'ANDC': 'joins clauses: and. A relation may follow it', 'ORC': 'joins clauses: or', 'BUT': 'joins clauses: but',
 'NAMED': 'binds the handle that follows to this thing', 'BY': 'whose words this sentence or block is',
 'CALL': 'in the header: names the person addressed', 'NAME': 'the next word is a proper name',
 'BE': 'in DEFINE: separates term and meaning. As a predicate: empty "is" for role phrases',
 'IF': 'IF {condition} {then} {else}', 'EACH': 'EACH handle IN phrase {block}: for each', 'IN': 'see EACH',
 'WHILE': 'WHILE {condition} {block}', 'RETURN': 'gives back a value (logic)',
 'STEP': 'refers to a numbered sentence: STEP 3', 'UPTO': 'range between two numbers or labels: 3 UPTO 5',
 'ALL': 'every one', 'MAJOR': 'most of', 'MANY': 'many; much', 'SEVERAL': 'more than one', 'SOME': 'at least one; some',
 'FEW': 'few; little', 'NONE': 'no; none', 'ANY': 'whichever (no existence implied)',
 'GENERIC': 'the kind in general (exceptions allowed)', 'WHOLE': 'the set taken together, not each member',
 'THAT': 'the one the reader can identify', 'THIS': 'the one present or just pointed at', 'OTHER': 'a different one',
 'SAME': 'the same one', 'SPECIFIC': 'a particular one I have in mind', 'ORD': 'ORD 3 = the third',
 'AROUND': 'about, roughly (before a number or a quality)', 'EXACT': 'exactly', 'ATLEAST': 'at least', 'ATMOST': 'at most',
 'ABOVE': 'more than (a number)', 'BELOW': 'fewer than (a number)',
 'ME': 'the writer (inside a BY block: that speaker)', 'YOU': 'the addressee', 'US': 'the writer\'s group, without the addressee', 'WE': 'the writer and the addressee together',
 'SELF': 'in a modifying block: the head. Elsewhere: the AGENT of its own clause', 'MUTUAL': 'each other',
 'WHAT': 'question word. Before a head: which. WHAT MANY: how many. Before a quality: how',
 'FIRST': 'first slot of a logic function', 'SECOND': 'second slot', 'THIRD': 'third slot', 'FOURTH': 'fourth slot',
}
assert set(MEAN) == set(PT), set(PT) ^ set(MEAN)

CLASS_TITLE = [
 ('opener', 'Openers: what kind of statement this is (first word of every sentence)'),
 ('relation', 'Relations: how this sentence relates to another (after the opener; label numbers may follow)'),
 ('strength', 'Strength: how sure the writer is'), ('attitude', 'Attitude'),
 ('time', 'Negation and time'), ('modal', 'Modals'), ('aspect', 'Aspect: how the event unfolds'),
 ('degree', 'Degree'), ('focus', 'Focus'), ('value', 'Values'),
 ('role', 'Roles: each stands before its phrase'), ('linker', 'Linkers: attach a modifier to the word before'),
 ('conj', 'Joiners'), ('struct', 'Structure words'), ('quant', 'Amount and reference words: before the head'),
 ('nummod', 'Number modifiers'), ('head', 'Person and question words, logic slots'),
]


def nat(gloss, hmap=None):
    toks, errs = L.tokens_gloss(gloss)
    assert not errs, (gloss, errs)
    return L.to_native(toks, hmap=hmap).strip()


def exblock(glosses):
    """Examples: native line, name line, English line (from the translator, whole block in one context)."""
    hmap = {}
    n = nat('\n'.join(glosses), hmap)
    out, r = E.translate(n, 'native', hletter={v: k for k, v in hmap.items()})
    assert not r['errors'], (glosses, r['errors'])
    nl = [x.strip() for x in n.split('\n')]
    assert len(nl) == len(glosses) == len(out), (len(nl), len(glosses), len(out), glosses)
    lines = []
    for a_, g, en in zip(nl, glosses, out):
        lines += [a_, '    ' + g, '    = ' + en, '']
    return '```\n' + '\n'.join(lines).rstrip() + '\n```'


def ptable(cls):
    rows = [(n, PT[n][1]) for n in PT if PT[n][0] == cls]
    return '| Form | Name | Meaning |\n|---|---|---|\n' + '\n'.join(f'| {f} | {n} | {MEAN[n]} |' for n, f in rows)


def build_spec():
    T = open(L.HERE + '/spec_template.md', encoding='utf-8').read()
    T = re.sub(r'\{\{table:(\w+)\}\}', lambda m: ptable(m.group(1)), T)
    T = re.sub(r'\{\{alltables\}\}', lambda m: '\n\n'.join(f'### {t}\n\n{ptable(c)}' for c, t in CLASS_TITLE), T)

    def exrep(m):
        gl = [x.strip() for x in m.group(1).strip().split('\n') if x.strip()]
        return exblock(gl)
    T = re.sub(r'\{\{ex\n(.*?)\}\}', exrep, T, flags=re.S)
    T = re.sub(r'\{\{n:([^}]*)\}\}', lambda m: nat(m.group(1)), T)
    T = T.replace('{{suffixes}}', '| Suffix | Name | Meaning | Example |\n|---|---|---|---|\n' + '\n'.join(
        f'| {F.SUFFIX_FORMS[s]} | {s} | {d} | {e} |' for s, d, e in [
            ('opp', 'the opposite pole; the act that undoes', 'big.opp = small; do.opp = undo'),
            ('doer', 'the one who does it or is marked by it', 'teach.doer = teacher'),
            ('made', 'the product, or the thing it is done to', 'write.made = text; add.made = sum'),
            ('tool', 'the instrument made for it', 'cut.tool = knife; compute.tool = computer'),
            ('place', 'the place where it is done or kept', 'cook.place = kitchen'),
            ('ness', 'the abstract state', 'friend.ness = friendship'),
            ('group', 'a collection taken as one unit', 'tree.group = forest'),
            ('able', 'able to undergo it', 'read.able = readable')]))
    T = T.replace('{{loantable}}', 'Consonant letters: ' + ', '.join(f'{k}={v}' for k, v in F.LC.items()) +
                  '\n\nVowel-class letters (a e i o u and also w y x): ' + ', '.join(f'{k}={v}' for k, v in F.LV.items() if k) +
                  f"\n\nNo vowel-class letter follows the consonant: vowel {F.LV['']}. No consonant before the vowel: initial ㅇ.")
    T = T.replace('{{loanextra}}', 'Digits: ' + ', '.join(f'{k}={v}' for k, v in F.L_DIGIT.items()) +
                  '\n\nSigns: ' + ', '.join(f'`{k}`={v}' for k, v in F.L_SYM.items()) +
                  '\n\nAccents (after the letter): ' + ', '.join(f'{F.ACC_NAMES[k]}={v}' for k, v in F.L_ACC.items()) +
                  f'\n\nMarks: capital={F.L_CAP}, capitals on/off={F.L_LOCK}, Greek={F.L_GREEK}, filler={F.L_PAD}')
    T = T.replace('{{capblk}}', F.L_CAP).replace('{{lockblk}}', F.L_LOCK).replace('{{greekblk}}', F.L_GREEK).replace('{{padblk}}', F.L_PAD)
    T = T.replace('{{greekmap}}', ' '.join(f'{k}={v}' for k, v in F.GREEK.items()))
    T = T.replace('{{handles}}', ' '.join(F.HANDLE_FORMS[:24]))
    T = T.replace('{{spares}}', ' '.join(lex['spares'][:40]))
    open(L.HERE + '/SPEC.md', 'w', encoding='utf-8').write(T)
    return T


def build_words():
    lines = ['# Word list', '',
             'Each line: FORM  english  [type]  note.  Types: T thing, Q quality, A act (main participant is AGENT),',
             'E event (main participant is THEME; adding an AGENT means "causes it"), R relational (takes REL).',
             'Only these roots exist. If a meaning is not here: use a root plus a suffix, a KIND compound, a loan, or DEFINE a spare.',
             '', '## Roots (sorted by English)', '']
    for g in sorted(lex['roots']):
        e = lex['roots'][g]
        note = e['def']
        extra = []
        if e['noun']: extra.append('noun: ' + e['noun'])
        if e['rel'] and e['type'] == 'R': extra.append('REL: ' + e['rel'].lstrip('~'))
        lines.append(f"{e['form']}  {g}  [{e['type']}]  " + '; '.join(x for x in [note] + extra if x))
    lines += ['', '## Common derived words (English = root + suffix). "+agent" means: the root with an AGENT added.', '']
    for k, v in sorted(lex['derived'].items(), key=lambda kv: kv[1]):
        if '+agent' in k:
            base = k[:-6]; lines.append(f"{v} = {lex['roots'][base]['form']} ({base}) + AGENT")
        else:
            base, suf = k.split('.')
            lines.append(f"{v} = {lex['roots'][base]['form']}{F.SUFFIX_FORMS[suf]} ({base}.{suf})")
    lines += ['', '## Spare words (no meaning until you DEFINE one)', '', ' '.join(lex['spares'])]
    open(L.HERE + '/WORDS.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    return lines


if __name__ == '__main__':
    t = build_spec(); w = build_words()
    print(len(t), 'chars spec;', len(w), 'lines word list')
