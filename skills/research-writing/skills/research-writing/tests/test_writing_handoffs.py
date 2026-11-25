"""Cross-role regressions using the shipped writers, templates and verification scripts."""
import hashlib
import importlib.util
import json
import re
import sys
import subprocess
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from scripts import check_acronyms, verify_submission_package as submission
from scripts._claim_audit_constants import JUDGE_PROMPT_SHA256
from scripts.uncited_assertion_detector import detect_uncited


def load_helper(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def venue_checks(text, **limits):
    return {row["id"]: row["status"] for row in
            submission.run_family_b({"paper.md": text}, set(), "", limits)}


class WritingHandoffs(unittest.TestCase):
    def test_writer_bilingual_abstract_in_submission_package(self):
        agent = (ROOT / "roles/draft/paper/agents/abstract_bilingual_agent.md").read_text()
        block = agent.split("```markdown\n## Abstract\n", 1)[1].split("```", 1)[0]
        block = re.sub(r"^\[Background\].*$", "This result was replicated.", block, count=1, flags=re.M)
        block = re.sub(r"^\[Research Background\].*$", "观察可重复。", block, count=1, flags=re.M)
        manuscript = "## Abstract\n" + block + "\n## 正文\n试验" * 2
        limits = {"abstract_limits": {"en": 4, "zh": 5}, "keyword_range": {"min": 5, "max": 5}}
        self.assertEqual(venue_checks(manuscript, **limits)["B2"], "pass")
        self.assertEqual(venue_checks(manuscript, **limits)["B3"], "pass")
        for language in ("en", "zh"):
            with self.subTest(language=language):
                tighter = {**limits["abstract_limits"], language: 2}
                self.assertEqual(venue_checks(manuscript, abstract_limits=tighter)["B2"], "fail")
        self.assertEqual(venue_checks(manuscript.replace("观察可重复。", ""), **limits)["B2"], "not_checked")

    def test_zh_and_en_monolingual_caps_and_reference_scope(self):
        chinese = "## 摘要\n实验结果可靠。\n关键词：测试，声学\n## 正文\n" + "中文" * 5000
        chinese += "\n## 参考文献\nJones (2024)\n"
        verdicts = venue_checks(chinese, word_limit=2000, abstract_word_limit=6,
                                keyword_range={"min": 2, "max": 2})
        self.assertEqual([verdicts[k] for k in ("B1", "B2", "B3")], ["fail", "pass", "pass"])
        self.assertNotIn("Jones", submission._strip_reference_section(chinese))
        self.assertEqual(venue_checks("## Abstract\nWe observed two trials.", abstract_word_limit=3)["B2"], "fail")

    def test_reference_section_preserves_appendix_citations(self):
        for reference_title, appendix_title in (
            ("## 参考文献", "## 附录 A"), ("Bibliography\n------------", "Appendix A\n----------")
        ):
            with self.subTest(reference_title=reference_title):
                refs = (f"## Results\nText <!--ref:main-->\n{reference_title}\n"
                        "### First edition\nEntry <!--ref:not-in-prose-->\n"
                        f"{appendix_title}\nResult <!--ref:appendix--> and <!--ref:missing-->.")
                rows, path = submission.run_family_c(
                    {"paper.md": refs}, {}, {"main", "appendix"}, {"main", "appendix"}, ".bib")
                by_id = {row["id"]: row for row in rows}
                self.assertEqual(path, "joined_marker")
                self.assertEqual(by_id["C1"]["status"], "fail")
                self.assertIn("missing", by_id["C1"]["detail"])
                self.assertNotIn("not-in-prose", by_id["C1"]["detail"])
                self.assertEqual(by_id["C2"]["status"], "pass")

        # The same text boundary applies to author-year fallback, including the
        # unresolved appendix citation. Bare headings in plain text keep the
        # historical terminal-reference-list convention.
        text = "## Results\nJones (2022)\n## References\nGhost (2000)\n# Appendix\nSmith (2024)"
        cited, unresolved = submission._extract_fallback({"paper.md": text}, {("jones", "2022"): {"jones"}})
        self.assertIn("jones", cited)
        self.assertTrue(any("Smith" in item for item in unresolved))
        self.assertFalse(any("Ghost" in item for item in unresolved))
        self.assertNotIn("Ghost", submission._strip_reference_section("Body.\nReferences\nGhost (2000)"))

    def test_nonleaf_abstract_and_empty_abstract(self):
        self.assertEqual(venue_checks("## English Abstract\n### A study\none two three\n",
                                      abstract_word_limit=2)["B2"], "fail")
        self.assertEqual(venue_checks("## 摘要\n\n---\n关键词：研究\n## 正文\n内容",
                                      abstract_word_limit=5)["B2"], "not_checked")

    def test_citation_audit_preserves_source_and_recognizes_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            manuscript = Path(directory) / "paper.md"
            raw = b"Results showed a 20% improvement. <!--ref:lee-->\n"
            manuscript.write_bytes(raw)
            cited = manuscript.read_text()
            self.assertFalse(detect_uncited(cited)[0])
            self.assertTrue(detect_uncited(cited.split("<!--", 1)[0])[0])
            submission.run_family_c({"paper.md": cited}, {}, {"lee"}, {"lee"}, "references")
            self.assertEqual(manuscript.read_bytes(), raw)

    def test_judge_cache_tracks_distributed_prompt(self):
        text = (ROOT / "roles/orchestrate/agents/claim_ref_alignment_audit_agent.md").read_text()
        prompt = text.split("<!-- JUDGE-PROMPT-CANONICAL-START -->")[1].split("<!-- JUDGE-PROMPT-CANONICAL-END -->")[0]
        self.assertEqual(hashlib.sha256(prompt.strip().encode()).hexdigest(), JUDGE_PROMPT_SHA256)

    def test_simplified_chinese_abbreviations(self):
        text = (
            "## 方法\n"
            "结构方程模型（以下简称 SEM）、主成分分析（PCA）、独立成分分析（ICA）与非负矩阵分解（NMF）"
            "用于 IV级 与 II类 样本估计，并在子组比较（PCA与ICA，NMF）中复核。\n"
            "资料来源：内部队列统计（WHO）。\n"
            "## 参考文献\nIEEE NLP\n"
        )
        report = check_acronyms.check(text, scopes=("body",))
        self.assertEqual(report["status"], "checked")
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["coverage_limits"], [])

    def test_redline_template_with_nested_macros(self):
        checker = load_helper("rsp_redline", "roles/review/respond/scripts/check_package_consistency.py")
        template = (ROOT / "roles/review/respond/templates/revised-manuscript-redline.tex").read_text()
        start = template.index(r"\section{Introduction}")
        body = re.sub(r"\\revised\{([^{}]*)\}", r"\1", template[start:])
        clean = r"\documentclass{article}\begin{document}" + body
        self.assertEqual(checker.check_clean_marked(clean, template, "clean", "marked"), [])
        sentence = r"Result from \cite{Lee}: $x_{1}$."
        marked = r"\textcolor{red}{" + sentence + "}"
        self.assertEqual(checker.check_clean_marked(sentence, marked, "clean", "marked"), [])
        self.assertTrue(checker.check_clean_marked("Different conclusion.", marked, "clean", "marked"))

    def test_figure_package_survives_strict_handoff_and_resume(self):
        import yaml
        producer = ROOT / "roles/figures/make/ars-visualization/references/vlm_figure_verification.md"
        example = producer.read_text().split("```yaml\nfigure_table_trace:", 1)[1].split("```")[0]
        packet = yaml.safe_load("figure_table_trace:" + example)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "figures.yaml"
            path.write_text(yaml.safe_dump(packet))
            cli = [sys.executable, str(ROOT / "engine/scripts/check_figure_trace.py")]
            def run(*args):
                return subprocess.run([*cli, *args], capture_output=True, text=True)
            current = run("--package", path, "--figure", "fig-3")
            self.assertEqual(current.returncode, 0, current.stderr)
            digest = json.loads(current.stdout)["sha256"]
            self.assertEqual(run("--package", path, "--figure", "fig-3", "--expected-sha256", digest).returncode, 0)
            path.write_text("figure_table_trace: []")
            self.assertEqual(run("--package", path, "--figure", "fig-3").returncode, 1)
            self.assertEqual(run("--package", path, "--expected-sha256", digest).returncode, 1)
            legacy = run("--figure", "fig-3", "--table", "tab-1")
            self.assertEqual(legacy.returncode, 0)
            self.assertEqual(len(json.loads(legacy.stdout)["notes"]), 2)

    def test_trace_rejects_unknown_values_and_preserves_empty_limitations_note(self):
        from scripts.check_figure_trace import check_trace
        row = dict(artifact_id="F1", source_data="measures.csv", transformation={"script": "plot.py", "hash": "12abc"},
                   caption_claim="Group A is larger.", supported_manuscript_claims=[{"claim": "Group A is larger."}],
                   limitations=[])
        def run(**fields):
            return check_trace({"figure_table_trace": [dict(row, **fields)]}, ["F1"])
        self.assertFalse(run()["errors"])
        self.assertTrue(run()["notes"])
        for field, value in (("source_data", {}), ("source_data", "未知"), ("transformation", {"script": "plot.py"}),
                             ("caption_claim", None), ("supported_manuscript_claims", []),
                             ("supported_manuscript_claims", [{"claim": "C-001"}]), ("limitations", ["unknown"])):
            with self.subTest(field=field, value=value):
                self.assertTrue(run(**{field: value})["errors"])

    def test_re_review_manifest_accepts_local_and_legacy_disabled_config(self):
        import jsonschema
        from scripts.check_re_review_synthesis import ManifestError, validate_manifest
        required = ("original_manuscript", "revised_manuscript", "revision_roadmap",
                    "author_adjudication", "revision_evidence_bundle")
        optional = ("editorial_decision_letter", "response_to_reviewers", "round1_findings",
                    "round1_config_cards", "revision_patches", "apply_reports")
        artifacts = {k: {"present": True, "path_or_passport_ref": "path:" + k, "sha256": "a" * 64,
                         "version_label": None, "origin_date": None} for k in required}
        artifacts.update({k: {"present": False} for k in optional})
        manifest = {"contract_version": "1.1", "round_id": "round1", "artifacts": artifacts}
        schema = json.loads((ROOT / "engine/contracts/re_review/input_manifest.schema.json").read_text())
        jsonschema.validate(manifest, schema)
        jsonschema.validate(dict(manifest, cross_model_active=False), schema)
        validate_manifest(manifest)
        validate_manifest(dict(manifest, cross_model_active=False))
        with self.assertRaises(ManifestError):
            validate_manifest(dict(manifest, cross_model_active=True))

    def test_legacy_chinese_heading_with_or_without_locale(self):
        for title in ("Chinese Abstract", "Chinese Abstract (zh-TW)"):
            with self.subTest(title=title):
                text = f"## {title}\n研究結果。\n**關鍵詞**：聲學、測試"
                verdict = venue_checks(text, abstract_limits={"zh": 4}, keyword_range={"min": 2, "max": 2})
                self.assertEqual([verdict["B2"], verdict["B3"]], ["pass", "pass"])

    def test_rotated_svg_label_remains_auditable(self):
        audit = load_helper("rsp_svg", "roles/figures/make/scripts/audit_svg_schematic.py")
        data = b'<svg xmlns="http://www.w3.org/2000/svg" width="60mm" height="20mm" viewBox="0 0 60 20"><text x="10" y="10" font-size="2" transform="rotate(15)">Label</text></svg>'
        self.assertTrue(audit.audit_svg(data)["auditable"])

    def test_pdf_text_with_nested_stream_dictionary(self):
        audit = load_helper("rsp_pdf", "roles/figures/make/scripts/audit_pdf_text.py")
        payload = zlib.compress(b"BT /F1 12 Tf (Test) Tj ET")
        data = b"1 0 obj\n<< /Filter /FlateDecode /DecodeParms << /Predictor 1 >> >>\nstream\n" + payload + b"\nendstream\nendobj"
        self.assertTrue(audit.audit_pdf(data)["auditable"])

    def test_markdown_percent_survives_consistency_check(self):
        audit = load_helper("rsp_consistency", "references/nature-shared/scripts/check_consistency.py")
        text = "95% CI at a depth of 35 mm.\n95% CI at a depth of 3.5 cm."
        self.assertTrue(audit.check_equivalent_length_units({Path("paper.md"): text}))
        self.assertFalse(audit.check_equivalent_length_units({Path("paper.tex"): text}))


if __name__ == "__main__":
    unittest.main()
