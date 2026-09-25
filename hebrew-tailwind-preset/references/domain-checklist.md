# Domain Checklist: Tailwind CSS for Hebrew RTL

Anchor for Expert Review. Scope: configuring Tailwind CSS (v4 first, v3.3+ secondary) for Hebrew right-to-left web apps. Each row names where the skill covers it.

## Must cover (core)
| Item | Covered in | Basis |
|---|---|---|
| v4 install via a build plugin (Vite, PostCSS, webpack loader); CSS-first `@theme`; JS config no longer auto-detected | Step 1 | Tailwind upgrade guide; CHANGELOG 4.2.0 (webpack) |
| `dir="rtl"` + `lang="he"` on `<html>` | Step 3 | Tailwind RTL docs |
| `rtl:`/`ltr:` selector semantics: `ltr:` applies with no `dir`; nested `dir="auto"` islands match both | Step 3 | Tailwind variant reference; browser test |
| Logical utilities: `ms/me/ps/pe`, `border-s/e`, `rounded-s/e`, `text-start/end`, `scroll-m*/p*` | Step 2, reference | Tailwind docs; local compile |
| `inset-s-*`/`inset-e-*` (v4.2 rename of `start-*`/`end-*`), block-axis and logical sizing (v4.2) | Step 2, reference | CHANGELOG 4.2.0 |
| Hebrew font as the default: `--font-sans` feeds Preflight on `html`, form controls inherit | Step 1 | tailwindcss theme.css / preflight.css |
| next/font wiring: variable on `<html>`, `@theme inline`, `globals.css` imported in the root layout | Step 1 | Tailwind theme docs; Next.js CSS docs |
| `font-display: swap` for Hebrew web fonts | Step 1, Gotchas | MDN font-display |
| No double flips: `rtl:flex-row-reverse`, `rtl:space-x-reverse` | Step 3, Gotchas, reference | MDN flex-direction; local compile |
| Physical-only utilities needing `rtl:` overrides (gradients, shadows) | Gotchas | local compile |
| Hebrew line-height tokens that actually generate utilities (`--leading-hebrew*`) | Step 1 | Tailwind theme namespaces |

## Should cover (advanced)
| Item | Covered in | Basis |
|---|---|---|
| Monospace font with Hebrew glyphs, actually loaded | Step 1 | Google Fonts css2 API |
| Dark mode via `@custom-variant` combined with direction | Step 3 | Tailwind dark-mode docs |
| `@source` for external component libraries | Step 2 | Tailwind source-detection docs |
| Bidi isolation of LTR tokens inside Hebrew (codes, phones) | Step 4 | practice |
| v3 fallback path (`tailwind.config.js`, v3.3.0 floor) | Step 1, Troubleshooting | CHANGELOG 3.3.0 |
| `@tailwindcss/typography` prose in RTL | NOT YET: open lesson | not verified |
| `font-features-*` for Hebrew variable fonts | NOT YET: open lesson | not verified |

## Out of scope (explicit)
Rationale refreshed 2026-09-26.
- General CSS RTL patterns outside Tailwind (bidi algorithm, Intl formatting, MUI, portals): `hebrew-rtl-best-practices`.
- Full design-system tokens and brand palettes: `israeli-ui-design-system`.
- Tailwind v3.0-3.2: logical utilities do not exist and the dir variants were experimental; the skill recommends upgrading.

## Authoritative sources
Tailwind CSS docs (theme, upgrade guide, hover-focus-and-other-states, detecting classes), Tailwind CHANGELOG and GitHub releases, tailwindcss package theme.css and preflight.css, MDN (font-display, flex-direction), Next.js CSS docs, Google Fonts css2 API.
