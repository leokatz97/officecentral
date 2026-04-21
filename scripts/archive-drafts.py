"""
Archive all products currently in 'draft' status.
Dry-run by default; pass --confirm to write.
"""
import urllib.request
import urllib.error
import json
import re
import sys
import time

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}


def api_get(url, attempt=0):
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req) as resp:
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            return json.loads(resp.read().decode()), (m.group(1) if m else None)
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_get(url, attempt + 1)
        raise


def api_put(pid, body, attempt=0):
    payload = json.dumps(body).encode()
    req = urllib.request.Request(f'{API}/products/{pid}.json', data=payload, headers=HEADERS, method='PUT')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_put(pid, body, attempt + 1)
        return e.code, e.read().decode()


def main():
    confirm = '--confirm' in sys.argv
    drafts = []
    url = f'{API}/products.json?status=draft&limit=250&fields=id,title,status,handle,updated_at'
    while url:
        data, next_url = api_get(url)
        drafts.extend(data['products'])
        url = next_url

    print(f'Drafts found: {len(drafts)}')
    for d in drafts:
        print(f'  {d["id"]:18}  {d["title"][:70]}  updated={d["updated_at"][:10]}')

    if not confirm:
        print(f'\nDRY RUN. Pass --confirm to archive {len(drafts)} products.')
        return

    results = []
    for d in drafts:
        status, body = api_put(d['id'], {'product': {'id': d['id'], 'status': 'archived'}})
        ok = status in (200, 201)
        results.append({'id': d['id'], 'title': d['title'], 'status': status, 'ok': ok})
        print(f'  [{"OK" if ok else f"FAIL {status}"}] {d["title"][:55]}')
        time.sleep(0.55)

    succeeded = sum(1 for r in results if r['ok'])
    with open('archive-drafts-log.json', 'w') as f:
        json.dump({'attempted': len(results), 'succeeded': succeeded, 'results': results}, f, indent=2)
    print(f'\nDone: {succeeded}/{len(results)} archived.')


if __name__ == '__main__':
    main()
