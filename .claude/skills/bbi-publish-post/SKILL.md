---
name: bbi-publish-post
version: "1.0"
description: >
  Explicit slash command for taking a Brant Business Interiors (BBI) blog post from
  draft to live on the Shopify News blog. Runs the per-post pipeline proven on Post 1
  and the office-layout pillar, with the Post-1 friction designed out: one PREP DOCS PR
  (fact-check + conventions + PUBLISH PACK in a single pass, no second edit PR), then a
  create-as-draft to verify-before-flip to flip-live publish flow with human checkpoints,
  then close-out on the correct build-state row.

  Invoked as `/bbi-publish-post [post-name]`, for example
  `/bbi-publish-post ergonomic-chairs-worth-it` or `/bbi-publish-post canadian-made`.
  Parse the post name from the arguments. If none is given, ask once which draft to publish.

  Do NOT auto-trigger on general blogging, content, or Shopify mentions. Only fire when
  Leo explicitly invokes `/bbi-publish-post`.
---

# BBI Publish Post

Leo's canonical workflow for publishing a BBI blog post. Three phases, always in order,
each ending in a human-checkpoint HALT. The conventions make copy born clean, the engine
guarantees the FAQ schema stays honest, and the safety disciplines keep every write reversible.

Read `reference.md` in this directory before running: it holds the CONVENTIONS (apply
automatically), the SAFETY DISCIPLINES (non-negotiable, carried verbatim), the worked Post 1
template, the build-state row map, and the engine command reference.

---

## Usage

Leo invokes `/bbi-publish-post [post-name]`. Parse the post name from the arguments. If none
is given, ask once: "Which draft are we publishing?" then go to PHASE 1.

The draft normally lives in `data/content-drafts/` (see `00-INDEX.md`). The engine that does
the FAQ reformat, interlink application, byte-match, create, and flip is
`scripts/faq_interlink_engine.py` in this skill directory (dry-run by default, `--live` to write).

---

## Store & Business Context

- **Store:** office-central-online.myshopify.com (Admin API version 2026-04)
- **Blog:** News, blog ID `108557861177`, URL pattern `/blogs/news/{article-handle}`
- **Author:** Steve Katz (always)
- **Production write target:** role=main theme. Article writes are Admin-API only (no theme
  write), but still run the watcher preflight.
- **Worked template:** Post 1 OECM cornerstone (article `689003888953`) and the office-layout
  pillar (article `689229365561`); the FAQ + interlink engine descends from
  `scripts/standardize-articles.py`, which ran live on both.
- **Schema is free:** Article (BlogPosting) and FAQPage JSON-LD are template-level in
  `ds-article.liquid`. FAQPage auto-emits whenever the `faq.items` metafield is populated.
  No per-post schema work, ever.

---

## The pipeline (3 phases, human-checkpoint HALTs)

### PHASE 1: PREP (one DOCS PR)

Replaces the old separate fact-check PR and voice PR with a single pass, so copy is born clean
and never needs a second edit PR.

1. **Fact-check and source every claim.** Every statistic, date, and named figure gets a real
   cited source inline. Anything you cannot source: do not publish it. HALT-flag it for Leo.
2. **Apply the CONVENTIONS automatically** (full list in `reference.md`) so the draft is clean
   on arrival: no em-dashes; the exact OECM legal-entity wording; taxonomies framed as common
   patterns not canonical lists; worked examples ICP-realistic and internally consistent with
   the cited figures; tables as embedded HTML; a clean non-redundant article handle. The
   standardized FAQ markup (the "Frequently Asked Questions" heading plus the text-preserving
   Q/A chips) and the catalog interlinks are NOT hand-authored into the draft body. They are
   generated deterministically by the engine at create-draft (PHASE 2a) from the PREP-locked
   pack: PREP locks the FAQ text into `faq_items`, the plain draft FAQ heading into
   `faq_old_heading`, and the verified interlink targets into the `interlinks` list. The draft
   body therefore carries a plain FAQ (the `faq_old_heading` section with plain
   `<p><strong>Question</strong> Answer</p>` items) and no `<a>` interlinks yet; the engine
   inserts the chips and links at create and byte-gates the result before the unpublished POST.
3. **Validate title and meta PROGRAMMATICALLY:**
   `python3 scripts/faq_interlink_engine.py validate-meta --title "..." --meta "..."`
   (title < 60, meta <= 155). Do not eyeball it.
4. **Build the PUBLISH PACK:** title, meta description, handle, author = Steve Katz, tags,
   excerpt, the FAQ block, the `faq_items` list, the interlink list, and a publish checklist.
   Save it as the spec JSON the engine consumes (shape documented in the engine header).
5. **Surface post-specific editorial calls INLINE and batched**, then resolve and apply them
   IN THE SAME PR. Never open a second edit PR for editorial decisions.
6. **Verify interlink targets resolve before committing:**
   `python3 scripts/faq_interlink_engine.py check-handles --handles /collections/x,/products/y`
   Link to the MOST SPECIFIC page that returns 200 (a clean branded PDP if one exists for what
   is discussed, otherwise the collection). Aim for 3 to 6 per post, natural anchor text.
7. **Sync `faq_items` ONCE at the end and byte-verify.** The Q/A text in the PUBLISH PACK, the
   visible FAQ block, and the `faq_items` list must be identical. The chips are markup only.
8. **HALT** for Leo's voice pass. After he is happy, merge the PREP PR.

### PHASE 2: PUBLISH

**2a CREATE as unpublished draft.**
- Watcher preflight first (see SAFETY DISCIPLINES). Verify the blog is `108557861177`. Run a
  handle-collision check.
- POST CONTENT ONLY (no theme scaffolding, no D3 content cross-links), `published=false`.
- Set the `faq.items` metafield (matching the cornerstone format: `list.single_line_text_field`,
  `Question||Answer` lines) plus `global.title_tag` and `global.description_tag`.
- Hardened independent Admin-API readback, byte-match the visible FAQ against `faq.items`.
- Report the article ID and the draft URL. **HALT.**
- Command: `python3 scripts/faq_interlink_engine.py create-draft --spec PACK.json --live`
- **[HUMAN: Leo adds the featured image + alt text in Shopify Admin. Steve signs off.]**

**2b FLIP LIVE.**
- Verify-before-flip gate: featured image present, currently `published=false`, `faq.items`
  still byte-matches the current `body_html`, title and handle and SEO intact. HALT on any
  mismatch.
- Then `published=true`. Hardened independent readback. Report the live URL.
- Command: `python3 scripts/faq_interlink_engine.py flip-live --spec PACK.json --live`
- **[HUMAN: Leo runs the Google Rich Results Test. That is the only authoritative render check.
  This skill must NOT self-certify that the page renders.]**

### PHASE 3: CLOSE-OUT

1. **Record in build-state on the CORRECT row** (`BBI-Session-Kickoff/bbi-build-state.md`).
   Post 1 = the OECM cornerstone (`689003888953`). Batch posts are "Blog #N". Never clobber the
   cornerstone row. See the row map in `reference.md`.
2. **Reconcile the Cowork tracker ONCE, at go-live only.** Canonical file
   `/Users/leokatz/Documents/Claude/Artifacts/bbi-launch-tracker/index.html`. Strip completed
   items, then state RECONCILE CONFIRMED.
3. Branch to PR, squash-merge. Never commit to main.

---

## Rules (quick reference; full detail in reference.md)

- **Run the phases in order**, each ending in its HALT. Never run create and flip in one step.
- **One PREP PR.** Fact-check + conventions + editorial calls + PUBLISH PACK all land together.
- **Create as draft, then verify-before-flip, then flip live.** Never publish in the create step.
- **Post content only** on publish. D3 content-to-content cross-links stay HELD. Catalog
  interlinks (PDP or collection) are mandatory and are NOT part of the D3 hold.
- **`faq.items` byte-match is a hard gate.** Chips are markup only, never baked into the text or
  the metafield. Re-verify on a hardened independent readback, never the write log.
- **Programmatic gates, not eyeballing:** title < 60, meta <= 155, storefront 200 on every link.
- **Watcher preflight** before any theme-touching session; back up live bodies before editing.
- **Real-browser render check only** (Leo's Rich Results Test). The skill never self-certifies.
- **Record on the correct build-state row;** reconcile the Cowork tracker once at go-live.
