# Writing · 论文写作指导

[返回首页](../README.zh.md) · [来源与许可证](SOURCES.md)

## 总入口

用 [`paper-orchestra`](writing/paper-orchestra/skills/paper-orchestra/SKILL.md) 推进整篇论文或跨阶段任务。它确定本次要交付的产物、主张和证据，安排角色与子 pack，最后把结果汇入同一稿件。使用 `paper-orchestra` 组稿时，阶段推进、结果验收和最终汇稿均由它负责。

| 内嵌子 pack | Paper Orchestra 何时调用 | 交回的结果 |
| --- | --- | --- |
| [Nature](writing/paper-orchestra/packs/nature/) | 某个论点需要补文献、核引文，或已有段落、图件、审稿回复需要专项处理 | 可追溯的引文与证据、具体修改或图件 |
| [K-Dense Writing](writing/paper-orchestra/packs/k-dense-writing/) | 需要检查实验设计、统计口径、单位、不确定度或科学可视化 | 方法依据、结果口径与可报告范围 |
| [ARS-Codex](writing/paper-orchestra/packs/ars-codex/) | 某个阶段需要研究规划、系统综述或结构化审稿 | 对应阶段的计划、证据摘要或审稿意见 |

可以从大纲、已有资料、草稿或审稿意见进入，按缺口启用对应角色。只改一段、核一条引文或检查一张图时，可直接点名对应技能。

将 Paper Orchestra 的六个技能目录同级导入，再按需导入子 pack 的完整技能目录。Nature 的技能如引用 `nature-shared`，同时导入该目录。ARS-Codex 按需导入完整的 `academic-research-suite`。K-Dense Writing 与 Engineering Core 重叠的技能共用同一上游版本。

## 技能清单

- **Paper Orchestra（6）**：`paper-orchestra`、`paper-orchestra-outline`、`paper-orchestra-literature`、`paper-orchestra-figures`、`paper-orchestra-draft`、`paper-orchestra-review`。
- **Nature（20）**
  - 文献与引文：`nature-academic-search`、`nature-downloader`、`nature-literature-pipeline`、`nature-paper-card`、`nature-reader`、`nature-citation`、`nature-ref-verifier`。
  - 写作与研究记录：`nature-writing`、`nature-polishing`、`researchwrite`、`nature-statistics`、`nature-data`、`nature-experiment-log`。
  - 图表、演示和成果：`nature-figure`、`nature-image2ppt`、`nature-paper2ppt`、`nature-paper-to-patent`。
  - 审稿与回复：`nature-reviewer`、`nature-response`。
  - 共用依赖：`nature-shared`。
- **K-Dense Writing（7）**：`experimental-design`、`matlab`、`sympy`、`statistical-analysis`、`uncertainty-and-units`、`scientific-critical-thinking`、`scientific-visualization`。
- **ARS-Codex（1）**：`academic-research-suite`。
