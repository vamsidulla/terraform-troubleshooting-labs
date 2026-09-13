terraform {
  required_version = ">= 1.4.0, < 2.0.0"
}

locals {
  names = ["gateway", "api", "worker"]
}

resource "terraform_data" "node" {
  count = length(local.names)
  input = local.names[count.index]

  # Make an identity change require replacement in this local simulation.
  triggers_replace = [local.names[count.index]]
}
