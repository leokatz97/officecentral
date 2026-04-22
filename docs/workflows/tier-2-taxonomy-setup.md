# Tier 2 Taxonomy — Shopify Admin Setup

Steve's one-page reference for the steps that have to be done manually in the
Shopify admin. Everything script-driven is already handled — this covers the
GUI work.

## Status as of 2026-04-20

- **Primary nav axis: industry** (Business / Educational / Healthcare / Daycare) — preserved from the existing hand-built `main-menu-2` hierarchy
- **Secondary filters: room + type** — 14 smart collections at `/collections/room-*` and `/collections/type-*`, plus `type:*` / `room:*` tags on 584 products
- **Industry tags (`industry:*`)** pushed to 574 products so filters inside type/room collections can narrow by industry
- ***Other Industries*** removed from `main-menu-2`; the 4 core industries + *Shop by Room* + *Shop by Type* + *Look Books* remain
- All scripts live in `scripts/`:
  - `push-taxonomy-tags.py` — type/room/bestseller
  - `push-industry-tags.py` — industry
  - `build-taxonomy-tags.py`, `build-industry-tags.py` — classifiers
  - `create-collections.py`, `set-collection-sort.py` — smart collection setup
  - `update-main-menu.py`, `delete-menu-item.py` — menu via GraphQL
  - `verify-taxonomy.py` — API spot-checks

## Pivot note (later on 2026-04-20)

The plan originally made room + type the *primary* facets and pushed industry to Tier 5 landing pages. Steve reviewed the live result and pivoted: the store already had a 60+ sub-category industry hierarchy in `main-menu-2` that was the right primary nav. Room + type became secondary filter facets instead. The type/room work all carries forward unchanged — only the framing changed, plus an additional `industry:*` tag on each product.

## Step 1 — Create the 14 smart (automated) collections

Shopify admin → **Products → Collections → Create collection**. For each row
below, set:
- **Title:** as listed
- **Collection type:** Smart / Automated
- **Conditions:** *Products must match all conditions* → `Product tag` → `is equal to` → [Tag]
- **Sort order:** Manually (we push the order from `set-collection-sort.py` next)
- **Handle** (in the SEO section): must match exactly — this is what the sort-order script looks up

| Collection title | Handle | Tag |
|---|---|---|
| Chairs | `type-chairs` | `type:chairs` |
| Desks | `type-desks` | `type:desks` |
| Tables | `type-tables` | `type:tables` |
| Storage | `type-storage` | `type:storage` |
| Accessories | `type-accessories` | `type:accessories` |
| Lounge Seating | `type-lounge` | `type:lounge` |
| Outdoor | `type-outdoor` | `type:outdoor` |
| Private Office | `room-private-office` | `room:private-office` |
| Boardroom | `room-boardroom` | `room:boardroom` |
| Reception | `room-reception` | `room:reception` |
| Open Plan | `room-open-plan` | `room:open-plan` |
| Training Room | `room-training-room` | `room:training-room` |
| Break Room | `room-break-room` | `room:break-room` |
| Lounge | `room-lounge` | `room:lounge` |

Budget 15–20 minutes for all 14.

## Step 2 — Push velocity-sorted order

Once the collections exist:

```bash
python3 scripts/set-collection-sort.py               # dry-run first
python3 scripts/set-collection-sort.py --live        # write to Shopify
```

This fetches each collection by handle and PUTs a manual sort order — highest
sold_revenue first, never-sold products last.

## Step 3 — Rebuild the main nav menu

Shopify admin → **Online Store → Navigation → Main menu**. Replace existing
with:

```
Shop by Room     Shop by Type     Industries           About    Contact
  Private Office    Chairs            Health Centres
  Boardroom         Desks             Schools
  Reception         Tables            Government
  Open Plan         Storage           First Nations
  Training Room     Accessories       Engineering
  Break Room        Lounge Seating    Non-Profits
  Lounge            Outdoor
```

- "Shop by Room" children → link to `/collections/room-private-office`, etc.
- "Shop by Type" children → link to `/collections/type-chairs`, etc.
- "Industries" children → link to the Tier 5 landing pages (`/pages/health-centres`, etc. — these don't exist yet, they'll be built in Tier 5)

## Step 4 — Enable storefront filters on collection pages

Shopify admin → **Online Store → Themes → Customize** → **Collection template**.
In the theme editor sidebar, enable:

- **Filter by price**
- **Filter by product availability**
- **Filter by product tag** — add group for `type:*` and `room:*` so buyers can filter within a collection
- **Sort by** dropdown (default to "Manually" since we pushed a manual order)

## Step 5 — Sitemap resubmit

Once collections are live: Google Search Console → **Sitemaps** → resubmit
`https://brantbusinessinteriors.com/sitemap.xml`. Collections auto-include.

## Verification after each step

```bash
# After step 2, confirm products got the right tags:
python3 scripts/verify-taxonomy.py --sample=30
```

Then incognito-load a few collection pages and confirm top-sellers appear first.

## If something goes wrong

- **Wrong tag applied to a product** — edit the CSV, re-run `push-taxonomy-tags.py --live`. It only appends, so no manual cleanup needed. To remove a bad tag, edit it out in Shopify admin directly (tags field on product detail page).
- **Collection shows wrong products** — the tag condition is wrong; edit the collection's smart rule.
- **Sort order got clobbered by a Shopify action** — re-run `set-collection-sort.py --live`.
