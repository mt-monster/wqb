# trailSomeAlphas/skills —— GEM 引擎的捆绑（vendored）资产

> **本目录是"最后兜底"，不是运行时首选。** 2026-09-26 审计实测纠正了此前 README 的说法。

## 真实的 skill 目录解析顺序（2026-09-26 起）

解析逻辑在 [`pipeline_paths.py::_resolve_skill_dir()`](../pipeline_paths.py)，两个目录**统一同源**：

1. **环境变量覆盖**：`WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR`（指向 skill 根目录）
2. **`skill_roots` 候选**（主安装位优先，仓库 `Claude/skills/` 兜底）——由 `skill_roots.py` 的
   `candidate_paths_under_skill()` 枚举，顺序与 `wq-brain-campaign-toolkit/_lib/skill_roots.py`、
   `wqb.workflow._common._skill_roots()` 一致（有 `test_root_resolvers_use_single_source_helper` 守护）
3. **本目录（内嵌 legacy 兜底）**——仅在脱离仓库且所有安装位都缺失时命中，会打 `embedded:legacy` 来源标记

实测（2026-09-26，本机）：`FEATURE_IMPLEMENTATION_DIR` = `~/.claude/skills/brain-feature-implementation`，
喂进 LLM 的 `SKILL.md` 为**权威版 111 行**——即内嵌副本**平时并不生效**。

## 各资产的角色（纠正后的口径）

| 名称 | 顶层（`Claude/skills/`） | 本目录（vendored） |
|---|---|---|
| `brain-feature-implementation` | **权威版**（agent 调用 + 引擎 prompt 用） | `scripts/` 是**硬依赖**（`ace_lib` / `validator` 从这里导入）；`SKILL.md` 为**自动同步的副本** |
| `brain-data-feature-engineering` | **权威版**（322 行 `SKILL.md`） | prompt 模板子集；**本目录故意不放 `SKILL.md`** |

## 两条不可违背的约束

1. **`brain-feature-implementation/SKILL.md` 必须与顶层权威版逐字一致**。
   它被 `run_pipeline.py` 读入并拼进 **LLM prompt**，所以"同名不同文"在 SKILL.md 上是**有害**的
   ——2026-09-26 之前它是一份 2026-08-22 的 49 行旧英文稿（还引用不存在的 `manage_todo_list` 工具），
   一旦兜底命中就会把过时规范喂给模型。现由
   `tests/unit/test_gem_skill_paths.py::test_embedded_fi_copy_matches_authoritative` 机械守护。
   更新顶层后请同步：
   ```bash
   python tools/sync_gem_embedded_skill.py   # 或按测试失败提示手动复制
   ```
2. **`brain-data-feature-engineering/` 不要放 `SKILL.md`**。
   解析探针用的就是 `SKILL.md`：本目录没有它 → 自动跳过本目录、选中带完整文档的权威副本。
   若在此处补一份 `SKILL.md`，解析会**改回**内嵌目录，顶层 322 行文档将再次被静默屏蔽。

## 产物路径（2026-09-26 起迁出）

GEM 生成的 `*_ideas.md` 不再写进本目录（此前会把产物混入仓库 skill 树），
改由 `pipeline_reports.save_ideas_report()` 写到 **`GEM_REPORT_ROOT`**（= `GEM_DATA_ROOT/output_report`
= 仓库 `data/gem_runs/output_report/`，与 `data/` 同源，可用 `WQB_GEM_DATA_ROOT` 覆盖）。

## 变更纪律

- 改动 `scripts/`（`ace_lib` / `validator` / `pipeline_*`）需回归 GEM 全链路：
  `python tools/sync_skills.py` 后跑 `pytest tests/ -x`。
- 顶层 skill 的正文更新**不自动**传导到本目录；`SKILL.md` 由上面第 1 条的测试守护，
  其余资产如涉及引擎 prompt 语义，需手动同步并在此登记。
- **不要**用 `tools/sync_skills.py` 覆盖本目录的 `scripts/`，也**不要**把本目录当作顶层 skill 同步到安装位。
