# 能力清单

`research-writing` 的全部模式、来源，以及重叠能力的取舍。调用方式：`$research-writing <角色> [模式]`。

## 按角色

| 角色 | 模式 | 目录 | 来源 |
| --- | --- | --- | --- |
| 编排 | `full`、`resume` | `roles/orchestrate/` | Paper Orchestra 整稿流程 + ARS academic-pipeline |
| 大纲 | 默认（主张与证据表、任务卡） | `roles/outline/ROLE.md` | Paper Orchestra |
| | `socratic` | `outline/socratic/` | ARS deep-research |
| | `plan`、`outline-only` | `outline/plan/` | ARS academic-paper |
| | `design` | `outline/design/` | K-Dense experimental-design |
| | `appraise` | `outline/appraise/` | K-Dense scientific-critical-thinking |
| | `experiment`（`plan`、`run`、`manage`、`validate`） | `outline/experiment/` | ARS experiment-agent |
| 文献 | `verify`（默认） | `roles/literature/ROLE.md` | Paper Orchestra |
| | `search` | `literature/search/` | Nature academic-search（含 MCP server） |
| | `fulltext` | `literature/fulltext/` | Nature downloader |
| | `paper-card` | `literature/paper-card/` | Nature paper-card |
| | `read` | `literature/read/` | Nature reader |
| | `ref-verify` | `literature/ref-verify/` | Nature ref-verifier |
| | `cns-cite` | `literature/cns-cite/` | Nature citation |
| | `citation-check` | `literature/citation-check/` | ARS academic-paper |
| | `lit-review`、`systematic-review`、`fact-check`、`three-way-scan`、`deep`、`brief` | `literature/research/` | ARS deep-research |
| | `screen`（8 个子模式） | `literature/screen/` | ARS sr-screener |
| 图表 | `make`（默认） | `figures/make/` | Nature figure；`make/ars-visualization/` 来自 ARS academic-paper |
| | `audit` | `figures/audit/` | K-Dense scientific-visualization |
| 正文 | `section`（默认） | `draft/section/` | Nature writing |
| | `full`、`abstract`、`disclosure`、`format-convert` | `draft/paper/` | ARS academic-paper |
| | `polish` | `draft/polish/` | Nature polishing |
| | `stats-report` | `draft/stats-report/` | Nature statistics |
| | `analysis` | `draft/analysis/` | K-Dense statistical-analysis |
| | `data-availability` | `draft/data-availability/` | Nature data |
| 审稿 | `panel`、`methodology`、`guided`、`re-review` | `review/panel/` | ARS academic-paper-reviewer |
| | `nature` | `review/nature/` | Nature reviewer |
| | `respond` | `review/respond/` | Nature response |
| | `revision-coach`、`rebuttal-audit` | `review/revision-coach/` | ARS academic-paper |
| | `revise` | `review/revise/` + `review/ROLE.md` | Paper Orchestra；严格模式补丁来自 ARS |

角色负责范围、输入、验收、证据状态和交接；模式负责执行。模式交回的结果先由所属角色验收，再进入下一步。

## 重叠能力的取舍

| 任务 | 采用 | 说明 |
| --- | --- | --- |
| 核对一条引文 | 文献 `verify` | 查原文是否支持这句话 |
| 核对参考文献列表 | 文献 `ref-verify` | 逐字段核对书目信息 |
| 核对引文格式与对应 | 文献 `citation-check` | 查格式、正文与列表的对应 |
| 检索 | 文献 `search` | 研究模式检索时也调用它 |
| 综述 | 文献 `lit-review`；系统综述用 `systematic-review` | ARS academic-paper 的 `lit-review` 未保留 |
| 写章节 | 正文 `section` | 正文角色只验收与写入 |
| 写整稿 | 正文 `full` | 由编排角色调用时作为阶段 2 的一种走法 |
| 统计 | 报告与审查用 `stats-report`，新计算用 `analysis` | |
| 出图与审图 | 生成用 `make`，审查用 `audit` | 一张图只用一个模式生成 |
| 模拟审稿 | 多席位与编辑决定用 `panel`；按 Nature 标准用 `nature` | ARS 审稿团自带的 `quick` 未保留 |
| 回复与返修 | 回复信 `respond`；路线图 `revision-coach`；核对回复 `rebuttal-audit`；改稿 `revise` | ARS academic-paper 的 `revision` 并入 `revise` |
| 研究问题 | 大纲 `socratic` | ARS academic-paper 的 Socratic mentor 只用于 `plan` |
| 研究设计 | 方法学设计 `design`；实验执行与管理 `experiment` | |

## 默认模式与严格模式

默认模式只依靠提示约束和证据矩阵（见[交接约定](handoff.md)）。严格模式启用 ARS 的合约与校验脚本：

| 角色 | 严格模式内容 | 文件 |
| --- | --- | --- |
| 审稿 | 两次调用的 sprint contract、席位执行来源记录、re-review 三道门合约 | `review/panel/strict/` |
| 审稿 | 补丁式改稿 | `review/revise/references/revision_patch_protocol.md` |
| 正文 | 生成—评估合约 | `draft/paper/strict/` |
| 编排 | Material Passport、断点重置、引文来源终审 | `orchestrate/strict/` |
| 共用 | 交接 schema、合约模板、校验脚本 | `engine/` |

严格模式脚本需要 Python 3 与 `engine/requirements.txt` 中的依赖。

## 不在本技能中的能力

| 能力 | 去处 |
| --- | --- |
| 研究计划、开题报告、项目申请书 | 独立技能 `nature-proposal-writer` |
| 论文汇报 PPT、图片转 PPT | 独立技能 `nature-paper2ppt`、`nature-image2ppt` |
| 专利交底书 | 独立技能 `nature-paper-to-patent` |
| 定时文献推送 | 独立技能 `nature-literature-pipeline` |
| 实验日志整理 | 独立技能 `nature-experiment-log`，产出可作为大纲角色的输入 |
| 符号计算、MATLAB、单位与不确定度 | Research Engineering 的 `sympy`、`matlab`、`uncertainty-and-units` |

上游 ARS 中删除的部分：评测与测试、发布工具、审稿人校准模式、跨模型验证、模型分级、审稿目标标准绑定、跨运行裁决记录、调查分支账本、Claude/Codex 运行时适配层。
