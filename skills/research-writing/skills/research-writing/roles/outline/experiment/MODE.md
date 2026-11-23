<!-- 模式文件：outline/experiment。由 research-writing 路由加载，不单独注册为技能。改编自 ARS experiment-agent。 -->

# 实验与研究执行

调用 `$research-writing outline experiment <子模式>`。详细说明见 [`references/workflow_detail.md`](references/workflow_detail.md)。

| 子模式 | 用途 | agent | 交付 |
| --- | --- | --- | --- |
| `plan` | 以对话方式设计实验或研究方案 | 本文件与 workflow_detail 中的 plan 流程 | 代码实验计划或研究方案（`templates/code_experiment_plan.md`、`templates/study_protocol.md`） |
| `run` | 执行代码实验并监控 | [`agents/code_runner_agent.md`](agents/code_runner_agent.md) | 实验结果记录 |
| `manage` | 管理人类被试研究的流程与进度，可跨会话续接 | [`agents/study_manager_agent.md`](agents/study_manager_agent.md) | 研究状态记录（`templates/study_state.md`） |
| `validate` | 统计解释与复现验证 | code_runner（重跑）加 workflow_detail 中的统计解释流程 | 解释与复现结论 |

实验设计的方法学问题（随机化、区组、因子设计、样本量）用 `design`；只解释已有结果的统计报告用正文角色的 `stats-report`。

## 安全与伦理

- 执行代码前确认要运行的命令、输入数据和输出位置，用户同意后再运行。
- 涉及人类被试时按 [`references/irb_ethics_checklist.md`](references/irb_ethics_checklist.md) 检查，审查路径由所在机构判定，本技能不代为判定豁免或审查类别。
- 监控与停滞判断见 [`references/stall_detection_protocol.md`](references/stall_detection_protocol.md)，复现标准见 [`references/reproducibility_protocol.md`](references/reproducibility_protocol.md)，统计解释见 [`references/statistical_interpretation_guide.md`](references/statistical_interpretation_guide.md)。

## 交回大纲角色

实验计划与结果按主张 ID 记录：数据版本、分析条件、结果位置和适用范围，供大纲、图表和正文角色使用。与其他角色的交接字段见 [`references/ars_integration_guide.md`](references/ars_integration_guide.md)，其中的 Material Passport 只在严格模式下使用。
