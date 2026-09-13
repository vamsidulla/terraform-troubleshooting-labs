terraform {
  required_version = ">= 1.4.0, < 2.0.0"
}

resource "terraform_data" "environment" {
  input = "dev"
}

output "environment" {
  value = terraform_data.environmnt.output
}
