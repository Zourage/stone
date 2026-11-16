export const meta = {
  name: 'conlang-heavy-science-write',
  description: '21 writers (alternating Opus and Fable) each write one heavy chemistry, neuroscience or other science task entirely in the constructed language, under the no-English rule, and report what got in their way',
  phases: [{ title: 'Write', detail: '21 tasks, one writer and one file each' }],
}
const S = '<workdir>'
const TASKS = ['C01','C02','C03','C04','C05','C06','C07','C08','N01','N02','N03','N04','N05','N06','N07','X01','X02','X03','X04','X05','X06']
const SCHEMA = {type: 'object', properties: {
  wrote_file: {type: 'boolean'},
  problems: {type: 'array', items: {type: 'object', properties: {
    kind: {type: 'string', description: 'one of: loan_trouble, missing_word, missing_grammar, unclear_rule, contradiction_in_rules, awkward_but_possible, other'},
    what: {type: 'string', description: 'what you wanted to say or do, in English'},
    workaround: {type: 'string', description: 'what you wrote instead'},
  }, required: ['kind', 'what', 'workaround']}},
}, required: ['wrote_file', 'problems']}
phase('Write')
const res = await parallel(TASKS.map((t, i) => () => {
  const tag = i % 2 === 0 ? 'opus' : 'fable'
  const file = `${S}/test7/${t}_${tag}.txt`
  const prompt = `Language experiment. A constructed language is defined by two files. Read both in full first:
- ${S}/lang/SPEC.md (rule sheet)
- ${S}/lang/WORDS.md (word list)
Then read ${S}/test7/tasks.md and do task ${t} only.
Do not read any other files and do not run any scripts or checkers.
Write your answer ONCE, entirely in the constructed language in its native script following the rule sheet, to the file ${file} with a single Write call. Do not revise the file afterwards.
Important: the rule sheet forbids English words outside code. Technical terms, abbreviations and names of people that no root covers must be spelled as loan words by the letter table (section 8 of the rule sheet), not put in « ». Keep every named term from the task.
Then return your structured result: wrote_file, and "problems" = an honest list (in English) of every place where the language or the rule sheet got in your way: a term you could not spell as a loan or were unsure how to (kind loan_trouble), a word you needed and could not find, a construction the rules do not cover, a rule that was unclear or contradicted another, or something you could only say awkwardly. For each give what you wanted and what you wrote instead. List real problems only; an empty list is fine.`
  const o = {label: `${t}:${tag}`, phase: 'Write', schema: SCHEMA, agentType: 'general-purpose'}
  if (tag === 'opus') o.model = 'opus'
  return agent(prompt, o).then(r => ({task: t, model: tag, r}))
}))
return res.filter(Boolean)