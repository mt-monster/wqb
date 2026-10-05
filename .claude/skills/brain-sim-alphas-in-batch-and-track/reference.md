# brain-sim-alphas-in-batch-and-track Reference

## 目录与核心文件
- `configs/`：凭据配置与模板；`data/`：alpha 输入 JSON；`outputs/`：状态 CSV 与汇总产物（进度缓存）；`scripts/`：主代码。
- `scripts/batch_simulator.py`：批量提交、并发、轮询、CSV 持久化、断点续传。`scripts/ace_lib.py`：BRAIN API 会话封装。
- 推荐输入 `data/alpha_list.json`（兼容根目录 `alpha_list.json`）；推荐输出 `outputs/simulation_status.csv`。

## 运行模板（`<B>` / `<C>` 是占位，不是推荐值）
```powershell
Set-Location "<skills_root>/brain-sim-alphas-in-batch-and-track"
& $WQ_PY scripts/batch_simulator.py --config configs/config.json --alpha-json data/alpha_list.json `
    --output-csv outputs/simulation_status.csv --batch-size <B> --concurrency <C> --detached
```

## 长任务控制
- `--detached`：后台启动并立即返回；`--task-id`：可选任务 ID；`--tasks-dir`：任务根目录（缺省 `outputs/tasks`）
- `--status <task_id>`：查询后台任务状态并退出；`--tail-lines N`：查询时输出日志尾部行数
- `--enhance-diversity never|auto|always`：多样性增强，**缺省 `never`**（增强会改写表达式，见 SKILL）

```powershell
& $WQ_PY scripts/batch_simulator.py --status "<task_id>" --tail-lines 60
```

旧路径自动 fallback：`alpha_list.json`、`config.json`。

## 续传规则
依赖 ① 同一个输出 CSV；② 同一 alpha 内容 / settings / type（同一 `fingerprint`）。

## CSV 主要字段
`fingerprint`, `alpha_type`, `sim_id`, `status`, `alpha_id`；`pnl`, `sharpe`, `turnover`, `fitness`；`error`, `error_details`。

## 超时与长跑
- 超时不等于失败：先看 CSV 是否还在更新、`status` 分布；**「进程还活着吗」看 CSV（≥ 3 分钟无更新且进程不可达才算失败），「平台仿真卡住吗」看 `WAIT_THRESHOLDS.sim_stall_min`（60 分钟）**，两者判的是不同层。
- 优先用**同一 CSV** 重跑以触发续传。
