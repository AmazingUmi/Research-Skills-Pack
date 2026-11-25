#!/usr/bin/env python3
"""Read-only strict resume check. Resolve a recorded boundary and its stage/branch."""

import argparse
import json
import re
from pathlib import Path

import yaml

# Endpoint checks only. The state machine defines the evidence and author
# decision required for each edge, including the two integrity correction loops.
NEXT_STAGES = {
    "1": {"2"},
    "2": {"2.5"},
    "2.5": {"2", "3", "4", "3'", "4.5"},
    "3": {"2", "4", "4.5"},
    "4": {"3'"},
    "3'": {"4'", "4.5"},
    "4'": {"4.5"},
    "4.5": {"5"},
    "5": {"6"},
    "6": set(),
}
NAMES = {
    "research": "1", "write": "2", "integrity": "2.5", "review": "3",
    "revise": "4", "re-review": "3'", "re-revise": "4'", "final integrity": "4.5",
    "finalize": "5", "process summary": "6", "3p": "3'", "4p": "4'",
}


def stage_id(value):
    key = str(value).lower().strip().removeprefix("stage ").replace("′", "'").replace("_", " ")
    key = NAMES.get(key, key)
    if key not in NEXT_STAGES:
        raise ValueError(f"Unknown pipeline stage: {value!r}")
    return key


def resolve(passport, boundary_hash, *, stage=None, choice=None, mode=None):
    if not re.fullmatch(r"[a-f0-9]{12}", boundary_hash):
        raise ValueError("Expected a 12-hex boundary hash")
    ledger = passport.get("reset_boundary", [])
    entries = [row for row in ledger if row.get("kind") == "boundary" and row.get("hash") == boundary_hash]
    if len(entries) != 1:
        raise ValueError("Missing or ambiguous boundary")
    if any(row.get("kind") == "resume" and row.get("consumes_hash") == boundary_hash for row in ledger):
        raise ValueError("Boundary was already consumed")

    boundary = entries[0]
    source = stage_id(boundary["stage"])
    target = boundary["next"]
    pending = boundary.get("pending_decision")
    branch_mode = None
    if pending is not None:
        options = [option for option in pending["options"] if option["value"] == choice]
        if len(options) != 1:
            raise ValueError("Resolve the author's pending decision first")
        target = options[0]["next_stage"]
        branch_mode = options[0].get("next_mode")
    elif choice is not None:
        raise ValueError("This boundary has no pending branch")
    if target is None:
        if stage is not None or mode is not None:
            raise ValueError("A terminal boundary or branch has no downstream stage or mode")
        if pending is None and source not in {"5", "6"}:
            raise ValueError("Missing destination for this resume")
        return {"next_stage": None, "next_mode": None}

    target = stage_id(target)
    if source == "6" or (target != source and target not in NEXT_STAGES[source]):
        raise ValueError(f"Illegal transition {source} -> {target}")
    if stage is not None:
        requested = stage_id(stage)
        if requested != target and (pending is not None or requested != source):
            raise ValueError(f"Requested stage {requested} conflicts with the resolved destination {target}")
        target = requested
    if target in {"4", "4'"}:
        branch_mode = "revise" if branch_mode == "revision" else branch_mode
        mode = "revise" if mode == "revision" else mode
    if mode is not None and branch_mode is not None and mode != branch_mode:
        raise ValueError("Requested mode conflicts with the chosen branch")
    return {"next_stage": target, "next_mode": mode or branch_mode}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("passport", type=Path)
    parser.add_argument("boundary_hash")
    parser.add_argument("--stage")
    parser.add_argument("--choice", help="Branch actually chosen by the author")
    parser.add_argument("--mode")
    args = parser.parse_args()
    try:
        passport = yaml.safe_load(args.passport.read_text(encoding="utf-8"))
        if not isinstance(passport, dict):
            raise ValueError("Passport must be a mapping")
        result = resolve(passport, args.boundary_hash, stage=args.stage, choice=args.choice, mode=args.mode)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError, yaml.YAMLError) as exc:
        parser.exit(1, f"Resume refused: {exc}\n")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
