# Experiment handoff

## Reading Stage 1 Output

When a user brings Stage 1 (RESEARCH) output to the outline role's experiment mode, detect these section headings:

| Heading | Maps To |
|---------|---------|
| `## Research Question Brief` | plan mode step 1 (RQ + hypothesis), manage mode PLAN step 1 |
| `## Methodology Blueprint` | plan mode steps 2-4 (variables, design, methods), manage mode PLAN steps 2-4 |
| `## Annotated Bibliography` | Reference context (do not depend on; the outline role's experiment mode does not do lit review) |
| `## Synthesis Report` | Background context for experiment design |

Use equivalent headings or the project’s evidence matrix to locate these materials. Request additional context only when the available materials leave a required input unclear.

## Handoff to the next role

In the default workflow, give the receiving role the versioned experiment plan or
result, its claim IDs, dataset and analysis version, source locations and supported
scope in the [evidence matrix](../../../../references/handoff.md).

In the strict workflow, also pass the [Schema 9 Material Passport](../../../../engine/handoff_schemas.md#schema-9-material-passport-cross-stage-metadata). Its summary can appear in the report as follows.

```markdown
## Material Passport

- Origin Skill: outline experiment
- Origin Mode: [run | manage | validate | plan]
- Origin Date: [ISO 8601 timestamp]
- Verification Status: [UNVERIFIED | VERIFIED | STALE]
- Version Label: [exp_result_v1 | study_status_v1 | validation_v1 | code_plan_v1 | study_protocol_v1]
```

**Verification Status rules:**
- `run` mode output → `UNVERIFIED` (results not yet validated)
- `manage` mode output → `UNVERIFIED` (data collected but not analyzed)
- `plan` mode output → `UNVERIFIED` (design artifact only; nothing has been executed yet)
- `validate` mode output with a skipped, inapplicable, partial or failed re-run → `UNVERIFIED`. Report the extent of statistical interpretation and the actual re-run outcome separately in the validation report.
- `validate` mode output with a successful reproducibility re-run → `VERIFIED`
- A previously verified result whose data, code or analysis version has since changed is `STALE` until verified against the current inputs.
- When consuming an older validation report labelled `ANALYZED`, preserve the original report. In a new handoff record the completed interpretation in the report and use `UNVERIFIED` for execution-level verification unless the current result has a documented successful re-run.

**Optional fields** (include when available):
- `Integrity Pass Date`: timestamp of a passed integrity check, if one was performed
- `Upstream Dependencies`: version labels of artifacts this one depends on (e.g., if experiment used Stage 1 RQ Brief)
