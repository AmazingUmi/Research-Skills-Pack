# 科研技能包

[English](README.md) | 中文

可直接分发的科研 Agent 技能，分为两个 pack。

| Pack | 适用任务 |
| --- | --- |
| [Research Writing](skills/research-writing/) | 科研论文全流程。`research-writing` 技能整合 Paper Orchestra、ARS、Nature Skills 与 K-Dense，按编排、大纲、文献、图表、正文、审稿六个角色组织。另有 7 个独立技能，覆盖研究计划、汇报 PPT、专利、文献推送和实验日志。 |
| [Research Engineering](skills/research-engineering/) | 科研软件开发：MATLAB/Octave、SymPy、单位与不确定度、GPU 优化、多目标优化、机器学习、统计模型，以及 GitHub Actions 诊断。 |

## 使用方式

把 pack 中 `skills/` 下需要的技能目录整个复制到 Agent 的技能位置，保留目录内的全部文件。`research-writing` 只注册为一个技能，调用方式是 `$research-writing <角色> [模式]`，例如 `$research-writing full`、`$research-writing review panel`。全部模式见[能力清单](skills/research-writing/skills/research-writing/references/skill-map.md)。

### 让 Agent 导入本技能包

复制下面任一提示词发给你的 Agent（如 Codex、Claude Code 等）。如已克隆到本地，把仓库地址换成你的本地路径；如只需单个 pack，保留 `research-writing` 或 `research-engineering` 即可。

**项目级导入（仅当前项目生效）**

```text
请从 https://github.com/AmazingUmi/codex-research-bundles 导入科研技能包到当前项目的项目级技能目录（按你当前宿主的约定选择项目级 skills 路径，例如 .agents/skills/、.codex/skills/ 或 .claude/skills/）：
1. 获取仓库（若无法联网请提醒我提供本地路径），导入 skills/research-writing/skills/ 和 skills/research-engineering/skills/ 下的全部技能目录（或只导入我指定的技能；导入任一 nature-* 独立技能时一并带上 nature-shared）。
2. 每个含 SKILL.md 的技能目录须完整复制并保留内部全部子目录与文件，不要重命名目录，不要拆分或单独注册 research-writing 内部的角色与模式文件。
3. 写入前检查目标目录是否已有同名技能，如有冲突先向我确认后再覆盖。
4. 导入后核对每个技能目录的 SKILL.md 均可读取，并列出实际安装路径和已导入的技能清单。
```

**全局级导入（所有项目通用）**

```text
请从 https://github.com/AmazingUmi/codex-research-bundles 导入科研技能包到当前用户的全局技能目录（按你当前宿主的约定选择全局 skills 路径，例如 ~/.agents/skills/、~/.codex/skills/ 或 ~/.claude/skills/）：
1. 获取仓库（若无法联网请提醒我提供本地路径），导入 skills/research-writing/skills/ 和 skills/research-engineering/skills/ 下的全部技能目录（或只导入我指定的技能；导入任一 nature-* 独立技能时一并带上 nature-shared）。
2. 每个含 SKILL.md 的技能目录须完整复制并保留内部全部子目录与文件，不要重命名目录，不要拆分或单独注册 research-writing 内部的角色与模式文件。
3. 写入前检查目标目录是否已有同名技能，如有冲突先向我确认后再覆盖。
4. 导入后核对每个技能目录的 SKILL.md 均可读取，并列出实际安装路径和已导入的技能清单。
```

[使用说明](doc/usage.md)包含阶段 2 组稿、暂停续接、单角色调用的示例，以及论文流程图和两套技能树。

单独分发某个 pack 时，请保留其中的许可证与声明文件，并带上 [SOURCES.md](skills/SOURCES.md) 中对应的条目。该文件记录上游版本、本地改动与许可范围。

## 许可证

本仓库原创的文档采用 [Apache-2.0](LICENSE)。`research-writing` 技能因包含改编自 ARS 的内容，整体按 CC BY-NC 4.0（禁止商用）分发。其他技能保留各自的许可证，详见 [SOURCES.md](skills/SOURCES.md)。
