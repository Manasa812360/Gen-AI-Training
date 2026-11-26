# CHG0003051 — Risk assessment

Scoring uses `data/changes/change_risk_rubric.md`.

| Factor | Score | Reason |
|---|---:|---|
| Impact if it fails | 3 | A control or retention failure could make the customer-facing Customer Portal unavailable or delay recovery. |
| Complexity | 3 | Pipeline, migration-gate, smoke-test and registry-retention work requires coordinated Platform, Application and Database activity, meeting the rubric's multi-team high-complexity condition. |
| Change history | 3 | The record does not provide evidence that this specific gate and retention change has been performed previously. **ASSUMPTION:** Treat as first time until evidence is supplied. |
| Backout | 2 | The configuration can be reverted in version control, but the draft says only “revert” and has no tested backout evidence. |
| Timing | 1 | Thursday 23:00–01:00 IST is an agreed low-traffic window, subject to confirming the calendar date. |

## Result

- **Total:** 12/15
- **Category:** High
- **Required approval:** CAB
- **InfraSec sign-off:** Not triggered; no internet-exposed rule is included in the proposed scope.

## Conditions before approval

1. Confirm the concrete Thursday calendar date.
2. Supply the pipeline and registry repositories, owners and exact configuration revisions.
3. Demonstrate the migration-failure, schema-object and login tests in non-production.
4. Exercise and document the configuration backout where safely possible.
5. Confirm the specific prior production image and retention rule that will preserve it.
6. Obtain CAB approval. Obtain InfraSec sign-off as well if the implementation introduces any internet-exposed rule.

## Justification for score adjustment

The earlier 11/15 score treated the multi-team implementation as complexity 2. The rubric assigns 3 to multi-team work. Because Platform, Application and Database teams must coordinate the pipeline, migration gate, validation and retention controls, the corrected complexity is 3. This raises the total to 12/15 and changes the category from Medium to High.

