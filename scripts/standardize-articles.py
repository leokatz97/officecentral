#!/usr/bin/env python3
"""Standardize the 2 live blog posts — FAQ reformat + product interlinks.
Dry-run by default; pass --live to PUT. Byte-match guard on faq.items is enforced
before any write and re-verified on readback.
"""
import os, json, re, sys, difflib, datetime
import urllib.request
from bs4 import BeautifulSoup

# ---- env / api ----
for line in open(os.path.join(os.path.dirname(__file__), '..', '.env')):
    line = line.strip()
    if line and '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
API = '2026-04'
BLOG = '108557861177'

def api(path, method='GET', payload=None):
    url = f'https://{STORE}/admin/api/{API}/{path}'
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

# ---- per-article config ----
ARTS = {
    'oecm-cornerstone': {
        'id': '689003888953',
        'faq_h2_old': 'Common Questions Ontario School Boards Ask',
        'links': [
            # (find, replace, label) — find must occur exactly once
            ('Old task chairs fail',
             'Old <a href="/collections/task-chairs">task chairs</a> fail',
             'task-chairs'),
            ('<strong>Tables</strong> (boardroom, training, café, occasional)',
             '<strong><a href="/collections/tables">Tables</a></strong> (boardroom, training, café, occasional)',
             'tables'),
            ('<strong>Storage &amp; filing</strong> (lateral, vertical, mobile)',
             '<strong><a href="/collections/storage">Storage &amp; filing</a></strong> (lateral, vertical, mobile)',
             'storage'),
            ('<strong>Panels &amp; dividers</strong> (acoustic + visual)',
             '<strong><a href="/collections/panels-dividers">Panels &amp; dividers</a></strong> (acoustic + visual)',
             'panels-dividers'),
        ],
    },
    'office-layout-pillar': {
        'id': '689229365561',
        'faq_h2_old': 'Common Questions',
        'links': [
            ('<td>Benching, shared workstations, acoustic pods</td>',
             '<td><a href="/collections/benching-desks">Benching</a>, shared workstations, '
             '<a href="/collections/acoustic-pods">acoustic pods</a></td>',
             'benching-desks + acoustic-pods'),
            ('<td>Executive + L-shaped desks, storage, guest seating</td>',
             '<td><a href="/collections/executive-desks">Executive + L-shaped desks</a>, storage, guest seating</td>',
             'executive-desks'),
            ('<td>Height-adjustable shared desks, lockers, lounge + pods</td>',
             '<td>Height-adjustable shared desks, <a href="/collections/lockers">lockers</a>, lounge + pods</td>',
             'lockers'),
            ('height-adjustable for shared sit-stand',
             '<a href="/products/electric-height-adjustable-standing-desk-workstation-4">height-adjustable</a> for shared sit-stand',
             'electric height-adjustable desk (PDP)'),
        ],
    },
}

FAQ_NEW_H2 = 'Frequently Asked Questions'
TAG_Q = ('<span class="bbi-faq__tag" aria-hidden="true" style="display:inline-block;'
         'width:1.7em;height:1.7em;line-height:1.7em;margin-right:0.6em;text-align:center;'
         'border-radius:5px;background:#D4252A;color:#fff;font-family:\'JetBrains Mono\',ui-monospace,monospace;'
         'font-size:0.72em;font-weight:700;vertical-align:middle;">Q</span>')
TAG_A = ('<span class="bbi-faq__tag" aria-hidden="true" style="display:inline-block;'
         'width:1.7em;height:1.7em;line-height:1.7em;margin-right:0.6em;text-align:center;'
         'border-radius:5px;background:#0B0B0C;color:#fff;font-family:\'JetBrains Mono\',ui-monospace,monospace;'
         'font-size:0.72em;font-weight:700;vertical-align:middle;">A</span>')

ITEM_RE = re.compile(r'<p><strong>(?P<q>.*?)</strong>\s*(?P<a>.*?)</p>', re.S)

def transform_faq(body, h2_old):
    """Return (new_body, n_items). Scopes to the FAQ section only."""
    h2_tag = f'<h2>{h2_old}</h2>'
    assert body.count(h2_tag) == 1, f'FAQ h2 not unique: {h2_old!r}'
    start = body.index(h2_tag)
    # FAQ section runs until the next <h2>
    nxt = body.find('<h2>', start + len(h2_tag))
    if nxt == -1:
        nxt = len(body)
    head, section, tail = body[:start], body[start:nxt], body[nxt:]
    # rename heading
    section = section.replace(h2_tag, f'<h2>{FAQ_NEW_H2}</h2>', 1)

    items = []
    def repl(m):
        q = m.group('q'); a = m.group('a')
        items.append((q, a))
        return (
            '<div class="bbi-faq__item" style="padding:1.1em 0;border-top:1px solid #E5E5E7;">'
            f'<p class="bbi-faq__q" style="margin:0 0 0.5em;">{TAG_Q}<strong>{q}</strong></p>'
            f'<p class="bbi-faq__a" style="margin:0;">{TAG_A}{a}</p>'
            '</div>'
        )
    section = ITEM_RE.sub(repl, section)
    return head + section + tail, items

def apply_links(body, links):
    report = []
    for find, rep, label in links:
        c = body.count(find)
        if c != 1:
            raise SystemExit(f'LINK ANCHOR not unique (count={c}) for {label!r}: {find!r}')
        body = body.replace(find, rep, 1)
        report.append(label)
    return body, report

def parse_visible_faq(body):
    """Re-parse visible Q/A from body_html, stripping label markup. Returns list of (q,a)."""
    soup = BeautifulSoup(body, 'html.parser')
    out = []
    for item in soup.select('.bbi-faq__item'):
        for tag in item.select('.bbi-faq__tag'):
            tag.decompose()
        q_el = item.select_one('.bbi-faq__q strong')
        a_el = item.select_one('.bbi-faq__a')
        q = q_el.get_text() if q_el else ''
        a = a_el.get_text() if a_el else ''
        out.append((q.strip(), a.strip()))
    return out

def faq_items_metafield(aid):
    mfs = api(f'blogs/{BLOG}/articles/{aid}/metafields.json')['metafields']
    m = [x for x in mfs if x['namespace'] == 'faq' and x['key'] == 'items'][0]
    val = json.loads(m['value'])
    pairs = []
    for it in val:
        q, a = it.split('||', 1)
        pairs.append((q.strip(), a.strip()))
    return pairs, m

def bytematch(visible, metaf):
    if len(visible) != len(metaf):
        return False, f'count mismatch visible={len(visible)} meta={len(metaf)}'
    for i, ((vq, va), (mq, ma)) in enumerate(zip(visible, metaf)):
        if vq != mq:
            return False, f'item {i} Q differs:\n  visible={vq!r}\n  meta   ={mq!r}'
        if va != ma:
            return False, f'item {i} A differs:\n  visible={va!r}\n  meta   ={ma!r}'
    return True, f'all {len(visible)} Q/A pairs byte-match'

LIVE = '--live' in sys.argv
for name, cfg in ARTS.items():
    print('='*70)
    print(name, cfg['id'], '| LIVE' if LIVE else '| DRY RUN')
    art = api(f"blogs/{BLOG}/articles/{cfg['id']}.json")['article']
    body = art['body_html']
    meta_pairs, _ = faq_items_metafield(cfg['id'])

    # baseline: current visible FAQ should already match metafield (sanity)
    base_q = re.findall(r'<p><strong>(.*?)</strong>', body, re.S)
    print(f'  baseline FAQ <p><strong> count in body: {len(base_q)}')

    new_body, items = transform_faq(body, cfg['faq_h2_old'])
    print(f'  FAQ heading -> "{FAQ_NEW_H2}";  reformatted {len(items)} items with Q/A labels')
    new_body, linkrep = apply_links(new_body, cfg['links'])
    print('  links added:', ', '.join(linkrep))

    visible = parse_visible_faq(new_body)
    ok, msg = bytematch(visible, meta_pairs)
    print('  BYTE-MATCH (pre-write):', 'PASS' if ok else 'FAIL', '-', msg)
    if not ok:
        raise SystemExit('ABORT: byte-match failed before write')

    # diff summary
    diff = list(difflib.unified_diff(body.splitlines(), new_body.splitlines(),
                                     lineterm='', n=0))
    print(f'  diff: {sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))} added / '
          f'{sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))} removed lines; '
          f'len {len(body)} -> {len(new_body)}')

    if LIVE:
        ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        api(f"blogs/{BLOG}/articles/{cfg['id']}.json", 'PUT',
            {'article': {'id': int(cfg['id']), 'body_html': new_body}})
        # hardened independent readback
        rb = api(f"blogs/{BLOG}/articles/{cfg['id']}.json")['article']['body_html']
        same = (rb == new_body)
        print(f'  READBACK len={len(rb)} matches-intended={same}')
        rb_meta, _ = faq_items_metafield(cfg['id'])
        rb_vis = parse_visible_faq(rb)
        ok2, msg2 = bytematch(rb_vis, rb_meta)
        print('  BYTE-MATCH (readback):', 'PASS' if ok2 else 'FAIL', '-', msg2)
        # store readback for inspection
        open(f"data/backups/articles/{name}-{cfg['id']}-AFTER-{ts}.html", 'w').write(rb)
    else:
        # save proposed body for inspection
        open(f"data/backups/articles/{name}-{cfg['id']}-PROPOSED.html", 'w').write(new_body)
print('='*70)
print('LIVE WRITE DONE' if LIVE else 'DRY RUN COMPLETE — no writes. Proposed bodies saved (*-PROPOSED.html).')
