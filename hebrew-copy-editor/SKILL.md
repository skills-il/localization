---
name: hebrew-copy-editor
description: >-
  Proofread and copy-edit Hebrew text for grammar, spelling, punctuation, style
  consistency, and Academy of Hebrew Language compliance. Use when user asks
  about Hebrew proofreading, grammar checking, ktiv maleh rules, Academy of
  Hebrew Language standards, or Hebrew SEO text review. Covers ktiv maleh
  correction, construct state rules, gershayim punctuation, and gender-inclusive
  language options.
license: MIT
compatibility: >-
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
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
    he: "עורך עברית"
    en: "Hebrew Copy Editor"
  display_description:
    he: >-
      הגהה ועריכה לשונית של טקסטים בעברית בהתאם לכללי האקדמיה ללשון העברית
    en: >-
      Proofread and copy-edit Hebrew text for grammar, spelling, punctuation,
      style consistency, and Academy of Hebrew Language compliance
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# Hebrew Copy Editor

## Instructions

### Step 1: Initial Text Assessment

Assess the text on: register (formal/business/casual), spelling standard (ktiv maleh vs chaser), gender language approach, target audience, and purpose.

### Step 2: Ktiv Maleh (Full Spelling)

Apply Academy of Hebrew Language ktiv maleh standard. Key corrections:
- תכנה -> תוכנה (vav for /o/)
- שרות -> שירות (yod for /i/)
- תקשרת -> תקשורת (vav for /o/)

### Step 3: Grammar Checks

- Subject-verb agreement in gender, number, person
- Construct state (smichut): no article on first noun
- Direct object marker (et): required before definite objects

### Step 4: Punctuation

- Gershayim for acronyms: צה"ל not צהל
- Geresh for abbreviations: פרופ' not פרופ
- No period after gershayim abbreviations

### Step 5: Style Consistency

Match register throughout. Flag deviations.

### Step 6: Gender-Inclusive Language

Three approaches: A) neutral rewording, B) slash notation, C) traditional masculine. Never mix approaches in one document.

### Step 7: Hebrew SEO Review

Check keyword optimization, morphological variations, title tags (50-60 chars), meta descriptions (120-150 chars).

### Step 8: Deliver with Change Log

Provide: summary of changes, corrected text, change log table (original | corrected | category | rule), style recommendations.

## Examples

### Example 1: Proofread a Hebrew Marketing Email
User says: "Check this Hebrew email for grammar and spelling errors"
Actions:
1. Check ktiv maleh compliance (e.g., fix "חנות" to "חנות" with correct vav usage)
2. Verify gender agreement across sentences
3. Fix punctuation: gershayim for acronyms (צה"ל), geresh for abbreviations
4. Check for common calques from English (literal translations)
5. Suggest gender-inclusive alternatives where appropriate
Result: Corrected Hebrew text with tracked changes and explanation for each fix

### Example 2: Edit Hebrew UI Strings for Consistency
User says: "Review these Hebrew UI labels for our app"
Actions:
1. Verify consistent register (formal vs informal) across all strings
2. Check button text follows Hebrew UX conventions (imperative form)
3. Ensure consistent terminology (same Hebrew term for same concept)
4. Validate string length for UI constraints
Result: Consistent Hebrew UI copy with style guide recommendations

## Bundled Resources

### Scripts
- `scripts/check_hebrew.py` -- Scans Hebrew text for common spelling errors, inconsistent ktiv, and punctuation issues. Run: `python scripts/check_hebrew.py --help`

### References
- `references/ktiv-maleh-rules.md` -- Complete ktiv maleh (plene spelling) rules with exception lists, gershayim/geresh usage guide, and Academy of the Hebrew Language guidelines. Consult when verifying specific spelling rules or handling edge cases in ktiv maleh.

## Troubleshooting

### Error: "Text contains nikkud (vowel marks)"
Cause: Source text has nikkud which conflicts with ktiv maleh corrections
Solution: Strip nikkud first using Unicode normalization (remove characters in range U+0591-U+05C7), then apply ktiv maleh rules. Preserve nikkud only in liturgical or educational text.

### Error: "Cannot determine gender for inclusive language"
Cause: Hebrew requires grammatical gender but the target audience is mixed
Solution: Use slash notation (שולח/ת) for short forms, or restructure to avoid gendered verbs where possible. For UI: prefer infinitive forms ("לשלוח" instead of "שלח/שלחי").
