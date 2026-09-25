# מערכת עיצוב ישראלית

עובד עם React, Vue, Angular ו-HTML/CSS רגיל. לא דורש רשת לתבניות הליבה. מומלץ עם Storybook לפיתוח רכיבים.

## הנחיות

### שלב 1: בחירת זיווגי גופנים עבריים

תבחרו שילובי גופנים שמותאמים לקריאות בעברית ולתאימות לטינית:

| זיווג | גופן עברי | גופן לטיני | מתאים ל- | סגנון |
|-------|-----------|------------|----------|-------|
| עסקי מודרני | Heebo | Inter | SaaS, לוחות בקרה, ממשקי ניהול | נקי, ניטרלי |
| סטארטאפ ידידותי | Rubik | Source Sans 3 | אפליקציות צרכניות, אתרי שיווק | מעוגל, נגיש |
| ממשלתי/רשמי | Assistant | Roboto | אתרים ממשלתיים, דפים מוסדיים | מקצועי, בהיר |
| עריכה | Frank Ruhl Libre | Merriweather | בלוגים, חדשות, אתרי תוכן | סריף, ספרותי |
| מינימלי | Secular One | Montserrat | דפי נחיתה, תיקי עבודות | כותרות בולטות |

תסתכלו על `references/hebrew-typography.md` למדדי גופנים מלאים ולאסטרטגיות טעינה.

**תצורת טעינת גופנים:**
```css
/* ראשי: זיווג Heebo + Inter */
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&family=Inter:wght@300;400;500;700&display=swap');

:root {
  /* הגופן הלטיני ראשון: ב-Inter אין אותיות עבריות, ולכן כל אות עברית
     נופלת ל-Heebo. ב-Heebo יש גם אותיות לטיניות, אז אם הוא ראשון
     האנגלית תוצג ב-Heebo ו-Inter לעולם לא ייטען. */
  --font-sans: 'Inter', 'Heebo', 'Noto Sans Hebrew', Arial, sans-serif;
  --font-mono: 'Fira Code', 'Source Code Pro', monospace;
}

body {
  font-family: var(--font-sans);
}
```

משפחה גנרית (`sans-serif`) תמיד נמצאת, ולכן שום גופן שמופיע אחריה לא ישמש: שימו אותה אחרונה, פעם אחת, אחרי גופן מערכת עם אותיות עבריות (כאן Arial) כדי שהטקסט יישאר קריא בזמן שגופני הרשת נטענים. אם אתם רוצים את האותיות הלטיניות של Heebo עצמו ולא זיווג, כתבו רק את Heebo. לגופני ה-monospace כאן אין עברית, ולכן עברית בתוך קוד נופלת לגופן המערכת.

**ב-Next.js (`next/font`).** פרטו את תתי-הקבוצות לטעינה מראש, כולל `hebrew`; ל-`next/font` אין תת-קבוצה ברירת מחדל, והשמטת `subsets` כש-`preload` פעיל רק מפיקה אזהרה:

```tsx
import { Heebo, Inter } from 'next/font/google';
const heebo = Heebo({ subsets: ['hebrew', 'latin'], variable: '--font-heebo', display: 'swap' });
const inter = Inter({ subsets: ['latin'], variable: '--font-inter', display: 'swap' });
// <html lang="he" dir="rtl" className={`${inter.variable} ${heebo.variable}`}>
```

עם Tailwind v4, מחברים אותם ב-CSS עם `@theme inline { --font-sans: var(--font-inter), var(--font-heebo), sans-serif; }` (האפשרות `inline` נדרשת כשמשתנה תמה מפנה למשתנה אחר).

### שלב 2: סולם טיפוגרפי לעברית

אותיות עבריות מצוירות בין גובה ה-x לגובה האותיות הגדולות הלטיניות, בלי אותיות גדולות ובלי עולים גבוהים, ולכן עברית נקראת **קטנה יותר** מלטינית באותו גודל גופן. בנו את הסולם לפי העברית, לא לפי הלטינית (הגבהים שנמדדו לכל גופן נמצאים ב-`references/hebrew-typography.md`):

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

/* גוף טקסט עברי: dir יושב בדרך כלל על <html>, ולכן מתאימים לשני האלמנטים */
html[dir="rtl"] body,
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
  font-family: var(--font-sans);
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

**התנהגות RTL לשאר ערכת הרכיבים.** כפתורים, כרטיסים וסרגל הצד הם לא כל הסיפור - תשקפו כל רכיב כיווני:

| רכיב | התנהגות ב-RTL |
|------|----------------|
| פירורי לחם (breadcrumbs) | זורמים מימין לשמאל; המפריד (`/`, `>`, שברון) מצביע שמאלה (לכיוון הפירור הבא). מפריד טקסטואלי (`>`, `›`) הוא תו שהדפדפן כבר משקף ב-RTL, אז אל תוסיפו לו `scaleX(-1)` (זה הופך אותו בחזרה). רק שברון ב-SVG או בגופן אייקונים צריך `transform: scaleX(-1)`, ו-transform לא משפיע על אלמנט inline, אז תנו לתו של גופן האייקונים `display: inline-block`. |
| מודאלים / דיאלוגים | מודאל ממורכז לא דורש שינוי. כפתור הסגירה (X) יושב ב-inline-end (שמאל למעלה ב-RTL). כפתורי הפעולה בכותרת התחתונה: מוסכמה ביתית נפוצה שמה את הראשי ב-inline-start, כך שהוא נוחת מימין ב-RTL; בחרו סדר אחד והקפידו עליו. |
| תפריטים נפתחים | נפתחים מיושרים לקצה ה-inline-start של הטריגר; תפריטי משנה נפרשים לכיוון ה-inline-start (לשמאל ב-RTL). חץ/שברון מתהפך. |
| סליידרים / קלט טווח | המסילה מתמלאת מ-inline-start - ב-RTL המינימום מימין והמקסימום משמאל. `<input type="range">` עם `dir="rtl"` מטפל בזה; סליידרים מותאמים חייבים להפוך את כיוון המילוי. |
| פסי התקדמות | המילוי גדל מ-inline-start, כך שההתקדמות מתקדמת מימין לשמאל ב-RTL. תשתמשו ב-`transform-origin` / תכונות לוגיות, לא במקור `left: 0` קשיח. |
| הודעות צפות (toasts) | מחליקות פנימה מקצה ה-inline-end של החלון - שמאל למעלה או שמאל למטה ב-RTL (משוקף מהמוסכמה ימין-למעלה של LTR). תעגנו עם `inset-inline-end`, לא `right`. |

```css
/* toast מעוגן לקצה ה-inline-end -- מתהפך צד אוטומטית ב-RTL */
.toast {
  position: fixed;
  inset-block-start: 1rem;
  inset-inline-end: 1rem;
}

/* מילוי פס התקדמות גדל מ-inline-start */
.progress-fill {
  block-size: 100%;
  inline-size: var(--progress, 0%);
  /* המילוי מתחיל בקצה ה-inline-start: ימין ב-RTL, שמאל ב-LTR */
}
```

**ב-Tailwind v4.** השתמשו בכלים הלוגיים כדי שאותה רשימת מחלקות תעבוד בשני הכיוונים: `ps-*`/`pe-*` ו-`ms-*`/`me-*` (ריפוד ושוליים בציר השורה), `border-s`/`border-e`, `rounded-s-*`/`rounded-e-*`, `text-start`/`text-end`, ומגרסה 4.2.0 גם `inset-s-*`/`inset-e-*` ואת כלי ציר הבלוק `pbs-*`/`pbe-*`/`mbs-*`/`mbe-*`. גרסה 4.2.0 הוציאה משימוש את `start-*`/`end-*` לטובת `inset-s-*`/`inset-e-*`. השאירו את הווריאנטים `rtl:`/`ltr:` לחריגים אמיתיים, כמו היפוך אייקון כיווני (`rtl:-scale-x-100`), ולא לריווח.

**ב-shadcn/ui.** ההגדרה `rtl: true` בקובץ `components.json` גורמת ל-CLI להמיר `left-*`/`right-*` למחלקות לוגיות ולהפוך אייקונים נתמכים עם `rtl:rotate-180`, אבל רק בפרויקטים שנוצרו עם `shadcn create` בסגנונות החדשים (`base-nova`, `radix-nova`); פרויקטים אחרים עוברים לפי מדריך ההגירה שלו. הוסיפו את `DirectionProvider` שלו (`shadcn add direction`). התיעוד שלו גם מורה בינתיים להעביר `dir` לאלמנטים בפורטל, כמו התוכן של popover ו-tooltip, כמעקף לבעיה ידועה ב-tw-animate-css עם כלי ההחלקה הלוגיים.

**אילו אייקונים מתהפכים.** הפכו אייקונים שמראים כיוון לאורך שורת הקריאה, והשאירו את השאר:

| להפוך ב-RTL | לא להפוך |
|---------------|---------------|
| חיצי אחורה/קדימה, חצים בפירורי לחם ובמדדי שלבים, "הבא" ו"שליחה" | כפתורי ניגון, השהיה ודילוג במדיה (הם עוקבים אחרי כיוון הסרט) |
| השב, הזחת רשימה, אייקוני יישור טקסט | שעונים, רענון והיסטוריה (הזמן נע בכיוון השעון בכל מקום) |
| מילוי פסי התקדמות ומחוונים, צירי זמן לינאריים | סימן וי, חיפוש, מצלמה ושאר חפצים בלי כיוון |
| אייקונים של חפץ שנע קדימה | תרשימים וגרפים, מספרים, לוגואים, קווים נטויים |

בטל ובצע שוב רומזים גם לכיוון אופקי וגם לכיוון מעגלי: ב-RTL בחרו אחד והחילו אותו בעקביות. קבעו כל החלטה פעם אחת (למשל תכונת `data-mirror` או דגל ברישום האייקונים) ולא בכל שימוש מחדש.

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

**מצב כהה (שכבת טוקנים `colors-dark`).** תגדירו ערכת טוקנים כהה מקבילה במקום לקודד ערכים כהים קשיח לתוך הרכיבים. תשמרו על אותם שמות טוקנים כך שרכיבים מפנים ל-`var(--color-bg)` / `var(--color-text)` ולעולם לא מסתעפים לפי ערכת הנושא. הכיוון מאונך לערכת הנושא - RTL ומצב כהה הם צירים בלתי תלויים, כך שצירוף `[data-theme="dark"][dir="rtl"]` פשוט חייב לעבוד.

```css
:root {
  /* בהיר (ברירת מחדל) */
  --color-bg: #ffffff;
  --color-surface: #f9fafb;
  --color-text: #111827;
  --color-border: #e5e7eb;
}

:root[data-theme="dark"] {
  /* שכבת colors-dark -- אותם שמות טוקנים, ערכים כהים */
  --color-bg: #0b0f19;
  --color-surface: #151b2b;
  --color-text: #e5e7eb;
  --color-border: #2a3346;
}
```

הערה: טקסט עברי על רקע כהה עלול להיראות דק יותר בגלל צורות האותיות העבריות - תוודאו שהניגודיות עדיין עומדת ב-WCAG AA ושקלו משקל גופן מעט כבד יותר לטקסט גוף במצב כהה.

**הטמיעו ניגודיות לתוך הטוקנים.** שכבת הטוקנים של מערכת עיצוב צריכה להבטיח ניגודיות WCAG, לא להשאיר את זה למחברי הרכיבים. זווגו כל טוקן טקסט מול המשטח שלו ובדקו את היחס: טקסט גוף על `--color-bg` / `--color-surface` חייב להיות לפחות 4.5:1, וטקסט גדול, אייקונים וגבולות ממשק לפחות 3:1. בדקו במיוחד את טוקני הסטטוס: `--color-warning: #d97706` הוא 3.19:1 על לבן (3.05:1 על `--color-surface`), ו-`--color-primary-500: #3b82f6` הוא 3.68:1. זה עובר את רף 3:1 לטקסט גדול, אייקונים וגבולות ממשק (אז הם תקינים כקו פוקוס או כמילוי), אבל נכשל ברף 4.5:1 לטקסט גוף בגודל רגיל. אל תשימו טקסט קטן בצבעים האלה על רקע בהיר; הוסיפו גוון כהה יותר (רמת 600/700) כשצריך את הצבע כטקסט.

**העדיפו oklch לרמפות.** הגדירו רמפות צבע ב-`oklch()` (Baseline מאז 2023) עם נפילה ל-hex. בהירות אחידה-תפיסתית מקלה מאוד על יצירת רמפות נגישות ווריאנטים למצב כהה לעומת כוונון hex ידני.

**חלקו את הטוקנים לשכבות.** רכיבים לא צריכים להפנות לשלב גולמי בפלטה כמו `--color-primary-500`. השתמשו בשלוש שכבות: פרימיטיבים (`blue.600`), תפקידים סמנטיים שמפנים אליהם (`color.action.primary`), וטוקני רכיב שמפנים לתפקידים (`button.bg`). מיתוג מחדש או הוספת ערכת כהה משנים אז שכבה אחת.

**כתבו טוקנים פעם אחת**, בפורמט של קבוצת הקהילה של W3C לטוקני עיצוב (DTCG), שמודול הפורמט שלה בגרסה 2025.10 הוא דוח סופי של קבוצת קהילה (28 באוקטובר 2025). הפניות נכתבות כ-`{group.token}`, וערך צבע בגרסה 2025.10 הוא אובייקט:

```json
{
  "color": {
    "blue": { "600": { "$type": "color", "$value": { "colorSpace": "srgb", "components": [0.145, 0.388, 0.922], "hex": "#2563eb" } } },
    "action": { "primary": { "$type": "color", "$value": "{color.blue.600}" } }
  },
  "button": { "bg": { "$type": "color", "$value": "{color.action.primary}" } }
}
```

ל-Style Dictionary יש תמיכה ב-DTCG מגרסה 4, אבל התיעוד שלו אומר שגרסה 2025.10 עוד לא נתמכת במלואה (עבודה בתהליך בגרסה 5), אז בדקו את הגרסה שלכם לפני שמאמצים את תחביר הצבע כאובייקט. הפורמט `css/variables` שלו עם `outputReferences: true` שומר את שרשרת ההפניות ב-CSS שנוצר (`--button-bg: var(--color-action-primary)`), כך שהשכבות נשמרות גם בקוד.

**אורך שורה.** הוסיפו טוקן מידה והחילו אותו עם `max-inline-size`, למשל `--measure-prose: 65ch`. היחידה `ch` היא רוחב הספרה הלטינית "0", אז בדקו בדפדפן את אורך השורה העברית בפועל ואל תסמכו על המספר.

### שלב 5: תבניות עיצוב gov.il

לאתרים ממשלתיים ומוסדיים ישראליים, האסמכתא המוסמכת היא **מערכת העיצוב הממשלתית הישראלית (IGDS)** - מערכת העיצוב האטומי הרשמית שמשמשת לאיחוד חוויית המשתמש בכל אתרי gov.il. היא מתפרסמת כקובץ Figma Community ברישיון CC BY 4.0. הגרסה הנוכחית היא "Israeli Government DS 3.0" (https://www.figma.com/community/file/1637743894870099523/israeli-government-ds-3-0, כתובת התמיכה בדומיין digital.gov.il); הגרסה הקודמת "IGDS Design System File 2.0" (https://www.figma.com/community/file/1426262348206342909/igds-design-system-file-2-0) עדיין מופיעה, אז בדקו על איזו מהן פרויקט נבנה. אם אתם בונים מוצר אמיתי בזיקה ל-gov.il, תמשכו טוקנים, רכיבים ואת סגנון האיור העברי ב-RTL ישירות מקובץ ה-IGDS ב-Figma במקום לקרב אותם - IGDS מגדירה ערכות צבע, ריווח ואנטומיית רכיבים משלה, וקירובים יסטו באופן גלוי מדפי gov.il החיים.

ה-CSS למטה הוא **תבנית מוסדית גנרית, לא ה-IGDS הרשמי**. תשתמשו בו כפיגום התחלתי למראה מוסדי כשאין לכם גישה ל-IGDS; תחליפו את הערכים בטוקנים של IGDS ברגע שתהיה לכם גישה.

```css
/* תבנית כותרת מוסדית גנרית (לא טוקני IGDS רשמיים) */
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
  font-family: var(--font-sans);
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

**שדות זיהוי ויצירת קשר ישראליים.** שלושה סוגי קלט שמערכות עיצוב שנבנו קודם
כול ללטינית מפספסות:

```html
<!-- תעודת זהות: עד 9 ספרות, ואפס מוביל משמעותי.
     type="number" בולע אותו בשקט ומוסיף חיצי הגדלה. תמיד text יחד עם inputmode,
     ומאמתים בסקריפט אחרי ניקוי (isValidTz למטה), לא עם pattern. -->
<input id="tz" type="text" dir="ltr" inputmode="numeric"
       maxlength="9" autocomplete="off">

<!-- נייד ישראלי: 05X ועוד 7 ספרות, כולל הצורה עם מקף והצורה עם 972+
     שמשתמשים באמת מקלידים. נשאר LTR בתוך טופס RTL. מנרמלים בשליחה. -->
<input id="phone" type="tel" dir="ltr" inputmode="tel"
       autocomplete="tel">
<!-- מאמתים אחרי הסרת רווחים ומקפים (משתמשים מדביקים "054 123 4567"):
     /^(0|\+?972-?0?)5\d{8}$/ על הערך המנורמל, לא בתכונת pattern. -->

<!-- דוא"ל, כתובת אתר ו-IBAN הם תוכן לטיני: תכפו LTR כדי שהסמן והפיסוק
     יתנהגו כמו שצריך, גם כשהטופס מסביב הוא RTL. -->
<input id="email" type="email" dir="ltr" autocomplete="email">
```

הספרה התשיעית בתעודת זהות היא ספרת ביקורת, ומספרים קצרים יותר מושלמים בתשע ספרות עם אפסים משמאל. קודם משלימים, אחר כך מאמתים:

```js
function isValidTz(raw) {
  const digits = String(raw ?? '').trim();
  if (!/^\d{1,9}$/.test(digits) || /^0+$/.test(digits)) return false; // no empty, all-zero or non-digit input
  const id = digits.padStart(9, '0');
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    const n = Number(id[i]) * ((i % 2) + 1); // משקלות 1,2,1,2,...
    sum += n > 9 ? n - 9 : n;                // מחברים את ספרות המכפלה הדו-ספרתית
  }
  return sum % 10 === 0;
}
isValidTz('50012343'); // => true (מושלם ל-050012343)
```

**לשון מגדרית בממשק (נוהג).** פעלים ותארים בעברית נושאים מגדר, ולכן ציווי בלשון זכר בלבד ("לחץ", "הירשם") פונה לא נכון לחצי מהמשתמשים. סגנונות ביתיים נפוצים משתמשים בציווי ברבים ("לחצו", "הירשמו") או בשם פועל ("ללחוץ כאן"), או עוברים לשם עצם ("הרשמה"). בחרו סגנון אחד ורשמו אותו בהנחיות התוכן לצד הטוקנים.

**תוכן משתמש בכיוון מעורב.** כל מה שמשתמש הקליד, וכל מה שמגיע מ-API, עלול להיות
בעברית או בלטינית. אסור לקבע לו כיוון: `dir="auto"` נותן לתו החזק הראשון להכריע,
לכל רכיב בנפרד.

```html
<textarea dir="auto"></textarea>
<li dir="auto">{{ comment.body }}</li>
```

יש להגדיר `dir="auto"` על כל פריט בנפרד, אף פעם לא פעם אחת על העוטף של הרשימה:
עוטף יחיד מקבל את הכיוון של הפריט הראשון ומסיט את כל השאר.

### שלב 7: מוסכמות פורמט ישראליות (מטבע, מספרים, תאריכים)

תגי עיצוב ורכיבים צריכים לקודד מוסכמות פורמט ישראליות, לא לחקות ברירות מחדל אמריקאיות או אירופיות.

**מטבע: סימן השקל (₪)**

הסימן `₪` (U+20AA) בד"כ מופיע *אחרי* הסכום בהקשרים פיננסיים ישראליים (למשל `1,234.50 ₪`), אבל גם `₪ 1,234.50` נפוץ בקמעונאות. לא משנה באיזה קונבנציה בוחרים, יש ליישם אותה באופן עקבי. מכיוון שמספרים הם LTR מטבעם, סכום בתוך טקסט עברי RTL דורש בידוד דו-כיווני (bidi isolation) מפורש, אחרת סימני פיסוק מסביב עלולים להתערבב.

```html
<!-- נכון: בידוד הסכום כדי שסימן המטבע יישאר במקום -->
<p>המחיר הוא <bdi>1,234.50 ₪</bdi> בלבד.</p>
```

```js
// עדיף Intl.NumberFormat על פני פורמט ידני - הוא מטפל במיקום הסימן,
// במפרידי אלפים, ובסימני RTL בלתי נראים באופן עקבי בין דפדפנים.
new Intl.NumberFormat('he-IL', {
  style: 'currency',
  currency: 'ILS',
}).format(1234.5);
// => "‏1,234.50 ‏₪"  (נראה על המסך כ-"1,234.50 ₪")
```

המחרוזת שחוזרת אינה `"1,234.50 ₪"` הנקייה שהיא נראית. יש בה שני סימני RTL
בלתי נראים (U+200F) ורווח קשיח, וזה בדיוק מה שמונע מסימן השקל לזוז בטקסט
דו-כיווני. אף פעם לא להשוות אותה למחרוזת שנכתבה ביד בבדיקת snapshot או בבדיקת
יחידה: משווים פלט של `Intl` לפלט של `Intl`, או מסירים `‏ ` קודם.

**מספרים בתוך טקסט עברי**

מספרים (מספרי טלפון, ת"ז, מחירים, תאריכים) לא מתהפכים ב-RTL. אבל כשמספר ארוך יושב בתוך טקסט עברי, הדפדפן עלול לסדר מחדש את הפיסוק מסביב. יש להשתמש ב-`<bdi>` או ב-`dir="ltr"` על רכיב המספר כדי לנעול אותו.

```html
<p>מספר הזהות הוא <bdi>012345678</bdi>, בתוקף עד 2030.</p>
```

**תאריכים ושעה**

תאריכים בישראל נכתבים כשהיום ראשון, אף פעם לא `MM/DD/YYYY` אמריקאי ואף פעם לא בתבנית ISO `YYYY-MM-DD` בטקסט לממשק משתמש. שימוש בשעון 24 שעות (`14:30`) - AM/PM כמעט ולא בשימוש בממשקים ישראליים.

**המפריד בפלטפורמה הוא נקודה, לא לוכסן.** בתקן CLDR התבנית הקצרה של העברית היא `d.M.y`, ולכן `Intl` מחזיר נקודות ואין הגדרת דפדפן שתהפוך אותן ללוכסנים:

```js
new Intl.DateTimeFormat('he-IL', {
  day: '2-digit', month: '2-digit', year: 'numeric',
}).format(new Date(2026, 3, 20));
// => "20.04.2026"   (עם dateStyle: 'short' מתקבל "20.4.2026")
```

נקודות הן ברירת המחדל הבטוחה: זה מה שמשתמש ישראלי מצפה לראות וזה מה שכל אפליקציה
אחרת בעברית מציגה. אם הנחיות המותג דורשות `20/04/2026`, יש להרכיב את המחרוזת
ידנית במקום לצפות ש-`Intl` יפיק אותה:

```js
const parts = Object.fromEntries(
  new Intl.DateTimeFormat('he-IL', { day: '2-digit', month: '2-digit', year: 'numeric' })
    .formatToParts(new Date(2026, 3, 20))
    .map((p) => [p.type, p.value]),
);
`${parts.day}/${parts.month}/${parts.year}`; // => "20/04/2026"
```

**לוחות שנה.** עבור `he-IL`, הביטוי `locale.getWeekInfo?.() ?? locale.weekInfo` (עם `const locale = new Intl.Locale('he-IL')`; בחלק מסביבות הריצה, כולל Node 20 ו-22, יש רק את המאפיין הישן `weekInfo`) מחזיר `firstDay: 7` (ראשון) ו-`weekend: [5, 6]` (שישי ושבת). בוררי תאריך ורשתות לוח שנה חייבים להתחיל את השבוע ביום ראשון ולסמן את שישי ושבת, לא את שבת וראשון. שדה `<input type="date">` מקורי מוצג בפורמט של הדפדפן עצמו, ועלול להציג `20/04/2026` לצד הטקסט `20.04.2026` שלכם; השתמשו בבורר מותאם אם השניים חייבים להתאים.

להגדיר תגי עיצוב כדי שרכיבים במורד הזרם יישארו עקביים:

```css
:root {
  --date-format-short: 'dd.MM.yyyy';
  --time-format: 'HH:mm';
  --currency-locale: 'he-IL';
  --currency-code: 'ILS';
}
```

**מפרידי מספרים**

מפריד אלפים הוא פסיק (`1,234,567`), נקודה עשרונית היא נקודה (`1,234.50`). לא לעבור לסגנון האירופי `1.234,50` - הפיננסים בישראל משתמשים בקונבנציה האמריקאית.

### שלב 8: בדיקה בשני הכיוונים

רגרסיות RTL הן חזותיות, אז בודקים אותן חזותית. רנדרו כל סטורי של רכיב גם ב-`dir="rtl"` וגם ב-`dir="ltr"` (ובכל ערכת צבעים), למשל עם global ב-Storybook שקובע `dir` על שורש התצוגה, וצלמו כל שילוב ב-CI עם `toHaveScreenshot()` של Playwright. הוסיפו בדיקת lint או grep שנכשלת על מחלקות ותכונות פיזיות (`ml-`, `mr-`, `pl-`, `pr-`, `left-`, `right-`, `margin-left`) כדי שקוד חדש לא יחזיר אותן.

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
- הקובץ `references/domain-checklist.md` -- פריטי חובה ופריטים מתקדמים למערכת עיצוב RTL ישראלית, כל אחד עם המקור שלו, ושורות מפורשות של מה שמחוץ להיקף.
- הקובץ `references/hebrew-typography.md` -- קטלוג גופנים עבריים עם מדדי Google Fonts, זיווגים מומלצים למקרי שימוש שונים (SaaS, עריכה, ממשלה), אסטרטגיות ביצועים של טעינת גופנים, תכונות CSS ייחודיות לעברית (גובה שורה, ריווח מילים, כללי ריווח אותיות), והמלצות לסולם גדלים לממשקים דו-לשוניים עברית/אנגלית.

## מלכודות נפוצות
- טקסט עברי לרוב קצר מהמקביל האנגלי, אבל בכמה תלוי בטקסט. סוכנים עלולים לעצב layouts עם רוחב קבוע על בסיס אורך הטקסט באנגלית, וזה גורם לרווח לבן מיותר בעברית או לשבירת layout במעבר לאנגלית.
- הגופנים Heebo, Rubik ו-Assistant הם גופני רשת, שמוגשים מ-Google Fonts או באירוח עצמי. סוכנים עלולים לטעון אחד מהם בלי גופן מערכת חלופי לפני המשפחה הגנרית, ואז הטקסט לא מעוצב או קופץ בזמן הטעינה. השאירו `display: swap` (או `font-display: swap`) וגופן מערכת עם אותיות עבריות, כמו Arial, לפני `sans-serif`, כמו בשלב 1.
- תוויות טפסים בעברית צריכות להיות מיושרות לימין וממוקמות מימין לשדות (או מעליהם). סוכנים לפעמים ממקמים תוויות משמאל לשדות, וזה מוסכמה אנגלית שמרגישה לא טבעית ב-RTL.
- שדות קלט למספרי טלפון ישראליים צריכים לקבל פורמטים עם ובלי קידומת מדינה (054-1234567, ‎+972-54-1234567, וגם 0541234567). סוכנים עלולים לאמת רק את הפורמט הבינלאומי.
- סימן השקל (₪) הוא לא תו כיווני, ולכן מחיר inline כמו `1,234.50 ₪` בתוך פסקה בעברית עלול לזוז באופן לא צפוי בין דפדפנים. סוכנים בד"כ סומכים על אלגוריתם ה-bidi של הדפדפן ומדלגים על `<bdi>` או על `Intl.NumberFormat('he-IL', { style: 'currency' })`, וזה גורם לתצוגה לא עקבית של מחירים בין Chrome ל-Safari.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| Google Fonts – עברית | https://fonts.google.com/?subset=hebrew | Heebo, Assistant, Rubik, Frank Ruhl Libre, קטעי טעינה |
| תכונות CSS לוגיות (MDN) | https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Logical_properties_and_values | padding-inline, margin-block, מיקום לוגי |
| תמיכת RTL ב-Tailwind | https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support | וריאנטי `rtl:` ו-`ltr:` לספריות רכיבים |
| shadcn/ui RTL | https://ui.shadcn.com/docs/rtl | `rtl: true` בקובץ components.json, סגנונות נתמכים, DirectionProvider |
| WCAG Quick Reference | https://www.w3.org/WAI/standards-guidelines/wcag/ | דרישות ניגודיות וסדר קריאה שחלים על RTL |

## פתרון בעיות

### שגיאה: "הטקסט בעברית נראה צפוף או קטן מדי"
סיבה: משתמשים בגדלי גופן וגובהי שורה מותאמים ללטינית בעברית
פתרון: להגדיל את גודל הגופן הבסיסי ל-16px לפחות לגוף טקסט. לקבוע גובה שורה של 1.7 מינימום לעברית. אף פעם לא להוסיף ריווח אותיות לטקסט עברי. להוסיף ריווח מילים קל (0.05em) לשיפור הקריאות.

### שגיאה: "פריסת הרכיב נשברת ב-RTL"
סיבה: משתמשים בתכונות CSS פיזיות (margin-left, padding-right) במקום בתכונות לוגיות
פתרון: להחליף את כל התכונות הכיווניות הפיזיות במקבילות לוגיות: margin-inline-start, padding-inline-end, border-inline-start, inset-inline-start. להשתמש ב-flexbox וב-grid שמכבדים אוטומטית את תכונת dir.

### שגיאה: "אייקונים מצביעים לכיוון שגוי ב-RTL"
סיבה: אייקונים כיווניים (חצים, שברונים, כפתורי חזרה) לא משוקפים ל-RTL
פתרון: לשקף אייקונים כיווניים ב-SVG או בגופן אייקונים (כ-`inline-block`) עם CSS `transform: scaleX(-1)` בהקשר של `[dir="rtl"]`. אל תהפכו שברונים טקסטואליים כמו `>` או `›`: הדפדפן כבר משקף אותם ב-RTL. אייקונים לא-כיווניים (חיפוש, בית, הגדרות) לא צריכים להיות משוקפים. ליצור מחלקת שירות לשיקוף אייקונים ליישום עקבי.
