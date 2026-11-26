# Proposed parent incident: Customer Portal alert storm

Status: draft; desk lead review required. Correlation is not proof of cause.

The supplied alert data contains 18 Customer Portal alerts between 14:03:00 and
14:08:41 IST on 2026-11-12. Propose a single parent incident for these alerts:
CAPALR-000 through CAPALR-017. CAPALR-000 is the earliest critical alert and a
candidate lead alert, not an established root cause.

The Module 6 correlator uses fixed five-minute windows and produced two
Customer Portal groups (15 and 3 alerts). The common service and ongoing
symptoms justify proposing their consolidation for human review, not changing
the tool's window or claiming the groups were automatically merged.

CAPALR-018 and CAPALR-019 concern Finance Reporting, a different CMDB service.
Keep them as a separate group pending evidence of a relationship; do not attach
them to the portal parent just to force all 20 alerts into one incident.
