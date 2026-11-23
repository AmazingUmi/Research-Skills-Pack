# Mode Advisor — Unified Cross-Skill Decision Tree

## Purpose

Helps users (and the pipeline orchestrator) select the right skill and mode for their current situation. Eliminates the most common routing mistakes by mapping user intent to the optimal entry point.

---

## Quick Decision Matrix

| What do you want? | How far along? | Time? | Skill + Mode |
|-------------------|---------------|-------|--------------|
| Explore a topic | Starting fresh | 30 min | the literature role quick |
| Explore a topic | Starting fresh | 2+ hr | the literature role full |
| Think through a research idea | Have vague idea | Any | the literature role socratic |
| Systematic review | Have clear PICO | 3+ hr | the literature role systematic-review |
| Verify claims | Have specific claims | 30 min | the literature role fact-check |
| Write a paper | Have research done | 2+ hr | the draft role full |
| Plan a paper step by step | Have RQ, need structure | 1+ hr | the draft role plan |
| Fix citations | Have draft | 30 min | the draft role citation-check |
| Convert format | Have final draft | 15 min | the draft role format-convert |
| Review a paper | Have paper to evaluate | 1 hr | the review panel full |
| Check revision quality | Have revised draft | 30 min | the review panel re-review |
| Full pipeline (zero to publication) | Starting fresh | 5+ hr | the orchestrate role |
| Handle real reviewer feedback | Have review comments | 1+ hr | the orchestrate role (Stage 4 entry) |

---

## Common Misconceptions

| User Says | They Probably Need | Why |
|-----------|-------------------|-----|
| "Write me a paper on X" | the literature role first, THEN the draft role | Writing without research produces shallow papers with unsupported claims |
| "Review my paper" (but no draft exists) | the draft role plan mode | They need to write first, not review |
| "Check my citations" (but paper isn't done) | the draft role full mode | Finish writing first, then check citations as a separate pass |
| "I need a systematic review" | the literature role systematic-review mode | NOT the draft role lit-review structure (different methodology: PRISMA vs narrative) |
| "Just give me a quick paper" | the literature role quick + the draft role full | Quick research is fine, but paper writing still needs the full mode for quality |
| "Format my paper as APA" | the draft role format-convert mode | Not a rewrite; purely formatting transformation |
| "I got reviewer comments" | the orchestrate role Stage 4 entry (External Review) | Needs structured intake + strategic coaching, not just "fix what they said" |

---

## User Archetype Recommendations

| Archetype | Recommended Workflow | Rationale |
|-----------|---------------------|-----------|
| Graduate student (first paper) | the literature role socratic -> the draft role plan -> full pipeline | Socratic mode builds research thinking; plan mode structures the paper incrementally; pipeline ensures quality gates |
| Experienced researcher (submission prep) | the orchestrate role (full, from Stage 1 or mid-entry) | Knows what they want; benefits from the automated quality assurance and integrity checks |
| Advisor reviewing student work | the review panel full | Provides structured multi-perspective feedback the advisor can use in mentoring |
| Quick literature scan | the literature role quick or lit-review | Fast turnaround; no need for full pipeline overhead |
| Journal revision response | the orchestrate role (Stage 4 entry with review comments) | External Review Protocol handles real reviewer feedback with strategic coaching |
| Conference paper (short deadline) | the literature role quick -> the draft role full (conference type) | Compressed timeline; quick research + full writing with conference structure |
| Thesis chapter | the literature role full -> the draft role full | Each chapter treated as a standalone paper; full depth needed |
| Policy brief | the literature role quick -> the draft role full (policy_brief type) | Evidence-based but concise; quick research sufficient for policy scope |

---

## Skill Capability Boundaries

Understanding what each skill can and cannot do prevents misrouting:

| Skill | Can Do | Cannot Do |
|-------|--------|-----------|
| the literature role | Literature search, synthesis, RQ refinement, fact-checking | Write papers, review papers, format documents |
| the draft role | Write papers, revise papers, format documents, check citations | Conduct original research, review papers (as reviewer), verify integrity |
| the review panel | Review papers (5-person panel), re-review revisions | Write papers, conduct research, fix issues (only identifies them) |
| the orchestrate role | Orchestrate all stages, manage transitions, track state | Perform any substantive work (purely dispatching and coordinating) |
| integrity_verification_agent | Verify references, citations, data, originality | Fix issues (only identifies them), review paper quality |

---

## Decision Flowchart

```
START: What does the user want?
  |
  +--> "I want to research/explore/investigate"
  |      |
  |      +--> Have specific claims to verify? --> literature fact-check
  |      +--> Have clear PICO/systematic question? --> literature systematic-review
  |      +--> Want guided exploration? --> literature socratic
  |      +--> Want direct results, have time? --> literature full
  |      +--> Want direct results, short on time? --> literature quick
  |
  +--> "I want to write a paper"
  |      |
  |      +--> Have research/literature ready? --> draft (plan or full)
  |      +--> No research done yet? --> literature FIRST, then draft
  |      +--> Want full quality assurance? --> orchestrate (from Stage 1)
  |
  +--> "I want someone to review my paper"
  |      |
  |      +--> Have a complete draft? --> review panel full
  |      +--> Want integrity check + review? --> orchestrate (Stage 2.5 entry)
  |      +--> No draft yet? --> draft first
  |
  +--> "I need to revise based on feedback"
  |      |
  |      +--> From AI reviewers (pipeline)? --> Continue pipeline (Stage 4)
  |      +--> From real journal reviewers? --> orchestrate Stage 4 entry (External Review)
  |
  +--> "I want the full treatment (research to publication)"
         |
         +--> orchestrate (Stage 1 entry)
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
