"""Cross-check the local rebuttal contract against the synthesis gate."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

ENGINE = Path(__file__).resolve().parents[1] / "engine"
sys.path.insert(0, str(ENGINE))
from scripts import check_re_review_synthesis as synthesis


class LocalRebuttalTests(unittest.TestCase):
    def setUp(self):
        schema = (ENGINE / "contracts/re_review/traceability.schema.json").read_text()
        self.validator = Draft202012Validator(json.loads(schema))
        common = {"contract_version": "1.1", "round_id": "round-2"}
        self.manifest = dict(common, artifacts={"editorial_decision_letter": {"present": False}})
        self.roadmap = {"id": "REV-1", "obligation_class": "must_fix", "severity": "major",
                        "verification_criteria": "Report the sample count.", "reviewer": "R1"}
        criterion = {
            "item_id": "REV-1", "obligation_class": "must_fix",
            "inherited_criterion": {"roadmap_text": self.roadmap["verification_criteria"]},
            "operationalization": {"fully_addressed": "Count is reported.",
                                   "partially_addressed": "Only one group is reported.",
                                   "made_worse_discriminator": "Counts now contradict the data."},
            "expected_change_surface": "Table 1", "equivalence_policy": "allowed",
            "source_reviewer": "R1", "source_reviewer_labels": ["R1"],
        }
        self.precommitment = dict(common, items=[criterion], new_standards=[],
                                  input_manifest_hash=synthesis.canonical_hash(self.manifest))
        verdict = {"item_id": "REV-1", "applied_criterion": "precommitted", "verdict": "NOT_ADDRESSED",
                   "verified_by": "R1", "change_summary": "No change to Table 1.",
                   "evidence_anchor": ["table: Table 1"]}
        self.verdicts = dict(common, items=[verdict], dissents=[], new_issues=[], escalation_exceptions=[],
                             precommitment_hash=synthesis.canonical_hash(self.precommitment))
        self.author = {"author_triage": "will_address", "authorized_targets": [], "claim_strength_authorizations": []}
        self.body = {
            "item_id": "REV-1", "from_verdict": "NOT_ADDRESSED", "to_verdict": "FULLY_ADDRESSED",
            "basis": "valid_rebuttal", "rationale": "The existing supplement gives both counts.",
            "evidence_anchor": [{"anchor": "text: Response 1, paragraph 2", "anchor_artifact": "letter"}],
        }
        self.adjustment = dict(self.body, adjustment_id="ADJ-1")
        self.proposal = {"item_id": "REV-1", "proposal_id": "PRB-1", "drafted_adjustment": self.body,
                         "disposition": "booked:ADJ-1"}
        row = dict(self.author, item_id="REV-1", concern_id="R1", obligation_class="MUST_FIX",
                   original_comment="Report the sample count.", authors_claim="See Table S1.",
                   revision_location="Response 1", quality_assessment=self.body["rationale"], verified="YES",
                   status="FULLY_ADDRESSED", phase2a_verdict="NOT_ADDRESSED", final_verdict="FULLY_ADDRESSED",
                   verified_by="R1", adjustment_id="ADJ-1", addressed_by_rebuttal=True)
        self.operand = {"item_id": "REV-1", "final_verdict": "FULLY_ADDRESSED", "driving_severity": "major"}
        counts = {group: dict.fromkeys(synthesis.VERDICTS, 0) for group in synthesis.OBLIGATION_CLASSES}
        counts["must_fix"]["FULLY_ADDRESSED"] = 1
        residuals = {group: dict.fromkeys(synthesis.RESIDUAL_OBLIGATION_CLASSES, 0)
                     for group in synthesis.OBLIGATION_CLASSES}
        inputs = dict(per_item=[self.operand], verdict_counts=counts, residual_obligation_class_counts=residuals,
                      should_fix_addressed_rate={"numerator": 0, "denominator": 0}, regressions=[],
                      non_regression_new_issue_ids=[], escalations=[], apply_chain_witness="not_run_no_reports",
                      reject_recommended=False)
        self.trace = dict(common, revision=1, verdict_record_hash=synthesis.canonical_hash(self.verdicts),
                          rows=[row], adjustments=[self.adjustment], new_issues=[], post_letter_observations=[],
                          dissent_adjudications=[], resolution_intents=[], g2d_acceptances=[], escalation_approvals=[],
                          reapplications=[], pending_rebuttal_upgrades=[self.proposal], decision_inputs=inputs,
                          decision_state="Accept")

    def run_synthesis(self):
        self.validator.validate(self.trace)
        synthesis.validate_precommitment(self.precommitment)
        synthesis.validate_verdict_record(self.verdicts)
        synthesis.validate_traceability(self.trace)
        failures, _, _ = synthesis.check(self.manifest, self.precommitment, self.verdicts, self.trace,
                                         [self.roadmap], {"REV-1": self.author}, None, "not_run_no_reports", [])
        return failures.messages

    def test_ordinary_rebuttal_accepts_direct_booking(self):
        self.assertEqual(self.run_synthesis(), [])
        self.proposal["disposition"] = "booked_single_family:ADJ-1"
        self.assertTrue(self.run_synthesis())

    def test_critical_rebuttal_needs_local_disclosure_and_matching_proposal(self):
        self.roadmap["severity"] = self.operand["driving_severity"] = "critical"
        self.proposal["disposition"] = "booked_single_family:ADJ-1"
        self.assertTrue(self.run_synthesis())
        self.adjustment["critical_rebuttal_check"] = "single_family_disclosed"
        self.assertEqual(self.run_synthesis(), [])
        self.proposal["disposition"] = "booked:ADJ-1"
        self.assertTrue(self.run_synthesis())
        self.trace["pending_rebuttal_upgrades"].clear()
        self.assertTrue(self.run_synthesis())

    def test_booking_requires_the_original_proposal_evidence(self):
        self.adjustment["evidence_anchor"] = [{"anchor": "text: Unrelated paragraph", "anchor_artifact": "letter"}]
        self.assertTrue(self.run_synthesis())

    def test_retired_external_verdicts_fail_both_validators(self):
        for record, key, value in (
            (self.proposal, "disposition", "challenged:RADJ-1"),
            (self.proposal, "disposition", "booked_disclosed:ADJ-1"),
            (self.adjustment, "critical_rebuttal_check", "adjudicated:RADJ-1"),
            (self.adjustment, "critical_rebuttal_check", "pass_unavailable_disclosed"),
        ):
            with self.subTest(value=value), patch.dict(record, {key: value}):
                self.assertFalse(self.validator.is_valid(self.trace))
                with self.assertRaises(synthesis.ArtifactSchemaError):
                    synthesis.validate_traceability(self.trace)
