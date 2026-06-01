export const meta = {
  name: 'b4s6-draft-enrichment',
  description: 'PHASE-A-BLOCK-4-SESSION-6: auto-source + draft 13-field specs + body/SEO/tags for 26 Global-family PDPs (warranty SOURCE-OR-EMPTY)',
  phases: [{ title: 'Draft', detail: 'one agent per product: WebSearch -> WebFetch source -> extract -> draft (warranty source-or-empty)' }],
}

const TS = "20260601-114715"
// Briefs INLINED as a literal (args plumbing proved unreliable in Session 5).
const briefs = [{"handle":"marche-guest-chair","title":"Marche guest chair","sku":"GLO-8621","model_code":"8621","price":"670.64","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-marche-guest-chair-pre-20260601-114715.json"},{"handle":"guest-chair-6960-moda","title":"Guest chair 6960 moda","sku":"GLO 6960 Cloud","model_code":"6960","price":"449.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-guest-chair-6960-moda-pre-20260601-114715.json"},{"handle":"rebound-armchair-upholstered-seat-r5apug","title":"Rebound armchair, upholstered seat (r5apug)","sku":"GLB-R5APUG","model_code":"R5APUG","price":"389.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-rebound-armchair-upholstered-seat-r5apug-pre-20260601-114715.json"},{"handle":"rebound-armchair-polypropylene-seat-1","title":"Rebound armchair, polypropylene seat","sku":"GLB-R5APPG","model_code":"R5APPG","price":"359.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-rebound-armchair-polypropylene-seat-1-pre-20260601-114715.json"},{"handle":"stream-armchair-polypropylene-seat-back-2075app-1","title":"Stream armchair, polypropylene seat & back (2075app)","sku":"GLO-2075APP","model_code":"2075APP","price":"298.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-stream-armchair-polypropylene-seat-back-2075app-1-pre-20260601-114715.json"},{"handle":"stream-armless-chair-polypropylene-seat-back-2075app","title":"Stream armless chair, polypropylene seat & back (2075A, no arms)","sku":"GLB-2075APP","model_code":"2075A","price":"299.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-stream-armless-chair-polypropylene-seat-back-2075app-pre-20260601-114715.json"},{"handle":"the-twilight-armchair-wood-veneer-back-2198ws","title":"The twilight armchair, wood veneer back (2198ws)","sku":"GLO-2198","model_code":"2198WS","price":"329.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-the-twilight-armchair-wood-veneer-back-2198ws-pre-20260601-114715.json"},{"handle":"solo-gues-chair","title":"Solo guest chair (5225SSU)","sku":"GLO5225SSU","model_code":"5225SSU","price":"218.02","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-solo-gues-chair-pre-20260601-114715.json"},{"handle":"sonic-armchair-upholstered-seat-polypropylene-back-casters-6574","title":"Sonic armchair, upholstered seat & polypropylene back, casters (6574)","sku":"GLB6574","model_code":"6574","price":"296.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-sonic-armchair-upholstered-seat-polypropylene-back-casters-6574-pre-20260601-114715.json"},{"handle":"rambler-ottoman-8-shape-size-options","title":"Rambler ottoman (8 shape & size options)","sku":"GLB-RA2222SQ","model_code":"RA2222SQ","price":"439.99","product_type":"","cluster":"waiting-room-seating","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-rambler-ottoman-8-shape-size-options-pre-20260601-114715.json"},{"handle":"craft-round-20-unit","title":"Craft round 20\" unit","sku":"GLB-MVL13007","model_code":"MVL13007","price":"269.99","product_type":"","cluster":"boardroom","sub_brand":"Global","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-craft-round-20-unit-pre-20260601-114715.json"},{"handle":"craft-wedge-unit","title":"Craft wedge unit","sku":"GLB-MVL13009","model_code":"MVL13009","price":"229.99","product_type":"","cluster":"boardroom","sub_brand":"Global","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-craft-wedge-unit-pre-20260601-114715.json"},{"handle":"craft-wedge-overtable-chrome-leg-1","title":"Craft wedge overtable, chrome leg","sku":"GLBMVL13022ACJ","model_code":"MVL13022ACJ","price":"288.00","product_type":"","cluster":"boardroom","sub_brand":"Global","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-craft-wedge-overtable-chrome-leg-1-pre-20260601-114715.json"},{"handle":"work-table-at","title":"Work table (AT6030)","sku":"GLBAT6030","model_code":"AT6030","price":"349.99","product_type":"","cluster":"boardroom","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-work-table-at-pre-20260601-114715.json"},{"handle":"table-18x28","title":"Table 18\"x28\" (occasional/training table; resolve SKU DTS1828 vs title)","sku":"GLBDTS1828PGIVC","model_code":"DTS1828P","price":"354.59","product_type":"","cluster":"occasional-table-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-table-18x28-pre-20260601-114715.json"},{"handle":"table-29-x-28-3","title":"Table 29\"x28\" (occasional/training table; resolve SKU DTS1828 vs title 29x28 conflict)","sku":"GLBDTS1828PBLK","model_code":"DTS1828P","price":"350.19","product_type":"","cluster":"occasional-table-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-table-29-x-28-3-pre-20260601-114715.json"},{"handle":"luray-executive-chair","title":"Luray executive chair","sku":"GLO-64612","model_code":"64612","price":"899.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-luray-executive-chair-pre-20260601-114715.json"},{"handle":"sidero-1","title":"Sidero (GC6922HB)","sku":"GLB-(GC6922HB)","model_code":"GC6922HB","price":"939.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-sidero-1-pre-20260601-114715.json"},{"handle":"sora-mesh-back-chair-6941-6942","title":"Sora mesh back chair (6941/6942)","sku":"GLB6941","model_code":"6941","price":"799.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-sora-mesh-back-chair-6941-6942-pre-20260601-114715.json"},{"handle":"global-accord-mesh-back-tilter","title":"Global Accord mesh back tilter (2676-4)","sku":"GLB 2676-4","model_code":"2676-4","price":"749.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-global-accord-mesh-back-tilter-pre-20260601-114715.json"},{"handle":"basics-comfort-time-ultra-multi-tilter-big-tall-with-headrest","title":"Basics Comfort-Time Ultra multi-tilter, big & tall, with headrest","sku":"GLB BAOMVL13042G5","model_code":"MVL13042","price":"794.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Basics","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-basics-comfort-time-ultra-multi-tilter-big-tall-with-headrest-pre-20260601-114715.json"},{"handle":"echo-medium-back-multi-tilter-3671-3-1","title":"Echo medium back multi-tilter (3671-3)","sku":"GLB-36713","model_code":"3671-3","price":"650.00","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-echo-medium-back-multi-tilter-3671-3-1-pre-20260601-114715.json"},{"handle":"basics-elora-chair-high-back-black-leather-luxhide-mvl1893upu30bl20","title":"Basics Elora chair, high back, black leather (Luxhide) (MVL1893)","sku":"GLB-MVL1893U","model_code":"MVL1893","price":"649.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Basics","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-basics-elora-chair-high-back-black-leather-luxhide-mvl1893upu30bl20-pre-20260601-114715.json"},{"handle":"chevron-ultra-medium-back-multi-tilter-chair","title":"Chevron Ultra medium back multi-tilter chair (BAO1121-3)","sku":"GLB-BAO1121-3G5","model_code":"BAO1121-3","price":"599.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"GFG-PREMIUM","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-chevron-ultra-medium-back-multi-tilter-chair-pre-20260601-114715.json"},{"handle":"adapt-high-back-synchro-tilter-mvl11724-mvl11725","title":"Adapt high back synchro-tilter (MVL11724 / MVL11725)","sku":"GLO-MVL11724","model_code":"MVL11724","price":"399.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-adapt-high-back-synchro-tilter-mvl11724-mvl11725-pre-20260601-114715.json"},{"handle":"yoho-armless-drafting-task-chair-stool","title":"Yoho armless drafting task chair / stool (MVL2796)","sku":"GLO-MVL2796","model_code":"MVL2796","price":"369.99","product_type":"","cluster":"exec-seating-descriptive","sub_brand":"Global","warranty_basis":"OTG-VALUE","source_domains":["globalfurnituregroup.com","officestogo.com"],"snapshot":"data/backups/session-6-yoho-armless-drafting-task-chair-stool-pre-20260601-114715.json"}]
log(`Drafting ${briefs.length} products (warranty SOURCE-OR-EMPTY)`)

const DRAFT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['handle','source_url_used','auto_source','boilerplate_detected','manufacturer','product_line','model_codes','dimensions','weight','weight_capacity','materials','finishes_available','key_features','certifications','warranty','warranty_source_url','country_of_manufacture','who_its_for','body_html','seo_title','seo_description','tags','priority_keywords_landed','flags'],
  properties: {
    handle: { type: 'string' },
    source_url_used: { type: 'string' },
    auto_source: { type: 'string', enum: ['success','partial','fail'] },
    source_notes: { type: 'string' },
    boilerplate_detected: { type: 'boolean' },
    manufacturer: { type: 'string' },
    product_line: { type: 'string' },
    model_codes: { type: 'array', items: { type: 'string' } },
    dimensions: { type: 'string' },
    weight: { type: 'string' },
    weight_capacity: { type: 'string' },
    materials: { type: 'array', items: { type: 'string' } },
    finishes_available: { type: 'array', items: { type: 'string' } },
    key_features: { type: 'array', items: { type: 'string' } },
    certifications: { type: 'array', items: { type: 'string' } },
    warranty: { type: 'string' },
    warranty_source_url: { type: 'string' },
    country_of_manufacture: { type: 'string' },
    who_its_for: { type: 'string' },
    body_html: { type: 'string' },
    seo_title: { type: 'string' },
    seo_description: { type: 'string' },
    tags: { type: 'array', items: { type: 'string' } },
    priority_keywords_landed: {
      type: 'object', additionalProperties: false,
      required: ['title','meta','body'],
      properties: {
        title: { type: 'array', items: { type: 'string' } },
        meta: { type: 'array', items: { type: 'string' } },
        body: { type: 'array', items: { type: 'string' } },
      },
    },
    flags: { type: 'array', items: { type: 'string' } },
  },
}

// ============ CONTROLLING WARRANTY MATRICES (verbatim, fetched Phase 1 2026-06-01) ============
const WARRANTY = `
=== WARRANTY: SOURCE-OR-EMPTY. NEVER DEFAULT. (Session 5 over-stamped "Limited Lifetime" — do not repeat.) ===
The reference file manufacturer-defaults.yaml hardcodes GFG warranty = "Limited Lifetime Warranty".
IGNORE that default entirely. You must SOURCE the precise warranty term for THIS product from a
manufacturer warranty/product page. If you cannot confirm a term from a real source, set warranty="" and
add flag "warr-unconfirmed". Put the URL you confirmed the warranty from in warranty_source_url
(or "none"). Do NOT assert any term you did not source.

Two controlling matrices. Use the one matching this product's warranty_basis:

--- OTG-VALUE basis (Offices To Go / value catalog — MVL value line, Basics, OTG/Newland prefixes) ---
Source: officestogo.com/warranty. NO LIFETIME ANYWHERE in this matrix.
  • Non-moving parts (laminate table tops, frames, structure): 5 years
  • Moving parts (drawers, slides, leveling glides, locks): 2 years
  • Gas cylinders, tilt mechanisms, other moving parts: 2 years
  • Upholstery materials and foam: 2 years
  • Task light / lamp / monitor arm / power modules: 2 years
  • Electric height-adjustable base motors/controllers: 5 years
  • Seating basis: 8-hour single shift, users up to 275 lbs.
  -> A VALUE-LINE CHAIR is typically "2-year" (upholstery/foam/mechanism). A VALUE LAMINATE TABLE is
     typically "5-year" (non-moving top). CONFIRM the exact figure on the product/series page; if the
     page states a specific term use it; if unconfirmable -> warranty="" + flag "warr-unconfirmed".
     NEVER write lifetime for an OTG-VALUE item.

--- GFG-PREMIUM basis (Global parent premium catalog — bare-numeric model codes) ---
Source: globalfurnituregroup.com/warranty.
  • General seating: frame & components "for the life of the product" (limited lifetime); control
    mechanisms 12 years; UPHOLSTERY / FOAM / MESH / FABRIC = 5 years.
  • Heavy-duty seating: components 12 years; upholstery/foam 5 years.
  • Laminate tables & casegoods: lifetime; electrical devices & moving parts 5 years.
  • Metal filing/storage: lifetime; keyless locks 2 years.
  • Panel systems: lifetime; panel textiles/electrical/task lights 5 years.
  -> A PREMIUM SEAT may carry "limited lifetime on frame and mechanism, 5 years on upholstery, foam and
     mesh" — but ONLY assert lifetime if you SOURCE it for this product. Polypropylene stacking/guest
     chairs and budget seating frequently are NOT lifetime — confirm. If you cannot confirm -> warranty=""
     + flag "warr-unconfirmed". When you do write lifetime, include the standard caveat phrasing
     "...with 5 years on upholstery, foam and mesh."

=== WARRANTY BODY SYNC + STRAY-FIGURE SCAN (hard) ===
- The warranty sentence in body_html MUST match the warranty metafield exactly (same term/years).
- Scan ALL feature/spec/body text you write for stray numeric warranty figures ("2 years", "15-year",
  "lifetime", "5-year") that do NOT match the metafield term, and remove/correct them. Session 5 shipped
  leftover mismatched figures — do not.
`

const RULES = `
You are drafting ONE Brant Business Interiors (BBI) Shopify PDP enrichment. BBI is a Canadian B2B
office-furniture dealer serving institutional buyers (school boards, hospitals, municipalities) and
private businesses. Output is consumed by an automated review step — return ONLY the structured object.

FIRST: load tools via ToolSearch (query "select:WebSearch,WebFetch,Read"), then use them.
You MAY Read the product snapshot JSON (path given) for the current title/body/sku.

=== AUTO-SOURCE (before drafting) ===
1. WebSearch for the product on its PRIMARY domain using model code + product name
   (e.g. '"{model_code}" {title} site:{primary_domain}'). Try the fallback domain if primary misses.
2. WebFetch the best manufacturer product/series page. Extract: exact model code(s), dimensions
   (overall W x D x H; seat-height range for chairs), weight, weight capacity, materials, finishes/
   colour options, key features, certifications, warranty, country of manufacture.
3. Set auto_source: "success" (product page + specs), "partial" (series/family page or limited specs),
   "fail" (no usable source — draft conservatively from snapshot only). Put the actual URL in
   source_url_used (or "none").

=== MANUFACTURER (all 26 are Global Furniture Group family) ===
- manufacturer = "Global Furniture Group" ALWAYS (sub-brand house rule: Basics / Offices To Go / OTG /
  ObusForme / Global series all resolve to GFG as manufacturer). Sub-brand/series -> product_line
  (e.g. "Global", "Basics", "Offices To Go", or the series name like "Craft", "Rebound", "Stream").
- country_of_manufacture = "Canada" (locked for GFG) — but if a specific source contradicts, follow source + flag.

${WARRANTY}

=== CERTIFICATIONS (per-product source verification with citation) ===
- DO NOT auto-apply GREENGUARD. Only include a cert you CONFIRMED on the source page. ANSI/BIFMA is often
  confirmable at the series page. SEATING especially: GREENGUARD frequently NOT documented — extra scrutiny.
- If you cannot confirm any cert: certifications=[] and add flag "certs-unconfirmed". Put the citation in
  source_notes when you do apply a cert.

=== 13 specs.* FIELDS (exact data shapes) ===
manufacturer(single line) | product_line(single line) | model_codes(array) | dimensions(single line,
seat-height range inline for chairs) | weight(single line e.g. "46 lbs") | weight_capacity(single line
e.g. "300 lbs") | materials(array, one per line) | finishes_available(array) | key_features(array) |
certifications(array) | warranty(single line) | country_of_manufacture(single line) | who_its_for(single
line audience sentence). If a value is genuinely unknown after sourcing, use "" and add a flag — do NOT
invent specs. Single-line fields must contain NO newline characters.

=== body_html ===
- Theme splits at FIRST <h3>: text before first <h3> = lede (above spec table); <h3> sections below.
  Structure: 1 lede <p> (2-3 sentences, design-forward, institutional-aware), then <h3>Features</h3> +
  <ul>, optionally <h3>Specifications</h3> short prose, then a closing <p> with a quote CTA. Valid clean
  HTML. Preserve genuinely useful content from current body but rewrite to BBI voice.
- boilerplate_detected=true if CURRENT body (snapshot) is generic filler/stub; false if real copy.

=== BBI VOICE RULES (hard) ===
- NEVER write the literal "BBI" in customer copy. Always full "Brant Business Interiors".
- Design-forward, confident, concise. Benefit hook first, not a spec dump.
- Trust anchors where natural: family-owned since 1964; 296 George St N, Peterborough ON; OECM-eligible
  supplier (Ontario institutional buyers can purchase without open tender) — OECM as trust signal, not hero.
  Canadian-owned / Made in Canada is genuine for these Canada-made GFG products — fine to mention.
- CTA microcopy: "Request a Quote"; phone "Call 1-800-835-9565". Include a quote CTA line in closing <p>.
- No invented stats, no fabricated lead times, no Indigenous-segment marketing.

=== PRIORITY KEYWORDS (v1 LOCKED clusters only — integrate ONLY where genuinely fitting; no forced fit) ===
Brand terms (Global/OTG/Newland/Basics) are NOT keyword targets — descriptive use only.
This product's assigned cluster is given below. Locked bank:
- waiting-room-seating (guest/lounge/reception-area seating): "office chairs for waiting room",
  "waiting room chairs canada". Apply ONLY if genuinely guest/waiting seating.
- boardroom (conference/meeting tables): "boardroom table", "conference table", "wood boardroom table",
  "conference table canada". Apply ONLY to genuine conference/meeting tables.
- executive-desks (desks only — NOT chairs): "executive desk", "executive office desk", "l-shaped
  executive desk", "executive desk canada", "wood executive desk".
- exec-seating-descriptive (task/executive chairs): NO locked cluster. Use DESCRIPTIVE terms in
  title+meta only — "ergonomic office chair", "task chair", "executive chair". Land ZERO locked priority
  keywords (correct, not a failure).
- occasional-table-descriptive (small occasional/training tables — NOT conference tables): NO forced
  conference keyword. Descriptive only ("office table", "occasional table"). Land ZERO locked keywords.
  ALSO: resolve the SKU-vs-title dimension conflict from the source — state the real dimensions; flag
  "dims-conflict" if the source can't resolve it.
Record exactly which keywords you placed in title / meta / body in priority_keywords_landed (locked terms
only — do not list descriptive words as landed priority keywords).

=== GENERATION-TIME CONSTRAINTS (self-check BEFORE emit — no post-hoc trim) ===
- seo_title: <=60 chars INCLUDING the suffix " | Brant Business Interiors". If 60 is tight, DROP the
  suffix rather than truncate the product name. Do NOT use the long page-level suffix.
- seo_description: <=160 chars, institutional-buyer hook, natural keyword if one fits.
- No double-period artifacts (".."), no literal "BBI", no newlines in any single-line field.

=== TAGS ===
Start from snapshot's current tags; ADD (don't remove unless clearly wrong): "brand:global-furniture-group",
a "type:{slug}" tag (type:waiting-room-seating, type:lounge-seating, type:guest-seating, type:task-chair,
type:conference-table, type:table, type:ottoman, etc.), keep "oecm-eligible" if present. Return FULL final list.
`

phase('Draft')
const drafts = await parallel(briefs.map(b => () =>
  agent(
    RULES + "\n\n=== THIS PRODUCT ===\n" +
    "handle: " + b.handle + "\n" +
    "title (current): " + b.title + "\n" +
    "variant SKU: " + b.sku + "\n" +
    "model code: " + b.model_code + "\n" +
    "price: $" + b.price + "\n" +
    "ASSIGNED CLUSTER: " + b.cluster + "\n" +
    "WARRANTY BASIS: " + b.warranty_basis + " (use the matching matrix above; SOURCE-OR-EMPTY)\n" +
    "sub-brand routing: " + b.sub_brand + " -> product_line\n" +
    "PRIMARY source domain: " + b.source_domains[0] + " ; FALLBACK: " + (b.source_domains[1] || "none") + "\n" +
    "snapshot path (you may Read it): " + b.snapshot + "\n\n" +
    "Return the structured draft object for this product.",
    { label: b.handle.slice(0, 40), phase: 'Draft', schema: DRAFT_SCHEMA, agentType: 'general-purpose' }
  ).then(r => r).catch(e => ({ handle: b.handle, _error: String(e) }))
))

const ok = drafts.filter(d => d && !d._error)
const failed = drafts.filter(d => !d || d._error)
log(`Drafts complete: ${ok.length} ok, ${failed.length} errored`)
return { ts: TS, count: ok.length, drafts: ok, errored: failed.map(f => f && f.handle) }
