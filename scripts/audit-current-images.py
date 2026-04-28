"""
Audit every product image on the live Shopify store for AI-generated residuals.

Flags any image whose src matches *.fal.media* or whose alt ends in one of the
known AI-generation suffixes from the old pipeline.

Usage:
  python3 scripts/audit-current-images.py

Exit code 0 if 0 flagged; exit code 1 if any are found (so CI can gate on it).
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import datetime

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

# Known AI alt-text suffixes from old pipeline runs
AI_ALT_SUFFIXES = (
    ' - Office Setting',
    ' - Workspace View',
    ' - Detail Close-Up',
    ' - Studio White',
)

OUTPUT_CSV = os.path.join(RPT_DIR, f'current-images-audit-{TODAY}.csv')


# ---------------------------------------------------------------------------
# Shopify pagination helper
# ---------------------------------------------------------------------------
def get_all_products():
    url = f'{API}/products.json?limit=250&fields=id,handle,title,images'
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

    print('Fetching all products from Shopify…')
    products = get_all_products()
    print(f'  → {len(products)} products loaded')

    rows = []
    total_images = 0
    flagged = 0

    for p in products:
        for img in p.get('images', []):
            total_images += 1
            src = img.get('src', '')
            alt = img.get('alt', '') or ''
            reason = None

            if 'fal.media' in src:
                reason = 'fal_media_url'
            elif any(alt.endswith(suffix) for suffix in AI_ALT_SUFFIXES):
                reason = 'ai_alt_suffix'

            if reason:
                flagged += 1
                rows.append({
                    'handle':        p['handle'],
                    'product_id':    p['id'],
                    'title':         p['title'],
                    'image_id':      img['id'],
                    'position':      img.get('position', ''),
                    'src':           src,
                    'alt':           alt,
                    'flagged_reason': reason,
                })

    # Write CSV regardless (empty is fine — confirms clean run)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'handle', 'product_id', 'title', 'image_id', 'position', 'src', 'alt', 'flagged_reason'
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f'\nSummary')
    print(f'  Products : {len(products)}')
    print(f'  Images   : {total_images}')
    print(f'  Flagged  : {flagged}')
    print(f'  Output   : {OUTPUT_CSV}')

    if flagged:
        print(f'\n⚠️  {flagged} AI-residual image(s) found — review {OUTPUT_CSV} before continuing.')
        sys.exit(1)
    else:
        print('\n✅  Store is clean — 0 AI-residual images.')
        sys.exit(0)


if __name__ == '__main__':
    main()
