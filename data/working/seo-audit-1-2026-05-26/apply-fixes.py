#!/usr/bin/env python3
"""
SEO-AUDIT-1 Phase 7.2 — apply all approved fixes.

Order:
  1. Verify LIVE baseline (HALT if changed)
  2. Push meta-tags.liquid edit to DEV
  3. Page metafield writes (description_tag + title_tag) — 17 pages
  4. Collection metafield writes — 10 collections
  5. Blog hub + cornerstone article metafield writes
  6. Redirects + unpublish (FIX #9 + #10a)
  7. Re-verify LIVE baseline

Snapshots all pre-state metafields to backup dir.
Rate-limits 0.5s between writes.
"""
import urllib.request, urllib.error, json, os, sys, time, hashlib
from pathlib import Path

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
API_VERSION = '2026-04'
API = f'https://{STORE}/admin/api/{API_VERSION}'
DEV = '186373570873'
LIVE = '178274435385'
LIVE_BASELINE = '2026-05-16T16:47:22-04:00'

H_JSON = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}
H_READ = {'X-Shopify-Access-Token': TOKEN}

BACKUP = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('data/backups/seo-audit-1-fix-batch-pre-NOW')
BACKUP.mkdir(parents=True, exist_ok=True)
LOG = []

# ===== Copy table =====
PAGE_FIXES = {
    'about':               {'title': 'About Brant Business Interiors – Canadian-owned 1964',
                            'desc':  'Brant Business Interiors is a Canadian-owned commercial office furniture dealer in Peterborough, Ontario. OECM Agreement 2025-470. Family-owned since 1964.'},
    'brands':              {'title': 'Canadian Office Furniture Brands | Brant Business Interiors',
                            'desc':  'Authorized Canadian dealer for ergoCentric, Global Furniture Group, OTG / Offices to Go, Heartwood, ObusForme, and Keilhauer. OECM Agreement 2025-470.'},
    'brands-ergocentric':  {'title': 'ergoCentric Authorized Dealer Ontario | Brant Business',
                            'desc':  'Authorized ergoCentric dealer in Ontario. Canadian-engineered ergonomic seating, task chairs, and stools. OECM Agreement 2025-470. Quote in 1 business day.'},
    'brands-global-teknion': {'title': 'Global Furniture Group Dealer Ontario | Brant Business',
                              'desc':  'Authorized Global Furniture Group dealer in Ontario. Seating, desks, filing, and panels from Canada\'s largest contract furniture maker. OECM Agreement 2025-470.'},
    'brands-heartwood':    {'title': 'Heartwood Manufacturing Dealer Ontario | Brant Business',
                            'desc':  'Authorized Heartwood Manufacturing dealer in Ontario. Canadian-made veneer desks, casegoods, conference tables. OECM Agreement 2025-470. Quote in 1 business day.'},
    'brands-keilhauer':    {'title': 'Keilhauer Seating Dealer Ontario | Brant Business Interiors',
                            'desc':  'Keilhauer seating and lounge furniture from a Canadian-owned Ontario dealer. Mid-to-high-end contract chairs. OECM Agreement 2025-470. Quote in 1 business day.'},
    'brands-obusforme':    {'title': 'ObusForme Authorized Dealer Ontario | Brant Business',
                            'desc':  'Authorized ObusForme dealer in Ontario. Canadian-made ergonomic seating with the original Obus-back support system. OECM Agreement 2025-470. Quote in 1 day.'},
    'brands-otg':          {'title': 'OTG / Offices to Go Dealer Ontario | Brant Business',
                            'desc':  'Authorized OTG / Offices to Go dealer in Ontario. Canadian-made seating, desks, lounge, and accessories at workhorse price points. OECM Agreement 2025-470.'},
    'contact':             {'title': 'Contact Brant Business Interiors – Peterborough HQ',
                            'desc':  None},  # has existing desc 121ch, fine
    'customer-stories':    {'title': 'Office Furniture Customer Stories – Brant Business Interiors',
                            'desc':  'School boards, hospitals, and Ontario municipalities partnering with Brant Business Interiors. OECM Agreement 2025-470 case studies and verified installations.'},
    'delivery':            {'title': 'Office Furniture Delivery & Installation Ontario | Brant',
                            'desc':  'Free in-house delivery and assembly across Ontario by Brant Business Interiors. After-hours and weekend installs can typically be arranged at quote time.'},
    'design-services':     {'title': 'Free Office Design & Space Planning | Brant Business',
                            'desc':  None},  # existing 147ch, fine
    'education':           {'title': 'Education Furniture Ontario – OECM Agreement 2025-470',
                            'desc':  'Office furniture for Ontario school boards, colleges, and independent schools. OECM Agreement 2025-470 — order without open tender. Summer-window installs.'},
    'faq':                 {'title': None,  # existing 47ch ok
                            'desc':  None},  # existing 162ch ok
    'government':          {'title': 'Government Furniture Ontario – OECM Agreement 2025-470',
                            'desc':  'Office furniture for Ontario municipal, provincial, and federal offices. OECM Agreement 2025-470 — order without open tender. Audit-trail PO billing.'},
    'healthcare':          {'title': 'Healthcare & Clinical Office Furniture Ontario | Brant',
                            'desc':  None},  # existing 157ch ok
    'industries':          {'title': 'Ontario Institutional Furniture – OECM 2025-470 Supplier',
                            'desc':  None},  # existing 177ch, slightly long but kept
    'non-profit':          {'title': 'Non-Profit Office Furniture Ontario – OECM 2025-470',
                            'desc':  'Office furniture for Ontario non-profits, family health teams, and community-services agencies. OECM Agreement 2025-470. Budget-friendly leads, NET 30 terms.'},
    'oecm':                {'title': 'OECM Office Furniture Supplier – Agreement 2025-470',
                            'desc':  'Brant Basics is a verified OECM Supplier Partner under Agreement 2025-470. Ontario broader-public-sector buyers can order office furniture without open tender.'},
    'our-work':            {'title': 'Office Furniture Projects – Brant Business Interiors',
                            'desc':  'Recent Brant Business Interiors office furniture installs across Ontario — school boards, hospitals, municipalities, private boardrooms. OECM Agreement 2025-470.'},
    'professional-services': {'title': 'Professional Services Office Furniture Ontario | Brant',
                              'desc':  'Office furniture for Ontario law firms, accountants, design studios, and medical/dental offices. ergoCentric, OTG, Heartwood. Canadian-owned since 1964.'},
    'quote':               {'title': 'Request an Office Furniture Quote | Brant Business Interiors',
                            'desc':  'Request a furniture quote from Brant Business Interiors. Most quotes back in 1 business day. OECM Agreement 2025-470. 1-800-835-9565 for fast-track pricing.'},
    'relocation':          {'title': 'Office Relocation Services – Brant Business Interiors',
                            'desc':  'Office relocation management across Ontario by Brant Business Interiors. Inventory, packing, install, and after-hours coordination from one Canadian-owned team.'},
}

COLLECTION_FIXES = {
    'business-furniture': {'title': 'Office Furniture Ontario | Brant Business Interiors',
                           'desc':  'Brant Business Interiors\' full Ontario office furniture catalog — seating, desks, storage, tables, ergonomic, panels, accessories. OECM Agreement 2025-470.'},
    'seating':            {'title': 'Office Chairs & Seating Ontario | Brant Business',
                           'desc':  'Task chairs, executive seating, lounge, stacking, and 24-hour chairs from ergoCentric, OTG, Keilhauer, ObusForme. OECM Agreement 2025-470. Quote in 1 day.'},
    'desks':              {'title': 'Office Desks & Workstations Ontario | Brant Business',
                           'desc':  'Height-adjustable desks, L-shape, U-shape, benching, and reception desks from OTG and Heartwood. OECM Agreement 2025-470. Free CAD layout with every quote.'},
    'storage':            {'title': 'Office Storage & Filing Ontario | Brant Business',
                           'desc':  'Lateral files, vertical files, cabinets, bookcases, hutches, lockers, and fire-resistant safes for Ontario offices. OECM Agreement 2025-470. 1-day quote.'},
    'tables':             {'title': 'Office Tables Ontario | Brant Business Interiors',
                           'desc':  'Meeting, training, cafeteria, drafting, coffee, and bar-height tables from Canada\'s leading contract furniture brands. OECM Agreement 2025-470. 1-day quote.'},
    'boardroom':          {'title': 'Boardroom Furniture Ontario | Brant Business Interiors',
                           'desc':  'Boardroom tables, conference seating, lecterns, podiums, and AV-friendly furniture for Ontario offices. OECM Agreement 2025-470. Free CAD layout included.'},
    'accessories':        {'title': 'Office Accessories Ontario | Brant Business Interiors',
                           'desc':  'Chairmats, monitor arms, power modules, keyboard trays, lighting, and ergonomic accessories for Ontario offices. OECM Agreement 2025-470. 1-day quote.'},
    'ergonomic-products': {'title': 'Ergonomic Office Products Ontario | Brant Business',
                           'desc':  'Height-adjustable tables, monitor arms, keyboard trays, and sit-stand desktop units. ergoCentric and ObusForme ergonomics. OECM Agreement 2025-470.'},
    'panels-room-dividers': {'title': 'Panels & Room Dividers Ontario | Brant Business',
                             'desc':  'Modular panel systems, desk-top dividers, and modesty panels from OTG and Global Furniture Group. OECM Agreement 2025-470. CAD floor plan with every quote.'},
    'quiet-spaces':       {'title': 'Quiet Spaces & Acoustic Pods | Brant Business Interiors',
                           'desc':  'Telephone booths, acoustic walls, sound dampeners, and AV-friendly furniture for Ontario open-plan offices. OECM Agreement 2025-470. Quote in 1 business day.'},
}

BLOG_FIX = {
    'news': {'title': 'Office Furniture News & Buying Guides | Brant Business',
             'desc':  'Office-furniture buying guides, OECM procurement how-tos, and Ontario workplace insights from Brant Business Interiors. Updated regularly. 1-800-835-9565.'}
}

ARTICLE_FIX = {
    'oecm-ontario-school-boards-office-furniture': {
        'title': 'OECM Office Furniture for Ontario School Boards (2025-470)',
        'desc':  'How Ontario school boards procure office furniture under OECM Agreement 2025-470 — eligibility, ordering, delivery, lead times. By Brant Business Interiors.'
    }
}


def req(method, path, body=None, base=API):
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(f'{base}{path}', data=data, headers=H_JSON if body else H_READ, method=method)
    try:
        resp = urllib.request.urlopen(r, timeout=30)
        return resp.status, resp.read(), None
    except urllib.error.HTTPError as e:
        return e.code, b'', f'{e.code}: {e.read().decode()[:400]}'


def check_live():
    s, b, e = req('GET', f'/themes/{LIVE}.json')
    t = json.loads(b)['theme']
    if t['updated_at'] != LIVE_BASELINE:
        print(f'✗ LIVE BASELINE DRIFTED: {t["updated_at"]} (expected {LIVE_BASELINE})', file=sys.stderr)
        sys.exit(1)
    return True


def upsert_metafield(owner_resource, owner_id, namespace, key, value, mtype='string'):
    """Set metafield on a page/collection/blog/article. Returns (ok, detail)."""
    # First check if exists
    s, b, e = req('GET', f'/{owner_resource}/{owner_id}/metafields.json')
    if e:
        return False, f'list_err: {e}'
    metas = json.loads(b)['metafields']
    existing = next((m for m in metas if m.get('namespace')==namespace and m.get('key')==key), None)
    if existing:
        # Update
        body = {'metafield': {'id': existing['id'], 'value': value, 'type': mtype}}
        s, b, e = req('PUT', f'/metafields/{existing["id"]}.json', body)
        if e:
            return False, f'update_err: {e}'
        return True, f'updated mf id={existing["id"]}'
    else:
        # Create
        body = {'metafield': {'namespace': namespace, 'key': key, 'value': value, 'type': mtype}}
        s, b, e = req('POST', f'/{owner_resource}/{owner_id}/metafields.json', body)
        if e:
            return False, f'create_err: {e}'
        return True, f'created mf id={json.loads(b)["metafield"]["id"]}'


def write_page_seo(handle, title, desc):
    s, b, e = req('GET', f'/pages.json?handle={handle}&fields=id,handle')
    if e:
        log('page', handle, False, f'lookup: {e}')
        return
    pages = json.loads(b).get('pages', [])
    if not pages:
        log('page', handle, False, 'NOT FOUND')
        return
    pid = pages[0]['id']
    # Snapshot pre-state
    sm, bm, em = req('GET', f'/pages/{pid}/metafields.json')
    if not em:
        (BACKUP / f'page-{handle}-metafields.json').write_text(json.dumps(json.loads(bm), indent=2))

    if title is not None:
        ok, det = upsert_metafield('pages', pid, 'global', 'title_tag', title, 'single_line_text_field')
        log(f'page:{handle}', 'title_tag', ok, det)
        time.sleep(0.4)
    if desc is not None:
        ok, det = upsert_metafield('pages', pid, 'global', 'description_tag', desc, 'single_line_text_field')
        log(f'page:{handle}', 'description_tag', ok, det)
        time.sleep(0.4)


def write_collection_seo(handle, title, desc):
    # Try smart_collections first, then custom_collections
    cid = None
    for ep in ('smart_collections', 'custom_collections'):
        s, b, e = req('GET', f'/{ep}.json?handle={handle}&fields=id,handle')
        if not e:
            cols = json.loads(b).get(ep, [])
            if cols:
                cid = cols[0]['id']
                break
    if not cid:
        log('collection', handle, False, 'NOT FOUND')
        return
    sm, bm, em = req('GET', f'/collections/{cid}/metafields.json')
    if not em:
        (BACKUP / f'collection-{handle}-metafields.json').write_text(json.dumps(json.loads(bm), indent=2))
    if title is not None:
        ok, det = upsert_metafield('collections', cid, 'global', 'title_tag', title, 'single_line_text_field')
        log(f'col:{handle}', 'title_tag', ok, det)
        time.sleep(0.4)
    if desc is not None:
        ok, det = upsert_metafield('collections', cid, 'global', 'description_tag', desc, 'single_line_text_field')
        log(f'col:{handle}', 'description_tag', ok, det)
        time.sleep(0.4)


def write_blog_seo(handle, title, desc):
    s, b, e = req('GET', '/blogs.json')
    blog = next((x for x in json.loads(b)['blogs'] if x['handle']==handle), None)
    if not blog:
        log('blog', handle, False, 'NOT FOUND'); return
    bid = blog['id']
    sm, bm, em = req('GET', f'/blogs/{bid}/metafields.json')
    if not em:
        (BACKUP / f'blog-{handle}-metafields.json').write_text(json.dumps(json.loads(bm), indent=2))
    if title is not None:
        ok, det = upsert_metafield('blogs', bid, 'global', 'title_tag', title, 'single_line_text_field')
        log(f'blog:{handle}', 'title_tag', ok, det)
        time.sleep(0.4)
    if desc is not None:
        ok, det = upsert_metafield('blogs', bid, 'global', 'description_tag', desc, 'single_line_text_field')
        log(f'blog:{handle}', 'description_tag', ok, det)
        time.sleep(0.4)


def write_article_seo(blog_handle, article_handle, title, desc):
    s, b, e = req('GET', '/blogs.json')
    blog = next((x for x in json.loads(b)['blogs'] if x['handle']==blog_handle), None)
    if not blog:
        log('article', article_handle, False, 'blog NOT FOUND'); return
    bid = blog['id']
    s, b, e = req('GET', f'/blogs/{bid}/articles.json?published_status=published&limit=50')
    art = next((a for a in json.loads(b)['articles'] if a['handle']==article_handle), None)
    if not art:
        log('article', article_handle, False, 'article NOT FOUND'); return
    aid = art['id']
    sm, bm, em = req('GET', f'/articles/{aid}/metafields.json')
    if not em:
        (BACKUP / f'article-{article_handle}-metafields.json').write_text(json.dumps(json.loads(bm), indent=2))
    if title is not None:
        ok, det = upsert_metafield('articles', aid, 'global', 'title_tag', title, 'single_line_text_field')
        log(f'art:{article_handle}', 'title_tag', ok, det)
        time.sleep(0.4)
    if desc is not None:
        ok, det = upsert_metafield('articles', aid, 'global', 'description_tag', desc, 'single_line_text_field')
        log(f'art:{article_handle}', 'description_tag', ok, det)
        time.sleep(0.4)


def create_redirect(path, target):
    body = {'redirect': {'path': path, 'target': target}}
    s, b, e = req('POST', '/redirects.json', body)
    if e and '422' in e:
        # Might already exist; surface
        return False, e
    if e:
        return False, e
    rid = json.loads(b)['redirect']['id']
    return True, f'created redirect id={rid}'


def unpublish_page(handle):
    s, b, e = req('GET', f'/pages.json?handle={handle}&fields=id,handle,published_at')
    pages = json.loads(b).get('pages', [])
    if not pages:
        return False, 'NOT FOUND'
    pid = pages[0]['id']
    (BACKUP / f'page-{handle}-pre-unpublish.json').write_text(json.dumps(pages[0], indent=2))
    body = {'page': {'id': pid, 'published': False}}
    s, b, e = req('PUT', f'/pages/{pid}.json', body)
    if e:
        return False, e
    return True, f'unpublished page id={pid}'


def log(scope, key, ok, det):
    sym = '✓' if ok else '✗'
    LOG.append((scope, key, ok, det))
    print(f'  {sym} {scope:32s} {key:18s} {det[:80]}')


# ============================================================
def main():
    print(f'Pre-write LIVE baseline check…')
    check_live()
    print(f'✓ LIVE baseline {LIVE_BASELINE} OK')
    print()
    print(f'Backup dir: {BACKUP}')
    print()
    print('=== Phase 7.2 — Page metafield writes (17 pages) ===')
    for h, f in PAGE_FIXES.items():
        if f.get('title') is None and f.get('desc') is None:
            print(f'  · {h}: skipped (no writes needed — existing tags OK)')
            continue
        write_page_seo(h, f.get('title'), f.get('desc'))

    print('\n=== Phase 7.2 — Collection metafield writes (10 collections) ===')
    for h, f in COLLECTION_FIXES.items():
        write_collection_seo(h, f.get('title'), f.get('desc'))

    print('\n=== Phase 7.2 — Blog + article metafield writes ===')
    for h, f in BLOG_FIX.items():
        write_blog_seo(h, f.get('title'), f.get('desc'))
    for h, f in ARTICLE_FIX.items():
        write_article_seo('news', h, f.get('title'), f.get('desc'))

    print('\n=== Phase 7.2 — Redirects + unpublish (FIX #9 + #10a) ===')
    for source, target in [
        ('/pages/ergocentric', '/pages/brands-ergocentric'),
        ('/pages/how-to-adjust-my-new-chair', '/pages/brands-ergocentric'),
    ]:
        ok, det = create_redirect(source, target)
        log('redirect', source, ok, det)
        time.sleep(0.4)

    for h in ['ergocentric', 'how-to-adjust-my-new-chair']:
        ok, det = unpublish_page(h)
        log(f'unpublish:{h}', '', ok, det)
        time.sleep(0.4)

    # Post-write LIVE baseline check
    print(f'\nPost-write LIVE baseline check…')
    check_live()
    print(f'✓ LIVE baseline {LIVE_BASELINE} STILL OK')

    # Summary
    success = sum(1 for _, _, ok, _ in LOG if ok)
    failure = sum(1 for _, _, ok, _ in LOG if not ok)
    print(f'\n=== SUMMARY ===')
    print(f'  Successes: {success}')
    print(f'  Failures:  {failure}')
    if failure:
        print('FAILED WRITES:')
        for scope, key, ok, det in LOG:
            if not ok:
                print(f'  ✗ {scope} {key} → {det}')
        sys.exit(1)

    # Save log
    (BACKUP / 'write-log.json').write_text(json.dumps([
        {'scope': s, 'key': k, 'ok': o, 'detail': d} for s,k,o,d in LOG
    ], indent=2))


if __name__ == '__main__':
    main()
