---
name: hebrew-rtl-best-practices
description: >-
  Implement right-to-left (RTL) layouts for Hebrew web applications.
  Use when user asks about RTL layout, Hebrew text direction, bidirectional
  (bidi) text, Hebrew CSS, "right to left", or needs to build a Hebrew web UI. Covers
  CSS logical properties, the :dir() pseudo-class, Tailwind RTL, React/Next.js RTL setup,
  icon mirroring, Hebrew typography, and font selection. Do NOT use for Arabic RTL
  (similar but different typography) unless user explicitly asks for shared RTL
  patterns, or for native mobile RTL (React Native I18nManager, SwiftUI, Android)
  which is out of scope.
license: MIT
compatibility: 'Works with Claude Code, Claude.ai, Cursor. No network required.'
---

# שיטות עבודה מומלצות ל-RTL בעברית

## הנחיות

### שלב 1: הגדרת כיוון המסמך
תמיד מתחילים עם תכונת ה-HTML (לא רק עם CSS):

```html
<html lang="he" dir="rtl">
```

זה אומר לדפדפנים, לקוראי מסך ול-CSS להשתמש ב-RTL ככיוון הבסיס.

### שלב 2: תכונות CSS לוגיות
אף פעם לא להשתמש בתכונות כיווניות פיזיות לפריסה:

| פיזי (תימנעו) | לוגי (תשתמשו) |
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

ככה הפריסה משתקפת אוטומטית במצב RTL.

כשבאמת צריך כלל שתלוי בכיוון שתכונות לוגיות לא יכולות לבטא, עדיף להשתמש בפסבדו-קלאס `:dir()` במקום בסלקטורים על תכונת `[dir="rtl"]`:

```css
/* מודרני: מתאים לכיוון המחושב, כולל dir="auto" וירושה */
.chevron:dir(rtl) { transform: scaleX(-1); }

/* גישה ישנה: מתאים רק לתכונת dir מפורשת על האלמנט או מעליו */
[dir="rtl"] .chevron { transform: scaleX(-1); }
```

הפסבדו-קלאס `:dir()` הוא חלק מ-Selectors Level 4 והוא פותר את הכיוון *המחושב*, אז הוא עובד גם לאלמנטים שהכיוון שלהם מגיע מ-`dir="auto"` או מאב קדמון, איפה שסלקטור תכונה היה מפספס אותם. תמיכת דפדפנים: כרום ו-Edge הוסיפו אותו בגרסה 120 (סוף 2023), פיירפוקס תומך בו כבר שנים, וספארי הוסיף אותו ב-16.4, ולכן הוא כיום Baseline (זמין באופן נרחב בדפדפנים). לתמיכה בדפדפנים ישנים, כדאי לשמור כלל גיבוי עם `[dir="rtl"]` או להשתמש בתכונה לוגית במקום. אפשר לבדוק תמיכה עדכנית בכתובת https://caniuse.com/css-dir-pseudo.

### שלב 3: טיפול בטקסט דו-כיווני
כשמשלבים עברית עם אנגלית/מספרים:

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
- מספרי טלפון מופיעים הפוך: עוטפים ב-`<bdo dir="ltr">`
- סימני פיסוק בקצה הלא נכון של המשפט: משתמשים ב-`unicode-bidi: isolate`
- כתובות URL ואימייל בתוך טקסט עברי: עוטפים ב-`<span dir="ltr">`

מספרים ותאריכים: מספרים בודדים ותאריכים בפורמט `DD/MM/YYYY` בתוך טקסט עברי בדרך כלל מוצגים תקין כי ספרות הן חלשות-LTR, אבל מספר שאחריו מיד סימן, מטבע או מספר שני עלול להתהפך. כשערך חייב לשמור על סדר ויזואלי קבוע, בודדו אותו עם `<span dir="ltr">` או `unicode-bidi: isolate` במקום לסמוך על פתרון ה-bidi הדיפולטי.

עצבו את הערך ואז בודדו אותו: בידוד bidi רק מונע ממחרוזת *תקינה* להתהפך, הוא לא מייצר את המחרוזת הנכונה. השתמשו ב-Intl לעיצוב ואז בודדו: `Intl.NumberFormat('he-IL', { style: 'currency', currency: 'ILS' })` לסכומים בשקלים ו-`Intl.DateTimeFormat('he-IL')` לתאריכים, ועטפו את הפלט ב-`<span dir="ltr">` (או `unicode-bidi: isolate`) אם הוא יושב בתוך טקסט עברי. מפתחים נוטים לבלבל בין השניים ולהחיל תיקון bidi על באג עיצוב (ולהפך).

שדות טופס צריכים `dir="auto"`: הוסיפו `dir="auto"` לכל `<input>` ו-`<textarea>` כדי שכל ערך יפתור את כיוון הבסיס שלו. זה הבאג הכי בולט למשתמש קצה ב-RTL: אימייל או מילה באנגלית בתוך טופס עברי קופצים לצד הלא נכון בלעדיו. שימו לב שה-placeholder לא מפעיל זיהוי אוטומטי, אז קבעו את כיוון המנוחה ב-CSS אם המראה של שדה ריק חשוב.

האלמנט `<bdi>` מול `<bdo>`: השתמשו ב-`<bdo dir="ltr">` רק כשרוצים *לכפות* כיוון (הוא דורס את אלגוריתם ה-bidi). לתוכן שנוצר על ידי משתמשים או תוכן בכיוון לא ידוע, עדיף `<bdi>`, שמבודד את התוכן כך שהכיוון שלו מזוהה אוטומטית ולא יכול לדלוף לטקסט שמסביב:

```html
<!-- שם המשתמש יכול להיות בעברית או בלטינית; bdi מבודד אותו כך או כך -->
<p>שלום, <bdi>{{ userName }}</bdi>, ברוך הבא</p>
```

לשדות טקסט חופשי, `dir="auto"` (או `unicode-bidi: plaintext` ב-CSS) נותן לדפדפן לבחור את כיוון הבסיס לכל ערך, וזו ברירת המחדל הנכונה לתגובות, שמות ומחרוזות חיפוש שבהן לא יודעים מראש את השפה.

צללים וגרדיאנטים לא מתהפכים אוטומטית. תכונות CSS לוגיות משקפות פריסה, אבל היסטים וזוויות של `box-shadow`, `text-shadow` ו-`linear-gradient` הם פיזיים ונשארים קבועים כשהכיוון מתהפך. היסט צל של `4px 4px` שנראה תקין ב-LTR יצביע לכיוון "הלא נכון" ביחס לפריסת RTL. אותה מלכודת פיזית-לא-לוגית חלה גם על `transform-origin`, `background-position` ואנימציות keyframe מבוססות `translateX` (מגירות נשלפות, קרוסלות, אפקט נצנוץ התקדמות). הפכו כל אחד במפורש עם דריסת `:dir(rtl)` (או `[dir="rtl"]`) כשהכיוון שלו משמעותי.

### שלב 4: שיקוף אייקונים כיווניים

שיקוף אייקונים הוא אחד הבאגים הנפוצים ביותר ב-RTL. הכלל: לשקף אייקונים שהמשמעות שלהם קשורה לכיוון הקריאה, ולהשאיר את כל השאר במקום.

לשקף את אלה (הכיוון שלהם מקודד "קדימה/אחורה/הבא/הקודם" ביחס לסדר הקריאה):
- חצי ניווט, כפתורי קדימה ואחורה, שברונים בפירורי לחם
- חצי "שליחה" והגשה, חצי קרוסלה ועימוד
- חצי הזחה, קינון רשימות ותגובה
- מחווני התקדמות שמרמזים על תנועה קדימה

אל תשקפו את אלה (שיקוף הופך אותם לשגויים או לא מזוהים):
- לוגואים וסמלי מותג
- סימני וי וסימני X או סגירה
- כפתורי הפעלה של מדיה (כפתור הפעלה תמיד מצביע ימינה, הוא מתייחס לציר הזמן ולא לכיוון הקריאה)
- שעונים ואייקוני שעון אנלוגי (כיוון השעון אוניברסלי)
- אייקונים שמתארים עצמים מהעולם האמיתי עם כיוון קבוע (שפופרת טלפון, זכוכית מגדלת עם ידית, רוב אייקוני המוצר)

טכניקה, שיקוף עם טרנספורם היפוך אופקי:

```css
/* היפוך רק כשכיוון המסמך הוא RTL */
.icon-directional:dir(rtl) { transform: scaleX(-1); }
```

```html
<!-- Tailwind: variant של rtl: למקרים שתכונות לוגיות לא מכסות -->
<button class="rtl:-scale-x-100">
  <ArrowLeftIcon />
</button>
```

הרבה ערכות אייקונים (למשל Material Symbols) כבר מספקות וריאנטים מודעי-RTL, עדיף אותם על פני היפוך כשהם זמינים, כי אייקון הפוך עלול לעוות פרטים עדינים או טקסט מוטמע.

### שלב 5: טיפוגרפיה עברית
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

### שלב 6: הגדרה לפי פריימוורק

**Tailwind CSS RTL (v4, עדכני; כלים לוגיים מאז v3.3):**

עדיף להשתמש בכלי תכונות לוגיות במקום ב-variants של `rtl:`/`ltr:`:

| קלאס פיזי | קלאס לוגי | תכונת CSS |
|-----------|-----------|-----------|
| `ml-4` | `ms-4` | `margin-inline-start` |
| `mr-4` | `me-4` | `margin-inline-end` |
| `pl-4` | `ps-4` | `padding-inline-start` |
| `pr-4` | `pe-4` | `padding-inline-end` |
| `left-4` | `inset-s-4` (בעבר `start-4`) | `inset-inline-start` |
| `right-4` | `inset-e-4` (בעבר `end-4`) | `inset-inline-end` |
| `rounded-l-lg` | `rounded-s-lg` | `border-start-start-radius` + `border-end-start-radius` |
| `rounded-r-lg` | `rounded-e-lg` | `border-start-end-radius` + `border-end-end-radius` |

```html
<!-- רע: דורש שני קלאסים, נשבר בלי תכונת dir -->
<div class="ltr:ml-4 rtl:mr-4">...</div>

<!-- טוב: קלאס אחד, משתקף אוטומטית לפי dir -->
<div class="ms-4">...</div>
```

תשאירו את ה-variants של `rtl:` / `ltr:` רק למקרים שתכונות לוגיות לא מכסות (אייקונים כיווניים, transforms וכדומה).

**הערה ל-Tailwind v4:** גרסה 4 (זמינה רשמית מתחילת 2025, כיום v4.3) משתמשת בקונפיגורציה מבוססת CSS (`@import "tailwindcss"` ב-CSS) במקום `tailwind.config.js`. התכונות הלוגיות עובדות זהה בגרסאות 3 ו-4. החל מ-v4.3 (מאי 2026) כלי ה-inset הלוגיים `start-*`/`end-*` הוצאו משימוש לטובת `inset-s-*`/`inset-e-*` (השמות הישנים עדיין עובדים); כלי ה-margin/padding‏ `ms-*`/`me-*`/`ps-*`/`pe-*` לא הושפעו.

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

החבילה `next/font` שומרת את הגופן מקומית (בלי בקשות חיצוניות ל-Google Fonts, בלי הזזת פריסה).

**React עם MUI:**

גרסת MUI עדכנית (v9 נכון ל-2026) משתמשת בפיצול הרשמי `@mui/stylis-plugin-rtl`, ולא בחבילת הקהילה הישנה `stylis-plugin-rtl`. הפיצול הרשמי מתקן בעיות עם CSS layers ותומך בגרסאות Stylis עדכניות; זו ההגדרה המומלצת מאז MUI v6.

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

כדאי לאמת את שם הייבוא המדויק ואת ההגדרה מול מדריך ה-RTL העדכני של MUI (https://mui.com/material-ui/customization/right-to-left/) לגרסת ה-MUI שלכם.

ממשק ב-Portal (מודלים, תפריטים נפתחים, tooltips, הודעות toast): רכיבים שמרונדרים דרך portal (React `createPortal`, Radix, MUI Menu, Floating UI) נטענים תחת `document.body` ויורשים כיוון משם, אבל הרבה ספריות מניחות LTR. קבעו `dir` על `<html>` וגם העבירו את הגדרת הכיוון של הספרייה עצמה: ב-Radix צריך עטיפת `<DirectionProvider dir="rtl">`, ב-MUI צריך `direction: 'rtl'` ב-theme. אחרת חלוניות קופצות נפתחות בצד הלא נכון גם כשכל שאר העמוד תקין.

### שלב 7: מלכודות נפוצות שכדאי לבדוק
1. אייקונים כיווניים - צריך לשקף (ראו שלב 4 לאילו אייקונים להפוך ואילו להשאיר)
2. פסי התקדמות - צריכים להתמלא מימין לשמאל
3. סליידרים וקרוסלות - כיוון ההחלקה צריך להתהפך
4. תוויות טפסים - צריכות להיות מיושרות לימין
5. פירורי לחם (breadcrumbs) - כיוון המפריד צריך להתהפך
6. טבלאות - העמודות מסתדרות מחדש אוטומטית, אבל הכריחו תאים של מספרים, קוד ותאריכים חזרה ל-LTR עם `<td dir="ltr">` או `text-align: end`
7. גרפים - יכול להיות שציר ה-X צריך להתהפך לקוראים בעברית (ל-SVG אין תכונות לוגיות, אז השתמשו באפשרות `reversed`/`rtl` של ספריית הגרפים, לא ב-CSS)
8. צללים וגרדיאנטים - היסטים וזוויות פיזיים לא מתהפכים אוטומטית (ראו שלב 3)
9. אלמנטים קבועים (fixed) ודביקים (sticky) כמו כותרות, toasts, כפתורי FAB ומגירות - ערכי `left: 0` / `right: 0` קשיחים לא מתהפכים; השתמשו ב-`inset-inline-start` / `inset-inline-end`
10. פסי הגלילה יושבים משמאל ב-RTL - שמרו מקום עם `scrollbar-gutter: stable` כדי למנוע קפיצת תוכן; `text-wrap: balance` משפר כותרות בעברית

### שלב 8: אימות פריסת ה-RTL
כללי כתיבה לא מספיקים, אמתו לפני שילוח:
- הפכו את כל האפליקציה ל-`dir="rtl"` וסרקו אם משהו לא זז (סימן שהוא עדיין משתמש בתכונה פיזית).
- בדקו מחרוזת מעורבת אחת בכל משטח טקסט: `שלום John 050-1234567 ₪1,234` מפעילה עברית, לטינית, מספר טלפון וסכום מטבע בבת אחת.
- פתחו כל מודל, תפריט נפתח, tooltip ו-toast (ממשק ב-portal הוא הפספוס הנפוץ ביותר ב-RTL).
- בדקו אלמנטים קבועים/דביקים, גרפים/SVG, ושדות טופס עם `dir="auto"`.

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

<!-- נכון: מבודדים את תוכן ה-LTR -->
<p>התקשרו אלינו: <span dir="ltr">050-321-4450</span></p>
```

אפשר להשתמש ב-`unicode-bidi: isolate` על ה-span המכיל לפתרון מבוסס CSS בלבד.

### דוגמה 3: ניווט RTL ב-Tailwind
המשתמש אומר: "הסיידבר שלי בצד הלא נכון בעברית"

```html
<!-- רע: סיידבר תקוע בשמאל -->
<aside class="fixed left-0 w-64">...</aside>

<!-- טוב: סיידבר משתקף אוטומטית (inset-s-0; start-0 הוא הכינוי המיושן) -->
<aside class="fixed inset-s-0 w-64">...</aside>

<!-- אייקון חץ חזרה עדיין דורש variant של rtl: (היפוך אופקי, לא rtl:rotate-180 שמהפך גם אנכית) -->
<button class="rtl:-scale-x-100">
  <ArrowLeftIcon />
</button>
```

## משאבים מצורפים

### קובצי עזר
- `references/css-logical-properties.md` - טבלת מיפוי מלאה מתכונות CSS פיזיות ללוגיות (margin, padding, border, מיקום, יישור טקסט, גדלים) בתוספת המלצות למחסניות גופנים עבריים ל-sans-serif, serif ו-monospace. תסתכלו בו כשממירים גיליון סגנונות LTR לתכונות לוגיות תואמות RTL או בוחרים גופני ווב עבריים.

## מלכודות נפוצות
- הכלל `text-align: left` שגוי לעברית. תשתמשו ב-`text-align: start` שמכבד את כיוון המסמך. סוכנים נוטים לקודד יישור `left` ב-CSS.
- התכונות `margin-left` ו-`padding-right` לא מתהפכות במצב RTL. תשתמשו בתכונות CSS לוגיות: `margin-inline-start` ו-`padding-inline-end` במקום. סוכנים שאומנו על CSS של LTR ייצרו תכונות פיזיות.
- כיוון `row` ב-Flexbox מתהפך אוטומטית ב-RTL, אבל `row-reverse` גם מתהפך, מה שגורם להיפוך כפול וחזרה לסדר LTR. סוכנים עלולים להוסיף `row-reverse` כי הם חושבים שזה יוצר RTL, אבל בפועל זה יוצר LTR בתוך הקשר RTL.
- מספרי טלפון, מספרי כרטיסי אשראי וקטעי קוד חייבים להישאר LTR גם בתוך מיכלים RTL. תעטפו אותם ב-`<bdo dir="ltr">` או תשתמשו ב-`direction: ltr` על האלמנט המכיל. סוכנים לפעמים נותנים להם לרשת RTL.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| MDN תכונות CSS לוגיות | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | רשימת תכונות מלאה, טבלאות תמיכת דפדפנים |
| MDN פסבדו-קלאס `:dir()` | https://developer.mozilla.org/en-US/docs/Web/CSS/:dir | תחביר, התנהגות מול סלקטורים על תכונת `[dir]` |
| Can I use: `:dir()` | https://caniuse.com/css-dir-pseudo | טבלת תמיכת דפדפנים עדכנית |
| MDN אלמנט `<bdi>` | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi | בידוד תוכן דו-כיווני שנוצר על ידי משתמשים |
| תמיכת RTL ב-Tailwind CSS | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | תחביר variants של `rtl:` / `ltr:` |
| תכונות לוגיות ב-Tailwind | https://tailwindcss.com/docs/margin | כלי `ms-*`, `me-*`, `ps-*`, `pe-*` |
| MUI ימין לשמאל | https://mui.com/material-ui/customization/right-to-left/ | הגדרת `@mui/stylis-plugin-rtl` ל-MUI עדכני |
| Google Fonts עברית | https://fonts.google.com/?subset=hebrew | משפחות גופנים עבריים זמינות |
| W3C בינלאומיות | https://www.w3.org/International/articles/inline-bidi-markup/ | אלגוריתם bidi של Unicode, שיטות עבודה מומלצות |

## פתרון בעיות

### שגיאה: "יישור הטקסט נראה שגוי"
סיבה: שימוש ב-`text-align: left` במקום ב-`text-align: start`
פתרון: תחליפו כל `left` ו-`right` ב-`text-align` ל-`start` ו-`end`.

### שגיאה: "הפריסה לא משתקפת"
סיבה: שימוש ב-`margin` ו-`padding` פיזיים במקום בתכונות לוגיות
פתרון: תחליפו כל `margin-left` ו-`margin-right` ב-`margin-inline-start` ו-`margin-inline-end`.
