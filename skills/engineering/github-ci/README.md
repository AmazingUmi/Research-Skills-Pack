# GitHub CI

可选工程 pack。`gh-fix-ci` 用于排查 GitHub Actions 中失败的 PR 检查，读取检查结果和运行日志，汇总失败原因并提出修复计划。

让 Agent 导入完整的 [`gh-fix-ci` 技能目录](skills/gh-fix-ci/)，保留其中的脚本、元数据和资源。使用时需要 Python 3、已认证的 GitHub CLI（`gh`）以及目标仓库的检查结果和日志读取权限。

包内保留上游 [Apache-2.0 许可证](skills/gh-fix-ci/LICENSE.txt)。版本与来源见[仓库来源清单](../../SOURCES.md#github-ci)。
