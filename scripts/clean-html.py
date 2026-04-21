import urllib.request
import json
import re
import os
import html as html_lib
from bs4 import BeautifulSoup, NavigableString

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'

ALLOWED_TAGS = {'p', 'ul', 'ol', 'li', 'strong', 'b', 'em', 'i', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'}
JUNK_CLASS_PREFIXES = ('goods__', 'product-details-wrapper', 'margindiv', 'panel', 'row', 'col', 'productdetails',
                       'prod-category', 'text-small', 'product-points', 'productdescription', 'accordion',
                       'collapseDescription', 'panel-body', 'panel-group', 'form-group', 'product-description',
                       'product-brand', 'manufacturer-ref', 'MsoNormal')
HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def fetch_all_products():
    products = []
    url = f'{API}/products.json?limit=250&fields=id,title,body_html,handle'
    while url:
        req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            products.extend(data['products'])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(products)}...')
    return products


def strip_text(html):
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def classify(html):
    if not html or not html.strip():
        return 'empty'
    text = strip_text(html)
    if len(text) < 20:
        return 'empty'
    if 'mso-' in html or 'MsoNormal' in html:
        return 'word_junk'
    tag_density = len(re.findall(r'<[^>]+>', html)) / max(len(text.split()), 1)
    if tag_density > 0.5:
        return 'heavy_html'
    return 'clean'


def has_junk_class(tag):
    classes = tag.get('class') or []
    return any(c.startswith(JUNK_CLASS_PREFIXES) for c in classes)


def unwrap_junk_divs(soup):
    for tag in soup.find_all(['div', 'section', 'table', 'tbody', 'tr', 'td', 'thead']):
        tag.unwrap()


def clean_attrs(tag):
    if tag.name == 'span':
        tag.unwrap()
        return
    keep = {}
    tag.attrs = keep


def is_empty(tag):
    if tag.name == 'br':
        return False
    text = tag.get_text().replace('\xa0', '').strip()
    if text:
        return False
    if tag.find('img'):
        return False
    return True


def clean_html(raw):
    if not raw:
        return ''
    soup = BeautifulSoup(raw, 'lxml')
    if soup.body:
        soup = BeautifulSoup(''.join(str(c) for c in soup.body.contents), 'lxml')
        if soup.body:
            root = soup.body
        else:
            root = soup
    else:
        root = soup

    for t in root.find_all(['script', 'style', 'meta', 'link', 'form', 'input', 'button', 'iframe', 'img']):
        t.decompose()

    for t in root.find_all(True):
        if t.name not in ALLOWED_TAGS and t.name not in {'div', 'section', 'table', 'tbody', 'tr', 'td', 'thead', 'html', 'body', '[document]'}:
            t.unwrap()

    for t in root.find_all(['div', 'section', 'table', 'tbody', 'tr', 'td', 'thead']):
        t.unwrap()

    for t in list(root.find_all(True)):
        if t.name == 'span':
            t.unwrap()
            continue
        t.attrs = {}

    for _ in range(3):
        removed = False
        for t in list(root.find_all(True)):
            if t.name in HEADING_TAGS or t.name == 'p' or t.name == 'li':
                if is_empty(t):
                    t.decompose()
                    removed = True
        if not removed:
            break

    for ul in list(root.find_all(['ul', 'ol'])):
        if not ul.find('li'):
            ul.decompose()

    out = ''.join(str(c) for c in root.contents) if hasattr(root, 'contents') else str(root)
    out = re.sub(r'(\s*<p>\s*(&nbsp;|\xa0)?\s*</p>\s*)+', '', out)
    out = re.sub(r'\n\s*\n+', '\n', out)
    out = re.sub(r'[ \t]+', ' ', out)
    return out.strip()


def main():
    print('Fetching all products...')
    products = fetch_all_products()
    print(f'\nTotal: {len(products)} products\n')

    to_clean = []
    for p in products:
        cat = classify(p.get('body_html', ''))
        if cat in ('heavy_html', 'word_junk'):
            to_clean.append((p, cat))

    print(f'Products to clean: {len(to_clean)}')
    by_cat = {}
    for _, c in to_clean:
        by_cat[c] = by_cat.get(c, 0) + 1
    for c, n in by_cat.items():
        print(f'  {c}: {n}')

    cleaned = []
    skipped = []
    for p, cat in to_clean:
        try:
            after = clean_html(p['body_html'])
            before_text_len = len(strip_text(p['body_html']))
            after_text_len = len(strip_text(after))
            if after_text_len < max(10, before_text_len * 0.5):
                skipped.append((p, cat, f'text loss: {before_text_len} -> {after_text_len}'))
                continue
            cleaned.append({
                'id': p['id'],
                'title': p['title'],
                'handle': p.get('handle', ''),
                'category': cat,
                'before': p['body_html'],
                'after': after,
                'before_len': len(p['body_html']),
                'after_len': len(after),
            })
        except Exception as e:
            skipped.append((p, cat, f'error: {e}'))

    print(f'\nCleaned: {len(cleaned)}')
    print(f'Skipped: {len(skipped)}')
    if skipped:
        print('Skipped reasons (first 5):')
        for p, cat, r in skipped[:5]:
            print(f'  [{cat}] {p["title"][:50]}: {r}')

    samples = []
    word_junk_samples = [c for c in cleaned if c['category'] == 'word_junk'][:3]
    heavy_samples = [c for c in cleaned if c['category'] == 'heavy_html']
    heavy_samples = sorted(heavy_samples, key=lambda c: c['before_len'], reverse=True)[:7]
    samples = word_junk_samples + heavy_samples
    samples = samples[:10]

    html_parts = ['''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>HTML Cleanup Preview</title>
<style>
body { font-family: -apple-system, sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; }
h1 { color: #222; }
h2 { color: #444; border-bottom: 2px solid #ddd; padding-bottom: 6px; margin-top: 40px; }
.summary { background: #f4f4f4; padding: 16px; border-radius: 6px; margin-bottom: 24px; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.col { border: 1px solid #ccc; border-radius: 6px; padding: 14px; overflow: auto; max-height: 600px; background: #fff; }
.col.before { background: #fff5f5; }
.col.after { background: #f5fff5; }
.col h3 { margin-top: 0; font-size: 13px; text-transform: uppercase; color: #666; }
.rendered { border-top: 1px dashed #aaa; margin-top: 10px; padding-top: 10px; }
pre { white-space: pre-wrap; word-break: break-all; font-size: 11px; background: #fafafa; padding: 8px; border-radius: 4px; max-height: 240px; overflow: auto; }
.meta { font-size: 12px; color: #666; }
.cat { display: inline-block; padding: 2px 8px; border-radius: 3px; background: #eee; font-size: 11px; font-weight: bold; }
.cat.word_junk { background: #ffd; }
.cat.heavy_html { background: #dff; }
</style></head><body>''']
    html_parts.append(f'<h1>HTML Cleanup Preview — {len(samples)} sample products</h1>')
    html_parts.append(f'''<div class="summary">
<strong>Total products:</strong> {len(products)}<br>
<strong>To clean:</strong> {len(to_clean)} (heavy_html: {by_cat.get("heavy_html",0)}, word_junk: {by_cat.get("word_junk",0)})<br>
<strong>Cleaned successfully:</strong> {len(cleaned)}<br>
<strong>Skipped:</strong> {len(skipped)}<br>
<strong>Mode:</strong> DRY RUN — nothing written back to Shopify
</div>''')

    for s in samples:
        shrink = (1 - s['after_len'] / max(s['before_len'], 1)) * 100
        html_parts.append(f'''<h2>{html_lib.escape(s["title"])} <span class="cat {s["category"]}">{s["category"]}</span></h2>
<div class="meta">ID: {s["id"]} · handle: {s["handle"]} · {s["before_len"]} → {s["after_len"]} chars ({shrink:.0f}% smaller)</div>
<div class="pair">
  <div class="col before">
    <h3>BEFORE</h3>
    <div class="rendered">{s["before"]}</div>
    <pre>{html_lib.escape(s["before"])}</pre>
  </div>
  <div class="col after">
    <h3>AFTER</h3>
    <div class="rendered">{s["after"]}</div>
    <pre>{html_lib.escape(s["after"])}</pre>
  </div>
</div>''')

    html_parts.append('</body></html>')
    with open('html-cleanup-preview.html', 'w') as f:
        f.write('\n'.join(html_parts))

    with open('html-cleanup-results.json', 'w') as f:
        json.dump({
            'total': len(products),
            'to_clean': len(to_clean),
            'cleaned': len(cleaned),
            'skipped': len(skipped),
            'by_category': by_cat,
            'cleaned_ids': [c['id'] for c in cleaned],
            'skipped': [{'id': p['id'], 'title': p['title'], 'category': cat, 'reason': r} for p, cat, r in skipped],
        }, f, indent=2)

    print(f'\nPreview written to html-cleanup-preview.html ({len(samples)} samples)')
    print('Results saved to html-cleanup-results.json')
    print('DRY RUN — nothing written to Shopify')


if __name__ == '__main__':
    main()
