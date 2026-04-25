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
- **Products:** task seating, desks & workstations, storage & filing, collaboration, acoustic pods

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

**0. Inventory pre-generated images** — use the table below to find the exact subfolder for this page, then list the files inside it:

| Page name (as Leo says it) | Image folder |
|---|---|
| homepage | `data/page-images/homepage/` |
| global-teknion | `data/page-images/global-teknion/` |
| ergocentric | `data/page-images/ergocentric/` |
| keilhauer | `data/page-images/keilhauer/` |
| task-seating | `data/page-images/task-seating/` |
| desks | `data/page-images/desks/` |
| storage | `data/page-images/storage/` |
| collaboration | `data/page-images/collaboration/` |
| acoustic-pods | `data/page-images/acoustic-pods/` |
| home-office | `data/page-images/home-office/` |
| healthcare | `data/page-images/healthcare/` |
| education | `data/page-images/education/` |
| government | `data/page-images/government/` |
| non-profit | `data/page-images/non-profit/` |
| professional-services | `data/page-images/professional-services/` |
| design-services | `data/page-images/design-services/` |
| verticals-hub | `data/page-images/verticals-hub/` |
| collections-hub | `data/page-images/collections-hub/` |

Pattern inside each folder: `{slug}-product.jpg` (product hero) and `{slug}-space.jpg` (room scene, where it exists). If the page name doesn't match any row above, check `data/page-images/` directly for a matching folder before proceeding.

Also check the manifest CSV at `data/reports/generated-page-images-YYYY-MM-DD.csv` — if a slot is `SOURCE=OCI_PHOTO`, use the matching OCI photo from `data/oci-photos/catalog.json` for that slot instead.

**1. Read the site build checklist** at `previews/bbi-site-build-checklist.html` — find the entry matching the page name in the `PAGES` array. Extract its `tips` array. These are the pre-agreed best-practice tips for this exact page: ICP target, hero photo, CTA priority, copy angle, SEO keywords, trust signals. They are your primary brief.

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
- Which sections to use and in what order
- What content he needs to gather before starting (photos, logos, client names, product specs, etc.)
- Which links on this page point to pages not yet built — flag as `[placeholder]`

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
- All pages: LocalBusiness + Organization JSON-LD is already handled by `ds-structured-data.liquid` — confirm it's wired in.
- Service pages (Design Services, Delivery & Install, Relocation): invoke `/schema-markup-generator` → generate HowTo or Service JSON-LD.
- Pages with an FAQ section: invoke `/schema-markup-generator` → generate FAQPage JSON-LD.
- Product/category pages: invoke `/schema-markup-generator` → generate Product or ItemList JSON-LD.

Present the full SEO + AEO package as a pasteable block. Wait for Leo's go-ahead before Step 3.

---

## Step 3 — Claude Design Prompt

### Step 3 Readiness Gate

Confirm all four items are ready before generating the prompt. Do not proceed if any are missing.

- [ ] Brand constants block populated (hex codes, font, spacing, border-radius)
- [ ] All page images identified with exact file paths (from Pre-Step item 0)
- [ ] SEO title, H1, and meta description from Step 2B ready to paste
- [ ] Reference page identified (`page.oecm.json` or `page.brand-dealer.json`) for Leo to attach

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
- Break the HTML into a JSON template + Liquid section files
- Generate paste blocks for each file Leo needs to create in Shopify Admin → Edit Code
- Include the one-line addition to `theme/layout/theme.liquid`'s `bbi_landing` gate for the new template suffix

**For Type B:**
- Identify which Starlite sections to use for each piece of the design
- Call out any custom `ds-*` sections still needed
- Generate step-by-step Customizer instructions

---

## Step 6 — Shopify Admin Steps

Walk Leo through the manual work. Tell him exactly:

1. **What to create** (template, page, collection, or just customize an existing page)
2. **Where to go** in Shopify Admin (specific menu paths)
3. **What to paste and where** (file name → paste block)
4. **What to fill in the Customizer** (which section, which setting, which value)

Be explicit — no assumed knowledge. Leo is doing the clicking.

---

### Step 6 Interconnection Block

After the basic page creation steps, emit a tailored interconnection checklist based on the page type. Look up the page type below and output **only the rows that apply**.

**Page-type interconnection matrix:**

| Page type | Nav location | Hub to update | Cross-links FROM other pages |
|---|---|---|---|
| Collection page | Main nav → Catalog dropdown | Collections hub (`/collections`) — add a card | Homepage (featured categories), Product page template |
| Vertical page | Main nav → Industries dropdown | Industries hub (`/pages/industries`) — add a card | Relevant collection pages (e.g. Healthcare → Desks, Task Seating) |
| Service page | Main nav → Services dropdown | About page (`/pages/about`) — add a cross-link | Homepage (services strip), relevant vertical pages |
| Brand dealer page | Main nav → Brands dropdown | Brands hub (`/pages/brands`) — add a card | Relevant collection pages (products that brand supplies) |
| Campaign / landing | Not in main nav (use footer or CTA) | Homepage — add a banner CTA or seasonal link | OECM page, Contract Pricing page |
| Hub page | Main nav (top-level) | None — it IS the hub | All child pages must link back to this hub |

**Emit this checklist for every page:**

- [ ] **Template suffix** — assigned correctly in Shopify Admin → Pages → Theme template (e.g. `page.healthcare`)
- [ ] **Page handle** — matches expected URL slug (e.g. `healthcare` → `/pages/healthcare`). Verify in Pages → Edit URL and handle
- [ ] **Main nav** — go to Admin → Navigation → Main menu → edit the correct dropdown, add link with label and URL
- [ ] **Footer nav** — if this is a Services, About, or Contact page: add it to the Footer menu under the right column
- [ ] **Hub page updated** — go to the hub page (listed above for this page type) in Admin → Pages → edit the page's content/Customizer to add a card or link for this page
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

**Interconnection checks (4 additional — must pass before marking done):**
- [ ] Nav link — click through the correct main nav dropdown and confirm it lands on this page
- [ ] Hub page card/link — visit the hub page for this page type and confirm a card or link pointing here is live
- [ ] Cross-link from at least one existing page — visit one of the cross-link candidates from Step 6 and confirm the link is present and resolves correctly
- [ ] Collection handle (collection pages only) — confirm URL slug `/collections/{handle}` matches the template suffix `collection.{handle}` exactly

Once all 13 checks pass, update `previews/bbi-site-build-checklist.html` — find the entry for this page in the `PAGES` array and set its status to `done`. This keeps the checklist accurate as the source of truth for what's built vs. what's left.

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
