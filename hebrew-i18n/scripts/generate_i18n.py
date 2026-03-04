#!/usr/bin/env python3
"""Generate Hebrew i18n message files for common frameworks.

Scaffolds translation JSON structure with Hebrew plural forms,
date/number format patterns, and common UI strings for Israeli apps.

Usage:
    python generate_i18n.py --format react-intl --output src/locales/he.json
    python generate_i18n.py --format vue-i18n --output src/i18n/he.json
    python generate_i18n.py --help

Requirements:
    Python 3.9+ (no external dependencies)
"""

import argparse
import json
import sys


# Common Hebrew UI translations
COMMON_STRINGS = {
    "common.save": "שמור",
    "common.cancel": "ביטול",
    "common.delete": "מחק",
    "common.edit": "ערוך",
    "common.close": "סגור",
    "common.back": "חזרה",
    "common.next": "הבא",
    "common.previous": "הקודם",
    "common.search": "חיפוש",
    "common.loading": "טוען...",
    "common.error": "שגיאה",
    "common.success": "הצלחה",
    "common.confirm": "אישור",
    "common.yes": "כן",
    "common.no": "לא",
    "common.submit": "שלח",
    "common.reset": "איפוס",
}

# Hebrew plural form templates (ICU MessageFormat)
PLURAL_TEMPLATES = {
    "items": "{count, plural, one {פריט אחד} two {שני פריטים} other {{count} פריטים}}",
    "days": "{count, plural, one {יום אחד} two {יומיים} other {{count} ימים}}",
    "hours": "{count, plural, one {שעה אחת} two {שעתיים} other {{count} שעות}}",
    "minutes": "{count, plural, one {דקה אחת} two {שתי דקות} other {{count} דקות}}",
    "weeks": "{count, plural, one {שבוע אחד} two {שבועיים} other {{count} שבועות}}",
    "months": "{count, plural, one {חודש אחד} two {חודשיים} other {{count} חודשים}}",
    "years": "{count, plural, one {שנה אחת} two {שנתיים} other {{count} שנים}}",
    "files": "{count, plural, one {קובץ אחד} two {שני קבצים} other {{count} קבצים}}",
    "messages": "{count, plural, one {הודעה אחת} two {שתי הודעות} other {{count} הודעות}}",
    "results": "{count, plural, one {תוצאה אחת} two {שתי תוצאות} other {{count} תוצאות}}",
}

# Date-related strings
DATE_STRINGS = {
    "date.today": "היום",
    "date.yesterday": "אתמול",
    "date.tomorrow": "מחר",
    "date.sunday": "יום ראשון",
    "date.monday": "יום שני",
    "date.tuesday": "יום שלישי",
    "date.wednesday": "יום רביעי",
    "date.thursday": "יום חמישי",
    "date.friday": "יום שישי",
    "date.saturday": "שבת",
}

# Form validation messages
VALIDATION_STRINGS = {
    "validation.required": "שדה חובה",
    "validation.email": "כתובת אימייל לא תקינה",
    "validation.phone": "מספר טלפון לא תקין",
    "validation.minLength": "מינימום {min} תווים",
    "validation.maxLength": "מקסימום {max} תווים",
    "validation.israeliId": "מספר תעודת זהות לא תקין",
    "validation.postalCode": "מיקוד לא תקין",
}


def generate_react_intl(output_path):
    """Generate react-intl compatible JSON message file."""
    messages = {}
    messages.update(COMMON_STRINGS)
    messages.update(DATE_STRINGS)
    messages.update(VALIDATION_STRINGS)

    # Add plural templates
    for key, template in PLURAL_TEMPLATES.items():
        messages[f"plural.{key}"] = template

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"Generated react-intl messages: {output_path}")
    print(f"  {len(messages)} translation keys")


def generate_vue_i18n(output_path):
    """Generate vue-i18n compatible nested JSON message file."""
    messages = {
        "common": {},
        "date": {},
        "validation": {},
        "plural": {},
    }

    for key, value in COMMON_STRINGS.items():
        section, name = key.split(".", 1)
        messages[section][name] = value

    for key, value in DATE_STRINGS.items():
        section, name = key.split(".", 1)
        messages[section][name] = value

    for key, value in VALIDATION_STRINGS.items():
        section, name = key.split(".", 1)
        messages[section][name] = value

    for key, template in PLURAL_TEMPLATES.items():
        messages["plural"][key] = template

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"Generated vue-i18n messages: {output_path}")
    total = sum(len(v) for v in messages.values())
    print(f"  {total} translation keys in {len(messages)} sections")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Hebrew i18n message files"
    )
    parser.add_argument(
        "--format", choices=["react-intl", "vue-i18n"],
        default="react-intl",
        help="Output format (default: react-intl)"
    )
    parser.add_argument(
        "--output", default="he.json",
        help="Output file path (default: he.json)"
    )
    args = parser.parse_args()

    if args.format == "react-intl":
        generate_react_intl(args.output)
    elif args.format == "vue-i18n":
        generate_vue_i18n(args.output)


if __name__ == "__main__":
    main()
