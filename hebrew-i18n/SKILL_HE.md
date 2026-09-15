# בינלאומיות עברית

## הנחיות

### שלב 1: הגדרת מסגרת i18n

הכיוון שייך לאלמנט השורש `<html>`, לא ל-`div` עוטף. באפליקציית עמוד יחיד שמחליפה שפה בזמן ריצה, עדכנו אותו בכל פעם שהלוקאל משתנה:

```js
function applyLocale(locale) {
  document.documentElement.lang = locale;
  document.documentElement.dir = locale === 'he' ? 'rtl' : 'ltr';
}
```

**ספריית react-intl ב-React:**
```jsx
import { useEffect } from 'react';
import { IntlProvider } from 'react-intl';
import heMessages from './locales/he.json';

function App() {
  useEffect(() => applyLocale('he'), []);
  return (
    <IntlProvider locale="he" messages={heMessages}>
      {/* תוכן האפליקציה */}
    </IntlProvider>
  );
}
```

**ספריית react-i18next ב-React:** כברירת מחדל i18next לא משתמשת בתחביר ריבוי של ICU. היא בוחרת סיומת מפתח לפי `Intl.PluralRules`, ולכן עברית צריכה מפתחות `_one`, `_two` ו-`_other`:
```json
{
  "days_one": "יום אחד",
  "days_two": "יומיים",
  "days_other": "{{count}} ימים"
}
```
קוראים לזה עם `t('days', { count })`. מגרסה 24 של i18next אין מנגנון גיבוי כש-`Intl.PluralRules` חסר, כך שרק הצורות בסגנון אנגלי `_one`/`_other` עובדות וצורת `_two` פשוט לא מופיעה אף פעם. התיעוד של i18next מציין שמנוע Hermes של React Native חסר את `Intl.PluralRules`; בדקו את `typeof Intl.PluralRules` בסביבת היעד והוסיפו polyfill (למשל `intl-pluralrules`) אם הוא undefined.

**ספריית vue-i18n ב-Vue:** ב-vue-i18n צורות הריבוי מופרדות בקו אנכי, לא ב-ICU. בגרסאות 11.x (קו הגרסאות הנוכחי) הספרייה בוחרת את הצורה לפי מיקום ולא לפי `Intl.PluralRules`: שלוש צורות נקראות כ-`zero | one | other`, כך שבלי כלל `t('days', 1)` מציג את הצורה השנייה. לעברית, רשמו כלל שממפה 1, 2 וכל ספירה אחרת לשלוש הצורות, וקראו לזה עם `t('days', count)`:
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
בחירה אוטומטית לפי `Intl.PluralRules` היא שינוי שובר בענף הראשי של vue-i18n ולא קיימת בגרסאות 11.x.

**ספריית next-intl ב-Next.js App Router:**
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
המודול `next/root-params` זמין כברירת מחדל מ-Next.js 16.3. בגרסאות Next.js קודמות צריך להפעיל אותו עם `experimental.rootParams` בקובץ `next.config.ts`. מחברים את `request.ts` עם העטיפה `createNextIntlPlugin` מתוך `next-intl/plugin` בקובץ `next.config.ts`.

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
כשהוא מרונדר מתוך Server Component, הרכיב `NextIntlClientProvider` יורש את הלוקאל וההודעות מ-`request.ts`, כך שאין צורך לקרוא ל-`getMessages()` ולהעביר אותן.

**פריימוורק Angular:**
```json
// angular.json -- מוסיפים לוקאל עברי
"i18n": {
  "sourceLocale": "en",
  "locales": {
    "he": "src/locale/messages.he.xlf"
  }
}
```
צריך גם להגדיר `"localize": true` (או מערך של מזהי לוקאלים) באפשרויות ה-build, אחרת ה-CLI לא מייצר את גרסת העברית.

### שלב 2: צורות ריבוי בעברית

לעברית יש שלוש קטגוריות ריבוי שכל מסגרת i18n חייבת לטפל בהן:

| קטגוריה | מונח עברי | ספירה | דוגמה |
|----------|-----------|-------|---------|
| יחיד (one) | יחיד | 1, ושברים מתחת ל-1 | פריט אחד |
| זוגי (two) | זוגי | 2 | שני פריטים - צורת זוגי מיוחדת |
| רבים (other) | רבים | 0, 3+, שברים מ-1.0 ומעלה | 5 פריטים |

שימו לב: קטגוריית `many` ישנה (למספרים עגולים כמו 20 או 100) הוסרה מ-Unicode CLDR בגרסה 42 (2022). כללי הריבוי המודרניים בעברית משתמשים רק ב-`one`, `two` ו-`other`, ומספרים עגולים נופלים תחת `other`. אל תוסיפו ענף `many`; הוא יהיה קוד מת בכל סביבת ICU/CLDR עדכנית. שימו לב גם ש-`Intl.PluralRules('he').select(0.5)` מחזיר `one`, אז כתבו לשברים הודעה נפרדת ("חצי שעה") במקום להעביר אותם להודעת ספירה.

תסתכלו על `references/pluralization.md` לכללים מלאים ומקרי קצה.

**תבנית ICU MessageFormat (ל-react-intl ול-next-intl):**
```
{count, plural,
  one {פריט אחד}
  two {שני פריטים}
  other {{count} פריטים}
}
```

**תבניות ריבוי נפוצות בעברית:**

| יחיד | זוגי | רבים | תבנית |
|------|------|------|--------|
| יום | יומיים | ימים | זוגי לא סדיר |
| שעה | שעתיים | שעות | זוגי נקבה -תיים |
| חודש | חודשיים | חודשים | זוגי זכר -יים |
| שבוע | שבועיים | שבועות | זוגי זכר -יים |
| שנה | שנתיים | שנים | זוגי לא סדיר |

### שלב 3: פורמט תאריך ושעה

**פורמט התאריך הישראלי:** יום לפני חודש, אף פעם לא MM/DD/YYYY. שימו לב ש-`Intl.DateTimeFormat('he-IL')` מציג את התאריך הקצר עם מפרידי נקודה (DD.MM.YYYY), למשל `04.03.2026`; אם צריך לוכסנים, עצבו את החלקים ידנית.

```javascript
// שימוש ב-Intl.DateTimeFormat
const formatter = new Intl.DateTimeFormat('he-IL', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
// פלט: "4 במרץ 2026"

// פורמט קצר
const shortFormatter = new Intl.DateTimeFormat('he-IL', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
});
// פלט: "04.03.2026" (he-IL משתמש במפרידי נקודה, DD.MM.YYYY, לא לוכסנים)

// לוח עברי, בלי ספרייה
new Intl.DateTimeFormat('he-IL-u-ca-hebrew', { dateStyle: 'long' }).format(new Date(2026, 2, 4));
// פלט: "ט״ו באדר תשפ״ו"
```

**שמות ימים וחודשים בעברית:**

| יום | עברית | קיצור |
|-----|--------|-------|
| ראשון | יום ראשון | א׳ |
| שני | יום שני | ב׳ |
| שלישי | יום שלישי | ג׳ |
| רביעי | יום רביעי | ד׳ |
| חמישי | יום חמישי | ה׳ |
| שישי | יום שישי | ו׳ |
| שבת | שבת | ש׳ |

שבוע העבודה הישראלי: ראשון עד חמישי (לא שני עד שישי).

**תאריכים בלוח העברי:** לתצוגה, תוספת הלוקאל `-u-ca-hebrew` שלמעלה מספיקה. תשתמשו בספרייה כמו `hebcal` כשצריך טבלאות חגים, פרשת השבוע או חישובי תאריכים בלוח העברי.

### שלב 4: פורמט מספרים ומטבע

```javascript
// פורמט מספרים ישראלי: 1,000.50 (פסיק לאלפים, נקודה לעשרוני)
const numFormatter = new Intl.NumberFormat('he-IL');
numFormatter.format(1234567.89); // "1,234,567.89"

// מטבע שקל
const currFormatter = new Intl.NumberFormat('he-IL', {
  style: 'currency',
  currency: 'ILS',
});
currFormatter.format(1234.50); // נראה כמו "1,234.50 ₪"
```
מחרוזת המטבע היא לא ASCII פשוט: יש בה תווי RIGHT-TO-LEFT MARK בלתי נראים (U+200F) לפני הספרות ולפני סימן ה-₪, ורווח קשיח (U+00A0) במקום רווח רגיל. בדיקות snapshot, השוואות `===`, ייצוא ל-CSV ו-`parseFloat` על המחרוזת הזאת ייכשלו. הסירו את הסימנים עם `s.replace(/[\u200E\u200F]/g, '')` רק לצורך השוואת טקסט. אל תמירו פלט מעוצב בחזרה למספר: גם אחרי ההסרה, `parseFloat('1,234.50 ₪')` מחזיר `1` כי הוא נעצר בפסיק של האלפים. שמרו את המספר הגולמי, או קראו את החלקים עם `formatToParts()`.

**תבניות מספרים ישראליות:**

| סוג | פורמט | דוגמה |
|------|--------|---------|
| טלפון (נייד) | 05X-XXXXXXX | 054-1234567 |
| טלפון (קווי) | 0X-XXXXXXX | 02-6234567 |
| תעודת זהות | XXXXXXXXX | 123456782 (9 ספרות עם ספרת ביקורת) |
| מיקוד | XXXXXXX | 6100000 (7 ספרות) |
| מטבע | X,XXX.XX ₪ | 1,234.50 ₪ (הפלט של Intl מוסיף סימני כיוון בלתי נראים) |

### שלב 5: CSS עם תכונות לוגיות ל-RTL

תמיד תשתמשו בתכונות CSS לוגיות לפריסות שמוכנות ל-i18n:

```css
/* הגדרת RTL בסיסית */
html[lang="he"] {
  direction: rtl;
}

/* תכונות לוגיות - עובדות גם ב-LTR וגם ב-RTL */
.card {
  margin-inline-start: 1rem;  /* שוליים ימניים ב-RTL */
  padding-inline-end: 0.5rem; /* ריפוד שמאלי ב-RTL */
  border-inline-start: 3px solid blue; /* גבול ימני ב-RTL */
  text-align: start;          /* ימין ב-RTL, שמאל ב-LTR */
}

/* Flexbox מתהפך אוטומטית ב-RTL */
.nav {
  display: flex;
  gap: 1rem;
  /* אין צורך לשנות כיוון - flex מכבד את תכונת dir */
}
```

**תמיכת RTL ב-Tailwind CSS (גרסה 3.3 ומעלה, כולל v4):**

ל-Tailwind יש כלי עזר לתכונות לוגיות ו-variants ל-RTL:

```html
<!-- כלי עזר לתכונות לוגיות (מתהפכים אוטומטית ב-RTL) -->
<div class="ms-4 me-2 ps-3 pe-1 text-start">
  <!-- ms = margin-inline-start, me = margin-inline-end -->
  <!-- ps = padding-inline-start, pe = padding-inline-end -->
</div>

<!-- RTL/LTR variants לשליטה ספציפית לכיוון -->
<div class="ltr:ml-4 rtl:mr-4 ltr:text-left rtl:text-right">
  <!-- שליטה מפורשת לכל כיוון כשתכונות לוגיות לא מספיקות -->
</div>
```

| פיזי (תימנעו) | לוגי (מומלץ) | איך זה מתנהג ב-RTL |
|----------------|--------------|---------------|
| `ml-4` | `ms-4` | שוליים ימניים ב-RTL |
| `mr-4` | `me-4` | שוליים שמאליים ב-RTL |
| `pl-4` | `ps-4` | ריפוד ימני ב-RTL |
| `pr-4` | `pe-4` | ריפוד שמאלי ב-RTL |
| `text-left` | `text-start` | יישור לימין ב-RTL |
| `text-right` | `text-end` | יישור לשמאל ב-RTL |
| `rounded-l-lg` | `rounded-s-lg` | עיגול פינות ימניות ב-RTL |
| `border-r-2` | `border-e-2` | גבול שמאלי ב-RTL |

### שלב 6: טקסט דו-כיווני ושדות קלט

תסתכלו על `references/bidi.md` לתבניות מפורטות ומקרי קצה.

```html
<!-- בידוד תוכן LTR בתוך טקסט עברי -->
<p dir="rtl">
  הזמנה מספר <span dir="ltr">ORD-12345</span> אושרה
</p>

<!-- שימוש באלמנט bdi לתוכן שנוצר ע"י משתמשים -->
<p dir="rtl">
  המשתמש <bdi>JohnDoe123</bdi> נרשם
</p>

<!-- שדות טקסט חופשי: הדפדפן בוחר כיוון לפי מה שהמשתמש מקליד -->
<textarea dir="auto" name="comment"></textarea>

<!-- שדות שתמיד LTR: התווית נשארת RTL, השדה עצמו LTR -->
<label for="email">אימייל</label>
<input id="email" type="email" dir="ltr">
```
הערך `dir="auto"` נקבע לפי התו הראשון בעל כיוון חזק, כך שתגובה בעברית שמתחילה בשם באנגלית תקבל כיוון בסיס משמאל לימין. השתמשו בו לקלט משתמש שהכיוון שלו לא ידוע, וב-`dir` מפורש כשהכיוון ידוע (שדות אימייל, טלפון, URL, כרטיס אשראי ותעודת זהות הם `dir="ltr"`).

**תרחישי bidi נפוצים באפליקציות ישראליות:**

| סוג תוכן | כיוון | הטיפול |
|-----------|-------|--------|
| טקסט עברי | RTL | ברירת מחדל, בלי טיפול מיוחד |
| טקסט אנגלי בתוך עברי | LTR | עוטפים ב-`dir="ltr"` span |
| מספרי טלפון | LTR | עוטפים ב-`dir="ltr"` או `bdo` |
| כתובות URL ואימייל | LTR | עוטפים ב-`dir="ltr"` span |
| עברית מעורבת + קוד | שניהם | משתמשים ב-`unicode-bidi: isolate` |
| סכומי מטבע | מספרים LTR + סמל RTL | משתמשים ב-Intl.NumberFormat |
| טקסט שהמשתמש מקליד | לא ידוע | `dir="auto"` על השדה ועל האלמנט שמציג אותו |

### שלב 7: אינטגרציית RTL לפי פריימוורק

**שילוב Next.js App Router עם Tailwind:** הקטע הזה רק מדגים את כלי ה-Tailwind. השאירו את `NextIntlClientProvider` ואת הטיפול בלוקאל מה-layout של שלב 1, אחרת רכיבי client שקוראים ל-`useTranslations` ייכשלו.
```tsx
// app/[locale]/layout.tsx
export default async function LocaleLayout({ children, params }) {
  const { locale } = await params;
  return (
    <html lang={locale} dir={locale === 'he' ? 'rtl' : 'ltr'}>
      <body className="font-sans">
        {/* כלי Tailwind לוגיים מתהפכים אוטומטית לפי תכונת dir */}
        <main className="ms-4 me-4 text-start">{children}</main>
      </body>
    </html>
  );
}
```

```tsx
// components/NavBar.tsx - שימוש ב-rtl: variant להיפוך אייקונים
export function NavBar() {
  return (
    <nav className="flex items-center gap-4">
      <button className="ltr:rotate-0 rtl:rotate-180">
        <ChevronRight /> {/* מתהפך להצביע שמאלה ב-RTL */}
      </button>
    </nav>
  );
}
```

**שילוב Vue עם Vuetify:**
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

**ספריית Angular Material:**
```typescript
import { BidiModule } from '@angular/cdk/bidi';

@NgModule({
  imports: [BidiModule],
})
export class AppModule {}

// בתבנית:
// <div dir="rtl">...</div>
```

**פריימוורק React Native:** קוראים ל-`I18nManager.allowRTL(true)` ול-`I18nManager.forceRTL(true)` לעברית. ההגדרה נשמרת ונכנסת לתוקף רק אחרי טעינה מחדש של האפליקציה, אז כדאי לקבוע כיוון בעלייה או לבקש טעינה מחדש, ולא לצפות להיפוך מיידי.

## דוגמאות

### דוגמה 1: הוספת עברית לאפליקציית React קיימת
המשתמש אומר: "אני צריך להוסיף תמיכה בעברית לאפליקציית ה-React שלי"
תוצאה: מגדירים react-intl (ריבוי ICU) או react-i18next (מפתחות `_one`/`_two`/`_other`), יוצרים קובץ הודעות he.json, קובעים `lang` ו-`dir="rtl"` על `document.documentElement` כשהלוקאל משתנה, מחליפים מחרוזות קשיחות במפתחות תרגום, נותנים לשדות טקסט חופשי `dir="auto"`, ומטפלים בטקסט bidi לתוכן מעורב.

### דוגמה 2: פורמט תאריכים ומחירים ישראליים
המשתמש אומר: "איך אני מפרמט תאריכים ומחירים למשתמשים ישראלים?"
תוצאה: משתמשים ב-Intl.DateTimeFormat עם לוקאל he-IL לתאריכים בפורמט ישראלי (יום לפני חודש; הפורמט הקצר מופרד בנקודות, DD.MM.YYYY), ב-`he-IL-u-ca-hebrew` לתאריכים בלוח העברי, ב-Intl.NumberFormat עם מטבע ILS לפורמט של שקלים, ומסירים את סימני הכיוון הבלתי נראים לפני השוואה או ייצוא של מחרוזות מעוצבות.

### דוגמה 3: תיקון בעיות טקסט דו-כיווני
המשתמש אומר: "מספרי טלפון וטקסט באנגלית נראים שבורים בממשק העברי שלי"
תוצאה: עוטפים מספרי טלפון ב-spans עם `dir="ltr"`, מבודדים תוכן אנגלי עם `unicode-bidi: isolate`, משתמשים באלמנט `bdi` לתוכן מהמשתמש, ובודקים עם מחרוזות מעורבות עברית/אנגלית.

### דוגמה 4: צורות ריבוי בעברית
המשתמש אומר: "התרגומים בעברית מציגים צורות ריבוי שגויות"
תוצאה: ממשים שלוש קטגוריות (one/two/other) בתחביר שהמסגרת מצפה לו (ICU ל-react-intl ול-next-intl, קווים אנכיים עם כלל ריבוי ל-vue-i18n, סיומות מפתח ל-i18next), מטפלים בצורות זוגי ליחידות זמן, וב-React Native מוסיפים polyfill ל-`Intl.PluralRules`.

### דוגמה 5: הוספת עברית לפרויקט Next.js App Router
המשתמש אומר: "אני רוצה להוסיף תמיכה בעברית ואנגלית לפרויקט Next.js App Router שלי"
תוצאה: מתקינים next-intl, יוצרים סגמנט נתיב `[locale]`, מוסיפים `i18n/routing.ts`, `i18n/request.ts` ו-`proxy.ts` (`middleware.ts` לפני Next.js 16), עוטפים את `next.config.ts` עם `createNextIntlPlugin`, קובעים `dir="rtl"` על `<html>` ללוקאל עברי, יוצרים קובצי he.json ו-en.json עם תחביר ריבוי ICU, ומשתמשים בכלי Tailwind לוגיים (`ms-*`, `me-*`, `text-start`) לעיצוב מותאם RTL.

## משאבים מצורפים

### סקריפטים
- `scripts/generate_i18n.py` - יצירת קובצי הודעות i18n בעברית: בונה מבנה תרגום JSON עם צורות ריבוי עבריות בתחביר של כל פריימוורק (ICU ל-react-intl ול-next-intl, קווים אנכיים ל-vue-i18n, עם כלל הריבוי העברי משלב 1). הרצה: `python scripts/generate_i18n.py --help`

### קובצי עזר
- `references/pluralization.md` - כללי ריבוי מלאים בעברית עם צורות יחיד, זוגי ורבים לקטגוריות מילים נפוצות (זמן, כמויות, אובייקטים), נוסח כלל ה-CLDR העדכני, תבניות ICU MessageFormat, ומקרי קצה לשברים ולהסכמת מספרים בעברית.
- `references/bidi.md` - תבניות טיפול בטקסט דו-כיווני לאפליקציות עבריות: סקירה של אלגוריתם bidi של Unicode, שימוש בתכונת dir ב-HTML, תכונות CSS unicode-bidi, פתרונות bidi לפי פריימוורק, ומלכודות נפוצות עם תוכן מעורב עברית/אנגלית/מספרים.

## מלכודות נפוצות
- סוכנים עלולים להגדיר dir="rtl" רק על אלמנט ה-body או על div עוטף, אבל כיוון RTL חייב להיות מוגדר ברמת html כדי להשפיע נכון על פסי גלילה, יישור טקסט ברירת מחדל, ותכונות CSS לוגיות. באפליקציות עמוד יחיד, עדכנו את `document.documentElement.dir` כשהלוקאל משתנה.
- צורות רבים בעברית מורכבות: יש יחיד, זוגי (לחלק מהשמות), ורבים. סוכנים עלולים לממש יחיד/רבים בסגנון אנגלי (1 מול הרבה) ולפספס את צורת הזוגי (יומיים = 2 ימים למשל).
- סוכנים כותבים מחרוזות ריבוי ICU לכל פריימוורק. ספריית vue-i18n מצפה לצורות מופרדות בקו אנכי (ובגרסאות 11.x גם לכלל ריבוי עברי) ו-i18next מצפה לסיומות מפתח `_one`/`_two`/`_other`; מחרוזת ICU בהן תוצג כמו שהיא או לא תעבור ריבוי אף פעם.
- מפתחות i18n לעברית לא צריכים להשתמש בטקסט אנגלי כמפתח (t('Submit') למשל) כי תרגומים בעברית יכולים להיות הרבה יותר קצרים או ארוכים, וזה שובר layouts. תשתמשו במפתחות סמנטיים (t('form.submit') למשל).
- סוכנים שוכחים לפעמים להפוך מיקומי אייקונים ב-RTL: חיצים, שברונים ומחוונים צריכים להתהפך אופקית. חץ "הבא" צריך להצביע שמאלה בממשק עברי, לא ימינה.
- ההתנהגות של `space-x-*` ב-Tailwind שונה בין גרסאות. בגרסה 3 הוא קובע שוליים פיזיים שמאל/ימין ולא מתהפך, אז מוסיפים `space-x-reverse` תחת RTL או משתמשים ב-`gap-*`. בגרסה 4 הוא קובע `margin-inline-start/end`, שכבר עוקב אחרי `dir`, כך שהוספת `space-x-reverse` ל-RTL הופכת את הרווחים פעמיים. בשתי הגרסאות עדיף `gap-*` עם flex/grid.

## פתרון בעיות

### שגיאה: "צורות הריבוי לא תואמות לדקדוק עברי"
סיבה: מסגרת ה-i18n לא מוגדרת לכללי ריבוי של שלוש קטגוריות בעברית, או שההודעה כתובה בתחביר שהמסגרת לא מפרשת
פתרון: עברית משתמשת ב-one/two/other (לא רק one/other כמו באנגלית). ב-react-intl וב-next-intl תשתמשו ב-ICU MessageFormat עם קטגוריית `two`; ב-vue-i18n בקווים אנכיים `one | two | other` יחד עם פונקציית `pluralRules` לעברית; ב-i18next במפתחות `_one`/`_two`/`_other`. ב-React Native הוסיפו polyfill ל-`Intl.PluralRules`.

### שגיאה: "תאריך מוצג בפורמט MM/DD/YYYY במקום DD/MM/YYYY"
סיבה: משתמשים בלוקאל en-US במקום he-IL לפורמט תאריכים
פתרון: תשתמשו ב-`new Intl.DateTimeFormat('he-IL')` או הגדירו את ספריית התאריכים עם לוקאל he-IL. אף פעם אל תניחו פורמט תאריך אמריקאי למשתמשים ישראלים.

### שגיאה: "מחיר מעוצב נכשל בבדיקת שוויון או מומר למספר שגוי"
סיבה: הקריאה `Intl.NumberFormat('he-IL', { style: 'currency', currency: 'ILS' })` מוסיפה סימני כיוון U+200F, רווח קשיח ופסיקי אלפים
פתרון: השוו ושמרו מספרים גולמיים. להשוואת טקסט, הסירו את הסימנים עם `/[\u200E\u200F]/g` והחליפו U+00A0 ברווח רגיל. אל תריצו `parseFloat` על מחרוזת מעוצבת; הוא נעצר בפסיק הראשון.

### שגיאה: "מספרים מופיעים הפוך בהקשר RTL"
סיבה: כיוון ה-RTL משפיע על סדר הצגת הספרות
פתרון: מספרים בעברית הם תמיד LTR. תשתמשו ב-`dir="ltr"` על תוכן מספרי או תסתמכו על אלגוריתם bidi של Unicode שמטפל בספרות נכון כברירת מחדל. הבעיה היא בד"כ עם סימני הפיסוק שסביבם, לא עם הספרות עצמן.
