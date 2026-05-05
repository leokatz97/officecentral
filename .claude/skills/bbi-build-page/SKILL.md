---
name: bbi-build-page
description: >
  Explicit slash command for building Brant Business Interiors (BBI) Shopify pages.
  Runs Leo's full 7-step workflow entirely inside Claude Code — reads the LOCKED design
  system files, builds the HTML preview directly, previews it in-browser, then converts
  to Shopify. No Claude Design / claude.ai/design involved.

  Invoked as `/bbi-build-page [page name]` — e.g. `/bbi-build-page homepage`,
  `/bbi-build-page contact`, `/bbi-build-page healthcare`. Parse the page name
  from the arguments.

  Do NOT auto-trigger on general page-building requests, mentions of Shopify,
  or phrases like "build a page". Only fire when Leo explicitly invokes
  `/bbi-build-page`.
---

# BBI Build Page

Leo's canonical workflow for building a new BBI Shopify page. Seven steps, always in order, no skipping — even for simple pages. **Built entirely in Claude Code** — reads canonical design system sources, writes the HTML, previews in browser, iterates, then converts to Shopify.

---

## Usage

Leo invokes: `/bbi-build-page [page name]`

Parse the page name from the arguments. If he didn't include one, ask once: "Which page are we building?" Then go straight to the Pre-Step.

---

## Store & Business Context

- **Store:** office-central-online.myshopify.com
- **Theme:** "BBI Landing Dev" (ID 186373570873) — draft only, never publish
- **Plan:** Shopify Basic — no CLI. All edits via Shopify Admin → Edit Code or Customizer
- **Business:** Brant Business Interiors (BBI), part of Office Central Group of Companies
- **Credentials:** OECM Supplier Partner (Agreement 2025-470), authorized ergoCentric dealer
- **Buyers:** B2B institutional — schools, healthcare, government, non-profit across Ontario. Everything is quote-based — no cart checkout.
- **Address:** 295 George St N, Peterborough, ON K9J 3H2
- **Phone:** 1-800-835-9565
- **Email:** info@brantbusinessinteriors.com
- **Products:** Business Furniture only (scope change 2026-04-25). 9 categories: Seating, Desks & Workstations, Storage & Filing, Tables, Boardroom, Ergonomic Products, Panels & Dividers, Accessories, Quiet Spaces. Educational, Daycare & ECE, and Healthcare & Seniors verticals were archived.

---

## Brand Design Tokens — Locked Anchors

Source of truth: [docs/strategy/design-system.md](../../docs/strategy/design-system.md). Do not re-derive tokens in any prompt — paste anchors only and reference the spec by name.

**Locked color anchors (do not relitigate):**
- `red-surface` = `#D4252A` (buttons / banners / sale badges)
- `red-text` = `~#A81E22` (any red text on white — AA 4.5:1 verified in design-system.md)
- Anchor neutral = charcoal `#0B0B0C` (body + headings — NOT navy, supersedes any `#1a2744` reference)
- Canvas = `#FFFFFF`. Surface tier = `#FAFAFA`. **Anything warmer is banned.**
- **No beige / tan / cream / sand. No warm tones. No dark mode. No gradients on red. No red as body link color. No red headings.**
- Red density target: 5–8% per screen.

**Token vocabulary (use these names — Shopify Admin maps them 1:1):**
- Per-scheme: `--background, --cardBackground, --textColor, --linkColor, --headingColor, --buttonBackground, --buttonColor, --buttonBorder, --inputBackground, --inputBorder, --borderColor, --line-color, --shadowColor` (+ hover/alternate variants — full list in design-system.md)
- Global: `--saleBadgeBackground, --soldBadgeBackground, --headerBg, --headerColor, --cartCountBg, --submenuBg` (+ siblings)
- Two schemes are defined: `scheme-default` (white canvas, 90% of pages) and `scheme-inverse` (charcoal canvas, hero/feature blocks only)

**Tone:** B2B institutional. Outcome-focused. No fluff. No serif. No emoji on the site. Maple-leaf icon required wherever Canadian-Owned or Made-in-Canada copy appears.

Reference templates: [theme/templates/page.oecm.json](../../theme/templates/page.oecm.json) and [theme/templates/page.brand-dealer.json](../../theme/templates/page.brand-dealer.json) — match their section order. **For visual rhythm, attach the ANTI-REF screens** from `Design System Zips/5 - Landing Page (2)/uploads/15-ANTI-REF-homepage.png` (homepage layout) and `16-ANTI-REF-nav.png` (header/nav). These are the authoritative visual anchors — they supersede any `data/design-photos/design-system-v1-*/` reference screens.

---

## Existing ds-* Inventory — Never Rebuild

**Sections** (`theme/sections/`):
- `ds-site-header.liquid` — nav, `tel:` phone link, quote modal trigger
- `ds-site-footer.liquid` — 4-column footer. Links format: `Label | /url` per line
- `ds-announce-bar.liquid` — scrolling announcement strip
- `ds-page-hero.liquid` — inner page hero with photo, seal, CTAs
- `ds-feature-strip.liquid` — 3-column icon feature strip
- `ds-featured-grid.liquid` — card grid with photos and quote CTAs
- `ds-trust-row.liquid` — logo/client trust row
- `ds-quote-cta.liquid` — bottom-of-page quote CTA band
- `ds-quote-modal-mount.liquid` — mounts the quote modal

**Snippets** (`theme/snippets/`):
- `ds-head-assets.liquid` — loads CSS, JS, JSON-LD (wired in via header)
- `ds-structured-data.liquid` — Organization + LocalBusiness JSON-LD (confirmed working)
- `ds-button.liquid` — params: `label`, `variant`, `href`, `quote`, `arrow`

**Assets** (`theme/assets/`):
- `ds-landing.css` + `ds-landing.js` — all styles and modal logic

**Templates already done** (`theme/templates/`):
- `page.oecm.json` (OECM landing, QA passed)
- `page.brand-dealer.json` (ergoCentric dealer, QA passed)

**Layout gate:** `theme/layout/theme.liquid` suppresses Starlite header/footer/cart on BBI landing templates via the `bbi_landing` variable. Every new Type-A suffix needs one line added to that gate.

**Photo library:** `data/oci-photos/catalog.json` — 48 real project photos. Use for heroes, Our Work, industry pages.

**Component canon:** All canonical CSS and page templates live in `Design System Zips/5 - PDP/src/`. This is the complete, up-to-date design system bundle — use it as the single source of truth for every page type.

**Shared CSS (used on every page):**
- `Design System Zips/5 - PDP/src/tokens.css` — all CSS custom property definitions
- `Design System Zips/5 - PDP/src/bbi-components.css` — all shared classes: `.bbi-btn`, `.bbi-mono`, `.bbi-section`, `.bbi-container`, `.bbi-section-head`, `.bbi-card--collection`, `.bbi-card--product`, `.bbi-badge--oecm`, `.bbi-ph`, `.bbi-cta-section`, header, footer

**Page-specific CSS + JSX template (by page type):**

| Page type | JSX template | CSS file | Class prefix |
|---|---|---|---|
| Homepage | `src/Homepage.jsx` | `src/homepage.css` | `.hp-*` |
| Collection category | `src/CollectionCategory.jsx` | `src/collection-category.css` | (check file) |
| Collection (sub-collection) | `src/Collection.jsx` | `src/collection.css` | (check file) |
| Landing pages (OECM, industries, brands, services, about) | `src/Landing.jsx` | `src/landing.css` | `.lp-*` |
| PDP (unbuyable + buyable) | `src/ProductDetail.jsx` | `src/pdp.css` | `.pd-*` |

**Landing page section order** (from `Landing.jsx` composition):
Header → Breadcrumbs (`.lp-crumbs-band`) → Hero (`.lp-hero`) → Intro (`.lp-intro`) → Differentiators (`.lp-diff`) → Trust photos (`.lp-trust-row`, conditional) → Proof bar (`.lp-proof-bar`, conditional) → Crosslinks (`.lp-crosslinks`, conditional) → OECM bar (conditional) → FAQ (`.lp-faq`) → Closer (`.bbi-cta-section.scheme-inverse`) → Footer

**PDP section order** (from `ProductDetail.jsx` composition):
Header → Breadcrumbs (`.pd-crumb-band`) → Hero (`.pd-hero`, gallery 60% + commerce panel 40%) → Description (`.pd-description`) → Specs (`.pd-specs`, conditional) → Variants (`.pd-variants`, conditional) → OECM bar → Related (`.pd-related`, conditional) → Brand block (`.pd-brand-block`, conditional) → Closer (`.bbi-cta-section.scheme-inverse`) → Footer

**Visual reference:** `Design System Zips/5 - PDP/BBI Templates Bundle.html` — rendered HTML of ALL templates in one file. Use as a visual anchor for any page type.

**ANTI-REF images** (visual lock for header/nav): `Design System Zips/5 - Landing Page (2)/uploads/15-ANTI-REF-homepage.png` and `16-ANTI-REF-nav.png` — still the canonical nav/header reference.

Do not invent class names or token names. Every class used must trace back to these source files. `data/design-photos/components-v1-2026-04-27/Components.html` is a retired spec sheet — do not use it as a reference.

**AI page-image library:** pre-generated 16:9 hero images for every BBI landing page, produced by `scripts/generate-page-images.py` (fal.ai flux/schnell). See slug→folder table in Pre-Step.
To (re)generate: `python3 scripts/generate-page-images.py --live` (or `--limit=3 --live` for a smoke test).

---

## Trust Signal Placement Matrix

Reference table used by Step 2 (microcopy inventory) and Step 3 (Claude Design prompt). Trust signals must land in specific slots, not be sprinkled. "Always" = required on every page of that type; "If applicable" = include only when the page topic supports it (e.g. OECM logo on government/healthcare/education, not on private-sector dealer pages).

| Trust signal | Where it MUST appear | Where it MAY appear | Never |
|---|---|---|---|
| **Phone `1-800-835-9565`** | Header (`tel:` link, always) + 1 in-body CTA (hero subheading OR quote-cta band) | Footer | Buried in body paragraph text |
| **OECM Supplier Partner (Agreement 2025-470)** | Trust row (logo or text badge) on every page targeting Primary ICP (institutional Ontario) | Hero subheading on OECM/government/healthcare/education pages; first 200 words of body copy as a stated fact (AEO anchor) | Marketing-claim phrasing ("we're proud to be…"); decorative repetition |
| **Canadian-owned line** | Footer (always) | Hero subheading on industry/brand pages; trust row as separate badge | Inside product cards; mid-paragraph fluff |
| **🍁 Maple leaf icon** | Adjacent to every "Canadian-made" or "Canadian-owned" claim | — | As decorative background; without an accompanying claim |
| **Authorized dealer (ergoCentric, Keilhauer, Global, Teknion)** | Brand-dealer pages: hero subheading + trust row | Category pages where the brand is featured (single line in feature strip) | Generic landing pages where the brand isn't relevant |
| **Client logo row** | Trust row on Type A landing pages with Primary ICP | Homepage, About, Customer Stories | Conversion-only pages (Quote form, 404) |
| **Testimonial quote** | Trust row OR dedicated testimonial block on industry/brand/services pages | Homepage, Customer Stories | Hero (too dense); quote-cta band (competes with form CTA) |

**Per-page-type defaults (apply unless the brief says otherwise):**

| Page type | Hero subheading anchor | Trust row content | Quote CTA band sub-line |
|---|---|---|---|
| Industry (healthcare/education/government) | OECM line + phone | OECM seal + 4–6 client logos + Canadian-owned badge | "OECM-eligible. Quote in 1 business day." |
| Brand dealer (Keilhauer, ergoCentric, etc.) | "Authorized [Brand] dealer" + 🍁 if Canadian-made | Brand logo + OECM seal (if Primary ICP) + 2–3 client logos | "Authorized dealer. Quote in 1 business day." |
| Service (design, delivery, relocation) | Outcome-anchor (e.g. "Free space plan included") + phone | OECM seal + 4–6 client logos | "Quote in 1 business day. Phone 1-800-835-9565." |
| OECM (`/pages/oecm`) | OECM agreement number + "purchase without open tender" | OECM seal (large) + Ontario buyer logos | "OECM Agreement 2025-470. Quote in 1 business day." |
| Category (Seating, Desks, etc.) | Category outcome (e.g. "Built for institutional use") | OECM seal + 3 brand logos carried in this category | "Quote in 1 business day." |
| Brand-filtered smart collection | Brand-only line ("Authorized [Brand] dealer") | Brand logo only | "Quote in 1 business day." |
| About / Customer Stories | Canadian-owned + Ontario-focused | Client logos + Canadian-owned badge | Standard quote CTA |
| FAQ / Contact / Quote form | Phone (no OECM in hero — would distract from form) | OECM seal in trust row only | (page IS the conversion endpoint — no separate band) |
| Homepage | Outcome-anchor + phone | Full client logo strip + OECM seal + Canadian-owned badge | Standard quote CTA |

If a page type isn't listed, default to: OECM in trust row (if Primary ICP), phone in header + quote-cta, Canadian-owned in footer.

---

## Two Page Types

**Type A — BBI Custom Landing Page**
(campaign pages, dealer pages, OECM, verticals, services)
- Uses: JSON template + `ds-*` sections + BBI header/footer
- Starlite chrome: **suppressed** (via `bbi_landing` gate)

**Type B — Standard Shopify Page**
(homepage, product pages, collection pages, about, contact)
- Uses: default Shopify templates + Starlite sections
- Starlite chrome: **active**

---

## Pre-Step — Pull Page Brief (you do this before Step 1)

Before scoping, load every piece of context available for this page:

**Wave 0 Gate — check before building any Phase 1+ page**

Read `docs/plan/shopify-fix-plan.md` Wave 0 section and surface the status of these blocking items. If any are ⬜ Not started, flag them to Leo before continuing — SEO won't compound without this foundation in place:

| # | Task | Blocking? |
|---|------|-----------|
| W0-1 | GSC + GA4 live | Phase 1 pages (SEO untrackable until live) |
| W0-2 | Google Business Profile created | Local SEO |
| W0-3 | Product redirect CSV uploaded | All shop pages |
| W0-4 | Meta titles + descriptions audited | Blocked on W0-1 |
| W0-6 | Parent domain backlinks | Authority |
| W0-7 | OECM + trust signals on BBI store | Trust pages |

If Leo wants to proceed anyway, note which W0 items are outstanding and flag that SEO impact will be limited until they're done. Don't block the build — just make the dependency visible.

---

**Pre-Step 0a — Design System Gate**

Before scoping any page, verify the design-system rebuild is in place. If any of these checks fail, stop and tell Leo to run / finish the 3-phase Claude Design playbook before continuing:

- [ ] `docs/strategy/design-system.md` exists and contains no `TBD` placeholders in the per-scheme color tables, typography table, or radius/shadow scales
- [ ] `docs/reviews/design-system-audit-2026-04-27.md` is present (token-name reference)
- [ ] The canonical design system bundle exists at `Design System Zips/5 - PDP/src/` — specifically confirm these files are present:
  - `tokens.css`, `bbi-components.css` (shared — required for every page)
  - `Homepage.jsx` + `homepage.css` (homepage)
  - `Landing.jsx` + `landing.css` (all landing pages)
  - `ProductDetail.jsx` + `pdp.css` (all PDPs)
  - `CollectionCategory.jsx` + `collection-category.css` (category pages)
  - `Collection.jsx` + `collection.css` (sub-collection pages)
- [ ] ANTI-REF images exist at `Design System Zips/5 - Landing Page (2)/uploads/15-ANTI-REF-homepage.png` and `16-ANTI-REF-nav.png` (visual header/nav lock)
- [ ] Logo exists at `Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png` ("Brant ✱ BI | Business Interiors" wordmark)
- [ ] **Before building any page:** read the corresponding JSX template for that page type — the component tree defines section order. Never derive structure from memory or prose.

If `design-system.md` still has TBDs, surface the missing rows and pause. Do not let the page build re-derive tokens.

---

**0. Inventory pre-generated images** — use the table below to find the exact subfolder for this page, then list the files inside it:

| Page name (as Leo says it) | Image folder |
|---|---|
| homepage | `data/page-images/homepage/` |
| about / about-us | `data/page-images/about-us/` |
| **Shop — vertical & category pages (post-2026-04-25 architecture)** | |
| business-furniture / shop-hub | `data/page-images/business-furniture/` |
| seating | `data/page-images/seating/` |
| desks | `data/page-images/desks/` |
| storage | `data/page-images/storage/` |
| tables | `data/page-images/tables/` |
| boardroom | `data/page-images/boardroom/` |
| ergonomic-products | `data/page-images/ergonomic-products/` |
| panels-room-dividers / panels | `data/page-images/panels-room-dividers/` |
| accessories | `data/page-images/accessories/` |
| quiet-spaces | `data/page-images/quiet-spaces/` |
| **"View all" smart collections (no dedicated image folder — use parent category image)** | |
| all-seating | use `data/page-images/seating/` hero (these are browse pages — no new image generation needed) |
| all-desks | use `data/page-images/desks/` |
| all-storage | use `data/page-images/storage/` |
| all-tables | use `data/page-images/tables/` |
| all-boardroom | use `data/page-images/boardroom/` |
| all-ergonomic-products | use `data/page-images/ergonomic-products/` |
| all-panels | use `data/page-images/panels-room-dividers/` |
| all-accessories | use `data/page-images/accessories/` |
| all-quiet-spaces | use `data/page-images/quiet-spaces/` |
| all-business-furniture | use `data/page-images/business-furniture/` |
| **Industries** | |
| industries-hub | `data/page-images/industries-hub/` |
| healthcare | `data/page-images/healthcare/` |
| education | `data/page-images/education/` |
| government | `data/page-images/government/` |
| non-profit | `data/page-images/non-profit/` |
| professional-services | `data/page-images/professional-services/` |
| **Brands** | |
| brands-hub | `data/page-images/brands-hub/` |
| keilhauer | `data/page-images/keilhauer/` |
| global-teknion | `data/page-images/global-teknion/` |
| ergocentric | `data/page-images/ergocentric/` |
| **Services** | |
| design-services | `data/page-images/design-services/` |
| delivery | `data/page-images/delivery/` |
| **Trust & system pages (no image folder yet — generate via `scripts/generate-page-images.py` if needed)** | |
| faq | _none — text-heavy page, hero from oci-photos optional_ |
| quote (Request a Quote) | _none — form page, hero from oci-photos optional_ |
| customer-stories | _none yet — use client logos from `data/testimonials/` + project photos from `data/oci-photos/` (Mattamy, Kawartha Dairy, etc.). Generate hero via script if needed._ |
| blog-resources | _none — generate if building_ |
| 404 | _none — uses category thumbnails_ |
| **Deprecated (do not use — kept for reference only)** | |
| ~~task-seating~~ | use `seating/` (post-2026-04-25 architecture: `/collections/seating` is the category page; old task-seating is now a sub-collection) |
| ~~collaboration~~ | use `boardroom/` |
| ~~acoustic-pods~~ | use `quiet-spaces/` |
| ~~home-office~~ | page removed in scope change 2026-04-25 |
| ~~collections-hub~~ | use `business-furniture/` (Shop Hub removed; nav links directly to `/collections/business-furniture`) |
| ~~verticals-hub~~ | use `industries-hub/` |

Pattern inside each folder: `{slug}-product.jpg` (product hero) and `{slug}-space.jpg` (room scene, where it exists). If the page name doesn't match any row above, check `data/page-images/` directly for a matching folder before proceeding.

Also check the manifest CSV at `data/reports/generated-page-images-YYYY-MM-DD.csv` — if a slot is `SOURCE=OCI_PHOTO`, use the matching OCI photo from `data/oci-photos/catalog.json` for that slot instead.

**After identifying the folder, run `ls data/page-images/{slug}/` and report the exact filenames found.** Do not guess filenames from the pattern — confirm they exist before citing them in Step 3's Claude Design prompt.

If neither `{slug}-product.jpg` nor `{slug}-space.jpg` exists in the folder (and no OCI photo is specified in the manifest CSV), **pause here** and ask Leo to choose before continuing:
- **(a)** Generate: `python3 scripts/generate-page-images.py --limit=1 --live` (add `--slug={slug}` if supported, otherwise run the full script and pull the new file)
- **(b)** Substitute an OCI photo from `data/oci-photos/catalog.json` — pick the one whose description best matches the page theme
- **(c)** Proceed with a solid `--borderColor` (`#DEE1E6`) placeholder — not ideal for first-impression pages, but acceptable for rough drafts

Do not proceed to Step 1 until image slots are confirmed.

**1. Read the site build checklist** at `previews/bbi-planning-hub.html` — find the entry matching the page name in the `PAGES` array. Extract its `tips` array. These are the pre-agreed best-practice tips for this exact page: ICP target, hero photo, CTA priority, copy angle, SEO keywords, trust signals. They are your primary brief.

**2. Read ICP & voice** at `docs/strategy/icp.md` — confirm which ICP (Primary = institutional Ontario, Secondary = SMB) this page targets and apply the matching voice calibration. Note any SEO keyword lists relevant to this page — you'll use them in Step 2B.

**3. Read voice samples** at `docs/strategy/voice-samples.md` — reference the 5 approved rewrites so copy tone in the Step 2 brief matches what's already been signed off.

**4. Check photo library** at `data/oci-photos/catalog.json` — the checklist tips usually name specific photos. Confirm the filename exists before citing it in Step 3's Claude Design prompt.

**5. Read competitor context** at `docs/strategy/competitor-analysis.md` — note any direct competitors, overlapping SKUs, or positioning gaps relevant to this page. Use to sharpen differentiation in Step 2 copy.

**6. Read testimonials** at `docs/strategy/testimonials.md` — pull 1–2 client quotes that match the ICP for this page. Available for use in trust row, hero sub-copy, or quote CTA.

**7. Read segment analysis** at `docs/strategy/segment-analysis.md` — confirm revenue share and buyer profile for the segment this page targets. Use to calibrate urgency, price anchors, and trust signals in Step 2.

Summarize the loaded brief to Leo in one short block: tips, ICP target, **exact image files to attach in Step 3** (filenames + which slot each covers: hero-product / hero-space / OCI photo), 1 competitor differentiator, 1 client quote if available. Confirm before Step 1.

---

## Step 1 — Scope (you do this, ~2 min)

Tell Leo:
- Page type (A or B)
- Which sections to use and in what order — start from the default stack below, then add/remove/reorder based on the page tips from the Pre-Step
- What content he needs to gather before starting (photos, logos, client names, product specs, etc.)
- Which links on this page point to pages not yet built — flag as `[placeholder]`

**Default section stacks (starting point — adjust per page):**

**Type A — BBI Custom Landing Page** (industries, brands, services, OECM, campaigns):
1. `ds-announce-bar` — include only if there's a seasonal promo or OECM-specific message active; omit otherwise
2. `ds-site-header` — always
3. `ds-page-hero` — full-width, photo background; H1 goes here
4. `ds-feature-strip` — 3 key value props (outcome-focused, not feature-list)
5. `ds-featured-grid` — product/service cards, or sub-category tiles; every card needs an image slot
6. `ds-trust-row` — client logos, OECM seal, certifications
7. `ds-quote-cta` — conversion band at bottom
8. `ds-quote-modal-mount` — always; mounts the quote modal used by all CTAs
9. `ds-site-footer` — always

Remove `ds-featured-grid` for text-heavy pages (FAQ, Contact, policies) where a card grid doesn't apply. Add a second `ds-feature-strip` or a testimonial block between trust-row and quote-cta on pages where social proof needs more weight.

**Type B — Standard Shopify Page** (homepage, collection pages, product pages, about, contact):
Type B uses Starlite sections, not ds-*. Start from the closest completed BBI page template as a structural reference (see Step 3 readiness gate for options). Identify which Starlite section handles each piece of the Claude Design output in Step 5.

Wait for Leo to confirm the scope before moving to Step 2.

---

## Step 2 — Content Brief

Three sub-steps in order. Do not collapse them — each gates the next. The output of all three combined is the "approved content brief" that Step 2B references.

---

### Step 2.1 — ICP Voice Gate

Before writing any copy, lock the voice for this page. Ask Leo explicitly:

> **Which ICP is this page targeting — Primary (institutional Ontario: school boards, hospitals, municipalities, OECM buyers) or Secondary (SMB private-sector: Ontario commercial offices, dental/medical clinics, professional services firms)?**

Default the suggestion based on the Pre-Step item 2 reading of `docs/strategy/icp.md` and the page tips, but require Leo to confirm — don't assume.

Once confirmed, **read the matching voice rules from `docs/strategy/icp.md`** and inject them into the brief as a "Voice Lock" block. Use this format:

```
VOICE LOCK — [Primary | Secondary] ICP
- Tone: [exact tone descriptor from icp.md]
- Reading level: [grade level / formality marker from icp.md]
- Pronouns: [we / you / they conventions from icp.md]
- Forbidden words: [exact list from icp.md, e.g. "innovative", "cutting-edge", "synergy"]
- Required anchors: [trust signals + facts that MUST appear in body copy — pull from icp.md]
- CTA voice: [imperative / suggestive / formal — from icp.md]
- Phone CTA wording: [exact phrasing approved for this ICP]
```

This block is the source of truth for the rest of Step 2 and for Step 2B SEO copy. Every headline, body paragraph, and CTA in this brief must conform to it. Do not proceed to 2.2 until Leo confirms the Voice Lock is correct.

**If `icp.md` doesn't have an explicit voice rule for the field above, mark it `[derive from voice-samples.md]` and pull the closest approved sample as the calibration anchor — don't invent a rule.**

---

### Step 2.2 — Microcopy Inventory

Before writing body copy, list every microcopy element this page will need. The goal is to fix labels and CTA wording up front so they're consistent across the page (and across the site).

Output a table — Leo edits in place if he wants different wording:

| Element | Type | Wording |
|---|---|---|
| Primary CTA | Button | _e.g._ Request a Quote |
| Secondary CTA | Button | _e.g._ Call 1-800-835-9565 |
| Hero CTA | Button | (same as primary unless page-specific) |
| Quote CTA band heading | Headline | _e.g._ Ready to outfit your space? |
| Quote CTA band sub-line | Body | (pull from Trust Signal Placement Matrix per page type) |
| Quote modal heading | Modal | _e.g._ Request a Quote |
| Quote modal submit | Button | _e.g._ Send request |
| Quote form labels | Form | Name / Organization / Email / Phone / Project details |
| Quote form helper text | Form | _e.g._ We respond within 1 business day. |
| "View all" link (category pages) | Link | _e.g._ View all [Category] → |
| "Shop [Brand] products" link (brand pages) | Link | _e.g._ Shop Keilhauer products → |
| Breadcrumb separator | Layout | `>` (chevron, not slash) |
| Card CTA (product/sub-collection tiles) | Button | _e.g._ Request a Quote (NOT "Add to cart" — no checkout) |
| Phone link aria-label | a11y | _e.g._ Call Brant Business Interiors at 1-800-835-9565 |
| Empty state (if any) | Body | (e.g. for filtered results) |

**Site-wide rules — read the canonical "Microcopy lockup" section in `docs/strategy/icp.md` and apply every locked element verbatim.** Highlights (full list lives in icp.md):
- Quote CTA: **"Request a Quote"** (never "Get a Quote", "Get Pricing", "Contact Sales")
- Phone CTA: **"Call 1-800-835-9565"** (full number always — never "Call us")
- Form submit button: **"Send request"** (never "Submit")
- Form helper after submit: **"We respond within 1 business day."** (never "24 hours", "ASAP")
- Brand name in body copy: **"Brant Business Interiors"** — NEVER abbreviate to "BBI" in customer-facing copy
- Card CTA on product/sub-collection tiles: **"Request a Quote"** (never "Add to cart" — no checkout)
- Breadcrumb separator: `>` chevron (never `/`)

If this page introduces a new microcopy element not in icp.md's Microcopy lockup table, flag it to Leo and add it to icp.md before using it on the page — never let one-off variants leak in via Claude Design output.

Wait for Leo to confirm the inventory before writing body copy.

---

### Step 2.3 — Body Copy

Now write all the actual copy for the page, applying the locked Voice (2.1) and using only the approved microcopy (2.2):
- Every headline, subheadline, body paragraph, CTA label
- Written for the confirmed ICP — no tone drift mid-page
- Outcome-focused ("free design layout included" — not "we offer design services")
- Pull real BBI facts: OECM agreement number (2025-470), phone, brands carried, Ontario scope
- Include 1–2 client quotes from testimonials if available (pulled in Pre-Step)
- Weave in the competitive differentiator identified in Pre-Step
- Trust signals placed per the **Trust Signal Placement Matrix** above — do NOT scatter them; map each signal to a specific section/slot

Present the brief as a structured block Leo can scan, with the Voice Lock + Microcopy Inventory tables included at the top so the full content package is reviewable in one read. Wait for his sign-off before Step 2B.

---

## Step 2B — SEO & AEO Layer (you do this, ~3 min)

With the content brief approved, generate the full SEO + AEO package for this page before writing the Claude Design prompt.

**2B-1: SEO Title + Meta Description**
Invoke `/meta-tags-optimizer` with the page name, target keyword (from icp.md keyword lists), and the approved content brief. Output:
- SEO title: ≤60 chars, ends with `| Brant Business Interiors — a division of Office Central Inc. (OECM Supplier)`
- Meta description: 150–160 chars, outcome-focused, includes target keyword

**2B-2: Header Hierarchy**
Define H1, H2, H3 order with target keywords naturally placed. H1 = page hero headline (one only, never duplicate). H2s = section headers.

**2B-3: GEO/AEO Pass**
Invoke `/geo-content-optimizer` with the approved content brief. Apply its output to:
- Add 1–2 direct-answer sentences near the top of body copy (answers "what is X" queries that AI tools surface)
- Ensure OECM status, Ontario scope, and Canadian ownership are stated as facts (not marketing claims) in the first ~200 words — these are the citation anchors for AI engines

**2B-4: Schema Markup (page-type dependent)**

`Organization` + `LocalBusiness` JSON-LD is already handled by `ds-structured-data.liquid` — confirm it's wired in (present in `<head>` via `ds-head-assets`). Do not re-emit these for every page.

Use the table below to determine which additional schema to generate via `/schema-markup-generator`:

| Page type | Schema to generate | Notes |
|---|---|---|
| Design Services | `HowTo` | Step-by-step design process (consult → space plan → specify → install) |
| Delivery & Installation | `HowTo` | Step-by-step delivery process |
| Relocation Management | `Service` | No clear steps — describe the service scope |
| OECM Procurement (`/pages/oecm`) | `Service` | Use `GovernmentService` as the `@type` subtype |
| Any page with a visible FAQ section | `FAQPage` | In addition to the page-level schema above |
| Category pages (Seating, Desks, etc.) | `ItemList` | One `ListItem` per featured product or sub-collection tile |
| Brand dealer pages (Keilhauer, ergoCentric, etc.) | `LocalBusiness` supplement | Brand already in `Organization`; add `brand` property referencing the manufacturer |
| Customer Stories | `Review` per testimonial | One `Review` block per client quote shown on the page |
| Blog articles | `Article` + `FAQPage` (if Q&A section present) | Always include `Article`; add `FAQPage` only when the article has a visible Q&A block |
| Homepage | `WebSite` + `SiteNavigationElement` | Helps AI engines understand site structure |
| Request a Quote | `ContactPage` | Standard contact/form page schema |
| All other landing pages | None beyond base `Organization`/`LocalBusiness` | Don't force schema where it doesn't fit — bad structured data hurts more than none |

Present the full SEO + AEO package as a pasteable block. Wait for Leo's go-ahead before Step 3.

---

## Step 3 — Build HTML

### Step 3 Readiness Gate

Confirm all items are ready before writing any code:

- [ ] Brand constants confirmed (tokens read from `Design System Zips/5 - Landing Page (2)/uploads/05-tokens.css`)
- [ ] All page images identified with exact file paths (from Pre-Step item 0)
- [ ] SEO title, H1, and meta description from Step 2B locked
- [ ] Voice Lock + microcopy inventory from Steps 2.1–2.2 approved
- [ ] Trust signal slots resolved (hero subheading / trust row / quote-cta sub-line per page-type matrix — no placeholders)
- [ ] Structural template read for this page type (all in `Design System Zips/5 - PDP/src/`):
  - **Homepage:** `src/Homepage.jsx`
  - **Landing pages** (OECM, industries, brands, services, about): `src/Landing.jsx`
  - **PDP** (product pages, unbuyable or buyable): `src/ProductDetail.jsx`
  - **Collection category:** `src/CollectionCategory.jsx`
  - **Collection (sub-collection):** `src/Collection.jsx`

---

### What to read before writing

Before writing a single line of HTML, read these files in full. All paths are under `Design System Zips/5 - PDP/src/`:

1. `tokens.css` — all CSS custom property definitions
2. `bbi-components.css` — all shared component classes (required for every page)
3. The JSX template for this page type — defines section order and component tree:
   - Homepage → `Homepage.jsx`
   - Landing (OECM / industries / brands / services / about) → `Landing.jsx`
   - PDP → `ProductDetail.jsx`
   - Collection category → `CollectionCategory.jsx`
   - Collection → `Collection.jsx`
4. The page-specific CSS for this page type:
   - Homepage → `homepage.css` (`.hp-*` classes)
   - Landing → `landing.css` (`.lp-*` classes)
   - PDP → `pdp.css` (`.pd-*` classes)
   - Collection category → `collection-category.css`
   - Collection → `collection.css`

Do not invent class names or token names. Every class used must exist in these files. If a pattern isn't in the source files, it doesn't belong on the page.

---

### How to build the file

**Output file:** `previews/{slug}-draft-v1.html` (self-contained — all CSS inlined in `<style>`)

**Structure of the file:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[SEO TITLE FROM STEP 2B]</title>
  <meta name="description" content="[META DESCRIPTION FROM STEP 2B]">
  <!-- Google Fonts: JetBrains Mono for .bbi-mono elements -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* 1. Paste full contents of 05-tokens.css here — scheme-default vars on :root */
    /* 2. Paste full contents of 06-bbi-components.css here */
    /* 3. Paste full contents of page-specific CSS (07/08/09) here */
    /* 4. Any remaining layout rules specific to this page only */
  </style>
</head>
<body class="scheme-default">
  <!-- Header -->
  <!-- [sections in order per LOCKED template] -->
  <!-- Footer -->
</body>
</html>
```

**Locked header constants (always):**
- Logo: `Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png` — alt "Brant Business Interiors", height 36px
- Nav labels: Shop | Brands | Verticals | Our work | Services | About
- Header right: phone text link "Call 1-800-835-9565" + charcoal `.bbi-btn--primary` "Request a Quote" (never red)
- Header height: 72px, max-width inner 1320px, padding 0 32px

**Section rhythm (every body section except OECMBar):**
```html
<section class="bbi-section">     <!-- padding: 96px 0 -->
  <div class="bbi-container">    <!-- max-width: 1320px; padding: 0 32px; margin: 0 auto -->
    ...
  </div>
</section>
```

**Section head eyebrow rule (every section with a heading):**
```html
<div class="bbi-section-head">
  <div>
    <p class="bbi-section-head__eyebrow bbi-mono">Eyebrow text</p>
    <h2 class="bbi-section-head__title">Section heading</h2>
  </div>
</div>
```
CSS: `.bbi-section-head__eyebrow::before { content:""; display:block; width:24px; height:1px; background:var(--saleBadgeBackground); flex-shrink:0; }`

**Image slots — use `.bbi-ph` placeholders where real images aren't available:**
```html
<div class="bbi-ph" style="aspect-ratio:16/9;">
  <span class="bbi-ph__label">Description</span>
</div>
```
If a real image file exists (from Pre-Step), use `<img src="..." loading="lazy" alt="...">` instead.

**Collection page note:** Any product card grid — every card **must** have a 16:9 or 4:3 image slot at the very top. No text-only cards.

**Red density rule:** After writing each section, count red surface area. Red appears only on: hero primary CTA (`.hp-hero__cta-red`), hero eyebrow dot, section head `::before` rule, OECM badge accent, service mono numbers, testimonial quote mark SVG. Target 5–8% per screen. Never on headings, body links, or the header CTA.

---

### After writing the file

Tell Leo: "Draft written to `previews/{slug}-draft-v1.html`. Moving to Step 4 to preview."

Do not wait for approval — proceed directly to Step 4.

---

## Step 4 — Preview & Iterate

Open the preview, check it visually, fix any issues before moving to Step 5. This is Claude Code's QA pass — do it thoroughly so Step 7 is a formality.

**4a. Start preview:**

```
preview_start previews/{slug}-draft-v1.html
```

**4b. Take a screenshot and check:**

```
preview_screenshot
```

Look for:
- Header renders correctly (logo, nav labels, charcoal CTA)
- Sections appear in the correct order per the LOCKED template
- Section head eyebrows have the red `::before` rule visible
- Hero primary CTA is red; header CTA is charcoal
- No warm tones (beige/tan/cream) anywhere
- `.bbi-ph` placeholders render as striped grey boxes with labels
- Text is readable — charcoal on white, not low-contrast

**4c. Check console for errors:**

```
preview_console_logs
```

Fix any CSS parse errors or missing variable warnings before continuing.

**4d. Check responsive at 375px:**

```
preview_resize 375 812
preview_screenshot
```

Confirm: nav collapses or truncates cleanly, hero text doesn't overflow, grid columns stack correctly.

**4e. Iterate:**

For each issue found, edit the HTML file directly and re-screenshot. Repeat until the page matches the LOCKED template visually. Common fixes:
- Wrong class name → check against `06-bbi-components.css` and `07-homepage.css`
- Token not resolving → confirm the var name exists in `05-tokens.css`
- Section out of order → re-read the LOCKED JSX and reorder

**4f. Final screenshot:**

Take a full-page screenshot at 1440px width and share it with Leo before proceeding to Step 5.

```
preview_resize 1440 900
preview_screenshot
```

Wait for Leo's go-ahead before Step 5.

---

## Step 5 — Convert to Shopify

Take the HTML from Claude Design and convert it:

**For Type A:**

Start by emitting the skeleton `page.{suffix}.json` template Leo needs to create in Edit Code. Fill in `heading`, `subheading`, and `image` for `ds-page-hero` from the approved content brief; leave other settings as `{}` — they're set via the Customizer or hardcoded in the section itself.

```json
{
  "sections": {
    "announce-bar":     { "type": "ds-announce-bar",       "settings": {} },
    "site-header":      { "type": "ds-site-header",        "settings": {} },
    "page-hero":        { "type": "ds-page-hero",          "settings": { "heading": "[H1 FROM STEP 2B]", "subheading": "[SUB-HEADLINE]", "image": "" } },
    "feature-strip":    { "type": "ds-feature-strip",      "settings": {} },
    "featured-grid":    { "type": "ds-featured-grid",      "settings": {} },
    "trust-row":        { "type": "ds-trust-row",          "settings": {} },
    "quote-cta":        { "type": "ds-quote-cta",          "settings": {} },
    "quote-modal-mount":{ "type": "ds-quote-modal-mount",  "settings": {} },
    "site-footer":      { "type": "ds-site-footer",        "settings": {} }
  },
  "order": ["announce-bar","site-header","page-hero","feature-strip","featured-grid","trust-row","quote-cta","quote-modal-mount","site-footer"]
}
```

Remove unused sections from the `sections` object AND the `order` array (e.g. omit `announce-bar` if there's no active promo; omit `featured-grid` for text-heavy pages).

Then emit the `theme/layout/theme.liquid` gate addition. Read the current gate block first, then add the new suffix to it:

```liquid
{%- if template.suffix == 'oecm' or template.suffix == 'brand-dealer' or template.suffix == '[NEW-SUFFIX-HERE]' -%}
```

Tell Leo: "Open `theme/layout/theme.liquid`, find the `bbi_landing` assignment block, and add `or template.suffix == '[NEW-SUFFIX-HERE]'` to the condition. Do this before the template will render correctly."

Finally, break any custom HTML sections from the Claude Design output into Liquid snippet paste blocks. Generate a separate code block for each file Leo needs to create.

**For Type B:**
- Identify which Starlite sections to use for each piece of the design
- Call out any custom `ds-*` sections still needed
- Generate step-by-step Customizer instructions

---

## Step 6 — Shopify Admin Steps

Walk Leo through the manual work. Tell him exactly:

1. **What to create** (template, page, collection, or just customize an existing page)
2. **Where to go** — use the direct URLs below, not menu paths
3. **What to paste and where** (file name → paste block)
4. **What to fill in the Customizer** (which section, which setting, which value)

Be explicit — no assumed knowledge. Leo is doing the clicking.

**Direct Shopify Admin URLs for this store:**

| Task | URL |
|---|---|
| Create a new page | `https://admin.shopify.com/store/office-central-online/pages/new` |
| Edit pages list | `https://admin.shopify.com/store/office-central-online/pages` |
| Edit navigation menus | `https://admin.shopify.com/store/office-central-online/menus` |
| Edit code (theme files) | `https://admin.shopify.com/store/office-central-online/themes/186373570873/editor` → click "Edit code" |
| Theme Customizer | `https://admin.shopify.com/store/office-central-online/themes/186373570873/editor` |
| Create a new smart collection | `https://admin.shopify.com/store/office-central-online/collections/new` |
| Collections list | `https://admin.shopify.com/store/office-central-online/collections` |
| Files (to upload images) | `https://admin.shopify.com/store/office-central-online/content/files` |

---

### Step 6 Interconnection Block

After the basic page creation steps, emit a tailored interconnection checklist based on the page type. Look up the page type below and output **only the rows that apply**.

**Page-type interconnection matrix** (post-2026-04-25 architecture):

| Page type | Template | Nav location | Hub to update | Cross-links FROM other pages |
|---|---|---|---|---|
| BF vertical page (`/collections/business-furniture`) | `collection.category.json` | Main nav → "Shop Furniture" links here directly (no Shop Hub) | None — it IS the shop entry | Homepage (shop entry banner), every category page (footer "See all Business Furniture →") |
| BF category page (`/collections/seating`, `/collections/desks`, etc. — 9 total) | `collection.category.json` | Main nav → Shop Furniture dropdown (single column, 9 items) | BF Hub (`/collections/business-furniture`) — confirm tile exists | Industry pages (e.g. Government → Desks, Storage), brand pages (e.g. Keilhauer → Seating + Boardroom) |
| BF sub-collection (`/collections/highback-seating`, `/collections/l-shape-desks-desks`, etc. — ~68 total) | `collection.json` | Not in main nav — reached via category page tile or "View all" smart collection | Parent category page — confirm tile links here | Product pages (related products), "View all [Category]" smart collection |
| "View all" smart collection (`/collections/all-seating`, etc. — 9 total + 1 vertical) | `collection.json` | Not in nav — accessed via "View all [Category] →" button on category page | Parent category page — confirm "View all" button links here | (no other cross-links — terminal browse view) |
| Brand-filtered smart collection (`/collections/keilhauer`, `/collections/global`, `/collections/teknion`, `/collections/ergocentric`) | `collection.json` (vendor-filtered) | Not in nav — accessed via brand dealer page button | Parent brand dealer page — confirm "Shop [Brand] products →" button links here | Product pages from that vendor |
| Industry page (`/pages/healthcare`, `/pages/education`, etc.) | Landing page template | Main nav → Industries dropdown | Industries hub (`/pages/industries`) — add a card | Homepage (industries strip), relevant BF category pages, OECM page |
| Industries hub (`/pages/industries`) | Landing page template | Main nav (top-level "Industries") | None — it IS the hub | Homepage (industries strip), every industry page (cross-link back) |
| Brand dealer page (`/pages/brands-keilhauer`, etc.) | Landing page template | Main nav → Brands dropdown | Brands hub (`/pages/brands`) — add a card | Relevant BF category pages (e.g. Keilhauer card on Seating page), brand-filtered smart collection (button) |
| Brands hub (`/pages/brands`) | Landing page template | Main nav (top-level "Brands") | None — it IS the hub | Homepage (optional brands row), every brand page (cross-link back) |
| Service page (`/pages/design-services`, `/pages/delivery`, `/pages/relocation`, `/pages/oecm`) | Landing page template | Main nav → Services dropdown | About page or footer | Homepage (services strip), relevant industry pages (OECM linked from Healthcare/Education/Government) |
| About / Contact / Our Work | Landing page template | Footer + nav About dropdown | None | Homepage, every quote CTA |
| Customer Stories (`/pages/customer-stories`) | Landing page template (industry-filter variant — must include Review JSON-LD per testimonial via `/schema-markup-generator`) | Footer + nav About dropdown | None | Homepage (testimonials section: "Read customer stories →"), every industry page ("See [Industry] customer stories →" filtered link), `/pages/quote`, About page, Contract Pricing |
| FAQ (`/pages/faq`) | Landing page template (FAQ variant — must include FAQPage JSON-LD via `/schema-markup-generator`) | Footer + nav About dropdown | None | Every product page (sticky "Questions?" link), every service page, footer |
| Request a Quote (`/pages/quote`) | Landing page template (form-heavy variant) | Main nav right-side CTA button | None — it IS the conversion endpoint | Every product page, every category page (phone CTA block), every industry page, every service page, every sub-collection footer |
| Contract Pricing (`/pages/contract-pricing`) ⚠️ _not in site-architecture-2026-04-25.md — confirm with Leo before building_ | Landing page template (form-heavy) | Footer / industry-page link | None | Industry pages, OECM page |
| Blog / Resources hub (`/blogs/news`) | Custom blog template | Main nav (optional "Resources") + footer | None — it IS the hub | Footer link, every article cross-links back |
| Blog article (`/blogs/news/[handle]`) | Article template (must include Article + FAQPage JSON-LD via `/schema-markup-generator`) | Not in nav — reached via Resources hub | Resources hub | Related category page, related industry page, `/pages/quote` CTA at bottom |
| Custom 404 (`/404`) | `404.json` | N/A — system page | N/A | (terminal — but links OUT to 4 top categories + search + phone) |
| Policies (`/policies/*`) | Auto-generated, content-only | Footer (Shopify standard) | N/A | Footer link only |
| Campaign / one-off landing | Landing page template | Not in main nav (use footer or homepage banner) | Homepage — add a banner CTA or seasonal link | OECM page, Contract Pricing page |

**Emit this checklist for every page:**

- [ ] **Template suffix** — assigned correctly in Shopify Admin → Pages → Theme template (e.g. `page.healthcare`, `collection.category` for category pages, `collection` for sub-collections)
- [ ] **Page handle** — matches expected URL slug (e.g. `healthcare` → `/pages/healthcare`). Verify in Pages → Edit URL and handle
- [ ] **Main nav** — go to Admin → Navigation → Main menu → edit the correct dropdown, add link with label and URL (skip for sub-collections, smart collections, and system pages — see matrix)
- [ ] **Footer nav** — if this is a Services, About, FAQ, Contact, or Policies page: add it to the Footer menu under the right column
- [ ] **Hub page updated** — go to the hub page (listed above for this page type) in Admin → Pages → edit the page's content/Customizer to add a card or link for this page
- [ ] **Breadcrumb** — for shop pages: confirm 4-level breadcrumb (Home > Shop Furniture > [Category] > [Sub-collection]) reflects the current path. BreadcrumbList JSON-LD should already be live; just verify.
- [ ] **"View all" button (category pages only)** — confirm "View all [Category] →" button at top of tile grid links to the smart collection (e.g. `/collections/all-seating`). If the smart collection doesn't exist yet, create it (Admin → Products → Collections → Create collection → Smart, condition: tag equals `category:[name]`).
- [ ] **Brand-filtered button (brand pages only)** — confirm "Shop [Brand] products →" button links to the vendor-filtered smart collection (`/collections/keilhauer`, `/collections/global`, `/collections/teknion`, `/collections/ergocentric`). If missing, create as smart collection with condition: vendor equals `[Brand]`.
- [ ] **SEO fields** — in Admin → Pages → [this page] → scroll to Search engine listing preview → set Page title and Meta description from Step 2B
- [ ] **Cross-links wired** — visit 2–3 existing live pages (listed above for this page type) and confirm they contain a link TO this new page; if not, flag for Leo to add

---

## Step 7 — QA Checklist

After Leo says "it's live in the draft theme", walk him through these 9 checks. Mark the page `[✓]` on the master checklist only when all 9 pass.

- [ ] Mobile layout at 375px — nothing broken or overflowing
- [ ] All links resolve — no `#` placeholders from unbuilt pages
- [ ] Quote modal opens from every CTA and closes correctly
- [ ] `tel:` link is tappable on mobile
- [ ] View Source → search `application/ld+json` — structured data present
- [ ] Page title set in Shopify → Pages → SEO section
- [ ] Meta description set (150–160 chars, outcome-focused)
- [ ] Photo alt text meaningful (not empty, not filename)
- [ ] Run `/on-page-seo-auditor` on the draft theme preview URL — resolve any errors before marking done

**Interconnection checks (must pass before marking done):**
- [ ] Nav link — click through the correct main nav dropdown and confirm it lands on this page (skip for sub-collections, smart collections, system pages)
- [ ] Hub page card/link — visit the hub page for this page type and confirm a card or link pointing here is live
- [ ] Cross-link from at least one existing page — visit one of the cross-link candidates from Step 6 and confirm the link is present and resolves correctly
- [ ] Collection handle (shop pages only) — confirm URL slug `/collections/{handle}` matches the template suffix exactly (`collection.category.{handle}` for category pages, `collection.{handle}` for sub-collections)
- [ ] Breadcrumb (shop pages only) — for category pages: Home > Shop Furniture > [Category]. For sub-collections: Home > Shop Furniture > [Category] > [Sub-collection]. Confirm BreadcrumbList JSON-LD reflects this.
- [ ] "View all" button (category pages only) — click "View all [Category] →" and confirm it lands on the populated smart collection (`/collections/all-seating`, etc.) with products visible
- [ ] Brand-filtered button (brand pages only) — click "Shop [Brand] products →" and confirm it lands on the vendor-filtered smart collection with that brand's products visible
- [ ] FAQ schema (FAQ + article pages) — view source, search `"@type":"FAQPage"`, confirm structured data matches the visible Q&A content

**Design-system conformance (must pass on every new page):**
- [ ] Red density 5–8% — eyeball the rendered page; flag if a hero, badge cluster, or CTA stack pushes past 8%
- [ ] No beige / tan / cream / sand anywhere — scan card backgrounds, footers, alternate-section bands
- [ ] All headings render in `--headingColor` (charcoal), never red
- [ ] All body links render in `--linkColor` (charcoal-derived), never red
- [ ] Focus rings visible on every interactive element against white canvas (≥3:1)
- [ ] Maple-leaf icon present wherever Canadian-Owned / Made-in-Canada copy appears
- [ ] Quote-request CTA visually outranks every secondary action on its block (BBI's primary conversion pattern)
- [ ] Product cards (any grid) have 16:9 image slot at top — no exceptions
- [ ] Logo is new "Brant ✱ BI | Business Interiors" wordmark from `uploads/14-bbi-logo-v2.png` — not old version
- [ ] Nav labels are: Shop | Brands | Verticals | Our work | Services | About — not old labels
- [ ] Header CTA ("Request a Quote") is charcoal, not red — red only on hero primary CTA (`hp-hero__cta-red`)
- [ ] Every body section uses `.bbi-section` (padding 96px 0) + `.bbi-container` (max-width 1320px, padding 0 32px) wrappers
- [ ] Every section head eyebrow has red `::before` rule (24px × 1px, `var(--saleBadgeBackground)`)
- [ ] Class names match canonical system — check the prefix for this page type and confirm every class traces back to a source file:
  - Shared: `.bbi-*` (from `bbi-components.css`)
  - Homepage: `.hp-*` (from `homepage.css`)
  - Landing pages: `.lp-*` (from `landing.css`)
  - PDP: `.pd-*` (from `pdp.css`)
  - No invented class names allowed on any page type
- [ ] Homepage only: no CTA band between Testimonials and Footer (`.bbi-cta-section` is for landing pages and PDPs, not homepage)
- [ ] Landing pages: closer band uses `.bbi-cta-section.scheme-inverse` (shared component, not `.lp-*`)
- [ ] PDP (unbuyable): commerce panel shows quote CTA, not "Add to cart" — `data.commerce.buyable = false` pattern
- [ ] PDP: gallery is 4:5 aspect ratio on desktop, 1:1 on mobile; thumb strip is 6-column grid

Once all checks pass, update `previews/bbi-planning-hub.html` — find the entry for this page in the `PAGES` array and set its status to `done`. This keeps the planning hub accurate as the source of truth for what's built vs. what's left.

---

## Rules

- **Always run all 7 steps in order** — no shortcuts, even for simple pages
- **Never rebuild** anything in the ds-* inventory — reuse it
- **Suppress Starlite chrome only on Type A** — Type B uses it
- **Never publish the dev theme** — everything stays in "BBI Landing Dev" draft
- **Never delete products** — archive or unpublish; prefer unpublish when sold-history exists
- **Wait for Leo's go-ahead** between Pre-Step, Steps 1, 2, 2B, and after Step 4 screenshot — don't run the whole flow autonomously
- **Flag unbuilt pages** as `[placeholder]` in Step 1 so Leo can decide which to build next
- **SEO/AEO is non-negotiable** — Step 2B runs on every page, no skipping even for simple pages
- **Read before writing** — always read the LOCKED source files (tokens, components, LOCKED JSX) before writing any HTML in Step 3. Never invent classes or tokens.
