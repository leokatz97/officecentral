#!/usr/bin/env python3
"""
create-smart-collections.py  (SMART-1)
────────────────────────────────────────
Create 14 smart collections for BBI:

  10 "view all" per category
     all-seating, all-desks, all-storage, all-tables, all-boardroom,
     all-ergonomic, all-panels, all-accessories, all-quiet-spaces,
     all-business-furniture   (disjunctive — union of all 9 type tags)

  4 brand-filtered
     keilhauer, global-teknion, ergocentric, oecm-eligible

SAFETY MODEL
  • Default is DRY RUN — no writes without --live.
  • Backs up existing smart-collection list before any writes.
  • Idempotent — re-running skips collections that already exist.
  • --rollback <log> deletes every collection this script created in that run.

Usage:
  python3 scripts/create-smart-collections.py               # dry run
  python3 scripts/create-smart-collections.py --live        # create all 14
  python3 scripts/create-smart-collections.py --live --only oecm-eligible
  python3 scripts/create-smart-collections.py --rollback data/logs/smart-create-<ts>.json --live
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

# ── Store constants ───────────────────────────────────────────────────────────

STORE       = "office-central-online.myshopify.com"
API_VERSION = "2024-01"


# ── API helpers ───────────────────────────────────────────────────────────────

def _headers(token: str) -> dict:
    return {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}


def _get(url: str, token: str, retries: int = 3) -> dict:
    req = urllib.request.Request(url, headers=_headers(token))
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"__error": e.code, "__body": e.read().decode()[:400]}
    return {"__error": "timeout"}


def _post(url: str, body: dict, token: str) -> tuple:
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=_headers(token), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def _delete(url: str, token: str) -> tuple:
    req = urllib.request.Request(url, headers=_headers(token), method="DELETE")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}


def get_smart_collection(handle: str, token: str):
    url = f"https://{STORE}/admin/api/{API_VERSION}/smart_collections.json?handle={urllib.parse.quote(handle)}"
    data = _get(url, token)
    colls = data.get("smart_collections", [])
    return colls[0] if colls else None


def get_custom_collection(handle: str, token: str):
    url = f"https://{STORE}/admin/api/{API_VERSION}/custom_collections.json?handle={urllib.parse.quote(handle)}"
    data = _get(url, token)
    colls = data.get("custom_collections", [])
    return colls[0] if colls else None


def delete_custom_collection(collection_id: int, token: str) -> tuple:
    url = f"https://{STORE}/admin/api/{API_VERSION}/custom_collections/{collection_id}.json"
    return _delete(url, token)


def create_smart_collection(title, handle, rules, disjunctive, token) -> tuple:
    url = f"https://{STORE}/admin/api/{API_VERSION}/smart_collections.json"
    body = {
        "smart_collection": {
            "title": title,
            "handle": handle,
            "rules": rules,
            "disjunctive": disjunctive,
            "sort_order": "best-selling",
        }
    }
    return _post(url, body, token)


def delete_smart_collection(collection_id: int, token: str) -> tuple:
    url = f"https://{STORE}/admin/api/{API_VERSION}/smart_collections/{collection_id}.json"
    return _delete(url, token)


# ── Collection definitions ────────────────────────────────────────────────────

CATEGORY_TYPE_TAGS = [
    "type:chairs",
    "type:desks",
    "type:storage",
    "type:tables",
    "type:boardroom",
    "type:ergonomic",
    "type:panels",
    "type:accessories",
    "type:quiet-spaces",
]

# Each tuple: (handle, title, rules_list, disjunctive)
COLLECTIONS = [
    # ── View-all per category (single-rule, conjunctive) ──────────────────────
    (
        "all-seating",
        "All Seating",
        [{"column": "tag", "relation": "equals", "condition": "type:chairs"}],
        False,
    ),
    (
        "all-desks",
        "All Desks & Workstations",
        [{"column": "tag", "relation": "equals", "condition": "type:desks"}],
        False,
    ),
    (
        "all-storage",
        "All Storage & Filing",
        [{"column": "tag", "relation": "equals", "condition": "type:storage"}],
        False,
    ),
    (
        "all-tables",
        "All Tables",
        [{"column": "tag", "relation": "equals", "condition": "type:tables"}],
        False,
    ),
    (
        "all-boardroom",
        "All Boardroom & Conference",
        [{"column": "tag", "relation": "equals", "condition": "type:boardroom"}],
        False,
    ),
    (
        "all-ergonomic",
        "All Ergonomic Products",
        [{"column": "tag", "relation": "equals", "condition": "type:ergonomic"}],
        False,
    ),
    (
        "all-panels",
        "All Panels & Dividers",
        [{"column": "tag", "relation": "equals", "condition": "type:panels"}],
        False,
    ),
    (
        "all-accessories",
        "All Accessories",
        [{"column": "tag", "relation": "equals", "condition": "type:accessories"}],
        False,
    ),
    (
        "all-quiet-spaces",
        "All Quiet Spaces",
        [{"column": "tag", "relation": "equals", "condition": "type:quiet-spaces"}],
        False,
    ),
    # ── View-all business furniture (union of all 9 type tags, disjunctive) ───
    (
        "all-business-furniture",
        "All Business Furniture",
        [{"column": "tag", "relation": "equals", "condition": t} for t in CATEGORY_TYPE_TAGS],
        True,
    ),
    # ── Brand-filtered ────────────────────────────────────────────────────────
    (
        "keilhauer",
        "Keilhauer",
        [{"column": "tag", "relation": "equals", "condition": "brand:keilhauer"}],
        False,
    ),
    (
        "global-teknion",
        "Global / Teknion",
        [{"column": "tag", "relation": "equals", "condition": "brand:global-teknion"}],
        False,
    ),
    (
        "ergocentric",
        "ergoCentric",
        [{"column": "tag", "relation": "equals", "condition": "brand:ergocentric"}],
        False,
    ),
    (
        "oecm-eligible",
        "OECM-Eligible Products",
        [{"column": "tag", "relation": "equals", "condition": "oecm-eligible"}],
        False,
    ),
    # ── BRAND-PAGES-1 brand×category (15 collections, 2026-05-20) ─────────────
    # OTG (Offices to Go) — 7 collections, rule: brand:otg-offices-to-go AND type:<cat>
    (
        "otg-chairs",
        "OTG Seating",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:chairs"}],
        False,
    ),
    (
        "otg-desks",
        "OTG Desks & Workstations",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:desks"}],
        False,
    ),
    (
        "otg-storage",
        "OTG Storage & Filing",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:storage"}],
        False,
    ),
    (
        "otg-tables",
        "OTG Tables",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:tables"}],
        False,
    ),
    (
        "otg-accessories",
        "OTG Accessories",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:accessories"}],
        False,
    ),
    (
        "otg-lounge",
        "OTG Lounge Seating",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:lounge"}],
        False,
    ),
    (
        "otg-panels",
        "OTG Panels & Dividers",
        [{"column": "tag", "relation": "equals", "condition": "brand:otg-offices-to-go"},
         {"column": "tag", "relation": "equals", "condition": "type:panels"}],
        False,
    ),
    # Heartwood — 3 collections, rule: brand:heartwood-manufacturing-ltd AND type:<cat>
    (
        "heartwood-desks",
        "Heartwood Desks & Workstations",
        [{"column": "tag", "relation": "equals", "condition": "brand:heartwood-manufacturing-ltd"},
         {"column": "tag", "relation": "equals", "condition": "type:desks"}],
        False,
    ),
    (
        "heartwood-storage",
        "Heartwood Storage & Casegoods",
        [{"column": "tag", "relation": "equals", "condition": "brand:heartwood-manufacturing-ltd"},
         {"column": "tag", "relation": "equals", "condition": "type:storage"}],
        False,
    ),
    (
        "heartwood-tables",
        "Heartwood Tables",
        [{"column": "tag", "relation": "equals", "condition": "brand:heartwood-manufacturing-ltd"},
         {"column": "tag", "relation": "equals", "condition": "type:tables"}],
        False,
    ),
    # ObusForme — 1 collection (thin catalog), rule: brand:obusforme AND type:chairs
    (
        "obusforme-chairs",
        "ObusForme Seating",
        [{"column": "tag", "relation": "equals", "condition": "brand:obusforme"},
         {"column": "tag", "relation": "equals", "condition": "type:chairs"}],
        False,
    ),
    # Global Furniture Group — 4 collections, rule: brand:global-furniture-group AND type:<cat>
    (
        "gfg-chairs",
        "Global Seating",
        [{"column": "tag", "relation": "equals", "condition": "brand:global-furniture-group"},
         {"column": "tag", "relation": "equals", "condition": "type:chairs"}],
        False,
    ),
    (
        "gfg-tables",
        "Global Tables",
        [{"column": "tag", "relation": "equals", "condition": "brand:global-furniture-group"},
         {"column": "tag", "relation": "equals", "condition": "type:tables"}],
        False,
    ),
    (
        "gfg-desks",
        "Global Desks & Workstations",
        [{"column": "tag", "relation": "equals", "condition": "brand:global-furniture-group"},
         {"column": "tag", "relation": "equals", "condition": "type:desks"}],
        False,
    ),
    (
        "gfg-storage",
        "Global Storage & Filing",
        [{"column": "tag", "relation": "equals", "condition": "brand:global-furniture-group"},
         {"column": "tag", "relation": "equals", "condition": "type:storage"}],
        False,
    ),
]


# ── Backup helpers ────────────────────────────────────────────────────────────

def backup_smart_collections(token: str, ts: str) -> Path:
    url = f"https://{STORE}/admin/api/{API_VERSION}/smart_collections.json?limit=250"
    data = _get(url, token)
    existing = data.get("smart_collections", [])
    path = Path(f"data/backups/{ts}/smart-collections-pre-smart1.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(existing, indent=2))
    print(f"  Backup saved: {path}  ({len(existing)} smart collections found)")
    return path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Create 14 BBI smart collections (SMART-1). Default: DRY RUN."
    )
    parser.add_argument("--live", action="store_true", help="Write to Shopify.")
    parser.add_argument("--only", metavar="HANDLE", help="Create only one collection by handle.")
    parser.add_argument(
        "--convert-custom",
        action="store_true",
        help="If a handle is taken by a custom (manual) collection, delete it and recreate as smart.",
    )
    parser.add_argument(
        "--rollback",
        metavar="LOG_FILE",
        help="Delete all collections created in the named run log.",
    )
    args = parser.parse_args()

    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path) as f:
        env = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.startswith("#"))
    token = env.get("SHOPIFY_TOKEN", "")
    if not token:
        sys.exit("ERROR: SHOPIFY_TOKEN not found in .env")

    Path("data/backups").mkdir(parents=True, exist_ok=True)
    Path("data/logs").mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── Rollback ─────────────────────────────────────────────────────────────
    if args.rollback:
        log_path = Path(args.rollback)
        if not log_path.exists():
            sys.exit(f"ERROR: log file not found: {log_path}")
        with open(log_path) as f:
            run_log = json.load(f)

        created = [r for r in run_log if r.get("action") == "created"]
        print(f"\nROLLBACK: {'LIVE' if args.live else 'DRY RUN'} — {len(created)} collections to delete\n")

        for entry in created:
            handle = entry["handle"]
            coll_id = entry.get("id")
            if not coll_id:
                coll = get_smart_collection(handle, token)
                coll_id = coll["id"] if coll else None

            if coll_id and args.live:
                status, _ = delete_smart_collection(coll_id, token)
                flag = "✅ deleted" if status in (200, 204) else f"❌ error {status}"
                time.sleep(0.35)
            elif coll_id:
                flag = "DRY  would delete"
            else:
                flag = "SKIP (not found)"

            print(f"  {flag:<20}  {handle}  (id={coll_id})")

        print("\nRollback complete." if args.live else "\nDry-run. Pass --live to apply.")
        return

    # ── Create mode ──────────────────────────────────────────────────────────
    target = COLLECTIONS
    if args.only:
        target = [c for c in COLLECTIONS if c[0] == args.only]
        if not target:
            sys.exit(f"ERROR: handle '{args.only}' not found in COLLECTIONS list")

    print(f"\nSMART-1 — Create BBI smart collections")
    print(f"Mode  : {'LIVE — writing to Shopify' if args.live else 'DRY RUN — no writes'}")
    print(f"Store : {STORE}")
    print(f"Target: {len(target)} collections\n")

    backup_path = backup_smart_collections(token, ts)
    print("  Waiting 2s for rate-limit recovery...\n")
    time.sleep(2)

    results = []

    for handle, title, rules, disjunctive in target:
        existing = get_smart_collection(handle, token)
        time.sleep(0.35)

        if existing:
            action = "existing"
            coll_id = existing["id"]
            flag = "⏭  SKIP (exists)"
        elif args.live:
            # Check if a custom collection is blocking the handle
            custom = get_custom_collection(handle, token)
            time.sleep(0.35)
            if custom and args.convert_custom:
                del_status, _ = delete_custom_collection(custom["id"], token)
                time.sleep(0.5)
                if del_status not in (200, 204):
                    action = "error"
                    coll_id = None
                    flag = f"❌ ERROR deleting custom {del_status}"
                    results.append({"handle": handle, "title": title, "action": action,
                                    "id": coll_id, "disjunctive": disjunctive})
                    print(f"  {flag:<28}  {handle}")
                    continue
            status, resp = create_smart_collection(title, handle, rules, disjunctive, token)
            if status in (200, 201):
                action = "created"
                coll_id = resp.get("smart_collection", {}).get("id")
                flag = "✅ CREATED"
                if custom and args.convert_custom:
                    flag = "✅ CONVERTED (custom→smart)"
            else:
                action = "error"
                coll_id = None
                flag = f"❌ ERROR {status}: {str(resp)[:80]}"
            time.sleep(0.5)
        else:
            # Dry run — report whether a custom blocker exists
            custom = get_custom_collection(handle, token)
            time.sleep(0.35)
            if custom:
                action = "would_convert" if args.convert_custom else "blocked_custom"
                flag = "DRY  would convert custom→smart" if args.convert_custom else "⚠️  BLOCKED (custom exists)"
            else:
                action = "would_create"
                flag = "DRY  would create"
            coll_id = None

        rule_summary = (
            f"disjunctive OR ({len(rules)} type tags)"
            if disjunctive
            else rules[0]["condition"]
        )
        print(f"  {flag:<28}  {handle:<28}  rule={rule_summary}")

        results.append({
            "handle":      handle,
            "title":       title,
            "action":      action,
            "id":          coll_id,
            "disjunctive": disjunctive,
        })

    # Save JSON log
    log_path = Path(f"data/logs/smart-create-{ts}.json")
    log_path.write_text(json.dumps(results, indent=2))

    # Save CSV report
    csv_path = Path(f"data/reports/smart-collections-{ts}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["handle", "title", "action", "id", "disjunctive"])
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in ["handle", "title", "action", "id", "disjunctive"]})

    # Summary
    n_created  = sum(1 for r in results if r["action"] in ("created", "would_convert", "would_create"))
    n_existing = sum(1 for r in results if r["action"] == "existing")
    n_would    = sum(1 for r in results if r["action"] in ("would_create", "would_convert"))
    n_error    = sum(1 for r in results if r["action"] in ("error", "blocked_custom"))

    print(f"\n{'='*60}")
    if args.live:
        print(f"SMART-1 complete")
        print(f"  Created  : {n_created}")
        print(f"  Skipped  : {n_existing}  (already existed)")
        print(f"  Errors   : {n_error}")
    else:
        print(f"SMART-1 dry-run")
        print(f"  Would create : {n_would}")
        print(f"  Already exist: {n_existing}")

    print(f"\nLog    : {log_path}")
    print(f"Backup : {backup_path}")
    print(f"Report : {csv_path}")

    if args.live and n_created > 0:
        print(f"\nRollback: python3 scripts/create-smart-collections.py --rollback {log_path} --live")


if __name__ == "__main__":
    main()
