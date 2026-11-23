<!-- 模式文件：outline/plan 与 outline/outline-only。由 research-writing 路由加载，不单独注册为技能。改编自 ARS academic-paper 的 plan 与 outline-only 模式。 -->

# 论文规划

| 模式 | 调用 | 参与的 agent | 交付 |
| --- | --- | --- | --- |
| `plan` | `$research-writing outline plan` | intake、socratic_mentor（论文版）、argument_builder、structure_architect | 逐章计划与对话中整理出的要点（INSIGHT） |
| `outline-only` | `$research-writing outline outline-only` | intake、structure_architect、argument_builder | 详细大纲与证据地图 |

研究问题还没定时先用 `socratic`。大纲角色自己的“工作步骤”适合已有材料、只需要主张与证据表和下游任务卡的情况；本模式适合需要逐章讨论、反复打磨结构的情况。

## `plan`

按 [`references/plan_mode_protocol.md`](references/plan_mode_protocol.md) 逐章对话：

1. 用 `@/roles/draft/paper/agents/intake_agent.md` 的简化访谈确认论文类型、学科和目标。
2. 由 [`agents/socratic_mentor_agent.md`](agents/socratic_mentor_agent.md) 逐章提问，帮助作者想清每一章要论证什么。导师只提问，不替作者决定贡献表述。
3. 用 [`agents/argument_builder_agent.md`](agents/argument_builder_agent.md) 对论证做压力测试。
4. 汇总成论文蓝图，每章的要点标出依据（作者已有的材料、待找的文献、待做的分析）。

示例见 [`examples/plan_mode_guided_writing.md`](examples/plan_mode_guided_writing.md)。

## `outline-only`

1. 用 intake 确认配置。
2. 由 [`agents/structure_architect_agent.md`](agents/structure_architect_agent.md) 选择结构（参考 [`references/paper_structure_patterns.md`](references/paper_structure_patterns.md)），写出大纲、字数分配和证据地图。
3. 由 argument_builder 建立主张—证据链，处理反方论点。

## 交回大纲角色

把蓝图或大纲转写为大纲角色的交付格式：章节写作计划、主张与证据表（主张 ID、状态）、文献检索单、图件任务卡和待核清单。agent 文件中提到审稿目标标准绑定时，一律按 `criteria_binding_unavailable` 处理。
