terraform {
  required_version = ">= 1.4.0, < 2.0.0"
}

# An independent input starts the dependency chain.
resource "terraform_data" "network" {
  input = "development-network"
}

resource "terraform_data" "application" {
  input = {
    name       = "developer-kit"
    network_id = terraform_data.network.id
  }
}

output "application" {
  value = terraform_data.application.output
}
