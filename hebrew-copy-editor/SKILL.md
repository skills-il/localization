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
