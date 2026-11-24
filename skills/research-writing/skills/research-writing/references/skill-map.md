# 能力清单

`research-writing` 注册一个技能。角色按整稿阶段承担任务，各模式按 `$research-writing <角色> [模式]` 调用。阶段的主责、触发条件和交付物由[整稿编排](../roles/orchestrate/ROLE.md)规定。

## 按角色

| 角色 | 模式 | 用途与交付 | 来源 |
| --- | --- | --- | --- |
| [编排 `orchestrate`](../roles/orchestrate/ROLE.md) | `full`、`resume` | `full` 调度阶段、两次完整性核查和作者检查点，汇总终稿与可选过程记录。`resume` 从同次流程的有效断点续接 | Paper Orchestra 整稿流程 + ARS academic-pipeline |
| [大纲 `outline`](../roles/outline/ROLE.md) | 不带模式的组稿调用 | 阶段 2 输出大纲、主张与证据表、文献检索单和图件任务卡 | Paper Orchestra |
| | `socratic` | 把未成形的题目收敛为研究问题和计划摘要 | ARS deep-research |
| | `plan`、`outline-only` | 逐章讨论计划，或一次交付详细大纲与证据地图 | ARS academic-paper |
| | `design`、`appraise` | 设计研究方案，或评估已有证据的强度、偏倚与支持范围 | K-Dense experimental-design、scientific-critical-thinking |
| | `experiment`（`plan`、`run`、`manage`、`validate`） | 规划、执行、管理或验证实验，交付过程和结果记录 | ARS experiment-agent |
| [文献 `literature`](../roles/literature/ROLE.md) | `verify` | 检查所引原文能否支持指定主张，交回可用引文和待核项 | Paper Orchestra |
| | `search`、`fulltext` | 检索候选来源，按需取得可访问的全文或补充材料 | Nature academic-search（含可选 MCP）、downloader |
| | `paper-card`、`read` | 拆解单篇论文的方法和证据，或按实际阅读范围做对照精读 | Nature paper-card、reader |
| | `ref-verify`、`citation-check`、`cns-cite` | 依次检查书目字段、正文和文末格式对应、按用户指定的 Nature/CNS 范围找引文 | Nature ref-verifier、ARS academic-paper、Nature citation |
| | `deep`、`brief`、`lit-review` | 完整研究报告、研究简报或文献综述，按阶段 1 的研究目标选择 | ARS deep-research |
| | `systematic-review`、`screen` | 处理明示的系统综述或文献筛选任务。`screen` 有 8 个子模式，可独立拟协议、筛选、裁决和复核，也可从既有判定生成计数 | ARS deep-research、sr-screener |
| | `fact-check`、`three-way-scan` | 逐条核查事实，或按研究问题、方法与结论比较候选论文 | ARS deep-research |
| [图表 `figures`](../roles/figures/ROLE.md) | `make`、`audit` | `make` 生成图表、图注和可复核材料。`audit` 检查现有图件并给出问题与修法 | Nature figure（含 ARS academic-paper 的可视化后端）、K-Dense scientific-visualization |
| [正文 `draft`](../roles/draft/ROLE.md) | `section`、`full` | 写指定章节或汇成完整初稿，整合已交回的证据、引文和图件 | Nature writing、ARS academic-paper |
| | `abstract`、`polish` | 写摘要和关键词，或润色、翻译和压缩已有文字 | ARS academic-paper、Nature polishing |
| | `stats-report`、`analysis` | 写或审查统计报告，或在设计阶段估算样本量、对已收集数据开展计算并交付分析结果 | Nature statistics、K-Dense statistical-analysis |
| | `data-availability`、`disclosure`、`format-convert` | 生成数据和代码声明、AI 使用声明，或按交付要求转换格式和引用样式 | Nature data、ARS academic-paper |
| [审稿 `review`](../roles/review/ROLE.md) | `panel`、`methodology`、`guided`、`nature` | 完整模拟审稿、方法学专项审查、引导式审阅或 Nature 期刊视角 | ARS academic-paper-reviewer、Nature reviewer |
| | `re-review` | 对照模拟首轮意见和新旧稿，交回逐项核对结果与新决定 | ARS academic-paper-reviewer |
| | `revision-coach`、`revise`、`respond` | 整理意见与作者取舍，写入获准修改，再按实际改动起草回复 | ARS academic-paper、Paper Orchestra，严格补丁来自 ARS、Nature response |
| | `rebuttal-audit` | 按原意见检查已有回复。真实外审核对还需对照新旧稿 | ARS academic-paper |

角色负责范围、输入、验收、证据状态和交接；模式负责执行。模式交回的结果先由所属角色验收，再进入下一步。

## 重叠能力的取舍

| 任务 | 采用 | 说明 |
| --- | --- | --- |
| 核对一条引文 | 文献 `verify` | 查原文是否支持这句话 |
| 核对参考文献列表 | 文献 `ref-verify` | 逐字段核对书目信息 |
| 核对引文格式与对应 | 文献 `citation-check` | 查格式、正文与列表的对应 |
| 检索 | 文献 `search` | 研究模式检索时也调用它 |
| 综述 | 文献 `lit-review`；系统综述用 `systematic-review` | ARS academic-paper 的 `lit-review` 未保留 |
| 写章节 | 正文 `section` | 从已核材料起草章节，由正文角色校对并写入初稿 |
| 写整稿 | 正文 `full` | 由编排角色调用时作为阶段 2 的一种走法 |
| 统计 | 报告与审查用 `stats-report`，新计算用 `analysis` | |
| 出图与审图 | `figures make` 生成，`figures audit` 审查 | 正文复用验收后的图件和图件 ID。缺图且任务包含制图时才交给 `figures make` |
| 模拟审稿 | 多席位与编辑决定用 `panel`；按 Nature 标准用 `nature` | ARS 审稿团自带的 `quick` 未保留 |
| 回复与返修 | 回复信 `respond`，路线图 `revision-coach`，核对回复 `rebuttal-audit`，授权改稿 `revise` | 整稿阶段 4 由 `revise` 写主稿，`respond` 按修订候选生成回复。阶段 3′ 的真实外审核对还比较原稿、修订稿和意见 |
| 研究问题 | 大纲 `socratic` | ARS academic-paper 的 Socratic mentor 只用于 `plan` |
| 研究设计 | 方法学设计 `design`；实验执行与管理 `experiment` | |

## 默认模式与严格模式

默认整稿用[证据矩阵](handoff.md)交接。部分专项模式自有依赖，按角色说明加载。严格模式启用 ARS 的合约与校验脚本：

| 角色 | 严格模式内容 | 文件 |
| --- | --- | --- |
| 审稿 | 两次调用的 sprint contract、席位执行来源记录、re-review 三道门合约 | `review/panel/strict/` |
| 审稿 | 补丁式改稿 | `review/revise/references/revision_patch_protocol.md` |
| 正文 | 生成—评估合约 | `draft/paper/strict/` |
| 编排 | Material Passport、断点重置、引文来源终审 | `orchestrate/strict/` |
| 共用 | 交接 schema、合约模板、校验脚本 | `engine/` |

严格模式脚本需要 Python 3 与 `engine/requirements.txt` 中的依赖。

## 可按需导入的配套技能

配套技能有自己的 `SKILL.md`，按任务另行导入。编排只在阶段任务确需时使用配套能力，角色验收结果并纳入证据或交付物。

| 能力 | 去处 |
| --- | --- |
| 研究计划、开题报告、项目申请书 | 独立技能 `nature-proposal-writer` |
| 论文汇报 PPT、图片转 PPT | 独立技能 `nature-paper2ppt`、`nature-image2ppt` |
| 专利交底书 | 独立技能 `nature-paper-to-patent` |
| 定时文献推送 | `nature-literature-pipeline`。发现的资料可作为 `literature` 检索和核验的候选 |
| 实验日志整理 | `nature-experiment-log`。日志可交给 `outline` 整理研究主张和证据 |
| 数值工作流与符号推导 | `matlab` 可辅助 `outline experiment` 的数值工作流，`sympy` 可辅助论证和 `review` 的推导复核 |
| 单位核算与统计模型 | `uncertainty-and-units` 可辅助 `draft` 核算数字。`statsmodels` 可辅助 `outline design` 和 `draft analysis` 的统计模型工作 |

合并技能从 `references/nature-shared/` 读取内置参考。独立的 `nature-shared` 供其他 Nature 技能按其说明导入。

上游 ARS 中删除的部分：评测与测试、发布工具、审稿人校准模式、跨模型验证、模型分级、审稿目标标准绑定、跨运行裁决记录、调查分支账本、Claude/Codex 运行时适配层。
