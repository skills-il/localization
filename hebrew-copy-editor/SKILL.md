---
name: hebrew-copy-editor
description: >-
  Proofread and copy-edit Hebrew text for grammar, spelling, punctuation, style
  consistency, and Academy of Hebrew Language compliance. Use when user asks to
  edit Hebrew text, "tagih li et ha-ivrit", proofread a Hebrew document, fix
  Hebrew grammar, check ktiv maleh, review Hebrew style consistency, or apply
  gender-inclusive Hebrew writing. Covers all 7 binyanim, construct state
  (smichut), definite direct object marking, register matching, and Hebrew SEO
  copy. Do NOT use for translation or content generation from scratch (use
  hebrew-content-writer).
license: MIT
compatibility: 'No network required. Works with Claude Code, Claude.ai, Cursor.'
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags:
    he:
      - עריכה
      - עברית
      - דקדוק
      - הגהה
      - כתיב
    en:
      - editing
      - hebrew
      - grammar
      - proofreading
      - spelling
  display_name:
    he: עורך עברית
    en: Hebrew Copy Editor
  display_description:
    he: הגהה ועריכה לשונית של טקסטים בעברית בהתאם לכללי האקדמיה ללשון העברית
    en: >-
      Proofread and copy-edit Hebrew text for grammar, spelling, punctuation,
      style consistency, and Academy of Hebrew Language compliance.
---

# Hebrew Copy Editor

## Instructions

### Step 1: Initial Text Assessment

Before making corrections, assess the text on these dimensions:

| Dimension | What to Check |
|-----------|--------------|
| Register | Is the tone consistent? (formal, business, casual, literary) |
| Spelling standard | Is ktiv maleh (full) or ktiv chaser (deficient) used? Are they mixed? |
| Gender language | What approach is used? (traditional, slash notation, gender-neutral) |
| Target audience | Who reads this? (general public, professionals, government, youth) |
| Purpose | What is the text for? (marketing, legal, UX, editorial, academic) |

Report the assessment to the user before proceeding with edits. This ensures alignment on expectations.

### Step 2: Apply Ktiv Maleh (Full Spelling) Rules

Modern Hebrew follows the Academy of Hebrew Language's ktiv maleh standard. The key principle: use vav and yod to represent vowels.

**Common corrections:**

| Ktiv Chaser (wrong in modern) | Ktiv Maleh (correct) | Vowel Added |
|------------------------------|---------------------|-------------|
| תכנה | תוכנה | vav for /o/ |
| שרות | שירות | yod for /i/ |
| מדיניות | מדיניות | (already correct) |
| ברור | ברור | (already correct) |
| תקשרת | תקשורת | vav for /o/ |
| ספרות | סיפרות | yod for /i/ (when meaning "literature") |
| חנוך | חינוך | yod for /i/ |

**Exception words that do NOT add vav/yod:**
- Words where the spelling is well-established: כל (kol), על (al), של (shel)
- Biblical/liturgical quotes: retain original spelling
- Proper nouns and brand names: keep original form

**Double-vav and double-yod rules:**
- Consonantal vav (v sound) next to vowel vav: write two vavs. Example: תוו (tav, musical note)
- Consonantal yod (y sound) next to vowel yod: write two yods. Example: הייתי (hayiti)

### Step 3: Check Grammar Fundamentals

**Subject-verb agreement:**
- Past tense: agrees in person, gender, and number
- Present tense: agrees in gender and number only (no person distinction)
- Future tense: agrees in person, gender, and number

| Error | Correction | Rule |
|-------|-----------|------|
| הילדה הלך הביתה | הילדה הלכה הביתה | Verb must match feminine subject |
| הסטודנטים למדה | הסטודנטים למדו | Verb must match plural subject |
| אני הולכת (male speaker) | אני הולך | Present tense matches speaker gender |

**Construct state (smichut) rules:**
1. First noun loses its definite article: "beit ha-sefer" not "ha-beit ha-sefer"
2. First noun may change vowel form: bayit becomes beit, davar becomes dvar
3. Feminine -a ending becomes -at: mishpacha becomes mishpachat
4. Adjectives agree with the LAST noun: "beit sefer gadol" (big school, masc. because sefer is masc.)

| Error | Correction | Rule |
|-------|-----------|------|
| הבית ספר | בית הספר | No article on first noun |
| בית הספר הגדולה | בית הספר הגדול | Adj. agrees with sefer (masc.) |
| חדר של אוכל | חדר אוכל | Use smichut, not "shel" |

**Direct object marker (et):**
- Required before definite direct objects: "ra'iti ET ha-yeled" (I saw the child)
- Not used with indefinite objects: "ra'iti yeled" (I saw a child)
- Required with proper nouns: "pagashti ET David" (I met David)
- Required with possessive suffixes: "ahavti ET ima sheli" (I loved my mother)

### Step 4: Punctuation and Typography

**Hebrew-specific punctuation rules:**
- Geresh (') and gershayim ("): used for acronyms (rashei tevot), e.g., צה"ל, ת"ז
- Maqaf (Hebrew hyphen ־): connects compound words. Unicode U+05BE. In practice, the regular hyphen (-) is acceptable in digital text.
- Quotation marks: Hebrew uses regular quotation marks ("...") or guillemets. Israeli convention increasingly uses "..." (same as English).
- Exclamation and question marks: same as English, placed at the end of the sentence (which is the LEFT side in RTL display).

**Common punctuation errors:**
| Error | Correction | Rule |
|-------|-----------|------|
| צהל | צה"ל | Acronyms get gershayim between last two letters |
| פרופ דוד כהן | פרופ' דוד כהן | Abbreviations get geresh |
| ד"ר. כהן | ד"ר כהן | No period after gershayim abbreviation |
| 5,000,000 ש"ח | 5,000,000 ₪ | Use shekel symbol, not abbreviation, in modern text |

### Step 5: Style Consistency Checks

**Register consistency:**
Identify the register and flag any deviations.

| Register | Markers | Avoid |
|----------|---------|-------|
| Formal (gvoha) | Passive constructions, long sentences, traditional gender | Slang, contractions, first person |
| Business | Clear structure, professional terms, moderate formality | Overly casual, street Hebrew |
| Casual | Short sentences, contractions, colloquial expressions | Formal passive, archaic words |
| UX/Interface | Imperative mood, ultra-short, action verbs | Long explanations, passive voice |

**Common style errors:**

| Context | Error | Fix |
|---------|-------|-----|
| Formal document | נגיד ש... (let's say...) | לדוגמה... (for example...) |
| UX button | ללחוץ כאן על מנת להמשיך | המשך (Continue) |
| Marketing | המוצר שלנו הוא טוב מאוד | המוצר שלנו מוביל ב... (Our product leads in...) |
| Legal | אתה חייב לשלם | על המשתמש/ת לשלם (The user must pay) |

### Step 6: Gender-Inclusive Language Review

Three approaches, choose based on context:

**Approach A: Gender-neutral rewording (recommended for tech/UX):**
| Gendered | Gender-neutral | Method |
|----------|---------------|--------|
| המשתמש צריך (the user needs, m.) | יש צורך ב... / נדרש... | Impersonal construction |
| אתה יכול לבחור (you can choose, m.) | ניתן לבחור | "It is possible to" |
| הלקוחות מרוצים (customers are satisfied, m.) | שביעות רצון לקוחותינו | Noun-based rephrasing |
| הוא/היא | מי ש... (whoever...) | Relative clause |

**Approach B: Slash notation (common in business):**
```
משתמשים/ות יקרים/ות (dear users)
העובד/ת רשאי/ת (the employee may)
```

**Approach C: Traditional masculine (only for legal/government if specified):**
Use masculine plural for mixed groups. Note this is becoming less common even in formal contexts.

**Rules for gender-inclusive editing:**
1. Never mix approaches within the same document
2. If the text already uses one approach, maintain it
3. If no approach is established, recommend Approach A for new content
4. Slash notation requires matching gender in ALL parts: adjectives, verbs, nouns

### Step 7: Hebrew SEO Copy Review

When editing web content or marketing copy, check these SEO factors:

**Hebrew keyword optimization:**
- Verify keywords match actual Israeli search patterns (not direct English translations)
- Check for morphological variations: include root forms and common inflections
- Example: for "insurance" target both "ביטוח" and "לבטח", "מבוטח", "ביטוחים"

**Hebrew meta content:**
- Title tags: 50-60 Hebrew characters, primary keyword near start
- Meta descriptions: 120-150 characters, include call-to-action
- Header hierarchy: H1 once per page, H2/H3 for structure
- Hebrew text is denser than English: shorter paragraphs (2-3 sentences)

**Readability for Hebrew:**
- Average sentence length: 15-20 words (shorter than English norm)
- Use active voice unless formal register requires passive
- Break up long construct chains: "the result of the investigation of the committee" is hard to read; restructure
- Bold key terms for scanning

### Step 8: Deliver the Edited Text

Format your response with:
1. **Summary of changes**: categorized (grammar, spelling, style, gender, punctuation)
2. **Edited text**: full corrected version
3. **Change log**: a table showing original vs. corrected text with the rule applied
4. **Style recommendations**: suggestions for improvement beyond errors

Example change log format:

| Original | Corrected | Category | Rule |
|----------|----------|----------|------|
| הבית ספר | בית הספר | Grammar | Smichut: no article on first noun |
| תכנה | תוכנה | Spelling | Ktiv maleh: vav for /o/ |
| המשתמש צריך | יש צורך | Gender | Gender-neutral impersonal |

## Examples

### Example 1: Business Email Proofreading
**Input**: "Check this Hebrew business email for errors and style"
**Output**: Assessment of register (business), identification of ktiv chaser errors, flag mixed gender language, corrected version with change log.

### Example 2: Legal Document Review
**Input**: "Edit this Hebrew contract for grammar and consistency"
**Output**: Assessment of formal register, check smichut constructions, verify legal terminology consistency, ensure proper use of gendered language per legal convention, corrected version.

### Example 3: Marketing Copy Polish
**Input**: "Polish this Hebrew marketing page for our SaaS product"
**Output**: Register check (business-casual), SEO keyword review, gender-inclusive language audit, readability improvements, corrected version with all changes documented.

### Example 4: UX Text Review
**Input**: "Review all Hebrew UI strings in this file"
**Output**: Check for imperative mood consistency, verify ultra-short format, flag passive constructions, ensure gender-neutral language (Approach A), corrected strings with explanations.

### Example 5: Academic Text Editing
**Input**: "Edit this Hebrew research abstract"
**Output**: Verify formal register, check academic conventions, verify smichut chains, confirm ktiv maleh throughout, review subject-verb agreement, corrected version.

## Troubleshooting

- **Issue**: User sends text with mixed ktiv maleh and ktiv chaser
  **Solution**: Standardize to ktiv maleh throughout, unless the text includes direct quotes from sources that use ktiv chaser (in which case, preserve the original spelling in quotes and note the discrepancy).

- **Issue**: Text uses gender language inconsistently
  **Solution**: First determine the intended approach (ask if unclear). Then apply that approach consistently throughout. Flag sentences where gender-neutral rewording changes the meaning.

- **Issue**: Construct state (smichut) vs. "shel" disagreement with user
  **Solution**: Modern Hebrew increasingly uses "shel" where smichut would be traditional. For formal/literary text, prefer smichut. For casual/spoken-register text, "shel" is acceptable. Explain the distinction to the user.

- **Issue**: Acronym formatting varies in the document
  **Solution**: Standardize all acronyms to use gershayim between the last two letters (e.g., צה"ל, ת"ז, בג"ץ). Single-letter abbreviations use geresh (e.g., פרופ', ד"ר). Be consistent.

- **Issue**: Numbers and currency formatting inconsistent
  **Solution**: For NIS amounts, use the shekel symbol. For percentages, place the % after the number. Dates in DD/MM/YYYY or Hebrew month name format. Be consistent with thousands separators (commas).
