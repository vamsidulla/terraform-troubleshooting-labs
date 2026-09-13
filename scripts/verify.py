#!/usr/bin/env python3
"""Verify intentional errors, local applies, state migration, and cleanup."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "TF_IN_AUTOMATION": "1", "CHECKPOINT_DISABLE": "1"}


def tf(directory, *args, code=0):
    result = subprocess.run(
        ["terraform", f"-chdir={directory}", *args], env=ENV, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90,
    )
    if result.returncode != code:
        raise AssertionError(f"Expected {code}, got {result.returncode}: {args}\n{result.stdout}")
    return result.stdout


def resources(directory):
    state = json.loads(tf(directory, "show", "-json"))
    return {
        resource["address"]: resource["values"]
        for resource in state.get("values", {}).get("root_module", {}).get("resources", [])
    }


def plan(directory, filename):
    tf(directory, "plan", "-input=false", "-no-color", f"-out={filename}")
    return json.loads(tf(directory, "show", "-json", filename))


def destroy(directory):
    tf(directory, "destroy", "-input=false", "-auto-approve", "-no-color")
    assert not resources(directory), "Managed resources remain after destroy"


def main():
    if not shutil.which("terraform"):
        raise SystemExit("Install Terraform and put it on PATH as described in README.md.")
    tf(ROOT, "fmt", "-check", "-recursive")
    print("PASS: Terraform formatting checks")
    with tempfile.TemporaryDirectory(prefix="terraform-troubleshooting-") as temp:
        work = Path(temp)
        shutil.copytree(ROOT / "labs", work / "labs", ignore=shutil.ignore_patterns(
            ".terraform", "*.tfstate*", "*.tfplan", "*.tfplan.json"))

        for slug, diagnostic in [
            ("01-input-validation", "environment must be dev or int"),
            ("02-resource-reference", "Reference to undeclared resource"),
            ("03-dependency-cycle", "Cycle"),
        ]:
            broken = work / "labs" / slug / "broken"
            fixed = work / "labs" / slug / "fixed"
            tf(broken, "init", "-input=false", "-no-color")
            if slug == "01-input-validation":
                tf(broken, "validate", "-no-color")
                error = tf(broken, "plan", "-input=false", "-no-color", code=1)
            else:
                error = tf(broken, "validate", "-no-color", code=1)
            assert diagnostic in error, f"Wrong failure for {slug}:\n{error}"

            tf(fixed, "init", "-input=false", "-no-color")
            tf(fixed, "validate", "-no-color")
            plan(fixed, "fixed.tfplan")
            tf(fixed, "apply", "-input=false", "-no-color", "fixed.tfplan")
            state = resources(fixed)
            if slug != "03-dependency-cycle":
                assert json.loads(tf(fixed, "output", "-json", "environment")) == "dev"
                assert len(state) == 1
            else:
                result = json.loads(tf(fixed, "output", "-json", "application"))
                assert result["name"] == "developer-kit"
                assert result["network_id"] == state["terraform_data.network"]["id"]
                assert len(state) == 2
            tf(fixed, "plan", "-input=false", "-no-color", "-detailed-exitcode")
            destroy(fixed)
            print(f"PASS: {slug}: expected failure, valid apply, unchanged plan, and destroy")

        module = work / "migration"
        module.mkdir()
        source = work / "labs" / "04-count-to-foreach"
        shutil.copy2(source / "baseline/main.tf", module / "main.tf")
        tf(module, "init", "-input=false", "-no-color")
        plan(module, "baseline.tfplan")
        tf(module, "apply", "-input=false", "-no-color", "baseline.tfplan")
        original = resources(module)
        api_id = original['terraform_data.node[0]']["id"]
        worker_id = original['terraform_data.node[1]']["id"]

        shutil.copy2(source / "broken/main.tf", module / "main.tf")
        tf(module, "validate", "-no-color")
        broken_plan = plan(module, "broken.tfplan")
        changes = broken_plan["resource_changes"]
        replacements = [c for c in changes if "delete" in c["change"]["actions"]
                        and "create" in c["change"]["actions"]]
        creates = [c for c in changes if c["change"]["actions"] == ["create"]]
        assert len(replacements) == 2 and len(creates) == 1
        assert resources(module) == original, "Planning changed baseline state"
        print("PASS: count insertion plans two replacements and one new instance; state unchanged")

        shutil.copy2(source / "fixed/main.tf", module / "main.tf")
        tf(module, "validate", "-no-color")
        fixed_plan = plan(module, "fixed.tfplan")
        changes = fixed_plan["resource_changes"]
        assert all("delete" not in c["change"]["actions"] for c in changes)
        assert sum(c["change"]["actions"] == ["create"] for c in changes) == 1
        moves = {c["previous_address"]: c["address"] for c in changes if "previous_address" in c}
        assert moves == {
            'terraform_data.node[0]': 'terraform_data.node["api"]',
            'terraform_data.node[1]': 'terraform_data.node["worker"]',
        }
        tf(module, "apply", "-input=false", "-no-color", "fixed.tfplan")
        final = resources(module)
        assert final['terraform_data.node["api"]']["id"] == api_id
        assert final['terraform_data.node["worker"]']["id"] == worker_id
        assert final['terraform_data.node["gateway"]']["input"] == "gateway"
        tf(module, "plan", "-input=false", "-no-color", "-detailed-exitcode")
        destroy(module)
        print("PASS: moved blocks preserve both IDs; only gateway is created; unchanged plan and destroy")


if __name__ == "__main__":
    main()
