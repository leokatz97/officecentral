// Collection.jsx — /collections/seating
// Template 3 — a single collection page (canonical: Seating).
// Composes only Phase-2 patterns (.bbi-btn, .bbi-badge, .bbi-card--product,
// .bbi-section, .bbi-section-head, .bbi-cta-section, .bbi-crumbs, header,
// footer) + the cn-* template-scoped classes in collection.css.
// Generalizes per the 9-category list — swap the data block at top, the
// page reflows for any category (Desks, Storage, Tables, etc.).

/* ---- atom imports from Homepage.jsx -------------------------------- */
const _MapleLeaf = window.MapleLeaf;
const _Placeholder = window.Placeholder;
const _HeaderDesktop = window.HeaderDesktop;
const _HeaderMobile = window.HeaderMobile;
const _Footer = window.Footer;

/* ============================================================
   Data — Seating as the canonical example. The shape generalizes
   to any of the 9 categories; only the values change.
   ============================================================ */
const CN_CATEGORY = {
  slug: "seating",
  title: "Seating",
  count: "120+ models",
  brandCount: "12 brands",
  warrantyHeadline: "12-year warranty on Canadian-made tier",
  standfirst:
    "Task chairs, stacking, lounge, and 24/7 industrial — 120+ models across 12 brands. Every Canadian-made tier carries a 12-year warranty; we file the claim.",
  subcats: [
    { slug: "task",       label: "Task",       count: 48 },
    { slug: "stacking",   label: "Stacking",   count: 22 },
    { slug: "lounge",     label: "Lounge",     count: 19 },
    { slug: "conference", label: "Conference", count: 17 },
    { slug: "executive",  label: "Executive",  count: 9 },
    { slug: "247",        label: "24/7 Industrial", count: 5 },
  ],
  brands: [
    { name: "ergoCentric",   tier: "Canadian-made", canadian: true,  authorized: true },
    { name: "Global",        tier: "Canadian-made", canadian: true,  authorized: true },
    { name: "Steelcase",     tier: "Premium",       canadian: false, authorized: true },
    { name: "Allsteel",      tier: "Premium",       canadian: false, authorized: true },
    { name: "Knoll",         tier: "Premium",       canadian: false, authorized: true },
    { name: "Herman Miller", tier: "Premium",       canadian: false, authorized: true },
    { name: "Nightingale",   tier: "Canadian-made", canadian: true,  authorized: false },
    { name: "Humanscale",    tier: "Specialist",    canadian: false, authorized: true },
  ],
};

/* Product shape: title, brand, sub-category, height range, fabric tier,
   warranty, badges, buyable flag (data-driven CTA per the brief). */
const CN_PRODUCTS = [
  { id: "tcent-hybrid", brand: "ergoCentric", title: "tCentric Hybrid task chair", subcat: "Task",
    badges: ["canadian", "auth"], canadian: true, buyable: true,
    spec: "Mesh back · sync-tilt · 12-yr warranty", price: "from $1,189" },
  { id: "geocentric",   brand: "ergoCentric", title: "geoCentric heavy-duty task", subcat: "24/7 Industrial",
    badges: ["canadian", "auth", "247"], canadian: true, buyable: false,
    spec: "24/7 use · 350 lb rated · custom fabric", price: "Quote · made-to-order" },
  { id: "leap-v2",      brand: "Steelcase",   title: "Leap V2 task chair",         subcat: "Task",
    badges: ["auth"], canadian: false, buyable: true,
    spec: "LiveBack · adjustable arms · 12-yr warranty", price: "from $1,449" },
  { id: "amia",         brand: "Steelcase",   title: "Amia conference chair",      subcat: "Conference",
    badges: ["auth"], canadian: false, buyable: true,
    spec: "Live Lumbar · 4-way arms · contract grade", price: "from $1,089" },
  { id: "gesture",      brand: "Steelcase",   title: "Gesture executive task",     subcat: "Executive",
    badges: ["auth"], canadian: false, buyable: false,
    spec: "Spec'd to floor plan · custom upholstery", price: "Quote · made-to-order" },
  { id: "obusforme",    brand: "ergoCentric", title: "Obusforme Comfort lounge",   subcat: "Lounge",
    badges: ["canadian", "auth", "low"], canadian: true, buyable: true,
    spec: "Cleanable vinyl · healthcare-rated · 7-yr", price: "from $899" },
  { id: "supra",        brand: "Global",      title: "Supra stacking chair",       subcat: "Stacking",
    badges: ["canadian", "auth"], canadian: true, buyable: true,
    spec: "Stacks 5 high · poly back · 5-yr", price: "from $329" },
  { id: "cs-one",       brand: "Allsteel",    title: "Acuity task chair",          subcat: "Task",
    badges: ["auth"], canadian: false, buyable: true,
    spec: "Mesh back · 4D arms · 12-yr warranty", price: "from $999" },
  { id: "bola",         brand: "Knoll",       title: "Bola task chair",            subcat: "Task",
    badges: ["auth"], canadian: false, buyable: false,
    spec: "Spec'd to floor plan · waitlist 6–8 wk",  price: "Quote · authorized" },
];

/* ---- breadcrumbs band ---------------------------------------------- */
function CNBreadcrumbs() {
  return (
    <div className="cn-crumb-band">
      <div className="cn-crumb-band__inner">
        <ol className="bbi-crumbs" aria-label="Breadcrumb">
          <li><a href="/">Home</a></li>
          <li><a href="/collections/business-furniture">Shop</a></li>
          <li>{CN_CATEGORY.title}</li>
        </ol>
      </div>
    </div>
  );
}

/* ---- intro band (tighter than template-2) -------------------------- */
function CNIntro({ mobile }) {
  return (
    <section className="cn-intro" aria-labelledby="cn-intro-title">
      <div className="cn-intro__grid">
        <div className="cn-intro__copy">
          <p className="cn-intro__eyebrow">Collection</p>
          <h1 id="cn-intro-title" className="cn-intro__title">{CN_CATEGORY.title}.</h1>
          <p className="cn-intro__deck">{CN_CATEGORY.standfirst}</p>
        </div>
        <dl className="cn-intro__stats" aria-label="What's inside">
          <div className="cn-intro__stat">
            <dt>Models</dt>
            <dd>{CN_CATEGORY.count}</dd>
          </div>
          <div className="cn-intro__stat">
            <dt>Brands</dt>
            <dd>{CN_CATEGORY.brandCount}</dd>
          </div>
          <div className="cn-intro__stat">
            <dt>Warranty</dt>
            <dd>{CN_CATEGORY.warrantyHeadline}</dd>
          </div>
        </dl>
      </div>
    </section>
  );
}

/* ---- filter bar (horizontal, with sub-cat chip row folded in) ------ */
function CNFilterBar({ mobile, activeSub, setActiveSub, filters, setFilters }) {
  const subcats = CN_CATEGORY.subcats;
  return (
    <section className="cn-filter-band" aria-label="Filter and sort">
      <div className="cn-filter-band__inner">

        {/* Row 1 — sub-category chips (folded-in sub-cat facet) */}
        <div className="cn-subchips" role="tablist" aria-label="Sub-category">
          <button
            type="button"
            role="tab"
            aria-selected={activeSub === "all"}
            className={"cn-subchip" + (activeSub === "all" ? " is-active" : "")}
            onClick={() => setActiveSub("all")}
          >
            <span className="cn-subchip__label">All</span>
            <span className="cn-subchip__count">{CN_PRODUCTS.length}</span>
          </button>
          {subcats.map((s) => (
            <button
              key={s.slug}
              type="button"
              role="tab"
              aria-selected={activeSub === s.slug}
              className={"cn-subchip" + (activeSub === s.slug ? " is-active" : "")}
              onClick={() => setActiveSub(s.slug)}
            >
              <span className="cn-subchip__label">{s.label}</span>
              <span className="cn-subchip__count">{s.count}</span>
            </button>
          ))}
        </div>

        {/* Row 2 — filter triggers + sort */}
        <div className="cn-filter-row">
          <div className="cn-filter-triggers">
            <CNFilterTrigger label="Brand" value={filters.brand}     onClear={() => setFilters({...filters, brand: null})} />
            <CNFilterTrigger label="Height range" value={filters.height} onClear={() => setFilters({...filters, height: null})} />
            <CNFilterTrigger label="Fabric tier" value={filters.fabric} onClear={() => setFilters({...filters, fabric: null})} />
            <CNFilterTrigger label="Warranty"     value={filters.warranty} onClear={() => setFilters({...filters, warranty: null})} />
            <button
              type="button"
              className={"cn-toggle" + (filters.canadian ? " is-on" : "")}
              aria-pressed={filters.canadian}
              onClick={() => setFilters({...filters, canadian: !filters.canadian})}
            >
              <span className="cn-toggle__dot" aria-hidden="true">
                {filters.canadian ? <_MapleLeaf size={11} /> : null}
              </span>
              <span className="cn-toggle__label">Canadian-made only</span>
            </button>
          </div>
        </div>

        {/* Row 3 — result count + sort + active chips */}
        <div className="cn-result-strip">
          <p className="cn-result-strip__count">
            Showing <b>1–{Math.min(9, CN_PRODUCTS.length)}</b> of <b>120</b> models
            {activeSub !== "all" && (
              <span className="cn-result-strip__filter">
                {" · "}
                <span className="cn-result-strip__filter-name">
                  {subcats.find((s) => s.slug === activeSub)?.label}
                </span>
                <button
                  type="button"
                  className="cn-result-strip__filter-x"
                  aria-label="Clear sub-category filter"
                  onClick={() => setActiveSub("all")}
                >×</button>
              </span>
            )}
          </p>
          <label className="cn-sort">
            <span className="cn-sort__label">Sort by</span>
            <span className="cn-sort__select">
              Featured
              <span className="cn-sort__chev" aria-hidden="true">▾</span>
            </span>
          </label>
        </div>

      </div>
    </section>
  );
}

function CNFilterTrigger({ label, value, onClear }) {
  const has = !!value;
  return (
    <span className={"cn-filter" + (has ? " is-set" : "")}>
      <button type="button" className="cn-filter__btn">
        <span className="cn-filter__label">{label}</span>
        {has && <span className="cn-filter__value">{value}</span>}
        <span className="cn-filter__chev" aria-hidden="true">▾</span>
      </button>
      {has && (
        <button type="button" className="cn-filter__x" aria-label={"Clear " + label} onClick={onClear}>×</button>
      )}
    </span>
  );
}

/* ---- product grid -------------------------------------------------- */
function CNProductGrid({ mobile, activeSub }) {
  // Filter products by active sub-cat for display realism
  const visible = activeSub === "all"
    ? CN_PRODUCTS
    : CN_PRODUCTS.filter((p) => {
        const target = CN_CATEGORY.subcats.find((s) => s.slug === activeSub)?.label;
        return p.subcat === target;
      });
  // Pad to at least 9 by re-using; in production, real data fills.
  const padded = visible.length >= 6 ? visible : [...visible, ...CN_PRODUCTS.filter((p) => !visible.includes(p))].slice(0, 9);
  const list = padded.length ? padded : CN_PRODUCTS;
  return (
    <section className={"cn-grid-section" + (mobile ? " cn-grid-section--mobile" : "")} aria-label="Products">
      <div className="cn-grid-section__inner">
        <div className={"cn-grid" + (mobile ? " cn-grid--mobile" : "")}>
          {list.map((p) => <CNProductCard key={p.id} product={p} />)}
        </div>
      </div>
    </section>
  );
}

function CNProductCard({ product }) {
  const { brand, title, subcat, badges, spec, price, buyable, canadian } = product;
  const hasLowStock = badges.includes("low");
  return (
    <article className="bbi-card bbi-card--product cn-product">
      <div className="bbi-card__media">
        <_Placeholder label={title + " · 16:9"} />
        {/* Top-left badge stack — sub-category mono chip is the always-on
            anchor; conditional badges layer on top via cn-product__badges. */}
        <span className="cn-product__subcat" aria-hidden="true">{subcat}</span>
        <div className="cn-product__badges">
          {canadian && (
            <span className="bbi-badge bbi-badge--canadian">
              <_MapleLeaf size={11} />
              Canadian-made
            </span>
          )}
          {badges.includes("auth") && !canadian && (
            <span className="bbi-badge bbi-badge--oem">Authorized dealer</span>
          )}
          {hasLowStock && (
            /* low-stock uses --warningBackground (token-driven, AAA on ink) */
            <span className="cn-product__low">
              <span className="cn-product__low-dot" aria-hidden="true" />
              Low stock
            </span>
          )}
        </div>
      </div>
      <div className="bbi-card__body cn-product__body">
        <p className="bbi-card__brand">{brand}</p>
        <h3 className="bbi-card__title"><a href={"/products/" + product.id}>{title}</a></h3>
        <p className="cn-product__spec">{spec}</p>
        <div className="cn-product__foot">
          <span className="cn-product__price">{price}</span>
          {/* Data-driven CTA — buyable → Add to cart, otherwise Request a quote.
              Same visual treatment, different intent — generalizes per BBI rule. */}
          {buyable ? (
            <a className="bbi-btn bbi-btn--primary bbi-btn--sm" href={"/cart/add?id=" + product.id}>
              Add to cart
            </a>
          ) : (
            <a className="bbi-btn bbi-btn--secondary bbi-btn--sm" href={"/pages/quote?ref=" + product.id}>
              Request a quote
            </a>
          )}
        </div>
      </div>
    </article>
  );
}

/* ---- pagination ---------------------------------------------------- */
function CNPagination() {
  return (
    <nav className="cn-pagination" aria-label="Pagination">
      <div className="cn-pagination__inner">
        <p className="cn-pagination__count">Showing 1–9 of 120 models</p>
        <ol className="cn-pagination__pages" aria-label="Pages">
          <li><span className="cn-page is-current" aria-current="page">1</span></li>
          <li><a className="cn-page" href="?page=2">2</a></li>
          <li><a className="cn-page" href="?page=3">3</a></li>
          <li className="cn-page-sep" aria-hidden="true">…</li>
          <li><a className="cn-page" href="?page=14">14</a></li>
          <li><a className="cn-page cn-page--next" href="?page=2">Next <span className="arrow">→</span></a></li>
        </ol>
      </div>
    </nav>
  );
}

/* ---- brand strip (this category only) ------------------------------ */
function CNBrandStrip() {
  return (
    <section className="cn-brand-strip" aria-labelledby="cn-brand-title">
      <div className="cn-brand-strip__inner">
        <div className="cn-brand-strip__head">
          <p className="bbi-section-head__eyebrow">Brands carried in {CN_CATEGORY.title.toLowerCase()}</p>
          <h2 id="cn-brand-title" className="cn-brand-strip__title">
            {CN_CATEGORY.brandCount} across three tiers.
          </h2>
        </div>
        <ul className="cn-brand-strip__list">
          {CN_CATEGORY.brands.map((b) => (
            <li key={b.name} className="cn-brand-strip__item">
              <a className="cn-brand-strip__link" href={"/pages/brands/" + b.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}>
                <span className="cn-brand-strip__name">
                  {b.canadian && <_MapleLeaf size={11} />}
                  {b.name}
                </span>
                <span className="cn-brand-strip__tier">
                  <span className={"cn-brand-strip__dot cn-brand-strip__dot--" + (b.authorized ? "auth" : "stocked")} aria-hidden="true" />
                  {b.tier}{b.authorized ? " · authorized" : " · stocked"}
                </span>
              </a>
            </li>
          ))}
        </ul>
        <div className="cn-brand-strip__foot">
          <span>Don't see a brand? We work with 30+ manufacturers across this category.</span>
          <a className="bbi-btn bbi-btn--secondary bbi-btn--sm" href="/pages/brands">Full brand directory</a>
        </div>
      </div>
    </section>
  );
}

/* ---- OECM bar (mirrors locked patterns) ---------------------------- */
function CNOECM() {
  return (
    <section className="cn-oecm" aria-label="OECM trust signal">
      <div className="cn-oecm__inner">
        <div className="cn-oecm__lead">
          <span className="bbi-badge bbi-badge--oecm">
            <span className="dot" />
            OECM vendor of record
          </span>
          <p className="cn-oecm__copy">
            Brant Business Interiors is an approved OECM supplier — pre-qualified procurement for Ontario's broader public sector. Use existing OECM agreements without re-tendering.
          </p>
        </div>
        <div className="cn-oecm__meta">
          <a className="bbi-btn bbi-btn--tertiary" href="/pages/oecm">
            <span className="label">Read the OECM details</span>
            <span className="arrow">→</span>
          </a>
        </div>
      </div>
    </section>
  );
}

/* ---- CTA closer (category-aware copy) ----------------------------- */
function CNCloser() {
  return (
    <section className="bbi-cta-section scheme-inverse">
      <div className="bbi-cta-section__inner">
        <div>
          <p className="bbi-cta-section__eyebrow">Quoting in volume</p>
          <h2 className="bbi-cta-section__heading">
            Outfitting a whole floor of {CN_CATEGORY.title.toLowerCase()}?
          </h2>
          <p className="bbi-cta-section__sub">
            100+ chairs, mixed brands, OECM paperwork, install. Same Ontario team. We respond within 1 business day.
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
function Collection({ mobile = false }) {
  const [activeSub, setActiveSub] = React.useState("all");
  const [filters, setFilters] = React.useState({
    brand: null, height: null, fabric: null, warranty: null, canadian: false,
  });
  return (
    <div className={"scheme-default cn-page" + (mobile ? " cn-page--mobile" : "")}>
      {mobile ? <_HeaderMobile /> : <_HeaderDesktop current="shop" />}
      <CNBreadcrumbs />
      <CNIntro mobile={mobile} />
      <CNFilterBar
        mobile={mobile}
        activeSub={activeSub}
        setActiveSub={setActiveSub}
        filters={filters}
        setFilters={setFilters}
      />
      <CNProductGrid mobile={mobile} activeSub={activeSub} />
      <CNPagination />
      <CNBrandStrip />
      <CNOECM />
      <CNCloser />
      <_Footer mobile={mobile} />
    </div>
  );
}

window.Collection = Collection;
