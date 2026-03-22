---
name: israeli-travel-planner
description: >-
  Plan domestic travel in Israel with local transportation, accommodations, national
  parks, and cultural considerations. Use when user asks about traveling in Israel,
  Israeli hotel chains, bus routes, Israel Railways, Rav-Kav card, national parks,
  tiyul b'aretz, Dead Sea, Eilat, or trip planning within Israel. Covers Egged/Dan/Kavim
  buses, train schedules, Rashut HaTeva sites, Shabbat travel restrictions, and seasonal
  advice.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode,
  Codex.
metadata:
  author: skills-il
  version: 1.1.0
  category: localization
  tags:
    he:
    - תיירות
    - תחבורה
    - טיולים
    - מלונות
    - גנים-לאומיים
    - ישראל
    en:
    - tourism
    - transportation
    - travel
    - hotels
    - national-parks
    - israel
  display_name:
    he: מתכנן טיולים בישראל
    en: Israeli Travel Planner
  display_description:
    he: >-
      תכנון טיולים בארץ עם תחבורה מקומית, לינה, אתרי טבע ושיקולים תרבותיים. שימוש
      כשצריך מידע על אוטובוסים, רכבת ישראל, רב-קו, גנים לאומיים, מלונות, או תכנון
      נסיעות בהתחשב בשבת וחגים.
    en: >-
      Plan domestic travel in Israel with local transportation, accommodations, national
      parks, and cultural considerations. Use when user asks about traveling in Israel,
      Israeli hotel chains, bus routes, Israel Railways, Rav-Kav card, national parks,
      tiyul b'aretz, Dead Sea, Eilat, or trip planning within Israel. Covers Egged/Dan/Kavim
      buses, train schedules, Rashut HaTeva sites, Shabbat travel restrictions, and
      seasonal advice.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
  - antigravity
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

## Rav-Kav Card
Rechargeable smart card for all public transport. Types: Personal (with photo) and Anonymous. Load passes: daily, weekly, monthly, or stored value.

## Shabbat Travel
Public transit stops Friday afternoon through Saturday night. Alternatives: sherut (shared taxi), private taxis (Gett/Yango), driving. Haifa has limited Shabbat bus service. Yom Kippur: ALL roads closed.

## Hotel Chains
- Dan Hotels: Luxury (1,200-3,500 NIS/night)
- Isrotel: Resort/Family (900-2,800 NIS)
- Fattal/Leonardo: Mid-range (700-2,200 NIS)
- Zimmerim: Country lodges in Galilee/Golan (600-2,200 NIS)

Note: Prices are approximate and should be verified before booking as rates fluctuate seasonally.

## Top National Parks (Rashut HaTeva)
Masada, Ein Gedi, Banias, Caesarea, Tel Dan, Rosh HaNikra, Timna Park, Ein Avdat.
For current pricing on individual park entries and multi-site passes, visit parks.org.il or contact parks directly.

## Regional Highlights
- Dead Sea: Ein Gedi + Masada sunrise + floating
- Eilat: Coral Beach, Timna, tax-free shopping
- Galilee/Golan: Banias, Tel Dan, wineries, Tzfat
- Jerusalem: Old City, Yad Vashem, Mahane Yehuda
- Tel Aviv: Beaches, Jaffa, Carmel Market, Neve Tzedek

## Examples

### Example 1: Plan a Weekend Trip to the Dead Sea
User says: "Plan a weekend trip from Tel Aviv to the Dead Sea"
Actions:
1. Transport: Egged bus 421 from Tel Aviv Central Station (2.5 hours, ~42 NIS) or rental car via Route 90
2. Accommodation: Ein Bokek hotel strip (450-1,200 NIS/night) or Ein Gedi hostel (220-350 NIS/night)
3. Activities: Ein Gedi Nature Reserve (entry fees at parks.org.il), Masada sunrise hike, Dead Sea beach (free public beaches at Ein Bokek)
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

## Gotchas
- Public transportation in Israel does not operate on Shabbat (Friday afternoon to Saturday evening) in most cities. Agents may plan Saturday itineraries that rely on buses or trains. Exceptions: Haifa has limited Shabbat service; shared taxis (sherut) run on some routes.
- Israeli bus numbers and route names use Hebrew characters. Agents may not recognize that route 17-aleph is a different route from 17. Always include the Hebrew letter suffix.
- The Rav-Kav card (Israel's transit smart card) cannot be purchased or loaded remotely via API. Agents may suggest digital loading when only physical kiosk or driver loading is available.
- Google Maps transit directions in Israel are often inaccurate for bus arrival times. The official source is the Moovit app or the Ministry of Transport GTFS feed. Agents should not rely solely on Google Maps.

## Troubleshooting

### Error: "Bus route information may be outdated"
Cause: Israeli bus routes and schedules change frequently, especially after Egged/Dan restructuring
Solution: Always note that schedules should be verified on Moovit or the bus company website. Provide the Moovit/Google Maps link for real-time data.

### Error: "National park is closed on requested date"
Cause: Parks may close for holidays, weather, or security
Solution: Check the Israel Nature and Parks Authority website (parks.org.il) for closures. Note that parks close early on Fridays and eves of holidays. Suggest alternative nearby attractions.