# Israeli Holiday Calendar Reference

## Major Holidays (Yom Tov -- no work)

| Holiday | Hebrew Name | Hebrew Calendar | Approx. Gregorian | Duration |
|---------|-------------|-----------------|-------------------|----------|
| Rosh Hashanah | ראש השנה | Tishrei 1-2 | Sep/Oct | 2 days |
| Yom Kippur | יום כיפור | Tishrei 10 | Sep/Oct | 1 day |
| Sukkot | סוכות | Tishrei 15 | Sep/Oct | 1 day (+ chol ha-moed) |
| Shemini Atzeret / Simchat Torah | שמיני עצרת / שמחת תורה | Tishrei 22 | Oct | 1 day (combined in Israel) |
| Pesach (first day) | פסח | Nisan 15 | Mar/Apr | 1 day (+ chol ha-moed) |
| Pesach (last day) | פסח | Nisan 21 | Mar/Apr | 1 day |
| Shavuot | שבועות | Sivan 6 | May/Jun | 1 day |

**Note:** Israel observes 1-day Yom Tov (not 2 like diaspora) for all holidays except Rosh Hashanah.

## National Holidays

| Holiday | Hebrew Name | Hebrew Calendar | Type |
|---------|-------------|-----------------|------|
| Yom Ha-Shoah | יום השואה | Nisan 27 | Memorial -- entertainment closed |
| Yom Ha-Zikaron | יום הזיכרון | Iyar 4 | Memorial -- restricted commerce |
| Yom Ha-Atzmaut | יום העצמאות | Iyar 5 | Independence Day -- most businesses closed |

## Scheduling Impact by Period

### High Impact (avoid scheduling)
- **Rosh Hashanah through Yom Kippur (Tishrei 1-10):** "Days of Awe" -- many take extended time off
- **Sukkot week (Tishrei 15-22):** Chol ha-moed days have reduced availability
- **Pesach week (Nisan 15-22):** Chol ha-moed days have reduced availability
- **Yom Kippur (Tishrei 10):** Entire country shuts down -- absolutely no scheduling

### Medium Impact (schedule with caution)
- **Pre-Rosh Hashanah week:** Very busy with preparations
- **Pre-Pesach week:** Extremely busy (cleaning, shopping)
- **Erev Chag (any holiday eve):** Businesses close early, similar to Friday
- **Post-holiday first day:** "Recovery day" -- avoid critical meetings

### Low Impact (mostly normal)
- **Chanukah:** Not a Yom Tov -- businesses open normally, but school events
- **Purim:** Not a Yom Tov -- some businesses may close, festive atmosphere
- **Tu B'Shvat:** Minor holiday -- normal business
- **Lag B'Omer:** Minor holiday -- bonfires evening before

### Mourning Periods (restrict celebrations/events)
- **Sefirat Ha-Omer:** Between Pesach and Shavuot -- some restrict weddings/events
- **Three Weeks (17 Tammuz - 9 Av):** No weddings, concerts, or joyful events
- **Nine Days (1-9 Av):** Stricter restrictions on celebrations

## Shabbat Timing by Season (Jerusalem)

| Month | Candle Lighting (approx.) | Havdalah (approx.) | Friday Business Close |
|-------|--------------------------|--------------------|-----------------------|
| January | 16:15 | 17:30 | 13:00-14:00 |
| February | 16:45 | 17:55 | 13:30-14:30 |
| March | 17:15 | 18:25 | 14:00-15:00 |
| April (DST) | 18:45 | 19:55 | 15:00-16:00 |
| May | 19:10 | 20:25 | 15:30-16:30 |
| June | 19:25 | 20:45 | 16:00-17:00 |
| July | 19:20 | 20:40 | 16:00-17:00 |
| August | 19:00 | 20:15 | 15:30-16:30 |
| September | 18:20 | 19:30 | 15:00-16:00 |
| October (DST end) | 17:40 | 18:50 | 14:00-15:00 |
| November | 16:10 | 17:20 | 13:00-14:00 |
| December | 16:05 | 17:20 | 13:00-14:00 |

**City-specific candle-lighting minutes before sunset:**

| City | `b=` value | Notes |
|------|-----------|-------|
| Jerusalem | 40 | Ancient Jerusalem custom |
| Haifa, Zikhron Ya'akov | 30 | Local minhag |
| Tel Aviv, Beer Sheva, Eilat, Netanya, most other Israeli cities | 18 | Standard Hebcal default |

## 2026 Key Dates (Israel observance, verified May 2026)

| Holiday | Gregorian | Day of week |
|---------|-----------|-------------|
| Pesach (first day) | April 2, 2026 (eve April 1) | Thursday |
| Pesach (last day) | April 8, 2026 | Wednesday |
| Yom HaShoah | April 14, 2026 | Tuesday |
| Yom HaZikaron | April 21, 2026 | Tuesday |
| Yom HaAtzmaut | April 22, 2026 | Wednesday (nidcheh, postponed one day) |
| Shavuot | May 22, 2026 (eve May 21) | Friday |
| 17 Tammuz fast | early July 2026 | start of the Three Weeks |
| Tisha B'Av | July 23, 2026 (eve July 22) | Thursday |
| Rosh Hashana | September 12 to 13, 2026 (eve September 11) | Saturday and Sunday; combined with the Shabbat that precedes it, creates a three-day no-work span |
| Yom Kippur | September 21, 2026 (eve September 20) | Monday |
| Sukkot (first day) | September 26, 2026 (eve September 25) | Saturday (Friday eve) |
| Sukkot (last day, chol ha-moed boundary) | October 2, 2026 | Friday |
| Shemini Atzeret / Simchat Torah | October 3, 2026 (eve October 2) | Saturday |

In 2026, Sukkot starts Friday evening and runs into Shabbat, and Shemini Atzeret falls on Friday-Saturday. These create extended no-work spans for Israeli businesses.

## Havdalah Calculation

Hebcal default with `M=on` is Tzeit HaKochavim (sun 8.5 degrees below horizon, around 42 to 50 minutes after sunset in Israel). Fixed-minute alternatives via `m=N`:

| `m=` value | Minhag |
|-----------|--------|
| `m=42` | Three medium-sized stars |
| `m=50` | Three small stars |
| `m=72` | Rabbeinu Tam (stricter) |
| `m=0` | Suppress havdalah times |

## HebCal API Quick Reference

Endpoints documented at `https://www.hebcal.com/home/developer-apis`. Rate limit: 90 requests per 10-second window (HTTP 429 on overflow).

**Shabbat times:**
```
GET https://www.hebcal.com/shabbat?cfg=json&gy=YEAR&gm=MONTH&gd=DAY&latitude=LAT&longitude=LON&tzid=Asia/Jerusalem&b=40&M=on
```
Use `b=40` for Jerusalem, `b=30` for Haifa, `b=18` elsewhere. `M=on` enables Tzeit HaKochavim havdalah; replace with `m=42` / `m=50` / `m=72` for fixed minutes.

**Holiday list (Israeli observance):**
```
GET https://www.hebcal.com/hebcal?v=1&cfg=json&year=YEAR&month=x&maj=on&min=on&mod=on&i=on
```
The `i=on` flag is critical; without it you get diaspora 2-day Yom Tov.

**Hebrew date converter:**
```
GET https://www.hebcal.com/converter?cfg=json&gy=YEAR&gm=MONTH&gd=DAY&g2h=1
```

**Zmanim (halachic times like sunrise, midday, alot hashachar):**
```
GET https://www.hebcal.com/zmanim?cfg=json&latitude=LAT&longitude=LON&tzid=Asia/Jerusalem&date=YYYY-MM-DD
```
