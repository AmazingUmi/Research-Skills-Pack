# Research Engineering

科研软件开发与计算技能。每个技能独立使用，按项目需要选择并导入完整目录。工具与库的要求见各技能的 `SKILL.md`。

[查看技能树](../../doc/figures/engineering-skill-tree.svg)

| 技能 | 用途 | 来源 |
| --- | --- | --- |
| [`matlab`](skills/matlab/SKILL.md) | MATLAB 与 GNU Octave 数值工作流 | K-Dense |
| [`sympy`](skills/sympy/SKILL.md) | 符号数学、精确计算、LaTeX 与代码生成 | K-Dense |
| [`uncertainty-and-units`](skills/uncertainty-and-units/SKILL.md) | 单位换算与量纲检查、测量不确定度传播 | K-Dense |
| [`optimize-for-gpu`](skills/optimize-for-gpu/SKILL.md) | GPU 性能优化 | K-Dense |
| [`pymoo`](skills/pymoo/SKILL.md) | 多目标优化 | K-Dense |
| [`scikit-learn`](skills/scikit-learn/SKILL.md) | 机器学习 | K-Dense |
| [`pytorch-lightning`](skills/pytorch-lightning/SKILL.md) | 深度学习训练工程 | K-Dense |
| [`statsmodels`](skills/statsmodels/SKILL.md) | 统计模型 | K-Dense |
| [`gh-fix-ci`](skills/gh-fix-ci/SKILL.md) | 诊断 GitHub Actions 中失败的 PR 检查。需要 Python 3、已认证的 GitHub CLI 和仓库访问权限 | OpenAI skills |

统计检验与结果报告、科学可视化、证据评估、实验设计在 Research Writing 的 `research-writing` 技能中（`draft analysis`、`figures audit`、`outline appraise`、`outline design`），这里不重复收录。

## 许可证

- K-Dense 技能：[MIT 及版权声明](licenses/K-Dense-MIT.md)；pymoo 与 PyTorch Lightning 技能另适用 [Apache-2.0](licenses/Apache-2.0.txt)；SymPy、scikit-learn、statsmodels 的 BSD 3-Clause 原文见 [SymPy](licenses/SymPy-LICENSE.txt)、[scikit-learn](licenses/Scikit-learn-LICENSE.txt)、[statsmodels](licenses/Statsmodels-LICENSE.txt)。
- `gh-fix-ci`：[Apache-2.0](skills/gh-fix-ci/LICENSE.txt)。

固定版本与逐技能许可证见 [SOURCES.md](../SOURCES.md)。
