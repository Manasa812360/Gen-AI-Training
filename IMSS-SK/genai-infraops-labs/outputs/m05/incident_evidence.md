# INC0010260: Decision-Tree Evidence

Snapshot date: 2026-11-25

## 1. DNS

Command result for the configured ingress host:

```text
** server can't find portal.exmaple-corp.local: SERVFAIL
```

Assessment: **Bad.** The configured name does not resolve from this diagnostic host and appears misspelled. The result must be repeated from the affected Pune network before attributing the customer failure to DNS.

## 2. Ingress

```text
NAME     CLASS    HOSTS                       ADDRESS   PORTS
portal   <none>   portal.exmaple-corp.local             80

Rules:
  portal.exmaple-corp.local
    /   portal-web:80
```

Assessment: **Bad.** No external address is assigned. The host is suspicious, class is unset, and no ingress events are present.

## 3. Service endpoints

```text
service/portal-web   ClusterIP   10.96.158.49   80/TCP   app=portal-web-v2
endpoints/portal-web <none>
```

Pod labels are `app=portal-web`, while the Service selector is `app=portal-web-v2`.

Assessment: **Bad and directly consistent with HTTP 503.** There are no Service endpoints.

## 4. Pod status

```text
portal-web-854fb64865-dq6rn   1/1   Running             0
portal-web-854fb64865-p2vnv   1/1   Running             0
portal-api-85ffb49f46-sqkbr   0/1   ImagePullBackOff   0
```

Assessment: **Mixed.** Both web pods are ready but excluded by the selector. The API pod has an independent image failure.

## 5. Events

```text
Failed to pull image "nginx:1.27-alpine-hotfx": ... not found
Error: ErrImagePull
Error: ImagePullBackOff
FailedScheduling: 0/1 nodes are available: 1 Insufficient cpu, 1 Insufficient memory
Back-off restarting failed container worker in report-worker
```

Assessment: **Bad.** Events confirm the API image failure and additional unrelated workload failures. Selector mismatches do not necessarily generate warning events.

## 6. Recent change

```text
deployment.apps/portal-web   REVISION 1   CHANGE-CAUSE <none>
deployment.apps/portal-api   REVISION 1   CHANGE-CAUSE <none>
```

Ingress, Service, and portal deployments were created at `2026-11-25T20:58:35Z`, after the ticket timestamp. The draft change record has no evidence of execution. The original incident timeline cannot be established from this cluster alone.

## Confirmed ranking

1. Service selector mismatch leaves the ingress backend without endpoints.
2. Ingress has no assigned address and its host appears malformed.
3. API image is not present, causing `ImagePullBackOff`.
