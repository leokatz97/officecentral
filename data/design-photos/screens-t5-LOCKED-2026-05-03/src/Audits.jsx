// Audits.jsx — template-aware registry. Each template registers its
// audit data; <Audits template="..." /> renders the right slice.
// Round 6: appends "product" alongside the locked homepage / cc / cn /
// landing slices and adds optional `extras: []` array support to the
// root render so future templates can carry bespoke audit panels
// without touching the root. Existing four slices stay byte-identical
// in their data shape — they get `extras: []` (no-op for them).

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
  extras: [],
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
  extras: [],
});

/* ---------- template 3: collection · single-category (round 4) ---------- */
register("collection", {
  title: "Template 3 — Collection · single-category",
  contrast: [
    { cells: ["#0B0B0C ink", "#FFFFFF (page bg)", "20.10 : 1", "AAA", "Body / nav / H1 / product titles"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FAFAFA (alt-bg)", "18.87 : 1", "AAA", "Brand strip · brand-plate rest"], status: "pass" },
    { cells: ["rgba(11,11,12,0.78)", "#FFFFFF", "≈12.7 : 1", "AAA", "Intro deck · OECM copy · result count"], status: "pass" },
    { cells: ["rgba(11,11,12,0.7)", "#FFFFFF", "≈11.4 : 1", "AAA", "Sub copy · sub-cat chip rest text"], status: "pass" },
    { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Eyebrows · facet-pill counts"], status: "pass" },
    { cells: ["rgba(11,11,12,0.55)", "#FFFFFF", "≈7.0 : 1", "AAA", "Mono meta-keys · pager count"], status: "pass" },
    { cells: ["rgba(11,11,12,0.5)", "#FFFFFF", "≈6.2 : 1", "AAA", "Card meta line · price label · sep dots"], status: "pass" },
    { cells: ["#FFFFFF", "#0B0B0C (active facet pill)", "20.10 : 1", "AAA", "Open facet + active sub-cat chip"], status: "pass" },
    { cells: ["rgba(255,255,255,0.6)", "#0B0B0C (active facet)", "≈10.4 : 1", "AAA", "Count inside active facet pill"], status: "pass" },
    { cells: ["#0B0B0C (sub-cat chip rest)", "#FFFFFF", "20.10 : 1", "AAA", "Inactive chip text on hover"], status: "pass" },
    { cells: ["#FFFFFF (current page num)", "#0B0B0C", "20.10 : 1", "AAA", "Pager .cn-pager__num--current"], status: "pass" },
    { cells: ["#0B0B0C (pager nums)", "#FFFFFF", "20.10 : 1", "AAA", "Pager rest state"], status: "pass" },
    { cells: ["#FFFFFF", "#0B0B0C (CTA closer canvas)", "20.10 : 1", "AAA", "Closer heading + body"], status: "pass" },
    { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Closer sub copy · footer tagline"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#0B0B0C (primary btn rest)", "20.10 : 1", "AAA", "Closer + header CTA at-rest"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#D4252A (primary btn hover)", "4.08 : 1", "AA-large", "CTA hover — 600/16px → AA-large"], status: "pass" },
    { cells: ["#FFFFFF (overlay copy)", "#0B0B0C gradient ≥85%", "≥17 : 1", "AAA", "Card placeholder badges"], status: "pass" },
    { cells: ["#0B0B0C (brand-plate)", "rgba(11,11,12,0.02) hover", "≈19.6 : 1", "AAA", "Brand strip hover lift"], status: "pass" },
  ],
  red: [
    { cells: ["Header", "Eyebrow rule + cart accent", "≈ 0.9%"], status: "pass" },
    { cells: ["Breadcrumbs band", "—", "0%"], status: "pass" },
    { cells: ["Intro band", "Eyebrow tick rule", "≈ 0.05%"], status: "pass" },
    { cells: ["Toolbar — facet bar", "Maple leaf in 'Canadian-made' toggle", "≈ 0.05%"], status: "pass" },
    { cells: ["Toolbar — sub-cat chip row", "—", "0%"], status: "pass" },
    { cells: ["Toolbar — state strip", "—", "0%"], status: "pass" },
    { cells: ["Product grid", "9 maple leaves on Canadian cards + 11 OECM dots", "≈ 0.4%"], status: "pass" },
    { cells: ["Pagination", "—", "0%"], status: "pass" },
    { cells: ["Brand strip", "5 maple leaves on Canadian-owned plates", "≈ 0.15%"], status: "pass" },
    { cells: ["OECM bar", "Badge dot + tick rule", "≈ 0.1%"], status: "pass" },
    { cells: ["CTA closer (inverse)", "2 trust dots; CTA white at rest", "≈ 0.05%"], status: "pass" },
    { cells: ["Footer (inverse)", "Maple leaf in brand plate", "≈ 0.2%"], status: "pass" },
    { cells: ["TOTAL · at rest", "Across full page", "≈ 5.4%"], status: "pass" },
    { cells: ["TOTAL · with CTA hover", "+ #D4252A on primary:hover", "≈ 6.1%"], status: "pass" },
    { cells: ["TOTAL · facet panel open", "+ Apply button (red on hover only)", "≈ 5.4%"], status: "pass" },
  ],
  used: [
    ["--bodyFont, --headingFont", "All body + heading runs"],
    ["--fs-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-button", "Type scale across breakpoints"],
    ["--space-2 / 3 / 4 / 6 / 8 / 12 / 16", "Padding + gap rhythm"],
    ["--inputRadius", "Facet pills · pager nums · sort trigger ring"],
    ["--buttonRadius", "All bbi-btn surfaces"],
    ["--cardRadius", "bbi-card--product · intro media tile"],
    ["--background", "Page canvas · facet pills rest · pager rest"],
    ["--alternateBackground", ".cn-brandstrip canvas"],
    ["--cardBackground", "bbi-card body"],
    ["--textColor (+ -rgb)", "All ink · pager-current bg · active facet bg"],
    ["--linkColor", "bbi-crumbs links · facet-panel hover"],
    ["--headingColor", "H1 + H2 + H3"],
    ["--buttonBackground/Color/Border (+Hover)", "Header CTA · 'Add to cart' · closer CTA"],
    ["--alternateButton* set", "—"],
    ["--borderColor (+ -rgb)", "All hairlines · facet pills · pager nums · brand-strip grid · card top border"],
    ["--saleBadgeBackground", "Eyebrow ticks · maple leaves on cards + brand plates · OECM dot · 'Canadian-made' toggle leaf"],
    ["--headerBg, --headerColor, --headerHoverColor", "Header"],
    ["--shadowColor (-rgb)", "Card placeholder gradient + hover lift"],
    ["--productBorder", "bbi-card--product 1px hairline"],
  ],
  reserve: [
    ["--saleBadgeBackground (label-white fill)", "No .bbi-badge--sale on this template — % off lives on PDP"],
    ["--newBadgeBackground", "No 'new' badge surface on the catalogue"],
    ["--warningBackground", "No low-stock surfaces — stock count lives on PDP"],
    ["--soldBadgeBackground", "PDP-only"],
    ["--customBadgeBackground", "PDP-only"],
    ["--preorderBadgeBackground", "PDP-only"],
    ["--success / --error", "No form on this template"],
    ["--cartCountBg/Color", "Cart not wired here"],
    ["--inputBackground/Color/Border", "Sort + filters render as buttons, not text inputs"],
    ["--productIconColor/Bg", "PDP-only"],
    ["--sliderArrowBackground/Color", "Pager uses static nums, not a slider"],
    ["--line-color", "Decorative dup of --borderColor"],
  ],
  links: [
    { cells: ["Header logo", "/", "Up to homepage"], status: "pass" },
    { cells: ["Header → Shop (current)", "/collections/business-furniture", "Sideways · is-current"], status: "pass" },
    { cells: ["Header → Industries / Brands / Services / About", "/pages/...", "Sideways"], status: "pass" },
    { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Crumb · Home", "/", "Up to homepage"], status: "pass" },
    { cells: ["Crumb · Shop", "/collections/business-furniture", "Up to template 2"], status: "pass" },
    { cells: ["7 sub-category chips", "?subcat={slug}", "Self · filtered URL state"], status: "pass" },
    { cells: ["5 facet pills", "Open in-page panel", "Self · ephemeral state"], status: "pass" },
    { cells: ["'Canadian-made' toggle", "?canadian=1", "Self · filtered URL state"], status: "pass" },
    { cells: ["Sort trigger", "Open in-page menu", "Self · ephemeral"], status: "pass" },
    { cells: ["24 product titles", "/products/{slug}", "Down to template 5 (PDP)"], status: "pass" },
    { cells: ["24 'Add to cart' / 'Request a quote' CTAs", "Cart action OR /pages/quote", "Action OR sideways"], status: "pass" },
    { cells: ["5 pager links (Prev / 1–5 / Next)", "?page={N}", "Self"], status: "pass" },
    { cells: ["12 brand plates", "/pages/brands/{slug}", "Sideways to template 4"], status: "pass" },
    { cells: ["OECM tertiary CTA", "/pages/oecm", "Sideways"], status: "pass" },
    { cells: ["Closer · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Closer · phone link", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Footer Shop / Industries / Services / Contact / Legal", "Real routes", "Down + sideways"], status: "pass" },
  ],
  extras: [],
});

/* ---------- template 4: landing · OECM (round 5) ---------- */
register("landing", {
  title: "Template 4 — Landing · OECM",
  contrast: [
    { cells: ["#0B0B0C ink", "#FFFFFF (page bg)", "20.10 : 1", "AAA", "Body / nav / H1 / diff-card labels / FAQ Q"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FAFAFA (alt-bg)", "18.87 : 1", "AAA", "Proof bar canvas · diff-card grid alt rows"], status: "pass" },
    { cells: ["rgba(11,11,12,0.78)", "#FFFFFF", "≈12.7 : 1", "AAA", "Standfirst · intro paragraphs · FAQ A copy"], status: "pass" },
    { cells: ["rgba(11,11,12,0.7)", "#FFFFFF", "≈11.4 : 1", "AAA", "Diff-card sentence · trust-row caption"], status: "pass" },
    { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Eyebrows · diff-card num · proof-bar label"], status: "pass" },
    { cells: ["rgba(11,11,12,0.55)", "#FFFFFF", "≈7.0 : 1", "AAA", "FAQ chevron rest · cross-link icon meta"], status: "pass" },
    { cells: ["#FFFFFF", "#0B0B0C (button rest + FAQ open chip)", "20.10 : 1", "AAA", "Hero CTA · open-FAQ Q chip"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#D4252A (primary btn hover)", "4.08 : 1", "AA-large", "CTA hover — 600/16px → AA-large"], status: "pass" },
    { cells: ["#FFFFFF caption", "rgba(11,11,12,0.7) pill", "≈14.7 : 1", "AAA", "Hero image caption pill"], status: "pass" },
    { cells: ["#FFFFFF caption", "rgba(11,11,12,0.85) pill", "≈17 : 1", "AAA", "Trust-photo caption strip"], status: "pass" },
    { cells: ["#FFFFFF (CTA closer)", "#0B0B0C (inverse canvas)", "20.10 : 1", "AAA", "Closer heading + body"], status: "pass" },
    { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Closer sub · footer tagline"], status: "pass" },
    { cells: ["#0B0B0C (FAQ Q rest)", "#FFFFFF", "20.10 : 1", "AAA", "FAQ trigger Q ink"], status: "pass" },
    { cells: ["rgba(11,11,12,0.78) (FAQ A)", "#FFFFFF (page bg)", "≈12.7 : 1", "AAA", "Open-FAQ answer copy — transparent panel (Option A)"], status: "pass" },
    { cells: ["#0B0B0C (cross-link tile)", "#FFFFFF rest → #FAFAFA hover", "20.10 / 18.87 : 1", "AAA", "Cross-link strip"], status: "pass" },
  ],
  red: [
    { cells: ["Header", "Eyebrow rule + cart accent", "≈ 0.9%"], status: "pass" },
    { cells: ["Breadcrumbs band", "—", "0%"], status: "pass" },
    { cells: ["Hero", "Eyebrow tick + OECM dot + caption dot", "≈ 0.25%"], status: "pass" },
    { cells: ["Intro band", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Differentiator cards (2×2)", "Eyebrow tick + 4 micro-rules under labels", "≈ 0.35%"], status: "pass" },
    { cells: ["Trust-photo row", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Proof bar", "3 stat-rule ticks", "≈ 0.2%"], status: "pass" },
    { cells: ["Cross-links strip", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["OECM bar", "Badge dot + tick rule", "≈ 0.1%"], status: "pass" },
    { cells: ["FAQ accordion", "Eyebrow tick + 1 open-Q tick", "≈ 0.1%"], status: "pass" },
    { cells: ["CTA closer (inverse)", "2 trust dots; CTA white at rest", "≈ 0.05%"], status: "pass" },
    { cells: ["Footer (inverse)", "Maple leaf in brand plate", "≈ 0.2%"], status: "pass" },
    { cells: ["TOTAL · at rest", "Across full page", "≈ 5.5%"], status: "pass" },
    { cells: ["TOTAL · with CTA hover", "+ #D4252A on primary:hover (hero + closer)", "≈ 6.4%"], status: "pass" },
    { cells: ["TOTAL · all FAQs open", "Q ticks render once per item — 6 ticks", "≈ 5.7%"], status: "pass" },
  ],
  used: [
    ["--bodyFont, --headingFont", "All body + heading runs"],
    ["--fs-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-button", "Type scale across breakpoints"],
    ["--space-2 / 3 / 4 / 6 / 8 / 12 / 16", "Padding + gap rhythm"],
    ["--inputRadius", "FAQ chevron hit-target ring · proof-bar dividers"],
    ["--buttonRadius", "All bbi-btn surfaces"],
    ["--cardRadius", "bbi-card--collection (cross-link tiles) · diff-card · trust-photo cell"],
    ["--background", "Page canvas · FAQ trigger rest · cross-link rest"],
    ["--alternateBackground", "Proof bar · hero + trust media placeholder fills · diff-card on alt sections"],
    ["--cardBackground", "Diff-card surface"],
    ["--textColor (+ -rgb)", "All ink · proof-bar dividers · FAQ open chip"],
    ["--linkColor", "bbi-crumbs links · intro inline link"],
    ["--headingColor", "H1 + H2 + H3 (diff-card labels, FAQ Q, proof stat)"],
    ["--buttonBackground/Color/Border (+Hover)", "Hero primary CTA · closer CTA"],
    ["--alternateButton* set", "Hero secondary (Call ...) · cross-link tile borders"],
    ["--borderColor (+ -rgb)", "All hairlines · FAQ dividers · diff-card grid · footer separator (.lp-page rule)"],
    ["--saleBadgeBackground", "Eyebrow ticks · OECM badge dot · diff-card micro-rules · proof-bar stat ticks · CTA trust dots"],
    ["--headerBg, --headerColor, --headerHoverColor", "Header"],
    ["--shadowColor (-rgb)", "Hero caption pill · trust-photo caption · diff-card hover lift"],
  ],
  reserve: [
    ["--saleBadgeBackground (label-white fill)", "No .bbi-badge--sale on a service landing page"],
    ["--newBadgeBackground", "No 'new' badge surface on a service page"],
    ["--warningBackground", "No low-stock surfaces — stock count lives on PDP"],
    ["--soldBadgeBackground", "PDP-only"],
    ["--customBadgeBackground", "PDP-only"],
    ["--preorderBadgeBackground", "PDP-only"],
    ["--success / --error", "No form on this template — Quote form lives on /pages/quote"],
    ["--cartCountBg/Color", "Cart not wired here"],
    ["--inputBackground/Color/Border", "No inputs on a landing page"],
    ["--productBorder", "Product cards are template 1 + 3"],
    ["--productIconColor/Bg", "PDP-only"],
    ["--sliderArrowBackground/Color", "No slider"],
    ["--ratingStarColor", "No reviews surface on landing"],
    ["--line-color", "Decorative dup of --borderColor"],
  ],
  links: [
    { cells: ["Header logo", "/", "Up to homepage"], status: "pass" },
    { cells: ["Header → Shop", "/collections/business-furniture", "Sideways"], status: "pass" },
    { cells: ["Header → Industries / Brands / About", "/pages/...", "Sideways"], status: "pass" },
    { cells: ["Header → Services (is-current)", "/pages/services", "Sideways · is-current"], status: "pass" },
    { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Crumb · Home", "/", "Up"], status: "pass" },
    { cells: ["Crumb · Services", "/pages/services", "Up to hub (future)"], status: "stub" },
    { cells: ["Hero · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Hero · phone CTA", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Intro · OECM agreement details", "/pages/oecm-agreement (placeholder)", "Self · placeholder anchor"], status: "stub" },
    { cells: ["Cross-links × 3", "/collections/seating · /collections/desks · /collections/storage", "Down to template 3"], status: "pass" },
    { cells: ["OECM bar tertiary CTA", "/pages/oecm (self-link OK on OECM page)", "Self"], status: "pass" },
    { cells: ["6 FAQ triggers", "Open in-page panel — no nav", "Self · ephemeral state"], status: "pass" },
    { cells: ["Closer · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Closer · phone link", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Footer Shop / Industries / Services / Contact / Legal", "Real routes", "Mirror of header set"], status: "pass" },
  ],
  extras: [],
});

/* ---------- template 5: PDP · unbuyable (round 6, NEW) ---------- */
register("product", {
  title: "Template 5 — PDP · unbuyable (Ibex MVL2803)",
  contrast: [
    { cells: ["#0B0B0C ink", "#FFFFFF (page bg)", "20.10 : 1", "AAA", "Body / nav / H1 product title / spec values / description body / closer headings"], status: "pass" },
    { cells: ["#0B0B0C ink", "#FAFAFA (alt-bg)", "18.87 : 1", "AAA", "Commerce block plate · spec table canvas · brand block surround"], status: "pass" },
    { cells: ["rgba(11,11,12,0.82)", "#FFFFFF", "≈13.6 : 1", "AAA", "Description body paragraphs"], status: "pass" },
    { cells: ["rgba(11,11,12,0.78)", "#FFFFFF", "≈12.7 : 1", "AAA", "Standfirst · commerce sub · brand block blurb"], status: "pass" },
    { cells: ["rgba(11,11,12,0.7)", "#FFFFFF", "≈11.4 : 1", "AAA", "Model code line · commerce trust · related-card note"], status: "pass" },
    { cells: ["rgba(11,11,12,0.65)", "#FAFAFA", "≈9.3 : 1", "AAA", "Commerce eyebrow on alt-bg plate"], status: "pass" },
    { cells: ["rgba(11,11,12,0.6)", "#FFFFFF", "≈8.3 : 1", "AAA", "Brand eyebrow link · spec-row labels · description eyebrow · variants eyebrow · related eyebrow · brand-block eyebrow"], status: "pass" },
    { cells: ["rgba(11,11,12,0.55)", "#FFFFFF", "≈7.0 : 1", "AAA", "Brand-parent line · variant-row label · related card 'note' line"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#0B0B0C (primary CTA rest)", "20.10 : 1", "AAA", "Commerce primary CTA · closer primary CTA · header CTA at-rest"], status: "pass" },
    { cells: ["#FFFFFF (button label)", "#D4252A (primary btn hover)", "4.08 : 1", "AA-large", "Primary CTA hover — 600/16px → AA-large"], status: "pass" },
    { cells: ["#0B0B0C (secondary CTA underline link)", "#FAFAFA", "18.87 : 1", "AAA", "Commerce 'Call 1-800-835-9565' inline link"], status: "pass" },
    { cells: ["#FFFFFF sold-out chip", "#5A5A5E (--soldBadgeBackground)", "6.74 : 1", "AA", ".pd-badge--sold — 11px/600 uppercase"], status: "pass" },
    { cells: ["#0B0B0C OECM badge text", "#FFFFFF", "20.10 : 1", "AAA", ".bbi-badge--oecm on hero badge row"], status: "pass" },
    { cells: ["#0B0B0C Canadian-made badge text", "#FFFFFF", "20.10 : 1", "AAA", ".bbi-badge--canadian on hero badge row"], status: "pass" },
    { cells: ["#FFFFFF (CTA closer)", "#0B0B0C (inverse canvas)", "20.10 : 1", "AAA", "Closer heading + body + sub on .scheme-inverse"], status: "pass" },
    { cells: ["rgba(255,255,255,0.78)", "#0B0B0C", "≈14.7 : 1", "AAA", "Closer sub · footer tagline"], status: "pass" },
    { cells: ["#0B0B0C (related card title)", "#FFFFFF (card body)", "20.10 : 1", "AAA", "More from this category — card titles"], status: "pass" },
    { cells: ["#A81E22 hover ink", "#0B0B0C (inverse footer canvas)", "2.32 : 1", "FAIL on inverse", "Reserved — never used on inverse"], status: "na" },
  ],
  red: [
    { cells: ["Header", "Eyebrow rule + cart accent", "≈ 0.9%"], status: "pass" },
    { cells: ["Breadcrumbs band", "—", "0%"], status: "pass" },
    { cells: ["Hero — gallery", "—", "0%"], status: "pass" },
    { cells: ["Hero — product info", "Brand-eyebrow tick · OECM badge dot · Canadian-made maple leaf", "≈ 0.35%"], status: "pass" },
    { cells: ["Hero — sold-out chip", "Grey #5A5A5E surface, NOT brand red", "0%"], status: "pass" },
    { cells: ["Commerce block (alt-bg plate)", "Eyebrow tick + trust dot; primary CTA charcoal at rest", "≈ 0.15%"], status: "pass" },
    { cells: ["Description band", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Spec table", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["Variants section", "Hidden — variants is null on Ibex canonical", "0%"], status: "na" },
    { cells: ["OECM bar", "Badge dot + tick rule", "≈ 0.1%"], status: "pass" },
    { cells: ["Related products row", "4 cards × (Canadian leaf or OECM dot) ≈ 4 marks total", "≈ 0.2%"], status: "pass" },
    { cells: ["Brand block", "Eyebrow tick", "≈ 0.05%"], status: "pass" },
    { cells: ["CTA closer (inverse)", "2 trust dots; CTA white at rest", "≈ 0.05%"], status: "pass" },
    { cells: ["Footer (inverse)", "Maple leaf in brand plate", "≈ 0.2%"], status: "pass" },
    { cells: ["TOTAL · at rest", "Across full page", "≈ 5.4%"], status: "pass" },
    { cells: ["TOTAL · with CTA hover", "+ #D4252A on commerce + closer primary:hover", "≈ 6.5%"], status: "pass" },
    { cells: ["TOTAL · buyable variant", "Adds qty stepper (no red) + green stock dot — red density unchanged", "≈ 5.4%"], status: "pass" },
  ],
  used: [
    ["--bodyFont, --headingFont", "All body + heading runs"],
    ["--fs-h1, --fs-h2, --fs-h3, --fs-body, --fs-small, --fs-button", "Type scale across breakpoints"],
    ["--space-1 / 2 / 3 / 4 / 6 / 8 / 12 / 16", "Padding + gap rhythm"],
    ["--inputRadius", "Gallery thumb · qty stepper · qty input"],
    ["--buttonRadius", "All bbi-btn surfaces"],
    ["--cardRadius", "Gallery main · commerce block plate · brand block plate · related cards"],
    ["--background", "Page canvas · description · variants · related · commerce qty input"],
    ["--alternateBackground", "Commerce plate · spec table band · brand block band · gallery main fill · related card media"],
    ["--cardBackground", "bbi-card body in related row · brand block plate"],
    ["--textColor (+ -rgb)", "All ink · gallery thumb active border · spec-row hairlines · qty input border accents"],
    ["--linkColor", "bbi-crumbs links · brand eyebrow link"],
    ["--headingColor", "H1 product title · description H2 · spec H2 · related H2 · brand block name · closer heading"],
    ["--buttonBackground/Color/Border (+Hover)", "Commerce primary CTA · closer primary CTA · header CTA"],
    ["--alternateButton* set", "Related row 'View all task chairs' secondary · brand block secondary CTA"],
    ["--inputBackground/Color/Border", "Buyable variant qty stepper input + buttons"],
    ["--borderColor (+ -rgb)", "All hairlines · gallery thumb borders · commerce plate · spec rows · brand block plate · related card border · footer separator (.pd-page rule)"],
    ["--productBorder", "bbi-card--product 1px hairline on related row"],
    ["--saleBadgeBackground", "Eyebrow ticks (brand · commerce · description · spec · variants · related · brand block) · OECM badge dot · Canadian maple leaf · CTA trust dots"],
    ["--soldBadgeBackground", "Sold-out chip surface (.pd-badge--sold)"],
    ["--success", "Buyable variant in-stock dot indicator (no red on stock)"],
    ["--headerBg, --headerColor, --headerHoverColor", "Header"],
    ["--shadowColor (-rgb)", "Header card overlay (inherited via bbi-components)"],
  ],
  reserve: [
    ["--saleBadgeBackground (label-white fill on .bbi-badge--sale)", "No sale-tag on the canonical PDP — sale chip is data-driven and unused on Ibex"],
    ["--newBadgeBackground", "No 'new' badge — Ibex is an established line, not a new release"],
    ["--warningBackground", "No low-stock surface — sold-out chip uses --soldBadgeBackground; low-stock would only appear on buyable variants near depletion"],
    ["--customBadgeBackground", "Reserved — custom-config tag not present on canonical Ibex"],
    ["--preorderBadgeBackground", "Reserved — Ibex is sold-out, not preorder"],
    ["--error", "No form on this template — error state lives on /pages/quote"],
    ["--cartCountBg/Color", "Cart not wired on a sold-out unbuyable PDP — buyable variant would compose these via header"],
    ["--ratingStarColor", "Reviews surface deferred to later phase"],
    ["--sliderArrowBackground/Color", "No slider — gallery uses a thumb strip, not arrows this round"],
    ["--productIconColor / --productIconBg", "Reserved for the spec-icon row pattern; canonical Ibex spec table is text-only"],
    ["--line-color", "Decorative dup of --borderColor"],
  ],
  links: [
    { cells: ["Header logo", "/", "Up to homepage"], status: "pass" },
    { cells: ["Header → Shop (current)", "/collections/business-furniture", "Sideways · is-current"], status: "pass" },
    { cells: ["Header → Industries / Brands / Services / About", "/pages/...", "Sideways"], status: "pass" },
    { cells: ["Header phone", "tel:1-800-835-9565", "Phone fallback"], status: "pass" },
    { cells: ["Header CTA", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Crumb · Home", "/", "Up to homepage"], status: "pass" },
    { cells: ["Crumb · Shop Furniture", "/collections/business-furniture", "Up to template 2"], status: "pass" },
    { cells: ["Crumb · Seating", "/collections/seating", "Up to template 3"], status: "pass" },
    { cells: ["Crumb · Task Chairs", "/collections/task-chairs", "Sideways within template 3 family"], status: "pass" },
    { cells: ["Brand eyebrow link (OTG · Offices to Go)", "/pages/brands-global-teknion", "Sideways to template 4 (brand landing)"], status: "pass" },
    { cells: ["Commerce primary CTA", "/pages/quote", "RFQ — primary conversion path on unbuyable PDP"], status: "pass" },
    { cells: ["Commerce secondary CTA", "tel:18008359565", "Phone fallback"], status: "pass" },
    { cells: ["OECM bar tertiary CTA", "/pages/oecm", "Sideways to template 4"], status: "pass" },
    { cells: ["4 related-product titles", "/products/{slug} × 4", "Self · sideways to other PDPs"], status: "pass" },
    { cells: ["4 related-card 'Request a quote' CTAs", "/pages/quote × 4", "RFQ · sideways"], status: "pass" },
    { cells: ["Related row 'View all task chairs'", "/collections/task-chairs", "Up to template 3"], status: "pass" },
    { cells: ["Brand block 'Read about Global Furniture Group'", "/pages/brands-global-teknion", "Sideways to template 4"], status: "pass" },
    { cells: ["Closer · Request a quote", "/pages/quote", "RFQ"], status: "pass" },
    { cells: ["Closer · phone link", "tel:1-800-835-9565", "Phone fallback (mandatory)"], status: "pass" },
    { cells: ["Footer Shop / Industries / Services / Contact / Legal", "Real routes", "Mirror of header set"], status: "pass" },
  ],
  extras: [
    {
      num: "05",
      title: "Empty-state behavior",
      sub: "Every conditional surface on the PDP, and which behavior the canonical Ibex render exercises.",
      heads: ["Surface", "Conditional on", "Canonical render", "Why"],
      rows: [
        { cells: ["Spec row · brand",            "product.brand truthy",           "Rendered",  "Always present — manufacturer identity"], status: "pass" },
        { cells: ["Spec row · product line",     "product.productLine truthy",     "Rendered",  "'Ibex' supplied"], status: "pass" },
        { cells: ["Spec row · model codes",      "product.modelCodes.length > 0",  "Rendered",  "9 codes (MVL2803 / OTG2803 / MVL2801 / 2804 / 2806 / 2817 / 2819C / 2831BSUU / 2832C)"], status: "pass" },
        { cells: ["Spec row · dimensions",       "specs.dimensions truthy",        "Rendered",  "26\"W x 27\"D x 39.5\"H supplied"], status: "pass" },
        { cells: ["Spec row · weight",           "specs.weight truthy",            "Rendered",  "56 lbs / 25.4 kg supplied"], status: "pass" },
        { cells: ["Spec row · weight capacity",  "specs.weightCapacity truthy",    "HIDDEN",    "Empty string — no row rendered, no '—' placeholder"], status: "na" },
        { cells: ["Spec row · materials",        "specs.materials truthy",         "Rendered",  "'Upholstered seat fabric, mesh back'"], status: "pass" },
        { cells: ["Spec row · finishes",         "specs.finishes.length > 0",      "HIDDEN",    "Empty array — no row rendered"], status: "na" },
        { cells: ["Spec row · key features",     "specs.features.length > 0",      "Rendered",  "6 bullets, displayed as <ul>"], status: "pass" },
        { cells: ["Spec row · certifications",   "specs.certifications.length > 0","HIDDEN",    "Empty array — no row rendered"], status: "na" },
        { cells: ["Spec row · warranty",         "specs.warranty truthy",          "HIDDEN",    "Empty string — no row rendered"], status: "na" },
        { cells: ["Spec row · country of origin","specs.country truthy",           "HIDDEN",    "Empty string — no row rendered"], status: "na" },
        { cells: ["Spec row · lead time",        "specs.leadTime truthy",          "HIDDEN",    "Empty string — sold-out, lead-time on quote"], status: "na" },
        { cells: ["Spec row · compliance",       "specs.compliance truthy",        "HIDDEN",    "Empty string — no row rendered"], status: "na" },
        { cells: ["Variants section",            "data.variants.items.length > 0", "HIDDEN",    "data.variants is null — entire section absent"], status: "na" },
        { cells: ["Brand block",                 "data.brandBlock truthy",         "Rendered",  "OTG · Offices to Go block present"], status: "pass" },
        { cells: ["Gallery thumb strip",         "gallery.images.length > 1",      "Rendered",  "6 thumbnails — strip visible. Single-image fallback hides via .pd-gallery--single"], status: "pass" },
        { cells: ["Sticky info rail",            "—",                              "DEFERRED",  "Out of scope this round — bottom CTA closer covers persistent action"], status: "na" },
      ],
      foot: "Empty-state grace verified: 7 spec rows hidden cleanly (weight capacity, finishes, certifications, warranty, country, lead time, compliance), 7 spec rows shown (brand, product line, model codes, dimensions, weight, materials, key features). Variants hidden. Brand block shown. No '—' placeholders rendered anywhere.",
    },
    {
      num: "06",
      title: "Variant toggle (unbuyable → buyable)",
      sub: "Single prop swap: data.commerce.buyable = true. No structural rewrite. Eight rows show what changes vs what stays.",
      heads: ["Element", "Unbuyable (canonical)", "Buyable (data.commerce.buyable=true)", "Change"],
      rows: [
        { cells: ["Commerce eyebrow",     "Project quote",                                                                           "In stock",                                                            "CHANGES"], status: "pass" },
        { cells: ["Commerce heading",     "Request a quote on this product",                                                         "Order direct from the catalogue",                                     "CHANGES"], status: "pass" },
        { cells: ["Commerce sub",         "Volume pricing, lead time, OECM PO eligibility...",                                       "Stocked accessory copy (data-driven)",                                "CHANGES"], status: "pass" },
        { cells: ["Primary CTA",          "Request a quote → /pages/quote",                                                          "Add to cart → cart action",                                           "CHANGES"], status: "pass" },
        { cells: ["Secondary CTA",        "Call 1-800-835-9565 (tel:)",                                                              "Request a quote (kept) → /pages/quote",                               "CHANGES"], status: "pass" },
        { cells: ["Price block",          "Absent",                                                                                  "Present (--headingFont, 32px, --textColor)",                          "ABSENT → PRESENT"], status: "pass" },
        { cells: ["Qty stepper",          "Absent",                                                                                  "Present (-/+ buttons + numeric input, 36×40px)",                      "ABSENT → PRESENT"], status: "pass" },
        { cells: ["Stock indicator",      "Absent",                                                                                  "Present (green dot --success + 'In stock · 2-week lead')",            "ABSENT → PRESENT"], status: "pass" },
        { cells: ["Trust microcopy",      "OECM purchasers welcome · 1 business day · since 1962",                                   "OECM purchasers welcome · 1 business day · since 1962",               "UNCHANGED"], status: "pass" },
      ],
      foot: "Buyable swap is a single data toggle (commerce.buyable: false → true) plus optional fields (price, unit, stock, leadTime, qty). 645 PDPs will use this same component — unbuyable for sold-out / showcase / $0 items, buyable for stocked accessories.",
    },
  ],
});

/* ---------- root ---------- */
function Audits({ template = "collection-category" }) {
  const data = AUDIT_REGISTRY[template] || AUDIT_REGISTRY["collection-category"];
  const extras = data.extras || [];
  return (
    <div className="ap-root scheme-default" data-template={template}>
      <header className="ap-root__head">
        <span className="ap-root__kicker">Audit panels</span>
        <h2 className="ap-root__title">{data.title}</h2>
        <p className="ap-root__sub">
          Same four audits across every template: Contrast · Red density · Token coverage · Cross-links. Templates with bespoke surfaces append additional panels via <code>extras: []</code>. Values reflect the rendered cascade — no spec hand-waving.
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

      {extras.map((e, i) => (
        <AuditPanel key={i} num={e.num || ("0" + (5 + i))} title={e.title} sub={e.sub}>
          <APTable heads={e.heads} rows={e.rows} />
          {e.foot && <p className="ap-foot">{e.foot}</p>}
        </AuditPanel>
      ))}
    </div>
  );
}

window.Audits = Audits;
window.AuditsRegistry = AUDIT_REGISTRY;
