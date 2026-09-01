import csv
import re
import sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)

PRODUCTS_CSV = Path('/Users/leokatz/Downloads/products_export_1.csv')


def extract_prefix(sku):
    """Pull the alphabetic prefix from a SKU (handles GLB, HDL, MVL, OTG, etc.)."""
    if not sku:
        return ''
    m = re.match(r'^([A-Z]+)', sku.strip().upper())
    return m.group(1) if m else ''


def main():
    prefix_counts = Counter()
    prefix_examples = {}
    seen = set()
    with PRODUCTS_CSV.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sku = (row.get('Variant SKU') or '').strip()
            if not sku or sku in seen:
                continue
            seen.add(sku)
            p = extract_prefix(sku)
            if p:
                prefix_counts[p] += 1
                if p not in prefix_examples:
                    prefix_examples[p] = []
                if len(prefix_examples[p]) < 3:
                    prefix_examples[p].append(sku)

    print(f'{"Prefix":10} {"Count":>6}  Examples')
    print('-' * 80)
    for p, cnt in prefix_counts.most_common():
        ex = ', '.join(prefix_examples[p])
        print(f'{p:10} {cnt:>6}  {ex}')


if __name__ == '__main__':
    main()
