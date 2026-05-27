#!/usr/bin/env python3
"""Diagnose search-icon strikethrough at mobile + desktop viewports.

Inspects computed style on the search-icon SVG (and ancestors) for
text-decoration, ::before/::after overlays, and verifies whether
both the circle (lens) and path (handle) are rendered.

Outputs JSON + a screenshot of the mobile nav drawer.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

STORE = "office-central-online.myshopify.com"
DEV = 186373570873
URL = f"https://{STORE}/?preview_theme_id={DEV}&_ab=0&_fd=0&_sc=1"

OUT = Path(__file__).parent

DIAG_JS = r"""
() => {
  function chain(el) {
    const arr = [];
    let cur = el;
    while (cur && cur !== document.documentElement) {
      const cs = getComputedStyle(cur);
      const before = getComputedStyle(cur, '::before');
      const after = getComputedStyle(cur, '::after');
      let sel = cur.tagName.toLowerCase();
      if (cur.id) sel += '#' + cur.id;
      if (cur.className && typeof cur.className === 'string') {
        const c = cur.className.trim().split(/\s+/).slice(0, 3).join('.');
        if (c) sel += '.' + c;
      }
      arr.push({
        sel,
        color: cs.color,
        textDecoration: cs.textDecoration,
        textDecorationLine: cs.textDecorationLine,
        textDecorationColor: cs.textDecorationColor,
        textDecorationStyle: cs.textDecorationStyle,
        textDecorationThickness: cs.textDecorationThickness,
        fontStyle: cs.fontStyle,
        position: cs.position,
        // pseudo content
        beforeContent: before.content,
        beforeBg: before.backgroundColor,
        beforeBorder: before.borderTop + ' / ' + before.borderBottom,
        beforeHW: `${before.width}x${before.height}`,
        afterContent: after.content,
        afterBg: after.backgroundColor,
        afterBorder: after.borderTop + ' / ' + after.borderBottom,
        afterHW: `${after.width}x${after.height}`,
      });
      cur = cur.parentElement;
    }
    return arr;
  }

  const result = {};

  // Mobile-nav search submit button + its icon
  const mobBtn = document.querySelector('.bbi-mobile-nav__search-submit');
  const mobSvg = mobBtn ? mobBtn.querySelector('svg') : null;
  const mobCircle = mobBtn ? mobBtn.querySelector('svg circle') : null;
  const mobPath = mobBtn ? mobBtn.querySelector('svg path') : null;

  // Desktop inline search-bar icon
  const deskIconSpan = document.querySelector('.bbi-header__search-icon');
  const deskSvg = deskIconSpan ? deskIconSpan.querySelector('svg') : null;
  const deskCircle = deskIconSpan ? deskIconSpan.querySelector('svg circle') : null;
  const deskPath = deskIconSpan ? deskIconSpan.querySelector('svg path') : null;

  function svgRender(el) {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return {
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      display: cs.display,
      visibility: cs.visibility,
      opacity: cs.opacity,
      stroke: cs.stroke,
      fill: cs.fill,
      color: cs.color,
      textDecoration: cs.textDecoration,
    };
  }

  result.mobile = {
    button_visible: mobBtn ? mobBtn.offsetWidth > 0 : false,
    button_rect: mobBtn ? mobBtn.getBoundingClientRect().toJSON() : null,
    button_chain: mobBtn ? chain(mobBtn) : null,
    svg: svgRender(mobSvg),
    circle: svgRender(mobCircle),
    path: svgRender(mobPath),
  };
  result.desktop = {
    span_visible: deskIconSpan ? deskIconSpan.offsetWidth > 0 : false,
    span_rect: deskIconSpan ? deskIconSpan.getBoundingClientRect().toJSON() : null,
    span_chain: deskIconSpan ? chain(deskIconSpan) : null,
    svg: svgRender(deskSvg),
    circle: svgRender(deskCircle),
    path: svgRender(deskPath),
  };
  return result;
}
"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        diag = {}

        # MOBILE: iPhone SE 375x667 — open hamburger, then inspect
        ctx = browser.new_context(viewport={"width": 375, "height": 667},
                                  is_mobile=True, has_touch=True,
                                  device_scale_factor=2)
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=45000)
        # Find + tap hamburger
        hamburger_selectors = [
            ".bbi-mobile-toggle", ".bbi-hamburger", "button[aria-controls*='mobile']",
            ".bbi-nav__toggle", "[data-mobile-nav-toggle]",
            "button[aria-label*='menu' i]", "button[aria-label*='nav' i]",
        ]
        ham = None
        for sel in hamburger_selectors:
            try:
                el = page.locator(sel).first
                if el.count() > 0 and el.is_visible():
                    ham = (sel, el); break
            except Exception:
                pass
        if ham:
            print(f"mobile: tapping {ham[0]}", file=sys.stderr)
            ham[1].click()
            page.wait_for_timeout(500)
        else:
            print("mobile: hamburger NOT FOUND — proceeding without open drawer", file=sys.stderr)

        diag["mobile_375"] = page.evaluate(DIAG_JS)
        page.screenshot(path=str(OUT / "mobile-search-drawer-open.png"), full_page=False)
        ctx.close()

        # DESKTOP: 1280x800 — inline search bar visible
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=45000)
        diag["desktop_1280"] = page.evaluate(DIAG_JS)
        page.screenshot(path=str(OUT / "desktop-search-bar.png"),
                        clip={"x": 0, "y": 0, "width": 1280, "height": 200})
        ctx.close()

        browser.close()

    out = OUT / "diagnose-search-icon.json"
    out.write_text(json.dumps(diag, indent=2))
    print(f"\nWrote {out}", file=sys.stderr)

    # Pretty-print key findings
    for vp, data in diag.items():
        print(f"\n=== {vp} ===")
        for ctx_name in ("mobile", "desktop"):
            d = data.get(ctx_name, {})
            if not d.get("svg"):
                print(f"  {ctx_name}: not rendered")
                continue
            print(f"  {ctx_name}:")
            print(f"    svg:    {d['svg']}")
            print(f"    circle: {d['circle']}")
            print(f"    path:   {d['path']}")
            chain_key = "button_chain" if ctx_name == "mobile" else "span_chain"
            chain = d.get(chain_key) or []
            print(f"    ancestor text-decoration chain:")
            for level in chain[:6]:
                td = level["textDecorationLine"]
                col = level["textDecorationColor"]
                if td != "none" or level["beforeContent"] != "none" or level["afterContent"] != "none":
                    print(f"      [{level['sel']}] td={td!r} td-color={col} fontStyle={level['fontStyle']}")
                    if level["beforeContent"] != "none":
                        print(f"        ::before content={level['beforeContent']} bg={level['beforeBg']} {level['beforeHW']}")
                    if level["afterContent"] != "none":
                        print(f"        ::after  content={level['afterContent']} bg={level['afterBg']} {level['afterHW']}")
                else:
                    print(f"      [{level['sel']}] (clean)")


if __name__ == "__main__":
    main()
