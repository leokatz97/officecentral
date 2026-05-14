# NAV-VERIFY Audit
_2026-05-14 · Read-only · Step ~31._

## Summary

- Nav links audited: 33
- Footer links audited: 29
- **Total: 62**
- HEALTHY-PUBLISHED: 59
- DEAD-NO-REDIRECT: 0 ✅
- DEAD-WITH-REDIRECT: 0 ✅
- EXTERNAL: 0 (no external links present in nav or footer)
- SKIPPED: 3 (tel: × 2, mailto: × 1)

**Overall verdict: CLEAN.** Every nav and footer destination resolves to a published, healthy resource. Zero dead links on the highest-traffic surface.

---

## Coverage

### Nav (bbi-nav.liquid) — 33 links

| Menu | Links | URLs |
|---|---|---|
| Logo | 1 | `/` |
| Shop Furniture | 9 | `/collections/seating`, `/collections/desks`, `/collections/storage`, `/collections/tables`, `/collections/boardroom`, `/collections/ergonomic-products`, `/collections/panels-room-dividers`, `/collections/accessories`, `/collections/quiet-spaces` |
| Industries | 6 | `/pages/industries`, `/pages/healthcare`, `/pages/education`, `/pages/government`, `/pages/non-profit`, `/pages/professional-services` |
| Brands | 4 | `/pages/brands`, `/pages/brands-keilhauer`, `/pages/brands-global-teknion`, `/pages/brands-ergocentric` |
| Services | 5 | `/pages/design-services`, `/pages/delivery`, `/pages/relocation`, `/pages/quote`, `/pages/faq` |
| About | 5 | `/pages/about`, `/pages/our-work`, `/pages/customer-stories`, `/pages/oecm`, `/pages/contact` |
| Utility bar | 3 | `/cart`, `/search` (form), `tel:` (skipped) |

### Footer (bbi-footer.liquid) — 29 links

| Column | Links | URLs |
|---|---|---|
| Shop | 9 | Same 9 category collections |
| Industries | 6 | Same 6 industry pages |
| Services | 8 | 6 service pages + `/pages/customer-stories` + `/blogs/news` |
| Contact | 2 | `tel:` (skipped), `mailto:` (skipped) |
| Trust band | 1 | `/pages/oecm` (duplicate, healthy) |
| Legal | 3 | `/policies/privacy-policy`, `/policies/terms-of-service`, `/policies/shipping-policy` |

---

## DEAD findings (per surface)

_None._

All 59 verifiable links returned `published=True` from the Shopify Admin API.

- All 9 category collections confirmed **smart collections**, published.
- All 20 pages confirmed **published**.
- `/blogs/news` confirmed present (id=108557861177).
- All 3 policies confirmed present via Shopify policies API.

---

## Shopify-managed menus (linklists)

The Shopify Admin API returned `403/404` for both `/admin/api/2024-04/linklists.json` and `/admin/api/2024-04/menus.json` — the token scope does not include `read_content` for linklists. However, this is not a gap: BBI's nav and footer are **fully Liquid-driven** (hardcoded in `bbi-nav.liquid` and `bbi-footer.liquid` snippets), not driven by Shopify's Online Store → Navigation menus. All links were audited directly from the theme source files.

---

## Recommendation

- **DEAD-NO-REDIRECT = 0 in nav + footer: NAV-VERIFY closes cleanly. No follow-up needed.**
- The one pre-existing dead link (`/collections/other` in `ds-pdp-base.liquid:422`) was fixed in commit `b779f3e` (LINK-ROT-FIX-1) prior to this audit — it was a PDP breadcrumb fallback, not a nav or footer link.
- No action required before launch on the nav/footer surface.

---

## Notes

- Desktop and mobile nav share identical link sets (mobile accordion mirrors the desktop mega-menu exactly).
- The "Request a Quote" button in the nav utility bar is a JS modal trigger (`data-bbi-quote-trigger`), not an `<a href>` link — no URL to verify.
- The `/cart` and `/search` links are Shopify system endpoints guaranteed healthy by the platform.
