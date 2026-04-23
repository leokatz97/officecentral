"""
Push the BBI landing-page additions into an unpublished Shopify theme.

Reads files from the repo's `theme/` folder and uploads:
  - assets/ds-*
  - assets/bbi-*.svg
  - assets/maple-leaf.svg
  - sections/ds-*.liquid
  - snippets/ds-*.liquid
  - templates/page.oecm.json
  - templates/page.brand-dealer.json

Then creates two Shopify Pages bound to the new templates.

Env:
  SHOPIFY_TOKEN — Admin API token with write_themes + write_content
  SHOPIFY_STORE — office-central-online.myshopify.com

Usage:
  python3 scripts/bbi-push-landing.py <THEME_ID>
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = os.environ.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API = '2026-04'

if len(sys.argv) < 2:
    print('Usage: python3 scripts/bbi-push-landing.py <THEME_ID>')
    sys.exit(1)
THEME_ID = sys.argv[1]

BASE = f'https://{STORE}/admin/api/{API}'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

ROOT = Path(os.environ.get('BBI_PUSH_ROOT', Path(__file__).resolve().parent.parent))
THEME = ROOT / 'theme'
if not THEME.exists():
    raise SystemExit(f'theme/ not found at {THEME} — set BBI_PUSH_ROOT to the repo root that has theme/')

TEXT_SUFFIXES = {'.liquid', '.json', '.css', '.js', '.svg'}
BINARY_SUFFIXES = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.ico'}


def api(method, path, body=None):
    url = f'{BASE}{path}'
    data = None
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode() or '{}'
            return json.loads(raw), resp.status
    except urllib.error.HTTPError as e:
        return {'_error': e.read().decode(), '_code': e.code}, e.code


def upload_file(path: Path, key: str):
    if path.suffix.lower() in BINARY_SUFFIXES:
        data = base64.b64encode(path.read_bytes()).decode()
        body = {'asset': {'key': key, 'attachment': data}}
    else:
        body = {'asset': {'key': key, 'value': path.read_text(encoding='utf-8')}}
    result, code = api('PUT', f'/themes/{THEME_ID}/assets.json', body)
    ok = code < 300
    print(f"  {'OK ' if ok else 'FAIL'} {key} ({code})")
    if not ok:
        print(f"       {result.get('_error', result)[:200]}")
    return ok


def files_to_push():
    patterns = [
        ('assets', 'ds-*'),
        ('assets', 'bbi-*.svg'),
        ('assets', 'maple-leaf.svg'),
        ('sections', 'ds-*.liquid'),
        ('snippets', 'ds-*.liquid'),
        ('templates', 'page.oecm.json'),
        ('templates', 'page.brand-dealer.json'),
    ]
    for subdir, pattern in patterns:
        for p in sorted((THEME / subdir).glob(pattern)):
            key = f'{subdir}/{p.name}'
            yield p, key


def ensure_page(title, handle, template_suffix):
    existing, code = api('GET', f'/pages.json?handle={handle}&limit=1')
    if code >= 300:
        print(f'  FAIL lookup {handle}: {existing}')
        return None
    pages = existing.get('pages', [])
    if pages:
        page_id = pages[0]['id']
        result, code = api('PUT', f'/pages/{page_id}.json', {
            'page': {'id': page_id, 'template_suffix': template_suffix}
        })
        print(f'  OK  page updated {handle} (id={page_id})')
        return page_id
    result, code = api('POST', '/pages.json', {
        'page': {
            'title': title,
            'handle': handle,
            'body_html': '',
            'template_suffix': template_suffix,
            'published': False,  # keep unpublished; the dev theme is unpublished anyway
        }
    })
    if code >= 300:
        print(f'  FAIL create {handle}: {result}')
        return None
    page_id = result['page']['id']
    print(f'  OK  page created {handle} (id={page_id})')
    return page_id


def main():
    print(f'Pushing to theme {THEME_ID} on {STORE}')
    print(f'API base: {BASE}')
    print()

    # Preflight: can we read the theme?
    info, code = api('GET', f'/themes/{THEME_ID}.json')
    if code >= 300:
        print(f'FAIL preflight — theme {THEME_ID} not reachable: {info}')
        return 1
    print(f'Theme name: {info["theme"]["name"]}  role={info["theme"]["role"]}')
    print()

    # Upload assets
    print('Uploading files:')
    ok, fail = 0, 0
    for path, key in files_to_push():
        if upload_file(path, key):
            ok += 1
        else:
            fail += 1
    print()
    print(f'Upload: {ok} ok, {fail} failed')
    if fail:
        return 1

    # Create pages
    print()
    print('Ensuring pages exist and are bound to the new templates:')
    ensure_page('OECM', 'oecm', 'oecm')
    ensure_page('ergoCentric', 'ergocentric', 'brand-dealer')
    print()

    preview_base = f'https://{STORE.replace(".myshopify.com", "")}.myshopify.com'
    print('Preview URLs (accessible only via the dev theme Preview link in admin):')
    print(f'  {preview_base}/pages/oecm?preview_theme_id={THEME_ID}')
    print(f'  {preview_base}/pages/ergocentric?preview_theme_id={THEME_ID}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
