---
name: israeli-ui-design-system
description: Build RTL-first UI component libraries and design systems for Israeli applications with Hebrew typography. Use when user asks about Hebrew UI components, "itzuv" (design), Israeli design system, Hebrew font pairing, RTL component library, "tipografia ivrit" (Hebrew typography), or gov.il design patterns. Covers RTL-first component architecture, Hebrew font pairings (Heebo+Inter, Rubik+Source Sans Pro), gov.il design system patterns, Israeli formatting conventions (shekel sign, DD/MM/YYYY dates, 24-hour clock), and culturally appropriate UI for Israeli users. Do NOT use for general RTL CSS (use hebrew-rtl-best-practices) or accessibility audits (use israeli-accessibility-compliance instead).
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
| Friendly Startup | Rubik | Source Sans Pro | Consumer apps, marketing sites | Rounded, approachable |
| Government/Formal | Assistant | Roboto | Gov sites, institutional pages | Professional, clear |
| Editorial | Frank Ruhl Libre | Merriweather | Blogs, news, content sites | Serif, literary |
| Minimal | Secular One | Montserrat | Landing pages, portfolios | Bold headlines |

See `references/hebrew-typography.md` for complete font metrics and loading strategies.

**Font loading configuration:**
```css
/* Primary: Heebo + Inter pairing */
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&family=Inter:wght@300;400;500;700&display=swap');

:root {
  --font-hebrew: 'Heebo', 'Assistant', 'Noto Sans Hebrew', sans-serif;
  --font-latin: 'Inter', 'Roboto', sans-serif;
  --font-mono: 'Fira Code', 'Source Code Pro', monospace;
}

body {
  font-family: var(--font-hebrew), var(--font-latin);
}
```

### Step 2: Hebrew Typography Scale

Hebrew characters are visually larger than Latin at the same font size. Adjust the type scale:

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

/* Hebrew body text */
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
  font-family: var(--font-hebrew), var(--font-latin);
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
| Breadcrumbs | Flow right-to-left; the separator (`/`, `>`, chevron) points left (toward the next crumb). Use a logical separator or mirror a chevron with `transform: scaleX(-1)`. |
| Modals / dialogs | Centered modals need no change. Close (X) button sits at the inline-end (top-left in RTL). Footer action buttons: primary at the inline-start, so the primary lands on the right in RTL. |
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

### Step 5: Gov.il Design Patterns

For government and institutional Israeli websites, the authoritative reference is the **Israeli Government Design System (IGDS)** - the formal atomic-design system used to unify the user experience across gov.il sites. It is published as a Figma Community file ("IGDS Design System File 2.0", https://www.figma.com/community/file/1426262348206342909/igds-design-system-file-2-0), with companion illustration libraries. If you are building a real gov.il-adjacent product, pull tokens, components, and the RTL Hebrew illustration style directly from the IGDS Figma file rather than approximating them - IGDS defines its own color ramps, spacing, and component anatomy, and approximations will visibly diverge from live gov.il pages.

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
  font-family: var(--font-hebrew), var(--font-latin);
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
// => "1,234.50 ₪"
```

**Numbers in Hebrew body text**

Numbers (phone numbers, ID numbers, prices, dates) do not reverse under RTL. But when a long number sits inside Hebrew text, browsers may reflow surrounding punctuation. Use `<bdi>` or `dir="ltr"` on the number element to lock it.

```html
<p>מספר הזהות הוא <bdi>012345678</bdi>, בתוקף עד 2030.</p>
```

**Dates and time**

Default to the Israeli convention: `DD/MM/YYYY` (e.g., `20/04/2026`), not US `MM/DD/YYYY` or ISO `YYYY-MM-DD` in user-facing copy. Use 24-hour time (`14:30`); AM/PM is rare in Israeli UIs.

```js
new Intl.DateTimeFormat('he-IL', {
  day: '2-digit', month: '2-digit', year: 'numeric',
}).format(new Date());
// => "20.4.2026" or "20/04/2026" depending on browser locale data
```

Define design tokens so downstream components stay consistent:

```css
:root {
  --date-format-short: 'dd/MM/yyyy';
  --time-format: 'HH:mm';
  --currency-locale: 'he-IL';
  --currency-code: 'ILS';
}
```

**Number separators**

Thousands separator is comma (`1,234,567`), decimal is period (`1,234.50`). Do not switch to European `1.234,50` style; Israeli finance uses the US convention.

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
- `references/hebrew-typography.md` -- Hebrew font catalog with Google Fonts metrics, recommended pairings for different use cases (SaaS, editorial, government), font loading performance strategies, Hebrew-specific CSS properties (line-height, word-spacing, letter-spacing rules), and type scale recommendations for bilingual Hebrew/English interfaces.

## Gotchas
- Hebrew text is typically 15-30% shorter than its English equivalent. Agents may design UI layouts with fixed widths based on English text length, causing Hebrew text to have too much whitespace or breaking the layout when switching to English.
- The standard Hebrew web font stack should prioritize system fonts: "Segoe UI", "Rubik", "Heebo", Arial, sans-serif. Agents may use Google Fonts Hebrew fonts without including a fallback, causing FOUT on slow connections.
- Form labels in Hebrew should be right-aligned and placed to the right of inputs (or above them). Agents often place labels to the left of inputs, which is the English convention and feels unnatural in RTL.
- Phone number input fields for Israeli numbers should accept formats with and without country code: 054-1234567, +972-54-1234567, and 0541234567. Agents may only validate the international format.
- The shekel sign (₪) is not a directional character, so an inline price like `1,234.50 ₪` inside a Hebrew paragraph can shift unpredictably between browsers. Agents usually trust the browser bidi algorithm and skip `<bdi>` or `Intl.NumberFormat('he-IL', { style: 'currency' })`, causing inconsistent price rendering between Chrome and Safari.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Google Fonts – Hebrew | https://fonts.google.com/?subset=hebrew | Heebo, Assistant, Rubik, Frank Ruhl Libre, loading snippets |
| CSS logical properties (MDN) | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | padding-inline, margin-block, logical positioning |
| Tailwind RTL support | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | `rtl:` and `ltr:` variants for component libraries |
| shadcn/ui | https://ui.shadcn.com | RTL-friendly component recipes and primitives |
| WCAG 2.1 quick reference | https://www.w3.org/WAI/WCAG21/quickref/ | Contrast and reading-order requirements that apply to RTL |

## Troubleshooting

### Error: "Hebrew text looks cramped or too small"
Cause: Using Latin-optimized font sizes and line heights for Hebrew
Solution: Increase base font size to at least 16px for body text. Set line-height to 1.7 minimum for Hebrew. Never apply letter-spacing to Hebrew text. Add slight word-spacing (0.05em) for readability.

### Error: "Component layout breaks in RTL"
Cause: Using physical CSS properties (margin-left, padding-right) instead of logical properties
Solution: Replace all physical directional properties with logical equivalents: margin-inline-start, padding-inline-end, border-inline-start, inset-inline-start. Use flexbox and grid which automatically respect the dir attribute.

### Error: "Icons point in wrong direction in RTL"
Cause: Directional icons (arrows, chevrons, back buttons) not mirrored for RTL
Solution: Mirror directional icons using CSS `transform: scaleX(-1)` within `[dir="rtl"]` context. Non-directional icons (search, home, settings) should NOT be mirrored. Create an icon mirroring utility class for consistent application.
