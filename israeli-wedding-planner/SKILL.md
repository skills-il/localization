---
name: israeli-wedding-planner
description: >-
  Plan an Israeli wedding from engagement to chuppah, covering venue selection
  (ulmot, ganot aruim), vendor comparison via Israeli platforms (Celebrate,
  Engaged, Save A Date, Walla Wedding), budget planning (~100-140K NIS average),
  Rabbinate registration (tik nisuin, teudat ravakut), halachic requirements
  (mikveh, ketuba), guest management, per-plate cost optimization, seasonal
  pricing, and timeline creation. Use when user asks about "chatuna b'yisrael",
  Israeli wedding planning, wedding budget, "ulam aruim", "ulmot", "ganim",
  wedding vendors, Rabbinate requirements, "tik nisuin", ketuba, or wedding
  timeline. Prevents common mistakes like missing Rabbinate deadlines, overpaying
  on Thursday weddings, or forgetting AKUM fees. Do NOT use for destination
  weddings abroad, non-Jewish religious ceremonies, or divorce proceedings.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.0.0
  category: localization
  tags:
    he:
      - חתונה
      - אולם-אירועים
      - רבנות
      - תקציב
      - ספקים
      - ישראל
    en:
      - wedding
      - event-venue
      - rabbinate
      - budget
      - vendors
      - israel
  display_name:
    he: מתכנן חתונות בישראל
    en: Israeli Wedding Planner
  display_description:
    he: >-
      תכנון חתונה ישראלית מאירוסין ועד חופה: בחירת אולם או גן אירועים, השוואת
      ספקים דרך פלטפורמות ישראליות (Celebrate, מאורסים, Save A Date, וואלה חתונות),
      תכנון תקציב (ממוצע 100-140 אלף שקל), רישום ברבנות (תיק נישואין, תעודת
      רווקות), דרישות הלכתיות (מקווה, כתובה), ניהול מוזמנים, אופטימיזציה של
      מחיר למנה, תמחור עונתי ובניית לוח זמנים.
    en: >-
      Plan an Israeli wedding from engagement to chuppah: venue selection, vendor
      comparison via Israeli platforms, budget planning (~100-140K NIS average),
      Rabbinate registration, halachic requirements, guest management, per-plate
      cost optimization, seasonal pricing, and timeline creation. Prevents common
      mistakes like missing Rabbinate deadlines or overpaying on popular weekdays.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Wedding Planner

## Wedding Budget Breakdown

Average Israeli wedding cost: **100,000-140,000 NIS** (2025-2026 data). The single largest expense is the venue and catering.

| Category | Typical Range (NIS) | % of Budget | Notes |
|----------|-------------------|-------------|-------|
| Venue + catering | 60,000-100,000 | 55-65% | Per-plate x guests. Biggest variable |
| Photography + video | 8,000-20,000 | 8-12% | Still + video package |
| Music (DJ or band) | 4,000-15,000 | 4-8% | Plus AKUM license fee |
| Wedding dress | 3,000-15,000 | 3-8% | Purchase, rental, or custom |
| Groom's suit | 1,500-5,000 | 1-3% | Purchase or rental |
| Makeup + hair | 2,000-5,000 | 2-3% | Bride + optional entourage |
| Flowers + design | 2,000-10,000 | 2-5% | Most venues work with external designers |
| Invitations + magnets | 1,000-3,000 | 1-2% | Custom magnets are Israeli tradition |
| Rabbinate registration | ~710 | <1% | Fixed fee (40% discount for olim chadashim) |
| Other (transport, gifts, tips) | 3,000-8,000 | 3-5% | Shuttle bus, welcome gifts |

### Per-Plate Cost by Region and Venue Type

| Venue Type | Central Israel | Periphery | Notes |
|-----------|---------------|-----------|-------|
| Budget hall | 200-280 NIS | 180-250 NIS | Basic menu, weekday |
| Mid-range hall | 280-380 NIS | 250-320 NIS | Most common choice |
| Premium hall/garden | 380-500 NIS | 320-420 NIS | Higher-end catering |
| Luxury venue | 500-800+ NIS | 400-600 NIS | Top-tier Tel Aviv venues |

### Day-of-Week Pricing

| Day | Price Impact | Notes |
|-----|-------------|-------|
| Sunday-Wednesday | Baseline | Cheapest option |
| Thursday | +10-20% | Very popular, nearly as expensive as peak |
| Friday daytime | +10-15% | Must end before Shabbat, time pressure |
| Saturday night (motzei Shabbat) | +5-15% | Premium for convenience |

### Seasonal Pricing

| Season | Price Impact | Notes |
|--------|-------------|-------|
| Winter (Nov-Feb) | Cheapest | Rain risk, but best for negotiation |
| Spring (Mar-May) | Mid-range | Garden weddings popular |
| Summer (Jun-Aug) | Most expensive | Peak demand, book 12+ months ahead |
| Sefirat HaOmer | N/A | 33 days of restricted weddings (Pesach to Lag BaOmer) |
| Three Weeks (Tammuz-Av) | N/A | No weddings from 17 Tammuz to 9 Av |

**Negotiation tip:** Close deals with vendors in winter, even for summer weddings. Vendors are more willing to negotiate when their calendar is empty.

## Rabbinate Registration (Tik Nisuin)

### Timeline

Open a marriage file at your local Religious Council **21-90 days before the wedding**. Do not leave this to the last month.

### Required Documents

| Document | Who | Notes |
|----------|-----|-------|
| Teudat Zehut (ID) | Both | Original, not copy |
| 3 passport photos | Both | Recent photos |
| Parents' Ketuba | Both | Original or certified copy |
| Teudat Ravakut | Both (if registering outside your city) | Certificate of bachelorhood from your local Rabbinate |
| Registration fee | Both | ~710 NIS (40% discount for olim within 2 years) |
| Kosher certificate of venue | Couple | Must be from the Rabbinate, not private kashrut |
| Birth certificate | Olim/converts | Required for immigrants |
| Conversion documents | Converts | Original papers + rabbi's letter |

### Process Steps

1. **Gather documents** -- collect all items above
2. **Visit local Religious Council** -- both bride and groom must appear together
3. **Interview** -- the Rabbinate official verifies Jewish status and eligibility
4. **Schedule chuppah** -- the Rabbinate assigns a mesader kiddushin (officiating rabbi) or you request your own
5. **Bride's mikveh visit** -- required before the wedding, typically 1-7 days before
6. **Wedding day** -- mesader kiddushin conducts chuppah, signs ketuba, witnesses sign

### Common Rabbinate Pitfalls

- Kohanim cannot marry divorced women or converts (must verify before planning)
- If parents married abroad, additional documentation proving Jewish status may be required
- Some Religious Councils have long wait times -- book early
- The Rabbinate-approved mesader kiddushin is free; choosing your own rabbi is optional and additional cost

## Vendor Selection Guide

### Israeli Wedding Platforms

| Platform | URL | Specialty |
|----------|-----|-----------|
| Celebrate (Celebrite) | celebrateisrael.co.il | Full vendor directory, easy comparison |
| Engaged (Meorasim) | engaged.co.il | Deals and discounts in 25+ categories |
| Save A Date | saveadate.co.il | Vendor ratings and reviews |
| Walla Wedding | mazaltov.walla.co.il | Israel's largest wedding portal |
| Mithatnimim Group | mithatnimgroup.com | Recommended vendors index |
| MyWedPlan | mywedplan.online | Wedding management tools + vendor directory |

### Vendor Categories and What to Check

| Vendor | Key Questions | Red Flags |
|--------|--------------|-----------|
| Venue (ulam/gan) | Per-plate price, minimum guests, included services, rain backup | No written contract, unclear cancellation policy |
| Photographer | Portfolio review, number of edited photos, drone option, delivery timeline | No contract for album delivery date |
| Videographer | Highlight reel + full ceremony, drone, delivery time | More than 3 months delivery |
| DJ/Band | Equipment included, AKUM fee covered, playlist flexibility | Not mentioning AKUM (you will pay it anyway) |
| Makeup artist | Trial session, travel to venue, entourage pricing | No trial before booking |
| Florist/designer | Centerpieces, chuppah design, venue coordination | Not visiting venue before event |

### AKUM (Israeli Musicians' Union)

Any public performance of music at a wedding requires an **AKUM license fee**. The fee varies by event parameters (check current tariffs at acum.org.il). This covers royalties to songwriters and composers. Either the DJ/band or the couple pays it -- clarify in the contract. Without it, the DJ risks a fine.

## Wedding Timeline Template

### 12 Months Before
- Set budget and guest count estimate
- Book venue (for summer weddings, book 12-18 months ahead)
- Start Rabbinate document gathering

### 8-10 Months Before
- Book photographer and videographer
- Book DJ or band
- Choose wedding dress (allow 4-6 months for alterations)

### 6 Months Before
- Book makeup artist and hair stylist
- Order invitations and save-the-date magnets
- Book florist/designer

### 3 Months Before
- Open Rabbinate file (tik nisuin)
- Finalize guest list
- Arrange transportation (shuttle bus if needed)

### 1 Month Before
- Final dress fitting
- Confirm all vendors in writing
- Prepare seating chart
- Bride schedules mikveh visit

### 1 Week Before
- Confirm final guest count with venue
- Prepare wedding day timeline for vendors
- Groom's aufruf (Torah reading on preceding Shabbat, if applicable)

### Wedding Day
- Kabbalat panim (reception): bride and groom greet guests separately
- Badeken (veiling): groom covers bride's face
- Chuppah ceremony: ketuba signing, ring, sheva brachot
- Yichud: couple's private moment after chuppah
- Dinner and dancing

## Guest Management

### Israeli Wedding Norms

| Aspect | Typical | Notes |
|--------|---------|-------|
| Guest count | 200-400 | Israeli weddings are large by global standards |
| RSVP rate | ~70-80% | Expect 20-30% no-shows |
| Gift (matana) | 250-400 NIS/person | Cash in envelope, covers the plate cost |
| Plus-ones | Expected | Couples invited together by default |
| Children | Varies | Specify on invitation if children are/aren't welcome |
| Colleagues | Common | Israeli culture includes workplace invitations |

### Matana (Cash Gift) Expectations

Guests typically give cash to cover their plate cost plus a small addition:
- **Close family:** 500-1,000 NIS per person
- **Friends:** 300-500 NIS per person
- **Colleagues/acquaintances:** 250-350 NIS per person
- **Couples:** Double the individual amount

## Examples

### Example 1: Budget Wedding Planning
User says: "We want to plan a wedding in Israel for under 100,000 NIS"

Actions:
1. Suggest weekday (Sun-Wed) in winter for lowest venue pricing
2. Target periphery venues (Sharon, Shfela) for 200-280 NIS/plate
3. Limit guest list to 200 (realistic budget: 200 x 250 NIS = 50K for venue)
4. Allocate remaining 50K across photographer (8K), DJ (5K), dress (5K), design (3K), Rabbinate (710), and contingency
5. Recommend negotiating in winter months even for spring/summer dates

Result: Detailed budget spreadsheet with per-vendor allocation.

### Example 2: Rabbinate Registration
User says: "What do we need for the Rabbinate? Our wedding is in 2 months"

Actions:
1. Flag urgency: must open tik nisuin at least 21 days before
2. List all required documents (see Rabbinate section)
3. Check if registering in home city (no teudat ravakut needed) or elsewhere
4. Remind about bride's mikveh scheduling
5. Mention that Kohanim have marriage restrictions -- ask if relevant

Result: Document checklist with timeline for completion.

### Example 3: Vendor Comparison
User says: "We're comparing 3 venues in the center, how do we decide?"

Actions:
1. Create comparison table: per-plate price, minimum guests, included services
2. Check if price includes DJ setup area, chuppah structure, parking
3. Ask about rain backup plan (critical for garden venues)
4. Verify Rabbinate kashrut certificate for each venue
5. Suggest visiting on the same day of week as planned wedding

Result: Side-by-side venue comparison with total cost projections.

## Bundled Resources

### References
- `references/wedding-budget-calculator.md` -- Detailed budget template with Israeli cost benchmarks
- `references/rabbinate-checklist.md` -- Step-by-step Rabbinate registration guide with document checklist

## Gotchas

### 1. AKUM Fee Surprise
Agents often forget the AKUM (Israeli Musicians' Union) license fee when calculating music costs. This is mandatory for any public music performance at weddings. The fee varies by event parameters (check acum.org.il for current tariffs). Always include it in budget calculations and clarify in the DJ/band contract who pays.

### 2. Rabbinate Deadline Window
The tik nisuin must be opened 21-90 days before the wedding -- not earlier, not later. Agents may suggest "start as early as possible" but the Rabbinate will reject applications filed more than 90 days out. Conversely, less than 21 days leaves no buffer for missing documents.

### 3. Sefirat HaOmer and Three Weeks Restrictions
Agents commonly schedule weddings during the 33 days of Sefirat HaOmer (Pesach to Lag BaOmer) or the Three Weeks (17 Tammuz to 9 Av) when traditional Jewish weddings are not held. Always check the Hebrew calendar before suggesting dates.

### 4. Per-Plate Does Not Include Everything
The per-plate price at Israeli venues typically covers food and basic hall rental, but NOT: DJ setup area rental, valet parking, design/flowers, external catering surcharges, or Shabbat early-closure surcharges. Always ask what is and isn't included.

### 5. Kashrut Certificate Mismatch
The Rabbinate requires the venue's kashrut certificate to be from the local Religious Council (Rabbinate), not from a private kashrut organization (like Badatz or Mehadrin). If the venue only has private kashrut, the Rabbinate may not approve the wedding there.

## Troubleshooting

### Error: "Rabbinate rejected our application"
Cause: Missing documents (most commonly parents' ketuba or teudat ravakut)
Solution: Contact the specific Religious Council to ask which document is missing. If parents' ketuba is lost, request a copy from the Rabbinate where parents married.

### Error: "Venue price increased after booking"
Cause: Contract may allow price adjustments for guest count changes or menu upgrades
Solution: Review the original contract. Israeli consumer protection law requires written agreements. If no written contract exists, the verbal price should hold -- consider filing a complaint with the Consumer Protection Authority.

### Error: "Cannot find mesader kiddushin"
Cause: Did not request through Rabbinate or private rabbi is unavailable
Solution: The local Religious Council can assign a mesader kiddushin at no extra cost. For a specific rabbi, contact them directly and then inform the Rabbinate of your choice.
