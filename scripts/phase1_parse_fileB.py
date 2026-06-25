#!/usr/bin/env python3
"""Parse brand keyword-suggestion + PAA pulls into compact tables for FILE B."""
import os, sys, json, re
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "research", "phase1-raw")
OUT = os.path.join(ROOT, "data", "research", "phase1-parsed")
os.makedirs(OUT, exist_ok=True)

# BBI ranked positions
def bbi_positions():
    b = json.load(open(os.path.join(RAW, "ranked__brantbusinessinteriors_com.json")))
    out = {}
    for it in b["tasks"][0]["result"][0]["items"] or []:
        kw = it["keyword_data"]["keyword"]
        se = (it.get("ranked_serp_element", {}) or {}).get("serp_item", {}) or {}
        out[kw] = se.get("rank_absolute") or se.get("rank_group")
    return out
BBI = bbi_positions()

def load_sugg(files):
    rows = {}
    for fn in files:
        p = os.path.join(RAW, f"sugg__{fn}.json")
        if not os.path.exists(p):
            continue
        b = json.load(open(p))
        try:
            items = b["tasks"][0]["result"][0]["items"] or []
        except Exception:
            items = []
        for it in items:
            kw = it.get("keyword", "") or (it.get("keyword_data") or {}).get("keyword","")
            ki = it.get("keyword_info") or (it.get("keyword_data") or {}).get("keyword_info") or {}
            vol = ki.get("search_volume") or 0
            comp = ki.get("competition_level") or ""
            intent = ((it.get("search_intent_info") or {}) or {}).get("main_intent","")
            if not kw:
                continue
            if kw not in rows or vol > rows[kw]["vol"]:
                rows[kw] = {"kw": kw, "vol": vol, "comp": comp, "intent": intent}
    return sorted(rows.values(), key=lambda x: -x["vol"])

BRANDS = {
  # carried -> (seed files, has_brand_page)
  "Global":      (["global_office_furniture","global_chair"], "global-teknion"),
  "OTG (Offices To Go)": (["otg_office_furniture","offices_to_go"], "otg"),
  "Teknion":     (["teknion"], "global-teknion"),
  "Humanscale":  (["humanscale"], None),
  "Keilhauer":   (["keilhauer"], "keilhauer"),
  "ergoCentric": (["ergocentric"], "ergocentric"),
  "Heartwood":   (["heartwood_furniture","heartwood_innovations"], "heartwood"),
  "ObusForme":   (["obusforme"], "obusforme"),
  "Safco":       (["safco","safco_products"], None),
  "FireKing":    (["fireking"], None),
  "Office Star": (["office_star","office_star_products"], None),
}
REFERENCE = {
  "Herman Miller": ["herman_miller"],
  "Steelcase":     ["steelcase"],
  "Haworth":       ["haworth_office"],
  "Nightingale":   ["nightingale_chair"],
}

def bbi_pos(kw):
    # exact or loose contains match
    if kw in BBI:
        return BBI[kw]
    return None

def emit(name, files, page):
    rows = load_sugg(files)
    rows = [r for r in rows if r["vol"] and r["vol"] > 0][:15]
    print(f"\n### {name}  (brand page: {page or 'NONE'})  — {len(rows)} terms vol>0")
    if not rows:
        print("   (near-zero measured brand demand)")
        return
    for r in rows:
        bp = bbi_pos(r["kw"])
        bp = f"p{bp}" if bp else "absent"
        print(f"   vol{r['vol']:>6} {r['comp']:<7} {r['intent'][:13]:<13} {bp:<7} {r['kw']}")

print("="*70)
print("CARRIED BRANDS (actionable)")
print("="*70)
for name,(files,page) in BRANDS.items():
    emit(name, files, page)

print("\n"+"="*70)
print("REFERENCE-ONLY (NON-CARRIED) — demand sizing, NOT page targets")
print("="*70)
for name, files in REFERENCE.items():
    emit(name, files, None)

# ---- PAA extraction ----
print("\n"+"="*70)
print("PAA QUESTIONS per brand query")
print("="*70)
for fn in sorted(os.listdir(RAW)):
    if not fn.startswith("paa__"):
        continue
    b = json.load(open(os.path.join(RAW, fn)))
    qs = []
    try:
        items = b["tasks"][0]["result"][0]["items"] or []
    except Exception:
        items = []
    aio = False
    for it in items:
        t = it.get("type")
        if t == "people_also_ask":
            for el in it.get("items", []) or []:
                q = el.get("title")
                if q: qs.append(q)
        if t == "ai_overview":
            aio = True
    label = fn.replace("paa__","").replace(".json","").replace("_"," ")
    print(f"\n[{label}]  AI-Overview={'YES' if aio else 'no'}")
    for q in qs[:8]:
        print(f"   Q: {q}")
