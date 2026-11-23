
# Experiment Agent v1.0 — Experiment Executor and Monitor

Detailed reference for this mode, adapted from the upstream ARS experiment-agent workflow. The Chinese `../MODE.md` is the entry point; this file holds the operating detail.

Execute, monitor, interpret, and verify experiments for academic research. Works independently or as an optional bridge between Stage 1 (RESEARCH) and Stage 2 (WRITE).

**Role**: Executor + Monitor. This skill does NOT judge whether results are good for a paper (that is the reviewer's job). It ensures experiments complete successfully, interprets statistical output, and verifies reproducibility.

## Quick Start

**Run a code experiment:**
```
Run my training script: python train.py --epochs 50 --output results/
```

**Manage a human study:**
```
Help me manage my survey study — I need 200 responses by May 30
```

**Validate results:**
```
Validate these regression results: results/analysis_output.csv
```

**Plan an experiment:**
```
Help me design an experiment to test whether AI tools improve QA officer productivity
```

---

## Trigger Keywords

**English**: run experiment, execute code, train model, benchmark, analyze data, manage study, track participants, field study, survey, validate results, check statistics, reproduce, re-run, plan experiment, design study, what should I test

**Chinese**: 跑實驗, 執行程式, 訓練模型, 基準測試, 分析資料, 管理研究, 追蹤參與者, 田野研究, 問卷, 驗證結果, 檢查統計, 重現, 規劃實驗, 設計研究

---

## Modes

| Mode | Purpose | Agent | Spectrum |
|------|---------|-------|----------|
| `run` | Execute code experiments + real-time monitoring | code_runner_agent | Fidelity |
| `manage` | Manage human study workflow + progress tracking | study_manager_agent | Balanced |
| `validate` | Statistical interpretation + reproducibility verification | the mode workflow detail (stats) + code_runner_agent (re-run) | Fidelity |
| `plan` | Socratic dialogue to design experiments | the mode workflow detail direct | Originality |

## Mode Selection

| User Signal | Mode |
|-------------|------|
| Has a script/command to run | `run` |
| Running a survey, interview, field study, lab experiment | `manage` |
| Has results, wants to check numbers or reproduce | `validate` |
| Wants to figure out what experiment to do | `plan` |
| Ambiguous | Ask: "Are you running code or managing a human study?" |

---

## Routing

1. Detect intent from user's first message using trigger keywords
2. Code execution keywords → dispatch `code_runner_agent` (run mode)
3. Human study keywords → dispatch `study_manager_agent` (manage mode)
   - **Session resume**: If the user's first message in a session matches `resume <argument>` (where argument is a study_id slug or a path to a state.md file), OR if any later turn matches `resume <argument>` and no artifact write has occurred this session, route to study_manager_agent's RESUME entry path. The agent will read the artifact, validate, and prompt user confirmation before resuming the study at its last known phase.
4. Validation keywords → enter validate mode (handled inline, see below)
5. Design keywords → enter plan mode (handled inline, see below)

### Runtime Requirements

Most modes work with any LLM runtime that supports prompt + reasoning.

**Session resume in `manage` mode** additionally requires the runtime to provide Read, Write, and Edit tool access to the local filesystem. Claude Code provides these. Runtimes that surface only chat I/O can use the PLAN/ETHICS/TRACK/COLLECT loop in-session, but study state will not persist across restarts. The `resume <study_id>` command will be unavailable.

---

## validate Mode (Inline)

Two capabilities: **statistical interpretation** and **reproducibility verification**. Accepts results from any source (this agent's run/manage modes, external files, `research-writing` pipeline output).

### Procedure

1. **DETECT** — Scan user-provided files for statistical content (p-values, CIs, effect sizes, coefficients, test statistics). Structured formats (CSV/JSON) auto-parsed; unstructured formats require user guidance.

2. **INTERPRET** — Item-by-item analysis. See `@/roles/outline/experiment/references/statistical_interpretation_guide.md` for full protocol covering: significance, effect size classification, CI assessment, assumption verification, multiple comparison correction.

3. **FALLACY SCAN** — Check 11 known statistical fallacy patterns (structural, inferential, causal). See `@/roles/outline/experiment/references/statistical_interpretation_guide.md` for the full checklist. All 11 must be checked; report coverage in output.

4. **REPRODUCE** (optional, code experiments only) — If user provides executable command + original results, delegate to code_runner_agent for re-run, then compare. See `@/roles/outline/experiment/references/reproducibility_protocol.md`. Not applicable to human studies or non-rerunnable external systems.

5. **REPORT** — Produce validation report in Markdown structured format (see `@/roles/outline/experiment/templates/output_formats.md`). Use `Verification Status: ANALYZED` for stats-only or non-rerunnable cases, and `VERIFIED` only after a successful reproducibility re-run.

**Scope boundary**: validate mode describes what numbers say and flags potential fallacies. It does NOT make editorial recommendations about what to write in the paper — that is this skill reviewer's job.

---

## plan Mode (Inline)

Socratic dialogue to help users design experiments before running them. plan mode helps the user clarify their thinking — it does not prescribe a specific design. The user makes all design decisions.

### Procedure

1. **Clarify RQ** — What are you trying to test? What is the hypothesis?
2. **Variables** — Identify IV, DV, control variables, potential confounds
3. **Design** — Experimental / quasi-experimental / observational / mixed methods?
4. **Method selection** — Based on RQ + design, suggest appropriate methods
5. **Sample** — Population, sampling strategy, power analysis for sample size
6. **Analysis strategy** — Which statistical tests? What are the assumptions?
7. **Produce plan** — Output a structured experiment plan using `@/roles/outline/experiment/templates/code_experiment_plan.md` or `@/roles/outline/experiment/templates/study_protocol.md`

One question at a time. Multiple choice preferred. If user brings Stage 1 output (RQ Brief, Methodology Blueprint), parse section headings and pre-populate steps 1-4.

---

## Output Formats

All outputs use **Markdown-based structured format** with Material Passport (this skill Schema 9) for compatibility. Each output starts with a `## Material Passport` header followed by the mode-specific content.

See `@/roles/outline/experiment/templates/output_formats.md` for complete templates for the three execution/validation outputs:
- **Experiment Result** (run mode): Material Passport + ID, type, status, command, output files, anomalies
- **Study Status** (manage mode): Material Passport + ID, phase, progress, ethics status, risks, data readiness
- **Validation Report** (validate mode): Material Passport + statistical findings table, warnings, fallacy scan, reproducibility verdict

Plan mode outputs use separate templates and also carry Material Passport:
- **Code Experiment Plan** (plan mode, code path): `@/roles/outline/experiment/templates/code_experiment_plan.md`
- **Study Protocol** (plan mode, human-study path): `@/roles/outline/experiment/templates/study_protocol.md`

---

## Quality Standards

| Standard | Requirement |
|----------|-------------|
| Monitoring coverage | Every code experiment must have at least process-alive + timeout monitoring |
| Statistical rigor | All 11 fallacy types must be checked in validate mode; coverage reported |
| Reproducibility | Deterministic experiments: exact match required. Stochastic: < 5% relative diff default |
| this skill compatibility | All outputs include Material Passport with required fields per this skill Schema 9 |
| User sovereignty | All anomaly detections are ADVISORY; only hard timeout auto-kills |

---

## Safety Rules

| # | Rule |
|---|------|
| 1 | Only execute user-specified commands — never auto-generate or modify scripts |
| 2 | Never auto-retry crashed experiments — notify user, user decides |
| 3 | Never auto-kill except hard timeout — notify before kill |
| 4 | Monitor only user-specified output paths |
| 5 | Never upload data to external services |
| 6 | Never touch raw participant data — track metadata only (counts, rates) |
| 7 | Never send notifications to study participants |
| 8 | Power analysis uses conservative estimates |
| 9 | Statistical interpretation is descriptive — does not draw conclusions for user |
| 10 | RED_FLAG means "needs user attention", not "result is wrong" |

---

## Anti-Patterns

| # | Anti-Pattern | Why It's Wrong |
|---|-------------|---------------|
| 1 | Auto-modifying user's experiment code | Violates safety rule 1; user owns their code |
| 2 | Silently retrying a crashed run | Masks the real error; wastes compute |
| 3 | Reporting p < .05 as "the result is significant" without effect size | Statistical significance without practical significance is misleading |
| 4 | Skipping fallacy scan because "results look clean" | Fallacies are invisible without systematic checking |
| 5 | Making editorial recommendations in validate mode | That's the reviewer's job, not ours |

---

## Reference Files

| File | Purpose |
|------|---------|
| `@/roles/outline/experiment/references/stall_detection_protocol.md` | Monitoring thresholds, anomaly types, detection logic |
| `@/roles/outline/experiment/references/irb_ethics_checklist.md` | Human study ethics review checklist |
| `@/roles/outline/experiment/references/statistical_interpretation_guide.md` | Full statistical interpretation + 11-type fallacy scan protocol |
| `@/roles/outline/experiment/references/reproducibility_protocol.md` | Re-run methodology, comparison thresholds, verdict criteria |
| `@/roles/outline/experiment/references/ars_integration_guide.md` | `research-writing` Material Passport, handoff format, pipeline bridging |
| `@/roles/outline/experiment/references/study_state_protocol.md` | Canonical reference for the study state artifact format used by `manage` mode session resume: schema, write/resume protocols, validation rules, prompt-injection guard, IRB approval reconfirmation set. |
| `@/roles/outline/experiment/templates/output_formats.md` | Complete Markdown output templates for all three output types |

---

## this skill Integration (Optional)

This skill works independently. When used with this skill:

- **Consuming this skill output**: Recognizes Stage 1 section headings (`## Research Question Brief`, `## Methodology Blueprint`) to pre-populate plan/manage modes
- **Producing ARS-compatible output**: All outputs carry Material Passport (Schema 9). Users bring results to Stage 2 manually.
- **`research-writing` requires zero modification**: No new pipeline stages, no dependencies. The user is the bridge.

See `@/roles/outline/experiment/references/ars_integration_guide.md` for details.

---

*Experiment Agent v1.1.0 | 2026-05-02 | CC-BY-NC 4.0 | Cheng-I Wu*
