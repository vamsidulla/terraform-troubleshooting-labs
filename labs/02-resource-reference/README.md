# 02 · An output references an undeclared resource

Beginner · 15 minutes

## Scenario

A small configuration cannot validate because an output references a resource Terraform cannot find.

Run from the repository root with Terraform installed. Each `broken/` and `fixed/` directory is an independent root module. Keep these directories separate: Terraform combines all `.tf` files in one directory.

## Reproduce and investigate

```bash
terraform -chdir=labs/02-resource-reference/broken init -input=false
terraform -chdir=labs/02-resource-reference/broken validate
```



### Expected evidence

Validation reports a reference to an undeclared resource. The declared label is `environment`, but the output references `environmnt`. Formatting alone cannot prove a reference resolves.

Read the address and line number in the error, compare it with the configuration and input files, then explain a testable hypothesis.

<details>
<summary>Reveal the fix and verification</summary>

Correct the reference to the declared address. A resource address includes its type and label. Editing a reference is different from renaming a managed resource block; a rename may require an explicit state move, as demonstrated in Lab 04.

```bash
terraform -chdir=labs/02-resource-reference/fixed init -input=false
terraform -chdir=labs/02-resource-reference/fixed validate
terraform -chdir=labs/02-resource-reference/fixed plan -out=lab.tfplan
terraform -chdir=labs/02-resource-reference/fixed apply lab.tfplan
terraform -chdir=labs/02-resource-reference/fixed output environment
terraform -chdir=labs/02-resource-reference/fixed plan -detailed-exitcode
```

Review the saved plan before applying it. The output should be "dev". The final plan must show no changes and return 0. With `-detailed-exitcode`, 1 means an error and 2 means a successful plan with changes.

</details>

## Interview check

A directory has an entry for “environment,” but your lookup asks for “environmnt.” Why would retrying the request not help?

## Cleanup

```bash
terraform -chdir=labs/02-resource-reference/fixed destroy
```

Review the destruction plan, then type `yes`. These examples create only local state entries. There is nothing to destroy in the broken variant if you stopped at the demonstrated error. Local state and plan files are ignored by Git. See [validation results](../../VALIDATION.md).
