terraform {
  required_version = ">= 1.4.0, < 2.0.0"
}

variable "environment" {
  description = "The non-production environment for this exercise."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "int"], var.environment)
    error_message = "environment must be dev or int."
  }
}

resource "terraform_data" "environment" {
  input = var.environment
}

output "environment" {
  value = terraform_data.environment.output
}
