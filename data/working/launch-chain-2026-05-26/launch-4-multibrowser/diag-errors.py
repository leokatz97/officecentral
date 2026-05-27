"""Identify the recurring 401 + PDP 404s + PDP JS error."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "https://www.brantbusinessinteriors.com"
URLS = [
    ("homepage", "/"),
    ("pdp", "/products/boardroom-table-rectangular-94-5x47-25"),
]
OUT = Path(__file__).parent

async def run():
    out = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for label, path in URLS:
            ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
            page = await ctx.new_page()
            requests = []
            console = []
            errors = []
            page.on("response", lambda r: requests.append({"url": r.url, "status": r.status, "type": r.request.resource_type}))
            page.on("console", lambda m: console.append({"type": m.type, "text": m.text, "location": str(m.location)}) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append({"msg": str(e), "stack": getattr(e, 'stack', '')}))
            await page.goto(BASE + path, wait_until="networkidle", timeout=45000)
            non200 = [r for r in requests if r["status"] >= 400]
            out[label] = {
                "non200_resources": non200,
                "console_errors": console,
                "page_errors": errors,
            }
            await ctx.close()
        await browser.close()
    OUT.joinpath("diag-errors.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

asyncio.run(run())
