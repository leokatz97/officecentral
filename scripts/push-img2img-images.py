"""
Push approved img2img images to Shopify.

Reads:
  data/reports/generated-img2img-<batch>.csv  (the new lowercase schema)
  data/reports/approval-<batch>.json
    {"batch": "...", "approvals": {handle: {pos2: bool, pos3: bool, pos4: bool, ...}}}

Pushes each row where the matching pos<N> is true.

Guards:
  - Hard-fail on SKIP_NOT_FOUND.
  - Pre-push hero-integrity: re-fetch product, confirm pos-1 still equals
    source_hero_url from manifest. Abort the product if hero changed.
  - Alt-text tagged with "[AI office context]" for future audit.

Usage:
  python3 scripts/push-img2img-images.py --batch=batch-pilot                    # DRY RUN
  python3 scripts/push-img2img-images.py --batch=batch-pilot --live             # write
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API   = 'https://{}/admin/api/2026-04'.format(STORE)
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type':           'application/json',
}

RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
TODAY   = datetime.now().strftime('%Y-%m-%d')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')

ALT_TAG = '[AI office context]'

CONTEXT_LABELS = {
    2: 'Studio white background',
    3: 'Office context A',
    4: 'Office context B',
}


def parse_args():
    live     = '--live' in sys.argv
    batch    = None
    manifest = None
    approval = None
    for arg in sys.argv[1:]:
        if arg.startswith('--batch='):
            batch = arg.split('=', 1)[1]
        elif arg.startswith('--manifest='):
            manifest = arg.split('=', 1)[1]
        elif arg.startswith('--approval='):
            approval = arg.split('=', 1)[1]
    if not batch:
        sys.exit('Required: --batch=<name>  (e.g. --batch=batch-pilot)')
    return live, batch, manifest, approval


def load_manifest(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('status') == 'OK':
                rows.append(row)
    return rows


def load_approval(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get('approvals', {})


def filter_approved(manifest_rows, approvals):
    out = []
    for row in manifest_rows:
        handle = row['handle']
        try:
            pos = int(row['position'])
        except (ValueError, KeyError):
            continue
        a = approvals.get(handle) or {}
        key = 'pos{}'.format(pos)
        if a.get(key) is True:
            out.append(row)
    return out


def fetch_product(handle, cache):
    if handle in cache:
        return cache[handle]
    encoded = urllib.parse.quote(handle)
    url = '{}/products.json?handle={}&fields=id,images&limit=1'.format(API, encoded)
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    pid, pos1_src = None, None
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data     = json.loads(resp.read().decode())
            products = data.get('products', [])
            if products:
                p = products[0]
                pid = str(p['id'])
                images = p.get('images') or []
                if images:
                    pos1 = sorted(images, key=lambda i: i.get('position') or 999)[0]
                    pos1_src = pos1.get('src')
    except urllib.error.HTTPError as e:
        print('  FETCH-ERR {}: {}'.format(e.code, e.read().decode()[:120]))
    except Exception as e:
        print('  FETCH-ERR: {}'.format(e))
    cache[handle] = (pid, pos1_src)
    time.sleep(0.5)
    return pid, pos1_src


def push_image(product_id, fal_url, position, alt_text, retries=3):
    url = '{}/products/{}/images.json'.format(API, product_id)
    payload = json.dumps({
        'image': {
            'src':      fal_url,
            'position': int(position),
            'alt':      alt_text,
        }
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='POST')
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.loads(resp.read().decode())['image']
        except urllib.error.HTTPError:
            raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                wait = attempt * 5
                print('  network error (attempt {}/{}): {} — retrying in {}s'.format(attempt, retries, e, wait))
                time.sleep(wait)
    raise last_err


def build_alt(title, position):
    label = CONTEXT_LABELS.get(int(position), 'Office context')
    return '{} - {} {}'.format(title or 'Product', label, ALT_TAG).strip()


def resolve_paths(batch, manifest_arg, approval_arg):
    manifest = manifest_arg or os.path.join(RPT_DIR, 'generated-img2img-{}.csv'.format(batch))
    approval = approval_arg or os.path.join(RPT_DIR, 'approval-{}.json'.format(batch))
    if not os.path.exists(manifest):
        sys.exit('Manifest not found: {}'.format(manifest))
    if not os.path.exists(approval):
        sys.exit('Approval JSON not found: {}\nRun render-image-review.py + serve-review.py first.'.format(approval))
    return manifest, approval


def main():
    live, batch, manifest_arg, approval_arg = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    manifest_path, approval_path = resolve_paths(batch, manifest_arg, approval_arg)

    print('Mode:     ' + mode)
    print('Manifest: ' + manifest_path)
    print('Approval: ' + approval_path)

    rows = load_manifest(manifest_path)
    approvals = load_approval(approval_path)
    rows = filter_approved(rows, approvals)
    if not rows:
        sys.exit('No approved rows to push. Check the approval JSON.')

    by_handle = {}
    for row in rows:
        by_handle.setdefault(row['handle'], []).append(row)

    print('{} approved images for {} products.\n'.format(len(rows), len(by_handle)))

    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RPT_DIR, exist_ok=True)

    cache = {}
    pushed = []
    aborted = []
    errors = []
    result_rows = []

    # Title cache for alt text — manifest doesn't carry title, fetch lazily.
    title_cache = {}

    def get_title(handle, pid):
        if handle in title_cache:
            return title_cache[handle]
        encoded = urllib.parse.quote(handle)
        url = '{}/products.json?handle={}&fields=title&limit=1'.format(API, encoded)
        req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
        title = ''
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                products = data.get('products') or []
                if products:
                    title = products[0].get('title') or ''
        except Exception:
            pass
        title_cache[handle] = title
        return title

    for i, (handle, img_rows) in enumerate(by_handle.items(), 1):
        print('[{}/{}] {}'.format(i, len(by_handle), handle))

        pid, live_pos1 = fetch_product(handle, cache)

        if not pid:
            print('  HARD-FAIL: product handle not found in Shopify.')
            print('  Reconcile {} before re-running this batch.'.format(handle))
            sys.exit(1)

        manifest_hero = img_rows[0].get('source_hero_url') or ''
        if manifest_hero and live_pos1 and manifest_hero != live_pos1:
            print('  ABORT: hero changed between generation and push.')
            print('    manifest: {}'.format(manifest_hero[:100]))
            print('    live:     {}'.format(live_pos1[:100]))
            aborted.append(handle)
            for row in img_rows:
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   row['position'],
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL':  '',
                    'Alt_Text':         '',
                    'FAL_Source_URL':   row.get('fal_url', ''),
                    'Source_Hero_URL':  manifest_hero,
                    'Live_Pos1_URL':    live_pos1 or '',
                    'Status':           'ABORT_HERO_CHANGED',
                })
            continue

        if not live_pos1:
            print('  ABORT: live product has no pos-1 image.')
            aborted.append(handle)
            for row in img_rows:
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   row['position'],
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL':  '',
                    'Alt_Text':         '',
                    'FAL_Source_URL':   row.get('fal_url', ''),
                    'Source_Hero_URL':  manifest_hero,
                    'Live_Pos1_URL':    '',
                    'Status':           'ABORT_NO_HERO',
                })
            continue

        title = get_title(handle, pid)

        for row in sorted(img_rows, key=lambda r: int(r['position'])):
            pos      = row['position']
            fal_url  = row['fal_url']
            alt_text = build_alt(title, pos)

            if not live:
                print('  pos-{}: DRY RUN -> would push to product {}'.format(pos, pid))
                print('    alt: {}'.format(alt_text))
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL':  '',
                    'Alt_Text':         alt_text,
                    'FAL_Source_URL':   fal_url,
                    'Source_Hero_URL':  manifest_hero,
                    'Live_Pos1_URL':    live_pos1,
                    'Status':           'DRY_RUN',
                })
                continue

            try:
                img_data = push_image(pid, fal_url, pos, alt_text)
                cdn_url  = img_data.get('src', '')
                img_id   = str(img_data.get('id', ''))
                pushed.append((handle, pos))
                print('  pos-{}: PUSHED -> {}'.format(pos, cdn_url[:70]))
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': img_id,
                    'Shopify_CDN_URL':  cdn_url,
                    'Alt_Text':         alt_text,
                    'FAL_Source_URL':   fal_url,
                    'Source_Hero_URL':  manifest_hero,
                    'Live_Pos1_URL':    live_pos1,
                    'Status':           'PUSHED',
                })
                time.sleep(0.5)
            except urllib.error.HTTPError as e:
                code = e.code
                msg  = e.read().decode()[:300]
                if code == 429:
                    print('  pos-{}: 429 rate limit, sleeping 5s and retrying'.format(pos))
                    time.sleep(5)
                    try:
                        img_data = push_image(pid, fal_url, pos, alt_text)
                        cdn_url  = img_data.get('src', '')
                        img_id   = str(img_data.get('id', ''))
                        pushed.append((handle, pos))
                        print('  pos-{}: PUSHED (retry) -> {}'.format(pos, cdn_url[:70]))
                        result_rows.append({
                            'Handle':           handle,
                            'Product_ID':       pid,
                            'Image_Position':   pos,
                            'Shopify_Image_ID': img_id,
                            'Shopify_CDN_URL':  cdn_url,
                            'Alt_Text':         alt_text,
                            'FAL_Source_URL':   fal_url,
                            'Source_Hero_URL':  manifest_hero,
                            'Live_Pos1_URL':    live_pos1,
                            'Status':           'PUSHED',
                        })
                        time.sleep(0.5)
                        continue
                    except Exception as e2:
                        msg = str(e2)

                print('  pos-{}: ERROR {} - {}'.format(pos, code, msg[:150]))
                errors.append({'handle': handle, 'pos': pos, 'code': code, 'msg': msg[:300]})
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL':  '',
                    'Alt_Text':         alt_text,
                    'FAL_Source_URL':   fal_url,
                    'Source_Hero_URL':  manifest_hero,
                    'Live_Pos1_URL':    live_pos1,
                    'Status':           'ERROR_{}'.format(code),
                })

    out_csv = os.path.join(RPT_DIR, 'shopify-img2img-pushed-{}.csv'.format(TODAY))
    fieldnames = [
        'Handle', 'Product_ID', 'Image_Position', 'Shopify_Image_ID',
        'Shopify_CDN_URL', 'Alt_Text', 'FAL_Source_URL',
        'Source_Hero_URL', 'Live_Pos1_URL', 'Status',
    ]
    write_header = not os.path.exists(out_csv)
    with open(out_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(result_rows)

    log_path = os.path.join(LOG_DIR, 'push-img2img-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':     mode,
            'batch':    batch,
            'manifest': manifest_path,
            'approval': approval_path,
            'products': len(by_handle),
            'images':   len(rows),
            'pushed':   len(pushed),
            'aborted':  aborted,
            'errors':   errors,
        }, f, indent=2)

    print()
    print('=' * 60)
    print('Summary: ' + mode)
    print('  Products:   {}'.format(len(by_handle)))
    print('  Pushed:     {}'.format(len(pushed)))
    print('  Aborted:    {}'.format(len(aborted)))
    print('  Errors:     {}'.format(len(errors)))
    print('  Result CSV: ' + out_csv)
    print('  Audit log:  ' + log_path)
    print('=' * 60)

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to push.')


if __name__ == '__main__':
    main()
