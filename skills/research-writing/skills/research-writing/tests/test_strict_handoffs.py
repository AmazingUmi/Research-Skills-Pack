"""Exercise strict handoffs with the copy helper, resume CLI and shipped passports."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))
from scripts.check_experiment_provenance import validate_provenance
from scripts.check_re_review_synthesis import ManifestError, compute_apply_chain_witness
from scripts.repro_lock_validation import validate_block


def run(script, *args):
    return subprocess.run([sys.executable, str(ENGINE / "scripts" / script), *map(str, args)],
                          cwd=ROOT, capture_output=True, text=True)


class StrictHandoffs(unittest.TestCase):
    def test_anchor_working_copy_reaches_rereview_hash_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = Path(tmp, "source.md")
            working = Path(tmp, "working.md")
            initial = b"# Results\r\n\r\nTwo samples.\r\n"
            original.write_bytes(initial)
            result = run("ars_anchorize_draft.py", original, "--output", working)
            self.assertEqual(result.returncode, 0, result.stderr)
            block = json.loads(Path(str(working) + ".block-manifest.json").read_text())
            self.assertEqual(original.read_bytes(), initial)
            self.assertEqual(block["original_sha256"], hashlib.sha256(initial).hexdigest())
            self.assertEqual(block["working_sha256"], hashlib.sha256(working.read_bytes()).hexdigest())
            self.assertNotEqual(block["original_sha256"], block["working_sha256"])
            patch_digest = "a" * 64
            revised_digest = "b" * 64
            manifest = {"artifacts": {"revision_patches": {"items": [{"sha256": patch_digest}]},
                                      "original_manuscript": {"present": True, "sha256": block["working_sha256"]},
                                      "revised_manuscript": {"sha256": revised_digest}}}
            report = {"report_format_version": "1.3", "base_draft_hash": block["base_draft_hash"],
                      "output_draft_hash": revised_digest[:12], "patch_digest": patch_digest,
                      "authorization_witness": {"status": "pass", "unregistered_claim_drift_review_required": True}}
            self.assertEqual(compute_apply_chain_witness(manifest, [report])[0], "pass")
            manifest["artifacts"]["original_manuscript"]["sha256"] = block["original_sha256"]
            with self.assertRaises(ManifestError):
                compute_apply_chain_witness(manifest, [report])
            retry = Path(tmp, "retry.md")
            failed = run("ars_anchorize_draft.py", original, "--output", retry,
                         "--manifest-out", Path(tmp, "absent", "manifest.json"))
            self.assertNotEqual(failed.returncode, 0)
            self.assertFalse(retry.exists())
            self.assertEqual(run("ars_anchorize_draft.py", original, "--output", retry).returncode, 0)
            self.assertEqual(original.read_bytes(), initial)

    def test_resume_examples_and_old_branch_label(self):
        doc = (ENGINE / "handoff_schemas.md").read_text()
        example = "reset_boundary:" + doc.split("\nreset_boundary:", 1)[1].split("\n```", 1)[0]
        passport = yaml.safe_load(example)
        old = passport["reset_boundary"][1]
        old["pending_decision"]["options"][0]["next_mode"] = "revision"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "passport.yaml")
            def attempt(boundary, *args):
                raw = yaml.safe_dump(passport).encode("utf-8")
                path.write_bytes(raw)
                result = run("check_resume_target.py", path, boundary["hash"], *args)
                self.assertEqual(path.read_bytes(), raw)
                return result
            first = passport["reset_boundary"][0]
            self.assertNotEqual(attempt(first).returncode, 0)  # already consumed in the example
            passport["reset_boundary"].pop()
            self.assertNotEqual(attempt(first, "--stage", "3").returncode, 0)
            self.assertEqual(json.loads(attempt(first).stdout)["next_stage"], "2.5")
            first["next"] = "3"  # persisted illegal edge must also fail
            self.assertNotEqual(attempt(first).returncode, 0)
            self.assertNotEqual(attempt(old, "--stage", "4").returncode, 0)
            self.assertNotEqual(attempt(old, "--choice", "revise", "--stage", "2").returncode, 0)
            self.assertEqual(json.loads(attempt(old, "--choice", "revise").stdout),
                             {"next_stage": "4", "next_mode": "revise"})
            self.assertIsNone(json.loads(attempt(old, "--choice", "abort").stdout)["next_stage"])

    def test_resume_keeps_the_recorded_route_and_terminal_decisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            passport = Path(tmp, "passport.yaml")
            boundary = {"kind": "boundary", "hash": "12ab12ab12ab", "stage": "3", "next": "4"}

            def attempt(*args):
                raw = yaml.safe_dump({"reset_boundary": [boundary]}).encode()
                passport.write_bytes(raw)
                result = run("check_resume_target.py", passport, boundary["hash"], *args)
                self.assertEqual(passport.read_bytes(), raw)
                return result

            self.assertEqual(json.loads(attempt("--stage", "revise").stdout)["next_stage"], "4")
            self.assertEqual(json.loads(attempt("--stage", "review").stdout)["next_stage"], "3")
            self.assertNotEqual(attempt("--stage", "4.5").returncode, 0)
            boundary["next"] = "6"
            self.assertNotEqual(attempt("--stage", "3").returncode, 0)
            boundary.update(stage="5", next=None)
            self.assertIsNone(json.loads(attempt().stdout)["next_stage"])
            for args in (("--stage", "5"), ("--stage", "6"), ("--mode", "full")):
                self.assertNotEqual(attempt(*args).returncode, 0)

            boundary.update(stage="3", next="4", pending_decision={"options": [
                {"value": "revise", "next_stage": "4", "next_mode": "revise"},
                {"value": "abort", "next_stage": None}]})
            self.assertNotEqual(attempt("--choice", "revise", "--stage", "3").returncode, 0)
            self.assertNotEqual(attempt("--choice", "abort", "--stage", "4").returncode, 0)
            self.assertIsNone(json.loads(attempt("--choice", "abort").stdout)["next_stage"])

    def test_legacy_and_pack_experiment_provenance(self):
        passport = yaml.safe_load((ENGINE / "examples/passport_with_experiment_provenance.yaml").read_text())
        self.assertEqual(validate_provenance(passport["experiment_provenance"]), [])
        entry = passport["experiment_provenance"][0]
        entry["execution"] = {"origin": "pack_run", "executor": "outline experiment run",
                              "results": "results.json", "verification_status": "UNVERIFIED"}
        self.assertTrue(validate_provenance([entry]))
        entry["execution"]["command"] = "python measure.py"
        self.assertEqual(validate_provenance([entry]), [])
        entry["execution"]["confirmed_by"] = "scholar"
        self.assertEqual(validate_provenance([entry]), [])
        entry["execution"]["confirmed_by"] = "agent"
        self.assertTrue(validate_provenance([entry]))
        guide = (ROOT / "references/artifact_reproducibility_pattern.md").read_text()
        lock = yaml.safe_load(guide.split("```yaml\n", 1)[1].split("\n```", 1)[0])["repro_lock"]
        self.assertEqual(validate_block(lock), [])
        self.assertEqual(run("repro_lock_validation.py", ENGINE / "examples/passport_with_repro_lock.yaml").returncode, 0)
        del lock["cross_model"]["enabled"]
        self.assertTrue(validate_block(lock))

    def test_stage_snapshot_and_dashboard_cover_the_active_role_table(self):
        orchestrate = ROOT / "roles/orchestrate"
        role = (orchestrate / "ROLE.md").read_text()
        current_stages = [stage.replace("′", "p") for stage in
                          re.findall(r"^\| ([1-6](?:′|\.5)?) [^|]+\|", role, re.M)]
        status_doc = (orchestrate / "agents/state_tracker_agent.md").read_text()
        sample = json.loads(status_doc.split("## Tracked State Structure", 1)[1]
                            .split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(list(sample["stages"]), current_stages)
        self.assertEqual(sample["stages"][sample["current_stage"]]["status"], "in_progress")
        dashboard = (orchestrate / "references/progress_dashboard_template.md").read_text()
        rendered_stages = [stage.replace("'", "p") for stage in
                           re.findall(r"^  Stage ([1-6](?:'|\.5)?) ", dashboard, re.M)]
        self.assertEqual(rendered_stages, current_stages)

    def test_old_claim_keys_survive_collision_in_example_handoff(self):
        directory = ENGINE / "contracts/passport"
        claim_schema = json.loads((directory / "claim_intent_manifest.schema.json").read_text())
        claim = claim_schema["properties"]["claims"]["items"]["properties"]["claim_id"]
        doc = (ROOT / "references/handoff.md").read_text()
        rows = re.findall(r"^\| A \| (C-\d+) \| B \| (C-\d+) \| (.+?) \|$", doc, re.M)
        self.assertEqual(set(k for k, _, _ in rows), {"C-001", "C-01"})
        by_target = {target: (source, refs) for source, target, refs in rows}
        self.assertEqual(len(by_target), 2)
        for target in by_target:
            Draft202012Validator(claim).validate(target)
        figure_target = next(target for target, (_, refs) in by_target.items() if "F-01" in refs)
        self.assertEqual(by_target[figure_target][0], "C-01")
        source_schema = json.loads((directory / "literature_corpus_entry.schema.json").read_text())
        self.assertIn("year", source_schema["required"])
        self.assertFalse(Draft202012Validator(source_schema["properties"]["year"]).is_valid("未知"))


if __name__ == "__main__":
    unittest.main()
