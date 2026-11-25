# Parent Incident: GRP-0001

- **Short description:** Finance Reporting degraded by high load, disk pressure, and slow queries
- **Business service:** Finance Reporting
- **Impact:** Production reporting on `srv-fin-app-02` and `srv-fin-db-01` is likely degraded or unavailable. Finance users may experience slow reports, failed queries, or timeouts.
- **Probable cause (hypothesis):** Resource pressure on `srv-fin-app-02`, including high CPU/load and low disk space, may be increasing query latency or causing failures on `srv-fin-db-01`. The alerts establish correlation, not root cause.
- **First 3 read-only checks:**
  1. On `srv-fin-app-02`: `uptime; top -b -n 1 -o %CPU | head -30; df -h /var; df -i /var`.
  2. On `srv-fin-db-01`: `uptime; top -b -n 1 -o %CPU | head -30; sudo ss -ltnp | grep -E ':5432|:3306'`.
  3. From the documented monitoring view, compare the five-minute CPU, load, disk, query-latency, and target-health timelines for both hosts.
- **Owner group:** LINUX-L2
- **Runbook:** TBD
- **Linked child alerts:** ALR-9027, ALR-9026, ALR-9002, ALR-9007, ALR-9017, ALR-9028, ALR-9025, ALR-9009, ALR-9001, ALR-9006, ALR-9024, ALR-9016, ALR-9030, ALR-9008, ALR-9015, ALR-9010, ALR-9003, ALR-9019, ALR-9014
- **Root alert:** ALR-9011
- **Suggested priority:** P2
- **Priority reasoning:** Impact 2 because a production business service is degraded across its application and database components. Urgency 1 because repeated critical alerts and query/target-down signals indicate active operational risk; user confirmation is still required. Impact 2 + urgency 1 maps to P2.
- **Human review:** Confirm reported user impact and work-stoppage status before finalizing priority; if reporting is confirmed fully unavailable, reassess the impact as 1 for P1 consideration.
