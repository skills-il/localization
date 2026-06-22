# מחולל מסמכים בעברית

## הנחיות

### שלב 1: בחרו את פורמט הפלט

| פורמט | ספרייה | מתאים ל- | תמיכת RTL |
|--------|---------|----------|-------------|
| PDF | reportlab | חשבוניות, מסמכי מס, טפסים להדפסה | רושמים גופן עברי, משתמשים ב-`canvas.drawRightString()` |
| PDF | WeasyPrint | מסמכים מעוצבים מ-HTML/CSS | מובנה דרך `dir="rtl"` ב-HTML |
| DOCX | python-docx | חוזים, הצעות מחיר, פרוטוקולים | מגדירים `bidi` בפסקה; מפצלים runs מעורבים, מגדירים גופן `w:cs` ו-`w:rtl` רק על ה-runs העבריים |
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
from bidi import get_display  # python-bidi 0.6.x; ראו הערה למטה

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
- ייבוא python-bidi: הייבוא הקנוני והמומלץ הוא `from bidi import get_display` (העליון). הנתיב הישן `from bidi.algorithm import get_display` עדיין נטען ב-0.6.x כמודול תאימות לאחור, אבל עדיף להשתמש בייבוא העליון. גרסה 0.6.x גם הפסיקה לתמוך בפייתון מתחת ל-3.9.
- טקסט רב-שורתי: `drawRightString()` מצייר שורה אחת ולא גולש. לכל טקסט גוף ארוך משורה אחת, תשתמשו ב-flowable מסוג `Paragraph` (מ-`reportlab.platypus`) עם `ParagraphStyle` מיושר לימין ו-RTL. הסקריפט המצורף `scripts/generate_doc.py` משתמש ב-`drawRightString` שורה-שורה למסמכים קומפקטיים בפריסה קבועה (חשבוניות, קבלות); הוא יחתוך מחרוזות עבריות ארוכות. כדאי לעבור ל-`Paragraph` ול-flowables של platypus לחוזים או לכל טקסט גוף שגולש.

### שורות מעורבות עברית / לטינית / ספרות

הכשל הנפוץ ביותר ב-RTL במסמכים מיוצרים הוא שורה שמערבת תיאור בעברית עם מספרים LTR וסמל מטבע, למשל שורת פריט בחשבונית. `get_display()` מטפל בסידור הדו-כיווני, אבל צריך להעביר את *כל המחרוזת הלוגית* בקריאה אחת כדי שהאלגוריתם יראה את ההקשר המלא:

```python
from bidi import get_display

# סדר לוגי: תיאור בעברית, אחר כך כמות, מחיר ליחידה, מטבע
line = 'ייעוץ טכני (3 שעות) - 1,500.00 ש"ח'
c.setFont('Heebo', 11)
c.drawRightString(width - 20 * mm, y, get_display(line))
```

הספרות, הפסיק, הנקודה והסוגריים נשארים כולם במיקום ה-LTR הנכון כי האלגוריתם הדו-כיווני פותר אותם ביחס לעברית שמסביב. אל תפצלו את השורה לחלקים ותסדרו אותם בעצמכם, ואל תקראו ל-`get_display()` רק על החלק העברי, שתי הגישות שוברות את סדר המספרים.

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

ב-DOCX טקסט מעורב עברית/אנגלית נשבר הכי הרבה, ומנוע ה-bidi של Microsoft Word מחמיר יותר מתקן Unicode. LibreOffice, תצוגה מקדימה של macOS ורוב המציגים מרנדרים תוצאה סלחנית שמסתירה באגים ייחודיים ל-Word, אז תמיד בדקו ב-Word עצמו ולא במציג חלופי. ארבעה כללים, כל אחד נלמד מול Word אמיתי:

1. כל פסקה עברית נושאת `<w:bidi/>` (כיוון בסיס RTL); שורה באנגלית בלבד (ערך מעבדה, שם תרופה, שורה קלינית באנגלית) מקבלת בסיס LTR ויישור לשמאל. העוזר קובע זאת לכל פסקה לפי האם השורה מכילה עברית, כך ששורות באנגלית בלבד לא נדחקות לשוליים הימניים במסמך עברי.
2. **אל תשימו `<w:rtl/>` על ה-runs של פסקה מעורבת עברית+אנגלית.** זו המלכודת הגדולה ביותר ב-Word. Word מכבד `<w:rtl/>` בקפדנות: כל לטינית או מספר שנלכד ב-run מסומן rtl (או לידו) נהפך, כך ש-`7/2023` מודפס `2023/7`, קוד `KI-67` מוטבע מתהפך, והסוגריים סביב קבוצה מעורבת כמו `(גסטרית, KI-67)` לא מזדווגים נכון. בפסקה מעורבת ה-`<w:bidi/>` של הפסקה כבר מסדר את השורה, השאירו כל run בלי דגל.
3. **סמנו `<w:rtl/>` רק על runs עבריים של פסקה ללא אותיות לטיניות** (תווית או כותרת עברית טהורה, ספרות מותרות). שם הדגל מעגן נקודתיים נגררות (`מחלות רקע:`) לקצה השמאלי. סמן כותרת מספרי מוביל (`2.`, `10.`) ממוזג בנוסף אל ה-run העברי (`_merge_list_marker`) כדי שהנקודה שלו לא תתהפך ל-`.2`; תאריך כמו `13/01/2026` נשאר run מסוג LTR נפרד כדי ש-Word לא יהפוך אותו. הפיצול נשאר לפי סקריפט כדי שכל run יקבל את גופן הסקריפט המורכב הנכון.
4. כל run מגדיר את גופן הסקריפט המורכב (`w:cs`) ואת הגודל (`w:szCs`). עברית היא "סקריפט מורכב" במודל של Word, אז `w:ascii`/`w:sz` לבדם לעולם לא חלים על התווים העבריים. השמטת `w:cs`/`w:szCs` היא הסיבה הנפוצה ביותר ל"הגופן והגודל שהגדרתי לא עשו כלום והעברית נראית שבורה". מודגש ונטוי זהים: `w:b`/`w:i` משפיעים רק על לטינית, צריך גם `w:bCs`/`w:iCs`. **לעולם אל תכניסו תווי בידוד כיווניים של Unicode (U+2066-2069) או סימונים כדי לכפות סדר, Word מרנדר אותם כריבועי `.notdef` גלויים בגופן David גם כשמציגים אחרים מסתירים אותם.**

```python
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# בלוק עברי + צורות הצגה עבריות. משמש לבחירת כיוון של כל run.
_HEB = re.compile(r'[\u0590-\u05FF\uFB1D-\uFB4F]')
_LIST_MARKER = re.compile(r'^\d{1,2}\.$')  # 1-2 digit list marker, e.g. "2."

def _strong(ch):
    """True לאות עברית, False לתו חזק מסוג LTR (לטינית או ספרת ASCII), None לתו
    ניטרלי. ספרות נחשבות LTR כדי שמספר לא ירכב בתוך run עברי (Word הופך מספר
    שנלכד ב-run מסומן rtl)."""
    if _HEB.match(ch):
        return True
    if ch.isascii() and ch.isalnum():
        return False
    return None

def _split_by_script(text):
    """מפצל מחרוזת מעורבת ל-runs בצורת (segment, is_rtl).

    כיוון כל run נקבע לפי התווים החזקים שבו; תווים ניטרליים (רווחים, ספרות,
    פיסוק) נצמדים ל-run הנוכחי. ניטרלים בתחילת המחרוזת יורשים את כיוון התו
    החזק הראשון בכל המחרוזת (ברירת מחדל RTL למחרוזת ניטרלית לגמרי במסמך עברי),
    כך ששורה לטינית בעיקרה שמתחילה בספרה או בסוגר לא מסומנת בטעות RTL. הפיצול
    מקבץ תווים כך שכל run יקבל את גופן הסקריפט המורכב הנכון; ב-Word כיוון ה-run
    נקבע לפי כללי ה-rtl ב-add_rtl_paragraph, ולא לפי הפיצול הזה לבדו.
    """
    default_rtl = next((s for s in (_strong(c) for c in text) if s is not None), True)
    segments, buf, buf_rtl = [], '', None
    for ch in text:
        s = _strong(ch)
        kind = s if s is not None else (buf_rtl if buf_rtl is not None else default_rtl)
        if buf_rtl is None or kind == buf_rtl:
            buf, buf_rtl = buf + ch, kind
        else:
            segments.append((buf, buf_rtl))
            buf, buf_rtl = ch, kind
    if buf:
        segments.append((buf, buf_rtl))
    return segments

def _shift_boundary_spaces(segments):
    """מעביר רווח שבסוף run מסוג LTR שקודם ל-run מסוג RTL אל תחילת ה-run ה-RTL.
    Word גוזם רווח נגרר של run בגבול כיוון, מה שמצמיד מספר מוביל לכותרת
    ("2.\u05db\u05d5\u05ea\u05e8\u05ea"); רווח מוביל ב-run ה-RTL שורד ומחזיר את הרווח.
    בלי זה כותרות עבריות ממוספרות מאבדות את הרווח אחרי "N.".
    """
    out = [[seg, rtl] for seg, rtl in segments]
    for i in range(len(out) - 1):
        seg, rtl = out[i]
        nseg, nrtl = out[i + 1]
        if rtl is False and nrtl is True and seg.endswith(' '):
            stripped = seg.rstrip(' ')
            out[i][0] = stripped
            out[i + 1][0] = seg[len(stripped):] + nseg
    return [(s, r) for s, r in out if s]

def _merge_list_marker(segments):
    """סמן רשימה מספרי מוביל קצר ("2.", "10.") בשורת RTL חייב להיות חלק מה-run
    העברי, אחרת Word מציף את הנקודה שלו לצד הלא נכון (".2"). ממזגים run סמן
    מסוג LTR מוביל אל ה-run העברי שאחריו. מתאים רק ל-1-2 ספרות + נקודה, לעולם
    לא לתאריך כמו 13/01/2026 (שחייב להישאר run מסוג LTR כדי ש-Word לא יהפוך אותו)."""
    if (len(segments) >= 2 and segments[0][1] is False
            and _LIST_MARKER.match(segments[0][0].strip())
            and segments[1][1] is True):
        return [(segments[0][0] + segments[1][0], True)] + list(segments[2:])
    return list(segments)

def _para_is_rtl(text):
    """בוחר את כיוון הבסיס של הפסקה במסמך עברי.

    אות עברית כלשהי -> בסיס RTL: משפט עברי משלב לעיתים קרובות מונחים באנגלית,
    שמות תרופות או מספרים, וחייב עדיין לזרום מימין לשמאל. אין עברית אבל יש לטינית
    -> בסיס LTR, כך ששורה באנגלית בלבד (ערך מעבדה, שורה קלינית באנגלית) תיושר
    לשמאל במקום להידחק לשוליים הימניים. הכול ניטרלי (ספרות/פיסוק) -> RTL, ברירת
    המחדל של המסמך. זה התיקון ל"שורות באנגלית בלבד יוצאות מיושרות לימין והמסמך
    עדיין נראה שבור ב-RTL".
    """
    if _HEB.search(text):
        return True
    if any(ch.isascii() and ch.isalnum() for ch in text):
        return False
    return True

def add_rtl_paragraph(doc, text, font='David', size=12, bold=False, italic=False,
                      heading_level=None):
    """מוסיף פסקה שמרנדרת נכון טקסט מעורב עברית/לטינית/ספרות, ובוחרת אוטומטית
    כיוון בסיס RTL או LTR לפי האם השורה מכילה עברית.

    מכסה פסקאות גוף בלבד. תאי טבלה, כותרות עליונות/תחתונות ורשימות ממוספרות הם
    "סיפורים" נפרדים במסמך: החילו את אותה לוגיקה על כל אחת מהפסקאות שלהם, והוסיפו
    `<w:bidi/>` ל-`sectPr` של המקטע עבור עמוד RTL מלא.
    """
    p = doc.add_heading(level=heading_level) if heading_level else doc.add_paragraph()

    # (1) כיוון בסיס של הפסקה: RTL כשהשורה מכילה עברית כלשהי (משפט עברי משלב
    #     לעיתים אנגלית וחייב עדיין לזרום מימין לשמאל); LTR לשורה לטינית בלבד,
    #     כך ששורה באנגלית בלבד תיושר לשמאל במקום להידחק לשוליים הימניים.
    base_rtl = _para_is_rtl(text)
    pPr = p._p.get_or_add_pPr()
    if base_rtl:
        pPr.append(pPr.makeelement(qn('w:bidi'), {}))
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if base_rtl else WD_ALIGN_PARAGRAPH.LEFT

    # פסקה שיש בה אות לטינית כלשהי היא "מעורבת": לעולם לא מסמנים rtl על ה-runs
    # שלה (כלל 2). פסקה עם עברית בלבד (+ספרות/פיסוק) היא "טהורה": ה-runs העבריים
    # שלה כן מקבלים rtl, כדי לעגן נקודתיים נגררות ומספרים מובילים.
    para_has_latin = any(ch.isascii() and ch.isalpha() for ch in text)

    for segment, is_rtl in _shift_boundary_spaces(_merge_list_marker(_split_by_script(text))):
        run = p.add_run(segment)
        rPr = run._r.get_or_add_rPr()
        # ילדי rPr חייבים להישאר בסדר הסכמה של OOXML: rFonts, b, bCs, i, iCs, sz, szCs, rtl
        rPr.append(rPr.makeelement(qn('w:rFonts'), {
            qn('w:ascii'): font, qn('w:hAnsi'): font, qn('w:cs'): font}))
        if bold:
            # הדגשה דורשת גם w:b (לטינית) וגם w:bCs (סקריפט מורכב / עברית)
            rPr.append(rPr.makeelement(qn('w:b'), {}))
            rPr.append(rPr.makeelement(qn('w:bCs'), {}))
        if italic:
            # נטוי דורש באותו אופן גם w:i וגם w:iCs עבור עברית
            rPr.append(rPr.makeelement(qn('w:i'), {}))
            rPr.append(rPr.makeelement(qn('w:iCs'), {}))
        # (3) גודל סקריפט מורכב, כדי שהגודל יחול על העברית
        rPr.append(rPr.makeelement(qn('w:sz'),   {qn('w:val'): str(size * 2)}))
        rPr.append(rPr.makeelement(qn('w:szCs'), {qn('w:val'): str(size * 2)}))
        # (2) מסמנים rtl רק על runs עבריים של פסקה ללא אותיות לטיניות. בפסקה
        #     מעורבת עברית+אנגלית אף run לא מסומן, אחרת Word הופך את המספרים/
        #     הלטינית המוטבעים ומשבש סוגריים. ה-<w:bidi/> של הפסקה לבדו מסדר
        #     שורות מעורבות נכון.
        if is_rtl and not para_has_latin:
            rPr.append(rPr.makeelement(qn('w:rtl'), {}))
    return p

doc = Document()
doc.styles['Normal'].font.name = 'David'
doc.styles['Normal'].font.size = Pt(12)

add_rtl_paragraph(doc, 'חוזה שירותים', size=18, bold=True, heading_level=1)
add_rtl_paragraph(doc, 'ההסכם נחתם בין חברת Acme בע"מ לבין הלקוח (גרסה 2).')

doc.save('contract.docx')
```

**אל תקראו ל-`get_display()` על טקסט של DOCX.** בניגוד ל-reportlab (שמצייר גליפים במיקום קבוע ולכן זקוק ל-python-bidi כדי לסדר אותם), Word מפעיל את אלגוריתם ה-bidi בעצמו. עיבוד מקדים של מחרוזת עם `get_display()` והעברתה ל-python-docx מפעילים את האלגוריתם פעמיים ומשבשים את התוצאה. `get_display()` שייך לנתיב ה-PDF בלבד.

העוזר הזה מכסה פסקאות גוף. **טבלאות, כותרות עליונות/תחתונות ורשימות ממוספרות/תבליטים** הם "סיפורים" נפרדים במסמך שהעוזר לא מגיע אליהם: החילו את אותה לוגיקה של `<w:bidi/>` + פיצול runs לפי סקריפט על כל אחת מהפסקאות שלהם, והוסיפו `<w:bidi/>` ל-`sectPr` של המקטע עבור זרימת עמוד RTL מלאה.

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
- **מספר הקצאה במודל "חשבוניות ישראל"** לחשבונית מס בסכום שמעל הסף הנוכחי. הסף יורד בהדרגה (20,000 ש"ח ב-2025, 10,000 ש"ח מינואר 2026, **5,000 ש"ח מ-1 ביוני 2026**, לפני מע"מ). בסכום שמעל הסף הקונה אינו יכול לקזז את מס התשומות אלא אם המוכר קיבל מספר הקצאה מרשות המסים והדפיס אותו על החשבונית. הוסיפו שדה מספר הקצאה לכל תבנית חשבונית והתייחסו לסף כרגיש לזמן (ודאו את הסכום העדכני מול רשות המסים).

## דוגמאות

### דוגמה 1: חשבונית מס כ-PDF
המשתמש אומר: "צור חשבונית מס בעברית כ-PDF לעסק שלי"
תוצאה: יוצרים PDF בגודל A4 עם reportlab או WeasyPrint, עם פריסת RTL, כותרת עסק, מספר חשבונית רץ, טבלת פריטים, חישוב מע"מ 18%, סכומים בש"ח עם סמל שקל, וגופן עברי לאורך כל המסמך.

### דוגמה 2: חוזה DOCX בעברית
המשתמש אומר: "נסח חוזה שירותים בעברית כמסמך Word"
תוצאה: משתמשים ב-python-docx עם העוזר `add_rtl_paragraph` (שלב 5): פסקאות `<w:bidi/>`, פיצול runs לפי סקריפט כך שאנגלית/מספרים מוטבעים נשארים במקומם, גופן `w:cs` וגודל `w:szCs`, גופן David, יישור RTL, סעיפים מובנים (צדדים, היקף, תנאי תשלום, ביטול, חתימות), וניסוח משפטי עברי תקני.

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

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| תיעוד reportlab | https://docs.reportlab.com/ | API של Canvas, flowables של platypus, רישום גופנים |
| תיעוד WeasyPrint | https://doc.courtbouillon.org/weasyprint/stable/ | המרת HTML/CSS ל-PDF, תמיכת RTL, @font-face |
| תיעוד python-docx | https://python-docx.readthedocs.io/ | מודל המסמך, runs, תכונות פסקה |
| python-bidi (PyPI) | https://pypi.org/project/python-bidi/ | גרסה נוכחית, נתיב ייבוא, יומן שינויים |
| דרישות חשבונית מס בישראל | https://he.wikipedia.org/wiki/חשבונית_מס | שדות חובה בחשבונית מס; כדאי להצליב מול כללי רשות המסים העדכניים |

לדרישות משפטיות מחייבות תמיד כדאי לאמת מול ההנחיות העדכניות של רשות המסים, ערך הוויקיפדיה הוא נקודת התמצאות ולא מקור סמכות.

## שרתי MCP מומלצים

אין שרת MCP שמתאים לסקיל הזה. יצירת מסמכים בעברית רצה כולה דרך ספריות פייתון ו-Node מקומיות (reportlab, WeasyPrint, python-docx, pptxgenjs); אין שירות חיצוני לעטוף כשרת MCP. תשתמשו בסקריפטים המצורפים ובקוד שבחלק ההנחיות ישירות.

## מלכודות נפוצות
- צריך להפעיל את `get_display()` שורה-שורה בזמן הציור, מיד לפני `drawRightString()`, ולא פעם אחת על מסמך או בלוק רב-שורתי שלם. האלגוריתם הדו-כיווני אינו אידמפוטנטי: הרצה שלו על טקסט שכבר סודר מחדש הופכת את התווים פעמיים ומפיקה פלט משובש. טעות נפוצה של סוכנים היא "לעבד מראש" רשימה שלמה של שורות דרך `get_display()` ואז לקרוא לו שוב בתוך לולאת הציור.
- מחוללי PDF נוטים לכיוון טקסט LTR כברירת מחדל. מסמכים בעברית חייבים כיוון פסקה RTL, וטקסט מעורב עברית-אנגלית צריך תמיכה תקינה באלגוריתם BiDi.
- ל-DOCX (python-docx) יש מלכודת הפוכה מ-PDF: אל תריצו `get_display()` על הטקסט, Word מפעיל את אלגוריתם ה-bidi בעצמו ועיבוד מקדים הופך אותו פעמיים. שני הכשלים שמפיקים קובץ Word עברי "שבור" הם (א) הכנסת שורה שלמה מעורבת עברית/אנגלית ל-run אחד המסומן `<w:rtl/>` (האנגלית קופצת לצד הלא נכון והפיסוק זז) ו-(ב) הגדרת `w:ascii`/`w:sz` בלבד בלי גופן הסקריפט המורכב `w:cs` / גודל `w:szCs` (הגופן והגודל פשוט לא חלים על העברית). בפסקה מעורבת עברית/אנגלית לא מסמנים rtl על אף run (ה-`<w:bidi/>` של הפסקה לבדו מסדר אותה, וסימון rtl יהפוך מספרים/לטינית); rtl נשמר רק לפסקאות עבריות טהורות. מגדירים `w:cs` ו-`w:szCs` על כל run.
- run בלי כיוון מפורש יורש את כיוון הבסיס של הפסקה. אחרי ש-`add_rtl_paragraph` מוסיף פסקה עברית, הוספת run נוסף בהמשך (למשל שורת חתימה) בלי להריץ שוב את הפיצול לפי סקריפט עלולה להשאיר את ה-run בלי סימון, הגדירו את כיוונו במפורש במקום להניח שהוא יורש נכון.
- סוכנים עלולים לבחור גופנים בלי תמיכה בתווים עבריים (Arial עובד, אבל הרבה גופנים דקורטיביים לטיניים לא). תמיד תוודאו שהגופן כולל את טווח ה-Unicode העברי (U+0590-U+05FF).
- פורמט התאריך בעברית הוא DD/MM/YYYY בהקשר חילוני, ותאריכים עבריים (ט"ו באדר תשפ"ו למשל) למסמכים דתיים/מסורתיים. סוכנים עלולים ללכת ל-MM/DD/YYYY כברירת מחדל.
- מסמכים משפטיים בישראל דורשים עיצוב מסוים: לא משתמשים בניקוד בעברית עסקית/משפטית רגילה. סוכנים עלולים להוסיף ניקוד כי הם חושבים שזה משפר את הבהירות, אבל בפועל זה נראה לא מקצועי במסמכים רשמיים.

## פתרון בעיות

### שגיאה: "תווים עבריים מוצגים כריבועים או סימני שאלה"
סיבה: גופן עברי לא רשום או לא קיים במערכת
פתרון: תורידו גופן TTF עברי (Heebo מ-Google Fonts למשל), רשמו אותו עם `pdfmetrics.registerFont()` ל-reportlab, או התקינו אותו כגופן מערכת ל-WeasyPrint.

### שגיאה: "הטקסט מוצג משמאל לימין במקום מימין לשמאל"
סיבה: חסר סידור bidi או הגדרת כיוון RTL
פתרון: ב-reportlab, תפעילו `get_display()` מ-python-bidi. ב-python-docx, תבנו פסקאות עם העוזר `add_rtl_paragraph` משלב 5 (מגדיר `<w:bidi/>` על הפסקה ו-`<w:rtl/>` על ה-runs העבריים). ב-WeasyPrint, תוודאו `dir="rtl"` על אלמנט ה-HTML.

### שגיאה: "מספרים וסימני פיסוק במיקום שגוי"
סיבה: אלגוריתם הטקסט הדו-כיווני לא מטפל נכון בתוכן מעורב עברית/מספרים
פתרון: ב-reportlab, מעבירים את כל המחרוזת הלוגית דרך `get_display()` בקריאה אחת (ראו "שורות מעורבות עברית / לטינית / ספרות"). בכלים מבוססי HTML (WeasyPrint), תוודאו `unicode-bidi: isolate` על רכיבי span מוטבעים ב-LTR. ב-DOCX/python-docx עושים את ההפך מתיקון ה-PDF: לעולם לא קוראים ל-`get_display()` (Word מסדר בעצמו). מגדירים `<w:bidi/>` על הפסקה ומגדירים גופן `w:cs` וגודל `w:szCs` על כל run. בפסקה מעורבת לא מסמנים rtl על אף run; rtl רק על runs עבריים של פסקה ללא לטינית (ראו `add_rtl_paragraph` בשלב 5).

### שגיאה: "קובץ Word עברי מציג אנגלית בצד הלא נכון, או שהגופן/הגודל מתעלמים"
סיבה: כל השורה המעורבת ב-run אחד המסומן `<w:rtl/>` (האנגלית קופצת), או שה-runs מגדירים רק `w:ascii`/`w:sz` ולא את `w:cs`/`w:szCs` של הסקריפט המורכב (העברית מתעלמת מהגופן/הגודל). בדיקת נוכחות פשוטה של `<w:rtl/>` עוברת גם על קובץ שעדיין מרונדר שבור, אז תבדקו את מבנה ה-runs ולא רק את הדגל.
פתרון: השתמשו בעוזר `add_rtl_paragraph` משלב 5: פיצול runs לפי סקריפט, `w:cs` + `w:szCs` על כל run, ו-rtl רק על runs עבריים של פסקה ללא לטינית (בפסקה מעורבת אף run לא מסומן).
