# Validation results

Executed on 2026-09-13 using Terraform 1.14.7 on Linux x86_64. The verification driver used Python 3.12.14.

Command: `python3 scripts/verify.py` with Terraform on `PATH`.

```text
PASS: Terraform formatting checks
PASS: 01-input-validation: expected failure, valid apply, unchanged plan, and destroy
PASS: 02-resource-reference: expected failure, valid apply, unchanged plan, and destroy
PASS: 03-dependency-cycle: expected failure, valid apply, unchanged plan, and destroy
PASS: count insertion plans two replacements and one new instance; state unchanged
PASS: moved blocks preserve both IDs; only gateway is created; unchanged plan and destroy
```

| Check | Observed result |
|---|---|
| Invalid input | `validate` succeeded; `plan` rejected `deev` using the declared rule |
| Incorrect reference | `validate` rejected the undeclared resource address |
| Dependency cycle | `validate` reported the mutual dependency cycle |
| Fixed modules | Validation and apply succeeded; outputs matched the intended values |
| Repeated plans | `plan -detailed-exitcode` returned 0 after every valid apply |
| Inserting into a count-based list | The plan contained two replacements plus one new instance; it was not applied |
| Migration using moved blocks | Two address moves, one creation, zero deletions; both original IDs were preserved |
| Cleanup | Destroy succeeded and the local state contained no managed resources afterward |

All stateful runs used temporary directories and the built-in `terraform_data` resource. These checks do not validate cloud resources, remote backends, state locking, credentials, external providers, production migrations, or Terraform versions other than 1.14.7.
