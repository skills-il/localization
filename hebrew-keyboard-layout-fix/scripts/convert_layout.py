#!/usr/bin/env python3
"""Fix text typed on the wrong keyboard layout (Hebrew <-> English US).

Every word is flipped by physical key position: Hebrew words become English,
English words become Hebrew, so mixed text is fully swapped.

Usage:
    python convert_layout.py "tbh rumv"            # -> אני רוצה
    python convert_layout.py --to he "Tbh rumv"    # force every letter to Hebrew
    echo "יקךךם" | python convert_layout.py         # reads stdin

Pure standard library, no network access.
"""
import argparse
import re
import sys

# Same physical keys, row by row (top, home, bottom) on the US and Hebrew layouts.
EN = "qwertyuiopasdfghjkl;'zxcvbnm,./"
HE = "/'קראטוןםפשדגכעיחלךף,זסבהנמצתץ."

TO_HE = {e: h for e, h in zip(EN, HE)}
TO_EN = {h: e for e, h in zip(EN, HE)}


def is_hebrew_letter(c):
    return "א" <= c <= "ת"


def is_english_letter(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def to_hebrew(c):
    return TO_HE.get(c.lower(), c)


def to_english(c):
    return TO_EN.get(c, c)


def _word_direction(word):
    heb = sum(1 for c in word if is_hebrew_letter(c))
    eng = sum(1 for c in word if is_english_letter(c))
    if heb == 0 and eng == 0:
        return None
    return "en" if heb > eng else "he"


def convert(text, force=None):
    """Flip text typed on the wrong layout.

    force: None (auto, per word), "he" (everything to Hebrew) or "en" (everything to English).
    """
    if force == "he":
        return "".join(to_hebrew(c) for c in text)
    if force == "en":
        return "".join(to_english(c) for c in text)

    # Keep whitespace (spaces, tabs, newlines) exactly as-is between words.
    parts = re.split(r"(\s+)", text)
    directions = [None if (not p or p.isspace()) else _word_direction(p) for p in parts]

    out = []
    prev = None
    for i, part in enumerate(parts):
        if not part or part.isspace():
            out.append(part)
            continue
        d = directions[i]
        if d is None:
            # Punctuation/digits only: follow the previous word, else the next one.
            d = prev or next((x for x in directions[i + 1:] if x), None)
        for c in part:
            if is_hebrew_letter(c):
                out.append(to_english(c))
            elif is_english_letter(c):
                out.append(to_hebrew(c))
            elif d == "en":
                out.append(to_english(c))
            elif d == "he":
                out.append(to_hebrew(c))
            else:
                out.append(c)
        if directions[i]:
            prev = directions[i]
    return "".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fix text typed on the wrong keyboard layout (Hebrew <-> English).")
    parser.add_argument("text", nargs="*", help="text to convert (default: read stdin)")
    parser.add_argument("--to", choices=["he", "en"], help="force the target language for every character")
    args = parser.parse_args(argv)

    text = " ".join(args.text) if args.text else sys.stdin.read().lstrip("\ufeff").rstrip("\n")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(convert(text, args.to))
    return 0


if __name__ == "__main__":
    sys.exit(main())
