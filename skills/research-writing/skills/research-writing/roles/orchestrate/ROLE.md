<!-- 角色文件：由 research-writing 路由加载，不单独注册为技能。整合 Paper Orchestra 的整稿流程与 ARS academic-pipeline 的阶段、检查点和完整性核查。 -->

> **角色 · 编排**　调用 `$research-writing orchestrate [模式]` 或 `$research-writing full`，由 [`research-writing`](../../SKILL.md) 路由进入。

# 编排整稿

本角色负责从研究材料到成稿的全过程：判断从哪个阶段进入，安排各角色和模式，在关键节点停下请用户确认，运行完整性核查，汇合各分支，最后整理交付物与过程记录。本角色自己不写正文、不审稿，具体工作交给其他角色。

| 模式 | 什么时候用 | 交付 |
| --- | --- | --- |
| `full` | 从研究材料或想法出发，走完整篇论文 | 终稿、完整性核查报告、过程记录 |
| `resume` | 恢复同一次流程已记录的断点 | 从已验证的阶段和检查点继续，沿用经过核对的产物 |

用户只要一个阶段的产物时，不进入本角色，直接调用对应角色。详细的阶段状态机、交接内容和异常处理见 [`references/workflow_detail.md`](references/workflow_detail.md) 与 [`references/pipeline_state_machine.md`](references/pipeline_state_machine.md)。

## 1. 先按手头材料选择入口

| 手上有 | 新开 `full` 时的阶段顺序 |
| --- | --- |
| 只有想法或宽泛题目 | 阶段 1，先 `outline socratic` |
| 研究问题明确，需要文献与研究基础 | 阶段 1，用 `literature deep`、`brief` 或 `lit-review` |
| 核心材料齐备，或要把已有章节续写成完整初稿 | 阶段 2，标出可复用章节、待写段落和待算结果 |
| 已有完整稿件，需要首轮审稿 | 阶段 2.5 → 3 |
| 已有稿件和审稿意见，需要返修 | 阶段 2.5 → 4，沿用已有审稿意见 |
| 已有修订稿，需要复审 | 阶段 2.5 → 3′，按复审模式核对所需材料 |
| 已有定稿候选，只差排版与投稿材料 | 阶段 2.5 → 4.5 → 5，保留定稿前的强制检查点 |

新开 `full` 带入完整稿件以审稿、返修或定稿时，先对当前版本运行阶段 2.5。以前的核查报告可供本次核查参考。开始前向用户确认通过核查后的目标阶段、各阶段使用的模式和预计交互轮数。目标阶段缺少必要材料时，先补齐材料或确认适用的走法。

`resume` 先核对同一次流程的已记录阶段、稿件版本和未决检查点，再从该点恢复。已经完成且仍有效的阶段 2.5 可以沿用。若当前稿件与记录不符，重新核查受影响的阶段。仅提供旧报告或稿件时按上表开始新流程。严格模式的跨会话恢复见[断点重置协议](strict/passport_as_reset_boundary.md)。

## 2. 阶段与角色调用

`orchestrate` 管整条流程的分派、交接和检查点。下表列出各阶段实际执行工作的角色、模式和交付物，适用于默认和严格流程。严格模式在相应交接处增加校验。

| 阶段 | 执行角色 | 调用与选择条件 | 交付 |
| --- | --- | --- | --- |
| 1 研究 | `outline`、`literature` | 按[阶段 1](#阶段-1-的研究任务)选择研究问题、设计和文献模式 | 研究问题、方法蓝图、文献依据或综述，按实际任务交付 |
| 2 写作 | `outline` → `literature`、`figures` → `draft` | 先用 `outline` 制定章节及证据任务，按需分派文献、统计分析和图表，再用 `draft section` 或 `draft full` 汇稿。见[阶段 2](#阶段-2-的组稿方式) | 初稿及其引文、图件和证据记录 |
| 2.5 完整性核查 | `orchestrate` | 用[内部核查流程](#4-完整性核查阶段-25-与-45)检查完成的初稿或带入的完整稿件 | 核查报告及对应稿件版本 |
| 3 模拟审稿 | `review` | `review panel`，先请作者确认审稿人卡片 | 审稿报告、模拟编辑决定、返修路线图 |
| 4 返修 | `review` | 需要梳理意见或收集作者取舍时用 `review revision-coach`。按授权用 `review revise` 改稿，需要回复信用 `review respond` | 作者取舍与变更记录、修订稿，按需附回复信 |
| 3′ 复审 | `review` | 模拟审稿用 `review re-review`。真实外审按[外审核对流程](references/external_review_protocol.md#step-4-self-verification-completeness-check)核对，已有回复可用 `review rebuttal-audit` 检查覆盖 | 逐项核对表。模拟复审另给模拟编辑决定 |
| 4′ 再返修 | `review` | 模拟复审仍为大修时，按新一轮作者授权用 `review revise` 修改一次 | 第二版修订稿与变更记录 |
| 4.5 终稿核查 | `orchestrate` | 用[内部核查流程](#4-完整性核查阶段-25-与-45)检查当前完整终稿，在进入阶段 5 前呈交作者确认 | 终稿核查报告及对应稿件版本 |
| 5 定稿 | `draft` | `draft format-convert` 按确认的格式交付。按需调用 `draft disclosure` 和 `draft data-availability` | Markdown 终稿或用户指定格式，按需附投稿声明 |
| 6 过程记录 | `orchestrate` | 用户接受时按[过程记录流程](references/process_summary_protocol.md)汇总已完成阶段与决策 | 写作过程、协作记录及未决事项 |

复审中缺少可决定结论的材料时，保留已完成的核对，标明对应意见和所缺材料，在阶段 3′ 等作者补充后复核受影响项。真实外审逐项记录能否证实回复中的改动。

进入阶段 4.5 前，若复审为 Minor Revision，逐项记录剩余、部分解决、恶化或新增问题的修订位置及复核结果，或作者逐项签署的留置理由。缺少处置则保留在 3′ 检查点。

返修次数：阶段 4 和 4′ 各一轮，4′ 之后直接进入 4.5，不再回到审稿。仍未解决的问题写进“已知局限”。

### 阶段 1 的研究任务

- 研究问题尚未成形时用 `outline socratic`。问题已明确但需要设计研究时用 `outline design`。要判断证据强度时用 `outline appraise`，需要详细实验方案时可用 `outline experiment plan`。实验执行按单独授权和实验模式的要求处理。
- 按文献交付物选择模式。完整研究报告用 `literature deep`，简报用 `literature brief`，叙述性综述用 `literature lit-review`，明确要求系统综述时用 `literature systematic-review`。用户要求单独筛选已有记录时用 `literature screen`，筛选前先由作者确认协议。

### 阶段 2 的组稿方式

沿用 Paper Orchestra 的分工：

1. **立大纲。** `outline` 默认直接执行大纲角色的工作步骤，为主要主张建 ID，交付主张证据表、章节计划、检索单和图件任务卡。逐章讨论选 `outline plan`，需要详细大纲和证据地图时选 `outline outline-only`。
2. **按任务查文献、计算与制图。** 需要根据原始数据计算估计值、区间或检验时，用 `draft analysis` 交付数据版本、分析单位、计算方法及结果定位。纯文字结果也走这一步；图表或正文依赖该计算时，等结果核对后再引用。 按具体主张找出处或核对来源，用 `literature verify`。需要多源检索候选资料时用 `literature search`，需要进一步读原文时按权限补充全文。出图用 `figures make`，已有图的证据与表现评估用 `figures audit`。文献和图表分支输入独立时可以并行。依赖文献数值的图先等数值核验完成。
3. **汇合与写作。** 把同一主张对应的文献、原始材料、分析和图件汇合，由 `draft` 作为唯一写入者整合章节、引用和编号。整篇初稿用 `draft full`，按节推进用 `draft section`。已有证据和图件随任务交接，核对后复用。

各分支交接按[交接约定](../../references/handoff.md)。汇合前核对各分支覆盖了哪些主张、用了哪个版本、哪些仍待核。缺失或冲突只限制受影响的论断，其余照常推进。

## 3. 检查点

每个阶段结束后都要停下，提示用户并等待确认。

| 类型 | 什么时候 | 内容 |
| --- | --- | --- |
| 完整 | 第一个检查点、完整性核查之后、阶段 5 完成时 | 交付物清单、进度面板（[`references/progress_dashboard_template.md`](references/progress_dashboard_template.md)）、可选操作 |
| 简要 | 用户连续两次以上说“继续”的非关键阶段 | 一行状态与“继续 / 暂停” |
| 强制 | 完整性核查未通过、审稿决定（阶段 3、3′）、进入阶段 5 之前 | 不能跳过，必须由用户本人明确回复 |

- 强制检查点不能自动通过，即使上一阶段的结果看起来完美。
- 用户连续四次以上说“继续”后，插入一次完整检查点。
- 用户可以在任何检查点暂停，之后用 `resume` 继续。
- 每次完整检查点前自查：最新产出中有没有未核实的引文？是否不加辨别地接受了所有意见？各项标准是改善、不变、退步还是无法比较？是否加入了用户和路线图都没有要求的内容？本阶段的交付物是否齐全？有疑虑就写进检查点。
- 阶段切换时，用一小段话提醒下一阶段最相关的铁律与常见错误（见 [`references/reinforcement_content.md`](references/reinforcement_content.md)），防止长对话中原则被遗忘。

## 4. 完整性核查（阶段 2.5 与 4.5）

在组稿前确定 `integrity_mode`，默认值为 `default`。写手、核查者和导出器沿用同一任务卡设置。严格流程及其恢复记录使用 `strict`。

默认按[证据矩阵核查](agents/default_integrity_review.md)检查参考文献、引用语境、统计数据、原创性和主张。严格模式由[严格核查 Agent](agents/integrity_verification_agent.md)执行[完整性协议](references/integrity_review_protocol.md)与机器校验，适用时再调用[合规 Agent](agents/compliance_agent.md)生成 Schema 12 报告。

- 两种模式都按 [AI 研究失败检查](references/ai_research_failure_modes.md)和适用的合规规则处理阻断项。
- 核查未通过时，按当前模式交回修正清单并复核，最多三轮。三轮后仍有一般核查问题时，列出未解决项，由用户明确决定是否带着这些标记继续，决定写入过程记录。失败模式和合规项遵循各自的阻断及解除规则。
- 阶段 4.5 以当前稿件为基线，从头执行适用的核查范围。

## 5. 缺材料、改中间件和失败时怎么办

| 遇到的情况 | 应怎样继续 |
| --- | --- |
| 已有前一阶段产物 | 检查材料、稿件版本和论断口径是否匹配，可用的部分直接复用 |
| 文献找得到，原文却未支撑当前措辞 | 保留真实书目信息，标记该主张待核或缺证据，改成已获支持的说法 |
| 图件只有截图，或缺可核数据 | 对可确认内容做版式、图注或结构处理，数据级核对列为待核 |
| 材料或分析口径冲突 | 并列记下版本、来源与差异，明确适用范围；写作可先处理无冲突部分 |
| 单个分支失败或部分缺项 | 保存可用结果，从受影响的角色继续，向下游同步限制 |
| 模板、引文或编译环境缺失 | 保留可编辑稿件，报告实际完成到何处；编译失败时保留候选与基线 |
| 用户改变数据、目标期刊或论断范围 | 复核受影响的任务及其下游，避免把旧口径带进新稿 |
| 审稿决定为拒稿 | 让用户选择：回到阶段 2 大幅重构，或结束 |
| 用户中途离开 | 保存状态（[`agents/state_tracker_agent.md`](agents/state_tracker_agent.md)），下次用 `resume` 继续 |

## 6. 不做的事

- 不自己写正文或审稿，只调度和协调。
- 不跳过完整性核查，不自动通过强制检查点。
- 不因为上下文太长而让后一阶段质量低于前一阶段；发现退步时暂停，重新加载原则再继续。
- 不悄悄丢掉审稿意见：返修跟踪表要列出每条意见的处理状态。
- 过程记录中的协作评分如实给出，每个分数都附具体依据。
- 用户可以随时暂停或退出。

## 7. 可选观察与严格模式

- **协作深度观察。** [`agents/collaboration_depth_agent.md`](agents/collaboration_depth_agent.md) 仅在作者要求此项反馈时，在完整或简要检查点以及过程记录中观察协作方式（委托程度、警觉性等），只作参考，从不阻断，不在强制检查点运行。
- **主张与引文对齐审计。** 用户要求时，在阶段 4 → 5 之间由 [`agents/claim_ref_alignment_audit_agent.md`](agents/claim_ref_alignment_audit_agent.md) 抽样审计引用是否真正支持主张。
- **严格模式。** 需要可复核的阶段状态、Material Passport、断点重置或引文来源终审时，按 [`strict/pipeline_orchestrator_agent.md`](strict/pipeline_orchestrator_agent.md) 执行，状态与交接字段见 `@/engine/handoff_schemas.md`，断点重置见 [`strict/passport_as_reset_boundary.md`](strict/passport_as_reset_boundary.md)。严格模式依赖 `@/engine/scripts/` 下的脚本，脚本无法运行时报告失败，不以默认模式冒充。

## 8. 调用示例

- **文本研究，搭大纲。** “用 `$research-writing outline` 根据两版文本和我的批注搭论证主线，标出可定位的引文，以及需要更多材料才能成立的判断。”
- **定量研究，写结果。** “用 `$research-writing draft section` 依据样本说明和结果表写结果部分，保留指标定义、比较条件和不确定性。”
- **综述，核引用并画图。** “用 `$research-writing full` 从我的方法框架和文献清单开始组稿，交付可验证的引文、示意图和图注。”
- **理论论文，审推导。** “用 `$research-writing review` 检查定理表述、证明前提和引理引用，逐条指出缺失条件和证据位置，只给审阅意见。”
- **收到外审，逐条回复。** “用 `$research-writing review respond` 按审稿原编号起草回复，区分已经改完的内容和仍需补证据的问题。”

完整示例见 `examples/` 下的完整流程、中途进入与完整性失败恢复三个例子。

## 与上游项目的对应

**PaperOrchestra。** 原项目由 Python 调度器控制顺序：大纲以 JSON 保存计划；开启自动制图时，文献与制图同时读取初始大纲，完成后把引文、图件和更新后的大纲交给一次全文写作调用，随后编译、审稿与精修。原实现的内容精修最多三轮，每版经过三份模拟审稿与一次汇总，按总分选择版本，之后单独检查视觉版式。本组保留大纲、文献、图表、正文、审稿返修五个环节和“大纲之后文献与图表并行”的组织方式，迭代次数由用户目标与证据决定，采纳以可核验证据为准。[论文 §4](https://arxiv.org/html/2604.05018v1#S4) · [并行调度](https://github.com/google-research/paper-orchestra/blob/d9bae997e793a015ed38bb1605be9eb58c00284f/methods/paper_writer_with_plotting.py#L98-L208) · [精修源码](https://github.com/google-research/paper-orchestra/blob/d9bae997e793a015ed38bb1605be9eb58c00284f/methods/agents/content_refinement_agent.py#L201-L593) · [模拟审稿](https://github.com/google-research/paper-orchestra/blob/d9bae997e793a015ed38bb1605be9eb58c00284f/autoraters/agent_review.py#L112-L181)

**ARS academic-pipeline。** 阶段编号（1、2、2.5、3、4、3′、4′、4.5、5、6）、三类检查点、两次完整性核查、两阶段审稿与过程记录沿用 ARS 的设计。ARS 中的跨模型验证、跨运行裁决记录与可选的调查分支账本没有保留。
