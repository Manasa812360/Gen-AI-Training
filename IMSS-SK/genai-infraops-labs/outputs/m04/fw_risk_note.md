# InfraSec risk note: vendor SSH access

**Recommendation: Reject as submitted.** The proposal exposes TCP port 22 on
the portal application security group to every IPv4 address on the internet.
It may be approved only after the source is restricted and the compensating
controls below are evidenced.

## Risks

- Internet-wide SSH exposure creates direct opportunities for credential
  attacks, vulnerability exploitation and unauthorised administrative access.
- The rule gives no assurance that traffic comes from the named vendor or an
  approved support location.
- A compromise could affect the portal service and data accessible from that
  server.
- The request does not define an expiry, access path, logging requirements or
  a tested backout procedure.

## Failed controls

- Least privilege and restricted source addressing
- Internet-exposure approval and InfraSec sign-off
- Time-bounded vendor access with named source ownership
- Explicit authentication, monitoring, audit and backout requirements

## Safer alternative

Permit SSH only from the vendor's verified static egress IP or, preferably,
from an approved corporate VPN/bastion. For example:

```hcl
cidr_blocks = ["203.0.113.10/32"] # Replace with the verified vendor egress IP.
```

Use key-based access, least-privilege accounts, session logging, multi-factor
authentication where supported, and automatic rule expiry. Prefer a bastion or
managed access service over direct SSH to the application server. Record the
owner, approved window and backout, then validate access from the allowed and
denied sources.

Any revised internet-exposed rule remains subject to mandatory InfraSec
approval.
