#!/usr/bin/env python3
"""Turn a Nesach Tabu (land-registry extract) into a normalized spreadsheet.

A Nesach Tabu has repeating sections: many owners (each with a fractional share),
many mortgages, many cautions, plus liens, court orders, expropriations and easements.
This script flattens the OCR text of one extract into a normalized CSV where a `section`
column marks each row, and a `detail` column carries the section-specific extras (a
mortgage's degree, a caution's beneficiary and reference, a lease's end date). Every row
carries the gush / helka / tat_helka key so several extracts concatenate cleanly.

This is a best-effort STRUCTURING AID for a lawyer or clerk to review, NOT a substitute
for reading the Nesach. Land registry documents are legally consequential and OCR is
noisy, so the script is loud about what it could not place: content before the first
recognized section header is emitted as `section=unrecognized`, and it prints warnings to
stderr for a section header with no parsed rows, a concentrated/historical Nesach, owner
shares that do not sum exactly to the whole, padded or failing ת.ז. numbers, and an empty
result. Always read the warnings.

It writes UTF-8 with a BOM so Excel detects the encoding and shows the Hebrew correctly
(the sheet direction itself is an Excel view setting a CSV cannot carry). It keeps the
share verbatim (125/1000, not 0.125) because rounding a long denominator loses legal
precision. See references/nesach-tabu-structure.md for the section-to-column mapping.

Usage:
  python tabu_to_spreadsheet.py --file ocr_text.txt --out nesach.csv
  python tabu_to_spreadsheet.py --json extracted.json --out nesach.csv   # needs raw_text
  python tabu_to_spreadsheet.py --example
"""

import argparse
import csv
import io
import json
import re
import sys
from fractions import Fraction

GUSH_RE = re.compile(r'גוש[:\s]*(\d+)')
# Match תת-חלקה FIRST and remove it, so the plain-חלקה match cannot pick up the digits
# that belong to the sub-parcel. The separator may be a space, a hyphen or a maqaf (־).
TAT_HELKA_RE = re.compile(r'תת[\s\-\u05BE]*חלקה[:\s]*(\d+)')
HELKA_RE = re.compile(r'חלקה[:\s]*(\d+)')

# Labels are printed or OCR'd with dots, ASCII quotes or Hebrew geresh/gershayim.
_Q = r'[.\'"\u05F3\u05F4]?'
PERSONAL_LABEL = rf'(?:ת{_Q}ז{_Q}|מספר זהות)'
OTHER_LABEL = rf'(?:ח{_Q}פ{_Q}|מספר תאגיד|ע{_Q}ר{_Q}|דרכון)'
# A personal ת.ז. is 9 digits, or 8 when the leading zero was not printed, optionally
# with the check digit split off by a hyphen. Shorter reads are fragments, never padded. Company / amuta numbers may be printed with
# hyphens (51-234567-8); passports may start with up to two letters.
PERSONAL_ID_RE = re.compile(PERSONAL_LABEL + r'[:\s]*(\d{8}-\d|\d{8,9})(?![\d-])')
OTHER_ID_RE = re.compile(OTHER_LABEL + r'[:\s]*([A-Z]{0,2}\d{5,9}|\d{2}-\d{6}-\d)(?![\d-])')
# A share is a single a/b fraction. The look-arounds stop it from matching inside a deed
# number such as 12345/2015/1.
SHARE_RE = re.compile(r'((?<![\d/])\d{1,7}\s*/\s*\d{1,7}(?![\d/])|בשלמות)')
DEGREE_RE = re.compile(r'דרגה\s*([א-ת]\S*)')
BENEFICIARY_RE = re.compile(r'לטובת[:\s]+(.+)')
SECTION_REF_RE = re.compile(r'סעיף\s*\d+[א-ת]?')
DATE_RE = re.compile(r'(?<![\d/.])\d{1,2}[./]\d{1,2}[./]\d{2,4}(?![\d/]|\.\d)')
# Word-bounded, so the עד inside מועד or הועדה is not a marker. סיום / תום win over עד.
END_DATE_RE = re.compile(r'(?<![\u05D0-\u05EA])[בהל]?(?:סיום|תום)(?![\u05D0-\u05EA])\D{0,20}?'
                         r'(\d{1,2}[./]\d{1,2}[./]\d{2,4})')
UNTIL_DATE_RE = re.compile(r'(?<![\u05D0-\u05EA])עד(?![\u05D0-\u05EA])\D{0,20}?'
                           r'(\d{1,2}[./]\d{1,2}[./]\d{2,4})')
# A deed (שטר) number: three slash-separated parts (12345/2015/1), or an older two-part
# number when it directly follows the word שטר. Kept in `detail`, never read as the share.
DEED_RE = re.compile(r'(?:שטר\s*)?(?<![\d/])\d{1,7}/\d{4}/\d{1,4}(?![\d/])|שטר\s*\d{1,7}/\d{1,4}(?![\d/])')

# Nikud and cantillation only: U+0591-U+05C7 minus the maqaf, paseq, sof pasuq and nun
# hafukha punctuation inside that range.
NIKUD_RE = re.compile('[\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]')
SOFIT_MAP = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}


def strip_key(text):
    """Normalize a string for label/header matching only (never for stored values)."""
    text = NIKUD_RE.sub('', text)
    return ''.join(SOFIT_MAP.get(ch, ch) for ch in text)


# Section HEADERS are recognized only when the whole line is made of header words
# (optionally joined by ו / "על הזכויות" / a colon). A content line such as "צו הריסה
# מנהלי" or "בנק לאומי למשכנתאות בעמ" contains a section keyword but is NOT a header;
# treating keyword-containing short lines as headers silently dropped liens, orders and
# creditors in earlier versions. Order of SECTION_WORDS decides a compound header.
SECTION_WORDS = [
    ('owner', ['בעלויות', 'בעלות', 'בעלים']),
    ('lease', ['חכירות', 'חכירה']),
    ('mortgage', ['משכנתאות', 'שעבודים']),
    ('lien', ['עיקולים']),
    ('expropriation', ['הפקעות']),
    ('easement', ['זיקות', 'זיקת']),
    ('order', ['צווים']),
    ('caution', ['הערות', 'הערה']),
]
FILLER_WORDS = {'ו', 'רישום', 'על', 'הזכויות', 'הנכס', 'אזהרה', 'הנאה', 'שיפוטיים', 'נוספות'}
_HEADER_LOOKUP = {strip_key(w): name for name, words in SECTION_WORDS for w in words}
_FILLER = {strip_key(w) for w in FILLER_WORDS}
# An entry line normally starts with its TYPE; a line that does so is never merged into
# the entry above it.
ENTRY_TYPE_RE = re.compile(r'^(?:משכנת[אה]|הערת אזהרה|הערה|עיקול|צו|זיקת הנאה|הפקעה|חכירה|שעבוד)(?![א-ת])')
ENTRY_SPLIT_RE = re.compile(r'[,;]\s*(?=(?:משכנת[אה]|הערת אזהרה|עיקול|צו)(?![א-ת]))')
# "חלק" here is the share LABEL; the lookahead stops it from eating "חלקה" (parcel).
SHARE_LABEL_RE = re.compile(r'חלק(?=[\s\d/]|$)')
# Lines that are document furniture, not section content (registry office title etc.).
FURNITURE_RE = re.compile(r'לשכת\s*רישום|פנקס|רשות\s*לרישום|נסח\s*טאבו|נסח\s*רישום')
ENCUMBRANCE_SECTIONS = ('mortgage', 'caution', 'lien', 'order', 'expropriation', 'easement')
# A line carrying its own degree, deed, id, section reference or case/file number is its own
# entry even when OCR dropped the type word, so it is never merged into the entry above.
OWN_ENTRY_RE = re.compile(r'דרגה|שטר|סעיף\s*\d|תיק\s*\d|(?<![\d/])\d{1,7}/\d{2,4}(?:/\d{1,4})?(?![\d/])')
TYPE_WORDS_RE = re.compile(r'משכנת[אה]|הערת אזהרה|הערה|עיקול|צו|זיקת הנאה|הפקעה|שעבוד|רוכש')


def _classify_header(folded):
    """Return the section name if the whole line is a section header, else None."""
    words = re.sub(r'[:\-\u05BE,.()]', ' ', folded).split()
    if not words:
        return None
    section = None
    for w in words:
        w = w[1:] if w.startswith('ו') and len(w) > 2 and w[1:] in _HEADER_LOOKUP else w
        if w in _HEADER_LOOKUP:
            section = section or _HEADER_LOOKUP[w]
        elif w not in _FILLER:
            return None
    return section


def _first(pattern, text):
    m = pattern.search(text)
    return m.group(1).strip() if m else ''


def _owner_id(line):
    """(id, is_personal). Hyphenated numbers are joined; a personal ת.ז. comes first."""
    m = PERSONAL_ID_RE.search(line)
    if m:
        return m.group(1).replace('-', ''), True
    m = OTHER_ID_RE.search(line)
    if m:
        return m.group(1).replace('-', ''), False
    return '', False


def _share(line):
    """Extract an ownership share, ignoring dates and deed numbers."""
    return _first(SHARE_RE, DEED_RE.sub(' ', DATE_RE.sub(' ', line)))


def _extract_property_key(text):
    key = strip_key(text)
    gush = _first(GUSH_RE, key)
    tat_helka = _first(TAT_HELKA_RE, key)
    key_wo_tat = TAT_HELKA_RE.sub(' ', key)
    helka = _first(HELKA_RE, key_wo_tat)
    return gush, helka, tat_helka


def _build_detail(section, line):
    """Section-specific extras that would otherwise be lost in the name blob."""
    bits = []
    if section == 'mortgage':
        deg = _first(DEGREE_RE, line)
        if deg:
            bits.append(f'דרגה {deg}')
    if section in ENCUMBRANCE_SECTIONS:
        ben = BENEFICIARY_RE.search(line)
        if ben:
            bits.append('לטובת ' + ben.group(1).strip())
        ref = SECTION_REF_RE.search(line)
        if ref and not (ben and ref.group(0) in ben.group(1)):
            bits.append(ref.group(0))
    deed = DEED_RE.search(line)
    if deed:
        d = deed.group(0)
        bits.append(d if d.startswith('שטר') else 'שטר ' + d)
    if section == 'lease':
        end = END_DATE_RE.search(line) or UNTIL_DATE_RE.search(line)
        dates = DATE_RE.findall(DEED_RE.sub(' ', line))
        if end:
            bits.append('עד ' + end.group(1))
        elif dates:
            # No "עד/סיום" marker: report every date rather than guess which one ends it.
            bits.append('תאריכים: ' + ', '.join(dates))
    return '; '.join(bits)


def _clean_name(line):
    name = PERSONAL_ID_RE.sub('', line)
    name = OTHER_ID_RE.sub('', name)
    # A bare id label with no number after it (OCR dropped the digits).
    name = re.sub(rf'(?:{PERSONAL_LABEL}|{OTHER_LABEL})(?=[:\s]*$)', '', name)
    name = DEED_RE.sub('', name)
    name = DEGREE_RE.sub('', name)
    name = DATE_RE.sub('', name)
    name = SHARE_RE.sub('', name)
    name = SHARE_LABEL_RE.sub('', name)
    name = SECTION_REF_RE.sub('', name)
    name = re.sub(r'לטובת[:\s]*', '', name)
    # Keep Hebrew, spaces, quotes, hyphen, Latin letters and digits (company names).
    name = re.sub(r'[^\u0590-\u05FFA-Za-z0-9\s"\'\-]', '', name)
    name = ' '.join(name.split())
    return re.sub(r'(?:\s+(?:עד|מ-?|תאריך סיום|מועד תחילה))+$', '', name).strip()


def _has_party(row):
    """True if an encumbrance row already names someone (beyond its type words)."""
    rest = TYPE_WORDS_RE.sub('', row['name'])
    rest = re.sub(r'[\d\s"\'\-]', '', rest)
    return bool(rest or row['owner_id'] or 'לטובת' in row['detail'])


def _make_row(base, section, line):
    oid, personal = _owner_id(line)
    label_no_id = bool(re.search(PERSONAL_LABEL + r'[:\s]*\d', line)) and not oid
    n_ids = len(PERSONAL_ID_RE.findall(line)) + len(OTHER_ID_RE.findall(line))
    share = _share(line) if section in ('owner', 'lease', 'unrecognized') else ''
    detail = _build_detail(section, line)
    if section in ENCUMBRANCE_SECTIONS:
        # On an encumbrance row an a/b number is not an ownership share: it may be a case or
        # file number, or the fraction of the rights encumbered ("על 1/2 מהזכויות"). Kept
        # verbatim in detail, unlabelled, for the reader to interpret.
        nums = [m for m in re.findall(r'(?<![\d/])\d{1,7}/\d{1,7}(?![\d/])', DEED_RE.sub(' ', DATE_RE.sub(' ', line)))]
        if nums:
            detail = '; '.join(x for x in (detail, ', '.join(nums)) if x)
    return dict(base, section=section, name=_clean_name(line), owner_id=oid,
                share=share, detail=detail, _personal=personal,
                _label_no_id=label_no_id, _typed=bool(ENTRY_TYPE_RE.match(line)), _n_ids=n_ids)


def parse_nesach(ocr_text):
    """Parse raw Nesach OCR text into normalized rows. Returns (rows, warnings)."""
    gush, helka, tat_helka = _extract_property_key(ocr_text)
    base = {'gush': gush, 'helka': helka, 'tat_helka': tat_helka}
    rows = [dict(base, section='property', name='', owner_id='', share='', detail='')]
    warnings = []

    if re.search(r'מרוכז|מְרֻכָּז', ocr_text):
        warnings.append('This looks like a נסח מרוכז (concentrated extract) covering a whole '
                        'building: it holds many apartments, each with its own owners. The single '
                        'gush/helka/tat_helka key and the owner-share-sum check do NOT hold. Split '
                        'per apartment by hand.')
    if re.search(r'היסטורי|מחוק', ocr_text):
        warnings.append('This looks like a נסח היסטורי (or contains struck-through מחוק owners). '
                        'Past/deleted owners may be emitted as if current. Verify each owner row.')

    lines = []
    for raw in ocr_text.split('\n'):
        raw = raw.strip()
        if raw:
            parts = [p.strip() for p in ENTRY_SPLIT_RE.split(raw) if p.strip()]
            for part in parts:
                # Two owners printed on one line ("א ת.ז. ... 1/2, ב ת.ז. ... 1/2").
                if len(PERSONAL_ID_RE.findall(part)) + len(OTHER_ID_RE.findall(part)) > 1:
                    lines.extend(p.strip() for p in re.split(r'[,;]\s+', part) if p.strip())
                else:
                    lines.append(part)

    current = None
    headers_seen = []          # (section, rows_before) to detect empty sections
    unplaced = []
    i = 0
    while i < len(lines):
        line = lines[i]
        folded = strip_key(line)
        header = _classify_header(folded)
        if header:
            current = header
            headers_seen.append((header, len(rows)))
            i += 1
            continue

        if current is None:
            # The property line (has גוש) and document furniture are expected before the
            # first section and are already captured in the key.
            if not (GUSH_RE.search(folded) or FURNITURE_RE.search(line)):
                unplaced.append(dict(_make_row(base, 'unrecognized', line)))
            i += 1
            continue

        # Multi-line owner/lease block: a name-only line followed by an id/share-only line.
        if current in ('owner', 'lease') and not _owner_id(line)[0] and not _share(line) \
                and i + 1 < len(lines):
            nxt = lines[i + 1]
            if (_owner_id(nxt)[0] or _share(nxt)) and not _classify_header(strip_key(nxt)) \
                    and not _clean_name(nxt):
                line = line + ' ' + nxt
                i += 1

        row = _make_row(base, current, line)
        prev = rows[-1] if rows[-1]['section'] == current else None
        # An id starts a new entry only when the entry above already names its party; a
        # type-only entry ("משכנתא דרגה ראשונה") takes the creditor line below it, id and all.
        own_entry = bool(ENTRY_TYPE_RE.match(line) or OWN_ENTRY_RE.search(line)
                         or (_owner_id(line)[0] and (prev is None or _has_party(prev))))
        is_beneficiary = line.lstrip().startswith('לטובת')
        if current in ENCUMBRANCE_SECTIONS and prev is not None and (is_beneficiary or not own_entry):
            if is_beneficiary:
                # Column-wise OCR can print several type-only entries and then their
                # beneficiaries: give the line to the earliest entry with no party yet.
                block = []
                for r in reversed(rows):
                    if r['section'] != current:
                        break
                    block.insert(0, r)
                open_entries = [r for r in block if not _has_party(r)]
                target = open_entries[0] if open_entries else None
                if len(open_entries) > 1:
                    warnings.append(f'"{line}" was given to "{target["name"]}", the first of '
                                    f'{len(open_entries)} entries with no beneficiary yet. Check the pairing.')
                if target is None:
                    target = prev
                    warnings.append(f'"{line}" could not be matched to an entry without a '
                                    f'beneficiary; it was attached to "{prev["name"]}". Check it.')
            else:
                # A bare creditor name on its own line belongs to the entry above it (a
                # second bank on the same mortgage is a joint creditor).
                target = prev
            target['name'] = ' '.join(x for x in (target['name'], row['name']) if x)
            target['owner_id'] = target['owner_id'] or row['owner_id']
            target['_personal'] = target.get('_personal') or row['_personal']
            target['detail'] = '; '.join(x for x in (target['detail'], row['detail']) if x)
        elif row['name'] or row['owner_id'] or row['share'] or row['detail']:
            rows.append(row)
        i += 1

    if unplaced:
        warnings.append(f'{len(unplaced)} content line(s) appeared before any recognized section '
                        'header and were emitted as section=unrecognized. A section title was '
                        'probably garbled by OCR; review them by hand.')
        rows.extend(unplaced)
    for n, (section, before) in enumerate(headers_seen):
        after = headers_seen[n + 1][1] if n + 1 < len(headers_seen) else len(rows) - len(unplaced)
        if after == before:
            warnings.append(f'Section "{section}" has a header but no rows were parsed under it. '
                            'Its entries were probably lost or garbled; read that section by hand.')
    if not any(r['section'] not in ('property',) for r in rows):
        warnings.append('No owner, lease or encumbrance rows were found. The input is empty, is not '
                        'a Nesach, or its section titles were not recognized. Do not treat an empty '
                        'sheet as "no encumbrances".')
    if not (gush and helka):
        warnings.append('gush/helka not found in the text; the property key columns are empty.')
    for r in rows:
        oid = r.get('owner_id', '')
        if r.get('_personal') and oid.isdigit():
            if len(oid) < 9:
                warnings.append(f'{r["section"]} row "{r["name"]}": ת.ז. {oid} has fewer than 9 digits '
                                'and was checked left-padded with zeros. A truncated read can pass by '
                                'chance; confirm it against the extract.')
            if not valid_israeli_id(oid):
                warnings.append(f'{r["section"]} row "{r["name"]}": ת.ז. {oid} fails the Israeli ID '
                                'check digit, most likely an OCR misread. Check it against the extract.')
        if r.get('_label_no_id'):
            warnings.append(f'{r["section"]} row "{r["name"]}": a ת.ז. label is followed by a number '
                            'that is not 8-9 digits (an OCR misread), so no id was recorded.')
        if r['section'] in ENCUMBRANCE_SECTIONS and r['section'] != 'mortgage' \
                and not r.get('_typed', True):
            warnings.append(f'{r["section"]} row "{r["name"]}" does not start with an entry type: it may '
                            'be a separate entry, or a wrapped continuation of the entry above it. '
                            'Check it against the extract.')
        if r.get('_n_ids', 0) > 1:
            warnings.append(f'{r["section"]} row "{r["name"]}" holds more than one id; only the first '
                            'was recorded. Split it by hand.')
        if r['section'] == 'mortgage' and 'דרגה' not in r['detail']:
            warnings.append(f'mortgage row "{r["name"]}" has no degree: it may be a joint creditor '
                            'of the mortgage above it, or its degree was not read. Check it.')
        if r['section'] == 'owner' and not r['share'] and not r['owner_id']:
            warnings.append(f'owner row "{r["name"]}" has neither a share nor an id: it may be a '
                            'misfiled line from another section. Check it.')
    return rows, warnings


def valid_israeli_id(id_number):
    """Israeli ID check digit: weights 1,2,1,2..., digit-sum each product, total % 10 == 0."""
    if not id_number.isdigit() or len(id_number) > 9:
        return False
    id_number = id_number.zfill(9)
    total = 0
    for i, ch in enumerate(id_number):
        val = int(ch) * (i % 2 + 1)
        total += val - 9 if val > 9 else val
    return total % 10 == 0


def rows_to_csv(rows):
    buf = io.StringIO()
    fields = ['section', 'gush', 'helka', 'tat_helka', 'name', 'owner_id', 'share', 'detail']
    writer = csv.DictWriter(buf, fieldnames=fields)
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r.get(k, '') for k in fields})
    return '﻿' + buf.getvalue()


def check_shares_sum_to_whole(rows):
    """Owner shares must sum to exactly 1 (בשלמות). Exact fractions, no tolerance."""
    total = Fraction(0)
    saw_fraction = False
    unparsed = 0
    missing = 0
    for r in rows:
        if r['section'] != 'owner':
            continue
        s = r.get('share', '')
        if s == 'בשלמות':
            total += 1
            saw_fraction = True
        elif '/' in s:
            try:
                num, den = s.split('/')
                total += Fraction(int(num.strip()), int(den.strip()))
                saw_fraction = True
            except (ValueError, ZeroDivisionError):
                unparsed += 1
        elif s:
            unparsed += 1
        else:
            missing += 1
    out = []
    if saw_fraction and total != 1:
        out.append(f'Owner shares sum to {total} ({float(total):.4f}), not 1 (בשלמות). An owner row '
                   'was probably missed by OCR, or this is a historical/concentrated Nesach. Flag '
                   'for human review.')
    if unparsed:
        out.append(f'{unparsed} owner row(s) had a share the script could not parse; they are '
                   'excluded from the sum above. Check them by hand.')
    if missing:
        out.append(f'{missing} owner row(s) have no share at all; the sum check cannot cover them.')
    return out


EXAMPLE_TEXT = """לשכת רישום המקרקעין
גוש 6941 חלקה 55 תת-חלקה 12
בעלויות
מכר 12345/2015/1 דנה כהן ת.ז. 000000018 חלק 1/2
יוסי לוי
ת"ז 000000026 חלק 1/2
משכנתאות
משכנתא דרגה ראשונה
בנק למשכנתאות בעמ ח.פ. 512345678
עיקולים
עיקול לטובת הוצאה לפועל סעיף 34
צווים
צו הריסה לטובת הועדה המקומית סעיף 212
הערות
הערת אזהרה לטובת רוכש סעיף 126
חכירות
עיריית תל אביב עד 31/12/2050
"""


def main():
    ap = argparse.ArgumentParser(description='Nesach Tabu -> normalized spreadsheet')
    src = ap.add_mutually_exclusive_group()
    src.add_argument('--file', help='Path to a text file of OCR output from a Nesach')
    src.add_argument('--json', help='extract_form_fields.py JSON output (needs raw_text; run it with --raw-text)')
    src.add_argument('--example', action='store_true', help='Run on a bundled sample')
    ap.add_argument('--out', help='Write CSV here instead of stdout')
    args = ap.parse_args()

    if args.example:
        text = EXAMPLE_TEXT
    elif args.file:
        with open(args.file, encoding='utf-8') as fh:
            text = fh.read()
    elif args.json:
        try:
            with open(args.json, encoding='utf-8') as fh:
                data = json.load(fh)
        except (OSError, ValueError) as exc:
            print(f'Could not read {args.json} as JSON: {exc}', file=sys.stderr)
            return 2
        text = data.get('raw_text') or data.get('text') or ''
        if not text:
            print('JSON has no raw_text field. Re-run extract_form_fields.py with --raw-text, '
                  'or pass the OCR text via --file.', file=sys.stderr)
            return 2
    else:
        ap.print_help()
        return 1

    rows, warnings = parse_nesach(text)
    # The notice travels inside the file, so a forwarded sheet still says what it is.
    rows.append({'section': 'notice', 'gush': '', 'helka': '', 'tat_helka': '', 'owner_id': '',
                 'share': '', 'detail': '',
                 'name': 'Unofficial OCR transcription, not the registry record / תעתיק OCR לא רשמי, לא הנסח הרשמי'})
    csv_text = rows_to_csv(rows)
    warnings += check_shares_sum_to_whole(rows)

    if args.out:
        with open(args.out, 'w', encoding='utf-8', newline='') as fh:
            fh.write(csv_text)
        print(f'Wrote {len(rows)} rows to {args.out}')
    else:
        sys.stdout.write(csv_text)
    for w in warnings:
        print(f'\nWARNING: {w}', file=sys.stderr)
    print('\nNOTE: this sheet is an unofficial OCR transcription of the Nesach, not the registry '
          'record. It gives no opinion on what any entry means for a transaction.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
