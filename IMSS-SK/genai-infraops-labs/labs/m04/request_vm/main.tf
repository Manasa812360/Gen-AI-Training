terraform {
  required_version = ">= 1.5.0"
}

locals {
  vm_request = {
    size  = var.size
    os    = trimspace(var.os)
    owner = trimspace(var.owner)
  }
}
