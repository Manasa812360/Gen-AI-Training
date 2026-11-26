# Daily Kubernetes Cluster Health Checklist

Use the correct production or operational context and run all checks read-only. Record the UTC timestamp, operator, context, exceptions, and incident/change references with the results.

## 1. Access and versions

- [ ] Record the current context: `kubectl config current-context`
- [ ] Confirm API and client access: `kubectl version`
- [ ] Confirm client/server skew is within the supported range.

Good: API responds and the intended context is active.

## 2. Node health and capacity

- [ ] Check node state: `kubectl get nodes -o wide`
- [ ] Check pressure conditions: `kubectl describe nodes`
- [ ] Check node consumption: `kubectl top nodes`

Good: all expected nodes are `Ready`; no disk, memory, PID, or network pressure; capacity has operational headroom. If metrics are unavailable, report that limitation and use node conditions plus monitoring.

## 3. Control plane and system workloads

- [ ] Inspect system pods: `kubectl get pods -n kube-system -o wide`
- [ ] Check supporting namespaces: `kubectl get pods -n local-path-storage -o wide`
- [ ] Check control-plane component health where supported: `kubectl get componentstatuses`

Good: expected controllers are Running and Ready, with stable restart counts. Treat deprecated `componentstatuses` as supplemental, not authoritative.

## 4. Cluster workload health

- [ ] Find unhealthy pods: `kubectl get pods -A --field-selector=status.phase!=Running -o wide`
- [ ] Review all pod states: `kubectl get pods -A -o wide`
- [ ] Review namespace deployments: `kubectl get deployments -A`

Good: no unexplained Pending, CrashLoopBackOff, ImagePullBackOff, or NotReady workloads; all expected replicas are available.

## 5. Networking

- [ ] Review Services: `kubectl get svc -A`
- [ ] Review endpoints: `kubectl get endpoints -A`
- [ ] Review ingresses: `kubectl get ingress -A -o wide`
- [ ] Investigate empty endpoints by comparing Service selectors with pod labels.

Good: required Services have ready endpoints and ingress resources have valid backends and expected addresses.

## 6. Storage

- [ ] Review claims: `kubectl get pvc -A`
- [ ] Review volumes: `kubectl get pv`
- [ ] Review storage classes: `kubectl get storageclass`

Good: required claims and volumes are Bound and the expected default StorageClass is present.

## 7. Events and capacity failures

- [ ] Review cluster warnings: `kubectl get events -A --field-selector=type=Warning --sort-by=.lastTimestamp`
- [ ] Review priority namespaces: `kubectl get events -n <namespace> --sort-by=.lastTimestamp`

Good: no recurring scheduling, image-pull, mount, eviction, readiness, authentication, quota, or restart failures.

## 8. Rollouts and recent changes

- [ ] Review deployments with incomplete availability: `kubectl get deployments -A`
- [ ] Review relevant revisions: `kubectl rollout history deployment/<name> -n <namespace>`
- [ ] Compare recent warning times with approved changes.

Good: rollout revisions are expected, available replicas match desired replicas, and no unapproved change correlates with degradation.

## 9. Escalation

Create an incident/escalation when:

- a node becomes NotReady;
- control-plane or DNS workloads are unhealthy;
- critical Services have no endpoints;
- scheduling failures persist;
- restarts or warnings are increasing;
- metrics required for an operational decision are unavailable;
- a critical rollout is incomplete or unapproved.

Attach command outputs, timestamps, affected namespaces, ruled-out causes, suspected cause, and requested action. Do not apply, delete, scale, restart, or edit resources as part of the daily health check.
