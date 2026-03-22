---
name: hebrew-rtl-best-practices
description: >-
  Implement right-to-left (RTL) layouts for Hebrew web and mobile applications.
  Use when user asks about RTL layout, Hebrew text direction, bidirectional
  (bidi) text, Hebrew CSS, "right to left", or needs to build Hebrew UI. Covers
  CSS logical properties, Tailwind RTL, React/Vue RTL, Hebrew typography, and
  font selection. Do NOT use for Arabic RTL (similar but different typography)
  unless user explicitly asks for shared RTL patterns.
license: MIT
compatibility: 'Works with Claude Code, Claude.ai, Cursor. No network required.'
metadata:
  author: skills-il
  version: 1.1.0
  category: localization
  tags:
    he:
      - ימין-לשמאל
      - עברית
      - CSS
      - פריסה
      - טיפוגרפיה
      - דו-כיווני
    en:
      - rtl
      - hebrew
      - css
      - layout
      - typography
      - bidi
  display_name:
    he: שיטות עבודה מומלצות ל-RTL
    en: Hebrew Rtl Best Practices
  display_description:
    he: הנחיות ותבניות ליצירת ממשקים עבריים עם תמיכה מלאה בכתיבה מימין לשמאל
    en: >-
      Implement right-to-left (RTL) layouts for Hebrew web and mobile
      applications. Use when user asks about RTL layout, Hebrew text direction,
      bidirectional (bidi) text, Hebrew CSS, "right to left", or needs to build
      Hebrew UI. Covers CSS logical properties, Tailwind RTL, React/Vue RTL,
      Hebrew typography, and font selection. Do NOT use for Arabic RTL (similar
      but different typography) unless user explicitly asks for shared RTL
      patterns.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
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

**Tailwind CSS RTL:**
```js
// tailwind.config.js
module.exports = {
  // Tailwind v2.2+ has built-in RTL support with rtl: and ltr: variants
}
```
```html
<div class="ltr:ml-4 rtl:mr-4">
  <!-- Or better: use logical utilities if available -->
</div>
```

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

**Next.js:**
הוספת `dir="rtl"` לפריסת השורש והגדרת טעינת גופנים עבריים.

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
תוצאה: החלפת כל תכונות ה-CSS הפיזיות במקבילות לוגיות, הוספת dir="rtl", התאמת מחסנית גופנים.

### דוגמה 2: בעיית טקסט דו-כיווני
המשתמש אומר: "מספרים מוצגים הפוך בטקסט העברי שלי"
תוצאה: עטיפת תוכן מספרי ב-span עם dir="ltr" ו-unicode-bidi: isolate.

## משאבים מצורפים

### קובצי עזר
- `references/css-logical-properties.md` — טבלת מיפוי מלאה מתכונות CSS פיזיות ללוגיות (margin, padding, border, מיקום, יישור טקסט, גדלים) בתוספת המלצות למחסניות גופנים עבריים ל-sans-serif, serif ו-monospace. יש לעיין בו בעת המרת גיליון סגנונות LTR לתכונות לוגיות תואמות RTL או בחירת גופני ווב עבריים.

## מלכודות נפוצות
- CSS text-align: left הוא שגוי לעברית. יש להשתמש ב-text-align: start שמכבד את כיוון המסמך. סוכנים מקודדים לעתים יישור left ב-CSS.
- margin-left ו-padding-right לא מתהפכים במצב RTL. יש להשתמש בתכונות CSS לוגיות: margin-inline-start ו-padding-inline-end במקום. סוכנים שאומנו על CSS של LTR ייצרו תכונות פיזיות.
- כיוון row ב-Flexbox מתהפך אוטומטית ב-RTL, אבל row-reverse גם מתהפך, מה שגורם להיפוך כפול בחזרה לסדר LTR. סוכנים עלולים להוסיף row-reverse בחושבם שזה יוצר RTL, אבל בפועל זה יוצר LTR בתוך הקשר RTL.
- מספרי טלפון, מספרי כרטיסי אשראי וקטעי קוד חייבים להישאר LTR גם בתוך מיכלים RTL. יש לעטוף אותם ב-bdo dir="ltr" או להשתמש ב-direction: ltr על האלמנט המכיל. סוכנים לעתים נותנים להם לרשת RTL.

## פתרון בעיות

### שגיאה: "יישור הטקסט נראה שגוי"
סיבה: שימוש ב-`text-align: left` במקום `text-align: start`
פתרון: החלפת כל `left`/`right` ב-text-align ב-`start`/`end`.

### שגיאה: "הפריסה לא משתקפת"
סיבה: שימוש ב-margin/padding פיזיים במקום תכונות לוגיות
פתרון: החלפת כל `margin-left`/`margin-right` ב-`margin-inline-start`/`margin-inline-end`.