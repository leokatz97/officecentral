# Pay After — Payment Reminder Copy (Day 2 & Day 5)

These reminders are sent by a **scheduled-email / unpaid-invoice app** (see
[REMEDIATION-PLAN.md](../REMEDIATION-PLAN.md), step 6), *not* by a Shopify
notification template. They fire only while the order remains
`financial_status == pending`. Once an order is marked **Paid** in Admin, the app
must stop the sequence for that order.

**Schedule:** **day-2 and day-5 only** — *no* immediate reminder (the Order
confirmation is now the immediate invoice). **Auto-cancel: OFF** to start (do not
let the app cancel/close unpaid orders automatically).

**Token mapping:** `{order}`, `{first_name}`, and `{amount}` below are **generic
placeholders** to be mapped to the chosen app's own merge tokens (syntax is
app-specific and is NOT Shopify notification Liquid — see the table at the
bottom). Confirm the exact tags in the app before sending.

---

## Day 2 — first reminder

**Subject:**

```
Reminder: Invoice {order} is awaiting payment
```

**Body:**

```
Hi {first_name},
A quick reminder that your Brant Business Interiors order {order} is reserved but not yet paid.
Amount due: {amount}
To pay, call 1-800-835-9565 (Mon–Fri, 8:30 a.m.–5:00 p.m. ET) and quote your order number. We accept credit card by phone, Interac e-Transfer, EFT / bank transfer, cheque, and PO / invoice terms for OECM and public-sector accounts.
Already paid? Please disregard this message.
— Brant Business Interiors, a division of Office Central
```

---

## Day 5 — second reminder

**Subject:**

```
Second reminder: Invoice {order} — payment needed to keep your order
```

**Body:**

```
Hi {first_name},
We haven't yet received payment for order {order} (amount due: {amount}), so it's still on hold.
To complete payment, call 1-800-835-9565 (Mon–Fri, 8:30 a.m.–5:00 p.m. ET) and quote your order number. Methods: credit card by phone, Interac e-Transfer, EFT / bank transfer, cheque, or PO / invoice terms.
Questions, or need different arrangements? Just reply or call — we're happy to help.
— Brant Business Interiors · OECM Agreement 2025-470
```

---

## Token mapping (match the Order-confirmation invoice block)

Whichever app sends these, the copy must resolve the same data points used in the
Order-confirmation invoice block so the customer sees a consistent invoice:

| Purpose | Placeholder here | Invoice block (Shopify notification) | Map to app token |
|---|---|---|---|
| Order / invoice number | `{order}` | `{{ name }}` | app order-number merge tag |
| Amount due | `{amount}` | `{{ total_price \| money }}` | app order-total merge tag |
| Customer first name | `{first_name}` | `{{ customer.first_name }}` | app customer-first-name merge tag |
| Pay-by-phone line | (static) | `1-800-835-9565`, Mon–Fri 8:30 a.m.–5:00 p.m. ET | static text |

Reminder-app merge-tag syntax is **app-specific** and will NOT be Shopify
notification Liquid — confirm the exact tags in the chosen app before sending.
