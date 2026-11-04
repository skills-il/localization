# Domain Coverage Checklist: hebrew-ai-text-humanizer

Generated: 2026-11-02. Aggregator sweep: the Academy of the Hebrew Language "common errors" index (https://hebrew-academy.org.il/topic/sheelot_teshuvot/mivharteshuvot/shgiot-nefotsot/) and its usage-decisions page, then the primary Academy pages per item. Language norms change slowly, so volatility is `stable`; the Academy pages carry their own update dates and should be re-read on each review.

## Must cover (core)
- [x] Conditional connectors ruled non-standard: במידה ו־, היה ו־ (use אם). Source: https://hebrew-academy.org.il/במידה-ש־/ and https://hebrew-academy.org.il/היה-ו־-היות-ש־-היות-ו־-וביטויים-קרובים/. Why core: the only calque items with an Academy ruling, so they must be labelled as rules, not taste.
- [x] במידה ש־ allowed only for real degree. Source: Academy usage decisions page. Why core: a naive fix turns במידה ו־ into במידה ש־ and is still wrong in a condition.
- [x] היות ו־ non-standard. Source: same Academy page.
- [x] עבור is style, not error. Source: Academy usage decisions page. Why core: prevents the skill from calling legitimate Hebrew "wrong".
- [x] Inflated register substitutions (על מנת for כדי, אשר for ש, במידה ו־ for אם). Source: Bahat quote on the Academy במידה ש־ page.
- [x] Maqaf between a prefix and a digit or Latin-script word. Source: https://hebrew-academy.org.il/על-מקף-וקו-מפריד/ and the punctuation rules.
- [x] Maqaf versus dash: the dash is legitimate Hebrew, spaced on both sides; only unspaced use and overuse are tells. Source: Academy punctuation rules and the maqaf/dash answer. Why core: the brief's suspected claim "em dashes are not native Hebrew" is false per the Academy and was dropped.
- [x] Geresh and gershayim, no periods in abbreviations. Source: Academy punctuation rules.
- [x] No space before punctuation, as an Academy RECOMMENDATION ("מומלץ מאוד"), with the light typographic space noted as a printing tradition. Source: https://hebrew-academy.org.il/הרווח-כולו-שלכם-רווחים-בסביבת-סימני/
- [x] Range dash exception: the Academy writes a range dash without spaces (maqaf note footnote; spacing guidance), so an unspaced en dash between words is `check`, never `rule`, and ranges are excluded from dash density. Round 2, from the independent judge.
- [x] Addressing a mixed audience: plural suggested, slashes hard to recommend, masculine is the unmarked default. Source: https://hebrew-academy.org.il/פנייה-המיועדת-לגבר-וגם-לאישה/
- [x] Direction problems in mixed Hebrew, English and numbers, and the RLM character. Source: Academy punctuation rules appendix A; https://www.w3.org/International/articles/inline-bidi-markup/ ; https://www.w3.org/International/questions/qa-bidi-unicode-controls
- [x] Fact preservation: numbers, codes, links, Hebrew weekdays and number words, negation count and `--keep` names are checked by `--compare` (exit 3 when nothing was checkable, never a pass); Hebrew names without `--keep`, amounts in words outside the list, and meaning are checked by the mandatory manual inventory on every host. Round 2 (2026-11-03): the first version reported success on zero tokens and could not see a changed surname, weekday, number word or flipped negation.
- [x] The writer's gender in first-person text: asked at intake; never defaulted to masculine; neutral forms (past or future verbs, כדאי + infinitive, אנחנו) when unknown; every gender decision logged. Round 2: the first version's own LinkedIn example invented a masculine "הייתי מתחיל".
- [x] Ethics boundary: editing for clarity and voice; refuses to frame work as detector evasion; says so plainly when disclosure is required.

## Should cover (advanced / edge cases)
- [x] Register targets (dugri / professional / formal) and which markers each allows (style guidance, no source claimed).
- [x] Structure tells (list-itis, bold labels, emoji bullets, triads, summary closers, headings in short texts, exclamation density): style guidance, no statistic claimed.
- [x] Agreement slips the script cannot see (feminine subjects, numerals, construct plurals): manual read.
- [x] LinkedIn and announcement tells (LNK01 to LNK08: "excited to share", "journey", "fills me with pride", "4 amazing years", blanket thanks, buzzwords, hashtag conventions, hook and paragraph length): style guidance, no source claimed.
- [x] Grammar-level translationese (GRM01 to GRM04: redundant subject pronouns, light-verb nominalisations, question-opening האם, על ידי passives): style guidance.
- [x] Over-Hebraised vocabulary versus the loanwords Israeli professionals use (VOC01) and spelling consistency within a text (SPL01): style guidance.
- [x] False-positive guards (Round 2): CAL05 is `check` and needs a following comma; PUN04 flags מס. only before a number; REG01 directives only before a known infinitive; CAL11 needs a repeated pronoun after a separator; PUN01 to PUN03 skip whole words made of prefix letters (מה, של, כל). Regression fixtures in scripts/fixtures/, tests in scripts/test_hebrew_ai_tells.py.
- [x] Spelling consistency inside the text (SPL01). Full ktiv maleh normalisation stays with hebrew-content-writer.

## Out of scope (explicit, with rationale)
- Writing new Hebrew content from a brief: `hebrew-content-writer`.
- Tokenising, morphology, NLP code: `hebrew-nlp-toolkit`.
- Producing formatted DOCX or PDF: `hebrew-document-generator`.
- Translating from English or another language: the skill edits Hebrew that already exists; a user who pastes English is told so.
- Making text pass an AI detector, or removing evidence of AI use where disclosure is required: refused by design. Users plausibly ask for this, so the answer is written (Gotchas), not silence.
- Any claim about detection rates or which patterns detectors use: no reliable public source; the skill makes none.

## Authoritative sources
- https://hebrew-academy.org.il/topic/hahlatot/punctuation/ : punctuation rules (maqaf, dash, geresh, gershayim, appendix on Latin text).
- https://hebrew-academy.org.il/topic/hahlatot/grammardecisions/terminology-ordinance/4-1-שימושי-לשון/ : usage decisions (עבור, במידה ש).
- https://hebrew-academy.org.il/במידה-ש־/ : במידה ו־ and the Bahat quote.
- https://hebrew-academy.org.il/היה-ו־-היות-ש־-היות-ו־-וביטויים-קרובים/ : היה ו־, היות ו־.
- https://hebrew-academy.org.il/על-מקף-וקו-מפריד/ : maqaf versus dash.
- https://hebrew-academy.org.il/פנייה-המיועדת-לגבר-וגם-לאישה/ : addressing both genders.
- https://www.w3.org/International/articles/inline-bidi-markup/ : bidi failure cases.

- [x] Round 3 (2026-11-03): negation check compares negation PHRASES, so a swap with an equal count is still caught. The closed negation list matches whole words (מלא, שאל, אל are not negations, ללא counts once). Dual number words (שנתיים, יומיים...) are added. Geresh day ranges are excluded from dash density. PUN06 is check, not rule.

## Known bad claims (do not regress)
- "Every unspaced dash is an Academy violation." False: the range dash is unspaced by Academy rule.
- "Space before punctuation is an Academy rule." It is a strong recommendation; old printing used a light space.
- "Add RLM between a Latin name and its number (a model or version number)." Wrong: such a number already renders with the name, and RLM inside it can reorder the pair. RLM is for a SEPARATE number after an English phrase (W3C case).
- "Em dashes are not a Hebrew punctuation habit." False: the Academy rules define the dash (קו מפריד) as a Hebrew mark. Only overuse and unspaced English-style use are flagged.
- "עבור is incorrect." False: the Academy calls it a question of style.
