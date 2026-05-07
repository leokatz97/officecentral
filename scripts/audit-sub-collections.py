#!/usr/bin/env python3
"""
audit-sub-collections.py
────────────────────────
Checks every BBI sub-collection (Level 3 in the 3-level shop hierarchy)
against the canonical slug list from docs/plan/site-architecture-2026-04-25.md.

For each sub-collection:
  • HTTP status (200 / 301 / 404)
  • Product count via Shopify Admin REST API
  • Template suffix (should be blank — default collection.json)

Output:
  • Stdout — summary table + counts by category
  • data/reports/sub-collection-audit-<timestamp>.csv
  • Exit 0 always (report-only, not a gate script)

Usage:
  python3 scripts/audit-sub-collections.py [--no-preview]

Reads SHOPIFY_TOKEN from env for product-count API calls.
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────

STORE       = "office-central-online.myshopify.com"
THEME_ID    = "186373570873"
API_VERSION = "2024-01"
BASE_URL    = "https://brantbusinessinteriors.com"

# Canonical sub-collection slug inventory from docs/plan/site-architecture-2026-04-25.md
# Format: {category: [slugs...]}
SUB_COLLECTIONS = {
    "seating": [
        "highback-seating",
        "medium-back-seating",
        "mesh-seating",
        "leather-faux-seating",
        "stools-seating",
        "lounge-chairs-seating",
        "ottomans",
        "guest-seating",
        "stacking-seating",
        "folding-stacking-chairs-carts",
        "nesting-chairs-chair",
        "24-hour-seating",
        "big-heavy-seating",
        "cluster-seating",
        "industrial-seating",
        "gaming",
    ],
    "desks": [
        "u-shape-desks-desks",
        "l-shape-desks-desks",
        "height-adjustable-tables-desks",
        "multi-person-workstations-desks",
        "benching-desks",
        "table-desks",
        "straight-desks-desks",
        "reception",
        "office-suites-desks",
    ],
    "storage": [
        "lateral-files-storage",
        "vertical-files",
        "storage-cabinets-storage",
        "bookcases-storage",
        "hutch",
        "lateral-storage-combo-storage",
        "end-tab-filing-storage",
        "pedestal-drawers-storage",
        "fire-resistant-safes-storage",
        "metal-shelving",
        "lockers",
        "fire-resistant-file-cabinets-storage",
        "wardrobe-storage",
        "credenzas",
    ],
    "tables": [
        "meeting-tables",
        "coffee-tables",
        "training-flip-top-tables",
        "end-tables-tables",
        "drafting-tables",
        "round-square-tables",
        "cafeteria-kitchen-tables",
        "bar-height-tables",
        "folding-tables-tables",
        "table-bases",
    ],
    "boardroom": [
        "boardroom-conference-meeting",
        "lecterns-podiums",
        "audio-visual-equipment",
    ],
    "ergonomic-products": [
        "height-adjustable-tables",
        "monitor-arms",
        "keyboard-trays",
        "desktop-sit-stand",
    ],
    "panels-room-dividers": [
        "room-dividers-panels-dividers",
        "desk-top-dividers",
        "modesty-panels",
    ],
    "accessories": [
        "chairmats-accessories",
        "power-modules-accessories",
        "coat-racks-accessories",
        "lighting",
    ],
    "quiet-spaces": [
        "telephone-booths",
        "walls",
        "sound-dampeners",
        "av-stand",
        "planters",
    ],
}

CATEGORY_PRODUCT_COUNT_SPEC = {
    "seating":              16,
    "desks":                9,
    "storage":              14,
    "tables":               10,
    "boardroom":            3,
    "ergonomic-products":   4,
    "panels-room-dividers": 3,
    "accessories":          4,
    "quiet-spaces":         5,
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def http_status(url: str) -> int:
    """Return HTTP status for a URL (follows redirects)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BBI-SubCollection-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1


def get_collection_info(handle: str, token: str) -> dict:
    """
    Fetch collection by handle + product count from Shopify Admin API.
    Returns dict with id, title, products_count, template_suffix, or {} if not found.
    Tries smart_collections then custom_collections. Product count fetched via
    /collections/{id}/products/count.json (products_count is not on the list endpoint).
    """
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    for endpoint in ("smart_collections", "custom_collections"):
        url = (
            f"https://{STORE}/admin/api/{API_VERSION}/{endpoint}.json"
            f"?handle={handle}&fields=id,handle,title,template_suffix"
        )
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read())
            key = endpoint  # custom_collections / smart_collections
            cols = data.get(key, [])
            if not cols:
                continue
            col = cols[0]
            # Fetch product count via products/count?collection_id= (more reliable)
            col_id = col["id"]
            time.sleep(0.5)  # rate-limit: Shopify Basic = 2 calls/sec
            count_url = f"https://{STORE}/admin/api/{API_VERSION}/products/count.json?collection_id={col_id}"
            try:
                req2 = urllib.request.Request(count_url, headers=headers)
                with urllib.request.urlopen(req2, timeout=12) as r2:
                    count_data = json.loads(r2.read())
                col["products_count"] = count_data.get("count", None)
            except Exception:
                col["products_count"] = None
            return col
        except Exception:
            pass
    return {}


def flag_issues(status: int, product_count, template_suffix: str) -> list:
    """Return list of issue strings for a sub-collection."""
    issues = []
    if status == 404:
        issues.append("404-not-found")
    elif status != 200:
        issues.append(f"http-{status}")
    if product_count == 0:
        issues.append("empty-collection")
    elif product_count is None:
        issues.append("api-miss")
    if template_suffix and template_suffix != "":
        issues.append(f"wrong-suffix:{template_suffix}")
    return issues


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audit BBI sub-collections (report only).")
    parser.add_argument("--no-http", action="store_true", help="Skip HTTP status checks (faster)")
    parser.add_argument("--no-api", action="store_true", help="Skip Shopify API product-count checks")
    args = parser.parse_args()

    token = os.environ.get("SHOPIFY_TOKEN", "")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    Path("data/reports").mkdir(parents=True, exist_ok=True)
    out_path = Path(f"data/reports/sub-collection-audit-{ts}.csv")

    total_slugs = sum(len(v) for v in SUB_COLLECTIONS.values())
    print(f"\nBBI Sub-Collection Audit — {ts}")
    print(f"Base URL : {BASE_URL}")
    print(f"Slugs    : {total_slugs} across {len(SUB_COLLECTIONS)} categories")
    print(f"HTTP     : {'SKIP' if args.no_http else 'ON'}")
    print(f"API      : {'SKIP (no SHOPIFY_TOKEN)' if not token else 'SKIP (--no-api)' if args.no_api else 'ON'}")
    print(f"Output   : {out_path}\n")

    rows = []
    category_summary = {}

    for category, slugs in SUB_COLLECTIONS.items():
        spec_count = CATEGORY_PRODUCT_COUNT_SPEC.get(category, len(slugs))
        cat_pass = 0
        cat_warn = 0
        cat_fail = 0

        print(f"── {category} ({len(slugs)} sub-collections) ──")

        for slug in slugs:
            url = f"{BASE_URL}/collections/{slug}"

            # HTTP check
            if args.no_http:
                status = "SKIP"
            else:
                status = http_status(url)
                time.sleep(0.15)

            # API check
            if not token or args.no_api:
                product_count = None
                template_suffix = "SKIP"
            else:
                info = get_collection_info(slug, token)
                product_count = info.get("products_count") if info else None
                template_suffix = info.get("template_suffix") or ""
                time.sleep(0.6)  # extra pause after both API calls complete

            # Determine result — SKIP only if BOTH HTTP and API are skipped
            no_data = (status == "SKIP") and (product_count is None) and (template_suffix == "SKIP")
            if no_data:
                result = "SKIP"
            else:
                issues = flag_issues(
                    status if status != "SKIP" else 200,
                    product_count,
                    template_suffix if template_suffix != "SKIP" else "",
                )
                if any("404" in i or "http-" in i or "wrong-suffix" in i for i in issues):
                    result = "FAIL"
                    cat_fail += 1
                elif "empty-collection" in issues or "api-miss" in issues:
                    result = "WARN"
                    cat_warn += 1
                else:
                    result = "PASS"
                    cat_pass += 1

            notes = "; ".join(flag_issues(
                status if status != "SKIP" else 200,
                product_count,
                template_suffix if template_suffix != "SKIP" else "",
            )) if result != "SKIP" else "checks skipped"

            icon = {"PASS": "✅", "WARN": "⚠ ", "FAIL": "❌", "SKIP": "──"}.get(result, "  ")
            prod_str = str(product_count) if product_count is not None else "—"
            print(f"  {icon} {slug:<45} http={status!s:<5} prods={prod_str:<6} {notes or 'OK'}")

            rows.append({
                "category":        category,
                "slug":            slug,
                "url":             url,
                "http_status":     status,
                "product_count":   product_count if product_count is not None else "",
                "template_suffix": template_suffix,
                "result":          result,
                "notes":           notes,
            })

        category_summary[category] = {
            "spec": spec_count,
            "pass": cat_pass,
            "warn": cat_warn,
            "fail": cat_fail,
        }
        print()

    # ── Write CSV ────────────────────────────────────────────────────────────
    fieldnames = ["category", "slug", "url", "http_status", "product_count",
                  "template_suffix", "result", "notes"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # ── Summary ──────────────────────────────────────────────────────────────
    total_pass = sum(v["pass"] for v in category_summary.values())
    total_warn = sum(v["warn"] for v in category_summary.values())
    total_fail = sum(v["fail"] for v in category_summary.values())
    total_checked = total_pass + total_warn + total_fail

    print("────────────────────────────────────────────────────────────")
    print(f"Category summary  (spec = expected sub-collection count):")
    print(f"  {'Category':<25} {'Spec':>5} {'Found':>6} {'PASS':>5} {'WARN':>5} {'FAIL':>5}")
    print("  " + "-" * 58)
    for cat, s in category_summary.items():
        found = s["pass"] + s["warn"] + s["fail"]
        print(f"  {cat:<25} {s['spec']:>5} {found:>6} {s['pass']:>5} {s['warn']:>5} {s['fail']:>5}")
    print("  " + "-" * 58)
    total_found = total_pass + total_warn + total_fail
    print(f"  {'TOTAL':<25} {total_slugs:>5} {total_found:>6} {total_pass:>5} {total_warn:>5} {total_fail:>5}")
    print(f"\nCSV    : {out_path}")

    if total_fail > 0:
        print(f"\n⚠  {total_fail} sub-collection(s) need attention (see FAIL rows above).")
    else:
        print(f"\n✅  All checked sub-collections OK.")

    # Exit 0 always — this is a report-only script
    sys.exit(0)


if __name__ == "__main__":
    main()
