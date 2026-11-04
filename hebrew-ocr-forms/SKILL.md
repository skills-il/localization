---
name: hebrew-ocr-forms
description: Process and extract data from scanned Israeli government forms using OCR. Supports Tabu (land registry), Tax Authority forms, Bituach Leumi documents, and other official Israeli paperwork. Use when user asks to OCR Hebrew documents, extract data from Israeli forms, "lesarek tofes", parse Tabu extract, read scanned tax form, or process Israeli government documents. Includes Hebrew OCR configuration, field extraction patterns, and RTL text handling. Do NOT use for handwritten Hebrew recognition (requires specialized models) or non-Israeli form processing.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(tesseract:*)
compatibility: Requires Tesseract OCR with Hebrew language pack, and poppler (pdftotext / pdftoppm) for PDFs. Python with pytesseract, Pillow, and opencv-python.
---

# Hebrew OCR Forms

## Instructions

### Step 0: Decide Whether This Needs OCR At All

**Check for a text layer first.** Most documents gov.il issues today are born-digital PDFs: the land-registry Nesach, a Form 106 exported from payroll software, Bituach Leumi certificates downloaded from the personal area. Run `pdftotext -layout file.pdf -` (poppler); if it prints real Hebrew, use that text and skip OCR entirely, because OCR can only lose characters that are already exact. Hebrew from some PDFs comes out in visual (reversed) order; re-order it before matching labels. Only image-only pages (scans, phone photos) go through Steps 2-3. The registry's own page states a Nesach is recognized as an original only in its digital form, not when printed, so ask for the PDF instead of re-scanning a printout.

**If you can read images yourself** (a vision-capable agent), you may read a page directly instead of installing Tesseract, but still run the deterministic checks from Step 6 (ID check digit, owner-share sum) on what you read.

**Privacy.** These pages carry ID numbers, salaries, tax and benefit data, which is personal data under the Privacy Protection Law (Amendment 13 in force since 14 August 2025, with stronger enforcement powers). Default to local Tesseract. Before sending pages to a cloud OCR or LLM API:
- confirm the data owner allows it, and never send Bituach Leumi disability or maternity letters (medical details) without their explicit consent;
- remember the major cloud engines may process data outside Israel, which the transfer-abroad regulations (תקנות הגנת הפרטיות (העברת מידע אל מאגרי מידע שמחוץ לגבולות המדינה)) govern, and that an office keeping such scans is also subject to the data-security regulations (תקנות הגנת הפרטיות (אבטחת מידע));
- mask ID numbers in any field you do not need, and delete uploaded pages and intermediate images when the job is done;
- for law and accounting offices, client documents are also covered by professional confidentiality.

**The output is an unofficial transcription.** Every value the scripts emit is an OCR reading, not the issuing authority's record; the JSON carries a `notice` field, and the Nesach CSV ends with a `notice` row saying the same. Never present the CSV as the Nesach itself, and give no opinion on what an entry (a caution, an attachment, an order) means for a transaction.

### Step 1: Identify the Form Type
| Form Type | Source | Key Identifiers | Common Fields |
|-----------|--------|-----------------|---------------|
| Nesach Tabu | Land Registry | "נסח טאבו", "לשכת רישום המקרקעין" | Gush, Chelka, Owner, Liens |
| Form 106 | Tax Authority | "טופס 106", "אישור על משכורת וניכוי מס", "מספר תיק ניכויים" | Tax year, Withholding file no., Employee TZ, Salary (field 158/172), Tax withheld (field 042) |
| Ishur Nikui | Tax Authority | "אישור ניכוי מס במקור", "אישור ניהול ספרים וניכוי מס במקור" | Withholding rate, Validity, File / osek number. Confirm the rate and validity in the Tax Authority's online lookup by file number before applying them |
| Form 806/857 | Tax Authority | "0806/0857", "אישור שנתי על ניכוי מס הכנסה מתשלומים" | Payer's withholding file, Payee ID, Gross paid, Tax withheld (annual certificate of withholding at source on payments, NOT a capital-gains form) |
| Form 102 | Bituach Leumi | "טופס 102", "דין וחשבון על העסקת עובדים" | Employer, Employees, Wages, Contributions (monthly employer report) |
| BL certificate | Bituach Leumi | "המוסד לביטוח לאומי" header, with a title such as "אישור זכאות לגמלאות שנתי" or "אישור תשלומים שנתי" | Benefit type, Period, Amount |
| Rishayon Rechev | Vehicle Licensing | "רישיון רכב" | Plate, Owner, Expiry |

Capital-gains reports are Form 1399, not 857. BL "Form 100" is not an employer report (BL publishes it as a claimant's refusal form), so do not key on it. A document titled "אישור זכויות" is not a Nesach; the extractor keeps it out of the Nesach parser.

### Step 2: Preprocess the Scanned Image

See `scripts/preprocess_image.py` for the full preprocessing pipeline. Key steps:
1. Convert to grayscale (optionally crop a dark scanner frame with `--remove-borders PX` first, so it does not skew the angle estimate)
2. Deskew -- Israeli forms are often slightly rotated from scanning; estimates beyond 15 degrees are refused rather than guessed. The estimate uses all ink, so on our synthetic test pages a large stamp or signature rotated a straight page by about 1-3 degrees; check the output and use `--no-deskew` if so
3. Denoise (non-local means, `--denoise-strength`, default 15)
4. Binarize only on request (`--binarize`, best with `--denoise-strength 20`). Tesseract binarizes internally, and an adaptive threshold on a grainy scan turns grain into speckle it reads as letters; on our test scans the grayscale output read every field while the binarized one lost some
5. Phone photos and low-DPI scans: this pipeline does not correct perspective or uneven page curvature. The script warns when the image is far smaller than an A4 page at 300 DPI, and when the median letter height is too small for OCR (on our synthetic test pages about 4 px failed and about 7 px read cleanly; it warns below 8 px), which catches a distant photo even from a 12 MP camera. Ask for a rescan at 300 DPI or a closer photo with a scanner app that flattens the page

### Step 3: Run Hebrew OCR with Tesseract

See `scripts/extract_form_fields.py` for the full extraction pipeline.

**Tesseract configuration for Hebrew forms:**
```python
config = (
    '--oem 1 '          # LSTM neural net (best for Hebrew)
    '--psm 6 '          # Assume uniform block of text
    '-l heb+eng '       # Hebrew + English (forms have both)
    '-c preserve_interword_spaces=1'  # Keep spacing for field alignment
)
```

- For tabular forms (Tabu, Form 106, 102, 806/857), use PSM 4 instead of PSM 6. In auto mode the script reads once, detects the form, and re-reads tabular forms with PSM 4
- Always use LSTM mode (--oem 1) for best Hebrew accuracy
- Include both heb and eng languages since forms mix Hebrew and English/numbers; add `ara` (`--lang heb+ara+eng`) for bilingual Hebrew/Arabic forms

### Step 4: Extract Fields by Form Type

**Tabu Extract (Nesach Tabu) key fields:**
- Gush (block) number: look for "גוש" followed by digits
- Chelka (parcel) number: look for "חלקה" followed by digits
- Sub-parcel (tat-chelka): mandatory for an apartment in a shared building; note it is NOT necessarily the apartment number
- Owner name: follows "בעלים" or "שם הבעלים"
- ID number (TZ): follows "ת.ז." or "מספר זהות", 9 digits
- Ownership share (chelek): a fraction of the whole, e.g. "1/2", "125/1000", or "בשלמות" (in full). Keep it verbatim, do NOT convert to a decimal
- Right type: "בעלות" (ownership), "חכירה" (lease), "חכירה לדורות" (generational lease)

A Nesach is not flat: one property can list several owners (each with a share), several mortgages, and several cautions (he'arat azhara). Extract each repeating section into its own rows rather than one field per label. See Step 4b to turn the whole extract into a spreadsheet.

**Tax Form (Form 106) key fields** (the form is titled "אישור על משכורת וניכוי מס"):
- Tax year: follows "שנת מס"
- Employer: "מספר תיק ניכויים" (the withholding file number), plus "שם מלא של המעסיק"
- Employee: "מספר זהות העובד"
- Salary: the "משכורת" row, annual-return field 158/172
- Income tax withheld: "ניכיתי ושילמתי מס הכנסה", field 042

Amount rows print the field code next to the amount, and Tesseract often glues them ("04221,340"). The script reads an amount only from the salary row and the tax row, right after the field code or label, never from a bare 42/158/172 elsewhere on the page (street numbers, phones, branch numbers), and names the fields `salary_158_172` and `income_tax_042`. When a row is found but its amount cannot be read cleanly (space-grouped thousands "184 500", an OCR'd letter O for zero) the field is omitted and listed in `rows_without_amount`; read those by hand. A negative amount is kept but listed in `negative_amounts` for a human to confirm. Tax above salary sets `tax_exceeds_salary` (flagged, never corrected), and a labelled employee ID that is not 8-9 digits sets `employee_tz_unreadable`. Field 158/172 is the total the employer paid during the tax year; do not relabel it "taxable income".

### Step 4b: Turn a Full Tabu Extract into a Spreadsheet

For the common request "parse a Nesach Tabu into Excel" (פירוק נסח טאבו לאקסל), the challenge is the repeating sections: a lawyer wants one row per owner (with the share), one row per mortgage, one row per caution, not a single merged field. `scripts/tabu_to_spreadsheet.py` takes the OCR text (or the JSON from `extract_form_fields.py`) and writes a normalized CSV where a `section` column marks each row as property / owner / lease / mortgage / caution, with the gush / helka / tat_helka key repeated on every row so several extracts concatenate cleanly.

```bash
python scripts/tabu_to_spreadsheet.py --file nesach_ocr.txt --out nesach.csv
```

Two things it does deliberately: it writes UTF-8 with a BOM so Excel detects the encoding and shows the Hebrew without a manual import step (the sheet's right-to-left view is an Excel setting a CSV cannot carry), and it keeps the share as a verbatim string (`125/1000`, not `0.125`) because rounding a long denominator loses legal precision. It also warns when the owner shares do not sum to 1 (בשלמות), which usually means OCR dropped an owner row and the extract needs human review. See `references/nesach-tabu-structure.md` for the full section-to-column mapping.

### Step 5: Handle RTL and Bidirectional Text

```python
import unicodedata

def normalize_bidi_text(text):
    """Normalize bidirectional text from Hebrew OCR output."""
    lines = text.split('\n')
    normalized = []
    for line in lines:
        # Strip bidi control characters
        clean = ''.join(
            c for c in line
            if unicodedata.category(c) != 'Cf'
        )
        clean = ' '.join(clean.split())
        if clean:
            normalized.append(clean)
    return '\n'.join(normalized)
```

**Strip nikud before exact-string matching.** `normalize_bidi_text()` only removes Unicode category `Cf` (format) characters. Hebrew nikud and cantillation marks (in U+0591 to U+05C7) are category `Mn` (non-spacing mark), so they survive this filter. If a scanned form happens to contain vocalized text, or the OCR engine hallucinates stray marks, an exact-string or regex keyword match like `"גוש"` will silently fail against `"גּוּשׁ"`. Strip nikud explicitly before keyword matching:

```python
import re

# U+0591-U+05C7 minus the four punctuation marks inside it: maqaf U+05BE
# (the Hebrew hyphen, as in תת־חלקה), paseq U+05C0, sof pasuq U+05C3,
# nun hafukha U+05C6. Stripping the whole range would delete the maqaf.
NIKUD_RE = re.compile('[\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]')

def strip_nikud(text):
    """Remove Hebrew diacritics so keyword regexes match reliably."""
    return NIKUD_RE.sub('', text)
```

**Normalize final-form letters when matching.** Hebrew has five final (sofit) letter forms: ך ם ן ף ץ. They are the same letters as כ מ נ פ צ but are encoded as distinct code points. OCR usually preserves them correctly, but keyword and fuzzy-match logic can break: a label OCR'd with a final form will not equal a search term written with the medial form, and vice versa. When matching field labels, normalize both sides to a single form first:

```python
SOFIT_MAP = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}

def normalize_sofit(text):
    """Fold final-form letters to their medial forms for matching."""
    return ''.join(SOFIT_MAP.get(ch, ch) for ch in text)
```

Apply `strip_nikud()` and `normalize_sofit()` only to the matching key, never to the value you store or display, the final forms and any nikud are part of correct Hebrew and must be preserved in output.

### Step 6: Validate Extracted Data

After extraction, validate key fields. The scripts already do the first two and the ID cross-check below is yours:
- **TZ numbers:** Run through Israeli ID validation algorithm (check digit). The scripts accept 9 digits, or 8 when the leading zero was not printed (flagged `*_padded`); shorter reads are treated as fragments and never padded, because a padded fragment can pass the check digit by chance
- **Confidence:** `extract_form_fields.py` returns `ocr_confidence` (mean word confidence and the words under 60) and `field_confidence` (the lowest confidence among the OCR tokens each numeric field came from); route any field under 60 to a human
- **Dates:** Verify DD/MM/YYYY format and valid date ranges
- **Amounts:** Check that numeric fields parse correctly, no OCR artifacts in digits
- **Gush/Chelka:** Verify numeric format, reasonable ranges
- **Cross-reference:** If TZ appears in multiple fields, verify consistency

## Examples

### Example 1: Process a Tabu Extract into a Spreadsheet
User says: "Parse this scanned Tabu document into Excel" (פירוק נסח טאבו לאקסל)
Result: Preprocess image, run Hebrew OCR, identify as Nesach Tabu, then run `tabu_to_spreadsheet.py` to normalize the repeating sections into rows (one per owner with their share, one per mortgage, one per caution), validate each TZ, and write an Excel-ready UTF-8-BOM CSV. Flag for human review if the owner shares do not sum to בשלמות.

### Example 2: Batch Process Tax Forms
User says: "I have 50 scanned Tofes 106 forms -- extract salary and tax data"
Result: First try `pdftotext` on each file (payroll-exported 106s are usually text PDFs). For scans, loop over the files: preprocess, run `extract_form_fields.py --form-type tofes_106`, keep `field_confidence` with each record, validate the employee TZ, and collect the JSON into one CSV. Send any record with a field under 60 or a non-empty `rows_without_amount` to manual review.

### Example 3: OCR Quality Issues
User says: "The OCR isn't reading the Hebrew text correctly"
Result: Diagnose preprocessing -- check image resolution (Tesseract works best at 300 DPI or more), verify deskewing, compare the default grayscale output with `--binarize`, raise `--denoise-strength` on grainy scans, try different PSM modes, check Hebrew language pack installation.

## Bundled Resources

### Scripts
- `scripts/preprocess_image.py` - Prepare scanned Israeli form images for OCR: grayscale conversion, optional border crop, deskewing (`--no-deskew` to skip), non-local-means denoising, optional adaptive binarization and CLAHE contrast enhancement. Refuses PDFs with a pointer to `pdftotext` / `pdftoppm`. Run: `python scripts/preprocess_image.py --help`
- `scripts/extract_form_fields.py` - Run Tesseract Hebrew OCR on one page image and extract fields. Auto-detects Nesach, Form 106, 806/857, 102, ishur nikui, BL certificates and vehicle licences. Dedicated field extractors exist for the Nesach (property key and first owner) and Form 106; every other type gets its ids (with check-digit result), dates and amounts listed unlabelled, for you to map using `--raw-text`. Always outputs `ocr_confidence` and `field_confidence`. Run: `python scripts/extract_form_fields.py --help`
- `scripts/tabu_to_spreadsheet.py` - Turn the OCR text of a full Nesach Tabu into a normalized, Excel-ready CSV: one row per owner (with share), mortgage, and caution, keyed by gush/helka/tat_helka. Keeps shares verbatim, keeps deed numbers (12345/2015/1) out of the share column, and warns when owner shares do not sum exactly to בשלמות, when a section header has no rows under it, when a ת.ז. fails its check digit or was padded, or when nothing was parsed. Run: `python scripts/tabu_to_spreadsheet.py --example`

### References
- `references/israeli-form-types.md` - Detailed catalog of Israeli government form types (Tabu/land registry, Tax Authority forms, Bituach Leumi documents) with field descriptions, regex extraction patterns, ID validation rules, date/currency formats, and OCR tips per form layout. Consult when identifying an unknown form or building field extraction logic for a specific document type.
- `references/domain-checklist.md` - What a complete workflow in this domain covers, what is explicitly out of scope, and why. Consult when a request falls near the edge of the skill.
- `references/nesach-tabu-structure.md` - The section-by-section layout of a Nesach Tabu (property / owners with shares / leases / mortgages / cautions) and how each section maps to spreadsheet columns. Consult when parsing a land-registry extract into a table.

## OCR Engine Options

We have not benchmarked these engines against each other. The table records what each vendor documents for Hebrew; test any engine on a sample of your own pages before a batch.

| Engine | Hebrew printed text | Hebrew handwriting | Cost model | When to use |
|--------|---------------------|--------------------|------------|-------------|
| Tesseract (heb+eng, LSTM) | `heb` model in tessdata; works best at 300 DPI or more | Not reliable | Free, self-hosted | Default for local batches and privacy-sensitive data |
| Google Cloud Vision - Document Text Detection | Listed (`iw`) | Hebrew script not in Vision's handwriting list | Per-request | Mixed-quality scans when a cloud API is acceptable |
| Google Document AI - Enterprise Document OCR | Listed (`iw`) | Marked not supported | Per-page | Google's own recommendation for scanned documents over Vision |
| AWS Textract (AnalyzeDocument) | NOT supported (English, Spanish, German, Italian, French, Portuguese only) | English only | Per-page | Do NOT use for Hebrew forms |
| Azure Document Intelligence - Read / Layout | Listed (`he`) | Not in its handwriting table | Per-page | Printed Hebrew PDFs when you are already on Azure |
| Azure Vision - Read OCR | Not in its printed-OCR language table | Not listed | Per-transaction | Not for Hebrew; use Document Intelligence instead |
| Claude Vision (claude-sonnet-5-5 / claude-opus-5-5) | No published per-language OCR list; test on your pages | Not benchmarked here, treat as unreliable | Token-based | Unusual layouts, or when you also want the model to reason about the data |

Notes: none of these engines is documented as reliable for handwritten Hebrew, so flag handwritten sections (old Tabu extracts, filled-in boxes) for human review instead of auto-extraction. Google's language tables list Hebrew as `iw`, so pass `languageHints: ['iw']` to Vision; Tesseract uses `heb`; Azure Document Intelligence uses `he`. Cloud engines are also a privacy decision, see Step 0.

## Gotchas
- Hebrew OCR accuracy drops significantly for handwritten text, especially for the letters vav, zayin, and yod which look similar. Always include confidence scores and flag low-confidence characters.
- Scanned Israeli government forms often have mixed Hebrew and Arabic text. Agents may OCR the Arabic sections as Hebrew or skip them entirely. Both languages use RTL but different Unicode ranges; install Tesseract's `ara` data and pass `--lang heb+ara+eng`.
- Israeli ID numbers (mispar zehut) extracted via OCR should be validated with the check-digit algorithm, as single-digit OCR errors are common. Phone numbers have no check digit; check them against the expected format only.
- Many Israeli forms use dot-matrix printed Hebrew, which has lower OCR accuracy than laser-printed text. Agents may report higher confidence than warranted for older government documents.
- Tesseract can reorder digit runs inside an RTL line. A number like a 9-digit TZ or an invoice amount printed inside a Hebrew sentence may come back with its digit groups shuffled, even when each individual digit was read correctly. Do not trust the raw left-to-right order of numbers extracted from a mixed Hebrew/digit line, re-anchor each number to its field label and re-validate with check-digit or range rules.
- Tesseract drops the space between a Hebrew word and an adjacent number ("טופס106", "שנת מס2025", "בתאריך15/03/2025") and between two numbers ("04221,340"). Match labels with whitespace removed, never use `\b` between Hebrew and digits, and split known field codes off amounts before parsing.
- The bundled scripts only accept a single image file. Many Israeli forms are multi-page PDFs (a Tofes 106 packet, a multi-sheet Tabu extract). Convert each PDF page to an image first, for example with `pdf2image` (`convert_from_path`) or `pdftoppm`, then run preprocessing and OCR per page and merge the extracted fields. Do not feed a raw PDF to `preprocess_image.py` or `extract_form_fields.py`.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Tesseract documentation | https://tesseract-ocr.github.io/tessdoc/ | Installation, language packs, LSTM mode, PSM values |
| Tesseract Hebrew traineddata | https://github.com/tesseract-ocr/tessdata | Hebrew model for tesseract |
| Google Cloud Vision - Documents | https://docs.cloud.google.com/vision/docs/fulltext-annotations | Document Text Detection API reference |
| AWS Textract - AnalyzeDocument | https://docs.aws.amazon.com/textract/latest/dg/how-it-works-analyzing.html | Forms and tables extraction |
| Azure Document Intelligence - OCR languages | https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/language-support/ocr | Hebrew row in the printed-text table (Azure Vision Read's own table has none) |
| Google Cloud Vision - languages | https://docs.cloud.google.com/vision/docs/languages | The code listed for Hebrew (`iw`) |
| Tesseract - Improving quality | https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html | Internal binarization, noise, 300 DPI guidance |
| Israeli ID check-digit spec | https://he.wikipedia.org/wiki/ספרת_ביקורת | Algorithm for validating a 9-digit Israeli ID |
| Form 106 service | https://www.gov.il/he/service/itc-106 | Official title and purpose of Form 106. Bot-protected, renders in a browser |
| Land-registry extract (Nesach Tabu) service | https://www.gov.il/he/service/land_registration_extract | What a Nesach contains (owners, mortgages, liens, orders), gush/helka/tat-helka keys. Bot-protected, renders in a browser |

## Troubleshooting

### Error: "Tesseract Hebrew language pack not found"
Cause: Hebrew traineddata not installed
Solution: Install with `sudo apt-get install tesseract-ocr-heb` (Ubuntu) or `brew install tesseract-lang` (macOS). Verify with `tesseract --list-langs`.

### Error: "OCR output is garbled or reversed"
Cause: Two verified causes. (1) Bidirectional ordering of mixed Hebrew/number lines. (2) Scanner grain binarized into speckle: on our grainy test scans the binarized image returned pages of mixed Latin/Hebrew garbage while the denoised grayscale image read every field.
Solution: For (1), use `normalize_bidi_text()` and re-anchor numbers to their labels; check the image is not mirrored. For (2), run `preprocess_image.py` without `--binarize` (the default), or with `--binarize --denoise-strength 20`.

### Error: "Low accuracy on specific form sections"
Cause: Poor scan quality, stamps/signatures overlapping text, colored backgrounds
Solution: Increase preprocessing -- apply stronger denoising, crop to specific form regions, use ROI-based extraction for known form layouts.