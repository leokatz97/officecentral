"""
Generate 10 BBI logo options using fal.ai Ideogram v2.
2 options per each of 5 design directions.

Output:   data/logos/options/option-01.png … option-10.png
Index:    data/logos/options/index.json

Usage:
  python3 scripts/generate-logo-options.py              # dry run (no API calls)
  python3 scripts/generate-logo-options.py --live       # call fal.ai + download
"""
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
    env = dict(
        line.strip().split('=', 1)
        for line in f
        if '=' in line and not line.strip().startswith('#')
    )

FAL_KEY     = env['FAL_KEY']
OUT_DIR     = os.path.join(ROOT, 'data', 'logos', 'options')
FAL_ENDPOINT = 'https://fal.run/fal-ai/ideogram/v2'

# ---------------------------------------------------------------------------
# 10 logo option specs
# ---------------------------------------------------------------------------
OPTIONS = [
    {
        "id": "01",
        "direction": "Modernize",
        "prompt": (
            "Professional corporate logo design. Horizontal wordmark reading "
            "'Brant BASICS | BUSINESS INTERIORS'. Clean bold geometric sans-serif. "
            "'Brant' in charcoal #0B0B0C, 'BASICS' in deep red #D4252A with a small "
            "Canadian maple leaf icon beside it, thin vertical rule divider, "
            "'BUSINESS INTERIORS' in charcoal small-caps to the right. "
            "Pure white background. Modern, precise, institutional. No tagline."
        ),
    },
    {
        "id": "02",
        "direction": "Modernize",
        "prompt": (
            "Professional corporate logo. Horizontal lockup: 'BRANT' in light-weight "
            "charcoal sans-serif, immediately followed by 'BASICS' in heavy-weight "
            "deep red #D4252A, then a thin vertical rule, then 'BUSINESS INTERIORS' "
            "in small-caps charcoal stacked two lines on the right. Small red maple "
            "leaf superscript near BASICS. White background. Refined, balanced, B2B."
        ),
    },
    {
        "id": "03",
        "direction": "Bold & Punchy",
        "prompt": (
            "Bold commercial logo. 'BRANT BASICS' set in extra-bold condensed "
            "sans-serif all-caps, large, deep red #D4252A fill. Beneath it a full-width "
            "charcoal #0B0B0C bar with 'BUSINESS INTERIORS' reversed out in white "
            "small-caps. Strong contrast, heavy grid, no decoration. "
            "White background overall. High-impact B2B brand mark."
        ),
    },
    {
        "id": "04",
        "direction": "Bold & Punchy",
        "prompt": (
            "Bold horizontal logo on a black #0B0B0C background banner. "
            "'Brant BASICS' in white knockout extra-bold sans-serif on the left, "
            "with a red maple-leaf star replacing the dot in 'BASICS'. "
            "'BUSINESS INTERIORS' in white small-caps right side. "
            "Horizontal layout, industrial authority, tight kerning."
        ),
    },
    {
        "id": "05",
        "direction": "Minimal",
        "prompt": (
            "Minimalist corporate wordmark. Single line: 'BRANT BASICS  BUSINESS INTERIORS' "
            "in thin geometric sans-serif all-caps, very wide letter-spacing, charcoal "
            "#0B0B0C. A single hairline rule in deep red #D4252A beneath the full width. "
            "No icon, no border, pure white background. Understated, elegant, institutional."
        ),
    },
    {
        "id": "06",
        "direction": "Minimal",
        "prompt": (
            "Minimal monogram logo. A perfect red circle containing 'BB' in clean white "
            "sans-serif. To the right: 'Brant Business Interiors' in two lines — 'Brant' "
            "light weight charcoal, 'Business Interiors' regular weight charcoal, "
            "vertically centered beside the circle. White background. Clean, professional, scalable."
        ),
    },
    {
        "id": "07",
        "direction": "Fresh Rebrand",
        "prompt": (
            "Modern rebrand logo. 'BBI' as a geometric letterform mark in deep charcoal "
            "#0B0B0C — the letters constructed from architectural floor-plan grid lines, "
            "with a thin red accent line. Beneath the mark: 'Brant Business Interiors' "
            "in clean light sans-serif charcoal. White background. Architectural, credible, fresh."
        ),
    },
    {
        "id": "08",
        "direction": "Fresh Rebrand",
        "prompt": (
            "Contemporary rebrand. Abstract icon made of two interlocking 'B' letterforms "
            "suggesting a building floor plan, deep charcoal with a single red accent corner. "
            "Beside it: 'Brant Business Interiors' in clean modern sans-serif charcoal. "
            "White background. No maple leaf. Architectural, sophisticated, B2B."
        ),
    },
    {
        "id": "09",
        "direction": "Canadian Heritage",
        "prompt": (
            "Canadian-themed corporate logo. 'Brant BASICS' wordmark where the 'A' in "
            "BASICS is replaced by a prominent stylized Canadian maple leaf in deep red "
            "#D4252A. 'BASICS' in bold charcoal around it. Sub-line: "
            "'Business Interiors  |  Est. Ontario' in small charcoal sans-serif caps. "
            "White background. Canadian pride, institutional trust."
        ),
    },
    {
        "id": "10",
        "direction": "Canadian Heritage",
        "prompt": (
            "Institutional crest-style badge logo. Circular badge design: maple leaf at "
            "the top center in red, 'BRANT BUSINESS INTERIORS' arching around the top "
            "half, 'OECM Certified Supplier' arching the bottom half, all in charcoal "
            "#0B0B0C. Red and black palette. White background. Authoritative, governmental, Ontario B2B."
        ),
    },
]

# ---------------------------------------------------------------------------
# fal.ai call
# ---------------------------------------------------------------------------
def call_fal(prompt, max_retries=3):
    body = json.dumps({
        'prompt':              prompt,
        'aspect_ratio':        '16:9',
        'style_type':          'DESIGN',
        'magic_prompt_option': 'OFF',
    }).encode()
    headers = {
        'Authorization': 'Key ' + FAL_KEY,
        'Content-Type':  'application/json',
    }
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                FAL_ENDPOINT, data=body, headers=headers, method='POST'
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
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
            print('    fal.ai {} (attempt {}/{}), retrying in {}s'.format(
                code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** (attempt + 1)
            print('    error (attempt {}/{}): {}, retrying in {}s'.format(
                attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None


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
# Main
# ---------------------------------------------------------------------------
def main():
    live = '--live' in sys.argv

    if not live:
        print('\n=== DRY RUN — pass --live to generate images ===\n')
        for opt in OPTIONS:
            print('option-{}.png  [{}]'.format(opt['id'], opt['direction']))
            print('  Prompt: {}'.format(opt['prompt'][:120] + '...'))
            print()
        print('10 options across 5 directions.')
        print('Run with --live to call fal.ai Ideogram v2 and download PNGs.\n')
        return

    os.makedirs(OUT_DIR, exist_ok=True)

    index = []
    generated = 0
    failed    = 0

    print('\n=== Generating 10 BBI logo options via Ideogram v2 ===\n')

    for opt in OPTIONS:
        filename = 'option-{}.png'.format(opt['id'])
        dest     = os.path.join(OUT_DIR, filename)

        if os.path.exists(dest):
            size = os.path.getsize(dest)
            print('[{}] {} ({}) already exists ({} KB) — skipping'.format(
                opt['id'], filename, opt['direction'], size // 1024))
            index.append({**opt, 'file': filename, 'status': 'skipped'})
            continue

        print('[{}] {} ({}) — calling fal.ai...'.format(
            opt['id'], filename, opt['direction']))

        url = call_fal(opt['prompt'])
        if not url:
            print('    FAILED — skipping')
            failed += 1
            index.append({**opt, 'file': filename, 'status': 'failed'})
            continue

        ok = download_image(url, dest)
        if ok:
            size = os.path.getsize(dest)
            print('    Downloaded — {} KB'.format(size // 1024))
            generated += 1
            index.append({**opt, 'file': filename, 'url': url, 'status': 'ok'})
        else:
            failed += 1
            index.append({**opt, 'file': filename, 'status': 'download_failed'})

    # Write index
    index_path = os.path.join(OUT_DIR, 'index.json')
    with open(index_path, 'w') as f:
        json.dump({'generated_at': datetime.now().isoformat(), 'options': index}, f, indent=2)

    print('\n=== Done: {} generated, {} failed ==='.format(generated, failed))
    print('Images saved to: {}'.format(OUT_DIR))
    print('Index: {}'.format(index_path))
    print('\nOpen the folder in Finder to review, then tell Claude which number you want as the canonical logo.\n')


if __name__ == '__main__':
    main()
