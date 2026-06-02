# BBI Re-sourcing — Provenance Report (2026-06-02)

**Task:** correct `vendor="Brant Business Interiors"` data-errors to real manufacturers (BBI is a dealer, not a manufacturer) — the hard prerequisite for the Brand filter.
**Carry-forward** from the 2026-05-30 brand-recovery audit (PR #62: 183 corrected, 204 left UNKNOWN). Since then `sku-prefix-lookup.yaml` gained deterministic decodes for HDL/IOF/RIC/HZN/MTY, unblocking most of the residual tail.

**Method:** Admin-API GraphQL read of all live `vendor:BBI` products → signal-based sourcing (SKU-prefix primary, per SKU-PREFIX-PATTERNS-ARE-DETERMINISTIC) → CONFIDENT/AMBIGUOUS classification. No Shopify writes, no theme files touched.

## Decisions locked (Leo, 2026-06-02)
- **HDL folded into `Heartwood`** (single clean `brand:heartwood` chip; same brand family as HTW).
- **Scope = tier-1 only (97).** The 18 tier-2 sub-code/line/title promotions defer to the Steve/manual pile.
- **HOLD — report only.** Zero Shopify writes this session; the apply script is staged for a future `--live` go.

## Summary

| Class | N | Action |
|---|---:|---|
| **CONFIDENT — tier 1** (write-ready) | **97** | correct vendor + add `brand:*` (STAGED, held) |
| CONFIDENT — tier 2 (deferred to Steve) | 18 | locked sub-code/line/title; confirm then write |
| AMBIGUOUS | 87 | leave untouched → Steve/manual |
| SKIP (services) | 19 | leave untouched (BBI-as-vendor acceptable) |
| **Total scanned** | **221** | |

**N corrected (planned, held): 97**  ·  **M deferred-to-Steve: 105** (18 tier-2 + 87 ambiguous)  ·  **19 services skipped.**

## Tier-1 confident — manufacturer distribution (the 97)

| Manufacturer | N | brand tag |
|---|---:|---|
| Heartwood | 40 | `brand:heartwood` |
| Intelligent Office Furniture | 26 | `brand:intelligent-office-furniture` |
| Richelieu | 12 | `brand:richelieu` |
| Horizon Furniture | 10 | `brand:horizon-furniture` |
| MityBilt | 9 | `brand:mitybilt` |

## Tier-1 sourcing map (product → manufacturer + signal)

| Handle | SKU sample | → Manufacturer | Signal |
|---|---|---|---|
| av-stand-sa-81-3016 | `HDL-SA81-3016` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-SA81-3016) (sku) |
| cabinet-file-file-right-wardrobe-inv-6524cff | `HDL- INV-6524CFFWR-24` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL- INV-6524CFFWR-24) (sku |
| cord-cover | `HDL-100-WM1300` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-100-WM1300) (sku) |
| credenza-lflf-1 | `HDL-2@INV2236LFX+2272TOP` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-2@INV2236LFX+2272TOP) ( |
| credenza-lfmsu | `HDL-2@INV2236LFX+2272TOP` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-2@INV2236LFX+2272TOP) ( |
| desk-shells | `HDLINV2448DS` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDLINV2448DS) (sku) |
| desk-top-dividers | `HDL-OUT-TM1-1530PLX` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-OUT-TM1-1530PLX) (sku) |
| desk-top-dividers-1 | `HDL-OUTEM1-1524PETST` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-OUTEM1-1524PETST) (sku) |
| educational-student-tables-5-shapes-sizes | `HDL-EDU-SQ48-RPH2` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-EDU-SQ48-RPH2) (sku) |
| fax-printer-machine-stand | `HDL-SA-84-3220` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-SA-84-3220) (sku) |
| folding-chair-cart | `HDL-TLT-CCART` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-TLT-CCART) (sku) |
| height-adjustable-l-shape-71x71 | `HDL-HT-ADJ-LAYOUT #7` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-HT-ADJ-LAYOUT #7) (sku) |
| height-adjustable-l-shape-table-1 | `HDL-CLI-E1-3LEG-3060+244` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-CLI-E1-3LEG-3060+2448 T |
| hutch-5-sizes | `HDLINV3636H` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDLINV3636H) (sku) |
| l-shape-suite-layout-41c | `HDL-Layout 41C` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-Layout 41C) (sku) |
| laminate-modesty-panels | `HDLINV-MP2-1430LAPBLK` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDLINV-MP2-1430LAPBLK) (sku |
| laptop-holder-for-100-ma1c-100-ma2c-monitor- | `HDL-100LPTP` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-100LPTP) (sku) |
| levels-bookcase | `HDL LEV-6532BK` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL LEV-6532BK) (sku) |
| levels-l-shape | `HDL-LEVELS LAYOUT2` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-LEVELS LAYOUT2) (sku) |
| manual-height-adjustable-base | `HDL-900-CRANK` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-900-CRANK) (sku) |
| meeting-table | `HDL-INV-2436TBL-SQ2OFT` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV-2436TBL-SQ2OFT) (sk |
| metal-cross-base-with-levelers | `HDL-900-CROSS-B-27 SIL` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-900-CROSS-B-27 SIL) (sk |
| metal-round-metal-base | `HDL-900-ROU20-SIL` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-900-ROU20-SIL) (sku) |
| metal-square-metal-base | `HDL-900-SQB20-SIL` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-900-SQB20-SIL) (sku) |
| new-pneumatic-single-arm-monitor-stand | `HDL-100-MA1C` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-100-MA1C) (sku) |
| plexiglass-modesty-panels | `HDLINV-MP1-1530PLX` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDLINV-MP1-1530PLX) (sku) |
| reception-unit-72x72 | `HDL-Layout # 15` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-Layout # 15) (sku) |
| round-metal-base | `HDL-900-ROU20SIL` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-900-ROU20SIL) (sku) |
| round-table-29-high | `HDL-R36RT900CROSS30` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-R36RT900CROSS30) (sku) |
| round-table-42 | `HDL-INV42RT-INV-XB26` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV42RT-INV-XB26) (sku) |
| round-table-cross-base-8-colours | `HDLINVR36+	900-CROSS-B-2` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDLINVR36+	900-CROSS-B-27)  |
| sit-stand-1 | `HDL-100-DTHA` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-100-DTHA) (sku) |
| soho-desk-single-pedestal-2-sizes | `HDL-MA11-2448` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-MA11-2448) (sku) |
| taper-leg-table | `HDL-INV-2436TBL-TAPER` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV-2436TBL-TAPER) (sku |
| tucana-elite-training-nesting-tables | `HDL TU-98B-2448TBL` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL TU-98B-2448TBL) (sku) |
| upscale-meeting-boardroom-tables-3-sizes-8-c | `HDL-INV-REC9648-MUP` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV-REC9648-MUP) (sku) |
| upscale-meeting-boardroom-tables-3-sizes-8-c | `HDL-INV-RT9648-MUP` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV-RT9648-MUP) (sku) |
| upscale-table-1 | `HDL-INV-R36-MUPBLK` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV-R36-MUPBLK) (sku) |
| wardrobe | `HDL-INV6518WCL` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL-INV6518WCL) (sku) |
| white-board-magnetic-mobile-on-wheels | `HDL 100-7138MWF` | Heartwood | sku_prefix: SKU prefix HDL (e.g. HDL 100-7138MWF) (sku) |
| banquet-chair-stacking | `HZN-A117V` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-A117V) (sku) |
| corner-maker-12 | `HZN-CM2` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-CM2) (sku) |
| demeter-mid-back-ergonomic-chair-buyers-choi | `HZN-DEM HB` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-DEM HB) (sku) |
| easy-pull-in-out-keyboard-tray | `HZNKL28SG27` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZNKL28SG27) (sku) |
| i-pad-holders | `HZN-ECAPSF02` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-ECAPSF02) (sku) |
| keyboard-tray-multi-adjustable | `HZN-ECA EB02` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-ECA EB02) (sku) |
| keyboard-tray-multi-position | `HZN-JV01` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-JV01) (sku) |
| shoptech-082 | `HZN-082` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-082) (sku) |
| shoptech-2410 | `HZN-2410` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-2410) (sku) |
| staxx-chair | `HZN-NK03` | Horizon Furniture | sku_prefix: SKU prefix HZN (e.g. HZN-NK03) (sku) |
| circular-reception-unit-w-41-r | `IOF-W41R` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-W41R) (sku) |
| credenza-60x20 | `IOF-Typical #W-066` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-Typical #W-066) (sku) |
| credenza-sliding-doors | `IOF-UN6024SC/SC/SLD2` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN6024SC/SC/SLD2) (sku) |
| credenza-storage-hutch | `IOF-UN7224/MP/SC` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN7224/MP/SC) (sku) |
| credenza-storage-storage-with-locks | `IOF-UN6024/SC/SC` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN6024/SC/SC) (sku) |
| display-shelving | `IOF-B2016-17 X 2` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-B2016-17 X 2) (sku) |
| drafting-table | `IOF-Q000111061` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-Q000111061) (sku) |
| drafting-table-custom | `IOF-Typical #W-021` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-Typical #W-021) (sku) |
| l-shape-desk-with-hutch | `IOF-UN72HUTDO43-UN7230TD` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN72HUTDO43-UN7230TD-UN |
| laminate-lockers-1 | `IOF-Lock#003` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-Lock#003) (sku) |
| lateral-file-storage-cabinet-with-shelves-co | `IOF-UN3066LF/SC/GD/21` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN3066LF/SC/GD/21) (sku |
| lateral-file-wood-laminate-2-3-4-drawer-opti | `IOFUN3624LF2` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOFUN3624LF2) (sku) |
| lectern-storage-stand | `IOF-Typical #W-020` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-Typical #W-020) (sku) |
| mobile-machine-stand-with-shelf-on-wheels | `IOF-C901221` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-C901221) (sku) |
| mobile-pedestal-file-file | `IOF IFFM21` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF IFFM21) (sku) |
| modern-grigio-reception-desk | `IOFW10R` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOFW10R) (sku) |
| nutmeg-reception | `IOFW19R` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOFW19R) (sku) |
| pneumatic-single-table | `IOF-PN2420` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-PN2420) (sku) |
| racetrack-conference-table-1-top | `IOFRAPB3660` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOFRAPB3660) (sku) |
| storage-cabinet-with-doors | `IOF-B2016-87` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-B2016-87) (sku) |
| storage-wardrobe-unit | `IOF-UN3072WD/21` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN3072WD/21) (sku) |
| table-desk-height-adjustable | `IOF-HA#014-2460` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-HA#014-2460) (sku) |
| table-tops | `IOF-UN3624TOP/NGM` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN3624TOP/NGM) (sku) |
| temptations-office-suite | `IOF-B2016-62` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-B2016-62) (sku) |
| temptations-office-suite-copy | `IOF-B2016-49` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-B2016-49) (sku) |
| wardrobe-with-lock | `IOF-UN3072SC/WD/24` | Intelligent Office Furniture | sku_prefix: SKU prefix IOF (e.g. IOF-UN3072SC/WD/24) (sku) |
| aktivity-environ-table | `MTY-EN30R` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY-EN30R) (sku) |
| aktivity-rectangle-height-adjustable-table | `MTY-IS-AT2424` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY-IS-AT2424) (sku) |
| contemporary-metal-desk | `MTY- TUT2448.MPL` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY- TUT2448.MPL) (sku) |
| horseshoe-study-table-height-adjustable-c-sh | `MTY-IS-ATC#3660` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY-IS-ATC#3660) (sku) |
| indigenous-medicine-wheel-huddl | `MTY-HDDLGMED#` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY-HDDLGMED#) (sku) |
| metal-apex-desk | `MTYB AP3060.BBF2` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTYB AP3060.BBF2) (sku) |
| metal-desk-laminate-top | `MTY-IS-AP2460.BBF.MOD` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY-IS-AP2460.BBF.MOD) (sku |
| table-round-height-adjustable | `MTY-AT48RMPL` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY-AT48RMPL) (sku) |
| ultima-adjustable-stool | `MTY- IS-S2026` | MityBilt | sku_prefix: SKU prefix MTY (e.g. MTY- IS-S2026) (sku) |
| charging-station-with-a-clamp | `RIC-OME0023A1U1C90` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC-OME0023A1U1C90) (sku) |
| clamp-on-power-bar-and-usb-charging-station | `RIC-23213030` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC-23213030) (sku) |
| desk-power-grommet | `RIC- DS86101P1A1C90` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC- DS86101P1A1C90) (sku) |
| jax-keyboard-tray | `RIC5008479C3` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC5008479C3) (sku) |
| jax-sit-to-stand | `RIC-5008479C3` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC-5008479C3) (sku) |
| momentum-series-combos-keyboard-arm-premium- | `RIC 5007438C3` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC 5007438C3) (sku) |
| power-plant-500222pp90-daisychaining | `RIC500222PP90` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC500222PP90) (sku) |
| power-station-with-3-outlets-and-2-usb | `RIC-201314100` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC-201314100) (sku) |
| sit2stand-series-sit-stand-workstation | `RIC-500S2S001R30` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC-500S2S001R30) (sku) |
| tower-charging-station-with-usb-ports-2-colo | `RIC-PBK2WAY2030` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC-PBK2WAY2030) (sku) |
| triple-monitor-and-ipad-holder | `RIC 500FP23100 & FEL 804` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC 500FP23100 & FEL 804410 |
| two-stage-electric-height-adjustable-table | `RIC 5002L2S244890` | Richelieu | sku_prefix: SKU prefix RIC (e.g. RIC 5002L2S244890) (sku) |

## Tier-2 deferred (18) — locked sub-code / line / title, confirm before writing

| Handle | SKU sample | → Manufacturer | Signal |
|---|---|---|---|
| foundations-next-gen-serenity-safereach-comp | `` | Foundations | direct_name: Foundations Next Gen (title) |
| desk-double-pedestal | `NLP109` | Global Furniture Group | sku_subcode: SKU sub-code NLP (e.g. NLP109) (sku) |
| desk-u-shape-mlp205-1 | `NLP321` | Global Furniture Group | sku_subcode: SKU sub-code NLP (e.g. NLP321) (sku) |
| eor-guest-chair-mvl3920b | `` | Global Furniture Group | model_code: MVL3920B (MVL Ibex line) (title) |
| table-desk-13-colour-options | `NLP224 WCR` | Global Furniture Group | sku_subcode: SKU sub-code NLP (e.g. NLP224 WCR) (sku) |
| coffee-table-1 | `INVCOFREC2436` | Heartwood | sku_subcode: SKU sub-code INVCOFREC (e.g. INVCOFREC2436) (sk |
| l-shape-workstations | `INV3060DS-INVHPF-INV2430` | Heartwood | sku_subcode: SKU sub-code INV (e.g. INV3060DS-INVHPF-INV2430 |
| levels-suite | `Levels Layout 1` | Heartwood | sku_subcode: SKU sub-code LEVELS (e.g. Levels Layout 1) (sku |
| round-table-29-high-8-colours | `INV900-SQB20-BLK R30` | Heartwood | sku_subcode: SKU sub-code INV (e.g. INV900-SQB20-BLK R30) (s |
| u-shape-height-adjust-desk | `INNO-LAYOUT 67` | Heartwood | sku_subcode: SKU sub-code INNO (e.g. INNO-LAYOUT 67) (sku) |
| shoptech-099rx | `` | Horizon Furniture | direct_name: Shoptech (title) |
| bow-front-desk-72x42 | `UN7242BWL/BBF` | Intelligent Office Furniture | sku_subcode: SKU sub-code UN (e.g. UN7242BWL/BBF) (sku) |
| credenza-with-sliding-doors-36-high | `UN6024SC/SC/SLD2/36H` | Intelligent Office Furniture | sku_subcode: SKU sub-code UN (e.g. UN6024SC/SC/SLD2/36H) (sk |
| hutch-with-doors | `UN36HUTDO/43` | Intelligent Office Furniture | sku_subcode: SKU sub-code UN (e.g. UN36HUTDO/43) (sku) |
| storage-right-ff-sc-left-wardrobe | `UN3072FF/SC/WD/21` | Intelligent Office Furniture | sku_subcode: SKU sub-code UN (e.g. UN3072FF/SC/WD/21) (sku) |
| aktivity-puddle | `MYB-AT60PUD` | MityBilt | metafield_manufacturer: specs.manufacturer=MityBilt (metafie |
| screenflex-5-panel-mobile-light-duty-portabl | `` | Screenflex | direct_name: Screenflex (title) |
| screenflex-room-dividers | `GLI T9AB226455` | Screenflex | direct_name: Screenflex (title) |

## Ambiguous (87) — untouched, → Steve/manual

| SKU prefix / reason | N | Example | Sample title |
|---|---:|---|---|
| `(no-sku)` | 46 | `900-SQU20BARSIL-INVSQ2` | Ultra | Armless High Back Tilter Black |
| `SCN` | 7 | `scn-nd426` | Recycled plastic picnic tables *(locked-undecoded: lockers/site-furnishings, supplier invoice)* |
| `WS` | 3 | `WS48-PLANTER/B` | Indoor planter |
| `C` | 3 | `C-HR-4LEG12` | Student Chair 4 sizes |
| `BEL` | 2 | `BEL-HFP154829-GVS` | Planter |
| `BELAIR` | 2 | `BELAIR HCG473608-4DAG1` | Ceiling grids sound acoustic dampeners |
| `BURO` | 1 | `BURO-CTBO 9636+ HB9636` | Boat shaped conference table — 96" x 36" x 29" |
| `SPR` | 1 | `SPR-LLR99554` | Gas lift monitor riser |
| `SOFT` | 1 | `Soft Pods-1` | Soft pods |
| `DSQ` | 1 | `DSQ1824OAKBLK` | Student Desk |
| `DTS` | 1 | `DTS1828P` | Student Desk |
| `SANOMA` | 1 | `Sanoma` | Sonoma |
| `ERGOACCESS` | 1 | `ERGOACCESS-LR72-927B-G` | Oci platinum monitor arms |
| `BOSVLED` | 1 | `BOSVLED500` | Desk lamp - 5.30 w LED bulb - adjustable - met |
| `RDL` | 1 | `RDL-140QI-B` | LED desk lamp with wireless charger - LED |
| `RSIRDL` | 1 | `RSIRDL110U` | LED desk lamp with USB and night light |
| `SP` | 1 | `SP22104P030` | Sphere power |
| `SYNN` | 1 | `SYNN-AD18XL-58-B-PVC` | Anda seat phantom king gaming style office cha |
| `BCMB` | 1 | `BCMB2429WHTSIDEPANEL` | Dual coloured bookcase (15 sizes available) —  |
| `JNT` | 1 | `JNT5946JC` | Hideaway storage cabinet |
| `MGE` | 1 | `MGE-1091503100000` | Hardfloor casters |
| `MYB` | 1 | `MYB- AT2448Z` | Trapezoid tables (3 sizes) — 3 sizes |
| `DIVERSIFIEDAFT` | 1 | `DIVERSIFIEDAFT48305` | Makerspace tables |
| `HTM` | 1 | `HTM3058T/KEZLIFT` | Manual height adjustable table |
| `GLC` | 1 | `GLC-GFT3072R` | Ganging plates for terina tables gfcngfp |
| `HCA` | 1 | `HCA4747-BAM9-T` | Felt acoustic room dividers |
| `CAB` | 1 | `CAB1622LOBBF-CTS3636G-` | Links custom reception unit — 60"x72" |
| `EDU` | 1 | `EDU-SOFIA-LEG-14` | Student Chairs (3 sizes) |
| `ERG` | 1 | `ERG-CS25703` | Corner maker — 2 sizes |
| `TEK` | 1 | `TEK-LLF60L2036D1A 2102` | 6 drawer end tab cabinet S128 drawers — 6 draw |

*Candidate hints (NOT auto-applied — flagged for Steve):* `MYB`→MityBilt (sibling has the `specs.manufacturer` metafield); `TEK`→possibly Teknion; `JNT`→possibly Jonti-Craft; `SYNN`→possibly AndaSeat (gaming); `DIVERSIFIEDAFT`→possibly Diversified. None are in the 19-brand dictionary, so they stay ambiguous.

## Skipped (19) — service / non-product line items

Delivery / installation / freight / disposal / dismantle / additional-service rows. `vendor=BBI` is acceptable here (BBI provides the service). Left untouched.

## Brand-filter readiness

The filter reads card `data-vendor`, so any product left at `vendor=BBI` still renders a **"Brant Business Interiors" brand chip**. Residual characterization (106 untouched = 87 ambiguous + 19 skip):

| Residual bucket | N |
|---|---:|
| Published & real product | 52 |
| Published $0 (quote-only) | 7 |
| Unpublished (not on storefront) | 18 |
| Phantom/option rows | 10 |
| Services (SKIP) | 19 |

**Verdict:** writing the 97 tier-1 corrections **unblocks the Brand filter for those products**, but **~59 published-real products would still surface a "Brant Business Interiors" chip** — too large to ship the filter cleanly alongside. Recommend either (a) suppress the BBI chip in the filter UI until the Steve pass resolves the ~59, or (b) run the Steve pass on the tier-2 (18) + ambiguous (87) first. The tier-2 18 are the cheapest wins (already sourced, just need a confirm).

## Artifacts
- Worksheet: `data/reports/bbi-resourcing-2026-06-02.csv` (+ `-evidence.json`)
- Scan (read-only): `scripts/scan-bbi-resourcing-2026-06-02.py`
- Apply (staged, dry-run default): `scripts/apply-bbi-resourcing-2026-06-02.py` — `--tier1 --live` writes the 97.
