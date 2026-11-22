# figures4papers Reference Index

<!-- Pack change: reference the external demo repository and preserve local fallbacks. -->

Use this file when a user asks for a `figures4papers` look, cites the older
`scientific-figure-making` skill, or needs a concrete Python/matplotlib reference.

This pack links to the [figures4papers project](https://github.com/ChenLiu-1996/figures4papers)
for optional external examples. Check the terms of the revision consulted. For
local work, use the bundled examples and reference files listed below.

## Use boundary

1. Study layout, palette, axes, legends, and export structure as reference patterns.
2. Reimplement with original code and the user's own data whenever the upstream
   license or written permission does not clearly authorize copying or modification.
3. Never reuse manuscript-specific labels, metric values, statistical results, or
   visual assets as placeholders for real evidence.
4. Record the external reference and implementation provenance in the internal QA
   record when it materially influenced the result.
5. Preserve the editable SVG/PDF/TIFF and source-data rules from `api.md` and
   `qa-contract.md`.

## External project map

| Project | Open when |
|---------|-----------|
| `figure_ImmunoStruct` | Method-comparison and ablation bars |
| `figure_CellSpliceNet` | Compact benchmark and cross-species bars |
| `figure_brainteaser` | Category, rewriting, and self-correction panels |
| `figure_VIGIL` | Radar, trend, ablation, and probability/manifold panels |
| `figure_ophthal_review` | Time trends and composition heatmaps |
| `figure_RNAGenScape` | Heatmaps, optimization, manifold, and sweep plots |
| `figure_Dispersion` | Conceptual sphere and observation panels |
| `figure_Cflows` | Diffusion, trajectory, comparison, and ablation panels |
| `figure_FPGM` | Frequency-prior or distribution-style motivation |

## Prefer repository-owned implementation paths

When copying is not clearly authorized, route the pattern through the repository's
own material:

| Requested pattern | Open and use |
|-------------------|--------------|
| Grouped bars, ablation bars, shared legends | `tutorials.md`, `common-patterns.md` |
| Radar or polar comparison | `chart-types.md`, then implement with original code |
| Trends, sweeps, and reference baselines | `tutorials.md`, `chart-types.md` |
| Heatmap or annotated matrix | `tutorials.md`, `template-catalog.md` |
| Probability or manifold concept panel | `chart-types.md` |
| Submission typography, palette, and export | `api.md`, `design-theory.md` |
| CSV-driven reproducible plots | `template-catalog.md`, `scripts/plot_templates.py` |

## Upstream source

<https://github.com/ChenLiu-1996/figures4papers>

Check the current upstream license and obtain permission when required before
redistributing, modifying, or publishing derived materials.
