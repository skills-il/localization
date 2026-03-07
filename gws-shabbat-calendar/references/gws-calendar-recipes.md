# Google Workspace CLI - Calendar Recipes Reference

## Installation and Authentication

### Install
```bash
npm install -g @google/gws
# or use npx for one-off commands
npx @google/gws calendar agenda
```

### Authentication
```bash
# Interactive OAuth login (personal or workspace account)
gws auth login

# Service account setup (for automation)
gws auth setup

# Check current auth status
gws auth status
```

## Core Calendar Commands

### gws calendar insert

Create a new calendar event.

```bash
gws calendar insert \
  --summary "Event Title" \
  --start "2026-03-11T10:00:00" \
  --end "2026-03-11T11:00:00" \
  --timezone "Asia/Jerusalem" \
  --description "Event description" \
  --location "Office, Tel Aviv" \
  --attendees "user1@company.co.il,user2@company.co.il" \
  --visibility "default" \
  --status "confirmed"
```

**Key flags:**

| Flag | Description | Example |
|------|-------------|---------|
| `--summary` | Event title | `"Sprint Planning"` |
| `--start` | Start time (ISO 8601) | `"2026-03-11T10:00:00"` |
| `--end` | End time (ISO 8601) | `"2026-03-11T11:00:00"` |
| `--timezone` | IANA timezone | `"Asia/Jerusalem"` |
| `--description` | Event description | `"Weekly sync"` |
| `--location` | Event location | `"Room 3, Floor 2"` |
| `--attendees` | Comma-separated emails | `"a@co.il,b@co.il"` |
| `--recurrence` | RRULE string | `"RRULE:FREQ=WEEKLY;BYDAY=MO"` |
| `--visibility` | default, public, private | `"private"` |
| `--calendar-id` | Target calendar | `"primary"` |
| `--dry-run` | Preview without creating | (no value) |
| `--output` | Output format | `"json"` |

### gws calendar agenda

View calendar events for a date range.

```bash
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-14" \
  --timezone "Asia/Jerusalem" \
  --output json
```

**Key flags:**

| Flag | Description | Example |
|------|-------------|---------|
| `--from` | Start date (YYYY-MM-DD) | `"2026-03-08"` |
| `--to` | End date (YYYY-MM-DD) | `"2026-03-14"` |
| `--timezone` | IANA timezone | `"Asia/Jerusalem"` |
| `--calendar-id` | Target calendar | `"primary"` |
| `--output` | Output format (json/text) | `"json"` |
| `--max-results` | Maximum events | `"50"` |

### gws calendar update

Update an existing event.

```bash
gws calendar update \
  --event-id "EVENT_ID" \
  --summary "Updated Title" \
  --start "2026-03-12T10:00:00" \
  --end "2026-03-12T11:00:00" \
  --timezone "Asia/Jerusalem"
```

### gws calendar delete

Delete a calendar event.

```bash
gws calendar delete --event-id "EVENT_ID"
```

## Recurrence Rules (RRULE)

### Israeli Workweek (Sun-Thu)
```
RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH
```

### Every Sunday and Wednesday
```
RRULE:FREQ=WEEKLY;BYDAY=SU,WE
```

### Monthly on first Sunday
```
RRULE:FREQ=MONTHLY;BYDAY=1SU
```

### Weekly with end date
```
RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH;UNTIL=20261231T235959Z
```

### Bi-weekly on Sunday
```
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=SU
```

### Day abbreviations
| Day | RRULE Code |
|-----|-----------|
| Sunday | SU |
| Monday | MO |
| Tuesday | TU |
| Wednesday | WE |
| Thursday | TH |
| Friday | FR |
| Saturday | SA |

## Recipes

### Block Focus Time
```bash
gws calendar insert \
  --summary "Focus Time" \
  --start "2026-03-08T09:00:00" \
  --end "2026-03-08T12:00:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH" \
  --visibility private \
  --description "Protected deep work time"
```

### Find Free Time
```bash
# Export agenda as JSON then analyze gaps
gws calendar agenda \
  --from "2026-03-08" \
  --to "2026-03-12" \
  --timezone "Asia/Jerusalem" \
  --output json > events.json
```

### Batch Event Invites
```json
[
  {
    "summary": "1:1 with Alice",
    "start": "2026-03-08T10:00:00",
    "end": "2026-03-08T10:30:00",
    "timezone": "Asia/Jerusalem",
    "attendees": ["alice@company.co.il"]
  },
  {
    "summary": "1:1 with Bob",
    "start": "2026-03-08T10:30:00",
    "end": "2026-03-08T11:00:00",
    "timezone": "Asia/Jerusalem",
    "attendees": ["bob@company.co.il"]
  }
]
```

```bash
gws calendar insert --batch schedule.json
```

### Reschedule Meeting
```bash
# Find the event
gws calendar agenda --from "2026-03-08" --to "2026-03-08" --output json

# Update with new time
gws calendar update \
  --event-id "FOUND_EVENT_ID" \
  --start "2026-03-09T10:00:00" \
  --end "2026-03-09T11:00:00" \
  --timezone "Asia/Jerusalem"
```

### Create Recurring Event with Exceptions
```bash
# Create the series
gws calendar insert \
  --summary "Team Meeting" \
  --start "2026-03-08T14:00:00" \
  --end "2026-03-08T15:00:00" \
  --timezone "Asia/Jerusalem" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=SU"

# Then delete specific occurrences that fall on holidays
gws calendar delete --event-id "EVENT_ID" --instance "2026-04-05T14:00:00+03:00"
```

## Output Parsing

### JSON Event Structure
```json
{
  "id": "abc123",
  "summary": "Event Title",
  "start": {
    "dateTime": "2026-03-08T10:00:00+02:00",
    "timeZone": "Asia/Jerusalem"
  },
  "end": {
    "dateTime": "2026-03-08T11:00:00+02:00",
    "timeZone": "Asia/Jerusalem"
  },
  "attendees": [
    {"email": "user@company.co.il", "responseStatus": "accepted"}
  ],
  "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH"],
  "status": "confirmed"
}
```

### Timezone Considerations

| Timezone | UTC Offset | When |
|----------|-----------|------|
| Asia/Jerusalem (IST) | UTC+2 | Winter (last Sun Oct - last Fri before Apr 2) |
| Asia/Jerusalem (IDT) | UTC+3 | Summer (last Fri before Apr 2 - last Sun Oct) |
| America/New_York (EST) | UTC-5 | Winter |
| America/New_York (EDT) | UTC-4 | Summer |
| America/Los_Angeles (PST) | UTC-8 | Winter |
| America/Los_Angeles (PDT) | UTC-7 | Summer |

### Israel-US Business Hour Overlap

| US Timezone | Israel Hours | US Hours | Overlap Window (IST) |
|-------------|-------------|----------|---------------------|
| ET (EST/EDT) | 09:00-18:00 | 09:00-17:00 | 16:00-18:00 (winter) / 16:00-18:00 (summer) |
| CT (CST/CDT) | 09:00-18:00 | 09:00-17:00 | 17:00-18:00 (narrow) |
| PT (PST/PDT) | 09:00-18:00 | 09:00-17:00 | Minimal direct overlap |
