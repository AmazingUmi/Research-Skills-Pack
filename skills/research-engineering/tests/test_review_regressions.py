"""Run with unittest discover. Numeric cases use the dependencies of the tested skill."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILLS = Path(__file__).resolve().parents[1] / "skills"
UNITS = SKILLS / "uncertainty-and-units/scripts"


def cli(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)],
                          text=True, capture_output=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ScientificCliTests(unittest.TestCase):
    def run_spec(self, script, spec, *args):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(spec))
            return cli(UNITS / script, "--spec", path, *args)

    def test_budget_requires_source_and_converts_components(self):
        script = "uncertainty_budget.py"
        self.assertNotEqual(cli(UNITS / script).returncode, 0)
        components = [dict(distribution="normal", value=0.1, unit="mm"),
                      dict(distribution="normal", value=100, unit="µm")]
        result = self.run_spec(script, dict(unit="mm", components=components))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertAlmostEqual(json.loads(result.stdout)["combined_standard_uncertainty"], 0.02**0.5)
        components[0]["unit"] = "second"
        self.assertNotEqual(self.run_spec(script, dict(unit="mm", components=components)).returncode, 0)

    def test_propagation_converts_uncertainty_and_samples(self):
        spec = dict(expression="a+b", unit="m", variables=[
            dict(name="a", value=1, u=0.1, unit="m"), dict(name="b", value=50, u=10, unit="cm")])
        result = self.run_spec("propagate_uncertainty.py", spec, "--trials", 10000, "--seed", 7)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertAlmostEqual(report["gum_framework"]["value"], 1.5)
        self.assertAlmostEqual(report["gum_framework"]["combined_standard_uncertainty"], 0.02**0.5)
        self.assertAlmostEqual(report["monte_carlo"]["mean"], 1.5, delta=0.01)
        self.assertAlmostEqual(report["monte_carlo"]["standard_uncertainty"], 0.02**0.5, delta=0.01)
        spec["unit"] = "s"
        self.assertNotEqual(self.run_spec("propagate_uncertainty.py", spec).returncode, 0)

    def test_unit_conversion_preserves_each_input_derivative(self):
        # Pint quantities must preserve the identity of each uncertainties.Variable.
        for expression, source, output, nominal, u in (
            ("a", "m", "cm", 400, 10), ("sqrt(a)", "m**2", "cm", 200, 2.5),
            ("a**2", "cm", "m**2", 0.0016, 0.00008)
        ):
            with self.subTest(expression=expression):
                spec = dict(expression=expression, unit=output, variables=[dict(name="a", value=4, u=.1, unit=source)])
                result = self.run_spec("propagate_uncertainty.py", spec, "--no-monte-carlo")
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)["gum_framework"]
                self.assertAlmostEqual(report["value"], nominal)
                self.assertAlmostEqual(report["combined_standard_uncertainty"], u)

    def test_malformed_units_return_cli_errors(self):
        for unit in ("m /", "(m", "2*m"):
            with self.subTest(unit=unit):
                spec = dict(unit="m", components=[dict(distribution="normal", value=1, unit=unit)])
                budget = self.run_spec("uncertainty_budget.py", spec)
                model = dict(expression="a", unit="m", variables=[dict(name="a", value=1, u=.1, unit=unit)])
                propagation = self.run_spec("propagate_uncertainty.py", model, "--no-monte-carlo")
                for result in (budget, propagation):
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertTrue(result.stderr.startswith("error:"), result.stderr)

    def test_m_file_block_comment_delimiters(self):
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory).resolve() / "sample.m"
            src.write_text("%{ section\nsystem('example');\n%{\x0c section\nsystem('vt');\n%{\u00a0\neval(nbsp);\n%{\n%{\n%}\neval(expr);\n%}\neval(expr);\n", encoding="utf-8")
            result = cli(SKILLS / "matlab/scripts/scan_m_code.py", src, "--root", src.parent)
            self.assertNotIn("Traceback", result.stderr)
            rows = json.loads(result.stdout)["findings"]
            self.assertEqual({2, 4, 6, 12}, {row["line"] for row in rows})

    def test_text_file_and_unit_attributes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.txt"
            result = cli(UNITS / "format_result.py", "--value", "5", "--uncertainty", ".1",
                         "--format", "text", "--unit", "m", "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("±", output.read_text())
            source = Path(directory) / "units.py"
            source.write_text("x = 20 * ureg.degC + 5 * ureg.degC")
            audit = cli(UNITS / "audit_units.py", "--input", source)
            self.assertIn("UNIT002", {i["rule"] for i in json.loads(audit.stdout)["results"][0]["findings"]})


class ClassificationTests(unittest.TestCase):
    def test_categorical_missing_and_absent_test_class(self):
        import pandas as pd
        pipeline = load_module("classification_pipeline", SKILLS / "scikit-learn/scripts/classification_pipeline.py")
        x = pd.DataFrame({"integer": pd.Series([1, 2, None], dtype="Int64"),
                          "boolean": pd.Series([True, False, None], dtype="boolean")})
        encoded = pipeline.create_preprocessing_pipeline([], list(x)).fit_transform(x)
        self.assertEqual(encoded.shape, (3, 6))
        with self.assertRaisesRegex(ValueError, "Test split has no samples"):
            pipeline.train_and_evaluate_model(pd.DataFrame({"constant": [1]*120}),
                                              [0]*114+[1]*6, ["constant"], [], test_size=.05)


class CheckInspectionTests(unittest.TestCase):
    def test_json_for_a_green_pull_request(self):
        gh = load_module("inspect_checks", SKILLS / "gh-fix-ci/scripts/inspect_pr_checks.py")
        response = gh.GhResult(0, '[{"name":"tests","bucket":"pass","state":"SUCCESS"}]', "")
        output = io.StringIO()
        with patch.object(sys, "argv", ["inspect_pr_checks.py", "--json", "--pr", "7"]), \
             patch.object(gh, "find_git_root", return_value=SKILLS), \
             patch.object(gh, "ensure_gh_available", return_value=True), \
             patch.object(gh, "run_gh_command", return_value=response), redirect_stdout(output):
            self.assertEqual(gh.main(), 0)
        self.assertEqual(json.loads(output.getvalue()), {"pr": "7", "results": []})

    def test_external_check_and_cross_repo_job(self):
        gh = load_module("inspect_checks", SKILLS / "gh-fix-ci/scripts/inspect_pr_checks.py")
        responses = [gh.GhResult(0, "{}", ""), gh.GhResult(0, "FAIL: bad result", "")]
        with patch.object(gh, "run_gh_command", side_effect=responses) as run:
            info = gh.analyze_check(dict(link="https://ci.example.org/runs/123"), SKILLS, 10, 2)
            self.assertEqual(info["status"], "external")
            run.assert_not_called()
            info = gh.analyze_check(dict(link="https://github.com/org/repo/actions/runs/40/job/41"),
                                    SKILLS, 10, 2)
            self.assertEqual(info["logSnippet"], "FAIL: bad result")
            commands = [call.args[0] for call in run.call_args_list]
            self.assertTrue(all(c[c.index("-R")+1] == "org/repo" for c in commands))
            self.assertEqual(commands[-1][-3:], ["--job", "41", "--log"])
