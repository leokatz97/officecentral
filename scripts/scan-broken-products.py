"""
Scan all products for issues that cause broken product pages:
  - missing images (images == 0)
  - all variants out of stock + inventory tracked (shows "unavailable")
  - status == active but handle looks malformed
  - 404 check: HEAD every product URL on the public site
Writes report to data/broken-products-report.json
"""
import urllib.request
import urllib.error
import urllib.parse
import json
import re
import os
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, '.env')
TOKEN = None
for line in open(ENV_PATH):
    if line.startswith('SHOPIFY_TOKEN='):
        TOKEN = line.strip().split('=', 1)[1].strip('"').strip("'")
        break

STORE = 'office-central-online.myshopify.com'
PUBLIC = 'https://brantbusinessinteriors.com'
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}


def fetch_all_products():
    products = []
    fields = 'id,title,handle,status,published_at,images,variants,vendor,product_type,tags'
    url = f'{API}/products.json?limit=250&fields={fields}'
    while url:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            products.extend(data['products'])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(products)}...')
    return products


def check_url(url, timeout=10):
    """HEAD the public URL. Return (status_code, final_url) or (None, error)."""
    try:
        req = urllib.request.Request(url, method='HEAD', headers={
            'User-Agent': 'Mozilla/5.0 (office-central audit)'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.url
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:
        return None, str(e)


def main():
    print('Fetching all products...')
    products = fetch_all_products()
    print(f'\nTotal: {len(products)} products\n')

    no_images = []
    all_oos = []           # all variants out of stock + tracked = "unavailable"
    zero_price = []
    bad_handle = []
    drafts_with_handle = []
    live_404 = []
    live_non_200 = []

    # Filter to active + published products for the live check
    for p in products:
        pid = p['id']
        title = p['title']
        handle = p.get('handle') or ''
        status = p.get('status')
        published = p.get('published_at')
        images = p.get('images') or []
        variants = p.get('variants') or []

        if not images:
            no_images.append({'id': pid, 'title': title, 'handle': handle, 'status': status})

        # Check variant availability
        tracked_variants = [v for v in variants if v.get('inventory_management') == 'shopify']
        if tracked_variants:
            oos = [v for v in tracked_variants if (v.get('inventory_quantity') or 0) <= 0
                   and v.get('inventory_policy') == 'deny']
            if oos and len(oos) == len(tracked_variants):
                all_oos.append({
                    'id': pid, 'title': title, 'handle': handle,
                    'status': status, 'variant_count': len(variants)
                })

        # Zero/missing price on any variant
        for v in variants:
            try:
                if float(v.get('price') or 0) <= 0:
                    zero_price.append({
                        'id': pid, 'title': title, 'handle': handle,
                        'variant_id': v['id'], 'variant_title': v.get('title')
                    })
                    break
            except (ValueError, TypeError):
                pass

        # Malformed handle
        if handle and not re.match(r'^[a-z0-9][a-z0-9\-]*$', handle):
            bad_handle.append({'id': pid, 'title': title, 'handle': handle})

        if status == 'draft' and handle:
            drafts_with_handle.append({'id': pid, 'title': title, 'handle': handle})

    # Live HTTP check — only on active + published
    live_targets = [p for p in products if p.get('status') == 'active' and p.get('published_at')]
    print(f'\nLive-checking {len(live_targets)} active/published product URLs...')
    for i, p in enumerate(live_targets, 1):
        url = f"{PUBLIC}/products/{p['handle']}"
        code, final = check_url(url)
        if code == 404:
            live_404.append({'id': p['id'], 'title': p['title'], 'handle': p['handle'], 'url': url})
        elif code is None or code >= 400:
            live_non_200.append({
                'id': p['id'], 'title': p['title'], 'handle': p['handle'],
                'url': url, 'code': code, 'err': str(final) if code is None else None
            })
        if i % 25 == 0:
            print(f'  checked {i}/{len(live_targets)}... ({len(live_404)} 404s, {len(live_non_200)} other errors)')
        time.sleep(0.05)  # be polite

    report = {
        'total_products': len(products),
        'active_published': len(live_targets),
        'summary': {
            'no_images': len(no_images),
            'all_oos_active': sum(1 for p in all_oos if p['status'] == 'active'),
            'all_oos_total': len(all_oos),
            'zero_price': len(zero_price),
            'bad_handle': len(bad_handle),
            'drafts_with_handle': len(drafts_with_handle),
            'live_404': len(live_404),
            'live_non_200': len(live_non_200),
        },
        'no_images': no_images,
        'all_oos': all_oos,
        'zero_price': zero_price,
        'bad_handle': bad_handle,
        'live_404': live_404,
        'live_non_200': live_non_200,
    }

    out = os.path.join(ROOT, 'data', 'broken-products-report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)

    print('\n=== SUMMARY ===')
    for k, v in report['summary'].items():
        print(f'  {k:22} {v}')
    print(f'\nReport: {out}')


if __name__ == '__main__':
    main()
