"""Run the public build command on rejected drafts and existing packages."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from test_validation import valid_draft

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def build(directory, draft):
    source = directory / "source.json"
    source.write_text(json.dumps(draft, ensure_ascii=False), encoding="utf-8")
    return subprocess.run([sys.executable, str(SCRIPTS / "build_patent_package.py"),
                           str(source), "--output-dir", str(directory / "delivery"), "--prefix", "sample"],
                          cwd=directory, capture_output=True, text=True)


def self_referential():
    draft = valid_draft()
    draft["claims"].append({"number": 2, "text": "根据权利要求1或2所述的方法，其特征在于，输出融合特征。"})
    draft["claim_feature_map"].append({"claim_number": 2, "feature": "融合特征", "evidence_ids": ["EV1"]})
    return draft


def snapshot(directory):
    return {p.relative_to(directory): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob("*") if p.is_file()}


class BuildGateTests(unittest.TestCase):
    def test_rejected_first_build_writes_only_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = build(root, self_referential())
            self.assertEqual(result.returncode, 1, result.stderr)
            output = root / "delivery"
            reports = {p.name for p in output.iterdir()}
            self.assertEqual(reports, {"sample-草稿验证报告.txt", "sample-权利要求检查.txt"})
            self.assertIn("FORWARD_REFERENCE", (output / "sample-权利要求检查.txt").read_text(encoding="utf-8"))

    def test_failed_retry_preserves_all_prior_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "delivery"
            output.mkdir()
            for name in ("权利要求书.docx", "权利要求书.txt", "权利要求检查.txt", "草稿验证报告.txt"):
                (output / ("sample-" + name)).write_bytes(b"previous edition")
            (output / "sample-figures").mkdir()
            (output / "sample-figures/figure_1.svg").write_bytes(b"previous drawing")
            previous = snapshot(output)
            result = build(root, self_referential())
            self.assertEqual(result.returncode, 1, result.stderr)
            after = snapshot(output)
            self.assertEqual({p: after[p] for p in previous}, previous)
            rejected = [p for p in after if p not in previous]
            self.assertEqual(len(rejected), 2)
            self.assertTrue(all(p.parts[0].startswith("sample-failed-") for p in rejected))
            self.assertIn("FORWARD_REFERENCE", next((output / p).read_text(encoding="utf-8")
                                                   for p in rejected if "权利要求检查" in p.name))

    def test_valid_build_renders_documents_and_figures(self):
        from importlib.util import find_spec
        for dependency in ("docx", "latex2mathml", "PIL"):
            if find_spec(dependency) is None:
                self.skipTest(f"Full DOCX render requires {dependency}")
        sys.path.insert(0, str(SCRIPTS))
        try:
            from render_flowchart_svg import load_font
            try:
                load_font(18)
            except ValueError as error:
                self.skipTest(str(error))
        finally:
            sys.path.remove(str(SCRIPTS))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = build(root, valid_draft())
            self.assertEqual(result.returncode, 0, result.stderr)
            output = root / "delivery"
            self.assertEqual(len(list(output.glob("sample-*.docx"))), 5)
            self.assertTrue(list((output / "sample-figures").glob("*.png")))
            with zipfile.ZipFile(output / "sample-完整审阅稿.docx") as z:
                self.assertIn(b"<m:oMath", z.read("word/document.xml"))
                self.assertTrue(any(p.startswith("word/media/") for p in z.namelist()))
