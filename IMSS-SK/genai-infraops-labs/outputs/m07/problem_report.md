# Problem candidate report

Source: `outputs/m07/clusters.csv` generated with `--k 10` from 200 resolved
tickets covering approximately three months.

Monthly effort uses:

`(cluster tickets / 3 months) x mean handle_time_min / 60`.

Root causes below are hypotheses until confirmed by Problem Management.

## Cluster names

| Cluster | Name (6 words or fewer) |
|---|---|
| 3 | VPN disconnects after client update |
| 1 | Repeated account lockouts |
| 5 | Laptop and portal slow response |
| 2 | Password reset requests |
| 4 | Outlook profile loading failures |
| 0 | Printer queue stuck |
| 6 | Mailbox quota full |
| 7 | New-joiner account provisioning |
| 8 | `/var` disk space exhaustion |
| 9 | Shared-drive access denied |

## Top five Problem candidates

### 1. Recurring endpoint high CPU

- **Problem statement:** Laptops repeatedly become very slow with high CPU,
  requiring L2 intervention.
- **Suspected root cause (HYPOTHESIS):** A stuck Windows update loop repeatedly
  consumes CPU until the update process is disabled or cleared.
- **Cluster:** 5, 26 tickets, mean handle time 48.58 minutes.
- **Monthly effort:** `(26 / 3) x 48.58 / 60 = 7.02 hours`.
- **Evidence tickets:** `INC0008007`, `INC0008024`, `INC0008051`. All three
  report high CPU or a very slow laptop, and resolution notes identify a stuck
  Windows update loop.
- **Workaround in use:** Disable the stuck update loop and clear temporary files.
- **KB gap:** Yes. No applicable laptop high-CPU/Windows-update KB exists in
  `data/kb/`.
- **Review note:** Cluster 5 also contains portal performance tickets. Its total
  effort is therefore a mixed-cluster estimate; Problem Management should split
  endpoint and portal records before finalising the scope.

### 2. VPN disconnects after update

- **Problem statement:** VPN sessions disconnect repeatedly after the client
  update, producing recurring Network L2 work.
- **Suspected root cause (HYPOTHESIS):** VPN client 5.3 has an MTU-related
  incompatibility affecting connectivity to `vpn-gw-pune-01`.
- **Cluster:** 3, 33 tickets, mean handle time 28.73 minutes.
- **Monthly effort:** `(33 / 3) x 28.73 / 60 = 5.27 hours`.
- **Evidence tickets:** `INC0008006`, `INC0008029`, `INC0008030`. All three
  report repeated VPN disconnects after a client update and cite the same
  workaround and MTU issue.
- **Workaround in use:** Reinstall client 5.2.1, clear the cached profile, and
  set MTU 1350.
- **KB gap:** Yes. `KB0001_vpn_basic.md` covers failed connections but omits the
  repeated-disconnect/MTU symptom and stale known-client-version guidance.

### 3. Repeated account lockouts

- **Problem statement:** Accounts repeatedly lock despite successful user
  password resets, generating recurring Wintel L2 work.
- **Suspected root cause (HYPOTHESIS):** Cached stale credentials in a mobile
  mail application continue authenticating with an old password.
- **Cluster:** 1, 26 tickets, mean handle time 24.42 minutes.
- **Monthly effort:** `(26 / 3) x 24.42 / 60 = 3.53 hours`.
- **Evidence tickets:** `INC0008005`, `INC0008011`, `INC0008012`. All three
  report repeated lockouts and identify stale mobile-mail credentials in the
  resolution notes.
- **Workaround in use:** Remove the old mobile-mail account, add corrected
  credentials, and unlock the AD account.
- **KB gap:** Yes. Existing password-reset guidance does not cover diagnosis of
  stale credentials causing repeated lockouts.

### 4. Outlook profile loading failures

- **Problem statement:** Outlook repeatedly hangs while loading a profile,
  although webmail remains available.
- **Suspected root cause (HYPOTHESIS):** A damaged or inconsistent local Outlook
  profile/OST is preventing normal client startup.
- **Cluster:** 4, 20 tickets, mean handle time 24.95 minutes.
- **Monthly effort:** `(20 / 3) x 24.95 / 60 = 2.77 hours`.
- **Evidence tickets:** `INC0008026`, `INC0008052`, `INC0008059`. All three
  report Outlook not opening during profile loading and were restored by
  rebuilding the profile and OST.
- **Workaround in use:** Recreate the Outlook profile, rebuild the OST, and use
  webmail while Outlook is repaired.
- **KB gap:** Yes. No Outlook profile/OST troubleshooting article exists in
  `data/kb/`.

### 5. Print jobs stuck in queue

- **Problem statement:** Jobs repeatedly become stuck for printer
  `prn-pune-3f-01`, affecting multiple teams.
- **Suspected root cause (HYPOTHESIS):** The print spooler or printer firmware
  state can become unhealthy and retain queued jobs.
- **Cluster:** 0, 18 tickets, mean handle time 20.33 minutes.
- **Monthly effort:** `(18 / 3) x 20.33 / 60 = 2.03 hours`.
- **Evidence tickets:** `INC0008000`, `INC0008001`, `INC0008010`. All three
  concern stuck jobs for the same printer and use the same spooler/firmware
  remediation.
- **Workaround in use:** Restart the print spooler, clear stuck jobs, and update
  printer firmware.
- **KB gap:** Yes. No stuck-print-queue or `prn-pune-3f-01` KB exists in
  `data/kb/`.

## Evidence confirmation

Three evidence tickets per candidate were opened from the source CSV and checked
for matching category, symptom, and resolution. Cluster 5's mixed endpoint/portal
membership is explicitly called out rather than treating the cluster as one
confirmed cause.
