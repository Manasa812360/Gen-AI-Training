# Capstone evidence pack

Status: read-only investigation; no remediation executed. The named
sd-investigator chat mode was not available as a callable tool in this
session; the checks below follow its read-only evidence-pack format.

## Summary

The scenario describes a portal release at 14:00 IST on 2026-11-12 followed by
login complaints and alerts. The currently available lab cluster was created
on 2026-11-25, so it is a later reproduction, not proof of the historical
incident's state or cause.

## Timeline (IST)

- 2026-11-12 14:00: release time stated in the capstone brief.
- 14:03:00: first supplied HTTP5xxRate alert, CAPALR-000.
- 14:05:18: first supplied PodNotReady alert, CAPALR-006.
- 14:06:23: first supplied ImagePullBackOff alert, CAPALR-011.
- 14:08:15: first supplied LoginSuccessRateLow alert, CAPALR-015.
- 2026-11-26: read-only cluster inspection in context `kind-genai-labs`.

## Evidence

- `kubectl get deployments,pods -n portal -o wide`: portal-api is 0/1
  available and its pod is `ImagePullBackOff`.
- `kubectl describe pod -n portal -l app=portal-api`: the registry reported
  the configured `nginx:1.27-alpine-hotfx` image as `not found`.
- `kubectl get service portal-web -n portal -o yaml`: the live selector is
  `app: portal-web`; `kubectl get endpoints -n portal` shows two endpoints.
  The checked-in broken fixture instead specifies `app: portal-web-v2`.
- `kubectl get ingress portal -n portal -o yaml`: the configured host is
  `portal.exmaple-corp.local`. The intended host and ingress controller
  availability have not been independently established.
- `data/capstone/alerts.json` and `data/cmdb/ci_inventory.csv`: alert groups
  and their service mappings are documented in `alert_incident.md`.

## Ranked hypotheses

1. **High confidence, current lab state:** the API cannot start because its
   configured image cannot be found. Whether this explains the historical
   customer 503s or login failure is unverified.
2. **Medium confidence, current lab state:** the ingress host may be
   misspelled. Confirm the intended host and ingress setup before changing it.
3. **Low confidence, current lab state:** a missing Service endpoint explains
   the current outage. The observed Service has two endpoints; the fixture's
   old selector is not the current selector.

## Ruled out

The current portal-web Service has no missing-endpoint condition in this
inspection. No historical cause is ruled out from this later cluster snapshot.

## Recommended next action and escalation

Hand over to Resolver. Ask APP-PORTAL-L2 and K8S-PLATFORM-L3 to confirm an
approved API image, intended ingress host and end-to-end verification path.
Propose a scoped plan with pre-checks and rollback; obtain the required human
approvals before execution. Do not reapply the stale Service selector fix.
