import csv
import sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)

PRODUCTS_CSV = Path('/Users/leokatz/Downloads/products_export_1.csv')

METAFIELD_COLUMNS = {
    'Color': 'Color (product.metafields.shopify.color-pattern)',
    'Material': 'Material (product.metafields.shopify.material)',
    'Style': 'Style (product.metafields.shopify.style)',
    'Suitable location': 'Suitable location (product.metafields.shopify.suitable-location)',
    'Furniture/Fixture material': 'Furniture/Fixture material (product.metafields.shopify.furniture-fixture-material)',
    'Upholstery material': 'Upholstery material (product.metafields.shopify.upholstery-material)',
    'Seat type': 'Seat type (product.metafields.shopify.seat-type)',
    'Back type': 'Back type (product.metafields.shopify.back-type)',
    'Backrest type': 'Backrest type (product.metafields.shopify.backrest-type)',
}


def main():
    values = {label: Counter() for label in METAFIELD_COLUMNS}
    seen_handles = set()
    with PRODUCTS_CSV.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = row.get('Handle', '')
            if not h or h in seen_handles:
                continue
            seen_handles.add(h)
            for label, col in METAFIELD_COLUMNS.items():
                v = (row.get(col) or '').strip()
                if v:
                    for item in v.split(','):
                        item = item.strip()
                        if item:
                            values[label][item] += 1

    for label, counter in values.items():
        print(f'\n=== {label} ({sum(counter.values())} instances across {len(counter)} values) ===')
        for val, cnt in counter.most_common(30):
            print(f'  {cnt:>4}  {val}')


if __name__ == '__main__':
    main()
