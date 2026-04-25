"""
Generate 2 AI product images per 1-image product using fal.ai flux/schnell.

Reads data/exports/products-export-2026-04-21.csv, finds products with exactly
1 image, and generates:
  - gen-2: clean studio shot on white background
  - gen-3: product in a modern Canadian office environment

Images are downloaded to data/generated-images/{handle}-gen-{2,3}.jpg.
A manifest CSV is written to data/reports/generated-images-YYYY-MM-DD.csv.
Resume-safe: skips handles whose local files already exist.

Usage:
  python3 scripts/generate-product-images.py              # dry run
  python3 scripts/generate-product-images.py --live       # call fal.ai + download
  python3 scripts/generate-product-images.py --limit=5 --live  # smoke test
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
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

FAL_KEY = env['FAL_KEY']

CSV_IN  = os.path.join(ROOT, 'data', 'exports', 'products-export-2026-04-21.csv')
IMG_DIR = os.path.join(ROOT, 'data', 'generated-images')
RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
TODAY   = datetime.now().strftime('%Y-%m-%d')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')

FAL_ENDPOINT = 'https://fal.run/fal-ai/flux/schnell'

# ---------------------------------------------------------------------------
# Category -> furniture label (for prompt context)
# ---------------------------------------------------------------------------
CATEGORY_LABELS = [
    (['chair', 'armchair', 'seating'],          'office ergonomic chair'),
    (['stool'],                                  'counter stool'),
    (['reception'],                              'reception desk'),
    (['workstation', 'cubicle', 'panel'],        'office workstation'),
    (['desk'],                                   'office desk'),
    (['file cabinet', 'file box', 'filing'],     'filing cabinet'),
    (['storage cabinet', 'locker'],              'storage cabinet'),
    (['bookcase', 'shelv'],                      'bookcase'),
    (['keyboard', 'monitor arm'],                'desk accessory'),
    (['lamp'],                                   'desk lamp'),
    (['cart'],                                   'mobile office cart'),
    (['whiteboard', 'dry-erase', 'board'],       'whiteboard'),
    (['table'],                                  'conference table'),
]


def furniture_label(product_category, product_type):
    source = product_category.strip()
    if '>' in source:
        source = source.rsplit('>', 1)[-1].strip()
    if not source:
        source = product_type.strip()
    slug = source.lower()
    for keywords, label in CATEGORY_LABELS:
        if any(k in slug for k in keywords):
            return label
    return 'office furniture'


def build_prompts(title, product_category, product_type):
    label       = furniture_label(product_category, product_type)
    short_title = title[:80]
    gen2 = (
        "Professional product photography of {}, a {}, "
        "on a clean white studio background. Crisp even lighting, sharp detail, "
        "slight drop shadow, commercial catalogue style. No people, no text overlays."
    ).format(short_title, label)
    gen3 = (
        "{}, a {}, photographed in a bright modern Canadian "
        "office environment. Natural window light, contemporary neutral decor, "
        "professional workspace setting. Realistic lifestyle product photo. "
        "No people visible, no text overlays."
    ).format(short_title, label)
    gen4 = (
        "Close-up detail shot of {}, a {}, highlighting material texture, "
        "craftsmanship and finish quality. Shallow depth of field, soft studio "
        "lighting, muted warm background. Editorial product photography, "
        "premium feel. No people, no text overlays."
    ).format(short_title, label)
    return gen2, gen3, gen4


# ---------------------------------------------------------------------------
# fal.ai API
# ---------------------------------------------------------------------------
def call_fal(prompt, max_retries=3):
    body = json.dumps({
        'prompt':               prompt,
        'image_size':           'landscape_4_3',
        'num_inference_steps':  4,
        'num_images':           1,
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
            print('    fal.ai {} (attempt {}/{}), retrying in {}s'.format(code, attempt+1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** (attempt + 1)
            print('    fal.ai error (attempt {}/{}): {}, retrying in {}s'.format(attempt+1, max_retries, e, wait))
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
# CSV reader
# ---------------------------------------------------------------------------
def load_one_image_products(csv_path):
    by_handle = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            handle = row.get('Handle', '').strip()
            if not handle:
                continue
            img = row.get('Image Src', '').strip()
            if handle not in by_handle:
                by_handle[handle] = {
                    'title':            row.get('Title', '').strip(),
                    'product_category': row.get('Product Category', '').strip(),
                    'product_type':     row.get('Type', '').strip(),
                    'image_srcs':       set(),
                }
            if img:
                by_handle[handle]['image_srcs'].add(img)

    result = []
    for handle, meta in by_handle.items():
        if len(meta['image_srcs']) == 1:
            result.append({
                'handle':           handle,
                'title':            meta['title'],
                'product_category': meta['product_category'],
                'product_type':     meta['product_type'],
            })
    return result


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
    print('Source: ' + CSV_IN)

    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(RPT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    print('Loading products...')
    products = load_one_image_products(CSV_IN)
    print('Found {} products with exactly 1 image.'.format(len(products)))

    if limit:
        products = products[:limit]
        print('Limiting to first {} products ({} images).'.format(limit, limit * 3))

    # Cost guard
    pending = 0
    for p in products:
        for pos in (2, 3, 4):
            path = os.path.join(IMG_DIR, '{}-gen-{}.jpg'.format(p['handle'], pos))
            if not os.path.exists(path):
                pending += 1

    cost_low  = pending * 0.003
    cost_high = pending * 0.006
    print('\nPending images: {}'.format(pending))
    print('Estimated cost: ${:.2f}-${:.2f}'.format(cost_low, cost_high))

    if live and cost_high > 5.00:
        ans = input('\nEstimated cost exceeds $5. Type YES to continue: ')
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
        cat    = p['product_category']
        ptype  = p['product_type']
        prompt_gen2, prompt_gen3, prompt_gen4 = build_prompts(title, cat, ptype)

        print('[{}/{}] {}'.format(i, total, handle))

        for pos, alt_suffix, prompt in [
            (2, 'Office Setting',   prompt_gen2),
            (3, 'Workspace View',   prompt_gen3),
            (4, 'Detail Close-Up',  prompt_gen4),
        ]:
            alt_text   = '{} - {}'.format(title, alt_suffix)
            local_path = os.path.join(IMG_DIR, '{}-gen-{}.jpg'.format(handle, pos))

            if os.path.exists(local_path):
                print('  gen-{}: SKIP (already exists)'.format(pos))
                skipped += 1
                manifest_rows.append({
                    'Handle': handle, 'Title': title, 'Product_Type': cat or ptype,
                    'Image_Position': pos, 'FAL_URL': '', 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'SKIPPED_EXISTS',
                })
                continue

            if not live:
                print('  gen-{}: DRY RUN - would generate {}-gen-{}.jpg'.format(pos, handle, pos))
                manifest_rows.append({
                    'Handle': handle, 'Title': title, 'Product_Type': cat or ptype,
                    'Image_Position': pos, 'FAL_URL': '', 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'DRY_RUN',
                })
                continue

            fal_url = call_fal(prompt)
            if not fal_url:
                print('  gen-{}: ERROR - fal.ai returned no URL'.format(pos))
                errors.append({'handle': handle, 'pos': pos, 'stage': 'fal'})
                manifest_rows.append({
                    'Handle': handle, 'Title': title, 'Product_Type': cat or ptype,
                    'Image_Position': pos, 'FAL_URL': '', 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'ERROR',
                })
                continue

            ok = download_image(fal_url, local_path)
            if not ok:
                print('  gen-{}: ERROR - download failed'.format(pos))
                errors.append({'handle': handle, 'pos': pos, 'stage': 'download', 'fal_url': fal_url})
                manifest_rows.append({
                    'Handle': handle, 'Title': title, 'Product_Type': cat or ptype,
                    'Image_Position': pos, 'FAL_URL': fal_url, 'Local_Path': local_path,
                    'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'ERROR',
                })
                continue

            size_kb = os.path.getsize(local_path) // 1024
            print('  gen-{}: OK ({} KB) -> {}-gen-{}.jpg'.format(pos, size_kb, handle, pos))
            generated += 1
            manifest_rows.append({
                'Handle': handle, 'Title': title, 'Product_Type': cat or ptype,
                'Image_Position': pos, 'FAL_URL': fal_url, 'Local_Path': local_path,
                'Alt_Text': alt_text, 'Prompt': prompt, 'Status': 'OK',
            })

    # Write manifest CSV
    manifest_path = os.path.join(RPT_DIR, 'generated-images-{}.csv'.format(TODAY))
    fieldnames = ['Handle', 'Title', 'Product_Type', 'Image_Position',
                  'FAL_URL', 'Local_Path', 'Alt_Text', 'Prompt', 'Status']
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    # Write audit log
    log_path = os.path.join(LOG_DIR, 'image-generation-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':               mode,
            'total_products':     total,
            'generated':          generated,
            'skipped_existing':   skipped,
            'errors':             len(errors),
            'error_details':      errors,
            'cost_estimate_low':  round(generated * 0.003, 4),
            'cost_estimate_high': round(generated * 0.006, 4),
        }, f, indent=2)

    print()
    print('Summary: ' + mode)
    print('  Products processed:  {}'.format(total))
    print('  Images generated:    {}'.format(generated))
    print('  Skipped (existing):  {}'.format(skipped))
    print('  Errors:              {}'.format(len(errors)))
    if generated:
        print('  Actual cost (est):   ${:.2f}-${:.2f}'.format(generated * 0.003, generated * 0.006))
    print('  Manifest CSV:        ' + manifest_path)
    print('  Images folder:       ' + IMG_DIR)
    print('  Audit log:           ' + log_path)

    if not live:
        print('\n[DRY RUN] No API calls made. Re-run with --live to generate images.')


if __name__ == '__main__':
    main()
