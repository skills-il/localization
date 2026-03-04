# Tailwind CSS RTL Configuration Reference

## Tailwind v4 Configuration (CSS-first)

```css
@import "tailwindcss";

@theme {
  /* Hebrew font stacks */
  --font-hebrew: 'Heebo', 'Assistant', 'Noto Sans Hebrew', sans-serif;
  --font-hebrew-serif: 'Frank Ruhl Libre', 'David Libre', serif;
  --font-mono: 'Fira Code', 'Source Code Pro', monospace;

  /* Hebrew-optimized type scale */
  --text-xs: 0.8125rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Hebrew line heights */
  --leading-tight: 1.4;
  --leading-normal: 1.7;
  --leading-relaxed: 1.9;
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
| `left-*` | `start-*` | Inset inline start |
| `right-*` | `end-*` | Inset inline end |

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

### Conditional Flex Direction
```html
<!-- Reverse flex in RTL when needed -->
<div class="flex rtl:flex-row-reverse">...</div>
```

### Conditional Positioning
```html
<!-- Position at the "end" side -->
<span class="absolute top-0 rtl:left-0 ltr:right-0">...</span>
```

## Migration Guide: Physical to Logical

Search and replace in your templates:

1. `ml-` -> `ms-` (except `ml-auto` -> `ms-auto`)
2. `mr-` -> `me-` (except `mr-auto` -> `me-auto`)
3. `pl-` -> `ps-`
4. `pr-` -> `pe-`
5. `text-left` -> `text-start`
6. `text-right` -> `text-end`
7. `left-` -> `start-`
8. `right-` -> `end-`
9. `border-l` -> `border-s`
10. `border-r` -> `border-e`
11. `rounded-l-` -> `rounded-s-`
12. `rounded-r-` -> `rounded-e-`

Note: `float-left` -> `float-start` and `float-right` -> `float-end` require Tailwind v3.3+ or v4.
