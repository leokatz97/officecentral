"""
PE-3 — Normalize product titles to `[Brand] [Product name] — [Key spec]`.

Pulls every active product from Shopify (read-only GraphQL), then proposes a
normalized title in sentence case, preserving brand casing (ergoCentric,
tCentric) and SKU/model codes. Flags low-confidence rows so a human can
decide rather than letting the script guess.

Output:
  data/reports/pe3-title-normalize-draft.csv
  Columns: handle, current_title, proposed_title, brand_detected,
           spec_detected, confidence, notes

No Anthropic API calls. No Shopify writes. No --live flag.

Usage:
  python3 scripts/normalize-pe3-titles.py
  python3 scripts/normalize-pe3-titles.py --limit=20
  python3 scripts/normalize-pe3-titles.py --handle=<handle>
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CSV = os.path.join(ROOT, 'data', 'reports', 'pe3-title-normalize-draft.csv')

ENV_PATH = os.path.join(ROOT, '.env')
if not os.path.exists(ENV_PATH):
    ENV_PATH = '/Users/leokatz/Desktop/Office Central/.env'

with open(ENV_PATH) as f:
    ENV = dict(line.strip().split('=', 1) for line in f
               if '=' in line and not line.startswith('#'))

# Task brief used SHOPIFY_API_TOKEN; reference script (draft-pe4-seo.py) uses
# SHOPIFY_TOKEN. Accept either so this works in both worktrees.
SHOPIFY_TOKEN = ENV.get('SHOPIFY_API_TOKEN') or ENV['SHOPIFY_TOKEN']
SHOPIFY_STORE = ENV.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')

GRAPHQL_URL = f'https://{SHOPIFY_STORE}/admin/api/2026-04/graphql.json'
SHOPIFY_HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_TOKEN,
    'Content-Type': 'application/json',
}

CSV_FIELDS = [
    'handle',
    'current_title',
    'proposed_title',
    'brand_detected',
    'spec_detected',
    'confidence',
    'notes',
]

# ---------------------------------------------------------------------------
# Brand registry — canonical casing preserved on output.
# Order matters: longer / more specific patterns must come BEFORE shorter ones
# so "Global Furniture Group" is matched before "Global".
# ---------------------------------------------------------------------------
BRANDS_CANONICAL: list[tuple[str, str]] = [
    # (match_pattern_lowercase, canonical_casing)
    ('global furniture group', 'Global Furniture Group'),
    ('groupe lacasse', 'Groupe Lacasse'),
    ('heartwood manufacturing', 'Heartwood Manufacturing'),
    ('spec furniture', 'Spec Furniture'),
    ('borgo seating', 'Borgo Seating'),
    ('three h', 'Three H'),
    ('ofgo studio', 'OFGO Studio'),
    ('obusforme', 'ObusForme'),
    ('ergocentric', 'ergoCentric'),
    ('tcentric', 'tCentric'),
    ('keilhauer', 'Keilhauer'),
    ('nienkämper', 'Nienkämper'),
    ('nienkamper', 'Nienkämper'),
    ('allseating', 'Allseating'),
    ('teknion', 'Teknion'),
    ('lacasse', 'Groupe Lacasse'),
    ('artopex', 'Artopex'),
    ('logiflex', 'Logiflex'),
    ('swiftspace', 'Swiftspace'),
    ('ezobord', 'ezoBord'),
    ('tayco', 'Tayco'),
    ('krug', 'Krug'),
    ('borgo', 'Borgo Seating'),
    ('ofgo', 'OFGO Studio'),
    ('offices to go', 'Offices to Go'),
    ('global', 'Global'),
]

# Vendor-string fallbacks (Shopify vendor field) → canonical brand.
VENDOR_TO_BRAND: dict[str, str] = {
    'global': 'Global',
    'global furniture group': 'Global Furniture Group',
    'teknion': 'Teknion',
    'keilhauer': 'Keilhauer',
    'krug': 'Krug',
    'tayco': 'Tayco',
    'allseating': 'Allseating',
    'ergocentric': 'ergoCentric',
    'obusforme': 'ObusForme',
    'lacasse': 'Groupe Lacasse',
    'groupe lacasse': 'Groupe Lacasse',
    'logiflex': 'Logiflex',
    'artopex': 'Artopex',
    'three h': 'Three H',
    'heartwood': 'Heartwood Manufacturing',
    'spec furniture': 'Spec Furniture',
    'borgo': 'Borgo Seating',
    'nienkamper': 'Nienkämper',
    'nienkämper': 'Nienkämper',
    'ofgo': 'OFGO Studio',
    'ofgo studio': 'OFGO Studio',
    'swiftspace': 'Swiftspace',
    'ezobord': 'ezoBord',
}

# Tokens that must stay capitalized as proper nouns / acronyms even in
# sentence-cased product names.
KEEP_CAPS = {
    'L-Shape', 'L-shape', 'U-Shape', 'U-shape', 'T-Shape',
    'OECM', 'BBI', 'LED', 'USB', 'PVC', 'HDPE', 'ABS', 'IT',
    'MDF', 'HPL', 'MFC', 'EU', 'AC', 'DC',
}

# Spec-detection patterns.
# Trailing word boundary intentionally omitted on RE_SIZE_AB so the inch mark
# at the very end (`...29"`) is included in the match.
RE_SIZE_AB = re.compile(
    r"""(?<![A-Za-z0-9])\d+(?:\.\d+)?["']?\s*[xX×]\s*\d+(?:\.\d+)?["']?(?:\s*[xX×]\s*\d+(?:\.\d+)?["']?)?"""
)
RE_SIZE_SINGLE = re.compile(r'(?<![A-Za-z0-9])\d+(?:\.\d+)?["\']')
RE_MODEL_CODE = re.compile(r'^[A-Z0-9-]{2,}$')  # per brief
RE_MULTI_OPTION = re.compile(r'\b(\d+)\s*(sizes?|colou?rs?|finishes?|options?|drawers?)\b', re.IGNORECASE)

KNOWN_FINISHES = {
    'oak', 'walnut', 'maple', 'cherry', 'mahogany', 'beech', 'birch', 'ash',
    'laminate', 'veneer', 'mesh', 'leather', 'vinyl', 'fabric', 'polyurethane',
}
KNOWN_COLOURS = {
    'black', 'white', 'grey', 'gray', 'charcoal', 'silver', 'chrome',
    'navy', 'blue', 'red', 'green', 'beige', 'taupe', 'graphite',
}

PRODUCT_TYPES = {
    'chair', 'chairs', 'desk', 'desks', 'table', 'tables', 'cabinet', 'cabinets',
    'workstation', 'workstations', 'bookcase', 'bookcases', 'sofa', 'sofas',
    'lounge', 'stool', 'stools', 'bench', 'benches', 'shelf', 'shelves',
    'shelving', 'storage', 'pedestal', 'pedestals', 'credenza', 'hutch',
    'screen', 'screens', 'panel', 'panels', 'lectern', 'podium', 'reception',
    'partition', 'pod', 'pods', 'booth',
}


# ---------------------------------------------------------------------------
# Shopify GraphQL — bulk paginated fetch of active products
# ---------------------------------------------------------------------------
def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    for attempt in range(5):
        req = urllib.request.Request(GRAPHQL_URL, data=payload,
                                     headers=SHOPIFY_HEADERS, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = 2 + attempt * 2
                print(f'  · Shopify {e.code} — backoff {wait}s', file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        if data.get('errors'):
            err = json.dumps(data['errors'])[:300]
            if 'THROTTLED' in err.upper():
                time.sleep(2 + attempt * 2)
                continue
            raise RuntimeError(f'GraphQL errors: {err}')
        return data['data']
    raise RuntimeError('GraphQL gave up after retries')


PRODUCTS_QUERY = """
query Products($cursor: String) {
  products(first: 100, after: $cursor, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        handle
        title
        vendor
        productType
        tags
      }
    }
  }
}
"""


def fetch_all_active_products() -> list[dict]:
    out: list[dict] = []
    cursor = None
    page = 0
    while True:
        page += 1
        data = gql(PRODUCTS_QUERY, {'cursor': cursor})
        edges = data['products']['edges']
        for e in edges:
            n = e['node']
            out.append({
                'handle': n['handle'],
                'title': n['title'] or '',
                'vendor': (n.get('vendor') or '').strip(),
                'productType': (n.get('productType') or '').strip(),
                'tags': n.get('tags') or [],
            })
        info = data['products']['pageInfo']
        print(f'  page {page}: +{len(edges)} (total {len(out)})')
        if not info['hasNextPage']:
            break
        cursor = info['endCursor']
        time.sleep(0.4)
    return out


def fetch_one(handle: str) -> list[dict]:
    q = """
    query($h: String!) {
      productByHandle(handle: $h) {
        handle title vendor productType tags
      }
    }
    """
    data = gql(q, {'h': handle})
    n = data.get('productByHandle')
    if not n:
        return []
    return [{
        'handle': n['handle'],
        'title': n['title'] or '',
        'vendor': (n.get('vendor') or '').strip(),
        'productType': (n.get('productType') or '').strip(),
        'tags': n.get('tags') or [],
    }]


# ---------------------------------------------------------------------------
# Title parsing
# ---------------------------------------------------------------------------
def detect_brand(title: str, vendor: str) -> tuple[str, str]:
    """Return (canonical_brand, source). source ∈ {'title','vendor',''}."""
    t_low = title.lower()
    for needle, canon in BRANDS_CANONICAL:
        # Word-boundary-ish: avoid matching 'global' inside 'globalsomething'.
        # Allow brand to appear anywhere in title.
        pattern = r'(?<![a-z0-9])' + re.escape(needle) + r'(?![a-z0-9])'
        if re.search(pattern, t_low):
            return canon, 'title'
    v_low = vendor.lower()
    if v_low and v_low in VENDOR_TO_BRAND:
        return VENDOR_TO_BRAND[v_low], 'vendor'
    return '', ''


def strip_brand_from_title(title: str, brand: str) -> str:
    """Remove the matched brand prefix/occurrence from the title."""
    if not brand:
        return title
    # Try every canonical-cased variant + lowercase + uppercase + title-case.
    for variant in {brand, brand.lower(), brand.upper(), brand.title()}:
        idx = title.lower().find(variant.lower())
        if idx >= 0:
            return (title[:idx] + title[idx + len(variant):]).strip(' -—|·')
    return title


def extract_spec(remaining: str) -> tuple[str, str]:
    """Look at the tail of the remaining title for a key spec.

    Returns (spec_string, kind). kind ∈
      {'size','model','multi-option','colour','finish',''}
    Empty string if no clear spec found.
    """
    text = remaining.strip()

    # Multi-option pattern wins: "(8 Sizes & 9 Colour options)" → 8 sizes
    m = RE_MULTI_OPTION.search(text)
    if m:
        return f'{m.group(1)} {m.group(2).lower()}', 'multi-option'

    # Size like 30x60, 6'x6', 96"x30" — prefer the LAST occurrence so we pick
    # the trailing dimensions in titles like "1" Shelf 32" Wide x 72" High"
    ab_matches = list(RE_SIZE_AB.finditer(text))
    if ab_matches:
        return ab_matches[-1].group(0).strip(), 'size'

    # Model code at end (preserve casing exactly as-is). Brief pins the regex
    # to ^[A-Z0-9-]{2,}$, but we additionally require a digit so we don't
    # mistake plain words ("EACH", "ABS") for SKUs.
    tokens = re.findall(r'[A-Za-z0-9-]+', text)
    if tokens:
        last = tokens[-1]
        if RE_MODEL_CODE.match(last) and any(c.isdigit() for c in last):
            return last, 'model'

    # Single-dimension like 96" — also prefer the last
    single_matches = list(RE_SIZE_SINGLE.finditer(text))
    if single_matches:
        return single_matches[-1].group(0).strip(), 'size'

    # Trailing colour / finish word
    last_word = re.findall(r'[A-Za-z]+', text)
    if last_word:
        lw = last_word[-1].lower()
        if lw in KNOWN_COLOURS:
            return last_word[-1].title(), 'colour'
        if lw in KNOWN_FINISHES:
            return last_word[-1].title(), 'finish'

    return '', ''


def sentence_case(name: str, restore_brand_tokens: bool = False,
                  brand: str = '') -> str:
    """Lowercase everything except: first word, KEEP_CAPS tokens, and
    tokens matching the model-code regex (with at least one digit).

    `restore_brand_tokens` is only set True when the brand actually
    appeared in the title (so the brand stripping might have left a
    sub-token behind that we want to re-case). When the brand came from
    the vendor field, we leave plain English words alone.
    """
    if not name:
        return name
    parts = re.split(r'(\s+|[-—|/&])', name)
    out: list[str] = []
    word_index = 0
    brand_tokens_lower = set(brand.lower().split()) if (restore_brand_tokens and brand) else set()
    for p in parts:
        if not p.strip() or re.match(r'^[\s\-—|/&]+$', p):
            out.append(p)
            continue
        token_clean = p.strip()
        kc_match = next((kc for kc in KEEP_CAPS if kc.lower() == token_clean.lower()), None)
        if kc_match:
            out.append(kc_match)
        elif RE_MODEL_CODE.match(token_clean) and any(c.isdigit() for c in token_clean):
            out.append(token_clean)
        elif token_clean.lower() in brand_tokens_lower:
            for needle, canon in BRANDS_CANONICAL:
                if token_clean.lower() == needle.split()[-1]:
                    out.append(canon.split()[-1])
                    break
            else:
                out.append(token_clean)
        elif word_index == 0:
            out.append(token_clean[:1].upper() + token_clean[1:].lower())
        else:
            out.append(token_clean.lower())
        word_index += 1
    return ''.join(out).strip()


def normalize(row: dict) -> dict:
    """Produce the proposed title + confidence for one product."""
    title = (row['title'] or '').strip()
    notes: list[str] = []

    if not title:
        return {
            'handle': row['handle'],
            'current_title': '',
            'proposed_title': '',
            'brand_detected': '',
            'spec_detected': '',
            'confidence': 'low',
            'notes': 'empty title',
        }

    brand, brand_source = detect_brand(title, row['vendor'])
    remaining = strip_brand_from_title(title, brand)

    # Strip surrounding pipes / em-dashes that were used as separators
    remaining = re.sub(r'^\s*[\|\-—–·]\s*', '', remaining)
    remaining = re.sub(r'\s*[\|\-—–·]\s*$', '', remaining).strip()

    spec, spec_kind = extract_spec(remaining)

    # Build product-name body: remove the spec substring from remaining (only
    # if the spec was a tail token, to avoid ripping mid-title text). Allow
    # any trailing punctuation between the spec and end-of-string.
    body = remaining
    if spec:
        m = re.search(re.escape(spec) + r'[\s\-—|·,&"\']*$', body, re.IGNORECASE)
        if m:
            body = body[:m.start()].rstrip(' -—|·,&').strip()
        else:
            notes.append('spec inline — not stripped from name')

    # Clean up duplicate whitespace and trailing punctuation
    body = re.sub(r'\s{2,}', ' ', body).strip(' -—|·,&')
    if not body:
        body = remaining  # fall back

    body_cased = sentence_case(body, restore_brand_tokens=(brand_source == 'title'), brand=brand)

    # Confidence scoring
    if brand and spec:
        confidence = 'high'
    elif brand or spec:
        confidence = 'medium'
    else:
        confidence = 'low'

    # Special downgrades
    if not brand:
        notes.append('no brand detected')
    elif brand_source == 'vendor':
        notes.append('brand from vendor field')

    if not spec:
        notes.append('no spec detected — name only')
    elif spec_kind == 'multi-option':
        notes.append('multi-variant; spec describes option count')

    # Compose proposed title
    parts = []
    if brand:
        parts.append(brand)
    if body_cased:
        parts.append(body_cased)
    head = ' '.join(parts).strip()
    if spec and head:
        proposed = f'{head} — {spec}'
    elif spec:
        proposed = spec
    else:
        proposed = head

    # Final guard: if proposed equals current (case-sensitive), note it
    if proposed.strip() == title.strip():
        notes.append('no change needed')

    return {
        'handle': row['handle'],
        'current_title': title,
        'proposed_title': proposed,
        'brand_detected': brand,
        'spec_detected': spec,
        'confidence': confidence,
        'notes': '; '.join(notes),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    args = sys.argv[1:]
    limit: int | None = None
    only_handle: str | None = None
    for a in args:
        if a.startswith('--limit='):
            limit = int(a.split('=', 1)[1])
        if a.startswith('--handle='):
            only_handle = a.split('=', 1)[1]

    print('PE-3 — title normalization (read-only).')
    print(f'Output: {OUT_CSV}')
    print()

    if only_handle:
        print(f'Fetching single product: {only_handle}')
        products = fetch_one(only_handle)
    else:
        print('Fetching all active products via Shopify GraphQL...')
        products = fetch_all_active_products()

    print(f'Active products: {len(products)}')
    if limit:
        products = products[:limit]
        print(f'Capped to first {limit} for this run.')

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    counts = {'high': 0, 'medium': 0, 'low': 0}
    written = 0

    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for p in products:
            row = normalize(p)
            w.writerow(row)
            counts[row['confidence']] = counts.get(row['confidence'], 0) + 1
            written += 1

    print()
    print('=' * 60)
    print(f'Wrote {written} rows to {OUT_CSV}')
    print(f'  high:   {counts["high"]:>4}')
    print(f'  medium: {counts["medium"]:>4}')
    print(f'  low:    {counts["low"]:>4}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
