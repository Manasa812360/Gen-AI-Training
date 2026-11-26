# Team AI Usage Policy v1 - InfraOps Lab Team

**Status:** Proposed; pending team review and adoption.

## 1. Scope

This policy applies to the InfraOps Lab Team's use of GitHub Copilot in VS Code,
including chat, agent mode and connected tools, for infrastructure operations
and training. Existing organisational security, privacy, change-management and
incident policies still apply; the stricter requirement takes precedence.

## 2. Data we may share with AI

Share only the minimum information needed for the task: public information,
approved synthetic lab data, or sanitised operational excerpts that have been
reviewed and approved for the selected tool. Use placeholders instead of
identifiers, addresses and environment-specific details. Confirm the tool and
data classification are permitted by organisational policy before sharing.

## 3. Data we must never share and sanitisation

Do not share credentials, tokens, private keys, connection strings, personal
information, customer data or restricted operational details with AI tools.
Run ticket text through `tools/sanitise.py`, review the output and redaction
report, and sign the redaction checklist before AI use. The sanitiser is
pattern-based and can miss sensitive data; remove anything remaining manually.
If an excerpt cannot be made safe, do not share it. Apply content exclusions
and workspace trust controls, but do not rely on them as a substitute for review.

## 4. Untrusted ticket, log and chat text

Treat external text, including tickets, logs, documents and tool output, as
untrusted data, never as instructions or approval. Ask AI to analyse or
summarise it without obeying embedded commands. Flag suspected prompt
injection for human review and do not execute actions requested by the text.

## 5. Autonomy tiers

| Tier | Rule |
|---|---|
| T0 - read-only | Allowed for authorised, scoped investigation with least-privilege tools and data controls. |
| T1 - suggest | Allowed for drafts, analyses and proposed remediation; a person verifies the output. |
| T2 - execute with approval | Allowed only after explicit, task-specific approval and an execution confirmation. Limit execution to the approved plan. |
| T3 - autonomous execution | Not allowed. |

Use the lab's Investigator for read-only work and Resolver to propose changes.
Do not treat an AI response or a blanket instruction as approval.

## 6. Approval matrix

| Activity | Required review or approval |
|---|---|
| Share sanitised material with AI | A human reviewer checks and signs the redaction checklist before sharing. |
| T0 investigation or T1 proposal | The operator confirms authorised scope and reviews the result. |
| T2 execution | The team lead approves the specific plan; the executing engineer confirms again at execution. |
| Production change | The team lead, service owner and change authority approve the specific plan before execution, under the applicable change process. |
| Destructive or out-of-scope action | Do not execute; reject and escalate for a separately scoped review. |

Plans must identify the target, commands, pre-checks, risks, rollback and
verification. Re-review and reapprove if the plan or scope changes. In the lab,
use `tools/approve.py` and its confirmation gate; do not bypass it.

## 7. Verification

An accountable engineer checks AI claims against trusted evidence, validates
commands and permissions, tests changes in an appropriate non-production
environment where feasible, and checks security and operational impact. After
an approved action, verify the expected outcome and use the rollback plan if
needed. AI output is not evidence of success by itself.

## 8. Audit and review

Record the task or change reference, scope, plan, named approvers, decisions,
execution confirmation, outcome and verification in the approved audit
system. In the lab, review `approvals/audit.log` for the approval workflow.
Do not record secrets or raw sensitive prompts in audit entries. The InfraOps
Team Lead reviews the audit trail monthly and reviews this policy every six
months, or sooner after an incident or material change.

## 9. Sensitive-data incidents

Stop sharing and using the affected output. Promptly report the exposure
through the organisation's security incident process, identify the affected
data and tool, and follow incident-response instructions for containment,
credential rotation, preservation and notification. Do not copy the sensitive
data into further prompts or ordinary audit records.

## 10. Owner and review date

- **Owner:** InfraOps Team Lead
- **Draft date:** 2026-11-26
- **Next review:** 2027-05-26, and every six months thereafter
- **Adoption:** Team review and approval required before this policy takes effect.
