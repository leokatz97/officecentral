#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-5 — Phase 6 writer + hardened readback.

Sequential Admin GraphQL productUpdate (descriptionHtml, vendor, productType, tags, seo)
with embedded specs.* metafields, then a hardened readback comparator (cosmetic
normalization tolerant) and a cache-busted storefront curl per product. HALTS on any
hard mismatch. Logs per-product to data/logs/session-5-{ts}.log.

Pre-write snapshots already captured in Phase 3 (data/backups/session-5-*-pre-*.json) —
verified on disk before each write.
"""
import json, os, sys, time, html, re, urllib.request, urllib.error, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_env():
    env = {}
    for line in open(os.path.join(ROOT, ".env")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
    return env
ENV = load_env()
TOKEN = ENV["SHOPIFY_TOKEN"]
STORE = ENV.get("SHOPIFY_STORE", "office-central-online.myshopify.com")
API = "2026-04"
GQL = f"https://{STORE}/admin/api/{API}/graphql.json"

def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        "X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503): time.sleep(2*(attempt+1)); continue
            raise
    raise RuntimeError("gql retries exhausted")

TYPEMAP = {
    "type:table": "Tables", "type:desk": "Desks", "type:storage-filing": "Filing & Storage",
    "type:task-chair": "Task Chairs", "type:workstation": "Workstations",
    "type:lounge-seating": "Lounge Seating", "type:task-stool": "Task Stools",
    "type:height-adjustable-base": "Height-Adjustable Bases",
    "type:privacy-screen": "Privacy Screens", "type:privacy-panel": "Privacy Panels",
}
SINGLE = {"manufacturer","product_line","dimensions","weight","weight_capacity",
          "warranty","country_of_manufacture","who_its_for"}
LIST   = {"model_codes","finishes_available","key_features","certifications"}
MULTI  = {"materials"}
TYPEDEF = {**{k:"single_line_text_field" for k in SINGLE},
           **{k:"list.single_line_text_field" for k in LIST},
           "materials":"multi_line_text_field"}

def build_metafields(d):
    out = []
    for k in list(SINGLE):
        v = (d.get(k) or "").strip()
        if v: out.append({"namespace":"specs","key":k,"type":TYPEDEF[k],"value":v})
    for k in list(LIST):
        v = d.get(k) or []
        if v: out.append({"namespace":"specs","key":k,"type":TYPEDEF[k],"value":json.dumps(v)})
    for k in list(MULTI):
        v = d.get(k) or []
        if v: out.append({"namespace":"specs","key":k,"type":TYPEDEF[k],"value":"\n".join(v)})
    return out

def producttype(d):
    for t in d["tags"]:
        if t in TYPEMAP: return TYPEMAP[t]
    return ""

UPDATE = """
mutation($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id }
    userErrors { field message }
  }
}
"""
READ = """
query($id: ID!) {
  product(id: $id) {
    descriptionHtml vendor productType tags
    seo { title description }
    metafields(first: 50, namespace: "specs") { edges { node { key value type } } }
  }
}
"""

def norm(s):
    if s is None: return ""
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def curl_storefront(handle, ts):
    url = f"https://www.brantbusinessinteriors.com/products/{handle}?_b4s5={ts}"
    try:
        out = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}",
                              "-A","Mozilla/5.0 b4s5-verify", url],
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip()
    except Exception as e:
        return f"ERR:{e}"

def main():
    data = json.load(open("/tmp/session5_drafts.json"))["drafts"]
    state = json.load(open("/tmp/session5_state.json"))
    pre_ts = state["ts"]
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    logf = open(os.path.join(ROOT, "data", "logs", f"session-5-{ts}.log"), "w")
    def log(m):
        print(m); logf.write(m+"\n"); logf.flush()

    log(f"=== PHASE 6 WRITE START ts={ts} | {len(data)} products ===")
    results = {}
    for i, d in enumerate(data, 1):
        h = d["handle"]
        gid = state["results"][h]["snapshot"]  # path
        snap_path = os.path.join(ROOT, f"data/backups/session-5-{h}-pre-{pre_ts}.json")
        if not os.path.exists(snap_path):
            log(f"[{i}/27] {h} :: HALT — pre-write snapshot missing {snap_path}"); sys.exit(2)
        pid = json.load(open(snap_path))["id"]

        inp = {
            "id": pid,
            "descriptionHtml": d["body_html"],
            "vendor": "Global Furniture Group",
            "tags": d["tags"],
            "seo": {"title": d["seo_title"], "description": d["seo_description"]},
            "metafields": build_metafields(d),
        }
        pt = producttype(d)
        if pt: inp["productType"] = pt

        res = gql(UPDATE, {"input": inp})
        errs = res.get("errors") or res["data"]["productUpdate"]["userErrors"]
        if errs:
            log(f"[{i}/27] {h} :: HALT — productUpdate errors: {json.dumps(errs)}"); sys.exit(2)

        time.sleep(0.4)
        rb = gql(READ, {"id": pid})["data"]["product"]
        mism = []
        if norm(rb["seo"]["title"]) != norm(d["seo_title"]): mism.append(f"seo.title")
        if norm(rb["seo"]["description"]) != norm(d["seo_description"]): mism.append("seo.description")
        if norm(rb["descriptionHtml"]) != norm(d["body_html"]): mism.append("descriptionHtml")
        if set(rb["tags"]) != set(d["tags"]): mism.append(f"tags ({set(d['tags'])^set(rb['tags'])})")
        if rb["vendor"] != "Global Furniture Group": mism.append(f"vendor={rb['vendor']}")
        if pt and rb["productType"] != pt: mism.append(f"productType={rb['productType']}")
        # metafields
        rbmf = {e["node"]["key"]: e["node"]["value"] for e in rb["metafields"]["edges"]}
        for mf in inp["metafields"]:
            got = rbmf.get(mf["key"])
            if got is None: mism.append(f"mf.{mf['key']} MISSING"); continue
            if mf["type"].startswith("list."):
                if json.loads(got) != json.loads(mf["value"]): mism.append(f"mf.{mf['key']}")
            else:
                if norm(got) != norm(mf["value"]): mism.append(f"mf.{mf['key']}")
        if mism:
            log(f"[{i}/27] {h} :: HALT — readback mismatch: {mism}")
            sys.exit(2)

        code = curl_storefront(h, ts)
        sf = "OK" if code == "200" else f"WARN({code})"
        results[h] = {"written": True, "metafields": len(inp["metafields"]),
                      "productType": pt, "storefront": code}
        log(f"[{i}/27] {h} :: WRITE OK | mf={len(inp['metafields'])} | readback MATCH | storefront {sf}")
        time.sleep(0.3)

    json.dump({"ts": ts, "results": results}, open("/tmp/session5_write.json", "w"), indent=2)
    log(f"\n=== PHASE 6 COMPLETE — {len(results)}/27 written, all readbacks MATCH ===")
    sf_warn = [h for h,r in results.items() if r["storefront"] != "200"]
    if sf_warn: log(f"storefront non-200 (edge cache lag, Admin-API readback is the gate): {sf_warn}")

if __name__ == "__main__":
    main()
