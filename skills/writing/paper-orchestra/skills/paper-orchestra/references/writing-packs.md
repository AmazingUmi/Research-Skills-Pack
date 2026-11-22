# Writing 下层技能分工

先选当前阶段和负责角色。只有任务需要专项方法时，才加载下表对应技能。把期望产物、相关主张 ID、证据版本、允许使用的来源及可写范围传给执行者。专项检查按任务和材料取用，证据不足的推断登记为待核。结果按[交接约定](handoff.md)回到 Paper Orchestra，由当前角色核对后继续。

| 阶段 | 按需调用 | 交回的产物 |
| --- | --- | --- |
| 立大纲或缩小研究问题 | ARS `academic-research-suite: ars-plan`，或 K-Dense `experimental-design` | 限定范围的写作计划、证据缺口或设计意见 |
| 查出处、组织文献 | Nature `nature-academic-search`、`nature-citation`、`nature-ref-verifier`。需要完整的综述方法时可用 ARS `academic-research-suite: ars-lit-review` | 可定位的书目、主张支持范围和待核项 |
| 核数、制图 | 根据任务选 K-Dense `statistical-analysis`、`uncertainty-and-units`、`scientific-visualization`，或用 Nature `nature-figure` 处理投稿图件 | 方法和计算依据、图件位置、图注及适用条件 |
| 起草、润色 | Nature `nature-writing` 或 `nature-polishing` | 指定章节的正文或润色建议，保留证据、术语和引用依据 |
| 审稿、回复 | Nature `nature-reviewer`、`nature-response`，或按需用 ARS `academic-research-suite: ars-reviewer` 获取独立意见 | 关联主张的审阅问题或按原意见编号的回复建议 |

给 ARS 明确一个模式和阶段产物。在同一次 Paper Orchestra 组稿任务里，由 Paper Orchestra 推进后续阶段并安排最终整合，ARS 回交该阶段的建议或核查结果。

## 找到技能

- **直接读取分发包。** 从本文所在的 `references/` 出发，在 `../../../packs/<pack>/skills/<技能名>/SKILL.md` 读取所选技能。`<pack>` 为 `nature`、`k-dense-writing` 或 `ars-codex`。ARS 入口文件对应目录 `academic-research-suite`。
- **已导入 Agent。** 按技能名称从 Agent 的技能列表或当前技能目录定位。Nature 技能需要的 `nature-shared` 与对应技能同级导入。

如果所需技能或它依赖的工具不可用，用当前 Paper Orchestra 角色完成能独立交付的部分，并标明哪些结论仍需补核。
