#!/usr/bin/env python3
"""Independent Admin-API readback verifier for Track C batch-2 drafts.
Fresh GET (never the mutation echo). Verifies:
  - publishedAt is null (DRAFT)
  - global.title_tag == PACK title (byte-for-byte)
  - global.description_tag == PACK meta_description (byte-for-byte)
  - faq.items metafield present AND byte-matches the visible FAQ block
  - body landed (non-empty), engine interlink anchors present,
    no raw <a> the engine did not insert
Usage: _trackc_readback.py <article_id> <pack.json>
Exit 0 = all PASS, 1 = any FAIL.
"""
import os, sys, json, urllib.request
from bs4 import BeautifulSoup

STORE = 'office-central-online.myshopify.com'; API = '2026-04'

def _load_env():
    if os.path.exists('.env'):
        for line in open('.env'):
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k, v.strip().strip('"').strip("'"))
_load_env()

def api(path):
    tok = os.environ['SHOPIFY_TOKEN']
    req = urllib.request.Request(f'https://{STORE}/admin/api/{API}/{path}',
                                 headers={'X-Shopify-Access-Token': tok})
    return json.load(urllib.request.urlopen(req))

def pairs_from_items(items):
    return [(it.split('||', 1)[0].strip(), it.split('||', 1)[1].strip()) for it in items]

def parse_visible_faq(body):
    soup = BeautifulSoup(body, 'html.parser')
    out = []
    for item in soup.select('.bbi-faq__item'):
        for tag in item.select('.bbi-faq__tag'):
            tag.decompose()
        q = item.select_one('.bbi-faq__q strong')
        a = item.select_one('.bbi-faq__a')
        out.append(((q.get_text() if q else '').strip(), (a.get_text() if a else '').strip()))
    return out

aid = sys.argv[1]
spec = json.load(open(sys.argv[2]))
blog = spec['blog_id']

art = api(f"blogs/{blog}/articles/{aid}.json")['article']
mfs = api(f"blogs/{blog}/articles/{aid}/metafields.json")['metafields']
def mf(ns, key):
    m = [x for x in mfs if x['namespace'] == ns and x['key'] == key]
    return m[0]['value'] if m else None

results = []

# 1. publishedAt null
pub = art.get('published_at')
results.append(('publishedAt is null (DRAFT)', pub is None, f"published_at={pub!r}"))

# 2. title_tag byte-for-byte
tt = mf('global', 'title_tag')
results.append(('global.title_tag == PACK title', tt == spec['title'],
                f"len {len(tt) if tt else 0}; got={tt!r}"))

# 3. description_tag byte-for-byte
dt = mf('global', 'description_tag')
results.append(('global.description_tag == PACK meta', dt == spec['meta_description'],
                f"len {len(dt) if dt else 0}; got={dt!r}"))

# 4. faq.items present + byte-match visible
fi = mf('faq', 'items')
if fi is None:
    results.append(('faq.items present', False, 'missing'))
else:
    canon = pairs_from_items(json.loads(fi))
    visible = parse_visible_faq(art['body_html'])
    bm = (len(visible) == len(canon)) and all(v == c for v, c in zip(visible, canon))
    results.append((f'faq.items byte-match visible ({len(canon)} pairs)', bm,
                    f"visible={len(visible)} canon={len(canon)}"))

# 5. body landed + anchors + no stray <a>
body = art['body_html'] or ''
nonempty = len(body) > 500
results.append(('body landed (non-empty)', nonempty, f"len={len(body)}"))

# engine interlink anchors: each replacement (rep, 2nd elem) must be present
inter = spec.get('interlinks', [])
missing = [lk[2] for lk in inter if lk[1] not in body]
results.append((f'all {len(inter)} engine anchors present', not missing,
                f"missing={missing}"))

# no raw <a> beyond the ones the engine inserted
inserted_hrefs = []
for lk in inter:
    soup = BeautifulSoup(lk[1], 'html.parser')
    for a in soup.find_all('a'):
        if a.get('href'):
            inserted_hrefs.append(a['href'])
body_soup = BeautifulSoup(body, 'html.parser')
all_hrefs = [a.get('href') for a in body_soup.find_all('a') if a.get('href')]
stray = [h for h in all_hrefs if h not in inserted_hrefs]
results.append((f'no stray <a> ({len(all_hrefs)} total, {len(inserted_hrefs)} engine)',
                not stray, f"stray={stray[:5]}"))

allok = all(ok for _, ok, _ in results)
print(f"READBACK article {aid} (handle={art['handle']}):")
for name, ok, detail in results:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} -- {detail}")
print('  RESULT:', 'PASS' if allok else 'FAIL')
sys.exit(0 if allok else 1)
