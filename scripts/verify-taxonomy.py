"""
Phase B verification — spot-check the Shopify-side tags after push-taxonomy-tags.py.

Samples 20 random products from the proposed CSV, fetches their live tags via
the Shopify Admin API, and reports which facet tags are present. Exits 0 if
every sampled row has at least a type:* tag, non-zero otherwise.

Usage:
  python3 scripts/verify-taxonomy.py              # sample 20 random
  python3 scripts/verify-taxonomy.py --sample=50  # larger sample
"""
import csv
import json
import os
import random
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'

IN_CSV = os.path.join(ROOT, 'data', 'reports', 'taxonomy-tags-proposed.csv')
ID_FROM_URL = re.compile(r'/products/(\d+)')


def fetch_tags(pid: str) -> list:
    url = f'{API}/products/{pid}.json?fields=id,tags'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        tags_csv = json.loads(resp.read().decode())['product'].get('tags', '') or ''
    return [t.strip() for t in tags_csv.split(',') if t.strip()]


def main() -> None:
    sample_size = 20
    for arg in sys.argv[1:]:
        if arg.startswith('--sample='):
            sample_size = int(arg.split('=', 1)[1])

    with open(IN_CSV, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    taggable = [r for r in rows if r['type_tag'] or r['room_tag']
                or r['industry_tag'] or r['bestseller'] == 'true']
    sample = random.sample(taggable, min(sample_size, len(taggable)))

    print(f'Sampling {len(sample)} of {len(taggable)} taggable products')
    print()

    missing_type = 0
    partial = 0
    ok = 0

    for i, row in enumerate(sample, 1):
        m = ID_FROM_URL.search(row['admin_url'])
        pid = m.group(1) if m else None
        if not pid:
            print(f'  [{i}] BAD-URL {row["title"][:60]}')
            continue

        live = fetch_tags(pid)
        has_type = any(t.startswith('type:') for t in live)
        has_room = any(t.startswith('room:') for t in live)
        has_industry = any(t.startswith('industry:') for t in live)
        has_bestseller = 'bestseller' in live

        expected = {
            'type': bool(row['type_tag']),
            'room': bool(row['room_tag']),
            'industry': bool(row['industry_tag']),
            'bestseller': row['bestseller'] == 'true',
        }
        live_flags = {
            'type': has_type,
            'room': has_room,
            'industry': has_industry,
            'bestseller': has_bestseller,
        }

        mismatches = [k for k, v in expected.items() if v and not live_flags[k]]

        if expected['type'] and not has_type:
            missing_type += 1
            mark = 'MISSING-TYPE'
        elif mismatches:
            partial += 1
            mark = f'PARTIAL ({",".join(mismatches)})'
        else:
            ok += 1
            mark = 'OK'

        tags_summary = [t for t in live if t.startswith(('type:', 'room:', 'industry:'))
                        or t == 'bestseller']
        print(f'  [{i:>2}] {mark:<28} {row["title"][:50]:<50} → {tags_summary}')

    print()
    print(f'OK:            {ok}')
    print(f'Partial:       {partial}')
    print(f'Missing type:  {missing_type}')

    if missing_type > 0:
        print('\nFAIL: some sampled products missing required type tag.')
        sys.exit(1)

    print('\nPASS: all sampled products have at least a type: tag.')


if __name__ == '__main__':
    main()
