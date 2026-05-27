#!/usr/bin/env python3
"""Post-fix verification: render the magnifying-glass icon at 4 viewports
in WebKit (iOS-Safari proxy), screenshot the icon area, confirm path data
in DOM matches new geometry."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright

STORE = "office-central-online.myshopify.com"
DEV = 186373570873
URL = f"https://{STORE}/?preview_theme_id={DEV}&_ab=0&_fd=0&_sc=1"
OUT = Path(__file__).parent

UA_IOS = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) "
          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
          "Version/17.4 Mobile/15E148 Safari/604.1")

VIEWPORTS = [
    ("iphone-se",   375,  667, True,  3),
    ("pixel-7",     412,  915, True,  3),
    ("ipad-mini",   768, 1024, True,  2),
    ("desktop",    1280,  800, False, 2),
]


def main():
    with sync_playwright() as p:
        for engine_name, engine in [("webkit", "webkit"), ("chromium", "chromium")]:
            browser = getattr(p, engine).launch()
            for vname, vw, vh, is_mob, dpr in VIEWPORTS:
                ctx_kw = dict(viewport={"width": vw, "height": vh}, device_scale_factor=dpr)
                if is_mob:
                    ctx_kw.update(is_mobile=True, has_touch=True, user_agent=UA_IOS)
                ctx = browser.new_context(**ctx_kw)
                page = ctx.new_page()
                page.goto(URL, wait_until="networkidle", timeout=45000)

                # Locate the right icon
                if vw < 1024:
                    # Open hamburger first
                    for sel in [".bbi-hamburger", ".bbi-mobile-toggle"]:
                        try:
                            if page.locator(sel).first.count() > 0:
                                page.locator(sel).first.click()
                                page.wait_for_timeout(400)
                                break
                        except Exception:
                            pass
                    icon_sel = ".bbi-mobile-nav__search-submit"
                else:
                    icon_sel = ".bbi-header__search-icon"

                # Confirm path d= in DOM
                path_d = page.evaluate(f"""() => {{
                  const el = document.querySelector('{icon_sel} svg path');
                  return el ? el.getAttribute('d') : null;
                }}""")

                shot = OUT / f"verify-{engine_name}-{vname}-icon.png"
                page.locator(icon_sel).first.screenshot(path=str(shot))
                print(f"  {engine_name:8s} {vname:10s} {vw}x{vh} dpr={dpr}  path d={path_d!r}  → {shot.name}")
                ctx.close()
            browser.close()


if __name__ == "__main__":
    main()
