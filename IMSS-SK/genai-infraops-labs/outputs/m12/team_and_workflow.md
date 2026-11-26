# Capstone team and workflow

Branch: `team/desklead`; intended PR base: `main`.

| Role | Team member |
|---|---|
| Desk lead | A |
| Investigator | B |
| Approver | C |
| Communicator | D |
| Presenter | D |

1. Sanitise the source tickets and obtain a named redaction sign-off.
2. Generate schema-valid triage and run the confidence router. A reviews all
   P1/P2, VIP, security and low-confidence items before any ticket changes.
3. Review the proposed portal parent incident and separate Finance alerts.
4. B verifies the evidence pack and hands an evidence-based plan to the
   Resolver; cluster observations are not historical incident evidence.
5. C reviews and rejects or approves specific plans. An approved plan requires
   separate execution confirmation; record outcomes and verification.
6. D reviews the customer, bridge, RCA, KB and change drafts before publication.
7. Prepare a PR only after reviewing its complete diff for sensitive material,
   including prior branch history, and present the verified workflow and audit.

The current triage and communications are drafts. No tickets, customer
messages or incident records have been updated.
