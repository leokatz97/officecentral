#!/usr/bin/env python3
"""
AI-1 deploy: create/update Shopify Page 'llms-txt' from data/llms-txt-draft.md
and add a URL redirect /llms.txt -> /pages/llms-txt.

Usage:
  python3 scripts/deploy-ai1-llmstxt.py            # DRY RUN (default)
  python3 scripts/deploy-ai1-llmstxt.py --live     # actually create/update

Notes:
  - Page body is the markdown wrapped in <pre> for max AI crawler readability.
  - Handle: llms-txt  →  Public URL: /pages/llms-txt
  - Redirect: /llms.txt → /pages/llms-txt (requires write_content scope; will
    print a manual fallback if scope is missing).
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / '.env'
MD_PATH = ROOT / 'data/llms-txt-draft.md'

for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip())

SHOP = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN,
        'Content-Type': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if 'errors' in data:
        raise RuntimeError(f'GraphQL errors: {data["errors"]}')
    return data['data']

def find_page_by_handle(handle):
    q = '''query($q: String!) {
      pages(first: 1, query: $q) { edges { node { id handle title } } }
    }'''
    d = gql(q, {'q': f'handle:{handle}'})
    edges = d['pages']['edges']
    return edges[0]['node'] if edges else None

def main():
    live = '--live' in sys.argv
    md = MD_PATH.read_text()
    title = 'BBI for AI assistants (llms.txt)'
    handle = 'llms-txt'
    # Wrap raw markdown in <pre> for AI/text-first readability.
    body_html = (
        '<p>This page is a structured summary of Brant Business Interiors '
        'for use by AI assistants and search-engine crawlers '
        '(<a href="https://llmstxt.org" rel="noopener">llmstxt.org</a> spec).</p>'
        f'<pre style="white-space:pre-wrap;font-family:ui-monospace,Menlo,monospace;font-size:13px;line-height:1.55;">{md}</pre>'
    )

    print(f'Mode: {"LIVE" if live else "DRY RUN"}')
    print(f'Source: {MD_PATH} ({len(md):,} chars)')
    print(f'Page handle: {handle}')
    print(f'Public URL: https://www.brantbusinessinteriors.com/pages/{handle}')
    print()

    existing = find_page_by_handle(handle)
    if existing:
        print(f'  Page exists: {existing["id"]} — will UPDATE')
    else:
        print('  Page does not exist — will CREATE')
    print(f'  Redirect: /llms.txt → /pages/{handle}')

    if not live:
        print('\n(Pass --live to apply.)')
        return 0

    # Create or update page
    if existing:
        m = '''mutation($input: PageUpdateInput!, $id: ID!) {
          pageUpdate(id: $id, page: $input) {
            page { id handle title }
            userErrors { field message }
          }
        }'''
        d = gql(m, {'id': existing['id'], 'input': {
            'title': title, 'body': body_html, 'isPublished': True,
        }})
        errs = d['pageUpdate']['userErrors']
        if errs:
            raise RuntimeError(f'pageUpdate errors: {errs}')
        page = d['pageUpdate']['page']
        print(f'  ✓ Updated page {page["id"]}')
    else:
        m = '''mutation($input: PageCreateInput!) {
          pageCreate(page: $input) {
            page { id handle title }
            userErrors { field message }
          }
        }'''
        d = gql(m, {'input': {
            'title': title, 'handle': handle, 'body': body_html, 'isPublished': True,
        }})
        errs = d['pageCreate']['userErrors']
        if errs:
            raise RuntimeError(f'pageCreate errors: {errs}')
        page = d['pageCreate']['page']
        print(f'  ✓ Created page {page["id"]}')

    # Redirect
    try:
        m = '''mutation($input: UrlRedirectInput!) {
          urlRedirectCreate(urlRedirect: $input) {
            urlRedirect { id path target }
            userErrors { field message }
          }
        }'''
        d = gql(m, {'input': {'path': '/llms.txt', 'target': f'/pages/{handle}'}})
        errs = d['urlRedirectCreate']['userErrors']
        if errs and 'has already been taken' in str(errs):
            print('  ✓ Redirect /llms.txt already exists — skipping')
        elif errs:
            raise RuntimeError(f'urlRedirectCreate errors: {errs}')
        else:
            print(f'  ✓ Created redirect /llms.txt → /pages/{handle}')
    except Exception as e:
        msg = str(e)
        if 'access denied' in msg.lower() or 'write_content' in msg.lower() or 'access' in msg.lower():
            print()
            print('  ⚠️  Could not auto-create redirect — token missing write_content scope.')
            print('  MANUAL STEP for Leo:')
            print('     Shopify Admin → Online Store → Navigation → URL Redirects → Create URL redirect')
            print(f'     From: /llms.txt   To: /pages/{handle}')
        else:
            raise

    print()
    print('=' * 60)
    print(f'Page live: https://www.brantbusinessinteriors.com/pages/{handle}')
    print('After redirect is in place, /llms.txt will serve the same content.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
