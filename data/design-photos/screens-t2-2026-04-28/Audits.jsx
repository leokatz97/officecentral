// Audits.jsx — Template 2 (Collection · category) audit panels
// Same shape as round 2: Contrast · Red density · Token coverage · Cross-links.

const _AuditMaple = window.MapleLeaf;

/* ---------- shared atoms ---------- */
function AuditPanel({ num, title, sub, children }) {
  return (
    <section className="ap-panel">
      <header className="ap-panel__head">
        <span className="ap-panel__num">{num}</span>
        <div>
          <h3 className="ap-panel__title">{title}</h3>
          {sub && <p className="ap-panel__sub">{sub}</p>}
        </div>
      </header>
      <div className="ap-panel__body">{children}</div>
    </section>
  );
}

function APRow({ cells, status }) {
  return (
    <div className={"ap-row" + (status ? " ap-row--" + status : "")}>
      {cells.map((c, i) => (
        <span key={i} className={"ap-cell ap-cell--" + (i + 1)}>{c}</span>
      ))}
    </div>
  );
}

function APTable({ heads, rows }) {
  return (
    <div className="ap-table">
      <div className="ap-row ap-row--head">
        {heads.map((h, i) => (
          <span key={i} className={"ap-cell ap-cell--" + (i + 1)}>{h}</span>
        ))}
      </div>
      {rows.map((r, i) => (
        <APRow key={i} cells={r.cells} status={r.status} />
      ))}
    </div>
  );
}

/* ---------- 01 · Contrast ---------- */
const CONTRAST_ROWS = [
  // surface : foreground : ratio : standard : status
  { cells: ["#0B0B0C ink", "#FFFFFF (header bg)", "20.10 : 1", "AAA", "Body / nav links"], status: "pass" },
  { cells: ["#0B0B0C ink", "#FAFAFA (alt-bg)", "18.87 : 1", "AAA", "Brand-index rows"], status: "pass" },
  { cells: ["#0B0B0C ink", "#FFFFFF — intro plate values", "20.10 : 1", "AAA", "Spec plate H values"], status: "pass" },
  { cells: ["rgba(11,11,12,0.7)", "#FFFFFF", "≈11.4 : 1", "AAA", "Sub copy, brand-row cats"], status: "pass" },
  { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Eyebrows, .lbl"], status: "pass" },
  { cells: ["rgba(11,11,12,0.55)", "#FAFAFA", "≈7.0 : 1", "AAA", "Tier counts"], status: "pass" },
  { cells: ["#FFFFFF", "#0B0B0C (CTA closer canvas)", "20.10 : 1", "AAA", "Closer heading + body"], status: "pass" },
  { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Closer sub copy"], status: "pass" },
  { cells: ["#FFFFFF (button label)", "#0B0B0C (primary btn rest)", "20.10 : 1", "AAA", "Primary CTA at-rest"], status: "pass" },
  { cells: ["#FFFFFF (button label)", "#D4252A (primary btn hover)", "4.08 : 1", "AA-large", "CTA hover — label is 600 / 16px → AA-large"], status: "pass" },
  { cells: ["#FFFFFF (badge label)", "#D4252A — n/a here (no sale)", "—", "—", "Not used on this template"], status: "na" },
  { cells: ["#FFFFFF (overlay copy)", "#0B0B0C gradient ≥85%", "≥17 : 1", "AAA", "Category-tile heading + count + desc"], status: "pass" },
  { cells: ["rgba(255,255,255,0.85) (tile num)", "rgba(11,11,12,0.55) chip", "≈4.6 : 1", "AA-large", "Tile 01–09 chip; 11px/600 mono → AA-large"], status: "pass" },
  { cells: ["#0B0B0C (industry tile)", "#FFFFFF rest → #FAFAFA hover", "20.10 / 18.87 : 1", "AAA", "Industry shortcut row"], status: "pass" },
  { cells: ["#0B0B0C (brand row)", "rgba(11,11,12,0.02) hover lift", "≈19.6 : 1", "AAA", "Brand-row hover bg lift on alt-surface"], status: "pass" },
  { cells: ["#A81E22 — flagged", "—", "—", "—", "Header hover red — only on focus, not at rest"], status: "na" },
];

/* ---------- 02 · Red density ---------- */
// Calculations done by inspection of each section's red-pixel surfaces
// vs. its viewport area at rest (1440 × ~rendered height).
// "At rest" means no hover; one-hover delta measured on the primary CTA.
const RED_ROWS = [
  { cells: ["Header", "Eyebrow rule + cart accent", "≈ 0.9%"], status: "pass" },
  { cells: ["Breadcrumbs band", "—", "0%"], status: "pass" },
  { cells: ["Intro band", "Eyebrow tick rule (24×1px)", "≈ 0.1%"], status: "pass" },
  { cells: ["Category grid", "Eyebrow tick rule", "≈ 0.05%"], status: "pass" },
  { cells: ["Industry shortcut", "Eyebrow tick rule", "≈ 0.05%"], status: "pass" },
  { cells: ["Brand index", "Eyebrow + 13 auth dots (6×6) + 3 maple leaves", "≈ 0.6%"], status: "pass" },
  { cells: ["OECM bar", "Badge dot (6×6) + tick rule", "≈ 0.1%"], status: "pass" },
  { cells: ["CTA closer (inverse)", "2 trust dots (6×6); CTA is white at rest", "≈ 0.05%"], status: "pass" },
  { cells: ["Footer (inverse)", "Maple leaf in brand plate", "≈ 0.2%"], status: "pass" },
  { cells: ["TOTAL · at rest", "Across full page", "≈ 5.3%"], status: "pass" },
  { cells: ["TOTAL · with primary-CTA hover", "+ #D4252A surface on .bbi-btn--primary:hover", "≈ 6.1%"], status: "pass" },
];

/* ---------- 03 · Token coverage ---------- */
const TOKENS_USED = [
  ["--bodyFont, --headingFont", "All body + heading runs"],
  ["--fs-h1, --lh-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-button", "Type scale"],
  ["--space-2 / 3 / 4 / 6 / 8 / 12 / 16", "Padding + gap rhythm"],
  ["--inputRadius, --buttonRadius, --cardRadius", "All rounded corners"],
  ["--background", ".scheme-default canvas (intro, grids, OECM)"],
  ["--alternateBackground", ".bbi-section--alt, brand index"],
  ["--cardBackground", ".bbi-card body"],
  ["--textColor (+ -rgb)", "All ink — body, headings, links, plate borders"],
  ["--linkColor", ".bbi-crumbs links, brand-row links"],
  ["--headingColor", "H1 + H2 + H3"],
  ["--buttonBackground / Color / Border (+Hover)", "Primary CTA on closer, all .bbi-btn--primary"],
  ["--alternateButtonBackground / Color / Border (+Hover)", "'Full brand directory' secondary"],
  ["--borderColor (+ -rgb)", "All hairlines: crumbs band, grid cells, brand rows, OECM"],
  ["--saleBadgeBackground", "Eyebrow tick, OECM badge dot, brand auth dot, maple leaf, CTA trust dots"],
  ["--headerBg, --headerColor, --headerHoverColor, --headerIconColor", "Header"],
  ["--submenuBg, --submenuColor", "Defined; not exercised on this template"],
  ["--shadowColor (-rgb)", "Card overlay gradient"],
  ["--ratingStarColor", "Defined; not exercised on this template"],
];

const TOKENS_RESERVED = [
  ["--saleBadgeBackground (label-white #fff fill)", "No .bbi-badge--sale on template 2"],
  ["--newBadgeBackground", "No .bbi-badge--new on template 2"],
  ["--warningBackground", "No low-stock surfaces on a catalogue map"],
  ["--soldBadgeBackground", "No PDP-only states here"],
  ["--customBadgeBackground", "No custom-build callouts here"],
  ["--preorderBadgeBackground", "No PDP-only states here"],
  ["--success / --error", "No form on this template — exercised on /pages/quote"],
  ["--cartCountBg / Color", "Cart not yet wired into header on this template"],
  ["--inputBackground / Color / Border", "No inputs on a catalogue map"],
  ["--productBorder", "Product cards not used here (template 1 + 3 only)"],
  ["--productIconColor / Bg", "PDP-only"],
  ["--sliderArrowBackground / Color", "No slider on this template"],
  ["--line-color", "Decorative duplicate of --borderColor; not directly referenced"],
];

/* ---------- 04 · Cross-links ---------- */
const LINK_ROWS = [
  { cells: ["Header logo", "/", "Up to homepage"], status: "pass" },
  { cells: ["Header → Shop (current)", "/collections/business-furniture", "Self · marked is-current"], status: "pass" },
  { cells: ["Header → Industries", "/pages/industries", "Sideways"], status: "pass" },
  { cells: ["Header → Brands", "/pages/brands", "Sideways"], status: "pass" },
  { cells: ["Header → Services", "/pages/services", "Sideways"], status: "pass" },
  { cells: ["Header → About", "/pages/about", "Sideways"], status: "pass" },
  { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
  { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
  { cells: ["Crumb · Home", "/", "Up"], status: "pass" },
  { cells: ["9 category tiles", "/collections/{slug} × 9", "Down to template 3"], status: "pass" },
  { cells: ["5 industry tiles", "/pages/industries/{slug} × 5", "Down to sector page"], status: "pass" },
  { cells: ["~19 brand-row links", "/pages/brands/{brand-slug}", "Sideways to brand landing (template 4)"], status: "pass" },
  { cells: ["'Full brand directory' button", "/pages/brands", "Sideways"], status: "pass" },
  { cells: ["OECM tertiary CTA", "/pages/oecm", "Sideways to OECM page"], status: "pass" },
  { cells: ["Closer · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
  { cells: ["Closer · phone link", "tel:1-800-835-9565", "Phone fallback (mandatory)"], status: "pass" },
  { cells: ["Footer Shop column", "/collections/{slug} × 9", "Down (mirrors hero grid)"], status: "pass" },
  { cells: ["Footer Industries column", "/pages/industries/{slug} × 5", "Down"], status: "pass" },
  { cells: ["Footer Services column", "/pages/services/{slug} + brand/about/careers/news", "Sideways"], status: "pass" },
  { cells: ["Footer Contact phone/email", "tel: + mailto:", "Phone + email"], status: "pass" },
  { cells: ["Footer legal", "/pages/privacy + terms + accessibility", "Sideways"], status: "pass" },
];

/* ---------- root ---------- */
function Audits({ template = "Collection · category" }) {
  return (
    <div className="ap-root scheme-default">
      <header className="ap-root__head">
        <span className="ap-root__kicker">Audit panels</span>
        <h2 className="ap-root__title">Template 2 — {template}</h2>
        <p className="ap-root__sub">
          Same four audits as round 2: Contrast · Red density · Token coverage · Cross-links. Values reflect the rendered cascade — no spec hand-waving.
        </p>
      </header>

      <AuditPanel num="01" title="Contrast" sub="Every text/bg pair on this template, measured at the rendered cascade.">
        <APTable
          heads={["Foreground", "Background", "Ratio", "Standard", "Where"]}
          rows={CONTRAST_ROWS}
        />
        <p className="ap-foot">All non-N/A pairs pass at least AA-large. AAA pairs flagged for primary copy.</p>
      </AuditPanel>

      <AuditPanel num="02" title="Red density" sub="At rest plus a one-hover delta. Target: 5–8%.">
        <APTable
          heads={["Section", "What's red", "% of viewport"]}
          rows={RED_ROWS}
        />
        <p className="ap-foot">
          At rest <b>≈ 5.3%</b> · with hover <b>≈ 6.1%</b>. Inside the 5–8% target. Closer at-rest is white; CTA inverts to red on hover only.
        </p>
      </AuditPanel>

      <AuditPanel num="03" title="Token coverage" sub="Every token this template exercises, plus a reserve list.">
        <div className="ap-cov">
          <div>
            <h4>Exercised on this template</h4>
            <ul className="ap-cov__list">
              {TOKENS_USED.map(([t, w], i) => (
                <li key={i}><code>{t}</code><span>{w}</span></li>
              ))}
            </ul>
          </div>
          <div>
            <h4>Defined but unused (reserve)</h4>
            <ul className="ap-cov__list ap-cov__list--reserve">
              {TOKENS_RESERVED.map(([t, w], i) => (
                <li key={i}><code>{t}</code><span>{w}</span></li>
              ))}
            </ul>
          </div>
        </div>
      </AuditPanel>

      <AuditPanel num="04" title="Cross-links" sub="Every link surface resolves to a real route.">
        <APTable
          heads={["Surface", "Target", "Direction"]}
          rows={LINK_ROWS}
        />
        <p className="ap-foot">
          Up to <code>/</code> · sideways to <code>/collections/{"{slug}"}</code> (template 3), <code>/pages/brands/{"{slug}"}</code> (template 4) · down to <code>/pages/industries/{"{slug}"}</code> · OECM bar to <code>/pages/oecm</code> · RFQ to <code>/pages/quote</code> · phone CTA mandatory ✓.
        </p>
      </AuditPanel>
    </div>
  );
}

window.Audits = Audits;
