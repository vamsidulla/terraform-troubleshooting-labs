# 03 · Two resources wait for each other

Intermediate · 20 minutes

## Scenario

The configuration models a network and an application. Each object needs the other object's output before it can be created. Both are local terraform_data objects; no real infrastructure is involved.

Run from the repository root with Terraform installed. Each `broken/` and `fixed/` directory is an independent root module. Keep these directories separate: Terraform combines all `.tf` files in one directory.

## Reproduce and investigate

```bash
terraform -chdir=labs/03-dependency-cycle/broken init -input=false
terraform -chdir=labs/03-dependency-cycle/broken validate
```



### Expected evidence

Terraform reports a cycle involving the two resource addresses. There is no valid creation order.

Read the address and line number in the error, compare it with the configuration and input files, then explain a testable hypothesis.

<details>
<summary>Reveal the fix and verification</summary>

Give the network an independent input, then reference its ID from the application. That expression creates the dependency in the correct direction. Adding `depends_on`, moving blocks up the file, or adding sleeps does not remove a logical cycle. Rework the input/output contract so a starting point exists.

```bash
terraform -chdir=labs/03-dependency-cycle/fixed init -input=false
terraform -chdir=labs/03-dependency-cycle/fixed validate
terraform -chdir=labs/03-dependency-cycle/fixed plan -out=lab.tfplan
terraform -chdir=labs/03-dependency-cycle/fixed apply lab.tfplan
terraform -chdir=labs/03-dependency-cycle/fixed output application
terraform -chdir=labs/03-dependency-cycle/fixed plan -detailed-exitcode
```

Review the saved plan before applying it. The output should be an object containing name = "developer-kit" and a nonempty network_id. The final plan must show no changes and return 0. With `-detailed-exitcode`, 1 means an error and 2 means a successful plan with changes.

</details>

## Interview check

Two people agree that each will unlock a door only after the other unlocks theirs. What must change to let the process start?

## Cleanup

```bash
terraform -chdir=labs/03-dependency-cycle/fixed destroy
```

Review the destruction plan, then type `yes`. These examples create only local state entries. There is nothing to destroy in the broken variant if you stopped at the demonstrated error. Local state and plan files are ignored by Git. See [validation results](../../VALIDATION.md).
