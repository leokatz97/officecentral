#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-3 — Phase 5.3 refresh of the enrichment worksheet.

Updates data/reports/other-collection-products-20260527-093211-with-recs.csv:
  - current_vendor -> corrected manufacturer for every brand-recovered product
  - new column brand_recovered_2026_05_30 = 'Y' for recovered products (else '')

Source of truth = the brand-recovery worksheet rows with decision == APPROVE.
Match key = product_id. Read-only against Shopify; only rewrites the local CSV.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKSHEET = ROOT / 'data' / 'reports' / 'brand-recovery-2026-05-30.csv'
ENRICH = ROOT / 'data' / 'reports' / 'other-collection-products-20260527-093211-with-recs.csv'
NEWCOL = 'brand_recovered_2026_05_30'

# product_id -> corrected vendor, from APPROVE rows
corrected = {r['product_id']: r['recommended_vendor_correction']
             for r in csv.DictReader(WORKSHEET.open()) if r['decision'] == 'APPROVE'}
print(f'{len(corrected)} approved corrections in worksheet')

rows = list(csv.DictReader(ENRICH.open()))
cols = list(rows[0].keys())
if NEWCOL not in cols:
    cols.append(NEWCOL)

updated = 0
for r in rows:
    pid = r.get('product_id')
    if pid in corrected:
        r['current_vendor'] = corrected[pid]
        r[NEWCOL] = 'Y'
        updated += 1
    else:
        r.setdefault(NEWCOL, '')
        if not r.get(NEWCOL):
            r[NEWCOL] = ''

with ENRICH.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
    w.writeheader()
    w.writerows(rows)

print(f'enrichment CSV refreshed: {updated} rows vendor-corrected + flagged (of {len(rows)} total)')
print(f'(corrections not present in this CSV: {len(corrected) - updated} — they live outside /collections/other)')
