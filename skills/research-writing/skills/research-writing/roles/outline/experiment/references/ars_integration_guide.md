# this skill Integration Guide

How the outline role's experiment mode works with research-writing pipeline. This file lives in the outline role's experiment mode repo. this skill requires zero modification.

## Principle

```
outline experiment ──knows──> ARS handoff format
ARS ──does not know──> outline experiment
User ──bridges──> between the two
```

## Reading Stage 1 Output

When a user brings Stage 1 (RESEARCH) output to the outline role's experiment mode, detect these section headings:

| Heading | Maps To |
|---------|---------|
| `## Research Question Brief` | plan mode step 1 (RQ + hypothesis), manage mode PLAN step 1 |
| `## Methodology Blueprint` | plan mode steps 2-4 (variables, design, methods), manage mode PLAN steps 2-4 |
| `## Annotated Bibliography` | Reference context (do not depend on; the outline role's experiment mode does not do lit review) |
| `## Synthesis Report` | Background context for experiment design |

**Detection method**: Loose heading matching. Do not depend on this skill schema version numbers. If headings are present, parse. If not, ask user for context.

## Producing ARS-Compatible Output

All the outline role's experiment mode outputs include a **Material Passport** header (this skill Schema 9):

```markdown
## Material Passport

- Origin Skill: outline experiment
- Origin Mode: [run | manage | validate | plan]
- Origin Date: [ISO 8601 timestamp]
- Verification Status: [UNVERIFIED | ANALYZED | VERIFIED]
- Version Label: [exp_result_v1 | study_status_v1 | validation_v1 | code_plan_v1 | study_protocol_v1]
```

**Verification Status rules:**
- `run` mode output → `UNVERIFIED` (results not yet validated)
- `manage` mode output → `UNVERIFIED` (data collected but not analyzed)
- `plan` mode output → `UNVERIFIED` (design artifact only; nothing has been executed yet)
- `validate` mode output without a successful reproducibility re-run → `ANALYZED` (statistical interpretation completed, but execution-level verification is absent, not applicable, or failed)
- `validate` mode output with a successful reproducibility re-run → `VERIFIED`
- Only upgrade a prior `run` artifact to `VERIFIED` after a successful reproducibility re-run. If re-run is skipped, not applicable, partial, or fails, keep the original artifact at `UNVERIFIED` and attach the separate validation report.

**Optional fields** (include when available):
- `Integrity Pass Date`: timestamp when validate mode completed
- `Upstream Dependencies`: version labels of artifacts this one depends on (e.g., if experiment used Stage 1 RQ Brief)

## User Workflow: this skill → the outline role's experiment mode → this skill

```
1. User runs ARS Stage 1 (literature) → gets RQ Brief + Methodology Blueprint
2. User copies relevant sections to outline experiment
3. outline experiment: plan mode → run/manage mode → validate mode → produces results
4. User copies experiment_result / validation_report back to ARS
5. User starts ARS Stage 2 (draft) with experiment results as input
6. ARS Stage 2 writer sees Material Passport → knows origin and verification status
```

The user is the bridge. No API calls, no automated handoff, no shared state.

## Future this skill Integration (Not v1)

If this skill ever wants to auto-detect the outline role's experiment mode output:

```
At Stage 2 start:
  if user input contains "## Material Passport" with "Origin Skill: outline experiment":
    → auto-load experiment results as Stage 2 source material
    → skip "do you have experiment data?" question
  else:
    → normal flow
```

This requires a one-line detection in the orchestrate role. Not implemented in v1 — documented here for future reference.
