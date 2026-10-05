# Examples

## 触发短语
- 「帮我批量回测这个 alpha_list.json，并保存进 simulation_status.csv」
- 「继续上次中断的 batch simulation（断点续传）」
- 「把并发降到 1 重跑失败项」
- 「统计 simulation_status.csv 里 COMPLETE / ERROR 数量」

（「批量提交 alpha」不是本 skill 的触发词——这里只**发起回测**；提交 alpha 是 L5。战役目录内的整波回测用 `workflow_batch_track`，见 SKILL 入口选用表。）

## 预期行为
- 用本目录的 `scripts/batch_simulator.py`；凭据由脚本自己读取（环境变量 `CREDENTIALS_*` → `configs/config.json`，agent 不读 `.env`、不打印口令）。
- 结果以 CSV 与 `status` 分布汇报，而不只看终端 tail；结果同时在 `backtest_results`。

## 推荐命令形态（占位）
- `& $WQ_PY scripts/batch_simulator.py --config configs/config.json --alpha-json data/alpha_list.json --output-csv outputs/simulation_status.csv --batch-size <B> --concurrency <C> --detached`
- `& $WQ_PY scripts/batch_simulator.py --status "<task_id>" --tail-lines 60`
