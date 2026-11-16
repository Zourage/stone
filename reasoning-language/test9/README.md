# test9: an interrupted task given only in the language

Question: if the task itself is never shown in English, does a writer understand it, answer in the language, stop when asked, take a correction, and finish?

- `turn1.txt`: the task (four tasks with durations, three ordering rules, two workers; say what can run together and the order; do not compute the time; wait). `turn1.gloss` is the same in the debugging notation.
- `turn2.txt`: the follow-up (two facts were wrong: one worker, task C takes 1 hour; say which earlier sentences still hold; compute the least time and explain).
- `prompt_turn1.txt`: the whole first prompt. Its English part names no topic.
- `<model><n>_turn1.txt`, `_turn2.txt`: the replies. `_english.txt`: machine English of the whole exchange.

Four writers, two per model. All four answered only in the language, held off computing, and waited. After the follow-up all four withdrew the claim that B and C run together, kept the ordering claims, and gave 7 hours with the working. Every sentence parsed. Two writers also noted that B and C can swap without changing the total.

Limits: four runs, one small puzzle, and the word list (root to English) was in context throughout.
