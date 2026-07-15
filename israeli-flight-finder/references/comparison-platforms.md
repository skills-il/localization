# Flight Comparison Platforms for Israeli Travelers

## Pre-Filled Deep-Link Search URLs

Build a click-ready search for the traveler's exact route and dates, then open it to read the live fares (or hand it to the traveler). Verified URL patterns:

| Platform | Round-trip template | Notes |
|----------|---------------------|-------|
| Google Flights | `https://www.google.com/travel/flights?q=Flights+from+TLV+to+{CITY}+on+{YYYY-MM-DD}+returning+{YYYY-MM-DD}&curr=ILS&gl=IL&hl=he` | Natural-language query; plain city name; `curr=ILS` forces shekel prices |
| Skyscanner | `https://www.skyscanner.co.il/transport/flights/tlv/{dest}/{YYMMDD}/{YYMMDD}/` | Lowercase city name or IATA; dates as `YYMMDD`; whole month = `{YYMM}00`; "anywhere cheap" = `tlv/anywhere/{YYMMDD}/` |
| KAYAK | `https://il.kayak.com/flights/TLV-{DEST}/{YYYY-MM-DD}/{YYYY-MM-DD}?sort=price_a` | IATA codes; `sort=price_a` = cheapest first; use `il.kayak.com` for a Hebrew/ILS view |

- One-way: drop the second date segment on Skyscanner and KAYAK.
- Nonstop and max-price filters: apply them on the results page (sidebar), do not fabricate filter query parameters.
- Google Flights and Skyscanner render fares with JavaScript, so read them with a real browser/rendering tool; KAYAK and the Google Flights natural-language query are the most fetch-friendly.
- Worked example (TLV→Rome, 3-10 Aug 2026): Skyscanner `.../tlv/rome/260803/260810/`; KAYAK `.../TLV-ROM/2026-08-03/2026-08-10?sort=price_a`.

## Global Platforms with Hebrew Support

### Google Flights
- **URL**: google.com/travel/flights?gl=IL&hl=he
- **Hebrew**: Full Hebrew interface
- **Strengths**: AI-powered Flight Deals (natural language search in Hebrew), price tracking with email alerts, "Explore" destination map, fare history graphs showing if current price is low/typical/high
- **Data source**: Pulls pricing directly from airlines and select OTAs
- **Best for**: Direct airline prices, price monitoring, flexible destination discovery

### Skyscanner
- **URL**: skyscanner.co.il
- **Hebrew**: Full Hebrew interface
- **Strengths**: Broadest provider coverage (1000+ airlines and OTAs), "Everywhere" search (cheapest destination for your dates), monthly price calendar, price alerts
- **Data source**: Aggregates from airlines, OTAs, and travel agencies worldwide
- **Best for**: Finding the absolute cheapest option including OTA deals, flexible destination search

### KAYAK
- **URL**: il.kayak.com
- **Hebrew**: Full Hebrew interface
- **Strengths**: Fare forecasting ("buy now" or "wait" recommendation), flexible date search, price alerts, hotel+flight bundles
- **Data source**: Searches 100+ travel sites
- **Best for**: Price prediction, flexible date search

## Israeli Platforms

### Issta
- **URL**: issta.co.il
- **Hebrew**: Native Hebrew platform
- **Founded**: 1956 (originally Israeli Student Travel Association)
- **Strengths**: Israel's largest travel agency (60+ branches nationwide), flight+hotel package deals, charter flights, physical locations for in-person booking, Hebrew-first customer support
- **Best for**: Package deals, charter flights to popular destinations, travelers who prefer Hebrew support and in-person service

### Lametayel
- **URL**: lametayel.co.il
- **Hebrew**: Native Hebrew platform
- **Strengths**: One of Israel's most popular travel content sites, aggregates prices from Israeli tour operators and airlines, strong comparison engine for flights departing Israel
- **Best for**: Comparing Israeli operator prices, finding deals from Israeli travel companies

## Platform Selection Quick Reference

| Need | Best Platform |
|------|--------------|
| Cheapest flight overall | Google Flights + Skyscanner cross-check |
| Cheapest destination for my dates | Skyscanner "Everywhere" |
| Flight + hotel package | Issta |
| Price drop alerts | Google Flights or KAYAK |
| Hebrew-only user who wants help | Issta (has physical branches + phone support) |
| Low-cost carrier comparison | Skyscanner (best Wizz Air coverage) |
| Fare prediction (buy now or wait?) | KAYAK |
