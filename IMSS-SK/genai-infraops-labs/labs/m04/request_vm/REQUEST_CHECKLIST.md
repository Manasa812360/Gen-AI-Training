# Service Desk checklist: new VM request

Use this checklist for every standard VM service request. Do not treat a
successful Terraform validation as provisioning approval.

## 1. Identify and qualify the request

- [ ] Record the request number and requestor's contact details.
- [ ] Confirm the request is for a new standard VM, not an incident or a
      non-standard hosting exception.
- [ ] Record the purpose, target environment, required-by date and expected
      retirement date.
- [ ] Collect the requested size: `small`, `medium` or `large`.
- [ ] Collect the supported operating system and version.
- [ ] Record the accountable owner as a team, assignment group or named owner.
- [ ] Confirm the cost centre or budget code and the business service.
- [ ] Record whether backup, monitoring and patching are required; use the
      applicable platform defaults unless an approved exception exists.

## 2. Obtain approvals

- [ ] Obtain the requestor's manager or delegated service-owner approval.
- [ ] Obtain Cloud Ops approval after reviewing the capacity, cost and planned
      specification.
- [ ] Obtain InfraSec approval for any internet exposure, privileged access or
      security exception.
- [ ] Route non-standard sizes, unsupported operating systems or production
      access through the relevant change and exception process.
- [ ] Record each approver, decision and date on the request.

## 3. Validate the request module

Run from `labs/m04/request_vm`:

```bash
terraform init -backend=false
terraform fmt -check
terraform validate
terraform plan \
  -var='size=medium' \
  -var='os=Ubuntu 22.04' \
  -var='owner=APP-PORTAL-L2'
```

- [ ] Confirm the size is exactly `small`, `medium` or `large`.
- [ ] Confirm the OS is a supported version and is not blank.
- [ ] Confirm the owner is named, active and not blank.
- [ ] Review the plan output for unintended resources or changes.
- [ ] Save the validation and plan evidence with the request.

## 4. Fulfil and verify

- [ ] Confirm all required approvals before provisioning.
- [ ] Provision through the approved automation only; do not make console-only
      changes.
- [ ] Verify VM reachability, OS version, size, ownership tags, monitoring,
      patching and backup configuration.
- [ ] Confirm access follows least privilege and test it with the intended
      owner.
- [ ] Record the VM identifier, hostname/IP address and provisioning evidence.
- [ ] If access is not working, follow the incident process rather than bypassing
      approved controls.

Any firewall or SSH request is a separate change. Reject unrestricted
`0.0.0.0/0` SSH exposure and refer it to InfraSec for a restricted source CIDR,
VPN, bastion or another approved access path.

## 5. Hand over and close

- [ ] Send the access and VM details through an approved, access-controlled
      channel; never include passwords or private keys in the ticket.
- [ ] Provide the support route, patching expectations, backup status and
      retirement reminder.
- [ ] Ask the owner to confirm successful access and completion.
- [ ] Set the request outcome, attach evidence and close only after owner
      confirmation or the agreed follow-up is complete.

Suggested hand-over message:

> Your VM is ready. Details: [hostname/IP], [OS and version], [size],
> and accountable owner: [owner]. Monitoring, patching and backup status:
> [status]. Please confirm that you can access the VM through [approved access
> path]. For issues, contact [support group] and quote request [request number].
