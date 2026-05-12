# Prompt 4 — Pass 2: Move-to-Other + Generate Enrichment CSV

**Paste the safety preflight first** (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.

**Critical:** this is a multi-phase script with **HARD HALTS** between phases. After each phase, Claude Code stops, reports to Steve, and waits for explicit "proceed" before continuing. Do not bulldoze through phases.

**Prerequisite:** Steve has reviewed `data/reports/product-triage-pass1-2026-05-11.csv` and filled in `steve_override_action` per row (either `move-to-other` or `keep`, or any other valid action).

---

## The prompt

```
You are working on the BBI Shopify store (dev theme 186373570873 for theme
changes; product changes are store-wide).

PASS 2 of the product enrichment workflow. This pass:
  1. Patches the PDP template for single-tier related products + Other-aware breadcrumb
  2. Creates a new "Other" custom collection (junk drawer, no nav link)
  3. Canary tests the PDP on ONE product before bulk operation
  4. Bulk-moves Steve-flagged archive products to Other + strips their tags
  5. Generates an enrichment CSV for kept products with pre-filled drafts

HARD HALTS between every phase. Report findings, wait for Steve's "proceed".

— READ THESE FIRST —

  1. CLAUDE.md (auto-loaded)
  2. BBI-Session-Kickoff/01-safety-preflight.md (preflight)
  3. BBI-Session-Kickoff/bbi-build-state.md
  4. data/reports/product-triage-pass1-2026-05-11.csv (Steve's reviewed
     triage with steve_override_action filled in)
  5. data/reports/pe1-hero100-descriptions.csv (LOCKED voice)
  6. data/reports/pe3-hero100-titles.csv (LOCKED title format)
  7. data/reports/pe7-longtail-seo.csv (LOCKED SEO meta format)
  8. data/specs/specs.json (already-researched spec data, confidence ratings)
  9. docs/strategy/icp.md
  10. docs/strategy/voice-samples.md
  11. theme/sections/ds-pdp-base.liquid (current PDP source)
  12. theme/snippets/bbi-breadcrumb-jsonld.liquid (breadcrumb JSON-LD)

Confirm reads in chat before running any code.

═══════════════════════════════════════════════════════════════════════
PHASE 0 — PDP template patches
═══════════════════════════════════════════════════════════════════════

Patch theme/sections/ds-pdp-base.liquid to handle tag-less products
gracefully. Two changes:

PATCH A — Simplify related products to single-tier (was 3-tier from PROMPT-3):

  Replace the existing 3-tier fallback block with:
    - Only Tier 1 logic: query collections['all-' + type_tag.removed].products
    - Exclude current product
    - Show top 4 (collection already sorted best-selling)
    - Heading: "Best sellers in {Category capitalized}"
    - Hide section ENTIRELY if no type_tag OR if filtered count == 0

  Preserve the capture pattern that worked around where_exp outer-scope limit.
  Remove Tier 2 (room) and Tier 3 (all-business-furniture) code entirely.

PATCH B — Breadcrumb falls back to "Other" when type_tag is blank:

  In ds-pdp-base.liquid breadcrumb HTML:
    {%- if type_tag != blank -%}
      <a href="/collections/{{ cat_handle }}">{{ cat_title }}</a>
    {%- else -%}
      <a href="/collections/other">Other</a>
    {%- endif -%}

  In theme/snippets/bbi-breadcrumb-jsonld.liquid:
    Same fallback logic — when product has no type tag, the breadcrumb
    schema's category item points to /collections/other with name "Other".

Push both files via direct API:

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, urllib.request
  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']
  THEME = '186373570873'
  for key, path in [
      ('sections/ds-pdp-base.liquid', 'theme/sections/ds-pdp-base.liquid'),
      ('snippets/bbi-breadcrumb-jsonld.liquid', 'theme/snippets/bbi-breadcrumb-jsonld.liquid'),
  ]:
      with open(path, 'rb') as f:
          content = f.read().decode('utf-8')
      body = json.dumps({'asset': {'key': key, 'value': content}}).encode()
      req = urllib.request.Request(
          f'https://{STORE}/admin/api/2024-04/themes/{THEME}/assets.json',
          data=body, method='PUT',
          headers={'X-Shopify-Access-Token': TOKEN,
                   'Content-Type': 'application/json'})
      with urllib.request.urlopen(req) as r:
          print(f'  {key}: HTTP {r.status}')
  PYEOF

>>> HALT — Report PHASE 0:
    - Both files pushed (HTTP 200)
    - Brief diff summary: lines changed in each file
    - Smoke test URL: pick any normal PDP and confirm related products
      section still works for a product WITH type tag (e.g. an in-stock
      seating product). Heading should read "Best sellers in Seating".

Wait for Steve's "proceed" before Phase 1.

═══════════════════════════════════════════════════════════════════════
PHASE 1 — Create "Other" custom collection
═══════════════════════════════════════════════════════════════════════

Create a single Shopify custom collection. No products yet, no
sub-collections, no nav membership.

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, urllib.request
  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']

  # First check if 'other' already exists
  req = urllib.request.Request(
      f'https://{STORE}/admin/api/2024-04/custom_collections.json?handle=other',
      headers={'X-Shopify-Access-Token': TOKEN})
  existing = json.loads(urllib.request.urlopen(req).read()).get('custom_collections', [])
  if existing:
      print(f'Already exists: id={existing[0]["id"]} handle={existing[0]["handle"]}')
      with open('data/reports/_other-collection.json', 'w') as f:
          json.dump(existing[0], f, indent=2)
  else:
      body = json.dumps({'custom_collection': {
          'title': 'Other',
          'handle': 'other',
          'published': True,
          'sort_order': 'manual',
          'body_html': '<p>Specialty, legacy, and limited-availability items. Contact us for current availability or a quote.</p>',
      }}).encode()
      req = urllib.request.Request(
          f'https://{STORE}/admin/api/2024-04/custom_collections.json',
          data=body, method='POST',
          headers={'X-Shopify-Access-Token': TOKEN,
                   'Content-Type': 'application/json'})
      with urllib.request.urlopen(req) as r:
          created = json.loads(r.read())['custom_collection']
      print(f'Created: id={created["id"]} handle={created["handle"]}')
      with open('data/reports/_other-collection.json', 'w') as f:
          json.dump(created, f, indent=2)
  PYEOF

>>> HALT — Report PHASE 1:
    - Collection ID
    - Handle: "other"
    - URL: https://office-central-online.myshopify.com/collections/other?preview_theme_id=186373570873
    - Confirm URL returns 200 (currently empty — that's expected)

Wait for Steve's "proceed" before Phase 2.

═══════════════════════════════════════════════════════════════════════
PHASE 2 — Canary PDP test on ONE product
═══════════════════════════════════════════════════════════════════════

Pick one test product. Default: teknion-boardroom (a $0 Teknion showcase
flagged for archive in Pass 1). Steve can override with any other
move-to-other-flagged product before proceeding.

Steps:
  1. Backup current state of test product (tags, collection memberships)
  2. Fetch baseline PDP HTML before any change
  3. Strip type:* and room:* tags via API
  4. Add to "Other" collection via API
  5. Wait 5 seconds for Shopify to propagate
  6. Re-fetch PDP HTML
  7. Diff baseline vs. after — report what changed

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, time, urllib.request, urllib.error
  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']
  THEME = '186373570873'
  TEST_HANDLE = 'teknion-boardroom'

  hdr = {'X-Shopify-Access-Token': TOKEN}

  # Get product
  req = urllib.request.Request(
      f'https://{STORE}/admin/api/2024-04/products.json?handle={TEST_HANDLE}',
      headers=hdr)
  prod = json.loads(urllib.request.urlopen(req).read())['products'][0]
  pid = prod['id']
  print(f'Test product: {prod["title"]} (id={pid})')
  print(f'  Current tags: {prod["tags"]}')

  # Backup
  os.makedirs('data/backups', exist_ok=True)
  ts = time.strftime('%Y%m%d_%H%M%S')
  with open(f'data/backups/canary-product-{TEST_HANDLE}-{ts}.json', 'w') as f:
      json.dump(prod, f, indent=2)
  print(f'  Backup: data/backups/canary-product-{TEST_HANDLE}-{ts}.json')

  # Baseline PDP fetch (preview cookie required for dev theme HTML)
  # NOTE: dev preview requires Shopify admin session; use source-level
  # checks instead by fetching the rendered theme via Section Rendering
  # API or comparing live HTML against expected fragments.
  baseline_url = f'https://office-central-online.myshopify.com/products/{TEST_HANDLE}?preview_theme_id={THEME}'
  try:
      r = urllib.request.urlopen(
          urllib.request.Request(baseline_url, headers={'User-Agent': 'Mozilla/5.0'}))
      baseline_html = r.read().decode('utf-8', errors='replace')
      print(f'  Baseline HTTP {r.status}, {len(baseline_html)} bytes')
  except urllib.error.HTTPError as e:
      print(f'  Baseline fetch error: HTTP {e.code} — note dev preview may require auth')
      baseline_html = ''

  with open(f'data/backups/canary-pdp-baseline-{ts}.html', 'w') as f:
      f.write(baseline_html)

  # Strip type:* and room:* tags
  new_tags = ','.join(
      t.strip() for t in prod['tags'].split(',')
      if not t.strip().startswith('type:')
      and not t.strip().startswith('room:')
  )
  print(f'  New tags: {new_tags}')

  body = json.dumps({'product': {'id': pid, 'tags': new_tags}}).encode()
  req = urllib.request.Request(
      f'https://{STORE}/admin/api/2024-04/products/{pid}.json',
      data=body, method='PUT',
      headers={**hdr, 'Content-Type': 'application/json'})
  urllib.request.urlopen(req)
  print(f'  Tags updated')

  # Add to Other collection
  with open('data/reports/_other-collection.json') as f:
      other_cid = json.load(f)['id']
  body = json.dumps({'collect': {
      'product_id': pid, 'collection_id': other_cid}}).encode()
  req = urllib.request.Request(
      f'https://{STORE}/admin/api/2024-04/collects.json',
      data=body, method='POST',
      headers={**hdr, 'Content-Type': 'application/json'})
  try:
      urllib.request.urlopen(req)
      print(f'  Added to Other collection (id={other_cid})')
  except urllib.error.HTTPError as e:
      err = e.read().decode()
      if 'already' in err.lower():
          print(f'  Already in Other collection')
      else:
          print(f'  Add failed: {err[:200]}')

  print('  Waiting 5s for Shopify to propagate...')
  time.sleep(5)

  # Re-fetch PDP after change
  try:
      r = urllib.request.urlopen(
          urllib.request.Request(baseline_url, headers={'User-Agent': 'Mozilla/5.0'}))
      after_html = r.read().decode('utf-8', errors='replace')
      print(f'  After HTTP {r.status}, {len(after_html)} bytes')
  except urllib.error.HTTPError as e:
      print(f'  After fetch error: HTTP {e.code}')
      after_html = ''

  with open(f'data/backups/canary-pdp-after-{ts}.html', 'w') as f:
      f.write(after_html)

  # Diff summary
  print('\n=== DIFF SUMMARY ===')
  print(f'  Baseline length: {len(baseline_html)}')
  print(f'  After length:    {len(after_html)}')
  print(f'  Both contain product title: {prod["title"] in baseline_html} / {prod["title"] in after_html}')
  print(f'  Baseline mentions Boardroom (category): "Boardroom" in baseline = {"Boardroom" in baseline_html}')
  print(f'  After  mentions "Other" (new category): "Other" in after = ">Other<" in after_html')
  print(f'  Baseline has .pdp-related section: {"pdp-related" in baseline_html}')
  print(f'  After  has .pdp-related section:    {"pdp-related" in after_html}')
  print(f'  Baseline JSON-LD count: {baseline_html.count("application/ld+json")}')
  print(f'  After  JSON-LD count:   {after_html.count("application/ld+json")}')

  # Write a structured findings file
  findings = {
      'test_product': TEST_HANDLE,
      'product_id': pid,
      'backup_path': f'data/backups/canary-product-{TEST_HANDLE}-{ts}.json',
      'baseline_html_path': f'data/backups/canary-pdp-baseline-{ts}.html',
      'after_html_path': f'data/backups/canary-pdp-after-{ts}.html',
      'baseline_bytes': len(baseline_html),
      'after_bytes': len(after_html),
      'title_renders_baseline': prod['title'] in baseline_html,
      'title_renders_after': prod['title'] in after_html,
      'related_section_baseline': 'pdp-related' in baseline_html,
      'related_section_after': 'pdp-related' in after_html,
      'jsonld_count_baseline': baseline_html.count('application/ld+json'),
      'jsonld_count_after': after_html.count('application/ld+json'),
      'other_in_after_breadcrumb': '>Other<' in after_html or 'collections/other' in after_html,
  }
  with open(f'data/reports/canary-findings-{ts}.json', 'w') as f:
      json.dump(findings, f, indent=2)
  print(f'\nFindings written to data/reports/canary-findings-{ts}.json')
  PYEOF

>>> HALT — Report PHASE 2:
    - Test product used
    - Backup paths
    - Diff summary table
    - Validate the PDP at:
        https://office-central-online.myshopify.com/products/teknion-boardroom?preview_theme_id=186373570873
      (Steve will open in browser — note dev preview may require admin auth)
    - Recommendation: PASS (proceed to bulk) / FAIL (rollback canary, patch
      template, retry)

If Steve says ROLLBACK: restore from backup file (re-apply original tags,
remove from Other), then halt for further diagnosis.

If Steve says PROCEED: continue to Phase 3.

═══════════════════════════════════════════════════════════════════════
PHASE 3 — Bulk move archive-flagged products to Other + strip tags
═══════════════════════════════════════════════════════════════════════

Read the reviewed Pass 1 CSV. For every row where
steve_override_action (or action_default if no override) is one of:
  archive · archive-duplicate · move-to-other
…apply the same treatment as the canary: strip type:* and room:* tags,
add to Other collection. Status stays active.

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, csv, time, urllib.request, urllib.error
  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']

  with open('data/reports/_other-collection.json') as f:
      other_cid = json.load(f)['id']

  with open('data/reports/product-triage-pass1-2026-05-11.csv') as f:
      rows = list(csv.DictReader(f))

  MOVE_ACTIONS = {'archive', 'archive-duplicate', 'move-to-other'}
  targets = []
  for r in rows:
      action = (r.get('steve_override_action') or r.get('action_default', '')).strip()
      if action in MOVE_ACTIONS:
          targets.append(r)
  print(f'Will move {len(targets)} products to Other.')

  # Backup current state for all targets (in one file)
  ts = time.strftime('%Y%m%d_%H%M%S')
  os.makedirs('data/backups', exist_ok=True)
  backup_path = f'data/backups/pre-move-state-{ts}.json'
  backup_data = []
  hdr = {'X-Shopify-Access-Token': TOKEN}

  print('Pulling current state for backup...')
  for i, t in enumerate(targets):
      pid = t['product_id']
      req = urllib.request.Request(
          f'https://{STORE}/admin/api/2024-04/products/{pid}.json?fields=id,handle,tags,status',
          headers=hdr)
      try:
          d = json.loads(urllib.request.urlopen(req).read())['product']
          backup_data.append(d)
      except Exception as e:
          backup_data.append({'id': pid, 'error': str(e)})
      time.sleep(0.5)
      if i % 25 == 0:
          print(f'  Backed up {i}/{len(targets)}')

  with open(backup_path, 'w') as f:
      json.dump(backup_data, f, indent=2)
  print(f'Backup: {backup_path}')

  # Dry-run first
  CONFIRM = False  # ← set True after reviewing dry-run

  if not CONFIRM:
      print('\nDRY RUN — first 10 targets:')
      for t in targets[:10]:
          print(f'  {t["handle"]} (id={t["product_id"]}, tier={t["tier_auto"]}, '
                f'flags=[{t["archive_reason"]}])')
      print(f'\nTotal to move: {len(targets)}')
      print(f'Set CONFIRM = True and re-run to execute.')
  else:
      print('\nExecuting bulk move...')
      ok, fail = 0, []
      for i, t in enumerate(targets):
          pid = t['product_id']
          # Get current tags
          req = urllib.request.Request(
              f'https://{STORE}/admin/api/2024-04/products/{pid}.json?fields=id,tags',
              headers=hdr)
          try:
              d = json.loads(urllib.request.urlopen(req).read())['product']
          except Exception as e:
              fail.append({'handle': t['handle'], 'error': f'fetch: {e}'})
              continue
          # Strip tags
          new_tags = ','.join(
              tag.strip() for tag in (d['tags'] or '').split(',')
              if not tag.strip().startswith('type:')
              and not tag.strip().startswith('room:')
          )
          # PUT
          body = json.dumps({'product': {'id': pid, 'tags': new_tags}}).encode()
          req = urllib.request.Request(
              f'https://{STORE}/admin/api/2024-04/products/{pid}.json',
              data=body, method='PUT',
              headers={**hdr, 'Content-Type': 'application/json'})
          try:
              urllib.request.urlopen(req)
          except urllib.error.HTTPError as e:
              fail.append({'handle': t['handle'], 'error': f'tag-update: {e.code}'})
              time.sleep(0.6)
              continue
          # Add to Other
          body = json.dumps({'collect': {
              'product_id': pid, 'collection_id': other_cid}}).encode()
          req = urllib.request.Request(
              f'https://{STORE}/admin/api/2024-04/collects.json',
              data=body, method='POST',
              headers={**hdr, 'Content-Type': 'application/json'})
          try:
              urllib.request.urlopen(req)
          except urllib.error.HTTPError as e:
              err = e.read().decode()
              if 'already' not in err.lower():
                  fail.append({'handle': t['handle'], 'error': f'collect: {e.code}'})
          ok += 1
          time.sleep(0.6)
          if i % 25 == 0:
              print(f'  Moved {i}/{len(targets)}')

      print(f'\n=== BULK MOVE COMPLETE ===')
      print(f'  Success: {ok}/{len(targets)}')
      print(f'  Failed:  {len(fail)}')
      if fail:
          with open(f'data/reports/move-failures-{ts}.json', 'w') as f:
              json.dump(fail, f, indent=2)
          print(f'  Failures saved to data/reports/move-failures-{ts}.json')
  PYEOF

>>> HALT — Report PHASE 3:
    - Total moved (success / fail)
    - Failure log if any
    - Backup path
    - Sample verification: pick 5 random moved products, confirm
      - They appear in /collections/other
      - They do NOT appear in /collections/all-<their-old-type>
      - Their PDP renders without errors

Wait for Steve's "proceed" before Phase 4.

═══════════════════════════════════════════════════════════════════════
PHASE 4 — Generate enrichment CSV for kept products
═══════════════════════════════════════════════════════════════════════

Read the reviewed Pass 1 CSV. Filter to rows where action is "keep" (not
moved). For each: pre-fill draft title, body_html, SEO meta, and spec
metafields per the locked PE-1 voice. Output a single CSV that Steve
edits in Sheets.

TIERED RESEARCH per Steve's earlier decision:
  - Tier A: deep specs research via brand source URLs (Global, Teknion,
    ObusForme, ergoCentric, OTG, Keilhauer, Kimball, Mayline, etc.)
    Read the brand page, populate spec data, then generate draft.
  - Tier B: only research if brand is in known list; else template draft.
  - Tier D: minimal template draft.

DRAFTS MATCH THE PE-1 SHIPPED FORMAT EXACTLY (do NOT use the brief's
expanded effydesk structure):
  - Bold lede sentence (1 line)
  - Context paragraph (3-5 sentences, conversational, B2B voice)
  - <h3>Key features</h3> + <ul> 5-9 bullets, each one factual + sourced
  - <h3>Who it's for</h3> + paragraph naming target buyer roles +
    institutional verticals (municipal, school board, family health
    team, professional services)
  - BBI close paragraph with "Call 1-800-835-9565" CTA
  - OECM signal when product fits institutional procurement
  - "Canadian-made" signal when brand origin confirmed
  - NEVER fabricate dimensions, model codes, warranty terms, or
    certifications. If not in source, note "no model code in source" in
    the notes column rather than invent.

Title format (LOCKED from pe3-hero100-titles.csv):
  "<Brand> <Model-Code> <Product Title>", sentence case, ≤60 chars.
  Drop "| Brant Business Interiors" suffix if it pushes over 60.

SEO title: 50-60 chars, keyword-first.
SEO desc:  140-155 chars, includes spec + use case.

CSV columns (in this order):

  product_id, handle, tier, vendor, current_type_tag, current_room_tag,
  current_title, current_body_html_first_300,
  draft_title, draft_title_chars, draft_body_html, draft_body_word_count,
  draft_seo_title, draft_seo_title_chars,
  draft_seo_desc, draft_seo_desc_chars,
  draft_spec_dimensions, draft_spec_weight, draft_spec_weight_capacity,
  draft_spec_material, draft_spec_finishes, draft_spec_warranty,
  draft_spec_certifications, draft_spec_assembly,
  draft_spec_country_of_manufacture, draft_spec_model_codes,
  draft_spec_source_urls,
  draft_confidence, draft_notes,
  image_action, steve_approval, steve_final_overrides

How Steve uses it:
  - Open in Google Sheets
  - Each draft_* cell pre-filled with Claude's suggestion
  - Steve EDITS IN PLACE where corrections are needed (no separate
    "final" column to copy into — the draft column is the working copy)
  - image_action: blank by default; Steve fills "add-real-photo" if needed
  - steve_approval: required per row — one of "approve" / "revise" / "skip"
  - steve_final_overrides: free-text notes for any rows needing follow-up
  - Save back to data/reports/, name pattern:
      pe-kept-enrichment-reviewed-YYYY-MM-DD.csv

Output path: data/reports/pe-kept-enrichment-2026-05-11.csv
Sorted by category (current_type_tag), then by tier.

>>> HALT — Report PHASE 4:
    - CSV path + total rows
    - Tier breakdown (A / B / D counts)
    - draft_confidence distribution (high / medium / low / none)
    - Top 5 rows with draft_confidence = "none" — these need Steve's
      attention or are candidates to move-to-Other after all
    - Top 5 rows where Tier A deep research couldn't find source URLs
      (research_failed flag)
    - Summary: estimated Steve editing time (~5 min/row for Tier A,
      ~2 min for Tier B, ~30 sec for Tier D)
    - Next step: Steve reviews in Sheets, fills steve_approval per row,
      saves back. Then triggers Pass 3 (push to Shopify).

Commit:
  "PE-Pass2: PDP single-tier related, Other collection, X products
   moved, Y kept with drafts generated"
```

---

## Notes for Steve

**What happens between phases.** Each `>>> HALT` is a hard stop. Claude Code prints findings and waits for your "proceed". If anything looks off — wrong test product, unexpected diff in canary, too many move-to-Other rows, low draft confidence — you can stop, correct, and re-run from that phase. No phase ships unless you explicitly say go.

**Why Phase 0 first.** If we move products to Other without first patching the PDP template, breadcrumbs may render with empty category segments and JSON-LD may break. Phase 0 patches the template, Phase 2 verifies the patch worked on one product, only then does Phase 3 hit the other 382.

**What the enrichment CSV gives you.** Each cell is pre-filled with Claude's best draft, sourced from PE-1 voice, specs.json data where available, and brand source URLs for Tier A products. Your job is final-pass editor: scan, correct, mark approve. You're not writing from scratch.

**Pass 3 (the actual push) is separate.** Once you've reviewed and approved rows in the enrichment CSV, I'll write a Pass 3 prompt that validates the schema, pushes in batches of 25 with rollback, logs every change. Pass 3 is mechanical — your editing work is the last creative step.

**Sales-window note.** The triage CSV from Pass 1 was 24-month sales. The kept set in Phase 4 inherits those classifications. Any A/B/C/D you've overridden in the triage CSV carries through.
