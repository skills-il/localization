---
name: hebrew-content-writer
description: Write and edit professional content in Hebrew including marketing copy, UX text, articles, emails, and social media posts. Use when user asks to write in Hebrew, "ktov b'ivrit", create Hebrew marketing content, edit Hebrew text, write Hebrew UX copy, or optimize Hebrew content for SEO. Covers grammar rules, register from formal to dugri, mixed Hebrew/English, gendered language, nikud and numerals, and Hebrew SEO best practices. Do NOT use for Hebrew NLP/ML tasks (use hebrew-nlp-toolkit) or translation (use a translation skill).
license: MIT
---

# Hebrew Content Writer

## Instructions

### Step 1: Identify Content Type and Register
| Content Type | Register | Audience | Key Characteristics |
|-------------|----------|----------|-------------------|
| Legal / Government | Formal (gvoha) | Officials, lawyers | Passive voice, complex sentences, traditional gendering |
| Business / Corporate | Business | Professionals | Clear, professional, moderate formality |
| Marketing / Ads | Business-Casual | General public | Persuasive, benefit-focused, concise |
| Direct / Dugri | Dugri | Israeli general public | Blunt, no softeners, short imperative sentences |
| UX / Interface | Direct | End users | Imperative mood, ultra-short, action-oriented |
| Social Media | Informal | Young adults | Casual, slang-friendly, emoji-compatible |
| Blog / Article | Business | Readers | Informative, SEO-aware, structured |

### Step 2: Apply Hebrew Grammar Rules

**Spelling Standard -- Use Ktiv Maleh (Full Spelling):**
Modern Hebrew content uses ktiv maleh (plene spelling) with vav and yod for vowels:
- Correct: תוכנה (tochnah) not תכנה
- Correct: שירות (sherut) not שרות
- Follow Academy of Hebrew Language guidelines

**Smichut (Construct State) Rules:**
- First noun loses definite article: "beit ha-sefer" (the school) not "ha-beit ha-sefer"
- First noun may change form: bayit -> beit, yom -> yom (unchanged)
- To make a smichut plural, pluralize the first noun: בתי ספר (schools), not בתי ספרים. The second noun keeps whatever number its own meaning needs (ספרי ילדים, חנות בגדים)

**Direct Object Marker (et):**
- Required before definite direct objects: "ra'iti ET ha-sefer" (I saw the book)
- NOT used with indefinite objects: "ra'iti sefer" (I saw a book)
- Common mistake: omitting "et" or using it with indefinite objects

**Subject-Verb Agreement:**
- Verbs agree in gender and number with their subject
- Past tense: also agrees in person
- Present tense: only gender and number (no person distinction)
- Future tense: gender, number, and person

### Step 3: Handle Gendered Language

**Option A -- Traditional (default for formal/legal):**
Use masculine plural for mixed groups. Standard in government, legal, academic writing.

**Option B -- Slash Notation (for business/marketing):**
```
משתמשים/ות יקרים/ות (dear users, m/f)
```

**Option C -- Gender-Neutral Rewording (recommended for UX/tech):**
| Instead of | Use |
|-----------|-----|
| המשתמש צריך ללחוץ (the user needs to click, m.) | יש ללחוץ על (click on) |
| אתה יכול לבחור (you can choose, m.) | אפשר לבחור (it is possible to choose) |
| הלקוחות שלנו מרוצים (our customers are satisfied, m.) | רמת שביעות הרצון בקרב הלקוחות גבוהה (customer satisfaction is high) |

**Ask the user** which approach they prefer if not specified.

### Step 4: Common Hebrew Writing Mistakes to Avoid

| Mistake | Wrong | Correct | Rule |
|---------|-------|---------|------|
| Smichut with ha- on first noun | הבית הספר | בית הספר | Only second noun gets ha- |
| Missing et | ראיתי הכלב | ראיתי את הכלב | Definite direct object needs et |
| Wrong gender agreement | הילדה הלך | הילדה הלכה | Verb must match subject gender |
| Mixed ktiv | תוכנה/תכנה in same text | Pick one consistently | Use ktiv maleh throughout |
| Colloquial in formal text | נגיד ש... | לדוגמה... | Match register to context |

### Step 5: Hebrew SEO Optimization

**Keyword Strategy:**
- Research keywords in Hebrew using Google Keyword Planner (region: Israel)
- Account for morphological variations -- target root words and common forms
- Example: "ביטוח" (insurance) also search "ביטוחים", "לבטח", "מבוטח"
- Consider bilingual searches -- Israelis search English for tech terms

**On-Page SEO for Hebrew:**
- Title tag: primary keyword near the beginning. Google sets no length limit but truncates the displayed title to fit the device width, so keep the key words early
- Meta description: a compelling call-to-action. Google sets no length limit here either and truncates the snippet as needed, so lead with the value
- H1: One per page, contains primary keyword
- URL slug: Google recommends words in the audience's language, and transliterated words where relevant. Hebrew words (percent-encoded in the URL), a transliteration ("bituach-briut") or an English equivalent all work; pick one convention per site
- Alt text: Descriptive Hebrew text for images
- Internal linking: Use Hebrew anchor text

**Content Structure:**
- Use short paragraphs (2-3 sentences) -- Hebrew text appears denser than English
- Use headers (H2, H3) every 200-300 words
- Bulleted lists improve readability in Hebrew
- Bold key terms for scanning

**Advertising sent by fax, automated call, SMS, email or any other electronic message such as WhatsApp (Communications Law section 30A):**
- Send only with the recipient's prior explicit consent in writing; consent given in an electronic message or a recorded call counts. A one-time approach to a business recipient that asks them to agree to receive advertising is not a violation.
- The exception for commercial advertising sent without consent needs ALL three: the recipient gave their details while buying, or negotiating to buy, a product or service and was told they would be used for advertising; they were given a chance to refuse and did not; and the advertising is for a similar kind of product or service.
- State these prominently and clearly, without misleading: that it is advertising, with the word "פרסומת" (or "בקשת תרומה" for a donation request, "תעמולה" for propaganda) at the start and, in an electronic message, in its title or subject line; the advertiser's name, address and contact details; and the recipient's right to refuse at any time with a simple way to do so (for an electronic message, a valid internet address for refusals).
- For an automated call, the recorded message must also say at its start that the recipient may ask to be removed from the mailing list, and let them do so right away, including by pressing a key.
- For an SMS the law replaces that list: the message states only the advertiser's name and contact details for sending a refusal.
- A court may award up to 1,000 NIS per advertising message sent knowingly in breach, without proof of damage.
- Donation requests and propaganda messages have their own variants of these rules (for example, section 30A(b1) for nonprofits and public-benefit companies sending by email); check the statute for those.
- Check the statute text and the Ministry of Communications FAQ (https://www.gov.il/he/pages/17052018_7) before writing campaign copy; these requirements come from the law, not from style.

### Step 6: Write in the Dugri (Direct) Register

"Dugri" is the blunt, no-nonsense register Israelis use and expect in everyday speech and increasingly in product copy, support replies, and startup marketing. It is a distinct mode, not just "informal" - it can be polite and still completely direct. Use it when the brand voice is plain-spoken or when softening would feel evasive to an Israeli reader.

How to write dugri:
- Drop English-style softeners. Cut "we would be happy to", "it might be worth considering", "please feel free to". Say the thing.
- Short sentences, one idea each. Long subordinate clauses read as bureaucratic.
- Second-person imperative is fine and friendly: "תשלחו לנו את המספר" (send us the number), "תבדקו את זה" (check this).
- Lead with the point, then the reason - not the other way around.
- Dugri is not rude. It still uses "תודה" and basic courtesy; it just refuses to pad.

| Padded (avoid) | Dugri (use) |
|----------------|-------------|
| נשמח אם תוכלו לשקול לעדכן את הפרטים | תעדכנו את הפרטים |
| ייתכן שכדאי לבדוק את החיבור לאינטרנט | תבדקו את החיבור לאינטרנט |
| אנחנו מתנצלים על אי הנוחות שנגרמה | סליחה על אי הנוחות. (add "תיקנו את זה" only if it is true) |

### Step 7: Handle Mixed Hebrew/English (Heblish)

Israeli writing routinely mixes Hebrew and English, especially in tech, marketing, and business copy. The decision for each English term is keep, transliterate, or translate:

- **Keep in English** - established tech/product terms with no natural Hebrew equivalent in daily use: API, SaaS, deploy, dashboard (often), email (though "אימייל"/"מייל" is also common). Brand and product names always stay in English.
- **Transliterate** - terms that have entered spoken Hebrew phonetically: "אימייל", "סטארטאפ", "פינטק", "באג", "פיצ'ר". Use when the transliteration is what people actually say.
- **Translate** - terms with a well-established Hebrew word the audience uses: "תוכנה" (software), "משתמש" (user), "הורדה" (download), "עדכון" (update). Forcing English here reads as lazy.

RTL/LTR mixing in one line:
- An English term inside a Hebrew sentence keeps its LTR run; the browser's bidi algorithm usually handles a single word, but wrap longer English strings, codes, or anything with punctuation in `<bdi>` or `dir="ltr"` so surrounding Hebrew punctuation does not reorder.
- Keep a space on both sides of the English run.

English nouns taking Hebrew grammar:
- Hebrew plural: Israelis routinely add Hebrew plural endings to English nouns - "באגים" (bugs), "לינקים" (links), "פיצ'רים" (features). This is natural; do not "correct" it to English plurals.
- Definite article: the Hebrew "ה־" attaches to the English noun - "האפ" (the app), "הלינק" (the link), "הדשבורד" (the dashboard).
- Gender: assign the English noun a Hebrew gender consistently (usually masculine by default) so verbs and adjectives agree - "הדשבורד נטען" not "הדשבורד נטענה".

### Step 8: Nikud, Numerals, and Dates

**When to add nikud (vowel points):**
- Children's content, early-reader material, songs, poetry.
- A single ambiguous word where context does not disambiguate (e.g., to distinguish "סֵפֶר" from "סַפָּר").
- Foreign names and unfamiliar loanwords on first mention.

**When to omit nikud:**
- Modern body copy, UI text, marketing, articles - standard unvocalized Hebrew. Adding nikud throughout looks like a textbook and slows fluent readers.

**Numerals and dates:**
- In running body copy, prefer digits for most numbers ("3 ימים", "תוך 24 שעות"); spelling out is reserved for formal/legal text or numbers that open a sentence.
- Number-gender agreement: 1 and 2 agree with the noun ("יום אחד", "שני ימים"; "שנה אחת", "שתי שנים"). From 3 to 10 the number takes the OPPOSITE-looking form (a known trap): a masculine noun takes the form ending in ה, "שלושה ימים" (three days), and a feminine noun takes the form without it, "שלוש שנים" (three years).
- Dates follow Israeli convention `DD/MM/YYYY` and 24-hour time. See `israeli-ui-design-system` for formatting in UI components.
- Gershayim (״) mark an acronym and go before its last letter (צה״ל, בי״ס); a geresh (׳) marks a shortened word and goes after its last written letter (מס׳, עמ׳). The Academy leaves the choice between double and single quotation marks to house style.
- Put a maqaf (־) between a Hebrew prefix and a number or a Latin-letter word: ב־2026, ה־API, המאה ה־12. A maqaf joins with no spaces; a dash (–) separates and takes a space on each side, except in a range, where it takes no spaces (עמ' 46–53, 16.00–18.00).

### Step 9: Literal-Translation Pitfalls

Calques from English produce text that is grammatical but unmistakably translated. Watch for:

| Pitfall | Wrong (calque) | Natural Hebrew |
|---------|----------------|----------------|
| "to make sense" translated word-for-word | זה עושה סנס / זה עושה שכל | זה הגיוני / זה נשמע הגיוני |
| Over-using generic "אתה" for impersonal "you" | אתה צריך ללחוץ, אתה יכול לראות | יש ללחוץ, אפשר לראות |
| "בכדי" used where plain "כדי" belongs | בכדי לשמור את הקובץ | כדי לשמור את הקובץ |
| Hitpa'el verb given a direct object with "את" | להתחבר את החשבון | לחבר את החשבון / להתחבר לחשבון |
| Literal "at the end of the day" | בסוף היום | בסופו של דבר / בשורה התחתונה |

"בכדי" is not wrong in every context, but it is overused as a fancier-looking "כדי"; default to plain "כדי".

## Examples

### Example 1: Marketing Email
User says: "Write a Hebrew marketing email for a SaaS product launch"
Result: Write business-register Hebrew email with compelling subject line, benefit-focused body, clear CTA. If the email is advertising, first confirm the recipients consented or meet the three-condition exception in Step 5, then start the subject line with "פרסומת" and include the sender details and refusal address. Apply SEO principles if it will be a web version. Use gender-inclusive language.

### Example 2: UX Error Message
User says: "Write Hebrew error messages for a login form"
Result: Write short, clear, action-oriented Hebrew text in imperative mood. Use neutral/inclusive phrasing. Examples: "הסיסמה שגויה. נסו שוב" (The password is incorrect. Try again).

### Example 3: SEO Blog Post
User says: "Write a Hebrew blog post about cloud security for Israeli businesses"
Result: Research Hebrew keywords, write structured article with proper H2/H3 hierarchy, include meta description, use ktiv maleh throughout, business register.

### Example 4: Gender-Inclusive Rewrite
User says: "Make this Hebrew text gender-inclusive"
Result: Identify gendered forms, apply Option C rewording where possible, use slash notation where rewording is awkward, maintain readability and register.

## Bundled Resources

### References
- `references/hebrew-grammar-quick-ref.md` - Concise Hebrew grammar reference covering all 7 binyanim (verb patterns) with usage guidance by register, ktiv maleh vs. ktiv chaser spelling examples, common smichut (construct state) forms, and four gender-inclusive writing patterns with before/after examples. Consult when writing or editing Hebrew content and need to verify grammar rules, choose the correct register, or apply gender-neutral phrasing.

## Gotchas
- Agents default to formal/literary Hebrew (safa gvoha) when writing marketing or UI text. Israeli users expect casual, conversational Hebrew. Use colloquial phrasing, not textbook Hebrew.
- Hebrew punctuation differs from English: the geresh (') and gershayim (") are used for abbreviations (e.g., tsahal) and acronyms, not for quotation. Agents may strip these or replace them with standard ASCII quotes.
- Agents tend to transliterate English idioms literally into Hebrew, producing unnatural text. "Think outside the box" does not translate directly; use native Hebrew expressions instead.
- Hebrew has grammatical gender that must agree between nouns, verbs, and adjectives. Agents often use masculine defaults even when addressing a female user or a feminine noun.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Academy of the Hebrew Language | https://hebrew-academy.org.il | Official spelling rules, loanword decisions, new terms |
| Milog online dictionary | https://milog.co.il | Modern Hebrew usage, register, common phrasing |
| Ravmilim online dictionary | https://www.ravmilim.co.il | Synonyms, collocations, grammatical info |
| Academy decisions (ההחלטות) | https://hebrew-academy.org.il/topic/hahlatot/ | Academy decisions on grammar, spelling and terminology |
| Academy punctuation rules (כללי הפיסוק) | https://hebrew-academy.org.il/topic/hahlatot/punctuation/ | Maqaf, gershayim, geresh, quotation marks |
| Hebrew style guide (Wikipedia) | https://he.wikipedia.org/wiki/ויקיפדיה:לשון | Community-maintained modern Hebrew language and style conventions |

## Troubleshooting

### Error: "Text mixes formal and informal registers"
Cause: Inconsistent tone throughout the content
Solution: Identify the target register at the start and apply it consistently. Common issue when multiple writers contribute or when translating from English.

### Error: "SEO keywords don't match Hebrew search patterns"
Cause: Direct translation of English keywords to Hebrew
Solution: Use Google Keyword Planner with Israel region. Hebrew search patterns differ from English -- Israelis may search differently than direct translations suggest.