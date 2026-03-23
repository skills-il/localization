---
name: hebrew-i18n
description: Implement comprehensive Hebrew internationalization (i18n) patterns for web and mobile applications. Use when user asks about Hebrew localization, "beinle'umiyut", i18n for Israeli apps, Hebrew plural forms, Hebrew date formatting, RTL CSS logical properties, bidirectional text handling, or React/Vue/Angular RTL integration. Covers Hebrew pluralization rules, date and number formatting for Israel, RTL-first CSS, and bidi text algorithms. Do NOT use for NLP or content writing (use hebrew-nlp-toolkit or hebrew-content-writer instead).
license: MIT
compatibility: Works with any JavaScript/TypeScript framework. No network required for core patterns. ICU and Intl API used for date/number formatting.
---

# Hebrew I18n

## Instructions

### Step 1: Set Up the I18n Framework

**React (react-intl / react-i18next):**
```jsx
import { IntlProvider } from 'react-intl';
import heMessages from './locales/he.json';

function App() {
  return (
    <IntlProvider locale="he" messages={heMessages}>
      <div dir="rtl" lang="he">
        {/* App content */}
      </div>
    </IntlProvider>
  );
}
```

**Vue (vue-i18n):**
```js
import { createI18n } from 'vue-i18n';
const i18n = createI18n({
  locale: 'he',
  fallbackLocale: 'en',
  messages: { he: heMessages, en: enMessages },
});
```

**Angular:**
```typescript
// angular.json -- add Hebrew locale
"i18n": {
  "sourceLocale": "en",
  "locales": {
    "he": "src/locale/messages.he.xlf"
  }
}
```

### Step 2: Hebrew Plural Forms

Hebrew has three plural categories that i18n frameworks must handle:

| Category | Hebrew Term | Count | Example |
|----------|-------------|-------|---------|
| one (singular) | יחיד | 1 | פריט אחד (one item) |
| two (dual) | זוגי | 2 | שני פריטים (two items) -- uses special dual form |
| other (plural) | רבים | 0, 3+ | 5 פריטים (5 items) |

See `references/pluralization.md` for complete rules and edge cases.

**ICU MessageFormat pattern:**
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

**Israeli date format:** DD/MM/YYYY (not MM/DD/YYYY)

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
// Output: "04/03/2026" (DD/MM/YYYY)
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

**Hebrew calendar dates:** Use libraries like `hebcal` for Hebrew calendar conversion. Format: day + Hebrew month name (e.g., "ה׳ באדר תשפ״ו").

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
currFormatter.format(1234.50); // "1,234.50 ₪"
```

**Israeli-specific number patterns:**

| Type | Format | Example |
|------|--------|---------|
| Phone (mobile) | 05X-XXXXXXX | 054-1234567 |
| Phone (landline) | 0X-XXXXXXX | 02-6234567 |
| Teudat Zehut (ID) | XXXXXXXXX | 123456782 (9 digits with check digit) |
| Postal code | XXXXXXX | 6100000 (7 digits) |
| Currency | X,XXX.XX ₪ | 1,234.50 ₪ |

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

### Step 6: Bidirectional Text Handling

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
```

**Common bidi scenarios in Israeli apps:**

| Content Type | Direction | Handling |
|-------------|-----------|----------|
| Hebrew text | RTL | Default, no special handling |
| English text in Hebrew | LTR | Wrap in `dir="ltr"` span |
| Phone numbers | LTR | Wrap in `dir="ltr"` or `<bdo>` |
| URLs and emails | LTR | Wrap in `dir="ltr"` span |
| Mixed Hebrew + code | Both | Use `unicode-bidi: isolate` |
| Currency amounts | LTR numbers + RTL symbol | Use Intl.NumberFormat |

### Step 7: Framework-Specific RTL Integration

**React with styled-components:**
```jsx
import { ThemeProvider } from 'styled-components';

const theme = {
  dir: 'rtl',
  isRTL: true,
};

const Container = styled.div`
  direction: ${({ theme }) => theme.dir};
  margin-inline-start: 1rem;
`;
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

## Examples

### Example 1: Add Hebrew to Existing React App
User says: "I need to add Hebrew language support to my React app"
Result: Set up react-i18next with Hebrew locale, create he.json message file, configure plural rules, add RTL wrapper with dir="rtl", replace hardcoded strings with translation keys, and handle bidi text for mixed content.

### Example 2: Format Israeli Dates and Currency
User says: "How do I format dates and prices for Israeli users?"
Result: Use Intl.DateTimeFormat with he-IL locale for DD/MM/YYYY dates, Intl.NumberFormat with ILS currency for shekel formatting, and ensure numbers display correctly in RTL context.

### Example 3: Fix Bidirectional Text Issues
User says: "Phone numbers and English text look wrong in my Hebrew UI"
Result: Wrap phone numbers in `dir="ltr"` spans, isolate English content with `unicode-bidi: isolate`, use `bdi` element for user-generated content, and test with mixed Hebrew/English strings.

### Example 4: Hebrew Plural Forms
User says: "My Hebrew translations show wrong plural forms"
Result: Implement ICU MessageFormat with three categories (one/two/other), handle dual forms for time units, and configure i18n framework plural rules for Hebrew locale.

## Bundled Resources

### Scripts
- `scripts/generate_i18n.py` — Generate Hebrew i18n message files: scaffold translation JSON/XLIFF structure, extract Hebrew plural form templates, produce locale files for react-intl, vue-i18n, and angular i18n. Run: `python scripts/generate_i18n.py --help`

### References
- `references/pluralization.md` — Complete Hebrew pluralization rules with singular, dual, and plural forms for common word categories (time, quantities, objects), ICU MessageFormat patterns, and edge cases for Hebrew number agreement.
- `references/bidi.md` — Bidirectional text handling patterns for Hebrew applications: Unicode bidi algorithm overview, HTML dir attribute usage, CSS unicode-bidi properties, framework-specific bidi solutions, and common pitfalls with mixed Hebrew/English/number content.

## Gotchas
- Agents may set `dir="rtl"` only on the body element, but RTL direction must be set at the `<html>` level to properly affect scroll bars, default text alignment, and CSS logical properties.
- Hebrew plural forms are complex: there are singular, dual (for some nouns), and plural forms. Agents may implement simple English-style singular/plural (1 vs. many) and miss the dual form (e.g., yomayim = 2 days).
- i18n keys for Hebrew should not use the English text as the key (e.g., `t('Submit')`) because Hebrew translations can be much shorter or longer, breaking layouts. Use semantic keys (e.g., `t('form.submit')`).
- Agents often forget to reverse icon positions in RTL: arrows, chevrons, and progress indicators should mirror horizontally. A "next" arrow should point left in Hebrew UI, not right.

## Troubleshooting

### Error: "Plural forms not matching Hebrew grammar"
Cause: i18n framework not configured for Hebrew three-category plural rules
Solution: Hebrew uses one/two/other (not just one/other like English). Ensure your framework is configured with CLDR Hebrew plural rules. In react-intl, use ICU MessageFormat with the `two` category.

### Error: "Date showing MM/DD/YYYY instead of DD/MM/YYYY"
Cause: Using en-US locale instead of he-IL for date formatting
Solution: Use `new Intl.DateTimeFormat('he-IL')` or configure your date library with the he-IL locale. Never assume American date format for Israeli users.

### Error: "Numbers appear reversed in RTL context"
Cause: RTL direction affecting digit display order
Solution: Numbers in Hebrew are always LTR. Use `dir="ltr"` on numeric content or rely on the Unicode bidi algorithm which handles digits correctly by default. The issue is usually with surrounding punctuation, not the digits themselves.