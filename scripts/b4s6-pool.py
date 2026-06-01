#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-6 — Phase 2 pool identifier (live Admin API, read-only).

Pulls every vendor='Global Furniture Group' product, filters to the UNENRICHED pool
(no live specs.manufacturer metafield), resolves the SKU prefix per product, classifies
body state, flags keyword-cluster relevance (executive-desks / reception / boardroom /
waiting-room-seating), and EXCLUDES (a) non-Global SKU prefixes (e.g. MityBilt MTY
re-routes) and (b) BOILERPLATE-corrupted bodies (the deferred fix-first track).

Ranks the eligible pool by cluster-relevance first, then price (ROI proxy). Writes
/tmp/b4s6-pool.json. No mutations.
"""
import json, os, re, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = {}
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); ENV[k.strip()] = v.strip().strip('"').strip("'")
TOKEN = ENV["SHOPIFY_TOKEN"]
STORE = ENV.get("SHOPIFY_STORE", "office-central-online.myshopify.com")
GQL = f"https://{STORE}/admin/api/2026-04/graphql.json"
HDR = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

# SKU prefixes that resolve to Global Furniture Group (longest stem first)
GLOBAL_PREFIXES = ["OFGO", "GLB", "GLO", "OTG", "MVL", "NLP", "NL", "ML", "MLP"]
NON_GLOBAL_PREFIXES = {  # explicit re-routes that may be mis-vendored as Global
    "MTY": "MityBilt", "SAF": "Safco", "HTW": "Heartwood", "OSP": "Office Star Products",
    "SEN": "Sentry Safe", "DEF": "deflecto", "GDX": "Gardex", "BORGO": "Borgo",
    "FOU": "Foundations", "FEL": "Fellowes", "TAY": "Tayco", "TAYCO": "Tayco",
    "ALLSE": "Allseating", "LCF": "Links Contract", "MMM": "3M", "VCT": "Victor",
    "HDL": "Heartwood Distributors", "IOF": "Intelligent Office Furniture",
    "RIC": "Richelieu", "HZN": "Horizon Furniture", "SCN": "UNKNOWN-SCN",
}

def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers=HDR, method="POST")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read())
            if "errors" in d:
                raise SystemExit(f"GraphQL errors: {d['errors']}")
            return d["data"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503):
                time.sleep(2 * (attempt + 1)); continue
            raise
    raise RuntimeError("gql retries exhausted")

Q = """
query($cursor: String) {
  products(first: 100, after: $cursor, query: "vendor:'Global Furniture Group'") {
    pageInfo { hasNextPage endCursor }
    edges { node {
      id legacyResourceId handle title productType status tags descriptionHtml
      priceRangeV2 { minVariantPrice { amount } maxVariantPrice { amount } }
      mfManu: metafield(namespace: "specs", key: "manufacturer") { value }
      variants(first: 5) { edges { node { sku } } }
    } }
  }
}
"""

def resolve_prefix(skus):
    """Return (prefix, vendor_guess) from the first non-empty SKU's alpha stem."""
    for s in skus:
        if not s: continue
        m = re.match(r"^([A-Za-z]+)", s.strip())
        if not m: continue
        alpha = m.group(1).upper()
        # longest-stem-first match against known Global prefixes
        for p in sorted(GLOBAL_PREFIXES, key=len, reverse=True):
            if alpha.startswith(p):
                return p, "Global Furniture Group"
        for p in sorted(NON_GLOBAL_PREFIXES, key=len, reverse=True):
            if alpha.startswith(p):
                return p, NON_GLOBAL_PREFIXES[p]
        return alpha, "UNKNOWN"
    return None, "NO_SKU"

def classify_body(html):
    if not html or not html.strip():
        return "NO_BODY"
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    low = text.lower()
    boiler = [
        "office central is", "brant business interiors is a", "your trusted source",
        "we are a leading", "contact us for a quote today", "is a leading supplier",
        "family-owned and operated since 1964 and",
    ]
    if any(b in low for b in boiler) and len(text) < 600:
        return "BOILERPLATE"
    if len(text) < 80:
        return "THIN"
    return f"REAL({len(text)}c)"

# Keyword-cluster relevance heuristics (title + type + tags).
# The 4 LOCKED funnel clusters from priority-keywords.yaml. Task/exec CHAIRS are NOT
# a locked cluster (they route to executive-seating / descriptive) — tracked separately.
CLUSTERS = {
    "executive-desks": [r"\bexecutive\b.*\bdesk\b", r"\bl-?shape", r"management.*(desk|suite)",
                        r"\bu-?shape", r"credenza", r"\bdesk\b.*(suite|station)", r"privacy.?panel"],
    "reception":       [r"reception"],
    "boardroom":       [r"boardroom", r"conference", r"\bmeeting\b", r"\bcraft\b", r"racetrack",
                        r"\bboat-?shaped\b", r"work.?table", r"\btablet\b", r"^table[- ]",
                        r"\btable\b.*\d+\s*x\s*\d+", r"overtable", r"lectern|podium"],
    "waiting-room-seating": [r"waiting", r"\bguest\b", r"\blounge\b", r"\bsofa\b", r"\bbench\b",
                        r"\bsled\b", r"side chair", r"armchair", r"armless.*chair", r"\bmoda\b",
                        r"\bsolo\b", r"twilight", r"\bspritz\b", r"rebound", r"stream", r"sonic",
                        r"reception.*(chair|seat)"],
}
# Task/executive seating — descriptive keyword use only (title+meta), pending ergonomic cluster
EXEC_SEATING_PAT = [r"executive.*chair", r"multi-?tilter", r"synchro-?tilter", r"mesh-?back",
                    r"task chair", r"tilter", r"drafting.*(stool|chair)", r"swivel.*stool"]
# Pure accessories / non-funnel — deprioritize (still eligible, just low value to clusters)
ACCESSORY_PAT = [r"\bdolly\b", r"\bcaster", r"planter", r"follower.?block", r"ionic.?feet",
                 r"\bglides?\b"]

def cluster_match(title, ptype, tags):
    blob = (title + " " + (ptype or "") + " " + " ".join(tags)).lower()
    hits = [c for c, pats in CLUSTERS.items() if any(re.search(p, blob) for p in pats)]
    return hits

def tag_role(title, ptype, tags, clusters):
    blob = (title + " " + (ptype or "") + " " + " ".join(tags)).lower()
    if any(re.search(p, blob) for p in ACCESSORY_PAT):
        return "accessory"
    if clusters:
        return "cluster"
    if any(re.search(p, blob) for p in EXEC_SEATING_PAT):
        return "exec-seating"
    return "other"

def fnum(x):
    try: return float(x)
    except: return 0.0

prods, cursor = [], None
while True:
    d = gql(Q, {"cursor": cursor})
    conn = d["products"]
    prods.extend(e["node"] for e in conn["edges"])
    if conn["pageInfo"]["hasNextPage"]:
        cursor = conn["pageInfo"]["endCursor"]
    else:
        break

rows = []
for n in prods:
    skus = [e["node"]["sku"] for e in n["variants"]["edges"]]
    prefix, vendor_guess = resolve_prefix(skus)
    pr = n.get("priceRangeV2") or {}
    price = max(fnum((pr.get("maxVariantPrice") or {}).get("amount")),
                fnum((pr.get("minVariantPrice") or {}).get("amount")))
    enriched = bool((n.get("mfManu") or {}).get("value"))
    body = classify_body(n["descriptionHtml"])
    clusters = cluster_match(n["title"], n["productType"], n["tags"])
    role = tag_role(n["title"], n["productType"], n["tags"], clusters)
    rows.append({
        "product_id": n["legacyResourceId"], "handle": n["handle"], "title": n["title"],
        "product_type": n["productType"], "status": n["status"], "price": price,
        "first_sku": next((s for s in skus if s), None), "sku_prefix": prefix,
        "vendor_guess": vendor_guess, "enriched_live": enriched, "body_state": body,
        "clusters": clusters, "role": role,
    })

Path("/tmp/b4s6-pool.json").write_text(json.dumps(rows, indent=2))

total = len(rows)
enriched = [r for r in rows if r["enriched_live"]]
pool = [r for r in rows if not r["enriched_live"]]
# Eligibility: Global-resolved prefix AND not boilerplate-corrupted
non_global = [r for r in pool if r["vendor_guess"] != "Global Furniture Group"]
boiler = [r for r in pool if r["vendor_guess"] == "Global Furniture Group" and r["body_state"] == "BOILERPLATE"]
eligible = [r for r in pool if r["vendor_guess"] == "Global Furniture Group" and r["body_state"] != "BOILERPLATE"]

ROLE_RANK = {"cluster": 0, "exec-seating": 1, "other": 2, "accessory": 3}
def rank_key(r):
    return (ROLE_RANK.get(r["role"], 9), -len(r["clusters"]), -r["price"])
eligible.sort(key=rank_key)

print(f"=== LIVE Admin API (2026-04): vendor='Global Furniture Group' ===")
print(f"  total products:                 {total}")
print(f"  already enriched (specs.manu):  {len(enriched)}")
print(f"  unenriched pool:                {len(pool)}")
print(f"    - EXCLUDED non-Global prefix: {len(non_global)}  {sorted(set(str(r['sku_prefix']) for r in non_global))}")
print(f"    - EXCLUDED boilerplate-corrupt: {len(boiler)}")
print(f"    - ELIGIBLE:                   {len(eligible)}")
from collections import Counter
rc = Counter(r["role"] for r in eligible)
print(f"       roles: {dict(rc)}")
print(f"\n=== ELIGIBLE POOL — by role (cluster > exec-seating > other > accessory), then price ===")
for r in eligible:
    cl = ",".join(r["clusters"]) or "-"
    print(f"  [{r['role']:12}] ${r['price']:8.2f} [{str(r['sku_prefix']) or '??':5}] {r['body_state']:11} {r['status']:8} <{cl:30}> {r['handle'][:48]}")
print(f"\n=== EXCLUDED non-Global / no-SKU (re-routes) ===")
for r in non_global:
    print(f"  [{str(r['sku_prefix']):5}->{r['vendor_guess']:24}] {r['handle'][:50]}")
print("\nwritten /tmp/b4s6-pool.json")
