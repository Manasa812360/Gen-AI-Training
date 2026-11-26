# Eight-minute capstone presentation - outline

This is a draft for D; replace pending items only with verified outcomes.

| Time | Topic |
|---|---|
| 0:00-1:00 | Scenario, team roles and the proposed Customer Portal parent incident. |
| 1:00-2:00 | Redaction, human review and the missed CAP003 password that was caught and manually removed. |
| 2:00-3:00 | Schema-valid triage, duplicate follow-up, VIP and security review queues. |
| 3:00-4:00 | Two portal alert groups and the separate Finance group; why correlation is not causation. |
| 4:00-5:00 | Read-only evidence: API image failure, live Service endpoints, and the historical-versus-lab timing caveat. |
| 5:00-6:00 | Review the actual rejection, approval, execution and verification audit once available; do not claim pending steps occurred. |
| 6:00-7:00 | Customer, bridge, RCA, KB and permanent-change drafts and their review gates. |
| 7:00-8:00 | Demonstrate verification, remaining risks and questions. |

AI/tool error caught: the sanitiser masked the wrong part of CAP003's password
phrase and left the password later in the sentence. Review caught the residual
secret before the generated output was used for triage; caller names also
needed manual redaction. Avoid showing the original value in the presentation.
