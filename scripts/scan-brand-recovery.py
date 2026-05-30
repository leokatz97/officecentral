#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-3 — Catalog-wide brand-recovery scan (READ-ONLY).

Fetches every product where vendor == "Brant Business Interiors" via the Admin
GraphQL API (paginated), runs manufacturer signal-detection over
title/body/tags/SKU/metafields, classifies confidence, and writes the review
worksheet to data/reports/brand-recovery-<date>.csv.

Signal priority (highest first):
  1. Service/non-product line-item guard (Delivery/Installation) -> SKIP
  2. Structured body field "Manufacturer {Name}" / "Brand {Name}"  -> HIGH
  3. SKU prefix mapped to a known manufacturer (model-code equivalent) -> HIGH
  4. Direct manufacturer name in title/body                        -> HIGH
  5. Model-code regex (MVL-, 2400/2424/2670, 2130SL, KX-)          -> HIGH
  6. Sub-brand (Offices To Go / OTG / ObusForme / Basics)          -> MEDIUM
  7. Product-line name                                             -> MEDIUM
  8. Designer name                                                 -> LOW
  9. Otherwise: record SKU prefix as ambiguous_prefix              -> UNKNOWN

No writes to Shopify. No theme files touched.
"""
import json, re, csv, html, urllib.request, sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=', 1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
if not TOKEN:
    sys.exit('FATAL: SHOPIFY_TOKEN not loaded from .env')
SHOP = 'office-central-online.myshopify.com'
GQL = f'https://{SHOP}/admin/api/2024-10/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}
DATE = '2026-05-30'

QUERY = '''
query($cursor: String) {
  products(first: 100, after: $cursor, query: "vendor:'Brant Business Interiors'") {
    pageInfo { hasNextPage endCursor }
    edges { node {
      id legacyResourceId handle title vendor productType descriptionHtml tags
      variants(first: 50) { edges { node { sku title } } }
      metafields(first: 100) { edges { node { namespace key value } } }
    }}
  }
}'''


def gql(query, variables):
    body = json.dumps({'query': query, 'variables': variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers=HDR, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    if 'errors' in d:
        raise RuntimeError(json.dumps(d['errors'], indent=2))
    return d['data']


def fetch_all():
    out, cursor, page = [], None, 0
    while True:
        page += 1
        conn = gql(QUERY, {'cursor': cursor})['products']
        out.extend(e['node'] for e in conn['edges'])
        print(f'  page {page}: +{len(conn["edges"])} (total {len(out)})', file=sys.stderr)
        if not conn['pageInfo']['hasNextPage']:
            break
        cursor = conn['pageInfo']['endCursor']
    return out


# ---------------------------------------------------------------------------
# Canonical vendor names
# ---------------------------------------------------------------------------
GLOBAL = 'Global Furniture Group'

# SKU-prefix stem -> canonical vendor. Confident set (treated as model-code, HIGH).
# Match by uppercased-SKU startswith, longest stem first.
PREFIX_MAP = [
    ('GLBM', GLOBAL), ('GLBD', GLOBAL), ('GLBN', GLOBAL), ('GLBC', GLOBAL),
    ('GLBMV', GLOBAL), ('GLBML', GLOBAL), ('GLB', GLOBAL), ('GLO', GLOBAL),
    ('OFGO', GLOBAL), ('OTG', GLOBAL), ('MVL', GLOBAL),
    ('SAF', 'Safco'),
    ('HTW', 'Heartwood'),
    ('OSP', 'Office Star Products'),
    ('BORGO', 'Borgo'),
    ('FOU', 'Foundations'),
    ('SEN', 'Sentry Safe'),
    ('DEF', 'deflecto'),
    ('GDX', 'Gardex'),
    ('MMM', '3M'),
    ('VCT', 'Victor'),
    ('FEL', 'Fellowes'),
    ('TAYCO', 'Tayco'), ('TAY', 'Tayco'),
    ('ALLSE', 'Allseating'),
    ('LCF', 'Links Contract Furniture'),
]
PREFIX_MAP.sort(key=lambda x: -len(x[0]))  # longest stem first
CONFIDENT_PREFIXES = {p for p, _ in PREFIX_MAP}

# Structured "Manufacturer {X}" / "Brand {X}" body-field value -> canonical vendor
STRUCTURED_NAME = [
    ('global upholstery', GLOBAL), ('offices to go', GLOBAL), ('global', GLOBAL),
    ('deflecto', 'deflecto'), ('gardex', 'Gardex'), ('sentry', 'Sentry Safe'),
    ('heartwood', 'Heartwood'), ('safco', 'Safco'), ('victor', 'Victor'),
    ('3m', '3M'), ('screenflex', 'Screenflex'),
    ('links contract', 'Links Contract Furniture'), ('borgo', 'Borgo'),
    ('foundations', 'Foundations'), ('office star', 'Office Star Products'),
    ('fellowes', 'Fellowes'), ('tayco', 'Tayco'), ('allseating', 'Allseating'),
]

# Direct manufacturer name in free text (word-boundary, case-insensitive) -> HIGH
DIRECT_NAMES = [
    (r'Global\s+Furniture\s+Group', GLOBAL), (r'Global\s+Furniture', GLOBAL),
    (r'Global\s+Upholstery', GLOBAL), (r'Teknion', 'Teknion'),
    (r'Humanscale', 'Humanscale'), (r'Steelcase', 'Steelcase'),
    (r'Keilhauer', 'Keilhauer'), (r'Ergo\s*Centric', 'ErgoCentric'),
    (r'Heartwood', 'Heartwood'), (r'Safco', 'Safco'), (r'Kensington', 'Kensington'),
    (r'Fire\s*King', 'FireKing'), (r'Herman[-\s]Miller', 'Herman Miller'),
]
HON_TOKEN = re.compile(r'\bHON\b')  # case-sensitive + furniture context

MODEL_CODES = [
    (re.compile(r'\bMVL-?\d{3,4}\b', re.I), GLOBAL, 'MVL Ibex line'),
    (re.compile(r'\b(2400|2424|2670)\b'), GLOBAL, 'Concorde line code'),
    (re.compile(r'\b2130SL\b', re.I), 'Safco', '2130SL Active Collection'),
    (re.compile(r'\bKX-\d+\b', re.I), 'Kensington', 'KX- pattern'),
]

SUB_BRANDS = [
    (r'Offices\s+To\s+Go', 'Offices To Go'), (r'\bOTG\b', 'OTG'),
    (r'ObusForme', 'ObusForme'), (r'\bBasics\b', 'Basics'),  # Basics needs ctx
]

PRODUCT_LINES = [
    (['Concorde', 'Ibex', 'Vion', 'Ergo Boss'], GLOBAL),
    (['Aeron', 'Mirra', 'Embody', 'Eames', 'Verus'], 'Herman Miller'),
    (['Freedom', 'Liberty', 'Diffrient', 'eFloat', 'Quattro'], 'Humanscale'),
    (['Leap', 'Gesture', 'Amia', 'Series 1'], 'Steelcase'),
]
AMBIG_LINES = {'Wind', 'World', 'Nova', 'Freedom', 'Liberty', 'Accord', 'Leap',
               'Gesture', 'Quattro'}

DESIGNERS = [('Zooey Chu', GLOBAL), ('Bill Stumpf', 'Herman Miller'),
             ('Niels Diffrient', 'Humanscale')]

# vendor -> brand tag slug
SLUG = {
    GLOBAL: 'global-furniture-group', 'Teknion': 'teknion', 'Humanscale': 'humanscale',
    'Steelcase': 'steelcase', 'Keilhauer': 'keilhauer', 'ErgoCentric': 'ergocentric',
    'Heartwood': 'heartwood', 'Safco': 'safco', 'Kensington': 'kensington',
    'FireKing': 'fireking', 'HON': 'hon', 'Herman Miller': 'herman-miller',
    'Office Star Products': 'office-star-products', 'Borgo': 'borgo',
    'Foundations': 'foundations', 'Sentry Safe': 'sentry-safe', 'deflecto': 'deflecto',
    'Gardex': 'gardex', '3M': '3m', 'Victor': 'victor', 'Fellowes': 'fellowes',
    'Tayco': 'tayco', 'Allseating': 'allseating', 'Screenflex': 'screenflex',
    'Links Contract Furniture': 'links-contract-furniture',
}

SERVICE_RX = re.compile(r'\b(delivery|installation|freight|surcharge|tailgate)\b', re.I)
SERVICE_SKU = re.compile(r'^(DELIV|INSTA|INSTALL|FREIGHT|ASSTD)', re.I)
FURNITURE_CTX = re.compile(
    r'\b(chair|desk|table|stool|cabinet|storage|seating|workstation|filing|drawer|'
    r'bookcase|lounge|sofa|panel|screen|ergonomic|task|office|furniture|credenza|'
    r'hutch|pedestal|bench|recliner|footrest|monitor|keyboard|reception|conference|'
    r'guest|executive|drafting|riser|stand|locker)\b', re.I)


def strip_html_text(h):
    if not h:
        return ''
    t = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


def map_structured(val):
    v = val.strip().lower()
    for needle, vendor in STRUCTURED_NAME:
        if needle in v:
            return vendor
    return None


CONF_RANK = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}


def scan_product(p):
    title = p.get('title') or ''
    body = strip_html_text(p.get('descriptionHtml'))
    ptype = p.get('productType') or ''
    tags = p.get('tags') or []
    skus = [v['node'].get('sku') or '' for v in p['variants']['edges']]
    sku = next((s.strip() for s in skus if s.strip()), '')
    sku_pref = (re.match(r'^([A-Za-z]+)', sku).group(1).upper() if re.match(r'^([A-Za-z]+)', sku) else '')
    mfs = {f"{e['node']['namespace']}.{e['node']['key']}": (e['node'].get('value') or '')
           for e in p['metafields']['edges']}

    base = {
        'product_id': p['legacyResourceId'], 'product_handle': p['handle'],
        'current_title': title, 'current_vendor': p.get('vendor'),
        'current_body_first_200': body[:200], 'product_type': ptype,
        'sku_sample': sku, 'sku_prefix': sku_pref,
        'detected_manufacturer': 'NONE', 'confidence': 'UNKNOWN',
        'evidence_summary': '', 'recommended_vendor_correction': 'NONE',
        'sub_brand_detected': '', 'ambiguous_prefix': '', 'decision': '',
        '_evidence': [],
    }

    # --- 1. service / non-product guard ---
    if SERVICE_RX.search(title) or SERVICE_SKU.match(sku) or re.match(r'^(Delivery|Installation)', title, re.I):
        base.update(evidence_summary='service/non-product line item (delivery/installation/etc.)',
                    decision='SKIP', confidence='UNKNOWN', detected_manufacturer='NONE')
        return base

    evidence, manuf_conf, sub_brand = [], {}, None

    def add(manuf, conf, sig, matched, loc):
        evidence.append({'signal_type': sig, 'matched_text': matched, 'location': loc,
                         'manufacturer': manuf, 'confidence': conf})
        if manuf and manuf != 'NONE':
            if manuf not in manuf_conf or CONF_RANK[conf] > CONF_RANK[manuf_conf[manuf]]:
                manuf_conf[manuf] = conf

    fields = {'title': title, 'body': body[:6000], 'tags': ' '.join(tags),
              'variant': ' '.join(v['node'].get('title') or '' for v in p['variants']['edges'])}
    ctx = bool(FURNITURE_CTX.search(f'{title} {body} {ptype}'))

    # --- 2. structured body fields ---
    mm = re.search(r'\bManufacturer\s+([A-Z][A-Za-z0-9.,&/ ]{2,40}?)\s+(?:Manufacturer Ref|Brand|Item Code)', body)
    if mm:
        v = map_structured(mm.group(1))
        if v:
            add(v, 'HIGH', 'direct_name_match', f'Manufacturer={mm.group(1).strip()}', 'body')
    bm = re.search(r'\bBrand\s+([A-Za-z0-9][A-Za-z0-9.,&/ ]{1,30}?)\s+(?:Item Code|Manufacturer|$)', body)
    if bm:
        v = map_structured(bm.group(1))
        if v:
            add(v, 'HIGH', 'direct_name_match', f'Brand={bm.group(1).strip()}', 'body')
            if 'offices to go' in bm.group(1).strip().lower() and sub_brand is None:
                sub_brand = 'Offices To Go'

    # --- 3. SKU prefix (model-code equivalent) ---
    for stem, vendor in PREFIX_MAP:
        if sku_pref == stem or sku.upper().startswith(stem):
            add(vendor, 'HIGH', 'model_code', f'SKU prefix {stem}', 'sku')
            break

    # specs.manufacturer metafield
    mf = mfs.get('specs.manufacturer', '').strip()
    if mf:
        v = map_structured(mf) or (mf if mf in SLUG else None)
        if v:
            add(v, 'HIGH', 'direct_name_match', f'specs.manufacturer={mf}', 'metafield')

    # existing brand:* tags
    for t in tags:
        m = re.match(r'brand:(.+)', t.strip(), re.I)
        if m:
            slug = m.group(1).strip().lower()
            vendor = next((v for v, s in SLUG.items() if s == slug), None)
            if vendor:
                add(vendor, 'HIGH', 'direct_name_match', t, 'tags')

    # --- 4. direct names in free text ---
    for loc in ('title', 'body', 'tags', 'variant'):
        for pat, vendor in DIRECT_NAMES:
            m = re.search(r'\b' + pat + r'\b', fields[loc], re.I)
            if m:
                add(vendor, 'HIGH' if loc in ('title', 'body') else 'MEDIUM',
                    'direct_name_match', m.group(0), loc)
    for loc in ('title', 'body'):
        if HON_TOKEN.search(fields[loc]) and ctx:
            add('HON', 'HIGH', 'direct_name_match', 'HON', loc)
            break

    # --- 5. model-code regexes ---
    for loc in ('sku', 'title', 'body'):
        text = sku if loc == 'sku' else fields[loc]
        for rx, vendor, desc in MODEL_CODES:
            m = rx.search(text)
            if m:
                add(vendor, 'HIGH', 'model_code', f'{m.group(0)} ({desc})', loc)

    # --- 6. sub-brands -> Global (MEDIUM) ---
    for loc in ('title', 'body', 'tags'):
        for pat, name in SUB_BRANDS:
            m = re.search(pat, fields[loc], re.I)
            if m:
                if name == 'Basics' and not ctx:
                    continue
                add(GLOBAL, 'MEDIUM', 'sub_brand', m.group(0), loc)
                if sub_brand is None:
                    sub_brand = name

    # --- 7. product lines (MEDIUM) ---
    for loc in ('title', 'body'):
        for names, vendor in PRODUCT_LINES:
            for name in names:
                if re.search(r'\b' + re.escape(name) + r'\b', fields[loc], re.I):
                    if name in AMBIG_LINES and not ctx:
                        continue
                    add(vendor, 'MEDIUM', 'product_line', name, loc)

    # --- 8. designers (LOW) ---
    for loc in ('title', 'body'):
        for name, vendor in DESIGNERS:
            if re.search(r'\b' + re.escape(name) + r'\b', fields[loc], re.I):
                add(vendor, 'LOW', 'designer', name, loc)

    # --- resolve ---
    if manuf_conf:
        ev_count = Counter(e['manufacturer'] for e in evidence)
        detected = max(manuf_conf, key=lambda m: (CONF_RANK[manuf_conf[m]], ev_count[m]))
        confidence = manuf_conf[detected]
        base.update(detected_manufacturer=detected, confidence=confidence,
                    recommended_vendor_correction=detected, sub_brand_detected=sub_brand or '')
    else:
        # nothing detected — flag the SKU prefix for Leo to decode
        base['ambiguous_prefix'] = sku_pref or '(no-sku)'

    base['evidence_summary'] = '; '.join(
        f"[{e['confidence']}] {e['signal_type']}:'{e['matched_text']}' in {e['location']}->{e['manufacturer']}"
        for e in evidence) or (f'no manufacturer signal; sku_prefix={sku_pref or "none"}')
    base['_evidence'] = evidence
    return base


def main():
    print('Fetching BBI-vendored products via GraphQL...', file=sys.stderr)
    products = fetch_all()
    print(f'Total fetched: {len(products)}', file=sys.stderr)
    rows = [scan_product(p) for p in products]

    cols = ['product_id', 'product_handle', 'current_title', 'current_vendor',
            'current_body_first_200', 'detected_manufacturer', 'confidence',
            'evidence_summary', 'recommended_vendor_correction', 'sub_brand_detected',
            'decision', 'product_type', 'sku_sample', 'sku_prefix', 'ambiguous_prefix']
    out_csv = ROOT / 'data' / 'reports' / f'brand-recovery-{DATE}.csv'
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    (ROOT / 'data' / 'reports' / f'brand-recovery-{DATE}-evidence.json').write_text(json.dumps(rows, indent=2))

    by_conf = defaultdict(list)
    for r in rows:
        by_conf[r['confidence']].append(r)
    svc = [r for r in rows if r['decision'] == 'SKIP']

    def bd(rs):
        return ', '.join(f'{m}={n}' for m, n in Counter(r['detected_manufacturer'] for r in rs).most_common())

    print('\n' + '=' * 54)
    print('BRAND-RECOVERY SCAN COMPLETE')
    print('=' * 54)
    print(f'Total BBI-vendored products scanned: {len(rows)}')
    print(f'  (of which service/non-product line-items auto-SKIP: {len(svc)})\n')
    print('Confidence distribution:')
    for tier in ('HIGH', 'MEDIUM', 'LOW', 'UNKNOWN'):
        rs = by_conf.get(tier, [])
        print(f'  {tier:8s}: {len(rs):4d}  {bd(rs) if tier != "UNKNOWN" else ""}')
    top = Counter(r['detected_manufacturer'] for r in rows
                  if r['confidence'] in ('HIGH', 'MEDIUM') and r['detected_manufacturer'] != 'NONE')
    print('\nTop detected manufacturers (HIGH+MEDIUM):')
    for m, n in top.most_common():
        print(f'  {m}: {n}')
    amb = Counter(r['ambiguous_prefix'] for r in rows if r['ambiguous_prefix'])
    print('\nAmbiguous SKU prefixes needing decode (UNKNOWN, not service):')
    for pfx, n in amb.most_common():
        ex = next((r['sku_sample'] for r in rows if r['ambiguous_prefix'] == pfx and r['sku_sample']), '')
        sample = next((r['current_title'][:38] for r in rows if r['ambiguous_prefix'] == pfx), '')
        print(f'  {pfx:12s} {n:3d}  e.g. {ex:24s} | {sample}')
    print(f'\nWorksheet: {out_csv.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
