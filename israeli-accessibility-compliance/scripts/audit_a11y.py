#!/usr/bin/env python3
"""Run IS 5568 accessibility audit on Israeli websites.

Checks for Israeli-specific accessibility requirements based on the
IS 5568 standard (Part 1, September 2023: WCAG 2.0 AA plus Israeli
national changes). Covers the page language, RTL direction on Hebrew
pages, bypass blocks, labels, headings, and a link to the accessibility
statement that regulation 35ה requires.

This is a STATIC-HTML auditor: it fetches the raw HTML and cannot
evaluate color contrast or JavaScript-rendered (SPA) content. For
contrast and JS-rendered checks, use the axe-core + Selenium path
shown in SKILL.md Step 10.

Exit codes: 0 all checks passed, no warnings; 1 a check failed; 2 no
failures but a warning (overlay script, statement on another domain);
3 the URL could not be fetched, so nothing was audited.

Usage:
    python audit_a11y.py --url https://www.example.com
    python audit_a11y.py --url https://www.example.com --output report.json
    python audit_a11y.py --help

Requirements:
    pip install requests beautifulsoup4
"""

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing required dependencies. Install with:", file=sys.stderr)
    print("  pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)


RTL_LANGS = ("he", "iw", "ar", "yi", "fa")


def _page_lang(soup):
    html_tag = soup.find("html")
    return (html_tag.get("lang", "") if html_tag else "").strip().lower()


def check_lang_attribute(soup):
    """Check that the page declares its language (WCAG 3.1.1).

    Any declared language passes: an English or Arabic page is correct
    with lang="en" or lang="ar". Requiring "he" false-FAILed every
    non-Hebrew page of a bilingual site.
    """
    html_tag = soup.find("html")
    if not html_tag:
        return {"pass": False, "message": "No <html> element found"}

    lang = html_tag.get("lang", "").strip()
    if lang:
        return {"pass": True, "message": f"lang=\"{lang}\" found"}
    return {"pass": False, "message": "No lang attribute on <html>"}


def check_dir_attribute(soup):
    """Check for RTL direction on pages whose declared language is RTL.

    dir="rtl" is good practice for Hebrew content, not a clause of
    IS 5568, and it does not apply to LTR pages.
    """
    html_tag = soup.find("html")
    if not html_tag:
        return {"pass": False, "message": "No <html> element found"}

    lang = _page_lang(soup)
    if lang and not lang.split("-")[0] in RTL_LANGS:
        return {"pass": True, "message": f"Not applicable (lang=\"{lang}\" is LTR)"}

    dir_attr = html_tag.get("dir", "")
    if dir_attr == "rtl":
        return {"pass": True, "message": "dir=\"rtl\" found"}
    elif dir_attr:
        return {
            "pass": False,
            "message": f"dir=\"{dir_attr}\" found but expected \"rtl\"",
        }
    return {"pass": False, "message": "No dir attribute on <html>"}


def check_page_title(soup):
    """Check for Hebrew page title."""
    title = soup.find("title")
    if title is None:
        return {"pass": False, "message": "No <title> element found"}
    # .string is None whenever <title> has more than one child node (a stray
    # comment, a split entity, a nested element), which would misreport a page
    # that does have a title. get_text() flattens all children.
    title_text = title.get_text(strip=True)
    if len(title_text) > 0:
        return {"pass": True, "message": f"Title: \"{title_text[:50]}\""}
    return {"pass": False, "message": "Empty <title> element"}


def check_skip_navigation(soup):
    """Check for a bypass-blocks mechanism (WCAG 2.4.1).

    A skip link is the simplest mechanism, but a <main> landmark (or
    role="main") also satisfies 2.4.1, so a page with landmarks and no
    skip link is not a failure.
    """
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        text = link.get_text(strip=True)
        if href.startswith("#") and ("דלג" in text or "skip" in text.lower()):
            return {"pass": True, "message": f"Skip link found: \"{text}\""}
    if soup.find("main") or soup.find(attrs={"role": "main"}):
        return {
            "pass": True,
            "message": "No skip link, but a main landmark is present (satisfies 2.4.1)",
        }
    return {
        "pass": False,
        "message": "No skip link (e.g. 'דלג לתוכן הראשי') and no <main> landmark",
    }


FILENAME_ALT = re.compile(r"\.(jpe?g|png|gif|webp|svg|avif)$|^(img|image|dsc|photo)[_-]?\d+", re.I)
GENERIC_ALT = {"תמונה", "צילום", "לוגו", "image", "img", "photo", "picture", "logo", "icon"}


def check_images_alt(soup):
    """Check image alt text.

    Missing alt fails. Empty alt is correct for a decorative image, so it
    passes, EXCEPT when the image is the only content of a link or button:
    then the control has no accessible name. Alt text that is a file name
    ("IMG_2031.jpg") or a generic word ("תמונה", "image") is reported too,
    because it satisfies a presence check while telling a screen-reader
    user nothing.
    """
    images = soup.find_all("img")
    if not images:
        return {"pass": True, "message": "No images found"}

    missing, unnamed_controls, weak = [], [], []
    for i, img in enumerate(images):
        src = img.get("src", f"image_{i}")[:50]
        hidden = (img.get("role") or "").lower() in ("presentation", "none") or \
            (img.get("aria-hidden") or "").lower() == "true"
        if not img.has_attr("alt"):
            if not hidden:
                missing.append(src)
            continue
        alt = (img.get("alt") or "").strip()
        if not alt:
            control = img.find_parent(["a", "button"])
            if control is not None and not _accessible_name(control):
                unnamed_controls.append(src)
            continue
        if FILENAME_ALT.search(alt) or alt.lower() in GENERIC_ALT:
            weak.append(f"{src} (alt=\"{alt[:30]}\")")

    problems = []
    if missing:
        problems.append(f"{len(missing)} images missing alt: {', '.join(missing[:3])}")
    if unnamed_controls:
        problems.append(
            f"{len(unnamed_controls)} image-only links/buttons with empty alt: {', '.join(unnamed_controls[:3])}"
        )
    if weak:
        problems.append(f"{len(weak)} images with file-name or generic alt: {', '.join(weak[:3])}")
    if problems:
        return {"pass": False, "message": "; ".join(problems)}
    return {"pass": True, "message": f"All {len(images)} images have usable alt (empty alt treated as decorative)"}


def _accessible_name(control):
    """Approximate a link or button's accessible name from ALL its content.

    aria-label / aria-labelledby win; otherwise the name is the text plus the
    alt of every image inside it, so an alt="" icon beside a named image or
    text still leaves the control named.
    """
    if (control.get("aria-label") or "").strip() or control.get("aria-labelledby"):
        return "aria"
    parts = [control.get_text(" ", strip=True)]
    parts += [(im.get("alt") or "").strip() for im in control.find_all("img")]
    return " ".join(p for p in parts if p).strip()


OVERLAY_HOSTS = ("acsbapp.com", "accessibe.com", "userway.org", "audioeye.com",
                 "equalweb.com", "nagich.co.il", "enable.co.il")


def check_overlay_scripts(soup):
    """WARN when a third-party accessibility overlay script is loaded.

    An overlay is not a failure by itself, but it does not make a page
    accessible, and the static checks above say nothing about what it
    injects at runtime. Always a warning, never a failure.
    """
    found = []
    for s in soup.find_all("script", src=True):
        host = urlparse(s["src"]).netloc.lower()
        if any(h in host for h in OVERLAY_HOSTS):
            found.append(host)
    if found:
        return {"pass": True, "warn": True,
                "message": f"Overlay script(s) loaded: {', '.join(sorted(set(found)))}. "
                           "An overlay does not make the page accessible; audit the page itself."}
    return {"pass": True, "message": "No known overlay script"}


def check_form_labels(soup):
    """Check that form inputs have associated labels.

    Recognises all three valid association mechanisms: explicit
    <label for="id">, implicit nesting (<label><input></label>), and
    aria-label / aria-labelledby. type="image" inputs are labelled by
    their alt text. Duplicate ids are reported separately, since a
    for= reference to a repeated id is ambiguous.
    """
    inputs = soup.find_all(["input", "select", "textarea"])
    unlabeled = []
    seen_ids = {}
    for inp in inputs:
        inp_type = (inp.get("type") or "").lower()
        if inp_type in ("hidden", "submit", "button", "reset"):
            continue

        inp_id = inp.get("id", "")
        if inp_id:
            seen_ids[inp_id] = seen_ids.get(inp_id, 0) + 1

        # image buttons are named by alt text, not by a label
        if inp_type == "image":
            if not (inp.get("alt") or "").strip():
                unlabeled.append(inp.get("name", inp_id or "image-input"))
            continue

        has_explicit = bool(inp_id and soup.find("label", attrs={"for": inp_id}))
        has_implicit = inp.find_parent("label") is not None
        # title= is the last fallback in the accessible-name computation, so a
        # control named only by title is labelled (weakly, but not unlabelled).
        has_aria = bool(
            (inp.get("aria-label") or "").strip() or inp.get("aria-labelledby")
            or (inp.get("title") or "").strip()
        )
        if not (has_explicit or has_implicit or has_aria):
            unlabeled.append(inp.get("name", inp_id or "unknown"))

    duplicates = [i for i, n in seen_ids.items() if n > 1]

    problems = []
    if unlabeled:
        problems.append(
            f"{len(unlabeled)} inputs without labels: {', '.join(unlabeled[:3])}"
        )
    if duplicates:
        problems.append(
            f"duplicate form ids (ambiguous label targets): {', '.join(duplicates[:3])}"
        )
    if problems:
        return {"pass": False, "message": "; ".join(problems)}
    return {"pass": True, "message": f"All {len(inputs)} form controls are labelled"}


def check_accessibility_statement(soup, base_url):
    """Look for a link that plausibly points at an accessibility statement.

    This is a WEAK signal, not verification. A third-party overlay widget
    link, or any link that merely mentions accessibility, also matches.
    The link must at least resolve to a distinct page: an in-page anchor,
    a javascript: handler or a link back to the current URL is rejected,
    because those are how overlay triggers present themselves. Confirming
    that the statement exists and carries the required content is a
    manual step. The statement itself is required by regulation 35ה, which
    asks for three things: the adjustments made, the coordinator's details
    where one must be appointed, and contact details for reporting missing
    accessibility. A statement hosted on another domain (typically an
    overlay vendor's) is reported as a warning, since the operator does not
    control its content.
    """
    links = soup.find_all("a", href=True)
    a11y_keywords = ["נגישות", "accessibility", "negishot"]

    for link in links:
        text = link.get_text(strip=True).lower()
        href = link.get("href", "").strip()
        if not any(kw in text or kw in href.lower() for kw in a11y_keywords):
            continue
        if href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        full_url = urljoin(base_url, href)
        if full_url.split("#")[0].rstrip("/") == base_url.split("#")[0].rstrip("/"):
            continue
        result = {
            "pass": True,
            "message": (
                f"Candidate accessibility link: \"{link.get_text(strip=True)}\" "
                f"-> {full_url} (verify the page content manually)"
            ),
        }
        page_host = urlparse(base_url).netloc.lower().removeprefix("www.")
        link_host = urlparse(full_url).netloc.lower().removeprefix("www.")
        if link_host and page_host and link_host != page_host:
            result["warn"] = True
            result["message"] += f"; hosted on another domain ({link_host})"
        return result

    return {
        "pass": False,
        "message": "No link to a separate accessibility statement page (הצהרת נגישות) found",
    }


def check_heading_hierarchy(soup):
    """Check heading levels for skips.

    Multiple <h1> elements are valid in HTML5 sectioning content and are
    NOT a WCAG 2.0 AA or IS 5568 failure, so they are not reported. The
    real finding is a skipped level (h2 followed by h4). A missing H1 is
    reported as a note, not a failure: WCAG does not require one.
    IS 5568 raises 2.4.10 Section Headings to AA, so a page with no
    headings at all fails; confirm manually that it really has no
    hierarchical text.
    """
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    if not headings:
        return {"pass": False, "message": "No headings found (IS 5568 2.4.10)"}

    h1_count = len(soup.find_all("h1"))

    skips = []
    previous = None
    for h in headings:
        level = int(h.name[1])
        if previous is not None and level > previous + 1:
            text = h.get_text(strip=True)[:30]
            skips.append(f"h{previous} -> h{level} at \"{text}\"")
        previous = level

    if skips:
        return {
            "pass": False,
            "message": f"{len(skips)} skipped heading level(s): {'; '.join(skips[:3])}",
        }

    note = "" if h1_count else "; note: no H1"
    return {
        "pass": True,
        "message": f"No skipped heading levels ({len(headings)} headings, {h1_count} H1{note})",
    }


def run_audit(url):
    """Run full IS 5568 accessibility audit on a URL."""
    print(f"Auditing: {url}\n")

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; a11y-audit/1.0; +https://agentskills.co.il)"
            },
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(3)  # distinct from 1: the page was never audited

    # response.text falls back to ISO-8859-1 when the server sends text/html with no
    # charset, which mojibakes every Hebrew byte and false-FAILs the Hebrew checks.
    soup = BeautifulSoup(response.content, "html.parser")

    checks = {
        "lang_attribute": check_lang_attribute(soup),
        "dir_attribute": check_dir_attribute(soup),
        "page_title": check_page_title(soup),
        "skip_navigation": check_skip_navigation(soup),
        "images_alt": check_images_alt(soup),
        "form_labels": check_form_labels(soup),
        "accessibility_statement": check_accessibility_statement(soup, url),
        "heading_hierarchy": check_heading_hierarchy(soup),
        "overlay_scripts": check_overlay_scripts(soup),
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    total = len(checks)

    print("IS 5568 Accessibility Audit Results")
    print("=" * 50)
    for name, result in checks.items():
        status = "PASS" if result["pass"] else "FAIL"
        if result["pass"] and result.get("warn"):
            status = "WARN"
        print(f"  [{status}] {name}: {result['message']}")

    warnings = sum(1 for c in checks.values() if c.get("warn"))
    print(f"\nScore: {passed}/{total} checks passed, {warnings} warning(s)")
    # A static check cannot establish legal compliance either way, so the
    # status never says "compliant" or "non-compliant". Warnings (an overlay
    # script, a statement hosted on another domain) mean the static checks
    # say little about what the user actually gets, so they never read PASSED.
    if passed < total:
        print("Status: AUTOMATED ISSUES FOUND - fix them, then run the manual checks")
    elif warnings:
        print("Status: NO STATIC FAILURES, BUT WARNINGS NEED REVIEW (see WARN lines; manual testing required)")
    else:
        print("Status: AUTOMATED CHECKS PASSED (manual testing still required)")

    return {"url": url, "checks": checks, "passed": passed, "total": total,
            "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(
        description="Run IS 5568 accessibility audit on Israeli websites"
    )
    parser.add_argument(
        "--url", required=True,
        help="URL to audit"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output JSON report file path (optional)"
    )
    args = parser.parse_args()

    results = run_audit(args.url)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nReport saved: {args.output}")

    # Exit codes: 0 = all checks passed with no warnings; 1 = at least one
    # check failed; 2 = no failures but at least one warning; 3 = fetch
    # error (raised in run_audit). A CI gate that
    # should tolerate an overlay can accept 2 explicitly.
    if results["passed"] < results["total"]:
        sys.exit(1)
    if results["warnings"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
