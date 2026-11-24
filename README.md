# Research Skill Bundles

English | [中文](README.zh.md)

Distributable agent skills for research, organised into two packs.

| Pack | Use it for |
| --- | --- |
| [Research Writing](skills/research-writing/) | Scientific papers end to end. The `research-writing` skill combines Paper Orchestra, ARS, Nature Skills and K-Dense into six roles (orchestrate, outline, literature, figures, draft, review). Seven standalone skills cover proposals, slides, patents, literature feeds and lab logs. |
| [Research Engineering](skills/research-engineering/) | Scientific software: MATLAB/Octave, SymPy, units and uncertainty, GPU optimisation, multi-objective optimisation, machine learning, statistical models, and GitHub Actions diagnosis. |

## Use a pack

Copy the skill directories you need from a pack's `skills/` into your agent's skill location, keeping every file inside each directory. `research-writing` registers as a single skill; call it as `$research-writing <role> [mode]`, for example `$research-writing full` or `$research-writing review panel`. Its [skill map](skills/research-writing/skills/research-writing/references/skill-map.md) lists every mode.

### Prompts for an agent to import the packs

Send either prompt to your agent (e.g. Codex or Claude Code). Replace the repository URL with a local path if you already cloned it, and keep only `research-writing` or `research-engineering` if you do not need both.

**Project-level import (current project only)**

```text
Import the research skill packs from https://github.com/AmazingUmi/codex-research-bundles into this project's project-level skills directory (use your host's project skills path, such as .agents/skills/, .codex/skills/, or .claude/skills/):
1. Fetch the repository (or ask me for a local path if network access is unavailable) and copy all skill directories under skills/research-writing/skills/ and skills/research-engineering/skills/ (or only the specific skills I name; include nature-shared whenever importing any standalone nature-* skill).
2. Copy each directory containing SKILL.md intact with all subdirectories and files. Do not rename skill directories, and do not flatten or separately register internal role/mode files inside research-writing.
3. Check for existing skill directories with the same name before writing, and ask for confirmation before overwriting any conflict.
4. Verify that every installed skill directory has a readable SKILL.md, then report the exact install path and list of imported skills.
```

**Global import (available across all projects)**

```text
Import the research skill packs from https://github.com/AmazingUmi/codex-research-bundles into my user-level global skills directory (use your host's global skills path, such as ~/.agents/skills/, ~/.codex/skills/, or ~/.claude/skills/):
1. Fetch the repository (or ask me for a local path if network access is unavailable) and copy all skill directories under skills/research-writing/skills/ and skills/research-engineering/skills/ (or only the specific skills I name; include nature-shared whenever importing any standalone nature-* skill).
2. Copy each directory containing SKILL.md intact with all subdirectories and files. Do not rename skill directories, and do not flatten or separately register internal role/mode files inside research-writing.
3. Check for existing skill directories with the same name before writing, and ask for confirmation before overwriting any conflict.
4. Verify that every installed skill directory has a readable SKILL.md, then report the exact install path and list of imported skills.
```

The [usage guide (Chinese)](doc/usage.md) includes prompts for entering a writing stage, resuming a run, and using individual roles, along with the workflow and skill trees.

If you share a pack, keep its license and notice files together with the matching entries in [SOURCES.md](skills/SOURCES.md), which records upstream revisions, local changes and license scope.

## License

Documentation authored in this repository is available under [Apache-2.0](LICENSE). The `research-writing` skill is distributed under CC BY-NC 4.0 (non-commercial) because it includes adapted ARS material. Other skills keep their component licenses. See [SOURCES.md](skills/SOURCES.md) for each component's terms.
