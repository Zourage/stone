export const meta = {
  name: 'conlang-wide-write',
  description: '24 writers (Opus and Fable) each write one task entirely in the constructed language and report what they could not express',
  phases: [{ title: 'Write', detail: '12 tasks x 2 models, one file each' }],
}
const S = '<workdir>'
const TASKS = ['K01','K02','K03','K04','K05','K06','K07','K08','K09','K10','K11','K12']
const MODELS = [{tag: 'opus', model: 'opus'}, {tag: 'fable', model: undefined}]
const SCHEMA = {type: 'object', properties: {
  wrote_file: {type: 'boolean'},
  problems: {type: 'array', items: {type: 'object', properties: {
    kind: {type: 'string', description: 'one of: missing_word, missing_grammar, unclear_rule, contradiction_in_rules, awkward_but_possible, other'},
    what: {type: 'string', description: 'what you wanted to say or do, in English'},
    workaround: {type: 'string', description: 'what you wrote instead'},
  }, required: ['kind', 'what', 'workaround']}},
}, required: ['wrote_file', 'problems']}
const items = TASKS.flatMap(t => MODELS.map(m => ({t, m})))
phase('Write')
const res = await parallel(items.map(it => () => {
  const file = `${S}/test5/${it.t}_${it.m.tag}.txt`
  const prompt = `Language experiment. A constructed language is defined by two files. Read both in full first:
- ${S}/lang/SPEC.md (rule sheet)
- ${S}/lang/WORDS.md (word list)
Then read ${S}/test5/tasks.md and do task ${it.t} only.
Do not read any other files and do not run any scripts or checkers.
Write your answer ONCE, entirely in the constructed language in its native script following the rule sheet (no English, no Latin letters except inside « » where the rule sheet allows), to the file ${file} with a single Write call. Do not revise the file afterwards.
Then return your structured result: wrote_file, and "problems" = an honest list (in English) of every place where the language or the rule sheet got in your way: a word you needed and could not find, a construction the rules do not cover, a rule that was unclear or contradicted another, or something you could only say awkwardly. For each give what you wanted and what you wrote instead. List real problems only; an empty list is fine.`
  const o = {label: `${it.t}:${it.m.tag}`, phase: 'Write', schema: SCHEMA, agentType: 'general-purpose'}
  if (it.m.model) o.model = it.m.model
  return agent(prompt, o).then(r => ({task: it.t, model: it.m.tag, r}))
}))
return res.filter(Boolean)