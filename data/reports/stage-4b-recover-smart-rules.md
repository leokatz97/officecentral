# Stage 4b Recovery — Smart Collection Rules Audit
_Generated: 2026-05-08_

## Desk & Category Hub Smart Collections

| Handle | Count | Logic | Rules |
|---|---|---|---|
| accessories | 91 | OR | tag equals `type:accessories`; tag equals `type:desk-accessories`; tag equals `type:power-modules`; tag equals `type:chair-accessories` |
| all | 648 | AND | type not_equals `Avis-add-charge`; type not_equals `mws_apo_generated` |
| avada-best-sellers | 624 | AND | variant_price greater_than `0`; type not_equals `mws_apo_generated` |
| boardroom | 87 | OR | tag equals `room:boardroom`; tag equals `type:boardroom-tables`; tag equals `type:conference-tables` |
| bundle-builder-products | 0 | AND | type equals `Custom Bundle`; type not_contains `mws_fee_generated`; type not_equals `mws_apo_generated` |
| business-furniture | 624 | AND | tag not_equals `industry:educational`; tag not_equals `industry:daycare`; tag not_equals `industry:healthcare` |
| desks | 98 | OR | tag equals `type:desks`; tag equals `type:benching`; tag equals `type:workstations`; tag equals `type:sit-stand` |
| ergonomic-products | 16 | OR | title contains `monitor arm`; title contains `keyboard tray`; title contains `sit-stand`; title contains `anti-fatigue` |
| fees-products | 653 | AND | type not_contains `mws_fee_generated`; type not_equals `mws_apo_generated` |
| lounge-reception | 16 | OR | tag equals `waiting-room`; type contains `lounge`; type contains `reception`; title contains `lounge`; title contains `reception` |
| mandatory-fees | 1 | AND | type equals `Fee`; type not_equals `mws_apo_generated`; type not_contains `mws_fee_generated` |
| orderly-emails-recommended-products | 100 | AND | variant_inventory greater_than `0`; type not_equals `mws_apo_generated` |
| panels-room-dividers | 16 | OR | title contains `partition`; title contains `room divider`; title contains `modesty panel`; title contains `otg panel`; title contains `divider` |
| products | 648 | AND | type not_equals `Avis-add-charge`; type not_contains `mws_fee_generated`; type not_equals `mws_apo_generated` |
| products-1 | 648 | AND | type not_equals `Avis-add-charge`; type not_equals `mws_apo_generated` |
| quiet-spaces | 9 | OR | title contains `acoustic`; title contains `sound dampener`; title contains `phone booth`; title contains `soft pod` |
| room-boardroom | 87 | AND | tag equals `room:boardroom` |
| room-break-room | 0 | AND | tag equals `room:break-room` |
| room-lounge | 10 | AND | tag equals `room:lounge` |
| room-open-plan | 11 | AND | tag equals `room:open-plan` |
| room-private-office | 168 | AND | tag equals `room:private-office` |
| room-reception | 21 | AND | tag equals `room:reception` |
| room-training-room | 5 | AND | tag equals `room:training-room` |
| seating | 194 | OR | tag equals `type:chairs`; tag equals `type:lounge`; tag equals `type:ergonomic-seating`; tag equals `type:bariatric-seating`; tag equals `type:stacking`; tag equals `type:seating` |
| smart-products-filter-index-do-not-delete | 653 | OR | variant_price greater_than `-9999` |
| storage | 82 | OR | tag equals `type:storage`; tag equals `type:filing`; tag equals `type:bookcases`; tag equals `type:cabinets`; tag equals `type:lateral-files` |
| tables | 104 | OR | tag equals `type:tables`; tag equals `type:folding-tables`; tag equals `type:training-tables`; tag equals `type:cafeteria-tables` |
| task-chairs | 10 | OR | tag equals `task-chair`; type contains `task`; title contains `task chair` |
| type-accessories | 91 | AND | tag equals `type:accessories` |
| type-chairs | 184 | AND | tag equals `type:chairs` |
| type-desks | 98 | AND | tag equals `type:desks` |
| type-lounge | 10 | AND | tag equals `type:lounge` |
| type-outdoor | 5 | AND | tag equals `type:outdoor` |
| type-storage | 82 | AND | tag equals `type:storage` |
| type-tables | 104 | AND | tag equals `type:tables` |

## Issues Found

- **room-break-room**: 0 products. Rules: [{'column': 'tag', 'relation': 'equals', 'condition': 'room:break-room'}]
- **bundle-builder-products**: 0 products. Rules: [{'column': 'type', 'relation': 'equals', 'condition': 'Custom Bundle'}, {'column': 'type', 'relation': 'not_contains', 'condition': 'mws_fee_generated'}, {'column': 'type', 'relation': 'not_equals', 'condition': 'mws_apo_generated'}]

## Desk Hub Health Check

| Collection | Count | Rule Tags | Status |
|---|---|---|---|
| type-accessories | 91 | `type:accessories` | ✓ Healthy |
| accessories | 91 | `type:accessories`, `type:desk-accessories`, `type:power-modules`, `type:chair-accessories` | ✓ Healthy |
| type-chairs | 184 | `type:chairs` | ✓ Healthy |
| type-desks | 98 | `type:desks` | ✓ Healthy |
| desks | 98 | `type:desks`, `type:benching`, `type:workstations`, `type:sit-stand` | ✓ Healthy |
| room-lounge | 10 | `room:lounge` | ✓ Healthy |
| lounge-reception | 16 | `waiting-room`, `lounge`, `reception`, `lounge`, `reception` | ✓ Healthy |
| type-lounge | 10 | `type:lounge` | ✓ Healthy |
| seating | 194 | `type:chairs`, `type:lounge`, `type:ergonomic-seating`, `type:bariatric-seating`, `type:stacking`, `type:seating` | ✓ Healthy |
| type-storage | 82 | `type:storage` | ✓ Healthy |
| storage | 82 | `type:storage`, `type:filing`, `type:bookcases`, `type:cabinets`, `type:lateral-files` | ✓ Healthy |
| type-tables | 104 | `type:tables` | ✓ Healthy |
| tables | 104 | `type:tables`, `type:folding-tables`, `type:training-tables`, `type:cafeteria-tables` | ✓ Healthy |
| task-chairs | 10 | `task-chair`, `task`, `task chair` | ✓ Healthy |