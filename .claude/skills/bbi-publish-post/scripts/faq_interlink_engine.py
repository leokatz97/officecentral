#!/usr/bin/env python3
"""bbi-publish-post FAQ + interlink engine.

Absorbs the proven logic from scripts/standardize-articles.py (which ran live on
both Post 1 and the office-layout pillar on 2026-06-03) and generalizes it via a
publish-pack spec JSON so the same engine drives every future post.

Everything is DRY-RUN by default. Pass --live to perform writes.
The faq.items byte-match guard is enforced before any write and re-verified on a
hardened independent Admin-API readback (never the write log).

Subcommands:
  validate-meta   --title T --meta M          programmatic title<60 / meta<=155 gate
  check-handles   --handles a,b,c             storefront 200 check on link targets
  verify-faq      --article ID                live body_html vs faq.items byte-match
  standardize     --spec spec.json [--live]   reformat FAQ + interlinks on an EXISTING article
  create-draft    --spec spec.json [--live]   POST as published:false + set faq.items + readback
  flip-live       --spec spec.json [--live]   verify-before-flip gate then PUT published:true

Publish-pack spec JSON shape (only the fields each command needs are required):
  {
    "blog_id": "108557861177",
    "article_id": "689229365561",          # standardize / flip-live (existing article)
    "title": "...",                          # create-draft  (must be < 60 chars)
    "meta_description": "...",               # create-draft  (must be <= 155 chars)
    "handle": "clean-article-handle",        # create-draft  (no redundancy)
    "author": "Steve Katz",
    "tags": ["education", "OECM"],
    "excerpt": "...",
    "body_file": "data/content-drafts/NN-slug.html",  # create-draft body source
    "faq_old_heading": "Common Questions",   # the visible heading to rename
    "faq_items": ["Question||Answer", ...],  # canonical Q/A, becomes faq.items
    "interlinks": [["find", "replace", "label"], ...]   # count-guarded, find must be unique
  }
"""
import os, sys, json, re, argparse, difflib, datetime
import urllib.request, urllib.error
from bs4 import BeautifulSoup

# ---------------------------------------------------------------- env / api
def _load_env():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, '..', '..', '..', '..', '.env'),
                 os.path.join(os.getcwd(), '.env')):
        if os.path.exists(cand):
            for line in open(cand):
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k, v.strip().strip('"').strip("'"))
            return
_load_env()

STORE = 'office-central-online.myshopify.com'
API = '2026-04'
BLOG_DEFAULT = '108557861177'   # News blog

def api(path, method='GET', payload=None):
    token = os.environ.get('SHOPIFY_TOKEN')
    if not token:
        raise SystemExit('FATAL: SHOPIFY_TOKEN not set (silent PUT guard). Aborting.')
    url = f'https://{STORE}/admin/api/{API}/{path}'
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={'X-Shopify-Access-Token': token, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

# ---------------------------------------------------------------- FAQ chips
FAQ_NEW_H2 = 'Frequently Asked Questions'
_TAG_BASE = ('display:inline-block;width:1.7em;height:1.7em;line-height:1.7em;'
             'margin-right:0.6em;text-align:center;border-radius:5px;color:#fff;'
             "font-family:'JetBrains Mono',ui-monospace,monospace;font-size:0.72em;"
             'font-weight:700;vertical-align:middle;')
TAG_Q = f'<span class="bbi-faq__tag" aria-hidden="true" style="{_TAG_BASE}background:#D4252A;">Q</span>'
TAG_A = f'<span class="bbi-faq__tag" aria-hidden="true" style="{_TAG_BASE}background:#0B0B0C;">A</span>'
_ITEM_RE = re.compile(r'<p><strong>(?P<q>.*?)</strong>\s*(?P<a>.*?)</p>', re.S)

def render_faq_chips(body, old_h2, new_h2=FAQ_NEW_H2):
    """Rename the FAQ heading and wrap each Q/A pair with presentational chips.

    Chips are markup only. The question text stays inside <strong> and the answer
    text is moved verbatim, so re-parsing (with chips stripped) byte-matches the
    original. Scoped to the FAQ section only (heading to next <h2>).
    Returns (new_body, items) where items is the list of (q, a) found.
    """
    h2_tag = f'<h2>{old_h2}</h2>'
    if body.count(h2_tag) != 1:
        raise SystemExit(f'FAQ heading not unique: {old_h2!r} (count={body.count(h2_tag)})')
    start = body.index(h2_tag)
    nxt = body.find('<h2>', start + len(h2_tag))
    if nxt == -1:
        nxt = len(body)
    head, section, tail = body[:start], body[start:nxt], body[nxt:]
    section = section.replace(h2_tag, f'<h2>{new_h2}</h2>', 1)
    items = []
    def repl(m):
        q, a = m.group('q'), m.group('a')
        items.append((q, a))
        return ('<div class="bbi-faq__item" style="padding:1.1em 0;border-top:1px solid #E5E5E7;">'
                f'<p class="bbi-faq__q" style="margin:0 0 0.5em;">{TAG_Q}<strong>{q}</strong></p>'
                f'<p class="bbi-faq__a" style="margin:0;">{TAG_A}{a}</p>'
                '</div>')
    section = _ITEM_RE.sub(repl, section)
    return head + section + tail, items

def apply_interlinks(body, links):
    """Count-guarded string replacements. Each find must occur exactly once."""
    report = []
    for find, rep, label in links:
        c = body.count(find)
        if c != 1:
            raise SystemExit(f'INTERLINK anchor not unique (count={c}) for {label!r}: {find!r}')
        body = body.replace(find, rep, 1)
        report.append(label)
    return body, report

def parse_visible_faq(body):
    """Re-parse visible Q/A from body_html, stripping chip markup."""
    soup = BeautifulSoup(body, 'html.parser')
    out = []
    for item in soup.select('.bbi-faq__item'):
        for tag in item.select('.bbi-faq__tag'):
            tag.decompose()
        q_el = item.select_one('.bbi-faq__q strong')
        a_el = item.select_one('.bbi-faq__a')
        out.append(((q_el.get_text() if q_el else '').strip(),
                    (a_el.get_text() if a_el else '').strip()))
    return out

def pairs_from_items(faq_items):
    out = []
    for it in faq_items:
        q, a = it.split('||', 1)
        out.append((q.strip(), a.strip()))
    return out

def faq_items_metafield(blog_id, article_id):
    mfs = api(f'blogs/{blog_id}/articles/{article_id}/metafields.json')['metafields']
    m = [x for x in mfs if x['namespace'] == 'faq' and x['key'] == 'items']
    if not m:
        return None, None
    return pairs_from_items(json.loads(m[0]['value'])), m[0]

def bytematch(visible, pairs):
    if len(visible) != len(pairs):
        return False, f'count mismatch visible={len(visible)} canonical={len(pairs)}'
    for i, ((vq, va), (mq, ma)) in enumerate(zip(visible, pairs)):
        if vq != mq:
            return False, f'item {i} Q differs:\n  visible={vq!r}\n  canon  ={mq!r}'
        if va != ma:
            return False, f'item {i} A differs:\n  visible={va!r}\n  canon  ={ma!r}'
    return True, f'all {len(visible)} Q/A pairs byte-match'

# ---------------------------------------------------------------- spec
def load_spec(path):
    spec = json.load(open(path))
    if 'body_html' not in spec and spec.get('body_file'):
        spec['body_html'] = open(spec['body_file']).read()
    spec.setdefault('blog_id', BLOG_DEFAULT)
    spec.setdefault('interlinks', [])
    return spec

def _ts():
    return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

# ---------------------------------------------------------------- commands
def cmd_validate_meta(a):
    t, m = a.title, a.meta
    tok = len(t) < 60
    mok = len(m) <= 155
    print(f'title : {len(t)} chars  {"PASS (<60)" if tok else "FAIL (>=60)"}  | {t!r}')
    print(f'meta  : {len(m)} chars  {"PASS (<=155)" if mok else "FAIL (>155)"}  | {m!r}')
    sys.exit(0 if (tok and mok) else 1)

def cmd_check_handles(a):
    import http.client, ssl
    handles = [h.strip() for h in a.handles.split(',') if h.strip()]
    base = 'www.brantbusinessinteriors.com'
    ctx = ssl.create_default_context()
    allok = True
    for h in handles:
        path = h if h.startswith('/') else '/' + h
        conn = http.client.HTTPSConnection(base, context=ctx, timeout=20)
        try:
            conn.request('GET', path, headers={'User-Agent': 'Mozilla/5.0'})
            code = conn.getresponse().status
        except Exception as e:
            code = f'ERR {e}'
        finally:
            conn.close()
        ok = (code == 200)
        allok = allok and ok
        print(f'{code}  {path}')
    sys.exit(0 if allok else 1)

def cmd_verify_faq(a):
    art = api(f'blogs/{a.blog}/articles/{a.article}.json')['article']
    pairs, mf = faq_items_metafield(a.blog, a.article)
    if pairs is None:
        raise SystemExit('No faq.items metafield on this article.')
    visible = parse_visible_faq(art['body_html'])
    ok, msg = bytematch(visible, pairs)
    print('BYTE-MATCH:', 'PASS' if ok else 'FAIL', '-', msg)
    sys.exit(0 if ok else 1)

def _transform(spec):
    body = spec['body_html']
    new_body, items = render_faq_chips(body, spec['faq_old_heading'])
    new_body, linkrep = apply_interlinks(new_body, spec['interlinks'])
    canonical = pairs_from_items(spec['faq_items']) if spec.get('faq_items') else \
                [(q, a) for q, a in items]
    visible = parse_visible_faq(new_body)
    ok, msg = bytematch(visible, canonical)
    return new_body, items, linkrep, ok, msg, canonical

def cmd_standardize(a):
    spec = load_spec(a.spec)
    art = api(f"blogs/{spec['blog_id']}/articles/{spec['article_id']}.json")['article']
    ts = _ts()
    bdir = 'data/backups/articles'
    os.makedirs(bdir, exist_ok=True)
    open(f"{bdir}/{spec['article_id']}-body-before-{ts}.html", 'w').write(art['body_html'])
    spec['body_html'] = art['body_html']
    new_body, items, linkrep, ok, msg, _ = _transform(spec)
    print(f"FAQ -> '{FAQ_NEW_H2}', {len(items)} items reformatted; links: {', '.join(linkrep)}")
    print('BYTE-MATCH (pre-write):', 'PASS' if ok else 'FAIL', '-', msg)
    if not ok:
        raise SystemExit('ABORT: byte-match failed before write.')
    print(f'len {len(art["body_html"])} -> {len(new_body)}')
    if not a.live:
        open(f"{bdir}/{spec['article_id']}-PROPOSED-{ts}.html", 'w').write(new_body)
        print('DRY RUN: proposed body saved. Re-run with --live to write.')
        return
    api(f"blogs/{spec['blog_id']}/articles/{spec['article_id']}.json", 'PUT',
        {'article': {'id': int(spec['article_id']), 'body_html': new_body}})
    rb = api(f"blogs/{spec['blog_id']}/articles/{spec['article_id']}.json")['article']['body_html']
    open(f"{bdir}/{spec['article_id']}-AFTER-{ts}.html", 'w').write(rb)
    rb_pairs, _ = faq_items_metafield(spec['blog_id'], spec['article_id'])
    ok2, msg2 = bytematch(parse_visible_faq(rb), rb_pairs)
    print('READBACK byte-match (vs live faq.items):', 'PASS' if ok2 else 'FAIL', '-', msg2)

def cmd_create_draft(a):
    spec = load_spec(a.spec)
    if not (len(spec['title']) < 60):
        raise SystemExit(f"title >= 60 ({len(spec['title'])}). Fix in PREP.")
    if not (len(spec['meta_description']) <= 155):
        raise SystemExit(f"meta > 155 ({len(spec['meta_description'])}). Fix in PREP.")
    # handle collision check
    existing = api(f"blogs/{spec['blog_id']}/articles.json?handle={spec['handle']}&limit=1")['articles']
    if existing:
        raise SystemExit(f"HANDLE COLLISION: {spec['handle']} already exists (id {existing[0]['id']}).")
    new_body, items, linkrep, ok, msg, canonical = _transform(spec)
    print(f"FAQ -> '{FAQ_NEW_H2}', {len(items)} items; links: {', '.join(linkrep)}")
    print('BYTE-MATCH (visible vs faq_items):', 'PASS' if ok else 'FAIL', '-', msg)
    if not ok:
        raise SystemExit('ABORT: byte-match failed before create.')
    payload = {'article': {
        'title': spec['title'], 'author': spec.get('author', 'Steve Katz'),
        'body_html': new_body, 'handle': spec['handle'],
        'tags': ','.join(spec.get('tags', [])), 'published': False}}
    if spec.get('excerpt'):
        payload['article']['summary_html'] = spec['excerpt']
    if not a.live:
        print('DRY RUN: would POST published:false with the above payload. Re-run with --live.')
        return
    ts = _ts()
    bdir = 'data/backups/articles'; os.makedirs(bdir, exist_ok=True)
    res = api(f"blogs/{spec['blog_id']}/articles.json", 'POST', payload)['article']
    aid = res['id']
    json.dump({'payload': payload, 'response': res},
              open(f"{bdir}/create-{aid}-{ts}.json", 'w'), indent=2, ensure_ascii=False)
    # set faq.items + SEO metafields
    api(f"blogs/{spec['blog_id']}/articles/{aid}/metafields.json", 'POST',
        {'metafield': {'namespace': 'faq', 'key': 'items',
                       'type': 'list.single_line_text_field',
                       'value': json.dumps(spec['faq_items'], ensure_ascii=False)}})
    api(f"blogs/{spec['blog_id']}/articles/{aid}/metafields.json", 'POST',
        {'metafield': {'namespace': 'global', 'key': 'title_tag',
                       'type': 'single_line_text_field', 'value': spec['title']}})
    api(f"blogs/{spec['blog_id']}/articles/{aid}/metafields.json", 'POST',
        {'metafield': {'namespace': 'global', 'key': 'description_tag',
                       'type': 'single_line_text_field', 'value': spec['meta_description']}})
    rb = api(f"blogs/{spec['blog_id']}/articles/{aid}.json")['article']
    rb_pairs, _ = faq_items_metafield(spec['blog_id'], aid)
    ok2, msg2 = bytematch(parse_visible_faq(rb['body_html']), rb_pairs)
    print(f"CREATED unpublished id={aid} handle={rb['handle']} published={rb['published_at']}")
    print(f"  URL (draft): /blogs/news/{rb['handle']}")
    print('  READBACK byte-match (vs faq.items):', 'PASS' if ok2 else 'FAIL', '-', msg2)
    print('  HALT: human adds featured image + alt text; Steve signs off. Then run flip-live.')

def cmd_flip_live(a):
    spec = load_spec(a.spec)
    aid = spec['article_id']
    art = api(f"blogs/{spec['blog_id']}/articles/{aid}.json")['article']
    checks = []
    checks.append(('currently unpublished', art['published_at'] is None))
    checks.append(('featured image present', bool(art.get('image'))))
    rb_pairs, _ = faq_items_metafield(spec['blog_id'], aid)
    fok, fmsg = (bytematch(parse_visible_faq(art['body_html']), rb_pairs) if rb_pairs else (False, 'no faq.items'))
    checks.append((f'faq.items byte-match ({fmsg})', fok))
    checks.append(('title intact', art['title'] == spec.get('title', art['title'])))
    checks.append(('handle intact', art['handle'] == spec.get('handle', art['handle'])))
    print('VERIFY-BEFORE-FLIP:')
    for name, ok in checks:
        print(f'  [{"PASS" if ok else "FAIL"}] {name}')
    if not all(ok for _, ok in checks):
        raise SystemExit('HALT: verify-before-flip gate failed. No flip.')
    if not a.live:
        print('DRY RUN: all gates PASS. Re-run with --live to flip published:true.')
        return
    api(f"blogs/{spec['blog_id']}/articles/{aid}.json", 'PUT',
        {'article': {'id': int(aid), 'published': True}})
    rb = api(f"blogs/{spec['blog_id']}/articles/{aid}.json")['article']
    print(f"FLIPPED LIVE: published_at={rb['published_at']}")
    print(f"  Live URL: https://www.brantbusinessinteriors.com/blogs/news/{rb['handle']}")
    print('  HALT: Leo runs Google Rich Results Test (the only authoritative render check).')

def main():
    p = argparse.ArgumentParser(description='bbi-publish-post FAQ + interlink engine (dry-run default)')
    sub = p.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('validate-meta'); s.add_argument('--title', required=True); s.add_argument('--meta', required=True); s.set_defaults(fn=cmd_validate_meta)
    s = sub.add_parser('check-handles'); s.add_argument('--handles', required=True); s.set_defaults(fn=cmd_check_handles)
    s = sub.add_parser('verify-faq'); s.add_argument('--article', required=True); s.add_argument('--blog', default=BLOG_DEFAULT); s.set_defaults(fn=cmd_verify_faq)
    for name, fn in (('standardize', cmd_standardize), ('create-draft', cmd_create_draft), ('flip-live', cmd_flip_live)):
        s = sub.add_parser(name); s.add_argument('--spec', required=True); s.add_argument('--live', action='store_true'); s.set_defaults(fn=fn)
    a = p.parse_args()
    a.fn(a)

if __name__ == '__main__':
    main()
