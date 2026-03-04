#!/usr/bin/env python3
"""Check Hebrew text for common spelling and style issues.

Scans text for ktiv maleh violations, inconsistent gershayim usage,
and common Hebrew spelling mistakes.

Usage:
    python check_hebrew.py --input text.txt
    python check_hebrew.py --text "הטקסט לבדיקה"
    python check_hebrew.py --help

Requirements:
    Python 3.9+ (no external dependencies)
"""

import argparse
import re
import sys


# Common ktiv maleh corrections (chaser -> maleh)
KTIV_MALEH_FIXES = {
    "תכנה": "תוכנה",
    "שרות": "שירות",
    "תקשרת": "תקשורת",
    "אנטרנט": "אינטרנט",
    "אנפורמציה": "אינפורמציה",
    "תכנון": "תוכנון",
    "תכנית": "תוכנית",
    "חברתי": "חברתי",
    "עדכון": "עידכון",
    "שפור": "שיפור",
    "שקום": "שיקום",
    "תעוד": "תיעוד",
    "קשור": "קישור",
    "סכום": "סיכום",
    "חשוב": "חישוב",
    "נסוי": "ניסוי",
}

# Acronyms that need gershayim
COMMON_ACRONYMS = {
    "צהל": 'צה"ל',
    "שבכ": 'שב"כ',
    "מעמ": 'מע"מ',
    "בגץ": 'בג"ץ',
    "תנך": 'תנ"ך',
    "רמבם": 'רמב"ם',
    "חנל": 'חנ"ל',
}


def check_ktiv_maleh(text):
    """Check for ktiv chaser that should be ktiv maleh."""
    issues = []
    words = re.findall(r'[\u0590-\u05FF]+', text)
    for word in words:
        if word in KTIV_MALEH_FIXES:
            issues.append({
                "type": "ktiv_maleh",
                "original": word,
                "suggestion": KTIV_MALEH_FIXES[word],
                "message": f'כתיב חסר: "{word}" -> "{KTIV_MALEH_FIXES[word]}"'
            })
    return issues


def check_gershayim(text):
    """Check for acronyms missing gershayim."""
    issues = []
    words = re.findall(r'[\u0590-\u05FF]+', text)
    for word in words:
        if word in COMMON_ACRONYMS:
            issues.append({
                "type": "gershayim",
                "original": word,
                "suggestion": COMMON_ACRONYMS[word],
                "message": f'חסר גרשיים: "{word}" -> "{COMMON_ACRONYMS[word]}"'
            })
    return issues


def check_punctuation(text):
    """Check for common Hebrew punctuation issues."""
    issues = []

    # Check for English quotes instead of Hebrew
    if '"' in text and '\u05F4' not in text:
        issues.append({
            "type": "punctuation",
            "message": 'שימוש במירכאות אנגליות במקום גרשיים עבריים (\u05F4)'
        })

    # Check for double spaces
    if "  " in text:
        issues.append({
            "type": "punctuation",
            "message": "נמצאו רווחים כפולים"
        })

    return issues


def analyze_text(text):
    """Run all checks on the given text."""
    all_issues = []
    all_issues.extend(check_ktiv_maleh(text))
    all_issues.extend(check_gershayim(text))
    all_issues.extend(check_punctuation(text))
    return all_issues


def main():
    parser = argparse.ArgumentParser(
        description="Check Hebrew text for common issues"
    )
    parser.add_argument("--input", help="Input text file to check")
    parser.add_argument("--text", help="Direct text to check")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Error: provide --input or --text")
        sys.exit(1)

    issues = analyze_text(text)

    if not issues:
        print("No issues found.")
        return

    print(f"Found {len(issues)} issue(s):\n")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. [{issue['type']}] {issue['message']}")

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
