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

# Stage 3.2c — exactly the 56 populated legacy collections from stage-3.2a.5-migration-plan.md §1.
# highback-seating is excluded (already migrated in Stage 3.2b).
# 0-product collections (audio-visual-equipment, chair-accessories, anti-fatigue-mats,
# technology, metal-shelving) are excluded per migration plan §6.
# Missing handles (monitor-accessories, filing-accessories, mobility-aids,
# phone-booths, meeting-pods) are excluded — don't exist in Shopify.
SUB_COLLECTION_HANDLES = [
    # Seating (15)
    "medium-back-seating", "mesh-seating", "guest-seating", "leather-faux-seating",
    "lounge-chairs-seating", "stacking-seating", "stools-seating", "big-heavy-seating",
    "industrial-seating", "folding-stacking-chairs-carts", "ottomans",
    "nesting-chairs-chair", "24-hour-seating", "gaming", "cluster-seating",
    # Desks (9)
    "l-shape-desks-desks", "height-adjustable-tables-desks", "straight-desks-desks",
    "u-shape-desks-desks", "office-suites-desks", "multi-person-workstations-desks",
    "table-desks", "reception", "benching-desks",
    # Storage (13)
    "bookcases-storage", "storage-cabinets-storage", "fire-resistant-safes-storage",
    "credenzas", "pedestal-drawers-storage", "lateral-files-storage",
    "fire-resistant-file-cabinets-storage", "lockers", "vertical-files",
    "wardrobe-storage", "lateral-storage-combo-storage", "hutch", "end-tab-filing-storage",
    # Tables (10)
    "meeting-tables", "round-square-tables", "folding-tables-tables", "drafting-tables",
    "coffee-tables", "end-tables-tables", "table-bases", "training-flip-top-tables",
    "cafeteria-kitchen-tables", "bar-height-tables",
    # Boardroom (2)
    "boardroom-conference-meeting", "lecterns-podiums",
    # Ergonomic Products (4)
    "height-adjustable-tables", "desktop-sit-stand", "monitor-arms", "keyboard-trays",
    # Panels & Room Dividers (3)
    "room-dividers-panels-dividers", "desk-top-dividers", "modesty-panels",
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
