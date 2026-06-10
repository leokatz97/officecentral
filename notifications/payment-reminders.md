# Pay After — Payment Reminder Copy (Day 2 & Day 5)

> **STATUS: AWAITING COPY.** Leo is providing the finalized day-2 and day-5 reminder
> copy separately. This file is a version-controlled placeholder so the path exists
> in the PR. **Do not invent this copy** — paste the approved text into the two blocks
> below, replacing the `<<PASTE …>>` markers, then commit.

These reminders are sent by a **scheduled-email / abandoned-invoice app** (see
[REMEDIATION-PLAN.md](../REMEDIATION-PLAN.md), step 6), *not* by a Shopify
notification template. They fire only while the order remains
`financial_status == pending`. Once an order is marked **Paid** in Admin, the app
must stop the sequence for that order.

---

## Day 2 — first reminder

**Subject:**

```
<<PASTE DAY-2 SUBJECT>>
```

**Body:**

```
<<PASTE DAY-2 BODY>>
```

---

## Day 5 — second reminder

**Subject:**

```
<<PASTE DAY-5 SUBJECT>>
```

**Body:**

```
<<PASTE DAY-5 BODY>>
```

---

## Required merge fields (match the invoice block)

Whichever app sends these, the copy must resolve the same data points used in the
Order-confirmation invoice block so the customer sees a consistent invoice:

| Purpose | Invoice block (Shopify notification) | Typical reminder-app equivalent |
|---|---|---|
| Order / invoice number | `{{ name }}` | order name / number merge tag |
| Amount due | `{{ total_price \| money }}` | order total merge tag |
| Customer first name | `{{ customer.first_name }}` | customer first-name merge tag |
| Pay-by-phone line | `1-800-835-9565`, Mon–Fri 8:30 a.m.–5:00 p.m. ET | static text |

Reminder-app merge-tag syntax is **app-specific** and will NOT be Shopify
notification Liquid — confirm the exact tags in the chosen app before sending.
