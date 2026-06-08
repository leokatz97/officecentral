"""Server-side guard logic for onboard_product / create_collection.

These run REGARDLESS of what the caller asked — they are the enforcement that
the build spec requires to live server-side, not in skill text. Pure decision
helpers here; the tools orchestrate them and the ShopifyClient.
"""
from __future__ import annotations

import re
from typing import Optional

from . import config
from .references import BrandResolution, ReferenceData


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower())
    return s.strip("-")


# ── BRAND RE-RESOLUTION + VENDOR LOCK ───────────────────────────────────────
def resolve_brand(refs: ReferenceData, sku: str) -> BrandResolution:
    """Always re-resolve from the SKU prefix — the prefix wins over any
    caller-supplied brand/vendor."""
    return refs.resolve_sku(sku)


def check_vendor(resolution: BrandResolution, requested_vendor: Optional[str]) -> dict:
    """Vendor must equal the resolved manufacturer. Reject the forbidden BBI
    vendor outright. Returns {ok, vendor, error}."""
    manufacturer = resolution.manufacturer
    # Hard rule: never set the BBI house name as vendor.
    if requested_vendor and requested_vendor.strip().lower() == config.FORBIDDEN_VENDOR.lower():
        return {"ok": False, "vendor": None,
                "error": f"Refused to set vendor to '{config.FORBIDDEN_VENDOR}'. "
                         f"Vendor must be the manufacturer ('{manufacturer}')."}
    # If the caller supplied a vendor that conflicts with the resolved brand, reject.
    if requested_vendor and manufacturer and \
            requested_vendor.strip().lower() != manufacturer.strip().lower():
        return {"ok": False, "vendor": None,
                "error": f"vendor conflict: payload vendor '{requested_vendor}' != "
                         f"manufacturer resolved from SKU prefix '{manufacturer}'. "
                         f"Prefix wins; correct the payload or escalate to Leo."}
    return {"ok": True, "vendor": manufacturer, "error": None}


# ── SPEC FILTER (source_url required) ────────────────────────────────────────
def filter_specs(specs: list[dict]) -> tuple[list[dict], list[dict]]:
    """Keep only specs that carry a source_url. Drop (and report) the rest.
    Never fabricate a value. Returns (kept, dropped_with_reason)."""
    kept, dropped = [], []
    for s in specs or []:
        name = (s.get("name") or "").strip()
        value = s.get("value")
        src = (s.get("source_url") or "").strip()
        if not name or value in (None, ""):
            dropped.append({"name": name, "reason": "missing name or value"})
            continue
        if not src:
            dropped.append({"name": name, "value": value,
                            "reason": "no source_url — spec dropped (never fabricated)"})
            continue
        kept.append({"name": name, "value": value, "source_url": src,
                     "source_date": s.get("source_date")})
    return kept, dropped


def spec_metafields(kept: list[dict]) -> list[dict]:
    """Build metafieldsSet inputs (namespace 'specs'). Value stored as text;
    provenance (source_url/date) is carried in the verification report + audit."""
    out = []
    for s in kept:
        out.append({
            "namespace": "specs",
            "key": slugify(s["name"]).replace("-", "_"),
            "type": "single_line_text_field",
            "value": str(s["value"]).strip(),
        })
    return out


# ── CONFIRMED-BY-STEVE GATES ─────────────────────────────────────────────────
def gate_confirmed(obj: Optional[dict], label: str) -> tuple[Optional[dict], Optional[str]]:
    """Return (obj, None) only if obj carries confirmed_by_steve truthy; else
    (None, note) so the field is omitted and reported."""
    if obj is None:
        return None, None
    if obj.get("confirmed_by_steve"):
        return obj, None
    return None, f"{label} omitted — not confirmed_by_steve"


# ── SMART RULE → REQUIRED TAGS ───────────────────────────────────────────────
def required_tags_from_rule(smart_collection: dict) -> tuple[list[str], list[str]]:
    """From a live smart collection's rules, derive tags to add so the product
    joins. Returns (tags_to_add, unsatisfiable_notes).

    Adding every tag:equals condition satisfies both AND (disjunctive=false) and
    OR (disjunctive=true) rule sets. Non-tag columns (title/type/vendor) can't be
    satisfied by tags — reported so membership is verified by readback instead."""
    rules = smart_collection.get("rules", []) or []
    tags, notes = [], []
    for r in rules:
        col = r.get("column")
        rel = r.get("relation")
        cond = r.get("condition")
        if col == "tag" and rel == "equals":
            tags.append(cond)
        else:
            notes.append(f"rule [{col} {rel} '{cond}'] not tag-satisfiable")
    # de-dup, preserve order
    seen, uniq = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t); uniq.append(t)
    return uniq, notes


# ── FEED / BORN-FEED-READY VERDICT ───────────────────────────────────────────
def feed_ready_verdict(*, vendor, specs_written, google_category,
                       identifier_satisfied, image_ok, price_or_quote) -> dict:
    """Compute a born-feed-ready verdict + the gaps that block it.
    `identifier_satisfied` = has a GTIN OR is flagged as a custom product (no GTIN
    needed). The caller decides how that boolean is established."""
    gaps = []
    if not vendor:
        gaps.append("missing vendor/brand")
    if not google_category:
        gaps.append("no google_product_category")
    if not identifier_satisfied:
        gaps.append("no GTIN and not flagged as a custom product (mm-google-shopping.custom_product)")
    if not image_ok:
        gaps.append("no image passing the >=500px check")
    if not price_or_quote:
        gaps.append("no price and not marked quote_only")
    if not specs_written:
        gaps.append("no sourced specs written")
    return {"born_feed_ready": len(gaps) == 0, "gaps": gaps}


def feed_ready_from_product(p: dict) -> dict:
    """Derive born-feed-ready PURELY from persisted product state (a node from
    ShopifyClient.get_product_full). Used by BOTH verify_product and
    onboard_product's post-write readback so the two tools always agree."""
    from . import config  # local import to avoid cycle at module load
    variants = [v["node"] for v in p.get("variants", {}).get("edges", [])]
    images = [i["node"] for i in p.get("images", {}).get("edges", [])]
    specs = {e["node"]["key"]: e["node"]["value"]
             for e in p.get("metafields", {}).get("edges", [])}
    google_cat = (p.get("googleProductCategory") or {}).get("value")
    custom_product = str((p.get("customProduct") or {}).get("value") or "").lower() == "true"
    has_gtin = any((v.get("barcode") or "").strip() for v in variants)
    image_ok = any((i.get("width") or 0) >= config.MIN_IMAGE_PX and
                   (i.get("height") or 0) >= config.MIN_IMAGE_PX for i in images)
    price = variants[0].get("price") if variants else None
    price_or_quote = bool(price and price not in ("0.00", "0", None)) \
        or ("quote-only" in (p.get("tags") or []))
    return feed_ready_verdict(
        vendor=p.get("vendor"), specs_written=bool(specs), google_category=google_cat,
        identifier_satisfied=(has_gtin or custom_product),
        image_ok=image_ok, price_or_quote=price_or_quote)
