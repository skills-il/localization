# Hebrew Content Writer Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for writing professional content in Hebrew — articles, marketing copy, UX text, emails, and social media — with correct grammar, register, gendered language handling, and SEO optimization.

**Architecture:** Document/Asset Creation skill (Category 1). Embeds Hebrew writing rules, stylistic guidance, register conventions, and SEO best practices for Hebrew content.

**Tech Stack:** SKILL.md, Hebrew grammar reference, SEO guidelines.

---

## Research

### Hebrew Grammar Rules for Professional Writing
- **Verb conjugation:** Hebrew verbs conjugate by gender (masculine/feminine), number (singular/plural), and person (1st/2nd/3rd)
- **Construct state (smichut):** Noun pairs where the first noun changes form — e.g., "beit sefer" (school) not "bayit sefer"
- **Definite article:** "ha-" prefix — both nouns in smichut take it or neither does
- **Spelling conventions:** Academy of Hebrew Language (Ha-Akademia La-Lashon Ha-Ivrit) standards — ktiv maleh (full spelling with vav/yod) vs. ktiv chaser (deficient spelling)
- **Punctuation:** Hebrew uses the same punctuation marks as English but placed left-to-right within RTL text. Geresh (') and gershayim (") are used for abbreviations and acronyms
- **Common mistakes:** Incorrect smichut, mixing ktiv maleh/chaser, wrong gender agreement, misuse of "et" (direct object marker)

### Formal vs. Informal Register
- **Formal (safa gvoha):** Used in legal documents, government communications, academic writing, business correspondence. Full verb forms, passive binyanim (nif'al, pu'al, huf'al), complex sentence structures
- **Informal (safa yevm-yomit):** Used in social media, casual marketing, chat. Shortened forms, slang, loanwords from English/Arabic, colloquial expressions
- **Business register:** Middle ground — professional but accessible. Common in corporate communications, product descriptions, professional emails
- **UX writing:** Short, clear, action-oriented. Uses imperative mood (masculine singular as default, or gender-inclusive alternatives)

### Gendered Language Handling
- **Default masculine (traditional):** Hebrew traditionally defaults to masculine plural for mixed groups
- **Inclusive writing trends:** Growing use of slash notation (XXX/ot), combined forms, or rewording to avoid gendered language
- **Slash notation:** "ha-mashqianim/ot" (the investors, m/f)
- **Neutral rewording:** Use infinitive forms or collective nouns to avoid gendering — "yesh lehashqia" instead of "ata tsarikh lehashqia"
- **Audience consideration:** Tech and startup content trending inclusive; government and legal still mostly traditional

### Hebrew SEO Best Practices
- **Keyword research:** Hebrew search volume differs significantly from English — use Google Keyword Planner with "il" region
- **Morphological variations:** Hebrew morphology means one root can have dozens of surface forms — target root forms and common conjugations
- **Title tags:** 50-60 characters in Hebrew (slightly fewer than English due to character width)
- **Meta descriptions:** 120-150 characters in Hebrew
- **URL slugs:** Transliterated Hebrew or English keywords (Hebrew in URLs is technically valid but less common)
- **Search intent:** Israeli users often search in Hebrew for local topics and English for tech topics — consider bilingual content strategy

### Use Cases
1. **Write marketing copy** — Professional Hebrew ad copy, landing pages, email campaigns
2. **UX writing** — Hebrew interface text, button labels, error messages, onboarding flows
3. **Content editing** — Review and correct Hebrew text for grammar, register, and style
4. **SEO content** — Hebrew blog posts and articles optimized for Israeli search
5. **Gender-inclusive writing** — Rewrite content using inclusive Hebrew language

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: hebrew-content-writer
description: >-
  Write and edit professional content in Hebrew including marketing copy, UX text,
  articles, emails, and social media posts. Use when user asks to write in Hebrew,
  "ktov b'ivrit", create Hebrew marketing content, edit Hebrew text, write Hebrew
  UX copy, or optimize Hebrew content for SEO. Covers grammar rules, formal vs
  informal register, gendered language handling, and Hebrew SEO best practices.
  Do NOT use for Hebrew NLP/ML tasks (use hebrew-nlp-toolkit) or translation
  (use a translation skill).
license: MIT
compatibility: "No network required. Works with Claude Code, Claude.ai, Cursor."
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags: [hebrew, content, writing, seo, copywriting, localization]
---

# Hebrew Content Writer

## Instructions

### Step 1: Identify Content Type and Register
| Content Type | Register | Audience | Key Characteristics |
|-------------|----------|----------|-------------------|
| Legal / Government | Formal (gvoha) | Officials, lawyers | Passive voice, complex sentences, traditional gendering |
| Business / Corporate | Business | Professionals | Clear, professional, moderate formality |
| Marketing / Ads | Business-Casual | General public | Persuasive, benefit-focused, concise |
| UX / Interface | Direct | End users | Imperative mood, ultra-short, action-oriented |
| Social Media | Informal | Young adults | Casual, slang-friendly, emoji-compatible |
| Blog / Article | Business | Readers | Informative, SEO-aware, structured |

### Step 2: Apply Hebrew Grammar Rules

**Spelling Standard — Use Ktiv Maleh (Full Spelling):**
Modern Hebrew content uses ktiv maleh (plene spelling) with vav and yod for vowels:
- Correct: תוכנה (tochnah) not תכנה
- Correct: שירות (sherut) not שרות
- Follow Academy of Hebrew Language guidelines

**Smichut (Construct State) Rules:**
- First noun loses definite article: "beit ha-sefer" (the school) not "ha-beit ha-sefer"
- First noun may change form: bayit -> beit, yom -> yom (unchanged)
- Adjectives agree with the LAST noun in the chain

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

**Option A — Traditional (default for formal/legal):**
Use masculine plural for mixed groups. Standard in government, legal, academic writing.

**Option B — Slash Notation (for business/marketing):**
```
משתמשים/ות יקרים/ות (dear users, m/f)
```

**Option C — Gender-Neutral Rewording (recommended for UX/tech):**
| Instead of | Use |
|-----------|-----|
| המשתמש צריך ללחוץ (the user needs to click, m.) | יש ללחוץ על (click on) |
| אתה יכול לבחור (you can choose, m.) | ניתן לבחור (it is possible to choose) |
| הלקוחות שלנו מרוצים (our customers are satisfied, m.) | שביעות רצון הלקוחות שלנו (the satisfaction of our customers) |

**Ask the user** which approach they prefer if not specified.

### Step 4: Common Hebrew Writing Mistakes to Avoid

| Mistake | Wrong | Correct | Rule |
|---------|-------|---------|------|
| Smichut with ha- on first noun | הבית הספר | בית הספר | Only second noun gets ha- |
| Missing et | ראיתי הכלב | ראיתי את הכלב | Definite direct object needs et |
| Wrong gender agreement | הילדה הלך | הילדה הלכה | Verb must match subject gender |
| Mixed ktiv | תוכנה/תכנה in same text | Pick one consistently | Use ktiv maleh throughout |
| Incorrect vav ha-hipukh | ואז הוא הולך | ואז הוא הלך | Vav ha-hipukh is biblical, not modern |
| Colloquial in formal text | נגיד ש... | לדוגמה... | Match register to context |

### Step 5: Hebrew SEO Optimization

**Keyword Strategy:**
- Research keywords in Hebrew using Google Keyword Planner (region: Israel)
- Account for morphological variations — target root words and common forms
- Example: "ביטוח" (insurance) also search "ביטוחים", "לבטח", "מבוטח"
- Consider bilingual searches — Israelis search English for tech terms

**On-Page SEO for Hebrew:**
- Title tag: 50-60 Hebrew characters, primary keyword near beginning
- Meta description: 120-150 characters, compelling call-to-action
- H1: One per page, contains primary keyword
- URL slug: Transliterated Hebrew ("bituach-briut") or English equivalent
- Alt text: Descriptive Hebrew text for images
- Internal linking: Use Hebrew anchor text

**Content Structure:**
- Use short paragraphs (2-3 sentences) — Hebrew text appears denser than English
- Use headers (H2, H3) every 200-300 words
- Bulleted lists improve readability in Hebrew
- Bold key terms for scanning

## Examples

### Example 1: Marketing Email
User says: "Write a Hebrew marketing email for a SaaS product launch"
Result: Write business-register Hebrew email with compelling subject line, benefit-focused body, clear CTA. Apply SEO principles if it will be a web version. Use gender-inclusive language.

### Example 2: UX Error Message
User says: "Write Hebrew error messages for a login form"
Result: Write short, clear, action-oriented Hebrew text in imperative mood. Use neutral/inclusive phrasing. Examples: "הסיסמה שגויה. יש לנסות שנית" (The password is incorrect. Please try again).

### Example 3: SEO Blog Post
User says: "Write a Hebrew blog post about cloud security for Israeli businesses"
Result: Research Hebrew keywords, write structured article with proper H2/H3 hierarchy, include meta description, use ktiv maleh throughout, business register.

### Example 4: Gender-Inclusive Rewrite
User says: "Make this Hebrew text gender-inclusive"
Result: Identify gendered forms, apply Option C rewording where possible, use slash notation where rewording is awkward, maintain readability and register.

## Troubleshooting

### Error: "Text mixes formal and informal registers"
Cause: Inconsistent tone throughout the content
Solution: Identify the target register at the start and apply it consistently. Common issue when multiple writers contribute or when translating from English.

### Error: "SEO keywords don't match Hebrew search patterns"
Cause: Direct translation of English keywords to Hebrew
Solution: Use Google Keyword Planner with Israel region. Hebrew search patterns differ from English — Israelis may search differently than direct translations suggest.
```
