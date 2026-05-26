"""
Wire a hero image into a BBI section by patching the template JSON via Shopify Admin API.

Used by the interactive manual image upload session (Day 11 #14e, 2026-05-25).
The operator uploads a processed JPG to Shopify Files (manual drag-drop in Admin),
pastes the resulting CDN URL back; this script then converts the CDN URL to the
`shopify://shop_images/{filename}` reference and writes it into
`sections.<section_key>.settings.hero_image` of the target template JSON, on the
specified theme (DEV: 186373570873).

LIVE theme `178274435385` must not be touched — there is no guard here, but the
operator is expected to pass only the DEV theme id.

Env:
  SHOPIFY_TOKEN — Admin API token with write_themes
  SHOPIFY_STORE — office-central-online.myshopify.com (default)

Usage:
  python3 scripts/bbi-wire-hero-image.py <theme_id> <template> <section_key> <cdn_url>

Example (slot 7 — Desks hero):
  python3 scripts/bbi-wire-hero-image.py 186373570873 \
    templates/collection.desks.json ds-cc-base \
    'https://cdn.shopify.com/s/files/1/0859/0413/0361/files/desks-hero.jpg?v=1779736700'
"""
import os
import sys
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse


TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = os.environ.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API_VERSION = '2026-04'


def _request(method, path, body=None):
    url = f'https://{STORE}/admin/api/{API_VERSION}{path}'
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        method=method,
        data=data,
        headers={
            'X-Shopify-Access-Token': TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='replace')
        raise SystemExit(f'HTTP {e.code} on {method} {path}\n{body}')


def cdn_url_to_shop_images(cdn_url):
    """Extract filename from a Shopify CDN URL and wrap as shopify://shop_images/{filename}.

    Input example:
      https://cdn.shopify.com/s/files/1/0859/0413/0361/files/desks-hero.jpg?v=1779736700
    Output:
      shopify://shop_images/desks-hero.jpg
    """
    parsed = urlparse(cdn_url)
    filename = parsed.path.rsplit('/', 1)[-1]
    if not filename:
        raise SystemExit(f'Could not extract filename from CDN URL: {cdn_url}')
    return f'shopify://shop_images/{filename}'


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)

    theme_id, template_key, section_key, cdn_url = sys.argv[1:5]
    shop_ref = cdn_url_to_shop_images(cdn_url)

    print(f'  Theme:    {theme_id}')
    print(f'  Template: {template_key}')
    print(f'  Section:  {section_key}')
    print(f'  CDN URL:  {cdn_url}')
    print(f'  → New hero_image: {shop_ref}')
    print()

    # 1) GET current template JSON
    asset_path = f'/themes/{theme_id}/assets.json?asset[key]={template_key}'
    got = _request('GET', asset_path)
    raw = got['asset']['value']
    template = json.loads(raw)

    sections = template.get('sections', {})
    if section_key not in sections:
        raise SystemExit(
            f'Section key "{section_key}" not found in {template_key}. '
            f'Available keys: {list(sections.keys())}'
        )

    section = sections[section_key]
    settings = section.setdefault('settings', {})
    old = settings.get('hero_image')
    settings['hero_image'] = shop_ref

    print(f'  hero_image: {old!r}')
    print(f'           → {shop_ref!r}')
    print()

    # 2) PUT updated JSON
    new_raw = json.dumps(template, indent=2, ensure_ascii=False)
    put_body = {
        'asset': {
            'key': template_key,
            'value': new_raw,
        }
    }
    _request('PUT', f'/themes/{theme_id}/assets.json', put_body)
    print(f'  ✓ wired hero_image on {template_key}')


if __name__ == '__main__':
    main()
