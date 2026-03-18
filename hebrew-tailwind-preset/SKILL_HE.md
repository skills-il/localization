# תצורת Tailwind לעברית

## הנחיות

### שלב 1: הגדרת Tailwind v4 ל-RTL

ראו `references/rtl-config.md` למדריך תצורה מלא.

**Tailwind v4 (תצורה מבוססת CSS):**
```css
/* app.css */
@import "tailwindcss";

@theme {
  /* מחסניות גופנים עבריות */
  --font-hebrew: 'Heebo', 'Assistant', 'Noto Sans Hebrew', sans-serif;
  --font-hebrew-serif: 'Frank Ruhl Libre', 'David Libre', serif;
  --font-mono: 'Fira Code', 'Source Code Pro', monospace;

  /* סולם גדלים מותאם לעברית */
  --text-xs: 0.8125rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;

  /* גובהי שורה לעברית (גבוהים יותר מברירת מחדל לטינית) */
  --leading-tight: 1.4;
  --leading-normal: 1.7;
  --leading-relaxed: 1.9;
}
```

**Tailwind v3 (תצורת JavaScript):**
```js
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        hebrew: ['Heebo', 'Assistant', 'Noto Sans Hebrew', 'sans-serif'],
        'hebrew-serif': ['Frank Ruhl Libre', 'David Libre', 'serif'],
      },
      lineHeight: {
        'hebrew': '1.7',
        'hebrew-tight': '1.4',
        'hebrew-relaxed': '1.9',
      },
    },
  },
  plugins: [],
};
```

### שלב 2: שימוש בתכונות שירות לוגיות

תמיד להעדיף תכונות שירות לוגיות על פני כיווניות פיזיות:

| פיזי (יש להימנע) | לוגי (יש להשתמש) | התנהגות ב-RTL |
|-------------------|-----------------|---------------|
| `ml-4` | `ms-4` | שוליים ימניים ב-RTL |
| `mr-4` | `me-4` | שוליים שמאליים ב-RTL |
| `pl-4` | `ps-4` | ריפוד ימני ב-RTL |
| `pr-4` | `pe-4` | ריפוד שמאלי ב-RTL |
| `left-0` | `start-0` | ימין: 0 ב-RTL |
| `right-0` | `end-0` | שמאל: 0 ב-RTL |
| `border-l` | `border-s` | גבול ימני ב-RTL |
| `border-r` | `border-e` | גבול שמאלי ב-RTL |
| `rounded-l-lg` | `rounded-s-lg` | עיגול ימני ב-RTL |
| `rounded-r-lg` | `rounded-e-lg` | עיגול שמאלי ב-RTL |
| `text-left` | `text-start` | מיושר לימין ב-RTL |
| `text-right` | `text-end` | מיושר לשמאל ב-RTL |
| `scroll-ml-4` | `scroll-ms-4` | שוליים ימניים לגלילה ב-RTL |

### שלב 3: שימוש בוריאנטים כיווניים לסגנונות ייחודיים ל-RTL

כאשר נדרשות דריסות ייחודיות לכיוון:

```html
<!-- הגדרת שורש -->
<html lang="he" dir="rtl">

<!-- שימוש בוריאנט כיווני -->
<div class="flex rtl:flex-row-reverse">
  <span class="rtl:rotate-180">&#8594;</span>
  <span>הבא</span>
</div>

<!-- שיקוף אייקונים כיווניים -->
<button class="flex items-center gap-2">
  <svg class="rtl:scale-x-[-1]"><!-- אייקון חץ --></svg>
  <span>חזרה</span>
</button>

<!-- ריווח מותנה שמשתנה לפי כיוון -->
<div class="ltr:ml-auto rtl:mr-auto">
  <!-- דחיפה לקצה בשני הכיוונים -->
</div>
```

### שלב 4: תכונות שירות טיפוגרפיות לעברית

```html
<!-- גוף טקסט עברי עם הגדרות תקינות -->
<body dir="rtl" class="font-hebrew text-base leading-hebrew
                        tracking-normal">

  <!-- כותרת עברית -->
  <h1 class="text-3xl font-bold leading-hebrew-tight">
    כותרת ראשית
  </h1>

  <!-- פסקה עברית -->
  <p class="text-base leading-hebrew [word-spacing:0.05em]">
    טקסט גוף עם ריווח מותאם לקריאות עברית.
  </p>

  <!-- תוכן מעורב עברית + אנגלית -->
  <p class="text-base leading-hebrew">
    פריט מספר <span dir="ltr" class="font-mono">ORD-12345</span> אושר
  </p>
</body>
```

### שלב 5: תבניות רכיבים RTL-First עם Tailwind

**כרטיס RTL-first:**
```html
<div class="rounded-lg border border-gray-200 p-6">
  <div class="flex items-center justify-between mb-4
              border-b border-gray-100 pb-4">
    <h3 class="text-lg font-bold">כותרת הכרטיס</h3>
    <span class="text-sm text-gray-500">פעיל</span>
  </div>
  <p class="text-base leading-hebrew text-gray-700">
    תוכן הכרטיס עם טקסט בעברית.
  </p>
  <div class="mt-4 flex gap-3">
    <button class="bg-blue-600 text-white px-4 py-2 rounded-md">
      אישור
    </button>
    <button class="border border-gray-300 px-4 py-2 rounded-md">
      ביטול
    </button>
  </div>
</div>
```

**ניווט RTL-first:**
```html
<nav dir="rtl" class="flex items-center justify-between
                       px-6 py-4 bg-white border-b">
  <div class="flex items-center gap-3">
    <img src="/logo.svg" alt="לוגו" class="h-8">
    <span class="font-bold text-xl">שם האתר</span>
  </div>
  <ul class="flex gap-6 text-sm font-medium">
    <li><a href="/" class="text-blue-600">ראשי</a></li>
    <li><a href="/about" class="text-gray-600">אודות</a></li>
    <li><a href="/contact" class="text-gray-600">צור קשר</a></li>
  </ul>
</nav>
```

**פריסת סרגל צד RTL-first:**
```html
<div class="grid grid-cols-[280px_1fr] min-h-screen">
  <!-- סרגל צד: מופיע מימין ב-RTL אוטומטית -->
  <aside class="border-e border-gray-200 pe-6 p-4">
    <nav class="space-y-2">
      <a href="#" class="block ps-4 py-2 rounded-md
                         bg-blue-50 text-blue-700 border-s-4
                         border-blue-600">לוח בקרה</a>
      <a href="#" class="block ps-4 py-2 rounded-md
                         text-gray-600">הגדרות</a>
    </nav>
  </aside>
  <!-- תוכן ראשי -->
  <main class="p-6">
    <h1 class="text-2xl font-bold mb-6">לוח בקרה</h1>
  </main>
</div>
```

### שלב 6: תכונות שירות לטפסים בעברית

```html
<form dir="rtl" class="max-w-lg space-y-6">
  <div>
    <label for="name" class="block text-sm font-medium
                              text-gray-700 mb-2">שם מלא</label>
    <input id="name" type="text"
           class="w-full px-4 py-3 border border-gray-300
                  rounded-md text-base font-hebrew
                  focus:outline-none focus:ring-2
                  focus:ring-blue-500">
  </div>

  <div>
    <label for="phone" class="block text-sm font-medium
                               text-gray-700 mb-2">טלפון</label>
    <input id="phone" type="tel" dir="ltr"
           placeholder="05X-XXXXXXX"
           class="w-full px-4 py-3 border border-gray-300
                  rounded-md text-base
                  focus:outline-none focus:ring-2
                  focus:ring-blue-500">
  </div>

  <div>
    <label for="message" class="block text-sm font-medium
                                 text-gray-700 mb-2">הודעה</label>
    <textarea id="message" rows="4"
              class="w-full px-4 py-3 border border-gray-300
                     rounded-md text-base font-hebrew
                     leading-hebrew
                     focus:outline-none focus:ring-2
                     focus:ring-blue-500"></textarea>
  </div>

  <button type="submit"
          class="w-full bg-blue-600 text-white py-3
                 rounded-md font-medium text-base
                 hover:bg-blue-700 transition-colors">
    שליחה
  </button>
</form>
```

## דוגמאות

### דוגמה 1: הגדרת Tailwind לפרויקט עברי
המשתמש אומר: "הגדר Tailwind לאפליקציית הווב העברית שלי"
תוצאה: הוספת משפחות גופנים עבריות לתמה של Tailwind, הגדרת גובהי שורה מותאמים לעברית, הגדרת `dir="rtl"` על אלמנט ה-HTML הראשי, והדגמת שימוש בתכונות שירות לוגיות (ms-/me-/ps-/pe-) במקום פיזיות (ml-/mr-/pl-/pr-).

### דוגמה 2: המרת רכיב Tailwind מ-LTR ל-RTL
המשתמש אומר: "התאם את רכיב ה-Tailwind הזה לעבודה ב-RTL עברי"
תוצאה: החלפת כל מחלקות השירות הפיזיות במקבילות לוגיות (ml- ל-ms-, pl- ל-ps-, text-left ל-text-start, border-l ל-border-s, rounded-l ל-rounded-s), הוספת וריאנטי rtl: לאייקונים כיווניים, והגדרת מחלקת font-hebrew על אלמנטי טקסט.

### דוגמה 3: בניית לוח בקרה עברי עם Tailwind
המשתמש אומר: "צור פריסת לוח בקרה עברי עם Tailwind"
תוצאה: בניית פריסת grid עם סרגל צד RTL (border-e, pe-6), ניווט עם גופן עברי וזרימת RTL, רכיבי כרטיסים עם ריווח לוגי, ואלמנטי טופס עם טיפוגרפיה עברית תקינה (font-hebrew, leading-hebrew).

## משאבים מצורפים

### קובצי עזר
- `references/rtl-config.md` -- מדריך תצורת Tailwind CSS ל-RTL מלא: דוגמאות תצורה CSS-first ל-v4 ו-JavaScript ל-v3, טבלת מיפוי מלאה מתכונות שירות פיזיות ללוגיות, תבניות שימוש בוריאנטים כיווניים, מחסניות גופנים עבריות מוכנות, הגדרות תגי טיפוגרפיה, ומדריך מיגרציה מתכונות פיזיות ללוגיות.

## מלכודות נפוצות
- Tailwind CSS v3+ תומך בווריאנטים RTL (תחילית rtl:), אבל סוכנים לא משתמשים בהם ומקודדים mr-4 כשצריך להשתמש ב-ms-4 (margin-start) לתאימות RTL.
- הכלי space-x-4 ב-Tailwind לא מכבד כיוון RTL. סוכנים חייבים להשתמש ב-gap-4 עם flex או grid, או להוסיף ידנית rtl:space-x-reverse כדי להפוך את כיוון הרווח.
- הצהרות גופנים מותאמים לעברית חייבות לכלול font-display: swap כדי למנוע FOIT (הבזק של טקסט בלתי נראה). סוכנים עלולים להשמיט זאת, מה שגורם לטקסט עברי להיעלם בזמן טעינת הגופן.
- text-left ו-text-right ב-Tailwind הן תכונות פיזיות. יש להשתמש בקלאסים text-start ו-text-end ליישור מודע RTL. סוכנים ברירת מחדל לקלאסי כיוון פיזיים.

## פתרון בעיות

### שגיאה: "תכונות שירות לוגיות של Tailwind לא עובדות"
סיבה: שימוש בגרסת Tailwind ישנה ללא תמיכה בתכונות לוגיות
פתרון: תכונות שירות לוגיות (ms-, me-, ps-, pe-, start-, end-) דורשות Tailwind v3.3+. עבור v3.0-3.2, יש להשתמש בוריאנטי rtl:/ltr: במקום (למשל `rtl:mr-4 ltr:ml-4`). ל-Tailwind v4 יש תמיכה מלאה בתכונות לוגיות מובנית.

### שגיאה: "גופן לא מוחל עם מחלקת font-hebrew"
סיבה: משפחת גופנים עברית לא הוגדרה בתצורת Tailwind
פתרון: הוספת מחסנית גופנים עברית לתמה של Tailwind תחת fontFamily.hebrew. וידוא שה-CSS של הגופן מיובא (קישור Google Fonts או @font-face מקומי). אימות ששם המחלקה תואם את מפתח התצורה.

### שגיאה: "סרגל צד מופיע בצד הלא נכון ב-RTL"
סיבה: פריסת Grid או Flex לא מכבדת תכונת dir
פתרון: CSS Grid ו-Flexbox מכבדים אוטומטית `dir="rtl"`. יש לוודא ש-`dir="rtl"` מוגדר על אלמנט ה-`html`. שימוש בתכונות לוגיות לגבולות (border-e במקום border-r) וריפוד (pe- במקום pr-). אין להשתמש ב-`direction: rtl` ב-CSS; יש להשתמש בתכונת ה-HTML במקום.
