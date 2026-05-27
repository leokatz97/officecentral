#!/usr/bin/env python3
"""High-DPR screenshot of just the search-icon area at mobile + desktop,
plus a Safari-flavored UA test to see if native search-field decorations
are showing."""
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


def main():
    with sync_playwright() as p:
        browser = p.webkit.launch()  # WebKit for closest-to-iOS rendering

        # Mobile at iPhone SE 375x667 with DPR=3 + iOS Safari UA
        ctx = browser.new_context(
            viewport={"width": 375, "height": 667},
            device_scale_factor=3,
            is_mobile=True, has_touch=True,
            user_agent=UA_IOS,
        )
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=45000)

        # Open hamburger
        for sel in [".bbi-hamburger", ".bbi-mobile-toggle",
                    "button[aria-label*='menu' i]"]:
            try:
                if page.locator(sel).first.count() > 0:
                    page.locator(sel).first.click()
                    page.wait_for_timeout(500)
                    break
            except Exception:
                pass

        # Find the mobile search submit button + screenshot it directly
        btn = page.locator(".bbi-mobile-nav__search-submit").first
        btn.screenshot(path=str(OUT / "mobile-search-icon-webkit-zoom.png"))
        # Also screenshot the whole search row
        page.locator(".bbi-mobile-nav__search-row").first.screenshot(
            path=str(OUT / "mobile-search-row-webkit.png"))

        # Get bounding box info
        bb_btn = btn.bounding_box()
        bb_input = page.locator(".bbi-mobile-nav__search-input").first.bounding_box()
        bb_form = page.locator(".bbi-mobile-nav__search-form").first.bounding_box()
        print(f"WebKit/iOS-Safari mobile:")
        print(f"  form rect:  {bb_form}")
        print(f"  input rect: {bb_input}")
        print(f"  button rect: {bb_btn}")

        # Look for any rendered webkit search decoration
        decor = page.evaluate("""() => {
          const input = document.querySelector('.bbi-mobile-nav__search-input');
          if (!input) return null;
          const cs = getComputedStyle(input);
          // Probe for the webkit search decoration
          let dec = null, cancel = null;
          try { dec = getComputedStyle(input, '::-webkit-search-decoration'); } catch(e) {}
          try { cancel = getComputedStyle(input, '::-webkit-search-cancel-button'); } catch(e) {}
          return {
            webkitAppearance: cs.webkitAppearance || cs.appearance,
            paddingLeft: cs.paddingLeft,
            backgroundImage: cs.backgroundImage,
            decoration_display: dec ? dec.display : null,
            cancel_display: cancel ? cancel.display : null,
          };
        }""")
        print(f"  input webkit-decoration:", decor)
        ctx.close()

        # DESKTOP at 1280
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=UA_IOS.replace("iPhone; CPU iPhone OS 17_4 like Mac OS X",
                                      "Macintosh; Intel Mac OS X 10_15_7")
                              .replace("Mobile/15E148", "")
        )
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=45000)
        page.locator(".bbi-header__search-bar").first.screenshot(
            path=str(OUT / "desktop-search-bar-webkit.png"))
        ctx.close()

        browser.close()
    print(f"\nScreenshots in {OUT}")


if __name__ == "__main__":
    main()
