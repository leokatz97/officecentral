# Watcher Discovery — Forensic Snapshot 2026-05-27 ~14:30 EDT

## What this is

A complete byte-snapshot of LIVE theme `186373570873` ("BBI Landing Dev", role=main) taken immediately after a long-running `shopify theme dev` watcher (PID 28041, running since 2026-05-11) was discovered to be auto-PUTting local theme/ edits to LIVE — bypassing the SCHEMA-CRIT-1 approval gate.

Captured by Claude session under SCHEMA-CRIT-1, Leo Katz directing. Pre-condition for any process recovery / forensic review.

## Discovery timeline

- 14:22-14:23 EDT: Local `Edit` against `theme/snippets/bbi-product-jsonld.liquid` (Fix 1: BreadcrumbList position-2 URL).
- 14:24:13 EDT: LIVE asset `snippets/bbi-product-jsonld.liquid` server-side `updated_at` bumped to byte-identical state as LOCAL post-edit (sha256 `4fe3c703fab0e62b4c253a82f2669c181f06a6da73e257f5a5e06c4b5591e66b`).
- 14:24:14 EDT: LIVE theme `updated_at` bumped.
- ~14:26 EDT: Claude's pre-PUT `updated_at` re-check caught the drift. PUT was halted (approval phrase `fire schema-crit-1 fix-1` was issued but Claude's PUT never executed — the watcher had already pushed).
- ~14:30 EDT: `ps aux | grep shopify` revealed PID 28041 = `node /opt/homebrew/bin/shopify theme dev --store=office-central-online --theme=186373570873 --port=9292`. Pointed at LIVE-main.
- 14:30 EDT: Watcher killed. Confirmed dead. No other shopify processes running.
- 14:30+ EDT: This snapshot taken.

## What's in this directory

```
data/forensics/2026-05-27-watcher-discovery/
├── README.md                          (this file)
├── meta/
│   ├── theme.json                     theme metadata at snapshot time
│   ├── assets-index.json              full asset list from Admin API with checksum+size+updated_at
│   └── snapshot-manifest.json         per-asset sha256 + md5 + size + live md5 match flag
└── snapshot/
    ├── assets/                        downloaded asset files (mirror of LIVE theme tree)
    ├── config/
    ├── layout/
    ├── locales/
    ├── sections/
    ├── snippets/
    └── templates/
```

359 assets total. 311 md5-matched LIVE server checksum byte-exactly; 48 are JSON files (config/settings_*.json, templates/*.json) that show known JSON re-escape wire-format variance — semantically identical, wire-format differs. This pattern is documented in the build-state log.

## Critical file states at snapshot time

| File | sha256 | Notes |
|---|---|---|
| `snippets/bbi-product-jsonld.liquid` (LIVE post-watcher-PUT) | `4fe3c703fab0e62b4c253a82f2669c181f06a6da73e257f5a5e06c4b5591e66b` | Contains the Fix 1 BreadcrumbList pre-assign. Pushed by watcher, NOT by Claude. |
| Same file, pre-fix backup | `21e0156f31312e53f0928a18b069844a28c92900fc68d9d4c40f4274e1742a9f` | At `data/backups/2026-05-27-schema-crit-1/bbi-product-jsonld.liquid.pre-fix1`. |

## Implication

Any local `Edit` against `theme/**` between 2026-05-11 (when the watcher started) and 2026-05-27 14:30 (when it was killed) was auto-PUT to LIVE-main without approval gating. This snapshot is the forensic ground truth needed to scope process recovery: cross-referencing this snapshot against git history will reveal how many `Edit`-mediated changes the watcher promoted to LIVE outside intended approval cycles.

## Do not modify

This snapshot is immutable evidence. Anything you want to inspect, copy to a working directory first.
