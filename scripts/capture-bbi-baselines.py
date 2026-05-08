#!/usr/bin/env python3
"""
capture-bbi-baselines.py
BBI Launch Readiness — Phase 3 Screenshot Baseline Tool

Usage:
    python3 scripts/capture-bbi-baselines.py
    python3 scripts/capture-bbi-baselines.py --url http://127.0.0.1:9292/pages/healthcare
    python3 scripts/capture-bbi-baselines.py --lock   # copy current/ → locked/

Saves screenshots to:
    data/baselines/{template-type}/{slug}-{viewport}.png

Requirements:
    pip install playwright
    playwright install chromium

The URLs below point to shopify theme dev localhost (NOT live admin).
No cookies are stored; no credentials are sent.
"""

import argparse
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

# ─── URL list ────────────────────────────────────────────────────────────────
# Edit BASE_URL to match your `shopify theme dev` local address.
# Default is 127.0.0.1:9292 (Shopify CLI 3.x default).

BASE_URL = "http://127.0.0.1:9292"

URLS = [
    # (url, template_type, slug)
    (f"{BASE_URL}/",                                         "homepage",      "home"),
    (f"{BASE_URL}/collections/business-furniture",           "hub",           "business-furniture"),
    (f"{BASE_URL}/collections/seating",                      "hub",           "seating"),
    (f"{BASE_URL}/collections/desks",                        "hub",           "desks"),
    (f"{BASE_URL}/collections/highback-seating",             "sub-collection","highback-seating"),
    (f"{BASE_URL}/collections/mesh-seating",                 "sub-collection","mesh-seating"),
    (f"{BASE_URL}/products/ashton-high-back-tilter",         "pdp",           "ashton-high-back-tilter"),
    (f"{BASE_URL}/pages/healthcare",                         "industry",      "healthcare"),
    (f"{BASE_URL}/pages/education",                          "industry",      "education"),
    (f"{BASE_URL}/pages/oecm",                               "service",       "oecm"),
    (f"{BASE_URL}/pages/quote",                              "service",       "quote"),
    (f"{BASE_URL}/pages/industries",                         "hub",           "industries"),
    (f"{BASE_URL}/pages/faq",                                "service",       "faq"),
    (f"{BASE_URL}/pages/about",                              "trust",         "about"),
]

VIEWPORTS = [
    {"width": 375,  "height": 812,  "name": "375"},   # iPhone SE / mobile
    {"width": 768,  "height": 1024, "name": "768"},   # iPad / tablet
    {"width": 1280, "height": 900,  "name": "1280"},  # desktop
]

BASELINES_DIR = Path("data/baselines")

# ─── Helpers ─────────────────────────────────────────────────────────────────

def slug_from_url(url: str) -> str:
    """Derive a filesystem-safe slug from a URL path."""
    path = urlparse(url).path.strip("/") or "home"
    return path.replace("/", "-")


def output_path(base_dir: Path, template_type: str, slug: str, viewport_name: str) -> Path:
    d = base_dir / template_type
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{slug}-{viewport_name}.png"


def check_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except ImportError:
        return False


# ─── Main capture logic ───────────────────────────────────────────────────────

def capture_url(page, url: str, template_type: str, slug: str, viewport: dict, out_dir: Path) -> dict:
    """Screenshot one (URL, viewport) pair. Returns a result dict."""
    vp_name = viewport["name"]
    dest = output_path(out_dir, template_type, slug, vp_name)

    try:
        page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
        page.goto(url, wait_until="networkidle", timeout=30_000)
        # Wait for BBI nav to be present (if available); fall back after 3s
        try:
            page.wait_for_selector(".bbi-header", timeout=3_000)
        except Exception:
            pass
        page.screenshot(path=str(dest), full_page=True)
        return {"url": url, "viewport": vp_name, "file": str(dest), "status": "OK", "error": ""}
    except Exception as exc:
        return {"url": url, "viewport": vp_name, "file": str(dest), "status": "FAIL", "error": str(exc)}


def run_capture(urls_to_capture, out_dir: Path):
    from playwright.sync_api import sync_playwright

    results = []
    total = len(urls_to_capture) * len(VIEWPORTS)
    done = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            # No stored auth state — these are public dev-theme pages
            ignore_https_errors=True,
        )
        page = context.new_page()

        for (url, template_type, slug) in urls_to_capture:
            for vp in VIEWPORTS:
                result = capture_url(page, url, template_type, slug, vp, out_dir)
                results.append(result)
                done += 1
                status_icon = "✓" if result["status"] == "OK" else "✗"
                print(f"  [{done}/{total}] {status_icon} {slug} @ {vp['name']}px  →  {result['file']}")
                if result["status"] == "FAIL":
                    print(f"        ERROR: {result['error']}")

        context.close()
        browser.close()

    return results


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Capture BBI dev-theme screenshot baselines using Playwright."
    )
    parser.add_argument(
        "--url",
        help="Override: capture a single URL instead of the full list. "
             "Format: http://127.0.0.1:9292/some/path",
        default=None,
    )
    parser.add_argument(
        "--out-dir",
        help="Override output directory (default: data/baselines/current/)",
        default=None,
    )
    parser.add_argument(
        "--lock",
        action="store_true",
        help="Copy data/baselines/current/ → data/baselines/locked/ after capture.",
    )
    args = parser.parse_args()

    # Check we're in the repo root
    if not Path("theme").is_dir():
        print("ERROR: Run this script from the repo root (Office Central/).")
        sys.exit(1)

    # Playwright availability check
    if not check_playwright():
        print("ERROR: Playwright is not installed.")
        print()
        print("To install:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print()
        print("Then re-run this script.")
        sys.exit(1)

    # Determine output directory
    if args.out_dir:
        out_dir = Path(args.out_dir)
    else:
        out_dir = BASELINES_DIR / "current"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build URL list
    if args.url:
        parsed = urlparse(args.url)
        slug = slug_from_url(args.url)
        template_type = "override"
        urls_to_capture = [(args.url, template_type, slug)]
        print(f"Single-URL mode: {args.url}  (slug: {slug})")
    else:
        urls_to_capture = URLS
        print(f"Full capture: {len(URLS)} URLs × {len(VIEWPORTS)} viewports = {len(URLS)*len(VIEWPORTS)} screenshots")

    print(f"Output dir: {out_dir}")
    print(f"Base URL:   {BASE_URL}")
    print()
    print("Make sure `shopify theme dev` is running at the BASE_URL above.")
    print("Press Ctrl-C to cancel.")
    print()

    start = time.time()
    results = run_capture(urls_to_capture, out_dir)
    elapsed = time.time() - start

    ok = sum(1 for r in results if r["status"] == "OK")
    fail = sum(1 for r in results if r["status"] == "FAIL")

    print()
    print(f"Done in {elapsed:.1f}s — {ok} OK / {fail} FAIL")

    if args.lock:
        import shutil
        locked_dir = BASELINES_DIR / "locked"
        if locked_dir.exists():
            shutil.rmtree(locked_dir)
        shutil.copytree(str(out_dir), str(locked_dir))
        print(f"Locked: {out_dir}  →  {locked_dir}")

    if fail > 0:
        print()
        print("FAILED captures:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  {r['url']}  @{r['viewport']}px  —  {r['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
