export const meta = {
  name: 'item2-spec-research',
  description: 'Research manufacturer datasheets for weight/dimensions on 177 feed-blocked BBI products',
  phases: [{ title: 'Research', detail: 'one agent per ~3 same-manufacturer products' }],
}

// args = { chunks: [[handle, handle, handle], ...] }  (grouped by manufacturer)
const WORKLIST = '/Users/leokatz/Desktop/Office Central/data/reports/item2-research-worklist-2026-06-05.json'
const parsed = typeof args === 'string' ? JSON.parse(args) : args
const chunks = parsed && parsed.chunks
if (!Array.isArray(chunks)) throw new Error('args.chunks must be an array of handle-arrays')
log(`Researching ${chunks.reduce((n, c) => n + c.length, 0)} products in ${chunks.length} agent batches`)

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['results'],
  properties: {
    results: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['handle', 'id', 'dimensions_value', 'dimensions_url', 'dimensions_snippet',
                   'weight_value', 'weight_url', 'weight_snippet', 'notes'],
        properties: {
          handle: { type: 'string' },
          id: { type: 'string' },
          dimensions_value: { type: 'string', description: 'Overall dims like 26"W x 24.5"D x 43"H, or "" if not found on a manufacturer-domain page' },
          dimensions_url: { type: 'string', description: 'Manufacturer-domain URL (the brand\'s own site) where the dims appear, else ""' },
          dimensions_snippet: { type: 'string', description: 'Verbatim text from that page containing the dimension figures, else ""' },
          weight_value: { type: 'string', description: 'Product/shipping weight like 37.5 lbs, or "" if not found on a manufacturer-domain page' },
          weight_url: { type: 'string', description: 'Manufacturer-domain URL where the weight appears, else ""' },
          weight_snippet: { type: 'string', description: 'Verbatim text from that page containing the weight figure, else ""' },
          notes: { type: 'string', description: 'Brief: what was found/not found, any reseller-only data seen (do NOT put reseller data in *_value)' },
        },
      },
    },
  },
}

const results = await parallel(chunks.map((handles, idx) => () => {
  const prompt = `You are sourcing furniture spec data for a Google Shopping feed. WRONG DATA IS WORSE THAN MISSING DATA. Never estimate, never infer, never guess. Only report a value you can read VERBATIM on the MANUFACTURER'S OWN WEBSITE (a manufacturer-domain URL).

STEP 1 — read the worklist to get each product's model SKUs, manufacturer, and what it needs:
  Read the JSON file: ${WORKLIST}
  It is an array of objects with fields: handle, id, title, all_skus, vendor, manufacturer_guess, site_hint, needs.
  Process ONLY these handles: ${JSON.stringify(handles)}

STEP 2 — for EACH of those products, use WebSearch then WebFetch to find the model's spec sheet / cut sheet / product detail page ON THE MANUFACTURER'S OWN DOMAIN (use the manufacturer_guess + site_hint as the starting point). Extract:
  - OVERALL DIMENSIONS (width x depth x height; include seat height for chairs).
  - PRODUCT or SHIPPING WEIGHT (lbs and/or kg) — the hard one; furniture weight is often only in dealer price lists. If it is NOT on the manufacturer's own domain, leave weight_value EMPTY (record any reseller figure in notes instead).

STRICT RULES:
1. A *_value may be filled ONLY if *_url is a manufacturer-domain page AND *_snippet is the verbatim text from that page containing the figure. If you cannot meet all three, leave all three EMPTY ("") for that field.
2. Reseller / dealer / marketplace pages (officeanything, wayfair, amazon, offisavvy, madisonliquidators, etc.) DO NOT qualify. Mention them in notes only.
3. Match the SKU/model EXACTLY. If a page covers a product LINE with many sizes, only report dims/weight if you can tie them to THIS model number; otherwise leave empty and explain in notes.
4. Format dimensions like: 26"W x 24.5"D x 43"H (seat height 18"-22.5"). Format weight like: 37.5 lbs (17 kg).
5. Return one result object per product, echoing its handle and id EXACTLY from the worklist.

Return all ${handles.length} products via the structured output.`
  return agent(prompt, { label: `research#${idx}`, phase: 'Research', schema: SCHEMA })
    .then(r => (r && r.results) ? r.results : [])
}))

const flat = results.filter(Boolean).flat()
log(`Collected ${flat.length} product results`)
return { count: flat.length, results: flat }
