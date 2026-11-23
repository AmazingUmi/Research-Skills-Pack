# Two-Stage Review Protocol (Added in v2.0)

## Stage 3: First Review (Full Review)

- **Input**: Paper that passed integrity check
- **Review team**: Journal-Fit Reviewer + R1 (methodology) + R2 (domain) + R3 (interdisciplinary) + Devil's Advocate
- **Output**: 5 review reports + Editorial Decision + Revision Roadmap + Socratic Revision Coaching
- **Decision branches**: Accept -> Stage 4.5 / Minor|Major -> Revision Coaching -> Stage 4 / Reject -> Stage 2 or end

See `@/roles/review/panel/MODE.md` for review process details.

## Stage 3 -> 4 Transition: Revision Coaching

The Journal-Fit Reviewer uses Socratic dialogue to guide the user in understanding review comments and planning revision strategy (max 8 rounds). User can say "just fix it for me" to skip; when the user's answer already says how to revise, coaching is offered rather than started.

## Stage 3': Second Review (Verification Review)

Use this section for simulated reviews. For real feedback, use [external self-verification](external_review_protocol.md#step-4-self-verification-completeness-check) and route the checked revision and response to Stage 4.5 after its checkpoint.

- **Default inputs** include the revised and original drafts, prior findings or reviewer comments, revision roadmap and available response. If the user brings an external revision, verify that the materials cover the prior round before dispatch.
- **Strict inputs** follow [strict re-review dispatch](../strict/pipeline_orchestrator_agent.md#stage-3-re-review-contract-dispatch). Use the original draft, exact author-adjudication sidecar, replayed Revision-Evidence Bundle and ordered apply report/patch pairs. Apply the strict protocol's Round-1 finding and reviewer-card presence rules. A missing required original, roadmap, authorization or bundle produces `manifest_incomplete`.
- **Mode and output** use `review re-review` for the comparison table, residual issues and new decision. The strict procedure also emits a validated R&R Traceability Matrix. When the user requests a fresh full review, use `review panel` with the revised draft and available context and produce the usual five reviews, decision and roadmap.
- **Decision branches**: Accept|Minor -> Stage 4.5 / Major -> Residual Coaching -> Stage 4' (a Major driven only by items the author declined may instead take a limitations-only Stage 4' without coaching; `../agents/the orchestrate role § Declined Items at Stage 3' and Stage 4')

See `@/roles/review/panel/MODE.md` Re-Review Mode for verification review process.

## Stage 3' -> 4' Transition: Residual Coaching

The Journal-Fit Reviewer guides the user in understanding residual issues and making trade-offs (max 5 rounds). User can say "just fix it" to skip.
