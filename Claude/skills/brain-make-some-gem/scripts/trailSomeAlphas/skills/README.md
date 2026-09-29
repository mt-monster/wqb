# trailSomeAlphas/skills —— GEM 引擎的捆绑（vendored）兜底资产

> **本目录是"最后兜底"，不是运行时首选；其中大部分是顶层 skill 的派生副本。** 2026-09-29 更正：这些 `SKILL.md` **正文从不拼进 LLM prompt**（此前的说法写反了）。

## 真实的 skill 目录解析顺序

解析逻辑在 [`pipeline_paths.py::_resolve_skill_dir()`](../pipeline_paths.py)，两个目录**统一同源**：

1. **环境变量覆盖**：`WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR`（指向 skill 根目录）
2. **`skill_roots` 候选**（主安装位优先，仓库 `Claude/skills/` 兜底）——由 `skill_roots.py` 的 `candidate_paths_under_skill()` 枚举，顺序与 `wq-brain-campaign-toolkit/_lib/skill_roots.py`、`wqb.workflow._common._skill_roots()` 一致（有 `test_root_resolvers_use_single_source_helper` 守护）
3. **本目录（内嵌 legacy 兜底）**——仅在脱离仓库且所有安装位都缺失时命中，启动日志会打 `embedded:legacy` 来源标记

实测（本机）：两个目录都解析到主安装位 / 仓库副本，内嵌副本**平时并不生效**。

## 各资产的角色

| 名称 | 顶层（`Claude/skills/`） | 本目录（vendored） |
|---|---|---|
| `brain-feature-implementation` | **权威版** | `scripts/` 是**硬依赖**（解析兜底命中时 `ace_lib` / `validator` / `implement_idea` 从这里导入）；`SKILL.md` 为**自动同步的副本**（引擎不使用它的正文） |
| `brain-data-feature-engineering` | **权威版** | `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md` 是顶层同名文件的**逐字节副本**（目录内有 `GENERATED.md` 标记；引擎不读它们）；**故意不放 `SKILL.md`** |

## SKILL.md 到底怎么被引擎用的

`run_pipeline.py` 会 `read_text_optional()` 读两份 `SKILL.md`，但 `pipeline_prompts.build_prompt`：
- **dfe**：只看「是否非空」——非空就附一句固定的 8 问提示（不变 / 变化 / 异常 / 交互 / 结构 / 累积 / 相对 / 本质），不复制文件内容；
- **FI**：接收但**完全不使用**。

所以文档篇幅与内容**不影响**生成质量；`[skill-doc] … MISSING` 的真正含义是「skill 目录解析异常」（FI 目录同时承载 `scripts/`）。这一点由 `tests/unit/test_se_docs.py`（AST）钉死——将来若又把 SKILL 文本拼进 prompt，要同步改本节。

## 两条不可违背的约束

1. **以下四个文件必须与顶层权威版逐字节一致**：FI `SKILL.md`、dfe `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md`。它们不进 prompt，但同名不同文会让人在兜底位读到过时规范（2026-09-26 前内嵌 FI `SKILL.md` 是 49 行旧英文稿，还引用不存在的 `manage_todo_list`；内嵌 dfe `reference.md` 也已漂移过）。机械守护：`tests/unit/test_gem_skill_paths.py`。更新顶层后同步：
   ```bash
   python tools/sync_gem_embedded_skill.py --apply   # --check 只校验
   ```
2. **`brain-data-feature-engineering/` 不要放 `SKILL.md`**。解析探针用的就是 `SKILL.md`：本目录没有它 → 自动跳过本目录、选中带完整文档的权威副本。若在此处补一份 `SKILL.md`，解析会**改回**内嵌目录。

## 产物路径（2026-09-26 起迁出）

GEM 生成的 `*_ideas.md` 不再写进本目录，改由 `pipeline_reports.save_ideas_report()` 写到 **`GEM_REPORT_ROOT`**（= `GEM_DATA_ROOT/output_report` = 仓库 `data/gem_runs/output_report/`，与 `data/` 同源，可用 `WQB_GEM_DATA_ROOT` 覆盖）。

## 变更纪律

- 改动 `scripts/`（`ace_lib` / `validator` / `pipeline_*`）需回归 GEM 全链路：`python tools/sync_skills.py` 后跑 `pytest tests/ -x`；`validator.py` 须与 `alpha-expression-verifier` 权威版四处一起改（`tests/unit/test_se_docs.py` 守护）。
- **不要**用 `tools/sync_skills.py` 覆盖本目录的 `scripts/`，也**不要**把本目录当作顶层 skill 同步到安装位。
