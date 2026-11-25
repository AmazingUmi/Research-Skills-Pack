#!/usr/bin/env python3
"""Anchorize a draft: stamp block markers + emit the block manifest.

#89 Item 7 Slice A. Normative source:
`docs/design/2026-06-10-390-diff-patch-revision-mode-spec.md` §3.1.

What this script owns (and the LLM never does): block-ID assignment.
It stamps every unlabeled block with a fresh `<!--block:BNNNN-->` marker
(`max(existing) + 1`, document order, never renumbered) and emits the
block manifest — the ONLY legitimate source for every hash a patch
document carries (`base_draft_hash` + per-op `old_hash`). The writer
copies hashes from the manifest; it never computes them (§3.1: a Bucket A
agent with all Bash denied would hallucinate a hash if asked).

Properties the test suite pins (§8.1):
  - idempotent: a second run is byte-identical and rewrites nothing;
  - content-neutral: output minus marker lines == input bytes;
  - manifest agreement: per-block hashes and `base_draft_hash` equal an
    independent recomputation over the final anchored file.

Manifest sidecar: `<draft>.block-manifest.json` (override with
`--manifest-out`), shape per
`contracts/patch/block_manifest.schema.json`.

Exit codes: 0 = ok; 2 = the parser refused the document (§3.1
malformed-state / unsupported-construct rules — fail closed, fix the
draft and re-run).

Usage:
    python engine/scripts/ars_anchorize_draft.py original.md --output working.md
    python engine/scripts/ars_anchorize_draft.py working.md --manifest-out working-manifest.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__ in (None, ""):  # pragma: no cover - direct CLI invocation
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts._block_parser import (
    BLOCK_ID_FORMAT,
    BlockParseError,
    ParsedDocument,
    atomic_write_bytes,
    base_draft_hash,
    parse_document,
)

_EXCERPT_MAX = 80
MANIFEST_FORMAT_VERSION = "1.0"


def _line_eol(text: str, span_start: int) -> str:
    """EOL style of the line starting at span_start ('\\r\\n' or '\\n')."""
    nl = text.find("\n", span_start)
    if nl == -1:
        return "\n"
    return "\r\n" if nl > span_start and text[nl - 1] == "\r" else "\n"


def _anchorize(text: str) -> tuple[str, int]:
    """Anchorize ``text``; returns (anchored text, newly labeled count)."""
    parsed = parse_document(text)
    next_num = parsed.next_fresh_id_num()
    newly_labeled = 0
    pieces: list[str] = []
    pos = 0
    for block in parsed.blocks:
        start = block.full_start
        pieces.append(text[pos:start])
        if block.block_id is None:
            marker_id = BLOCK_ID_FORMAT.format(next_num)
            next_num += 1
            newly_labeled += 1
            pieces.append(f"<!--block:{marker_id}-->{_line_eol(text, block.span[0])}")
        pieces.append(text[start : block.span[1]])
        pos = block.span[1]
    pieces.append(text[pos:])
    return "".join(pieces), newly_labeled


def anchorize_text(text: str) -> str:
    """Return the anchored document text (pure function; parser may raise)."""
    return _anchorize(text)[0]


def build_manifest(anchored_raw: bytes, parsed: ParsedDocument) -> dict:
    blocks = []
    for block in parsed.blocks:
        excerpt = block.first_line
        if len(excerpt) > _EXCERPT_MAX:
            excerpt = excerpt[: _EXCERPT_MAX - 1] + "…"
        blocks.append(
            {
                "block_id": block.block_id,
                "old_hash": block.norm_hash,
                "first_line_excerpt": excerpt,
            }
        )
    return {
        "manifest_format_version": MANIFEST_FORMAT_VERSION,
        "base_draft_hash": base_draft_hash(anchored_raw),
        "blocks": blocks,
    }


def anchorize_file(draft_path: Path, manifest_path: Path, output_path: Path | None = None) -> dict:
    """Anchorize a private copy, or refresh a working draft in place for legacy callers."""
    working = output_path or draft_path
    if manifest_path.resolve() in (working.resolve(), draft_path.resolve()):
        raise ValueError("the manifest needs a distinct output path")
    if output_path is not None and working.resolve() == draft_path.resolve():
        raise ValueError("the working copy must differ from the original")
    raw = draft_path.read_bytes()
    text = raw.decode("utf-8")

    anchored, newly_labeled = _anchorize(text)
    changed = anchored != text
    anchored_raw = anchored.encode("utf-8")

    # Defensive re-parse of what is now on disk: every block labeled,
    # grammar intact. A failure here is a bug, not a user error.
    reparsed = parse_document(anchored)
    unlabeled = [b for b in reparsed.blocks if b.block_id is None]
    if unlabeled:  # pragma: no cover - self-check
        raise AssertionError("anchorize self-check failed: unlabeled block survived")

    manifest = build_manifest(anchored_raw, reparsed)
    if output_path is not None:
        manifest["original_sha256"] = hashlib.sha256(raw).hexdigest()
        manifest["working_sha256"] = hashlib.sha256(anchored_raw).hexdigest()
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if output_path is not None:
        # Reserve a fresh working path. A failed manifest write permits a clean retry.
        target = working.open("xb")
        try:
            with target:
                target.write(anchored_raw)
            atomic_write_bytes(manifest_path, manifest_bytes)
        except BaseException:
            working.unlink(missing_ok=True)
            raise
    else:
        if changed:
            atomic_write_bytes(working, anchored_raw)
        atomic_write_bytes(manifest_path, manifest_bytes)

    return {
        "changed": changed,
        "blocks_total": len(reparsed.blocks),
        "blocks_newly_labeled": newly_labeled,
        "manifest_path": str(manifest_path),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("draft", type=Path, help="source Markdown; without --output only use a private working draft (in place)")
    parser.add_argument(
        "--manifest-out",
        type=Path,
        default=None,
        help="block manifest output path (default: <draft>.block-manifest.json)",
    )
    parser.add_argument("--output", type=Path, help="create a new anchored working copy, preserving the input")
    args = parser.parse_args(argv)

    manifest_path = args.manifest_out or Path(str(args.output or args.draft) + ".block-manifest.json")
    try:
        summary = anchorize_file(args.draft, manifest_path, args.output)
    except (OSError, ValueError) as exc:
        print(f"Cannot prepare anchored draft: {exc}", file=sys.stderr)
        return 2
    except BlockParseError as exc:
        print(f"REJECTED [{exc.kind}]: {exc}", file=sys.stderr)
        return 2

    print(
        "anchorize ok: {total} blocks ({new} newly labeled, {state}) -> manifest {mpath}".format(
            total=summary["blocks_total"],
            new=summary["blocks_newly_labeled"],
            state="file updated" if summary["changed"] else "already anchored",
            mpath=summary["manifest_path"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
