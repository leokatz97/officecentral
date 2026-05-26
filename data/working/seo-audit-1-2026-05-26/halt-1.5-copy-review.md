# HALT 1.5 — Phase 7.1 Copy + Decisions for Leo Review

**Scope probe (Phase 7.0) results:**

| Path | Status |
|---|:-:|
| `write_content` — page metafields | ✓ |
| `write_products` — collection metafields | ✓ |
| `metafieldsSet` — shop-owner metafields | ✓ |
| URL redirect POST+DELETE | ✓ |
| Page PUT (template_suffix) | ✓ |
| `shopUpdate` mutation | ✗ (removed in current Admin GraphQL) |
| REST `PUT /shop.json` description | ✗ (406) |

**No Steve handoff anywhere. Storefront-wide SEO writes go through theme.liquid override (FIX #3 + #4 + #5 collapse into a single `theme/snippets/meta-tags.liquid` edit).**

LIVE baseline post-probe: `2026-05-16T16:47:22-04:00` ✓ unchanged.

---

## FIX #5 + #3 + #4 — `theme/snippets/meta-tags.liquid` edit (1 file, 1 push)

`meta-tags.liquid` renders at theme.liquid:10 **before** `{{ content_for_header }}`, so our tags win for OG parsers.

**Diff plan** (current → proposed):

```diff
   {%- liquid
-    assign og_title = page_title | default: shop.name
+    if template == 'index'
+      assign og_title = 'Office Furniture for Canadian Businesses | Brant Business Interiors'
+    else
+      assign og_title = page_title | default: shop.name
+    endif
     assign og_url = canonical_url | default: request.origin
     assign og_type = 'website'
-    assign og_description = page_description | default: shop.description | default: shop.name
+    {%- comment -%} BBI-voice fallback replaces stale shop.description on pages w/o per-page SEO desc {%- endcomment -%}
+    assign bbi_default_desc = 'Commercial office furniture for Ontario businesses, schools, and institutions. ergoCentric · GFG · OTG · Heartwood · ObusForme. OECM Agreement 2025-470. Quote in 1 business day.'
+    if template == 'index'
+      assign og_description = 'Commercial office furniture for Ontario businesses, schools, and institutions. Global Furniture Group, OTG / Offices to Go, Heartwood Manufacturing. OECM Supplier Partner (Agreement 2025-470). Quote in 1 business day.'
+    else
+      assign og_description = page_description | default: bbi_default_desc
+    endif

     if request.page_type == 'product'
       assign og_type = 'product'
     elsif request.page_type == 'article'
       assign og_type = 'article'
     elsif request.page_type == 'password'
       assign og_url = request.origin
     endif
   %}

   <meta property="og:site_name" content="{{ shop.name }}">
   <meta property="og:url" content="{{ og_url }}">
   <meta property="og:title" content="{{ og_title | escape }}">
   <meta property="og:type" content="{{ og_type }}">
   <meta property="og:description" content="{{ og_description | escape }}">

-  {%- if page_image -%}
+  {%- if template == 'index' -%}
+    {%- assign hp_og = 'og-preview.png' | asset_url -%}
+    <meta property="og:image" content="{{ hp_og | replace: 'https:', 'http:' }}">
+    <meta property="og:image:secure_url" content="{{ hp_og }}">
+    <meta property="og:image:width" content="1200">
+    <meta property="og:image:height" content="630">
+  {%- elsif page_image -%}
     <meta property="og:image" content="http:{{ page_image | image_url }}">
     <meta property="og:image:secure_url" content="https:{{ page_image | image_url }}">
     <meta property="og:image:width" content="{{ page_image.width }}">
     <meta property="og:image:height" content="{{ page_image.height }}">
   {%- endif -%}
```

**Approve?** Y/N or edit

---

## FIX #2 + #8 — Per-page meta descriptions (29 writes)

Format: `current` → `proposed` (target 150–160 chars; OECM Agreement 2025-470 where contextually appropriate; brand-voice rules per memory `feedback_bbi_copy_voice.md`; private-sector tone for prof-services per CONTENT-POLISH-1 Session A; clinical-first tone for healthcare per `feedback_healthcare_tone.md`).

### Pages (17)

**1. `/pages/about`** _(current: empty)_
```
Brant Business Interiors is a Canadian-owned commercial office furniture dealer in Peterborough, Ontario. OECM Agreement 2025-470. Family-owned since 1964.
```
156 chars ✓

**2. `/pages/brands` (hub)** _(current: empty)_
```
Authorized Canadian dealer for ergoCentric, Global Furniture Group, OTG / Offices to Go, Heartwood, ObusForme, and Keilhauer. OECM Agreement 2025-470.
```
153 chars ✓

**3. `/pages/brands-ergocentric`** _(current: empty)_
```
Authorized ergoCentric dealer in Ontario. Canadian-engineered ergonomic seating, task chairs, and stools. OECM Agreement 2025-470. Quote in 1 business day.
```
156 chars ✓

**4. `/pages/brands-global-teknion`** _(current: empty — GFG-family scope per BRAND-PAGES-1)_
```
Authorized Global Furniture Group dealer in Ontario. Seating, desks, filing, and panels from Canada's largest contract furniture maker. OECM Agreement 2025-470.
```
161 chars (1 over — acceptable; can trim if needed)

**5. `/pages/brands-heartwood`** _(current: empty)_
```
Authorized Heartwood Manufacturing dealer in Ontario. Canadian-made veneer desks, casegoods, conference tables. OECM Agreement 2025-470. Quote in 1 business day.
```
161 chars (1 over — acceptable)

**6. `/pages/brands-keilhauer`** _(current: empty)_
```
Keilhauer seating and lounge furniture from a Canadian-owned Ontario dealer. Mid-to-high-end contract chairs. OECM Agreement 2025-470. Quote in 1 business day.
```
159 chars ✓

**7. `/pages/brands-obusforme`** _(current: empty)_
```
Authorized ObusForme dealer in Ontario. Canadian-made ergonomic seating with the original Obus-back support system. OECM Agreement 2025-470. Quote in 1 day.
```
156 chars ✓

**8. `/pages/brands-otg`** _(current: empty)_
```
Authorized OTG / Offices to Go dealer in Ontario. Canadian-made seating, desks, lounge, and accessories at workhorse price points. OECM Agreement 2025-470.
```
156 chars ✓

**9. `/pages/customer-stories`** _(current: empty)_
```
School boards, hospitals, and Ontario municipalities partnering with Brant Business Interiors. OECM Agreement 2025-470 case studies and verified installations.
```
160 chars ✓

**10. `/pages/delivery`** _(current: empty)_
```
Free in-house delivery and assembly across Ontario by Brant Business Interiors. After-hours and weekend installs can typically be arranged at quote time.
```
154 chars ✓

**11. `/pages/education`** _(current: empty)_
```
Office furniture for Ontario school boards, colleges, and independent schools. OECM Agreement 2025-470 — order without open tender. Summer-window installs.
```
156 chars ✓

**12. `/pages/government`** _(current: empty)_
```
Office furniture for Ontario municipal, provincial, and federal offices. OECM Agreement 2025-470 — order without open tender. Audit-trail PO billing.
```
150 chars ✓

**13. `/pages/non-profit`** _(current: empty)_
```
Office furniture for Ontario non-profits, family health teams, and community-services agencies. OECM Agreement 2025-470. Budget-friendly leads, NET 30 terms.
```
158 chars ✓

**14. `/pages/oecm`** ⭐ _(current: empty — strategic page)_
```
Brant Basics is a verified OECM Supplier Partner under Agreement 2025-470. Ontario broader-public-sector buyers can order office furniture without open tender.
```
160 chars ✓

**15. `/pages/our-work`** _(current: empty)_
```
Photos of recent Brant Business Interiors office furniture installs across Ontario — school boards, hospitals, municipalities, private boardrooms. OECM 2025-470.
```
162 chars (2 over — trim?)

Trimmed alt: `Recent Brant Business Interiors office furniture installs across Ontario — school boards, hospitals, municipalities, private boardrooms. OECM Agreement 2025-470.` (160)

**16. `/pages/professional-services`** _(current: empty — PRIVATE-SECTOR tone per CONTENT-POLISH-1 Session A; light on OECM)_
```
Office furniture for Ontario law firms, accounting practices, design studios, and medical/dental offices. ergoCentric, OTG, Heartwood. Canadian-owned since 1964.
```
162 chars (2 over — trim?)

Trimmed alt: `Office furniture for Ontario law firms, accountants, design studios, and medical/dental offices. ergoCentric, OTG, Heartwood. Canadian-owned since 1964.` (152)

**17. `/pages/quote`** _(current: empty, but renders 320-char auto-desc — FIX #8 here)_
```
Request a furniture quote from Brant Business Interiors. Most quotes back in 1 business day. OECM Agreement 2025-470. Phone 1-800-835-9565 for fast-track pricing.
```
161 chars (1 over — trim 'phone' label?)

Trimmed alt: `Request a furniture quote from Brant Business Interiors. Most quotes back in 1 business day. OECM Agreement 2025-470. 1-800-835-9565 for fast-track pricing.` (157)

**18. `/pages/relocation`** _(current: empty)_
```
Office relocation management across Ontario by Brant Business Interiors. Inventory, packing, install, and after-hours coordination from one Canadian-owned team.
```
160 chars ✓

### Collections (10 — covers FIX #2 plus the auto-filled col-business-furniture for SEO control)

**19. `/collections/business-furniture`** _(current: collection.description auto-fills 64 chars)_
```
Brant Business Interiors' full Ontario office furniture catalog — seating, desks, storage, tables, ergonomic, panels, accessories. OECM Agreement 2025-470.
```
156 chars ✓

**20. `/collections/seating`**
```
Task chairs, executive seating, lounge, stacking, and 24-hour chairs from ergoCentric, OTG, Keilhauer, ObusForme. OECM Agreement 2025-470. Quote in 1 day.
```
155 chars ✓

**21. `/collections/desks`**
```
Height-adjustable desks, L-shape, U-shape, benching, and reception desks from OTG and Heartwood. OECM Agreement 2025-470. Free CAD layout with every quote.
```
156 chars ✓

**22. `/collections/storage`**
```
Lateral files, vertical files, cabinets, bookcases, hutches, lockers, and fire-resistant safes for Ontario offices. OECM Agreement 2025-470. Ships across Canada.
```
163 chars (3 over — trim 'across Canada'?)

Trim: `Lateral files, vertical files, cabinets, bookcases, hutches, lockers, and fire-resistant safes for Ontario offices. OECM Agreement 2025-470. 1-day quote.` (153)

**23. `/collections/tables`**
```
Meeting, training, cafeteria, drafting, coffee, and bar-height tables from Canada's leading contract furniture brands. OECM Agreement 2025-470. 1-day quote.
```
157 chars ✓

**24. `/collections/boardroom`**
```
Boardroom tables, conference seating, lecterns, podiums, and AV-friendly furniture for Ontario offices. OECM Agreement 2025-470. Free CAD layout included.
```
155 chars ✓

**25. `/collections/accessories`**
```
Chairmats, monitor arms, power modules, keyboard trays, lighting, and ergonomic accessories for Ontario offices. OECM Agreement 2025-470. 1-day quote.
```
151 chars ✓

**26. `/collections/ergonomic-products`**
```
Height-adjustable tables, monitor arms, keyboard trays, and sit-stand desktop units. ergoCentric and ObusForme ergonomics. OECM Agreement 2025-470.
```
148 chars ✓

**27. `/collections/panels-room-dividers`**
```
Modular panel systems, desk-top dividers, and modesty panels from OTG and Global Furniture Group. OECM Agreement 2025-470. CAD floor plan with every quote.
```
156 chars ✓

**28. `/collections/quiet-spaces`**
```
Telephone booths, acoustic walls, sound dampeners, and AV-friendly furniture for Ontario open-plan offices. OECM Agreement 2025-470. Quote in 1 business day.
```
158 chars ✓

### Blog + Article (2)

**29. `/blogs/news` (hub)**
```
Office-furniture buying guides, OECM procurement how-tos, and Ontario workplace insights from Brant Business Interiors. Updated regularly. 1-800-835-9565.
```
155 chars ✓

**30. `/blogs/news/oecm-ontario-school-boards-office-furniture` (cornerstone — currently 324 chars auto)**
```
How Ontario school boards procure office furniture under OECM Agreement 2025-470 — eligibility, ordering, delivery, and lead-time guidance from Brant Business Interiors.
```
170 chars (10 over — trim?)

Trim: `How Ontario school boards procure office furniture under OECM Agreement 2025-470 — eligibility, ordering, delivery, and lead-time guidance from BBI.` (148)

But "BBI" is forbidden in customer copy per memory. Use:

Trim 2: `How Ontario school boards procure office furniture under OECM Agreement 2025-470 — eligibility, ordering, delivery, lead times. By Brant Business Interiors.` (160)

**Approve all 29 descriptions?** Y / specify edits per-page / "redraft with shorter form"

---

## FIX #7 — Title rewrites (32 pages — but 5 already have title_tag; 27 actually need rewrites)

Current → proposed (target 50–60 chars including the " | Brant Business Interiors" suffix; some pages drop the suffix when title alone is descriptive). PDP titles are auto-derived from `product.title | shop.name` — separate handling at the end.

Note: The 5 pages with existing title_tag (contact 63ch, design-services 69ch, faq 47ch, healthcare 125ch, industries 95ch) — healthcare + industries need trims; contact + design-services are 3–9 chars over (borderline). FAQ is fine.

### Pages needing new or trimmed title_tag (17 pages + 4 trims)

**Custom pages currently no title_tag (17 — Shopify auto-renders `{page.title} – {shop.name}`):**

| # | Page | Proposed title (≤60) | Chars |
|---|---|---|---:|
| 1 | /pages/about | `About Brant Business Interiors – Canadian-owned 1964` | 53 |
| 2 | /pages/brands | `Canadian Office Furniture Brands \| Brant Business Interiors` | 60 |
| 3 | /pages/brands-ergocentric | `ergoCentric Authorized Dealer Ontario \| Brant Business` | 54 |
| 4 | /pages/brands-global-teknion | `Global Furniture Group Dealer Ontario \| Brant Business` | 55 |
| 5 | /pages/brands-heartwood | `Heartwood Manufacturing Dealer Ontario \| Brant Business` | 56 |
| 6 | /pages/brands-keilhauer | `Keilhauer Seating Dealer Ontario \| Brant Business Interiors` | 60 |
| 7 | /pages/brands-obusforme | `ObusForme Authorized Dealer Ontario \| Brant Business` | 53 |
| 8 | /pages/brands-otg | `OTG / Offices to Go Dealer Ontario \| Brant Business` | 52 |
| 9 | /pages/customer-stories | `Office Furniture Customer Stories \| Brant Business Interiors` | 61 (drop article: `Office Furniture Customer Stories – Brant Business Interiors` = 60) |
| 10 | /pages/delivery | `Office Furniture Delivery & Installation Ontario \| Brant` | 56 |
| 11 | /pages/education | `Education Furniture Ontario – OECM Agreement 2025-470` | 53 |
| 12 | /pages/government | `Government Furniture Ontario – OECM Agreement 2025-470` | 54 |
| 13 | /pages/non-profit | `Non-Profit Office Furniture Ontario – OECM 2025-470` | 51 |
| 14 | /pages/oecm | `OECM Office Furniture Supplier – Agreement 2025-470` | 51 |
| 15 | /pages/our-work | `Office Furniture Projects Ontario \| Brant Business Interiors` | 61 (`Office Furniture Projects – Brant Business Interiors` = 53) |
| 16 | /pages/professional-services | `Professional Services Office Furniture Ontario \| Brant` | 54 |
| 17 | /pages/quote | `Request an Office Furniture Quote \| Brant Business Interiors` | 60 |
| 18 | /pages/relocation | `Office Relocation Services Ontario \| Brant Business Interiors` | 62 (`Office Relocation Services – Brant Business Interiors` = 54) |

**Trims for pages with existing oversized title_tag (4):**

| # | Page | Current (chars) | Proposed (≤60) | Chars |
|---|---|---|---|---:|
| 19 | /pages/contact | `Height Adjustable Workstations: Optimal Office Furniture Design` (63) | `Contact Brant Business Interiors – Peterborough HQ` | 50 |
| 20 | /pages/design-services | `Free Office Design Layout & Space Planning \| Brant Business Interiors` (69) | `Free Office Design & Space Planning \| Brant Business` | 52 |
| 21 | /pages/healthcare | `Healthcare & Clinical Office Furniture Ontario \| Brant Business Interiors — a division of Office Central Inc.` (125) | `Healthcare & Clinical Office Furniture Ontario \| Brant` | 54 |
| 22 | /pages/industries | `Ontario Institutional Furniture \| Healthcare, Education & Government \| Brant Business Interiors` (95) | `Ontario Institutional Office Furniture \| OECM Agreement 2025-470` | 64 (1 over) → `Ontario Institutional Furniture – OECM 2025-470 Supplier` (55) |

### Collections (10 — currently auto-rendered `{collection.title} – {shop.name}` which runs long)

| # | Collection | Current auto (chars) | Proposed (≤60) | Chars |
|---|---|---|---|---:|
| 23 | /collections/business-furniture | `Business Furniture – Office Central & Brant Business Interiors` (~63) | `Office Furniture Ontario \| Brant Business Interiors` | 51 |
| 24 | /collections/seating | `Seating – Office Central & Brant Business Interiors` (~52) | `Office Chairs & Seating Ontario \| Brant Business` | 49 |
| 25 | /collections/desks | `Desks & Workstations – Office Central & Brant Business Interiors` | `Office Desks & Workstations Ontario \| Brant Business` | 53 |
| 26 | /collections/storage | `Storage & Filing – Office Central & Brant Business Interiors` | `Office Storage & Filing Ontario \| Brant Business` | 49 |
| 27 | /collections/tables | `Tables – Office Central & Brant Business Interiors` | `Office Tables Ontario \| Brant Business Interiors` | 49 |
| 28 | /collections/boardroom | `Boardroom – Office Central & Brant Business Interiors` | `Boardroom Furniture Ontario \| Brant Business Interiors` | 54 |
| 29 | /collections/accessories | `Accessories – Office Central & Brant Business Interiors` | `Office Accessories Ontario \| Brant Business Interiors` | 53 |
| 30 | /collections/ergonomic-products | `Ergonomic Products – Office Central & Brant Business Interiors` | `Ergonomic Office Products Ontario \| Brant Business` | 51 |
| 31 | /collections/panels-room-dividers | `Panels & Room Dividers – Office Central & Brant Business Interiors` | `Panels & Room Dividers Ontario \| Brant Business` | 48 |
| 32 | /collections/quiet-spaces | `Quiet Spaces – Office Central & Brant Business Interiors` | `Quiet Spaces & Acoustic Pods \| Brant Business Interiors` | 56 |

### Blog + Article

| # | URL | Current | Proposed | Chars |
|---|---|---|---|---:|
| 33 | /blogs/news | `News – Office Central & Brant Business Interiors` | `Office Furniture News & Buying Guides \| Brant Business` | 55 |
| 34 | /blogs/news/oecm-… | `OECM for Ontario School Boards: How to Procure Office Furniture Under Agreement 2025-470` (133) | `OECM Office Furniture for Ontario School Boards (2025-470)` | 58 |

### PDP (1 — pattern, not per-product write — Hero PDP already has decent title)

| # | URL | Current title_tag | Action |
|---|---|---|---|
| 35 | /products/adapt-high-back-synchro-tilter-mvl11724 | `Adapt MVL11724 High Back Synchro-Tilter Chair` (45) | Keep — already 45 chars and product-named. No write needed. |

**Other Hero 100 products:** PE-4 already pushed SEO titles on 100 Hero products (per commit `a2118f3`). Sample/audit those post-launch as part of PE-5 work — out of scope for SEO-AUDIT-1 today. The PDP template's `<title>` for products WITHOUT title_tag would be Shopify auto-rendering `{product.title} – {shop.name}` which is long. **Sitewide PDP title trim is a Wave-E follow-up, not this audit.**

**Approve all title rewrites?** Y / specify edits / "drop suffix '| Brant Business Interiors' from all to save chars"

---

## FIX #1b — `data/llms-txt-draft.md` refresh (full rewrite for 7 stale items)

I'll show the literal proposed file content rather than a diff (it's a substantive rewrite). Will write to `data/llms-txt-draft.md` only — no push to /llms.txt because of FIX #1a constraint (see next section).

**Proposed updated `data/llms-txt-draft.md`:**

```markdown
# Brant Business Interiors

> Brant Business Interiors (BBI) is a Canadian-owned commercial office furniture
> dealer based in Peterborough, Ontario at 296 George St N, K9J 3H2. Part of the
> Office Central Group of Companies. Brant Basics is the OECM-registered entity
> under Agreement 2025-470 — Ontario broader-public-sector buyers can order
> without an open tender. We sell business furniture (seating, desks, storage,
> tables, ergonomic accessories, panels, quiet spaces) to Ontario institutional
> buyers — non-profits, family health teams, school boards, hospitals,
> municipalities, First Nations band offices — and to Ontario SMB private-sector
> offices in manufacturing, professional services, trades, and logistics.
> Catalog ships across Canada (Quebec excluded). Family-owned since 1964.
> Phone: 1-800-835-9565.

## What we sell

- [Shop Business Furniture](https://www.brantbusinessinteriors.com/collections/business-furniture) — Full catalog of commercial-grade office furniture; primary entry point.
- [Seating](https://www.brantbusinessinteriors.com/collections/seating) — Task chairs, executive chairs, mesh, leather, lounge, stacking, 24-hour, big-and-heavy.
- [Desks & Workstations](https://www.brantbusinessinteriors.com/collections/desks) — L-shape, U-shape, height-adjustable, benching, multi-person workstations, reception desks.
- [Storage & Filing](https://www.brantbusinessinteriors.com/collections/storage) — Lateral files, vertical files, cabinets, bookcases, hutches, lockers, fire-resistant safes.
- [Tables](https://www.brantbusinessinteriors.com/collections/tables) — Meeting, training, cafeteria, coffee, drafting, end, bar-height, folding.
- [Boardroom](https://www.brantbusinessinteriors.com/collections/boardroom) — Conference tables, lecterns, podiums, audio-visual furniture.
- [Ergonomic Products](https://www.brantbusinessinteriors.com/collections/ergonomic-products) — Height-adjustable tables, monitor arms, keyboard trays, desktop sit-stand units.
- [Panels & Room Dividers](https://www.brantbusinessinteriors.com/collections/panels-room-dividers) — Room dividers, desk-top dividers, modesty panels.
- [Accessories](https://www.brantbusinessinteriors.com/collections/accessories) — Chairmats, power modules, coat racks, lighting.
- [Quiet Spaces](https://www.brantbusinessinteriors.com/collections/quiet-spaces) — Telephone booths, walls, sound dampeners, AV stands, planters.

## Who we serve (industry pages)

- [Healthcare](https://www.brantbusinessinteriors.com/pages/healthcare) — Furniture for clinics, family health teams, small hospitals, long-term care, dental/medical offices. Waiting room seating, exam-room seating, reception desks, recliners, bariatric seating, storage.
- [Education](https://www.brantbusinessinteriors.com/pages/education) — Furniture for school boards, independent schools, post-secondary, and training spaces. Stack chairs, training tables, storage, panels, room dividers.
- [Government](https://www.brantbusinessinteriors.com/pages/government) — Furniture for federal, provincial, and municipal offices. Desks, storage, panels, secure filing.
- [Non-Profit](https://www.brantbusinessinteriors.com/pages/non-profit) — Furniture for community-services agencies, social-services non-profits, religious organizations, and First Nations band offices. Seating and tables that work in a busy community space.
- [Professional Services](https://www.brantbusinessinteriors.com/pages/professional-services) — Furniture for law, accounting, insurance, design, and medical/dental offices. Executive seating, reception desks, boardroom tables, client-facing finishes.

## Trust & procurement

- [OECM Procurement](https://www.brantbusinessinteriors.com/pages/oecm) — Brant Basics is a verified OECM Supplier Partner under **Agreement 2025-470**. Ontario broader-public-sector buyers (school boards, hospitals, municipalities, colleges, universities, social-services agencies) can purchase from us under this agreement without running a separate open tender. This is Brant Business Interiors' biggest procurement differentiator and is not held by most Ontario furniture dealers.
- [About Us](https://www.brantbusinessinteriors.com/pages/about) — Canadian-owned, family-owned since 1964, 296 George St N Peterborough HQ.
- [Free Design Services](https://www.brantbusinessinteriors.com/pages/design-services) — Free CAD floor plans + furniture-placement renderings.
- [Delivery & Installation](https://www.brantbusinessinteriors.com/pages/delivery) — In-house Ontario delivery + installation; after-hours arrangements available.
- [Office Relocation](https://www.brantbusinessinteriors.com/pages/relocation) — Inventory, packing, install, and after-hours coordination.
- [Customer Stories](https://www.brantbusinessinteriors.com/pages/customer-stories) — Verified case studies from Ontario school boards, hospitals, and municipalities.
- [Our Work](https://www.brantbusinessinteriors.com/pages/our-work) — Photo gallery of recent installs across Ontario.
- [Contact](https://www.brantbusinessinteriors.com/pages/contact) — Peterborough HQ; phone 1-800-835-9565.
- [FAQ](https://www.brantbusinessinteriors.com/pages/faq) — Ordering, OECM procurement, NET 30 terms, Ontario delivery, returns, design services.
- [Request a Quote](https://www.brantbusinessinteriors.com/pages/quote) — For project buys, multi-desk fit-outs, multi-unit pricing, and OECM orders. Quotes in 1 business day. Phone: 1-800-835-9565.
- [Resources & News](https://www.brantbusinessinteriors.com/blogs/news) — Buying guides, industry insights, procurement how-tos.
- [OECM for Ontario School Boards (Agreement 2025-470) — cornerstone post](https://www.brantbusinessinteriors.com/blogs/news/oecm-ontario-school-boards-office-furniture)
- [Homepage](https://www.brantbusinessinteriors.com/)

## Brand sub-pages (authorized dealer)

- [Brands hub](https://www.brantbusinessinteriors.com/pages/brands)
- [ergoCentric](https://www.brantbusinessinteriors.com/pages/brands-ergocentric) — Canadian-engineered ergonomic seating (Mississauga, ON)
- [Global Furniture Group (GFG)](https://www.brantbusinessinteriors.com/pages/brands-global-teknion) — Toronto-HQ contract furniture; the anchor line
- [Heartwood Manufacturing](https://www.brantbusinessinteriors.com/pages/brands-heartwood) — Canadian-made veneer desks and casegoods
- [Keilhauer](https://www.brantbusinessinteriors.com/pages/brands-keilhauer) — Mid-to-high-end Canadian seating (Toronto)
- [ObusForme](https://www.brantbusinessinteriors.com/pages/brands-obusforme) — Canadian ergonomic-support seating
- [OTG / Offices to Go](https://www.brantbusinessinteriors.com/pages/brands-otg) — Canadian workhorse-priced seating + casegoods

## Key entity facts

- **Legal name:** Brant Business Interiors, part of the Office Central Group of Companies. Brant Basics is the OECM-registered entity.
- **Location:** 296 George St N, Peterborough ON K9J 3H2, Canada
- **Phone:** 1-800-835-9565
- **OECM status:** Verified Supplier Partner under **Agreement 2025-470** — Ontario broader-public-sector buyers can order without open tender
- **Canadian-owned:** Yes, fully Canadian-owned and operated; family-owned since 1964
- **Area served (primary):** Ontario — Peterborough, Kawartha Lakes, Northumberland, GTA, Toronto, Mississauga, Markham, Richmond Hill, Barrie, North Bay, London, Ottawa
- **Area served (secondary):** Rest of Canada excluding Quebec — BC, Alberta, Manitoba, Saskatchewan, Atlantic provinces, territories
- **Quebec:** Out of scope (language and freight/install logistics)
- **Buyer types served:** Ontario institutional / non-profit (primary, ~60% of online revenue); Ontario SMB private sector (secondary, ~40%); rest-of-Canada institutional + SMB (sub-ICP, SEO upside)
- **Typical order size:** $500–$15,000 online; multi-desk fit-outs above that move to the quote channel
- **Languages:** English (Canadian)

## Canadian brands we carry

Lead authorized lines (in order of catalog depth):

- **Global Furniture Group (GFG)** — Toronto-HQ; the parent of the Business Interiors contract line that anchors the catalog. Seating, desks, filing, panels.
- **OTG / Offices to Go** — Canadian; workhorse-priced seating, casegoods, lounge, accessories.
- **Heartwood Manufacturing** — Canadian-made veneer desks, casegoods, conference tables.
- **ObusForme** — Canadian; ergonomic-support seating with the proprietary back-support system.
- **ergoCentric** — Mississauga, Ontario; Canadian-engineered ergonomic seating.

Available on request (not primary leads):

- **Keilhauer** — Toronto; mid-to-high-end seating, lounge, and contract seating.
- **Teknion** — Toronto; workstations, seating, architectural walls.
- Plus 25+ additional authorized accessory lines (lighting, power modules, panels, AV).

## What's not on this site

- Home-office / WFH consumer product (no consumer price points; commercial-grade only)
- Gaming / streaming chairs
- French-language pages (Quebec out of scope)
- US-only or Mexico-only fulfilment

## Contact

- **Phone:** 1-800-835-9565
- **HQ:** 296 George St N, Peterborough ON K9J 3H2
- **Quote requests:** [/pages/quote](https://www.brantbusinessinteriors.com/pages/quote)
- **Website:** [https://www.brantbusinessinteriors.com](https://www.brantbusinessinteriors.com)

---

*This file is `llms.txt`-style guidance for large-language-model crawlers
(GPTBot, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, Google-Extended) so
they can orient on Brant Business Interiors quickly without crawling the
entire catalog. Last updated: 2026-05-26.*
```

**Approve refresh?** Y / specify edits / "drop the Office Central Group of Companies framing — use Brant Basics only"

---

## FIX #1a — llms.txt deployment path investigation

**Findings from inspection:**

1. **Current `/llms.txt` on LIVE** is served by Shopify with header `server-timing: pageType=llms_txt` — this is Shopify's **new built-in auto-generated agent instructions** (UCP / Shop Pay / MCP discovery boilerplate). Body has 0 BBI-specific content.
2. **AI-1 (commit `a2118f3`) deployed `/pages/llms-txt` as a Shopify Page + URL redirect** — that still exists in Admin (the page is published) but Shopify's auto-pageType *takes precedence over* the redirect for /llms.txt.
3. **Shopify allows `templates/robots.txt.liquid` override** for robots.txt. The analogous `templates/llms.txt.liquid` is NOT documented as supported by Shopify yet. Shopify Help docs (Online Store → Preferences → AI features) mention `llms.txt` but only as auto-generated. No theme-template hook available as of this audit.
4. **No Shopify Admin → Preferences toggle** exists to inject custom content into the auto-generated llms.txt.

**Implication:** there's currently **no deployment path** for BBI-specific llms.txt content in the standard Shopify surface. The refreshed `data/llms-txt-draft.md` (FIX #1b above) is ready as soon as Shopify ships a hook OR Leo opens a Shopify support ticket asking for custom-content injection on `/llms.txt`.

**Recommendation:** Refresh the draft (FIX #1b — saves the file, no push). Log FIX #1a as **WAIVE — post-launch backlog**, monitor Shopify changelog for `llms.txt.liquid` support.

**Approve recommendation?** Y / "open Shopify support ticket as part of this batch" / "try templates/llms.txt.liquid override anyway and see if Shopify honors it"

---

## FIX #9 — `/pages/ergocentric` redirect (auto-apply)

```
POST /admin/api/2026-04/redirects.json
{ "redirect": { "path": "/pages/ergocentric", "target": "/pages/brands-ergocentric" } }
```

Plus optional: unpublish `/pages/ergocentric` so it no longer renders (currently published with empty BBI chrome). Without unpublish, the redirect catches storefront hits but the page still appears in sitemaps and the admin.

**Recommendation:** Apply redirect + unpublish (`PUT /pages/{id}.json { page: { published: false } }`).

**Approve?** Y / "redirect only — leave published" / N

---

## FIX #10 — `/pages/how-to-adjust-my-new-chair` (decision needed)

Currently: empty `page` template suffix → falls back to default page.json → BBI chrome renders but H1=0 (template never sets one), no meta-desc. Published as a Shopify Page with content (visual guides, animations — per the existing og:description "Visual Guides Seating Operating Mechanism Animations Video…").

**Options:**

**(a) Redirect to `/pages/brands-ergocentric`** _(default)_
- ✓ Fast (5 min API)
- ✓ The brands-ergocentric BBI section is the natural home for ergonomic chair guidance
- ✗ Loses the existing visual guides + videos in the page body
- ✗ Breaks any inbound links from search results / customer emails referencing the old URL → 301 preserves SEO juice

**(b) Rebuild as `ds-lp-howto-chair.liquid`** _(Wave-E-style proper integration)_
- ✓ Keeps the visual guides + brings them into the BBI design system
- ✓ Adds proper H1, meta-desc, JSON-LD (HowTo schema would be high-value AEO content)
- ✗ +30–60 min of section build + template wire-up + content migration
- ✗ Outside today's launch scope; better as a separate post-launch task

**(c) Unpublish** _(retire the page)_
- ✓ Cleanest if the page has no traffic
- ✗ Loses any inbound SEO value if Google indexed it
- Worth checking: does Search Console show clicks on this URL? (Don't have access from Claude Code without Search Console OAuth.)

**My recommendation: (a) redirect now, log (b) rebuild as post-launch backlog.** The visual-guide content can be migrated into the ergoCentric brand sub-page later; the URL preserves SEO juice via 301. (c) is acceptable if Leo confirms no traffic.

**Choose:** `a` / `b` / `c` / "redirect to a different target like /pages/faq"

---

## FIX #6 + #11–#15 — Lower-priority FIXes (status + recommendation)

| # | Finding | Recommendation |
|---|---|---|
| #6 | og:site_name "Office Central & Brant Business Interiors" — long but matches header co-brand wordmark | **Keep as-is.** No write. |
| #11 | PDP Lighthouse Performance 81 / 7.81 MB byte weight (avisplus.io reviews + image weights) | **Defer post-launch.** Image-weight optimization touches every Hero PDP and risks regressing SPEC-CANARY work. Schedule a separate PDP-PERF-1 session. |
| #12 | PDP LCP 2585ms (target ≤2500ms, 85ms over) | **Defer post-launch.** Same root cause as #11. Marginal. |
| #13 | PDP A11y 0.85 (vs 0.92 sitewide) | **Defer post-launch.** Likely missing form labels / button-name attrs on variant pickers. Schedule PDP-A11Y-1 (~30 min). |
| #14 | Best Practices 0.73 flat sitewide | **Defer post-launch.** Likely deprecated 3rd-party API. Investigate during post-LAUNCH-1 health check. |
| #15 | Brand sub-pages alt coverage 66.7% (2/6 images missing alt) | **Could absorb into Phase 7.2** — fast theme edit to the 6 `ds-lp-brands-*.liquid` sections to add alts. ~10 min. **Recommend include.** |

**Approve recommendations?** Y or specify which to include / defer

---

## CONSOLIDATED APPROVAL OPTIONS

Type one of:

- **`approve all, FIX #10 = a`** — fire Phase 7.2 with everything as drafted, /pages/how-to-adjust → /pages/brands-ergocentric redirect, FIX #15 included, FIX #1a logged as WAIVE
- **`approve all, FIX #10 = b`** — same but rebuild the howto page (adds ~45 min to Phase 7.2)
- **`approve all, FIX #10 = c`** — same but unpublish the howto page
- **`approve except {N}`** — fire all except specified items
- **`edits: <inline edits>`** — apply your inline copy edits, then fire
- **`show diffs for FIX #7`** — display literal before/after for all 32 title rewrites in a tighter table before approving
- **`redraft FIX #2`** — different voice on the meta descriptions (e.g. "more conversational" / "drop OECM from every one")
- **`stop`** — halt without writes
