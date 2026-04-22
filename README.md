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

## Working context — critical

- **OECM supplier partner:** Both Office Central and Brant Basics are verified OECM partners. Ontario school boards / hospitals / libraries / universities / municipalities can buy from BBI through OECM without open tender. No Ontario competitor has this status.
- **"Keep every product live" strategy:** Do not archive or clearance products. Unbuyable items (sold-out / $0-price / showcase) stay live with a **Request a Quote** CTA.
- **Archive, never delete:** If a product must be cut, archive or unpublish — never delete. Prefer unpublish when sold history exists.
