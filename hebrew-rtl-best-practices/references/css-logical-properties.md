# CSS Logical Properties Quick Reference for Hebrew RTL

## Property Mapping Table

### Margin
| Physical | Logical | Notes |
|----------|---------|-------|
| `margin-left` | `margin-inline-start` | Start of reading direction |
| `margin-right` | `margin-inline-end` | End of reading direction |
| `margin-top` | `margin-block-start` | Top in both LTR and RTL |
| `margin-bottom` | `margin-block-end` | Bottom in both LTR and RTL |

### Padding
| Physical | Logical |
|----------|---------|
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `padding-top` | `padding-block-start` |
| `padding-bottom` | `padding-block-end` |

### Border
| Physical | Logical |
|----------|---------|
| `border-left` | `border-inline-start` |
| `border-right` | `border-inline-end` |
| `border-top` | `border-block-start` |
| `border-bottom` | `border-block-end` |

### Positioning
| Physical | Logical |
|----------|---------|
| `left` | `inset-inline-start` |
| `right` | `inset-inline-end` |
| `top` | `inset-block-start` |
| `bottom` | `inset-block-end` |

### Text and Alignment
| Physical | Logical |
|----------|---------|
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `float: left` | `float: inline-start` |
| `float: right` | `float: inline-end` |

### Sizing
| Physical | Logical |
|----------|---------|
| `width` | `inline-size` |
| `height` | `block-size` |
| `min-width` | `min-inline-size` |
| `max-width` | `max-inline-size` |

## Hebrew Font Stack Recommendations

### Sans-Serif (recommended for web)
```css
font-family: 'Heebo', 'Assistant', 'Rubik', 'Noto Sans Hebrew', 'Arial Hebrew', sans-serif;
```

### Serif (for formal/print-style content)
```css
font-family: 'Frank Ruhl Libre', 'David Libre', 'Noto Serif Hebrew', serif;
```

### Monospace (for code with Hebrew comments)
```css
font-family: 'Cousine', 'Noto Sans Mono', monospace;
```

## Browser Support Notes
- CSS Logical Properties are supported in all modern browsers (Chrome 89+, Firefox 66+, Safari 15+, Edge 89+)
- For older browser support, use PostCSS plugin `postcss-logical` as a fallback
- Flexbox and Grid automatically respect `dir="rtl"` -- no additional CSS needed for basic layout reversal
