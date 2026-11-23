<!-- 角色文件：由 research-writing 路由加载，不单独注册为技能。整合 Paper Orchestra 的整稿流程与 ARS academic-pipeline 的阶段、检查点和完整性核查。 -->

> **角色 · 编排**　调用 `$research-writing orchestrate [模式]` 或 `$research-writing full`，由 [`research-writing`](../../SKILL.md) 路由进入。

# 编排整稿

本角色负责从研究材料到成稿的全过程：判断从哪个阶段进入，安排各角色和模式，在关键节点停下请用户确认，运行完整性核查，汇合各分支，最后整理交付物与过程记录。本角色自己不写正文、不审稿，具体工作交给其他角色。

| 模式 | 什么时候用 | 交付 |
| --- | --- | --- |
| `full` | 从研究材料或想法出发，走完整篇论文 | 终稿、完整性核查报告、过程记录 |
| `resume` | 接着上次停下的阶段继续 | 从断点继续，沿用已有产物 |

用户只要一个阶段的产物时，不进入本角色，直接调用对应角色。详细的阶段状态机、交接内容和异常处理见 [`references/workflow_detail.md`](references/workflow_detail.md) 与 [`references/pipeline_state_machine.md`](references/pipeline_state_machine.md)。

## 1. 先按手头材料选择入口

| 手上有 | 从哪个阶段进入 |
| --- | --- |
| 只有想法或宽泛题目 | 阶段 1，先 `outline socratic` |
| 研究问题明确，需要文献与研究基础 | 阶段 1，用 `literature deep`、`brief` 或 `lit-review` |
| 研究问题与核心材料齐备，暂无稿件 | 阶段 2 |
| 已有稿件 | 阶段 2.5，先做完整性核查再审稿 |
| 已有稿件和审稿意见 | 阶段 4 |
| 已有修订稿 | 阶段 3′ |
| 只差排版与投稿材料 | 阶段 2.5 核查后进入阶段 5 |

判断入口后，向用户确认入口、各阶段准备使用的模式，以及大致的工作量和交互轮数，再开始。已经有稿件的情况不能跳过阶段 2.5；以前的核查报告只作参考，稿件仍要重新核查。

## 2. 阶段

| 阶段 | 内容 | 调用 | 交付 |
| --- | --- | --- | --- |
| 1 研究 | 研究问题、方法、文献与综合 | `outline socratic`、`literature deep` / `brief` / `lit-review` / `systematic-review`，需要时 `outline experiment` | 研究问题、方法蓝图、文献与综合 |
| 2 写作 | 大纲 → 文献与图表分支 → 正文 | 见下方“阶段 2 的组稿方式” | 初稿 |
| 2.5 完整性核查 | 写完后、审稿前 | [`agents/integrity_verification_agent.md`](agents/integrity_verification_agent.md) | 核查报告与修正后的稿件 |
| 3 审稿 | 模拟同行评审 | `review panel` | 审稿报告、编辑决定、返修路线图 |
| 4 返修 | 按路线图修改并回复 | `review revision-coach`、`review revise`、`review respond` | 修订稿与回复信 |
| 3′ 复审 | 核对修订是否回应意见 | `review re-review` | 逐项核对表与新决定 |
| 4′ 再返修 | 复审仍为大修时，最多一轮 | `review revise` | 第二版修订稿 |
| 4.5 终稿核查 | 从头重新核查，不只复查已知问题 | integrity_verification_agent | 终稿核查报告 |
| 5 定稿 | 格式与投稿材料 | `draft format-convert`、`draft disclosure`、`draft data-availability` | 终稿（Markdown，按需 DOCX、PDF、LaTeX） |
| 6 过程记录 | 写作过程、协作情况与 AI 的自我检讨 | 按 [`references/process_summary_protocol.md`](references/process_summary_protocol.md) | 过程记录（用户可以不要） |

返修次数：阶段 4 和 4′ 各一轮，4′ 之后直接进入 4.5，不再回到审稿。仍未解决的问题写进“已知局限”。

### 阶段 2 的组稿方式

沿用 Paper Orchestra 的分工：

1. **立大纲。** `outline` 为主要主张建立 ID，写明哪些证据能证明、哪些待验证，给出各节任务、检索单和图件任务卡。需要逐章讨论时用 `outline plan`。
2. **跑分支。** `literature` 按检索单查背景、前作和定向出处；`figures` 按任务卡出图或复核已有图。两个分支输入独立时可以并行。若比较图要用文献中的数值，先核实这些数值再画图。
3. **汇合与写作。** 把同一主张对应的文献、原始材料、分析和图件汇合，决定可以采用的论断。由 `draft` 作为唯一写入者整合章节、引用和编号：需要一次写出整篇初稿时用 `draft full`，按节推进时用 `draft section`。

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

按 [`references/integrity_review_protocol.md`](references/integrity_review_protocol.md) 分五步：参考文献、引用语境、统计数据、原创性、主张。主张核验见 [`references/claim_verification_protocol.md`](references/claim_verification_protocol.md)：高影响主张（核心结论、数值、因果、方法关键、有争议的）全部核验，其余抽样。

- 同时运行 [`references/ai_research_failure_modes.md`](references/ai_research_failure_modes.md) 的 7 类 AI 研究失败检查（实现错误、虚构结果、走捷径、把错误当发现、方法造假、框架锁定等）。任何一类被判定为“疑似”就阻断，用户说明理由后才能继续，理由要记录并写进过程记录。
- 系统综述等适用的情况下，由 [`agents/compliance_agent.md`](agents/compliance_agent.md) 做 PRISMA-trAIce 与 RAISE 合规检查，见 `@/references/compliance_checkpoint_protocol.md`。
- 未通过时修正后重新核查，最多三轮；三轮后仍有问题，列出未解决项，由用户决定是否继续，决定要记录。未解决项不能悄悄去掉。
- 阶段 4.5 必须从头重新核查，因为修订可能带来新问题。
- 抄袭与重复检查见 [`references/plagiarism_detection_protocol.md`](references/plagiarism_detection_protocol.md)。

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

- **协作深度观察。** [`agents/collaboration_depth_agent.md`](agents/collaboration_depth_agent.md) 在完整和简要检查点、以及过程记录时观察用户的协作方式（委托程度、警觉性等），只作参考，从不阻断，不在强制检查点运行。
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
