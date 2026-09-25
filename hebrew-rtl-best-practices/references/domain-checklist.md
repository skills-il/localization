# Domain Checklist: Hebrew RTL for web apps

Anchor for Expert Review. Scope: right-to-left layout and bidirectional text for Hebrew web UIs (HTML/CSS, Tailwind, React/Next.js, MUI). Each row names the step that covers it.

## Must cover (core)
| Item | Covered in | Basis |
|---|---|---|
| `lang="he"` + `dir="rtl"` on `<html>`, not CSS `direction` alone | Step 1 | HTML spec directionality; W3C i18n inline-bidi-markup |
| Physical-to-logical property mapping (margin, padding, border, inset, text-align, float) | Step 2, reference | MDN CSS logical properties |
| `:dir()` vs `[dir]` selectors, with support versions | Step 2 | MDN `:dir()`, caniuse |
| Bidi isolation: `<bdi>`, `<bdo>`, `dir`, `unicode-bidi` values, and when NOT to use `bidi-override` | Step 3 | MDN unicode-bidi, UAX #9 |
| Phone numbers: which formats actually reorder (spaces, `+972`) vs which do not (hyphen-only) | Step 3, Example 2 | UAX #9 rule W4, browser render |
| Formatting vs isolation: `Intl` he-IL currency/date output, do not force LTR on RLM-marked output | Step 3 | CLDR he currency pattern |
| Hebrew calendar dates via `-u-ca-hebrew` | Step 3 | MDN Intl.DateTimeFormat |
| Form inputs: `dir="auto"`; tel is LTR by default; email/url deliberate LTR with the Hebrew-IDN caveat | Step 3 | HTML spec directionality; IANA `.ישראל` |
| Icon mirroring: which icons flip, which do not, horizontal flip not rotate | Step 4 | practice |
| Hebrew typography: caselessness, nikkud vertical room, letter-spacing used for emphasis | Step 5 | Unicode case FAQ, W3C hlreq |
| Tailwind v4 logical utilities, the v4.2 inset rename, physical-only utilities needing `rtl:` | Step 6 | Tailwind release notes, local compile |
| Next.js App Router locale layout (`app/[locale]/layout.tsx`) setting `lang`/`dir` | Step 6 | Next.js layout docs |
| MUI RTL: default-export plugin, theme direction, App Router cache options | Step 6 | MUI RTL and Next.js integration docs |
| Portalled UI direction (Radix DirectionProvider, MUI theme) | Step 6 | Radix / MUI docs |
| RTL scroll coordinates (`scrollLeft` 0 to negative) | Gotchas | MDN Element.scrollLeft |
| Flex/Grid mirror automatically; `row-reverse` double-flips | Gotchas, reference | MDN flex-direction, MDN grid logical values |
| Verification: flip the app, canonical mixed test string, portals, screenshot diff | Step 8 | practice |

## Should cover (advanced)
| Item | Covered in | Basis |
|---|---|---|
| Code, pre, kbd, file paths stay LTR | Gotchas | practice; UAX #9 neutrals |
| Tables with numeric/code/date cells | Step 7 | practice |
| Charts/SVG have no logical properties | Step 7 | practice |
| Scrollbar side and `scrollbar-gutter` | Step 7 | web.dev Baseline; Tailwind v4.3 |
| `lang` on embedded opposite-language runs | Step 3 | W3C "Why use the language attribute" |
| Late-arriving logical values (`float`/`clear` inline-*, `resize`, `overflow-inline`) | reference | MDN browser-compat-data |
| Hebrew fonts with a Hebrew subset, incl. monospace | Step 5, reference | Google Fonts css2 API |
| Arrow-key semantics reverse in RTL (tabs, sliders, radio groups) | NOT YET: open lesson | needs a WAI-ARIA APG / Radix passage before encoding |
| Carousel libraries' own RTL flags (Embla, Swiper) | NOT YET: open lesson | not verified against their docs |

## Out of scope (explicit)
Rationale refreshed 2026-09-26.
- Arabic shaping and Arabic typography: different script behaviour; the description routes it away unless shared patterns are asked for.
- Native mobile RTL (React Native I18nManager, SwiftUI, Android): excluded by the description.
- Hebrew punctuation and quotation marks (geresh, gershayim, Hebrew quotes): copy-level concern, not layout.
- Hebrew search normalisation (nikkud stripping, final-letter forms): text processing, belongs to NLP skills.
- i18n routing, locale detection and hreflang: general internationalisation; the skill assumes a locale segment exists.
- Full design-system tokens: `israeli-ui-design-system`; Tailwind presets in depth: `hebrew-tailwind-preset`.

## Authoritative sources
MDN (CSS logical properties, `:dir()`, unicode-bidi, flex-direction, grid logical values, Element.scrollLeft, Intl), MDN browser-compat-data, WHATWG HTML (dom.html directionality, rendering 15.3.5), Unicode UAX #9, CLDR `he.xml`, W3C hlreq and W3C i18n articles, Tailwind CSS docs and GitHub releases, MUI docs, Next.js docs, Google Fonts css2 API, IANA root zone database.
