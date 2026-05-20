# POLICY-PAGES-AUDIT
_2026-05-20 · Read-only audit of Shopify default policy pages (Privacy, Shipping, Refund, Terms)_

Scope: surface content gaps in the four Shopify-managed policy pages that
Steve needs to address pre-launch. Read-only — no theme or Shopify writes.
Source URLs (LIVE):
- https://www.brantbusinessinteriors.com/policies/privacy-policy
- https://www.brantbusinessinteriors.com/policies/shipping-policy
- https://www.brantbusinessinteriors.com/policies/refund-policy
- https://www.brantbusinessinteriors.com/policies/terms-of-service

All four pages returned **200 OK**. Findings below are based on rendered
text content extracted from each page.

---

## Summary

| Policy | Status | Critical gaps | Should-improve |
|--------|--------|---------------|----------------|
| Privacy  | NEEDS-REVIEW (wrong-entity)   | 6 | 4 |
| Shipping | MISSING (boilerplate-empty)   | 7 | 2 |
| Refund   | NEEDS-REVIEW (thin + dual-email) | 4 | 3 |
| Terms    | NEEDS-REVIEW (tri-branded)    | 5 | 4 |

Page sizes (rendered text):

| Policy | Chars | Note |
|--------|-------|------|
| Privacy  | 27,264 | Long, but for the wrong company |
| Shipping |     15 | Only the H1 "Shipping policy" — zero body content |
| Refund   |    804 | Single short paragraph, dual-brand emails |
| Terms    | 41,489 | Tri-branded (Office Central / BBI / Brant Basics) |

---

## Critical gaps (must fix before LAUNCH-2)

### 1. Shipping Policy is effectively empty
Page renders only the heading "Shipping policy" with zero body. For an
institutional B2B furniture site that quotes lead times, delivery zones,
and white-glove installation, this is a launch-blocker. Government and
healthcare buyers commonly require shipping terms in writing before they
will issue a PO.

### 2. Privacy Policy is for the wrong legal entity
The Privacy Policy identifies the Company as **"Office Central Inc.,
60 Leek Crescent, Richmond Hill, Ontario, L4B 1H1"** and links to
**https://www.officecentral.com**, with contact email
**customerservice@officecentral.com**. This document is not Brant Business
Interiors' privacy policy — it is Office Central's. A buyer doing due
diligence will flag this immediately as a credibility / legal risk.

### 3. No PIPEDA / GDPR language anywhere
Searched all 4 policies — **zero mentions** of PIPEDA, GDPR, or equivalent
Canadian privacy framework. PIPEDA compliance language is effectively
mandatory for Canadian B2B serving public-sector buyers (school boards,
hospitals, municipalities, OECM contracts).

### 4. Tri-branded Terms of Service
Terms of Service opens with: **"Office Central & Brant Business Interiors"**
as the operating entity (dual brand). Then Section 20 contact is
**sales@brantbasics.com**, and Section 21 references **"Brant Basics
Management"** and **furnorders@officecentral.com**. Three different brand
surfaces in a single document. A procurement officer can't tell which
legal entity the contract is actually with.

### 5. Refund Policy uses two competing email surfaces
Refund Policy directs damage reports to both
`furnorders@officecentral.com` **and** `sales@brantbusinessinteriors.com`.
Two emails = no clear escalation path. Also lacks the basics buyers
expect: return window, restocking fee policy, custom/configured-goods
clause, refund timeline.

### 6. No phone number, no Brantford/Ontario address in any policy
Searched all 4 policies for phone numbers (519/905/416/1-800) and for
"Brantford" — **zero hits**. The homepage shows `1-800-835-9565`, but
none of the policies surface a phone, fax, or BBI-specific street
address. The only address in any policy is Office Central's Richmond
Hill address inside the Privacy Policy (see gap #2).

### 7. No `info@brantbusinessinteriors.com` anywhere
The target post-launch contact email is not referenced in any policy.
All four pages either omit a contact entirely, use the Office Central
email, the Brant Basics email, or the `sales@brantbusinessinteriors.com`
sales alias — never the canonical `info@` address.

### 8. Governing law is "laws of Canada", not Ontario
Terms § 18: "These Terms of Service … shall be governed by … the laws of
Canada." There is no province-specific law in Canada — contracts must
be governed by a specific province (Ontario for BBI). This is a real
legal defect, not stylistic.

### 9. Shipping policy is not even linked from the footer
Homepage footer/policy links resolve only to:
`/policies/privacy-policy`, `/policies/refund-policy`,
`/policies/terms-of-service`. **`/policies/shipping-policy` is not
linked from the homepage** even though the URL resolves with 200. This
means even if Steve writes a shipping policy, it won't be discoverable
without a footer/menu change.

---

## Should-improve (nice-to-have)

- **Updated dates inconsistent:** Privacy is dated "Last updated: May 22,
  2023" (2.9 years stale). Shipping, Refund, and Terms have **no date
  shown at all**. Add a "Last updated: YYYY-MM-DD" line to all four after
  the rewrite.
- **Currency not stated:** No mention of CAD anywhere in any policy.
  Buyers from outside Ontario / Canadian government RFPs commonly need
  explicit currency confirmation in writing.
- **No OECM / institutional procurement note:** Given OECM eligibility
  is BBI's key B2B differentiator, the Terms should acknowledge
  institutional purchase-order workflow (PO acceptance, net-30 terms,
  tax-exempt invoicing for qualifying buyers).
- **Lead times not stated:** Custom-build furniture commonly has 8–16
  week lead times. Not setting expectations in the Shipping Policy
  invites disputes after order.
- **Installation services not covered:** BBI offers white-glove delivery
  + installation. Shipping Policy should describe the service area
  (Ontario? Canada-wide?), what's included, and how installation is
  quoted.
- **No data-subject-rights language in Privacy:** No mention of right to
  access, correct, or delete personal data, nor a designated privacy
  contact / data officer.
- **No force majeure clause** in Terms (recommended for institutional
  contracts that may be challenged during supply-chain or weather
  disruption).
- **Restocking-fee policy absent** in Refund. Common B2B furniture
  restocking fees are 15–35%; silence here is ambiguous.
- **No "custom / configured goods are non-returnable" clause** in Refund
  — critical for ergonomic-chair and modular-desk configurations.
- **"All Sales are Final" appears twice with different wording** —
  once in Refund Policy, once in Terms § 21. Consolidate to one
  authoritative version, referenced from the other.

---

## Per-policy details

### A. Privacy Policy — NEEDS-REVIEW (wrong-entity)

**Exists:** Yes, 200 OK, 27,264 chars of text.
**Last updated:** May 22, 2023 (only policy with a date).

**Wrong info found:**
- Company defined as **"Office Central Inc., 60 Leek Crescent, Richmond
  Hill, Ontario, L4B 1H1"** — this is not BBI.
- Website referenced as **"Office Central, accessible from
  https://www.officecentral.com"** — wrong domain.
- Privacy contact email: **`customerservice@officecentral.com`** — not
  a BBI surface.

**Missing items (B2B / Canadian baseline):**
- No mention of PIPEDA.
- No mention of GDPR or equivalent EU rights (low priority but standard
  in modern privacy policies).
- No explicit "right to access / correct / delete personal data"
  section.
- No designated privacy officer / contact for privacy questions.
- No data-retention period.

**Recommendation for Steve:**
- Rewrite the Company definition block to: **Brant Business Interiors
  Inc.**, with the correct Brantford, Ontario address.
- Replace the website reference with **https://www.brantbusinessinteriors.com**.
- Replace the contact email with **info@brantbusinessinteriors.com**
  (post-day 2 once the inbox is live).
- Add a paragraph: PIPEDA compliance, data subject rights (access /
  correction / deletion), retention period, and a privacy contact.
- Refresh the "Last updated" date to the rewrite date.

---

### B. Shipping Policy — MISSING (boilerplate-empty)

**Exists:** Page resolves with 200 OK, but body content is **15 chars
total** — only the heading "Shipping policy". No paragraphs, no clauses.

**Footer link status:** **NOT LINKED** from the homepage footer (only
Privacy, Refund, and Terms are linked).

**Missing items (B2B baseline):**
- Service areas (Ontario / Canada-wide / U.S.?).
- Delivery timeframes / standard lead times.
- Custom-build lead times (typical 8–16 weeks for furniture).
- White-glove / installation service description and quoting basis.
- Shipping costs basis (quoted per project, flat freight, etc.).
- Damaged-goods handling and inspection-on-delivery requirement.
- Title-and-risk-of-loss transfer point (Terms § 5 says "Once we
  transfer products to the carrier, title and risk of loss passes to
  you" — Shipping Policy should mirror or reference this).

**Recommendation for Steve:** This is the highest-priority rewrite.
Draft a policy that covers the seven items above. Once written, also
ensure footer / nav links to `/policies/shipping-policy` so the page is
discoverable.

---

### C. Refund Policy — NEEDS-REVIEW (thin + dual-email)

**Exists:** Yes, 200 OK, 804 chars.

**Current content (paraphrased):**
- No cancellations or returns once order is sent.
- Damages must be reported within 24 hours of receipt.
- Report damages to either `furnorders@officecentral.com` **or**
  `sales@brantbusinessinteriors.com`.
- All sales final; no exchanges.

**Wrong info found:**
- Dual-brand contact emails (Office Central + BBI).
- No BBI phone or address.

**Missing items (B2B baseline):**
- Restocking fee policy (or explicit "no restocking fee" if that's the
  intent).
- Explicit "custom / configured goods are non-returnable" clause —
  critical for ergonomic chairs and modular desks.
- Refund timeline (how long for credit to be issued once damage
  approved).
- Process detail: who arranges the replacement / pickup, who pays
  return freight.
- "Last updated" date.

**Recommendation for Steve:**
- Pick ONE contact email: `info@brantbusinessinteriors.com` (or
  `sales@brantbusinessinteriors.com` if `info@` isn't ready). Remove
  the Office Central email entirely.
- Extend the 24-hour window for damage notice — institutional receiving
  often can't inspect within 24h. 5 business days is more defensible.
- Add a custom-goods clause and a clear refund timeline.

---

### D. Terms of Service — NEEDS-REVIEW (tri-branded)

**Exists:** Yes, 200 OK, 41,489 chars. Structurally complete (sections 1–21).

**Wrong info found:**
- Opens as **"Office Central & Brant Business Interiors"** — dual
  brand, ambiguous legal entity.
- Section 18 (Governing Law): "the laws of Canada" — not a valid
  jurisdiction. Must be a province (Ontario for BBI).
- Section 20 (Contact): **`sales@brantbasics.com`** — third brand
  surface; neither BBI nor Office Central.
- Section 21 references **"Brant Basics Management"** and routes
  warranty claims to **`furnorders@officecentral.com`**.

**Missing items:**
- No "Last updated" date.
- No B2B / institutional purchase-order language (PO acceptance,
  net-30, tax-exempt invoicing for qualifying buyers).
- No force majeure clause.
- No explicit dispute-resolution mechanism beyond "laws of Canada".

**Sections that look fine and don't need rework:**
- § 1 Access and Account
- § 2 Our Products (colour-variance disclaimer is standard and useful)
- § 3 Orders (right-to-decline language is appropriate for B2B)
- § 4 Prices and Billing (subject-to-change language is fine)
- § 5 Shipping and Delivery (title/risk-of-loss transfer is fine)
- § 15 Disclaimer of Warranties (standard)

**Recommendation for Steve:**
- Decide the legal entity: **Brant Business Interiors Inc.** —
  collapse all three brand surfaces to that single name throughout.
- § 18 Governing Law: change "laws of Canada" → "**laws of the Province
  of Ontario and the federal laws of Canada applicable therein**".
- § 20 Contact: replace `sales@brantbasics.com` with
  `info@brantbusinessinteriors.com`.
- § 21: keep the all-sales-final clause but route email to a BBI
  address, remove "Brant Basics Management".
- Add a "Last updated" footer line.
- Add a short force-majeure section and a B2B PO acceptance paragraph.

---

## Cross-policy consistency findings

- **Company name consistency:** ❌ No.
  - Privacy → "Office Central Inc."
  - Shipping → (empty, no company stated)
  - Refund → no company stated; mixed `@officecentral.com` and
    `@brantbusinessinteriors.com` emails
  - Terms → "Office Central & Brant Business Interiors" + "Brant Basics
    Management" (§ 21)
- **Contact info consistency:** ❌ No.
  - Privacy → `customerservice@officecentral.com`
  - Shipping → none
  - Refund → `furnorders@officecentral.com` + `sales@brantbusinessinteriors.com`
  - Terms → `sales@brantbasics.com` (§ 20) + `furnorders@officecentral.com` (§ 21)
- **Address consistency:** ❌ No.
  - Only Privacy has an address — and it's the wrong one (Office Central
    Inc., Richmond Hill).
- **Phone consistency:** ❌ No phone in any policy.
- **Updated dates:** Inconsistent. Privacy: "May 22, 2023". Shipping,
  Refund, Terms: no date.
- **Footer linking from homepage:** ⚠️ Partial.
  - Linked: `/policies/privacy-policy`, `/policies/refund-policy`,
    `/policies/terms-of-service`
  - **Not linked: `/policies/shipping-policy`** (even though the page
    resolves with 200).
- **Checkout policy links:** Not directly auditable from this read-only
  pass (would need a live checkout session). Shopify checkout
  automatically links to all four standard policies if they exist in
  Settings → Policies — verify in Admin once the rewrites are in.

---

## Recommended actions for Steve (prioritized)

1. **(BLOCKER) Write a real Shipping Policy.** Currently zero body content.
2. **(BLOCKER) Rewrite Privacy Policy to identify BBI as the data
   controller.** Currently references Office Central Inc., Richmond Hill,
   and officecentral.com.
3. **(BLOCKER) Fix Terms § 18 Governing Law** from "laws of Canada" to
   "laws of the Province of Ontario and the federal laws of Canada
   applicable therein".
4. **(BLOCKER) Collapse all three brand surfaces in Terms** (Office
   Central, BBI, Brant Basics) down to **Brant Business Interiors Inc.**
   throughout.
5. **(HIGH) Pick one contact email** across all four policies. Default
   to `info@brantbusinessinteriors.com` once the inbox is live; until
   then `sales@brantbusinessinteriors.com`. Remove every `@officecentral.com`
   and `@brantbasics.com` reference.
6. **(HIGH) Add PIPEDA-compliance language** to the Privacy Policy
   (collection, use, disclosure, data-subject rights, privacy officer
   contact, retention).
7. **(HIGH) Add Shipping policy link to the homepage footer.** Even
   after the rewrite, the page is currently not discoverable from the
   site nav.
8. **(MEDIUM) Tighten the Refund Policy:** restocking fee position,
   custom-goods non-returnability, refund timeline, extend damage-notice
   window from 24 hours to 5 business days.
9. **(MEDIUM) Add a single "Last updated: YYYY-MM-DD" line** at the top
   or bottom of each of the four policies, refreshed to the rewrite
   date.
10. **(LOW) Add force majeure + B2B PO-acceptance paragraphs** to Terms.
11. **(LOW) Note CAD currency** explicitly in Terms § 4 Prices and
    Billing.

---

## How to update policies in Shopify Admin

Policy edits do **not** require a theme deploy. They're stored in
Shopify Settings, not in the theme.

1. Open Shopify Admin → **Settings** (bottom-left gear).
2. In the left sidebar choose **Policies**.
3. You will see four editable text areas: Refund policy, Privacy policy,
   Shipping policy, Terms of service. (There is also "Contact
   information" but it is optional.)
4. Click into each, paste the rewritten policy text, and click **Save**.
5. Changes go live immediately on the public-facing `/policies/*` URLs
   and at checkout — no theme push, no deploy step.
6. **Footer/nav link for Shipping Policy:** this is theme-level, not
   policy-level. After Steve writes the Shipping Policy, ask the dev
   team to add a footer link to `/policies/shipping-policy` so the page
   is discoverable from the homepage. (Privacy, Refund, and Terms are
   already linked.)

---

_End of audit._
