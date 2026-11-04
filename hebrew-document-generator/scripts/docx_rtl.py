#!/usr/bin/env python3
"""Word-safe Hebrew (RTL) paragraphs and tables for python-docx.

Import the helpers, or run the file to write a sample contract:

    python docx_rtl.py --output contract.docx

    from docx_rtl import new_hebrew_document, add_rtl_paragraph, add_rtl_table
    doc = new_hebrew_document()
    add_rtl_paragraph(doc, 'ההסכם נחתם בין חברת Acme בע"מ לבין הלקוח (גרסה 2).')
    add_rtl_table(doc, ['תיאור', 'כמות'], [['פיתוח Acme', 2]])
    doc.save('out.docx')

Rules the helpers implement (checked against Microsoft Word's own rendering):

1. A paragraph with any Hebrew gets <w:bidi/> (RTL base) and NO explicit
   alignment. w:jc is logical, so jc=right on an RTL paragraph means the line
   END, which Word draws on the visual LEFT. An RTL paragraph with no jc starts
   at the visual right. A pure-English line gets LTR base and left alignment.
2. Each line is split into runs by script. Hebrew runs, and neutral stretches
   that resolve to RTL, carry <w:rtl/>. Latin and digit runs never do, so
   dates, codes and amounts are not reversed. Without <w:rtl/> on the Hebrew
   runs, Word lays the runs of a mixed line out left to right.
3. Every run sets the complex-script font and size (w:cs, w:szCs), and bold or
   italic set w:bCs / w:iCs too, because Word applies w:ascii / w:sz / w:b only
   to Latin text.
4. Tables get <w:bidiVisual/> (table_direction = RTL) so the first logical
   column is drawn on the right, and every cell paragraph follows rule 1.

Never call bidi.get_display() on DOCX text (Word runs the bidi algorithm
itself), and never insert Unicode directional marks or isolates (Word draws
them as boxes in the David font).

Requires: pip install python-docx
"""

import argparse
import re
import sys
import unicodedata

try:
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_DIRECTION, WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
except ImportError:
    print("Missing required dependency. Install with:", file=sys.stderr)
    print("  pip install python-docx", file=sys.stderr)
    sys.exit(1)

# Hebrew block + Hebrew presentation forms, as explicit escapes.
_HEB = re.compile('[֐-׿יִ-ﭏ]')
_LIST_MARKER = re.compile(r'^\d{1,2}$')  # the "2" of a leading "2." marker
_NUM_SEPARATORS = ',./:-+'
_NUM_AFFIXES = '%₪$€#°'  # percent, shekel, dollar, euro, #, degree


_BRACKETS = {'(': ')', '[': ']', '{': '}'}


def _strong(ch):
    """True for a right-to-left letter (Hebrew), False for a left-to-right
    letter (any script, including accented Latin such as "Nestl\u00e9") or an
    ASCII digit, None for a neutral character."""
    bidi_class = unicodedata.bidirectional(ch)
    if bidi_class in ('R', 'AL'):
        return True
    if bidi_class == 'L' or (ch.isascii() and ch.isdigit()):
        return False
    return None


def _para_is_rtl(text):
    """RTL base for any line with Hebrew; LTR for a line with Latin letters or
    digits and no Hebrew; RTL for an all-neutral line (the document default)."""
    strong = [s for s in (_strong(ch) for ch in text) if s is not None]
    if any(strong):
        return True
    if strong:
        return False
    return True


def _split_by_script(text):
    """Split a line into (segment, is_rtl) runs, following the Unicode bidi
    rules closely enough for Word.

    Hebrew letters are RTL, Latin letters are LTR, and ASCII digits form LTR
    runs of their own. A separator between two digits ("7/2023", "1,500.00",
    "03-1234567") and a %, currency or # sign touching a number stay with the
    number, and so does a leading + or - sign ("+972-3-1234567").
    A number that follows a Latin word ("KI-67") joins it. A bracket pair
    around Latin text that follows a Latin word ("Acme (Israel)") stays
    Latin, so Word does not mirror the closing bracket. Any other
    neutral stretch (spaces, brackets, punctuation) takes its neighbours'
    direction when both agree and otherwise the paragraph direction, with
    numbers counting as RTL neighbours inside a Hebrew line. This keeps the
    ")" and "." after "(18%)" or "(2)" in the RTL run.
    """
    para_rtl = _para_is_rtl(text)
    n = len(text)
    kinds = []  # 'R', 'L', 'EN' (digit) or None (neutral)
    for ch in text:
        s = _strong(ch)
        kinds.append(None if s is None else ('R' if s else ('EN' if ch.isdigit() else 'L')))
    for i in range(1, n - 1):  # one separator between two digits joins them
        if (kinds[i] is None and text[i] in _NUM_SEPARATORS
                and kinds[i - 1] == 'EN' and kinds[i + 1] == 'EN'):
            kinds[i] = 'EN'
    i = 0
    while i < n:  # %, currency and # signs touching a number join it
        if kinds[i] is None and text[i] in _NUM_AFFIXES:
            j = i
            while j < n and kinds[j] is None and text[j] in _NUM_AFFIXES:
                j += 1
            if (i > 0 and kinds[i - 1] == 'EN') or (j < n and kinds[j] == 'EN'):
                for m in range(i, j):
                    kinds[m] = 'EN'
            i = j
        else:
            i += 1
    for i in range(n - 1):  # a leading + or - sign joins the number after it
        if (kinds[i] is None and text[i] in '+-' and kinds[i + 1] == 'EN'
                and (i == 0 or text[i - 1].isspace() or text[i - 1] in '(:')):
            kinds[i] = 'EN'
    last = 'R' if para_rtl else 'L'  # a number after a Latin word is Latin
    for i in range(n):
        if kinds[i] in ('L', 'R'):
            last = kinds[i]
        elif kinds[i] == 'EN' and last == 'L':
            kinds[i] = 'L'
    para = 'R' if para_rtl else 'L'

    def as_strong(kind):
        return 'R' if kind == 'EN' else kind

    stack = []  # bracket pairs (Unicode rule N0)
    for i, ch in enumerate(text):
        if kinds[i] is not None:
            continue
        if ch in _BRACKETS:
            stack.append((i, _BRACKETS[ch]))
        elif stack and ch == stack[-1][1]:
            start, _ = stack.pop()
            inside = {as_strong(kinds[m]) for m in range(start + 1, i)} - {None}
            if para in inside:
                side = para
            elif inside:
                prev = next((as_strong(kinds[m]) for m in range(start - 1, -1, -1)
                             if kinds[m] is not None), para)
                side = prev
            else:
                continue
            kinds[start] = kinds[i] = side
    i = 0
    while i < n:  # neutral stretches
        if kinds[i] is not None:
            i += 1
            continue
        j = i
        while j < n and kinds[j] is None:
            j += 1
        before = 'R' if i > 0 and kinds[i - 1] == 'EN' else (kinds[i - 1] if i > 0 else para)
        after = 'R' if j < n and kinds[j] == 'EN' else (kinds[j] if j < n else para)
        fill = before if before == after else para
        for m in range(i, j):
            kinds[m] = fill
        i = j
    segments, buf, buf_rtl = [], '', None
    for ch, kind in zip(text, kinds):
        rtl = kind == 'R'
        if buf_rtl is None or rtl == buf_rtl:
            buf, buf_rtl = buf + ch, rtl
        else:
            segments.append((buf, buf_rtl))
            buf, buf_rtl = ch, rtl
    if buf:
        segments.append((buf, buf_rtl))
    return segments


def _merge_list_marker(segments):
    """Merge a leading 1-2 digit list marker ("2.", "10.") into the Hebrew run
    that follows it, or Word floats the period to the wrong side (".2"). A date
    like 13/01/2026 never qualifies and stays its own LTR run."""
    if (len(segments) >= 2 and segments[0][1] is False
            and _LIST_MARKER.match(segments[0][0].strip())
            and segments[1][1] is True and segments[1][0].startswith('.')):
        return [(segments[0][0] + segments[1][0], True)] + list(segments[2:])
    return list(segments)


def _shift_boundary_spaces(segments):
    """Move a space at the end of an LTR run that precedes an RTL run to the
    start of the RTL run. Word trims trailing whitespace at a direction
    boundary, which would glue the two words together."""
    out = [[seg, rtl] for seg, rtl in segments]
    for i in range(len(out) - 1):
        seg, rtl = out[i]
        nseg, nrtl = out[i + 1]
        if rtl is False and nrtl is True and seg.endswith(' '):
            stripped = seg.rstrip(' ')
            out[i][0] = stripped
            out[i + 1][0] = seg[len(stripped):] + nseg
    return [(s, r) for s, r in out if s]


def _fill_paragraph(p, text, font, size, bold=False, italic=False):
    """Set the base direction of paragraph p and add its per-script runs."""
    base_rtl = _para_is_rtl(text)
    if base_rtl:
        pPr = p._p.get_or_add_pPr()
        pPr.append(pPr.makeelement(qn('w:bidi'), {}))
        # No alignment: an RTL paragraph starts at the visual right by default.
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for segment, is_rtl in _shift_boundary_spaces(_merge_list_marker(_split_by_script(text))):
        run = p.add_run(segment)
        rPr = run._r.get_or_add_rPr()
        # Keep rPr children in OOXML schema order: rFonts, b, bCs, i, iCs, sz, szCs, rtl
        rPr.append(rPr.makeelement(qn('w:rFonts'), {
            qn('w:ascii'): font, qn('w:hAnsi'): font, qn('w:cs'): font}))
        if bold:
            rPr.append(rPr.makeelement(qn('w:b'), {}))
            rPr.append(rPr.makeelement(qn('w:bCs'), {}))
        if italic:
            rPr.append(rPr.makeelement(qn('w:i'), {}))
            rPr.append(rPr.makeelement(qn('w:iCs'), {}))
        rPr.append(rPr.makeelement(qn('w:sz'), {qn('w:val'): str(size * 2)}))
        rPr.append(rPr.makeelement(qn('w:szCs'), {qn('w:val'): str(size * 2)}))
        if is_rtl:
            rPr.append(rPr.makeelement(qn('w:rtl'), {}))
    return p


def new_hebrew_document(font='David', size=12):
    """Create a Document whose Normal style and first section are RTL-ready."""
    doc = Document()
    doc.styles['Normal'].font.name = font
    doc.styles['Normal'].font.size = Pt(size)
    set_section_rtl(doc.sections[0])
    return doc


def set_section_rtl(section):
    """Add <w:bidi/> to a section so Word treats the page as RTL (column order,
    gutter side). Inserted before w:docGrid to keep the sectPr schema order."""
    sectPr = section._sectPr
    if sectPr.find(qn('w:bidi')) is not None:
        return
    bidi = sectPr.makeelement(qn('w:bidi'), {})
    grid = sectPr.find(qn('w:docGrid'))
    if grid is not None:
        grid.addprevious(bidi)
    else:
        sectPr.append(bidi)


def add_rtl_paragraph(doc, text, font='David', size=12, bold=False, italic=False,
                      heading_level=None):
    """Add a body paragraph (or heading) with mixed Hebrew/Latin/digit text."""
    p = doc.add_heading(level=heading_level) if heading_level else doc.add_paragraph()
    return _fill_paragraph(p, text, font, size, bold, italic)


def set_cell_rtl_text(cell, text, font='David', size=11, bold=False):
    """Fill a table cell. Hebrew and numeric cells alike align flush right,
    because an RTL cell paragraph with no w:jc starts at the visual right."""
    p = cell.paragraphs[0]
    p.text = ''
    pPr = p._p.get_or_add_pPr()
    pPr.append(pPr.makeelement(qn('w:bidi'), {}))
    for segment, is_rtl in _shift_boundary_spaces(_merge_list_marker(_split_by_script(text))):
        run = p.add_run(segment)
        rPr = run._r.get_or_add_rPr()
        rPr.append(rPr.makeelement(qn('w:rFonts'), {
            qn('w:ascii'): font, qn('w:hAnsi'): font, qn('w:cs'): font}))
        if bold:
            rPr.append(rPr.makeelement(qn('w:b'), {}))
            rPr.append(rPr.makeelement(qn('w:bCs'), {}))
        rPr.append(rPr.makeelement(qn('w:sz'), {qn('w:val'): str(size * 2)}))
        rPr.append(rPr.makeelement(qn('w:szCs'), {qn('w:val'): str(size * 2)}))
        if is_rtl:
            rPr.append(rPr.makeelement(qn('w:rtl'), {}))


def add_rtl_table(doc, headers, rows, font='David', size=11):
    """Add a table whose first logical column is drawn on the right. Keep the
    data in logical order; do not reverse the column lists yourself."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.table_direction = WD_TABLE_DIRECTION.RTL  # emits <w:bidiVisual/>
    table.alignment = WD_TABLE_ALIGNMENT.RIGHT      # table block hugs the right margin
    for j, h in enumerate(headers):
        set_cell_rtl_text(table.rows[0].cells[j], h, font=font, size=size, bold=True)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            set_cell_rtl_text(table.rows[i].cells[j], str(val), font=font, size=size)
    return table


def main():
    parser = argparse.ArgumentParser(description="Write a sample Hebrew contract .docx")
    parser.add_argument("--output", default="contract.docx", help="Output .docx path")
    args = parser.parse_args()

    doc = new_hebrew_document()
    add_rtl_paragraph(doc, 'חוזה שירותים (טיוטה לדוגמה)', size=18, bold=True)
    add_rtl_paragraph(doc, 'ההסכם נחתם ביום 13/01/2026 בין חברת Acme בע"מ לבין הלקוח (גרסה 2).')
    add_rtl_paragraph(doc, '1. היקף העבודה', bold=True)
    add_rtl_paragraph(doc, '1.1. החברה תספק שירותי פיתוח ב-Python ותחזוקה (3 חודשים).')
    add_rtl_paragraph(doc, '2. תמורה', bold=True)
    add_rtl_table(doc, ['תיאור', 'כמות', 'מחיר', 'סה"כ'],
                  [['ייעוץ טכני (3 שעות)', 1, '1,500.00', '1,500.00'],
                   ['פיתוח Acme (שלב 2)', 2, '600.00', '1,200.00']])
    add_rtl_paragraph(doc, 'מע"מ (18%) יתווסף לסכומים. טלפון: 03-1234567, דוא"ל: info@acme.co.il')
    add_rtl_paragraph(doc, 'Signed in two copies')
    doc.save(args.output)
    print(f"Generated contract: {args.output}")


if __name__ == "__main__":
    main()
