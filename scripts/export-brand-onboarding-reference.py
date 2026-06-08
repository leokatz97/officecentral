#!/usr/bin/env python3
"""Deterministic exporter for brand-onboarding-reference-<date>.json.

Rebuilds the consolidated brand-onboarding snapshot that the BBI onboarding skill
(bbi_onboarding_mcp) bundles, purely from:

  - data/reference/sku-prefix-lookup.yaml      (prefixes + decoded sub-codes + undecoded)
  - data/reference/manufacturer-defaults.yaml  (country / certs / warranty)
  - data/reference/brand-collection-routing.yaml (brand → tag/collection routing)
  - Shopify Admin API GET (smart + custom collections, active products)

Everything in the JSON is derivable from those four sources — there is no
hand-curated content. This script IS the "snapshot exporter" referenced by
bbi_onboarding_mcp/references.py (which previously only existed ad-hoc).

Key reverse-engineered rules (validated by `--diff` against the prior JSON):
  * Prefix → brand resolution: leading alpha run of the first non-empty variant
    SKU, greedy longest-known match over BOTH top-level prefixes AND decoded
    sub-codes. This is why INV/LEV/UN (HDL/IOF sub-codes) resolve and are NOT
    orphans even though no SKU literally starts with HDL or IOF.
  * Manufacturer aliases fold lookup values onto canonical routing brands.
  * Brands sorted by canonical_manufacturer (case-sensitive); undecoded last.

READ-ONLY against Shopify. Writes only the JSON it is told to (--out).

Usage:
  python3 scripts/export-brand-onboarding-reference.py --out /tmp/regen.json
  python3 scripts/export-brand-onboarding-reference.py --out /tmp/regen.json \
      --diff data/exports/brand-onboarding-reference-2026-06-08.json
  python3 scripts/export-brand-onboarding-reference.py --date 2026-06-08 --write-canonical
"""
import argparse
import json
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import date as _date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / ".env"
REF = ROOT / "data" / "reference"
API_VERSION = "2024-10"
STORE = "office-central-online.myshopify.com"
GQL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

# Lookup-value → canonical routing manufacturer_name. Folds distributor / short
# forms onto the brand they belong to (documented inline in sku-prefix-lookup.yaml).
MANUFACTURER_ALIAS = {
    "Heartwood Distributors Ltd.": "Heartwood",  # HDL distributor code, same family as HTW
    "Links Contract": "Links Contract Furniture",  # LCF live vendor form
}

STANDALONE_NOTE = ("In sku-prefix-lookup but no brand-collection-routing entry; "
                   "target collections not yet defined.")


# ---------------------------------------------------------------- Shopify I/O
def _token() -> str:
    for line in ENV.read_text().splitlines():
        if line.strip().startswith("SHOPIFY_TOKEN"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FATAL: SHOPIFY_TOKEN not in .env")


def _gql(token, query, variables=None):
    req = urllib.request.Request(
        GQL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read())
    if "errors" in d:
        sys.exit("GQL errors: " + json.dumps(d["errors"]))
    return d["data"]


PRODUCTS_Q = """
query($cursor:String){
  products(first:100, after:$cursor, query:"status:active"){
    pageInfo{hasNextPage endCursor}
    nodes{ handle title vendor publishedAt
      variants(first:25){nodes{sku}} }
  }
}"""

COLLECTIONS_Q = """
query($cursor:String){
  collections(first:100, after:$cursor){
    pageInfo{hasNextPage endCursor}
    nodes{ handle title legacyResourceId
      ruleSet{ rules{column relation condition} } }
  }
}"""


def _paginate(token, query, root):
    out, cursor = [], None
    while True:
        block = _gql(token, query, {"cursor": cursor})[root]
        out.extend(block["nodes"])
        if not block["pageInfo"]["hasNextPage"]:
            return out
        cursor = block["pageInfo"]["endCursor"]


# ---------------------------------------------------------------- sub-code parse
def parse_sub_codes(key_sub_codes):
    """'INV/INVR/INVMP = Innovations' -> ['INV','INVR','INVMP']; multiword tokens dropped."""
    codes = set()
    for entry in key_sub_codes or []:
        head = str(entry).split("=", 1)[0]
        for tok in re.split(r"[/,]", head):
            c = tok.strip().upper()
            if re.fullmatch(r"[A-Z0-9]+", c):
                codes.add(c)
    return sorted(codes)


# ---------------------------------------------------------------- prefix resolver
def leading_alpha(sku):
    m = re.match(r"\s*([A-Za-z]+)", sku or "")
    return m.group(1).upper() if m else None


class Resolver:
    """Greedy longest-known match over top-level prefixes + decoded sub-codes."""
    def __init__(self, code_to_brand):
        self.codes = sorted(code_to_brand, key=len, reverse=True)
        self.map = code_to_brand

    def resolve(self, sku):
        alpha = leading_alpha(sku)
        if not alpha:
            return None, "numeric"
        for c in self.codes:               # longest first
            if alpha.startswith(c):
                return self.map[c], "known"
        return alpha, "orphan"


# ---------------------------------------------------------------- build snapshot
def build(token, gen_date):
    sku_yaml = yaml.safe_load((REF / "sku-prefix-lookup.yaml").read_text())
    mfr_yaml = yaml.safe_load((REF / "manufacturer-defaults.yaml").read_text())
    routing_yaml = yaml.safe_load((REF / "brand-collection-routing.yaml").read_text())

    lookup = sku_yaml["sku_prefix_lookup"]
    decoded = sku_yaml.get("decoded_details", {}) or {}
    undecoded = sku_yaml.get("undecoded", {}) or {}
    routing = routing_yaml["brand_routing"]

    def canon(mfr):
        return MANUFACTURER_ALIAS.get(mfr, mfr)

    def tmpl(items):
        # routing_tag_template values like `type:{product_type_slug}` are written
        # in unquoted YAML flow syntax and parse to {'type': {'product_type_slug': None}};
        # render them back to the literal template string the JSON expects.
        out = []
        for x in items or []:
            if isinstance(x, dict) and len(x) == 1:
                k, v = next(iter(x.items()))
                if isinstance(v, dict) and len(v) == 1:
                    ik, iv = next(iter(v.items()))
                    if iv is None:
                        out.append(f"{k}:{{{ik}}}")
                        continue
            out.append(x)
        return out

    # manufacturer_name -> routing brand_key
    mfr_to_key = {meta["manufacturer_name"]: key for key, meta in routing.items()}

    # prefix -> canonical manufacturer
    prefix_mfr = {p: canon(v) for p, v in lookup.items()}

    # sub-codes per prefix
    sub_codes_for_prefix = {p: parse_sub_codes(meta.get("key_sub_codes"))
                            for p, meta in decoded.items()}

    # --- assemble brand records keyed by brand_key ---
    brands = {}

    def ensure_routing_brand(key):
        meta = routing[key]
        mdef_raw = mfr_yaml.get(key, {})
        mdef = ({"country_of_manufacture": mdef_raw.get("country_of_manufacture"),
                 "certifications_typical": mdef_raw.get("certifications_typical", []),
                 "warranty": mdef_raw.get("warranty")} if mdef_raw else {})
        brands[key] = {
            "brand_key": key,
            "canonical_manufacturer": meta["manufacturer_name"],
            "brand_tag": meta.get("brand_tag"),
            "sub_brands": meta.get("sub_brands", []),
            "sku_prefixes": [],
            "documented_sub_codes": [],
            "routing_tag_template": tmpl(meta.get("routing_tag_template")),
            "collections_by_type": meta.get("primary_collections_by_type", {}) or {},
            "manufacturer_defaults": mdef,
            "notes": [],
            "_status": "active",
        }

    for key in routing:
        ensure_routing_brand(key)

    def standalone_key(mfr):
        return re.sub(r"[^a-z0-9]", "", mfr.lower())

    def ensure_standalone_brand(mfr):
        key = standalone_key(mfr)
        if key not in brands:
            brands[key] = {
                "brand_key": key, "canonical_manufacturer": mfr, "brand_tag": None,
                "sub_brands": [], "sku_prefixes": [], "documented_sub_codes": [],
                "routing_tag_template": None, "collections_by_type": {},
                "manufacturer_defaults": {}, "notes": [STANDALONE_NOTE],
                "_status": "active",
            }
        return key

    # map every top-level prefix to its brand_key; attach prefixes + sub-codes
    code_to_brand = {}
    for prefix, mfr in prefix_mfr.items():
        bkey = mfr_to_key.get(mfr) or ensure_standalone_brand(mfr)
        brands[bkey]["sku_prefixes"].append(prefix)
        code_to_brand[prefix] = bkey
        for sub in sub_codes_for_prefix.get(prefix, []):
            brands[bkey]["documented_sub_codes"].append(sub)
            code_to_brand.setdefault(sub, bkey)

    # undecoded pseudo-brands
    undecoded_brands = {}
    for prefix, meta in undecoded.items():
        bkey = f"undecoded:{prefix}"
        notes = [f"Undecoded SKU prefix — {meta.get('status')}"]
        if meta.get("category"):
            notes.append("category: " + " ".join(str(meta["category"]).split()))
        if meta.get("resolution"):
            notes.append("resolution: " + " ".join(str(meta["resolution"]).split()))
        undecoded_brands[bkey] = {
            "brand_key": bkey, "canonical_manufacturer": None, "brand_tag": None,
            "sub_brands": [], "sku_prefixes": [prefix], "routing_tag_template": None,
            "collections_by_type": {}, "manufacturer_defaults": {}, "notes": notes,
            "_status": "steve-gated",
        }
        code_to_brand[prefix] = bkey  # undecoded SCN counts toward its own bucket

    for b in brands.values():
        b["sku_prefixes"].sort()
        b["documented_sub_codes"] = sorted(set(b["documented_sub_codes"]))

    # --- live Shopify crawl ---
    collections = _paginate(token, COLLECTIONS_Q, "collections")
    smart, custom = {}, {}
    for c in collections:
        rec = {"collection_id": int(c["legacyResourceId"]), "title": c["title"]}
        if c.get("ruleSet"):
            rec["rules"] = [{"column": r["column"].lower(), "relation": r["relation"].lower(),
                             "condition": r["condition"]} for r in c["ruleSet"]["rules"]]
            smart[c["handle"]] = rec
        else:
            custom[c["handle"]] = rec

    products = _paginate(token, PRODUCTS_Q, "products")
    live = [p for p in products if p.get("publishedAt")]

    resolver = Resolver(code_to_brand)
    live_count = defaultdict(int)
    orphans = {}
    no_sku = numeric = 0
    for p in live:
        skus = [v["sku"] for v in p["variants"]["nodes"] if v.get("sku")]
        if not skus:
            no_sku += 1
            continue
        bkey, kind = resolver.resolve(skus[0])
        if kind == "numeric":
            numeric += 1
        elif kind == "known":
            live_count[bkey] += 1
        else:  # orphan
            o = orphans.setdefault(bkey, {"count": 0, "skus": [], "prods": []})
            o["count"] += 1
            if len(o["skus"]) < 3:
                o["skus"].append(skus[0])
                o["prods"].append({"handle": p["handle"], "title": p["title"],
                                   "vendor": p.get("vendor")})

    for bkey, n in live_count.items():
        if bkey in brands:
            brands[bkey].setdefault("_live", 0)
            brands[bkey]["_live"] = n
        elif bkey in undecoded_brands:
            undecoded_brands[bkey]["_live"] = n

    # --- target_collections + smart conditions ---
    def collection_record(handle):
        if handle in smart:
            s = smart[handle]
            tag_conds = [f'equals "{r["condition"]}"' for r in s["rules"]
                         if r["column"] == "tag" and r["relation"] == "equals"]
            return {"handle": handle, "membership": "SMART",
                    "collection_id": s["collection_id"], "title": s["title"],
                    "smart_rules": s["rules"], "smart_tag_conditions": tag_conds}, tag_conds
        if handle in custom:
            c = custom[handle]
            return {"handle": handle, "membership": "MANUAL",
                    "collection_id": c["collection_id"], "title": c["title"]}, []
        return {"handle": handle, "membership": "missing",
                "collection_id": None, "title": None}, []

    routed_missing = {}  # handle -> set(manufacturer)
    for b in brands.values():
        seen, targets, brand_conds = set(), [], []
        for handles in b["collections_by_type"].values():
            for h in handles:
                if h in seen:
                    continue
                seen.add(h)
                rec, conds = collection_record(h)
                targets.append(rec)
                if rec["membership"] == "missing":
                    routed_missing.setdefault(h, []).append(b["canonical_manufacturer"])
                for c in conds:
                    if c not in brand_conds:
                        brand_conds.append(c)
        b["target_collections"] = targets
        b["smart_collection_tag_conditions"] = brand_conds

    # --- finalize brand records (exact field order) ---
    def finalize(b, undecoded=False):
        rec = {
            "brand_key": b["brand_key"],
            "canonical_manufacturer": b["canonical_manufacturer"],
            "brand_tag": b["brand_tag"],
            "sub_brands": b["sub_brands"],
            "sku_prefixes": b["sku_prefixes"],
        }
        if not undecoded:
            rec["documented_sub_codes"] = b["documented_sub_codes"]
        rec.update({
            "routing_tag_template": b["routing_tag_template"],
            "collections_by_type": b["collections_by_type"],
            "target_collections": b.get("target_collections", []),
            "smart_collection_tag_conditions": b.get("smart_collection_tag_conditions", []),
            "default_google_product_category": None,
            "manufacturer_defaults": b["manufacturer_defaults"],
            "live_product_count": b.get("_live", 0),
            "status": b["_status"],
            "notes": b["notes"],
        })
        return rec

    regular = [finalize(b) for b in brands.values()]
    regular.sort(key=lambda r: r["canonical_manufacturer"])
    undec = [finalize(b, undecoded=True) for b in undecoded_brands.values()]
    undec.sort(key=lambda r: r["brand_key"])
    brand_list = regular + undec

    orphan_list = []
    for bkey, o in orphans.items():
        orphan_list.append({"prefix": bkey, "live_product_count": o["count"],
                            "sample_skus": o["skus"], "sample_products": o["prods"]})
    orphan_list.sort(key=lambda o: (-o["live_product_count"], o["prefix"]))  # deterministic & reproducible

    routed_missing_list = [{"handle": h, "routed_for_brands": v}
                           for h, v in routed_missing.items()]
    routed_missing_list.sort(key=lambda r: r["handle"])

    meta = {
        "generated": gen_date,
        "store": STORE,
        "api_version": API_VERSION,
        "purpose": "Consolidated brand onboarding reference for downstream intake tool. GET-only snapshot.",
        "sources": [
            "data/reference/manufacturer-defaults.yaml",
            "data/reference/sku-prefix-lookup.yaml",
            "data/reference/brand-collection-routing.yaml",
            "Shopify Admin API GET /smart_collections, /custom_collections, /products (status=active)",
        ],
        "collection_membership_legend": {
            "SMART": "rule/tag-based smart collection — product joins by carrying the required tag(s)",
            "MANUAL": "custom collection — product must be added via a Collect (write_products)",
            "missing": "handle routed in reference files but no such collection exists on the store yet",
        },
        "prefix_match_method": "Leading alpha run of the first non-empty variant SKU, greedy longest-known-prefix match.",
        "live_product_filter": "status=active AND published_at not null (live on Online Store).",
        "counts": {
            "active_products_fetched": len(products),
            "live_published_products": len(live),
            "products_without_sku_skipped": no_sku,
            "products_numeric_sku_no_alpha_prefix": numeric,
            "smart_collections_on_store": len(smart),
            "custom_collections_on_store": len(custom),
            "brands": len(brand_list),
            "orphan_prefixes": len(orphan_list),
            "routed_but_missing_collections": len(routed_missing_list),
        },
        "google_product_category_note": "No google_product_category is recorded in any of the three reference files; field emitted as null for every brand.",
    }
    return {"meta": meta, "brands": brand_list, "orphans": orphan_list,
            "routed_but_missing_collections": routed_missing_list}


# ---------------------------------------------------------------- diff helper
def categorize_diff(old, new):
    """Return (prefix_related, other) human-readable difference lists."""
    prefix_rel, other = [], []
    ob = {b["brand_key"]: b for b in old["brands"]}
    nb = {b["brand_key"]: b for b in new["brands"]}
    if set(ob) != set(nb):
        other.append(f"brand set changed: +{sorted(set(nb)-set(ob))} -{sorted(set(ob)-set(nb))}")
    for k in sorted(set(ob) & set(nb)):
        for field in ob[k]:
            ov, nv = ob[k].get(field), nb[k].get(field)
            if ov == nv:
                continue
            line = f"brand[{k}].{field}: {ov!r} -> {nv!r}"
            if field in ("sku_prefixes", "live_product_count", "documented_sub_codes"):
                prefix_rel.append(line)
            else:
                other.append(line)
    op = {o["prefix"] for o in old["orphans"]}
    npf = {o["prefix"] for o in new["orphans"]}
    if op != npf:
        prefix_rel.append(f"orphans removed: {sorted(op-npf)}; added: {sorted(npf-op)}")
    for ok, nk in [(k, k) for k in old["meta"]["counts"]]:
        ov, nv = old["meta"]["counts"][ok], new["meta"]["counts"].get(nk)
        if ov != nv:
            (prefix_rel if ok in ("orphan_prefixes",) else other).append(
                f"meta.counts.{ok}: {ov} -> {nv}")
    # non-prefix meta differences
    for key in new["meta"]:
        if key == "counts":
            continue
        if old["meta"].get(key) != new["meta"][key]:
            other.append(f"meta.{key} changed")
    return prefix_rel, other


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="output JSON path")
    ap.add_argument("--date", default=_date.today().isoformat())
    ap.add_argument("--diff", help="path to a prior JSON to diff against")
    ap.add_argument("--write-canonical", action="store_true",
                    help="write to data/exports + onboarding-mcp-state + bundle reference_data")
    args = ap.parse_args()

    snap = build(_token(), args.date)
    text = json.dumps(snap, indent=2, ensure_ascii=False) + "\n"

    outs = []
    if args.out:
        outs.append(Path(args.out))
    if args.write_canonical:
        fn = f"brand-onboarding-reference-{args.date}.json"
        outs += [ROOT / "data" / "exports" / fn,
                 ROOT / "data" / "onboarding-mcp-state" / fn,
                 ROOT / "bbi_onboarding_mcp" / "reference_data" / fn]
    for p in outs:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        print(f"wrote {p}")
    if not outs:
        sys.stdout.write(text)

    if args.diff:
        old = json.loads(Path(args.diff).read_text())
        prefix_rel, other = categorize_diff(old, snap)
        print("\n=== PREFIX-RELATED DIFFERENCES (expected) ===")
        for l in prefix_rel:
            print("  +", l)
        print("\n=== NON-PREFIX DIFFERENCES (must be empty / explained) ===")
        if other:
            for l in other:
                print("  !", l)
        else:
            print("  (none)")


if __name__ == "__main__":
    main()
