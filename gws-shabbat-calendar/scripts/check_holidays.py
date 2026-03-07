#!/usr/bin/env python3
"""
Check Jewish holidays and Shabbat times using the HebCal API.

Usage:
    python3 check_holidays.py --help
    python3 check_holidays.py --date 2026-03-13
    python3 check_holidays.py --month 2026-09
    python3 check_holidays.py --range 2026-03-01 2026-04-01
    python3 check_holidays.py --shabbat
    python3 check_holidays.py --shabbat --city jerusalem

Exits with code 1 if the queried date falls on Shabbat or a holiday.
Exits with code 0 if the date is a regular day.
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

CACHE_DIR = Path("/tmp/.hebcal_cache")
CACHE_TTL_HOURS = 24

CITY_GEONAME_IDS = {
    "tel-aviv": "293397",
    "jerusalem": "281184",
    "haifa": "294801",
    "beer-sheva": "295530",
    "eilat": "295277",
}

DEFAULT_CITY = "tel-aviv"

# Holiday categories that block scheduling
BLOCKING_CATEGORIES = {"holiday"}
BLOCKING_SUBCATEGORIES = {"major", "shabbat"}


def get_cache_path(year: int, month: int) -> Path:
    """Return cache file path for a given year-month."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"hebcal_{year}_{month:02d}.json"


def fetch_holidays(year: int, month: int, geonameid: str) -> list[dict]:
    """Fetch holidays from HebCal API with caching."""
    cache_path = get_cache_path(year, month)

    if cache_path.exists():
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if (datetime.now() - mtime).total_seconds() < CACHE_TTL_HOURS * 3600:
            with open(cache_path) as f:
                return json.load(f)

    url = (
        f"https://www.hebcal.com/hebcal?v=1&cfg=json"
        f"&year={year}&month={month}"
        f"&geo=geonameid&geonameid={geonameid}"
        f"&maj=on&min=on&mod=on&nx=on&mf=on&ss=on&i=on"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "gws-shabbat-calendar/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            with open(cache_path, "w") as f:
                json.dump(items, f)
            return items
    except Exception as e:
        print(f"Warning: Could not fetch HebCal data: {e}", file=sys.stderr)
        if cache_path.exists():
            with open(cache_path) as f:
                return json.load(f)
        return []


def fetch_shabbat_times(geonameid: str) -> list[dict]:
    """Fetch this week's Shabbat times."""
    url = f"https://www.hebcal.com/shabbat?cfg=json&geonameid={geonameid}&M=on"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "gws-shabbat-calendar/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("items", [])
    except Exception as e:
        print(f"Warning: Could not fetch Shabbat times: {e}", file=sys.stderr)
        return []


def is_blocked_day(date_str: str, items: list[dict]) -> tuple[bool, list[str]]:
    """Check if a given date (YYYY-MM-DD) is blocked by holidays."""
    blocked_reasons = []
    for item in items:
        item_date = item.get("date", "")[:10]
        if item_date == date_str:
            category = item.get("category", "")
            title = item.get("title", "")
            if category in ("candles", "havdalah", "holiday"):
                blocked_reasons.append(f"{title} ({category})")
    return len(blocked_reasons) > 0, blocked_reasons


def check_friday(date: datetime) -> bool:
    """Check if a date is a Friday (Erev Shabbat)."""
    return date.weekday() == 4  # 4 = Friday


def check_saturday(date: datetime) -> bool:
    """Check if a date is a Saturday (Shabbat)."""
    return date.weekday() == 5  # 5 = Saturday


def format_item(item: dict) -> str:
    """Format a HebCal item for display."""
    date = item.get("date", "")[:10]
    title = item.get("title", "")
    category = item.get("category", "")
    hebrew = item.get("hebrew", "")
    memo = item.get("memo", "")

    parts = [f"  {date}  {title}"]
    if hebrew:
        parts[0] += f"  ({hebrew})"
    if category:
        parts[0] += f"  [{category}]"
    if memo:
        parts.append(f"           {memo[:80]}")
    return "\n".join(parts)


def cmd_date(args):
    """Check a specific date."""
    date = datetime.strptime(args.date, "%Y-%m-%d")
    geonameid = CITY_GEONAME_IDS.get(args.city, CITY_GEONAME_IDS[DEFAULT_CITY])
    items = fetch_holidays(date.year, date.month, geonameid)

    print(f"Checking: {args.date} ({date.strftime('%A')})")
    print(f"City: {args.city}")
    print()

    if check_saturday(date):
        print("BLOCKED: Shabbat (Saturday)")
        sys.exit(1)

    if check_friday(date):
        print("WARNING: Erev Shabbat (Friday) - schedule before 14:00 only")

    is_blocked, reasons = is_blocked_day(args.date, items)
    if is_blocked:
        print(f"BLOCKED: {', '.join(reasons)}")
        sys.exit(1)

    day_items = [i for i in items if i.get("date", "")[:10] == args.date]
    if day_items:
        print("Events on this date:")
        for item in day_items:
            print(format_item(item))
    else:
        print("OK: No holidays or Shabbat conflicts")

    sys.exit(0)


def cmd_month(args):
    """Show holidays for a given month."""
    year, month = map(int, args.month.split("-"))
    geonameid = CITY_GEONAME_IDS.get(args.city, CITY_GEONAME_IDS[DEFAULT_CITY])
    items = fetch_holidays(year, month, geonameid)

    print(f"Holidays for {args.month} ({args.city}):")
    print()

    if not items:
        print("  No holidays found for this month.")
        return

    for item in sorted(items, key=lambda x: x.get("date", "")):
        print(format_item(item))


def cmd_range(args):
    """Show holidays for a date range."""
    start = datetime.strptime(args.range[0], "%Y-%m-%d")
    end = datetime.strptime(args.range[1], "%Y-%m-%d")
    geonameid = CITY_GEONAME_IDS.get(args.city, CITY_GEONAME_IDS[DEFAULT_CITY])

    all_items = []
    current = start
    seen_months = set()
    while current <= end:
        key = (current.year, current.month)
        if key not in seen_months:
            seen_months.add(key)
            all_items.extend(fetch_holidays(current.year, current.month, geonameid))
        current += timedelta(days=28)

    # Filter to range
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    filtered = [
        i for i in all_items
        if start_str <= i.get("date", "")[:10] <= end_str
    ]

    print(f"Holidays from {start_str} to {end_str} ({args.city}):")
    print()

    if not filtered:
        print("  No holidays found in this range.")
        return

    for item in sorted(filtered, key=lambda x: x.get("date", "")):
        print(format_item(item))


def cmd_shabbat(args):
    """Show this week's Shabbat times."""
    geonameid = CITY_GEONAME_IDS.get(args.city, CITY_GEONAME_IDS[DEFAULT_CITY])
    items = fetch_shabbat_times(geonameid)

    print(f"Shabbat times ({args.city}):")
    print()

    for item in items:
        category = item.get("category", "")
        if category in ("candles", "havdalah"):
            date = item.get("date", "")
            title = item.get("title", "")
            print(f"  {title}: {date}")


def main():
    parser = argparse.ArgumentParser(
        description="Check Jewish holidays and Shabbat times (HebCal API)"
    )
    parser.add_argument(
        "--city",
        choices=list(CITY_GEONAME_IDS.keys()),
        default=DEFAULT_CITY,
        help=f"City for Shabbat times (default: {DEFAULT_CITY})",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--date", help="Check specific date (YYYY-MM-DD)")
    group.add_argument("--month", help="Show holidays for month (YYYY-MM)")
    group.add_argument("--range", nargs=2, metavar=("START", "END"),
                       help="Show holidays for date range (YYYY-MM-DD YYYY-MM-DD)")
    group.add_argument("--shabbat", action="store_true",
                       help="Show this week's Shabbat times")

    args = parser.parse_args()

    if args.date:
        cmd_date(args)
    elif args.month:
        cmd_month(args)
    elif args.range:
        cmd_range(args)
    elif args.shabbat:
        cmd_shabbat(args)


if __name__ == "__main__":
    main()
