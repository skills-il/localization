---
name: hebrew-ai-text-humanizer
description: Edits Hebrew that reads as machine-written or translated (emails, LinkedIn posts, product pages, WhatsApp messages to customers, reports) into natural Israeli Hebrew. Use when the user pastes Hebrew that sounds like AI or translated, "ze nishma kmo ChatGPT", "taarokh li et ha-ivrit", or asks to fix register, gender addressing, maqaf or gershayim. Flags a named catalogue of AI-Hebrew patterns (calques like bemida ve and al menat, register mismatch, mixed addressing, list-itis, dash overuse, prefix-number maqaf, bidi breaks) by line, rewrites at the chosen register keeping every fact, number and name, and returns a change log so the writer learns. Editing for clarity and voice, not detector evasion. Do NOT use for writing new content (hebrew-content-writer), Hebrew NLP code (hebrew-nlp-toolkit), DOCX or PDF output (hebrew-document-generator), or translation from another language.
license: MIT
compatibility: Optional Python 3 (standard library only, no network) for scripts/hebrew-ai-tells.py. On chat-only hosts (Claude.ai, ChatGPT, Claude Desktop without a shell, Manus, Grok) the skill follows the no-script route in Step 2 using references/ai-hebrew-patterns.md. Gemini Spark can run the script; it makes no network calls.
---

# Hebrew AI Text Humanizer

## Problem

Hebrew written by an AI model, or translated from an English draft, has a recognisable accent: במידה ו־ where an Israeli writes אם, "חשוב לציין" before every point, bold labels and emoji bullets, a reader addressed as לקוח/ה in one line and as אתה in the next, and ב2025 with no maqaf. Readers notice it within a sentence and trust the text less. This skill finds each of those patterns with a line reference, rewrites the text at the register the user wants without touching a single fact, and hands back a change log so the writer stops producing the same patterns.

## What you need from the user

1. **The Hebrew text** (pasted, or a file path on shell hosts). If it is not Hebrew, stop: translation is out of scope.
2. **Channel and audience**: LinkedIn post, customer email, WhatsApp to customers, product page, internal report, letter to an authority.
3. **Target register**: dugri / casual, professional, or formal. If the user does not say, propose one from the channel (WhatsApp: casual; LinkedIn and customer email: professional; authority letter: formal) and say which you chose.
4. **The writer's gender**, whenever the text speaks in the first person (a LinkedIn post, a personal email). Hebrew first person is gendered in the present tense, participles and adjectives (נרגש / נרגשת, מתחיל / מתחילה). Ask; never assume masculine. If the user does not want to say, keep every first-person form gender-neutral (see Step 5 rule 3) and say so under Judgement calls.
5. **Addressing the reader**: plural (default for a mixed audience), masculine singular, feminine singular, or one named person.
6. **Must-keep items**: names of people and companies, brand terms, legal wording, quotes, a signature line, anything the user does not want touched.

If the user states that the goal is to get past an AI detector, or to hide AI use where a disclosure rule applies (a course assignment, a submission that requires disclosure), say plainly that the skill does not do that, and offer the clarity edit only under the user's own disclosure obligations. Do not promise any detector outcome in any case.

## Instructions

### Step 1: Intake and branch
Collect the items above. Branch:
- Text is in English or another language: decline the rewrite and point to translation; the skill edits existing Hebrew.
- Legal wording, or any wording the user marked as fixed: scan and report only, do not rewrite those sentences.
- Detector-evasion goal: apply the boundary above before anything else.

Check: before rewriting you know the register, the reader's addressing form and, for first-person text, the writer's gender (or that it stays neutral). Ask one short question that covers whatever is missing.

### Step 2: Scan against the catalogue
**Shell hosts**: save the text to a file and run:

```bash
python3 scripts/hebrew-ai-tells.py input.txt --register professional --channel linkedin
```

Each line of output is `L<line>:C<col>  <id>  [rule|style|check]  "<match>"  <hint>`, then document-level findings (list-itis, dash density, triads, summary closers, headings, exclamations, mixed addressing, hashtags, LinkedIn hook and paragraph length, mixed spelling) and a density figure (scored flags per 100 words; bands: under 3 light, under 8 moderate, otherwise heavy). The density is an editing-workload heuristic for this catalogue only. Never present it as an AI-detection score or as a verdict on who wrote the text.

**No-script route (chat-only hosts)**: walk the text line by line through `references/ai-hebrew-patterns.md` sections A to E (calques, register, addressing, structure, punctuation and direction) and `references/channel-grammar-gender.md` sections F to I (LinkedIn tells, grammar-level translationese, vocabulary and spelling, the writer's gender). Record each hit as `line N: <id> "<span>"`. Report the number of hits, not a density.

Either route: also read for what no regex sees, namely gender and number agreement (המערכת מאפשרת, שתי אפשרויות), gendered first-person forms, a sentence whose meaning is unclear, and claims that sound invented.

### Step 3: Triage every flag
For each flag decide one of:
- **Fix**: the pattern is present and the target register does not want it.
- **Keep**: a false positive or a deliberate choice. Typical ones: ניתן meaning "was given", אשר as a name, מסע as a real trip, a list that really is a list of parallel items, אנו in a formal letter, a dash used once for real emphasis, a casual emoji in a WhatsApp message, a Hebrew word the brand prefers over the loanword.
- **Ask**: the fix would change meaning (for example dropping "אסטרטגית" or merging two claims).

Status decides wording. Only these may be called non-standard: CAL03, CAL06, STR04 (glued em dash) and PUN01 to PUN04 when printed as `rule`, and CAL04 or CAL05 after you have read the sentence and confirmed it is a plain condition (the script prints those two as `check`). An unspaced en dash between words (STR04 `check`) is correct when it marks a range, which the Academy writes without spaces. PUN05 (space before punctuation) is an Academy recommendation: say "the Academy recommends", not "non-standard". Everything else is style: "reads as translated", "template tell", "register". עבור is explicitly a style question per the Academy, and the dash is a legitimate Hebrew mark per the Academy punctuation rules.

### Step 4: Build the fact inventory (every host)
Before rewriting, list every number, date, time, weekday, name of a person, company or place, brand, product, code (order numbers, coupon codes), link, e-mail, promise, deadline and negation ("לא כולל", "אין"). Do this by hand on every host: the script cannot see Hebrew names or meaning. These must all be present after the rewrite with the same values and the same polarity. Do not add facts, figures, results or examples that are not in the source, even to make the text "more concrete".

### Step 5: Rewrite
Rules, in priority order:
1. Facts and intent unchanged. The writer's claims stay theirs, at the same strength: a general claim does not become a personal opinion, "worked together" does not become "started working together".
2. One addressing form for the reader throughout: every verb, pronoun, possessive suffix and adjective matches it. For a mixed audience use plural (the Academy grammar committee's suggestion); avoid slash forms.
3. The writer's gender: never introduce a gendered first-person form that is not already in the source. Keep the source's gender where it has one. If unknown, use forms that are the same for both: past or future verbs (הובלתי, אשמח), "כדאי" plus an infinitive, or "אנחנו".
4. Register as chosen. Casual: short sentences, direct verbs, אנחנו, no preambles. Professional: full sentences, no office-form markers (הננו, ברצוננו, בנוגע ל־), no slang, and the loanwords Israeli professionals actually use (פידבק, מייל, אפליקציה) rather than over-Hebraised ones. Formal: אנו and impersonal directives allowed, but never במידה ו־, היה ו־, היות ו־.
5. Grammar: אם for conditions, כדי for purpose, ש־ for relative clauses, כי or כיוון ש־ for cause; drop subject pronouns the verb already carries (הובלתי, not אני הובלתי); plain verbs over light-verb phrases (הטמענו, not ביצענו הטמעה); no האם at the start of a casual or professional question; fewer על ידי passives. Delete importance preambles and scene-setting openers.
6. Channel. LinkedIn: the news in the first line, before the "see more" fold; one idea per short paragraph; no "excited to share", "journey", "fills me with pride" or blanket thank-yous; at most about three hashtags, at the end, multi-word Hebrew tags joined with an underscore. Email: the news in the subject line. WhatsApp: short, one message, at most one emoji.
7. Structure: prose for reasoning; keep a list only for parallel items the reader scans. Remove bold labels, emoji bullets, headings in short texts, and the summary sentence at the end of every paragraph.
8. Punctuation: join a prefix to a number or Latin word (in social and marketing copy with the keyboard hyphen, ב-2025; in print and formal text with the maqaf, ב־2025; keep one choice throughout), geresh and gershayim instead of periods (מס', צה"ל), no space before punctuation, the dash only with a space on each side and rarely. Keep the writer's spelling of a word consistent (תוכנית or תכנית, not both).
9. Direction: start Hebrew lines with Hebrew when you can. When an English phrase is followed by a separate number (Harry Potter followed by "3 פעמים"), rephrase so the number is not right after it, or in plain text insert RLM (U+200F) after the English phrase. Leave a number that is part of a name alone, and never put RLM inside such a name: it can reorder the name and its number.
10. Keep the writer's voice: their idioms, humour, signature and length (within about a fifth longer or shorter unless asked).

### Step 6: Verify
**Shell hosts**:

```bash
python3 scripts/hebrew-ai-tells.py rewrite.txt --register professional --channel linkedin
python3 scripts/hebrew-ai-tells.py input.txt --compare rewrite.txt --keep "Name One,Company Name"
```

The first must show no remaining rule-level flags, and every remaining style flag must be one you chose to keep. The second checks digits, Latin-script tokens, URLs, e-mails, @handles, Hebrew weekdays and number words, negation phrases that disappear (each negation word with the word after it, so a negation moved to a different word is caught only when the word after it differs: a negation moved between sentences that share the verb, "המחיר לא כולל משלוח. ההחזר כולל עמלה." to "המחיר כולל משלוח. ההחזר לא כולל עמלה.", is not flagged by the negation check, which is why the manual negation inventory below is mandatory), and the names passed with `--keep` (put every person, company and place name from the Step 4 inventory there). Exit 0: all present. Exit 1: something to restore or confirm with the user (MISSING, CHANGED, CHECK lines). Exit 3: nothing in the original was machine-checkable, which is never a pass. It always prints what it did NOT check; cover that with the Step 4 inventory.

**Every host**: tick through the Step 4 inventory one item at a time against the rewrite (names, weekdays, amounts in words, every negation), check every first-person form against rule 3, and re-walk catalogue sections A and E on the rewrite.

Then read the rewrite once as an Israeli reader would. If any sentence needs a second read, fix it.

## Output

Return, in this order, as plain text (never inside a code block, which breaks right-to-left rendering):

1. **The rewritten text**, ready to paste.
2. **Change log** table: `# | Pattern | Before | After | Why`. One row per change; "Why" is one short clause, and says "Academy rule" only for the rule-status patterns in Step 3.
3. **Judgement calls**: every meaning-level edit the user should confirm (a dropped adjective, a merged sentence, a softened or generalised claim, a general claim made personal or the reverse) and every gender decision (gender assumed from the user's answer, or kept neutral because unknown).
4. **Kept as is**: flags you deliberately left, with the reason.
5. **Fact check**: say exactly what was checked and how. Template: "Script: <N of N checkable items present, listed>; <any MISSING, CHANGED or CHECK lines>. By hand: <list what you checked (names, weekdays, amounts in words, each negation) and every change found, including negations moved or rewritten>." Never write "names preserved" unless you checked the names.
6. **Watch next time**: the two or three patterns that occurred most, so the writer can catch them.

## Examples

### Example 1: LinkedIn post (about 120 words), professional register, writer's gender not given
Input (the two long dashes of the original are written here as [em dash], because this file avoids the character):

> בעולם של היום, חשוב לציין שבינה מלאכותית היא לא רק כלי [em dash] היא שותפה אסטרטגית.
>
> ב2025 הובלתי בחברת נתיב לוגיסטיקה מעבר למערכת תכנון מסלולים מבוססת AI. זה היה מסע מאתגר, אבל כל צעד בדרך לימד אותנו משהו חדש. התוצאות מדברות בעד עצמן:
> 🚀 **יעילות:** קיצרנו את זמני החלוקה ב-18 אחוז
> 💡 **חדשנות:** הצוות למד לעבוד עם כלים חדשים
> 🤝 **שיתוף פעולה:** המחלקות עבדו יחד באופן משמעותי
>
> במידה ואתם שוקלים מהלך דומה, יש לציין כי הדבר דורש הכנה, סבלנות ומחויבות. על מנת להבטיח שהמעבר יצליח, ניתן להתחיל בפיילוט קטן עבור צוות אחד.
>
> בסופו של יום, זה לא על הטכנולוגיה [em dash] זה על האנשים.
> מה דעתכם? אשמח לשמוע בתגובות! 👇

Scan (shell host, `--register professional --channel linkedin`): 21 inline flags (CAL01, CAL02, CAL03, CAL07, CAL09 twice, CAL10, CAL11 twice, CAL12, CAL13 twice, CAL15, LNK02, PUN01, STR02 three times, STR03 three times) plus document-level STR04 (two long dashes in 103 words): 22 scored flags, 21.4 per 100 words, heavy edit. The rewrite scans clean (0 flags).

Rewritten text:

> בינה מלאכותית היא שותפה לעבודה, לא רק כלי.
>
> ב-2025 הובלתי בחברת נתיב לוגיסטיקה מעבר למערכת לתכנון מסלולים שמבוססת על AI. זה היה מאתגר, וכל שלב בדרך לימד אותנו משהו חדש. מה יצא מזה:
> קיצרנו את זמני החלוקה ב-18 אחוז.
> הצוות למד לעבוד עם כלים חדשים.
> המחלקות עבדו הרבה ביחד.
>
> שוקלים מהלך דומה? כדאי להתחיל בפיילוט קטן עם צוות אחד. זה דורש הכנה, סבלנות ומחויבות.
>
> בסוף, האנשים חשובים יותר מהטכנולוגיה.
> מה דעתכם? עשיתם מעבר כזה? אשמח לשמוע בתגובות איך זה הלך אצלכם.

Change log (excerpt):

| # | Pattern | Before | After | Why |
|---|---|---|---|---|
| 1 | CAL10 + CAL09 | בעולם של היום, חשוב לציין ש | (removed) | opener and preamble add nothing |
| 2 | CAL11 | היא לא רק כלי [em dash] היא שותפה אסטרטגית | היא שותפה לעבודה, לא רק כלי | contrast frame, dash removed |
| 3 | PUN01 | ב2025 | ב-2025 | Academy rule: join prefix and digit (hyphen, social copy) |
| 4 | LNK02 + CAL13 | זה היה מסע מאתגר ... התוצאות מדברות בעד עצמן | זה היה מאתגר, וכל שלב בדרך לימד אותנו משהו חדש. מה יצא מזה | "journey", English idiom |
| 5 | STR02 + STR03 | 🚀 **יעילות:** | (plain sentence) | template tell |
| 6 | CAL15 | עבדו יחד באופן משמעותי | עבדו הרבה ביחד | -ly adverb calque |
| 7 | CAL03 | במידה ואתם שוקלים | שוקלים | Academy rule: במידה ו־ is non-standard; question form instead |
| 8 | CAL07 + CAL12 + CAL02 + CAL01 | על מנת להבטיח שהמעבר יצליח, ניתן להתחיל בפיילוט קטן עבור צוות אחד | כדאי להתחיל בפיילוט קטן עם צוות אחד | inflated connectors, register |
| 9 | CAL13 + CAL11 | בסופו של יום, זה לא על הטכנולוגיה [em dash] זה על האנשים | בסוף, האנשים חשובים יותר מהטכנולוגיה. | idiom, contrast frame |

Judgement calls: the writer's gender was not given, so every first-person form is neutral (הובלתי, אשמח, and "כדאי להתחיל" rather than "הייתי מתחיל / מתחילה"); "אסטרטגית" dropped as filler (restore if it matters to you); "זה היה מסע מאתגר, אבל כל צעד" became "זה היה מאתגר, וכל שלב" (journey dropped, claim kept); "זה לא על הטכנולוגיה, זה על האנשים" became the positive "האנשים חשובים יותר מהטכנולוגיה", same claim without the contrast frame, so one negation is gone (see the fact check); "המחלקות עבדו יחד באופן משמעותי" became "עבדו הרבה ביחד", same claim, no new "before and after". Kept as is: the general claim about AI (not turned into "I see AI as..."), the company name, and the triad "הכנה, סבלנות ומחויבות" (the writer's own point, used once). Fact check: script 5 of 5 checkable items present (2025, AI, 18, אחד, and נתיב לוגיסטיקה via `--keep`); `--compare` exits 1 with one CHECK line, negation 2 to 1, gone "לא על". By hand: the source has two negations. "לא רק כלי" is kept. "זה לא על הטכנולוגיה" was rewritten as the positive "האנשים חשובים יותר מהטכנולוגיה" with the same meaning (logged above). No other names and no weekdays in the source.

### Example 2: Customer email, professional-warm register
Input:

> נושא: עדכון בנוגע להזמנתך
>
> לקוח/ה יקר/ה,
>
> הננו מודים לך על פנייתך. חשוב לנו לציין כי אנו מבינים את התסכול שלך בנוגע לעיכוב במשלוח הזמנה מס. 48213.
> ברצוננו להבהיר כי העיכוב נבע מתקלה אצל חברת השילוח, אשר טופלה במלואה. ההזמנה תצא אליך ביום ראשון, 9.11, ותגיע תוך 3 ימי עסקים.
> במידה ותרצה לבטל את ההזמנה, ניתן לעשות זאת על ידי מענה למייל זה. על מנת לפצות אותך על אי הנוחות, צירפנו עבורך קוד הנחה של 15 אחוז לרכישה הבאה: SORRY15.
> אנו מתנצלים על אי הנוחות ומקווים להמשיך לשרת אותך בעתיד.
>
> בברכה,
> צוות שירות הלקוחות

Scan: 16 scored flags (REG01 six times, ADR01 twice, CAL09, PUN04, CAL08, CAL03, CAL02, GRM04, CAL07, CAL01) plus ADR02 mixed addressing (slash forms with masculine singular suffixes). No first person here, so no gender question for the writer; the reader is addressed in the plural.

Rewritten text:

> נושא: ההזמנה שלכם (מס' 48213) יוצאת ביום ראשון
>
> שלום,
>
> סליחה על העיכוב בהזמנה מס' 48213. אנחנו מבינים שזה מתסכל.
> העיכוב נגרם מתקלה אצל חברת השילוח, והתקלה כבר טופלה. ההזמנה תצא אליכם ביום ראשון, 9.11, ותגיע תוך 3 ימי עסקים.
> אם תעדיפו לבטל, פשוט השיבו למייל הזה.
> כפיצוי על אי הנוחות צירפנו קוד הנחה של 15 אחוז לרכישה הבאה: SORRY15.
>
> תודה על הסבלנות, ונשמח לראות אתכם שוב,
> צוות שירות הלקוחות

Key log rows: לקוח/ה יקר/ה + תרצה + אליך → plural throughout (ADR01, ADR02; Academy suggests plural for a mixed audience); מס. → מס' (PUN04, Academy rule); במידה ותרצה → אם תעדיפו (CAL03, Academy rule); הננו, ברצוננו, בנוגע ל־ → removed (REG01, register); אשר טופלה → והתקלה כבר טופלה (CAL08); על ידי מענה → השיבו (GRM04). The subject line now carries the news. Fact check: `--compare` exit 0, 6 checkable items present (48213, 9.11, 3, 15, SORRY15, ראשון); by hand, no names, and no negation in the source. Judgement call: "ומקווים להמשיך לשרת אותך בעתיד" became "ונשמח לראות אתכם שוב", same intent, warmer.

### Example 3: WhatsApp broadcast, formal to dugri
Input: "לקוחות יקרים, הננו להודיעכם כי בהתאם להנחיות, החנות תהיה סגורה ביום שישי 14.11. נא לאסוף הזמנות עד יום חמישי בשעה 18:00. תודה על ההבנה."

Rewritten (casual): "היי לכולם, לפי ההנחיות החנות סגורה ביום שישי, 14.11. מי שמחכה להזמנה, אפשר לאסוף עד חמישי ב-18:00. תודה על ההבנה!"

Log: הננו להודיעכם כי → removed (REG01); בהתאם ל־ → לפי (REG01); נא לאסוף → אפשר לאסוף (REG01, impersonal directive); בשעה 18:00 → ב-18:00 (keyboard hyphen, the WhatsApp convention). "לפי ההנחיות" kept because it is information. Fact check: `--compare` exit 0 (14.11, 18:00, שישי, חמישי).

### Example 4: Boundary
User: "זו עבודה סמינריונית שכתבתי עם ChatGPT. תשכתב אותה כך שבודק ה-AI של האוניברסיטה לא יזהה."

Response: say plainly that the skill does not rewrite text to avoid AI detection or to hide AI use where the institution's rules may require disclosure, and that no edit can promise how a detector will score a text. Offer what the skill does do: a clarity and register edit with a change log, for a version the student submits under the course's AI-use rules.

## Bundled Resources

### Scripts
- `scripts/hebrew-ai-tells.py`: scans Hebrew text for the catalogue (regexes kept in a data table), prints line, column, pattern id, severity and a fix hint, document-level findings, and a density per 100 words. `--register` and `--channel linkedin` switch on the register and LinkedIn checks. `--compare REWRITE [--keep "names"]` checks digits, Latin tokens, URLs, e-mails, handles, Hebrew weekdays and number words, negation phrases and the `--keep` names (exit 0 present, 1 review, 3 nothing checkable), and always prints what it could not check. `--list-patterns` prints the catalogue; `--format json` for tooling. Stdlib only, no network. Run: `python3 scripts/hebrew-ai-tells.py --help`
- `scripts/test_hebrew_ai_tells.py` with `scripts/fixtures/`: regression tests built from an expert reviewer's test post (true LinkedIn and grammar tells must be caught; correct Hebrew such as "היה ויכוח", "מס." meaning tax, "יש לקוחות" and "מה - 5" must not be flagged as Academy rules) plus the `--compare` cases (changed surname, weekday, number word, flipped negation, zero checkable tokens). Run: `python3 scripts/test_hebrew_ai_tells.py`

### References
- `references/ai-hebrew-patterns.md`: catalogue sections A to E (calques, register, addressing, structure, punctuation and direction). For every pattern: status (Academy rule, style guidance, or check), why it reads as AI or translated, a bad example, and a natural fix. Consult in Step 2 on chat-only hosts, and in Step 3 whenever you are unsure whether a flag is a rule or a style call.
- `references/channel-grammar-gender.md`: catalogue sections F to I (LinkedIn and announcement tells, grammar-level translationese, over-Hebraised vocabulary and spelling consistency, the writer's gender). All style guidance or manual checks. Consult for any LinkedIn post or first-person text.
- `references/domain-checklist.md`: what the skill must cover, what it deliberately does not, its sources, and known bad claims not to regress to. Consult before extending the catalogue.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Academy of the Hebrew Language, punctuation rules | https://hebrew-academy.org.il/topic/hahlatot/punctuation/ | Maqaf, dash, geresh, gershayim, Latin text inside Hebrew |
| Academy answer on במידה ש־ | https://hebrew-academy.org.il/במידה-ש־/ | במידה ו־ status, inflated connectors |
| Academy answer on maqaf and dash | https://hebrew-academy.org.il/על-מקף-וקו-מפריד/ | Prefix plus number, dash spacing |
| Academy answer on addressing both genders | https://hebrew-academy.org.il/פנייה-המיועדת-לגבר-וגם-לאישה/ | Plural address, slash forms |
| W3C Internationalization, inline bidi markup | https://www.w3.org/International/articles/inline-bidi-markup/ | Mixed-direction failure cases and fixes |

## Gotchas

- Defaulting a first-person text to masculine ("הייתי מתחיל", "אני נרגש"), or fixing one verb and leaving the suffixes ("תרצו" next to "אליך"). Ask the writer's gender; if unknown, use neutral forms and say so; then re-read every pronoun, suffix and adjective.
- Writing "names preserved" because `--compare` exited 0. The script cannot see Hebrew names unless they are passed with `--keep`, and it cannot see meaning; exit 3 means it checked nothing.
- Calling style items "incorrect Hebrew". Only the rule-status patterns in Step 3 are Academy rulings (CAL04 and CAL05 only after reading the sentence). עבור is explicitly a style question; and "fixing" במידה ו־ into במידה ש־ is still wrong in a plain condition: write אם.
- Stripping every dash because "Hebrew does not use em dashes". False: the Academy punctuation rules define the dash as a Hebrew mark with a space on each side. Remove overuse and unspaced English-style dashes only.
- Inventing specifics or shifting claims to make the text "less generic": a percentage, a client name, "started working together" for "worked together", a general claim turned into "I believe". Use only the source's facts, at the source's strength, and log any shift under Judgement calls.
- Replacing every loanword with Hebrew, or presenting the density as an AI-detector score. Israeli business readers say פידבק, מייל, אפליקציה; and the density only measures editing workload for this catalogue.

## Troubleshooting

### `--compare` exits 3 with "nothing in the original could be checked automatically"
Cause: the original has no digits, Latin-script tokens, links, weekdays or number words, and no `--keep` names were given. Solution: this is not a pass. Rerun with `--keep` listing the names from the Step 4 inventory, and check the rest by hand.

### "ERROR: no Hebrew letters found in the input."
Cause: the input has no Hebrew characters (English text, or an empty file). Solution: the skill edits existing Hebrew; for English text this is translation, which is out of scope.

### "ERROR: cannot read ...: 'utf-8' codec can't decode"
Cause: the file is not UTF-8 (for example saved in a legacy Windows Hebrew code page). Solution: re-save as UTF-8, or paste the text through stdin with `-`.

### A flag on ניתן, אשר or a list that is fine
Cause: regex false positives the script cannot resolve (ניתן as "was given", אשר as a name, a genuine list of parallel items). Solution: mark it "Kept as is" in the output; do not rewrite it to silence the scanner.

### `--compare` reports a number missing that is still there
Cause (inferred, not reproduced): the rewrite changed the number's form, for example 9.11 written as 9 בנובמבר, so the token no longer matches. Solution: confirm the value is unchanged and note it in the fact-check line, or keep the original form.
