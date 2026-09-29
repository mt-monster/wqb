# trailSomeAlphas（GEM 引擎本体）

> 标准入口是 `workflow_gem`（MCP）/ `gem` 节点；流程、铁律与排障见 [`../../SKILL.md`](../../SKILL.md)，模块职责与产物路径速查见 [`../../reference.md`](../../reference.md)。
> 本目录只是引擎代码：`run_pipeline.py`（主流水线）· `pipeline_*.py` · `economic_priors.py` · `skeletons*.py` · `skill_roots.py`，以及内嵌兜底副本 `skills/`（见 [`skills/README.md`](skills/README.md)）。
> 2026-09-29 由英文旧稿重写：旧稿把已迁走的深嵌套路径当产物位置、把已废止的 `.qoder/skills` 当运行位置、教 PowerShell 设 key + 裸 `python`，
> 还列了代码里并不存在的 `MOONSHOT_MODEL` 环境变量。

## 什么时候直接跑 `run_pipeline.py`

只有 workflow 节点不可用时。日常经 `scripts/headless_runner/run.py`（凭据注入、`--detached`、`--status` / `--watch`），用法见 [`../headless_runner/README.md`](../headless_runner/README.md)。参数以 `run_pipeline.py --help` 为准。

## 前置

- **BRAIN 账号**：环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（旧别名 `BRAIN_USERNAME` / `BRAIN_EMAIL` / `BRAIN_PASSWORD` 仍认）。**不要把口令写在命令行**——`--username` / `--password` 只是兼容旧调用，会进入进程列表与 shell 历史。
- **LLM 通道**：`MOONSHOT_API_KEY`（给了 `--ideas-file` 就不调 LLM，不需要密钥）；端点 `MOONSHOT_BASE_URL`；模型用 `--moonshot-model`（缺省 `kimi-k2.6`）——**没有** `MOONSHOT_MODEL` 环境变量。
- 变量全表与缺省值见 [`docs/env_and_switches.md`](../../../../../docs/env_and_switches.md)。

## 运行（在仓库根，用 `$WQ_PY`，不需要 `cd`）

```powershell
# 生成 ideas + 渲染表达式 + 写入 expressions 表（status=gem）
& $WQ_PY Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py --data-category analyst --region USA --delay 1 --dataset-id analyst45 --universe TOP3000 --instrument-type EQUITY --data-type MATRIX
# 用现成的 ideas markdown（不调 LLM）
& $WQ_PY Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py --data-category analyst --region USA --delay 1 --dataset-id analyst45 --ideas-file <ideas.md> --universe TOP3000 --instrument-type EQUITY --data-type MATRIX
```

`--universe` 缺省 `TOP3000` **只对 USA 合理**，其它区域取 `config.REGIONS[<R>]["default_universe"]`；`--data-type` 取 `MATRIX` / `VECTOR` / `GROUP`，须与 `get_datafields` 返回的类型一致。

## 校验规则（流程内实现）

- ideas markdown 必须含带 `**Implementation Example**` 的 `**Concept**` 块（格式见 `brain-data-feature-engineering` SKILL「第 4 步」）；整份文件零块 → 直接报错。
- `--dataset-id` 必填；模板的 `{占位符}` 必须是数据集字段的后缀，对不上的被丢弃并打印 `[validate] 丢弃 …`。
- 数据集 CSV 在实现前会确保存在且可读。

## 产物

| 产物 | 位置 |
|---|---|
| ideas 报告 | `data/gem_runs/output_report/gem_{REGION}_delay{DELAY}_{DATASET}_ideas.md`（`GEM_REPORT_ROOT`；人工写的用 `manual_` 前缀） |
| 最终表达式（中间产物，**不是真相源**） | `data/gem_runs/{DATASET}_{REGION}_delay{DELAY}/final_expressions.json`（`WQB_GEM_DATA_ROOT` 可覆盖） |
| 真相源 | `data/wqb.db` 的 `expressions` 表（`status=gem`，wave = `s2_<DS>_d<DELAY>`，`--wave` 可改）；打印 `[db] expressions/<REGION>/<wave> n=…` |

旧深嵌套位（`skills/brain-feature-implementation/data/…`、`skills/brain-data-feature-engineering/output_report/…`）是历史兜底，**勿再用于新跑**。
