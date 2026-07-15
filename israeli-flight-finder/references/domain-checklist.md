# Domain Coverage Checklist: Israeli Flight Finder

Scope: helping a traveler in Israel find and compare the cheapest international flights from Ben Gurion (TLV) / Ramon (ETM), including doing the live comparison, understanding Israeli-airline pricing, and clearing entry/scheduling constraints.

## Must cover (core)

- **Live comparison workflow**: build pre-filled search links for the exact route and dates, pull the actual current fares, normalize to total cost, and present a real comparison. This is the skill's core job. (Precedent: user complaint that a "flight finder" that only names websites without comparing is not usable.)
- **Comparison platforms**: Google Flights, Skyscanner, KAYAK (global, Hebrew UI) + Issta / Lametayel (Israeli agencies, packages). What each is best for.
- **Deep-link / pre-filled search URLs** for the platforms so a search can be constructed programmatically (Google Flights `q=` NL query, Skyscanner `/transport/flights/tlv/{dest}/{YYMMDD}/`, KAYAK `/flights/TLV-{DEST}/{date}/`).
- **Anti-fabrication rule for prices**: fares change hourly; never invent or recall a price. If live data cannot be read, hand over the pre-filled links. (Core trust requirement.)
- **Israeli carriers**: El Al (LY), Israir (6H), Arkia (IZ), plus low-cost (Wizz Air) and the foreign-carrier landscape. Network scope and hub (TLV / Ramon).
- **Baggage policies + fees** for El Al (Lite/Classic/Flex), Israir, Arkia, Wizz, incl. advance-vs-airport pricing and the El Al Lite Europe/UAE gate-check rule. Baggage must be folded into total-cost comparison.
- **Shabbat-aware scheduling**: El Al does not fly Shabbat/holidays; Israir Shabbat policy; Arkia most likely to fly Shabbat; foreign carriers fly 7 days. (Israeli-calendar constraint generic tools ignore.)
- **Seasonal pricing**: peak (chagim, summer, Purim), shoulder, off-peak (January cheapest); holiday prices front-load 2-4 weeks before.
- **Entry requirements for Israeli travelers to Europe**: passport 6-month validity, EES (live 10 April 2026, biometric), ETIAS (not yet required; late-2026/2027, may slip). A cheap fare is worthless if the traveler cannot board/enter.
- **TLV security / arrival time**: Israel Airports Authority 3-hours-before-international recommendation.
- **Volatility disclaimer**: post-Feb-2026-war carrier status is a moving target; verify live per airline/route.

## Should cover (advanced)

- **Booking strategy / timing**: book weeks not months out; day-of-week effects small; use price alerts (Google Flights / KAYAK).
- **Money-saving tactics**: cross-check 3+ platforms, flexible dates (whole-month view), nearby airports, multi-city / open-jaw, Skyscanner "Everywhere".
- **Israeli deal sources**: secret-flights sites, Telegram/Facebook deal channels (error fares not on aggregators).
- **Points & miles**: El Al Matmid, Israeli credit-card earn (Isracard, Amex IL, Max).
- **Flight+hotel packages**: Issta / Lametayel bundles vs booking separately.
- **Departure airport choice**: TLV vs Ramon (Eilat) for southern travelers.
- **Kosher / special meals**: El Al kosher by default; foreign carriers need KSML request.
- **Disruption protection**: refundable fares / insurance covering airspace closure (2026 TLV risk).
- **Recommended MCP**: Ben Gurion Flights (live TLV arrivals/departures, flight status, not prices).

## Out of scope (explicit)

- **Domestic travel within Israel** - handled by `israeli-travel-planner`.
- **Train schedules** - handled by `railil`.
- **Hotel-only bookings** - not a flight-comparison task.
- **Actual booking / payment execution** - the skill compares and links out; the traveler books on the platform.
- **Live price data as a stored fact** - prices are pulled live per query, never encoded in the skill.
- **Arkia Shabbat-flying permanence** - a potential Haredi buyout could change it; treat as a watch item, not a fixed fact.

## Authoritative sources

- Airline baggage/network: elal.com/eng/baggage, israir.co.il, arkia.co.il/en/luggage-information, wizzair.com
- Carrier resumption status (post-war): airline own sites; travel trade press (mtm.travel, openjaw.com), ynetnews, timesofisrael
- Entry rules: travel-europe.europa.eu (EES/ETIAS), home-affairs.ec.europa.eu
- TLV security: iaa.gov.il
- Platforms: google.com/travel/flights, skyscanner.co.il, kayak.com, issta.co.il, lametayel.co.il
