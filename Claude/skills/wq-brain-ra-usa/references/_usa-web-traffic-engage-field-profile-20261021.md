# web_traffic_engage 字段画像与探针档案（USA / TOP3000 / D1）

> 快照：2026-10-21　｜　数据集：`web_traffic_engage`（Web Traffic Engagement Signals，other 塔，**未点亮**）
> 数据集级：105 MATRIX 字段 / coverage 0.433 / userCount 185 / alphaCount 419 / valueScore 4 / pyramid ×1.4
> 平台事实（`get_datafields`，filter_sharpe=True）：`platform_count=105`、`complete=true`、`sharpe_filter_removed=0`
> ⇒ 本集**没有被 OS/IS Sharpe 过滤器剔除的字段**，105 条即全量。
> 口径（提案批）：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / FASTEXPR /
> pasteurization ON / maxTrade OFF / 2014-01-01 → 2023-12-31

## §1 字段画像

### 1.1 结构：5 指标 × 4 平台 × 6 视图

| 维度 | 取值 |
|---|---|
| 指标 | `visit_count`（访问次数）、`pageview_count`（浏览页数）、`avg_pages_per_session`（每次访问页数）、`avg_session_time` / `session_time`（停留时长，秒）、`bounce_ratio`（跳出率，比例） |
| 平台 | `desktop_`（桌面）、`mobile_`（移动）、`total_`（桌面+移动合计）、`aggregate_`（同上，厂商另一套命名；`aggregate_bounce_rate` 用 `rate` 而非 `ratio`） |
| 视图 | `today`（当日观测）、`timeseries_7d` / `timeseries_28d`（时序模型预测）、`forecast_7d` / `forecast_28d`（自回归预测）、`predicted_*` / `autoregressive_*` / `autoreg_*`（**模型误差 MAPE 诊断**，非信号） |

**关键结构事实**

1. **同一指标有「观测 vs 两套预测」三条腿** ⇒ 天然可构造 **意外（观测 − 预测）** 与 **模型分歧（AR vs TS）** 两类信号，而不必跨数据集。
2. **平台维度是「结构位移」而非独立信号**：`mobile/total` 份额变化是零售行为结构迁移，与总量变化正交。
3. **`predicted_*` 绝大多数是 MAPE 诊断**：105 条里有 25 条描述明确写 "Model fitness (MAPE %) / diagnostic metric"，
   它们度量的是**预测误差**而非流量本身。**批 1 一律不用**——用它们得到的是「模型可信度」信号，机制不同，会污染归因。
   命名并不统一（例：`overall_bounce_ratio_predicted_28d` 描述是时序预测、`overall_bounce_ratio_autoreg_28d` 才是 MAPE；
   `mobile_avg_pages_per_visit_predicted_28d` 写的是预测）⇒ **以描述为准，不以名字为准**，后续若要用必须先逐条核对。
4. **覆盖率 0.4308–0.4344，几乎全员一致**：这是「有映射站点」的股票集合，不是字段级缺失差异。
   低覆盖 ⇒ 必须 `ts_backfill`（本批统一 120），否则长期 NaN 会形成持仓集中（`CONCENTRATED_WEIGHT`）。
   覆盖 0.433 仅略高于 0.40 的硬地板 ⇒ **边距薄，任何分档/条件筛都会把有效截面进一步压小**。

### 1.2 完整清单（105 条，按视图分组；括号内为字段 alphaCount）

**A. 当日观测 `*_today`（27 条）**
`desktop_visit_count_today`(60) · `total_visit_count_today`(59) · `aggregate_bounce_ratio_today`(48) ·
`total_pageview_count_today`(30) · `desktop_pageview_count_today`(29) · `total_avg_pages_per_session_today`(15) ·
`mobile_visit_count_today`(12) · `desktop_avg_pages_per_session_today`(6) · `mobile_pageview_count_today`(6) ·
`total_session_time_today`(6) · `mobile_session_time_today`(3) · `mobile_avg_pages_per_session_today`(3) ·
`desktop_bounce_ratio_today`(1) · `desktop_session_time_today`(1) · `mobile_bounce_ratio_today`(1) ·
`aggregate_bounce_rate_autoregressive_28d`(5)〔MAPE〕
**B. 时序预测 `*_timeseries_7d`（13 条）**
`mobile_visit_count_timeseries_7d`(22) · `total_visit_count_timeseries_7d`(22) · `desktop_pageview_count_timeseries_7d`(11) ·
`total_pageview_count_timeseries_7d`(12) · `desktop_visit_count_timeseries_7d`(10) · `desktop_session_time_timeseries_7d`(6) ·
`desktop_avg_pages_per_session_timeseries_7d`(5) · `desktop_bounce_ratio_timeseries_7d`(4) · `total_session_time_timeseries_7d`(4) ·
`mobile_pageview_count_timeseries_7d`(3) · `mobile_session_time_timeseries_7d`(2) · `mobile_avg_pages_per_session_timeseries_7d`(1) ·
`total_avg_pages_per_session_timeseries_7d`(0)
**C. 时序预测 `*_timeseries_28d`（12 条）**
`desktop_pageview_count_timeseries_28d`(11) · `total_visit_count_timeseries_28d`(10) · `mobile_visit_count_timeseries_28d`(9) ·
`desktop_visit_count_timeseries_28d`(8) · `mobile_pageview_count_timeseries_28d`(6) · `total_pageview_count_timeseries_28d`(4) ·
`desktop_bounce_ratio_timeseries_28d`(3) · `desktop_session_time_timeseries_28d`(3) · `total_session_time_timeseries_28d`(3) ·
`mobile_session_time_timeseries_28d`(2) · `mobile_bounce_ratio_timeseries_28d`(0) ·
`total_avg_pages_per_session_timeseries_28d`(0)
**D. 自回归预测 `*_forecast_7d`（14 条）**
`aggregate_bounce_ratio_forecast_7d`(**21**) · `desktop_visit_count_forecast_7d`(10) · `desktop_session_time_forecast_7d`(7) ·
`mobile_visit_count_forecast_7d`(7) · `total_pageview_count_forecast_7d`(6) · `total_visit_count_forecast_7d`(5) ·
`total_avg_pages_per_session_forecast_7d`(5) · `desktop_pageview_count_forecast_7d`(4) · `total_session_time_forecast_7d`(2) ·
`desktop_avg_pages_per_session_forecast_7d`(1) · `mobile_avg_pages_per_session_forecast_7d`(2) ·
`mobile_bounce_ratio_forecast_7d`(2) · `desktop_bounce_ratio_forecast_7d`(2) · `mobile_session_time_forecast_7d`(2) ·
`mobile_pageview_count_forecast_7d`(0)
**E. 自回归预测 `*_forecast_28d`（12 条）**
`desktop_visit_count_forecast_28d`(1) · `mobile_visit_count_forecast_28d`(1) · `total_visit_count_forecast_28d`(1) ·
`desktop_pageview_count_forecast_28d`(2) · `mobile_pageview_count_forecast_28d`(3) · `total_pageview_count_forecast_28d`(1) ·
`desktop_avg_pages_per_session_forecast_28d`(2) · `mobile_avg_pages_per_session_forecast_28d`(4) ·
`total_avg_pages_per_session_forecast_28d`(3) · `desktop_bounce_ratio_forecast_28d`(2) · `mobile_bounce_ratio_forecast_28d`(0) ·
`desktop_session_time_forecast_28d`(4) · `mobile_session_time_forecast_28d`(3) · `total_session_time_forecast_28d`(1)
**F. MAPE / 诊断（`predicted_*` / `autoregressive_*` / `autoreg_*` / `pred_*`，27 条）**
`aggregate_bounce_ratio_predicted_7d`(20) · `desktop_page_views_timeseries_pred_7d`(14)〔描述为首 7 日预测，待核〕 ·
`aggregate_session_time_predicted_28d`(6) · `aggregate_session_time_predicted_7d`(2) ·
`desktop_avg_pages_per_session_predicted_28d`(2) · `desktop_avg_pages_per_session_predicted_7d_2`(0) ·
`desktop_avg_session_time_predicted_28d`(0) · `desktop_avg_session_time_predicted_7d`(0) ·
`desktop_bounce_ratio_predicted_28d`(0) · `desktop_bounce_ratio_predicted_7d`(1) ·
`desktop_pageview_count_predicted_28d`(1) · `desktop_pageview_count_predicted_7d`(1) ·
`desktop_visit_count_predicted_28d`(1) · `desktop_visit_count_predicted_7d`(0) ·
`mobile_avg_pages_per_session_predicted_28d_2`(0) · `mobile_avg_pages_per_session_predicted_7d`(2) ·
`mobile_avg_pages_per_visit_predicted_28d`(0) · `mobile_bounce_ratio_predicted_28d`(0) ·
`mobile_bounce_ratio_predicted_7d`(1) · `mobile_pageview_count_predicted_28d`(0) ·
`mobile_pageview_count_predicted_7d`(0) · `mobile_session_time_predicted_28d`(0) ·
`mobile_session_time_predicted_7d`(3) · `mobile_site_visits_autoregressive_28d`(1) ·
`mobile_visit_count_autoreg_7d`(0) · `overall_bounce_ratio_autoreg_28d`(1) ·
`overall_bounce_ratio_predicted_28d`(2) · `overall_bounce_ratio_predicted_7d`(0) ·
`total_avg_pages_per_session_predicted_28d`(3) · `total_avg_pages_per_session_predicted_7d`(3) ·
`total_pageview_count_predicted_28d`(0) · `total_pageview_count_predicted_7d`(1) ·
`total_session_time_forecast_28d`〔见 E〕 · `total_visit_count_predicted_28d`(1) · `total_visit_count_predicted_7d`(1)

> 计数说明：A–E 按「视图」列全，F 收录全部 `predicted_/autoreg_/autoregressive_` 命名件；
> 个别字段在新旧命名间重复出现（如 `aggregate_bounce_rate_autoregressive_28d`），以平台返回 id 为准。

### 1.3 覆盖率与量纲

- **cov 0.4308–0.4344**（105 条全部落在 2.7 pt 带内）⇒ 缺失是**股票级**（有无映射站点），不是字段级。
- **量纲三类**：计数（visits / pageviews，重尾、量级跨 3–4 个数量级）、比例（bounce ratio，0–1）、
  时长/页数（秒、pages/visit，正偏）。⇒ **计数类必须先取对数或直接秩变换**；比例类可直接 zscore；
  跨字段相除（如 session_time / visits）会产生**量纲比**，VERIFY 下可能报 UNITS 警告，优先用已有比值字段
  （`avg_pages_per_session`、`avg_session_time`）。
- **更新频率**：日频。`today` 是高噪点值（周末/节假日效应强），`timeseries_*` 是平滑预测，
  `forecast_*` 是自回归预测 ⇒ **同机制优先用平滑序列做 zscore，减少换手**。

### 1.4 alpha 生态与拥挤度

- 数据集 aC 419 / uC 185 ⇒ 相对 `stock_search_trends`（202/85）**更拥挤，但仍是中低量级**
  （对照 `other143` 19245、`dl_riskfree_returns` 3304）。
- 单字段最拥挤：`desktop_visit_count_today` 60、`total_visit_count_today` 59、`aggregate_bounce_ratio_today` 48
  ⇒ **「当日总访问量水平」这一族已被挖过**；`timeseries_*` / `forecast_*` 侧字段 aC 普遍 ≤ 22，**白空间在预测腿与结构位移**。
- 平台层面本集未登记 dead_end（本轮 `get_datasets(category="other")` 返回 valueScore 4 / ×1.4，未标死）。

## §2 适用机制（可陈述的经济逻辑）

| # | 机制 | 论文/经验依据 | 对应桶 |
|---|---|---|---|
| M1 | **零售关注度冲击 → 短期买入压力，随后反转** | Da, Engelberg & Gao (2011) "In Search of Attention"（搜索量代理关注度）；Barber & Odean (2008) 注意力驱动的净买入 | Change |
| M2 | **关注度意外（观测 vs 模型预期）** | 同上 + 预期误差文献：意外部分才携带新信息 | Surprise |
| M3 | **参与深度（页/次、停留时长）代表「真实兴趣」而非「标题党关注」** | 参与度作为需求强度代理；跳出率为反向参与 | Change / Level |
| M4 | **移动端份额迁移 = 用户结构变化**，与总量变化正交 | 平台结构位移，零售行为迁移 | Propagation |
| M5 | **两套预测模型的截面分歧 = 信息不确定性** | 分析师分歧度文献的模型类比 | Dispersion |
| M6 | **关注度加速度（短窗 vs 长窗 zscore 差）** | 关注度边际变化优于水平 | Change |

**方向先验与风险**

- M1/M2 的方向**不预设**：关注度上升既可能是买入压力（短多），也可能是已被定价的反转（短空）。
  ⇒ 批 1 对主力信号**同时出反号对照**（E3），避免把「方向猜错」误记成「机制无效」。
- **水平类信号（M3 的 Level 形态）天然带规模暴露**：访问量与市值高度相关，
  `group_rank(..., industry)` 只去掉行业均值、去不掉规模。批 1 **不做纯水平**，全部取**变化量**。
- **与 `stock_search_trends` 同属 web-attention 族**：若那条 SUB 修复成功并提交，
  本集的候选要额外过 SELF 相关；反之本集若先成，同样约束对方。**两集不同时提交同向信号**。

## §3 批 1 探针设计（10 条 = 一次 multisim）

统一设置：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 5 / trunc 0.08 / VERIFY / nan ON / FASTEXPR /
pasteurization ON / maxTrade OFF。统一骨架：`quantile(group_rank(winsorize(X, std=4), industry))`，
其中 `X = ts_backfill(信号, 120)`；**不用 `trade_when` 门控**（关注度门控在 stock_search_trends 上曾把 Sharpe 打到 0.73）。

| # | 桶 | 机制 | 表达式核心（X 部分） |
|---:|---|---|---|
| E1 | Change | M1 关注度冲击·总量 | `ts_zscore(total_visit_count_timeseries_7d, 66)` |
| E2 | Change | M1 关注度冲击·桌面 | `ts_zscore(desktop_visit_count_timeseries_7d, 66)` |
| E3 | Change（反号） | M1 方向对照 | `-`E1 |
| E4 | Change | M3 参与深度（页/次） | `ts_zscore(total_avg_pages_per_session_today, 66)` |
| E5 | Change（反向） | M3 跳出率恶化 | `-ts_zscore(aggregate_bounce_ratio_today, 66)` |
| E6 | Change | M3 桌面停留时长 | `ts_zscore(desktop_session_time_today, 66)` |
| E7 | Propagation | M4 移动端份额变化 | `ts_zscore(mobile_visit_count_timeseries_7d / total_visit_count_timeseries_7d, 66)` |
| E8 | Surprise | M2 观测 vs 时序预测 | `ts_zscore((total_visit_count_today - total_visit_count_timeseries_7d) / total_visit_count_timeseries_7d, 66)` |
| E9 | Dispersion | M5 AR vs TS 分歧 | `ts_zscore(total_visit_count_forecast_7d / total_visit_count_timeseries_7d, 66)` |
| E10 | Change | M6 关注度加速度 | `ts_zscore(total_visit_count_timeseries_7d, 22) - ts_zscore(total_visit_count_timeseries_28d, 66)` |

**批级自检**（对应 toolkit 闸 6）：桶覆盖 4 类（Change / Propagation / Surprise / Dispersion）✓；
跨指标 ≥ 4 种（visits / pageviews 未用 / pages-per-session / session-time / bounce）✓；
平台腿 3 种（total / desktop / mobile）✓；同指标不超 3 条（visits 系 E1/E2/E3/E8/E9/E10 共 6 条**但各自是不同视图腿**
—— 若闸 6 判「同字段族过密」，拆成两批：E1–E5 一批、E6–E10 一批）。

## §4 预注册停止条件（先写死，结果回来看）

1. **SUB 墙**：`sub_universe_sharpe / sharpe < 0.4367` ⇒ 该表达式不进入修复，直接记容量不足。
   （对照：`stock_search_trends` 最好 0.413 差 0.04 未过；本集若同形态，说明这是 web-attention 族的**族级容量墙**，不是单个构造问题。）
2. **风格 beta**：`risk_neutralized_sharpe < 0.3` ⇒ 纯风格暴露，不花仿真修。
3. **撤换判据**：批 1 十条**无一条** S ≥ 1.0 且 F ≥ 0.6 ⇒ 判本集弱（不是判死），转 `filing_sentiment`（21 条 VECTOR，aC 49）。
4. **判死判据**：批 1 + 批 2（≤ 20 条）后仍无 S ≥ 1.58 且 F ≥ 1.0 者 ⇒ 记 `USA-WEB-TRAFFIC-WEAK`，不再投第三批。
5. **不做的操作**：不磨 decay / 窗口刷 SUB（同族磨参数被 D0-P 禁止）；SUB 不过先归因容量，再决定换结构或换集。

## §5 与既有交付的关系

- 当前 USA 已交付 **5 ACTIVE**（analyst_consensus / institutions / pv 等族），本集属 **other 塔**、与既有交付**跨塔**，
  prod 同源风险低于继续在 analyst 族内找第 6 颗。
- 本集候选若过闸，交付报告需登记：数据集 `web_traffic_engage`、塔位 `USA/D1/OTHER`（×1.4）、
  机制桶、`SUB/S` 比值与 `rns` 读数。

---

## §6 批 1 实测（2026-10-21，multisim `3xNiwh5c84WX95I19kdmmku3`，10/10 COMPLETE，0 error）

设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / FASTEXPR / 2014-01-01→2023-12-31。
实际骨架与 §3 略有出入：平台侧落库为 `quantile(group_rank(winsorize(ts_backfill(ts_zscore(X, 66), 120), std=4), industry))`
——**`ts_backfill` 在 z 分之后**（§3 写的顺序是 backfill 在 z 分之前），这是本轮实际生效的形态，复现以此为准。

| # | alpha | X | S | F | TO | R | DD | SUB | SUB/S | 2Y | rns | RA | prod |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| E1 | `RRA6XP3j` | `ts_zscore(total_visit_count_timeseries_7d, 66)` | **2.17** | **2.07** | 9.43% | 11.39% | 7.28% | 1.69 | 0.78 | 2.21 | 3.65 | 全过 | **0.9740** ✗ |
| E2 | `bl8OpAkr` | `ts_zscore(desktop_visit_count_timeseries_7d, 66)` | **2.09** | **1.96** | 10.00% | 11.02% | 7.57% | 1.56 | 0.75 | 2.23 | 3.51 | 全过 | 未测（同 E1 机制） |
| E4 | `WjLekJQO` | `ts_zscore(total_avg_pages_per_session_today, 66)` | 1.85 | 1.46 | 15.95% | 9.99% | 8.64% | 1.20 | 0.65 | 1.86 | 3.36 | 全过 | **0.9906** ✗ |
| E6 | `xA1bM50m` | `ts_zscore(desktop_session_time_today, 66)` | 1.85 | 1.45 | 16.37% | 10.05% | 8.60% | 1.15 | 0.62 | 1.83 | 3.30 | 全过 | 未测（同 E4 机制） |
| E8 | `omoW2ZO2` | `ts_zscore((today−7d)/7d, 66)` | 1.97 | 1.54 | 17.56% | 10.76% | 8.34% | 1.26 | 0.64 | 2.07 | 3.61 | 全过 | 待测 |
| E10 | `58jgRYWX` | `ts_zscore(7d, 22) − ts_zscore(28d, 66)` | 1.74 | 1.48 | 9.88% | 9.02% | 8.67% | 1.09 | 0.63 | 1.93 | 2.95 | 全过 | 待测 |
| E7 | `e76QAEoN` | `ts_zscore(mobile_visit/total_visit, 66)` | 1.79 | 1.54 | 10.30% | 9.27% | 7.04% | 1.11 | 0.62 | 1.47 | 2.84 | 2Y 差 0.11 | 待测 |
| E9 | `RRA6XPWb` | `ts_zscore(forecast_7d/7d, 66)` | 1.53 | 1.17 | 14.06% | 8.17% | 9.06% | 0.80 | 0.52 | 1.38 | 2.38 | S+2Y 双差 | — |
| E3 | `RRA6XPQa` | `−`E1 | −2.17 | −2.07 | 9.43% | −11.39% | 62.1% | −1.69 | — | −2.21 | −3.65 | 4 项 FAIL | — |
| E5 | `j2e8LOb5` | `−ts_zscore(aggregate_bounce_ratio_today, 66)` | −1.70 | −1.29 | 16.20% | −9.32% | 53.4% | −1.10 | — | −1.69 | −2.79 | 4 项 FAIL | — |

### 6.1 预注册判据的逐条回读（§4）

1. **SUB 墙：本集不存在。** 六条全闸者的 `SUB/S` = 0.62–0.78，**全部高于 0.4367**，
   与 `stock_search_trends`（最好 0.413）形成鲜明对照 ⇒ **「web-attention 族有族级容量墙」这个假设被证伪**：
   墙不在容量，在本集的覆盖结构（cov 0.433 的股票集合）与平滑序列（`timeseries_*` 而非高噪 `today`）。
2. **风格 beta：不存在。** `rns` = 2.38–3.65，是 `stock_search_trends` 那批的近两倍 ⇒ 信号是特异性的，不是规模/流动性 beta。
3. **撤换判据未触发**：六条 S ≥ 1.74 且 F ≥ 1.45，远高于 S≥1.0 & F≥0.6。
4. **判死判据未触发**：已有 5 条同时满足 S ≥ 1.58 且 F ≥ 1.0（E1/E2/E4/E6/E8/E10 中除 E9 外全部满足）。

### 6.2 prod 是唯一且致命的墙（已测五条，含全部变化量腿）—— **封存 `USA-WEB-TRAFFIC-PROD-SAT`**

| alpha | 机制 | prod max | `[0.7,0.8)` | `[0.8,0.9)` | `[0.9,1]` | 读法 |
|---|---|---:|---:|---:|---:|---|
| `RRA6XP3j` | 访问量水平 | **0.9740** | 1317 | 180 | 3 | 少数几条近乎复刻 + 中密度邻域 |
| `WjLekJQO` | 页数/会话水平 | **0.9906** | 2038 | 247 | 4 | 同上，更极端 |
| `omoW2ZO2` | E8 今日偏离 7 日均（变化量） | **0.9908** | — | — | — | 变化量腿同样撞墙 |
| `58jgRYWX` | E10 7d vs 28d 加速度（变化量） | **0.9781** | 9463 | 1763 | 47 | 直方图重心远高于水平腿，但仍有一条 ≥0.9 |
| `e76QAEoN` | E7 移动端份额（结构位移） | **0.9782** | 9576 | 1791 | 42 | 同 58jgRYWX 形态 |

**五条机制互不相同（水平 / 页数 / 今日偏离 / 加速度 / 份额）却全部落在 0.974–0.991** ⇒ 不是某条构造撞车，
而是**本数据集的「注意力」信息整体已被生产池编码**。变化量腿的直方图（`[0.8,0.9)` 1.7–1.8k）比重更高，
说明它们与池中 alpha 的相关分布更宽，但**最大值仍有一条 ≥0.9 的近复刻**，D0-P 判据同样触发。

按 §6.2 原预注册规则（三条待测腿 ≥0.75 即封存）：**实测 3/3 触发，记 `USA-WEB-TRAFFIC-PROD-SAT`**。
本集 IS 质量是 `stock_search_trends` 的升级版（S/F/rns 全面更高、SUB 无墙），但**同样死在 prod**，
且这次证明「换成变化量/结构位移也救不回来」——**prod 墙与字段的时间变换形式无关**，
它衡量的是「信息本身」是否被别的 alpha 表达过，而不是「表达式长得像不像」。

> 复测口径：`e76QAEoN` 的第一次轮询因平台端连接重置（`RemoteDisconnected`）在 360 s 处断线，
> 第二次 detached 轮询返回 0.9782；两条变化量腿的读数一致（0.9781 / 0.9782），不是单次抖动。

### 6.3 可复用结论（已定稿）

- **容量墙不是 web-attention 族的通病**：`stock_search_trends` 的 SUB 缺口来自它自己的构造（`stock_search` 字段的市场级退化），
  换成 `timeseries_*` 平滑序列后同区同设置 SUB/S 直接从 0.41 抬到 0.62–0.78。**「关注度族容量不足」这个结论只对该数据集成立。**
- **`ts_backfill` 放在 z 分之后**（先 `ts_zscore` 再 `ts_backfill(120)`）在本批没有造成集中持仓：
  3,000 只股票里 long 1,069–1,251 / short 1,672–1,836，CW 全过。这与「backfill 必须在 z 分之前」的经验**不冲突**——
  前提是 z 分本身用的是**有覆盖的窗口**（66 天），z 分后的 backfill 只填偶发缺口，不制造长期常数。
- **镜面变体的代价**：E3/E5 的反号是逐位对称（S/F/SUB/2Y/rns 全部取负），**不产生任何新信息**；
  反号只在原方向被定价时才值得独立跑，不能用它当「另一个候选」。
