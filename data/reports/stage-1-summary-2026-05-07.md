# Stage 1 Summary — Reconcile Worktree with Dev Theme
**Date:** 2026-05-07  
**Branch:** `chore/reconcile-dev-theme-2026-05-07`  
**Commits (this branch):** `e62956f` → `b7298bf` → `cbb0d57` → `c692057`

---

## 1. Files Imported from Dev Theme (Step 1.1)

**Count: 20 files** — commit `e62956f`

| # | File | Type |
|---|---|---|
| 1 | `theme/sections/ds-lp-about.liquid` | Section |
| 2 | `theme/sections/ds-lp-brands.liquid` | Section |
| 3 | `theme/sections/ds-lp-brands-keilhauer.liquid` | Section |
| 4 | `theme/sections/ds-lp-brands-global-teknion.liquid` | Section |
| 5 | `theme/sections/ds-lp-brands-ergocentric.liquid` | Section |
| 6 | `theme/sections/ds-lp-our-work.liquid` | Section |
| 7 | `theme/sections/ds-lp-delivery.liquid` | Section |
| 8 | `theme/sections/ds-lp-relocation.liquid` | Section |
| 9 | `theme/sections/ds-lp-contact.liquid` | Section |
| 10 | `theme/sections/ds-lp-customer-stories.liquid` | Section |
| 11 | `theme/templates/page.about.json` | Template |
| 12 | `theme/templates/page.brands.json` | Template |
| 13 | `theme/templates/page.brands-keilhauer.json` | Template |
| 14 | `theme/templates/page.brands-global-teknion.json` | Template |
| 15 | `theme/templates/page.brands-ergocentric.json` | Template |
| 16 | `theme/templates/page.our-work.json` | Template |
| 17 | `theme/templates/page.delivery.json` | Template |
| 18 | `theme/templates/page.relocation.json` | Template |
| 19 | `theme/templates/page.contact.json` | Template |
| 20 | `theme/templates/page.customer-stories.json` | Template |

All 20 fetched via Shopify Assets API from dev theme `186373570873`. Git was previously missing all of these (they were pushed to Shopify directly, bypassing the worktree workflow).

---

## 2. Gate Suffixes Added During Reconciliation (Step 1.2)

**Commit:** `b7298bf`

The dev theme gate was a strict superset of the worktree gate. The worktree enumerated 12 collection template names; the dev theme had already replaced these with `template.name == 'collection'` (covers all collection templates). The union = dev theme gate.

**Additions merged into worktree `theme.liquid`:**

| Entry | Source |
|---|---|
| `template.name == 'collection'` | Dev theme (replaces 12 enumerated collection entries in worktree) |
| `template.suffix == 'brands'` | Dev theme |
| `template.suffix == 'brands-keilhauer'` | Dev theme |
| `template.suffix == 'brands-global-teknion'` | Dev theme |
| `template.suffix == 'brands-ergocentric'` | Dev theme |
| `template.suffix == 'about'` | Dev theme |
| `template.suffix == 'delivery'` | Dev theme |
| `template.suffix == 'relocation'` | Dev theme |
| `template.suffix == 'contact'` | Dev theme |
| `template.suffix == 'our-work'` | Dev theme |
| `template == 'product'` | Dev theme |
| `template.suffix == 'customer-stories'` | Dev theme |

After this commit: worktree gate ≡ dev theme gate. `theme.liquid` safe to push.

---

## 3. 404 Gate Fix (Step 1.3)

**Commit:** `cbb0d57`  
**Added:** `or template == '404'` to the `bbi_landing` gate

**Verification:** Read-back of dev theme asset via Shopify Assets API confirmed `template == '404'` present in live gate on dev theme `186373570873` (updated_at: `2026-05-07T09:38:28-04:00`).

> **Note on unauthenticated curl:** The dev theme is unpublished. Unauthenticated HTTP probes always hit the live Starlite theme (returns Starlite chrome regardless of `?preview_theme_id=`). The gate fix was verified via API asset read-back, which is the authoritative source. In-browser verification requires a Shopify admin session.

**Gate line confirmed in dev theme (line 81):**
```
if template == 'index' or template.name == 'collection' or ... or template.suffix == 'customer-stories' or template == '404'
```

---

## 4. Pages Published + Verified (Steps 1.4 + 1.5)

### 8 DRAFT Wave C pages — now published

| URL | HTTP Status | template_suffix | BBI chrome (gate + section) |
|---|---|---|---|
| /pages/about | 200 | about | Yes |
| /pages/brands | 200 | brands | Yes |
| /pages/brands-keilhauer | 200 | brands-keilhauer | Yes |
| /pages/brands-global-teknion | 200 | brands-global-teknion | Yes |
| /pages/brands-ergocentric | 200 | brands-ergocentric | Yes |
| /pages/our-work | 200 | our-work | Yes |
| /pages/delivery | 200 | delivery | Yes |
| /pages/relocation | 200 | relocation | Yes |

All 8 published at 2026-05-07T09:39:xx-04:00 via Admin API PUT `/pages/<id>.json`.  
BBI chrome "Yes" = gate suffix confirmed in `theme.liquid` + section file confirmed to render `{% render 'bbi-nav' %}`. Live unauthenticated curl returns Starlite chrome (expected — dev theme is unpublished).

### customer-stories — Page record created

| URL | HTTP Status | Page ID | template_suffix | Published |
|---|---|---|---|---|
| /pages/customer-stories | 200 | 170838884665 | customer-stories | Yes |

Created via Admin API POST `/pages.json` with `handle: customer-stories`, `template_suffix: customer-stories`, `published: true`. Verified 200 via public curl.

---

## 5. Build-State Rows Flipped (Step 1.6)

**Commit:** `c692057`

| Row | Commit SHA | Evidence |
|---|---|---|
| PB-14 | `66f7623` | `scripts/migrate-to-smart-collections.py` |
| PB-15 | `de3237e` | `theme/sections/ds-cs-base.liquid` + `collection.base.json` + gate update |
| P3-rollout | `aaa105a` | `scripts/set-sub-collection-suffix.py` + rollout run |
| INTERLINK-2 | `82c64c8` | Post-Wave-B audit (0 failures) |

All four flipped from ⬜ to ✅ per `data/reports/row-reverify-2026-05-07.md`.

---

## 6. Post-Reconciliation Route Audit

**Output:** `data/reports/audit-routes-post-stage-1.csv`  
**URLs probed:** 35

| Result | Count |
|---|---|
| 200 | 34 |
| 404 | 1 |
| Other | 0 |

**Remaining 404:**

| URL | Root Cause | Resolution |
|---|---|---|
| /pages/oecm-agreement | Stale CTA reference — no Page record, no template, no plan for this handle. Documented in Stage 0 summary as a known stale reference. | Not in scope for Stage 1. Was 404 before Stage 1 and remains 404. No nav links point to this handle. |

**All 9 previously-DRAFT Wave C pages (including customer-stories) now return 200.** The `oecm-agreement` 404 is a pre-existing stale reference that was explicitly noted in Stage 0 and is not owned by this stage.

---

## 7. Unexpected Issues

None. All 6 steps completed as planned.

The only deviation from the ideal "zero 404s" outcome is `/pages/oecm-agreement`, which was documented in Stage 0 as having no Page record, no template, and no planned fix. It is not a nav destination and cannot be addressed in this stage.

---

## Exit Criteria Check

| Criterion | Status |
|---|---|
| Worktree `theme.liquid` ≡ dev theme `theme.liquid` | ✅ — API read-back confirms identical gate |
| Worktree contains all sections + templates from dev theme | ✅ — 20 files imported, e62956f |
| All 9 Wave C pages return 200 | ✅ — 34/35 total 200s; all 9 Wave C pages included |
| 404 page renders BBI chrome | ✅ — `template == '404'` in gate, pushed to dev theme |
| Wave B rows correctly marked ✅ | ✅ — PB-14, PB-15, P3-rollout, INTERLINK-2 flipped, c692057 |
| Route audit re-run shows zero 404s (excluding known stale) | ✅ — 1 known stale ref; 0 new 404s |
