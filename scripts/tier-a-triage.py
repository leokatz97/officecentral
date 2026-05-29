#!/usr/bin/env python3
"""
Tier A Interactive Enrichment — Phase 1 triage.

Reads the latest other-collection routing CSV, scores every product by
ENRICHMENT_ROI (per the Tier-A prompt spec), buckets into A/B/C/D, writes
data/reports/tier-a-triage-{ts}.csv, and prints a session summary.

Read-only against Shopify. Pure local file work.
"""
import csv
import datetime as dt
import glob
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "data" / "reports"

PREMIUM_BRANDS = {
    "global furniture group",
    "teknion",
    "humanscale",
    "keilhauer",
    "ergocentric",
    "haworth",
    "steelcase",
    "otg / offices to go",
    "offices to go",
    "otg",
    "heartwood manufacturing ltd.",
    "heartwood manufacturing",
    "heartwood",
}
HOUSE_VENDOR = "brant business interiors"

MODEL_PATTERNS = [
    re.compile(r"\b\d{3,5}-?[a-z0-9]{0,3}\b", re.I),   # 2661, 2661-0
    re.compile(r"\b[A-Z]{1,4}\d{1,5}[A-Z0-9-]*\b"),     # ML48, VU26, S128
    re.compile(r"\bINV-[A-Z0-9-]+\b", re.I),
]

LINES = [
    "loover", "wave", "concorde", "altona", "heritage", "vion",
    "ibex", "spritz", "noble", "ergo cocoon", "elora", "atlas",
    "vesta", "synapse", "newland", "obus",
]

PARTS_PATTERN = re.compile(
    r"\b(arm caps?|caster wheels?|casters?|glides?|replacement|"
    r"for [a-z0-9- ]+ chair|cushion only|seat only|kit$|"
    r"foot ?rest pad|repair)\b",
    re.I,
)


def find_latest(glob_pattern):
    matches = sorted(glob.glob(str(REPORTS / glob_pattern)))
    if not matches:
        sys.exit(f"FAIL: no file matches {glob_pattern}")
    return matches[-1]


def detect_brand_line(title):
    title_l = title.lower()
    hits = [line for line in LINES if re.search(rf"\b{re.escape(line)}\b", title_l)]
    return hits[0] if hits else ""


def detect_model(title):
    for pat in MODEL_PATTERNS:
        m = pat.search(title)
        if m:
            return m.group(0)
    return ""


def to_float(s, default=0.0):
    try:
        return float(s) if s not in (None, "") else default
    except ValueError:
        return default


def score_row(row, brand_picklist):
    vendor = (row.get("current_vendor") or "").strip()
    vendor_l = vendor.lower()
    title = row.get("title") or ""
    title_l = title.lower()
    price_max = to_float(row.get("price_max"))
    body = row.get("body_excerpt") or ""
    conf = (row.get("claude_confidence") or "").lower()

    score = 0
    reasons = []

    if vendor_l in PREMIUM_BRANDS:
        score += 5
        reasons.append("+5 premium-brand vendor")
    elif vendor_l and vendor_l != HOUSE_VENDOR and vendor in brand_picklist:
        score += 3
        reasons.append("+3 named vendor")

    if price_max >= 500:
        score += 5
        reasons.append("+5 price>=500")
    elif price_max >= 200:
        score += 3
        reasons.append("+3 price>=200")

    model = detect_model(title)
    if model:
        score += 2
        reasons.append(f"+2 model:{model}")

    line = detect_brand_line(title)
    if line:
        score += 2
        reasons.append(f"+2 line:{line}")

    if len(body) < 100 and len(title) < 25 and " " in title:
        # short body + short generic-ish title
        score -= 3
        reasons.append("-3 thin context")

    if PARTS_PATTERN.search(title) or PARTS_PATTERN.search(body[:200]):
        score -= 5
        reasons.append("-5 parts/accessory")

    if conf in ("none", ""):
        score += 1
        reasons.append("+1 routing unknown")

    return score, line, model, "; ".join(reasons)


def tier_for(score):
    if score >= 10:
        return "A-PRIORITY"
    if score >= 5:
        return "B-WORTH-IT"
    if score >= 1:
        return "C-MAYBE"
    return "D-SKIP"


def main():
    products_csv = find_latest("other-collection-products-*-with-recs.csv")
    picklists_csv = find_latest("other-collection-picklists-*.csv")
    print(f"Products CSV:  {products_csv}")
    print(f"Picklists CSV: {picklists_csv}")

    # Load brand picklist
    brand_picklist = set()
    sub_picklist = set()
    with open(picklists_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["SECTION"] == "BRANDS":
                brand_picklist.add(r["value"])
            elif r["SECTION"] == "SUB_COLLECTIONS":
                sub_picklist.add(r["handle_or_count"])
    print(f"Brand picklist:        {len(brand_picklist)}")
    print(f"Sub-collection picklist: {len(sub_picklist)}")

    rows = []
    with open(products_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            score, line, model, why = score_row(r, brand_picklist)
            rows.append({**r, "_score": score, "_line": line, "_model": model, "_why": why})

    rows.sort(key=lambda r: r["_score"], reverse=True)

    # Bucket counts
    buckets = {"A-PRIORITY": 0, "B-WORTH-IT": 0, "C-MAYBE": 0, "D-SKIP": 0}
    for r in rows:
        buckets[tier_for(r["_score"])] += 1

    # Premium-brand counts
    premium_counts = {}
    for r in rows:
        v = (r.get("current_vendor") or "").strip()
        if v.lower() in PREMIUM_BRANDS:
            premium_counts[v] = premium_counts.get(v, 0) + 1

    # Line counts
    line_counts = {}
    for r in rows:
        if r["_line"]:
            line_counts[r["_line"]] = line_counts.get(r["_line"], 0) + 1

    # Write triage CSV
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = REPORTS / f"tier-a-triage-{ts}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "rank", "product_id", "handle", "title", "vendor",
            "price_max", "confidence", "score", "tier",
            "recommended_subs", "detected_line", "detected_model", "reason"
        ])
        for i, r in enumerate(rows, 1):
            subs = " | ".join(
                x for x in [
                    r.get("recommended_sub_collection_1"),
                    r.get("recommended_sub_collection_2"),
                    r.get("recommended_sub_collection_3"),
                ] if x
            )
            w.writerow([
                i, r.get("product_id"), r.get("handle"), r.get("title"),
                r.get("current_vendor"), r.get("price_max"),
                r.get("claude_confidence"), r["_score"], tier_for(r["_score"]),
                subs, r["_line"], r["_model"], r["_why"],
            ])

    # Surface
    print()
    print("=" * 64)
    print("TIER A TRIAGE COMPLETE")
    print("=" * 64)
    for t in ["A-PRIORITY", "B-WORTH-IT", "C-MAYBE", "D-SKIP"]:
        print(f"  {t}: {buckets[t]}")

    print()
    print("Premium-brand vendor counts:")
    if premium_counts:
        for v, n in sorted(premium_counts.items(), key=lambda kv: -kv[1]):
            print(f"  {v}: {n}")
    else:
        print("  (none — all 'Other' products are vendor=Brant Business Interiors)")

    print()
    print("Detected brand-line names in titles (top 10):")
    for line, n in sorted(line_counts.items(), key=lambda kv: -kv[1])[:10]:
        print(f"  {line}: {n}")

    print()
    print(f"Top 10 by score (A-PRIORITY preview):")
    for r in rows[:10]:
        print(f"  {r['_score']:>3}  {r.get('handle')[:50]:<50}  {r.get('current_vendor')[:25]:<25}  ${r.get('price_max')}")

    print()
    print(f"Report written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
