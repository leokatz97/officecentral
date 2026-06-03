# bbi-publish-post reference

Long-form detail for the `/bbi-publish-post` skill. Keep SKILL.md tight; this file holds the
conventions, safety disciplines, worked template, row map, and engine reference.

Note on style: this skill encodes the no-em-dash convention, so this file is written without
em-dashes too. En-dashes appear only inside numeric ranges.

---

## CONVENTIONS (apply automatically; the 4 newest are marked NEW)

- **No em-dashes anywhere.** En-dashes only in numeric ranges (for example 3–6, 8–5). Do not
  introduce em-dashes in your own annotations or commit messages either.
- **OECM / legal-entity wording, always verbatim:** "registered under our parent legal entity,
  Brant Basics, as an authorized OECM Supplier Partner." Customer-facing brand is the full
  "Brant Business Interiors", never the literal "BBI". Brant Basics is cited only in the OECM
  legal-entity context.
- **Taxonomies are "common patterns," never a canonical list.** When a post lists layout types,
  chair categories, and so on, frame them as common patterns. Worked examples must be
  ICP-realistic and internally consistent with the cited figures in the same post.
- **North Star:** qualified Ontario and Canadian business and institutional buyers converting to
  a quote or a design consult. Author is always Steve Katz.
- **NEW · FAQ.** Section titled "Frequently Asked Questions" (or "FAQ"). Each item renders with
  presentational Q and A chips (aria-hidden span, inline-styled, text-preserving). The question
  and answer TEXT must byte-match `faq.items`. The chips are markup only and are never baked into
  the text or into the metafield. FAQPage and Article JSON-LD are template-level in
  `ds-article.liquid` and auto-emit, so there is no per-post schema work.
- **NEW · Interlinks (MANDATORY per post, not held).** Link to the MOST SPECIFIC catalog page
  that RESOLVES: a PDP where a clean branded one exists for what is discussed, otherwise the
  collection. Verify storefront 200 before linking. Natural anchor text, roughly 3 to 6 per post.
  This is distinct from the still-HELD D3 content-to-content cross-links.
- **NEW · Tables.** All in-body tables must be embedded HTML `<table>` with `<caption>` and
  `scope="col"` so `ds-article.liquid` styles them. Never images, never unconverted markdown.
- **NEW · URL / blog handle.** Articles live at `/blogs/{blog}/{article}`; the blog segment is
  mandatory and cannot be removed. The current blog handle is "news". Set a clean article handle
  (no redundancy) from the first post. If the blog is ever renamed, every article URL changes and
  301 redirects are required; the API token lacks `write_content`, so redirects ship as a CSV for
  Steve to upload in Admin.

---

## SAFETY DISCIPLINES (carry verbatim; non-negotiable)

- Watcher preflight before any theme-touching session. A `shopify theme dev` watcher bound to
  role=main auto-pushes local edits and silently bypasses the approval gate. Check with
  `ps aux | grep "shopify theme dev"` and confirm none is running.
- Branch to PR, squash-merge, never commit to main.
- Hardened independent Admin-API readback, never the write log. Edge cache can serve stale or
  variant full-page HTML, so the Admin-API asset or article readback is the gate; a cache-busted
  curl is only supplementary.
- Create-as-draft, then verify-before-flip, then flip-live. Never publish in the create step.
- Post content only on publish. D3 content cross-links stay HELD.
- Back up live article bodies before editing (to `data/backups/articles/`, timestamped).
- Real-browser render check only. Leo's Google Rich Results Test is the authoritative render
  check. The skill never self-certifies that a page renders.

---

## Build-state row map (PHASE 3)

Canonical build-state file: `BBI-Session-Kickoff/bbi-build-state.md` (the Cowork tracker is the
visual mirror of it). Record on the CORRECT row:

- **"Post 1" = the OECM cornerstone**, article `689003888953`, handle
  `oecm-ontario-school-boards-office-furniture`. Do not clobber this row.
- **The office-layout pillar** is logged as "Blog #2", article `689229365561`, handle
  `how-to-plan-an-office-layout-ontario`.
- **Future batch posts** are "Blog #N" (the content-engine drafts in `data/content-drafts/`,
  index `00-INDEX.md`). Each gets its own row, in NEXT ACTIONS order.

When recording, append a tight clause to the post's existing row rather than rewriting it, and
keep the em-dash-free style.

---

## Cowork tracker reconcile (PHASE 3, go-live only)

- Canonical file: `/Users/leokatz/Documents/Claude/Artifacts/bbi-launch-tracker/index.html`.
- Reconcile ONCE, at go-live only (not at create-draft). Strip completed items, align with the
  build-state rows, then state RECONCILE CONFIRMED in your report.

---

## Worked template (Post 1 friction designed out)

The 2026-06-03 office-layout pillar shipped through this exact path: draft, then fact-check and
source, then voice pass, then Admin-API create-as-draft, then featured image by Leo, then Steve
sign-off, then live flip. The friction that this skill removes:

- Post 1 used separate fact-check and voice PRs. PHASE 1 folds both into one PREP PR, with the
  editorial calls surfaced inline and applied in the same PR (never a second edit PR).
- Post 1 synced `faq.items` across three locations by hand. The engine syncs once at the end and
  byte-verifies, then re-verifies on a hardened readback.
- Post 1 left interlinks to the held D3 pass. Catalog interlinks are now mandatory per post and
  decoupled from D3 (catalog URLs are stable and final; D3 content-to-content links stay HELD).
- The standardization pass (2026-06-03) renamed both posts' FAQ to "Frequently Asked Questions"
  with text-preserving chips and added catalog interlinks. That logic is the engine here.

### ergoCentric catalog gap (known)

Post 1 names "ergoCentric task chairs" but no clean branded ergoCentric task-chair PDP is live,
so the standardization linked the Task Chairs collection instead. When publishing the
Canadian-made post (content-engine draft 4) or any ergoCentric-heavy post, prefer a branded PDP
if one has since been added; otherwise fall back to the collection and flag the gap.

---

## Engine reference: `scripts/faq_interlink_engine.py`

Dry-run by default. Pass `--live` to write. Loads `SHOPIFY_TOKEN` from `.env` and aborts loudly
if it is unset (silent-PUT guard).

```
validate-meta --title T --meta M            programmatic title<60 / meta<=155 gate
check-handles --handles a,b,c               storefront 200 check on link targets
verify-faq    --article ID [--blog ID]      live body_html vs faq.items byte-match
standardize   --spec PACK.json [--live]     reformat FAQ + interlinks on an EXISTING article
create-draft  --spec PACK.json [--live]     POST published:false + faq.items + SEO meta + readback
flip-live     --spec PACK.json [--live]     verify-before-flip gate then PUT published:true
```

Spec JSON (the PUBLISH PACK) shape is documented in the engine file header. Minimum fields by
command:

- `validate-meta`, `check-handles`: none (pass values on the CLI).
- `verify-faq`: none (pass the article ID on the CLI).
- `standardize`: `article_id`, `faq_old_heading`, `faq_items`, `interlinks`.
- `create-draft`: `title`, `meta_description`, `handle`, `author`, `tags`, `excerpt`,
  `body_file` (or `body_html`), `faq_old_heading`, `faq_items`, `interlinks`.
- `flip-live`: `article_id`, and `title` + `handle` for the intact checks.

The engine enforces the gates so they cannot be skipped: byte-match must PASS before any write,
interlink anchors must be unique (count-guarded), create refuses a colliding handle and a
title >= 60 or meta > 155, and flip refuses unless the article is currently unpublished, has a
featured image, still byte-matches `faq.items`, and has the intact title and handle.

The original worked instance is `scripts/standardize-articles.py` at the repo root (the version
that ran live on both posts). This engine generalizes it via the spec JSON.
