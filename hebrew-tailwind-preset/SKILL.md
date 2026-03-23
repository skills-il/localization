---
name: hebrew-tailwind-preset
description: Configure Tailwind CSS v4 for Hebrew RTL applications with dir variants, Hebrew font stacks, and logical property utilities. Use when user asks about Tailwind RTL setup, Hebrew Tailwind config, "Tailwind ivrit" (Hebrew Tailwind), RTL utility classes, logical properties in Tailwind, ms-/me- utilities, or Tailwind Hebrew font configuration. Covers Tailwind v4 dir variants, Hebrew font stack presets, logical property utilities (ms-/me-/ps-/pe- instead of ml-/mr-/pl-/pr-), RTL-first component patterns, and Hebrew typography tokens. Do NOT use for general CSS RTL patterns (use hebrew-rtl-best-practices) or full design systems (use israeli-ui-design-system instead).
license: MIT
compatibility: Tailwind CSS v4.0+ recommended. Compatible with v3.1+ for dir variants. Works with React, Vue, Angular, Next.js, Nuxt. No network required.
---

# Hebrew Tailwind Preset

## Instructions

### Step 1: Configure Tailwind v4 for RTL

See `references/rtl-config.md` for complete configuration reference.

**Tailwind v4 (CSS-first configuration):**
```css
/* app.css */
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

  /* Hebrew line heights (taller than Latin defaults) */
  --leading-tight: 1.4;
  --leading-normal: 1.7;
  --leading-relaxed: 1.9;
}
```

**Tailwind v3 (JavaScript configuration):**
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

### Step 2: Use Logical Property Utilities

Always prefer logical utilities over physical directional ones:

| Physical (avoid) | Logical (use) | RTL Behavior |
|-------------------|--------------|--------------|
| `ml-4` | `ms-4` | Right margin in RTL |
| `mr-4` | `me-4` | Left margin in RTL |
| `pl-4` | `ps-4` | Right padding in RTL |
| `pr-4` | `pe-4` | Left padding in RTL |
| `left-0` | `start-0` | Right: 0 in RTL |
| `right-0` | `end-0` | Left: 0 in RTL |
| `border-l` | `border-s` | Right border in RTL |
| `border-r` | `border-e` | Left border in RTL |
| `rounded-l-lg` | `rounded-s-lg` | Right rounded in RTL |
| `rounded-r-lg` | `rounded-e-lg` | Left rounded in RTL |
| `text-left` | `text-start` | Right-aligned in RTL |
| `text-right` | `text-end` | Left-aligned in RTL |
| `scroll-ml-4` | `scroll-ms-4` | Right scroll margin in RTL |

### Step 3: Use Dir Variants for RTL-Specific Styles

When you need direction-specific overrides:

```html
<!-- Root setup -->
<html lang="he" dir="rtl">

<!-- Dir variant usage -->
<div class="flex rtl:flex-row-reverse">
  <span class="rtl:rotate-180">&#8594;</span>
  <span>הבא</span>
</div>

<!-- Icon mirroring for directional icons -->
<button class="flex items-center gap-2">
  <svg class="rtl:scale-x-[-1]"><!-- arrow icon --></svg>
  <span>חזרה</span>
</button>

<!-- Conditional spacing that differs by direction -->
<div class="ltr:ml-auto rtl:mr-auto">
  <!-- Push to end in both directions -->
</div>
```

### Step 4: Hebrew Typography Utilities

```html
<!-- Hebrew body text with proper settings -->
<body dir="rtl" class="font-hebrew text-base leading-hebrew
                        tracking-normal">

  <!-- Hebrew heading -->
  <h1 class="text-3xl font-bold leading-hebrew-tight">
    כותרת ראשית
  </h1>

  <!-- Hebrew paragraph -->
  <p class="text-base leading-hebrew [word-spacing:0.05em]">
    טקסט גוף עם ריווח מותאם לקריאות עברית.
  </p>

  <!-- Mixed Hebrew + English content -->
  <p class="text-base leading-hebrew">
    פריט מספר <span dir="ltr" class="font-mono">ORD-12345</span> אושר
  </p>
</body>
```

### Step 5: RTL-First Component Patterns with Tailwind

**RTL-first card:**
```html
<div class="rounded-lg border border-gray-200 p-6">
  <div class="flex items-center justify-between mb-4
              border-b border-gray-100 pb-4">
    <h3 class="text-lg font-bold">כותרת הכרטיס</h3>
    <span class="text-sm text-gray-500">פעיל</span>
  </div>
  <p class="text-base leading-hebrew text-gray-700">
    תוכן הכרטיס עם טקסט בעברית.
  </p>
  <div class="mt-4 flex gap-3">
    <button class="bg-blue-600 text-white px-4 py-2 rounded-md">
      אישור
    </button>
    <button class="border border-gray-300 px-4 py-2 rounded-md">
      ביטול
    </button>
  </div>
</div>
```

**RTL-first navigation:**
```html
<nav dir="rtl" class="flex items-center justify-between
                       px-6 py-4 bg-white border-b">
  <div class="flex items-center gap-3">
    <img src="/logo.svg" alt="לוגו" class="h-8">
    <span class="font-bold text-xl">שם האתר</span>
  </div>
  <ul class="flex gap-6 text-sm font-medium">
    <li><a href="/" class="text-blue-600">ראשי</a></li>
    <li><a href="/about" class="text-gray-600">אודות</a></li>
    <li><a href="/contact" class="text-gray-600">צור קשר</a></li>
  </ul>
</nav>
```

**RTL-first sidebar layout:**
```html
<div class="grid grid-cols-[280px_1fr] min-h-screen">
  <!-- Sidebar: appears on right in RTL automatically -->
  <aside class="border-e border-gray-200 pe-6 p-4">
    <nav class="space-y-2">
      <a href="#" class="block ps-4 py-2 rounded-md
                         bg-blue-50 text-blue-700 border-s-4
                         border-blue-600">לוח בקרה</a>
      <a href="#" class="block ps-4 py-2 rounded-md
                         text-gray-600">הגדרות</a>
    </nav>
  </aside>
  <!-- Main content -->
  <main class="p-6">
    <h1 class="text-2xl font-bold mb-6">לוח בקרה</h1>
  </main>
</div>
```

### Step 6: Form Utilities for Hebrew

```html
<form dir="rtl" class="max-w-lg space-y-6">
  <div>
    <label for="name" class="block text-sm font-medium
                              text-gray-700 mb-2">שם מלא</label>
    <input id="name" type="text"
           class="w-full px-4 py-3 border border-gray-300
                  rounded-md text-base font-hebrew
                  focus:outline-none focus:ring-2
                  focus:ring-blue-500">
  </div>

  <div>
    <label for="phone" class="block text-sm font-medium
                               text-gray-700 mb-2">טלפון</label>
    <input id="phone" type="tel" dir="ltr"
           placeholder="05X-XXXXXXX"
           class="w-full px-4 py-3 border border-gray-300
                  rounded-md text-base
                  focus:outline-none focus:ring-2
                  focus:ring-blue-500">
  </div>

  <div>
    <label for="message" class="block text-sm font-medium
                                 text-gray-700 mb-2">הודעה</label>
    <textarea id="message" rows="4"
              class="w-full px-4 py-3 border border-gray-300
                     rounded-md text-base font-hebrew
                     leading-hebrew
                     focus:outline-none focus:ring-2
                     focus:ring-blue-500"></textarea>
  </div>

  <button type="submit"
          class="w-full bg-blue-600 text-white py-3
                 rounded-md font-medium text-base
                 hover:bg-blue-700 transition-colors">
    שליחה
  </button>
</form>
```

## Examples

### Example 1: Set Up Tailwind for Hebrew Project
User says: "Configure Tailwind for my Hebrew web app"
Result: Add Hebrew font families to Tailwind theme, configure Hebrew-optimized line heights, set up `dir="rtl"` on root HTML element, and demonstrate using logical utilities (ms-/me-/ps-/pe-) instead of physical ones (ml-/mr-/pl-/pr-).

### Example 2: Convert LTR Tailwind Component to RTL
User says: "Make this Tailwind component work in Hebrew RTL"
Result: Replace all physical utility classes with logical equivalents (ml- to ms-, pl- to ps-, text-left to text-start, border-l to border-s, rounded-l to rounded-s), add rtl: variants for directional icons, and set font-hebrew class on text elements.

### Example 3: Build Hebrew Dashboard with Tailwind
User says: "Create a Hebrew admin dashboard layout with Tailwind"
Result: Build grid layout with RTL sidebar (border-e, pe-6), navigation with Hebrew font and RTL flow, card components using logical spacing, and form elements with proper Hebrew typography (font-hebrew, leading-hebrew).

## Bundled Resources

### References
- `references/rtl-config.md` -- Complete Tailwind CSS RTL configuration reference: v4 CSS-first and v3 JavaScript config examples, full physical-to-logical utility mapping table, dir variant usage patterns, Hebrew font stack presets, typography token definitions, and migration guide from physical to logical utilities.

## Gotchas
- Tailwind CSS v3+ supports RTL variants (`rtl:` prefix), but agents often do not use them, instead hardcoding `mr-4` when they should use `ms-4` (margin-start) for RTL compatibility.
- The `space-x-4` utility in Tailwind does not respect RTL direction. Agents must use `gap-4` with flex or grid, or manually add `rtl:space-x-reverse` to flip spacing direction.
- Custom font declarations for Hebrew must include `font-display: swap` to prevent FOIT (Flash of Invisible Text). Agents may omit this, causing Hebrew text to disappear during font loading.
- Tailwind's `text-left` and `text-right` are physical properties. Use `text-start` and `text-end` classes for RTL-aware alignment. Agents default to physical direction classes.

## Troubleshooting

### Error: "Tailwind logical utilities not working"
Cause: Using older Tailwind version without logical property support
Solution: Logical utilities (ms-, me-, ps-, pe-, start-, end-) require Tailwind v3.3+. For v3.0-3.2, use rtl:/ltr: variants instead (e.g., `rtl:mr-4 ltr:ml-4`). Tailwind v4 has full logical property support built in.

### Error: "Font not applying with font-hebrew class"
Cause: Hebrew font family not defined in Tailwind configuration
Solution: Add the Hebrew font stack to your Tailwind theme under fontFamily.hebrew. Ensure the font CSS is imported (Google Fonts link or local @font-face). Verify the class name matches your config key.

### Error: "Sidebar appears on wrong side in RTL"
Cause: Grid or flex layout not respecting dir attribute
Solution: CSS Grid and Flexbox automatically respect `dir="rtl"`. Ensure `dir="rtl"` is set on the `html` element. Use logical properties for borders (border-e instead of border-r) and padding (pe- instead of pr-). Do not use `direction: rtl` in CSS; use the HTML attribute instead.
