---
name: israeli-flight-finder
description: "Compare flight prices from Ben Gurion Airport (TLV) across Google Flights, Skyscanner, KAYAK, and Israeli platforms like Issta and Lametayel. Use when a user asks about cheap flights from Israel, flight comparison, airline baggage policies, best time to book flights, or seasonal pricing from TLV. Covers El Al, Israir, Arkia, and low-cost carriers like Wizz Air. Helps users find the cheapest fares, understand Israeli airline baggage fees, and plan around peak and off-peak travel seasons. Do NOT use for domestic travel within Israel (use israeli-travel-planner), train schedules (use railil), or hotel-only bookings."
license: MIT
---

# Israeli Flight Finder

Find the cheapest flights from Ben Gurion Airport (TLV) by comparing prices across multiple platforms and understanding Israeli airline pricing patterns.

## Comparison Platforms

Use multiple platforms -- each has different strengths. Never rely on a single source.

| Platform | URL | Strengths | Hebrew UI |
|----------|-----|-----------|-----------|
| Google Flights | google.com/travel/flights?gl=IL&hl=he | AI-powered Flight Deals, price tracking, "Explore" map, fare history graphs | Yes |
| Skyscanner | skyscanner.co.il | Broadest coverage (1000+ providers), "Everywhere" search, monthly price calendar | Yes |
| KAYAK | il.kayak.com | Price alerts, fare forecasting, flexible date search | Yes |
| Issta | issta.co.il | Israeli travel agency, package deals (flight+hotel), Hebrew-first UX, physical branches | Yes |
| Lametayel | lametayel.co.il | Israeli comparison engine, aggregates Israeli operators, popular among Hebrew speakers | Yes |

### When to Use Which Platform

- **Cheapest fare overall**: Start with Google Flights (best for direct airline prices), then cross-check on Skyscanner (catches OTA deals Google misses).
- **Flexible destination** ("anywhere cheap"): Skyscanner "Everywhere" search or Google Flights "Explore" map.
- **Package deals (flight+hotel)**: Issta excels at bundled packages that save hundreds of NIS vs booking separately.
- **Hebrew-only users**: Issta and Lametayel have the best Hebrew UX. Google Flights and Skyscanner also have full Hebrew interfaces.
- **Price tracking**: Google Flights and KAYAK both offer email alerts when prices drop on tracked routes.

### Google Flights AI Flight Deals

Google Flights offers an AI-powered "Flight Deals" feature available in Israel in Hebrew. Users can describe what they want in natural language (e.g., "a one-week winter trip to a city with great food, direct flights only") and the tool suggests matching flights. Access it at google.com/travel/flights with locale set to Israel.

## Israeli Airlines

### El Al (LY) -- Flag Carrier

- **Hub**: Ben Gurion (TLV)
- **Network**: 51+ direct destinations worldwide
- **Website**: elal.com
- **Frequent flyer**: Matmid, with five tiers (Matmid base, Silver, Gold, Platinum, Top Platinum). Since April 2025, status is earned via a revenue-linked "Diamonds" currency and re-qualified every 12 months; the old soft-landing grace tier was eliminated, so under-qualifying members drop straight to the matching tier.

**Baggage policy:**

| Fare class | Carry-on | Checked bags |
|------------|----------|--------------|
| Economy Lite | 1 x 8 kg (56x45x25 cm) + 1 personal item | None included |
| Economy Classic | 1 x 8 kg + 1 personal item | 1 x 23 kg |
| Economy Flex | 1 x 8 kg + 1 personal item | 1 x 23 kg |
| Premium | 1 x 8 kg + 1 personal item | 2 x 23 kg |
| Business | 1 x 16 kg (56x45x25 cm) + 1 personal item | 2 x 32 kg |

**Economy Lite restriction (Europe/UAE)**: Since May 2025, Lite fare passengers on flights to/from Europe or the UAE must check their carry-on at the gate (free of charge). Only a personal item (max 38x30x18 cm) is allowed in the cabin. This does NOT apply to US routes or Classic/Flex fares. Matmid elite members (Gold+) are exempt.

**Matmid members**: Gold, Platinum, and Top Platinum get enhanced carry-on privileges.

### Israir (6H)

- **Hub**: Ben Gurion (TLV), Ramon Airport (Eilat)
- **Network**: ~49 international destinations (Europe, New York, India, Central Asia) + domestic (Eilat, Haifa)
- **Website**: israir.co.il
- **Fleet**: Transitioning to all-Airbus (A320/A330); A330s for long-haul (New York, Asia)

**Baggage policy (updated March 2026):**

| Item | Weight | Cost (advance) | Cost (airport) |
|------|--------|----------------|----------------|
| Personal item | Small bag (under seat) | Free | Free |
| Carry-on | 10 kg | $30 per direction | $40 |
| 1st checked bag | 23 kg | $60 per direction | $100 |
| Overweight (24-32 kg) | -- | +$20 per direction | +$70 |

Standard fares do not include checked baggage. Some vacation packages may bundle bags.

### Arkia (IZ)

- **Hub**: Ben Gurion (TLV), Ramon Airport (Eilat)
- **Network**: ~40 international destinations including New York, Bangkok, European cities, Greek islands
- **Website**: arkia.co.il
- **New for 2026**: Business class on select European routes (Paris first), plus Phuket, Malaga, Ibiza, Vilnius, Hanoi

**Baggage policy (international flights, verify on arkia.co.il):**

| Item | Weight | Cost (advance) | Cost (airport) |
|------|--------|----------------|----------------|
| Carry-on | 7 kg | Free | Free |
| Trolley bag | 8 kg | $20 | $25 / EUR 25 |
| Checked bag | 20 kg | $45 | $90 / EUR 85 |
| Excess per kg | -- | -- | $10 / EUR 10 |

### Low-Cost Carriers

**Wizz Air (W6)**: Hungarian low-cost carrier, now establishing a major base at Ben Gurion (and a secondary base at Ramon). First flight from the new base (Tel Aviv–Budapest) launched March 2026. The airline currently operates about 21 routes from Israel and plans to grow to roughly 50 routes, offering 1.7 million seats in 2026, making it the second-largest airline at TLV after El Al. Total investment: around $1 billion, dozens of new routes, A320-family aircraft. Only a small personal item (40x30x20 cm) is free on base fares; cabin bags and checked bags are paid add-ons. Check wizzair.com for current route status and baggage add-on pricing.

**Ryanair**: Has officially removed Tel Aviv from its route map. Cancelled 22 planned routes and roughly 1 million seats for the 2025-2026 season due to disputes with Ben Gurion Airport over slot allocation and Terminal 1 availability. As of early 2026, Ryanair has stated it will not resume TLV operations until at least summer 2026, conditional on the airport confirming S26 slots and Terminal 1 access.

### Foreign Carriers

- **flydubai**: Operates one of the densest schedules to TLV: about 10 daily Dubai–Tel Aviv flights as of late 2025, a >50% increase vs 2023. Often a strong option for connections to the Gulf, Asia, and East Africa via Dubai.
- **Emirates**: Has fully withdrawn all Tel Aviv flights. No planned return as of early 2026.
- **Turkish Airlines, American Airlines, Virgin Atlantic, Korean Air, Cathay Pacific**: Have not resumed TLV service since the October 2023 suspensions. Verify current status on each airline's site before relying on them.
- **European carriers** (Lufthansa Group, Air France-KLM, ITA, Iberia, Aegean, LOT, Wizz, easyJet, Pegasus, SunExpress, etc.): Most have resumed and expanded TLV service through 2025-2026. Availability by route fluctuates with security conditions, so always verify.

## Seasonal Pricing Guide

### Peak Periods (Most Expensive)

- **Jewish holidays**: Rosh Hashana, Sukkot, Pesach -- prices spike 2-4 weeks before
- **Summer** (July-August): School vacation, highest demand
- **Purim break** (March): Short but expensive window

### Shoulder Seasons (Moderate)

- **April-May** (between Pesach and summer): Good weather, moderate prices
- **September** (between summer and holidays): Brief window before Rosh Hashana
- **October-November** (after Sukkot): Prices drop rapidly

### Off-Peak (Cheapest)

- **January**: Cheapest month to fly from TLV
- **February** (excluding Purim): Low demand
- **November-December** (excluding Hanukkah): Winter low season

## Booking Strategies

### Timing

- **Book 15-30 days ahead for domestic, 31-45 days ahead for international**. Expedia's 2026 Air Hacks Report found these windows beat booking 6+ months in advance by about $130 (domestic) and $190 (international).
- **Friday is the cheapest day to BOOK** (Expedia 2026): up to 3% cheaper than Sunday, which is the most expensive day to book. This reverses the old "book on Tuesday" advice.
- **Friday is also a cheap day to FLY**: save roughly 14% on domestic and 8% on international vs flying on Sunday. Tuesday remains the least crowded flying day.
- Set price alerts on Google Flights or KAYAK for routes you're watching, then pounce when the fare dips below the "typical" band on the fare-history graph.

### Money-Saving Tips

1. **Compare across 3+ platforms**: Prices differ significantly between platforms for the same route
2. **Check package deals on Issta**: Flight+hotel bundles often beat booking separately by hundreds of NIS
3. **Use "Everywhere" search on Skyscanner**: Find the cheapest destination for your dates instead of picking a destination first
4. **Consider nearby airports**: For European destinations, flying to a nearby city and taking a train can be cheaper (e.g., fly to Bergamo instead of Milan)
5. **Book baggage in advance**: All Israeli airlines charge significantly more for baggage purchased at the airport vs online in advance
6. **Check Wizz Air for European routes**: Low-cost fares start very low but add-ons (bags, seats) add up -- compare total cost including bags
7. **Flexible dates**: Shifting departure by 1-2 days can save 30%+ on the same route

### Flight+Hotel Packages

Israeli travel agencies (Issta, Lametayel) specialize in package deals that bundle flights and hotels. These can be significantly cheaper than booking separately, especially for popular destinations like Greece, Cyprus, Turkey, and European cities.

## How to Search

### Step-by-Step: Finding the Cheapest Flight

1. **Start with Google Flights** (google.com/travel/flights?gl=IL&hl=he):
   - Enter origin (TLV) and destination
   - Use the date grid or price graph to find cheapest dates
   - Enable "Track prices" for email alerts
   - Check "Explore" for flexible destination ideas

2. **Cross-check on Skyscanner** (skyscanner.co.il):
   - Same route and dates
   - Sort by "Cheapest" to see all options including OTAs
   - Use "Whole month" view to spot the cheapest window

3. **Check Israeli platforms**:
   - Issta (issta.co.il) for package deals
   - Lametayel (lametayel.co.il) for aggregated Israeli operator prices

4. **Compare total costs**:
   - Base fare + baggage fees + seat selection + extras
   - Low-cost carriers show low base fares but add-ons matter

### Step-by-Step: Flexible Destination Search

1. **Skyscanner**: Set destination to "Everywhere", choose your dates, sort by price
2. **Google Flights**: Click "Explore" to see a map with prices to all destinations
3. Filter by: direct flights only, max price, specific regions

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Ben Gurion Flights](https://agentskills.co.il/en/mcp/ben-gurion-flights) | Real-time TLV arrivals and departures from the Israel Airports Authority. Complement the price-comparison workflow with live flight status on travel day. |

## Gotchas

1. **El Al Lite fares to Europe/UAE have no cabin carry-on**: Since May 2025, Lite fare passengers must check their carry-on at the gate (free). Only a small personal item fits in the cabin. This catches many budget travelers off guard. Does not apply to US routes.

2. **Baggage pricing varies wildly between Israeli airlines**: Arkia charges for checked bags on all fares; El Al includes bags on Classic and above; Israir charges for everything except a personal item (as of March 2026). Always check the specific fare's baggage inclusion before comparing base prices.

3. **Israeli holiday pricing is front-loaded**: Prices spike 2-4 weeks BEFORE the holiday, not on the holiday itself. By the time Rosh Hashana starts, the peak pricing window has passed for most routes.

4. **"Direct" does not mean "nonstop" on some platforms**: Skyscanner and some OTAs list flights with a technical stop (same plane, brief stop) as "direct." Verify on the airline's own site if nonstop matters to you.

5. **Issta and Lametayel prices include different things**: Issta package prices often include hotel+transfers; Lametayel shows flight-only comparison. Comparing a Lametayel flight price to an Issta package price is not apples-to-apples.

6. **Currency mismatches**: Google Flights shows prices in NIS by default for Israeli users, but Skyscanner may show USD or EUR depending on settings. Ensure you're comparing in the same currency.

## Bundled Resources

- `references/comparison-platforms.md` -- Detailed platform comparison with URLs and features
- `references/airline-baggage-quick-ref.md` -- Quick-reference baggage table for all Israeli airlines

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| El Al baggage policy | https://www.elal.com/eng/baggage | Current carry-on weight/size, Lite fare restrictions, Matmid tier exemptions |
| Israir baggage policy | https://www.israir.co.il | Advance vs airport carry-on and checked-bag pricing, personal item rules |
| Arkia baggage policy | https://www.arkia.co.il/en/luggage-information | Trolley and checked-bag fees, weight limits, excess/kg charges |
| Wizz Air baggage & routes | https://www.wizzair.com | Base fare inclusions, WIZZ Priority add-on, current Israel route list |
| Google Flights (Israel) | https://www.google.com/travel/flights?gl=IL&hl=he | Flight Deals AI availability, fare-history bands, tracked-price alerts |
| Expedia 2026 Air Hacks (AFAR coverage) | https://www.afar.com/magazine/expedia-data-shows-new-best-day-to-book-cheaper-flights | Cheapest booking day, best day to fly, optimal booking window |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Google Flights shows no results from TLV | Locale not set to Israel | Add `?gl=IL&hl=he` to the URL |
| Skyscanner prices differ from airline site | OTA pricing vs direct pricing | Book directly with airline if price matches; OTA prices may include markup or different fare class |
| Issta shows only packages, not flights | Default view shows packages | Navigate to the "Flights" (טיסות) section specifically |
| Price alert not working | Tracking not enabled | On Google Flights, click the toggle next to "Track prices" after searching a route |
| Baggage fees not shown upfront | Low-cost carrier practices | Click through to the booking page to see total cost with bags and extras |
