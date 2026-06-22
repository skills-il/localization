---
name: hebrew-document-generator
description: Generate Hebrew documents (PDF, DOCX/Word, PPTX) with correct right-to-left layout, mixed Hebrew-and-English bidi handling, and Hebrew typography. Use whenever the output is a Hebrew or mixed Hebrew/English Word document, Hebrew PDF, or Hebrew PowerPoint ("Hebrew Word document", "מסמך Word בעברית", "create a .docx in Hebrew", "litstor hozeh"), or Israeli templates like Heshbonit Mas, Hozeh, or Protokol. ALSO use this for the symptom where a Hebrew document looks fine on screen or in Claude but comes out scrambled, reversed, or broken in Word, with English, numbers, or punctuation on the wrong side ("Hebrew text reversed in Word", "fix Hebrew formatting in Word"); the fix is regenerating the .docx with paragraph-level RTL/bidi, NOT a web/CSS RTL change. Prefer over the generic docx/pdf skills ONLY when the document is Hebrew or RTL; for English-only docs use the generic skill. Covers reportlab, WeasyPrint, python-docx, pptxgenjs. Do NOT use for OCR or reading existing documents (use hebrew-ocr-forms).
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

DOCX is where mixed Hebrew/English breaks most often, and Microsoft Word's bidi engine is stricter than the Unicode standard. LibreOffice, macOS Preview/Quick Look, and most viewers render forgiving output that HIDES Word-only bugs, so always verify in Word itself, not a substitute renderer. Four rules, each learned against real Word:

1. Every Hebrew paragraph carries `<w:bidi/>` (RTL base direction); a pure-English line (a lab value, a drug name, an English-only row) gets LTR base + left alignment instead. The helper picks this per paragraph from whether the line contains any Hebrew, so English-only rows do not hang off the right margin in an otherwise Hebrew document.
2. **Do NOT put `<w:rtl/>` on the runs of a MIXED Hebrew+English paragraph.** This is the single biggest Word trap. Word honors `<w:rtl/>` strictly: any Latin or number that lands in (or beside) an rtl-flagged run gets force-reversed, so `7/2023` prints as `2023/7`, an embedded `KI-67` code flips, and the parentheses around a mixed group like `(גסטרית, KI-67)` mis-pair. In a mixed paragraph the paragraph's own `<w:bidi/>` already orders the line correctly, leave every run unflagged.
3. **Flag `<w:rtl/>` ONLY on Hebrew runs of a paragraph that has no Latin letters** (a pure-Hebrew label or heading, digits allowed). There the flag is what anchors a trailing colon (`מחלות רקע:`) to the left end. A leading section-number marker (`2.`, `10.`) is additionally merged into the Hebrew run (`_merge_list_marker`) so its period does not flip to `.2`; a date like `13/01/2026` is left as its own LTR run so Word does not reverse it. The split stays by script so each run still gets the right complex-script font.
4. Every run sets the complex-script font (`w:cs`) and size (`w:szCs`). Hebrew is a "complex script" in Word's model, so `w:ascii`/`w:sz` alone never govern the Hebrew glyphs. Omitting `w:cs`/`w:szCs` is the most common cause of "the font/size I set did nothing and the Hebrew looks broken". Bold and italic are the same: `w:b`/`w:i` only affect Latin, you also need `w:bCs`/`w:iCs`. **Never insert Unicode directional isolates (U+2066-2069) or marks to force order, Word renders them as visible `.notdef` boxes in the David font even though other viewers hide them.**

```python
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# Hebrew block + Hebrew presentation forms. Used to pick each run's direction.
_HEB = re.compile(r'[\u0590-\u05FF\uFB1D-\uFB4F]')  # Hebrew block + presentation forms
_LIST_MARKER = re.compile(r'^\d{1,2}\.$')  # 1-2 digit list marker, e.g. "2."

def _strong(ch):
    """True for a Hebrew letter, False for a strong-LTR char (Latin OR ASCII
    digit), None for neutral. Digits count as LTR so a number never rides inside
    a Hebrew run (Word force-reverses numbers caught in an rtl-flagged run)."""
    if _HEB.match(ch):
        return True
    if ch.isascii() and ch.isalnum():
        return False
    return None

def _split_by_script(text):
    """Split a mixed string into (segment, is_rtl) runs.

    Each run's direction is set by its STRONG characters; neutral chars
    (spaces, digits, punctuation) attach to the current run. Leading neutrals
    inherit the direction of the first strong character in the WHOLE string
    (falling back to RTL for an all-neutral string in a Hebrew document), so a
    Latin-dominant line that starts with a digit or bracket is not mis-flagged
    RTL. The split groups characters so each run can carry the correct
    complex-script font; in Word, run DIRECTION is governed by the rtl rules
    in add_rtl_paragraph, not by this split alone.
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
    """Move a space at the END of an LTR run that directly precedes an RTL run to
    the START of that RTL run. Word trims a run's trailing whitespace at a
    direction boundary, which glues a leading number to its heading
    ("2.\u05db\u05d5\u05ea\u05e8\u05ea"); a leading space on the RTL run survives and restores
    the gap. Without this, numbered Hebrew headings lose the space after "N.".
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
    """A leading short list-number marker ("2.", "10.") on an RTL line must be part
    of the Hebrew RTL run, or Word floats its period to the wrong side (".2").
    Merge a leading LTR marker run into the Hebrew run that follows it. Matches
    only 1-2 digits + period, never a date like 13/01/2026 (which must stay an
    LTR run so Word does not reverse it)."""
    if (len(segments) >= 2 and segments[0][1] is False
            and _LIST_MARKER.match(segments[0][0].strip())
            and segments[1][1] is True):
        return [(segments[0][0] + segments[1][0], True)] + list(segments[2:])
    return list(segments)

def _para_is_rtl(text):
    """Choose the paragraph base direction for a Hebrew document.

    Any Hebrew letter -> RTL base: a Hebrew sentence routinely embeds English
    terms, drug names, or numbers and must still flow right-to-left. No Hebrew
    but Latin present -> LTR base, so a pure-English line (a lab value, an
    English-only clinical row) renders left-aligned instead of hugging the right
    margin. All-neutral (digits/punctuation only) -> RTL, the document default.
    This is the fix for "English-only lines come out right-aligned and the
    document still looks RTL-broken".
    """
    if _HEB.search(text):
        return True
    if any(ch.isascii() and ch.isalnum() for ch in text):
        return False
    return True

def add_rtl_paragraph(doc, text, font='David', size=12, bold=False, italic=False,
                      heading_level=None):
    """Add a paragraph that renders mixed Hebrew/Latin/digit text correctly,
    auto-selecting RTL or LTR base direction from whether the line has Hebrew.

    Covers BODY paragraphs only. Table cells, headers/footers, and numbered
    lists are separate document stories: apply the same logic to each of their
    paragraphs, and add `<w:bidi/>` to the section `sectPr` for a fully RTL page.
    """
    p = doc.add_heading(level=heading_level) if heading_level else doc.add_paragraph()

    # (1) paragraph base direction: RTL when the line contains any Hebrew (a
    #     Hebrew sentence routinely embeds English terms and must still flow
    #     right-to-left); LTR for a pure-Latin line so an English-only row reads
    #     left-aligned instead of hugging the right margin.
    base_rtl = _para_is_rtl(text)
    pPr = p._p.get_or_add_pPr()
    if base_rtl:
        pPr.append(pPr.makeelement(qn('w:bidi'), {}))
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if base_rtl else WD_ALIGN_PARAGRAPH.LEFT

    # A paragraph with ANY Latin letter is "mixed": never rtl-flag its runs
    # (rule 2 above). A paragraph with only Hebrew (+digits/punct) is "pure":
    # its Hebrew runs DO get rtl, to anchor trailing colons and leading numbers.
    para_has_latin = any(ch.isascii() and ch.isalpha() for ch in text)

    for segment, is_rtl in _shift_boundary_spaces(_merge_list_marker(_split_by_script(text))):
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
        # (2) Flag rtl ONLY on Hebrew runs of a paragraph with no Latin letters.
        #     In a mixed Hebrew+English paragraph, NO run is flagged, or Word
        #     force-reverses the embedded numbers/Latin and mis-pairs parens.
        #     The paragraph <w:bidi/> alone orders mixed lines correctly.
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