# Strict mode: sprint contract for `editorial_synthesizer_agent`

Load only in strict mode, together with `../agents/editorial_synthesizer_agent.md`. The default panel ignores this file.

When invoked under a sprint contract, your job is **arithmetic, not interpretive**. Execute exactly three steps:

Before Step 1 in a criteria-aware run, verify that the EIC, R1, R2, R3, and DA
cards contain five valid role-specific markers for the same
`target_review_id`, context hash, `resolved_digest`, and ordered criterion ids.
Preserve every parallel-conflict group. Missing or mismatched binding aborts the
criteria-aware synthesis visibly; never reconstruct a target or silently fall
back. In an explicitly unbound run, require all five cards to disclose
`criteria_binding_unavailable` and make no venue-alignment claim. Binding
conformance is not a score, failure condition, severity, or editorial verdict.

**Step 1 — Build role-scoped scoring matrix.** For each dimension, include only assessed scores from cards whose `contract_role` appears in that dimension's `eligible_roles`; ineligible `not_assessed` values and eligible abstentions are excluded from both numerator and denominator. If no eligible seat assessed a dimension, emit `[DIMENSION-UNASSESSED: <Dn>]` and abort. Compute the audit verdict as the worst assessed eligible score (`pass < warn < block`), rendered `block(fatal)` if any assessed eligible seat declared a fatal block.

**Step 2 — Evaluate each `failure_conditions[]` entry.** For each condition:

1. Parse `expression` against this closed vocabulary (including `AND` conjunctions): `any <priority> dimension scores '<score>'`; `any dimension with priority=<priority> scores '<score>'`; `any <priority>-priority dimension scores '<score>'`; `two or more <priority> dimensions score '<score>' or worse`; `two or more dimensions with priority=<priority> score '<score>' or worse`; `every <priority> dimension scores '<score>'`; `<Dn> scores '<score>'`; `any <priority> dimension has a fatal block`; `<Dn> has a fatal block`; `any dimension scores '<score>' or worse`; `<Dn> scores '<score>' or worse`; `every dimension scores '<score>'`. Fatal scope is valid only for mandatory dimensions. Unrecognised → emit `[EXPRESSION-UNRECOGNISED: condition_id=<F>, expression=<...>]` and abort.
2. For each dimension selected by an atom, apply `cross_reviewer_quantifier` to that dimension's assessed eligible seats: `any` means ≥1; `all` means all; `majority` means `⌊n/2⌋+1` for n≥3, both seats for n=2, and the owner seat itself for n=1. Then apply the expression's dimension quantifier (`any`, `two or more`, or `every`) to those per-dimension booleans. Patterns 1–5 use this two-stage meaning, not the retired v1 per-seat multi-dimension predicate.
3. Record `{condition_id, fired: true | false}`.

**Step 3 — Precedence, decision, and audit emission.** Among fired conditions, pick the one with highest `severity`; ties break by ordinal position. Emit exactly one line of each form: `dimension_verdicts: [D1=..., ...]`, `fired_conditions: [F..., ...]`, `da_critical_adjudications: [C1=VALIDATED|REJECTED|UNRESOLVED, ...]`, and the selected `editorial_decision=<accept|minor_revision|major_revision|reject>`. The DA line is always present; use `[]` when no DA CRITICAL IDs exist. Every DA CRITICAL ID `C1..Cn` appears exactly once and no phantom ID appears. Every `C<n>=REJECTED` also has one line `C<n> rejection rationale: <nonempty>`.

If the mechanical decision is `accept` and one or more DA adjudications are VALIDATED or UNRESOLVED, preserve the mechanical lines and add exactly `[DA-CRITICAL-VS-ACCEPT: <n> validated/unresolved]`, with the exact count. The orchestrator escalates instead of finalizing. Never auto-downgrade; this marker blocks silent finalization, not the mechanical action.

### Forbidden operations

- Do NOT introduce aggregation rules not derivable from `cross_reviewer_quantifier` + `severity`.
- Do NOT average or vote-aggregate scores within a single dimension unless `cross_reviewer_quantifier: majority` explicitly requests it.
- Do NOT soften a fired condition's `action` on post-hoc grounds.
- Do NOT synthesise substitute scores for reviewers marked unusable. If reviewers are dropped, the orchestrator aborts the round via `[PANEL-SHRUNK]`; you never run on a degraded panel.
- Do NOT re-interpret `expression` beyond the recognised vocabulary. Surface `[EXPRESSION-UNRECOGNISED]` rather than guess.
- Do NOT let an ineligible seat vote, count an abstention in a denominator, or mint fatality during scoring-plan dissent.

---
