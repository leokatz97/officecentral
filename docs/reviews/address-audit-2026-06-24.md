# BBI Company NAP (Name / Address / Phone / Contact) Relocation Audit

**Date:** 2026-06-24
**Branch:** `audit/address-inventory-2026-06-24`
**Type:** READ-ONLY inventory pass (Pass 1 repo grep + Pass 2 Shopify Admin/MCP reads). **Zero mutations made.** No theme writes, no Admin/content writes, no `shopify theme dev`, no redirects. The only file written this session is this report.
**Purpose:** Exhaustive inventory of every place the company NAP appears, across the theme repo AND the live Shopify store, to scope a future relocation address change. **This is the audit only — no edits proposed or staged.**

---

## Current NAP being hunted (the values that may relocate)

| Element | Current value | Notes |
|---|---|---|
| Street | `296 George St N` | also "George St N", "George Street North" |
| City / region / postal | `Peterborough, ON K9J 3H2` | postal variants `K9J 3H2`, `K9J3H2`, `K9J` |
| Phone (storefront) | `1-800-835-9565` | toll-free; variants `tel:18008359565`, `+1-800-835-9565`, `1&#8209;800&#8209;835&#8209;9565` |
| Phone (Admin/back-office) | `416-845-8636` (shop + Peterborough location), `905-887-7700` (Toronto location) | **NEW — discovered in Admin; these are NOT the storefront toll-free** |
| Email | `info@brantbusinessinteriors.com` | **+ two more variants found:** `quotes@brantbusinessinteriors.com`, `sales@brantbusinessinteriors.com`; Admin `contactEmail` = `steve@brantbusinessinteriors.com` |
| Founding | `since 1964` / `foundingDate 1964` | colocated NAP copy — logged so it isn't missed; JUDGMENT |

> ⚠️ **Stale residuals found:** `Brantford` (2 surfaces) and a Toronto **`60 Leek Crescent, Richmond Hill`** warehouse location — see HUMAN-CHECK / JUDGMENT notes.

---

## Reader's note on the master table

The NAP appears in **hundreds** of places — chiefly the storefront phone CTA (`1-800-835-9565`, ~248 hits across 78 theme files) and the "since 1964" founding line (~130 hits across 42 files), which are the *same string repeated*. To stay exhaustive without becoming unreadable, the table below:
- enumerates **every discrete address occurrence** (street / postal / email) at line level — these are the finite, must-change items;
- groups the **ubiquitous repeated strings** (phone CTA, "since 1964") **per file with line numbers + an occurrence count**. This is deliberate grouping, *not* truncation — counts are exact (from `rg -c`).

Change-class: **REPLACE** = literal old-NAP value that must change on relocation · **JUDGMENT** = depends on whether the HQ city changes (every Peterborough / addressRegion "Ontario" / areaServed / "since 1964") · **HUMAN-CHECK** = out of API/grep reach.

---

# MASTER TABLE

## A) THEME — canonical schema + global chrome (single source of truth)

| # | Surface | Location | Exact string | Element | Variant | Class |
|---|---|---|---|---|---|---|
| 1 | THEME | theme/snippets/bbi-org-schema.liquid:35 | `"streetAddress": "296 George St N"` | street | JSON-LD streetAddress | REPLACE |
| 2 | THEME | bbi-org-schema.liquid:36 | `"addressLocality": "Peterborough"` | city | JSON-LD | JUDGMENT |
| 3 | THEME | bbi-org-schema.liquid:37 | `"addressRegion": "ON"` | region | JSON-LD | JUDGMENT |
| 4 | THEME | bbi-org-schema.liquid:38 | `"postalCode": "K9J 3H2"` | postal | JSON-LD | REPLACE |
| 5 | THEME | bbi-org-schema.liquid:31 | `"telephone": "+18008359565"` | phone | JSON-LD +1 | REPLACE |
| 6 | THEME | bbi-org-schema.liquid:32 | `"email": "info@brantbusinessinteriors.com"` | email | JSON-LD | REPLACE |
| 7 | THEME | bbi-org-schema.liquid:30 | `"foundingDate": "1964"` | founding | JSON-LD | JUDGMENT |
| 8 | THEME | theme/snippets/bbi-localbusiness-schema.liquid:38-41 | `streetAddress 296 George St N / Peterborough / ON / K9J 3H2` | street/city/region/postal | JSON-LD PostalAddress | REPLACE |
| 9 | THEME | bbi-localbusiness-schema.liquid:34 | `"telephone": "+1-800-835-9565"` | phone | JSON-LD +1- | REPLACE |
| 10 | THEME | bbi-localbusiness-schema.liquid:35 | `"email": "info@brantbusinessinteriors.com"` | email | JSON-LD | REPLACE |
| 11 | THEME | bbi-localbusiness-schema.liquid:33 | desc: "at 296 George St N, Peterborough — toll-free 1-800-835-9565 … since 1964" | street/city/phone/founding | mixed text | REPLACE |
| 12 | THEME | bbi-localbusiness-schema.liquid:49-51 | `areaServed: [Ontario, Canada]` | areaServed | JSON-LD array | JUDGMENT |
| 13 | THEME | bbi-localbusiness-schema.liquid:54 | `"foundingDate": "1964"` | founding | JSON-LD | JUDGMENT |
| 14 | THEME | bbi-localbusiness-schema.liquid:56 | `hasMap …destination=296+George+Street+North+Peterborough+ON+K9J+3H2+Canada` | street/city/postal | URL-encoded | REPLACE |
| 15 | THEME | theme/snippets/bbi-homepage-schema.liquid:45 | "…dealer in Peterborough … since 1964." | city/founding | description | JUDGMENT |
| 16 | THEME | bbi-homepage-schema.liquid:110 | "Call 1-800-835-9565 …" | phone | FAQPage answer | REPLACE |
| 17 | THEME | theme/snippets/bbi-service-jsonld.liquid:37 | `"areaServed": { … }` | areaServed | JSON-LD (per-service) | JUDGMENT |
| 18 | THEME | theme/snippets/bbi-footer.liquid:238 | `href="tel:18008359565"` … `1-800-835-9565` | phone | tel: + display | REPLACE |
| 19 | THEME | bbi-footer.liquid:242 | `href="mailto:info@brantbusinessinteriors.com"` | email | mailto: | REPLACE |
| 20 | THEME | bbi-footer.liquid:246 | `296 George St N<br>Peterborough, ON K9J 3H2` | street/city/postal | HTML address block | REPLACE |
| 21 | THEME | bbi-footer.liquid:255 | "Since 1964" | founding | footer text | JUDGMENT |
| 22 | THEME | theme/snippets/bbi-nav.liquid:635, 812-814 | `tel:18008359565` … `1-800-835-9565` (desktop + mobile nav) | phone | tel: + display ×2 | REPLACE |
| 23 | THEME | bbi-nav.liquid:12 | `{% render 'bbi-org-schema' %}` | (include) | pulls canonical NAP | — |
| 24 | THEME | theme/snippets/bbi-homepage-faq.liquid:39 | "Call 1-800-835-9565 …" | phone | accordion answer | REPLACE |
| 25 | THEME | theme/snippets/bbi-quote-modal.liquid:391 | "…or call 1-800-835-9565." | phone | error message | REPLACE |
| 26 | THEME | bbi-quote-modal.liquid:399 | "Ontario team since 1964" | founding | trust line | JUDGMENT |
| 27 | THEME | theme/snippets/ds-browse-faq.liquid:228 | "Call 1-800-835-9565 …" | phone | FAQ | REPLACE |
| 28 | THEME | theme/layout/theme.liquid:37 | "…Peterborough…" (title/meta) | city | meta | JUDGMENT |

## B) THEME — contact / about / delivery / relocation / oecm sections (NAP-heavy body copy)

| # | Surface | Location | Exact string | Element | Class |
|---|---|---|---|---|---|
| 29 | THEME | theme/sections/ds-lp-contact.liquid:87 | `tel:18008359565` → `1-800-835-9565` | phone | REPLACE |
| 30 | THEME | ds-lp-contact.liquid:92 | `mailto:info@brantbusinessinteriors.com` | email | REPLACE |
| 31 | THEME | ds-lp-contact.liquid:97 | `296 George St N<br>Peterborough, ON K9J 3H2` | street/city/postal | REPLACE |
| 32 | THEME | ds-lp-contact.liquid:131 | Google **Maps embed** `?q=296+George+Street+North+Peterborough+ON+K9J+3H2` | street/city/postal | REPLACE |
| 33 | THEME | ds-lp-contact.liquid:139 | Maps **directions** `destination=296+George+Street+North+Peterborough+ON+K9J+3H2+Canada` | street/city/postal | REPLACE |
| 34 | THEME | theme/sections/ds-lp-about.liquid:231 | `296 George St N, Peterborough, ON K9J 3H2` | street/city/postal | REPLACE |
| 35 | THEME | ds-lp-about.liquid:223 | `mailto:info@brantbusinessinteriors.com` | email | REPLACE |
| 36 | THEME | ds-lp-about.liquid:130, 207, 259 | "Call 1-800-835-9565" ×3 (incl. `1&#8209;800…` entity form) | phone | REPLACE |
| 37 | THEME | theme/sections/ds-lp-delivery.liquid:206 | "…same address at 296 George St N, Peterborough. … since 1964…" | street/city/founding | REPLACE |
| 38 | THEME | ds-lp-delivery.liquid:338 | "…headquartered at 296 George St N, Peterborough, ON K9J 3H2. … since 1964…" | street/city/postal/founding | REPLACE |
| 39 | THEME | ds-lp-delivery.liquid:161-163 | `areaServed: [Ontario, Western Canada]` | areaServed | JUDGMENT |
| 40 | THEME | ds-lp-delivery.liquid:185 + :182,:253 | "Call 1-800-835-9565" / "Family-owned since 1964" ×2 | phone/founding | REPLACE / JUDGMENT |
| 41 | THEME | theme/sections/ds-lp-relocation.liquid:194 | "…same address at 296 George St N, Peterborough. … since 1964…" | street/city/founding | REPLACE |
| 42 | THEME | ds-lp-relocation.liquid:299 | "…headquartered at 296 George St N, Peterborough, ON K9J 3H2. … since 1964…" | street/city/postal/founding | REPLACE |
| 43 | THEME | ds-lp-relocation.liquid:149 | `areaServed: Ontario` | areaServed | JUDGMENT |
| 44 | THEME | ds-lp-relocation.liquid:173 + :170 | "1-800-835-9565" / "since 1964" | phone/founding | REPLACE / JUDGMENT |
| 45 | THEME | theme/sections/ds-lp-oecm.liquid:470 | "…head office at 296 George St N, Peterborough." | street/city | REPLACE |
| 46 | THEME | ds-lp-oecm.liquid:554 | "…headquartered at 296 George St N, Peterborough, ON K9J 3H2. … since 1964…" | street/city/postal/founding | REPLACE |
| 47 | THEME | ds-lp-oecm.liquid:308 | `areaServed: "Ontario, Canada"` | areaServed | JUDGMENT |
| 48 | THEME | ds-lp-oecm.liquid:726, 732 | phone defaults `1-800-835-9565` / `18008359565` (schema settings) | phone | REPLACE |

## C) THEME — segment / brand / product / utility sections

| # | Surface | Location | Exact string | Element | Class |
|---|---|---|---|---|---|
| 49 | THEME | ds-lp-healthcare.liquid:257 | "…headquartered at 296 George St N…" | street | REPLACE |
| 50 | THEME | ds-lp-healthcare.liquid:261, 416-417 | entity note + "Call 1-800-835-9565" | street/phone | REPLACE |
| 51 | THEME | ds-lp-education.liquid:135-136, 140 | "A Peterborough dealer, family-owned since 1964" + "296 George St N" entity note | street/city/founding | REPLACE |
| 52 | THEME | ds-lp-education.liquid:394-395 | "Call 1-800-835-9565" (×11 phone hits in file) | phone | REPLACE |
| 53 | THEME | ds-lp-government.liquid:219, 224, 384-385 | entity note `296 George St N` + "Call 1-800-835-9565" | street/phone | REPLACE |
| 54 | THEME | ds-lp-non-profit.liquid:324, 328, 388-389 | entity note `296 George St N` + "Call 1-800-835-9565" | street/phone | REPLACE |
| 55 | THEME | ds-lp-professional-services.liquid:369, 373, 344-345 | entity note `296 George St N` + "Call 1-800-835-9565" | street/phone | REPLACE |
| 56 | THEME | ds-lp-industries.liquid:300, 309, 728 | entity note `296 George St N` + "Call 1-800-835-9565" | street/phone | REPLACE |
| 57 | THEME | ds-lp-brands-global-teknion.liquid:363 | "Brant Business Interiors · 296 George St N, Peterborough, ON K9J 3H2 · …" | street/city/postal | REPLACE |
| 58 | THEME | ds-lp-ergonomic-office-chairs.liquid:168, 171 | entity note + "296 George St N, Peterborough, ON K9J 3H2" footer line | street/city/postal | REPLACE |
| 59 | THEME | ds-lp-sit-stand-desks.liquid:410, 433 | entity note + "296 George St N, Peterborough, ON K9J 3H2" footer line | street/city/postal | REPLACE |
| 60 | THEME | ds-lp-quote.liquid:401, 408 | "Ontario-owned and family-run since 1964" + entity note | founding/street | REPLACE/JUDGMENT |
| 61 | THEME | ds-lp-quote.liquid:416 | schema default `"info@brantbusinessinteriors.com"` | email | REPLACE |
| 62 | THEME | ds-review-base.liquid:456 | "Brant Business Interiors · 296 George St N, Peterborough, ON K9J 3H2 · …" | street/city/postal | REPLACE |
| 63 | THEME | ds-lp-faq.liquid:186 (×2), :164, :201, :226 | "Call 1-800-835-9565" / "Peterborough region" / PO email (16 phone hits in file) | phone/city/email | REPLACE/JUDGMENT |
| 64 | THEME | ds-pdp-base.liquid:644, 799 | "Call 1-800-835-9565" ×2 (PDP CTAs) | phone | REPLACE |
| 65 | THEME | ds-cc-base.liquid:628, 998 | "1-800-835-9565" ×2 (collection CTAs) | phone | REPLACE |
| 66 | THEME | ds-article.liquid:353 | "Or call … 1-800-835-9565" | phone | REPLACE |
| 67 | THEME | ds-blog-list.liquid:211 | "Or call … 1-800-835-9565" | phone | REPLACE |
| 68 | THEME | ds-system-404.liquid:171 | "Or call us: 1-800-835-9565" | phone | REPLACE |
| 69 | THEME | ds-cs-base.liquid (1 phone hit), ds-lp-our-work / customer-stories / design-services / brands (otg/heartwood/obusforme/keilhauer/ergocentric/brands) | "Call 1-800-835-9565" CTAs + "Ontario"/"since 1964" | phone/founding | REPLACE/JUDGMENT |

## D) THEME — city section + 15 city page templates (each embeds full HQ NAP)

`theme/sections/ds-lp-city.liquid` (lines 36-37, 282, 454, 535-536) is the shared template holding the default HQ block: **"296 George St N … Peterborough, ON K9J 3H2 · 1-800-835-9565 · since 1964"** (REPLACE street/postal/phone; JUDGMENT founding).

Each `theme/templates/page.city-*.json` embeds the same HQ NAP at a consistent line pattern (~5 NAP fields/file). Files (15): **peterborough** (HQ — ~30 Peterborough mentions + street/postal/phone), barrie, brampton, brantford, burlington, cambridge, hamilton, kitchener-waterloo, london, markham, mississauga, oakville, oshawa, vaughan.

| # | Surface | Location pattern (per city template) | Exact string | Element | Class |
|---|---|---|---|---|---|
| 70 | THEME | page.city-*.json:~93 & ~151 | "headquartered at 296 George St N in Peterborough and serving <City>…" | street/city | REPLACE |
| 71 | THEME | page.city-*.json:~159 (entity_note) | "296 George St N, Peterborough, ON K9J 3H2" | street/city/postal | REPLACE |
| 72 | THEME | page.city-*.json:~145 & ~146 | `1-800-835-9565` + `18008359565` (CTA href) | phone | REPLACE |
| 73 | THEME | page.city-*.json:~142 | "…since 1964" | founding | JUDGMENT |
| 74 | THEME | page.city-peterborough.json:10, 86, 141-167 | HQ-specific: "Our showroom is at 296 George St N", "from our Peterborough headquarters at 296 George St N", "home showroom since 1964" (+~30 Peterborough mentions throughout — all JUDGMENT) | street/city/postal/phone/founding | REPLACE/JUDGMENT |

> The 14 non-HQ city templates each contain ~6 REPLACE NAP hits (street + postal + phone) → **~84 REPLACE occurrences across the city template set**, plus page.city-peterborough.json (~11 enumerated + ~30 city-name JUDGMENT mentions).

## E) THEME — non-city templates, collection templates, llms.txt, index

| # | Surface | Location | Exact string | Element | Class |
|---|---|---|---|---|---|
| 75 | THEME | theme/templates/llms.txt.liquid:8-10 | "296 George St N, Peterborough, ON K9J 3H2, Canada" + `1-800-835-9565` + `info@…` + founded `1964` | street/city/postal/phone/email/founding | REPLACE |
| 76 | THEME | theme/templates/index.json:32 | homepage section settings: "296 George St N" + "since 1964" | street/founding | REPLACE/JUDGMENT |
| 77 | THEME | page.oecm.json:110 | `1-800-835-9565` | phone | REPLACE |
| 78 | THEME | page.healthcare.json:24,38,83 | `1-800-835-9565` ×3 | phone | REPLACE |
| 79 | THEME | page.quote.json:60,62 | `info@brantbusinessinteriors.com` + `1-800-835-9565` | email/phone | REPLACE |
| 80 | THEME | page.education / non-profit / government / professional-services.json:7 | `1-800-835-9565` (×1 each) | phone | REPLACE |
| 81 | THEME | page.design-services.json:52,54,62 | `1-800-835-9565` ×2 + **`sales@brantbusinessinteriors.com`** | phone/email | REPLACE |
| 82 | THEME | page.review-executive / review-medical-clinics / review-law-firms.json:115,118,122,162 | "since 1964" ×2 + `1-800-835-9565` + "296 George St N, Peterborough, ON K9J 3H2" (each of 3 files) | street/city/postal/phone/founding | REPLACE |
| 83 | THEME | collection.tables.json:63,108 | `1-800-835-9565` ×2 | phone | REPLACE |
| 84 | THEME | collection.storage.json:123,130,137 | `1-800-835-9565` ×3 + **`quotes@brantbusinessinteriors.com`** | phone/email | REPLACE |
| 85 | THEME | collection.accessories.json:80,94,101,108 | `1-800-835-9565` ×4 + **`quotes@brantbusinessinteriors.com`** | phone/email | REPLACE |
| 86 | THEME | collection.panels-room-dividers.json:60,67,74 | `1-800-835-9565` ×2 + **`quotes@brantbusinessinteriors.com`** + "Peterborough" | phone/email/city | REPLACE/JUDGMENT |

> **Theme literal aggregate (rg -c):** `296 George St N` = **98 hits / 43 files** · `K9J 3H2` = **48 / 42** · phone (`835-9565`/`18008359565`) = **248 / 78** · `since 1964` = **130 / 42** · emails: `info@` ×20, `quotes@` ×12, `sales@` ×2.
> Collection templates with ZERO NAP: collection.desks / seating / boardroom / business-furniture / ergonomic-products / quiet-spaces.json. Config `settings_data.json` / `settings_schema.json`: ZERO NAP.

---

## F) ADMIN — Shopify store back-office (drives invoices, emails, checkout, legal)

| # | Surface | Object · field | Exact value | Element | Class |
|---|---|---|---|---|---|
| 87 | ADMIN | **Shop · billingAddress** (`shop.billingAddress`) | `296 George St N` / Peterborough / Ontario (ON) / `K9J 3H2` / Canada · phone `4168458636` | street/city/region/postal/phone | **REPLACE** — drives invoices, order/shipping emails, packing slips, checkout, legal |
| 88 | ADMIN | Shop · email | `info@brantbusinessinteriors.com` | email | REPLACE |
| 89 | ADMIN | Shop · contactEmail | `steve@brantbusinessinteriors.com` | email | JUDGMENT (back-office contact; may persist) |
| 90 | ADMIN | **Location** `gid://…/95832113465` "Peterborough Warehouse" | `296 George St N`, Peterborough ON `K9J 3H2`, Canada · phone `4168458636` | street/city/postal/phone | **REPLACE** — fulfillment/pickup address on every order |
| 91 | ADMIN | **Location** `gid://…/103081836857` "Toronto Warehouse" | `60 Leek Crescent`, **Richmond Hill** ON `L4B 1H1` · phone `+19058877700` | street/city/postal/phone | **JUDGMENT / HUMAN-CHECK** — second active location; confirm with Steve whether it stays, moves, or is the relocation target |
| 92 | ADMIN | **Shop Policy — Contact Information** | "…296 George St N, Peterborough, ON K9J 3H2" + `info@…` | street/city/postal/email | **REPLACE** (checkout-served legal page) |
| 93 | ADMIN | **Shop Policy — Privacy** | "…296 George St N, Peterborough, ON K9J 3H2" + `info@…` | street/city/postal/email | **REPLACE** |
| 94 | ADMIN | **Shop Policy — Refund** | "…296 George St N, Peterborough…" + `info@…` + `1-800-835-9565` ×2 | street/city/postal/email/phone | **REPLACE** |
| 95 | ADMIN | **Shop Policy — Shipping** | "…296 George St N, Peterborough…" + `info@…` + `1-800-835-9565` | street/city/postal/email/phone | **REPLACE** |
| 96 | ADMIN | **Shop Policy — Terms of Service** | "…296 George St N, Peterborough…" + `info@…` | street/city/postal/email | **REPLACE** |
| 97 | ADMIN | Shop metafield `avada_faq.widgetSetting` | contact email `steve@brantbusinessinteriors.com` (Avada FAQ app widget) | email | JUDGMENT (app-stored contact) |
| 98 | ADMIN | Media files (filename scan) | logos only: `oc-head-logo-v3.png`, `OCI_BBI-logo.svg`, `New_OC_BBI_Logo-raster.png`, `bbi-logo-v2.png`, etc. — no address text in filename/alt | — | HUMAN-CHECK (eyeball footer logo / any baked-in address — low risk; no map/letterhead image found by name) |

---

## G) CONTENT — Shopify Online Store pages & blog articles (body_html)

| # | Surface | Object · handle | Exact / summary | Element | Class |
|---|---|---|---|---|---|
| 99 | CONTENT | Page `/pages/llms-txt` (170621272377) "BBI for AI assistants" | full NAP in body: 296 George St N, K9J 3H2, Peterborough ×3, `1-800-835-9565`, `info@…`, since 1964 ×2 — **AND a stale `Brantford` reference** | street/city/postal/phone/email/founding + **stale** | **REPLACE** (+ fix stale Brantford) |
| 100 | CONTENT | Page `/pages/win-a-prize-with-brant-basics` (150007742777) | body: "296 George St N" + "K9J 3H2" + "Peterborough" ×3 (incl. "Peterborough Pete's game") | street/postal/city | REPLACE/JUDGMENT |
| 101 | CONTENT | Blog **News** (108557861177) — **44 articles, ALL carry the phone CTA** `1-800-835-9565` (×1 each, "Call/Or call …") | every article body | phone | REPLACE (×44) |
| 102 | CONTENT | …of those, **~38 articles also carry "since 1964"** in body (1-2× each); 2 articles also carry "1964" in their `faq.items` metafield | article body / faq metafield | founding | JUDGMENT |
| 103 | CONTENT | Article `oecm-ontario-school-boards-office-furniture` | full street NAP: 296 George + Peterborough + **`quotes@brantbusinessinteriors.com`** + 1964 | street/city/email/founding | REPLACE |
| 104 | CONTENT | Articles `source-office-furniture-alternative-ontario`, `ikea-office-furniture-alternative-business-ontario`, `wayfair-professional-office-furniture-alternative-ontario`, `buying-new-vs-used-office-furniture-ontario` | each body: "296 George St N" + "K9J 3H2" + "Peterborough" + phone + 1964 | street/city/postal/phone/founding | REPLACE (×4) |
| 105 | CONTENT | Article `commercial-office-furniture-suppliers-ontario` | body: phone + 1964 + **stale `Brantford` ×2** | phone/founding/**stale** | REPLACE (fix stale Brantford) |
| 106 | CONTENT | Article SEO metafields (`global.title_tag` / `global.description_tag`) | scanned all 44 — **ZERO NAP** (no address/phone/postal) | — | clean |
| 107 | CONTENT | Legacy pages `/pages/contact` ("Office Spaces Designers & Architects"), `/pages/shipping-delivery`, `/pages/suppliers`, `/pages/ergocentric`, `/pages/quote`, legacy `/pages/frequently-asked-questions` | bodies scanned — **no hardcoded street/postal/phone/email NAP** (generic copy) | — | clean (legacy pages flagged in brief are clear) |
| 108 | CONTENT | **Collections (392 scanned)** — 14 leaf collections carry "since 1964" / "Peterborough" in `descriptionHtml` (e.g. height-adjustable-tables, meeting-tables, boardroom-conference-meeting, bariatric-seating, reception-side-guest-chairs, folding-stacking-chairs-carts, lecterns-podiums, +7). **No street/postal/phone/email in any collection description or SEO metafield.** | founding/city | JUDGMENT |

---

## H) DATA-DOC — internal repo docs (seed copy; update so regen doesn't reintroduce stale NAP)

| # | Surface | File | NAP elements | Class |
|---|---|---|---|---|
| 109 | DATA-DOC | **`data/llms-txt-draft.md`** | full NAP, ~46 hits — **master seed for the AI-assistant entity facts** | DATA-DOC (canonical seed) |
| 110 | DATA-DOC | **`data/city-pages/peterborough-PACK.json`** | full HQ NAP (296 George, K9J 3H2, phone, 1964), ~29 hits — primary geo-pack seed | DATA-DOC (canonical seed) |
| 111 | DATA-DOC | **`data/city-pages/*-PACK.json`** (≈19 other geo packs: belleville, kingston, oshawa, …) | each embeds the canonical HQ NAP as context — cascading regen risk | DATA-DOC |
| 112 | DATA-DOC | `BBI-Session-Kickoff/bbi-build-state.md` (+8 `.bak` snapshots) | street/postal/phone/email/1964 throughout | DATA-DOC (main tracker; backups archival) |
| 113 | DATA-DOC | `BBI-Session-Kickoff/bbi-interlinking-map.md` | email/phone/postal/street (~32) | DATA-DOC |
| 114 | DATA-DOC | `docs/plan/bbi-lead-routing.md` (+ `docs/strategy/bbi-lead-routing.md`, `data/reports/lead-routing-2026-05-24.md`) | full NAP — live ops routing | DATA-DOC (update before quoting post-move) |
| 115 | DATA-DOC | `docs/strategy/icp.md`, `docs/strategy/lead-inbox-provisioning.md`, `docs/strategy/policy-pages-audit.md` | full NAP — ICP/positioning/founding narrative | DATA-DOC |
| 116 | DATA-DOC | `data/content-drafts/*.md` (01-pillar published; 02+ unpublished drafts, step-2-2-category-copy.md) | NAP in body/FAQ source — **don't regen until NAP locked** | DATA-DOC (hold for review) |
| 117 | DATA-DOC | `data/audits/schema-audit-2026-05-27/captures/*.jsonld.json` (23 files) | baked NAP in captured JSON-LD — point-in-time snapshots | DATA-DOC (archival; re-audit after move) |
| 118 | DATA-DOC | `data/forensics/2026-05-27-watcher-discovery/snapshot/**` (theme snapshot), `data/design-photos/screens-*/**.html` | baked NAP — forensic/design snapshots, NOT live | DATA-DOC (archival; do not regen from) |
| 119 | DATA-DOC | `data/reports/competitor-recon-2026-05-25.md`, `interlink-3-audit-2026-05-23.md`, `keyword-research/raw/*peterborough*`, `_catalog-feed-snapshot-*.json` (+catalog/spec reports) | NAP/phone/city in generated reports | DATA-DOC (archival) |
| 120 | DATA-DOC | `CLAUDE.md`, `data/reference/priority-keywords.yaml` | brand domain / "Peterborough" keyword note | DATA-DOC (low density) |

> **Excluded as noise:** `data/backups/`, `data/exports/`, `data/logs/` (snapshots). **TOTAL DATA-DOC files with NAP ≈ 45.**

---

## I) OUT-OF-REACH — not exposed to API / grep (HUMAN-CHECK)

| # | Surface | What to check | Class |
|---|---|---|---|
| 121 | OUT-OF-REACH | **Shopify Settings → Notifications** — order confirmation, shipping confirmation, **draft-order invoice**, POS receipt, etc. These email/print templates are NOT exposed by the Admin API used here and pull from / can hardcode the NAP. **Must be eyeballed in Admin.** | HUMAN-CHECK |
| 122 | OUT-OF-REACH | **Third-party quote/invoice apps storing their own "from"/company address:** OmegaQuote / **QuoteSnap** (`OmegaQuote*` shop metafields — DTC + B2B + list settings), **Globo Request-for-Quote** (`globo.rfq_theme_*` — 11 theme configs), Magical "mandatory fees". Quote/RFQ PDFs & emails likely carry a company address set inside the app admin. **Check each app's settings.** | HUMAN-CHECK |
| 123 | OUT-OF-REACH | **Avada FAQ app** stores `steve@brantbusinessinteriors.com` (verified in `avada_faq.widgetSetting`); confirm no address/phone in the app's own dashboard. | HUMAN-CHECK |
| 124 | OUT-OF-REACH | **Address baked into images** — footer/header logo files (`OC_BBI`/`bbi-logo-v2`), any showroom/map graphic. No map/letterhead image found by filename, but logos and hero images must be eyeballed for embedded address text. | HUMAN-CHECK |
| 125 | OUT-OF-REACH | **Google Business Profile + external citations** (directories, OECM supplier listing, social profiles, schema aggregators). Handled separately, after the on-site change. | HUMAN-CHECK |
| 126 | OUT-OF-REACH | **Email DNS / mailbox provisioning** for `info@` / `quotes@` / `sales@` / `steve@ brantbusinessinteriors.com` — unaffected by address move unless domain/brand changes; noted for completeness. | HUMAN-CHECK |

---

# ROLLUP 1 — Canonical sources (change the source, not the symptom)

| NAP element | Single source of truth | Notes |
|---|---|---|
| **Structured JSON-LD (Org / LocalBusiness / WebSite)** | `theme/snippets/bbi-org-schema.liquid` + `theme/snippets/bbi-localbusiness-schema.liquid` | Org-schema is included via `bbi-nav.liquid` site-wide; localbusiness-schema holds full PostalAddress + hasMap + areaServed. **Primary on-site canonical.** |
| **Per-service areaServed** | `theme/snippets/bbi-service-jsonld.liquid` | colocated with homepage schema |
| **Global footer NAP block** | `theme/snippets/bbi-footer.liquid:238-255` | the human-visible address/phone/email on every page |
| **Nav phone CTA** | `theme/snippets/bbi-nav.liquid` (desktop + mobile) | |
| **AI-assistant entity facts** | `theme/templates/llms.txt.liquid` (live) ← seeded by `data/llms-txt-draft.md` | update BOTH; the draft is the regen seed |
| **City-page HQ block** | `theme/sections/ds-lp-city.liquid:36-37` (template default) ← seeded by `data/city-pages/*-PACK.json` | per-template overrides live in each `page.city-*.json` |
| **Invoices / order & shipping emails / checkout / packing slips** | **Shop `billingAddress`** (Admin) | NOT in theme — the single most important non-theme source |
| **Fulfillment / pickup address** | **Location "Peterborough Warehouse"** (Admin) | + decide fate of "Toronto Warehouse" / 60 Leek Crescent |
| **Legal pages** | **5 Shop Policies** (Admin, checkout-served) | full NAP in each |
| **Emails (contact)** | `info@` (storefront/shop), `quotes@` (collection/blog CTAs), `sales@` (design-services), `steve@` (Admin contactEmail + Avada FAQ) | four distinct mailboxes referenced |

---

# ROLLUP 2 — Count by surface (REPLACE-class hits)

| Surface | REPLACE hits (literal old NAP that must change) | Notes |
|---|---|---|
| **THEME** | **~430+** | street `296 George` 98 + postal `K9J 3H2` 48 + phone 248 + emails 34 (across 43-78 files). Phone CTA is the bulk. |
| **ADMIN** | **~20 fields** | shop billingAddress (5 fields + phone) + Peterborough Location (4 + phone) + 5 policies (each ~4 fields) + shop email. Low row count, **highest blast radius** (invoices/legal/checkout). |
| **CONTENT** | **~55** | 44 article phone CTAs + 6 articles w/ full address + 2 pages (llms-txt, win-a-prize) + quotes@ in 1 article. |
| **DATA-DOC** | **~45 files** | seed/doc copy; not customer-facing but regenerates customer-facing copy. |
| **JUDGMENT (all surfaces)** | "since 1964" ~130 theme + ~38 articles + 14 collections; every `Peterborough` / addressRegion `Ontario` / `areaServed` — **only change if the HQ city changes.** |
| **Stale residuals** | 2 | `Brantford` in `/pages/llms-txt` body + article `commercial-office-furniture-suppliers-ontario`. |

---

# ROLLUP 3 — Out-of-reach / human-must-do

1. **Shopify Settings → Notifications** (order/shipping/draft-invoice/POS templates) — not API-readable here; must be checked in Admin. **Highest-risk blind spot for invoices.**
2. **Quote/RFQ apps with their own address store:** OmegaQuote/**QuoteSnap** (DTC+B2B), **Globo RFQ** (11 theme configs), Magical mandatory-fees — quote/invoice PDFs & emails. Check each app admin.
3. **Avada FAQ app** — confirmed holds `steve@…` email; verify no address/phone.
4. **Address baked into images** — footer/header logos + hero/showroom graphics (eyeball; no map/letterhead found by filename).
5. **Google Business Profile + external citations / directories / OECM listing / social** — handle after the on-site change.
6. **Second physical location** — "Toronto Warehouse" `60 Leek Crescent, Richmond Hill` (+ stale `Brantford` mentions): confirm with Steve whether it stays, is the relocation target, or should be removed.

---

## Summary

- **Total occurrences inventoried:** **hundreds** — anchored by phone CTA (248 theme hits / 78 files), street `296 George St N` (98 / 43), postal `K9J 3H2` (48 / 42), plus ~55 CONTENT and ~20 high-blast-radius ADMIN fields and ~45 DATA-DOC files.
- **REPLACE-class (must change on relocation):** **~430+ theme + ~20 Admin fields + ~55 content + ~45 doc files.** Discrete address strings (street/postal/email) and the Admin billingAddress/location/policies are the finite must-change set; the phone CTA is the highest-frequency repeated string.
- **JUDGMENT-class (only if the HQ city changes):** every `since 1964` (~180), `Peterborough`, addressRegion `Ontario`, and all `areaServed` values.
- **Surfaces touched:** THEME (snippets/sections/templates/layout), ADMIN (shop, 2 locations, 5 policies, app metafields, media), CONTENT (2 pages, 44 blog articles, 14 collections), DATA-DOC (~45 files), plus 6 OUT-OF-REACH human-check items.
- **Two stale residuals to clean up regardless of the move:** `Brantford` ×2 surfaces.
- **No mutations were made.** This is the audit pass only.
