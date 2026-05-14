# Ideas Backlog — Explore Later

Parking lot for Shopify / BBI improvement ideas. Not active tasks — come back to research and scope when ready.

---

## 1. Shopify AI Toolkit
Research what's in Shopify's native AI toolkit (Sidekick, Magic, product description AI, etc.) and which pieces apply to BBI.

- Notes:

## 2. Add trust badges
Identify where (PDP, cart, checkout) and which badges matter for B2B institutional Canadian buyers (Made in Canada, warranty, secure checkout, BBB, etc.).

- Notes:

## 3. Capture customers on Shopify
Lead-capture mechanisms: quote requests, email capture popups, account creation incentives, exit intent, gated spec sheets.

- Notes:

## 4. Product-specific FAQs
FAQ blocks on PDPs tailored to each product category (chairs vs. desks vs. acoustic pods vs. storage). Reduces support load and boosts SEO.

- Notes:

## 5. Fix shipping info — need timelines
Surface delivery/installation timelines directly on PDPs and cart. Cross-reference `docs/workflows/delivery-installation-shipping-setup.md`.

- Notes:

## 6. Customer logos, testimonials, photos
Social proof assets — collect logos of institutional clients, written testimonials, and install photos. Cross-reference the OCI photo library (48 real project photos catalogued at `data/oci-photos/catalog.json`).

- Notes:

## 7. Anatomy of a high-performing product page
Research task. Audit top B2B furniture PDPs and distill what drives conversion. Competitors already documented in `reference_competitor_sites` memory (POI, ABCO/Source, Grand & Toy).

- Notes:

## 8. fal.ai image generation — landing pages & collection pages
Use fal.ai flux/schnell to generate hero and section images for all 27 BBI pages (collection pages + landing pages + vertical pages). Two image types per page:

**Type A — Top product hero:** Take the #1 featured SKU for each collection (already defined in checklist), generate a polished hero-scale image of that product in a relevant setting (matches the collection's ICP and tone).

**Type B — Space/environment hero:** Generate a full room scene for each page that captures the page's vibe — e.g. a bright boardroom for Collaboration, a clinical hallway for Healthcare, a focused home office nook for Home Office. These are page-level atmosphere shots, not product shots.

**Output structure:**
```
data/page-images/
  homepage/
  task-seating/
  desks/
  storage/
  collaboration/
  home-office/
  acoustic-pods/
  healthcare/
  education/
  government/
  non-profit/
  professional-services/
  design-services/
  our-work/
  collections-hub/
  verticals-hub/
  (+ brand pages: keilhauer, global-teknion, ergocentric)
```

**Script approach:** Follow the same pattern as `scripts/generate-product-images.py` — stdlib only, `--live`/`--limit` flags, manifest CSV, audit log, resume-safe.

**Pages + their top SKU + space concept** (from `previews/bbi-site-build-checklist.html`):

| Page | Route | Top SKU / product hero | Space concept |
|---|---|---|---|
| Homepage | / | L-Shape Desk or ObusForme chair | Executive open-plan office, bright, Canadian |
| Task Seating | /collections/task-seating | ObusForme Comfort High Back 1240-3 | Modern ergonomic office, multiple desks/chairs |
| Desks & Workstations | /collections/desks | L-Shape Desk & Hutch | Corner executive office, natural light |
| Storage & Filing | /collections/storage | Premium Series Lateral File 9300 | Records room / institutional filing corridor |
| Collaboration | /collections/collaboration | Boardroom table + Keilhauer chairs | Formal boardroom, Canadian institution |
| Home Office | /collections/home-office | Compact L-shape sit-stand desk | Bright home office nook, residential feel |
| Acoustic Pods | /collections/acoustic-pods | Privacy pod unit | Open-plan office with pod installed |
| Healthcare | /pages/healthcare | Bariatric chair or healthcare desk | Clinical hallway or nursing station |
| Education | /pages/education | Training table + chairs | Classroom or library study space |
| Government | /pages/government | Workstation panel system | Government open-plan office |
| Non-Profit | /pages/non-profit | Task chair + simple desk | Warm community office |
| Professional Services | /pages/professional-services | Sit-stand desk | Modern professional services office |
| Design Services | /pages/design-services | Space planning concept render | Open-plan layout under construction/planning |
| Our Work | /pages/our-work | (use OCI photos — don't generate) | — |
| Collections Hub | /collections | Mixed hero of top 3 categories | Wide-angle modern office, multiple zones |
| Verticals Hub | /pages/verticals | Sector collage | Institutional multi-sector collage |
| Keilhauer brand | /pages/brands-keilhauer | Keilhauer boardroom chair | Upscale Toronto boardroom |
| Global/Teknion brand | /pages/brands-global-teknion | Panel workstation system | Corporate open-plan, systems furniture |
| ergoCentric brand | /pages/brands-ergocentric | ergoCentric task chair | Ergonomics-focused modern office |

**Reference:** `previews/bbi-site-build-checklist.html` for per-page hero specs · `data/oci-photos/catalog.json` for existing real photos (use real OCI photos where available before generating) · `scripts/generate-product-images.py` for the fal.ai pattern to follow.

**Also included in scope (slots 1–6 identified 2026-04-24):**

**Slot 1 — Collection hub tiles** (`/collections` overview): 6 square tiles (one per category). Missing: Desks, Storage, Home Office — OCI covers the rest.

**Slot 2 — Industry hub tiles** (`/pages/industries`): 5 sector tiles. OCI covers Healthcare, Education, Government. Generate: Non-Profit, Professional Services.

**Slot 3 — Brand hub tiles** (`/pages/brands`): 3 premium lifestyle shots — Keilhauer, Global/Teknion, ergoCentric.

**Slot 4 — Homepage featured product cards**: 3 SKU hero cards below the main hero (ObusForme chair, L-Shape Desk, Acoustic Pod). Styled close-up with context, different from collection hero.

**Slot 5 — Service page mid-section images**: 2–3 section break images for Design Services, Delivery + Install, Relocation Management (beyond just the page hero).

**Slot 6 — OECM page hero** (`/pages/oecm`): One institutional hero — government procurement / public sector workspace credibility shot.

**Output folder structure (full):**
```
data/page-images/
  homepage/              → hero-product.jpg, hero-space.jpg, featured-card-chair.jpg, featured-card-desk.jpg, featured-card-pods.jpg
  task-seating/          → hero-product.jpg, hero-space.jpg
  desks/                 → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  storage/               → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  collaboration/         → hero-product.jpg, hero-space.jpg
  home-office/           → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  acoustic-pods/         → hero-product.jpg, hero-space.jpg
  healthcare/            → hero-product.jpg, hero-space.jpg
  education/             → hero-product.jpg, hero-space.jpg
  government/            → hero-product.jpg, hero-space.jpg
  non-profit/            → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  professional-services/ → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  design-services/       → hero-product.jpg, hero-space.jpg, section-planning.jpg, section-reveal.jpg
  delivery/              → hero-space.jpg, section-install.jpg, section-deliver.jpg
  relocation/            → hero-space.jpg, section-move.jpg
  oecm/                  → hero-space.jpg
  collections-hub/       → hero-space.jpg
  industries-hub/        → hero-space.jpg
  brands-hub/            → hero-space.jpg
  keilhauer/             → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  global-teknion/        → hero-product.jpg, hero-space.jpg, hub-tile.jpg
  ergocentric/           → hero-product.jpg, hero-space.jpg, hub-tile.jpg
```

- Notes:

## 9. SEO blog post featured images
Each blog post in the SEO content strategy needs a 1200×630 featured image. Acoustic pods, ergonomics, OECM procurement guides, and workspace trends are the priority topics (per `docs/strategy/` SEO plan). Build a lightweight `generate-blog-images.py` script once the content calendar is confirmed — same fal.ai pattern, 16:9 format, text-overlay-safe (subject centred, darker edges).

- Notes:

## 10. Open Graph / social share images
One 1200×630 OG image per major page (~20 total) — what appears when a URL is shared on LinkedIn, email, or Teams. High priority for B2B buyers who forward procurement links to colleagues. Images should be text-overlay-safe with BBI brand colours as a CSS overlay layer (not baked into the image). Generate in a batch once the page heroes are finalized — reuse or crop from hero images where possible.

- Notes:

---

## Post-launch PDP enhancement candidates
_Surfaced during COMP-SCRAPE-1 audit (2026-05-14). Items here are NOT in Wave E scope. Review post-launch when prioritizing v1.1 / v2 work._

### 11. PDP ergonomic-features panel
- **Source:** COMP-SCRAPE-1 audit 2026-05-14 (`docs/strategy/competitor-audit-ugoburo.md`, section 6 — PDP findings)
- **Pattern:** Icon + one-sentence plain-language explainer per ergonomic adjustment feature — e.g., "Seat Height — Raise or lower to allow your feet to rest flat on the floor. Avoids pressure under your thighs, easing blood flow." Ugoburo's Vion PDP carries 10 of these blocks.
- **Why valuable:** AI-search-friendly (clear semantic content that LLMs can extract and cite); institutional-buyer-friendly (helps less-technical procurement officers understand product specs without jargon).
- **Where applicable:** Chair PDPs first, then sit-stand desks, monitor arms, and other ergonomic product types.
- **Effort estimate:** Section template + small icon library (~half a day) + ~2 hrs per-product copy for the top 30 ergonomic SKUs. Roughly half a day of Claude Code work + ~3–4 hrs of content/curation. Resume-safe if broken into product batches.
- **When:** v1.1 or v2 post-launch enhancement. **Not Wave E.**

### 12. OECM eligibility callout snippet on all furniture-grade PDPs
- **Source:** COMP-SCRAPE-1 audit 2026-05-14 (`docs/strategy/competitor-audit-ugoburo.md`, post-launch backlog list + gap analysis row #5)
- **Pattern:** Small callout block on every furniture-grade PDP: "OECM Agreement 2025-470 eligible — institutional buyers can purchase without open tender. [Request a quote →]" Links to `/pages/oecm`. Ugoburo misses this entirely on their PDPs despite having a government page.
- **Why valuable:** BBI's single biggest competitive edge vs ugoburo is the OECM moat; surfacing it at PDP level converts procurement-officer traffic that landed on a specific product.
- **Where applicable:** All `oecm-eligible`-tagged products (~584 active SKUs). Implement as a Liquid snippet that checks the tag and renders conditionally.
- **Effort estimate:** ~1–2 hrs for the snippet + conditional Liquid logic. Content is already written on `/pages/oecm`.
- **When:** Could ship as a quick v1.1 win immediately post-launch. **Not Wave E** (defer if scope grows during INTERLINK-3).

### 13. Above-the-fold lead time display on PDPs
- **Source:** COMP-SCRAPE-1 audit 2026-05-14 (`docs/strategy/competitor-audit-ugoburo.md`, section 6 — PDP findings)
- **Pattern:** Institutional buyers need lead time *before* they engage, not buried in a spec table. Ugoburo hides it in "More Information" rows. Surface it prominently above the fold (e.g., "Lead time: 6–8 weeks for qty 20+") for chairs and desks with the `leadtime` metafield populated.
- **Why valuable:** Reduces pre-quote back-and-forth; signals operational credibility to procurement officers who need delivery windows for project planning.
- **Where applicable:** Any PDP with `product.metafields.custom.leadtime` populated (currently: chair + desk spec products from the Hero 100 spec batch at `data/specs/`).
- **Effort estimate:** ~1 hr Liquid change to surface existing metafield value above the fold. Larger effort if `leadtime` metafield is sparsely populated and needs backfill.
- **When:** v1.1 post-launch. **Not Wave E.**

### 14. Find Your Chair guided wizard
- **Source:** COMP-SCRAPE-1 audit 2026-05-14 (`docs/strategy/competitor-audit-ugoburo.md`, methodology note + gap analysis row #8)
- **Pattern:** Ugoburo's `/en/find-your-office-ergonomic-chair.html` — a step-through wizard (body type, use case, budget, adjustability needs) that narrows to a recommended SKU. Skipped in the audit as out-of-Wave-E scope.
- **Why valuable:** High-intent conversion tool; reduces support load for undecided buyers; strong AI-search footprint ("best ergonomic chair for [X]" queries where a structured recommendation page ranks).
- **Where applicable:** Ergonomic seating category. Could extend to desks (sit-stand vs fixed, use case, size).
- **Effort estimate:** Multi-week build. Requires a decision-tree data model, conditional Liquid or JS rendering, and curated product recommendations per path. Not feasible as a Claude Code solo session.
- **When:** Wave 2+ backlog. **Not Wave E.**
