"""
Clean the BBI logo via fal-ai/clarity-upscaler.

Reads data/logos/bbi-logo.png, upscales 2x with high resemblance
(no creative reinterpretation), writes data/logos/bbi-logo-cleaned.png.

Usage:
  python3 scripts/clean-bbi-logo.py            # dry run
  python3 scripts/clean-bbi-logo.py --live     # call fal.ai + save

Cost: ~$0.05-$0.07 via fal-ai/clarity-upscaler
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC      = os.path.join(ROOT, 'data', 'logos', 'bbi-logo-cleaned.png')
DEST     = os.path.join(ROOT, 'data', 'logos', 'bbi-logo-hires.png')

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f
               if '=' in line and not line.strip().startswith('#'))
FAL_KEY = env['FAL_KEY']

ENDPOINT = 'https://fal.run/fal-ai/clarity-upscaler'


def call_clarity(img_path, max_retries=3):
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    data_uri = 'data:image/png;base64,' + b64

    body = json.dumps({
        'image_url':           data_uri,
        'scale':               4,
        'creativity':          0.05,
        'resemblance':         0.95,
        'sharpness':           8,
        'num_inference_steps': 20,
    }).encode()
    headers = {
        'Authorization': 'Key ' + FAL_KEY,
        'Content-Type':  'application/json',
    }

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(ENDPOINT, data=body, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read().decode())
            if 'image' in result:
                return result['image']['url']
            if 'images' in result:
                return result['images'][0]['url']
            print('Unexpected response: {}'.format(str(result)[:200]))
            return None
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:200]
            if e.code in (400, 401, 403):
                print('fal.ai {} (will not retry): {}'.format(e.code, msg))
                return None
            wait = 2 ** (attempt + 1)
            print('fal.ai {} (attempt {}/{}), retrying in {}s'.format(
                e.code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** (attempt + 1)
            print('Error (attempt {}/{}): {}, retrying in {}s'.format(
                attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None


def download(url, dest_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(dest_path, 'wb') as f:
        f.write(data)


def main():
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode:   ' + mode)
    print('Source: {} ({} KB)'.format(SRC, os.path.getsize(SRC) // 1024))
    print('Dest:   ' + DEST)
    print('Engine: fal-ai/clarity-upscaler  scale=4  creativity=0.05  resemblance=0.95  sharpness=8')
    print('Cost:   ~$0.05-$0.07')

    if not live:
        print('\n[DRY RUN] Re-run with --live to clean the logo.')
        return

    print('\nCalling fal.ai...')
    url = call_clarity(SRC)
    if not url:
        sys.exit('FAILED - no URL returned')

    download(url, DEST)
    after_kb = os.path.getsize(DEST) // 1024
    print('OK  -> {} ({} KB)'.format(DEST, after_kb))
    print('Source URL: ' + url)


if __name__ == '__main__':
    main()
