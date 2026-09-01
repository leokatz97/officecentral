import csv
import sys
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

PRODUCTS_CSV = Path('/Users/leokatz/Downloads/products_export_1.csv')
PRIORITIES_CSV = Path(__file__).resolve().parent.parent / 'data' / 'enrichment-priorities.csv'

TIER_A_HANDLES = set()
with PRIORITIES_CSV.open(newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['Tier'] == 'A':
            TIER_A_HANDLES.add(r['Handle'])


def main():
    variants_by_handle = defaultdict(list)
    titles = {}
    options_by_handle = defaultdict(lambda: ['', '', ''])
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
            if sku or opt1 or opt2 or opt3:
                variants_by_handle[h].append({
                    'sku': sku,
                    'opt1': opt1,
                    'opt2': opt2,
                    'opt3': opt3,
                })

    print(f'Total handles with variants: {len(variants_by_handle)}\n')

    no_sku = [h for h, vs in variants_by_handle.items() if not any(v['sku'] for v in vs)]
    print(f'Handles with ZERO variant SKUs: {len(no_sku)}')
    print(f'Handles with at least one SKU: {len(variants_by_handle) - len(no_sku)}\n')

    print('=== TIER A VARIANT SAMPLE ===\n')
    for h in list(TIER_A_HANDLES)[:8]:
        vs = variants_by_handle.get(h, [])
        opts = options_by_handle[h]
        opt_names = [o for o in opts if o]
        print(f'-- {titles.get(h, h)} ({h})')
        print(f'   Option names: {opt_names}')
        print(f'   Variant count: {len(vs)}')
        skus = [v["sku"] for v in vs if v["sku"]]
        unique_skus = list(dict.fromkeys(skus))
        print(f'   Unique SKUs ({len(unique_skus)}): {unique_skus[:6]}{" ..." if len(unique_skus) > 6 else ""}')
        for v in vs[:4]:
            print(f'     sku="{v["sku"]}" | {v["opt1"]} | {v["opt2"]} | {v["opt3"]}')
        if len(vs) > 4:
            print(f'     ... ({len(vs) - 4} more)')
        print()


if __name__ == '__main__':
    main()
