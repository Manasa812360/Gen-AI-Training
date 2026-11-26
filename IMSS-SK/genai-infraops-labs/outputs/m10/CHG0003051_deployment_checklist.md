# CHG0003051 — Deployment checklist

## Pre-change

- [ ] Confirm the approved calendar date and 23:00–01:00 IST window.
- [ ] Confirm CAB, Change Manager and peer-review approvals.
- [ ] Record implementer, rollback owner and escalation contacts.
- [ ] Record current pipeline and registry-retention configuration revisions.
- [ ] Confirm the previous approved `portal-api` image is available.
- [ ] Confirm production portal health and HTTP 5xx rate are at baseline.
- [ ] Confirm Service Desk and monitoring coverage.
- [ ] Attach evidence for controlled migration-failure, schema-object and login tests.
- [ ] Confirm the proposed backout can restore the prior configuration revisions.

## Implementation

- [ ] Apply the approved pipeline change through version control.
- [ ] Confirm migration failure propagates to pipeline failure and blocks activation.
- [ ] Confirm required schema-object validation is enabled.
- [ ] Confirm the authenticated-login smoke test is enabled and fails on HTTP 5xx.
- [ ] Apply the approved registry-retention change.
- [ ] Confirm the approved previous image remains available.

## Verification

- [ ] Run the approved non-production validation and retain the result.
- [ ] Confirm the active production portal release is unchanged unless separately approved.
- [ ] Validate portal health and authenticated login.
- [ ] Confirm the HTTP 5xx rate remains within the agreed baseline for 15 minutes.
- [ ] Confirm there is no unexpected pipeline, database or registry impact.
- [ ] Record exact evidence and timestamps in the change record.

## Backout triggers

Stop and back out for any failed migration gate, unexpected portal degradation, missing rollback image, increased HTTP 5xx, unauthorised configuration drift or inability to verify the result.

## Closure

- [ ] Record the implementation and test evidence.
- [ ] Mark backout as tested or untested with evidence.
- [ ] Send completion communication to the Service Desk and stakeholders.
- [ ] Schedule enhanced monitoring and review for the next portal release.

