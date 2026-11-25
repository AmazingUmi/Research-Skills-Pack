"""Check the identity and structure of figure handoffs before assessing their claims."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import re
from pathlib import Path

import yaml


REQUIRED = {"artifact_id", "source_data", "transformation", "caption_claim",
            "supported_manuscript_claims", "limitations"}


def known_text(value):
    return isinstance(value, str) and value.strip().casefold() not in {
        "", "unknown", "tbd", "n/a", "none", "未知", "待核", "待确认", "待確認", "待补", "待補"
    }


def invalid_fields(row, claim_bearing):
    source = row["source_data"]
    if not (known_text(source) or isinstance(source, dict)
            and any(known_text(source.get(k)) for k in ("dataset_id", "file"))):
        yield "source_data must identify the source file or dataset"
    transform = row["transformation"]
    if isinstance(transform, dict):
        if not all(known_text(transform.get(k)) for k in ("script", "hash")):
            yield "transformation must identify the script and hash"
    elif not known_text(transform) or transform.strip().casefold() in {"computed manually", "see paper"}:
        yield "transformation needs a script and hash or a specific manual derivation"
    if not known_text(row["caption_claim"]):
        yield "caption_claim needs the caption's claim text"
    claims = row["supported_manuscript_claims"]
    if not isinstance(claims, list) or (claim_bearing and not claims):
        yield "supported_manuscript_claims must list the substantive manuscript claims"
    else:
        for claim in claims:
            if not isinstance(claim, dict) or not known_text(claim.get("claim")) or re.fullmatch(r"C-\d+", claim["claim"].strip()):
                yield "each supported claim needs its text"
            elif "locator" in claim and not known_text(claim["locator"]):
                yield "a supplied claim locator must identify a manuscript location"
    limitations = row["limitations"]
    if not isinstance(limitations, list) or any(not known_text(item) for item in limitations):
        yield "limitations must be a list of stated limitations or an empty list"


def check_trace(package: dict | None, figures=(), tables=()) -> dict:
    errors, notes, entries = [], [], {}
    if package is not None:
        if not isinstance(package, dict) or not isinstance(package.get("figure_table_trace"), list):
            errors.append("figure package lacks a figure_table_trace array")
        else:
            for row in package["figure_table_trace"]:
                if not isinstance(row, dict) or not known_text(row.get("artifact_id")):
                    errors.append("trace row lacks an artifact ID")
                    continue
                key = row["artifact_id"]
                if key in entries:
                    errors.append(f"{key}: duplicate figure trace")
                entries[key] = row
                missing = REQUIRED.difference(row)
                if missing:
                    errors.append(f"{key}: missing {', '.join(sorted(missing))}")
                    continue
                problems = list(invalid_fields(row, key in figures or key in tables))
                errors.extend(f"{key}: {problem}" for problem in problems)
                if not problems and not row["limitations"]:
                    notes.append(f"{key}: limitations list is empty")
    for key in figures:
        if key not in entries:
            (notes if package is None else errors).append(f"{key}: trace unavailable")
    notes.extend(f"{key}: table trace unavailable" for key in tables if key not in entries)
    return {"errors": errors, "notes": notes, "artifact_ids": list(entries)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, help="unchanged Figure Package in YAML or JSON; omit for a legacy figure")
    parser.add_argument("--figure", action="append", default=[], help="claim-bearing figure ID, repeatable")
    parser.add_argument("--table", action="append", default=[], help="standalone table ID, repeatable")
    parser.add_argument("--expected-sha256", help="package digest recorded at the earlier gate")
    args = parser.parse_args(argv)
    try:
        raw = args.package.read_bytes() if args.package else None
        digest = sha256(raw).hexdigest() if raw is not None else None
        if args.expected_sha256 and args.expected_sha256 != digest:
            parser.exit(1, "figure package differs from the recorded artifact\n")
        package = yaml.safe_load(raw) if raw is not None else None
        if raw is not None and package is None:
            parser.exit(1, "empty Figure Package\n")
        result = check_trace(package, args.figure, args.table)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        parser.exit(2, f"Cannot read figure package: {exc}\n")
    result["sha256"] = digest
    print(json.dumps(result, ensure_ascii=False))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
