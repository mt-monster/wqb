# trailSomeAlphas/skills —— GEM 引擎的捆绑（vendored）资产

> **这不是顶层 skills 的重复副本，请勿按"同步镜像"处理。**

本目录是 `brain-make-some-gem` skill 内置的 GEM 引擎（`trailSomeAlphas`）的**自包含运行时依赖**：

- `run_pipeline.py:54-56` 直接以 `BASE_DIR / "skills"` 定位本目录：
  ```python
  SKILLS_DIR = BASE_DIR / "skills"
  FEATURE_ENGINEERING_DIR   = SKILLS_DIR / "brain-data-feature-engineering"
  FEATURE_IMPLEMENTATION_DIR = SKILLS_DIR / "brain-feature-implementation"
  ```
- 引擎从 `brain-feature-implementation/scripts/` 导入 `ace_lib`、`validator`（表达式校验/平台交互），
  并读取 `brain-data-feature-engineering/` 的模板构建 prompt。

## 与顶层 skills 的关系

| 名称 | 顶层（`Claude/skills/`） | 本目录（vendored） |
|---|---|---|
| `brain-feature-implementation` | 完整版（面向 agent 调用） | 引擎运行所需的精简子集（`scripts/` 为硬依赖） |
| `brain-data-feature-engineering` | 完整版 | 引擎 prompt 模板子集 |

两者**同名不同文属设计使然**：顶层版供 agent 阅读，本目录版供 GEM 引擎离线运行。
**不要**用 `tools/sync_skills.py` 覆盖本目录，也**不要**把本目录当作顶层 skill 同步到安装位。

## 变更纪律

- 改动本目录的 `scripts/`（ace_lib/validator 等）需回归 GEM 全链路
  （`python tools/sync_skills.py` 后再跑 `pytest tests/ -x`）。
- 顶层 skill 的正文更新**不自动**传导到本目录；如涉及引擎 prompt 语义，需手动同步并在此登记。
