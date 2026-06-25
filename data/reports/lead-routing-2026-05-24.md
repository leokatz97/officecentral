# BBI Lead Routing Analysis — 2026-05-24

**Owner:** Leo Katz (read-only audit, no theme writes)
**Scope:** All lead-intake surfaces across the BBI Shopify theme prior to LAUNCH-2
**Repo HEAD at audit:** `bc0918c` (Step 36c follow-up — ds-article.liquid CSS bug-fix bundle)
**Branch:** `main`

---

## Executive Summary

| Metric | Result |
|---|---|
| Total lead entry-point **surfaces** | **5** (modal, nav, footer, page CTAs, fallback `mailto`/`tel`) |
| Total **trigger instances** scanned | 67 `/pages/quote` anchors + 9 `data-bbi-quote-trigger` buttons + 96 `tel:` + 10 `mailto:` + 3 legacy contact forms |
| Distinct **destinations** | 3 — Shopify `/contact` endpoint (modal), `info@brantbusinessinteriors.com`, `tel:18008359565` |
| **CRITICAL** findings | **0** |
| **HIGH** findings | **3** |
| **MED** findings | **2** |
| **LOW** findings | **2** |
| **LAUNCH-2 readiness** | **GO with caveats** — proceed pending verification of HIGH-1 (Shopify Settings > Notifications inbox) and acknowledgement of HIGH-2 (no-JS fallback) + HIGH-3 (stale `/pages/contact` CTA on unbuyable PDPs) |

Top-line: the in-theme plumbing is sound — every quote CTA on the site funnels through the sitewide `bbi-quote-modal` via either `data-bbi-quote-trigger` or the `/pages/quote` href-intercept handler. The risk is **not** broken HTML; it is **inbox routing**. The modal snippet's own header comment (`bbi-quote-modal.liquid:2-6`) says per-type routing is a placeholder pending LEAD-INBOX-1. Until then, every submission lands in whichever single inbox is configured in Shopify Admin > Settings > Notifications > Contact form. That inbox identity is **not auditable from the theme** and must be confirmed in Admin before launch.

---

## Routing flow diagram

```
                              ┌─── HEADER CTA (desktop + mobile)  ─┐
                              │    [data-bbi-quote-trigger]         │
                              │                                     │
                              ├─── ANY /pages/quote ANCHOR (×67)   ─┤   intercepted
                              │    href="/pages/quote" globally     │   client-side
                              ├─── PDP "Request a Quote"           ─┤   by modal's
   QUOTE-INTENT LEADS  ───────┤    (ds-pdp-base ×2)                 │   global click
                              ├─── DESIGN consult button           ─┤   listener
                              │    (lead_type="design")             │
                              ├─── COLLECTION sticky CTA           ─┤
                              ├─── BLOG CTA, 404 CTA               ─┤
                              └─── FOOTER "Request a Quote" link  ─┘
                                                │
                                                ▼
                                  ╔═════════════════════════════╗
                                  ║   bbi-quote-modal (dialog)  ║
                                  ║   POST /contact             ║
                                  ║   contact[tags]=bbi-quote-  ║
                                  ║                  modal      ║
                                  ║   contact[lead_type]=       ║
                                  ║     quote|design|oecm|      ║
                                  ║     contact                 ║
                                  ║   contact[subject]=         ║
                                  ║     [Quote Request] / ...   ║
                                  ║   + product/collection ctx  ║
                                  ╚══════════════╤══════════════╝
                                                 │
                                                 ▼
                              Shopify Admin > Settings > Notifications
                                  > Contact form ───► [ONE inbox]
                                  (CURRENT — pending LEAD-INBOX-1)
                                                 │
                              (FUTURE — Phase 4) │ tag/subject-based
                                                 ▼  forwarding rule
                                       quotes@brantbusinessinteriors.com
                                       design@brantbusinessinteriors.com
                                       info@brantbusinessinteriors.com

   GENERAL CONTACT  ─────────► mailto:info@brantbusinessinteriors.com  (×10)
   PHONE            ─────────► tel:18008359565  (×96)  +  tel:+18008359565 (×1)
```

---

## Entry point inventory

### A. Sitewide modal — `theme/snippets/bbi-quote-modal.liquid`
- **Render point:** `theme/layout/theme.liquid:170` — rendered once per page inside the `bbi_landing` gate.
- **Gated to (per `bbi-landing-gate.liquid`):** index, cart, all collection pages, all PDPs, 404, blog index, article, search, customer account templates, plus 20 explicit page suffixes (about, brands*, contact, customer-stories, delivery, design-services, education, faq, government, healthcare, industries, non-profit, oecm, our-work, professional-services, quote, relocation).
- **Triggered by:** (1) any element with `[data-bbi-quote-trigger]`; (2) any `<a href="/pages/quote*">` click (the modal's `connectedCallback` installs a `document`-level click listener at `bbi-quote-modal.liquid:441-467`).
- **Submit endpoint:** `POST /contact` via `fetch` (`bbi-quote-modal.liquid:579`). Uses Shopify's `{% form 'contact' %}` helper.
- **Hidden context preserved on submit:**
  | Field | Value |
  |---|---|
  | `contact[tags]` | `bbi-quote-modal` |
  | `contact[lead_type]` | `quote` \| `design` \| `oecm` \| `contact` (from trigger `data-lead-type`) |
  | `contact[subject]` | Per-type: `[Quote Request] / [Design Consultation] / [OECM Inquiry] / [General Contact] via Brant Business Interiors` (`bbi-quote-modal.liquid:479-486`) |
  | `contact[product_handle]` | From trigger `data-product-handle` or URL `?product=` param |
  | `contact[product_title]` | From trigger `data-product-title` or URL `?title=` param |
  | `contact[collection_handle]` | From trigger `data-collection-handle` or URL `?collection=` param |
  | `product` | Duplicate of product title for legacy compatibility |
- **Visible form fields:** name (required), email (required), phone, company, enquiry_type (select: General quote / OECM purchase / Design consultation / Delivery / Other), body/scope (required).
- **Destination:** Shopify Admin > Settings > Notifications > **Contact form** inbox. The snippet's header comment (lines 2-6) acknowledges this is **placeholder routing pending LEAD-INBOX-1**.
- **Success behaviour:** dialog flips to success panel with recap (name/email/enquiry type/product); 1-business-day promise displayed; backdrop/Escape disabled in success state so user must explicitly close.
- **Error behaviour:** only triggered by network failure (no response); message reads "Something went wrong. Please try again or call 1-800-835-9565."

### B. Quote page — `theme/sections/ds-lp-quote.liquid` (template suffix `quote`)
- **Hero primary CTA** (`:428`) — `href="{{ _cta_url }}"` defaulting to `/pages/quote` → opens modal.
- **Hero phone CTA** (`:429`) — `tel:{{ section.settings.phone_href }}`.
- **Contact section channel cards** (`:517-549`):
  - "Online quote form" (`:517`) — `href="{{ _form_url }}"` defaulting to `/pages/quote` → opens modal. *(PR-2 fix — was defaulting to `/pages/contact` before)*
  - "Call 1-800-835-9565" (`:528`) — `tel:{{ section.settings.phone_href }}`.
  - Email channel (`:539`) — `mailto:{{ _email }}` defaulting to `info@brantbusinessinteriors.com`.
- **OECM callout primary CTA** (`:563`) — `href="{{ _cta_url }}"` → opens modal.
- **OECM callout secondary** (`:564`) — `href="/pages/oecm"` (navigation, not lead intake).
- **CTA closer phone** (`:771`) — `tel:{{ section.settings.phone_href }}`.

### C. Contact page — `theme/sections/ds-lp-contact.liquid` (template suffix `contact`)
- **No form on this page** (confirmed during PR-2 investigation).
- **Phone display + CTA** (`:87`, `:118`) — `tel:18008359565` (hardcoded, 11-digit, no `+1`).
- **Email display** (`:92`) — `mailto:info@brantbusinessinteriors.com`.
- **Showroom address** (`:97`) — 701 The Queensway, Units 2-4, Peterborough ON K9J 7J6 (consistent with `project_bbi_canonical_address` memory).
- **Hours** (`:102`) — Monday-Friday 9 am - 5 pm ET.
- **"Request a Quote" CTA** (`:117`) — `href="/pages/quote"` → opens modal (via global intercept).
- **OECM bar** (`:153`) — links to `/pages/oecm` (navigation).

### D. OECM page — `theme/sections/ds-lp-oecm.liquid` (template suffix `oecm`)
- **Hero primary CTA** (`:363`) — `href="{{ _cta_url }}"` defaulting to `/pages/quote` → opens modal.
- **Hero phone CTA** (`:364`) — `tel:{{ section.settings.phone_href }}`.
- **Coverage footnote phone** (`:425`).
- **How-to-purchase footnote phone** (`:453`).
- **CTA closer primary** (`:637`) — opens modal.
- **CTA closer phone** (`:644`).

### E. Industry / brand / service landing pages (16 sections)
- **Pattern:** every `ds-lp-*` section ends with a CTA closer pair: primary `<a href="/pages/quote">` (opens modal) + secondary `<a href="tel:18008359565">`. The FAQ block above the closer adds a third "Still have a question? Call ... or request a quote" line.
- **Files using this pattern:** `ds-lp-about`, `ds-lp-brands` + 6 brand pages (`-ergocentric`, `-global-teknion`, `-heartwood`, `-keilhauer`, `-obusforme`, `-otg`), `ds-lp-customer-stories`, `ds-lp-delivery`, `ds-lp-education`, `ds-lp-faq`, `ds-lp-government`, `ds-lp-healthcare`, `ds-lp-industries`, `ds-lp-non-profit`, `ds-lp-our-work`, `ds-lp-professional-services`, `ds-lp-relocation`.
- **Anomaly — `ds-lp-design-services.liquid:447-450`** — only landing-page CTA in the theme that uses `data-bbi-quote-trigger data-lead-type="design"`. Routes to modal with subject `[Design Consultation] via Brant Business Interiors`.

### F. PDP — `theme/sections/ds-pdp-base.liquid`
- **Main "Request a Quote" trigger** (`:623`) — `data-bbi-quote-trigger data-lead-type="quote"` with `data-product-handle` / `data-product-title` / `data-collection-handle` passed through (`:974` resolves the trigger element).
- **CTA closer "Request a Quote"** (`:796`) — `data-bbi-quote-trigger data-lead-type="quote"` (no product context).
- **Phone CTAs** (`:642`, `:797`) — `tel:18008359565`.
- **Helper question:** `:642` "Questions? Call 1-800-835-9565".

### G. Collection page — `theme/sections/ds-cc-base.liquid`
- **Sticky CTA** (`:986`) — `data-bbi-quote-trigger data-lead-type="quote"`.
- **Phone CTAs** (`:625`, `:982`) — `tel:18008359565`.

### H. Other surfaces
- **Header (`bbi-nav.liquid`):** desktop phone (`:619`), desktop quote CTA `<button data-bbi-quote-trigger>` (`:622`), mobile-nav phone (`:796`), mobile-nav quote CTA (`:800`). Both desktop and mobile nav also include a `<a href="/pages/quote">Request a Quote</a>` inside dropdowns (`:573`, `:772`) — these open the modal via the global anchor intercept.
- **Footer (`bbi-footer.liquid`):** phone (`:237`), email mailto (`:241`), Services-column "Request a Quote" link (`:224`) → modal via intercept.
- **404 page (`ds-system-404.liquid`):** quote button (`:167`) + phone (`:171`).
- **Blog list (`ds-blog-list.liquid`):** CTA button (`:228`) + phone (`:229`).
- **Article (`ds-article.liquid`):** `/pages/quote` anchor (`:336`) + phone (`:337`).
- **Search results (`ds-search-results.liquid`):** product card `/pages/quote` link (`:326`).
- **Customer Stories collection (`ds-cs-base.liquid`):** closer phone `tel:+18008359565` (`:593` — the **only** E.164-formatted `tel:` in the theme) + `/pages/quote?source=collection-cta&lead_type=design-consultation` (`:597`).
- **Browse FAQ snippet (`ds-browse-faq.liquid:228`):** "Still have a question?" phone + quote link.

---

## Verified consistency — PASSING checks

- ✓ **Modal-funnel coverage** — every `/pages/quote` href in the theme (67 instances) is intercepted by the modal's document-level click listener (`bbi-quote-modal.liquid:455-466`). The closure check is `href.startsWith('/pages/quote')`, so query-string variants (e.g. `ds-cs-base.liquid:597` passes `?source=collection-cta&lead_type=design-consultation`) are caught.
- ✓ **Tag preservation** — every modal submission carries `contact[tags]=bbi-quote-modal` (hardcoded in snippet, line 348) and `contact[lead_type]` populated from the trigger context. The lead_type is reflected in `contact[subject]` so even a human-only inbox triage can split intent.
- ✓ **Product-context preservation** — PDP quote triggers (`ds-pdp-base.liquid:623`, `:974`) pass `data-product-handle` / `data-product-title` / `data-collection-handle` through to the modal, populated into hidden fields on open (`bbi-quote-modal.liquid:474-476`).
- ✓ **Lead-type subject mapping** — `quote`, `design`, `oecm`, `contact` each get a distinct subject prefix (`bbi-quote-modal.liquid:479-486`). `design` lead-type currently only fires from `ds-lp-design-services.liquid:447`; `oecm`/`contact` lead-types are wired but no in-theme trigger currently sets them (OECM callouts go via plain `/pages/quote` anchors → default `lead_type=quote`).
- ✓ **Single canonical phone number** — every `tel:` link points at the same number `18008359565` (1-800-835-9565 toll-free).
- ✓ **Single canonical general email** — every `mailto:` points at `info@brantbusinessinteriors.com`. No leakage to `quotes@` or `design@` aliases that don't yet exist.
- ✓ **Single canonical address** — every footer/contact mention reads "701 The Queensway, Units 2-4, Peterborough ON K9J 7J6" — consistent with `project_bbi_canonical_address` memory (Brantford references already retired in S4-CONTACT-FIX).
- ✓ **Modal isolation from cart** — the snippet does not write to cart, does not perform redirects, and waits for `fetch` to complete before showing success state.

---

## Gaps

### CRITICAL findings

**None.** No routing-breaking issues that would lose a lead outright on the day-of-launch.

### HIGH findings

#### HIGH-1 — Inbox destination is unverified
- **Surface:** Modal submissions (and the legacy `contact-form.liquid` if it's still rendered anywhere) post to Shopify `/contact`, which routes to **whichever email address is configured in Shopify Admin > Settings > Notifications > Contact form**.
- **Evidence:** `bbi-quote-modal.liquid:2-6` comment explicitly says — "Form action is a placeholder. Per-type routing to quotes@/design@/info@ wires up in Phase 4 after LEAD-INBOX-1 (Steve provisions inboxes). Do NOT change the routing destination here without updating the build state."
- **Risk:** if the Settings > Notifications inbox is not currently monitored (e.g. still pointing at a personal `@gmail.com` placeholder, or at an alias that bounces), every LAUNCH-2 lead lands in /dev/null.
- **What this audit can verify from theme code:** the tag (`bbi-quote-modal`), lead_type, and subject prefix are all carried correctly so a human triaging the inbox can sort intent.
- **What this audit CANNOT verify:** the actual mailbox where Shopify delivers it.
- **Recommended pre-launch action:** **Steve must confirm the Settings > Notifications > Contact form sender notification email is currently `info@brantbusinessinteriors.com` (or whichever single inbox is monitored)**, and that a test submission lands in that inbox within ~60 seconds. Without this confirmation the launch is exposed.

#### HIGH-2 — No-JS users can't open the modal
- **Surface:** every `data-bbi-quote-trigger` is a `<button type="button">` element, not an `<a>`. With JS disabled, clicking does nothing. There is no `href` fallback.
- **Affected triggers (9 buttons across 6 files):**
  - `bbi-nav.liquid:622` (header desktop quote CTA)
  - `bbi-nav.liquid:800` (mobile-nav quote CTA)
  - `ds-pdp-base.liquid:623` (PDP primary quote)
  - `ds-pdp-base.liquid:796` (PDP closer quote)
  - `ds-cc-base.liquid:986` (collection sticky quote)
  - `ds-blog-list.liquid:228` (blog index quote)
  - `ds-system-404.liquid:167` (404 page quote)
  - `ds-lp-design-services.liquid:448` (design consult button)
- **Counterweight:** the same surfaces also expose `<a href="/pages/quote">` somewhere (header dropdown, footer, page CTAs). With JS off, the anchor intercept also fails — but the link still navigates to the standalone Quote page, where the user finds phone/email channel cards. So **a no-JS user is not stranded** — they can call `1-800-835-9565` or email `info@brantbusinessinteriors.com` from the Quote page. They just can't submit a structured form.
- **Severity rationale:** HIGH because every PDP/collection/404 "Request a Quote" button is dead for the (small) no-JS audience. Not CRITICAL because phone+email channels remain reachable.
- **Recommended action (post-launch):** progressively-enhance buttons by making them `<a href="/pages/quote?product=...">` underneath, with JS doing `e.preventDefault()` before opening the modal. This is the same pattern the snippet already supports — it just isn't applied to the trigger HTML.

#### HIGH-3 — Stale `/pages/contact` CTA on unbuyable PDPs
- **Location:** `theme/snippets/product-form-buttons.liquid:30-36`.
- **Behaviour:** for sold-out OR $0-price products (the BBI "unbuyable item → lead capture" pattern per `feedback_unbuyable_to_quote` memory), the Add-to-Cart button is replaced with `<a href="/pages/contact?subject=Quote+request%3A+{{ product.title }}&product={{ product.handle }}">Request a Quote</a>`.
- **Problem:** this CTA navigates to `/pages/contact` — which has **no form**. The modal does not intercept `/pages/contact` (only `/pages/quote*`). User has to click again on the contact page's "Request a Quote" button (which then does open the modal). Extra hop, lost intent, lost subject/product context.
- **Why PR-2 missed it:** PR-2 fixed the `/pages/contact` defaults inside `ds-lp-quote.liquid`. It didn't touch the product-form-buttons snippet, which is a separate (legacy Starlite-inherited) file.
- **Blast radius:** every sold-out / $0-price / showcase product card on the storefront. Per the unbuyable-as-lead-capture strategy, these ARE the highest-intent B2B leads (they actively want to talk to sales because the storefront can't transact for them).
- **Recommended pre-launch action:** rewrite the CTA to either (a) `<button data-bbi-quote-trigger data-lead-type="quote" data-product-handle="{{ product.handle }}" data-product-title="{{ product.title | escape }}">`, or (b) `<a href="/pages/quote?product={{ product.handle | url_encode }}&title={{ product.title | url_encode }}">`. Option (b) is one-line and preserves no-JS fallback. **30-min fix; recommended for pre-launch.**

### MED findings

#### MED-1 — Phone format inconsistency (INTERLINK-3 scope, partly relevant here)
- 96 of 97 `tel:` links in the theme use 11-digit `tel:18008359565` (no `+`). 1 uses E.164 `tel:+18008359565` (`ds-cs-base.liquid:593`).
- iOS Safari, Chrome Android, and macOS Safari all accept the 11-digit form for North American numbers — tap-to-call works. Behaviour on Windows/Linux dialers, on macOS FaceTime, on third-party softphones is less predictable; E.164 is the safe form.
- This is exactly the INTERLINK-3 finding (89 instances) — confirmed deferred post-launch. The audit corroborates that **none of the failing-format `tel:` links are on the lead-intake critical path in a way that would silently lose a lead** (every phone display also shows the human-readable `1-800-835-9565` next to it, so a user can dial manually if the link fails).
- **Recommended action:** keep deferred per INTERLINK-3.

#### MED-2 — Legacy Starlite forms still in theme
- `theme/sections/contact-form.liquid` and `theme/snippets/product-query-form.liquid` are inherited Starlite-era contact forms that still call `{% form 'contact' %}` and would route into the same Shopify Notifications inbox as the BBI modal — but with no `lead_type` tag or any BBI-specific metadata.
- Neither file is referenced by any BBI page template (verified — none of the BBI page templates render `contact-form` section, and `product-query-form` is gated by a `formTrigger` variable that no BBI section sets).
- **Risk:** if Steve ever adds the `contact-form` section to a JSON template in Theme Editor, leads from that page would arrive at the same inbox with NO tag, indistinguishable from BBI modal leads, and could quietly bury the funnel signal.
- **Recommended action:** post-launch — delete `contact-form.liquid` and `product-query-form.liquid` (dead code), or rename to `_legacy-contact-form.liquid` to make them un-renderable from Theme Editor.

### LOW findings

#### LOW-1 — `oecm` and `contact` lead-types are wired in the modal but never set
- `bbi-quote-modal.liquid:479-486` maps four lead-types (`quote`, `design`, `oecm`, `contact`) to subject prefixes. Only `quote` and `design` (via `ds-lp-design-services.liquid:448`) are actually set by any trigger. OECM page CTAs use plain `href="/pages/quote"` anchors which inherit `lead_type=quote`.
- **Recommended action (post-launch):** update OECM-page CTAs to `<a href="/pages/quote?lead_type=oecm">` so the URL intercept seeds `lead_type=oecm`. The modal already supports this via `url.searchParams.get('lead_type')` (`bbi-quote-modal.liquid:461`). Low-risk, low-value polish.

#### LOW-2 — No analytics dataLayer event on modal submit
- The modal's `_handleSubmit` (`bbi-quote-modal.liquid:569-599`) does not push a GA4 / dataLayer event on success. Submissions are invisible to GA without a Shopify Flow workaround.
- Out of scope for LEAD-2 per the prompt (analytics is post-launch concern), but flagging.

---

## Recommendations

### Pre-launch (LAUNCH-2 GO/NO-GO blockers)

1. **CONFIRM Shopify Admin > Settings > Notifications > Contact form sender notification email** — this is the single most important verification before launch. **OWNER: Steve.** [HIGH-1]
2. **Submit a test lead via the modal on DEV theme** with a distinct subject keyword, time it, and verify arrival in the configured inbox within 60 seconds. **OWNER: Leo or Steve.** [HIGH-1 verification]
3. **OPTIONAL — fix `product-form-buttons.liquid:30`** to point at `/pages/quote?product=...` instead of `/pages/contact?subject=...`. 30-minute change, recommended if there's time today; otherwise launch with the extra-hop UX and queue for first-week patch. [HIGH-3]

### Post-launch backlog

4. **No-JS button fallback** — convert `data-bbi-quote-trigger` button elements to anchors with hrefs, JS does `preventDefault`. Quick win across 9 trigger sites. [HIGH-2]
5. **Delete or rename legacy `contact-form.liquid` and `product-query-form.liquid`** to prevent accidental Theme-Editor introduction of untagged lead intake. [MED-2]
6. **INTERLINK-3 phone format cleanup** — already queued. [MED-1]
7. **Wire `lead_type=oecm` on OECM page CTAs.** [LOW-1]
8. **Add GA4/dataLayer success event in modal `_handleSubmit`.** [LOW-2]
9. **LEAD-INBOX-1 — provision `quotes@` and `design@` aliases**, configure inbox-routing rule (Shopify Flow or external email forwarder) keyed on `contact[subject]` prefix. This is the work the modal snippet header comment is referring to.

---

## LAUNCH-2 readiness call

**GO** — conditional on Steve confirming the Shopify Notifications inbox per HIGH-1 (a 5-minute Admin check + 1 test submission). All in-theme plumbing is correct; the modal funnel covers every quote CTA on the site; phone + email fallbacks are present and consistent; no CRITICAL findings.

The HIGH-3 stale CTA is a UX papercut, not a lead-loss issue (users still arrive on /pages/contact where they can call, email, or click through to the modal). HIGH-2 (no-JS) affects a minimal audience and still leaves phone/email reachable. Both can ship as-is and be patched in week 1.

---

*Audit conducted read-only against repo HEAD `bc0918c` on 2026-05-24 per DO NEXT #6 / Step 22 LEAD-2. No theme files modified. No Shopify Admin changes. Pre-existing untracked items left untouched.*
