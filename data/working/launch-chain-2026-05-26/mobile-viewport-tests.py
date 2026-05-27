#!/usr/bin/env python3
"""Phase 0.B — mobile breakpoint tests across 5 viewports × 4 pages.

Captures: docOverflow, scrollWidth vs innerWidth, oversized elements,
nav hamburger presence (<1024), desktop nav hidden (<1024), broken images,
tap-target sizes for primary CTAs.

Output: data/working/launch-chain-2026-05-26/mobile-viewport-tests.json
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

STORE = "office-central-online.myshopify.com"
DEV_THEME_ID = 186373570873
PREVIEW_PARAMS = f"preview_theme_id={DEV_THEME_ID}&_ab=0&_fd=0&_sc=1"

VIEWPORTS = [
    ("iPhone SE",     375, 667),
    ("iPhone 14 Pro", 393, 852),
    ("Pixel 7",       412, 915),
    ("iPad Mini P",   768, 1024),
    ("iPad Mini L",   1024, 768),
]
PAGES = ["/", "/pages/about", "/pages/oecm", "/collections/seating"]

UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
      "Version/17.0 Mobile/15E148 Safari/604.1")

MEASURE_JS = r"""
() => {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const docW = document.documentElement.scrollWidth;
  const bodyW = document.body.scrollWidth;
  const docOverflow = Math.max(0, docW - vw);

  // Find every element wider than the viewport
  const oversized = [];
  const all = document.querySelectorAll('*');
  for (const el of all) {
    const r = el.getBoundingClientRect();
    if (r.width > vw + 1) {
      let sel = el.tagName.toLowerCase();
      if (el.id) sel += '#' + el.id;
      else if (el.className && typeof el.className === 'string') {
        const c = el.className.trim().split(/\s+/).slice(0, 2).join('.');
        if (c) sel += '.' + c;
      }
      oversized.push({sel, w: Math.round(r.width)});
      if (oversized.length >= 10) break;
    }
  }

  // Nav state
  const ham = document.querySelector('.bbi-mobile-toggle, .bbi-hamburger, [data-mobile-nav-toggle], button[aria-controls*="mobile"], .bbi-nav__toggle');
  const hamVisible = !!(ham && getComputedStyle(ham).display !== 'none' && ham.offsetWidth > 0);
  const desktopNav = document.querySelector('.bbi-nav, .bbi-header__nav');
  const desktopNavVisible = !!(desktopNav && getComputedStyle(desktopNav).display !== 'none' && desktopNav.offsetWidth > 0);

  // Broken images
  const imgs = Array.from(document.querySelectorAll('img'));
  const broken = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.src);

  // Primary CTAs and tap-target sizes
  const ctaSelectors = [
    'a[href="/pages/quote"]',
    '.bbi-btn',
    '.bbi-btn--primary',
    '.hp-hero__cta-red',
    'a[href*="quote"]',
  ];
  const ctas = [];
  const seen = new Set();
  for (const sel of ctaSelectors) {
    document.querySelectorAll(sel).forEach(el => {
      if (seen.has(el)) return;
      seen.add(el);
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) {
        ctas.push({
          sel,
          w: Math.round(r.width),
          h: Math.round(r.height),
          text: (el.innerText || '').trim().slice(0, 40),
        });
      }
    });
    if (ctas.length >= 10) break;
  }

  return {
    vw, vh, docW, bodyW, docOverflow,
    oversized,
    hamVisible, desktopNavVisible,
    imgCount: imgs.length, broken,
    ctas,
    title: document.title,
    h1: (document.querySelector('h1') || {}).innerText || '',
  };
}
"""


def main():
    results = {"meta": {"theme_id": DEV_THEME_ID, "ts": int(time.time())}, "tests": []}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vname, vw, vh in VIEWPORTS:
            ctx = browser.new_context(
                viewport={"width": vw, "height": vh},
                user_agent=UA,
                device_scale_factor=2,
                is_mobile=vw < 768,
                has_touch=True,
            )
            page = ctx.new_page()
            # Prime the cookie via homepage hit
            print(f"[{vname} {vw}x{vh}] priming cookie...", file=sys.stderr)
            page.goto(f"https://{STORE}/?{PREVIEW_PARAMS}", wait_until="domcontentloaded", timeout=45000)
            for path in PAGES:
                url = f"https://{STORE}{path}?{PREVIEW_PARAMS}"
                print(f"[{vname} {vw}x{vh}] {path}", file=sys.stderr)
                try:
                    resp = page.goto(url, wait_until="networkidle", timeout=60000)
                    status = resp.status if resp else 0
                    page.wait_for_timeout(500)
                    measure = page.evaluate(MEASURE_JS)
                except Exception as e:
                    results["tests"].append({
                        "viewport": vname, "vw": vw, "vh": vh, "path": path,
                        "status": -1, "error": str(e),
                    })
                    continue
                # Expected nav state
                expect_ham = vw < 1024
                ham_ok = measure["hamVisible"] == expect_ham
                desktop_nav_ok = measure["desktopNavVisible"] != expect_ham
                # Tap target check: any CTA <44px
                tap_fail = [c for c in measure["ctas"] if min(c["w"], c["h"]) < 44]
                # docOverflow allowed ≤1px (subpixel rounding)
                overflow_ok = measure["docOverflow"] <= 1
                no_oversized = len(measure["oversized"]) == 0
                no_broken = len(measure["broken"]) == 0

                passed = overflow_ok and no_broken and ham_ok and no_oversized
                results["tests"].append({
                    "viewport": vname, "vw": vw, "vh": vh, "path": path,
                    "status": status,
                    "title": measure["title"],
                    "h1": measure["h1"],
                    "docOverflow": measure["docOverflow"],
                    "scrollWidth": measure["docW"],
                    "innerWidth": measure["vw"],
                    "oversized": measure["oversized"],
                    "hamVisible": measure["hamVisible"],
                    "desktopNavVisible": measure["desktopNavVisible"],
                    "expect_ham": expect_ham,
                    "ham_ok": ham_ok,
                    "desktop_nav_ok": desktop_nav_ok,
                    "img_count": measure["imgCount"],
                    "broken": measure["broken"],
                    "ctas": measure["ctas"],
                    "tap_fail": tap_fail,
                    "overflow_ok": overflow_ok,
                    "pass": passed,
                })
            ctx.close()
        browser.close()

    out = Path(__file__).parent / "mobile-viewport-tests.json"
    out.write_text(json.dumps(results, indent=2))
    n = len(results["tests"])
    passed = sum(1 for t in results["tests"] if t.get("pass"))
    print(f"\n=== {passed}/{n} pass ===")
    if passed < n:
        for t in results["tests"]:
            if not t.get("pass"):
                print(f"FAIL {t['viewport']} {t['path']}: "
                      f"overflow={t.get('docOverflow')} "
                      f"ham_ok={t.get('ham_ok')} "
                      f"oversized={len(t.get('oversized', []))} "
                      f"broken={len(t.get('broken', []))} "
                      f"tap_fail={len(t.get('tap_fail', []))}")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
