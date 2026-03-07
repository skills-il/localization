---
name: gws-shabbat-calendar
description: >-
  Automate Google Calendar scheduling with Shabbat and Jewish holiday awareness
  using the Google Workspace CLI (gws). Use when user asks to create events that
  respect Shabbat boundaries, view Israeli workweek agenda (Sun-Thu), block
  focus time with Erev Shabbat cutoff, find free slots excluding Jewish
  holidays, or manage recurring events on Israeli workweek patterns. Uses gws
  calendar insert, gws calendar agenda, and related recipes. Do NOT use for
  non-Google calendar systems (Outlook, Apple Calendar) or religious halachic
  rulings about exact Shabbat times (consult a rabbi for those).
license: MIT
allowed-tools: 'Bash(npx:*) Bash(gws:*) Bash(node:*) Bash(curl:*) Bash(python:*)'
compatibility: >-
  Requires Node.js 18+ and the Google Workspace CLI (@google/gws). Network
  required for Google Calendar API and HebCal holiday lookups. Works with any
  Google Workspace or personal Gmail account.
metadata:
  author: choroshin
  version: 1.0.0
  category: localization
  tags:
    he:
      - גוגל-וורקספייס
      - גוגל-קלנדר
      - שבת
      - חגים
      - תזמון
      - ישראל
    en:
      - google-workspace
      - google-calendar
      - shabbat
      - jewish-holidays
      - scheduling
      - israel
  display_name:
    he: יומן שבת עם GWS
    en: GWS Shabbat Calendar
  display_description:
    he: >-
      אוטומציית תזמון יומן גוגל עם מודעות לשבת וחגים באמצעות Google Workspace
      CLI -- בדיקת גבולות, תבניות שבוע עבודה ישראלי ותזמון בטוח מחגים.
    en: >-
      Automate Google Calendar scheduling with Shabbat and Jewish holiday
      awareness using the Google Workspace CLI -- boundary checks, Israeli
      workweek patterns, and holiday-safe scheduling.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# GWS Shabbat Calendar

## Instructions

### Step 1: Verify GWS CLI Setup

Before scheduling, confirm the Google Workspace CLI is installed and authenticated.

```bash
# Install gws globally (or use npx)
npm install -g @google/gws

# Authenticate with Google account
gws auth login

# Verify authentication
gws auth status
```

If the user has not authenticated, guide them through `gws auth login` first. For project-level configuration (service accounts, workspace domain), use `gws auth setup`.

### Step 2: Determine Scheduling Context

Identify what the user needs and which constraints apply.

| Context | Key Constraints | GWS Command |
|---------|----------------|-------------|
| Create single event | Shabbat boundary check, holiday check | `gws calendar insert` |
| View weekly agenda | Israeli workweek (Sun-Thu) filter | `gws calendar agenda` |
| Block focus time | Erev Shabbat cutoff (Friday 14:00) | `gws calendar insert` (recurring) |
| Find free slots | Exclude Shabbat + holidays | `gws calendar agenda` + gap analysis |
| Recurring meetings | Israeli workweek pattern (Sun-Thu) | `gws calendar insert --recurrence` |
| Batch invites | Multi-attendee with timezone awareness | batch-event-invites recipe |
| Reschedule meeting | Holiday conflict resolution | reschedule-meeting recipe |
| Cross-timezone | Israel/US overlap with Shabbat guard | `gws calendar insert` + timezone math |

### Step 3: Fetch Jewish Calendar Data

Before creating or modifying events, check for Shabbat times and upcoming holidays using the HebCal API. Use `scripts/check_holidays.py` for programmatic lookups.

**Shabbat times for a specific date:**
```bash
curl -s "https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data.get('items', []):
    cat = item.get('category', '')
    if cat in ('candles', 'havdalah'):
        print(f\"{cat}: {item['date']}\")
"
```

**Holiday lookup for date range:**
```bash
# Check holidays for a given month (YYYY-MM format)
python3 scripts/check_holidays.py --month 2026-09
```

**Key reference data (see `references/jewish-calendar-reference.md`):**

| Holiday | Hebrew | Duration | Scheduling Impact |
|---------|--------|----------|-------------------|
| Shabbat | שבת | Weekly (Fri sunset - Sat sunset) | No events after Friday 14:00 |
| Rosh Hashana | ראש השנה | 2 days (Tishrei 1-2) | Full block |
| Yom Kippur | יום כיפור | 1 day (Tishrei 10) | Full block, no work Erev YK afternoon |
| Sukkot | סוכות | 7+1 days | First/last days full block, Chol HaMoed partial |
| Pesach | פסח | 7 days | First/last days full block, Chol HaMoed partial |
| Shavuot | שבועות | 1 day | Full block |
| Yom HaZikaron | יום הזיכרון | 1 day | National memorial, reduced scheduling |
| Yom HaShoah | יום השואה | 1 day | National memorial, reduced scheduling |

**Israeli business conventions:**
- Workweek: Sunday through Thursday
- Friday: half-day, most offices close by 13:00-14:00
- Erev Chag (holiday eve): offices close early, typically by 13:00
- Timezone: `Asia/Jerusalem` (UTC+2 winter / UTC+3 summer, IST/IDT)

### Step 4: Create Events with Shabbat Boundary Checks

Always validate event timing against Shabbat and holiday boundaries before inserting.

**Single event creation with boundary check:**
```bash
# Step 1: Check if the requested time conflicts with Shabbat
python3 scripts/check_holidays.py --date 2026-03-13

# Step 2: If clear, create the event
gws calendar insert \
  --summary "Sprint Planning" \
  --start "2026-03-11T10:00:00" \
  --end "2026-03-11T11:00:00" \
  --timezone "Asia/Jerusalem" \
  --description "Weekly sprint planning session" \
  --attendees "team@company.co.il"
```

**Friday event with automatic cutoff enforcement:**
```bash
# For Friday events, enforce 14:00 cutoff
# Calculate: if end_time > Friday 14:00 IST, reject or adjust
gws calendar insert \
  --summary "Quick sync" \
  --start "2026-03-13T11:00:00" \
  --end "2026-03-13T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --description "Pre-weekend sync (ends before Erev Shabbat cutoff)"
```

**Dry-run mode for validation:**
```bash
gws calendar insert \
  --summary "Team meeting" \
  --start "2026-03-11T14:00:00" \
  --end "2026-03-11T15:00:00" \
  --timezone "Asia/Jerusalem" \
  --dry-run
```

### Step 5: View Israeli Workweek Agenda

Filter agenda output to show only Israeli business days (Sunday through Thursday).

**Weekly agenda for Israeli workweek:**
```bash
# Get this week's agenda (Sun-Thu only)
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-12" \
  --timezone "Asia/Jerusalem"
```

**Filter and format with holiday annotations:**
```bash
# Get agenda and annotate holidays
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-14" \
  --timezone "Asia/Jerusalem" \
  --output json | python3 -c "
import json, sys
from datetime import datetime

events = json.load(sys.stdin)
for e in events:
    start = datetime.fromisoformat(e['start']['dateTime'])
    day = start.weekday()
    # Filter: 6=Sun, 0=Mon, 1=Tue, 2=Wed, 3=Thu (Israeli workweek)
    if day in (6, 0, 1, 2, 3):
        print(f\"{start.strftime('%a %d/%m %H:%M')} - {e['summary']}\")
"
```

### Step 6: Block Focus Time with Erev Shabbat Awareness

Create recurring focus time blocks that respect Friday cutoffs.

**Block daily focus time (Sun-Thu, 09:00-12:00):**
```bash
gws calendar insert \
  --summary "Focus Time (Do Not Disturb)" \
  --start "2026-03-08T09:00:00" \
  --end "2026-03-08T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --visibility private \
  --description "Protected deep work time. Auto-scheduled by GWS Shabbat Calendar."
```

**Friday-specific short focus block (ends before 13:00):**
```bash
gws calendar insert \
  --summary "Friday Focus (Short)" \
  --start "2026-03-13T09:00:00" \
  --end "2026-03-13T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=FR" \
  --visibility private \
  --description "Short Friday focus block, ends before Erev Shabbat."
```

### Step 7: Find Free Slots Excluding Holidays

Analyze calendar gaps while filtering out Shabbat and holiday periods.

```bash
# Step 1: Get existing events for the week
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-12" \
  --timezone "Asia/Jerusalem" \
  --output json > /tmp/week_events.json

# Step 2: Find free slots using the helper script
python3 scripts/find_free_slots.py \
  --events /tmp/week_events.json \
  --work-start 09:00 \
  --work-end 18:00 \
  --friday-end 14:00 \
  --duration 60 \
  --exclude-holidays
```

**Cross-timezone free slot finder (Israel + US East):**
```bash
python3 scripts/find_free_slots.py \
  --events /tmp/week_events.json \
  --work-start 09:00 \
  --work-end 18:00 \
  --friday-end 14:00 \
  --duration 60 \
  --overlap-tz "America/New_York" \
  --overlap-start 09:00 \
  --overlap-end 17:00 \
  --exclude-holidays
```

### Step 8: Manage Recurring Events on Israeli Patterns

Set up recurring events that follow the Israeli workweek and auto-skip holidays.

**Recurring standup (Sun-Thu at 09:30):**
```bash
gws calendar insert \
  --summary "Daily Standup" \
  --start "2026-03-08T09:30:00" \
  --end "2026-03-08T09:45:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --attendees "dev-team@company.co.il" \
  --description "Daily standup. Israeli workweek schedule (Sun-Thu)."
```

**To handle holiday conflicts with recurring events:**
1. Fetch upcoming holidays: `python3 scripts/check_holidays.py --range 2026-03-01 2026-04-01`
2. Identify conflicts with the recurring schedule
3. Use the reschedule-meeting recipe to move conflicting occurrences:
```bash
# Reschedule a specific occurrence that falls on a holiday
gws calendar update \
  --event-id "EVENT_ID" \
  --start "2026-03-15T09:30:00" \
  --end "2026-03-15T09:45:00" \
  --timezone "Asia/Jerusalem"
```

### Step 9: Batch Operations and Advanced Recipes

**Batch event creation from a schedule file:**
```bash
# Create multiple events from a JSON schedule
# See references/gws-calendar-recipes.md for the batch format
gws calendar insert --batch schedule.json --dry-run
```

**Weekly schedule report:**
```bash
# Generate a formatted weekly report
gws calendar agenda \
  --from "$(date -v-sun +%Y-%m-%d)" \
  --to "$(date -v+thu +%Y-%m-%d)" \
  --timezone "Asia/Jerusalem" \
  --output json | python3 -c "
import json, sys
events = json.load(sys.stdin)
print(f'Total events this week: {len(events)}')
for e in events:
    print(f\"  - {e.get('start',{}).get('dateTime','')[:16]} {e['summary']}\")
"
```

## Examples

### Example 1: Schedule a Team Meeting Respecting Shabbat

User says: "Schedule a 1-hour team meeting for next Wednesday at 14:00 Israel time with the backend team"

Actions:
1. Check Wednesday date against Jewish calendar: `python3 scripts/check_holidays.py --date 2026-03-11`
2. Confirm no holiday conflict (Wednesday is a regular Israeli workday)
3. Create the event:
```bash
gws calendar insert \
  --summary "Backend Team Meeting" \
  --start "2026-03-11T14:00:00" \
  --end "2026-03-11T15:00:00" \
  --timezone "Asia/Jerusalem" \
  --attendees "backend-team@company.co.il" \
  --description "Weekly backend sync"
```
Result: Event created on Wednesday 14:00 IST, no Shabbat or holiday conflicts.

### Example 2: Find Meeting Slots Across Israel/US Timezones

User says: "Find available 30-minute slots this week for a call with our New York team, avoiding Shabbat and holidays"

Actions:
1. Fetch this week's agenda: `gws calendar agenda --from 2026-03-08 --to 2026-03-12 --timezone "Asia/Jerusalem" --output json > /tmp/week.json`
2. Run cross-timezone slot finder:
```bash
python3 scripts/find_free_slots.py \
  --events /tmp/week.json \
  --work-start 09:00 --work-end 18:00 --friday-end 14:00 \
  --duration 30 \
  --overlap-tz "America/New_York" --overlap-start 09:00 --overlap-end 17:00 \
  --exclude-holidays
```
3. Present available overlapping slots (typically 16:00-18:00 IST / 09:00-11:00 EST on Sun-Thu)
Result: List of free slots where both Israel and New York teams are available during business hours, with Shabbat and holidays excluded.

### Example 3: Set Up Recurring Sun-Thu Standups with Holiday Auto-Check

User says: "Create a daily 15-minute standup at 09:30 for the dev team, Sunday through Thursday, and check if any upcoming holidays conflict"

Actions:
1. Create the recurring event:
```bash
gws calendar insert \
  --summary "Dev Team Standup" \
  --start "2026-03-08T09:30:00" \
  --end "2026-03-08T09:45:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --attendees "dev-team@company.co.il"
```
2. Check upcoming holidays for the next 30 days: `python3 scripts/check_holidays.py --range 2026-03-08 2026-04-08`
3. Report any conflicts and offer to add exceptions for those dates
Result: Recurring standup created for Sun-Thu. User informed of upcoming Pesach dates that will need manual cancellation or rescheduling.

## Bundled Resources

### Scripts
- `scripts/check_holidays.py` -- Query HebCal API for Shabbat times and Jewish holidays. Run: `python3 scripts/check_holidays.py --help`
- `scripts/find_free_slots.py` -- Find available meeting slots excluding Shabbat, holidays, and existing events. Supports cross-timezone overlap. Run: `python3 scripts/find_free_slots.py --help`

### References
- `references/jewish-calendar-reference.md` -- Complete reference for Jewish holidays, Israeli business conventions, and Shabbat scheduling rules. Consult when determining which dates are blocked or have reduced hours.
- `references/gws-calendar-recipes.md` -- Google Workspace CLI calendar command reference and advanced recipes. Consult when constructing gws calendar commands, batch operations, or recurrence rules.

## Troubleshooting

### Error: "gws: command not found"
Cause: The Google Workspace CLI is not installed or not in PATH.
Solution: Install with `npm install -g @google/gws` or use `npx @google/gws calendar ...` for one-off commands. Verify with `gws --version`.

### Error: "Not authenticated" or "Token expired"
Cause: The OAuth token has expired or the user has not logged in.
Solution: Run `gws auth login` to re-authenticate. For service accounts, run `gws auth setup` and provide the credentials JSON file.

### Error: "Event conflicts with Shabbat boundary"
Cause: The requested event time falls after Friday 14:00 or during Shabbat (Friday sunset to Saturday sunset).
Solution: Move the event to before Friday 14:00, or to Sunday-Thursday. Use `python3 scripts/check_holidays.py --date YYYY-MM-DD` to verify the exact Shabbat candle-lighting time for that week.

### Error: "Holiday data unavailable" or HebCal API timeout
Cause: Network issue or HebCal API is temporarily unavailable.
Solution: The `scripts/check_holidays.py` script caches results locally. For offline use, consult `references/jewish-calendar-reference.md` for fixed holiday dates. Note that Hebrew calendar dates shift in the Gregorian calendar each year.

### Error: "No overlapping slots found" for cross-timezone scheduling
Cause: The Israel/US business hour overlap window is too narrow (typically 3-4 hours) combined with existing events.
Solution: Expand the search range to multiple days. Consider earlier US start times or later Israel times. Use `--duration` flag with a shorter meeting length (e.g., 15 or 20 minutes).
