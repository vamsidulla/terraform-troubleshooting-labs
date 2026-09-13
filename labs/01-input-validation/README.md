# 01 · A plan rejects the environment input

Beginner · 15 minutes

## Scenario

The configuration has a valid default, but the plan fails with an environment validation error.

Run from the repository root with Terraform installed. Each `broken/` and `fixed/` directory is an independent root module. Keep these directories separate: Terraform combines all `.tf` files in one directory.

## Reproduce and investigate

```bash
terraform -chdir=labs/01-input-validation/broken init -input=false
terraform -chdir=labs/01-input-validation/broken validate
terraform -chdir=labs/01-input-validation/broken plan -input=false
```

Compare the successful validation with the failed plan using the real input values.

### Expected evidence

The plan exits with an invalid variable value error. `terraform.tfvars` supplies `deev`, which overrides the default `dev`. Configuration validation alone does not establish that the actual input values satisfy the contract.

Read the address and line number in the error, compare it with the configuration and input files, then explain a testable hypothesis.

<details>
<summary>Reveal the fix and verification</summary>

Correct the supplied value to `dev`; keep the validation rule. A guardrail rejecting invalid input is working correctly. Inspect input sources and precedence instead of weakening the rule.

```bash
terraform -chdir=labs/01-input-validation/fixed init -input=false
terraform -chdir=labs/01-input-validation/fixed validate
terraform -chdir=labs/01-input-validation/fixed plan -out=lab.tfplan
terraform -chdir=labs/01-input-validation/fixed apply lab.tfplan
terraform -chdir=labs/01-input-validation/fixed output environment
terraform -chdir=labs/01-input-validation/fixed plan -detailed-exitcode
```

Review the saved plan before applying it. The output should be "dev". The final plan must show no changes and return 0. With `-detailed-exitcode`, 1 means an error and 2 means a successful plan with changes.

</details>

## Interview check

The order form says “deev” while the catalog lists “dev.” Should the clerk change the catalog or correct the order? Map this to variable values and validation.

## Cleanup

```bash
terraform -chdir=labs/01-input-validation/fixed destroy
```

Review the destruction plan, then type `yes`. These examples create only local state entries. There is nothing to destroy in the broken variant if you stopped at the demonstrated error. Local state and plan files are ignored by Git. See [validation results](../../VALIDATION.md).
