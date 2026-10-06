# brain-sim-alphas-in-batch-and-track 使用说明

本目录是**兼容 CLI 路径**（`scripts/batch_simulator.py`）：批量发起 alpha 回测，并支持基于 CSV 的断点续传。何时用它、何时改用 `workflow_batch_track` / toolkit `pipeline.py`，见 [`SKILL.md`](SKILL.md) 的「入口选用表」——**战役目录内的正式波次不走这里**。发起回测 ≠ 提交 alpha。

## 目录结构

- `configs/`：本地凭据配置（`config.json`，已被 `.gitignore`）与模板，见 `configs/README.md`
- `data/`：alpha 列表输入 JSON（如 `alpha_list.json`，样例 `alpha_list.example.json`）
- `outputs/`：状态 CSV 输出（**进度缓存**，不是跨阶段交接真相源；结果同时入库 `backtest_results`）
- `scripts/`：`batch_simulator.py`（批量提交、并发、轮询、状态落盘、断点续传）、`ace_lib.py`（BRAIN API 封装）、`diversity_enhancer.py`（可选的多样性增强，缺省关闭）

## 凭据

**agent 不读取 `.env`、不打印凭据、不把口令放命令行**；凭据由脚本自己读取。标准环境变量名 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（与 MCP 服务、toolkit 同名，在你自己的 shell 或宿主配置里设置，不要写进命令行或提交进仓库）。解析顺序：环境变量（另认旧别名 `BRAIN_EMAIL` / `BRAIN_USERNAME` / `BRAIN_PASSWORD`）→ `--config`（`configs/config.json`）→ 工作区 `world-quant-brain-mcp/.env`。`configs/config.json` 格式见 `configs/README.md`。

## 运行方式

在本目录执行（`<B>` / `<C>` 是**占位**，不是推荐值；战役内正式波次走填槽，见 `wqb-concurrency` §8）：

```powershell
& $WQ_PY scripts/batch_simulator.py --config configs/config.json --alpha-json data/alpha_list.json `
    --output-csv outputs/simulation_status.csv --batch-size <B> --concurrency <C> --detached
& $WQ_PY scripts/batch_simulator.py --status "<task_id>" --tail-lines 60      # 查询后台任务状态
```

兼容旧路径（无需立即迁移）：根目录的 `config.json`、`alpha_list.json`。

## 输出 CSV 命名规则

不传 `--output-csv` 时自动用 `outputs/<alpha_json文件名>_simulation_status.csv`（例：`data/alpha_list.json` → `outputs/alpha_list_simulation_status.csv`）：同一个 JSON 文件持续复用同一个 CSV（可断点续传），不同文件名得到不同 CSV。手动传了 `--output-csv` 则以传入路径为准。

## 断点续传规则

依赖：① 输入 alpha 内容计算得到的 `fingerprint`；② 同一个状态 CSV。同时满足（同一 CSV、alpha 内容 / settings / type 未变）会自动跳过已完成任务。不影响续传：`alpha_list.json` 改文件名、输入顺序变化。会导致重跑：换了状态 CSV、修改了 alpha 内容、更改了 fingerprint 计算逻辑。

运行日志会显示：`Resume check: recognized X/Y ... pending Z`、每批 `Resume detected: skipped N ...`、本轮 `Run summary -> skipped/submitted/completed/failed`。

## 输出 CSV 字段

`fingerprint`（续传唯一键）、`alpha_type`（`REGULAR` / `SUPER`）、`regular_expression` / `selection_expression` / `combo_expression`、`settings_json`、`simulate_data_json`（精简回测载荷）、`sim_id`、`status`（`COMPLETE` / `ERROR` / `FAIL` 等）、`alpha_id`、`pnl` / `sharpe` / `turnover` / `fitness`、`error` / `error_details`。

## 常见问题

1. **429 / `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`**：程序已内置退避重试；仍频繁 429 见 `wqb-concurrency`（孤儿模拟占槽、`WQB_GLOBAL_SLOTS` 降账户级并发）。
2. **看起来没有续传**：检查是否用了同一个状态 CSV、输入 alpha 是否被改。
3. **只想新开一轮独立任务**：换一个新的输出 CSV 文件名。
