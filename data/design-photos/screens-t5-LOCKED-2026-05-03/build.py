#!/usr/bin/env python3
"""Build the three HTML deliverables from src/.

Pattern: inline every CSS file in <style>, inline every JSX in
<script type="text/babel">. React + ReactDOM + Babel UMDs from unpkg.
Functionally equivalent to the round-6 standalone — flat-inline form.
"""
import os, base64, hashlib, sys, pathlib, json

ROOT = pathlib.Path(__file__).parent.resolve()
SRC = ROOT / "src"
ASSETS = ROOT / "assets"

CSS_ORDER = [
    "tokens.css",
    "bbi-components.css",
    "homepage.css",
    "collection-category.css",
    "collection.css",
    "landing.css",
    "pdp.css",
    "audits.css",
]

JSX_ORDER = [
    "Homepage.jsx",
    "CollectionCategory.jsx",
    "Collection.jsx",
    "Landing.jsx",
    "ProductDetail.jsx",
    "Audits.jsx",
]

HEAD_LINKS = """
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""

UMDS = """
<script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
"""

def read(p):
    return (SRC / p).read_text(encoding="utf-8")

def all_css():
    parts = []
    for f in CSS_ORDER:
        parts.append(f"/* ===== {f} ===== */\n" + read(f))
    return "\n\n".join(parts)

def all_jsx_blocks():
    """Returns list of JSX file content (each will become its own
    <script type='text/babel'> tag so Babel can compile them in order)."""
    return [(f, read(f)) for f in JSX_ORDER]

def logo_data_uri():
    p = ASSETS / "bbi-logo-v2.png"
    if not p.exists():
        return ""
    b = p.read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode("ascii")

def jsx_script_tags(only_files=None):
    """Concat ALL JSX into ONE script block so Babel compiles them as a
    single program and execution order is guaranteed. Each file is wrapped
    in a block ({}) so its top-level `const _HeaderDesktop = window.HeaderDesktop`
    lines (which collide across files) are block-scoped. Each file exposes
    its public API via `window.X = X;` at the bottom (already in source)."""
    parts = []
    for fname, content in all_jsx_blocks():
        if only_files and fname not in only_files:
            continue
        parts.append(f"/* ===== {fname} ===== */\n{{\n{content}\n}}")
    one = "\n\n".join(parts)
    return f'<script type="text/babel" data-presets="react" data-filename="bundle.jsx">\n{one}\n</script>'

def css_style_tag():
    return f"<style>\n{all_css()}\n</style>"

def asset_replace(html):
    """Logo lives at assets/bbi-logo-v2.png next to the HTML in the zip
    deliverable, so no inlining required. The bundle is otherwise
    self-contained (CSS + JSX inlined, React/ReactDOM/Babel from unpkg)."""
    return html


# ============================================================
# 1. index.html — DesignCanvas driver, 5 sections
# ============================================================

INDEX_DRIVER = """
<script type="text/babel" data-presets="react" data-filename="DesignCanvas.jsx">
const { useEffect: __dcUseEffect, useRef: __dcUseRef } = React;

function Artboard({ id, label, width, height, children }) {
  return (
    <div className="dc-artboard" id={id}>
      <div className="dc-artboard__head">
        <span className="dc-artboard__num">{id}</span>
        <span className="dc-artboard__label">{label}</span>
        <span className="dc-artboard__dim">{width} × {height}</span>
      </div>
      <div className="dc-artboard__frame" style={{ width: width + 'px', minHeight: height + 'px' }}>
        <div className={"dc-artboard__inner" + (width <= 400 ? ' dc-artboard__inner--mobile' : '')}>
          {children}
        </div>
      </div>
    </div>
  );
}

function Section({ tag, title, children }) {
  return (
    <section className="dc-section" id={"section-" + tag}>
      <header className="dc-section__head">
        <span className="dc-section__tag">{tag}</span>
        <h2 className="dc-section__title">{title}</h2>
      </header>
      <div className="dc-section__body">{children}</div>
    </section>
  );
}

function DesignCanvas() {
  return (
    <div className="dc-root">
      <header className="dc-head">
        <h1>BBI · Design canvas</h1>
        <p>Five locked templates, three artboards each (desktop · mobile · audits). All five render against the v1 token set + Phase-2 components — no new tokens, no additions to bbi-components.css.</p>
      </header>

      <Section tag="01 Homepage" title="Template 1 — Homepage">
        <Artboard id="hp-1440" label="Desktop · 1440" width={1440} height={4400}>
          <window.Homepage />
        </Artboard>
        <Artboard id="hp-375" label="Mobile · 375" width={375} height={6800}>
          <window.Homepage mobile={true} />
        </Artboard>
        <Artboard id="hp-audits" label="Audits · 1280" width={1280} height={2400}>
          <window.Audits template="homepage" />
        </Artboard>
      </Section>

      <Section tag="02 Collection · category" title="Template 2 — /collections/business-furniture">
        <Artboard id="cc-1440" label="Desktop · 1440" width={1440} height={4600}>
          <window.CollectionCategory />
        </Artboard>
        <Artboard id="cc-375" label="Mobile · 375" width={375} height={7400}>
          <window.CollectionCategory mobile={true} />
        </Artboard>
        <Artboard id="cc-audits" label="Audits · 1280" width={1280} height={2400}>
          <window.Audits template="collection-category" />
        </Artboard>
      </Section>

      <Section tag="03 Collection" title="Template 3 — /collections/seating">
        <Artboard id="cn-1440" label="Desktop · 1440" width={1440} height={5400}>
          <window.Collection />
        </Artboard>
        <Artboard id="cn-375" label="Mobile · 375" width={375} height={9200}>
          <window.Collection mobile={true} />
        </Artboard>
        <Artboard id="cn-audits" label="Audits · 1280" width={1280} height={2800}>
          <window.Audits template="collection" />
        </Artboard>
      </Section>

      <Section tag="04 Landing · OECM" title="Template 4 — /pages/oecm">
        <Artboard id="lp-1440" label="Desktop · 1440" width={1440} height={5200}>
          <window.Landing />
        </Artboard>
        <Artboard id="lp-375" label="Mobile · 375" width={375} height={8400}>
          <window.Landing mobile={true} />
        </Artboard>
        <Artboard id="lp-audits" label="Audits · 1280" width={1280} height={2600}>
          <window.Audits template="landing" />
        </Artboard>
      </Section>

      <Section tag="05 PDP · unbuyable" title="Template 5 — /products/ibex-mvl2803">
        <Artboard id="pd-1440" label="Desktop · 1440" width={1440} height={4600}>
          <window.ProductDetail />
        </Artboard>
        <Artboard id="pd-375" label="Mobile · 375" width={375} height={7800}>
          <window.ProductDetail mobile={true} />
        </Artboard>
        <Artboard id="pd-audits" label="Audits · 1280" width={1280} height={3000}>
          <window.Audits template="product" />
        </Artboard>
      </Section>
    </div>
  );
}

const __dcRoot = ReactDOM.createRoot(document.getElementById('root'));
__dcRoot.render(<DesignCanvas />);
</script>
"""

DC_CSS = """
<style>
body { background: #E5E5E7; font-family: 'Inter', system-ui, sans-serif; color: #0B0B0C; margin: 0; }
.dc-root { padding: 48px 32px 96px; }
.dc-head { max-width: 1280px; margin: 0 auto 48px; }
.dc-head h1 { font-family: 'Inter Tight', 'Inter', sans-serif; font-size: 32px; letter-spacing: -0.015em; font-weight: 600; margin: 0 0 8px; }
.dc-head p { font-size: 14px; line-height: 1.55; color: rgba(11,11,12,0.7); margin: 0; max-width: 70ch; }
.dc-section { margin-top: 64px; }
.dc-section__head { max-width: 1280px; margin: 0 auto 24px; display: flex; align-items: baseline; gap: 16px; padding-bottom: 12px; border-bottom: 1px solid rgba(11,11,12,0.3); }
.dc-section__tag { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(11,11,12,0.6); }
.dc-section__title { font-family: 'Inter Tight', 'Inter', sans-serif; font-size: 20px; font-weight: 600; margin: 0; letter-spacing: -0.01em; }
.dc-section__body { display: flex; flex-direction: row; gap: 48px; flex-wrap: wrap; align-items: flex-start; padding: 24px 0; overflow-x: auto; }
.dc-artboard { display: flex; flex-direction: column; gap: 12px; }
.dc-artboard__head { display: flex; align-items: baseline; gap: 12px; padding: 0 4px; font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; color: rgba(11,11,12,0.7); }
.dc-artboard__num { font-weight: 600; color: rgba(11,11,12,0.55); }
.dc-artboard__label { color: #0B0B0C; }
.dc-artboard__dim { color: rgba(11,11,12,0.5); }
.dc-artboard__frame { background: #FFFFFF; border: 1px solid rgba(11,11,12,0.18); box-shadow: 0 4px 24px rgba(11,11,12,0.06); overflow: hidden; }
.dc-artboard__inner--mobile { width: 100%; }
</style>
"""

def build_index():
    css = css_style_tag()
    jsx = jsx_script_tags()
    html = (
      "<!DOCTYPE html>\n<html lang=\"en\"><head>\n"
      + HEAD_LINKS
      + "<title>BBI · Design canvas · 5 templates</title>\n"
      + css + DC_CSS
      + UMDS
      + "</head>\n<body>\n<div id=\"root\"></div>\n"
      + jsx
      + INDEX_DRIVER
      + "</body></html>\n"
    )
    return asset_replace(html)


# ============================================================
# 2. BBI Templates Bundle.html — same 5-section canvas, self-contained
# ============================================================

def build_bundle():
    # Same as index but with a different title and a tiny note in the head.
    # Both are functionally the same single-file canvas.
    html = build_index().replace(
      "<title>BBI · Design canvas · 5 templates</title>",
      "<title>BBI · Templates Bundle · 1–5 standalone</title>"
    )
    return html


# ============================================================
# 3. Template 5 - PDP (unbuyable).html — isolated review file
# ============================================================

PDP_REVIEW_DRIVER = """
<script type="text/babel" data-presets="react" data-filename="PDPReview.jsx">
function PDPReview() {
  return (
    <div className="dc-root">
      <header className="dc-head">
        <h1>BBI · Template 5 · PDP (unbuyable)</h1>
        <p>Isolated review file. Three artboards: desktop 1440 · mobile 375 · audits 1280. Canonical render is Ibex MVL2803 — sold-out, OECM-eligible, sparse spec fields exercising empty-state grace directly.</p>
      </header>
      <section className="dc-section">
        <header className="dc-section__head">
          <span className="dc-section__tag">05 PDP · unbuyable</span>
          <h2 className="dc-section__title">Template 5 — /products/ibex-mvl2803</h2>
        </header>
        <div className="dc-section__body">
          <div className="dc-artboard" id="pd-1440">
            <div className="dc-artboard__head">
              <span className="dc-artboard__num">pd-1440</span>
              <span className="dc-artboard__label">Desktop · 1440</span>
              <span className="dc-artboard__dim">1440 × 4600</span>
            </div>
            <div className="dc-artboard__frame" style={{ width: '1440px', minHeight: '4600px' }}>
              <window.ProductDetail />
            </div>
          </div>
          <div className="dc-artboard" id="pd-375">
            <div className="dc-artboard__head">
              <span className="dc-artboard__num">pd-375</span>
              <span className="dc-artboard__label">Mobile · 375</span>
              <span className="dc-artboard__dim">375 × 7800</span>
            </div>
            <div className="dc-artboard__frame" style={{ width: '375px', minHeight: '7800px' }}>
              <window.ProductDetail mobile={true} />
            </div>
          </div>
          <div className="dc-artboard" id="pd-audits">
            <div className="dc-artboard__head">
              <span className="dc-artboard__num">pd-audits</span>
              <span className="dc-artboard__label">Audits · 1280</span>
              <span className="dc-artboard__dim">1280 × 3000</span>
            </div>
            <div className="dc-artboard__frame" style={{ width: '1280px', minHeight: '3000px' }}>
              <window.Audits template="product" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
const __pdRoot = ReactDOM.createRoot(document.getElementById('root'));
__pdRoot.render(<PDPReview />);
</script>
"""

def build_pdp_review():
    css = css_style_tag()
    # PDP review still needs all source files because ProductDetail
    # composes shared atoms from Homepage.jsx (HeaderDesktop, HeaderMobile,
    # Footer, MapleLeaf, Placeholder).
    jsx = jsx_script_tags()
    html = (
      "<!DOCTYPE html>\n<html lang=\"en\"><head>\n"
      + HEAD_LINKS
      + "<title>BBI · Template 5 · PDP (unbuyable)</title>\n"
      + css + DC_CSS
      + UMDS
      + "</head>\n<body>\n<div id=\"root\"></div>\n"
      + jsx
      + PDP_REVIEW_DRIVER
      + "</body></html>\n"
    )
    return asset_replace(html)


# ============================================================
# Run
# ============================================================

def write(name, content):
    p = ROOT / name
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {name}  ({len(content):,} chars / {len(content)/1024/1024:.2f} MB)")

def sha16(p):
    return hashlib.sha256((SRC / p).read_bytes()).hexdigest()[:16]

def main():
    print("Building HTML deliverables...")
    write("index.html", build_index())
    write("BBI Templates Bundle.html", build_bundle())
    write("Template 5 - PDP (unbuyable).html", build_pdp_review())

    print("\nLocked-file SHA-256 (first 16 chars):")
    locked = [
        "Homepage.jsx", "CollectionCategory.jsx", "Collection.jsx",
        "Landing.jsx", "tokens.css", "bbi-components.css",
        "homepage.css", "collection-category.css", "collection.css",
        "landing.css", "audits.css",
    ]
    sums = {}
    for f in locked:
        s = sha16(f)
        sums[f] = s
        print(f"  {f:30s}  {s}")

    new_files = ["pdp.css", "ProductDetail.jsx", "Audits.jsx"]
    print("\nNew/extended files:")
    for f in new_files:
        s = sha16(f)
        sums[f] = s
        print(f"  {f:30s}  {s}")

    (ROOT / "sha256.json").write_text(json.dumps(sums, indent=2), encoding="utf-8")
    print(f"\n  wrote sha256.json")

if __name__ == "__main__":
    main()
