#!/usr/bin/env python3
"""Check Shabbat times and Israeli holidays for scheduling decisions.

A standalone utility for querying whether a given date/time falls within
Shabbat or an Israeli holiday, and for finding the next available business
slot in Israel.

Usage:
    python check_shabbat.py                     # Check if now is Shabbat
    python check_shabbat.py --date 2026-03-06   # Check a specific date
    python check_shabbat.py --next-slot          # Find next available slot
    python check_shabbat.py --holidays 2026      # List holidays for a year

Requirements:
    pip install requests pytz
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, time

try:
    import pytz
    IL_TZ = pytz.timezone("Asia/Jerusalem")
except ImportError:
    print("Warning: pytz not installed. Using UTC offsets.", file=sys.stderr)
    IL_TZ = None

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests",
          file=sys.stderr)
    sys.exit(1)


# Israeli business hours by weekday (Python weekday: 0=Monday ... 6=Sunday)
BUSINESS_HOURS = {
    6: (time(8, 0), time(18, 0)),   # Sunday (first Israeli business day)
    0: (time(8, 0), time(18, 0)),   # Monday
    1: (time(8, 0), time(18, 0)),   # Tuesday
    2: (time(8, 0), time(18, 0)),   # Wednesday
    3: (time(8, 0), time(18, 0)),   # Thursday
    4: (time(8, 0), time(13, 0)),   # Friday (half day)
    5: None,                         # Saturday (Shabbat -- closed)
}


def get_shabbat_times(date=None, latitude=31.7683, longitude=35.2137,
                      tzid="Asia/Jerusalem"):
    """Get Shabbat candle lighting and havdalah times from HebCal API.

    Args:
        date: Date to check (default: today). Finds the nearest Friday.
        latitude: Location latitude (default: Jerusalem).
        longitude: Location longitude (default: Jerusalem).
        tzid: Timezone ID (default: Asia/Jerusalem).

    Returns:
        Dictionary with 'candle_lighting' and 'havdalah' ISO datetime strings.
    """
    if date is None:
        date = datetime.now()

    # Find next Friday
    days_until_friday = (4 - date.weekday()) % 7
    if days_until_friday == 0 and date.weekday() != 4:
        days_until_friday = 7
    friday = date + timedelta(days=days_until_friday)

    response = requests.get("https://www.hebcal.com/shabbat", params={
        "cfg": "json",
        "gy": friday.year,
        "gm": friday.month,
        "gd": friday.day,
        "latitude": latitude,
        "longitude": longitude,
        "tzid": tzid,
        "b": 18,   # Candle lighting 18 min before sunset (Israel standard)
        "M": "on"  # Include havdalah
    })
    response.raise_for_status()

    data = response.json()
    times = {}
    for item in data.get("items", []):
        if item["category"] == "candles":
            times["candle_lighting"] = item["date"]
        elif item["category"] == "havdalah":
            times["havdalah"] = item["date"]

    return times


def get_holidays(year):
    """Get all Israeli holidays for a given Gregorian year from HebCal API.

    Args:
        year: Gregorian year (e.g. 2026).

    Returns:
        List of holiday dictionaries with title, date, category, yomtov flag.
    """
    response = requests.get("https://www.hebcal.com/hebcal", params={
        "v": 1,
        "cfg": "json",
        "year": year,
        "month": "x",   # All months
        "maj": "on",    # Major holidays
        "min": "on",    # Minor holidays
        "mod": "on",    # Modern holidays
        "i": "on",      # Israeli holidays (1-day yom tov)
        "nx": "off",
        "ss": "off"
    })
    response.raise_for_status()

    data = response.json()
    holidays = []
    for item in data.get("items", []):
        if item["category"] in ("holiday", "roshchodesh"):
            holidays.append({
                "title": item["title"],
                "date": item["date"],
                "category": item.get("subcat", item["category"]),
                "yomtov": item.get("yomtov", False),
                "memo": item.get("memo", "")
            })

    return holidays


def is_business_day(date, holidays_cache=None):
    """Check if a date is a valid Israeli business day.

    Args:
        date: Date object to check.
        holidays_cache: Optional list of holiday dicts from get_holidays().

    Returns:
        True if the date is a business day in Israel.
    """
    # Saturday is always Shabbat
    if date.weekday() == 5:
        return False

    # Check against holiday cache
    if holidays_cache:
        date_str = date.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str) and h.get("yomtov", False):
                return False

    return True


def should_run_today(holidays_cache=None, skip_friday=False,
                     skip_erev_chag=False):
    """Determine if a scheduled job should run today.

    Args:
        holidays_cache: Optional list of holiday dicts.
        skip_friday: Also skip Fridays (half days).
        skip_erev_chag: Skip days before a holiday (erev chag).

    Returns:
        Tuple of (should_run: bool, reason: str).
    """
    if IL_TZ:
        today = datetime.now(IL_TZ).date()
    else:
        today = datetime.utcnow().date()

    # Never run on Shabbat
    if today.weekday() == 5:
        return False, "Shabbat"

    # Check holidays
    if holidays_cache:
        date_str = today.strftime("%Y-%m-%d")
        for h in holidays_cache:
            if h["date"].startswith(date_str) and h.get("yomtov", False):
                return False, f"Yom Tov: {h['title']}"

        # Check if tomorrow is Yom Tov (today is Erev Chag)
        if skip_erev_chag:
            tomorrow = today + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            for h in holidays_cache:
                if (h["date"].startswith(tomorrow_str) and
                        h.get("yomtov", False)):
                    return False, f"Erev Chag: {h['title']} tomorrow"

    # Optionally skip Friday
    if skip_friday and today.weekday() == 4:
        return False, "Friday (half day)"

    return True, "Business day"


def find_next_available_slot(start_date, duration_minutes=60,
                             holidays_cache=None,
                             preferred_hours=(9, 17)):
    """Find the next available business slot in Israel.

    Args:
        start_date: Date to start searching from.
        duration_minutes: Required slot duration in minutes.
        holidays_cache: Optional list of holiday dicts.
        preferred_hours: Tuple of (start_hour, end_hour) for preferred range.

    Returns:
        Dictionary with date, day name, start time, and end time, or None.
    """
    current = start_date
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

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

        slot_start = max(open_time, preferred_start)
        slot_end = min(close_time, preferred_end)

        slot_start_dt = datetime.combine(current, slot_start)
        slot_end_dt = datetime.combine(current, slot_end)

        if (slot_end_dt - slot_start_dt).total_seconds() >= duration_minutes * 60:
            return {
                "date": current.strftime("%Y-%m-%d"),
                "day": day_names[current.weekday()],
                "start": slot_start.strftime("%H:%M"),
                "end": slot_end.strftime("%H:%M"),
            }

        current += timedelta(days=1)

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Check Shabbat times and Israeli holidays for scheduling"
    )
    parser.add_argument(
        "--date", "-d",
        help="Date to check (YYYY-MM-DD format, default: today)"
    )
    parser.add_argument(
        "--shabbat-times", action="store_true",
        help="Get candle lighting and havdalah times for nearest Shabbat"
    )
    parser.add_argument(
        "--holidays", type=int, metavar="YEAR",
        help="List Israeli holidays for a given year"
    )
    parser.add_argument(
        "--is-business-day", action="store_true",
        help="Check if the date is an Israeli business day"
    )
    parser.add_argument(
        "--next-slot", action="store_true",
        help="Find next available business slot"
    )
    parser.add_argument(
        "--duration", type=int, default=60,
        help="Meeting duration in minutes (default: 60)"
    )
    parser.add_argument(
        "--lat", type=float, default=31.7683,
        help="Latitude (default: Jerusalem 31.7683)"
    )
    parser.add_argument(
        "--lon", type=float, default=35.2137,
        help="Longitude (default: Jerusalem 35.2137)"
    )
    args = parser.parse_args()

    # Parse date
    if args.date:
        check_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        check_date = datetime.now()

    # Default action: check if today is a business day and get Shabbat times
    if not any([args.shabbat_times, args.holidays, args.is_business_day,
                args.next_slot]):
        args.shabbat_times = True
        args.is_business_day = True

    results = {}

    if args.shabbat_times:
        try:
            times = get_shabbat_times(
                check_date, latitude=args.lat, longitude=args.lon
            )
            results["shabbat_times"] = times
        except Exception as e:
            results["shabbat_times_error"] = str(e)

    if args.holidays:
        try:
            holidays = get_holidays(args.holidays)
            yom_tov_only = [h for h in holidays if h.get("yomtov", False)]
            results["holidays"] = holidays
            results["yom_tov_count"] = len(yom_tov_only)
        except Exception as e:
            results["holidays_error"] = str(e)

    if args.is_business_day:
        # Try to get holidays for validation
        try:
            holidays_cache = get_holidays(check_date.year)
        except Exception:
            holidays_cache = None

        is_bday = is_business_day(check_date.date(), holidays_cache)
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]
        results["business_day_check"] = {
            "date": check_date.strftime("%Y-%m-%d"),
            "day": day_names[check_date.weekday()],
            "is_business_day": is_bday
        }

    if args.next_slot:
        try:
            holidays_cache = get_holidays(check_date.year)
        except Exception:
            holidays_cache = None

        slot = find_next_available_slot(
            check_date.date(),
            duration_minutes=args.duration,
            holidays_cache=holidays_cache
        )
        results["next_available_slot"] = slot

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
