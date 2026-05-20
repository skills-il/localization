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

# Candle-lighting minutes before sunset by city minhag.
# Jerusalem uses 40 min, Haifa and Zikhron Ya'akov use 30 min, elsewhere 18 min.
CANDLE_LIGHTING_MIN = {
    "jerusalem": 40,
    "haifa": 30,
    "zikhron_yaakov": 30,
    "default": 18,
}

def get_shabbat_times(date=None, latitude=31.7683, longitude=35.2137,
                      tzid="Asia/Jerusalem", city="jerusalem"):
    """Get Shabbat candle lighting and havdalah times.
    Default location: Jerusalem (40 min candle-lighting custom).
    """
    if date is None:
        date = datetime.now()

    # Find next Friday
    days_until_friday = (4 - date.weekday()) % 7
    friday = date + timedelta(days=days_until_friday)

    b = CANDLE_LIGHTING_MIN.get(city, CANDLE_LIGHTING_MIN["default"])

    response = requests.get("https://www.hebcal.com/shabbat", params={
        "cfg": "json",
        "gy": friday.year,
        "gm": friday.month,
        "gd": friday.day,
        "latitude": latitude,
        "longitude": longitude,
        "tzid": tzid,
        "b": b,       # Candle lighting min before sunset (city-aware)
        "M": "on",    # Havdalah at Tzeit HaKochavim (sun 8.5 deg below horizon)
        # Alternative: use m=42 / m=50 / m=72 for fixed minutes after sunset
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
| Three Weeks (Bein HaMetzarim) | 17 Tammuz to 9 Av (around Jul-early Aug) | No weddings or celebratory events; corporate parties typically deferred |
| Tisha B'Av | 9 Av (around late Jul / early Aug) | Fast day; many treat as half-day or off |
| Summer (Jul-Aug) | July-August | School vacation, reduced business |
| Winter Shabbat | Nov-Feb | Early Shabbat (Friday closes earlier) |
| Summer Shabbat | May-Aug | Late Shabbat (more Friday availability) |

**Key 2026 holiday dates to plan around (Israel observance):**

| Holiday | Gregorian (around) | Workdays lost |
|---------|---------------------|---------------|
| Pesach | April 1 to April 8, 2026 | First and seventh days are Yom Tov; middle is chol ha-moed |
| Yom HaShoah | April 13 to April 14, 2026 (evening to evening) | Memorial; entertainment closed |
| Yom HaZikaron | April 20 to April 21, 2026 | Memorial; restricted commerce |
| Yom HaAtzmaut | April 21 to April 22, 2026 | Independence Day; most businesses closed |
| Shavuot | May 21 to May 22, 2026 (evening to evening) | One day Yom Tov in Israel |
| Tisha B'Av | July 22 to July 23, 2026 (evening to evening) | Fast day |
| Rosh Hashana | September 11 to September 13, 2026 | Two-day Yom Tov + Shabbat = three-day no-work span |
| Yom Kippur | September 20 to September 21, 2026 (evening to evening) | Country shuts down |
| Sukkot | September 25 to October 2, 2026 | First and last days Yom Tov; middle is chol ha-moed |
| Shemini Atzeret / Simchat Torah | October 2 to October 3, 2026 | One day in Israel, falls on Friday-Shabbat |

Dates verified against Hebcal 2026 (Israeli observance). Always re-check the calendar each year; the Hebrew calendar slides against the Gregorian by 11 to 19 days. In 2026, Yom HaAtzmaut is postponed by one day (nidcheh) because the natural date would have triggered Yom HaZikaron on a problematic day.

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
- `scripts/check_shabbat.py`: standalone utility to query Shabbat times, Israeli holidays, and business-day status via the HebCal API. Supports checking whether a date is Shabbat/Yom Tov, listing all holidays for a year, and finding the next available Israeli business slot with configurable duration, location, and city minhag. Run: `python scripts/check_shabbat.py --help`

### References
- `references/israeli-holiday-calendar.md`: complete Israeli holiday calendar with Hebrew dates, Gregorian approximations, scheduling impact levels (high/medium/low), mourning period restrictions, seasonal Shabbat candle-lighting times by month for Jerusalem, 2026 key dates, and HebCal API endpoint reference. Consult when planning around chagim, determining seasonal Friday closing times, or checking if an event conflicts with a mourning period.

## Recommended MCP Servers

For live Hebrew calendar data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|-----------------|---------|
| **hebcal** | Jewish holidays, Shabbat candle lighting times, Havdalah times, Torah readings, and Hebrew-Gregorian date conversion via the official Hebcal API | [Install hebcal](https://agentskills.co.il/en/mcp/hebcal) |

When the `hebcal` MCP is available, use its tools for accurate Shabbat times and holiday dates instead of hardcoded values. The MCP provides location-aware candle lighting times for any Israeli city.

## Offline Libraries

If you cannot reach the Hebcal API at runtime (CI, airgapped, rate-limited at 90 req/10s), use a local library and skip the HTTP call:

| Library | Language | Notes |
|---------|----------|-------|
| `@hebcal/core` | JavaScript / TypeScript | Actively maintained (v6.x as of May 2026). Pure JS, no network. Install: `npm i @hebcal/core` |
| `pyluach` | Python | Hebrew calendar arithmetic and Hebrew/Gregorian conversion. Stable but low-activity (v2.3.0); fine for date conversion but no built-in candle-lighting times. Pair with a sunset/zmanim library or cache pre-computed times |
| `hebcal-go` | Go | Maintained by the Hebcal team |

The deprecated `hebcal-js` package (NPM `hebcal`) is the predecessor of `@hebcal/core`; do not start new work on it.

## Gotchas
- Shabbat candle-lighting differs by city in Israel. Jerusalem uses 40 minutes before sunset, Haifa and Zikhron Ya'akov use 30 minutes, and most other cities use 18 minutes. Using one `b=` value for all of Israel will under- or over-shoot Friday cutoffs by 10 to 22 minutes. Pass the city-specific offset to the Hebcal API.
- Israeli holidays (chagim) have different work restrictions than Shabbat. Most holidays are one day in Israel but two days in the diaspora (Rosh Hashana is two days in both). Using a diaspora holiday calendar for Israeli scheduling will block extra workdays that are actually chol ha-moed in Israel.
- The Hebrew calendar has leap years with an extra month (Adar II), occurring 7 times in a 19-year cycle. Agents may calculate dates using the Gregorian calendar and miss this month entirely.
- Business hours in Israel run Sunday to Thursday, with Friday a half-day (until early afternoon). Saturday is the weekly rest day, not Sunday. Agents may schedule Friday afternoon meetings or Monday-morning deadlines.
- Yom HaAtzmaut and Yom HaZikaron can be postponed (nidcheh) when their natural date would conflict with Shabbat. In 2026 the dates shift accordingly. Always trust the Hebcal `i=on` flag rather than computing Iyar 5 directly.
- Havdalah default in Hebcal is now Tzeit HaKochavim (sun 8.5 degrees below the horizon, around 40 to 50 minutes after sunset in Israel). Stricter Rabbeinu Tam observers use 72 minutes. Pick the right `m=` value if your audience is not the default.
- Yom Kippur is treated as Shabbat for scheduling purposes (full shutdown, including secular businesses, transit, and broadcast media in Israel). Do not deploy or schedule anything inside the 25-hour window.
- The Three Weeks (17 Tammuz to 9 Av) is a mourning period; weddings, concerts, and corporate celebration events are typically deferred. The Nine Days (1 to 9 Av) is stricter. Treat as a "no launch parties" window even though it is not a Yom Tov.

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

### Error: "Wrong candle-lighting time for Jerusalem"
Cause: Passing `b=18` (the Hebcal default) with Jerusalem coordinates instead of the Jerusalem custom of 40 minutes.
Solution: Always pass `b=40` when the user is in Jerusalem, `b=30` for Haifa and Zikhron Ya'akov, `b=18` everywhere else. Hebcal exposes the same convention.

### Error: "Havdalah time looks off by 8-30 minutes"
Cause: Mixing `M=on` (Tzeit HaKochavim, sun 8.5 degrees below horizon, around 42 to 50 min after sunset) with a hardcoded "42 minutes" or "72 minutes" assumption.
Solution: Pick one method explicitly. Use `M=on` for the Hebcal default, `m=42` for medium stars, `m=50` for small stars, or `m=72` for the stricter Rabbeinu Tam custom. Document which one your scheduler uses so downstream agents do not double-shift.