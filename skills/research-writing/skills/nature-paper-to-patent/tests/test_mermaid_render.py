from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "mermaid_render.py"
SPEC = importlib.util.spec_from_file_location("mermaid_render", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MermaidCommandTests(unittest.TestCase):
    def test_missing_word_output_fails_and_preserves_previous_export(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "draft.md"
            markdown = Path(directory) / "disclosure.md"
            word = markdown.with_suffix(".docx")
            source.write_text("# Updated disclosure", encoding="utf-8")
            word.write_bytes(b"previous export")
            args = ["-i", str(source), "-o", str(markdown), "--no-math"]
            # A converter can exit successfully without producing the requested file.
            with mock.patch.object(MODULE.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)):
                self.assertNotEqual(MODULE.main(args), 0)
                self.assertEqual(MODULE.main([*args, "--no-docx"]), 0)
            self.assertEqual(markdown.read_text(encoding="utf-8").strip(), "# Updated disclosure")
            self.assertEqual(word.read_bytes(), b"previous export")

    def test_windows_npx_is_resolved_to_an_executable_path(self) -> None:
        def which(command: str) -> str | None:
            if command == "npx":
                return r"C:\Program Files\nodejs\npx.cmd"
            return None

        with mock.patch.object(MODULE, "_local_mmdc", return_value=None), mock.patch.object(
            MODULE.shutil, "which", side_effect=which
        ):
            command = MODULE._find_mmdc_invocation()

        self.assertEqual(command[0], r"C:\Program Files\nodejs\npx.cmd")
        self.assertEqual(command[1:], ["-y", "@mermaid-js/mermaid-cli", "mmdc"])

    def test_render_keeps_paths_as_separate_arguments(self) -> None:
        completed = subprocess.CompletedProcess([], 0, "", "")
        with tempfile.TemporaryDirectory(prefix="mermaid path ") as directory, mock.patch.object(
            MODULE.subprocess, "run", return_value=completed
        ) as run:
            output = Path(directory) / "figures & charts" / "diagram.png"
            MODULE._render_one_mermaid(
                "graph TD; A-->B",
                output,
                [r"C:\Program Files\nodejs\npx.cmd", "-y", "@mermaid-js/mermaid-cli", "mmdc"],
                scale=2.0,
                width=1400,
                height=1050,
            )

        command = run.call_args.args[0]
        self.assertIsInstance(command, list)
        self.assertIn(str(output), command)
        self.assertNotIn("shell", run.call_args.kwargs)

    def test_missing_mermaid_runtime_has_an_actionable_error(self) -> None:
        with mock.patch.object(MODULE, "_local_mmdc", return_value=None), mock.patch.object(
            MODULE.shutil, "which", return_value=None
        ):
            with self.assertRaisesRegex(RuntimeError, "Node.js"):
                MODULE._find_mmdc_invocation()


if __name__ == "__main__":
    unittest.main()
