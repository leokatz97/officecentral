#!/usr/bin/env python3
"""Generate the BBI re-sourcing provenance report (markdown) from the worksheet.
READ-ONLY: reads data/reports/bbi-resourcing-2026-06-02.csv, writes the .md.
"""
import csv
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / 'data' / 'reports' / 'bbi-resourcing-2026-06-02.csv'
OUT = ROOT / 'data' / 'reports' / 'bbi-resourcing-provenance-2026-06-02.md'
rows = list(csv.DictReader(CSV.open()))


def slug(s):
    import re
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


confident = [r for r in rows if r['classification'] == 'CONFIDENT']
t1 = [r for r in confident if r['confidence_tier'] == 'tier1']
t2 = [r for r in confident if r['confidence_tier'] == 'tier2']
ambiguous = [r for r in rows if r['classification'] == 'AMBIGUOUS']
skip = [r for r in rows if r['classification'] == 'SKIP']

L = []
w = L.append
w('# BBI Re-sourcing — Provenance Report (2026-06-02)')
w('')
w('**Task:** correct `vendor="Brant Business Interiors"` data-errors to real manufacturers '
  '(BBI is a dealer, not a manufacturer) — the hard prerequisite for the Brand filter.')
w('**Carry-forward** from the 2026-05-30 brand-recovery audit (PR #62: 183 corrected, 204 left UNKNOWN). '
  'Since then `sku-prefix-lookup.yaml` gained deterministic decodes for HDL/IOF/RIC/HZN/MTY, '
  'unblocking most of the residual tail.')
w('')
w('**Method:** Admin-API GraphQL read of all live `vendor:BBI` products → signal-based sourcing '
  '(SKU-prefix primary, per SKU-PREFIX-PATTERNS-ARE-DETERMINISTIC) → CONFIDENT/AMBIGUOUS classification. '
  'No Shopify writes, no theme files touched.')
w('')
w('## Decisions locked (Leo, 2026-06-02)')
w('- **HDL folded into `Heartwood`** (single clean `brand:heartwood` chip; same brand family as HTW).')
w('- **Scope = tier-1 only (97).** The 18 tier-2 sub-code/line/title promotions defer to the Steve/manual pile.')
w('- **HOLD — report only.** Zero Shopify writes this session; the apply script is staged for a future `--live` go.')
w('')
w('## Summary')
w('')
w('| Class | N | Action |')
w('|---|---:|---|')
w(f'| **CONFIDENT — tier 1** (write-ready) | **{len(t1)}** | correct vendor + add `brand:*` (STAGED, held) |')
w(f'| CONFIDENT — tier 2 (deferred to Steve) | {len(t2)} | locked sub-code/line/title; confirm then write |')
w(f'| AMBIGUOUS | {len(ambiguous)} | leave untouched → Steve/manual |')
w(f'| SKIP (services) | {len(skip)} | leave untouched (BBI-as-vendor acceptable) |')
w(f'| **Total scanned** | **{len(rows)}** | |')
w('')
w(f'**N corrected (planned, held): {len(t1)}**  ·  **M deferred-to-Steve: {len(t2)+len(ambiguous)}** '
  f'({len(t2)} tier-2 + {len(ambiguous)} ambiguous)  ·  **{len(skip)} services skipped.**')
w('')

# tier1 distribution
w('## Tier-1 confident — manufacturer distribution (the 97)')
w('')
w('| Manufacturer | N | brand tag |')
w('|---|---:|---|')
for m, n in Counter(r['detected_manufacturer'] for r in t1).most_common():
    w(f'| {m} | {n} | `brand:{slug(m)}` |')
w('')

# full tier1 sourcing map
w('## Tier-1 sourcing map (product → manufacturer + signal)')
w('')
w('| Handle | SKU sample | → Manufacturer | Signal |')
w('|---|---|---|---|')
for r in sorted(t1, key=lambda r: (r['detected_manufacturer'], r['product_handle'])):
    sig = r['primary_signal'].replace('|', '/')[:60]
    w(f"| {r['product_handle'][:44]} | `{r['sku_sample'][:24]}` | {r['detected_manufacturer']} | {sig} |")
w('')

# tier2 deferred
w('## Tier-2 deferred (18) — locked sub-code / line / title, confirm before writing')
w('')
w('| Handle | SKU sample | → Manufacturer | Signal |')
w('|---|---|---|---|')
for r in sorted(t2, key=lambda r: (r['detected_manufacturer'], r['product_handle'])):
    sig = r['primary_signal'].replace('|', '/')[:60]
    w(f"| {r['product_handle'][:44]} | `{r['sku_sample'][:24]}` | {r['detected_manufacturer']} | {sig} |")
w('')

# ambiguous
w('## Ambiguous (87) — untouched, → Steve/manual')
w('')
amb_by = defaultdict(list)
for r in ambiguous:
    amb_by[r['ambiguous_prefix']].append(r)
w('| SKU prefix / reason | N | Example | Sample title |')
w('|---|---:|---|---|')
for pfx, rs in sorted(amb_by.items(), key=lambda x: -len(x[1])):
    ex = next((r['sku_sample'] for r in rs if r['sku_sample']), '')
    title = rs[0]['current_title'][:46]
    note = ''
    if pfx == 'SCN':
        note = ' *(locked-undecoded: lockers/site-furnishings, supplier invoice)*'
    w(f"| `{pfx}` | {len(rs)} | `{ex[:22]}` | {title}{note} |")
w('')
w('*Candidate hints (NOT auto-applied — flagged for Steve):* `MYB`→MityBilt (sibling has the '
  '`specs.manufacturer` metafield); `TEK`→possibly Teknion; `JNT`→possibly Jonti-Craft; '
  '`SYNN`→possibly AndaSeat (gaming); `DIVERSIFIEDAFT`→possibly Diversified. None are in the '
  '19-brand dictionary, so they stay ambiguous.')
w('')

# skip
w('## Skipped (19) — service / non-product line items')
w('')
w('Delivery / installation / freight / disposal / dismantle / additional-service rows. '
  '`vendor=BBI` is acceptable here (BBI provides the service). Left untouched.')
w('')

# readiness
w('## Brand-filter readiness')
w('')
w('The filter reads card `data-vendor`, so any product left at `vendor=BBI` still renders a '
  '**"Brant Business Interiors" brand chip**. Residual characterization (106 untouched = 87 ambiguous + 19 skip):')
w('')
w('| Residual bucket | N |')
w('|---|---:|')
w('| Published & real product | 52 |')
w('| Published $0 (quote-only) | 7 |')
w('| Unpublished (not on storefront) | 18 |')
w('| Phantom/option rows | 10 |')
w('| Services (SKIP) | 19 |')
w('')
w('**Verdict:** writing the 97 tier-1 corrections **unblocks the Brand filter for those products**, but '
  '**~59 published-real products would still surface a "Brant Business Interiors" chip** — too large to '
  'ship the filter cleanly alongside. Recommend either (a) suppress the BBI chip in the filter UI until the '
  'Steve pass resolves the ~59, or (b) run the Steve pass on the tier-2 (18) + ambiguous (87) first. '
  'The tier-2 18 are the cheapest wins (already sourced, just need a confirm).')
w('')
w('## Artifacts')
w('- Worksheet: `data/reports/bbi-resourcing-2026-06-02.csv` (+ `-evidence.json`)')
w('- Scan (read-only): `scripts/scan-bbi-resourcing-2026-06-02.py`')
w('- Apply (staged, dry-run default): `scripts/apply-bbi-resourcing-2026-06-02.py` — '
  '`--tier1 --live` writes the 97.')
w('')

OUT.write_text('\n'.join(L))
print(f'Wrote {OUT.relative_to(ROOT)} ({len(L)} lines)')
