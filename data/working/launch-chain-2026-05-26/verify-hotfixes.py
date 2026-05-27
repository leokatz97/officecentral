#!/usr/bin/env python3
"""Post-hotfix verification:
  Fix 1 (logo)     — confirm asset_url for bbi-logo-v2.png resolves on LIVE
  Fix 2 (PDP CTA)  — confirm .pdp-cta-closer__btn renders white on dark
  Fix 3 (OECM strip) — confirm .hp-oecm has ink bg + white text + red dot
"""
from __future__ import annotations
import json, urllib.request, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

LIVE = "https://www.brantbusinessinteriors.com"
PDP = LIVE + "/products/obusforme-comfort-high-back-chair-fabric-1240-3"
HOME = LIVE + "/"
OUT = Path(__file__).parent
UA_IOS = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) "
          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
          "Version/17.4 Mobile/15E148 Safari/604.1")


def main():
    # Fix 1 — HEAD the new asset_url path
    print("=== Fix 1 — bbi-logo-v2.png asset_url HEAD ===")
    # Shopify serves theme assets via /cdn/shop/t/<theme_id>/assets/<key>
    # Easier: just do a HEAD on the public_url we got back from the PUT
    public_url = "https://cdn.shopify.com/s/files/1/0859/0413/0361/t/24/assets/bbi-logo-v2.png?v=1779841962"
    req = urllib.request.Request(public_url, method="HEAD",
                                 headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req, timeout=15)
        print(f"  ✓ HTTP {r.status}  {r.headers.get('Content-Type')}  {r.headers.get('Content-Length','?')}B")
    except Exception as e:
        print(f"  ✗ {e}")

    with sync_playwright() as p:
        for engine_name, engine in [("chromium", p.chromium), ("webkit", p.webkit)]:
            browser = engine.launch()

            # === Fix 2 verification (PDP CTA) ===
            for vp_name, vw, vh, ismob, dpr in [("iphone-se", 375, 667, True, 3),
                                                  ("desktop", 1280, 800, False, 2)]:
                kw = dict(viewport={"width": vw, "height": vh}, device_scale_factor=dpr)
                if ismob:
                    kw.update(is_mobile=True, has_touch=True, user_agent=UA_IOS)
                ctx = browser.new_context(**kw)
                page = ctx.new_page()
                page.goto(PDP, wait_until="networkidle", timeout=60000)
                # Force CSS cache bust if needed (CDN may be stale)
                page.wait_for_timeout(500)
                cta = page.evaluate("""() => {
                  const el = document.querySelector('a.pdp-cta-closer__btn');
                  if (!el) return null;
                  const cs = getComputedStyle(el);
                  const r = el.getBoundingClientRect();
                  return {tag: el.tagName, color: cs.color, bg: cs.backgroundColor,
                          border: cs.borderColor, w: Math.round(r.width), h: Math.round(r.height)};
                }""")
                ok = cta and cta["color"] in ("rgb(255, 255, 255)", "rgba(255, 255, 255, 1)")
                sym = "✓" if ok else "✗"
                print(f"\n=== Fix 2 — {engine_name} {vp_name} — PDP CTA ===")
                print(f"  {sym} {cta}")
                # Screenshot the CTA closer
                try:
                    page.locator(".pdp-cta-closer").first.scroll_into_view_if_needed()
                    page.wait_for_timeout(300)
                    page.locator(".pdp-cta-closer").first.screenshot(
                        path=str(OUT / f"after-fix2-pdp-cta-{engine_name}-{vp_name}.png"))
                except Exception as e:
                    print(f"  screenshot fail: {e}")
                ctx.close()

            # === Fix 3 verification (OECM strip on home) ===
            ctx = browser.new_context(viewport={"width": 1280, "height": 1600})
            page = ctx.new_page()
            page.goto(HOME, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(500)
            oecm = page.evaluate("""() => {
              const sec = document.querySelector('section.hp-oecm');
              if (!sec) return null;
              const copy = sec.querySelector('.hp-oecm__copy');
              const badge = sec.querySelector('.bbi-badge--oecm');
              const dot = badge ? badge.querySelector('.dot') : null;
              const link = sec.querySelector('.bbi-btn--tertiary');
              const csSec = getComputedStyle(sec);
              return {
                section: {bg: csSec.backgroundColor, color: csSec.color,
                          border_top: csSec.borderTopColor},
                copy:   copy   ? {color: getComputedStyle(copy).color} : null,
                badge:  badge  ? {color: getComputedStyle(badge).color, border: getComputedStyle(badge).borderColor} : null,
                dot:    dot    ? {bg: getComputedStyle(dot).backgroundColor} : null,
                link:   link   ? {color: getComputedStyle(link).color} : null,
              };
            }""")
            print(f"\n=== Fix 3 — {engine_name} desktop — OECM strip ===")
            ink_ok = oecm and oecm["section"]["bg"] == "rgb(11, 11, 12)"
            copy_ok = oecm and oecm["copy"] and oecm["copy"]["color"] == "rgb(250, 248, 245)"
            dot_ok = oecm and oecm["dot"] and oecm["dot"]["bg"] == "rgb(212, 37, 42)"
            link_ok = oecm and oecm["link"] and oecm["link"]["color"] == "rgb(250, 248, 245)"
            print(f"  ink bg:    {'✓' if ink_ok else '✗'}  {oecm['section'] if oecm else 'n/a'}")
            print(f"  copy:      {'✓' if copy_ok else '✗'}  {oecm['copy'] if oecm else ''}")
            print(f"  badge:     {oecm['badge'] if oecm else ''}")
            print(f"  red dot:   {'✓' if dot_ok else '✗'}  {oecm['dot'] if oecm else ''}")
            print(f"  link:      {'✓' if link_ok else '✗'}  {oecm['link'] if oecm else ''}")
            try:
                page.locator("section.hp-oecm").first.scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                page.locator("section.hp-oecm").first.screenshot(
                    path=str(OUT / f"after-fix3-oecm-{engine_name}.png"))
            except Exception as e:
                print(f"  screenshot fail: {e}")
            ctx.close()
            browser.close()


if __name__ == "__main__":
    main()
