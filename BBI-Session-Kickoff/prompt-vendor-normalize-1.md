# VENDOR-NORMALIZE-1 — Build canonical brand vocabulary

**Paste the safety preflight first** (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.

Step 1 of 35 on the BBI Launch Tracker. Hard prereq for PE Pass 3 batches 3/4/6 (Step 7) and for VENDOR-NORMALIZE-2 (Step 4).

This is a **thinking step**, not a code-deploy step. Two outputs:

- `docs/strategy/brand-canonical-map.md` — decision doc (the why)
- `docs/strategy/brand-canonical-map.csv` — machine-readable map (the input for downstream steps)

Read-only on Shopify. No theme writes. No product writes. Two hard halts where you decide before Claude finalizes.

---

## The prompt

```
You are running VENDOR-NORMALIZE-1 — building a canonical brand
vocabulary for BBI's Shopify catalog. Read-only on Shopify; the only
files you write are the two canonical-map outputs.

— READ THESE FIRST —

  1. CLAUDE.md (auto-loaded)
  2. BBI-Session-Kickoff/01-safety-preflight.md — run preflight
  3. BBI-Session-Kickoff/bbi-build-state.md — pay specific attention
     to the new "Known Data Hygiene Issues" section
  4. data/reports/audit-tech-debt-2026-05-12.md (DEBT-01 / 02 context)
  5. data/reports/pe1-hero100-descriptions.csv (LOCKED voice — for
     understanding how brands are referenced in BBI's writing)
  6. docs/strategy/icp.md
  7. data/specs/specs.json (already-researched specs for Hero 100;
     read the "manufacturer" + "brand" fields and confidence ratings)

Confirm reads in chat before running any code.

— HARD RULES —

  - READ-ONLY on Shopify. No PUT, no POST, no metafield writes,
    no tag changes. The only files you write are
    docs/strategy/brand-canonical-map.md and brand-canonical-map.csv.
  - SCOPE IS TIGHT: build the map from the 152 enriched products
    that already have specs.manufacturer metafield populated. The
    remaining 441 unenriched products are OUT OF SCOPE — they'll
    be classified during PE Pass 3 batches 3/4/6 using the map as
    a vocabulary reference. Do NOT try to fuzzy-guess brands from
    titles for the 441; that's wasted effort that duplicates PE
    Pass 3 work.
  - Two HARD HALTS. After each, print findings and wait for
    Steve's "proceed". Do not bulldoze through.

═══════════════════════════════════════════════════════════════════════
PHASE 1 — Pull and roll up the raw data
═══════════════════════════════════════════════════════════════════════

Pull every product with a specs.manufacturer metafield populated.
Expected count: ~152. Group by raw metafield string. Tally counts.

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, time, urllib.request
  from collections import Counter, defaultdict

  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']
  hdr = {'X-Shopify-Access-Token': TOKEN}

  # Pull all active products
  products = []
  url = (f'https://{STORE}/admin/api/2024-04/products.json'
         f'?limit=250&status=active&fields=id,handle,title,vendor,tags')
  while url:
      req = urllib.request.Request(url, headers=hdr)
      with urllib.request.urlopen(req) as r:
          data = json.loads(r.read())
          link = r.headers.get('Link', '')
      products += data.get('products', [])
      url = None
      for p in link.split(','):
          if 'rel="next"' in p:
              url = p.split(';')[0].strip().strip('<>')
              break
      time.sleep(0.5)
  print(f'Pulled {len(products)} active products.')

  # Pull specs.manufacturer metafield for each
  enriched = []
  for i, p in enumerate(products):
      pid = p['id']
      url = (f'https://{STORE}/admin/api/2024-04/products/{pid}'
             f'/metafields.json?namespace=specs&key=manufacturer')
      req = urllib.request.Request(url, headers=hdr)
      try:
          with urllib.request.urlopen(req) as r:
              mfs = json.loads(r.read()).get('metafields', [])
          if mfs:
              enriched.append({
                  'product_id': pid,
                  'handle': p['handle'],
                  'title': p['title'],
                  'shopify_vendor': p.get('vendor', ''),
                  'tags': p.get('tags', ''),
                  'manufacturer_raw': mfs[0]['value'],
              })
      except Exception as e:
          pass  # No metafield is expected for most
      if i % 50 == 0:
          print(f'Checked {i}/{len(products)} for specs.manufacturer')
      time.sleep(0.3)

  print(f'\nProducts with specs.manufacturer: {len(enriched)}')

  os.makedirs('data/reports', exist_ok=True)
  with open('data/reports/_vendor-normalize-raw.json', 'w') as f:
      json.dump(enriched, f, indent=2)

  # Count raw string variants
  variants = Counter(p['manufacturer_raw'] for p in enriched)
  print(f'\nRaw specs.manufacturer string variants: {len(variants)}')
  print('\nTop 30 variants by frequency:')
  for s, n in variants.most_common(30):
      print(f'  {n:4d}  {s}')

  # Also tally Shopify vendor field for cross-reference
  shopify_vendors = Counter(p['shopify_vendor'] for p in enriched)
  print(f'\nShopify vendor field on enriched products:')
  for v, n in shopify_vendors.most_common():
      print(f'  {n:4d}  {v}')

  # Also tally brand:* tags for cross-reference
  brand_tags = Counter()
  for p in enriched:
      for t in (p['tags'] or '').split(','):
          t = t.strip()
          if t.startswith('brand:'):
              brand_tags[t] += 1
  print(f'\nbrand:* tags on enriched products:')
  for t, n in brand_tags.most_common():
      print(f'  {n:4d}  {t}')
  PYEOF

>>> HALT 1 — Raw distribution surfaced

Report:
  - Total enriched products found
  - Number of raw specs.manufacturer string variants
  - Top 30 variants by frequency
  - Shopify vendor field distribution on enriched products
  - brand:* tag distribution on enriched products
  - Your initial read on which strings clearly belong to the same
    canonical brand family (e.g., "all six of these are Global
    Furniture Group divisions: ..."). Group them as you see them,
    but do NOT decide standalone-vs-fold yet — that's Phase 2.

Wait for Steve's "proceed" before Phase 2.

═══════════════════════════════════════════════════════════════════════
PHASE 2 — Propose canonical names + standalone-vs-fold decisions
═══════════════════════════════════════════════════════════════════════

For each brand family identified in Phase 1, propose:

  1. canonical_brand: the single canonical name to use across
     specs.manufacturer, Shopify vendor field, and brand:* tags
     (e.g., "Global Furniture Group", "Heartwood Manufacturing")

  2. parent_brand: blank if this IS the parent; otherwise the
     canonical name of the parent family

  3. is_standalone_brand: True if this brand should have its own
     callable storefront identity (own brand page, own brand
     collection, own brand:* tag value) — False if it should fold
     into the parent's storefront identity. Sub-brands that are
     recognizable to buyers in their own right (e.g., OTG / Offices
     to Go in office furniture) typically stand alone even if a
     parent company owns them. Sub-brands that are internal
     divisions (e.g., "Global Upholstery Co." as just a corporate
     entity behind multiple products) typically fold.

  4. storefront_callable: True if this brand should appear in
     category-page brand callouts. Default True for standalone
     brands with ≥10 products in the enriched set; False otherwise
     (per the COLLECTION-CLEANUP-1 brand callout audit threshold
     in the launch tracker).

  5. reasoning: 1-2 sentence justification per decision.

Build a proposal table covering every brand family from Phase 1.
For Global Furniture Group specifically, list every division as a
separate proposal row (Global, OTG / Offices to Go, Newland,
Fileworks, Basics, Global Upholstery Co., etc.) with your
recommended is_standalone_brand value per division.

Also flag any string variants that are AMBIGUOUS — cases where
you can't tell from the string alone which canonical brand applies
(e.g., a one-off "Office Source" — is that a brand or just a
descriptor?). Surface these for Steve to resolve.

>>> HALT 2 — Proposed canonical map ready for review

Report:
  - The full proposal table, brand-by-brand
  - Ambiguous-string list for Steve to resolve
  - Summary stats:
    * X canonical brands proposed total
    * Y standalone brands (would have storefront callouts)
    * Z folded sub-brands
  - Specifically flag your recommendation for the Global Furniture
    Group division question (which divisions standalone vs. fold)

Wait for Steve's "proceed" or "revise — [specific overrides]".
Steve may say things like "OTG stands alone, fold the rest", or
"standalone all six", or "fold all except OTG". Apply his overrides
before Phase 3.

═══════════════════════════════════════════════════════════════════════
PHASE 3 — Write the canonical map outputs
═══════════════════════════════════════════════════════════════════════

After Steve's overrides are applied, finalize the two output files.

OUTPUT 1 — docs/strategy/brand-canonical-map.md

Structure:

  # BBI Brand Canonical Map
  _Generated by VENDOR-NORMALIZE-1 · 2026-05-XX · Read-only input
  for VENDOR-NORMALIZE-2 + PE Pass 3 batch prompts._

  ## Purpose
  [2-3 sentences: why this exists, what downstream steps consume it]

  ## Data sources audited
  - X enriched products with specs.manufacturer metafield
  - Y raw string variants identified
  - Z canonical brands resolved

  ## Canonical brands
  For each canonical brand (sorted by product count, descending):

    ### {Canonical Brand Name}
    - **Product count:** N
    - **Standalone storefront brand:** Yes / No (folded into {parent})
    - **Storefront callable:** Yes / No
    - **Mapped from variants:**
      - "Variant string 1" (N products)
      - "Variant string 2" (N products)
    - **Reasoning:** [1-2 sentences from Phase 2 proposal,
      reflecting any Steve overrides]

  ## Sub-brand decisions
  [For families with multiple sub-brands — e.g., Global Furniture
  Group — capture the parent and the standalone/fold call per
  division in a single subsection.]

  ## Ambiguous strings resolved by Steve
  [List each ambiguous variant from Phase 2 with the resolution
  Steve chose.]

  ## Downstream consumers
  - VENDOR-NORMALIZE-2 (Step 4): applies this map to the 152
    already-enriched products
  - PE Pass 3 batches 3 / 4 / 6 (Step 7): batch prompts use this
    map to populate vendor_override per product
  - COLLECTION-CLEANUP-1 (Step 9): uses storefront_callable flag
    to decide which brand callouts survive on category pages

OUTPUT 2 — docs/strategy/brand-canonical-map.csv

Columns (in this order):

  string_variant, canonical_brand, parent_brand,
  is_standalone_brand, storefront_callable, product_count, notes

One row per raw string variant found in Phase 1, plus one
"canonical-name-itself" row per canonical brand (where
string_variant == canonical_brand) for downstream tools that look
up the canonical name directly. Sort by canonical_brand ASC then
product_count DESC.

Commit:
  git add docs/strategy/brand-canonical-map.md
  git add docs/strategy/brand-canonical-map.csv
  git commit -m "VENDOR-NORMALIZE-1: canonical brand map — N brands,
   M variants resolved from K enriched products"

>>> HALT 3 — Final handoff

Report:
  - Both file paths
  - Final canonical brand count + standalone count + callable count
  - Top 5 canonical brands by product count
  - Commit hash
  - Steve's next move: paste VENDOR-NORMALIZE-2 prompt (Step 4) to
    apply this map to the 152 enriched products, OR paste
    TAG-AUDIT-1 (Step 5) in parallel — both safe to run before
    PE Pass 3 batch prompt edits land.
```
