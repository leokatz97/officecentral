"""
Verify whether the HTML cleanup (clean-html.py dry run) was actually
pushed to Shopify. For each id in html-cleanup-results.json, fetch the
current body_html and classify. Anything still heavy_html/word_junk
was never pushed.
"""
import urllib.request
import urllib.error
import json
import re
import time
from collections import Counter

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}


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


def fetch_product(pid, attempt=0):
    req = urllib.request.Request(
        f'{API}/products/{pid}.json?fields=id,title,body_html,handle',
        headers=HEADERS,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())['product']
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            wait = 2 ** attempt
            print(f'    429, backing off {wait}s')
            time.sleep(wait)
            return fetch_product(pid, attempt + 1)
        raise


def main():
    with open('html-cleanup-results.json') as f:
        results = json.load(f)
    cleaned_ids = results['cleaned_ids']
    print(f'Checking {len(cleaned_ids)} products that were "cleaned" in the dry run...\n')

    status = Counter()
    still_dirty = []
    sample = []
    for i, pid in enumerate(cleaned_ids, 1):
        p = fetch_product(pid)
        time.sleep(0.55)
        cat = classify(p.get('body_html', ''))
        status[cat] += 1
        if cat in ('heavy_html', 'word_junk'):
            still_dirty.append({'id': pid, 'title': p['title'], 'category': cat,
                                'len': len(p.get('body_html', ''))})
        if len(sample) < 3:
            sample.append({'id': pid, 'title': p['title'], 'category': cat,
                           'len': len(p.get('body_html', ''))})
        if i % 25 == 0:
            print(f'  {i}/{len(cleaned_ids)} checked')

    print('\n=== CURRENT STATE OF "CLEANED" PRODUCTS ===')
    for cat, n in status.most_common():
        print(f'  {cat:15} {n}')

    print(f'\nStill dirty: {len(still_dirty)} / {len(cleaned_ids)}')
    print('\n=== FIRST 3 SAMPLES ===')
    for s in sample:
        print(f'  [{s["category"]:11}] {s["title"][:55]:55}  live_len={s["len"]}')

    verdict = 'NOT PUSHED' if len(still_dirty) > len(cleaned_ids) * 0.8 else (
        'PARTIALLY PUSHED' if still_dirty else 'PUSHED')
    print(f'\nVERDICT: cleanup is {verdict}')

    with open('verify-cleanup-report.json', 'w') as f:
        json.dump({
            'checked': len(cleaned_ids),
            'status': dict(status),
            'still_dirty': still_dirty,
            'verdict': verdict,
        }, f, indent=2)
    print('\nWrote verify-cleanup-report.json')


if __name__ == '__main__':
    main()
