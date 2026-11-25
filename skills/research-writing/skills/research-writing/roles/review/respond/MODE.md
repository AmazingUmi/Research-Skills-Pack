<!-- Mode file: review/respond. Ported from Nature Skills `nature-response`; loaded by the research-writing router, not registered as a skill. -->

# Nature Reviewer Response — Router

## Routing protocol

For a new task, load the core and matching resources below. Reuse already loaded guidance on follow-ups; load more only when the task needs it.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). Then read every file listed under `always_load`:

- `static/core/stance.md` — the editor-facing purpose, the default stance, the red lines, and the source hierarchy that apply to every response job.
- `static/core/workflow.md` — accepted inputs, the revision correspondence workflow, and the output package format.

### 2. No content axis — identify mode and language inline

Unlike `$research-writing draft section` or `$research-writing figures make`, this mode has no fragment axis. Its variation is identified at runtime, not by loading different content bodies:

- **correspondence task** — `draft` / `revise` (revise an existing response) / `cover-letter` / `revision-package` / `latex-template` / `appeal-like`.
- **decision type** — minor revision, major revision, revise-and-resubmit, transfer after review, or unclear.
- **user language** — if the user writes Chinese, also produce the 中文核对 block.

Decision type is required for a new package-level revision strategy or complete response package.
First extract it from the editor letter or task context. If it remains unclear, ask whether this
is a `Major Revision` or `Minor Revision` and pause only decision-dependent work. A local wording
edit, audit of an existing reply, or comment-level triage may proceed with decision type marked
unknown. Do not infer the decision from the number, tone, or difficulty of reviewer comments.

Use `references/intake-and-routing.md` to fix the task mode, minimum inputs, and readiness state before drafting. Route appeal-like cases separately; do not draft an appeal as the default path.

For a local edit, return the requested passage. For an audit or triage request, return the specialist findings and relevant missing facts. Do not expand it into a master tracker, cover letter, or complete revision package unless
requested. Apply the package workflow below only to the parts needed for the requested output.

### 3. Run the workflow

Route review of an existing response to `review rebuttal-audit` and comment triage to `review revision-coach` before executing the drafting workflow. Draft or edit replies under the strategy and changes the author confirmed.

In an orchestrated Stage 4, `review revise` writes the manuscript. Use its revised version and change record to write the response and, when requested, produce a marked copy against the baseline. Send further manuscript changes back to `review revise`. When called on its own, edit the manuscript alongside the response if the user requests both. Keep the baseline and use a single manuscript writer.

Follow the workflow in `static/core/workflow.md`: if the user pasted a journal email, first parse manuscript metadata, decision type, editor instructions, reviewer reports, required files, deadlines, and reviewer-visibility rules from the email; identify mode and pass the decision-type gate; apply the Major- or Minor-Revision strategy without downgrading the severity of individual comments; extract editor instructions (IDs `E.1`) then reviewer comments (`R1.1`, `R2.1`) when present; classify each item by response action and independently verified work status; build an internal/editor master strategy and tracker; draft a standalone privacy-filtered response for each mutually blind reviewer; when a reviewer missed material already present in the manuscript, flag the clarity issue and suggest a targeted fix or apply it within the editing scope above; draft a revision cover letter when required; map every claimed change to a manuscript location or explicit placeholder; mark changed manuscript text in red on a backed-up copy when editing; format quoted revised manuscript text in the response letter in italics; flag missing author input; run QA; and derive package readiness from the per-item statuses and blocking state.

Whenever a response proposes or performs a manuscript main-text edit, also load
`@/references/nature-shared/core/main-text-discipline.md`. Answer the reviewer completely
in the letter, but keep the manuscript change to the shortest text needed for
the reader. Prefer replacement or compression over appending, and route
non-central robustness or reconciliation detail to SI unless it changes the
central interpretation.

Never invent experiments, citations, line numbers, figure panels, supplementary items, editor instructions, or manuscript changes. Mark anything the author must supply as `AUTHOR_INPUT_NEEDED`.

### 4. Reach for references only when needed

The files under `references/` and `templates/` are deep resources, not defaults. Open them on demand per the `references.on_demand` table in the manifest — for example `references/comment-taxonomy.md` to classify comments, `references/action-mapping.md` for tracker fields, `references/tone-and-stance.md` for disagreement wording, `references/difficult-cases.md` for impossible experiments / conflicting reviewers / appeal-like cases, `references/chinese-author-alignment.md` for Chinese author notes, `references/latex-templates.md` for `.tex` cover/response/redline outputs, `@/references/nature-shared/core/main-text-discipline.md` for reviewer-driven manuscript additions and evidence relocation, `references/package-consistency-audit.md` whenever the manuscript is edited alongside the letter or the package is about to be compiled and delivered, and `references/qa-checklist.md` before finalizing.

`qa-checklist.md` and `package-consistency-audit.md` are complementary and both apply to a final package: the first asks whether the response is complete, honest, and well-toned; the second asks whether the marked manuscript, the clean manuscript, and the letter actually agree with each other after editing. For a LaTeX package, run `scripts/check_package_consistency.py` after the first complete draft, after every manuscript edit, and immediately before delivery. Any manuscript edit invalidates the letter's verbatim quotes and page references, so re-run the audit rather than treating it as a one-time final check.
