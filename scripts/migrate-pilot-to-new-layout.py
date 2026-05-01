"""
One-shot migration: rename the 15 pilot images from
  data/generated-img2img-images/<handle>-gen-<N>.jpg
to
  data/img2img/phase1/batch-pilot/<handle>__pos<N>__<scene>.jpg

And rewrite the old manifest into the new lowercase schema at
  data/reports/generated-img2img-batch-pilot.csv

Run once. Idempotent — skips if already migrated.
"""
import csv
import json
import os
import shutil
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API   = 'https://{}/admin/api/2026-04'.format(STORE)

OLD_MANIFEST = os.path.join(ROOT, 'data', 'reports', 'generated-img2img-2026-04-28.csv')
OLD_DIR      = os.path.join(ROOT, 'data', 'generated-img2img-images')
NEW_DIR      = os.path.join(ROOT, 'data', 'img2img', 'phase1', 'batch-pilot')
NEW_MANIFEST = os.path.join(ROOT, 'data', 'reports', 'generated-img2img-batch-pilot.csv')

SCENES = {2: 'sceneA-institutional', 3: 'sceneB-smb', 4: 'studio-white'}

NEW_FIELDS = [
    'handle', 'product_id', 'position', 'scene', 'filename',
    'source_hero_url', 'fal_url', 'prompt', 'generation_id', 'status', 'timestamp',
]


def fetch_pid(handle, cache):
    if handle in cache:
        return cache[handle]
    url = '{}/products.json?handle={}&fields=id&limit=1'.format(API, urllib.parse.quote(handle))
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    pid = ''
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            products = data.get('products') or []
            if products:
                pid = str(products[0]['id'])
    except Exception as e:
        print('  warn: pid lookup failed for {}: {}'.format(handle, e))
    cache[handle] = pid
    return pid


def main():
    if not os.path.exists(OLD_MANIFEST):
        sys.exit('Old manifest not found: {}'.format(OLD_MANIFEST))
    os.makedirs(NEW_DIR, exist_ok=True)

    pid_cache = {}
    new_rows = []
    moved = 0
    missing = 0

    with open(OLD_MANIFEST, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') != 'OK':
                continue
            handle = row['Handle']
            try:
                pos = int(row['Image_Position'])
            except (ValueError, KeyError):
                continue
            scene = SCENES.get(pos)
            if not scene:
                continue
            old_filename = '{}-gen-{}.jpg'.format(handle, pos)
            old_path = os.path.join(OLD_DIR, old_filename)
            new_filename = '{}__pos{}__{}.jpg'.format(handle, pos, scene)
            new_path = os.path.join(NEW_DIR, new_filename)

            if os.path.exists(new_path):
                # already migrated
                pass
            elif os.path.exists(old_path):
                shutil.copy2(old_path, new_path)
                moved += 1
            else:
                print('  MISSING: {}'.format(old_path))
                missing += 1
                continue

            pid = fetch_pid(handle, pid_cache)

            new_rows.append({
                'handle':         handle,
                'product_id':     pid,
                'position':       pos,
                'scene':          scene,
                'filename':       new_filename,
                'source_hero_url': row.get('Source_Hero_URL', ''),
                'fal_url':        row.get('FAL_URL', ''),
                'prompt':         row.get('Prompt', ''),
                'generation_id':  '',  # not preserved in old manifest
                'status':         'OK',
                'timestamp':      row.get('Timestamp', ''),
            })

    new_rows.sort(key=lambda r: (r['handle'], r['position']))
    with open(NEW_MANIFEST, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=NEW_FIELDS)
        writer.writeheader()
        writer.writerows(new_rows)

    print('=' * 60)
    print('Migrated: {} files moved (already-present skipped)'.format(moved))
    print('Missing:  {}'.format(missing))
    print('Wrote:    {} rows to {}'.format(len(new_rows), NEW_MANIFEST))
    print('Output:   {}'.format(NEW_DIR))
    print('=' * 60)


if __name__ == '__main__':
    main()
