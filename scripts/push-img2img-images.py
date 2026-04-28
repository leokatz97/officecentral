"""
Push approved img2img images to Shopify (Phase 3d).

Fork of push-generated-images.py with these deltas:
  1. Reads data/reports/generated-img2img-{date}.csv joined with the approval
     JSON (data/reports/approval-{date}-batch-{N}.json). Only pushes rows where
     the approval JSON says true for that position.
  2. HARD-FAILS on SKIP_NOT_FOUND in the main loop (the original logged and
     continued — see scripts/push-generated-images.py:203-217). Reconcile handles
     before re-running.
  3. PRE-PUSH HERO-INTEGRITY CHECK: re-fetches the product, confirms pos-1 src
     still equals Source_Hero_URL from the manifest. If the hero was changed
     between generation and push, that product is aborted (the AI was conditioned
     on a now-stale reference).
  4. ALT-TEXT TAGGED with '[AI office context]' so future audit scripts can
     identify these images in bulk.

Reuses fetch_product_id and push_image (retry/backoff) by copy-adapt — does not
modify the original push-generated-images.py.

Usage:
  python3 scripts/push-img2img-images.py --batch=pilot-5                    # DRY RUN
  python3 scripts/push-img2img-images.py --batch=pilot-5 --live             # write
  python3 scripts/push-img2img-images.py --batch=pilot-5 \
          --manifest=data/reports/generated-img2img-2026-04-28.csv \
          --approval=data/reports/approval-2026-04-28-batch-pilot-5.json --live
"""
import csv
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths & credentials (mirrors push-generated-images.py:30-41)
# ---------------------------------------------------------------------------
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
        sys.exit('Required: --batch=<name>  (e.g. --batch=pilot-5)')
    return live, batch, manifest, approval


def latest_manifest():
    matches = sorted(glob.glob(os.path.join(RPT_DIR, 'generated-img2img-*.csv')))
    if not matches:
        sys.exit('No generated-img2img-*.csv found.')
    return matches[-1]


def load_manifest(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') == 'OK':
                rows.append(row)
    return rows


def load_approval(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get('approvals', {})


def filter_approved(manifest_rows, approvals):
    out = []
    for row in manifest_rows:
        handle = row['Handle']
        try:
            pos = int(row['Image_Position'])
        except (ValueError, KeyError):
            continue
        a = approvals.get(handle) or {}
        key = 'gen2' if pos == 2 else ('gen3' if pos == 3 else None)
        if key and a.get(key) is True:
            out.append(row)
    return out


# ---------------------------------------------------------------------------
# Shopify API helpers (copy-adapted from push-generated-images.py:90-139)
# ---------------------------------------------------------------------------
def fetch_product(handle, cache):
    """Return (product_id, pos1_src) for handle, using cache."""
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
    """POST image to Shopify. Retries on socket/network errors. Raises on HTTP error."""
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


# ---------------------------------------------------------------------------
# Alt-text builder
# ---------------------------------------------------------------------------
CONTEXT_LABELS = {
    2: 'Office context A',
    3: 'Office context B',
}


def build_alt(title, position):
    label = CONTEXT_LABELS.get(int(position), 'Office context')
    return '{} - {} {}'.format(title or 'Product', label, ALT_TAG).strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    live, batch, manifest_arg, approval_arg = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'

    manifest_path = manifest_arg or latest_manifest()
    approval_path = approval_arg or os.path.join(RPT_DIR, 'approval-{}-batch-{}.json'.format(TODAY, batch))

    if not os.path.exists(approval_path):
        sys.exit('Approval JSON not found: {}\nRun render-image-review.py + serve-review.py first.'.format(approval_path))

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
        by_handle.setdefault(row['Handle'], []).append(row)

    print('{} approved images for {} products.\n'.format(len(rows), len(by_handle)))

    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RPT_DIR, exist_ok=True)

    cache = {}
    pushed = []
    aborted = []
    errors = []
    result_rows = []

    for i, (handle, img_rows) in enumerate(by_handle.items(), 1):
        print('[{}/{}] {}'.format(i, len(by_handle), handle))

        pid, live_pos1 = fetch_product(handle, cache)

        # Hard-fail on SKIP_NOT_FOUND (replaces log-and-continue at
        # scripts/push-generated-images.py:203-217 in the original).
        if not pid:
            print('  HARD-FAIL: product handle not found in Shopify.')
            print('  Reconcile {} before re-running this batch.'.format(handle))
            sys.exit(1)

        manifest_hero = img_rows[0].get('Source_Hero_URL') or ''
        if manifest_hero and live_pos1 and manifest_hero != live_pos1:
            print('  ABORT: hero changed between generation and push.')
            print('    manifest: {}'.format(manifest_hero[:100]))
            print('    live:     {}'.format(live_pos1[:100]))
            aborted.append(handle)
            for row in img_rows:
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   row['Image_Position'],
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL':  '',
                    'Alt_Text':         '',
                    'FAL_Source_URL':   row.get('FAL_URL', ''),
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
                    'Image_Position':   row['Image_Position'],
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL':  '',
                    'Alt_Text':         '',
                    'FAL_Source_URL':   row.get('FAL_URL', ''),
                    'Source_Hero_URL':  manifest_hero,
                    'Live_Pos1_URL':    '',
                    'Status':           'ABORT_NO_HERO',
                })
            continue

        for row in sorted(img_rows, key=lambda r: int(r['Image_Position'])):
            pos      = row['Image_Position']
            fal_url  = row['FAL_URL']
            title    = row.get('Title', '')
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
