# `nature-shared/` - shared support package for nature-* skills

Install next to `nature-paper2ppt`. The merged `research-writing` skill uses
its embedded copy. Entries below also identify the corresponding writing modes.

## Contents

| File | Consumers |
|---|---|
| `core/reader-workflow.md` | `research-writing draft polish`, `research-writing draft section` |
| `core/paper-type-taxonomy.md` | `research-writing draft polish`, `research-writing draft section` |
| `core/ethics.md` | `research-writing draft polish`, `research-writing draft section` |
| `core/research-compliance.md` | `research-writing draft section` and skills needing Nature Portfolio specialist compliance checks |
| `core/terminology-ledger.md` | `research-writing draft polish`, `research-writing draft section`, `research-writing literature read`, `nature-paper2ppt` |
| `core/consistency-sweep.md` | `research-writing draft polish`, `research-writing review nature`, `research-writing review respond`, `research-writing draft stats-report` |
| `core/main-text-discipline.md` | `research-writing draft section`, `research-writing draft polish`, `research-writing review respond` |
| `core/nature-results-discussion.md` | Nature / Nature Portfolio Results claim escalation and Discussion synthesis for `research-writing draft section` and `research-writing draft polish`, distilled from published NMI and flagship Nature papers (not official policy) |
| `core/discussion-argument-language.md` | Journal-general Discussion functions, reverse-funnel control, evidence-calibrated modality, claim boundaries, and future-work auditing for `research-writing draft section` and `research-writing draft polish` (writing guidance, not journal policy) |
| `core/nature-introduction.md` | Nature / Nature Portfolio problem funnels, exact gaps, and Introduction–Results alignment for `research-writing draft section` and `research-writing draft polish`, initially distilled from NMI papers (not official policy) |
| `core/nature-abstract.md` | Nature / Nature Portfolio discovery-centred abstract evidence chains, claim hierarchy, and numeric selection for `research-writing draft section` and `research-writing draft polish`, initially distilled from NMI papers (not official policy) |
| `journal-formats/nat-comms.md` | `research-writing draft polish`, `research-writing draft section` |
| `journal-formats/nature.md` | `research-writing draft section` and skills needing exact flagship `Nature Article` submission rules |
| `journal-formats/nature-machine-intelligence.md` | Writing, polishing, figure, data, and statistics workflows for NMI submissions |

`scripts/check_consistency.py` provides a mechanical first pass for terminology variants, equal values reported at different precision, and equivalent lengths expressed in different units. Its output is a set of warnings for contextual review, not automatic edits.

## When to Put Files Here

Only place a file here when two or more skills need to reuse the same content. If the content serves only one skill, keep it in that skill's own `static/` or `references/` directory.

## When to Keep Content Local

The shared layer should hold definitions and references only, such as paper-type classifications, reader workflows, ethics rules, or terminology ledgers. Skill-specific diagnosis, drafting, modification, and output logic should remain in each skill's own files.

## Relationship With Other Skills

`nature-shared/` is not a standalone workflow. It is a shared dependency package that other `nature-*` skills read on demand.
