#!/usr/bin/env python3
"""Generate Hebrew PDF documents with RTL support using reportlab.

Produces sample Israeli business documents (tax invoice, receipt) with
proper Hebrew typography, right-to-left text layout, and VAT calculations.
The sample data is illustrative; replace it with real business details.

Usage:
    python generate_doc.py --type invoice --output invoice.pdf
    python generate_doc.py --type receipt --output receipt.pdf --font Heebo-Regular.ttf
    python generate_doc.py --help

Without --font the script looks for a Hebrew-capable TTF in common system
locations and exits with an error if none is found. It never falls back to
Helvetica, which has no Hebrew glyphs and silently prints empty boxes.

Requirements:
    pip install reportlab python-bidi
"""

import argparse
import os
import sys
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import mm
    from reportlab.lib import colors
except ImportError:
    print("Missing required dependency. Install with:", file=sys.stderr)
    print("  pip install reportlab", file=sys.stderr)
    sys.exit(1)

try:
    # Use the pure-Python implementation. In python-bidi 0.5+ the top-level
    # `from bidi import get_display` wraps the Rust unicode-bidi crate, which
    # does not mirror brackets (rule L4, upstream issue #25), so "(18%)"
    # renders as ")18%(" in a reportlab PDF. bidi.algorithm still ships in
    # 0.6.x and mirrors correctly.
    from bidi.algorithm import get_display
except ImportError:
    print("Missing required dependency. Install with:", file=sys.stderr)
    print("  pip install python-bidi  # 0.6.x, requires Python 3.9+", file=sys.stderr)
    sys.exit(1)


# Israeli VAT rate
VAT_RATE = 0.18

# Candidate Hebrew-capable TTF files, checked in order when --font is omitted.
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf",
    "/usr/share/fonts/noto/NotoSansHebrew-Regular.ttf",
    "/usr/share/fonts/truetype/culmus/DavidCLM-Medium.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\david.ttf",
]


def register_hebrew_font(font_path, font_name="HebrewFont"):
    """Register a TTF font with reportlab and confirm it has Hebrew glyphs.

    Returns the registered font name, or None if the file cannot be loaded
    or does not contain the Hebrew letter alef.
    """
    try:
        font = TTFont(font_name, font_path)
    except Exception as e:
        print(f"Warning: could not load font {font_path}: {e}", file=sys.stderr)
        return None
    if ord("א") not in font.face.charToGlyph:
        print(f"Warning: {font_path} has no Hebrew glyphs", file=sys.stderr)
        return None
    pdfmetrics.registerFont(font)
    return font_name


def find_hebrew_font():
    """Return the first registered Hebrew-capable candidate font, or None."""
    for path in FONT_CANDIDATES:
        if os.path.isfile(path):
            name = register_hebrew_font(path)
            if name:
                print(f"Using font: {path}", file=sys.stderr)
                return name
    return None


def hebrew_text(text):
    """Reorder a logical Hebrew/mixed string into visual order for reportlab."""
    return get_display(text)


def draw_hebrew_line(c, x, y, text, font_name, font_size):
    """Draw a right-aligned Hebrew text line whose right edge is at x."""
    c.setFont(font_name, font_size)
    c.drawRightString(x, y, hebrew_text(text))


def wrap_hebrew_lines(text, font_name, font_size, max_width):
    """Wrap a logical-order string into lines that fit max_width points.

    Wrap BEFORE reordering: reportlab's Paragraph wraps the visual string it
    is given, so feeding it get_display() output puts the last sentence on the
    top line. Break the logical text into words, fill each line, and only then
    run get_display() on each finished line.
    """
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and pdfmetrics.stringWidth(candidate, font_name, font_size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_hebrew_paragraph(c, x, y, text, font_name, font_size, max_width,
                          leading=None):
    """Draw a wrapped, right-aligned Hebrew paragraph whose right edge is at x.
    Returns the y coordinate below the last line."""
    leading = leading or font_size * 1.5
    c.setFont(font_name, font_size)
    for line in wrap_hebrew_lines(text, font_name, font_size, max_width):
        c.drawRightString(x, y, hebrew_text(line))
        y -= leading
    return y


def generate_invoice(filename, font_name, business_info=None):
    """Generate a sample Hebrew tax invoice (Heshbonit Mas)."""
    if business_info is None:
        business_info = {
            "name": "חברת דוגמה בע\"מ",
            "address": "רחוב הרצל 1, תל אביב",
            "osek_number": "512345678",
            "invoice_number": "1001",
            "customer_name": "לקוח לדוגמה בע\"מ",
            "customer_id": "515555555",
            # Israel Invoices model: a tax invoice at/above the Tax Authority
            # threshold needs an allocation number, or the buyer cannot deduct
            # the input VAT. Fill in the number the Tax Authority issued.
            "allocation_number": "__________",
        }

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    right_margin = width - 20 * mm
    left_margin = 20 * mm

    # Header. The words "חשבונית מס" and "עוסק מורשה" are required on the
    # document; "מקור" marks the original handed to the customer.
    draw_hebrew_line(c, right_margin, height - 25 * mm,
                     "חשבונית מס", font_name, 22)
    c.setFont(font_name, 12)
    c.drawString(left_margin, height - 25 * mm, hebrew_text("מקור"))
    draw_hebrew_line(c, right_margin, height - 35 * mm,
                     business_info["name"], font_name, 14)
    draw_hebrew_line(c, right_margin, height - 42 * mm,
                     business_info["address"], font_name, 10)
    draw_hebrew_line(c, right_margin, height - 49 * mm,
                     f"עוסק מורשה {business_info['osek_number']}",
                     font_name, 10)

    # Invoice details
    today = datetime.now().strftime("%d/%m/%Y")
    draw_hebrew_line(c, right_margin, height - 60 * mm,
                     f"חשבונית מס מספר {business_info['invoice_number']}",
                     font_name, 11)
    draw_hebrew_line(c, right_margin, height - 67 * mm,
                     f"תאריך: {today}", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 74 * mm,
                     f"לכבוד: {business_info['customer_name']}, "
                     f"ח.פ. {business_info['customer_id']}",
                     font_name, 11)
    draw_hebrew_line(c, right_margin, height - 81 * mm,
                     f"מספר הקצאה: {business_info['allocation_number']}",
                     font_name, 11)

    # Separator line
    c.setStrokeColor(colors.black)
    c.line(left_margin, height - 87 * mm, right_margin, height - 87 * mm)

    # Sample line items
    items = [
        ("שירותי ייעוץ - חודש ינואר", 1, 5000.00),
        ("פיתוח תוכנה - שלב א׳", 1, 12000.00),
        ("תחזוקה שוטפת (3 חודשים)", 3, 800.00),
    ]

    # Table header
    y = height - 96 * mm
    c.setFont(font_name, 10)
    c.drawRightString(right_margin, y, hebrew_text("תיאור"))
    c.drawString(left_margin + 80 * mm, y, hebrew_text("כמות"))
    c.drawString(left_margin + 50 * mm, y, hebrew_text("מחיר"))
    c.drawString(left_margin, y, hebrew_text("סה\"כ"))

    c.line(left_margin, y - 2 * mm, right_margin, y - 2 * mm)

    # Table rows
    y -= 9 * mm
    subtotal = 0.0
    for desc, qty, price in items:
        total = qty * price
        subtotal += total
        c.drawRightString(right_margin, y, hebrew_text(desc))
        c.drawString(left_margin + 80 * mm, y, str(qty))
        c.drawString(left_margin + 50 * mm, y, f"{price:,.2f}")
        c.drawString(left_margin, y, f"{total:,.2f}")
        y -= 7 * mm

    # Totals
    c.line(left_margin, y, right_margin, y)
    y -= 8 * mm
    vat = round(subtotal * VAT_RATE, 2)
    grand_total = subtotal + vat

    draw_hebrew_line(c, left_margin + 60 * mm, y,
                     f"סכום ביניים: {subtotal:,.2f} ש\"ח",
                     font_name, 11)
    y -= 7 * mm
    draw_hebrew_line(c, left_margin + 60 * mm, y,
                     f"מע\"מ ({VAT_RATE:.0%}): {vat:,.2f} ש\"ח",
                     font_name, 11)
    y -= 7 * mm
    draw_hebrew_line(c, left_margin + 60 * mm, y,
                     f"סה\"כ לתשלום: {grand_total:,.2f} ש\"ח",
                     font_name, 13)

    # Wrapped notes paragraph (drawRightString alone never wraps)
    y -= 14 * mm
    y = draw_hebrew_paragraph(
        c, right_margin, y,
        "הערות: התשלום יבוצע בהעברה בנקאית תוך 30 יום ממועד החשבונית "
        "(שוטף + 30). מסמך זה הוא דוגמת עימוד בלבד. חשבונית מס מופקת בפועל "
        "מתוכנה מורשית, במקור ובהעתק, עם מספר הקצאה כשהוא נדרש.",
        font_name, 10, right_margin - left_margin)
    y -= 6 * mm
    draw_hebrew_line(c, right_margin, y, "חתימה: ____________________",
                     font_name, 11)

    c.save()
    print(f"Generated invoice: {filename}")


def generate_receipt(filename, font_name):
    """Generate a sample Hebrew receipt (Kabala)."""
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    right_margin = width - 20 * mm

    draw_hebrew_line(c, right_margin, height - 25 * mm,
                     "קבלה", font_name, 22)
    draw_hebrew_line(c, right_margin, height - 40 * mm,
                     "חברת דוגמה בע\"מ", font_name, 14)
    draw_hebrew_line(c, right_margin, height - 47 * mm,
                     "עוסק מורשה 512345678", font_name, 10)

    today = datetime.now().strftime("%d/%m/%Y")
    draw_hebrew_line(c, right_margin, height - 55 * mm,
                     f"תאריך: {today}", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 62 * mm,
                     "קבלה מספר 5001", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 69 * mm,
                     "התקבל מאת: לקוח לדוגמה בע\"מ", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 79 * mm,
                     "התקבל סך: 22,892.00 ש\"ח (עבור חשבונית מס 1001)",
                     font_name, 13)
    draw_hebrew_line(c, right_margin, height - 87 * mm,
                     "אמצעי תשלום: העברה בנקאית", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 100 * mm,
                     "מסמך זה הוא דוגמת עימוד בלבד ואינו קבלה שהופקה.",
                     font_name, 10)

    c.save()
    print(f"Generated receipt: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Hebrew PDF documents with RTL support"
    )
    parser.add_argument(
        "--type", choices=["invoice", "receipt"], default="invoice",
        help="Document type to generate (default: invoice)"
    )
    parser.add_argument(
        "--output", default="output.pdf",
        help="Output PDF file path (default: output.pdf)"
    )
    parser.add_argument(
        "--font", default=None,
        help="Path to a Hebrew TTF font file (default: auto-detect a "
             "Hebrew-capable system font)"
    )
    args = parser.parse_args()

    if args.font:
        font_name = register_hebrew_font(args.font)
    else:
        font_name = find_hebrew_font()
    if not font_name:
        print("Error: no Hebrew-capable TTF font available. Pass --font with "
              "a Hebrew TTF (for example Heebo-Regular.ttf from Google Fonts).",
              file=sys.stderr)
        sys.exit(2)

    if args.type == "invoice":
        generate_invoice(args.output, font_name)
    elif args.type == "receipt":
        generate_receipt(args.output, font_name)


if __name__ == "__main__":
    main()
