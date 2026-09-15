#!/usr/bin/env python3
"""Generate Hebrew i18n message files for common frameworks.

Scaffolds translation JSON structure with Hebrew plural forms,
date/number format patterns, and common UI strings for Israeli apps.

Usage:
    python generate_i18n.py --format react-intl --output src/locales/he.json
    python generate_i18n.py --format vue-i18n --output src/i18n/he.json
    python generate_i18n.py --format next-intl --output messages/he.json
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

# Hebrew plural forms in CLDR category order for Hebrew: one, two, other.
# Hebrew has no zero/few/many categories, so three forms cover every count.
# {count} is replaced with the number in the "other" form.
PLURAL_FORMS = {
    "items": ("פריט אחד", "שני פריטים", "{count} פריטים"),
    "days": ("יום אחד", "יומיים", "{count} ימים"),
    "hours": ("שעה אחת", "שעתיים", "{count} שעות"),
    "minutes": ("דקה אחת", "שתי דקות", "{count} דקות"),
    "weeks": ("שבוע אחד", "שבועיים", "{count} שבועות"),
    "months": ("חודש אחד", "חודשיים", "{count} חודשים"),
    "years": ("שנה אחת", "שנתיים", "{count} שנים"),
    "files": ("קובץ אחד", "שני קבצים", "{count} קבצים"),
    "messages": ("הודעה אחת", "שתי הודעות", "{count} הודעות"),
    "results": ("תוצאה אחת", "שתי תוצאות", "{count} תוצאות"),
}


def icu_plural(forms):
    """ICU MessageFormat plural string, used by react-intl and next-intl."""
    one, two, other = forms
    return "{count, plural, one {%s} two {%s} other {%s}}" % (one, two, other)


def vue_plural(forms):
    """vue-i18n pipe-separated plural string.

    vue-i18n does not parse ICU plural syntax. vue-i18n 11.x
    picks a case by position and reads three cases as zero | one | other, so
    register a Hebrew rule in createI18n that maps 1 -> 0, 2 -> 1, anything
    else -> 2: pluralRules with legacy: false, or pluralizationRules in legacy
    mode (the default on 11.x when legacy is not set).
    {count} is a predefined argument.
    """
    return " | ".join(forms)


PLURAL_TEMPLATES = {key: icu_plural(forms) for key, forms in PLURAL_FORMS.items()}

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
    """Generate vue-i18n compatible nested JSON message file.

    Plurals use vue-i18n pipe syntax, used as t('plural.days', count).
    """
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

    for key, forms in PLURAL_FORMS.items():
        messages["plural"][key] = vue_plural(forms)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"Generated vue-i18n messages: {output_path}")
    print("  Plurals are one | two | other: in createI18n set legacy: false and")
    print("  pluralRules: { he: (choice) => (choice === 1 ? 0 : choice === 2 ? 1 : 2) }")
    print("  (in legacy mode the option is pluralizationRules)")
    total = sum(len(v) for v in messages.values())
    print(f"  {total} translation keys in {len(messages)} sections")


def generate_next_intl(output_path):
    """Generate next-intl compatible nested JSON message file.

    next-intl uses nested namespaces and supports ICU MessageFormat
    for plurals. Structure: { namespace: { key: value } }
    """
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

    print(f"Generated next-intl messages: {output_path}")
    total = sum(len(v) for v in messages.values())
    print(f"  {total} translation keys in {len(messages)} namespaces")
    print("  Use with: const t = useTranslations('common');")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Hebrew i18n message files"
    )
    parser.add_argument(
        "--format", choices=["react-intl", "vue-i18n", "next-intl"],
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
    elif args.format == "next-intl":
        generate_next_intl(args.output)


if __name__ == "__main__":
    main()
