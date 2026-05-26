#!/usr/bin/env python3
"""bbi-preview-dev.py — Open the BBI dev theme preview reliably.

Dev theme:  186373570873  (BBI Landing Dev)
Live theme: 178274435385  (DO NOT TOUCH)

WHY THE OBVIOUS URL FAILS
-------------------------
The naive `https://office-central-online.myshopify.com/?preview_theme_id=<id>`
URL gets 301-redirected to the custom domain (brantbusinessinteriors.com)
because the primary domain is set there. That redirect STRIPS the
`preview_theme_id` query param, so the second hop lands on the live site.

WHY THIS WORKS
--------------
Adding `_ab=0&_fd=0&_sc=1` tells Shopify to stay on the canonical
myshopify.com host instead of bouncing to the custom domain:
  * _ab=0  → suppress A/B redirect to primary domain
  * _fd=0  → forwarding disabled
  * _sc=1  → storefront context (set preview cookie)

The first request 302s back to the myshopify.com root and issues a
`_shopify_essential` cookie that encodes the preview-theme state. As long
as the cookie travels with the redirect (browsers do this automatically
for same-host redirects), every subsequent request renders the dev theme.
The `preview_theme_id` query param is stripped from the URL after the
first hop — preview state lives in the cookie from that point on.

USAGE
-----
  ./scripts/bbi-preview-dev.py                  open homepage in browser
  ./scripts/bbi-preview-dev.py --path /collections/desks
  ./scripts/bbi-preview-dev.py --verify         curl-check dev markers
  ./scripts/bbi-preview-dev.py --print-only     print URL, do not open
"""

from __future__ import annotations

import argparse
import http.cookiejar
import re
import subprocess
import sys
import urllib.parse
import urllib.request

STORE = "office-central-online.myshopify.com"
DEV_THEME_ID = 186373570873
LIVE_THEME_ID = 178274435385  # never push here
PREVIEW_PARAMS = "_ab=0&_fd=0&_sc=1"


def build_url(path: str = "/") -> str:
    if not path.startswith("/"):
        path = "/" + path
    return (
        f"https://{STORE}{path}"
        f"?preview_theme_id={DEV_THEME_ID}&{PREVIEW_PARAMS}"
    )


def verify(path: str = "/") -> int:
    """Follow the redirect with a cookie jar and confirm dev-theme signals."""
    url = build_url(path)
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
        ("User-Agent", "bbi-preview-dev/1.0 (verification)"),
        ("Accept", "text/html"),
    ]
    print(f"GET {url}")
    with opener.open(url, timeout=30) as resp:
        final_url = resp.geturl()
        body = resp.read().decode("utf-8", errors="replace")
        status = resp.status
    print(f"→ final URL: {final_url}")
    print(f"→ status:    {status}")
    print(f"→ size:      {len(body):,} bytes")

    theme_paths = sorted(set(re.findall(r"/cdn/shop/t/(\d+)/", body)))
    hp_hero = body.count("hp-hero__title")
    logo_width = "logoWidth" in body

    print(f"→ asset theme numbers in body: {theme_paths or '(none found)'}")
    print(f"→ hp-hero__title occurrences:  {hp_hero}")
    print(f"→ logoWidth present:           {logo_width}")

    # hp-hero__title is the strongest signal: it only exists in the dev
    # theme's templates/index.json + assets/bbi-homepage.css.
    # logoWidth is in sections/header.liquid; the homepage layout doesn't
    # render the header section group, so it's expected to be absent there.
    ok = hp_hero > 0 or logo_width
    if not ok:
        print("FAIL: no dev-theme markers found.", file=sys.stderr)
        return 1
    print("OK: dev theme is being rendered.")
    return 0


def open_in_browser(url: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", url], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", url], check=False)
    else:
        subprocess.run(["python3", "-m", "webbrowser", url], check=False)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--path", default="/", help="Storefront path to preview (default: /)")
    p.add_argument("--verify", action="store_true", help="Curl the URL and check for dev-theme markers")
    p.add_argument("--print-only", action="store_true", help="Print the URL but do not open a browser")
    args = p.parse_args()

    if args.verify:
        return verify(args.path)

    url = build_url(args.path)
    print(url)
    if not args.print_only:
        open_in_browser(url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
