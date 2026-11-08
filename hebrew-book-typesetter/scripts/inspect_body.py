#!/usr/bin/env python3
"""Inspect a pandoc-generated body.typ before typesetting, and optionally fix it.

Word manuscripts often fake headings with bold text instead of using Word's
heading styles. pandoc only turns real heading styles into Typst headings, so a
book with fake headings comes out with no chapters, no table of contents and no
running heads. This script reports what pandoc found and can promote short,
fully-bold paragraphs to headings.

    python3 inspect_body.py body.typ                  # report only
    python3 inspect_body.py body.typ --fix-quotes     # רש"י -> רש״י, ד' -> ד׳
    python3 inspect_body.py body.typ --promote 1      # bold-only lines become level-1 headings
    python3 inspect_body.py body.typ --promote 1 --match '^פרק' --out step1.typ
    python3 inspect_body.py step1.typ --promote 2 --out body.fixed.typ

Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

HEB = "\u05d0-\u05ea"
MARKS = "\u0591-\u05c7"  # nikkud and teamim that may sit on a letter
DQ = r'(?:\\"|["\u201c\u201d\u05f4])'
SQ = r"(?:\\'|['\u2018\u2019])"
# Gershayim: a double quote before the LAST letter of a Hebrew word (רש"י, הרמב"ם, רַשִׁ"י).
# A quote that opens a quotation after a prefix letter (ו"שלום") is followed by several
# letters, so it is left alone.
GERSHAYIM = re.compile(r"(?<=[%s])([%s]*)%s(?=[%s][%s]*(?![%s]))" % (HEB, MARKS, DQ, HEB, MARKS, HEB))
GERSHAYIM_FIND = re.compile(r"[%s][%s]*%s[%s][%s]*(?![%s])" % (HEB, MARKS, DQ, HEB, MARKS, HEB))
# Geresh candidate: a single quote right after a Hebrew letter (with any marks) that ends the word.
GERESH_CAND = re.compile(r"(?<=[%s])([%s]*)%s(?![%s])" % (HEB, MARKS, SQ, HEB))
# An opening single quote: at line start, after a space or bracket, or after a one-letter prefix
# (ב'שלום'), followed by a Hebrew letter.
SQ_OPEN = re.compile(r"(?:^|(?<=[\s(\[])|(?<=[\s(\[][ובכלמשה])|(?<=^[ובכלמשה]))%s(?=[%s])" % (SQ, HEB))
TEAMIM = re.compile("[\u0591-\u05af]")
METEG = "\u05bd"

STRONG_ONLY = re.compile(r"^#strong\[(?P<t>[^\]\n]{1,80})\]\s*$")


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def report(text):
    lines = text.splitlines()
    h1 = sum(1 for l in lines if re.match(r"^= ", l))
    h2 = sum(1 for l in lines if re.match(r"^== ", l))
    h3 = sum(1 for l in lines if re.match(r"^={3,} ", l))
    foot = text.count("#footnote[")
    imgs = text.count("#image(")
    tables = text.count("#table(")
    fake = [p.strip() for p in paragraphs(text) if STRONG_ONLY.match(p.strip())]
    words = len(re.findall(r"\w+", text))
    g2 = len(GERSHAYIM_FIND.findall(text))
    g1 = sum(len(geresh_positions(line)) for line in text.splitlines())
    teamim = len(TEAMIM.findall(text))
    meteg = text.count(METEG)
    print(f"words (approx)        : {words}")
    print(f"level-1 headings (=)  : {h1}")
    print(f"level-2 headings (==) : {h2}")
    print(f"deeper headings       : {h3}")
    print(f"footnotes             : {foot}")
    print(f"images                : {imgs}")
    print(f"tables                : {tables}")
    print(f"quote marks to convert: {g2} gershayim, {g1} geresh  (fix with --fix-quotes)")
    print(f"cantillation marks    : {teamim}, meteg: {meteg}")
    print(f"bold-only short lines : {len(fake)}  (likely headings typed as bold text)")
    for f in fake[:10]:
        print("   ", STRONG_ONLY.match(f).group("t"))
    if h1 == 0 and fake:
        print("\nNo real chapters found. Re-run with --promote 1 (or fix the Word styles and re-export).")
    if teamim:
        print("\nCantillation marks found: pass --teamim-font with a font that has them (e.g. 'Ezra SIL').")
        print("Never rely on automatic font fallback for them: it can duplicate letters inside the word.")
    if meteg:
        print("Meteg found: use a body font that has it (Frank Ruhl Libre does, David Libre does not).")
    if imgs:
        print("\nImages found: pandoc extracts them only with --extract-media=media; check they are 300 dpi or more.")
    return fake


def geresh_positions(line):
    """Indexes of single quotes that are a geresh, skipping the closing quote of a
    single-quoted phrase ('לא', 'על הגאולה'): a candidate that follows an unclosed
    opening quote on the same line closes it instead."""
    events = [(m.start(), "open") for m in SQ_OPEN.finditer(line)]
    events += [(m.end(1), "cand") for m in GERESH_CAND.finditer(line)]
    out, is_open = [], False
    for pos, kind in sorted(events):
        if kind == "open":
            is_open = True
        elif is_open:
            is_open = False  # closing quote of a quotation, not a geresh
        else:
            out.append(pos)
    return out


def fix_line(line):
    line = GERSHAYIM.sub(lambda m: m.group(1) + "\u05f4", line)
    pos = geresh_positions(line)
    for p in reversed(pos):
        q = 2 if line.startswith("\\'", p) else 1
        line = line[:p] + "\u05f3" + line[p + q:]
    return line


def fix_quotes(text):
    return "\n".join(fix_line(l) for l in text.split("\n"))


def promote(text, level, match=None):
    marks = "=" * level
    pat = re.compile(match) if match else None
    out = []
    for p in re.split(r"(\n\s*\n)", text):
        m = STRONG_ONLY.match(p.strip())
        if m and (pat is None or pat.search(m.group("t"))):
            out.append(f"{marks} {m.group('t').strip()}")
        else:
            out.append(p)
    return "".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("body")
    ap.add_argument("--promote", type=int, choices=[1, 2, 3], help="turn bold-only short lines into headings of this level")
    ap.add_argument("--match", help="only promote lines matching this regex, e.g. '^פרק' for chapters")
    ap.add_argument("--fix-quotes", action="store_true",
                    help="convert quotes inside Hebrew abbreviations to real gershayim and geresh")
    ap.add_argument("--out", help="write the fixed file here (default: overwrite the input)")
    a = ap.parse_args(argv)
    path = Path(a.body)
    if not path.exists():
        sys.exit(f"not found: {path}")
    text = path.read_text(encoding="utf-8")
    report(text)
    fixed = text
    if a.fix_quotes:
        fixed = fix_quotes(fixed)
    if a.promote:
        fixed = promote(fixed, a.promote, a.match)
    if fixed != text:
        target = Path(a.out) if a.out else path
        target.write_text(fixed, encoding="utf-8")
        what = []
        if a.fix_quotes:
            what.append("gershayim and geresh fixed")
        if a.promote:
            what.append(f"bold-only lines promoted to level-{a.promote} headings")
        print("\n" + ", ".join(what) + f" -> {target}")


if __name__ == "__main__":
    main()
