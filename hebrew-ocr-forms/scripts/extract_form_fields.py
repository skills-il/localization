#!/usr/bin/env python3
"""Extract structured data from Israeli government forms using Hebrew OCR.

This script runs Tesseract OCR on preprocessed Israeli form images and
extracts structured fields based on the form type (Tabu, Tofes 106, etc.).

Usage:
    python extract_form_fields.py image.png --form-type tabu
    python extract_form_fields.py image.png --form-type tofes_106 --output result.json
    python extract_form_fields.py image.png --lang heb+ara+eng --raw-text

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


TABULAR_FORMS = ('tabu', 'tofes_106', 'tofes_102', 'tofes_806_857')


def build_config(form_type, lang):
    """Tesseract config. Tabular forms use PSM 4 (single column, variable sizes)."""
    psm = 4 if form_type in TABULAR_FORMS else 6
    return (f'--oem 1 --psm {psm} -l {lang} '
            '-c preserve_interword_spaces=1')


def ocr_hebrew_form(image_path, form_type="general", lang="heb+eng"):
    """Run OCR on a preprocessed Israeli form image.

    Args:
        image_path: Path to image (preferably preprocessed).
        form_type: A form type id; tabular types are read with PSM 4.
        lang: Tesseract language list, e.g. 'heb+eng' or 'heb+ara+eng'.

    Returns:
        Tuple of (raw_text, word_data_dict). word_data_dict is
        pytesseract.image_to_data output and carries per-word confidence.
    """
    with open(image_path, 'rb') as fh:
        if fh.read(5) == b'%PDF-':
            raise ValueError(
                f"{image_path} is a PDF, not an image. If it is born-digital (has a text "
                "layer) extract the text with pdftotext instead of OCR. If it is a scan, "
                "rasterize each page first (pdftoppm -r 300 -png) and run this per page.")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    config = build_config(form_type, lang)
    pil = Image.fromarray(img)
    text = pytesseract.image_to_string(pil, config=config)
    data = pytesseract.image_to_data(pil, config=config, output_type=pytesseract.Output.DICT)
    return text, data


def field_confidence(fields, data):
    """Lowest OCR confidence among the tokens a field value was read from.

    Tokens are matched on their digits, so a glued token ("04221,340") still maps to the
    value it produced (21340). Only numeric fields are scored.
    """
    toks = [(re.sub(r'\D', '', str(w)), float(c)) for w, c in
            zip(data.get('text', []), data.get('conf', [])) if str(w).strip() and float(c) >= 0]
    out = {}
    for name, value in fields.items():
        digits = re.sub(r'\D', '', str(value)) if isinstance(value, str) else ''
        if len(digits) < 3:
            continue
        hits = [c for d, c in toks if len(d) >= 3 and (digits in d or d in digits)]
        if hits:
            out[name] = round(min(hits), 1)
    return out


def confidence_summary(data, low=60):
    """Mean word confidence and the words below `low`, from image_to_data output."""
    words = [(w, float(c)) for w, c in zip(data.get('text', []), data.get('conf', []))
             if str(w).strip() and float(c) >= 0]
    if not words:
        return {"mean": None, "words": 0, "low_confidence_words": []}
    mean = sum(c for _, c in words) / len(words)
    lows = [{"text": w, "conf": round(c, 1)} for w, c in words if c < low]
    return {"mean": round(mean, 1), "words": len(words), "low_confidence_words": lows}


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


# Labels are printed, typed and OCR'd with dots, ASCII quotes or Hebrew geresh/gershayim
# (ת.ז / ת"ז / ת״ז, מס' / מס׳), so every label pattern tolerates all of them.
Q = r'[.\'"\u05F3\u05F4]?'
TZ_LABEL = rf'(?:ת{Q}ז{Q}|מספר זהות(?: העובד)?|זהות העובד)'
NIKUD_RE = re.compile(r'[\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]')
SOFIT_MAP = str.maketrans('ךםןףץ', 'כמנפצ')
AMOUNT_RE = re.compile(r'(?<![\d/.])(-?(?:\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?|\d{4,}(?:\.\d{1,2})?))(?![\d/]|\.\d)')
# A number directly after a field code or row label may be small (a zero tax, a low salary).
# Rejects a number followed by a letter (OCR'd "O" for 0: "18O,500") or by a space-grouped
# thousands block ("184 500"): returning "18" or "184" would be silently wrong.
ROW_AMOUNT_RE = re.compile(r'^\s*[:₪]?\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?)'
                           r'(?![\d/A-Za-z\u05D0-\u05EA,]|\.\d|\s\d{3}(?!\d))')
WELL_FORMED_RE = re.compile(r'-?(?:\d{1,3}(?:,\d{3})+(?:\.\d{1,2})?|\d+\.\d{2})$')
# No \b: Tesseract glues words to numbers ("בתאריך15/03/2025"), and a Hebrew letter
# next to a digit is not a word boundary.
DATE_RE = re.compile(r'(?<![\d/.])\d{1,2}[./]\d{1,2}[./]\d{2,4}(?![\d/]|\.\d)')


def match_key(text):
    """Normalize text for keyword matching only: no nikud, no sofit, no spaces/quotes.

    Tesseract often drops the space between a Hebrew word and a number in RTL lines
    ("טופס106"), so keywords are compared with all whitespace and quote marks removed.
    Never use this for stored values.
    """
    text = NIKUD_RE.sub('', text).translate(SOFIT_MAP)
    return re.sub(r'[\s"\'\u05F3\u05F4]', '', text)


# 9 digits, or 8 when the leading zero was not printed; shorter reads are fragments.
TZ_DIGITS = r'(\d{8}-\d|\d{8,9})(?![\d-])'


def _id_field(match):
    """Return (id, padded) for a captured id; an 8-digit id is left-padded to 9."""
    raw = match.group(1).replace('-', '')
    return raw.zfill(9), len(raw) < 9


def extract_tabu_fields(ocr_text):
    """Extract the property key and the FIRST owner from a Nesach Tabu.

    A Nesach has many owners, mortgages and cautions; for the full table use
    tabu_to_spreadsheet.py on this script's --raw-text output.
    """
    fields = {}
    gush = re.search(r'גוש[:\s]*(\d+)', ocr_text)
    if gush:
        fields['gush'] = gush.group(1)
    no_tat = re.sub(r'תת[\s\-\u05BE]*חלקה[:\s]*\d+', ' ', ocr_text)
    helka = re.search(r'חלקה[:\s]*(\d+)', no_tat)
    if helka:
        fields['chelka'] = helka.group(1)
    tat = re.search(r'תת[\s\-\u05BE]*חלקה[:\s]*(\d+)', ocr_text)
    if tat:
        fields['tat_chelka'] = tat.group(1)
    tz = re.search(TZ_LABEL + r'[:\s]*' + TZ_DIGITS, ocr_text)
    if tz:
        fields['tz_number'], padded = _id_field(tz)
        if padded:
            fields['tz_number_padded'] = True
    return fields


def _row_amount(text_after):
    """The amount printed right after a field code or label, or None.

    OCR often glues the code to the amount ("04221,340"); a glued remainder is accepted
    only when it is a well-formed amount, so a real amount that merely begins with the
    code's digits is not cut.
    """
    text_after = DATE_RE.sub(' ', text_after)
    m = ROW_AMOUNT_RE.match(text_after)
    if not m:
        return None
    return m.group(1).replace(',', '')


def _amount_after(line, code_re, label_re):
    """Find the amount on a row: after the field code if present, else after the label.

    If a field code is on the line but no clean amount follows it, return None rather
    than falling back to the label (the label fallback would read the glued code).
    """
    code_seen = False
    for m in code_re.finditer(line):
        code_seen = True
        rest = line[m.end():]
        if rest.startswith('-'):
            # "042-21,340": a hyphen glued to the code is a separator or a table rule,
            # not a minus sign.
            rest = ' ' + rest[1:]
        if rest[:1].isdigit():
            glued = re.match(r'(-?[\d,]+(?:\.\d{1,2})?)', rest).group(1)
            if WELL_FORMED_RE.match(glued):
                return glued.replace(',', '')
            continue
        amt = _row_amount(rest)
        if amt is not None:
            return amt
    if code_seen:
        return None
    m = label_re.search(line)
    if m:
        rest = re.sub(r'^\s*\(\d\)', '', line[m.end():])
        amt = _row_amount(rest)
        if amt is None:
            return None
        bare = amt.lstrip('-')
        later = AMOUNT_RE.findall(DATE_RE.sub(' ', rest)[rest.find(bare) + len(bare):])
        # A short leading number followed by a real amount is a code whose leading zero
        # OCR dropped ("42 21,340") or a count ("12 חודשים 184,500"): ambiguous, so the
        # row is reported instead of guessed.
        if bare in KNOWN_CODES or (len(bare.split('.')[0]) < 4 and ',' not in bare and later):
            return None
        return amt
    return None


# No digit lookahead: a code glued to its amount ("172/158184,500") must still match;
# _amount_after only accepts a glued remainder that is a well-formed amount.
KNOWN_CODES = {'42', '042', '158', '172'}
SALARY_CODE_RE = re.compile(r'(?<!\d)(?:172/158|158/172|158|172)(?!/)')
SALARY_LABEL_RE = re.compile(r'משכורת(?:\s*\(\d\))?|שכר ברוטו')
TAX_CODE_RE = re.compile(r'(?<![\d,.])042')
TAX_LABEL_RE = re.compile(r'ניכיתי ושילמתי מס הכנסה(?:\s*\(\d\))?|מס שנוכה')
TITLE_RE = re.compile(r'אישור|טופס|תקנות')


def extract_tofes_106_fields(ocr_text):
    """Extract fields from a Form 106 (אישור על משכורת וניכוי מס).

    Amounts are read only from the salary row ("משכורת", field 158/172) and the tax row
    ("ניכיתי ושילמתי מס הכנסה", field 042), taking the number printed right after the
    field code or label. A bare 42/158/172 elsewhere (a street number, a phone, a branch)
    is never used, and the title line is skipped. If a row is found but its amount cannot
    be read, the field is omitted and listed in `rows_without_amount`.
    """
    fields = {}
    year = re.search(r'שנת\s*(?:ה)?מס[^\d\n]{0,6}(\d{4})', ocr_text)
    if year:
        fields['tax_year'] = year.group(1)
    employer = re.search(rf'(?:מספר תיק ניכויים|תיק ניכויים|מספר מעביד|מס{Q} עוסק)[:\s]*(\d{{8,9}})', ocr_text)
    if employer:
        fields['withholding_file_number'] = employer.group(1)
    tz = re.search(TZ_LABEL + r'[:\s]*' + TZ_DIGITS, ocr_text)
    if tz:
        fields['employee_tz'], padded = _id_field(tz)
        if padded:
            fields['employee_tz_padded'] = True
    elif re.search(TZ_LABEL + r'[:\s]*\d', ocr_text):
        fields['employee_tz_unreadable'] = True  # a labelled id that is not 8-9 digits

    missing = []
    for name, label_re, code_re in (('salary_158_172', SALARY_LABEL_RE, SALARY_CODE_RE),
                                    ('income_tax_042', TAX_LABEL_RE, TAX_CODE_RE)):
        row_seen = False
        for line in ocr_text.split('\n'):
            if not label_re.search(line) or (TITLE_RE.search(line) and not code_re.search(line)):
                continue
            row_seen = True
            amt = _amount_after(line, code_re, label_re)
            if amt is not None and name == 'salary_158_172' and len(amt.lstrip('-').split('.')[0]) < 3:
                amt = None  # a one- or two-digit "salary" is a stray token, not the row's amount
            if amt is not None:
                fields[name] = amt
                break
        if row_seen and name not in fields:
            missing.append(name)
    if missing:
        fields['rows_without_amount'] = missing
    try:
        if float(fields['income_tax_042']) > float(fields['salary_158_172']):
            # Flag, never correct: tax withheld above salary means a misread somewhere.
            fields['tax_exceeds_salary'] = True
    except (KeyError, ValueError):
        pass
    negative = [n for n in ('salary_158_172', 'income_tax_042') if fields.get(n, '').startswith('-')]
    if negative:
        fields['negative_amounts'] = negative  # rare on a 106; confirm against the form
    return fields


CURRENCY_AMOUNT_RE = re.compile(r'(?:₪|ש"ח|ש״ח|שח)\s*(-?\d{1,3}(?:\.\d{1,2})?)(?![\d,])|(?<![\d,.])(-?\d{1,3}(?:\.\d{1,2})?)\s*(?:₪|ש"ח|ש״ח)')


def _generic_amounts(ocr_text, ids):
    """Amounts with 4+ digits or thousands separators, plus small amounts next to ₪ / ש"ח.

    Dates are masked first so a year is never listed as an amount, and 9-digit ids are
    excluded.
    """
    text = DATE_RE.sub(' ', ocr_text)
    out = [a.replace(',', '') for a in AMOUNT_RE.findall(text)
           if a.lstrip('-').split('.')[0] not in ids]
    for m in CURRENCY_AMOUNT_RE.finditer(text):
        out.append(m.group(1) or m.group(2))
    return out


def extract_generic_fields(ocr_text):
    """For form types without a dedicated extractor: every id, date and amount found.

    The agent maps these to the form's own labels using raw_text; nothing here claims
    to know which amount is which.
    """
    ids = []
    for m in re.finditer(r'(?<!\d)(\d{9})(?!\d)', ocr_text):
        ids.append({"value": m.group(1), "valid_israeli_id": validate_israeli_id(m.group(1))})
    return {
        "candidate_ids": ids,
        "dates": DATE_RE.findall(ocr_text),
        "amounts": _generic_amounts(ocr_text, {i["value"] for i in ids}),
        "percentages": re.findall(r'(?<![\d.])(\d{1,3}(?:\.\d{1,2})?)\s*%', ocr_text),
        "note": "No dedicated extractor for this form type: values are listed, not labelled. "
                "Map them to fields using raw_text.",
    }


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


# Checked in order; the most specific forms come first. Each entry is (form, title
# phrases matched anywhere, phrases matched only on short lines near the top: form numbers,
# and headers such as the BL institution name that also appear inside other documents). A
# document that merely MENTIONS "טופס 106" in its body (a refund request, a BL letter) is
# not a 106. Bare גוש/חלקה is NOT enough for a Nesach (arnona bills print them too).
FORM_INDICATORS = [
    # 102 first: its body can mention ניכוי ממשכורת, a 106 never carries the 102 title.
    ('tofes_102', ['דין וחשבון על העסקת עובדים'], ['טופס 102']),
    ('tofes_106', ['אישור על משכורת וניכוי מס'], ['טופס 106', 'ניכוי ממשכורת']),
    ('tofes_806_857', ['אישור שנתי על ניכוי מס הכנסה מתשלומים'],
     ['0806/0857', 'טופס 857', 'טופס 806']),
    ('ishur_nikui', ['אישור ניכוי מס במקור', 'אישור ניהול ספרים וניכוי מס במקור'], []),
    ('tabu', ['נסח טאבו', 'נסח רישום', 'לשכת רישום המקרקעין', 'פנקסי המקרקעין'], []),
    # Rights confirmations for unregistered property (רמ"י, a developer, a housing company)
    # look like a Nesach but are not one (and never carry its title); keep them out of the tabu
    # extractor.
    ('rights_confirmation', [], ['אישור זכויות']),
    ('rishayon_rechev', ['רישיון רכב', 'רשיון רכב'], []),
    # "אישור זכאות" / "אישור על תשלום" are generic titles (housing, utilities), so a BL
    # certificate is recognized by the institution's own header.
    ('bituach_leumi', [], ['המוסד לביטוח לאומי']),
]
HEADER_LINES = 6


def _keyword_re(keyword):
    """Space/quote-insensitive pattern; numbers are digit-bounded, and a "<word> <number>"
    keyword also matches the "<number> <word>" order Tesseract can produce in RTL lines."""
    def build(k):
        parts = re.split(r'(\d+)', match_key(k))
        return ''.join(rf'(?<!\d){p}(?!\d)' if p.isdigit() else re.escape(p) for p in parts if p)
    alts = [build(keyword)]
    m = re.fullmatch(r'(\D+?)\s*(\d+)', keyword)
    if m:
        alts.append(build(m.group(2) + m.group(1)))
        # A form-number keyword must not be glued to a preceding Hebrew letter: "בטופס 106"
        # ("in Form 106") is a mention, not a title.
        alts = [rf'(?<![\u05D0-\u05EA]){a}' for a in alts]
    return re.compile('|'.join(alts))


def detect_form_type(ocr_text):
    """Auto-detect the Israeli form type from OCR text."""
    key = match_key(ocr_text)
    # Form numbers count only on short title-like lines near the top, each line matched on
    # its own, so "יש לצרף טופס 106" in the body of another document is not a 106.
    head = [match_key(l) for l in ocr_text.split('\n')[:HEADER_LINES] if len(l.split()) <= 6]
    for form_type, titles, numbers in FORM_INDICATORS:
        if any(_keyword_re(k).search(key) for k in titles) or \
                any(_keyword_re(k).search(h) for k in numbers for h in head):
            return form_type
    if 'גוש' in key and 'חלקה' in key and re.search(r'בעלויות|משכנתאות|הערותאזהרה', key):
        return 'tabu'
    return 'general'


FORM_TYPES = ['auto', 'tabu', 'tofes_106', 'tofes_806_857', 'tofes_102', 'ishur_nikui',
              'bituach_leumi', 'rishayon_rechev', 'rights_confirmation', 'general']


def main():
    parser = argparse.ArgumentParser(
        description="Extract fields from Israeli government forms via Hebrew OCR"
    )
    parser.add_argument("image", help="Path to form image (one page; rasterize PDFs first)")
    parser.add_argument("--form-type", choices=FORM_TYPES, default='auto',
                        help="Form type (default: auto-detect)")
    parser.add_argument("--lang", default="heb+eng",
                        help="Tesseract languages (default heb+eng; add ara for Arabic sections)")
    parser.add_argument("--output", "-o", help="Output JSON file path (default: stdout)")
    parser.add_argument("--raw-text", action="store_true",
                        help="Also include raw OCR text in output")
    args = parser.parse_args()

    print(f"Processing: {args.image}", file=sys.stderr)
    try:
        raw_text, ocr_data = ocr_hebrew_form(args.image, args.form_type, args.lang)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    normalized_text = normalize_bidi_text(raw_text)

    if args.form_type == 'auto':
        form_type = detect_form_type(normalized_text)
        print(f"Detected form type: {form_type}", file=sys.stderr)
        if form_type in TABULAR_FORMS:
            # The first pass used PSM 6; tabular forms read better with PSM 4.
            raw_text, ocr_data = ocr_hebrew_form(args.image, form_type, args.lang)
            normalized_text = normalize_bidi_text(raw_text)
    else:
        form_type = args.form_type

    if form_type == 'tabu':
        fields = extract_tabu_fields(normalized_text)
    elif form_type == 'tofes_106':
        fields = extract_tofes_106_fields(normalized_text)
    else:
        fields = extract_generic_fields(normalized_text)

    for key in ('tz_number', 'employee_tz'):
        if key in fields:
            fields[f'{key}_valid'] = validate_israeli_id(fields[key])

    result = {
        "form_type": form_type,
        "fields": fields,
        "ocr_confidence": confidence_summary(ocr_data),
        "field_confidence": field_confidence(fields, ocr_data),
        "notice": "Unofficial OCR transcription, not the issuing authority's record. Confirm "
                  "every value against the original document before relying on it.",
    }
    if not normalized_text.strip():
        result["warning"] = "OCR returned no text. Check the image, language data and preprocessing."
    if args.raw_text:
        result["raw_text"] = normalized_text

    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Results saved to: {args.output}", file=sys.stderr)
    else:
        print(output_json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
