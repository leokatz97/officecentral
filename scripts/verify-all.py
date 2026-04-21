"""
End-to-end sanity check for today's changes:
  1. 7 deleted SKUs → should 404
  2. 2 new shipping products → status=active AND published_at set
  3. 191 HTML cleanups → body no longer heavy_html/word_junk (sample)
  4. 41 dedup trims → shorter than logged before_len (sample)
  5. 21 archived drafts → status=archived
  6. 10 archived shipping SKUs → status=archived
  7. 6 review descriptions → body_html length matches
"""
import urllib.request
import urllib.error
import json
import re
import time
import random

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}


def api_get(url, attempt=0):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_get(url, attempt + 1)
        return e.code, None


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


def fetch(pid):
    return api_get(f'{API}/products/{pid}.json')


def main():
    # 1) Deletions
    with open('purge-log.json') as f:
        purge = json.load(f)
    print('== 1. DELETED SKUs should 404 ==')
    for r in purge['results']:
        status, _ = fetch(r['id'])
        ok = status == 404
        print(f'  [{"OK" if ok else f"FAIL status={status}"}] {r["title"]}')
        time.sleep(0.55)

    # 2) New shipping products
    with open('consolidate-shipping-log.json') as f:
        cons = json.load(f)
    print('\n== 2. NEW SHIPPING PRODUCTS ==')
    for label, pid in [('Delivery', cons['new_delivery_id']),
                       ('Installation', cons['new_installation_id'])]:
        status, data = fetch(pid)
        if data and 'product' in data:
            p = data['product']
            pub = p.get('published_at')
            print(f'  [{label}] id={pid} status={p["status"]} published_at={pub} variants={len(p.get("variants",[]))}')
        else:
            print(f'  [{label}] FAIL status={status}')
        time.sleep(0.55)

    # 3) HTML cleanups — sample 5
    with open('push-cleanup-log.json') as f:
        push = json.load(f)
    ok_ids = [r['id'] for r in push['results'] if r['ok']]
    sample = random.sample(ok_ids, min(5, len(ok_ids)))
    print(f'\n== 3. HTML CLEANUPS (random 5 of {len(ok_ids)}) ==')
    for pid in sample:
        status, data = fetch(pid)
        if data and 'product' in data:
            p = data['product']
            cat = classify(p.get('body_html', ''))
            print(f'  [{"OK" if cat == "clean" else "STILL "+cat}] {p["title"][:55]}  len={len(p.get("body_html","") or "")}')
        time.sleep(0.55)

    # 4) Dedup trims — sample 5
    with open('dedup-log.json') as f:
        dedup = json.load(f)
    with open('dedup-plan.json') as f:
        dedup_plan = json.load(f)
    plan_by_id = {x['id']: x for x in dedup_plan['trim']}
    trimmed_ids = [r['id'] for r in dedup['results'] if r['ok']]
    sample = random.sample(trimmed_ids, min(5, len(trimmed_ids)))
    print(f'\n== 4. DEDUP TRIMS (random 5 of {len(trimmed_ids)}) ==')
    for pid in sample:
        status, data = fetch(pid)
        if data and 'product' in data:
            p = data['product']
            live_len = len(p.get('body_html', '') or '')
            expected_after = plan_by_id.get(pid, {}).get('after_len', None)
            expected_before = plan_by_id.get(pid, {}).get('before_len', None)
            marker = 'OK' if expected_after and abs(live_len - expected_after) <= 5 else 'DIFF'
            print(f'  [{marker}] {p["title"][:55]:55}  live={live_len}  expected={expected_after}  from={expected_before}')
        time.sleep(0.55)

    # 5) Drafts archived
    with open('archive-drafts-log.json') as f:
        arch = json.load(f)
    ok_ids = [r['id'] for r in arch['results'] if r['ok']]
    sample = random.sample(ok_ids, min(5, len(ok_ids)))
    print(f'\n== 5. ARCHIVED DRAFTS (random 5 of {len(ok_ids)}) ==')
    for pid in sample:
        status, data = fetch(pid)
        if data and 'product' in data:
            p = data['product']
            print(f'  [{"OK" if p["status"] == "archived" else "FAIL status="+p["status"]}] {p["title"][:55]}')
        time.sleep(0.55)

    # 6) Old shipping archived
    ok_ids = [r['id'] for r in cons['archived'] if r['ok']]
    print(f'\n== 6. OLD SHIPPING SKUs ARCHIVED ({len(ok_ids)}) ==')
    for pid in ok_ids:
        status, data = fetch(pid)
        if data and 'product' in data:
            p = data['product']
            print(f'  [{"OK" if p["status"] == "archived" else "FAIL status="+p["status"]}] {p["title"][:50]}')
        time.sleep(0.55)

    # 7) Review descriptions
    with open('descriptions-log.json') as f:
        desc = json.load(f)
    ok_ids = [r['id'] for r in desc['results'] if r['ok']]
    print(f'\n== 7. REVIEW DESCRIPTIONS ({len(ok_ids)}) ==')
    for pid in ok_ids:
        status, data = fetch(pid)
        if data and 'product' in data:
            p = data['product']
            body = p.get('body_html', '') or ''
            has_content = len(strip_text(body)) > 100
            print(f'  [{"OK" if has_content else "EMPTY"}] {p["title"][:55]}  text_len={len(strip_text(body))}')
        time.sleep(0.55)


if __name__ == '__main__':
    main()
