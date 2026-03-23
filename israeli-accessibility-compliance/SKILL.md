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

## Gotchas
- Israeli accessibility law (IS 5568) is based on WCAG 2.0 AA, but has additional Israeli-specific requirements for bilingual (Hebrew + Arabic) government sites. Agents may apply only WCAG without the Israeli additions.
- Screen readers for Hebrew (NVDA, JAWS) read RTL text differently than LTR. Agents may generate ARIA labels assuming LTR reading order, which confuses Hebrew screen reader users.
- Israeli law requires accessibility statements (hatzaharat negishut) to be published on every website. Agents may generate WCAG-compliant sites without this mandatory statement page.
- Color contrast requirements in IS 5568 match WCAG 2.0 AA (4.5:1 for text), but agents may not account for Hebrew font rendering, which can appear thinner than Latin fonts at the same size, requiring slightly higher contrast.

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