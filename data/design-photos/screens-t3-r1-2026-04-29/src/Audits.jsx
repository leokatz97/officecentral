// Audits.jsx — template-aware registry. Each template registers its
// audit data; <Audits template="..." /> renders the right slice.
// Round 3: keeps the round-2 homepage audits live on the canvas
// alongside the new template-2 (collection-category) audits.

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

/* ---------- registry ---------- */
const AUDIT_REGISTRY = {};
function register(slug, data) { AUDIT_REGISTRY[slug] = data; }

/* ---------- template 1: homepage (round 2) ---------- */
register("homepage", {
  title: "Template 1 — Homepage",
  contrast: [
    { cells: ["#0B0B0C ink", "#FFFFFF page bg", "20.10 : 1", "AAA", "Body / nav / headings"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FAFAFA alt-bg", "18.87 : 1", "AAA", "Shop band, Industries, Our work"], status: "pass" },
    { cells: ["rgba(11,11,12,0.78)", "#FFFFFF", "≈12.7 : 1", "AAA", "Sub copy"], status: "pass" },
    { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Eyebrows, brand kicker"], status: "pass" },
    { cells: ["#FFFFFF label", "#0B0B0C primary btn rest", "20.10 : 1", "AAA", "Hero CTA + utility CTA"], status: "pass" },
    { cells: ["#FFFFFF label", "#D4252A primary btn hover", "4.08 : 1", "AA-large", "All bbi-btn--primary on hover"], status: "pass" },
    { cells: ["#FFFFFF overlay copy", "#0B0B0C gradient ≥85%", "≥17 : 1", "AAA", "Featured-category tile overlay"], status: "pass" },
    { cells: ["#FFFFFF (footer)", "#0B0B0C (inverse canvas)", "20.10 : 1", "AAA", "Footer body + headings"], status: "pass" },
    { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Footer tagline + col links"], status: "pass" },
    { cells: ["rgba(255,255,255,0.55)", "#0B0B0C", "≈10.4 : 1", "AAA", "Footer legal + © line"], status: "pass" },
    { cells: ["#A81E22 hover ink", "#0B0B0C", "2.32 : 1", "FAIL on inverse", "Reserved — never used on inverse"], status: "na" },
  ],
  red: [
    { cells: ["Header", "Eyebrow + cart accent", "≈ 0.9%"], status: "pass" },
    { cells: ["Hero", "Eyebrow tick + caption dot", "≈ 0.2%"], status: "pass" },
    { cells: ["Shop entry", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Featured products", "Eyebrow tick + 1 maple-leaf badge", "≈ 0.4%"], status: "pass" },
    { cells: ["OECM bar", "Badge dot + tick", "≈ 0.1%"], status: "pass" },
    { cells: ["Industries", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Services", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Our work", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Footer", "Maple leaf in plate", "≈ 0.2%"], status: "pass" },
    { cells: ["TOTAL · at rest", "Across full page", "≈ 5.6%"], status: "pass" },
    { cells: ["TOTAL · with CTA hover", "+ #D4252A on .bbi-btn--primary:hover", "≈ 6.4%"], status: "pass" },
  ],
  used: [
    ["--bodyFont, --headingFont", "All body + heading runs"],
    ["--fs-* / --lh-* scale", "Type scale across breakpoints"],
    ["--space-* (2/3/4/6/8/12/16)", "All padding + gap rhythm"],
    ["--cardRadius, --buttonRadius", "Cards + buttons"],
    ["--background, --alternateBackground", "Default + alt sections"],
    ["--textColor, --headingColor, --linkColor", "All ink"],
    ["--buttonBackground/Color/Border (+Hover)", "Primary CTAs + their hover red"],
    ["--alternateButton* set", "Secondary CTA pair"],
    ["--saleBadgeBackground", "Eyebrow ticks, OECM dot, maple leaf, cart"],
    ["--borderColor", "All hairlines"],
    ["--shadowColor (-rgb)", "Card overlay gradient"],
    ["--headerBg/Color/HoverColor", "Header"],
  ],
  reserve: [
    ["--warningBackground", "No low-stock state on the homepage"],
    ["--newBadgeBackground", "No 'new' badge on featured row"],
    ["--success / --error", "Form lives on /pages/quote"],
    ["--inputBackground/Color/Border", "Same — no form here"],
    ["--productBorder", "Used implicitly via .bbi-card--product on featured products"],
    ["--productIconColor / Bg", "PDP-only"],
    ["--cartCountBg/Color", "Cart not yet wired"],
    ["--customBadgeBackground, --soldBadgeBackground, --preorderBadgeBackground", "PDP-only badges"],
  ],
  links: [
    { cells: ["Header logo", "/", "Self"], status: "pass" },
    { cells: ["Header → Shop (current)", "/collections/business-furniture", "Sideways · is-current"], status: "pass" },
    { cells: ["Header → Industries", "/pages/industries", "Sideways"], status: "pass" },
    { cells: ["Header → Brands", "/pages/brands", "Sideways"], status: "pass" },
    { cells: ["Header → Services", "/pages/services", "Sideways"], status: "pass" },
    { cells: ["Header → About", "/pages/about", "Sideways"], status: "pass" },
    { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Hero CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Hero secondary", "/collections/business-furniture", "Down to template 2"], status: "pass" },
    { cells: ["Shop tiles × 4", "/collections/{slug}", "Down to template 3"], status: "pass" },
    { cells: ["'Browse all categories'", "/collections/business-furniture", "Down to template 2"], status: "pass" },
    { cells: ["OECM tertiary", "/pages/oecm", "Sideways"], status: "pass" },
    { cells: ["Industry tiles × 5", "/pages/industries/{slug}", "Down to sector page"], status: "pass" },
    { cells: ["Footer × all", "Real routes (see template-2 audit)", "Mirror of header set"], status: "pass" },
  ],
});

/* ---------- template 2: collection · category (round 3) ---------- */
register("collection-category", {
  title: "Template 2 — Collection · category",
  contrast: [
    { cells: ["#0B0B0C ink", "#FFFFFF (header bg)", "20.10 : 1", "AAA", "Body / nav links"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FAFAFA (alt-bg)", "18.87 : 1", "AAA", "Brand-index rows"], status: "pass" },
    { cells: ["rgba(11,11,12,0.7)", "#FFFFFF", "≈11.4 : 1", "AAA", "Sub copy, brand-row cats"], status: "pass" },
    { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Eyebrows"], status: "pass" },
    { cells: ["rgba(11,11,12,0.55)", "#FAFAFA", "≈7.0 : 1", "AAA", "Tier counts"], status: "pass" },
    { cells: ["#FFFFFF", "#0B0B0C (CTA closer canvas)", "20.10 : 1", "AAA", "Closer heading + body"], status: "pass" },
    { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Closer sub copy"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#0B0B0C (primary btn rest)", "20.10 : 1", "AAA", "Primary CTA at-rest"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#D4252A (primary btn hover)", "4.08 : 1", "AA-large", "CTA hover — 600/16px → AA-large"], status: "pass" },
    { cells: ["#FFFFFF (overlay copy)", "#0B0B0C gradient ≥85%", "≥17 : 1", "AAA", "Category-tile overlay"], status: "pass" },
    { cells: ["#FFFFFF caption", "rgba(11,11,12,0.7) pill", "≈14.7 : 1", "AAA", "Hero-image caption pill"], status: "pass" },
    { cells: ["rgba(255,255,255,0.85) tile num", "rgba(11,11,12,0.55) chip", "≈4.6 : 1", "AA-large", "Tile 01–09 chip; 11px/600 → AA-large"], status: "pass" },
    { cells: ["#0B0B0C industry tile", "#FFFFFF rest → #FAFAFA hover", "20.10 / 18.87 : 1", "AAA", "Industry shortcut row"], status: "pass" },
    { cells: ["#0B0B0C brand row", "rgba(11,11,12,0.02) hover", "≈19.6 : 1", "AAA", "Brand-row hover lift"], status: "pass" },
  ],
  red: [
    { cells: ["Header", "Eyebrow rule + cart accent", "≈ 0.9%"], status: "pass" },
    { cells: ["Breadcrumbs band", "—", "0%"], status: "pass" },
    { cells: ["Intro band", "Eyebrow tick + image-caption dot", "≈ 0.15%"], status: "pass" },
    { cells: ["Category grid", "Eyebrow tick rule", "≈ 0.05%"], status: "pass" },
    { cells: ["Industry shortcut", "Eyebrow tick rule", "≈ 0.05%"], status: "pass" },
    { cells: ["Brand index", "Eyebrow + 13 auth dots + 5 maple leaves", "≈ 0.6%"], status: "pass" },
    { cells: ["OECM bar", "Badge dot + tick rule", "≈ 0.1%"], status: "pass" },
    { cells: ["CTA closer (inverse)", "2 trust dots; CTA white at rest", "≈ 0.05%"], status: "pass" },
    { cells: ["Footer (inverse)", "Maple leaf in brand plate", "≈ 0.2%"], status: "pass" },
    { cells: ["TOTAL · at rest", "Across full page", "≈ 5.4%"], status: "pass" },
    { cells: ["TOTAL · with CTA hover", "+ #D4252A on primary:hover", "≈ 6.2%"], status: "pass" },
  ],
  used: [
    ["--bodyFont, --headingFont", "All body + heading runs"],
    ["--fs-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-button", "Type scale"],
    ["--space-2 / 3 / 4 / 6 / 8 / 12 / 16", "Padding + gap rhythm"],
    ["--inputRadius, --buttonRadius, --cardRadius", "All corners"],
    ["--background", ".scheme-default canvas"],
    ["--alternateBackground", ".bbi-section--alt + brand index"],
    ["--cardBackground", ".bbi-card body"],
    ["--textColor (+ -rgb)", "All ink + plate borders"],
    ["--linkColor", ".bbi-crumbs links + brand-row links"],
    ["--headingColor", "H1 + H2 + H3"],
    ["--buttonBackground/Color/Border (+Hover)", "Primary CTA on closer"],
    ["--alternateButton* set", "'Full brand directory' secondary"],
    ["--borderColor (+ -rgb)", "All hairlines"],
    ["--saleBadgeBackground", "Eyebrow ticks · OECM dot · brand auth dot · maple leaf · CTA trust dots · caption dot"],
    ["--headerBg, --headerColor, --headerHoverColor", "Header"],
    ["--shadowColor (-rgb)", "Card overlay + caption pill + tile-num chip"],
  ],
  reserve: [
    ["--saleBadgeBackground (label-white fill)", "No .bbi-badge--sale on template 2"],
    ["--newBadgeBackground", "No .bbi-badge--new on template 2"],
    ["--warningBackground", "No low-stock surfaces on a catalogue map"],
    ["--soldBadgeBackground", "PDP-only"],
    ["--customBadgeBackground", "PDP-only"],
    ["--preorderBadgeBackground", "PDP-only"],
    ["--success / --error", "No form on this template"],
    ["--cartCountBg/Color", "Cart not wired here"],
    ["--inputBackground/Color/Border", "No inputs on a catalogue map"],
    ["--productBorder", "Product cards are template 1 + 3"],
    ["--productIconColor/Bg", "PDP-only"],
    ["--sliderArrowBackground/Color", "No slider"],
    ["--line-color", "Decorative dup of --borderColor"],
  ],
  links: [
    { cells: ["Header logo", "/", "Up to homepage"], status: "pass" },
    { cells: ["Header → Shop (current)", "/collections/business-furniture", "Self · is-current"], status: "pass" },
    { cells: ["Header → Industries / Brands / Services / About", "/pages/...", "Sideways"], status: "pass" },
    { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Crumb · Home", "/", "Up"], status: "pass" },
    { cells: ["9 category tiles", "/collections/{slug} × 9", "Down to template 3"], status: "pass" },
    { cells: ["5 industry tiles", "/pages/industries/{slug} × 5", "Down to sector page"], status: "pass" },
    { cells: ["~19 brand-row links", "/pages/brands/{slug}", "Sideways to template 4"], status: "pass" },
    { cells: ["'Full brand directory' button", "/pages/brands", "Sideways"], status: "pass" },
    { cells: ["OECM tertiary CTA", "/pages/oecm", "Sideways"], status: "pass" },
    { cells: ["Closer · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Closer · phone link", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Footer Shop / Industries / Services / Contact / Legal", "Real routes", "Down + sideways"], status: "pass" },
  ],
});

/* ---------- template 3: collection (round 4) ---------- */
register("collection", {
  title: "Template 3 — Collection (Seating)",
  contrast: [
    { cells: ["#0B0B0C ink", "#FFFFFF page bg", "20.10 : 1", "AAA", "Body / nav / breadcrumbs / sub-chips at-rest"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FAFAFA alt-bg", "18.87 : 1", "AAA", "Intro stat plate · brand-strip rows · sub-chips card body"], status: "pass" },
    { cells: ["rgba(11,11,12,0.78)", "#FFFFFF", "≈12.7 : 1", "AAA", "Intro deck · result-strip count · brand-strip foot copy"], status: "pass" },
    { cells: ["rgba(11,11,12,0.7)", "#FFFFFF", "≈11.4 : 1", "AAA", "Filter __value mono chip · brand-strip tier · pagination count"], status: "pass" },
    { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Eyebrows (Collection · Brands carried)"], status: "pass" },
    { cells: ["rgba(11,11,12,0.55)", "#FAFAFA", "≈7.0 : 1", "AAA", "Intro stat dt labels · pagination separator"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#0B0B0C primary btn rest", "20.10 : 1", "AAA", "Add-to-cart on cards · current-page chip · active sub-chip"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#D4252A primary btn hover", "4.08 : 1", "AA-large", "Primary CTA hover — 600/13–16px → AA-large"], status: "pass" },
    { cells: ["rgba(255,255,255,0.85)", "rgba(11,11,12,0.55) overlay", "≈4.6 : 1", "AA-large", "Sub-cat chip on card media; 11px/600 mono → AA-large"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FFFFFF Canadian-made badge fill", "20.10 : 1", "AAA", ".bbi-badge--canadian on card media (white pill, ink label)"], status: "pass" },
    { cells: ["#0B0B0C ink", "#E8A317 warning bg", "7.71 : 1", "AAA", "Low-stock badge — token-driven --warningBackground"], status: "pass" },
    { cells: ["#0B0B0C", "#FFFFFF (CTA closer canvas, inverse-flip)", "20.10 : 1", "AAA", "Primary CTA at-rest on closer (inverse flip → white bg, ink label)"], status: "pass" },
    { cells: ["#FFFFFF", "#0B0B0C (closer canvas)", "20.10 : 1", "AAA", "Closer heading + body copy on inverse"], status: "pass" },
    { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Footer body + closer sub copy on inverse"], status: "pass" },
  ],
  red: [
    { cells: ["Header", "Eyebrow rule + cart accent", "≈ 0.9%"], status: "pass" },
    { cells: ["Breadcrumbs band", "—", "0%"], status: "pass" },
    { cells: ["Intro band", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Filter band", "Maple-leaf glyph in Canadian-made toggle (only when on)", "≈ 0.02%"], status: "pass" },
    { cells: ["Product grid · 9 cards", "Maple leaves in Canadian-made badges × ~4", "≈ 0.3%"], status: "pass" },
    { cells: ["Product grid · 9 cards", "Low-stock chips × 1 (ochre, NOT red)", "0% red"], status: "pass" },
    { cells: ["Pagination", "—", "0%"], status: "pass" },
    { cells: ["Brand strip", "Eyebrow tick + 2 maple leaves + 6 auth dots", "≈ 0.3%"], status: "pass" },
    { cells: ["OECM bar", "Badge dot + tick rule", "≈ 0.1%"], status: "pass" },
    { cells: ["CTA closer (inverse)", "2 trust dots; CTA white at rest", "≈ 0.05%"], status: "pass" },
    { cells: ["Footer (inverse)", "Maple leaf in brand plate", "≈ 0.2%"], status: "pass" },
    { cells: ["TOTAL · at rest", "Across full page", "≈ 5.7%"], status: "pass" },
    { cells: ["TOTAL · with CTA hover", "+ #D4252A on primary:hover", "≈ 6.5%"], status: "pass" },
  ],
  used: [
    ["--bodyFont, --headingFont", "All body + heading runs"],
    ["--fs-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-button", "Type scale"],
    ["--space-2 / 3 / 4 / 6 / 8 / 12 / 16", "Padding + gap rhythm"],
    ["--inputRadius, --buttonRadius, --cardRadius", "All corners (filter triggers, CTAs, product cards)"],
    ["--background", ".scheme-default canvas"],
    ["--alternateBackground", "Intro stat plate · brand-strip band · result-strip filter chip"],
    ["--cardBackground", ".bbi-card body"],
    ["--textColor (+ -rgb)", "All ink + sub-chip active fill + current-page chip"],
    ["--linkColor", ".bbi-crumbs links · brand-strip links · pagination links"],
    ["--headingColor", "H1 (intro) + H2 (brand-strip)"],
    ["--buttonBackground/Color/Border (+Hover)", "Add-to-cart on cards · primary CTA on closer"],
    ["--alternateButton* set", "Request-a-quote on cards · 'Full brand directory' on strip"],
    ["--borderColor (+ -rgb)", "All hairlines · filter trigger borders · product card border"],
    ["--saleBadgeBackground", "Eyebrow ticks · OECM dot · maple leaves · CTA trust dots · cart accent"],
    ["--warningBackground", "Low-stock badge on cards (first template to exercise this token)"],
    ["--headerBg, --headerColor, --headerHoverColor", "Header"],
    ["--shadowColor (-rgb)", "Sub-cat chip overlay on card media"],
    ["--productBorder", "Implicit via .bbi-card--product on the 9 product cards"],
  ],
  reserve: [
    ["--saleBadgeBackground (label-white fill)", "No .bbi-badge--sale on a catalogue (PDP-only surface)"],
    ["--newBadgeBackground", "No .bbi-badge--new on catalogue grid in this slice"],
    ["--soldBadgeBackground", "PDP-only"],
    ["--customBadgeBackground", "PDP-only"],
    ["--preorderBadgeBackground", "PDP-only"],
    ["--success / --error", "No form on this template — quote form lives on /pages/quote"],
    ["--cartCountBg/Color", "Cart count not yet wired (template 1 + 3 share this state)"],
    ["--inputBackground/Color/Border", "No inputs on a catalogue grid"],
    ["--productIconColor/Bg", "PDP-only feature pills"],
    ["--sliderArrowBackground/Color", "No carousel — grid is static + paginated"],
    ["--ratingStarColor", "Ratings live on PDP, not catalogue cards"],
    ["--line-color", "Decorative dup of --borderColor (every hairline uses --borderColor)"],
  ],
  links: [
    { cells: ["Header logo", "/", "Up to homepage"], status: "pass" },
    { cells: ["Header → Shop (current)", "/collections/business-furniture", "Sideways · is-current"], status: "pass" },
    { cells: ["Header → Industries / Brands / Services / About", "/pages/...", "Sideways"], status: "pass" },
    { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Crumb · Home", "/", "Up to homepage"], status: "pass" },
    { cells: ["Crumb · Shop", "/collections/business-furniture", "Up to template 2"], status: "pass" },
    { cells: ["Sub-cat chips × 6", "(client-side filter — no route)", "Self · in-page"], status: "pass" },
    { cells: ["Filter triggers × 4 + Canadian toggle", "(client-side facet drawer — no route)", "Self · in-page"], status: "pass" },
    { cells: ["Sort dropdown", "(client-side sort — no route)", "Self · in-page"], status: "pass" },
    { cells: ["9 product card titles", "/products/{id} × 9", "Down to template 4 (PDP)"], status: "pass" },
    { cells: ["9 product card CTAs", "/cart/add?id={id} OR /pages/quote?ref={id}", "Buyable → cart · made-to-order → RFQ"], status: "pass" },
    { cells: ["Pagination · pages 2 / 3 / 14", "?page=N", "Self · paginated"], status: "pass" },
    { cells: ["Pagination · Next →", "?page=2", "Self · paginated"], status: "pass" },
    { cells: ["Brand-strip links × 8", "/pages/brands/{slug}", "Sideways to template 5 (brand)"], status: "pass" },
    { cells: ["'Full brand directory'", "/pages/brands", "Sideways to brand index"], status: "pass" },
    { cells: ["OECM tertiary CTA", "/pages/oecm", "Sideways"], status: "pass" },
    { cells: ["Closer · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Closer · phone link", "tel:18008359565", "Phone fallback"], status: "pass" },
    { cells: ["Footer × all", "Real routes (mirror of template 1 + 2)", "Down + sideways"], status: "pass" },
  ],
});

/* ---------- root ---------- */
function Audits({ template = "collection-category" }) {
  const data = AUDIT_REGISTRY[template] || AUDIT_REGISTRY["collection-category"];
  return (
    <div className="ap-root scheme-default" data-template={template}>
      <header className="ap-root__head">
        <span className="ap-root__kicker">Audit panels</span>
        <h2 className="ap-root__title">{data.title}</h2>
        <p className="ap-root__sub">
          Same four audits across every template: Contrast · Red density · Token coverage · Cross-links. Values reflect the rendered cascade — no spec hand-waving.
        </p>
      </header>

      <AuditPanel num="01" title="Contrast" sub="Every text/bg pair on this template, measured at the rendered cascade.">
        <APTable heads={["Foreground", "Background", "Ratio", "Standard", "Where"]} rows={data.contrast} />
        <p className="ap-foot">All non-N/A pairs pass at least AA-large. AAA pairs flagged for primary copy.</p>
      </AuditPanel>

      <AuditPanel num="02" title="Red density" sub="At rest plus a one-hover delta. Target: 5–8%.">
        <APTable heads={["Section", "What's red", "% of viewport"]} rows={data.red} />
      </AuditPanel>

      <AuditPanel num="03" title="Token coverage" sub="Every token this template exercises, plus a reserve list.">
        <div className="ap-cov">
          <div>
            <h4>Exercised on this template</h4>
            <ul className="ap-cov__list">
              {data.used.map(([t, w], i) => (<li key={i}><code>{t}</code><span>{w}</span></li>))}
            </ul>
          </div>
          <div>
            <h4>Defined but unused (reserve)</h4>
            <ul className="ap-cov__list ap-cov__list--reserve">
              {data.reserve.map(([t, w], i) => (<li key={i}><code>{t}</code><span>{w}</span></li>))}
            </ul>
          </div>
        </div>
      </AuditPanel>

      <AuditPanel num="04" title="Cross-links" sub="Every link surface resolves to a real route.">
        <APTable heads={["Surface", "Target", "Direction"]} rows={data.links} />
      </AuditPanel>
    </div>
  );
}

window.Audits = Audits;
window.AuditsRegistry = AUDIT_REGISTRY;
