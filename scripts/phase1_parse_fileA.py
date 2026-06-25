#!/usr/bin/env python3
"""Parse Phase-1 competitor ranked-keyword raw pulls into compact tables for FILE A.
Outputs to data/research/phase1-parsed/. No network.
"""
import os, sys, json, csv, re
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "research", "phase1-raw")
OUT = os.path.join(ROOT, "data", "research", "phase1-parsed")
os.makedirs(OUT, exist_ok=True)

COMPS = ["poi_ca", "theofficeshop_ca", "atwork_ca", "sourceofficefurniture_ca",
         "grandandtoy_com", "staples_ca"]
BBI = "brantbusinessinteriors_com"

def load_items(slug):
    p = os.path.join(RAW, f"ranked__{slug}.json")
    if not os.path.exists(p):
        return []
    b = json.load(open(p))
    try:
        return b["tasks"][0]["result"][0]["items"] or []
    except Exception:
        return []

def page_type(url):
    u = (url or "").lower()
    if re.search(r"/(blogs?|news|articles?|resources|learn|guides?)/", u):
        return "BLOG"
    if "/products/" in u or "/product/" in u or re.search(r"/p/|/ip/", u):
        return "PDP"
    if re.search(r"/(collections?|product-category|category|categories|c/|shop)/", u):
        return "COLLECTION"
    # homepage or /pages/
    if u.rstrip("/").count("/") <= 3:
        return "LANDING(home)"
    return "LANDING"

def row(it):
    kd = it.get("keyword_data", {})
    ki = kd.get("keyword_info", {}) or {}
    se = (it.get("ranked_serp_element", {}) or {}).get("serp_item", {}) or {}
    intent = ((kd.get("search_intent_info") or {}).get("main_intent") or "")
    return {
        "keyword": kd.get("keyword", ""),
        "volume": ki.get("search_volume") or 0,
        "kd": (ki.get("competition_level") or ""),
        "position": se.get("rank_absolute") or se.get("rank_group") or 0,
        "etv": round(se.get("etv") or 0, 1),
        "url": se.get("url") or "",
        "type": page_type(se.get("url")),
        "intent": intent,
    }

# ---- Per-competitor: write keyword rows + top pages ----
bbi_items = {r["keyword"]: r for r in (row(i) for i in load_items(BBI))}
print(f"BBI ranks for {len(bbi_items)} keywords (top positions):")
for k, v in sorted(bbi_items.items(), key=lambda x: x[1]["position"])[:60]:
    print(f"  p{v['position']:>3} vol{v['volume']:>6}  {k}  [{v['type']}]")

all_comp_kw = defaultdict(lambda: {"vol": 0, "comps": set(), "best_pos": {}})
summary = {}
for slug in COMPS:
    items = [row(i) for i in load_items(slug)]
    items = [r for r in items if r["keyword"]]
    # top pages: aggregate by url
    pages = defaultdict(lambda: {"etv": 0.0, "kws": []})
    for r in items:
        pages[r["url"]]["etv"] += r["etv"]
        pages[r["url"]]["kws"].append(r)
    toppages = []
    for url, d in pages.items():
        best = max(d["kws"], key=lambda x: x["etv"])
        toppages.append({"url": url, "etv": round(d["etv"],1), "nkw": len(d["kws"]),
                         "primary_kw": best["keyword"], "vol": best["volume"],
                         "pos": best["position"], "type": best["type"]})
    toppages.sort(key=lambda x: -x["etv"])
    summary[slug] = {"nkw": len(items), "toppages": toppages[:30], "kws": items}
    # write csv
    with open(os.path.join(OUT, f"comp_{slug}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["keyword","volume","kd","position","etv","type","intent","url"])
        w.writeheader()
        for r in sorted(items, key=lambda x:-x["etv"]):
            w.writerow(r)
    # accumulate for gap
    for r in items:
        e = all_comp_kw[r["keyword"]]
        e["vol"] = max(e["vol"], r["volume"])
        e["comps"].add(slug)
        e["best_pos"][slug] = r["position"]

# ---- GAP: comp keywords where BBI absent or > pos 20 ----
gap = []
for kw, e in all_comp_kw.items():
    bpos = bbi_items.get(kw, {}).get("position", 0)
    bbi_absent = kw not in bbi_items or bpos > 20
    if not bbi_absent:
        continue
    score = e["vol"] * len(e["comps"])
    gap.append({"keyword": kw, "volume": e["vol"], "ncomp": len(e["comps"]),
                "score": score, "comps": ",".join(sorted(s.replace("_ca","").replace("_com","") for s in e["comps"])),
                "bbi_pos": bpos if bpos else "absent"})
gap.sort(key=lambda x: -x["score"])
with open(os.path.join(OUT, "gap.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["keyword","volume","ncomp","score","comps","bbi_pos"])
    w.writeheader()
    for r in gap:
        w.writerow(r)

# ---- print compact summaries ----
print("\n=== TOP PAGES per competitor (by est. traffic) ===")
for slug in COMPS:
    s = summary[slug]
    print(f"\n--- {slug} ({s['nkw']} kw in top20) ---")
    for p in s["toppages"][:12]:
        rel = re.sub(r"^https?://[^/]+", "", p["url"]) or "/"
        print(f"  etv{p['etv']:>6} nkw{p['nkw']:>3} [{p['type']:<13}] p{p['pos']:>3} vol{p['vol']:>6}  {p['primary_kw']}  -> {rel[:60]}")

print(f"\n=== CONTENT GAP (BBI absent/>20) — {len(gap)} terms, top 50 by vol×ncomp ===")
for r in gap[:50]:
    print(f"  score{r['score']:>7} vol{r['volume']:>6} n{r['ncomp']}  {r['keyword']}  [{r['comps']}] bbi={r['bbi_pos']}")
print("\nWrote:", OUT)
