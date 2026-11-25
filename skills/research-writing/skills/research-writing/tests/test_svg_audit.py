import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

AUDIT = Path(__file__).resolve().parents[1] / "roles/figures/make/scripts/audit_svg_schematic.py"


class EditableSchematicTests(unittest.TestCase):
    def test_rotated_label_is_checked_at_its_final_position(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "figure.svg"
            for transform, x, expected in [("", 20, 0), ("rotate(-90 20 75)", 20, 0),
                                           ("rotate(-90 20 75)", 300, 1)]:
                with self.subTest(transform=transform, x=x):
                    path.write_text(
                        '<svg xmlns="http://www.w3.org/2000/svg" width="89mm" height="89mm" viewBox="0 0 252 252">'
                        f'<text x="{x}" y="75" font-size="6" transform="{transform}">Axis</text></svg>'
                    )
                    result = subprocess.run([sys.executable, str(AUDIT), str(path), "--json"],
                                            text=True, capture_output=True)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    report = json.loads(result.stdout)
                    self.assertTrue(report["auditable"])
                    if expected:
                        self.assertIn("text.off-canvas", {f["kind"] for f in report["findings"]})
