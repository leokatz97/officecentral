// Landing.jsx — /pages/oecm
// Template 4 — Service / OECM landing page.
// Composes only Phase-2 patterns + Homepage-shared atoms (HeaderDesktop,
// HeaderMobile, Footer, MapleLeaf, Placeholder).
// New patterns are scoped under .lp-page (landing.css).
//
// Data-driven: <Landing /> with no props renders the OECM page from
// OECM_DEFAULTS. Pass a `data` prop shaped like OECM_DEFAULTS to render
// /pages/healthcare, /pages/brands-keilhauer, /pages/about, etc.
// Three sections present/absent toggle on data.{trustPhotos|crosslinks}.length
// and on data.proofStats truthiness; hero badge toggles on data.hero.heroBadge.show.

const _HeaderDesktop = window.HeaderDesktop;
const _HeaderMobile  = window.HeaderMobile;
const _Footer        = window.Footer;
const _MapleLeaf     = window.MapleLeaf;
const _Placeholder   = window.Placeholder;

const { useState } = React;

/* ---------- icon glyphs (composed in currentColor) -------------------- */
function IconCheck() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      <rect x="3" y="3" width="26" height="26" />
      <path d="M9 16.5 l5 5 l9 -11" />
    </svg>
  );
}
function IconShield() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      <path d="M16 3 L27 7 V16 c0 7 -5 11 -11 13 c-6 -2 -11 -6 -11 -13 V7 Z" />
      <path d="M11 16 l4 4 l6 -8" />
    </svg>
  );
}
function IconHandshake() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      <circle cx="16" cy="16" r="12" />
      <path d="M9 16 l4 4 l4 -4 l4 4 l-4 4" />
      <path d="M9 16 l4 -4 l4 4 l4 -4 l4 4" />
    </svg>
  );
}
function IconGrid() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      <rect x="4" y="4" width="10" height="10" />
      <rect x="18" y="4" width="10" height="10" />
      <rect x="4" y="18" width="10" height="10" />
      <rect x="18" y="18" width="10" height="10" />
    </svg>
  );
}
function IconArrowRight() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      <path d="M3 9 H15" />
      <path d="M10 4 L15 9 L10 14" />
    </svg>
  );
}
function IconChevronDown() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
      <path d="M3 6 L8 11 L13 6" />
    </svg>
  );
}
function IconSeating() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.3" aria-hidden="true">
      <path d="M7 13 V6 a3 3 0 0 1 3 -3 h8 a3 3 0 0 1 3 3 V13" />
      <path d="M5 13 H23 v6 H5 Z" />
      <path d="M8 19 V25 M20 19 V25" />
    </svg>
  );
}
function IconDesk() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.3" aria-hidden="true">
      <path d="M3 11 H25" />
      <path d="M5 11 V23 M23 11 V23" />
      <path d="M3 8 H25 V11 H3 Z" />
    </svg>
  );
}
function IconStorage() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="currentColor" strokeWidth="1.3" aria-hidden="true">
      <rect x="5" y="3" width="18" height="22" />
      <path d="M5 12 H23 M5 18 H23" />
      <path d="M10 7 H13 M10 15 H13 M10 21 H13" />
    </svg>
  );
}

const ICON_REGISTRY = {
  check: IconCheck,
  shield: IconShield,
  handshake: IconHandshake,
  grid: IconGrid,
  seating: IconSeating,
  desk: IconDesk,
  storage: IconStorage,
};
function resolveIcon(key) {
  return ICON_REGISTRY[key] || IconCheck;
}

/* ===================================================================
   OECM_DEFAULTS — round-5 OECM page content, lifted to data shape.
   <Landing /> with no `data` prop renders byte-identical to round 5.
   =================================================================== */
const OECM_DEFAULTS = {
  crumbs: [
    { label: "Home", href: "/" },
    { label: "Services", href: "/pages/services" },
    { label: "OECM purchasing", current: true },
  ],
  headerCurrent: "services",

  hero: {
    eyebrow: "Service · OECM",
    h1: "Furnish your school, hospital, or council without re-tendering.",
    standfirst: "BBI is an OECM-approved supplier — Ontario's broader public sector can buy seating, desks, storage, and acoustics from us under existing OECM agreements. No RFP. No vendor onboarding. One quote, one PO, one invoice.",
    heroBadge: { show: true, label: "OECM vendor of record · pre-qualified" },
    primaryCta: { label: "Request a quote", href: "/pages/quote" },
    secondaryCta: { label: "Call 1-800-835-9565", href: "tel:18008359565" },
    media: {
      placeholderLabel: "Hero · 5:4 · BPS facility install",
      caption: "Halton DSB · 240 task chairs · OECM PO #4521",
    },
  },

  intro: {
    eyebrow: "What OECM means",
    h2: "You've already done the procurement. We honour it.",
    paragraphs: [
      "OECM (Ontario Education Collaborative Marketplace) negotiates pre-tendered agreements on behalf of the broader public sector — schools, colleges, universities, hospitals, municipalities, and not-for-profits. If your organization is OECM-eligible, you can buy from any approved supplier under those agreed terms without running your own RFP.",
      "BBI has held OECM vendor-of-record status on the office furniture category since 2019. That means our pricing, warranty terms, delivery windows, and product range are already vetted against OECM's procurement standards. You skip the tender. We skip the markup. Everyone keeps their afternoon.",
    ],
    inlineCta: { label: "Read the full agreement details →", href: "/pages/oecm-agreement" },
  },

  diffs: {
    eyebrow: "Why BBI",
    h2: "Four reasons OECM purchasers send us their POs.",
    items: [
      { num: "01", icon: "check",     label: "Pre-tendered pricing", sentence: "OECM-negotiated rates on the full BBI catalogue. No 'sharpened pencil' games — the price you see is the price agreed at the master-agreement level." },
      { num: "02", icon: "shield",    label: "No RFP needed",        sentence: "If you're OECM-eligible, your purchasing policy already lists us as compliant. Skip the 6-week tender; quote and PO move in days, not months." },
      { num: "03", icon: "handshake", label: "Single Ontario partner", sentence: "Ontario-owned since 1962, head office in Brantford. One account team owns your file from quote through warranty — no out-of-province handoffs." },
      { num: "04", icon: "grid",      label: "Full brand range",     sentence: "18 manufacturer lines under one OECM SKU set — ergoCentric, Keilhauer, Global, Teknion, and the rest. You buy the right chair, not the closest one." },
    ],
  },

  trustPhotos: {
    eyebrow: "Recent OECM installs",
    h2: "Three Ontario sites we shipped last year, all under existing OECM agreements.",
    items: [
      { key: "Education",  title: "Halton DSB · admin offices",        note: "240 task chairs · OECM PO · 2024" },
      { key: "Healthcare", title: "Brantford General · waiting",       note: "60 vinyl-grade lounge units · OECM PO · 2023" },
      { key: "Government", title: "City of Hamilton · council suites", note: "32 private offices fit-out · OECM PO · 2024" },
    ],
  },

  // pending Steve sign-off — OECM-specific stats (2019 / 340+ / 90+) need source confirmation
  proofStats: [
    { num: "2019", label: "OECM vendor since",  detail: "Office furniture category — re-qualified each contract cycle." },
    { num: "340+", label: "OECM POs delivered", detail: "Across 90+ Ontario school boards, hospitals, and municipalities since 2019." },
    { num: "1 day", label: "Quote turnaround", detail: "Most OECM line-item quotes return within one business day of intake." },
  ],

  crosslinks: {
    eyebrow: "Browse the catalogue",
    h2: "Start with the category, end with a PO.",
    items: [
      { label: "Seating",              meta: "120 models · OECM-eligible", href: "/collections/seating", icon: "seating" },
      { label: "Desks & workstations", meta: "Height-adjustable + fixed",  href: "/collections/desks",   icon: "desk" },
      { label: "Storage & filing",     meta: "Lateral · vertical · mobile", href: "/collections/storage", icon: "storage" },
    ],
  },

  oecmBar: {
    show: true,
    copy: "Pre-qualified procurement for Ontario's broader public sector — schools, hospitals, councils, colleges. Use existing OECM agreements without re-tendering.",
    cta: { label: "You're already here", href: "/pages/oecm", arrow: "↗" },
  },

  faqs: {
    eyebrow: "FAQ",
    h2: "Six questions OECM purchasers ask before sending the PO.",
    items: [
      { q: "Who's eligible to buy from BBI under OECM?",
        a: "Any OECM-eligible organization: Ontario school boards (K-12), publicly-assisted colleges and universities, hospitals and CCACs, municipalities and their agencies, broader-public-sector organizations, and not-for-profits in the social and education sectors. If you're not sure, OECM publishes the eligible-buyer list on their site, or call us and we'll confirm in five minutes." },
      { q: "Do I still need internal sign-off?",
        a: "Yes — your organization's purchasing policy still applies (signing limits, board approvals, etc.), but you skip the tender step. Most OECM buyers go quote → internal PO authorization → BBI PO. The 6–8 weeks normally spent issuing an RFP, evaluating bids, and writing a contract is what disappears." },
      { q: "Is the OECM price always the lowest?",
        a: "Honestly, not always — open-tender bids on a single high-volume SKU can occasionally beat the OECM rate. But once you factor in tender cost, evaluation time, and the risk of a non-compliant low bidder, OECM nets out cheaper on the vast majority of orders. For very large fit-outs we'll tell you directly if running a separate tender would save you money." },
      { q: "What's the warranty handling under OECM?",
        a: "Same as any BBI order — we file the manufacturer claim on your behalf and keep the chair (or desk, or panel) in service. ergoCentric mechanisms carry 12 years; most other lines are 10. Loaner chairs are available during repair. One service contact, Ontario-based." },
      { q: "How does delivery and install work?",
        a: "BBI's own crew handles delivery, assembly, levelling, and removal of old furniture — we don't subcontract logistics. After-hours and weekend installs are available for occupied spaces. W5-cleared installers for ministry and hospital sites." },
      { q: "Can I add non-OECM-eligible items to the same PO?",
        a: "Yes. We can split a single quote into the OECM-eligible portion (drawn against the master agreement) and any out-of-scope items handled under your normal procurement. You get one delivery, one install, one invoice — the procurement tracking just lists the two streams." },
    ],
  },

  closer: {
    eyebrow: "Quoting under OECM",
    h2: "Send us your wish list. We'll send back an OECM-line-item quote.",
    sub: "Floor plan, square footage, or a list of seat counts — any starting point works. One business day to a quote, one Ontario team end-to-end.",
    primaryCta: { label: "Request a quote", href: "/pages/quote" },
    trust: [
      { html: <><b>1 business day response</b> on every OECM quote — no minimums.</> },
      { html: <>Or call <a href="tel:18008359565">1-800-835-9565</a> · Mon–Fri 8–5 ET</> },
    ],
  },
};

/* ---------- breadcrumbs ----------------------------------------------- */
function LpBreadcrumbs({ items }) {
  return (
    <div className="lp-crumbs-band">
      <div className="lp-crumbs-band__inner">
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

/* ---------- HERO ------------------------------------------------------ */
function LpHero({ data }) {
  const { eyebrow, h1, standfirst, heroBadge, primaryCta, secondaryCta, media } = data;
  return (
    <section className="lp-hero" aria-label="Hero">
      <div className="lp-hero__inner">
        <div className="lp-hero__text">
          <p className="lp-hero__eyebrow bbi-mono">
            <span className="lp-hero__eyebrow-label">{eyebrow}</span>
          </p>
          {heroBadge && heroBadge.show && (
            <span className="lp-hero__badge">
              <span className="lp-hero__badge-dot" />
              {heroBadge.label}
            </span>
          )}
          <h1>{h1}</h1>
          <p className="lp-hero__standfirst">{standfirst}</p>
          <div className="lp-hero__cta-row">
            {primaryCta && (
              <a className="bbi-btn bbi-btn--primary bbi-btn--lg" href={primaryCta.href}>
                {primaryCta.label} <span className="arrow">→</span>
              </a>
            )}
            {secondaryCta && (
              <a className="bbi-btn bbi-btn--secondary bbi-btn--lg" href={secondaryCta.href}>
                {secondaryCta.label}
              </a>
            )}
          </div>
        </div>
        <div className="lp-hero__media" aria-hidden="true">
          <div className="lp-hero__media-placeholder">{media.placeholderLabel}</div>
          {media.caption && (
            <div className="lp-hero__caption">
              <span className="lp-hero__caption-dot" />
              <span>{media.caption}</span>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

/* ---------- INTRO (memo-style) --------------------------------------- */
function LpIntro({ data }) {
  const { eyebrow, h2, paragraphs, inlineCta } = data;
  return (
    <section className="lp-intro" aria-label="What this service means for you">
      <div className="lp-intro__inner">
        <p className="lp-intro__eyebrow bbi-mono">{eyebrow}</p>
        <h2>{h2}</h2>
        <div className="lp-intro__body">
          {paragraphs.map((p, i) => <p key={i}>{p}</p>)}
          {inlineCta && (
            <p>
              <a href={inlineCta.href}>{inlineCta.label}</a>
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

/* ---------- DIFFERENTIATORS (2×2 grid skinning .bbi-card) ------------ */
function LpDifferentiators({ data }) {
  const { eyebrow, h2, items } = data;
  return (
    <section className="lp-diff" aria-label="Why BBI">
      <div className="lp-diff__inner">
        <div className="lp-diff__head">
          <p className="lp-diff__eyebrow bbi-mono">{eyebrow}</p>
          <h2>{h2}</h2>
        </div>
        <div className="lp-diff__grid">
          {items.map((d) => {
            const Icon = resolveIcon(d.icon);
            return (
              <article key={d.num} className="bbi-card lp-diff-card">
                <span className="lp-diff-card__num">{d.num}</span>
                <span className="lp-diff-card__icon"><Icon /></span>
                <h3 className="lp-diff-card__label">
                  <span>{d.label}</span>
                </h3>
                <p className="lp-diff-card__sentence">{d.sentence}</p>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ---------- TRUST PHOTO ROW ------------------------------------------ */
function LpTrustRow({ data }) {
  const { eyebrow, h2, items } = data;
  return (
    <section className="lp-trust-row" aria-label="Recent installs">
      <div className="lp-trust-row__inner">
        <div className="lp-trust-row__head">
          <p className="lp-trust-row__eyebrow bbi-mono">{eyebrow}</p>
          <h2>{h2}</h2>
        </div>
        <div className="lp-trust-row__grid">
          {items.map((p) => (
            <figure key={p.title} className="lp-trust-row__cell">
              <div className="lp-trust-row__cell-placeholder">{p.key} · 4:3</div>
              <figcaption className="lp-trust-row__caption">
                <span className="lp-trust-row__caption-key">{p.key}</span>
                <span><b>{p.title}</b></span>
                <span style={{ color: "rgba(var(--background-rgb),0.78)" }}>{p.note}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- PROOF BAR ------------------------------------------------- */
function LpProofBar({ stats }) {
  return (
    <section className="lp-proof-bar" aria-label="Track record">
      <div className="lp-proof-bar__inner">
        {stats.map((s, i) => (
          <div key={i} className="lp-proof-bar__stat">
            <span className="lp-proof-bar__stat-num">{s.num}</span>
            <span className="lp-proof-bar__stat-label">{s.label}</span>
            <span className="lp-proof-bar__stat-detail">{s.detail}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

/* ---------- CROSS-LINKS strip (down to template 3) ------------------- */
function LpCrosslinks({ data }) {
  const { eyebrow, h2, items } = data;
  return (
    <section className="lp-crosslinks" aria-label="Browse the catalogue">
      <div className="lp-crosslinks__inner">
        <div className="lp-crosslinks__head">
          <div>
            <p className="lp-crosslinks__eyebrow bbi-mono">{eyebrow}</p>
            <h2>{h2}</h2>
          </div>
        </div>
        <div className="lp-crosslinks__grid">
          {items.map((c) => {
            const Icon = resolveIcon(c.icon);
            return (
              <a key={c.label} className="lp-crosslinks__tile" href={c.href}>
                <span className="lp-crosslinks__tile-icon"><Icon /></span>
                <span className="lp-crosslinks__tile-label">
                  <span className="lp-crosslinks__tile-name">{c.label}</span>
                  <span className="lp-crosslinks__tile-meta">{c.meta}</span>
                </span>
                <span className="lp-crosslinks__tile-arrow"><IconArrowRight /></span>
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ---------- OECM bar (reuses the locked Homepage pattern) ------------ */
function LpOECMBar({ data }) {
  return (
    <section className="hp-oecm" aria-label="OECM trust signal">
      <div className="bbi-container hp-oecm__inner">
        <div className="hp-oecm__lead">
          <span className="bbi-badge bbi-badge--oecm">
            <span className="dot" />
            OECM vendor of record
          </span>
          <p className="hp-oecm__copy">{data.copy}</p>
        </div>
        <div className="hp-oecm__meta">
          <a className="bbi-btn bbi-btn--tertiary" href={data.cta.href}>
            <span className="label">{data.cta.label}</span>
            <span className="arrow">{data.cta.arrow || "→"}</span>
          </a>
        </div>
      </div>
    </section>
  );
}

/* ---------- FAQ accordion -------------------------------------------- */
function LpFAQItem({ idx, q, a, isOpen, onToggle }) {
  const num = String(idx + 1).padStart(2, "0");
  return (
    <div className={"lp-faq__item" + (isOpen ? " lp-faq__item--open" : "")}>
      <button className="lp-faq__trigger" aria-expanded={isOpen} onClick={onToggle}>
        <span className="lp-faq__trigger-num">{num}</span>
        <span>{q}</span>
        <span className="lp-faq__chevron"><IconChevronDown /></span>
      </button>
      {isOpen && (
        <div className="lp-faq__answer">
          <p>{a}</p>
        </div>
      )}
    </div>
  );
}

function LpFAQ({ data }) {
  const [open, setOpen] = useState(0);
  const { eyebrow, h2, items } = data;
  return (
    <section className="lp-faq" aria-label="Frequently asked questions">
      <div className="lp-faq__inner">
        <div className="lp-faq__head">
          <p className="lp-faq__eyebrow bbi-mono">{eyebrow}</p>
          <h2>{h2}</h2>
        </div>
        <div className="lp-faq__list">
          {items.map((f, i) => (
            <LpFAQItem
              key={i}
              idx={i}
              q={f.q}
              a={f.a}
              isOpen={open === i}
              onToggle={() => setOpen(open === i ? -1 : i)}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- CTA closer (reuses .bbi-cta-section verbatim) ------------ */
function LpCloser({ data }) {
  return (
    <section className="bbi-cta-section scheme-inverse">
      <div className="bbi-cta-section__inner">
        <div>
          <p className="bbi-cta-section__eyebrow">{data.eyebrow}</p>
          <h2 className="bbi-cta-section__heading">{data.h2}</h2>
          <p className="bbi-cta-section__sub">{data.sub}</p>
        </div>
        <div className="bbi-cta-section__actions">
          <a className="bbi-btn bbi-btn--primary bbi-btn--lg" href={data.primaryCta.href}>
            {data.primaryCta.label} <span className="arrow">→</span>
          </a>
          {data.trust && data.trust.map((t, i) => (
            <div key={i} className="bbi-cta-section__trust">
              <span className="dot" />
              <span>{t.html}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------- page composition ----------------------------------------- */
function Landing({ mobile = false, data = OECM_DEFAULTS }) {
  const showTrust       = data.trustPhotos && data.trustPhotos.items && data.trustPhotos.items.length > 0;
  const showProof       = !!(data.proofStats && data.proofStats.length > 0);
  const showCrosslinks  = data.crosslinks && data.crosslinks.items && data.crosslinks.items.length > 0;
  const showOECMBar     = !!(data.oecmBar && data.oecmBar.show !== false);

  return (
    <div className={"scheme-default lp-page" + (mobile ? " lp-page--mobile" : "")}>
      {mobile ? <_HeaderMobile /> : <_HeaderDesktop current={data.headerCurrent} />}
      <LpBreadcrumbs items={data.crumbs} />
      <LpHero data={data.hero} />
      <LpIntro data={data.intro} />
      <LpDifferentiators data={data.diffs} />
      {showTrust       && <LpTrustRow data={data.trustPhotos} />}
      {showProof       && <LpProofBar stats={data.proofStats} />}
      {showCrosslinks  && <LpCrosslinks data={data.crosslinks} />}
      {showOECMBar     && <LpOECMBar data={data.oecmBar} />}
      <LpFAQ data={data.faqs} />
      <LpCloser data={data.closer} />
      <_Footer mobile={mobile} />
    </div>
  );
}

window.Landing = Landing;
window.LANDING_OECM_DEFAULTS = OECM_DEFAULTS;
