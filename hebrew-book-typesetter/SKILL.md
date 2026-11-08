---
name: hebrew-book-typesetter
description: "Turn a long Hebrew Word manuscript (memoir, poetry with nikkud, chidushei torah, academic book) into a print-ready book PDF, then prepare it for an Israeli print shop, ISBN and legal deposit. Use when the user says 'lay out my book', 'typeset a Hebrew book', 'imud sefer', 'imud le-dfus', 'print-ready PDF', 'self-publish a book in Hebrew', 'my Word file for the printer', or asks about ISBN (mis'tav) or depositing copies at the National Library. Converts docx with pandoc to Typst, builds a right-bound layout with mirrored margins, Hebrew-letter page numbers (tet-vav for 15), running heads, footnotes and a table of contents, then computes the cover and spine. Prevents the costly reprint that follows a file with wrong binding side, broken nikkud or missing imprint details. Do NOT use for short documents, letters, reports or slides (use hebrew-document-generator) or for writing and editing the text itself (use hebrew-content-writer)."
license: MIT
compatibility: "Best on agents with a shell (Claude Code, Cursor, Codex, Gemini CLI and similar), which run pandoc, Typst and the bundled Python scripts. Chat surfaces (Claude.ai, ChatGPT, Claude Desktop without a shell) follow the no-install route in Step 2, where the user compiles on typst.app in the browser."
---

# Hebrew Book Typesetter

## Problem

Israeli authors who self-publish usually arrive with a long Word file and a print shop that wants "a closed PDF". Word cannot reliably produce a right-bound book with mirrored margins, Hebrew-letter page numbers and running heads, and AI assistants routinely get the Hebrew-specific parts wrong: binding on the left, the cover laid out like an English book, 15 written as yud-heh, nikkud and teamim broken by the font, and the imprint details the Books Law requires left out. A wrong file means paying for a reprint.

## Instructions

### Step 1: Collect the decisions before touching the file

Ask only what you cannot infer. Most authors do not know these answers yet, so offer the default and say why.

| Decision | Default | Notes |
|---|---|---|
| Print shop | Ask | Their own file spec beats every default below. Ask the user to request it. |
| Binding | Perfect-bound paperback | A short stapled booklet (קונטרס) has no spine and needs a page count the shop can fold into sheets; a hardcover needs the binder's own layout. Ask which one. |
| Trim size | A5 (14.8 x 21 cm) | The most common size in Israel per PrintaBook. 17 x 24 cm suits academic books and sefarim with long notes (Dfus Eichut lists it as standard). |
| Bleed | None for a text-only interior | Only needed when ink reaches the page edge (photos, full-page backgrounds) and always on the cover. Armon Rama, for example, requires 3 mm on each side. |
| Margins | Inside 22, outside 20, top 28, bottom 22 mm | Dfus Eichut suggests 2.8 cm top and 2.2 cm bottom when there is a running head; PrintaBook asks for at least 1.5 cm. Make the inside margin larger for thick books. |
| Page numbers | Hebrew letters for sefarim, digits for memoirs and academic books | Hebrew letters without geresh or gershayim, as the Academy of the Hebrew Language rules for page numbers. |
| Chapter start | Next page | `odd` makes every chapter open on a recto; the blank pages it adds get no number. |
| Font | Frank Ruhl Libre | Free (SIL Open Font License), includes meteg. See Step 5. |
| Front matter | Title, imprint page on its back, then any dedication, approbations, introduction, table of contents | Sefarim usually carry approbations (הסכמות) and a dedication or memorial page (הקדשה / לעילוי נשמת); ask for them. |

A Word page count is not a book page count. Compute the cover only after the PDF exists.

### Step 2: Convert the Word file

**Route A (shell available).** Use pandoc's Typst writer and keep images:

```bash
pandoc manuscript.docx -t typst --extract-media=media -o body.typ
```

Hebrew text, nikkud and Word footnotes survive the conversion (footnotes become `#footnote[...]`). Text direction does not travel with it; the template in Step 4 sets it.

**Route B (chat surface, no shell, non-technical user).** Read the uploaded .docx and write the Typst source chapter by chapter (`ch01.typ`, `ch02.typ`, ...), using `=` for chapter titles, `==` for sections and `#footnote[...]` for notes. Escape Typst special characters (`#`, `$`, `*`, `_`, `@`, `<`) with a backslash, and write abbreviations with real gershayim and geresh (רש״י, ד׳).

Fidelity is the main risk on this route, especially for Torah text: carry every word, letter and nikkud mark over exactly as written, never retype from memory or "correct" anything. After each chapter, state its first and last sentence and its approximate word count so the user can compare it with the Word file, and ask them to check pesukim and sources by eye.

Give the user `references/book-template.typ` (a ready template with an imprint page and table of contents; fill in the title, author and the `____` details, and add one `#include` line per chapter). Then walk them through typst.app: create a free account, start an empty project, upload the .typ files and the font files (Frank Ruhl Libre, plus the Ezra SIL file SILEOT.ttf whenever the text quotes pesukim with teamim; without it those words show doubled letters or boxes), open `book.typ`, and download the PDF from the button at the top right. Long manuscripts do not fit in one reply: deliver one chapter per message and keep a running list of what is done. If the project gets too many files, merge chapters into fewer files.

### Step 3: Check and clean what pandoc produced

```bash
python3 scripts/inspect_body.py body.typ
```

It reports headings, footnotes, images, tables, quote marks inside abbreviations, cantillation marks, and short fully-bold lines. Then fix what it found:

```bash
python3 scripts/inspect_body.py body.typ --fix-quotes
python3 scripts/inspect_body.py body.typ --promote 1 --match '^פרק' --out step1.typ
python3 scripts/inspect_body.py step1.typ --promote 2 --out body.typ
```

- Word keeps a typewriter or curly quote in ראשי תיבות; a sefer has hundreds of them, and print should show ״ and ׳. `--fix-quotes` converts a quote before the last letter of a word (רש"י) and a quote after a letter that ends a word (ד'), and leaves an opening quotation after a prefix letter (ו"שלום") and a single-quoted phrase ('לא') alone. It also works when the letters carry nikkud (רַשִׁ"י).
- Many manuscripts fake chapter titles with bold text, which leaves the book with no chapters, table of contents or running heads. Show the user the promoted list before compiling; a bold line inside a poem is not a heading.
- If cantillation marks are reported, plan `--teamim-font` (Step 5). If meteg is reported, keep a body font that has it (Frank Ruhl Libre).

### Step 4: Generate the book template

```bash
python3 scripts/make_book.py --body body.typ --title "שם הספר" --author "שם המחבר" \
  --trim 148x210 --toc --numbering gematria --imprint \
  --year-published "____" --year-printed "____" \
  --publisher "שם המחבר" --publisher-address "כתובת" --printer "שם הדפוס" --printer-address "כתובת הדפוס" \
  --dedication "לעילוי נשמת ..." --front-file haskamot.typ --front-file intro.typ \
  --out book.typ
```

What the template guarantees, and why each matters:

- `binding: right` with `inside` / `outside` margins. Typst binds right-to-left text on the right; never use `left` / `right` margins in a Hebrew book or the spine margin lands on the wrong side of every other page.
- The body always opens on a recto, so every odd page number falls on a recto, whatever the length of the front matter. Blank pages added to reach a recto get no page number and no running head.
- Front matter in Hebrew-book order: title, imprint page on its back (with the ISBN if one was issued), then dedication, the `--front-file` files (approbations, introduction) and the table of contents, each opening on a recto, all unnumbered. Headings inside front-matter files stay out of the table of contents, and the table of contents shows the same page numbers as the folios.
- Running heads: book title on even pages, current chapter on odd pages, none on a chapter's opening page.
- Hebrew-letter page numbers: 15 and 16 come out as טו and טז. Combinations such as רע are not reordered; for a long sefer, review the folios and adjust the `gematria` function in `book.typ`.
- Footnotes: `--footnote-reset chapter` restarts numbering in each chapter, `--footnote-numbering gematria` uses Hebrew letters, `--note-font` sets the notes in another font.
- `--bleed N` uses Typst's page bleed, which writes a TrimBox into the PDF so the print shop's software knows where to cut.
- `--pad-to N` adds blank pages at the end so the page count divides by the shop's signature size. The default is 2, so the PDF always has an even page count.
- The title and author are inserted as literal text, so quotes and characters such as `#` or `*` in a title print as typed.

Run `python3 scripts/make_book.py --help` for every option (font size, leading, indent, chapter start, gershayim on folios).

Indexes (מפתח פסוקים, מפתח עניינים) are not generated; if the user wants one, it is compiled by hand from the final page numbers.

### Step 5: Fonts, nikkud and teamim

| Need | Font | License |
|---|---|---|
| Body text with nikkud and meteg | Frank Ruhl Libre | SIL Open Font License 1.1 |
| Body text with nikkud, no meteg in the text | David Libre | SIL Open Font License 1.1 |
| Rashi script for commentary or notes (`--note-font`) | Noto Rashi Hebrew | SIL Open Font License 1.1 |
| Pesukim with teamim (`--teamim-font "Ezra SIL"`) | Ezra SIL | SIL Open Font License |
| Culmus family (Frank Ruehl CLM, David CLM and more) | Check each font | Read the license of each font before embedding it in a sold book |

Frank Ruhl Libre and David Libre have no cantillation marks, and David Libre has no meteg. Do NOT rely on automatic fallback to another font for those marks: the missing mark gets patched from a second font letter by letter, which can duplicate letters inside the word (בראשְשִׁית) and mix typefaces mid-word. `--teamim-font` instead sets every whole word that carries a cantillation mark in the teamim font; words with meteg follow it only when the body font lacks meteg (automatic for David Libre, or `--meteg-in-teamim-font`), so vocalized poetry stays in one typeface. Ezra SIL looks slightly larger than the body text, which is normal for quoted pesukim. Alternatively, set the whole book in Ezra SIL with `--font "Ezra SIL"`. The no-install template already includes the teamim rule.

Pass the font folder with `--font-path fonts`. On typst.app, upload the .ttf files into the project. Commercial Windows fonts (David, Narkisim) may not be licensed for embedding in a sold book; switch to an OFL font rather than guess.

Proof nikkud and teamim on rendered pages, not in a text extract: copy-paste from a PDF scrambles combining marks even when the print is correct. Render every page that has pesukim, not a sample:

```bash
typst compile --font-path fonts --format png --ppi 110 book.typ 'proof-{p}.png'
```

### Step 6: Compile and proof

```bash
typst compile --font-path fonts book.typ book.pdf
```

Proof checklist to give the user:

- Open the PDF in two-page view: the wider margin faces the spine, odd page numbers sit on rectos, blank pages are unnumbered.
- Numbers and English words inside Hebrew lines read in the right order (dates, verse references, years).
- Abbreviations show ״ and ׳, and a joining dash in Hebrew is a maqaf (־) where the author intended one.
- Every chapter appears in the table of contents with the right page.
- Footnotes land on the same page as their marker.
- Typst already avoids most single lines stranded at the top or bottom of a page; fix any left with a manual `#pagebreak()` only after the text is final.
- Images: ask the shop for the resolution and colour mode it needs; colour pages inside the book usually change the price.
- Fonts are embedded: Typst embeds them by default.

### Step 7: Hand off to the print shop

Print shops ask for a closed PDF, never Word, with the interior and the cover as two separate files and the interior as single consecutive pages (not spreads). Before sending, ask the shop for: trim size, bleed, minimum inner margin, whether the page count must divide by a fixed number (then use `--pad-to`), paper type and its thickness (caliper), and whether they require PDF/X.

Typst exports PDF 1.4 to 2.0, PDF/A and PDF/UA, but not PDF/X. If the shop insists on PDF/X, say so plainly: most shops convert the file in their preflight, or the user can export it from a PDF tool such as Acrobat's preflight. Do not claim the file is PDF/X.

Cover: compute the canvas once the page count is final.

```bash
python3 scripts/cover_size.py --pages 212 --caliper 0.1 --trim 148x210 --bleed 3 --multiple 16
```

The spine is leaves (pages divided by 2) times the paper thickness from the shop. Multiplying pages instead of leaves doubles the spine. A Hebrew book opens from the right, so on the flat cover sheet the FRONT cover is the left-hand panel: [front] [spine] [back]. A stapled booklet has no spine. For a hardcover or a cover with flaps (כנפיים), ask the binder for their layout (פריסה) instead of computing it. Request a proof copy and measure its real spine before the full run.

### Step 8: Imprint page, ISBN and legal deposit

**Imprint page (the back of the title page).** Section 3 of the Books Law (Duty of Delivery and Specification of Particulars), 5761-2000, requires every book published in Israel to state the year of publication, the year of printing, the name and address of the printer and of the publisher, and that it was published in Israel. A self-publishing author is the publisher. `--imprint` builds this page; any detail not passed stays as `____` so it cannot be forgotten silently. Books for a limited audience such as family members or guests at a private event are exempt under the Books Regulations.

**ISBN (מסת"ב).** Optional, issued in Israel by the Israel Center for Libraries (not the National Library). Per its price list (check before ordering, prices change), a single number costs 160 NIS without a barcode or 195 NIS with one, standard allocation takes 5 working days, and only 4 single numbers can be bought before moving to blocks. Print it on the back of the title page (`--isbn`) and on the back cover (barcode on the back cover). Softcover and hardcover each need their own number, and so does a revised edition. An ISBN does not protect copyright and is not part of legal deposit.

**Legal deposit.** A book offered to the public in 50 or more copies, paid or free, must be deposited: 2 complete copies, free, to the National Library within 30 days of publication. Use the National Library's online deposit form, which issues a deposit number, then bring or mail the copies. A later edition with any change in content or form must be deposited again. State the rule and let the user apply it to their print run; see `references/isbn-and-deposit.md` for the Knesset Library and State Archives copies and the penalty.

## Examples

### Example 1: Chidushei torah, 100 Word pages

User says: "יש לי קובץ וורד של 100 עמודים עם חידושי תורה וכותרות, אני רוצה לעמד אותו כספר להדפסה"

Actions:
1. Ask for the print shop's spec and binding; default to 17 x 24 cm with Hebrew-letter page numbers. Ask about approbations and a memorial page.
2. `pandoc` to `body.typ`; `inspect_body.py` reports bold lines starting with סימן, quote marks in abbreviations, and cantillation marks.
3. `--fix-quotes`, then promote the סימן lines to headings.
4. `make_book.py --trim 170x240 --numbering gematria --toc --imprint --teamim-font "Ezra SIL" --footnote-reset chapter --front-file haskamot.typ --dedication "..."`.
5. Render every page with pesukim to PNG and check the marks.
6. Explain the deposit rule (50 copies offered to the public) and that an ISBN is optional.

Result: `book.pdf` with front matter in order, odd folios on rectos, a TrimBox, and a print-shop checklist.

### Example 2: Family memoir on a chat surface

User says: "כתבתי ספר זיכרונות לסבא, 30 עותקים למשפחה. אין לי מושג בתוכנות."

Actions:
1. Route B: convert chapter by chapter, one message per chapter, with first and last sentence for checking; give `references/book-template.typ` set to digit page numbers.
2. Walk the user through typst.app upload and PDF download.
3. Explain the rule: deposit applies only to a book offered to the public in 50 or more copies, and the Books Regulations exempt editions for a limited audience such as family members; an ISBN is optional.

Result: a print-ready A5 PDF made without installing anything.

### Example 3: Poetry with nikkud and photos

User says: "ספר שירה מנוקד עם תמונות שיוצאות עד הקצה"

Actions: `--extract-media=media` in pandoc; `--bleed 3` (or the shop's figure); proof nikkud as PNG; check image resolution and colour with the shop; compute the cover with `cover_size.py`.

Result: interior PDF with bleed and TrimBox, cover dimensions, and a list of questions for the shop.

## Bundled Resources

### Scripts
- `scripts/make_book.py` -- Generates the Typst book template (trim, bleed, right-bound mirrored margins, recto-safe page numbering, front matter with imprint page, running heads, footnote options, teamim font, padding). Run: `python3 scripts/make_book.py --help`
- `scripts/inspect_body.py` -- Reports what pandoc found, converts quotes to gershayim and geresh, and promotes bold-only lines to headings. Run: `python3 scripts/inspect_body.py --help`
- `scripts/cover_size.py` -- Spine width and the flat cover canvas for a right-bound paperback. Run: `python3 scripts/cover_size.py --help`

### References
- `references/book-template.typ` -- Ready-made template for the no-install route (A5, imprint page, table of contents). Consult when the user cannot run scripts.
- `references/print-shop-handoff.md` -- Questions to ask the shop, per-shop figures with sources, PDF requirements and the spine formula. Consult before sending files to a printer.
- `references/isbn-and-deposit.md` -- ISBN prices and rules, the Books Law duties, the limited-audience exemption, the other copies and the penalty. Consult when the user asks about ISBN, deposit or the imprint page.

## Gotchas

- Agents bind Hebrew books on the left and lay out covers like English books. A Hebrew book is bound on the right, and the flat cover reads [front] [spine] [back] from left to right.
- Agents restart page numbers without forcing a recto, so odd folios land on versos once the front matter has an odd page count. The body must open on a recto.
- Agents let a fallback font supply teamim or meteg, which duplicates letters inside the word. Set those words whole in a font that has the marks.
- Agents compute the spine from pages instead of leaves, doubling it.
- Agents write 15 and 16 as yud-heh and yud-vav, and add gershayim to page numbers. Use טו / טז, and no geresh or gershayim on page numbers.
- Agents say the National Library issues ISBNs or that an ISBN protects copyright. The Israel Center for Libraries issues them, and they protect nothing.
- Agents tell every author to deposit copies. The duty applies only from 50 copies offered to the public, and family or private-event books are exempt.
- Agents claim a Typst PDF is PDF/X. It is not; Typst offers PDF/A and PDF/UA only.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Books Law, 5761-2000 (Wikisource) | https://he.wikisource.org/wiki/חוק_הספרים_(חובת_מסירה_וציון_הפרטים) | Deposit copies, 30-day deadline, 50-copy threshold, section 3 particulars |
| Books Regulations (Wikisource) | https://he.wikisource.org/wiki/תקנות_הספרים_(חובת_מסירה_וציון_הפרטים) | Limited-audience exemption, digital deposit |
| National Library, depositing | https://www.nli.org.il/he/at-your-service/who-we-are/depositing | Online deposit form and procedure |
| Israel Center for Libraries, ISBN | https://icl.org.il/isbn | ISBN prices, delivery time, placement rules |
| Typst page reference | https://typst.app/docs/reference/layout/page/ | Binding, inside/outside margins, bleed |
| Typst PDF export | https://typst.app/docs/reference/pdf/ | Supported PDF standards |

## Troubleshooting

### Error: "unknown font family"
Cause: Typst cannot see the font. Verified: Typst does not find a font that is not installed or passed with `--font-path`.
Solution: Put the .ttf files in `fonts/` and compile with `--font-path fonts`; on typst.app, upload them into the project.

### Letters doubled or boxes inside pesukim
Cause: the body font has no cantillation marks (or no meteg) and another font filled them in letter by letter, or no font had them at all. Verified with Frank Ruhl Libre and David Libre, which have no teamim.
Solution: compile with `--teamim-font "Ezra SIL"` (font file in `fonts/`), or set the whole book in Ezra SIL.

### Odd page numbers on left-hand pages
Cause: a template that restarts numbering without forcing a recto. `make_book.py` forces it; a hand-edited `book.typ` may have lost the `#recto()` line before `counter(page).update(1)`.
Solution: regenerate with `make_book.py`, or restore that line.

### Nikkud looks scrambled when copied out of the PDF
Cause: text extraction reorders combining marks; the printed page can still be correct.
Solution: Proof from rendered PNG pages (Step 5), not from copied text.

### The table of contents is empty
Cause: pandoc found no headings, usually because chapter titles were typed as bold text.
Solution: `inspect_body.py --promote 1`, then regenerate.
