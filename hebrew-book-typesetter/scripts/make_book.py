#!/usr/bin/env python3
"""Generate a Typst book template for a Hebrew (right-to-left) manuscript.

Typical flow:
    pandoc manuscript.docx -t typst --extract-media=media -o body.typ
    python3 inspect_body.py body.typ --fix-quotes
    python3 make_book.py --body body.typ --title "שם הספר" --author "שם המחבר" \
        --trim 148x210 --toc --imprint --out book.typ
    typst compile --font-path fonts book.typ book.pdf

The generated book.typ is plain text. It can also be uploaded, together with
body.typ and the font files, to the typst.app web editor and exported to PDF
there, which needs no installation.

What the template guarantees:
  * binding on the RIGHT, margins given as inside / outside (mirrored per page)
  * the body always starts on a recto, and every page numbered 1, 3, 5 ... is a recto
  * blank pages inserted to reach a recto carry no page number and no running head
  * front matter in the order of a Hebrew book: title, imprint page on its back,
    then dedication, approbations / introduction files, table of contents,
    each opening on a recto
  * words carrying cantillation marks (teamim) or meteg are set whole in the
    teamim font, never patched letter by letter from a fallback font

Every measurement is a STARTING POINT. The print shop's own file spec wins:
confirm trim size, bleed and minimum inner margin with them before printing.
Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

FONTS_WITHOUT_METEG = {"David Libre"}
PRESETS = {"a5": (148, 210), "b5": (176, 250), "a4": (210, 297)}


def parse_trim(value: str):
    v = value.strip().lower()
    if v in PRESETS:
        return PRESETS[v]
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*[x*]\s*(\d+(?:\.\d+)?)", v)
    if not m:
        raise argparse.ArgumentTypeError(
            f"trim must be WIDTHxHEIGHT in mm (e.g. 140x210) or one of {sorted(PRESETS)}")
    w, h = float(m.group(1)), float(m.group(2))
    if not (70 <= w <= 300 and 100 <= h <= 420):
        raise argparse.ArgumentTypeError("trim size looks wrong: expected millimetres, e.g. 140x210")
    return w, h


def s(text: str) -> str:
    """A Typst string literal. Displayed with #name, so # * _ $ @ < and quotes stay literal."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


HELPERS = r'''
// ---------- helpers ----------
// Hebrew letter numerals: 15 and 16 are written טו / טז (never יה / יו).
// Page numbers take no geresh or gershayim; pass marks: true for other uses.
#let gematria(n, marks: false) = {
  let units = ("", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט")
  let tens = ("", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ")
  let hundreds = ("", "ק", "ר", "ש", "ת")
  let out = ""
  let rest = calc.rem(n, 1000)
  let thousands = calc.quo(n, 1000)
  if thousands > 0 { out += gematria(thousands) + "׳" }
  while rest >= 400 { out += "ת"; rest -= 400 }
  if rest >= 100 { out += hundreds.at(calc.quo(rest, 100)); rest = calc.rem(rest, 100) }
  if rest == 15 { out += "טו"; rest = 0 }
  else if rest == 16 { out += "טז"; rest = 0 }
  else {
    out += tens.at(calc.quo(rest, 10))
    out += units.at(calc.rem(rest, 10))
  }
  if not marks { return out }
  let cs = out.clusters()
  if cs.len() == 1 { out + "׳" } else { cs.slice(0, -1).join() + "״" + cs.last() }
}

// Start the next content on a recto (odd physical page). The markers let the
// header and footer recognise the blank page this may insert.
#let recto() = [#metadata("end") <rb-end>#pagebreak(to: "odd", weak: true)#metadata("start") <rb-start>]

#let is-blank() = {
  let p = here().page()
  let ends = query(<rb-end>)
  let starts = query(<rb-start>)
  let blank = false
  for (e, st) in ends.zip(starts) {
    if e.location().page() < p and p < st.location().page() { blank = true }
  }
  if query(<pad>).any(x => x.location().page() == p) { blank = true }
  blank
}

// Front matter has no page number or running head: both start on the page
// carrying <body-start>.
#let in-body() = {
  let b = query(<body-start>)
  b.len() > 0 and here().page() >= b.first().location().page()
}
'''


def build(a) -> str:
    w, h = a.trim
    if a.numbering == "gematria":
        page_num = "gematria(n, marks: %s)" % ("true" if a.gershayim else "false")
    else:
        page_num = "str(n)"
    if a.footnote_numbering == "gematria":
        fn_num = "(..n) => gematria(n.pos().first())"
    else:
        fn_num = '"1"'
    if a.chapter_start == "odd":
        chapter_break = "recto()"
    elif a.chapter_start == "any":
        chapter_break = "pagebreak(weak: true)"
    else:
        chapter_break = "none"
    fn_reset = "counter(footnote).update(0)" if a.footnote_reset == "chapter" else "none"

    fonts = "(" + s(a.font) + ",)"
    teamim = ""
    if a.teamim_font:
        # Whole words that carry a cantillation mark (U+0591-U+05AF). Meteg (U+05BD) is added
        # only when the body font lacks it, so vocalized words are not pulled out of the body font.
        marks = "\\u{0591}-\\u{05AF}" + ("\\u{05BD}" if (a.meteg_in_teamim_font or a.font in FONTS_WITHOUT_METEG) else "")
        teamim = ('#show regex("[\\\\p{Hebrew}\\\\p{M}]*[%s][\\\\p{Hebrew}\\\\p{M}]*"): '
                  'set text(font: %s)\n' % (marks, s(a.teamim_font)))
        # The last word of a pasuk carries silluq (same code point as meteg) and ends in sof pasuq:
        # keep it in the teamim font with the rest of the verse.
        teamim += ('#show regex("[\\\\p{Hebrew}\\\\p{M}]*\\u{05BD}[\\\\p{Hebrew}\\\\p{M}־]*\\u{05C3}"): '
                   'set text(font: %s)\n' % s(a.teamim_font))
    note_font = ""
    if a.note_font:
        note_font = "#show footnote.entry: set text(font: %s)\n" % s(a.note_font)

    front = []
    # Title page (recto 1) and its back (verso 2).
    front.append('''#align(center + horizon)[
  #text(size: 2.2em, weight: "bold")[#book-title]
  #if book-subtitle != "" [ \\ #v(0.6em) #text(size: 1.3em)[#book-subtitle] ]
  #v(1.8em)
  #text(size: 1.3em)[#book-author]
]
#pagebreak()''')
    if a.imprint:
        lines = [
            ("© ", a.copyright or "____"),
            ("שנת ההוצאה לאור: ", a.year_published or "____"),
            ("שנת ההדפסה: ", a.year_printed or "____"),
            ("המוציא לאור: ", ((a.publisher or "____") + ", " + (a.publisher_address or "____"))),
            ("הדפוס: ", ((a.printer or "____") + ", " + (a.printer_address or "____"))),
        ]
        body = "\n".join("  #%s#%s \\" % (s(k), s(v)) for k, v in lines)
        isbn = ""
        if a.isbn:
            isbn = "  #v(0.8em)\n  #%s \\\n" % s("מסת״ב / ISBN " + a.isbn)
        front.append('''#align(bottom)[
  #set text(size: 0.85em)
  #set par(first-line-indent: 0em, justify: false)
%s
%s  #v(0.8em)
  #%s
]''' % (body, isbn, s("יצא לאור בישראל")))
    else:
        front.append("// (back of the title page left blank; run with --imprint to fill it)\n#hide[.]")
    if a.dedication:
        front.append('''#recto()
#align(center + horizon)[#text(size: 1.15em, style: "italic")[#%s]]''' % s(a.dedication))
    for f in a.front_file:
        front.append("#recto()\n#[\n  #set heading(outlined: false)\n  #include %s\n]" % s(f))
    if a.toc:
        front.append("#recto()\n#outline(title: [#%s], depth: %d)" % (s(a.toc_title), a.toc_depth))

    pad = ""
    if a.pad_to:
        pad = '''
// Pad with blank pages so the page count divides by %d (the shop's signature size).
#metadata("end") <body-end>
#context {
  let total = locate(<body-end>).page()
  let extra = calc.rem(%d - calc.rem(total, %d), %d)
  for _ in range(extra) { pagebreak(); [#metadata("pad") <pad>] }
}
''' % (a.pad_to, a.pad_to, a.pad_to, a.pad_to)

    nl = "\n"
    return f'''// Generated by hebrew-book-typesetter/scripts/make_book.py
// Trim {w:g}x{h:g} mm, bleed {a.bleed:g} mm per side. With a bleed, the PDF gets a TrimBox.
// Hebrew books bind on the RIGHT, so "inside" is the right margin of a recto page.
{HELPERS}
#let book-title = {s(a.title)}
#let book-subtitle = {s(a.subtitle)}
#let book-author = {s(a.author)}

#set document(title: book-title, author: book-author)
#set text(lang: "he", dir: rtl, font: {fonts}, size: {a.size}pt)
#set par(justify: true, leading: {a.leading}em, first-line-indent: (amount: {a.indent}em, all: false))
{teamim}{note_font}#set footnote(numbering: {fn_num})
#set footnote.entry(separator: line(length: 3cm, stroke: 0.5pt))
#set page(
  width: {w:g}mm,
  height: {h:g}mm,
  bleed: {a.bleed:g}mm,
  binding: right,
  margin: (inside: {a.inside:g}mm, outside: {a.outside:g}mm, top: {a.top:g}mm, bottom: {a.bottom:g}mm),
  // Used by the table of contents; the visible folio is drawn by the footer below.
  numbering: (..n) => {page_num.replace("gematria(n,", "gematria(n.pos().first(),").replace("str(n)", "str(n.pos().first())")},
  footer: context {{
    if not in-body() or is-blank() {{ return none }}
    let n = counter(page).get().first()
    align(center)[#{page_num}]
  }},
  header: context {{
    if not in-body() or is-blank() {{ return none }}
    let p = here().page()
    // No running head on a page where a chapter opens.
    if query(heading.where(level: 1, outlined: true)).any(x => x.location().page() == p) {{ return none }}
    let chapters = query(heading.where(level: 1, outlined: true).before(here()))
    set text(size: 0.8em)
    // Book title on even pages, current chapter on odd pages.
    if calc.even(counter(page).get().first()) {{
      align(center)[#book-title]
    }} else if chapters.len() > 0 {{
      align(center)[#chapters.last().body]
    }}
  }},
)
#show heading.where(level: 1): it => {{
  if it.outlined {{ {chapter_break}; {fn_reset} }}
  v(4em)
  align(center, text(size: 1.6em, weight: "bold", it.body))
  v(2em)
}}
#show heading.where(level: 2): it => align(center, block(above: 1.6em, below: 1em, text(size: 1.15em, weight: "bold", it.body)))

// ---------- front matter (no page numbers, no running heads) ----------
{nl.join(front)}

// ---------- body: always opens on a recto, numbered from 1 ----------
#recto()
#counter(page).update(1)
#metadata("start") <body-start>
#include {s(a.body)}
{pad}'''


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--body", required=True, help="pandoc output (body.typ), path relative to --out")
    p.add_argument("--out", default="book.typ")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--author", default="")
    p.add_argument("--trim", type=parse_trim, default=parse_trim("a5"),
                   help="WIDTHxHEIGHT in mm, or a5 / b5 / a4. Confirm with the print shop.")
    p.add_argument("--bleed", type=float, default=0.0,
                   help="mm per side. Only needed if something runs to the page edge. Ask the print shop.")
    p.add_argument("--inside", type=float, default=22.0, help="inner (spine) margin from the trim edge, mm")
    p.add_argument("--outside", type=float, default=20.0, help="outer margin from the trim edge, mm")
    p.add_argument("--top", type=float, default=28.0, help="top margin, mm (room for the running head)")
    p.add_argument("--bottom", type=float, default=22.0, help="bottom margin, mm (room for the page number)")
    p.add_argument("--font", default="Frank Ruhl Libre",
                   help="body font family (must be installed or passed with --font-path)")
    p.add_argument("--teamim-font", default="",
                   help="font for whole words carrying cantillation marks or meteg, e.g. 'Ezra SIL'")
    p.add_argument("--meteg-in-teamim-font", action="store_true",
                   help="also move words with meteg to the teamim font (automatic for David Libre, which lacks meteg)")
    p.add_argument("--note-font", default="", help="font for footnotes, e.g. 'Noto Rashi Hebrew'")
    p.add_argument("--size", type=float, default=11.5, help="body size in pt")
    p.add_argument("--leading", type=float, default=0.75, help="extra line spacing, em")
    p.add_argument("--indent", type=float, default=1.2, help="paragraph first-line indent, em")
    p.add_argument("--numbering", choices=["gematria", "arabic"], default="gematria")
    p.add_argument("--gershayim", action="store_true",
                   help="page numbers like ט״ו (the Academy rule is to leave page numbers without marks)")
    p.add_argument("--footnote-numbering", choices=["arabic", "gematria"], default="arabic")
    p.add_argument("--footnote-reset", choices=["book", "chapter"], default="book")
    p.add_argument("--chapter-start", choices=["odd", "any", "none"], default="any",
                   help="any = next page; odd = every chapter opens on a recto (blank pages get no number)")
    p.add_argument("--toc", action="store_true", help="add a table of contents (opens on a recto)")
    p.add_argument("--toc-title", default="תוכן העניינים")
    p.add_argument("--toc-depth", type=int, default=2)
    p.add_argument("--imprint", action="store_true",
                   help="fill the back of the title page with the details section 3 of the Books Law requires")
    p.add_argument("--year-published", default="")
    p.add_argument("--year-printed", default="")
    p.add_argument("--publisher", default="", help="a self-publishing author is the publisher")
    p.add_argument("--publisher-address", default="")
    p.add_argument("--printer", default="")
    p.add_argument("--printer-address", default="")
    p.add_argument("--isbn", default="", help="only if one was issued; it is optional")
    p.add_argument("--copyright", default="", help="free text for the copyright line")
    p.add_argument("--dedication", default="", help="dedication or memorial line, on its own recto")
    p.add_argument("--front-file", action="append", default=[],
                   help="extra front-matter .typ file (approbations, introduction), each opens on a recto; repeatable, in order")
    p.add_argument("--pad-to", type=int, default=2,
                   help="add blank pages at the end so the total divides by this number; default 2 (an even count); ask the shop for 4, 8, 16 or 32")
    a = p.parse_args(argv)
    if a.bleed < 0 or a.bleed > 10:
        p.error("--bleed is per side in mm and should be between 0 and 10")
    if a.pad_to < 0:
        p.error("--pad-to must be positive")
    if a.inside < a.outside:
        print("warning: inside margin is smaller than outside; thick books lose text into the spine",
              file=sys.stderr)
    if a.imprint:
        missing = [k for k in ("year_published", "year_printed", "publisher", "publisher_address",
                               "printer", "printer_address") if not getattr(a, k)]
        if missing:
            print("note: imprint fields left as ____ for: " + ", ".join(missing), file=sys.stderr)
    out = Path(a.out)
    out.write_text(build(a), encoding="utf-8")
    print(f"wrote {out}  (trim {a.trim[0]:g}x{a.trim[1]:g} mm, bleed {a.bleed:g} mm)")


if __name__ == "__main__":
    main()
