#!/usr/bin/env python3
"""FEED-AUDIT analyzer (READ-ONLY) — operates on the cached catalog snapshot.

Produces:
  A) Part 1 feed-readiness per-product evaluation vs current GMC spec + summary.
  B) Part 2 vendor mis-tag candidates with HIGH / AMBIGUOUS / NON-BBI-CONFLICT
     classification (does NOT write — emits a worksheet the apply step consumes).

Inputs:  data/reports/_catalog-feed-snapshot-<date>.json
         data/reference/sku-prefix-lookup.yaml (single-manufacturer prefixes)
Outputs: data/reports/feed-readiness-<date>.json   (per-product + summary)
         data/reports/vendor-mistag-candidates-<date>.csv
"""
import json, re, html, sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATE = datetime.now().strftime('%Y-%m-%d')
SNAP = ROOT / 'data' / 'reports' / f'_catalog-feed-snapshot-{DATE}.json'
snap = json.loads(SNAP.read_text())
PRODUCTS = snap['products']

# ---- canonical vendor strings used in Steve's live catalog -----------------
GLOBAL = 'Global Furniture Group'
OTG = 'OTG / Offices to Go'
# Single-manufacturer SKU prefixes -> canonical vendor (NO sub-brand ambiguity).
# Global-family prefixes are handled separately (they split Global/OTG/ObusForme).
SINGLE_MFR_PREFIX = {
    'SAF': 'Safco', 'HTW': 'Heartwood Manufacturing', 'HDL': 'Heartwood Manufacturing',
    'OSP': 'Office Star Products', 'SEN': 'Sentry Safe', 'DEF': 'Deflecto',
    'GDX': 'Gardex', 'MMM': '3M', 'VCT': 'Victor Technology', 'FEL': 'Fellowes',
    'TAY': 'Tayco', 'TAYCO': 'Tayco', 'ALLSE': 'Allseating', 'MTY': 'MityBilt',
    'MYB': 'MityBilt', 'IOF': 'Intelligent Office Furniture', 'RIC': 'Richelieu',
    'HZN': 'Horizon', 'BORGO': 'Borgo', 'FOU': 'Foundations Worldwide',
    'KMW': 'Kensington', 'FIR': 'FireKing', 'FIRCF': 'FireKing', 'GDXGX': 'Gardex',
}
GLOBAL_FAMILY_PREFIX = ('GLB', 'GLO', 'MVL', 'OTG', 'OFGO', 'BAO', 'GLC')
SERVICE_PREFIX = ('DELIVERY', 'INSTALLATION', 'INSTALL', 'FREIGHT', 'DELIV', 'INSTA')
BBI_VENDORS = {'Brant Business Interiors', 'Office Central & Brant Business Interiors', '', None}

PROMO_RX = re.compile(r'\b(sale|free shipping|best price|cheap|discount|clearance|% off|deal of)\b', re.I)
SERVICE_RX = re.compile(r'\b(delivery|installation|freight|surcharge|tailgate|assembly fee)\b', re.I)


def strip_html(h):
    if not h:
        return ''
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def mfdict(p):
    return {f"{e['node']['namespace']}.{e['node']['key']}": (e['node'].get('value') or '')
            for e in p['metafields']['edges']}


def first_sku(p):
    for e in p['variants']['edges']:
        s = (e['node'].get('sku') or '').strip()
        if s:
            return s
    return ''


def prefix_of(sku):
    m = re.match(r'^([A-Za-z]+)', sku)
    return m.group(1).upper() if m else ''


def single_mfr_for_prefix(pref):
    """Longest-stem match against single-manufacturer prefixes."""
    for stem in sorted(SINGLE_MFR_PREFIX, key=len, reverse=True):
        if pref.startswith(stem):
            return SINGLE_MFR_PREFIX[stem]
    return None


def map_specs_manufacturer(val):
    """specs.manufacturer metafield -> canonical live vendor string."""
    v = (val or '').strip().lower()
    if not v:
        return None
    if 'obusforme' in v:
        return 'ObusForme'
    if 'offices to go' in v or re.search(r'\botg\b', v):
        return OTG
    if 'global' in v or 'basics' in v:
        return GLOBAL
    table = {
        'heartwood': 'Heartwood Manufacturing', 'safco': 'Safco', 'kensington': 'Kensington',
        'fireking': 'FireKing', 'fire king': 'FireKing', 'office star': 'Office Star Products',
        'deflecto': 'Deflecto', 'gardex': 'Gardex', 'sentry': 'Sentry Safe',
        'victor': 'Victor Technology', 'fellowes': 'Fellowes', 'tayco': 'Tayco',
        'allseating': 'Allseating', 'mitybilt': 'MityBilt', 'teknion': 'Teknion',
        'humanscale': 'Humanscale', 'intelligent office': 'Intelligent Office Furniture',
        'richelieu': 'Richelieu', 'horizon': 'Horizon', 'borgo': 'Borgo',
        'foundations': 'Foundations Worldwide', '3m': '3M', 'mergeworks': 'MergeWorks',
        'lesro': 'Lesro Industries', 'ergocentric': 'ErgoCentric', 'keilhauer': 'Keilhauer',
    }
    for needle, canon in table.items():
        if needle in v:
            return canon
    return None


def vendor_family(v):
    v = (v or '').lower()
    if 'global' in v or 'offices to go' in v or 'otg' in v or 'obusforme' in v:
        return 'Global'
    return v


# ===========================================================================
# PART 1 — feed readiness
# ===========================================================================
def audit_feed(p):
    status = p['status']
    vendor = p.get('vendor') or ''
    title = p.get('title') or ''
    body = strip_html(p.get('descriptionHtml'))
    ptype = (p.get('productType') or '').strip()
    mf = mfdict(p)
    gcat = mf.get('mm-google-shopping.google_product_category', '').strip()
    cat = p.get('category') or {}
    cat_set = bool(cat) and cat.get('name') not in (None, '', 'Uncategorized')
    sku = first_sku(p)
    variants = [e['node'] for e in p['variants']['edges']]
    v0 = variants[0] if variants else {}
    barcode = (v0.get('barcode') or '').strip()
    try:
        price = float(v0.get('price') or 0)
    except Exception:
        price = 0.0
    fi = p.get('featuredImage') or {}
    img_w, img_h = fi.get('width') or 0, fi.get('height') or 0
    dims = mf.get('specs.dimensions', '').strip()
    wt = mf.get('specs.weight', '').strip()
    vwt = ((v0.get('inventoryItem') or {}).get('measurement') or {}).get('weight') or {}
    vwt_val = vwt.get('value') or 0

    is_service = bool(SERVICE_RX.search(title)) or prefix_of(sku).startswith(SERVICE_PREFIX)

    errors, missing = [], []
    # brand
    if vendor in BBI_VENDORS:
        errors.append('brand=BBI/blank (not a manufacturer)')
    # identifier: gtin else mpn(sku)+brand
    if not barcode and not sku:
        errors.append('no identifier (no GTIN, no MPN/SKU)')
    elif not barcode and not sku and vendor in BBI_VENDORS:
        errors.append('identifier_exists fails (no gtin/mpn/brand)')
    # price
    if price <= 0:
        errors.append('price<=0 (feed-invalid; B2B quote page)')
    # image
    if not fi:
        errors.append('no image_link')
    elif img_w < 500 or img_h < 500:
        missing.append(f'image <500px ({img_w}x{img_h})')
    # title
    if len(title) > 150:
        missing.append(f'title >150 chars ({len(title)})')
    if PROMO_RX.search(title):
        missing.append('promo language in title')
    # description
    if len(body) < 50:
        missing.append(f'thin/no description ({len(body)} chars)')
    if re.search(r'<a\s|https?://', p.get('descriptionHtml') or ''):
        missing.append('link in description')
    # category / product_type
    if not gcat and not cat_set:
        missing.append('no google_product_category')
    if not ptype and not gcat and not cat_set:
        missing.append('no product_type/category at all')
    # dimensions / weight
    if not dims:
        missing.append('no dimensions (specs.dimensions)')
    if not wt and not vwt_val:
        missing.append('no shipping weight')

    if is_service:
        st = 'SERVICE-SKIP'
    elif errors:
        st = 'DATA-ERROR'
    elif missing:
        st = 'MISSING-ATTRIBUTES'
    else:
        st = 'READY'
    return {
        'id': p['legacyResourceId'], 'handle': p['handle'], 'status': status,
        'vendor': vendor, 'sku': sku, 'feed_status': st,
        'errors': errors, 'missing': missing,
    }


# ===========================================================================
# PART 2 — vendor mis-tag detection
# ===========================================================================
def detect_vendor(p):
    vendor = p.get('vendor') or ''
    sku = first_sku(p)
    pref = prefix_of(sku)
    mf = mfdict(p)
    title = p.get('title') or ''
    body = strip_html(p.get('descriptionHtml'))
    text = f'{title} {body}'.lower()
    tags = p.get('tags') or []

    is_service = bool(SERVICE_RX.search(title)) or pref.startswith(SERVICE_PREFIX)
    is_bbi = vendor in BBI_VENDORS

    # only care about: vendor=BBI/blank, OR vendor disagrees with a single-mfr prefix
    single = single_mfr_for_prefix(pref) if pref else None

    # DETERMINISTIC SKU-model override (sku-prefix-lookup.yaml: SKU is the primary
    # signal, more reliable than body/metafield text which can be corrupt).
    # Global's OWN part-number stems carry a Global/OTG product by definition;
    # ergoCentric/Heartwood/etc. do not use GLB part numbers. An MVL#### model is
    # an Offices To Go task-seating SKU (officestogo.com/.../<line>/MVL####).
    sku_u = sku.upper()
    GLOBAL_OWN = ('GLB', 'GLO', 'MVL', 'OTG', 'OFGO', 'BAO')
    own_global = any(pref.startswith(o) for o in GLOBAL_OWN)
    has_mvl_model = bool(re.search(r'\bMVL\d{3,4}\b', sku_u))

    # authoritative per-product signal — but a corrupt brand metafield on a
    # Global-own SKU must NOT mask the SKU truth, so we gate it below.
    spec_mfr = map_specs_manufacturer(mf.get('specs.manufacturer', ''))
    if own_global and spec_mfr and vendor_family(spec_mfr) != 'Global':
        spec_mfr = None  # metafield contradicts a deterministic Global-own SKU -> distrust it
    # brand: tag
    tag_vendor = None
    for t in tags:
        m = re.match(r'brand:(.+)', t.strip(), re.I)
        if m:
            slug = m.group(1).strip().lower()
            tag_map = {'global-furniture-group': GLOBAL, 'offices-to-go': OTG,
                       'heartwood': 'Heartwood Manufacturing', 'safco': 'Safco',
                       'mitybilt': 'MityBilt', 'office-star-products': 'Office Star Products'}
            tag_vendor = tag_map.get(slug)
            break
    sub_signal = None
    if re.search(r'offices\s+to\s+go|\botg\b', text):
        sub_signal = OTG
    elif 'obusforme' in text:
        sub_signal = 'ObusForme'

    if is_service:
        return None

    expected, conf, evidence = None, None, []
    if has_mvl_model:
        # deterministic: MVL#### is an Offices To Go model (officestogo.com)
        expected, conf = OTG, 'HIGH'
        _mvl = re.search(r'MVL\d{3,4}', sku_u).group(0)
        evidence.append(_mvl + ' = Offices To Go model (officestogo.com); deterministic SKU overrides brand metafield')
    elif spec_mfr:
        expected = spec_mfr
        conf = 'HIGH'
        evidence.append(f'specs.manufacturer->{spec_mfr}')
    elif single:
        expected = single
        conf = 'HIGH'
        evidence.append(f'SKU prefix {pref}->{single} (single-mfr)')
    elif pref.startswith(GLOBAL_FAMILY_PREFIX):
        if sub_signal == OTG:
            expected, conf = OTG, 'HIGH'
            evidence.append(f'Global-family prefix {pref} + "Offices To Go" text')
        elif sub_signal == 'ObusForme':
            expected, conf = 'ObusForme', 'HIGH'
            evidence.append(f'Global-family prefix {pref} + "ObusForme" text')
        else:
            expected, conf = GLOBAL, 'HIGH'
            evidence.append(f'Global-family prefix {pref}->{GLOBAL} (parent manufacturer)')
    elif tag_vendor:
        expected, conf = tag_vendor, 'MEDIUM'
        evidence.append(f'brand: tag->{tag_vendor}')
    else:
        expected, conf = None, 'AMBIGUOUS'
        evidence.append(f'no resolving signal; prefix={pref or "(none)"}')

    # is there a problem?
    if is_bbi:
        problem = 'vendor=BBI/blank'
    elif expected and vendor_family(vendor) != vendor_family(expected) and vendor.strip() != (expected or '').strip():
        problem = 'vendor disagrees with evidence'
    else:
        return None  # vendor already consistent

    # classification of the FIX
    if conf == 'AMBIGUOUS' or expected is None:
        cls = 'AMBIGUOUS'
    elif has_mvl_model:
        # deterministic documented model -> apply even if current vendor is a
        # (corrupt) non-BBI brand. This is the MVL2836/MVL2837 Part-Time case.
        cls = 'HIGH'
    elif not is_bbi:
        # human already set a non-BBI vendor that conflicts -> needs Steve's call
        cls = 'NON-BBI-CONFLICT'
    else:
        cls = 'HIGH' if conf == 'HIGH' else 'AMBIGUOUS'

    return {
        'id': p['legacyResourceId'], 'handle': p['handle'], 'status': p['status'],
        'current_vendor': vendor, 'sku': sku, 'prefix': pref,
        'expected_vendor': expected or '', 'confidence': conf,
        'problem': problem, 'classification': cls,
        'evidence': '; '.join(evidence), 'title': title[:80],
    }


def main():
    feed = [audit_feed(p) for p in PRODUCTS]
    active = [f for f in feed if f['status'] == 'ACTIVE']
    # summary
    fs = Counter(f['feed_status'] for f in active)
    gap = Counter()
    for f in active:
        for m in f['missing']:
            gap[re.sub(r'\(.*?\)', '', m).strip()] += 1
        for e in f['errors']:
            gap['[ERR] ' + re.sub(r'\(.*?\)', '', e).strip()] += 1

    cand = [c for c in (detect_vendor(p) for p in PRODUCTS) if c]
    cls_count = Counter(c['classification'] for c in cand)

    out = {
        'date': DATE, 'total_products': len(PRODUCTS),
        'active': len(active),
        'archived': sum(1 for p in PRODUCTS if p['status'] == 'ARCHIVED'),
        'feed_status_active': dict(fs),
        'gap_counts_active': dict(gap.most_common()),
        'vendor_mistag_classification': dict(cls_count),
        'feed_per_product': feed,
        'vendor_candidates': cand,
    }
    outp = ROOT / 'data' / 'reports' / f'feed-readiness-{DATE}.json'
    outp.write_text(json.dumps(out, indent=2))

    # csv for vendor candidates
    import csv
    cols = ['id', 'handle', 'status', 'current_vendor', 'expected_vendor', 'confidence',
            'classification', 'problem', 'prefix', 'sku', 'evidence', 'title']
    cpath = ROOT / 'data' / 'reports' / f'vendor-mistag-candidates-{DATE}.csv'
    with cpath.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(cand)

    # console summary
    print('=' * 60)
    print('FEED-READINESS (ACTIVE products = feed-eligible set)')
    print('=' * 60)
    print(f'Total products: {len(PRODUCTS)}  | ACTIVE: {len(active)}  | ARCHIVED: {out["archived"]}')
    rdy = fs.get('READY', 0)
    print(f'\nFeed status (ACTIVE): {dict(fs)}')
    print(f'Feed-ready %: {100*rdy/len(active):.1f}%  ({rdy}/{len(active)})')
    print('\nGap counts (ACTIVE):')
    for k, v in gap.most_common():
        print(f'  {v:4d}  {k}')
    print('\n' + '=' * 60)
    print('VENDOR MIS-TAG CANDIDATES')
    print('=' * 60)
    print(f'Total flagged: {len(cand)}  -> {dict(cls_count)}')
    print('\nHIGH-confidence fixes by expected vendor:')
    hi = Counter(c['expected_vendor'] for c in cand if c['classification'] == 'HIGH')
    for v, n in hi.most_common():
        print(f'  {n:3d}  -> {v}')
    print('\nHIGH fixes by status:')
    print('  ', Counter(c['status'] for c in cand if c['classification'] == 'HIGH'))
    print('\nAMBIGUOUS (flag for Steve):', cls_count.get('AMBIGUOUS', 0))
    print('NON-BBI-CONFLICT (flag for Steve):', cls_count.get('NON-BBI-CONFLICT', 0))
    print(f'\nWrote {outp.relative_to(ROOT)}')
    print(f'Wrote {cpath.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
