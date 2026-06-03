#!/usr/bin/env python3
"""PHASE 3 — transparent weighted scoring of comparison-post candidates.

Candidate fields are grounded in the measured DataForSEO data (Phase 2 CSVs) and
the live SERP reads. Each dimension is scored 1-5 with the rationale encoded; the
weighted total drives the ranking. Reproducible -> the ranking is defensible.
Outputs data/reports/comparison-content/phase3-scored-candidates.csv
"""
import csv, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "reports", "comparison-content")

# weights (sum=1.0). Winnability + fit + conversion weighted over raw volume,
# because BBI is a near-zero-authority regional B2B dealer (ETV ~60/mo, 0 top-3).
W = {"winnability":0.25, "northstar":0.20, "conversion":0.20, "volume":0.15, "aeo":0.10, "intent":0.10}

# candidates: (id, title, primary_kw, cluster_vol, primary_kd, serp_tier, scores...)
# serp_tier: WIN=dealer/.ca SERP no US-review lock; MID=one review giant; HARD=US review-giant+Reddit lock
# scores are 1-5: vol, intent(comparison/commercial), win, north(B2B/Ontario fit), conv(routing+$), aeo
C = [
 # id, title, primary_kw(vol/kd), cluster_vol, serp_tier, vol,int,win,north,conv,aeo, route
 ("C1","Best Standing & Sit-Stand Desks for Canadian Offices","best standing desk canada (480/KD3)",3900,"WIN",
   5,4,5,4,4,3,"height-adjustable-tables (200)"),
 ("C2","Best Office Pods, Phone Booths & Acoustic Booths for Canadian Offices","office pods canada (140/KD0)",1270,"WIN",
   4,4,5,5,5,3,"acoustic-pods (200)"),
 ("C3","Best Canadian-Made Office Chairs & Furniture (Buy-Canadian Guide)","canadian made office chairs (140/KD0)",460,"WIN",
   3,4,5,5,5,4,"buy-canadian (200)"),
 ("C4","Best Heavy-Duty, Big-and-Tall & 24/7 Office Chairs","heavy duty office chair (170/KD0)",340,"WIN",
   3,4,5,5,4,3,"seating (200)"),
 ("C5","Commercial vs Consumer-Grade Office Furniture: A Business Buyer's Guide","commercial office furniture (90/KD0)",300,"WIN",
   3,4,5,5,5,4,"seating/desks + quote"),
 ("C6","Best Conference & Boardroom Tables for Canadian Meeting Rooms","boardroom tables (880/KD?)",1700,"WIN",
   4,4,4,5,5,3,"boardroom + meeting-tables (200)"),
 ("C7","Best Reception & Waiting-Room Furniture for Canadian Offices","reception desk (2900/nav)",3100,"WIN",
   5,3,4,5,5,3,"reception-desks-desks (200)"),
 ("C8","Best Office Chairs for Long Hours: A Canadian Business Buyer's Guide","best office chairs for long hours (260/KD8)",2300,"MID",
   5,5,3,4,4,5,"seating (200)"),
 ("C9","Best Ergonomic Office Chairs in Canada (Commercial Buyer's Guide)","best ergonomic office chair canada (320/KD6)",1600,"MID",
   4,5,3,4,4,5,"seating (200)"),
 ("C10","Where to Buy Office Furniture in Toronto & Ontario (Supplier Comparison)","best office furniture toronto (20/geo)",600,"WIN",
   3,4,4,5,5,3,"quote + geo pages (LP)"),
 ("C11","Affordable Office Furniture for Small Business & Startups (Canada)","best budget office chair (590/KD24)",1900,"MID",
   4,5,3,5,5,4,"budget collections + quote"),
 ("C12","Cubicle vs Open-Plan vs Hybrid: An Office-Layout Comparison","cubicle vs open office (20/KD?)",120,"WIN",
   2,4,5,5,4,5,"design-services + workstations"),
 ("C13","Best Modular Office Furniture & Benching for Growing Teams","best modular office furniture (?/?)",250,"WIN",
   2,4,4,5,5,3,"desks (benching 301->desks)"),
 ("C14","Best Executive Office Chairs & Desks for Leadership Offices","best executive office chair (70/KD11)",400,"MID",
   3,4,3,4,5,3,"executive-desks + seating (200)"),
 ("C15","Most Comfortable Office Chairs / Best for Back Pain (Business)","most comfortable office chair (590/KD19)",1700,"HARD",
   4,5,2,3,4,5,"seating (200)"),
 ("C16","Premium Office Chair Showdown: Herman Miller vs Steelcase vs Canadian-Made","herman miller vs steelcase (90/KD0)",350,"MID",
   3,5,3,3,4,5,"seating (BBI carries all 3)"),
 ("C17","Best Office Filing Cabinets & Storage for Business","best filing cabinet (30/KD0)",200,"MID",
   2,3,3,3,4,4,"storage (200)"),
]

rows=[]
for (cid,title,pk,cvol,tier,vol,intn,win,north,conv,aeo,route) in C:
    total = (vol*W["volume"]+intn*W["intent"]+win*W["winnability"]
             +north*W["northstar"]+conv*W["conversion"]+aeo*W["aeo"])
    rows.append({"id":cid,"title":title,"primary_kw":pk,"cluster_vol_est":cvol,"serp_tier":tier,
                 "s_volume":vol,"s_intent":intn,"s_winnability":win,"s_northstar":north,
                 "s_conversion":conv,"s_aeo":aeo,"route":route,"WEIGHTED":round(total,2)})
rows.sort(key=lambda r:-r["WEIGHTED"])
with open(os.path.join(OUT,"phase3-scored-candidates.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

print("RANK  SCORE  TIER  ID   TITLE")
for i,r in enumerate(rows,1):
    print(f"{i:>3}.  {r['WEIGHTED']:>4}  {r['serp_tier']:<4} {r['id']:<4} {r['title'][:58]}")
print("\nweights:",W)
print("wrote phase3-scored-candidates.csv")
