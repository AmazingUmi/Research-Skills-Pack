# Pipeline State Machine v2.0 — Complete Definition

This document defines all legal states, transition conditions, transition actions, and exception handling for the orchestrate role v2.0.

---

## State Definitions

### Stage States

| State | Description |
|-------|------------|
| `pending` | Not yet started, waiting for prerequisite stage to complete |
| `in_progress` | Currently executing |
| `completed` | Completed, deliverables recorded |
| `skipped` | User chose to skip (only for non-mandatory stages) |
| `blocked` | Preconditions not met (e.g., integrity check FAIL) |

### Pipeline Global States

| State | Description |
|-------|------------|
| `initializing` | Detecting entry point and materials |
| `running` | Pipeline executing (at least one stage is in_progress) |
| `awaiting_confirmation` | Stage complete, waiting for user to confirm checkpoint |
| `paused` | User paused, can resume at any time |
| `completed` | All required stages complete, final paper produced |
| `aborted` | User abandoned (e.g., chose to abandon after Reject) |

---

## State Transition Diagram (ASCII)

```
New full run
  Research needed → 1 Research → 2 Write → 2.5 Integrity
  Materials ready → 2 Write → 2.5 Integrity
  Manuscript ready → 2.5 Integrity

After 2.5 and its checkpoint, route to the confirmed target:
  First review → 3 Review
  Review feedback available → 4 Revise
  Revisions ready for review → 3' Re-review
  Formatting and submission only → 4.5 Final integrity

3 Review: Accept → 4.5 | Minor or Major → 4 | Reject → 2 or end
4 Revise → 3' Re-review: Accept or Minor → 4.5 | Major → 4' → 4.5
4.5 Final integrity → mandatory finalization checkpoint → 5 Finalize
5 Finalize → 6 Process summary → completion, or decline 6 → completion

Integrity failure at 2.5 or 4.5 → correction and re-verification at that gate
Validated resume → recorded stage and any pending checkpoint of the same run
```

---

## Legal State Transitions

Use [the stage-to-role table](../ROLE.md#2-阶段与角色调用) for role and mode dispatch. Select the integrity procedure for Stages 2.5 and 4.5 via [the role's integrity section](../ROLE.md#4-完整性核查阶段-25-与-45). Default runs use the [evidence-matrix procedure](../agents/default_integrity_review.md). Material Passport and replay requirements apply when running the strict procedure.

### Normal Flow Transitions

| From | To | Precondition | Action |
|------|----|-------------|--------|
| INIT | Stage 1 | User confirms starting from Stage 1 | Dispatch `outline` and `literature` as needed for the research tasks |
| INIT | Stage 2 | User has research materials and confirms Stage 2 entry | Give the materials to `outline`, then route the selected literature, figures and draft tasks |
| INIT | Stage 2.5 | User brings a complete manuscript into a new full run | Confirm target stage and run the integrity procedure on that version. Use any older report as context |
| Stage 1 | **checkpoint** | Stage 1 completed | Wait for user confirmation |
| checkpoint | Stage 2 | User confirms | Give the available research question, methodology and sources to `outline` to start assembly |
| Stage 2 | **checkpoint** | Stage 2 completed, Paper Draft produced | Wait for user confirmation |
| checkpoint | Stage 2.5 | User confirms | Pass Paper Draft to the selected integrity procedure |
| Stage 2.5 | **checkpoint** | PASS, or recorded Integrity Check FAIL Loop resolution (§ below) | Wait for user confirmation |
| Stage 2.5 | Stage 2.5 (retry) | FAIL | Fix issues, re-verify (max 3 rounds) |
| checkpoint (after 2.5) | Stage 3 | User confirms first review | Pass the checked draft and recorded findings to `review panel` |
| checkpoint (after 2.5) | Stage 4 | User confirms revision and supplies review feedback | Pass the checked draft and feedback to the review role |
| checkpoint (after 2.5) | Stage 3' | User confirms re-review of an existing revision and the selected mode's inputs are available | Pass the checked revision and prior review materials to the applicable re-review branch |
| checkpoint (after 2.5) | Stage 4.5 | User confirms formatting and submission only | Pass the checked final candidate to final integrity. Enter Stage 5 through its mandatory checkpoint |
| Stage 3 | **checkpoint** | Decision produced | Wait for user confirmation (MANDATORY — review decision) |
| checkpoint | Stage 4 | Decision = Minor/Major, user confirms | Pass Revision Roadmap |
| checkpoint | Stage 4.5 | Decision = Accept, user confirms | Skip revision, go directly to final verification |
| Stage 4 | **checkpoint** | Stage 4 completed | Wait for user confirmation |
| checkpoint (after 4) | Stage 3' | User confirms | Dispatch `review`. Simulated review uses `review re-review`, with [a replay-bound handoff](../strict/pipeline_orchestrator_agent.md#stage-3-re-review-contract-dispatch) in strict mode. Real feedback uses [external self-verification](external_review_protocol.md#step-4-self-verification-completeness-check) against the comments, drafts and response |
| Stage 3' | **checkpoint** | Decision produced | Wait for user confirmation (MANDATORY — review decision) |
| Stage 3' (external) | **checkpoint** | Response and draft consistency check completed | Present discrepancies and wait for user confirmation before final integrity |
| checkpoint (external 3') | Stage 4.5 | User confirms after reviewing the reconciliation | Pass the checked draft, response and unresolved findings |
| checkpoint | Stage 4.5 | Decision = Accept/Minor, user confirms | Pass final draft to final verification |
| checkpoint | Stage 4' | Decision = Major, user confirms | Pass new Revision Roadmap (limitations-only when the user chooses it for a Major that rests only on items they declined; `../agents/the orchestrate role § Declined Items at Stage 3' and Stage 4') |
| Stage 4' | **checkpoint** | Stage 4' completed | Wait for user confirmation |
| checkpoint | Stage 4.5 | User confirms | Pass revised draft to final verification |
| Stage 4.5 | **checkpoint** | PASS (zero issues, counting the final-output pre-check items; notes such as UNVERIFIABLE_ACCESS are not issues), or recorded Integrity Check FAIL Loop resolution (§ below) | Wait for user confirmation |
| Stage 4.5 | Stage 4.5 (retry) | FAIL | Fix issues, re-verify (max 3 rounds) |
| checkpoint | Stage 5 | User confirms (MANDATORY — the Stage 5 entry gate; see § Stage 5 boundary semantics) | Record the finalization decisions and pass the accepted draft to `draft` for formatting and applicable submission materials |
| Stage 5 | **checkpoint** | Stage 5 completed, Final Paper delivered | Wait for user confirmation (FULL — never SLIM; see § Stage 5 boundary semantics) |
| checkpoint | Stage 6 | User confirms | `orchestrate` produces the process record per `process_summary_protocol.md` |
| checkpoint | completed | User declines Stage 6 | Mark Stage 6 `skipped` (non-mandatory stage); set pipeline global state `completed` |
| Stage 6 | **terminal checkpoint** | Process Record delivered | Wait for terminal acknowledgement (see § Stage 6 terminal semantics) |
| terminal checkpoint | completed | User acknowledges (`finish` / `end` / `done` / `confirm`, or an unambiguous natural-language equivalent) | Mark Stage 6 `completed`; set pipeline global state `completed` |

**Strict experiment intake.** Follow the [experiment intake protocol](../strict/pipeline_orchestrator_agent.md#experiment-intake-question) to record the declaration before the strict Stage 2 writer or integrity gate dispatches.

### Special Flow Transitions

| From | To | Precondition | Action |
|------|----|-------------|--------|
| Stage 3 (Reject) | Stage 2 | User chooses to restructure | Clear Stage 2-3 state, preserve Stage 1 materials, restart Stage 2 |
| Stage 3 (Reject) | ABORT | User chooses to abandon | Save all produced materials, mark pipeline aborted |
| Stage 3' (Major) | Stage 4' | User confirms | Last revision opportunity |
| Stage 4' | Stage 4.5 | Revision complete | Go directly to final verification (no return to review) |
| Any stage | PAUSED | User says "pause" or "stop here" | Save pipeline state |
| PAUSED | Recorded stage or next stage | User resumes a validated run | Restore state, confirm the tracked manuscript and report still apply, and resolve any pending checkpoint before dispatch. Re-run invalidated gates |

### Prohibited Transitions (Illegal)

| From | To | Reason |
|------|----|--------|
| INIT / Stage 1 | Stage 3, 4, 3' or 5 | A new full run with a manuscript must pass through Stage 2.5 and its checkpoint before dispatching a downstream stage |
| Stage 2 | Stage 3 | **Cannot skip Stage 2.5 (integrity check is mandatory)** |
| Stage 4 | Stage 5 | Cannot skip RE-REVIEW (revision must be re-reviewed) |
| Stage 3' | Stage 5 | **Cannot skip Stage 4.5 (final integrity check is mandatory)** |
| Stage 4' | Stage 3' | Cannot return to RE-REVIEW (max 1 round of RE-REVISE) |
| Stage 5 | Stage 3 | Cannot roll back (no review after FINALIZE) |
| completed | in_progress | Completed stages cannot restart |

---

## Stage 5 and Stage 6 Boundary Semantics

The two boundaries below were under-specified before (different runtimes could resolve them differently). This section is the authority; `../ROLE.md` mirrors it.

### Stage 5 boundary semantics

"Before finalization (Stage 5): always MANDATORY" refers to exactly ONE checkpoint: the **Stage 5 entry gate** — the checkpoint between Stage 4.5 PASS and the Stage 5 dispatch. It is MANDATORY because it carries the finalization decisions:

- explicit confirmation to proceed to finalization (no auto-advance);
- the finalization-format decision: citation style (APA 7.0 / Chicago / IEEE, ...) — the "Stage 5 finalization format" pending decision the passport-reset machinery records at this boundary.

Transition state: `awaiting_confirmation` → on user confirmation → Stage 5 `in_progress`.

In strict mode, surface the advisories inside this same checkpoint, after the exact
Stage 4.5 PASS and before the confirmation. The orchestrator runs first and
second against the identical accepted-draft artifact ID/SHA-256. They do
not create a second checkpoint or transition state. A schema-valid degraded
artifact (exit 1) is preserved; a failure writes no carrier and records only
bounded `ADVISORY_UNAVAILABLE:<CODE>`. Neither result blocks/delays confirmation,
changes Stage 4.5, adds remediation routing, or changes Stage-5 dispatch.

Any manuscript revision stales both carriers and returns through integrity before
the fixed-then-sequence reruns on the new accepted bytes. Reusing only
one old carrier is invalid handoff cargo, not a new state-machine branch.

Other confirmations near Stage 5 are NOT this MANDATORY boundary:

1. The in-stage interactions of the Stage 5 output process — the question of which files to produce (Step 2) and the content confirmation before the final PDF (Step 4) — are part of Stage 5 execution, not pipeline checkpoints; they are asked during the stage, never at the gate.
2. The **Stage 5 completion checkpoint** (Final Paper delivered, before Stage 6) follows the global stage-completion rule: it is a FULL checkpoint — never SLIM, because final-deliverable acceptance must not be downgraded — but it is not on the MANDATORY list.

### Stage 6 terminal semantics

Stage 6 is a non-mandatory stage (it is absent from the orchestrator's non-skippable list). At the Stage 5 completion checkpoint the user may decline it: Stage 6 is marked `skipped` and the pipeline still terminates `completed` (the Final Paper was already produced at Stage 5).

When Stage 6 runs, its completion is the pipeline's **terminal checkpoint**:

1. After delivering the Process Record (MD, plus PDF when the user asked for it, per the user's language choice), the orchestrator prompts for a terminal acknowledgement.
2. Terminal acknowledgement vocabulary: `finish` / `end` / `done` / `confirm`, or an unambiguous natural-language equivalent that accepts the deliverables. Change requests (the other language version, content corrections) keep Stage 6 `in_progress` — they are not acknowledgements.
3. On acknowledgement: state_tracker marks Stage 6 `completed` and sets the pipeline global state to `completed`. This is the terminal transition — there is no next stage.
4. After `completed`, no stage transition is legal (see Prohibited Transitions). New requests start a new pipeline run or a targeted single-skill invocation (mid-entry).

### Checkpoint decision provenance

Every checkpoint decision, terminal acknowledgement, override, consent grant, and authorization input in this state machine exists only when it appears in a user turn. A subagent report, a hook or tool result, a template's default branch, an orchestrator-written checkpoint summary, or a paraphrase of an earlier turn is never the user's decision; a checkpoint whose decision has not appeared in a user turn is still open. Re-transmission to a subagent quotes the user's words (or the exact deterministic authorization artifact) and never widens them. Where a deterministic authorization artifact exists (the integrity-correction authorization, the user's read-scope declaration scope) it is the enforced form of this rule; elsewhere the rule is prompt-level. Mirrored operationally in the orchestrate role § Checkpoint authority fidelity; the risk is indexed as R11 in `docs/RISK_REGISTER.md`.

**Run ledger.** When the run has a passport file, the orchestrator appends each checkpoint's opening and the user's answer in their exact words, as they happen, to the run ledger beside the passport (`<passport-stem>_run_ledger.yaml`, written by `@/engine/scripts/run_ledger.py`), with the other records its mirror lists. After compaction, on resume, and after a subagent return, a decision that neither the ledger records in the user's words nor a user turn in the session shows is still open. The ledger records decisions; it never creates one, so an entry written without a user turn is not a decision (R11). Mirrored in the orchestrate role § Run ledger and handoff check; the loss risk is indexed as R12.

---

## Material Dependency Matrix

| Material | Produced At | Consumed At | Required/Recommended |
|----------|-----------|-------------|---------------------|
| RQ Brief | Stage 1 | Stage 2 (Phase 0) | Recommended |
| Methodology Blueprint | Stage 1 | Stage 2 (Phase 0) | Recommended |
| Bibliography | Stage 1 | Stage 2 (Phase 1) | Recommended |
| Synthesis Report | Stage 1 | Stage 2 (Phase 3) | Recommended |
| `preregistration-artifact/1.0` sidecar + provided named companion | Stage 1 shell-capable dispatch | Academic-paper intake, every handoff, Stage 4.5/checkpoint | Strict procedure only. **Receipt required when this dispatch runs**; validate and carry exact bytes |
| Paper Draft | Stage 2 or user-provided | Stage 2.5 (input) | **Required** |
| **Integrity Report (Pre) and checked draft** | **Stage 2.5** | **Confirmed target (3, 4, 3' or 4.5)** | **Required**. Preserve the warning and open issues on a recorded FAIL-loop continuation |
| Review reports or external review comments | Stage 3 or user-provided | Stage 4 and Stage 3' | In strict Stage 3', apply the Round-1 finding presence policy from the strict handoff |
| Editorial Decision | Stage 3 or user-provided | Stage 4 | Carry when produced or supplied |
| Revision Roadmap | Stage 3, Stage 4 coaching or user-provided | Stage 4 and Stage 3' | Required to revise or verify a round. Use the existing feedback to build it when needed |
| Revised Draft | Stage 4 or user-provided | Stage 3' | Required. Include the original draft when required by the selected re-review procedure |
| Response to Reviewers | Stage 4 | Stage 3' (input) | Recommended |
| Editorial Decision Letter (Schema 6) | Stage 3 | Stage 3' (input) | Recommended (— its Review Panel Provenance block feeds the Judge Record; absent → "unknown (provenance block absent)") |
| Apply report(s) + paired revision patch/diff files (sidecar + patch JSON) | Stage 4 | Stage 3' (input) + Stage 4.5 (input) | Strict patch rounds only. Keep the pairs together and validate the ordered chain under `re_review_mode_protocol.md` § Input Manifest |
| Traceability sidecar (`@/engine/contracts/re_review/traceability.schema.json`) | Stage 3' | Stage 4.5 (input — frozen `previously_missed`/`indeterminate` records, §8; direct on Accept/Minor, through 4' on Major) | Recommended (contract-mode Stage 3' only; a `[LEGACY-NO-CONTRACT]` run produces none — visible degradation at 4.5, not a block) |
| Reviewer Configuration Cards | Stage 3 (field_analyst) | Stage 3' (re-review mode — yardstick continuity; field_analyst NOT re-run) | Recommended (absent → visible regeneration fallback, `re_review_mode_protocol.md` § Yardstick Continuity; a fresh full review at 3' regenerates by definition) |
| **Re-Review Report** | **Stage 3'** | **Stage 4' (input)** | **Required (if Major)** |
| **Re-Revised Draft** | **Stage 4'** | **Stage 4.5 (input)** | **Required (if executed)** |
| **Integrity Report (Final)** | **Stage 4.5** | **Stage 5 (prerequisite)** | **Required** |
| Final Paper | Stage 5 | User (delivery) | Required |
| Process Record | Stage 6 | User (delivery) | Optional (Stage 6 is skippable) |

---

## Exception State Handling

### Timeout

If a stage shows no progress for an extended period (e.g., Socratic mode exceeds 15 rounds without convergence):
1. state_tracker marks the stage as `stalled`
2. orchestrator provides options:
   - Switch mode (socratic -> full)
   - Narrow scope
   - Skip this stage (non-mandatory stages only)

### Missing Materials

If materials are found missing during transition (gap types per `../agents/state_tracker_agent.md`):
1. state_tracker reports the material gap
2. Missing required material blocks that transition. The orchestrator identifies what to supply or the stage that produces it. Strict runs also record `HANDOFF_INCOMPLETE` under `@/engine/handoff_schemas.md` Validation Rules, rule 5.
3. Missing recommended material: the transition is not blocked; the user is told it may affect quality and can backfill or continue
4. Integrity checks cannot be skipped in either case

### Integrity Check FAIL Loop

If Stage 2.5 or 4.5 corrections exceed 3 rounds without passing:
1. List all unverifiable items
2. User decides:
   - Manually handle unverifiable items
   - Remove unverifiable citations
   - Continue to next stage (with "partially unverified" warning), except for an item the Stage 5 formatter would refuse (`../agents/the orchestrate role § Final-Output Pre-Check at Stage 4.5), which is handled or removed

### Session Interruption

If the user leaves and returns:
1. orchestrator displays Progress Dashboard
2. Confirm whether to continue from breakpoint
3. Check if any outdated materials need refreshing

---

## Revision Loop Rules

### Simplified Revision Cycle

```
v2.0's revision cycle is simpler and more explicit than v1.0:

Stage 3 (First REVIEW)
  -> Decision: Accept -> Stage 4.5
  -> Decision: Minor/Major -> Stage 4
      -> Stage 4 (REVISE)
          -> Stage 3' (RE-REVIEW, verification)
              -> Decision: Accept/Minor -> Stage 4.5
              -> Decision: Major -> Stage 4' (last revision)
                  -> Stage 4.5 (go directly to final verification, no return to review)

Maximum 1 round of RE-REVISE, no infinite loops.
Unresolved issues -> Acknowledged Limitations.
```

### Differences from v1.0

| v1.0 | v2.0 |
|------|------|
| Max 2 review-revise cycles | Fixed 2 reviews (Stage 3 + Stage 3') + max 1 RE-REVISE |
| No integrity check | Mandatory Pre-review + Final integrity check |
| 4 reviewers | 5 reviewers (+Devil's Advocate) |
| Can skip any stage | Stage 2.5 and 4.5 cannot be skipped |
| No mandatory checkpoints | Every stage requires a checkpoint |

## Reset-boundary transitions (flag-gated)

When `RW_PASSPORT_RESET=1`, every FULL or MANDATORY checkpoint carries an implicit state transition to a terminal `awaiting_resume` state. The next stage only starts when a new session posts `resume_from_passport=<hash>`.

Transition semantics:

```
Stage N [working]
  -> FULL checkpoint
    -> [flag OFF]  Stage N+1 [working]           (earlier continuation)
    -> [flag ON]   append boundary entry -> awaiting_resume
         -> resume_from_passport=<hash>
              -> append resume entry (consumes_hash=<hash>)
              -> Stage N+1 [working]              (fresh session, passport-loaded)
```

Iron rules:

- `awaiting_resume` is not persisted in `state_tracker`; it is computed from the passport ledger. A `boundary` entry with hash `H` is awaiting resume iff no later `resume` entry in `reset_boundary[]` carries `consumes_hash == H`. Single pass over the ledger, no out-of-band state.
- `systematic-review` under flag ON cannot transition `Stage N → Stage N+1` without a fresh-session resume. In-session continuation is refused.
- Other modes under flag ON allow in-session continuation as a fallback, but the orchestrator must still load Stage N+1 input strictly from the passport (no replay of prior turns).
- SLIM checkpoints never enter `awaiting_resume`.
- MANDATORY checkpoints also enter `awaiting_resume` when the flag is ON. Integrity gates remain MANDATORY; the reset does not downgrade them. The `### Resume Instruction` subsection emitted alongside `[PASSPORT-RESET: ...]` carries the passport file path and resume command — it does NOT carry the user decision prompt. The decision prompt happens on resume, after the fresh session loads the passport (see next rule).
- If a `boundary` entry carries `pending_decision`, `next` is advisory only. The user's branch choice happens AFTER `resume_from_passport=<hash>` in the fresh session, or right after an in-session `continue` in non-SR modes, never in the reset checkpoint itself. The orchestrator re-prompts the user in the new session before transitioning to any `Stage N+1`. The `resume` entry records the chosen branch via `chosen_branch`. Actual routing comes from the matched option's `next_stage`/`next_mode`; `next` is a fallback default only.
- `pending_decision` stays authoritative for the reset path when the run ledger also records the checkpoint. The ledger's opened entry names the boundary hash (`reset_boundary_hash`), and the answer closes both: the `resume` entry that consumes that hash records it, and so does the ledger's closing entry for the same checkpoint.

See [`passport_as_reset_boundary.md`](../strict/passport_as_reset_boundary.md) for the full protocol.
