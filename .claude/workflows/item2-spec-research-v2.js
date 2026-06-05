export const meta = {
  name: 'item2-spec-research-v2',
  description: 'Re-research weight/dimensions for the 96 missing BBI products (file-write output, no StructuredOutput)',
  phases: [{ title: 'Research', detail: 'agents write batch JSON to /tmp/item2-results' }],
}

const WORKLIST = '/Users/leokatz/Desktop/Office Central/data/reports/item2-research-worklist-2026-06-05.json'
const OUTDIR = '/tmp/item2-results'
const parsed = typeof args === 'string' ? JSON.parse(args) : args
const chunks = parsed && parsed.chunks
if (!Array.isArray(chunks)) throw new Error('args.chunks must be an array of handle-arrays')
log(`Re-researching ${chunks.reduce((n, c) => n + c.length, 0)} products in ${chunks.length} batches (file-write)`)

const out = await parallel(chunks.map((handles, idx) => () => {
  const outpath = `${OUTDIR}/batch-${idx}.json`
  const prompt = `You are sourcing furniture spec data for a Google Shopping feed. WRONG DATA IS WORSE THAN MISSING DATA. Never estimate, never infer, never guess. Only report a value you can read VERBATIM on the MANUFACTURER'S OWN WEBSITE (a manufacturer-domain URL).

STEP 1 — Read the worklist JSON file: ${WORKLIST}
It is an array of objects: { handle, id, title, all_skus, vendor, manufacturer_guess, site_hint, needs }.
Process ONLY these handles: ${JSON.stringify(handles)}

STEP 2 — For EACH product, use WebSearch then WebFetch to find the model's spec/cut sheet / product detail page ON THE MANUFACTURER'S OWN DOMAIN (start from manufacturer_guess + site_hint). Extract:
  - OVERALL DIMENSIONS (W x D x H; include seat height for chairs).
  - PRODUCT or SHIPPING WEIGHT (lbs and/or kg). Furniture weight is often only in dealer price lists — if it is NOT on the manufacturer's own domain, leave weight empty (note any reseller figure in notes).

STRICT RULES:
1. A value may be filled ONLY if its url is a manufacturer-domain page AND the snippet is verbatim text from that page containing the figure. If you cannot meet all three, leave that field's value/url/snippet as "".
2. Reseller/dealer/marketplace pages (officeanything, wayfair, amazon, offisavvy, madisonliquidators, etc.) DO NOT qualify. Mention in notes only.
3. Match the SKU/model EXACTLY. If a page covers a product LINE with many sizes, only report dims/weight you can tie to THIS model; else leave empty and explain in notes.
4. Format dims like: 26"W x 24.5"D x 43"H (seat height 18"-22.5"). Weight like: 37.5 lbs (17 kg).

STEP 3 — Write your results as JSON to this exact path using the Write tool: ${outpath}
The file MUST be a JSON object: {"results": [ {"handle","id","dimensions_value","dimensions_url","dimensions_snippet","weight_value","weight_url","weight_snippet","notes"}, ... ]}
Echo each product's handle and id EXACTLY from the worklist. Include one object per processed handle (${handles.length} total). After writing, reply with just: "wrote ${handles.length} to ${outpath}".`
  return agent(prompt, { label: `re-research#${idx}`, phase: 'Research', agentType: 'general-purpose' })
    .then(() => outpath)
}))

log(`Done — ${out.filter(Boolean).length} batches reported written to ${OUTDIR}`)
return { batches: out.filter(Boolean).length, outdir: OUTDIR }
