"""
Phase X3 — correct industry tag misclassifications flagged 2026-04-20.

Two fix sets:

1. ObusForme (7 products) — the classifier put these in `industry:healthcare`
   via the `obusforme` keyword, but ObusForme is a general-purpose ergonomic
   back-support brand, not healthcare-specific. Remove `industry:healthcare`
   and add `industry:business`.

2. Foundations cribs/strollers (3 products) — skipped by the classifier
   because they have no `type_tag` upstream, but they're obvious daycare.
   Add `industry:daycare`.

Reads current tags live, computes the corrected tag string, writes back.
Idempotent and safe to re-run.

Run AFTER push-industry-tags.py has finished — otherwise the main push will
re-add `industry:healthcare` to the ObusForme rows after this removes it.

Usage:
  python3 scripts/fix-industry-tag-corrections.py              # dry run
  python3 scripts/fix-industry-tag-corrections.py --live       # write
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

LOG_DIR = os.path.join(ROOT, 'data', 'logs')

# (product_id, title, tags_to_remove, tags_to_add)
OBUSFORME_SWAP = ([], ['industry:healthcare'], ['industry:business'])
FOUNDATIONS_ADD = ([], [], ['industry:daycare'])

FIXES = [
    # ObusForme: healthcare → business
    ('9776141041977', 'Basics® ObusForme® Elite Heavy Duty Multi-Tilter Chair TS2770-3',
     ['industry:healthcare'], ['industry:business']),
    ('9666747924793', 'Global OBUSforme Elite Multi-Tilter Chair High Back',
     ['industry:healthcare'], ['industry:business']),
    ('9666748711225', 'OBUSforme Elite Multi-Tilter Medium Back Chair',
     ['industry:healthcare'], ['industry:business']),
    ('10052615831865', 'ObusForme Comfort High Back Chair 1260-3 Schukra',
     ['industry:healthcare'], ['industry:business']),
    ('9039326609721', 'ObusForme Comfort High back Chair 1240-3',
     ['industry:healthcare'], ['industry:business']),
    ('9938997543225', 'ObusForme Comfort Medium back Chair 1261-3 Schukra',
     ['industry:healthcare'], ['industry:business']),
    ('9840806887737', 'ObusForme Comfort Medium back Chair 1241-3',
     ['industry:healthcare'], ['industry:business']),

    # Foundations: skipped → daycare
    ('9685414871353', 'Foundations Next Gen Serenity Compact Crib',
     [], ['industry:daycare']),
    ('9685444297017', 'Foundations Sport Splash 3-Seat Strollers',
     [], ['industry:daycare']),
    ('9685440528697', 'Foundations Sport Splash, Quad Strollers',
     [], ['industry:daycare']),
]


def fetch_tags(pid: str) -> str:
    url = f'{API}/products/{pid}.json?fields=id,tags'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product'].get('tags', '') or ''


def put_tags(pid: str, tags_csv: str) -> int:
    url = f'{API}/products/{pid}.json'
    payload = json.dumps({'product': {'id': int(pid), 'tags': tags_csv}}).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as resp:
        return resp.status


def apply_diff(existing_csv: str, remove: list, add: list) -> tuple:
    """Return (new_csv, changed, removed_hits, added_hits)."""
    existing = [t.strip() for t in existing_csv.split(',') if t.strip()]
    remove_lower = {t.lower() for t in remove}
    add_lower = {t.lower() for t in add}

    kept = [t for t in existing if t.lower() not in remove_lower]
    removed_hits = [t for t in existing if t.lower() in remove_lower]

    existing_lower_after_remove = {t.lower() for t in kept}
    added_hits = [t for t in add if t.lower() not in existing_lower_after_remove]
    kept.extend(added_hits)

    new_csv = ', '.join(kept)
    changed = (new_csv != existing_csv) or bool(removed_hits) or bool(added_hits)
    return new_csv, changed, removed_hits, added_hits


def main() -> None:
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print(f'Fixes queued: {len(FIXES)}')
    print()

    updated = 0
    noop = 0
    errors = []
    results = []

    for i, (pid, title, remove, add) in enumerate(FIXES, 1):
        try:
            existing = fetch_tags(pid)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:120]}'
            print(f'  [{i}/{len(FIXES)}] FETCH-ERR {msg} · {title[:55]}')
            errors.append({'pid': pid, 'title': title, 'stage': 'fetch',
                           'error': msg})
            continue

        new_csv, changed, removed_hits, added_hits = apply_diff(existing, remove, add)

        if not changed:
            noop += 1
            print(f'  [{i}/{len(FIXES)}] NOOP · {title[:55]}')
            time.sleep(0.25)
            continue

        action = []
        if removed_hits:
            action.append(f'-{",".join(removed_hits)}')
        if added_hits:
            action.append(f'+{",".join(added_hits)}')
        action_str = ' '.join(action)

        if not live:
            print(f'  [{i}/{len(FIXES)}] WOULD {action_str} · {title[:55]}')
            continue

        try:
            status = put_tags(pid, new_csv)
            updated += 1
            results.append({'pid': pid, 'title': title,
                            'removed': removed_hits, 'added': added_hits,
                            'status': status})
            print(f'  [{i}/{len(FIXES)}] {status} {action_str} · {title[:55]}')
            time.sleep(0.6)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:200]}'
            print(f'  [{i}/{len(FIXES)}] PUT-ERR {msg} · {title[:55]}')
            errors.append({'pid': pid, 'title': title, 'stage': 'put',
                           'error': msg})

    print()
    print(f'Summary: {mode}')
    print(f'  NOOP:     {noop}')
    print(f'  Updated:  {updated}')
    print(f'  Errors:   {len(errors)}')

    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_path = os.path.join(LOG_DIR, f'fix-industry-tag-corrections-{ts}.json')
    with open(log_path, 'w') as f:
        json.dump({'mode': mode, 'total': len(FIXES),
                   'noop': noop, 'updated': updated,
                   'errors': errors, 'results': results}, f, indent=2)
    print(f'  Audit log: {log_path}')

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
