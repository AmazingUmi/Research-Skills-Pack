# Research Writing

科研论文写作技能包。核心是 [`research-writing`](skills/research-writing/SKILL.md)：一个按角色组织的写作技能，整合了 Paper Orchestra、ARS、Nature Skills 和 K-Dense 的写作能力。另附 7 个论文稿件之外的独立技能。

## research-writing

由六个角色组成：编排、大纲、文献、图表、正文、审稿。调用方式是 `$research-writing <角色> [模式]`，例如：

- `$research-writing full`：从研究材料出发走完整篇论文，包括完整性核查、模拟审稿、返修和定稿。
- `$research-writing literature systematic-review`：做系统综述。
- `$research-writing review panel`：五席位模拟审稿，并给出编辑决定。
- `$research-writing draft section`：写指定章节。

全部模式见[能力清单](skills/research-writing/references/skill-map.md)。默认模式只依靠提示和证据矩阵，不需要额外环境。严格模式使用 `engine/` 下的合约与校验脚本，需要 Python 3 和 [`engine/requirements.txt`](skills/research-writing/engine/requirements.txt) 中的依赖。部分模式另有自己的依赖，例如 `literature search` 的可选 MCP server、`literature fulltext` 的 Node.js、`figures make` 的绘图库，详见各模式目录。

## 独立技能

| 技能 | 用途 |
| --- | --- |
| [`nature-proposal-writer`](skills/nature-proposal-writer/SKILL.md) | 研究计划、开题报告、科研项目申请书 |
| [`nature-paper2ppt`](skills/nature-paper2ppt/SKILL.md) | 由论文或阅读笔记生成中文学术汇报 PPT |
| [`nature-image2ppt`](skills/nature-image2ppt/SKILL.md) | 把幻灯片截图、扫描件还原成可编辑 PPT |
| [`nature-paper-to-patent`](skills/nature-paper-to-patent/SKILL.md) | 专利草稿与技术交底书 |
| [`nature-literature-pipeline`](skills/nature-literature-pipeline/SKILL.md) | 多源检索、打分、精读和归档的定时文献推送 |
| [`nature-experiment-log`](skills/nature-experiment-log/SKILL.md) | 标准化实验日志，产出可作为 `research-writing` 大纲角色的输入 |
| [`nature-shared`](skills/nature-shared/SKILL.md) | 上述 Nature 技能的共用参考，随它们一起导入 |

## 导入

把 `skills/` 下需要的技能目录整个复制到 Agent 的技能位置，保留目录内的全部文件。`research-writing` 只注册一个技能，内部的角色和模式文件不叫 `SKILL.md`，不会被单独注册。

## 许可证

- `research-writing` 整体按 [CC BY-NC 4.0](LICENSE) 分发（禁止商用），因为其中包含改编自 ARS 的内容。Paper Orchestra（Apache-2.0）、Nature Skills（Apache-2.0 / MIT）、K-Dense（MIT）的许可文本与署名见 [NOTICE](NOTICE) 和 [licenses/](licenses/)。
- 7 个独立技能不适用 CC BY-NC 4.0，保留 Nature Skills 的 Apache-2.0 或 MIT 许可（[licenses/Apache-2.0-Nature.txt](licenses/Apache-2.0-Nature.txt)、[licenses/MIT-Nature-contributors.txt](licenses/MIT-Nature-contributors.txt)，以及各技能目录中的附加许可）。

来源版本与改动见 [SOURCES.md](../SOURCES.md)。
