# Flight Comparison Workflow Script

This is a reference workflow for AI agents to follow when helping users compare flights from Israel.

## Input Parameters

- **Origin**: Ben Gurion Airport (TLV) by default
- **Destination**: Specific city or "anywhere/cheapest"
- **Dates**: Specific dates or flexible ("cheapest month")
- **Passengers**: Number of travelers
- **Baggage needs**: Carry-on only or checked bags needed
- **Preferences**: Direct flights only, specific airline, budget limit

## Comparison Workflow

### Step 1: Gather Requirements
Ask the user:
1. Where do you want to fly? (or "anywhere cheap")
2. When? (specific dates or flexible)
3. How many passengers?
4. Do you need checked baggage?
5. Any airline preference?
6. Budget limit in NIS?

### Step 2: Platform Search Order
1. Google Flights (google.com/travel/flights?gl=IL&hl=he) -- best for direct prices
2. Skyscanner (skyscanner.co.il) -- catches OTA deals
3. Issta (issta.co.il) -- check package deals if hotel also needed
4. KAYAK (il.kayak.com) -- for price prediction

### Step 3: Calculate Total Cost
For each option found:
- Base fare
- + Checked baggage fee (if needed)
- + Seat selection (if desired)
- + Any add-ons
- = Total cost per person

### Step 4: Present Comparison
Format results as:

| Option | Airline | Route | Total (NIS) | Bags Included | Notes |
|--------|---------|-------|-------------|---------------|-------|
| 1 | ... | ... | ... | ... | ... |

### Step 5: Recommend
- Cheapest overall (including bags)
- Best value (price vs convenience balance)
- Best for families (most generous baggage)

## Seasonal Advice
- If traveling during Jewish holidays: warn about price spikes, suggest booking 6+ weeks ahead
- If flexible on dates: suggest cheapest month (January) or shoulder seasons
- If budget is tight: suggest Wizz Air for European routes (but warn about add-on costs)
