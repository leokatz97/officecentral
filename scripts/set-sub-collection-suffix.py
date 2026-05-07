#!/usr/bin/env python3
"""
set-sub-collection-suffix.py
─────────────────────────────
P3-rollout: apply template_suffix='base' to all 68 BBI sub-collections so
they render the ds-cs-base.liquid product-listing template.

Uses custom_collections PUT endpoint (per verified API scope).

Usage:
  python3 scripts/set-sub-collection-suffix.py           # dry run
  python3 scripts/set-sub-collection-suffix.py --live    # write to Shopify
  python3 scripts/set-sub-collection-suffix.py --live --rollback  # restore pre-migration state
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

STORE       = "office-central-online.myshopify.com"
API_VERSION = "2024-01"
TARGET_SUFFIX = "base"

# All 68 sub-collection handles from site-architecture-2026-04-25.md
SUB_COLLECTION_HANDLES = [
    # Seating
    "highback-seating", "medium-back-seating", "mesh-seating", "leather-faux-seating",
    "stools-seating", "lounge-chairs-seating", "ottomans", "guest-seating",
    "stacking-seating", "folding-stacking-chairs-carts", "nesting-chairs-chair",
    "24-hour-seating", "big-heavy-seating", "cluster-seating", "industrial-seating", "gaming",
    # Desks
    "u-shape-desks-desks", "l-shape-desks-desks", "height-adjustable-tables-desks",
    "multi-person-workstations-desks", "benching-desks", "table-desks",
    "straight-desks-desks", "reception", "office-suites-desks",
    # Storage
    "lateral-files-storage", "vertical-files", "storage-cabinets-storage",
    "bookcases-storage", "hutch", "lateral-storage-combo-storage", "end-tab-filing-storage",
    "pedestal-drawers-storage", "fire-resistant-safes-storage", "metal-shelving",
    "lockers", "fire-resistant-file-cabinets-storage", "wardrobe-storage", "credenzas",
    # Tables
    "meeting-tables", "coffee-tables", "training-flip-top-tables", "end-tables-tables",
    "drafting-tables", "round-square-tables", "cafeteria-kitchen-tables",
    "bar-height-tables", "folding-tables-tables", "table-bases",
    # Boardroom
    "boardroom-conference-meeting", "lecterns-podiums", "audio-visual-equipment",
    # Ergonomic
    "height-adjustable-tables", "monitor-arms", "keyboard-trays", "desktop-sit-stand",
    # Panels
    "room-dividers-panels-dividers", "desk-top-dividers", "modesty-panels",
    # Accessories
    "chair-accessories", "desk-accessories", "monitor-accessories",
    "anti-fatigue-mats", "filing-accessories", "mobility-aids", "technology",
    # Quiet Spaces
    "phone-booths", "meeting-pods",
]


def _headers(token):
    return {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}


def get_collection_by_handle(handle, token):
    url = f"https://{STORE}/admin/api/{API_VERSION}/custom_collections.json?handle={urllib.parse.quote(handle)}"
    req = urllib.request.Request(url, headers=_headers(token))
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        colls = data.get("custom_collections", [])
        return colls[0] if colls else None
    except urllib.error.HTTPError as e:
        return None


def set_suffix(coll_id, suffix, token):
    url = f"https://{STORE}/admin/api/{API_VERSION}/custom_collections/{coll_id}.json"
    body = json.dumps({"custom_collection": {"id": coll_id, "template_suffix": suffix}}).encode()
    req = urllib.request.Request(url, data=body, headers=_headers(token), method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}


def main():
    parser = argparse.ArgumentParser(description="P3-rollout: set template_suffix=base on 68 sub-collections.")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--rollback", action="store_true", help="Restore pre-migration state from backup.")
    args = parser.parse_args()

    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path) as f:
        env = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.startswith("#"))
    token = env.get("SHOPIFY_TOKEN", "")
    if not token:
        sys.exit("ERROR: SHOPIFY_TOKEN not found in .env")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(f"data/backups/{ts}/sub-collection-suffixes-pre.json")

    print(f"\nP3-rollout: set template_suffix='{TARGET_SUFFIX}' on {len(SUB_COLLECTION_HANDLES)} sub-collections")
    print(f"Mode  : {'LIVE — writing to Shopify' if args.live else 'DRY RUN — no API calls'}")
    print(f"Store : {STORE}\n")

    # Rollback mode
    if args.rollback:
        backups_dir = Path("data/backups")
        candidates = sorted(backups_dir.glob("*/sub-collection-suffixes-pre.json"), reverse=True)
        if not candidates:
            sys.exit("No backup found in data/backups/")
        bpath = candidates[0]
        print(f"Rollback from: {bpath}")
        with open(bpath) as f:
            backup = json.load(f)
        for entry in backup:
            handle = entry["handle"]
            coll_id = entry["id"]
            prev_suffix = entry["prev_suffix"] or ""
            if not coll_id:
                print(f"  SKIP  {handle}  — was missing")
                continue
            if args.live:
                status, _ = set_suffix(coll_id, prev_suffix, token)
                print(f"  {'OK' if status == 200 else 'ERR'}   {handle}  → suffix='{prev_suffix}' ({status})")
                time.sleep(0.4)
            else:
                print(f"  DRY   {handle}  → would restore suffix='{prev_suffix}'")
        print("\nRollback complete." if args.live else "\nDry-run. Pass --live to apply.")
        return

    # Fetch current state + backup
    print("Fetching current collection state...")
    rows = []
    for handle in SUB_COLLECTION_HANDLES:
        time.sleep(0.35)
        coll = get_collection_by_handle(handle, token)
        if coll:
            rows.append({"handle": handle, "id": coll["id"],
                         "prev_suffix": coll.get("template_suffix") or ""})
        else:
            rows.append({"handle": handle, "id": None, "prev_suffix": ""})

    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup_path.write_text(json.dumps(rows, indent=2))
    print(f"Backup: {backup_path}")

    # Print plan
    to_write = [r for r in rows if r["id"] and r["prev_suffix"] != TARGET_SUFFIX]
    already  = [r for r in rows if r["id"] and r["prev_suffix"] == TARGET_SUFFIX]
    missing  = [r for r in rows if not r["id"]]
    print(f"\nTo update : {len(to_write)}")
    print(f"Already ok: {len(already)}")
    print(f"Missing   : {len(missing)}")
    for r in missing:
        print(f"  MISS  {r['handle']}")

    if not args.live:
        print("\nDry-run complete. Pass --live to apply.")
        return

    # Execute
    print(f"\nWriting {len(to_write)} collections...")
    Path("data/logs").mkdir(parents=True, exist_ok=True)
    log = []
    ok = fail = 0
    for r in to_write:
        status, resp = set_suffix(r["id"], TARGET_SUFFIX, token)
        entry = {**r, "new_suffix": TARGET_SUFFIX, "status": status}
        log.append(entry)
        if status == 200:
            print(f"  OK    {r['handle']}")
            ok += 1
        else:
            print(f"  ERR   {r['handle']} ({status}): {str(resp)[:80]}")
            fail += 1
        time.sleep(0.4)

    log_path = Path(f"data/logs/set-sub-suffix-{ts}.json")
    log_path.write_text(json.dumps(log, indent=2))

    print(f"\nDone: {ok} ok, {fail} failed")
    print(f"Log   : {log_path}")
    print(f"Backup: {backup_path}")
    if ok > 0:
        print(f"Rollback: python3 scripts/set-sub-collection-suffix.py --rollback --live")

    # Smoke test: 5 random sub-collections
    print("\n── Smoke test: 5 collections ──")
    import random
    sample = random.sample([r for r in to_write if r["id"]], min(5, len(to_write)))
    for r in sample:
        coll = get_collection_by_handle(r["handle"], token)
        suffix = coll.get("template_suffix") if coll else "ERR"
        status = "✅" if suffix == TARGET_SUFFIX else "❌"
        print(f"  {status} {r['handle']}  suffix={suffix}")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
