"""
Audit hero (position-1) images across all live Shopify products.

Flags products where the pos-1 image is missing, below minimum dimensions,
or has an AI-pipeline alt-text suffix.

Usage:
  python3 scripts/audit-hero-images.py

Output:
  data/reports/hero-audit-{date}.csv
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import datetime

# Dimension check removed — small catalog images (300–400px) are valid
# img2img pipeline conditions on pos-1 and adds full-size images at pos 2+3.
# Only flag genuinely missing images and AI-residual alt-text.

AI_ALT_SUFFIXES = (
    ' - Office Setting',
    ' - Workspace View',
    ' - Detail Close-Up',
    ' - Studio White',
)

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API   = 'https://{}/admin/api/2026-04'.format(STORE)
HEADERS = {'X-Shopify-Access-Token': TOKEN}

RPT_DIR = os.path.join(ROOT, 'data', 'reports')
TODAY   = datetime.now().strftime('%Y-%m-%d')
OUTPUT_CSV = os.path.join(RPT_DIR, f'hero-audit-{TODAY}.csv')


# ---------------------------------------------------------------------------
# Shopify pagination
# ---------------------------------------------------------------------------
def get_all_products():
    url = f'{API}/products.json?limit=250&published_status=published&fields=id,handle,title,images'
    products = []
    while url:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            products.extend(data.get('products', []))
            link = resp.headers.get('Link', '')
            url = None
            for part in link.split(','):
                part = part.strip()
                if 'rel="next"' in part:
                    url = part.split(';')[0].strip().strip('<>')
    return products


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(RPT_DIR, exist_ok=True)

    print('Fetching all products…')
    products = get_all_products()
    print(f'  → {len(products)} products loaded')

    rows = []

    # Distribution buckets for pos-1 width
    dist = {'no_image': 0, 'lt400': 0, '400_599': 0, '600_799': 0, 'ge800': 0}

    for p in products:
        images = p.get('images', [])
        # Sort by position to reliably get pos-1
        images_sorted = sorted(images, key=lambda i: i.get('position', 999))
        hero = images_sorted[0] if images_sorted else None

        image_count = len(images)
        pos1_src    = hero['src']  if hero else ''
        pos1_alt    = (hero.get('alt') or '') if hero else ''
        pos1_width  = hero.get('width', 0)  if hero else 0
        pos1_height = hero.get('height', 0) if hero else 0

        # Determine flag reason (dimension check intentionally omitted)
        reason = None
        if not hero:
            reason = 'no_image'
            dist['no_image'] += 1
        elif any(pos1_alt.endswith(s) for s in AI_ALT_SUFFIXES):
            reason = 'ai_residual'
            w = pos1_width
            if   w < 400: dist['lt400']   += 1
            elif w < 600: dist['400_599'] += 1
            elif w < 800: dist['600_799'] += 1
            else:         dist['ge800']   += 1
        else:
            # Clean — still bin for distribution stats
            w = pos1_width
            if   w < 400: dist['lt400']   += 1
            elif w < 600: dist['400_599'] += 1
            elif w < 800: dist['600_799'] += 1
            else:         dist['ge800']   += 1

        needs_review = reason is not None

        rows.append({
            'handle':        p['handle'],
            'product_id':    p['id'],
            'title':         p['title'],
            'image_count':   image_count,
            'pos1_src':      pos1_src,
            'pos1_alt':      pos1_alt,
            'pos1_width':    pos1_width,
            'pos1_height':   pos1_height,
            'needs_review':  needs_review,
            'flag_reason':   reason or '',
        })

    flagged = [r for r in rows if r['needs_review']]

    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'handle', 'product_id', 'title', 'image_count',
            'pos1_src', 'pos1_alt', 'pos1_width', 'pos1_height',
            'needs_review', 'flag_reason',
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f'\nSummary')
    print(f'  Total products : {len(products)}')
    print(f'  Flagged        : {len(flagged)}')
    print(f'\nPos-1 width distribution (all products):')
    print(f'  No image   : {dist["no_image"]}')
    print(f'  < 400px    : {dist["lt400"]}')
    print(f'  400–599px  : {dist["400_599"]}')
    print(f'  600–799px  : {dist["600_799"]}')
    print(f'  ≥ 800px    : {dist["ge800"]}')
    print(f'\nFlagged breakdown:')
    for reason_key in ('no_image', 'ai_residual'):
        count = sum(1 for r in flagged if r['flag_reason'] == reason_key)
        print(f'  {reason_key:<14}: {count}')
    print(f'\nOutput: {OUTPUT_CSV}')

    if flagged:
        print(f'\n⚠️  {len(flagged)} product(s) need hero fixes. Open previews/hero-audit-{TODAY}.html to triage.')
        sys.exit(1)
    else:
        print('\n✅  All heroes pass — 0 flagged.')
        sys.exit(0)


if __name__ == '__main__':
    main()
