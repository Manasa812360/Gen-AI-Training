# Runbook Q&A prompt tests

## 1. How should L1 troubleshoot recurring VPN disconnects?

Ask whether the password has expired and use the self-service reset process if it has (`runbooks/vpn_troubleshooting.md`, step 1). Check the client version; version 5.3.x has a known MTU issue (`runbooks/vpn_troubleshooting.md`, step 2). For 5.3.x, set MTU 1350 or reinstall 5.2.1, then clear the cached profile and reconnect (`runbooks/vpn_troubleshooting.md`, steps 3–4). Escalate to NETWORK-L2 if more than three users at one site are affected or step 3 does not help (`runbooks/vpn_troubleshooting.md`, escalation criteria).

## 2. How do I reset a user's password?

Verify the employee ID, manager name and registered callback number before resetting (`runbooks/password_reset.md`, step 1). Reset the password in AD tools and require a password change at next logon (`runbooks/password_reset.md`, step 2). Read the password on the verified call only and never send it by email or chat (`runbooks/password_reset.md`, step 3). Record the verification method and escalate to WINTEL-L2 when identity cannot be verified or the account is privileged (`runbooks/password_reset.md`, step 4 and escalation criteria).

## 3. What is required before restarting a Kubernetes deployment?

Check the deployment and rollout history first (`runbooks/k8s_pod_restart.md`, step 1). Submit a remediation plan containing the restart and undo commands (`runbooks/k8s_pod_restart.md`, step 2). Execute the approved plan through the approval tool, then verify rollout status (`runbooks/k8s_pod_restart.md`, steps 3–4).

## 4. What should L2 check first when the customer portal is unreachable?

Confirm whether one user, one site or all users are affected, then check the status page and open P1/P2 incidents (`runbooks/portal_unreachable.md`, step 1). Check ingress, endpoint readiness, pod readiness and recent events in that order (`runbooks/portal_unreachable.md`, steps 2–5). Also check changes from the previous 24 hours (`runbooks/portal_unreachable.md`, step 6). Any cluster-changing fix requires a remediation plan and L2/L3 approval (`runbooks/portal_unreachable.md`, change-approval note).

## 5. How do I reset the SAN switch?

No runbook covers this - escalate to L2

## Verification

- Questions tested: 5
- Questions with supported, step-specific citations: 4
- Unsupported questions: 1
- Invented procedure for the unsupported question: No
