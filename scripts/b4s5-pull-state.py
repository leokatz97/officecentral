#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-5 — Phase 3 live state puller.

Reads /tmp/session5_batch.json (the approved 27-handle manifest), queries each
product by handle via the Admin GraphQL API, captures the canonical fields, and
writes a pre-write snapshot to data/backups/session-5-{handle}-pre-{ts}.json
(gitignored). Emits a body-state classification summary at the end.

Read-only against Shopify. No mutations.
"""
import json, os, sys, time, urllib.request, urllib.error, datetime, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_env():
    env = {}
    with open(os.path.join(ROOT, ".env")) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

ENV = load_env()
TOKEN = ENV["SHOPIFY_TOKEN"]
STORE = ENV.get("SHOPIFY_STORE", "office-central-online.myshopify.com")
API = "2026-04"
GQL = f"https://{STORE}/admin/api/{API}/graphql.json"

def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json",
    })
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503):
                time.sleep(2 * (attempt + 1)); continue
            raise
    raise RuntimeError("gql retries exhausted")

PRODUCT_Q = """
query($handle: String!) {
  productByHandle(handle: $handle) {
    id
    handle
    title
    descriptionHtml
    vendor
    productType
    status
    tags
    seo { title description }
    metafields(first: 50, namespace: "specs") {
      edges { node { key value type } }
    }
    variants(first: 1) { edges { node { sku price } } }
    featuredImage { url }
  }
}
"""

def classify_body(html):
    if not html or not html.strip():
        return "NO_BODY"
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    low = text.lower()
    boiler = [
        "office central is", "brant business interiors is a", "your trusted source",
        "we are a leading", "contact us for a quote today", "is a leading supplier",
        "family-owned and operated since 1964 and",  # generic stub pattern
    ]
    if any(b in low for b in boiler) and len(text) < 600:
        return "BOILERPLATE"
    if len(text) < 80:
        return "THIN"
    return f"REAL({len(text)}c)"

def main():
    manifest = json.load(open("/tmp/session5_batch.json"))
    handles = manifest["handles"]
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bdir = os.path.join(ROOT, "data", "backups")
    os.makedirs(bdir, exist_ok=True)
    summary = {"NO_BODY": [], "BOILERPLATE": [], "THIN": [], "REAL": []}
    results = {}
    for h in handles:
        data = gql(PRODUCT_Q, {"handle": h})
        if data.get("errors"):
            print(f"  !! {h}: GraphQL errors: {data['errors']}", file=sys.stderr)
            continue
        p = data["data"]["productByHandle"]
        if not p:
            print(f"  !! {h}: NOT FOUND", file=sys.stderr)
            continue
        mfs = {e["node"]["key"]: e["node"] for e in p["metafields"]["edges"]}
        v = p["variants"]["edges"][0]["node"] if p["variants"]["edges"] else {}
        snap = {
            "handle": p["handle"], "id": p["id"], "title": p["title"],
            "descriptionHtml": p["descriptionHtml"], "vendor": p["vendor"],
            "productType": p["productType"], "status": p["status"], "tags": p["tags"],
            "seo": p["seo"], "specs_metafields": mfs,
            "variant_sku": v.get("sku"), "variant_price": v.get("price"),
            "featuredImage": (p["featuredImage"] or {}).get("url"),
            "pulled_at": ts,
        }
        path = os.path.join(bdir, f"session-5-{h}-pre-{ts}.json")
        json.dump(snap, open(path, "w"), indent=2)
        cls = classify_body(p["descriptionHtml"])
        key = "REAL" if cls.startswith("REAL") else cls
        summary[key].append(h)
        results[h] = {"cls": cls, "vendor": p["vendor"], "sku": v.get("sku"),
                      "price": v.get("price"), "specs_count": len(mfs),
                      "status": p["status"], "type": p["productType"],
                      "snapshot": os.path.relpath(path, ROOT)}
        time.sleep(0.25)
    json.dump({"ts": ts, "results": results}, open("/tmp/session5_state.json", "w"), indent=2)
    print(f"\n=== PHASE 3 PULL COMPLETE — ts={ts} ===")
    print(f"pulled: {len(results)}/{len(handles)}")
    print(f"  NO_BODY    : {len(summary['NO_BODY'])}  {summary['NO_BODY']}")
    print(f"  BOILERPLATE: {len(summary['BOILERPLATE'])}  {summary['BOILERPLATE']}")
    print(f"  THIN       : {len(summary['THIN'])}  {summary['THIN']}")
    print(f"  REAL body  : {len(summary['REAL'])}")
    print("\n=== per-product ===")
    for h in handles:
        r = results.get(h)
        if not r:
            print(f"  MISSING  {h}"); continue
        print(f"  [{r['cls']:12}] sku={str(r['sku']):14} ${str(r['price']):>9} specs={r['specs_count']} {r['status']:8} {h}")

if __name__ == "__main__":
    main()
