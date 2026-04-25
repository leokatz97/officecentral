"""
Generate 3 AI product images per "clean" product (no flags, already multi-image).

Source: data/reports/clean-products-handles.json (216 handles, extracted from
        previews/Product-enrichment.html — pub=true, fl=[])

Generates:
  - gen-2: clean studio shot on white background
  - gen-3: product in a bright modern Canadian office environment
  - gen-4: close-up detail / texture shot

Images are downloaded to data/generated-clean-images/{handle}-gen-{2,3,4}.jpg.
Manifest CSV -> data/reports/generated-clean-images-YYYY-MM-DD.csv
Audit log    -> data/logs/clean-image-generation-YYYYMMDD-HHMMSS.json

Resume-safe: skips handles whose local files already exist.

Usage:
  python3 scripts/generate-clean-product-images.py              # dry run
  python3 scripts/generate-clean-product-images.py --live       # call fal.ai + download
  python3 scripts/generate-clean-product-images.py --limit=3 --live  # smoke test
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths & credentials
# ---------------------------------------------------------------------------
def _find_root():
    # Walk up from script location to find the directory containing .env
    path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        path = os.path.dirname(path)
        if os.path.exists(os.path.join(path, '.env')):
            return path
    raise FileNotFoundError('.env not found in any parent directory')

ROOT = _find_root()

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

FAL_KEY = env['FAL_KEY']

HANDLES_JSON = os.path.join(ROOT, 'data', 'reports', 'clean-products-handles.json')
IMG_DIR      = os.path.join(ROOT, 'data', 'generated-clean-images')
RPT_DIR      = os.path.join(ROOT, 'data', 'reports')
LOG_DIR      = os.path.join(ROOT, 'data', 'logs')
TODAY        = datetime.now().strftime('%Y-%m-%d')
TS           = datetime.now().strftime('%Y%m%d-%H%M%S')

FAL_ENDPOINT  = 'https://fal.run/fal-ai/flux/schnell'
COST_GUARD    = 2.00
COST_PER_LOW  = 0.003
COST_PER_HIGH = 0.004


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------
def build_prompts(title):
    short = title[:80]
    gen2 = (
        "Professional product photography of {} on a clean white studio background, "
        "crisp even lighting, slight drop shadow, commercial catalogue style. "
        "No people, no text overlays."
    ).format(short)
    gen3 = (
        "{} in a bright modern Canadian open-plan office environment, "
        "warm natural window light, contemporary neutral decor. "
        "No people, no text overlays."
    ).format(short)
    gen4 = (
        "Close-up detail shot of {}, shallow depth of field, editorial style, "
        "studio lighting, emphasis on material texture and craftsmanship. "
        "No people, no text overlays."
    ).format(short)
    return gen2, gen3, gen4


# ---------------------------------------------------------------------------
# fal.ai API
# ---------------------------------------------------------------------------
def call_fal(prompt, max_retries=3):
    body = json.dumps({
        'prompt':              prompt,
        'image_size':          'landscape_4_3',
        'num_inference_steps': 4,
        'num_images':          1,
    }).encode()
    headers = {
        'Authorization': 'Key ' + FAL_KEY,
        'Content-Type':  'application/json',
    }
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(FAL_ENDPOINT, data=body, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
                url  = data['images'][0]['url']
                time.sleep(1)
                return url
        except urllib.error.HTTPError as e:
            code = e.code
            msg  = e.read().decode()[:200]
            if code in (400, 401, 403):
                print('    fal.ai {} error (will not retry): {}'.format(code, msg[:100]))
                return None
            wait = 2 ** (attempt + 1)
            print('    fal.ai {} (attempt {}/{}), retrying in {}s'.format(code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** (attempt + 1)
            print('    fal.ai error (attempt {}/{}): {}, retrying in {}s'.format(attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None


# ---------------------------------------------------------------------------
# Image download
# ---------------------------------------------------------------------------
def download_image(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print('    Download error: {}'.format(e))
        return False


# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
def parse_args():
    live  = '--live' in sys.argv
    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
    return live, limit


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    live, limit = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)
    print('Source: ' + HANDLES_JSON)

    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(RPT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    with open(HANDLES_JSON) as f:
        products = json.load(f)

    print('Loaded {} clean products.'.format(len(products)))

    if limit:
        products = products[:limit]
        print('Limiting to first {} products ({} images).'.format(limit, limit * 3))

    # Cost guard: count pending images
    pending = 0
    for p in products:
        for pos in (2, 3, 4):
            path = os.path.join(IMG_DIR, '{}-gen-{}.jpg'.format(p['handle'], pos))
            if not os.path.exists(path):
                pending += 1

    cost_low  = pending * COST_PER_LOW
    cost_high = pending * COST_PER_HIGH
    print('\nPending images: {}'.format(pending))
    print('Estimated cost: ${:.2f}-${:.2f}'.format(cost_low, cost_high))

    if live and cost_high > COST_GUARD:
        ans = input('\nEstimated cost exceeds ${}. Type YES to continue: '.format(COST_GUARD))
        if ans.strip().upper() != 'YES':
            sys.exit('Aborted.')

    print()

    manifest_rows = []
    generated     = 0
    skipped       = 0
    errors        = []
    total         = len(products)

    for i, p in enumerate(products, 1):
        handle = p['handle']
        title  = p['title']
        prompt_gen2, prompt_gen3, prompt_gen4 = build_prompts(title)

        print('[{}/{}] {}'.format(i, total, handle))

        for pos, alt_suffix, prompt in [
            (2, 'Studio White',    prompt_gen2),
            (3, 'Office Setting',  prompt_gen3),
            (4, 'Detail Close-Up', prompt_gen4),
        ]:
            alt_text   = '{} - {}'.format(title, alt_suffix)
            local_path = os.path.join(IMG_DIR, '{}-gen-{}.jpg'.format(handle, pos))

            if os.path.exists(local_path):
                print('  gen-{}: SKIP (already exists)'.format(pos))
                skipped += 1
                manifest_rows.append({
                    'Handle': handle, 'Title': title,
                    'Image_Position': pos, 'Filename': os.path.basename(local_path),
                    'FAL_URL': '', 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'SKIPPED_EXISTS',
                })
                continue

            if not live:
                print('  gen-{}: DRY RUN - would generate {}-gen-{}.jpg'.format(pos, handle, pos))
                manifest_rows.append({
                    'Handle': handle, 'Title': title,
                    'Image_Position': pos, 'Filename': os.path.basename(local_path),
                    'FAL_URL': '', 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'DRY_RUN',
                })
                continue

            fal_url = call_fal(prompt)
            if not fal_url:
                print('  gen-{}: ERROR - fal.ai returned no URL'.format(pos))
                errors.append({'handle': handle, 'pos': pos, 'stage': 'fal'})
                manifest_rows.append({
                    'Handle': handle, 'Title': title,
                    'Image_Position': pos, 'Filename': os.path.basename(local_path),
                    'FAL_URL': '', 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'ERROR',
                })
                continue

            ok = download_image(fal_url, local_path)
            if not ok:
                print('  gen-{}: ERROR - download failed'.format(pos))
                errors.append({'handle': handle, 'pos': pos, 'stage': 'download', 'fal_url': fal_url})
                manifest_rows.append({
                    'Handle': handle, 'Title': title,
                    'Image_Position': pos, 'Filename': os.path.basename(local_path),
                    'FAL_URL': fal_url, 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'ERROR',
                })
                continue

            size_kb = os.path.getsize(local_path) // 1024
            print('  gen-{}: OK ({} KB) -> {}-gen-{}.jpg'.format(pos, size_kb, handle, pos))
            generated += 1
            manifest_rows.append({
                'Handle': handle, 'Title': title,
                'Image_Position': pos, 'Filename': os.path.basename(local_path),
                'FAL_URL': fal_url, 'Local_Path': local_path,
                'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'GENERATED',
            })

    # Write manifest CSV
    manifest_path = os.path.join(RPT_DIR, 'generated-clean-images-{}.csv'.format(TODAY))
    fieldnames = ['Handle', 'Title', 'Image_Position', 'Filename', 'FAL_URL', 'Local_Path', 'Alt_Text', 'Prompt', 'Status']
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    # Write audit log
    log_path = os.path.join(LOG_DIR, 'clean-image-generation-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':               mode,
            'total_products':     total,
            'generated':          generated,
            'skipped_existing':   skipped,
            'errors':             len(errors),
            'error_details':      errors,
            'cost_estimate_low':  round(generated * COST_PER_LOW, 4),
            'cost_estimate_high': round(generated * COST_PER_HIGH, 4),
        }, f, indent=2)

    print()
    print('Summary: ' + mode)
    print('  Products processed:  {}'.format(total))
    print('  Images generated:    {}'.format(generated))
    print('  Skipped (existing):  {}'.format(skipped))
    print('  Errors:              {}'.format(len(errors)))
    if generated:
        print('  Actual cost (est):   ${:.2f}-${:.2f}'.format(
            generated * COST_PER_LOW, generated * COST_PER_HIGH))
    print('  Manifest CSV:        ' + manifest_path)
    print('  Images folder:       ' + IMG_DIR)
    print('  Audit log:           ' + log_path)

    if not live:
        print('\n[DRY RUN] No API calls made. Re-run with --live to generate images.')


if __name__ == '__main__':
    main()
