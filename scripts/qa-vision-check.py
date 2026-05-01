"""
Score every img2img generation by sending a side-by-side composite (source hero
+ AI image) to fal-ai/any-llm/vision (default model: google/gemini-flash-1.5)
and parsing a JSON match score.

For each row in data/reports/generated-img2img-<batch>.csv with status=OK:
  1. Build composite [reference | generated] → /tmp/qa-composites/...
  2. Ask Gemini: 'Does the right side depict the same product as the left side?'
     Reply must be JSON: {score: 0-10, match: bool, reason: string}.
  3. If score < 7 and --retry, regenerate via fal-ai/flux-pro/kontext (max 2x).
  4. Final status: OK / RETRY1 / RETRY2 / FLAG_HUMAN.

Outputs:
  data/reports/qa-vision-<batch>.csv  (per-batch, lowercase columns)

Cost (~$0.001 per check via Gemini Flash; ~$0.04 per regen):
  ~15 images: ~$0.02 + retries

Usage:
  python3 scripts/qa-vision-check.py --batch=batch-pilot
  python3 scripts/qa-vision-check.py --batch=batch-pilot --phase=phase1
  python3 scripts/qa-vision-check.py --batch=batch-pilot --no-retry
"""
import base64
import csv
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Paths & credentials
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

FAL_KEY = env.get('FAL_KEY') or os.environ.get('FAL_KEY')
if not FAL_KEY:
    sys.exit('FAL_KEY not found in .env or environment.')

FAL_HEADERS = {
    'Authorization': 'Key ' + FAL_KEY,
    'Content-Type':  'application/json',
}

VISION_ENDPOINT = 'https://fal.run/fal-ai/any-llm/vision'
VISION_MODEL    = 'google/gemini-flash-1.5'

REGEN_ENDPOINT  = 'https://fal.run/fal-ai/flux-pro/kontext'

RPT_DIR  = os.path.join(ROOT, 'data', 'reports')
IMG_ROOT = os.path.join(ROOT, 'data', 'img2img')
COMP_DIR = '/tmp/bbi-qa-composites'
TS       = datetime.now().strftime('%Y%m%d-%H%M%S')

PASS_THRESHOLD = 7
MAX_RETRIES    = 2


# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
def parse_args():
    batch    = None
    phase    = 'phase1'
    do_retry = True
    manifest = None
    img_dir  = None
    for arg in sys.argv[1:]:
        if arg.startswith('--batch='):
            batch = arg.split('=', 1)[1]
        elif arg.startswith('--phase='):
            phase = arg.split('=', 1)[1]
        elif arg == '--no-retry':
            do_retry = False
        elif arg.startswith('--manifest='):
            manifest = arg.split('=', 1)[1]
        elif arg.startswith('--img-dir='):
            img_dir = arg.split('=', 1)[1]
    if not batch:
        sys.exit('Required: --batch=<name>')
    return batch, phase, do_retry, manifest, img_dir


# ---------------------------------------------------------------------------
# Image fetch + composite
# ---------------------------------------------------------------------------
def fetch_bytes(source):
    if source.startswith('http://') or source.startswith('https://'):
        req = urllib.request.Request(source, headers={'User-Agent': 'bbi-qa/1.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    with open(source, 'rb') as f:
        return f.read()


def make_composite(ref_bytes, gen_bytes, out_path, target_h=720):
    a = Image.open(io.BytesIO(ref_bytes)).convert('RGB')
    b = Image.open(io.BytesIO(gen_bytes)).convert('RGB')
    aw = int(a.width * (target_h / a.height))
    bw = int(b.width * (target_h / b.height))
    a = a.resize((aw, target_h), Image.LANCZOS)
    b = b.resize((bw, target_h), Image.LANCZOS)
    label_h = 36
    gap = 16
    total_w = aw + gap + bw
    total_h = target_h + label_h
    canvas = Image.new('RGB', (total_w, total_h), 'white')
    canvas.paste(a, (0, label_h))
    canvas.paste(b, (aw + gap, label_h))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
    except Exception:
        font = ImageFont.load_default()
    draw.text((8, 6), 'A: REFERENCE (real product)', fill='black', font=font)
    draw.text((aw + gap + 8, 6), 'B: GENERATED', fill='black', font=font)
    canvas.save(out_path, 'JPEG', quality=85)
    with open(out_path, 'rb') as f:
        return f.read()


def to_data_uri(jpg_bytes):
    return 'data:image/jpeg;base64,' + base64.standard_b64encode(jpg_bytes).decode('ascii')


# ---------------------------------------------------------------------------
# fal vision
# ---------------------------------------------------------------------------
PROMPT = (
    'You see one composite image with two photos side by side: A on the left is a real reference product photo, '
    'B on the right is supposed to depict the same product placed in an office context. '
    'Does the product in B match the product in A in form, colour, material, hardware, and proportions? '
    'Reply with ONLY a single-line JSON object: '
    '{"score": <integer 0-10>, "match": <true|false>, "reason": "<one short sentence>"}. '
    'No other text, no preamble, no markdown.'
)

JSON_RE = re.compile(r'\{[^{}]*"score"[^{}]*\}', re.DOTALL)


def vision_check(composite_data_uri, max_retries=3):
    body = json.dumps({
        'model':         VISION_MODEL,
        'prompt':        PROMPT,
        'image_url':     composite_data_uri,
    }).encode()
    last_err = ''
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(VISION_ENDPOINT, data=body, headers=FAL_HEADERS, method='POST')
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode())
            text = (data.get('output') or data.get('response') or data.get('text') or '').strip()
            if not text and isinstance(data.get('messages'), list):
                for m in data['messages']:
                    if m.get('content'):
                        text = m['content']
                        break
            m = JSON_RE.search(text)
            if not m:
                return None, None, 'parse_error', text[:200]
            parsed = json.loads(m.group(0))
            return int(parsed.get('score', 0)), bool(parsed.get('match', False)), parsed.get('reason', ''), text[:200]
        except urllib.error.HTTPError as e:
            code = e.code
            msg  = e.read().decode()[:200]
            if code in (400, 401, 403):
                return None, None, 'http {}: {}'.format(code, msg[:120]), msg
            last_err = 'http {}'.format(code)
            wait = 2 ** (attempt + 1)
            print('    fal vision {} (attempt {}/{}), retrying in {}s'.format(code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            last_err = str(e)
            wait = 2 ** (attempt + 1)
            print('    fal vision network error (attempt {}/{}): {} — retrying in {}s'.format(attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None, None, last_err, ''


# ---------------------------------------------------------------------------
# Regeneration
# ---------------------------------------------------------------------------
def regenerate(prompt, image_url):
    body = json.dumps({
        'prompt':              prompt,
        'image_url':           image_url,
        'guidance_scale':      3.5,
        'num_inference_steps': 28,
        'image_size':          'landscape_4_3',
        'num_images':          1,
        'safety_tolerance':    '2',
    }).encode()
    try:
        req = urllib.request.Request(REGEN_ENDPOINT, data=body, headers=FAL_HEADERS, method='POST')
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
            imgs = data.get('images') or []
            if imgs:
                return imgs[0]['url'], None
            return None, 'no images'
    except Exception as e:
        return None, str(e)


def download_to(url, dest_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'bbi-qa/1.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(dest_path, 'wb') as f:
            f.write(resp.read())


# ---------------------------------------------------------------------------
# Manifest IO
# ---------------------------------------------------------------------------
QA_FIELDS = [
    'handle', 'product_id', 'position', 'scene', 'filename',
    'source_hero_url', 'fal_url', 'local_path',
    'score', 'match', 'reason', 'status', 'retries', 'timestamp',
]


def load_manifest(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('status') == 'OK':
                rows.append(row)
    return rows


def append_qa(out_path, row):
    new_file = not os.path.exists(out_path)
    with open(out_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=QA_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    batch, phase, do_retry, manifest_arg, img_dir_arg = parse_args()
    manifest = manifest_arg or os.path.join(RPT_DIR, 'generated-img2img-{}.csv'.format(batch))
    img_dir  = img_dir_arg  or os.path.join(IMG_ROOT, phase, batch)
    qa_out   = os.path.join(RPT_DIR, 'qa-vision-{}.csv'.format(batch))

    if not os.path.exists(manifest):
        sys.exit('Manifest not found: {}'.format(manifest))

    rows = load_manifest(manifest)
    if not rows:
        sys.exit('No OK rows in {}.'.format(manifest))

    os.makedirs(COMP_DIR, exist_ok=True)
    if os.path.exists(qa_out):
        os.remove(qa_out)

    print('Manifest: {}'.format(manifest))
    print('Img dir:  {}'.format(img_dir))
    print('Vision:   {} via fal-ai/any-llm/vision'.format(VISION_MODEL))
    print('Rows:     {}'.format(len(rows)))
    print('Output:   {}'.format(qa_out))
    print('Retry:    {}'.format('on' if do_retry else 'off'))
    print()

    pass_count = 0
    flag_count = 0
    retry_count = 0

    for i, row in enumerate(rows, 1):
        handle   = row['handle']
        position = row['position']
        scene    = row.get('scene', '')
        source   = row['source_hero_url']
        fal_url  = row['fal_url']
        filename = row.get('filename') or '{}__pos{}__{}.jpg'.format(handle, position, scene)
        local    = os.path.join(img_dir, filename)
        prompt   = row.get('prompt', '')
        product_id = row.get('product_id', '')
        print('[{}/{}] {} pos {}'.format(i, len(rows), handle, position))

        gen_src_local = local if os.path.exists(local) else None
        try:
            ref_bytes = fetch_bytes(source)
            if gen_src_local:
                gen_bytes = fetch_bytes(gen_src_local)
            else:
                gen_bytes = fetch_bytes(fal_url)
            comp_path = os.path.join(COMP_DIR, '{}__pos{}.jpg'.format(handle, position))
            comp_bytes = make_composite(ref_bytes, gen_bytes, comp_path)
            data_uri = to_data_uri(comp_bytes)
        except Exception as e:
            print('  composite FAIL: {}'.format(e))
            append_qa(qa_out, {
                'handle': handle, 'product_id': product_id,
                'position': position, 'scene': scene, 'filename': filename,
                'source_hero_url': source, 'fal_url': fal_url, 'local_path': local,
                'score': '', 'match': '', 'reason': 'composite_error: {}'.format(e),
                'status': 'FLAG_HUMAN', 'retries': 0, 'timestamp': TS,
            })
            flag_count += 1
            continue

        retries = 0
        score, match, reason, raw = vision_check(data_uri)
        status = 'OK' if (score is not None and score >= PASS_THRESHOLD) else 'RETRY0'

        while do_retry and (score is None or score < PASS_THRESHOLD) and retries < MAX_RETRIES:
            retries += 1
            print('  score={} → regenerating (attempt {}/{})'.format(score, retries, MAX_RETRIES))
            new_url, err = regenerate(prompt, source)
            if not new_url:
                print('    regen FAIL: {}'.format(err))
                break
            try:
                download_to(new_url, local)
                fal_url = new_url
                gen_bytes = fetch_bytes(local)
                comp_bytes = make_composite(ref_bytes, gen_bytes, comp_path)
                data_uri = to_data_uri(comp_bytes)
            except Exception as e:
                print('    regen DOWNLOAD-FAIL: {}'.format(e))
                break
            score, match, reason, raw = vision_check(data_uri)

        if score is None or score < PASS_THRESHOLD:
            status = 'FLAG_HUMAN'
            flag_count += 1
        else:
            if retries == 0:
                status = 'OK'
            else:
                status = 'RETRY{}'.format(retries)
                retry_count += 1
            pass_count += 1

        print('  → {} score={} match={} reason={}'.format(status, score, match, (reason or '')[:80]))

        append_qa(qa_out, {
            'handle': handle, 'product_id': product_id,
            'position': position, 'scene': scene, 'filename': filename,
            'source_hero_url': source, 'fal_url': fal_url, 'local_path': local,
            'score': score if score is not None else '',
            'match': str(match) if match is not None else '',
            'reason': reason or '',
            'status': status, 'retries': retries, 'timestamp': TS,
        })

    print()
    print('=' * 60)
    print('Pass:           {}'.format(pass_count))
    print('Flagged:        {}'.format(flag_count))
    print('Saved by retry: {}'.format(retry_count))
    print('Output:         {}'.format(qa_out))
    print('=' * 60)


if __name__ == '__main__':
    main()
