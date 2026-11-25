# Evidence Pack - INC0010260

## Summary

The customer portal was unreachable with HTTP 503 because the `portal-web`
Service had no live upstream endpoints. The Service selector has now been
corrected and resolves to two running pods. Additional suspected faults remain
outside the investigator's read-only scope.

## Timeline (IST)

- 2026-11-09 09:05:03: nginx logged `no live upstreams -> 503`.
- 2026-11-09 09:05:10: The 503 condition was repeated.
- 2026-11-09 09:36:00: INC0010260 was opened by Pune Office.

## Evidence

Evidence verified with `kubectl` after the selector correction:

1. `portal-web ClusterIP 10.96.158.49 <none> 80/TCP 84m app=portal-web`
2. `portal-web 10.244.0.8:80,10.244.0.9:80 84m`

The first line confirms the Service selector is `app=portal-web`. The second
confirms that the Service now has two endpoints.

## Ranked hypotheses

1. **Incorrect `portal-web` Service selector - High**
   - The prior selector did not match the running pods.
   - The Service had no endpoints, matching the `no live upstreams` 503 errors.
   - The corrected selector now resolves to two endpoints.
2. **Invalid `portal-api` image tag - High**
   - `portal-api` was observed in `ImagePullBackOff`.
   - Its configured image is `nginx:1.27-alpine-hotfx`.
   - The deployment reported zero available replicas.
3. **Ingress hostname typo - Medium**
   - The configured host is `portal.exmaple-corp.local`.
   - This may affect hostname routing but does not explain the directly observed
     lack of Service endpoints.

## Ruled out

- Insufficient running web pods: both `portal-web` pods were `Running` and
  `1/1 Ready`.
- Immediate capacity scaling: the direct 503 cause was the absence of Service
  endpoints, not exhausted web-pod capacity.

## Recommended next action

The investigation is complete. Refusing to perform further remediation because
the investigator is read-only.

**Hand over to Resolver.**

The Resolver should investigate the `portal-api` image pull failure and confirm
whether the ingress hostname is intended, then validate the portal end to end.

## Escalation target

`APP-PORTAL-L2`
