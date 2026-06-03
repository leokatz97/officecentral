#!/usr/bin/env python3
"""
Render the prioritized DISCREPANCY REPORT markdown from the aggregated
discrepancy JSON. Hand-written framing + programmatically-built SKU tables
(so SKU references can't drift). Writes to docs/reviews/.
READ-ONLY w.r.t. catalog. No live writes.
"""
import json
from collections import defaultdict

DATE = '2026-06-03'
DISC = f'data/reports/spec-audit-discrepancies-{DATE}.json'
VER = f'data/reports/spec-audit-verified-specs-{DATE}.json'
DATASET = f'data/reports/spec-audit-dataset-{DATE}.json'
OUT = f'docs/reviews/spec-audit-comparison-categories-{DATE}.md'

d = json.load(open(DISC))
disc = d['discrepancies']
no_ds = d['no_datasheet_products']
verified = json.load(open(VER))['skus']
dataset = json.load(open(DATASET))

PURL = 'https://www.brantbusinessinteriors.com/products/'


def row(x, show_claim=True):
    pl = f'`{x["id"]}`'
    title = x['title'].replace('|', '\\|')
    claimed = (x.get('claimed') or '').replace('|', '\\|') or '—'
    actual = (x.get('datasheet_value') or '').replace('|', '\\|') or '—'
    fix = (x.get('recommended_correction') or '').replace('|', '\\|') or '—'
    if show_claim:
        return f'| [{title}]({PURL}{x["handle"]}) | {pl} | {claimed} | {actual} | {fix} |'
    return f'| [{title}]({PURL}{x["handle"]}) | {pl} | {fix} |'


def section(items, header_claim=True):
    out = []
    if header_claim:
        out.append('| Product | ID | Claimed (current) | Datasheet says | Recommended correction |')
        out.append('|---|---|---|---|---|')
    else:
        out.append('| Product | ID | Recommended action |')
        out.append('|---|---|---|')
    for x in items:
        out.append(row(x, header_claim))
    return '\n'.join(out)


# ---- buckets ----
warranty = [x for x in disc if x['spec'] == 'warranty']
origin = [x for x in disc if x['spec'] == 'country_of_manufacture']
certs = [x for x in disc if x['spec'] == 'certifications']
config = [x for x in disc if x['kind'] == 'CONFIG-DIVERGENCE']
legal_other = [x for x in disc if x['legal_sensitive'] and x['spec'] not in
               ('warranty', 'country_of_manufacture', 'certifications')]
factual = [x for x in disc if not x['legal_sensitive'] and x['kind'] == 'MISMATCH']

# category coverage from dataset
cat_counts = defaultdict(lambda: [0, 0])  # name -> [verifiable, total]
for r in dataset:
    for c in r['categories']:
        cat_counts[c][1] += 1
        if r['verifiability'] == 'datasheet-verifiable':
            cat_counts[c][0] += 1

clean = sum(1 for x in disc) and None  # placeholder
n_findings = len(verified)

lines = []
A = lines.append

A(f'# Catalog spec-audit — comparison-target categories ({DATE})')
A('')
A('**Status:** AUDIT ONLY — verified, reported, cached. **No live PDP writes were made.** '
  'Corrections run later in reviewed batches; warranty/origin items are Steve-gated. '
  'This document is the prioritized discrepancy report; the cached verified-spec dataset and '
  'raw per-SKU findings live alongside it (see *Artifacts*).')
A('')
A('## 1. What was audited')
A('')
A('Every **active + published** product in the nine comparison-target categories '
  '(standing/height-adjustable desks, task/ergonomic chairs, executive/guest seating, '
  'big-and-tall + 24-hour seating, conference/boardroom tables, reception, benching/workstations, '
  'acoustic pods, storage/filing). Of **214** products mapped into those categories, **130** carry a '
  'real manufacturer + model code and are therefore *datasheet-verifiable*; the other **84** are '
  'house-brand generics or branded items with no model code and have no manufacturer datasheet to '
  'check against (see §6).')
A('')
A('Each verifiable SKU\'s **claimed** headline specs (the values currently published in `body_html`, '
  'the `specs.*` metafields, and the `global.description_tag`) were cross-checked against the '
  '**manufacturer datasheet** — Global Furniture Group, Offices To Go, Heartwood, and the per-item '
  'brands for the singletons. Each spec was classed **VERIFIED / MISMATCH / UNVERIFIABLE** and, where '
  'wrong, severity-tagged **legal** (warranty, country-of-origin, certification/fire claims) vs '
  '**factual**. The Heartwood Tier discipline applies throughout: where claimed values diverge enough '
  'to imply a *different configuration or model*, the SKU is **flagged, not guessed**.')
A('')
A('## 2. Headline numbers')
A('')
A('| Metric | Count |')
A('|---|---|')
A(f'| Verifiable SKUs audited | **130** |')
A(f'| SKUs fully clean | 35 |')
A(f'| SKUs with ≥1 mismatch | 69 |')
A(f'| SKUs unverifiable overall | 26 |')
A(f'| Spec-level: VERIFIED | 592 |')
A(f'| Spec-level: MISMATCH | 78 |')
A(f'| Spec-level: UNVERIFIABLE | 160 |')
A(f'| **Legally-sensitive items (warranty / origin / certs / fire)** | **{sum(1 for x in disc if x["legal_sensitive"])}** |')
A(f'| — warranty | {len(warranty)} |')
A(f'| — country-of-origin / Made-in-Canada | {len(origin)} |')
A(f'| — certifications / fire rating | {len(certs)+sum(1 for x in disc if x["spec"]=="fire rating")} |')
A(f'| Config / wrong-model divergences (Tier-flagged) | {len(config)} |')
A(f'| Factual mismatches | {len(factual)} |')
A(f'| Verified-spec SKUs cached for comparison content | {n_findings} |')
A('')
A('### The one systemic finding')
A('')
A('The dominant defect is **warranty over-assertion**, and it is systemic, not per-SKU. '
  'AI-drafted copy repeatedly published **"Limited Lifetime"** or a flat **"15-year"** term on '
  'products whose manufacturer grants something narrower:')
A('')
A('- **Global / Basics seating:** the program is named "Limited Lifetime" but **functional parts are '
  'capped** (foam/textile/electrical 5 yr, mechanism 12 yr); copy implying all-component lifetime '
  'overstates it. Several SKUs also invented a **"25-year corporate"** tier that does not exist — and '
  'BBI\'s entire ICP (school boards, hospitals, municipalities) buys as *corporate/institutional* end '
  'users, so this is the wrong tier to advertise.')
A('- **Offices To Go seating:** general seating is "Limited Lifetime" (parts capped 2–5 yr); '
  '**heavy-duty 350 lb seating is a separate 5-YEAR term, not lifetime**; and a recurring **"15-year"** '
  'figure appears on OTG chairs where OTG publishes no such term (it looks imported from the '
  'Newland/ergoCentric warranty).')
A('- **OTG / Newland desking & storage:** the correct term is **15 yr (5 yr on moving/electrical '
  'parts)**, but copy says "Limited Lifetime." Lifetime is supportable **only on the laminate surface**.')
A('')
A('This single pattern accounts for most of the legal-severity flags. It should be fixed as **one '
  'sweeping warranty-language batch keyed to manufacturer + product class**, not SKU-by-SKU. This '
  'matches the standing enrichment-warranty guidance (set warranty from the manufacturer warranty page '
  'per catalog/prefix; sync body copy).')
A('')

A('## 3. CRITICAL — Steve-gated (legal: warranty & country-of-origin)')
A('')
A('> These change a legal claim on the page. **Do not edit live without Steve\'s sign-off.** '
  'Grouped for one batched fix per manufacturer/class.')
A('')
A('### 3a. Warranty (40 items — 27 confirmed wrong, 13 unverifiable-legal)')
A('')
A(section(warranty))
A('')
A('### 3b. Country-of-origin / "Made in Canada" (27 items)')
A('')
A('> Recurring trap: **"Canadian-owned" ≠ "Made in Canada."** Powered desk bases / lift columns are '
  'commonly imported even on Canadian-assembled casegoods. None of these should carry a hard '
  'Made-in-Canada claim until confirmed against the manufacturer per model.')
A('')
A(section(origin))
A('')
if certs or any(x['spec'] == 'fire rating' for x in disc):
    A('### 3c. Certifications & fire rating (compliance claims)')
    A('')
    A('> Over-claimed or unstated certifications are a compliance exposure for institutional tenders. '
      'Only assert a cert the datasheet states verbatim.')
    A('')
    A(section(certs + [x for x in disc if x['spec'] == 'fire rating']))
    A('')

A('## 4. Config / wrong-model divergences (Tier-flagged — resolve before any fix)')
A('')
A('> These are **not** simple value corrections. The claimed specs diverge enough to suggest the page '
  'describes a *different base/model/config* than the model code implies. **Pin the physical product '
  'first; do not guess which side is right.**')
A('')
A('**⚠ Highest priority — the prior Heartwood "fix" looks half-applied to the wrong base.** '
  'The Tier-1 electric sit-to-stand desk (`9687458873657`, model code `CLIE1-INV2442TOP` = **Cleo '
  'CLI-E1**) was rewritten by commit `171aca6` to **Athena (ATH-E1)** values: height 27.5"–45.5", '
  '2-stage, 1"/sec, 2 yr electrical / 5 yr steel. But the two specs left untouched — **<55 dB** and '
  '**265/320 lb capacity** — match *Cleo*, not Athena (<50 dB, 220/330 lb). The block is now '
  'internally inconsistent: half Cleo, half Athena. Either the model code is stale (it is really an '
  'Athena) or the corrections applied the wrong base family. **Resolve against the physical base '
  'before re-publishing.** Same open question on the Tier-2 L-shape set (`HT-ADJ-Layout` is a layout '
  'code, not a fixed base).')
A('')
A(section(config, header_claim=False))
A('')

A('## 5. Factual mismatches (batch-fixable, not legally sensitive)')
A('')
A('> Dimensions, mechanism naming (operator vs synchro vs multi-tilter), material names '
  '(LuxPlus vinyl vs Luxhide bonded leather; felt vs PET), table shape, drawer/shelf config, brand '
  'mis-tags, stale model references in meta tags. Correct in reviewed batches; no Steve gate, but '
  'verify each against the cited datasheet at fix time.')
A('')
A(section(factual))
A('')

A('## 6. Out of verification scope — no manufacturer datasheet (84 products)')
A('')
A('These comparison-category products are **house-brand generics** (`unverifiable-no-datasheet`) or '
  'carry a brand but **no model code** (`brand-known-no-model`). There is no manufacturer datasheet to '
  'verify them against, so any headline spec on them is **self-asserted**. They **cannot safely carry '
  'datasheet-backed comparison specs** — for comparison content, prefer the verified SKUs in §7. '
  'Listed for inventory completeness; full list in the artifact JSON.')
A('')
A('| Verifiability | Count |')
A('|---|---|')
nd = defaultdict(int)
for x in no_ds:
    nd[x['verifiability']] += 1
for k, v in sorted(nd.items()):
    A(f'| {k} | {v} |')
A('')

A('## 7. Cached verified-spec dataset')
A('')
A(f'`data/reports/spec-audit-verified-specs-{DATE}.json` — **{n_findings} SKUs** with their '
  '**datasheet-confirmed** specs only, each carrying its source citation(s). This is the clean pool '
  'product-specific comparisons should pull from: every value in it was confirmed against a real '
  'manufacturer datasheet during this pass. (SKUs with mismatches still appear here for their *clean* '
  'specs; the disputed specs are excluded and listed in §3–5 instead.)')
A('')
A('### Category coverage (verifiable / total mapped)')
A('')
A('| Category | Verifiable | Total mapped |')
A('|---|---|---|')
order = ['standing-desks', 'task-ergonomic-chairs', 'executive-guest-seating',
         'big-tall-24hr-seating', 'conference-boardroom-tables', 'reception',
         'benching-workstations', 'acoustic-pods', 'storage-filing']
for c in order:
    if c in cat_counts:
        A(f'| {c} | {cat_counts[c][0]} | {cat_counts[c][1]} |')
A('')

A('## 8. Method, sources & guardrails')
A('')
A('- **Pull:** `scripts/audit-spec-pull.py` (GraphQL Admin API, read-only) → '
  f'`data/reports/spec-audit-dataset-{DATE}.json`. Categorized by tag + title keyword; verifiability '
  'set by real `specs.manufacturer` + `specs.model_codes`.')
A('- **Batch:** `scripts/audit-spec-batch.py` → per-manufacturer-family research batches.')
A('- **Verify:** 14 parallel research passes, one per batch, each cross-checking claimed specs against '
  'the manufacturer datasheet (globalfurnituregroup.com, officestogo.com, heartwoodmfg.com, and the '
  'per-item brand sites). Real datasheet URLs cited per SKU in the findings JSON; nothing invented — '
  'where a datasheet or value could not be found, the spec is **UNVERIFIABLE**, never guessed.')
A('- **Aggregate:** `scripts/audit-spec-aggregate.py` → verified-spec cache + discrepancy JSON.')
A('- **No live writes.** No `specs.*` metafield, `body_html`, or meta tag was modified. This is DOCS '
  'only, on an audit branch, opened as a PR (not merged).')
A('')
A('## Artifacts')
A('')
A(f'- `data/reports/spec-audit-dataset-{DATE}.json` — full pulled dataset (214 SKUs, claimed specs + categorization).')
A(f'- `data/reports/spec-audit-batches-{DATE}/` — per-batch research inputs.')
A(f'- `data/reports/spec-audit-findings-{DATE}/` — raw per-SKU findings with cited datasheet URLs (14 files, 130 SKUs).')
A(f'- `data/reports/spec-audit-verified-specs-{DATE}.json` — **cached verified-spec dataset** ({n_findings} SKUs).')
A(f'- `data/reports/spec-audit-discrepancies-{DATE}.json` — machine-readable discrepancy list.')
A('')

open(OUT, 'w').write('\n'.join(lines) + '\n')
print(f'Wrote {OUT}  ({len(lines)} lines)')
print(f'warranty={len(warranty)} origin={len(origin)} certs={len(certs)} config={len(config)} factual={len(factual)} legal_other={len(legal_other)}')
