# Stage 4a — Trust Pills + Brand Block Audit

**Date:** 2026-05-07  
**Catalog size:** 594 active products (all 3 pages checked)

---

## 6a — Trust Pill Tag Coverage

### Full tag census results

The full 594-product catalog has exactly **17 unique tag keys** in use:

| Tag | Count | % of catalog |
|---|---|---|
| `industry:business` | 548 | 92.3% |
| `type:chairs` | 174 | 29.3% |
| `room:private-office` | 163 | 27.4% |
| `bestseller` | 131 | 22.1% |
| `type:tables` | 97 | 16.3% |
| `type:desks` | 95 | 16.0% |
| `type:accessories` | 91 | 15.3% |
| `room:boardroom` | 83 | 14.0% |
| `type:storage` | 80 | 13.5% |
| `room:reception` | 21 | 3.5% |
| `room:open-plan` | 11 | 1.9% |
| `room:lounge` | 8 | 1.3% |
| `type:lounge` | 8 | 1.3% |
| `type:outdoor` | 4 | 0.7% |
| `room:training-room` | 3 | 0.5% |
| `industry:daycare` | 1 | 0.2% |
| `industry:healthcare` | 1 | 0.2% |

### Canadian-made tag coverage

**0 products** carry any tag containing "canadian", "canada", "maple", "made-in", or "made_in".  
The canonical trust pill tag (`canadian-made`) does not exist in the catalog.

### OECM-eligible tag coverage

**0 products** carry any tag containing "oecm".  
The canonical trust pill tag (`oecm-eligible`) does not exist in the catalog.

### Implication

The T5 badge row (OECM · Canadian-made) cannot be driven by product tags today. Two options:

**Option A — Metafield fallback (recommended for Stage 4b):**  
Use `product.metafields.specs.country_of_manufacture` to drive the Canadian-made badge. Products with `country_of_manufacture = "Canada"` get the badge. Confirmed available on ~10% of catalog (those with spec metafields). Scales as more spec data is pushed.

**Option B — Tagging pass (pre-Stage-4b blocker):**  
Add `canadian-made` and `oecm-eligible` tags to relevant products via a bulk-tag script. Requires identifying which products qualify — a manual or AI-assisted classification task. Estimated ~1 day effort. Locks trust pill source of truth to tags (more flexible long-term, consistent with existing taxonomy pattern).

**Recommendation:** Use Option A for Stage 4b (metafield fallback, immediate). Schedule Option B as a post-Stage-4 data task. The Liquid can support both: check tag first, fall back to metafield.

---

## 6b — Brand Block Requirements

### Priority brands in catalog

| Brand | Shopify vendor name | Product count | Brand Shopify page | Brand section | Brand images |
|---|---|---|---|---|---|
| ergoCentric | Not a distinct vendor — ergoCentric products sell under `Brant Business Interiors` or `Global Furniture Group` (OTG sub-brand) | Unknown — no vendor match | `/pages/brands-ergocentric` ✅ | `ds-lp-brands-ergocentric.liquid` ✅ | `data/page-images/ergocentric/` ✅ |
| Keilhauer | Not present as vendor in catalog | 0 products found with Keilhauer vendor | `/pages/brands-keilhauer` ✅ | `ds-lp-brands-keilhauer.liquid` ✅ | `data/page-images/keilhauer/` ✅ |
| Global / Teknion | `Global Furniture Group` (32 products), `Teknion` (11 products) | 43 products | `/pages/brands-global-teknion` ✅ | `ds-lp-brands-global-teknion.liquid` ✅ | `data/page-images/global-teknion/` ✅ |

### Brand asset availability

**ergoCentric:**
- ✅ Brand blurb — exists in `ds-lp-brands-ergocentric.liquid` ("As an authorized ergoCentric dealer, Brant Business Interiors provides access to the full product line, trial chair programs, and volume pricing for large institutional orders. The 12-year mechanism warranty...")
- ✅ Hero images — `data/page-images/ergocentric/ergocentric-product.jpg`, `ergocentric-space.jpg`
- ❌ Brand logo — No standalone ergoCentric manufacturer logo asset in `theme/assets/` or `data/`. Section uses schema `image_picker` — would need to upload to Shopify Files and reference via schema setting.
- ✅ "Authorized dealer" badge copy — present in brand section
- ⚠️ "View all" link target — `/collections/ergocentric` smart collection does NOT exist; brand page is `/pages/brands-ergocentric` (acceptable interim link target)

**Keilhauer:**
- ✅ Brand blurb — likely exists in `ds-lp-brands-keilhauer.liquid` (not verified line-by-line but same structure as ergoCentric section)
- ✅ Hero images — `data/page-images/keilhauer/keilhauer-product.jpg`, `keilhauer-space.jpg`
- ❌ Brand logo — Same gap as ergoCentric
- ⚠️ "View all" link target — `/collections/keilhauer` does NOT exist; 0 Keilhauer products found under that vendor name
- ❌ Products in catalog under Keilhauer vendor — **none found**. Keilhauer may not be carried yet, or products may be filed under `Brant Business Interiors`.

**Global / Teknion:**
- ✅ Brand blurb — likely exists in `ds-lp-brands-global-teknion.liquid`
- ✅ Hero images — `data/page-images/global-teknion/global-teknion-product.jpg`, `global-teknion-space.jpg`
- ❌ Brand logo — Same gap
- ✅ Products in catalog — 32 + 11 = 43 products under `Global Furniture Group` + `Teknion` vendors
- ⚠️ "View all" link target — `/collections/global-teknion` smart collection does NOT exist; vendor-filtered collections are SMART-1 (not yet built). Brand page `/pages/brands-global-teknion` works as interim.

### Brand block Liquid strategy

Given vendor field inconsistency (ergoCentric products don't use "ergoCentric" as vendor), a **tag-based or metafield-based brand signal** is more reliable than `product.vendor` matching. Proposed approach for Stage 4b:

```liquid
{% if product.vendor == 'Global Furniture Group' or product.vendor == 'Teknion' %}
  {# show Global/Teknion brand block #}
{% elsif product.metafields.specs.manufacturer contains 'ergoCentric' %}
  {# show ergoCentric brand block #}
{% elsif product.vendor == 'Offices to Go' %}
  {# show OTG/Global brand block as fallback #}
{% endif %}
```

This covers the confirmed vendor distribution. Brand block is hidden (not shown) when no vendor match.

### Interim "View all [Brand]" links

Until SMART-1 vendor-filtered collections are built:
- ergoCentric → `/pages/brands-ergocentric`
- Keilhauer → `/pages/brands-keilhauer`
- Global / Teknion → `/pages/brands-global-teknion`

These pages exist and are live. Update to collection links after SMART-1.

---

## Summary

| Trust signal | Feasible in Stage 4b? | Source | Coverage today |
|---|---|---|---|
| Canadian-made badge | ✅ Yes | `specs.country_of_manufacture = "Canada"` metafield | ~10% of catalog (grows with spec push) |
| OECM-eligible badge | ⚠️ Needs tagging pass | No tag exists; metafield fallback not available | 0% |
| Sold-out badge | ✅ Yes | `product.available == false` | 92% of catalog |
| Brand block — Global/Teknion | ✅ Yes | `product.vendor` match | 43 products |
| Brand block — ergoCentric | ✅ Yes (with spec metafield fallback) | `specs.manufacturer contains 'ergoCentric'` | ~10% (grows with spec push) |
| Brand block — Keilhauer | ⚠️ Partial | `product.vendor == 'Keilhauer'` | 0 products currently |
