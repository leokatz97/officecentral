# OG / Social Meta Audit — Sitewide

**Task:** OG-META-WIRE-UP-SITEWIDE (Phase A, Block 2, Session 2)
**Date:** 2026-05-30
**Branch:** `feature/og-meta-wire-up-sitewide-2026-05-30`
**PR:** #54
**Outcome:** No-op closure — coverage already 100% complete sitewide. No Liquid edit, no production PUT. Image-quality items logged as new Tier 2B follow-ups.

---

## TL;DR

The task brief anticipated **missing** `og:image` / `og:title` / `og:description` on pages without an obvious primary image, requiring a wire-up. **That gap does not exist.** Every page type already emits a complete, reachable set of Open Graph + Twitter Card tags. A literal "wire up missing tags" edit would have written **zero** new tags.

What remains is **image quality / relevance** (not presence), which mostly needs assets from Steve rather than Liquid edits. Those are logged as follow-ups, not actioned this session.

---

## Where the logic lives

All og/twitter logic is a single snippet — [`theme/snippets/meta-tags.liquid`](../../theme/snippets/meta-tags.liquid) — rendered once from `theme/layout/theme.liquid:11`.

**Drift check:** local `meta-tags.liquid` is **byte-identical** to production theme `186373570873` (role=main). No drift.

### What it emits

**Sitewide chrome (every page):** `og:site_name`, `og:url` (`canonical_url || request.origin`), `og:title`, `og:type`, `og:description`, `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, conditional `twitter:site`.

**`og:type` switching:** `index`/pages → `website`; product → `product`; article → `article`.

**`og:image` resolution:**
- `template == 'index'` → `og-preview.png` asset (1024×1024), with `:secure_url`, `:width`, `:height`.
- `elsif page_image` → product/article/collection featured image via `image_url`.
- *(no explicit else branch — and none is needed; see below)*

**Why every other page still gets an og:image:** Shopify's `page_image` global itself falls back to the **store's Social-sharing-image preference** (Online Store → Preferences) when a template has no specific image. That preference is currently **`IMG_2566.jpg` (1039×1184, portrait)**. So brand pages, OECM, industries, About, blog index, and image-less collections all still emit a complete og:image — the `elsif page_image` branch is truthy on them.

---

## Coverage table — live cache-busted curl, 10 representative URLs

| Page type | URL | og:title | og:desc | og:image | og:url | og:type | Image source (actual) |
|---|---|:---:|:---:|:---:|:---:|---|---|
| Homepage | `/` | ✅ | ✅ | ✅ | ✅ | website | `og-preview.png` 1024×1024 (square) |
| PDP | `/products/boardroom-table-rectangular-94-5x47-25` | ✅ | ✅ | ✅ | ✅ | product | product featured img 658×352 (small) |
| Collection | `/collections/seating` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default — no collection.image) |
| Brand | `/pages/brands-global-teknion` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default) |
| OECM | `/pages/oecm` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default) |
| Industries hub | `/pages/industries` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default) |
| Healthcare | `/pages/healthcare` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default) |
| Blog index | `/blogs/news` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default) |
| Blog article | `/blogs/news/oecm-ontario-school-boards-office-furniture` | ✅ | ✅ | ✅ | ✅ | article | article img Photo1.webp 1500×1099 ✅ |
| About | `/pages/about` | ✅ | ✅ | ✅ | ✅ | website | IMG_2566.jpg (store default) |

**og:image reachability:** all four distinct image URLs return **HTTP 200** (homepage og-preview.png, PDP product img, store-default IMG_2566.jpg, blog article Photo1.webp).

---

## What is actually weak (quality / relevance, not presence)

1. **🟡 Shared generic fallback image.** 6 of 10 page types (all landing/brand/static + image-less collections) share `IMG_2566.jpg`. It's **portrait 1039×1184** — wrong aspect ratio for `summary_large_image` cards (want ~1.91:1, 1200×630), so it letterboxes/crops awkwardly on LinkedIn/FB. → **OG-IMG-DEFAULT-LANDSCAPE** follow-up.
2. **🟡 PDP image is tiny** (658×352) — below the 1200px-wide social minimum; renders soft in cards. → data-side image-quality item (overlaps AI image pipeline Session 03).
3. **🟢 Homepage og-preview.png is square** (1024×1024) — renders OK but not ideal 1.91:1. → fold into OG-IMG-DEFAULT-LANDSCAPE.
4. **🟢 No `twitter:image` tag** anywhere — X falls back to og:image, so functionally fine. → **OG-TWITTER-IMAGE-EXPLICIT** (optional hardening).
5. **🟢 Per-segment OG images.** Landing/brand pages would benefit from topically-relevant per-segment OG images (healthcare/education/gov/brands) instead of a single generic default. → **OG-IMG-PER-SEGMENT** (needs Steve assets).

---

## New Tier 2B follow-ups logged

| ID | Description | Blocker |
|---|---|---|
| OG-IMG-DEFAULT-LANDSCAPE | Replace store social-share default (portrait 1039×1184) with explicit 1200×630 landscape OG default; fold homepage og-preview into same ratio | Needs 1200×630 asset (generate or crop) |
| OG-IMG-PER-SEGMENT | Per-segment topical OG images for landing/brand pages (healthcare/education/gov/non-profit/pro-services/brands) | Needs Steve assets |
| OG-TWITTER-IMAGE-EXPLICIT | Add explicit `twitter:image` mirroring og:image (optional — X already falls back) | None (low priority) |

---

## Manual external validation (Leo, post-session)

Coverage and reachability are verified server-side. Render-quality on the social platforms can only be confirmed by their own scrapers. Run these on the URLs in the coverage table at convenience:

- **LinkedIn Post Inspector:** https://www.linkedin.com/post-inspector/
- **FB Sharing Debugger:** https://developers.facebook.com/tools/debug/
- **Twitter/X Card Validator:** https://cards-dev.twitter.com/validator

Priority URLs (highest social-share value): `/`, `/pages/oecm`, the OECM blog article, `/pages/healthcare`, `/pages/brands-global-teknion`.

---

## Verification methodology note

No production write occurred this session, so the per-file PUT byte-snapshot / readback gate did not apply. The Admin-API readback **was** used as the audit gate to confirm zero drift on `meta-tags.liquid` (and to re-confirm PR #53's `bbi-homepage-schema` / `bbi-homepage-faq` merge state). Cache-busted curl was the supplementary live-render check.
