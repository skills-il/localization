# Jewish Calendar Reference for Scheduling

## Israeli Workweek

| Day | Hebrew | Status | Business Hours |
|-----|--------|--------|----------------|
| Sunday (Yom Rishon) | יום ראשון | Full workday | 08:00-18:00 |
| Monday (Yom Sheni) | יום שני | Full workday | 08:00-18:00 |
| Tuesday (Yom Shlishi) | יום שלישי | Full workday | 08:00-18:00 |
| Wednesday (Yom Revi'i) | יום רביעי | Full workday | 08:00-18:00 |
| Thursday (Yom Chamishi) | יום חמישי | Full workday | 08:00-18:00 |
| Friday (Yom Shishi) | יום שישי | Half day | 08:00-13:00 (14:00 max) |
| Saturday (Shabbat) | שבת | Day of rest | No business |

## Timezone

- **Standard:** IST (Israel Standard Time) = UTC+2
- **Daylight Saving:** IDT (Israel Daylight Time) = UTC+3
- **IANA identifier:** `Asia/Jerusalem`
- **DST transitions:** Last Friday before April 2 (spring forward), last Sunday of October (fall back)

## Shabbat Rules

| Rule | Detail |
|------|--------|
| Start | Friday at sunset (candle-lighting, typically 18 minutes before sunset) |
| End | Saturday at nightfall (Havdalah, typically 40-72 minutes after sunset) |
| Business cutoff | Friday 13:00-14:00 (most offices close by this time) |
| Erev Shabbat | Friday afternoon, reduced activity |
| API source | `https://www.hebcal.com/shabbat?cfg=json&geonameid=293397` (Tel Aviv) |

### Common Geoname IDs for HebCal
| City | Geoname ID |
|------|-----------|
| Tel Aviv | 293397 |
| Jerusalem | 281184 |
| Haifa | 294801 |
| Beer Sheva | 295530 |

## Major Jewish Holidays (Chagim)

### Full Work Prohibition (Yom Tov)

| Holiday | Hebrew | Hebrew Date | Typical Gregorian | Duration | Impact |
|---------|--------|-------------|-------------------|----------|--------|
| Rosh Hashana | ראש השנה | 1-2 Tishrei | Sep/Oct | 2 days | Full block, no work |
| Yom Kippur | יום כיפור | 10 Tishrei | Sep/Oct | 1 day | Full block, fasting, country shuts down |
| Sukkot (first day) | סוכות | 15 Tishrei | Sep/Oct | 1 day | Full block |
| Shemini Atzeret / Simchat Torah | שמיני עצרת / שמחת תורה | 22 Tishrei | Oct | 1 day | Full block |
| Pesach (first day) | פסח | 15 Nisan | Mar/Apr | 1 day | Full block |
| Pesach (last day) | פסח | 21 Nisan | Mar/Apr | 1 day | Full block |
| Shavuot | שבועות | 6 Sivan | May/Jun | 1 day | Full block |

### Intermediate Days (Chol HaMoed)

| Period | Hebrew | Duration | Impact |
|--------|--------|----------|--------|
| Chol HaMoed Sukkot | חול המועד סוכות | 5 days | Partial, many take off, reduced scheduling |
| Chol HaMoed Pesach | חול המועד פסח | 4-5 days | Partial, many take off, reduced scheduling |

### National Memorial and Independence Days

| Day | Hebrew | Impact |
|-----|--------|--------|
| Yom HaShoah | יום השואה | Memorial day, sirens, reduced activity |
| Yom HaZikaron | יום הזיכרון | Memorial day, sirens, country pauses |
| Yom HaAtzmaut | יום העצמאות | Independence Day, national holiday |

### Fast Days

| Fast | Hebrew | Impact |
|------|--------|--------|
| Tzom Gedaliah | צום גדליה | Minor fast, most work normally |
| Asara B'Tevet | עשרה בטבת | Minor fast, most work normally |
| Ta'anit Esther | תענית אסתר | Minor fast, day before Purim |
| Shiva Asar B'Tammuz | שבעה עשר בתמוז | Minor fast |
| Tisha B'Av | תשעה באב | Major fast, many take off, reduced scheduling |

### Other Notable Days

| Day | Hebrew | Impact |
|-----|--------|--------|
| Purim | פורים | Not a day off but festive, costume day, reduced productivity |
| Chanukah | חנוכה | 8 days, work continues, school holidays, early departures |
| Tu BiShvat | ט"ו בשבט | Regular workday |
| Lag BaOmer | ל"ג בעומר | Regular workday |

## Erev Chag (Holiday Eve) Rules

| Rule | Detail |
|------|--------|
| Office closing | Most close by 13:00 on Erev Chag |
| Meeting scheduling | Avoid afternoon meetings on Erev Chag |
| Similar to Friday | Treat Erev Chag like Erev Shabbat for scheduling purposes |

## HebCal API Reference

### Holiday Lookup
```
GET https://www.hebcal.com/hebcal?v=1&cfg=json&year=YYYY&month=MM&geo=geonameid&geonameid=293397&maj=on&min=on&mod=on&nx=on&mf=on&ss=on
```

### Parameters
| Param | Values | Description |
|-------|--------|-------------|
| `maj` | on/off | Major holidays |
| `min` | on/off | Minor holidays |
| `mod` | on/off | Modern holidays (Yom HaShoah, etc.) |
| `nx` | on/off | Rosh Chodesh |
| `mf` | on/off | Minor fasts |
| `ss` | on/off | Special Shabbatot |
| `i` | on/off | Israeli calendar (1-day Yom Tov) |

### Response Categories
| Category | Meaning |
|----------|---------|
| `holiday` | Jewish holiday |
| `candles` | Shabbat/Yom Tov candle lighting |
| `havdalah` | End of Shabbat/Yom Tov |
| `roshchodesh` | New Hebrew month |

## Scheduling Decision Matrix

| Day Type | Can Schedule? | Hours | Notes |
|----------|--------------|-------|-------|
| Sun-Thu (regular) | Yes | 08:00-18:00 | Normal Israeli business day |
| Friday (regular) | Limited | 08:00-13:00 | End by 14:00 absolute latest |
| Shabbat | No | N/A | No scheduling |
| Yom Tov | No | N/A | No scheduling |
| Chol HaMoed | Caution | 08:00-16:00 | Many on vacation, expect low attendance |
| Erev Chag | Limited | 08:00-13:00 | Treat like Friday |
| Memorial days | Caution | 08:00-18:00 | Avoid morning meetings (sirens) |
| Fast days (minor) | Yes | 08:00-18:00 | Normal hours, some may leave early |
| Tisha B'Av | Caution | 08:00-14:00 | Major fast, many take off |
