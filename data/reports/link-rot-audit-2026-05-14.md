# LINK-ROT-1 Audit
_2026-05-14 · Read-only audit · Step ~30._

## Summary
- Templates scanned: 43 files
- Internal link occurrences found: 305 (94 unique URLs)
- HEALTHY: 93 unique URLs (304 occurrences)
- DEAD-WITH-REDIRECT: 0 unique URLs (0 occurrences)
- DEAD-NO-REDIRECT: 1 unique URLs (1 occurrences) ⚠️ ACTION REQUIRED
- DEAD-EXTERNAL-DEP: 0 unique URLs
- REVIEW: 0 unique URLs

**Overall verdict: Almost entirely clean.** The 164-collection unpublish + redirect CSV from COLLECTION-CLEANUP-APPLY left no dangling theme links — all sub-collections, category pages, brand pages, and landing pages resolve. One dead link found: `/collections/other` (intentionally unpublished archive collection, no redirect, referenced once in PDP breadcrumb fallback).

## DEAD-NO-REDIRECT links (action required)

| Source file | Line | Target | Context | Suggested fix |
|---|---|---|---|---|
| theme/sections/ds-pdp-base.liquid | 422 | `/collections/other` | <a href="/collections/other">Other</a> | Remove link or redirect; /collections/other intentionally unpublished as archive |

### Detail: /collections/other

`/collections/other` is the archive collection created in PE-PASS-2 (id=527013085497) to hold 337 archived/moved products. It was intentionally **unpublished** in COLLECTION-CLEANUP-APPLY (commit 737f6f6) — correct behaviour, as customers should not browse the archive.

**The problem:** `theme/sections/ds-pdp-base.liquid:422` renders a "Other" breadcrumb link to `/collections/other` as a fallback when a product has no recognized category tag. If a customer reaches a product whose breadcrumb resolves to this path and clicks it, they hit a 404.

**Scope:** Only products currently in the `other` collection (337 archived items, all moved from nav) would show this breadcrumb. Since those products are not front-of-site (not in nav, no smart-collection membership), real user exposure is very low — but not zero (direct URL visits, Google-indexed legacy PDPs).

**Suggested fix (two options):**
1. **Remove the breadcrumb link** for the "Other" fallback — render the text "Other" without an `<a>` tag (`ds-pdp-base.liquid:422`). Zero-effort, prevents 404.
2. **Redirect `/collections/other` → `/collections/all`** — add to `data/url-redirects-bulk.csv` and import in Shopify Admin. Breadcrumb link still shows but lands on a working page.

Recommendation: **Option 1** (remove the `<a>` tag) since `/collections/other` is intentionally hidden and "Browse all archived items" is not a useful nav destination for any customer.

## DEAD-WITH-REDIRECT links (optimize when convenient)

_None._

## DEAD-EXTERNAL-DEP links (track for future)

_None._

## REVIEW links (manual decision needed)

_None._

## Dynamic Liquid links (not scanned — for reference)

The following link patterns are dynamically generated via Liquid and were not verified (correct by construction):

- `theme/sections/ds-cs-base.liquid:318` — `href="/collections/{{ parent_handle }}"` — resolves to the parent category collection; always a KEEP collection per interlinking map
- `theme/sections/ds-cs-base.liquid:547` — same `{{ parent_handle }}` pattern in empty-state message
- `theme/sections/ds-pdp-base.liquid:420` — `href="/collections/{{ cat_handle }}"` — resolves to the product's type-tag category; any product in a live collection will resolve correctly
- `theme/snippets/product-form-buttons.liquid:31` — `href="/pages/contact?subject=..."` — query-string variant of `/pages/contact` (verified HEALTHY)
- `theme/snippets/social-sharing-icons.liquid:9,23,37,50` — external sharing URLs (Facebook, Twitter/X, Pinterest, LinkedIn) — excluded from scope

## Recommended next action

### DEAD-NO-REDIRECT (1 URL, 1 occurrence) — fix before launch

**`ds-pdp-base.liquid:422`** — remove `<a href="/collections/other">` wrapper from the "Other" fallback breadcrumb. Change:
```liquid
<a href="/collections/other">Other</a>
```
to:
```html
<span>Other</span>
```
This is a 1-line fix. Commit as `fix: remove dead /collections/other breadcrumb link on PDP`.

### DEAD-WITH-REDIRECT — none found
The 164-redirect CSV from COLLECTION-CLEANUP-APPLY covered all collection renames cleanly. No template links were left pointing at redirect-covered dead collections.

### DEAD-EXTERNAL-DEP — none found
No links to future planned pages (e.g. planned BRAND-PAGES-1 deliverables) found in current theme.

### Overall
The theme is in excellent link health. This audit clears the LINK-ROT-1 gate for Wave E pre-launch hardening. The one actionable fix is a single-line change.
