#!/usr/bin/env python3
"""Compute spine width and the full cover sheet size for a paperback.

Spine width = number of leaves x paper thickness, where a leaf is two pages.
The paper thickness (caliper) comes from the print shop, because it depends on
the paper they will actually use. Do not guess it.

A Hebrew book binds on the RIGHT: held closed with the front cover facing you,
the spine is on your right. Laid flat (outside facing you), the FRONT cover is
therefore the LEFT-hand panel and the back cover is the right-hand panel, the
reverse of an English book.

Example:
    python3 cover_size.py --pages 212 --caliper 0.1 --trim 140x210 --bleed 3
Stdlib only.
"""
import argparse
import math
import re


def parse_trim(v):
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*[x*]\s*(\d+(?:\.\d+)?)\s*", v.lower())
    if not m:
        raise argparse.ArgumentTypeError("trim must be WIDTHxHEIGHT in mm, e.g. 140x210")
    return float(m.group(1)), float(m.group(2))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pages", type=int, required=True, help="interior page count, including blanks")
    p.add_argument("--caliper", type=float, required=True,
                   help="thickness of ONE leaf (sheet) of the interior paper in mm, from the print shop")
    p.add_argument("--trim", type=parse_trim, required=True, help="WIDTHxHEIGHT in mm")
    p.add_argument("--bleed", type=float, default=0.0, help="cover bleed per side in mm, from the print shop")
    p.add_argument("--cover-board", type=float, default=0.0,
                   help="extra mm to add to the spine as the print shop specifies (for a hardcover, get the binder's layout instead)")
    p.add_argument("--multiple", type=int, default=0,
                   help="if the shop prints in signatures, round pages up to this multiple (e.g. 4, 8, 16)")
    a = p.parse_args(argv)
    if a.pages <= 0 or a.caliper <= 0 or a.caliper > 1:
        p.error("pages must be positive and caliper is per leaf in mm (a fraction of a millimetre)")
    pages = a.pages
    if pages % 2:
        pages += 1
        print(f"note: a book has an even number of pages; using {pages} (one blank page added)")
    if a.multiple:
        pages = int(math.ceil(pages / a.multiple) * a.multiple)
    leaves = pages / 2
    spine = leaves * a.caliper + a.cover_board
    w, h = a.trim
    sheet_w = 2 * w + spine + 2 * a.bleed
    sheet_h = h + 2 * a.bleed
    print(f"pages used for spine : {pages}" + (f" (rounded up from {a.pages}; pad the interior PDF to match)" if pages != a.pages else ""))
    print(f"leaves               : {leaves:g}")
    print(f"spine width          : {spine:.1f} mm")
    print(f"cover sheet          : {sheet_w:.1f} x {sheet_h:.1f} mm (including bleed)")
    print("layout, left to right: [FRONT cover] [spine] [back cover]  (Hebrew book, bound on the right)")
    print(f"  front panel x = {a.bleed:.1f} .. {a.bleed + w:.1f} mm")
    print(f"  spine       x = {a.bleed + w:.1f} .. {a.bleed + w + spine:.1f} mm")
    print(f"  back panel  x = {a.bleed + w + spine:.1f} .. {a.bleed + 2 * w + spine:.1f} mm")
    if spine < 5:
        print("note: a spine this thin usually cannot carry readable text; ask the print shop.")


if __name__ == "__main__":
    main()
