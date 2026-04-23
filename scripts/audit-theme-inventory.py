"""
Audit the live Shopify theme and admin pages.
Outputs a coverage checklist for the BBI rebuild.

Writes:
  data/theme-inventory.json    — raw list of templates/sections/snippets/pages
  data/theme-coverage.md       — human-readable checklist
"""
import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
THEME_ID = '178274435385'
API = '2026-04'

BASE = f'https://{STORE}/admin/api/{API}'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {'_error': 'forbidden', '_url': url}
        raise


def list_theme_assets():
    data = get(f'{BASE}/themes/{THEME_ID}/assets.json')
    return [a['key'] for a in data['assets']]


def list_pages():
    url = f'{BASE}/pages.json?limit=250'
    data = get(url)
    if data.get('_error'):
        return None
    return data.get('pages', [])


def list_collections():
    colls = []
    for endpoint in ['custom_collections.json', 'smart_collections.json']:
        url = f'{BASE}/{endpoint}?limit=250&fields=id,title,handle,published_at,updated_at'
        data = get(url)
        if data.get('_error'):
            continue
        key = endpoint.replace('.json', '')
        colls.extend(data.get(key, []))
    return colls


def list_blogs_and_articles():
    data = get(f'{BASE}/blogs.json')
    if data.get('_error'):
        return None, None
    blogs = data.get('blogs', [])
    articles = []
    for b in blogs:
        ad = get(f'{BASE}/blogs/{b["id"]}/articles.json?limit=250&fields=id,title,handle,published_at')
        if ad.get('_error'):
            continue
        a = ad.get('articles', [])
        articles.extend([{**art, 'blog_handle': b['handle']} for art in a])
    return blogs, articles


def list_menus():
    # Storefront nav menus via GraphQL
    query = """
    { menus(first: 50) { edges { node { handle title items { title url type } } } } }
    """
    body = json.dumps({'query': query}).encode()
    req = urllib.request.Request(
        f'{BASE}/graphql.json', data=body, headers=HEADERS, method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    edges = data.get('data', {}).get('menus', {}).get('edges', [])
    return [e['node'] for e in edges]


def main():
    print('Fetching theme assets...')
    assets = list_theme_assets()

    templates = sorted([a for a in assets if a.startswith('templates/')])
    sections = sorted([a for a in assets if a.startswith('sections/')])
    snippets = sorted([a for a in assets if a.startswith('snippets/')])
    layout = sorted([a for a in assets if a.startswith('layout/')])
    config = sorted([a for a in assets if a.startswith('config/')])
    locales = sorted([a for a in assets if a.startswith('locales/')])
    assets_misc = sorted([a for a in assets if a.startswith('assets/')])

    print(f'  templates: {len(templates)}')
    print(f'  sections:  {len(sections)}')
    print(f'  snippets:  {len(snippets)}')
    print(f'  layout:    {len(layout)}')

    print('Fetching admin pages...')
    pages = list_pages()
    if pages is None:
        print('  SKIPPED — read_content scope missing')
        pages = []
        pages_scope_missing = True
    else:
        print(f'  pages: {len(pages)}')
        pages_scope_missing = False

    print('Fetching collections...')
    collections = list_collections()
    print(f'  collections: {len(collections)}')

    print('Fetching blogs + articles...')
    blogs, articles = list_blogs_and_articles()
    if blogs is None:
        print('  SKIPPED — read_content scope missing')
        blogs, articles = [], []
    else:
        print(f'  blogs: {len(blogs)}, articles: {len(articles)}')

    print('Fetching navigation menus...')
    try:
        menus = list_menus()
    except Exception as e:
        print(f'  menus fetch failed: {e}')
        menus = []
    print(f'  menus: {len(menus)}')

    inventory = {
        'theme_id': THEME_ID,
        'templates': templates,
        'sections': sections,
        'snippets': snippets,
        'layout': layout,
        'config': config,
        'locales_count': len(locales),
        'assets_count': len(assets_misc),
        'pages': [{'id': p['id'], 'title': p['title'], 'handle': p['handle'],
                   'published': bool(p.get('published_at'))} for p in pages],
        'collections': [{'title': c['title'], 'handle': c['handle'],
                         'published': bool(c.get('published_at'))} for c in collections],
        'blogs': [{'title': b['title'], 'handle': b['handle']} for b in blogs],
        'articles': [{'title': a['title'], 'handle': a['handle'],
                      'blog': a['blog_handle'],
                      'published': bool(a.get('published_at'))} for a in articles],
        'menus': [{'handle': m['handle'], 'title': m['title'],
                   'item_count': len(m.get('items', []))} for m in menus],
    }

    out_json = '/Users/leokatz/Desktop/Office Central/data/theme-inventory.json'
    with open(out_json, 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f'\nWrote {out_json}')

    # Build markdown checklist
    md = ['# BBI Shopify Theme — Coverage Checklist',
          f'\nTheme ID: `{THEME_ID}` · Generated from live theme inventory\n',
          '## 1. Page templates (each = a page type)',
          f'Total: **{len(templates)}**\n']
    for t in templates:
        md.append(f'- [ ] `{t}`')
    md.append('\n## 2. Sections (reusable blocks)')
    md.append(f'Total: **{len(sections)}**\n')
    for s in sections:
        md.append(f'- [ ] `{s}`')
    md.append('\n## 3. Snippets (smaller reusable pieces)')
    md.append(f'Total: **{len(snippets)}**\n')
    for s in snippets:
        md.append(f'- [ ] `{s}`')
    md.append('\n## 4. Layout files')
    for l in layout:
        md.append(f'- [ ] `{l}`')
    md.append('\n## 5. Admin pages (content pages in Shopify admin)')
    if pages_scope_missing:
        md.append('*Not fetched — `read_content` scope missing. Pull manually from Shopify Admin → Online Store → Pages.*')
    else:
        md.append(f'Total: **{len(pages)}** ({sum(1 for p in pages if p.get("published_at"))} published)\n')
        for p in pages:
            status = 'published' if p.get('published_at') else 'DRAFT'
            md.append(f'- [ ] `/pages/{p["handle"]}` — {p["title"]} ({status})')
    md.append('\n## 6. Collections (category pages)')
    md.append(f'Total: **{len(collections)}** ({sum(1 for c in collections if c.get("published_at"))} published)\n')
    for c in sorted(collections, key=lambda x: x['handle']):
        status = '' if c.get('published_at') else ' (DRAFT)'
        md.append(f'- [ ] `/collections/{c["handle"]}` — {c["title"]}{status}')
    md.append('\n## 7. Blog + articles')
    for b in blogs:
        md.append(f'\n### Blog: {b["title"]} (`/blogs/{b["handle"]}`)')
        blog_articles = [a for a in articles if a['blog_handle'] == b['handle']]
        for a in blog_articles:
            status = '' if a.get('published_at') else ' (DRAFT)'
            md.append(f'- [ ] `/blogs/{b["handle"]}/{a["handle"]}` — {a["title"]}{status}')
    md.append('\n## 8. Navigation menus')
    for m in inventory['menus']:
        md.append(f'- [ ] `{m["handle"]}` — {m["title"]} ({m["item_count"]} items)')

    md.append('\n---')
    md.append('## Summary')
    md.append(f'- Templates: {len(templates)}')
    md.append(f'- Sections: {len(sections)}')
    md.append(f'- Snippets: {len(snippets)}')
    md.append(f'- Admin pages: {len(pages)}')
    md.append(f'- Collections: {len(collections)}')
    md.append(f'- Blog articles: {len(articles)}')
    md.append(f'- Menus: {len(menus)}')
    md.append(f'- Other assets (JS/CSS/images): {len(assets_misc)}')

    out_md = '/Users/leokatz/Desktop/Office Central/data/theme-coverage.md'
    with open(out_md, 'w') as f:
        f.write('\n'.join(md))
    print(f'Wrote {out_md}')


if __name__ == '__main__':
    main()
