#!/usr/bin/env python3
"""Check Shabbat times and Israeli holidays for scheduling decisions.

A standalone utility for querying whether a given date/time falls within
Shabbat, a Yom Tov, or another Israeli non-working observance, and for
finding the next available business slot in Israel.

Stringency direction: every ambiguous case resolves toward NOT scheduling.
A day that is closed for part of the country is reported as closed, and a
moment inside the candle-lighting-to-havdalah window is reported as Shabbat
even when the calendar date is a weekday.

Usage:
    python check_shabbat.py                      # Is it Shabbat right now?
    python check_shabbat.py --is-rest-period-now # Shabbat OR Yom Tov, time-aware
    python check_shabbat.py --date 2026-03-06    # Check a specific date
    python check_shabbat.py --next-slot          # Find next available slot
    python check_shabbat.py --holidays 2026      # List holidays for a year
    python check_shabbat.py --city haifa --shabbat-times

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


# Hebcal geonameids. Passing geonameid makes Hebcal apply each city's own
# candle-lighting minhag automatically, which is why it is the preferred path
# over sending raw latitude/longitude plus a hand-picked b= offset.
CITY_GEONAMEID = {
    "jerusalem": 281184,
    "tel_aviv": 293397,
    "haifa": 294801,
    "beersheba": 295530,
    "tiberias": 293322,
    "safed": 293100,
    "netanya": 294071,
    "ashdod": 295629,
    "petah_tikva": 293918,
}

# Fallback only, for the raw latitude/longitude path. Hebcal documents exactly
# three Israeli offsets: 40 minutes for Jerusalem, 30 for Haifa and Zikhron
# Ya'akov, 18 everywhere else. Do NOT invent additional per-city values here;
# use a geonameid instead so Hebcal supplies the city's own minhag.
CANDLE_LIGHTING_MIN = {
    "jerusalem": 40,
    "haifa": 30,
    "zikhron_yaakov": 30,
    "default": 18,
}

# Days that are not Yom Tov but on which the country, or a large part of it,
# does not work. Hebcal reports these with yomtov=false, so a yomtov-only
# filter silently treats them as ordinary business days.
#   closed  = do not schedule at all
#   reduced = morning only; businesses shut by early afternoon
CLOSED_OBSERVANCES = {
    "Yom HaAtzma'ut": "closed",
    "Yom HaAtzmaut": "closed",
    "Yom HaZikaron": "closed",
    "Yom HaShoah": "reduced",
    # Evening-before closures. Yom HaZikaron opens with the 20:00 siren the
    # previous evening and Yom HaShoah with an evening ceremony; places of
    # entertainment are shut from that evening. The DAY before each is
    # therefore not a normal evening either.
    "Tish'a B'Av": "reduced",
    "Purim": "reduced",
    # Minor fast days. Only visible when get_holidays() passes mf=on.
    "Tzom Gedaliah": "reduced",
    "Asara B'Tevet": "reduced",
    "Ta'anit Esther": "reduced",
    "Ta'anit Bechorot": "reduced",
    "Tzom Tammuz": "reduced",
}

# Observed in Jerusalem and other historically walled cities only. A national
# scheduler must not block it, and a Jerusalem scheduler must not ignore it.
JERUSALEM_ONLY_OBSERVANCES = {"Shushan Purim"}


def _norm(title):
    """Normalize a Hebcal title for lookup.

    Hebcal emits typographic apostrophes (U+2019), so "Yom HaAtzma’ut" never
    matches a table keyed on the ASCII form. Matching on the raw title is how
    Yom HaAtzma'ut and Tish'a B'Av were silently reported as business days.
    """
    return title.replace("\u2019", "'").replace("\u02bc", "'").strip()


def candle_lighting_minutes(city=None, latitude=None, longitude=None):
    """Return the candle-lighting offset in minutes for the raw lat/lon path.

    Prefer get_shabbat_times(geonameid=...) instead: Hebcal then applies the
    city's own minhag and this function is not consulted at all.

    The city name wins when it is one of the three documented Israeli minhagim.
    The coordinate fallback requires BOTH latitude and longitude, because
    latitude alone cannot separate Jerusalem from coastal cities that sit on
    the same parallel (Ashdod is 31.80N and uses 18 minutes, not 40).
    """
    if city:
        key = city.lower()
        if key in ("default", "none", ""):
            key = None
        if key in CANDLE_LIGHTING_MIN and key != "default":
            return CANDLE_LIGHTING_MIN[key]
        if key is not None:
            return CANDLE_LIGHTING_MIN["default"]
        # city was explicitly "default": fall through to coordinates so the
        # caller does not silently get 18 minutes for Jerusalem.

    if latitude is not None and longitude is not None:
        # Jerusalem, within roughly 15 km of the city centre.
        if 31.70 <= latitude <= 31.85 and 35.10 <= longitude <= 35.30:
            return CANDLE_LIGHTING_MIN["jerusalem"]
        # Haifa and Zikhron Ya'akov, along the Carmel coast.
        if 32.55 <= latitude <= 32.85 and 34.90 <= longitude <= 35.10:
            return CANDLE_LIGHTING_MIN["haifa"]

    return CANDLE_LIGHTING_MIN["default"]


def get_shabbat_times(date=None, latitude=31.7683, longitude=35.2137,
                      tzid="Asia/Jerusalem", city="jerusalem", geonameid=None):
    """Get Shabbat candle lighting and havdalah times from Hebcal.

    Args:
        date: Date to anchor on (default: today). Resolves to the Shabbat of
            THAT week, so asking on a Saturday returns the Shabbat currently
            in progress, not the following one.
        latitude / longitude: Location for the raw-coordinate path.
        tzid: Timezone ID (default: Asia/Jerusalem).
        city: City key for the fallback candle-lighting minhag.
        geonameid: Preferred. When given, Hebcal applies the city's own
            candle-lighting minhag and latitude/longitude/city are ignored.

    Returns:
        Dictionary with 'candle_lighting' and 'havdalah' ISO datetime strings.
    """
    if date is None:
        date = datetime.now(IL_TZ) if IL_TZ else datetime.now()

    # Anchor on the Friday of the CURRENT Shabbat week. Saturday belongs to the
    # Shabbat that began the previous evening, so it must look backwards by one
    # day, not forwards by six. Sunday through Thursday look forwards.
    if date.weekday() == 5:            # Saturday
        friday = date - timedelta(days=1)
    else:
        friday = date + timedelta(days=(4 - date.weekday()) % 7)

    params = {
        "cfg": "json",
        "gy": friday.year,
        "gm": friday.month,
        "gd": friday.day,
        "M": "on",   # Havdalah at tzeit hakochavim (sun 8.5 deg below horizon)
    }
    if geonameid is not None:
        params["geonameid"] = geonameid
    else:
        params["latitude"] = latitude
        params["longitude"] = longitude
        params["tzid"] = tzid
        params["b"] = candle_lighting_minutes(city=city, latitude=latitude,
                                              longitude=longitude)

    response = requests.get("https://www.hebcal.com/shabbat", params=params,
                            timeout=20)
    response.raise_for_status()

    # A week containing a chag returns SEVERAL candles/havdalah pairs. Select
    # the one belonging to the target Friday; taking the last match seen
    # silently returns chag times labelled as Shabbat times, off by days.
    friday_str = friday.strftime("%Y-%m-%d")
    saturday_str = (friday + timedelta(days=1)).strftime("%Y-%m-%d")
    data = response.json()
    times = {}
    for item in data.get("items", []):
        if item["category"] == "candles" and item["date"].startswith(friday_str):
            times["candle_lighting"] = item["date"]
        elif (item["category"] == "havdalah"
                and item["date"].startswith(saturday_str)):
            times["havdalah"] = item["date"]

    return times


def get_holidays(year):
    """Get all Israeli holidays for a given Gregorian year from Hebcal.

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
        "i": "on",      # Israeli observance (1-day yom tov)
        "mf": "on",     # Minor fasts. Without this, Tzom Gedaliah, Asara
                        # B'Tevet, Ta'anit Esther, Ta'anit Bechorot and Tzom
                        # Tammuz never appear at all: maj/min/mod do not
                        # return them.
        "nx": "off",
        "ss": "off"
    }, timeout=20)
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


def classify_day(date, holidays_cache=None, jerusalem=False):
    """Classify an Israeli calendar date for scheduling.

    Returns a tuple of (status, reason) where status is one of:
        "closed"         -- Shabbat, Yom Tov, or a national shutdown day
        "reduced"        -- open in the morning only (erev chag, fast day)
        "evening_closed" -- a full working day whose EVENING is restricted
                            (eve of Yom HaZikaron, Yom HaShoah, Tisha B'Av)
        "open"           -- ordinary business day

    Chol ha-moed returns "open": it is a legal workday in Israel, though
    staffing is thin. The caller decides whether to treat it as reduced.
    """
    if date.weekday() == 5:
        return "closed", "Shabbat"

    if not holidays_cache:
        # Fail CLOSED. An empty cache means Hebcal was unreachable or rate
        # limited, and answering "open" there is how a scheduler books a
        # meeting on Yom Kippur during an outage.
        return "closed", "Unknown: holiday data unavailable, failing closed"

    date_str = date.strftime("%Y-%m-%d")
    tomorrow_str = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    status, reason = "open", "Business day"

    # Erev status is DERIVED, not enumerated: any day whose successor is Yom
    # Tov is an erev chag and shuts by early afternoon. A hardcoded erev list
    # silently misses cases like Hoshana Raba (erev Shmini Atzeret).
    # The same applies to the national closures that are not Yom Tov: Yom
    # HaZikaron opens with the 20:00 siren the evening before, so no evening
    # event belongs on the preceding date either.
    EVENING_ONSET = ("Yom HaZikaron", "Yom HaShoah", "Tish'a B'Av")
    for h in holidays_cache:
        if not h["date"].startswith(tomorrow_str):
            continue
        title = _norm(h["title"])
        if h.get("yomtov", False):
            status, reason = "reduced", "Erev %s (morning only)" % title
            break
        if title in EVENING_ONSET:
            # A full working DAY. Only the evening is restricted, so this is
            # deliberately not "reduced": collapsing it into the erev-chag
            # status would drag in the morning-only clamp and block an
            # ordinary Monday afternoon.
            status = "evening_closed"
            reason = ("Eve of %s (workday, but no evening events: observance "
                      "starts this evening)" % title)
            break

    for h in holidays_cache:
        if not h["date"].startswith(date_str):
            continue
        title = _norm(h["title"])
        if h.get("yomtov", False):
            return "closed", "Yom Tov: %s" % title
        if title in JERUSALEM_ONLY_OBSERVANCES:
            if jerusalem:
                return "closed", "%s (Jerusalem and walled cities)" % title
            continue
        level = CLOSED_OBSERVANCES.get(title)
        if level == "closed":
            return "closed", title
        if level == "reduced" and status == "open":
            status, reason = "reduced", "%s (morning only)" % title

    return status, reason


def is_business_day(date, holidays_cache=None, jerusalem=False,
                    allow_reduced=True):
    """Check if a date is a valid Israeli business day.

    A "reduced" day (erev chag, fast day) counts as a business day by default
    because the morning is workable. Pass allow_reduced=False for deployments
    and anything else that must not run on a half-staffed day.
    """
    status, _ = classify_day(date, holidays_cache, jerusalem=jerusalem)
    if status == "closed":
        return False
    if status == "reduced" and not allow_reduced:
        return False
    return True


def is_rest_period_now(now=None, **shabbat_kwargs):
    """Time-aware check: is this MOMENT inside Shabbat OR a Yom Tov?

    Hebcal's /shabbat endpoint returns every candle-lighting and havdalah pair
    in the week, including Erev Chag, so one call covers both. Checking only
    the Friday pair is why an erev-Yom-Kippur cron fired at 19:30 with Yom
    Kippur already in.

    is_business_day() answers a question about a calendar DATE. Shabbat and
    Yom Tov begin at candle-lighting the previous evening, so a Friday date is
    a business day while Friday 19:00 is already Shabbat. Anything that fires
    at a specific time (a cron, a notification send, a deploy) must use this
    function, not the date-granular one.

    Returns (bool, reason).
    """
    if now is None:
        now = datetime.now(IL_TZ) if IL_TZ else datetime.utcnow()
    if now.tzinfo is None and IL_TZ:
        now = IL_TZ.localize(now)

    try:
        for start, end in _rest_windows(now, **shabbat_kwargs):
            if start <= now <= end:
                return True, "Rest period (%s to %s)" % (start.isoformat(),
                                                         end.isoformat())
    except (KeyError, ValueError, requests.RequestException) as exc:
        # Fail closed rather than guessing.
        return True, "Rest times unavailable (%s); failing closed" % exc

    return False, "Not a rest period"


def _rest_windows(anchor, **kwargs):
    """Every (candle_lighting, havdalah) pair Hebcal reports for that week.

    Query the ANCHOR DATE itself. Hebcal's weekly window rolls over on Sunday
    at local midnight, so the anchor date's own week is the one that contains
    it. Shifting forward to the next Friday first (as get_shabbat_times must,
    because it is specifically asked for Shabbat) fetches the FOLLOWING week
    for any Sunday-to-Thursday moment, which is how a Sunday-evening Yom
    Kippur onset reads back as "not a rest period".
    """
    params = {"cfg": "json", "gy": anchor.year, "gm": anchor.month,
              "gd": anchor.day, "M": "on"}
    if kwargs.get("geonameid") is not None:
        params["geonameid"] = kwargs["geonameid"]
    else:
        params["latitude"] = kwargs.get("latitude", 31.7683)
        params["longitude"] = kwargs.get("longitude", 35.2137)
        params["tzid"] = kwargs.get("tzid", "Asia/Jerusalem")
        params["b"] = candle_lighting_minutes(
            city=kwargs.get("city", "jerusalem"),
            latitude=params["latitude"], longitude=params["longitude"])

    # Fetch the previous week too. A week can open with a havdalah whose
    # candle-lighting belongs to the week before (a chag that began on the
    # preceding Friday), and pairing the leftover havdalah with a LATER
    # candle by position produces an inverted window that can never match.
    # That is how a Sunday Yom Tov read back as "not a rest period".
    items = []
    for offset in (-7, 0):
        d = anchor + timedelta(days=offset)
        q = dict(params, gy=d.year, gm=d.month, gd=d.day)
        r = requests.get("https://www.hebcal.com/shabbat", params=q,
                         timeout=20)
        r.raise_for_status()
        items.extend(r.json().get("items", []))

    seen, events = set(), []
    for i in items:
        if i["category"] not in ("candles", "havdalah"):
            continue
        key = (i["category"], i["date"])
        if key in seen:
            continue
        seen.add(key)
        events.append((datetime.fromisoformat(i["date"]), i["category"]))
    events.sort()

    # Pair each candle-lighting with the FIRST havdalah after it, by time.
    windows, open_start = [], None
    for when, cat in events:
        if cat == "candles":
            if open_start is None:
                open_start = when
        elif open_start is not None:
            windows.append((open_start, when))
            open_start = None
    return windows


def should_run_today(holidays_cache=None, skip_friday=False,
                     skip_erev_chag=False, now=None, jerusalem=False,
                     time_aware=True, rest_kwargs=None):
    """Determine if a scheduled job should run right now.

    With time_aware=True (the default) this also refuses to run inside the
    live candle-lighting-to-havdalah window, so a Friday-evening cron does not
    fire during Shabbat just because the calendar date is still Friday.

    rest_kwargs is passed through to is_rest_period_now (geonameid, or
    city/latitude/longitude). Omitting it evaluates the window for Jerusalem,
    which is 22 minutes early for a Tel Aviv caller.

    Returns (should_run: bool, reason: str).
    """
    if now is None:
        now = datetime.now(IL_TZ) if IL_TZ else datetime.utcnow()
    today = now.date()

    if time_aware:
        resting, why = is_rest_period_now(now, **(rest_kwargs or {}))
        if resting:
            return False, why

    status, reason = classify_day(today, holidays_cache, jerusalem=jerusalem)
    if status == "closed":
        return False, reason
    if status == "reduced":
        # "Morning only" has to mean morning only. Treating a reduced day as
        # runnable until midnight is how a job lands at 19:30 on erev chag.
        if skip_erev_chag or (time_aware and now.time() >= time(13, 0)):
            return False, reason
    if status == "evening_closed":
        # The working day is fine; the evening is not.
        if time_aware and now.time() >= time(17, 0):
            return False, reason

    if skip_friday and today.weekday() == 4:
        return False, "Friday (half day)"

    return True, reason


def find_next_available_slot(start, duration_minutes=60,
                             holidays_cache=None,
                             preferred_hours=(9, 17),
                             jerusalem=False,
                             allow_reduced=False):
    """Find the next available business slot in Israel.

    Args:
        start: datetime or date to search from. When a datetime is given, its
            time of day is honoured, so searching from Thursday 17:30 will not
            propose Thursday 09:00.
        duration_minutes: Required slot length. The returned slot is exactly
            this long, not the whole open window.
        holidays_cache: Optional list of holiday dicts from get_holidays().
        preferred_hours: (start_hour, end_hour) preferred range.
        jerusalem: Apply Jerusalem-only observances (Shushan Purim).
        allow_reduced: Permit erev chag and fast days. Off by default, since
            the usual caller is scheduling a meeting other people must attend.

    Returns:
        Dictionary with date, day name, start, end, and the classification
        reason, or None if nothing was found within 60 days.
    """
    if isinstance(start, datetime):
        current = start.date()
        earliest = start.time()
    else:
        current = start
        earliest = time(0, 0)

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

    for _ in range(60):
        status, reason = classify_day(current, holidays_cache,
                                      jerusalem=jerusalem)
        hours = BUSINESS_HOURS.get(current.weekday())
        blocked = status == "closed" or (status == "reduced" and
                                         not allow_reduced)

        if not blocked and hours is not None:
            open_time, close_time = hours
            slot_start = max(open_time, time(preferred_hours[0], 0), earliest)
            slot_end = min(close_time, time(preferred_hours[1], 0))
            if status == "reduced":
                # "Morning only" has to bind here too, or this entrypoint
                # hands out an erev-Yom-Kippur afternoon slot whose own
                # reason string says the day is morning only.
                slot_end = min(slot_end, time(13, 0))

            span = (datetime.combine(current, slot_end) -
                    datetime.combine(current, slot_start))
            if span.total_seconds() >= duration_minutes * 60:
                end_dt = (datetime.combine(current, slot_start) +
                          timedelta(minutes=duration_minutes))
                return {
                    "date": current.strftime("%Y-%m-%d"),
                    "day": day_names[current.weekday()],
                    "start": slot_start.strftime("%H:%M"),
                    "end": end_dt.strftime("%H:%M"),
                    "status": status,
                    "reason": reason,
                }

        current += timedelta(days=1)
        earliest = time(0, 0)

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Check Shabbat times and Israeli holidays for scheduling"
    )
    parser.add_argument("--date", "-d",
                        help="Date to check (YYYY-MM-DD, default: today)")
    parser.add_argument("--shabbat-times", action="store_true",
                        help="Candle lighting and havdalah for that week's Shabbat")
    parser.add_argument("--is-shabbat-now", "--is-rest-period-now",
                        dest="is_shabbat_now", action="store_true",
                        help="Time-aware check of whether Shabbat or a Yom Tov "
                             "is in progress right now")
    parser.add_argument("--holidays", type=int, metavar="YEAR",
                        help="List Israeli holidays for a given year")
    parser.add_argument("--is-business-day", action="store_true",
                        help="Classify the date as closed / reduced / open")
    parser.add_argument("--next-slot", action="store_true",
                        help="Find next available business slot")
    parser.add_argument("--duration", type=int, default=60,
                        help="Meeting duration in minutes (default: 60)")
    parser.add_argument("--lat", type=float, default=31.7683,
                        help="Latitude (default: Jerusalem 31.7683)")
    parser.add_argument("--lon", type=float, default=35.2137,
                        help="Longitude (default: Jerusalem 35.2137)")
    parser.add_argument("--city", default="jerusalem",
                        help="City key. Known geonameids: %s. Anything else "
                             "falls back to latitude/longitude."
                             % ", ".join(sorted(CITY_GEONAMEID)))
    parser.add_argument("--jerusalem", action="store_true",
                        help="Apply Jerusalem-only observances (Shushan Purim)")
    args = parser.parse_args()

    if args.date:
        check_date = datetime.strptime(args.date, "%Y-%m-%d")
        if IL_TZ:
            check_date = IL_TZ.localize(check_date)
    else:
        check_date = datetime.now(IL_TZ) if IL_TZ else datetime.now()

    geonameid = CITY_GEONAMEID.get((args.city or "").lower())
    jerusalem = args.jerusalem or (args.city or "").lower() == "jerusalem"

    if not any([args.shabbat_times, args.holidays, args.is_business_day,
                args.next_slot, args.is_shabbat_now]):
        args.shabbat_times = True
        args.is_business_day = True

    results = {}

    if args.shabbat_times:
        try:
            results["shabbat_times"] = get_shabbat_times(
                check_date, latitude=args.lat, longitude=args.lon,
                city=args.city, geonameid=geonameid)
        except Exception as e:
            results["shabbat_times_error"] = str(e)

    if args.is_shabbat_now:
        resting, why = is_rest_period_now(
            check_date, geonameid=geonameid, latitude=args.lat,
            longitude=args.lon, city=args.city)
        results["is_rest_period_now"] = {"resting": resting, "reason": why}

    if args.holidays:
        try:
            holidays = get_holidays(args.holidays)
            results["holidays"] = holidays
            results["yom_tov_count"] = len(
                [h for h in holidays if h.get("yomtov", False)])
        except Exception as e:
            results["holidays_error"] = str(e)

    if args.is_business_day or args.next_slot:
        try:
            # Load this year AND the next: --next-slot searches 60 days
            # forward, so a December query crosses into a year the cache
            # would otherwise be blind to.
            holidays_cache = (get_holidays(check_date.year) +
                              get_holidays(check_date.year + 1))
        except Exception:
            holidays_cache = None

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]

        if args.is_business_day:
            status, reason = classify_day(check_date.date(), holidays_cache,
                                          jerusalem=jerusalem)
            results["business_day_check"] = {
                "date": check_date.strftime("%Y-%m-%d"),
                "day": day_names[check_date.weekday()],
                "status": status,
                "reason": reason,
                "is_business_day": status != "closed",
            }

        if args.next_slot:
            results["next_available_slot"] = find_next_available_slot(
                check_date, duration_minutes=args.duration,
                holidays_cache=holidays_cache, jerusalem=jerusalem)

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
