---
name: israeli-travel-planner
description: >-
  Plan domestic travel in Israel with local transportation, accommodations,
  national parks, and cultural considerations. Use when user asks about
  traveling in Israel, Israeli hotel chains, bus routes, Israel Railways,
  Rav-Kav card, national parks, "tiyul b'aretz", Dead Sea, Eilat, or trip
  planning within Israel. Covers Egged/Dan/Kavim buses, train schedules,
  Rashut HaTeva sites, Shabbat travel restrictions, and seasonal advice.
  Do NOT use for international flights, visa requirements, or overseas travel.
license: MIT
compatibility: No network required. Works offline with reference data.
metadata:
  author: skills-il
  version: 1.0.0
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
    he: תכנון טיולים בארץ עם תחבורה, לינה, אתרי טבע ושיקולים תרבותיים
    en: >-
      Plan domestic travel in Israel with local transportation, accommodations,
      national parks, and cultural considerations. Use when user asks about
      traveling in Israel, bus routes, Israel Railways, Rav-Kav card, national
      parks, Dead Sea, Eilat, or trip planning. Covers public transit, hotel
      chains, Rashut HaTeva sites, and Shabbat travel restrictions.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Travel Planner

## Instructions

### Step 1: Understand Israeli Transportation Options
Israel has multiple public and private transportation systems:

**Bus Companies:**
| Company | Hebrew | Coverage Area | Website |
|---------|--------|--------------|---------|
| Egged | אגד | Nationwide intercity, Jerusalem urban | egged.co.il |
| Dan | דן | Tel Aviv metro (Gush Dan) | dan.co.il |
| Kavim | קווים | Central Israel, Modi'in, Beit Shemesh | kavim-t.co.il |
| Metropoline | מטרופולין | Sharon region, Netanya, Hadera | metropoline.com |
| Superbus | סופרבוס | Modi'in-Jerusalem corridor, Ramla/Lod | superbus.co.il |
| Nateev Express | נתיב אקספרס | Beer Sheva, Negev region | nateevexpress.com |
| Afikim | אפיקים | Lower Galilee, Tiberias, Afula | afikim.co.il |
| Tnufa | תנופה | Upper Galilee, Golan | tnufa.co.il |

**Israel Railways (Rakevet Yisrael):**
| Route | Key Stops | Frequency | Travel Time |
|-------|-----------|-----------|-------------|
| Tel Aviv - Haifa | Herzliya, Netanya, Hadera, Binyamina | Every 20-30 min | ~1 hour |
| Tel Aviv - Jerusalem (Navot) | Ben Gurion Airport | Every 30 min | ~30 min (fast line) |
| Tel Aviv - Beer Sheva | Lod, Kiryat Gat | Every 30-60 min | ~1.5 hours |
| Haifa - Nahariya | Acre (Akko), Nahariya | Every 30 min | ~40 min |
| Tel Aviv - Ashkelon | Yavne, Ashdod | Every 20-30 min | ~45 min |
| Binyamina - Modi'in | Via Ben Gurion | Hourly | ~1 hour |

**Light Rail:**
- Jerusalem Light Rail (Rakevet Kala Yerushalayim): Red Line operational, Green/Blue lines under construction
- Tel Aviv Light Rail (Rakevet Kala Tel Aviv): Red Line opened 2023, connects Petah Tikva to Bat Yam via central Tel Aviv

**Rav-Kav Smart Card:**
- Rechargeable transit card for all public transport
- Two types: Personal (ishi, with photo) and Anonymous (anonimi)
- Purchase at train stations, bus central stations, or post offices
- Load passes: Daily (yomi), weekly (shvu'i), monthly (chodshi), or stored value
- Discounts: Students, soldiers, seniors, disabled

### Step 2: Plan Around Shabbat and Holidays
**Critical for travel planning in Israel:**

| Day/Period | Public Transit Status | Alternatives |
|-----------|----------------------|-------------|
| Friday afternoon (from ~2-4pm) | Buses/trains stop | Sherut (shared taxi), private taxi, driving |
| Saturday (Shabbat) | No buses/trains until ~Saturday evening | Sherut on select routes, taxis, walking |
| Saturday night (Motza'ei Shabbat) | Resumes ~30 min after Shabbat ends | Check exact time (varies by season) |
| Jewish holidays (Chagim) | Same as Shabbat | Same alternatives |
| Yom Kippur | ALL roads closed, no vehicles | Walking only, nationwide |
| Holiday eves | Early shutdown like Friday | Plan early departure |

**Shabbat times vary by season:**
- Summer: Shabbat starts ~7:30pm Friday, ends ~8:30pm Saturday
- Winter: Shabbat starts ~4:00pm Friday, ends ~5:15pm Saturday
- Always check exact times for the specific week (zmanim)

**Exception:** Haifa operates limited bus service on Shabbat.

### Step 3: Choose Accommodations
**Major Israeli Hotel Chains:**
| Chain | Hebrew | Style | Price Range | Key Locations |
|-------|--------|-------|-------------|---------------|
| Dan Hotels | מלונות דן | Luxury/Business | 800-2,500 NIS/night | Tel Aviv, Jerusalem, Eilat, Haifa, Caesarea |
| Isrotel | ישרוטל | Resort/Family | 600-2,000 NIS/night | Eilat, Dead Sea, Ramon, Tel Aviv |
| Fattal Hotels (Leonardo) | מלונות פתאל | Mid-range/Business | 500-1,500 NIS/night | Nationwide, largest chain |
| Atlas Hotels | מלונות אטלס | Boutique | 400-1,200 NIS/night | Tel Aviv (focused) |
| Prima Hotels | מלונות פרימה | Mid-range | 400-1,000 NIS/night | Jerusalem, Tiberias, Eilat, Tel Aviv |
| Herbert Samuel | הרברט סמואל | Boutique/Luxury | 700-2,000 NIS/night | Jerusalem, Tel Aviv, Herzliya |

**Alternative Accommodations:**
- Kibbutz guest houses (Tzimmer Kibbutzi): Rural, nature, affordable (300-800 NIS)
- Zimmer (country lodges): Popular in Galilee, Golan (400-1,500 NIS, weekends more expensive)
- Airbnb/Booking.com: Widely available
- Youth hostels (Akhsaniyot No'ar): Budget option (100-300 NIS)
- ILH - Israel Hostels: Backpacker-friendly chain

**Seasonal pricing:**
- Peak: Jewish holidays (Sukkot, Pesach), July-August, weekends year-round
- Off-peak: November-February (except holidays), Sunday-Thursday

### Step 4: National Parks and Nature Reserves
Rashut HaTeva VeHaGanim (Israel Nature and Parks Authority) manages:

| Site | Hebrew | Region | Highlights |
|------|--------|--------|------------|
| Masada | מצדה | Dead Sea | UNESCO site, Herod's fortress, sunrise hike |
| Ein Gedi | עין גדי | Dead Sea | Desert oasis, waterfalls, ibex, Dead Sea shore |
| Banias (Hermon Stream) | בניאס | Golan | Waterfall, Crusader ruins, river trail |
| Caesarea | קיסריה | Coast | Roman theater, Herodian harbor, Crusader city |
| Tel Dan | תל דן | Upper Galilee | Biblical springs, nature walk, Canaanite gate |
| Rosh HaNikra | ראש הניקרה | North Coast | Sea grottoes, cable car, Lebanese border |
| Timna Park | פארק תמנע | Eilat area | Solomon's Pillars, ancient copper mines |
| Ein Avdat | עין עבדת | Negev | Canyon, springs, Nabataean ruins |
| Beit She'an | בית שאן | Jordan Valley | Roman-Byzantine city, theater |
| Gamla | גמלא | Golan | Vulture observatory, waterfall, ancient fortress |
| Coral Beach | חוף אלמוג | Eilat | Snorkeling, coral reef reserve |
| Achziv | אכזיב | North Coast | Beach, Crusader ruins, sea pools |

**Entrance fees (2024 reference):**
- Adult: 22-39 NIS per site
- Child (5-18): 9-24 NIS
- Multi-site pass (Kartisiya): 6 sites for 110 NIS (adult), valid 14 days
- Annual subscription (Manuy Shanti): ~195 NIS, unlimited entries year-round

### Step 5: Plan Regional Itineraries

**Dead Sea Region (1-2 days):**
- Ein Gedi nature reserve + Ein Gedi beach
- Masada (sunrise hike recommended, cable car available)
- Dead Sea floating at public/resort beaches
- Qumran (Dead Sea Scrolls site)
- Tip: Lowest point on Earth (-430m), extremely hot in summer (40-45C)

**Eilat (2-4 days):**
- Coral Beach Nature Reserve (snorkeling)
- Underwater Observatory
- Timna Park (half day)
- Red Canyon hike
- Dolphin Reef
- Getting there: Flights (50 min from TLV), bus (4.5 hours), driving (3.5 hours)
- Tip: Tax-free shopping zone (no VAT)

**Galilee and Golan (2-3 days):**
- Tiberias (Tveria) as base, Sea of Galilee
- Banias waterfall and nature reserve
- Tel Dan Nature Reserve
- Golan winery tours (Ramat HaGolan)
- Mount Hermon (skiing in winter, Jan-Mar)
- Rosh Pina and Safed (Tzfat) old cities

**Jerusalem (2-4 days):**
- Old City: Western Wall, Church of Holy Sepulchre, Dome of the Rock
- Yad Vashem Holocaust Memorial
- Israel Museum (Dead Sea Scrolls)
- Mahane Yehuda Market (Shuk)
- Mount of Olives
- City of David archaeological site

**Tel Aviv (1-3 days):**
- Beaches: Gordon, Frishman, Banana Beach
- Jaffa Old City and flea market
- Carmel Market (Shuk HaCarmel)
- Neve Tzedek neighborhood
- Rothschild Boulevard and Bauhaus architecture
- Sarona Market

**Negev Desert (1-2 days):**
- Ramon Crater (Makhtesh Ramon), largest erosion crater in the world
- Ein Avdat canyon
- Sde Boker (Ben-Gurion's desert home)
- Stargazing (minimal light pollution)

### Step 6: Practical Travel Tips

**Weather by season:**
| Season | Months | Temperature | Notes |
|--------|--------|-------------|-------|
| Spring | March-May | 18-28C | Best time, wildflowers (Kalaniyot in Feb-Mar) |
| Summer | June-August | 28-40C+ | Hot, beach season, Dead Sea extremely hot |
| Autumn | September-November | 22-32C | Holiday season, pleasant |
| Winter | December-February | 8-18C | Rain in north/center, skiing on Hermon, warm in Eilat |

**Useful phone numbers:**
- Police (Mishtara): 100
- Ambulance (Magen David Adom): 101
- Fire (Kiba'ei Esh): 102
- Tourist information: *3888

**Money:**
- Currency: New Israeli Shekel (NIS/ILS)
- Credit cards widely accepted (Visa, Mastercard, Amex less common)
- ATMs (Kaspomat) available everywhere
- Tipping: 10-15% at restaurants, round up for taxis

**Water:**
- Tap water is safe to drink throughout Israel
- Carry extra water in desert/Dead Sea region (minimum 3 liters per person per day)

## Examples

### Example 1: Weekend Getaway
**Input:** "Plan a weekend trip to the Galilee for a couple"
**Output:** Thursday departure (before Friday shutdown), drive or bus to Tiberias. Friday morning: Ein Gedi HaGoshrim or similar nature hike. Friday lunch in Rosh Pina. Pre-Shabbat check-in at zimmer. Saturday: Relax, walk around Tzfat old city (walking distance). Motza'ei Shabbat return or Sunday morning. Estimate budget: zimmer (800-1,500 NIS/night), meals (200-400 NIS/day), activities (100-200 NIS).

### Example 2: Family National Parks Trip
**Input:** "We want to visit national parks with kids, which ones are best?"
**Output:** Recommend family-friendly parks: Ein Gedi (easy trails, water), Banias (waterfall, moderate walk), Caesarea (open, interactive), Coral Beach Eilat (snorkeling). Suggest kartisiya multi-site pass for savings. Note: bring water, sunscreen, hats. Best season: spring or autumn.

### Example 3: Dead Sea Day Trip
**Input:** "How do I get from Tel Aviv to the Dead Sea for a day?"
**Output:** Options: Drive (1.5 hours via Route 90), Egged bus to Ein Gedi/Ein Bokek. Recommend early departure (7am). Visit Ein Gedi reserve (morning), float at Ein Bokek public beach (afternoon). Bring: towel, flip-flops, water, avoid shaving day-of (salt stings). Return by 5pm to avoid dark mountain roads.

### Example 4: Budget Travel
**Input:** "Cheapest way to travel around Israel for a week"
**Output:** Use Rav-Kav with stored value for all buses/trains. Stay at hostels (ILH chain, 100-200 NIS/night). Eat at shukim (markets) and falafel stands (15-30 NIS/meal). Buy kartisiya for parks. Travel Sunday-Thursday for lowest prices. Total estimate: 2,500-4,000 NIS for 7 days including transport, accommodation, food, activities.

## Troubleshooting

### Error: "No buses running on Saturday"
Cause: Shabbat - public transit stops Friday afternoon through Saturday night
Solution: Use sherut (shared taxi) on select intercity routes (e.g., Tel Aviv-Jerusalem, Tel Aviv-Haifa). Book private taxi via Gett or Yango apps. Plan travel for before Shabbat or after Motza'ei Shabbat. Note: Haifa has limited Shabbat bus service.

### Error: "National park is full / entrance denied"
Cause: Popular parks fill up on holidays and weekends (especially Ein Gedi, Banias)
Solution: Arrive early (before 9am) or book online in advance at parks.org.il. Consider visiting on weekdays instead. Some parks close entry when capacity is reached but allow exit.

### Error: "Rav-Kav not working on this bus"
Cause: Card not loaded, wrong pass type, or technical issue
Solution: Ensure card has stored value or valid pass. Some regional operators had integration delays. Keep receipt from last load. If card is damaged, replace at train station or designated offices (free replacement if under warranty).
