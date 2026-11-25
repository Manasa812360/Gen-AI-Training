# CAB one-pager — CHG0003051

## What

Add release controls so a failed database migration blocks `portal-api` activation, and retain an approved previous production image. Add schema-object and authenticated-login validation to prevent the pipeline from reporting a partial release as successful.

## Why

INC-MAJ-0042 caused a customer-facing portal login outage because a required database column was missing while the pipeline reported success. Recovery was delayed because the rollback image had been removed under retention.

## Risk

**High — 12/15.**

- Impact if it fails: 3
- Complexity: 3 — coordinated multi-team implementation
- First-time change: 3
- Backout documented but untested: 2
- Low-traffic agreed window: 1

Approval required: CAB. Obtain InfraSec sign-off as well if the final design adds an internet-exposed rule.

## Planned window

Thursday 23:00–01:00 IST. **VERIFY the calendar date.**

## Backout

Backout is to stop the release, restore the previous version-controlled pipeline and registry-retention revisions, confirm the active portal release remains unchanged, and repeat portal health checks. **Backout is currently untested.**

## Communications

Notify Change Manager, Platform, Application, Database and Service Desk before the window. Send start, validation and closure updates. Escalate any failed gate, missing rollback image, HTTP 5xx increase or customer impact immediately.

## Go/no-go checklist

1. [ ] Calendar date, implementer and approvers are confirmed.
2. [ ] CAB, Change Manager and peer review approvals are recorded.
3. [ ] Current pipeline and retention configuration revisions are recorded.
4. [ ] The previous approved `portal-api` rollback image is present and identifiable.
5. [ ] Controlled migration-failure test proves activation is blocked.
6. [ ] Schema-object and authenticated-login tests pass in non-production.
7. [ ] Backout has been documented, exercised safely, and evidence attached, or the Change Manager accepts it as untested.
8. [ ] InfraSec has signed off if any internet-exposed rule is included.
9. [ ] Monitoring, Service Desk coverage and escalation contacts are ready.
10. [ ] Production portal health is at baseline before implementation.

## Decision

**GO only after all mandatory checks are satisfied. Otherwise NO-GO.**

