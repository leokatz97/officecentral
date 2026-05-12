# BBI: Tracker Cleanup + PE Pass 2 Execution (Combined)

**Paste this in a fresh Cowork session.** This is a self-contained briefing — the new session has no context from the prior conversation. Everything it needs is in this prompt.

This prompt does TWO things in one session:

1. **Restructures the BBI Launch Tracker artifact** — splits the sprawling PROMPT-4 row into discrete tracked tasks
2. **Executes PE Pass 2 work** — patches the PDP, creates the "Other" custom collection, runs a canary test, bulk-moves ~336 archive-recommended products to Other, generates an enrichment CSV for kept products

**Hard halts between every Pass 2 phase** — Steve confirms before each one proceeds. You can't bulldoze through.

The duplicate-rescue decision (Option 2 from prior conversation) is **baked into Phase 3 logic** — Phase 3 only moves products where `action_default == 'archive'`, automatically skipping all `archive-duplicate` rows. Steve does NOT need to edit the Pass 1 CSV first.

---

## Project context

Brant Business Interiors is a B2B Shopify store cutting over from a Starlite theme to a custom BBI design system. Currently ~80% complete (102 of 128 tracked items). Catalog is 646 products — 100 Hero already enriched. Work in flight: product enrichment for the remaining 553 non-Hero products.

- **Project root:** `/Users/leokatz/Desktop/Office Central`
- **Project rules:** `CLAUDE.md` (auto-loaded by Claude Code; you read manually)
- **Build state doc:** `BBI-Session-Kickoff/bbi-build-state.md`
- **Dev theme ID:** `186373570873` (BBI Landing Dev — only write target)
- **Live theme ID:** `178274435385` (NEVER write)
- **Shopify store:** `office-central-online.myshopify.com`
- **API token:** `SHOPIFY_TOKEN` in `.env`

---

## BBI Launch Tracker artifact

- **Cowork artifact id:** `bbi-launch-tracker`
- **Underlying HTML file:** `/Users/leokatz/Library/Application Support/Claude/local-agent-mode-sessions/.../outputs/bbi-launch-tracker.html` (find the exact path via `mcp__cowork__list_artifacts`)
- **Update mechanism:** Read the HTML → Edit in place → call `mcp__cowork__update_artifact` with `id: "bbi-launch-tracker"`, the `html_path`, and a clean `update_summary`

---

## Why PROMPT-4 needs splitting

PROMPT-4 evolved through 7 architectural pivots in one day (2026-05-11) — from "write 500 descriptions" to "soft-prune via Other collection + 5-phase Pass 2 + enrichment CSV". The single row in the tracker now has dense multi-paragraph notes. Steve can't see at a glance what's done, what's next, or what's blocked.

Split it into three discrete rows so each has its own status.

---

## What you'll do — execution order

```
STEP 0  — Safety preflight (~30 sec, verifies DEV theme)
STEP 1  — Tracker restructure (~5 min, no halts)
                ↓
PHASE 0 — PDP template patches (~5 min) >>> HALT
                ↓
PHASE 1 — Create "Other" collection (~2 min) >>> HALT
                ↓
PHASE 2 — Canary PDP test on teknion-boardroom (~5 min) >>> HALT (Steve eyeballs PDP in browser)
                ↓
PHASE 3 — Bulk move ~336 archive products to Other (~15 min, dry-run + confirm) >>> HALT
                ↓
PHASE 4 — Generate enrichment CSV for ~170 kept products (~30 min, deep research on Tier A) >>> HALT
                ↓
STEP 8  — Post-execution tracker update (~3 min, mark PE-PASS-2-PHASES done in Recently Shipped)
```

---

## STEP 0 — Safety preflight

Run this BEFORE any other work:

```bash
export $(grep -v '^#' "/Users/leokatz/Desktop/Office Central/.env" | xargs) && python3 -c "
import urllib.request, json, os
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
for name, tid in [('DEV', '186373570873'), ('LIVE', '178274435385')]:
    req = urllib.request.Request(
        f'https://{STORE}/admin/api/2026-04/themes/{tid}.json',
        headers={'X-Shopify-Access-Token': TOKEN})
    t = json.loads(urllib.request.urlopen(req).read())['theme']
    print(f'{name}: {t[\"name\"]}  role={t[\"role\"]}  id={t[\"id\"]}')
print('Write target confirmed: 186373570873 (DEV only)')
"
```

Confirm output shows DEV = unpublished, LIVE = main. If anything looks off, halt and report.

---

## STEP 1 — Tracker restructure

Find the BBI Launch Tracker HTML file via `mcp__cowork__list_artifacts` (look for id `bbi-launch-tracker`). Read it. Make these changes:

### 1a. Remove the existing PROMPT-4 row

Search for the row `<tr class="task-row" ... <td class="col-id">PROMPT-4</td>` in the Session Queue tbody. Delete it entirely. It's currently a sprawling multi-paragraph row that's being split into the rows below.

### 1b. Insert 3 new rows at the top of the Session Queue open block

In execution order:

**Row 1 — PE-PASS-2-PHASES (in progress while this session runs):**

```html
<tr class="task-row" data-status="open" data-owner="cc">
  <td class="col-id">PE-PASS-2-PHASES</td>
  <td class="col-task"><strong>🔴 PE Pass 2 — move-to-Other + enrichment CSV generation (in progress this session)</strong><span class="notes">Combined with tracker restructure 2026-05-11. <strong>Phase 0:</strong> PDP template patches (single-tier related products; breadcrumb fallback to "Other" when type tag blank; same fallback in <code>bbi-breadcrumb-jsonld.liquid</code>). <strong>Phase 1:</strong> create "Other" custom collection (handle <code>other</code>, published, manual sort, not in nav). <strong>Phase 2:</strong> canary PDP test on <code>teknion-boardroom</code> — backup state, baseline HTML, strip tags + add to Other, re-fetch, diff. Steve eyeballs PDP in browser → PROCEED or ROLLBACK. <strong>Phase 3:</strong> bulk move ~336 archive products (action_default == 'archive' only; archive-duplicate rows auto-rescued); dry-run-first, rate-limit 2 calls/sec, backed up. <strong>Phase 4:</strong> generate enrichment CSV for ~170 kept products (Tier A deep research, Tier B brand template, Tier D minimal). Hard halts between every phase.</span></td>
  <td class="col-status"><span class="badge open">In progress</span></td>
  <td class="col-owner"><span class="owner cc">Claude Code</span></td>
</tr>
```

**Row 2 — PE-CSV-EDIT (Steve's long step after Phase 4):**

```html
<tr class="task-row" data-status="open" data-owner="steve">
  <td class="col-id">PE-CSV-EDIT</td>
  <td class="col-task"><strong>Steve edits enrichment CSV in Sheets</strong><span class="notes">After PE-PASS-2-PHASES Phase 4 hands off. Open <code>data/reports/pe-kept-enrichment-2026-05-11.csv</code> in Google Sheets. ~170 rows, ~25 cols. Each <code>draft_*</code> cell pre-filled. Edit in place where corrections needed (no separate "final" column). Mark <code>steve_approval</code> per row: <code>approve</code> / <code>revise</code> / <code>skip</code>. Optional: <code>image_action = "add-real-photo"</code> if product needs a real photo. Save back as <code>pe-kept-enrichment-reviewed-YYYY-MM-DD.csv</code>. Estimated 7-12 hours focused editing (~5 min/row Tier A, ~2 min Tier B, ~30 sec Tier D).</span></td>
  <td class="col-status"><span class="badge open">After Phase 4</span></td>
  <td class="col-owner"><span class="owner steve">Steve</span></td>
</tr>
```

**Row 3 — PE-PASS-3 (Claude Code push, prompt not written yet):**

```html
<tr class="task-row" data-status="open" data-owner="cc">
  <td class="col-id">PE-PASS-3</td>
  <td class="col-task"><strong>Push reviewed enrichments to Shopify (prompt not yet written)</strong><span class="notes">After Steve finishes PE-CSV-EDIT. Validate the reviewed CSV schema. Push <code>approved</code> rows in batches of 25 (title + body_html + SEO meta + spec metafields) with rollback per batch. Logs every change to <code>data/logs/</code>. Skips <code>revise</code> and <code>skip</code> rows. Prompt to be written after PE-CSV-EDIT lands.</span></td>
  <td class="col-status"><span class="badge open">After CSV edit</span></td>
  <td class="col-owner"><span class="owner cc">Claude Code</span></td>
</tr>
```

### 1c. Update the Critical Path strip

Find the `<section class="crit">` block. Replace the existing single "PE 3-pass enrichment" step with three granular steps:

```html
<div class="crit__step current">
  <div class="crit__step-label">→ PE Pass 2 phases</div>
  <div class="crit__step-detail">PDP patches · Other · canary · bulk move · enrichment CSV</div>
</div>
<div class="crit__step">
  <div class="crit__step-label">PE CSV edit</div>
  <div class="crit__step-detail">Steve reviews ~170 kept products in Sheets</div>
</div>
<div class="crit__step">
  <div class="crit__step-label">PE Pass 3 push</div>
  <div class="crit__step-detail">Approved rows to Shopify in batches of 25</div>
</div>
```

Leave the other steps (Collection cleanup, Page image fill, Wave E hardening, SEO-AUDIT-1, Image CSV review, GO/NO-GO, Publish) unchanged.

### 1d. Update the Right Now callout

Replace existing callout content with:

```html
<div class="callout callout--now">
  <div class="callout__head"><span class="dot"></span>Right now</div>
  <h3>PE-PASS-2-PHASES in progress this session — Steve confirms each halt</h3>
  <p>Tracker restructured 2026-05-11. PROMPT-4 split into <strong>PE-PASS-2-PHASES</strong> (this session, 5 phases with hard halts), <strong>PE-CSV-EDIT</strong> (Steve's long editing pass after), and <strong>PE-PASS-3</strong> (final push prompt to be written later).</p>
  <p><strong>Duplicate rescue baked in.</strong> Phase 3 only moves <code>action_default == "archive"</code> rows (~336 products). All <code>archive-duplicate</code> rows (47 products: delivery fees, chair mats, chair variants — the false-positive clusters) are auto-rescued. Steve does NOT need to edit the Pass 1 CSV.</p>
  <p><strong>Teknion handling:</strong> the 5 Teknion $0 showcase products move to Other (per BBI Rule #2 — they stay live as quote-only pages, just relocated to /collections/other).</p>
  <p><strong>Sequence after this session lands:</strong> PE-CSV-EDIT (Steve, 7-12 hours editing) → PE-PASS-3 (Claude Code push, prompt TBD) → COLLECTION-CLEANUP-1 → PROMPT-5 → PAGE-IMG-1 → Wave E hardening.</p>
</div>
```

### 1e. Update counts

Find the header `tracker__meta strong`, progress bar `progressLabel` + fill width + legend counts, footer note counts string, and session queue progress span + fill width. Set:

- Overall: **102 done · 2 partial · 4 blocked · 22 open · 130 total · 78%**
- Session queue: **5 done · 6 open · 11 total · 45%** (was 5/9; removed 1 PROMPT-4 row, added 3 PE rows = net +2 rows = 11 total; 5 done unchanged)

Math: removed 1 row (PROMPT-4), added 3 rows (PE-PASS-2-PHASES, PE-CSV-EDIT, PE-PASS-3) → net +2 to total. 128+2 = 130. Done stays at 102. Open was 20, now 20+2 = 22. 102/130 = 78.5% → display 78%.

### 1f. Push tracker update

Call `mcp__cowork__update_artifact` with id `bbi-launch-tracker`, the html_path, and update_summary:

> "Split PROMPT-4 into PE-PASS-2-PHASES (in progress), PE-CSV-EDIT, PE-PASS-3. Critical path strip now shows 3 granular PE steps. Right Now callout reflects the duplicate-rescue-baked-in Pass 2 architecture. Counts: 102/130/78%."

---

## PHASE 0 — PDP template patches

Patch `theme/sections/ds-pdp-base.liquid` for two changes:

**PATCH A — Simplify related products to single-tier** (was 3-tier from PROMPT-3):
- Only Tier 1 logic: query `collections['all-' + type_tag.removed].products`
- Exclude current product
- Show top 4 (collection already sorted best-selling)
- Heading: "Best sellers in {Category capitalized}"
- Hide section ENTIRELY if no `type_tag` OR if filtered count == 0
- Preserve the capture pattern that worked around the `where_exp` outer-scope limit
- Remove Tier 2 (room) and Tier 3 (all-business-furniture) code entirely

**PATCH B — Breadcrumb falls back to "Other" when type_tag is blank:**

In `ds-pdp-base.liquid` breadcrumb HTML:
```liquid
{%- if type_tag != blank -%}
  <a href="/collections/{{ cat_handle }}">{{ cat_title }}</a>
{%- else -%}
  <a href="/collections/other">Other</a>
{%- endif -%}
```

In `theme/snippets/bbi-breadcrumb-jsonld.liquid`: same fallback in the schema — when product has no type tag, the breadcrumb's category item points to `/collections/other` with name "Other".

Push both files via direct API:

```bash
cd "/Users/leokatz/Desktop/Office Central" && export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
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
```

**>>> HALT — Report PHASE 0:**
- Both files pushed (HTTP 200)
- Brief diff summary (lines changed in each file)
- Smoke test URL: any normal seating PDP — confirm related products section still works with type tag intact. Heading should read "Best sellers in Seating".

Wait for Steve's "proceed" before Phase 1.

---

## PHASE 1 — Create "Other" custom collection

```bash
cd "/Users/leokatz/Desktop/Office Central" && export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
import os, json, urllib.request
STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']

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
```

**>>> HALT — Report PHASE 1:**
- Collection ID
- Handle: "other"
- URL: `https://office-central-online.myshopify.com/collections/other?preview_theme_id=186373570873`
- Confirm URL returns 200 (currently empty — that's expected)

Wait for Steve's "proceed" before Phase 2.

---

## PHASE 2 — Canary PDP test on teknion-boardroom

```bash
cd "/Users/leokatz/Desktop/Office Central" && export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
import os, json, time, urllib.request, urllib.error
STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']
THEME = '186373570873'
TEST_HANDLE = 'teknion-boardroom'

hdr = {'X-Shopify-Access-Token': TOKEN}

req = urllib.request.Request(
    f'https://{STORE}/admin/api/2024-04/products.json?handle={TEST_HANDLE}',
    headers=hdr)
prod = json.loads(urllib.request.urlopen(req).read())['products'][0]
pid = prod['id']
print(f'Test product: {prod["title"]} (id={pid})')
print(f'  Current tags: {prod["tags"]}')

os.makedirs('data/backups', exist_ok=True)
ts = time.strftime('%Y%m%d_%H%M%S')
with open(f'data/backups/canary-product-{TEST_HANDLE}-{ts}.json', 'w') as f:
    json.dump(prod, f, indent=2)
print(f'  Backup: data/backups/canary-product-{TEST_HANDLE}-{ts}.json')

baseline_url = f'https://office-central-online.myshopify.com/products/{TEST_HANDLE}?preview_theme_id={THEME}'
try:
    r = urllib.request.urlopen(
        urllib.request.Request(baseline_url, headers={'User-Agent': 'Mozilla/5.0'}))
    baseline_html = r.read().decode('utf-8', errors='replace')
    print(f'  Baseline HTTP {r.status}, {len(baseline_html)} bytes')
except urllib.error.HTTPError as e:
    print(f'  Baseline fetch error: HTTP {e.code} — dev preview may require auth')
    baseline_html = ''

with open(f'data/backups/canary-pdp-baseline-{ts}.html', 'w') as f:
    f.write(baseline_html)

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

print('\n=== DIFF SUMMARY ===')
print(f'  Baseline length: {len(baseline_html)}')
print(f'  After length:    {len(after_html)}')
print(f'  Both contain product title: {prod["title"] in baseline_html} / {prod["title"] in after_html}')
print(f'  Baseline JSON-LD count: {baseline_html.count("application/ld+json")}')
print(f'  After  JSON-LD count:   {after_html.count("application/ld+json")}')
print(f'  Baseline has .pdp-related section: {"pdp-related" in baseline_html}')
print(f'  After  has .pdp-related section:    {"pdp-related" in after_html}')
print(f'  After  mentions "Other" (new category): {"collections/other" in after_html}')

findings = {
    'test_product': TEST_HANDLE,
    'product_id': pid,
    'backup_path': f'data/backups/canary-product-{TEST_HANDLE}-{ts}.json',
    'baseline_bytes': len(baseline_html),
    'after_bytes': len(after_html),
    'title_renders_baseline': prod['title'] in baseline_html,
    'title_renders_after': prod['title'] in after_html,
    'related_section_baseline': 'pdp-related' in baseline_html,
    'related_section_after': 'pdp-related' in after_html,
    'jsonld_count_baseline': baseline_html.count('application/ld+json'),
    'jsonld_count_after': after_html.count('application/ld+json'),
    'other_in_after_breadcrumb': 'collections/other' in after_html,
}
with open(f'data/reports/canary-findings-{ts}.json', 'w') as f:
    json.dump(findings, f, indent=2)
print(f'\nFindings: data/reports/canary-findings-{ts}.json')
PYEOF
```

**>>> HALT — Report PHASE 2:**
- Test product used, backup paths
- Diff summary table
- Steve will open the PDP at the canary URL in browser (logged into Shopify admin) and decide PROCEED or ROLLBACK

If Steve says ROLLBACK: restore from backup (re-apply original tags, remove from Other), then halt for further diagnosis.

If Steve says PROCEED: continue to Phase 3.

---

## PHASE 3 — Bulk move with duplicate rescue baked in

```bash
cd "/Users/leokatz/Desktop/Office Central" && export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
import os, json, csv, time, urllib.request, urllib.error
STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']

with open('data/reports/_other-collection.json') as f:
    other_cid = json.load(f)['id']

with open('data/reports/product-triage-pass1-2026-05-11.csv') as f:
    rows = list(csv.DictReader(f))

# DUPLICATE RESCUE BAKED IN: move only 'archive', skip 'archive-duplicate' and 'move-to-other'
# Per Steve's 2026-05-11 decision (Option 2): keep all 47 duplicates as-is.
MOVE_ACTIONS = {'archive'}  # NOT archive-duplicate, NOT move-to-other
targets = []
rescued = 0
for r in rows:
    action_default = (r.get('action_default') or '').strip()
    action_override = (r.get('steve_override_action') or '').strip()
    action = action_override if action_override else action_default
    if action in MOVE_ACTIONS:
        targets.append(r)
    elif action == 'archive-duplicate':
        rescued += 1

print(f'Will move {len(targets)} products to Other.')
print(f'Auto-rescued (archive-duplicate): {rescued} products kept in original categories.')

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

CONFIRM = False  # ← Steve flips True after dry-run review

if not CONFIRM:
    print('\nDRY RUN — first 10 targets:')
    for t in targets[:10]:
        print(f'  {t["handle"]} (id={t["product_id"]}, tier={t["tier_auto"]}, '
              f'flags=[{t["archive_reason"]}])')
    print(f'\nTotal to move: {len(targets)}')
    print(f'Rescued duplicates: {rescued}')
    print(f'Set CONFIRM = True and re-run to execute.')
else:
    print('\nExecuting bulk move...')
    ok, fail = 0, []
    for i, t in enumerate(targets):
        pid = t['product_id']
        req = urllib.request.Request(
            f'https://{STORE}/admin/api/2024-04/products/{pid}.json?fields=id,tags',
            headers=hdr)
        try:
            d = json.loads(urllib.request.urlopen(req).read())['product']
        except Exception as e:
            fail.append({'handle': t['handle'], 'error': f'fetch: {e}'})
            continue
        new_tags = ','.join(
            tag.strip() for tag in (d['tags'] or '').split(',')
            if not tag.strip().startswith('type:')
            and not tag.strip().startswith('room:')
        )
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
```

**>>> HALT — Report PHASE 3 (dry-run):**
- Total targets, rescued count
- First 10 targets
- Backup path

Steve confirms: PROCEED → flip `CONFIRM = True` and re-run the same script to execute. Or BACK OUT → no action taken, backup is the rollback.

After execute: report ok/fail count, any failure log path, sample-verify 5 random moved products (visible in /collections/other, NOT in /collections/all-<their-old-type>).

---

## PHASE 4 — Generate enrichment CSV for kept products

Read the Pass 1 CSV. Filter to rows where action is NOT in `{archive, archive-duplicate, move-to-other, leave-unpublished}` — these are the kept products. Generate drafts per the locked PE-1 voice.

**TIERED RESEARCH:**
- Tier A: deep specs research via brand source URLs (Global, Teknion, ObusForme, ergoCentric, OTG, Keilhauer, Kimball, Mayline, Fellowes, Deflecto). Read the brand page, populate spec data, generate draft.
- Tier B: research only if brand is in known list; else template draft.
- Tier D: minimal template draft.

**LOCKED DRAFT FORMAT (matches PE-1 shipped):**
- Bold lede sentence (1 line)
- Context paragraph (3-5 sentences, conversational, B2B voice)
- `<h3>Key features</h3>` + `<ul>` 5-9 bullets, factual + sourced
- `<h3>Who it's for</h3>` + paragraph naming buyer roles + institutional verticals (municipal, school board, family health team, professional services)
- BBI close with "Call 1-800-835-9565" CTA
- OECM signal when product fits institutional procurement
- "Canadian-made" signal when brand origin confirmed
- NEVER fabricate dimensions, model codes, warranty terms, or certifications. If not in source, note "no model code in source" rather than invent.

**Title format (LOCKED from pe3-hero100-titles.csv):**
- `<Brand> <Model-Code> <Product Title>`, sentence case, ≤60 chars
- Drop "| Brant Business Interiors" suffix if it pushes over 60

**SEO title:** 50-60 chars, keyword-first. **SEO desc:** 140-155 chars, includes spec + use case.

**CSV columns (in this order):**

```
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
```

Output: `data/reports/pe-kept-enrichment-2026-05-11.csv`, sorted by category (current_type_tag), then by tier.

**>>> HALT — Report PHASE 4:**
- CSV path + total rows
- Tier breakdown (A / B / D counts)
- draft_confidence distribution (high / medium / low / none)
- Top 5 rows with draft_confidence = "none" — candidates for Steve to consider move-to-other later
- Top 5 rows where Tier A deep research couldn't find source URLs
- Estimated Steve editing time

---

## STEP 8 — Post-execution tracker update

After Phase 4 lands, update the tracker to reflect what shipped:

### 8a. Add a row to Recently Shipped

Insert this near the top of the Recently Shipped tbody (above the existing PE-PASS-1-AUDIT row):

```html
<tr class="task-row" data-status="done" data-owner="cc">
  <td class="col-id">PE-PASS-2-PHASES</td>
  <td class="col-task"><strong>PE Pass 2 — move-to-Other + enrichment CSV (2026-05-11)</strong><span class="notes">All 5 phases completed. <strong>Phase 0:</strong> PDP template patches deployed (single-tier related products + breadcrumb fallback to "Other" when type tag blank). <strong>Phase 1:</strong> Other custom collection created (id captured in <code>data/reports/_other-collection.json</code>). <strong>Phase 2:</strong> canary test on teknion-boardroom PASSED. <strong>Phase 3:</strong> bulk moved N products to Other (47 duplicates auto-rescued, kept in original categories). <strong>Phase 4:</strong> enrichment CSV generated at <code>data/reports/pe-kept-enrichment-2026-05-11.csv</code> with M rows (drafts pre-filled). Backup files in <code>data/backups/</code>. Next step: Steve edits the enrichment CSV (PE-CSV-EDIT row in Session Queue).</span></td>
  <td class="col-status"><span class="badge done">Done</span></td>
  <td class="col-owner"><span class="owner cc">Claude Code</span></td>
</tr>
```

Fill in the actual N (moved count) and M (CSV row count) from Phase 3 + Phase 4 output.

### 8b. Remove PE-PASS-2-PHASES from Session Queue (or mark its status done in place)

Either:
- **Remove** the open PE-PASS-2-PHASES row from Session Queue (cleanest — done work doesn't clutter the queue)
- OR **mark in place** with `data-status="done"` and badge "Done" — keeps the row visible in queue for history

Either is fine. Pick one based on which the rest of the queue uses (look at how COLLECTION-DS-1 and PROMPT-3 etc. are handled — they're left in queue marked done).

### 8c. Update Right Now callout to point at PE-CSV-EDIT

```html
<div class="callout callout--now">
  <div class="callout__head"><span class="dot"></span>Right now</div>
  <h3>Steve: edit the enrichment CSV in Google Sheets (~7-12 hours)</h3>
  <p>PE-PASS-2-PHASES ✓ shipped. CSV at <code>data/reports/pe-kept-enrichment-2026-05-11.csv</code> — M rows, ~25 cols, drafts pre-filled. Edit cells in place where corrections needed, mark <code>steve_approval</code> per row (<code>approve</code> / <code>revise</code> / <code>skip</code>). Save back as <code>pe-kept-enrichment-reviewed-YYYY-MM-DD.csv</code>.</p>
  <p>Once approved, fire PE-PASS-3 to push approvals to Shopify (prompt to be written after CSV edit lands).</p>
</div>
```

### 8d. Update counts

- Overall: **103 done · 2 partial · 4 blocked · 21 open · 130 total · 79%** (PE-PASS-2-PHASES now done = +1 done, -1 open; total unchanged because we moved a row from queue to shipped)
- Session queue: **6 done · 5 open · 11 total · 55%** (PE-PASS-2-PHASES marked done if left in queue; or **5 done · 5 open · 10 total · 50%** if removed)

### 8e. Push final tracker update

```
mcp__cowork__update_artifact
  id: "bbi-launch-tracker"
  html_path: <same path>
  update_summary: "PE-PASS-2-PHASES ✓ shipped: PDP patches deployed, Other collection created, N products moved (47 duplicates rescued), enrichment CSV generated with M rows. Right Now callout points at PE-CSV-EDIT (Steve's long editing pass). Counts: 103/130/79%."
```

---

## Verification before closing the session

After Step 8e, verify:

- [ ] Tracker artifact updated and visible in Cowork sidebar
- [ ] PE-PASS-2-PHASES status reflects done across all surfaces (Recently Shipped, Right Now callout, counts)
- [ ] All backup files exist:
  - `data/backups/canary-product-teknion-boardroom-<ts>.json`
  - `data/backups/canary-pdp-baseline-<ts>.html`
  - `data/backups/canary-pdp-after-<ts>.html`
  - `data/backups/pre-move-state-<ts>.json`
- [ ] CSV exists: `data/reports/pe-kept-enrichment-2026-05-11.csv`
- [ ] Failures log (if any): `data/reports/move-failures-<ts>.json`
- [ ] `data/reports/_other-collection.json` exists with the Other collection ID
- [ ] Spot-check: 5 random moved products visible at `/collections/other?preview_theme_id=186373570873`, NOT visible in `/collections/all-<their-old-type>`

Report final summary to Steve:
1. Tracker restructured ✓
2. PDP patches pushed ✓
3. Other collection created (id, URL)
4. Canary test result
5. Bulk move stats (success/fail, rescued count)
6. Enrichment CSV generated (rows, tier distribution, draft confidence distribution)
7. Next Steve action: edit the enrichment CSV in Sheets

---

## Hard rules (apply throughout)

- Theme writes: ONLY to dev theme `186373570873`. Never to live `178274435385`.
- HR1 baked into Phase 3 logic: products with `action_default == 'archive-duplicate'` are automatically skipped (the 47 false-positive duplicates).
- HR2: unpublished products are never touched (their `action_default = 'leave-unpublished'`, won't match Phase 3 filter or Phase 4 keep filter).
- HR3: the 100 Hero products are skipped — they're not in the Pass 1 CSV working set.
- HR4: Pass 1 already shipped (read-only audit). This session executes Pass 2. Pass 3 (push approved drafts to Shopify) is a separate session, prompt not yet written.
- HR5: HARD HALTS between every Pass 2 phase. Do not bulldoze through. Steve confirms each transition.

---

## Context dump — for reference if questions arise mid-session

**Move-to-Other rationale.** Soft-prune via "Other" collection instead of hard archive. Preserves URLs (no broken bookmarks), preserves SEO equity (no inbound link rot), keeps products quotable, fully reversible. The "Other" collection is published but NOT in nav — accessible by direct URL only. Junk-drawer behavior.

**Tag-strip mechanics.** When a product loses its `type:*` tag, it auto-drops out of the smart collection `all-<type>` (smart collections key on tags). Same for `room:*` tags. The product stays at `status=active`, URL unchanged, PDP still renders.

**PDP for tag-less products.** After PHASE 0 patches: breadcrumb shows "Home → Shop Furniture → Other → Product" with "Other" linked to `/collections/other`. Related products section is hidden entirely (no type tag → no Tier 1 query → section skipped). JSON-LD breadcrumb schema uses the same "Other" fallback so Google Rich Results validates.

**Voice format (LOCKED from PE-1 shipped CSVs):**
1. Bold lede sentence
2. Context paragraph (3-5 sentences, B2B voice)
3. `<h3>Key features</h3>` + `<ul>` 5-9 bullets, factual + sourced
4. `<h3>Who it's for</h3>` + audience paragraph
5. BBI close with `Call 1-800-835-9565` CTA
6. OECM / Canadian-made signals when applicable
7. Never fabricate specs

**Files of interest:**
- `data/reports/product-triage-pass1-2026-05-11.csv` — Pass 1 audit output, input to Phase 3
- `data/reports/pe1-hero100-descriptions.csv` — voice anchor for body_html
- `data/reports/pe3-hero100-titles.csv` — title format anchor
- `data/reports/pe7-longtail-seo.csv` — SEO meta format anchor
- `data/specs/specs.json` — existing spec research with manufacturer URLs
- `docs/strategy/icp.md`, `docs/strategy/voice-samples.md` — audience + voice

If any path is missing, look in `Prompt-4-Bundle/` for alternate location (the Pass 1 session noted some files were under there).
