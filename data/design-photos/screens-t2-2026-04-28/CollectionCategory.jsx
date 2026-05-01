// CollectionCategory.jsx — /collections/business-furniture
// Template 2 — the catalogue map (shop hub, not a single collection).
// Composes only Phase-2 patterns + Homepage-shared atoms.
// New patterns are template-scoped (cc-* in collection-category.css).

const { useMemo: __ccUseMemo } = React;

/* ---- atom imports from Homepage.jsx -------------------------------- */
const _MapleLeaf = window.MapleLeaf;
const _Placeholder = window.Placeholder;
const _HeaderDesktop = window.HeaderDesktop;
const _HeaderMobile = window.HeaderMobile;
const _Footer = window.Footer;

/* ---- breadcrumbs band --------------------------------------------- */
function CCBreadcrumbs({ mobile = false }) {
  return (
    <div className="cc-crumb-band">
      <div className="cc-crumb-band__inner">
        <ol className="bbi-crumbs" aria-label="Breadcrumb">
          <li><a href="/">Home</a></li>
          <li>Shop</li>
        </ol>
      </div>
    </div>
  );
}

/* ---- intro band ---------------------------------------------------- */
function CCIntro({ mobile = false }) {
  return (
    <section className="cc-intro" aria-labelledby="cc-intro-title">
      <div className="cc-intro__grid">
        <div className="cc-intro__copy">
          <p className="cc-intro__eyebrow">Shop the catalogue</p>
          <h1 id="cc-intro-title" className="cc-intro__title">
            Business furniture, every category.
          </h1>
          <p className="cc-intro__deck">
            9 categories from seating to quiet rooms — Steelcase, Allsteel, ergoCentric, Global, AMQ, and 30+ more brands.
          </p>
          <p className="cc-intro__sub">
            Order direct from any collection, or hand us the floor plan and we'll quote the full fit-out.
          </p>
        </div>
        <div className="cc-intro__plate" aria-label="Catalogue at a glance">
          <div className="cc-intro__row">
            <span className="lbl">Categories</span>
            <span className="val">9</span>
          </div>
          <div className="cc-intro__row">
            <span className="lbl">Brands</span>
            <span className="val">30<span className="unit">+</span></span>
          </div>
          <div className="cc-intro__row">
            <span className="lbl">Models in catalogue</span>
            <span className="val">1,200<span className="unit">+</span></span>
          </div>
          <div className="cc-intro__row">
            <span className="lbl">Quote response</span>
            <span className="val">1<span className="unit">business day</span></span>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---- 9-category grid ---------------------------------------------- */
const CC_CATEGORIES = [
  { title: "Seating", slug: "seating", count: "120+ models", desc: "Task · stacking · lounge" },
  { title: "Desks & Workstations", slug: "desks-workstations", count: "80+ models", desc: "Sit-stand · benching · executive" },
  { title: "Storage & Filing", slug: "storage-filing", count: "60+ models", desc: "Lateral · pedestal · lockers" },
  { title: "Tables", slug: "tables", count: "45+ models", desc: "Conference · café · folding" },
  { title: "Boardroom", slug: "boardroom", count: "28 systems", desc: "Tables · credenzas · AV" },
  { title: "Ergonomic Products", slug: "ergonomic-products", count: "70+ models", desc: "Monitor arms · keyboards · footrests" },
  { title: "Panels & Dividers", slug: "panels-dividers", count: "40+ systems", desc: "Acoustic · freestanding · desk-mount" },
  { title: "Accessories", slug: "accessories", count: "200+ items", desc: "Power · lighting · whiteboards" },
  { title: "Quiet Spaces", slug: "quiet-spaces", count: "12 pods", desc: "Phone booths · meeting pods" },
];

function CCCategoryGrid({ mobile = false }) {
  return (
    <section className="cc-cat-section" aria-labelledby="cc-cat-title">
      <div className="bbi-container">
        <div className="bbi-section-head">
          <div>
            <p id="cc-cat-title" className="bbi-section-head__eyebrow">9 categories</p>
            <h2 className="bbi-section-head__title">From a single chair to a quiet room.</h2>
          </div>
          <p className="bbi-section-head__sub">
            Every tile is a real catalogue page. Click in to filter by brand, height, fabric tier, or warranty.
          </p>
        </div>
        <div className={"cc-cat-grid" + (mobile ? " cc-cat-grid--mobile" : "")}>
          {CC_CATEGORIES.map((cat, i) => (
            <a key={cat.slug} className="bbi-card bbi-card--collection" href={"/collections/" + cat.slug}>
              <span className="bbi-card__num">0{(i + 1).toString().padStart(2, "0").slice(-2)}</span>
              <div className="bbi-card__media">
                <_Placeholder label={cat.title + " · 5:4"} />
                <div className="bbi-card__overlay">
                  <h3>{cat.title}</h3>
                  <span className="count">{cat.count}</span>
                  <span className="desc">{cat.desc}</span>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---- industry shortcut row ----------------------------------------- */
const CC_INDUSTRIES = [
  { title: "Office & Corporate", slug: "office-corporate", note: "Workstations · private offices · café" },
  { title: "Healthcare", slug: "healthcare", note: "Exam · waiting · acute care" },
  { title: "Education", slug: "education", note: "K-12 · post-secondary · libraries" },
  { title: "Government", slug: "government", note: "Municipal · provincial · OECM" },
  { title: "Industrial", slug: "industrial", note: "24/7 chairs · ESD · warehousing" },
];

function CCIndustryShortcut({ mobile = false }) {
  return (
    <section className="cc-industry-section" aria-labelledby="cc-ind-title">
      <div className="bbi-container">
        <div className="bbi-section-head">
          <div>
            <p id="cc-ind-title" className="bbi-section-head__eyebrow">Skip the catalogue</p>
            <h2 className="bbi-section-head__title">Buying for a sector? Start there instead.</h2>
          </div>
          <p className="bbi-section-head__sub">
            Sector pages route to the brands, warranty terms, and OECM agreements specific to that buyer — not the full catalogue.
          </p>
        </div>
        <div className={"cc-industry-grid" + (mobile ? " cc-industry-grid--mobile" : "")}>
          {CC_INDUSTRIES.map((s, i) => (
            <a key={s.slug} className="cc-industry" href={"/pages/industries/" + s.slug}>
              <span className="cc-industry__num">0{i + 1}</span>
              <h3 className="cc-industry__title">{s.title}</h3>
              <p className="cc-industry__note">{s.note}</p>
              <span className="cc-industry__arrow">
                Sector page <span className="arrow">→</span>
              </span>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---- brand index (composition (c) — tiered text-list) -------------- */
const CC_BRAND_TIERS = [
  {
    num: "01",
    name: "Premium",
    count: "12 brands · authorized dealer",
    rows: [
      { name: "Steelcase", cats: "Seating · Desks · Storage · Boardroom", status: "Authorized dealer", auth: true },
      { name: "Allsteel", cats: "Seating · Workstations · Storage", status: "Authorized dealer", auth: true },
      { name: "Knoll", cats: "Seating · Tables · Quiet spaces", status: "Authorized dealer", auth: true },
      { name: "Herman Miller", cats: "Seating · Workstations", status: "Authorized dealer", auth: true },
      { name: "Haworth", cats: "Workstations · Panels · Storage", status: "Authorized dealer", auth: true },
      { name: "Teknion", cats: "Workstations · Boardroom · Quiet spaces", status: "Authorized dealer", auth: true, canadian: true },
      { name: "Humanscale", cats: "Ergonomic · Monitor arms · Lighting", status: "Authorized dealer", auth: true },
    ],
  },
  {
    num: "02",
    name: "Canadian-made",
    count: "8 brands · domestic supply chain",
    rows: [
      { name: "ergoCentric", cats: "Seating · Ergonomic · Industrial", status: "Authorized · Ontario territory", auth: true, canadian: true },
      { name: "Global", cats: "Seating · Desks · Storage · Tables", status: "Authorized dealer", auth: true, canadian: true },
      { name: "Artopex", cats: "Workstations · Boardroom · Storage", status: "Authorized dealer", auth: true, canadian: true },
      { name: "Inscape", cats: "Workstations · Storage · Walls", status: "Authorized dealer", auth: true, canadian: true },
      { name: "Groupe Lacasse", cats: "Desks · Boardroom · Reception", status: "Authorized dealer", auth: true, canadian: true },
      { name: "Nightingale", cats: "Seating · Ergonomic", status: "Stocked · quote available", auth: false, canadian: true },
    ],
  },
  {
    num: "03",
    name: "Specialist",
    count: "10+ brands · category leaders",
    rows: [
      { name: "AMQ Solutions", cats: "Sit-stand · Benching · Power", status: "Authorized dealer", auth: true },
      { name: "Framery", cats: "Quiet spaces · Phone booths", status: "Authorized dealer", auth: true },
      { name: "Loftwall", cats: "Panels · Acoustic dividers", status: "Stocked · quote available", auth: false },
      { name: "Workrite", cats: "Sit-stand desks · Keyboard trays", status: "Stocked · quote available", auth: false },
      { name: "ESI", cats: "Monitor arms · Ergonomic", status: "Stocked · quote available", auth: false },
      { name: "Safco", cats: "Storage · Mailroom · Mobile", status: "Stocked · quote available", auth: false },
    ],
  },
];

function CCBrandIndex({ mobile = false }) {
  return (
    <section className="cc-brand-index" aria-labelledby="cc-brand-title">
      <div className="cc-brand-index__head">
        <div>
          <p className="bbi-section-head__eyebrow">The shelf behind the shelf</p>
          <h2 id="cc-brand-title" className="bbi-section-head__title" style={{ maxWidth: "26ch" }}>
            30+ brands. Three tiers. One Ontario partner.
          </h2>
        </div>
        <p className="bbi-section-head__sub" style={{ maxWidth: "44ch" }}>
          We're an authorized dealer for the premium and Canadian-made tiers — meaning factory pricing, factory warranty, and BBI files the claim. Specialist brands we stock and quote.
        </p>
      </div>

      <div className="cc-brand-index__inner">
        {CC_BRAND_TIERS.map((tier) => (
          <div key={tier.num} className="cc-brand-tier">
            <div className="cc-brand-tier__meta">
              <span className="cc-brand-tier__num">{tier.num}</span>
              <h3 className="cc-brand-tier__name">{tier.name}</h3>
              <span className="cc-brand-tier__count">{tier.count}</span>
            </div>
            <div className="cc-brand-tier__rows">
              {tier.rows.map((row) => (
                <a
                  key={row.name}
                  href={"/pages/brands/" + row.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}
                  className="cc-brand-row"
                >
                  <span className="cc-brand-row__name">
                    {row.canadian && <_MapleLeaf size={12} />}
                    {row.name}
                  </span>
                  <span className="cc-brand-row__cats">{row.cats}</span>
                  <span className={"cc-brand-row__status" + (row.auth ? "" : " cc-brand-row__status--stocked")}>
                    <span className="dot" />
                    {row.status}
                  </span>
                </a>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="cc-brand-index__foot">
        <span>Don't see a brand? We work with 30+ manufacturers — ask us.</span>
        <a className="bbi-btn bbi-btn--secondary" href="/pages/brands">Full brand directory</a>
      </div>
    </section>
  );
}

/* ---- OECM bar (mirrors locked homepage hp-oecm) -------------------- */
function CCOECM() {
  return (
    <section className="cc-oecm" aria-label="OECM trust signal">
      <div className="cc-oecm__inner">
        <div className="cc-oecm__lead">
          <span className="bbi-badge bbi-badge--oecm">
            <span className="dot" />
            OECM vendor of record
          </span>
          <p className="cc-oecm__copy">
            Brant Business Interiors is an approved OECM supplier — pre-qualified procurement for Ontario's broader public sector. Use existing OECM agreements without re-tendering.
          </p>
        </div>
        <div className="cc-oecm__meta">
          <a className="bbi-btn bbi-btn--tertiary" href="/pages/oecm">
            <span className="label">Read the OECM details</span>
            <span className="arrow">→</span>
          </a>
        </div>
      </div>
    </section>
  );
}

/* ---- CTA closer (reuses .bbi-cta-section verbatim) ----------------- */
function CCCloser() {
  return (
    <section className="bbi-cta-section scheme-inverse">
      <div className="bbi-cta-section__inner">
        <div>
          <p className="bbi-cta-section__eyebrow">Two ways to buy</p>
          <h2 className="bbi-cta-section__heading">
            Order what you need today, or hand us the floor plan.
          </h2>
          <p className="bbi-cta-section__sub">
            Same Ontario team, same warehouse, same brands either way. We respond within 1 business day on every quote — no matter the size.
          </p>
        </div>
        <div className="bbi-cta-section__actions">
          <a className="bbi-btn bbi-btn--primary bbi-btn--lg" href="/pages/quote">
            Request a quote <span className="arrow">→</span>
          </a>
          <div className="bbi-cta-section__trust">
            <span className="dot" />
            <span><b>1 business day response</b> on every quote — no minimums, no accounts.</span>
          </div>
          <div className="bbi-cta-section__trust">
            <span className="dot" />
            <span>Or call <a href="tel:18008359565">1-800-835-9565</a> · Mon–Fri 8–5 ET</span>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---- page composition ---------------------------------------------- */
function CollectionCategory({ mobile = false }) {
  return (
    <div className={"scheme-default cc-page" + (mobile ? " cc-page--mobile" : "")}>
      {mobile ? <_HeaderMobile /> : <_HeaderDesktop current="shop" />}
      <CCBreadcrumbs mobile={mobile} />
      <CCIntro mobile={mobile} />
      <CCCategoryGrid mobile={mobile} />
      <CCIndustryShortcut mobile={mobile} />
      <CCBrandIndex mobile={mobile} />
      <CCOECM />
      <CCCloser />
      <_Footer mobile={mobile} />
    </div>
  );
}

window.CollectionCategory = CollectionCategory;
