---
name: hebrew-rtl-best-practices
description: Implement right-to-left (RTL) layouts for Hebrew web applications. Use when user asks about RTL layout, Hebrew text direction, bidirectional (bidi) text, Hebrew CSS, "right to left", or needs to build a Hebrew web UI. Covers CSS logical properties, the :dir() pseudo-class, Tailwind RTL, React/Next.js RTL setup, icon mirroring, Hebrew typography, and font selection. Do NOT use for Arabic RTL (similar but different typography) unless user explicitly asks for shared RTL patterns, or for native mobile RTL (React Native I18nManager, SwiftUI, Android) which is out of scope.
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

When you genuinely need a direction-specific rule that logical properties cannot express, prefer the `:dir()` pseudo-class over `[dir="rtl"]` attribute selectors:

```css
/* Modern: matches the resolved direction, including dir="auto" and inheritance */
.chevron:dir(rtl) { transform: scaleX(-1); }

/* Older approach: only matches an explicit dir attribute on/above the element */
[dir="rtl"] .chevron { transform: scaleX(-1); }
```

`:dir()` is part of Selectors Level 4 and resolves the *computed* direction, so it also works for elements whose direction comes from `dir="auto"` or from an ancestor, where an attribute selector would miss them. Browser support: Chrome and Edge shipped it in version 120 (late 2023), Firefox has supported it for years, and Safari added it in 16.4, so it is now Baseline (widely available). For older-browser support, keep an `[dir="rtl"]` fallback rule or use a logical property instead. Check current support at https://caniuse.com/css-dir-pseudo.

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

**Numbers and dates:** Standalone numbers and DD/MM/YYYY dates inside Hebrew text usually render fine because digits are weak-LTR, but a number that is immediately followed by a sign, currency, or a second number can flip. When a value must keep a fixed visual order, isolate it with `<span dir="ltr">` or `unicode-bidi: isolate` rather than trusting the default bidi resolution.

**Format the value, then isolate it.** Bidi isolation only stops a *correct* string from flipping; it does not produce the right string. Use `Intl` to format, then isolate: `Intl.NumberFormat('he-IL', { style: 'currency', currency: 'ILS' })` for shekel amounts and `Intl.DateTimeFormat('he-IL')` for dates, and wrap the output in `<span dir="ltr">` (or `unicode-bidi: isolate`) if it sits inline in Hebrew prose. Devs commonly conflate the two and apply bidi fixes to a formatting bug (or vice versa).

**Form inputs need `dir="auto"`.** Put `dir="auto"` on every `<input>` and `<textarea>` so each value resolves its own base direction. This is the most visible end-user RTL bug: an email or an English word typed into a Hebrew form jumps to the wrong side without it. Note that the placeholder does not trigger auto-detection, so set the resting direction with CSS if the empty-field look matters.

**`<bdi>` vs `<bdo>`:** use `<bdo dir="ltr">` only when you want to *force* a direction (it overrides the bidi algorithm). For user-generated or unknown-direction content, prefer `<bdi>`, which *isolates* the content so its direction is auto-detected and cannot leak into the surrounding text:

```html
<!-- User name could be Hebrew or Latin; bdi isolates it either way -->
<p>שלום, <bdi>{{ userName }}</bdi>, ברוך הבא</p>
```

For free-text fields, `dir="auto"` (or `unicode-bidi: plaintext` in CSS) lets the browser pick the base direction per value, which is the correct default for comments, names, and search queries where you do not know the language in advance.

**Shadows and gradients do not auto-flip.** CSS logical properties mirror layout, but `box-shadow`, `text-shadow`, and `linear-gradient` offsets/angles are physical and stay fixed when direction flips. A shadow offset of `4px 4px` that looks correct in LTR will point the "wrong" way relative to an RTL layout. The same physical-not-logical trap applies to `transform-origin`, `background-position`, and `translateX`-based keyframe animations (slide-in drawers, carousels, progress shimmer). Flip each explicitly with a `:dir(rtl)` (or `[dir="rtl"]`) override when its direction is meaningful.

### Step 4: Mirror Directional Icons

Icon mirroring is one of the highest-frequency RTL bugs. The rule: mirror icons whose meaning is tied to reading direction, leave everything else alone.

**Mirror these** (their direction encodes "forward/back/next/previous" relative to reading order):
- Navigation arrows, back/forward buttons, breadcrumb chevrons
- "Send" / submit arrows, carousel and pagination arrows
- Indentation, list-nesting, and reply arrows
- Progress indicators that imply forward motion

**Do NOT mirror these** (mirroring makes them wrong or unrecognizable):
- Logos and brand marks
- Checkmarks and X / close icons
- Media play buttons (a play button always points right, it refers to the timeline, not reading direction)
- Clocks and analog-time icons (clockwise is universal)
- Icons depicting real-world objects with a fixed orientation (a phone handset, a magnifying glass with the handle, most product icons)

Technique, mirror with a horizontal flip transform:

```css
/* Flip only when the document direction is RTL */
.icon-directional:dir(rtl) { transform: scaleX(-1); }
```

```html
<!-- Tailwind: rtl: variant for the cases logical properties cannot cover -->
<button class="rtl:-scale-x-100">
  <ArrowLeftIcon />
</button>
```

Many icon sets (for example Material Symbols) already ship RTL-aware variants, prefer those over flipping when available, because a flipped icon can mis-render fine detail or embedded text.

### Step 5: Hebrew Typography
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

### Step 6: Framework-Specific Setup

**Tailwind CSS RTL (v4, current; logical utilities since v3.3):**

Prefer logical property utilities over `rtl:`/`ltr:` variants:

| Physical class | Logical class | CSS property |
|---------------|--------------|-------------|
| `ml-4` | `ms-4` | `margin-inline-start` |
| `mr-4` | `me-4` | `margin-inline-end` |
| `pl-4` | `ps-4` | `padding-inline-start` |
| `pr-4` | `pe-4` | `padding-inline-end` |
| `left-4` | `inset-s-4` (was `start-4`) | `inset-inline-start` |
| `right-4` | `inset-e-4` (was `end-4`) | `inset-inline-end` |
| `rounded-l-lg` | `rounded-s-lg` | `border-start-start-radius` + `border-end-start-radius` |
| `rounded-r-lg` | `rounded-e-lg` | `border-start-end-radius` + `border-end-end-radius` |

```html
<!-- Bad: requires two classes, breaks without dir attribute -->
<div class="ltr:ml-4 rtl:mr-4">...</div>

<!-- Good: single class, auto-mirrors based on dir -->
<div class="ms-4">...</div>
```

Reserve `rtl:` / `ltr:` variants only for cases logical properties cannot handle (e.g., directional icons, transforms).

**Tailwind v4 note:** v4 (GA since early 2025, currently v4.3) uses CSS-first configuration (`@import "tailwindcss"` in CSS) instead of `tailwind.config.js`. Logical utilities work identically in both v3 and v4. As of v4.3 (May 2026) the logical *inset* utilities `start-*`/`end-*` are deprecated in favor of `inset-s-*`/`inset-e-*` (the old names still work); the margin/padding utilities `ms-*`/`me-*`/`ps-*`/`pe-*` are unaffected.

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

Current MUI (v9 as of 2026) uses the official fork `@mui/stylis-plugin-rtl`, not the older community `stylis-plugin-rtl` package. The official fork fixes CSS-layers issues and supports current Stylis versions; this has been the recommended setup since MUI v6.

```jsx
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { rtlPlugin } from '@mui/stylis-plugin-rtl';
import { prefixer } from 'stylis';

const cacheRtl = createCache({
  key: 'muirtl',
  stylisPlugins: [prefixer, rtlPlugin],
});

const theme = createTheme({ direction: 'rtl' });
```

Confirm the exact import name and setup against the current MUI RTL guide (https://mui.com/material-ui/customization/right-to-left/) for your MUI version.

**Portalled UI (modals, dropdowns, tooltips, toasts).** Components rendered through a portal (React `createPortal`, Radix, MUI Menu, Floating UI) mount at `document.body` and inherit direction from there, but many libraries assume LTR. Set `dir` on `<html>` AND pass the library's own direction setting: Radix needs a `<DirectionProvider dir="rtl">` wrapper, MUI needs `direction: 'rtl'` in the theme. Otherwise popovers open on the wrong side even when the rest of the page is correct.

### Step 7: Common Pitfalls to Check
1. Directional icons -- mirror them (see Step 4 for which icons to flip and which to leave)
2. Progress bars -- should fill from right to left
3. Sliders/carousels -- swipe direction should reverse
4. Form labels -- should be right-aligned
5. Breadcrumbs -- separator direction should reverse
6. Tables -- columns reorder automatically, but force numeric, code, and date cells back to LTR with `<td dir="ltr">` or `text-align: end`
7. Charts -- x-axis may need to reverse for Hebrew readers (SVG has no logical properties, so use the charting library's `reversed`/`rtl` option, not CSS)
8. Shadows and gradients -- physical offsets/angles do not auto-flip (see Step 3)
9. Fixed and sticky chrome (headers, toasts, FABs, drawers) -- hardcoded `left: 0` / `right: 0` does not flip; use `inset-inline-start` / `inset-inline-end`
10. Scrollbars sit on the left in RTL -- reserve space with `scrollbar-gutter: stable` to avoid reflow; `text-wrap: balance` improves Hebrew headings

### Step 8: Verify the RTL Layout
Authoring rules are not enough, verify before shipping:
- Flip the whole app to `dir="rtl"` and scan for anything that did not move (it is still using a physical property).
- Test one canonical mixed string in every text surface: `שלום John 050-1234567 ₪1,234` exercises Hebrew, Latin, a phone number, and a currency amount at once.
- Open every modal, dropdown, tooltip, and toast (portalled UI is the most common RTL miss).
- Check fixed/sticky chrome, charts/SVG, and form fields with `dir="auto"`.

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

<!-- Good: sidebar auto-mirrors (inset-s-0; start-0 is the deprecated alias) -->
<aside class="fixed inset-s-0 w-64">...</aside>

<!-- Back arrow icon still needs rtl: variant (horizontal flip, not rotate-180 which also flips vertically) -->
<button class="rtl:-scale-x-100">
  <ArrowLeftIcon />
</button>
```

## Bundled Resources

### References
- `references/css-logical-properties.md` - Complete physical-to-logical CSS property mapping table (margin, padding, border, positioning, text alignment, sizing) plus Hebrew font stack recommendations for sans-serif, serif, and monospace. Consult when converting any LTR stylesheet to RTL-compatible logical properties or choosing Hebrew web fonts.

## Gotchas
- CSS `text-align: left` is wrong for Hebrew. Use `text-align: start` which respects the document direction. Agents frequently hardcode `left` alignment in CSS.
- `margin-left` and `padding-right` do not flip in RTL mode. Use CSS logical properties: `margin-inline-start` and `padding-inline-end` instead. Agents trained on LTR CSS will generate physical properties.
- Flexbox `row` direction auto-reverses in RTL, but `row-reverse` also reverses, causing a double-flip back to LTR order. Agents may add `row-reverse` thinking it creates RTL, but it actually creates LTR within an RTL context.
- Phone numbers, credit card numbers, and code snippets must remain LTR even inside RTL containers. Wrap them in `<bdo dir="ltr">` or use `direction: ltr` on the containing element. Agents often let these inherit RTL.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| MDN CSS Logical Properties | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | Full property list, browser support tables |
| MDN `:dir()` pseudo-class | https://developer.mozilla.org/en-US/docs/Web/CSS/:dir | Syntax, behavior vs `[dir]` attribute selectors |
| Can I use: `:dir()` | https://caniuse.com/css-dir-pseudo | Current browser support table |
| MDN `<bdi>` element | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi | Isolating user-generated bidi content |
| Tailwind CSS RTL Support | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | `rtl:` / `ltr:` variant syntax |
| Tailwind Logical Properties | https://tailwindcss.com/docs/margin | `ms-*`, `me-*`, `ps-*`, `pe-*` utilities |
| MUI Right-to-left | https://mui.com/material-ui/customization/right-to-left/ | `@mui/stylis-plugin-rtl` setup for current MUI |
| Google Fonts Hebrew | https://fonts.google.com/?subset=hebrew | Available Hebrew font families |
| W3C Internationalization | https://www.w3.org/International/articles/inline-bidi-markup/ | Unicode bidi algorithm, markup best practices |

## Troubleshooting

### Error: "Text alignment looks wrong"
Cause: Using `text-align: left` instead of `text-align: start`
Solution: Replace all `left`/`right` in text-align with `start`/`end`.

### Error: "Layout not mirroring"
Cause: Using physical margin/padding instead of logical properties
Solution: Replace all `margin-left`/`margin-right` with `margin-inline-start`/`margin-inline-end`.