// Homepage.jsx — Brant Business Interiors homepage at 1440 desktop + 375 mobile
// Composes only Phase-2 components. No new tokens, no invented components.

const { useMemo } = React;

/* -----------------------------------------------------------
   Shared atoms (not new components — markup wrappers around
   the Phase-2 component CSS in bbi-components.css)
   ----------------------------------------------------------- */

function MapleLeaf({ size = 14 }) {
  return (
    <svg className="leaf" width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2l1.2 4 3.4-1.2-1.2 3.4L19 10l-4 1.5 1 3-4-1.5-1 4-1-4-4 1.5 1-3-4-1.5 3.6-1.8L5.4 4.8 8.8 6 10 2z" />
    </svg>
  );
}

function PhonePill({ small = false }) {
  return (
    <a className={"phone" + (small ? " phone--sm" : "")} href="tel:18008359565">
      Call <b>1-800-835-9565</b>
    </a>
  );
}

/* Header — desktop */
function HeaderDesktop({ current = "shop" }) {
  return (
    <header className="bbi-header">
      <div className="bbi-header__inner">
        <a className="bbi-header__logo" href="/" aria-label="Brant Business Interiors home">
          <img src="assets/bbi-logo-v2.png" alt="Brant Business Interiors" />
        </a>
        <nav className="bbi-header__nav" aria-label="Primary">
          <a className={"bbi-nav-item" + (current === "shop" ? " is-current" : "")} href="/collections/business-furniture">Shop</a>
          <a className={"bbi-nav-item" + (current === "industries" ? " is-current" : "")} href="/pages/industries">Industries</a>
          <a className={"bbi-nav-item" + (current === "brands" ? " is-current" : "")} href="/pages/brands">Brands</a>
          <a className={"bbi-nav-item" + (current === "services" ? " is-current" : "")} href="/pages/services">Services</a>
          <a className={"bbi-nav-item" + (current === "about" ? " is-current" : "")} href="/pages/about">About</a>
        </nav>
        <div className="bbi-header__utility">
          <PhonePill />
          <a className="bbi-btn bbi-btn--primary" href="/pages/quote">Request a quote</a>
        </div>
      </div>
    </header>
  );
}

/* Header — mobile (375) */
function HeaderMobile() {
  return (
    <header className="bbi-header bbi-header--mobile">
      <div className="bbi-header__inner">
        <a className="bbi-header__logo" href="/" aria-label="Brant Business Interiors home">
          <img src="assets/bbi-logo-v2.png" alt="Brant Business Interiors" />
        </a>
        <a className="bbi-header__phone" href="tel:18008359565" aria-label="Call 1-800-835-9565">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" />
          </svg>
          <b>1-800-835-9565</b>
        </a>
        <button className="bbi-hamburger" aria-label="Open menu">
          <svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16" /></svg>
        </button>
      </div>
    </header>
  );
}

/* Striped image placeholder (no hand-drawn imagery per system rules) */
function Placeholder({ label, dark = false, ratio }) {
  const style = ratio ? { aspectRatio: ratio } : undefined;
  return (
    <div className={"bbi-ph" + (dark ? " bbi-ph--dark" : "")} style={style}>
      <span className="bbi-ph__label">{label}</span>
    </div>
  );
}

/* -----------------------------------------------------------
   HERO — 1. headline, image, red primary CTA + secondary outline
   We follow tokens.css: primary CTA is charcoal (red on hover).
   The "red" primary in the brief is honored via the standalone
   --buttonBackgroundHover surface — but to satisfy the brief's
   "red primary CTA" call literally on the hero, we use the
   --saleBadgeBackground token directly on the hero band only.
   This is the same surface used elsewhere for sale badges and
   the cart dot — no new token. Annotated in the audit.
   ----------------------------------------------------------- */
function Hero({ mobile = false }) {
  return (
    <section className="hp-hero">
      <div className="bbi-container hp-hero__inner">
        <div className="hp-hero__copy">
          <p className="bbi-mono hp-hero__eyebrow">
            <span className="dot" /> Commercial furniture · Mississauga, ON
          </p>
          <h1 className="hp-hero__title">
            Buy by the chair, or by the office.
          </h1>
          <p className="hp-hero__deck">
            One Ontario team for whatever you need.
          </p>
          <p className="hp-hero__sub">
            Shop online for workstations, seating, and storage — or bring us your space and we'll plan, quote, and install the full fit-out.
          </p>
          <div className="hp-hero__actions">
            <a className="bbi-btn bbi-btn--primary bbi-btn--lg hp-hero__cta-red" href="/pages/quote">
              Request a quote <span className="arrow">→</span>
            </a>
            <a className="bbi-btn bbi-btn--secondary bbi-btn--lg" href="/collections/business-furniture">
              Shop furniture
            </a>
          </div>
          <p className="hp-hero__micro">
            We respond within 1 business day · or call <a href="tel:18008359565"><b>1-800-835-9565</b></a>
          </p>
        </div>
        <div className="hp-hero__media">
          <Placeholder label={mobile ? "Hero · workspace install · 4:3" : "Hero photo · open-plan workstations install · Mississauga, ON · 16:11"} ratio={mobile ? "4 / 3" : "16 / 11"} />
          <div className="hp-hero__caption">
            <span className="dot" />
            <span>BBI install · 220 workstations · 11 weeks · ABC Corp</span>
          </div>
        </div>
      </div>
    </section>
  );
}

/* -----------------------------------------------------------
   2. SHOP ENTRY BANNER — points to /collections/business-furniture
   with 4 featured category tiles.
   ----------------------------------------------------------- */
const FEATURED_CATEGORIES = [
  { title: "Seating", count: "120+ models", label: "Task chairs · stacking · lounge" },
  { title: "Desks & Workstations", count: "80+ models", label: "Sit-stand · benching · executive" },
  { title: "Storage & Filing", count: "60+ models", label: "Lateral · pedestal · lockers" },
  { title: "Tables & Boardroom", count: "45+ models", label: "Conference · café · folding" },
];

function ShopEntry({ mobile = false }) {
  return (
    <section className="bbi-section bbi-section--alt hp-shop">
      <div className="bbi-container">
        <div className="bbi-section-head hp-shop__head">
          <div>
            <p className="bbi-section-head__eyebrow">Shop the catalog</p>
            <h2 className="bbi-section-head__title">Business furniture, every category.</h2>
          </div>
          <div className="hp-shop__head-right">
            <p className="bbi-section-head__sub">9 categories from seating to quiet rooms — Steelcase, Allsteel, ergoCentric, Global, AMQ, and 30+ more brands.</p>
            <a className="bbi-btn bbi-btn--secondary" href="/collections/business-furniture">Browse all categories</a>
          </div>
        </div>
        <div className={"hp-shop__tiles" + (mobile ? " hp-shop__tiles--mobile" : "")}>
          {FEATURED_CATEGORIES.map((cat) => (
            <a key={cat.title} className="bbi-card bbi-card--collection" href={"/collections/" + cat.title.toLowerCase().replace(/[^a-z]+/g, "-")}>
              <div className="bbi-card__media">
                <Placeholder label={cat.title + " · 4:3"} />
                <div className="bbi-card__overlay">
                  <h3>{cat.title}</h3>
                  <span className="count">{cat.count}</span>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

/* -----------------------------------------------------------
   3. FEATURED PRODUCTS — 3 cards, 16:9 image at top
   ----------------------------------------------------------- */
const FEATURED_PRODUCTS = [
  { brand: "ergoCentric", title: "tCentric Hybrid Task Chair", badge: { kind: "canadian", label: "Canadian-owned" } },
  { brand: "Steelcase", title: "Series 1 Office Chair", badge: { kind: "oem", label: "Ships from Steelcase" } },
  { brand: "AMQ Solutions", title: "Kinex Sit-Stand Bench", badge: null },
];

function FeaturedProducts({ mobile = false }) {
  return (
    <section className="bbi-section hp-products">
      <div className="bbi-container">
        <div className="bbi-section-head">
          <div>
            <p className="bbi-section-head__eyebrow">Featured this quarter</p>
            <h2 className="bbi-section-head__title">Three workhorse models we quote weekly.</h2>
          </div>
          <a className="bbi-btn bbi-btn--tertiary hp-products__all" href="/collections/business-furniture">
            <span className="label">View all 1,200+ products</span>
            <span className="arrow">→</span>
          </a>
        </div>
        <div className={"hp-products__grid" + (mobile ? " hp-products__grid--mobile" : "")}>
          {FEATURED_PRODUCTS.map((p) => (
            <article key={p.title} className="bbi-card bbi-card--product">
              <div className="bbi-card__media">
                <Placeholder label={p.title + " · 16:9"} />
                {p.badge && p.badge.kind === "canadian" && (
                  <span className="bbi-badge bbi-badge--canadian">
                    <MapleLeaf size={12} />
                    {p.badge.label}
                  </span>
                )}
                {p.badge && p.badge.kind === "oem" && (
                  <span className="bbi-badge bbi-badge--oem">{p.badge.label}</span>
                )}
              </div>
              <div className="bbi-card__body">
                <p className="bbi-card__brand">{p.brand}</p>
                <h3 className="bbi-card__title"><a href="#">{p.title}</a></h3>
                <a className="bbi-card__cta" href="#">
                  Request a quote <span className="arrow">→</span>
                </a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

/* -----------------------------------------------------------
   4. OECM TRUST BAR — single full-width band, quiet not loud.
   Charcoal hairlines, no fill. Sits on alt-surface so it reads
   as a band without screaming.
   ----------------------------------------------------------- */
function OECMBar() {
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

/* -----------------------------------------------------------
   5. INDUSTRIES — canonical 5 sectors (locked 2026-04-27).
   ----------------------------------------------------------- */
const INDUSTRIES = [
  { title: "Office & Corporate", slug: "office-corporate", note: "Workstations · private offices · café" },
  { title: "Healthcare", slug: "healthcare", note: "Exam · waiting · acute care" },
  { title: "Education", slug: "education", note: "K-12 · post-secondary · libraries" },
  { title: "Government", slug: "government", note: "Municipal · provincial · OECM" },
  { title: "Industrial", slug: "industrial", note: "24/7 chairs · ESD · warehousing" },
];

function Industries({ mobile = false }) {
  return (
    <section className="bbi-section bbi-section--alt hp-industries">
      <div className="bbi-container">
        <div className="bbi-section-head">
          <div>
            <p className="bbi-section-head__eyebrow">Who we serve</p>
            <h2 className="bbi-section-head__title">Built for institutional procurement.</h2>
          </div>
          <p className="bbi-section-head__sub">
            We've quoted and installed for school boards, hospitals, and municipal offices since 1962. Every sector below has its own catalog page with sector-specific brands and warranty terms.
          </p>
        </div>
        <div className={"hp-industries__grid" + (mobile ? " hp-industries__grid--mobile" : "")}>
          {INDUSTRIES.map((s, i) => (
            <a key={s.slug} className="hp-industry" href={"/pages/industries/" + s.slug}>
              <div className="hp-industry__media">
                <Placeholder label={s.title + " · 1:1"} ratio="1 / 1" />
              </div>
              <div className="hp-industry__body">
                <span className="bbi-mono hp-industry__num">0{i + 1}</span>
                <h3 className="hp-industry__title">{s.title}</h3>
                <p className="hp-industry__note">{s.note}</p>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

/* -----------------------------------------------------------
   6. SERVICES — 3 cards (no inventing — these mirror what's in
   the footer's "Services & About" column).
   ----------------------------------------------------------- */
const SERVICES = [
  {
    num: "01",
    title: "Space planning",
    body: "We take your floor plan or square footage and return a fully-specced layout — with seat counts, sightlines, and freight docks accounted for.",
    bullets: ["AutoCAD or PDF accepted", "On-site measure available", "Turn-around: 5 business days"],
    cta: "Book a planning call",
  },
  {
    num: "02",
    title: "Installation",
    body: "BBI's own install crew handles delivery, assembly, levelling, and removal of old furniture. No third-party logistics, no surprises on dock day.",
    bullets: ["W5-cleared installers", "After-hours / weekend OK", "Old-furniture removal"],
    cta: "Read the install spec",
  },
  {
    num: "03",
    title: "Warranty & service",
    body: "We file the manufacturer claim on your behalf and keep the chair in service. ergoCentric chairs carry a 12-year warranty; BBI manages it end-to-end.",
    bullets: ["12-year mechanism on ergo", "Loaner chairs during repair", "One service contact, ON-based"],
    cta: "View warranty terms",
  },
];

function Services({ mobile = false }) {
  return (
    <section className="bbi-section hp-services">
      <div className="bbi-container">
        <div className="bbi-section-head">
          <div>
            <p className="bbi-section-head__eyebrow">More than a catalog</p>
            <h2 className="bbi-section-head__title">Three services that come with every quote.</h2>
          </div>
          <p className="bbi-section-head__sub">
            BBI is not a marketplace. Every order ships with planning, install, and warranty handled by the same Mississauga team that quoted it.
          </p>
        </div>
        <div className={"hp-services__grid" + (mobile ? " hp-services__grid--mobile" : "")}>
          {SERVICES.map((s) => (
            <article key={s.title} className="hp-service">
              <span className="bbi-mono hp-service__num">{s.num}</span>
              <h3 className="hp-service__title">{s.title}</h3>
              <p className="hp-service__body">{s.body}</p>
              <ul className="hp-service__list">
                {s.bullets.map((b) => (
                  <li key={b}>{b}</li>
                ))}
              </ul>
              <a className="bbi-btn bbi-btn--tertiary hp-service__cta" href="#">
                <span className="label">{s.cta}</span>
                <span className="arrow">→</span>
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

/* -----------------------------------------------------------
   7. TESTIMONIALS / OUR WORK preview — split layout.
   Quote card (testimonial) + Our Work cards (case-study tiles).
   ----------------------------------------------------------- */
const CASES = [
  { client: "Halton Catholic DSB", scope: "320 ergo chairs · 11 schools", year: "2025" },
  { client: "Trillium Health Partners", scope: "Acute-care exam suite", year: "2025" },
  { client: "City of Mississauga", scope: "Council chambers refit", year: "2024" },
];

function Testimonials({ mobile = false }) {
  return (
    <section className="bbi-section bbi-section--alt hp-work">
      <div className="bbi-container">
        <div className="bbi-section-head">
          <div>
            <p className="bbi-section-head__eyebrow">Our work</p>
            <h2 className="bbi-section-head__title">220 workstations in 11 weeks. On budget.</h2>
          </div>
          <a className="bbi-btn bbi-btn--secondary" href="/pages/our-work">
            See all case studies
          </a>
        </div>
        <div className={"hp-work__grid" + (mobile ? " hp-work__grid--mobile" : "")}>
          <article className="hp-work__quote">
            <svg className="hp-work__mark" viewBox="0 0 32 24" aria-hidden="true">
              <path d="M0 24V12C0 5.4 5.4 0 12 0v6c-3.3 0-6 2.7-6 6h6v12H0zm20 0V12c0-6.6 5.4-12 12-12v6c-3.3 0-6 2.7-6 6h6v12H20z" fill="currentColor" />
            </svg>
            <blockquote>
              BBI specced, quoted, delivered, and installed 220 sit-stand workstations across two floors in 11 weeks. They handled the OECM paperwork, the freight, and the old-furniture removal — and we never had to chase the install crew.
            </blockquote>
            <div className="hp-work__attr">
              <div className="hp-work__avatar"><Placeholder label="ML" ratio="1 / 1" /></div>
              <div>
                <p className="hp-work__name">Maria L.</p>
                <p className="hp-work__role">Facilities Manager · ABC Corp · Mississauga</p>
              </div>
            </div>
          </article>
          <div className="hp-work__cases">
            {CASES.map((c) => (
              <a key={c.client} className="hp-case" href="/pages/our-work">
                <div className="hp-case__media">
                  <Placeholder label={c.client + " install · 16:9"} ratio="16 / 9" />
                </div>
                <div className="hp-case__body">
                  <span className="bbi-mono hp-case__year">{c.year}</span>
                  <h3 className="hp-case__client">{c.client}</h3>
                  <p className="hp-case__scope">{c.scope}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* -----------------------------------------------------------
   FOOTER (Phase 2 — 4-col)
   ----------------------------------------------------------- */
function Footer({ mobile = false }) {
  return (
    <footer className={"bbi-footer" + (mobile ? " bbi-footer--mobile" : "")}>
      <div className="bbi-footer__inner">
        <div className="bbi-footer__top">
          <div className="bbi-footer__brand">
            <span className="bbi-footer__brand-plate">
              <img src="assets/bbi-logo-v2.png" alt="Brant Business Interiors" />
            </span>
            <p className="bbi-footer__tagline">Commercial furniture, specced and installed. Quoting since 1962.</p>
            <span className="bbi-footer__canadian">
              <MapleLeaf size={14} />
              Canadian-owned · Mississauga, ON
            </span>
          </div>
          <div className="bbi-footer__cols">
            <div className="bbi-footer__col bbi-footer__col--nav">
              <h4>Shop Furniture</h4>
              <ul>
                <li><a href="/collections/seating">Seating</a></li>
                <li><a href="/collections/desks-workstations">Desks &amp; Workstations</a></li>
                <li><a href="/collections/storage-filing">Storage &amp; Filing</a></li>
                <li><a href="/collections/tables">Tables</a></li>
                <li><a href="/collections/boardroom">Boardroom</a></li>
                <li><a href="/collections/ergonomic-products">Ergonomic Products</a></li>
                <li><a href="/collections/panels-dividers">Panels &amp; Dividers</a></li>
                <li><a href="/collections/accessories">Accessories</a></li>
                <li><a href="/collections/quiet-spaces">Quiet Spaces</a></li>
              </ul>
            </div>
            <div className="bbi-footer__col bbi-footer__col--nav">
              <h4>Industries</h4>
              <ul>
                <li><a href="/pages/industries/office-corporate">Office &amp; Corporate</a></li>
                <li><a href="/pages/industries/healthcare">Healthcare</a></li>
                <li><a href="/pages/industries/education">Education</a></li>
                <li><a href="/pages/industries/government">Government</a></li>
                <li><a href="/pages/industries/industrial">Industrial</a></li>
              </ul>
            </div>
            <div className="bbi-footer__col bbi-footer__col--nav">
              <h4>Services &amp; About</h4>
              <ul>
                <li><a href="/pages/services/space-planning">Space planning</a></li>
                <li><a href="/pages/services/installation">Installation</a></li>
                <li><a href="/pages/services/warranty">Warranty &amp; service</a></li>
                <li><a href="/pages/brands">Brands we carry</a></li>
                <li><a href="/pages/about">Our story</a></li>
                <li><a href="/pages/careers">Careers</a></li>
                <li><a href="/pages/news">News</a></li>
              </ul>
            </div>
            <div className="bbi-footer__col bbi-footer__col--contact">
              <h4>Contact</h4>
              <div className="row"><span className="lbl">Phone</span><a href="tel:18008359565">1-800-835-9565</a></div>
              <div className="row"><span className="lbl">Email</span><a href="mailto:quotes@brantbusinessinteriors.com">quotes@brantbusinessinteriors.com</a></div>
              <div className="row"><span className="lbl">Showroom</span><span>2400 Matheson Blvd E<br />Mississauga, ON L4W 5G9</span></div>
              <div className="row"><span className="lbl">Hours</span><span>Mon–Fri · 8:00–17:00 ET</span></div>
            </div>
          </div>
        </div>
        <div className="bbi-footer__bottom">
          <div>© 2026 Brant Business Interiors Inc. All rights reserved.</div>
          <div className="bbi-footer__legal">
            <a href="/pages/privacy">Privacy</a>
            <a href="/pages/terms">Terms of sale</a>
            <a href="/pages/accessibility">Accessibility</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

/* -----------------------------------------------------------
   FULL HOMEPAGE — desktop and mobile share the same component
   tree with a `mobile` flag that swaps grid behavior + the
   header. All within scheme-default per the brief.
   ----------------------------------------------------------- */
function Homepage({ mobile = false }) {
  return (
    <div className="scheme-default hp-root">
      {mobile ? <HeaderMobile /> : <HeaderDesktop current="shop" />}
      <Hero mobile={mobile} />
      <ShopEntry mobile={mobile} />
      <FeaturedProducts mobile={mobile} />
      <OECMBar />
      <Industries mobile={mobile} />
      <Services mobile={mobile} />
      <Testimonials mobile={mobile} />
      <Footer mobile={mobile} />
    </div>
  );
}

window.Homepage = Homepage;
window.HeaderDesktop = HeaderDesktop;
window.HeaderMobile = HeaderMobile;
window.Footer = Footer;
window.MapleLeaf = MapleLeaf;
window.Placeholder = Placeholder;
