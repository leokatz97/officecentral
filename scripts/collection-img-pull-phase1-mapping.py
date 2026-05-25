#!/usr/bin/env python3
"""
COLLECTION-IMG-PULL-1 / Phase 1 — Build 53-slot mapping table.

Parses 9 category templates, extracts hero + tile slots, queries Shopify Admin API
for each collection's lead product (bestseller tag preferred, else first product in
default sort), writes mapping CSV. READ-ONLY against Shopify.

Usage: python3 scripts/collection-img-pull-phase1-mapping.py
"""
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "theme" / "templates"
OUT_CSV = ROOT / "data" / "research" / "collection-img-pull-mapping-2026-05-25.csv"
STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
TOKEN = os.environ.get("SHOPIFY_TOKEN")
if not TOKEN:
    print("ERROR: SHOPIFY_TOKEN not set in env", file=sys.stderr)
    sys.exit(1)

RATE_LIMIT_SEC = 0.45

TEMPLATE_HANDLES = [
    "seating",
    "desks",
    "tables",
    "storage",
    "boardroom",
    "accessories",
    "panels-room-dividers",
    "ergonomic-products",
    "business-furniture",
]


def api_get(path):
    """GET against the Shopify Admin API. Returns dict. Rate-limits 0.45s."""
    url = f"https://{STORE}/admin/api/{API_VERSION}/{path}"
    req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        body = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP {e.code} on {path}: {body[:200]}", file=sys.stderr)
        raise
    finally:
        time.sleep(RATE_LIMIT_SEC)
    return data


def fetch_collection_by_handle(handle):
    """Returns collection dict (smart or custom) with id/title, or None."""
    # Try smart first, fall back to custom
    for ctype in ("smart_collections", "custom_collections"):
        path = f"{ctype}.json?handle={urllib.parse.quote(handle)}"
        data = api_get(path)
        if data and data.get(ctype):
            return data[ctype][0], ctype
    return None, None


def fetch_collection_products(collection_id, limit=50):
    """Returns list of products in the collection, default sort order."""
    path = f"collections/{collection_id}/products.json?limit={limit}"
    data = api_get(path)
    if not data:
        return []
    return data.get("products", [])


def pick_lead_product(products):
    """Find product tagged 'bestseller' with at least one image, else first product
    with an image, else None. (Leo HALT 1 decision 2026-05-25: skip image-less leads.)"""
    if not products:
        return None, "SKIP_empty"
    # First pass: bestseller WITH images
    for p in products:
        tags = [t.strip().lower() for t in (p.get("tags") or "").split(",")]
        if "bestseller" in tags and (p.get("images") or []):
            return p, "bestseller"
    # Second pass: first product WITH images in default sort
    for p in products:
        if p.get("images") or []:
            return p, "first_in_collection"
    return None, "SKIP_no_images_in_collection"


def parse_templates():
    """Walk 9 templates, return list of slot dicts (without lead-product data yet)."""
    slots = []
    for thandle in TEMPLATE_HANDLES:
        tpath = TEMPLATES_DIR / f"collection.{thandle}.json"
        with open(tpath) as f:
            tdata = json.load(f)
        sec = tdata["sections"]["ds-cc-base"]
        # Hero slot
        slot_id = f"{thandle}-hero"
        slots.append({
            "slot_id": slot_id,
            "slot_type": "hero",
            "parent_template": f"collection.{thandle}.json",
            "block_key": None,
            "collection_handle": thandle,
            "current_image": sec["settings"].get("hero_image", ""),
        })
        # Tile slots
        for bkey in sec.get("block_order", []):
            blk = sec["blocks"].get(bkey)
            if not blk or blk.get("type") != "tile":
                continue
            link = blk["settings"].get("link", "")
            # Extract handle from /collections/<handle>
            if "/collections/" in link:
                chandle = link.split("/collections/")[-1].split("?")[0].split("#")[0].strip("/")
            else:
                chandle = ""
            slots.append({
                "slot_id": f"{thandle}-tile-{bkey.replace('tile-', '')}",
                "slot_type": "tile",
                "parent_template": f"collection.{thandle}.json",
                "block_key": bkey,
                "collection_handle": chandle,
                "current_image": blk["settings"].get("image", ""),
            })
    return slots


def classify_current_image(img_uri):
    """Categorize current image: placeholder / pagepic_be1409d / bucket_b / legacy_stocky / empty."""
    if not img_uri:
        return "empty"
    if img_uri.startswith("shopify://shop_images/"):
        fname = img_uri.split("/")[-1].lower()
        # Bucket B (homepage-only — none of these slots) and PAGE-IMG-1 (page heroes only)
        # don't apply to category collection templates. All current refs are Avada-era stock.
        # be1409d filenames are like "page-images/*" with hash suffixes from fal.ai.
        if any(token in fname for token in ("-space.", "-product.", "oci-", "inspiration-",
                                              "lounge-", "mattamy", "pods-", "subject-areas-")):
            return "legacy_stocky"
        return "legacy_stocky"
    return "unknown"


def main():
    print("Phase 1 — parsing 9 category templates...")
    slots = parse_templates()
    print(f"  parsed {len(slots)} slots: {sum(1 for s in slots if s['slot_type']=='hero')} hero + "
          f"{sum(1 for s in slots if s['slot_type']=='tile')} tile")

    # Cache collection lookups (some tiles point at the same handle as a hero)
    coll_cache = {}
    print(f"\nFetching collection + lead product per handle (rate-limited {RATE_LIMIT_SEC}s)...")
    for i, slot in enumerate(slots, 1):
        h = slot["collection_handle"]
        if not h:
            slot["collection_title"] = ""
            slot["lead_product_id"] = ""
            slot["lead_product_handle"] = ""
            slot["lead_product_title"] = ""
            slot["lead_product_image_src"] = ""
            slot["selection_reason"] = "SKIP_no_handle"
            continue
        if h not in coll_cache:
            print(f"  [{i:2d}/{len(slots)}] {slot['slot_id']:55s} → /collections/{h}")
            coll, _ctype = fetch_collection_by_handle(h)
            if not coll:
                coll_cache[h] = {
                    "collection_id": None, "collection_title": "",
                    "lead_product": None, "reason": "SKIP_collection_not_found",
                }
            else:
                products = fetch_collection_products(coll["id"], limit=50)
                lead, reason = pick_lead_product(products)
                coll_cache[h] = {
                    "collection_id": coll["id"],
                    "collection_title": coll.get("title", ""),
                    "lead_product": lead,
                    "reason": reason,
                }
        else:
            print(f"  [{i:2d}/{len(slots)}] {slot['slot_id']:55s} → /collections/{h} (cached)")

        c = coll_cache[h]
        slot["collection_title"] = c["collection_title"]
        slot["selection_reason"] = c["reason"]
        lead = c["lead_product"]
        if lead:
            slot["lead_product_id"] = lead["id"]
            slot["lead_product_handle"] = lead.get("handle", "")
            slot["lead_product_title"] = lead.get("title", "")
            imgs = lead.get("images") or []
            slot["lead_product_image_src"] = imgs[0]["src"] if imgs else ""
            if not slot["lead_product_image_src"]:
                slot["selection_reason"] = "SKIP_lead_no_image"
        else:
            slot["lead_product_id"] = ""
            slot["lead_product_handle"] = ""
            slot["lead_product_title"] = ""
            slot["lead_product_image_src"] = ""

    # Compute target_spec, current_image_status, action
    for slot in slots:
        slot["target_spec"] = "1920x1080" if slot["slot_type"] == "hero" else "1200x900"
        slot["current_image_status"] = classify_current_image(slot["current_image"])
        if slot["selection_reason"].startswith("SKIP_"):
            slot["action"] = "SKIP"
        elif slot["current_image_status"] in ("legacy_stocky", "empty", "unknown"):
            slot["action"] = "REPLACE"
        elif slot["current_image_status"] == "bucket_b_populated":
            slot["action"] = "KEEP"
        else:
            slot["action"] = "REPLACE"

    # Write CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "slot_id", "slot_type", "parent_template", "block_key",
        "collection_handle", "collection_title",
        "lead_product_id", "lead_product_handle", "lead_product_title",
        "lead_product_image_src", "selection_reason",
        "target_spec", "current_image", "current_image_status", "action",
    ]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for slot in slots:
            w.writerow({k: slot.get(k, "") for k in cols})

    # Summary
    total = len(slots)
    replace = sum(1 for s in slots if s["action"] == "REPLACE")
    keep = sum(1 for s in slots if s["action"] == "KEEP")
    skip = sum(1 for s in slots if s["action"] == "SKIP")
    bestseller = sum(1 for s in slots if s["selection_reason"] == "bestseller")
    first = sum(1 for s in slots if s["selection_reason"] == "first_in_collection")

    print(f"\n{'='*72}")
    print(f"PHASE 1 SUMMARY  →  {OUT_CSV.relative_to(ROOT)}")
    print(f"{'='*72}")
    print(f"  Total slots:                {total}")
    print(f"  REPLACE:                    {replace}")
    print(f"  KEEP (bucket B):            {keep}")
    print(f"  SKIP (empty/missing/blank): {skip}")
    print(f"  Bestseller-driven picks:    {bestseller}")
    print(f"  First-in-collection picks:  {first}")
    print()
    print("First 10 rows:")
    for s in slots[:10]:
        print(f"  {s['slot_id']:50s} | {s['action']:7s} | {s['selection_reason']:25s} | "
              f"{s['lead_product_handle'][:35]:35s}")
    if skip > 0:
        print(f"\nSKIP rows ({skip}):")
        for s in slots:
            if s["action"] == "SKIP":
                print(f"  {s['slot_id']:50s} | reason={s['selection_reason']:30s} | "
                      f"handle={s['collection_handle']}")


if __name__ == "__main__":
    main()
