#!/usr/bin/env python3
"""
COLLECTION-IMG-PULL-1 / Phase 5 — Apply shopify:// URIs to template JSONs on DEV theme.

Hard-gated to theme 186373570873 (DEV). Backs up every target template JSON to
data/backups/collection-img-pull-pre-<ts>/ BEFORE any write. Re-fetches after each
PATCH to verify the new URI landed.

Usage: python3 scripts/collection-img-pull-phase5-apply.py
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_CSV = ROOT / "data" / "research" / "collection-img-pull-mapping-2026-05-25.csv"
UP_CSV = ROOT / "data" / "working" / "collection-img-pull-2026-05-25" / "uploaded.csv"
TS = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP_DIR = ROOT / "data" / "backups" / f"collection-img-pull-pre-{TS}"

DEV_THEME_ID = "186373570873"
STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
TOKEN = os.environ.get("SHOPIFY_TOKEN")
if not TOKEN:
    print("ERROR: SHOPIFY_TOKEN not set", file=sys.stderr); sys.exit(1)

RATE_LIMIT_SEC = 0.45


def admin_request(method, path, body=None):
    url = f"https://{STORE}/admin/api/{API_VERSION}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} HTTP {e.code}: {body[:400]}")
    finally:
        time.sleep(RATE_LIMIT_SEC)


def fetch_template(theme_id, asset_key):
    got = admin_request("GET", f"/themes/{theme_id}/assets.json?asset[key]={asset_key}")
    return json.loads(got["asset"]["value"])


def put_template(theme_id, asset_key, template_obj):
    raw = json.dumps(template_obj, indent=2, ensure_ascii=False)
    return admin_request("PUT", f"/themes/{theme_id}/assets.json", {
        "asset": {"key": asset_key, "value": raw}
    })


def main():
    # SAFETY GATE
    assert DEV_THEME_ID == "186373570873", "DEV theme ID drift detected — refuse to run"
    print(f"PHASE 5 — APPLY to theme {DEV_THEME_ID}")
    info = admin_request("GET", f"/themes/{DEV_THEME_ID}.json")["theme"]
    print(f"  theme: {info['name']!r}  role={info['role']}  id={info['id']}")
    if info["role"] == "main":
        raise SystemExit("REFUSING — target theme has role=main (LIVE). Abort.")
    if info["name"] != "BBI Landing Dev":
        raise SystemExit(f"REFUSING — target theme name {info['name']!r} != 'BBI Landing Dev'.")

    # Load mapping + uploads
    with open(MAP_CSV) as f:
        mapping = {r["slot_id"]: r for r in csv.DictReader(f)}
    with open(UP_CSV) as f:
        uploads = {r["slot_id"]: r for r in csv.DictReader(f)}

    # Build per-template apply plan
    plan = defaultdict(list)
    for slot_id, row in mapping.items():
        if row["action"] != "REPLACE":
            continue
        up = uploads.get(slot_id)
        if not up or up["status"] != "READY" or not up["shop_images_uri"]:
            print(f"  SKIP {slot_id} (upload not READY)")
            continue
        tmpl = row["parent_template"]
        plan[tmpl].append({
            "slot_id": slot_id,
            "slot_type": row["slot_type"],
            "block_key": row["block_key"],
            "shop_uri": up["shop_images_uri"],
            "old_uri": row["current_image"],
        })

    print(f"  templates to patch: {len(plan)}")
    print(f"  total slot updates: {sum(len(v) for v in plan.values())}")

    # BACKUP first
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nBackup → {BACKUP_DIR.relative_to(ROOT)}/")
    for tmpl_name in plan.keys():
        asset_key = f"templates/{tmpl_name}"
        t = fetch_template(DEV_THEME_ID, asset_key)
        backup_path = BACKUP_DIR / tmpl_name
        backup_path.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
        print(f"  ✓ {tmpl_name}")

    # APPLY
    print(f"\nApplying updates...")
    write_log = []
    fail_log = []
    for tmpl_name, updates in plan.items():
        asset_key = f"templates/{tmpl_name}"
        t = fetch_template(DEV_THEME_ID, asset_key)
        sec = t["sections"]["ds-cc-base"]
        n_hero = 0
        n_tile = 0
        for u in updates:
            if u["slot_type"] == "hero":
                sec["settings"]["hero_image"] = u["shop_uri"]
                n_hero += 1
            else:
                blk = sec["blocks"].get(u["block_key"])
                if not blk:
                    fail_log.append((u["slot_id"], f"block_key {u['block_key']} not found"))
                    continue
                blk["settings"]["image"] = u["shop_uri"]
                n_tile += 1
        put_template(DEV_THEME_ID, asset_key, t)

        # Verify by re-fetching
        v = fetch_template(DEV_THEME_ID, asset_key)
        vsec = v["sections"]["ds-cc-base"]
        verified_h = 0
        verified_t = 0
        for u in updates:
            if u["slot_type"] == "hero":
                if vsec["settings"].get("hero_image") == u["shop_uri"]:
                    verified_h += 1
                    write_log.append((u["slot_id"], "OK"))
                else:
                    fail_log.append((u["slot_id"], "hero verify mismatch"))
            else:
                blk = vsec["blocks"].get(u["block_key"])
                if blk and blk["settings"].get("image") == u["shop_uri"]:
                    verified_t += 1
                    write_log.append((u["slot_id"], "OK"))
                else:
                    fail_log.append((u["slot_id"], "tile verify mismatch"))

        print(f"  ✓ {tmpl_name:48s}  hero={n_hero}/{verified_h}  tile={n_tile}/{verified_t}")

    print()
    print("=" * 72)
    print(f"PHASE 5 SUMMARY  →  backup {BACKUP_DIR.relative_to(ROOT)}/")
    print("=" * 72)
    print(f"  Templates patched:  {len(plan)}")
    print(f"  Slots verified OK:  {len(write_log)}")
    print(f"  Failures:           {len(fail_log)}")
    if fail_log:
        print("FAILURES:")
        for sid, reason in fail_log:
            print(f"  {sid}: {reason}")
        sys.exit(1)


if __name__ == "__main__":
    main()
