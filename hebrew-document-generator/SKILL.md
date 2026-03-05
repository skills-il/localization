---
name: hebrew-document-generator
description: >-
  Generate professional Hebrew documents including PDF, DOCX, and PPTX with
  full RTL support and proper Hebrew typography. Use when user asks to create
  Hebrew PDF, generate Israeli business documents, "lehafik heshbonit",
  "litstor hozeh", build Hebrew Word document, create Hebrew PowerPoint, or
  produce Israeli templates such as Heshbonit Mas (tax invoice), Hozeh
  (contract), Hatza'at Mechir (proposal), or Protokol (meeting minutes).
  Covers reportlab, WeasyPrint, python-docx, and pptxgenjs with bidi
  paragraph support. Do NOT use for OCR or reading existing documents (use
  hebrew-ocr-forms instead).
license: MIT
allowed-tools: 'Bash(python:*) Bash(pip:*) Bash(node:*) Bash(npm:*)'
compatibility: >-
  Requires Python 3.9+ with reportlab or WeasyPrint for PDF, python-docx for
  DOCX. Node.js with pptxgenjs for PPTX. Hebrew fonts must be available on
  the system.
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags:
    he:
      - מסמכים
      - עברית
      - PDF
      - RTL
      - חשבונית
      - חוזה
      - ישראל
    en:
      - documents
      - hebrew
      - pdf
      - rtl
      - invoice
      - contract
      - israel
  display_name:
    he: מחולל מסמכים בעברית
    en: Hebrew Document Generator
  display_description:
    he: יצירת מסמכים עסקיים בעברית בפורמטים PDF, DOCX ו-PPTX עם תמיכה מלאה ב-RTL
    en: >-
      Generate professional Hebrew documents including PDF, DOCX, and PPTX
      with full RTL support and proper Hebrew typography. Use when user asks
      to create Hebrew PDF, generate Israeli business documents, "lehafik
      heshbonit", "litstor hozeh", build Hebrew Word document, create Hebrew
      PowerPoint, or produce Israeli templates such as Heshbonit Mas (tax
      invoice), Hozeh (contract), Hatza'at Mechir (proposal), or Protokol
      (meeting minutes). Covers reportlab, WeasyPrint, python-docx, and
      pptxgenjs with bidi paragraph support. Do NOT use for OCR or reading
      existing documents (use hebrew-ocr-forms instead).
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
---

# Hebrew Document Generator

## Instructions

### Step 1: Choose the Output Format

| Format | Library | Best For | RTL Support |
|--------|---------|----------|-------------|
| PDF | reportlab | Invoices, tax docs, printable forms | Register Hebrew font, use `canvas.drawRightString()` |
| PDF | WeasyPrint | Styled documents from HTML/CSS | Native via `dir="rtl"` in HTML |
| DOCX | python-docx | Contracts, proposals, meeting minutes | Set paragraph `bidi` and RTL run properties |
| PPTX | pptxgenjs (Node) | Presentations, slide decks | RTL text boxes with `rtlMode: true` |

### Step 2: Install Dependencies and Hebrew Fonts

**Python PDF generation:**
```bash
pip install reportlab weasyprint
```

**Python DOCX generation:**
```bash
pip install python-docx python-bidi
```

**Node.js PPTX generation:**
```bash
npm install pptxgenjs
```

**Recommended Hebrew fonts (install on system):**

| Font | Style | Best For | Source |
|------|-------|----------|--------|
| Heebo | Sans-serif, modern | Web-style documents, invoices | Google Fonts |
| David | Classic serif | Legal contracts, formal letters | System (Windows/macOS) |
| Narkisim | Serif, elegant | Proposals, invitations | System (Windows) |
| Frank Ruehl | Traditional serif | Academic, literary | Google Fonts (Frank Ruhl Libre) |
| Rubik | Sans-serif, rounded | Presentations, marketing | Google Fonts |
| Assistant | Sans-serif, clean | Business correspondence | Google Fonts |

See `references/hebrew-fonts.md` for download links and installation instructions.

### Step 3: Generate Hebrew PDF with reportlab

See `scripts/generate_doc.py` for the full generation pipeline.

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from bidi.algorithm import get_display

# Register Hebrew font
pdfmetrics.registerFont(TTFont('Heebo', 'Heebo-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Heebo-Bold', 'Heebo-Bold.ttf'))

def create_hebrew_pdf(filename, title, content_lines):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title -- right-aligned for RTL
    c.setFont('Heebo-Bold', 18)
    hebrew_title = get_display(title)
    c.drawRightString(width - 20*mm, height - 30*mm, hebrew_title)

    # Body lines
    c.setFont('Heebo', 12)
    y = height - 50*mm
    for line in content_lines:
        display_line = get_display(line)
        c.drawRightString(width - 20*mm, y, display_line)
        y -= 7*mm

    c.save()
```

Key points for reportlab Hebrew:
- Always use `get_display()` from python-bidi to reorder characters
- Use `drawRightString()` for right-aligned RTL text
- Register TTF Hebrew fonts explicitly -- reportlab has no built-in Hebrew support
- Set line height to at least 1.5x font size for Hebrew readability

### Step 4: Generate Hebrew PDF with WeasyPrint

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
  <!-- Document content here -->
</body>
</html>
"""

HTML(string=html_content).write_pdf('invoice.pdf')
```

WeasyPrint advantages for Hebrew:
- Full CSS support including logical properties
- Native RTL via HTML `dir` attribute
- Tables render correctly in RTL
- Supports `@font-face` for custom Hebrew fonts

### Step 5: Generate Hebrew DOCX with python-docx

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_paragraph_rtl(paragraph):
    """Set paragraph direction to RTL for Hebrew text."""
    pPr = paragraph._p.get_or_add_pPr()
    bidi = pPr.makeelement(qn('w:bidi'), {})
    pPr.append(bidi)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def set_run_rtl(run):
    """Set run direction to RTL."""
    rPr = run._r.get_or_add_rPr()
    rtl = rPr.makeelement(qn('w:rtl'), {})
    rPr.append(rtl)

doc = Document()
# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'David'
font.size = Pt(12)

# Add Hebrew heading
heading = doc.add_heading(level=1)
run = heading.add_run('חוזה שירותים')
set_run_rtl(run)
set_paragraph_rtl(heading)

# Add Hebrew paragraph
para = doc.add_paragraph()
run = para.add_run('הסכם זה נערך ונחתם ביום...')
run.font.name = 'David'
run.font.size = Pt(12)
set_run_rtl(run)
set_paragraph_rtl(para)

doc.save('contract.docx')
```

### Step 6: Generate Hebrew PPTX with pptxgenjs

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

pptx.layout = 'LAYOUT_16x9';
pptx.rtlMode = true;

const slide = pptx.addSlide();

// Hebrew title
slide.addText('סקירה רבעונית', {
  x: 0.5, y: 0.5, w: '90%', h: 1.0,
  fontSize: 28,
  fontFace: 'Heebo',
  color: '1a1a2e',
  align: 'right',
  rtlMode: true,
  bold: true,
});

// Hebrew bullet points
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

### Step 7: Israeli Business Document Templates

See `references/templates.md` for complete field specifications per document type.

| Template | Hebrew Name | Required Fields |
|----------|-------------|-----------------|
| Tax Invoice | חשבונית מס | Business name, Osek Murshe number, date, line items, VAT (18%), total |
| Contract | חוזה | Parties, TZ/company numbers, terms, signatures, date |
| Price Proposal | הצעת מחיר | Business details, itemized pricing, validity period, terms |
| Meeting Minutes | פרוטוקול | Date, attendees, agenda, decisions, action items |
| Receipt | קבלה | Business name, receipt number, amount, payment method, date |

**Tax Invoice (Heshbonit Mas) required fields by Israeli law:**
- Business name and address
- Osek Murshe (authorized dealer) number
- Sequential invoice number
- Date of issue
- Customer name and TZ/company number
- Line items with description, quantity, unit price
- Subtotal, VAT at 18%, and total in NIS

## Examples

### Example 1: Generate Tax Invoice PDF
User says: "Create a Hebrew tax invoice PDF for my business"
Result: Use reportlab or WeasyPrint to generate A4 PDF with RTL layout, business header, sequential invoice number, itemized table, VAT calculation at 18%, totals in NIS with shekel symbol, and Hebrew font throughout.

### Example 2: Create Hebrew Contract DOCX
User says: "Draft a Hebrew service contract as a Word document"
Result: Use python-docx with bidi paragraph support, David font, RTL alignment, structured sections (parties, scope, payment terms, termination, signatures), proper Hebrew legal phrasing.

### Example 3: Build Hebrew Presentation
User says: "Make a Hebrew PowerPoint for our quarterly review"
Result: Use pptxgenjs with rtlMode enabled, Heebo font, right-aligned text boxes, RTL bullet points, Hebrew slide titles, and professional layout.

### Example 4: Batch Document Generation
User says: "Generate 50 Hebrew invoices from a CSV file"
Result: Read CSV data, iterate rows, use `scripts/generate_doc.py` to produce individual PDFs with unique invoice numbers, customer details, and line items per row.

## Bundled Resources

### Scripts
- `scripts/generate_doc.py` — Generate Hebrew PDF documents with reportlab: register Hebrew fonts, apply RTL text reordering with python-bidi, produce Israeli business documents (invoices, receipts) with proper VAT calculations and NIS formatting. Run: `python scripts/generate_doc.py --help`

### References
- `references/hebrew-fonts.md` — Hebrew font catalog with recommended fonts for different document types (sans-serif, serif, monospace), Google Fonts download links, system font availability matrix, font pairing suggestions, and installation instructions for macOS, Linux, and Windows.
- `references/templates.md` — Israeli business document templates with required fields per document type (tax invoice, contract, proposal, receipt, meeting minutes), Israeli legal requirements for invoices, VAT rules, and standard Hebrew business phrasing.

## Troubleshooting

### Error: "Hebrew characters display as boxes or question marks"
Cause: Hebrew font not registered or not found on system
Solution: Download a Hebrew TTF font (e.g., Heebo from Google Fonts), register it with `pdfmetrics.registerFont()` for reportlab, or install it as a system font for WeasyPrint.

### Error: "Text appears left-to-right instead of right-to-left"
Cause: Missing bidi reordering or RTL direction setting
Solution: For reportlab, apply `get_display()` from python-bidi. For python-docx, call `set_paragraph_rtl()` and `set_run_rtl()`. For WeasyPrint, ensure `dir="rtl"` on the HTML element.

### Error: "Numbers and punctuation in wrong position"
Cause: Bidirectional text algorithm not handling mixed Hebrew/number content
Solution: Wrap numeric sequences in LTR marks. In reportlab, use `get_display()` with `base_dir='R'`. In HTML-based tools, ensure proper `unicode-bidi: isolate` on embedded LTR spans.