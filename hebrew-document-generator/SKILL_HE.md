# מחולל מסמכים בעברית

## הנחיות

### שלב 1: בחרו את פורמט הפלט

| פורמט | ספרייה | מתאים ל- | תמיכת RTL |
|--------|---------|----------|-------------|
| PDF | reportlab | חשבוניות, מסמכי מס, טפסים להדפסה | רושמים גופן עברי, משתמשים ב-`canvas.drawRightString()` |
| PDF | WeasyPrint | מסמכים מעוצבים מ-HTML/CSS | מובנה דרך `dir="rtl"` ב-HTML |
| DOCX | python-docx | חוזים, הצעות מחיר, פרוטוקולים | מגדירים `bidi` בפסקה ותכונות RTL |
| PPTX | pptxgenjs (Node) | מצגות, שקפים | תיבות טקסט RTL עם `rtlMode: true` |

### שלב 2: התקינו תלויות וגופנים עבריים

**יצירת PDF בפייתון:**
```bash
pip install reportlab weasyprint
```

**יצירת DOCX בפייתון:**
```bash
pip install python-docx python-bidi
```

**יצירת PPTX ב-Node.js:**
```bash
npm install pptxgenjs
```

**גופנים עבריים מומלצים (מתקינים על המערכת):**

| גופן | סגנון | מתאים ל- | מקור |
|-------|-------|----------|--------|
| Heebo | סנס-סריף, מודרני | מסמכי ווב, חשבוניות | Google Fonts |
| David | סריף קלאסי | חוזים משפטיים, מכתבים רשמיים | מערכת (Windows/macOS) |
| Narkisim | סריף, אלגנטי | הצעות מחיר, הזמנות | מערכת (Windows) |
| Frank Ruehl | סריף מסורתי | אקדמי, ספרותי | Google Fonts (Frank Ruhl Libre) |
| Rubik | סנס-סריף, מעוגל | מצגות, שיווק | Google Fonts |
| Assistant | סנס-סריף, נקי | התכתבות עסקית | Google Fonts |

תסתכלו על `references/hebrew-fonts.md` לקישורי הורדה והוראות התקנה.

### שלב 3: PDF בעברית עם reportlab

תסתכלו על `scripts/generate_doc.py` לפייפליין המלא של היצירה.

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from bidi.algorithm import get_display

# רישום גופן עברי
pdfmetrics.registerFont(TTFont('Heebo', 'Heebo-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Heebo-Bold', 'Heebo-Bold.ttf'))

def create_hebrew_pdf(filename, title, content_lines):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # כותרת -- יישור לימין עבור RTL
    c.setFont('Heebo-Bold', 18)
    hebrew_title = get_display(title)
    c.drawRightString(width - 20*mm, height - 30*mm, hebrew_title)

    # שורות תוכן
    c.setFont('Heebo', 12)
    y = height - 50*mm
    for line in content_lines:
        display_line = get_display(line)
        c.drawRightString(width - 20*mm, y, display_line)
        y -= 7*mm

    c.save()
```

נקודות חשובות ל-reportlab בעברית:
- תמיד להשתמש ב-`get_display()` מ-python-bidi לסידור מחדש של תווים
- להשתמש ב-`drawRightString()` לטקסט RTL מיושר לימין
- לרשום גופני TTF עבריים במפורש - ל-reportlab אין תמיכה מובנית בעברית
- לקבוע גובה שורה של לפחות 1.5 מגודל הגופן לקריאות בעברית

### שלב 4: PDF בעברית עם WeasyPrint

```python
from weasyprint import HTML

html_content = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<style>
  @font-face {
    font-family: 'Heebo';
    src: url('Heebo-Regular.ttf');
  }
  body {
    font-family: 'Heebo', sans-serif;
    direction: rtl;
    font-size: 12pt;
    line-height: 1.7;
  }
  h1 { font-size: 18pt; text-align: start; }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #333;
    padding: 6px 10px;
    text-align: start;
  }
</style>
</head>
<body>
  <h1>חשבונית מס</h1>
  <!-- תוכן המסמך כאן -->
</body>
</html>
"""

HTML(string=html_content).write_pdf('invoice.pdf')
```

היתרונות של WeasyPrint לעברית:
- תמיכה מלאה ב-CSS כולל תכונות לוגיות
- RTL מובנה דרך תכונת `dir` ב-HTML
- טבלאות מוצגות נכון ב-RTL
- תמיכה ב-`@font-face` לגופנים עבריים מותאמים

### שלב 5: DOCX בעברית עם python-docx

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_paragraph_rtl(paragraph):
    """מגדיר כיוון פסקה ל-RTL עבור טקסט עברי."""
    pPr = paragraph._p.get_or_add_pPr()
    bidi = pPr.makeelement(qn('w:bidi'), {})
    pPr.append(bidi)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def set_run_rtl(run):
    """מגדיר כיוון run ל-RTL."""
    rPr = run._r.get_or_add_rPr()
    rtl = rPr.makeelement(qn('w:rtl'), {})
    rPr.append(rtl)

doc = Document()
style = doc.styles['Normal']
font = style.font
font.name = 'David'
font.size = Pt(12)

heading = doc.add_heading(level=1)
run = heading.add_run('חוזה שירותים')
set_run_rtl(run)
set_paragraph_rtl(heading)

para = doc.add_paragraph()
run = para.add_run('הסכם זה נערך ונחתם ביום...')
run.font.name = 'David'
run.font.size = Pt(12)
set_run_rtl(run)
set_paragraph_rtl(para)

doc.save('contract.docx')
```

### שלב 6: PPTX בעברית עם pptxgenjs

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

pptx.layout = 'LAYOUT_16x9';
pptx.rtlMode = true;

const slide = pptx.addSlide();

// כותרת בעברית
slide.addText('סקירה רבעונית', {
  x: 0.5, y: 0.5, w: '90%', h: 1.0,
  fontSize: 28,
  fontFace: 'Heebo',
  color: '1a1a2e',
  align: 'right',
  rtlMode: true,
  bold: true,
});

// נקודות תבליט בעברית
slide.addText([
  { text: 'תוצאות כספיות', options: { bullet: true, rtlMode: true } },
  { text: 'יעדים לרבעון הבא', options: { bullet: true, rtlMode: true } },
  { text: 'סיכום פעילות', options: { bullet: true, rtlMode: true } },
], {
  x: 0.5, y: 2.0, w: '90%', h: 3.0,
  fontSize: 18,
  fontFace: 'Heebo',
  align: 'right',
  rtlMode: true,
});

pptx.writeFile({ fileName: 'quarterly-review.pptx' });
```

### שלב 7: תבניות מסמכים עסקיים ישראליים

תסתכלו על `references/templates.md` למפרטי שדות מלאים לכל סוג מסמך.

| תבנית | שם בעברית | שדות נדרשים |
|----------|-------------|-----------------|
| חשבונית מס | חשבונית מס | שם עסק, מספר עוסק מורשה, תאריך, פריטים, מע"מ (18%), סה"כ |
| חוזה | חוזה | צדדים, ת.ז./ח.פ., תנאים, חתימות, תאריך |
| הצעת מחיר | הצעת מחיר | פרטי עסק, תמחור מפורט, תוקף, תנאים |
| פרוטוקול | פרוטוקול | תאריך, משתתפים, סדר יום, החלטות, משימות |
| קבלה | קבלה | שם עסק, מספר קבלה, סכום, אמצעי תשלום, תאריך |

**חשבונית מס - שדות שהחוק הישראלי דורש:**
- שם העסק וכתובת
- מספר עוסק מורשה
- מספר חשבונית רץ
- תאריך הנפקה
- שם הלקוח ות.ז./ח.פ.
- פריטים עם תיאור, כמות, מחיר ליחידה
- סכום ביניים, מע"מ 18%, וסה"כ בש"ח

## דוגמאות

### דוגמה 1: חשבונית מס כ-PDF
המשתמש אומר: "צור חשבונית מס בעברית כ-PDF לעסק שלי"
תוצאה: יוצרים PDF בגודל A4 עם reportlab או WeasyPrint, עם פריסת RTL, כותרת עסק, מספר חשבונית רץ, טבלת פריטים, חישוב מע"מ 18%, סכומים בש"ח עם סמל שקל, וגופן עברי לאורך כל המסמך.

### דוגמה 2: חוזה DOCX בעברית
המשתמש אומר: "נסח חוזה שירותים בעברית כמסמך Word"
תוצאה: משתמשים ב-python-docx עם תמיכה בפסקה דו-כיוונית, גופן David, יישור RTL, סעיפים מובנים (צדדים, היקף, תנאי תשלום, ביטול, חתימות), וניסוח משפטי עברי תקני.

### דוגמה 3: מצגת בעברית
המשתמש אומר: "הכן מצגת בעברית לסקירה הרבעונית שלנו"
תוצאה: משתמשים ב-pptxgenjs עם rtlMode מופעל, גופן Heebo, תיבות טקסט מיושרות לימין, נקודות תבליט ב-RTL, כותרות שקפים בעברית, ופריסה מקצועית.

### דוגמה 4: מסמכים באצווה
המשתמש אומר: "צור 50 חשבוניות בעברית מקובץ CSV"
תוצאה: קוראים נתוני CSV, עוברים על השורות, משתמשים ב-`scripts/generate_doc.py` כדי לייצר קובצי PDF בודדים עם מספרי חשבונית ייחודיים, פרטי לקוח ופריטים לכל שורה.

## משאבים מצורפים

### סקריפטים
- `scripts/generate_doc.py` - יצירת מסמכי PDF בעברית עם reportlab: רישום גופנים עבריים, סידור טקסט RTL עם python-bidi, הפקת מסמכים עסקיים ישראליים (חשבוניות, קבלות) עם חישובי מע"מ ופורמט ש"ח. הרצה: `python scripts/generate_doc.py --help`

### קובצי עזר
- `references/hebrew-fonts.md` - קטלוג גופנים עבריים עם גופנים מומלצים לסוגי מסמכים שונים (סנס-סריף, סריף, מונוספייס), קישורי הורדה מ-Google Fonts, טבלת זמינות של גופני מערכת, הצעות לזיווג גופנים, והוראות התקנה ל-macOS, Linux ו-Windows.
- `references/templates.md` - תבניות מסמכים עסקיים ישראליים עם שדות נדרשים לכל סוג מסמך (חשבונית מס, חוזה, הצעת מחיר, קבלה, פרוטוקול), דרישות החוק הישראלי לחשבוניות, כללי מע"מ, וניסוח עסקי סטנדרטי בעברית.

## מלכודות נפוצות
- מחוללי PDF נוטים לכיוון טקסט LTR כברירת מחדל. מסמכים בעברית חייבים כיוון פסקה RTL, וטקסט מעורב עברית-אנגלית צריך תמיכה תקינה באלגוריתם BiDi.
- סוכנים עלולים לבחור גופנים בלי תמיכה בתווים עבריים (Arial עובד, אבל הרבה גופנים דקורטיביים לטיניים לא). תמיד תוודאו שהגופן כולל את טווח ה-Unicode העברי (U+0590-U+05FF).
- פורמט התאריך בעברית הוא DD/MM/YYYY בהקשר חילוני, ותאריכים עבריים (ט"ו באדר תשפ"ו למשל) למסמכים דתיים/מסורתיים. סוכנים עלולים ללכת ל-MM/DD/YYYY כברירת מחדל.
- מסמכים משפטיים בישראל דורשים עיצוב מסוים: לא משתמשים בניקוד בעברית עסקית/משפטית רגילה. סוכנים עלולים להוסיף ניקוד כי הם חושבים שזה משפר את הבהירות, אבל בפועל זה נראה לא מקצועי במסמכים רשמיים.

## פתרון בעיות

### שגיאה: "תווים עבריים מוצגים כריבועים או סימני שאלה"
סיבה: גופן עברי לא רשום או לא קיים במערכת
פתרון: תורידו גופן TTF עברי (Heebo מ-Google Fonts למשל), רשמו אותו עם `pdfmetrics.registerFont()` ל-reportlab, או התקינו אותו כגופן מערכת ל-WeasyPrint.

### שגיאה: "הטקסט מוצג משמאל לימין במקום מימין לשמאל"
סיבה: חסר סידור bidi או הגדרת כיוון RTL
פתרון: ב-reportlab, תפעילו `get_display()` מ-python-bidi. ב-python-docx, תקראו ל-`set_paragraph_rtl()` ול-`set_run_rtl()`. ב-WeasyPrint, תוודאו `dir="rtl"` על אלמנט ה-HTML.

### שגיאה: "מספרים וסימני פיסוק במיקום שגוי"
סיבה: אלגוריתם הטקסט הדו-כיווני לא מטפל נכון בתוכן מעורב עברית/מספרים
פתרון: עוטפים רצפי מספרים בסימוני LTR. ב-reportlab, משתמשים ב-`get_display()` עם `base_dir='R'`. בכלים מבוססי HTML, תוודאו `unicode-bidi: isolate` על רכיבי span מוטבעים ב-LTR.
