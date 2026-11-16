export const meta = {
  name: 'conlang-science-write',
  description: '20 writers (alternating Opus and Fable) each write one science or computing task entirely in the constructed language and report what they could not express',
  phases: [{ title: 'Write', detail: '20 tasks, one writer and one file each' }],
}
const S = '<workdir>'
const TASKS = ['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20']
const SCHEMA = {type: 'object', properties: {
  wrote_file: {type: 'boolean'},
  problems: {type: 'array', items: {type: 'object', properties: {
    kind: {type: 'string', description: 'one of: missing_word, missing_grammar, unclear_rule, contradiction_in_rules, awkward_but_possible, other'},
    what: {type: 'string', description: 'what you wanted to say or do, in English'},
    workaround: {type: 'string', description: 'what you wrote instead'},
  }, required: ['kind', 'what', 'workaround']}},
}, required: ['wrote_file', 'problems']}
phase('Write')
const res = await parallel(TASKS.map((t, i) => () => {
  const tag = i % 2 === 0 ? 'opus' : 'fable'
  const file = `${S}/test6/${t}_${tag}.txt`
  const prompt = `Language experiment. A constructed language is defined by two files. Read both in full first:
- ${S}/lang/SPEC.md (rule sheet)
- ${S}/lang/WORDS.md (word list)
Then read ${S}/test6/tasks.md and do task ${t} only.
Do not read any other files and do not run any scripts or checkers.
Write your answer ONCE, entirely in the constructed language in its native script following the rule sheet (no English, no Latin letters except inside « » where the rule sheet allows), to the file ${file} with a single Write call. Do not revise the file afterwards.
Then return your structured result: wrote_file, and "problems" = an honest list (in English) of every place where the language or the rule sheet got in your way: a word you needed and could not find, a construction the rules do not cover, a rule that was unclear or contradicted another, or something you could only say awkwardly. For each give what you wanted and what you wrote instead. List real problems only; an empty list is fine.`
  const o = {label: `${t}:${tag}`, phase: 'Write', schema: SCHEMA, agentType: 'general-purpose'}
  if (tag === 'opus') o.model = 'opus'
  return agent(prompt, o).then(r => ({task: t, model: tag, r}))
}))
return res.filter(Boolean)