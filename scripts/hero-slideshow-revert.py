#!/usr/bin/env python3
"""
HOMEPAGE-HERO-SLIDESHOW-1 — REVERT.

Restores templates/index.json + bbi-homepage.css from the pre-slideshow backup,
then swaps the bbi-hp-ph hero placeholder for a real <img> of the office photo
(already in Shopify Files from the slideshow upload). Pushes both to DEV.

DEV-only. Idempotent: re-running produces same end state.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_JSON = ROOT / "theme" / "templates" / "index.json"
CSS_FILE = ROOT / "theme" / "assets" / "bbi-homepage.css"
BACKUP_DIR = ROOT / "data" / "backups" / "hero-slideshow-v2-pre-20260525-232746"

STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
DEV_THEME_ID = "186373570873"
LIVE_THEME_ID = "178274435385"
RATE_LIMIT_SEC = 0.5

OFFICE_CDN = "https://cdn.shopify.com/s/files/1/0859/0413/0361/files/hp-hero-slide-1-office.jpg?v=1779765474"

OLD_PLACEHOLDER = '<div class="bbi-hp-ph bbi-hp-ph--hero" role="img" aria-label="Executive office installation by Brant Business Interiors, Peterborough Ontario"></div>'

NEW_IMG = (
    '<img src="' + OFFICE_CDN + '"\n'
    '             alt="Executive office installation by Brant Business Interiors, Peterborough Ontario"\n'
    '             fetchpriority="high"\n'
    '             loading="eager"\n'
    '             decoding="async"\n'
    '             width="1920"\n'
    '             height="1080">'
)

TOKEN = os.environ.get("SHOPIFY_TOKEN")
if not TOKEN:
    print("ERROR: SHOPIFY_TOKEN not set", file=sys.stderr); sys.exit(1)


def api_get(path):
    req = urllib.request.Request(
        f"https://{STORE}/admin/api/{API_VERSION}/{path}",
        headers={"X-Shopify-Access-Token": TOKEN},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def api_put(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://{STORE}/admin/api/{API_VERSION}/{path}",
        data=body, method="PUT",
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} on PUT {path}: {body[:500]}")
    finally:
        time.sleep(RATE_LIMIT_SEC)


def main():
    # ── Guards ────────────────────────────────────────────────────────
    print(f"DEV target → {DEV_THEME_ID}")
    t = api_get(f"themes/{DEV_THEME_ID}.json")["theme"]
    assert t["role"] != "main", f"REFUSE: theme {DEV_THEME_ID} role=main"
    print(f"  name={t['name']}  role={t['role']}  ✓ unpublished")
    live = api_get(f"themes/{LIVE_THEME_ID}.json")["theme"]
    expected_live = "2026-05-16T16:47:22-04:00"
    assert live["updated_at"] == expected_live, \
        f"LIVE baseline mismatch: {live['updated_at']} != {expected_live}"
    print(f"  LIVE updated_at OK ({live['updated_at']})")

    # ── Step 1: Restore index.json from backup, then swap placeholder ─
    print(f"\n[1/4] Restoring {INDEX_JSON.relative_to(ROOT)} from backup")
    backup_index_text = (BACKUP_DIR / "index.json").read_text(encoding="utf-8")
    backup_index = json.loads(backup_index_text)
    hero_setting = backup_index["sections"]["bbi-hero"]["settings"]["custom_liquid"]
    assert OLD_PLACEHOLDER in hero_setting, \
        "backup hero block doesn't contain expected placeholder div"
    swapped = hero_setting.replace(OLD_PLACEHOLDER, NEW_IMG)
    backup_index["sections"]["bbi-hero"]["settings"]["custom_liquid"] = swapped
    with open(INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(backup_index, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"      Restored + swapped bbi-hp-ph → <img src=...office.jpg>")

    # ── Step 2: Restore bbi-homepage.css from backup ──────────────────
    print(f"\n[2/4] Restoring {CSS_FILE.relative_to(ROOT)} from backup")
    backup_css = (BACKUP_DIR / "bbi-homepage.css").read_text(encoding="utf-8")
    CSS_FILE.write_text(backup_css, encoding="utf-8")
    assert "HOMEPAGE HERO CAROUSEL — 2026-05-26" not in CSS_FILE.read_text(encoding="utf-8"), \
        "carousel CSS marker still present after restore"
    print(f"      Restored ({len(backup_css)} chars); carousel CSS removed")

    # ── Step 3: Push templates/index.json to DEV ──────────────────────
    print(f"\n[3/4] PUT theme {DEV_THEME_ID} ← templates/index.json")
    status, resp = api_put(
        f"themes/{DEV_THEME_ID}/assets.json",
        {"asset": {"key": "templates/index.json",
                   "value": INDEX_JSON.read_text(encoding="utf-8")}},
    )
    asset = resp["asset"]
    print(f"      HTTP {status} · size={asset.get('size')} · updated_at={asset.get('updated_at')}")

    # ── Step 4: Push assets/bbi-homepage.css to DEV ───────────────────
    print(f"\n[4/4] PUT theme {DEV_THEME_ID} ← assets/bbi-homepage.css")
    status, resp = api_put(
        f"themes/{DEV_THEME_ID}/assets.json",
        {"asset": {"key": "assets/bbi-homepage.css",
                   "value": CSS_FILE.read_text(encoding="utf-8")}},
    )
    asset = resp["asset"]
    print(f"      HTTP {status} · size={asset.get('size')} · updated_at={asset.get('updated_at')}")

    # ── Verify by re-fetching ─────────────────────────────────────────
    print(f"\nVerifying via re-fetch...")
    r1 = api_get(f"themes/{DEV_THEME_ID}/assets.json?asset[key]=templates/index.json")
    fetched_hero = json.loads(r1["asset"]["value"])["sections"]["bbi-hero"]["settings"]["custom_liquid"]
    r2 = api_get(f"themes/{DEV_THEME_ID}/assets.json?asset[key]=assets/bbi-homepage.css")
    fetched_css = r2["asset"]["value"]

    checks = {
        "carousel root marker GONE": "data-hero-carousel" not in fetched_hero,
        "data-hero-pause GONE": "data-hero-pause" not in fetched_hero,
        "no <script> tag in hero": "<script>" not in fetched_hero,
        "no hp-hero__slide articles": "hp-hero__slide" not in fetched_hero,
        "office CDN img present": "hp-hero-slide-1-office.jpg" in fetched_hero,
        "img fetchpriority=high": 'fetchpriority="high"' in fetched_hero,
        "img loading=eager": 'loading="eager"' in fetched_hero,
        "old eyebrow restored": "Canadian-owned · Since 1964" in fetched_hero,
        "OECM Agreement 2025-470 present (x1)": fetched_hero.count("OECM Agreement 2025-470") == 1,
        "Request a Quote present (x1)": fetched_hero.count("Request a Quote") == 1,
        "phone tel link present (x1)": fetched_hero.count("tel:18008359565") == 1,
        "Shop furniture secondary CTA present": "Shop furniture" in fetched_hero,
        "hp-hero__caption present": 'class="hp-hero__caption"' in fetched_hero,
        "CSS carousel marker GONE": "HOMEPAGE HERO CAROUSEL — 2026-05-26" not in fetched_css,
        "CSS .hp-hero--carousel rule GONE": ".hp-hero--carousel" not in fetched_css,
        "CSS original .hp-hero rule still present": ".hp-hero__inner" in fetched_css,
    }
    print()
    print("=" * 72)
    all_ok = True
    for label, ok in checks.items():
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {label}")
        if not ok: all_ok = False
    print("=" * 72)
    if not all_ok:
        print("ONE OR MORE CHECKS FAILED"); sys.exit(3)
    print("REVERT COMPLETE — hero back to old format with office.jpg")


if __name__ == "__main__":
    main()
