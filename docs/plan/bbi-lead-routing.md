# BBI Lead Routing — current state (2026-05-07)

Audit produced by crawling all `ds-lp-*` sections, `bbi-nav.liquid`, `bbi-footer.liquid`, and `templates/index.json` custom-liquid blocks in the dev theme (`186373570873`). Every CTA that a visitor can click is catalogued below.

---

## CTAs found (audit)

### Homepage (`/` — `templates/index.json`)

| Section | CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|---|
| `bbi-hero` | Request a Quote | `<a>` button | `/pages/quote` | none |
| `bbi-hero` | Shop furniture | `<a>` button | `/collections/business-furniture` | — |
| `bbi-hero` | 1-800-835-9565 | `<a>` inline | `tel:18008359565` | — |
| `bbi-featured` | Request a Quote (×3 product cards) | `<a>` button | `/pages/quote` | none |
| `bbi-services` | Request a Quote | `<a>` button | `/pages/quote` | none |

### BBI Nav (`snippets/bbi-nav.liquid`)

| Context | CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|---|
| Desktop header | 1-800-835-9565 | `<a>` phone | `tel:18008359565` | — |
| Desktop header | Request a Quote | `<a>` button | `/pages/quote` | none |
| Desktop "About" dropdown | Request a Quote | `<a>` dropdown link | `/pages/quote` | none |
| Desktop "About" dropdown | Contact | `<a>` dropdown link | `/pages/contact` | none (page not yet built) |
| Mobile nav | Request a Quote | `<a>` | `/pages/quote` | none |
| Mobile nav | Contact | `<a>` | `/pages/contact` | none (page not yet built) |
| Mobile nav | 1-800-835-9565 | `<a>` | `tel:18008359565` | — |

### BBI Footer (`snippets/bbi-footer.liquid`)

| CTA label | Element | Destination |
|---|---|---|
| Request a Quote | `<a>` | `/pages/quote` |
| 1-800-835-9565 | `<a>` | `tel:18008359565` |
| info@brantbusinessinteriors.com | `<a>` | `mailto:info@brantbusinessinteriors.com` |

### Industries Hub (`/pages/industries` — `ds-lp-industries.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| Request a Quote (hero) | `<a>` button | `/pages/quote` | none |
| 1-800-835-9565 (hero) | `<a>` | `tel:18008359565` | — |
| Request a quote (FAQ inline) | `<a>` | `/pages/quote` | none |
| Request a Quote (closer) | `<a>` button | `/pages/quote` | none |
| 1-800-835-9565 (closer sub-line) | `<a>` | `tel:18008359565` | — |

### Healthcare (`/pages/healthcare` — `ds-lp-healthcare.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| Request a Quote (hero) | `<a>` button | `/pages/quote` | none |
| Call 1-800-835-9565 (hero) | `<a>` button | `tel:18008359565` | — |
| Learn about OECM purchasing (OECM bar) | `<a>` button | `/pages/oecm` | — |
| Request a quote (FAQ inline) | `<a>` | `/pages/quote` | none |
| 1-800-835-9565 (FAQ inline) | `<a>` | `tel:18008359565` | — |
| Request a Quote (closer) | `<a>` button | `/pages/quote` | none |
| 1-800-835-9565 (closer) | `<a>` | `tel:18008359565` | — |

_Education, Government, Non-Profit: identical CTA structure to Healthcare above._

### Professional Services (`/pages/professional-services` — `ds-lp-professional-services.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| Request a Quote (hero) | `<a>` button | `/pages/quote` | none |
| Call 1-800-835-9565 (hero) | `<a>` button | `tel:18008359565` | — |
| Request a quote (FAQ inline) | `<a>` | `/pages/quote` | none |
| 1-800-835-9565 (FAQ inline) | `<a>` | `tel:18008359565` | — |
| Request a Quote (closer) | `<a>` button | `/pages/quote` | none |
| 1-800-835-9565 (closer) | `<a>` | `tel:18008359565` | — |

_(No OECM bar on professional-services.)_

### OECM (`/pages/oecm` — `ds-lp-oecm.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| Request a Quote (hero, configurable) | `<a>` button | `/pages/quote` (schema default `cta_primary_url`) | none |
| Call 1-800-835-9565 (hero) | `<a>` button | `tel:18008359565` | — |
| Request a Quote (closer) | `<a>` button | `/pages/quote` (same schema default) | none |
| 1-800-835-9565 (closer) | `<a>` | `tel:18008359565` | — |

### Design Services (`/pages/design-services` — `ds-lp-design-services.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| Call 1-800-835-9565 (hero) | `<a>` button | `tel:18008359565` | — |
| Tell us about your project (inline form) | `<form>` | `mailto:sales@brantbusinessinteriors.com` | none (mailto) |
| Call 1-800-835-9565 (closer) | `<a>` button | `tel:18008359565` | — |

### FAQ (`/pages/faq` — `ds-lp-faq.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| 1-800-835-9565 (multiple FAQ answers) | `<a>` | `tel:18008359565` | — |
| info@brantbusinessinteriors.com (FAQ answers) | `<a>` | `mailto:info@brantbusinessinteriors.com` | — |
| Request a quote (FAQ section nudges ×5) | `<a>` | `/pages/quote` | none |

### Quote page (`/pages/quote` — `ds-lp-quote.liquid`)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| Online quote form (contact option 1) | `<a>` | `/pages/contact` (schema `form_url` — **not set in template JSON; falls back to `/pages/contact` which has no template yet**) | none |
| info@brantbusinessinteriors.com (contact option 2) | `<a>` | `mailto:info@brantbusinessinteriors.com` | — |
| 1-800-835-9565 (contact option 3) | `<a>` | `tel:18008359565` | — |
| Learn about OECM purchasing | `<a>` | `/pages/oecm` | — |
| Request a Quote (closer) | `<a>` | `/pages/quote` (self-link) | none |
| 1-800-835-9565 (closer) | `<a>` | `tel:18008359565` | — |

### Collection pages (`ds-cc-base.liquid` — all 9 category + hub pages)

| CTA label | Element | Destination | Lead-type tag? |
|---|---|---|---|
| 1-800-835-9565 (breadcrumb bar inline) | `<a>` | `tel:18008359565` | — |
| 1-800-835-9565 (phone CTA band) | `<a>` | `tel:18008359565` | — |
| Request a Quote (phone CTA band) | `<a>` button | `/pages/quote` | none |

---

## Forms found (audit)

| Source page | Form element | Action / destination | Fields | Lead-type tag? | Likely inbox |
|---|---|---|---|---|---|
| `/pages/design-services` | `<form action="mailto:...">` | `mailto:sales@brantbusinessinteriors.com` | name, company, email, project_type, square_footage, timeline, budget | none | **sales@brantbusinessinteriors.com** — native mailto, opens user's mail client. Not a server-side submission. Unreliable for lead capture. |
| `/pages/quote` | "Online quote form" link | `/pages/contact` (default; `form_url` not set in template JSON) | **No form on /pages/quote itself** — it links OUT to `/pages/contact`, which has no `page.contact.json` template yet (404 or Starlite default page). | — | **BROKEN** — no form at destination. Steve to verify: does `/pages/contact` exist in Shopify admin as a page? |
| All other pages | No inline forms | All quote CTAs link to `/pages/quote` | n/a | n/a | Deferred to `/pages/quote` |

> **Critical gap:** The design-services form uses `mailto:`, which opens the visitor's local email client and is invisible to BBI — no CRM record, no auto-reply, no fallback if the visitor doesn't have a mail client configured. This is the only "form submission" on the entire dev theme today.
>
> **Second gap:** `/pages/quote` has no embedded form — it presents three contact options, one of which links to `/pages/contact` which doesn't exist yet as a BBI landing page.

---

## Email channels (Shopify notification settings — Steve to fill in)

| Channel | Where it goes today | Notes |
|---|---|---|
| Shopify Sender email | TBD | Set in **Settings → General → Sender email** in Shopify Admin. This is the address Shopify uses as the "From" on all store notifications. Not readable via API without admin auth. |
| Shopify Customer email | TBD | Set in **Settings → Notifications → Customer notifications**. Governs where Shopify's `{% form 'contact' %}` submissions land. Not readable via API. |
| `sales@brantbusinessinteriors.com` | Active — design-services mailto target | Hardcoded in `ds-lp-design-services.liquid` schema setting `form_email`. Steve to confirm which inbox this is and whether it's monitored. |
| `info@brantbusinessinteriors.com` | Active — footer link, FAQ answers, quote page channel 2 | Used as the generic contact address. Steve to confirm monitored inbox. |
| Any custom routing logic? | Likely none today | No Shopify Flow, no app-level routing, no hidden `contact[lead_type]` fields in any current form. |

---

## Phone: 1-800-835-9565

- **Routes to:** TBD — Steve to fill in (physical office line? forwarding service?)
- **Hours / after-hours:** TBD — Steve to confirm. Current copy says "Mon–Fri 8–5 ET" but this isn't verified against actual routing.

---

## Decisions locked for LEAD-3 (2026-05-07)

LEAD-3 will replace the current fragmented state with a unified `bbi-lead-form.liquid` modal that appears on every bbi_landing page. All decisions below are Steve-approved as of 2026-05-07.

### Three target inboxes

Steve will configure mail-server forwarding on his side; the form just submits to the right address.

| Inbox | Purpose |
|---|---|
| `quotes@brantbusinessinteriors.com` | All quote requests + OECM procurement inquiries |
| `design@brantbusinessinteriors.com` | Design consultation requests |
| `info@brantbusinessinteriors.com` | General contact / FAQ follow-ups |

### Lead-type → inbox mapping

| `lead_type` value | Routes to | CTA that sets it |
|---|---|---|
| `quote` | `quotes@brantbusinessinteriors.com` | "Request a Quote" / "Get pricing" everywhere |
| `design` | `design@brantbusinessinteriors.com` | "Get a free design consultation" |
| `contact` | `info@brantbusinessinteriors.com` | "Contact" / general inquiries / FAQ nudges |
| `oecm` | `quotes@brantbusinessinteriors.com` | OECM page quote CTA (Steve may override to separate inbox during LEAD-3 build) |

### Modal behaviour

- **Trigger:** Every quote/design/contact/oecm CTA across all bbi_landing pages opens the modal (10 `ds-lp-*` sections + 10 collection pages + homepage). No redirect to `/pages/quote`.
- **Success state:** In-modal confirmation screen (don't close immediately). Message: _"We received your request. Expect a reply within 1 business day."_ + optional secondary CTA "Browse our work" → `/pages/our-work`.
- **Auto-reply per lead_type:**
  - `quote` → "Thanks for your quote request. Our team will respond within 1 business day with availability and pricing."
  - `design` → "Thanks for your design consultation request. We'll be in touch within 1 business day to schedule a complimentary in-person or virtual session."
  - `contact` → "Thanks for reaching out. We'll respond within 1 business day."
  - `oecm` → "Thanks for your OECM procurement inquiry. Our team will respond within 1 business day with documentation and pricing."
  - _(Final auto-reply copy reviewed and approved by Steve during LEAD-3 build.)_

### Implementation tech (drafted for LEAD-3 build)

- Single `theme/snippets/bbi-lead-form.liquid` rendered into a hidden `<dialog>` element on every bbi_landing page via `theme/layout/theme.liquid`.
- Web Component `<bbi-quote-modal>` manages open/close + focus trap (mirrors NAV-2's `<bbi-nav-mobile>` pattern — WCAG 2.1 AA compliant).
- Form posts to Shopify `{% form 'contact' %}` with a hidden `contact[lead_type]` field set per CTA invocation.
- **Routing implementation** (decided during LEAD-3 build — three options in priority order):
  1. **Shopify Flow** — reads `contact[lead_type]` from the form submission and forwards to the matching inbox. Cleanest; no external infra.
  2. **Per-form Sender Email override** — Shopify allows different notification email per contact form. Requires a separate form endpoint per lead_type.
  3. **Cloudflare Worker proxy** — intercepts the form POST and routes to correct inbox based on `lead_type`. Fallback if Flow/Shopify routing doesn't support per-field routing.

---

## Action items before LEAD-3 build

| Item | Owner | Notes |
|---|---|---|
| Confirm Shopify Sender email | Steve | Settings → General in Shopify Admin |
| Confirm `info@` and `sales@` inboxes are monitored | Steve | Are these forwarding to `steve@`? |
| Confirm phone 1-800-835-9565 routing + hours | Steve | Physical line, forwarding service, or VoIP? |
| Decide whether `/pages/contact` should exist as a standalone page or be replaced by the modal | Steve | Current nav links to it; no template exists |
| Confirm OECM lead_type inbox (`quotes@` or separate) | Steve | Default is `quotes@` above; override if needed |
| Verify Shopify plan supports Flow or identify routing method | Steve / Leo | Shopify Basic supports basic Flow triggers; confirm |
