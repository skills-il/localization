# בינלאומיות עברית

## הנחיות

### שלב 1: הגדרת מסגרת I18n

**React (react-intl / react-i18next):**
```jsx
import { IntlProvider } from 'react-intl';
import heMessages from './locales/he.json';

function App() {
  return (
    <IntlProvider locale="he" messages={heMessages}>
      <div dir="rtl" lang="he">
        {/* תוכן האפליקציה */}
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

**Next.js App Router (next-intl):**
```tsx
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({ children, params }) {
  const { locale } = await params;
  const messages = await getMessages();
  return (
    <html lang={locale} dir={locale === 'he' ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

```ts
// middleware.ts
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';
export default createMiddleware(routing);
```

```ts
// i18n/routing.ts
import { defineRouting } from 'next-intl/routing';
export const routing = defineRouting({
  locales: ['he', 'en'],
  defaultLocale: 'he',
});
```

**Angular:**
```typescript
// angular.json -- הוספת לוקאל עברי
"i18n": {
  "sourceLocale": "en",
  "locales": {
    "he": "src/locale/messages.he.xlf"
  }
}
```

### שלב 2: צורות ריבוי בעברית

לעברית שלוש קטגוריות ריבוי שמסגרות i18n חייבות לטפל בהן:

| קטגוריה | מונח עברי | ספירה | דוגמה |
|----------|-----------|-------|---------|
| יחיד (one) | יחיד | 1 | פריט אחד |
| זוגי (two) | זוגי | 2 | שני פריטים -- משתמש בצורת זוגי מיוחדת |
| רבים (other) | רבים | 0, 3+ | 5 פריטים |

ראו `references/pluralization.md` לכללים מלאים ומקרי קצה.

**תבנית ICU MessageFormat:**
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

### שלב 3: עיצוב תאריך ושעה

**פורמט תאריך ישראלי:** DD/MM/YYYY (לא MM/DD/YYYY)

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
// פלט: "04/03/2026" (DD/MM/YYYY)
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

שבוע עבודה ישראלי: יום ראשון עד יום חמישי (לא שני עד שישי).

**תאריכים בלוח העברי:** שימוש בספריות כמו `hebcal` להמרת לוח עברי. פורמט: יום + שם חודש עברי (למשל "ה׳ באדר תשפ״ו").

### שלב 4: עיצוב מספרים ומטבע

```javascript
// פורמט מספרים ישראלי: 1,000.50 (פסיק לאלפים, נקודה לעשרוני)
const numFormatter = new Intl.NumberFormat('he-IL');
numFormatter.format(1234567.89); // "1,234,567.89"

// מטבע שקל ישראלי
const currFormatter = new Intl.NumberFormat('he-IL', {
  style: 'currency',
  currency: 'ILS',
});
currFormatter.format(1234.50); // "1,234.50 ₪"
```

**תבניות מספרים ישראליות:**

| סוג | פורמט | דוגמה |
|------|--------|---------|
| טלפון (נייד) | 05X-XXXXXXX | 054-1234567 |
| טלפון (קווי) | 0X-XXXXXXX | 02-6234567 |
| תעודת זהות | XXXXXXXXX | 123456782 (9 ספרות עם ספרת ביקורת) |
| מיקוד | XXXXXXX | 6100000 (7 ספרות) |
| מטבע | X,XXX.XX ₪ | 1,234.50 ₪ |

### שלב 5: CSS עם תכונות לוגיות ל-RTL

תמיד להשתמש בתכונות CSS לוגיות לפריסות מוכנות ל-i18n:

```css
/* הגדרת RTL בסיסית */
html[lang="he"] {
  direction: rtl;
}

/* תכונות לוגיות -- עובדות גם ב-LTR וגם ב-RTL */
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
  /* אין צורך בשינוי כיוון -- flex מכבד תכונת dir */
}
```

**Tailwind CSS RTL (v3.3+):**

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

| פיזי (להימנע) | לוגי (מומלץ) | התנהגות ב-RTL |
|----------------|--------------|---------------|
| `ml-4` | `ms-4` | שוליים ימניים ב-RTL |
| `mr-4` | `me-4` | שוליים שמאליים ב-RTL |
| `pl-4` | `ps-4` | ריפוד ימני ב-RTL |
| `pr-4` | `pe-4` | ריפוד שמאלי ב-RTL |
| `text-left` | `text-start` | יישור לימין ב-RTL |
| `text-right` | `text-end` | יישור לשמאל ב-RTL |
| `rounded-l-lg` | `rounded-s-lg` | עיגול פינות ימניות ב-RTL |
| `border-r-2` | `border-e-2` | גבול שמאלי ב-RTL |

### שלב 6: טיפול בטקסט דו-כיווני

ראו `references/bidi.md` לתבניות מפורטות ומקרי קצה.

```html
<!-- בידוד תוכן LTR בתוך טקסט עברי -->
<p dir="rtl">
  הזמנה מספר <span dir="ltr">ORD-12345</span> אושרה
</p>

<!-- שימוש באלמנט bdi לתוכן שנוצר על ידי משתמשים -->
<p dir="rtl">
  המשתמש <bdi>JohnDoe123</bdi> נרשם
</p>
```

**תרחישי bidi נפוצים באפליקציות ישראליות:**

| סוג תוכן | כיוון | טיפול |
|-----------|-------|--------|
| טקסט עברי | RTL | ברירת מחדל, ללא טיפול מיוחד |
| טקסט אנגלי בתוך עברי | LTR | עטיפה ב-`dir="ltr"` span |
| מספרי טלפון | LTR | עטיפה ב-`dir="ltr"` או `bdo` |
| כתובות URL ואימייל | LTR | עטיפה ב-`dir="ltr"` span |
| עברית מעורבת + קוד | שניהם | שימוש ב-`unicode-bidi: isolate` |
| סכומי מטבע | מספרים LTR + סמל RTL | שימוש ב-Intl.NumberFormat |

### שלב 7: אינטגרציית RTL ספציפית לפריימוורק

**Next.js App Router עם Tailwind:**
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
// components/NavBar.tsx -- שימוש ב-rtl: variant להיפוך אייקונים
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

**Vue עם Vuetify:**
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

// בתבנית:
// <div dir="rtl">...</div>
```

## דוגמאות

### דוגמה 1: הוספת עברית לאפליקציית React קיימת
המשתמש אומר: "אני צריך להוסיף תמיכה בעברית לאפליקציית ה-React שלי"
תוצאה: הגדרת react-i18next עם לוקאל עברי, יצירת קובץ הודעות he.json, הגדרת כללי ריבוי, הוספת עטיפת RTL עם dir="rtl", החלפת מחרוזות קשיחות במפתחות תרגום, וטיפול בטקסט bidi לתוכן מעורב.

### דוגמה 2: עיצוב תאריכים ומחירים ישראליים
המשתמש אומר: "איך אני מעצב תאריכים ומחירים למשתמשים ישראליים?"
תוצאה: שימוש ב-Intl.DateTimeFormat עם לוקאל he-IL לתאריכים בפורמט DD/MM/YYYY, Intl.NumberFormat עם מטבע ILS לעיצוב שקלים, ווידוא שמספרים מוצגים נכון בהקשר RTL.

### דוגמה 3: תיקון בעיות טקסט דו-כיווני
המשתמש אומר: "מספרי טלפון וטקסט באנגלית נראים שגוי בממשק העברי שלי"
תוצאה: עטיפת מספרי טלפון ב-spans עם `dir="ltr"`, בידוד תוכן אנגלי עם `unicode-bidi: isolate`, שימוש באלמנט `bdi` לתוכן שנוצר על ידי משתמשים, ובדיקה עם מחרוזות מעורבות עברית/אנגלית.

### דוגמה 4: צורות ריבוי בעברית
המשתמש אומר: "התרגומים בעברית מציגים צורות ריבוי שגויות"
תוצאה: מימוש ICU MessageFormat עם שלוש קטגוריות (one/two/other), טיפול בצורות זוגי עבור יחידות זמן, והגדרת כללי ריבוי של מסגרת ה-i18n ללוקאל עברי.

### דוגמה 5: הוספת עברית לפרויקט Next.js App Router
המשתמש אומר: "אני רוצה להוסיף תמיכה בעברית ואנגלית לפרויקט Next.js App Router שלי"
תוצאה: התקנת next-intl, יצירת סגמנט נתיב `[locale]`, הגדרת middleware לזיהוי שפה, הגדרת `dir="rtl"` על `<html>` ללוקאל עברי, יצירת קובצי הודעות he.json ו-en.json עם תחביר ריבוי ICU, ושימוש בכלי Tailwind לוגיים (`ms-*`, `me-*`, `text-start`) לעיצוב מותאם RTL.

## משאבים מצורפים

### סקריפטים
- `scripts/generate_i18n.py` — יצירת קובצי הודעות i18n בעברית: פיגום מבנה תרגום JSON, חילוץ תבניות ריבוי עבריות, הפקת קובצי לוקאל ל-react-intl, vue-i18n ו-next-intl. הרצה: `python scripts/generate_i18n.py --help`

### קובצי עזר
- `references/pluralization.md` — כללי ריבוי מלאים בעברית עם צורות יחיד, זוגי ורבים לקטגוריות מילים נפוצות (זמן, כמויות, אובייקטים), תבניות ICU MessageFormat, ומקרי קצה להסכמת מספרים בעברית.
- `references/bidi.md` — תבניות טיפול בטקסט דו-כיווני לאפליקציות עבריות: סקירת אלגוריתם bidi של Unicode, שימוש בתכונת dir ב-HTML, תכונות CSS unicode-bidi, פתרונות bidi ספציפיים לפריימוורק, ומלכודות נפוצות עם תוכן מעורב עברית/אנגלית/מספרים.

## מלכודות נפוצות
- סוכנים עלולים להגדיר dir="rtl" רק על אלמנט ה-body, אבל כיוון RTL חייב להיות מוגדר ברמת html כדי להשפיע נכון על פסי גלילה, יישור טקסט ברירת מחדל, ותכונות CSS לוגיות.
- צורות רבים בעברית מורכבות: יש יחיד, זוגי (לחלק מהשמות), ורבים. סוכנים עלולים לממש יחיד/רבים בסגנון אנגלית (1 מול הרבה) ולפספס את צורת הזוגי (למשל יומיים = 2 ימים).
- מפתחות i18n לעברית לא צריכים להשתמש בטקסט אנגלי כמפתח (למשל t('Submit')) כי תרגומים עבריים יכולים להיות הרבה יותר קצרים או ארוכים, מה ששובר layouts. יש להשתמש במפתחות סמנטיים (למשל t('form.submit')).
- סוכנים שוכחים לעתים להפוך מיקומי אייקונים ב-RTL: חיצים, שברונים ומחוונים צריכים להשתקף אופקית. חץ "הבא" צריך להצביע שמאלה בממשק עברי, לא ימינה.
- ב-Tailwind CSS, הכלי `space-x-*` לא מתהפך אוטומטית ב-RTL. עדיף להשתמש ב-`gap-*` עם flex/grid, או להוסיף `space-x-reverse` כש-RTL פעיל. באופן דומה, העדיפו כלים לוגיים (`ms-*`, `me-*`, `ps-*`, `pe-*`) על פני פיזיים (`ml-*`, `mr-*`, `pl-*`, `pr-*`).

## פתרון בעיות

### שגיאה: "צורות ריבוי לא תואמות דקדוק עברי"
סיבה: מסגרת i18n לא מוגדרת לכללי ריבוי בעלי שלוש קטגוריות בעברית
פתרון: עברית משתמשת ב-one/two/other (לא רק one/other כמו באנגלית). יש לוודא שהמסגרת מוגדרת עם כללי ריבוי CLDR לעברית. ב-react-intl, שימוש ב-ICU MessageFormat עם קטגוריית `two`.

### שגיאה: "תאריך מוצג בפורמט MM/DD/YYYY במקום DD/MM/YYYY"
סיבה: שימוש בלוקאל en-US במקום he-IL לעיצוב תאריכים
פתרון: שימוש ב-`new Intl.DateTimeFormat('he-IL')` או הגדרת ספריית התאריכים עם לוקאל he-IL. לעולם לא להניח פורמט תאריך אמריקאי למשתמשים ישראליים.

### שגיאה: "מספרים מופיעים הפוך בהקשר RTL"
סיבה: כיוון RTL משפיע על סדר הצגת ספרות
פתרון: מספרים בעברית הם תמיד LTR. שימוש ב-`dir="ltr"` על תוכן מספרי או הסתמכות על אלגוריתם bidi של Unicode שמטפל בספרות נכון כברירת מחדל. הבעיה היא בדרך כלל עם סימני פיסוק סביבם, לא עם הספרות עצמן.
