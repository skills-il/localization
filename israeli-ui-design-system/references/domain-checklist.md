# Domain Checklist: Israeli RTL-First Design Systems

Anchor for expert review. This checklist was bootstrapped by the 2026-09-26 panel expert, then reviewed and sourced. The Where column points to the skill.

## Must cover (core)

| Item | Source | Where |
|------|--------|-------|
| `dir` and `lang` on `<html>`, with every rule keyed to it (logical properties, selectors that match `html[dir]`) | MDN logical properties | Steps 2-3 |
| Font stack order for a Hebrew and Latin pairing, the Hebrew subset, and a system fallback with Hebrew glyphs | Google Fonts metadata; Next.js font API | Step 1 |
| Hebrew type scale and line height, applied under RTL | Measured font metrics (`hebrew-typography.md`) | Step 2 |
| Icon and glyph mirroring, including bidi-mirrored characters that must NOT be flipped again | Material bidirectionality; Unicode BidiMirroring.txt (`>` and `›` are mirrored) | Step 3 |
| Israeli formatting: ILS, day-first dot dates, 24-hour time, separators, bidi isolation | CLDR he.xml; MDN Intl | Step 7 |
| Calendars: week starts Sunday, weekend is Friday and Saturday | `Intl.Locale('he-IL').getWeekInfo()` (MDN) | Step 7 |
| Israeli form fields: teudat zehut (9 digits, check digit, left zero-padding), mobile phone, 7-digit postal code | he.wikipedia "מספר זהות (ישראל)" and "ספרת ביקורת" | Step 6 |
| Token contrast for text against surface (4.5:1) and UI (3:1) | WCAG 2.x 1.4.3 / 1.4.11 | Step 4 |
| Token tiers and DTCG authoring | DTCG Format 2025.10; Style Dictionary docs | Step 4 |

## Should cover (advanced)

| Item | Source | Status |
|------|--------|--------|
| Gender-inclusive Hebrew microcopy | House-style practice, no statute | Covered, Step 6 (labelled practice) |
| Native `<input type="date">` display versus Intl output | Browser behaviour | Covered, Step 7 |
| Dialog action order in RTL | House convention | Covered, Step 3 (labelled as a choice) |
| Hebrew calendar dates (`-u-ca-hebrew`) for holiday and government contexts | ECMA-402 calendars | Not covered; next cycle |
| `color-scheme`, fluid type, directional motion and reduced motion, `tabular-nums` | CSS specs | Not covered; logged in optimization-log |

## Out of scope (explicit)

| Item | Rationale (2026-09-26) |
|------|------------------------|
| Accessibility audits and IS 5568 legal compliance | Sibling skill `israeli-accessibility-compliance` |
| General RTL CSS not tied to a design system | Sibling skill `hebrew-rtl-best-practices` |
| Official gov.il visual identity | Lives in the IGDS Figma files; this skill's institutional CSS is a generic scaffold only |

## Authoritative sources

- https://fonts.google.com/metadata/fonts
- https://nextjs.org/docs/app/api-reference/components/font
- https://tailwindcss.com/docs/theme; https://raw.githubusercontent.com/tailwindlabs/tailwindcss/main/CHANGELOG.md
- https://ui.shadcn.com/docs/rtl
- https://m2.material.io/design/usability/bidirectionality.html
- https://www.designtokens.org/TR/2025.10/format/
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/getWeekInfo
