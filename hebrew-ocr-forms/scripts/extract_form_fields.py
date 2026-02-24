#!/usr/bin/env python3
"""Extract structured data from Israeli government forms using Hebrew OCR.

This script runs Tesseract OCR on preprocessed Israeli form images and
extracts structured fields based on the form type (Tabu, Tofes 106, etc.).

Usage:
    python extract_form_fields.py image.png --form-type tabu
    python extract_form_fields.py image.png --form-type tofes_106 --output result.json

Requirements:
    pip install pytesseract Pillow opencv-python numpy
    Also requires Tesseract OCR with Hebrew language pack:
      macOS: brew install tesseract tesseract-lang
      Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-heb
"""

import argparse
import json
import re
import sys
import unicodedata

try:
    import cv2
    import numpy as np
    import pytesseract
    from PIL import Image
except ImportError:
    print("Missing required dependencies. Install with:", file=sys.stderr)
    print("  pip install pytesseract Pillow opencv-python numpy", file=sys.stderr)
    print("Also install Tesseract OCR with Hebrew language pack:", file=sys.stderr)
    print("  macOS: brew install tesseract tesseract-lang", file=sys.stderr)
    print("  Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-heb", file=sys.stderr)
    sys.exit(1)


def ocr_hebrew_form(image_path, form_type="general"):
    """Run OCR on a preprocessed Israeli form image.

    Args:
        image_path: Path to image (preferably preprocessed).
        form_type: One of 'general', 'tabu', 'tofes_106', 'tofes_100'.

    Returns:
        Tuple of (raw_text, structured_data_dict).
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    # Tesseract configuration for Hebrew forms
    config = (
        '--oem 1 '          # LSTM neural net (best for Hebrew)
        '--psm 6 '          # Assume uniform block of text
        '-l heb+eng '       # Hebrew + English (forms have both)
        '-c preserve_interword_spaces=1'  # Keep spacing for field alignment
    )

    # For tabular forms, use PSM 4 (single column, variable sizes)
    if form_type in ('tabu', 'tofes_106', 'tofes_100'):
        config = config.replace('--psm 6', '--psm 4')

    # Run OCR
    text = pytesseract.image_to_string(
        Image.fromarray(img),
        config=config
    )

    # Also get structured data with bounding boxes
    data = pytesseract.image_to_data(
        Image.fromarray(img),
        config=config,
        output_type=pytesseract.Output.DICT
    )

    return text, data


def normalize_bidi_text(text):
    """Normalize bidirectional text from Hebrew OCR output.

    Strips Unicode bidi control characters and normalizes whitespace.

    Args:
        text: Raw OCR output text.

    Returns:
        Cleaned text with normalized whitespace and no bidi markers.
    """
    lines = text.split('\n')
    normalized = []
    for line in lines:
        clean = ''.join(
            c for c in line
            if unicodedata.category(c) != 'Cf'  # Remove format characters
        )
        clean = ' '.join(clean.split())
        if clean:
            normalized.append(clean)
    return '\n'.join(normalized)


def extract_tabu_fields(ocr_text):
    """Extract structured fields from a Tabu (land registry) extract.

    Args:
        ocr_text: Raw OCR text from a Nesach Tabu document.

    Returns:
        Dictionary of extracted fields.
    """
    fields = {}

    # Gush (block) number
    gush_match = re.search(r'גוש[:\s]*(\d+)', ocr_text)
    if gush_match:
        fields['gush'] = gush_match.group(1)

    # Chelka (parcel) number
    chelka_match = re.search(r'חלקה[:\s]*(\d+)', ocr_text)
    if chelka_match:
        fields['chelka'] = chelka_match.group(1)

    # Owner name -- follows "בעלים" or "שם"
    owner_match = re.search(
        r'(?:בעלים|שם הבעלים)[:\s]*([\u0590-\u05FF\s]+)', ocr_text
    )
    if owner_match:
        fields['owner_name'] = owner_match.group(1).strip()

    # ID number (Teudat Zehut)
    tz_match = re.search(
        r'(?:ת\.?ז\.?|מספר זהות)[:\s]*(\d{5,9})', ocr_text
    )
    if tz_match:
        fields['tz_number'] = tz_match.group(1).zfill(9)

    # Rights type
    rights_match = re.search(
        r'(?:סוג הזכות|זכות)[:\s]*([\u0590-\u05FF\s]+)', ocr_text
    )
    if rights_match:
        fields['rights_type'] = rights_match.group(1).strip()

    return fields


def extract_tofes_106_fields(ocr_text):
    """Extract structured fields from a Tofes 106 annual employer statement.

    Args:
        ocr_text: Raw OCR text from a Tofes 106 document.

    Returns:
        Dictionary of extracted fields.
    """
    fields = {}

    # Tax year
    year_match = re.search(r'שנת מס[:\s]*(\d{4})', ocr_text)
    if year_match:
        fields['tax_year'] = year_match.group(1)

    # Employer number
    employer_match = re.search(
        r'(?:מספר מעביד|מס׳ עוסק)[:\s]*(\d{9})', ocr_text
    )
    if employer_match:
        fields['employer_number'] = employer_match.group(1)

    # Gross salary
    salary_match = re.search(
        r'(?:שכר ברוטו|הכנסה חייבת)[:\s]*₪?\s*([\d,]+\.?\d*)', ocr_text
    )
    if salary_match:
        fields['gross_salary'] = salary_match.group(1).replace(',', '')

    # Tax deducted
    tax_match = re.search(
        r'(?:מס שנוכה|ניכוי מס)[:\s]*₪?\s*([\d,]+\.?\d*)', ocr_text
    )
    if tax_match:
        fields['tax_deducted'] = tax_match.group(1).replace(',', '')

    # Employee TZ
    tz_match = re.search(
        r'(?:ת\.?ז\.?|זהות העובד)[:\s]*(\d{9})', ocr_text
    )
    if tz_match:
        fields['employee_tz'] = tz_match.group(1)

    return fields


def validate_israeli_id(id_number):
    """Validate an Israeli ID number using the check digit algorithm.

    Args:
        id_number: String of 9 digits.

    Returns:
        True if the ID number is valid.
    """
    if not id_number or len(id_number) != 9 or not id_number.isdigit():
        return False

    total = 0
    for i, digit in enumerate(id_number):
        val = int(digit) * ((i % 2) + 1)
        if val > 9:
            val -= 9
        total += val

    return total % 10 == 0


def detect_form_type(ocr_text):
    """Auto-detect the Israeli form type from OCR text.

    Args:
        ocr_text: Raw OCR text.

    Returns:
        String form type identifier.
    """
    indicators = {
        'tabu': ['נסח טאבו', 'לשכת רישום המקרקעין', 'גוש', 'חלקה'],
        'tofes_106': ['טופס 106', 'דו״ח שנתי למעביד', 'דוח שנתי למעביד'],
        'tofes_857': ['טופס 857', 'רווח הון'],
        'ishur_nikui': ['אישור ניכוי מס במקור'],
        'bituach_leumi': ['אישור זכאויות', 'ביטוח לאומי'],
        'tofes_100': ['טופס 100', 'דין וחשבון'],
        'rishayon_rechev': ['רישיון רכב'],
    }

    for form_type, keywords in indicators.items():
        for keyword in keywords:
            if keyword in ocr_text:
                return form_type

    return 'general'


def main():
    parser = argparse.ArgumentParser(
        description="Extract fields from Israeli government forms via Hebrew OCR"
    )
    parser.add_argument("image", help="Path to form image")
    parser.add_argument(
        "--form-type",
        choices=['auto', 'tabu', 'tofes_106', 'tofes_100', 'general'],
        default='auto',
        help="Form type (default: auto-detect)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: stdout)"
    )
    parser.add_argument(
        "--raw-text", action="store_true",
        help="Also include raw OCR text in output"
    )
    args = parser.parse_args()

    print(f"Processing: {args.image}", file=sys.stderr)

    # Run OCR
    raw_text, ocr_data = ocr_hebrew_form(args.image, args.form_type)
    normalized_text = normalize_bidi_text(raw_text)

    # Detect or use specified form type
    if args.form_type == 'auto':
        form_type = detect_form_type(normalized_text)
        print(f"Detected form type: {form_type}", file=sys.stderr)
    else:
        form_type = args.form_type

    # Extract fields based on form type
    if form_type == 'tabu':
        fields = extract_tabu_fields(normalized_text)
    elif form_type == 'tofes_106':
        fields = extract_tofes_106_fields(normalized_text)
    else:
        fields = {"note": "No specific extractor for this form type"}

    # Validate TZ numbers if found
    for key in ('tz_number', 'employee_tz'):
        if key in fields:
            fields[f'{key}_valid'] = validate_israeli_id(fields[key])

    result = {
        "form_type": form_type,
        "fields": fields,
    }

    if args.raw_text:
        result["raw_text"] = normalized_text

    # Output
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Results saved to: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
