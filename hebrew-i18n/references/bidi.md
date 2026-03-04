# Bidirectional Text Handling for Hebrew

## Unicode Bidi Algorithm Overview

The Unicode Bidirectional Algorithm (UBA) determines the direction of text display. Key concepts:

- **Strong characters:** Hebrew letters (RTL), Latin letters (LTR)
- **Weak characters:** Numbers (LTR), punctuation (context-dependent)
- **Neutral characters:** Spaces, some symbols (take direction from context)

## HTML Direction Attributes

### dir Attribute
```html
<!-- Document-level RTL -->
<html dir="rtl" lang="he">

<!-- Block-level override -->
<div dir="ltr">English content here</div>

<!-- Inline isolation -->
<span dir="ltr">user@example.com</span>
```

### The bdi Element
Use for user-generated content where direction is unknown:
```html
<p>המשתמש <bdi>JohnDoe123</bdi> הגיב</p>
<p>המשתמש <bdi>אברהם</bdi> הגיב</p>
```

### The bdo Element
Force a specific direction (overrides bidi algorithm):
```html
<p>מספר טלפון: <bdo dir="ltr">054-1234567</bdo></p>
```

## CSS Bidi Properties

```css
/* Isolate embedded content */
.ltr-embed {
  unicode-bidi: isolate;
  direction: ltr;
}

/* Override bidi algorithm entirely */
.force-ltr {
  unicode-bidi: bidi-override;
  direction: ltr;
}

/* Plaintext -- useful for pre/code blocks */
.code-block {
  unicode-bidi: plaintext;
}
```

## Common Problem Patterns and Solutions

### Phone Numbers in Hebrew Text
Problem: `054-1234567` may display as `1234567-054`
```html
<!-- Solution -->
<p dir="rtl">טלפון: <span dir="ltr">054-1234567</span></p>
```

### URLs in Hebrew Text
Problem: URL parts may reorder
```html
<!-- Solution -->
<p dir="rtl">בקרו ב-<a href="https://example.com" dir="ltr">example.com</a></p>
```

### Mixed List Items
Problem: Numbered list with Hebrew and English items
```html
<ol dir="rtl">
  <li>פריט ראשון</li>
  <li><span dir="ltr">English item</span></li>
  <li>פריט שלישי</li>
</ol>
```

### Parentheses and Brackets
Problem: `(hello)` in RTL context may display as `)hello(`
Solution: The bidi algorithm handles matched pairs correctly when text direction is properly set. If issues persist, use `unicode-bidi: isolate`.

## Framework-Specific Solutions

### React
```jsx
function BidiText({ children, dir = 'auto' }) {
  return <span dir={dir} style={{ unicodeBidi: 'isolate' }}>{children}</span>;
}

// Usage
<p dir="rtl">
  הזמנה מספר <BidiText dir="ltr">ORD-12345</BidiText> אושרה
</p>
```

### Vue
```vue
<template>
  <p dir="rtl">
    {{ hebrewText }}
    <span dir="ltr" style="unicode-bidi: isolate">{{ ltrContent }}</span>
  </p>
</template>
```

## Testing Bidirectional Text

Test strings that expose common bidi bugs:
- `"הזמנה 12345 אושרה"` -- number in Hebrew sentence
- `"טלפון: 054-1234567"` -- phone with punctuation
- `"שלום user@email.com בוקר טוב"` -- email in Hebrew
- `"גרסה v2.1.3-beta"` -- version string
- `"מחיר: $99.99 (כולל מע"מ)"` -- currency with parentheses
