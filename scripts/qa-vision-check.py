"""
Score every img2img generation by sending the source hero + the AI image to
Claude Opus 4.7 vision and parsing a JSON match score.

For each row in data/reports/generated-img2img-{date}.csv with Status=OK:
  1. Fetch source hero URL + FAL URL.
  2. Ask Claude: 'Does B depict the same product as A in form/colour/material?'
     Reply must be JSON: {score: 0-10, match: bool, reason: string}.
  3. If score < 7, regenerate that position (up to 2 retries) by re-running
     fal-ai/flux-pro/kontext with the original prompt + source hero.
  4. Final status: OK / RETRY1 / RETRY2 / FLAG_HUMAN.

Outputs:
  - data/reports/qa-vision-{date}.csv

Cost (~$0.005-0.01 per check, ~$0.04 per regen):
  - 10 images: ~$0.10  (Wave 0 pilot)
  - 40 images: ~$0.40  (Wave 1 pilot)

Requires ANTHROPIC_API_KEY in .env.

Usage:
  python3 scripts/qa-vision-check.py
  python3 scripts/qa-vision-check.py --manifest=data/reports/generated-img2img-2026-04-28.csv
  python3 scripts/qa-vision-check.py --no-retry
"""
import base64
import csv
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths & credentials
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

ANTHROPIC_API_KEY = env.get('ANTHROPIC_API_KEY') or os.environ.get('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    sys.exit('ANTHROPIC_API_KEY not found in .env or environment. Add it before running QA.')

FAL_KEY = env.get('FAL_KEY')

ANTHROPIC_ENDPOINT = 'https://api.anthropic.com/v1/messages'
ANTHROPIC_HEADERS  = {
    'x-api-key':         ANTHROPIC_API_KEY,
    'anthropic-version': '2023-06-01',
    'content-type':      'application/json',
}
ANTHROPIC_MODEL = 'claude-opus-4-7'

FAL_ENDPOINT = 'https://fal.run/fal-ai/flux-pro/kontext'
FAL_HEADERS  = {
    'Authorization': 'Key ' + (FAL_KEY or ''),
    'Content-Type':  'application/json',
}

IMG_DIR = os.path.join(ROOT, 'data', 'generated-img2img-images')
RPT_DIR = os.path.join(ROOT, 'data', 'reports')
TODAY   = datetime.now().strftime('%Y-%m-%d')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')

QA_OUTPUT = os.path.join(RPT_DIR, 'qa-vision-{}.csv'.format(TODAY))

PASS_THRESHOLD = 7
MAX_RETRIES    = 2


def parse_args():
    manifest = None
    do_retry = True
    for arg in sys.argv[1:]:
        if arg.startswith('--manifest='):
            manifest = arg.split('=', 1)[1]
        elif arg == '--no-retry':
            do_retry = False
    return manifest, do_retry


def latest_manifest():
    matches = sorted(glob.glob(os.path.join(RPT_DIR, 'generated-img2img-*.csv')))
    if not matches:
        sys.exit('No generated-img2img-*.csv found. Run generate-img2img-product-images.py first.')
    return matches[-1]


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------
def fetch_image_b64(source):
    """source can be a URL or a local file path. Returns (b64, media_type)."""
    if source.startswith('http://') or source.startswith('https://'):
        req = urllib.request.Request(source, headers={'User-Agent': 'bbi-qa/1.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            ct   = resp.headers.get('Content-Type', 'image/jpeg').split(';')[0].strip()
    else:
        with open(source, 'rb') as f:
            data = f.read()
        ct = 'image/jpeg' if source.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
    return base64.standard_b64encode(data).decode('ascii'), ct


# ---------------------------------------------------------------------------
# Claude vision
# ---------------------------------------------------------------------------
PROMPT = (
    'Image A is a real product photo (the reference). '
    'Image B is supposed to depict the same product placed in an office context. '
    'Does the product in B match the product in A in form, colour, material, hardware, and proportions? '
    'Reply with ONLY a JSON object on a single line: '
    '{"score": <integer 0-10>, "match": <true|false>, "reason": "<one sentence>"}. '
    'No other text.'
)

JSON_RE = re.compile(r'\{[^{}]*"score"[^{}]*\}')


def vision_check(source_hero, generated, max_retries=3):
    try:
        a_b64, a_ct = fetch_image_b64(source_hero)
        b_b64, b_ct = fetch_image_b64(generated)
    except Exception as e:
        return None, None, 'fetch_error: {}'.format(e), ''

    body = json.dumps({
        'model':      ANTHROPIC_MODEL,
        'max_tokens': 200,
        'messages': [{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': 'Image A:'},
                {'type': 'image', 'source': {'type': 'base64', 'media_type': a_ct, 'data': a_b64}},
                {'type': 'text', 'text': 'Image B:'},
                {'type': 'image', 'source': {'type': 'base64', 'media_type': b_ct, 'data': b_b64}},
                {'type': 'text', 'text': PROMPT},
            ],
        }],
    }).encode()

    last_err = ''
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(ANTHROPIC_ENDPOINT, data=body, headers=ANTHROPIC_HEADERS, method='POST')
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
            text = ''.join(b.get('text', '') for b in data.get('content', []) if b.get('type') == 'text').strip()
            m = JSON_RE.search(text)
            if not m:
                return None, None, 'parse_error', text[:200]
            parsed = json.loads(m.group(0))
            return int(parsed.get('score', 0)), bool(parsed.get('match', False)), parsed.get('reason', ''), text[:200]
        except urllib.error.HTTPError as e:
            code = e.code
            msg  = e.read().decode()[:200]
            if code in (400, 401, 403):
                return None, None, 'http {}: {}'.format(code, msg[:100]), msg
            last_err = 'http {}'.format(code)
            wait = 2 ** (attempt + 1)
            print('    Anthropic {} (attempt {}/{}), retrying in {}s'.format(code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            last_err = str(e)
            wait = 2 ** (attempt + 1)
            print('    Anthropic network error (attempt {}/{}): {} — retrying in {}s'.format(attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None, None, last_err, ''


# ---------------------------------------------------------------------------
# fal.ai regeneration
# ---------------------------------------------------------------------------
def regenerate(prompt, image_url):
    if not FAL_KEY:
        return None, 'no FAL_KEY for retry'
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
        req = urllib.request.Request(FAL_ENDPOINT, data=body, headers=FAL_HEADERS, method='POST')
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
    'Handle', 'Title', 'Image_Position', 'Source_Hero_URL', 'FAL_URL', 'Local_Path',
    'Score', 'Match', 'Reason', 'Status', 'Retries', 'Timestamp',
]


def load_manifest_rows(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') == 'OK':
                rows.append(row)
    return rows


def append_qa(row):
    new_file = not os.path.exists(QA_OUTPUT)
    with open(QA_OUTPUT, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=QA_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    manifest_arg, do_retry = parse_args()
    manifest = manifest_arg or latest_manifest()
    rows = load_manifest_rows(manifest)
    if not rows:
        sys.exit('No OK rows in {}.'.format(manifest))

    print('Manifest: {}'.format(manifest))
    print('Rows:     {}'.format(len(rows)))
    print('Output:   {}'.format(QA_OUTPUT))
    print('Retry:    {}'.format('on' if do_retry else 'off'))
    print()

    pass_count = 0
    flag_count = 0
    retry_count = 0

    for i, row in enumerate(rows, 1):
        handle   = row['Handle']
        position = row['Image_Position']
        source   = row['Source_Hero_URL']
        fal_url  = row['FAL_URL']
        local    = row['Local_Path']
        prompt   = row.get('Prompt', '')
        title    = row.get('Title', '')
        gen_src  = local if local and os.path.exists(local) else fal_url
        print('[{}/{}] {} pos {}'.format(i, len(rows), handle, position))

        retries  = 0
        score, match, reason, raw = vision_check(source, gen_src)
        status   = 'OK' if (score is not None and score >= PASS_THRESHOLD) else 'RETRY0'

        while do_retry and (score is None or score < PASS_THRESHOLD) and retries < MAX_RETRIES:
            retries += 1
            print('  score={} → regenerating (attempt {}/{})'.format(score, retries, MAX_RETRIES))
            new_url, err = regenerate(prompt, source)
            if not new_url:
                print('    regen FAIL: {}'.format(err))
                break
            try:
                download_to(new_url, local)
                gen_src = local
                fal_url = new_url
            except Exception as e:
                print('    regen DOWNLOAD-FAIL: {}'.format(e))
                break
            score, match, reason, raw = vision_check(source, gen_src)

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

        append_qa({
            'Handle': handle, 'Title': title,
            'Image_Position': position,
            'Source_Hero_URL': source, 'FAL_URL': fal_url, 'Local_Path': local,
            'Score': score if score is not None else '',
            'Match': str(match) if match is not None else '',
            'Reason': reason or '',
            'Status': status, 'Retries': retries, 'Timestamp': TS,
        })

    print()
    print('=' * 60)
    print('Pass:           {}'.format(pass_count))
    print('Flagged:        {}'.format(flag_count))
    print('Saved by retry: {}'.format(retry_count))
    print('Output:         {}'.format(QA_OUTPUT))
    print('=' * 60)


if __name__ == '__main__':
    main()
