terraform {
  required_version = ">= 1.4.0, < 2.0.0"
}

locals {
  names = toset(["gateway", "api", "worker"])
}

resource "terraform_data" "node" {
  for_each         = local.names
  input            = each.key
  triggers_replace = [each.key]
}

# Map the original baseline addresses to stable logical identities.
moved {
  from = terraform_data.node[0]
  to   = terraform_data.node["api"]
}

moved {
  from = terraform_data.node[1]
  to   = terraform_data.node["worker"]
}
