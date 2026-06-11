# Office Central / Brant Business Interiors — Shopify Working Repo

Working repository for the Brant Business Interiors (BBI) Shopify cleanup. BBI is the furniture division of Brant Basics, owned by Office Central (founded 1964). B2B institutional Canadian buyers — school boards, hospitals, municipalities, OECM-eligible.

- **Store:** [brantbusinessinteriors.com](https://www.brantbusinessinteriors.com)
- **Shopify Admin:** [office-central-online](https://admin.shopify.com/store/office-central-online)
- **Contact owner:** Leo (leo@venn.ca) · working with Steve Katz

---

## Start here every session

| Need | File |
|---|---|
| **The live task list** — what's done, in progress, blocked | [docs/plan/shopify-fix-plan.md](docs/plan/shopify-fix-plan.md) |
| **Most recent status snapshot** | [docs/plan/status-snapshot-2026-04-20.md](docs/plan/status-snapshot-2026-04-20.md) |
| **Interactive HTML checklist** (the `update-checklist` skill writes here) | [previews/website-fix-checklist.html](previews/website-fix-checklist.html) |
| **Parking lot of ideas** (not active work) | [docs/plan/ideas-backlog.md](docs/plan/ideas-backlog.md) |
| **Brand voice + ICP + messaging** | [docs/strategy/icp.md](docs/strategy/icp.md) |
| **Approved product-description samples** | [docs/strategy/voice-samples.md](docs/strategy/voice-samples.md) |
| **Script reference** — what each script does + how to run | [scripts/README.md](scripts/README.md) |

---

## Folder map

```
.
├── docs/            Plans, strategy, workflows, review artifacts
│   ├── plan/        Active fix plan + status snapshots + idea backlog
│   ├── strategy/    Brand voice, ICP, segment analysis, competitor research
│   ├── workflows/   How-to runbooks (shipping tiers, taxonomy, design)
│   └── reviews/     Auto-generated review artifacts (for Steve's approval)
├── scripts/         50 Python/Node helpers — read/write Shopify, clean data
├── data/            Everything scripts read/write (CSVs, JSON, logs, backups)
│   ├── specs/       Per-product spec JSON from lookup-specs.py (Hero 100)
│   ├── reports/     Proposal CSVs (tags, industry) — source of truth for pushes
│   ├── redirects/   URL redirect CSVs for Shopify Admin upload
│   ├── exports/     Full Shopify product/order exports (reference snapshots)
│   ├── backups/     Pre-change snapshots (menus, products, collections)
│   ├── logs/        Push audit trails (timestamped JSON)
│   └── oci-photos/  48 real project photos scraped from officecentral.com
├── previews/        Browser-viewable HTML — the checklist, review pages, before/afters
├── theme/           Shopify theme code (layouts/sections/snippets/templates)
└── .claude/         Launch configs + agent tooling — ignore unless changing harness
```

---

## Running scripts

Most scripts follow the same pattern:

```bash
python3 scripts/<name>.py            # dry run (default — shows what would change)
python3 scripts/<name>.py --live     # actually writes to Shopify
python3 scripts/<name>.py --limit=10 # smoke-test on first 10
```

- Credentials live in `.env` (`SHOPIFY_TOKEN=...`). Never commit `.env`.
- Every `push-*` script backs up to `data/backups/` and logs to `data/logs/` before writing.
- See [scripts/README.md](scripts/README.md) for the per-script reference grouped by purpose.

---

## Previewing HTML locally

```bash
python3 scripts/serve-previews.py    # serves previews/ at http://localhost:8080/
```

The **website-fix-checklist** opens at [http://localhost:8080/website-fix-checklist.html](http://localhost:8080/website-fix-checklist.html).

---

## Metafields the theme reads

The theme only **reads** metafields (never writes them — set via Admin API / scripts). Canonical registry of the custom namespaces + keys the live theme depends on:

| Namespace.key | Type | Read by | Purpose |
|---|---|---|---|
| `collection.metafields.faq.items` | `list.single_line_text_field` | `ds-cs-base.liquid` (FAQ band) → `bbi-faq-jsonld.liquid` | Collection FAQ source of truth. One `"Question\|\|Answer"` string per list entry; entries missing the `\|\|` delimiter are skipped. Drives the visible accordion **and** the FAQPage JSON-LD (the two are byte/decode-equal). Added in Step 2.1; populated per category page in Step 2.2. |
| `article.metafields.faq.items` | `list.single_line_text_field` | `ds-article.liquid` (FAQ section + FAQPage JSON-LD) | Same `"Question\|\|Answer"` convention for blog articles. Populate only where the post has real, visible on-page Q&A (Google requires markup to mirror the visible section). |
| `collection.metafields.bbi.parent_hub_handle` | `single_line_text_field` | `ds-cs-base.liquid` (breadcrumb + parent-hub derivation) | Handle of the parent category hub for a sub-collection (e.g. `seating`). Set on `bariatric-seating` in Step 2.0 when it moved to `templateSuffix=base`. Section-setting fallback applies when the metafield is blank. |
| `collection.metafields.bbi.parent_hub_title` | `single_line_text_field` | `ds-cs-base.liquid` (breadcrumb label) | Display title of the parent hub (e.g. `Seating`). Pairs with `parent_hub_handle`. |
| `product.metafields.specs.*` | mixed | `bbi-product-jsonld.liquid` (`additionalProperty[]`) + PDP spec table | Per-product spec fields from the enrichment pipeline (Hero 100). See `docs/strategy/brand-canonical-map.md` for the `specs.manufacturer` canonical vocabulary. |
| `*.metafields.global.title_tag` / `global.description_tag` | `single_line_text_field` | Shopify SEO meta (`<title>` / `<meta name="description">`) | Native SEO title/meta; always apply regardless of template. |

> JSON-LD emitter inventory (which snippet emits what schema, per surface) lives in [docs/audits/schema-audit-2026-05-27.md](docs/audits/schema-audit-2026-05-27.md).

---

## Working context — critical

- **OECM supplier partner:** Both Office Central and Brant Basics are verified OECM partners. Ontario school boards / hospitals / libraries / universities / municipalities can buy from BBI through OECM without open tender. No Ontario competitor has this status.
- **"Keep every product live" strategy:** Do not archive or clearance products. Unbuyable items (sold-out / $0-price / showcase) stay live with a **Request a Quote** CTA.
- **Archive, never delete:** If a product must be cut, archive or unpublish — never delete. Prefer unpublish when sold history exists.
