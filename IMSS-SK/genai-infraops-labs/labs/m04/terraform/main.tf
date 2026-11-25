terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

resource "random_id" "network_suffix" {
  byte_length = 3
}

locals {
  model = {
    network = {
      name = "${var.network_name}-${random_id.network_suffix.hex}"
      cidr = var.network_cidr
    }
    vm = {
      name = var.vm_name
      size = var.vm_size
      os   = var.vm_os
    }
    security_group = {
      name = "${var.network_name}-https"
      ingress = [
        {
          description = "HTTPS from the private network"
          protocol    = "tcp"
          port        = 443
          source_cidr = "10.0.0.0/8"
        }
      ]
    }
  }
}

resource "local_file" "infrastructure_model" {
  filename = "${path.module}/${var.output_filename}"
  content  = jsonencode(local.model)
}
