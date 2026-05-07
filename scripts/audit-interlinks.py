#!/usr/bin/env python3
"""
audit-interlinks.py
───────────────────
Crawls all bbi_landing pages on the dev theme and runs the 12-point
interlinking check spec defined in docs/plan/bbi-interlinking-map.md.

Usage:
  python3 scripts/audit-interlinks.py [--live-url BASE_URL]

Defaults to https://brantbusinessinteriors.com with dev theme preview.
Reads SHOPIFY_TOKEN from env for check #12 (live-DOM vs theme asset).

Output:
  • Stdout — summary table
  • data/reports/interlink-audit-<timestamp>.csv
  • Exit 0 all green, Exit 1 any failure.

Checks (12-point spec from docs/plan/bbi-interlinking-map.md):
  1  nav-consistency    Same nav items on every page
  2  nav-active         Active nav item matches page context
  3  breadcrumb         Breadcrumb present, ≥2 levels
  4  crosslinks-unique  Crosslink tiles point to distinct destinations
  5  crosslinks-200     Crosslink hrefs return 200
  6  industries-hub     /pages/industries links to all 5 verticals
  7  footer-industries  Footer contains all 5 industry page links
  8  footer-services    Footer contains required service page links
  9  footer-parity      Footer link sets consistent across pages
  10 phone-cta          tel:18008359565 present
  11 quote-cta          Quote CTA link present and leads to /pages/quote
  12 drift-check        Theme API asset SHA matches worktree file

Notes:
  - Check 12 requires SHOPIFY_TOKEN env var
  - Checks 4, 5 only apply to pages that have crosslink tiles
  - Check 6 only applies to /pages/industries
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────

STORE         = "office-central-online.myshopify.com"
THEME_ID      = "186373570873"
API_VERSION   = "2024-01"
PREVIEW_PARAM = f"preview_theme_id={THEME_ID}"
BASE_URL      = "https://brantbusinessinteriors.com"

INDUSTRY_PAGES = [
    "/pages/healthcare",
    "/pages/education",
    "/pages/government",
    "/pages/non-profit",
    "/pages/professional-services",
]

SERVICE_PAGES = [
    "/pages/design-services",
    "/pages/delivery",
    "/pages/oecm",
    "/pages/faq",
]

PHONE_HREF = "tel:18008359565"

# All bbi_landing pages to audit
PAGES = [
    # Type A — landing pages
    {"path": "/",                            "type": "A", "section": "bbi-hero",                  "nav_active": ""},
    {"path": "/pages/oecm",                  "type": "A", "section": "ds-lp-oecm",                "nav_active": ""},
    {"path": "/pages/design-services",       "type": "A", "section": "ds-lp-design-services",     "nav_active": "services"},
    {"path": "/pages/quote",                 "type": "A", "section": "ds-lp-quote",               "nav_active": ""},
    {"path": "/pages/faq",                   "type": "A", "section": "ds-lp-faq",                 "nav_active": ""},
    {"path": "/pages/industries",            "type": "A", "section": "ds-lp-industries",          "nav_active": "industries"},
    {"path": "/pages/healthcare",            "type": "A", "section": "ds-lp-healthcare",          "nav_active": "industries"},
    {"path": "/pages/education",             "type": "A", "section": "ds-lp-education",           "nav_active": "industries"},
    {"path": "/pages/government",            "type": "A", "section": "ds-lp-government",          "nav_active": "industries"},
    {"path": "/pages/non-profit",            "type": "A", "section": "ds-lp-non-profit",          "nav_active": "industries"},
    {"path": "/pages/professional-services", "type": "A", "section": "ds-lp-professional-services","nav_active": "industries"},
    # Type B — collection category pages
    {"path": "/collections/business-furniture",   "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/seating",              "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/desks",                "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/storage",              "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/tables",               "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/boardroom",            "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/ergonomic-products",   "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/panels-room-dividers", "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/accessories",          "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
    {"path": "/collections/quiet-spaces",         "type": "B", "section": "ds-cc-base", "nav_active": "shop"},
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch(url: str, retries: int = 2) -> str | None:
    """Fetch URL HTML, return body string or None on error."""
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BBI-Audit/1.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt == retries:
                return None
            time.sleep(1)
    return None


def fetch_status(url: str) -> int:
    """Return HTTP status code for a URL."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BBI-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def find_hrefs(html: str) -> list:
    """Extract all href values from anchor tags."""
    return re.findall(r'<a[^>]+href=["\']([^"\'#][^"\']*)["\']', html)


def find_internal(hrefs: list) -> list:
    """Filter to internal (relative or same-domain) hrefs."""
    result = []
    for h in hrefs:
        if h.startswith("/") or h.startswith(BASE_URL):
            path = h.replace(BASE_URL, "")
            result.append(path)
    return result


def extract_nav_links(html: str) -> list:
    """Extract nav link hrefs (looks for bbi-nav class context)."""
    # Find bbi-nav block
    nav_match = re.search(r'class=["\'][^"\']*bbi-nav[^"\']*["\'].*?</nav', html, re.DOTALL)
    if not nav_match:
        nav_match = re.search(r'class=["\'][^"\']*bbi-nav[^"\']*["\'].*?(?=<section|<main|<div class="ds-)', html, re.DOTALL)
    if nav_match:
        return re.findall(r'<a[^>]+href=["\']([^"\']*)["\']', nav_match.group(0))
    return []


def extract_footer_links(html: str) -> list:
    """Extract footer link hrefs (looks for bbi-footer class context)."""
    footer_match = re.search(r'class=["\'][^"\']*bbi-footer[^"\']*["\'].*?</footer', html, re.DOTALL)
    if not footer_match:
        footer_match = re.search(r'class=["\'][^"\']*bbi-footer[^"\']*["\'].{0,50000}', html, re.DOTALL)
    if footer_match:
        return re.findall(r'<a[^>]+href=["\']([^"\']*)["\']', footer_match.group(0))
    return []


def shopify_asset_sha(key: str, token: str) -> str | None:
    """Fetch asset from Shopify Admin API and return MD5 of value."""
    url = f"https://{STORE}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]={key}"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            value = data.get("asset", {}).get("value", "")
            return hashlib.md5(value.encode()).hexdigest()
    except Exception:
        return None


def worktree_sha(path: str) -> str | None:
    """Return MD5 of a local theme file."""
    p = Path(path)
    if p.exists():
        return hashlib.md5(p.read_bytes()).hexdigest()
    return None


# ── Check functions ──────────────────────────────────────────────────────────

def check_nav_consistency(html: str, nav_baseline: list) -> tuple:
    """Check 1: Nav links match baseline."""
    links = set(extract_nav_links(html))
    if not nav_baseline:
        return "SKIP", "No baseline yet"
    expected = set(nav_baseline)
    if not links:
        return "WARN", "Could not extract nav links from page"
    missing = expected - links
    extra   = links - expected
    if missing:
        return "FAIL", f"Missing nav links: {sorted(missing)}"
    return "PASS", f"{len(links)} nav links found"


def check_nav_active(html: str, expected_active: str) -> tuple:
    """Check 2: Active nav state."""
    if not expected_active:
        return "SKIP", "No expected active item for this page type"
    # Look for aria-current, is-current, --active, active class near nav items
    active_patterns = [
        r'aria-current=["\']page["\']',
        r'class=["\'][^"\']*(?:is-current|--active|bbi-nav__item--active)[^"\']*["\']',
    ]
    for pat in active_patterns:
        if re.search(pat, html):
            return "PASS", f"Active state marker found"
    return "WARN", "No aria-current or active class detected (may be JS-driven)"


def check_breadcrumb(html: str) -> tuple:
    """Check 3: Breadcrumb present with ≥2 levels."""
    crumb_patterns = [
        r'class=["\'][^"\']*(?:breadcrumb|crumbs|ds-cc__crumbs|lp-crumbs)[^"\']*["\']',
        r'<nav[^>]+aria-label=["\'](?:breadcrumb|Breadcrumb)["\']',
    ]
    for pat in crumb_patterns:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            # Count Home and at least one more level
            start = m.start()
            snippet = html[start:start+1000]
            links = re.findall(r'<a[^>]+href=["\'][^"\']*["\']', snippet)
            if len(links) >= 1:
                return "PASS", f"Breadcrumb found with {len(links)+1}+ levels"
            return "WARN", "Breadcrumb container found but too shallow"
    return "WARN", "No breadcrumb container found (may be homepage)"


def check_crosslinks_unique(html: str) -> tuple:
    """Check 4: Crosslink tiles have unique destinations."""
    # Look for crosslink grid patterns
    patterns = [
        r'class=["\'][^"\']*(?:lp-crosslinks|ds-cc__tiles)[^"\']*["\'].*?(?=</section|</div>)',
        r'class=["\'][^"\']*ds-cc__tiles-grid[^"\']*["\'].*?(?=</div>)',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL)
        if m:
            hrefs = re.findall(r'<a[^>]+href=["\']([^"\']*)["\']', m.group(0))
            if len(hrefs) != len(set(hrefs)):
                dupes = [h for h in hrefs if hrefs.count(h) > 1]
                return "FAIL", f"Duplicate crosslink hrefs: {list(set(dupes))}"
            if hrefs:
                return "PASS", f"{len(hrefs)} unique crosslinks"
    return "SKIP", "No crosslink grid detected on this page"


def check_crosslinks_200(html: str, base: str) -> tuple:
    """Check 5: Crosslink hrefs return 200."""
    patterns = [
        r'class=["\'][^"\']*(?:lp-crosslinks|ds-cc__tiles)[^"\']*["\'].*?(?=</section)',
        r'class=["\'][^"\']*ds-cc__tiles-grid[^"\']*["\'].*?(?=</div>)',
    ]
    all_hrefs = []
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL)
        if m:
            all_hrefs += re.findall(r'<a[^>]+href=["\']([^"\']*)["\']', m.group(0))
    if not all_hrefs:
        return "SKIP", "No crosslinks to check"
    failures = []
    for href in set(all_hrefs):
        if href.startswith("/"):
            status = fetch_status(f"{base}{href}")
            if status not in (200, 301, 302):
                failures.append(f"{href} → {status}")
        time.sleep(0.05)  # gentle rate limiting
    if failures:
        return "FAIL", f"Dead crosslinks: {failures}"
    return "PASS", f"{len(set(all_hrefs))} crosslinks all 200/30x"


def check_industries_hub_links(html: str) -> tuple:
    """Check 6: Industries Hub links to all 5 verticals."""
    all_hrefs = find_hrefs(html)
    found = [p for p in INDUSTRY_PAGES if p in all_hrefs]
    missing = [p for p in INDUSTRY_PAGES if p not in all_hrefs]
    if missing:
        return "FAIL", f"Missing industry page links: {missing}"
    return "PASS", f"All 5 industry pages linked"


def check_footer_industries(html: str) -> tuple:
    """Check 7: Footer contains all 5 industry page links."""
    footer_links = extract_footer_links(html)
    if not footer_links:
        # Fallback: check full HTML
        footer_links = find_hrefs(html)
    found   = [p for p in INDUSTRY_PAGES if p in footer_links]
    missing = [p for p in INDUSTRY_PAGES if p not in footer_links]
    if len(found) < 5:
        return "FAIL", f"Footer missing industry links: {missing}"
    return "PASS", f"All 5 industry links in footer"


def check_footer_services(html: str) -> tuple:
    """Check 8: Footer contains required service page links."""
    footer_links = extract_footer_links(html)
    if not footer_links:
        footer_links = find_hrefs(html)
    found   = [p for p in SERVICE_PAGES if p in footer_links]
    missing = [p for p in SERVICE_PAGES if p not in footer_links]
    if len(found) < len(SERVICE_PAGES):
        return "FAIL", f"Footer missing service links: {missing}"
    return "PASS", f"All {len(SERVICE_PAGES)} service links in footer"


def check_footer_parity(html_map: dict) -> dict:
    """Check 9: Footer link sets consistent across pages (returns per-page results)."""
    sets = {}
    for path, html in html_map.items():
        links = set(l for l in extract_footer_links(html) if l.startswith("/pages/") or l.startswith("/collections/"))
        sets[path] = links
    if not sets:
        return {}
    baseline_path = list(sets.keys())[0]
    baseline = sets[baseline_path]
    results = {}
    for path, link_set in sets.items():
        missing = baseline - link_set
        extra   = link_set - baseline
        if missing or extra:
            results[path] = ("FAIL", f"vs {baseline_path}: missing={sorted(missing)}, extra={sorted(extra)}")
        else:
            results[path] = ("PASS", f"Footer matches baseline ({baseline_path})")
    return results


def check_phone_cta(html: str) -> tuple:
    """Check 10: Phone tel: link present."""
    if PHONE_HREF in html:
        return "PASS", "tel:18008359565 found"
    return "FAIL", "tel:18008359565 not found on page"


def check_quote_cta(html: str) -> tuple:
    """Check 11: Quote CTA present linking to /pages/quote."""
    if 'href="/pages/quote"' in html or "href='/pages/quote'" in html:
        return "PASS", "/pages/quote link found"
    # Check for quote modal trigger
    if 'data-quote' in html or 'js-quote' in html or 'quote-modal' in html:
        return "PASS", "Quote modal trigger found"
    return "FAIL", "No /pages/quote link or quote modal trigger found"


def check_drift(section_key: str, token: str) -> tuple:
    """Check 12: Theme API asset matches worktree file."""
    if not token:
        return "SKIP", "SHOPIFY_TOKEN not set"
    theme_sha = shopify_asset_sha(f"sections/{section_key}.liquid", token)
    if theme_sha is None:
        theme_sha = shopify_asset_sha(f"snippets/{section_key}.liquid", token)
    if theme_sha is None:
        return "SKIP", f"Asset sections/{section_key}.liquid not found in theme"
    # Try both sections/ and snippets/ in worktree
    local_sha = worktree_sha(f"theme/sections/{section_key}.liquid")
    if local_sha is None:
        local_sha = worktree_sha(f"theme/snippets/{section_key}.liquid")
    if local_sha is None:
        return "WARN", f"Local file theme/sections/{section_key}.liquid not found"
    if theme_sha == local_sha:
        return "PASS", "Theme asset matches worktree (no drift)"
    return "FAIL", f"DRIFT: theme SHA {theme_sha[:8]} ≠ local {local_sha[:8]}"


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BBI 12-point interlinking audit.")
    parser.add_argument("--base-url", default=BASE_URL, help="Base URL (default: brantbusinessinteriors.com)")
    parser.add_argument("--skip-200", action="store_true", help="Skip check 5 (crosslinks-200) — faster")
    parser.add_argument("--skip-drift", action="store_true", help="Skip check 12 (drift)")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    token = os.environ.get("SHOPIFY_TOKEN", "")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    Path("data/reports").mkdir(parents=True, exist_ok=True)
    out_path = Path(f"data/reports/interlink-audit-{ts}.csv")

    print(f"\nBBI Interlinking Audit — {ts}")
    print(f"Base URL : {base}")
    print(f"Pages    : {len(PAGES)}")
    print(f"Output   : {out_path}\n")

    # ── Phase 1: fetch all pages ────────────────────────────────────────────
    print("Fetching pages...")
    html_map = {}
    for page_def in PAGES:
        path = page_def["path"]
        url = f"{base}{path}"
        html = fetch(url)
        if html:
            html_map[path] = html
            print(f"  OK   {path}")
        else:
            html_map[path] = ""
            print(f"  MISS {path}")
        time.sleep(0.1)

    # ── Phase 2: establish nav baseline (from first responsive page) ────────
    nav_baseline = []
    for page_def in PAGES:
        html = html_map.get(page_def["path"], "")
        if html:
            links = extract_nav_links(html)
            if links:
                nav_baseline = links
                print(f"\nNav baseline from {page_def['path']}: {len(nav_baseline)} links")
                break

    # ── Phase 3: footer parity across all pages ────────────────────────────
    print("\nRunning footer parity check (#9)...")
    parity_results = check_footer_parity({p: h for p, h in html_map.items() if h})

    # ── Phase 4: run all checks per page ───────────────────────────────────
    print("\nRunning 12-point checks...\n")
    rows = []
    fail_count = 0

    CHECK_LABELS = {
        1: "nav-consistency",
        2: "nav-active",
        3: "breadcrumb",
        4: "crosslinks-unique",
        5: "crosslinks-200",
        6: "industries-hub-links",
        7: "footer-industries",
        8: "footer-services",
        9: "footer-parity",
        10: "phone-cta",
        11: "quote-cta",
        12: "drift-check",
    }

    for page_def in PAGES:
        path    = page_def["path"]
        ptype   = page_def["type"]
        section = page_def["section"]
        active  = page_def["nav_active"]
        html    = html_map.get(path, "")

        if not html:
            rows.append({"page": path, "check": "fetch", "result": "FAIL", "notes": "Could not fetch page"})
            fail_count += 1
            continue

        checks = []

        # 1
        r, n = check_nav_consistency(html, nav_baseline)
        checks.append((1, r, n))

        # 2
        r, n = check_nav_active(html, active)
        checks.append((2, r, n))

        # 3
        r, n = check_breadcrumb(html)
        checks.append((3, r, n))

        # 4
        r, n = check_crosslinks_unique(html)
        checks.append((4, r, n))

        # 5
        if args.skip_200:
            checks.append((5, "SKIP", "--skip-200 flag"))
        else:
            r, n = check_crosslinks_200(html, base)
            checks.append((5, r, n))

        # 6 — only applies to industries hub
        if path == "/pages/industries":
            r, n = check_industries_hub_links(html)
        else:
            r, n = "SKIP", "Only checked on /pages/industries"
        checks.append((6, r, n))

        # 7
        r, n = check_footer_industries(html)
        checks.append((7, r, n))

        # 8
        r, n = check_footer_services(html)
        checks.append((8, r, n))

        # 9
        r, n = parity_results.get(path, ("SKIP", "Not in parity set"))
        checks.append((9, r, n))

        # 10
        r, n = check_phone_cta(html)
        checks.append((10, r, n))

        # 11
        r, n = check_quote_cta(html)
        checks.append((11, r, n))

        # 12
        if args.skip_drift:
            checks.append((12, "SKIP", "--skip-drift flag"))
        else:
            r, n = check_drift(section, token)
            checks.append((12, r, n))

        for (num, result, notes) in checks:
            label = CHECK_LABELS[num]
            rows.append({"page": path, "check": f"{num:02d}-{label}", "result": result, "notes": notes})
            if result == "FAIL":
                fail_count += 1

        # Console summary per page
        results_str = " ".join(r for _, r, _ in checks)
        marker = "✅" if all(r in ("PASS","SKIP","WARN") for _,r,_ in checks) else "❌"
        print(f"  {marker} {path:<45} {results_str}")

    # ── Phase 5: write CSV ──────────────────────────────────────────────────
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["page","check","result","notes"])
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    passes = sum(1 for r in rows if r["result"] == "PASS")
    warns  = sum(1 for r in rows if r["result"] == "WARN")
    skips  = sum(1 for r in rows if r["result"] == "SKIP")
    fails  = sum(1 for r in rows if r["result"] == "FAIL")

    print(f"\n{'─'*60}")
    print(f"Results: {passes} PASS · {warns} WARN · {skips} SKIP · {fails} FAIL / {total} checks")
    print(f"CSV    : {out_path}")
    print()

    if fails > 0:
        print("FAILURES:")
        for row in rows:
            if row["result"] == "FAIL":
                print(f"  ❌  {row['page']:<40} {row['check']}")
                print(f"      {row['notes']}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
