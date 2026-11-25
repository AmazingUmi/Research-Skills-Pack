#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path

from deck_run_state import load_deck, load_jobs, now_iso, resolve_inside, run_dir_from_target, save_deck, save_jobs, set_run_status, write_json


SCRIPT_DIR = Path(__file__).resolve().parent


def run(command):
    print("+ " + " ".join(str(part) for part in command), flush=True)
    subprocess.run([str(part) for part in command], check=True)


def final_output_path(run_dir, deck):
    try:
        return resolve_inside(run_dir, deck.get("output", "final/deck_edited.pptx"))
    except ValueError as exc:
        raise SystemExit(f"Final output must stay inside run directory: {deck.get('output')}") from exc


def assert_pages_ready(run_dir, jobs):
    problems = []
    for page in jobs.get("pages", []):
        if page.get("status") not in {"recorded", "accepted"}:
            problems.append(f"{page['page_id']} status={page.get('status')}")
            continue
        result = page.get("result") or {}
        if result.get("validation_passed") is not True:
            problems.append(f"{page['page_id']} validation_passed={result.get('validation_passed')}")
    if problems:
        raise SystemExit("Pages are not ready for finalize:\n" + "\n".join(problems))


def record_final_status(run_dir, status):
    deck = load_deck(run_dir)
    jobs = load_jobs(run_dir)
    out = final_output_path(run_dir, deck)
    accepted = status == "complete"
    now = now_iso()
    for page in jobs.get("pages", []):
        if page.get("status") in {"recorded", "accepted"}:
            page["status"] = "accepted" if accepted else "recorded"
            page["accepted"] = accepted
            if accepted:
                page["accepted_at"] = now
            else:
                page.pop("accepted_at", None)
    jobs.update(run_status=status, updated_at=now)
    save_jobs(run_dir, jobs)
    summary = {"schema_version": 1, "run_id": deck.get("run_id"), "status": status,
               "page_count": len(jobs.get("pages", [])), "output": str(out),
               "validation": str(out.parent / "validation.json")}
    if accepted:
        deck["completed_at"] = summary["completed_at"] = now
    else:
        deck.pop("completed_at", None)
    save_deck(run_dir, deck)
    write_json(out.parent / "run_summary.json", summary)
    set_run_status(run_dir, status)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Build and validate the final editable PPTX from recorded pages.")
    parser.add_argument("run", help="Run directory or deck_manifest.json")
    args = parser.parse_args()

    run_dir = run_dir_from_target(args.run)
    deck = load_deck(run_dir)
    jobs = load_jobs(run_dir)
    assert_pages_ready(run_dir, jobs)

    out = final_output_path(run_dir, deck)
    out.parent.mkdir(parents=True, exist_ok=True)
    record_final_status(run_dir, "building")
    run([sys.executable, SCRIPT_DIR / "build_pptx_from_manifest.py", "--deck-manifest", run_dir / "deck_manifest.json", "--out", out])
    set_run_status(run_dir, "deck_built", "final pptx built")

    postprocess = SCRIPT_DIR.parents[2] / "scripts" / "postprocess_manifest_arrows.py"
    run([sys.executable, postprocess, out, "--run", run_dir, "--report", out.parent / "image2ppt_arrow_postprocess.json"])
    validation = out.parent / "validation.json"
    run([sys.executable, SCRIPT_DIR / "validate_pptx.py", out, "--deck-manifest", run_dir / "deck_manifest.json", "--report", validation])
    set_run_status(run_dir, "deck_validated", "final pptx validation passed")

    summary = record_final_status(run_dir, "awaiting_final_qa")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
