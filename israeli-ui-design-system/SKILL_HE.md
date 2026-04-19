# מערכת עיצוב ישראלית

## הנחיות

### שלב 1: בחירת זיווגי גופנים עבריים

תבחרו שילובי גופנים שמותאמים לקריאות בעברית ולתאימות לטינית:

| זיווג | גופן עברי | גופן לטיני | מתאים ל- | סגנון |
|-------|-----------|------------|----------|-------|
| עסקי מודרני | Heebo | Inter | SaaS, לוחות בקרה, ממשקי ניהול | נקי, ניטרלי |
| סטארטאפ ידידותי | Rubik | Source Sans Pro | אפליקציות צרכניות, אתרי שיווק | מעוגל, נגיש |
| ממשלתי/רשמי | Assistant | Roboto | אתרים ממשלתיים, דפים מוסדיים | מקצועי, בהיר |
| עריכה | Frank Ruhl Libre | Merriweather | בלוגים, חדשות, אתרי תוכן | סריף, ספרותי |
| מינימלי | Secular One | Montserrat | דפי נחיתה, תיקי עבודות | כותרות בולטות |

תסתכלו על `references/hebrew-typography.md` למדדי גופנים מלאים ולאסטרטגיות טעינה.

**תצורת טעינת גופנים:**
```css
/* ראשי: זיווג Heebo + Inter */
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

### שלב 2: סולם טיפוגרפי לעברית

תווים בעברית נראים גדולים יותר חזותית מתווים לטיניים באותו גודל גופן. תתאימו את סולם הגדלים:

```css
:root {
  /* סולם גדלים מותאם לעברית */
  --text-xs: 0.8125rem;   /* 13px -- מינימום קריא בעברית */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px -- מינימום לגוף טקסט עברי */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */

  /* גובהי שורה ייחודיים לעברית (גבוהים יותר מאשר בלטינית) */
  --leading-tight: 1.4;
  --leading-normal: 1.7;
  --leading-relaxed: 1.9;

  /* אף פעם לא להשתמש ב-letter-spacing בעברית */
  --tracking-hebrew: normal;
  /* ריווח מילים קל משפר את הקריאות בעברית */
  --word-spacing-hebrew: 0.05em;
}

/* גוף טקסט עברי */
body[dir="rtl"] {
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  letter-spacing: var(--tracking-hebrew);
  word-spacing: var(--word-spacing-hebrew);
}
```

### שלב 3: ארכיטקטורת רכיבים RTL-First

תעצבו רכיבים כש-RTL הוא ברירת המחדל, לא מחשבה שנייה:

```css
/* רכיב כפתור RTL-first */
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
  /* האייקון מתהפך אוטומטית ב-RTL */
}

.btn-icon-start {
  flex-direction: row;
  /* ב-RTL: האייקון מופיע מימין (צד ההתחלה) */
}

.btn-icon-end {
  flex-direction: row-reverse;
  /* ב-RTL: האייקון מופיע משמאל (צד הסיום) */
}

/* רכיב כרטיס RTL-first */
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

/* פריסת סרגל צד RTL-first */
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  /* ב-RTL: הסרגל הצדדי מופיע מימין אוטומטית */
}

.layout-sidebar {
  border-inline-end: 1px solid var(--border-color);
  padding-inline-end: 1.5rem;
}
```

### שלב 4: פלטת צבעים ותגי עיצוב ישראליים

```css
:root {
  /* תגי צבע מותאמים לישראל */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* צבעי סטטוס (אוניברסליים) */
  --color-success: #16a34a;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: #2563eb;

  /* פלטת אפורים */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-500: #6b7280;
  --color-gray-700: #374151;
  --color-gray-900: #111827;

  /* סולם ריווח */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;

  /* רדיוס גבול */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;
}
```

### שלב 5: תבניות עיצוב gov.il

לאתרים ממשלתיים ומוסדיים ישראליים, תלכו לפי מערכת העיצוב של gov.il:

```css
/* כותרת בהשראת gov.il */
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
  /* לוגו + שם אתר בעברית, מיושר לימין ב-RTL */
}

/* תבניות טפסי gov.il */
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

/* מחוון שלבים gov.il */
.gov-steps {
  display: flex;
  gap: var(--space-4);
  padding: 0;
  list-style: none;
  /* ב-RTL: השלבים זורמים מימין לשמאל */
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

### שלב 6: תבניות טפסים RTL-First

```html
<!-- טופס כתובת ישראלי -->
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

### שלב 7: מוסכמות פורמט ישראליות (מטבע, מספרים, תאריכים)

תגי עיצוב ורכיבים צריכים לקודד מוסכמות פורמט ישראליות, לא לחקות ברירות מחדל אמריקאיות או אירופיות.

**מטבע: סימן השקל (₪)**

הסימן `₪` (U+20AA) בד"כ מופיע *אחרי* הסכום בהקשרים פיננסיים ישראליים (למשל `1,234.50 ₪`), אבל גם `₪ 1,234.50` נפוץ בקמעונאות. לא משנה באיזה קונבנציה בוחרים, יש ליישם אותה באופן עקבי. מכיוון שמספרים הם LTR מטבעם, סכום בתוך טקסט עברי RTL דורש בידוד דו-כיווני (bidi isolation) מפורש, אחרת סימני פיסוק מסביב עלולים להתערבב.

```html
<!-- נכון: בידוד הסכום כדי שסימן המטבע יישאר במקום -->
<p>המחיר הוא <bdi>1,234.50 ₪</bdi> בלבד.</p>
```

```js
// עדיף Intl.NumberFormat על פני פורמט ידני — הוא מטפל במיקום הסימן,
// במפרידי אלפים, ובסימני RTL בלתי נראים באופן עקבי בין דפדפנים.
new Intl.NumberFormat('he-IL', {
  style: 'currency',
  currency: 'ILS',
}).format(1234.5);
// => "‏1,234.50 ₪"
```

**מספרים בתוך טקסט עברי**

מספרים (מספרי טלפון, ת"ז, מחירים, תאריכים) לא מתהפכים ב-RTL. אבל כשמספר ארוך יושב בתוך טקסט עברי, הדפדפן עלול לסדר מחדש את הפיסוק מסביב. יש להשתמש ב-`<bdi>` או ב-`dir="ltr"` על רכיב המספר כדי לנעול אותו.

```html
<p>מספר הזהות הוא <bdi>012345678</bdi>, בתוקף עד 2030.</p>
```

**תאריכים ושעה**

ברירת המחדל היא הקונבנציה הישראלית: `DD/MM/YYYY` (למשל `20/04/2026`), לא `MM/DD/YYYY` אמריקאי או `YYYY-MM-DD` של ISO בטקסט לממשק משתמש. שימוש בשעון 24 שעות (`14:30`) — AM/PM כמעט ולא בשימוש בממשקים ישראליים.

```js
new Intl.DateTimeFormat('he-IL', {
  day: '2-digit', month: '2-digit', year: 'numeric',
}).format(new Date());
// => "20.4.2026" או "20/04/2026" תלוי בנתוני locale של הדפדפן
```

להגדיר תגי עיצוב כדי שרכיבים במורד הזרם יישארו עקביים:

```css
:root {
  --date-format-short: 'dd/MM/yyyy';
  --time-format: 'HH:mm';
  --currency-locale: 'he-IL';
  --currency-code: 'ILS';
}
```

**מפרידי מספרים**

מפריד אלפים הוא פסיק (`1,234,567`), נקודה עשרונית היא נקודה (`1,234.50`). לא לעבור לסגנון האירופי `1.234,50` — הפיננסים בישראל משתמשים בקונבנציה האמריקאית.

## דוגמאות

### דוגמה 1: הקמת מערכת עיצוב ישראלית
המשתמש אומר: "צור מערכת עיצוב למוצר ה-SaaS הישראלי שלי"
תוצאה: מגדירים זיווג גופנים Heebo + Inter, מקימים סולם טיפוגרפי מותאם לעברית עם מינימום 16px לגוף טקסט וגובה שורה 1.7, מגדירים רכיבי בסיס RTL-first (כפתור, כרטיס, קלט, פריסת סרגל צד) עם תכונות CSS לוגיות, וקובעים תגי צבע מותאמים לישראל.

### דוגמה 2: בניית רכיב טופס בעברית
המשתמש אומר: "אני צריך טופס כתובת עברי עם פריסת RTL תקינה"
תוצאה: יוצרים טופס RTL עם תוויות בעברית, קבוצות שדות מיושרות לימין, כיוון קלט LTR לשדות מספריים (מספר בית, מיקוד, טלפון), קיבוץ fieldset תקין עם אגדות בעברית, ותבניות שדה ייחודיות לישראל (מיקוד 7 ספרות, בורר יישוב).

### דוגמה 3: יישום תבניות עיצוב gov.il
המשתמש אומר: "האתר הממשלתי שלי צריך להתאים לתקני העיצוב של gov.il"
תוצאה: מפעילים תבנית כותרת gov.il עם כחול מוסדי, ניווט בעברית עם זרימת RTL, מחווני שלבים לטפסים רב-דפיים, עיצוב טפסים נגיש עם מחוון פוקוס, ותחתית דף עם הקישורים הממשלתיים הנדרשים.

## משאבים מצורפים

### קובצי עזר
- `references/hebrew-typography.md` -- קטלוג גופנים עבריים עם מדדי Google Fonts, זיווגים מומלצים למקרי שימוש שונים (SaaS, עריכה, ממשלה), אסטרטגיות ביצועים של טעינת גופנים, תכונות CSS ייחודיות לעברית (גובה שורה, ריווח מילים, כללי ריווח אותיות), והמלצות לסולם גדלים לממשקים דו-לשוניים עברית/אנגלית.

## מלכודות נפוצות
- טקסט עברי קצר בד"כ ב-15-30% מהמקביל האנגלי. סוכנים עלולים לעצב layouts עם רוחב קבוע על בסיס אורך הטקסט באנגלית, וזה גורם לרווח לבן מיותר בעברית או לשבירת layout במעבר לאנגלית.
- סדר גופנים עבריים סטנדרטי לאתרים צריך לתת עדיפות לגופני מערכת: Segoe UI, Rubik, Heebo, Arial, sans-serif. סוכנים עלולים להשתמש בגופנים עבריים מ-Google Fonts בלי לכלול גופן חלופי, וזה גורם ל-FOUT בחיבורים איטיים.
- תוויות טפסים בעברית צריכות להיות מיושרות לימין וממוקמות מימין לשדות (או מעליהם). סוכנים לפעמים ממקמים תוויות משמאל לשדות, וזה מוסכמה אנגלית שמרגישה לא טבעית ב-RTL.
- סימן השקל (₪) הוא לא תו כיווני, ולכן מחיר inline כמו `1,234.50 ₪` בתוך פסקה בעברית עלול לזוז באופן לא צפוי בין דפדפנים. סוכנים בד"כ סומכים על אלגוריתם ה-bidi של הדפדפן ומדלגים על `<bdi>` או על `Intl.NumberFormat('he-IL', { style: 'currency' })`, וזה גורם לתצוגה לא עקבית של מחירים בין Chrome ל-Safari.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| Google Fonts – עברית | https://fonts.google.com/?subset=hebrew | Heebo, Assistant, Rubik, Frank Ruhl Libre, קטעי טעינה |
| תכונות CSS לוגיות (MDN) | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values | padding-inline, margin-block, מיקום לוגי |
| תמיכת RTL ב-Tailwind | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | וריאנטי `rtl:` ו-`ltr:` לספריות רכיבים |
| shadcn/ui | https://ui.shadcn.com | רכיבים תואמי RTL ופרימיטיבים |
| WCAG 2.1 Quick Reference | https://www.w3.org/WAI/WCAG21/quickref/ | דרישות ניגודיות וסדר קריאה שחלים על RTL |

## פתרון בעיות

### שגיאה: "הטקסט בעברית נראה צפוף או קטן מדי"
סיבה: משתמשים בגדלי גופן וגובהי שורה מותאמים ללטינית בעברית
פתרון: להגדיל את גודל הגופן הבסיסי ל-16px לפחות לגוף טקסט. לקבוע גובה שורה של 1.7 מינימום לעברית. אף פעם לא להוסיף ריווח אותיות לטקסט עברי. להוסיף ריווח מילים קל (0.05em) לשיפור הקריאות.

### שגיאה: "פריסת הרכיב נשברת ב-RTL"
סיבה: משתמשים בתכונות CSS פיזיות (margin-left, padding-right) במקום בתכונות לוגיות
פתרון: להחליף את כל התכונות הכיווניות הפיזיות במקבילות לוגיות: margin-inline-start, padding-inline-end, border-inline-start, inset-inline-start. להשתמש ב-flexbox וב-grid שמכבדים אוטומטית את תכונת dir.

### שגיאה: "אייקונים מצביעים לכיוון שגוי ב-RTL"
סיבה: אייקונים כיווניים (חצים, שברונים, כפתורי חזרה) לא משוקפים ל-RTL
פתרון: לשקף אייקונים כיווניים עם CSS `transform: scaleX(-1)` בהקשר של `[dir="rtl"]`. אייקונים לא-כיווניים (חיפוש, בית, הגדרות) לא צריכים להיות משוקפים. ליצור מחלקת שירות לשיקוף אייקונים ליישום עקבי.
