"""
Purge junk-SKU products from Shopify.

Safety rules enforced:
  1. Never delete anything with orders_90d > 0 or variant_orders_90d > 0
  2. Never delete service SKUs (delivery/installation) — they are checkout line items
  3. Dry-run by default; pass --confirm to actually delete

Input:  junk-inspection.json (from inspect-junk.py)
Output: purge-log.json
"""
import urllib.request
import urllib.error
import json
import sys
import time

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}


def delete_product(pid, attempt=0):
    req = urllib.request.Request(
        f'{API}/products/{pid}.json',
        headers=HEADERS,
        method='DELETE',
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            wait = 2 ** attempt
            print(f'    429, backing off {wait}s')
            time.sleep(wait)
            return delete_product(pid, attempt + 1)
        return e.code, e.read().decode()


def main():
    confirm = '--confirm' in sys.argv
    with open('junk-inspection.json') as f:
        report = json.load(f)

    safe_to_delete = []
    protected = []
    for r in report:
        reason = None
        if r['orders_90d'] > 0 or r['variant_orders_90d'] > 0:
            reason = f'has sales (orders_90d={r["orders_90d"]}, variant_orders_90d={r["variant_orders_90d"]})'
        elif r['suggested_action'] == 'service_sku_review':
            reason = 'service SKU (delivery/installation) — used at checkout'
        elif r['suggested_action'] == 'review':
            reason = 'looks like a real product, not junk — needs description, not delete'
        elif r['suggested_action'] != 'delete':
            reason = f'suggested_action={r["suggested_action"]}'

        if reason:
            protected.append({**r, 'protect_reason': reason})
        else:
            safe_to_delete.append(r)

    print(f'\n=== SAFE TO DELETE ({len(safe_to_delete)}) ===')
    for r in safe_to_delete:
        print(f'  {r["id"]:18}  {r["title"][:60]}')

    print(f'\n=== PROTECTED ({len(protected)}) ===')
    for r in protected:
        print(f'  [SKIP] {r["title"][:55]:55}  why: {r["protect_reason"]}')

    if not confirm:
        print(f'\nDRY RUN. Pass --confirm to delete {len(safe_to_delete)} products.')
        return

    print(f'\nDeleting {len(safe_to_delete)} products...')
    results = []
    for r in safe_to_delete:
        status, body = delete_product(r['id'])
        ok = status in (200, 204)
        results.append({'id': r['id'], 'title': r['title'], 'status': status,
                        'ok': ok, 'body': body[:200] if not ok else ''})
        marker = 'OK' if ok else f'FAIL {status}'
        print(f'  [{marker}] {r["title"][:55]}')
        time.sleep(0.55)

    succeeded = sum(1 for x in results if x['ok'])
    with open('purge-log.json', 'w') as f:
        json.dump({
            'confirmed': True,
            'attempted': len(results),
            'succeeded': succeeded,
            'failed': len(results) - succeeded,
            'results': results,
            'protected': protected,
        }, f, indent=2)
    print(f'\nDone: {succeeded}/{len(results)} deleted. Log: purge-log.json')


if __name__ == '__main__':
    main()
