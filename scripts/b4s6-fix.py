#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-6 — Phase 5 mechanical fixes on drafts (no writes).
Applies QA corrections, writes /tmp/b4s6_drafts_fixed.json. Substantive warranty
uncertainties (chevron, DTS table twins) are CONSERVATIVELY handled + flagged for Leo."""
import json, re, html
from pathlib import Path

data = json.load(open("/tmp/b4s6_drafts.json"))
drafts = {d["handle"]: d for d in data["drafts"]}
man = json.load(open("/tmp/b4s6_batch.json"))

# 1) Meta rewrites (all asserted <=160 below). moda was empty.
META = {
 "guest-chair-6960-moda": "Global Moda 6960 guest chair: molded-shell, designer office chairs for waiting room, lobby and reception areas. Made in Canada, OECM-eligible.",
 "stream-armchair-polypropylene-seat-back-2075app-1": "Stream 2075APP polypropylene stacking armchair: durable, wipe-clean office chairs for waiting room, lobby and training spaces. Made in Canada.",
 "stream-armless-chair-polypropylene-seat-back-2075app": "Global Stream 2075APP armless polypropylene stacking chair: easy-clean office chairs for waiting room and training spaces. Stacks 5 high.",
 "the-twilight-armchair-wood-veneer-back-2198ws": "Global Twilight 2198WS armchair with a flared wood-veneer back and foam seat: polished guest seating for Canadian reception and meeting spaces.",
 "solo-gues-chair": "Global Solo 5225 guest chair: durable, comfortable office chairs for waiting room and reception areas. OECM-eligible. Request a quote.",
 "craft-round-20-unit": "Craft Round 20-inch upholstered modular pouf: reconfigurable lounge seating for reception and collaborative spaces. Made in Canada. Request a quote.",
 "luray-executive-chair": "Global Luray executive chair: generous proportions, full back support and a Soft Descent lift. A premium ergonomic office chair built for long days.",
 "sidero-1": "Global Sidero multi-purpose stacking chair with a wallsaver steel frame and waterfall foam seat: built for clinics, waiting rooms and training spaces.",
 "echo-medium-back-multi-tilter-3671-3-1": "Echo 3671-3 ergonomic task chair with back, lumbar, seat and arm adjustment to fit any body. Made in Canada, OECM-eligible. Request a quote.",
 "chevron-ultra-medium-back-multi-tilter-chair": "Ergonomic medium-back multi-tilter office chair with seat-depth, back-angle and tilt control. Made in Canada, 300 lb capacity, OECM-eligible.",
 "yoho-armless-drafting-task-chair-stool": "Global Yoho armless drafting stool: pneumatic lift to 33.5 inches, compound-curved back and chromed footrest for standing-height workstations.",
}
for h,m in META.items():
    assert len(m) <= 160, f"{h} meta {len(m)}>160"
    drafts[h]["seo_description"] = m

# 2) Reconcile priority_keywords_landed to ONLY locked terms genuinely in rendered copy
LOCKED_ALL = ["office chairs for waiting room","waiting room chairs canada","boardroom table",
              "conference table","wood boardroom table","conference table canada","executive desk",
              "executive office desk","l-shaped executive desk","executive desk canada","wood executive desk"]
def strip_html(h):
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h or ""))).strip()
for h,d in drafts.items():
    rendered = (d.get("seo_title","")+" "+d.get("seo_description","")+" "+strip_html(d.get("body_html",""))).lower()
    landed = d.get("priority_keywords_landed",{}) or {"title":[],"meta":[],"body":[]}
    for slot, src in (("title",d.get("seo_title","")),("meta",d.get("seo_description","")),("body",strip_html(d.get("body_html","")))):
        landed[slot] = [t for t in LOCKED_ALL if t.lower() in (src or "").lower()]
    d["priority_keywords_landed"] = landed

# 3) echo body<->warranty sync: insert warranty sentence into Specifications/closing if absent
e = drafts["echo-medium-back-multi-tilter-3671-3-1"]
if "lifetime" not in e["body_html"].lower():
    warr_sent = " Backed by a limited lifetime warranty on the frame and components, 12 years on control mechanisms, with 5 years on upholstery, foam and mesh."
    # insert before the last </p>
    idx = e["body_html"].rfind("</p>")
    if idx != -1:
        e["body_html"] = e["body_html"][:idx] + warr_sent + e["body_html"][idx:]

# 4) Re-tag agent-discovered reclassifications (Craft x3 + work-table + rambler) OUT of boardroom
RETAG = {
 "craft-round-20-unit": ("lounge-seating","type:lounge-seating"),
 "craft-wedge-unit": ("lounge-seating","type:lounge-seating"),
 "craft-wedge-overtable-chrome-leg-1": ("lounge-seating","type:lounge-seating"),
 "work-table-at": ("table","type:table"),
 "rambler-ottoman-8-shape-size-options": ("lounge-seating","type:lounge-seating"),
}
for h,(newcluster,typetag) in RETAG.items():
    d=drafts[h]
    tags=[t for t in d.get("tags",[]) if not (t.startswith("type:conference") or t=="type:boardroom")]
    if typetag not in tags: tags.append(typetag)
    d["tags"]=tags
    man["cluster_assignment"][h]=newcluster

# 5) DTS table twins — same SKU stem DTS1828P, inconsistent warranty. Conservative source-or-empty:
#    one was lifetime (unsourced-confidently), one empty. Set BOTH empty + flag for Leo.
for h in ["table-18x28","table-29-x-28-3"]:
    d=drafts[h]
    d["warranty"]=""
    # strip any warranty sentence from body
    d["body_html"]=re.sub(r'[^.<>]*\b(lifetime|\d+\s*-?\s*year)[^.<]*\.',"",d["body_html"],flags=re.I)
    fl=set(d.get("flags",[])); fl.add("warr-unconfirmed-dts-family-inconsistent"); d["flags"]=sorted(fl)

# 6) chevron — keep lifetime but flag prominently for Leo decision (do NOT silently change)
c=drafts["chevron-ultra-medium-back-multi-tilter-chair"]
fl=set(c.get("flags",[])); fl.add("warr?-lifetime-vs-basics-value-NEEDS-LEO-DECISION"); c["flags"]=sorted(fl)

json.dump({"ts":data["ts"],"count":len(drafts),"drafts":list(drafts.values())},
          open("/tmp/b4s6_drafts_fixed.json","w"),indent=2)
json.dump(man, open("/tmp/b4s6_batch.json","w"), indent=2)  # persist re-tagged clusters
print("fixes applied -> /tmp/b4s6_drafts_fixed.json")
print("meta rewrites:",len(META)," retagged:",len(RETAG)," DTS twins emptied:2  chevron flagged")
