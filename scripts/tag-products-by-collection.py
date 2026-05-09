"""
tag-products-by-collection.py  (BATCH-4)

For 8 smart collections that show 0 products, tag all products that *should*
be in that collection so Shopify's smart-collection rules match them.

Collection → tag mapping
  all-boardroom      → type:boardroom
  all-ergonomic      → type:ergonomic
  all-panels         → type:panels
  all-quiet-spaces   → type:quiet-spaces
  keilhauer          → brand:keilhauer
  global-teknion     → brand:global-teknion
  ergocentric        → brand:ergocentric
  oecm-eligible      → oecm-eligible

Strategy: each smart collection's products are fetched via the Shopify
/products.json endpoint filtered by collection_id. This returns every product
already matched by the collection's existing rules (if any). Because these
collections currently have 0 products, we use the INTENDED rule's tag to
identify candidates instead: we search products by matching vendor, type, or
a pre-existing partial tag — see COLLECTION_CRITERIA below.

For brand collections (keilhauer, global-teknion, ergocentric) we match
products whose `vendor` field contains the brand name.
For type collections we match products whose `product_type` or existing
tags contain the type keyword.

Backup: before any write, original tags are saved to
  data/backups/<timestamp>/tag-backup-<handle>.json

Flags
  --dry-run  (default) — print what would change, no writes
  --live     — apply changes
  --rollback data/backups/<ts>/tag-backup-<handle>.json  — restore original tags
  --collection <handle>  — target one collection only (for smoke test)

Reports (printed to stdout):
  products found / already-tagged (skip) / would-tag (dry) or tagged (live) / errors

Usage
  python3 scripts/tag-products-by-collection.py                      # dry run all
  python3 scripts/tag-products-by-collection.py --collection keilhauer
  python3 scripts/tag-products-by-collection.py --live
  python3 scripts/tag-products-by-collection.py --rollback data/backups/20260509_../tag-backup-keilhauer.json --live
"""
import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime

TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
STORE = os.environ.get("SHOPIFY_STORE", "office-central-online.myshopify.com")
API_VERSION = "2026-04"

# ---------------------------------------------------------------------------
# Collection → (tag_to_add, search_strategy, search_value)
#   strategy "vendor"  → match products where vendor contains search_value
#   strategy "type"    → match products where product_type contains search_value
#   strategy "tag"     → match products already having a tag containing search_value
# ---------------------------------------------------------------------------
COLLECTION_MAP = {
    "all-boardroom":   ("type:boardroom",      "type",   "boardroom"),
    "all-ergonomic":   ("type:ergonomic",       "type",   "ergonomic"),
    "all-panels":      ("type:panels",          "type",   "panels"),
    "all-quiet-spaces":("type:quiet-spaces",    "type",   "quiet-spaces"),
    "keilhauer":       ("brand:keilhauer",      "vendor", "Keilhauer"),
    "global-teknion":  ("brand:global-teknion", "vendor", "Global"),
    "ergocentric":     ("brand:ergocentric",    "vendor", "ergoCentric"),
    "oecm-eligible":   ("oecm-eligible",        "vendor", ""),   # see note below
}
# Note: oecm-eligible has no simple programmatic rule — it needs manual curation.
# For now it is included but will report 0 candidates and produce a note.
OECM_SKIP_REASON = (
    "oecm-eligible: no automated vendor/type match — products must be curated "
    "manually. Run with --collection oecm-eligible to see this message."
)


def _headers(token: str) -> dict:
    return {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _get(url: str, token: str, retries: int = 5) -> dict:
    req = urllib.request.Request(url, headers=_headers(token))
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 2 ** attempt
                print(f"    [rate-limit] sleeping {wait}s …", flush=True)
                time.sleep(wait)
                continue
            return {"__error": e.code, "__body": e.read().decode()[:400]}
    return {"__error": "timeout"}


def _put(url: str, body: dict, token: str, retries: int = 5):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=_headers(token), method="PUT")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 2 ** attempt
                print(f"    [rate-limit] sleeping {wait}s …", flush=True)
                time.sleep(wait)
                continue
            return e.code, {"error": e.read().decode()[:400]}
    return 0, {"error": "timeout"}


def fetch_all_products(token: str) -> list:
    """Fetch every product (id, title, vendor, product_type, tags) via pagination."""
    products = []
    url = (
        f"https://{STORE}/admin/api/{API_VERSION}/products.json"
        f"?limit=250&fields=id,title,vendor,product_type,tags"
    )
    while url:
        data = _get(url, token)
        if "__error" in data:
            print(f"  ERROR fetching products: {data}", file=sys.stderr)
            break
        batch = data.get("products", [])
        products.extend(batch)
        if len(batch) < 250:
            break
        last_id = batch[-1]["id"]
        url = (
            f"https://{STORE}/admin/api/{API_VERSION}/products.json"
            f"?limit=250&fields=id,title,vendor,product_type,tags&since_id={last_id}"
        )
    # Deduplicate by id (can occur at page boundaries)
    seen = set()
    unique = []
    for p in products:
        if p["id"] not in seen:
            seen.add(p["id"])
            unique.append(p)
    return unique


def candidates_for_collection(handle: str, products: list) -> list:
    """Return products that match the collection's identification strategy.

    For vendor-based brand collections: searches vendor field, then title, then tags.
    For type-based collections: searches product_type field and existing tags.
    Reports a DATA-GAP warning when no matches are found.
    """
    if handle not in COLLECTION_MAP:
        return []
    tag_to_add, strategy, search_val = COLLECTION_MAP[handle]
    if handle == "oecm-eligible":
        print(f"  NOTE: {OECM_SKIP_REASON}")
        return []

    matched = []
    sv_lower = search_val.lower()
    for p in products:
        existing_tags = [t.strip() for t in p.get("tags", "").split(",") if t.strip()]
        if strategy == "vendor":
            vendor_match = sv_lower in p.get("vendor", "").lower()
            title_match  = sv_lower in p.get("title", "").lower()
            tag_match    = any(sv_lower in t.lower() for t in existing_tags)
            if vendor_match or title_match or tag_match:
                matched.append(p)
        elif strategy == "type":
            type_match = sv_lower in p.get("product_type", "").lower()
            tag_match  = any(sv_lower in t.lower() for t in existing_tags)
            if type_match or tag_match:
                matched.append(p)

    if not matched:
        print(
            f"  DATA GAP: 0 products found for '{search_val}' via "
            f"{'vendor+title+tags' if strategy == 'vendor' else 'product_type+tags'}. "
            f"Products have not been assigned vendor/type metadata yet. "
            f"Manual curation needed — assign vendor or add a partial tag, then re-run."
        )
    return matched


def backup_tags(products: list, handle: str, ts: str) -> Path:
    backup_dir = Path(f"data/backups/{ts}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    path = backup_dir / f"tag-backup-{handle}.json"
    records = [{"id": p["id"], "title": p["title"], "tags": p["tags"]} for p in products]
    path.write_text(json.dumps(records, indent=2))
    return path


def add_tag_to_product(product: dict, tag: str, token: str, dry_run: bool) -> str:
    """Add tag to product. Returns 'already_tagged', 'tagged', 'dry_run', or 'error:<msg>'."""
    existing = [t.strip() for t in product.get("tags", "").split(",") if t.strip()]
    if tag in existing:
        return "already_tagged"
    if dry_run:
        return "dry_run"
    new_tags = existing + [tag]
    url = f"https://{STORE}/admin/api/{API_VERSION}/products/{product['id']}.json"
    status, resp = _put(url, {"product": {"id": product["id"], "tags": ", ".join(new_tags)}}, token)
    if status == 200:
        return "tagged"
    return f"error:{status} {resp.get('error','')}"


def run_rollback(backup_path: Path, token: str, dry_run: bool):
    if not backup_path.exists():
        print(f"ERROR: backup file not found: {backup_path}", file=sys.stderr)
        sys.exit(1)
    records = json.loads(backup_path.read_text())
    print(f"Rolling back {len(records)} products from {backup_path}")
    ok = err = 0
    for rec in records:
        if dry_run:
            print(f"  [dry-run] would restore id={rec['id']} tags='{rec['tags']}'")
            ok += 1
            continue
        url = f"https://{STORE}/admin/api/{API_VERSION}/products/{rec['id']}.json"
        status, resp = _put(url, {"product": {"id": rec["id"], "tags": rec["tags"]}}, token)
        if status == 200:
            ok += 1
        else:
            print(f"  ERROR {rec['id']}: {status} {resp.get('error','')}", file=sys.stderr)
            err += 1
    print(f"Rollback complete: {ok} ok, {err} errors")


def main():
    parser = argparse.ArgumentParser(
        description="Tag products for 8 smart collections. Default: DRY RUN."
    )
    parser.add_argument(
        "--live", action="store_true",
        help="Apply tag writes to Shopify (default: dry run)."
    )
    parser.add_argument(
        "--collection", metavar="HANDLE",
        help="Target one collection handle only (for smoke testing)."
    )
    parser.add_argument(
        "--rollback", metavar="BACKUP_PATH",
        help="Path to a tag-backup-<handle>.json file to restore from."
    )
    args = parser.parse_args()
    dry_run = not args.live

    if not TOKEN:
        print("ERROR: SHOPIFY_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    # ── Rollback mode ────────────────────────────────────────────────────────
    if args.rollback:
        run_rollback(Path(args.rollback), TOKEN, dry_run)
        return

    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"tag-products-by-collection.py  [{mode}]")
    print(f"Store: {STORE}\n")

    # ── Determine collections to process ─────────────────────────────────────
    targets = [args.collection] if args.collection else list(COLLECTION_MAP.keys())
    invalid = [h for h in targets if h not in COLLECTION_MAP]
    if invalid:
        print(f"ERROR: unknown collection handles: {invalid}", file=sys.stderr)
        print(f"Valid handles: {list(COLLECTION_MAP.keys())}", file=sys.stderr)
        sys.exit(1)

    # ── Fetch all products once ───────────────────────────────────────────────
    print("Fetching all products …", flush=True)
    all_products = fetch_all_products(TOKEN)
    print(f"  {len(all_products)} products loaded\n")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    grand_found = grand_skip = grand_tag = grand_err = 0

    for handle in targets:
        tag_to_add = COLLECTION_MAP[handle][0]
        print(f"── {handle}  →  tag: {tag_to_add}")

        matched = candidates_for_collection(handle, all_products)
        if not matched and handle != "oecm-eligible":
            print(f"  0 candidate products found (no vendor/type match for '{COLLECTION_MAP[handle][2]}')\n")
            continue

        # Back up original tags before any writes
        if not dry_run and matched:
            bp = backup_tags(matched, handle, ts)
            print(f"  Backup: {bp}")

        found = len(matched)
        skip = tag = err_count = 0

        for p in matched:
            result = add_tag_to_product(p, tag_to_add, TOKEN, dry_run)
            if result == "already_tagged":
                skip += 1
            elif result in ("tagged", "dry_run"):
                tag += 1
                verb = "would-tag" if dry_run else "tagged"
                print(f"  {verb}: [{p['id']}] {p['title'][:60]}")
            else:
                err_count += 1
                print(f"  ERROR [{p['id']}] {p['title'][:50]}: {result}", file=sys.stderr)

        grand_found += found
        grand_skip  += skip
        grand_tag   += tag
        grand_err   += err_count

        print(f"  found={found}  already-tagged(skip)={skip}  "
              f"{'would-tag' if dry_run else 'tagged'}={tag}  errors={err_count}\n")

    print("─" * 60)
    print(f"TOTAL  found={grand_found}  skip={grand_skip}  "
          f"{'would-tag' if dry_run else 'tagged'}={grand_tag}  errors={grand_err}")
    if dry_run:
        print("\nThis was a DRY RUN. Pass --live to apply changes.")


if __name__ == "__main__":
    main()
