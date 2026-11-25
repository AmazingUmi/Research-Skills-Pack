# Stage 6: Process Summary Protocol (Added in v2.4)

**Trigger**: After the user confirms the Stage 5 completion checkpoint (FULL). Stage 6 is non-mandatory — the user may decline it at that checkpoint; it is then marked `skipped` and the pipeline still terminates `completed` (see `pipeline_state_machine.md` § Stage 6 terminal semantics)
**Purpose**: Document the complete human-AI collaboration history for the paper creation process, for user sharing, reporting, or reflection

## Workflow

```
1. Ask user language preference:
   "Which language version of the process record would you like to generate first?"
   - Chinese (Simplified or Traditional, matching the author’s manuscript)
   - English
   - Both (default: generate the user's primary conversation language first)
   Ask in the same question whether to add a PDF. An active standing constraint
   that answers either point is followed without asking (pipeline orchestrator
   § Standing Constraints).

2. Review session history and compile the following (after a reset boundary the
   session holds only the turns since the last resume: take earlier decisions and
   words from the passport and run ledger, and say in the record which parts come
   from those rather than the conversation):
   - User's initial instructions (verbatim quote)
   - Key decision points and user interventions at each stage
   - Direction correction moments and reasons
   - Iteration count and review result summaries
   - Intellectual insights raised by the user (e.g., questions that spawned new chapters)
   - Quality requirement evolution (e.g., formatting, tone adjustments)
   - Pipeline statistics (stage count, review rounds, integrity verification count, etc.)

2b. Include an AI self-reflection or author-requested feedback only if selected
    separately. Ground feedback in particular decisions and their effects.
    A process record alone does not request an evaluation of the author.

3. Generate Markdown version (paper_creation_process.md / paper_creation_process_en.md)

4. Only when a PDF was asked for, convert to LaTeX and compile PDF:
   - pandoc MD -> LaTeX body
   - Package complete LaTeX document (with cover page, table of contents, headers/footers)
   - tectonic compile PDF
   - Use a CJK-capable engine and an installed SC or TC font matching the chosen script.

5. Terminal acknowledgement (pipeline terminal checkpoint):
   - After delivering the process record, prompt the user to close the pipeline.
   - Acknowledgement vocabulary: "finish" / "end" / "done" / "confirm", or an
     unambiguous natural-language equivalent that accepts the deliverables.
   - Change requests (the other language version, content corrections) keep
     Stage 6 in_progress — they are not acknowledgements.
   - On acknowledgement: state_tracker marks Stage 6 completed and sets the pipeline global state to completed. There is no next stage.
     (See pipeline_state_machine.md § Stage 6 terminal semantics.)
```

## Required Content in Process Record

| Section | Content |
|---------|---------|
| Paper Information | Title, final deliverables list |
| Stage-by-Stage Process | Input/output/key decisions for each stage, with verbatim user quotes |
| Iteration Details | Review comment summaries, revision items, re-review results |
| Interaction Pattern Summary | User role, AI role, intervention count, key turning points — statistics table |
| User Key Decisions | Chronological list of every important decision made by the user |
| Key Lessons | Reusable lessons learned from the process |

## Optional reflection and feedback

On request, the AI may describe its own errors, corrective actions, and unresolved checks. Separately, the author may request feedback on particular collaboration decisions or choose the depth rubric. Specify which observations came from the current session and which came from a recorded checkpoint.

## Output Specifications

- **Filename**: `paper_creation_process.md` (Chinese) / `paper_creation_process_en.md` (English)
- **PDF** (when asked for): `paper_creation_process_zh.pdf` / `paper_creation_process_en.pdf`
- **LaTeX template**: `article` class, 12pt, A4, Times New Roman plus an installed CJK font for the selected SC or TC script
- **Includes table of contents**: `\tableofcontents`
- **Header**: left = document title (italic), right = date
- **Compilation**: tectonic (same toolchain as Stage 5)
