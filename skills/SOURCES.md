# Sources and licenses · 来源与许可证

本表记录分发包中的来源版本和本地改动。许可证正文和版权声明随各 pack 保存。技能版本来自上游元数据，快照版本由仓库提交标识。

2026-11-22 核对上游版本。ARS-Codex 和 K-Dense 采用当时的正式发布，Nature 和 GitHub CI 采用各自默认分支的固定提交。Paper Orchestra 的参考提交为 Google 上游当时的默认分支 HEAD。

## Writing

### Paper Orchestra

- 路径：[skills/writing/paper-orchestra](writing/paper-orchestra/)。
- 本地改编版本为 `v0.2.0`。包含一个编排入口和五个角色，可按写作阶段调用 `packs/` 下的 Nature、K-Dense Writing 和 ARS-Codex。三套子 pack 的版本和许可证分别列于下文。
- 参考来源：[google-research/paper-orchestra](https://github.com/google-research/paper-orchestra/tree/d9bae997e793a015ed38bb1605be9eb58c00284f)，提交 `d9bae997e793a015ed38bb1605be9eb58c00284f`。
- 许可证：上游与本地改编均为 Apache-2.0。随包提供 [LICENSE](writing/paper-orchestra/LICENSE) 和 [NOTICE](writing/paper-orchestra/NOTICE)。

### ARS-Codex

- 路径：[skills/writing/paper-orchestra/packs/ars-codex](writing/paper-orchestra/packs/ars-codex/)。
- 来源：[Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex/tree/82725acb393c4410ac6f47634a7f51b40a162fa4)，`v3.24.2`，提交 `82725acb393c4410ac6f47634a7f51b40a162fa4`。
- 收录 `skills/academic-research-suite/` 完整独立 Skill，并保留上游 `VERSION`、`CITATION.cff` 和许可。技能文件与固定提交一致。内部 ARS 来自 [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills/tree/fd5ff1b858374219b4d342e38587b66e18f61cbd) 的 `fd5ff1b858374219b4d342e38587b66e18f61cbd`。
- 许可证：ARS-Codex [LICENSE](writing/paper-orchestra/packs/ars-codex/LICENSE) 为 CC BY-NC 4.0，随内置工作流一同保留嵌套的许可和声明。

### Nature

- 路径为 [skills/writing/paper-orchestra/packs/nature](writing/paper-orchestra/packs/nature/README.md)
- 上游为 [Yuan1z0825/nature-skills@c6701db](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5)，2026-11-22 核对默认分支 `main` 的提交 `c6701dbea29afa7c596d029b957b7edc92130ea5`。固定提交覆盖本 pack 原选的 20 项技能。版本来自该提交的各技能 `manifest.yaml`，单项许可见表。
- `nature-image2ppt` 的组件上游是 [Paul-Jeo/Image2PPT@3bcedf4](https://github.com/Paul-Jeo/Image2PPT/tree/3bcedf41a277a3a4ae8024f6030437930c969d30)，由 Nature 源码清单记录。
- 分发时将上游 `nature-proposal-writer` 目录命名为 `researchwrite`，使路径和既有技能名一致。保留 `nature-paper-card` 双语教程和技能所需的 `nature-shared`。`nature-academic-search` 的上游 Claude Code 安装脚本不随 pack 分发，检索技能、工具说明和可选 MCP 源码均保留。
- `nature-figure` 随包保留自带的图表库和本地实现。上游曾附带的 `figures4papers` 预览与脚本改为外部参考，因所固定快照的[历史权属声明](writing/paper-orchestra/packs/nature/notices/figures4papers-upstream-notice.md)没有确认再分发许可。本地 README 和示例索引已经更新。`nature-reviewer` 中复制的出版方编辑流程正文改为简要说明及[出版方原文链接](https://www.nature.com/nature/for-authors/editorial-criteria-and-processes)。

| 技能 | 源路径 | 版本 | 许可证 / 声明 |
| --- | --- | --- | --- |
| `nature-academic-search` | [skills/nature-academic-search](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-academic-search) | 2.0.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-citation` | [skills/nature-citation](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-citation) | 2.1.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-data` | [skills/nature-data](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-data) | 2.2.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-downloader` | [skills/nature-downloader](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-downloader) | 2.1.0 | [MIT](writing/paper-orchestra/packs/nature/skills/nature-downloader/LICENSE) (baihe26) |
| `nature-experiment-log` | [skills/nature-experiment-log](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-experiment-log) | 1.0.2 | [MIT](writing/paper-orchestra/packs/nature/notices/MIT.txt) (SKILL.md 声明，Jiahao8595) |
| `nature-figure` | [skills/nature-figure](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-figure) | 2.8.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE)，外部示例见上述说明 |
| `nature-image2ppt` | [skills/nature-image2ppt](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-image2ppt) | 1.1.0 | [MIT](writing/paper-orchestra/packs/nature/skills/nature-image2ppt/LICENSE) (Image2PPT contributors、ningzimu) |
| `nature-literature-pipeline` | [skills/nature-literature-pipeline](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-literature-pipeline) | 1.0.1 | [MIT](writing/paper-orchestra/packs/nature/notices/MIT.txt) (SKILL.md 声明，Jiahao8595) |
| `nature-paper-card` | [skills/nature-paper-card](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-paper-card) | 1.2.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-paper-to-patent` | [skills/nature-paper-to-patent](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-paper-to-patent) | 1.0.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE)，`references/disclosure/` 保留 [MIT 通知](writing/paper-orchestra/packs/nature/skills/nature-paper-to-patent/references/disclosure/patent-disclosure-skill-MIT-LICENSE.txt) |
| `nature-paper2ppt` | [skills/nature-paper2ppt](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-paper2ppt) | 2.0.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-polishing` | [skills/nature-polishing](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-polishing) | 6.6.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-reader` | [skills/nature-reader](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-reader) | 2.1.0（SKILL.md 标注 2.1.1） | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-ref-verifier` | [skills/nature-ref-verifier](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-ref-verifier) | 1.0.1 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-response` | [skills/nature-response](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-response) | 1.7.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-reviewer` | [skills/nature-reviewer](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-reviewer) | 1.5.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-shared` | [skills/nature-shared](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-shared) | 1.6.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-statistics` | [skills/nature-statistics](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-statistics) | 1.3.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `nature-writing` | [skills/nature-writing](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-writing) | 1.5.0 | [Apache-2.0](writing/paper-orchestra/packs/nature/LICENSE) |
| `researchwrite` | [skills/nature-proposal-writer](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-proposal-writer) | 1.1.1 | [MIT](writing/paper-orchestra/packs/nature/notices/MIT.txt) (SKILL.md 声明) |

## K-Dense 科研技能

[Writing](writing/paper-orchestra/packs/k-dense-writing/) · [Engineering Core](engineering/k-dense-core/) · [Engineering Extensions](engineering/k-dense-extensions/)

三个包取自 [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360) 的 [`v2.72.0` 发行版](https://github.com/K-Dense-AI/scientific-agent-skills/releases/tag/v2.72.0)，提交 `526ebce143bc326f44471554e33d66a19c840360`。每个技能目录复制自该提交的 `skills/<名称>/`，目录内容未改动。表中的技能版本来自各自的 `SKILL.md`。Writing 与 Engineering Core 共有的技能采用同一快照。

| 技能 | 包 | 技能版本 | 许可证 |
| --- | --- | --- | --- |
| [`matlab`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/matlab) | Writing、Core | `1.4` | MIT |
| [`sympy`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/sympy) | Writing、Core | `1.5` | BSD-3-Clause（[上游技能指向 SymPy](https://github.com/sympy/sympy/blob/master/LICENSE)） |
| [`statistical-analysis`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/statistical-analysis) | Writing、Core | `2.0` | MIT |
| [`uncertainty-and-units`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/uncertainty-and-units) | Writing、Core | `1.3` | MIT |
| [`scientific-critical-thinking`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/scientific-critical-thinking) | Writing、Core | `1.5` | MIT |
| [`scientific-visualization`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/scientific-visualization) | Writing、Core | `1.4` | MIT |
| [`experimental-design`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/experimental-design) | Writing | `1.5` | MIT |
| [`optimize-for-gpu`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/optimize-for-gpu) | Extensions | `1.6` | MIT |
| [`pymoo`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/pymoo) | Extensions | `1.6` | Apache-2.0 |
| [`scikit-learn`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/scikit-learn) | Extensions | `1.5` | BSD-3-Clause |
| [`pytorch-lightning`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/pytorch-lightning) | Extensions | `1.4` | Apache-2.0 |
| [`statsmodels`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/statsmodels) | Extensions | `1.5` | BSD-3-Clause |

各包的 `licenses/` 收录 [K-Dense 上游 MIT 文本及版权声明](https://github.com/K-Dense-AI/scientific-agent-skills/blob/526ebce143bc326f44471554e33d66a19c840360/LICENSE.md)。相应包也附带 [Apache-2.0 全文](https://www.apache.org/licenses/LICENSE-2.0.txt)及 [SymPy 1.14.0](https://github.com/sympy/sympy/blob/sympy-1.14.0/LICENSE)、[scikit-learn 1.9.1](https://github.com/scikit-learn/scikit-learn/blob/1.9.1/COPYING)、[statsmodels 0.15.0](https://github.com/statsmodels/statsmodels/blob/v0.15.0/LICENSE.txt) 的 BSD-3-Clause 文本和原版权声明。

实验设计技能可按需配合 `statistical-power` 做样本量和功效估算，批判性思维技能可用 `scientific-schematics` 生成示意图，需专门处理 PyMC 建模时可用 `pymc` 技能。这些可选技能由 Agent 另行获取。

## Engineering

### GitHub CI

[Pack](engineering/github-ci/)

| Skill | Source | Version | License |
| --- | --- | --- | --- |
| `gh-fix-ci` | [openai/skills, `skills/.curated/gh-fix-ci/`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci) | Git commit `49f948faa9258a0c61caceaf225e179651397431` | [Apache-2.0](engineering/github-ci/skills/gh-fix-ci/LICENSE.txt) |

完整保留上游技能目录，包括入口、Python 脚本、Agent 元数据和两张图标。
