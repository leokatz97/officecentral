# Locked Tn References
**Created:** 2026-05-08
**Purpose:** Visual design references (screenshots or HTML exports) that serve as pixel-diff targets for BBI template verification.

---

## What goes here

A "locked Tn reference" is an approved visual state for a given template (T1–T6). It is either:

1. A **static HTML export** from Claude Design (approved by Steve), or
2. A **PNG screenshot** of the live dev-theme page captured after Steve's visual QA sign-off.

Once locked, this reference is the target for `scripts/diff-bbi-baselines.py`. A page only stays ✅ if it passes visual diff ≤5% against its locked reference after any change.

---

## File naming convention

For HTML exports from Claude Design:
```
T{n}-{template-name}-LOCKED-{date}.html
```

For dev-theme screenshots:
```
T{n}-{slug}-{viewport}px-LOCKED-{date}.png
```

Examples:
- `T3-category-hub-LOCKED-2026-04-29.html` — already exists at `data/design-photos/screens-t3-LOCKED-2026-04-29/`
- `T4-highback-seating-1280px-LOCKED-2026-05-08.png` — to be created

---

## Current reference status (as of 2026-05-08)

| Template | Reference | Location | Status |
|---|---|---|---|
| **T1 — Homepage** | DS-0 screen export + anti-regression baseline | `data/design-photos/screens-v1-2026-04-28/`, `data/design-photos/ANTI-REF-baseline-2026-04-27-homepage.png` | ✓ LOCKED — Steve approved |
| **T2 — Shop-All (Business Furniture)** | Claude Design T2 locked standalone HTML | `data/design-photos/screens-t2-locked-2026-04-28/01-02-LOCKED-standalone.html` | ✓ LOCKED — Steve approved |
| **T3 — Category Hub** | Claude Design T3 locked standalone HTML | `data/design-photos/screens-t3-LOCKED-2026-04-29/01-03-LOCKED-standalone.html` | ✓ LOCKED — Steve approved |
| **T4 — Sub-collection** | No screenshot locked yet | — | ✗ NOT LOCKED — needs Steve sign-off on dev theme |
| **T5 — PDP** | Claude Design T5 export (design mockup, not rendered page) | `data/design-photos/screens-t5-2026-05-04/` | ✗ BLOCKED — `ds-pdp-base.liquid` not built |
| **Cart** | None | — | ✗ BLOCKED — cart rebuild not started |
| **404** | None | — | ✗ BLOCKED — 404-1 not started |
| **Blog hub** | None | — | ✗ BLOCKED — BLOG-TPL-1 not started |
| **Article** | None | — | ✗ BLOCKED — BLOG-TPL-1 not started |
| **RFQ Modal** | None | — | ✗ BLOCKED — LEAD-3 not started |

---

## What needs Steve's decision before locking

The following templates need a **rendered page** (not just a Claude Design mockup) and **Steve's sign-off** before the locked screenshot can be taken:

| Template | What Steve needs to do | Tooling |
|---|---|---|
| T4 sub-collection | View `/collections/highback-seating` on dev theme; confirm design is acceptable | `shopify theme dev` + manual QA |
| T5 PDP | View a Hero-100 product page on dev theme after Stage 4b build; confirm design is acceptable | `shopify theme dev` + manual QA |
| Cart | Decide: rebuild to BBI design or leave as Starlite (per architecture intent §2m) | Decision only |
| 404 | View custom 404 page on dev theme after 404-1 build | `shopify theme dev` + manual QA |
| Blog/Article | View empty blog hub on dev theme after BLOG-TPL-1 build | `shopify theme dev` + manual QA |
| RFQ Modal | Review modal design in context of quote page after LEAD-3 build | `shopify theme dev` + manual QA |

---

## How to lock a new reference (workflow)

1. **Build + deploy** the template to the dev theme.
2. **Steve does visual QA** — opens the page in the browser, confirms it matches the design intent.
3. **Steve gives go-ahead** verbally or in Slack: "Lock this."
4. **Run capture script:**
   ```bash
   python3 scripts/capture-bbi-baselines.py --url http://127.0.0.1:9292/path/to/page
   ```
5. **Copy the captured PNG to this directory** with the naming convention above.
6. **Update `data/baselines/locked/`** by running:
   ```bash
   python3 scripts/capture-bbi-baselines.py --lock
   ```
7. **Update the status table** in this README.
8. **Commit** the new reference file and README update.

---

## How to run a diff check

```bash
# Capture current dev-theme screenshots
python3 scripts/capture-bbi-baselines.py

# Diff against locked baseline
python3 scripts/diff-bbi-baselines.py

# Output: data/reports/diff-baselines-{timestamp}.csv + diff PNGs at data/baselines/_diff/
```

A result of PASS (≤5% delta) on all pages = visual parity confirmed.

---

## Notes

- The `data/design-photos/screens-t3-LOCKED-2026-04-29/` and `screens-t2-locked-2026-04-28/` directories contain HTML exports, not PNGs. These can be used as a visual reference by rendering them in a browser, but cannot be directly used with `diff-bbi-baselines.py` (which requires PNGs). For pixel-diffing, capture a screenshot of the dev-theme rendering and lock that PNG.
- T4 and T5 references must be dev-theme screenshots, not Claude Design mockups, because the dev-theme rendering may differ from the mockup in font loading, image sizing, and responsive breakpoints.
