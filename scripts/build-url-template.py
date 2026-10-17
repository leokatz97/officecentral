import csv
import sys
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

PRODUCTS_CSV = Path('/Users/leokatz/Downloads/products_export_1.csv')
PRIORITIES_CSV = Path(__file__).resolve().parent.parent / 'data' / 'enrichment-priorities.csv'
OUT_TEMPLATE = Path(__file__).resolve().parent.parent / 'data' / 'url-enrichment-template.csv'
OUT_VARIANTS = Path(__file__).resolve().parent.parent / 'data' / 'product-variants-reference.csv'

TEMPLATE_COLUMNS = [
    'Tier', 'Revenue', 'Status', 'Handle', 'Title',
    'VariantCount', 'OptionNames', 'RepSKU', 'AllSKUs',
    'ProbableManufacturer', 'ManufacturerWebsite',
    'URL1', 'URL2', 'RawPaste', 'Notes',
]

MANUFACTURER_LOOKUP_CSV = Path(__file__).resolve().parent.parent / 'data' / 'sku-prefix-manufacturers.csv'


def load_manufacturer_lookup():
    import re
    lookup = []
    if not MANUFACTURER_LOOKUP_CSV.exists():
        return lookup
    with MANUFACTURER_LOOKUP_CSV.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            prefix = row.get('Prefix', '').strip()
            mfr = row.get('Manufacturer', '').strip()
            web = row.get('Website', '').strip()
            if prefix and mfr:
                lookup.append((prefix, mfr, web))
    lookup.sort(key=lambda x: -len(x[0]))
    return lookup


def sku_to_manufacturer(sku, lookup):
    import re
    if not sku:
        return '', ''
    up = sku.strip().upper()
    for prefix, mfr, web in lookup:
        if up.startswith(prefix):
            return mfr, web
    return '', ''
VARIANT_COLUMNS = ['Handle', 'Title', 'Tier', 'VariantSKU', 'Option1', 'Option2', 'Option3', 'Price']


def main():
    variants_by_handle = defaultdict(list)
    options_by_handle = defaultdict(lambda: ['', '', ''])
    titles = {}
    with PRODUCTS_CSV.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = row.get('Handle', '').strip()
            if not h:
                continue
            if row.get('Title', '').strip():
                titles[h] = row['Title'].strip()
            for i, key in enumerate(['Option1 Name', 'Option2 Name', 'Option3 Name']):
                v = (row.get(key) or '').strip()
                if v and not options_by_handle[h][i]:
                    options_by_handle[h][i] = v
            sku = (row.get('Variant SKU') or '').strip()
            opt1 = (row.get('Option1 Value') or '').strip()
            opt2 = (row.get('Option2 Value') or '').strip()
            opt3 = (row.get('Option3 Value') or '').strip()
            price = (row.get('Variant Price') or '').strip()
            if sku or opt1 or opt2 or opt3:
                variants_by_handle[h].append({
                    'sku': sku, 'opt1': opt1, 'opt2': opt2, 'opt3': opt3, 'price': price,
                })

    # Load tier info
    tier_by_handle = {}
    rev_by_handle = {}
    with PRIORITIES_CSV.open(newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            tier_by_handle[r['Handle']] = r['Tier']
            rev_by_handle[r['Handle']] = r['Revenue']

    # Build priorities rows for active products
    with PRIORITIES_CSV.open(newline='', encoding='utf-8') as f:
        priority_rows = [r for r in csv.DictReader(f) if r['Status'] == 'active']

    tier_order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    priority_rows.sort(key=lambda r: (tier_order.get(r['Tier'], 9), -float(r['Revenue'] or 0)))

    mfr_lookup = load_manufacturer_lookup()

    # Write URL template with variant info
    template_rows = []
    for r in priority_rows:
        h = r['Handle']
        variants = variants_by_handle.get(h, [])
        opts = options_by_handle[h]
        opt_names = '; '.join(o for o in opts if o and o != 'Title')
        skus = [v['sku'] for v in variants if v['sku']]
        unique_skus = list(dict.fromkeys(skus))
        rep_sku = unique_skus[0] if unique_skus else ''
        if len(unique_skus) <= 10:
            all_skus = '; '.join(unique_skus)
        else:
            all_skus = '; '.join(unique_skus[:10]) + f'; ...+{len(unique_skus) - 10} more'
        mfr, web = sku_to_manufacturer(rep_sku, mfr_lookup)
        template_rows.append({
            'Tier': r['Tier'],
            'Revenue': r['Revenue'],
            'Status': r['Status'],
            'Handle': h,
            'Title': r['Title'],
            'VariantCount': len(variants) if len(variants) > 1 or (variants and variants[0]['opt1'] not in ('', 'Default Title')) else 1,
            'OptionNames': opt_names,
            'RepSKU': rep_sku,
            'AllSKUs': all_skus,
            'ProbableManufacturer': mfr,
            'ManufacturerWebsite': web,
            'URL1': '',
            'URL2': '',
            'RawPaste': '',
            'Notes': '',
        })

    with OUT_TEMPLATE.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
        w.writeheader()
        w.writerows(template_rows)
    print(f'Wrote {len(template_rows)} active products to {OUT_TEMPLATE}')

    # Write per-variant reference file (all active products, one row per variant)
    active_handles = {r['Handle'] for r in priority_rows}
    variant_rows = []
    for h, variants in variants_by_handle.items():
        if h not in active_handles:
            continue
        for v in variants:
            variant_rows.append({
                'Handle': h,
                'Title': titles.get(h, ''),
                'Tier': tier_by_handle.get(h, ''),
                'VariantSKU': v['sku'],
                'Option1': v['opt1'],
                'Option2': v['opt2'],
                'Option3': v['opt3'],
                'Price': v['price'],
            })
    variant_rows.sort(key=lambda r: (tier_order.get(r['Tier'], 9), r['Handle'], r['Option1']))
    with OUT_VARIANTS.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=VARIANT_COLUMNS)
        w.writeheader()
        w.writerows(variant_rows)
    print(f'Wrote {len(variant_rows)} variant rows to {OUT_VARIANTS}')

    # Flag products with no SKU
    no_sku = [r for r in template_rows if not r['RepSKU']]
    print(f'\n{len(no_sku)} active products have ZERO variant SKUs — flagged for manual review:')
    for r in no_sku[:10]:
        print(f'  [{r["Tier"]}] ${r["Revenue"]:>10}  {r["Handle"]}  "{r["Title"]}"')
    if len(no_sku) > 10:
        print(f'  ... ({len(no_sku) - 10} more)')


if __name__ == '__main__':
    main()
