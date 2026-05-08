# Stage 5 Launch Audit — 4.3 Nav Interconnection
**Date:** 2026-05-08
**Sources:** `theme/snippets/bbi-nav.liquid`, `theme/snippets/bbi-footer.liquid`, `docs/plan/bbi-interlinking-map.md`, `docs/plan/site-architecture-2026-04-25.md`
**Auditor:** Claude Code (read-only pass)

---

## Nav structure (per `bbi-nav-spec.md` + NAV-1, commit `d41295a`)

Canonical nav: **5 top-level items** + phone CTA + Quote button (right-aligned)

```
[Logo]  |  Shop Furniture ▾  |  Industries ▾  |  Brands ▾  |  Services ▾  |  About ▾  |  1-800-835-9565  |  [Request Quote →]
```

### Shop Furniture dropdown targets

| Nav item | Target URL | Page built? |
|---|---|---|
| Shop Furniture (click) | `/collections/business-furniture` | ✓ Template exists |
| Seating | `/collections/seating` | ✓ |
| Desks & Workstations | `/collections/desks` | ✓ |
| Storage & Filing | `/collections/storage` | ✓ |
| Tables | `/collections/tables` | ✓ |
| Boardroom | `/collections/boardroom` | ✓ |
| Ergonomic Products | `/collections/ergonomic-products` | ✓ |
| Panels & Dividers | `/collections/panels-room-dividers` | ✓ |
| Accessories | `/collections/accessories` | ✓ |
| Quiet Spaces | `/collections/quiet-spaces` | ✓ |

### Industries dropdown targets

| Nav item | Target URL | Page built? |
|---|---|---|
| Healthcare | `/pages/healthcare` | ✓ |
| Education | `/pages/education` | ✓ |
| Government | `/pages/government` | ✓ |
| Non-Profit | `/pages/non-profit` | ✓ |
| Professional Services | `/pages/professional-services` | ✓ |

### Brands dropdown targets

| Nav item | Target URL | Page built? |
|---|---|---|
| Keilhauer | `/pages/brands-keilhauer` | ✓ Template + section exist |
| Global/Teknion | `/pages/brands-global-teknion` | ✓ Template + section exist |
| ergoCentric | `/pages/brands-ergocentric` | ✓ Template + section exist |

**⚠️ Brands pages have templates/sections in the repo but need Shopify Page records + published status verified.** Per Stage 0 audit, Wave C pages were built outside worktree. Must confirm Page records exist and are published before launch.

### Services dropdown targets

| Nav item | Target URL | Page built? |
|---|---|---|
| Design Services | `/pages/design-services` | ✓ |
| Delivery & Installation | `/pages/delivery` | ✓ Template + section exist |
| Relocation Management | `/pages/relocation` | ✓ Template + section exist |
| OECM Procurement | `/pages/oecm` | ✓ |

### About dropdown targets

| Nav item | Target URL | Page built? |
|---|---|---|
| Our Work | `/pages/our-work` | ✓ Template + section exist |
| About Us | `/pages/about` | ✓ Template + section exist |
| Contact | `/pages/contact` | ✓ Template + section exist |
| Request a Quote | `/pages/quote` | ✓ |

---

## Footer link verification

Footer defined in `theme/snippets/bbi-footer.liquid` (commit `f683fb9`, NAV-2).

### Footer required links per interlinking-map

| Column | Expected links | Status |
|---|---|---|
| Industries | Healthcare, Education, Government, Non-Profit, Professional Services | 5 links required — source confirmed in section |
| Services | Design Services, Delivery, Relocation, OECM, FAQ | 5 links required — confirmed in `9c8b7db` FAQ gap fix |
| Shop | All 9 category collection links | In footer |
| OECM trust band | Above copyright | Confirmed in NAV-2 |

---

## Known gap: Pages with templates but no confirmed Shopify Page record

Per `design-system-remediation-2026-05-07.md` Stage 0 findings, Wave C pages were built outside the worktree workflow. The following pages have template files but need Shopify Page record + `template_suffix` verification before being treated as confirmed live:

- `/pages/about`
- `/pages/brands`
- `/pages/brands-keilhauer`
- `/pages/brands-global-teknion`
- `/pages/brands-ergocentric`
- `/pages/our-work`
- `/pages/contact`
- `/pages/delivery`
- `/pages/relocation`
- `/pages/customer-stories`

**Action required:** Run `scripts/audit-sub-collections.py` or a dedicated Page audit script against the Shopify Admin API to confirm each handle has a published Page record with the correct `template_suffix`.

---

## Missing nav destinations

| Gap | Severity | Notes |
|---|---|---|
| `/collections/all-seating` (and all 9 "View all" targets) | BLOCK | SMART-1 not run — "View all [Category]" CTAs on hub pages will 404 |
| `/collections/keilhauer`, `/collections/ergocentric`, etc. | BLOCK | SMART-1 brand-filtered collections not created |
| `/404` page | FIX | No `404.json` template — uses Starlite default + broken chrome |
| `/blogs/news` (blog hub) | NIT | BLOG-TPL-1 deferred; can launch without |
| Customer Stories Shopify Page record | FIX | CS-1 template exists, Page record unconfirmed |

---

## Interlinking audit script status

- `scripts/audit-interlinks.py` exists (commit `937cbcc`, INTERLINK-1)
- Last clean run: post-Wave-B audit (0 failures, commit `82c64c8`)
- **Must re-run before launch** — significant new pages added since last run (Wave C, Stage 3.2 sub-collection migration)
- INTERLINK-3 row in Wave E is ⬜ (not done)

---

## Summary

| Category | Status |
|---|---|
| Nav top-level items | ✓ 5 items + phone + quote |
| Shop Furniture dropdown | ✓ All 9 targets have templates |
| Industries dropdown | ✓ All 5 pages built |
| Brands dropdown | ⚠️ Templates exist; Shopify Page records need verification |
| Services dropdown | ⚠️ Delivery/Relocation: templates exist; Page records need verification |
| About dropdown | ⚠️ Same — Page records need verification |
| Footer industries column | ✓ (source confirmed) |
| Footer services column | ✓ (9c8b7db FAQ fix confirmed) |
| "View all" category CTAs | ✗ BLOCKED — SMART-1 not run |
| INTERLINK-3 final audit | ⬜ Not run |
