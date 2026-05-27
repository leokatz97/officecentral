#!/usr/bin/env python3
"""Phase Z diagnostic: inspect .pdp-cta-closer__btn computed style on LIVE PDP
+ check all 8 LEAD-HIGH-2 anchor-converted buttons across multiple pages."""
from __future__ import annotations
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

LIVE = "https://www.brantbusinessinteriors.com"
PDP = LIVE + "/products/obusforme-comfort-high-back-chair-fabric-1240-3"
HOME = LIVE + "/"
BLOG = LIVE + "/blogs/news"
P404 = LIVE + "/intentionally-missing-page-for-test-12345"
QUOTE = LIVE + "/pages/quote"
COLLECTION = LIVE + "/collections/seating"
DESIGN = LIVE + "/pages/design-services"

OUT = Path(__file__).parent


def inspect(page, selectors):
    """Return computed-style snapshot for each selector found on the page."""
    return page.evaluate("""(sels) => {
      const out = {};
      function rgbToOpaque(rgb) { return rgb; }
      sels.forEach(sel => {
        const els = Array.from(document.querySelectorAll(sel));
        if (els.length === 0) { out[sel] = {found: 0}; return; }
        const results = els.slice(0, 3).map(el => {
          const cs = getComputedStyle(el);
          const r = el.getBoundingClientRect();
          // Get the highest-specificity selectors hitting color
          return {
            tagName: el.tagName.toLowerCase(),
            classes: el.className,
            href: el.getAttribute('href'),
            text: (el.innerText || '').trim().slice(0, 40),
            visible: r.width > 0 && r.height > 0,
            color: cs.color,
            backgroundColor: cs.backgroundColor,
            borderColor: cs.borderColor,
            background: cs.background.slice(0, 200),
            display: cs.display,
            textDecoration: cs.textDecorationLine,
            w: Math.round(r.width), h: Math.round(r.height),
          };
        });
        out[sel] = {found: els.length, samples: results};
      });
      return out;
    }""", selectors)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()

        results = {}

        # === PDP ===
        print(f"\n=== PDP: {PDP} ===", file=sys.stderr)
        page.goto(PDP, wait_until="networkidle", timeout=60000)
        results["pdp"] = inspect(page, [
            ".pdp-cta-closer__btn",
            ".pdp-btn--quote-outline",
            ".pdp-cta-closer__btn[href]",
            "a.pdp-cta-closer__btn",
        ])
        # Screenshot the CTA closer area
        try:
            page.locator(".pdp-cta-closer").first.scroll_into_view_if_needed()
            page.wait_for_timeout(400)
            page.locator(".pdp-cta-closer").first.screenshot(path=str(OUT / "live-pdp-cta-closer.png"))
        except Exception as e:
            print(f"screenshot fail: {e}", file=sys.stderr)
        try:
            page.locator(".pdp-quote-strip").first.scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            page.locator(".pdp-quote-strip").first.screenshot(path=str(OUT / "live-pdp-quote-strip.png"))
        except Exception as e:
            print(f"quote-strip screenshot fail: {e}", file=sys.stderr)

        # === HOMEPAGE ===
        print(f"\n=== HOME ===", file=sys.stderr)
        page.goto(HOME, wait_until="networkidle", timeout=60000)
        results["home"] = inspect(page, [
            ".bbi-btn--primary[href='/pages/quote']",
            "a.bbi-btn--primary",
        ])

        # === COLLECTION (for sticky bar bbi-btn--primary) ===
        print(f"=== COLLECTION ===", file=sys.stderr)
        page.goto(COLLECTION, wait_until="networkidle", timeout=60000)
        results["collection"] = inspect(page, [
            "a.bbi-btn--primary",
            ".bbi-btn--primary[href='/pages/quote']",
        ])

        # === BLOG LIST ===
        print(f"=== BLOG ===", file=sys.stderr)
        try:
            page.goto(BLOG, wait_until="networkidle", timeout=60000)
            results["blog"] = inspect(page, [
                ".blog-cta__btn",
                "a.blog-cta__btn",
            ])
        except Exception as e:
            results["blog"] = {"error": str(e)}

        # === 404 ===
        print(f"=== 404 ===", file=sys.stderr)
        page.goto(P404, wait_until="networkidle", timeout=60000)
        results["s404"] = inspect(page, [
            ".s404-btn--primary",
            "a.s404-btn--primary",
        ])

        # === DESIGN SERVICES ===
        print(f"=== DESIGN ===", file=sys.stderr)
        try:
            page.goto(DESIGN, wait_until="networkidle", timeout=60000)
            results["design"] = inspect(page, [
                "a.bbi-btn--primary[href='/pages/quote']",
                "a.bbi-btn--primary",
            ])
        except Exception as e:
            results["design"] = {"error": str(e)}

        # === MOBILE drawer button on homepage (need to open hamburger at mobile viewport) ===
        ctx.close()
        ctx = browser.new_context(viewport={"width": 375, "height": 667},
                                  is_mobile=True, has_touch=True, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(HOME, wait_until="networkidle", timeout=60000)
        for sel in [".bbi-hamburger", ".bbi-mobile-toggle"]:
            try:
                if page.locator(sel).first.count() > 0:
                    page.locator(sel).first.click()
                    page.wait_for_timeout(400)
                    break
            except Exception:
                pass
        results["mobile_drawer"] = inspect(page, [
            ".bbi-mobile-nav__quote",
            "a.bbi-mobile-nav__quote",
        ])

        ctx.close()
        browser.close()

    OUT.joinpath("diagnose-pdp-cta.json").write_text(json.dumps(results, indent=2))

    # Pretty-print key findings
    print("\n" + "=" * 70)
    print("FINDINGS (computed style on LIVE):")
    print("=" * 70)
    for pname, sels in results.items():
        if isinstance(sels, dict) and "error" in sels:
            print(f"\n[{pname}] ERROR: {sels['error']}")
            continue
        print(f"\n[{pname}]")
        for sel, data in sels.items():
            n = data.get("found", 0)
            if n == 0:
                continue
            for i, s in enumerate(data.get("samples", []), 1):
                if not s["visible"]:
                    print(f"  {sel}[{i}/{n}] {s['tagName']}.{s['classes'][:50]} — NOT VISIBLE")
                    continue
                broken = "❌ BROKEN" if (
                    s["color"] in ("rgb(0, 0, 0)", "rgba(0, 0, 0, 1)") and
                    s["backgroundColor"] in ("rgb(0, 0, 0)", "rgba(0, 0, 0, 1)", "rgba(11, 11, 12, 1)", "rgb(11, 11, 12)")
                ) else "✓ ok"
                print(f"  {sel}[{i}/{n}] {s['tagName']}  text={s['text']!r}  {broken}")
                print(f"      color={s['color']}  bg={s['backgroundColor']}  border={s['borderColor']}  size={s['w']}x{s['h']}")


if __name__ == "__main__":
    main()
