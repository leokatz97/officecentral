# AI-2 — robots.txt audit

**Date:** 2026-04-30
**Source:** https://www.brantbusinessinteriors.com/robots.txt (fetched live)
**Audit scope:** Confirm that no `Disallow` rule blocks GPTBot, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, or Googlebot from crawling content pages (products, collections, blog, marketing pages). Verify Shopify defaults are in effect with no custom overrides.

---

## TL;DR

**PASS — all six target crawlers can index content.** No custom `robots.txt.liquid` override is in place. The file is the Shopify-managed default. No specific `User-agent` blocks exist for any of the AI crawlers or Googlebot, so they fall under `User-agent: *`, which blocks only non-content paths (admin, cart, checkout, search, policies, sort/filter URLs, internal CDN JS). The only fully-blocked agent is `Nutch` (an open-source crawler, not an AI or search engine that matters for BBI's reach).

No action required. Recommendation: re-run this audit any time the theme is duplicated/published, since a custom `robots.txt.liquid` is the only way Shopify lets you override defaults — and it would silently override everything in this report.

---

## Per-crawler results

| Crawler | User-agent token | Listed explicitly? | Effective rule set | Content pages crawlable? | Status |
|---|---|---|---|---|---|
| OpenAI GPT | `GPTBot` | No | Falls under `User-agent: *` | Yes | PASS |
| Anthropic Claude (web) | `ClaudeBot` | No | Falls under `User-agent: *` | Yes | PASS |
| Anthropic (training) | `anthropic-ai` | No | Falls under `User-agent: *` | Yes | PASS |
| Perplexity | `PerplexityBot` | No | Falls under `User-agent: *` | Yes | PASS |
| Common Crawl | `CCBot` | No | Falls under `User-agent: *` | Yes | PASS |
| Google search | `Googlebot` | No | Falls under `User-agent: *` | Yes | PASS |
| Google AI Overviews opt-in | `Google-Extended` | No | Falls under `User-agent: *` | Yes (allowed) | PASS — and this is what we want for AI Overview readiness (AI-1, AI-3 in the checklist) |

---

## What `User-agent: *` actually blocks

All `Disallow` rules in the wildcard block target non-content URLs that should never be indexed:

- `/admin`, `/cart`, `/orders`, `/account`, `/checkout`, `/checkouts/`, `/carts`, `/85904130361/checkouts`, `/85904130361/orders` — store internals
- `/collections/*sort_by*`, `/collections/*+*`, `/collections/*%2B*`, `*/collections/*filter*&*filter*` — faceted/sort URL variants (avoid duplicate-content penalties)
- `/blogs/*+*`, `/blogs/*%2B*` — same idea on blog tag pages
- `/search` — internal site search results
- `/policies/` — auto-generated Shopify legal pages
- `/sf_private_access_tokens`, `/services/login_with_shop`, `/apple-app-site-association`, `/.well-known/shopify/monorail`, `/cdn/wpm/*.js` — Shopify infra
- `/recommendations/products`, `/*/recommendations/products` — JSON endpoints
- `/products/*-[a-f0-9]{8}-remote`, `/collections/*/products/*-[a-f0-9]{8}-remote` — Shopify "remote" product preview URLs

None of these block product, collection, blog post, or marketing page URLs. **Content is fully crawlable.**

The file ends with a `Sitemap: https://www.brantbusinessinteriors.com/sitemap.xml` directive — sitemap is published.

---

## Other agents listed (non-target — informational)

| User-agent | Block | Notes |
|---|---|---|
| `adsbot-google` | Restricted paths only (same set as `*`) | Shopify ships an explicit block because adsbot-google ignores the `*` wildcard. Content still crawlable. |
| `Nutch` | `Disallow: /` | Fully blocked. Nutch is the Apache open-source crawler — no impact on BBI reach. |
| `AhrefsBot` | `Crawl-delay: 10` + standard rules | Throttled but allowed. |
| `AhrefsSiteAudit` | `Crawl-delay: 10` + standard rules | Throttled but allowed. |
| `MJ12bot` | `Crawl-delay: 10` only | Allowed with throttle. |
| `Pinterest` | `Crawl-delay: 1` only | Allowed with light throttle. |

---

## Custom override check

There is **no** custom `theme/templates/robots.txt.liquid` file in the BBI theme repo. The live `robots.txt` matches Shopify's current managed default exactly — including the new `Robots & Agent policy` header banner Shopify added regarding "buy-for-me" agents and the official Checkout Kit. Confirmed by:

```
$ find theme/templates -name 'robots*'
(no results)
```

Shopify therefore serves the platform default. No human has overridden it.

---

## Recommendations

1. **No changes needed today.** GPTBot, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, and Googlebot can all index BBI content pages.
2. **Don't add a custom `robots.txt.liquid`.** A custom override is the only way Shopify lets you mistakenly block AI crawlers. Steve's stated goal (AI Overview readiness, GEO optimization) depends on `Google-Extended`, `GPTBot`, and `PerplexityBot` having full access — which they currently do.
3. **Re-run this audit:**
   - Whenever the theme is duplicated/published (theme switch can pull in stale `robots.txt.liquid`).
   - If we ever add a "block AI training bots" toggle in Shopify Admin (Online Store → Preferences). That toggle generates a custom override.
   - Quarterly, as a hygiene check.
4. **Companion checks (out of scope for AI-2 but worth noting):**
   - Verify no `<meta name="robots" content="noindex">` on content templates — covered separately by AI-12.
   - Verify sitemap.xml is reachable and current — Shopify regenerates this automatically.

---

## Raw file (verbatim, fetched 2026-04-30)

A copy of the full 189-line response is kept at `/tmp/bbi-robots.txt` for the duration of this session. The response is the Shopify-managed default; no diff against the platform default was found.
