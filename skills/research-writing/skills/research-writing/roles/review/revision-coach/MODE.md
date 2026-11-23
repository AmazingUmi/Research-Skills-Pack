<!-- 模式文件：review/revision-coach 与 review/rebuttal-audit。由 research-writing 路由加载，不单独注册为技能。改编自 ARS academic-paper 的 revision-coach 与 rebuttal-audit 模式。 -->

# 返修路线与回复核对

两个模式共用 [`agents/revision_coach_agent.md`](agents/revision_coach_agent.md) 的意见解析能力。

| 模式 | 调用 | 需要的输入 | 交付 |
| --- | --- | --- | --- |
| `revision-coach` | `$research-writing review revision-coach` | 审稿意见（任意格式），可附稿件 | 不排序的返修路线图、作者逐项取舍记录、可选的跟踪表和回复骨架 |
| `rebuttal-audit` | `$research-writing review rebuttal-audit` | 审稿意见 **和** 已写好的回复稿 | 逐条覆盖表、遗漏清单、风险提示和改进建议 |

只有意见、需要梳理返修路线时用 `revision-coach`。要写完整的回复信用 `respond`。核对修订稿时，首轮模拟审稿用 `re-review`，真实外审用[外审逐项自查](../../orchestrate/references/external_review_protocol.md#step-4-self-verification-completeness-check)。

## `revision-coach`

1. 按 agent 文件的处理流程解析每一条意见，一条不漏：原文、分类、涉及章节、具体承诺（commitment）。
2. 路线图只记录事实：严重程度、编辑要求、成本范围和后果分开记录，不替作者排工作顺序。
3. 请作者对每一项明确选择 `will_address`、`wont_address` 或 `not_on_point`，缺的选择不默认填。
4. 按需生成 [`templates/revision_tracking_template.md`](templates/revision_tracking_template.md) 跟踪表或 [`templates/revision_response_template.md`](templates/revision_response_template.md) 回复骨架。

**机构委员会来函。** 只有用户明确说来源是真实的委员会或机构审查办公室时，才按 [`references/committee_correspondence_protocol.md`](references/committee_correspondence_protocol.md) 处理。期刊或会议的审稿人、编辑、领域主席、程序委员会都按同行评审处理。

## `rebuttal-audit`

只核对作者已有的回复稿，不改写、不代写。

- 逐条标出每个审稿意见在回复稿中是 `addressed`、`partially` 还是 `missing`。
- 列出没有回应的意见。
- 标出风险：语气过于对抗、主张没有证据、误读了审稿人的意思。
- 给出建议，供作者自行决定。

输出是参考性的质量检查报告，不标记任何“已核验”或“可提交”状态。

## 交回审稿角色

每条意见保留原审稿人编号与原文，转写为问题 ID 并关联到主张 ID 与稿件位置。作者的取舍记录原样保留，`revise` 只处理标为 `will_address` 的项。文中出现的 Schema 编号对应 [`@/engine/handoff_schemas.md`](../../../engine/handoff_schemas.md)，只在严格模式下需要生成这些结构。
