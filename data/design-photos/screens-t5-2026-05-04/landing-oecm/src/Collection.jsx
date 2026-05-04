// Collection.jsx — /collections/seating
// Template 3 — single-category collection (the catalogue page).
// Composes only Phase-2 patterns + Homepage-shared atoms (HeaderDesktop,
// HeaderMobile, Footer, MapleLeaf, Placeholder).
// New patterns are scoped under .cn-page (collection.css).

const _HeaderDesktop = window.HeaderDesktop;
const _HeaderMobile  = window.HeaderMobile;
const _Footer        = window.Footer;
const _MapleLeaf     = window.MapleLeaf;
const _Placeholder   = window.Placeholder;

/* ---------- breadcrumbs ----------------------------------------------- */
function CnBreadcrumbs() {
  return (
    <div className="cn-crumb-band">
      <div className="cn-crumb-band__inner">
        <ol className="bbi-crumbs" aria-label="Breadcrumb">
          <li><a href="/">Home</a></li>
          <li><a href="/collections/business-furniture">Shop</a></li>
          <li>Seating</li>
        </ol>
      </div>
    </div>
  );
}

/* ---------- intro band ------------------------------------------------ */
function CnIntro({ mobile = false }) {
  return (
    <section className="cn-intro" aria-labelledby="cn-intro-title">
      <div className="cn-intro__inner">
        <div className="cn-intro__grid">
          <div className="cn-intro__copy">
            <p className="cn-intro__eyebrow">Collection · Seating</p>
            <h1 id="cn-intro-title" className="cn-intro__title">
              Task, stacking, lounge, executive — every seat we sell.
            </h1>
            <p className="cn-intro__deck">
              120 models from 18 brands. Steelcase, Allsteel, ergoCentric, Global, Humanscale, AMQ — plus 12 more.
            </p>
            <p className="cn-intro__deck" style={{ fontSize: 16, color: 'rgba(var(--textColor-rgb), 0.7)' }}>
              Order direct from the catalogue, or have us spec a fit-out across all 120. Same Ontario team either way.
            </p>
            <div className="cn-intro__meta">
              <div className="cn-intro__metaitem">
                <span className="cn-intro__metakey">Models</span>
                <span className="cn-intro__metaval">120</span>
              </div>
              <div className="cn-intro__metaitem">
                <span className="cn-intro__metakey">Brands</span>
                <span className="cn-intro__metaval">18</span>
              </div>
              <div className="cn-intro__metaitem">
                <span className="cn-intro__metakey">Canadian-made</span>
                <span className="cn-intro__metaval">42</span>
              </div>
              <div className="cn-intro__metaitem">
                <span className="cn-intro__metakey">In stock</span>
                <span className="cn-intro__metaval">86</span>
              </div>
              <div className="cn-intro__metaitem">
                <span className="cn-intro__metakey">Lead time</span>
                <span className="cn-intro__metaval">2–6 weeks</span>
              </div>
            </div>
          </div>
          <div className="cn-intro__media" aria-hidden="true">
            <_Placeholder label="Seating hero · task chair lineup · 4:5" ratio="4 / 5" />
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------- toolbar (filter bar + sub-category chip row + state strip) ---------- */
const CN_FACETS = [
  { id: "subcat",   label: "Sub-category", count: 6 },
  { id: "brand",    label: "Brand",        count: 18 },
  { id: "height",   label: "Height",       count: 4 },
  { id: "fabric",   label: "Fabric tier",  count: 5 },
  { id: "warranty", label: "Warranty",     count: 3 },
];

const CN_SUBCATS = [
  { id: "all",       label: "All",        count: 120 },
  { id: "task",      label: "Task",       count: 48 },
  { id: "stacking",  label: "Stacking",   count: 24 },
  { id: "lounge",    label: "Lounge",     count: 18 },
  { id: "executive", label: "Executive",  count: 16 },
  { id: "guest",     label: "Guest",      count: 9 },
  { id: "stools",    label: "Stools",     count: 5 },
];

function CnToolbar({ mobile = false }) {
  return (
    <div className="cn-toolbar">
      <div className="cn-toolbar__inner">
        {/* facet pill row */}
        <div className="cn-toolbar__row">
          <span className="cn-toolbar__label">Filter</span>
          {CN_FACETS.map((f) => (
            <button
              key={f.id}
              className={"cn-facet" + (f.id === "subcat" ? " cn-facet--open" : "")}
              aria-expanded={f.id === "subcat" ? "true" : "false"}
              aria-haspopup="true"
              type="button"
            >
              <span>{f.label}</span>
              <span className="cn-facet__count">{f.count}</span>
              <span className="cn-facet__caret" aria-hidden="true">▼</span>
            </button>
          ))}
          <button className="cn-facet cn-facet--toggle" type="button">
            <_MapleLeaf size={12} />
            <span>Canadian-made</span>
          </button>
        </div>

        {/* sub-category chip row — visible at rest under the bar */}
        <div className="cn-subchips" role="tablist" aria-label="Sub-category">
          <span className="cn-subchips__lead">Sub-category</span>
          {CN_SUBCATS.map((s) => (
            <button
              key={s.id}
              role="tab"
              aria-selected={s.id === "task" ? "true" : "false"}
              className={"cn-chip" + (s.id === "task" ? " cn-chip--on" : "") + (s.id === "all" ? " cn-chip--all" : "")}
              type="button"
            >
              <span>{s.label}</span>
              <span className="cn-chip__count">{s.count}</span>
            </button>
          ))}
        </div>

        {/* result state — count + sort, attached below */}
        <div className="cn-state">
          <p className="cn-state__count">
            Showing <b>1–24</b> of <b>48</b> task chairs
            <span style={{ color: 'rgba(var(--textColor-rgb), 0.45)', marginLeft: 8 }}>· filtered from 120</span>
          </p>
          <div className="cn-state__sort">
            <label htmlFor="cn-sort">Sort</label>
            <button id="cn-sort" className="cn-state__sort-trigger" type="button">
              <span>Featured</span>
              <span className="caret" aria-hidden="true">▾</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ---------- product grid ---------------------------------------------- */
// 24 task chairs — page 1 of 5. Brand names come from the round-3 brand index.
// Badge is data-driven: canadian (maple leaf), oem (transparent), oecm (eyebrow ring).
// Price is data-driven: list price OR "Quote required" italic.
const CN_PRODUCTS = [
  { brand: "ergoCentric",     model: "tCentric Hybrid",          subtitle: "Multi-tilt task chair",       code: "TCH-3000",   warranty: "Lifetime", price: "$899",   canadian: true,  oecm: false },
  { brand: "Steelcase",       model: "Series 1",                  subtitle: "Task chair, 4D arms",        code: "S1-435",     warranty: "12 yr",    price: "$614",   canadian: false, oecm: true  },
  { brand: "Allsteel",        model: "Acuity",                    subtitle: "Mesh-back task chair",       code: "ACT-12",     warranty: "12 yr",    price: "$789",   canadian: false, oecm: true  },
  { brand: "Humanscale",      model: "Freedom",                   subtitle: "Self-adjusting task chair",  code: "FRD-H",      warranty: "15 yr",    price: "$1,420", canadian: false, oecm: false },
  { brand: "Global",          model: "G20",                       subtitle: "Synchro task with arms",     code: "G20-3210",   warranty: "10 yr",    price: "$485",   canadian: true,  oecm: true  },
  { brand: "ergoCentric",     model: "geoCentric Mesh",           subtitle: "Mesh ergonomic task",        code: "GEO-M",      warranty: "Lifetime", price: "$725",   canadian: true,  oecm: true  },

  { brand: "AMQ Solutions",   model: "Activ Task",                subtitle: "Sit-stand stool task",       code: "ACT-S",      warranty: "10 yr",    price: "$540",   canadian: false, oecm: false },
  { brand: "Knoll",           model: "ReGeneration",              subtitle: "Polymer-back task",          code: "RGN-2",      warranty: "12 yr",    price: "$668",   canadian: false, oecm: false },
  { brand: "Herman Miller",   model: "Aeron Remastered",          subtitle: "Pellicle suspension chair",  code: "AER-B",      warranty: "12 yr",    price: "$1,795", canadian: false, oecm: false },
  { brand: "Steelcase",       model: "Gesture",                   subtitle: "360° arm task chair",        code: "GES-3HC",    warranty: "12 yr",    price: "$1,219", canadian: false, oecm: true  },
  { brand: "Global",          model: "Truform",                   subtitle: "High-back conference task",  code: "TRU-HB",     warranty: "10 yr",    price: "$612",   canadian: true,  oecm: true  },
  { brand: "ergoCentric",     model: "airCentric 2.0",            subtitle: "Mesh task chair",            code: "AC2-K",      warranty: "Lifetime", price: "$695",   canadian: true,  oecm: false },

  { brand: "Allsteel",        model: "Mimeo",                     subtitle: "24/7 task chair",            code: "MIM-A",      warranty: "12 yr",    price: "$1,049", canadian: false, oecm: false },
  { brand: "Humanscale",      model: "Diffrient Smart",           subtitle: "Self-adjusting mesh",        code: "DFS-M",      warranty: "15 yr",    price: "$899",   canadian: false, oecm: false },
  { brand: "Steelcase",       model: "Leap V2",                   subtitle: "Live-back task chair",      code: "LV2-46",     warranty: "12 yr",    price: "$1,089", canadian: false, oecm: true  },
  { brand: "Global",          model: "Granada",                   subtitle: "Executive high-back",        code: "GRN-EX",     warranty: "10 yr",    price: "Quote",  canadian: true,  oecm: true  },
  { brand: "AMQ Solutions",   model: "Ditto",                     subtitle: "Stacking guest chair",       code: "DIT-A",      warranty: "10 yr",    price: "$348",   canadian: false, oecm: false },
  { brand: "ergoCentric",     model: "saddleCentric",             subtitle: "Saddle-seat task stool",     code: "SAD-1",      warranty: "Lifetime", price: "$795",   canadian: true,  oecm: false },

  { brand: "Knoll",           model: "Generation",                subtitle: "Flex-back task chair",       code: "GEN-K",      warranty: "12 yr",    price: "$925",   canadian: false, oecm: false },
  { brand: "Allsteel",        model: "Inspire",                   subtitle: "Petite-frame task",          code: "INS-P",      warranty: "12 yr",    price: "$649",   canadian: false, oecm: true  },
  { brand: "Steelcase",       model: "Amia",                      subtitle: "LiveLumbar task chair",      code: "AMA-3",      warranty: "12 yr",    price: "$806",   canadian: false, oecm: true  },
  { brand: "Global",          model: "Concorde",                  subtitle: "Mid-back task chair",        code: "CON-MB",     warranty: "10 yr",    price: "$425",   canadian: true,  oecm: true  },
  { brand: "Humanscale",      model: "Liberty",                   subtitle: "Tri-panel mesh",             code: "LBT-O",      warranty: "15 yr",    price: "$1,195", canadian: false, oecm: false },
  { brand: "ergoCentric",     model: "youCentric",                subtitle: "24/7 multi-shift task",      code: "YOU-2",      warranty: "Lifetime", price: "Quote",  canadian: true,  oecm: false },
];

function CnProductCard({ p }) {
  const isQuote = p.price === "Quote";
  return (
    <article className="bbi-card bbi-card--product">
      <div className="bbi-card__media">
        <_Placeholder label={p.brand + " " + p.model + " · 16:9"} />
        {p.canadian && (
          <span className="bbi-badge bbi-badge--canadian">
            <_MapleLeaf size={12} />
            Canadian-made
          </span>
        )}
        {!p.canadian && p.oecm && (
          <span className="bbi-badge bbi-badge--oecm">
            <span className="dot" />
            OECM
          </span>
        )}
      </div>
      <div className="bbi-card__body">
        <p className="bbi-card__brand">{p.brand}</p>
        <h3 className="bbi-card__title"><a href="#">{p.model}</a></h3>
        <p className="cn-card__meta">
          <span>{p.subtitle}</span>
          <span className="sep" aria-hidden="true" />
          <span>{p.code}</span>
          <span className="sep" aria-hidden="true" />
          <span>{p.warranty}</span>
        </p>
        <div className="cn-card__row">
          <div className="cn-card__price">
            <span className="cn-card__price-label">{isQuote ? "Pricing" : "From"}</span>
            <span className={"cn-card__price-val" + (isQuote ? " cn-card__price-val--quote" : "")}>
              {isQuote ? "Quote required" : p.price}
            </span>
          </div>
          <div className="cn-card__cta-pair">
            <a className="bbi-card__cta" href="#">
              {isQuote ? "Request a quote" : "Add to cart"} <span className="arrow">→</span>
            </a>
            <span className="cn-card__cta-secondary">or quote &nbsp;·&nbsp; spec sheet</span>
          </div>
        </div>
      </div>
    </article>
  );
}

function CnGrid({ mobile = false }) {
  return (
    <section className="cn-grid-section" aria-labelledby="cn-grid-title">
      <div className="cn-grid-section__inner">
        <h2 id="cn-grid-title" className="bbi-visually-hidden" style={{
          position: 'absolute', width: 1, height: 1, padding: 0, margin: -1, overflow: 'hidden',
          clip: 'rect(0,0,0,0)', whiteSpace: 'nowrap', border: 0,
        }}>Task chairs</h2>
        <div className="cn-grid">
          {CN_PRODUCTS.map((p) => <CnProductCard key={p.code} p={p} />)}
        </div>
        <CnPager mobile={mobile} />
      </div>
    </section>
  );
}

function CnPager({ mobile = false }) {
  return (
    <nav className="cn-pager" aria-label="Pagination">
      <a className="cn-pager__edge cn-pager__edge--disabled" aria-disabled="true">
        <span aria-hidden="true">←</span>
        <span>Prev</span>
      </a>
      <div className="cn-pager__nums">
        <a className="cn-pager__num cn-pager__num--current" aria-current="page" href="#">1</a>
        <a className="cn-pager__num" href="?page=2">2</a>
        <a className="cn-pager__num" href="?page=3">3</a>
        <span className="cn-pager__num cn-pager__num--ellipsis">…</span>
        <a className="cn-pager__num" href="?page=5">5</a>
      </div>
      <a className="cn-pager__edge" href="?page=2">
        <span>Next</span>
        <span aria-hidden="true">→</span>
      </a>
      <span className="cn-pager__count">Page 1 of 5 · 48 task chairs</span>
    </nav>
  );
}

/* ---------- brand strip ----------------------------------------------- */
const CN_BRAND_STRIP = [
  { name: "ergoCentric", count: 14, canadian: true },
  { name: "Steelcase",   count: 12, canadian: false },
  { name: "Global",      count: 11, canadian: true },
  { name: "Allsteel",    count: 9,  canadian: false },
  { name: "Humanscale",  count: 8,  canadian: false },
  { name: "Knoll",       count: 7,  canadian: false },
  { name: "AMQ",         count: 6,  canadian: false },
  { name: "Herman Miller", count: 6, canadian: false },
  { name: "Teknion",     count: 5,  canadian: true },
  { name: "Haworth",     count: 5,  canadian: false },
  { name: "OFS",         count: 4,  canadian: false },
  { name: "Sitonit",     count: 3,  canadian: false },
];

function CnBrandStrip({ mobile = false }) {
  return (
    <section className="cn-brandstrip" aria-labelledby="cn-brand-title">
      <div className="cn-brandstrip__inner">
        <div className="cn-brandstrip__head">
          <h2 id="cn-brand-title" className="cn-brandstrip__title">12 brands carry seating with us.</h2>
          <p className="cn-brandstrip__sub">Click any brand to see its full range across all categories.</p>
        </div>
        <div className="cn-brandstrip__grid">
          {CN_BRAND_STRIP.map((b) => (
            <a key={b.name} className="cn-brand-plate" href={"/pages/brands/" + b.name.toLowerCase().replace(/\s+/g, "-")}>
              {b.canadian && <_MapleLeaf size={12} />}
              {b.canadian && <span className="cn-brand-plate__leaf"><_MapleLeaf size={12} /></span>}
              <span className="cn-brand-plate__name">{b.name}</span>
              <span className="cn-brand-plate__count">{b.count} models</span>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- OECM bar (mirrors locked .cc-oecm shape) ------------------ */
function CnOECM() {
  return (
    <section className="cn-oecm" aria-label="OECM trust signal">
      <div className="cn-oecm__inner">
        <div className="cn-oecm__lead">
          <span className="bbi-badge bbi-badge--oecm">
            <span className="dot" />
            OECM vendor of record
          </span>
          <p className="cn-oecm__copy">
            32 of these 120 seating models are pre-qualified through OECM. Use existing OECM pricing without re-tendering — Brant Business Interiors is an approved supplier.
          </p>
        </div>
        <div className="cn-oecm__meta">
          <a className="bbi-btn bbi-btn--tertiary" href="/pages/oecm">
            <span className="label">See OECM-eligible seating</span>
            <span className="arrow">→</span>
          </a>
        </div>
      </div>
    </section>
  );
}

/* ---------- CTA closer (reuses .bbi-cta-section verbatim) ------------- */
function CnCloser() {
  return (
    <section className="bbi-cta-section scheme-inverse">
      <div className="bbi-cta-section__inner">
        <div>
          <p className="bbi-cta-section__eyebrow">Two ways to buy</p>
          <h2 className="bbi-cta-section__heading">
            Order one chair, or have us spec the whole floor.
          </h2>
          <p className="bbi-cta-section__sub">
            120 seating models, 18 brands, one Ontario team. Order direct from the catalogue, or send us a floor plan and we'll quote the full fit-out.
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

/* ---------- page composition ------------------------------------------ */
function Collection({ mobile = false }) {
  return (
    <div className={"scheme-default cn-page" + (mobile ? " cn-page--mobile" : "")}>
      {mobile ? <_HeaderMobile /> : <_HeaderDesktop current="shop" />}
      <CnBreadcrumbs />
      <CnIntro mobile={mobile} />
      <CnToolbar mobile={mobile} />
      <CnGrid mobile={mobile} />
      <CnBrandStrip mobile={mobile} />
      <CnOECM />
      <CnCloser />
      <_Footer mobile={mobile} />
    </div>
  );
}

window.Collection = Collection;
