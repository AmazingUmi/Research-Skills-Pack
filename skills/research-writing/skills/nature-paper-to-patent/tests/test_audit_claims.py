import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audit_claims", ROOT / "scripts" / "audit_claims.py")
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def codes(text):
    return [finding.code for finding in AUDIT.audit(text)]


class AntecedentBasisTests(unittest.TestCase):
    def test_term_used_with_suo_shu_but_never_introduced_is_flagged(self):
        self.assertIn("ANTECEDENT_BASIS", codes("1. 一种装置，其特征在于，包括所述电极。\n"))

    def test_term_introduced_earlier_in_the_same_claim_is_not_flagged(self):
        self.assertNotIn(
            "ANTECEDENT_BASIS", codes("1. 一种检测装置，其特征在于，包括电极和基板，所述电极设置于所述基板上。\n")
        )

    def test_term_introduced_in_a_referenced_claim_is_not_flagged(self):
        text = "1. 一种检测装置，其特征在于，包括电极和基板。\n2. 根据权利要求1所述的装置，其特征在于，所述电极为金属电极。\n"
        self.assertNotIn("ANTECEDENT_BASIS", codes(text))

    def test_disjunctive_self_and_forward_references_block_delivery(self):
        first = "1. 一种检测装置，其特征在于，包括电极和基板。"
        for reference in ("1或2", "1、3", "1至3", "1或权利要求3"):
            claim = f"2. 根据权利要求{reference}所述的装置，其特征在于，包括外壳。"
            findings = AUDIT.audit(first + "\n" + claim)
            self.assertIn(("ERROR", "FORWARD_REFERENCE"), {(f.level, f.code) for f in findings})

    def test_antecedents_follow_only_transitive_references(self):
        first = "1. 一种检测装置，其特征在于，包括电极和基板。"
        second = "2. 根据权利要求1所述的装置，其特征在于，包括端帽。"
        third = "3. 根据权利要求{}所述的装置，其特征在于，所述端帽为铜制。"
        def inspect(ref):
            return AUDIT.audit("\n".join([first, second, third.format(ref)]))
        self.assertIn(("WARNING", 3, "ANTECEDENT_BASIS"),
                      {(f.level, f.claim, f.code) for f in inspect(1)})
        self.assertNotIn("ANTECEDENT_BASIS", [f.code for f in inspect(2)])


class GenericReferenceTests(unittest.TestCase):
    def test_reference_phrase_in_a_dependent_claim_is_not_a_term(self):
        text = "1. 一种检测装置，其特征在于，包括电极和基板，所述电极设置于所述基板上。\n2. 根据权利要求1所述的检测装置，其特征在于，所述电极为金属电极。\n"
        self.assertNotIn("ANTECEDENT_BASIS", codes(text))


if __name__ == "__main__":
    unittest.main()
