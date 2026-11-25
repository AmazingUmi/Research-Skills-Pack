<!-- 模式文件：outline/socratic。由 research-writing 路由加载，不单独注册为技能。改编自 ARS deep-research 的 socratic 模式。 -->

# 苏格拉底式研究引导

调用 `$research-writing outline socratic`。适用于只有宽泛题目、方向或兴趣，还没有可回答的研究问题的情况。

由 [`agents/socratic_mentor_agent.md`](agents/socratic_mentor_agent.md) 以提问引导作者，经过问题界定、方法反思、证据策略等层次逐步收敛；必要时调用 `@/roles/literature/research/agents/research_question_agent.md` 按 FINER 标准整理研究问题，由 `@/roles/literature/research/agents/devils_advocate_agent.md` 质疑假设。对话流程见 [`references/socratic_mode_protocol.md`](references/socratic_mode_protocol.md)，提问类型见 [`references/socratic_questioning_framework.md`](references/socratic_questioning_framework.md)，示例见 [`examples/socratic_guided_research.md`](examples/socratic_guided_research.md)。

## 约定

- 导师只提问，不提出、替换或排序作者的贡献表述，由作者自己回答。
- 对话结束时输出研究计划摘要。只有作者拟写综述时才按[文献角色的综述形式提示](../../literature/research/MODE.md)确认综述类型。实证、建模等研究沿用已确认的问题与方法。
- 两个可选环节默认关闭，只有用户本人在消息中要求时才打开：`reading-probe`（用户引用了具体文献时，请其复述一段内容，用于自查是否读过原文）和 `adjacent-probe`（探索阶段提出一个用户没想到的相邻视角，只以问题形式出现）。

## 交回大纲角色

研究问题、范围边界、子问题和需要补的证据，转写为大纲角色的主张草案与待核清单，再进入 `plan` 或大纲角色的工作步骤。
