export const meta = {
  name: 'b4s4-global-draft',
  description: 'B4S4 — auto-source + draft 20 Global Furniture Group products to BBI 13-field framework',
  phases: [{ title: 'Source+Draft', detail: 'one agent per product: web-source globalfurnituregroup.com + draft bundle' }],
}

// args = array of handles (the 20-product batch, in order)
const HANDLES = typeof args === 'string' ? JSON.parse(args) : args

const SHARED = `
You are enriching ONE product for Brant Business Interiors (BBI), a B2B Shopify store selling
office furniture to Canadian institutional buyers (school boards, hospitals, municipalities).
Manufacturer for every product in this batch is Global Furniture Group (globalfurnituregroup.com).

STEP 1 — LOAD THE PRODUCT
Read the file /tmp/b4s4-src.json (use the Read tool). It is a JSON array of 20 products.
Find the ONE object whose "handle" exactly equals the handle given to you below. Use ONLY that object.
It contains: title, price, skus[], options[], variant_titles[], existing_body_html (already has strong
spec data scraped from the manufacturer), existing_specs, collection_ids.

STEP 2 — AUTO-SOURCE (verify + augment)
The SKUs embed the Global model code (e.g. "GLO-NLP412" -> NLP412, "GLB 2526" -> 2526, "GLB8271" -> 8271,
"GLO-ML2630" -> ML2630). Try, in order, to confirm/augment specs from the manufacturer:
  a. Load WebFetch + WebSearch tools via ToolSearch (query "select:WebFetch,WebSearch").
  b. WebSearch '"{model_code}" site:globalfurnituregroup.com' (and the product line name, e.g. "Newland", "Prime", "Vitrola", "Wind", "Drift", "ML", "Loover", "Bungee"). WebFetch the best canonical product/series page.
  c. If globalfurnituregroup.com has nothing, a single general WebSearch for the model code is allowed.
The existing_body_html is already a strong source — your job is to STRUCTURE it and fill gaps with the
manufacturer page. Do NOT invent specs. If a field cannot be confirmed from existing_body_html OR the
web source, set it to null (for single fields) or [] (for lists) and add the field name to "missing".

source_quality:
  "excellent" = confirmed on a globalfurnituregroup.com product page, all/most fields filled
  "good"      = rich existing_body_html + partial web confirmation
  "partial"   = thin data, several fields missing
  "poor"      = almost nothing usable
  "REQUIRES_LEO_SOURCE" = no usable data anywhere
  "BOILERPLATE_CORRUPTED" = existing_body_html clearly describes a DIFFERENT product than the title
                            (e.g. a chair description on a desk). Set boilerplate_corrupted=true and DO
                            NOT fabricate — draft only what the title/SKU justify, flag for Leo.

STEP 3 — MANUFACTURER DEFAULTS (Global Furniture Group), override only if the source contradicts:
  warranty: "Limited Lifetime Warranty"
  country_of_manufacture: "Canada"  (Global + all sub-brands are Canada-made; most bodies say "Made in Canada")
  certifications: confirm from source; Global commonly carries GREENGUARD and/or BIFMA. Only list a
  certification you can justify from the source/body; otherwise leave [] and add to missing.

STEP 4 — DRAFT (BBI voice — institutional, design-forward, concrete; NO fluff)
  - title: clean retail title. Format like "Global {Product Line} {Descriptor}" e.g.
    "Global Newland U-Shaped Desk — 72\\"W × 96\\"D". Manufacturer brand shown is "Global" (the storefront
    name); the metafield manufacturer is the full "Global Furniture Group".
  - product_type: a clean type, e.g. Desk / Lateral File Cabinet / Storage Cabinet / Lounge Seating /
    Lounge Chair / Panel System / Flip-Top Table / Bar Stool / Task Chair / Workstation.
  - product_line: just the line name (e.g. "Newland", "Prime", "Vitrola", "Wind", "Drift", "ML", "Loover",
    "Bungee", "Robust"). Do NOT prefix with a sub-brand.
  - model_codes: array of the real model codes parsed from the SKUs (strip GLO-/GLB- prefixes; keep the code).
  - dimensions, weight, weight_capacity, materials (newline-separated string), finishes_available[],
    key_features[] (3-6 concrete bullets), certifications[].
  - who_its_for: one sentence naming the institutional setting (e.g. "Private offices and open-plan
    workstations in municipal and education environments...").
  - hook: a single bold-worthy opening sentence (design-forward, benefit-led).
  - lede: 2-3 sentence paragraph expanding the hook with concrete specifics.
  - seo_title: "Global {Product} | Brant Business Interiors" but if that exceeds 60 chars, DROP the
    " | Brant Business Interiors" suffix. HARD LIMIT 60 chars.
  - seo_description: <=160 chars, institutional-buyer hook, end with "OECM-eligible." if it fits.
  - image_alt: descriptive, not keyword-stuffed.
  - tags: MUST include "brand:global-furniture-group", "oecm-eligible", and a "type:{slug}" tag; add
    relevant material:/feature:/segment: tags. Lowercase, hyphenated.

VOICE RULES (mandatory):
  - NEVER write "BBI" in customer-facing copy — always "Brant Business Interiors".
  - No Indigenous-segment marketing.
  - If the product is Made in Canada, it's a selling point — weave it in naturally.
  - Do NOT include a phone/OECM call-to-action in the lede or features; that CTA is appended automatically.
  - Use straight ASCII in your JSON values (plain " and -). Final HTML entity formatting is applied later.

Return ONLY the structured object via the StructuredOutput tool. Be precise and factual.
`

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['handle','title','product_type','product_line','model_codes','dimensions','weight',
    'weight_capacity','materials','finishes_available','key_features','certifications','warranty',
    'country_of_manufacture','who_its_for','hook','lede','seo_title','seo_description','image_alt',
    'tags','source_quality','source_url','missing','boilerplate_corrupted','notes'],
  properties: {
    handle: { type: 'string' },
    title: { type: 'string' },
    product_type: { type: 'string' },
    product_line: { type: 'string' },
    model_codes: { type: 'array', items: { type: 'string' } },
    dimensions: { type: ['string','null'] },
    weight: { type: ['string','null'] },
    weight_capacity: { type: ['string','null'] },
    materials: { type: ['string','null'] },
    finishes_available: { type: 'array', items: { type: 'string' } },
    key_features: { type: 'array', items: { type: 'string' } },
    certifications: { type: 'array', items: { type: 'string' } },
    warranty: { type: ['string','null'] },
    country_of_manufacture: { type: ['string','null'] },
    who_its_for: { type: 'string' },
    hook: { type: 'string' },
    lede: { type: 'string' },
    seo_title: { type: 'string' },
    seo_description: { type: 'string' },
    image_alt: { type: 'string' },
    tags: { type: 'array', items: { type: 'string' } },
    source_quality: { type: 'string', enum: ['excellent','good','partial','poor','REQUIRES_LEO_SOURCE','BOILERPLATE_CORRUPTED'] },
    source_url: { type: ['string','null'] },
    missing: { type: 'array', items: { type: 'string' } },
    boilerplate_corrupted: { type: 'boolean' },
    notes: { type: ['string','null'] },
  },
}

phase('Source+Draft')
const drafts = await parallel(HANDLES.map((handle, i) => () =>
  agent(`${SHARED}\n\n=== YOUR PRODUCT HANDLE ===\n${handle}\n`, {
    label: `draft:${handle.slice(0,32)}`,
    phase: 'Source+Draft',
    schema: SCHEMA,
  }).then(d => ({ ...d, _n: i + 1, handle }))
))

return drafts.filter(Boolean)
