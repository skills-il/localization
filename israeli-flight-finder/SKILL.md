---
name: israeli-flight-finder
description: "Compare flight prices from Ben Gurion Airport (TLV) across Google Flights, Skyscanner, KAYAK, and Israeli platforms like Issta and Lametayel. Use when a user asks about cheap flights from Israel, flight comparison, airline baggage policies, best time to book flights, or seasonal pricing from TLV. Covers El Al, Israir, Arkia, and low-cost carriers like Wizz Air. Helps users find the cheapest fares, understand Israeli airline baggage fees, and plan around peak and off-peak travel seasons. Do NOT use for domestic travel within Israel (use israeli-travel-planner), train schedules (use railil), or hotel-only bookings."
license: MIT
---

# Israeli Flight Finder

Find the cheapest flights from Ben Gurion Airport (TLV) by comparing prices across multiple platforms and understanding Israeli airline pricing patterns.

> **TLV carrier status is highly volatile (verified May 2026).** The brief Iran war that began at the end of February 2026 closed Israeli airspace and forced nearly every foreign carrier to suspend TLV service again. Carriers are resuming on a rolling schedule through mid-2026, but dates slip constantly and depend on EASA conflict-zone advisories. Treat every "resumes on date X" claim below as a plan, not a guarantee - always verify the current route and the specific airline's status on its own site before relying on it.

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
- **Network**: As of May 2026, El Al is rebuilding toward roughly 40 international destinations after the February 2026 war disruption, with summer 2026 North American frequencies at an all-time high. It kept flying through the war (and ran rescue flights) while foreign carriers suspended, so it currently has an outsized share of TLV traffic.
- **Website**: elal.com
- **Does not fly Shabbat**: El Al does not operate on Shabbat or Jewish holidays - see the "Shabbat-Aware Scheduling" section below before planning return flights.
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

**Baggage policy (updated May 2026, verify on israir.co.il):**

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

| Item | Weight | Cost (advance) | Cost (airport) |
|------|--------|----------------|----------------|
| Carry-on | 7 kg | Free | Free |
| Trolley bag | 8 kg | $20 | $25 / EUR 25 |
| Checked bag | 20 kg | $45 | $90 / EUR 85 |
| Excess per kg | -- | -- | $10 / EUR 10 |

### Low-Cost Carriers

**Wizz Air (W6)**: Hungarian low-cost carrier. Wizz had been expanding aggressively at TLV, but the February 2026 war forced it to suspend all Israel operations along with everyone else, and its earlier hub-base plans were frozen. Wizz resumed TLV operations on **May 28, 2026**, reconnecting Tel Aviv with hubs such as London, Budapest, Rome, Bucharest, Larnaca, Milan, and Athens, with frequencies still ramping up over summer 2026. Verify the specific route on wizzair.com. Only a small personal item (40x30x20 cm) is free on base fares; cabin bags and checked bags are paid add-ons.

**Ryanair**: Has officially removed Tel Aviv from its route map. Cancelled 22 planned routes and roughly 1 million seats for the 2025-2026 season due to disputes with Ben Gurion Airport over slot allocation and Terminal 1 availability. As of May 2026, Ryanair still has no confirmed TLV return; any resumption is conditional on the airport resolving the slot and Terminal 1 dispute.

### Foreign Carriers

The February 2026 war reset this landscape. Most foreign carriers suspended TLV again and are resuming on a rolling schedule through mid-2026; the dates below are the latest plans as of May 2026 and slip frequently.

- **flydubai**: Before the war it ran one of the densest TLV schedules (about 10 daily Dubai–Tel Aviv flights). It suspended during the war and is among the carriers resuming service; verify the current Dubai–TLV frequency on flydubai.com. Still a strong option for connections to the Gulf, Asia, and East Africa via Dubai once flying.
- **Emirates**: Had fully withdrawn from Tel Aviv even before the 2026 war and has no confirmed return as of May 2026.
- **Turkish Airlines**: Off the TLV schedule since the late-2023 suspension. As of May 2026 it is tentatively planned to resume Tel Aviv from **July 1, 2026** (alongside other regional restarts), but this is dependent on EASA advisories and has slipped before. Verify on turkishairlines.com.
- **Lufthansa Group** (Lufthansa, Swiss, Austrian, Brussels, ITA): Suspended during the war; resuming TLV through mid-2026 in parallel with Wizz Air. Verify per route.
- **Other European carriers** (Air France-KLM, Iberia, Aegean, LOT, easyJet, Pegasus, SunExpress, etc.) and **other long-haul carriers** (American, Virgin Atlantic, Korean Air, Cathay Pacific): availability is in flux post-war. Some are resuming, some have not committed. Always verify current status on each airline's own site before relying on it.

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

- **Passport validity:** confirm the passport is valid for at least 6 months beyond the return date. This gates boarding for many destinations, not just Europe, and Israeli passport renewals can run into backlogs.
- **EES (Entry-Exit System) is live.** Since 10 April 2026 the EU records non-EU travelers' biometrics (facial image and fingerprints) at Schengen external borders instead of stamping passports. Expect this at the border; no advance action is needed.
- **ETIAS is not required yet.** ETIAS travel authorization is expected to become operational in Q4 2026 and only mandatory around April 2027 after a transitional period. As of mid-2026 an Israeli traveler does NOT need ETIAS to fly to Europe, so do not apply early through unofficial sites. Check the official EU travel page for the current rollout before a late-2026 or 2027 trip.

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

> **Plan for TLV security.** The Israel Airports Authority advises arriving **3 hours before international departures** (more at peak times) because of Israel's layered security screening. Factor this in when a cheap early-morning fare would require a pre-dawn arrival.

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

2. **Baggage pricing varies wildly between Israeli airlines**: Arkia charges for checked bags on all fares; El Al includes bags on Classic and above; Israir charges for everything except a personal item (as of May 2026). Always check the specific fare's baggage inclusion before comparing base prices.

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
| ETIAS (official EU) | https://travel-europe.europa.eu/etias_en | Whether ETIAS is required now for Israeli citizens, how to apply, EES rollout |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Google Flights shows no results from TLV | Locale not set to Israel | Add `?gl=IL&hl=he` to the URL |
| Skyscanner prices differ from airline site | OTA pricing vs direct pricing | Book directly with airline if price matches; OTA prices may include markup or different fare class |
| Issta shows only packages, not flights | Default view shows packages | Navigate to the "Flights" (טיסות) section specifically |
| Price alert not working | Tracking not enabled | On Google Flights, click the toggle next to "Track prices" after searching a route |
| Baggage fees not shown upfront | Low-cost carrier practices | Click through to the booking page to see total cost with bags and extras |
