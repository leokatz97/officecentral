#!/usr/bin/env python3
"""CATALOG — 225 vendor=BBI re-sourcing (READ-ONLY scan, 2026-06-02).

Carry-forward from the 2026-05-30 brand-recovery audit (PR #62, 183 corrected,
204 left UNKNOWN). Since then the SKU-prefix lookup gained deterministic decodes
for HDL / IOF / RIC / HZN / MTY (data/reference/sku-prefix-lookup.yaml). This
re-scan applies the now-richer lookup over the LIVE vendor="Brant Business
Interiors" residual (~221) and classifies each:

  CONFIDENT  — clear deterministic signal (SKU-prefix / MPN / unambiguous name)
  AMBIGUOUS  — no clear or conflicting signal -> flag for Steve, do NOT guess

Signal priority (highest first), per VENDOR-BBI-IS-ALWAYS-A-DATA-ERROR +
SKU-PREFIX-PATTERNS-ARE-DETERMINISTIC:
  1. Service/non-product line-item guard (Delivery/Installation) -> SKIP
  2. SKU prefix mapped to a known manufacturer (deterministic primary)  -> CONFIDENT
  3. Structured "Manufacturer {Name}" / "Brand {Name}" body field      -> CONFIDENT
  4. Direct manufacturer name in title/body                            -> CONFIDENT
  5. Model-code regex                                                  -> CONFIDENT
  6. Existing brand:* tag                                              -> CONFIDENT
  7. Sub-brand (Offices To Go / OTG / ObusForme / Basics)              -> CONFIDENT->Global
  8. Otherwise: record SKU prefix as ambiguous_prefix                  -> AMBIGUOUS

No writes to Shopify. No theme files touched.
Output: data/reports/bbi-resourcing-2026-06-02.csv (+ -evidence.json)
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
DATE = '2026-06-02'

QUERY = '''
query($cursor: String) {
  products(first: 100, after: $cursor, query: "vendor:'Brant Business Interiors'") {
    pageInfo { hasNextPage endCursor }
    edges { node {
      id legacyResourceId handle title vendor productType descriptionHtml tags
      variants(first: 50) { edges { node { sku title barcode } } }
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
# Canonical vendor names + deterministic SKU-prefix lookup
# (synced with data/reference/sku-prefix-lookup.yaml, 2026-06-02)
# ---------------------------------------------------------------------------
GLOBAL = 'Global Furniture Group'

# SKU-prefix stem -> canonical vendor. Match by uppercased-SKU startswith,
# longest stem first. CONFIDENT (deterministic) signal.
PREFIX_MAP = [
    # Global Furniture Group family
    ('GLBMV', GLOBAL), ('GLBML', GLOBAL), ('GLBM', GLOBAL), ('GLBD', GLOBAL),
    ('GLBN', GLOBAL), ('GLBC', GLOBAL), ('GLB', GLOBAL), ('GLO', GLOBAL),
    ('OFGO', GLOBAL), ('OTG', GLOBAL), ('MVL', GLOBAL),
    # Single manufacturers (Session 3)
    ('SAF', 'Safco'), ('HTW', 'Heartwood'), ('OSP', 'Office Star Products'),
    ('SEN', 'Sentry Safe'), ('DEF', 'deflecto'), ('GDX', 'Gardex'),
    ('BORGO', 'Borgo'), ('FOU', 'Foundations'), ('FEL', 'Fellowes'),
    ('TAYCO', 'Tayco'), ('TAY', 'Tayco'), ('ALLSE', 'Allseating'),
    ('LCF', 'Links Contract Furniture'), ('MMM', '3M'), ('VCT', 'Victor'),
    ('MTY', 'MityBilt'),
    # --- Newly decoded 2026-05-31 wrap-up (the carry-forward unblock) ---
    # HDL folded into 'Heartwood' per Leo 2026-06-02 (same brand family as HTW;
    # keeps a single clean brand:heartwood chip in the Brand filter).
    ('HDL', 'Heartwood'),                     # was "Heartwood Distributors Ltd." — folded
    ('IOF', 'Intelligent Office Furniture'),  # Canadian-made manufacturer
    ('RIC', 'Richelieu'),                     # ergo accessories (numeric MPN exact matches)
    ('HZN', 'Horizon Furniture'),             # distributor (seating + accessories)
]
PREFIX_MAP.sort(key=lambda x: -len(x[0]))  # longest stem first

# TIER-2 deterministic sub-code / product-line prefixes — locked in
# sku-prefix-lookup.yaml `decoded_details` + manufacturer-defaults.yaml.
# These are the SAME confidence as a top-level prefix (explicitly locked),
# but flagged tier-2 so the HALT review can eyeball the inference.
# HDL/Innovations/Levels family folded into 'Heartwood' per Leo 2026-06-02.
HEARTWOOD_DIST = 'Heartwood'
IOF = 'Intelligent Office Furniture'
SUBCODE_MAP = [
    # Heartwood Distributors — Innovations (INV*) + Levels (LEV*) + lines
    ('INVCOFREC', HEARTWOOD_DIST), ('INVREC', HEARTWOOD_DIST), ('INVMP', HEARTWOOD_DIST),
    ('INVR', HEARTWOOD_DIST), ('INV', HEARTWOOD_DIST), ('INNO', HEARTWOOD_DIST),
    ('LEVELS', HEARTWOOD_DIST), ('LEVSR', HEARTWOOD_DIST), ('LEV', HEARTWOOD_DIST),
    ('TUCANA', HEARTWOOD_DIST), ('SOHO', HEARTWOOD_DIST), ('UPSCALE', HEARTWOOD_DIST),
    # Intelligent Office Furniture — Universal casegoods (UN) + racetrack tables (RAPB)
    ('UN', IOF), ('RAPB', IOF),
    # Newland value desking line -> manufacturer = Global Furniture Group
    ('NLP', GLOBAL),
]
SUBCODE_MAP.sort(key=lambda x: -len(x[0]))

# Prefixes explicitly NOT decoded -> always AMBIGUOUS (Steve confirmation required)
UNDECODED_PREFIXES = {'SCN'}

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
    'Links Contract Furniture': 'links-contract-furniture', 'MityBilt': 'mitybilt',
    # newly decoded
    'Heartwood Distributors Ltd.': 'heartwood-distributors-ltd',
    'Intelligent Office Furniture': 'intelligent-office-furniture',
    'Richelieu': 'richelieu', 'Horizon Furniture': 'horizon-furniture',
}

STRUCTURED_NAME = [
    ('global upholstery', GLOBAL), ('offices to go', GLOBAL), ('global', GLOBAL),
    ('deflecto', 'deflecto'), ('gardex', 'Gardex'), ('sentry', 'Sentry Safe'),
    ('heartwood', 'Heartwood'), ('safco', 'Safco'), ('victor', 'Victor'),
    ('3m', '3M'), ('screenflex', 'Screenflex'),
    ('links contract', 'Links Contract Furniture'), ('borgo', 'Borgo'),
    ('foundations', 'Foundations'), ('office star', 'Office Star Products'),
    ('fellowes', 'Fellowes'), ('tayco', 'Tayco'), ('allseating', 'Allseating'),
    ('intelligent office', 'Intelligent Office Furniture'),
    ('richelieu', 'Richelieu'), ('horizon', 'Horizon Furniture'),
    ('mitybilt', 'MityBilt'), ('mity-lite', 'MityBilt'),
]

DIRECT_NAMES = [
    (r'Global\s+Furniture\s+Group', GLOBAL), (r'Global\s+Furniture', GLOBAL),
    (r'Global\s+Upholstery', GLOBAL), (r'Teknion', 'Teknion'),
    (r'Humanscale', 'Humanscale'), (r'Steelcase', 'Steelcase'),
    (r'Keilhauer', 'Keilhauer'), (r'Ergo\s*Centric', 'ErgoCentric'),
    (r'Heartwood', 'Heartwood'), (r'Safco', 'Safco'), (r'Kensington', 'Kensington'),
    (r'Fire\s*King', 'FireKing'), (r'Herman[-\s]Miller', 'Herman Miller'),
    (r'Office\s+Star', 'Office Star Products'), (r'Allseating', 'Allseating'),
    (r'Richelieu', 'Richelieu'), (r'Intelligent\s+Office\s+Furniture', 'Intelligent Office Furniture'),
    (r'MityBilt', 'MityBilt'), (r'Mity[-\s]?Lite', 'MityBilt'),
    (r'Screenflex', 'Screenflex'),          # room dividers — distinct brand
    (r'Shoptech', 'Horizon Furniture'),     # Horizon sub-line (decoded_details)
    (r'Foundations\s+(?:Worldwide|Next\s*Gen|SafeReach|Serenity)', 'Foundations'),
]
HON_TOKEN = re.compile(r'\bHON\b')

MODEL_CODES = [
    (re.compile(r'\bMVL-?\d{3,4}[A-Z]?\b', re.I), GLOBAL, 'MVL Ibex line'),
    (re.compile(r'\b(2400|2424|2670)\b'), GLOBAL, 'Concorde line code'),
    (re.compile(r'\b2130SL\b', re.I), 'Safco', '2130SL Active Collection'),
    (re.compile(r'\bKX-\d+\b', re.I), 'Kensington', 'KX- pattern'),
]

SUB_BRANDS = [
    (r'Offices\s+To\s+Go', 'Offices To Go'), (r'\bOTG\b', 'OTG'),
    (r'ObusForme', 'ObusForme'), (r'\bBasics\b', 'Basics'),
]

SERVICE_RX = re.compile(r'\b(delivery|installation|freight|surcharge|tailgate|'
                        r'disposal|dismantle|re-?assembl|recycl|additional\s+service)\b', re.I)
SERVICE_SKU = re.compile(r'^(DELIV|INSTA|INSTALL|FREIGHT|ASSTD|DISMANTLE|OCI-DISPOSAL)', re.I)
FURNITURE_CTX = re.compile(
    r'\b(chair|desk|table|stool|cabinet|storage|seating|workstation|filing|drawer|'
    r'bookcase|lounge|sofa|panel|screen|ergonomic|task|office|furniture|credenza|'
    r'hutch|pedestal|bench|recliner|footrest|monitor|keyboard|reception|conference|'
    r'guest|executive|drafting|riser|stand|locker)\b', re.I)

CONF_RANK = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}


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


def scan_product(p):
    title = p.get('title') or ''
    body = strip_html_text(p.get('descriptionHtml'))
    ptype = p.get('productType') or ''
    tags = p.get('tags') or []
    skus = [v['node'].get('sku') or '' for v in p['variants']['edges']]
    barcodes = [v['node'].get('barcode') or '' for v in p['variants']['edges']]
    sku = next((s.strip() for s in skus if s.strip()), '')
    barcode = next((b.strip() for b in barcodes if b.strip()), '')
    sku_pref = (re.match(r'^([A-Za-z]+)', sku).group(1).upper() if re.match(r'^([A-Za-z]+)', sku) else '')
    mfs = {f"{e['node']['namespace']}.{e['node']['key']}": (e['node'].get('value') or '')
           for e in p['metafields']['edges']}

    base = {
        'product_id': p['legacyResourceId'], 'product_handle': p['handle'],
        'current_title': title, 'current_vendor': p.get('vendor'),
        'current_body_first_200': body[:200], 'product_type': ptype,
        'sku_sample': sku, 'sku_prefix': sku_pref, 'barcode_sample': barcode,
        'detected_manufacturer': 'NONE', 'classification': 'AMBIGUOUS',
        'confidence': 'UNKNOWN', 'confidence_tier': '', 'primary_signal': '',
        'evidence_summary': '', 'recommended_vendor_correction': 'NONE',
        'sub_brand_detected': '', 'ambiguous_prefix': '', 'decision': '', '_evidence': [],
    }

    # --- 1. service / non-product guard ---
    if SERVICE_RX.search(title) or SERVICE_SKU.match(sku) or re.match(r'^(Delivery|Installation)', title, re.I):
        base.update(evidence_summary='service/non-product line item (delivery/installation/etc.)',
                    decision='SKIP', classification='SKIP', confidence='UNKNOWN')
        return base

    evidence, manuf_conf, sub_brand = [], {}, None
    primary = {'type': '', 'detail': ''}

    def add(manuf, conf, sig, matched, loc, primary_flag=False):
        evidence.append({'signal_type': sig, 'matched_text': matched, 'location': loc,
                         'manufacturer': manuf, 'confidence': conf})
        if manuf and manuf != 'NONE':
            if manuf not in manuf_conf or CONF_RANK[conf] > CONF_RANK[manuf_conf[manuf]]:
                manuf_conf[manuf] = conf
        if primary_flag and not primary['type']:
            primary['type'] = sig
            primary['detail'] = f'{matched} ({loc})'

    fields = {'title': title, 'body': body[:6000], 'tags': ' '.join(tags),
              'variant': ' '.join(v['node'].get('title') or '' for v in p['variants']['edges'])}
    ctx = bool(FURNITURE_CTX.search(f'{title} {body} {ptype}'))

    # --- 2a. SKU prefix — TIER 1 (top-level deterministic prefix) ---
    tier = ''
    for stem, vendor in PREFIX_MAP:
        if sku_pref == stem or sku.upper().startswith(stem):
            add(vendor, 'HIGH', 'sku_prefix', f'SKU prefix {stem} (e.g. {sku})', 'sku', primary_flag=True)
            tier = 'tier1'
            break

    # --- 2b. SKU sub-code — TIER 2 (locked decoded_details / documented line) ---
    if not tier:
        for stem, vendor in SUBCODE_MAP:
            if sku_pref == stem or sku.upper().startswith(stem):
                add(vendor, 'HIGH', 'sku_subcode', f'SKU sub-code {stem} (e.g. {sku})', 'sku', primary_flag=True)
                tier = 'tier2'
                break

    # --- 3. structured body fields ---
    mm = re.search(r'\bManufacturer\s+([A-Z][A-Za-z0-9.,&/ ]{2,40}?)\s+(?:Manufacturer Ref|Brand|Item Code)', body)
    if mm:
        v = map_structured(mm.group(1))
        if v:
            add(v, 'HIGH', 'structured_body', f'Manufacturer={mm.group(1).strip()}', 'body', primary_flag=True)
    bm = re.search(r'\bBrand\s+([A-Za-z0-9][A-Za-z0-9.,&/ ]{1,30}?)\s+(?:Item Code|Manufacturer|$)', body)
    if bm:
        v = map_structured(bm.group(1))
        if v:
            add(v, 'HIGH', 'structured_body', f'Brand={bm.group(1).strip()}', 'body', primary_flag=True)
            if 'offices to go' in bm.group(1).strip().lower() and sub_brand is None:
                sub_brand = 'Offices To Go'

    # specs.manufacturer metafield
    mf = mfs.get('specs.manufacturer', '').strip()
    if mf:
        v = map_structured(mf) or (mf if mf in SLUG else None)
        if v:
            add(v, 'HIGH', 'metafield_manufacturer', f'specs.manufacturer={mf}', 'metafield', primary_flag=True)

    # existing brand:* tags
    for t in tags:
        m = re.match(r'brand:(.+)', t.strip(), re.I)
        if m:
            slug = m.group(1).strip().lower()
            vendor = next((v for v, s in SLUG.items() if s == slug), None)
            if vendor:
                add(vendor, 'HIGH', 'existing_brand_tag', t, 'tags', primary_flag=True)

    # --- 4. direct names in free text ---
    for loc in ('title', 'body', 'tags', 'variant'):
        for pat, vendor in DIRECT_NAMES:
            m = re.search(r'\b' + pat + r'\b', fields[loc], re.I)
            if m:
                add(vendor, 'HIGH' if loc in ('title', 'body') else 'MEDIUM',
                    'direct_name', m.group(0), loc, primary_flag=(loc in ('title', 'body')))
    for loc in ('title', 'body'):
        if HON_TOKEN.search(fields[loc]) and ctx:
            add('HON', 'HIGH', 'direct_name', 'HON', loc, primary_flag=True)
            break

    # --- 5. model-code regexes ---
    for loc in ('sku', 'title', 'body'):
        text = sku if loc == 'sku' else fields[loc]
        for rx, vendor, desc in MODEL_CODES:
            m = rx.search(text)
            if m:
                add(vendor, 'HIGH', 'model_code', f'{m.group(0)} ({desc})', loc, primary_flag=True)

    # --- 6. sub-brands -> Global ---
    for loc in ('title', 'body', 'tags'):
        for pat, name in SUB_BRANDS:
            m = re.search(pat, fields[loc], re.I)
            if m:
                if name == 'Basics' and not ctx:
                    continue
                add(GLOBAL, 'MEDIUM', 'sub_brand', m.group(0), loc, primary_flag=True)
                if sub_brand is None:
                    sub_brand = name

    # --- resolve ---
    if manuf_conf:
        ev_count = Counter(e['manufacturer'] for e in evidence)
        detected = max(manuf_conf, key=lambda m: (CONF_RANK[manuf_conf[m]], ev_count[m]))
        confidence = manuf_conf[detected]
        # conflict check: more than one distinct HIGH-confidence manufacturer => AMBIGUOUS
        high_manufs = {m for m, c in manuf_conf.items() if c == 'HIGH'}
        classification = 'CONFIDENT' if (confidence == 'HIGH' and len(high_manufs) == 1) else \
                         ('CONFIDENT' if confidence == 'MEDIUM' and len({m for m in manuf_conf}) == 1 else 'AMBIGUOUS')
        # tier: tier1 if top-level prefix matched, else tier2 (sub-code/line/name/model)
        ctier = tier or ('tier2' if classification == 'CONFIDENT' else '')
        base.update(detected_manufacturer=detected, confidence=confidence,
                    classification=classification, confidence_tier=ctier,
                    recommended_vendor_correction=detected if classification == 'CONFIDENT' else 'NONE',
                    sub_brand_detected=sub_brand or '',
                    primary_signal=f"{primary['type']}: {primary['detail']}" if primary['type'] else '')
        if len(high_manufs) > 1:
            base['ambiguous_prefix'] = f'CONFLICT:{",".join(sorted(high_manufs))}'
    else:
        base['ambiguous_prefix'] = sku_pref or '(no-sku)'
        base['classification'] = 'AMBIGUOUS'

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
            'current_body_first_200', 'detected_manufacturer', 'classification',
            'confidence', 'confidence_tier', 'primary_signal', 'evidence_summary',
            'recommended_vendor_correction', 'sub_brand_detected', 'decision',
            'product_type', 'sku_sample', 'sku_prefix', 'barcode_sample', 'ambiguous_prefix']
    out_csv = ROOT / 'data' / 'reports' / f'bbi-resourcing-{DATE}.csv'
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    (ROOT / 'data' / 'reports' / f'bbi-resourcing-{DATE}-evidence.json').write_text(json.dumps(rows, indent=2))

    by_class = defaultdict(list)
    for r in rows:
        by_class[r['classification']].append(r)

    def bd(rs):
        return ', '.join(f'{m}={n}' for m, n in
                         Counter(r['detected_manufacturer'] for r in rs).most_common())

    confident = by_class.get('CONFIDENT', [])
    ambiguous = by_class.get('AMBIGUOUS', [])
    skip = by_class.get('SKIP', [])

    print('\n' + '=' * 60)
    print('BBI RE-SOURCING SCAN COMPLETE (2026-06-02)')
    print('=' * 60)
    t1 = [r for r in confident if r['confidence_tier'] == 'tier1']
    t2 = [r for r in confident if r['confidence_tier'] == 'tier2']
    print(f'Total vendor=BBI products scanned: {len(rows)}')
    print(f'  CONFIDENT (correctable): {len(confident)}  (tier1 top-prefix={len(t1)}, tier2 subcode/line/name={len(t2)})')
    print(f'  AMBIGUOUS (-> Steve):    {len(ambiguous)}')
    print(f'  SKIP (service items):    {len(skip)}\n')

    print('CONFIDENT manufacturer distribution:')
    for m, n in Counter(r['detected_manufacturer'] for r in confident).most_common():
        slug = SLUG.get(m, '???')
        print(f'  {m:34s} {n:4d}  -> brand:{slug}')

    print('\nCONFIDENT tier-2 promotions (review at HALT):')
    for r in t2:
        print(f"  [{r['detected_manufacturer'][:26]:26s}] {r['sku_sample'][:26]:26s} | {r['primary_signal'][:40]} | {r['current_title'][:30]}")

    print('\nCONFIDENT primary-signal breakdown:')
    for s, n in Counter(r['primary_signal'].split(':')[0] for r in confident).most_common():
        print(f'  {s:22s} {n}')

    print('\nAMBIGUOUS breakdown (by SKU prefix / reason):')
    amb = Counter(r['ambiguous_prefix'] for r in ambiguous)
    for pfx, n in amb.most_common():
        ex = next((r['sku_sample'] for r in ambiguous if r['ambiguous_prefix'] == pfx and r['sku_sample']), '')
        sample = next((r['current_title'][:42] for r in ambiguous if r['ambiguous_prefix'] == pfx), '')
        print(f'  {pfx:18s} {n:3d}  e.g. {ex:22s} | {sample}')

    print(f'\nWorksheet: {out_csv.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
