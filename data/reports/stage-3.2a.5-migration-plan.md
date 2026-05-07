# Stage 3.2a.5 — Migration Plan for Stage 3.2c

**Generated:** 2026-05-07  
**Inputs:** Full inventory from `stage-3.2a.5-collection-inventory.csv`, root cause from `stage-3.2a.5-root-cause-analysis.md`, product locations from `stage-3.2a.5-product-location-by-hub.csv`

---

## Migration Strategy: Flip Populated Legacy Collections to template_suffix=base

**Chosen approach:** Apply `template_suffix=base` to the 56 populated legacy sub-collections. Do NOT move products between collections.

**Rationale:**
- Products live in the 56 legacy collections today. Their URLs (`/collections/<handle>`) are established and may be indexed/linked.
- Moving products out of these collections and into the Stage 1.6 shells would require URL redirects, break existing links, and risks inventory fragmentation.
- Flipping `template_suffix` is a single API call per collection with no data movement, no URL changes, and no customer impact.
- The P3-rollout already proved this works: 62/62 succeeded in 5 minutes on 2026-05-06. Re-running is straightforward.

**Post-migration state:** The 36 Stage 1.6 empty shells become redundant (no products will ever reach them via this strategy). They should be evaluated for deletion or consolidation — see §4 below.

---

## §1 — Collections to flip to template_suffix=base (56 collections)

Run `set-sub-collection-suffix.py --live` against exactly these handles. All are populated legacy collections with 0 products currently reaching them via ds-cs-base.liquid.

| Hub | Handle | Products | Collection ID |
|---|---|---|---|
| boardroom | boardroom-conference-meeting | 11 | 473198788921 |
| boardroom | lecterns-podiums | 5 | 487507231033 |
| desks | l-shape-desks-desks | 31 | 473351094585 |
| desks | height-adjustable-tables-desks | 21 | 474620920121 |
| desks | straight-desks-desks | 17 | 473362202937 |
| desks | u-shape-desks-desks | 16 | 474620821817 |
| desks | office-suites-desks | 13 | 473351258425 |
| desks | multi-person-workstations-desks | 9 | 474621018425 |
| desks | table-desks | 6 | 473196134713 |
| desks | reception | 3 | 476571271481 |
| desks | benching-desks | 1 | 473196101945 |
| ergonomic-products | height-adjustable-tables | 19 | 473195905337 |
| ergonomic-products | desktop-sit-stand | 10 | 473196298553 |
| ergonomic-products | monitor-arms | 8 | 473196233017 |
| ergonomic-products | keyboard-trays | 6 | 473196265785 |
| panels-room-dividers | room-dividers-panels-dividers | 13 | 473347686713 |
| panels-room-dividers | desk-top-dividers | 4 | 473196659001 |
| panels-room-dividers | modesty-panels | 2 | 495571730745 |
| seating | medium-back-seating | 49 | 473194561849 |
| seating | mesh-seating | 44 | 472894013753 |
| seating | guest-seating | 39 | 472894112057 |
| seating | leather-faux-seating | 32 | 473194627385 |
| seating | lounge-chairs-seating | 16 | 473280184633 |
| seating | stacking-seating | 16 | 473194922297 |
| seating | stools-seating | 15 | 473280315705 |
| seating | big-heavy-seating | 10 | 473195086137 |
| seating | industrial-seating | 8 | 491934023993 |
| seating | folding-stacking-chairs-carts | 7 | 471653286201 |
| seating | ottomans | 7 | 492979781945 |
| seating | nesting-chairs-chair | 5 | 473350930745 |
| seating | 24-hour-seating | 4 | 473194987833 |
| seating | gaming | 3 | 476853895481 |
| seating | cluster-seating | 2 | 506551140665 |
| storage | bookcases-storage | 13 | 473349914937 |
| storage | storage-cabinets-storage | 13 | 473279463737 |
| storage | fire-resistant-safes-storage | 11 | 473349423417 |
| storage | credenzas | 9 | 487507067193 |
| storage | pedestal-drawers-storage | 9 | 473278906681 |
| storage | lateral-files-storage | 7 | 471657972025 |
| storage | fire-resistant-file-cabinets-storage | 6 | 473349620025 |
| storage | lockers | 6 | 487201374521 |
| storage | vertical-files | 6 | 471782261049 |
| storage | wardrobe-storage | 6 | 473197117753 |
| storage | lateral-storage-combo-storage | 5 | 473370100025 |
| storage | hutch | 2 | 494681751865 |
| storage | end-tab-filing-storage | 1 | 473196921145 |
| tables | meeting-tables | 12 | 473196560697 |
| tables | round-square-tables | 9 | 473196429625 |
| tables | folding-tables-tables | 8 | 473350209849 |
| tables | drafting-tables | 7 | 487507525945 |
| tables | coffee-tables | 5 | 473196364089 |
| tables | end-tables-tables | 5 | 473196396857 |
| tables | table-bases | 5 | 502405628217 |
| tables | training-flip-top-tables | 5 | 486802522425 |
| tables | cafeteria-kitchen-tables | 4 | 473196462393 |
| tables | bar-height-tables | 3 | 473196495161 |

**Script action:** Edit `SUB_COLLECTION_HANDLES` in `scripts/set-sub-collection-suffix.py` to contain only these 56 handles. Run with `--live`. Script handles backup, is idempotent, and has proven 7-second execution time.

**API calls needed:** 56 PUT requests. At 8 req/sec: ~7 seconds.

---

## §2 — Collections already on template_suffix=base with products (1 collection)

| Handle | Products | Status |
|---|---|---|
| highback-seating | 46 | DONE — migrated in Stage 3.2b. No action needed. |

---

## §3 — Schema config mapping for 56 newly-flipped collections

After flipping `template_suffix`, each collection needs `parent_category_handle` and `parent_category_title` set so breadcrumbs show the correct parent hub. The existing `set-base-collection-schemas.py` script handles this — extend `stage-3.2b-schema-mapping.csv` with these 56 rows (or create a new CSV and pass it as input).

| Handle | parent_category_handle | parent_category_title |
|---|---|---|
| boardroom-conference-meeting | boardroom | Boardroom |
| lecterns-podiums | boardroom | Boardroom |
| l-shape-desks-desks | desks | Desks & Workstations |
| height-adjustable-tables-desks | desks | Desks & Workstations |
| straight-desks-desks | desks | Desks & Workstations |
| u-shape-desks-desks | desks | Desks & Workstations |
| office-suites-desks | desks | Desks & Workstations |
| multi-person-workstations-desks | desks | Desks & Workstations |
| table-desks | desks | Desks & Workstations |
| reception | desks | Desks & Workstations |
| benching-desks | desks | Desks & Workstations |
| height-adjustable-tables | ergonomic-products | Ergonomic Products |
| desktop-sit-stand | ergonomic-products | Ergonomic Products |
| monitor-arms | ergonomic-products | Ergonomic Products |
| keyboard-trays | ergonomic-products | Ergonomic Products |
| room-dividers-panels-dividers | panels-room-dividers | Panels & Room Dividers |
| desk-top-dividers | panels-room-dividers | Panels & Room Dividers |
| modesty-panels | panels-room-dividers | Panels & Room Dividers |
| medium-back-seating | seating | Seating |
| mesh-seating | seating | Seating |
| guest-seating | seating | Seating |
| leather-faux-seating | seating | Seating |
| lounge-chairs-seating | seating | Seating |
| stacking-seating | seating | Seating |
| stools-seating | seating | Seating |
| big-heavy-seating | seating | Seating |
| industrial-seating | seating | Seating |
| folding-stacking-chairs-carts | seating | Seating |
| ottomans | seating | Seating |
| nesting-chairs-chair | seating | Seating |
| 24-hour-seating | seating | Seating |
| gaming | seating | Seating |
| cluster-seating | seating | Seating |
| bookcases-storage | storage | Storage & Filing |
| storage-cabinets-storage | storage | Storage & Filing |
| fire-resistant-safes-storage | storage | Storage & Filing |
| credenzas | storage | Storage & Filing |
| pedestal-drawers-storage | storage | Storage & Filing |
| lateral-files-storage | storage | Storage & Filing |
| fire-resistant-file-cabinets-storage | storage | Storage & Filing |
| lockers | storage | Storage & Filing |
| vertical-files | storage | Storage & Filing |
| wardrobe-storage | storage | Storage & Filing |
| lateral-storage-combo-storage | storage | Storage & Filing |
| hutch | storage | Storage & Filing |
| end-tab-filing-storage | storage | Storage & Filing |
| meeting-tables | tables | Tables |
| round-square-tables | tables | Tables |
| folding-tables-tables | tables | Tables |
| drafting-tables | tables | Tables |
| coffee-tables | tables | Tables |
| end-tables-tables | tables | Tables |
| table-bases | tables | Tables |
| training-flip-top-tables | tables | Tables |
| cafeteria-kitchen-tables | tables | Tables |
| bar-height-tables | tables | Tables |

**Script action:** Add these rows to `stage-3.2b-schema-mapping.csv` and re-run `set-base-collection-schemas.py --live`. No Theme Editor manual config needed.

**Note:** 5 Stage 1.6 shells with `unknown` hub also need mapping updates: `training-desks → desks`, `wall-storage → storage`, `waste-recycling → accessories`, `side-tables → tables`, `standing-tables → tables`. Add these rows to the mapping CSV as well.

---

## §4 — Stage 1.6 Empty Shells: Disposition

36 Stage 1.6 shells with `template_suffix=base` and 0 products. After adopting the legacy-flip strategy, these will remain empty.

**Recommendation: Leave in place.** The empty-state screen in `ds-cs-base.liquid` handles 0-products gracefully. Shells produce no SEO harm (no meaningful content to index). Deleting risks breaking any shared URL.

**Potential deletion candidates** (where a populated legacy collection covers the same scope):

| Shell Handle | Possible Legacy Counterpart | Legacy Products |
|---|---|---|
| boardroom-seating | boardroom-conference-meeting | 11 |
| collaborative-tables | meeting-tables | 12 |

These two pairs are semantically close. Flag for Steve's decision. Do not auto-delete.

---

## §5 — Effort Estimate

| Step | Method | Estimated Time |
|---|---|---|
| Re-run P3-rollout for 56 legacy collections | Script (`set-sub-collection-suffix.py --live`) | 5 min |
| Extend schema mapping CSV for 56 legacy + 5 shell-hub fixes | Edit CSV (mapping table in §3) | 15 min |
| Run schema config script for 93 collections | Script (`set-base-collection-schemas.py --live`) | 10 min |
| QA spot-check on dev theme | Browser walkthrough (5 hubs × 3 sub-pages) | 30 min |
| **Total** | | **~60 min** |

No Theme Editor manual config is needed — scripts handle all 93 collections.

---

## §6 — Gaps Not Covered by This Migration

| Gap | Status | Resolution |
|---|---|---|
| 5 P3 targets that still don't exist (monitor-accessories, filing-accessories, mobility-aids, phone-booths, meeting-pods) | Not in Shopify | Create if products exist; defer if not |
| `audio-visual-equipment` (boardroom, 0 products) | No products | No flip needed |
| `accessories` sub-collections with 0 products (chair-accessories, anti-fatigue-mats, technology) | No products | No flip needed |
| `quiet-spaces` (9 products at hub, 0 at any sub) | Products only at hub level | Re-tag products or wait for acoustic-pods stock |

---

## §7 — Top 3 Risks for Stage 3.2c

**Risk 1 (HIGH): Schema config covers only 37 of 93 base collections before Stage 3.2c**  
After Stage 3.2c, there will be 93 total base collections. 56 newly-flipped legacy collections will default to breadcrumb "Seating" without schema config. Run the schema script in the same session as the template flip.  
**Mitigation:** Use the §3 mapping table to extend `set-base-collection-schemas.py` before executing Stage 3.2c.

**Risk 2 (MEDIUM): Duplicate sub-collection entries visible in hubs after migration**  
Several hubs will have both the populated legacy collection (on base template) AND an empty Stage 1.6 shell (also on base template). Hub tile grids reference collections by URL — both will show up if hub templates link to both.  
**Mitigation:** Audit hub JSON template tile links after migration. Remove or redirect tiles pointing to empty shells.

**Risk 3 (MEDIUM): P3-revert rationale is undocumented**  
The revert logs (`revert-sub-suffix-20260507_125554.json`, `revert-sub-suffix-20260507_125644.json`) exist but no git commit or doc explains WHY the P3-rollout was reverted. Stage 3.2c should confirm the blocker is resolved before re-applying.  
**Mitigation:** Leo to confirm no blocker exists for re-applying template flip. If the revert was for a UI/design reason (template wasn't ready), Stage 3.2b completion resolves it.
