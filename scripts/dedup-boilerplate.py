"""
Detect and dedupe boilerplate content across product descriptions.

Approach:
  1. Fetch all products, strip HTML to normalized text.
  2. Cluster products whose descriptions share a >=200-char opening
     (matches the pattern seen in audit-report.json).
  3. For each cluster of 3+ products, compute the longest common
     shared blob across all members.
  4. Strip the shared blob from every member (keep what's unique).
  5. If a product's remaining unique text is <20 chars, fall back to
     leaving it alone and flag it for manual description writing.

Dry-run by default; pass --confirm to push.
"""
import urllib.request
import urllib.error
import json
import re
import sys
import time
import html as html_lib
from collections import defaultdict

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}


def strip_text(html):
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    text = html_lib.unescape(text)
    return re.sub(r'\s+', ' ', text).strip().lower()


def api_get(url, attempt=0):
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req) as resp:
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            return json.loads(resp.read().decode()), (m.group(1) if m else None)
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_get(url, attempt + 1)
        raise


def api_put(pid, body_html, attempt=0):
    payload = json.dumps({'product': {'id': pid, 'body_html': body_html}}).encode()
    req = urllib.request.Request(f'{API}/products/{pid}.json', data=payload, headers=HEADERS, method='PUT')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_put(pid, body_html, attempt + 1)
        return e.code, e.read().decode()


def fetch_all():
    products = []
    url = f'{API}/products.json?limit=250&fields=id,title,body_html,handle'
    while url:
        data, next_url = api_get(url)
        products.extend(data['products'])
        print(f'  fetched {len(products)}')
        url = next_url
    return products


def longest_common_prefix(strings):
    if not strings:
        return ''
    shortest = min(strings, key=len)
    for i, ch in enumerate(shortest):
        if any(s[i] != ch for s in strings):
            return shortest[:i]
    return shortest


def normalize_html(html):
    """Collapse whitespace so prefix matching is stable."""
    html = re.sub(r'\s+', ' ', html or '').strip()
    return html


def strip_prefix_html(body_html, shared_text_lower):
    """Strip a leading text run from body_html whose plain-text form matches shared_text_lower.

    Walks forward through the html, accumulating plain-text characters, and
    cuts at the html offset where the plain-text run has consumed len(shared_text_lower)
    characters that match the prefix.
    """
    target_len = len(shared_text_lower)
    consumed = 0
    i = 0
    inside_tag = False
    cut_at = None
    txt_buffer = []
    while i < len(body_html) and consumed < target_len:
        c = body_html[i]
        if c == '<':
            inside_tag = True
        elif c == '>':
            inside_tag = False
        elif not inside_tag:
            if c == '&':
                m = re.match(r'&[a-zA-Z#0-9]+;', body_html[i:])
                if m:
                    entity = html_lib.unescape(m.group())
                    for ec in entity:
                        el = ec.lower()
                        if consumed < target_len and el == shared_text_lower[consumed]:
                            consumed += 1
                            txt_buffer.append(ec)
                        elif consumed < target_len and el.isspace() and shared_text_lower[consumed] == ' ':
                            consumed += 1
                    i += len(m.group())
                    continue
            cl = c.lower()
            if cl.isspace():
                if consumed < target_len and shared_text_lower[consumed] == ' ':
                    if not txt_buffer or not txt_buffer[-1].isspace():
                        consumed += 1
                        txt_buffer.append(' ')
            elif consumed < target_len and cl == shared_text_lower[consumed]:
                consumed += 1
                txt_buffer.append(c)
            else:
                return None
        i += 1
    if consumed < target_len:
        return None
    cut_at = i
    remainder = body_html[cut_at:]
    remainder = re.sub(r'^(\s*<(p|ul|ol|li|br|h[1-6])[^>]*>\s*)*', '', remainder)
    remainder = remainder.strip()
    return remainder


def main():
    confirm = '--confirm' in sys.argv
    min_shared_chars = 200
    cluster_key_chars = 200

    print('Fetching all products...')
    products = fetch_all()
    print(f'\nTotal: {len(products)}\n')

    keyed = defaultdict(list)
    for p in products:
        text = strip_text(p.get('body_html', ''))
        if len(text) < min_shared_chars:
            continue
        key = text[:cluster_key_chars]
        keyed[key].append({'id': p['id'], 'title': p['title'], 'text': text,
                           'html': p.get('body_html', '') or ''})

    clusters = [v for v in keyed.values() if len(v) >= 2]
    print(f'Clusters with shared prefix >= {cluster_key_chars} chars: {len(clusters)}')
    print(f'Total products in clusters: {sum(len(c) for c in clusters)}\n')

    plan = []
    manual_needed = []
    for cluster in sorted(clusters, key=lambda c: -len(c)):
        texts = [m['text'] for m in cluster]
        shared = longest_common_prefix(texts)
        shared = shared.rstrip()
        if len(shared) < min_shared_chars:
            continue
        shared_preview = shared[:80] + ('...' if len(shared) > 80 else '')
        print(f'[CLUSTER x{len(cluster)}] shared={len(shared)} chars  "{shared_preview}"')
        for m in cluster:
            unique_tail = m['text'][len(shared):].strip()
            new_html = strip_prefix_html(m['html'], shared)
            if new_html is None:
                manual_needed.append({'id': m['id'], 'title': m['title'],
                                      'reason': 'could not locate shared prefix in html'})
                print(f'    [MANUAL] {m["title"][:55]}  — prefix anchor missing')
                continue
            if len(strip_text(new_html)) < 20:
                manual_needed.append({'id': m['id'], 'title': m['title'],
                                      'reason': f'remainder too short ({len(strip_text(new_html))} chars) — entirely boilerplate'})
                print(f'    [MANUAL] {m["title"][:55]}  — all boilerplate, no unique tail')
                continue
            plan.append({
                'id': m['id'], 'title': m['title'],
                'before_len': len(m['html']), 'after_len': len(new_html),
                'new_html': new_html,
            })
            print(f'    [TRIM]   {m["title"][:55]:55}  {len(m["html"])}→{len(new_html)}')

    print(f'\n=== PLAN ===')
    print(f'  trim:   {len(plan)}')
    print(f'  manual: {len(manual_needed)}')

    with open('dedup-plan.json', 'w') as f:
        json.dump({
            'clusters': len(clusters),
            'trim': [{'id': x['id'], 'title': x['title'],
                      'before_len': x['before_len'], 'after_len': x['after_len']} for x in plan],
            'manual_needed': manual_needed,
        }, f, indent=2)
    print('\nWrote dedup-plan.json')

    if not confirm:
        print('\nDRY RUN. Pass --confirm to push trims.')
        return

    print(f'\nPushing {len(plan)} trims...')
    results = []
    for i, x in enumerate(plan, 1):
        status, body = api_put(x['id'], x['new_html'])
        ok = status in (200, 201)
        results.append({'id': x['id'], 'title': x['title'], 'status': status, 'ok': ok})
        if not ok:
            print(f'  [FAIL {status}] {x["title"][:55]}')
        if i % 25 == 0:
            print(f'  {i}/{len(plan)} ({sum(1 for r in results if r["ok"])} ok)')
        time.sleep(0.55)

    succeeded = sum(1 for r in results if r['ok'])
    with open('dedup-log.json', 'w') as f:
        json.dump({'attempted': len(results), 'succeeded': succeeded, 'results': results,
                   'manual_needed': manual_needed}, f, indent=2)
    print(f'\nDone: {succeeded}/{len(results)} trimmed.')


if __name__ == '__main__':
    main()
