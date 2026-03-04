# Hebrew Pluralization Rules

## CLDR Plural Categories for Hebrew

Hebrew uses three plural categories defined by the Unicode CLDR:

| Category | Rule | Examples |
|----------|------|---------|
| one | n = 1 and v = 0 | 1 |
| two | n = 2 and v = 0 | 2 |
| other | everything else | 0, 3, 4, 5, 10, 100, 0.5, 1.5 |

Where `n` is the absolute value and `v` is the number of visible fraction digits.

## Common Noun Plural Forms

### Time Units

| Singular (1) | Dual (2) | Plural (3+) | With number |
|-------------|----------|-------------|-------------|
| יום אחד | יומיים | ימים | 5 ימים |
| שעה אחת | שעתיים | שעות | 3 שעות |
| דקה אחת | שתי דקות | דקות | 10 דקות |
| שנייה אחת | שתי שניות | שניות | 30 שניות |
| שבוע אחד | שבועיים | שבועות | 4 שבועות |
| חודש אחד | חודשיים | חודשים | 6 חודשים |
| שנה אחת | שנתיים | שנים | 3 שנים |

### Common Objects

| Singular | Dual | Plural |
|----------|------|--------|
| פריט אחד | שני פריטים | פריטים |
| קובץ אחד | שני קבצים | קבצים |
| הודעה אחת | שתי הודעות | הודעות |
| תוצאה אחת | שתי תוצאות | תוצאות |
| עמוד אחד | שני עמודים | עמודים |
| משתמש אחד | שני משתמשים | משתמשים |

## ICU MessageFormat Patterns

### Basic Pattern
```
{count, plural,
  one {פריט אחד}
  two {שני פריטים}
  other {{count} פריטים}
}
```

### With Gender Context
```
{count, plural,
  one {הודעה אחת חדשה}
  two {שתי הודעות חדשות}
  other {{count} הודעות חדשות}
}
```

### Zero Handling
Hebrew uses the `other` category for zero, but you may want explicit handling:
```
{count, plural,
  =0 {אין פריטים}
  one {פריט אחד}
  two {שני פריטים}
  other {{count} פריטים}
}
```

## Edge Cases

### Decimal Numbers
Decimal numbers always use the `other` category:
- 1.5 ימים (not יום)
- 2.5 שעות (not שעתיים)

### Numbers 11-19
Despite ending in teen forms, they use `other`:
- 11 ימים, 12 שעות, 15 פריטים

### Gender Agreement with Numbers
- Masculine: אחד, שניים, שלושה, ארבעה, חמישה
- Feminine: אחת, שתיים, שלוש, ארבע, חמש
- Numbers 1-10 take the OPPOSITE gender of the noun they modify
