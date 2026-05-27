# Morning Image Swaps — 4 hero images, post-launch hotfix discipline

Paste in fresh Claude Code session **AFTER** running the morning 24h monitor checks (GSC Coverage + GA4 Acquisition + Steve's quote inbox).

~30-40 min with 4 halts (one per image). Each swap surfaces:
1. Mapping of where the current image is referenced
2. Per-location decision (replace all vs select subset)
3. Apply + verify on LIVE
4. Re-render in headless across mobile + desktop

---

## Context for Claude Code

- **Date:** 2026-05-27 (Day 1 of 24h monitor period)
- **Site state:** BBI LIVE since 2026-05-26T20:08:47-04:00
- **LIVE theme:** 186373570873
- **Latest commit:** aba4dcd on feature/launch-chain-2026-05-26
- **Discipline:** Same as last night's PRODUCTION-HOTFIX-1 — pre-write backups, LIVE updated_at checks, no !important, theme check baseline must hold

## Source images for swap (provided by Leo)

| # | Surface | Source file |
|---|---|---|
| 1 | Seating collection hero (+ sitewide uses) | `~/Downloads/DBE_6942-8_ML48_VU26_Side.jpg` (mesh-back chair side profile, blue mesh, black seat) |
| 2 | Ergonomic collection hero (+ sitewide uses) | Pull primary PDP image from https://brantbusinessinteriors.com/products/dual-monitor-arm |
| 3 | Education industry hero (+ sitewide uses) | `~/Downloads/165387_-_Artcobell_-_product_grouping_with_intrepid.jpg` (modular classroom with teal chairs, "BELIEVE" art, kidney tables) |
| 4 | Homepage main hero (+ sitewide uses, og:image chain) | `~/Downloads/main_page/hero.jpg` OR `~/Downloads/main_page.zip` extracted hero.jpg (woman at sit-stand desk, teal accent chairs, bamboo, modular shelving) |

If files aren't at the exact paths above, search ~/Downloads/ for the patterns:
- `DBE_6942*` for #1
- `dual-monitor-arm` or `monitor-arm` for the PDP URL fetch for #2
- `165387*Artcobell*` for #3
- `hero.jpg` inside main_page* zip/folder for #4

---

## The prompt

```
You are running MORNING IMAGE SWAPS — 4 hero image replacements
on LIVE, post-launch hotfix discipline.

Prerequisites: Leo should have already run morning 24h monitor
checks per docs/plan/launch-4-24h-monitor-2026-05-26.md. If site
shows red flags from those checks, surface and pause this work.

— READ FIRST —

  1. CLAUDE.md (auto-loaded)
  2. BBI-Session-Kickoff/01-safety-preflight.md — preflight
  3. BBI-Session-Kickoff/bbi-build-state.md — confirm we're on
     feature/launch-chain-2026-05-26 @ aba4dcd or a new branch
     descendant
  4. docs/plan/launch-4-24h-monitor-2026-05-26.md — for red-flag
     awareness

— HARD RULES —

  - LIVE theme 186373570873 is the active surface. Writes go
    directly to production.
  - LIVE updated_at re-check before EACH write
  - Pre-write backup for each image being replaced
  - No !important
  - Theme check baseline 2855 / 166 must hold
  - 4 halts: one mapping halt PER image before write
  - Branch off feature/launch-chain-2026-05-26 @ aba4dcd:
      git checkout feature/launch-chain-2026-05-26
      git pull
      git checkout -b feature/morning-image-swaps-2026-05-27

═══════════════════════════════════════════════════════════════════════
PHASE 0 — Pre-flight + source image inventory
═══════════════════════════════════════════════════════════════════════

A. Run preflight. Confirm LIVE theme is 186373570873 role:main.

B. Verify all 4 source images are accessible:
   1. Search ~/Downloads/ for `DBE_6942*` → chair image
   2. Search ~/Downloads/ for `dual-monitor-arm*` OR plan to
      fetch from https://brantbusinessinteriors.com/products/dual-monitor-arm
   3. Search ~/Downloads/ for `165387*Artcobell*` → classroom image
   4. Search ~/Downloads/ for `hero.jpg` inside `main_page*` →
      homepage hero
   
   Surface findings. If any can't be located, HALT and ask Leo
   where to find them.

C. For image #2 specifically, if local file doesn't exist:
   - Fetch https://brantbusinessinteriors.com/products/dual-monitor-arm
   - Parse HTML for product media — likely <img> tags or
     product.media in JSON-LD
   - Identify candidate images (PDPs typically have 3-8 images)
   - Download all candidates to /tmp/dual-monitor-arm-candidates/
   - Surface options at Halt 2 so Leo picks which one

D. Branch:
     git checkout feature/launch-chain-2026-05-26
     git pull
     git status  # clean
     git checkout -b feature/morning-image-swaps-2026-05-27

═══════════════════════════════════════════════════════════════════════
PHASE 1 — IMAGE #1: SEATING COLLECTION HERO
═══════════════════════════════════════════════════════════════════════

A. Find current seating collection hero image:
   - Render https://brantbusinessinteriors.com/collections/seating
   - Inspect <img> elements at the hero position
   - Capture: filename, full CDN URL, alt text, dimensions
   
B. Map ALL sitewide uses of this image:
   - grep theme/ for the filename
   - grep theme/ for related "seating" hero variables
   - Check templates/index.json (homepage collection tiles)
   - Check ds-cc-base.liquid (collection card base)
   - Check any industry pages that may feature seating
   - Check og:image references for /collections/seating
   - Build list: file:line → context

C. Source the new image:
   - Locate DBE_6942-8_ML48_VU26_Side.jpg in ~/Downloads/
   - Check dimensions, format, file size
   - Validate it's a real JPEG (file command)

— HALT IMG-1 (MAPPING + DECISION) —

Print to Leo:

  IMAGE SWAP 1 — SEATING COLLECTION HERO
  
  Current image: {filename + CDN URL}
  Alt text: {current}
  Dimensions: {WxH}
  
  Sitewide uses found ({N} locations):
    1. {file:line} — context: {what page surface}
    2. {file:line} — context: ...
    ...
  
  New image source: ~/Downloads/DBE_6942-8_ML48_VU26_Side.jpg
    Dimensions: {WxH}
    File size: {N}KB
    Format: JPEG
  
  Recommendation: {if catalog product shot on white bg,
    flag whether it works as collection hero or if it's
    better suited only on PDP/featured product slots}
  
  EXACT-MATCH APPROVAL (case-sensitive; typos do not fire):
    "fire image-1 sitewide"  → replace at all {N} locations
    "fire image-1: 1, 3"     → replace at specific locations only
    "skip image-1"           → defer this swap
    "stop"                   → halt this session

Wait for response. Only proceed on exact match.

ON apply approval:

D. Pre-write LIVE updated_at check.
E. Pre-write backup of:
   - Current image asset (download from CDN to backup dir)
   - Each Liquid file being modified
   Backup to: data/backups/image-swap-seating-pre-{ts}/

F. Upload new image to theme/assets/ via Admin API
   OR upload to Shopify Files if section.settings.{name}.image
   is the reference path
   - Use appropriate filename (canonicalize, e.g.,
     bbi-seating-hero-2026-05-27.jpg)

G. Update each Liquid reference per Leo's approval.

H. Push affected files to LIVE 186373570873.

I. Wait 30 seconds for CDN propagation, THEN verify each push
   by API re-fetch byte-match. Skipping the wait risks a
   false-pass where the immediate re-fetch hits cache but
   customers still see the old image.

J. Re-render affected pages in headless at mobile + desktop:
   - https://brantbusinessinteriors.com/collections/seating
   - Any other affected page
   Confirm new image loads + dimensions look right.

K. Theme check baseline 2855 must hold.

— HALT IMG-1 COMMITTED (REAL-DEVICE CHECK) —

Print to Leo:

  IMAGE 1 COMMITTED — REAL-DEVICE CHECK

  Wait 60 seconds for CDN propagation (or hard refresh on phone).

  Open https://brantbusinessinteriors.com/collections/seating
  on phone. Verify:
  - New image renders (not old cached version)
  - Image looks right at mobile portrait orientation
  - Page loads at normal speed
  - No layout shift or visible regression

  EXACT-MATCH APPROVAL (case-sensitive):
    "image-1 good"     → proceed to image 2
    "image-1 issue: X" → halt, diagnose
    "rollback image-1" → restore from backup + re-push

Wait for response. Only proceed on exact match.

═══════════════════════════════════════════════════════════════════════
PHASE 2 — IMAGE #2: ERGONOMIC COLLECTION HERO
═══════════════════════════════════════════════════════════════════════

A. Find current ergonomic collection hero:
   - Render https://brantbusinessinteriors.com/collections/ergonomic-products
   - Identify current hero image

B. Map ALL sitewide uses (same pattern as Phase 1).

C. Source the new image:
   - If ~/Downloads/dual-monitor-arm*.jpg exists locally, use that
   - Otherwise fetch from
     https://brantbusinessinteriors.com/products/dual-monitor-arm
     and parse <script type="application/ld+json"> for Product
     image array
   - PDPs typically have multiple images (primary + alt angles + 
     lifestyle). Surface options at halt for Leo to pick.

— HALT IMG-2 (PDP IMAGE PICK + MAPPING DECISION) —

Print to Leo:

  IMAGE SWAP 2 — ERGONOMIC COLLECTION HERO
  
  Current image: {filename + CDN URL}
  
  Sitewide uses: {N} locations}
    {list}
  
  Source PDP: /products/dual-monitor-arm
  Available PDP images ({N} found):
    1. {URL or filename} — primary, {WxH}
    2. {URL or filename} — angle 2, {WxH}
    3. ...
  
  EXACT-MATCH APPROVAL (case-sensitive; typos do not fire):
    "fire image-2 sitewide pdp-N"  → use PDP image #N at all locs
                                     (e.g. "fire image-2 sitewide pdp-1")
    "fire image-2 pdp-N: 1, 3"     → use PDP image #N at locs 1+3 only
    "skip image-2"                 → defer this swap
    "stop"                         → halt this session

Wait for response. Only proceed on exact match. Then apply per
same pattern as Phase 1 (pre-write backup, LIVE updated_at check,
push, 30s CDN propagation wait, byte-match verify, re-render).

— HALT IMG-2 COMMITTED (REAL-DEVICE CHECK) —

Print to Leo:

  IMAGE 2 COMMITTED — REAL-DEVICE CHECK

  Wait 60 seconds for CDN propagation (or hard refresh on phone).

  Open https://brantbusinessinteriors.com/collections/ergonomic-products
  on phone. Verify:
  - New image renders (not old cached version)
  - Image looks right at mobile portrait orientation
  - Page loads at normal speed
  - No layout shift or visible regression

  EXACT-MATCH APPROVAL (case-sensitive):
    "image-2 good"     → proceed to image 3
    "image-2 issue: X" → halt, diagnose
    "rollback image-2" → restore from backup + re-push

Wait for response. Only proceed on exact match.

═══════════════════════════════════════════════════════════════════════
PHASE 3 — IMAGE #3: EDUCATION INDUSTRY HERO
═══════════════════════════════════════════════════════════════════════

A. Find current education industry hero:
   - Render https://brantbusinessinteriors.com/pages/education
   - Identify current hero image

B. Map sitewide uses.

C. Source: ~/Downloads/165387_-_Artcobell_-_product_grouping_with_intrepid.jpg

— HALT IMG-3 (MAPPING + DECISION) —

Same format as Phase 1 (current image, sitewide uses, new image
metadata, recommendation).

  EXACT-MATCH APPROVAL (case-sensitive; typos do not fire):
    "fire image-3 sitewide"  → replace at all {N} locations
    "fire image-3: 1, 3"     → replace at specific locations only
    "skip image-3"           → defer this swap
    "stop"                   → halt this session

Wait for response. Only proceed on exact match. Apply per same
pattern as Phase 1 (pre-write backup, LIVE updated_at check,
push, 30s CDN propagation wait, byte-match verify, re-render).

— HALT IMG-3 COMMITTED (REAL-DEVICE CHECK) —

Print to Leo:

  IMAGE 3 COMMITTED — REAL-DEVICE CHECK

  Wait 60 seconds for CDN propagation (or hard refresh on phone).

  Open https://brantbusinessinteriors.com/pages/education
  on phone. Verify:
  - New image renders (not old cached version)
  - Image looks right at mobile portrait orientation
  - Page loads at normal speed
  - No layout shift or visible regression

  EXACT-MATCH APPROVAL (case-sensitive):
    "image-3 good"     → proceed to image 4
    "image-3 issue: X" → halt, diagnose
    "rollback image-3" → restore from backup + re-push

Wait for response. Only proceed on exact match.

═══════════════════════════════════════════════════════════════════════
PHASE 4 — IMAGE #4: HOMEPAGE MAIN HERO (HIGHEST STAKES)
═══════════════════════════════════════════════════════════════════════

This is the homepage hero. Higher stakes than the other 3 — it's
the first impression for every visitor + powers the og:image
chain for any page without per-page og:image.

A. Find current homepage hero:
   - Render https://brantbusinessinteriors.com/
   - The current hero is hp-hero-office-breakout.jpg (shipped
     in HP-HERO-OFFICE-IMG branch as part of Day 12 work)
   - Capture its CDN URL + alt text + dimensions

B. Map sitewide uses:
   - templates/index.json (primary location)
   - Any section that references hp-hero-office-breakout
   - og:image fallback chain (currently og-preview.png on homepage —
     but worth confirming hero isn't doubled-up as og:image elsewhere)
   - Check if any social-share / Twitter card uses it

C. Source new image:
   - Look for hero.jpg in ~/Downloads/main_page/ or
     ~/Downloads/main_page.zip
   - If only the zip exists: unzip to /tmp/main_page-hero/
   - Validate: dimensions, format, file size
   - Note: this image is a lifestyle workspace shot (woman at
     sit-stand desk with laptop + coffee, teal chairs, bamboo,
     modular shelving) — much stronger than the previous
     hero per Leo's choice

D. Aspect ratio check:
   - Homepage hero typically renders at ~16:9 to ~21:9 aspect
     ratio on desktop, taller on mobile (due to object-fit:cover)
   - The hero.jpg from main_page is ~16:9 — should work
   - Surface aspect ratio + crop considerations at halt

— HALT IMG-4 (HOMEPAGE HERO — HIGHEST STAKES) —

Print to Leo:

  IMAGE SWAP 4 — HOMEPAGE MAIN HERO
  
  Current: hp-hero-office-breakout.jpg
    CDN URL: {url}
    Dimensions: {WxH} ({aspect})
    Alt text: {current}
    Used in: {file:line list}
  
  New image: hero.jpg from main_page
    Dimensions: {WxH} ({aspect})
    File size: {N}KB
    
  Image character: Lifestyle workspace shot — woman at sit-
    stand desk with laptop + coffee, teal accent chairs,
    bamboo plant, modular shelving with curated art. Premium
    B2B aesthetic.
  
  Compatibility notes:
    - Aspect ratio: {match / close / needs cropping}
    - object-fit:cover handling: {assessment}
    - Mobile: hero crops differently — center subject
      (woman + desk) should remain visible at portrait crop
  
  Proposed filename: bbi-homepage-hero-2026-05-27.jpg
    (preserves dating; allows easy rollback to
    hp-hero-office-breakout.jpg by reverting)
  
  Recommendation: {render side-by-side comparison at desktop
    1920 + mobile 393 before approving — high-stakes swap}
  
  EXACT-MATCH APPROVAL (case-sensitive; typos do not fire):
    "show comparison"        → render side-by-side first
    "fire image-4 sitewide"  → ship to all locations
    "fire image-4: 1"        → only specific location
    "skip image-4"           → defer this swap
    "stop"                   → halt this session

Wait for response. Only proceed on exact match.

ON apply: same pattern as Phases 1-3. Pre-write backup, push
to LIVE, 30s CDN propagation wait, byte-match verify, re-render
at multiple viewports including mobile portrait.

CRITICAL: After homepage hero swap, also verify:
- Lighthouse Performance score doesn't regress >5 points
  (large hero image affects LCP)
- og:image chain still works correctly on homepage
- LCP element renders within target (≤2.5s mobile)

— HALT IMG-4 COMMITTED (REAL-DEVICE CHECK) —

Print to Leo:

  IMAGE 4 COMMITTED — REAL-DEVICE CHECK (HOMEPAGE — HIGHEST STAKES)

  Wait 60 seconds for CDN propagation (or hard refresh on phone).

  Open https://brantbusinessinteriors.com/ on phone. Verify:
  - New hero renders (not old cached version)
  - Subject (woman + desk) still visible at mobile portrait crop
  - Page loads at normal speed (LCP ≤ 2.5s target)
  - No layout shift, no visible regression
  - Hero alt text reads correctly to screen reader (if testable)

  EXACT-MATCH APPROVAL (case-sensitive):
    "image-4 good"     → proceed to Phase 5 (commit + handoff)
    "image-4 issue: X" → halt, diagnose
    "rollback image-4" → restore hp-hero-office-breakout.jpg
                         from backup + re-push

Wait for response. Only proceed on exact match.

═══════════════════════════════════════════════════════════════════════
PHASE 5 — COMMIT + HANDOFF
═══════════════════════════════════════════════════════════════════════

After all 4 swaps (or any subset Leo approved):

A. Update bbi-build-state.md with MORNING-IMAGE-SWAPS-2026-05-27 row:
   Includes per-image before/after, locations changed,
   verification results.

B. Commit + push:
     git add theme/  # all modified files
     git add data/backups/image-swap-*-pre-*/  # if backups
       were captured locally (probably gitignored — surface)
     git add BBI-Session-Kickoff/bbi-build-state.md
     git commit -m "MORNING-IMAGE-SWAPS-2026-05-27: {N} hero
       images replaced on LIVE — seating, ergonomic, education,
       homepage. Pre-LAUNCH-1 commits preserved."
     git push -u origin feature/morning-image-swaps-2026-05-27

C. Print final handoff with:
   - Each swap's before/after
   - LIVE updated_at timestamps
   - PR URL for the branch
   - Any post-swap monitoring concerns (especially homepage
     hero LCP impact)

═══════════════════════════════════════════════════════════════════════
FAILURE MODES
═══════════════════════════════════════════════════════════════════════

If LIVE updated_at changes between writes: HALT immediately.

If any source image doesn't exist where expected: HALT, surface,
ask Leo to provide.

If image upload to Shopify fails (size, format, API errors):
surface specific error, may need to resize/recompress before
retry.

If homepage hero swap causes Lighthouse Performance >5 point
regression: HALT, surface, consider:
- Optimize the new image (resize, reformat to WebP/AVIF)
- Defer this swap to Week 1 polish

If any post-swap render shows unexpected layout breaks: 
HALT, roll back from backup, surface details.

If theme check picks up new offenses: roll back affected
writes, surface.

Begin Phase 0.
```
