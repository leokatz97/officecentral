"""
Push the HTML cleanup to Shopify for real.

Fetches every product, runs the same cleaner as clean-html.py, and for
any product whose current body_html is heavy_html or word_junk, PUTs
the cleaned body back. Skips any product where cleaning would drop
>50% of the text (safety net).

Dry-run by default; pass --confirm to actually write.
"""
import urllib.request
import urllib.error
import json
import re
import sys
import time
import html as html_lib
from bs4 import BeautifulSoup

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

ALLOWED_TAGS = {'p', 'ul', 'ol', 'li', 'strong', 'b', 'em', 'i', 'br',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'}
HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


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

    for t in root.find_all(['script', 'style', 'meta', 'link', 'form',
                            'input', 'button', 'iframe', 'img']):
        t.decompose()

    for t in root.find_all(True):
        if t.name not in ALLOWED_TAGS and t.name not in {
            'div', 'section', 'table', 'tbody', 'tr', 'td', 'thead',
            'html', 'body', '[document]'}:
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


def api_get(url, attempt=0):
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req) as resp:
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            return json.loads(resp.read().decode()), (m.group(1) if m else None)
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            wait = 2 ** attempt
            print(f'    429 on GET, backing off {wait}s')
            time.sleep(wait)
            return api_get(url, attempt + 1)
        raise


def api_put(pid, body_html, attempt=0):
    payload = json.dumps({'product': {'id': pid, 'body_html': body_html}}).encode()
    req = urllib.request.Request(
        f'{API}/products/{pid}.json',
        data=payload,
        headers=HEADERS,
        method='PUT',
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            wait = 2 ** attempt
            print(f'    429 on PUT, backing off {wait}s')
            time.sleep(wait)
            return api_put(pid, body_html, attempt + 1)
        return e.code, e.read().decode()


def fetch_all_products():
    products = []
    url = f'{API}/products.json?limit=250&fields=id,title,body_html,handle'
    while url:
        data, next_url = api_get(url)
        products.extend(data['products'])
        print(f'  fetched {len(products)}')
        url = next_url
    return products


def main():
    confirm = '--confirm' in sys.argv
    print('Fetching all products...')
    products = fetch_all_products()
    print(f'\nTotal: {len(products)} products\n')

    plan = []
    for p in products:
        cat = classify(p.get('body_html', ''))
        if cat not in ('heavy_html', 'word_junk'):
            continue
        raw = p['body_html']
        cleaned = clean_html(raw)
        before_text = len(strip_text(raw))
        after_text = len(strip_text(cleaned))
        if after_text < max(10, before_text * 0.5):
            plan.append({'id': p['id'], 'title': p['title'], 'category': cat,
                         'status': 'skip_text_loss',
                         'before_text': before_text, 'after_text': after_text})
            continue
        if cleaned == raw:
            plan.append({'id': p['id'], 'title': p['title'], 'category': cat,
                         'status': 'skip_noop'})
            continue
        plan.append({'id': p['id'], 'title': p['title'], 'category': cat,
                     'status': 'will_push', 'cleaned': cleaned,
                     'before_len': len(raw), 'after_len': len(cleaned)})

    to_push = [x for x in plan if x['status'] == 'will_push']
    skipped = [x for x in plan if x['status'] != 'will_push']

    print(f'Will push: {len(to_push)}')
    print(f'Skipped:   {len(skipped)} ({sum(1 for x in skipped if x["status"] == "skip_text_loss")} text-loss, '
          f'{sum(1 for x in skipped if x["status"] == "skip_noop")} no-op)')

    if not confirm:
        print('\nSample (first 5):')
        for x in to_push[:5]:
            shrink = (1 - x['after_len'] / max(x['before_len'], 1)) * 100
            print(f'  {x["title"][:55]:55}  {x["before_len"]}→{x["after_len"]} ({shrink:.0f}% smaller)')
        print(f'\nDRY RUN. Pass --confirm to push {len(to_push)} updates.')
        return

    print(f'\nPushing {len(to_push)} updates...')
    results = []
    for i, x in enumerate(to_push, 1):
        status, body = api_put(x['id'], x['cleaned'])
        ok = status in (200, 201)
        results.append({'id': x['id'], 'title': x['title'], 'status': status,
                        'ok': ok, 'body': body[:200] if not ok else ''})
        if not ok:
            print(f'  [FAIL {status}] {x["title"][:55]}')
        if i % 25 == 0:
            succeeded = sum(1 for r in results if r['ok'])
            print(f'  {i}/{len(to_push)}  ({succeeded} ok)')
        time.sleep(0.55)

    succeeded = sum(1 for r in results if r['ok'])
    with open('push-cleanup-log.json', 'w') as f:
        json.dump({
            'confirmed': True,
            'attempted': len(results),
            'succeeded': succeeded,
            'failed': len(results) - succeeded,
            'results': results,
            'skipped': skipped,
        }, f, indent=2)
    print(f'\nDone: {succeeded}/{len(results)} pushed. Log: push-cleanup-log.json')


if __name__ == '__main__':
    main()
