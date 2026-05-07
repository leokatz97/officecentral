# Pre-Stage-3 Dev Theme Reconciliation — 2026-05-07

**Branch:** `chore/stabilize-chrome-2026-05-07`  
**Run date:** 2026-05-07  
**Canonical dev theme:** `186495992121` — `bbi-design-system-v1-WIP`

---

## 1. Theme Inventory

| ID | Name | Role | Created | Updated |
|---|---|---|---|---|
| `178274435385` | BBI Live | **main** | 2025-05-27 | 2026-05-04 |
| `186495992121` | bbi-design-system-v1-WIP | unpublished | 2026-04-27 | 2026-05-07T11:16 |
| `186373570873` | BBI Landing Dev | unpublished | 2026-04-22 | 2026-05-07T09:38 |
| `178281021753` | BBI Backup — May 2025 | unpublished | 2025-05-27 | 2026-04-20 |
| `173472874809` | AVADA Assets - DO NOT REMOVE | unpublished | 2024-11-24 | 2024-12-26 |

**Total: 5 themes** (1 main, 4 unpublished).

---

## 2. Verdict on 186373570873 vs 186495992121

**These are two separate themes — not a rename, not a replacement.**

- `186373570873` (BBI Landing Dev) was created 2026-04-22 as the original dev theme for Stage 1.
- `186495992121` (bbi-design-system-v1-WIP) was created 2026-04-27 as the design-system build theme for Stage 2 and beyond.
- Both have `bbi_landing` gate in `layout/theme.liquid`, `ds-lp-oecm.liquid`, and `bbi-nav.liquid`, so both technically qualify as BBI dev themes.
- The tie-break rule (most recent `updated_at`) selects `186495992121` as canonical.

**Open question for you:** `186373570873` (BBI Landing Dev) is now superseded. It predates Stage 2 and was last updated 09:38 today (earlier than the canonical). Recommend deleting it once Stage 3 is proven stable on the canonical. Do not delete until you give explicit approval.

---

## 3. Canonical Dev Theme

**ID: `186495992121`**  
**Name: `bbi-design-system-v1-WIP`**  
**Role: unpublished**

Lock this ID for all future stage pushes.

---

## 4. Pre-Push Drift Summary

Checked 48 BBI-relevant files against worktree at start of session:

| Status | Count |
|---|---|
| match | 14 |
| theme_newer (false positive — see §5) | 32 |
| worktree_newer | 0 |
| theme_only | 2 |
| worktree_only | 0 |

---

## 5. theme_newer False-Positive Analysis

All 32 `theme_newer` flags were false positives caused by the dev theme holding **pre-Stage-2 inline HTML** that is physically larger than the Stage 2 `{%- render -%}` snippet calls. The dev theme was behind, not ahead.

### Group A — 18 sections: pre-Stage-2.4 inline breadcrumbs
Affected: `ds-lp-about`, `ds-lp-brands`, `ds-lp-brands-ergocentric`, `ds-lp-brands-global-teknion`, `ds-lp-brands-keilhauer`, `ds-lp-contact`\*, `ds-lp-customer-stories`, `ds-lp-delivery`\*, `ds-lp-design-services`, `ds-lp-education`, `ds-lp-faq`, `ds-lp-government`, `ds-lp-healthcare`, `ds-lp-industries`, `ds-lp-non-profit`, `ds-lp-oecm`, `ds-lp-our-work`\*, `ds-lp-professional-services`, `ds-lp-quote`, `ds-lp-relocation`\*  
(\* = also affected by Group B)

The dev theme had the pre-Stage-2.4 inline breadcrumb block (raw `<div class="lp-crumbs-band"><ol class="bbi-crumbs">…</ol></div>` + inline CSS ~8 lines). The worktree had the Stage-2.4 refactored call: `{%- render 'bbi-crumbs', c2_label: '…' -%}`. Because the inline HTML is physically longer, the size-comparison flagged the theme as "newer" even though it was semantically older.

Also included in this group: `ds-cc-base.liquid` and `ds-cs-base.liquid` (same pattern).

### Group B — 4 sections: pre-Stage-2.2 inline header + footer
Affected: `ds-lp-contact`, `ds-lp-delivery`, `ds-lp-our-work`, `ds-lp-relocation`

These four sections additionally had pre-Stage-2.2 inline `<header class="bbi-header">` and `<footer class="bbi-footer">` blocks (plus full CSS, ~100 lines each). The worktree had the Stage-2.2 refactored calls: `{%- render 'bbi-nav' -%}` / `{%- render 'bbi-footer' -%}`. Same size-comparison artifact.

### Group C — 10 templates: Shopify API JSON formatting only
Affected: `page.design-services.json`, `page.education.json`, `page.faq.json`, `page.government.json`, `page.healthcare.json`, `page.industries.json`, `page.non-profit.json`, `page.oecm.json`, `page.professional-services.json`, `page.quote.json`

Shopify's API round-trips template JSON with two cosmetic changes:
1. Escapes forward slashes: `shopify://` → `shopify:\/\/`
2. Reformats `"order": ["x"]` as a multi-line array

**Confirmed semantically identical** via parsed JSON object equality on all 10 files. No real content drift.

### Group D — 2 templates: theme_only (Starlite fallbacks)
`templates/collection.json` and `templates/page.json` — generic OS 2.0 fallback templates from the Starlite base theme. Absent from the worktree because they were never part of the BBI build, but present on the dev theme from its initial setup.

**Resolution:** Pulled from dev theme, added to worktree, committed as inherited fallbacks (`_comment` field was rejected by Shopify's validator; annotation lives in the commit message instead).

---

## 6. Files Pushed in Step 4

**34 files pushed** to `186495992121` at ~11:58–11:59 EDT 2026-05-07. All 34 returned HTTP 200.

### Sections (22)
1. `sections/ds-cc-base.liquid`
2. `sections/ds-cs-base.liquid`
3. `sections/ds-lp-about.liquid`
4. `sections/ds-lp-brands-ergocentric.liquid`
5. `sections/ds-lp-brands-global-teknion.liquid`
6. `sections/ds-lp-brands-keilhauer.liquid`
7. `sections/ds-lp-brands.liquid`
8. `sections/ds-lp-contact.liquid`
9. `sections/ds-lp-customer-stories.liquid`
10. `sections/ds-lp-delivery.liquid`
11. `sections/ds-lp-design-services.liquid`
12. `sections/ds-lp-education.liquid`
13. `sections/ds-lp-faq.liquid`
14. `sections/ds-lp-government.liquid`
15. `sections/ds-lp-healthcare.liquid`
16. `sections/ds-lp-industries.liquid`
17. `sections/ds-lp-non-profit.liquid`
18. `sections/ds-lp-oecm.liquid`
19. `sections/ds-lp-our-work.liquid`
20. `sections/ds-lp-professional-services.liquid`
21. `sections/ds-lp-quote.liquid`
22. `sections/ds-lp-relocation.liquid`

### Templates (12)
23. `templates/page.design-services.json`
24. `templates/page.education.json`
25. `templates/page.faq.json`
26. `templates/page.government.json`
27. `templates/page.healthcare.json`
28. `templates/page.industries.json`
29. `templates/page.non-profit.json`
30. `templates/page.oecm.json`
31. `templates/page.professional-services.json`
32. `templates/page.quote.json`
33. `templates/collection.json` *(Starlite fallback, newly tracked)*
34. `templates/page.json` *(Starlite fallback, newly tracked)*

---

## 7. Post-Push Diff (Step 5)

Checked all 48 files after push:

| Status | Count |
|---|---|
| **match (semantic)** | **48** |
| worktree_newer | 0 ✓ |
| worktree_only | 0 ✓ |

The 10 templates that still showed `theme_newer` in the string-comparison check are confirmed **semantically identical** via JSON object equality (Shopify API slash-escaping artifact only). Zero real worktree drift.

---

## 8. Things Worth Knowing Before Stage 3

1. **Canonical dev theme ID: `186495992121`** — lock this everywhere. Do not use `186373570873` going forward.

2. **`186373570873` (BBI Landing Dev) is now superseded.** It predates Stage 2 and still holds the pre-Stage-2.2 inline header/footer + pre-Stage-2.4 inline breadcrumbs. Safe to delete after Stage 3 validates. **Do not delete without explicit approval.**

3. **Starlite fallback templates are now in git.** `theme/templates/collection.json` and `theme/templates/page.json` are committed on this branch. They will appear as changes when merging to main — that's expected.

4. **The `diff` script uses character-count comparison, not semantic comparison.** For JSON templates, always verify with a parsed-object equality check (as done here) before treating a size difference as real drift. A future pre-stage reconciliation script should normalize Shopify's slash-escaping before comparing.

5. **No `theme_newer` files contained content the worktree was missing.** Every flag was a false positive. The worktree is authoritative for all 48 files.

---

*Report generated by Pre-Stage-3 reconciliation session — 2026-05-07*
