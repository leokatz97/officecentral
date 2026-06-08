---
name: bbi-register-brand
description: Use when Leo is registering a NEW brand into the BBI reference system — typically when he pastes a "NEW BRAND SETUP" note produced by Steve's onboarding tool, or asks to add a new vendor/brand/manufacturer to the reference. Adds the brand to the three reference YAMLs, regenerates the bundle JSON, reconciles the draft product, and opens a PR for review. Do NOT trigger on adding a single product to a brand that already exists in the reference.
---

# BBI Register Brand

Turn a "NEW BRAND SETUP" note (or an equivalent brand spec) into a registered brand in the BBI reference system — on a branch, as a PR for Leo to review. This is the step that makes a brand real so Steve's onboarding tool stops halting on it.

## Standing rules (same as the rest of BBI)
- **Vendor = the manufacturer**, never the dealer ("Brant Business Interiors" is always an error). The value you register is the canonical vendor string written to that brand's products.
- **Never guess.** If the note is missing something required (prefix, category, collection), STOP and ask Leo — do not invent it.
- **Branch -> PR -> squash-merge -> linear ff. Never commit main. Do NOT merge** — Leo reviews.
- **Exact-match readback:** after writing, re-read what you wrote and confirm it matches.

## Input
A "NEW BRAND SETUP" note with: Manufacturer (vendor), SKU prefix, default Google category, target collection (existing or new), Made-in-Canada/warranty (only if confirmed), the first product's draft link/handle, and which specs were sourced. If a required field is missing, ask Leo before writing anything.

## Steps

1. **Read the three reference files first** so you mirror their exact structure (don't impose a new format):
   - `data/reference/sku-prefix-lookup.yaml`
   - `data/reference/manufacturer-defaults.yaml`
   - `data/reference/brand-collection-routing.yaml`
   Confirm the brand isn't already present under a different key. Note the existing tag convention (there is a known mismatch where some smart rules expect a bare tag like `task-chair` while a template emits `type:task-chair` — follow whatever the live collection rules actually expect).

2. **On a new branch, add the brand:**
   - `sku-prefix-lookup.yaml`: map the SKU prefix -> the new brand key. Check for greedy-prefix collisions with existing prefixes (a shorter existing prefix that would swallow this one, or vice versa); add a guard if needed.
   - `manufacturer-defaults.yaml`: the brand key -> canonical vendor string, default Google product category, and country/Made-in-Canada + warranty ONLY if the note confirmed them.
   - `brand-collection-routing.yaml`: the brand key -> its target collection(s) and the routing tag(s) each collection needs, matching the live rule convention.

3. **Collection:**
   - Existing collection named in the note -> route to it.
   - "NEW collection needed" -> create it (smart with the rule, or manual). If you can't determine the smart rule safely, FLAG it for Leo instead of guessing.

4. **Reconcile the first product draft** (if a link/handle was given):
   - Set the product's `vendor` to the canonical vendor string you just registered (correct it if Steve's draft used a slightly different label).
   - Set the routing tag(s) so it joins the right smart collection, and/or add it to the manual collection.
   - Confirm it is still **DRAFT**. Never publish.

5. **Regenerate the bundle:** run `scripts/export-brand-onboarding-reference.py`. Confirm the new brand's prefix resolves, and that there are zero unexpected (non-brand) differences versus the previous JSON.

6. **Open a PR** (branch -> PR). Show Leo: the YAML diff, the regenerated-JSON diff, confirmation the prefix resolves, and the reconciled draft's link. **Do NOT merge.**

## After merge — remind Leo
The regenerated brand JSON must go back into Steve's skill bundle, or his tool still won't see the new brand: copy the new JSON into `bbi-product-onboarding/references/brand-onboarding-reference.json`, re-zip the `bbi-product-onboarding` folder, and re-upload it in Customize -> Skills (delete the old one first).
