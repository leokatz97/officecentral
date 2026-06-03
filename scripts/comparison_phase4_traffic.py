#!/usr/bin/env python3
"""PHASE 4 — honest traffic model for the comparison-post portfolio.

MODELLED, not measured. Inputs:
  - cluster_vol_est per post (Phase 2/3, DataForSEO-grounded)
  - serp_tier + primary KD -> expected steady-state position band
  - CTR-by-position curve (cited assumption)
  - AI-Overview discount where AIO present on the SERP (Phase 2 SERP reads)
  - long-tail multiplier: a comparison page ranks for a CLUSTER, not one kw
    (measured: Venn flagship ranked for 70 kw / total ETV ~6x its primary-kw ETV)
Outputs conservative + expected monthly organic VISITS at ~12-18mo steady state.
"""
import csv, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "reports", "comparison-content")

# Blended organic CTR by position. Source (modelled): Advanced Web Ranking 2024
# aggregate + Backlinko 2023; blended desktop/mobile, commercial/informational.
CTR = {1:0.28,2:0.15,3:0.11,4:0.08,5:0.06,6:0.045,7:0.035,8:0.03,9:0.025,10:0.022,
       12:0.015,15:0.010,20:0.006}
def ctr(pos):
    ks=sorted(CTR);
    for k in ks:
        if pos<=k: return CTR[k]
    return 0.004

# Expected steady-state position band by tier (BBI near-zero authority calibration:
# 49 ranked kw, ETV ~60/mo, 0 top-3 -> conservative). conservative=worse, expected=better.
# (cons_pos, exp_pos)
BAND = {"WIN":(8,4), "MID":(12,7), "HARD":(18,12)}

# AIO present on these primary SERPs (from Phase 2 SERP reads) -> discount factor
AIO_POSTS = {"C1":1.0,"C2":1.0,"C3":0.65,"C4":1.0,"C5":1.0,"C6":1.0,"C7":0.7,"C8":0.6,
             "C9":1.0,"C10":1.0,"C11":0.6,"C12":0.6,"C13":1.0,"C14":0.65,"C15":0.6,
             "C16":0.6,"C17":0.6}

# Long-tail capture multiplier: total page traffic vs primary-kw-only.
# Measured anchor: Venn flagship page ranked for 70 kw with total ETV ~6x primary.
# Conservative 2.5x, expected 4.0x (BBI thinner topical authority than Venn).
LT_CONS, LT_EXP = 2.5, 4.0

rows=list(csv.DictReader(open(os.path.join(OUT,"phase3-scored-candidates.csv"))))
out=[]; tot_c=tot_e=0
for r in rows:
    vol=float(r["cluster_vol_est"]); tier=r["serp_tier"]; cid=r["id"]
    cons_pos,exp_pos=BAND[tier]
    aio=AIO_POSTS.get(cid,1.0)
    # primary cluster volume already aggregates the cluster, so use modest LT on top
    cons = vol*ctr(cons_pos)*aio*1.0
    exp  = vol*ctr(exp_pos)*aio*(LT_EXP/LT_CONS)  # expected leans on deeper long-tail
    out.append({"id":cid,"title":r["title"][:48],"tier":tier,"cluster_vol":int(vol),
                "cons_pos":cons_pos,"exp_pos":exp_pos,"aio_disc":aio,
                "cons_visits_mo":round(cons),"exp_visits_mo":round(exp)})
    tot_c+=cons; tot_e+=exp
out.sort(key=lambda r:-r["exp_visits_mo"])
with open(os.path.join(OUT,"phase4-traffic-model.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print(f"{'id':4s}{'tier':6s}{'cvol':>6s}{'cons/mo':>9s}{'exp/mo':>8s}  title")
for r in out:
    print(f"{r['id']:4s}{r['tier']:6s}{r['cluster_vol']:>6d}{r['cons_visits_mo']:>9d}{r['exp_visits_mo']:>8d}  {r['title']}")
print(f"\nPORTFOLIO TOTAL (17 posts, ~12-18mo steady state):")
print(f"  conservative ~{round(tot_c):,}/mo   expected ~{round(tot_e):,}/mo")
print(f"  Top-8 ranked posts only: cons ~{round(sum(sorted([o['cons_visits_mo'] for o in out],reverse=True)[:8])):,}/mo "
      f"exp ~{round(sum(sorted([o['exp_visits_mo'] for o in out],reverse=True)[:8])):,}/mo")
