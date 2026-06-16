---
name: hebrew-document-generator
description: Generate professional Hebrew documents including PDF, DOCX, and PPTX with full RTL support and proper Hebrew typography. Use when user asks to create Hebrew PDF, generate Israeli business documents, "lehafik heshbonit", "litstor hozeh", build Hebrew Word document, create Hebrew PowerPoint, or produce Israeli templates such as Heshbonit Mas (tax invoice), Hozeh (contract), Hatza'at Mechir (proposal), or Protokol (meeting minutes). Covers reportlab, WeasyPrint, python-docx, and pptxgenjs with bidi paragraph support. Do NOT use for OCR or reading existing documents (use hebrew-ocr-forms instead).
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(node:*) Bash(npm:*)
compatibility: Requires Python 3.9+ with reportlab or WeasyPrint for PDF, python-docx for DOCX. Node.js with pptxgenjs for PPTX. Hebrew fonts must be available on the system.
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
from bidi import get_display  # python-bidi 0.6.x; see note below

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
- **python-bidi import:** the canonical, recommended import is `from bidi import get_display` (top-level). The older `from bidi.algorithm import get_display` path still imports in current 0.6.x as a back-compat parallel module, but prefer the top-level one. python-bidi 0.6.x also dropped support for Python below 3.9.
- **Multi-line text:** `drawRightString()` draws a single line and does NOT wrap. For any body text longer than one line, use reportlab's `Paragraph` flowable (from `reportlab.platypus`) with a right-aligned, RTL `ParagraphStyle` instead. The bundled `scripts/generate_doc.py` uses per-line `drawRightString` for compact fixed-layout documents (invoices, receipts); it will clip long Hebrew strings. Reach for `Paragraph` / platypus flowables for contracts or any wrapping body copy.

### Mixed Hebrew / Latin / Digit Lines

The single most common RTL failure in generated documents is a line that mixes a Hebrew description with LTR numbers and a currency symbol, for example an invoice line item. `get_display()` handles the bidi reordering, but you must pass the *whole logical string* in one call so the algorithm sees the full context:

```python
from bidi import get_display

# Logical order: Hebrew description, then qty, unit price, currency
line = 'ייעוץ טכני (3 שעות) - 1,500.00 ש"ח'
c.setFont('Heebo', 11)
c.drawRightString(width - 20 * mm, y, get_display(line))
```

The digits, the comma, the period, and the parentheses all stay in their correct LTR positions because the bidi algorithm resolves them relative to the surrounding Hebrew. Do NOT split the line into pieces and reorder them yourself, and do NOT call `get_display()` on the Hebrew part only, both approaches break the number ordering.

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
- **Allocation number (Mispar Haktzaa / מספר הקצאה) under the Israel Invoices model** for a tax invoice at or above the current threshold. The threshold is being phased down (20,000 NIS in 2025, 10,000 NIS from Jan 2026, **5,000 NIS from 1 June 2026**, pre-VAT). At/above the threshold the BUYER cannot deduct the input VAT unless the seller obtained a Tax Authority allocation number and printed it on the invoice. Add an allocation-number field to any invoice template and treat the threshold as time-sensitive (verify the current figure against Rashut HaMisim).

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
- `scripts/generate_doc.py` - Generate Hebrew PDF documents with reportlab: register Hebrew fonts, apply RTL text reordering with python-bidi, produce Israeli business documents (invoices, receipts) with proper VAT calculations and NIS formatting. Run: `python scripts/generate_doc.py --help`

### References
- `references/hebrew-fonts.md` - Hebrew font catalog with recommended fonts for different document types (sans-serif, serif, monospace), Google Fonts download links, system font availability matrix, font pairing suggestions, and installation instructions for macOS, Linux, and Windows.
- `references/templates.md` - Israeli business document templates with required fields per document type (tax invoice, contract, proposal, receipt, meeting minutes), Israeli legal requirements for invoices, VAT rules, and standard Hebrew business phrasing.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| reportlab documentation | https://docs.reportlab.com/ | Canvas API, platypus flowables, font registration |
| WeasyPrint documentation | https://doc.courtbouillon.org/weasyprint/stable/ | HTML/CSS to PDF, RTL support, @font-face |
| python-docx documentation | https://python-docx.readthedocs.io/ | Document model, runs, paragraph properties |
| python-bidi (PyPI) | https://pypi.org/project/python-bidi/ | Current version, import path, changelog |
| Israeli tax invoice requirements | https://he.wikipedia.org/wiki/חשבונית_מס | Mandatory fields for a Heshbonit Mas; cross-check against current Israel Tax Authority rules |

For binding legal requirements always confirm against the current Israel Tax Authority (Rashut HaMisim) guidance, the Wikipedia entry is a starting orientation, not the authority.

## Recommended MCP Servers

No MCP server applies to this skill. Hebrew document generation runs entirely through local Python and Node libraries (reportlab, WeasyPrint, python-docx, pptxgenjs); there is no external service to wrap as an MCP server. Use the bundled scripts and the code in the Instructions section directly.

## Gotchas
- `get_display()` must be applied per line at draw time, immediately before `drawRightString()`, NOT once on a whole multi-line document or block. The bidi algorithm is not idempotent: running it on text that was already reordered double-reverses the characters and produces scrambled output. A common agent mistake is to "pre-process" a whole list of lines through `get_display()` and then call it again inside the draw loop.
- PDF generators often default to left-to-right text flow. Hebrew documents MUST use RTL paragraph direction, and mixed Hebrew-English text requires proper BiDi (bidirectional) algorithm support.
- Agents may pick fonts that lack Hebrew character support (e.g., Arial works, but many decorative Latin fonts do not). Always verify the font includes the Hebrew Unicode range (U+0590-U+05FF).
- Hebrew date formatting uses DD/MM/YYYY in secular context and Hebrew calendar dates (e.g., 15 Adar 5786) for religious/traditional documents. Agents may default to MM/DD/YYYY.
- Legal documents in Israel require specific formatting: nikud (vowel marks) is NOT used in standard business/legal Hebrew. Agents may add nikud thinking it improves clarity, but it actually looks unprofessional in formal documents.

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