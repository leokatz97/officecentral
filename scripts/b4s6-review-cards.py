#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-6 — Phase 5 review-card generator.
Writes data/reports/b4s6-review-cards.md (before->after per product) + master table."""
import json, re, html
from pathlib import Path
ROOT = Path(".").resolve()

drafts = {d["handle"]: d for d in json.load(open("/tmp/b4s6_drafts_fixed.json"))["drafts"]}
man = json.load(open("/tmp/b4s6_batch.json"))
clusters = man["cluster_assignment"]
mvl = set(man["mvl_value_warranty_basis"])

def snap(h):
    p = ROOT/"data/backups"/f"session-6-{h}-pre-20260601-114715.json"
    return json.load(open(p)) if p.exists() else {}
def txt(h_):
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h_ or ""))).strip()

out = ["# B4S6 Review Cards — 26 Global-family PDPs (before → after)",
       "", "_Phase 5 batched review. QA gate: 0 FAILs / 0 WARNs. Warranty source-or-empty; lifetime only where sourced & never on value/MVL lines._", ""]

# ---- master table ----
out += ["## Master table", "",
  "| # | handle | sub-brand/line | cluster | source | warranty | locked KW | flags |",
  "|--|--|--|--|--|--|--|--|"]
for i,h in enumerate(man["handles"],1):
    d=drafts[h]
    rendered=(d.get("seo_title","")+" "+d.get("seo_description","")+" "+txt(d.get("body_html",""))).lower()
    locked=[t for t in ["office chairs for waiting room","waiting room chairs canada","boardroom table","conference table","executive desk"] if t in rendered]
    src={"success":"✓","partial":"~","fail":"✗"}.get(d.get("auto_source"),"?")
    w=d.get("warranty","") or "—(empty)"
    wshort = "lifetime+5yr" if "lifetime" in w.lower() else ("2yr" if w.startswith("2") else ("5yr" if w.startswith("5") else w[:14]))
    fl=";".join(f for f in d.get("flags",[]) if not f.startswith("source") )[:60]
    out.append(f"| {i} | {h[:40]} | {d.get('product_line','')} | {clusters.get(h,'')} | {src} | {wshort} | {','.join(locked) or '—'} | {fl} |")
out.append("")

# flag legend
out += ["## Flag legend","",
 "- `weight-unconfirmed` / `weight-capacity-unconfirmed` / `dims-unconfirmed` — spec not published on source; left empty (not invented).",
 "- `certs-unconfirmed` — no cert confirmable on source → `certifications=[]` (GREENGUARD never auto-applied).",
 "- `warr-unconfirmed*` — warranty left empty, source-or-empty rule.",
 "- `warr?-lifetime-vs-basics-value-NEEDS-LEO-DECISION` — chevron: lifetime applied but SKU may be Basics value (→2yr). **Your call.**",
 "- `warr-unconfirmed-dts-family-inconsistent` — table-18×28 / table-29×28 share SKU stem DTS1828P; agents diverged (one lifetime, one empty); both set EMPTY conservatively. **Your call on a value term.**",
 "- `cluster-mismatch:*` — agent corrected my cluster assignment (Craft = lounge poufs not tables; work-table = value table; sidero = guest chair). Re-tagged; zero forced keywords.",
 ""]

# ---- per-product cards ----
out += ["## Before → After cards",""]
FIELDS=["product_line","model_codes","dimensions","weight","weight_capacity","materials",
        "finishes_available","key_features","certifications","warranty","country_of_manufacture","who_its_for"]
for i,h in enumerate(man["handles"],1):
    d=drafts[h]; s=snap(h)
    s_specs=s.get("specs_metafields",{})
    out += [f"### {i}. {h}",
            f"- **SKU** `{s.get('variant_sku','')}` · **price** ${s.get('variant_price','')} · **status** {s.get('status','')} · **cluster** {clusters.get(h,'')} · **warranty-basis** {'OTG-VALUE' if h in mvl else 'GFG-PREMIUM'} · **source** {d.get('source_url_used','')}",
            "",
            f"**Title (SEO)** ({len(d.get('seo_title',''))}): `{d.get('seo_title','')}`  ",
            f"**Meta** ({len(d.get('seo_description',''))}): {d.get('seo_description','')}  ",
            f"**Manufacturer**: {d.get('manufacturer')} · **Line**: {d.get('product_line')}  ",
            f"**Dimensions**: {d.get('dimensions') or '—'} · **Weight**: {d.get('weight') or '—'} · **Cap**: {d.get('weight_capacity') or '—'} · **Made in**: {d.get('country_of_manufacture') or '—'}  ",
            f"**Warranty**: {d.get('warranty') or '—(empty, source-or-empty)'}  ",
            f"**Certifications**: {', '.join(d.get('certifications',[])) or '—(none confirmable)'}  ",
            f"**Materials**: {', '.join(d.get('materials',[]))}  ",
            f"**Finishes**: {', '.join(d.get('finishes_available',[]))}  ",
            f"**Key features**: " + "; ".join(d.get('key_features',[])) + "  ",
            f"**who_its_for**: {d.get('who_its_for','')}  ",
            f"**Locked KW landed**: {d.get('priority_keywords_landed',{})}  ",
            f"**Flags**: {', '.join(d.get('flags',[])) or 'none'}  ",
            "",
            f"**BODY before** ({len(txt(s.get('descriptionHtml','')))}c): {txt(s.get('descriptionHtml',''))[:240]}  ",
            "",
            f"**BODY after**:  ",
            "```html",
            d.get("body_html","")[:1400],
            "```",
            ""]

p = ROOT/"data/reports/b4s6-review-cards.md"
p.write_text("\n".join(out))
print(f"wrote {p} ({len(out)} lines)")
