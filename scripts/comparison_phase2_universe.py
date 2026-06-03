#!/usr/bin/env python3
"""PHASE 2 — Office-furniture COMPARISON keyword universe (DataForSEO REST-direct, Canada).

Step A: keyword_overview on a curated comparison-intent seed list (volume, CPC,
        competition, KD, search intent) across 9 categories x comparison patterns.
Step B: keyword_ideas expansion on category seeds to discover comparison long-tail.
Step C: brand-vs-brand + brand-review universe for the brands BBI carries.
Writes compact CSVs to data/reports/comparison-content/. Read-only.
"""
import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfs_client import post, LOCATION_CANADA, LANG

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "reports", "comparison-content")
RAW = os.path.join(OUT, "raw")

# ---- curated comparison-intent seeds (B2B/institutional lens, Canada) ----
SEEDS = [
 # ergonomic / task chairs
 "best office chair canada","best ergonomic office chair canada","best office chairs for long hours",
 "best office chair for sitting long hours","best ergonomic chair for back pain","best task chair",
 "best office chair for tall person","best office chair for heavy person","most comfortable office chair",
 "best office chair under 500","best budget office chair","ergonomic chair vs regular chair",
 "best commercial office chair","best office chair for 8 hours","best chair for office work",
 "best high back office chair","best mesh office chair","best office chair for posture",
 # executive / big-and-tall / 24-7
 "best executive office chair","best big and tall office chair","best 24 hour office chair",
 "best heavy duty office chair","heavy duty office chair","best office chair for big guys",
 # standing / height-adjustable desks
 "best standing desk canada","best standing desk for office","best electric standing desk",
 "best height adjustable desk","best sit stand desk","standing desk vs regular desk",
 "best standing desk under 1000","best adjustable desk canada","best office desk canada",
 "best executive desk","best l shaped desk","best computer desk for office",
 # benching / workstations
 "best office workstation","best benching system","best modular office furniture",
 "open plan office furniture","best office cubicles","cubicle vs open office",
 # conference / meeting tables
 "best conference table","best boardroom table","best meeting room furniture",
 "conference table buying guide","best boardroom chairs",
 # acoustic pods / booths
 "best office pods","best office phone booth","best acoustic pod","best meeting pod",
 "office pods canada","soundproof office pod","phone booth vs meeting pod","best office booth",
 # storage / filing
 "best filing cabinet","best office storage","filing cabinet alternatives","best lateral file cabinet",
 # reception / guest / lounge
 "best reception desk","best office reception furniture","best waiting room chairs","best lounge seating office",
 # supplier / dealer comparison (Ontario / Canada)
 "best office furniture stores canada","best office furniture toronto","office furniture suppliers ontario",
 "best office furniture company","top office furniture brands","best office furniture brands canada",
 "where to buy office furniture in canada","best place to buy office furniture",
 "commercial office furniture suppliers","office furniture dealers ontario",
 # commercial vs consumer / contract grade (durability axis)
 "commercial grade office furniture","contract furniture vs residential","commercial vs residential office chair",
 "office furniture for business","business office furniture","commercial office furniture",
 # canadian-made comparison (BBI moat)
 "canadian made office chairs","canadian office furniture brands","canadian office furniture manufacturers",
 "made in canada office furniture","best canadian office chair","canadian made office desks",
 # value / budget axis (B2B framing)
 "affordable office furniture canada","cheap office chairs canada","best value office chair",
 "office furniture for small business","best office furniture for startups",
]

# ---- expansion seeds for keyword_ideas (discover comparison long-tail) ----
IDEA_SEEDS = [
 "best office chair","ergonomic office chair","standing desk","office furniture canada",
 "office chair canada","conference table","office pod","filing cabinet",
 "executive chair","reception desk","heavy duty office chair","commercial office furniture",
]

def keyword_overview(keywords):
    payload = [{
        "keywords": keywords,
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
    }]
    return post("/v3/dataforseo_labs/google/keyword_overview/live", payload)

def keyword_ideas(seed_kw, limit=200):
    payload = [{
        "keywords": [seed_kw],
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "limit": limit,
        "filters": [["keyword_info.search_volume", ">=", 10]],
        "order_by": ["keyword_info.search_volume,desc"],
    }]
    return post("/v3/dataforseo_labs/google/keyword_ideas/live", payload)

def row_from_item(it):
    ki = it.get("keyword_info", {}) or {}
    kp = it.get("keyword_properties", {}) or {}
    si = it.get("search_intent_info", {}) or {}
    return {
        "keyword": it.get("keyword"),
        "volume": ki.get("search_volume"),
        "kd": kp.get("keyword_difficulty"),
        "cpc": ki.get("cpc"),
        "competition": ki.get("competition_level"),
        "intent": si.get("main_intent"),
        "intent_secondary": ",".join([str(x) for x in (si.get("foreign_intent") or [])]),
    }

def bulk_kd(keywords):
    """keyword_overview returns null KD; pull it from bulk_keyword_difficulty."""
    out = {}
    for i in range(0, len(keywords), 900):
        chunk = keywords[i:i+900]
        body = post("/v3/dataforseo_labs/google/bulk_keyword_difficulty/live", [{
            "keywords": chunk, "location_code": LOCATION_CANADA, "language_code": LANG,
        }])
        try:
            for it in body["tasks"][0]["result"][0]["items"]:
                out[it.get("keyword")] = it.get("keyword_difficulty")
        except Exception as e:
            print("  !! kd parse:", e)
    return out

# ---- Step A: curated seed overview ----
print("STEP A: keyword_overview on", len(SEEDS), "curated comparison seeds")
bodyA = keyword_overview(SEEDS)
json.dump(bodyA, open(os.path.join(RAW, "phase2-overview-curated.json"), "w"))
rowsA = []
try:
    for it in bodyA["tasks"][0]["result"][0]["items"]:
        rowsA.append(row_from_item(it))
except Exception as e:
    print("  !! overview parse error:", e)
rowsA = [r for r in rowsA if r["volume"] is not None]
# KD is null in keyword_overview -> merge from bulk_keyword_difficulty
kdmap = bulk_kd([r["keyword"] for r in rowsA])
for r in rowsA:
    r["kd"] = kdmap.get(r["keyword"])
rowsA.sort(key=lambda r: (r["volume"] or 0), reverse=True)
with open(os.path.join(OUT, "phase2-curated-seeds.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rowsA[0].keys())); w.writeheader(); w.writerows(rowsA)
print(f"  -> {len(rowsA)} seeds with Canada data. Top 15:")
for r in rowsA[:15]:
    print(f"     {(r['keyword'] or '')[:42]:43s} vol={str(r['volume']):>6s} kd={str(r['kd']):>4s} {r['competition']:>6} {r['intent']}")

# ---- Step B: keyword_ideas expansion ----
print("\nSTEP B: keyword_ideas expansion on", len(IDEA_SEEDS), "category seeds")
seen = set(r["keyword"] for r in rowsA)
ideas = []
for s in IDEA_SEEDS:
    body = keyword_ideas(s)
    json.dump(body, open(os.path.join(RAW, f"phase2-ideas-{s.replace(' ','_')}.json"), "w"))
    n = 0
    try:
        for it in body["tasks"][0]["result"][0]["items"]:
            kw = it.get("keyword","")
            r = row_from_item(it)
            r["seed"] = s
            ideas.append(r); n += 1
    except Exception as e:
        print(f"  !! ideas {s}: {e}")
    print(f"  {s:34s} -> {n} ideas")
    time.sleep(0.3)
with open(os.path.join(OUT, "phase2-keyword-ideas-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ideas[0].keys())); w.writeheader(); w.writerows(ideas)
print(f"  -> {len(ideas)} raw idea rows written")

# Filter ideas to comparison/intent-bearing patterns
PAT = ("best ","top "," vs ","review","comparison","compare","cheapest","affordable",
       "vs.","which ","most ","worth it","for office","for business","commercial","canadian","canada","ontario")
comp = [r for r in ideas if r["keyword"] and any(p in r["keyword"] for p in PAT)]
# dedupe by keyword, keep highest volume
dd = {}
for r in comp:
    k = r["keyword"]
    if k not in dd or (r["volume"] or 0) > (dd[k]["volume"] or 0):
        dd[k] = r
comp = sorted(dd.values(), key=lambda r: (r["volume"] or 0), reverse=True)
# merge KD for the filtered comparison set
kdmap2 = bulk_kd([r["keyword"] for r in comp])
for r in comp:
    r["kd"] = kdmap2.get(r["keyword"])
with open(os.path.join(OUT, "phase2-comparison-filtered.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(comp[0].keys())); w.writeheader(); w.writerows(comp)
print(f"  -> {len(comp)} comparison-pattern keywords (deduped) written")
print("\nDONE Phase 2 A+B")
