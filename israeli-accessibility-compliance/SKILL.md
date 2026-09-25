---
name: israeli-accessibility-compliance
description: Not an accessibility surveyor's opinion and not legal advice. Implement Israeli web accessibility compliance per IS 5568 standard, which is WCAG 2.0 AA plus Israeli national changes, for Hebrew RTL applications. Use when user asks about Israeli accessibility law, "negishot" (accessibility), IS 5568, "teken negishot" (accessibility standard), "nachim" (disabilities), Hebrew screen reader support, RTL ARIA patterns, or accessibility audit for Israeli websites. Covers mandatory legal requirements under the Equal Rights for Persons with Disabilities Act, who is exempt, enforcement and penalties, the accessibility coordinator role, Hebrew screen reader compatibility (NVDA, JAWS, VoiceOver), native mobile apps, and RTL-specific ARIA patterns. Do NOT use for general WCAG guidance without Israeli context (use standard a11y resources instead), or for building a self-hosted accessibility preferences widget (use wcag-accessibility-widget).
license: MIT
allowed-tools: Bash(python:*) Bash(pip:*)
compatibility: Works with any web framework. Python 3.9+ for audit script. No network required for core patterns. axe-core for automated testing.
---

# Israeli Accessibility Compliance

## Legal notice

This is a free information tool operated by an AI model. It explains Israeli accessibility law, maps the IS 5568 requirements, runs static HTML checks and drafts an accessibility statement, and all of its output is produced automatically, without the involvement, review or approval of a certified accessibility expert (morshe negishut). The output is not a certified accessibility expert's opinion, not an accredited accessibility audit and not legal advice: it is raw technical and explanatory material only. It does not include manual testing with assistive technology, does not review documents under IS 5568 Part 2, does not produce the technological-difficulty opinion required by Regulation 35ו(א), and does not verify the current index-linked statutory damages figure. An AI model may err, omit data or present a wrong conclusion.

The accessibility statement block in Step 9 and the output of audit_a11y.py are a working draft for internal organisational use, to be reviewed by a certified accessibility expert (morshe negishut) before publication and before being relied on against an enforcement action or a civil claim. This tool is not a substitute for advice that takes into account the particular circumstances and needs of each person, and before publishing an accessibility statement, claiming an exemption or answering a complaint you should turn to a certified accessibility expert or to a lawyer.

## Instructions

### Step 1: Understand the Legal Framework

Israeli web accessibility (negishot) is legally mandatory under the **Equal Rights for Persons with Disabilities Act (Chok Shivyon Zechuyot Le'Anashim Im Mugbaluyot), 1998** and the **Equal Rights for Persons with Disabilities (Service Accessibility Accommodations) Regulations, 2013** (Takanot Negishut LeSherut). The web duty is Sign ג' of Chapter ה' of those Regulations, **regulations 35 to 35ו**, added by the 2017 amendment and in force from 26 October 2017. Regulation 35 by itself holds only definitions, so cite the sub-regulation:

| Regulation | What it holds |
|------------|---------------|
| 35 | Definitions. "Internet service" expressly covers websites, documents and apps; the standard is IS 5568, all parts, as amended from time to time |
| 35א | The duty: IS 5568 at level AA (apps and time-based media go to 35ג and 35ד), documents, and the 60-day notice rule in 35א(ד) |
| 35ב | Third-party and user-generated content: the operator is not liable for it, but must supply accessible infrastructure such as an image-description field |
| 35ג | Mobile apps (Step 6a) |
| 35ד | Video: captions (WCAG 1.2.2) are required only of a public authority, or of an operator with average turnover above 5 million NIS, that edits or produces the video |
| 35ה | The accessibility statement (Step 9) |
| 35ו | Exemptions (Step 2), including technological difficulty |

**WCAG version.** IS 5568 Part 1, current edition September 2023 (replacing May 2021), states that apart from its national changes it is identical to **WCAG 2.0** of December 2008. It contains no 2.1 or 2.2 criteria. The national changes: 1.2.1 to 1.2.3 raised from A to AA; 1.2.4 and 1.2.5 moved from AA to AAA, so not required; 2.4.10 Section Headings raised from AAA to AA; 3.1.2 Language of Parts does not apply. Meeting WCAG 2.1 or 2.2 on top is future-proofing, not the legal floor.

**Who must comply:** All public-facing Israeli websites and mobile applications of service providers open to the public, including government agencies, educational institutions, healthcare providers, businesses, and non-profits.

**Standard conformance is necessary but not sufficient.** The legal duty is the *regulation*, which *incorporates IS 5568 by reference at level AA*. You can pass an automated WCAG / IS 5568 audit and still be non-compliant if you lack the accessibility statement, the coordinator (where required), or the reporting channel, and vice versa. Treat "meets IS 5568" and "legally compliant" as two separate checklists.

**Technological difficulty (35ו(א) to (ג)).** A certified service-accessibility expert (morshe negishut hasherut) may exempt a specific adjustment the operator's platform cannot technically support, based on the opinion of a professional (ish miktzoa), on the Commissioner's published form. The exemption lasts up to 3 years and can be renewed once for up to 3 more; beyond that only the Commissioner can grant it. The operator must provide alternative access, publish the exemption and the alternatives in the statement, and hand the form to a person with a disability who asks.

**Digital documents (IS 5568 Part 2).** Part 2 (current edition September 2023, replacing May 2020) covers documents such as PDFs and Office files. Under 35א(ג) a document prepared from 26 October 2017 onward and uploaded to a site or app must be accessible, and forms for online filling are covered even if older. Downloadable documents are one of the most common real-world audit failures, so do not stop at the HTML.

### Step 2: Who Is Exempt

Regulation 35ו bases the website exemptions on **turnover** (average over the last three tax years with non-zero turnover), not on employee count. There is no "25 employees" trigger for the website duty, and the old 300,000 NIS tier in 35ו(ח) was transitional and expired on 26 October 2020.

| Operator | Position |
|----------|----------|
| Osek patur, or average annual turnover not above 100,000 NIS (35ו(ז)) | Exempt from the website duty; the regulation sets no time limit |
| Average turnover up to 1,000,000 NIS, for a site or app it began operating before the Regulations' commencement (read by Kol Zchut as before 26 October 2017) (35ו(ט)) | Exempt for 3 years from the end of the last tax year in the average, renewable every 3 years, provided its contact channels for receiving the service are published accessibly |
| Any other operator (a new site above the lowest tier, or turnover above 1,000,000 NIS) | No automatic exemption. May apply to the Commission for a heavy-burden exemption under Act s.19יג(א)(2) |
| Public authority | No turnover exemption and no heavy-burden application |

**Threshold discrepancy.** The regulation text says 100,000 NIS, with no indexation clause and no later amendment found, and it governs. Kol Zchut says 120,000 NIS and describes that tier as a temporary, 3-year renewable exemption. A registered osek patur is exempt whatever its turnover, so the gap between the two figures matters only for other operators (an osek murshe, a company, an amuta) with turnover in that band. Treat 100,000 NIS as the line, and take any reliance on the higher figure to a lawyer or accountant.

Other exemptions in 35ו: a platform limit on a social network (ד); the content, not the infrastructure, of a service limited to pre-registered users with at most 500 registered at any time, unless a person with a disability asks (ה); and advertising that has an accessible alternative (י). Turnover is the operator's whole VAT-law transaction turnover (or the amuta or income-tax equivalent defined in reg 35), not just the site's revenue. Exemption from website accessibility does not exempt the operator from other service-accessibility duties. In particular, regulation 34(א)(4) requires publishing the accessibility arrangements of the service and its premises **on the operator's website, if it has one**, and 34(ה) requires publishing any exemption and the alternative arrangements the same way; both sit outside Sign ג', so a site exempt under 35ו still owes them. Nor does it exempt the operator from the separate **physical-premises accessibility** duty (negishut hamivne), which has its own regulations.

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

Section 26ז(ב) separately sets **27,360 NIS** for breaches of the adequate-representation duty. The website and app duty (35א, 35ג) sits in part ג' of the Eighth Schedule, and failing to display the statement (35ה) in part א'. Under s.26יא a continuing breach adds one-fiftieth of the penalty for every month it continues, and a repeat breach of the same duty within two years adds a sum equal to the penalty. Reductions apply for a clean prior record and for corrective action.

**The two tracks are not purely cumulative.** Amendment 23 added defenses in s.19נא(ג)(1א)-(1ב): a court will **not** award damages without proof of harm where the operator had filed a **written undertaking (ktav hitchayvut)** under Chapter ט' Sign ג' **before** the act or omission sued on and is complying with it (and with any extra conditions the officer set), or where an administrative penalty or administrative warning was imposed on it for that act or omission **before** it occurred, that defense running for the period the Commissioner set for carrying out the accommodations. The timing is the condition: an undertaking filed after a demand letter or a claim does not, by itself, answer that claim. Section 19נא(ג) also bars these damages where an accessibility order was issued and is being complied with (1), where an earlier claim over the same act is being complied with or was filed less than three months before and the operator is fixing on a reasonable timetable (2), or where the operator made an inquiry to the Commission a reasonable time before the claim was filed (3). Section 19נג(ג) likewise bars the Commission from suing over an act it has already penalised administratively. So an operator that filed an undertaking, or was penalised or warned, before the conduct sued on has a real answer to a civil claim over that conduct; one that turns to the Commission only after a claim does not.

**60-day cure period (35א(ד)).** A deviation is not treated as a violation unless the operator was first sent a notice demanding a fix and failed to fix it within a reasonable time, no later than 60 days from receiving the notice. The Tel Aviv District Court (ת"צ 52621-07-23, 22.1.2024) held that a class-action request needs a prior notice at least for a missing statement (35ה) or missing arrangements (34); that is not a Supreme Court holding. It is a real defense for operators, but not a grace period: under 35א(ד)(2) the operator must provide an alternative accommodation as soon as possible after receiving the notice, while the fix is pending.

**Filing a complaint (user side).** A user who hits an inaccessible site sends the operator a fix notice (which starts the 60-day clock); if it is not fixed in time, the user can complain to the Commission for Equal Rights of Persons with Disabilities or sue for the statutory damages. An operator should route incoming accessibility complaints to one owner (the coordinator, where one is required, Step 4) and act within the cure window.

### Step 4: The Accessibility Coordinator (Rakaz Negishut)

The coordinator duty originates in the **primary Act, section 19מב** (added by Amendment 2, 2005); regulation 91 implements it. There is a **single trigger**: whoever is responsible for supplying a public service as defined in Sign ד' **and employs at least 25 employees** must appoint, from among its own staff, a person as expert in accessibility for people with disabilities as possible, and so far as possible a person with a disability, as the **accessibility coordinator** (rakaz negishut). There is no separate public-body limb in 19מב. Note this 25-employee figure is the trigger for the *coordinator appointment*, not for the website-accessibility duty itself, which is universal subject to the revenue exemptions above. Section 19מב(ב) itself lists exactly two duties:

- Gives the public information about the accessibility of the public service or of the place where it is given.
- Gives **advice and training (ייעוץ והדרכה)** on the public service's own accessibility obligations.

Regulation 91 of the Service Accessibility Regulations repeats the appointment (91(א)) and the same two duties (91(ד)), adds qualification and annual-update requirements (91(ב), 91(ג)), and requires the operator to publish the coordinator's name, office and contact channels (91(ה)). Handling public complaints is common practice, but it is not a listed duty in the Act or in regulation 91, so do not cite either for it.

Under 35ה, the coordinator's details belong in the accessibility statement only where the operator is obliged to appoint one (see Step 9).

### Step 5: IS 5568 vs WCAG -- Key Differences

Separate the three layers: the standard's national changes, duties that come from the Regulations, and good practice.

| Area | WCAG 2.0 | Israeli layer (source) |
|------|----------|------------------------|
| Time-based media | 1.2.1 to 1.2.3 at A; 1.2.4, 1.2.5 at AA | IS 5568: 1.2.1 to 1.2.3 at AA, 1.2.4 and 1.2.5 at AAA. Regulation 35ד limits the captions duty (Step 1) |
| Section headings | 2.4.10 at AAA | IS 5568: required at AA; mark headings with H tags wherever text has hierarchical structure |
| Language of parts | 3.1.2 at AA | IS 5568: does not apply. `lang` on mixed-language spans is still good practice |
| Accessibility statement | Not required | Regulation 35ה (Step 9) |
| Reporting channel | Not required | Regulation 35ה: contact details for reporting missing accessibility, including the 35א(ד)(1) notice |
| `dir="rtl"`, Hebrew error text, RTL label alignment | Not specified | Good practice for Hebrew sites, not a clause of IS 5568 |

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
  <!-- Skip link: the simplest way to meet WCAG 2.4.1 (landmarks also satisfy it) -->
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

Key points in this structure:
- `lang="he"` and `dir="rtl"` on the `html` element
- Skip link in Hebrew ("דלג לתוכן הראשי")
- ARIA roles for landmarks
- Hebrew ARIA labels for navigation
- Link to accessibility statement (Hatzaharat Negishot) in footer

### Step 6a: Native Mobile Apps (Regulation 35ג)

There is no Israeli app standard, so 35ג(ב) applies the IS 5568 success criteria to apps **as far as possible and relevant**, using the accessibility options the operating system provides, on **at least two common operating systems** (in practice iOS and Android). Under 35ג(ג) an app is exempt if the identical service runs on a mobile-adapted website that meets the standard, provided the app carries an accessible link to that site. Under 35ה the accessibility statement must also appear inside the app.

Build with the platform APIs (UIKit/SwiftUI accessibility properties, Android `contentDescription` and Compose semantics, React Native `accessibilityLabel`/`accessibilityRole`), respect system font scaling, and test with VoiceOver and TalkBack. `audit_a11y.py` cannot audit an app. See `references/mobile-apps.md` for the criterion-to-API map and the test tools.

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

The duty is **regulation 35ה**, not IS 5568 (the 2023 Part 1 edition has no statement section). It comes on top of regulations 34 and 91(ה), so the statement page is also the natural place to publish the service's accessibility arrangements (34(א)(4)) and the coordinator's details (91(ה)). The statement must be in a prominent place on the site **and in the app, if there is one**, and must include: information on the accessibility adjustments made; the coordinator's details and contact channels, **if the operator must appoint one**; and details for reporting missing accessibility or requesting an accommodation, including a fix notice under 35א(ד)(1). If a 35ו technological exemption applies, publish it and the alternatives here.

```html
<article dir="rtl" lang="he">
  <h1>הצהרת נגישות</h1>

  <p>אנו ב-[שם החברה] מחויבים להנגשת האתר לאנשים עם מוגבלויות
     בהתאם לתקן הישראלי IS 5568, המעוגן ב-WCAG 2.0 ברמה AA.</p>

  <h2>אמצעי נגישות באתר</h2>
  <ul>
    <li>האתר תומך בניווט מלא באמצעות מקלדת</li>
    <li>האתר נבדק עם קוראי המסך [NVDA, VoiceOver]</li>
    <li>תמונות מלוות בטקסט חלופי</li>
  </ul>

  <h2>מגבלות נגישות ידועות</h2>
  <ul>
    <li>[פרטו כאן רכיבים, דפים או מסמכים שטרם הונגשו במלואם, אם יש, ואת מועד התיקון הצפוי. אם אין מגבלות ידועות, ציינו זאת במפורש]</li>
  </ul>

  <h2>דיווח על בעיית נגישות או בקשת הנגשה</h2>
  <p>נתקלתם ברכיב לא נגיש? אפשר לדווח או לבקש הנגשה:</p>
  <p>דוא"ל: <a href="mailto:negishot@example.co.il">negishot@example.co.il</a></p>
  <p>טלפון: <a href="tel:+97230000000" dir="ltr">03-000-0000</a></p>

  <!-- רק אם הארגון חייב במינוי רכז נגישות -->
  <p>רכז/ת נגישות: [שם, דרכי התקשרות]</p>

  <h2>הסדרי נגישות בשירות ובסניפים</h2>
  <p>[התאמות הנגישות בשירות ובמקומות שבהם הוא ניתן, אמצעי עזר לפי בקשה ואיך מקבלים אותם (תקנה 34(א)(4))]</p>
  <p>[אם חל פטור: הפטור וההתאמות החלופיות (תקנה 34(ה))]</p>

  <p>תאריך עדכון ההצהרה: [תאריך]</p>
</article>
```

As good practice, offer at least two reporting channels, and make sure neither depends on the component that may be inaccessible. The fuller content list (tested assistive technology, known limitations, third-party content) is in `references/is-5568.md`.

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

    # Run axe-core's default rule set (WCAG rules plus best practices)
    results = driver.execute_async_script(
        "axe.run().then(arguments[arguments.length - 1]);")

    driver.quit()
    return results
```

**IS 5568 compliance checklist (automated + manual):**

| Check | Automated | Tool |
|-------|-----------|------|
| `lang="he"` present | Yes | axe-core |
| `dir="rtl"` on Hebrew pages (practice) | Yes | Custom rule |
| Color contrast 4.5:1 | Yes | axe-core |
| All images have alt text | Yes | axe-core |
| Form inputs have labels | Yes | axe-core |
| Bypass blocks (skip link or landmarks, WCAG 2.4.1) | Yes | axe-core `bypass` |
| Keyboard navigation | Manual | Tab-through test |
| Screen reader compatibility | Manual | NVDA/VoiceOver test |
| Hebrew error messages | Manual | Visual inspection |
| Accessibility statement | Manual | Page existence check |

See `references/is-5568.md` for the complete checklist mapped to IS 5568 clauses.

## Recommended MCP Servers

No skills-il MCP covers accessibility auditing; the audit is the local script `scripts/audit_a11y.py`.

## Examples

### Example 1: Audit Existing Israeli Website
User says: "Check if my website meets Israeli accessibility standards"
Result: Run `scripts/audit_a11y.py` against the URL for the static checks (lang, dir, title, bypass blocks, alt text, labels, headings, statement link), then axe-core (Step 10) for contrast and JavaScript-rendered content, and list the manual checks still owed. Report findings per criterion, never a legal "compliant" verdict.

### Example 2: Add Accessibility Statement Page
User says: "I need to add an accessibility page to comply with Israeli law"
Result: Create a Hebrew accessibility statement (Hatzaharat Negishot) page covering what regulation 35ה requires: the adjustments made, a channel for reporting missing accessibility or requesting an accommodation, and the coordinator's details where the operator must appoint one, plus known limitations and the last update date. Link it from every page, and from inside the app if there is one.

### Example 3: Fix RTL Form Accessibility
User says: "Screen readers are not reading my Hebrew form correctly"
Result: Add `dir="rtl"` to the form element, ensure all labels are associated with inputs and use Hebrew text, add `aria-required="true"` for mandatory fields, provide Hebrew error messages with `role="alert"`, and set `dir="ltr"` on numeric inputs like phone and ID number fields.

### Example 4: Make Hebrew Data Table Accessible
User says: "My Hebrew table is not accessible to screen readers"
Result: Add `dir="rtl"` to the table element, include a Hebrew `caption`, use `scope="col"` and `scope="row"` on header cells, mark LTR content like order numbers with `dir="ltr"`, and ensure logical reading order matches visual RTL order.

## Bundled Resources

### Scripts
- `scripts/audit_a11y.py` -- Static-HTML IS 5568 audit: lang, dir on RTL pages, title, bypass blocks (skip link or main landmark), alt quality, form labels, statement link, heading levels, plus overlay-script warnings. Cannot check contrast, JavaScript-rendered content, documents or apps. Exit 1 on a failed check, 2 on warnings only, 3 on a fetch error, so it works as a CI gate. Run: `python scripts/audit_a11y.py --help`

### References
- `references/is-5568.md` -- Clause-by-clause IS 5568 reference mapped to WCAG 2.0 AA, Israeli additions, exemption tiers, both enforcement tracks, the coordinator role, the statement template, and the audit checklist.
- `references/domain-checklist.md` -- Must-cover and should-cover items with their provisions, how accessibility class actions work, and explicit out-of-scope rows.
- `references/mobile-apps.md` -- Regulation 35ג for native apps, IS 5568 criteria mapped to iOS, Android and React Native accessibility APIs, and the app test tools.
- `references/widget-implementation.md` -- Design rules and copy-pasteable TypeScript/React code for an optional preferences widget: pub-sub store, CSS class toggles, FOUC bootstrap, `Alt+A` shortcut, `MotionConfig` wiring, counter-invert rules.

## Building an Accessibility Preferences Widget

Israeli consumer-facing sites commonly expose a keyboard-operable preferences widget (contrast, text size, line spacing, cursor, motion), but **no regulation requires one**, and it does not make a site compliant. Build it only as a **user-preference comfort tool**: it toggles CSS classes on `<html>` and never mutates content DOM, injects `alt` text or rewrites ARIA. The FTC fined accessiBe $1M in April 2025 for claiming its overlay auto-remediated sites. The design rules (single-source class table shared with a FOUC bootstrap script, `Alt+A` detected via `e.code`, `aria-pressed` only on binary toggles, counter-inverting the widget under invert contrast, a print reset) and the full code are in `references/widget-implementation.md`.

## Avoiding Overlay Anti-Patterns

Accessibility overlay products (accessiBe, UserWay, AudioEye) claim to make sites compliant by injecting JavaScript that auto-generates alt text, rewrites ARIA, and fixes inaccessible markup at runtime. Overlay-protected sites still fail screen-reader testing, and **in April 2025 the FTC fined accessiBe $1M** for misleading claims about its overlay.

The Israeli Commission for Equal Rights of Persons with Disabilities has not endorsed any overlay product. IS 5568 compliance is evaluated against the site's actual rendered HTML, not against claims made by a plug-in.

When building such a widget, enforce these scope fences:

| Do | Do NOT |
|----|--------|
| Toggle CSS classes on `<html>` | Mutate content DOM, rewrite `alt` attributes, or inject ARIA |
| Provide user-controlled preferences (contrast, text size, motion) | Claim the widget alone makes the site "IS 5568 compliant" or "WCAG compliant" |
| Document scope as a comfort tool in the accessibility statement | Display a certification badge or "audited by" claim sourced from a vendor plug-in |
| Use OS font stacks for the readable-font toggle | Inject a webfont that changes rendered text width and re-flows past critical content |
| Persist preferences to `localStorage` and a cookie you control | Use third-party overlay SDKs that fingerprint users or apply tracking cookies as a side effect |

A widget is at most one layer; the site itself still needs semantic HTML, correct `dir` and `lang`, keyboard operability, labels, focus management and real screen-reader testing.

## Gotchas
- IS 5568 is WCAG 2.0 AA with national changes (media criteria re-levelled, 2.4.10 Section Headings required, 3.1.2 dropped), and the Regulations add the statement and reporting-channel duties (see Step 5). Agents may apply plain WCAG, or cite WCAG 2.1 as the legal floor, and get both wrong.
- Agents may copy a stale "businesses with 25+ employees or 300,000 NIS revenue must comply" rule. The 300,000 NIS tier expired on 26 October 2020. The website-accessibility duty is universal for public-facing services, subject to the turnover-based exemptions in 35ו (see Step 2). The 25-employee number is the trigger for appointing an accessibility coordinator under s.19מב of the Act, a separate duty in a different instrument.
- Agents may present the 50,000 NIS statutory-damages ceiling as a flat current figure. It is the base in s.19נא(ב) and is index-linked annually under s.19נא(ו) against the CPI, base index February 2005 (see Step 3).
- Agents may treat the civil and administrative tracks as purely cumulative, or may drop the timing condition. Section 19נא(ג)(1א)-(1ב) bars damages without proof of harm only where the undertaking was filed, or the penalty or warning imposed, before the act or omission sued on; 19נג(ג) separately bars the Commission from suing over an act it already penalised (see Step 3).
- Agents may skip the 60-day cure period. Under 35א(ד)(1) a deviation is not a violation until a fix notice went unanswered for up to 60 days; that it also bars a class-action request without notice is a district-court reading (see Step 3).
- Screen readers for Hebrew (NVDA, JAWS) read RTL text differently than LTR. Agents may generate ARIA labels assuming LTR reading order, which confuses Hebrew screen reader users.
- Regulation 35ה requires an accessibility statement on every site and app that owes the duty. Agents may generate WCAG-compliant sites without it, or cite IS 5568 as its source, or say "Regulation 35" when the web rules are split across 35 to 35ו.
- Color contrast requirements in IS 5568 match WCAG (4.5:1 for normal text, 3:1 for large text). The ratio is the same for Hebrew, but thin Hebrew font weights can still read poorly at a passing ratio, so check legibility at the weight actually shipped.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Commission for Equal Rights of Persons with Disabilities: heavy-burden exemption service | https://www.gov.il/he/service/application_for_exemption_internet_people_with_disabilities | Heavy-burden application under s.19יג(א)(2), Commission contact channels |
| IS 5568 Part 1, September 2023 (gov.il copy) | https://www.gov.il/BlobFolder/legalinfo/israeli_accessibility_standards_pdf/he/sitedocs_si-5568-1-september-2023.pdf | WCAG 2.0 basis and the national changes |
| Equal Rights Act (Nevo) | https://www.nevo.co.il/law_html/law01/p214m2_001.htm | Statute text: 19מב, 19נא, 19נג, chapter ט' |
| WCAG 2.0 quick reference | https://www.w3.org/WAI/WCAG21/quickref/?versions=2.0 | AA success criteria, the version IS 5568 is anchored to |
| Website accessibility exemptions (Kol Zchut) | https://www.kolzchut.org.il/he/פטור_מחובת_הנגשה_לאתרי_אינטרנט_ואפליקציות | Revenue-based exemption tiers |
| Service Accessibility Regulations (Nevo) | https://www.nevo.co.il/law_html/law01/500_865.htm | Regulations 35 to 35ו (web and apps) and 91 (coordinator) |

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