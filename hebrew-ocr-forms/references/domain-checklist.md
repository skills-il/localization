# Domain checklist: OCR and field extraction from Israeli government documents

What a complete workflow for reading scanned or exported Israeli government documents should
cover, what this skill deliberately leaves out, and why. Reviewed 2026-10-12. Facts behind each
item are quoted, with their sources, in `evidence.json`.

## Must cover (core)

1. **Text layer first, OCR second.** Check a PDF for a text layer (`pdftotext`) and OCR only
   image-only pages. The Nesach, a payroll-exported Form 106 and BL certificates are usually
   born-digital. Covered: SKILL.md Step 0.
2. **The digital Nesach is the original.** The registry states a Nesach is recognized as an
   original only in digital form. Ask for the PDF, and label every OCR output an unofficial
   transcription. Covered: Step 0, the JSON `notice` field and the Nesach script's closing note.
3. **Privacy.** Personal data under the Privacy Protection Law (Amendment 13 in force since
   14 August 2025): local processing by default, consent before cloud APIs, explicit consent for
   medical letters, the transfer-abroad and data-security regulations, masking, deletion,
   professional confidentiality. Covered: Step 0.
4. **Tesseract setup for Hebrew.** `-l heb+eng` (plus `ara` for bilingual forms), `--oem 1`,
   `--psm 4` for tabular forms and `--psm 6` for uniform blocks, `preserve_interword_spaces`.
   Covered: Step 3.
5. **Preprocessing that matches Tesseract's own guidance.** 300 DPI or more, deskew, frame
   removal before deskew, denoising, binarization optional because Tesseract binarizes
   internally. Covered: Step 2 and `preprocess_image.py`.
6. **Correct form identities.** Form 106 is "אישור על משכורת וניכוי מס"; 806/857 is the annual
   withholding certificate on payments, not capital gains (that is Form 1399); Form 102 is the
   employer's monthly BL report; BL "Form 100" is not an employer report; BL certificates carry
   the "המוסד לביטוח לאומי" header. Covered: Step 1 and `references/israeli-form-types.md`.
7. **Form 106 read by field code.** Salary row field 158/172, tax row field 042; never return a
   code, a year, a phone or a street number as an amount; report an unreadable row instead of
   guessing. Covered: Step 4 and `extract_form_fields.py`.
8. **Nesach structure.** One row per owner with a verbatim share, per mortgage with its degree,
   per caution / lien / order / easement / expropriation with its beneficiary; deed numbers kept
   out of the share; exact share sum; every unplaced or empty section warned. Covered: Step 4b,
   `tabu_to_spreadsheet.py` and `references/nesach-tabu-structure.md`.
9. **Israeli ID validation.** Check digit on every personal ID; 8-digit reads padded and flagged;
   shorter reads treated as fragments, never padded. Covered: Step 6 and both scripts.
10. **Hebrew text handling.** Bidi control characters, nikud stripping that keeps the maqaf,
    sofit folding for matching only, Tesseract dropping spaces between words and numbers.
    Covered: Step 5 and Gotchas.
11. **Engine choice by documented Hebrew support.** Textract has none, Azure Vision Read has none,
    Azure Document Intelligence and Google list Hebrew for printed text; no engine is documented
    as reliable for Hebrew handwriting. Covered: OCR Engine Options.
12. **Confidence and human review.** Per-word and per-field confidence, with a rule for what goes
    to a human. Covered: Step 6 and Example 2.
13. **Withholding certificates are confirmed online.** An OCR'd rate or validity date is checked
    in the Tax Authority's lookup before it is applied. Covered: Step 1 and the form reference.

## Should cover (advanced)

1. Phone-photo correction (perspective warp, shadow flattening). Partially covered: the
   preprocessing script warns on low resolution and SKILL.md says to rescan; no warp is
   implemented.
2. Dedicated extractors for 806/857, 102, BL certificates and the vehicle licence. Currently
   these are detected and their ids, dates, amounts and percentages are listed unlabelled.
3. A Nesach schema with separate action-type (מכר / ירושה / מתנה) and deed-date columns. Currently
   the deed number is kept in `detail` and the action type stays in `name`.
4. Output provenance (source line, bounding box) per extracted field.
5. A labelled regression set of synthetic pages run on every change to the scripts.

## Out of scope (explicit)

- **Handwritten Hebrew recognition.** No engine documents it as reliable; flag for human review.
  (2026-10-12)
- **Legal or tax interpretation.** What a caution, lien or order means for a transaction, and any
  tax computation, refund estimate or filing advice from 106 / 857, belong to the user's lawyer or
  accountant and to dedicated skills. This skill transcribes only. (2026-10-12)
- **Ordering, paying for or filing documents** (ordering a Nesach, filing 102 / 126, requesting BL
  certificates). Separate government-service flows. (2026-10-12)
- **Verifying a document's authenticity or digital signature.** The skill reads documents; it
  cannot establish that they are genuine. (2026-10-12)
- **Non-Israeli forms and training custom OCR models.** (2026-10-12)

## Authoritative sources

The sources behind every fact in this skill are listed with verbatim quotes in `evidence.json`,
and the main ones in the Reference Links section of SKILL.md.
