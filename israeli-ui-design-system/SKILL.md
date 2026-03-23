---
name: israeli-ui-design-system
description: Build RTL-first UI component libraries and design systems for Israeli applications with Hebrew typography. Use when user asks about Hebrew UI components, "itzuv" (design), Israeli design system, Hebrew font pairing, RTL component library, "tipografia ivrit" (Hebrew typography), or gov.il design patterns. Covers RTL-first component architecture, Hebrew font pairings (Heebo+Inter, Rubik+Source Sans Pro), gov.il design system patterns, and culturally appropriate UI for Israeli users. Do NOT use for general RTL CSS (use hebrew-rtl-best-practices) or accessibility audits (use israeli-accessibility-compliance instead).
license: MIT
compatibility: Works with React, Vue, Angular, and vanilla HTML/CSS. No network required for core patterns. Recommended with Storybook for component development.
---

# Israeli UI Design System

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

### Step 5: Gov.il Design Patterns

For government and institutional Israeli websites, follow the gov.il design system:

```css
/* Gov.il inspired header */
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
