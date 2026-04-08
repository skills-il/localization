---
name: hebrew-rtl-best-practices
description: Implement right-to-left (RTL) layouts for Hebrew web and mobile applications. Use when user asks about RTL layout, Hebrew text direction, bidirectional (bidi) text, Hebrew CSS, "right to left", or needs to build Hebrew UI. Covers CSS logical properties, Tailwind RTL, React/Next.js RTL setup, Hebrew typography, and font selection. Do NOT use for Arabic RTL (similar but different typography) unless user explicitly asks for shared RTL patterns.
license: MIT
compatibility: Works with Claude Code, Claude.ai, Cursor. No network required.
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

**Tailwind CSS RTL (v3.3+ / v4):**

Prefer logical property utilities over `rtl:`/`ltr:` variants:

| Physical class | Logical class | CSS property |
|---------------|--------------|-------------|
| `ml-4` | `ms-4` | `margin-inline-start` |
| `mr-4` | `me-4` | `margin-inline-end` |
| `pl-4` | `ps-4` | `padding-inline-start` |
| `pr-4` | `pe-4` | `padding-inline-end` |
| `left-4` | `start-4` | `inset-inline-start` |
| `right-4` | `end-4` | `inset-inline-end` |
| `rounded-l-lg` | `rounded-s-lg` | `border-start-start-radius` + `border-end-start-radius` |
| `rounded-r-lg` | `rounded-e-lg` | `border-start-end-radius` + `border-end-end-radius` |

```html
<!-- Bad: requires two classes, breaks without dir attribute -->
<div class="ltr:ml-4 rtl:mr-4">...</div>

<!-- Good: single class, auto-mirrors based on dir -->
<div class="ms-4">...</div>
```

Reserve `rtl:` / `ltr:` variants only for cases logical properties cannot handle (e.g., directional icons, transforms).

**Tailwind v4 note:** v4 uses CSS-first configuration (`@import "tailwindcss"` in CSS) instead of `tailwind.config.js`. Logical utilities work identically in both v3 and v4.

**Next.js App Router:**
```tsx
// app/layout.tsx
import { Heebo } from 'next/font/google';

const heebo = Heebo({
  subsets: ['hebrew', 'latin'],
  weight: ['400', '500', '700'],
});

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const isRTL = locale === 'he';

  return (
    <html lang={locale} dir={isRTL ? 'rtl' : 'ltr'}>
      <body className={heebo.className}>{children}</body>
    </html>
  );
}
```

`next/font` self-hosts the font (no external Google Fonts requests, zero layout shift).

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

### Step 6: Common Pitfalls to Check
1. Icons with directional meaning (arrows, back buttons) -- mirror them
2. Progress bars -- should fill from right to left
3. Sliders/carousels -- swipe direction should reverse
4. Form labels -- should be right-aligned
5. Breadcrumbs -- separator direction should reverse
6. Tables -- header alignment and cell alignment
7. Charts -- x-axis may need to reverse for Hebrew readers

## Examples

### Example 1: Convert LTR Component to RTL
User says: "Make this card component work in Hebrew"

Before (LTR-only):
```css
.card {
  margin-left: 16px;
  padding-right: 12px;
  text-align: left;
  border-left: 3px solid blue;
}
```

After (RTL-compatible):
```css
.card {
  margin-inline-start: 16px;
  padding-inline-end: 12px;
  text-align: start;
  border-inline-start: 3px solid blue;
}
```

With Tailwind, replace `ml-4 pr-3 text-left border-l-4` with `ms-4 pe-3 text-start border-s-4`.

### Example 2: Bidi Text Issue
User says: "Numbers are showing backwards in my Hebrew text"

```html
<!-- Wrong: phone number renders as 0544-123-050 -->
<p>התקשרו אלינו: 050-321-4450</p>

<!-- Correct: isolate the LTR content -->
<p>התקשרו אלינו: <span dir="ltr">050-321-4450</span></p>
```

Use `unicode-bidi: isolate` on the containing span for CSS-only solutions.

### Example 3: Tailwind RTL Navigation
User says: "My sidebar is on the wrong side in Hebrew"

```html
<!-- Bad: sidebar stuck on left -->
<aside class="fixed left-0 w-64">...</aside>

<!-- Good: sidebar auto-mirrors -->
<aside class="fixed start-0 w-64">...</aside>

<!-- Back arrow icon still needs rtl: variant -->
<button class="rtl:rotate-180">
  <ArrowLeftIcon />
</button>
```

## Bundled Resources

### References
- `references/css-logical-properties.md` — Complete physical-to-logical CSS property mapping table (margin, padding, border, positioning, text alignment, sizing) plus Hebrew font stack recommendations for sans-serif, serif, and monospace. Consult when converting any LTR stylesheet to RTL-compatible logical properties or choosing Hebrew web fonts.

## Gotchas
- CSS `text-align: left` is wrong for Hebrew. Use `text-align: start` which respects the document direction. Agents frequently hardcode `left` alignment in CSS.
- `margin-left` and `padding-right` do not flip in RTL mode. Use CSS logical properties: `margin-inline-start` and `padding-inline-end` instead. Agents trained on LTR CSS will generate physical properties.
- Flexbox `row` direction auto-reverses in RTL, but `row-reverse` also reverses, causing a double-flip back to LTR order. Agents may add `row-reverse` thinking it creates RTL, but it actually creates LTR within an RTL context.
- Phone numbers, credit card numbers, and code snippets must remain LTR even inside RTL containers. Wrap them in `<bdo dir="ltr">` or use `direction: ltr` on the containing element. Agents often let these inherit RTL.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| MDN CSS Logical Properties | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | Full property list, browser support tables |
| Tailwind CSS RTL Support | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | `rtl:` / `ltr:` variant syntax |
| Tailwind Logical Properties | https://tailwindcss.com/docs/margin#logical-properties | `ms-*`, `me-*`, `ps-*`, `pe-*` utilities |
| Google Fonts Hebrew | https://fonts.google.com/?subset=hebrew | Available Hebrew font families |
| W3C Internationalization | https://www.w3.org/International/articles/inline-bidi-markup/ | Unicode bidi algorithm, markup best practices |

## Troubleshooting

### Error: "Text alignment looks wrong"
Cause: Using `text-align: left` instead of `text-align: start`
Solution: Replace all `left`/`right` in text-align with `start`/`end`.

### Error: "Layout not mirroring"
Cause: Using physical margin/padding instead of logical properties
Solution: Replace all `margin-left`/`margin-right` with `margin-inline-start`/`margin-inline-end`.