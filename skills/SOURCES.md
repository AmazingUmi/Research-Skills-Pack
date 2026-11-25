# Sources and licenses · 来源与许可证

本文件记录各技能的上游版本、合并方式与许可证。许可证正文与版权声明随各 pack 保存。

2026-11-22 核对上游版本。ARS-Codex 与 K-Dense 采用当时的正式发布，Nature Skills 与 GitHub CI 采用各自默认分支的固定提交，Paper Orchestra 采用 Google 上游当时默认分支的 HEAD。2026-11-23 将写作侧的四个来源合并为 `research-writing` 技能。

2026-11-25 根据包审阅修订角色交接、质检、实验与分发。每个可安装技能的 `NOTICE` 附固定来源，相关许可证随技能目录复制。

## Research Writing

路径：[skills/research-writing](research-writing/)。

### research-writing（合并技能）

- 路径：[skills/research-writing/skills/research-writing](research-writing/skills/research-writing/)。只注册这一个技能，内部按编排、大纲、文献、图表、正文、审稿六个角色组织，角色下再分模式。模式与来源的对应见[能力清单](research-writing/skills/research-writing/references/skill-map.md)。
- 许可证：整体按 [CC BY-NC 4.0](research-writing/LICENSE) 分发，因为包含改编自 ARS 的内容。各来源的许可文本与署名见 [NOTICE](research-writing/NOTICE) 和 [licenses/](research-writing/licenses/)。
- 合并时的共同改动：
  - 内容按角色与模式重新归位，文件位置、交叉引用和交接字段都已改写；入口 `SKILL.md`、各角色 `ROLE.md` 和 ARS 来源模式的 `MODE.md` 为新写的中文文件。Nature 与 K-Dense 来源模式的 `MODE.md` 由原 `SKILL.md` 改名而来，保留上游结构，并按本包的目标语言、证据范围和角色权限调整执行规则。
  - 角色与模式文件不命名为 `SKILL.md`，不会被单独注册。
  - 文中以 `@/` 开头的路径以 `research-writing` 技能根目录为基准。

#### Paper Orchestra

- 参考来源：[google-research/paper-orchestra](https://github.com/google-research/paper-orchestra/tree/d9bae997e793a015ed38bb1605be9eb58c00284f)，提交 `d9bae997e793a015ed38bb1605be9eb58c00284f`，Apache-2.0（[licenses/Apache-2.0-PaperOrchestra.txt](research-writing/licenses/Apache-2.0-PaperOrchestra.txt)）。
- 本地改编 `v0.2.0` 的编排入口与五个角色成为合并技能的骨架：角色正文保留，新增模式表与验收规则；原 `references/workflow.md` 并入编排角色。

#### ARS-Codex

- 来源：[Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex/tree/82725acb393c4410ac6f47634a7f51b40a162fa4) `v3.24.2`，提交 `82725acb393c4410ac6f47634a7f51b40a162fa4`；内部 ARS 来自 [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills/tree/fd5ff1b858374219b4d342e38587b66e18f61cbd)，提交 `fd5ff1b858374219b4d342e38587b66e18f61cbd`。CC BY-NC 4.0，引用信息见 [licenses/ARS-CITATION.cff](research-writing/licenses/ARS-CITATION.cff)。
- 归位：deep-research → 文献 `research/` 与大纲 `socratic/`；academic-paper → 正文 `paper/`、大纲 `plan/`、文献 `citation-check/`、审稿 `revision-coach/`、图表 `make/ars-visualization/`；academic-paper-reviewer → 审稿 `panel/`；academic-pipeline → 编排；sr-screener → 文献 `screen/`；experiment-agent → 大纲 `experiment/`；shared → `references/` 与 `engine/`。各 workflow 原文清理后保存为对应目录的 `references/workflow_detail.md`。
- 默认模式与严格模式：sprint contract、生成—评估合约、re-review 三道门合约、Material Passport 与断点重置等机制移入各角色的 `strict/` 目录，只在严格模式下使用；默认模式改用证据矩阵。
- 删除：evals、tests、plugin-evals、audits、docs、tools、hooks、pi、commands、多语言 README、Codex 运行时适配层，以及审稿人校准模式、跨模型验证、模型分级、审稿目标标准绑定、跨运行裁决记录、调查分支账本、ARS 审稿团的 `quick`、academic-paper 的 `lit-review` 与 `revision`。路由核心的重复副本、版本与 issue 编号注记、设计文档链接也已去掉。
- 脚本：只保留文档引用的脚本及其 import 依赖闭包，放在 `engine/scripts/`（75 个），路径改为新布局；评测、发布、文档同步检查与已删除功能的脚本没有保留；维护用的 `stage_capability_matrix.json` 与 1.0 版 re-review 合约也已删除。第三方依赖见 [engine/requirements.txt](research-writing/skills/research-writing/engine/requirements.txt)。JSON schema 的 `$id` 与 `$ref` 保持上游原样（脚本按 `$id` 解析引用）；描述文字中的 issue 编号已去掉。被脚本锁定哈希的 `contracts/reviewer/full.json` 与 `preregistration_template.md` 未改动，`check_v3_9_4_temporal_verification.py` 对 `bibliography_agent.md` 的哈希锁已更新为合并后的基线。
- 环境变量：严格模式脚本读取的变量统一改为 `RW_` 前缀（如 `RW_PASSPORT_RESET`、`RW_CACHE_DIR`）；已删除功能的变量（跨模型、旧版复审、探针等）一并去掉。

#### Nature Skills（写作类）

- 上游：[Yuan1z0825/nature-skills@c6701db](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5)。版本来自该提交的各技能 `manifest.yaml`。
- 13 个写作类技能并入 `research-writing` 的模式目录，`nature-shared` 移到 `references/nature-shared/`。保留 `manifest.yaml` 与 `static/` 结构（`always_load` 指向 `MODE.md`）；删除各技能的 README、`agents/`、`evals/`、`tests/`。`nature-downloader` 的 README 改名为 `SETUP.md`。
- `nature-figure` 保留自带的图表库；上游曾附带的 `figures4papers` 预览与脚本改为外部参考，原因见[历史权属声明](research-writing/licenses/figures4papers-upstream-notice.md)。`nature-reviewer` 中复制的出版方编辑流程正文改为简要说明与[出版方原文链接](https://www.nature.com/nature/for-authors/editorial-criteria-and-processes)。`nature-academic-search` 的上游 Claude Code 安装脚本不随包分发。

#### K-Dense（写作类）

见下方 K-Dense 一节。四个技能并入 `research-writing` 的模式目录，原 `SKILL.md` 改名为 `MODE.md`，跨技能引用改为对应模式，并适配事前功效分析、审图与工具引用的交接方式。

### 独立技能

`nature-proposal-writer`、`nature-paper2ppt`、`nature-image2ppt`、`nature-paper-to-patent`、`nature-literature-pipeline`、`nature-experiment-log` 与 `nature-shared` 保持为独立技能，位于 [skills/research-writing/skills](research-writing/skills/)，不适用 CC BY-NC 4.0。`nature-proposal-writer` 沿用上游目录名；它曾以 `researchwrite` 分发，为避免与 `research-writing` 混淆已改回上游名，并删除了 SKILL.md 与 manifest 中关于旧名的说明。

2026-11-24 的本地修订还调整了独立技能的文献纳入与空白判断、开题 QA 范围和专利 Word 导出结果。合并技能同步调整整稿入口、引文与原创证据核查、系统综述筛选报告及复审交接。下表版本号标识引用的上游版本。

### Nature Skills 逐项

| 技能 | 现在的位置 | 源路径 | 版本 | 许可证 / 声明 |
| --- | --- | --- | --- | --- |
| `nature-academic-search` | literature `search` | [skills/nature-academic-search](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-academic-search) | 2.0.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-citation` | literature `cns-cite` | [skills/nature-citation](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-citation) | 2.1.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-data` | draft `data-availability` | [skills/nature-data](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-data) | 2.2.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-downloader` | literature `fulltext` | [skills/nature-downloader](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-downloader) | 2.1.0 | [MIT](research-writing/skills/research-writing/roles/literature/fulltext/LICENSE) (baihe26) |
| `nature-experiment-log` | 独立技能 | [skills/nature-experiment-log](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-experiment-log) | 1.0.2 | [MIT](research-writing/licenses/MIT-Nature-contributors.txt) (SKILL.md 声明，Jiahao8595) |
| `nature-figure` | figures `make` | [skills/nature-figure](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-figure) | 2.8.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt)，外部示例见上述说明 |
| `nature-image2ppt` | 独立技能 | [skills/nature-image2ppt](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-image2ppt) | 1.1.0 | [MIT](research-writing/skills/nature-image2ppt/LICENSE) (Image2PPT contributors、ningzimu) |
| `nature-literature-pipeline` | 独立技能 | [skills/nature-literature-pipeline](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-literature-pipeline) | 1.0.1 | [MIT](research-writing/licenses/MIT-Nature-contributors.txt) (SKILL.md 声明，Jiahao8595) |
| `nature-paper-card` | literature `paper-card` | [skills/nature-paper-card](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-paper-card) | 1.2.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-paper-to-patent` | 独立技能 | [skills/nature-paper-to-patent](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-paper-to-patent) | 1.0.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt)，`references/disclosure/` 保留 [MIT 通知](research-writing/skills/nature-paper-to-patent/references/disclosure/patent-disclosure-skill-MIT-LICENSE.txt) |
| `nature-paper2ppt` | 独立技能 | [skills/nature-paper2ppt](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-paper2ppt) | 2.0.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-polishing` | draft `polish` | [skills/nature-polishing](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-polishing) | 6.6.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-reader` | literature `read` | [skills/nature-reader](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-reader) | 2.1.0（SKILL.md 标注 2.1.1） | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-ref-verifier` | literature `ref-verify` | [skills/nature-ref-verifier](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-ref-verifier) | 1.0.1 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-response` | review `respond` | [skills/nature-response](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-response) | 1.7.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-reviewer` | review `nature` | [skills/nature-reviewer](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-reviewer) | 1.5.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-shared` | `references/nature-shared/`，并在独立技能中保留一份 | [skills/nature-shared](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-shared) | 1.6.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-statistics` | draft `stats-report` | [skills/nature-statistics](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-statistics) | 1.3.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-writing` | draft `section` | [skills/nature-writing](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-writing) | 1.5.0 | [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt) |
| `nature-proposal-writer` | 独立技能 | [skills/nature-proposal-writer](https://github.com/Yuan1z0825/nature-skills/tree/c6701dbea29afa7c596d029b957b7edc92130ea5/skills/nature-proposal-writer) | 1.1.1 | [MIT](research-writing/licenses/MIT-Nature-contributors.txt)（开题技能）。本包另从 `nature-paper-to-patent` 引入 [Word 公式转换脚本](research-writing/skills/nature-proposal-writer/scripts/math_to_omml.py)，该脚本沿用 [Apache-2.0](research-writing/licenses/Apache-2.0-Nature.txt)。 |

`nature-image2ppt` 的组件上游是 [Paul-Jeo/Image2PPT@3bcedf4](https://github.com/Paul-Jeo/Image2PPT/tree/3bcedf41a277a3a4ae8024f6030437930c969d30)，由 Nature 源码清单记录。

## K-Dense 科研技能

取自 [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360) 的 [`v2.72.0` 发行版](https://github.com/K-Dense-AI/scientific-agent-skills/releases/tag/v2.72.0)，提交 `526ebce143bc326f44471554e33d66a19c840360`。每个技能只放在一处：写作类并入 `research-writing`，其余在 Research Engineering。Research Engineering 保留上游目录名与兼容性说明，`statsmodels`、`uncertainty-and-units` 的跨包调用指向本包实际入口。

| 技能 | 现在的位置 | 技能版本 | 许可证 |
| --- | --- | --- | --- |
| [`matlab`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/matlab) | Research Engineering | `1.4` | MIT |
| [`sympy`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/sympy) | Research Engineering | `1.5` | BSD-3-Clause（[上游技能指向 SymPy](https://github.com/sympy/sympy/blob/master/LICENSE)） |
| [`statistical-analysis`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/statistical-analysis) | research-writing · draft `analysis` | `2.0` | MIT |
| [`uncertainty-and-units`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/uncertainty-and-units) | Research Engineering | `1.3` | MIT |
| [`scientific-critical-thinking`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/scientific-critical-thinking) | research-writing · outline `appraise` | `1.5` | MIT |
| [`scientific-visualization`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/scientific-visualization) | research-writing · figures `audit` | `1.4` | MIT |
| [`experimental-design`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/experimental-design) | research-writing · outline `design` | `1.5` | MIT |
| [`optimize-for-gpu`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/optimize-for-gpu) | Research Engineering | `1.6` | MIT |
| [`pymoo`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/pymoo) | Research Engineering | `1.6` | Apache-2.0 |
| [`scikit-learn`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/scikit-learn) | Research Engineering | `1.5` | BSD-3-Clause |
| [`pytorch-lightning`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/pytorch-lightning) | Research Engineering | `1.4` | Apache-2.0 |
| [`statsmodels`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/526ebce143bc326f44471554e33d66a19c840360/skills/statsmodels) | Research Engineering | `1.5` | BSD-3-Clause |

许可文本：[Research Writing](research-writing/licenses/K-Dense-MIT.md)、[Research Engineering](research-engineering/licenses/)（K-Dense MIT、Apache-2.0、SymPy 1.14.0、scikit-learn 1.9.1、statsmodels 0.15.0 的 BSD-3-Clause 原文与版权声明）。

`experimental-design`、`scientific-critical-thinking`、`statistical-analysis` 提到的 `statistical-power`、`scientific-schematics`、`pymc` 等技能不随包分发，需要时另行获取。

## Research Engineering

路径：[skills/research-engineering](research-engineering/)。原 K-Dense Core、K-Dense Extensions 与 GitHub CI 三个子包已打平到同一个 `skills/` 目录。

| Skill | Source | Version | License |
| --- | --- | --- | --- |
| `gh-fix-ci` | [openai/skills, `skills/.curated/gh-fix-ci/`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci) | Git commit `49f948faa9258a0c61caceaf225e179651397431` | [Apache-2.0](research-engineering/skills/gh-fix-ci/LICENSE.txt) |

保留上游入口、Python 脚本、Agent 元数据和两张图标。已修订跨仓查询和按作业提取日志。
