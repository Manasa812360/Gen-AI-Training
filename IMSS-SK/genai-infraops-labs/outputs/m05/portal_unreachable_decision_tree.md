# INC0010260: Portal Unreachable Decision Tree

All commands are read-only.

| Node | Command | Good | Bad | Next |
|---|---|---|---|---|
| DNS | Resolve the ingress host from the affected network with `getent hosts <host>` or `nslookup <host>` | Correct ingress/LB address and consistent resolution | Missing, incorrect, or inconsistent resolution | Ingress |
| Ingress | `kubectl get ingress portal -n portal -o wide`; `kubectl describe ingress portal -n portal` | Expected host and path, assigned address, valid `portal-web:80` backend, no warning events | No address, wrong host/path/class, missing backend, or configuration error | Service endpoints |
| Service endpoints | `kubectl get svc portal-web -n portal -o wide`; `kubectl get endpoints portal-web -n portal`; `kubectl get endpointslice -n portal -l kubernetes.io/service-name=portal-web` | Service port exists and EndpointSlice contains ready addresses on the target port | `<none>`, empty EndpointSlice, wrong port, or selector that does not match pod labels | Pod status |
| Pod status | `kubectl get pods -n portal -o wide`; `kubectl describe pod <pod> -n portal` | Required pods are Running and Ready with stable restart counts | Pending, crash loop, image pull failure, not-ready containers, or increasing restarts | Events |
| Events | `kubectl get events -n portal --sort-by=.lastTimestamp` | Only expected normal lifecycle events and no recent warnings | Pull, scheduling, mount, readiness, quota, or restart failures near incident start | Recent change |
| Recent change | `kubectl rollout history deployment/portal-web -n portal`; `kubectl rollout history deployment/portal-api -n portal`; review approved change records | Revision, images, selectors, and host match the approved release | Unapproved or failed change, revision mismatch, or configuration altered at incident time | Document cause; prepare approved remediation |

## Escalation gate

Escalate to `K8S-PLATFORM-L3` for a cluster/node-wide issue, unresolved cause after 30 minutes, or any remediation requiring cluster changes without approval.
