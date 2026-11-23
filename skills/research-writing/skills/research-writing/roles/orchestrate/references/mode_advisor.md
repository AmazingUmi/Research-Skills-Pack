# Mode Advisor — Unified Cross-Skill Decision Tree

## Purpose

Helps users (and the pipeline orchestrator) select the right skill and mode for their current situation. Eliminates the most common routing mistakes by mapping user intent to the optimal entry point.

---

## Quick Decision Matrix

| What do you want? | How far along? | Time? | Role + Mode (`$research-writing ...`) |
|-------------------|---------------|-------|---------------------------------------|
| Explore a topic quickly | Starting fresh | 30 min | `literature brief` |
| Explore a topic in depth | Starting fresh | 2+ hr | `literature deep` |
| Think through a research idea | Have vague idea | Any | `outline socratic` |
| Systematic review | Have clear PICO | 3+ hr | `literature systematic-review` |
| Verify claims | Have specific claims | 30 min | `literature fact-check` (or `literature verify` for a few citations) |
| Write a paper | Have research done | 2+ hr | `draft full` (or `draft section` for specific sections) |
| Plan a paper step by step | Have RQ, need structure | 1+ hr | `outline plan` (or `outline outline-only`) |
| Fix citations | Have draft | 30 min | `literature citation-check` (or `literature ref-verify` for bibliography fields) |
| Convert format | Have final draft | 15 min | `draft format-convert` |
| Review a paper | Have paper to evaluate | 1 hr | `review panel` (or `review nature`) |
| Check revision quality | Have revised draft | 30 min | `review re-review` |
| Full pipeline (zero to publication) | Starting fresh | 5+ hr | `orchestrate full` (or `$research-writing full`) |
| Handle real reviewer feedback | Have review comments | 1+ hr | `orchestrate full` (Stage 4 entry) or `review revision-coach` / `review respond` |

---

## Common Misconceptions

| User Says | They Probably Need | Why |
|-----------|-------------------|-----|
| "Write me a paper on X" | `literature` first, THEN `draft` | Writing without research produces shallow papers with unsupported claims |
| "Review my paper" (but no draft exists) | `outline plan` | They need a structured plan and draft first, not review |
| "Check my citations" (but paper isn't done) | `draft full` (or `draft section`) | Finish writing first, then check citations as a separate pass |
| "I need a systematic review" | `literature systematic-review` | NOT a narrative `literature lit-review` (different methodology: PRISMA vs narrative) |
| "Just give me a quick paper" | `literature brief` + `draft full` | Brief research is fine, but paper writing still needs `draft full` for quality |
| "Format my paper as APA" | `draft format-convert` | Not a rewrite; purely formatting transformation |
| "I got reviewer comments" | `orchestrate` Stage 4 entry (or `review revision-coach` → `review revise` → `review respond`) | Needs structured intake + strategic coaching, not just "fix what they said" |

---

## User Archetype Recommendations

| Archetype | Recommended Workflow | Rationale |
|-----------|---------------------|-----------|
| Graduate student (first paper) | `outline socratic` -> `outline plan` -> `orchestrate full` | Socratic mode builds research thinking; plan mode structures the paper incrementally; pipeline ensures quality gates |
| Experienced researcher (submission prep) | `orchestrate full` (from Stage 1 or mid-entry) | Knows what they want; benefits from the automated quality assurance and integrity checks |
| Advisor reviewing student work | `review panel` | Provides structured multi-perspective feedback the advisor can use in mentoring |
| Quick literature scan | `literature brief` or `literature lit-review` | Fast turnaround; no need for full pipeline overhead |
| Journal revision response | `orchestrate` (Stage 4 entry) or `review revision-coach` + `review respond` | External Review Protocol handles real reviewer feedback with strategic coaching |
| Conference paper (short deadline) | `literature brief` -> `draft full` (conference type) | Compressed timeline; brief research + full writing with conference structure |
| Thesis chapter | `literature deep` -> `draft full` | Each chapter treated as a standalone paper; full depth needed |
| Policy brief | `literature brief` -> `draft full` (policy_brief type) | Evidence-based but concise; brief research sufficient for policy scope |

---

## Role Capability Boundaries

Understanding what each role can and cannot do prevents misrouting:

| Role | Can Do | Cannot Do |
|------|--------|-----------|
| `outline` | RQ refinement (`socratic`), chapter planning (`plan`, `outline-only`), study design (`design`), evidence appraisal (`appraise`), experiment management (`experiment`) | Draft final prose, conduct full multi-seat peer review |
| `literature` | Multi-source search, fulltext retrieval, reading, verification, citation & reference checks, literature/systematic reviews, screening | Write manuscript body, review papers, format final submission files |
| `figures` | Generate figures (`make`), audit figures (`audit`), captions | Write body prose, conduct peer review |
| `draft` | Draft sections/full manuscripts, polish, statistical reporting/analysis, data availability, AI disclosure, format conversion | Conduct original peer review, verify end-to-end integrity independently |
| `review` | Multi-seat peer review (`panel`, `methodology`, `guided`, `re-review`, `nature`), revision roadmaps (`revision-coach`), rebuttal audit (`rebuttal-audit`), responses (`respond`), authorized edits (`revise`) | Conduct initial literature research from scratch |
| `orchestrate` | Orchestrate all stages, manage checkpoints and handoffs, track state | Perform any substantive writing or review work (purely dispatching and coordinating) |
| `integrity_verification_agent` | Verify references, citations, data, originality, claims | Fix issues (only identifies them), replace peer review |

---

## Decision Flowchart

```
START: What does the user want?
  |
  +--> "I want to research/explore/investigate"
  |      |
  |      +--> Have specific claims to verify? --> literature fact-check (or literature verify)
  |      +--> Have clear PICO/systematic question? --> literature systematic-review
  |      +--> Want guided exploration of a vague idea? --> outline socratic
  |      +--> Want direct results, have time? --> literature deep
  |      +--> Want direct results, short on time? --> literature brief
  |
  +--> "I want to write a paper"
  |      |
  |      +--> Need chapter plan / outline first? --> outline plan (or outline outline-only)
  |      +--> Have research/literature ready? --> draft full (or draft section)
  |      +--> No research done yet? --> literature FIRST, then draft
  |      +--> Want full quality assurance? --> orchestrate full (from Stage 1)
  |
  +--> "I want someone to review my paper"
  |      |
  |      +--> Have a complete draft? --> review panel (or review nature)
  |      +--> Want integrity check + review? --> orchestrate (Stage 2.5 entry)
  |      +--> No draft yet? --> outline / draft first
  |
  +--> "I need to revise based on feedback"
  |      |
  |      +--> From AI reviewers (pipeline)? --> Continue pipeline (Stage 4: review revise)
  |      +--> From real journal reviewers? --> orchestrate Stage 4 entry (or review revision-coach / review respond)
  |
  +--> "I want the full treatment (research to publication)"
         |
         +--> orchestrate full (Stage 1 entry)
```

---

## Pipeline Stage Entry Points

For users entering the pipeline mid-stream, this table clarifies what materials are needed:

| Entry Point | Required Materials | What Gets Skipped | Integrity Implications |
|------------|-------------------|-------------------|----------------------|
| Stage 1 (RESEARCH) | None | Nothing | Full pipeline |
| Stage 2 (WRITE) | RQ Brief + Bibliography | Stage 1 | Full pipeline from Stage 2 |
| Stage 2.5 (INTEGRITY) | Paper draft | Stages 1-2 | Integrity check runs on provided draft |
| Stage 3 (REVIEW) | Paper draft (a prior integrity report is optional context) | Stages 1-2 | Stage 2.5 runs first on the provided paper; a prior report informs it but does not replace it |
| Stage 4 (REVISE) | Paper + review comments | Stages 1-3 | Pipeline runs Stage 4 -> 3' -> 4.5 -> 5; Stage 4' runs between 3' and 4.5 only after a Major decision |
| Stage 5 (FINALIZE) | Revised paper (a prior integrity report is optional context) | Stages 1-4 | Stage 4.5 runs first on the provided paper; a prior report informs it but does not replace it |

---

## Anti-Patterns

These are common workflow mistakes to avoid:

| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|-----------------|
| Skipping research | Paper lacks evidence depth | Always do at least the literature role quick |
| Writing then researching | Confirmation bias in source selection | Research first, write second |
| Reviewing before integrity check | Wasted review effort on fabricated citations | Always Stage 2.5 before Stage 3 |
| Accepting all reviewer comments blindly | May introduce inconsistencies or weaken valid arguments | Use External Review Protocol's strategic coaching |
| Running pipeline for a 1-page abstract | Overhead far exceeds benefit | Use the draft role full directly |
| Using fact-check mode for literature review | Different purpose and methodology | Use the literature role full or systematic-review |
