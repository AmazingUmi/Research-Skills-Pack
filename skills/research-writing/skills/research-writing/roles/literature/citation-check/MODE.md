<!-- 模式文件：literature/citation-check。由 research-writing 路由加载，不单独注册为技能。改编自 ARS academic-paper 的 citation-check 模式。 -->

# 引文格式与一致性检查

调用 `$research-writing literature citation-check`。按 [`agents/citation_compliance_agent.md`](agents/citation_compliance_agent.md) 检查稿件的引文：

- 正文引用与参考文献列表是否一一对应，有无漏列或多列。
- 引用格式是否符合指定样式（APA 7、Chicago、MLA、IEEE、Vancouver），作者、年份、标题、出处、DOI 是否完整。
- 同一文献的写法是否前后一致。

格式依据：[`references/apa7_style_guide.md`](references/apa7_style_guide.md)、[`references/apa7_extended_guide.md`](references/apa7_extended_guide.md)，其他样式见 [`references/citation_format_switcher.md`](references/citation_format_switcher.md)。APA 7 下有中文文献时另读 [`references/apa7_chinese_citation_guide.md`](references/apa7_chinese_citation_guide.md)，按其中针对中文姓名的缩写和排序规则检查，不套用拉丁字母的排序清单。用户指定了期刊的特殊要求时，以期刊要求为准。

本模式只查格式和对应关系。要逐字段核对文献是否真实存在、卷期页码是否正确，用 `ref-verify`；要核对原文是否支持某句话，用 `verify`。

交付：单独的引文问题清单，列位置、原文、适用规则及建议替换文本。输入稿只读，由当期写手将采纳的改动汇入下一版。转换整份稿件的引用样式属于正文角色的 `format-convert`。
