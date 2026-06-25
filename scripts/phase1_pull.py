#!/usr/bin/env python3
"""Phase 1 research pull — competitor gap + carried-brand demand (BBI).
Read-only DataForSEO Labs + SERP pulls. Saves raw JSON under data/research/phase1-raw/.
Reuses scripts/dfs_client.py (creds from .mcp.json). No writes to Shopify, no theme.
"""
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfs_client import post, LOCATION_CANADA, LANG, ROOT

RAW = os.path.join(ROOT, "data", "research", "phase1-raw")
os.makedirs(RAW, exist_ok=True)

def save(name, obj):
    p = os.path.join(RAW, name)
    json.dump(obj, open(p, "w"), indent=1)
    sc = obj.get("status_code")
    try:
        n = len(obj["tasks"][0]["result"][0]["items"])
    except Exception:
        n = "?"
    print(f"  saved {name}  sc={sc} items={n} cost={obj.get('cost')}")
    return p

KWFILTER = "office|chair|desk|furniture|seating|workstation|filing|cubicle|boardroom|reception|table|cabinet|ergonomic|stool|pedestal|bookcase|panel|lobby|lounge|locker"

def ranked(target, big_retailer=False, limit=70):
    flt = [["ranked_serp_element.serp_item.rank_group", "<=", 20]]
    if big_retailer:
        flt = [["ranked_serp_element.serp_item.rank_group", "<=", 20], "and",
               ["keyword_data.keyword", "regex", KWFILTER]]
    payload = [{
        "target": target,
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "limit": limit,
        "filters": flt,
        "order_by": ["ranked_serp_element.serp_item.etv,desc"],
        "ignore_synonyms": True,
    }]
    return post("/v3/dataforseo_labs/google/ranked_keywords/live", payload)

def ranked_all(target, limit=1000):
    payload = [{
        "target": target,
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "limit": limit,
        "order_by": ["ranked_serp_element.serp_item.rank_group,asc"],
        "ignore_synonyms": True,
    }]
    return post("/v3/dataforseo_labs/google/ranked_keywords/live", payload)

def kw_suggestions(seed, limit=60):
    payload = [{
        "keyword": seed,
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "limit": limit,
        "include_serp_info": False,
        "filters": [["keyword_info.search_volume", ">", 0]],
        "order_by": ["keyword_info.search_volume,desc"],
    }]
    return post("/v3/dataforseo_labs/google/keyword_suggestions/live", payload)

def serp_paa(keyword):
    payload = [{
        "keyword": keyword,
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "depth": 20,
        "people_also_ask_click_depth": 2,
    }]
    return post("/v3/serp/google/organic/live/advanced", payload)

# ---- FILE A: competitors + BBI ----
COMPETITORS = {
    "poi.ca": False,
    "poibusinessinteriors.com": False,
    "theofficeshop.ca": False,
    "atwork.ca": False,
    "sourceofficefurniture.ca": False,
    "sourceofficefurniture.com": False,
    "grandandtoy.com": True,
    "staples.ca": True,
}

# ---- FILE B: brands ----
CARRIED = ["Global office furniture", "OTG office furniture", "Teknion",
           "Humanscale", "Keilhauer", "ergoCentric", "Heartwood furniture",
           "ObusForme", "Safco", "FireKing", "Office Star"]
REFERENCE = ["Herman Miller", "Steelcase", "Haworth office", "Nightingale chair"]

def run_competitors():
    print("== FILE A: competitor ranked keywords ==")
    for dom, big in COMPETITORS.items():
        try:
            b = ranked(dom, big_retailer=big, limit=70)
            save(f"ranked__{dom.replace('.','_')}.json", b)
        except Exception as e:
            print(f"  ERR {dom}: {e}")
        time.sleep(2)
    print("== BBI full ranked ==")
    b = ranked_all("brantbusinessinteriors.com", limit=1000)
    save("ranked__brantbusinessinteriors_com.json", b)

def run_brands():
    print("== FILE B: brand suggestions ==")
    for seed in CARRIED + REFERENCE:
        try:
            b = kw_suggestions(seed, limit=60)
            slug = seed.lower().replace(" ", "_")
            save(f"sugg__{slug}.json", b)
        except Exception as e:
            print(f"  ERR {seed}: {e}")
        time.sleep(2)

def run_paa():
    print("== FILE B: brand PAA SERP ==")
    PAA_QUERIES = ["global office chair", "otg office chair", "teknion office furniture",
                   "humanscale office chair", "keilhauer chairs", "ergocentric chair",
                   "heartwood office furniture", "obusforme office chair", "safco products",
                   "fireking filing cabinet", "office star chair",
                   "herman miller chair canada", "steelcase canada", "haworth chair",
                   "nightingale office chair"]
    for q in PAA_QUERIES:
        try:
            b = serp_paa(q)
            slug = q.lower().replace(" ", "_")
            save(f"paa__{slug}.json", b)
        except Exception as e:
            print(f"  ERR {q}: {e}")
        time.sleep(2)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "comp"):
        run_competitors()
    if which in ("all", "brands"):
        run_brands()
    if which in ("all", "paa"):
        run_paa()
    print("DONE", which)
