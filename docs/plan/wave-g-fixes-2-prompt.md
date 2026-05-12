# WAVE-G-FIXES-2 — Claude Code prompt (fresh session recommended)

> Recommend a **fresh Claude Code session**. Three previously-claimed BATCH-2/3 fixes are not actually working on dev theme `186373570873` (chips still go vertical on validation, blog CTA + 404 CTA still render black-on-black, `additional-services` product still 404s). A fresh context window will re-investigate from the live DOM rather than trust the prior session's assumptions.

---

## Alignment with the Launch Readiness Plan

This pass sits between **Phase 2 (complete)** and **Phase 3 (Wave E polish — not started)** in `docs/plan/launch-readiness-plan-2026-05-08.md`. It is a deliberate "Phase 2.5" polish pass before Phase 3 begins.

**One item is intentionally pulled forward out of sequence:** BATCH 2 (Universal Quote Modal) is the plan's **LEAD-3** row, which sits in Wave E and is gated on **LEAD-INBOX-1** (a Phase 4 Steve action — provision `quotes@`/`design@`/`info@` inboxes + verify SPF/DKIM/DMARC + confirm test receipt). We are pulling the **UI** forward; we are **not** pulling forward the routing wiring. The modal ships with a placeholder action URL pointing at the existing `/pages/quote` form action so it functions as a fallback — actual per-type routing to the three inboxes happens in Phase 4 once LEAD-INBOX-1 is done.

**This pass does NOT touch Phase 3 work.** After WAVE-G-FIXES-2 lands, the next session is still Phase 3: AI-6 BreadcrumbList shared snippet, INTERLINK-3 audit, the 3 redirect CSV uploads, FAQ schema on 9 category hubs, SYS-VERIFY-1, T4 locked reference. Do not skip Phase 3 — Phase 5 (SEO-AUDIT-1) is a hard gate that needs all of it.

---

## Prompt to paste

Read these files before starting any work:
- `CLAUDE.md`
- `docs/plan/bbi-build-state.md` (especially the `WAVE-G-FIXES-1` row — note which fixes were claimed done; we need to re-verify three of them)
- `theme/sections/ds-pdp-base.liquid`
- `theme/sections/ds-blog-list.liquid`
- `theme/sections/ds-system-404.liquid`
- `theme/sections/ds-lp-delivery.liquid`
- `theme/sections/ds-cc-base.liquid` (collection.category — has the brand callout block)
- `theme/templates/collection.business-furniture.json` (has the broken CTA)
- `theme/snippets/bbi-footer.liquid`
- `theme/snippets/bbi-nav.liquid`
- `theme/sections/ds-lp-quote.liquid` (canonical form fields — modal must match)

All fixes below are from a live visual review of dev theme `186373570873`. **Work through batches in order, commit each batch separately, push to the dev theme after each commit. After each push, fetch the live HTML/CSS via curl and DOM-verify the fix actually landed before moving on — do not trust "OK" responses from the asset push.**

---

### BATCH 1 — Verify and re-fix three regressions claimed-done in WAVE-G-FIXES-1

Each of these was marked ✅ in commit `42c4227` but is broken on the live dev theme. For each: fetch the rendered page with `curl '<url>?preview_theme_id=186373570873' -H 'User-Agent: Mozilla/5.0'`, find the actual offending CSS/JS that's still wrong, fix it, re-push, re-verify.

**1a. Variant chips still collapse to vertical on Add-to-Cart validation**
URL: https://office-central-online.myshopify.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873
Steps to reproduce: load page, do not select a finish, click Add to Cart. Chips reflow to single column.
Root cause to investigate: the `2g` fix in BATCH-2 added `.needs-selection` styling but the `.pdp-variants__options` flex container may be losing `display: flex; flex-wrap: wrap` because of an outer container shift, or another stylesheet (Starlite leftover, theme.css) is overriding it. Inspect computed styles in the validation state. Fix should `!important`-protect the flex layout if necessary, or remove the conflicting rule entirely.

**1b. "Ready to furnish your space" CTA on `/blogs/news` — black text on black button**
URL: https://office-central-online.myshopify.com/blogs/news?preview_theme_id=186373570873
The 3a fix added `color: #ffffff` to `.blog-cta__btn` but the button still renders dark text. Possible causes: (a) the rule is overridden by a higher-specificity selector elsewhere, (b) the ds-blog-list.liquid version on the dev theme is stale and `bbi-push-landing.py` is uploading from the wrong tree (see CLAUDE.md "lessons learned" #4 — worktree drift), (c) the button uses a different class on the live page than `.blog-cta__btn`. Fetch the live HTML, find the actual button class, set explicit `color: #ffffff !important` on the right selector, re-push.

**1c. 404 page "Can't find what you need" Request a Quote button — black text on black**
URL: hit any garbage URL on dev theme — e.g. https://office-central-online.myshopify.com/asdfasdf?preview_theme_id=186373570873
Same pattern as 1b. Find the actual button selector in `ds-system-404.liquid`, set explicit `color: #ffffff` (use `!important` if necessary), verify after push.

**1d. `/products/additional-services-dismantle-re-assemble` still 404**
URL: https://office-central-online.myshopify.com/products/additional-services-dismantle-re-assemble?preview_theme_id=186373570873
WAVE-G-FIXES-1 claimed the product was published via API. Verify with: `curl -s -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN" "https://office-central-online.myshopify.com/admin/api/2026-04/products.json?handle=additional-services-dismantle-re-assemble" | python3 -m json.tool`. Check `published_at`, `status`, `published_scope`. If `published_scope` is `global` and `published_at` is non-null but the storefront still returns 404, the issue is template-suffix related — confirm the product has `template_suffix` either `null` (default `product.json`) or a suffix that exists on the dev theme. Also confirm the product is published to the **Online Store** sales channel (not just `web` scope). Fix and verify with a fresh curl.

Commit BATCH 1 as one commit. Verify in the commit message which root cause each of the four fixes had.

---

### BATCH 2 — Universal Request-a-Quote modal (NEW — biggest item)

**Plan context:** This is **LEAD-3** from Wave E, pulled forward into this polish pass as a UI-only deliverable. The plan gates LEAD-3 on LEAD-INBOX-1 (Steve provisions 3 inboxes in Phase 4). We are **not** pulling LEAD-INBOX-1 forward — only the modal UI. The modal must ship with a placeholder action URL that uses the existing `/pages/quote` form action as fallback. Per-type routing (quote→quotes@, design→design@, contact→info@) is explicitly **deferred** to Phase 4 after LEAD-INBOX-1 is done. Document this clearly in the snippet header comment so the Phase 4 work knows what to wire up.

**Today's behavior (broken):** "Request a Quote" CTAs across the site behave inconsistently. Some navigate to `/pages/quote`, some open a `mailto:`, some link to a category page with a quote query string. Per the user: every Request-a-Quote CTA, regardless of page or context, should open a single consistent modal with the form. No navigation. After submit, an in-modal success state confirms completion.

**Target behavior:**
1. New snippet `theme/snippets/bbi-quote-modal.liquid` containing a `<dialog>`-based modal with a Web Component wrapper `<bbi-quote-modal>` (mirror the pattern of `bbi-nav-mobile` from NAV-2 — focus trap, Escape-to-close, click-outside-to-close).
2. The form inside the modal must contain **exactly the same fields as the `/pages/quote` form** (read `theme/sections/ds-lp-quote.liquid` to extract the canonical field list — name, email, phone, company, project type, budget range, timeline, message, file upload if present, etc.). Match field names so the routing destination accepts the payload.
3. **Submission target — placeholder, not final routing.** Use the same form action as `/pages/quote` (likely Shopify's `/contact#ContactFormQuote` or whatever ds-lp-quote.liquid uses). This is a deliberate placeholder — final per-type routing happens in Phase 4 after LEAD-INBOX-1. Add a header comment in the snippet:
   ```
   {%- comment -%}
     LEAD-3 (UI-only — shipped early in WAVE-G-FIXES-2, 2026-05-10)
     Form action is a placeholder. Per-type routing to quotes@/design@/info@
     wires up in Phase 4 after LEAD-INBOX-1 (Steve provisions inboxes).
     Do NOT change the routing destination here without updating the build state.
   {%- endcomment -%}
   ```
4. Optional context fields: when triggered from a PDP, the modal should pre-populate hidden inputs `product_handle`, `product_title`, `variant_id` (if a variant is selected). When triggered from a collection page, pre-populate `collection_handle`. When triggered with no context (footer, nav, generic CTA), no pre-fill. Also pre-populate a hidden `lead_type` field (`quote`, `design`, `contact`, `oecm`) based on the trigger button's `data-lead-type` attribute — Phase 4 routing reads this field to pick the destination inbox.
5. Success state: after submit, modal swaps to a confirmation panel with a checkmark, "Thanks — we'll get back to you within one business day", and a "Close" button. Modal does not close automatically; user closes it.
6. Wire-up: replace every `<a href="/pages/quote">` and `<a href="/pages/quote?...">` across the theme with `<button type="button" data-bbi-quote-trigger data-lead-type="quote" ...>` (preserving any existing query-string params as `data-` attributes for pre-fill). The Web Component listens for clicks on `[data-bbi-quote-trigger]` and opens the modal with the appropriate context.
7. Render the snippet once, in `theme/layout/theme.liquid` inside the `bbi_landing` gate, so it's available on every BBI page without re-rendering per section.
8. Do **NOT** touch the `/pages/quote` page itself — it stays as a fallback for users who land on it directly (e.g. from email links). The modal is the new primary path.

**Files likely touched:**
- New: `theme/snippets/bbi-quote-modal.liquid`
- New: `theme/assets/bbi-quote-modal.js` (or inline in the snippet — match existing pattern)
- Modified: `theme/layout/theme.liquid` (render snippet inside gate)
- Modified: `theme/snippets/bbi-nav.liquid` (Quote button → trigger)
- Modified: `theme/snippets/bbi-footer.liquid` (any quote CTA)
- Modified: `theme/sections/ds-pdp-base.liquid` (the two quote CTAs)
- Modified: `theme/sections/ds-cc-base.liquid` (any quote CTA)
- Modified: `theme/sections/ds-blog-list.liquid` (the "Ready to furnish your space" CTA — make this the modal trigger)
- Modified: `theme/sections/ds-system-404.liquid` (the "Can't find what you need" CTA)
- Modified: 10 `theme/sections/ds-lp-*.liquid` files — every quote CTA across landing pages
- Note: `ds-lp-quote.liquid` itself stays untouched

After push: open 5 different page types and click Request-a-Quote. Verify modal opens, has correct fields, closes via Escape and click-outside, submits without throwing console errors. Document each verification.

---

### BATCH 3 — PDP fixes (continued — items not in WAVE-G-FIXES-1)

All apply to `theme/sections/ds-pdp-base.liquid` unless noted. Test on https://office-central-online.myshopify.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873

**3a. Remove "Please note" delivery dropdown entirely**
Under the Colour swatches there is a "Please note" line with a delivery-detail dropdown. Find and delete it. WAVE-G-FIXES-1 claimed this was already removed (2f) — the file was correct but the dev theme has stale content, OR the line lives in a different section. Search the entire `theme/` directory for "Please note" and "delivery details" and remove every match. Then push and verify.

**3b. Variant size change does not refresh price**
Selecting a different size on the L-shape desk does not update the price shown next to "Add to Cart". The hidden variant_id input updates correctly (BATCH-2 2b fix), but the visible price stays on the first variant's price. Fix `BbiPdpVariants._updateFormId()` (in the `<script>` at the bottom of `ds-pdp-base.liquid`): when the matching variant is found, also update the `.pdp-price` text node with the new variant's `price` (formatted as money). Use `Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD' })`.

**3c. Description structure — three distinct sections**
Currently the description renders as one block between variants and the CTA. The user wants three distinct, labeled sections, in this order, between the variants and the CTA:

1. **About this product** — opens with one sentence on who the product is for (e.g. "Built for institutional buyers, school boards, and OECM facilities needing a durable, configurable workstation."), then the descriptive copy.
2. **Key Features** — bulleted list. Source: `product.metafields.specs.key_features` if present, else fall back to extracting bulleted lines from `product.description`, else hide the section.
3. **Specifications** — table from `specs.*` metafields. This is the existing spec table — currently rendered far below in a separate `.pdp-specs` block. **Move it inline into the info column**, between Key Features and the CTA. The standalone `.pdp-specs` block at the bottom should be removed (it's a duplicate location).

The "who it's for" line is for SEO + AEO — institutional buyer language drives the keywords we want. If `product.metafields.specs.who_its_for` exists, use that; else generate at render time using the product's tags/type (`{{ product.type }}` for "office buyers", append "OECM-eligible institutional buyers" if `oecm-eligible` tag present).

After fix: the L-shape desk PDP should show, in this column order under the variant chips: About this product → Key Features → Specifications → Add to Cart / Request a Quote.

**3d. Sold-out PDP returns 404**
URL: https://office-central-online.myshopify.com/products/anda-seat-phantom-king-gaming-style-office-chair?preview_theme_id=186373570873
Sold-out products should render the PDP with a Request-a-Quote CTA per BBI Rule #2 (unbuyable items stay live as lead-capture pages). They are 404'ing. Investigate via API: check `published_at`, `status`, `published_scope`, `template_suffix`. The product was likely unpublished when it sold out — re-publish to Online Store. Also check that BBI Rule #2 is enforced via theme guard (never delete, never unpublish on stockout) — if there's no enforcement, document a follow-up to write `scripts/audit-unpublished-products.py` and add it to the build state backlog.

Commit BATCH 3 as one commit.

---

### BATCH 4 — Brand callout: Canadian badge for all 4 brands

On the brand-callout block at the bottom of category pages (rendered by `ds-cc-base.liquid` or a child snippet), all four authorized dealer brands are Canadian:
- ergoCentric → Canadian Authorized ✅ (already correct)
- Keilhauer → Canadian Authorized ✅ (already correct)
- Global Furniture → Authorized ❌ (should be "Canadian Authorized")
- Teknion → Authorized ❌ (should be "Canadian Authorized")

Find the brand-callout rendering logic. The badge is likely either (a) a static string per brand block in the template JSON, or (b) a settings field. Either way: change Global Furniture and Teknion to display "Canadian Authorized" matching the other two brands. Verify on https://office-central-online.myshopify.com/collections/business-furniture?preview_theme_id=186373570873 and one other category page.

---

### BATCH 5 — Delivery page: remove emojis

URL: https://office-central-online.myshopify.com/pages/delivery?preview_theme_id=186373570873
Section title: "What's included" (or similar — the section with four feature cards). Cards:
- 🚚 Scheduled delivery windows
- 🔧 Professional assembly team
- 📋 Project coordination
- ♻️ Debris removal included

Remove the four emoji characters. If they are placed via `icon` settings in `ds-lp-delivery.liquid` schema, replace each with an empty string (or remove the icon line from the schema settings if cleaner). If they are inline in the section's HTML/Liquid, just delete the characters. Verify the cards still render with their titles and copy intact, just without the emoji.

---

### BATCH 6 — Business Furniture collection CTA copy fix

URL: https://office-central-online.myshopify.com/collections/business-furniture?preview_theme_id=186373570873
The "Get a free design consultation" button is rendering with two strings concatenated into one button: "Get a free design consultation. Business furniture". The intent is one button labeled "Shop all business furniture".

Open `theme/templates/collection.business-furniture.json`. Find the CTA block in the relevant section settings. The label is likely set as one string with a stray phrase appended; or there are two separate buttons in the schema being rendered as one because of a CSS layout collapse. Fix the label to read "Shop all business furniture" (or whatever copy makes sense as a single CTA — confirm with the user if uncertain, but default to "Shop all business furniture").

---

### BATCH 7 — Wave A bug double-check

The user said all 10 Wave A category collection pages "look good" but asked for a bug double-check. Run a DOM smoke check on each:

```
collections/business-furniture
collections/seating
collections/desks
collections/storage
collections/tables
collections/boardroom
collections/ergonomic-products
collections/panels-room-dividers
collections/accessories
collections/quiet-spaces
```

For each: `curl '<url>?preview_theme_id=186373570873' -H 'User-Agent: Mozilla/5.0' -s` and assert:
- exactly 1 `.bbi-header`
- exactly 1 `.bbi-footer`
- 0 `.shopify-section-group-header-group`
- breadcrumb is 3-level (Home > Shop Furniture > Category)
- at least one tile renders (grep for `pdp-prod-card` or the equivalent tile class)
- no obvious broken Liquid (no `Liquid syntax error` substring)
- the brand-callout fix from BATCH 4 reflects (where applicable)

Output a 10-row CSV: `collection,header_count,footer_count,starlite_leak,breadcrumb_levels,tiles_present,liquid_errors,verdict`. Save to `data/reports/wave-a-smoke-<date>.csv`. If anything fails, fix it in this batch.

---

### BATCH 8 — Push, verify, document

1. Push every changed theme file to dev theme `186373570873` via `BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873 --layout --snippets`. If `ds-pdp-base.liquid` or any other file 422s, surface the exact Liquid error and fix before moving on.
2. List updated verification URLs for each batch (BATCH 1: 4 URLs; BATCH 2: 5 trigger URLs across page types; BATCH 3: 2 URLs; BATCH 4–6: 1 URL each; BATCH 7: 10 URLs).
3. Add a new row to `docs/plan/bbi-build-state.md` under the existing "Wave G-Fixes" section. **Wording matters** — the LEAD-3 early-start needs to be explicit so Phase 4 knows what's already done and what still needs wiring:

```
| WAVE-G-FIXES-2 | Visual review pass 2 — LEAD-3 modal UI (early), PDP description structure, 6 minor fixes | ✅ | commits <SHA1>..<SHAN>; all on dev theme | BATCH-1 re-fix 3 regressions (chip flex, blog/404 button color, additional-services 404). **BATCH-2 LEAD-3 UI early-start** — universal `bbi-quote-modal` snippet + `<bbi-quote-modal>` Web Component, replaces all Request-a-Quote navigation across nav/footer/PDP/blog/404/10 landing pages. Form ships with placeholder action (matches `/pages/quote`); per-type routing to quotes@/design@/info@ pending **LEAD-INBOX-1 (Phase 4 Steve action)**. BATCH-3 PDP: removed "Please note" delivery line site-wide, variant price refresh on size change, restructured description into About/Key Features/Specifications inline, re-published sold-out products. BATCH-4 brand badge: Global+Teknion now show "Canadian Authorized". BATCH-5 delivery page emoji removal. BATCH-6 business-furniture CTA copy. BATCH-7 Wave A smoke test 10/10 green. |
```

4. **Also update the LEAD-3 row in Wave E** (in the same `bbi-build-state.md`):
   - Change status from ⬜ to 🟡 (UI shipped, routing pending)
   - Update Notes to start with: "🟡 **UI complete in WAVE-G-FIXES-2 (commit `<SHA>`)** — `theme/snippets/bbi-quote-modal.liquid` + `<bbi-quote-modal>` WC live on dev theme. Submission action is a placeholder pointing at `/pages/quote` form action. Per-type routing (quote→quotes@, design→design@, contact→info@, oecm→quotes@) pending LEAD-INBOX-1. To complete LEAD-3 in Phase 4: (a) confirm LEAD-INBOX-1 inboxes provisioned, (b) update form action in `bbi-quote-modal.liquid` to per-type routing (Shopify Flow OR per-form Sender Email OR Cloudflare Worker), (c) wire auto-replies per type, (d) smoke test each lead type lands in correct inbox." Keep the rest of the existing LEAD-3 notes intact.

5. Commit the build-state update separately as the final commit.

---

### Hard rules (apply across all batches)

- **Verify after every push.** Do not trust 200/OK responses. Curl the live page, grep for the expected post-fix string (or absence of the broken string), confirm before moving on. Three of four BATCH-2/3 fixes claimed-done in the prior session were never actually live.
- **`!important` is allowed only when CSS specificity from a third-party stylesheet (Starlite leftover, theme.css) is the proven cause** — and in that case, leave a `/* !important required: <reason> */` comment.
- **No deletions of products** (BBI rule #1). If `additional-services` or `anda-seat-phantom-king` is unpublished, re-publish — do not archive.
- **Worktree-aware push** — always run with `BBI_PUSH_ROOT=$(pwd)`. PB-12 fix is in place; don't bypass it.
- **Modal goes through the layout, not per-section** — render `bbi-quote-modal.liquid` exactly once in `theme.liquid` inside the gate, so a second click on a different page doesn't double-render.
- **Do not run `tag-products-by-collection.py --live`** — that's a separate authorization, still pending.
- **Halt and surface to me** if any batch is structurally larger than expected (e.g. quote modal needs a Cloudflare Worker or backend route — that's out of scope for this batch).

---

## Notes for me (Leo)

- **What this pass is and isn't:** This is a deliberate "Phase 2.5" polish pass between Phase 2 (done) and Phase 3 (Wave E polish — not started). It bundles three things: bug-fixing Phase 2 deliverables, copy/content polish, and pulling LEAD-3's UI forward. It does NOT touch any Phase 3 priorities — those happen next session.

- **LEAD-3 early-start is intentional.** Per the launch readiness plan, LEAD-3 sits in Wave E and is gated on LEAD-INBOX-1 (your Phase 4 action: provision `quotes@`/`design@`/`info@brantbusinessinteriors.com` + verify SPF/DKIM/DMARC + confirm test receipts at `steve@`). We are pulling the modal **UI** forward because it's a usability blocker now; we are NOT pulling the routing forward. The modal will work as a fallback (form submits to the same place `/pages/quote` does today). When you do LEAD-INBOX-1, the agent in Phase 4 will see the LEAD-3 row marked 🟡 with explicit "what still needs wiring" notes.

- **Two architectural questions the agent will surface:**
  1. **Sold-out PDP enforcement.** If sold-out products keep getting unpublished by something (a manual habit, an app integration, an inventory script), the modal/quote CTA on sold-out PDPs is moot — they'll keep 404'ing. The agent will flag this as a follow-up. Decide whether you want `scripts/audit-unpublished-products.py` added to the build state backlog (runs daily, alerts on any product flipped from published → unpublished).
  2. **`/pages/quote` page itself.** Now that every CTA opens the modal, the standalone `/pages/quote` page is only reachable via direct link. Decide whether to (a) keep it as-is for email-link traffic, (b) redirect it to the homepage with the modal auto-opening, or (c) leave the agent's default (keep as-is). Default for this pass is keep as-is.

- **What's still owed before launch after this pass:** Phase 3 (BreadcrumbList, INTERLINK-3, redirect uploads, FAQ schema on 9 hubs, SYS-VERIFY-1, T4 locked reference) → Phase 4 (GSC + GA4 + policy pages + LEAD-INBOX-1 + CONTENT-1 logo) → Phase 5 (SEO-AUDIT-1 hard gate) → Phase 6 (Lighthouse + A11Y + DS-VERIFY + VISUAL-COMP + IMG + MOBILE) → Phase 7 (LAUNCH-0 → LAUNCH-2). Calendar-critical path is GSC DNS verification (5–14 day async clock) — start that as early in Phase 4 as possible.
