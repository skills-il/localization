# Hebrew OCR Forms Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for OCR processing of Israeli government forms — extracting structured data from scanned Hebrew documents including Tabu (land registry), Tax Authority forms, Bituach Leumi (National Insurance), and other official Israeli documents.

**Architecture:** Document/Asset Creation skill (Category 1). Embeds knowledge of Israeli form types, field extraction patterns, Hebrew OCR configuration, and RTL text handling for reliable data extraction.

**Tech Stack:** SKILL.md, Python scripts using Tesseract OCR, reference for Israeli form layouts.

---

## Research

### Tesseract Hebrew Support
- **Language pack:** `heb` — Tesseract supports Hebrew via traineddata files
- **Installation:** `tesseract-ocr` + `tesseract-ocr-heb` language pack
- **Best practices for Hebrew OCR:**
  - Use `--psm 6` (assume uniform block of text) for structured forms
  - Use `--psm 4` (assume single column of variable sizes) for mixed-layout forms
  - Set `--oem 1` (LSTM neural net mode) for best Hebrew accuracy
  - Preprocess: Binarize, deskew, remove noise before OCR
  - Hebrew OCR accuracy is typically 85-95% depending on scan quality
- **Niqqud handling:** Most government forms use unvowelized Hebrew — OCR should not expect niqqud
- **RTL output:** Tesseract outputs Hebrew in logical order (right-to-left reading order stored left-to-right in string) — may need reordering for display

### Common Israeli Government Form Types

**Tabu (Land Registry / Lishkat Rishum Ha-Mekarkein):**
- Nesach Tabu (title deed extract): Owner name, ID, property block (gush), parcel (chelka), sub-parcel, rights type, encumbrances, liens
- Key fields: Gush number, Chelka number, owner details, mortgage/lien info
- Format: Multi-section tabular layout, Hebrew headers with numeric data

**Tax Authority (Rashut Ha-Misim):**
- Shomah (tax assessment): Annual income, tax brackets, deductions
- Ishur Nikui Mas Ba-Makor (withholding tax certificate): Employer details, tax rate, validity period
- Tofes 106 (annual employer statement): Salary, deductions, employer contributions
- Tofes 857 (capital gains): Transaction details, gain calculation, tax owed
- Key fields: Mispar osek (business number), TZ, tax year, amounts

**Bituach Leumi (National Insurance Institute):**
- Ishur Zkauyot (entitlement certificate): Benefits type, amounts, period
- Tvia (claim form): Claimant details, claim type, supporting documents list
- Tofes 100 (employer report): Employee list, wages, contribution calculations
- Key fields: TZ, date of birth, benefit type, monthly amount, validity dates

**Ministry of Interior (Misrad Ha-Pnim):**
- Teudat Zehut (ID card): Name, TZ number, date of birth, address
- Teudat Leda (birth certificate): Child name, parents, date/place of birth
- Ishur Toshavut (residency certificate): Address, residency status

**Misrad Ha-Rishui (Vehicle Licensing):**
- Rishayon Rechev (vehicle license): License plate, owner, vehicle details, test expiry
- Rishayon Nehiga (driving license): Name, ID, license class, expiry

### Field Extraction Patterns
- **Structured forms:** Fixed-position fields — use coordinate-based extraction
- **Semi-structured forms:** Labeled fields with variable positions — use label detection then extract adjacent text
- **Tables:** Grid detection + cell extraction — common in Tabu and tax forms
- **Dates:** Hebrew date format DD/MM/YYYY or DD.MM.YYYY, sometimes Hebrew calendar dates
- **Numbers:** Standard Arabic numerals (0-9), currency amounts with shekel symbol (₪)
- **ID numbers:** 9-digit format, sometimes with dashes (XX-XXXXXXX-X)

### Hebrew Text Direction Handling in OCR
- **Bidirectional text:** Forms often mix Hebrew (RTL) and numbers/English (LTR)
- **Logical vs. visual order:** Tesseract outputs logical order; display may need bidi algorithm
- **Field labels:** Hebrew labels are RTL but field values may be LTR (numbers, dates)
- **Table headers:** RTL reading order — rightmost column is first
- **Address fields:** Mix of Hebrew street names and Arabic numerals

### Use Cases
1. **Extract Tabu data** — Parse land registry extracts into structured JSON
2. **Process tax forms** — Extract salary and tax data from Tofes 106/857
3. **Parse Bituach Leumi documents** — Extract benefit entitlements and claim data
4. **Batch form processing** — Process multiple scanned forms with consistent extraction
5. **Validate extracted data** — Cross-reference extracted fields (ID validation, date checks)

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
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
allowed-tools: "Bash(python:*) Bash(pip:*) Bash(tesseract:*)"
compatibility: "Requires Tesseract OCR with Hebrew language pack. Python with pytesseract, Pillow, and opencv-python."
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags: [ocr, hebrew, forms, government, tabu, tax, bituach-leumi]
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

```python
import cv2
import numpy as np

def preprocess_for_hebrew_ocr(image_path):
    """Preprocess a scanned Israeli form for optimal Hebrew OCR."""
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Deskew — Israeli forms are often slightly rotated from scanning
    coords = np.column_stack(np.where(gray < 128))
    if len(coords) > 100:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        if abs(angle) > 0.5:
            (h, w) = gray.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            gray = cv2.warpAffine(gray, M, (w, h),
                                   flags=cv2.INTER_CUBIC,
                                   borderMode=cv2.BORDER_REPLICATE)

    # Binarize with adaptive threshold — handles uneven lighting
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 10
    )

    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return cleaned
```

### Step 3: Run Hebrew OCR with Tesseract

```python
import pytesseract
from PIL import Image

def ocr_hebrew_form(image_path, form_type="general"):
    """Run OCR on a preprocessed Israeli form image."""
    # Preprocess
    processed = preprocess_for_hebrew_ocr(image_path)

    # Tesseract configuration for Hebrew forms
    config = (
        '--oem 1 '          # LSTM neural net (best for Hebrew)
        '--psm 6 '          # Assume uniform block of text
        '-l heb+eng '       # Hebrew + English (forms have both)
        '-c preserve_interword_spaces=1'  # Keep spacing for field alignment
    )

    # For tabular forms (Tabu, Tofes 106), use PSM 4
    if form_type in ['tabu', 'tofes_106', 'tofes_100']:
        config = config.replace('--psm 6', '--psm 4')

    # Run OCR
    text = pytesseract.image_to_string(
        Image.fromarray(processed),
        config=config
    )

    # Also get structured data with bounding boxes
    data = pytesseract.image_to_data(
        Image.fromarray(processed),
        config=config,
        output_type=pytesseract.Output.DICT
    )

    return text, data
```

### Step 4: Extract Fields by Form Type

**Tabu Extract (Nesach Tabu):**
```python
import re

def extract_tabu_fields(ocr_text):
    """Extract structured fields from a Tabu extract."""
    fields = {}

    # Gush (block) number
    gush_match = re.search(r'גוש[:\s]*(\d+)', ocr_text)
    if gush_match:
        fields['gush'] = gush_match.group(1)

    # Chelka (parcel) number
    chelka_match = re.search(r'חלקה[:\s]*(\d+)', ocr_text)
    if chelka_match:
        fields['chelka'] = chelka_match.group(1)

    # Owner name — follows "בעלים" or "שם"
    owner_match = re.search(r'(?:בעלים|שם הבעלים)[:\s]*([\u0590-\u05FF\s]+)', ocr_text)
    if owner_match:
        fields['owner_name'] = owner_match.group(1).strip()

    # ID number
    tz_match = re.search(r'(?:ת\.?ז\.?|מספר זהות)[:\s]*(\d{5,9})', ocr_text)
    if tz_match:
        fields['tz_number'] = tz_match.group(1).zfill(9)

    # Rights type
    rights_match = re.search(r'(?:סוג הזכות|זכות)[:\s]*([\u0590-\u05FF\s]+)', ocr_text)
    if rights_match:
        fields['rights_type'] = rights_match.group(1).strip()

    return fields
```

**Tax Form (Tofes 106):**
```python
def extract_tofes_106_fields(ocr_text):
    """Extract structured fields from a Tofes 106 annual employer statement."""
    fields = {}

    # Tax year
    year_match = re.search(r'שנת מס[:\s]*(\d{4})', ocr_text)
    if year_match:
        fields['tax_year'] = year_match.group(1)

    # Employer number
    employer_match = re.search(r'(?:מספר מעביד|מס׳ עוסק)[:\s]*(\d{9})', ocr_text)
    if employer_match:
        fields['employer_number'] = employer_match.group(1)

    # Gross salary
    salary_match = re.search(r'(?:שכר ברוטו|הכנסה חייבת)[:\s]*₪?\s*([\d,]+\.?\d*)', ocr_text)
    if salary_match:
        fields['gross_salary'] = salary_match.group(1).replace(',', '')

    # Tax deducted
    tax_match = re.search(r'(?:מס שנוכה|ניכוי מס)[:\s]*₪?\s*([\d,]+\.?\d*)', ocr_text)
    if tax_match:
        fields['tax_deducted'] = tax_match.group(1).replace(',', '')

    # Employee TZ
    tz_match = re.search(r'(?:ת\.?ז\.?|זהות העובד)[:\s]*(\d{9})', ocr_text)
    if tz_match:
        fields['employee_tz'] = tz_match.group(1)

    return fields
```

### Step 5: Handle RTL and Bidirectional Text

```python
def normalize_bidi_text(text):
    """Normalize bidirectional text from Hebrew OCR output."""
    import unicodedata

    lines = text.split('\n')
    normalized = []

    for line in lines:
        # Strip bidi control characters
        clean = ''.join(
            c for c in line
            if unicodedata.category(c) != 'Cf'  # Remove format characters
        )
        # Normalize whitespace
        clean = ' '.join(clean.split())
        if clean:
            normalized.append(clean)

    return '\n'.join(normalized)


def detect_text_direction(text):
    """Detect whether a line is primarily Hebrew (RTL) or Latin (LTR)."""
    hebrew_chars = sum(1 for c in text if '\u0590' <= c <= '\u05FF')
    latin_chars = sum(1 for c in text if 'A' <= c <= 'z')

    if hebrew_chars > latin_chars:
        return 'rtl'
    return 'ltr'
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
User says: "I have 50 scanned Tofes 106 forms — extract salary and tax data"
Result: Set up batch pipeline — preprocess each image, OCR with Hebrew+English, extract Tofes 106 fields, validate, output to CSV/JSON with confidence scores.

### Example 3: OCR Quality Issues
User says: "The OCR isn't reading the Hebrew text correctly"
Result: Diagnose preprocessing — check image resolution (recommend 300 DPI minimum), verify deskewing, adjust binarization threshold, try different PSM modes, check Hebrew language pack installation.

## Troubleshooting

### Error: "Tesseract Hebrew language pack not found"
Cause: Hebrew traineddata not installed
Solution: Install with `sudo apt-get install tesseract-ocr-heb` (Ubuntu) or `brew install tesseract-lang` (macOS). Verify with `tesseract --list-langs`.

### Error: "OCR output is garbled or reversed"
Cause: Bidirectional text ordering issue
Solution: Use `normalize_bidi_text()` function. Ensure Tesseract is using `--oem 1` (LSTM mode). Check that the image is not mirrored.

### Error: "Low accuracy on specific form sections"
Cause: Poor scan quality, stamps/signatures overlapping text, colored backgrounds
Solution: Increase preprocessing — apply stronger denoising, crop to specific form regions, use ROI-based extraction for known form layouts.
```
