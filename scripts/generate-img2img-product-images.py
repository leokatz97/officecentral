"""
Generate three AI images per product using fal-ai/flux-pro/kontext,
conditioned on the product's live position-1 hero image (img2img anchoring).

Images generated per product:
  pos 2 — Scene A: mix of Ontario institutional/community setting (attractive)
  pos 3 — Scene B: SMB private-sector professional office (attractive)
  pos 4 — White background: clean studio product shot

Pipeline:
  1. For each handle, GET /admin/api/2026-04/products.json?handle={h} to fetch
     the LIVE pos-1 image URL (do not trust stale exports).
  2. SKIP_NO_HERO if image_count == 0.
  3. Build per-product prompt; spec JSON used when present (only ~19 of ~540 —
     img2img conditioning carries the accuracy load, prompts add scene flavor).
  4. Call fal-ai/flux-pro/kontext three times (pos 2, 3, 4).
     Save to data/generated-img2img-images/{handle}-gen-{2,3,4}.jpg.
  5. Append to data/reports/generated-img2img-{date}.csv.

Pos-1 is NEVER regenerated. Only positions 2, 3, and 4.

Usage:
  python3 scripts/generate-img2img-product-images.py --pilot=5 --handles="h1,h2,h3,h4,h5"
  python3 scripts/generate-img2img-product-images.py --pilot=20
  python3 scripts/generate-img2img-product-images.py --input=data/reports/some-handle-list.json
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

# ---------------------------------------------------------------------------
# Paths & credentials (mirrors push-generated-images.py:30-41)
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

SHOPIFY_TOKEN = env['SHOPIFY_TOKEN']
SHOPIFY_STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
SHOPIFY_API   = 'https://{}/admin/api/2026-04'.format(SHOPIFY_STORE)
SHOPIFY_HEADERS = {'X-Shopify-Access-Token': SHOPIFY_TOKEN}

FAL_KEY      = env['FAL_KEY']
FAL_ENDPOINT = 'https://fal.run/fal-ai/flux-pro/kontext'
FAL_HEADERS  = {
    'Authorization': 'Key ' + FAL_KEY,
    'Content-Type':  'application/json',
}

IMG_DIR  = os.path.join(ROOT, 'data', 'generated-img2img-images')
RPT_DIR  = os.path.join(ROOT, 'data', 'reports')
SPEC_DIR = os.path.join(ROOT, 'data', 'specs')
LOG_DIR  = os.path.join(ROOT, 'data', 'logs')
TODAY    = datetime.now().strftime('%Y-%m-%d')
TS       = datetime.now().strftime('%Y%m%d-%H%M%S')

DEFAULT_INPUT = os.path.join(RPT_DIR, 'clean-products-handles.json')
MANIFEST_PATH = os.path.join(RPT_DIR, 'generated-img2img-{}.csv'.format(TODAY))

# ---------------------------------------------------------------------------
# Office context pairs by category (drives prompt variation)
# Scene A: aspirational Ontario institutional/community setting
# Scene B: aspirational SMB private-sector professional office
# ---------------------------------------------------------------------------
CONTEXT_PAIRS = {
    'seating': (
        'a bright, beautifully styled Ontario health team or community services office — '
        'light oak surfaces, lush green plants, large windows flooding the room with natural light, '
        'warm and welcoming atmosphere',
        'a polished private office at a professional services firm — '
        'rich walnut desk, warm ambient lighting, curated bookshelves, '
        'premium finishes, law firm or consulting studio aesthetic',
    ),
    'desk': (
        'a warmly lit, well-designed administrative office at a Canadian non-profit or family health team — '
        'clean surfaces, fresh plants, natural light, calm and professional',
        'a sleek private office at a law firm or financial services company — '
        'dark wood tones, statement pendant lighting, premium leather accessories, polished and refined',
    ),
    'storage': (
        'a clean, well-organised administrative office at a small Ontario hospital or municipal office — '
        'neutral warm tones, natural light from large windows, tidy and professional',
        'a stylish professional office with curated storage and upscale finishes — '
        'accounting firm or insurance brokerage, warm lighting, sophisticated and put-together',
    ),
    'conference': (
        'a bright, modern boardroom at a community health centre or non-profit — '
        'large windows, natural light, clean contemporary lines, welcoming and collaborative',
        'a polished executive boardroom at a professional services firm — '
        'warm wood table, leather chairs, city skyline view, sophisticated and impressive',
    ),
    'healthcare': (
        'a calm, welcoming waiting area at a beautifully designed family health team or community clinic — '
        'soft neutral tones, natural light, green plants, warm and reassuring',
        'a premium medical or wellness clinic with contemporary finishes — '
        'clean white walls, warm wood accents, tasteful art, upscale and professional',
    ),
    'education': (
        'a bright, modern school or university administrative office — '
        'clean surfaces, natural light, plants, organised and inviting',
        'a contemporary corporate training room or professional development space — '
        'premium furnishings, warm lighting, polished and motivating',
    ),
    'lounge': (
        'a beautifully designed reception or lounge area at a Canadian non-profit or health centre — '
        'plants, warm natural light, comfortable and inviting, tasteful modern decor',
        'a stylish corporate lobby or breakout lounge at a professional services firm — '
        'premium upholstery, ambient lighting, curated art, sophisticated and welcoming',
    ),
    'default': (
        'a bright, beautifully styled Ontario office with abundant natural light, lush plants, '
        'and warm neutral tones — welcoming, calm, and professional',
        'a polished private office at a professional services firm — '
        'warm wood tones, curated decor, premium finishes, refined and impressive',
    ),
}

CATEGORY_KEYWORDS = [
    ('chair',         'seating'),
    ('stool',         'seating'),
    ('seating',       'seating'),
    ('sofa',          'lounge'),
    ('lounge',        'lounge'),
    ('reception',     'lounge'),
    ('bench',         'desk'),
    ('workstation',   'desk'),
    ('desk',          'desk'),
    ('table',         'conference'),
    ('conference',    'conference'),
    ('boardroom',     'conference'),
    ('cabinet',       'storage'),
    ('credenza',      'storage'),
    ('storage',       'storage'),
    ('filing',        'storage'),
    ('file',          'storage'),
    ('shelving',      'storage'),
    ('shelf',         'storage'),
    ('healthcare',    'healthcare'),
    ('medical',       'healthcare'),
    ('patient',       'healthcare'),
    ('school',        'education'),
    ('classroom',     'education'),
    ('lectern',       'education'),
]


def categorize(title):
    t = (title or '').lower()
    for keyword, category in CATEGORY_KEYWORDS:
        if keyword in t:
            return category
    return 'default'


# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
def parse_args():
    pilot    = None
    handles  = None
    input_p  = DEFAULT_INPUT
    for arg in sys.argv[1:]:
        if arg.startswith('--pilot='):
            pilot = int(arg.split('=', 1)[1])
        elif arg.startswith('--handles='):
            handles = [h.strip() for h in arg.split('=', 1)[1].split(',') if h.strip()]
        elif arg.startswith('--input='):
            input_p = arg.split('=', 1)[1]
    return pilot, handles, input_p


def load_handle_list(input_path, explicit_handles, pilot_n):
    """Resolve to a list of {handle, title} dicts."""
    if explicit_handles:
        rows = [{'handle': h, 'title': ''} for h in explicit_handles]
        if pilot_n and len(rows) > pilot_n:
            rows = rows[:pilot_n]
        return rows

    if not os.path.exists(input_path):
        sys.exit('Input not found: ' + input_path)

    with open(input_path, encoding='utf-8') as f:
        data = json.load(f)

    rows = [{'handle': r['handle'], 'title': r.get('title', '')} for r in data]
    if pilot_n:
        rows = rows[:pilot_n]
    return rows


# ---------------------------------------------------------------------------
# Shopify: fetch live pos-1 image
# ---------------------------------------------------------------------------
def fetch_product(handle):
    """Return (product_id, title, pos1_src) or (None, None, None)."""
    encoded = urllib.parse.quote(handle)
    url = '{}/products.json?handle={}&fields=id,title,images&limit=1'.format(SHOPIFY_API, encoded)
    req = urllib.request.Request(url, headers=SHOPIFY_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print('  Shopify {} error: {}'.format(e.code, e.read().decode()[:120]))
        return None, None, None
    products = data.get('products', [])
    if not products:
        return None, None, None
    p = products[0]
    images = p.get('images') or []
    if not images:
        return str(p['id']), p.get('title', ''), None
    pos1 = sorted(images, key=lambda i: i.get('position') or 999)[0]
    return str(p['id']), p.get('title', ''), pos1.get('src')


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------
def load_spec(handle):
    path = os.path.join(SPEC_DIR, handle + '.json')
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def spec_phrase(spec):
    if not spec:
        return ''
    s = spec.get('specs') or {}
    bits = []
    if s.get('manufacturer'):
        bits.append(s['manufacturer'])
    finishes = s.get('finishes_available') or []
    if finishes:
        bits.append(finishes[0])
    materials = s.get('materials') or ''
    if materials and len(materials) < 60:
        bits.append(materials)
    return ' '.join(bits).strip()


def build_prompt(title, context_phrase, spec):
    qualifier = spec_phrase(spec)
    base = title or 'product'
    desc = '{} {}'.format(qualifier, base).strip() if qualifier else base
    return (
        'The exact {desc} from the reference image, placed in {context}. '
        'Match the reference exactly: same form, colour, material, hardware, and proportions. '
        'Wide shot, mid-distance, eye-level, photorealistic. '
        'No people. No text overlays. No watermarks.'
    ).format(desc=desc[:120], context=context_phrase)


def build_prompt_white_bg(title, spec):
    qualifier = spec_phrase(spec)
    base = title or 'product'
    desc = '{} {}'.format(qualifier, base).strip() if qualifier else base
    return (
        'The exact {desc} from the reference image on a pure white background. '
        'Professional studio product photography, soft even lighting, subtle drop shadow, '
        'sharp focus on every detail. '
        'Match the reference exactly: same form, colour, material, hardware, and proportions. '
        'No background objects. No people. No text overlays. No watermarks.'
    ).format(desc=desc[:120])


# ---------------------------------------------------------------------------
# fal.ai call
# ---------------------------------------------------------------------------
def call_fal(prompt, image_url, max_retries=3):
    body = json.dumps({
        'prompt':              prompt,
        'image_url':           image_url,
        'guidance_scale':      3.5,
        'num_inference_steps': 28,
        'image_size':          'landscape_4_3',
        'num_images':          1,
        'safety_tolerance':    '2',
    }).encode()
    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(FAL_ENDPOINT, data=body, headers=FAL_HEADERS, method='POST')
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                imgs = data.get('images') or []
                if not imgs:
                    return None, 'no images returned'
                time.sleep(0.5)
                return imgs[0]['url'], None
        except urllib.error.HTTPError as e:
            code = e.code
            msg  = e.read().decode()[:200]
            if code in (400, 401, 403):
                return None, 'http {}: {}'.format(code, msg[:100])
            last_err = 'http {}: {}'.format(code, msg[:80])
            wait = 2 ** (attempt + 1)
            print('    fal.ai {} (attempt {}/{}), retrying in {}s'.format(code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            last_err = str(e)
            wait = 2 ** (attempt + 1)
            print('    fal.ai network error (attempt {}/{}): {} — retrying in {}s'.format(attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None, last_err or 'unknown error'


def download(url, dest_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'bbi-img2img/1.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(dest_path, 'wb') as f:
            f.write(resp.read())


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
MANIFEST_FIELDS = [
    'Handle', 'Title', 'Image_Position', 'FAL_URL', 'Local_Path',
    'Source_Hero_URL', 'Prompt', 'Status', 'Timestamp',
]


def append_manifest(row):
    new_file = not os.path.exists(MANIFEST_PATH)
    with open(MANIFEST_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    pilot, explicit_handles, input_path = parse_args()

    rows = load_handle_list(input_path, explicit_handles, pilot)
    if not rows:
        sys.exit('No handles to process.')

    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(RPT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    print('Mode:     img2img via fal-ai/flux-pro/kontext')
    print('Input:    {} ({} handle{})'.format(
        'CLI handles' if explicit_handles else input_path,
        len(rows), '' if len(rows) == 1 else 's',
    ))
    print('Manifest: ' + MANIFEST_PATH)
    print('Outputs:  ' + IMG_DIR)
    print('Estimated cost: ~${:.2f} ({} products x 3 images x ~$0.04)'.format(
        len(rows) * 3 * 0.04, len(rows),
    ))
    print()

    ok = 0
    skipped = 0
    failed = 0

    for i, row in enumerate(rows, 1):
        handle = row['handle']
        print('[{}/{}] {}'.format(i, len(rows), handle))

        product_id, live_title, pos1_src = fetch_product(handle)
        if product_id is None:
            print('  SKIP_NOT_FOUND')
            append_manifest({
                'Handle': handle, 'Title': row.get('title', ''),
                'Image_Position': '', 'FAL_URL': '', 'Local_Path': '',
                'Source_Hero_URL': '', 'Prompt': '',
                'Status': 'SKIP_NOT_FOUND', 'Timestamp': TS,
            })
            skipped += 1
            continue

        title = live_title or row.get('title', '')

        if not pos1_src:
            print('  SKIP_NO_HERO ({})'.format(title[:60]))
            append_manifest({
                'Handle': handle, 'Title': title,
                'Image_Position': '', 'FAL_URL': '', 'Local_Path': '',
                'Source_Hero_URL': '', 'Prompt': '',
                'Status': 'SKIP_NO_HERO', 'Timestamp': TS,
            })
            skipped += 1
            continue

        category = categorize(title)
        ctx_a, ctx_b = CONTEXT_PAIRS.get(category, CONTEXT_PAIRS['default'])
        spec = load_spec(handle)

        jobs = [
            (2, build_prompt(title, ctx_a, spec), 'scene-A'),
            (3, build_prompt(title, ctx_b, spec), 'scene-B'),
            (4, build_prompt_white_bg(title, spec), 'white-bg'),
        ]

        for position, prompt, label in jobs:
            local_path = os.path.join(IMG_DIR, '{}-gen-{}.jpg'.format(handle, position))
            print('  pos {} [{}]: {}'.format(position, label, prompt[:70]))

            fal_url, err = call_fal(prompt, pos1_src)
            if not fal_url:
                print('    FAIL: {}'.format(err))
                append_manifest({
                    'Handle': handle, 'Title': title,
                    'Image_Position': position, 'FAL_URL': '', 'Local_Path': '',
                    'Source_Hero_URL': pos1_src, 'Prompt': prompt,
                    'Status': 'FAIL_GENERATION', 'Timestamp': TS,
                })
                failed += 1
                continue

            try:
                download(fal_url, local_path)
            except Exception as e:
                print('    DOWNLOAD-FAIL: {}'.format(e))
                append_manifest({
                    'Handle': handle, 'Title': title,
                    'Image_Position': position, 'FAL_URL': fal_url, 'Local_Path': '',
                    'Source_Hero_URL': pos1_src, 'Prompt': prompt,
                    'Status': 'FAIL_DOWNLOAD', 'Timestamp': TS,
                })
                failed += 1
                continue

            append_manifest({
                'Handle': handle, 'Title': title,
                'Image_Position': position, 'FAL_URL': fal_url, 'Local_Path': local_path,
                'Source_Hero_URL': pos1_src, 'Prompt': prompt,
                'Status': 'OK', 'Timestamp': TS,
            })
            ok += 1

    print()
    print('=' * 60)
    print('Generated: {}'.format(ok))
    print('Skipped:   {}'.format(skipped))
    print('Failed:    {}'.format(failed))
    print('Manifest:  {}'.format(MANIFEST_PATH))
    print('=' * 60)


if __name__ == '__main__':
    main()
