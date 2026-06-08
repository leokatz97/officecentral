"""The four tools that make up the entire surface Steve can touch.

resolve_sku       (read)   — brand + routing + Google category, or needs-leo
onboard_product   (write)  — create a DRAFT, fully enriched, guards enforced
create_collection (write)  — smart|manual, optional sub-collection placement
verify_product    (read)   — current state + born-feed-ready verdict

These are plain functions returning JSON-serializable dicts so the local test
harness can call them directly without the MCP transport. server.py registers
them as MCP tools. All guards run server-side here, regardless of caller input.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from . import config, guards
from .audit import AuditLog
from .references import ReferenceData
from .shopify_client import ShopifyClient

# Singletons (reference data loaded once; audit log per-process).
_REFS: Optional[ReferenceData] = None
_AUDIT: Optional[AuditLog] = None


def get_refs() -> ReferenceData:
    global _REFS
    if _REFS is None:
        _REFS = ReferenceData()
    return _REFS


def get_audit() -> AuditLog:
    global _AUDIT
    if _AUDIT is None:
        _AUDIT = AuditLog()
    return _AUDIT


def _client(dry_run: bool) -> ShopifyClient:
    return ShopifyClient(dry_run=dry_run, audit=get_audit())


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ════════════════════════════════════════════════════════════════════════════
# resolve_sku
# ════════════════════════════════════════════════════════════════════════════
def resolve_sku(sku: str) -> dict:
    refs = get_refs()
    r = refs.resolve_sku(sku)
    if r.status != "resolved":
        return {"status": "needs-leo", "sku": sku, "reason": r.reason,
                "matched_prefix": r.matched_prefix}

    collections = []
    for tc in r.target_collections:
        entry = {"handle": tc.get("handle"), "membership": tc.get("membership"),
                 "title": tc.get("title"), "collection_id": tc.get("collection_id")}
        if tc.get("membership") == "SMART" and tc.get("smart_rules"):
            tags = [rule["condition"] for rule in tc["smart_rules"]
                    if rule.get("column") == "tag" and rule.get("relation") == "equals"]
            entry["required_tags"] = tags
        collections.append(entry)

    return {
        "status": "resolved",
        "sku": sku,
        "matched_prefix": r.matched_prefix,
        "brand_key": r.brand_key,
        "manufacturer": r.manufacturer,
        "brand_tag": r.brand_tag,
        "sub_brands": r.sub_brands,
        "routing_tag_template": r.routing_tag_template,
        "collections_by_type": r.collections_by_type,
        "routing_collections": collections,
        "default_google_product_category": r.default_google_product_category,
        "manufacturer_defaults": r.manufacturer_defaults,
    }


# ════════════════════════════════════════════════════════════════════════════
# onboard_product
# ════════════════════════════════════════════════════════════════════════════
def onboard_product(
    *,
    sku: str,
    title: str,
    description: str = "",
    seo_title: str = "",
    seo_description: str = "",
    price: Optional[str] = None,
    quote_only: bool = False,
    product_type: str = "",
    vendor: Optional[str] = None,
    specs: Optional[list] = None,
    feed: Optional[dict] = None,
    images: Optional[list] = None,
    collections: Optional[list] = None,
    extra_tags: Optional[list] = None,
    made_in_canada: Optional[dict] = None,
    warranty: Optional[dict] = None,
    dry_run: bool = False,
) -> dict:
    refs = get_refs()
    client = _client(dry_run)
    report: dict = {"tool": "onboard_product", "sku": sku, "dry_run": dry_run,
                    "status": "ok", "needs_leo": [], "writes": {}, "warnings": []}

    # ── Guard 1: re-resolve brand from SKU prefix (prefix wins) ─────────────
    resolution = guards.resolve_brand(refs, sku)
    if resolution.status != "resolved":
        return {**report, "status": "rejected", "reason": resolution.reason,
                "needs_leo": [resolution.reason]}
    report["resolved_brand"] = {"manufacturer": resolution.manufacturer,
                                "brand_tag": resolution.brand_tag,
                                "matched_prefix": resolution.matched_prefix}

    # ── Guard 2: vendor must equal resolved manufacturer; reject BBI ────────
    v = guards.check_vendor(resolution, vendor)
    if not v["ok"]:
        return {**report, "status": "rejected", "reason": v["error"]}
    vendor_final = v["vendor"]

    # ── Guard 3: duplicate guard — does a product with this SKU exist? ──────
    dup = client.find_product_by_sku(sku)
    if dup:
        return {**report, "status": "already_exists",
                "reason": f"a product with SKU {sku!r} already exists; not creating a duplicate",
                "existing_product": dup}

    # ── Resolve requested collections live; derive tags from smart rules ────
    requested_handles = list(collections or [])
    coll_plan = []  # each: {handle, membership, collection_id, required_tags, status}
    derived_tags: list[str] = []
    for h in requested_handles:
        # Prefer the pre-resolved snapshot entry; fall back to a live lookup.
        snap = next((tc for tc in resolution.target_collections if tc.get("handle") == h), None)
        smart = client.get_smart_collection_rule(h)
        if smart:
            tags, notes = guards.required_tags_from_rule(smart)
            derived_tags.extend(tags)
            coll_plan.append({"handle": h, "membership": "smart",
                              "collection_id": smart.get("id"),
                              "required_tags": tags, "unsatisfiable": notes,
                              "status": "will-tag"})
        else:
            found = client.find_collection(h, None)
            if found and found["type"] == "manual":
                coll_plan.append({"handle": h, "membership": "manual",
                                  "collection_id": found["id"], "status": "will-collect"})
            elif found:
                coll_plan.append({"handle": h, "membership": found["type"],
                                  "collection_id": found["id"], "status": "exists"})
            else:
                coll_plan.append({"handle": h, "membership": "missing",
                                  "status": "missing-reported-not-created"})
                report["needs_leo"].append(f"collection '{h}' does not exist — reported, not created")

    # ── Build final tag set ─────────────────────────────────────────────────
    tags = []
    for t in [resolution.brand_tag, *derived_tags, *(extra_tags or [])]:
        if t and t not in tags:
            tags.append(t)
    if quote_only and "quote-only" not in tags:
        tags.append("quote-only")
    report["tags_planned"] = tags

    # ── Guard 4: specs require source_url ───────────────────────────────────
    kept_specs, dropped_specs = guards.filter_specs(specs or [])
    report["specs"] = {"written": [s["name"] for s in kept_specs],
                       "dropped": dropped_specs}

    # ── Guard 5: confirmed_by_steve gates ───────────────────────────────────
    mic, mic_note = guards.gate_confirmed(made_in_canada, "made_in_canada")
    war, war_note = guards.gate_confirmed(warranty, "warranty")
    for n in (mic_note, war_note):
        if n:
            report["warnings"].append(n)

    # ── Feed attributes ─────────────────────────────────────────────────────
    feed = feed or {}
    google_cat = feed.get("google_product_category") or resolution.default_google_product_category
    identifier = feed.get("identifier")
    identifier_exists = bool(feed.get("identifier_exists"))
    condition = feed.get("condition") or config.DEFAULT_CONDITION

    # ── Image pre-checks (>=500px) ──────────────────────────────────────────
    image_plan = []
    any_image_ok = False
    for idx, img in enumerate(images or []):
        url = img.get("url")
        pos = img.get("position", idx + 1)
        dims = client.image_dimensions(url) if url else None
        if dims is None:
            status, ok = "unverified-size", False
        elif min(dims) >= config.MIN_IMAGE_PX:
            status, ok = "ok", True
        else:
            status, ok = f"too-small-{dims[0]}x{dims[1]}", False
        any_image_ok = any_image_ok or ok
        image_plan.append({"url": url, "position": pos, "alt": img.get("alt", ""),
                           "dimensions": dims, "check": status, "passes": ok})
    report["images"] = image_plan

    # ── Variant (price / quote-only / GTIN barcode) ─────────────────────────
    variant = {"sku": sku, "price": "0.00" if quote_only else (price or "0.00")}
    if identifier:
        variant["barcode"] = str(identifier)

    # ── CREATE (DRAFT only — never publishes) ───────────────────────────────
    created = client.create_product(
        title=title, body_html=description, vendor=vendor_final,
        product_type=product_type, tags=tags, variants=[variant], status="draft")

    if dry_run:
        report["writes"] = {"create_product": created.get("intended"),
                            "planned": client.planned_writes}
        report["collections"] = coll_plan
        report["feed"] = {"google_product_category": google_cat, "condition": condition,
                          "identifier": identifier, "identifier_exists": identifier_exists}
        report["feed_verdict"] = guards.feed_ready_verdict(
            vendor=vendor_final, specs_written=bool(kept_specs), google_category=google_cat,
            identifier=identifier, identifier_exists=identifier_exists,
            image_ok=any_image_ok, price_or_quote=bool(price) or quote_only)
        report["note"] = "DRY RUN — no writes performed. Re-run with dry_run=false to apply."
        return report

    pid = str(created["id"])
    gid = f"gid://shopify/Product/{pid}"
    report["product"] = {"id": pid, "gid": gid, "handle": created.get("handle"),
                         "admin_url": f"{config.ADMIN_BASE}/products/{pid}",
                         "status": created.get("status")}

    # Baseline backup post-create (no pre-existing data for a brand-new product).
    report["backup"] = client.backup_product(pid)

    # SEO + made-in-canada/warranty via productUpdate.
    pfields = {"seo": {"title": seo_title or title, "description": seo_description}}
    client.update_product_fields(gid, pfields)

    # Spec metafields (+ confirmed origin/warranty as spec fields).
    mf = guards.spec_metafields(kept_specs)
    if mic:
        mf.append({"namespace": "specs", "key": "country_of_manufacture",
                   "type": "single_line_text_field", "value": "Canada"})
        mf.append({"namespace": "specs", "key": "made_in_canada",
                   "type": "boolean", "value": "true"})
    if war and war.get("text"):
        mf.append({"namespace": "specs", "key": "warranty",
                   "type": "single_line_text_field", "value": str(war["text"])})
    # Feed metafields.
    if google_cat:
        mf.append({"namespace": "mm-google-shopping", "key": "google_product_category",
                   "type": "single_line_text_field", "value": str(google_cat)})
    mf.append({"namespace": "mm-google-shopping", "key": "condition",
               "type": "single_line_text_field", "value": condition})
    if mf:
        client.set_metafields(gid, mf)
    report["writes"]["metafields"] = [m["namespace"] + "." + m["key"] for m in mf]

    # Images (first passing one becomes featured at position 1).
    attached = []
    for img in image_plan:
        if not img["url"]:
            continue
        res = client.attach_image_by_url(pid, img["url"], img["position"], img["alt"])
        attached.append({"position": img["position"], "passes_500px": img["passes"],
                         "id": res.get("id")})
    report["writes"]["images_attached"] = attached

    # Manual collects (smart handled by tags above).
    for c in coll_plan:
        if c["status"] == "will-collect" and c.get("collection_id"):
            client.add_collect(pid, c["collection_id"])
            c["status"] = "collected"

    # ── READBACK + membership verify ────────────────────────────────────────
    rb = client.get_product_full(gid) or {}
    rb_tags = set(rb.get("tags", []))
    rb_specs = {e["node"]["key"]: e["node"]["value"]
                for e in (rb.get("metafields", {}).get("edges", []))}
    member_handles = {e["node"]["handle"] for e in (rb.get("collections", {}).get("edges", []))}
    checks = {
        "vendor": rb.get("vendor") == vendor_final,
        "product_type": rb.get("productType") == product_type,
        "status_draft": rb.get("status", "").lower() == "draft",
        "tags_superset": set(tags).issubset(rb_tags),
        "specs_present": all(m["key"] in rb_specs for m in guards.spec_metafields(kept_specs)),
    }
    for c in coll_plan:
        if c["membership"] == "smart":
            # Smart membership updates asynchronously; tags are the authoritative signal.
            c["verified"] = "tags-set" if set(c.get("required_tags", [])).issubset(rb_tags) else "tags-missing"
            c["live_member"] = c["handle"] in member_handles
        elif c["membership"] == "manual":
            c["verified"] = c["handle"] in member_handles
    report["collections"] = coll_plan
    report["readback_checks"] = checks
    report["readback_all_ok"] = all(checks.values())

    report["feed"] = {"google_product_category": google_cat, "condition": condition,
                      "identifier": identifier, "identifier_exists": identifier_exists}
    report["feed_verdict"] = guards.feed_ready_verdict(
        vendor=vendor_final, specs_written=bool(kept_specs), google_category=google_cat,
        identifier=identifier, identifier_exists=identifier_exists,
        image_ok=any_image_ok, price_or_quote=bool(price) or quote_only)

    if not report["readback_all_ok"]:
        report["status"] = "partial"
        report["warnings"].append("readback mismatch — see readback_checks; investigate before publish")
    report["manual_steps"] = [
        "DRAFT created — review in admin and click Publish (write_publications not held; this is the review gate).",
    ]
    if quote_only:
        report["manual_steps"].append(
            "quote_only item: set sales-channel exclusion in admin if it should not be buyable.")
    return report


# ════════════════════════════════════════════════════════════════════════════
# create_collection
# ════════════════════════════════════════════════════════════════════════════
def create_collection(
    *,
    name: str,
    type: str = "smart",          # "smart" | "manual"
    rule: Optional[list] = None,  # smart rules: [{column,relation,condition}]
    disjunctive: bool = False,
    products: Optional[list] = None,  # manual: product ids to collect
    sub_collection: bool = False,
    parent_collection: Optional[str] = None,  # handle
    seo_title: str = "",
    seo_description: str = "",
    image: Optional[dict] = None,
    auto_route_brands: Optional[list] = None,
    dry_run: bool = False,
) -> dict:
    client = _client(dry_run)
    refs = get_refs()
    handle = guards.slugify(name)
    report = {"tool": "create_collection", "name": name, "handle": handle,
              "type": type, "dry_run": dry_run, "status": "ok", "warnings": []}

    # ── Duplicate guard ──────────────────────────────────────────────────────
    existing = client.find_collection(handle, name)
    if existing:
        return {**report, "status": "already_exists",
                "reason": f"a collection with handle/name '{name}' already exists",
                "existing_collection": existing}

    # ── Sub-collection requires an existing parent ────────────────────────────
    parent = None
    if sub_collection:
        if not parent_collection:
            return {**report, "status": "rejected",
                    "reason": "sub_collection=true but no parent_collection supplied"}
        parent = client.find_collection(parent_collection, None)
        if not parent:
            return {**report, "status": "rejected",
                    "reason": f"parent collection '{parent_collection}' is missing — refusing to create orphan sub-collection"}

    # ── Create ────────────────────────────────────────────────────────────────
    if type == "smart":
        if not rule:
            return {**report, "status": "rejected", "reason": "smart collection requires a rule"}
        created = client.create_smart_collection(title=name, handle=handle, rules=rule,
                                                 disjunctive=disjunctive, image=image)
    else:
        created = client.create_custom_collection(title=name, handle=handle, image=image)

    if dry_run:
        report["writes"] = {"create": created.get("intended"), "planned": client.planned_writes}
        report["parent_resolved"] = parent
        report["manual_steps"] = [
            "Publish the collection to the Online Store channel in admin "
            "(write_publications not held by the server token)."]
        return report

    cid = created["id"]
    cgid = f"gid://shopify/Collection/{cid}"
    report["collection"] = {"id": cid, "gid": cgid, "handle": handle,
                            "admin_url": f"{config.ADMIN_BASE}/collections/{cid}"}

    # SEO.
    if seo_title or seo_description:
        client.set_collection_seo(cgid, seo_title or name, seo_description)

    # Manual: add products.
    collected = []
    if type == "manual":
        for pid in (products or []):
            client.add_collect(str(pid), cid)
            collected.append(pid)
    report["products_collected"] = collected

    # Nav placement for a sub-collection (reject already handled above).
    if sub_collection:
        nav = client.place_in_nav(menu_handle=config.NAV_MENU_HANDLE,
                                  parent_title=parent["title"],
                                  child_title=name, child_collection_gid=cgid)
        report["nav_placement"] = nav
        if not nav.get("ok"):
            report["warnings"].append(f"nav placement failed: {nav.get('error')}")

    # Register in canonical routing + re-export the snapshot the skill bundles.
    coll_meta = {"handle": handle, "type": type, "collection_id": cid, "title": name,
                 "smart_rules": rule if type == "smart" else None}
    report["reference_update"] = refs.register_route_and_reexport(
        collection_meta=coll_meta, auto_route_brands=auto_route_brands or [],
        date_stamp=_today(), dry_run=False)

    # Readback.
    rb = client.find_collection(handle, name)
    report["readback"] = {"found": bool(rb), "collection": rb}
    report["manual_steps"] = [
        "Publish the collection to the Online Store channel in admin "
        "(write_publications not held by the server token)."]
    return report


# ════════════════════════════════════════════════════════════════════════════
# verify_product
# ════════════════════════════════════════════════════════════════════════════
def verify_product(*, handle: Optional[str] = None, id: Optional[str] = None) -> dict:
    client = _client(dry_run=False)
    ref = handle or id
    if not ref:
        return {"tool": "verify_product", "status": "error", "reason": "supply handle or id"}
    p = client.get_product_full(ref)
    if not p:
        return {"tool": "verify_product", "status": "not_found", "ref": ref}

    specs = {e["node"]["key"]: e["node"]["value"] for e in p.get("metafields", {}).get("edges", [])}
    variants = [v["node"] for v in p.get("variants", {}).get("edges", [])]
    images = [i["node"] for i in p.get("images", {}).get("edges", [])]
    member_handles = [e["node"]["handle"] for e in p.get("collections", {}).get("edges", [])]
    google_cat = (p.get("googleProductCategory") or {}).get("value") if p.get("googleProductCategory") else None
    image_ok = any((i.get("width") or 0) >= config.MIN_IMAGE_PX and
                   (i.get("height") or 0) >= config.MIN_IMAGE_PX for i in images)
    price = variants[0].get("price") if variants else None

    verdict = guards.feed_ready_verdict(
        vendor=p.get("vendor"), specs_written=bool(specs), google_category=google_cat,
        identifier=None, identifier_exists=False, image_ok=image_ok,
        price_or_quote=bool(price and price != "0.00") or ("quote-only" in (p.get("tags") or [])))

    pid = p.get("legacyResourceId")
    return {
        "tool": "verify_product", "status": "ok",
        "product": {"id": pid, "gid": p.get("id"), "handle": p.get("handle"),
                    "title": p.get("title"), "status": p.get("status"),
                    "vendor": p.get("vendor"), "product_type": p.get("productType"),
                    "tags": p.get("tags"), "admin_url": f"{config.ADMIN_BASE}/products/{pid}",
                    "storefront_url": p.get("onlineStoreUrl")},
        "specs": specs,
        "feed": {"google_product_category": google_cat, "price": price},
        "images": [{"url": i.get("url"), "width": i.get("width"),
                    "height": i.get("height"), "passes_500px":
                    (i.get("width") or 0) >= config.MIN_IMAGE_PX and
                    (i.get("height") or 0) >= config.MIN_IMAGE_PX} for i in images],
        "collections": member_handles,
        "feed_verdict": verdict,
    }
