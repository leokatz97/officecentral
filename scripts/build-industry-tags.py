"""
Phase X1 — build the industry-classification CSV for Steve's review.

Reads data/reports/taxonomy-tags-proposed.csv and classifies every active
product into exactly one of four industries: daycare, healthcare, educational,
or business (default). Exclusive classification — first rule that matches wins,
in the priority order below.

Writes data/reports/industry-tags-proposed.csv with the proposed tag + the
matched rule so Steve can spot-check.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_CSV = os.path.join(ROOT, 'data', 'reports', 'taxonomy-tags-proposed.csv')
OUT_CSV = os.path.join(ROOT, 'data', 'reports', 'industry-tags-proposed.csv')


# Order matters: first match wins. Daycare first so "kids chair" doesn't fall
# through to educational.
INDUSTRY_RULES = [
    ('industry:daycare', [
        'crib', 'stroller', 'toddler', ' kids ', "kid's", 'play table',
        'aktivity', 'daycare', 'preschool', 'arts & crafts', 'manipulative',
        'dramatic play', 'book cart', 'foundations sport', 'foundations next',
        'sport splash', 'serenity compact', 'kids chair', 'kids couch',
    ]),
    ('industry:healthcare', [
        # NOTE: 'obusforme' intentionally excluded — it's a general-purpose
        # back-support brand used in all office settings, not healthcare-
        # specific. See 2026-04-20 correction pass for context.
        'bariatric', 'patient', 'clinical', 'clinician', 'medical',
        'overbed', 'bedside', 'exam room', 'waiting room',
        'gc comet', 'primacare', 'nourish', 'ht patient',
        'recliner', 'dining seating', 'headboard', 'footboard',
    ]),
    ('industry:educational', [
        'student', 'tablet chair', 'tablet arm', 'classroom', 'lecture',
        'library', 'laboratory', ' school ', 'flip top training',
        'nesting training', 'dorm', 'penitentiary', 'teacher',
    ]),
]

DEFAULT_TAG = 'industry:business'


def classify(title_lower: str) -> tuple:
    """Return (industry_tag, matched_rule) for a product title."""
    for tag, keywords in INDUSTRY_RULES:
        for kw in keywords:
            if kw in title_lower:
                return tag, f'keyword:"{kw.strip()}"'
    return DEFAULT_TAG, 'default'


def main() -> None:
    rows_out = []
    counts = {'industry:business': 0, 'industry:educational': 0,
              'industry:healthcare': 0, 'industry:daycare': 0}
    skipped_no_type = 0

    with open(IN_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            handle = row['handle']
            title = row['title']
            type_tag = row['type_tag']
            admin_url = row['admin_url']

            title_lower = title.lower()
            tag, rule = classify(title_lower)

            # Products with no type_tag are usually service SKUs, Teknion
            # showcase pages, etc. — skip them UNLESS an industry keyword
            # explicitly matched. Keyword hits override the type_tag gate
            # so products like Foundations cribs/strollers still get
            # `industry:daycare` even without a type_tag.
            if not type_tag and rule == 'default':
                skipped_no_type += 1
                rows_out.append({
                    'handle': handle,
                    'title': title,
                    'industry_tag': '',
                    'matched_rule': 'SKIPPED — no type_tag (service SKU or edge case)',
                    'admin_url': admin_url,
                    'notes': row.get('notes', ''),
                })
                continue

            counts[tag] += 1

            rows_out.append({
                'handle': handle,
                'title': title,
                'industry_tag': tag,
                'matched_rule': rule,
                'admin_url': admin_url,
                'notes': '',
            })

    # Sort by industry then title for easy scanning
    order = {
        'industry:daycare': 0,
        'industry:healthcare': 1,
        'industry:educational': 2,
        'industry:business': 3,
        '': 4,
    }
    rows_out.sort(key=lambda r: (order.get(r['industry_tag'], 9), r['title']))

    fieldnames = ['handle', 'title', 'industry_tag', 'matched_rule',
                  'admin_url', 'notes']
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    total = sum(counts.values())
    print(f'Wrote {OUT_CSV}')
    print(f'  Total classified:           {total}')
    for tag, count in counts.items():
        print(f'    {tag:<26} {count:>4}')
    print(f'  Skipped (no type_tag):      {skipped_no_type}')


if __name__ == '__main__':
    main()
