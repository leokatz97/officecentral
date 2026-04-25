"""
Sharpen all generated page images using fal-ai/clarity-upscaler.

Reads every .jpg from data/page-images/, runs it through the clarity-upscaler
(scale=2, high sharpness, high resemblance), and overwrites the file in place.

Usage:
  python3 scripts/sharpen-page-images.py              # dry run
  python3 scripts/sharpen-page-images.py --live       # sharpen all images
  python3 scripts/sharpen-page-images.py --limit=3 --live  # smoke test

Cost: ~$0.05–$0.07 per image via fal-ai/clarity-upscaler
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, 'data', 'page-images')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.strip().startswith('#'))
FAL_KEY = env['FAL_KEY']

FAL_ENDPOINT  = 'https://fal.run/fal-ai/clarity-upscaler'
COST_LOW      = 0.05
COST_HIGH     = 0.07


def find_images():
    paths = []
    for dirpath, _, filenames in os.walk(IMG_DIR):
        for fn in sorted(filenames):
            if fn.lower().endswith('.jpg'):
                paths.append(os.path.join(dirpath, fn))
    return sorted(paths)


def call_clarity(img_path, max_retries=3):
    with open(img_path, 'rb') as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode()
    data_uri = 'data:image/jpeg;base64,' + b64

    body = json.dumps({
        'image_url':            data_uri,
        'scale':                2,
        'creativity':           0.05,
        'resemblance':          0.95,
        'sharpness':            8,
        'num_inference_steps':  20,
    }).encode()
    headers = {
        'Authorization': 'Key ' + FAL_KEY,
        'Content-Type':  'application/json',
    }

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(FAL_ENDPOINT, data=body, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode())
            # clarity-upscaler returns {"image": {"url": "..."}} or {"images": [{"url": "..."}]}
            if 'image' in result:
                return result['image']['url']
            elif 'images' in result:
                return result['images'][0]['url']
            else:
                print('    Unexpected response: {}'.format(str(result)[:200]))
                return None
        except urllib.error.HTTPError as e:
            code = e.code
            msg  = e.read().decode()[:200]
            if code in (400, 401, 403):
                print('    fal.ai {} (will not retry): {}'.format(code, msg[:120]))
                return None
            wait = 2 ** (attempt + 1)
            print('    fal.ai {} (attempt {}/{}), retrying in {}s'.format(code, attempt+1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** (attempt + 1)
            print('    Error (attempt {}/{}): {}, retrying in {}s'.format(attempt+1, max_retries, e, wait))
            time.sleep(wait)
    return None


def download_image(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(dest_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print('    Download error: {}'.format(e))
        return False


def parse_args():
    live  = '--live' in sys.argv
    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
    return live, limit


def main():
    live, limit = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)

    images = find_images()
    if limit:
        images = images[:limit]
        print('Limiting to first {} image(s).'.format(limit))

    count = len(images)
    print('Images: {} | Est. cost: ${:.2f}–${:.2f}'.format(
        count, count * COST_LOW, count * COST_HIGH))

    if live and count * COST_HIGH > 2.00:
        ans = input('\nEstimated cost exceeds $2. Type YES to continue: ')
        if ans.strip().upper() != 'YES':
            sys.exit('Aborted.')

    print()
    os.makedirs(LOG_DIR, exist_ok=True)

    sharpened = 0
    errors    = []
    log_rows  = []

    for i, img_path in enumerate(images, 1):
        rel = os.path.relpath(img_path, ROOT)
        print('[{}/{}] {}'.format(i, count, rel))

        if not live:
            print('  DRY RUN')
            continue

        url = call_clarity(img_path)
        if not url:
            print('  ERROR - no URL returned')
            errors.append(rel)
            log_rows.append({'path': rel, 'status': 'ERROR'})
            continue

        before_kb = os.path.getsize(img_path) // 1024
        ok = download_image(url, img_path)
        if ok:
            after_kb = os.path.getsize(img_path) // 1024
            print('  OK  {} KB -> {} KB'.format(before_kb, after_kb))
            sharpened += 1
            log_rows.append({'path': rel, 'status': 'OK', 'before_kb': before_kb, 'after_kb': after_kb, 'url': url})
        else:
            print('  ERROR - download failed')
            errors.append(rel)
            log_rows.append({'path': rel, 'status': 'DOWNLOAD_FAIL', 'url': url})

        time.sleep(0.5)

    print()
    print('Summary: ' + mode)
    print('  Images sharpened: {}'.format(sharpened))
    print('  Errors:           {}'.format(len(errors)))
    if sharpened:
        print('  Actual cost (est): ${:.2f}–${:.2f}'.format(
            sharpened * COST_LOW, sharpened * COST_HIGH))

    if live:
        log_path = os.path.join(LOG_DIR, 'sharpen-page-images-{}.json'.format(TS))
        with open(log_path, 'w') as f:
            json.dump({'mode': mode, 'sharpened': sharpened,
                       'errors': errors, 'images': log_rows}, f, indent=2)
        print('  Log: ' + log_path)

    if not live:
        print('\n[DRY RUN] No API calls made. Re-run with --live to sharpen images.')
    if errors:
        print('\nFailed images:')
        for e in errors:
            print('  ' + e)


if __name__ == '__main__':
    main()
