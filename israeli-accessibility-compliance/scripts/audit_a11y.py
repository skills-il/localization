#!/usr/bin/env python3
"""Run IS 5568 accessibility audit on Israeli websites.

Checks for Israeli-specific accessibility requirements based on the
IS 5568 standard, which is anchored to WCAG 2.0 AA (IS 5568 adds some
2.1-aligned criteria; sources differ). Covers Hebrew language
declaration, RTL direction, ARIA labels, and the mandatory
accessibility statement page.

This is a STATIC-HTML auditor: it fetches the raw HTML and cannot
evaluate color contrast or JavaScript-rendered (SPA) content. For
contrast and JS-rendered checks, use the axe-core + Selenium path
shown in SKILL.md Step 10.

Usage:
    python audit_a11y.py --url https://example.co.il
    python audit_a11y.py --url https://example.co.il --output report.json
    python audit_a11y.py --help

Requirements:
    pip install requests beautifulsoup4
"""

import argparse
import json
import sys
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing required dependencies. Install with:", file=sys.stderr)
    print("  pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def check_lang_attribute(soup):
    """Check for Hebrew language declaration on html element."""
    html_tag = soup.find("html")
    if not html_tag:
        return {"pass": False, "message": "No <html> element found"}

    lang = html_tag.get("lang", "")
    if lang.startswith("he"):
        return {"pass": True, "message": f"lang=\"{lang}\" found"}
    elif lang:
        return {
            "pass": False,
            "message": f"lang=\"{lang}\" found but expected \"he\"",
        }
    return {"pass": False, "message": "No lang attribute on <html>"}


def check_dir_attribute(soup):
    """Check for RTL direction declaration."""
    html_tag = soup.find("html")
    if not html_tag:
        return {"pass": False, "message": "No <html> element found"}

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
    """Check for skip navigation link."""
    skip_links = soup.find_all("a", href=True)
    for link in skip_links:
        href = link.get("href", "")
        text = link.get_text(strip=True)
        if href.startswith("#") and ("דלג" in text or "skip" in text.lower()):
            return {"pass": True, "message": f"Skip link found: \"{text}\""}
    return {
        "pass": False,
        "message": "No skip navigation link found (expected Hebrew text with 'דלג')",
    }


def check_images_alt(soup):
    """Check that all images have alt attributes."""
    images = soup.find_all("img")
    if not images:
        return {"pass": True, "message": "No images found"}

    missing = []
    for i, img in enumerate(images):
        if not img.has_attr("alt"):
            src = img.get("src", f"image_{i}")
            missing.append(src[:50])

    if missing:
        return {
            "pass": False,
            "message": f"{len(missing)} images missing alt: {', '.join(missing[:3])}",
        }
    return {"pass": True, "message": f"All {len(images)} images have alt text"}


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
        has_aria = bool(
            (inp.get("aria-label") or "").strip() or inp.get("aria-labelledby")
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
    that the statement exists and carries the seven required items is a
    manual step.
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
        return {
            "pass": True,
            "message": (
                f"Candidate accessibility link: \"{link.get_text(strip=True)}\" "
                f"-> {full_url} (verify the page content manually)"
            ),
        }

    return {
        "pass": False,
        "message": "No link to a separate accessibility statement page (הצהרת נגישות) found",
    }


def check_heading_hierarchy(soup):
    """Check heading levels for skips.

    Multiple <h1> elements are valid in HTML5 sectioning content and are
    NOT a WCAG 2.0 AA or IS 5568 failure, so they are not reported. The
    real finding is a skipped level (h2 followed by h4).
    """
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    if not headings:
        return {"pass": False, "message": "No headings found"}

    h1_count = len(soup.find_all("h1"))
    if h1_count == 0:
        return {"pass": False, "message": "No H1 heading found"}

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

    return {
        "pass": True,
        "message": f"No skipped heading levels ({len(headings)} headings, {h1_count} H1)",
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
        sys.exit(1)

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
    }

    passed = sum(1 for c in checks.values() if c["pass"])
    total = len(checks)

    print("IS 5568 Accessibility Audit Results")
    print("=" * 50)
    for name, result in checks.items():
        status = "PASS" if result["pass"] else "FAIL"
        print(f"  [{status}] {name}: {result['message']}")

    print(f"\nScore: {passed}/{total} checks passed")
    if passed < total:
        print("Status: NON-COMPLIANT - remediation required")
    else:
        print("Status: AUTOMATED CHECKS PASSED (manual testing still required)")

    return {"url": url, "checks": checks, "passed": passed, "total": total}


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

    # Non-zero exit when any check failed, so the script works as a CI gate.
    if results["passed"] < results["total"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
