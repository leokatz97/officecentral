// ProductDetail.jsx — /products/{handle}
// Template 5 — Product Detail Page (unbuyable variant canonical).
// The same component handles the buyable variant via data.commerce.buyable.
// Composes only Phase-2 patterns + Homepage-shared atoms (HeaderDesktop,
// HeaderMobile, Footer, MapleLeaf, Placeholder).
// New patterns scoped under .pd-page (pdp.css).
//
// Data-driven: <ProductDetail /> with no props renders the canonical Ibex
// MVL2803 unbuyable PDP byte-identically every render. Pass `data` shaped
// like IBEX_DEFAULTS to render any of the 645 PDPs without a structural
// rewrite. Mirrors Landing.jsx's OECM_DEFAULTS pattern exactly.

const _HeaderDesktop = window.HeaderDesktop;
const _HeaderMobile  = window.HeaderMobile;
const _Footer        = window.Footer;
const _MapleLeaf     = window.MapleLeaf;
const _Placeholder   = window.Placeholder;

const { useState: __pdUseState } = React;

/* ===================================================================
   IBEX_DEFAULTS — canonical Ibex MVL2803 unbuyable PDP content,
   lifted to data shape. <ProductDetail /> with no `data` prop renders
   this exactly. Empty-state grace is exercised on the spec table —
   weight_capacity, finishes, certifications, warranty, country are
   all empty/absent and their rows hide.
   =================================================================== */
const IBEX_DEFAULTS = {
  crumbs: [
    { label: "Home", href: "/" },
    { label: "Shop Furniture", href: "/collections/business-furniture" },
    { label: "Seating", href: "/collections/seating" },
    { label: "Task Chairs", href: "/collections/task-chairs" },
    { label: "Ibex Multi-Tilter MVL2803", current: true },
  ],
  headerCurrent: "shop",

  product: {
    title: "Ibex | Upholstered Seat & Mesh Back Multi-Tilter MVL2803",
    brand: "OTG · Offices to Go",
    brandParent: "a division of Global Furniture Group",
    brandHref: "/pages/brands-global-teknion",
    productLine: "Ibex",
    primaryModel: "MVL2803",
    modelCount: 9,
    standfirst: "A multi-tilt task chair with a breathable mesh back, upholstered seat, and pneumatic height adjustment from 17.5\" to 21.5\". Ships with height-adjustable arms and an adjustable lumbar — built for an 8-hour shift, not a showroom.",
    badges: [
      { kind: "oecm",     label: "OECM-eligible" },
      { kind: "canadian", label: "Canadian-made" },
      { kind: "sold",     label: "Sold-out · quote available" },
    ],
  },

  gallery: {
    images: [
      { label: "Ibex MVL2803 · 3/4 front · main · 4:5" },
      { label: "Ibex MVL2803 · seat detail" },
      { label: "Ibex MVL2803 · mesh back" },
      { label: "Ibex MVL2803 · arm + lumbar" },
      { label: "Ibex MVL2803 · base + casters" },
      { label: "Ibex MVL2803 · seat-height range" },
    ],
  },

  commerce: {
    buyable: false,
    eyebrow: "Project quote",
    heading: "Request a quote on this product",
    sub: "Volume pricing, lead time, OECM PO eligibility, freight, install — all confirmed within 1 business day. We respond from the same Ontario team that quotes weekly.",
    primaryCtaLabel: "Request a quote",
    primaryCtaHref: "/pages/quote",
    secondaryCtaLabel: "Call 1-800-835-9565",
    secondaryCtaHref: "tel:18008359565",
    trust: "OECM purchasers welcome · Quotes within 1 business day · Same Ontario team since 1962",
    // buyable-only fields (left absent on canonical):
    // price, unit, stock, leadTime, qty
  },

  description: {
    eyebrow: "About this chair",
    h2: "Plain-spoken ergonomics for a shift, not a showroom.",
    paragraphs: [
      "The MVL2803 sits in the middle of the Ibex line — an upholstered seat for the cushioning, a mesh back for the airflow, and a multi-tilt mechanism that lets the seat and back move independently. It's the OTG chair we quote most often when a buyer wants a real ergonomic chair without specifying every detail of the seat foam.",
      "Pneumatic seat-height adjustment runs from 17.5\" to 21.5\" — which covers anyone from a 5'2\" desk worker to a 6'2\" architect on a stool-height bench. The arms are height-adjustable, the lumbar is adjustable, and the five-star base ships with carpet casters as standard (hard-floor casters available, named at quote time).",
      "OTG is a division of Global Furniture Group, which means the warranty paperwork goes through Global's Toronto office — same Canadian supply chain as the Global G20 and G30 lines. We file the claim on your behalf.",
    ],
    bestFor: "Best for full-time admin desks, school-board offices, and acute-care nurses' stations where the seat will see 6–10 hours a day, five days a week.",
  },

  specs: {
    // Populated rows on the canonical:
    dimensions: '26"W x 27"D x 39.5"H · Seat Height: 17.5" – 21.5"',
    weight: "56 lbs / 25.4 kg",
    materials: "Upholstered seat fabric, mesh back",
    features: [
      "Multi-tilt mechanism",
      "Upholstered seat with mesh back",
      "Pneumatic seat height adjustment (17.5\" – 21.5\")",
      "Height-adjustable arms",
      "Adjustable lumbar support",
      "Five-star base with casters",
    ],
    // Empty rows (hide cleanly — no "Warranty: —" placeholders):
    weightCapacity: "",
    finishes: [],
    certifications: [],
    warranty: "",
    country: "",
    leadTime: "",
    compliance: "",
  },

  variants: null,  // canonical: variants section hides entirely

  related: {
    eyebrow: "More from this category",
    h2: "Other task chairs we quote weekly.",
    items: [
      { brand: "ergoCentric", title: "tCentric Hybrid", note: "Multi-tilt · Lifetime warranty", canadian: true,  oecm: false, label: "tCentric Hybrid · 16:9" },
      { brand: "Global",      title: "G20 Synchro",     note: "Synchro tilt · 10-yr warranty",  canadian: true,  oecm: true,  label: "Global G20 · 16:9" },
      { brand: "Steelcase",   title: "Series 1",        note: "Live-back · 12-yr warranty",     canadian: false, oecm: true,  label: "Steelcase Series 1 · 16:9" },
      { brand: "Allsteel",    title: "Acuity",          note: "Mesh back · 12-yr warranty",     canadian: false, oecm: true,  label: "Allsteel Acuity · 16:9" },
    ],
  },

  brandBlock: {
    eyebrow: "About the brand",
    name: "OTG · Offices to Go",
    blurb: "OTG (Offices to Go) is the value-tier line from Global Furniture Group, headquartered in Toronto. We're an authorized dealer — same factory pricing, same warranty handling as the Global premium lines, on a shorter quote cycle.",
    href: "/pages/brands-global-teknion",
    ctaLabel: "Read about Global Furniture Group",
  },

  closer: {
    eyebrow: "Specifying for a project?",
    heading: "Outfitting more than one room?",
    sub: "Send us the floor plan or the spec list. We'll quote it as one project — products, freight, install, OECM paperwork. Same Ontario team. We respond within 1 business day.",
    primaryCtaLabel: "Request a quote",
    primaryCtaHref: "/pages/quote",
    trustLine: "or call 1-800-835-9565",
  },
};

/* ---------- breadcrumbs ---------- */
function PdBreadcrumbs({ items }) {
  return (
    <div className="pd-crumb-band">
      <div className="pd-crumb-band__inner">
        <ol className="bbi-crumbs" aria-label="Breadcrumb">
          {items.map((c, i) => (
            <li key={i} {...(c.current ? { "aria-current": "page" } : {})}>
              {c.current ? c.label : <a href={c.href}>{c.label}</a>}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}

/* ---------- HERO band: gallery + product info ---------- */
function PdGallery({ data }) {
  const [active, setActive] = __pdUseState(0);
  const images = data.images || [];
  const single = images.length <= 1;
  return (
    <div className={"pd-gallery" + (single ? " pd-gallery--single" : "")}>
      <div className="pd-gallery__main">
        <_Placeholder label={images[active] ? images[active].label : (data.placeholderLabel || "Product · 4:5")} />
      </div>
      {!single && (
        <div className="pd-gallery__thumbs">
          {images.map((img, i) => (
            <button
              key={i}
              type="button"
              className={"pd-gallery__thumb" + (i === active ? " pd-gallery__thumb--active" : "")}
              aria-label={"Show image " + (i + 1)}
              aria-current={i === active ? "true" : "false"}
              onClick={() => setActive(i)}
            >
              <_Placeholder label={"Thumb " + (i + 1)} />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function PdBadge({ b }) {
  if (b.kind === "canadian") {
    return (
      <span className="bbi-badge bbi-badge--canadian">
        <_MapleLeaf size={12} />
        {b.label}
      </span>
    );
  }
  if (b.kind === "oecm") {
    return (
      <span className="bbi-badge bbi-badge--oecm">
        <span className="dot" />
        {b.label}
      </span>
    );
  }
  if (b.kind === "oem") {
    return <span className="bbi-badge bbi-badge--oem">{b.label}</span>;
  }
  if (b.kind === "sale") {
    return <span className="bbi-badge bbi-badge--sale">{b.label}</span>;
  }
  if (b.kind === "new") {
    return <span className="bbi-badge bbi-badge--new">{b.label}</span>;
  }
  if (b.kind === "sold") {
    // Sold-out chip lives in pdp.css — does NOT exist in bbi-components.css.
    return <span className="pd-badge--sold">{b.label}</span>;
  }
  return <span className="bbi-badge">{b.label}</span>;
}

function PdCommerceUnbuyable({ data }) {
  return (
    <div className="pd-commerce">
      <p className="pd-commerce__eyebrow">{data.eyebrow}</p>
      <h2 className="pd-commerce__heading">{data.heading}</h2>
      <p className="pd-commerce__sub">{data.sub}</p>
      <a className="bbi-btn bbi-btn--primary bbi-btn--lg pd-commerce__primary" href={data.primaryCtaHref}>
        {data.primaryCtaLabel} <span className="arrow">→</span>
      </a>
      <a className="pd-commerce__secondary" href={data.secondaryCtaHref}>
        {data.secondaryCtaLabel}
      </a>
      <p className="pd-commerce__trust">
        <span className="dot" />
        <span>{data.trust}</span>
      </p>
    </div>
  );
}

function PdCommerceBuyable({ data }) {
  return (
    <div className="pd-commerce pd-commerce--buyable">
      <p className="pd-commerce__eyebrow">{data.eyebrow || "In stock"}</p>
      <h2 className="pd-commerce__heading">{data.heading || "Order direct from the catalogue"}</h2>
      <div className="pd-commerce__price">
        <span className="pd-commerce__price-val">{data.price}</span>
        {data.unit && <span className="pd-commerce__price-unit">{data.unit}</span>}
      </div>
      {data.stock && (
        <span className="pd-commerce__stock">
          <span className="dot" />
          {data.stock}{data.leadTime ? " · " + data.leadTime : ""}
        </span>
      )}
      <div className="pd-commerce__qty-row">
        <div className="pd-commerce__qty" role="group" aria-label="Quantity">
          <button className="pd-commerce__qty-btn" type="button" aria-label="Decrease quantity">−</button>
          <input className="pd-commerce__qty-val" type="text" defaultValue={data.qty || 1} aria-label="Quantity" readOnly />
          <button className="pd-commerce__qty-btn" type="button" aria-label="Increase quantity">+</button>
        </div>
        <a className="bbi-btn bbi-btn--primary bbi-btn--lg pd-commerce__primary" href="#cart">
          {data.primaryCtaLabel || "Add to cart"} <span className="arrow">→</span>
        </a>
      </div>
      <a className="pd-commerce__secondary" href={data.secondaryCtaHref || "/pages/quote"}>
        {data.secondaryCtaLabel || "Request a quote"}
      </a>
      <p className="pd-commerce__trust">
        <span className="dot" />
        <span>{data.trust || "OECM purchasers welcome · Quotes within 1 business day · Same Ontario team since 1962"}</span>
      </p>
    </div>
  );
}

function PdHero({ product, gallery, commerce }) {
  return (
    <section className="pd-hero" aria-label="Product hero">
      <div className="pd-hero__inner">
        <PdGallery data={gallery} />
        <div className="pd-product">
          <p className="pd-product__eyebrow">
            <a href={product.brandHref}>{product.brand}</a>
          </p>
          {product.brandParent && (
            <p className="pd-product__brand-parent">{product.brandParent}</p>
          )}
          <h1 className="pd-product__title">{product.title}</h1>
          <p className="pd-product__model">
            <b>{product.primaryModel}</b>
            {product.modelCount > 1 && (
              <>
                <span className="sep">·</span>
                {product.modelCount} model variants available
              </>
            )}
          </p>
          {product.badges && product.badges.length > 0 && (
            <div className="pd-product__badges">
              {product.badges.map((b, i) => <PdBadge key={i} b={b} />)}
            </div>
          )}
          <p className="pd-product__standfirst">{product.standfirst}</p>
          {commerce.buyable
            ? <PdCommerceBuyable data={commerce} />
            : <PdCommerceUnbuyable data={commerce} />
          }
        </div>
      </div>
    </section>
  );
}

/* ---------- DESCRIPTION / story block ---------- */
function PdDescription({ data }) {
  return (
    <section className="pd-description" aria-label="Description">
      <div className="pd-description__inner">
        {data.eyebrow && <p className="pd-description__eyebrow">{data.eyebrow}</p>}
        {data.h2 && <h2 className="pd-description__h2">{data.h2}</h2>}
        <div className="pd-description__body">
          {data.paragraphs.map((p, i) => <p key={i}>{p}</p>)}
        </div>
        {data.bestFor && (
          <p className="pd-description__bestfor">
            <b>Best for</b>
            {data.bestFor}
          </p>
        )}
      </div>
    </section>
  );
}

/* ---------- SPEC TABLE ---------- */
const SPEC_ROW_DEFS = [
  { key: "brand",          label: "Brand",          source: "product",  field: "brand" },
  { key: "productLine",    label: "Product line",   source: "product",  field: "productLine" },
  { key: "modelCodes",     label: "Model codes",    source: "product",  field: "modelCodes",     join: " · " },
  { key: "dimensions",     label: "Dimensions",     source: "specs",    field: "dimensions" },
  { key: "weight",         label: "Weight",         source: "specs",    field: "weight" },
  { key: "weightCapacity", label: "Weight capacity",source: "specs",    field: "weightCapacity" },
  { key: "materials",      label: "Materials",      source: "specs",    field: "materials" },
  { key: "finishes",       label: "Finishes",       source: "specs",    field: "finishes",       join: ", " },
  { key: "features",       label: "Key features",   source: "specs",    field: "features",       list: true },
  { key: "certifications", label: "Certifications", source: "specs",    field: "certifications", join: " · " },
  { key: "warranty",       label: "Warranty",       source: "specs",    field: "warranty" },
  { key: "country",        label: "Country of origin", source: "specs", field: "country" },
  { key: "leadTime",       label: "Lead time",      source: "specs",    field: "leadTime" },
  { key: "compliance",     label: "Compliance",     source: "specs",    field: "compliance" },
];

function specHasValue(v) {
  if (v == null) return false;
  if (Array.isArray(v)) return v.length > 0;
  return String(v).trim().length > 0;
}

function PdSpecs({ specs, product }) {
  // Hidden rows for the canonical Ibex render are computed off `specs`.
  // Brand / productLine / modelCodes are sourced from product.* so the
  // table always includes the manufacturer + model context — these are
  // structural identity fields, not optional spec fields.
  const productCtx = {
    brand: product.brand,
    productLine: product.productLine,
    modelCodes: product.modelCodes ||
      (product.primaryModel
        ? [product.primaryModel].concat(product.extraModels || [])
        : []),
  };
  const visible = SPEC_ROW_DEFS.filter((def) => {
    const v = def.source === "product" ? productCtx[def.field] : specs[def.field];
    return specHasValue(v);
  });
  if (visible.length === 0) return null;
  return (
    <section className="pd-specs" aria-label="Specifications">
      <div className="pd-specs__inner">
        <div className="pd-specs__head">
          <p className="pd-specs__eyebrow">Specifications</p>
          <h2 className="pd-specs__h2">Everything we'd put on the spec sheet.</h2>
        </div>
        <div className="pd-specs__table">
          {visible.map((def) => {
            const v = def.source === "product" ? productCtx[def.field] : specs[def.field];
            let valNode;
            if (def.list && Array.isArray(v)) {
              valNode = (
                <ul>{v.map((it, i) => <li key={i}>{it}</li>)}</ul>
              );
            } else if (Array.isArray(v)) {
              valNode = v.join(def.join || ", ");
            } else {
              valNode = v;
            }
            return (
              <div key={def.key} className="pd-spec-row">
                <span className="pd-spec-row__label bbi-mono">{def.label}</span>
                <span className="pd-spec-row__value">{valNode}</span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ---------- VARIANT selector / "What you'll quote" summary ---------- */
function PdVariants({ data }) {
  const items = (data && data.items) || [];
  if (items.length === 0) return null;
  return (
    <section className="pd-variants" aria-label="Configuration">
      <div className="pd-variants__inner">
        <p className="pd-variants__eyebrow">{data.eyebrow || "Configuration"}</p>
        <h2 className="pd-variants__h2">{data.h2 || "What you'll quote."}</h2>
        <div className="pd-variants__summary">
          {items.map((row, i) => (
            <div key={i} className="pd-variant-row">
              <span className="pd-variant-row__label">{row.label}</span>
              <span className="pd-variant-row__value">{row.value}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- OECM bar (reuses locked .hp-oecm) ---------- */
function PdOECMBar() {
  return (
    <section className="hp-oecm" aria-label="OECM trust signal">
      <div className="bbi-container hp-oecm__inner">
        <div className="hp-oecm__lead">
          <span className="bbi-badge bbi-badge--oecm">
            <span className="dot" />
            OECM vendor of record
          </span>
          <p className="hp-oecm__copy">
            Brant Business Interiors is an approved OECM supplier — pre-qualified procurement for Ontario's broader public sector. Use existing OECM agreements without re-tendering.
          </p>
        </div>
        <div className="hp-oecm__meta">
          <a className="bbi-btn bbi-btn--tertiary" href="/pages/oecm">
            <span className="label">Read the OECM details</span>
            <span className="arrow">→</span>
          </a>
        </div>
      </div>
    </section>
  );
}

/* ---------- RELATED products ---------- */
function PdRelatedCard({ p }) {
  return (
    <article className="bbi-card bbi-card--product">
      <div className="bbi-card__media">
        <_Placeholder label={p.label || (p.brand + " " + p.title + " · 16:9")} />
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
        <h3 className="bbi-card__title"><a href={p.href || "#"}>{p.title}</a></h3>
        <p className="bbi-card__brand" style={{ opacity: 0.78, textTransform: "none", letterSpacing: 0, fontFamily: "var(--bodyFont)", fontSize: 13 }}>
          {p.note}
        </p>
        <a className="bbi-card__cta" href={p.href || "/pages/quote"}>
          Request a quote <span className="arrow">→</span>
        </a>
      </div>
    </article>
  );
}

function PdRelated({ data }) {
  if (!data || !data.items || data.items.length === 0) return null;
  return (
    <section className="pd-related" aria-label="Related products">
      <div className="pd-related__inner">
        <div className="pd-related__head">
          <div>
            <p className="pd-related__eyebrow">{data.eyebrow}</p>
            <h2 className="pd-related__h2">{data.h2}</h2>
          </div>
          <a className="bbi-btn bbi-btn--secondary" href="/collections/task-chairs">
            View all task chairs
          </a>
        </div>
        <div className="pd-related__grid">
          {data.items.map((p, i) => <PdRelatedCard key={i} p={p} />)}
        </div>
      </div>
    </section>
  );
}

/* ---------- BRAND block ---------- */
function PdBrandBlock({ data }) {
  if (!data) return null;
  return (
    <section className="pd-brand-block" aria-label="About the brand">
      <div className="pd-brand-block__inner">
        <div className="pd-brand-block__plate">
          <p className="pd-brand-block__eyebrow">{data.eyebrow || "About the brand"}</p>
          <h2 className="pd-brand-block__name">{data.name}</h2>
          <p className="pd-brand-block__blurb">{data.blurb}</p>
          <a className="bbi-btn bbi-btn--secondary pd-brand-block__cta" href={data.href}>
            {data.ctaLabel || "Read about the brand"}
          </a>
        </div>
        <div>
          <_Placeholder label={(data.name || "Brand") + " · 4:3"} ratio="4 / 3" />
        </div>
      </div>
    </section>
  );
}

/* ---------- CTA closer (reuses .bbi-cta-section verbatim) ---------- */
function PdCloser({ data }) {
  return (
    <section className="bbi-cta-section scheme-inverse">
      <div className="bbi-cta-section__inner">
        <div>
          <p className="bbi-cta-section__eyebrow">{data.eyebrow}</p>
          <h2 className="bbi-cta-section__heading">{data.heading}</h2>
          <p className="bbi-cta-section__sub">{data.sub}</p>
        </div>
        <div className="bbi-cta-section__actions">
          <a className="bbi-btn bbi-btn--primary bbi-btn--lg" href={data.primaryCtaHref}>
            {data.primaryCtaLabel} <span className="arrow">→</span>
          </a>
          <div className="bbi-cta-section__trust">
            <span className="dot" />
            <span><b>1 business day response</b> on every quote — no minimums, no accounts.</span>
          </div>
          <div className="bbi-cta-section__trust">
            <span className="dot" />
            <span>{data.trustLine || "or call "}<a href="tel:18008359565">1-800-835-9565</a> · Mon–Fri 8–5 ET</span>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------- page composition ---------- */
function ProductDetail({ mobile = false, data = IBEX_DEFAULTS }) {
  const showSpecs = (() => {
    const specs = data.specs || {};
    const product = data.product || {};
    // The spec table also includes brand/productLine/modelCodes from product.*
    if (product.brand || product.productLine) return true;
    return Object.values(specs).some(v => Array.isArray(v) ? v.length > 0 : (v != null && String(v).trim().length > 0));
  })();
  const showVariants    = !!(data.variants && data.variants.items && data.variants.items.length > 0);
  const showBrandBlock  = !!data.brandBlock;
  const showRelated     = !!(data.related && data.related.items && data.related.items.length > 0);

  return (
    <div className={"scheme-default pd-page" + (mobile ? " pd-page--mobile" : "")}>
      {mobile ? <_HeaderMobile /> : <_HeaderDesktop current={data.headerCurrent || "shop"} />}
      <PdBreadcrumbs items={data.crumbs} />
      <PdHero product={data.product} gallery={data.gallery} commerce={data.commerce} />
      <PdDescription data={data.description} />
      {showSpecs     && <PdSpecs specs={data.specs || {}} product={data.product} />}
      {showVariants  && <PdVariants data={data.variants} />}
      <PdOECMBar />
      {showRelated   && <PdRelated data={data.related} />}
      {showBrandBlock && <PdBrandBlock data={data.brandBlock} />}
      <PdCloser data={data.closer} />
      <_Footer mobile={mobile} />
    </div>
  );
}

window.ProductDetail = ProductDetail;
window.PDP_IBEX_DEFAULTS = IBEX_DEFAULTS;
