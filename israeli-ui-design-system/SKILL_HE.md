# מערכת עיצוב ישראלית

## הנחיות

### שלב 1: בחירת זיווגי גופנים עבריים

בחירת שילובי גופנים מותאמים לקריאות עברית ותאימות לטינית:

| זיווג | גופן עברי | גופן לטיני | מתאים ל- | סגנון |
|-------|-----------|------------|----------|-------|
| עסקי מודרני | Heebo | Inter | SaaS, לוחות בקרה, ממשקי ניהול | נקי, ניטרלי |
| סטארטאפ ידידותי | Rubik | Source Sans Pro | אפליקציות צרכניות, אתרי שיווק | מעוגל, נגיש |
| ממשלתי/רשמי | Assistant | Roboto | אתרים ממשלתיים, דפים מוסדיים | מקצועי, בהיר |
| עריכה | Frank Ruhl Libre | Merriweather | בלוגים, חדשות, אתרי תוכן | סריף, ספרותי |
| מינימלי | Secular One | Montserrat | דפי נחיתה, תיקי עבודות | כותרות בולטות |

ראו `references/hebrew-typography.md` למדדי גופנים מלאים ואסטרטגיות טעינה.

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

### שלב 2: סולם טיפוגרפי עברי

תווים עבריים נראים גדולים יותר חזותית מלטיניים באותו גודל גופן. יש להתאים את סולם הגדלים:

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

  /* גובהי שורה ייחודיים לעברית (גבוהים יותר מלטינית) */
  --leading-tight: 1.4;
  --leading-normal: 1.7;
  --leading-relaxed: 1.9;

  /* לעולם לא להשתמש ב-letter-spacing לעברית */
  --tracking-hebrew: normal;
  /* ריווח מילים קל משפר קריאות עברית */
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

עיצוב רכיבים עם RTL כברירת מחדל, לא כמחשבה שנייה:

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
  /* אייקון מתהפך אוטומטית ב-RTL */
}

.btn-icon-start {
  flex-direction: row;
  /* ב-RTL: אייקון מופיע מימין (צד ההתחלה) */
}

.btn-icon-end {
  flex-direction: row-reverse;
  /* ב-RTL: אייקון מופיע משמאל (צד הסיום) */
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
  /* ב-RTL: סרגל הצד מופיע מימין אוטומטית */
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

לאתרים ממשלתיים ומוסדיים ישראליים, יש לעקוב אחר מערכת העיצוב של gov.il:

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
  /* ב-RTL: שלבים זורמים מימין לשמאל */
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

## דוגמאות

### דוגמה 1: הקמת מערכת עיצוב ישראלית
המשתמש אומר: "צור מערכת עיצוב למוצר ה-SaaS הישראלי שלי"
תוצאה: הגדרת זיווג גופנים Heebo + Inter, הקמת סולם טיפוגרפי מותאם לעברית עם מינימום 16px לגוף טקסט וגובה שורה 1.7, הגדרת רכיבי בסיס RTL-first (כפתור, כרטיס, קלט, פריסת סרגל צד) באמצעות תכונות CSS לוגיות, וקביעת תגי צבע מותאמים לישראל.

### דוגמה 2: בניית רכיב טופס בעברית
המשתמש אומר: "אני צריך טופס כתובת עברי עם פריסת RTL תקינה"
תוצאה: יצירת טופס RTL עם תוויות בעברית, קבוצות שדות מיושרות לימין, כיוון קלט LTR לשדות מספריים (מספר בית, מיקוד, טלפון), קיבוץ fieldset תקין עם אגדות בעברית, ותבניות שדה ייחודיות לישראל (מיקוד 7 ספרות, בורר יישוב).

### דוגמה 3: מימוש תבניות עיצוב gov.il
המשתמש אומר: "האתר הממשלתי שלי צריך להתאים לתקני העיצוב של gov.il"
תוצאה: החלת תבנית כותרת gov.il עם כחול מוסדי, ניווט עברי עם זרימת RTL, מחווני שלבים לטפסים רב-דפיים, עיצוב טפסים נגיש עם מחוונ פוקוס, ותחתית דף עם קישורים ממשלתיים נדרשים.

## משאבים מצורפים

### קובצי עזר
- `references/hebrew-typography.md` -- קטלוג גופנים עבריים עם מדדי Google Fonts, זיווגים מומלצים למקרי שימוש שונים (SaaS, עריכה, ממשלה), אסטרטגיות ביצועי טעינת גופנים, תכונות CSS ייחודיות לעברית (גובה שורה, ריווח מילים, כללי ריווח אותיות), והמלצות לסולם גדלים לממשקים דו-לשוניים עברית/אנגלית.

## מלכודות נפוצות
- טקסט עברי קצר ב-15-30% בדרך כלל מהמקביל האנגלי. סוכנים עלולים לעצב layouts עם רוחב קבוע בהתבסס על אורך טקסט אנגלי, מה שגורם לרווח לבן מיותר בעברית או לשבירת layout במעבר לאנגלית.
- סדר גופנים עבריים סטנדרטי לאתרים צריך לתעדף גופני מערכת: Segoe UI, Rubik, Heebo, Arial, sans-serif. סוכנים עלולים להשתמש בגופנים עבריים מ-Google Fonts בלי לכלול גופן חלופי, מה שגורם ל-FOUT בחיבורים איטיים.
- תוויות טפסים בעברית צריכות להיות מיושרות לימין וממוקמות מימין לשדות (או מעליהם). סוכנים ממקמים לעתים תוויות משמאל לשדות, מה שזו מוסכמה אנגלית שמרגישה לא טבעית ב-RTL.
- שדות קלט מספר טלפון למספרים ישראליים צריכים לקבל פורמטים עם ובלי קידומת מדינה: 054-1234567, 972-54-1234567+, ו-0541234567. סוכנים עלולים לאמת רק את הפורמט הבינלאומי.

## פתרון בעיות

### שגיאה: "טקסט עברי נראה צפוף או קטן מדי"
סיבה: שימוש בגדלי גופן וגובהי שורה מותאמים ללטינית עבור עברית
פתרון: הגדלת גודל גופן בסיסי ל-16px לפחות לגוף טקסט. הגדרת גובה שורה ל-1.7 מינימום לעברית. לעולם לא להוסיף ריווח אותיות לטקסט עברי. הוספת ריווח מילים קל (0.05em) לשיפור קריאות.

### שגיאה: "פריסת רכיב נשברת ב-RTL"
סיבה: שימוש בתכונות CSS פיזיות (margin-left, padding-right) במקום תכונות לוגיות
פתרון: החלפת כל התכונות הכיווניות הפיזיות במקבילות לוגיות: margin-inline-start, padding-inline-end, border-inline-start, inset-inline-start. שימוש ב-flexbox ו-grid שמכבדים אוטומטית את תכונת dir.

### שגיאה: "אייקונים מצביעים לכיוון שגוי ב-RTL"
סיבה: אייקונים כיווניים (חצים, שברונים, כפתורי חזרה) לא משוקפים ל-RTL
פתרון: שיקוף אייקונים כיווניים באמצעות CSS `transform: scaleX(-1)` בהקשר `[dir="rtl"]`. אייקונים לא-כיווניים (חיפוש, בית, הגדרות) לא צריכים להיות משוקפים. יצירת מחלקת שירות לשיקוף אייקונים ליישום עקבי.
