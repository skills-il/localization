# Domain Checklist: Israeli Travel Planner (public transport + national parks)

Scope: domestic travel in Israel relying on public transport and national parks, for a 2026 trip. Used to review the skill for current, correct fare / ticketing / park-fee / closure guidance. Every figure below is backed by a row in evidence.json.

## Must cover (a traveler is misled without these)

- **Current single-ride fare and the 90-minute transfer.** Post-25-April-2025 Derech Shava: 8 NIS for a ride up to 15 km, including 90 minutes of free transfers in the zone. Source: https://pti.org.il/DerekhShava/
- **Current single-ride distance-band prices (bus only, effective 25.04.2025).** up to 15 km = 8 ; up to 40 km = 14.5 ; up to 75 km = 19 ; up to 120 km = 19 ; up to 225 km = 30.5 ; over 225 km = 74 NIS. These superseded the pre-reform 5.5 / 12 / 16 / 16 / 27 figures. Source: https://pti.org.il/DerekhShava/
- **Daily caps by band (bus only).** up to 15 km ~11.5 ; up to 40 km ~21 ; up to 75 km ~27 ; up to 120 km ~30.5 ; up to 225 km ~52.5 NIS ; over 225 km has no daily cap. Source: https://pti.org.il/DerekhShava/
- **Nationwide unlimited monthly (Chofshi Artzi).** ~315 NIS for bus + light rail (up to 225 km). Source: https://ravkavonline.co.il/en/derekh-shava
- **Senior free-travel age.** 67+ ride free nationwide (lowered from 75, effective 25.04.2025). Source: https://ravkavonline.co.il/en/derekh-shava
- **Payment medium shift (Rav-Kav to app/EMV).** Rav-Kav still works; physical Rav-Kav can be loaded remotely via Rav-Kav Online / HopOn (Rav-Pass) apps + ravkavonline.co.il; EMV contactless (physical credit card, Apple Pay, Google Pay at the validator) is spreading but not universal. Source: https://www.egged.co.il/en/information-for-passengers/rav-kav-and-payment-apps
- **EMV is not Egged-only.** Dan accepts contactless on central-Israel buses since October 2022, Israel Railways accepts EMV at the gates, and Egged ran an early-2026 pilot in Eilat, Jerusalem and Haifa. Source: https://www.calcalistech.com/ctech/articles/0,7340,L-3741573,00.html
- **National-park entry fees AND the Masada cable-car surcharge.** Single adult entry ~31-46 NIS at main tourist sites (Ein Gedi 31, Masada 37, Caesarea 46). The Masada cable car is a separate charge the multi-site cards do NOT cover: official entrance ~37 NIS adult (21 child, 19 senior); the cable car does not include entrance, at ~32 NIS one-way (16 child) / ~54 NIS round-trip (32 child). Source: https://www.parks.org.il/article/price/ ; https://en.parks.org.il/reserve-park/masada-national-park/
- **Park multi-site tourist cards.** Blue (3 sites / 2 weeks) 90 NIS, Green (6 sites / 2 weeks) 130 NIS, Orange (unlimited / 2 weeks) 175 NIS; tourists only, exclude the Masada cable car. Source: https://en.parks.org.il/article/money-saving-tickets/
- **Park early closing on Fridays / holiday eves.** Parks close earlier on Fri and holiday eves; verify closures at parks.org.il. Source: https://www.parks.org.il/article/price/

## Should cover

- **Matmon annual subscription** (locals' alternative to tourist cards): ~181 NIS individual; couple and family tiers cost more (verify the current tiers). Source: https://www.parks.org.il/article/price/
- **Israel Railways contactless.** Trains accept tap-to-pay EMV at gates, not just Egged buses. Source: https://www.calcalistech.com/ctech/articles/0,7340,L-3741573,00.html
- **Galilee / peripheral rail lines.** Acre-Karmiel (2017) and Jezreel Valley Haifa-Beit She'an (2016) lines. Source: https://en.wikipedia.org/wiki/Railway_to_Karmiel
- **Live-data caveat.** Google Maps transit times unreliable in Israel; use Moovit / MoT GTFS. Source: operational knowledge.
- **Hebrew route-letter suffix** (17-aleph is not 17). Source: operational knowledge.
- **Bus operator list incl. rebrands** (Electra-Afikim, Superbus, Nateev Express, Metropoline). Source: https://en.wikipedia.org/wiki/Electra-Afikim
- **Eilat VAT-free zone** (saving the standard 18% VAT on eligible goods). Source: https://sovos.com/regulatory-updates/vat/israel-vat-rate-increase-to-18-from-january-1-2025/
- **Reserved/booking-only intercity lines** (e.g. 421 to the Dead Sea runs limited times, ~133 min, booking advised). Source: Moovit line 421 route page (see deadsea-421-fare-band in evidence.json).

## Out of scope

- International flights / outbound travel (skill is domestic; ben-gurion-flights MCP handles arrivals/departures separately)
- Car-rental contracts, insurance, fuel-card mechanics (gas price ceiling is a context note only)
- Hotel booking transactions and real-time room pricing (skill gives qualitative tiers only)
- Real-time schedules / live arrivals (delegated to MCP servers: openbus, israel-railways, routes-israel)
- Hiking trail navigation specifics (delegated to israel-hiking MCP)

## Authoritative sources

- Rav-Kav Online (fares, reform, remote loading): https://ravkavonline.co.il/en/derekh-shava
- National Authority for Public Transport (PTI), fare tables: https://pti.org.il/DerekhShava/
- Egged payment methods: https://www.egged.co.il/en/information-for-passengers/rav-kav-and-payment-apps
- Israel Nature and Parks Authority price list: https://www.parks.org.il/article/price/
- Israel Nature and Parks Authority money-saving tickets: https://en.parks.org.il/article/money-saving-tickets/
- Masada National Park (entry + cable car): https://en.parks.org.il/reserve-park/masada-national-park/
