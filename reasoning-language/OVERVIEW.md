# A reasoning language for AI models: short overview

*Working prototype, version 1. Status and limits are at the end.*

## What it is for

An experiment: can a language model do its writing and reasoning in a purpose-built language, and can that text be turned back into English by a program, with nothing lost?

English is hard for a program to read back exactly. Word order carries meaning, pronouns are ambiguous, and nothing forces a writer to say whether a statement is a fact, a guess or a conclusion. This language removes those three problems by design.

## The four ideas

**1. A word's shape tells you what kind of word it is.**
Words are written in Korean (Hangul) syllable blocks, used only as shapes. No Korean is involved.

| Shape | Kind | Example |
|---|---|---|
| one open block | grammar particle | 사 (marks the doer) |
| one closed block | short name for a thing ("A", "B") | 각 |
| open block + closed block | root word, from a fixed list of about 1,300 | 코롤 (dog) |
| root + ending | derived word, from 8 endings | 오덕 (write) → 오덕일 (writer), 오덕엄 (text) |
| several open blocks | borrowed word, spelled character by character from a table (capitals, hyphens and digits are kept) | 데키거티찌허 (kubernetes) |
| open block with a w-vowel | one of 13 code keywords | 화 (define) |

**2. Every participant is tagged, so order carries no meaning.**
The action comes first; each participant has a particle saying what role it plays. These two sentences mean exactly the same thing:

```
겨 러존 사 아 새 코롤 .      claim · see · doer: me · thing: dog
겨 러존 새 코롤 사 아 .      claim · see · thing: dog · doer: me
→ "I see the dog."
```

**3. Every sentence must say what kind of statement it is.**
The first word is an obligatory opener: claim, given, assumed, derived, recalled, question, proposal, definition and so on. A derived sentence names the numbered sentences it follows from.

```
1: 가 떠못 새 코롤 차 각 .               [given] The dog (call it A) is big.
2: 가 프촐 사 마 터슷 새 마 코롤 라 떠못 .   [given] All cats fear all big dogs.
3: 갸 1 2 프촐 사 마 터슷 새 각 .         [follows from 1 and 2] All cats fear A.
```

**4. No pronouns.** A thing is given a short name once (각 above) and that name is used afterwards, so "it" can never point at the wrong thing.

## Logic and code

The same grammar has a strict sub-form for definitions, conditions and loops, which a program converts to Python.

```
화 ( 사툭 라 떠못 ) 와 각 워 낙 회 { 되 { 툐 와 각 워 낙 } { 희 각 } . 희 낙 } .
→ define bigger-number(A, B): if A > B, return A; return B.
```

All code is written in this form, with the target language declared at the top and libraries imported under a short name; the converter emits Python or JavaScript.

Outside code there is no English at all. Technical terms and names are borrowed words spelled by the letter table (IL-4, "affinity maturation", people's names). The « » marks hold only symbols: chemical formulas, units, mathematical expressions, and names inside code.

## The tools

- A **parser** that accepts or rejects each sentence.
- A **rule-based translator** to literal English, with no model involved, so its output can be trusted as a record.
- An optional **model layer** that rewrites the literal English into natural English and lists every place it had to interpret.
- A **logic-to-Python** converter.
- A **rule sheet and word list** (about 120 KB together), which is all a model is given to learn it.

## Where it stands

Tested so far only on strong models, given the rule sheet and word list and no feedback:

- They write it correctly on the first attempt: stories, technical explanations, proofs and code. In the latest rounds every sentence parsed after small fixes to the rules.
- Readers answered 20 of 20 questions about texts given only in the language.
- In a meaning check on 7 passages, 78 of 91 units of meaning survived the round trip intact, 12 were weakened, 1 was wrong and none were lost.
- Every function written in it so far ran correctly when converted to Python.

Limits:

- **Not shown: that a model thinks in it.** Writing it takes several times more hidden work than the text itself, and what that work consists of has not been examined.
- **It is close to a regularised English.** Each root is defined by an English meaning, which is why translation is easy and also why it may not be a separate medium of thought.
- **Slow and costly.** Text is roughly 1.5 times as long as English in tokens and takes several times longer to produce.
- **Small samples**, one model family, and no test yet on weaker or open models.
