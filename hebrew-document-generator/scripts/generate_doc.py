#!/usr/bin/env python3
"""Generate Hebrew PDF documents with RTL support using reportlab.

Produces Israeli business documents (invoices, receipts) with proper
Hebrew typography, right-to-left text layout, and VAT calculations.

Usage:
    python generate_doc.py --type invoice --output invoice.pdf
    python generate_doc.py --type receipt --output receipt.pdf --font Heebo-Regular.ttf
    python generate_doc.py --help

Requirements:
    pip install reportlab python-bidi
"""

import argparse
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
    from bidi.algorithm import get_display
except ImportError:
    print("Missing required dependency. Install with:", file=sys.stderr)
    print("  pip install python-bidi", file=sys.stderr)
    sys.exit(1)


# Israeli VAT rate
VAT_RATE = 0.17


def register_hebrew_font(font_path, font_name="HebrewFont"):
    """Register a Hebrew TTF font with reportlab.

    Args:
        font_path: Path to the TTF font file.
        font_name: Name to register the font under.

    Returns:
        The registered font name.
    """
    try:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        return font_name
    except Exception as e:
        print(f"Warning: Could not register font {font_path}: {e}",
              file=sys.stderr)
        print("Falling back to Helvetica (Hebrew may not render correctly)",
              file=sys.stderr)
        return "Helvetica"


def hebrew_text(text):
    """Apply bidi algorithm for correct RTL display.

    Args:
        text: Hebrew text string.

    Returns:
        Display-reordered string for RTL rendering.
    """
    return get_display(text)


def draw_hebrew_line(c, x, y, text, font_name, font_size):
    """Draw a right-aligned Hebrew text line on the canvas.

    Args:
        c: reportlab Canvas object.
        x: Right edge x-coordinate.
        y: y-coordinate.
        text: Hebrew text to draw.
        font_name: Registered font name.
        font_size: Font size in points.
    """
    c.setFont(font_name, font_size)
    c.drawRightString(x, y, hebrew_text(text))


def generate_invoice(filename, font_name, business_info=None):
    """Generate a sample Hebrew tax invoice (Heshbonit Mas).

    Args:
        filename: Output PDF file path.
        font_name: Registered Hebrew font name.
        business_info: Optional dict with business details.
    """
    if business_info is None:
        business_info = {
            "name": "חברת דוגמה בע\"מ",
            "address": "רחוב הרצל 1, תל אביב",
            "osek_number": "123456789",
            "invoice_number": "1001",
        }

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    right_margin = width - 20 * mm
    left_margin = 20 * mm

    # Header
    draw_hebrew_line(c, right_margin, height - 25 * mm,
                     "חשבונית מס", font_name, 22)
    draw_hebrew_line(c, right_margin, height - 35 * mm,
                     business_info["name"], font_name, 14)
    draw_hebrew_line(c, right_margin, height - 42 * mm,
                     business_info["address"], font_name, 10)
    draw_hebrew_line(c, right_margin, height - 49 * mm,
                     f"עוסק מורשה: {business_info['osek_number']}",
                     font_name, 10)

    # Invoice details
    today = datetime.now().strftime("%d/%m/%Y")
    draw_hebrew_line(c, right_margin, height - 60 * mm,
                     f"חשבונית מס׳: {business_info['invoice_number']}",
                     font_name, 11)
    draw_hebrew_line(c, right_margin, height - 67 * mm,
                     f"תאריך: {today}", font_name, 11)

    # Separator line
    c.setStrokeColor(colors.black)
    c.line(left_margin, height - 73 * mm, right_margin, height - 73 * mm)

    # Sample line items
    items = [
        ("שירותי ייעוץ - חודש ינואר", 1, 5000.00),
        ("פיתוח תוכנה - שלב א׳", 1, 12000.00),
        ("תחזוקה שוטפת", 3, 800.00),
    ]

    # Table header
    y = height - 82 * mm
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
    vat = subtotal * VAT_RATE
    grand_total = subtotal + vat

    draw_hebrew_line(c, left_margin + 60 * mm, y,
                     f"סכום ביניים: {subtotal:,.2f} ש\"ח",
                     font_name, 11)
    y -= 7 * mm
    draw_hebrew_line(c, left_margin + 60 * mm, y,
                     f"מע\"מ (17%): {vat:,.2f} ש\"ח",
                     font_name, 11)
    y -= 7 * mm
    draw_hebrew_line(c, left_margin + 60 * mm, y,
                     f"סה\"כ לתשלום: {grand_total:,.2f} ש\"ח",
                     font_name, 13)

    c.save()
    print(f"Generated invoice: {filename}")


def generate_receipt(filename, font_name):
    """Generate a sample Hebrew receipt (Kabala).

    Args:
        filename: Output PDF file path.
        font_name: Registered Hebrew font name.
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    right_margin = width - 20 * mm

    draw_hebrew_line(c, right_margin, height - 25 * mm,
                     "קבלה", font_name, 22)
    draw_hebrew_line(c, right_margin, height - 40 * mm,
                     "חברת דוגמה בע\"מ", font_name, 14)

    today = datetime.now().strftime("%d/%m/%Y")
    draw_hebrew_line(c, right_margin, height - 55 * mm,
                     f"תאריך: {today}", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 62 * mm,
                     "קבלה מס׳: 5001", font_name, 11)
    draw_hebrew_line(c, right_margin, height - 72 * mm,
                     "התקבל סך: 19,890.00 ש\"ח", font_name, 13)
    draw_hebrew_line(c, right_margin, height - 80 * mm,
                     "אמצעי תשלום: העברה בנקאית", font_name, 11)

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
        help="Path to Hebrew TTF font file (optional)"
    )
    args = parser.parse_args()

    font_name = "Helvetica"
    if args.font:
        font_name = register_hebrew_font(args.font)

    if args.type == "invoice":
        generate_invoice(args.output, font_name)
    elif args.type == "receipt":
        generate_receipt(args.output, font_name)


if __name__ == "__main__":
    main()
