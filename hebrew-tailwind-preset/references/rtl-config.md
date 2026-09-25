# Tailwind CSS RTL Configuration Reference

## Tailwind v4 Configuration (CSS-first)

```css
@import "tailwindcss";

@theme {
  /* Hebrew font stacks */
  --font-sans: 'Heebo', 'Assistant', 'Noto Sans Hebrew', sans-serif; /* default font for html, body and form controls */
  --font-hebrew: 'Heebo', 'Assistant', 'Noto Sans Hebrew', sans-serif;
  --font-hebrew-serif: 'Frank Ruhl Libre', 'David Libre', serif;
  --font-mono: 'Cousine', 'Fira Code', monospace; /* Cousine carries Hebrew glyphs for code comments; Fira Code does not */

  /* Hebrew-optimized type scale */
  --text-xs: 0.8125rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Hebrew line heights. The --leading-* namespace is what generates
     leading-<name>, so these names create leading-hebrew,
     leading-hebrew-tight and leading-hebrew-relaxed. Using
     --leading-tight / --leading-normal / --leading-relaxed instead only
     overrides the built-in scale and leaves leading-hebrew* undefined. */
  --leading-hebrew: 1.7;
  --leading-hebrew-tight: 1.4;
  --leading-hebrew-relaxed: 1.9;
}
```

## Tailwind v3 Configuration (JavaScript)

```js
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{html,js,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        hebrew: ['Heebo', 'Assistant', 'Noto Sans Hebrew', 'sans-serif'],
        'hebrew-serif': ['Frank Ruhl Libre', 'David Libre', 'serif'],
      },
      lineHeight: {
        'hebrew': '1.7',
        'hebrew-tight': '1.4',
        'hebrew-relaxed': '1.9',
      },
    },
  },
  plugins: [],
};
```

## Complete Logical-to-Physical Utility Mapping

### Margin

| Physical | Logical | Description |
|----------|---------|-------------|
| `ml-*` | `ms-*` | Margin inline start |
| `mr-*` | `me-*` | Margin inline end |
| `ml-auto` | `ms-auto` | Auto margin inline start |
| `mr-auto` | `me-auto` | Auto margin inline end |

### Padding

| Physical | Logical | Description |
|----------|---------|-------------|
| `pl-*` | `ps-*` | Padding inline start |
| `pr-*` | `pe-*` | Padding inline end |

### Positioning

| Physical | Logical | Description |
|----------|---------|-------------|
| `left-*` | `inset-s-*` | Inset inline start (was `start-*`) |
| `right-*` | `inset-e-*` | Inset inline end (was `end-*`) |

As of Tailwind v4.2 (18 February 2026) the inset utilities `start-*`/`end-*` are deprecated in favor of `inset-s-*`/`inset-e-*` so the API lines up with `inset-bs-*`/`inset-be-*`. The old `start-*`/`end-*` names still work. This rename affects only inset/positioning; `ms-*`/`me-*`/`ps-*`/`pe-*`/`border-s`/`border-e` are unchanged.

### Border

| Physical | Logical | Description |
|----------|---------|-------------|
| `border-l` | `border-s` | Border inline start |
| `border-r` | `border-e` | Border inline end |
| `border-l-*` | `border-s-*` | Border width inline start |
| `border-r-*` | `border-e-*` | Border width inline end |

### Border Radius

| Physical | Logical | Description |
|----------|---------|-------------|
| `rounded-l-*` | `rounded-s-*` | Border radius inline start |
| `rounded-r-*` | `rounded-e-*` | Border radius inline end |
| `rounded-tl-*` | `rounded-ss-*` | Border radius start-start |
| `rounded-tr-*` | `rounded-se-*` | Border radius start-end |
| `rounded-bl-*` | `rounded-es-*` | Border radius end-start |
| `rounded-br-*` | `rounded-ee-*` | Border radius end-end |

### Text Alignment

| Physical | Logical | Description |
|----------|---------|-------------|
| `text-left` | `text-start` | Align to start (right in RTL) |
| `text-right` | `text-end` | Align to end (left in RTL) |

### Scroll

| Physical | Logical | Description |
|----------|---------|-------------|
| `scroll-ml-*` | `scroll-ms-*` | Scroll margin inline start |
| `scroll-mr-*` | `scroll-me-*` | Scroll margin inline end |
| `scroll-pl-*` | `scroll-ps-*` | Scroll padding inline start |
| `scroll-pr-*` | `scroll-pe-*` | Scroll padding inline end |

## Dir Variant Patterns

### Icon Mirroring
```html
<!-- Directional icons: mirror in RTL -->
<svg class="rtl:scale-x-[-1]"><!-- arrow, chevron, back --></svg>

<!-- Non-directional icons: do NOT mirror -->
<svg><!-- search, home, settings, close --></svg>
```

### Flex Direction (no variant needed)
```html
<!-- dir="rtl" already runs a flex row right to left -->
<div class="flex">...</div>

<!-- Wrong: rtl:flex-row-reverse double-flips back to LTR visual order -->
<div class="flex rtl:flex-row-reverse">...</div>
```

### Positioning at the End Side
```html
<!-- One logical class instead of a rtl:left-0 ltr:right-0 pair -->
<span class="absolute top-0 inset-e-0">...</span>
```

## Migration Guide: Physical to Logical

Search and replace in your templates:

1. `ml-` -> `ms-` (except `ml-auto` -> `ms-auto`)
2. `mr-` -> `me-` (except `mr-auto` -> `me-auto`)
3. `pl-` -> `ps-`
4. `pr-` -> `pe-`
5. `text-left` -> `text-start`
6. `text-right` -> `text-end`
7. `left-` -> `inset-s-` (v4.2+; `start-` still works but is deprecated)
8. `right-` -> `inset-e-` (v4.2+; `end-` still works but is deprecated)
9. `border-l` -> `border-s`
10. `border-r` -> `border-e`
11. `rounded-l-` -> `rounded-s-`
12. `rounded-r-` -> `rounded-e-`

Note: `float-left` -> `float-start` and `float-right` -> `float-end` require Tailwind v3.4+ or v4, and the underlying `float: inline-start` / `inline-end` needs Chrome/Edge 118+ (Firefox 55, Safari 15).
