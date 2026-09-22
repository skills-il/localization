---
name: hebrew-document-translation
description: Translate documents (PDF, Word, plain text) from English into professional, publication-quality Hebrew, preserving structure, formatting, tables, and terminology, with correct RTL layout. Works for any document type or subject matter (reports, contracts, manuals, marketing materials, legal or financial documents, correspondence, exams, or anything else) and for any organization or field, nothing about this skill is specific to one industry. Use this whenever the user asks to translate any document into Hebrew; whenever they want a Hebrew translation delivered as a proper Word/PDF file rather than plain chat text; and whenever they ask a new translation to "match", "align to", or "look like" the style/template of a previous or reference Hebrew document (cover page, headers/footers, table of contents, table styling, terminology). Also use when the user asks to build a reusable template/skill for this kind of translation work.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(node:*) Bash(npm:*) Bash(pdfimages:*) Bash(pdftotext:*) Bash(pdfinfo:*) Bash(grep:*) Bash(mkdir:*)
compatibility: Requires Node.js with the docx package for document generation, Python 3 with Pillow (PIL) for logo/color extraction, and poppler-utils (pdfimages, pdftotext, pdfinfo) plus LibreOffice for PDF rendering and verification.
---

# Hebrew Document Translation

Produces accurate, professionally formatted Hebrew translations of English documents of any kind,
reports, contracts, manuals, marketing copy, legal or financial documents, correspondence, exams,
or anything else, from any organization or field. It matches the visual and structural conventions
of real published Hebrew documents (title pages, running headers/footers, tables of contents with
correct page numbers, tables, RTL text flow). None of the mechanics below are specific to a
particular subject matter, treat the source document's own content and house style as the guide
to *what* it says; this skill is about *how* to render that faithfully in Hebrew.

Always check `/mnt/skills/public/docx/SKILL.md` first, this skill assumes and builds on it for
`docx` creation mechanics (docx-js gotchas, verification via LibreOffice, etc.). This skill adds
the Hebrew/RTL-specific layer on top.

## Instructions

### Step 1: Understand the deliverable

Ask (briefly, or infer from context) before building:

1. **Source**: a specific uploaded file, or free text to translate?
2. **Output format**: plain chat reply, Markdown file, or a formatted Word document (.docx)?
   - A short passage/summary → answer inline, no file.
   - A standalone document the user will keep/share/print (report, contract, manual, letter, exam,
     marketing piece, or anything else) → `.docx`.
3. **Template to match**: is there a reference document (previously translated, or a company
   template) whose look-and-feel the new translation should mirror? If the user says "make it
   match X" or shares an existing Hebrew doc, treat that doc as the authoritative style guide,
   don't invent a new layout. Extract its structure and colors directly (see Step 3).
4. **Register**: is this an official/branded document (needs cover page, running header/footer,
   TOC) or an informal one-off (simple translated body text is enough)?

If there's no reference template and the document is a real deliverable, a clean default is:
title page → copyright/front matter (if applicable) → table of contents → body, using the
running-header/footer pattern in `scripts/rtl_docx_helpers.js`.

### Step 2: Translate, don't transliterate

- Full sentences in natural, professional Hebrew, never word-for-word/machine-literal phrasing.
  Reread each translated sentence and ask "would a Hebrew-speaking professional actually write this?"
- **Keep acronyms, product/brand names, and field-specific standards or codes in English**,
  embedded inline in the Hebrew sentence, whatever those happen to be *in this particular
  document's field* (software terms like API/CI/CD in a tech manual, statute/clause numbers in a
  legal contract, drug or lab-test names in a medical report, ISO/accounting-standard codes in a
  financial document, etc.). This matches how real Hebrew professional documents are written in
  every field, don't force-translate or transliterate the source's acronyms and proper nouns just
  because they're in English. On first use of a term that has a common Hebrew equivalent, give the
  Hebrew phrase followed by the English term in parentheses, e.g. `בדיקות אינטגרציה (integration
  testing)` or `אחריות מוצר (product liability)`; after that, the shorter form is fine. When the
  exact expansion of an acronym in the source is itself a proper name/product term, keep it in
  English rather than translating the expansion. See `references/terminology-notes.md` for the
  general rule plus a couple of worked examples from different fields, treat any single field's
  glossary there as illustrative, not as a universal list to force onto an unrelated document.
- Prefer the more formal/official register word when the source is a formal document (the specific
  word depends entirely on the document's own field and house style, e.g. `לתשומת לב:` / `הערה:`
  for "Note:", or the more official synonym for a recurring role/concept term in whatever domain
  this document belongs to). If a reference document is available, copy its word choices exactly
  rather than picking your own synonym, consistency across a document family matters more than any
  single word's "correctness." Consistency also matters within one document: pick one term for a
  repeated concept and reuse it everywhere (don't alternate synonyms).
- Copyright/legal notices, disclaimers, and revision-history wording: translate precisely and
  completely, these are the sections most likely to be scrutinized. Keep organization names,
  product names, and `©` lines in their original English form/casing unless the reference template
  translates them too.
- This is a legitimate translation task on the user's own uploaded/authored content, not a
  copyright-restricted "reproduce web search results" scenario, translate the full document as
  requested. (The general copyright limits on quoting/reproducing *web search* results still apply
  separately and are unrelated to this kind of direct file translation.)

### Step 3: Match an existing template exactly, when one exists

When the user points at a reference Hebrew document (uploaded PDF/docx) to align to:

1. **Read its full text** (view the PDF/docx content) and note, precisely:
   - Cover page structure and copy order (what's English vs. Hebrew, bold/size/color hierarchy)
   - Running header/footer content and layout (what's on which side, page-number phrasing like
     `עמוד X מתוך Y`, version/date placement, copyright line language)
   - Section heading style and colors
   - How tables, numbered/lettered lists, and any other recurring structural patterns (e.g.
     multiple-choice options, clause lists, appendix items, whatever the document actually has)
     are formatted
   - Exact recurring phrases (translation disclaimers, standard boilerplate), reuse them verbatim
2. **Extract brand assets** (logos, icons) directly from the reference PDF rather than recreating
   them, see `references/logo-extraction.md`. Reuse the exact image in the new document's cover
   and running header for visual consistency.
3. **Extract colors** from those assets (e.g. via a quick Python/PIL dominant-color histogram) and
   reuse the same hex values for headings/titles, rather than guessing a similar-looking blue.
4. Build the new document with `scripts/rtl_docx_helpers.js` as the starting scaffold, adjusting
   copy/colors/logo to match what was just extracted.

### Step 4: RTL layout in docx-js

Hebrew documents need explicit RTL handling, Word does not infer it automatically from docx-js
output. See `scripts/rtl_docx_helpers.js` for ready-to-use helpers, and the rules behind them:

- Every `Paragraph` containing Hebrew needs `bidirectional: true` and `alignment: AlignmentType.RIGHT`.
- Every `TextRun` whose content is Hebrew needs `rightToLeft: true`. **Do not** flag a run
  `rightToLeft: true` if it mixes Hebrew with Latin letters or digits in one string, Word reorders
  and reflows a mixed run incorrectly (the Latin/digit portion can jump sides and punctuation can
  reflow), even though the paragraph itself is correctly `bidirectional`. This is the same failure
  mode documented for python-docx in the `hebrew-document-generator` skill; it applies equally here.
- Use a font with solid Hebrew glyph coverage, `Arial` renders cleanly and matches most
  corporate/professional templates; `David` is a reasonable serif alternative if the source uses one.
- **Tables**: set `visuallyRightToLeft: true` on any `Table` that should read right-to-left, this
  flips which physical side each defined column renders on. Define columns in your *logical* Hebrew
  reading order (rightmost column first) once `visuallyRightToLeft` is set.
- **Exception**: a header/footer table meant to mirror a Western brand-consistent layout (e.g. logo
  fixed to the physical right, text block fixed to the physical left, regardless of document
  language) should stay plain LTR (don't set `visuallyRightToLeft`), check the reference document
  for which convention it uses; don't assume.
- Mixed English/Hebrew inline (e.g. `NDA (Non-Disclosure Agreement)`) needs to be split into one
  `TextRun` per script segment, with `rightToLeft: true` only on the Hebrew segments, not one run
  covering the whole mixed string. Use the `scriptRuns()` helper in `scripts/rtl_docx_helpers.js`
  (used internally by `p()`, `heading1()`, `heading2()`, `buildHeader()`, and `buildFooter()`)
  instead of building a `TextRun` by hand for any text that might mix scripts.

### Step 5: Real, verified page numbers in the Table of Contents

Word's live `TableOfContents` field does **not** get recalculated by LibreOffice's headless PDF
conversion (used for verification in this environment), it renders blank. Two options:

- **Static TOC (recommended, most reliable across Word/LibreOffice/any PDF viewer)**: build the
  document once with placeholder page numbers, render it to PDF, programmatically find which PDF
  page each heading actually starts on, then hardcode those verified numbers into a plain
  two-column table (title + page number, right-to-left, with a dotted bottom border to mimic a
  leader line). Full recipe in `references/toc-pagination.md`. After inserting the real numbers,
  **re-render and re-check**, inserting the numbers can occasionally shift later pages by a line;
  don't assume the first pass is final.
- **Live field (only if the user will edit in Word and page numbers may change)**: use docx-js's
  `TableOfContents` with `updateFields`-style settings, and tell the user to right-click → "Update
  Field" after opening in Word. Don't rely on this if you need to *verify* correctness yourself in
  this environment.

For running-header/footer live page numbers (`עמוד X מתוך Y`), use the field-based approach, those
*do* work correctly in both Word and LibreOffice:
```js
new TextRun({ children: [PageNumber.CURRENT] })
new TextRun({ children: [PageNumber.TOTAL_PAGES] })
```

### Step 6: Verify before delivering

Always render and check before calling `present_files`:
```bash
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftotext -layout output.pdf -    # sanity-check Hebrew text, punctuation, embedded English terms
pdfinfo output.pdf | grep Pages   # confirm page count didn't shift after edits
```
`pdftotext` output for RTL text will look reordered/interleaved with bidi control characters when
piped to a terminal, that's a plain-text extraction artifact, not a real rendering bug. Judge
correctness by whether the Hebrew words, punctuation, and embedded English terms are all present
and undamaged, not by the raw left-to-right character order in the terminal dump. Also `view` a
rendered page image directly at least once for the cover and one content page, since that's the
only way to confirm the actual visual RTL layout, colors, and logo placement look right.

## Examples

### Example 1: Translating a business contract
User says: "Translate this service agreement into Hebrew, as a Word file ready for distribution"
Actions:
1. Identify it's a formal document → cover page, running header/footer, table of contents (if long enough)
2. Translate into formal legal Hebrew, keep clause/statute numbers and codes as in the source
3. Build with `scripts/rtl_docx_helpers.js`, set RTL on paragraphs, runs, and tables
4. Render to PDF, view the cover page and first content page
Result: A complete, formatted, and verified `.docx` file, delivered via `present_files`.

### Example 2: Matching an existing Hebrew document
User says: "I already have a previous translation of this guide/report, do the new chapter in exactly the same style"
Actions:
1. Read the previous document fully and record its cover page structure, running header/footer, colors, and recurring phrasing
2. Extract the logo and brand colors directly from the previous file (see `references/logo-extraction.md`)
3. Translate the new chapter, keeping the exact same word choices as the previous document
4. Build, render, and verify as in Steps 4-6
Result: A new chapter that looks like it came from the same production process as the previous document, regardless of field or organization.

## Bundled Resources

### Scripts
- `scripts/rtl_docx_helpers.js` - copy-paste-ready docx-js helper functions (paragraph/heading
  builders, header/footer/cover builders, RTL table cell helpers) used as the scaffold for any new
  bilingual Hebrew document. Consult when starting any new translated `.docx` build.

### References
- `references/logo-extraction.md` - how to pull a usable logo/image asset out of a reference PDF,
  including recovering transparency when the base color and alpha mask were embedded as two
  separate images. Consult when matching an existing branded template.
- `references/toc-pagination.md` - the render, discover, hardcode recipe for a correct, verified
  Table of Contents. Consult when the document needs a table of contents with real page numbers.
- `references/terminology-notes.md` - domain-agnostic Hebrew professional-translation conventions
  (English-retention rule, gender-neutral phrasing, consistency, numbers/codes/dates), plus a couple
  of small worked-example glossaries from specific fields. Consult as a style-rule reference, not
  as a fixed vocabulary to impose on every document.

## Reference Links

Official sources for verifying and updating the information in this skill:

| Source | URL | What to Check |
|--------|-----|---------------|
| docx (npm package) documentation | https://docx.js.org/ | API for Paragraph, TextRun, Table, Header/Footer, and the bidirectional/rightToLeft/visuallyRightToLeft options |
| Unicode Bidirectional Algorithm (UAX #9) | https://unicode.org/reports/tr9/ | The underlying rules for how mixed Hebrew/English text should reorder for display |
| Academy of the Hebrew Language (overview) | https://he.wikipedia.org/wiki/האקדמיה_ללשון_העברית | Starting orientation on the body that rules on official Hebrew style and terminology; cross-check against the Academy's own current guidance for binding rulings |
| poppler-utils documentation | https://poppler.freedesktop.org/ | pdfimages, pdftotext, pdfinfo usage and options |
| LibreOffice command-line documentation | https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html | --headless --convert-to usage and known limitations (e.g. TOC fields not recalculating) |

## Recommended MCP Servers

No MCP server applies to this skill. Hebrew document translation runs entirely through local
docx-js (Node), Python (Pillow) for asset extraction, and LibreOffice/poppler-utils for rendering
and verification; there is no external service to wrap as an MCP server. Use the bundled scripts
and the code in the Instructions section directly.

## Gotchas

- Assuming every document belongs to the software-testing/exam family - this skill is fully general
  and meant for any document type and field. Before choosing terminology, always check which field
  the *current* document actually belongs to, and don't assume the terminology that fit a previous
  document (e.g. software) also fits here.
- Translation that's too literal ("Google Translate style") sounds foreign to a professional Hebrew
  speaker, every sentence needs a pause and a check for whether a real Hebrew speaker would
  actually write it that way.
- Forgetting RTL on tables (`visuallyRightToLeft`) or on individual text runs (`rightToLeft: true`)
  produces a layout that looks like Hebrew "forced into" a document that's actually still LTR.
- Relying on a live `TableOfContents` field to *verify* correctness in this environment, it doesn't
  update on LibreOffice's headless rendering and shows blank. Build and verify actual page numbers
  instead (Step 5).
- Translating acronyms/product names into Hebrew "to make it sound more Hebrew", that's the exact
  opposite of what's expected in a real professional Hebrew document, in any field.
- Inconsistent terminology within the same document (switching between synonyms for one concept),
  pick one term and stick with it.

## Troubleshooting

### Error: "Table of contents shows blank after converting to PDF"
Cause: A live `TableOfContents` field isn't recalculated by LibreOffice's headless conversion.
Solution: Build a static table of contents with hardcoded, verified page numbers per
`references/toc-pagination.md`, rather than relying on a live field when you need to verify
correctness yourself.

### Error: "Extracted logo has a solid black background or inverted colors"
Cause: The PDF stored the logo as two separate images, a base RGB image and a separate grayscale
image that's actually the alpha mask.
Solution: Identify a pair of same-sized images (one RGB, one grayscale) and recombine them per the
recipe in `references/logo-extraction.md`.

### Error: "Hebrew text looks reversed/garbled when checked with pdftotext in the terminal"
Cause: This is an expected side effect of plain-text extraction versus bidi control characters, not
a rendering bug.
Solution: Check that the words, punctuation, and embedded English terms are present and intact (not
the character order), and also view an actual rendered page image for final visual confirmation.
