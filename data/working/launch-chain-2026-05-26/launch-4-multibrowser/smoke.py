"""LAUNCH-4 Phase A — Multi-browser smoke (Chromium + WebKit × 6 viewports × 5 URLs).

Read-only. Captures per-cell:
  HTTP 200, title contains Brant/BBI, body > 10kb,
  console errors, header logo, footer, quote CTA,
  nav (hamburger <1024 / nav links >=1024),
  computed-style spot checks (logo dim, PDP CTA contrast, OECM strip bg).
"""
import asyncio, json, sys, os
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "https://www.brantbusinessinteriors.com"
OUT = Path(__file__).parent
URLS = [
    ("homepage", "/"),
    ("oecm", "/pages/oecm"),
    ("collection-seating", "/collections/seating"),
    ("pdp-boardroom-table", "/products/boardroom-table-rectangular-94-5x47-25"),
    ("quote", "/pages/quote"),
]
# (engine, label, viewport_w, viewport_h, device_scale_factor, is_mobile)
COMBOS = [
    ("chromium", "Chromium 1920x1080", 1920, 1080, 1, False),
    ("chromium", "Chromium 1280x800",  1280, 800,  1, False),
    ("chromium", "Chromium 412x915 (Pixel 7)", 412, 915, 2.625, True),
    ("webkit",   "WebKit 1920x1080",   1920, 1080, 1, False),
    ("webkit",   "WebKit 393x852 (iPhone 14 Pro)", 393, 852, 3, True),
    ("webkit",   "WebKit 768x1024 (iPad Mini)",   768, 1024, 2, True),
]

async def check_cell(browser_type_name, browser, url_label, url_path, label, vw, vh, dsf, is_mobile):
    cell = {
        "engine": browser_type_name, "viewport": label,
        "url_label": url_label, "url_path": url_path,
        "vw": vw, "vh": vh,
        "ok": False, "issues": [], "checks": {},
    }
    ctx = await browser.new_context(
        viewport={"width": vw, "height": vh},
        device_scale_factor=dsf,
        is_mobile=is_mobile,
        has_touch=is_mobile,
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            if is_mobile and browser_type_name == "webkit"
            else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
                 "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        ),
    )
    console_errors = []
    page_errors = []
    page = await ctx.new_page()
    page.on("console", lambda msg: console_errors.append({"type": msg.type, "text": msg.text}) if msg.type == "error" else None)
    page.on("pageerror", lambda err: page_errors.append(str(err)))

    try:
        resp = await page.goto(BASE + url_path, wait_until="networkidle", timeout=45000)
        status = resp.status if resp else 0
        cell["checks"]["http"] = status
        if status != 200:
            cell["issues"].append(f"HTTP {status}")

        title = await page.title()
        cell["checks"]["title"] = title
        if not ("Brant" in title or "BBI" in title):
            cell["issues"].append(f"title missing Brant/BBI: {title!r}")

        body_html = await page.content()
        body_len = len(body_html)
        cell["checks"]["body_len"] = body_len
        if body_len < 10_000:
            cell["issues"].append(f"body_len {body_len} < 10kb")

        # Header logo
        logo = await page.query_selector("header img, .bbi-nav img, .bbi-nav__logo img")
        if logo:
            box = await logo.bounding_box()
            cell["checks"]["logo"] = {"w": box["width"] if box else 0, "h": box["height"] if box else 0} if box else None
            if not box or box["width"] < 10 or box["height"] < 10:
                cell["issues"].append(f"logo 0x0 or hidden: {box}")
        else:
            cell["issues"].append("header logo not found")

        # Footer
        footer = await page.query_selector("footer, .bbi-footer, [data-section-type*='footer']")
        cell["checks"]["footer"] = bool(footer)
        if not footer:
            cell["issues"].append("footer not found")

        # Nav: hamburger if mobile width, nav links if desktop width
        is_narrow = vw < 1024
        if is_narrow:
            hamb = await page.query_selector(".bbi-nav__hamburger, [aria-label*='menu' i], button[aria-controls*='nav' i], .bbi-mobile-nav__toggle, button[class*='hamburger']")
            cell["checks"]["hamburger"] = bool(hamb)
            if not hamb:
                cell["issues"].append("hamburger nav not found on <1024 viewport")
        else:
            nav_links = await page.query_selector_all("header nav a, .bbi-nav__links a, nav.bbi-nav a")
            cell["checks"]["nav_links_count"] = len(nav_links)
            if len(nav_links) < 2:
                cell["issues"].append(f"too few nav links: {len(nav_links)}")

        # Quote CTA
        quote_cta = await page.query_selector(
            "a[href='/pages/quote'], a[href*='quote'], button:has-text('Quote'), a:has-text('Request a Quote')"
        )
        cell["checks"]["quote_cta"] = bool(quote_cta)
        if not quote_cta:
            cell["issues"].append("Request a Quote CTA not found")

        # Computed-style spot checks
        if url_label == "pdp-boardroom-table":
            pdp_btn = await page.query_selector("a.pdp-cta-closer__btn, .pdp-cta-closer__btn")
            if pdp_btn:
                styles = await pdp_btn.evaluate("""el => {
                    const s = getComputedStyle(el);
                    return { color: s.color, bg: s.backgroundColor };
                }""")
                cell["checks"]["pdp_cta_styles"] = styles
                if styles["color"] == styles["bg"]:
                    cell["issues"].append(f"PDP CTA black-on-black regression: {styles}")
            else:
                cell["checks"]["pdp_cta_styles"] = "btn-not-found"

        if url_label == "homepage":
            strip = await page.query_selector(".hp-oecm, section.hp-oecm")
            if strip:
                bg = await strip.evaluate("el => getComputedStyle(el).backgroundColor")
                cell["checks"]["oecm_strip_bg"] = bg
                # Expect rgb(11, 11, 12) or similar dark
                import re
                m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", bg)
                if m:
                    r, g, b = int(m[1]), int(m[2]), int(m[3])
                    brightness = (r + g + b) / 3
                    if brightness > 60:
                        cell["issues"].append(f"OECM strip not dark: {bg}")
                else:
                    cell["issues"].append(f"OECM strip unparsable bg: {bg}")
            else:
                cell["checks"]["oecm_strip_bg"] = "section-not-found"

        cell["checks"]["console_errors"] = console_errors[:5]
        cell["checks"]["page_errors"] = page_errors[:5]
        if console_errors:
            cell["issues"].append(f"{len(console_errors)} console error(s)")
        if page_errors:
            cell["issues"].append(f"{len(page_errors)} page error(s)")

        cell["ok"] = not cell["issues"]

        # Screenshot only on failure
        if not cell["ok"]:
            shot = OUT / f"FAIL-{url_label}-{browser_type_name}-{vw}x{vh}.png"
            try:
                await page.screenshot(path=str(shot), full_page=False)
                cell["screenshot"] = shot.name
            except Exception as e:
                cell["screenshot_err"] = str(e)
    except Exception as e:
        cell["issues"].append(f"exception: {type(e).__name__}: {e}")
    finally:
        await ctx.close()
    return cell

async def main():
    results = []
    async with async_playwright() as p:
        for engine_name in ["chromium", "webkit"]:
            browser = await getattr(p, engine_name).launch()
            engine_combos = [c for c in COMBOS if c[0] == engine_name]
            for (_, label, vw, vh, dsf, is_mobile) in engine_combos:
                for (url_label, url_path) in URLS:
                    print(f"[{engine_name}] {label} :: {url_label} ...", flush=True)
                    cell = await check_cell(engine_name, browser, url_label, url_path, label, vw, vh, dsf, is_mobile)
                    status = "PASS" if cell["ok"] else "FAIL"
                    print(f"   -> {status} {cell['issues'] if cell['issues'] else ''}", flush=True)
                    results.append(cell)
            await browser.close()

    out_file = OUT / "smoke-matrix.json"
    out_file.write_text(json.dumps(results, indent=2))
    n_pass = sum(1 for r in results if r["ok"])
    n_fail = len(results) - n_pass
    print(f"\n=== SUMMARY: {n_pass}/{len(results)} PASS, {n_fail} FAIL ===")
    print(f"Output: {out_file}")
    return 0 if n_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
