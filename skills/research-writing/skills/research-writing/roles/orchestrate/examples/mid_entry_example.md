# Example: Starting the Default Pipeline with an Existing Draft

The author has a complete 7,000-word IMRaD draft, its references, and the analysis tables. This is a new run with the current draft as its baseline.

> **Author.** Use `$research-writing full` on my draft “Machine Learning Approaches for Predicting University Attrition Risk in Taiwan.” I'd like the full workflow through simulated review, revision, and LaTeX finalization.

## Stage 2.5 — Verify the Current Draft

The orchestrator confirms the starting version, target, and planned stages with the author. The existing materials cover the research and initial drafting stages, so the run starts at 2.5. An integrity report from an earlier run can point to useful evidence. The orchestrator still checks the current draft.

The author confirms the plan. The [default integrity procedure](../agents/default_integrity_review.md) records references, citation context, data, originality, and claim verification in a report and evidence matrix tied to the current draft. For example, `C-07`, an AUROC reported for the held-out set, links to the exact analysis table and evaluation split. The check passes, and the author confirms the transition to review.

## Stage 3 — Panel Review

[`review panel`](../../review/panel/MODE.md) prepares reviewer cards and waits for the author to confirm them before dispatching the five seats. The editorial decision records a major revision. The roadmap identifies `R-001`, a request to clarify which cohorts the validation covers, and `R-002`, a request to document the use restrictions on student records. The author confirms which items to address and supplies the study's approved data-use wording.

## Stage 4 — Revision

[`review revise`](../../review/revise/MODE.md) keeps the verified draft as the baseline and edits a candidate within the author's approved scope. The new version narrows the claims about external validity to the observed cohorts and adds the data-use statement. It accompanies a change record and a point-by-point response.

## Stage 3′ — Re-Review

After the author confirms the transition, [`review re-review`](../../review/panel/MODE.md#re-review) uses the original draft, revised draft, roadmap, and first-round reviewer cards. It checks the changes against the evidence before reading the response, then issues an Accept decision. The author confirms which candidate advances to the final check.

## Stages 4.5 and 5 — Verify, Then Finalize

The orchestrator checks the entire candidate with the [default integrity procedure](../agents/default_integrity_review.md) and presents the final report. After the author confirms the checked version and requested output, [`draft format-convert`](../../draft/paper/MODE.md) prepares the LaTeX and bibliography files from that version.
