# Capstone redaction review

Status: the user approved this copy for AI triage; reviewer identity was not
provided, so a named checklist sign-off is still outstanding.

The initial `tools/sanitise.py` pass masked the phone number and flagged CAP006
as suspected prompt injection. In CAP003, it masked the word following the
password label but missed the password later in the sentence. It also left
caller names untouched because the tool processes only the description column.

The copy in `tickets_sanitised.csv` additionally replaces caller identities with
consistent aliases, removes the entire password-bearing clause in CAP003, and
replaces the embedded instruction in CAP006 while preserving its flag. The
ticket IDs, operational symptoms and VIP marker remain for triage. The
sanitiser's initial output is not included because it is not safe to share.

Reviewer: name not provided. A named reviewer should check all fields for
residual sensitive data, confirm that aliases and redactions preserve enough
context, and sign this checklist before further sharing.
