---
name: hebrew-ocr-forms
description: >-
  Process and extract data from scanned Israeli government forms using OCR.
  Supports Tabu (land registry), Tax Authority forms, Bituach Leumi documents,
  and other official Israeli paperwork. Use when user asks to OCR Hebrew
  documents, extract data from Israeli forms, "lesarek tofes", parse Tabu
  extract, read scanned tax form, or process Israeli government documents.
  Includes Hebrew OCR configuration, field extraction patterns, and RTL text
  handling. Do NOT use for handwritten Hebrew recognition (requires specialized
  models) or non-Israeli form processing.
license: MIT
allowed-tools: 'Bash(python:*) Bash(pip:*) Bash(tesseract:*)'
compatibility: >-
  Requires Tesseract OCR with Hebrew language pack. Python with pytesseract,
  Pillow, and opencv-python.
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags:
    he:
      - זיהוי-תווים
      - עברית
      - טפסים
      - ממשל
      - טאבו
      - מיסים
      - ביטוח-לאומי
    en:
      - ocr
      - hebrew
      - forms
      - government
      - tabu
      - tax
      - bituach-leumi
  display_name:
    he: OCR לטפסים בעברית
    en: Hebrew Ocr Forms
  display_description:
    he: 'זיהוי תווים אופטי לטפסי ממשלה בעברית — טאבו, רשות המסים ועוד'
    en: >-
      Process and extract data from scanned Israeli government forms using OCR.
      Supports Tabu (land registry), Tax Authority forms, Bituach Leumi
      documents, and other official Israeli paperwork. Use when user asks to OCR
      Hebrew documents, extract data from Israeli forms, "lesarek tofes", parse
      Tabu extract, read scanned tax form, or process Israeli government
      documents. Includes Hebrew OCR configuration, field extraction patterns,
      and RTL text handling. Do NOT use for handwritten Hebrew recognition
      (requires specialized models) or non-Israeli form processing.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - antigravity
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
    lines = text.split('
')
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
    return '
'.join(normalized)
```

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
- `scripts/preprocess_image.py` — Prepare scanned Israeli form images for OCR: grayscale conversion, deskewing rotated scans, adaptive binarization for uneven lighting, morphological noise removal, optional CLAHE contrast enhancement, and border removal. Run: `python scripts/preprocess_image.py --help`
- `scripts/extract_form_fields.py` — Run Tesseract Hebrew OCR on preprocessed form images and extract structured fields by form type. Supports auto-detection of Tabu, Tofes 106, and other Israeli government forms. Outputs JSON with extracted fields and Israeli ID validation. Run: `python scripts/extract_form_fields.py --help`

### References
- `references/israeli-form-types.md` — Detailed catalog of Israeli government form types (Tabu/land registry, Tax Authority forms, Bituach Leumi documents) with field descriptions, regex extraction patterns, ID validation rules, date/currency formats, and OCR tips per form layout. Consult when identifying an unknown form or building field extraction logic for a specific document type.

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