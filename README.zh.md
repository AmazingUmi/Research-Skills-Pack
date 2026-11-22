# Codex 科研技能包

[English](README.md) | 中文

可直接分发的科研技能文件。按任务从 Writing 和 Engineering 两份清单开始。

| 清单 | 适用任务 |
| --- | --- |
| [Writing](skills/WRITING.md) | Paper Orchestra 统领论文工作，按阶段调用内嵌的 Nature、K-Dense Writing 和 ARS-Codex。 |
| [Engineering](skills/ENGINEERING.md) | 科研软件项目开发、数值方法、验证、性能检查和可选的 GitHub Actions 诊断。 |

## 使用方式

要推进一篇论文时，让 Agent 读取 [Paper Orchestra 总入口](skills/writing/paper-orchestra/skills/paper-orchestra/SKILL.md)，并给它访问整个 [Paper Orchestra pack](skills/writing/paper-orchestra/) 的权限。只处理一项任务时，也可以直接打开对应技能的 `SKILL.md`。

长期使用时，把主 pack 和所选子 pack 的 `skills/` 中需要的完整技能目录导入 Agent 支持的位置。Paper Orchestra 的六个技能同级导入，并保留引用文档、脚本和资源。两份清单都收录的技能导入一次即可。

单独分发某个 pack 时，请一并保留其中的许可证和声明，并带上 [SOURCES.md](skills/SOURCES.md) 中对应的来源条目。该表记录上游版本、提交、许可范围和本地改动。

## 许可证

本仓库原创的文档、技能清单及本地 Paper Orchestra 改编采用 [Apache-2.0](LICENSE)。随包提供的第三方内容继续适用各自的许可证和声明，包括 ARS-Codex 的 CC BY-NC 4.0。详见[各 pack 的来源与许可证](skills/SOURCES.md)。
