# BBI Design Workflow — Claude Design → Shopify Theme

**Rule:** Use Claude Design + Dribbble to generate high-fidelity visual mockups. Port the visual result (colors, type, layout, component styling, animations) back into the BBI Shopify theme at `theme/`. Do **not** export to Next.js or rebuild off Shopify.

---

## Step 1 — Build the design system once

- Go to `claude.ai/design` → Design systems → Create new.
- Source a starting brand kit from [getdesign.md](https://getdesign.md) (free, 68 brands). Copy the `design.md` content and paste into the design system's "additional notes."
- For BBI, seed it with the brand direction from the brand kit task: match brantbasics.com theme (colors, fonts, spacing). If the Chrome extension isn't connected yet, extract colors/fonts from brantbasics.com manually first.
- One shared design system keeps the homepage, OECM landing, vertical pages, and brand dealer pages visually coherent.

## Step 2 — Structure from Dribbble

- For office-furniture page layouts: [dribbble.com/search/office-furniture-website](https://dribbble.com/search/office-furniture-website).
- Pick a layout whose *structure* (hero + section order + grid) fits the page type. Save the screenshot.
- The Dribbble shot drives **layout**; the design system drives **look**.

## Step 3 — Generate in Claude Design

- `claude.ai/design` → Home → Prototype → pick the BBI design system → **high-fidelity** (not wireframe).
- Attach the Dribbble screenshot. Prompt: use design system for branding, use screenshot for structure. Name the pages you want (e.g., OECM landing, Schools vertical, Healthcare vertical, Brand dealer — ergoCentric).
- Iterate with the comment/edit/draw tools on specific elements. Replace placeholder names/photos with real content — pull from the OCI photo library at `data/oci-photos/catalog.json`.

## Step 4 — Port to Shopify (do NOT use the Next.js export path)

- Skip the "Handoff to Claude Code → Next.js" step from the transcript. BBI is Shopify.
- Screenshot or extract CSS values from the Claude Design output (colors, spacing, font sizes, component styling).
- Apply to the BBI Shopify theme at `theme/` — edit Liquid templates, `theme.liquid`, section files, and `assets/` CSS.
- For animations: use lightweight vanilla CSS transitions / Intersection Observer. Only pull in GSAP if a specific animation genuinely needs it; avoid bloating the theme for decoration.

## Step 5 — Verify on the Shopify dev theme

- Push to a Shopify dev/preview theme, not the live theme.
- Review on desktop + mobile before promoting.

---

## Key links

- **Claude Design:** `claude.ai/design`
- **Design kit library:** [getdesign.md](https://getdesign.md)
- **Office furniture layout references:** [dribbble.com/search/office-furniture-website](https://dribbble.com/search/office-furniture-website)
- **GSAP demos** (reference only, don't default to using it): `demos.gsap.com`

## Where this applies in the wave plan

- **Wave 1:** OECM landing, brand dealer pages (ergoCentric/Keilhauer/Global/Teknion), vertical pages (Schools, Healthcare, Government) — all get designed via this workflow before the Liquid build.
- **Wave 3:** City-level SEO pages reuse the same design system for consistency.
- **Brand kit:** produces the seed design system used in Step 1.
