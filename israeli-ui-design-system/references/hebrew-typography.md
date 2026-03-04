# Hebrew Typography Reference

## Font Pairing Recommendations

### Modern Business (SaaS, Dashboards)
- **Hebrew:** Heebo (300, 400, 500, 700)
- **Latin:** Inter (300, 400, 500, 700)
- **Monospace:** Fira Code
- **Notes:** Best overall pairing. Heebo's x-height matches Inter well. Both have wide weight ranges.

### Friendly Startup (Consumer Apps)
- **Hebrew:** Rubik (300, 400, 500, 700)
- **Latin:** Source Sans Pro (300, 400, 600, 700)
- **Monospace:** Source Code Pro
- **Notes:** Rubik's rounded corners give a friendly feel. Good for mobile-first designs.

### Government/Institutional
- **Hebrew:** Assistant (200, 300, 400, 600, 700, 800)
- **Latin:** Roboto (300, 400, 500, 700)
- **Monospace:** Roboto Mono
- **Notes:** Clean and professional. Assistant has exceptional weight range for Hebrew.

### Editorial (Blogs, News)
- **Hebrew:** Frank Ruhl Libre (300, 400, 500, 700, 900)
- **Latin:** Merriweather (300, 400, 700, 900)
- **Notes:** Serif pairing for long-form reading. Excellent for content-heavy sites.

### Bold Headlines
- **Hebrew:** Secular One (400)
- **Latin:** Montserrat (400, 700)
- **Notes:** Secular One is display-only (one weight). Pair with Heebo or Assistant for body text.

## Hebrew Font Metrics

| Font | x-height | Weight Range | Google Fonts | Characters |
|------|----------|-------------|--------------|------------|
| Heebo | 0.52 | 100-900 | Yes | Hebrew + Latin |
| Rubik | 0.50 | 300-900 | Yes | Hebrew + Latin |
| Assistant | 0.51 | 200-800 | Yes | Hebrew + Latin |
| Frank Ruhl Libre | 0.45 | 300-900 | Yes | Hebrew + Latin |
| Secular One | 0.53 | 400 | Yes | Hebrew + Latin |
| Noto Sans Hebrew | 0.52 | 100-900 | Yes | Hebrew only |
| David Libre | 0.44 | 400-700 | Yes | Hebrew + Latin |

## Font Loading Strategies

### Critical Hebrew Font Loading
```html
<!-- Preload primary Hebrew font -->
<link rel="preload" href="/fonts/Heebo-Regular.woff2"
      as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/Heebo-Bold.woff2"
      as="font" type="font/woff2" crossorigin>
```

### Font Display Strategy
```css
@font-face {
  font-family: 'Heebo';
  src: url('/fonts/Heebo-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap; /* Show fallback immediately, swap when loaded */
  unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;
}
```

### Subsetting for Performance
Hebrew Unicode ranges for subsetting:
- `U+0590-05FF` -- Hebrew block (main characters)
- `U+FB1D-FB4F` -- Hebrew presentation forms
- `U+200C-200D` -- Zero-width non-joiner/joiner
- `U+20AA` -- New Shekel sign

## Hebrew CSS Properties

### Line Height
Hebrew text requires taller line heights than Latin:
- **Tight:** 1.4 (headings only)
- **Normal:** 1.7 (body text recommended)
- **Relaxed:** 1.9 (dense content, small text)

### Letter Spacing
**Never add letter-spacing to Hebrew text.** Hebrew characters are designed to sit at their natural spacing. Adding letter-spacing breaks the visual flow and reduces readability.

### Word Spacing
Slight word spacing (0.03-0.05em) improves Hebrew readability without affecting Latin text.

### Minimum Font Sizes
- Body text: 16px minimum (Hebrew appears smaller than Latin at same size)
- Secondary text: 14px minimum
- Captions/footnotes: 13px minimum (absolute minimum for readable Hebrew)

## Bilingual Typography

When designing for Hebrew + English content:
1. Hebrew font should be listed first in font-family
2. Hebrew text needs larger line-height than Latin
3. Hebrew headings may need to be 1-2px larger than Latin equivalents
4. Use `lang` attribute to apply language-specific styles
5. Test both scripts at every size in the type scale
