---
name: bbi-build-page
description: >
  Explicit slash command for building Brant Business Interiors (BBI) Shopify pages.
  Runs Leo's full 7-step workflow coordinating Claude Code, Claude Design
  (claude.ai/design), and Shopify Admin.

  Invoked as `/bbi-build-page [page name]` — e.g. `/bbi-build-page homepage`,
  `/bbi-build-page contact`, `/bbi-build-page healthcare`. Parse the page name
  from the arguments.

  Do NOT auto-trigger on general page-building requests, mentions of Shopify,
  or phrases like "build a page". Only fire when Leo explicitly invokes
  `/bbi-build-page`.
---

# BBI Build Page

Leo's canonical workflow for building a new BBI Shopify page. Seven steps, always in order, no skipping — even for simple pages.

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

## Brand Design Tokens

Exact CSS variables from `theme/assets/ds-landing.css`. Use these in every Claude Design prompt.

```
--bbi-ink: #0B0B0C           (primary text, button fills)
--bbi-paper: #F7F8FA         (page background)
--bbi-paper-raised: #FFFFFF  (card/panel surface)
--bbi-accent: #D4252A        (Brant red — use sparingly)
--bbi-gray-200: #DEE1E6      (default border)
--bbi-gray-500: #6F7580      (meta/caption text)
--bbi-gray-700: #363A42      (body/secondary text)
--bbi-font-sans: system-ui, "Geist", "Inter", Helvetica, sans-serif
```

**Tone:** B2B institutional. Outcome-focused. No fluff. No serif. No emoji on the site.

Reference templates: `theme/templates/page.oecm.json` and `theme/templates/page.brand-dealer.json` — match their section order and content style when in doubt.

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

**AI page-image library:** pre-generated 16:9 hero images for every BBI landing page, produced by `scripts/generate-page-images.py` (fal.ai flux/schnell). See slug→folder table in Pre-Step.
To (re)generate: `python3 scripts/generate-page-images.py --live` (or `--limit=3 --live` for a smoke test).

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
- **(c)** Proceed with a solid `--bbi-gray-200` placeholder — not ideal for first-impression pages, but acceptable for rough drafts

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

Write all copy for the page:
- Every headline, subheadline, body paragraph, CTA label
- Written for B2B institutional procurement buyers
- Outcome-focused ("free design layout included" — not "we offer design services")
- Pull real BBI facts: OECM agreement number (2025-470), phone, brands carried, Ontario scope
- Include 1–2 client quotes from testimonials if available (pulled in Pre-Step)
- Weave in the competitive differentiator identified in Pre-Step

Present the brief as a structured block Leo can scan. Wait for his sign-off before Step 2B.

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

## Step 3 — Claude Design Prompt

### Step 3 Readiness Gate

Confirm all four items are ready before generating the prompt. Do not proceed if any are missing.

- [ ] Brand constants block populated (hex codes, font, spacing, border-radius)
- [ ] All page images identified with exact file paths (from Pre-Step item 0)
- [ ] SEO title, H1, and meta description from Step 2B ready to paste
- [ ] Reference page identified for Leo to attach — pick the most structurally similar completed page:
  - `page.oecm.json` → service / trust / procurement pages
  - `page.brand-dealer.json` → dealer / brand showcase pages
  - As more pages complete QA, add their template handles here so Leo always has the closest match

---

**Before pasting into Claude Design, tell Leo to attach these files:**

1. **Page images** (exact paths from Pre-Step image inventory):
   - `data/page-images/{slug}/{slug}-product.jpg` → hero / product showcase image
   - `data/page-images/{slug}/{slug}-space.jpg` → full-room background (if it exists)
   - Or the OCI photo listed in the Pre-Step summary if that slot is `SOURCE=OCI_PHOTO`

2. **Reference page HTML** — attach the rendered HTML of a completed BBI page as a structural anchor. Use the source of `page.oecm.json` or `page.brand-dealer.json`. Tell Claude Design: "Match the component structure and visual rhythm of the attached reference page — dark header, full-width hero, feature strip, card grid, CTA band."

> These are the images Claude Design must use — do not let it generate placeholder imagery.

---

**Collection page note:** If this page includes a product card grid (desks, seating, storage, any category page), every card **must** have a 16:9 or 4:3 image slot at the top — `object-fit: cover`. Do not build text-only cards. The SECONDARY PRODUCT ROW standard in the prompt enforces this; confirm it is present before submitting.

Emit the exact prompt for Leo to paste into claude.ai/design. Use this template — fill in the bracketed parts:

```
Design a [PAGE TYPE] for Brant Business Interiors (BBI).

Brand constants (use exactly — do not invent):
Background: #F7F8FA | Card surface: #FFFFFF | Primary text: #0B0B0C
Accent (sparingly): #D4252A | Border: #DEE1E6
Secondary text: #363A42 | Meta/caption: #6F7580
Font: system-ui, "Geist", "Inter", Helvetica, sans-serif — no serif, no display fonts
Spacing scale: 8px base unit (8 / 16 / 24 / 32 / 48 / 64 / 96px)
Border-radius: 4px on cards, 2px on buttons

Tone: B2B institutional. Clean. No fluff. Ontario commercial furniture dealer.
Reference: Match the component structure and visual rhythm of the attached reference page —
dark header, full-width hero, feature strip, card grid, CTA band.

Trust signals (weave into copy naturally — not as a separate section):
- OECM Supplier Partner, Agreement 2025-470 — Ontario institutional buyers can purchase without open tender
- Canadian-owned business serving Ontario
- Authorized dealer: ergoCentric — add 🍁 maple leaf icon near any "Canadian-made" claims
- Phone: 1-800-835-9565 — must appear in the header and at least one in-body CTA

Images: I am attaching [N] image(s). Use them as-is — do NOT generate placeholder imagery.
- [{slug}-product.jpg] → hero / product showcase image
- [{slug}-space.jpg] → full-room background / space atmosphere (if attached)

Page: [NAME]
Purpose: [PURPOSE IN ONE LINE]

SEO title: [TITLE FROM STEP 2B]
Meta description: [DESCRIPTION FROM STEP 2B]
H1: [H1 FROM STEP 2B HEADER HIERARCHY]

Sections (in order):
1. [SECTION] — [CONTENT]
2. [SECTION] — [CONTENT]
...

Mobile-first. Output clean, self-contained HTML + CSS only.
Use CSS custom properties matching these names where possible:
--bbi-ink, --bbi-paper, --bbi-accent, --bbi-gray-200, --bbi-font-sans

SECONDARY PRODUCT ROW (any card grid showing collection products):
Every product card MUST have an image slot at the top before any text content.
Image slot: 16:9 or 4:3 aspect ratio, width: 100%, object-fit: cover.
In this prototype use the attached product image or a solid --bbi-gray-200 placeholder — do NOT generate decorative imagery.
Card structure (top to bottom): image slot → product name → short descriptor → CTA button.
```

End your message with:
> → Go to claude.ai/design, attach the files listed above, paste the prompt, build the page, then paste the HTML output back here.

Then wait. Do not proceed until Leo pastes HTML.

---

## Step 4 — Leo Runs Claude Design

Leo builds the page in claude.ai/design using your prompt and pastes the full HTML output back into the session. You do nothing here — just wait.

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

Once all checks pass, update `previews/bbi-planning-hub.html` — find the entry for this page in the `PAGES` array and set its status to `done`. This keeps the planning hub accurate as the source of truth for what's built vs. what's left.

---

## Rules

- **Always run all 7 steps in order** — no shortcuts, even for simple pages
- **Never rebuild** anything in the ds-* inventory — reuse it
- **Suppress Starlite chrome only on Type A** — Type B uses it
- **Never publish the dev theme** — everything stays in "BBI Landing Dev" draft
- **Never delete products** — archive or unpublish; prefer unpublish when sold-history exists
- **Wait for Leo's go-ahead** between Pre-Step, Steps 1, 2, 2B, 3, and 5 — don't run the whole flow autonomously
- **Flag unbuilt pages** as `[placeholder]` in Step 1 so Leo can decide which to build next
- **SEO/AEO is non-negotiable** — Step 2B runs on every page, no skipping even for simple pages
- **One-shot rule** — the Claude Design prompt must pass all 4 gate items before submission. Never submit a partial prompt intending to revise; credits are spent per generation, not per session
