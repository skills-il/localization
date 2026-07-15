---
name: israeli-flight-finder
description: "Compare real flight prices from Ben Gurion (TLV): build pre-filled search links for Google Flights, Skyscanner, and KAYAK for the traveler's exact route and dates, read the live fares off them, and add Israeli-airline baggage for a true total cost. Use when someone asks to find or compare cheap flights from Israel, wants the cheapest fare or the cheapest dates to fly, or asks about El Al, Israir, Arkia, or Wizz Air baggage fees, seasonal TLV pricing, or Issta flight+hotel packages. Presents a real comparison and never quotes invented prices. Do NOT use for domestic travel within Israel (use israeli-travel-planner), train schedules (use railil), or hotel-only bookings."
license: MIT
---

# Israeli Flight Finder

Find the cheapest flights from Ben Gurion Airport (TLV) by building a real, live price comparison for the traveler's exact route and dates, then reading the current fares off the search platforms. This skill does the comparison; it does not just list websites.

> **TLV carrier status is highly volatile (verified July 2026).** The February 2026 Iran war closed Israeli airspace and shut Ben Gurion for roughly 40 days; the airport fully reopened on 9 April 2026 and operates normally now, but the foreign-carrier recovery is uneven, some airlines are back while several stay suspended into autumn 2026, and dates slip constantly with EASA conflict-zone advisories. Treat every carrier status below as a snapshot, not a guarantee. This volatility is exactly why the workflow in "How to Search" builds a live search for the user's own dates instead of trusting a static route list, always confirm the specific airline and route on its own site (or via a live search) before relying on it.

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
- **Network**: As of summer 2026, El Al runs roughly 900 weekly flights to 50+ international destinations, its largest-ever schedule, including a record North American program (~55 weekly flights). It kept flying through the February 2026 war (and ran rescue flights) while foreign carriers suspended, so it still holds an outsized share of TLV traffic.
- **Website**: elal.com
- **Does not fly Shabbat**: El Al does not operate on Shabbat or Jewish holidays - see the "Shabbat-Aware Scheduling" section below before planning return flights.
- **Frequent flyer**: Matmid, whose program has four tier statuses above base membership (Silver, Gold, Platinum, Top Platinum). You advance by earning "Diamonds", the more Diamonds, the faster you climb.

**Baggage policy:**

| Fare class | Carry-on | Checked bags |
|------------|----------|--------------|
| Economy Lite | 1 x 8 kg (56x45x25 cm) + 1 personal item | None included |
| Economy Classic | 1 x 8 kg + 1 personal item | 1 x 23 kg |
| Economy Flex | 1 x 8 kg + 1 personal item | 1 x 23 kg |
| Premium | 1 x 8 kg + 1 personal item | 2 x 23 kg |
| Business | 1 x 16 kg (56x45x25 cm) + 1 personal item | 2 x 32 kg |

**Economy Lite restriction (Europe/UAE)**: Since May 2025, Lite fare passengers on flights to/from Europe or the UAE must check their carry-on at the gate (free of charge). Only a personal item (max 38x30x18 cm) is allowed in the cabin. This does NOT apply to US routes or Classic/Flex fares. Matmid Frequent Flyer members with Silver status or higher are exempt.

**Matmid members**: Silver status and above are exempt from the Lite gate-check and get enhanced carry-on privileges.

### Israir (6H)

- **Hub**: Ben Gurion (TLV), Ramon Airport (Eilat)
- **Network**: ~49 international destinations (Europe, New York, India, Central Asia) + domestic (Eilat, Haifa)
- **Website**: israir.co.il
- **Fleet**: Transitioning to all-Airbus (A320/A330); A330s for long-haul (New York, Asia)

**Baggage policy (updated July 2026, verify on israir.co.il):**

| Item | Weight | Cost (advance) | Cost (airport) |
|------|--------|----------------|----------------|
| Personal item | Small bag (under seat) | Free | Free |
| Carry-on | 10 kg | $30 per direction | $40 |
| 1st checked bag | 23 kg | $65 per direction | $100 |
| 2nd checked bag | 23 kg | $80 per direction | -- |
| Bags 3-5 (each) | 23 kg | $120 per direction | -- |
| Overweight (24-32 kg) | -- | +$20 per direction | +$70 |

Israir raised the advance first-bag fee to $65 per direction effective 1 May 2026; the airport fee stays $100. Always confirm the live figure before booking.

Standard fares do not include checked baggage. Some vacation packages may bundle bags.

### Arkia (IZ)

- **Hub**: Ben Gurion (TLV), Ramon Airport (Eilat)
- **Network**: ~40 international destinations including New York, Bangkok, European cities, Greek islands
- **Website**: arkia.co.il
- **New for 2026**: Business class on select European routes (Paris first), plus Phuket, Malaga, Ibiza, Vilnius, Hanoi

**Baggage policy (international flights, verify on arkia.co.il):**

| Item | Weight / Size | Cost (advance) | Cost (airport) |
|------|---------------|----------------|----------------|
| Hand bag (under-seat) | 20x30x40 cm, no weight limit | Free | Free |
| Trolley bag | 8 kg (25x45x56 cm) | $25 | $30 / EUR 25 |
| Checked bag | 20 kg | $50 | $90 / EUR 85 |
| Excess per kg | -- | -- | $10 / EUR 10 |

Second checked bag $70 advance / $100 airport, third $90 advance / $120 airport (verified on arkia.co.il, July 2026).

### Low-Cost Carriers

**Wizz Air (W6)**: Hungarian low-cost carrier. Wizz had been expanding aggressively at TLV, but the February 2026 war forced it to suspend all Israel operations along with everyone else, and its earlier hub-base plans were frozen. Wizz resumed TLV operations on **May 28, 2026**, reconnecting Tel Aviv with hubs such as London, Budapest, Rome, Bucharest, Larnaca, Milan, and Athens, with frequencies still ramping up over summer 2026. Verify the specific route on wizzair.com. Only a small personal item (40x30x20 cm) is free on base fares; cabin bags and checked bags are paid add-ons.

**Ryanair**: Has officially removed Tel Aviv from its route map. Cancelled 22 planned routes and roughly 1 million seats for the 2025-2026 season due to disputes with Ben Gurion Airport over slot allocation and Terminal 1 availability. As of July 2026, Ryanair still has no confirmed TLV return; any resumption is conditional on the airport resolving the slot and Terminal 1 dispute.

### Foreign Carriers

The February 2026 war reset this landscape. Some foreign carriers have returned, several stay suspended, and the dates slip frequently. The status below is as of July 2026.

- **flydubai**: Operating TLV-Dubai again (up to ~10 daily flights before the early-June 2026 regional flare-up trimmed the schedule); verify the current Dubai-TLV frequency on flydubai.com. Still the main option for connections to the Gulf, Asia, and East Africa via Dubai.
- **Emirates**: Fully withdrew from Tel Aviv before the 2026 war and has NOT returned as of July 2026. Dubai is served by flydubai, not Emirates.
- **Turkish Airlines**: Still NOT flying Tel Aviv as of July 2026. It resumed several other regional routes (Abu Dhabi from 1 July, then Dammam, Kuwait, Bahrain) but has only said it is "considering" a TLV return, with no confirmed date. Verify on turkishairlines.com before assuming an Istanbul connection.
- **Lufthansa Group** (Lufthansa, Swiss, Austrian, Brussels, ITA): Mostly back. Lufthansa and SWISS resumed TLV on 1 July 2026 and Austrian in June; Brussels Airlines stays suspended (through 24 October 2026). Verify the specific route.
- **Other carriers**: Aegean, Air France, and Etihad (Abu Dhabi) are among the carriers operating again. Still suspended into autumn 2026 as of July: easyJet (not before autumn), United (~7 Sep), Delta (~6 Sep), Air Canada (~7 Sep), American (not before Jan 2027), plus Iberia and British Airways (return dates uncertain). Post-war schedules move weekly, so always verify current status on each airline's own site before relying on it.

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

## Shabbat-Aware Scheduling

Hebrew-calendar timing constrains flight options in a way generic search tools ignore.

- **El Al does not fly on Shabbat or Jewish holidays.** Its scheduled operations stop from Friday afternoon (before sundown) until Saturday after sundown. For observant travelers this is a feature; for everyone it means El Al has **no** Friday-evening or Saturday-daytime departures or arrivals. A Friday-night or Saturday return on El Al simply does not exist - you must fly Thursday, early Friday, or Saturday night onward. The same no-fly window blocks **outbound** Friday-evening and Saturday departures, not just returns.
- **Israir** has, under its current ownership, also cancelled flights departing on Saturday and on Friday nights, observing Shabbat. So for Saturday departures, do not count on Israir either - verify on israir.co.il.
- **Arkia** is the Israeli carrier most likely to operate on Shabbat. If a Friday-night or Saturday flight is essential and you want an Israeli airline, Arkia is usually the option to check first.
- **Foreign carriers** fly seven days a week, so a Friday-night or Saturday departure from TLV generally means a foreign airline (or Arkia).
- **Planning rule**: when building a return itinerary, fix the Shabbat window first. If the traveler is observant or wants an Israeli carrier, plan returns for Thursday, Friday before midday, or Saturday night. Around Jewish holidays the same no-fly window applies to El Al on the holiday itself, on top of the pre-holiday price spike.

## Entry Requirements (Europe: EES and ETIAS)

A cheap fare is worthless if the traveler cannot board or enter, so check entry rules and passport validity before recommending any route.

- **Passport validity:** confirm the passport is valid for at least 6 months beyond the return date (a safe rule for most destinations, though Schengen's own minimum is 3 months beyond departure from the area). For Schengen there is a second rule that trips up Israeli travelers with older passports: the passport must have been **issued within the last 10 years**, so a document renewed with a paper validity extension can be refused at boarding even if the printed expiry looks fine. Israeli passport renewals can also run into backlogs.
- **EES (Entry-Exit System) is live.** Since 10 April 2026 the EU records non-EU travelers' biometrics (facial image and fingerprints) at Schengen external borders instead of stamping passports. Expect this at the border; no advance action is needed.
- **ETIAS is not required yet.** As of July 2026 an Israeli traveler does NOT need ETIAS to fly to Europe. The EU's official timeline still targets a launch in late 2026 with a transitional period before it becomes mandatory (around 2027), but the rollout has repeatedly slipped and EU agencies have signalled the late-2026 date may move into 2027. Do not apply early through unofficial sites, and check the official EU travel page for the current status before a late-2026 or 2027 trip.

## Booking Strategies

### Timing

- **Book several weeks out, not months.** Hard day/dollar "optimal window" claims date fast and rarely beat active price tracking. For European leisure routes from TLV, roughly 6-8 weeks out is a reasonable target; expect a 2-4 week pre-holiday spike around the chagim.
- **Day-of-week effects are small and shift yearly.** Recent Expedia data put the cheapest day to *fly* mid-week (Tuesday, around 14% below the peak day domestically) with weekend departures at a premium; the cheapest day to *book* moves year to year. Do not over-optimize the day, set a price alert instead.
- Set price alerts on Google Flights or KAYAK for routes you're watching, then pounce when the fare dips below the "typical" band on the fare-history graph.

### Money-Saving Tips

1. **Compare across 3+ platforms**: Prices differ significantly between platforms for the same route
2. **Check package deals on Issta**: Flight+hotel bundles often beat booking separately by hundreds of shekels
3. **Use "Everywhere" search on Skyscanner**: Find the cheapest destination for your dates instead of picking a destination first
4. **Consider nearby airports**: For European destinations, flying to a nearby city and taking a train can be cheaper (e.g., fly to Bergamo instead of Milan)
5. **Book baggage in advance**: All Israeli airlines charge significantly more for baggage purchased at the airport vs online in advance
6. **Check Wizz Air for European routes**: Low-cost fares start very low but add-ons (bags, seats) add up -- compare total cost including bags
7. **Flexible dates**: Shifting departure by 1-2 days can save 30%+ on the same route
8. **Try multi-city / open-jaw**: For multi-stop Europe trips, flying into one city and out of another (e.g. into Rome, out of Milan) often beats a round-trip. Google Flights and Skyscanner both support multi-city search.
9. **Protect against disruption**: TLV routes still get suspended on short notice (EASA conflict-zone advisories). For non-refundable foreign-carrier fares, prefer a refundable/flexible fare or travel insurance that covers airspace closure and conflict disruption, and check the airline's rebooking policy before booking. This is the most likely way to lose money on a 2026 TLV booking.

### Deal Sources (Israeli)

Error fares and flash deals vanish fast and rarely appear on the big aggregators. Israeli travelers track them through dedicated channels:

- **Secret-flights sites** (e.g. secretflights.co.il, "טיסות סודיות") that surface mispriced fares.
- **Telegram deal channels and Facebook groups** focused on TLV departures.

Treat these as a complement to the aggregators, not a replacement, and book fast because error fares get pulled quickly.

### Points and Miles

For frequent flyers the cash price is not the only lever:

- **El Al Matmid** points can be redeemed for award flights, and tier status adds baggage and lounge value.
- **Israeli cards** (Isracard, American Express Israel, Max) often earn Matmid points or airline miles, and some dollar-linked cards add travel perks. Compare the points cost against the cash fare before booking.

### Flight+Hotel Packages

Israeli travel agencies (Issta, Lametayel) specialize in package deals that bundle flights and hotels. These can be significantly cheaper than booking separately, especially for popular destinations like Greece, Cyprus, Turkey, and European cities.

### Departure Airport: TLV vs Ramon (Eilat)

Most international flights leave from Ben Gurion (TLV), but Ramon Airport (ETM) near Eilat also handles some international and charter routes, and Israir and Arkia base operations there. For travelers in the south, departing from Ramon can save the long drive to TLV; for everyone else, TLV almost always has more routes, more frequencies, and more price competition. When comparing, factor the ground cost and time to reach each airport - a cheaper Ramon fare can be eaten up by getting to Eilat. Check both when your destination is one Ramon actually serves (mostly European leisure routes and charters).

### Kosher and Special Meals

- **El Al** serves kosher meals by default on all flights - no special request needed (its kitchen is certified kosher).
- **Israir and Arkia** also cater to the Israeli market and offer kosher options; confirm when booking.
- **Foreign carriers** do not serve kosher by default. If you keep kosher, request a kosher meal (special meal code KSML) at booking or at least 24-48 hours before departure - it cannot be arranged at the gate. The same applies to other special meals (vegetarian, vegan, gluten-free). On very short flights some carriers serve no meal at all, so a special-meal request may simply not apply.

## How to Search

> **Plan for TLV security.** The Israel Airports Authority advises arriving **3 hours before international departures** (more at peak times, and summer 2026 is congested) because of Israel's layered security screening. Factor this in when a cheap early-morning fare would require a pre-dawn arrival.

**This skill's job is to compare real flights, not to name websites.** Follow the workflow below: build the pre-filled search links for the traveler's exact route and dates, read the live fares off them, add baggage to get a true total, and return an actual comparison. Never substitute remembered or estimated prices for this work (see "Never invent a price").

### Step 1: Gather the Trip

Assume TLV as the origin and ask only for what is missing:

1. Destination (city or airport code, or "anywhere cheap")
2. Dates (specific, or a flexible month)
3. Number of passengers
4. Checked bag needed, or carry-on only?
5. Nonstop only, or connections OK?
6. Airline preference or budget ceiling (optional)

### Step 2: Build the Pre-Filled Search Links

Construct a real, click-ready search URL for each platform from the route and dates. These are verified URL patterns, substitute the destination and dates. Skyscanner takes the lowercase city name or IATA code and dates as `YYMMDD`; KAYAK takes IATA codes (Rome = `ROM`, Paris = `PAR`, Larnaca = `LCA`) and dates as `YYYY-MM-DD`; Google Flights takes plain city names.

| Platform | Round-trip URL template |
|----------|-------------------------|
| Google Flights | `https://www.google.com/travel/flights?q=Flights+from+TLV+to+{CITY}+on+{YYYY-MM-DD}+returning+{YYYY-MM-DD}&curr=ILS&gl=IL&hl=he` |
| Skyscanner | `https://www.skyscanner.co.il/transport/flights/tlv/{dest}/{YYMMDD}/{YYMMDD}/` |
| KAYAK | `https://il.kayak.com/flights/TLV-{DEST}/{YYYY-MM-DD}/{YYYY-MM-DD}?sort=price_a` |

- **One-way**: drop the second date (Skyscanner: one `YYMMDD` segment; KAYAK: one date).
- **Flexible month** (find the cheapest dates): Skyscanner whole-month view, `https://www.skyscanner.co.il/transport/flights/tlv/{dest}/{YYMM}00/` (note the `00` in place of the day).
- **"Anywhere cheap"**: Skyscanner "Everywhere", `https://www.skyscanner.co.il/transport/flights/tlv/anywhere/{YYMMDD}/`, or the Google Flights "Explore" map.
- **Nonstop / max-price**: build the base link, then apply the nonstop and price filters on the results page (the sidebar filters), do not guess filter query parameters.
- **Keep one currency**: use `il.kayak.com` (as shown), NOT `www.kayak.com` which defaults to USD. Google Flights `curr=ILS` and Skyscanner `.co.il` already return shekels. Mixing a USD KAYAK fare into the NIS total in Step 4 is the currency trap in Gotcha 6.
- Worked example (TLV→Rome, 3-10 Aug 2026): Google Flights `...q=Flights+from+TLV+to+Rome+on+2026-08-03+returning+2026-08-10...`; Skyscanner `.../tlv/rome/260803/260810/`; KAYAK `.../TLV-ROM/2026-08-03/2026-08-10?sort=price_a`.

### Step 3: Pull the Live Fares

Open each link and read the actual results, do not stop at building the URLs:

- With a browser tool (or a flights MCP), navigate to each URL and read the top 3-5 fares: airline, price in shekels, number of stops, total duration, and departure/return times.
- **All three platforms render fares with JavaScript**, KAYAK included. Reading live prices needs a real browser/rendering tool or a flights MCP; a plain `WebFetch` returns an empty shell with no fares. If you do NOT have a browser tool this turn, do not report a comparison from `WebFetch` alone, hand the traveler the pre-filled links from Step 2 instead (see "Never invent a price").
- Cross-check at least two platforms, the same route routinely differs by hundreds of NIS between Google Flights (direct airline fares) and Skyscanner (OTA deals).
- For flexible dates, read the cheapest-date cells from the Skyscanner month calendar or the Google Flights date grid.
- For real-time TLV flight status on travel day, the [Ben Gurion Flights](https://agentskills.co.il/en/mcp/ben-gurion-flights) MCP gives live arrivals and departures (it does not return prices).

### Step 4: Normalize to Total Cost

A base fare is not comparable until you add what the traveler actually needs. For each option compute:

`base fare + checked-bag fee (if needed) + seat selection (if wanted) = total per person`.

Pull the bag fees from the Israeli-airline tables above: El Al includes a checked bag on Classic and up, while Israir, Arkia, and Wizz charge for almost everything. A low base fare on Israir, Arkia, or Wizz routinely loses to El Al Classic once a 23 kg bag is added, this is the single most common comparison mistake.

### Step 5: Present the Comparison

Return a table with the REAL fares you pulled, cheapest total first:

| Option | Airline | Route / Stops | Base (NIS) | Bags (NIS) | Total (NIS) | Notes |
|--------|---------|---------------|-----------|-----------|------------|-------|
| 1 | ... | ... | ... | ... | ... | e.g. no Shabbat return, gate-check carry-on on Lite |

Then give a one-line recommendation covering cheapest total, best value (price vs. stops and timing), and best for a family with bags. Include the Step 2 links so the traveler can book or re-check the live price.

### Never Invent a Price

**Every number in the comparison must come from a page you actually loaded this session.** Do not estimate, guess, or fill in "typical" fares from memory, flight prices change hourly and a fabricated comparison is worse than none. If you cannot read live prices this turn (no web or browser access, the page is bot-blocked, or a captcha appears), do NOT write any numbers. Instead, hand the traveler the ready-to-click links you built in Step 2, pre-filled for their exact route and dates, and say plainly that these open live results to compare because you could not read the fares yourself this turn. Being honest about missing live data keeps the skill trustworthy; fake numbers destroy it.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Ben Gurion Flights](https://agentskills.co.il/en/mcp/ben-gurion-flights) | Real-time TLV arrivals and departures from the Israel Airports Authority. Complement the price-comparison workflow with live flight status on travel day. |

## Gotchas

1. **El Al Lite fares to Europe/UAE have no cabin carry-on**: Since May 2025, Lite fare passengers must check their carry-on at the gate (free). Only a small personal item fits in the cabin. This catches many budget travelers off guard. Does not apply to US routes.

2. **Baggage pricing varies wildly between Israeli airlines**: Arkia charges for checked bags on all fares; El Al includes bags on Classic and above; Israir charges for everything except a personal item (as of July 2026). Always check the specific fare's baggage inclusion before comparing base prices.

3. **Israeli holiday pricing is front-loaded**: Prices spike 2-4 weeks BEFORE the holiday, not on the holiday itself. By the time Rosh Hashana starts, the peak pricing window has passed for most routes.

4. **"Direct" does not mean "nonstop" on some platforms**: Skyscanner and some OTAs list flights with a technical stop (same plane, brief stop) as "direct." Verify on the airline's own site if nonstop matters to you.

5. **Issta and Lametayel prices include different things**: Issta package prices often include hotel+transfers; Lametayel shows flight-only comparison. Comparing a Lametayel flight price to an Issta package price is not apples-to-apples.

6. **Currency mismatches**: Google Flights shows prices in NIS by default for Israeli users, but Skyscanner may show USD or EUR depending on settings. Ensure you're comparing in the same currency.

7. **Prices must be pulled live, never recalled**: fares change hourly, so a remembered or "typical" number is almost always wrong by the time it is quoted. Read the actual current price off the search links every time you compare, and if you cannot read live prices this turn, hand over the pre-filled links instead of guessing. A comparison built from invented numbers is the fastest way to lose the user's trust.

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
| ETIAS (official EU) | https://travel-europe.europa.eu/etias_en | Whether ETIAS is required now for Israeli citizens, how to apply, EES rollout |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Google Flights shows no results from TLV | Locale not set to Israel | Add `?gl=IL&hl=he` to the URL |
| Skyscanner prices differ from airline site | OTA pricing vs direct pricing | Book directly with airline if price matches; OTA prices may include markup or different fare class |
| Issta shows only packages, not flights | Default view shows packages | Navigate to the "Flights" (טיסות) section specifically |
| Price alert not working | Tracking not enabled | On Google Flights, click the toggle next to "Track prices" after searching a route |
| Baggage fees not shown upfront | Low-cost carrier practices | Click through to the booking page to see total cost with bags and extras |
