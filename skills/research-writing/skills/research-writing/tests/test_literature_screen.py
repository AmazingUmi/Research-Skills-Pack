"""Exercise RIS preparation, both screening stages, and PRISMA reporting offline."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "roles/literature/screen/scripts"
sys.path.insert(0, str(SCRIPTS))
import srlib


class ScreeningHandoffTests(unittest.TestCase):
    def test_fulltext_reasons_locations_and_pdf_identity(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            work, out = root / "work", root / "outputs"

            def run(script, *args):
                subprocess.run([sys.executable, str(SCRIPTS / script), "--work", str(work), *map(str, args)],
                               capture_output=True, text=True, check=True)

            title = "A comparative study of seasonal measurements"
            ris = root / "import.ris"
            ris.write_text("".join(f"TY  - JOUR\nTI  - {title}\nAU  - {author}\nPY  - 2024\nER  - \n\n"
                                   for author in ("Green, A", "White, B")), encoding="utf-8")
            run("prepare_records.py", "--inputs", ris)
            ids = [rec["id"] for rec in srlib.load_json(work / "records.json")["unique"]]
            self.assertEqual(len(ids), 2)
            self.assertEqual(len(srlib.load_json(work / "candidate_duplicates.json")), 1)
            protocol = root / "protocol.md"
            protocol.write_text("Include prospective seasonal observations. " * 6, encoding="utf-8")
            cfg = srlib.load_config(None)
            source = root / "reviews.json"

            def merge(stage, labels, overrides=None):
                ctx = srlib.activate_context(work, stage, protocol, cfg)["context_id"]
                source.write_text(json.dumps([{"label": f"{label}@{ctx}", "decisions": rows}
                                              for label, rows in labels]), encoding="utf-8")
                run("merge_decisions.py", "--stage", stage, "--from", source,
                    *(("--overrides", overrides) if overrides else ()))

            def report(stage):
                run("build_outputs.py", "--stage", stage, "--out", out)
                return srlib.load_json(out / f"{stage.upper()}_prisma_counts.json")

            ta = [{"id": rid, "d": "include", "code": "INC"} for rid in ids]
            merge("ta", [(f"{role}:b001", ta) for role in ("A", "B")])
            self.assertTrue(report("ta")["complete"])
            pdf = root / f"{ids[0]}.pdf"
            pdf.write_bytes(b"%PDF-1.5\nfixture")
            run("prepare_fulltext.py", "--pdf-dir", root)
            exclusion = {"id": ids[0], "d": "exclude", "code": srlib.exclusion_codes(cfg, "ft")[0],
                         "why": "Population outside the confirmed protocol"}
            overrides = root / "overrides.csv"
            overrides.write_text(f"id,d,code,why,where\n{ids[0]},exclude,{exclusion['code']},,\n", encoding="utf-8")
            labels = [(f"{role}:{ids[0]}", [exclusion]) for role in ("FTA", "FTB")]
            merge("ft", labels, overrides)
            self.assertFalse(report("ft")["complete"])
            exclusion["where"] = "page 2, study population"
            merge("ft", labels)
            counts = report("ft")
            self.assertTrue(counts["complete"])
            self.assertEqual((counts["reports_not_retrieved"], counts["reports_excluded"]), (1, 1))
            pdf.write_bytes(b"%PDF-1.5\nnew revision")
            counts = report("ft")
            self.assertFalse(counts["complete"])
            self.assertEqual(counts["reports_assessed"], 0)


if __name__ == "__main__":
    unittest.main()
