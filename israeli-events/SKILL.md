---
name: israeli-events
description: Find Israeli live events (concerts, theatre, comedy, dance, opera, children's shows, festivals), venue logistics (parking, transport, nearby restaurants, capacity, accessibility), and complete outing plans. Bilingual Hebrew/Russian. Use when the user asks about live events in Israel; or wants venue parking/transport info; or asks "what should I do tonight in Tel Aviv / Haifa / Jerusalem"; or wants ticket purchase links for Israeli shows.
license: MIT
---

# Israeli Live Events Skill

This skill provides four capabilities for Israeli live entertainment, all backed by the public agentic API at `https://www.venues-israel.com/api/`. Bilingual (Hebrew `he` + Russian `ru`); the API is public and unauthenticated.

## When to use this skill

Trigger on any of these:

- The user asks about live events, concerts, theatre, comedy, dance, opera, musicals, children's shows, or festivals **in Israel**.
- The user asks about a specific Israeli venue's parking, public transport, nearby restaurants, capacity, accessibility, or directions.
- The user asks "what should I do tonight / this weekend in [Israeli city]?" or wants outing recommendations.
- The user wants to find a ticket purchase link for an Israeli event.

Do NOT trigger for:

- Events outside Israel (no coverage).
- Sports events (limited coverage; the directory is built around cultural/entertainment venues).
- Movie listings (the API is for live events, not cinema).

## The four tools

### 1. `searchEvents` — filtered event search

Use for **specific filtered queries**: "concerts in Tel Aviv next month under 300 NIS", "children's shows in Haifa".

Inputs:
- `city` (string, optional) — slug like `tel-aviv`, `haifa`, `jerusalem`, `beer-sheva`, `ramat-gan`.
- `genre` (enum, optional) — one of `concert | theater | standup | musical | dance | classical | opera | children | festival | lecture`.
- `lang` (`he` | `ru`, default `he`) — selects localized names + descriptions + affiliate provider.
- `date_from` (`YYYY-MM-DD`, optional)
- `price_max` (integer NIS, optional)
- `artist` (string, optional, partial match)
- `limit` (1-50, default 10)

Returns an array of events with affiliate purchase links (`kassa.co.il` for Russian, `kartisim.co.il` for Hebrew).

### 2. `getVenueInfo` — venue logistics

Use when the user asks about **a specific venue's parking, transport, nearby restaurants, or accessibility**. They typically reference the venue by name; first call `searchEvents` if you need to discover the venue's slug.

Inputs:
- `slug` (string, **required**) — venue slug like `auditorium-rozin-tel-aviv`. Find via `searchEvents` event objects' `venue.name` if needed.
- `lang` (`he` | `ru`, default `he`).

Returns: parking + public transport + up to 5 nearby restaurants + capacity + accessibility + Google rating + a `data_completeness` object (`{transport, parking, restaurants, capacity}` booleans). When `data_completeness.restaurants === false`, the venue has fewer than 3 nearby restaurants on file (typically rural).

**Coverage note:** 96.5% of venues have transport data; 84% have full logistics. All major cities at 100% except Jerusalem (92%), Ashkelon (75%), Netanya (50%).

### 3. `planOuting` — composed event + venue + restaurants

Use when the user has chosen a specific event and wants a **complete outing plan** — what to know about the venue, where to eat nearby, when to arrive.

Inputs:
- `event_slug` (string, **required**) — from `searchEvents` results.
- `lang` (`he` | `ru`, default `he`).

Returns: event details + full venue logistics + top 3 nearby restaurants within 600m + suggested arrival time (30 min before show) + parking recommendation + the affiliate purchase link.

### 4. `recommendEvents` — natural-language recommendations

Use when the user gives a **free-form, fuzzy preference** rather than specific filters: "something romantic for date night", "a high-energy concert to lift my mood", "a kids show this weekend that won't break the bank".

Inputs:
- `query` (string, **required**) — the user's free-form description.
- `lang` (`he` | `ru`, default `he`) — strict language filter (only events with `lang` content are returned).
- `limit` (1-50, default 20).

Returns the parsed intent + a ranked event list. The intent fields show what the underlying Claude Haiku-based intent extractor inferred; surface this back to the user so they can correct misinterpretations.

## Hebrew & Russian language handling

- The API responses are **bilingual**: pass `lang=he` for Hebrew names + Hebrew checkout, `lang=ru` for Russian names + Russian checkout. Russian users go through `kassa.co.il`; Hebrew users through `kartisim.co.il`. The affiliate link in the response is already routed correctly.
- Venue names + addresses are returned in **Hebrew** for both `he` and `ru` (a Russian venue-name backfill is a Phase-1 follow-up). When responding to a Russian user, you can transliterate venue names if helpful, but the API field is canonical Hebrew.

## Common patterns

### "Find me X in city Y"
1. `searchEvents` with `city` and any other filters.
2. Surface 3-5 top results with name, date, price, image, affiliate_link.

### "What's at venue Z?"
1. `searchEvents` with the venue's city to find events; filter results by `venue.name` matching Z.
2. Optionally `getVenueInfo` to add logistics.

### "I'm going to event E — plan it"
1. `planOuting` with `event_slug`.
2. Surface the structured response.

### "I'm in the mood for…"
1. `recommendEvents` with the user's natural-language query.
2. Show the parsed intent + top 3 ranked events.

## Error handling

- All four tools return a `200` with content or a `4xx`/`5xx` with `{error: string}`. Surface the `error` text to the user in their preferred language; don't retry blindly.
- `getVenueInfo` returns `404` when the slug doesn't exist. Suggest the user provide the venue name or city for a better lookup.
- `planOuting` returns `404` when the event slug doesn't exist or has expired. Re-query `searchEvents` for current events.

## Provider + license

- **Provider:** [venues-israel.com](https://www.venues-israel.com), `venues.israel@gmail.com`.
- **License:** MIT.
- **API docs:** [`https://www.venues-israel.com/api/openapi.json`](https://www.venues-israel.com/api/openapi.json).
- **Agent Card:** [`https://www.venues-israel.com/.well-known/a2a/agent-card`](https://www.venues-israel.com/.well-known/a2a/agent-card).
