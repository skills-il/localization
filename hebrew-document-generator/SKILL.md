---
name: hebrew-document-generator
description: Generate professional Hebrew documents (PDF, DOCX/Word, and PPTX) with correct right-to-left layout, mixed Hebrew-and-English bidi handling, and proper Hebrew typography. Use whenever the output is a Hebrew or mixed Hebrew/English Word document, Hebrew PDF, or Hebrew PowerPoint, including phrasings like "Hebrew Word document", "Word document in Hebrew", "מסמך Word בעברית", "create a .docx in Hebrew", "lehafik heshbonit", and "litstor hozeh", or Israeli templates such as Heshbonit Mas (tax invoice), Hozeh (contract), Hatza'at Mechir (proposal), or Protokol (meeting minutes). Prefer this over the generic docx or pdf skills ONLY when the document is Hebrew or right-to-left, because those do not set RTL/bidi and produce scrambled Hebrew with English words and punctuation in the wrong place; for English-only documents use the generic skill. Covers reportlab, WeasyPrint, python-docx, and pptxgenjs. Do NOT use for OCR or reading existing documents (use hebrew-ocr-forms instead).
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
| DOCX | python-docx | Contracts, proposals, meeting minutes | Set paragraph `bidi`; split mixed runs, set `w:cs` font + `w:rtl` on Hebrew runs only |
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

DOCX is where mixed Hebrew/English breaks most often. Word runs the Unicode bidi algorithm itself at render time, so getting it right is about emitting the correct XML flags, NOT about reordering characters yourself. Three things must all be true:

1. Every Hebrew paragraph carries `<w:bidi/>` (RTL base direction). This is what keeps the whole line ordered right-to-left and lets Word place embedded English and numbers correctly.
2. A line that mixes scripts is split into per-script runs so we can flag ONLY the Hebrew runs `<w:rtl/>` and leave the Latin runs LTR. The paragraph `<w:bidi/>` is what orders the line; the split exists to avoid the actual bug (flagging a Latin run `<w:rtl/>`, which forces RTL onto the English and makes it jump sides) and to attach complex-script styling where it belongs.
3. Every run sets the complex-script font (`w:cs`) and size (`w:szCs`). Hebrew is a "complex script" in Word's model, so `w:ascii`/`w:sz` alone never govern the Hebrew glyphs. Omitting `w:cs`/`w:szCs` is the single most common cause of "the font/size I set did nothing and the Hebrew looks broken". The same rule applies to **bold and italic**: `w:b`/`w:i` only affect Latin, you also need `w:bCs`/`w:iCs` or your bold Hebrew renders un-bolded.

```python
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# Hebrew block + Hebrew presentation forms. Used to pick each run's direction.
_HEB = re.compile(r'[֐-׿יִ-ﭏ]')

def _strong(ch):
    """True for a Hebrew letter, False for a strong-LTR letter, None for neutral."""
    if _HEB.match(ch):
        return True
    if ch.isalpha():
        return False
    return None

def _split_by_script(text):
    """Split a mixed string into (segment, is_rtl) runs.

    Each run's direction is set by its STRONG characters; neutral chars
    (spaces, digits, punctuation) attach to the current run. Leading neutrals
    inherit the direction of the first strong character in the WHOLE string
    (falling back to RTL for an all-neutral string in a Hebrew document), so a
    Latin-dominant line that starts with a digit or bracket is not mis-flagged
    RTL. Word's bidi algorithm fixes the final visual order, so this split only
    has to get the strong characters into correctly-flagged runs.
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

def add_rtl_paragraph(doc, text, font='David', size=12, bold=False, italic=False,
                      heading_level=None):
    """Add an RTL paragraph that renders mixed Hebrew/Latin/digit text correctly.

    Covers BODY paragraphs only. Table cells, headers/footers, and numbered
    lists are separate document stories: apply the same logic to each of their
    paragraphs, and add `<w:bidi/>` to the section `sectPr` for a fully RTL page.
    """
    p = doc.add_heading(level=heading_level) if heading_level else doc.add_paragraph()

    # (1) paragraph base direction = RTL
    pPr = p._p.get_or_add_pPr()
    pPr.append(pPr.makeelement(qn('w:bidi'), {}))
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for segment, is_rtl in _split_by_script(text):
        run = p.add_run(segment)
        rPr = run._r.get_or_add_rPr()
        # rPr children must stay in OOXML schema order: rFonts, b, bCs, i, iCs, sz, szCs, rtl
        rPr.append(rPr.makeelement(qn('w:rFonts'), {
            qn('w:ascii'): font, qn('w:hAnsi'): font, qn('w:cs'): font}))
        if bold:
            # bold needs BOTH w:b (Latin) and w:bCs (complex script / Hebrew)
            rPr.append(rPr.makeelement(qn('w:b'), {}))
            rPr.append(rPr.makeelement(qn('w:bCs'), {}))
        if italic:
            # italic likewise needs BOTH w:i and w:iCs for Hebrew
            rPr.append(rPr.makeelement(qn('w:i'), {}))
            rPr.append(rPr.makeelement(qn('w:iCs'), {}))
        # (3) complex-script font size, so the size applies to Hebrew
        rPr.append(rPr.makeelement(qn('w:sz'),   {qn('w:val'): str(size * 2)}))
        rPr.append(rPr.makeelement(qn('w:szCs'), {qn('w:val'): str(size * 2)}))
        # (2) mark ONLY Hebrew runs rtl; Latin runs stay LTR
        if is_rtl:
            rPr.append(rPr.makeelement(qn('w:rtl'), {}))
    return p

doc = Document()
doc.styles['Normal'].font.name = 'David'
doc.styles['Normal'].font.size = Pt(12)

add_rtl_paragraph(doc, 'חוזה שירותים', size=18, bold=True, heading_level=1)
add_rtl_paragraph(doc, 'ההסכם נחתם בין חברת Acme בע"מ לבין הלקוח (גרסה 2).')

doc.save('contract.docx')
```

**Do NOT call `get_display()` on DOCX text.** Unlike reportlab (which draws pre-positioned glyphs and therefore needs python-bidi to reorder them), Word applies the bidi algorithm itself. Pre-shaping a string with `get_display()` and then handing it to python-docx double-applies the algorithm and scrambles the result. `get_display()` belongs to the PDF path only.

This helper covers body paragraphs. **Tables, headers/footers, and numbered/bulleted lists** are separate document stories the helper does not reach: apply the same `<w:bidi/>` + per-script-run logic to each of their paragraphs, and add `<w:bidi/>` to the section `sectPr` for full RTL page flow.

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
Result: Use python-docx with the `add_rtl_paragraph` helper (Step 5): `<w:bidi/>` paragraphs, per-script run splitting so embedded English/numbers stay in place, `w:cs` font + `w:szCs` size, David font, RTL alignment, structured sections (parties, scope, payment terms, termination, signatures), proper Hebrew legal phrasing.

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
- DOCX (python-docx) has the opposite trap from PDF: do NOT run `get_display()` on the text, Word applies the bidi algorithm itself and pre-shaping double-reverses it. The two failure modes that produce "broken" Hebrew Word files are (a) putting a whole mixed Hebrew/English line in ONE run flagged `<w:rtl/>` (the English jumps sides and punctuation reflows) and (b) setting only `w:ascii`/`w:sz` and never the complex-script `w:cs` font / `w:szCs` size (your font and size silently never apply to the Hebrew). Split mixed lines per script, flag only Hebrew runs rtl, and set `w:cs` + `w:szCs` on every run.
- A run with no explicit direction inherits the paragraph base direction. After `add_rtl_paragraph` adds a Hebrew paragraph, appending another run later (e.g. a signature line) without re-running the per-script split can leave that run unmarked, set its direction explicitly rather than assuming it inherits correctly.
- Agents may pick fonts that lack Hebrew character support (e.g., Arial works, but many decorative Latin fonts do not). Always verify the font includes the Hebrew Unicode range (U+0590-U+05FF).
- Hebrew date formatting uses DD/MM/YYYY in secular context and Hebrew calendar dates (e.g., 15 Adar 5786) for religious/traditional documents. Agents may default to MM/DD/YYYY.
- Legal documents in Israel require specific formatting: nikud (vowel marks) is NOT used in standard business/legal Hebrew. Agents may add nikud thinking it improves clarity, but it actually looks unprofessional in formal documents.

## Troubleshooting

### Error: "Hebrew characters display as boxes or question marks"
Cause: Hebrew font not registered or not found on system
Solution: Download a Hebrew TTF font (e.g., Heebo from Google Fonts), register it with `pdfmetrics.registerFont()` for reportlab, or install it as a system font for WeasyPrint.

### Error: "Text appears left-to-right instead of right-to-left"
Cause: Missing bidi reordering or RTL direction setting
Solution: For reportlab, apply `get_display()` from python-bidi. For python-docx, build paragraphs with the `add_rtl_paragraph` helper in Step 5 (sets `<w:bidi/>` on the paragraph and `<w:rtl/>` on the Hebrew runs). For WeasyPrint, ensure `dir="rtl"` on the HTML element.

### Error: "Numbers and punctuation in wrong position"
Cause: Bidirectional text algorithm not handling mixed Hebrew/number content
Solution: For reportlab, pass the whole logical string through `get_display()` in one call (see "Mixed Hebrew / Latin / Digit Lines"). In HTML-based tools (WeasyPrint), ensure proper `unicode-bidi: isolate` on embedded LTR spans. For DOCX/python-docx, do the OPPOSITE of the PDF fix: never call `get_display()` (Word reorders itself). Set `<w:bidi/>` on the paragraph, split the line into per-script runs, flag only the Hebrew runs `<w:rtl/>`, and set the `w:cs` font + `w:szCs` size on every run (see Step 5's `add_rtl_paragraph`).

### Error: "Hebrew Word (.docx) renders with English on the wrong side, or my font/size is ignored"
Cause: The whole mixed line is in one run marked `<w:rtl/>` (English jumps), or the runs set only `w:ascii`/`w:sz` and never the complex-script `w:cs`/`w:szCs` (Hebrew ignores the font/size). A bare presence check for `<w:rtl/>` passes on a file that still renders broken, so verify the run structure, not just the flag.
Solution: Use the `add_rtl_paragraph` helper in Step 5: per-script run splitting, rtl on Hebrew runs only, `w:cs` + `w:szCs` on every run.