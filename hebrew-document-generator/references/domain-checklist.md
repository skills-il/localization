# Domain checklist: Hebrew document generation

Anchor for the Expert Review. Each row says why it is core and where the skill covers it.

## Must cover (core)

| Item | Why it is core | Covered in |
|------|----------------|------------|
| Hebrew-capable font registered for reportlab, with a failure when none is found | reportlab has no built-in Hebrew; a Latin font prints boxes | Step 2-3, `scripts/generate_doc.py` (glyph check, exit 2) |
| Bidi reordering for reportlab with bracket mirroring | reportlab draws glyphs in the order given; python-bidi's top-level Rust import does not mirror brackets (python-bidi issue #25) | Step 3, Mixed lines, Gotchas |
| Multi-line Hebrew wrapping in PDF, in logical order | Wrapping a reordered string reverses line order | Step 3, `wrap_hebrew_lines()` |
| WeasyPrint system dependencies (Pango) and `base_url` for fonts | Missing Pango fails to import; missing base_url silently drops the Hebrew font | Step 2, Step 4, Troubleshooting |
| DOCX paragraph base direction without explicit `jc` | `jc` is logical; right on RTL renders left in Word | Step 5 rule 1, `scripts/docx_rtl.py` |
| DOCX run direction: `w:rtl` on Hebrew runs, never on Latin/digit runs; neutrals resolved to the correct side | Word lays unflagged runs of a mixed line LTR, and reverses numbers inside rtl runs | Step 5 rule 2, `scripts/docx_rtl.py` |
| Complex-script font and size (`w:cs`, `w:szCs`, `w:bCs`, `w:iCs`) | Word applies ascii/sz/b/i only to Latin | Step 5 rule 3 |
| DOCX table column order (`bidiVisual`) and cell alignment | python-docx tables are LTR by default | Hebrew Tables in DOCX |
| PPTX `rtlMode` and `lang: 'he-IL'`; table columns reversed in data | pptxgenjs defaults to LTR and en-US | Step 6 |
| Which Israeli document to issue (עוסק פטור vs עוסק מורשה; חשבונית מס, חשבונית מס/קבלה, חשבונית עסקה, קבלה, חשבון עסקה) | An עוסק פטור may not issue a tax invoice (Kol Zchut) | Step 7, `references/templates.md` |
| Tax invoice required fields, including "עוסק מורשה", "מקור" and signature | Kol Zchut's list of mandatory fields | Step 7, `references/templates.md` |
| Allocation number threshold (5,000 NIS before VAT from 1.6.2026) | Without it the buyer cannot deduct input VAT (Tax Authority notice) | Step 7, `references/templates.md` |
| Samples are layouts, not issued documents; real invoices come from authorized software | Kol Zchut: invoices printed from a book or authorized software, original and copy | Step 7, Legal notice |
| VAT rate 18% | In force since 01.01.2025 | Step 7, scripts |

## Should cover (advanced)

| Item | Status |
|------|--------|
| Page numbers ("עמוד X מתוך Y") in an RTL DOCX footer and in PDFs | Partial: `_fill_paragraph` works on footer paragraphs; PAGE/NUMPAGES fields not shown. Deferred. |
| Word numbering (numbering.xml) for Hebrew lists | Not covered; manual "1." markers are handled. Deferred. |
| Header-row repeat (`w:tblHeader`) and column widths in invoice tables | Not covered. Deferred. |
| Page breaks for long invoices in reportlab | Documented as a limitation in Example 4. |
| Rounding VAT to the agora with Decimal | Script rounds VAT to 2 places before the total. |

## Out of scope (explicit)

| Item | Rationale (2026-10-01) |
|------|------------------------|
| Requesting an allocation number from the Tax Authority, digital signatures on PDFs | Belongs to invoicing software; the skill routes there (green-invoice skill). A user may ask; the answer given is where to get it. |
| Legal content of contracts | The skill handles layout; the Legal notice routes substance to a lawyer. |
| Reading or OCR of existing documents | Routed to hebrew-ocr-forms. |
| Hebrew calendar date conversion | Other localization skills cover it. |

## Authoritative sources

- Kol Zchut, הוצאת חשבונית מס, חשבונית עסקה וקבלה
- Israel Tax Authority notice, 24.05.2026 (allocation-number threshold)
- python-bidi README and issue #25
- WeasyPrint first steps documentation
- pptxgenjs text API documentation
