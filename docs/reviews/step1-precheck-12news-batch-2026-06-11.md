# Step 1 Pre-Publish CHECK — 12 News batch (READ-ONLY)

**Date:** 2026-06-11
**Mode:** READ-ONLY. No `articleUpdate`, no publish, no `--live`, no body/FAQ/SEO/image writes. Engine gates run DRY. The only write is this review record.
**Blog:** News (`108557861177`). **Author gate:** Steve Katz. **Source of truth:** `create-*` payload backups in `data/backups/articles/`.
**Out of scope (by instruction):** featured image and `image.alt` — Leo handles image, alt, and publishing. Not checked, not listed as blockers.

## Verdict table

| # | Slug | Article ID | Verdict |
|---|------|-----------|---------|
| 1 | poi-business-interiors-alternative-ontario | 689253155129 | **CONTENT-CLEAR** |
| 2 | the-office-shop-alternative-ontario | 689253220665 | **CONTENT-CLEAR** |
| 3 | staples-office-furniture-alternative-ontario | 689253482809 | **CONTENT-CLEAR** |
| 4 | grand-and-toy-office-furniture-alternative-ontario | 689253515577 | **CONTENT-CLEAR** |
| 5 | commercial-office-furniture-suppliers-ontario | 689253450041 | **CONTENT-CLEAR** |
| 6 | how-much-office-space-do-you-need | 689254334777 | **CONTENT-CLEAR** |
| 7 | hybrid-activity-based-work-office-design | 689254400313 | **CONTENT-CLEAR** |
| 8 | medical-dental-clinic-furniture-ontario | 689254498617 | **CONTENT-CLEAR** |

**Summary:** All 8 slugs are CONTENT-CLEAR. None require a fix before Leo's image + publish step. No slug from the not-eligible list appeared in this batch.

## Per-slug evidence

Authoritative source = independent Admin-API read of each live draft (not the write log). Engine gates run DRY via `.claude/skills/bbi-publish-post/scripts/faq_interlink_engine.py`.

| Slug | Published | Author | Words (≥2200) | Em-dashes | Literal "BBI" | `/blogs/news` `<a>` in body | OECM verbatim | validate-meta (title<60 / meta≤155) | check-handles | verify-faq byte-match |
|------|-----------|--------|---------------|-----------|---------------|------------------------------|----------------|--------------------------------------|---------------|------------------------|
| poi-business-interiors-alternative-ontario | false ✓ | Steve Katz ✓ | 2344 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 52 / 148 PASS | 6/6 → 200 | PASS (5 pairs) |
| the-office-shop-alternative-ontario | false ✓ | Steve Katz ✓ | 2260 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 37 / 155 PASS | 6/6 → 200 | PASS (5 pairs) |
| staples-office-furniture-alternative-ontario | false ✓ | Steve Katz ✓ | 2229 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 54 / 153 PASS | 6/6 → 200 | PASS (6 pairs) |
| grand-and-toy-office-furniture-alternative-ontario | false ✓ | Steve Katz ✓ | 2270 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 58 / 149 PASS | 6/6 → 200 | PASS (6 pairs) |
| commercial-office-furniture-suppliers-ontario | false ✓ | Steve Katz ✓ | 2513 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 52 / 154 PASS | 6/6 → 200 | PASS (6 pairs) |
| how-much-office-space-do-you-need | false ✓ | Steve Katz ✓ | 2540 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 47 / 146 PASS | 6/6 → 200 | PASS (6 pairs) |
| hybrid-activity-based-work-office-design | false ✓ | Steve Katz ✓ | 2531 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 44 / 138 PASS | 6/6 → 200 | PASS (6 pairs) |
| medical-dental-clinic-furniture-ontario | false ✓ | Steve Katz ✓ | 2264 ✓ | 0 ✓ | 0 ✓ | none ✓ | present, verbatim ✓ | 46 / 137 PASS | 6/6 → 200 | PASS (6 pairs) |

## Non-carried-brand review (resolved, not blockers)

The carried set is: Global, OTG, Teknion, Humanscale, Keilhauer, ergoCentric, Heartwood, ObusForme, Safco, FireKing, Office Star. The body scan flagged three brand strings; each was read in context and confirmed as a **competitor description**, not a claim that Brant Business Interiors carries the brand:

- **poi-business-interiors-alternative-ontario** — "Steelcase": POI is described as a "Steelcase Premier Partner" anchored to the Steelcase line. Competitor's product model, in a comparison post. Not a BBI carry claim.
- **commercial-office-furniture-suppliers-ontario** — "Steelcase": same — POI listed in a supplier table as a Steelcase Premier Partner. Not a BBI carry claim.
- **the-office-shop-alternative-ontario** — "Groupe Lacasse": listed among The Office Shop's *own* roster of partner brands (Global, Groupe Lacasse, Krug, Humanscale, National, Keilhauer, Workspace 48, Watson, Three H). Competitor's roster, not a BBI carry claim.

## Notes

- **Catalog interlinks are plain `<a>` to `/collections/`, `/products/`, and `/pages/` only.** Zero `<a href=".../blogs/news...">` in any body — D3 content-to-content links remain plain text / held, as required.
- **All internal links resolve 200** (catalog + page links checked, not just catalog interlinks).
- **`faq.items` byte-match PASS** on every article against current `body_html` (chips are markup only).
- Tightest word count is staples at 2229 (29 over the 2,200 floor); all others comfortably clear.

## Build-state row delta (NOT applied — read-only)

`BBI-Session-Kickoff/bbi-build-state.md` was **not** edited. For the publish session, these 8 drafts are Step-1 content-clear and ready for Leo's image + flip on their respective "Blog #N" rows. No row was written in this pass.
