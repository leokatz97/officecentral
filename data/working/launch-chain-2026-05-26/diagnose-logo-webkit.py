#!/usr/bin/env python3
"""WebKit-engine + iOS Safari UA logo render test on LIVE."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright

LIVE = "https://brantbusinessinteriors.com/"
PDP = "https://brantbusinessinteriors.com/products/obusforme-comfort-high-back-chair-fabric-1240-3"
OUT = Path(__file__).parent
UA_IOS = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) "
          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
          "Version/17.4 Mobile/15E148 Safari/604.1")


def main():
    with sync_playwright() as p:
        for engine_name, engine in [("webkit", p.webkit), ("chromium", p.chromium)]:
            browser = engine.launch()
            for vp_name, vw, vh, ismob, dpr in [
                ("iphone-se", 375, 667, True, 3),
                ("desktop", 1280, 800, False, 2),
            ]:
                kw = dict(viewport={"width": vw, "height": vh}, device_scale_factor=dpr)
                if ismob:
                    kw.update(is_mobile=True, has_touch=True, user_agent=UA_IOS)
                ctx = browser.new_context(**kw)
                page = ctx.new_page()
                resp_log = []
                page.on("response", lambda r: resp_log.append({"url": r.url, "status": r.status, "ct": r.headers.get("content-type", "")}) if "logo" in r.url.lower() else None)
                page.on("requestfailed", lambda r: resp_log.append({"url": r.url, "failure": r.failure}) if "logo" in r.url.lower() else None)

                page.goto(LIVE, wait_until="networkidle", timeout=60000)
                # Force lazy images by scrolling to bottom
                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1500)
                page.evaluate("() => window.scrollTo(0, 0)")
                page.wait_for_timeout(500)
                # Open hamburger if mobile
                if ismob:
                    try:
                        page.locator(".bbi-hamburger").first.click()
                        page.wait_for_timeout(800)
                    except Exception:
                        pass

                logos = page.evaluate("""() => {
                  return Array.from(document.querySelectorAll('img')).filter(img => {
                    const parentCls = img.closest('a,div,header,section')?.className || '';
                    return /logo|brand/i.test(parentCls + ' ' + (img.alt || ''));
                  }).map(img => ({
                    parent_class: img.closest('a,div,header,section')?.className,
                    src: img.src,
                    currentSrc: img.currentSrc,
                    complete: img.complete,
                    naturalW: img.naturalWidth,
                    naturalH: img.naturalHeight,
                    visible: img.getBoundingClientRect().width > 0,
                  }));
                }""")
                print(f"\n=== {engine_name} {vp_name} {vw}x{vh} (UA={'iOS' if ismob else 'default'}) ===")
                for i, img in enumerate(logos):
                    ok = img["complete"] and img["naturalW"] > 0
                    sym = "✓" if ok else "✗ BROKEN"
                    print(f"  {sym} parent={img['parent_class']!r}  natural={img['naturalW']}x{img['naturalH']}  visible={img['visible']}")
                    print(f"      src={img['src']}")

                for r in resp_log:
                    print(f"  [response/fail] {r}")

                # Screenshot the header
                try:
                    page.locator(".bbi-header, header.bbi-header").first.screenshot(
                        path=str(OUT / f"live-header-{engine_name}-{vp_name}.png"))
                except Exception:
                    page.screenshot(path=str(OUT / f"live-page-{engine_name}-{vp_name}.png"),
                                    clip={"x": 0, "y": 0, "width": vw, "height": 150})
                ctx.close()
            browser.close()


if __name__ == "__main__":
    main()
