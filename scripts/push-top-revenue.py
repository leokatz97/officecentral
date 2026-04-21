"""
Pushes cleaned body_html back to Shopify for the products listed in
clean-top-revenue-payload.json.

Safety:
- Re-fetches each product's current body_html right before writing and saves
  it to a timestamped backup file (rollback path).
- Aborts the product if the current server body_html no longer matches the
  'before' recorded in the payload (catalog changed since dry-run — needs
  re-review).
- 500ms sleep between writes to stay well under Shopify's 2 req/s admin limit.
"""

import json
import time
import urllib.error
import urllib.request
from datetime import datetime

PAYLOAD_PATH = 'clean-top-revenue-payload.json'

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'


def fetch_product(pid):
    url = f'{API}/products/{pid}.json?fields=id,title,body_html'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product']


def update_body_html(pid, new_body):
    url = f'{API}/products/{pid}.json'
    body = json.dumps({'product': {'id': pid, 'body_html': new_body}}).encode()
    req = urllib.request.Request(
        url, data=body, method='PUT',
        headers={
            'X-Shopify-Access-Token': TOKEN,
            'Content-Type': 'application/json',
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product']


def main():
    with open(PAYLOAD_PATH) as f:
        payload = json.load(f)

    print(f'Pushing cleaned body_html for {len(payload)} products')
    print(f'Store: {STORE}')
    print()

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = f'body-html-backup-{timestamp}.json'
    pushed = []
    skipped_drift = []
    errors = []
    backup = []

    for i, item in enumerate(payload, 1):
        pid = item['id']
        title = item['title']
        expected_before = item['before']
        new_body = item['after']

        try:
            current = fetch_product(pid)
        except urllib.error.HTTPError as e:
            errors.append({'id': pid, 'title': title, 'phase': 'fetch', 'error': f'{e.code} {e.reason}'})
            print(f'  [{i:>2}/{len(payload)}] ERROR fetching {pid}: {e.code}')
            continue
        except Exception as e:
            errors.append({'id': pid, 'title': title, 'phase': 'fetch', 'error': str(e)})
            print(f'  [{i:>2}/{len(payload)}] ERROR fetching {pid}: {e}')
            continue

        current_body = current.get('body_html') or ''
        backup.append({'id': pid, 'title': current.get('title', title), 'body_html': current_body})

        if current_body.strip() != expected_before.strip():
            skipped_drift.append({'id': pid, 'title': title})
            print(f'  [{i:>2}/{len(payload)}] SKIP drift (content changed since dry-run): {title[:55]}')
            time.sleep(0.5)
            continue

        try:
            update_body_html(pid, new_body)
            pushed.append({'id': pid, 'title': title})
            print(f'  [{i:>2}/{len(payload)}] OK  {title[:60]}')
        except urllib.error.HTTPError as e:
            body = ''
            try:
                body = e.read().decode()
            except Exception:
                pass
            errors.append({'id': pid, 'title': title, 'phase': 'push', 'error': f'{e.code} {e.reason} {body[:200]}'})
            print(f'  [{i:>2}/{len(payload)}] ERROR pushing {pid}: {e.code} {e.reason}')
        except Exception as e:
            errors.append({'id': pid, 'title': title, 'phase': 'push', 'error': str(e)})
            print(f'  [{i:>2}/{len(payload)}] ERROR pushing {pid}: {e}')

        time.sleep(0.5)

    with open(backup_path, 'w') as f:
        json.dump(backup, f, indent=2)

    print()
    print(f'Pushed:        {len(pushed)}')
    print(f'Skipped drift: {len(skipped_drift)}')
    print(f'Errors:        {len(errors)}')
    print(f'Backup:        {backup_path}')

    if skipped_drift:
        print('\nDrift-skipped (re-run dry-run for these before pushing):')
        for s in skipped_drift:
            print(f'  - {s["title"]} (id {s["id"]})')

    if errors:
        print('\nErrors:')
        for e in errors:
            print(f'  - [{e["phase"]}] {e["title"]} (id {e["id"]}): {e["error"]}')


if __name__ == '__main__':
    main()
