# L2-to-L3 Escalation Pack — INC0010260

## Summary

Pune customer portal requests return HTTP 503. Frontend pods are healthy, but the Service has no ready endpoints. The ingress also has no assigned address.

## Evidence

- `endpoints/portal-web`: `<none>`
- Service selector: `app=portal-web-v2`
- Frontend pod label: `app=portal-web`
- Two frontend pods: `1/1 Running`, zero restarts
- API pod: `0/1 ImagePullBackOff`
- Events report that the configured API image was not found
- Ingress, Service, and deployments are revision/generation 1 with no change cause recorded

## Ruled out

- Frontend pod crash
- Frontend readiness failure
- Cluster-wide outage: the node is Ready and system pods are Running
- Repeated frontend restarts

## Suspected cause

The Service selector does not match frontend pod labels, leaving the ingress backend without endpoints and producing the 503. Invalid ingress publication/configuration and the API image failure are additional faults.

## Requested action

Validate the intended routing and DNS configuration, correct the Service selector, restore the API image, validate ingress publication, and confirm an end-to-end portal request. Apply all cluster changes only through the approved change process.
