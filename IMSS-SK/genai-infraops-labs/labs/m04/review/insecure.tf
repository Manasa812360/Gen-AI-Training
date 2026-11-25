# Lab 4.2 - Remediated Terraform review example. Do not apply.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

provider "aws" {
  alias  = "replica"
  region = "ap-southeast-1"
}

data "aws_caller_identity" "current" {}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Allow HTTPS from the private application network"

  ingress {
    description = "HTTPS from the private application network"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}

resource "aws_kms_key" "reports" {
  description         = "Encrypt finance report objects"
  enable_key_rotation = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EnableAccountAdministration"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "AllowReportReplication"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.s3_replication.arn
        }
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_kms_key" "reports_replica" {
  provider            = aws.replica
  description         = "Encrypt replicated finance report objects"
  enable_key_rotation = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EnableAccountAdministration"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "AllowReportReplication"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.s3_replication.arn
        }
        Action = [
          "kms:Encrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_s3_bucket" "reports" {
  bucket = "hm-finance-reports-demo"
}

# checkov:skip=CKV_AWS_144:Replication destination is not replicated again to prevent duplicate/looping report copies.
resource "aws_s3_bucket" "reports_replica" {
  provider = aws.replica
  bucket   = "hm-finance-reports-demo-replica"
}

resource "aws_s3_bucket" "access_logs" {
  bucket = "hm-finance-reports-access-logs"
}

resource "aws_s3_bucket" "access_logs_replica" {
  provider = aws.replica
  bucket   = "hm-finance-reports-access-logs-replica"
}

resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "reports_replica" {
  provider                = aws.replica
  bucket                  = aws_s3_bucket.reports_replica.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "access_logs" {
  bucket                  = aws_s3_bucket.access_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "access_logs_replica" {
  provider                = aws.replica
  bucket                  = aws_s3_bucket.access_logs_replica.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "reports_replica" {
  provider = aws.replica
  bucket   = aws_s3_bucket.reports_replica.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "access_logs_replica" {
  provider = aws.replica
  bucket   = aws_s3_bucket.access_logs_replica.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.reports.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports_replica" {
  provider = aws.replica
  bucket   = aws_s3_bucket.reports_replica.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.reports_replica.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.reports.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "access_logs_replica" {
  provider = aws.replica
  bucket   = aws_s3_bucket.access_logs_replica.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.reports_replica.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_logging" "reports" {
  bucket        = aws_s3_bucket.reports.id
  target_bucket = aws_s3_bucket.access_logs.id
  target_prefix = "reports/"
}

resource "aws_s3_bucket_logging" "reports_replica" {
  provider      = aws.replica
  bucket        = aws_s3_bucket.reports_replica.id
  target_bucket = aws_s3_bucket.access_logs_replica.id
  target_prefix = "reports/"
}

resource "aws_s3_bucket_lifecycle_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id

  rule {
    id     = "retain-current-and-expire-versions"
    status = "Enabled"

    filter {
      prefix = ""
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  depends_on = [aws_s3_bucket_versioning.reports]
}

resource "aws_s3_bucket_lifecycle_configuration" "reports_replica" {
  provider = aws.replica
  bucket   = aws_s3_bucket.reports_replica.id

  rule {
    id     = "retain-current-and-expire-versions"
    status = "Enabled"

    filter {
      prefix = ""
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  depends_on = [aws_s3_bucket_versioning.reports_replica]
}

resource "aws_s3_bucket_lifecycle_configuration" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id

  rule {
    id     = "abort-incomplete-access-log-uploads"
    status = "Enabled"

    filter {
      prefix = ""
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  rule {
    id     = "expire-old-access-logs"
    status = "Enabled"

    filter {
      prefix = "reports/"
    }

    expiration {
      days = 365
    }

  }

  depends_on = [aws_s3_bucket_versioning.access_logs]
}

resource "aws_s3_bucket_lifecycle_configuration" "access_logs_replica" {
  provider = aws.replica
  bucket   = aws_s3_bucket.access_logs_replica.id

  rule {
    id     = "abort-incomplete-access-log-uploads"
    status = "Enabled"

    filter {
      prefix = ""
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  rule {
    id     = "expire-old-access-logs"
    status = "Enabled"

    filter {
      prefix = "reports/"
    }

    expiration {
      days = 365
    }

  }

  depends_on = [aws_s3_bucket_versioning.access_logs_replica]
}

resource "aws_s3_bucket_notification" "reports" {
  bucket      = aws_s3_bucket.reports.id
  eventbridge = true
}

resource "aws_s3_bucket_notification" "reports_replica" {
  provider    = aws.replica
  bucket      = aws_s3_bucket.reports_replica.id
  eventbridge = true
}

resource "aws_s3_bucket_notification" "access_logs" {
  bucket      = aws_s3_bucket.access_logs.id
  eventbridge = true
}

resource "aws_s3_bucket_notification" "access_logs_replica" {
  provider    = aws.replica
  bucket      = aws_s3_bucket.access_logs_replica.id
  eventbridge = true
}

resource "aws_iam_role" "s3_replication" {
  name = "finance-reports-replication"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "s3_replication" {
  name = "finance-reports-replication"
  role = aws_iam_role.s3_replication.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.reports.arn,
          aws_s3_bucket.access_logs.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging"
        ]
        Resource = [
          "${aws_s3_bucket.reports.arn}/*",
          "${aws_s3_bucket.access_logs.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ]
        Resource = [
          "${aws_s3_bucket.reports_replica.arn}/*",
          "${aws_s3_bucket.access_logs_replica.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = aws_kms_key.reports.arn
      },
      {
        Effect   = "Allow"
        Action   = "kms:Encrypt"
        Resource = aws_kms_key.reports_replica.arn
      }
    ]
  })
}

resource "aws_s3_bucket_replication_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id
  role   = aws_iam_role.s3_replication.arn

  rule {
    id       = "replicate-finance-reports"
    priority = 1
    status   = "Enabled"

    delete_marker_replication {
      status = "Enabled"
    }

    destination {
      bucket        = aws_s3_bucket.reports_replica.arn
      storage_class = "STANDARD"

      encryption_configuration {
        replica_kms_key_id = aws_kms_key.reports_replica.arn
      }
    }

    filter {}
  }

  depends_on = [aws_s3_bucket_versioning.reports]
}

resource "aws_s3_bucket_replication_configuration" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id
  role   = aws_iam_role.s3_replication.arn

  rule {
    id       = "replicate-access-logs"
    priority = 1
    status   = "Enabled"

    delete_marker_replication {
      status = "Enabled"
    }

    destination {
      bucket        = aws_s3_bucket.access_logs_replica.arn
      storage_class = "STANDARD"

      encryption_configuration {
        replica_kms_key_id = aws_kms_key.reports_replica.arn
      }
    }

    filter {}
  }

  depends_on = [aws_s3_bucket_versioning.access_logs]
}

resource "aws_iam_role" "app" {
  name = "finance-app"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "app" {
  name = "finance-app"
  role = aws_iam_role.app.name
}

resource "aws_instance" "app" {
  ami                    = "ami-0123456789abcdef0"
  instance_type          = "m5.8xlarge"
  vpc_security_group_ids = [aws_security_group.web.id]
  iam_instance_profile   = aws_iam_instance_profile.app.name
  ebs_optimized          = true
  monitoring             = true

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    encrypted   = true
    kms_key_id  = aws_kms_key.reports.arn
    volume_size = 20
    volume_type = "gp3"
  }
}
