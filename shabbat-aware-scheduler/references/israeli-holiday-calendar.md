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

**Jerusalem exception:** Candle lighting 40 minutes before sunset (vs. 18 minutes elsewhere in Israel).

## HebCal API Quick Reference

**Shabbat times:**
```
GET https://www.hebcal.com/shabbat?cfg=json&gy=YEAR&gm=MONTH&gd=DAY&latitude=LAT&longitude=LON&tzid=Asia/Jerusalem&b=18&M=on
```

**Holiday list:**
```
GET https://www.hebcal.com/hebcal?v=1&cfg=json&year=YEAR&month=x&maj=on&min=on&mod=on&i=on
```

**Hebrew date converter:**
```
GET https://www.hebcal.com/converter?cfg=json&gy=YEAR&gm=MONTH&gd=DAY&g2h=1
```
