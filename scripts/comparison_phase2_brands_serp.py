#!/usr/bin/env python3
"""PHASE 2 C+D — brand-vs-brand universe + live SERP reads (DataForSEO, Canada)."""
import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfs_client import post, LOCATION_CANADA, LANG

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "reports", "comparison-content")
RAW = os.path.join(OUT, "raw")

# ---- Step C: brand-vs-brand + brand review/comparison terms ----
BRAND_KW = [
 # brand-vs-brand
 "herman miller vs steelcase","steelcase vs herman miller","herman miller vs haworth",
 "steelcase vs haworth","aeron vs leap","steelcase leap vs herman miller aeron",
 "global vs teknion","humanscale vs herman miller","ergocentric vs herman miller",
 "secretlab vs herman miller","branch vs steelcase",
 # brand reviews
 "ergocentric review","ergocentric chair review","global furniture review",
 "keilhauer review","steelcase review","herman miller review","hon chair review",
 "teknion review","offices to go review","obusforme chair review","allseating review",
 "humanscale review","global office chair review",
 # brand "chairs" / dealer (comparison-adjacent, recon overlap validation)
 "ergocentric chairs","global furniture group","keilhauer chairs","teknion office chairs",
 "hon office chairs","herman miller chairs","steelcase chairs","allseating chairs",
 "offices to go chairs","obusforme chair","humanscale chairs","global office chairs",
 # material / type comparison axes
 "mesh vs leather office chair","mesh vs fabric office chair","standing desk vs sitting desk",
 "sit stand desk vs regular desk","leather vs mesh office chair","task chair vs executive chair",
 "ergonomic chair vs gaming chair","fabric vs mesh office chair",
 # is-it-worth-it (AEO comparison value)
 "is herman miller worth it","are ergonomic chairs worth it","are standing desks worth it",
 "is steelcase worth it","is ergocentric a good brand",
]

# ---- Step D: SERP reads for priority comparison clusters ----
SERP_KW = [
 "best office chair canada","best office chairs","best office chairs for long hours",
 "best standing desk canada","best ergonomic office chair canada","canadian made office chairs",
 "office pods canada","heavy duty office chair","best executive office chair",
 "commercial office furniture","best filing cabinet","best office furniture toronto",
 "best big and tall office chair","cubicle vs open office","herman miller vs steelcase",
 "best conference table","best boardroom table","best reception desk",
 "office chairs canada","best budget office chair",
]

def keyword_overview(keywords):
    return post("/v3/dataforseo_labs/google/keyword_overview/live",
                [{"keywords": keywords, "location_code": LOCATION_CANADA, "language_code": LANG}])

def bulk_kd(keywords):
    out = {}
    for i in range(0, len(keywords), 900):
        body = post("/v3/dataforseo_labs/google/bulk_keyword_difficulty/live",
                    [{"keywords": keywords[i:i+900], "location_code": LOCATION_CANADA, "language_code": LANG}])
        try:
            for it in body["tasks"][0]["result"][0]["items"]:
                out[it.get("keyword")] = it.get("keyword_difficulty")
        except Exception as e: print("kd err", e)
    return out

def serp(keyword, depth=20):
    return post("/v3/serp/google/organic/live/advanced",
                [{"keyword": keyword, "location_code": LOCATION_CANADA, "language_code": LANG,
                  "depth": depth, "people_also_ask_click_depth": 1}])

# Step C
print("STEP C: brand/material/value comparison overview on", len(BRAND_KW), "kw")
b = keyword_overview(BRAND_KW)
json.dump(b, open(os.path.join(RAW, "phase2c-brand-overview.json"), "w"))
rows = []
for it in b["tasks"][0]["result"][0]["items"]:
    ki = it.get("keyword_info", {}) or {}; si = it.get("search_intent_info", {}) or {}
    if ki.get("search_volume") is None: continue
    rows.append({"keyword": it.get("keyword"), "volume": ki.get("search_volume"),
                 "cpc": ki.get("cpc"), "competition": ki.get("competition_level"),
                 "intent": si.get("main_intent")})
kd = bulk_kd([r["keyword"] for r in rows])
for r in rows: r["kd"] = kd.get(r["keyword"])
rows.sort(key=lambda r: (r["volume"] or 0), reverse=True)
with open(os.path.join(OUT, "phase2-brand-comparison.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["keyword","volume","kd","cpc","competition","intent"]); w.writeheader(); w.writerows(rows)
print(f"  -> {len(rows)} brand/comparison kw with data. Top 20:")
for r in rows[:20]:
    print(f"     {r['keyword'][:40]:41s} vol={str(r['volume']):>5s} kd={str(r['kd']):>4s} {r['intent']}")

# Step D
print("\nSTEP D: live SERP reads on", len(SERP_KW), "priority clusters")
serp_rows = []; paa_rows = []
for kw in SERP_KW:
    body = serp(kw, depth=20)
    json.dump(body, open(os.path.join(RAW, f"serp-{kw.replace(' ','_').replace('/','-')}.json"), "w"))
    try:
        res = body["tasks"][0]["result"][0]
        items = res.get("items", []) or []
    except Exception as e:
        print(f"  !! {kw}: {e}"); continue
    feature_types = sorted(set(i.get("type") for i in items if i.get("type")))
    organic = [i for i in items if i.get("type") == "organic"]
    for i in organic[:10]:
        serp_rows.append({"keyword": kw, "position": i.get("rank_group"),
                          "domain": i.get("domain"), "title": (i.get("title") or "")[:80],
                          "url": (i.get("url") or "")[:120]})
    # PAA
    for i in items:
        if i.get("type") == "people_also_ask":
            for el in i.get("items", []) or []:
                paa_rows.append({"keyword": kw, "question": el.get("title")})
    has_ai = any(i.get("type") == "ai_overview" for i in items)
    has_fs = any(i.get("type") == "featured_snippet" for i in items)
    has_lp = any(i.get("type") == "local_pack" for i in items)
    has_shop = any(i.get("type") in ("shopping","popular_products","commercial_units") for i in items)
    print(f"  {kw[:34]:35s} feats: AIO={has_ai} FS={has_fs} LP={has_lp} SHOP={has_shop} | top3: {[o.get('domain') for o in organic[:3]]}")
    time.sleep(0.4)

with open(os.path.join(OUT, "phase2-serp-top10.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["keyword","position","domain","title","url"]); w.writeheader(); w.writerows(serp_rows)
with open(os.path.join(OUT, "phase2-serp-paa.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["keyword","question"]); w.writeheader(); w.writerows(paa_rows)
print(f"\n  -> {len(serp_rows)} SERP rows, {len(paa_rows)} PAA questions written")
print("DONE Phase 2 C+D")
