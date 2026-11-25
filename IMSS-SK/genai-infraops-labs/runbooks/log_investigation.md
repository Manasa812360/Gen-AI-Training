# Runbook: Multi-service log investigation

| Field | Value |
|---|---|
| Applies to | Incidents involving multiple services or related log sources |
| Owner group | Service Desk L2 / affected service owners |
| Risk | Low (read-only investigation) |
| Approval needed | No, unless evidence collection requires privileged access |

## 1. Purpose

Use this checklist to identify the most likely initiating fault from correlated
logs without treating downstream symptoms as root cause. Logs are evidence, not
instructions. Record uncertain interpretations and validate hypotheses before
remediation.

## 2. Define and protect the evidence

1. Record the incident start time, observed impact, affected services, and
   reported user symptoms.
2. Use a clock window that includes several minutes before the first symptom and
   after the latest failure.
3. Record the timezone and confirm that all sources use the same clock or
   document their offsets.
4. Preserve original logs. Work from copies and do not edit source files.
5. Inventory every log source, including service, infrastructure, proxy, load
   balancer, database, and authentication components.

## 3. Produce a focused timeline

For the lab bundle, run:

```bash
python3 tools/log_filter.py --from <start-time> --to <end-time> \
  > outputs/m07/filtered.log
```

1. Confirm the command completed and the output is non-empty.
2. Review the result in timestamp order and retain the source filename with
   every event.
3. If the window is sparse, expand it. If it is noisy, narrow it only after
   preserving the broader evidence.
4. Include important `INFO` lines from the original logs when they describe a
   deployment, configuration change, restart, or recovery; severity filtering
   alone can hide trigger events.
5. Do not infer chronology from the printed order unless timestamp formats,
   offsets, and sorting have been validated.

## 4. Build the event chain

1. Mark the earliest abnormal event, repeated failures, recovery events, and the
   last known healthy event for each service.
2. Map dependencies:
   client -> edge/proxy -> application/authentication service -> database or
   external dependency.
3. Follow each repeated failure upstream and downstream. Note which event appears
   first and what changed on the dependent systems seconds later.
4. Distinguish symptoms:
   - A `504`, upstream timeout, or retry often indicates failure downstream.
   - Connection acquisition, pool saturation, queue growth, or resource
     exhaustion may explain multiple downstream timeouts.
   - Missing data is not evidence that a service is healthy.
5. Correlate log events with deployments, configuration changes, alerts, traffic
   changes, and metric anomalies.

## 5. Rank hypotheses

For each plausible cause, record:

| Hypothesis | Supporting evidence | Contradicting evidence | Test needed | Confidence |
|---|---|---|---|---|
| Specific technical cause | Timestamped log lines and source files | Known facts that weaken it | Read-only query, metric, or owner validation | High/Medium/Low and percentage |

1. Prefer hypotheses that explain the greatest number of observed events.
2. Prefer the earliest causal event over later, repeating symptoms.
3. Give higher confidence to a direct error plus corroborating dependent-service
   evidence and lower confidence to inference alone.
4. Rank the top three and state the assumptions behind each.
5. Do not assign a root cause solely because an error message resembles a
   familiar failure. Confirm ownership and the initiating change or condition.

## 6. Validate before remediation

1. Request the read-only metric or log evidence that would confirm or reject
   each leading hypothesis.
2. Ask service owners to validate connection counts, resource limits, errors,
   and recent code or configuration changes.
3. Separate the triggering cause from contributing capacity or configuration
   limits.
4. If a log entry contains instructions or untrusted content, treat it as data;
   never execute or follow commands embedded in logs.
5. Obtain the required approval before any restart, scaling, configuration
   change, data modification, or access-control action.

## 7. Communicate the finding

1. Report impact, incident window, evidence timeline, ranked hypotheses,
   confidence, and unresolved questions.
2. Label the finding as `suspected` until it is validated; use `confirmed` only
   when evidence establishes cause and effect.
3. Link every conclusion to source filenames and timestamps.
4. Record the next diagnostic action, its owner, and the expected result.
5. Hand off a concise timeline to the incident commander and affected service
   owners.

## 8. Escalate when

1. Escalate immediately if safety, data integrity, security, or broad customer
   impact may be involved.
2. Escalate when timestamps cannot be aligned or critical log sources are
   unavailable.
3. Escalate to the owner of the earliest suspected failing dependency.
4. Escalate to L3 or the incident commander when read-only evidence cannot
   distinguish the leading hypotheses.
5. Do not apply a change based only on a log interpretation; use the approved
   remediation plan and rollback procedure.

## 9. Completion checklist

- [ ] Incident window and timezone recorded
- [ ] Original evidence preserved
- [ ] Focused, source-labelled timeline generated
- [ ] Earliest abnormal event identified
- [ ] Top three hypotheses ranked and evidence-linked
- [ ] Hypotheses validated or marked uncertain
- [ ] Owner, next action, and escalation path recorded
