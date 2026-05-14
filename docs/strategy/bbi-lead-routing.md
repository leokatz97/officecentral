# BBI Lead Routing — LEAD-3 Implementation
_2026-05-14 · Option D: subject-line injection + M365 inbox rules + auto-reply at alias level_

---

## What was implemented

### Theme changes (DEV theme 186373570873)

**`theme/snippets/bbi-quote-modal.liquid`** — two additions:

1. Hidden field added to the Shopify contact form:
   ```html
   <input type="hidden" name="contact[subject]" id="bbi-qm-subject"
          value="[Quote Request] via Brant Business Interiors">
   ```

2. JS `open()` method now populates this field based on `lead_type` when the modal is triggered:
   ```js
   const subjectMap = {
     'quote':   '[Quote Request] via Brant Business Interiors',
     'design':  '[Design Consultation] via Brant Business Interiors',
     'oecm':    '[OECM Inquiry] via Brant Business Interiors',
     'contact': '[General Contact] via Brant Business Interiors'
   };
   ```

**`theme/sections/ds-lp-design-services.liquid`** — replaced broken `<form action="mailto:...">` with a `data-bbi-quote-trigger data-lead-type="design"` button. Submissions from the Design Services page now go through the standard BBI quote modal with `lead_type=design` pre-set, landing at `[Design Consultation] via Brant Business Interiors`.

### Lead type → subject prefix mapping

| Trigger context | `lead_type` value | Subject prefix injected |
|---|---|---|
| Quote modal (default, PDP CTAs, nav/footer) | `quote` | `[Quote Request]` |
| Design Services page | `design` | `[Design Consultation]` |
| OECM page CTAs | `oecm` | `[OECM Inquiry]` |
| Contact page / generic links | `contact` | `[General Contact]` |

---

## ⚠️ Step Steve must complete manually: customer_email update

Shopify's Admin API does not allow updating `customer_email` programmatically (returns 406). Steve must do this in Shopify Admin.

**Current value:** `sales@brantbusinessinteriors.com`
**Target value:** `info@brantbusinessinteriors.com`

**How to update:**
1. Go to **Shopify Admin → Settings → General**
2. Under **"Store details"** → **"Customer account email"** (or "Contact information" depending on version)
3. Change the email to `info@brantbusinessinteriors.com`
4. Click **Save**

All form submissions from the BBI quote modal will then land at `info@brantbusinessinteriors.com`, which forwards to `steve@brantbusinessinteriors.com`.

---

## Subject-line behaviour: confirmed 2026-05-14

Tested on DEV theme 186373570873. Findings:

- **SMTP subject line:** `New customer message on May 14, 2026 at 3:24 pm` — Shopify's fixed template. `contact[subject]` does NOT override the SMTP subject.
- **Email body:** `[Quote Request] via Brant Business Interiors` IS present — appears as the value under the Shopify-generated "New customer message on %{creation_date}:" label in the notification body.
- All other fields confirmed present: Lead Type, Tags, Enquiry Type, Name, Email, Phone, Company, Body.

**Path B is the correct path.** Inbox rules match body content.

Path A (subject rules) and the test section below are superseded — leaving Path B+ (Shopify template edit) as the optional upgrade path.

---

## Path B: Inbox rules matching email BODY (confirmed correct path)

If Shopify sends `"Customer enquiry"` as the subject regardless of the form field, use M365 body-content rules instead.

**In GoDaddy M365 admin → info@ mailbox → Inbox Rules → Add rule:**

| Condition | Action |
|---|---|
| Body contains `[Quote Request]` | Move to folder "Quotes" (or flag) |
| Body contains `[Design Consultation]` | Move to folder "Design" (or flag) |
| Body contains `[OECM Inquiry]` | Move to folder "OECM" (or flag) |
| Body contains `[General Contact]` | Move to folder "General" (or flag) |

> **Note:** Body-content rules are slightly less reliable than subject rules (body indexing can lag), but they work for operational routing where latency of a few minutes is acceptable.

---

## Path B+ (optional, cleanest long-term): Edit Shopify notification template subject

If you want the SMTP subject line to always show the routing tag (making Path A work permanently), edit the Shopify contact notification template:

1. Shopify Admin → **Settings → Notifications**
2. Find **"Customer message"** (under Contact section) → click to edit
3. Find the **Subject** field — change it to:
   ```
   {{ contact.subject | default: 'Customer enquiry' }}
   ```
4. Click **Save**

After this, every contact form submission where `contact[subject]` is set will use that value as the actual SMTP subject. Path A inbox rules then work reliably.

---

## Auto-reply setup (Steve, M365)

Native Shopify contact forms don't support auto-replies. Auto-reply is set at the M365 alias-mailbox level. Since `quotes@`, `design@`, and `info@` all forward to `steve@`, the auto-reply fires at the alias level before forwarding.

### Per-alias auto-reply (GoDaddy M365 admin)

Repeat for each of the three aliases:

1. **GoDaddy M365 admin** → Users → `quotes@brantbusinessinteriors.com` → Mail
2. **Automatic replies** (or "Out of Office") → Enable for external senders
3. Set the auto-reply message (sample for each):

**quotes@ auto-reply:**
> Subject: We received your quote request — Brant Business Interiors
>
> Thank you for reaching out to Brant Business Interiors.
>
> We've received your quote request and our Ontario team will review it and respond within 1 business day — usually the same day.
>
> In the meantime, you can browse our full catalogue at brantbusinessinteriors.com, or call us directly at 1-800-835-9565.
>
> — The BBI Team

**design@ auto-reply:**
> Subject: We received your design consultation request — Brant Business Interiors
>
> Thank you for reaching out to Brant Business Interiors.
>
> We've received your design consultation request. Our team will review your project details and be in touch within 1 business day with next steps for your free CAD floor plan.
>
> Questions? Call us at 1-800-835-9565.
>
> — The BBI Team

**info@ auto-reply:**
> Subject: We received your message — Brant Business Interiors
>
> Thank you for contacting Brant Business Interiors.
>
> We've received your message and will respond within 1 business day.
>
> For product quotes or project pricing, you can also call us directly at 1-800-835-9565.
>
> — The BBI Team

> **GoDaddy M365 note:** Navigate to each alias mailbox via email.godaddy.com → Manage users → [alias] → Mailbox settings → Automatic replies. If the UI doesn't show per-alias auto-reply, check whether GoDaddy's M365 plan supports it — shared mailboxes and full mailboxes handle this differently.

---

## End-to-end test plan

Run after all manual steps are complete (customer_email updated + notification template edited if Path B+ chosen + auto-replies set):

| # | Action | Expected result |
|---|---|---|
| 1 | Submit quote modal with `lead_type=quote` (default from any product page or quote CTA) | Email arrives at `info@` / `steve@` with subject `[Quote Request] via Brant Business Interiors` (or body contains it) · auto-reply fires from `quotes@` |
| 2 | Submit quote modal from Design Services page (data-lead-type="design") | Email subject / body contains `[Design Consultation]` · enquiry_type pre-set to "Design consultation" · auto-reply fires from `design@` |
| 3 | Submit from OECM page | Email subject / body contains `[OECM Inquiry]` |
| 4 | Submit from Contact page link | Email subject / body contains `[General Contact]` |
| 5 | Verify inbox rule sorts test submissions into correct folders at `steve@` | Quotes in "Quotes" folder, Design in "Design" folder, etc. |
| 6 | Verify auto-reply lands in the test sender's inbox, from the correct alias address | Separate replies from `quotes@` and `design@` for tests 1 and 2 |

---

## Summary of Steve's manual follow-up tasks

| # | Task | Where | Time |
|---|---|---|---|
| 1 | Update `customer_email` → `info@brantbusinessinteriors.com` | Shopify Admin → Settings → General | 2 min |
| 2 | Run subject-line test (submit form, check email subject) | Any browser | 5 min |
| 3 | **If subject test passes (Path A):** Set inbox rules matching subject | GoDaddy M365 → info@ or steve@ | 10 min |
| 4 | **If subject test fails (Path B):** Set inbox rules matching body | GoDaddy M365 → info@ or steve@ | 10 min |
| 5 | *(Optional, recommended)* Edit Shopify notification template subject | Shopify Admin → Settings → Notifications → Customer message | 5 min |
| 6 | Set auto-reply on quotes@, design@, info@ | GoDaddy M365 admin | 15 min |
| 7 | Run full end-to-end test (test plan above) | Browser + email | 10 min |

**Total estimated time: ~45 min.**

---

## What is NOT required (already complete)

- ✅ Three inboxes (`quotes@`, `design@`, `info@`) — provisioned in LEAD-INBOX-1
- ✅ SPF includes `spf.protection.outlook.com` — confirmed LEAD-INBOX-1
- ✅ DKIM active (selector1) — confirmed LEAD-INBOX-1
- ✅ DMARC updated with rua= — confirmed LEAD-INBOX-1
- ✅ BBI quote modal with lead_type field — built in WAVE-G-FIXES-2
- ✅ contact[subject] hidden field + JS populate — LEAD-3 (this session)
- ✅ Design Services mailto: form → modal trigger — LEAD-3 (this session)
