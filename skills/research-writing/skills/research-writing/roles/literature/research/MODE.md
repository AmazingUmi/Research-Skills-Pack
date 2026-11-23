<!-- 模式文件：literature/research。由 research-writing 路由加载，不单独注册为技能。改编自 ARS deep-research。 -->

# 文献研究

由一组研究 agent 完成文献检索、来源核验、综合与报告。详细的阶段、agent 分工和失败处理见 [`references/workflow_detail.md`](references/workflow_detail.md)；本文件说明各模式怎么选、在哪里停下、交回什么。

| 模式 | 调用 | 参与的 agent | 交付 |
| --- | --- | --- | --- |
| `lit-review` | `$research-writing literature lit-review` | bibliography、source_verification、synthesis | 带注书目与综合，1,500–4,000 词 |
| `systematic-review` | `$research-writing literature systematic-review` | research_question、research_architect、bibliography、source_verification、risk_of_bias、meta_analysis、synthesis、report_compiler、editor_in_chief、ethics_review、devils_advocate | 符合 PRISMA 2020 的报告、森林图数据、GRADE 表 |
| `fact-check` | `$research-writing literature fact-check` | source_verification | 逐条核查报告 |
| `three-way-scan` | `$research-writing literature three-way-scan` | bibliography、source_verification | 按 WHY / HOW / WHAT 对比的论文短名单与跨文献小结 |
| `deep` | `$research-writing literature deep` | 除 socratic_mentor、risk_of_bias、meta_analysis 外的全部 | 完整研究报告，3,000–8,000 词 |
| `brief` | `$research-writing literature brief` | research_question、bibliography、source_verification、report_compiler | 研究简报，500–1,500 词 |

研究问题还不清楚时，先用 `$research-writing outline socratic`。要对已有文本做审阅，用审稿角色，不在这里做。只需要核对一两条引文时，用文献角色的 `verify` 模式即可，不必进入本模式。

## 检查点

- **研究问题确认。** `deep` 和 `systematic-review` 在第 1 阶段（研究问题与方法蓝图）结束后停下，等用户确认后再检索。
- **综述形式提示（Review-form note）。** 用户选择 `lit-review`，或确认研究问题时，告诉用户可以选择的综述形式：系统综述、范围综述、叙述或整合综述、快速综述，或不做正式综述。说明这件事由用户决定，本技能不推荐也不设默认；然后等待回复，在回复之前不开始检索。用户已经说明了综述形式，或本项目中已经回答过，就不再提示。只有用户明确选择，才进入 `systematic-review`。
- **Devil's Advocate 检查点。** `deep` 和 `systematic-review` 在研究问题、综合、成稿三处由 [`agents/devils_advocate_agent.md`](agents/devils_advocate_agent.md) 把关，Critical 问题解决前不进入下一阶段。
- **伦理审查。** 发现 Critical 级别的学术诚信问题（伪造、抄袭、缺少 AI 使用披露、曲解来源）时停下，请用户确认。用户可以说明理由后继续，理由要记录下来。
- **修订轮数。** 成稿修订最多两轮，仍未解决的问题写进“已知局限”。

## 来源与检索

- 检索时可调用 `$research-writing literature search` 的多源检索；Semantic Scholar、OpenAlex、Crossref、arXiv 与中文文献的接口说明在 `references/*_api_protocol.md`。
- 核验来源时区分书目身份（这篇文献是否存在、版本是否正确）与主张支持（原文是否支持这句话），并记录实际读到的范围：全文、节选、摘要或仅书目。
- 每篇文献的方法缺陷按 [`@/references/per_source_method_weaknesses.md`](../../../references/per_source_method_weaknesses.md) 记录，标明是作者自己承认的还是读者推断的。只读过摘要时写“未评估”。

## 严格模式

需要可复核的文献语料、引文来源记录或预注册材料时，按 [`@/engine/handoff_schemas.md`](../../../engine/handoff_schemas.md) 生成 Material Passport 中的对应条目，schema 在 `@/engine/contracts/passport/`。默认不生成，只用证据矩阵。

## 交回文献角色

把检索与核验结果转写进证据矩阵：每条可引用的文献给出引用键、书目信息、实际读到的版本与位置、支持哪条主张（主张 ID）以及支持范围；无法确认的标为待核、缺证据或冲突。综述正文交给文献角色验收后，再交正文角色或编排角色。
