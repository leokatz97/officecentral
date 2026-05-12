# Prompt 4 — Pass 1: Product Triage (Audit, No Writes)

**Paste the safety preflight first (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.**

---

## Files to have in workspace before starting

Verify these exist at these paths. If any are missing, copy them in before pasting the prompt below.

| File | Workspace path |
|---|---|
| Strategy brief | `docs/strategy/product-enrichment-brief.md` |
| Voice anchor — descriptions | `data/reports/pe1-hero100-descriptions.csv` |
| Voice anchor — titles | `data/reports/pe3-hero100-titles.csv` |
| Voice anchor — SEO | `data/reports/pe7-longtail-seo.csv` |
| Spec research database | `data/specs/specs.json` |
| Hero 100 reference list | `data/reports/hero-100.csv` |
| Long-tail working set | `data/reports/longtail-products.csv` |
| ICP / audience | `docs/strategy/icp.md` |
| Approved voice samples | `docs/strategy/voice-samples.md` |

CLAUDE.md and `BBI-Session-Kickoff/bbi-build-state.md` auto-load via project rules.

---

## The prompt

```
You are working on the Brant Business Interiors Shopify catalog (read-only
for Pass 1). Store: office-central-online.myshopify.com.

PASS 1 of a multi-pass product enrichment workflow. Pass 1 = audit and
triage ONLY. You produce a single CSV that Steve reviews in Google Sheets
before any enrichment writes happen in Pass 2. NO product writes. NO theme
writes. NO metafield writes.

— READ THESE BEFORE STARTING —

Read each file fully. Confirm in chat that you've read them before
running any code.

  1. CLAUDE.md (auto-loaded — project rules + BBI guardrails)
  2. BBI-Session-Kickoff/01-safety-preflight.md (run the preflight check)
  3. docs/strategy/product-enrichment-brief.md (strategy + data quality
     snapshot — 646 products, the 13/12/29/41/75/72/330 quality issues)
  4. data/reports/pe1-hero100-descriptions.csv (LOCKED voice for
     body_html — bold lede → Key features h3+ul → Who it's for h3+p →
     BBI close with 1-800-835-9565 CTA)
  5. data/reports/pe3-hero100-titles.csv (LOCKED title format —
     "<Brand> <Model> <Title>" sentence case, ≤60 chars, drop "| Brant
     Business Interiors" suffix if it pushes over)
  6. data/reports/pe7-longtail-seo.csv (LOCKED SEO meta format)
  7. data/specs/specs.json (already-researched specs with manufacturer
     URLs and confidence ratings — DO NOT re-research these in Pass 1;
     just read the confidence column per handle)
  8. data/reports/hero-100.csv (the 100 products already enriched via
     PE-1/2/3/7 — SKIP these in the triage)
  9. data/reports/longtail-products.csv (sanity-check the working set
     count matches)
  10. docs/strategy/icp.md
  11. docs/strategy/voice-samples.md

— HARD RULES (no exceptions, no overrides) —

HR1: every $0-price product → action = "archive". Always.
HR2: every unpublished/draft product → action = "leave-unpublished".
     Do NOT enrich, do NOT archive — these sit in admin as drafts
     indefinitely. Steve has explicitly waived enrichment work on them
     ("waste of work").
HR3: the 100 handles in hero-100.csv are SKIPPED — already shipped.
HR4: NO Shopify product mutations in Pass 1. Read-only on /products,
     /orders, /metafields. The only file you write is the triage CSV.
HR5: NO theme writes. This task does not touch theme files at all.

— SCOPE —

ALL Shopify products (any status), MINUS the 100 in hero-100.csv.
Expected working set: ~546.

— OUTPUT —

Single CSV: data/reports/product-triage-pass1-YYYY-MM-DD.csv
Sorted by category, then tier, then handle.

Columns (in this order):
  product_id, handle, title, status, price, vendor, product_type,
  type_tag, room_tag, category,
  units_sold_24mo, units_sold_12mo, orders_24mo, last_order_date,
  revenue_24mo,
  image_count, has_real_image,
  body_html_chars, has_desc,
  spec_count, specs_confidence,
  has_seo_title, has_seo_desc,
  cluster_id, is_cluster_best, cluster_size,
  tier_auto, archive_recommended, archive_reason,
  action_default, redirect_target_handle,
  steve_override_action, steve_notes

steve_override_action and steve_notes are BLANK columns Steve fills in
during review. Everything else is computed.

— TIER CLASSIFICATION —

Tier A — full enrichment (deep specs research in Pass 2):
  - Published AND (has sales in last 24 months OR strategic category
    chairs/desks/storage/tables)
  - Has body_html OR appears in specs.json with confidence=high
  - Action: keep

Tier B — light enrichment (template-grade drafts in Pass 2):
  - Published, zero sales, has body_html (any length), clear title
    with identifiable brand
  - Action: keep

Tier C — archive candidate (default skews aggressive — fight to keep):
  - Zero sales 24mo AND (no-desc OR no-real-image OR generic-title)
  - OR duplicate of another product (and is not the best in cluster)
  - OR specs.json confidence=none AND generic title
  - Action: archive (with redirect if has type/room tag)

Tier D — keep but minimal:
  - Ancillary products (chair mats, generic accessories) that need to
    exist for quoting but aren't worth polish. Has body_html but no
    brand and minimal sales.
  - Action: keep-minimal

If a product matches multiple tiers, the LOWEST tier wins (C beats B
beats A). But HR1/HR2/HR3 always override.

— FLAG DETECTION (these populate archive_reason) —

no-sales-24mo:   units_sold_24mo == 0
no-desc:         len(body_html.strip()) < 50
no-real-image:   image_count == 0 OR all images match placeholder
                 fingerprints (substrings: 'no-image', 'placeholder',
                 'default-product')
generic-title:   title matches /^[A-Za-z\s\-/&]+\s*(-\s*)?\d+["']?\s*x\s*
                 \d+["']?(\s*x\s*\d+["']?)?\s*$/ (dimensions-only)
                 OR title contains no known brand keyword AND no model
                 code (\b[A-Z]{2,}-?\d{2,}\b or \b\d{2,}-\d{2,}\b)
specs-unknown:   specs.json confidence == "none" OR not in specs.json
zero-price:      price == 0 (HARD: always archive)
duplicate:       fuzzy title match (SequenceMatcher >= 0.85) AND same
                 vendor

Known brand keywords (case-insensitive substring match):
  global, teknion, obusforme, ergocentric, otg, offices to go,
  keilhauer, kimball, mayline, fellowes, deflecto, sentry, heartwood,
  innovations, zira, newland, aeramax, schukra, hdl, toughlite,
  rollamat, roma, honor roll, links contract

archive_reason column = '; '.join of all flags that triggered.

— DUPLICATE DETECTION —

For each non-Hero product, compute a normalized fingerprint:
  - lowercase
  - strip non-alphanumeric
  - split into words, sort alphabetically, rejoin
Cluster using difflib.SequenceMatcher with threshold 0.85, scoped to
same vendor.

Within each cluster, pick the BEST product:
  1. Highest units_sold_24mo
  2. Tiebreak: most images
  3. Tiebreak: longest body_html
The best gets is_cluster_best = True, others = False.
Non-best cluster members: action = "archive-duplicate",
redirect_target_handle = best's handle.

— REDIRECT TARGET —

For each archive candidate (published only — unpublished have no public
URL to redirect):
  1. If duplicate AND not best: redirect to best's handle
  2. Else if has type_tag: redirect to "collections/all-<type>"
  3. Else if has room_tag: redirect to "collections/<room>"
  4. Else: redirect to "collections/all"

— STEP 1: Pull product catalog (read-only) —

export $(grep -v '^#' .env | xargs)

python3 - <<'EOF'
import os, json, time, urllib.request
STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']

products = []
url = (f'https://{STORE}/admin/api/2024-04/products.json'
       f'?limit=250&status=any&fields=id,handle,title,vendor,product_type,'
       f'tags,status,published_at,body_html,images,variants,'
       f'created_at,updated_at')

while url:
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        link = r.headers.get('Link', '')
    products += data.get('products', [])
    url = None
    for p in link.split(','):
        if 'rel="next"' in p:
            url = p.split(';')[0].strip().strip('<>'); break
    time.sleep(0.6)

os.makedirs('data/reports', exist_ok=True)
print(f'Pulled {len(products)} products.')
with open('data/reports/_products-raw.json', 'w') as f:
    json.dump(products, f)
EOF

— STEP 2: Pull 24-month sales data —

python3 - <<'EOF'
import os, json, time, urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']

now = datetime.now(timezone.utc)
cutoff_24 = (now - timedelta(days=730)).isoformat()
cutoff_12 = (now - timedelta(days=365)).isoformat()

sales = defaultdict(lambda: {'units_24mo': 0, 'units_12mo': 0,
                              'orders': 0, 'last_order_date': '',
                              'revenue_24mo': 0.0})

url = (f'https://{STORE}/admin/api/2024-04/orders.json'
       f'?status=any&created_at_min={cutoff_24}&limit=250'
       f'&fields=id,created_at,line_items,financial_status')

order_count = 0
while url:
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        link = r.headers.get('Link', '')
    for order in data.get('orders', []):
        if order.get('financial_status') in ('voided', 'refunded'):
            continue
        for li in order.get('line_items', []):
            pid = li.get('product_id')
            if not pid: continue
            qty = li.get('quantity', 0)
            price = float(li.get('price', 0))
            sales[pid]['units_24mo'] += qty
            sales[pid]['revenue_24mo'] += qty * price
            sales[pid]['orders'] += 1
            if order['created_at'] >= cutoff_12:
                sales[pid]['units_12mo'] += qty
            if not sales[pid]['last_order_date'] or \
               order['created_at'] > sales[pid]['last_order_date']:
                sales[pid]['last_order_date'] = order['created_at']
        order_count += 1
    url = None
    for p in link.split(','):
        if 'rel="next"' in p:
            url = p.split(';')[0].strip().strip('<>'); break
    time.sleep(0.6)

print(f'Processed {order_count} orders. Sales data for {len(sales)} products.')
with open('data/reports/_product-sales-24mo.json', 'w') as f:
    json.dump({str(k): v for k, v in sales.items()}, f)
EOF

— STEP 3: Pull SEO metafields (one bulk pass) —

python3 - <<'EOF'
import os, json, time, urllib.request
STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']

with open('data/reports/_products-raw.json') as f:
    products = json.load(f)

seo = {}
for i, p in enumerate(products):
    url = (f'https://{STORE}/admin/api/2024-04/products/{p["id"]}.json'
           f'?fields=id,metafields_global_title_tag,'
           f'metafields_global_description_tag')
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())['product']
        seo[str(p['id'])] = {
            'has_seo_title': bool(data.get('metafields_global_title_tag')),
            'has_seo_desc': bool(data.get('metafields_global_description_tag')),
        }
    except Exception as e:
        seo[str(p['id'])] = {'has_seo_title': False, 'has_seo_desc': False}
    if i % 50 == 0:
        print(f'SEO check {i}/{len(products)}')
    time.sleep(0.3)

with open('data/reports/_product-seo.json', 'w') as f:
    json.dump(seo, f)
print(f'SEO metadata pulled for {len(seo)} products.')
EOF

— STEP 4: Classify + write triage CSV —

python3 - <<'EOF'
import json, csv, re, os
from difflib import SequenceMatcher
from datetime import datetime
from collections import Counter

with open('data/reports/_products-raw.json') as f:
    products = json.load(f)
with open('data/reports/_product-sales-24mo.json') as f:
    sales = json.load(f)
with open('data/reports/_product-seo.json') as f:
    seo = json.load(f)
with open('data/specs/specs.json') as f:
    specs_data = json.load(f)

hero_handles = set()
with open('data/reports/hero-100.csv') as f:
    for row in csv.DictReader(f):
        hero_handles.add(row['handle'])

KNOWN_BRANDS = {
    'global', 'teknion', 'obusforme', 'ergocentric', 'otg',
    'offices to go', 'keilhauer', 'kimball', 'mayline', 'fellowes',
    'deflecto', 'sentry', 'heartwood', 'innovations', 'zira',
    'newland', 'aeramax', 'schukra', 'hdl', 'toughlite', 'rollamat',
    'roma', 'honor roll', 'links contract',
}
PLACEHOLDER_HINTS = ['no-image', 'placeholder', 'default-product']
GENERIC_DIMS_RE = re.compile(
    r'^[A-Za-z\s\-/&]+\s*(-\s*)?\d+["\']?\s*x\s*\d+["\']?'
    r'(\s*x\s*\d+["\']?)?\s*$', re.IGNORECASE)
MODEL_CODE_RE = re.compile(r'\b[A-Z]{2,}-?\d{2,}\b|\b\d{2,}-\d{2,}\b')

def normalize_title(t):
    t = t.lower()
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    return ' '.join(sorted(t.split()))

def is_generic_title(title):
    if GENERIC_DIMS_RE.match(title.strip()):
        return True
    if MODEL_CODE_RE.search(title):
        return False
    lower = title.lower()
    return not any(b in lower for b in KNOWN_BRANDS)

def get_tag(tags_str, prefix):
    if not tags_str: return ''
    for t in [x.strip() for x in tags_str.split(',')]:
        if t.startswith(prefix): return t
    return ''

def is_real_image(url):
    if not url: return False
    lower = url.lower()
    return not any(h in lower for h in PLACEHOLDER_HINTS)

working = [p for p in products if p['handle'] not in hero_handles]
print(f'Working set: {len(working)} (excluded {len(hero_handles)} Hero)')

# Cluster duplicates (within same vendor)
fingerprints = [(p['handle'], normalize_title(p['title']),
                  (p.get('vendor') or '').lower()) for p in working]
cluster_map = {}
clusters = {}
cid = 0
for i, (h1, f1, v1) in enumerate(fingerprints):
    if h1 in cluster_map: continue
    cid += 1
    clusters[cid] = [h1]
    cluster_map[h1] = cid
    for j in range(i + 1, len(fingerprints)):
        h2, f2, v2 = fingerprints[j]
        if h2 in cluster_map: continue
        if v1 != v2: continue
        if SequenceMatcher(None, f1, f2).ratio() >= 0.85:
            clusters[cid].append(h2)
            cluster_map[h2] = cid

dup_clusters = {c: hs for c, hs in clusters.items() if len(hs) > 1}
print(f'Duplicate clusters: {len(dup_clusters)} covering '
      f'{sum(len(hs) for hs in dup_clusters.values())} products')

# Pick best per cluster
product_by_handle = {p['handle']: p for p in working}
def score(p):
    s = sales.get(str(p['id']), {})
    return (s.get('units_24mo', 0), len(p.get('images', [])),
            len((p.get('body_html') or '')))

best_per_cluster = {}
for c, handles in dup_clusters.items():
    best = max(handles, key=lambda h: score(product_by_handle[h]))
    best_per_cluster[c] = best

# Build rows
rows = []
for p in working:
    pid = str(p['id'])
    s = sales.get(pid, {})
    seo_p = seo.get(pid, {})
    images = p.get('images', [])
    body = p.get('body_html', '') or ''
    title = p['title']
    handle = p['handle']
    is_pub = bool(p.get('published_at'))
    status = p.get('status', 'active') if is_pub else 'draft'

    variants = p.get('variants', [])
    price = float(variants[0]['price']) if variants else 0.0

    type_tag = get_tag(p.get('tags', ''), 'type:')
    room_tag = get_tag(p.get('tags', ''), 'room:')
    cat = type_tag.replace('type:', '') or 'uncategorized'

    cid_ = cluster_map.get(handle)
    csize = len(clusters.get(cid_, [handle]))
    is_best = (cid_ in best_per_cluster
               and best_per_cluster[cid_] == handle)

    spec_entry = specs_data.get(handle, {}).get('specs', {})
    spec_conf = spec_entry.get('confidence', 'none')
    spec_count = (len(spec_entry.get('key_features', []))
                  + (1 if spec_entry.get('dimensions') else 0)
                  + (1 if spec_entry.get('warranty') else 0))

    real_img = any(is_real_image(im.get('src')) for im in images)
    has_desc = len(body.strip()) >= 50
    generic = is_generic_title(title)
    units_24 = s.get('units_24mo', 0)

    flags = []
    if units_24 == 0: flags.append('no-sales-24mo')
    if not has_desc: flags.append('no-desc')
    if not real_img: flags.append('no-real-image')
    if generic: flags.append('generic-title')
    if spec_conf == 'none' and generic: flags.append('specs-unknown')
    if price == 0: flags.append('zero-price')
    if csize > 1 and not is_best: flags.append('duplicate')

    # Apply rules (HR1/HR2 override everything)
    if not is_pub:
        tier, action, archive = 'skip', 'leave-unpublished', 'no'
    elif price == 0:
        tier, action, archive = 'C', 'archive', 'yes'
    elif csize > 1 and not is_best:
        tier, action, archive = 'C', 'archive-duplicate', 'yes'
    elif units_24 == 0 and (not has_desc or not real_img or generic):
        tier, action, archive = 'C', 'archive', 'yes'
    elif units_24 > 0 or type_tag in (
            'type:chairs', 'type:desks', 'type:storage', 'type:tables'):
        tier, action, archive = 'A', 'keep', 'no'
    elif has_desc and not generic:
        tier, action, archive = 'B', 'keep', 'no'
    else:
        tier, action, archive = 'D', 'keep-minimal', 'no'

    redirect = ''
    if action.startswith('archive') and is_pub:
        if csize > 1 and cid_ in best_per_cluster:
            redirect = best_per_cluster[cid_]
        elif type_tag:
            redirect = f"collections/all-{type_tag.replace('type:', '')}"
        elif room_tag:
            redirect = f"collections/{room_tag.replace('room:', '')}"
        else:
            redirect = 'collections/all'

    rows.append({
        'product_id': p['id'], 'handle': handle, 'title': title,
        'status': status, 'price': price,
        'vendor': p.get('vendor', ''),
        'product_type': p.get('product_type', ''),
        'type_tag': type_tag, 'room_tag': room_tag, 'category': cat,
        'units_sold_24mo': units_24,
        'units_sold_12mo': s.get('units_12mo', 0),
        'orders_24mo': s.get('orders', 0),
        'last_order_date': s.get('last_order_date', ''),
        'revenue_24mo': round(s.get('revenue_24mo', 0), 2),
        'image_count': len(images), 'has_real_image': real_img,
        'body_html_chars': len(body), 'has_desc': has_desc,
        'spec_count': spec_count, 'specs_confidence': spec_conf,
        'has_seo_title': seo_p.get('has_seo_title', False),
        'has_seo_desc': seo_p.get('has_seo_desc', False),
        'cluster_id': cid_ or '', 'is_cluster_best': is_best,
        'cluster_size': csize,
        'tier_auto': tier, 'archive_recommended': archive,
        'archive_reason': '; '.join(flags),
        'action_default': action,
        'redirect_target_handle': redirect,
        'steve_override_action': '', 'steve_notes': '',
    })

rows.sort(key=lambda r: (r['category'], r['tier_auto'], r['handle']))

ts = datetime.now().strftime('%Y-%m-%d')
out = f'data/reports/product-triage-pass1-{ts}.csv'
cols = list(rows[0].keys())
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

print(f'\n=== TRIAGE SUMMARY ===')
print(f'Output: {out}')
print(f'Total: {len(rows)}')
print('\nBy tier:')
for t, n in Counter(r['tier_auto'] for r in rows).most_common():
    print(f'  {t}: {n}')
print('\nBy action:')
for a, n in Counter(r['action_default'] for r in rows).most_common():
    print(f'  {a}: {n}')
arc = sum(1 for r in rows if r['archive_recommended'] == 'yes')
print(f'\nArchive recommended: {arc}')
print(f'  Hard-rule $0: {sum(1 for r in rows if r["price"] == 0 and r["archive_recommended"] == "yes")}')
print(f'  Duplicates: {sum(1 for r in rows if "duplicate" in r["archive_reason"])}')
print(f'Leave-unpublished: {sum(1 for r in rows if r["action_default"] == "leave-unpublished")}')
print(f'Duplicate clusters: {len(dup_clusters)}')
EOF

— STEP 5: Sanity checks —

Verify before handoff (print each pass/fail):
  ✓ Total rows == working set size (646 minus Hero 100 = ~546)
  ✓ Every $0-priced row → action == "archive"
  ✓ Every unpublished row → action == "leave-unpublished"
  ✓ Exactly one row per cluster has is_cluster_best == True
  ✓ Non-best cluster members all have action == "archive-duplicate"
  ✓ Archive rows with is_pub=True have non-empty redirect_target_handle
  ✓ Keep rows have empty redirect_target_handle

If any sanity check fails: report which, stop, do not hand off.

— STEP 6: Handoff report —

Print to chat:
  1. CSV path
  2. Summary block from Step 4
  3. Top 5 BORDERLINE archive recommendations (Tier C rows that have
     any sales OR have a known brand keyword in title — flag these as
     "Steve should spot-check before approving")
  4. Top 5 duplicate clusters (cluster_id, count, all handles, which
     is best) so Steve can verify the "best" pick is right

Steve will:
  1. Open the CSV in Google Sheets
  2. Filter by tier / archive_recommended / category
  3. Fill in steve_override_action and steve_notes where he disagrees
  4. Save the reviewed CSV back to data/reports/
  5. Trigger Pass 2 with the reviewed file

Commit (one commit, audit only):
  "PE-Pass1: product triage CSV — 646 products audited, ~XXX flagged
   for archive"
```

---

## What Pass 2 will look like (preview, not running yet)

Once you've reviewed the Pass 1 CSV and approved the archive set, Pass 2 splits into:

- **Pass 2a — Deep specs research** for Tier A survivors not already in `specs.json`. Pulls brand source URLs, populates spec data, extends `specs.json`.
- **Pass 2b — Draft generation** for all survivors. Per-row drafts grounded in voice CSVs + specs.json. Output: drafts CSV grouped by category.
- **Pass 3 — Push.** Validates approved drafts, pushes to Shopify in batches of 25 with rollback per batch. Generates `data/url-redirects-bulk-archive.csv` for the archive set — you upload to Shopify Admin separately.

I'll write each Pass 2 prompt after you've reviewed the Pass 1 output, because the exact shape depends on what survives.
