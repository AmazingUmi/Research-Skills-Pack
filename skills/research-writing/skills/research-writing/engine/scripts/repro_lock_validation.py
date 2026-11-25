#!/usr/bin/env python3
"""Canonical repro_lock field set — single source of truth (#260).

Validate the passport-level reproducibility lock or import validate_block for an
individual lock. The entry-level JSON Schema mirrors these value constraints.
"""
from __future__ import annotations

from typing import Any

SUPPORTED_SCHEMA_VERSIONS = {"1.0"}
SUPPORTED_HASH_TIMINGS = {"skill-load"}

REQUIRED_FIELDS = {
    "schema_version",
    "stochasticity_declaration",
    "ars_version",
    "model",
    "prompts",
    "materials",
    "external_protocols",
    "cross_model",
}

REQUIRED_MODEL = {"family", "id", "weight_stable"}
REQUIRED_PROMPTS = {"hash_timing", "skill_md_hash", "agents_bundle_hash"}
REQUIRED_MATERIALS = {"list_hash", "count"}
REQUIRED_EXTERNAL = {"s2_api_protocol_version", "s2_snapshot_available"}
REQUIRED_CROSSMODEL = {"enabled", "secondary_model_id"}

# (sub-block name, required field set) pairs, iteration-ordered for stable output.
_SUBBLOCKS = (
    ("model", REQUIRED_MODEL),
    ("prompts", REQUIRED_PROMPTS),
    ("materials", REQUIRED_MATERIALS),
    ("external_protocols", REQUIRED_EXTERNAL),
    ("cross_model", REQUIRED_CROSSMODEL),
)


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value != ""


def _boolean(value: Any) -> bool:
    return isinstance(value, bool)


def _string_or_null(value: Any) -> bool:
    return value is None or isinstance(value, str)


def _whole_number(value: Any) -> bool:
    # JSON Schema counts 3.0 as an integer, and bool is an int subclass in Python.
    if isinstance(value, bool):
        return False
    is_whole = isinstance(value, int) or (isinstance(value, float) and value.is_integer())
    return is_whole and value >= 0


def _one_of(allowed: set[str]) -> tuple[Any, str]:
    return (lambda value: isinstance(value, str) and value in allowed), f"one of {sorted(allowed)}"


# Value rules for each required field: (rule, what the error message asks for).
# These mirror the nested schema in experiment_provenance_entry.schema.json.
_NON_EMPTY = (_non_empty_string, "a non-empty string")
_BOOLEAN = (_boolean, "true or false")
_TOP_LEVEL_RULES = {
    "schema_version": _one_of(SUPPORTED_SCHEMA_VERSIONS),
    "stochasticity_declaration": _NON_EMPTY,
    "ars_version": _NON_EMPTY,
}
_SUBBLOCK_RULES = {
    "model": {"family": _NON_EMPTY, "id": _NON_EMPTY, "weight_stable": _BOOLEAN},
    "prompts": {
        "hash_timing": _one_of(SUPPORTED_HASH_TIMINGS),
        "skill_md_hash": _NON_EMPTY,
        "agents_bundle_hash": _NON_EMPTY,
    },
    "materials": {"list_hash": _NON_EMPTY, "count": (_whole_number, "a whole number of 0 or more")},
    "external_protocols": {"s2_api_protocol_version": _NON_EMPTY, "s2_snapshot_available": _BOOLEAN},
    "cross_model": {"enabled": _BOOLEAN, "secondary_model_id": (_string_or_null, "a string or null")},
}


def validate_block(lock: dict[str, Any]) -> list[str]:
    """Validate a populated repro_lock mapping; return a list of error strings.

    Checks required keys and their values (#1050). Extra keys are allowed here,
    which is the one difference from the nested entry schema.
    Caller handles the missing-key / null-opt-out / non-mapping top-level cases
    (those need passport-level context the block alone lacks).
    """
    errors: list[str] = []

    missing = REQUIRED_FIELDS - set(lock.keys())
    for m in sorted(missing):
        errors.append(f"repro_lock: missing required field '{m}'")

    for name, (rule, wanted) in _TOP_LEVEL_RULES.items():
        if name in lock and not rule(lock[name]):
            errors.append(f"repro_lock.{name} = {lock[name]!r}, must be {wanted}")

    for name, required in _SUBBLOCKS:
        if name not in lock:
            continue  # missing top-level already reported
        sub = lock[name]
        if not isinstance(sub, dict):
            errors.append(f"repro_lock.{name} must be a mapping")
            continue
        for m in sorted(required - set(sub.keys())):
            errors.append(f"repro_lock.{name}: missing required field '{m}'")
        for field, (rule, wanted) in _SUBBLOCK_RULES[name].items():
            if field in sub and not rule(sub[field]):
                errors.append(f"repro_lock.{name}.{field} = {sub[field]!r}, must be {wanted}")

    return errors

def main() -> int:
    import argparse
    from pathlib import Path
    import sys
    import yaml

    parser = argparse.ArgumentParser(description="Validate a passport's top-level reproducibility lock.")
    parser.add_argument("passport", type=Path)
    args = parser.parse_args()
    try:
        passport = yaml.safe_load(args.passport.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        parser.exit(2, f"Cannot read passport: {exc}\n")
    if not isinstance(passport, dict) or "repro_lock" not in passport:
        parser.exit(1, "Missing repro_lock\n")
    lock = passport["repro_lock"]
    if lock is None:
        print("repro_lock explicitly opted out", file=sys.stderr)
        return 0
    errors = validate_block(lock) if isinstance(lock, dict) else ["repro_lock must be a mapping or null"]
    for error in errors:
        print(error, file=sys.stderr)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
