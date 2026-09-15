#!/usr/bin/env python3
"""Preprocess Hebrew text for NLP pipelines.

Provides utilities for normalizing Hebrew text before feeding it to models
like DictaBERT, DictaLM, or AlephBERT. Handles Unicode normalization,
niqqud (diacritics) removal, whitespace cleanup, and optional English
token handling.

Usage:
    python preprocess_hebrew.py "שלום עולם"
    python preprocess_hebrew.py --file input.txt --output cleaned.txt
    echo "טקסט עם ניקוד" | python preprocess_hebrew.py --stdin

Requirements:
    No external dependencies (uses only Python standard library).
"""

import argparse
import re
import sys
import unicodedata


def preprocess_hebrew(text, remove_niqqud=True, normalize_whitespace=True,
                      remove_punctuation=False):
    """Preprocess Hebrew text for NLP model input.

    Args:
        text: Input Hebrew text string.
        remove_niqqud: Remove Hebrew diacritics/vowel marks (default: True).
        normalize_whitespace: Collapse multiple spaces (default: True).
        remove_punctuation: Remove all punctuation marks (default: False).

    Returns:
        Cleaned Hebrew text string.
    """
    # Step 1: Unicode NFC normalization
    text = unicodedata.normalize('NFC', text)

    # Step 2: Remove niqqud and cantillation marks. The U+0591-U+05C7 block
    # also holds punctuation, so skip maqaf U+05BE, paseq U+05C0,
    # sof pasuq U+05C3 and nun hafukha U+05C6 instead of stripping the range.
    if remove_niqqud:
        text = re.sub(r'[\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]', '', text)

    # Step 3: Remove biblical punctuation (paseq U+05C0, sof pasuq U+05C3).
    # Maqaf (Hebrew hyphen) U+05BE is kept, it joins words.
    text = re.sub(r'[\u05C0\u05C3]', '', text)

    # Step 4: Geresh (U+05F3) and gershayim (U+05F4) carry meaning in
    # abbreviations (צה״ל) and are kept as they are.

    # Step 5: Optionally remove punctuation
    if remove_punctuation:
        # Most text types an ASCII " inside acronyms (צה"ל, מע"מ). Convert it to
        # gershayim only in the acronym shape: two or more Hebrew letters, the
        # quote, then exactly one final Hebrew letter. A quoted word such as
        # "כן" does not match. ASCII ' is never converted, because a closing
        # single quote after a Hebrew word looks the same as a geresh.
        text = re.sub(
            r'(?<=[א-ת]{2})"(?=[א-ת](?![א-ת]))',
            '״',
            text,
        )
        # Keep Hebrew letters, digits, spaces, geresh/gershayim and the shekel
        # sign. Removed marks become a space so hyphenated tokens do not fuse.
        text = re.sub(r'[^֐-׿׳״₪\w\s]', ' ', text)

    # Step 6: Normalize whitespace
    if normalize_whitespace:
        text = re.sub(r'\s+', ' ', text).strip()

    return text


def detect_hebrew_ratio(text):
    """Calculate the ratio of Hebrew characters in the text.

    Args:
        text: Input text string.

    Returns:
        Float between 0 and 1 representing the Hebrew character ratio.
    """
    if not text:
        return 0.0

    total_alpha = 0
    hebrew_chars = 0
    for char in text:
        if char.isalpha() or ('\u0590' <= char <= '\u05FF'):
            total_alpha += 1
            if '\u0590' <= char <= '\u05FF':
                hebrew_chars += 1

    return hebrew_chars / total_alpha if total_alpha > 0 else 0.0


def segment_mixed_text(text):
    """Segment text into Hebrew and non-Hebrew segments.

    Useful for processing mixed Hebrew-English text where each language
    needs different handling.

    Args:
        text: Input mixed-language text.

    Returns:
        List of tuples (segment_text, language) where language is
        'hebrew' or 'other'.
    """
    segments = []
    current_segment = []
    current_lang = None

    for char in text:
        if '\u0590' <= char <= '\u05FF':
            char_lang = 'hebrew'
        elif char.isspace():
            char_lang = current_lang  # Spaces belong to current segment
        else:
            char_lang = 'other'

        if char_lang != current_lang and current_lang is not None:
            segment_text = ''.join(current_segment).strip()
            if segment_text:
                segments.append((segment_text, current_lang))
            current_segment = []

        current_lang = char_lang
        current_segment.append(char)

    # Don't forget the last segment
    if current_segment:
        segment_text = ''.join(current_segment).strip()
        if segment_text:
            segments.append((segment_text, current_lang))

    return segments


def remove_urls(text):
    """Remove URLs from Hebrew text.

    Args:
        text: Input text that may contain URLs.

    Returns:
        Text with URLs removed.
    """
    return re.sub(r'https?://\S+', '', text)


def normalize_numbers(text):
    """Normalize number formats in Hebrew text.

    Standardizes comma-separated numbers and currency symbols.

    Args:
        text: Input text with numbers.

    Returns:
        Text with normalized number formats.
    """
    # Remove thousands separators only (1,000,000 -> 1000000). A comma followed
    # by anything other than exactly three digits (3,5 or 1,2,3) is left alone.
    text = re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', text)
    # Normalize the shekel abbreviation only when it carries gershayim U+05F4
    # or an ASCII double quote. The bare form is skipped because שח is also
    # an ordinary word (הוא שח, שח מט). One attached prefix letter
    # (בש"ח, לש"ח) is allowed and kept.
    text = re.sub(
        r'(?<![א-ת])([בוכלמהש]?)ש[״"]ח(?![א-ת])',
        r'\1₪',
        text,
    )
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess Hebrew text for NLP pipelines"
    )
    parser.add_argument(
        "text", nargs="?",
        help="Hebrew text to preprocess (or use --file/--stdin)"
    )
    parser.add_argument(
        "--file", "-f",
        help="Input file path"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--stdin", action="store_true",
        help="Read from stdin"
    )
    parser.add_argument(
        "--keep-niqqud", action="store_true",
        help="Keep niqqud (diacritics) in text"
    )
    parser.add_argument(
        "--remove-punctuation", action="store_true",
        help="Remove all punctuation"
    )
    parser.add_argument(
        "--remove-urls", action="store_true",
        help="Remove URLs from text"
    )
    parser.add_argument(
        "--normalize-numbers", action="store_true",
        help="Normalize number formats"
    )
    parser.add_argument(
        "--detect-language", action="store_true",
        help="Print Hebrew character ratio"
    )
    parser.add_argument(
        "--segment", action="store_true",
        help="Segment text into Hebrew and non-Hebrew parts"
    )
    args = parser.parse_args()

    # Get input text
    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)

    # Detect language ratio if requested
    if args.detect_language:
        ratio = detect_hebrew_ratio(text)
        print(f"Hebrew character ratio: {ratio:.2%}")
        if ratio > 0.5:
            print("Text is primarily Hebrew")
        else:
            print("Text is primarily non-Hebrew")
        return

    # Segment if requested
    if args.segment:
        segments = segment_mixed_text(text)
        for seg_text, lang in segments:
            print(f"[{lang}] {seg_text}")
        return

    # Preprocess
    if args.remove_urls:
        text = remove_urls(text)
    if args.normalize_numbers:
        text = normalize_numbers(text)

    result = preprocess_hebrew(
        text,
        remove_niqqud=not args.keep_niqqud,
        remove_punctuation=args.remove_punctuation
    )

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
