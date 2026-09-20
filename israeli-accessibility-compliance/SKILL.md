---
name: israeli-accessibility-compliance
description: Not an accessibility surveyor's opinion and not legal advice. Implement Israeli web accessibility compliance per IS 5568 standard, anchored to WCAG 2.0 AA (IS 5568 adds some 2.1-aligned criteria; sources differ), for Hebrew RTL applications. Use when user asks about Israeli accessibility law, "negishot" (accessibility), IS 5568, "teken negishot" (accessibility standard), "nachim" (disabilities), Hebrew screen reader support, RTL ARIA patterns, or accessibility audit for Israeli websites. Covers mandatory legal requirements under the Equal Rights for Persons with Disabilities Act, who is exempt, enforcement and penalties, the accessibility coordinator role, Hebrew screen reader compatibility (NVDA, JAWS, VoiceOver), and RTL-specific ARIA patterns. Do NOT use for general WCAG guidance without Israeli context (use standard a11y resources instead).
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*)
compatibility: Works with any web framework. Python 3.9+ for audit script. No network required for core patterns. axe-core for automated testing.
---

# Israeli Accessibility Compliance

## Legal notice

This is a free information tool operated by an AI model. It explains Israeli accessibility law, maps the IS 5568 requirements, runs static HTML checks and drafts an accessibility statement, and all of its output is produced automatically, without the involvement, review or approval of a certified accessibility expert (morshe negishut). The output is not a certified accessibility expert's opinion, not an accredited accessibility audit and not legal advice: it is raw technical and explanatory material only. It does not include manual testing with assistive technology, does not review documents under IS 5568 Part 2, does not produce the technological-difficulty opinion required by Regulation 35, and does not verify the current index-linked statutory damages figure. An AI model may err, omit data or present a wrong conclusion.

The accessibility statement block in Step 9 and the output of audit_a11y.py are a working draft for internal organisational use, to be reviewed by a certified accessibility expert (morshe negishut) before publication and before being relied on against an enforcement action or a civil claim. This tool is not a substitute for advice that takes into account the particular circumstances and needs of each person, and before publishing an accessibility statement, claiming an exemption or answering a complaint you should turn to a certified accessibility expert or to a lawyer.

## Instructions

### Step 1: Understand the Legal Framework

Israeli web accessibility (negishot) is legally mandatory under the **Equal Rights for Persons with Disabilities Act (Chok Shivyon Zechuyot Le'Anashim Im Mugbaluyot), 1998** and the **Equal Rights for Persons with Disabilities (Service Accessibility Accommodations) Regulations, 2013** (Takanot Negishut LeSherut).

| Regulation | Requirement | Status | Penalty |
|------------|-------------|--------|---------|
| IS 5568 (2017, updated 2020 and 2023) | Israeli accessibility standard, anchored to WCAG 2.0 AA | New websites accessible from 25 October 2015; existing websites by 26 October 2017; the October 2020 date extended the lower-revenue exemption tiers, not the universal deadline | Statutory civil damages without proof of harm, base 50,000 NIS under s.19נא(ב), CPI-index-linked (see Step 3) |
| Takanat Negishut LeSherut (2013) | Public websites and apps must comply | In effect; covers services provided to the public | Lawsuits + statutory damages |
| Mobile applications | Included in scope per the 2013 regulations; explicitly reaffirmed in later updates | In effect | Same statutory damages |
| Government sites | Must meet IS 5568 Level AA | In effect | Commission oversight + administrative penalty |

**Note on WCAG version.** IS 5568, including the September 2023 Part 1 edition, stays legally anchored to **WCAG 2.0 AA**; WCAG 2.1 alignment is partial or vendor-claimed, and some sources do describe IS 5568:2020 as 2.1 AA, so sources differ. Target WCAG 2.0 AA plus the Israeli additions below. Meeting 2.1 and 2.2 on top is useful future-proofing, not the legal floor.

**Who must comply:** All public-facing Israeli websites and mobile applications of service providers open to the public, including government agencies, educational institutions, healthcare providers, businesses, and non-profits.

**Standard conformance is necessary but not sufficient.** The legal duty is the *regulation* (Service Accessibility Regulations 2013), which *incorporates IS 5568 Part 1 by reference at level AA*. You can pass an automated WCAG / IS 5568 audit and still be non-compliant if you lack the accessibility statement, the coordinator (where required), a feedback channel, or the certified-expert opinion described below, and vice versa. Treat "meets IS 5568" and "legally compliant" as two separate checklists.

**Certified accessibility expert (Morshe Negishut Hasherut).** Where an operator claims an exemption for "technological difficulty" under Regulation 35, the regulation requires a **written opinion from a certified service-accessibility expert (morshe negishut hasherut)** prepared in consultation with an internet-accessibility professional. In practice the accessibility statement and the audit behind it are also expected to be backed by a morshe negishut; compliance is not a pure developer/automated-audit exercise.

**Digital documents (IS 5568 Part 2).** IS 5568 is split into Part 1 (web content) and **Part 2 (accessibility of digital documents, e.g. PDFs and Office files), published 2020**. PDFs and downloadable documents on a public-facing Israeli site fall under the accessibility duty and are one of the most common real-world audit failures, so do not stop at the HTML.

### Step 2: Who Is Exempt

The Service Accessibility Regulations base website-accessibility exemptions on **revenue**, not on employee count. There is no "25 employees" or "300,000 NIS" trigger in the regulations. The exemption tiers are:

| Operator | Exemption |
|----------|-----------|
| Osek patur (VAT-exempt dealer) | Full exemption from website accessibility |
| Average annual revenue under 120,000 NIS | Temporary 3-year exemption, renewable every 3 years while average revenue stays at or below 120,000 NIS |
| Average annual revenue from 120,000 NIS up to 1,000,000 NIS | 3-year exemption for an existing site whose operation began before 26 October 2017; a new site built after that date must be accessible |
| Average annual revenue above 1,000,000 NIS | No automatic exemption. The operator must apply to the Commission for Equal Rights of Persons with Disabilities to claim a heavy-burden exemption |

These exemptions (except the heavy-burden application) are automatic and need no approval, but the operator must re-check their revenue every 3 years. Exemption from website accessibility does not exempt the operator from other service-accessibility duties, nor from the separate **physical-premises accessibility** duty (negishut hamivne), which is governed by its own regulations.

### Step 3: Enforcement and Penalties

Two enforcement tracks run in parallel:

- **Civil lawsuit.** A claimant can sue for **statutory damages without proof of harm**, only needing to show the site is non-compliant. Section 19נא(ב) sets the ceiling at **50,000 NIS**, but 19נא(ו)(1) index-links that sum: it is updated once a year against the Consumer Price Index, with a base index of February 2005. So 50,000 NIS is the statutory base, not today's number, and the practical current ceiling is higher. Do not quote an updated figure you have not read from the Commission's published sum.
- **Administrative enforcement by the Commission.** Chapter ט' of the Equal Rights Act, added by **Amendment 23 (2022) and in force from 10 August 2023** (conditioned on publication of the regulations under s.26יב(ב)), gave the Commission an administrative track: warnings, written undertakings, accessibility orders, and an **administrative monetary penalty** (izum kaspi). Section 26ז was later amended by Amendment 25 (2024) and its sums re-indexed by הודעה תשפ"ה-2025 and הודעה תשפ"ו-2026. The 10.8.2023 date matters because it bounds which conduct is exposed to the administrative track at all.

**Debtor size bands (s.26ז(א)),** measured by turnover (מחזור עסקאות) in the year preceding the breach:

| Term | Definition |
|------|------------|
| חייב זעיר | Turnover not exceeding 2,000,000 NIS. Public authorities excluded |
| חייב קטן | Turnover above 2,000,000 NIS and not exceeding 20,000,000 NIS. Public authorities excluded |
| חייב רגיל | Anything that is neither of the above |

**Penalty amounts (s.26ז(ג), as updated by הודעה תשפ"ו-2026),** in NIS, by the part of the Eighth Schedule the breached provision sits in:

| Eighth Schedule part | חייב זעיר | חייב קטן | חייב רגיל |
|---|---|---|---|
| א' | 1,310 | 3,830 | 13,680 |
| ב' | 2,620 | 7,660 | 27,360 |
| ג' | 3,940 | 14,220 | 41,030 |
| ד' | 3,940 | 14,220 | 218,820 |

Section 26ז(ב) separately sets **27,360 NIS** for breaches of the adequate-representation duty. A per-day charge runs while a violation continues, and reductions apply for a clean prior record and for corrective action.

**The two tracks are not purely cumulative.** Amendment 23 added defenses in s.19נא(ג)(1א)-(1ב): a court will **not** award damages without proof of harm where the operator had already filed a **written undertaking (ktav hitchayvut)** under Chapter ט' Sign ג' and is complying with it, or where an administrative penalty or an administrative warning was already imposed on it for the same act or omission, that defense running for the period the Commissioner set for carrying out the accommodations. Section 19נג(ג) likewise bars the Commission from suing over an act it has already penalised administratively. An operator that has taken the administrative route therefore has a real answer to a later civil claim on the same facts.

**60-day cure period.** A deviation is not treated as a violation unless the operator was first sent a notice demanding a fix and failed to fix it within a reasonable time, no later than 60 days from receiving the notice. A class-action request for an inaccessible site has no cause of action if no prior fix notice was sent. This is a real defense for operators.

**Filing a complaint (user side).** A user who hits an inaccessible site sends the operator a fix notice (which starts the 60-day clock); if it is not fixed in time, the user can complain to the Commission for Equal Rights of Persons with Disabilities or sue for the statutory damages. The operator's accessibility coordinator (Step 4) is the first point of contact for such complaints, so an operator should route incoming accessibility complaints through the coordinator and act within the cure window.

### Step 4: The Accessibility Coordinator (Rakaz Negishut)

The coordinator duty sits in the **primary Act, section 19מב** (added by Amendment 2, 2005), **not** in the 2013 Service Accessibility Regulations. There is a **single trigger**: whoever is responsible for supplying a public service as defined in Sign ד' **and employs at least 25 employees** must appoint, from among its own staff, a person as expert in accessibility for people with disabilities as possible, and so far as possible a person with a disability, as the **accessibility coordinator** (rakaz negishut). There is no separate public-body limb in 19מב. Note this 25-employee figure is the trigger for the *coordinator appointment*, not for the website-accessibility duty itself, which is universal subject to the revenue exemptions above. Section 19מב(ב) itself lists exactly two duties:

- Gives the public information about the accessibility of the public service or of the place where it is given.
- Gives **advice and training (ייעוץ והדרכה)** on the public service's own accessibility obligations.

Two further duties are commonly attributed to the coordinator, but they come from the Service Accessibility Regulations rather than from 19מב, so do not cite the Act for them:

- Handles accessibility inquiries and complaints from the public.
- Helps the parties responsible for accessibility carry out and maintain the required accommodations.

The coordinator's name and contact details must appear in the accessibility statement (see Step 9).

### Step 5: IS 5568 vs WCAG -- Key Differences

IS 5568 is anchored to WCAG 2.0 AA (sources differ on whether the current edition reaches 2.1) and adds Israeli-specific requirements:

| Area | WCAG 2.0 AA | IS 5568 Addition |
|------|-------------|------------------|
| Language | Declare lang attribute | Must support `lang="he"` with RTL |
| Text direction | Not specified | Must declare `dir="rtl"` for Hebrew content |
| Contrast | 4.5:1 for text | Same, plus contrast check with Hebrew fonts |
| Form labels | Associated labels | Labels must support RTL alignment |
| Error messages | Descriptive errors | Must be in Hebrew for Hebrew sites |
| Accessibility statement | Recommended | Mandatory (Hatzaharat Negishot) |
| Contact info | Not required | Must provide accessibility contact method |
| Bilingual public bodies | Not specified | A government or public body that serves the public in Hebrew and Arabic should make its content accessible in both languages, not Hebrew only |

### Step 6: Set Up Accessible RTL HTML Structure

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

### Step 7: Hebrew Screen Reader Compatibility

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

### Step 8: RTL-Specific ARIA Patterns

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

### Step 9: Accessibility Statement (Hatzaharat Negishot)

IS 5568 requires a published accessibility statement. Required content:

```html
<article dir="rtl" lang="he">
  <h1>הצהרת נגישות</h1>

  <p>אנו ב-[שם החברה] מחויבים להנגשת האתר לאנשים עם מוגבלויות
     בהתאם לתקן הישראלי IS 5568, המעוגן ב-WCAG 2.0 ברמה AA.</p>

  <h2>אמצעי נגישות באתר</h2>
  <ul>
    <li>האתר תומך בניווט מלא באמצעות מקלדת</li>
    <li>האתר תומך בקוראי מסך (NVDA, JAWS, VoiceOver)</li>
    <li>תמונות מלוות בטקסט חלופי</li>
    <li>ניגודיות צבעים עומדת ביחס 4.5:1 לפחות</li>
  </ul>

  <h2>מגבלות נגישות ידועות</h2>
  <ul>
    <li>[פרטו כאן רכיבים, דפים או מסמכים שטרם הונגשו במלואם, אם יש, ואת מועד התיקון הצפוי. אם אין מגבלות ידועות, ציינו זאת במפורש]</li>
  </ul>

  <h2>פנייה בנושא נגישות</h2>
  <p>רכז/ת נגישות: [שם]</p>
  <p>טלפון: <a href="tel:+97212345678" dir="ltr">+972-1-234-5678</a></p>
  <p>דוא"ל: <a href="mailto:negishot@example.co.il">negishot@example.co.il</a></p>

  <p>תאריך ביקורת הנגישות האחרונה: [תאריך]</p>
  <p>תאריך עדכון ההצהרה: [תאריך]</p>
</article>
```

The full required-content list (7 items, including known limitations and the audit date) is in `references/is-5568.md`. A statement that omits known limitations or the audit date is a common audit finding.

### Step 10: Automated Accessibility Testing

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

## Recommended MCP Servers

No relevant MCP server applies to Israeli accessibility compliance. The skills-il MCP directory has no accessibility, IS 5568, or WCAG-auditing MCP at this time. The audit in this skill runs as a local Python script (`scripts/audit_a11y.py`), not through an MCP. If an accessibility-audit MCP is added to the directory later, prefer it for live-site scanning and keep the script for offline checks.

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
- `scripts/audit_a11y.py` -- Static-HTML IS 5568 audit: lang, dir, title, skip link, image alt, form labels, accessibility-statement link, heading levels. Exits 1 when a check fails, so it works as a CI gate. Run: `python scripts/audit_a11y.py --help`

### References
- `references/is-5568.md` -- Clause-by-clause IS 5568 reference mapped to WCAG 2.0 AA, Israeli additions, exemption tiers, both enforcement tracks, the coordinator role, the statement template, and the audit checklist.
- `references/widget-implementation.md` -- Copy-pasteable TypeScript/React code for a Regulation 35 preferences widget: pub-sub store, CSS class toggles, FOUC bootstrap, `Alt+A` shortcut, `MotionConfig` wiring, counter-invert rules.

## Building a Compliant Accessibility Preferences Widget

Israeli consumer-facing sites commonly expose an accessibility control surface (no regulation mandates a widget as such) that users can operate with the keyboard, typically a floating widget with toggles for contrast, text size, line spacing, cursor, and motion. This widget is a **user-preference comfort tool**, not an automation overlay. The difference is legally and financially significant: the FTC fined accessiBe $1M in April 2025 for misleading claims that its overlay auto-remediated sites (it didn't). The widget you ship must do only what the user asks it to do.

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
- Israeli accessibility law (IS 5568) is anchored to WCAG 2.0 AA (sources differ on whether the current edition reaches 2.1), and adds Israeli-specific requirements on top, including the bilingual-content expectation for public bodies that serve the public in Hebrew and Arabic (see Step 5). Agents may apply only WCAG without the Israeli additions.
- Agents may copy a stale "businesses with 25+ employees or 300,000 NIS revenue must comply" rule. That figure is not in the regulations. The website-accessibility duty is universal for public-facing services, subject to revenue-based exemptions (see Step 2, Who Is Exempt). The 25-employee number is the trigger for appointing an accessibility coordinator under s.19מב of the Act, a separate duty in a different instrument.
- Agents may present the 50,000 NIS statutory-damages ceiling as a flat current figure. It is the base in s.19נא(ב) and is index-linked annually under s.19נא(ו) against the CPI, base index February 2005 (see Step 3).
- Agents may treat the civil and administrative tracks as purely cumulative. Sections 19נא(ג)(1א)-(1ב) and 19נג(ג) give an operator that has filed a written undertaking, or that was already penalised administratively for the same act, a defense against damages without proof of harm (see Step 3).
- Agents may skip the 60-day cure period. A non-compliant operator must first receive a fix notice and be given up to 60 days before a suit or class-action request has a cause of action (see Step 3).
- Screen readers for Hebrew (NVDA, JAWS) read RTL text differently than LTR. Agents may generate ARIA labels assuming LTR reading order, which confuses Hebrew screen reader users.
- Israeli law requires accessibility statements (hatzaharat negishut) to be published on every website. Agents may generate WCAG-compliant sites without this mandatory statement page.
- Color contrast requirements in IS 5568 match WCAG (4.5:1 for normal text, 3:1 for large text), but agents may not account for Hebrew font rendering, which can appear thinner than Latin fonts at the same size, requiring slightly higher contrast.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Commission for Equal Rights of Persons with Disabilities | https://www.gov.il/he/departments/moj_disability_rights/govil-landing-page | Law, enforcement, complaints |
| IS 5568 / Tav Negishut | https://www.sii.org.il/en/ | Source for the IS 5568 standard |
| Equal Rights Act (Nevo) | https://www.nevo.co.il/law_html/law01/p214m2_001.htm | Statute text: 19מב, 19נא, 19נג, chapter ט' |
| WCAG 2.0 quick reference | https://www.w3.org/WAI/WCAG21/quickref/?versions=2.0 | AA success criteria, the version IS 5568 is anchored to |
| Website accessibility exemptions (Kol Zchut) | https://www.kolzchut.org.il/he/פטור_מחובת_הנגשה_לאתרי_אינטרנט_ואפליקציות | Revenue-based exemption tiers |
| NVDA Hebrew support | https://www.nvaccess.org/ | Free screen reader used for Hebrew testing |

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