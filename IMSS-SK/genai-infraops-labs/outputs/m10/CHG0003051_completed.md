# CHG0003051 — Completed change proposal

**Status:** Draft for Change Manager, peer review and CAB; not approved or executed.  
**Type:** Normal  
**Requested by:** APP-PORTAL-L2  
**Related incident:** INC-MAJ-0042  
**Short description:** Add a mandatory migration-failure gate to the portal release pipeline and preserve an approved rollback image.

## Description

The Customer Portal release pipeline reported success when a database migration failed, allowing an incompatible `portal-api` release to serve traffic. The previous stable image had then been removed by registry retention, delaying rollback and requiring a rebuild. This change will make migration failure block application activation and will retain an approved rollback candidate for each active production release.

## Configuration items

- `portal-api`
- `k8s-prod-cluster-01`

## Planned window

Thursday 23:00–01:00 IST. **VERIFY:** Confirm the calendar date before approval.

## Implementation plan

1. Confirm named change owners and obtain the production pipeline and registry configuration snapshots.
2. Add a pipeline gate that treats any database-migration failure as a failed release and prevents application activation.
3. Add a post-migration check for required database objects and a portal login smoke test that fails the release on HTTP 5xx.
4. Update registry retention so an approved previous production image remains available while its replacement release is active.
5. Apply the pipeline and retention configuration through the reviewed, version-controlled deployment process.
6. Confirm that the active production release continues using the existing approved image while the controls are verified.
7. Run the test plan and retain logs, configuration references and approval evidence in the change record.

**ASSUMPTION:** The production pipeline and registry are version-controlled. **VERIFY** the repository, configuration keys, retaining-image count and configuration owner before approval.

## Test plan

### Before implementation

1. Record current pipeline status, pipeline configuration revision and registry retention values.
2. Confirm the previous approved `portal-api` image exists and can be identified as the rollback candidate.
3. In a non-production pipeline, run a controlled migration-failure test and confirm the release fails and application activation does not occur.
4. In non-production, run a successful migration and confirm the required schema-object check and authenticated-login smoke test pass.
5. Confirm a release with an HTTP 5xx login result fails and does not proceed as successful.

### After implementation

1. Confirm the production pipeline reports a migration failure as a failed release.
2. Confirm a successful non-production control release passes all gates.
3. Confirm the configured rollback candidate remains present after applying retention.
4. Run an approved post-deployment portal health and authenticated-login test.
5. Observe production HTTP 5xx rate and portal error metrics for at least 15 minutes; proceed only while they remain within the agreed baseline.
6. Confirm no unauthorised or internet-exposed rule was introduced.

## Backout plan

**Status: DOCUMENTED, UNTESTED.**

1. Stop the release if any gate or production validation fails.
2. Restore the immediately previous version-controlled pipeline configuration revision.
3. Restore the immediately previous approved registry-retention configuration revision.
4. Confirm the active portal release is unchanged and remains operational.
5. Confirm the rollback candidate image has not been deleted and document its presence.
6. Re-run the pipeline and portal health checks.
7. If the portal is degraded, follow the approved major-incident rollback process rather than making ad hoc production changes.

**Go/no-go stop conditions:** missing owner, missing previous configuration revision, no recoverable rollback image, failed controlled test, unapproved production configuration difference, or portal degradation.

## Communication

- Notify the Change Manager, APP-PORTAL-L2, Platform, Application, Database, Service Desk and incident-management contacts before the window.
- Service Desk sends updates at start, after each validation stage, and at closure.
- Any failed gate or customer impact triggers a stop and immediate escalation.

## Risk

**High — 12/15.** See `CHG0003051_risk_assessment.md`.

## Approval status

- Change Manager: Pending
- Peer technical reviewer: Pending
- CAB: Required and pending

