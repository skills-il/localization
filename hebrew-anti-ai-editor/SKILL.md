---
name: hebrew-anti-ai-editor
description: Style editing of stiff or machine-sounding Hebrew into natural Hebrew across four registers, using eight modular operations (D1-D8). Use when user asks to make Hebrew text sound natural, remove machine-like phrasing, or run specific edit operations D1-D8 (Hebrew: ערוך לעברית טבעית). Do NOT use to evade AI-text detectors or to edit facts.
license: MIT
metadata:
  author: moti-luchim
  version: 1.0.0
  category: writing
  tags: [hebrew, style-editing, editing, natural-language, rtl]
  tags_he: [עברית, עריכת-סגנון, עריכה, שפה-טבעית, ימין-לשמאל]
  display_name_he: עורך עברית טבעית
---
# Hebrew Anti-AI Editor (Hebrew style editor)

## 1. Disclaimer
This is a style-editing aid. Its goal is clearer, more natural Hebrew. It is not a tool for evading AI-text detectors, and it makes no claim about how any detector will score a text. Where rules of academic integrity, a court or an employer require disclosing AI assistance, the user remains responsible for following them. Style editing does not verify facts. In legal text it is not legal advice. Do not rely on its output alone.

## 2. Purpose
Many machine-written Hebrew texts are grammatical but stiff: too formal, padded with inflated connectors, and translated word by word from English syntax. The skill finds these patterns and rewrites them into natural Hebrew without damaging professional terminology or meaning.

## 3. When to use
- The user asks to make Hebrew text more natural, remove stiff or machine-like phrasing, or polish a draft.
- The user asks for specific operations ("apply D3 and D7").
- The user supplies raw Hebrew text produced by a language model and asks to improve it.

## 4. Input
- The Hebrew text.
- Optional: target register (F, A, P, C below) and a sample of the user's own writing, for voice matching.
- Optional: a list of operations to apply. Default is the full path.

## 5. Output
1. Register chosen.
2. The edited text.
3. Main changes: patterns fixed and operations used.
4. Preservation notes: terms, construct phrases and distinctions kept on purpose.

## 6. Registers
- F: formal, legal, academic. Standard phrasing is kept (for example "אשר", "על מנת", complex construct chains), but calques are removed.
- A: article or professional blog. Fluent standard language, structured paragraphs, no worn-out connectors at the start of every sentence.
- P: post or marketing copy. Direct address, short rhythmic sentences.
- C: spoken or personal messages. Everyday, relaxed language.

## 7. The eight editing operations (D1-D8)
The letter D stands for the Hebrew letter dalet used in the original names (ד1 to ד8). Each operation can run alone or as part of the full path.
- D1, remove formulaic wording: replace stock openings, predictable transitions and repeated structures that add no content. Keep any sentence that already works.
- D2, voice preservation: infer the user's characteristic words, formality and structure from samples, and fix weak phrasing without imposing a generic editor voice or adding humor, slang or opinions that were not in the source. With no samples, say there is no basis for a personal style profile.
- D3, fluff elimination: delete repetition, self-evident statements and empty transitions. A sentence with useful content is shortened, not deleted. Keep substantive distinctions and context.
- D4, spoken readability and professional tone: prefer simple natural words suited to the audience. No slang, no forced friendliness, no forced rhetorical questions. In legal, academic or official text, keep terms of art and genre conventions.
- D5, precision over vagueness: find generalizations and abstract words and replace them with wording supported by the source. Examples come only from the source. If precision needs new information, ask the user instead of guessing.
- D6, reading cadence: fix monotone sentence length, openings and structure. Read the text aloud in your head and keep clear logical links between ideas.
- D7, anti-overpolishing: change only what harms clarity, credibility or flow. Keep wording with character and a personal point of view. Polish alone is not a reason to change.
- D8, final gate: check the opening, transitions, examples, endings and tone. Compare against the source to confirm every fact, position and caveat survived. Names, numbers, quotations and links need separate verification.

## 8. Working steps
1. Identify the register and the requested operations.
2. Find patterns: "ליצור" for abstract nouns (prefer "לגבש", "להפיק"), translated clichés, service openings and chatbot closings, inflated connectors ("מהווה", "משמש כ", "הינו") except in normative definitions in register F.
3. Rewrite using the chosen operations.
4. Report as in section 5.

## 9. Behavior when material is missing
- Very short text: edit lightly and say there is too little to judge the pattern.
- No source for a vague claim: keep it and flag it, do not invent specifics.
- Unclear register: ask once, or default to A and say so.

## 10. Privacy
Texts may hold personal or case details. Use them only for this edit. Do not paste them to public places or third-party services. Use invented examples when sharing the skill.

## 11. Synthetic example
Source (invented, register A): "בסופו של יום, חשוב לציין שהפתרון מהווה כלי מרכזי ליצירת ערך עבור הלקוחות."
Edited: "הפתרון עוזר ללקוחות לחסוך זמן." Only if the source supports the "save time" claim. If it does not, the edit stays at "הפתרון הוא כלי מרכזי ללקוחות" and flags the missing specific.
Changes: D1 (cliché opening removed), D3 (empty phrase removed), D5 (vague "value" flagged).

## Usage example
User says: "Make this paragraph sound natural, register A."
Result: the edited text, the operations used (for example D1, D3), and a note of what was kept on purpose.

## Troubleshooting

### Error: The edit changed a fact or a term
Cause: An operation shortened or reworded too far
Solution: Run D8 against the source and restore the original wording of facts, names, numbers and terms.

### Error: The text sounds over-polished
Cause: Too many operations were applied
Solution: Re-run with D7 only and keep wording that has a personal voice.

## Hebrew version
The same skill in Hebrew, with the same sections in the same order, is in references/SKILL_HE.md.
