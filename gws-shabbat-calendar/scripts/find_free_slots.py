#!/usr/bin/env python3
"""
Find free meeting slots in a Google Calendar agenda, excluding Shabbat,
Jewish holidays, and existing events.

Supports cross-timezone overlap for Israel/US scheduling.

Usage:
    python3 find_free_slots.py --help
    python3 find_free_slots.py --events events.json --duration 60
    python3 find_free_slots.py --events events.json --duration 30 --exclude-holidays
    python3 find_free_slots.py --events events.json --duration 60 \\
        --overlap-tz "America/New_York" --overlap-start 09:00 --overlap-end 17:00

Input:
    JSON file from `gws calendar agenda --output json`

Output:
    List of available time slots (printed to stdout)
"""

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


# Israeli workweek: Sunday=6, Monday=0, Tuesday=1, Wednesday=2, Thursday=3
ISRAELI_WORKDAYS = {6, 0, 1, 2, 3}  # Python weekday() values
FRIDAY_WEEKDAY = 4


def parse_time(time_str: str) -> tuple[int, int]:
    """Parse HH:MM string to hours and minutes."""
    parts = time_str.split(":")
    return int(parts[0]), int(parts[1])


def fetch_holidays_for_week(start_date: datetime, end_date: datetime) -> set[str]:
    """Fetch holidays from HebCal for the given date range."""
    holidays = set()

    current = start_date
    seen_months = set()
    while current <= end_date:
        key = (current.year, current.month)
        if key not in seen_months:
            seen_months.add(key)
            url = (
                f"https://www.hebcal.com/hebcal?v=1&cfg=json"
                f"&year={current.year}&month={current.month}"
                f"&geo=geonameid&geonameid=293397"
                f"&maj=on&min=off&mod=on&nx=off&mf=off&ss=off&i=on"
            )
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "gws-shabbat-calendar/1.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    for item in data.get("items", []):
                        category = item.get("category", "")
                        if category == "holiday":
                            date_str = item.get("date", "")[:10]
                            holidays.add(date_str)
            except Exception as e:
                print(f"Warning: Could not fetch holidays: {e}", file=sys.stderr)
        current += timedelta(days=28)

    return holidays


def load_events(events_file: str) -> list[dict]:
    """Load events from a JSON file."""
    with open(events_file) as f:
        return json.load(f)


def parse_event_times(events: list[dict]) -> list[tuple[datetime, datetime]]:
    """Extract start/end datetimes from event list."""
    busy = []
    for event in events:
        start_info = event.get("start", {})
        end_info = event.get("end", {})

        start_str = start_info.get("dateTime", start_info.get("date", ""))
        end_str = end_info.get("dateTime", end_info.get("date", ""))

        if not start_str or not end_str:
            continue

        try:
            start = datetime.fromisoformat(start_str)
            end = datetime.fromisoformat(end_str)
            busy.append((start, end))
        except ValueError:
            continue

    return sorted(busy, key=lambda x: x[0])


def get_work_hours(
    date: datetime,
    work_start: tuple[int, int],
    work_end: tuple[int, int],
    friday_end: tuple[int, int],
) -> tuple[datetime, datetime] | None:
    """Get work hours for a given date, respecting Israeli workweek."""
    weekday = date.weekday()

    if weekday == 5:  # Saturday (Shabbat)
        return None
    if weekday not in ISRAELI_WORKDAYS and weekday != FRIDAY_WEEKDAY:
        return None

    start_h, start_m = work_start
    if weekday == FRIDAY_WEEKDAY:
        end_h, end_m = friday_end
    else:
        end_h, end_m = work_end

    day_start = date.replace(hour=start_h, minute=start_m, second=0, microsecond=0)
    day_end = date.replace(hour=end_h, minute=end_m, second=0, microsecond=0)

    return day_start, day_end


def compute_overlap_window(
    date: datetime,
    local_start: datetime,
    local_end: datetime,
    overlap_tz_offset: int,
    overlap_start: tuple[int, int],
    overlap_end: tuple[int, int],
) -> tuple[datetime, datetime] | None:
    """Compute the overlap window between local and remote business hours."""
    # Convert remote business hours to local time
    remote_start_utc_h = overlap_start[0] - overlap_tz_offset
    remote_end_utc_h = overlap_end[0] - overlap_tz_offset

    # Israel is UTC+2 (winter) or UTC+3 (summer)
    # Approximate: use +2 for simplicity, user should adjust
    israel_offset = 2
    remote_start_local = remote_start_utc_h + israel_offset
    remote_end_local = remote_end_utc_h + israel_offset

    overlap_begin = date.replace(
        hour=max(local_start.hour, remote_start_local),
        minute=0, second=0, microsecond=0,
    )
    overlap_finish = date.replace(
        hour=min(local_end.hour, remote_end_local),
        minute=0, second=0, microsecond=0,
    )

    if overlap_begin >= overlap_finish:
        return None

    return overlap_begin, overlap_finish


def find_gaps(
    day_start: datetime,
    day_end: datetime,
    busy: list[tuple[datetime, datetime]],
    duration_min: int,
) -> list[tuple[datetime, datetime]]:
    """Find free slots of at least duration_min minutes."""
    slots = []
    current = day_start

    day_busy = [
        (max(s, day_start), min(e, day_end))
        for s, e in busy
        if s < day_end and e > day_start
    ]
    day_busy.sort(key=lambda x: x[0])

    for busy_start, busy_end in day_busy:
        if (busy_start - current).total_seconds() >= duration_min * 60:
            slots.append((current, busy_start))
        current = max(current, busy_end)

    if (day_end - current).total_seconds() >= duration_min * 60:
        slots.append((current, day_end))

    return slots


def main():
    parser = argparse.ArgumentParser(
        description="Find free meeting slots excluding Shabbat and holidays"
    )
    parser.add_argument(
        "--events", required=True,
        help="Path to JSON events file (from gws calendar agenda --output json)",
    )
    parser.add_argument(
        "--work-start", default="09:00",
        help="Work start time HH:MM (default: 09:00)",
    )
    parser.add_argument(
        "--work-end", default="18:00",
        help="Work end time HH:MM (default: 18:00)",
    )
    parser.add_argument(
        "--friday-end", default="14:00",
        help="Friday end time HH:MM (default: 14:00)",
    )
    parser.add_argument(
        "--duration", type=int, default=60,
        help="Minimum slot duration in minutes (default: 60)",
    )
    parser.add_argument(
        "--exclude-holidays", action="store_true",
        help="Exclude Jewish holidays (queries HebCal API)",
    )
    parser.add_argument(
        "--overlap-tz",
        help="Remote timezone for cross-tz scheduling (e.g., America/New_York)",
    )
    parser.add_argument(
        "--overlap-start", default="09:00",
        help="Remote work start HH:MM (default: 09:00)",
    )
    parser.add_argument(
        "--overlap-end", default="17:00",
        help="Remote work end HH:MM (default: 17:00)",
    )

    args = parser.parse_args()

    work_start = parse_time(args.work_start)
    work_end = parse_time(args.work_end)
    friday_end = parse_time(args.friday_end)

    events = load_events(args.events)
    busy = parse_event_times(events)

    if not busy:
        print("No events found in the input file.", file=sys.stderr)

    # Determine date range from events
    if busy:
        min_date = min(s for s, _ in busy).date()
        max_date = max(e for _, e in busy).date()
    else:
        min_date = datetime.now().date()
        max_date = min_date + timedelta(days=5)

    # Extend range to cover full work week
    start_date = min_date
    end_date = max_date

    # Fetch holidays if requested
    holidays = set()
    if args.exclude_holidays:
        holidays = fetch_holidays_for_week(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.min.time()),
        )

    # Timezone offsets for overlap calculation
    tz_offsets = {
        "America/New_York": -5,
        "America/Chicago": -6,
        "America/Denver": -7,
        "America/Los_Angeles": -8,
        "Europe/London": 0,
        "Europe/Berlin": 1,
    }

    overlap_tz_offset = None
    if args.overlap_tz:
        overlap_tz_offset = tz_offsets.get(args.overlap_tz)
        if overlap_tz_offset is None:
            print(
                f"Warning: Unknown timezone '{args.overlap_tz}'. "
                f"Known: {', '.join(tz_offsets.keys())}",
                file=sys.stderr,
            )

    overlap_start = parse_time(args.overlap_start)
    overlap_end = parse_time(args.overlap_end)

    print(f"Free slots ({args.duration}+ min):")
    print(f"  Work hours: {args.work_start}-{args.work_end} (Fri: until {args.friday_end})")
    if args.exclude_holidays:
        print(f"  Excluding {len(holidays)} holiday(s)")
    if args.overlap_tz:
        print(f"  Overlap with {args.overlap_tz} ({args.overlap_start}-{args.overlap_end})")
    print()

    total_slots = 0
    current_date = start_date

    while current_date <= end_date:
        dt = datetime.combine(current_date, datetime.min.time())
        date_str = current_date.strftime("%Y-%m-%d")

        # Skip Shabbat
        if dt.weekday() == 5:
            current_date += timedelta(days=1)
            continue

        # Skip holidays
        if date_str in holidays:
            print(f"  {date_str} ({dt.strftime('%A')}): HOLIDAY - skipped")
            current_date += timedelta(days=1)
            continue

        # Get work hours
        hours = get_work_hours(dt, work_start, work_end, friday_end)
        if hours is None:
            current_date += timedelta(days=1)
            continue

        day_start, day_end = hours

        # Apply overlap window if specified
        if overlap_tz_offset is not None:
            overlap = compute_overlap_window(
                dt, day_start, day_end,
                overlap_tz_offset, overlap_start, overlap_end,
            )
            if overlap is None:
                print(f"  {date_str} ({dt.strftime('%A')}): No overlap window")
                current_date += timedelta(days=1)
                continue
            day_start, day_end = overlap

        # Find gaps
        slots = find_gaps(day_start, day_end, busy, args.duration)

        if slots:
            print(f"  {date_str} ({dt.strftime('%A')}):")
            for slot_start, slot_end in slots:
                duration = int((slot_end - slot_start).total_seconds() / 60)
                print(
                    f"    {slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
                    f"  ({duration} min)"
                )
                total_slots += 1

        current_date += timedelta(days=1)

    print()
    print(f"Total available slots: {total_slots}")


if __name__ == "__main__":
    main()
