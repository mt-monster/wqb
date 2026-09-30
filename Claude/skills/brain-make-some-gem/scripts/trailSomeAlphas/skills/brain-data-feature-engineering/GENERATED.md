# GENERATED —— 勿手改

本目录的 `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md` 是顶层
`Claude/skills/brain-data-feature-engineering/` 同名文件的**逐字节副本**（**顶层是源，这里是派生物**）。

- 改内容请改顶层，然后：`python tools/sync_gem_embedded_skill.py --apply`
- 漂移由 `tests/unit/03_gem/test_gem_skill_paths.py` 守护（`--check` 等价）
- GEM 引擎**不读**这三个文件（它只读 dfe 的 `SKILL.md` 判断「是否非空」，决定附不附一句固定的 8 问提示）
- **本目录故意不放 `SKILL.md`**：解析探针用它把内嵌目录排除掉，见上级 `../README.md`
