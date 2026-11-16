export const meta = {
  name: 'test8-reader-scope-tone',
  description: 'Three leftover tests: loan-heavy round trip, scope ambiguity with and without the nesting rule, tone label distinguishability',
  phases: [
    { title: 'Translate', detail: '7 writers translate dense passages' },
    { title: 'Read', detail: 'two readers per passage: machine English only, native text plus rules' },
    { title: 'Judge', detail: 'compare each reconstruction with the source' },
    { title: 'Scope write', detail: '4 writers encode 12 two-reading items' },
    { title: 'Scope read', detail: '2 readers per writer pick the reading' },
    { title: 'Tone write', detail: '2 generators write messages per tone' },
    { title: 'Tone label', detail: '3 annotators label the messages' },
  ],
}
const ROOT = '/home/user/stone/reasoning-language'
const P = [
`The Suzuki-Miyaura reaction joins an aryl halide to a boronic acid. In the first step Pd(0) inserts into the C-Br bond of 4-bromotoluene; this oxidative addition gives a Pd(II) complex and is usually the slowest step. Unless a base such as K2CO3 is present, transmetalation does not occur, because the neutral boronic acid is too weak a nucleophile. Reductive elimination then releases 4-methylbiphenyl and returns Pd(0). Akira Suzuki shared the 2010 Nobel Prize for this work, although the 18-electron complex Pd(PPh3)4 that most students draw is not the active catalyst: it must first lose two PPh3 ligands.`,
`The Eyring equation, k = (kB·T/h)·exp(-ΔG‡/RT), relates a rate constant to the Gibbs energy of activation. For ΔG‡ = 85 kJ/mol at 298 K it gives k of about 8×10^-3 s^-1. Replacing a C-H bond by C-D lowers the zero-point energy, so the C-D bond is harder to break; a ratio kH/kD near 7 therefore shows that this bond breaks in the rate-determining step. A ratio near 1 does not prove the opposite, however: the bond may still break, but only after the slow step. Henry Eyring published the equation in 1935, the same year as Evans and Polanyi.`,
`Hodgkin and Huxley described the squid giant axon as a capacitor of 1 µF/cm² in parallel with three conductances: gNa = 120, gK = 36 and gL = 0.3 mS/cm². At rest, near -65 mV, the Na+ channels are mostly closed. A stimulus that passes the threshold of about -55 mV opens them, and the potential rises toward ENa = +50 mV within 1 ms. The potential then falls for two reasons: the Na+ channels inactivate, and the slower K+ channels open and pull it toward EK = -77 mV. During the next 2 to 4 ms a second spike is impossible or needs a much stronger stimulus; this is not because the membrane is tired but because the h-gate has not yet reset.`,
`The Higgs boson was announced on 4 July 2012 by the ATLAS and CMS collaborations at the LHC. Its mass is about 125 GeV/c², and it has spin 0, unlike every other elementary particle known. The W+, W- and Z0 bosons get their masses from the Higgs field, whereas the photon stays massless. It is often said that the Higgs field gives all matter its mass; that is misleading, since about 99% of the mass of a proton comes from the energy of the gluon field described by QCD, not from the Higgs field. François Englert and Peter Higgs received the 2013 Nobel Prize; Robert Brout had died in 2011.`,
`Doubling the CO2 concentration from 280 to 560 ppm adds a radiative forcing of about 3.7 W/m². If nothing else changed, the surface would warm by roughly 1.2 K. The IPCC's AR6 report nevertheless gives a likely range of 2.5 to 4.0 K, because water vapour and the ice-albedo effect amplify the warming, while the cloud feedback remains the largest uncertainty. Under scenario SSP1-2.6 warming probably stays below 2 °C by 2100; under SSP5-8.5 it could exceed 4 °C. A weakening of the AMOC would cool north-western Europe slightly, but it would not cancel global warming.`,
`Unix was written at Bell Labs in 1969 by Ken Thompson and Dennis Ritchie on a PDP-7 with only 8 kB of memory. Because AT&T was then forbidden to sell software, the source code was licensed to universities for a small fee, and at UC Berkeley Bill Joy turned it into BSD. In 1983 Richard Stallman started the GNU project so that a complete free system would exist; it had every part except a kernel. Linus Torvalds supplied that part in 1991 with Linux 0.01, which he first called "just a hobby". The file /etc/passwd and the command grep -r still work today almost as they did then.`,
`On 17 August 2017 the LIGO and Virgo detectors recorded GW170817, a signal lasting about 100 s from two neutron stars merging 130 million light-years away in the galaxy NGC 4993. Only 1.7 s later the Fermi satellite saw the gamma-ray burst GRB 170817A. That delay over such a distance shows that gravitational waves travel at the speed of light to within one part in 10^15. The kilonova AT 2017gfo that followed had spectra showing strontium, which confirms that the r-process happens in such mergers. It does not follow that all gold comes from them: supernovae of some kinds may contribute too.`,
]
const PROB = { type: 'array', items: { type: 'string' } }
const WRITE_S = { type: 'object', properties: { sentences: { type: 'integer' }, problems: PROB }, required: ['sentences', 'problems'] }
const READ_S = { type: 'object', properties: { english: { type: 'string' }, unsure: PROB }, required: ['english', 'unsure'] }
const JUDGE_S = { type: 'object', properties: {
  units: { type: 'array', items: { type: 'object', properties: { unit: { type: 'string' }, status: { enum: ['intact', 'weakened', 'wrong', 'lost'] }, note: { type: 'string' } }, required: ['unit', 'status'] } },
  terms: { type: 'array', items: { type: 'object', properties: { term: { type: 'string' }, status: { enum: ['exact', 'altered', 'missing'] }, got: { type: 'string' } }, required: ['term', 'status'] } },
}, required: ['units', 'terms'] }

const count = (arr, key) => arr.reduce((m, x) => { m[x[key]] = (m[x[key]] || 0) + 1; return m }, {})
const perm = n => Array.from({ length: n }, (_, i) => i).sort((a, b) => ((a * 37 + 11) % n) - ((b * 37 + 11) % n) || a - b)

// ---------- A. round trip ----------
const roundTrip = pipeline(P.map((p, i) => ({ p, id: 'P' + (i + 1) })),
  it => agent(`You are testing a constructed language. Read the rule sheet ${ROOT}/lang/SPEC.md completely and use the word list ${ROOT}/lang/WORDS.md. Read no other file and run no program.\n\nTranslate the passage below into the language, completely and exactly: every term, name, number and unit, and every logical link (because, although, unless, therefore). One numbered sentence per line, in the form the rule sheet shows. Write the result with ONE Write call to ${ROOT}/test8/${it.id}.txt (native script only, no English, no comments). Do not revise after writing.\n\nThen return the number of sentences and a list of concrete problems you met (missing word, unclear rule, loan spelling trouble).\n\nPASSAGE:\n${it.p}`,
    { label: 'write:' + it.id, phase: 'Translate', schema: WRITE_S }),
  async (w, it) => {
    const readers = await parallel([
      () => agent(`Run exactly this command and read its output:\n\ncd ${ROOT} && python3 lang/english.py native test8/${it.id}.txt\n\nThe output is a literal machine translation of a text written in a constructed language. Read nothing else in that folder (in particular no other file in test8/ and no rule sheet). Working ONLY from the command output, write the passage as natural, exact English: keep every term, name, number, unit and logical link as you find it; do not add facts from your own knowledge and do not correct anything that looks wrong. List anything you could not make sense of under "unsure".`,
        { label: 'read-machine:' + it.id, phase: 'Read', schema: READ_S }),
      () => agent(`Read the rule sheet ${ROOT}/lang/SPEC.md completely and use the word list ${ROOT}/lang/WORDS.md. Then read ${ROOT}/test8/${it.id}.txt, a text in that constructed language. Read no other file and run no program. Working ONLY from the text and the two reference files, write the passage as natural, exact English: decode every loan word by the letter table, keep every term, name, number, unit and logical link; do not add facts from your own knowledge and do not correct anything that looks wrong. List anything you could not decode or were unsure of under "unsure".`,
        { label: 'read-native:' + it.id, phase: 'Read', schema: READ_S }),
    ])
    const arms = ['machine', 'native']
    const judged = await parallel(readers.map((r, k) => () => r ? agent(`Compare a RECONSTRUCTION with its SOURCE passage. Do not use any tools.\n\n1. Split the SOURCE into its units of meaning (one claim, reason, condition or contrast each; typically 12 to 20). For each unit say whether the reconstruction has it "intact", "weakened" (vaguer, or a link such as because/unless lost or softened), "wrong" (says something different) or "lost".\n2. List every technical term, proper name, number-with-unit, formula and identifier in the SOURCE. For each say whether the reconstruction has it "exact" (same letters, capitals, hyphens, digits and signs; ordinary spacing differences do not count), "altered" (give what it has under "got") or "missing".\n\nSOURCE:\n${it.p}\n\nRECONSTRUCTION:\n${r.english}`,
      { label: `judge-${arms[k]}:${it.id}`, phase: 'Judge', schema: JUDGE_S }) : null))
    return { id: it.id, writer: w, arms: arms.map((a, k) => ({ arm: a, english: readers[k] && readers[k].english, unsure: readers[k] && readers[k].unsure, judge: judged[k], units: judged[k] && count(judged[k].units, 'status'), terms: judged[k] && count(judged[k].terms, 'status') })) }
  })

// ---------- B. scope ----------
const ITEMS = [
['I did not leave because of the rain.', 'I stayed, and the rain was the reason.', 'I did leave, but the rain was not the reason.'],
['You must not open the valve and start the pump.', 'What is forbidden is doing both; doing only one of them is allowed.', 'Each of the two actions is forbidden by itself.'],
['Probably the test failed and the log was deleted.', 'The speaker finds it probable that both things happened; neither is stated as fact.', 'The test probably failed; that the log was deleted is stated as plain fact.'],
['You do not have to attend / you must not attend.', 'Attending is not required (you may stay away or come).', 'Staying away is required (you are forbidden to attend).'],
['He did not answer deliberately.', 'He chose on purpose to give no answer.', 'He answered, but the answering was not done on purpose.'],
['We can not test the old version.', 'We are free to skip testing it (it is possible for us not to test it).', 'We are unable to test it.'],
['The engineer does not believe the bridge is safe.', 'The engineer believes that the bridge is unsafe.', 'The engineer has no belief that it is safe (may simply have no opinion).'],
['I hope the test passes and the build is fast.', 'The speaker hopes for both things.', 'The speaker hopes the test passes, and states as a fact that the build is fast.'],
['The alarm did not ring twice.', 'On two occasions the alarm failed to ring.', 'It is false that the alarm rang two times (it rang some other number of times).'],
['She did not speak to anger him.', 'She stayed silent, and her purpose in staying silent was to anger him.', 'She spoke, but angering him was not her purpose.'],
['The guard must check the bags or the tickets.', 'The guard has one duty with a free choice: check at least one of the two.', 'The guard has one specific duty, either the bags or the tickets, and the speaker does not know which.'],
['He was not sad and tired.', 'He was not sad; he was tired.', 'It is false that he was both sad and tired at once.'],
]
const itemText = ITEMS.map((x, i) => `${i + 1}. "${x[0]}"  A: ${x[1]}  B: ${x[2]}`).join('\n')
const SW_S = { type: 'object', properties: { sentences: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, text: { type: 'string' } }, required: ['id', 'text'] } }, problems: PROB }, required: ['sentences', 'problems'] }
const SR_S = { type: 'object', properties: { answers: { type: 'array', items: { type: 'object', properties: { n: { type: 'integer' }, reading: { enum: ['A', 'B', 'unclear'] } }, required: ['n', 'reading'] } } }, required: ['answers'] }
const SARMS = [['full', `${ROOT}/lang/SPEC.md`], ['noscope', `${ROOT}/test8/SPEC_noscope.md`]]
const scopeJobs = SARMS.flatMap(a => [1, 2].map(k => ({ arm: a[0], spec: a[1], k })))
const scope = pipeline(scopeJobs,
  j => agent(`You are testing a constructed language. Read the rule sheet ${j.spec} completely and use the word list ${ROOT}/lang/WORDS.md. Read no other file and run no program.\n\nBelow are 12 English sentences that can each be read two ways. For EACH reading (A and B) write one sentence of the constructed language that has exactly that reading and cannot be taken as the other. 24 sentences, ids 1A, 1B, 2A ... 12B. Native script only. Use only what the rule sheet gives you; if you see no way to force a reading, write your best attempt and say so under problems.\n\nWrite them with ONE Write call to ${ROOT}/test8/scope_${j.arm}${j.k}.txt, one per line as "1A: <sentence>", and return the same sentences.\n\n${itemText}`,
    { label: `scope-write:${j.arm}${j.k}`, phase: 'Scope write', schema: SW_S }),
  async (w, j) => {
    const ok = w.sentences.filter(s => /^\d+[AB]$/.test(s.id.trim()))
    const order = perm(ok.length).map(i => ok[i])
    const list = order.map((s, n) => { const it = ITEMS[parseInt(s.id) - 1]; return `${n + 1}. English: "${it[0]}"\n   Reading A: ${it[1]}\n   Reading B: ${it[2]}\n   Sentence: ${s.text.replace(/^\s*\d+[AB]\s*:\s*/, '')}` }).join('\n\n')
    const rs = await parallel([1, 2].map(r => () => agent(`Read the rule sheet ${j.spec} completely and use the word list ${ROOT}/lang/WORDS.md. Read no other file and run no program.\n\nBelow are ${order.length} sentences in that constructed language. Each was written to express ONE of two readings of an ambiguous English sentence. For each, decide from the sentence itself, by the rules, which reading it expresses: "A", "B", or "unclear" if by the rules it could be either or neither. Judge each sentence on its own; do not guess from the other sentences in the list.\n\n${list}`,
      { label: `scope-read:${j.arm}${j.k}.${r}`, phase: 'Scope read', schema: SR_S })))
    const res = rs.filter(Boolean).map(r => { let right = 0, wrong = 0, unclear = 0; const miss = []
      order.forEach((s, n) => { const a = (r.answers.find(x => x.n === n + 1) || {}).reading; const want = s.id.trim().slice(-1)
        if (a === want) right++; else { if (a === 'unclear' || !a) unclear++; else wrong++; miss.push(s.id.trim() + ':' + (a || 'none')) } })
      return { right, wrong, unclear, miss } })
    return { arm: j.arm, k: j.k, n: order.length, problems: w.problems, readers: res }
  })

// ---------- C. tone ----------
const TONES = [
['SURPRISE', 'the speaker did not expect this'], ['EMPHASIS', 'the speaker stresses that this point matters'], ['POLITE', 'courteous, softened wording toward the listener'],
['REGRET', 'the speaker wishes this were otherwise, often about own doing'], ['GLAD', 'the speaker is pleased about this'], ['ANNOYED', 'the speaker is irritated'],
['JEST', 'said as a joke, not to be taken seriously'], ['IRONY', 'the speaker means the opposite of the literal words'], ['FRANK', 'blunt honesty, no softening'],
['HOPE', 'the speaker wants this to come true'], ['FEAR', 'the speaker is afraid this is or will be so'], ['SERIOUS', 'explicitly not joking; to be taken at face value and with weight'],
['WARM', 'affection or friendliness toward the listener'], ['SAD', 'sorrow about this'], ['GRATEFUL', 'thankful to someone'],
['RHETORICAL', 'a question asked to make a point, no answer wanted'], ['HINT', 'the speaker is implying something without saying it outright'], ['WARNING', 'the speaker alerts the listener to a danger'],
['RELUCTANT', 'the speaker says or does this unwillingly'], ['PROUD', 'pride in an achievement, own or someone else\'s'], ['CURIOUS', 'the speaker would like to know more'],
['DOUBT', 'the speaker is sceptical that this is true'], ['EXCITED', 'eager, energised anticipation or enthusiasm'], ['RESIGNED', 'the speaker accepts something unwelcome as unavoidable'],
['DISGUST', 'the speaker finds this repellent'], ['EMBARRASSED', 'the speaker feels awkward or ashamed about this'], ['COMFORT', 'the speaker is trying to soothe or reassure the listener'],
]
const toneList = TONES.map(t => `${t[0]}: ${t[1]}`).join('\n')
const names = TONES.map(t => t[0])
const TG_S = { type: 'object', properties: { messages: { type: 'array', items: { type: 'object', properties: { tone: { enum: names }, text: { type: 'string' } }, required: ['tone', 'text'] } } }, required: ['messages'] }
const TL_S = { type: 'object', properties: { labels: { type: 'array', items: { type: 'object', properties: { n: { type: 'integer' }, tone: { enum: names } }, required: ['n', 'tone'] } } }, required: ['labels'] }
const SETTINGS = ['a software team chatting at work about a release', 'friends and family messaging about everyday life (meals, travel, weather, plans)']
const tone = (async () => {
  phase('Tone write')
  const gens = (await parallel(SETTINGS.map((s, g) => () => agent(`Do not use any tools. Below is a list of 27 tone labels with definitions. For EACH label write 2 short English messages (one sentence each, at most 20 words) set among ${s}, in which a careful reader would recognise that tone as the single dominant one. Write naturally, as people really write: do not name the tone or use the label word or an obvious synonym of it, and do not use emoji. 54 messages in all.\n\n${toneList}`,
    { label: 'tone-gen:' + (g + 1), phase: 'Tone write', schema: TG_S })))).filter(Boolean)
  const all = gens.flatMap(g => g.messages)
  const order = perm(all.length).map(i => all[i])
  const list = order.map((m, n) => `${n + 1}. ${m.text}`).join('\n')
  const labs = (await parallel([1, 2, 3].map(a => () => agent(`Do not use any tools. Below is a list of 27 tone labels with definitions, then ${order.length} short messages. Give each message exactly one label: the single tone that dominates it. Judge each message on its own.\n\n${toneList}\n\nMESSAGES:\n${list}`,
    { label: 'tone-label:' + a, phase: 'Tone label', schema: TL_S })))).filter(Boolean)
  const stat = {}; names.forEach(t => stat[t] = { n: 0, hit: 0, conf: {} })
  const allAgree = { n: 0, agree: 0 }
  order.forEach((m, n) => { const got = labs.map(l => (l.labels.find(x => x.n === n + 1) || {}).tone)
    allAgree.n++; if (got.every(g => g === got[0])) allAgree.agree++
    got.forEach(g => { const s = stat[m.tone]; s.n++; if (g === m.tone) s.hit++; else s.conf[g] = (s.conf[g] || 0) + 1 }) })
  return { messages: all.length, annotators: labs.length, allAgree, stat, sample: order.slice(0, 12) }
})()

const [A, B, C] = await Promise.all([roundTrip, scope, tone])
return { roundTrip: A, scope: B, tone: C }