---
name: hebrew-document-generator
description: Not legal advice. Generate Hebrew documents (PDF, DOCX/Word, PPTX) with correct RTL layout, mixed Hebrew-and-English bidi handling, and Hebrew typography. Use whenever the output is a Hebrew or mixed Hebrew/English Word document, Hebrew PDF, or Hebrew PowerPoint ("Hebrew Word document", "מסמך Word בעברית", "create a .docx in Hebrew"), or Israeli templates like Heshbonit Mas, Hozeh, or Protokol. ALSO use this for the symptom where a Hebrew document looks fine on screen or in Claude but comes out scrambled, reversed, or broken in Word, with English, numbers, or punctuation on the wrong side ("Hebrew text reversed in Word", "fix Hebrew formatting in Word"); the fix is regenerating the .docx with paragraph-level RTL/bidi, NOT a web/CSS RTL change. Prefer over the generic docx/pdf skills ONLY when the document is Hebrew or RTL; for English-only docs use the generic skill. Covers reportlab, WeasyPrint, python-docx, pptxgenjs. Do NOT use for OCR or reading existing documents (use hebrew-ocr-forms).
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(node:*) Bash(npm:*)
compatibility: Requires Python 3.9+ with reportlab or WeasyPrint for PDF, python-docx for DOCX. Node.js with pptxgenjs for PPTX. Hebrew fonts must be available on the system.
---

# Hebrew Document Generator

## Legal notice

This is a free information tool operated by an AI model. It lays out and formats Hebrew documents (PDF, Word and PowerPoint) from the content you supply, and shows the customary section and field structure for a contract, invoice, receipt and price proposal. All of its output is produced automatically by an AI model, without the involvement, review or approval of a lawyer, tax advisor or accountant. The output is not legal advice, not a legal opinion and not a document prepared by a lawyer; it is a layout template that you fill in and adapt yourself. The tool does not examine the circumstances of your transaction, does not assess whether any clause is valid or enforceable, and does not adapt the clauses to the law that applies to you. An AI model may err, omit information or reach a wrong conclusion.

Any contract, letter or other text this skill drafts is an automatic draft for personal organization only. It is not a document prepared by a lawyer, and it must not be relied on as evidence. The invoice and receipt samples are layout examples, not issued tax documents. Responsibility for reporting and paying tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those the law permits. It does not replace advice that considers each person's specific facts and needs: before taking a legal step, signing a document, or filing one with an authority or a court, consult a lawyer. Any use of the output is at the user's sole responsibility.

## Instructions

### Step 1: Choose the Output Format

| Format | Library | Best For | RTL Support |
|--------|---------|----------|-------------|
| PDF | reportlab | Invoices, tax docs, printable forms | Register Hebrew font, use `canvas.drawRightString()` |
| PDF | WeasyPrint | Styled documents from HTML/CSS | Native via `dir="rtl"` in HTML |
| DOCX | python-docx | Contracts, proposals, meeting minutes | `scripts/docx_rtl.py`: paragraph `bidi`, runs split by script, `w:rtl` on Hebrew runs only, `w:cs` font on every run |
| PPTX | pptxgenjs (Node) | Presentations, slide decks | RTL text boxes with `rtlMode: true` |

### Step 2: Install Dependencies and Hebrew Fonts

**Python PDF generation:**
```bash
pip install reportlab weasyprint python-bidi
```

WeasyPrint also needs the Pango system library. The simplest route on macOS is `brew install weasyprint`; on Debian or Ubuntu install `libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0` before `pip install`. A missing library fails with `cannot load library 'libgobject-2.0-0'`; on macOS with Homebrew Pango already installed, `export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` fixes it.

**Python DOCX generation:**
```bash
pip install python-docx
```

**Node.js PPTX generation:**
```bash
npm install pptxgenjs
```

**Recommended Hebrew fonts (install on system):**

| Font | Style | Best For | Source |
|------|-------|----------|--------|
| Heebo | Sans-serif, modern | Web-style documents, invoices | Google Fonts |
| David | Classic serif | Legal contracts, formal letters | System (Windows; macOS with Microsoft Office) |
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
from bidi.algorithm import get_display  # NOT `from bidi import get_display`, see below

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
- **python-bidi import, use `from bidi.algorithm import get_display`.** python-bidi 0.6.x ships two implementations. `bidi.algorithm` is the pure-Python one, compatible with earlier versions, and it mirrors brackets. The top-level `from bidi import get_display` wraps a Rust crate that skips the mirroring rule (upstream issue #25), so `(18%)` prints as `)18%(` in a reportlab PDF, and every parenthesis in a Hebrew line comes out backwards. python-bidi 0.6.x requires Python 3.9+.
- **Multi-line text:** `drawRightString()` draws a single line and does NOT wrap. Do not hand `get_display()` output to a reportlab `Paragraph`: it wraps the already-reversed string, so the LAST sentence lands on the top line, and `wordWrap='RTL'` without bidi prints every word's letters backwards. Wrap in LOGICAL order first, then run `get_display()` on each finished line: `wrap_hebrew_lines()` / `draw_hebrew_paragraph()` in `scripts/generate_doc.py` do this. For long flowing documents (contracts), WeasyPrint (Step 4) wraps Hebrew natively.

### Mixed Hebrew / Latin / Digit Lines

The single most common RTL failure in generated documents is a line that mixes a Hebrew description with LTR numbers and a currency symbol, for example an invoice line item. `get_display()` handles the bidi reordering, but you must pass the *whole logical string* in one call so the algorithm sees the full context:

```python
from bidi.algorithm import get_display

# Logical order: Hebrew description, then qty, unit price, currency
line = 'ייעוץ טכני (3 שעות) - 1,500.00 ש"ח'
c.setFont('Heebo', 11)
c.drawRightString(width - 20 * mm, y, get_display(line))
```

The digits, the comma, the period, and the parentheses all land correctly because the bidi algorithm resolves them relative to the surrounding Hebrew (and `bidi.algorithm` mirrors the parentheses). Do NOT split the line into pieces and reorder them yourself, and do NOT call `get_display()` on the Hebrew part only, both approaches break the number ordering.

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

# base_url is required: without it the relative font URL is silently ignored
# and a fallback font (no Hebrew on many Linux servers) is embedded instead.
HTML(string=html_content, base_url='.').write_pdf('invoice.pdf')
```

WeasyPrint advantages for Hebrew:
- Supports CSS logical properties
- Native RTL via HTML `dir` attribute
- Tables render correctly in RTL
- Supports `@font-face` for custom Hebrew fonts

### Step 5: Generate Hebrew DOCX with python-docx

DOCX is where mixed Hebrew/English breaks most often. Microsoft Word's bidi handling differs from LibreOffice, macOS Preview/Quick Look and most viewers, which render forgiving output that HIDES Word-only bugs, so verify in Word itself. Use the bundled `scripts/docx_rtl.py` (copy it next to your code or import it); it implements these rules:

1. **Paragraph direction:** a line with any Hebrew gets `<w:bidi/>` (RTL base) and **no explicit alignment**. `w:jc` is logical, so `jc=right` on an RTL paragraph means the line END, which Word draws on the visual LEFT. An RTL paragraph with no `jc` starts at the visual right. A pure-English line gets LTR base and left alignment.
2. **Runs split by script, `<w:rtl/>` on the Hebrew runs, never on Latin or digit runs.** Without `<w:rtl/>` on its Hebrew runs, Word lays the runs of a mixed line out left to right: `ההסכם נחתם בין חברת Acme בע"מ` comes out with its phrases in reverse order. With a Latin word or a number INSIDE an rtl-flagged run, Word reverses it (`7/2023` becomes `2023/7`). So digits form their own LTR runs, separators between digits (`1,500.00`, `03-1234567`) and `%`/currency signs stay with the number, a number after a Latin word (`KI-67`) joins it, a leading `+`/`-` sign joins its number (`+972-3-1234567`), and brackets and punctuation between the two scripts go to the Hebrew side, so `(גרסה 2).` keeps its closing bracket and period in place. The exception is a bracket pair around Latin text right after a Latin word (`Acme (Israel)`, `Office (365)`): it stays with the Latin run, or Word mirrors the closing bracket into the Hebrew run. Letters are classified by their Unicode bidi class, so accented Latin (`Nestlé`) stays one word. A leading list marker (`2.`, `10.`) is merged into the Hebrew run so the period does not flip to `.2`.
3. **Complex-script properties on every run:** `w:cs` font and `w:szCs` size (Word applies `w:ascii`/`w:sz` only to Latin text), and `w:bCs`/`w:iCs` alongside `w:b`/`w:i`. Omitting `w:cs`/`w:szCs` is the classic "the font/size I set did nothing" bug.
4. **Never insert Unicode directional marks or isolates** (U+200E, U+2066-2069): Word draws them as visible boxes in the David font.

```python
import sys
sys.path.insert(0, 'scripts')  # wherever docx_rtl.py lives
from docx_rtl import new_hebrew_document, add_rtl_paragraph, add_rtl_table

doc = new_hebrew_document(font='David', size=12)   # also sets <w:bidi/> on the section
add_rtl_paragraph(doc, 'חוזה שירותים', size=18, bold=True)
add_rtl_paragraph(doc, 'ההסכם נחתם ביום 13/01/2026 בין חברת Acme בע"מ לבין הלקוח (גרסה 2).')
add_rtl_paragraph(doc, '2. תמורה', bold=True)
add_rtl_table(doc, ['תיאור', 'כמות', 'מחיר', 'סה"כ'],
              [['ייעוץ טכני (3 שעות)', 1, '1,500.00', '1,500.00'],
               ['פיתוח Acme', 2, '600.00', '1,200.00']])
doc.save('contract.docx')
```

`python scripts/docx_rtl.py --output sample.docx` writes a sample that exercises every rule. All of the above was checked against Microsoft Word's own rendering (Word 16.113 for Mac, exported to PDF by Word itself).

**Do NOT call `get_display()` on DOCX text.** Word runs the bidi algorithm itself, so pre-shaping double-applies it and scrambles the line. `get_display()` belongs to the reportlab path only.

**Headers, footers and numbered lists** are separate document stories: fill their paragraphs with the same logic (the module's `_fill_paragraph(p, text, font, size)` works on any paragraph object, e.g. `section.footer.paragraphs[0]`).

### Hebrew Tables in DOCX (the "table comes out reversed" fix)

A reversed table (first logical column, e.g. `תיאור`, on the LEFT) is a **column-order** bug, not a text-direction one. python-docx tables have no `<w:bidiVisual/>`, so Word lays columns out left to right. A Hebrew table needs BOTH fixes, and `add_rtl_table` applies both:

1. **Column order:** `table.table_direction = WD_TABLE_DIRECTION.RTL` emits `<w:bidiVisual/>`, drawing the first logical column on the right. `table.alignment = WD_TABLE_ALIGNMENT.RIGHT` makes the table block hug the right margin.
2. **Cell text:** each cell is its own paragraph, so it gets `<w:bidi/>` and the per-script runs from rule 2, with NO explicit alignment. Setting a "right" alignment on RTL cells pushes Hebrew to the visual LEFT while number cells stay right (the v1.7.0 bug).

Keep header and row data in logical order; reversing the column lists yourself double-reverses once `bidiVisual` is set. For an **invoice totals block** the label cell usually spans columns via `row.cells[a].merge(row.cells[b])`; a merged span can land on the wrong side under `bidiVisual`, so check the merged row in Word.

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
  lang: 'he-IL',   // default is en-US: PowerPoint would spell-check the Hebrew as English
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
  lang: 'he-IL',
});

pptx.writeFile({ fileName: 'quarterly-review.pptx' });
```

**PPTX tables** have the same RTL column-order concern as DOCX. pptxgenjs renders table columns in the order of your `rows` array, it does not auto-mirror for RTL. So that the first logical column reads on the right, reverse the cell order per row in your data, and set `rtlMode: true` (plus `align: 'right'`) on every cell's `options` so the text inside each cell is right-aligned and bidi-handled:

```javascript
// Logical columns: תיאור | כמות | מחיר. Reverse per row so col 1 displays on the right
const headers = ['תיאור', 'כמות', 'מחיר'];
const dataRows = [['ייעוץ', '1', '1,500.00']];
const opt = { rtlMode: true, align: 'right', fontFace: 'Heebo', lang: 'he-IL' };
const tableRows = [headers, ...dataRows].map(
  row => [...row].reverse().map(text => ({ text, options: opt }))
);
slide.addTable(tableRows, { x: 0.5, y: 1.5, w: 9 });  // rtlMode is a per-cell text option, not a table option
```

Note the opposite convention from DOCX: python-docx exposes a real `bidiVisual` column-flip (`table_direction = RTL`) so you keep data in logical order, whereas pptxgenjs has no such flag, so you reverse the columns in the data yourself. Verify the rendered slide.

### Step 7: Israeli Business Document Templates

See `references/templates.md` for the field list of each document type.

| Template | Hebrew Name | Core Fields |
|----------|-------------|-------------|
| Tax Invoice | חשבונית מס | The words "חשבונית מס" and "עוסק מורשה", business name, address and osek number, serial number, date, transaction details, price before VAT, VAT (18%) and total, "מקור" on the original |
| Contract | חוזה | Parties, TZ/company numbers, terms, signatures, date |
| Price Proposal | הצעת מחיר | Business details, itemized pricing, validity period, terms |
| Meeting Minutes | פרוטוקול | Date, attendees, agenda, decisions, action items |
| Receipt | קבלה | Business name, receipt number, amount, payment method, date |

**Ask which document the user actually needs before producing an "invoice".** An **עוסק פטור** does not charge VAT and may not issue a חשבונית מס or a חשבונית מס/קבלה; it issues a קבלה when paid. An **עוסק מורשה** issues a חשבונית עסקה or a חשבונית מס, a קבלה on payment, or a combined חשבונית מס/קבלה only when payment is received at the time of the transaction. A חשבון עסקה (payment request) is a free-form document with no reporting obligation.

**Allocation number (מספר הקצאה, Israel Invoices model):** from 1 June 2026 it is required on a tax invoice for a transaction above 5,000 NIS before VAT (it was 20,000 NIS in 2025 and 10,000 NIS from 1 January 2026) when the buyer is an עוסק מורשה who asks for one; without it the buyer cannot deduct the input VAT. The threshold keeps moving, so treat it as time-sensitive.

**The bundled samples are layouts, not issued documents.** A real tax invoice is printed from a pre-printed book or from authorized invoicing software, in an original and a copy, and allocation numbers come from the Tax Authority. Use the samples to get Hebrew layout right, and point a user who needs to issue invoices to invoicing software (see the `green-invoice` skill).

## Examples

### Example 1: Generate Tax Invoice PDF
User says: "Create a Hebrew tax invoice PDF for my business"
Result: First ask whether the business is an עוסק מורשה or עוסק פטור and whether payment was already received (Step 7), then build an A4 PDF with reportlab or WeasyPrint: business header with the required words, serial number, itemized table, VAT at 18%, totals in NIS, an allocation-number field, and a note that the file is a layout sample rather than an issued tax invoice.

### Example 2: Create Hebrew Contract DOCX
User says: "Draft a Hebrew service contract as a Word document"
Result: Use `scripts/docx_rtl.py` (Step 5): `<w:bidi/>` paragraphs with no explicit alignment, per-script runs with `<w:rtl/>` on the Hebrew runs so embedded English and numbers stay in place, `w:cs` font and `w:szCs` size, David font, and structured sections (parties, scope, payment terms, termination, signatures). Present it as a draft per the Legal notice.

### Example 3: Build Hebrew Presentation
User says: "Make a Hebrew PowerPoint for our quarterly review"
Result: Use pptxgenjs with `rtlMode` and `lang: 'he-IL'` on every text box, Heebo font, right-aligned text, RTL bullet points, and reversed column order in tables.

### Example 4: Batch Document Generation
User says: "Generate 50 Hebrew invoice PDFs from a CSV file"
Result: `scripts/generate_doc.py` has no CSV input. Import its `generate_invoice(filename, font_name, business_info)` and `register_hebrew_font()` and loop over the rows, or copy its drawing helpers into your own loop. It draws one page with no page breaks, so split long item lists yourself. For documents that must be legally issued, route to invoicing software (Step 7).

## Bundled Resources

### Scripts
- `scripts/generate_doc.py` - Sample Hebrew invoice and receipt PDFs with reportlab: Hebrew font registration with a glyph check (auto-detects a Hebrew system font, exits with code 2 instead of printing boxes), bracket-safe bidi reordering, logical-order line wrapping, VAT at 18%. Run: `python scripts/generate_doc.py --help`
- `scripts/docx_rtl.py` - Word-safe Hebrew paragraphs, tables and RTL sections for python-docx (Step 5). Import it, or run `python scripts/docx_rtl.py --output sample.docx`.

### References
- `references/hebrew-fonts.md` - Hebrew font catalog with recommended fonts for different document types (sans-serif, serif, monospace), Google Fonts download links, system font availability matrix, font pairing suggestions, and installation instructions for macOS, Linux, and Windows.
- `references/templates.md` - Israeli business document templates: the required fields of a tax invoice, which document each type of business issues, and customary fields for contracts, proposals, receipts and meeting minutes, VAT rules, and standard Hebrew business phrasing.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| reportlab documentation | https://docs.reportlab.com/ | Canvas API, platypus flowables, font registration |
| WeasyPrint documentation | https://doc.courtbouillon.org/weasyprint/stable/ | HTML/CSS to PDF, RTL support, @font-face |
| python-docx documentation | https://python-docx.readthedocs.io/ | Document model, runs, paragraph properties |
| python-bidi (PyPI) | https://pypi.org/project/python-bidi/ | Current version, import path, changelog |
| Kol Zchut: tax invoice, transaction invoice and receipt | https://www.kolzchut.org.il/he/הוצאת_חשבונית_מס,_חשבונית_עסקה_וקבלה | Required fields, who may issue which document |
| Israel Tax Authority: allocation-number threshold | https://www.gov.il/he/pages/pa240525-1 | Current Israel Invoices threshold |

## Recommended MCP Servers

No MCP server applies to this skill. Hebrew document generation runs entirely through local Python and Node libraries (reportlab, WeasyPrint, python-docx, pptxgenjs); there is no external service to wrap as an MCP server. Use the bundled scripts and the code in the Instructions section directly.

## Gotchas
- `get_display()` must be applied per line at draw time, immediately before `drawRightString()`, NOT once on a whole multi-line document or block. The bidi algorithm is not idempotent: running it on text that was already reordered double-reverses the characters and produces scrambled output. A common agent mistake is to "pre-process" a whole list of lines through `get_display()` and then call it again inside the draw loop.
- PDF generators often default to left-to-right text flow. Hebrew documents MUST use RTL paragraph direction, and mixed Hebrew-English text requires proper BiDi (bidirectional) algorithm support.
- DOCX (python-docx) has the opposite trap from PDF: do NOT run `get_display()` on the text, Word applies the bidi algorithm itself. The failure modes that produce "broken" Hebrew Word files are (a) a whole mixed line in ONE run flagged `<w:rtl/>` (numbers and English reverse), (b) mixed lines with NO `<w:rtl/>` on the Hebrew runs (the phrases come out in reverse order), (c) `jc=right` on RTL paragraphs (left-aligned text), and (d) no complex-script `w:cs` font / `w:szCs` size (your font and size never apply to the Hebrew). `scripts/docx_rtl.py` avoids all four.
- In a reportlab PDF, `from bidi import get_display` (the Rust implementation) does not mirror brackets, so every `(...)` in Hebrew prints reversed. Import from `bidi.algorithm`.
- Appending a run to an existing Hebrew paragraph by hand (e.g. a signature line) skips the per-script split and the `<w:rtl/>` flag. Build the whole line with `add_rtl_paragraph` instead.
- A reversed Hebrew DOCX *table* (first column on the left) is a COLUMN-ORDER bug, not a text-direction one. `add_rtl_paragraph` and per-cell bidi do nothing about it: python-docx tables have no `<w:bidiVisual/>`, so Word lays columns out LTR. Set `table.table_direction = WD_TABLE_DIRECTION.RTL` on the table AND run each cell through the per-cell bidi helper, you need both (see "Hebrew Tables in DOCX"). Keep your column data in logical order, reversing it yourself double-reverses once `bidiVisual` is set.
- Agents may pick fonts that lack Hebrew character support (e.g., Arial works, but many decorative Latin fonts do not). Always verify the font includes the Hebrew Unicode range (U+0590-U+05FF).
- Hebrew date formatting uses DD/MM/YYYY in secular context and Hebrew calendar dates (e.g., 15 Adar 5786) for religious/traditional documents. Agents may default to MM/DD/YYYY.
- Legal documents in Israel require specific formatting: nikud (vowel marks) is NOT used in standard business/legal Hebrew. Agents may add nikud thinking it improves clarity, but it actually looks unprofessional in formal documents.

## Troubleshooting

### Error: "Hebrew characters display as boxes or question marks"
Cause: Hebrew font not registered or not found on system
Solution: Download a Hebrew TTF font (e.g., Heebo from Google Fonts), register it with `pdfmetrics.registerFont()` for reportlab, or install it as a system font for WeasyPrint.

### Error: "Text appears left-to-right instead of right-to-left"
Cause: Missing bidi reordering or RTL direction setting
Solution: For reportlab, apply `get_display()` from `bidi.algorithm`. For python-docx, build paragraphs with `scripts/docx_rtl.py` (sets `<w:bidi/>` on the paragraph and `<w:rtl/>` on the Hebrew runs). For WeasyPrint, ensure `dir="rtl"` on the HTML element.

### Error: "Numbers and punctuation in wrong position"
Cause: Bidirectional text algorithm not handling mixed Hebrew/number content
Solution: For reportlab, pass the whole logical string through `get_display()` from `bidi.algorithm` in one call (see "Mixed Hebrew / Latin / Digit Lines"); parentheses that come out as `)...(` mean the top-level Rust `bidi` import was used. In WeasyPrint, set `dir="rtl"` on the `<html>` element and pass the text in logical order: its text engine lays the line out from logical order (checked with WeasyPrint 70, even though WeasyPrint's documentation still lists bidirectional text among unsupported features), so never pre-reorder HTML text with `get_display()`, and check the rendered PDF. For DOCX/python-docx, do the OPPOSITE of the PDF fix: never call `get_display()` (Word reorders itself). Set `<w:bidi/>` on the paragraph, split the line into per-script runs, flag only the Hebrew runs `<w:rtl/>`, and set the `w:cs` font + `w:szCs` size on every run (see Step 5).

### Error: "Hebrew Word (.docx) renders with English on the wrong side, or my font/size is ignored"
Cause: The whole mixed line is in one run marked `<w:rtl/>` (English and numbers reverse), the Hebrew runs of a mixed line carry no `<w:rtl/>` (phrases in reverse order), or the runs set only `w:ascii`/`w:sz` and never the complex-script `w:cs`/`w:szCs` (Hebrew ignores the font/size). A bare presence check for `<w:rtl/>` passes on a file that still renders broken, so verify the run structure, not just the flag.
Solution: Use `scripts/docx_rtl.py` (Step 5): per-script runs, rtl on Hebrew runs only, `w:cs` + `w:szCs` on every run.

### Error: "Hebrew table (.docx) comes out reversed, the first column is on the left"
Cause: This is a COLUMN-ORDER bug, not a text-direction one. python-docx tables ship with no `<w:bidiVisual/>` on `<w:tblPr>`, so Word lays the columns out left-to-right and the first logical column lands on the left, making the whole table read backwards. Fixing the text inside each cell does not move the columns.
Solution: Set `table.table_direction = WD_TABLE_DIRECTION.RTL` once per table (emits `<w:bidiVisual/>`, which mirrors the visual column order to RTL), AND run each cell's text through the per-cell bidi helper. Both are needed; `add_rtl_table` does both. Keep your header/row data in natural logical order, do NOT reverse the column list yourself, that double-reverses once `bidiVisual` is set. Verify in Word, not LibreOffice/Preview (they mirror tables more forgivingly and hide this).

### Error: "Hebrew table cells are aligned to the left (headers/text on the left, numbers on the right)"
Cause: A physical `RIGHT` alignment was set on the cell paragraphs. `w:jc` in OOXML is LOGICAL, not physical: `right` means "line END", and in a Hebrew `<w:bidi/>` paragraph the line ends on the LEFT, so a RIGHT alignment pushes Hebrew to the visual left while LTR number cells still go right, leaving the table ragged and mismatched.
Solution: Do NOT set any explicit alignment on RTL table cells. Give each cell paragraph `<w:bidi/>` and leave alignment unset, an RTL paragraph defaults to its START edge (the visual right), so headers, Hebrew text, and numbers all line up flush right. See `set_cell_rtl_text` in `scripts/docx_rtl.py`.

### Error: "Every Hebrew paragraph in my Word file is aligned to the left"
Cause: The paragraphs carry `<w:bidi/>` AND an explicit right alignment (`WD_ALIGN_PARAGRAPH.RIGHT`, i.e. `w:jc="right"`). `jc` is logical, so on an RTL paragraph "right" is the line end, the visual left.
Solution: Leave alignment unset on RTL paragraphs; they start at the visual right. `scripts/docx_rtl.py` does this.

### Error: "WeasyPrint: cannot load library 'libgobject-2.0-0'" or the PDF uses a non-Hebrew font
Cause: Pango is not installed or not on the library path, or the HTML was rendered without `base_url` so a relative `@font-face` URL was ignored.
Solution: Install Pango (Step 2), and pass `base_url` to `HTML(...)` (Step 4).
