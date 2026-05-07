# Stage 3.2c.5 — Metafield Namespace & Key Selection

**Generated:** 2026-05-07

## Existing metafield namespaces on collections

- `global.title_tag` (string) — Shopify standard SEO field, set on some collections
- `global.description_tag` (string) — Shopify standard SEO field

No `bbi.*` namespace entries found on any collection. Safe to create.

The metafield_definitions REST endpoint returns 404 (it is a GraphQL Admin API endpoint only). Metafields can still be set without a formal definition — they are created on-demand via the REST metafields endpoint.

## Selected keys

| Field | Namespace | Key | Type | Example value |
|---|---|---|---|---|
| Parent hub handle | `bbi` | `parent_hub_handle` | `single_line_text_field` | `seating` |
| Parent hub title | `bbi` | `parent_hub_title` | `single_line_text_field` | `Seating` |

## Liquid access pattern

```liquid
collection.metafields.bbi.parent_hub_handle
collection.metafields.bbi.parent_hub_title
```

## Resolution order in ds-cs-base.liquid

```liquid
{%- assign parent_handle = collection.metafields.bbi.parent_hub_handle
    | default: section.settings.parent_category_handle
    | default: 'business-furniture' -%}
{%- assign parent_title = collection.metafields.bbi.parent_hub_title
    | default: section.settings.parent_category_title
    | default: 'Business Furniture' -%}
```

1. **Metafield** — set by script, covers all 88 base collections
2. **Section setting fallback** — allows per-collection Theme Editor override if needed
3. **Hard default** — 'business-furniture' / 'Business Furniture' (safe top-level fallback, not 'seating')

## Coverage

88 collections mapped (56 newly-flipped + 32 pre-existing shells including highback-seating).
5 additional Stage 1.6 shells added to mapping even though not yet confirmed base (training-desks, wall-storage, waste-recycling, side-tables, standing-tables) — script skips gracefully if not found.
