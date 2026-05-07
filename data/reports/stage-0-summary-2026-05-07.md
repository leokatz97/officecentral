# Stage 0 Summary — Design System Remediation 2026-05-07

**Generated:** 2026-05-07  
**Auditor:** Claude Code (Stage 0 audit — no pushes, no edits to build-state)  
**Artifacts produced:**
- `data/reports/audit-routes-2026-05-07.csv` — 34 URL probes
- `data/reports/page-records-2026-05-07.csv` — 22 Shopify Page records cross-referenced
- `data/reports/design-baseline-2026-05-07/manifest.json` — 10 baseline screenshots documented
- `data/reports/row-reverify-2026-05-07.md` — all ✅ rows re-evaluated

---

## 1. Total 404s

**10 URLs return non-200 on the public site:**

| URL | Status | Root Cause |
|---|---|---|
| /pages/about | 404_DRAFT | Shopify Page exists with correct suffix but is DRAFT (unpublished) |
| /pages/brands | 404_DRAFT | Same — DRAFT |
| /pages/brands-keilhauer | 404_DRAFT | Same — DRAFT |
| /pages/brands-global-teknion | 404_DRAFT | Same — DRAFT |
| /pages/brands-ergocentric | 404_DRAFT | Same — DRAFT |
| /pages/our-work | 404_DRAFT | Same — DRAFT |
| /pages/delivery | 404_DRAFT | Same — DRAFT |
| /pages/relocation | 404_DRAFT | Same — DRAFT |
| /pages/customer-stories | 404 | **ROOT_CAUSE_404** — no Shopify Page record at all |
| /pages/oecm-agreement | 404 | Stale CTA reference — no Page record, no template, no plan for this handle |

**The original remediation hypothesis was wrong.** The plan assumed missing Page records were the primary cause. The audit shows the opposite: 8 of 9 nav-linked pages DO have Page records with correct template_suffix values — they are simply DRAFT. The only genuine missing record is `customer-stories`.

---

## 2. Chrome Inconsistencies

### A — 404 page chrome bug (all 404 responses show Starlite header)
`template == '404'` is absent from the `bbi_landing` gate in **both** the worktree `theme.liquid` and the dev theme's `theme.liquid`. Every 404 response (DRAFT pages, ROOT_CAUSE_404, garbage URLs) renders Starlite chrome above the BBI custom 404 content — a visual collision that presents the BrantBasics header to users who hit dead links.

This affects: /pages/about, /pages/brands-keilhauer, /pages/customer-stories, and any other 404 encountered by users. **Fix: add `or template == '404'` to bbi_landing gate.**

### B — Worktree gate ≠ dev theme gate (push hazard)
The worktree `theme/layout/theme.liquid` and the dev theme's live `layout/theme.liquid` have diverged:

| Capability | Worktree gate | Dev theme gate |
|---|---|---|
| Collection templates | Per-suffix enumeration (12 entries) | `template.name == 'collection'` (1 clause, all covered) |
| Wave C page suffixes | Missing all 9 (about, brands*, delivery, relocation, our-work, contact) | All 9 present |
| product template | Missing | `template == 'product'` present |
| 404 template | Missing | Missing (bug in both) |

A push of `theme.liquid` from this worktree (without first syncing) would overwrite the dev theme with the less-complete gate, breaking BBI chrome on all Wave C pages and all PDPs. **This is the highest-severity finding from the audit.**

### C — Logo renders as text on homepage (CONTENT-1)
Homepage design baseline screenshot shows "Brant BASICS Interiors" text wordmark instead of the image logo. The `logo` image_picker value in `theme/templates/index.json` is either cleared or pointing to a stale CDN URL. CONTENT-1 is an open `🔔 NEEDS DECISION` row — this gap is expected and tracked.

### D — Starlite Chat widget on sub-collection pages
`/collections/highback-seating` design baseline shows the Starlite Shopify Chat widget persisting in the bottom-right corner. This is a Starlite app-embed that is not suppressed when BBI chrome renders. Not a gate bug — an app-embed suppression gap on sub-collection pages.

### E — Policies pages — no BBI chrome (expected, but confirm before launch)
`/policies/privacy-policy`, `/policies/terms-of-service`, `/policies/shipping-policy` all return 200 but with `has_bbi_nav=false, has_bbi_footer=false` (Starlite chrome). Policy pages are Shopify-generated and cannot have a template suffix. They are correctly excluded from `bbi_landing`. This is expected behavior per architecture — confirm with Steve pre-launch that the Starlite chrome on policies pages is acceptable.

---

## 3. Build-State Row Count — ✅ → Needs Correction

**No rows are fully regressed (⬜).** All committed work is present in git and functional where tested.

### Provisional rows (keep ✅ in build-state, add noted gap):
| Row | Gap | Stage 1 action |
|---|---|---|
| NAV-3 | Worktree gate missing Wave C + product suffixes | **Sync gate as Step 1 of Stage 1** |
| NAV-4 | Logo text fallback on homepage (CONTENT-1 active) | Covered by CONTENT-1 decision |
| PB-9 | Worktree uses per-suffix enumeration vs. dev `template.name` | Resolve during gate sync |
| P2-2 Seating | Hero image not set, CTA copy wrong | Content task, not code |
| INTERLINK-1 | 92 WARNs on auth-gated checks | Rerun after launch |

**Total rows to drop from ✅: 0** (all provisional, none regressed)

### Wave B documentation lag (mark ✅ in Stage 1):
All 4 Wave B rows are committed but show ⬜ in build-state — the file was not updated at commit time.

| Row | Evidence SHA |
|---|---|
| PB-14 | `66f7623` |
| PB-15 | `de3237e` |
| P3-rollout | `aaa105a` |
| INTERLINK-2 | `82c64c8` |

---

## 4. Dev Theme vs. Worktree Drift (scope not in build-state)

The following theme files exist in the dev theme but are **not committed to the worktree git**:

| File | Type | Notes |
|---|---|---|
| `layout/theme.liquid` | Layout | Gate extended (Wave C + product); not reflected in git |
| `templates/page.about.json` | Template | Wave C — DRAFT |
| `templates/page.brands.json` | Template | Wave C — DRAFT |
| `templates/page.brands-keilhauer.json` | Template | Wave C — DRAFT |
| `templates/page.brands-global-teknion.json` | Template | Wave C — DRAFT |
| `templates/page.brands-ergocentric.json` | Template | Wave C — DRAFT |
| `templates/page.our-work.json` | Template | Wave C — DRAFT |
| `templates/page.delivery.json` | Template | Wave C — DRAFT |
| `templates/page.relocation.json` | Template | Wave C — DRAFT |
| `templates/page.contact.json` | Template | Published — contact page live |
| `templates/page.customer-stories.json` | Template | Wave G — no Page record |
| `sections/ds-lp-about.liquid` | Section | Wave C |
| `sections/ds-lp-brands.liquid` | Section | Wave C |
| `sections/ds-lp-brands-keilhauer.liquid` | Section | Wave C |
| `sections/ds-lp-brands-global-teknion.liquid` | Section | Wave C |
| `sections/ds-lp-brands-ergocentric.liquid` | Section | Wave C |
| `sections/ds-lp-our-work.liquid` | Section | Wave C |
| `sections/ds-lp-delivery.liquid` | Section | Wave C |
| `sections/ds-lp-relocation.liquid` | Section | Wave C |
| `sections/ds-lp-contact.liquid` | Section | Published |
| `sections/ds-lp-customer-stories.liquid` | Section | Wave G |

These were built and pushed to Shopify directly (not via worktree) in a session that ran without proper worktree sync. The build-state Wave C rows correctly show ⬜ (not built via proper workflow). The dev theme is ahead of git.

---

## 5. Recommended Stage 1 Start Point

**Stage 1 goal:** Close the gap between dev theme reality and build-state records. Enable all 8 DRAFT pages to be published. Fix the 404 chrome bug.

### Step 1 — Reconcile worktree gate (BLOCKING — do before any theme.liquid push)
Pull `layout/theme.liquid` from dev theme via Shopify Assets API and commit it to the worktree. Alternatively, manually add the 9 missing Wave C suffixes + `template == 'product'` + `template == '404'` to the worktree gate. Verify with `diff` before pushing. This is the single most dangerous open item.

**Gate additions needed in worktree:**
```liquid
or template.suffix == 'about'
or template.suffix == 'brands'
or template.suffix == 'brands-keilhauer'
or template.suffix == 'brands-global-teknion'
or template.suffix == 'brands-ergocentric'
or template.suffix == 'our-work'
or template.suffix == 'delivery'
or template.suffix == 'relocation'
or template.suffix == 'contact'
or template.suffix == 'customer-stories'
or template == 'product'
or template == '404'
```
(Also consider adopting dev theme's cleaner `template.name == 'collection'` to replace the 12-entry enumeration.)

### Step 2 — Commit Wave C files from dev theme to worktree git
Pull each `ds-lp-*.liquid` section and `page.*.json` template from the dev theme and commit them. This syncs git with what is already running on the dev theme. No new builds — just capturing existing work.

### Step 3 — Publish 8 DRAFT pages
Use the Admin API to set `published_at` on the 8 DRAFT Page records (about, brands, brands-keilhauer, brands-global-teknion, brands-ergocentric, our-work, delivery, relocation). These pages already have correct templates — they just need to be made public. After publish, re-run route audit to confirm 200s.

### Step 4 — Create customer-stories Shopify Page record
POST a new Page with `handle: customer-stories`, `template_suffix: customer-stories`. The template exists in the dev theme. This moves customer-stories from ROOT_CAUSE_404 to DRAFT_OK_TEMPLATE. (CS-1 in Wave G covers building the actual content.)

### Step 5 — Update Wave B rows in build-state
Mark PB-14, PB-15, P3-rollout, INTERLINK-2 as ✅ with their respective SHAs.

### Step 6 (optional, low risk) — Remove stale Page records
The `brand-dealer` and `smoke-test` Shopify Page records (STALE_ORPHAN in page-records CSV) have no templates and no nav links. They can be unpublished or left alone — they cause no 404s in the nav since no links point to them.

---

## Appendix — Artifact Locations

| Artifact | Path |
|---|---|
| Route audit CSV | `data/reports/audit-routes-2026-05-07.csv` |
| Page records CSV | `data/reports/page-records-2026-05-07.csv` |
| Design baseline manifest | `data/reports/design-baseline-2026-05-07/manifest.json` |
| Row reverify | `data/reports/row-reverify-2026-05-07.md` |
| This summary | `data/reports/stage-0-summary-2026-05-07.md` |
| Route audit script | `scripts/stage0-route-audit.py` |
| Page records script | `scripts/stage0-page-records.py` |
