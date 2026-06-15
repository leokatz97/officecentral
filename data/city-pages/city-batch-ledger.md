# BBI Step 7 — City Batch Master Ledger

_Generated 2026-06-15 · DATA ONLY (read/research). No theme writes, no page creates, no keyword locking._

**Scope:** 19 research cities + Mississauga (row 1, already built). Toronto + Ottawa EXCLUDED (parked as live-article convert+301 decisions — both exist as `office-furniture-{city}-ontario` articles on `/blogs/news`).

**Keyword data:** DataForSEO `keyword_overview` + `bulk_keyword_difficulty`, location Canada, en (primaries cross-checked vs google_ads Ontario,Canada). Volume = `office furniture {city}` primary. KD `low (no value)` = DataForSEO returned no difficulty (sparse SERP for the geo term — comparable geo terms land KD 5–19; Mississauga, already built, returned KD 5).

**Local proof:** HONESTY GATE — `data/oci-photos/` holds NO city-tagged projects. Every city is coverage-only. Peterborough is the one genuine physical presence (HQ, real NAP).

**Cross-link targets (checked once, all live):** `/pages/oecm` ✓ · `/pages/design-services` ✓ · `/pages/delivery` ✓ · `/pages/quote` ✓ · `/collections/business-furniture` (648) ✓ · `/collections/seating` (131) ✓ · `/collections/desks` (41) ✓

| # | City | slug | handle free? | collision | primary vol | KD | keyword free? | local proof | coverage (Steve: YES) | wave | flags |
|---|------|------|:---:|---|:---:|:---:|:---:|------|:---:|:---:|-------|
| 1 | Mississauga | office-furniture-mississauga | n/a (BUILT) | self (page gid 172098945337) | ~50 (KD 5) | 5 | free | coverage-only | YES | BUILT — unpublished | reference row |
| 2 | Brampton | office-furniture-brampton | YES (404) | none | 140 | low (no value) | free | coverage-only | YES | A | — |
| 3 | Burlington | office-furniture-burlington | YES (404) | none | 140 | low (no value) | free | coverage-only | YES | A | ambiguous name (disambiguate w/ 'Ontario') |
| 4 | Markham | office-furniture-markham | YES (404) | none | 140 | 12 | free | coverage-only | YES | A | — |
| 5 | Vaughan | office-furniture-vaughan | YES (404) | none | 90 | 9 | free | coverage-only | YES | A | — |
| 6 | Barrie | office-furniture-barrie | YES (404) | none | 90 | low (no value) | free | coverage-only | YES | A | — |
| 7 | Hamilton | office-furniture-hamilton | YES (404) | none | 50 | low (no value) | free | coverage-only | YES | A | — |
| 8 | Peterborough | office-furniture-peterborough | YES (404) | none | 30 | low (no value) | free | HQ real-NAP | YES | A | Peterborough-HQ (real-NAP, distinct template — NOT a coverage page) |
| 9 | Kitchener-Waterloo | office-furniture-kitchener-waterloo | YES (404) | none | 70 | low (no value) | free | coverage-only | YES | B | KW pair → one page; title targets Kitchener (70), Waterloo (20) in body |
| 10 | Cambridge | office-furniture-cambridge | YES (404) | none | 40 | 13 | free | coverage-only | YES | B | ambiguous name (disambiguate w/ 'Ontario') |
| 11 | Oshawa | office-furniture-oshawa | YES (404) | none | 40 | 5 | free | coverage-only | YES | B | eastern-cluster |
| 12 | London | office-furniture-london | YES (404) | none | 30 | 19 | free | coverage-only | YES | B | ambiguous name (disambiguate w/ 'Ontario') |
| 13 | Oakville | office-furniture-oakville | YES (404) | none | 30 | low (no value) | free | coverage-only | YES | B | — |
| 14 | Brantford | office-furniture-brantford | YES (404) | none | 30 | 13 | free | coverage-only | YES | B | brand namesake (Brant) |
| 15 | St. Catharines | office-furniture-st-catharines | YES (404) | none | 30 | 12 | free | coverage-only | YES | C | — |
| 16 | Kingston | office-furniture-kingston | YES (404) | none | 30 | 17 | free | coverage-only | YES | C | eastern-cluster; ambiguous name (disambiguate w/ 'Ontario') |
| 17 | Guelph | office-furniture-guelph | YES (404) | none | 20 | 15 | free | coverage-only | YES | C | — |
| 18 | Richmond Hill | office-furniture-richmond-hill | YES (404) | none | 10 | 42 | free | coverage-only | YES | C | ambiguous name (disambiguate w/ 'Ontario'); KD42 anomaly |
| 19 | Belleville | office-furniture-belleville | YES (404) | none | 10 | 42 | free | coverage-only | YES | C | eastern-cluster; ambiguous name (disambiguate w/ 'Ontario'); KD42 anomaly |
| 20 | Niagara Falls | office-furniture-niagara-falls | YES (404) | none | ~0 (no DB data) | low (no value) | free | coverage-only | YES | C | ambiguous name (disambiguate w/ 'Ontario'); thin volume |

## Proposed build waves (ranked by volume × commercial density)

**Wave A — anchor + top volume/density (build first):** Peterborough (HQ anchor, real NAP), Brampton (140), Burlington (140), Markham (140), Vaughan (90), Barrie (90), Hamilton (50, major metro).

**Wave B — strong secondary markets:** Kitchener-Waterloo (70/+20), Oshawa (40, eastern/closest to HQ), Cambridge (40), Brantford (30, namesake — easy KD13 brand win), Oakville (30), London (30).

**Wave C — fill / lower volume / eastern / ambiguous-KD:** St. Catharines (30), Kingston (30, eastern), Guelph (20), Richmond Hill (10, KD42), Belleville (10, eastern, KD42), Niagara Falls (~0, thin).

## Flags for Leo

- **Eastern cluster (Oshawa, Kingston, Belleville):** consumes the PENDING `eastern-ontario-geo` cluster in priority-keywords.yaml (~25 net-new geo kw, earmarked `-> geo_page`). Building these as city PAGES realizes part of that pending cluster — note at lock time.
- **Page-vs-article convention:** Toronto + Ottawa live as ARTICLES (`office-furniture-{city}-ontario`, `/blogs/news`). All new builds are PAGES (`office-furniture-{slug}`). Intentional split; if these geo terms are later consolidated, decide whether the Toronto/Ottawa articles convert to pages (+301).
- **Peterborough = HQ-special:** distinct real-NAP template (headquartered, shortest lead times), NOT a 'coverage area' page. Treat separately from the coverage template.
- **Ambiguous-name cities** (London, Cambridge, Burlington, Kingston, Belleville, Richmond Hill, Niagara Falls): bare term collides with same-named foreign/US places. Disambiguate with 'Ontario' in title/H1/schema. Belleville & Richmond Hill returned KD42 (inflated by the collision) — real local difficulty is low.
- **No keyword is locked.** Every primary is FREE; locking happens per-build at close-out, not now.
