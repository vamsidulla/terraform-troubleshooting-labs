# Terraform Troubleshooting Labs

Learn to diagnose failed plans and recognize a dangerous successful plan before applying it.

**Four local labs · Beginner → Intermediate · No cloud credentials · Built-in provider only**

These are personal Terraform learning exercises. They use the built-in `terraform_data` resource to practice validation, dependency graphs, plans, state, and identity. No cloud infrastructure, provisioners, or external providers are used. The examples make no claim about production Terraform experience.

## Learning sequence

| Order | Lab | What you learn |
|---|---|---|
| 1 | [Invalid environment input](labs/01-input-validation/) | Input sources, variable validation, validate vs. plan |
| 2 | [Undeclared resource reference](labs/02-resource-reference/) | Resource addresses and diagnostic evidence |
| 3 | [Dependency cycle](labs/03-dependency-cycle/) | Graph reasoning and independent inputs |
| 4 | [count → for_each migration](labs/04-count-to-foreach/) | Plan review, stable identity, moved blocks, preserving state |

Work in order: reproduce → read the evidence → explain → fix → inspect the plan → apply → verify → destroy. Each guide includes an analogy-based interview question.

## Prerequisites

- [Terraform CLI](https://developer.hashicorp.com/terraform/install), version 1.4 or later and below 2.0. Runtime verification used 1.14.7; other versions have not been tested here.
- Linux, macOS, or WSL with a Bash-compatible terminal for the documented commands.
- Python 3.10+ only if you want to run the automated verification script.

Check the tool and open the first lab:

```bash
terraform version
terraform -chdir=labs/01-input-validation/broken init -input=false
terraform -chdir=labs/01-input-validation/broken plan -input=false
```

Run commands from this repository's root. Terraform loads every `.tf` file in a directory together: keep the broken and fixed modules separate. Lab 04 explicitly copies its stages into one working directory to preserve state.

## Repeatable verification

```bash
python3 scripts/verify.py
```

This uses temporary copies, checks the deliberate failures, applies only valid local configurations, verifies no-change plans, and tests that the migration preserves the original IDs. It also runs destroy. See [VALIDATION.md](VALIDATION.md) for the actual result and limitations.

## State and cleanup

Follow each lab's destroy instructions. State and saved plans remain local and are ignored by Git. The included `terraform.tfvars` files contain only demonstration environment labels; keep real secrets out of committed inputs. The exercise does not test remote state, locking, cloud permissions, provider APIs, or live infrastructure drift.

## References

- [terraform_data resource](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
- [Input validation](https://developer.hashicorp.com/terraform/language/validate)
- [Dependency graph](https://developer.hashicorp.com/terraform/internals/graph)
- [for_each](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
- [Refactoring with moved blocks](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)

Previous topics: [Ansible Troubleshooting Labs](https://github.com/vamsidulla/ansible-troubleshooting-labs) and [Kubernetes Troubleshooting Labs](https://github.com/vamsidulla/kubernetes-troubleshooting-labs).

Created for [Vamsi Krishna's personal learning portfolio](https://github.com/vamsidulla).
