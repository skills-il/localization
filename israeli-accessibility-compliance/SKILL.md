---
name: israeli-accessibility-compliance
description: Implement Israeli web accessibility compliance per IS 5568 standard and WCAG 2.1 AA for Hebrew RTL applications. Use when user asks about Israeli accessibility law, "negishot" (accessibility), IS 5568, "teken negishot" (accessibility standard), "nachim" (disabilities), Hebrew screen reader support, RTL ARIA patterns, or accessibility audit for Israeli websites. Covers mandatory legal requirements under the Equal Rights for Persons with Disabilities Act, Hebrew screen reader compatibility (NVDA, JAWS, VoiceOver), RTL-specific ARIA patterns, and penalties for non-compliance. Do NOT use for general WCAG guidance without Israeli context (use standard a11y resources instead).
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*)
compatibility: Works with any web framework. Python 3.9+ for audit script. No network required for core patterns. axe-core for automated testing.
---

# Israeli Accessibility Compliance

## Instructions

### Step 1: Understand the Legal Framework

Israeli web accessibility (negishot) is legally mandatory under the **Equal Rights for Persons with Disabilities Act (Chok Shivyon Zechuyot Le'Anashim Im Mugbaluyot), 1998** and its 2013 accessibility regulations.

| Regulation | Requirement | Deadline | Penalty |
|------------|-------------|----------|---------|
| IS 5568 | Israeli accessibility standard based on WCAG 2.1 AA | Mandatory since 2017 | Up to 50,000 NIS per violation |
| Takanat Negishot 2013 | Public websites must comply | In effect | Lawsuits + fines |
| Amendment 19 (2022) | Mobile apps included | In effect | Same as above |
| Government sites | Must meet IS 5568 Level AA | In effect | Government oversight |

**Who must comply:** All public-facing Israeli websites and mobile applications, including businesses with 25+ employees, government agencies, educational institutions, healthcare providers, and any service provider open to the public.

### Step 2: IS 5568 vs WCAG 2.1 -- Key Differences

IS 5568 is based on WCAG 2.1 AA but adds Israeli-specific requirements:

| Area | WCAG 2.1 AA | IS 5568 Addition |
|------|-------------|------------------|
| Language | Declare lang attribute | Must support `lang="he"` with RTL |
| Text direction | Not specified | Must declare `dir="rtl"` for Hebrew content |
| Contrast | 4.5:1 for text | Same, plus contrast check with Hebrew fonts |
| Form labels | Associated labels | Labels must support RTL alignment |
| Error messages | Descriptive errors | Must be in Hebrew for Hebrew sites |
| Accessibility statement | Recommended | Mandatory (Hatzaharat Negishot) |
| Contact info | Not required | Must provide accessibility contact method |

### Step 3: Set Up Accessible RTL HTML Structure

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>שם האתר - כותרת הדף</title>
</head>
<body>
  <!-- Skip navigation link (required) -->
  <a href="#main-content" class="skip-link">דלג לתוכן הראשי</a>

  <header role="banner">
    <nav role="navigation" aria-label="ניווט ראשי">
      <!-- Navigation items -->
    </nav>
  </header>

  <main id="main-content" role="main">
    <!-- Page content -->
  </main>

  <footer role="contentinfo">
    <a href="/accessibility-statement">הצהרת נגישות</a>
  </footer>
</body>
</html>
```

Key IS 5568 requirements in this structure:
- `lang="he"` and `dir="rtl"` on the `html` element
- Skip navigation link in Hebrew ("דלג לתוכן הראשי")
- ARIA roles for landmarks
- Hebrew ARIA labels for navigation
- Link to accessibility statement (Hatzaharat Negishot) in footer

### Step 4: Hebrew Screen Reader Compatibility

Test with these screen readers commonly used in Israel:

| Screen Reader | Platform | Hebrew Support | Testing Notes |
|--------------|----------|----------------|---------------|
| NVDA | Windows | Excellent with eSpeak-ng Hebrew | Free, most common in Israel |
| JAWS | Windows | Good with Eloquence Hebrew | Commercial, institutional use |
| VoiceOver | macOS/iOS | Good native Hebrew TTS | Built-in, growing adoption |
| TalkBack | Android | Good with Google TTS Hebrew | Built-in on Android devices |

**Hebrew-specific screen reader patterns:**

```html
<!-- Announce content direction changes -->
<p dir="rtl" lang="he">
  טקסט בעברית עם <span dir="ltr" lang="en">English text</span> משולב
</p>

<!-- Hebrew ARIA labels -->
<button aria-label="סגור חלון">X</button>
<input type="search" aria-label="חיפוש באתר" placeholder="חפש...">

<!-- Hebrew live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true" dir="rtl">
  הטופס נשלח בהצלחה
</div>
```

### Step 5: RTL-Specific ARIA Patterns

```html
<!-- RTL form with accessible error messages -->
<form dir="rtl" novalidate>
  <div role="group" aria-labelledby="personal-info">
    <h2 id="personal-info">פרטים אישיים</h2>

    <label for="full-name">שם מלא</label>
    <input id="full-name" type="text" required
           aria-required="true"
           aria-describedby="name-error"
           aria-invalid="false">
    <span id="name-error" role="alert" class="error" hidden>
      נא למלא שם מלא
    </span>

    <label for="teudat-zehut">תעודת זהות</label>
    <input id="teudat-zehut" type="text" pattern="[0-9]{9}"
           inputmode="numeric" dir="ltr"
           aria-required="true"
           aria-describedby="tz-help tz-error">
    <span id="tz-help" class="hint">9 ספרות</span>
    <span id="tz-error" role="alert" class="error" hidden>
      מספר תעודת זהות לא תקין
    </span>
  </div>
</form>

<!-- RTL data table -->
<table dir="rtl">
  <caption>סיכום הזמנות</caption>
  <thead>
    <tr>
      <th scope="col">מספר הזמנה</th>
      <th scope="col">תאריך</th>
      <th scope="col">סכום</th>
      <th scope="col">סטטוס</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td dir="ltr">ORD-12345</td>
      <td>04/03/2026</td>
      <td dir="ltr">1,234.50 &#8362;</td>
      <td>הושלם</td>
    </tr>
  </tbody>
</table>
```

### Step 6: Accessibility Statement (Hatzaharat Negishot)

IS 5568 requires a published accessibility statement. Required content:

```html
<article dir="rtl" lang="he">
  <h1>הצהרת נגישות</h1>

  <p>אנו ב-[שם החברה] מחויבים להנגשת האתר לאנשים עם מוגבלויות
     בהתאם לתקן הישראלי IS 5568 ולהנחיות WCAG 2.1 ברמה AA.</p>

  <h2>אמצעי נגישות באתר</h2>
  <ul>
    <li>האתר תומך בניווט מלא באמצעות מקלדת</li>
    <li>האתר תומך בקוראי מסך (NVDA, JAWS, VoiceOver)</li>
    <li>תמונות מלוות בטקסט חלופי</li>
    <li>ניגודיות צבעים עומדת ביחס 4.5:1 לפחות</li>
  </ul>

  <h2>פנייה בנושא נגישות</h2>
  <p>רכז/ת נגישות: [שם]</p>
  <p>טלפון: <a href="tel:+97212345678" dir="ltr">+972-1-234-5678</a></p>
  <p>דוא"ל: <a href="mailto:negishot@example.co.il">negishot@example.co.il</a></p>

  <p>תאריך עדכון אחרון: [תאריך]</p>
</article>
```

### Step 7: Automated Accessibility Testing

See `scripts/audit_a11y.py` for the full audit pipeline.

```python
# Quick accessibility check with axe-core via selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_accessibility_audit(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Inject axe-core
    axe_script = open('axe.min.js').read()
    driver.execute_script(axe_script)

    # Run audit with Hebrew locale rules
    results = driver.execute_script("""
        return axe.run({
            rules: {
                'html-has-lang': { enabled: true },
                'valid-lang': { enabled: true },
                'document-title': { enabled: true },
                'bypass': { enabled: true },
                'color-contrast': { enabled: true },
                'label': { enabled: true },
                'image-alt': { enabled: true }
            }
        });
    """)

    driver.quit()
    return results
```

**IS 5568 compliance checklist (automated + manual):**

| Check | Automated | Tool |
|-------|-----------|------|
| `lang="he"` present | Yes | axe-core |
| `dir="rtl"` present | Yes | Custom rule |
| Color contrast 4.5:1 | Yes | axe-core |
| All images have alt text | Yes | axe-core |
| Form inputs have labels | Yes | axe-core |
| Skip navigation link | Yes | axe-core |
| Keyboard navigation | Manual | Tab-through test |
| Screen reader compatibility | Manual | NVDA/VoiceOver test |
| Hebrew error messages | Manual | Visual inspection |
| Accessibility statement | Manual | Page existence check |

See `references/is-5568.md` for the complete checklist mapped to IS 5568 clauses.

## Examples

### Example 1: Audit Existing Israeli Website
User says: "Check if my website meets Israeli accessibility standards"
Result: Run `scripts/audit_a11y.py` against the URL, check for IS 5568 requirements including Hebrew lang attribute, RTL direction, contrast ratios, ARIA labels in Hebrew, skip navigation, and accessibility statement page. Generate a compliance report with pass/fail per criterion.

### Example 2: Add Accessibility Statement Page
User says: "I need to add an accessibility page to comply with Israeli law"
Result: Create a Hebrew accessibility statement (Hatzaharat Negishot) page with all legally required sections: compliance level, accessibility features, known limitations, contact information for the accessibility coordinator (rakaz negishot), and last update date.

### Example 3: Fix RTL Form Accessibility
User says: "Screen readers are not reading my Hebrew form correctly"
Result: Add `dir="rtl"` to the form element, ensure all labels are associated with inputs and use Hebrew text, add `aria-required="true"` for mandatory fields, provide Hebrew error messages with `role="alert"`, and set `dir="ltr"` on numeric inputs like phone and ID number fields.

### Example 4: Make Hebrew Data Table Accessible
User says: "My Hebrew table is not accessible to screen readers"
Result: Add `dir="rtl"` to the table element, include a Hebrew `caption`, use `scope="col"` and `scope="row"` on header cells, mark LTR content like order numbers with `dir="ltr"`, and ensure logical reading order matches visual RTL order.

## Bundled Resources

### Scripts
- `scripts/audit_a11y.py` -- Run IS 5568 accessibility audit: automated checks for Hebrew lang attribute, RTL direction, ARIA labels, contrast ratios, and skip navigation using axe-core and selenium. Generates compliance report with pass/fail per IS 5568 clause. Run: `python scripts/audit_a11y.py --help`

### References
- `references/is-5568.md` -- Complete IS 5568 standard reference: clause-by-clause requirements mapped to WCAG 2.1 AA, Israeli-specific additions, legal penalty schedule under the Equal Rights for Persons with Disabilities Act, mandatory accessibility statement template, and checklist for compliance audits.
- `references/widget-implementation.md` -- Copy-pasteable TypeScript/React code for a Regulation 35 accessibility preferences widget: pub-sub prefs store with `useSyncExternalStore`, class-based CSS toggles, FOUC bootstrap script, `Alt+A` keyboard shortcut (layout-independent via `e.code`), framer-motion `MotionConfig` wiring, and counter-invert rules. Consult when the user wants to ship the widget surface itself, not just audit compliance.

## Building a Compliant Accessibility Preferences Widget

Regulation 35 and IS 5568 require Israeli consumer-facing sites to expose an accessibility control surface that users can operate with the keyboard, typically a floating widget with toggles for contrast, text size, line spacing, cursor, and motion. This widget is a **user-preference comfort tool**, not an automation overlay. The difference is legally and financially significant: the FTC fined accessiBe $1M in April 2025 for misleading claims that its overlay auto-remediated sites (it didn't). The widget you ship must do only what the user asks it to do.

### Feature Set

A minimum-viable Regulation 35 widget exposes these toggles:

| Toggle | Type | Values |
|--------|------|--------|
| Highlight links | Binary | on / off |
| Contrast mode | Cycle | off / high / invert / monochrome |
| Text size | Cycle | 100% / 115% / 130% / 150% |
| Line spacing | Cycle | normal / 1.6 / 2.0 |
| Readable font | Binary | on / off (OS stack only, no webfont) |
| Highlight headings | Binary | on / off |
| Black cursor | Binary | on / off |
| Large cursor | Binary | on / off |
| Stop animations | Binary | on / off |
| Reset | Action | clears all preferences |

### Architecture

Three parts: a preferences store, a UI panel, and a CSS layer.

1. **Preferences store.** A pub-sub store (`subscribe` / `getSnapshot` / `getServerSnapshot` / `set` / `reset`) consumed by React via `useSyncExternalStore`. State is persisted to `localStorage` under a versioned key (e.g., `site_a11y_prefs_v1`). Version mismatches invalidate stored state so schema bumps do not leave stale fields around. Pre-populate the in-memory cache on `notify()` so subscriber fan-out does not trigger redundant `localStorage` reads.

2. **UI panel.** A floating trigger button (`fixed bottom-6 start-6 z-40`, RTL-aware via CSS logical properties) opens a Radix Sheet containing a 3-column grid of toggle cards plus a Reset action. The trigger carries `aria-expanded`, `aria-controls`, and `aria-keyshortcuts="Alt+A"`.

3. **CSS layer.** Every visual change is driven by CSS classes on `<html>` (for example `a11y-contrast-high`, `a11y-text-150`, `a11y-lines-20`, `a11y-reduce-motion`). **The widget never mutates content DOM.** It does not inject `alt` text, reorder nodes, or rewrite ARIA. That is the line that separates a compliant user-preference tool from a banned overlay.

### Single-Source Class Rules

The class list applied at runtime must be identical to the one applied by the FOUC bootstrap script (below), or users see a flash of unstyled preferences on every page load. Define the mapping once and generate both the runtime `applyPrefsToElement()` function and the bootstrap `<script>` body from the same table:

```ts
const CLASS_RULES = [
  ['a11y-links',           (p) => p.links,                 '!!p.links'],
  ['a11y-contrast-high',   (p) => p.contrast === 'high',   "p.contrast==='high'"],
  ['a11y-contrast-invert', (p) => p.contrast === 'invert', "p.contrast==='invert'"],
  ['a11y-contrast-mono',   (p) => p.contrast === 'mono',   "p.contrast==='mono'"],
  ['a11y-text-115',        (p) => p.textSize === 115,      'p.textSize===115'],
  ['a11y-text-130',        (p) => p.textSize === 130,      'p.textSize===130'],
  ['a11y-text-150',        (p) => p.textSize === 150,      'p.textSize===150'],
] as const;
```

### FOUC Prevention

Preferences live in `localStorage`, which means the first paint happens at default styling and only after React hydrates does the widget re-apply the user's settings. That flash is unacceptable for users who rely on high contrast or 150% text. Fix it with an inline `<script>` in `<head>` that runs synchronously before React hydrates:

```ts
// Generated from CLASS_RULES so runtime and bootstrap can't drift
export const A11Y_BOOTSTRAP_SCRIPT =
  `(function(){try{var raw=localStorage.getItem('site_a11y_prefs_v1');` +
  `if(!raw)return;var p=JSON.parse(raw);if(p.version!==1)return;` +
  `var c=document.documentElement.classList;` +
  CLASS_RULES.map(([cls,,js]) => `c.toggle(${JSON.stringify(cls)},${js})`).join(';') +
  `}catch(e){}})()`;
```

In your root layout:

```tsx
<head>
  <script dangerouslySetInnerHTML={{ __html: A11Y_BOOTSTRAP_SCRIPT }} />
</head>
```

Keep a `useEffect` safety net in the widget component that re-applies classes after mount. If `localStorage` is blocked (private browsing, quota exceeded), the bootstrap silently returns and the safety net covers the case.

### Keyboard Shortcut: Use `e.code`, Not `e.key`

Regulation 35 requires the widget to be reachable from any focus context. `Alt+A` is the industry default. Detect it via `e.code`, not `e.key`:

```ts
if (e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey && e.code === 'KeyA') {
  e.preventDefault();
  togglePanel();
}
```

On macOS, `Alt+A` produces the dead-key `å` for `e.key`, which fails the intuitive `e.key === 'a'` check. `e.code` is the physical key position and is layout-independent across macOS, Windows, and Linux.

### ARIA Correctness

- **Binary toggles** (links highlight, readable font, cursor, motion, headings): use `aria-pressed={active}`.
- **Cycling toggles** (contrast, text size, line spacing): **omit `aria-pressed`**. Reading "pressed" aloud is misleading when the control has more than two states. The accessible name itself should carry the current value: `aria-label={`"${label}: ${valueLabel}"`}`.
- **Live region** announcing state changes: use `role="status" aria-live="polite"` and render it **outside** the Sheet portal. Portals unmount when the Sheet closes; a live region inside the portal loses late-arriving announcements.

### framer-motion / Reduced Motion

If the app uses framer-motion, wrap the tree in a `<MotionConfig>` that mirrors the Stop Animations toggle:

```tsx
<MotionConfig reducedMotion={prefs.reduceMotion ? 'always' : 'user'}>
```

`'always'` forces reduced motion when the widget toggle is on. `'user'` falls back to the OS `prefers-reduced-motion` media query when the toggle is off, so system-level requests are still honored.

### Counter-Invert the Widget

If the user enables invert or monochrome contrast, the whole page is filtered. The widget itself must be counter-inverted so the user can still read it to turn the setting off:

```css
html.a11y-contrast-invert #a11y-widget-panel,
html.a11y-contrast-invert #a11y-widget-trigger {
  filter: invert(1) hue-rotate(180deg);
}
```

Forget this and users end up with an unreadable widget they cannot deactivate.

### Print Rule

Reset every `a11y-*` class in print context so high-contrast filters and inverted colors do not follow the user to paper:

```css
@media print {
  html[class*="a11y-"] { filter: none !important; }
  html[class*="a11y-text-"] { font-size: 100% !important; }
  html[class*="a11y-lines-"] { line-height: normal !important; }
}
```

See `references/widget-implementation.md` for complete copy-pasteable code covering the pub-sub store, the FOUC bootstrap, the React component with the ToggleCard grid, the `MotionA11yProvider`, and the CSS class reference table.

## Avoiding Overlay Anti-Patterns

Accessibility overlay products (accessiBe, UserWay, AudioEye) claim to make sites compliant by injecting JavaScript that auto-generates alt text, rewrites ARIA, and fixes inaccessible markup at runtime. Disability advocates and US regulators have documented that overlay-protected sites still fail screen-reader testing. **In April 2025 the FTC fined accessiBe $1M** and ordered ongoing compliance monitoring for misleading advertising about its overlay's capabilities.

The Israeli Commission for Equal Rights of Persons with Disabilities has not endorsed any overlay product. IS 5568 compliance is evaluated against the site's actual rendered HTML, not against claims made by a plug-in.

When building the widget above, enforce these scope fences:

| Do | Do NOT |
|----|--------|
| Toggle CSS classes on `<html>` | Mutate content DOM, rewrite `alt` attributes, or inject ARIA |
| Provide user-controlled preferences (contrast, text size, motion) | Claim the widget alone makes the site "IS 5568 compliant" or "WCAG compliant" |
| Document scope as a comfort tool in the accessibility statement | Display a certification badge or "audited by" claim sourced from a vendor plug-in |
| Use OS font stacks for the readable-font toggle | Inject a webfont that changes rendered text width and re-flows past critical content |
| Persist preferences to `localStorage` and a cookie you control | Use third-party overlay SDKs that fingerprint users or apply tracking cookies as a side effect |

The widget is one layer of compliance. The other layers, semantic HTML, correct `dir` and `lang`, keyboard operability, real screen-reader testing, proper form labels, working focus management, the accessibility statement page (Hatzaharat Negishot), and a named accessibility coordinator, all have to be built into the site itself. No widget substitutes for that work.

## Gotchas
- Israeli accessibility law (IS 5568) is based on WCAG 2.1 AA, but has additional Israeli-specific requirements for bilingual (Hebrew + Arabic) government sites. Agents may apply only WCAG without the Israeli additions.
- Screen readers for Hebrew (NVDA, JAWS) read RTL text differently than LTR. Agents may generate ARIA labels assuming LTR reading order, which confuses Hebrew screen reader users.
- Israeli law requires accessibility statements (hatzaharat negishut) to be published on every website. Agents may generate WCAG-compliant sites without this mandatory statement page.
- Color contrast requirements in IS 5568 match WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text), but agents may not account for Hebrew font rendering, which can appear thinner than Latin fonts at the same size, requiring slightly higher contrast.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Commission for Equal Rights of Persons with Disabilities | https://www.gov.il/he/departments/mugbaluyot | Israeli accessibility law, enforcement, complaints |
| IS 5568 / Tav Negishut | https://www.sii.org.il/en/ | Israeli Standards Institute source for the IS 5568 standard |
| Equal Rights Act (Nevo) | https://www.nevo.co.il/law_html/law01/p214m2_001.htm | Legal text of the Equal Rights for Persons with Disabilities Act |
| WCAG 2.1 quick reference | https://www.w3.org/WAI/WCAG21/quickref/ | Success criteria and techniques for AA compliance |
| NVDA Hebrew support | https://www.nvaccess.org/ | Free screen reader widely used for Hebrew a11y testing |

## Troubleshooting

### Error: "Screen reader announces content in wrong order"
Cause: Visual RTL order does not match DOM order, or missing dir attribute
Solution: Ensure the DOM source order matches the intended reading order for RTL. Add `dir="rtl"` to container elements. Use CSS logical properties for layout instead of physical positioning that may conflict with reading order.

### Error: "Hebrew form validation messages not announced"
Cause: Error messages not using ARIA live regions or alert role
Solution: Add `role="alert"` to error message containers and ensure they are populated dynamically after validation. Use `aria-describedby` to link error messages to their input fields. Error text must be in Hebrew for Hebrew forms.

### Error: "Skip navigation link not working in RTL layout"
Cause: Skip link positioned off-screen using physical CSS (left: -9999px)
Solution: Use `inset-inline-start: -9999px` instead of `left: -9999px` for the skip link. Ensure the target element has `id` and `tabindex="-1"` for focus management. Test that the skip link is the first focusable element in tab order.