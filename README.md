# Codex Research Skill Bundles

English | [中文](README.zh.md)

A distributable collection of skill files for research and scientific software projects.

| List | Use it for |
| --- | --- |
| [Writing](skills/WRITING.md) | Paper Orchestra leads manuscript work and calls on the bundled Nature, K-Dense Writing, and ARS-Codex packs as needed. |
| [Engineering](skills/ENGINEERING.md) | Scientific software development, numerical methods, validation, performance checks, and optional GitHub Actions diagnosis. |

## Use a pack

To run a manuscript workflow, give your agent access to the [Paper Orchestra pack](skills/writing/paper-orchestra/) and open [the main skill](skills/writing/paper-orchestra/skills/paper-orchestra/SKILL.md). For a single operation, you can open the relevant specialist's `SKILL.md` directly.

For recurring use, import complete skill directories from the pack's `skills/` and any selected child pack's `skills/` into your agent's supported skill location. Keep the six Paper Orchestra skill directories alongside one another and preserve their references, scripts, and assets. When two packs include the same skill, import one copy.

Each pack documents its scope and runtime requirements. If you share an individual pack, include its license and notice files and the matching entries from [SOURCES.md](skills/SOURCES.md). That file records upstream revisions, skill versions, local changes, and license scope.

## License

The documentation and selection lists authored in this repository and the local Paper Orchestra adaptation are available under [Apache-2.0](LICENSE). Bundled third-party materials retain their component licenses and notices, including CC BY-NC 4.0 for ARS-Codex. See [sources and licenses](skills/SOURCES.md) for the terms of each pack.
