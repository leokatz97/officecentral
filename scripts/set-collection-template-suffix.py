#!/usr/bin/env python3
"""
set-collection-template-suffix.py
──────────────────────────────────
Sets template_suffix on Shopify collections so they render the
collection.category.json template (which uses ds-cc-base.liquid).

DEFAULT BEHAVIOUR: DRY RUN — prints what WOULD change, makes no API calls.
Requires --live flag for actual writes (per CLAUDE.md BBI rule #4).

Usage:
  python3 scripts/set-collection-template-suffix.py <THEME_ID> [handles...]
  python3 scripts/set-collection-template-suffix.py <THEME_ID> --live
  python3 scripts/set-collection-template-suffix.py <THEME_ID> --rollback data/backups/<ts>/collection-suffixes-pre.json
  python3 scripts/set-collection-template-suffix.py <THEME_ID> seating --live   # single collection

Examples:
  # Dry-run all targets (safe to run anytime):
  python3 scripts/set-collection-template-suffix.py 186373570873

  # Apply to one collection only:
  python3 scripts/set-collection-template-suffix.py 186373570873 seating --live

  # Apply to all targets:
  python3 scripts/set-collection-template-suffix.py 186373570873 --live

  # Rollback to a previous backup:
  python3 scripts/set-collection-template-suffix.py 186373570873 --rollback data/backups/20260506_201448/collection-suffixes-pre.json --live

Notes:
  - Backs up current template_suffix values to data/backups/<ts>/collection-suffixes-pre.json BEFORE writing
  - Logs every API response to data/logs/set-suffix-<ts>.json
  - SHOPIFY_TOKEN env var required
  - PB-10: only seed seating for the smoke test; bulk-suffix in P2-1..P2-10
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ── Default targets (all 10 collection.category.json collections) ──────────
DEFAULT_TARGETS = [
    "business-furniture",
    "seating",
    "desks",
    "storage",
    "tables",
    "boardroom",
    "ergonomic-products",
    "panels-room-dividers",
    "accessories",
    "quiet-spaces",
]

TARGET_SUFFIX = "category"

# ── Helpers ─────────────────────────────────────────────────────────────────

STORE = "office-central-online.myshopify.com"
API_VERSION = "2024-01"


def api_base(token: str) -> dict:
    return {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    }


def get_collection_by_handle(handle: str, token: str):
    """Fetch collection metadata by handle. Returns the collection dict or None."""
    url = f"https://{STORE}/admin/api/{API_VERSION}/collections.json?handle={handle}"
    req = urllib.request.Request(url, headers=api_base(token), method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            cols = data.get("collections", [])
            return cols[0] if cols else None
    except urllib.error.HTTPError as e:
        print(f"  WARN  GET {handle}: HTTP {e.code} — {e.read().decode()[:120]}", file=sys.stderr)
        return None


def set_template_suffix(collection_id: int, suffix: str, token: str):
    """PUT template_suffix on a collection. Returns (status_code, response_dict)."""
    url = f"https://{STORE}/admin/api/{API_VERSION}/collections/{collection_id}.json"
    body = json.dumps({"collection": {"id": collection_id, "template_suffix": suffix}}).encode()
    req = urllib.request.Request(url, data=body, headers=api_base(token), method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def ensure_dirs():
    Path("data/backups").mkdir(parents=True, exist_ok=True)
    Path("data/logs").mkdir(parents=True, exist_ok=True)


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Set template_suffix on BBI collections. Default: DRY RUN."
    )
    parser.add_argument("theme_id", help="Shopify theme ID (for reference only; suffix is store-wide).")
    parser.add_argument(
        "handles",
        nargs="*",
        help="Collection handles to process. Omit for all DEFAULT_TARGETS.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Actually write to Shopify. Without this flag, only a dry run is performed.",
    )
    parser.add_argument(
        "--rollback",
        metavar="BACKUP_FILE",
        help="Restore template_suffix values from a backup JSON file.",
    )
    parser.add_argument(
        "--suffix",
        default=TARGET_SUFFIX,
        metavar="SUFFIX",
        help=f"Template suffix to apply (default: '{TARGET_SUFFIX}'). Example: --suffix=seating",
    )
    args = parser.parse_args()

    token = os.environ.get("SHOPIFY_TOKEN")
    if not token:
        sys.exit("ERROR: SHOPIFY_TOKEN env var is not set.")

    live = args.live
    target_suffix = args.suffix  # may be overridden from CLI
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ensure_dirs()

    # ── Rollback mode ────────────────────────────────────────────────────────
    if args.rollback:
        backup_path = Path(args.rollback)
        if not backup_path.exists():
            sys.exit(f"ERROR: backup file not found: {backup_path}")
        with open(backup_path) as f:
            backup = json.load(f)

        print(f"\nROLLBACK from {backup_path}")
        print(f"Mode: {'LIVE — writing to Shopify' if live else 'DRY RUN — no API calls'}\n")

        header = f"{'handle':<40} {'id':<14} {'restore_suffix':<20} {'action'}"
        print(header)
        print("-" * len(header))

        log_entries = []
        for entry in backup:
            handle  = entry["handle"]
            col_id  = entry["id"]
            restore = entry["template_suffix"] or ""
            action  = "RESTORE" if live else "DRY-RUN"
            print(f"  {handle:<38} {col_id:<14} {restore or '(none)':<20} {action}")
            if live:
                status, resp = set_template_suffix(col_id, restore, token)
                action = f"HTTP {status}"
                log_entries.append({"handle": handle, "id": col_id, "restore": restore, "status": status, "response": resp})
                print(f"    → {action}")

        if live and log_entries:
            log_path = Path(f"data/logs/set-suffix-rollback-{ts}.json")
            log_path.write_text(json.dumps(log_entries, indent=2))
            print(f"\nLog saved: {log_path}")

        print("\nRollback complete." if live else "\nDry-run complete. Pass --live to apply.")
        return

    # ── Forward mode ─────────────────────────────────────────────────────────
    targets = args.handles if args.handles else DEFAULT_TARGETS

    print(f"\nStore   : {STORE}")
    print(f"Theme   : {args.theme_id}  (suffix is store-wide, not per-theme)")
    print(f"Suffix  : {target_suffix}")
    print(f"Targets : {', '.join(targets)}")
    print(f"Mode    : {'LIVE — writing to Shopify' if live else 'DRY RUN — no API calls'}\n")

    # 1. Fetch current state for all handles
    print("Fetching current collection data...")
    collections_info = {}
    for handle in targets:
        col = get_collection_by_handle(handle, token)
        if col:
            collections_info[handle] = col
            print(f"  FOUND  {handle}  (id={col['id']}, current_suffix={col.get('template_suffix') or '(none)'})")
        else:
            print(f"  MISS   {handle}  — collection not found in store, skipping")

    # 2. Backup before any writes
    backup_path = Path(f"data/backups/{ts}/collection-suffixes-pre.json")
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup_data = [
        {
            "handle":          h,
            "id":              col["id"],
            "title":           col.get("title"),
            "template_suffix": col.get("template_suffix") or "",
        }
        for h, col in collections_info.items()
    ]
    backup_path.write_text(json.dumps(backup_data, indent=2))
    print(f"\nBackup saved: {backup_path}")

    # 3. Print summary table
    col_w = max(len(h) for h in targets) + 2 if targets else 30
    print(f"\n  {'handle':<{col_w}} {'current_suffix':<22} {'new_suffix':<22} action")
    print("  " + "-" * (col_w + 22 + 22 + 12))

    to_write = []
    for handle in targets:
        col = collections_info.get(handle)
        if not col:
            print(f"  {handle:<{col_w}} {'—':<22} {'—':<22} SKIP (not found)")
            continue
        current = col.get("template_suffix") or ""
        if current == target_suffix:
            print(f"  {handle:<{col_w}} {current:<22} {target_suffix:<22} ALREADY SET")
        else:
            action = "WRITE" if live else "DRY-RUN"
            print(f"  {handle:<{col_w}} {current or '(none)':<22} {target_suffix:<22} {action}")
            to_write.append((handle, col["id"], current))

    # 4. Execute writes
    if not live:
        print(f"\n{len(to_write)} collection(s) would be updated. Pass --live to apply.")
        if backup_data:
            print(f"Rollback available: {backup_path}")
        return

    if not to_write:
        print("\nNothing to do — all collections already have the target suffix.")
        return

    print(f"\nWriting {len(to_write)} collection(s)...")
    log_entries = []
    ok_count = 0
    fail_count = 0

    for handle, col_id, prev_suffix in to_write:
        status, resp = set_template_suffix(col_id, target_suffix, token)
        entry = {
            "handle":     handle,
            "id":         col_id,
            "prev_suffix": prev_suffix,
            "new_suffix":  target_suffix,
            "status":      status,
            "response":    resp,
        }
        log_entries.append(entry)
        if status == 200:
            print(f"  OK   {handle} ({status})")
            ok_count += 1
        else:
            print(f"  ERR  {handle} ({status}): {str(resp)[:120]}")
            fail_count += 1

    # 5. Save log
    log_path = Path(f"data/logs/set-suffix-{ts}.json")
    log_path.write_text(json.dumps(log_entries, indent=2))
    print(f"\nResults: {ok_count} ok, {fail_count} failed")
    print(f"Log    : {log_path}")
    print(f"Rollback: {backup_path}")


if __name__ == "__main__":
    main()
