---
name: israeli-ui-design-system
description: Build RTL-first UI component libraries and design systems for Israeli applications with Hebrew typography. Use when user asks about Hebrew UI components, "itzuv" (design), Israeli design system, Hebrew font pairing, RTL component library, "tipografia ivrit" (Hebrew typography), or gov.il design patterns. Covers RTL-first component architecture, Hebrew font pairings (Heebo+Inter, Rubik+Source Sans 3), gov.il design system patterns, Israeli formatting conventions (shekel sign, day-first dates, 24-hour clock), and culturally appropriate UI for Israeli users. Do NOT use for general RTL CSS (use hebrew-rtl-best-practices) or accessibility audits (use israeli-accessibility-compliance instead).
license: MIT
---

# Israeli UI Design System

Works with React, Vue, Angular, and vanilla HTML/CSS. No network required for core patterns. Recommended with Storybook for component development.

## Instructions

### Step 1: Choose Hebrew Font Pairings

Select font combinations optimized for Hebrew readability and Latin compatibility:

| Pairing | Hebrew Font | Latin Font | Best For | Style |
|---------|-------------|------------|----------|-------|
| Modern Business | Heebo | Inter | SaaS, dashboards, admin panels | Clean, neutral |
| Friendly Startup | Rubik | Source Sans 3 | Consumer apps, marketing sites | Rounded, approachable |
| Government/Formal | Assistant | Roboto | Gov sites, institutional pages | Professional, clear |
| Editorial | Frank Ruhl Libre | Merriweather | Blogs, news, content sites | Serif, literary |
| Minimal | Secular One | Montserrat | Landing pages, portfolios | Bold headlines |

See `references/hebrew-typography.md` for complete font metrics and loading strategies.

**Font loading configuration:**
```css
/* Primary: Heebo + Inter pairing */
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&family=Inter:wght@300;400;500;700&display=swap');

:root {
  /* Latin face FIRST: Inter has no Hebrew glyphs, so Hebrew characters
     fall through to Heebo per glyph. Heebo ships Latin glyphs too, so
     listing it first would render English in Heebo and Inter never loads. */
  --font-sans: 'Inter', 'Heebo', 'Noto Sans Hebrew', Arial, sans-serif;
  --font-mono: 'Fira Code', 'Source Code Pro', monospace;
}

body {
  font-family: var(--font-sans);
}
```

A generic family (`sans-serif`) always matches, so nothing listed after it is ever used: keep it last, once, after a system font with Hebrew glyphs (Arial here) so text stays readable while the web fonts load. If you want Heebo's own Latin letters instead of a pairing, list Heebo alone. Monospace faces here have no Hebrew, so Hebrew inside code falls back to the system font.

**Next.js (`next/font`).** List the subsets to preload, including `hebrew`; `next/font` has no default subset, and leaving `subsets` out while `preload` is on only produces a warning:

```tsx
import { Heebo, Inter } from 'next/font/google';
const heebo = Heebo({ subsets: ['hebrew', 'latin'], variable: '--font-heebo', display: 'swap' });
const inter = Inter({ subsets: ['latin'], variable: '--font-inter', display: 'swap' });
// <html lang="he" dir="rtl" className={`${inter.variable} ${heebo.variable}`}>
```

With Tailwind v4, map them in CSS with `@theme inline { --font-sans: var(--font-inter), var(--font-heebo), sans-serif; }` (`inline` is required when a theme variable references another variable).

### Step 2: Hebrew Typography Scale

Hebrew letters are drawn between the Latin x-height and cap height, with no capitals or tall ascenders, so Hebrew reads **smaller** than Latin at the same font size. Size the scale for Hebrew, not for Latin (measured heights per font are in `references/hebrew-typography.md`):

```css
:root {
  /* Hebrew-adjusted type scale */
  --text-xs: 0.8125rem;   /* 13px -- minimum readable Hebrew */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px -- Hebrew body text minimum */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */

  /* Hebrew-specific line heights (taller than Latin) */
  --leading-tight: 1.4;
  --leading-normal: 1.7;
  --leading-relaxed: 1.9;

  /* NEVER use letter-spacing for Hebrew */
  --tracking-hebrew: normal;
  /* Slight word spacing improves Hebrew readability */
  --word-spacing-hebrew: 0.05em;
}

/* Hebrew body text: dir usually sits on <html>, so match either element */
html[dir="rtl"] body,
body[dir="rtl"] {
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  letter-spacing: var(--tracking-hebrew);
  word-spacing: var(--word-spacing-hebrew);
}
```

### Step 3: RTL-First Component Architecture

Design components with RTL as the default, not an afterthought:

```css
/* RTL-first button component */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding-inline: 1.5rem;
  padding-block: 0.75rem;
  border-radius: 0.375rem;
  font-family: var(--font-sans);
  font-weight: 500;
  text-align: start;
  /* Icon automatically flips in RTL */
}

.btn-icon-start {
  flex-direction: row;
  /* In RTL: icon appears on the right (start side) */
}

.btn-icon-end {
  flex-direction: row-reverse;
  /* In RTL: icon appears on the left (end side) */
}

/* RTL-first card component */
.card {
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: start;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-block-end: 1rem;
  padding-block-end: 1rem;
  border-block-end: 1px solid var(--border-color);
}

/* RTL-first sidebar layout */
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  /* In RTL: sidebar appears on the right automatically */
}

.layout-sidebar {
  border-inline-end: 1px solid var(--border-color);
  padding-inline-end: 1.5rem;
}
```

**RTL behavior for the rest of the component set.** Buttons, cards, and the sidebar are not the whole story - mirror every directional component:

| Component | RTL behavior |
|-----------|--------------|
| Breadcrumbs | Flow right-to-left; the separator (`/`, `>`, chevron) points left (toward the next crumb). A text separator (`>`, `›`) is a bidi-mirrored character that the browser already flips in RTL, so do not add `scaleX(-1)` to it (that flips it back). Only SVG or icon-font chevrons need `transform: scaleX(-1)`, and a transform has no effect on an inline element, so give an icon-font glyph `display: inline-block`. |
| Modals / dialogs | Centered modals need no change. Close (X) button sits at the inline-end (top-left in RTL). Footer action buttons: a common house convention puts the primary at the inline-start, so it lands on the right in RTL; pick one order and keep it. |
| Dropdowns / menus | Open aligned to the inline-start edge of the trigger; submenu flyouts expand toward the inline-start (to the left in RTL). Caret/chevron mirrors. |
| Sliders / range inputs | The track fills from the inline-start - in RTL the minimum is on the right, maximum on the left. Native `<input type="range">` with `dir="rtl"` handles this; custom sliders must flip the fill direction. |
| Progress bars | Fill grows from the inline-start, so progress advances right-to-left in RTL. Use `transform-origin` / logical properties, not a hardcoded `left: 0` origin. |
| Toasts / snackbars | Slide in from the inline-end edge of the viewport - top-left or bottom-left in RTL (mirrored from the LTR top-right convention). Anchor with `inset-inline-end`, not `right`. |

```css
/* Toast anchored to the inline-end edge -- flips sides automatically in RTL */
.toast {
  position: fixed;
  inset-block-start: 1rem;
  inset-inline-end: 1rem;
}

/* Progress bar fill grows from the inline-start */
.progress-fill {
  block-size: 100%;
  inline-size: var(--progress, 0%);
  /* fill starts at the inline-start edge: right in RTL, left in LTR */
}
```

**Tailwind v4.** Use the logical utilities so one class list works in both directions: `ps-*`/`pe-*` and `ms-*`/`me-*` (inline padding and margin), `border-s`/`border-e`, `rounded-s-*`/`rounded-e-*`, `text-start`/`text-end`, and, since v4.2.0, `inset-s-*`/`inset-e-*` plus the block-axis `pbs-*`/`pbe-*`/`mbs-*`/`mbe-*`. v4.2.0 deprecated `start-*`/`end-*` in favour of `inset-s-*`/`inset-e-*`. Keep the `rtl:`/`ltr:` variants for true exceptions, such as flipping a directional icon (`rtl:-scale-x-100`), not for spacing.

**shadcn/ui.** Setting `rtl: true` in `components.json` makes the CLI convert `left-*`/`right-*` to logical classes and flip supported icons with `rtl:rotate-180`, but only for projects created with `shadcn create` in the newer styles (`base-nova`, `radix-nova`); other projects follow its migration guide. Add its `DirectionProvider` (`shadcn add direction`). Its docs also say to pass `dir` to portal elements such as popover and tooltip content for now, as a workaround for a known tw-animate-css issue with logical slide utilities.

**Which icons mirror.** Mirror icons that show direction along the reading line; leave the rest:

| Mirror in RTL | Do not mirror |
|---------------|---------------|
| Back/forward arrows, chevrons in breadcrumbs and steppers, "next" and "send" | Media play, pause and seek controls (they follow tape direction) |
| Reply, list indent, text-align icons | Clocks, refresh and history icons (time runs clockwise everywhere) |
| Progress and slider fills, linear timelines | Checkmarks, search, camera and other non-directional objects |
| Icons of an object moving forward | Charts and graphs, numbers, logos, slashes |

Undo and redo imply both a horizontal and a circular direction: in RTL choose one and apply it consistently. Encode each choice once (for example a `data-mirror` attribute or an icon-registry flag) rather than per usage.

### Step 4: Israeli Color Palette and Design Tokens

```css
:root {
  /* Israeli-appropriate color tokens */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Status colors (universal) */
  --color-success: #16a34a;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: #2563eb;

  /* Neutral palette */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-500: #6b7280;
  --color-gray-700: #374151;
  --color-gray-900: #111827;

  /* Spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;
}
```

**Dark mode (`colors-dark` token tier).** Define a parallel dark token set rather than hardcoding dark values into components. Keep the same token names so components reference `var(--color-bg)` / `var(--color-text)` and never branch on theme. Direction is orthogonal to theme - RTL and dark mode are independent axes, so a `[data-theme="dark"][dir="rtl"]` combination must just work.

```css
:root {
  /* light (default) */
  --color-bg: #ffffff;
  --color-surface: #f9fafb;
  --color-text: #111827;
  --color-border: #e5e7eb;
}

:root[data-theme="dark"] {
  /* colors-dark tier -- same token names, dark values */
  --color-bg: #0b0f19;
  --color-surface: #151b2b;
  --color-text: #e5e7eb;
  --color-border: #2a3346;
}
```

Note: Hebrew text on dark backgrounds can look thinner because of Hebrew letterforms - verify contrast still meets WCAG AA and consider a slightly heavier font weight for dark-mode body text.

**Encode contrast into the tokens.** A design system's token layer should guarantee WCAG contrast, not leave it to component authors. Pair every text token against its surface and check the ratio: body text on `--color-bg` / `--color-surface` must be at least 4.5:1, and large text, icons, and UI borders at least 3:1. Audit the status tokens specifically: `--color-warning: #d97706` is 3.19:1 on white (3.05:1 on `--color-surface`) and `--color-primary-500: #3b82f6` is 3.68:1. That passes the 3:1 bar for large text, icons, and UI borders (so they are fine as a focus outline or a fill), but fails the 4.5:1 bar for normal-size body text. Do not put small text in these colors on a light background; introduce a darker step (a 600/700 shade) when you need the color as text.

**Prefer oklch for ramps.** Define color ramps in `oklch()` (Baseline since 2023) with hex fallbacks. Perceptually-uniform lightness makes accessible ramps and dark-mode variants far easier to generate than hand-tuned hex values.

**Tier the tokens.** Components should never reference a raw palette step such as `--color-primary-500`. Use three tiers: primitives (`blue.600`), semantic roles that point at them (`color.action.primary`), and component tokens that point at roles (`button.bg`). Rebranding or adding a dark theme then changes one layer.

**Author tokens once**, in the W3C Design Tokens Community Group (DTCG) format, whose Format Module 2025.10 is a Final Community Group Report (28 October 2025). Aliases use `{group.token}`, and a 2025.10 color value is an object:

```json
{
  "color": {
    "blue": { "600": { "$type": "color", "$value": { "colorSpace": "srgb", "components": [0.145, 0.388, 0.922], "hex": "#2563eb" } } },
    "action": { "primary": { "$type": "color", "$value": "{color.blue.600}" } }
  },
  "button": { "bg": { "$type": "color", "$value": "{color.action.primary}" } }
}
```

Style Dictionary has supported DTCG since v4, but its docs say 2025.10 is not fully supported yet (work in progress in v5), so check your version before adopting the object color syntax. Its `css/variables` format with `outputReferences: true` keeps the alias chain in the emitted CSS (`--button-bg: var(--color-action-primary)`), so the tiers survive into code.

**Line length.** Add a measure token and apply it with `max-inline-size`, e.g. `--measure-prose: 65ch`. The `ch` unit is the width of the Latin "0", so check the real Hebrew line length in the browser rather than trusting the number.

### Step 5: Gov.il Design Patterns

For government and institutional Israeli websites, the authoritative reference is the **Israeli Government Design System (IGDS)** - the formal atomic-design system used to unify the user experience across gov.il sites. It is published as a Figma Community file under CC BY 4.0. The current version is "Israeli Government DS 3.0" (https://www.figma.com/community/file/1637743894870099523/israeli-government-ds-3-0, support address at digital.gov.il); the earlier "IGDS Design System File 2.0" (https://www.figma.com/community/file/1426262348206342909/igds-design-system-file-2-0) is still listed, so check which one a project was built on. If you are building a real gov.il-adjacent product, pull tokens, components, and the RTL Hebrew illustration style directly from the IGDS Figma file rather than approximating them - IGDS defines its own color ramps, spacing, and component anatomy, and approximations will visibly diverge from live gov.il pages.

The CSS below is a **generic institutional pattern, NOT the official IGDS**. Use it as a starting scaffold for an institutional look when you do not have IGDS access; replace the values with IGDS tokens once you do.

```css
/* Generic institutional header pattern (NOT official IGDS tokens) */
.gov-header {
  background-color: #1a3a5c;
  color: #ffffff;
  padding-block: var(--space-4);
  padding-inline: var(--space-6);
}

.gov-header-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  /* Logo + Hebrew site name, right-aligned in RTL */
}

/* Gov.il form patterns */
.gov-form-group {
  margin-block-end: var(--space-6);
}

.gov-label {
  display: block;
  font-weight: 500;
  margin-block-end: var(--space-2);
  color: var(--color-gray-700);
}

.gov-input {
  inline-size: 100%;
  padding: var(--space-3);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: var(--text-base);
}

.gov-input:focus {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

/* Gov.il step indicator */
.gov-steps {
  display: flex;
  gap: var(--space-4);
  padding: 0;
  list-style: none;
  /* In RTL: steps flow right-to-left */
}

.gov-step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.gov-step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  inline-size: 2rem;
  block-size: 2rem;
  border-radius: var(--radius-full);
  background-color: var(--color-primary-500);
  color: #ffffff;
  font-weight: 700;
}
```

### Step 6: RTL-First Form Patterns

```html
<!-- Israeli address form -->
<form dir="rtl" lang="he">
  <fieldset>
    <legend>כתובת</legend>

    <div class="form-group">
      <label for="street">רחוב</label>
      <input id="street" type="text" dir="rtl">
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="house-num">מספר בית</label>
        <input id="house-num" type="text" dir="ltr"
               inputmode="numeric" size="6">
      </div>
      <div class="form-group">
        <label for="apartment">דירה</label>
        <input id="apartment" type="text" dir="ltr"
               inputmode="numeric" size="4">
      </div>
    </div>

    <div class="form-group">
      <label for="city">יישוב</label>
      <input id="city" type="text" dir="rtl">
    </div>

    <div class="form-group">
      <label for="postal">מיקוד</label>
      <input id="postal" type="text" dir="ltr"
             inputmode="numeric" pattern="[0-9]{7}"
             maxlength="7" size="10">
    </div>
  </fieldset>
</form>
```

**Israeli identity and contact fields.** Three input types that Latin-first design
systems get wrong:

```html
<!-- Teudat zehut: up to 9 digits, and a leading zero is significant.
     type="number" silently eats it and adds spinners. Always text + inputmode,
     and validate in script after trimming (isValidTz below), not with pattern. -->
<input id="tz" type="text" dir="ltr" inputmode="numeric"
       maxlength="9" autocomplete="off">

<!-- Israeli mobile: 05X + 7 digits, accepting the dashed and +972 forms users
     actually type. Keep it LTR inside the RTL form. Normalise on submit. -->
<input id="phone" type="tel" dir="ltr" inputmode="tel"
       autocomplete="tel">
<!-- Validate after stripping spaces and dashes (users paste "054 123 4567"):
     /^(0|\+?972-?0?)5\d{8}$/ on the normalised value, not a pattern attribute. -->

<!-- Email, URL and IBAN are Latin content: force LTR so the cursor and any
     punctuation behave, even though the surrounding form is RTL. -->
<input id="email" type="email" dir="ltr" autocomplete="email">
```

The ninth digit of a teudat zehut is a check digit, and shorter numbers are left-padded with zeros to nine digits. Pad first, then validate:

```js
function isValidTz(raw) {
  const digits = String(raw ?? '').trim();
  if (!/^\d{1,9}$/.test(digits) || /^0+$/.test(digits)) return false; // no empty, all-zero or non-digit input
  const id = digits.padStart(9, '0');
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    const n = Number(id[i]) * ((i % 2) + 1); // weights 1,2,1,2,...
    sum += n > 9 ? n - 9 : n;                // add the digits of a two-digit product
  }
  return sum % 10 === 0;
}
isValidTz('50012343'); // => true (padded to 050012343)
```

**Gendered microcopy (practice).** Hebrew verbs and adjectives carry gender, so a masculine-only imperative ("לחץ", "הירשם") addresses half your users wrongly. Common house styles use the plural imperative ("לחצו", "הירשמו") or an infinitive ("ללחוץ כאן"), or reword to a noun ("הרשמה"). Pick one style and put it in the content guidelines next to the tokens.

**Mixed-direction user content.** Anything a user typed, and anything from an API,
may be Hebrew or Latin. Do not hardcode a direction on it: `dir="auto"` lets the
first strong character decide, per element.

```html
<textarea dir="auto"></textarea>
<li dir="auto">{{ comment.body }}</li>
```

Set `dir="auto"` per item, never once on a list wrapper: a single wrapper takes
the direction of the first item and misaligns every other one.

### Step 7: Israeli Formatting Conventions (Currency, Numbers, Dates)

Design tokens and components must encode Israel-specific formatting, not mirror Latin/US defaults.

**Currency: shekel sign (₪)**

The shekel sign `₪` (U+20AA) is typically placed after the amount in Israeli financial contexts (e.g., `1,234.50 ₪`), though `₪ 1,234.50` is also common in retail. Whichever convention you pick, apply it consistently. Because numbers are inherently LTR, any amount inline inside Hebrew RTL text needs explicit bidi isolation or the surrounding punctuation may reorder.

```html
<!-- Correct: isolate the amount so the currency symbol stays put -->
<p>המחיר הוא <bdi>1,234.50 ₪</bdi> בלבד.</p>
```

```js
// Prefer Intl.NumberFormat over hand-formatting -- it handles symbol placement,
// grouping separators, and invisible RTL marks correctly across browsers.
new Intl.NumberFormat('he-IL', {
  style: 'currency',
  currency: 'ILS',
}).format(1234.5);
// => "‏1,234.50 ‏₪"  (renders as "1,234.50 ₪")
```

The returned string is NOT the clean `"1,234.50 ₪"` it looks like. It carries two
RTL marks (U+200F) and a non-breaking space, which is exactly what keeps the sign
from drifting in bidi text. Never assert string equality against a hand-typed
literal in a snapshot or unit test: compare `Intl` output to `Intl` output, or
strip `‏ ` first.

**Numbers in Hebrew body text**

Numbers (phone numbers, ID numbers, prices, dates) do not reverse under RTL. But when a long number sits inside Hebrew text, browsers may reflow surrounding punctuation. Use `<bdi>` or `dir="ltr"` on the number element to lock it.

```html
<p>מספר הזהות הוא <bdi>012345678</bdi>, בתוקף עד 2030.</p>
```

**Dates and time**

Israeli dates are day-first, never US `MM/DD/YYYY` and never ISO `YYYY-MM-DD` in
user-facing copy. Use 24-hour time (`14:30`); AM/PM is rare in Israeli UIs.

**The platform separator is a dot, not a slash.** CLDR gives Hebrew the short
pattern `d.M.y`, so `Intl` returns dots and no browser setting turns them into
slashes:

```js
new Intl.DateTimeFormat('he-IL', {
  day: '2-digit', month: '2-digit', year: 'numeric',
}).format(new Date(2026, 3, 20));
// => "20.04.2026"   (dateStyle: 'short' gives "20.4.2026")
```

Dots are the safe default: they are what a native user expects and what every
other Hebrew app shows. If a brand guideline demands `20/04/2026`, compose it
yourself instead of expecting `Intl` to produce it:

```js
const parts = Object.fromEntries(
  new Intl.DateTimeFormat('he-IL', { day: '2-digit', month: '2-digit', year: 'numeric' })
    .formatToParts(new Date(2026, 3, 20))
    .map((p) => [p.type, p.value]),
);
`${parts.day}/${parts.month}/${parts.year}`; // => "20/04/2026"
```

**Calendars.** For `he-IL`, `locale.getWeekInfo?.() ?? locale.weekInfo` (with `const locale = new Intl.Locale('he-IL')`; some runtimes, including Node 20 and 22, only have the older `weekInfo` accessor) returns `firstDay: 7` (Sunday) and `weekend: [5, 6]` (Friday and Saturday). Date pickers and calendar grids must start the week on Sunday and mark Friday and Saturday, not Saturday and Sunday. A native `<input type="date">` displays in the browser's own locale format, which can show `20/04/2026` beside your `20.04.2026` text; use a custom picker if the two must match.

Define design tokens so downstream components stay consistent:

```css
:root {
  --date-format-short: 'dd.MM.yyyy';
  --time-format: 'HH:mm';
  --currency-locale: 'he-IL';
  --currency-code: 'ILS';
}
```

**Number separators**

Thousands separator is comma (`1,234,567`), decimal is period (`1,234.50`). Do not switch to European `1.234,50` style; Israeli finance uses the US convention.

### Step 8: Test Both Directions

RTL regressions are visual, so test them visually. Render every component story in both `dir="rtl"` and `dir="ltr"` (and in each theme), for example with a Storybook global that sets `dir` on the preview root, and snapshot each combination in CI with Playwright's `toHaveScreenshot()`. Add a lint or grep check that fails on physical classes and properties (`ml-`, `mr-`, `pl-`, `pr-`, `left-`, `right-`, `margin-left`) so new code cannot reintroduce them.

## Examples

### Example 1: Set Up Israeli Design System
User says: "Create a design system for my Israeli SaaS product"
Result: Configure Heebo + Inter font pairing, set up Hebrew-adjusted type scale with 16px minimum body text and 1.7 line height, define RTL-first component primitives (button, card, input, sidebar layout) using CSS logical properties, and establish Israeli-appropriate color tokens.

### Example 2: Build Hebrew Form Component
User says: "I need a Hebrew address form with proper RTL layout"
Result: Create RTL form with Hebrew labels, right-aligned field groups, LTR input direction for numeric fields (house number, postal code, phone), proper fieldset grouping with Hebrew legends, and Israeli-specific field patterns (7-digit postal code, city selector).

### Example 3: Implement Gov.il Design Patterns
User says: "My government website needs to match gov.il design standards"
Result: Apply gov.il header pattern with institutional blue, Hebrew navigation with RTL flow, step indicators for multi-page forms, accessible form styling with focus indicators, and footer with required government links.

## Bundled Resources

### References
- `references/domain-checklist.md` -- Must-cover and should-cover items for an Israeli RTL design system, each with its source, plus explicit out-of-scope rows.
- `references/hebrew-typography.md` -- Hebrew font catalog with Google Fonts metrics, recommended pairings for different use cases (SaaS, editorial, government), font loading performance strategies, Hebrew-specific CSS properties (line-height, word-spacing, letter-spacing rules), and type scale recommendations for bilingual Hebrew/English interfaces.

## Gotchas
- Hebrew text is often shorter than its English equivalent, but by how much varies with the copy. Agents may design UI layouts with fixed widths based on English text length, causing Hebrew text to have too much whitespace or breaking the layout when switching to English.
- Heebo, Rubik and Assistant are web fonts, served from Google Fonts or self-hosted. Agents may load one with no system fallback before the generic family, so text is unstyled or jumps while it loads. Keep `display: swap` (or `font-display: swap`) and a system font with Hebrew glyphs, such as Arial, before `sans-serif`, as in Step 1.
- Form labels in Hebrew should be right-aligned and placed to the right of inputs (or above them). Agents often place labels to the left of inputs, which is the English convention and feels unnatural in RTL.
- Phone number input fields for Israeli numbers should accept formats with and without country code: 054-1234567, +972-54-1234567, and 0541234567. Agents may only validate the international format.
- The shekel sign (₪) is not a directional character, so an inline price like `1,234.50 ₪` inside a Hebrew paragraph can shift unpredictably between browsers. Agents usually trust the browser bidi algorithm and skip `<bdi>` or `Intl.NumberFormat('he-IL', { style: 'currency' })`, causing inconsistent price rendering between Chrome and Safari.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Google Fonts – Hebrew | https://fonts.google.com/?subset=hebrew | Heebo, Assistant, Rubik, Frank Ruhl Libre, loading snippets |
| CSS logical properties (MDN) | https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Logical_properties_and_values | padding-inline, margin-block, logical positioning |
| Tailwind RTL support | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | `rtl:` and `ltr:` variants for component libraries |
| shadcn/ui RTL | https://ui.shadcn.com/docs/rtl | `rtl: true` in components.json, supported styles, DirectionProvider |
| WCAG quick reference | https://www.w3.org/WAI/standards-guidelines/wcag/ | Contrast and reading-order requirements that apply to RTL |

## Troubleshooting

### Error: "Hebrew text looks cramped or too small"
Cause: Using Latin-optimized font sizes and line heights for Hebrew
Solution: Increase base font size to at least 16px for body text. Set line-height to 1.7 minimum for Hebrew. Never apply letter-spacing to Hebrew text. Add slight word-spacing (0.05em) for readability.

### Error: "Component layout breaks in RTL"
Cause: Using physical CSS properties (margin-left, padding-right) instead of logical properties
Solution: Replace all physical directional properties with logical equivalents: margin-inline-start, padding-inline-end, border-inline-start, inset-inline-start. Use flexbox and grid which automatically respect the dir attribute.

### Error: "Icons point in wrong direction in RTL"
Cause: Directional icons (arrows, chevrons, back buttons) not mirrored for RTL
Solution: Mirror directional SVG or icon-font icons (as `inline-block`) using CSS `transform: scaleX(-1)` within `[dir="rtl"]` context. Do not flip text chevrons such as `>` or `›`: the browser already mirrors them in RTL. Non-directional icons (search, home, settings) should NOT be mirrored. Create an icon mirroring utility class for consistent application.
