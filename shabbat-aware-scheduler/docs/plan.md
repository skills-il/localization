# Shabbat-Aware Scheduler Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for scheduling that respects Shabbat, Israeli holidays (chagim), and the Hebrew calendar — including halachic times (zmanim), Israeli business hours, and holiday-aware date calculations.

**Architecture:** Domain-Specific Intelligence skill. Embeds knowledge of Hebrew calendar, zmanim calculations, Israeli holiday schedule, and business hour conventions for building scheduling logic.

**Tech Stack:** SKILL.md, Python scheduling scripts, zmanim API references.

---

## Research

### Zmanim (Halachic Times) APIs and Libraries
- **HebCal API:** `https://www.hebcal.com/zmanim` — Free REST API for zmanim, holidays, Torah readings
  - Endpoints: `/shabbat`, `/converter` (Hebrew/Gregorian dates), `/holidays`
  - Returns candle lighting, havdalah, and all zmanim for a location
- **KosherJava (KosherZmanim):** Java library ported to Python (`zmanim` PyPI package)
  - Calculates all standard zmanim: sunrise, sunset, candle lighting, havdalah
  - Supports multiple halachic opinions (GRA, Rabbeinu Tam, etc.)
- **Key zmanim for scheduling:**
  - **Candle lighting:** Typically 18-40 minutes before sunset on Friday (varies by community — 18 min standard in Israel, 40 min in Jerusalem)
  - **Havdalah:** After 3 stars visible Saturday night (typically 42-72 minutes after sunset)
  - **Shkiah (sunset):** Exact sunset time — Shabbat begins before this
  - **Tzet ha-kochavim:** Nightfall — when 3 medium stars are visible

### Israeli Holiday Calendar (Chagim)
- **Shabbat:** Every Friday sunset to Saturday nightfall — NO EXCEPTIONS
- **Rosh Hashanah:** Tishrei 1-2 (September/October) — 2 days
- **Yom Kippur:** Tishrei 10 — Most restrictive day, entire country stops
- **Sukkot:** Tishrei 15 (1 day yom tov in Israel + chol ha-moed through Tishrei 21)
- **Shemini Atzeret / Simchat Torah:** Tishrei 22 (1 day in Israel, combined)
- **Pesach:** Nisan 15 and 21 (yom tov days, chol ha-moed between)
- **Shavuot:** Sivan 6 (1 day in Israel)
- **Israeli Independence Day (Yom Ha-Atzmaut):** Iyar 5 — National holiday, most businesses closed
- **Israeli Memorial Day (Yom Ha-Zikaron):** Iyar 4 — Solemn day, restricted commerce
- **Holocaust Remembrance Day (Yom Ha-Shoah):** Nisan 27 — Solemn day, entertainment venues closed
- **Chol Ha-Moed:** Intermediate days of Sukkot and Pesach — some businesses open, reduced hours
- **Note:** Israel observes 1-day yom tov (not 2 like diaspora) for all holidays except Rosh Hashanah

### Israeli Business Hours
- **Standard workweek:** Sunday through Thursday (NOT Monday-Friday)
- **Friday:** Half day — most businesses close by 14:00-15:00 (depending on season and Shabbat entry time)
- **Saturday:** Closed (Shabbat) — exceptions: essential services, Arab-sector businesses, some secular entertainment
- **Sunday:** Regular business day (first day of the Israeli workweek)
- **Typical hours:** 08:00/09:00 to 17:00/18:00 Sunday-Thursday
- **Government offices:** Usually 08:00-15:00/16:00 Sunday-Thursday, some have public hours only certain days
- **Banks:** Typically Sunday-Thursday, some open Thursday evening, limited Friday hours
- **Tech companies:** Often flexible, but meetings typically 09:00-18:00 Sunday-Thursday

### Scheduling Around Chagim
- **Erev Chag (holiday eve):** Similar to Friday — businesses close early
- **Chol Ha-Moed:** Many people vacation; expect reduced availability
- **Pre-holiday rush:** Week before Pesach and Rosh Hashanah — very busy, hard to schedule
- **Post-chag:** First day back often a "recovery day" — avoid scheduling critical meetings
- **Sefirat Ha-Omer:** Between Pesach and Shavuot — some observe restrictions on events/celebrations
- **Three Weeks / Nine Days:** Between 17 Tammuz and 9 Av — no celebrations, weddings, or joyful events

### Use Cases
1. **Schedule a meeting** — Find available slots respecting Shabbat and chagim
2. **Plan a deployment** — Ensure deployments don't overlap with Shabbat or holidays
3. **Set business hours** — Configure Israeli business hour logic for an application
4. **Holiday-aware cron jobs** — Schedule recurring tasks that skip Shabbat and holidays
5. **Event planning** — Check dates against Hebrew calendar restrictions

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: shabbat-aware-scheduler
description: >-
  Schedule meetings, deployments, and events respecting Shabbat, Israeli holidays
  (chagim), and Hebrew calendar constraints. Use when user asks to schedule around
  Shabbat, "zmanim", check Israeli holidays, plan around chagim, set Israeli
  business hours, or needs Hebrew calendar-aware scheduling logic. Includes
  halachic times (zmanim) via HebCal API, full Israeli holiday calendar, and
  Israeli business hour conventions. Do NOT use for religious halachic rulings
  (consult a rabbi) or diaspora 2-day holiday scheduling.
license: MIT
allowed-tools: "Bash(python:*) Bash(pip:*) Bash(curl:*)"
compatibility: "Network required for HebCal API calls. Works offline with pre-cached holiday data. Python recommended."
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags: [shabbat, scheduling, hebrew-calendar, zmanim, holidays, israel]
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

**Core scheduling engine:**
```python
from datetime import datetime, timedelta, time
import pytz

IL_TZ = pytz.timezone("Asia/Jerusalem")

# Israeli business hours
BUSINESS_HOURS = {
    6: (time(8, 0), time(18, 0)),  # Sunday (weekday 6 in Python)
    0: (time(8, 0), time(18, 0)),  # Monday
    1: (time(8, 0), time(18, 0)),  # Tuesday
    2: (time(8, 0), time(18, 0)),  # Wednesday
    3: (time(8, 0), time(18, 0)),  # Thursday
    4: (time(8, 0), time(13, 0)),  # Friday (half day)
    5: None,                        # Saturday (Shabbat — closed)
}

def is_business_day(date, holidays_cache=None):
    """Check if a date is a valid Israeli business day."""
    # Saturday is always non-business
    if date.weekday() == 5:
        return False

    # Check against holiday cache
    if holidays_cache:
        date_str = date.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str) and h["yomtov"]:
                return False

    return True


def is_shabbat_now(shabbat_times):
    """Check if current time falls within Shabbat."""
    now = datetime.now(IL_TZ)
    candle = datetime.fromisoformat(shabbat_times["candle_lighting"])
    havdalah = datetime.fromisoformat(shabbat_times["havdalah"])

    return candle <= now <= havdalah


def find_next_available_slot(
    start_date,
    duration_minutes=60,
    holidays_cache=None,
    preferred_hours=(9, 17)
):
    """Find the next available business slot in Israel."""
    current = start_date

    for _ in range(60):  # Search up to 60 days ahead
        if not is_business_day(current, holidays_cache):
            current += timedelta(days=1)
            continue

        hours = BUSINESS_HOURS.get(current.weekday())
        if hours is None:
            current += timedelta(days=1)
            continue

        open_time, close_time = hours
        preferred_start = time(preferred_hours[0], 0)
        preferred_end = time(preferred_hours[1], 0)

        # Use the later of business open and preferred start
        slot_start = max(open_time, preferred_start)
        # Use the earlier of business close and preferred end
        slot_end = min(close_time, preferred_end)

        # Check if duration fits
        slot_start_dt = datetime.combine(current, slot_start)
        slot_end_dt = datetime.combine(current, slot_end)

        if (slot_end_dt - slot_start_dt).total_seconds() >= duration_minutes * 60:
            return {
                "date": current.strftime("%Y-%m-%d"),
                "day": ["Monday", "Tuesday", "Wednesday", "Thursday",
                        "Friday", "Saturday", "Sunday"][current.weekday()],
                "start": slot_start.strftime("%H:%M"),
                "end": slot_end.strftime("%H:%M"),
            }

        current += timedelta(days=1)

    return None
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

    # Optionally skip Friday
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
| Winter Shabbat | Nov-Feb | Early Shabbat — Friday closes earlier |
| Summer Shabbat | May-Aug | Late Shabbat — more Friday availability |

## Examples

### Example 1: Schedule a Meeting
User says: "Schedule a team meeting for next week"
Result: Check Israeli business hours (Sun-Thu), verify no chagim, suggest available slots. Avoid Friday unless morning and confirm it's not Erev Chag.

### Example 2: Deployment Window
User says: "When is the safest time to deploy this week?"
Result: Find a Tuesday or Wednesday slot (mid-week, maximum buffer from Shabbat), during business hours, not before a holiday. Recommend morning deployment for maximum rollback time before Shabbat.

### Example 3: Holiday-Aware Cron
User says: "Set up a daily report that skips Shabbat and holidays"
Result: Provide cron configuration with should_run_today() check, pre-loaded holiday cache for the year, with logging for skipped days.

## Troubleshooting

### Error: "Meeting scheduled during Shabbat"
Cause: Timezone mismatch — server in UTC, Shabbat times in local
Solution: Always convert to Asia/Jerusalem timezone before checking. Shabbat times vary by season and location.

### Error: "Holiday not detected"
Cause: Using Gregorian-only calendar without Hebrew date mapping
Solution: Use HebCal API which handles Hebrew-Gregorian conversion. Cache holiday data annually and refresh at Rosh Hashanah.

### Error: "Friday meeting too late"
Cause: Fixed 17:00 Friday cutoff regardless of season
Solution: In winter, Shabbat can start as early as 16:00. Always check actual candle lighting time for the specific Friday.
```
