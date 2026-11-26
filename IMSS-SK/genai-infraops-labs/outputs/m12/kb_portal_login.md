# Draft KB - Portal login 503 or slow reports

**Audience:** Service Desk. **Status:** Draft; owner review required.

## Symptoms

Customers report portal login errors or slow report pages. A 503 or a slow page
alone does not identify the cause.

## Read-only checks

1. Record the start time, affected service and scope without collecting
   passwords or personal details in AI prompts.
2. Review current alerts and existing incident records; link related reports
   only after the desk lead confirms the relationship.
3. Ask the platform team to check the portal Service endpoints, pod readiness,
   API image-pull events and ingress host against approved configuration.
4. Escalate to APP-PORTAL-L2 and K8S-PLATFORM-L3 with sanitised evidence.

## Resolution and verification

Do not apply a fix from this draft. A resolver must propose an evidence-based
plan with rollback and obtain task-specific approval. After execution, verify
the technical checks and an approved end-to-end login path, then obtain
service-owner confirmation before closing customer tickets. No resolution has
yet been verified for this capstone.
