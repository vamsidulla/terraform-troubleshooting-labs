# 04 · Inserting a list item would replace existing objects

Intermediate · 35 minutes

## Scenario

Two components, `api` and `worker`, already exist in Terraform state. Adding `gateway` to the front of a count-based list changes the meaning of existing numeric indexes.

This lab deliberately uses `terraform_data.triggers_replace` so changing an instance's assigned name forces a replacement. It models an identity-sensitive attribute. Real provider schemas decide whether an actual attribute change is an update or replacement.

**Use one working directory and preserve its state across all three stages.** The `baseline`, `broken`, and `fixed` folders are source snapshots, not three separate deployments. Do not apply the broken plan: the provided moves assume the original baseline state.

## 1. Establish the baseline

Run from the repository root. On the first attempt `.lab-work/04-count-to-foreach` must be unused. If you already ran the lab, follow cleanup before repeating.

```bash
mkdir -p .lab-work/04-count-to-foreach
cp labs/04-count-to-foreach/baseline/main.tf .lab-work/04-count-to-foreach/main.tf
terraform -chdir=.lab-work/04-count-to-foreach init -input=false
terraform -chdir=.lab-work/04-count-to-foreach plan -out=baseline.tfplan
terraform -chdir=.lab-work/04-count-to-foreach apply baseline.tfplan
terraform -chdir=.lab-work/04-count-to-foreach state list
terraform -chdir=.lab-work/04-count-to-foreach state show 'terraform_data.node[0]'
terraform -chdir=.lab-work/04-count-to-foreach state show 'terraform_data.node[1]'
```

Record the two IDs and names. Index 0 is `api`; index 1 is `worker`.

## 2. Inspect the broken change without applying it

```bash
cp labs/04-count-to-foreach/broken/main.tf .lab-work/04-count-to-foreach/main.tf
terraform -chdir=.lab-work/04-count-to-foreach plan -out=broken.tfplan
```

Expect **two replacements and one additional instance**: Terraform reports 3 to add and 2 to destroy because each replacement has both a create and a delete. Index 0 now means `gateway`, index 1 means `api`, and index 2 means `worker`.

Explain why `terraform validate` can succeed even though this plan is undesirable. How could a reviewer detect the impact before apply?

<details>
<summary>Reveal the migration and verification</summary>

## 3. Use stable keys and explicitly move the original state addresses

The fixed configuration uses `for_each` with component names. Two `moved` blocks map the original indexes to `api` and `worker`. It does not discard state or import new copies of those objects.

```bash
cp labs/04-count-to-foreach/fixed/main.tf .lab-work/04-count-to-foreach/main.tf
terraform -chdir=.lab-work/04-count-to-foreach validate
terraform -chdir=.lab-work/04-count-to-foreach plan -out=fixed.tfplan
terraform -chdir=.lab-work/04-count-to-foreach apply fixed.tfplan
terraform -chdir=.lab-work/04-count-to-foreach state list
terraform -chdir=.lab-work/04-count-to-foreach state show 'terraform_data.node["api"]'
terraform -chdir=.lab-work/04-count-to-foreach state show 'terraform_data.node["worker"]'
terraform -chdir=.lab-work/04-count-to-foreach plan -detailed-exitcode
```

Review before apply: the fixed plan should show the two address moves, **one creation (`gateway`), and no replacements or deletions**. The `api` and `worker` IDs must match the IDs recorded before migration. The final plan must return 0 with no changes.

Keys must themselves remain stable: renaming a `for_each` key changes an address. Retain moved blocks while consumers may still upgrade from the old addresses. For real infrastructure, inspect the actual state and back it up before planning a migration; never assume index-to-name mappings from this example apply elsewhere.

</details>

## Interview check

A hotel identifies reservations by row number. Inserting a new row reassigns everyone's number. Why is a stable reservation ID a better identity? Why must the old row-to-ID mapping be preserved during migration?

## Cleanup and repeat

```bash
terraform -chdir=.lab-work/04-count-to-foreach destroy
```

Review and confirm with `yes`. The same destroy command works if you stop after baseline or the broken plan; the objects exist only in local state. After successful destruction, you can repeat from step 1 in the now-empty state. Do not delete state as a troubleshooting shortcut.

See [validation results](../../VALIDATION.md) for the tested plan counts and identity checks.
