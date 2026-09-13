terraform {
  required_version = ">= 1.4.0, < 2.0.0"
}

# These are local state objects, not real network or application resources.
resource "terraform_data" "network" {
  input = terraform_data.application.output
}

resource "terraform_data" "application" {
  input = terraform_data.network.output
}
