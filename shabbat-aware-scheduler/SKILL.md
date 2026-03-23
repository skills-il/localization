---
name: shabbat-aware-scheduler
description: Schedule meetings, deployments, and events respecting Shabbat, Israeli holidays (chagim), and Hebrew calendar constraints. Use when user asks to schedule around Shabbat, "zmanim", check Israeli holidays, plan around chagim, set Israeli business hours, or needs Hebrew calendar-aware scheduling logic. Includes halachic times (zmanim) via HebCal API, full Israeli holiday calendar, and Israeli business hour conventions. Do NOT use for religious halachic rulings (consult a rabbi) or diaspora 2-day holiday scheduling.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(curl:*)
compatibility: Network required for HebCal API calls. Works offline with pre-cached holiday data. Python recommended.
---

# Shabbat-Aware Scheduler

## Instructions

### Step 1: Determine Scheduling Context
| Context | Key Constraints | Examples |
|---------|----------------|---------|
| Meeting scheduling | Israeli business hours (Sun-Thu), Shabbat, chagim | "Schedule a team meeting next week" |
| Deployment planning | No deploys during Shabbat, chagim, or Erev Chag | "When can we deploy this release?" |
| Event planning | Hebrew calendar restrictions, venue availability | "Plan a product launch event" |
| Cron/automation | Skip Shabbat and holidays for recurring tasks | "Run this job daily except Shabbat" |
| Notification timing | Don't send during Shabbat or late hours | "Schedule push notification campaign" |

### Step 2: Get Zmanim and Holiday Data

Use the HebCal API to retrieve Shabbat times and holiday data.
See `scripts/check_shabbat.py` for a ready-to-use utility.

**Query HebCal API for Shabbat times:**
```python
import requests
from datetime import datetime, timedelta

def get_shabbat_times(date=None, latitude=31.7683, longitude=35.2137, tzid="Asia/Jerusalem"):
    """Get Shabbat candle lighting and havdalah times.
    Default location: Jerusalem.
    """
    if date is None:
        date = datetime.now()

    # Find next Friday
    days_until_friday = (4 - date.weekday()) % 7
    friday = date + timedelta(days=days_until_friday)

    response = requests.get("https://www.hebcal.com/shabbat", params={
        "cfg": "json",
        "gy": friday.year,
        "gm": friday.month,
        "gd": friday.day,
        "latitude": latitude,
        "longitude": longitude,
        "tzid": tzid,
        "b": 18,  # Candle lighting minutes before sunset (18 for Israel)
        "M": "on"  # Include havdalah
    })

    data = response.json()
    times = {}
    for item in data.get("items", []):
        if item["category"] == "candles":
            times["candle_lighting"] = item["date"]
        elif item["category"] == "havdalah":
            times["havdalah"] = item["date"]

    return times
```

**Get all Israeli holidays for a year:**
```python
def get_holidays(year):
    """Get all Israeli holidays for a given year."""
    response = requests.get("https://www.hebcal.com/hebcal", params={
        "v": 1,
        "cfg": "json",
        "year": year,
        "month": "x",  # All months
        "maj": "on",   # Major holidays
        "min": "on",   # Minor holidays
        "mod": "on",   # Modern holidays
        "i": "on",     # Israeli holidays (1-day yom tov)
        "nx": "off",
        "ss": "off"
    })

    data = response.json()
    holidays = []
    for item in data.get("items", []):
        if item["category"] in ["holiday", "roshchodesh"]:
            holidays.append({
                "title": item["title"],
                "date": item["date"],
                "category": item.get("subcat", item["category"]),
                "yomtov": item.get("yomtov", False),
                "memo": item.get("memo", "")
            })

    return holidays
```

### Step 3: Implement Scheduling Logic

**Israeli business hours:**

| Day | Hours | Notes |
|-----|-------|-------|
| Sunday | 08:00-18:00 | First day of Israeli workweek |
| Monday | 08:00-18:00 | Regular business day |
| Tuesday | 08:00-18:00 | Regular business day |
| Wednesday | 08:00-18:00 | Regular business day |
| Thursday | 08:00-18:00 | Regular business day |
| Friday | 08:00-13:00 | Half day (closes before Shabbat) |
| Saturday | Closed | Shabbat (no business) |

**Core scheduling function:**
```python
from datetime import datetime, timedelta, time
import pytz

IL_TZ = pytz.timezone("Asia/Jerusalem")

BUSINESS_HOURS = {
    6: (time(8, 0), time(18, 0)),  # Sunday
    0: (time(8, 0), time(18, 0)),  # Monday
    1: (time(8, 0), time(18, 0)),  # Tuesday
    2: (time(8, 0), time(18, 0)),  # Wednesday
    3: (time(8, 0), time(18, 0)),  # Thursday
    4: (time(8, 0), time(13, 0)),  # Friday (half day)
    5: None,                        # Saturday (Shabbat)
}

def is_business_day(date, holidays_cache=None):
    """Check if a date is a valid Israeli business day."""
    if date.weekday() == 5:  # Saturday
        return False
    if holidays_cache:
        date_str = date.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str) and h["yomtov"]:
                return False
    return True
```

### Step 4: Holiday-Aware Cron Jobs

```python
def should_run_today(holidays_cache=None, skip_friday=False, skip_erev_chag=False):
    """Determine if a scheduled job should run today."""
    today = datetime.now(IL_TZ).date()

    # Never run on Shabbat
    if today.weekday() == 5:
        return False, "Shabbat"

    # Check holidays
    if holidays_cache:
        date_str = today.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str):
                if h["yomtov"]:
                    return False, f"Yom Tov: {h['title']}"

        # Check if tomorrow is Yom Tov (today is Erev Chag)
        if skip_erev_chag:
            tomorrow = today + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            for h in holidays_cache:
                if h["date"].startswith(tomorrow_str) and h["yomtov"]:
                    return False, f"Erev Chag: {h['title']} tomorrow"

    if skip_friday and today.weekday() == 4:
        return False, "Friday (half day)"

    return True, "Business day"
```

### Step 5: Pre-Holiday and Seasonal Awareness

| Period | Dates (approx.) | Impact on Scheduling |
|--------|-----------------|---------------------|
| Erev Shabbat (Friday) | Every week | Close by 13:00-15:00 depending on season |
| Erev Rosh Hashanah | ~Sep | Businesses close by noon |
| Rosh Hashanah + Yom Kippur season | Tishrei 1-10 | 10 days of reduced availability |
| Sukkot week | Tishrei 15-22 | Many on vacation, chol ha-moed |
| Pre-Pesach week | Before Nisan 15 | Extremely busy, cleaning/shopping |
| Pesach week | Nisan 15-22 | Many on vacation, chol ha-moed |
| Summer (Jul-Aug) | July-August | School vacation, reduced business |
| Winter Shabbat | Nov-Feb | Early Shabbat (Friday closes earlier) |
| Summer Shabbat | May-Aug | Late Shabbat (more Friday availability) |

## Examples

### Example 1: Schedule a Meeting
User says: "Schedule a team meeting for next week"
Result: Check Israeli business hours (Sun-Thu), verify no chagim, suggest available slots. Avoid Friday unless morning and confirm it is not Erev Chag.

### Example 2: Deployment Window
User says: "When is the safest time to deploy this week?"
Result: Find a Tuesday or Wednesday slot (mid-week, maximum buffer from Shabbat), during business hours, not before a holiday. Recommend morning deployment for maximum rollback time before Shabbat.

### Example 3: Holiday-Aware Cron
User says: "Set up a daily report that skips Shabbat and holidays"
Result: Provide cron configuration with should_run_today() check, pre-loaded holiday cache for the year, with logging for skipped days.

## Bundled Resources

### Scripts
- `scripts/check_shabbat.py` — Standalone utility to query Shabbat times, Israeli holidays, and business-day status via the HebCal API. Supports checking whether a date is Shabbat/Yom Tov, listing all holidays for a year, and finding the next available Israeli business slot with configurable duration and location. Run: `python scripts/check_shabbat.py --help`

### References
- `references/israeli-holiday-calendar.md` — Complete Israeli holiday calendar with Hebrew dates, Gregorian approximations, scheduling impact levels (high/medium/low), mourning period restrictions, seasonal Shabbat candle-lighting times by month for Jerusalem, and HebCal API endpoint reference. Consult when planning around chagim, determining seasonal Friday closing times, or checking if an event conflicts with a mourning period.

## Gotchas
- Shabbat times vary by city in Israel. Jerusalem candle lighting is 40 minutes before sunset, while most other cities use 20-30 minutes. Agents may use a single time for all of Israel.
- Israeli holidays (chagim) have different work restrictions than Shabbat. Some holidays are one day in Israel but two days in the diaspora. Agents may use diaspora holiday calendars for Israeli scheduling.
- The Hebrew calendar has leap years with an extra month (Adar II), occurring 7 times in a 19-year cycle. Agents may calculate dates using the Gregorian calendar and miss this month entirely.
- Business hours in Israel typically run Sunday-Thursday, with Friday being a half-day (until early afternoon). Agents may schedule Friday afternoon meetings or Monday morning deadlines (Saturday is the weekly rest day, not Sunday).

## Troubleshooting

### Error: "Meeting scheduled during Shabbat"
Cause: Timezone mismatch, server in UTC, Shabbat times in local
Solution: Always convert to Asia/Jerusalem timezone before checking. Shabbat times vary by season and location.

### Error: "Holiday not detected"
Cause: Using Gregorian-only calendar without Hebrew date mapping
Solution: Use HebCal API which handles Hebrew-Gregorian conversion. Cache holiday data annually and refresh at Rosh Hashanah.

### Error: "Friday meeting too late"
Cause: Fixed 17:00 Friday cutoff regardless of season
Solution: In winter, Shabbat can start as early as 16:00. Always check actual candle lighting time for the specific Friday.