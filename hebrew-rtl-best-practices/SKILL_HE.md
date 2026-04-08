---
name: hebrew-rtl-best-practices
description: >-
  Implement right-to-left (RTL) layouts for Hebrew web and mobile applications.
  Use when user asks about RTL layout, Hebrew text direction, bidirectional
  (bidi) text, Hebrew CSS, "right to left", or needs to build Hebrew UI. Covers
  CSS logical properties, Tailwind RTL, React/Next.js RTL setup, Hebrew typography, and
  font selection. Do NOT use for Arabic RTL (similar but different typography)
  unless user explicitly asks for shared RTL patterns.
license: MIT
compatibility: 'Works with Claude Code, Claude.ai, Cursor. No network required.'
---

# שיטות עבודה מומלצות ל-RTL בעברית

## הנחיות

### שלב 1: הגדרת כיוון המסמך
תמיד להתחיל עם תכונת ה-HTML (לא רק CSS):

```html
<html lang="he" dir="rtl">
```

זה מורה לדפדפנים, קוראי מסך ו-CSS להשתמש ב-RTL ככיוון הבסיס.

### שלב 2: שימוש בתכונות CSS לוגיות
לעולם לא להשתמש בתכונות כיווניות פיזיות לפריסה:

| פיזי (יש להימנע) | לוגי (יש להשתמש) |
|-------------------|-----------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `border-left` | `border-inline-start` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `float: left` | `float: inline-start` |
| `left: 10px` | `inset-inline-start: 10px` |

כך הפריסה תשתקף אוטומטית במצב RTL.

### שלב 3: טיפול בטקסט דו-כיווני
בעת שילוב עברית עם אנגלית/מספרים:

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

בעיות bidi נפוצות:
- מספרי טלפון מופיעים הפוך: עטיפה ב-`<bdo dir="ltr">`
- סימני פיסוק בקצה הלא נכון של המשפט: שימוש ב-`unicode-bidi: isolate`
- כתובות URL/אימייל בתוך טקסט עברי: עטיפה ב-`<span dir="ltr">`

### שלב 4: טיפוגרפיה עברית
מחסנית גופנים מומלצת:
```css
font-family: 'Heebo', 'Assistant', 'Rubik', 'Noto Sans Hebrew', sans-serif;
```

הגדרות טיפוגרפיה:
```css
body[dir="rtl"] {
  font-size: 16px; /* Hebrew needs slightly larger than Latin */
  line-height: 1.7;
  letter-spacing: normal; /* NEVER add letter-spacing for Hebrew */
  word-spacing: 0.05em; /* Slight word spacing improves readability */
}
```

### שלב 5: הגדרה לפי פריימוורק

**Tailwind CSS RTL (v3.3+ / v4):**

עדיף להשתמש בכלי תכונות לוגיות במקום variants של `rtl:`/`ltr:`:

| קלאס פיזי | קלאס לוגי | תכונת CSS |
|-----------|-----------|-----------|
| `ml-4` | `ms-4` | `margin-inline-start` |
| `mr-4` | `me-4` | `margin-inline-end` |
| `pl-4` | `ps-4` | `padding-inline-start` |
| `pr-4` | `pe-4` | `padding-inline-end` |
| `left-4` | `start-4` | `inset-inline-start` |
| `right-4` | `end-4` | `inset-inline-end` |
| `rounded-l-lg` | `rounded-s-lg` | `border-start-start-radius` + `border-end-start-radius` |
| `rounded-r-lg` | `rounded-e-lg` | `border-start-end-radius` + `border-end-end-radius` |

```html
<!-- רע: דורש שני קלאסים, נשבר בלי תכונת dir -->
<div class="ltr:ml-4 rtl:mr-4">...</div>

<!-- טוב: קלאס אחד, משתקף אוטומטית לפי dir -->
<div class="ms-4">...</div>
```

יש לשמור את variants של `rtl:` / `ltr:` רק למקרים שתכונות לוגיות לא מכסות (למשל אייקונים כיווניים, transforms).

**הערה ל-Tailwind v4:** גרסה 4 משתמשת בקונפיגורציה מבוססת CSS (`@import "tailwindcss"` ב-CSS) במקום `tailwind.config.js`. התכונות הלוגיות עובדות זהה בגרסאות 3 ו-4.

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

`next/font` מאחסן את הגופן מקומית (ללא בקשות חיצוניות ל-Google Fonts, אפס הזזת פריסה).

**React עם MUI:**
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

### שלב 6: מלכודות נפוצות לבדיקה
1. אייקונים עם משמעות כיוונית (חצים, כפתורי חזרה) — יש לשקפם
2. פסי התקדמות — צריכים להתמלא מימין לשמאל
3. סליידרים/קרוסלות — כיוון החלקה צריך להתהפך
4. תוויות טפסים — צריכות להיות מיושרות לימין
5. פירורי לחם (breadcrumbs) — כיוון המפריד צריך להתהפך
6. טבלאות — יישור כותרות ותאים
7. גרפים — ייתכן שציר ה-X צריך להתהפך עבור קוראים בעברית

## דוגמאות

### דוגמה 1: המרת רכיב LTR ל-RTL
המשתמש אומר: "התאם את רכיב הכרטיס הזה לעבודה בעברית"

לפני (LTR בלבד):
```css
.card {
  margin-left: 16px;
  padding-right: 12px;
  text-align: left;
  border-left: 3px solid blue;
}
```

אחרי (תואם RTL):
```css
.card {
  margin-inline-start: 16px;
  padding-inline-end: 12px;
  text-align: start;
  border-inline-start: 3px solid blue;
}
```

ב-Tailwind, מחליפים `ml-4 pr-3 text-left border-l-4` ב-`ms-4 pe-3 text-start border-s-4`.

### דוגמה 2: בעיית טקסט דו-כיווני
המשתמש אומר: "מספרים מוצגים הפוך בטקסט העברי שלי"

```html
<!-- שגוי: מספר הטלפון מוצג כ-0544-123-050 -->
<p>התקשרו אלינו: 050-321-4450</p>

<!-- נכון: בידוד התוכן ה-LTR -->
<p>התקשרו אלינו: <span dir="ltr">050-321-4450</span></p>
```

ניתן להשתמש ב-`unicode-bidi: isolate` על ה-span המכיל לפתרון מבוסס CSS בלבד.

### דוגמה 3: ניווט RTL ב-Tailwind
המשתמש אומר: "הסיידבר שלי בצד הלא נכון בעברית"

```html
<!-- רע: סיידבר תקוע בשמאל -->
<aside class="fixed left-0 w-64">...</aside>

<!-- טוב: סיידבר משתקף אוטומטית -->
<aside class="fixed start-0 w-64">...</aside>

<!-- אייקון חץ חזרה עדיין דורש variant של rtl: -->
<button class="rtl:rotate-180">
  <ArrowLeftIcon />
</button>
```

## משאבים מצורפים

### קובצי עזר
- `references/css-logical-properties.md` — טבלת מיפוי מלאה מתכונות CSS פיזיות ללוגיות (margin, padding, border, מיקום, יישור טקסט, גדלים) בתוספת המלצות למחסניות גופנים עבריים ל-sans-serif, serif ו-monospace. יש לעיין בו בעת המרת גיליון סגנונות LTR לתכונות לוגיות תואמות RTL או בחירת גופני ווב עבריים.

## מלכודות נפוצות
- CSS text-align: left הוא שגוי לעברית. יש להשתמש ב-text-align: start שמכבד את כיוון המסמך. סוכנים מקודדים לעתים יישור left ב-CSS.
- margin-left ו-padding-right לא מתהפכים במצב RTL. יש להשתמש בתכונות CSS לוגיות: margin-inline-start ו-padding-inline-end במקום. סוכנים שאומנו על CSS של LTR ייצרו תכונות פיזיות.
- כיוון row ב-Flexbox מתהפך אוטומטית ב-RTL, אבל row-reverse גם מתהפך, מה שגורם להיפוך כפול בחזרה לסדר LTR. סוכנים עלולים להוסיף row-reverse בחושבם שזה יוצר RTL, אבל בפועל זה יוצר LTR בתוך הקשר RTL.
- מספרי טלפון, מספרי כרטיסי אשראי וקטעי קוד חייבים להישאר LTR גם בתוך מיכלים RTL. יש לעטוף אותם ב-bdo dir="ltr" או להשתמש ב-direction: ltr על האלמנט המכיל. סוכנים לעתים נותנים להם לרשת RTL.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| MDN תכונות CSS לוגיות | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | רשימת תכונות מלאה, טבלאות תמיכת דפדפנים |
| תמיכת RTL ב-Tailwind CSS | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | תחביר variants של `rtl:` / `ltr:` |
| תכונות לוגיות ב-Tailwind | https://tailwindcss.com/docs/margin#logical-properties | כלי `ms-*`, `me-*`, `ps-*`, `pe-*` |
| Google Fonts עברית | https://fonts.google.com/?subset=hebrew | משפחות גופנים עבריים זמינות |
| W3C בינלאומיות | https://www.w3.org/International/articles/inline-bidi-markup/ | אלגוריתם bidi של Unicode, שיטות עבודה מומלצות |

## פתרון בעיות

### שגיאה: "יישור הטקסט נראה שגוי"
סיבה: שימוש ב-`text-align: left` במקום `text-align: start`
פתרון: החלפת כל `left`/`right` ב-text-align ב-`start`/`end`.

### שגיאה: "הפריסה לא משתקפת"
סיבה: שימוש ב-margin/padding פיזיים במקום תכונות לוגיות
פתרון: החלפת כל `margin-left`/`margin-right` ב-`margin-inline-start`/`margin-inline-end`.