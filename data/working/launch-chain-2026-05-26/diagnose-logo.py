#!/usr/bin/env python3
"""Phase A diagnostic: render LIVE homepage in headless, see if logo loads."""
from __future__ import annotations
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

LIVE_APEX = "https://brantbusinessinteriors.com/"
LIVE_WWW = "https://www.brantbusinessinteriors.com/"
OUT = Path(__file__).parent


def probe(page, url):
    failed = []
    page.on("requestfailed", lambda r: failed.append({"url": r.url, "failure": r.failure}))
    page.on("response", lambda r: None)
    page.goto(url, wait_until="networkidle", timeout=60000)
    # Inspect every logo img on the page
    result = page.evaluate("""() => {
      const out = [];
      document.querySelectorAll('img').forEach(img => {
        const cls = (img.className || '') + ' ' + (img.closest('a,div,header,section')?.className || '');
        if (/logo|brand/i.test(cls + ' ' + (img.alt || ''))) {
          out.push({
            tag: 'img',
            src: img.src,
            alt: img.alt,
            classes: img.className,
            parent_class: img.closest('a,div,header,section')?.className,
            complete: img.complete,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            displayedWidth: img.width,
            displayedHeight: img.height,
            currentSrc: img.currentSrc,
          });
        }
      });
      return out;
    }""")
    return result, failed


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        for url in (LIVE_APEX, LIVE_WWW):
            print(f"\n=== {url} ===")
            result, failed = probe(page, url)
            for img in result:
                ok = img["complete"] and img["naturalWidth"] > 0
                sym = "✓" if ok else "✗ BROKEN"
                print(f"  {sym} alt={img['alt']!r}")
                print(f"      src={img['src']}")
                print(f"      currentSrc={img['currentSrc']}")
                print(f"      classes={img['classes']!r}  parent={img['parent_class']!r}")
                print(f"      natural={img['naturalWidth']}x{img['naturalHeight']}  displayed={img['displayedWidth']}x{img['displayedHeight']}")
            for f in failed:
                if 'logo' in f['url'].lower():
                    print(f"  REQUEST FAILED: {f}")
            # Screenshot the header
            try:
                page.locator(".bbi-header").first.screenshot(path=str(OUT / f"live-header-{url.split('//')[1].split('/')[0]}.png"))
            except Exception as e:
                print(f"  header screenshot fail: {e}")

        ctx.close(); browser.close()


if __name__ == "__main__":
    main()
