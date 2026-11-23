# Research Skill Bundles

English | [中文](README.zh.md)

Distributable agent skills for research, organised into two packs.

| Pack | Use it for |
| --- | --- |
| [Research Writing](skills/research-writing/) | Scientific papers end to end. The `research-writing` skill combines Paper Orchestra, ARS, Nature Skills and K-Dense into six roles (orchestrate, outline, literature, figures, draft, review). Seven standalone skills cover proposals, slides, patents, literature feeds and lab logs. |
| [Research Engineering](skills/research-engineering/) | Scientific software: MATLAB/Octave, SymPy, units and uncertainty, GPU optimisation, multi-objective optimisation, machine learning, statistical models, and GitHub Actions diagnosis. |

## Use a pack

Copy the skill directories you need from a pack's `skills/` into your agent's skill location, keeping every file inside each directory. `research-writing` registers as a single skill; call it as `$research-writing <role> [mode]`, for example `$research-writing full` or `$research-writing review panel`. Its [skill map](skills/research-writing/skills/research-writing/references/skill-map.md) lists every mode.

If you share a pack, keep its license and notice files together with the matching entries in [SOURCES.md](skills/SOURCES.md), which records upstream revisions, local changes and license scope.

## License

Documentation authored in this repository is available under [Apache-2.0](LICENSE). The `research-writing` skill is distributed under CC BY-NC 4.0 (non-commercial) because it includes adapted ARS material. Other skills keep their component licenses. See [SOURCES.md](skills/SOURCES.md) for each component's terms.
