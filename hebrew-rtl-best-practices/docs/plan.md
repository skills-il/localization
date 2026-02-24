# Hebrew RTL Best Practices Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill that teaches Claude to properly implement right-to-left (RTL) layouts for Hebrew web and mobile applications, including bidirectional text handling.

**Architecture:** Document/Asset Creation skill (Category 1). Embeds CSS/HTML RTL patterns, bidirectional text handling rules, and Hebrew typography best practices.

**Tech Stack:** SKILL.md, references for RTL CSS patterns and Hebrew typography guides.

---

## Research

### RTL Challenges in Hebrew
- Hebrew text flows right-to-left, but numbers and Latin text flow left-to-right
- Mixed content (bidi) requires proper Unicode Bidi Algorithm handling
- CSS `direction: rtl` is necessary but not sufficient
- Logical CSS properties (`margin-inline-start` vs `margin-left`) are critical
- Many UI frameworks have incomplete RTL support

### Key CSS Properties for RTL
- `direction: rtl` — Sets text direction
- `dir="rtl"` on HTML element — Better than CSS-only
- Logical properties: `margin-inline-start`, `padding-inline-end`, `border-inline-start`
- `text-align: start` vs `text-align: right`
- Flexbox: `flex-direction` automatically reverses in RTL
- Grid: Follows document direction

### Hebrew Typography
- Common web fonts: Heebo, Assistant, Rubik, Open Sans Hebrew, Noto Sans Hebrew
- Font size: Hebrew generally needs ~10% larger than Latin for same readability
- Line height: Hebrew benefits from slightly more generous line height (~1.6-1.8)
- Letter spacing: Not recommended for Hebrew (breaks ligature reading)

### Use Cases
1. **RTL layout setup** — Configure HTML/CSS for Hebrew-first applications
2. **Bidi text handling** — Handle mixed Hebrew/English/number content
3. **Component RTL** — Make specific UI components RTL-compatible
4. **Framework-specific RTL** — React, Vue, Tailwind, MUI RTL configuration
5. **Testing RTL** — Verify RTL rendering and common pitfalls

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: hebrew-rtl-best-practices
description: >-
  Implement right-to-left (RTL) layouts for Hebrew web and mobile applications.
  Use when user asks about RTL layout, Hebrew text direction, bidirectional
  (bidi) text, Hebrew CSS, "right to left", or needs to build Hebrew UI. Covers
  CSS logical properties, Tailwind RTL, React/Vue RTL, Hebrew typography, and
  font selection. Do NOT use for Arabic RTL (similar but different typography)
  unless user explicitly asks for shared RTL patterns.
license: MIT
compatibility: "Works with Claude Code, Claude.ai, Cursor. No network required."
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags: [rtl, hebrew, css, layout, typography, bidi]
---

# Hebrew RTL Best Practices

## Instructions

### Step 1: Set Up Document Direction
Always start with the HTML attribute (not just CSS):

```html
<html lang="he" dir="rtl">
```

This tells browsers, screen readers, and CSS to use RTL as the base direction.

### Step 2: Use CSS Logical Properties
NEVER use physical directional properties for layout:

| Physical (avoid) | Logical (use) |
|-------------------|--------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `border-left` | `border-inline-start` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `float: left` | `float: inline-start` |
| `left: 10px` | `inset-inline-start: 10px` |

This ensures the layout automatically mirrors in RTL mode.

### Step 3: Handle Bidirectional Text
When mixing Hebrew and English/numbers:

```css
/* Isolate embedded LTR content */
.ltr-content {
  unicode-bidi: isolate;
  direction: ltr;
}

/* For inline elements with mixed content */
.bidi-override {
  unicode-bidi: bidi-override;
}
```

Common bidi issues:
- Phone numbers appearing reversed: Wrap in `<bdo dir="ltr">`
- Punctuation at wrong end of sentence: Use `unicode-bidi: isolate`
- URLs/emails in Hebrew text: Wrap in `<span dir="ltr">`

### Step 4: Hebrew Typography
Recommended font stack:
```css
font-family: 'Heebo', 'Assistant', 'Rubik', 'Noto Sans Hebrew', sans-serif;
```

Typography settings:
```css
body[dir="rtl"] {
  font-size: 16px; /* Hebrew needs slightly larger than Latin */
  line-height: 1.7;
  letter-spacing: normal; /* NEVER add letter-spacing for Hebrew */
  word-spacing: 0.05em; /* Slight word spacing improves readability */
}
```

### Step 5: Framework-Specific Setup

**Tailwind CSS RTL:**
```js
// tailwind.config.js
module.exports = {
  // Tailwind v3.1+ has built-in RTL support
  // Use rtl: and ltr: variants
}
```
```html
<div class="ltr:ml-4 rtl:mr-4">
  <!-- Or better: use logical utilities if available -->
</div>
```

**React with MUI:**
```jsx
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import rtlPlugin from 'stylis-plugin-rtl';
import { prefixer } from 'stylis';

const cacheRtl = createCache({
  key: 'muirtl',
  stylisPlugins: [prefixer, rtlPlugin],
});

const theme = createTheme({ direction: 'rtl' });
```

**Next.js:**
Add `dir="rtl"` to root layout and configure font loading for Hebrew fonts.

### Step 6: Common Pitfalls to Check
1. Icons with directional meaning (arrows, back buttons) — mirror them
2. Progress bars — should fill from right to left
3. Sliders/carousels — swipe direction should reverse
4. Form labels — should be right-aligned
5. Breadcrumbs — separator direction should reverse
6. Tables — header alignment and cell alignment
7. Charts — x-axis may need to reverse for Hebrew readers

## Examples

### Example 1: Convert LTR Component to RTL
User says: "Make this card component work in Hebrew"
Result: Replace all physical CSS properties with logical equivalents, add dir="rtl", adjust font stack.

### Example 2: Bidi Text Issue
User says: "Numbers are showing backwards in my Hebrew text"
Result: Wrap numeric content in `<span dir="ltr">` with `unicode-bidi: isolate`.

## Troubleshooting

### Error: "Text alignment looks wrong"
Cause: Using `text-align: left` instead of `text-align: start`
Solution: Replace all `left`/`right` in text-align with `start`/`end`.

### Error: "Layout not mirroring"
Cause: Using physical margin/padding instead of logical properties
Solution: Replace all `margin-left`/`margin-right` with `margin-inline-start`/`margin-inline-end`.
```
