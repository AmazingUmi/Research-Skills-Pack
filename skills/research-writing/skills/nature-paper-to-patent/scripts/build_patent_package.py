#!/usr/bin/env python3
"""Build the standard split Chinese patent application package."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp

import audit_claims
import validate_patent_draft


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def validate(data: dict) -> None:
    required = ("title", "claims", "specification", "abstract", "figures")
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError(f"Missing required complete-package content: {', '.join(missing)}")
    spec = data["specification"]
    if not spec.get("figure_descriptions"):
        raise ValueError("Specification must contain figure descriptions")
    if "equations" not in spec:
        raise ValueError(
            "Specification must contain an equations array; use an empty array only when "
            "the source contains no core technical formulas"
        )
    source_analysis = data.get("source_analysis", {})
    if source_analysis.get("contains_core_formulas") and not spec.get("equations"):
        raise ValueError(
            "The source is marked as containing core formulas, but specification.equations is empty"
        )
    for equation in spec.get("equations", []):
        if not equation.get("latex"):
            raise ValueError(
                f"Equation {equation.get('number')} must include latex source for native Office Math"
            )
    equation_numbers = [item.get("number") for item in spec.get("equations", [])]
    if equation_numbers and equation_numbers != list(range(1, len(equation_numbers) + 1)):
        raise ValueError(
            f"Equation numbers must be consecutive integers starting at 1: {equation_numbers}"
        )
    abstract_figure_number = data.get("abstract_figure_number")
    if not isinstance(abstract_figure_number, int):
        raise ValueError("abstract_figure_number must be an integer")
    figure = next(
        (
            item
            for item in data["figures"]
            if item.get("number") == abstract_figure_number
        ),
        None,
    )
    if figure is None:
        raise ValueError(
            f"abstract_figure_number {abstract_figure_number} does not reference an existing figure"
        )
    if not figure.get("complete_claim_flow"):
        raise ValueError("The abstract figure must be a complete principal claim flow")
    if source_analysis.get("contains_methodology_figures"):
        methodology = [item for item in data["figures"] if item.get("type") == "methodology"]
        if not methodology:
            raise ValueError(
                "The source is marked as containing methodology figures, but no methodology "
                "figure is included"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="UTF-8 patent draft JSON")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prefix", default="patent")
    args = parser.parse_args()

    data = json.loads(args.draft.read_text(encoding="utf-8"))
    root = Path(__file__).resolve().parent
    args.output_dir.mkdir(parents=True, exist_ok=True)
    validation = validate_patent_draft.validate(data)
    reports = {}
    claims_body = ""
    failed = any(item.level == "ERROR" for item in validation)
    if not failed:
        try:
            validate(data)
        except ValueError as exc:
            validation.append(validate_patent_draft.Finding("ERROR", "PACKAGE_CONTENT", str(exc)))
            failed = True

    validation_name = f"{args.prefix}-草稿验证报告.txt"
    reports[validation_name] = validate_patent_draft.format_report(validation)
    audit_name = f"{args.prefix}-权利要求检查.txt"
    if not failed:
        claims_body = "\n".join(f"{claim['number']}. {claim['text']}" for claim in data["claims"]) + "\n"
        findings = audit_claims.audit(claims_body)
        reports[audit_name] = audit_claims.format_report(findings)
        failed = any(item.level == "ERROR" for item in findings)

    report_dir = args.output_dir
    if failed and any((report_dir / name).exists() for name in reports):
        # A rejected rebuild keeps the previous package and its audit reports together.
        report_dir = Path(mkdtemp(prefix=f"{args.prefix}-failed-", dir=report_dir))
    for name, content in reports.items():
        path = report_dir / name
        path.write_text(content, encoding="utf-8")
        if failed:
            print(path)
    if failed:
        return 1

    docx_script = root / "render_patent_docx.py"
    figure_script = root / "render_flowchart_svg.py"

    figure_dir = args.output_dir / f"{args.prefix}-figures"
    run(
        [
            sys.executable,
            str(figure_script),
            str(args.draft),
            "--output-dir",
            str(figure_dir),
            "--png",
        ]
    )

    outputs = {
        "claims": args.output_dir / f"{args.prefix}-权利要求书.docx",
        "specification": args.output_dir / f"{args.prefix}-说明书.docx",
        "abstract": args.output_dir / f"{args.prefix}-说明书摘要.docx",
        "abstract-figure": args.output_dir / f"{args.prefix}-摘要附图.docx",
        "all": args.output_dir / f"{args.prefix}-完整审阅稿.docx",
    }
    for part, output in outputs.items():
        command = [
            sys.executable,
            str(docx_script),
            str(args.draft),
            "--output",
            str(output),
            "--part",
            part,
        ]
        if part in {"specification", "abstract", "abstract-figure", "all"}:
            command.extend(["--figure-dir", str(figure_dir)])
        run(command)

    claims_text = args.output_dir / f"{args.prefix}-权利要求书.txt"
    claims_text.write_text(claims_body, encoding="utf-8")
    json_copy = args.output_dir / f"{args.prefix}-结构化草稿.json"
    if args.draft.resolve() != json_copy.resolve():
        shutil.copy2(args.draft, json_copy)

    for output in (*outputs.values(), json_copy, report_dir / audit_name, report_dir / validation_name):
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
