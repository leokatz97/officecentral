export const meta = {
  name: 'b4s5-draft-enrichment',
  description: 'PHASE-A-BLOCK-4-SESSION-5: auto-source + draft 13-field specs + body/SEO/tags for 27 Global-family PDPs',
  phases: [{ title: 'Draft', detail: 'one agent per product: WebSearch -> WebFetch source -> extract -> draft' }],
}

const TS = "20260601-104429"
const briefs = [{"handle": "height-adjustable-rectangular-table-2-legs-nl48243qht", "title": "Height adjustable rectangular table - 2 legs", "sku": "GLBNL48243QHT", "model_code": "NL48243QHT", "price": "769.99", "product_type": "", "sub_brand": "Newland (Offices To Go line)", "source_domains": ["officestogo.com", "ugoburo.ca"], "snapshot": "data/backups/session-5-height-adjustable-rectangular-table-2-legs-nl48243qht-pre-20260601-104429.json"}, {"handle": "round-table-x-base-5", "title": "Round table - x-base", "sku": "GLBNL36RX", "model_code": "NL36RX", "price": "349.99", "product_type": "", "sub_brand": "Newland (Offices To Go line)", "source_domains": ["officestogo.com", "ugoburo.ca"], "snapshot": "data/backups/session-5-round-table-x-base-5-pre-20260601-104429.json"}, {"handle": "u-shaped-suite-with-table-desk-72w-x-96d", "title": "\"u\" shaped suite with table desk - 72\"w x 96\"d \u2014 96\"", "sku": "GLO-NLP229", "model_code": "NLP229", "price": "1857.60", "product_type": "", "sub_brand": "Newland (Offices To Go line)", "source_domains": ["officestogo.com", "ugoburo.ca"], "snapshot": "data/backups/session-5-u-shaped-suite-with-table-desk-72w-x-96d-pre-20260601-104429.json"}, {"handle": "management-l-shaped-suite-66w-x-72d", "title": "Management \"l\" shaped suite - 66\"w x 72\"d \u2014 72\"", "sku": "GLB NLP234", "model_code": "NLP234", "price": "1649.99", "product_type": "", "sub_brand": "Newland (Offices To Go line)", "source_domains": ["officestogo.com", "ugoburo.ca"], "snapshot": "data/backups/session-5-management-l-shaped-suite-66w-x-72d-pre-20260601-104429.json"}, {"handle": "two-drawer-lateral-file-nl3624lft", "title": "Two drawer lateral file \u2014 NL3624LFT", "sku": "GLBNL3624LFT", "model_code": "NL3624LFT", "price": "647.73", "product_type": "", "sub_brand": "Newland (Offices To Go line)", "source_domains": ["officestogo.com", "ugoburo.ca"], "snapshot": "data/backups/session-5-two-drawer-lateral-file-nl3624lft-pre-20260601-104429.json"}, {"handle": "lumi-high-back-synchro-tilter-chair", "title": "Lumi | high back synchro-tilter chair", "sku": "GLO-OTG11357", "model_code": "OTG11357", "price": "369.99", "product_type": "", "sub_brand": "Offices To Go", "source_domains": ["officestogo.com", "globalfurnituregroup.com"], "snapshot": "data/backups/session-5-lumi-high-back-synchro-tilter-chair-pre-20260601-104429.json"}, {"handle": "flip-top-table-48-x-24", "title": "Flip-top table \u2014 48\" x 24\"", "sku": "GLBML4824FTASN", "model_code": "ML4824FTASN", "price": "459.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-flip-top-table-48-x-24-pre-20260601-104429.json"}, {"handle": "workstation-96-x-50-x-29-4-person-station", "title": "Workstation - 96\" x 50\" x 29\" (4 person station) \u2014 96\" x 50\" x 29\"", "sku": "GLBMLP496ASN", "model_code": "MLP496ASN", "price": "2099.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-workstation-96-x-50-x-29-4-person-station-pre-20260601-104429.json"}, {"handle": "coffee-table-33-x-33-15-height-2", "title": "Coffee table 33\" x 33\" 15\" height \u2014 33\" x 33\"", "sku": "GLB7889", "model_code": "7889", "price": "907.34", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-coffee-table-33-x-33-15-height-2-pre-20260601-104429.json"}, {"handle": "coffee-table-seating", "title": "Coffee table & seating", "sku": "GLO-ML35SCDK", "model_code": "ML35SCDK", "price": "288.00", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-coffee-table-seating-pre-20260601-104429.json"}, {"handle": "craft-cube-square-unit", "title": "Craft cube | square unit", "sku": "GLB-MVL13012", "model_code": "MVL13012", "price": "229.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-craft-cube-square-unit-pre-20260601-104429.json"}, {"handle": "craft-curve-120-degree-unit-2", "title": "Craft | curve-120 degree unit", "sku": "GLB-MVL13010", "model_code": "MVL13010", "price": "399.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-craft-curve-120-degree-unit-2-pre-20260601-104429.json"}, {"handle": "craft-rectangle-unit-1", "title": "Craft | rectangle unit", "sku": "GLB-MVL13011", "model_code": "MVL13011", "price": "319.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-craft-rectangle-unit-1-pre-20260601-104429.json"}, {"handle": "half-round-40-unit", "title": "Half round 40\" unit \u2014 40\"", "sku": "GLB-MVL13008", "model_code": "MVL13008", "price": "329.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-half-round-40-unit-pre-20260601-104429.json"}, {"handle": "loover-high-back-synchro-tilter", "title": "Loover high back synchro tilter", "sku": "GLB-26618", "model_code": "26618", "price": "649.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-loover-high-back-synchro-tilter-pre-20260601-104429.json"}, {"handle": "fame-high-back-weight-sensing-synchro-tilter", "title": "Fame | High Back Weight Sensing Synchro-Tilter", "sku": "GLB-OTG11401", "model_code": "OTG11401", "price": "399.99", "product_type": "", "sub_brand": "Offices To Go", "source_domains": ["officestogo.com", "globalfurnituregroup.com"], "snapshot": "data/backups/session-5-fame-high-back-weight-sensing-synchro-tilter-pre-20260601-104429.json"}, {"handle": "tl-high-back-multi-tilter", "title": "Tl | high back multi-tilter", "sku": "MVL6070HA", "model_code": "MVL6070HA", "price": "649.00", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-tl-high-back-multi-tilter-pre-20260601-104429.json"}, {"handle": "altona-high-back-leather-tilter", "title": "Altona | high back leather tilter", "sku": "OTG11616B", "model_code": "OTG11616B", "price": "249.99", "product_type": "", "sub_brand": "Offices To Go", "source_domains": ["officestogo.com", "globalfurnituregroup.com"], "snapshot": "data/backups/session-5-altona-high-back-leather-tilter-pre-20260601-104429.json"}, {"handle": "granada-deluxe-high-back-multi-tilter-1170-3-2", "title": "Granada deluxe high back multi-tilter (1170-3) \u2014 1170-3", "sku": "GLB11703", "model_code": "11703", "price": "669.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-granada-deluxe-high-back-multi-tilter-1170-3-2-pre-20260601-104429.json"}, {"handle": "zim-synchro-tilter-chair-high-back-mesh-mesh-back-black", "title": "Zim synchro-tilter chair high back mesh mesh back", "sku": "OTG11351AB", "model_code": "OTG11351AB", "price": "399.99", "product_type": "", "sub_brand": "Offices To Go", "source_domains": ["officestogo.com", "globalfurnituregroup.com"], "snapshot": "data/backups/session-5-zim-synchro-tilter-chair-high-back-mesh-mesh-back-black-pre-20260601-104429.json"}, {"handle": "danio-armless-height-adjustable-task-stool", "title": "Danio | armless height adjustable task stool", "sku": "MVL2723", "model_code": "MVL2723", "price": "259.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-danio-armless-height-adjustable-task-stool-pre-20260601-104429.json"}, {"handle": "kate-medium-back-armchair-2813", "title": "Kate medium back armchair (2813) \u2014 2813", "sku": "GLO-2813", "model_code": "2813", "price": "730.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-kate-medium-back-armchair-2813-pre-20260601-104429.json"}, {"handle": "echo-3670-3-task-chair", "title": "Echo 3670-3 task chair", "sku": "GLB36703", "model_code": "36703", "price": "699.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-echo-3670-3-task-chair-pre-20260601-104429.json"}, {"handle": "quick-assembly-electric-height-adjustable-base-2-legs", "title": "Quick assembly electric height adjustable base - 2 legs", "sku": "GLBMLIR30B BLK", "model_code": "MLIR30B", "price": "699.99", "product_type": "Heights adjustable base", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-quick-assembly-electric-height-adjustable-base-2-legs-pre-20260601-104429.json"}, {"handle": "privacy-desk-top-dividers", "title": "Privacy desk top dividers", "sku": "GLB-PT9PP3013-1", "model_code": "PT9PP3013-1", "price": "150.00", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-privacy-desk-top-dividers-pre-20260601-104429.json"}, {"handle": "desk-top-divider-divide", "title": "Desk top divider divide", "sku": "GLO-DGP1224TUN-2@DPOST12TUN", "model_code": "DGP1224TUN-2", "price": "280.00", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-desk-top-divider-divide-pre-20260601-104429.json"}, {"handle": "part-time-task-chair-with-height-adjustable-arms-mvl", "title": "Part-Time | Task Chair with Height Adjustable Arms MVL", "sku": "GLB-MVL2846", "model_code": "MVL2846", "price": "279.99", "product_type": "", "sub_brand": "Global (parent catalog)", "source_domains": ["globalfurnituregroup.com", "officestogo.com"], "snapshot": "data/backups/session-5-part-time-task-chair-with-height-adjustable-arms-mvl-pre-20260601-104429.json"}]
log(`Drafting ${briefs.length} products`)

const DRAFT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['handle','source_url_used','auto_source','boilerplate_detected','manufacturer','product_line','model_codes','dimensions','weight','weight_capacity','materials','finishes_available','key_features','certifications','warranty','country_of_manufacture','who_its_for','body_html','seo_title','seo_description','tags','priority_keywords_landed','flags'],
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

const RULES = `
You are drafting one Brant Business Interiors (BBI) Shopify PDP enrichment. BBI is a Canadian B2B
office-furniture dealer serving institutional buyers (school boards, hospitals, municipalities) and
private businesses. Output is consumed by an automated review step - return ONLY the structured object.

FIRST: load tools you need via ToolSearch (query "select:WebSearch,WebFetch,Read"), then use them.
You MAY Read the product snapshot JSON (path given) for the current title/body/sku.

=== AUTO-SOURCE (do this before drafting) ===
1. WebSearch for the product on its PRIMARY source domain using the model code + product name
   (e.g. '"{model_code}" {title} site:{primary_domain}'). Try the fallback domain if primary misses.
2. WebFetch the best manufacturer product/series page. Extract: exact model code(s), dimensions
   (overall W x D x H, seat-height range for chairs), weight, weight capacity, materials, finishes/
   colour options, key features, certifications, warranty, country of manufacture.
3. Set auto_source: "success" (found product page, specs extracted), "partial" (found series/family
   page or limited specs), or "fail" (no usable source - draft conservatively from snapshot only).
   Always put the actual URL you used in source_url_used (or "none" if fail).

=== MANUFACTURER DEFAULTS (Global Furniture Group family - ALL 27 are GFG) ===
- manufacturer = "Global Furniture Group" ALWAYS (sub-brand house rule: Newland / Offices To Go / OTG /
  Basics / ObusForme all resolve to GFG as manufacturer). Put the sub-brand in product_line
  (e.g. "Offices To Go", "Newland", "Basics", or the series/family name like "Craft", "Loover").
- country_of_manufacture = "Canada" (locked for all GFG).
- warranty: GFG default is "Limited Lifetime Warranty" - but CONFIRM from source; seating/filing lines
  sometimes differ. If source states a specific term, use it. If unconfirmed, use "Limited Lifetime Warranty"
  and add flag "warranty-defaulted".
- certifications: DO NOT auto-apply GREENGUARD. Only include a cert you actually confirmed on the source
  page (ANSI/BIFMA is often confirmable at the series page; Newland desking lines carry GREENGUARD/
  GREENGUARD Gold). If you cannot confirm any cert, return certifications=[] and add flag "certs-unconfirmed".

=== 13 specs.* FIELDS (exact data shapes) ===
manufacturer(single line) | product_line(single line) | model_codes(array) | dimensions(single line,
seat-height range inline for chairs) | weight(single line e.g. "46 lbs") | weight_capacity(single line
e.g. "300 lbs") | materials(array, one material per line) | finishes_available(array) | key_features(array)
| certifications(array) | warranty(single line) | country_of_manufacture(single line) | who_its_for(single
line, audience sentence). If a value is genuinely unknown after sourcing, use "" (empty) and add a flag -
do NOT invent specs. NEWLINE SANITIZATION: single-line fields (manufacturer, product_line, dimensions,
weight, weight_capacity, warranty, country_of_manufacture, who_its_for) must contain NO newline characters.

=== body_html ===
- Theme splits at FIRST <h3>: text before first <h3> = lede (renders above spec table); <h3> sections
  render below. Structure: 1 lede <p> (2-3 sentences, design-forward, institutional-aware), then
  <h3>Features</h3> with a <ul> of features, optionally <h3>Specifications</h3> short prose, then a
  closing <p> with the quote CTA. Keep valid, clean HTML. Preserve any genuinely useful content from the
  current body but rewrite to BBI voice.
- Set boilerplate_detected=true if the CURRENT body (from snapshot) is generic filler/stub; false if it
  was real product copy.

=== BBI VOICE RULES (hard) ===
- NEVER write the literal "BBI" in customer copy. Always full "Brant Business Interiors".
- Design-forward, confident, concise. Lead with a benefit hook, not a spec dump.
- Trust anchors where natural: family-owned since 1964; 296 George St N, Peterborough ON; OECM-eligible
  supplier (Ontario institutional buyers can purchase without open tender) - use OECM as a trust signal,
  not the hero. Canadian-owned / Made in Canada: when you state it, it is genuinely a selling point for
  this GFG (Canada-made) product - fine to mention.
- CTA microcopy: "Request a Quote" and phone "Call 1-800-835-9565". Most of these are quote-request
  products; include a quote CTA line in the closing <p>.
- No invented stats, no fabricated lead times, no Indigenous-segment marketing.

=== PRIORITY KEYWORDS (v1 LOCKED clusters only) ===
Integrate 1-2 ONLY where they genuinely fit THIS product. Do NOT force. Brand terms (Global/OTG/Newland)
are NOT locked keywords - use brand names descriptively only, never as the keyword target.
LOCKED bank by product nature:
- Executive desk / management suite / U/L-shaped suite: "executive desk", "executive office desk",
  "l-shaped executive desk", "executive desk canada", "wood executive desk".
- Reception desk products: "reception desk", "l-shaped reception desk", "reception desk canada",
  "modern reception desk".
- Boardroom / conference / meeting table: "boardroom table", "conference table", "wood boardroom table",
  "conference table canada".
- Task/executive/guest SEATING (chairs, tilters, stools): map to executive-seating / waiting-room-seating
  funnels. Fitting terms: "office chairs for waiting room", "waiting room chairs canada" ONLY if genuinely
  guest/waiting seating; for executive/task chairs prefer descriptive "ergonomic office chair", "task chair".
- Lounge / coffee / occasional / modular tables: reception & lounge AREA furniture. A table is NOT a
  "waiting room chair" - do not apply chair keywords to tables. If nothing fits cleanly, land ZERO
  priority keywords and say so (correct behavior, not a failure).
Record exactly which keywords you placed in title / meta / body in priority_keywords_landed.

=== SEO ===
- seo_title: product-focused, <=60 chars, suffix " | Brant Business Interiors" when it fits; if 60 chars
  is tight, drop the suffix rather than truncate the product name. Do NOT use the long page-level suffix.
- seo_description: <=160 chars, institutional-buyer hook, natural keyword if one fits.

=== TAGS ===
Start from the snapshot's current tags; ADD (do not remove unless clearly wrong): "brand:global-furniture-group",
a "type:{slug}" tag for the product type (e.g. type:task-chair, type:lounge-seating, type:desk,
type:storage-filing, type:table, type:workstation), and keep "oecm-eligible" if present. Return the FULL
final tag list.
`

phase('Draft')
const drafts = await parallel(briefs.map(b => () =>
  agent(
    RULES + "\n\n=== THIS PRODUCT ===\n" +
    "handle: " + b.handle + "\n" +
    "title (current): " + b.title + "\n" +
    "variant SKU: " + b.sku + "\n" +
    "model code (SKU minus GLB/GLO wrapper): " + b.model_code + "\n" +
    "price: $" + b.price + "\n" +
    "product_type (current): " + (b.product_type || "(none)") + "\n" +
    "sub-brand routing: " + b.sub_brand + "\n" +
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
