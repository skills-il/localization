---
name: hebrew-i18n
description: Implement comprehensive Hebrew internationalization (i18n) patterns for web and mobile applications. Use when user asks about Hebrew localization, "beinle'umiyut", i18n for Israeli apps, Hebrew plural forms, Hebrew date formatting, RTL CSS logical properties, bidirectional text handling, React/Vue/Angular/Next.js RTL integration, Tailwind CSS RTL, or next-intl setup. Covers Hebrew pluralization rules, date and number formatting for Israel, RTL-first CSS, Tailwind RTL utilities, and bidi text algorithms. Do NOT use for NLP or content writing (use hebrew-nlp-toolkit or hebrew-content-writer instead).
license: MIT
compatibility: Works with any JavaScript/TypeScript framework. No network required for core patterns. ICU and Intl API used for date/number formatting.
---

# Hebrew I18n

## Instructions

### Step 1: Set Up the I18n Framework

Direction belongs on the root `<html>` element, not on a wrapper `div`. In a single-page app that switches language at runtime, update it whenever the locale changes:

```js
function applyLocale(locale) {
  document.documentElement.lang = locale;
  document.documentElement.dir = locale === 'he' ? 'rtl' : 'ltr';
}
```

**React (react-intl):**
```jsx
import { useEffect } from 'react';
import { IntlProvider } from 'react-intl';
import heMessages from './locales/he.json';

function App() {
  useEffect(() => applyLocale('he'), []);
  return (
    <IntlProvider locale="he" messages={heMessages}>
      {/* App content */}
    </IntlProvider>
  );
}
```

**React (react-i18next):** i18next does not use ICU plural syntax by default. It selects a key suffix from `Intl.PluralRules`, so Hebrew needs `_one`, `_two` and `_other` keys:
```json
{
  "days_one": "יום אחד",
  "days_two": "יומיים",
  "days_other": "{{count}} ימים"
}
```
Call it as `t('days', { count })`. Since i18next v24 there is no fallback when `Intl.PluralRules` is missing, so only English-style `_one`/`_other` resolve and the `_two` form silently never appears. The i18next docs note that React Native's Hermes engine lacks `Intl.PluralRules`; check `typeof Intl.PluralRules` on your target and add a polyfill (such as `intl-pluralrules`) if it is undefined.

**Vue (vue-i18n):** vue-i18n plurals are pipe-separated, not ICU. vue-i18n 11.x (the current release line) chooses the case by position, not by `Intl.PluralRules`: three cases are read as `zero | one | other`, so without a rule `t('days', 1)` prints the second case. For Hebrew, register a rule that maps 1, 2 and every other count to the three cases, and call it as `t('days', count)`:
```js
import { createI18n } from 'vue-i18n';

// cases: one | two | other
const hePlural = (choice) => (choice === 1 ? 0 : choice === 2 ? 1 : 2);

const i18n = createI18n({
  legacy: false, // 11.x defaults to legacy mode, which ignores pluralRules
  locale: 'he',
  fallbackLocale: 'en',
  pluralRules: { he: hePlural }, // in legacy mode the option is pluralizationRules
  messages: { he: heMessages, en: enMessages }, // he: { days: 'יום אחד | יומיים | {count} ימים' }
});
// t('days', 2) -> "יומיים"
```
Automatic selection by `Intl.PluralRules` is a breaking change on the vue-i18n main branch and is not in the 11.x releases.

**Next.js App Router (next-intl):**
```ts
// src/i18n/routing.ts
import { defineRouting } from 'next-intl/routing';
export const routing = defineRouting({
  locales: ['he', 'en'],
  defaultLocale: 'he',
});
```

```ts
// src/proxy.ts (named middleware.ts before Next.js 16)
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';

export default createMiddleware(routing);

export const config = {
  matcher: '/((?!api|trpc|_next|_vercel|.*\\..*).*)'
};
```

```ts
// src/i18n/request.ts (supplies locale and messages to getTranslations / useTranslations)
import { hasLocale } from 'next-intl';
import { getRequestConfig } from 'next-intl/server';
import { routing } from './routing';
import { notFound } from 'next/navigation';
import * as rootParams from 'next/root-params';

export default getRequestConfig(async ({ locale }) => {
  if (!locale) {
    const paramValue = await rootParams.locale();
    if (hasLocale(routing.locales, paramValue)) {
      locale = paramValue;
    } else {
      notFound();
    }
  }
  return {
    locale,
    messages: (await import(`../../messages/${locale}.json`)).default
  };
});
```
`next/root-params` is available by default from Next.js 16.3. On earlier Next.js versions it must be enabled with `experimental.rootParams` in `next.config.ts`. Wire `request.ts` in with the `createNextIntlPlugin` wrapper from `next-intl/plugin` in `next.config.ts`.

```tsx
// src/app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getLocale } from 'next-intl/server';

export default async function LocaleLayout({ children }) {
  const locale = await getLocale();
  return (
    <html lang={locale} dir={locale === 'he' ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}
```
Rendered from a Server Component, `NextIntlClientProvider` inherits locale and messages from `request.ts`, so there is no need to call `getMessages()` and pass them in.

**Angular:**
```json
// angular.json -- add Hebrew locale
"i18n": {
  "sourceLocale": "en",
  "locales": {
    "he": "src/locale/messages.he.xlf"
  }
}
```
Also set `"localize": true` (or an array of locale IDs) in the build options, otherwise the CLI does not generate the Hebrew build.

### Step 2: Hebrew Plural Forms

Hebrew has three plural categories that i18n frameworks must handle:

| Category | Hebrew Term | Count | Example |
|----------|-------------|-------|---------|
| one (singular) | יחיד | 1, and decimals below 1 | פריט אחד (one item) |
| two (dual) | זוגי | 2 | שני פריטים (two items) -- uses special dual form |
| other (plural) | רבים | 0, 3+, decimals of 1.0 and above | 5 פריטים (5 items) |

Note: an older `many` category (for round numbers like 20 or 100) was removed from Unicode CLDR in version 42 (2022). Modern Hebrew plural rules use only `one`, `two`, and `other`, and round numbers resolve to `other`. Do not add a `many` branch; it would be dead code on any current ICU/CLDR runtime. Also note that `Intl.PluralRules('he').select(0.5)` returns `one`, so give fractions their own wording ("חצי שעה") rather than passing them to a count message.

See `references/pluralization.md` for complete rules and edge cases.

**ICU MessageFormat pattern (react-intl, next-intl):**
```
{count, plural,
  one {פריט אחד}
  two {שני פריטים}
  other {{count} פריטים}
}
```

**Common Hebrew plural patterns:**

| Singular (יחיד) | Dual (זוגי) | Plural (רבים) | Pattern |
|-----------------|-------------|---------------|---------|
| יום (day) | יומיים (2 days) | ימים (days) | Irregular dual |
| שעה (hour) | שעתיים (2 hours) | שעות (hours) | Feminine dual -תיים |
| חודש (month) | חודשיים (2 months) | חודשים (months) | Masculine dual -יים |
| שבוע (week) | שבועיים (2 weeks) | שבועות (weeks) | Masculine dual -יים |
| שנה (year) | שנתיים (2 years) | שנים (years) | Irregular dual |

### Step 3: Date and Time Formatting

**Israeli date format:** day before month, never MM/DD/YYYY. Note that `Intl.DateTimeFormat('he-IL')` renders the short date with dot separators (DD.MM.YYYY), e.g. `04.03.2026`; if you specifically need slashes, format the parts manually.

```javascript
// Using Intl.DateTimeFormat
const formatter = new Intl.DateTimeFormat('he-IL', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
// Output: "4 במרץ 2026"

// Short format
const shortFormatter = new Intl.DateTimeFormat('he-IL', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
});
// Output: "04.03.2026" (he-IL uses dot separators, DD.MM.YYYY, not slashes)

// Hebrew calendar, no library needed
new Intl.DateTimeFormat('he-IL-u-ca-hebrew', { dateStyle: 'long' }).format(new Date(2026, 2, 4));
// Output: "ט״ו באדר תשפ״ו"
```

**Hebrew day and month names:**

| Day | Hebrew | Abbreviation |
|-----|--------|-------------|
| Sunday | יום ראשון | א׳ |
| Monday | יום שני | ב׳ |
| Tuesday | יום שלישי | ג׳ |
| Wednesday | יום רביעי | ד׳ |
| Thursday | יום חמישי | ה׳ |
| Friday | יום שישי | ו׳ |
| Saturday | שבת | ש׳ |

Israeli business week: Sunday through Thursday (not Monday through Friday).

**Hebrew calendar dates:** for display, the `-u-ca-hebrew` locale extension above is enough. Use a library such as `hebcal` when you need holiday tables, parashat hashavua or date arithmetic in the Hebrew calendar.

### Step 4: Number and Currency Formatting

```javascript
// Israeli number format: 1,000.50 (comma for thousands, dot for decimal)
const numFormatter = new Intl.NumberFormat('he-IL');
numFormatter.format(1234567.89); // "1,234,567.89"

// Israeli Shekel currency
const currFormatter = new Intl.NumberFormat('he-IL', {
  style: 'currency',
  currency: 'ILS',
});
currFormatter.format(1234.50); // looks like "1,234.50 ₪"
```
The currency string is not plain ASCII: it contains invisible RIGHT-TO-LEFT MARK characters (U+200F) before the digits and before the ₪ sign, and a NO-BREAK SPACE (U+00A0) instead of a normal space. Snapshot tests, `===` comparisons, CSV exports and `parseFloat` on that string will fail. Strip the marks with `s.replace(/[\u200E\u200F]/g, '')` only for text comparisons. Never parse formatted output back into a number: even after stripping, `parseFloat('1,234.50 ₪')` returns `1` because it stops at the grouping comma. Keep the raw number, or read the pieces with `formatToParts()`.

**Israeli-specific number patterns:**

| Type | Format | Example |
|------|--------|---------|
| Phone (mobile) | 05X-XXXXXXX | 054-1234567 |
| Phone (landline) | 0X-XXXXXXX | 02-6234567 |
| Teudat Zehut (ID) | XXXXXXXXX | 123456782 (9 digits with check digit) |
| Postal code | XXXXXXX | 6100000 (7 digits) |
| Currency | X,XXX.XX ₪ | 1,234.50 ₪ (Intl output adds invisible direction marks) |

### Step 5: RTL CSS with Logical Properties

Always use CSS logical properties for i18n-ready layouts:

```css
/* Base RTL setup */
html[lang="he"] {
  direction: rtl;
}

/* Logical properties -- work in both LTR and RTL */
.card {
  margin-inline-start: 1rem;  /* right margin in RTL */
  padding-inline-end: 0.5rem; /* left padding in RTL */
  border-inline-start: 3px solid blue; /* right border in RTL */
  text-align: start;          /* right in RTL, left in LTR */
}

/* Flexbox automatically reverses in RTL */
.nav {
  display: flex;
  gap: 1rem;
  /* No direction override needed -- flex respects dir attribute */
}
```

**Tailwind CSS RTL (v3.3+, including v4):**

Tailwind provides logical property utilities and RTL variants:

```html
<!-- Logical property utilities (auto-flip for RTL) -->
<div class="ms-4 me-2 ps-3 pe-1 text-start">
  <!-- ms = margin-inline-start, me = margin-inline-end -->
  <!-- ps = padding-inline-start, pe = padding-inline-end -->
</div>

<!-- RTL/LTR variants for direction-specific overrides -->
<div class="ltr:ml-4 rtl:mr-4 ltr:text-left rtl:text-right">
  <!-- Explicit per-direction when logical properties are not enough -->
</div>
```

| Physical (avoid) | Logical (prefer) | RTL behavior |
|-------------------|-------------------|-------------|
| `ml-4` | `ms-4` | Right margin in RTL |
| `mr-4` | `me-4` | Left margin in RTL |
| `pl-4` | `ps-4` | Right padding in RTL |
| `pr-4` | `pe-4` | Left padding in RTL |
| `text-left` | `text-start` | Right-aligned in RTL |
| `text-right` | `text-end` | Left-aligned in RTL |
| `rounded-l-lg` | `rounded-s-lg` | Right corners in RTL |
| `border-r-2` | `border-e-2` | Left border in RTL |

### Step 6: Bidirectional Text and Form Inputs

See `references/bidi.md` for detailed patterns and edge cases.

```html
<!-- Isolate LTR content within Hebrew text -->
<p dir="rtl">
  הזמנה מספר <span dir="ltr">ORD-12345</span> אושרה
</p>

<!-- Use bdi element for user-generated content -->
<p dir="rtl">
  המשתמש <bdi>JohnDoe123</bdi> נרשם
</p>

<!-- Free-text fields: let the browser pick direction from what the user types -->
<textarea dir="auto" name="comment"></textarea>

<!-- Fields that are always LTR: keep the label RTL, force the input LTR -->
<label for="email">אימייל</label>
<input id="email" type="email" dir="ltr">
```
`dir="auto"` uses the first strongly directional character, so a Hebrew comment that starts with an English name gets a left-to-right base direction. Use it for unknown user input, and an explicit `dir` when the direction is known (email, phone, URL, card and ID fields are `dir="ltr"`).

**Common bidi scenarios in Israeli apps:**

| Content Type | Direction | Handling |
|-------------|-----------|----------|
| Hebrew text | RTL | Default, no special handling |
| English text in Hebrew | LTR | Wrap in `dir="ltr"` span |
| Phone numbers | LTR | Wrap in `dir="ltr"` or `<bdo>` |
| URLs and emails | LTR | Wrap in `dir="ltr"` span |
| Mixed Hebrew + code | Both | Use `unicode-bidi: isolate` |
| Currency amounts | LTR numbers + RTL symbol | Use Intl.NumberFormat |
| User-typed text | Unknown | `dir="auto"` on the field and on the element that displays it |

### Step 7: Framework-Specific RTL Integration

**Next.js App Router with Tailwind:** this snippet only illustrates the Tailwind utilities. Keep the `NextIntlClientProvider` and locale handling from the Step 1 layout, or client components that call `useTranslations` will fail.
```tsx
// app/[locale]/layout.tsx
export default async function LocaleLayout({ children, params }) {
  const { locale } = await params;
  return (
    <html lang={locale} dir={locale === 'he' ? 'rtl' : 'ltr'}>
      <body className="font-sans">
        {/* Tailwind logical utilities auto-flip based on dir attribute */}
        <main className="ms-4 me-4 text-start">{children}</main>
      </body>
    </html>
  );
}
```

```tsx
// components/NavBar.tsx -- uses rtl: variant for icon flipping
export function NavBar() {
  return (
    <nav className="flex items-center gap-4">
      <button className="ltr:rotate-0 rtl:rotate-180">
        <ChevronRight /> {/* Flips to point left in RTL */}
      </button>
    </nav>
  );
}
```

**Vue with Vuetify:**
```js
import { createVuetify } from 'vuetify';
const vuetify = createVuetify({
  locale: {
    locale: 'he',
    fallback: 'en',
    rtl: { he: true },
  },
});
```

**Angular Material:**
```typescript
import { BidiModule } from '@angular/cdk/bidi';

@NgModule({
  imports: [BidiModule],
})
export class AppModule {}

// In template:
// <div dir="rtl">...</div>
```

**React Native:** call `I18nManager.allowRTL(true)` and `I18nManager.forceRTL(true)` for Hebrew. The setting is persisted and only takes effect after the app reloads, so switch direction at startup or prompt a reload rather than expecting an instant flip.

## Examples

### Example 1: Add Hebrew to Existing React App
User says: "I need to add Hebrew language support to my React app"
Result: Set up react-intl (ICU plurals) or react-i18next (`_one`/`_two`/`_other` keys), create the he.json message file, set `lang` and `dir="rtl"` on `document.documentElement` when the locale changes, replace hardcoded strings with translation keys, give free-text inputs `dir="auto"`, and handle bidi text for mixed content.

### Example 2: Format Israeli Dates and Currency
User says: "How do I format dates and prices for Israeli users?"
Result: Use Intl.DateTimeFormat with he-IL locale for Israeli-format dates (day before month; the short form renders dot-separated, DD.MM.YYYY), `he-IL-u-ca-hebrew` for Hebrew calendar dates, Intl.NumberFormat with ILS currency for shekel formatting, and strip the invisible direction marks before comparing or exporting formatted strings.

### Example 3: Fix Bidirectional Text Issues
User says: "Phone numbers and English text look wrong in my Hebrew UI"
Result: Wrap phone numbers in `dir="ltr"` spans, isolate English content with `unicode-bidi: isolate`, use `bdi` element for user-generated content, and test with mixed Hebrew/English strings.

### Example 4: Hebrew Plural Forms
User says: "My Hebrew translations show wrong plural forms"
Result: Implement three categories (one/two/other) in the syntax your framework expects (ICU for react-intl/next-intl, pipes plus a plural rule for vue-i18n, key suffixes for i18next), handle dual forms for time units, and on React Native add an `Intl.PluralRules` polyfill.

### Example 5: Add Hebrew to Next.js App Router
User says: "I want to add Hebrew and English support to my Next.js App Router project"
Result: Install next-intl, create the `[locale]` route segment, add `i18n/routing.ts`, `i18n/request.ts` and `proxy.ts` (`middleware.ts` before Next.js 16), wrap `next.config.ts` with `createNextIntlPlugin`, set `dir="rtl"` on `<html>` for the Hebrew locale, create he.json and en.json with ICU plural syntax, and use Tailwind logical utilities (`ms-*`, `me-*`, `text-start`) for RTL-ready styles.

## Bundled Resources

### Scripts
- `scripts/generate_i18n.py`: Generate Hebrew i18n message files. Scaffolds translation JSON structure with Hebrew plural forms in each framework's own syntax (ICU for react-intl and next-intl, pipe-separated for vue-i18n, used with the Hebrew plural rule from Step 1). Run: `python scripts/generate_i18n.py --help`

### References
- `references/pluralization.md`: Complete Hebrew pluralization rules with singular, dual, and plural forms for common word categories (time, quantities, objects), the current CLDR rule text, ICU MessageFormat patterns, and edge cases for decimals and Hebrew number agreement.
- `references/bidi.md`: Bidirectional text handling patterns for Hebrew applications. Unicode bidi algorithm overview, HTML dir attribute usage, CSS unicode-bidi properties, framework-specific bidi solutions, and common pitfalls with mixed Hebrew/English/number content.

## Gotchas
- Agents may set `dir="rtl"` only on the body element or a wrapper div, but RTL direction must be set at the `<html>` level to properly affect scroll bars, default text alignment, and CSS logical properties. In SPAs, update `document.documentElement.dir` when the locale changes.
- Hebrew plural forms are complex: there are singular, dual (for some nouns), and plural forms. Agents may implement simple English-style singular/plural (1 vs. many) and miss the dual form (e.g., yomayim = 2 days).
- Agents write ICU plural strings for every framework. vue-i18n expects pipe-separated cases (and, on 11.x, a Hebrew plural rule) and i18next expects `_one`/`_two`/`_other` key suffixes; an ICU string in either renders literally or never pluralizes.
- i18n keys for Hebrew should not use the English text as the key (e.g., `t('Submit')`) because Hebrew translations can be much shorter or longer, breaking layouts. Use semantic keys (e.g., `t('form.submit')`).
- Agents often forget to reverse icon positions in RTL: arrows, chevrons, and progress indicators should mirror horizontally. A "next" arrow should point left in Hebrew UI, not right.
- Tailwind `space-x-*` behaves differently by version. In v3 it sets physical left/right margins and does not flip, so add `space-x-reverse` under RTL or use `gap-*`. In v4 it sets `margin-inline-start/end`, which already follows `dir`, so adding `space-x-reverse` for RTL double-reverses the spacing. Prefer `gap-*` with flex/grid in both.

## Troubleshooting

### Error: "Plural forms not matching Hebrew grammar"
Cause: i18n framework not configured for Hebrew three-category plural rules, or the message uses a syntax the framework does not parse
Solution: Hebrew uses one/two/other (not just one/other like English). In react-intl and next-intl use ICU MessageFormat with the `two` category; in vue-i18n use `one | two | other` pipes with the Hebrew `pluralRules` function; in i18next use `_one`/`_two`/`_other` keys. On React Native add an `Intl.PluralRules` polyfill.

### Error: "Date showing MM/DD/YYYY instead of DD/MM/YYYY"
Cause: Using en-US locale instead of he-IL for date formatting
Solution: Use `new Intl.DateTimeFormat('he-IL')` or configure your date library with the he-IL locale. Never assume American date format for Israeli users.

### Error: "Formatted price fails an equality test or parses to the wrong number"
Cause: `Intl.NumberFormat('he-IL', { style: 'currency', currency: 'ILS' })` inserts U+200F direction marks, a no-break space and grouping commas
Solution: Compare and store raw numbers. For text comparisons, strip the marks with `/[\u200E\u200F]/g` and normalize U+00A0 to a space. Do not `parseFloat` a formatted string; it stops at the first comma.

### Error: "Numbers appear reversed in RTL context"
Cause: RTL direction affecting digit display order
Solution: Numbers in Hebrew are always LTR. Use `dir="ltr"` on numeric content or rely on the Unicode bidi algorithm which handles digits correctly by default. The issue is usually with surrounding punctuation, not the digits themselves.
