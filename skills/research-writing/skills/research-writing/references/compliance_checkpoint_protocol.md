---
title: Compliance Checkpoint Protocol (Stage 2.5 / 4.5 dual gate)
applies_to: "@/roles/orchestrate/agents/compliance_agent.md"
---

# Compliance Checkpoint Protocol

Defines how `compliance_agent` participates in Stage 2.5 and Stage 4.5 Integrity Gates, how its decision interacts with the existing FAIL loop, and how user overrides are processed.

**Used by**: `compliance_agent` (Task 8), `the orchestrate role/MODE.md` Stage 2.5 / 4.5.

## Dual-gate summary

| Aspect | Stage 2.5 | Stage 4.5 |
|---|---|---|
| PRISMA-trAIce scope (SR mode only) | M1, M2, M3, M4, M5, M6, M7, M8, M9, M10 | T1, A1, I1, R1, R2, D1, D2 |
| RAISE principles focus | human_oversight, fit_for_purpose | transparency, reproducibility |
| RAISE 8-role matrix | not populated | populated (SR mode only) |
| Block condition | SR mode AND any Mandatory item = FAIL, OR SR mode AND any RAISE principle = fail | Same |
| Warn condition | Highly Recommended FAIL, OR RAISE principle = warn | Same |
| Info condition | Recommended / Optional FAIL | Same |
| Non-SR mode | RAISE principles_only, warn-only (never block) | Same |
| Checkpoint output | FULL checkpoint + `compliance` section in dashboard | Same |

## Decision precedence

Inside a single checkpoint, decisions aggregate as:

```
overall_decision = max_severity(
  prisma_trAIce.block_decision,
  raise.block_decision,
  legacy_integrity_verification_decision,  # existing Stage 2.5/4.5 check
  legacy_failure_mode_checklist_decision   # Failure Mode Checklist
)

severity order: pass < warn < block
```

Non-SR mode caps the compliance contribution at `warn`.

## User action UX

### On block

Orchestrator presents:

```
[COMPLIANCE BLOCK] Stage <N>

PRISMA-trAIce Mandatory fails: M4 (Input Data)
RAISE principles fail: reproducibility

Choose:
  (a) backfill — return to Stage 2 and add missing material
  (b) manual handling — edit manuscript directly, rerun compliance
  (c) acknowledge limitation — invoke user override (see §Override Ladder)
```

### On warn

Dashboard bullets, FULL checkpoint. User confirms with free text or `continue`.

### On info (Recommended / Optional fail)

Bullet in dashboard, no flow interruption.

## Canonical gap-tag vocabulary

Compliance reports and fixture templates use these canonical tags in `gaps[].reason`, `principle_evidence[]`, and narrative fields. They are lexical signals — `compliance_agent` (Task 8) and downstream readers pattern-match on them.

| Tag | Where it appears | Meaning |
|---|---|---|
| `[MATERIAL GAP]` | `gaps[].reason`, `principle_evidence[]`, `evidence[]` | The item cannot be verified because the underlying material (passport field, manuscript section, supplementary file) is missing. Apply [Anti-Leakage Protocol](../roles/draft/paper/references/anti_leakage_protocol.md) — do not hallucinate. |
| `[WEAK EVIDENCE]` | `principle_evidence[]` | The item is nominally reported but the description is too vague for auditor use. Triggers CA-4 downgrade: a RAISE principle marked `pass` with `[WEAK EVIDENCE]` in its evidence should be downgraded to `warn`. |
| `[GAP]` | `roles[].evidence_synthesists` narrative and similar role-level fields | Short form for a role-level gap carried forward from item-level fails. Permitted only in the 8-role matrix narrative; item-level reasons MUST use the long `[MATERIAL GAP]` form. |

Casing is significant — uppercase square-bracketed. Lowercase or missing brackets are treated as plain prose and will not be recognised as gap signals.

<!-- harness-retirement 2026-06-10 (F-008): the "do not hallucinate" tail on the [MATERIAL GAP] row is kept as known debt — high-stakes academic compliance surface with a silent failure mode; delete only with calibration evidence that the tail is inert. -->

## Override Ladder

A reporting limitation may be acknowledged with the author's reason, its exact scope and the affected items recorded in `compliance_history[].user_override`. The compliance agent drafts a disclosure addendum for the assigned writer. Confirmed fabricated, misattributed or materially unsupported citations are ineligible for citation even if the author chooses to continue the project. Record them in the rejection log, exclude them from the citable corpus, and require a verified correction or evidence of a false positive before reinstatement. Preserve historical records and resume state.

### Advisory adjudication-activity receipt

The compliance decision, friction-ladder enforcement, manuscript disclosure,
and ordinary routing/state effect are completed and made durable first. Only
afterward may the action-time producer best-effort append a closed activity
binding through the state tracker's sole-writer path; receipt failure cannot
change the override or checkpoint outcome.

Every executed compliance report is eligible to be bound as the
`compliance_report` role. A plain PASS or WARN report with no `user_override`
is a valid report-only **captured-zero** group. The paired
`compliance_override_action_receipt` is required only when the report satisfies
the complete qualifying-override predicate in the frozen spec: a
systematic-review compliance contribution actually blocks, user action is
required, the user override is true, and the recomputed blocker scope, stage,
run, report hash, actor/source/action, ordinal/friction, occurrence id, and
interaction digest all match. The action receipt contains no rationale. It is
forbidden for a plain report and may not turn a legacy-only block, PASS/WARN,
`user_action_required=false`, or malformed/non-qualifying override claim into
activity.

These receipt bindings remain internal activity metadata under
`state_tracker_agent.md` § "Adjudication-activity metadata". They never enter
`compliance_history`, the Material Passport, manuscript disclosure, checkpoint
decision, gate/verdict input, Process Record, handoff, or model prompt, and are
never reconstructed from prose. No model/judge/eval, network/API, clock, or
ambient scan participates in their production.

### `disclosure_addendum` template

```
The authors acknowledge the following compliance limitations for this <evidence synthesis|manuscript>:
- PRISMA-trAIce <item_id> (<item_title>) not fully reported. Rationale: <user text>.
- RAISE principle <principle_name>: <partial|not met>. Rationale: <user text>.
```

**Template fill rules** (compliance_agent uses these deterministically):

- `<evidence synthesis|manuscript>`: pick `evidence synthesis` when `mode in {systematic_review, other_evidence_synthesis}`; pick `manuscript` when `mode == primary_research`.
- `<partial|not met>`: pick `partial` when the principle's original status was `warn`; pick `not met` when it was `fail`.
- `<item_id>`: the PRISMA-trAIce item ID as listed in `user_override.scope[]`.
- `<item_title>`: look up the short title from `@/references/prisma_trAIce_protocol.md` (e.g. `M4` → "Input data").
- `<principle_name>`: one of `human_oversight`, `transparency`, `reproducibility`, `fit_for_purpose`.
- `<user text>`: verbatim copy of `user_override.rationale`, truncated to first 500 chars if longer (the addendum keeps prose; the full rationale lives in the compliance_history).

## Fail loop integration

After 3 unresolved rounds of retry at the same stage, orchestrator invokes the existing `pipeline_state_machine.md §Integrity Check FAIL Loop` procedure:

1. List all unresolvable items.
2. User picks [manual handling / remove AI usage from this stage / continue with "partially non-compliant" warning].
3. Chosen path is recorded as `compliance_history[].resolution_path`.

## Append-only history

`material_passport.compliance_history[]` never overwrites. On retry-pass, the previous fail entry is preserved with its own timestamp. The AI Self-Reflection Report at Stage 6 cites the full history to demonstrate how the correction was made — this is RAISE transparency applied to this skill itself.

## Boundary: non-pipeline invocation

When invoked from the draft role's `full` mode (primary research standalone), no pipeline state machine is available. Compliance_agent:

- Writes report to `./compliance_reports/<ISO-timestamp>.yaml` (local file)
- Does not trigger pipeline checkpoint dashboard
- If skill has a `disclosure` mode, hooks compliance output there
- `block_decision` capped at `warn`
