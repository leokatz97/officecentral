#!/usr/bin/env python3
"""
migrate-to-smart-collections.py
────────────────────────────────
Converts Shopify custom (manual) collections to smart (automated) collections
using tag-based rules derived from the BBI taxonomy.

SAFETY MODEL
  • Default is DRY RUN — no writes without --live.
  • Backs up all current custom-collection state before any writes.
  • Converts in batches of 10; asserts product counts haven't DROPPED > 10%
    after each batch (increases are acceptable — smart rules are a superset).
  • --rollback restores from a backup JSON.

REUSABLE HELPER
  The create_smart_collection() and get_or_create_smart_collection() functions
  are designed to be imported by SMART-1 (create-smart-collections.py) so the
  view-all + brand-filtered collections share the same API plumbing.

Usage:
  python3 scripts/migrate-to-smart-collections.py           # dry run all 68
  python3 scripts/migrate-to-smart-collections.py --live --batch=accessories
  python3 scripts/migrate-to-smart-collections.py --live   # full migration
  python3 scripts/migrate-to-smart-collections.py --rollback data/backups/<ts>/collections-pre-migration.json --live

Smoke test (per PB-14):
  1.  python3 scripts/migrate-to-smart-collections.py          # dry run
  2.  python3 scripts/migrate-to-smart-collections.py --live --batch=accessories
  3.  Verify counts held on /collections/accessories
  4.  python3 scripts/migrate-to-smart-collections.py --rollback data/backups/<ts>/collections-pre-migration.json --live
  5.  Verify count restored
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
from typing import Optional, Tuple

# ── Store constants ──────────────────────────────────────────────────────────

STORE       = "office-central-online.myshopify.com"
API_VERSION = "2024-01"
BATCH_SIZE  = 10

# ── Tag-rule mapping for all 68 sub-collections ──────────────────────────────
# Format: handle → (smart_rule_column, smart_rule_value, smart_rule_relation)
# relation is always "equals" unless noted.
# Collections marked NEEDS_ENRICHMENT have no unique tag yet;
# they get skipped in live mode but are reported in dry-run.

NEEDS_ENRICHMENT = "__NEEDS_ENRICHMENT__"

# Maps collection handle → tag rule string (e.g. "type:chairs")
# OR NEEDS_ENRICHMENT if no unique tag exists yet.
HANDLE_TO_RULE = {
    # ── Seating Level-2 ────────────────────────────────────────────────────
    "seating":                          "type:chairs",
    # Seating sub-collections share type:chairs → enrichment needed for subcategory rules
    "highback-seating":                 NEEDS_ENRICHMENT,
    "medium-back-seating":              NEEDS_ENRICHMENT,
    "mesh-seating":                     NEEDS_ENRICHMENT,
    "leather-faux-seating":             NEEDS_ENRICHMENT,
    "stools-seating":                   NEEDS_ENRICHMENT,
    "lounge-chairs-seating":            NEEDS_ENRICHMENT,
    "ottomans":                         NEEDS_ENRICHMENT,
    "guest-seating":                    NEEDS_ENRICHMENT,
    "stacking-seating":                 NEEDS_ENRICHMENT,
    "folding-stacking-chairs-carts":    NEEDS_ENRICHMENT,
    "nesting-chairs-chair":             NEEDS_ENRICHMENT,
    "24-hour-seating":                  NEEDS_ENRICHMENT,
    "big-heavy-seating":                NEEDS_ENRICHMENT,
    "cluster-seating":                  NEEDS_ENRICHMENT,
    "industrial-seating":               NEEDS_ENRICHMENT,
    "gaming":                           NEEDS_ENRICHMENT,

    # ── Desks Level-2 ──────────────────────────────────────────────────────
    "desks":                            "type:desks",
    "u-shape-desks-desks":              NEEDS_ENRICHMENT,
    "l-shape-desks-desks":              NEEDS_ENRICHMENT,
    "height-adjustable-tables-desks":   NEEDS_ENRICHMENT,
    "multi-person-workstations-desks":  NEEDS_ENRICHMENT,
    "benching-desks":                   NEEDS_ENRICHMENT,
    "table-desks":                      NEEDS_ENRICHMENT,
    "straight-desks-desks":             NEEDS_ENRICHMENT,
    "reception":                        NEEDS_ENRICHMENT,
    "office-suites-desks":              NEEDS_ENRICHMENT,

    # ── Storage Level-2 ────────────────────────────────────────────────────
    "storage":                          "type:storage",
    "lateral-files-storage":            NEEDS_ENRICHMENT,
    "vertical-files":                   NEEDS_ENRICHMENT,
    "storage-cabinets-storage":         NEEDS_ENRICHMENT,
    "bookcases-storage":                NEEDS_ENRICHMENT,
    "hutch":                            NEEDS_ENRICHMENT,
    "lateral-storage-combo-storage":    NEEDS_ENRICHMENT,
    "end-tab-filing-storage":           NEEDS_ENRICHMENT,
    "pedestal-drawers-storage":         NEEDS_ENRICHMENT,
    "fire-resistant-safes-storage":     NEEDS_ENRICHMENT,
    "metal-shelving":                   NEEDS_ENRICHMENT,
    "lockers":                          NEEDS_ENRICHMENT,
    "fire-resistant-file-cabinets-storage": NEEDS_ENRICHMENT,
    "wardrobe-storage":                 NEEDS_ENRICHMENT,
    "credenzas":                        NEEDS_ENRICHMENT,

    # ── Tables Level-2 ─────────────────────────────────────────────────────
    "tables":                           "type:tables",
    "meeting-tables":                   NEEDS_ENRICHMENT,
    "coffee-tables":                    NEEDS_ENRICHMENT,
    "training-flip-top-tables":         NEEDS_ENRICHMENT,
    "end-tables-tables":                NEEDS_ENRICHMENT,
    "drafting-tables":                  NEEDS_ENRICHMENT,
    "round-square-tables":              NEEDS_ENRICHMENT,
    "cafeteria-kitchen-tables":         NEEDS_ENRICHMENT,
    "bar-height-tables":                NEEDS_ENRICHMENT,
    "folding-tables-tables":            NEEDS_ENRICHMENT,
    "table-bases":                      NEEDS_ENRICHMENT,

    # ── Boardroom Level-2 ──────────────────────────────────────────────────
    "boardroom":                        "type:boardroom",
    "boardroom-conference-meeting":     NEEDS_ENRICHMENT,
    "lecterns-podiums":                 NEEDS_ENRICHMENT,
    "audio-visual-equipment":           NEEDS_ENRICHMENT,

    # ── Ergonomic Level-2 ──────────────────────────────────────────────────
    "ergonomic-products":               "type:ergonomic",
    "height-adjustable-tables":         NEEDS_ENRICHMENT,
    "monitor-arms":                     NEEDS_ENRICHMENT,
    "keyboard-trays":                   NEEDS_ENRICHMENT,
    "desktop-sit-stand":                NEEDS_ENRICHMENT,

    # ── Panels Level-2 ─────────────────────────────────────────────────────
    "panels-room-dividers":             "type:panels",
    "room-dividers-panels-dividers":    NEEDS_ENRICHMENT,
    "desk-top-dividers":                NEEDS_ENRICHMENT,
    "modesty-panels":                   NEEDS_ENRICHMENT,

    # ── Accessories Level-2 ────────────────────────────────────────────────
    "accessories":                      "type:accessories",
    "chair-accessories":                NEEDS_ENRICHMENT,
    "desk-accessories":                 NEEDS_ENRICHMENT,
    "monitor-accessories":              NEEDS_ENRICHMENT,
    "anti-fatigue-mats":                NEEDS_ENRICHMENT,
    "filing-accessories":               NEEDS_ENRICHMENT,
    "mobility-aids":                    NEEDS_ENRICHMENT,
    "technology":                       NEEDS_ENRICHMENT,

    # ── Quiet Spaces Level-2 ───────────────────────────────────────────────
    "quiet-spaces":                     "type:quiet-spaces",
    "phone-booths":                     NEEDS_ENRICHMENT,
    "meeting-pods":                     NEEDS_ENRICHMENT,
}


# ── API helpers (designed for import by SMART-1) ─────────────────────────────

def _headers(token: str) -> dict:
    return {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}


def _get(url, token, _retries=3):
    req = urllib.request.Request(url, headers=_headers(token))
    for attempt in range(_retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < _retries - 1:
                time.sleep(2 ** attempt)  # 1s, 2s backoff
                continue
            return {"__error": e.code, "__body": e.read().decode()[:400]}
    return {"__error": "timeout", "__body": "max retries exceeded"}


def _post(url, body, token):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=_headers(token), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def _put(url, body, token):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=_headers(token), method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def _delete(url, token):
    req = urllib.request.Request(url, headers=_headers(token), method="DELETE")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}


def get_custom_collection(handle: str, token: str, store: str = STORE) -> Optional[dict]:
    url = f"https://{store}/admin/api/{API_VERSION}/custom_collections.json?handle={urllib.parse.quote(handle)}"
    data = _get(url, token)
    colls = data.get("custom_collections", [])
    return colls[0] if colls else None


def get_smart_collection(handle: str, token: str, store: str = STORE) -> Optional[dict]:
    url = f"https://{store}/admin/api/{API_VERSION}/smart_collections.json?handle={urllib.parse.quote(handle)}"
    data = _get(url, token)
    colls = data.get("smart_collections", [])
    return colls[0] if colls else None


def get_collection_product_ids(collection_id, token, store=STORE):
    """Return list of product_ids in a custom collection via the Collects API."""
    product_ids = []
    url = f"https://{store}/admin/api/{API_VERSION}/collects.json?collection_id={collection_id}&limit=250"
    data = _get(url, token)
    collects = data.get("collects", [])
    product_ids.extend(c["product_id"] for c in collects)
    return product_ids


def restore_collects(collection_id, product_ids, token, store=STORE):
    """Re-add products to a restored custom collection via the Collects API."""
    restored = 0
    for pid in product_ids:
        url = f"https://{store}/admin/api/{API_VERSION}/collects.json"
        status, resp = _post(url, {"collect": {"collection_id": collection_id, "product_id": pid}}, token)
        if status in (200, 201):
            restored += 1
        time.sleep(0.2)
    return restored


def get_collection_product_count(collection_id, token, store=STORE):
    url = f"https://{store}/admin/api/{API_VERSION}/collects/count.json?collection_id={collection_id}"
    data = _get(url, token)
    return data.get("count", 0)


def get_smart_collection_product_count(collection_id: int, token: str, store: str = STORE) -> int:
    url = f"https://{store}/admin/api/{API_VERSION}/products/count.json?collection_id={collection_id}"
    data = _get(url, token)
    return data.get("count", 0)


def create_smart_collection(
    title,
    handle,
    rules,
    disjunctive=False,
    sort_order="best-selling",
    token="",
    store=STORE,
    body_html="",
):
    """
    Create a new smart collection. Returns (status_code, collection_dict).

    rules format: [{"column": "tag", "relation": "equals", "condition": "type:chairs"}]

    This function is the canonical helper imported by SMART-1
    (create-smart-collections.py) for the view-all + brand collections.
    """
    url = f"https://{store}/admin/api/{API_VERSION}/smart_collections.json"
    body = {
        "smart_collection": {
            "title": title,
            "handle": handle,
            "rules": rules,
            "disjunctive": disjunctive,
            "sort_order": sort_order,
            "body_html": body_html,
        }
    }
    return _post(url, body, token)


def get_or_create_smart_collection(
    title,
    handle,
    rules,
    disjunctive=False,
    sort_order="best-selling",
    token="",
    store=STORE,
):
    """
    Idempotent: returns ('existing', coll) if the handle already exists as a
    smart collection, else creates and returns ('created', coll).
    Used by SMART-1 for safe re-runs.
    """
    existing = get_smart_collection(handle, token, store)
    if existing:
        return "existing", existing
    status, resp = create_smart_collection(title, handle, rules, disjunctive, sort_order, token=token, store=store)
    if status in (200, 201):
        return "created", resp.get("smart_collection", resp)
    return "error", resp


def delete_custom_collection(collection_id, token, store=STORE):
    url = f"https://{store}/admin/api/{API_VERSION}/custom_collections/{collection_id}.json"
    return _delete(url, token)


def recreate_custom_collection(entry, token, store=STORE):
    """Recreate a custom collection from a backup entry (for rollback)."""
    url = f"https://{store}/admin/api/{API_VERSION}/custom_collections.json"
    body = {
        "custom_collection": {
            "title": entry["title"],
            "handle": entry["handle"],
            "body_html": entry.get("body_html", ""),
            "sort_order": entry.get("sort_order", "best-selling"),
            "published": entry.get("published", True),
        }
    }
    return _post(url, body, token)


def delete_smart_collection(collection_id, token, store=STORE):
    url = f"https://{store}/admin/api/{API_VERSION}/smart_collections/{collection_id}.json"
    return _delete(url, token)


# ── Backup ───────────────────────────────────────────────────────────────────

def backup_collections(handles, token, ts):
    """Snapshot current state of all targetted custom collections."""
    backup = []
    for handle in handles:
        time.sleep(0.35)  # stay well under Shopify 2 req/s burst limit
        coll = get_custom_collection(handle, token)
        if coll:
            product_ids = get_collection_product_ids(coll["id"], token)
            time.sleep(0.35)
            backup.append({
                "handle":       handle,
                "id":           coll["id"],
                "title":        coll.get("title", ""),
                "body_html":    coll.get("body_html", ""),
                "sort_order":   coll.get("sort_order", "best-selling"),
                "published":    bool(coll.get("published_at")),
                "product_count": len(product_ids),
                "product_ids":  product_ids,
            })
        else:
            # Not a custom collection — might already be smart or missing
            smart = get_smart_collection(handle, token)
            if smart:
                backup.append({
                    "handle":   handle,
                    "id":       None,
                    "title":    smart.get("title", ""),
                    "kind":     "smart",
                    "product_count": get_smart_collection_product_count(smart["id"], token),
                })
            else:
                backup.append({"handle": handle, "id": None, "kind": "missing"})

    path = Path(f"data/backups/{ts}/collections-pre-migration.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(backup, indent=2))
    print(f"  Backup saved: {path}")
    return path


# ── Migration logic ──────────────────────────────────────────────────────────

def migrate_one(handle, rule_tag, token, dry_run):
    """
    Convert a single custom collection to a smart collection.
    Returns a result dict with keys: handle, status, pre_count, post_count, error.
    """
    result = {"handle": handle, "rule_tag": rule_tag, "status": "?", "pre_count": 0, "post_count": 0, "error": ""}

    # 1. Get current custom collection
    coll = get_custom_collection(handle, token)
    if not coll:
        result["status"] = "SKIP_MISSING"
        result["error"] = "custom collection not found"
        return result

    pre_count = get_collection_product_count(coll["id"], token)
    result["pre_count"] = pre_count

    if dry_run:
        result["status"] = "DRY_RUN"
        return result

    # 2. Create smart collection with same handle (must delete custom first due to handle uniqueness)
    title      = coll.get("title", handle)
    body_html  = coll.get("body_html", "")
    sort_order = coll.get("sort_order", "best-selling")
    rules = [{"column": "tag", "relation": "equals", "condition": rule_tag}]

    # Check if a smart collection with this handle already exists
    existing_smart = get_smart_collection(handle, token)
    if existing_smart:
        result["status"] = "ALREADY_SMART"
        result["post_count"] = get_smart_collection_product_count(existing_smart["id"], token)
        return result

    # 3. Delete custom collection
    del_status, _ = delete_custom_collection(coll["id"], token)
    if del_status not in (200, 204):
        result["status"] = "ERR_DELETE"
        result["error"] = f"DELETE returned {del_status}"
        return result

    time.sleep(0.5)  # brief pause after delete

    # 4. Create smart collection with the same handle
    status, resp = create_smart_collection(
        title=title,
        handle=handle,
        rules=rules,
        sort_order=sort_order,
        token=token,
        body_html=body_html,
    )
    if status not in (200, 201):
        result["status"] = "ERR_CREATE"
        result["error"] = f"POST returned {status}: {str(resp)[:120]}"
        return result

    new_coll = resp.get("smart_collection", {})
    time.sleep(1.0)  # allow Shopify to index the new collection

    post_count = get_smart_collection_product_count(new_coll.get("id", 0), token)
    result["post_count"] = post_count
    result["smart_id"]   = new_coll.get("id")

    # 5. Regression check: post_count must be >= pre_count * 0.90
    threshold = pre_count * 0.90
    if post_count < threshold:
        result["status"] = "REGRESSION"
        result["error"] = (
            f"product count dropped from {pre_count} to {post_count} "
            f"(>{(1 - post_count / max(pre_count,1)) * 100:.0f}% drop)"
        )
    else:
        result["status"] = "OK"

    return result


def migrate_batch(handles, token, dry_run):
    """Process a batch of handles and return results."""
    results = []
    for handle in handles:
        rule_tag = HANDLE_TO_RULE.get(handle)

        if rule_tag is None:
            results.append({"handle": handle, "status": "SKIP_NO_MAPPING", "pre_count": 0, "post_count": 0, "error": "not in HANDLE_TO_RULE"})
            continue

        if rule_tag == NEEDS_ENRICHMENT:
            results.append({"handle": handle, "rule_tag": "NEEDS_ENRICHMENT", "status": "SKIP_ENRICHMENT", "pre_count": 0, "post_count": 0,
                            "error": "No unique tag — add sub-type tags to products first"})
            continue

        r = migrate_one(handle, rule_tag, token, dry_run)
        results.append(r)

        # Throttle API calls
        if not dry_run:
            time.sleep(0.5)

    return results


# ── Rollback ─────────────────────────────────────────────────────────────────

def rollback(backup_path: Path, token: str, dry_run: bool):
    """Restore custom collections from a backup file."""
    with open(backup_path) as f:
        backup = json.load(f)

    print(f"\nROLLBACK from {backup_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE — writing to Shopify'}\n")

    for entry in backup:
        handle = entry["handle"]
        kind   = entry.get("kind", "custom")

        if kind == "missing":
            print(f"  SKIP  {handle}  — was missing before migration")
            continue
        if kind == "smart":
            print(f"  SKIP  {handle}  — was already smart before migration")
            continue

        # The current state should be a smart collection (after migration)
        smart = get_smart_collection(handle, token)
        if smart:
            if dry_run:
                print(f"  DRY   {handle}  — would DELETE smart id={smart['id']} then RECREATE custom")
            else:
                # Delete the smart collection
                s, _ = delete_smart_collection(smart["id"], token)
                time.sleep(0.5)
                if s not in (200, 204):
                    print(f"  ERR   {handle}  — could not delete smart collection (status={s})")
                    continue
                # Recreate the custom collection
                cs, cr = recreate_custom_collection(entry, token)
                if cs in (200, 201):
                    new_id = cr.get("custom_collection", {}).get("id", "?")
                    print(f"  OK    {handle}  — smart deleted, custom recreated (id={new_id})")
                    # Restore product memberships
                    product_ids = entry.get("product_ids", [])
                    if product_ids and new_id != "?":
                        time.sleep(0.5)
                        restored = restore_collects(int(new_id), product_ids, token)
                        print(f"        — restored {restored}/{len(product_ids)} product collects")
                else:
                    print(f"  ERR   {handle}  — smart deleted but custom create failed ({cs}): {str(cr)[:80]}")
        else:
            # Already reverted or never migrated
            custom = get_custom_collection(handle, token)
            if custom:
                print(f"  SKIP  {handle}  — custom already exists (no smart found)")
            else:
                if dry_run:
                    print(f"  DRY   {handle}  — would RECREATE custom (neither custom nor smart found)")
                else:
                    cs, cr = recreate_custom_collection(entry, token)
                    if cs in (200, 201):
                        print(f"  OK    {handle}  — recreated custom collection")
                    else:
                        print(f"  ERR   {handle}  — recreate failed ({cs}): {str(cr)[:80]}")

        if not dry_run:
            time.sleep(0.5)

    print("\nRollback complete." if not dry_run else "\nDry-run complete. Pass --live to apply.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Migrate BBI custom collections → smart collections. Default: DRY RUN."
    )
    parser.add_argument("--live", action="store_true", help="Actually write to Shopify.")
    parser.add_argument("--batch", metavar="HANDLE", help="Migrate only the named collection (for smoke testing).")
    parser.add_argument("--rollback", metavar="BACKUP_FILE", help="Restore from backup JSON.")
    args = parser.parse_args()

    # Load credentials
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path) as f:
        env = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.startswith("#"))
    token = env.get("SHOPIFY_TOKEN", "")
    if not token:
        sys.exit("ERROR: SHOPIFY_TOKEN not found in .env")

    Path("data/backups").mkdir(parents=True, exist_ok=True)
    Path("data/logs").mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── Rollback mode ────────────────────────────────────────────────────────
    if args.rollback:
        bpath = Path(args.rollback)
        if not bpath.exists():
            sys.exit(f"ERROR: backup file not found: {bpath}")
        rollback(bpath, token, dry_run=not args.live)
        return

    # ── Migration mode ───────────────────────────────────────────────────────
    all_handles = list(HANDLE_TO_RULE.keys())

    if args.batch:
        target_handles = [args.batch]
        print(f"\nSmoke-test batch: {args.batch}")
    else:
        target_handles = all_handles
        print(f"\nFull migration: {len(target_handles)} collections")

    print(f"Mode  : {'LIVE — writing to Shopify' if args.live else 'DRY RUN — no API calls'}")
    print(f"Store : {STORE}\n")

    # Backup before any writes (even for dry-run, so rollback file is available)
    backup_path = backup_collections(target_handles, token, ts)

    # Allow Shopify rate-limit bucket to refill after backup API calls
    print("  Waiting 3s for rate-limit recovery...")
    time.sleep(3)

    # Split into batches of BATCH_SIZE
    batches = [target_handles[i:i+BATCH_SIZE] for i in range(0, len(target_handles), BATCH_SIZE)]

    all_results = []
    halted = False

    for batch_i, batch in enumerate(batches, 1):
        print(f"\n── Batch {batch_i}/{len(batches)} ({len(batch)} collections) ──")
        results = migrate_batch(batch, token, dry_run=not args.live)
        all_results.extend(results)

        # Regression check: halt if any REGRESSION in live mode
        regressions = [r for r in results if r["status"] == "REGRESSION"]
        if regressions and args.live:
            print(f"\n⚠️  REGRESSION DETECTED in batch {batch_i}! Halting.")
            for r in regressions:
                print(f"  {r['handle']}: {r['error']}")
            print(f"  Rollback with: python3 scripts/migrate-to-smart-collections.py --rollback {backup_path} --live")
            halted = True
            break

        # Print batch summary
        ok  = sum(1 for r in results if r["status"] == "OK")
        dr  = sum(1 for r in results if r["status"] == "DRY_RUN")
        ski = sum(1 for r in results if r["status"].startswith("SKIP"))
        err = sum(1 for r in results if r["status"].startswith("ERR"))
        print(f"  Batch {batch_i} done: ok={ok}, dry_run={dr}, skipped={ski}, errors={err}")

        for r in results:
            flag = "✅" if r["status"] in ("OK", "DRY_RUN", "ALREADY_SMART") else "⏭" if r["status"].startswith("SKIP") else "❌"
            rule = r.get("rule_tag", "—")
            print(f"  {flag} {r['handle']:<45} {r['status']:<20} rule={rule}  pre={r.get('pre_count','-')}  post={r.get('post_count','-')}")

    # Save log
    log_path = Path(f"data/logs/migrate-smart-{ts}.json")
    log_path.write_text(json.dumps(all_results, indent=2))

    # Summary
    total_ok  = sum(1 for r in all_results if r["status"] == "OK")
    total_dry = sum(1 for r in all_results if r["status"] == "DRY_RUN")
    total_ski = sum(1 for r in all_results if r["status"].startswith("SKIP"))
    total_err = sum(1 for r in all_results if r["status"].startswith("ERR"))
    total_reg = sum(1 for r in all_results if r["status"] == "REGRESSION")
    needs_enr = sum(1 for r in all_results if r.get("rule_tag") == "NEEDS_ENRICHMENT")

    print(f"\n{'='*60}")
    print(f"Migration {'HALTED' if halted else 'complete'}")
    print(f"  OK            : {total_ok}")
    print(f"  Dry-run shown : {total_dry}")
    print(f"  Skipped       : {total_ski}")
    print(f"    (needs enr.): {needs_enr}  — add sub-type tags then re-run")
    print(f"  Errors        : {total_err}")
    print(f"  Regressions   : {total_reg}")
    print(f"\nLog    : {log_path}")
    print(f"Backup : {backup_path}")
    if args.live and (total_ok > 0 or total_reg > 0):
        print(f"Rollback: python3 scripts/migrate-to-smart-collections.py --rollback {backup_path} --live")


if __name__ == "__main__":
    main()
