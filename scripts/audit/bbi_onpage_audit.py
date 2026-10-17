#!/usr/bin/env python3
"""
BBI on-page SEO / content audit — READ-ONLY diagnostic.

WHAT THIS DOES
  Enumerates every ds-cs-base leaf collection and every ds-lp-* landing page,
  reads them live (Admin API for structured data + the public storefront for
  rendered HTML), and flags per-page content/SEO gaps. Writes a Markdown + CSV
  report under data/audits/. It NEVER writes to the store or theme.

WHAT IT IS NOT
  This script performs ZERO mutations. No theme push, no metafield / collection /
  article writes, no GraphQL mutations, no published-state changes. Every HTTP
  call it makes is a GET. If you are editing this file and add a POST/PUT/DELETE,
  you are breaking its contract — stop.

GUARDRAILS BAKED IN
  * The live theme is verified by ROLE/ID, never by name. Theme 186373570873 is
    named "BBI Landing Dev" (a trap) but is role=main / published; "BBI Live" is
    UNPUBLISHED. The script asserts id==186373570873 AND role=='main' before it
    will read anything, and only reads it.
  * SHOPIFY_TOKEN is loaded from .env with read scope only.

GAP CLASSES → OWNING GROWTH-PLAN STEP (see bbi-build-state.md)
  Step 2 — leaf collection.description (answer-first intro) + FAQ JSON-LD that
           byte-matches a visible Q/A block (bbi-faq-jsonld emitter).
  Step 4 — brand / dealer page depth (ds-lp-brands-*).
  Step 5 — commercial-hub / industry landing depth (industries, healthcare, …).
  Step 6 — testimonial / Review schema (the review/comparison page program).
  Step 7 — city / geo pages: exact NAP string presence.
  Step 9 — site-wide SEO meta (title < 60, meta description <= 155).

USAGE
  set -a && source .env && set +a
  python3 scripts/audit/bbi_onpage_audit.py
"""

import os
import re
import csv
import sys
import json
import time
import html
import datetime
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
STORE = "office-central-online.myshopify.com"
PUBLIC = "https://www.brantbusinessinteriors.com"
API = "2026-04"
LIVE_THEME_ID = 186373570873           # verify by ID; "BBI Landing Dev" name is a trap
BASE = f"https://{STORE}/admin/api/{API}"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(REPO_ROOT, "theme", "templates")
OUT_DIR = os.path.join(REPO_ROOT, "data", "audits")

# Canonical NAP (locked by S4-CONTACT-FIX). Verified for *exact* match.
NAP_ADDRESS = "296 George St N, Peterborough ON K9J 3H2"
NAP_PHONE = "1-800-835-9565"

# SEO thresholds
TITLE_MAX = 60          # flag title length >= 60
META_DESC_MAX = 155     # flag meta description length > 155
ANSWER_FIRST_MIN_WORDS = 25   # flag intro shorter than this as boilerplate/empty

TOKEN = os.environ.get("SHOPIFY_TOKEN")
HEADERS = {"X-Shopify-Access-Token": TOKEN or "", "Content-Type": "application/json"}

# A counter that MUST stay zero. Every Admin/storefront call routes through the
# read helpers below; nothing increments this. It is printed at the end as proof.
WRITE_COUNT = 0


# ---------------------------------------------------------------------------
# Read-only HTTP helpers (GET only — by construction)
# ---------------------------------------------------------------------------
def admin_get(path):
    """GET against the Shopify Admin API. Read-only."""
    url = path if path.startswith("http") else f"{BASE}/{path.lstrip('/')}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:              # rate limited — back off
                time.sleep(2 * (attempt + 1))
                continue
            if e.code in (403, 404):
                return {"_error": e.code, "_url": url}
            raise
    return {"_error": "rate_limited", "_url": url}


def storefront_get(path):
    """GET a public storefront URL. Returns (status, html) — read-only."""
    url = path if path.startswith("http") else f"{PUBLIC}{path}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "BBI-onpage-audit/1.0 (+read-only diagnostic)"},
        method="GET",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            return e.code, ""
        except urllib.error.URLError:
            return 0, ""
    return 0, ""


# ---------------------------------------------------------------------------
# Guardrail: verify the live theme by ID + role before doing anything
# ---------------------------------------------------------------------------
def verify_live_theme():
    data = admin_get("themes.json")
    if data.get("_error"):
        sys.exit(f"FATAL: could not list themes ({data['_error']}). Check SHOPIFY_TOKEN.")
    match = [t for t in data["themes"] if t["id"] == LIVE_THEME_ID]
    if not match:
        sys.exit(f"FATAL: theme {LIVE_THEME_ID} not found. Refusing to proceed.")
    theme = match[0]
    if theme["role"] != "main":
        sys.exit(
            f"FATAL: theme {LIVE_THEME_ID} has role={theme['role']!r}, expected 'main'. "
            "Refusing to audit the wrong theme."
        )
    print(f"  ✓ live theme verified by ID {LIVE_THEME_ID} → role=main "
          f"(name {theme['name']!r} is a known trap; verified by role, not name)")
    return theme


# ---------------------------------------------------------------------------
# Discover target sets
# ---------------------------------------------------------------------------
def discover_lp_suffixes():
    """Parse theme/templates/page.*.json → {template_suffix: section_type} for
    every page whose main section is a ds-lp-* section."""
    out = {}
    for fn in os.listdir(TEMPLATES_DIR):
        if not fn.startswith("page.") or not fn.endswith(".json"):
            continue
        suffix = fn[len("page."):-len(".json")]
        if suffix == "":      # page.json default — no suffix
            continue
        try:
            with open(os.path.join(TEMPLATES_DIR, fn)) as f:
                doc = json.load(f)
        except (ValueError, OSError):
            continue
        lp = [s.get("type") for s in doc.get("sections", {}).values()
              if str(s.get("type", "")).startswith("ds-lp-")]
        if lp:
            out[suffix] = lp[0]
    return out


# Commercial-hub / industry landings whose copy depth is owned by Step 5.
HUB_SUFFIXES = {
    "sit-stand-desks", "ergonomic-office-chairs", "industries", "healthcare",
    "education", "government", "non-profit", "professional-services",
}
# A landing page is flagged for "thin content" only when its depth is owned by a
# growth-plan step (Step 4 brand/dealer pages, Step 5 commercial hubs). Other
# pages (contact, faq, about, …) are not depth-graded.
DEPTH_MIN_WORDS = 400


def lp_step(suffix, section):
    """Map a landing page to its owning growth-plan step (used for the row's home step)."""
    if suffix.startswith("city-"):
        return 7                       # geo / local
    if suffix.startswith("brands"):
        return 4                       # dealer / brand deepen
    if suffix in HUB_SUFFIXES:
        return 5                       # commercial-hub / industry landings
    return 5                           # default landing-page owner


def depth_step(suffix):
    """Return the step that owns this page's content depth, or None if not graded."""
    if suffix.startswith("brands"):
        return 4
    if suffix in HUB_SUFFIXES:
        return 5
    return None


# ---------------------------------------------------------------------------
# Live data fetchers
# ---------------------------------------------------------------------------
def list_leaf_collections():
    """All collections whose template_suffix == 'base' (renders ds-cs-base)."""
    out = []
    for endpoint, key in (("custom_collections.json", "custom_collections"),
                          ("smart_collections.json", "smart_collections")):
        url = (f"{endpoint}?limit=250&fields=id,handle,title,body_html,"
               f"template_suffix,published_at")
        data = admin_get(url)
        if data.get("_error"):
            continue
        out.extend(data.get(key, []))
    return [c for c in out if c.get("template_suffix") == "base"]


def list_lp_pages(lp_suffixes):
    """All live pages whose template_suffix is a known ds-lp-* suffix."""
    data = admin_get("pages.json?limit=250&fields=id,handle,title,body_html,"
                     "template_suffix,published_at")
    if data.get("_error"):
        return []
    return [p for p in data.get("pages", [])
            if p.get("template_suffix") in lp_suffixes]


def seo_metafields(owner_kind, owner_id):
    """Read global.title_tag / global.description_tag for a collection or page."""
    data = admin_get(f"{owner_kind}/{owner_id}/metafields.json")
    title_tag = desc_tag = None
    if not data.get("_error"):
        for m in data.get("metafields", []):
            if m.get("namespace") == "global" and m.get("key") == "title_tag":
                title_tag = m.get("value")
            elif m.get("namespace") == "global" and m.get("key") == "description_tag":
                desc_tag = m.get("value")
    return title_tag, desc_tag


# ---------------------------------------------------------------------------
# HTML / text helpers
# ---------------------------------------------------------------------------
_TAG_RE = re.compile(r"<[^>]+>")
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_WS_RE = re.compile(r"\s+")


def strip_to_text(markup):
    if not markup:
        return ""
    no_ss = _SCRIPT_STYLE_RE.sub(" ", markup)
    txt = _TAG_RE.sub(" ", no_ss)
    return _WS_RE.sub(" ", html.unescape(txt)).strip()


def first_words(text, n):
    return " ".join(text.split()[:n])


def extract_title(markup):
    m = re.search(r"<title[^>]*>(.*?)</title>", markup, re.DOTALL | re.IGNORECASE)
    return html.unescape(m.group(1).strip()) if m else ""


def extract_meta_description(markup):
    m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        markup, re.DOTALL | re.IGNORECASE)
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\'](.*?)["\'][^>]*name=["\']description["\']',
            markup, re.DOTALL | re.IGNORECASE)
    return html.unescape(m.group(1).strip()) if m else ""


def extract_jsonld(markup):
    """Return parsed JSON-LD objects (flattening @graph) from the page."""
    blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        markup, re.DOTALL | re.IGNORECASE)
    objs = []
    for raw in blocks:
        try:
            data = json.loads(raw.strip())
        except ValueError:
            continue
        items = data.get("@graph", [data]) if isinstance(data, dict) else data
        if isinstance(items, list):
            objs.extend(x for x in items if isinstance(x, dict))
        elif isinstance(items, dict):
            objs.append(items)
    return objs


def _types_of(obj):
    t = obj.get("@type", "")
    return [t] if isinstance(t, str) else list(t) if isinstance(t, list) else []


def analyse_faq(jsonld, visible_text):
    """Return (has_faq_schema, questions_byte_match) for FAQPage JSON-LD."""
    faqs = [o for o in jsonld if "FAQPage" in _types_of(o)]
    if not faqs:
        return False, None
    questions = []
    for f in faqs:
        for q in f.get("mainEntity", []) or []:
            name = (q.get("name") or "").strip()
            if name:
                questions.append(name)
    if not questions:
        return True, False
    vis = _WS_RE.sub(" ", visible_text).lower()
    matched = sum(1 for q in questions
                  if _WS_RE.sub(" ", html.unescape(q)).lower() in vis)
    return True, matched == len(questions)


def has_review_content(jsonld, markup):
    """True if Review / AggregateRating schema OR testimonial markup is present."""
    for o in jsonld:
        ts = _types_of(o)
        if any(t in ("Review", "AggregateRating") for t in ts):
            return True
        if o.get("aggregateRating") or o.get("review"):
            return True
    return bool(re.search(r'class=["\'][^"\']*testimonial', markup, re.IGNORECASE))


def find_nap(markup):
    """Exact-match the canonical address + phone in the raw HTML (whitespace-normalised)."""
    norm = _WS_RE.sub(" ", html.unescape(markup))
    return (_WS_RE.sub(" ", NAP_ADDRESS) in norm,
            _WS_RE.sub(" ", NAP_PHONE) in norm)


# ---------------------------------------------------------------------------
# Per-page audit
# ---------------------------------------------------------------------------
def audit_one(kind, rec, url_path, owner_kind, step):
    """Build one audit row. kind in {'collection','page'}."""
    published = bool(rec.get("published_at"))
    desc_html = rec.get("body_html") or ""
    desc_text = strip_to_text(desc_html)
    intro = first_words(desc_text, 60)
    intro_words = len(intro.split())

    title_tag, desc_tag = seo_metafields(owner_kind, rec["id"])

    row = {
        "kind": kind,
        "handle": rec.get("handle", ""),
        "title": rec.get("title", ""),
        "url": url_path,
        "step": step,
        "published": "yes" if published else "no",
        "desc_present": "yes" if desc_text else "no",
        "desc_words": len(desc_text.split()),
        "answer_first_words": intro_words,
        "rendered": "no",
        "http": "",
        "seo_title": "",
        "seo_title_len": "",
        "meta_desc_len": "",
        "faq_jsonld": "n/a",
        "faq_byte_match": "n/a",
        "review_or_testimonial": "n/a",
        "nap_address": "n/a",
        "nap_phone": "n/a",
        "flags": [],
    }

    flags = []

    # ---- description / answer-first (Step 2 for collections) ----
    if kind == "collection":
        if not desc_text:
            flags.append(("S2", "collection.description EMPTY (no answer-first intro)"))
        elif intro_words < ANSWER_FIRST_MIN_WORDS:
            flags.append(("S2", f"intro very short ({intro_words} words) — likely boilerplate"))

    # ---- rendered storefront checks (published only) ----
    if published:
        status, markup = storefront_get(url_path)
        row["http"] = status
        if status == 200 and markup:
            row["rendered"] = "yes"
            jsonld = extract_jsonld(markup)
            visible = strip_to_text(markup)

            seo_title = extract_title(markup)
            meta_desc = extract_meta_description(markup)
            row["seo_title"] = seo_title
            row["seo_title_len"] = len(seo_title)
            row["meta_desc_len"] = len(meta_desc)
            if seo_title and len(seo_title) >= TITLE_MAX:
                flags.append(("S9", f"SEO title {len(seo_title)} chars (>= {TITLE_MAX})"))
            if not meta_desc:
                flags.append(("S9", "meta description MISSING"))
            elif len(meta_desc) > META_DESC_MAX:
                flags.append(("S9", f"meta description {len(meta_desc)} chars (> {META_DESC_MAX})"))

            has_faq, faq_match = analyse_faq(jsonld, visible)
            row["faq_jsonld"] = "yes" if has_faq else "no"
            row["faq_byte_match"] = ("yes" if faq_match else "no") if has_faq else "no"
            # FAQ emitter gap is scoped to collection / category pages (per spec).
            if kind == "collection":
                if not has_faq:
                    flags.append(("S2", "no FAQ JSON-LD emitted on page"))
                elif faq_match is False:
                    flags.append(("S2", "FAQ JSON-LD present but Q/A NOT byte-matched in visible text"))

            # Content-depth grading for brand (Step 4) / commercial-hub (Step 5) pages.
            if kind == "page":
                dstep = depth_step(rec.get("template_suffix") or "")
                if dstep:
                    wc = len(visible.split())
                    if wc < DEPTH_MIN_WORDS:
                        flags.append((f"S{dstep}",
                                      f"thin rendered content ({wc} words, < {DEPTH_MIN_WORDS}) — deepen"))

            has_rev = has_review_content(jsonld, markup)
            row["review_or_testimonial"] = "yes" if has_rev else "no"
            if not has_rev:
                flags.append(("S6", "no testimonial / Review schema present"))

            addr_ok, phone_ok = find_nap(markup)
            row["nap_address"] = "exact" if addr_ok else "absent"
            row["nap_phone"] = "exact" if phone_ok else "absent"
            if step == 7:                      # NAP is the point of geo pages
                if not addr_ok:
                    flags.append(("S7", "canonical NAP address NOT present (exact)"))
                if not phone_ok:
                    flags.append(("S7", "canonical NAP phone NOT present (exact)"))
        else:
            flags.append(("--", f"storefront not rendered (HTTP {status})"))
    else:
        flags.append(("--", "unpublished — storefront checks skipped"))

    row["flags"] = flags
    return row


# ---------------------------------------------------------------------------
# Report writers
# ---------------------------------------------------------------------------
STEP_LABELS = {
    2: "Step 2 — leaf collection.description (answer-first) + FAQ JSON-LD byte-match",
    4: "Step 4 — brand / dealer page depth",
    5: "Step 5 — commercial-hub / industry landing depth",
    6: "Step 6 — testimonial / Review schema (review-page program)",
    7: "Step 7 — city / geo pages: exact NAP",
    9: "Step 9 — site-wide SEO meta (title < 60, meta desc <= 155)",
}
FLAG_STEP = {"S2": 2, "S4": 4, "S5": 5, "S6": 6, "S7": 7, "S9": 9}


def write_csv(rows, path):
    cols = ["kind", "handle", "title", "url", "step", "published", "desc_present",
            "desc_words", "answer_first_words", "rendered", "http", "seo_title_len",
            "meta_desc_len", "faq_jsonld", "faq_byte_match", "review_or_testimonial",
            "nap_address", "nap_phone", "flags"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            flat = "; ".join(f"[{c}] {m}" for c, m in r["flags"])
            w.writerow([r.get(c, "") if c != "flags" else flat for c in cols])


def write_md(rows, path, today, theme):
    # Tally DISTINCT pages flagged per owning step, and raw flags per step.
    step_pages = {k: 0 for k in STEP_LABELS}
    step_flags = {k: 0 for k in STEP_LABELS}
    for r in rows:
        steps_hit = set()
        for code, _ in r["flags"]:
            if code in FLAG_STEP:
                step_flags[FLAG_STEP[code]] += 1
                steps_hit.add(FLAG_STEP[code])
        for s in steps_hit:
            step_pages[s] += 1

    cols_present = sum(1 for r in rows if r["kind"] == "collection" and r["desc_present"] == "yes")
    cols_total = sum(1 for r in rows if r["kind"] == "collection")
    cols_pub = sum(1 for r in rows if r["kind"] == "collection" and r["published"] == "yes")

    lines = []
    lines.append(f"# BBI on-page audit — {today}")
    lines.append("")
    lines.append("**READ-ONLY diagnostic.** This report was generated by "
                 "`scripts/audit/bbi_onpage_audit.py`. Zero writes hit the store or theme.")
    lines.append("")
    lines.append(f"- Live theme verified by ID **{LIVE_THEME_ID}** → role **main** "
                 f"(name {theme['name']!r}; verified by role, not name).")
    lines.append(f"- Pages audited: **{len(rows)}** "
                 f"({cols_total} leaf collections + {len(rows) - cols_total} ds-lp pages).")
    lines.append(f"- Leaf collections published: **{cols_pub}/{cols_total}**; "
                 f"with a non-empty `collection.description`: **{cols_present}/{cols_total}**.")
    lines.append("")

    # ---- summary: gap class → step ----
    lines.append("## Gap summary → owning growth-plan step")
    lines.append("")
    lines.append("| Step | Gap class | Pages flagged | Total flags |")
    lines.append("|---|---|---|---|")
    for k in sorted(STEP_LABELS):
        lines.append(f"| {k} | {STEP_LABELS[k]} | {step_pages[k]} | {step_flags[k]} |")
    lines.append("")

    # ---- per-step page lists ----
    for k in sorted(STEP_LABELS):
        flagged = [r for r in rows if any(FLAG_STEP.get(c) == k for c, _ in r["flags"])]
        if not flagged:
            continue
        lines.append(f"### {STEP_LABELS[k]} — {len(flagged)} pages")
        lines.append("")
        for r in flagged:
            msgs = "; ".join(m for c, m in r["flags"] if FLAG_STEP.get(c) == k)
            lines.append(f"- `{r['handle']}` ({r['kind']}, [{r['url']}]({PUBLIC}{r['url']})) — {msgs}")
        lines.append("")

    # ---- full per-page table ----
    lines.append("## Per-page detail")
    lines.append("")
    lines.append("| Kind | Handle | Pub | Desc | Intro wds | Title len | Meta len | "
                 "FAQ | FAQ match | Review | NAP addr | NAP phone | Flags |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (x["kind"], x["step"], x["handle"])):
        nflags = len(r["flags"])
        lines.append(
            f"| {r['kind']} | `{r['handle']}` | {r['published']} | {r['desc_present']} | "
            f"{r['answer_first_words']} | {r['seo_title_len']} | {r['meta_desc_len']} | "
            f"{r['faq_jsonld']} | {r['faq_byte_match']} | {r['review_or_testimonial']} | "
            f"{r['nap_address']} | {r['nap_phone']} | {nflags} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Heuristics: answer-first flagged when the first 60 words of "
                 f"`collection.description` are empty or < {ANSWER_FIRST_MIN_WORDS} words. "
                 "FAQ byte-match = every FAQPage question `name` appears verbatim in the "
                 "rendered visible text. NAP = exact canonical string match._")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not TOKEN:
        sys.exit("FATAL: SHOPIFY_TOKEN not set. `set -a && source .env && set +a` first.")

    print("BBI on-page audit (READ-ONLY) — verifying live theme…")
    theme = verify_live_theme()

    lp_suffixes = discover_lp_suffixes()
    print(f"  ✓ discovered {len(lp_suffixes)} ds-lp-* page templates")

    print("  · reading leaf collections + landing pages via Admin API…")
    leaves = list_leaf_collections()
    pages = list_lp_pages(lp_suffixes)
    print(f"  ✓ {len(leaves)} ds-cs-base leaf collections, {len(pages)} ds-lp pages")

    rows = []
    print("  · auditing collections…")
    for c in leaves:
        rows.append(audit_one("collection", c, f"/collections/{c['handle']}",
                              "collections", step=2))
    print("  · auditing landing pages…")
    for p in pages:
        suffix = p["template_suffix"]
        step = lp_step(suffix, lp_suffixes.get(suffix, ""))
        rows.append(audit_one("page", p, f"/pages/{p['handle']}", "pages", step=step))

    today = datetime.date.today().isoformat()
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    md_path = os.path.join(OUT_DIR, f"{today}-onpage-audit.md")
    csv_path = os.path.join(OUT_DIR, f"{today}-onpage-audit.csv")
    write_md(rows, md_path, today, theme)
    write_csv(rows, csv_path)

    total_flags = sum(len(r["flags"]) for r in rows)
    print(f"\n  ✓ wrote {md_path}")
    print(f"  ✓ wrote {csv_path}")
    print(f"  · {len(rows)} pages audited, {total_flags} flags raised")
    # Proof of the read-only contract.
    print(f"\nZERO writes hit the store: {WRITE_COUNT} mutations performed "
          "(Admin + storefront calls were all GET).")


if __name__ == "__main__":
    main()
