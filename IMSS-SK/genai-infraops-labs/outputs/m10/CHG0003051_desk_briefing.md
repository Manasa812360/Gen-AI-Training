# Service Desk briefing — CHG0003051

## Purpose

The change prevents failed database migrations from being reported as successful portal releases and preserves an approved rollback image.

## Window

Thursday 23:00–01:00 IST; **verify the calendar date before use**.

## Expected calls

- Customers ask whether the portal will be unavailable.
- Customers report a brief login error during validation.
- Users ask whether a saved or retrying login request has failed.

Brief interruptions are possible, but sustained login failure or a repeated HTTP 5xx response is unexpected and must be escalated.

## Scripted answer

“We are carrying out approved maintenance to improve Customer Portal release safety and recovery. A brief login interruption may occur until 01:00 IST. Please retry after a few minutes. No account reset is required. We are monitoring the service and will provide the next update within the agreed incident cadence.”

Do not promise a restoration time beyond the approved window. Do not advise password resets unless a separate identity fault is confirmed.

## Escalation

1. Record the time, error shown, affected URL or login step, and caller location.
2. Link reports to CHG0003051 and the active incident, if one exists.
3. Escalate immediately to APP-PORTAL-L2 for repeated login failure or HTTP 5xx.
4. Notify the Change Manager and Platform team if the threshold is exceeded, validation fails or the rollback image is unavailable.
5. Escalate any multi-user or customer-wide impact to the Major Incident process.
6. Do not propose or execute production changes through the Service Desk.

## Next update

At the window start, after technical validation, and at closure. During an incident, follow the active Major Incident communication cadence.
