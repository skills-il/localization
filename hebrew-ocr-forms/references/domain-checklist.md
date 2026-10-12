# Domain checklist: OCR and field extraction from Israeli government documents

What a complete workflow for reading scanned or exported Israeli government documents should
cover, and where this skill stands on each item. Reviewed 2026-10-12. Facts behind the skill are
quoted, with their sources, in `evidence.json`. "Addressed" means the skill text covers it and,
where a script is involved, the behaviour was exercised on synthetic test pages or text fixtures.
Nothing is dropped from this list: an item the skill does not cover is marked as a future update
or as out of scope, with the reason.

## Must cover (core)

1. **Text layer first, OCR second.** Check a PDF for a text layer and OCR only image-only pages.
   Addressed: SKILL.md Step 0.
2. **Visual-order (reversed) Hebrew in extracted PDF text.** Partial: Step 0 warns that some PDFs
   yield reversed Hebrew and says to reorder it. Future update: a named reordering method and a
   detection heuristic, plus legacy-encoded PDFs.
3. **The digital Nesach is the only original.** Addressed: Step 0; the JSON `notice` field and the
   `notice` row at the end of the Nesach CSV (tested).
4. **Tesseract setup for Hebrew** (`heb+eng`, `ara` when needed, `--oem 1`, PSM 4 / 6,
   `preserve_interword_spaces`). Addressed: Step 3 and `extract_form_fields.py` (`--lang`).
5. **Preprocessing to Tesseract's guidance** (300 DPI, deskew, frames, denoise, optional
   binarization). Addressed: Step 2 and `preprocess_image.py` (tested on grainy, skewed and framed
   synthetic pages).
6. **Phone-photo input.** Partial: a text-height warning fires when letters are too small for OCR
   (tested on a simulated distant 12 MP photo) and Step 2 says to rescan or use a flattening
   scanner app. Future update: perspective warp and shadow flattening.
7. **Word boxes and confidence, not only plain text.** Partial: per-word and per-field confidence
   are output. Future update: per-field source text and bounding boxes.
8. **Hebrew text normalization.** Partial: bidi controls, nikud (keeping the maqaf), sofit folding,
   quote and geresh variants in labels. Future update: Unicode NFC and Hebrew presentation forms
   from PDF text.
9. **Mixed-direction tokens in RTL lines** (numbers, dates, amounts glued to words or codes).
   Addressed: Gotchas; both scripts handle glued tokens (tested).
10. **Israeli ID check-digit validation.** Addressed: 9 digits, or 8 padded and flagged; shorter
    reads are flagged, never padded (tested in both scripts).
11. **Nesach types and structure** (regular / concentrated / historical, sections). Partial:
    sections parsed; concentrated and historical extracts are warned. Future update: a status
    column for deleted registrations.
12. **Nesach-to-spreadsheet schema.** Partial: one row per owner / mortgage / encumbrance with
    shares verbatim, deed numbers and degrees in `detail`. Future update: separate action-type and
    deed-date columns.
13. **Form 106 field map.** Partial: salary (158/172), tax (042), withholding file, employee ID,
    tax year; a tax-above-salary flag. Other fields are listed in the form reference. Future
    update: months worked and the remaining fields in the extractor.
14. **Form 806/857 field map.** Future update: a dedicated extractor. Today the form is detected
    and its ids, dates, amounts and percentages are listed unlabelled.
15. **Withholding / bookkeeping certificate.** Addressed: Step 1 says to confirm the rate and
    validity in the Tax Authority's online lookup; percentages are extracted.
16. **Bituach Leumi Form 102 and certificates.** Partial: correct identities and header-based
    detection. Future update: dedicated extractors.
17. **Vehicle licence.** Future update: field map and extractor. Today it is only detected.
18. **Detection keyed on distinctive titles, not generic words.** Addressed: titles, header-only
    matching for form numbers and the BL header, no "גוש" fallback without section headers
    (tested).
19. **Cloud OCR engine facts for Hebrew.** Addressed: OCR Engine Options, from vendor
    documentation only.
20. **No-install path for non-developers.** Addressed: Step 0 (read the page directly, then run the
    deterministic checks).
21. **Privacy and data protection, local first.** Addressed: Step 0.
22. **Structuring only, no professional judgment.** Addressed: Step 0 says the output is an
    unofficial transcription with no interpretation of entries. A separate legal-notice section is
    not part of this skill, because it emits transcriptions only, not a legal or tax conclusion.
23. **Output contract and validation report.** Partial: JSON with fields, flags
    (`rows_without_amount`, `negative_amounts`, `tax_exceeds_salary`, `*_padded`,
    `employee_tz_unreadable`), confidence and a notice. Future update: a form-type confidence and
    explicit null-with-reason for every unread field.

## Should cover (advanced)

1. Batch mode with per-file error isolation, a summary CSV and de-duplication. Future update.
2. Deleted registrations in a historical Nesach as a separate status. Future update.
3. Digital-signature verification of the Nesach PDF. Out of scope: the skill reads documents; it
   cannot establish that they are genuine.
4. Unregistered-property documents (rights confirmations). Partial: detected as
   `rights_confirmation` and kept out of the Nesach parser. Future update: a field map.
5. Related certificates (bank annual certificates, payslips). Future update.
6. Company, osek and withholding-file number checks. Future update: format checks.
7. Arabic-script names and bilingual forms. Addressed: `--lang heb+ara+eng`.
8. Accuracy tuning (best-quality models, character whitelists for numeric zones). Future update.
9. PDF rasterization tooling. Partial: `pdftoppm` is named. Future update: compare alternatives.
10. Cloud deployment hygiene (region, vendor retention, data-processing terms). Partial: Step 0
    privacy. Future update: region and retention guidance.
11. A labelled regression set of synthetic pages run on every script change. Future update.
12. Handwritten fields detected and routed to a human. Partial: guidance to flag them; no
    automatic detection.

## Out of scope (explicit)

- **Handwritten Hebrew recognition.** No engine documents it as reliable; flag for human review.
  (2026-10-12)
- **Legal or tax interpretation.** What a caution, lien or order means for a transaction, and any
  tax computation, refund estimate or filing advice, belong to the user's lawyer or accountant and
  to dedicated skills. This skill transcribes only. (2026-10-12)
- **Ordering, paying for or filing documents.** Separate government-service flows. (2026-10-12)
- **Verifying a document's authenticity or digital signature.** See Should 3. (2026-10-12)
- **Non-Israeli forms and training custom OCR models.** (2026-10-12)

## Authoritative sources

The sources behind every fact in this skill are listed with verbatim quotes in `evidence.json`,
and the main ones in the Reference Links section of SKILL.md.
