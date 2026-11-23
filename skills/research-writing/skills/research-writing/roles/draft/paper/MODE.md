<!-- 模式文件：draft/paper。由 research-writing 路由加载，不单独注册为技能。改编自 ARS academic-paper。 -->

# 整稿写作与投稿材料

由一组写作 agent 完成整篇论文的起草，以及摘要、AI 使用披露和格式转换。阶段说明、agent 分工和失败处理见 [`references/workflow_detail.md`](references/workflow_detail.md) 与 [`references/workflow_phase_details.md`](references/workflow_phase_details.md)。

| 模式 | 调用 | 参与的 agent | 交付 |
| --- | --- | --- | --- |
| `full` | `$research-writing draft full` | intake、literature_strategist、structure_architect、argument_builder、draft_writer、citation_compliance、abstract_bilingual、peer_reviewer、formatter；有定量结果时加 visualization | 完整初稿（含图表时附绘图代码） |
| `abstract` | `$research-writing draft abstract` | intake、abstract_bilingual | 摘要与关键词（可双语） |
| `disclosure` | `$research-writing draft disclosure` | formatter（披露分支） | 按目标期刊政策生成的 AI 使用声明 |
| `format-convert` | `$research-writing draft format-convert` | formatter | LaTeX、DOCX（通过 Pandoc）、PDF 或 Markdown 稿件；可转换引用样式 |

只写或重写某一节时用 `section`；只改语言用 `polish`。规划论文结构用大纲角色的 `plan` 或 `outline-only`；按审稿意见改稿用审稿角色的 `revise`。

## `full` 的流程

| 阶段 | agent | 产出 |
| --- | --- | --- |
| 0 配置 | [`agents/intake_agent.md`](agents/intake_agent.md) | 论文配置记录：类型、学科、目标期刊、引用格式、输出格式、语言、字数 |
| 1 文献 | [`agents/literature_strategist_agent.md`](agents/literature_strategist_agent.md) | 检索策略与来源语料；已有文献角色交回的引文表时可跳过 |
| 2 结构 | `@/roles/outline/plan/agents/structure_architect_agent.md` | 大纲与证据地图 |
| 3 论证 | `@/roles/outline/plan/agents/argument_builder_agent.md` | 论证蓝图 |
| 4 起草 | [`agents/draft_writer_agent.md`](agents/draft_writer_agent.md) | 完整初稿 |
| 5a 引文 | `@/roles/literature/citation-check/agents/citation_compliance_agent.md` | 引文审核报告 |
| 5b 摘要 | [`agents/abstract_bilingual_agent.md`](agents/abstract_bilingual_agent.md) | 摘要与关键词（与 5a 并行） |
| 6 内部审阅 | [`agents/peer_reviewer_agent.md`](agents/peer_reviewer_agent.md) | 审阅报告，最多两轮修改 |
| 7 格式 | [`agents/formatter_agent.md`](agents/formatter_agent.md) | 最终输出 |

检查点：

1. 配置记录（阶段 0）须由用户确认后再继续。
2. 大纲（阶段 2）须由用户认可，可以要求调整结构。
3. 修改最多两轮，仍未解决的问题写进“已知局限”。
4. 内部审阅中的 Critical 问题未解决前不进入阶段 7。
5. 用户提供了自己的文献时，可以跳过阶段 1。

阶段 6 是写作内部的自查，不代替审稿角色的 `panel`。需要外部视角的模拟审稿时，成稿后再交给审稿角色。

## 写作约定

- 写作风格与判断：[`references/academic_writing_style.md`](references/academic_writing_style.md)、[`references/writing_judgment_framework.md`](references/writing_judgment_framework.md)；成稿前按 [`references/writing_quality_check.md`](references/writing_quality_check.md) 检查。
- 论文结构与模板：大纲角色的 `paper_structure_patterns.md`，以及本目录 `templates/` 下的 IMRaD、理论、综述、案例、会议论文和政策简报模板。
- 防止引入稿件外的结论：[`references/anti_leakage_protocol.md`](references/anti_leakage_protocol.md)。
- 投稿材料：期刊投稿 [`references/journal_submission_guide.md`](references/journal_submission_guide.md)、作者贡献 [`references/credit_authorship_guide.md`](references/credit_authorship_guide.md)、资助声明 [`references/funding_statement_guide.md`](references/funding_statement_guide.md)、LaTeX [`references/latex_template_reference.md`](references/latex_template_reference.md)。
- 缩写检查：起草、修改或写摘要后，可运行 `python3 @/engine/scripts/check_acronyms.py --input <稿件文件>`。

## `disclosure`

按 [`references/disclosure_mode_protocol.md`](references/disclosure_mode_protocol.md) 执行：先确认 AI 的使用类别和记录，再按 [`references/venue_disclosure_policies.md`](references/venue_disclosure_policies.md) 中目标期刊的政策判断是否需要披露、需要写什么。期刊不在收录范围或信息不全时停下说明，不用通用声明代替。按指定政策条款生成时，见 [`references/policy_anchor_disclosure_protocol.md`](references/policy_anchor_disclosure_protocol.md)。期刊政策会变化，交付时注明所依据政策的来源与核对日期。

## 严格模式

`full` 的阶段 4 和阶段 6 可以改为两次调用的生成—评估合约：写作者和评估者先在看不到稿件的情况下承诺标准，再分别起草和评审。说明见 [`strict/generator_evaluator_protocol.md`](strict/generator_evaluator_protocol.md) 与 `strict/` 下各 agent 的合约文件，合约模板在 `@/engine/contracts/writer/` 与 `@/engine/contracts/evaluator/`。引文来源记录、主张意图清单等 Passport 结构只在严格模式下生成，字段见 `@/engine/handoff_schemas.md`。

本技能不包含审稿目标标准绑定。agent 文件中提到 `ReviewCriteriaBindingManifest` 或 binding 时，一律按 `criteria_binding_unavailable` 处理，不作期刊契合度的断言。

## 交回正文角色

稿件由正文角色作为唯一写入者整合。交回时附：稿件版本与改动范围、关键主张及所用证据（主张 ID）、引用键与图件键、仍待核的问题。
