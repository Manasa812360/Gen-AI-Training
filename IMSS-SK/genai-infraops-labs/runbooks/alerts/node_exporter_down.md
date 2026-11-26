# Runbook: Node Exporter Down

| Field | Value |
|---|---|
| Applies to | Node Exporter targets firing `NodeExporterDown` for 5 minutes |
| Owner group | LINUX-L2 |
| Risk | Medium |
| Approval needed | Yes, before restarting the exporter or host |

## 1. Purpose

1. Restore host metric collection while distinguishing an exporter failure from host, network, container, or Prometheus scrape failure.

## 2. Pre-checks (read-only)

1. Confirm the failing target and scrape error: `curl -fsS http://127.0.0.1:9090/api/v1/targets`.
2. Check Prometheus health: `curl -fsS http://127.0.0.1:9090/-/ready`.
3. For the lab stack, check container state: `docker compose -f monitoring/docker-compose.yml ps`.
4. Inspect the exporter endpoint from the Prometheus network: `docker compose -f monitoring/docker-compose.yml exec -T prometheus wget -qO- http://node-exporter:9100/metrics >/dev/null`.
5. Review exporter logs without restarting: `docker compose -f monitoring/docker-compose.yml logs --tail=100 node-exporter`.
6. Confirm host reachability and whether other targets are failing at the same time.
7. Stop and escalate if the host itself is unavailable or multiple Prometheus targets are failing.

## 3. Steps (numbered, one action each, exact command)

1. For an isolated, stopped exporter container, obtain approval to restart it.
2. Restart only the exporter service: `docker compose -f monitoring/docker-compose.yml restart node-exporter`.
3. Record the container state, error, approval, and restart timestamp in the incident.

## 4. Verification (command + expected result)

1. Verify the exporter endpoint: `docker compose -f monitoring/docker-compose.yml exec -T prometheus wget -qO- http://node-exporter:9100/metrics >/dev/null`.

   Expected output: Command exits with status `0`.

2. Verify container state: `docker compose -f monitoring/docker-compose.yml ps node-exporter`.

   Expected output: Container state is `running`.

3. Verify the Prometheus target returns to `up` for the `node` job.
4. Verify the `NodeExporterDown` alert resolves after its 5-minute `for` period.

## 5. Rollback

1. Stop further restarts if a single approved restart does not restore the target.
2. Preserve exporter and Prometheus logs for investigation.
3. Restore the previously working container image or approved configuration only through a normal change record.
4. Do not restart the host as an implicit rollback.

## 6. Escalate when

1. Escalate to the host owner immediately if the target cannot be reached.
2. Escalate to LINUX-L2 if the container repeatedly exits or Prometheus reports scrape errors after one restart.
3. Escalate to NETWORK-L2 if only network-isolated targets fail or connectivity tests fail.
4. Escalate to the monitoring platform owner if multiple targets fail simultaneously.
5. Escalate to the incident commander if host health visibility is unavailable during a business-impacting incident.

## 7. Change history

1. 2026-11-25 - Created from the `NodeExporterDown` alert troubleshooting checklist.
