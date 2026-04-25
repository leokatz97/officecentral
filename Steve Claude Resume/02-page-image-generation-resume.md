# RESUME: BBI Page Image Generation (generate-page-images.py)

**Project path:** `/Users/leokatz/Desktop/Office Central/`
**Credentials:** `FAL_KEY` and `SHOPIFY_TOKEN` already in `.env`

---

## Status: Script Built & Verified — Live Run Pending

- `scripts/generate-page-images.py` — **fully rebuilt from scratch** (837 lines, all 6 slot types)
- Dry-run verified: 60 slots, 13 OCI skips, 47 generates, est. $1.03–$1.32
- `.claude/skills/bbi-build-page/SKILL.md` — **updated** with photo library block, Step 3 pre-check, and [IF IMAGES ATTACHED] conditional
- **No live images generated yet** — smoke test and full run still needed

---

## Next Steps

### 1. Smoke Test (3 images)
```bash
cd /Users/leokatz/Desktop/Office\ Central
python3 scripts/generate-page-images.py --limit=3 --live
```
Check `data/page-images/` — confirm one image generated, OCI slots show SKIPPED_OCI, manifest and audit log written.

### 2. Review Quality
Open the 3 generated JPEGs. If prompts need adjustment, edit `PAGE_SPECS` in the script before proceeding.

### 3. Full Run (~20 min, ~$1.03–$1.32)
```bash
python3 scripts/generate-page-images.py --live   # type YES at cost prompt
```

### 4. After Generation
Commit everything and run `git-sync` skill.

---

## What the Script Generates

**Model:** `fal-ai/flux/dev`, 28 inference steps, ~$0.025/image
**Endpoint:** `https://fal.run/fal-ai/flux/dev`
**Budget:** $2 total. Cost guard at $2.00 — prompts YES.
**Cost constants:** $0.022 low / $0.028 high per image

### 6 Slot Types:
- **Slot 1** — Page heroes: `hero-product.jpg` + `hero-space.jpg` (landscape_16_9) — every page
- **Slot 2** — Collection hub tiles: `hub-tile.jpg` (square) — desks, storage, home-office
- **Slot 3** — Industry hub tiles: `hub-tile.jpg` (square) — non-profit, professional-services
- **Slot 4** — Brand hub tiles: `hub-tile.jpg` (square) — keilhauer, global-teknion, ergocentric
- **Slot 5** — Homepage featured cards: `featured-card-chair/desk/pods.jpg` (landscape_4_3)
- **Slot 6** — Service section breaks: `section-*.jpg` (landscape_16_9) — design-services, delivery, relocation

### OCI Skip Table (13 slots — never generate these):
| Page | Slot | OCI file |
|---|---|---|
| homepage | hero-space | office-sitting-room-executive-sitting-1.jpg |
| collaboration | hero-space | Subject-Areas-boardroom.jpg |
| acoustic-pods | hero-space | Pods-4-1.jpg |
| healthcare | hero-space | OCI-Healthcare-Carousel-3.jpg |
| education | hero-space | OCI-Education-1.jpg |
| government | hero-space | OCI-Government-Federal-Furniture-Gallery-Image-1.jpg |
| design-services | hero-space | OCI-Planning-Desogn.jpg |
| task-seating | hub-tile | Inspiration-Ergonomics.jpg |
| collaboration | hub-tile | Subject-Areas-boardroom.jpg |
| acoustic-pods | hub-tile | Pods-4-1.jpg |
| healthcare | hub-tile | OCI-Healthcare-Furniture-Gallery-Image.jpg |
| education | hub-tile | OCI-Education-1.jpg |
| government | hub-tile | OCI-Government-Federal-Furniture-Gallery-Image-1.jpg |

### Output Folders:
```
data/page-images/
  homepage/              hero-product.jpg, hero-space.jpg, featured-card-chair.jpg, featured-card-desk.jpg, featured-card-pods.jpg
  task-seating/          hero-product.jpg, hero-space.jpg
  desks/                 hero-product.jpg, hero-space.jpg, hub-tile.jpg
  storage/               hero-product.jpg, hero-space.jpg, hub-tile.jpg
  collaboration/         hero-product.jpg, hero-space.jpg
  home-office/           hero-product.jpg, hero-space.jpg, hub-tile.jpg
  acoustic-pods/         hero-product.jpg, hero-space.jpg
  healthcare/            hero-product.jpg, hero-space.jpg
  education/             hero-product.jpg, hero-space.jpg
  government/            hero-product.jpg, hero-space.jpg
  non-profit/            hero-product.jpg, hero-space.jpg, hub-tile.jpg
  professional-services/ hero-product.jpg, hero-space.jpg, hub-tile.jpg
  design-services/       hero-product.jpg, hero-space.jpg, section-planning.jpg, section-reveal.jpg
  delivery/              hero-space.jpg, section-deliver.jpg, section-install.jpg
  relocation/            hero-space.jpg, section-move.jpg
  oecm/                  hero-space.jpg
  collections-hub/       hero-space.jpg
  industries-hub/        hero-space.jpg
  brands-hub/            hero-space.jpg
  keilhauer/             hero-product.jpg, hero-space.jpg, hub-tile.jpg
  global-teknion/        hero-product.jpg, hero-space.jpg, hub-tile.jpg
  ergocentric/           hero-product.jpg, hero-space.jpg, hub-tile.jpg
```

### Manifest & Logs:
- Manifest CSV: `data/reports/generated-page-images-YYYY-MM-DD.csv`
- Audit log: `data/logs/page-image-generation-YYYYMMDD-HHMMSS.json`

---

## Key Files
- Script: `scripts/generate-page-images.py`
- Pattern reference: `scripts/generate-product-images.py`
- Skill updated: `.claude/skills/bbi-build-page/SKILL.md`
- Backlog ref: `docs/plan/ideas-backlog.md` items #8, #9, #10
