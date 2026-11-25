# Revision Patch Protocol

**Toolchain:** Slice A — `@/engine/scripts/_block_parser.py`, `@/engine/scripts/ars_anchorize_draft.py`, `@/engine/scripts/ars_apply_revision_patch.py`, schemas under `@/engine/contracts/patch/`.
**Audience:** the pipeline orchestrator (orchestrated runs) and any user running revision rounds phase-by-phase across sessions (manual runs). The commands below are the same in both modes — orchestrated runs wrap them, manual runs type them.

**What this buys, stated honestly:** under patch apply, a block no operation names cannot be silently distorted, because no generation pass runs over it — that is a property of the apply script, not of the model. It does NOT make the edits themselves better, and structural rewrites are not patch-protected (they escalate, §3.6). Every summary of this feature must survive that sentence.

---

## Artifacts and naming

| Artifact | Produced by | Convention |
|---|---|---|
| Anchored draft | `ars_anchorize_draft.py` (on the private working copy) | every block carries `<!--block:BNNNN-->`; IDs never renumbered |
| Block manifest | same run, sidecar | `<draft>.block-manifest.json` — `base_draft_hash` + `{block_id, old_hash, first_line_excerpt}` per block; the ONLY legitimate hash source for a patch |
| Immutable roadmap | editorial synthesizer / confirmed standalone adapter | `revision-roadmap/1.0`, exact draft + block-manifest bindings |
| Claim surface manifest | deterministic registry builder | `claim-surface-manifest/1.0`, exact Claim Intent + UTF-8 surface bindings |
| Author adjudication | `@/engine/scripts/revision_roadmap.py build-adjudication` from explicit choices | `author-adjudication/1.0`; complete choices and exact authority only |
| Integrity correction list | issuing integrity gate | `integrity-correction-list/1.0`; correction descriptions and exact `proposed_targets` only — a proposal, never write authority |
| Integrity author input | author, from the exact proposed patch shown in-session | `integrity-correction-authorization-input/1.0`; explicit event receipts, one decision per issue, authorized targets/operations, and the author-approved `revision_patch_sha256` |
| Integrity authorization | `@/engine/scripts/revision_roadmap.py build-integrity-authorization` | `integrity-correction-authorization/1.0`; a deterministic sidecar that copies the author-approved patch hash and adds exact base/list/round bindings |
| Patch document | `draft_writer_agent` (revision invocation) | current `patch_format_version: 1.1`, schema `@/engine/contracts/patch/revision_patch.schema.json` |
| Revised draft | `ars_apply_revision_patch.py` | `--output` MUST be a new file (versioned artifact; the base is never modified) |
| Apply report | same run, sidecar | `<output>.apply-report.json`, format 1.3 — exact patch/pre/post bindings, replayed authorization witness, per-op claim/collateral declarations, structural and byte-preservation facts |
| Revision-Evidence Bundle | orchestrator | `revision-evidence-bundle/1.0`, continuous chain from exact integrity PASS through every write/no-op round to final draft |

The apply report shares the revised draft's lifecycle: it is a **required input to re-review and the final integrity gate** — re-reviewers read it to see exactly which blocks changed (`ops_applied[]`, `fresh_block_ids`, `pure_move_pairs`) and which are machine-guaranteed untouched. Consumers verify report-to-artifact freshness by the §11 ORDERED-CHAIN rule (which supersedes the old single-report `output_draft_hash`-vs-handed-draft check — that rule is wrong for multi-round sequences and misses base-link breaks): with reports ordered as applied, the FIRST report's `base_draft_hash` must equal the anchored pre-revision working draft's hash prefix (the strict manifest’s `original_manuscript`), each subsequent report's `base_draft_hash` its predecessor's `output_draft_hash`, and the LAST report's `output_draft_hash` — and only the last's — the handed revised draft's hash prefix. Any broken link means some patch ran against a different text than the chain claims (a rewritten-after-apply draft breaks the last link; a wrong base skews every diff-supported judgment) — treat the affected report(s) as stale and re-derive provenance before relying on them (the same report-to-artifact freshness class as the submission verifier's `STALE-REPORT` guard in `@/engine/scripts/verify_submission_package.py`; at the re-review stage the chain is checker-enforced as `apply_chain_witness`, `manifest_hash_mismatch` on breakage).

Keep the source SHA-256 from before anchoring alongside the full working SHA-256. The first integrity receipt, `original_manuscript`, roadmap and block manifest must bind the exact anchored working bytes. For an unanchored legacy manuscript, verify that working copy before starting the patch chain. A receipt or surface map for the unanchored source cannot be reused against changed bytes. Subsequent rounds take the preceding output as their base.

## Manual command sequence (one revision round)

```bash
# 1. At round entry, use a fresh working path and the previous round’s output
#    as input (the frozen source on round one). Keep both paths for replay.
python @/engine/scripts/ars_anchorize_draft.py original.md --output draft.md

# 1a. Acronym check: read-only, on the anchored draft. A report with
#     findings goes to the writer with the round's authority artifacts
#     (writing_quality_check.md § F); an integrity-correction round skips it.
python @/engine/scripts/check_acronyms.py --input draft.md --lang en

# 2. Validate the immutable roadmap, registered claim surfaces, and explicit
#    author sidecar. The writer receives all exact artifacts/bindings and emits
#    phase6_*/revision_patch_round1.json (current format 1.1, never a full draft).
python @/engine/scripts/revision_roadmap.py validate-adjudication \
    roadmap.json author-adjudication.json \
    --base draft.md \
    --block-manifest draft.md.block-manifest.json \
    --claim-surface claim-surface-manifest.json \
    --artifact-root revision-authority/

# 3. Apply — two-phase fail-closed; output must be a NEW file.
python @/engine/scripts/ars_apply_revision_patch.py draft.md \
    phase6_revision/revision_patch_round1.json \
    --block-manifest draft.md.block-manifest.json \
    --roadmap roadmap.json \
    --author-adjudication author-adjudication.json \
    --claim-surface-manifest claim-surface-manifest.json \
    --artifact-root revision-authority/ \
    --output draft.rev1.md

# 4. Run your normal post-revision steps (finalizer / citation checks, and
#    the acronym check, whose report goes to the user) on draft.rev1.md,
#    then re-review with draft.rev1.md.apply-report.json attached.
```

Exit codes: `0` applied · `2` Phase 1 rejection (structured failure report on stdout; base byte-untouched) · `3` structural refusal (see escalation) · `4` post-write self-check bug.

**On exit 2 (stale hash / unknown target / authorization/schema failure):** feed the failure report back to the writer for ONE re-emission of the whole patch against the same exact authority artifacts, unless the failure shows that author scope must change. On a second failure, stop: re-anchorize and rebuild the bound authority chain, collect a new explicit author adjudication, narrow the round, or abort. Never hand-edit a patch to force it through — a mismatch means the writer and gate did not share the same exact evidence.

**On exit 3 (structural flags):** the patch touches structure — heading rewrites/deletes, net section-count change, or `touched_ratio` strictly above **0.6** (the ship decision; `insert_after` merely *anchored* on a heading is exempt — inserting body text under a section heading is routine, not structural). Read the flags in the refusal output, then either narrow the patch, or — if the structural change is intended — re-run with the acknowledgment recorded:

```bash
python @/engine/scripts/ars_apply_revision_patch.py draft.md patch.json \
    --block-manifest draft.md.block-manifest.json \
    --roadmap roadmap.json \
    --author-adjudication author-adjudication.json \
    --claim-surface-manifest claim-surface-manifest.json \
    --artifact-root revision-authority/ \
    --output draft.rev1.md --acknowledge-structural
```

`--acknowledge-structural` is a deliberate user decision, never a default; the flags stay recorded in the apply report either way. `--touched-ratio-threshold 1.0` disables the ratio trigger (the comparator is strict `>`); overriding 0.6 in pipeline runs requires a recorded user decision.

### Integrity-correction variant (one revision round)

An integrity FAIL and its `integrity-correction-list/1.0` identify work to
propose; neither the gate verdict nor the list authorizes a write. The list
contains only `proposed_targets`. The writer first emits an exact patch 1.1
with `authorization_context: integrity_correction`, the supplied exact
`issue_list_sha256`, correction IDs in `roadmap_item_ids`, and empty
`claim_strength_changes[]` / `collateral_authorization_ids[]`. It does not
create or infer author approval.

Present those exact patch bytes and their deterministically computed SHA-256
to the author. Collect `integrity-correction-authorization-input/1.0` with the
same `revision_patch_sha256`, one explicit `authorize` or
`stop_without_write` decision per issue, and the exact authorized target and
operation subset for every `authorize` decision. A `stop_without_write`
decision grants no scope. If the author does not approve the exact patch, stop
without writing; any changed proposal is new bytes and requires a new explicit
input.

The deterministic builder validates the input against the exact patch and
copies the author-approved digest into a hash-bound sidecar:

```bash
python @/engine/scripts/revision_roadmap.py build-integrity-authorization \
    integrity-correction-list.json \
    --base draft.md \
    --patch phase6_revision/integrity_patch_round1.json \
    --author-choices integrity-author-input.json \
    --output integrity-authorization.json
```

Only then may apply run, and both integrity artifacts are mandatory:

```bash
python @/engine/scripts/ars_apply_revision_patch.py draft.md \
    phase6_revision/integrity_patch_round1.json \
    --block-manifest draft.md.block-manifest.json \
    --integrity-issue-list integrity-correction-list.json \
    --integrity-authorization integrity-authorization.json \
    --output draft.integrity-rev1.md
```

The apply gate replays the exact patch hash, list/base/round bindings, author
events and decisions, and target/operation subsets before structural analysis
or output creation. An op citing `stop_without_write`, an op outside the exact
authorized subset, or even a one-byte change to the patch rejects the whole
write. Review-roadmap authority arguments are forbidden on this branch.

**Structural scope escalation:** current rounds remain patch-based. If the
authorized scopes cannot express the intended change, stop and collect a new
explicit author sidecar with exact expanded targets, or narrow the edit.
Historical full re-emission remains a visibly separate legacy workflow; it
cannot emit a current 1.3 authorization PASS witness or appear as a current
Revision-Evidence Bundle round.

## Current authorization rules

- The current CLI rejects patch 1.0. Archived 1.0 schema/runtime live only
  under `@/engine/contracts/patch/legacy/v1_0/` and `scripts/legacy/`.
- Every review op cites only `will_address` items and stays inside their exact
  authorized block/operation subsets.
- Declined items authorize neither work nor claim movement. An overlapping
  target requires an exact, single-use collateral authorization for every
  declined item on that target.
- Every registered claim surface remains exact or uses one exact single-use
  author-approved replacement (manifest, claim, surface, block, hashes, text,
  rungs, direction). `will_address` alone is not claim authority.
- The report always discloses
  `unregistered_claim_drift_review_required: true`; unregistered semantic
  movement remains an E6 review surface.
- An all-declined round is a `review_noop`: no patch/report and byte-identical
  pre/post drafts.
- An integrity correction list and an integrity-gate result are proposal
  evidence only. The exact writer-emitted patch must be separately approved
  through explicit author input binding its `revision_patch_sha256` and exact
  targets/operations.
- Integrity apply requires both `--integrity-issue-list` and
  `--integrity-authorization`. `stop_without_write` grants no operation, and a
  substituted patch invalidates the hash-bound sidecar before any write.

Validate the accumulated bundle before re-review/final integrity:

```bash
python @/engine/scripts/revision_roadmap.py validate-bundle \
    revision-evidence-bundle.json --root revision-authority/
```

## Marker lifecycle (one rule for all marker kinds)

`<!--block:-->` markers live in **working drafts only**, exactly like `<!--ref:-->` / `<!--anchor:-->`. Two authoritative rules govern them — this doc indexes them rather than re-owning the wording, so the rule cannot drift out of sync with the surfaces the lint guards:

- **Word counts exclude markers** — strip every `<!--...-->` before `len(body.split())`. Authoritative: `@/references/word_count_conventions.md` § HTML-comment markers.
- **Phase 7 strips markers from converted final outputs**, after the marker-dependent gates run on the working draft; working drafts and `phase6_*/` artifacts keep theirs (the anchor layer the next round's manifest needs). Authoritative: `formatter_agent.md` § this skill Marker Stripping.
