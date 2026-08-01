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
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  PageBreak, Header, Footer, PageNumber, ImageRun, VerticalAlign, TableLayoutType
} = require('docx');
const fs = require('fs');

// ---- adjust these to match your document / extracted reference colors ----
const FONT = "Arial";          // solid Hebrew glyph coverage; swap for "David" if source uses a serif
const BRAND_BLUE = "015289";   // example - replace with a color actually extracted from the reference logo
const GRAY_LINE = "BFBFBF";
const LOGO_PATH = "./assets/logo.png"; // see references/logo-extraction.md for how to obtain this
const LOGO_W = 350, LOGO_H = 288;      // native pixel dimensions of the extracted logo asset

function logoImage(scale) {
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(LOGO_PATH),
    transformation: { width: Math.round(LOGO_W * scale), height: Math.round(LOGO_H * scale) }
  });
}

// ================= BASIC RTL PARAGRAPH HELPERS =================

// Every Hebrew paragraph needs bidirectional:true + RIGHT alignment; every run needs rightToLeft:true.
function p(text, opts = {}) {
  const {
    bold = false, size = 21, align = AlignmentType.RIGHT, italics = false,
    color = null, spacingAfter = 120, spacingBefore = 0, indent = null, border = null
  } = opts;
  return new Paragraph({
    alignment: align,
    bidirectional: true,
    spacing: { after: spacingAfter, before: spacingBefore },
    indent: indent || undefined,
    border: border || undefined,
    children: [new TextRun({ text, bold, italics, size, rightToLeft: true, color: color || undefined, font: FONT })]
  });
}

function heading1(text, opts = {}) {
  const { spacingBefore = 300 } = opts;
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    alignment: AlignmentType.RIGHT,
    bidirectional: true,
    spacing: { before: spacingBefore, after: 200 },
    children: [new TextRun({ text, bold: true, size: 30, color: BRAND_BLUE, rightToLeft: true, font: FONT })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    alignment: AlignmentType.RIGHT,
    bidirectional: true,
    spacing: { before: 260, after: 140 },
    // thin top rule = cheap visual separator between repeated blocks (questions, entries, etc.)
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: GRAY_LINE, space: 8 } },
    children: [new TextRun({ text, bold: true, size: 24, color: BRAND_BLUE, rightToLeft: true, font: FONT })]
  });
}

// ================= RTL TABLE CELL HELPER =================
// Remember: set `visuallyRightToLeft: true` on the Table itself, then define columns in the
// order you want them to appear reading right-to-left (rightmost column defined first).
function cell(text, opts = {}) {
  const { bold = false, width, shade = null, align = AlignmentType.RIGHT, size = 19 } = opts;
  return new TableCell({
    width: width != null ? { size: width, type: WidthType.DXA } : undefined,
    shading: shade ? { type: ShadingType.CLEAR, fill: shade } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: [p(text, { bold, size, align, spacingAfter: 0 })]
  });
}

// ================= RUNNING HEADER (matches: text block physically left, logo physically right) =================
function buildHeader({ productLine, subtitleLine, noteLine }) {
  const table = new Table({
    width: { size: 9350, type: WidthType.DXA },
    columnWidths: [7350, 2000], // NOT visuallyRightToLeft: keeps logo pinned to physical right like most brand templates
    layout: TableLayoutType.FIXED,
    borders: {
      top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: GRAY_LINE },
      left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }
    },
    rows: [new TableRow({
      children: [
        new TableCell({
          width: { size: 7350, type: WidthType.DXA },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            new Paragraph({ alignment: AlignmentType.RIGHT, bidirectional: true, spacing: { after: 20 },
              children: [new TextRun({ text: productLine, bold: true, size: 18, rightToLeft: true, font: FONT })] }),
            new Paragraph({ alignment: AlignmentType.RIGHT, bidirectional: true, spacing: { after: 20 },
              children: [new TextRun({ text: subtitleLine, bold: true, size: 18, rightToLeft: true, font: FONT })] }),
            new Paragraph({ alignment: AlignmentType.RIGHT, bidirectional: true,
              children: [new TextRun({ text: noteLine, italics: true, size: 15, rightToLeft: true, font: FONT })] })
          ]
        }),
        new TableCell({
          width: { size: 2000, type: WidthType.DXA },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [logoImage(0.135)] })]
        })
      ]
    })]
  });
  return new Header({ children: [table] });
}

function buildEmptyHeader() {
  return new Header({ children: [new Paragraph({ children: [] })] }); // used for the cover/title page
}

// ================= RUNNING FOOTER (live page count + version/date) =================
function buildFooter({ versionLabel, dateLabel }) {
  return new Footer({
    children: [
      new Paragraph({
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: GRAY_LINE, space: 6 } },
        alignment: AlignmentType.CENTER, bidirectional: true, spacing: { before: 60, after: 20 },
        children: [
          new TextRun({ text: "עמוד ", size: 17, rightToLeft: true, font: FONT }),
          new TextRun({ children: [PageNumber.CURRENT], size: 17, font: FONT }),      // live field - works in Word + LibreOffice
          new TextRun({ text: " מתוך ", size: 17, rightToLeft: true, font: FONT }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 17, font: FONT }),  // live field
          new TextRun({ text: `    |    ${versionLabel}    |    ${dateLabel}`, size: 17, rightToLeft: true, font: FONT })
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
        children: [p(title, { bold, size: 20, spacingAfter: 0 })]
      }),
      new TableCell({
        width: { size: 900, type: WidthType.DXA },
        borders: { bottom: { style: BorderStyle.DOTTED, size: 4, color: "999999" } },
        margins: { bottom: 40, top: 40 },
        children: [p(String(pageNum), { size: 20, align: AlignmentType.CENTER, spacingAfter: 0 })]
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
        document: { run: { font: FONT, size: 21, rightToLeft: true }, paragraph: { alignment: AlignmentType.RIGHT } }
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

module.exports = {
  FONT, BRAND_BLUE, GRAY_LINE, logoImage,
  p, heading1, heading2, cell,
  buildHeader, buildEmptyHeader, buildFooter,
  tocRow, buildTocTable, buildDocumentSkeleton
};
