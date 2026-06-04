#!/usr/bin/env python3
"""
Aggregate the per-batch spec-audit findings into the two AUDIT deliverables:

 1) Cached VERIFIED-SPEC dataset (data/reports/spec-audit-verified-specs-<date>.json)
    — per SKU, the datasheet-CONFIRMED specs only, each with its source citation.
 2) Prioritized DISCREPANCY REPORT data (data/reports/spec-audit-discrepancies-<date>.json)
    — every MISMATCH + flagged UNVERIFIABLE-legal + config_divergence, with severity,
      legal-sensitivity, recommended correction, grouped for batched fixing.

Also folds in the dataset's UNVERIFIABLE-no-datasheet / brand-known-no-model
products (the SKUs with no manufacturer datasheet to verify against).

READ-ONLY aggregation. No Shopify calls, no live writes. The human-facing
markdown report is written separately to docs/reviews/.
"""
import json, glob, os
from collections import Counter, defaultdict

DATE = '2026-06-03'
FINDINGS_DIR = f'data/reports/spec-audit-findings-{DATE}'
DATASET = f'data/reports/spec-audit-dataset-{DATE}.json'
VERIFIED_OUT = f'data/reports/spec-audit-verified-specs-{DATE}.json'
DISCREP_OUT = f'data/reports/spec-audit-discrepancies-{DATE}.json'

LEGAL_SPECS = {'warranty', 'country_of_manufacture', 'origin', 'fire_rating',
               'certifications'}  # certifications only when it's a compliance/legal claim


def load_findings():
    recs = []
    for f in sorted(glob.glob(f'{FINDINGS_DIR}/*.json')):
        batch = os.path.basename(f)[:-5]
        for r in json.load(open(f)):
            r['_batch'] = batch
            recs.append(r)
    return recs


def main():
    findings = load_findings()
    dataset = {r['id']: r for r in json.load(open(DATASET))}

    verified = []      # cached verified-spec dataset
    discrepancies = [] # mismatches + legal-unverifiable + config divergences

    counts = Counter()
    for r in findings:
        sid = r['id']
        ds = dataset.get(sid, {})
        confirmed = []
        for sf in r.get('spec_findings', []):
            cls = (sf.get('classification') or '').upper()
            counts[cls] += 1
            if cls == 'VERIFIED':
                confirmed.append({
                    'spec': sf['spec'],
                    'value': sf.get('datasheet_value') or sf.get('claimed'),
                    'source': r.get('datasheet_sources', []),
                })
            elif cls == 'MISMATCH':
                discrepancies.append({
                    'id': sid, 'handle': r['handle'], 'title': r['title'],
                    'brand': r['brand'], 'models': r['models'],
                    'categories': ds.get('categories', []),
                    'spec': sf['spec'], 'claimed': sf.get('claimed'),
                    'datasheet_value': sf.get('datasheet_value'),
                    'severity': sf.get('severity', 'factual'),
                    'legal_sensitive': (sf.get('severity') == 'legal') or (sf['spec'] in LEGAL_SPECS),
                    'recommended_correction': sf.get('recommended_correction'),
                    'notes': sf.get('notes'),
                    'kind': 'MISMATCH',
                    'sources': r.get('datasheet_sources', []),
                    'batch': r['_batch'],
                })
            elif cls == 'UNVERIFIABLE' and sf.get('severity') == 'legal':
                discrepancies.append({
                    'id': sid, 'handle': r['handle'], 'title': r['title'],
                    'brand': r['brand'], 'models': r['models'],
                    'categories': ds.get('categories', []),
                    'spec': sf['spec'], 'claimed': sf.get('claimed'),
                    'datasheet_value': sf.get('datasheet_value'),
                    'severity': 'legal',
                    'legal_sensitive': True,
                    'recommended_correction': sf.get('recommended_correction'),
                    'notes': sf.get('notes'),
                    'kind': 'UNVERIFIABLE-LEGAL',
                    'sources': r.get('datasheet_sources', []),
                    'batch': r['_batch'],
                })
        if confirmed:
            verified.append({
                'id': sid, 'handle': r['handle'], 'title': r['title'],
                'brand': r['brand'], 'models': r['models'],
                'categories': ds.get('categories', []),
                'datasheet_sources': r.get('datasheet_sources', []),
                'verified_specs': confirmed,
            })
        if r.get('config_divergence'):
            discrepancies.append({
                'id': sid, 'handle': r['handle'], 'title': r['title'],
                'brand': r['brand'], 'models': r['models'],
                'categories': ds.get('categories', []),
                'spec': 'CONFIG / MODEL', 'claimed': None, 'datasheet_value': None,
                'severity': 'config', 'legal_sensitive': False,
                'recommended_correction': 'Pin the exact base/model/config against the physical product before re-publishing; do not guess.',
                'notes': r.get('config_divergence_note'),
                'kind': 'CONFIG-DIVERGENCE',
                'sources': r.get('datasheet_sources', []),
                'batch': r['_batch'],
            })

    # products with no datasheet to verify against (not in the verifiable set)
    no_datasheet = [
        {'id': r['id'], 'handle': r['handle'], 'title': r['title'],
         'brand': r['brand'], 'categories': r['categories'],
         'verifiability': r['verifiability']}
        for r in json.load(open(DATASET))
        if r['verifiability'] in ('unverifiable-no-datasheet', 'brand-known-no-model')
    ]

    json.dump({'date': DATE, 'count': len(verified), 'skus': verified},
              open(VERIFIED_OUT, 'w'), indent=2, ensure_ascii=False)
    json.dump({'date': DATE, 'discrepancies': discrepancies,
               'no_datasheet_products': no_datasheet},
              open(DISCREP_OUT, 'w'), indent=2, ensure_ascii=False)

    # console summary
    sku_overall = Counter(r.get('overall', '?') for r in findings)
    legal = [d for d in discrepancies if d['legal_sensitive']]
    config = [d for d in discrepancies if d['kind'] == 'CONFIG-DIVERGENCE']
    print(f'SKUs verified (findings): {len(findings)}')
    print(f'  overall: {dict(sku_overall)}')
    print(f'spec-level classifications: {dict(counts)}')
    print(f'verified-spec SKUs cached: {len(verified)}')
    print(f'discrepancies total: {len(discrepancies)}  (legal-sensitive {len(legal)}, config-divergence {len(config)})')
    print(f'no-datasheet products (out of verifiable scope): {len(no_datasheet)}')
    print(f'\nWrote {VERIFIED_OUT}\nWrote {DISCREP_OUT}')


if __name__ == '__main__':
    main()
