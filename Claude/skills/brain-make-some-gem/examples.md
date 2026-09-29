# brain-make-some-gem 示例

> 流程见 [`SKILL.md`](SKILL.md)。2026-09-29 由英文旧稿重写：旧稿把 `scripts/headless_runner/run.py` 当标准入口（与 SKILL 的「标准入口 = `workflow_gem`」倒置），并把已迁走的深嵌套路径当核对位置。

## 触发例

1. 「用 EUR / analyst4 / delay1 / TOP2500 生成 VECTOR 的 GEM 表达式」
2. 「Run analyst10 in USA delay0 TOP3000 and give me final_expressions」
3. 「帮我把 KOR / model109 这波候选补一批」

## 期望行为

1. **先**跑 `workflow_campaign(stage="S2", subcommand="assemble-priors")`，再调
   `workflow_gem(region="EUR", dataset_id="analyst4", delay=1, universe="TOP2500", data_type="VECTOR")`
   （`data_type` 取自 `get_datafields`；`universe` 取自 `config.REGIONS`，不是一律 `TOP3000`）。
2. 后台任务用 `workflow_task_status(prefix="gem")` 轮询，**不 shell 翻日志**。
3. 完成后**核对落库**：`mcp__wqb-db__list_expressions(region="EUR", wave="s2_analyst4_d1")` 有行；回报 `expression_count`、`quality_estimation`、`mode_b_required` 与 `final_expressions_path`，并注明该文件不是真相源。
4. 未看到 `expressions` 行 → **不得声称步 4 成功**。

## 错误处理例

| 场景 | 期望回应 |
|---|---|
| `config.json not found` / `Missing required config fields: …` | 报告缺失的**键名**（不回显值），请用户按 `config.example.json` 建 / 补；agent 不读、不代填 `config.json` |
| `401` | 报告「凭据鉴权失败（看 `[cred]` 行的来源）」，请用户改环境变量 / `config.json`；不改管线代码 |
| **`402 Insufficient Balance`**，或「no meta.json within 90s」 | **不重试**。说明这是 LLM 余额 / 通道问题（干跑显示 OK 也不代表可用）；让用户充值，或改走手写 `manual` ideas → `ideas_file`（完全不调 LLM，见 FE 的「第 4 步」） |
| 候选不足 | 显式扩容 / 分波 / 换数据集；**不补参数变体凑数** |
