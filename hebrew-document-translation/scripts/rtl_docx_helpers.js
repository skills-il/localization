/**
 * rtl_docx_helpers.js
 *
 * Copy-paste scaffold for building professionally formatted, bilingual (Hebrew RTL / English LTR)
 * Word documents with docx-js. This is NOT a script you run as-is - copy the pieces you need into
 * your document's build script and adapt the copy, colors, and logo path.
 *
 * See /mnt/skills/public/docx/SKILL.md for general docx-js creation mechanics and gotchas first.
 * See ../references/logo-extraction.md and ../references/toc-pagination.md for the two trickiest
 * parts of matching a reference template exactly.
 */

const {
  Document, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  PageBreak, Header, Footer, PageNumber, ImageRun, VerticalAlign, TableLayoutType
} = require('docx');
const fs = require('fs');
// Install both packages directly: `npm i docx jszip`. jszip is only needed by packRtlDocx(), and
// relying on docx's own copy breaks under pnpm / Yarn PnP / nested installs that don't hoist it.

// ---- adjust these to match your document / extracted reference colors ----
const FONT = "Arial";          // solid Hebrew glyph coverage; swap for "David" if source uses a serif
const BRAND_BLUE = "015289";   // example - replace with a color actually extracted from the reference logo
const GRAY_LINE = "BFBFBF";
const LOGO_PATH = "./assets/logo.png"; // optional - see references/logo-extraction.md for how to obtain one
const LOGO_W = 350, LOGO_H = 288;      // native pixel dimensions of the extracted logo asset

// Returns null when there is no logo file, so a document with no reference template still builds
// (callers omit the logo cell instead of failing with ENOENT).
function logoImage(scale, logoPath = LOGO_PATH) {
  if (!logoPath || !fs.existsSync(logoPath)) return null;
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(logoPath),
    transformation: { width: Math.round(LOGO_W * scale), height: Math.round(LOGO_H * scale) }
  });
}

// ================= SCRIPT-AWARE RUN SPLITTING =================
// Hebrew Unicode block (letters, punctuation, points).
const HEBREW_CHAR = /[\u0590-\u05FF]/;
const LATIN_CHAR = /[A-Za-z]/;

// Word honors run-level rightToLeft strictly: any Latin letter or number in (or beside) an
// rtl-flagged run in a MIXED paragraph gets force-reversed ("7/2023" prints as "2023/7") and
// parentheses mis-pair. The rule (same as the hebrew-document-generator skill, verified in Word):
//   - paragraph contains Latin letters -> NO run gets rightToLeft; the paragraph's own
//     bidirectional:true orders the line.
//   - paragraph has no Latin letters (digits allowed) -> flag rightToLeft on the Hebrew runs only.
// Text is still split per script segment so each run can carry its own font settings.
// Pass `paragraphText` when these runs are only part of a paragraph (e.g. next to other runs),
// so the Latin check covers the whole paragraph, not just this fragment.
// A leading 1-2 digit list marker ("2. ", "10. ") is merged into the Hebrew segment that follows
// it, so it rides inside the rtl-flagged run; as its own neutral run Word floats the period to the
// wrong side (".2"). Only digits + period match, so a date like 13/01/2026 stays its own LTR run.
const LIST_MARKER = /^\s*\d{1,2}\.\s*$/;

function scriptRuns(text, runOpts = {}, paragraphText = text) {
  const mixed = LATIN_CHAR.test(String(paragraphText));
  const segments = String(text).match(/[\u0590-\u05FF]+|[^\u0590-\u05FF]+/g) || [String(text)];
  if (segments.length >= 2 && LIST_MARKER.test(segments[0]) && HEBREW_CHAR.test(segments[1])) {
    segments.splice(0, 2, segments[0] + segments[1]);
  }
  return segments.map(segment => new TextRun({
    ...runOpts,
    text: segment,
    rightToLeft: !mixed && HEBREW_CHAR.test(segment)
  }));
}

// ================= BASIC RTL PARAGRAPH HELPERS =================

// Base direction comes from the text: any Hebrew -> bidirectional + RIGHT; no Hebrew (an English
// brand/code line) -> LTR + LEFT, so it doesn't hug the right margin. Run-level rightToLeft is
// decided by scriptRuns (see the rule above), never set by hand.
function baseDirection(text) {
  const rtl = HEBREW_CHAR.test(String(text));
  return { bidirectional: rtl, alignment: rtl ? AlignmentType.RIGHT : AlignmentType.LEFT };
}

function p(text, opts = {}) {
  const {
    bold = false, size = 21, align = null, italics = false,
    color = null, spacingAfter = 120, spacingBefore = 0, indent = null, border = null
  } = opts;
  const dir = baseDirection(text);
  return new Paragraph({
    alignment: align || dir.alignment,
    bidirectional: dir.bidirectional,
    spacing: { after: spacingAfter, before: spacingBefore },
    indent: indent || undefined,
    border: border || undefined,
    children: scriptRuns(text, { bold, italics, size, color: color || undefined, font: FONT })
  });
}

function heading1(text, opts = {}) {
  const { spacingBefore = 300 } = opts;
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    ...baseDirection(text),
    spacing: { before: spacingBefore, after: 200 },
    children: scriptRuns(text, { bold: true, size: 30, color: BRAND_BLUE, font: FONT })
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    ...baseDirection(text),
    spacing: { before: 260, after: 140 },
    // thin top rule = cheap visual separator between repeated blocks (questions, entries, etc.)
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: GRAY_LINE, space: 8 } },
    children: scriptRuns(text, { bold: true, size: 24, color: BRAND_BLUE, font: FONT })
  });
}

// ================= RTL TABLE CELL HELPERS =================
// Remember: set `visuallyRightToLeft: true` on the Table itself, then define columns in the
// order you want them to appear reading right-to-left (rightmost column defined first).
//
// Cell paragraphs deliberately set NO alignment by default. OOXML `w:jc` is logical: "right" is
// the END of the line, which in a bidirectional paragraph is the visual LEFT. An RTL cell
// paragraph with alignment unset starts at its visual right edge, so Hebrew text and numbers line
// up flush right together (same rule as hebrew-document-generator's set_cell_rtl_text).
function cellParagraph(text, opts = {}) {
  const { bold = false, size = 19, align = undefined, color = null } = opts;
  return new Paragraph({
    alignment: align,
    bidirectional: true,
    spacing: { after: 0 },
    children: scriptRuns(text, { bold, size, color: color || undefined, font: FONT })
  });
}

function cell(text, opts = {}) {
  const { bold = false, width, shade = null, align = undefined, size = 19 } = opts;
  return new TableCell({
    width: width != null ? { size: width, type: WidthType.DXA } : undefined,
    shading: shade ? { type: ShadingType.CLEAR, fill: shade } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: [cellParagraph(text, { bold, size, align })]
  });
}

// ================= RUNNING HEADER (two physically-LTR columns: text column defined first so it
// sits on the physical left, logo column physical right; text inside the left column is itself
// right-aligned so Hebrew reads naturally). The logo column is dropped when there is no logo
// file, so the header also works for documents with no reference template =================
function buildHeader({ productLine, subtitleLine, noteLine, logoPath = LOGO_PATH }) {
  const logo = logoImage(0.135, logoPath);
  const textWidth = logo ? 7350 : 9350;
  const textCell = new TableCell({
    width: { size: textWidth, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    children: [
      new Paragraph({ alignment: AlignmentType.RIGHT, bidirectional: true, spacing: { after: 20 },
        children: scriptRuns(productLine, { bold: true, size: 18, font: FONT }) }),
      new Paragraph({ alignment: AlignmentType.RIGHT, bidirectional: true, spacing: { after: 20 },
        children: scriptRuns(subtitleLine, { bold: true, size: 18, font: FONT }) }),
      new Paragraph({ alignment: AlignmentType.RIGHT, bidirectional: true,
        children: scriptRuns(noteLine, { italics: true, size: 15, font: FONT }) })
    ]
  });
  const cells = [textCell];
  if (logo) {
    cells.push(new TableCell({
      width: { size: 2000, type: WidthType.DXA },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [logo] })]
    }));
  }
  const table = new Table({
    width: { size: 9350, type: WidthType.DXA },
    columnWidths: logo ? [7350, 2000] : [9350], // NOT visuallyRightToLeft: keeps logo pinned to physical right like most brand templates
    layout: TableLayoutType.FIXED,
    borders: {
      top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: GRAY_LINE },
      left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }
    },
    rows: [new TableRow({ children: cells })]
  });
  return new Header({ children: [table] });
}

function buildEmptyHeader() {
  return new Header({ children: [new Paragraph({ children: [] })] }); // used for the cover/title page
}

// ================= RUNNING FOOTER (live page count + version/date) =================
function buildFooter({ versionLabel, dateLabel }) {
  // One paragraph = one Latin check: if the version/date labels contain Latin letters, the
  // Hebrew runs here must not carry rightToLeft either (see scriptRuns).
  const tail = `    |    ${versionLabel}    |    ${dateLabel}`;
  const rtl = !LATIN_CHAR.test(tail);
  return new Footer({
    children: [
      new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: GRAY_LINE, space: 6 } },
        alignment: AlignmentType.CENTER, bidirectional: true, spacing: { before: 60, after: 20 },
        children: [
          new TextRun({ text: "עמוד ", size: 17, rightToLeft: rtl, font: FONT }),
          new TextRun({ children: [PageNumber.CURRENT], size: 17, font: FONT }),      // live field - works in Word + LibreOffice
          new TextRun({ text: " מתוך ", size: 17, rightToLeft: rtl, font: FONT }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 17, font: FONT }),  // live field
          ...scriptRuns(tail, { size: 17, font: FONT })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "© Your Organization Name", size: 15, font: FONT, color: "666666" })]
      })
    ]
  });
}

// ================= TOC ROW (static, verified page numbers - see references/toc-pagination.md) =================
function tocRow(title, pageNum, opts = {}) {
  const { bold = false } = opts;
  return new TableRow({
    children: [
      new TableCell({
        width: { size: 8200, type: WidthType.DXA },
        borders: { bottom: { style: BorderStyle.DOTTED, size: 4, color: "999999" } },
        margins: { bottom: 40, top: 40 },
        children: [cellParagraph(title, { bold, size: 20 })] // no alignment: RTL start edge = visual right
      }),
      new TableCell({
        width: { size: 900, type: WidthType.DXA },
        borders: { bottom: { style: BorderStyle.DOTTED, size: 4, color: "999999" } },
        margins: { bottom: 40, top: 40 },
        children: [cellParagraph(String(pageNum), { size: 20, align: AlignmentType.CENTER })]
      })
    ]
  });
}

function buildTocTable(rows) {
  return new Table({
    width: { size: 9100, type: WidthType.DXA },
    columnWidths: [8200, 900],
    visuallyRightToLeft: true, // title column reads on the right, page number on the left - standard Hebrew TOC convention
    borders: {
      top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }
    },
    rows
  });
}

// ================= DOCUMENT ASSEMBLY SKELETON =================
// A typical section: title page (separate first-page header/footer) + running header/footer elsewhere.
function buildDocumentSkeleton({ coverChildren, bodyChildren, header, footer, coverFooter }) {
  return new Document({
    styles: {
      default: {
        // Only font/size here. No rightToLeft or paragraph alignment in the defaults: anything that
        // doesn't set them (page-number fields, English cover content passed in coverChildren)
        // would inherit RTL. Direction and alignment are set per paragraph/run instead.
        document: { run: { font: FONT, size: 21 } }
      }
    },
    sections: [{
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1500, bottom: 1300, left: 1100, right: 1100 } }, // A4
        titlePage: true // enables a distinct first-page header/footer (usually blank/simple on the cover)
      },
      headers: { default: header, first: buildEmptyHeader() },
      footers: { default: footer, first: coverFooter },
      children: [...coverChildren, new Paragraph({ children: [new PageBreak()] }), ...bodyChildren]
    }]
  });
}

// ================= SECTION-LEVEL RTL (sectPr <w:bidi/>) =================
// docx-js has no section option for <w:bidi/>, so paragraphs can be RTL while the section itself
// (page flow, mirrored margins/gutter, header/footer flow) stays LTR. Pack with this instead of
// Packer.toBuffer: it adds <w:bidi/> to every sectPr. Schema order puts w:bidi after titlePg/
// textDirection and before rtlGutter/docGrid, so it is inserted ahead of those when present.
async function packRtlDocx(doc) {
  const { Packer } = require('docx');
  const JSZip = require('jszip'); // direct dependency: `npm i docx jszip`
  const zip = await JSZip.loadAsync(await Packer.toBuffer(doc));
  const xml = await zip.file('word/document.xml').async('string');
  const patched = xml.replace(/<w:sectPr\b[^>]*>[\s\S]*?<\/w:sectPr>/g, sect => {
    if (sect.includes('<w:bidi/>')) return sect;
    const anchor = sect.search(/<w:(rtlGutter|docGrid|printerSettings|sectPrChange)\b/);
    const at = anchor >= 0 ? anchor : sect.lastIndexOf('</w:sectPr>');
    return sect.slice(0, at) + '<w:bidi/>' + sect.slice(at);
  });
  zip.file('word/document.xml', patched);
  return zip.generateAsync({ type: 'nodebuffer' });
}

module.exports = {
  FONT, BRAND_BLUE, GRAY_LINE, logoImage,
  scriptRuns, p, heading1, heading2, cellParagraph, cell,
  buildHeader, buildEmptyHeader, buildFooter,
  tocRow, buildTocTable, buildDocumentSkeleton, packRtlDocx
};
