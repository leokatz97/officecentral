#!/usr/bin/env python3
"""
Build compact per-SKU verification records from the audit dataset and group them
into manufacturer-family research batches. READ-ONLY (reads the dataset JSON,
writes batch JSON for the research agents). No Shopify calls.

Output: data/reports/spec-audit-batches-2026-06-03.json
"""
import json, re
from collections import defaultdict

DATE = '2026-06-03'
SRC = f'data/reports/spec-audit-dataset-{DATE}.json'
OUT = f'data/reports/spec-audit-batches-{DATE}.json'

HEADLINE = ['dimensions', 'weight_capacity', 'materials', 'key_features',
            'certifications', 'warranty', 'country_of_manufacture', 'product_line']


def brand_family(brand):
    b = brand.lower()
    if 'heartwood' in b:
        return 'Heartwood'
    if 'otg' in b or 'offices to go' in b:
        return 'OTG'
    if 'global' in b or 'basics' in b or 'canadian workplace' in b or 'obusforme' in b:
        return 'Global-family'
    return 'Other'


def body_numeric_claims(html):
    """Pull sentences from body_html that carry verifiable numeric/spec claims,
    so the agent can flag overstatements in copy (the Heartwood failure mode)."""
    text = re.sub(r'<[^>]+>', ' ', html or '')
    text = re.sub(r'\s+', ' ', text).strip()
    sents = re.split(r'(?<=[.!?])\s+', text)
    pat = re.compile(r'\b(\d|stage|warranty|lifetime|year|lb|kg|inch|"|cm|certif|csa|ul |greenguard|bifma|canada|canadian|made in|speed|/sec|capacity|weight)\b', re.I)
    keep = [s for s in sents if pat.search(s)]
    return keep[:14]


def main():
    data = json.load(open(SRC))
    ver = [r for r in data if r['verifiability'] == 'datasheet-verifiable']

    records = []
    for r in ver:
        records.append({
            'id': r['id'],
            'handle': r['handle'],
            'title': r['title'],
            'brand': r['brand'],
            'models': r['models'],
            'categories': r['categories'],
            'claimed_specs': {k: r['specs'].get(k) for k in HEADLINE if r['specs'].get(k)},
            'global_description_tag': r.get('global_description_tag'),
            'body_numeric_claims': body_numeric_claims(r.get('body_html')),
        })

    fam = defaultdict(list)
    for rec in records:
        fam[brand_family(rec['brand'])].append(rec)

    # split large families into category-coherent batches of <= 11
    batches = []

    def add_batches(label, recs, size=11):
        for i in range(0, len(recs), size):
            chunk = recs[i:i + size]
            batches.append({'batch': f'{label}-{i//size + 1}', 'count': len(chunk), 'skus': chunk})

    # Global family: split by category bucket for coherent datasheet lookups
    gfam = fam['Global-family']
    seating = [r for r in gfam if any(c in ('task-ergonomic-chairs', 'executive-guest-seating', 'big-tall-24hr-seating') for c in r['categories'])]
    desks = [r for r in gfam if any(c in ('standing-desks', 'benching-workstations', 'conference-boardroom-tables') for c in r['categories']) and r not in seating]
    storage = [r for r in gfam if r not in seating and r not in desks and 'storage-filing' in r['categories']]
    reception = [r for r in gfam if r not in seating and r not in desks and r not in storage]
    add_batches('global-seating', seating)
    add_batches('global-desks-tables', desks)
    add_batches('global-storage', storage)
    add_batches('global-reception-other', reception)

    otg = fam['OTG']
    otg_seat = [r for r in otg if any(c in ('task-ergonomic-chairs', 'executive-guest-seating', 'big-tall-24hr-seating') for c in r['categories'])]
    otg_other = [r for r in otg if r not in otg_seat]
    add_batches('otg-seating', otg_seat)
    add_batches('otg-other', otg_other)

    add_batches('heartwood', fam['Heartwood'])
    add_batches('other-singletons', fam['Other'], size=14)

    json.dump({'date': DATE, 'total_verifiable': len(records), 'batches': batches},
              open(OUT, 'w'), indent=2, ensure_ascii=False)

    print(f'{len(records)} verifiable SKUs in {len(batches)} batches:')
    for b in batches:
        cats = defaultdict(int)
        for s in b['skus']:
            for c in s['categories']:
                cats[c] += 1
        print(f"  {b['batch']:26} {b['count']:3}  {dict(cats)}")
    print(f'\nWrote {OUT}')


if __name__ == '__main__':
    main()
