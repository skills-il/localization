---
name: hebrew-ocr-forms
description: Process and extract data from scanned Israeli government forms using OCR. Supports Tabu (land registry), Tax Authority forms, Bituach Leumi documents, and other official Israeli paperwork. Use when user asks to OCR Hebrew documents, extract data from Israeli forms, "lesarek tofes", parse Tabu extract, read scanned tax form, or process Israeli government documents. Includes Hebrew OCR configuration, field extraction patterns, and RTL text handling. Do NOT use for handwritten Hebrew recognition (requires specialized models) or non-Israeli form processing.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(tesseract:*)
compatibility: Requires Tesseract OCR with Hebrew language pack. Python with pytesseract, Pillow, and opencv-python.
---

# Hebrew OCR Forms

## Instructions

### Step 1: Identify the Form Type
| Form Type | Source | Key Identifiers | Common Fields |
|-----------|--------|-----------------|---------------|
| Nesach Tabu | Land Registry | "נסח טאבו", "לשכת רישום המקרקעין" | Gush, Chelka, Owner, Liens |
| Tofes 106 | Tax Authority | "טופס 106", "דו״ח שנתי למעביד" | Salary, Tax, Employer |
| Ishur Nikui | Tax Authority | "אישור ניכוי מס במקור" | Tax rate, Validity, TZ |
| Tofes 857 | Tax Authority | "טופס 857", "רווח הון" | Transaction, Gain, Tax |
| Ishur Zkauyot | Bituach Leumi | "אישור זכאויות", "ביטוח לאומי" | Benefit type, Amount |
| Tofes 100 | Bituach Leumi | "טופס 100", "דין וחשבון" | Employees, Wages |
| Rishayon Rechev | Vehicle Licensing | "רישיון רכב" | Plate, Owner, Expiry |

### Step 2: Preprocess the Scanned Image

See `scripts/preprocess_image.py` for the full preprocessing pipeline. Key steps:
1. Convert to grayscale
2. Deskew -- Israeli forms are often slightly rotated from scanning
3. Binarize with adaptive threshold -- handles uneven lighting from scanners
4. Remove noise with morphological operations

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

- For tabular forms (Tabu, Tofes 106), use PSM 4 instead of PSM 6
- Always use LSTM mode (--oem 1) for best Hebrew accuracy
- Include both heb and eng languages since forms mix Hebrew and English/numbers

### Step 4: Extract Fields by Form Type

**Tabu Extract (Nesach Tabu) key fields:**
- Gush (block) number: look for "גוש" followed by digits
- Chelka (parcel) number: look for "חלקה" followed by digits
- Owner name: follows "בעלים" or "שם הבעלים"
- ID number (TZ): follows "ת.ז." or "מספר זהות", 9 digits

**Tax Form (Tofes 106) key fields:**
- Tax year: follows "שנת מס"
- Employer number: follows "מספר מעביד" or "מס׳ עוסק", 9 digits
- Gross salary: follows "שכר ברוטו" or "הכנסה חייבת"
- Tax deducted: follows "מס שנוכה" or "ניכוי מס"

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

**Strip nikud before exact-string matching.** `normalize_bidi_text()` only removes Unicode category `Cf` (format) characters. Hebrew nikud (vowel diacritics, U+0591 to U+05C7) are category `Mn` (non-spacing mark), so they survive this filter. If a scanned form happens to contain vocalized text, or the OCR engine hallucinates stray marks, an exact-string or regex keyword match like `"גוש"` will silently fail against `"גּוּשׁ"`. Strip nikud explicitly before keyword matching:

```python
import re

NIKUD_RE = re.compile(r'[֑-ׇ]')

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

After extraction, validate key fields:
- **TZ numbers:** Run through Israeli ID validation algorithm (check digit)
- **Dates:** Verify DD/MM/YYYY format and valid date ranges
- **Amounts:** Check that numeric fields parse correctly, no OCR artifacts in digits
- **Gush/Chelka:** Verify numeric format, reasonable ranges
- **Cross-reference:** If TZ appears in multiple fields, verify consistency

## Examples

### Example 1: Process Tabu Extract
User says: "Extract data from this scanned Tabu document"
Result: Preprocess image, run Hebrew OCR, identify as Nesach Tabu, extract gush/chelka/owner/rights fields, validate TZ, return structured JSON.

### Example 2: Batch Process Tax Forms
User says: "I have 50 scanned Tofes 106 forms -- extract salary and tax data"
Result: Set up batch pipeline -- preprocess each image, OCR with Hebrew+English, extract Tofes 106 fields, validate, output to CSV/JSON with confidence scores.

### Example 3: OCR Quality Issues
User says: "The OCR isn't reading the Hebrew text correctly"
Result: Diagnose preprocessing -- check image resolution (recommend 300 DPI minimum), verify deskewing, adjust binarization threshold, try different PSM modes, check Hebrew language pack installation.

## Bundled Resources

### Scripts
- `scripts/preprocess_image.py` - Prepare scanned Israeli form images for OCR: grayscale conversion, deskewing rotated scans, adaptive binarization for uneven lighting, morphological noise removal, optional CLAHE contrast enhancement, and border removal. Run: `python scripts/preprocess_image.py --help`
- `scripts/extract_form_fields.py` - Run Tesseract Hebrew OCR on preprocessed form images and extract structured fields by form type. Supports auto-detection of Tabu, Tofes 106, and other Israeli government forms. Outputs JSON with extracted fields and Israeli ID validation. Run: `python scripts/extract_form_fields.py --help`

### References
- `references/israeli-form-types.md` - Detailed catalog of Israeli government form types (Tabu/land registry, Tax Authority forms, Bituach Leumi documents) with field descriptions, regex extraction patterns, ID validation rules, date/currency formats, and OCR tips per form layout. Consult when identifying an unknown form or building field extraction logic for a specific document type.

## OCR Engine Options

Tesseract is a strong free baseline for Hebrew print, but modern cloud vision APIs often match or beat it on noisy scans and stamped forms. Pick per use case:

| Engine | Hebrew print | Handwriting | Cost model | When to use |
|--------|--------------|-------------|------------|-------------|
| Tesseract (heb+eng, LSTM) | Good for clean scans at 300 DPI+ | Weak | Free, self-hosted | Default for batch local pipelines, privacy-sensitive data |
| Google Cloud Vision – Document Text Detection | Very good, robust to noise | Partial (printed-looking handwriting only) | Per-request | Mixed-quality scans, large batches, PDF forms |
| AWS Textract (AnalyzeDocument) | NOT supported (Latin-script languages only: EN/ES/DE/IT/FR/PT) | Not for Hebrew | Per-page | Do NOT use for Hebrew forms; its text/forms extraction returns garbage on Hebrew |
| Azure AI Vision – Read API | Not in the officially-listed printed-OCR set; verify on your own documents (community reports of gibberish on Hebrew) | Not reliable for Hebrew | Per-transaction | Test before relying on it for Hebrew; strong for Latin/enterprise PDFs |
| Claude Vision (claude-sonnet-4-6 / claude-opus-4-8) | Very good, context-aware | Good (with prompt guidance) | Token-based | Unusual form layouts, cross-field validation, when you want the model to also reason about the data |

Notes: none of these engines is reliable for cursive handwritten Hebrew on forms like old Tabu extracts. For those, flag for human review instead of auto-extraction. When you do call Google Cloud Vision for Hebrew, pass `languageHints: ['iw']` (Vision uses the legacy ISO code `iw` for Hebrew, not `he`); Tesseract uses `heb`. AWS Textract and Azure Read are not dependable for Hebrew, prefer Tesseract (`heb`), Google Cloud Vision (`iw`), or Claude Vision.

## Gotchas
- Hebrew OCR accuracy drops significantly for handwritten text, especially for the letters vav, zayin, and yod which look similar. Always include confidence scores and flag low-confidence characters.
- Scanned Israeli government forms often have mixed Hebrew and Arabic text. Agents may OCR the Arabic sections as Hebrew or skip them entirely. Both languages use RTL but different Unicode ranges.
- Israeli ID numbers (mispar zehut) and phone numbers extracted via OCR should be validated with check-digit algorithms after extraction, as single-digit OCR errors are common.
- Many Israeli forms use dot-matrix printed Hebrew, which has lower OCR accuracy than laser-printed text. Agents may report higher confidence than warranted for older government documents.
- Tesseract can reorder digit runs inside an RTL line. A number like a 9-digit TZ or an invoice amount printed inside a Hebrew sentence may come back with its digit groups shuffled, even when each individual digit was read correctly. Do not trust the raw left-to-right order of numbers extracted from a mixed Hebrew/digit line, re-anchor each number to its field label and re-validate with check-digit or range rules.
- The bundled scripts only accept a single image file. Many Israeli forms are multi-page PDFs (a Tofes 106 packet, a multi-sheet Tabu extract). Convert each PDF page to an image first, for example with `pdf2image` (`convert_from_path`) or `pdftoppm`, then run preprocessing and OCR per page and merge the extracted fields. Do not feed a raw PDF to `preprocess_image.py` or `extract_form_fields.py`.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Tesseract documentation | https://tesseract-ocr.github.io/tessdoc/ | Installation, language packs, LSTM mode, PSM values |
| Tesseract Hebrew traineddata | https://github.com/tesseract-ocr/tessdata | Hebrew model for tesseract |
| Google Cloud Vision – Documents | https://cloud.google.com/vision/docs/fulltext-annotations | Document Text Detection API reference |
| AWS Textract – AnalyzeDocument | https://docs.aws.amazon.com/textract/latest/dg/how-it-works-analyzing.html | Forms and tables extraction |
| Azure AI Vision – Read API | https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/language-support | Multi-language OCR; check the language-support list (Hebrew is not in the official printed-OCR set, verify before relying on it) |
| Israeli ID check-digit spec | https://he.wikipedia.org/wiki/מספר_זהות_(ישראל) | Algorithm for validating a 9-digit Israeli ID |

## Troubleshooting

### Error: "Tesseract Hebrew language pack not found"
Cause: Hebrew traineddata not installed
Solution: Install with `sudo apt-get install tesseract-ocr-heb` (Ubuntu) or `brew install tesseract-lang` (macOS). Verify with `tesseract --list-langs`.

### Error: "OCR output is garbled or reversed"
Cause: Bidirectional text ordering issue
Solution: Use `normalize_bidi_text()` function. Ensure Tesseract is using `--oem 1` (LSTM mode). Check that the image is not mirrored.

### Error: "Low accuracy on specific form sections"
Cause: Poor scan quality, stamps/signatures overlapping text, colored backgrounds
Solution: Increase preprocessing -- apply stronger denoising, crop to specific form regions, use ROI-based extraction for known form layouts.