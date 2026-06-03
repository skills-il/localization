---
name: israeli-travel-planner
description: Plan domestic travel in Israel with local transportation, accommodations, national parks, and cultural considerations. Use when user asks about traveling in Israel, Israeli hotel chains, bus routes, Israel Railways, Rav-Kav card, national parks, tiyul b'aretz, Dead Sea, Eilat, or trip planning within Israel. Covers Egged/Dan/Kavim buses, train schedules, Rashut HaTeva sites, Shabbat travel restrictions, and seasonal advice.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
---


# Israeli Travel Planner

## Bus Companies
| Company | Coverage |
|---------|----------|
| Egged | Nationwide intercity, Jerusalem |
| Dan | Tel Aviv metro (Gush Dan) |
| Kavim | Central Israel, Modi'in |
| Metropoline | Sharon region |
| Superbus | Jerusalem city, Haifa Metronit, north valleys |
| Nateev Express | Beer Sheva, Negev |

## Israel Railways Key Routes
- Tel Aviv - Haifa: ~1 hour, every 20-30 min
- Tel Aviv - Jerusalem: ~30 min (fast line)
- Tel Aviv - Beer Sheva: ~1.5 hours
- Haifa - Nahariya: ~40 min
- Acre - Karmiel: ~25 min (Galilee line, stations Ahidud and Karmiel)
- Haifa - Beit She'an: ~1 hour (Jezreel Valley line)

## Rav-Kav Card
Rechargeable smart card for all public transport. Types: Personal (with photo) and Anonymous. Load passes: daily, weekly, monthly, or stored value. The Rav-Kav is no longer the only fare medium: a physical Rav-Kav can be loaded remotely through the Rav-Kav Online, HopOn (Rav-Pass) apps and ravkavonline.co.il instead of only at a kiosk or with the driver.

EMV contactless (tap a physical credit card, Apple Pay or Google Pay) is spreading and is not Egged-bus-only: Dan has accepted contactless cards on its central-Israel buses since October 2022, Israel Railways lets you pay with an EMV card instead of a paper ticket or pre-loaded card, and Egged rolled out a contactless pilot in Eilat, Jerusalem and Haifa in early 2026. Train-reliant travelers can tap at rail gates.

## Public Transport Fares
Under the "Derech Shava" (Equal Path) reform that took effect 25 April 2025, single-ride fares are set by distance, not by operator. Current single-ride bus fares:
- Up to 15 km (urban): 8 NIS, including 90 minutes of free transfers within the zone.
- Up to 40 km: 14.5 NIS.
- Up to 75 km: 19 NIS.
- Up to 120 km: 19 NIS.
- Up to 225 km: 30.5 NIS.
- Over 225 km: 74 NIS.

A daily cap is the amount beyond which every further ride that day is free. The caps rise with the band: about 11.5 NIS up to 15 km, 21 NIS up to 40 km, 27 NIS up to 75 km, 30.5 NIS up to 120 km, 52.5 NIS up to 225 km; the over-225 km band has no daily cap. A nationwide unlimited monthly pass (up to 225 km) is about 315 NIS. Seniors aged 67 and over travel free nationwide (previously 75). Fares are slightly higher when a trip includes Israel Railways.

## Shabbat Travel
Public transit stops Friday afternoon through Saturday night. Alternatives: sherut (shared taxi), private taxis (Gett/Yango), driving. Haifa has limited Shabbat bus service. Yom Kippur: ALL roads closed.

## Hotel Chains
- Dan Hotels: luxury chain (city and resort)
- Isrotel: resort and family hotels (strong in Eilat and the Dead Sea)
- Fattal/Leonardo: mid-range city and resort hotels
- Zimmerim: country lodges and cabins in the Galilee and Golan
- Dead Sea range: Ein Bokek hotel strip (full-service resorts) versus the Ein Gedi hostel (budget)

Note: rates swing widely by season, location and event dates. Check current prices on booking sites rather than quoting a fixed figure.

## Top National Parks (Rashut HaTeva)
Masada, Ein Gedi, Banias, Caesarea, Tel Dan, Rosh HaNikra, Timna Park, Ein Avdat.
Single adult entry runs about 31 to 46 NIS at the main tourist sites (Ein Gedi and Banias 31, Masada 37, Caesarea 46), with children roughly half; smaller sites are lower. Tourist multi-site cards: Blue (3 sites) ~90 NIS, Green (6 sites) ~130 NIS, Orange (unlimited) ~175 NIS. The Matmon annual subscription is about 181 NIS for an individual (couple and family tiers cost more). Verify current pricing at parks.org.il, since rates change each year.

Masada cable car: a sunrise visit usually means taking the cable car, which is a SEPARATE charge the Blue/Green/Orange tourist cards do NOT cover. Official Masada entrance is about 37 NIS adult (21 child, 19 senior); the cable car is billed separately and does NOT include entrance, at about 32 NIS one-way (16 child) or 54 NIS round-trip (32 child). Budget the cable car on top of entrance and any tourist card.

## Regional Highlights
- Dead Sea: Ein Gedi + Masada sunrise + floating
- Eilat: Coral Beach, Timna, VAT-free shopping (Eilat is a VAT-free zone, so you save the standard 18% VAT on eligible goods)
- Galilee/Golan: Banias, Tel Dan, wineries, Tzfat
- Jerusalem: Old City, Yad Vashem, Mahane Yehuda
- Tel Aviv: Beaches, Jaffa, Carmel Market, Neve Tzedek

## Examples

### Example 1: Plan a Weekend Trip to the Dead Sea
User says: "Plan a weekend trip from Tel Aviv to the Dead Sea"
Actions:
1. Transport: Egged bus 421 from Tel Aviv Savidor to Masada (~2 hours 15 min, 24 stops; priced by distance band under Derech Shava, ~19 NIS for the up-to-120 km band) or rental car via Route 90
2. Accommodation: Ein Bokek hotel strip (full-service resorts) or the Ein Gedi hostel (budget); check current rates on booking sites
3. Activities: Ein Gedi Nature Reserve (entry ~31 NIS adult), Masada sunrise hike (entrance ~37 NIS; the cable car is a separate charge, ~32 NIS one-way / ~54 NIS round-trip, not including entrance), Dead Sea beach (free public beaches at Ein Bokek)
4. Food: Hotel restaurants, Arad for budget dining (20 min drive)
5. Tips: Bring water shoes, sunscreen SPF 50+, arrive early for Masada
Result: Complete itinerary with transport, accommodation, costs, and practical tips

### Example 2: Family Day Trip to the Galilee
User says: "Suggest a day trip for a family with kids in northern Israel"
Actions:
1. Route: Drive to Tiberias area via Route 6 + Route 77
2. Morning: Kfar Kedem biblical experience (verify current rates before visiting)
3. Lunch: Decks restaurant on the Kinneret, or falafel in Tiberias (budget option)
4. Afternoon: Hamat Gader hot springs or Kinneret beach (check current pricing)
5. Evening: Return via Route 6 (current toll rates available on toll road website)
Result: Family-friendly Galilee itinerary with kid activities and budget options

## Bundled Resources

### Scripts
- `scripts/plan_route.py` -- Calculates distances and suggests transport options between Israeli cities. Run: `python scripts/plan_route.py --help`

### References
- `references/israeli-transport-guide.md` -- Comprehensive guide to Israeli public transport (Egged, Dan, Israel Railways, Rav-Kav), national parks pricing, hotel chains, and regional highlights. Consult when planning detailed itineraries or comparing transport options.

## Recommended MCP Servers

For live transit and travel data, pair this skill with:

| MCP Server | What it provides | Install |
|------------|-----------------|---------|
| **israel-railways** | Real-time Israel Railways schedules, platform numbers, occupancy predictions, and service disruption alerts for 68 stations | [Install](https://agentskills.co.il/en/mcp/israel-railways) |
| **openbus** | Real-time bus arrival data from the Ministry of Transport for all Israeli transit operators | [Install](https://agentskills.co.il/en/mcp/openbus) |
| **routes-israel** | Multi-modal transit routing combining Google Routes, GTFS data, and live arrival times | [Install](https://agentskills.co.il/en/mcp/routes-israel) |
| **ben-gurion-flights** | Real-time flight arrivals and departures at Ben Gurion Airport (TLV) from official data | [Install](https://agentskills.co.il/en/mcp/ben-gurion-flights) |
| **israel-hiking** | Hiking trail search, route planning with elevation profiles, water sources, and points of interest | [Install](https://agentskills.co.il/en/mcp/israel-hiking) |
| **ims-weather** | Weather forecasts and alerts from the Israeli Meteorological Service for trip planning | [Install](https://agentskills.co.il/en/mcp/ims-weather) |

When these MCPs are available, use them for real-time transit schedules and travel data instead of the static reference tables above.

## Gotchas
- Public transportation in Israel does not operate on Shabbat (Friday afternoon to Saturday evening) in most cities. Agents may plan Saturday itineraries that rely on buses or trains. Exceptions: Haifa has limited Shabbat service; shared taxis (sherut) run on some routes.
- Israeli bus numbers and route names use Hebrew characters. Agents may not recognize that route 17-aleph is a different route from 17. Always include the Hebrew letter suffix.
- A physical Rav-Kav card cannot be loaded via a public API, but since early 2026 it is no longer the only option: the Rav-Kav Online / HopOn / Rav-Pass apps load a Rav-Kav remotely, and EMV contactless (tapping a credit card, Apple Pay or Google Pay at the validator) lets a traveler ride with no Rav-Kav at all. Don't tell users they must visit a physical kiosk or pay the driver.
- Google Maps transit directions in Israel are often inaccurate for bus arrival times. The official source is the Moovit app or the Ministry of Transport GTFS feed. Agents should not rely solely on Google Maps.

## Troubleshooting

### Error: "Bus route information may be outdated"
Cause: Israeli bus routes and schedules change frequently, especially after Egged/Dan restructuring
Solution: Always note that schedules should be verified on Moovit or the bus company website. Provide the Moovit/Google Maps link for real-time data.

### Error: "National park is closed on requested date"
Cause: Parks may close for holidays, weather, or security
Solution: Check the Israel Nature and Parks Authority website (parks.org.il) for closures. Note that parks close early on Fridays and eves of holidays. Suggest alternative nearby attractions.