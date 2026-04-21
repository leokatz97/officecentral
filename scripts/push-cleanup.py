"""
Push cleaned HTML for the top-seller products flagged as heavy_html/word_junk.

Usage:
  python3 push-cleanup.py            # dry run: preview only, no writes
  python3 push-cleanup.py --push     # writes to Shopify (after preview regen)
"""
import sys
import urllib.request
import urllib.error
import json
import re
import time
import html as html_lib
from bs4 import BeautifulSoup

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'

ALLOWED_TAGS = {'p', 'ul', 'ol', 'li', 'strong', 'b', 'em', 'i', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'}
HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def fetch_product(pid):
    url = f'{API}/products/{pid}.json?fields=id,title,handle,body_html'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product']


def put_product(pid, body_html):
    url = f'{API}/products/{pid}.json'
    payload = json.dumps({'product': {'id': pid, 'body_html': body_html}}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
        method='PUT',
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status


def strip_text(html):
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


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
        root = soup.body if soup.body else soup
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


def build_preview(items):
    parts = ['''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Push Cleanup Preview — Top 15</title>
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
</style></head><body>''']
    parts.append(f'<h1>Push Cleanup Preview — {len(items)} top-seller products</h1>')
    parts.append(f'''<div class="summary">
<strong>Products:</strong> {len(items)}<br>
<strong>Status:</strong> PREVIEW — run with <code>--push</code> to apply<br>
<strong>Store:</strong> {STORE}
</div>''')
    for s in items:
        shrink = (1 - len(s['after']) / max(len(s['before']), 1)) * 100
        parts.append(f'''<h2>#{s["rank"]} · {s["units_sold"]} units · {html_lib.escape(s["title"])}</h2>
<div class="meta">ID: {s["id"]} · handle: {s["handle"]} · {len(s["before"])} → {len(s["after"])} chars ({shrink:.0f}% smaller)</div>
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
    parts.append('</body></html>')
    return '\n'.join(parts)


def main():
    push_mode = '--push' in sys.argv

    with open('top-sellers.json') as f:
        data = json.load(f)

    cleanup_pids = data['cleanup_pids']
    rank_by_pid = {r['product_id']: (r['units_sold'], r['title'], data['top_list'].index(r) + 1)
                   for r in data['top_list']}
    print(f'Cleanup candidates: {len(cleanup_pids)} products\n')

    items = []
    for pid in cleanup_pids:
        p = fetch_product(pid)
        before = p['body_html'] or ''
        after = clean_html(before)
        before_text = len(strip_text(before))
        after_text = len(strip_text(after))
        guard_pass = after_text >= max(10, before_text * 0.5)
        units, title, rank = rank_by_pid[pid]
        items.append({
            'id': pid,
            'rank': rank,
            'units_sold': units,
            'title': p['title'],
            'handle': p['handle'],
            'before': before,
            'after': after,
            'before_text_len': before_text,
            'after_text_len': after_text,
            'guard_pass': guard_pass,
        })
        status = 'OK' if guard_pass else 'SKIP (text loss)'
        print(f'  #{rank:>2} [{status:<16}] {len(before):>5} → {len(after):>5} chars | {title[:55]}')

    writable = [i for i in items if i['guard_pass']]
    skipped = [i for i in items if not i['guard_pass']]
    print(f'\nPass guard: {len(writable)} | Skip: {len(skipped)}')

    with open('push-preview.html', 'w') as f:
        f.write(build_preview(items))
    print('\nPreview written to push-preview.html')

    if not push_mode:
        print('\n[DRY RUN] Review push-preview.html, then re-run with --push to write.')
        return

    print(f'\n>>> PUSHING {len(writable)} products to Shopify...')
    results = []
    for i, item in enumerate(writable, 1):
        try:
            status = put_product(item['id'], item['after'])
            print(f'  [{i}/{len(writable)}] {status} · {item["title"][:55]}')
            results.append({'id': item['id'], 'title': item['title'], 'status': status, 'ok': True})
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            print(f'  [{i}/{len(writable)}] ERROR {e.code}: {body} · {item["title"][:55]}')
            results.append({'id': item['id'], 'title': item['title'], 'error': f'{e.code} {body}', 'ok': False})
        except Exception as e:
            print(f'  [{i}/{len(writable)}] ERROR: {e} · {item["title"][:55]}')
            results.append({'id': item['id'], 'title': item['title'], 'error': str(e), 'ok': False})
        time.sleep(0.6)

    ok = sum(1 for r in results if r['ok'])
    print(f'\nDone. {ok}/{len(writable)} updated.')
    with open('push-cleanup-results.json', 'w') as f:
        json.dump({
            'pushed': len(writable),
            'ok': ok,
            'skipped_guard': [{'id': s['id'], 'title': s['title']} for s in skipped],
            'results': results,
        }, f, indent=2)
    print('Results saved to push-cleanup-results.json')


if __name__ == '__main__':
    main()
