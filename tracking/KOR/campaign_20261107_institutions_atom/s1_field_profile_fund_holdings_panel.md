# S1 · fund_holdings_panel 全字段画像（KOR / TOP600 / D1）

> 数据源：MCP `get_datafields(dataset_id=fund_holdings_panel, region=KOR, universe=TOP600, delay=1, **filter_sharpe=false**)`
> 返回 `count=30 / platform_count=30 / complete=true` ⇒ **30/30 全覆盖，无截断**。
> ⚠ 本集在 KOR 有历史判死记录 `KOR-FUND-HOLDINGS-PANEL-DEAD`（"event-aggregate flow fields here are noise"）。
> 本文件逐字段标明「判死族 / 未判死」，**未判死轴才允许进回测**。

## 0. 数据集级事实

| 项 | 值 |
|---|---|
| 数据集 | `fund_holdings_panel` · Global Institutional Fund Holdings |
| 平台 cov | **.8093**（TOP600 约 8 成标的） |
| 字段数 | **30**：MATRIX 12 + **VECTOR 18** |
| 披露节奏 | 日频铺平，但账户级持仓以**月度/季度**更新（`_active` 族为「活跃账户」子样本） |
| 关键陷阱 | VECTOR 字段必须 `vec_*` 聚合；且 `.6626` 覆盖族在 TOP600 上只剩 ~66% 标的 |

## 1. MATRIX 12 字段（存量 / 集中度 / 信念）

| # | 字段 | cov | aC | user | 语义 | 取值域 | 分布 | 频率 | 判死状态 | 可用性 |
|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | `holder_account_total` | .9553 | 30 | 21 | 持有该 ISIN 的**账户/基金数** | ≥0 整数 | 右偏，多为几十–几百 | 月/季 | ✅ 未判死 | ⭐ **广度轴**（Chen-Hong-Stein） |
| 2 | `top_weighted_account_number` | .9553 | 15 | 12 | 把该股列为**信念持仓**（权重 top30%）的账户数 | ≥0 整数 | 右偏、零堆积高 | 月/季 | ✅ 未判死 | ⭐ **信念广度轴** |
| 3 | `mean_security_weight` | .9553 | 12 | 10 | 持仓账户内该股的**平均权重**（占 AUM） | (0,1] | 右偏、0 附近堆积 | 月/季 | ✅ 未判死 | ⭐ **信念强度轴** |
| 4 | `security_holding_usd_value` | .9553 | 7 | 6 | 全体账户持有该股的**美元总额** | ≥0 美元 | 重尾最重 | 月/季 | ✅ 未判死 | 规模轴（必须比率化） |
| 5 | `herfindahl_index_holdings` | .9553 | 31 | 26 | 按账户权重算的**HHI 集中度** | (0,1] | 右偏、集中在小值 | 月/季 | ✅ 未判死 | ⭐ **拥挤度轴** |
| 6 | `holding_value_distribution_score` | .9553 | 19 | 17 | 持仓市值在账户间的**集中度自定义分** | 0–1 | 右偏 | 月/季 | ✅ 未判死 | 与 #5 共线，**二选一** |
| 7 | `holder_account_total_active` | .7666 | 6 | 6 | #1 的活跃账户子样本 | ≥0 整数 | 同 #1 | 月/季 | ⚠ 覆盖不足 | 仅作 #1 的灵敏度对照 |
| 8 | `top_weighted_account_number_active` | .7666 | 11 | 10 | #2 的活跃子样本 | ≥0 整数 | 同 #2 | 月/季 | ⚠ 覆盖不足 | 对照 |
| 9 | `mean_security_weight_active` | .7666 | 10 | 10 | #3 的活跃子样本 | (0,1] | 同 #3 | 月/季 | ⚠ 覆盖不足 | 对照 |
| 10 | `security_holding_usd_value_active` | .7666 | 6 | 6 | #4 的活跃子样本 | ≥0 美元 | 同 #4 | 月/季 | ⚠ 覆盖不足 | 对照 |
| 11 | `herfindahl_index_holdings_active` | .7666 | 11 | 11 | #5 的活跃子样本 | (0,1] | 同 #5 | 月/季 | ⚠ 覆盖不足 | 对照 |
| 12 | `holding_value_distribution_score_active` | .7666 | 7 | 6 | #6 的活跃子样本 | 0–1 | 同 #6 | 月/季 | ⚠ 覆盖不足 | 对照 |

**`_active` 族统一裁定**：覆盖率 .7666 < 主信号门槛 .90 ⇒ **不单独作主信号**，只在主族成功后做「子样本稳健性」对照。

## 2. VECTOR 18 字段（流量 / 交易事件）

| # | 字段 | cov | aC | 判死状态 | 裁定 |
|---|---|---|---:|---|---|
| 13 | `stable_boundary_trade_count_21d` | .887 | 13 | ✅ **未判死** | ⭐ **持久建仓/清仓计数**（同账户 21 交易日内无反向边界交易）——唯一保留的流量轴 |
| 14 | `stable_boundary_trade_count_21d_active` | .6626 | 1 | ⚠ 覆盖不足 | 不用 |
| 15 | `boundary_transaction_total` | .887 | 35 | ⛔ 判死族 | 不投 |
| 16 | `boundary_transaction_usd_value` | .887 | 6 | ⛔ 判死族 | 不投 |
| 17 | `boundary_transaction_total_active` | .6626 | 4 | ⛔ 判死 + 覆盖不足 | 不投 |
| 18 | `boundary_transaction_usd_value_active` | .6626 | 2 | ⛔ 判死 + 覆盖不足 | 不投 |
| 19 | `transaction_account_total` | .887 | 6 | ⛔ 判死族 | 不投 |
| 20 | `transaction_account_total_active` | .6626 | **0** | ⛔ 判死 + **平台 0 用户 0 alpha（疑空字段）** | 不投 |
| 21 | `herfindahl_index_transactions` | .887 | 2 | ⛔ 判死族 | 不投 |
| 22 | `herfindahl_index_transactions_active` | .6626 | 5 | ⛔ 判死 + 覆盖不足 | 不投 |
| 23 | `large_trade_count_50bps` | .887 | 3 | ⛔ 判死族 | 不投 |
| 24 | `large_trade_count_50bps_active` | .6626 | 1 | ⛔ 判死 + 覆盖不足 | 不投 |
| 25 | `security_transaction_usd_value` | .887 | 3 | ⛔ 判死族 | 不投 |
| 26 | `security_transaction_usd_value_active` | .6626 | 1 | ⛔ 判死 + 覆盖不足 | 不投 |
| 27 | `top_weighted_transaction_number` | .887 | 8 | ⛔ 判死族 | 不投 |
| 28 | `top_weighted_transaction_number_active` | .6626 | 1 | ⛔ 判死 + 覆盖不足 | 不投 |
| 29 | `transaction_value_distribution_score` | .887 | 4 | ⛔ 判死族 | 不投 |
| 30 | `transaction_value_distribution_score_active` | .6626 | 3 | ⛔ 判死 + 覆盖不足 | 不投 |

**VECTOR 聚合口径（若使用 #13）**：`vec_sum(stable_boundary_trade_count_21d)` = 当日全账户持久边界交易总数；
`vec_avg(...)` = 户均。二者经济含义不同：`vec_sum` = 全市场强度，`vec_avg` = 单账户强度 ⇒ **两个都测，只留优者**。

## 3. 数据清理 / 对齐 / 去噪 / 标准化

| 步骤 | 手法 | 理由 |
|---|---|---|
| VECTOR 聚合 | `vec_sum` / `vec_avg` 二选一，先测两条 | 聚合口径换 = 换信号 |
| 去量纲 | 一律 `group_rank(·, sector)` 或 `ts_rank(·, W)` | 账户数字段跨标的差 3–4 个数量级 |
| 时序平滑 | 广度/权重类用 `ts_mean(·, 63)`；持久流量用 `ts_sum(·, 21)` | 月/季更新 ⇒ 63d 平滑掉披露阶梯 |
| 反转归一 | 变化率除以自身滞后水平 `+1` | 防小基数爆炸 |
| NaN | 覆盖 .9553 / .887 ⇒ 保留 `nanHandling=OFF`，必要时 `ts_backfill(·, 21)` | 与 KOR 合法档一致 |
| 禁用 | 一切 `boundary_transaction_*` / `transaction_*` / `large_trade_*` / `*_distribution_score` | 历史判死族，遵守 `KOR-FUND-HOLDINGS-PANEL-DEAD` |

## 4. 可开的 5 条轴（本集白名单）

| 轴 | 字段组合 | 经济机制 | 备注 |
|---|---|---|---|
| A 持有人广度 | `holder_account_total` 变化率 | Chen-Hong-Stein (2002)：广度扩张 ⇒ 卖空约束放松 ⇒ 正向漂移 | 主推 |
| B 信念广度 | `top_weighted_account_number` / `holder_account_total` | 高信念账户占比 ⇒ 聪明钱集中 | 主推 |
| C 信念强度 | `mean_security_weight` 变化 | 现有持有人加仓 ⇒ 信息优势方加码 | 主推 |
| D 拥挤度 | `herfindahl_index_holdings` | 持仓集中 ⇒ 拥挤交易 ⇒ 未来反转 | 需测反向 |
| E 持久流量 | `vec_sum(stable_boundary_trade_count_21d)` | 剔除往返噪声后的**净建仓**信号 | 唯一保留流量轴 |

## 5. 与历史判死记录的对齐

| 判死条目 | 覆盖范围 | 本文件如何遵守 |
|---|---|---|
| `KOR-FUND-HOLDINGS-PANEL-DEAD`（"event-aggregate flow fields here are noise"） | **仅** event-aggregate flow / concentration | §2 中 16 个字段全部列入「不投」；§4 白名单只留 #13（带 21 日持久性过滤，非 event-aggregate）+ 6 个 MATRIX 存量字段 |
| 跨区：institutions6 作主信号判死 | 裸水平直用 | 本集不使用 institutions6；panel 侧只走 §4 五轴 |

## 6. 落盘与索引

- 本文件 = `tracking/KOR/campaign_20261107_institutions_atom/s1_field_profile_fund_holdings_panel.md`
- 姊妹文件：`s1_field_profile_institutions6.md`（11 字段）
- 上游：`s0_dataset_scan.md` · 下游：`s2_mechanism_evidence.md` → `waves.md`
