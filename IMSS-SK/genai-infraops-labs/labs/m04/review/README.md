# Infrastructure security review

This directory contains a remediated version of the intentionally insecure
Terraform example from Lab 4.2.

## Security controls

The configuration now:

- Uses the standard AWS credential provider chain instead of embedded credentials.
- Allows HTTPS from `10.0.0.0/8` only and removes public SSH access.
- Requires IMDSv2 and limits metadata response hops to one.
- Encrypts the EC2 root volume with KMS and enables EBS optimization and detailed
  monitoring.
- Attaches a dedicated EC2 instance profile without broad AWS permissions.
- Blocks all forms of public S3 access.
- Encrypts report, replica, and access-log buckets with rotating KMS keys.
- Enables S3 versioning, lifecycle cleanup, access logging, EventBridge
  notifications, and cross-region replication.
- Limits the replication role and policy to the required buckets, KMS keys,
  objects, and replication actions.
- Adds descriptions for security-group rules.
- Aborts incomplete multipart uploads after seven days.

## Least-privilege notes

The EC2 role starts with no application permissions. Add only the exact actions
and resource ARNs required if the workload later needs AWS API access.

The replication role can read replication metadata and versions from the source
buckets and write replicas to the destination buckets. Its KMS permissions are
restricted to decrypting source objects and encrypting destination objects.

## Validation

Run from the repository's `genai-infraops-labs` directory:

```bash
terraform fmt -check labs/m04/review/insecure.tf
terraform -chdir=labs/m04/review validate
checkov -d labs/m04/review --compact
```

The reviewed configuration is expected to report **100 passed checks, 0 failed,
and 0 skipped**.

## Safety

This example models secure infrastructure and is not intended to be applied.
Before using it outside the lab, replace the example AMI, bucket names, regions,
network design, and retention requirements with approved environment values and
review the IAM and KMS policies with the infrastructure owner.
