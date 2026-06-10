# REMEDIATION PLAN — "Pay After" pending-order invoice email

**Problem:** Orders placed through the **Pay After** payment method land as
`financial_status = pending` with **$0 received** (transaction `kind = SALE`,
`status = PENDING`), but Shopify auto-sends the standard **Order confirmation**
email, which reads like a completed purchase — and no payment request ever goes
out. Customers think they're done; BBI never gets paid (several pending orders
have even been **fulfilled** — goods shipped, unpaid).

**Fix:** Make the Order-confirmation email render as an **invoice** when the
order is unpaid, change its subject accordingly, and add a day-2 / day-5 payment
reminder sequence. Shopify notification templates **cannot** be edited via Admin
API or CLI, so the template edits are **manual** (paste-by-hand in
*Settings → Notifications*). This repo version-controls the exact copy.

Legend: **CODE-DONE** = done in this PR · **MANUAL-MINE** = Leo does it in Shopify Admin.

---

## Step 1 — Subject line → conditional invoice/confirmation — **CODE-DONE / MANUAL-MINE**

- **CODE-DONE:** Canonical subject saved at
  [`notifications/order-confirmation-subject.liquid`](notifications/order-confirmation-subject.liquid).
- **MANUAL-MINE:** *Settings → Notifications → Order confirmation → Edit*. Replace
  the **Email subject** field with the exact contents of that file:
  ```liquid
  {% if financial_status == 'pending' %}Invoice {{ name }} — payment required to release your order{% else %}Order {{ name }} confirmed — thank you{% endif %}
  ```

## Step 2 — Paste the invoice block at the TOP of the email body — **CODE-DONE / MANUAL-MINE**

- **CODE-DONE:** Canonical block saved at
  [`notifications/order-confirmation-invoice-block.liquid`](notifications/order-confirmation-invoice-block.liquid).
- **MANUAL-MINE:** In the same template's **Email body** code editor, paste the
  entire block **above the existing template markup** (before the first
  `<table>` / Liquid the default template ships with). It self-gates: the whole
  block only renders when `financial_status == 'pending'`, so paid orders are
  unaffected and still show the normal confirmation. The default order-summary
  table below it is intentionally kept ("The order summary below is for your records.").

## Step 3 — Conditional headline — **MANUAL-MINE**

- **MANUAL-MINE:** The default template has a hero/title line (typically
  `Thank you for your purchase!` or `Order {{ name }}`). Wrap it so unpaid orders
  don't say "thank you for your purchase". Suggested wrap (uses only validated
  variables — see PR validation):
  ```liquid
  {% if financial_status == 'pending' %}Invoice — payment required{% else %}Thank you for your purchase!{% endif %}
  ```
  Place this inside the existing title element; do not add a second `<h1>`.

## Step 4 — Preview — **MANUAL-MINE**

- **MANUAL-MINE:** Use the template editor **Preview**. Confirm: subject reads
  "Invoice #… — payment required…", the invoice block renders at the top with the
  pay-by-phone line and amount due, and the order summary still appears below.
  (Preview uses sample data; `financial_status` in preview may show paid — verify
  the live behaviour with the test send in Step 5.)

## Step 5 — Send a real test through "Pay After" — **MANUAL-MINE**

- **MANUAL-MINE:** Place a low-value live test order using the **Pay After**
  method (or use *Send test* if the template editor offers a pending sample).
  Confirm the received email shows the **invoice** variant, the amount matches
  `total_price | money`, and the phone number / hours are correct. Then **Save**.

## Step 6 — Day-2 / Day-5 payment reminders (app) — **MANUAL-MINE**

- **CODE-DONE:** Copy scaffold + required merge fields at
  [`notifications/payment-reminders.md`](notifications/payment-reminders.md)
  (**awaiting Leo's finalized day-2/day-5 copy** — paste it in, then commit).
- **MANUAL-MINE:** Shopify has **no native** "unpaid order reminder" automation,
  and reminder emails are **not** a notification template — install an app that
  watches `financial_status == pending` orders and sends a timed sequence, e.g.
  a "payment reminder / unpaid order" app or Shopify **Flow** + email action.
  Configure: trigger on order created with pending status, send at +2 days and
  +5 days, and **stop the sequence when the order is marked Paid**. Wire the
  app's merge tags to order number, amount due, and customer first name.
  *(Claude cannot install apps — config instructions only.)*

## Step 7 — Confirm sender email — **MANUAL-MINE**

- **MANUAL-MINE:** *Settings → Notifications → Sender email*. Audit shows shop
  `contactEmail = info@brantbusinessinteriors.com`. Confirm the sender is a
  monitored BBI inbox (so customer replies / "how do I pay?" land somewhere
  staffed) and that it's **verified** in Shopify (unverified senders get spam-
  filtered — fatal for an invoice the customer must act on). Align the reminder
  app's sender with this address.

---

## Post-deploy verification — **MANUAL-MINE**

- The **next** real Pay After order should receive the invoice-variant email.
  Spot-check it, then re-run the pending-orders audit (PR description query) to
  confirm new pending orders are no longer being fulfilled before payment.

## Out of scope for this PR (flagged, not fixed)

- **Already-fulfilled unpaid orders** (e.g. #1242 $6,186.64, #1246, #1245, #1244,
  #1247, #1249 — all FULFILLED + PENDING): these need **manual collection** by
  Steve; this fix only prevents recurrence. See PR description.
- The lone **`quotify`** tag on #1247 → verify whether a quote app is still
  installed and sending its own emails (possible duplicate-notification risk).
