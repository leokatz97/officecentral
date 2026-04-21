# Delivery + Installation — Shipping Rate Setup

Native Shopify flat-rate tiers approximating 20% of order value. $0 ongoing cost. ~10 min to set up.

## Where to configure
Shopify Admin → **Settings** → **Shipping and delivery** → Under **Shipping** click **Manage rates** on the general shipping profile (the one covering Canada / Ontario).

For each country/zone that Brant ships to, add these **7 flat rates** with the configuration below.

## Rate configuration

For each rate:
1. Click **Add rate** → **Use flat rate**
2. **Rate name:** `Delivery + Installation`  *(keep the name identical across all 7 — customer only ever sees one, based on their cart total)*
3. **Price:** (see table)
4. Click **Add conditions** → **Based on order price** → enter Min / Max

| # | Rate name | Price | Min order | Max order | Effective % at midpoint |
|---|---|---|---|---|---|
| 1 | Delivery + Installation | **$50.00**    | $0.00      | $250.00    | ~20% |
| 2 | Delivery + Installation | **$75.00**    | $250.00    | $500.00    | ~20% |
| 3 | Delivery + Installation | **$150.00**   | $500.00    | $1,000.00  | ~20% |
| 4 | Delivery + Installation | **$350.00**   | $1,000.00  | $2,500.00  | ~20% |
| 5 | Delivery + Installation | **$750.00**   | $2,500.00  | $5,000.00  | ~20% |
| 6 | Delivery + Installation | **$1,500.00** | $5,000.00  | $10,000.00 | ~20% |
| 7 | Delivery + Installation | **$2,500.00** | $10,000.00 | *(no max — or $25,000.00)* | 10–25% |

> **Why min/max non-overlapping?** Shopify shows every rate that matches the cart at checkout. Non-overlapping ranges mean only ONE "Delivery + Installation" rate shows up per cart — clean single-line display.

## Tier 7 — large orders

For orders over $10k (roughly 15% of Brant's historical orders), a flat 20% fee gets punishing ($2,000 on a $10k order, $5,000 on a $25k order). Two ways to handle:

- **Simple**: leave tier 7 as $2,500 with no max — customer pays $2,500 on any order $10k+. Effective rate drops to ~10% at $25k orders, which is more realistic for large deliveries.
- **Quote-based** *(recommended for very large orders)*: also add an **8th option** at this tier — `Contact for delivery quote — Delivery + Installation` at **$0.00**, min $10,000, no max. Customer can pick either "pay $2,500 now" or "contact for quote". If they pick the latter, a follow-up call from Steve sets the final number via draft order.

## Add a pickup / self-arranged option

To keep B2B customers who have their own movers, add one more rate on the same profile:

- **Rate name:** `Pickup or customer-arranged delivery`
- **Price:** `$0.00`
- No condition (always available)

Customer sees a choice at checkout — pay the 20% for Delivery + Installation, or skip it with pickup.

## Testing

After saving:
1. Open an incognito browser on `brantbusinessinteriors.com`
2. Add a $200 item → checkout → confirm "Delivery + Installation — $50.00" appears
3. Add a $600 item → confirm rate switches to $150
4. Add a $12,000 item → confirm rate switches to $2,500

## Rollback
Each rate is deletable individually from the same screen. Removing all 7 restores prior shipping behavior.
