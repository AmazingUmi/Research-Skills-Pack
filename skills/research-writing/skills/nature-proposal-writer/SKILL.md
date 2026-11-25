---
name: nature-proposal-writer
description: "Compose, revise, or audit research proposals, opening reports, and research plans from supporting evidence. Use for 研究计划、开题报告、科研项目申请书. For manuscript review, use the review role of research-writing."
license: MIT
metadata:
  hermes:
    tags: [research, writing, proposal, revision, qa, multi-agent]
    related_skills: [research-writing]
---

# nature-proposal-writer — proposal-first 科研写作 pipeline

受 autonovel（状态机+打分）、professor（动态专家）、brainstorming（入口追问）、anti-AI-writing（语言清理）启发的科研写作状态机。**不是通用"帮我写论文"prompt。**

需要初始化模板、按条件加载参考资料或执行导出脚本时，先读取 `manifest.yaml`，只加载与当前条件匹配的路径。

## 核心原则

1. **证据先于文字** — 起草前必须建立或读取 `research_canon` 和 `evidence_table`
2. **论证先于章节** — 写正文前必须完成 `argument_map`
3. **契约先于段落** — 每节需要 purpose / allowed claims / forbidden claims / inputs / validation
4. **范围先于完备** — 如果是分阶段写作，先锁定阶段边界
5. **专项审查** — 按当前问题选择相应专业视角，分派方式见 [professor-dispatch.md](references/professor-dispatch.md)。
6. **内容先于语言** — 诊断科学逻辑后再做 anti-slop / 语言打磨
7. **不自动升级事实** — 永远不把 "may indicate" 改成 "proves"，除非有证据支撑
8. **删除胜于解释** — 当某主张不可行，直接删除。正文干净，解释留给答辩
9. **该停就停** — 平台期、专家冲突、证据缺失是停止理由，不是润色理由

## 模式分派

本技能负责开题、研究计划和申请书中的文献综述章节。独立综述设计交给 `$research-writing literature lit-review`，系统综述交给 `literature systematic-review`，已有论文的审阅交给 `$research-writing review`。

| 输入 | 模式 |
|---|---|
| 开题或申请书的题目、方向、模糊想法 | `compose` — 加载 `references/compose-mode.md` |
| 已有开题报告或申请书的段落、章节或全文 | `revise` — 加载 `references/revise-mode.md` |
| 已有开题或申请草稿 + 扩写/补写/重构 | `hybrid` — 加载 `references/hybrid-mode.md` |

模糊时推断默认模式。只在选择会改变工作流时才问用户。

## 项目结构

**工作目录**：`<outputs>/nature-proposal-writer/<project-slug>/`

**标准文件**：

```
00_scope.md              写作任务边界
01_research_canon.md     硬事实和约束
02_evidence_table.md      claim → evidence 映射表
03_argument_map.md        论证架构
04_section_contracts.md   每节的 purpose / inputs / allowed & forbidden claims
05_style_guide.md         风格、术语、禁用表达
state.json                项目状态（mode、round、scores、technical_debts）
sources/                  用户材料、文献、数据
drafts/                   草稿和分节文件
revision_briefs/          修订简报
qa_logs/                  诊断、专家审查、anti-slop、打分记录
exports/                  最终输出（.md + .docx）
```

新建项目时按 `manifest.yaml` 的 `templates.on_demand` 路由从 `templates/` 取空模板。
`references/worked-example-quaternary-proposal.md` 提供了基于通用材料科学领域的开题修订与评分示例。

## Reference 文件索引

完整 reference 按任务需要加载，不要一次性注入全部文件：

| Reference | 加载时机 |
|---|---|
| `references/compose-mode.md` | 模式 = compose（9 步流程） |
| `references/revise-mode.md` | 模式 = revise（9 步流程） |
| `references/hybrid-mode.md` | 模式 = hybrid |
| `references/evaluation-rubric.md` | 使用 8 维 × 4 锚点评分体系时 |
| `references/research-anti-slop.md` | 清理中文 proposal 的模板化和空泛表达时 |
| `references/chinese-review-writing-style.md` | 撰写或修订开题材料的中文文献综述章节时 |
| `references/stopping-rules.md` | 判断继续迭代、拆分范围或停止时 |
| `references/professor-dispatch.md` | 按失败模式分派动态专家时 |
| `references/foundation-files.md` | 建立或修复 foundation 六文件时 |
| `references/project-structure.md` | 初始化项目目录或维护 `state.json` 时 |
| `references/export-archive.md` | 导出和归档 `.md` / `.docx` 时 |
| `references/partial-proposal-scope.md` | 分阶段写作并防止范围蔓延时 |
| `references/ref-renumbering-cascade.md` | 处理参考文献增删和编号级联时 |
| `references/review-paper-framework.md` | 设计申请书的文献综述章节框架时 |
| `references/review-critique-methodology.md` | 比较申请书文献综述章节的论据时 |
| `references/validation-checklist.md` | 自动检查主张、引用、编号和可复现性时 |
| `references/gpt-handoff-revision-brief.md` | 生成跨 agent 修订交接简报时 |
| `references/within-approved-proposal.md` | 在已批准的 proposal 框架内扩写时 |
| `references/worked-example-quaternary-proposal.md` | 需要查看开题返修与评分示例时 |
| `references/降承诺提案模式.md` | 证据不足，需要降低承诺强度时 |

## 运行交付

每次运行结束时输出：

1. 当前文件路径或修订后文本
2. 当前分数/状态
3. 剩余风险
4. 一条建议的下一步

## QA Mode — 四层质量保障 Pipeline

先确认本次交付物。研究计划、开题报告和项目申请的审查可进入本模式；其他文种只有作者明确点名使用本方案的专项检查时，才取其指定维度。一般稿件审阅交给 `$research-writing review`；邮件与周报按用户要求处理。

### 情境挡位

| 挡位 | 适用场景 | 阈值 |
|------|---------|------|
| `proposal` | 开题报告、研究计划或项目申请；按文种采用适用评分维度 | 7.0 |
| `quick` | 快速检查开题材料中的关键问题，或作者点名的专项检查 | 逐项列出依据 |

专项检查到所选维度即交付。完整开题 QA 按以下顺序执行。可使用宿主提供的专家或语言工具，也可按本包的[专家分工](references/professor-dispatch.md)、[中文表述指引](references/research-anti-slop.md)和[核对清单](references/validation-checklist.md)完成，报告中注明实际采用的方式。

### 完整开题 QA 的顺序

```
Gate 2: 按问题组织内容审查
  ├── 方案设计 → 可行性专家 + 领域专家
  └── 方案的文献基础 → 覆盖面与证据强度
  │
  ▼
Gate 1: 语言审查
  └── 按目标语种标出模糊措辞、无依据的修饰和术语不一致
  │
  ▼
Gate 3: auto-validation（格式/完整性层）
  └── 各项判断能否定位到文献、前期数据或计划依据？方法与编号是否清楚？
  │
  ▼
Gate 4: 评分阈值（分维度打分）
  ├── 总分≥阈值 → 通过 ✅
  └── 总分<阈值 → 按低分维度定向回退（不超过 3 轮）
```

**Gate 2 在 Gate 1 之前** — 避免改了句子后被专家打回重写。

### 使用方法

```
用户请求“审查这份开题报告的实验可行性”
  → 依据现有设备、样本和时间逐项指出可行条件及未决问题。
```

## 配置你的研究域

从已给材料提取研究背景、方法与约束，按实际问题选择审查视角。领域信息影响判断时，再向作者核实。
