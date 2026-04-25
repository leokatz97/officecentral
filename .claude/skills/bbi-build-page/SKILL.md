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

**AI page-image library:** `data/page-images/{page-slug}/` — pre-generated 16:9 hero images for every BBI landing page, produced by `scripts/generate-page-images.py` (fal.ai flux/schnell). Two files per page:
- `{slug}-product.jpg` — featured SKU in a polished commercial setting (Type A: product hero)
- `{slug}-space.jpg` — full room scene capturing the page atmosphere (Type B: space hero)
Pages where a real OCI photo already covers the space concept are flagged `SOURCE=OCI_PHOTO` in `data/reports/generated-page-images-YYYY-MM-DD.csv` — use the OCI photo for that slot instead.
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

1. **Read the site build checklist** at `previews/bbi-site-build-checklist.html` — find the entry matching the page name in the `PAGES` array. Extract its `tips` array. These are the pre-agreed best-practice tips for this exact page: ICP target, hero photo, CTA priority, copy angle, SEO keywords, trust signals. They are your primary brief.

2. **Read ICP & voice** at `docs/strategy/icp.md` — confirm which ICP (Primary = institutional Ontario, Secondary = SMB) this page targets and apply the matching voice calibration. Check the keyword lists for any SEO terms relevant to this page.

3. **Read voice samples** at `docs/strategy/voice-samples.md` — reference the 5 approved rewrites so copy tone in the Step 2 brief matches what's already been signed off.

4. **Check photo library** at `data/oci-photos/catalog.json` — the checklist tips usually name specific photos. Confirm the filename exists before citing it in Step 3's Claude Design prompt.

Summarize the loaded brief to Leo in one short block — tips, ICP target, recommended hero photo — and confirm before Step 1. This becomes the source of truth for all copy and design decisions on this page.

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

Present the brief as a structured block Leo can scan. Wait for his sign-off before Step 3.

---

## Step 3 — Claude Design Prompt

**Before writing the prompt:** check `data/page-images/{page-slug}/` for pre-generated hero images:
- If `{slug}-product.jpg` exists → reference it as the hero/product image in the design prompt and tell Leo to attach it to Claude Design.
- If `{slug}-space.jpg` exists → use it as the background/space image.
- If the slot is `SOURCE=OCI_PHOTO` (per the manifest CSV) → use the OCI photo filename from `data/oci-photos/` instead.
- If neither exists → note "no pre-generated image available — Claude Design will need to generate or you can run `python3 scripts/generate-page-images.py --limit=1 --live` first."

Emit the exact prompt for Leo to paste into claude.ai/design. Use this template — fill in the bracketed parts:

```
Design a [PAGE TYPE] for Brant Business Interiors (BBI).

Brand tokens:
Background: #F7F8FA | Cards: #FFFFFF | Text: #0B0B0C
Accent: #D4252A (use sparingly) | Border: #DEE1E6
Font: system-ui, Geist, Inter — sans-serif only, no serif

Tone: B2B institutional. Clean. No fluff. Ontario commercial furniture dealer.
Reference: Match the structure of the BBI OECM landing page — dark header,
full-width hero with right-side photo, feature strip, card grid, CTA band.

Page: [NAME]
Purpose: [PURPOSE IN ONE LINE]

Sections (in order):
1. [SECTION] — [CONTENT]
2. [SECTION] — [CONTENT]
...

Mobile-first. Output clean, self-contained HTML + CSS only.
Use CSS custom properties matching these names where possible:
--bbi-ink, --bbi-paper, --bbi-accent, --bbi-gray-200, --bbi-font-sans
```

End your message with:
> → Go to claude.ai/design, paste the prompt above, build the page, then paste the HTML output back here.

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

## Step 7 — QA Checklist

After Leo says "it's live in the draft theme", walk him through these 8 checks. Mark the page `[✓]` on the master checklist only when all 8 pass.

- [ ] Mobile layout at 375px — nothing broken or overflowing
- [ ] All links resolve — no `#` placeholders from unbuilt pages
- [ ] Quote modal opens from every CTA and closes correctly
- [ ] `tel:` link is tappable on mobile
- [ ] View Source → search `application/ld+json` — structured data present
- [ ] Page title set in Shopify → Pages → SEO section
- [ ] Meta description set (150–160 chars, outcome-focused)
- [ ] Photo alt text meaningful (not empty, not filename)

---

## Rules

- **Always run all 7 steps in order** — no shortcuts, even for simple pages
- **Never rebuild** anything in the ds-* inventory — reuse it
- **Suppress Starlite chrome only on Type A** — Type B uses it
- **Never publish the dev theme** — everything stays in "BBI Landing Dev" draft
- **Never delete products** — archive or unpublish; prefer unpublish when sold-history exists
- **Wait for Leo's go-ahead** between Pre-Step, Steps 1, 2, 3, and 5 — don't run the whole flow autonomously
- **Flag unbuilt pages** as `[placeholder]` in Step 1 so Leo can decide which to build next
