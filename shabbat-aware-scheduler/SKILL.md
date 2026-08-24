---
name: shabbat-aware-scheduler
description: Schedule meetings, deployments, and events respecting Shabbat, Israeli holidays (chagim), and Hebrew calendar constraints. Use when user asks to schedule around Shabbat, "zmanim", check Israeli holidays, plan around chagim, set Israeli business hours, or needs Hebrew calendar-aware scheduling logic. Includes halachic times (zmanim) via HebCal API, full Israeli holiday calendar, and Israeli business hour conventions. Do NOT use for religious halachic rulings (consult a rabbi) or diaspora 2-day holiday scheduling.
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*) Bash(curl:*)
compatibility: Network required for HebCal API calls. Works offline with pre-cached holiday data. Python recommended.
---

# Shabbat-Aware Scheduler

This tool computes calendar times and business scheduling only. It does not issue halachic rulings; for halachic questions consult a rabbi.

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
**Prefer `geonameid` over raw coordinates.** When you pass a geonameid, Hebcal applies that
city's own candle-lighting minhag for you and there is no `b=` value to get wrong. Reach for
latitude/longitude plus a hand-picked `b=` only for a location with no geonameid.

```python
import requests
from datetime import datetime, timedelta

CITY_GEONAMEID = {
    "jerusalem": 281184, "tel_aviv": 293397, "haifa": 294801,
    "beersheba": 295530, "tiberias": 293322, "safed": 293100,
}

def get_shabbat_times(date=None, geonameid=281184):
    """Candle lighting and havdalah for the Shabbat of the week containing `date`."""
    if date is None:
        date = datetime.now()

    # Anchor on the Friday of the CURRENT Shabbat week. Saturday belongs to the
    # Shabbat that started the evening before, so it looks BACK one day. Adding
    # (4 - weekday) % 7 unconditionally returns next week's Shabbat all Saturday,
    # which is 8 days wrong exactly when someone asks "when does Shabbat end?".
    if date.weekday() == 5:
        friday = date - timedelta(days=1)
    else:
        friday = date + timedelta(days=(4 - date.weekday()) % 7)

    response = requests.get("https://www.hebcal.com/shabbat", params={
        "cfg": "json",
        "gy": friday.year, "gm": friday.month, "gd": friday.day,
        "geonameid": geonameid,
        "M": "on",    # Havdalah at tzeit hakochavim (sun 8.5 deg below horizon)
        # Alternative: m=50 or m=72 for a fixed number of minutes after sunset
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

Hebcal's `b=` default is 18 minutes before sunset, 40 for Jerusalem and 30 for Haifa and
Zikhron Ya'akov, and the same offset governs Erev Chag (Rosh Hashana, Yom Kippur, Sukkot,
Shmini Atzeret, Simchat Torah, Pesach, Shavuot), not only Erev Shabbat.

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
        "mf": "on",    # Minor fasts. WITHOUT this, Tzom Gedaliah, Asara
                       # B'Tevet, Ta'anit Esther, Ta'anit Bechorot and
                       # Tzom Tammuz are absent from the response entirely.
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

# Days the country does not work that Hebcal reports with yomtov=false.
# Filtering on yomtov alone marks every one of these an ordinary business day.
CLOSED_OBSERVANCES = {
    "Yom HaAtzma'ut": "closed",   "Yom HaZikaron": "closed",
    "Tish'a B'Av": "reduced",     "Erev Yom Kippur": "reduced",
    "Erev Rosh Hashana": "reduced", "Erev Pesach": "reduced",
    "Erev Sukkot": "reduced",     "Erev Shavuot": "reduced",
}
JERUSALEM_ONLY = {"Shushan Purim"}   # walled cities only

def _norm(title):
    # Hebcal emits typographic apostrophes, so "Yom HaAtzma\u2019ut" never matches
    # an ASCII-keyed table. This one character is the whole bug.
    return title.replace("\u2019", "'").strip()

def classify_day(date, holidays_cache=None, jerusalem=False):
    """Return (status, reason).

    closed         Shabbat, Yom Tov, or a national shutdown day
    reduced        morning only (erev chag, fast day)
    evening_closed a full working day whose EVENING is restricted: eve of
                   Yom HaZikaron, Yom HaShoah, Tisha B'Av. Distinct from
                   reduced on purpose, or the morning-only clamp would
                   block an ordinary Monday afternoon.
    open           ordinary business day
    """
    if date.weekday() == 5:
        return "closed", "Shabbat"
    if not holidays_cache:
        return "open", "Business day (no holiday data loaded)"

    date_str = date.strftime("%Y-%m-%d")
    status, reason = "open", "Business day"
    for h in holidays_cache:
        if not h["date"].startswith(date_str):
            continue
        title = _norm(h["title"])
        if h.get("yomtov", False):
            return "closed", f"Yom Tov: {title}"
        if title in JERUSALEM_ONLY:
            if jerusalem:
                return "closed", f"{title} (Jerusalem and walled cities)"
            continue
        level = CLOSED_OBSERVANCES.get(title)
        if level == "closed":
            return "closed", title
        if level == "reduced" and status == "open":
            status, reason = "reduced", f"{title} (morning only)"
    return status, reason
```

Chol ha-moed classifies as `open`: it is a legal workday in Israel, though staffing is thin.
Resolve every other ambiguity toward `closed`. Proposing a slot that turns out to be shut
costs a rescheduled meeting; missing a closure costs the meeting itself.

### Step 4: Holiday-Aware Cron Jobs

**A date check is not a time check.** `classify_day()` answers a question about a calendar
DATE. Shabbat and Yom Tov begin at candle-lighting the evening BEFORE, so Friday is a business
date while Friday 19:00 is already Shabbat. Anything that fires at a specific moment (a cron, a
notification send, a deploy) must additionally test the live window, or it will run during
Shabbat every single week while reporting "Business day".

```python
def is_shabbat_now(now, times):
    """times = get_shabbat_times(now). Fail closed if the API is unreachable."""
    start = datetime.fromisoformat(times["candle_lighting"])
    end = datetime.fromisoformat(times["havdalah"])
    return start <= now <= end
```

```python
def should_run_today(holidays_cache=None, skip_friday=False, skip_erev_chag=False,
                     now=None, jerusalem=False, time_aware=True, rest_kwargs=None):
    """Determine if a scheduled job should run RIGHT NOW.

    rest_kwargs is passed to the live-window check (geonameid, or city and
    coordinates). Omitting it evaluates the window for Jerusalem, which is
    22 minutes early for a Tel Aviv caller.
    """
    today = datetime.now(IL_TZ).date()

    # Never run on Shabbat -- the live window, not just the weekday
    if is_shabbat_now(datetime.now(IL_TZ), get_shabbat_times()):
        return False, "Shabbat in progress"
    if today.weekday() == 5:
        return False, "Shabbat"

    # Check holidays
    if holidays_cache:
        date_str = today.strftime("%Y-%m-%d")
        status, reason = classify_day(today, holidays_cache)
        if status == "closed":
            return False, reason

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
| Shushan Purim | 15 Adar (day after Purim) | Jerusalem and other historically walled cities only. A national workday, a citywide day off in Jerusalem |
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
| Rosh Hashana | September 11 to September 13, 2026 | Day one falls ON Shabbat (Sat Sep 12) rather than beside it, so the closed span is two days, Sat and Sun, entered at Friday-evening candle lighting |
| Yom Kippur | September 20 to September 21, 2026 (evening to evening) | Country shuts down |
| Sukkot | September 25 to October 2, 2026 | Erev Sukkot is Sep 25; the only Yom Tov is Sukkot I on Sep 26. Sep 27 to Oct 2 is chol ha-moed, including Hoshana Raba on Oct 2, which is a workday |
| Shmini Atzeret (Simchat Torah in Israel) | October 2 to October 3, 2026 | The closing Yom Tov of the Sukkot cycle, one day in Israel. Falls on Shabbat, Oct 3 |
| Purim / Shushan Purim | March 3 and March 4, 2026 | Purim nationally on Mar 3; Shushan Purim on Mar 4 is observed in Jerusalem and walled cities only |

Dates verified against Hebcal 2026 (Israeli observance). Always re-check the calendar each year; the Hebrew calendar slides against the Gregorian by 11 to 19 days. In 2026 Yom HaAtzmaut falls on its natural date, 5 Iyyar 5786 (April 21 to 22), with no postponement. In other years it can be moved earlier or postponed when it, or Yom HaZikaron which always precedes it, would conflict with Shabbat, so never compute 5 Iyyar directly.

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
- `scripts/check_shabbat.py`: standalone utility to query Shabbat times, Israeli holidays, and business-day status via the Hebcal API. Classifies any date as closed / reduced / open (covering the non-Yom-Tov national closures and Jerusalem's Shushan Purim), offers a time-aware `--is-rest-period-now` check for crons that covers Yom Tov onset as well as Shabbat, and finds the next available Israeli business slot honouring the time of day you searched from. Run: `python scripts/check_shabbat.py --help`

### References
- `references/domain-checklist.md`: the coverage contract for this skill. Lists every Israeli calendar scheduling constraint the skill must handle, split per varying dimension (city minhag, havdalah convention, Yom Tov vs chol ha-moed, non-Yom-Tov national closures, city-dependent observances, erev half-days, DST, leap years, postponement rules), with a cited source per row.
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
- Yom HaAtzmaut and Yom HaZikaron can be postponed (nidcheh) when their natural date would conflict with Shabbat. In 2026 no shift applies (5 Iyyar 5786 falls on April 21 to 22). Always read the date back from Hebcal rather than computing 5 Iyyar directly. Hebcal applies the postponement itself; `i=on` is a separate flag that selects Israeli one-day Yom Tov and is not what performs the shift.
- Havdalah default in Hebcal is Tzeit HaKochavim (sun 8.5 degrees below the horizon). Measured against Hebcal's own zmanim endpoint for Jerusalem that is roughly 37 minutes after sunset in late summer and 39 to 40 minutes in midwinter, NOT the 50 minutes often quoted. Stricter Rabbeinu Tam observers use 72 minutes. Pick the right `m=` value if your audience is not the default.
- Hebcal marks only Yom Tov with `yomtov: true`. Yom HaAtzma'ut, Yom HaZikaron, Erev Yom Kippur, Tisha B'Av and every erev chag come back `yomtov: false`, so a filter written as `if h["yomtov"]` treats Independence Day as an ordinary Wednesday. Match on the title as well, and note that Hebcal writes those titles with a typographic apostrophe (`Yom HaAtzma\u2019ut`), so an ASCII-keyed lookup silently never fires.
- Minor fast days are invisible unless you pass `mf=on`. The `maj` / `min` / `mod` flags do NOT return Tzom Gedaliah, Asara B'Tevet, Ta'anit Esther, Ta'anit Bechorot or Tzom Tammuz. Tzom Gedaliah lands the day after Rosh Hashana, exactly when someone schedules the catch-up meeting.
- Fail CLOSED when the calendar data is missing. Hebcal is rate-limited at 90 requests per 10 seconds, and a scheduler that answers "business day" on a 429 will book a meeting on Yom Kippur. Treat an empty holiday cache as unknown-and-therefore-closed, never as open.
- Erev status should be DERIVED ("the next day carries `yomtov: true`"), not enumerated from a hardcoded list. A fixed list misses cases like Hoshana Raba, which is erev Shmini Atzeret in every year.
- Shushan Purim (15 Adar) is a full holiday in Jerusalem and other historically walled cities and a normal workday everywhere else. A national scheduler must not block it; a Jerusalem scheduler must not ignore it. This is the only Israeli observance whose status depends on the city rather than the date.
- Israel's daylight-saving rule is its own: DST starts on the FRIDAY before the last Sunday of March and ends on the last Sunday of October, so it matches neither the US nor the EU transition. In 2026 that is 27 March and 25 October. Both shifts move Friday candle-lighting by an hour in wall-clock terms, and the October end is the sharper trap because Shabbat suddenly starts an hour earlier. Rely on the `Asia/Jerusalem` tz database rather than a hardcoded offset.
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
Cause: Mixing `M=on` (Tzeit HaKochavim, sun 8.5 degrees below the horizon, measured at 37 to 40 minutes after sunset in Jerusalem across the year) with a hardcoded "42 minutes" or "72 minutes" assumption.
Solution: Pick one method explicitly. `M=on` is Hebcal's tzeit hakochavim (sun 8.5 degrees below the horizon, three small stars visible). `m=N` is instead a FIXED N minutes after sundown, so `m=50` and `m=72` are minute counts, not star counts. Document which one your scheduler uses so downstream agents do not double-shift.

### Error: "Meeting booked on Yom HaAtzmaut / Tisha B'Av / erev chag"
Cause: filtering the Hebcal feed on `yomtov == true` only. Verified against the 2026 Israeli feed: Yom HaZikaron (21 Apr), Yom HaAtzma'ut (22 Apr), Erev Yom Kippur (20 Sep) and Tisha B'Av (23 Jul) all return `yomtov: false`.
Solution: classify on the title as well as the flag, and normalize the typographic apostrophe first. See `classify_day()` in `scripts/check_shabbat.py`.

### Error: "Cron fired at 19:30 on Friday, during Shabbat"
Cause: the guard tested the weekday, and Friday is a business date until candle-lighting.
Solution: compare the current moment against the candle-lighting-to-havdalah window returned by Hebcal (`is_shabbat_now()`), and fail closed on the weekend if the API is unreachable.