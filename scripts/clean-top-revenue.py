"""
DRY-RUN cleaner for top-revenue Brant Business Interiors product descriptions.

Pareto focus: merges sales-report.json (top_products, by revenue) with
top-sellers.json (top_list, by units), dedupes by product_id, re-ranks by revenue,
takes top N, fetches body_html from Shopify, and cleans the messy inline styles
and wrapper divs. Skips products already classified 'clean' in top-sellers.json
so we don't touch what doesn't need touching.

Writes html-preview.html with a before/after side-by-side for review.
Does NOT push to Shopify. Approve the preview, then run push phase separately.
"""

import html as html_lib
import json
import re
import urllib.request
from bs4 import BeautifulSoup

TOP_N = 50
PREVIEW_PATH = 'html-preview.html'
RESULTS_PATH = 'clean-top-revenue-results.json'
PAYLOAD_PATH = 'clean-top-revenue-payload.json'

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'

ALLOWED_TAGS = {'p', 'ul', 'ol', 'li', 'strong', 'b', 'em', 'i', 'br',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
STRUCTURAL_TAGS = {'div', 'section', 'table', 'tbody', 'tr', 'td', 'thead',
                   'tfoot', 'th', 'article', 'aside', 'header', 'footer',
                   'main', 'nav', 'figure', 'figcaption'}
HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def fetch_product(pid):
    url = f'{API}/products/{pid}.json?fields=id,title,handle,body_html'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product']


def strip_text(html):
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = text.replace('&nbsp;', ' ').replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def classify(html):
    if not html or not html.strip():
        return 'empty'
    text = strip_text(html)
    if len(text) < 20:
        return 'empty'
    if 'mso-' in html or 'MsoNormal' in html or 'font-family:' in html:
        return 'word_junk'
    tag_density = len(re.findall(r'<[^>]+>', html)) / max(len(text.split()), 1)
    if tag_density > 0.5:
        return 'heavy_html'
    return 'clean'


def is_empty(tag):
    if tag.name == 'br':
        return False
    if tag.find('img'):
        return False
    text = tag.get_text().replace('\xa0', '').replace('&nbsp;', '').strip()
    return not text


def clean_html(raw):
    if not raw:
        return ''
    soup = BeautifulSoup(raw, 'lxml')
    if soup.body:
        soup = BeautifulSoup(''.join(str(c) for c in soup.body.contents), 'lxml')
    root = soup.body if soup.body else soup

    for t in root.find_all(['script', 'style', 'meta', 'link', 'form',
                            'input', 'button', 'iframe']):
        t.decompose()

    for t in list(root.find_all(True)):
        if t.name in ALLOWED_TAGS or t.name in STRUCTURAL_TAGS or t.name in {'img', 'a', 'span'}:
            continue
        t.unwrap()

    for t in list(root.find_all(STRUCTURAL_TAGS)):
        t.unwrap()

    for t in list(root.find_all('span')):
        t.unwrap()

    for t in list(root.find_all(True)):
        if t.name == 'a':
            href = t.get('href')
            t.attrs = {'href': href} if href else {}
        elif t.name == 'img':
            src = t.get('src')
            alt = t.get('alt', '')
            t.attrs = {'src': src, 'alt': alt} if src else {}
        else:
            t.attrs = {}

    empty_check_tags = HEADING_TAGS | {'p', 'li', 'strong', 'b', 'em', 'i'}
    for _ in range(5):
        removed = False
        for t in list(root.find_all(True)):
            if t.name in empty_check_tags and is_empty(t):
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


def build_candidate_list():
    with open('sales-report.json') as f:
        sales = json.load(f)
    with open('top-sellers.json') as f:
        sellers = json.load(f)

    merged = {}

    for p in sales['top_products']:
        pid = p.get('id')
        if not pid:
            continue
        cur = merged.get(pid, {'revenue': 0.0, 'title': p['title'], 'handle': None, 'html_category': None})
        cur['revenue'] += p.get('revenue', 0.0)
        merged[pid] = cur

    for p in sellers['top_list']:
        pid = p.get('product_id')
        if not pid:
            continue
        cur = merged.get(pid, {'revenue': 0.0, 'title': p['title'], 'handle': p.get('handle'), 'html_category': p.get('html_category')})
        cur['revenue'] = max(cur['revenue'], p.get('revenue', 0.0))
        if p.get('handle') and not cur.get('handle'):
            cur['handle'] = p['handle']
        if p.get('html_category'):
            cur['html_category'] = p['html_category']
        merged[pid] = cur

    ranked = sorted(
        ({'id': pid, **info} for pid, info in merged.items()),
        key=lambda r: r['revenue'],
        reverse=True,
    )
    return ranked[:TOP_N]


def main():
    candidates = build_candidate_list()
    print(f'Top {len(candidates)} candidates by revenue (after merge + dedupe)')
    total_rev = sum(c['revenue'] for c in candidates)
    print(f'Combined revenue of candidate set: ${total_rev:,.2f}')

    results = []
    skipped_clean = []
    skipped_empty = []
    errors = []

    for i, c in enumerate(candidates, 1):
        pid = c['id']
        pre_class = c.get('html_category')
        if pre_class == 'clean':
            skipped_clean.append(c)
            print(f'  [{i:>2}] SKIP (already clean): {c["title"][:60]}')
            continue

        try:
            prod = fetch_product(pid)
        except Exception as e:
            errors.append({'id': pid, 'title': c['title'], 'error': str(e)})
            print(f'  [{i:>2}] ERROR fetching {pid}: {e}')
            continue

        raw = prod.get('body_html') or ''
        cat = classify(raw)

        if cat == 'empty':
            skipped_empty.append({'id': pid, 'title': prod['title']})
            print(f'  [{i:>2}] SKIP (empty body_html): {prod["title"][:60]}')
            continue

        if cat == 'clean':
            skipped_clean.append({'id': pid, 'title': prod['title']})
            print(f'  [{i:>2}] SKIP (classified clean on fetch): {prod["title"][:60]}')
            continue

        cleaned = clean_html(raw)
        before_text = strip_text(raw)
        after_text = strip_text(cleaned)
        text_loss_pct = (1 - len(after_text) / max(len(before_text), 1)) * 100

        results.append({
            'id': pid,
            'title': prod['title'],
            'handle': prod.get('handle'),
            'revenue': c['revenue'],
            'category': cat,
            'before': raw,
            'after': cleaned,
            'before_len': len(raw),
            'after_len': len(cleaned),
            'before_text_len': len(before_text),
            'after_text_len': len(after_text),
            'text_loss_pct': text_loss_pct,
        })
        flag = ''
        if text_loss_pct > 20:
            flag = '  !! TEXT LOSS'
        print(f'  [{i:>2}] {cat:<11} {len(raw):>6} -> {len(cleaned):>6} chars '
              f'({text_loss_pct:>5.1f}% text loss) {prod["title"][:50]}{flag}')

    print()
    print(f'Cleaned: {len(results)}')
    print(f'Skipped (already clean): {len(skipped_clean)}')
    print(f'Skipped (empty): {len(skipped_empty)}')
    print(f'Errors: {len(errors)}')

    write_preview(results, skipped_clean, skipped_empty, errors, total_rev, len(candidates))

    with open(RESULTS_PATH, 'w') as f:
        json.dump({
            'candidate_count': len(candidates),
            'candidate_revenue': total_rev,
            'cleaned_count': len(results),
            'skipped_clean_count': len(skipped_clean),
            'skipped_empty_count': len(skipped_empty),
            'error_count': len(errors),
            'cleaned_ids': [r['id'] for r in results],
            'skipped_clean_ids': [s.get('id') for s in skipped_clean],
            'errors': errors,
            'questionable': [
                {'id': r['id'], 'title': r['title'], 'text_loss_pct': r['text_loss_pct']}
                for r in results if r['text_loss_pct'] > 20
            ],
        }, f, indent=2)

    with open(PAYLOAD_PATH, 'w') as f:
        json.dump([
            {
                'id': r['id'],
                'title': r['title'],
                'handle': r['handle'],
                'revenue': r['revenue'],
                'category': r['category'],
                'before': r['before'],
                'after': r['after'],
            }
            for r in results
        ], f, indent=2)

    print(f'\nPreview: {PREVIEW_PATH}')
    print(f'Results: {RESULTS_PATH}')
    print(f'Payload: {PAYLOAD_PATH}')
    print('DRY RUN — nothing written to Shopify')


def write_preview(results, skipped_clean, skipped_empty, errors, total_rev, candidate_count):
    parts = ['''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Top-Revenue HTML Cleanup Preview</title>
<style>
body { font-family: -apple-system, sans-serif; max-width: 1500px; margin: 20px auto; padding: 0 20px; color: #222; }
h1 { margin-bottom: 6px; }
.summary { background: #f4f4f4; padding: 16px; border-radius: 6px; margin: 16px 0 32px; line-height: 1.6; }
.summary strong { color: #000; }
h2 { color: #333; border-bottom: 2px solid #ddd; padding-bottom: 6px; margin-top: 44px; font-size: 18px; }
.meta { font-size: 12px; color: #666; margin-bottom: 8px; }
.cat { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-left: 6px; }
.cat.word_junk { background: #ffe8b3; color: #6a4500; }
.cat.heavy_html { background: #cce7ff; color: #003a6a; }
.cat.clean { background: #d4f5d4; color: #1a5a1a; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 18px; }
.col { border: 1px solid #ccc; border-radius: 6px; padding: 14px; overflow: auto; max-height: 520px; background: #fff; }
.col.before { background: #fff7f7; }
.col.after { background: #f3fff3; }
.col h3 { margin-top: 0; font-size: 12px; text-transform: uppercase; color: #666; letter-spacing: 0.5px; }
.rendered { border-top: 1px dashed #aaa; margin-top: 10px; padding-top: 10px; font-size: 14px; line-height: 1.5; }
.rendered img { max-width: 100%; }
pre { white-space: pre-wrap; word-break: break-all; font-size: 10.5px; background: #fafafa; padding: 8px; border-radius: 4px; max-height: 200px; overflow: auto; margin-top: 10px; }
.flag { display: inline-block; margin-left: 8px; padding: 2px 6px; border-radius: 3px; background: #ffdddd; color: #a00000; font-size: 11px; font-weight: bold; }
.skip-list { font-size: 13px; color: #555; }
.skip-list li { margin-bottom: 3px; }
</style></head><body>''']
    parts.append(f'<h1>Top-Revenue HTML Cleanup — DRY RUN</h1>')
    questionable = [r for r in results if r['text_loss_pct'] > 20]
    parts.append(f'''<div class="summary">
<strong>Candidate set:</strong> Top {candidate_count} products by merged revenue (sales-report + top-sellers, deduped) — combined revenue ${total_rev:,.2f}<br>
<strong>Cleaned in this preview:</strong> {len(results)} products<br>
<strong>Skipped (already clean):</strong> {len(skipped_clean)}<br>
<strong>Skipped (empty body):</strong> {len(skipped_empty)}<br>
<strong>Fetch errors:</strong> {len(errors)}<br>
<strong>Flagged for review (text loss &gt; 20%):</strong> {len(questionable)}<br>
<strong>Mode:</strong> DRY RUN — no writes to Shopify yet.
</div>''')

    if questionable:
        parts.append('<h2>⚠ Products with &gt;20% text loss — review these first</h2><ul class="skip-list">')
        for r in questionable:
            parts.append(f'<li>{html_lib.escape(r["title"])} — {r["text_loss_pct"]:.1f}% text loss (id {r["id"]})</li>')
        parts.append('</ul>')

    for r in sorted(results, key=lambda x: x['revenue'], reverse=True):
        shrink = (1 - r['after_len'] / max(r['before_len'], 1)) * 100
        flag = ' <span class="flag">TEXT LOSS</span>' if r['text_loss_pct'] > 20 else ''
        parts.append(f'''<h2>{html_lib.escape(r["title"])}
<span class="cat {r["category"]}">{r["category"]}</span>{flag}</h2>
<div class="meta">id {r["id"]} · handle {r["handle"]} · revenue ${r["revenue"]:,.2f} ·
markup {r["before_len"]:,} → {r["after_len"]:,} chars ({shrink:.0f}% smaller) ·
text {r["before_text_len"]:,} → {r["after_text_len"]:,} chars ({r["text_loss_pct"]:.1f}% loss)</div>
<div class="pair">
  <div class="col before">
    <h3>Before</h3>
    <div class="rendered">{r["before"]}</div>
    <pre>{html_lib.escape(r["before"])}</pre>
  </div>
  <div class="col after">
    <h3>After</h3>
    <div class="rendered">{r["after"]}</div>
    <pre>{html_lib.escape(r["after"])}</pre>
  </div>
</div>''')

    if skipped_clean:
        parts.append('<h2>Skipped — already clean</h2><ul class="skip-list">')
        for s in skipped_clean:
            parts.append(f'<li>{html_lib.escape(s.get("title", ""))}</li>')
        parts.append('</ul>')

    if skipped_empty:
        parts.append('<h2>Skipped — empty body_html</h2><ul class="skip-list">')
        for s in skipped_empty:
            parts.append(f'<li>{html_lib.escape(s.get("title", ""))} (id {s["id"]})</li>')
        parts.append('</ul>')

    if errors:
        parts.append('<h2>Errors</h2><ul class="skip-list">')
        for e in errors:
            parts.append(f'<li>{html_lib.escape(e["title"])} (id {e["id"]}): {html_lib.escape(e["error"])}</li>')
        parts.append('</ul>')

    parts.append('</body></html>')
    with open(PREVIEW_PATH, 'w') as f:
        f.write('\n'.join(parts))


if __name__ == '__main__':
    main()
