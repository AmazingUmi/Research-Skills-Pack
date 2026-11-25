# Pipeline Status Dashboard Template

This template defines the output format for the Progress Dashboard. Switch between language versions based on user language.

---

## English Version

Use the [stage-to-role table](../ROLE.md#2-阶段与角色调用) for all ten stage rows and substitute the run’s actual modes, including sub-stages and optional Stage 6.

```
+=========================================+
|   Academic Pipeline Status              |
+=========================================+
| Topic: {topic}                          |
+-----------------------------------------+

  {one row per stage, in the order of the stage-to-role table}
    {stage_id} {stage_name} [{status_icon}] {status_text}
    {actual_role_and_mode} {outputs_or_decision}
+-----------------------------------------+
| Materials:                              |
|   [{icon}] RQ Brief                     |
|   [{icon}] Methodology Blueprint        |
|   [{icon}] Bibliography                 |
|   [{icon}] Synthesis Report             |
|   [{icon}] Paper Draft                  |
|   [{icon}] Integrity Report (Pre)       |
|   [{icon}] Verified Paper Draft         |
|   [{icon}] Review Reports               |
|   [{icon}] Editorial Decision           |
|   [{icon}] Revision Roadmap             |
|   [{icon}] Revised Draft                |
|   [{icon}] Response to Reviewers        |
|   [{icon}] Re-Review Report             |
|   [{icon}] Re-Revised Draft             |
|   [{icon}] Integrity Report (Final)     |
|   [{icon}] Final Paper                  |
+-----------------------------------------+
| Revision History:                       |
|   {revision_history}                    |
+-----------------------------------------+
| Next Step: {next_step_suggestion}       |
+=========================================+
```

---

## Field Definitions

### status_icon

| Status | Icon |
|--------|------|
| completed | `v` |
| in_progress | `..` |
| pending | ` ` (space) |
| skipped | `--` |
| blocked | `!` |
| unrecorded in legacy snapshot | `?` |

### status_text

| Status | Text |
|--------|------|
| completed | Completed |
| in_progress | In Progress |
| pending | Pending |
| skipped | Skipped |
| blocked | Blocked |
| unrecorded in legacy snapshot | Unrecorded |

### mode_line

Format: `Mode: {mode_name}`
- Only displayed when status is completed or in_progress
- If mode switched (e.g., plan -> full), display the full path

### outputs_line

Format: `Outputs: {output_1}, {output_2}, ...`
- Only displayed when status is completed
- List all deliverables for that stage

### decision_line

Format: `Decision: {Accept/Minor Revision/Major Revision/Reject}`
- Only displayed when Stage 3 or Stage 3' is completed

### revision_round_line

Format: `Revision Round: {current}/{max}`
- Only displayed when Stage 4 is in_progress

### addressed_line

Format: `Addressed: {count}/{total} required revisions`
- Only displayed when Stage 4 is in_progress

### loop_count_line

Format: `Loop: {count}/1`
- Only displayed for Stage 3'

### material icon

| Status | Icon |
|--------|------|
| available | `v` |
| missing | ` ` (space) |

### revision_history

One line per round:
```
Round {n}: {decision} | {addressed}/{total} items addressed
  Pending: {pending_items_summary}
```

If no revision history, display "(No revision history yet)".

### next_step_suggestion

Auto-generated suggestion based on current state:
- Stage 1 completed: "Recommend proceeding to Stage 2 (WRITE) using {recommended_mode} mode"
- Stage 2 completed: "Recommend proceeding to Stage 2.5 (INTEGRITY) before peer review"
- Stage 3 completed (Major): "Need to enter Stage 4 (REVISE), {N} required items"
- Stage 4 completed: "Recommend proceeding to Stage 3' (RE-REVIEW) to confirm revision quality"
- Stage 3' completed (Accept): "Proceed to Stage 4.5 (FINAL INTEGRITY) before Stage 5 finalization"
- Stage 3' completed (Minor Revision): "Record per-item edit locations or signed retention rationales, then proceed to Stage 4.5 (FINAL INTEGRITY)"
- Stage 4.5 completed (PASS): "Confirm final submission checkpoint, then proceed to Stage 5 (FINALIZE)"
- Pipeline completed: "Pipeline complete! Final paper is ready (Stage 6 Process Summary optional)."

---

## Simplified Version (Auto-appended after stage completion)

One-line progress bar (following the ten-stage table):

```
Pipeline: [v]1 RESEARCH -> [v]2 WRITE -> [v]2.5 INTEGRITY -> [..]3 REVIEW -> [ ]4 REVISE -> [ ]3' RE-REVIEW -> [ ]4' RE-REVISE -> [ ]4.5 FINAL INTEGRITY -> [ ]5 FINALIZE -> [--]6 SUMMARY
```
