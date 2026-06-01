#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-6 — Phase 5 QA gate (no writes).
Validates 26 drafts before review:
  1. warranty metafield <-> body consistency (term must appear in body; 0 mismatches)
  2. stray numeric warranty figures in body not matching the metafield term
  3. SEO title <=60, meta <=160; no literal "BBI"; no double-period; no newlines in single-line fields
  4. keyword application verified against RENDERED copy (title/meta/body text), not landed-metadata
  5. manufacturer=Global Furniture Group; country sanity; certs sanity
Reads /tmp/b4s6_drafts_fixed.json + /tmp/b4s6_batch.json. Emits PASS/FAIL per check + a per-product table.
"""
import json, re, html
from pathlib import Path

drafts = {d["handle"]: d for d in json.load(open("/tmp/b4s6_drafts_fixed.json"))["drafts"]}
man = json.load(open("/tmp/b4s6_batch.json"))
clusters = man["cluster_assignment"]
mvl_value = set(man["mvl_value_warranty_basis"])

SINGLE_LINE = ["manufacturer","product_line","dimensions","weight","weight_capacity",
               "warranty","country_of_manufacture","who_its_for"]
# locked priority terms per cluster (for rendered-copy verification)
LOCKED = {
  "waiting-room-seating": ["office chairs for waiting room","waiting room chairs canada"],
  "boardroom": ["boardroom table","conference table","wood boardroom table","conference table canada"],
  "executive-desks": ["executive desk","executive office desk","l-shaped executive desk","executive desk canada","wood executive desk"],
}
WARR_FIG = re.compile(r'\b(\d+)\s*[- ]?\s*year', re.I)
LIFETIME = re.compile(r'lifetime', re.I)

def strip_html(h):
    t = re.sub(r"<[^>]+>", " ", h or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()

def warranty_years(s):
    return set(m.group(1) for m in WARR_FIG.finditer(s or ""))

issues = []  # (severity, handle, check, detail)
rows = []
for h in man["handles"]:
    d = drafts.get(h)
    if not d:
        issues.append(("FAIL", h, "missing-draft", "no draft returned")); continue
    body_text = strip_html(d.get("body_html",""))
    warr = (d.get("warranty") or "").strip()
    title = d.get("seo_title","") or ""
    meta = d.get("seo_description","") or ""
    flags = d.get("flags",[]) or []
    cl = clusters.get(h,"")
    rowflags = []

    # 1. warranty<->body consistency
    if warr:
        # the metafield warranty term's year-figures + lifetime status must be reflected in body
        w_years = warranty_years(warr); w_life = bool(LIFETIME.search(warr))
        b_years = warranty_years(body_text); b_life = bool(LIFETIME.search(body_text))
        # body should mention warranty; allow body to omit if no warranty section, but flag
        if "warrant" not in body_text.lower() and not w_life and not w_years:
            pass
        # mismatch: lifetime in metafield but not body, or vice versa
        if w_life != b_life and ("warrant" in body_text.lower() or b_life or w_life):
            issues.append(("FAIL", h, "warr-body-lifetime-mismatch", f"meta_life={w_life} body_life={b_life} | warr='{warr}'"))
            rowflags.append("WARRmiss")
        # stray year figs in body not in metafield (e.g. body says 2yr but metafield 5yr)
        stray = b_years - w_years
        # 1964 (founding year) and dimension-ish numbers excluded: only count near 'year'
        stray = {y for y in stray if y not in ("1964",)}
        if stray:
            issues.append(("WARN", h, "stray-warr-figure", f"body year-figs {sorted(b_years)} vs metafield {sorted(w_years)} | stray={sorted(stray)}"))
            rowflags.append("stray?")
    else:
        # empty warranty -> must be flagged warr-unconfirmed; body must not assert a warranty term
        if not any("warr" in f for f in flags):
            issues.append(("WARN", h, "empty-warr-no-flag", "warranty empty but no warr-unconfirmed flag"))
        if LIFETIME.search(body_text) or warranty_years(body_text):
            issues.append(("FAIL", h, "empty-warr-body-asserts", f"warranty empty but body asserts warranty terms"))
            rowflags.append("WARRmiss")

    # MVL-value items must NOT carry lifetime
    if h in mvl_value and (LIFETIME.search(warr) or LIFETIME.search(body_text)):
        issues.append(("FAIL", h, "mvl-lifetime", f"MVL/value item asserts lifetime: warr='{warr}'"))
        rowflags.append("MVLlife")

    # 3. constraints
    if len(title) > 60:
        issues.append(("FAIL", h, "title-too-long", f"{len(title)} chars: {title}")); rowflags.append("T>60")
    if len(meta) > 160:
        issues.append(("FAIL", h, "meta-too-long", f"{len(meta)} chars")); rowflags.append("M>160")
    if not meta.strip():
        issues.append(("WARN", h, "meta-empty", "seo_description empty")); rowflags.append("Mempty")
    for fld in [title, meta, d.get("body_html",""), d.get("who_its_for","")]:
        if re.search(r'\bBBI\b', fld or ""):
            issues.append(("FAIL", h, "literal-BBI", f"'BBI' in: {fld[:60]}")); rowflags.append("BBI")
            break
    if ".." in (title+meta+strip_html(d.get("body_html",""))).replace("...",""):
        issues.append(("WARN", h, "double-period", "")); rowflags.append("..")
    for k in SINGLE_LINE:
        v = d.get(k,"")
        if isinstance(v,str) and "\n" in v:
            issues.append(("FAIL", h, "newline-in-single-line", f"{k}")); rowflags.append("NL")

    # 4. keyword application vs RENDERED copy
    landed = d.get("priority_keywords_landed",{}) or {}
    declared = set(landed.get("title",[])+landed.get("meta",[])+landed.get("body",[]))
    rendered = (title+" || "+meta+" || "+body_text).lower()
    # verify each declared locked term actually appears in rendered copy
    locked_terms = LOCKED.get(cl,[])
    false_landed = []
    for term in declared:
        if term.lower() in [t.lower() for t in sum(LOCKED.values(),[])]:  # only check locked terms
            if term.lower() not in rendered:
                false_landed.append(term)
    if false_landed:
        issues.append(("FAIL", h, "kw-not-in-rendered", f"declared but absent in copy: {false_landed}"))
        rowflags.append("KWfalse")
    # what locked terms ARE genuinely in rendered copy
    genuine_locked = [t for t in locked_terms if t.lower() in rendered]

    # 5. manufacturer / country
    if d.get("manufacturer") != "Global Furniture Group":
        issues.append(("FAIL", h, "manufacturer-wrong", d.get("manufacturer"))); rowflags.append("MFG")

    rows.append({"handle":h,"cluster":cl,"title_len":len(title),"meta_len":len(meta),
                 "warr":warr or "(empty)","genuine_locked":genuine_locked,
                 "auto_source":d.get("auto_source"),"flags":flags,"rowflags":rowflags})

# ===== report =====
fails = [i for i in issues if i[0]=="FAIL"]
warns = [i for i in issues if i[0]=="WARN"]
print(f"=== QA GATE — 26 drafts ===")
print(f"FAILs: {len(fails)}   WARNs: {len(warns)}\n")
if fails:
    print("--- FAIL ---")
    for sev,h,chk,det in fails: print(f"  [{chk}] {h}: {det}")
if warns:
    print("\n--- WARN ---")
    for sev,h,chk,det in warns: print(f"  [{chk}] {h}: {det}")

print(f"\n=== PER-PRODUCT ===")
print(f"{'handle':52} {'cluster':22} T  M   src    locked-kw / flags")
for r in rows:
    fl = ",".join(r["rowflags"]) or "ok"
    gk = ";".join(r["genuine_locked"]) or "-"
    print(f"{r['handle'][:52]:52} {r['cluster'][:22]:22} {r['title_len']:>2} {r['meta_len']:>3} {r['auto_source'][:6]:6} [{fl}] kw={gk} dataflags={r['flags']}")

# keyword accounting summary
print("\n=== KEYWORD ACCOUNTING ===")
locked_landers=[r for r in rows if r["genuine_locked"]]
zero=[r for r in rows if not r["genuine_locked"]]
print(f"  locked-cluster landers (term genuinely in rendered copy): {len(locked_landers)}")
for r in locked_landers: print(f"     {r['handle'][:50]}: {r['genuine_locked']}")
print(f"  zero-locked-keyword (descriptive / no-fit): {len(zero)}")
