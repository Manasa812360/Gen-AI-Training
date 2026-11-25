# Runbook: High CPU

| Field | Value |
|---|---|
| Applies to | Linux hosts firing `HighCPU` for 5 minutes |
| Owner group | LINUX-L2 |
| Risk | Medium |
| Approval needed | Yes, before stopping or restarting a process |

## 1. Purpose

1. Identify the workload responsible for sustained CPU use and restore normal service without terminating an unidentified process.

## 2. Pre-checks (read-only)

1. Confirm the alert instance and timing in Prometheus before acting.
2. Confirm the affected host: `hostnamectl --static`.
3. Review load and running processes: `uptime; top -b -n 1 -o %CPU | head -30`.
4. Review sustained process CPU: `ps -eo pid,ppid,user,%cpu,%mem,etime,cmd --sort=-%cpu | head -20`.
5. Check service health for the leading process: `systemctl status <service> --no-pager`.
6. Check recent deployments or planned changes for the affected service.
7. Stop and escalate if the host is shared, the workload is unknown, or the alert is limited to a short collection spike.

## 3. Steps (numbered, one action each, exact command)

1. If a documented containerized workload is responsible, inspect it without changing state: `docker stats --no-stream`.
2. Collect recent application or service errors: `sudo journalctl -u <service> --since '30 minutes ago' --no-pager`.
3. Obtain approval from the service owner or incident commander before changing the workload.
4. Restart a documented service only when its owner approves the action: `sudo systemctl restart <service>`.
5. Record the command, approval, operator, and timestamp in the incident.

## 4. Verification (command + expected result)

1. Verify host CPU and load: `top -b -n 1 -o %CPU | head -20`.

   Expected output: CPU use and load trend downward without repeated near-100% usage.

2. Verify service state: `systemctl status <service> --no-pager`.

   Expected output: `Active: active (running)` and no new failure.

3. Verify the Prometheus alert has returned to the inactive state after its configured evaluation interval.
4. Confirm the dependent application health check and user-facing service both respond normally.

## 5. Rollback

1. If the approved restart causes a new failure, record the failure before taking further action.
2. Roll back only to the previously deployed version using the service's approved deployment procedure.
3. Do not use an ad hoc process stop, package removal, or configuration rollback.
4. Escalate if the prior version cannot be restored safely.

## 6. Escalate when

1. Escalate to the application owner when CPU is driven by an identified application process.
2. Escalate to LINUX-L2 immediately if load continues to rise, the host becomes unresponsive, or the process is in kernel space.
3. Escalate to the incident commander if multiple hosts or a business service are affected.
4. Escalate after one approved restart; do not repeatedly restart a service.
5. Escalate any suspected malicious process to SECOPS without terminating it.

## 7. Change history

1. 2026-11-25 - Created from the `HighCPU` alert troubleshooting checklist.

