# PPA 人工提交交接单：mL6Ozm72

> agent 到这里**停下并交接**：web UI 提交是人工通道，agent 不执行、不重复催。用户提交后运行 `python tools/ppa_handoff.py record --alpha-id <ID>` 回写。

- 区域 / universe / delay：USA / TOP3000 / D1
- 平台状态：UNSUBMITTED（须为 UNSUBMITTED 才需要提交）
- 表达式：`ts_decay_linear(group_rank(ts_zscore(ts_backfill(vec_avg(fnd110_original_value_fast_d1), 252), 252), subindustry), 200)`
- IS：Sharpe 1.29、Fitness 0.77、Turnover 0.015

## 自动核对（口径见 `wqb.config.compute_webdata_failed_counts`；判据数字见 submit-alpha 文档，本环境未向平台复核）
- Failed PPA = 0 ✔
- PPA 名单内仍 PENDING：无（有则待其算完再交接）
- Sharpe ≥ 1.0：1.29 ✔
- 算子 ≤ 8：调用 5 次 / 去重 5 个 ✔（平台按哪种口径数未在文档写明，两个都列）
- 字段 ≤ 3：2 个 ✔

## 必须由人核对（agent 无法确认）
- PPAC < 0.5：0.4885  ✔
- 当期活跃 Power Pool **主题窗口**（平台右上角铃铛；`MATCHES_THEMES` = PASS 才受理；非活跃区域报 "does not match any Power Pool Theme"）：**待填**
- 已准备好的属性：name（`<REGION>_<R|S>_<family>_<seq>`）、color `PURPLE`、tags `CH_PPA` + `SRC_<数据集>` + `PowerPoolSelected`、三段式 description（≥100 词）——见 `docs/alpha_properties_spec.md`

## 用户不在线时
候选留在提交队列（`submit_ready` 表，status 不变），**不重复催、不改走 MCP 通道**（MCP 预检会拦合法 PPA）。
