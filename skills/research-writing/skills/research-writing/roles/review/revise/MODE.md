<!-- 模式文件：review/revise。由 research-writing 路由加载，不单独注册为技能。 -->

# 按意见改稿

调用 `$research-writing review revise`。在用户授权的范围内按审稿意见修改稿件。

## 默认做法

按审稿角色 [`ROLE.md`](../ROLE.md) 的“授权改稿与版本选择”一节执行：保留当前接受稿作为基线，在差分或独立候选中修改，逐项对照基线复核，按证据决定采纳或退回。只处理返修路线图中作者标为 `will_address` 的项；没有路线图时，先用 `revision-coach` 整理意见，或请作者明确列出要改的项。

改稿时一份稿件只有一个写入者。语言层面的修改可以交给 `$research-writing draft polish`，新增或重写的段落可以交给 `$research-writing draft section`，返回的文字由本模式写入并复核。

## 严格模式：补丁式改稿

需要证明“没有点名的段落一个字都没动”时，按 [`references/revision_patch_protocol.md`](references/revision_patch_protocol.md) 执行：先用 `@/engine/scripts/ars_anchorize_draft.py` 给已复制的工作稿分块编号，同时记录原稿与加锚稿各自的哈希，写作者只产出补丁文件，再用 `@/engine/scripts/ars_apply_revision_patch.py` 确定性地应用，生成新文件和应用报告。基础稿件不被修改。应用报告供 `re-review` 核对改动范围。

这一机制只保证未点名的块不被改动，不保证改动本身更好；结构性重写不受补丁保护，需要升级为完整重写并重新审阅。
