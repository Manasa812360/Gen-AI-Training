# Permanent fix change record - draft

- **Service:** Customer Portal
- **Owner:** APP-PORTAL-L2 and K8S-PLATFORM-L3 to nominate a change owner.
- **Problem:** Portal alerts and login complaints followed a reported release;
  historical root cause remains unconfirmed. Current lab findings are in
  `evidence_pack.md`.
- **Proposed scope:** Confirm the intended API image and ingress host. Once
  established, correct version-controlled deployment configuration and add
  image availability, rollout and end-to-end login checks to the release
  process. Preserve an approved rollback artifact.
- **Pre-checks:** Validate scope, current image and ingress, service endpoints,
  image provenance, permissions and the approved maintenance window.
- **Implementation:** To be specified after the service owners identify the
  correct image, host and release pipeline; review a concrete plan before use.
- **Verification:** Test the configuration and pipeline in non-production,
  inspect rollout and endpoints, and exercise an approved end-to-end login
  path. Service owner must confirm success.
- **Backout:** Restore the last approved configuration and deploy an approved
  prior image; exact commands and artifact availability must be established.
  **Backout is untested.**
- **Risk:** Not scored. Change Manager must apply
  `data/changes/change_risk_rubric.md` once scope, history and timing are known.
  Obtain any required CAB and InfraSec sign-offs.
- **Approvals:** Team lead, service owner and change authority before production
  execution; no approvals have been recorded for this change.
