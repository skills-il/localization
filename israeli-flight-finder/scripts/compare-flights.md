# Flight Comparison Workflow Script

Reference workflow for an AI agent helping a user compare flights from Israel. The goal is a REAL comparison with live fares, not a list of websites. If live fares cannot be read, the agent hands over pre-filled search links instead of inventing numbers.

## Input Parameters

- **Origin**: Ben Gurion Airport (TLV) by default
- **Destination**: Specific city / airport code, or "anywhere / cheapest"
- **Dates**: Specific dates, or flexible ("cheapest month")
- **Passengers**: Number of travelers
- **Baggage needs**: Carry-on only, or checked bags needed
- **Preferences**: Nonstop only, specific airline, budget ceiling

## Comparison Workflow

### Step 1: Gather Requirements
Assume TLV as origin; ask only for what is missing:
1. Where to (or "anywhere cheap")?
2. When (specific dates or a flexible month)?
3. How many passengers?
4. Checked baggage needed, or carry-on only?
5. Nonstop only, or connections OK?
6. Airline preference or budget ceiling?

### Step 2: Build Pre-Filled Search Links
Substitute the destination and dates into the verified templates (see `references/comparison-platforms.md`):
- Google Flights: `https://www.google.com/travel/flights?q=Flights+from+TLV+to+{CITY}+on+{YYYY-MM-DD}+returning+{YYYY-MM-DD}&curr=ILS&gl=IL&hl=he`
- Skyscanner: `https://www.skyscanner.co.il/transport/flights/tlv/{dest}/{YYMMDD}/{YYMMDD}/` (whole month = `{YYMM}00`; anywhere = `tlv/anywhere/{YYMMDD}/`)
- KAYAK: `https://il.kayak.com/flights/TLV-{DEST}/{YYYY-MM-DD}/{YYYY-MM-DD}?sort=price_a`

### Step 3: Pull the Live Fares
Open each link and read the top 3-5 results: airline, price in shekels, stops, total duration, times.
- Use a real browser tool (or flights MCP) for Google Flights and Skyscanner (JavaScript-rendered).
- KAYAK and the Google Flights natural-language query are the most fetch-friendly if only `WebFetch` is available.
- Cross-check at least two platforms; the same route often differs by hundreds of NIS.

### Step 4: Calculate Total Cost
For each option found:
- Base fare
- + Checked baggage fee (if needed) -- from the Israeli-airline baggage tables
- + Seat selection (if desired)
- = Total cost per person
- El Al includes a bag on Classic and up; Israir, Arkia, and Wizz charge for almost everything, so a low base fare often loses once a 23 kg bag is added.

### Step 5: Present Comparison
Format the REAL fares, cheapest total first:

| Option | Airline | Route / Stops | Base (NIS) | Bags (NIS) | Total (NIS) | Notes |
|--------|---------|---------------|-----------|-----------|------------|-------|
| 1 | ... | ... | ... | ... | ... | ... |

### Step 6: Recommend
- Cheapest overall (including bags)
- Best value (price vs. stops and timing)
- Best for families (most generous baggage)
Include the Step 2 links so the user can book or re-check the live price.

## Never Invent a Price
Every number in the table must come from a page loaded this session. If live prices cannot be read (no web/browser access, bot-block, or captcha), do NOT write numbers -- hand over the pre-filled Step 2 links and say plainly they open live results, because you could not read the fares this turn. A fabricated comparison is worse than none.

## Seasonal Advice
- Jewish holidays: warn about price spikes (they front-load 2-4 weeks before), suggest booking 6+ weeks ahead.
- Flexible on dates: use the Skyscanner whole-month view or Google Flights date grid to find the cheapest window (January and shoulder seasons are cheapest).
- Tight budget: check Wizz Air for European routes, but warn that add-on costs (bags, seats) erode the low base fare.
