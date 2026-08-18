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
noisy, so the script is loud about what it could not place: it emits any line it cannot
assign to a known section as a `section=unrecognized` row (never silently dropped) and
prints warnings to stderr for unrecognized section headers, a concentrated/historical
Nesach, and owner shares that do not sum to the whole. Always read the warnings.

It writes UTF-8 with a BOM so Excel opens Hebrew columns right-to-left. It keeps the
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

GUSH_RE = re.compile(r'גוש[:\s]*(\d+)')
# Match תת-חלקה FIRST and remove it, so the plain-חלקה match cannot pick up the digits
# that belong to the sub-parcel (the "חלקה" inside "תת-חלקה").
TAT_HELKA_RE = re.compile(r'תת[\s-]*חלקה[:\s]*(\d+)')
HELKA_RE = re.compile(r'חלקה[:\s]*(\d+)')
# Owner id: a personal ת.ז., a company ח.פ. / תאגיד number, or a passport. All 5-9 digits.
ID_RE = re.compile(r'(?:ת\.?ז\.?|ח\.?פ\.?|מספר זהות|מספר תאגיד|דרכון)[:\s]*([A-Z]?\d{5,9})')
SHARE_RE = re.compile(r'(\d{1,7}\s*/\s*\d{1,7}|בשלמות)')
DEGREE_RE = re.compile(r'דרגה\s+(\S+)')
BENEFICIARY_RE = re.compile(r'לטובת\s+(.+)')
SECTION_REF_RE = re.compile(r'סעיף\s+\d+[א-ת]?')
DATE_RE = re.compile(r'\d{1,2}[./]\d{1,2}[./]\d{2,4}')

NIKUD_RE = re.compile(r'[֑-ׇ]')
SOFIT_MAP = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}

# Section header keywords -> canonical section name. Order matters: the most specific
# encumbrance keywords come before the generic "note" so a compound header like
# "הערות אזהרה ועיקולים" is classified by its strongest signal.
SECTION_MARKERS = [
    (re.compile(r'בעלו?יו?ת|בעלות'), 'owner'),
    (re.compile(r'חכיר'), 'lease'),
    (re.compile(r'משכנת|שעבוד'), 'mortgage'),
    (re.compile(r'עיקול'), 'lien'),
    (re.compile(r'הפקע'), 'expropriation'),
    (re.compile(r'זיקת|זיקות'), 'easement'),
    (re.compile(r'\bצו\b|צווים|צו\s'), 'order'),
    (re.compile(r'הער'), 'caution'),
]
# A caution content line usually starts with the caution TYPE, so treat these as content
# markers, not section switches, even when short.
CAUTION_CONTENT_HINT = re.compile(r'הערת אזהרה|לטובת')
# "חלק" here is the share LABEL; the lookahead stops it from eating "חלקה" (parcel).
NAME_LABEL_RE = re.compile(r'(?:ת\.?ז\.?|ח\.?פ\.?|מספר זהות|מספר תאגיד|דרכון|חלק(?=[\s\d/])|דרגה|לטובת|סעיף)')
# Lines that are document furniture, not section content (registry office title etc.).
FURNITURE_RE = re.compile(r'לשכת רישום|פנקס|רשות לרישום')


def strip_key(text):
    """Normalize a string for label/header matching only (never for stored values)."""
    text = NIKUD_RE.sub('', text)
    return ''.join(SOFIT_MAP.get(ch, ch) for ch in text)


def _first(pattern, text):
    m = pattern.search(text)
    return m.group(1).strip() if m else ''


def _share(line):
    """Extract an ownership share, ignoring date spans (31/12/2050 is not 31/12)."""
    return _first(SHARE_RE, DATE_RE.sub(' ', line))


def _classify_header(folded, raw):
    """Return the section name if this folded line is a section HEADER, else None.

    A header matches a section keyword, is short, and carries no id/share/date (those
    belong to content rows). This is deliberately stricter than "contains a keyword" so
    a content line like "הערת אזהרה לטובת רוכש" is NOT eaten as a header, and looser than
    an exact-length match so real headers of a few words still register.
    """
    if len(folded) > 30:
        return None
    if ID_RE.search(folded) or SHARE_RE.search(folded) or DATE_RE.search(folded):
        return None
    if CAUTION_CONTENT_HINT.search(folded):
        return None
    # Match markers against BOTH the raw line and the sofit-folded line. Matching only
    # the folded line would break a plural heading like "צווים": strip_key folds its
    # final ם to מ, so the literal "צווים" would never match and a court-orders section
    # would be silently misfiled. Checking the raw line too covers every sofit form.
    for marker, name in SECTION_MARKERS:
        if marker.search(folded) or marker.search(raw):
            return name
    return None


def _extract_property_key(text):
    key = strip_key(text)
    gush = _first(GUSH_RE, key)
    tat_helka = _first(TAT_HELKA_RE, key)
    # Remove the תת-חלקה span before matching plain חלקה so we do not capture its digits.
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
    if section in ('caution', 'lien', 'order', 'expropriation', 'easement'):
        ben = BENEFICIARY_RE.search(line)
        if ben:
            bits.append('לטובת ' + ben.group(1).strip())
        ref = SECTION_REF_RE.search(line)
        if ref:
            bits.append(ref.group(0))
    if section == 'lease':
        d = DATE_RE.search(line)
        if d:
            bits.append('עד ' + d.group(0))
    return '; '.join(bits)


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

    lines = [l.strip() for l in ocr_text.split('\n') if l.strip()]
    current = None
    seen_before_header = []
    i = 0
    while i < len(lines):
        line = lines[i]
        folded = strip_key(line)
        header = _classify_header(folded, line)
        if header:
            current = header
            i += 1
            continue

        oid = _first(ID_RE, line)
        share = _share(line)
        # Multi-line owner block: a name-only line followed by an id/share-only line.
        if current in ('owner', 'lease') and not oid and not share and i + 1 < len(lines):
            nxt = lines[i + 1]
            if (ID_RE.search(nxt) or _share(nxt)) and not _classify_header(strip_key(nxt), nxt):
                oid = _first(ID_RE, nxt)
                share = _share(nxt)
                line = line + ' ' + nxt
                i += 1  # consume the continuation line

        detail = _build_detail(current or '', line)
        name = NAME_LABEL_RE.sub('', line)
        name = ID_RE.sub('', name)
        name = SHARE_RE.sub('', name)
        name = DATE_RE.sub('', name)
        # Keep Hebrew, spaces, quotes, hyphen, Latin letters and digits (company names).
        name = re.sub(r'[^֐-׿A-Za-z0-9\s"\'\-]', '', name)
        name = ' '.join(name.split())

        if current is None:
            # The property-description line (has גוש) and document furniture (registry
            # title) are expected before the first section; they are already captured in
            # the property key, so do not flag them as unrecognized.
            if GUSH_RE.search(folded) or FURNITURE_RE.search(line):
                i += 1
                continue
            # Do NOT drop anything else: hold it and emit as unrecognized rows + warn.
            if oid or share or name:
                seen_before_header.append(dict(base, section='unrecognized',
                                               name=name, owner_id=oid, share=share, detail=detail))
        elif oid or share or name or detail:
            rows.append(dict(base, section=current, name=name,
                             owner_id=oid, share=share, detail=detail))
        i += 1

    if seen_before_header:
        warnings.append(f'{len(seen_before_header)} content line(s) appeared before any recognized '
                        'section header and were emitted as section=unrecognized. A section title was '
                        'probably garbled by OCR; review them by hand.')
        rows.extend(seen_before_header)
    return rows, warnings


def rows_to_csv(rows):
    buf = io.StringIO()
    fields = ['section', 'gush', 'helka', 'tat_helka', 'name', 'owner_id', 'share', 'detail']
    writer = csv.DictWriter(buf, fieldnames=fields)
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r.get(k, '') for k in fields})
    return '﻿' + buf.getvalue()


def check_shares_sum_to_whole(rows):
    total = 0.0
    saw_fraction = False
    unparsed = 0
    for r in rows:
        if r['section'] != 'owner':
            continue
        s = r.get('share', '')
        if s == 'בשלמות':
            total += 1.0
            saw_fraction = True
        elif '/' in s:
            try:
                num, den = s.split('/')
                total += int(num.strip()) / int(den.strip())
                saw_fraction = True
            except (ValueError, ZeroDivisionError):
                unparsed += 1
        elif s:
            unparsed += 1
    out = []
    if saw_fraction and abs(total - 1.0) > 0.01:
        out.append(f'Owner shares sum to {total:.3f}, not 1 (בשלמות). An owner row was probably '
                   'missed by OCR, or this is a historical/concentrated Nesach. Flag for human review.')
    if unparsed:
        out.append(f'{unparsed} owner row(s) had a share the script could not parse; they are '
                   'excluded from the sum above. Check them by hand.')
    return out


EXAMPLE_TEXT = """לשכת רישום המקרקעין
גוש 6941 חלקה 55 תת-חלקה 12
בעלויות
דנה כהן ת.ז. 012345678 חלק 1/2
יוסי לוי
ת.ז. 087654321 חלק 1/2
משכנתאות
בנק למשכנתאות בעמ ח.פ. 512345678 דרגה ראשונה
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
        with open(args.json, encoding='utf-8') as fh:
            data = json.load(fh)
        text = data.get('raw_text') or data.get('text') or ''
        if not text:
            print('JSON has no raw_text field. Re-run extract_form_fields.py with --raw-text, '
                  'or pass the OCR text via --file.', file=sys.stderr)
            return 2
    else:
        ap.print_help()
        return 1

    rows, warnings = parse_nesach(text)
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
    return 0


if __name__ == '__main__':
    sys.exit(main())
