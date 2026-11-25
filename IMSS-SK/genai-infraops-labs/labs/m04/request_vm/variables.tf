variable "size" {
  description = "Requested VM capacity tier. Allowed values are small, medium, or large."
  type        = string

  validation {
    condition     = contains(["small", "medium", "large"], var.size)
    error_message = "size must be one of: small, medium, large."
  }
}

variable "os" {
  description = "Operating system and version requested for the VM, for example Ubuntu 22.04."
  type        = string

  validation {
    condition     = length(trimspace(var.os)) > 0
    error_message = "os must not be empty."
  }
}

variable "owner" {
  description = "Team, assignment group, or named accountable owner of the VM."
  type        = string

  validation {
    condition     = length(trimspace(var.owner)) > 0
    error_message = "owner must not be empty."
  }
}
