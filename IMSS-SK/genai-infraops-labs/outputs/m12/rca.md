# Customer Portal incident RCA - draft

## Status and impact

Cause and recovery are **not confirmed**. Tickets report login 503s, slow
reports and customer escalation after the stated release on 2026-11-12.
Affected-user count, duration and recovery time are not available.

## Timeline (IST)

- 14:00: capstone brief states the release went live.
- 14:03: first supplied HTTP5xxRate alert.
- 14:05: first supplied PodNotReady alert.
- 14:06: first supplied ImagePullBackOff alert.
- 14:08: first supplied LoginSuccessRateLow alert.
- 2026-11-26: read-only inspection of a lab cluster created on 2026-11-25.

## Evidence and hypotheses

The later lab cluster has an API pod in ImagePullBackOff because its configured
image was reported not found; the web Service has two endpoints. The ingress
host also needs confirmation. See `evidence_pack.md`. These findings are useful
for the lab investigation but do not establish what caused the earlier
incident. The correlation script's earliest critical alert is a candidate lead
alert, not a root-cause determination.

## Contributing factors and recovery

Unknown. No capstone remediation or end-to-end recovery has been verified.
Obtain deployment records, historical logs and metrics, image provenance and
approved host configuration before stating a cause or recovery time.

## Proposed follow-up

Service owners should validate the approved API image and ingress host, add
release-time image availability and end-to-end login checks, and verify
rollback availability. Track ownership and deadlines through the change
process; these are proposals, not completed actions.
