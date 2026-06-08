#!/usr/bin/env python3
"""READ-ONLY orphan SKU-prefix diagnostic (Phase 1).

Fresh Admin-API pull of live products (status=active AND published_at not null),
extract the leading-alpha SKU prefix per product (greedy longest-known-prefix
match against sku-prefix-lookup.yaml), diff to find orphans, and emit an
evidence row per orphan: count, sample SKUs+titles, vendors, tags, signals.

No writes. No mutations. GET only.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / ".env"
LOOKUP = ROOT / "data/reference/sku-prefix-lookup.yaml"
API_VERSION = "2024-10"


def load_token():
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if line.startswith("SHOPIFY_TOKEN"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No SHOPIFY_TOKEN in .env")


def load_store():
    # default store from CLAUDE.md / known handle
    for line in ENV.read_text().splitlines():
        if line.strip().startswith("SHOPIFY_STORE"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return "office-central-online.myshopify.com"


def known_prefixes():
    # parse the sku_prefix_lookup: block only (avoid decoded_details/undecoded keys)
    prefixes = set()
    in_block = False
    for raw in LOOKUP.read_text().splitlines():
        if raw.startswith("sku_prefix_lookup:"):
            in_block = True
            continue
        if in_block:
            if raw and not raw.startswith((" ", "\t", "#")):
                break  # next top-level key
            m = re.match(r"\s+([A-Za-z0-9]+):\s*\S", raw)
            if m:
                prefixes.add(m.group(1).upper())
    return prefixes


TOKEN = load_token()
STORE = load_store()
GQL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"


def gql(query, variables):
    req = urllib.request.Request(
        GQL,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


QUERY = """
query($cursor: String) {
  products(first: 100, after: $cursor, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    nodes {
      handle title vendor tags publishedAt
      variants(first: 25) { nodes { sku } }
    }
  }
}
"""


def fetch_all():
    out, cursor = [], None
    while True:
        d = gql(QUERY, {"cursor": cursor})
        if "errors" in d:
            sys.exit("GQL errors: " + json.dumps(d["errors"]))
        block = d["data"]["products"]
        out.extend(block["nodes"])
        if not block["pageInfo"]["hasNextPage"]:
            break
        cursor = block["pageInfo"]["endCursor"]
    return out


def leading_alpha(sku):
    m = re.match(r"\s*([A-Za-z]+)", sku or "")
    return m.group(1).upper() if m else None


def resolve_prefix(sku, known):
    """Greedy longest-known-prefix match on the leading alpha run; else the alpha run."""
    alpha = leading_alpha(sku)
    if not alpha:
        return None, None  # numeric / no alpha
    # longest known prefix that the alpha run starts with
    cands = sorted((p for p in known if alpha.startswith(p)), key=len, reverse=True)
    if cands:
        return cands[0], "known"
    return alpha, "orphan"


def main():
    known = known_prefixes()
    prods = fetch_all()
    live = [p for p in prods if p.get("publishedAt")]

    orphan_rows = defaultdict(lambda: {"count": 0, "samples": [], "vendors": Counter(),
                                       "tags": Counter()})
    no_sku = numeric = known_hit = 0

    for p in live:
        skus = [v["sku"] for v in p["variants"]["nodes"] if v.get("sku")]
        if not skus:
            no_sku += 1
            continue
        sku0 = skus[0]
        pref, kind = resolve_prefix(sku0, known)
        if pref is None:
            numeric += 1
            continue
        if kind == "known":
            known_hit += 1
            continue
        r = orphan_rows[pref]
        r["count"] += 1
        if len(r["samples"]) < 3:
            r["samples"].append({"sku": sku0, "title": p["title"], "vendor": p.get("vendor")})
        r["vendors"][p.get("vendor") or "(none)"] += 1
        for t in p.get("tags", []):
            r["tags"][t] += 1

    result = {
        "store": STORE,
        "live_products": len(live),
        "active_fetched": len(prods),
        "no_sku_skipped": no_sku,
        "numeric_no_prefix": numeric,
        "known_prefix_hits": known_hit,
        "known_prefixes": sorted(known),
        "orphan_count": len(orphan_rows),
        "orphans": {},
    }
    for pref, r in sorted(orphan_rows.items(), key=lambda kv: -kv[1]["count"]):
        result["orphans"][pref] = {
            "count": r["count"],
            "samples": r["samples"],
            "vendors": dict(r["vendors"]),
            "tags": dict(r["tags"]),
        }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
