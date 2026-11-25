# Daily Cluster Health Snapshot

Date: 2026-11-25  
Context: `kind-genai-labs`

## Summary

Overall: **CRITICAL / escalation required**

| Check | Result | Status |
|---|---|---|
| Kubernetes API | Responsive; client v1.35.10, server v1.31.0 | Warn: version skew exceeds supported range |
| Nodes | One control-plane node Ready | Good |
| Control-plane components | Scheduler, controller manager, and etcd reported Healthy | Good |
| System workloads | All `kube-system` pods Running and Ready | Good |
| Metrics | Metrics API unavailable | Warn: resource trend cannot be checked |
| Portal web | Two pods Running and Ready, zero restarts | Good |
| Portal routing | Service has no endpoints | Critical |
| Portal API | ImagePullBackOff | Critical |
| Analytics batch | Pending due to insufficient CPU and memory | Critical |
| Report worker | CrashLoopBackOff with repeated restarts | Critical |
| Ingress | No assigned address | Critical |

## Evidence

```text
genai-labs-control-plane   Ready   control-plane   v1.31.0

portal-web pods:
  2/2 Running and Ready

service/portal-web:
  selector app=portal-web-v2
  endpoints <none>

portal-api:
  0/1 ImagePullBackOff

analytics-batch:
  0/1 Pending
  0/1 nodes available: Insufficient cpu, Insufficient memory

report-worker:
  0/1 CrashLoopBackOff
```

## Operational notes

- Early `NodeNotReady` warnings occurred during cluster startup; the node is now Ready and its control-plane pods are healthy.
- The portal Service selector does not match portal web pod labels.
- The portal API image tag does not exist.
- The daily snapshot was read-only; no resources were changed.
