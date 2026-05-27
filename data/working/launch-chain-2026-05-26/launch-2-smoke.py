#!/usr/bin/env python3
"""LAUNCH-2 smoke tests: HTTP, content markers, no Avada leakage, JSON-LD,
LEAD-HIGH-2 anchor, redirects, favicon CDN, og:image."""
from __future__ import annotations
import json, os, re, sys, urllib.request, urllib.error
from pathlib import Path

LIVE_HOST = "https://www.brantbusinessinteriors.com"
TOKEN = os.environ["SHOPIFY_TOKEN"]
RESULTS = {"smoke": {}, "lead_high_2": {}, "redirects": {}, "favicon": {}, "og_image": {}, "live_sanity": {}}


def fetch(url, follow=True):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 LAUNCH-2/1.0"})
    if not follow:
        # Use OpenerDirector that doesn't follow redirects
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        opener = urllib.request.build_opener(NoRedirect)
        try:
            return opener.open(req, timeout=30)
        except urllib.error.HTTPError as e:
            return e
    try:
        return urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        return e


def head(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 LAUNCH-2/1.0"})
    try:
        return urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        return e


# B. Smoke test 5 LIVE URLs
print("\n=== B. Smoke test 5 LIVE URLs ===")
pages = [
    ("/",                    ["Brant", "bbi-header", "Request a Quote"], ["primary-header-blocks", "nav-menu-link"]),
    ("/pages/about",         ["Brant", "bbi-header"], ["primary-header-blocks"]),
    ("/pages/oecm",          ["OECM", "Agreement 2025-470", "bbi-header"], ["primary-header-blocks"]),
    ("/collections/seating", ["seating", "bbi-header"], ["primary-header-blocks"]),
    ("/pages/quote",         ["Request a Quote", "bbi-quote", "bbi-header"], ["primary-header-blocks"]),
]
for path, must_have, must_not_have in pages:
    url = LIVE_HOST + path
    try:
        resp = fetch(url)
        body = resp.read().decode("utf-8", errors="replace")
        status = resp.status
        hits = [m for m in must_have if m.lower() in body.lower()]
        avada_leak = [m for m in must_not_have if m.lower() in body.lower()]
        jsonld = bool(re.search(r'<script[^>]*type="application/ld\+json"', body))
        liquid_err = "Liquid error" in body
        ok = status == 200 and len(hits) == len(must_have) and not avada_leak and jsonld and not liquid_err
        RESULTS["smoke"][path] = {
            "status": status, "bytes": len(body),
            "markers_hit": hits, "avada_leak": avada_leak,
            "jsonld": jsonld, "liquid_err": liquid_err, "pass": ok,
        }
        sym = "✓" if ok else "✗"
        print(f"  {sym} {path:25s} HTTP {status}  {len(body)//1024:4d}KB  markers={len(hits)}/{len(must_have)}  avada={len(avada_leak)}  jsonld={jsonld}  liquid_err={liquid_err}")
    except Exception as e:
        RESULTS["smoke"][path] = {"error": str(e), "pass": False}
        print(f"  ✗ {path}: {e}")

# C. LEAD-HIGH-2: anchor href fallback on homepage CTA
print("\n=== C. LEAD-HIGH-2 anchor fallback ===")
body = fetch(LIVE_HOST + "/").read().decode("utf-8", errors="replace")
# Look for <a ... href="/pages/quote" ... class="...bbi-btn...primary">
m = re.findall(r'<a[^>]*\bhref="/pages/quote"[^>]*\bclass="[^"]*bbi-btn[^"]*--primary[^"]*"', body, re.I)
m2 = re.findall(r'<a[^>]*\bclass="[^"]*bbi-btn[^"]*--primary[^"]*"[^>]*\bhref="/pages/quote"', body, re.I)
quote_anchor_present = len(m) + len(m2)
quote_resp = fetch(LIVE_HOST + "/pages/quote")
RESULTS["lead_high_2"] = {
    "quote_anchor_count": quote_anchor_present,
    "quote_page_status": quote_resp.status,
}
sym = "✓" if quote_anchor_present >= 1 and quote_resp.status == 200 else "✗"
print(f"  {sym} primary-CTA anchor → /pages/quote: {quote_anchor_present} matches; /pages/quote HTTP {quote_resp.status}")

# D. Test redirects
print("\n=== D. Redirects ===")
redirects = [
    ("/pages/ergocentric", "/pages/brands-ergocentric"),
    ("/pages/how-to-adjust-my-new-chair", "/pages/brands-ergocentric"),
]
for src, expected in redirects:
    resp = fetch(LIVE_HOST + src, follow=False)
    status = resp.status
    loc = resp.headers.get("Location", "")
    ok = status in (301, 302) and expected in loc
    RESULTS["redirects"][src] = {"status": status, "location": loc, "expected": expected, "pass": ok}
    sym = "✓" if ok else "✗"
    print(f"  {sym} {src:40s} → HTTP {status} Location={loc}")

# E. Favicon CDN HEAD checks
print("\n=== E. Favicon CDN accessibility ===")
# Pull the rendered head to find the link URLs
body_home = body  # already have homepage
fav_links = re.findall(r'<link[^>]*rel="(icon|apple-touch-icon|manifest)"[^>]*href="([^"]+)"', body_home, re.I)
also_links = re.findall(r'<link[^>]*href="([^"]+)"[^>]*rel="(icon|apple-touch-icon|manifest)"', body_home, re.I)
# Normalize to (rel, href)
fav_urls = [(r, h) for r, h in fav_links] + [(r, h) for h, r in also_links]
seen = set()
fav_unique = []
for r, h in fav_urls:
    if h not in seen:
        seen.add(h); fav_unique.append((r, h))
print(f"  found {len(fav_unique)} favicon-class link tags")
for rel, href in fav_unique:
    try:
        r = head(href)
        ct = r.headers.get("Content-Type", "")
        cl = r.headers.get("Content-Length", "?")
        ok = r.status == 200
        RESULTS["favicon"][href] = {"rel": rel, "status": r.status, "content_type": ct, "content_length": cl}
        sym = "✓" if ok else "✗"
        print(f"  {sym} rel={rel:18s} HTTP {r.status}  {ct:35s}  {cl}B  {href[:80]}")
    except Exception as e:
        RESULTS["favicon"][href] = {"rel": rel, "error": str(e)}
        print(f"  ✗ {href}: {e}")

# F. og:image references og-preview.png
print("\n=== F. og:image meta ===")
og = re.findall(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', body_home, re.I)
og += re.findall(r'<meta[^>]*content="([^"]+)"[^>]*property="og:image"', body_home, re.I)
og = list(dict.fromkeys(og))
print(f"  og:image meta tags: {len(og)}")
for u in og:
    has_preview = "og-preview" in u
    print(f"    {'✓' if has_preview else '✗'} {u}  preview-png={has_preview}")
RESULTS["og_image"] = {"meta_tags": og, "uses_og_preview": any("og-preview" in u for u in og)}

# J. LIVE updated_at unchanged since LAUNCH-1
print("\n=== J. LIVE updated_at sanity ===")
import urllib.parse
STORE = "office-central-online.myshopify.com"
req = urllib.request.Request(
    f"https://{STORE}/admin/api/2026-04/themes/186373570873.json",
    headers={"X-Shopify-Access-Token": TOKEN})
t = json.loads(urllib.request.urlopen(req).read())["theme"]
LAUNCH_1_TS = "2026-05-26T20:08:47-04:00"
unchanged = t["updated_at"] == LAUNCH_1_TS
RESULTS["live_sanity"] = {"current": t["updated_at"], "launch1_ts": LAUNCH_1_TS, "unchanged": unchanged}
sym = "✓" if unchanged else "✗"
print(f"  {sym} LIVE updated_at: {t['updated_at']}  (launch-1 stamp: {LAUNCH_1_TS}  unchanged={unchanged})")

# Save
Path(__file__).parent.joinpath("launch-2-smoke.json").write_text(json.dumps(RESULTS, indent=2))
print(f"\n→ launch-2-smoke.json")
