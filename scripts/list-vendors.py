import csv
import sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)

PRODUCTS_CSV = Path('/Users/leokatz/Downloads/products_export_1.csv')


def main():
    vendor_counts = Counter()
    seen = set()
    with PRODUCTS_CSV.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            h = row.get('Handle', '').strip()
            if not h or h in seen:
                continue
            seen.add(h)
            v = (row.get('Vendor') or '').strip()
            status = (row.get('Status') or '').strip()
            vendor_counts[(v, status)] += 1

    # Collapse by vendor
    by_vendor = Counter()
    by_vendor_active = Counter()
    for (v, status), cnt in vendor_counts.items():
        by_vendor[v] += cnt
        if status == 'active':
            by_vendor_active[v] += cnt

    print(f'Distinct vendors: {len(by_vendor)}\n')
    print(f'{"Vendor":60} {"Active":>8} {"Total":>8}')
    print('-' * 80)
    for v, total in by_vendor.most_common():
        print(f'{v:60} {by_vendor_active[v]:>8} {total:>8}')


if __name__ == '__main__':
    main()
