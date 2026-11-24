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

- **Default inputs** include the revised and original drafts, the simulated panel's earlier findings, the revision roadmap and the available response. A simulation resumed in a new session needs the materials from its previous round.
- **Strict inputs** follow [strict re-review dispatch](../strict/pipeline_orchestrator_agent.md#stage-3-re-review-contract-dispatch). Use the original draft, exact author-adjudication sidecar, replayed Revision-Evidence Bundle and ordered apply report/patch pairs. Apply the strict protocol's Round-1 finding and reviewer-card presence rules. A missing required original, roadmap, authorization or bundle produces `manifest_incomplete`.
- **Mode and output** use `review re-review` for the comparison table, residual issues and new decision. The strict procedure also emits a validated R&R Traceability Matrix. When the user requests a fresh full review, use `review panel` with the revised draft and available context and produce the usual five reviews, decision and roadmap.
- **Missing evidence**: When an unresolved item could change the decision, keep Stage 3' pending (user_review_required), request the named material and recheck the affected findings.
- Accept or Minor proceeds to Stage 4.5. Major returns to Stage 4' via residual coaching. If the decision rests entirely on items the author declined, offer the [limitations-only option](../strict/pipeline_orchestrator_agent.md#declined-items-at-stage-3-and-stage-4) at the checkpoint.

See `@/roles/review/panel/MODE.md` Re-Review Mode for verification review process.

## Stage 3' -> 4' Transition: Residual Coaching

The Journal-Fit Reviewer guides the user in understanding residual issues and making trade-offs (max 5 rounds). User can say "just fix it" to skip.
