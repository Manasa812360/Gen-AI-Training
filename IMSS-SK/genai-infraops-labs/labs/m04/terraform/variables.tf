variable "network_name" {
  description = "Base name of the modeled network."
  type        = string
  default     = "training"
}

variable "network_cidr" {
  description = "CIDR block assigned to the modeled network."
  type        = string
  default     = "10.10.0.0/16"

  validation {
    condition     = can(cidrhost(var.network_cidr, 0))
    error_message = "network_cidr must be a valid IPv4 or IPv6 CIDR block."
  }
}

variable "vm_name" {
  description = "Name of the modeled virtual machine."
  type        = string
  default     = "web-01"
}

variable "vm_size" {
  description = "Compute size of the modeled virtual machine."
  type        = string
  default     = "small"
}

variable "vm_os" {
  description = "Operating system installed on the modeled virtual machine."
  type        = string
  default     = "Ubuntu 24.04 LTS"
}

variable "output_filename" {
  description = "Name of the generated infrastructure model JSON file."
  type        = string
  default     = "infrastructure-model.json"

  validation {
    condition     = !can(regex("/", var.output_filename)) && endswith(var.output_filename, ".json")
    error_message = "output_filename must be a JSON filename without path separators."
  }
}
