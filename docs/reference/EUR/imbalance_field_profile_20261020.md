# EUR × Imbalance 家族 — 字段画像与回测档案

> 日期：2026-10-20 ｜ 设置：TOPCS1600 / SUBINDUSTRY / decay4 / trunc0.08 / maxTrade ON / nanHandling ON
> 纪律：full-coverage，euro_equity_imbalance 三闸全过（31/31 字段 · 5 族 · 边界 0 违规）

## 一、数据集全量清单（EUR）

| 数据集 | 平台类别 | 字段 | 平均覆盖 | 已有alpha | valueScore | 评估 |
|---|---|---:|---:|---:|---:|---|
| **imbalance5** | **IMBALANCE（官方唯一）** | **2** | 0.554 | **2853** | 1.0 | 太薄：`imb5_score`（油价韧性分）+ `imb5_mktcap`（**size 代理**）；极度拥挤 |
| **euro_equity_imbalance** | OTHER | **31** | 0.309 | **443** | **4.0** | ★ 真·订单流失衡，EUR 专属 |
| order_book_imbalance | OTHER | 256 | 0.212 | 154 | 5.0 | 字段多但仅 1/5 宇宙 |
| order_flow_imb | OPTION | **0** | — | 223 | 3.0 | **EUR 不可用**（平台 get_datafields 返回 0） |

## 二、euro_equity_imbalance 字段画像（31 VECTOR，cov 0.318；bucketed 组 0.251）

| 维度 | 字段 | 经济含义 |
|---|---|---|
| **D1 激进买盘** | aggressive_buy_trade_value / aggressive_buying_participant_count / aggressive_buy_turnover_concentration_index | taker 买入成交额 / 参与人数 / 集中度 |
| **D2 激进卖盘** | aggressive_sell_trade_value / aggressive_selling_participant_count / aggressive_sell_turnover_concentration_index | 同上（卖出） |
| **D3 净失衡（核心）** | **net_aggressive_trade_value**(AGG_BUY−AGG_SELL) / **net_trade_value**(BUY−SELL turnover) / aggressive_participant_net_count / net_net_participant_count / aggressive_net_net_participant_count / net_market_share_std_rescaled / net_buying_participant_count | **已是净值字段**，无需构造价差 |
| **D4 参与者广度** | buying/selling_participant_count, net_buying/net_selling_participant_count, aggressive_net_buying/net_selling_participant_count, participant_net_count | 买卖参与者数量 |
| **D5 总成交** | total_buy_trade_value / total_sell_trade_value | 总买卖额 |
| **D6 集中度** | buy/sell_turnover_concentration_index, buy/sell_market_share_std_rescaled | HHI 类 |
| **D7 价格** | session_open_price / session_close_price | 可算日内收益 |
| **D8 分桶失衡** | bucketed_net_order_imbalance_{quantile,uniform}, bucketed_sign_imbalance_{quantile,uniform} | 参与者分桶净失衡（cov 0.251） |

- **类型**：全 VECTOR 事件型 ⇒ 必须 `vec_*` 聚合（事件层不支持算术，同 insiders/institutions）
- **覆盖**：0.318（仅 1/3 宇宙）⇒ sub/robust 天然受限
- **更新**：日频会话级

## 三、适用模板与实测

| 模板 | 骨架 | 实测最佳 |
|---|---|---|
| 净流失衡栈 | `signed_power(ts_zscore(ts_backfill(vec_sum(net_*),66),126),1.5)` | S 0.67（2Y −0.63） |
| 净流裸聚合 | `vec_sum(net_*)` | S −0.95~0.64 |
| 流量比 | `divide(vec_sum(net_agg), add(add(vec_sum(total_buy),vec_sum(total_sell)),1e-4))` | S 0.30–0.45 |
| 日内收益 | `divide(vec_avg(close), add(vec_avg(open),1e-4))` | S 0.34 |
| 集中度/分桶 | `vec_avg(concentration / bucketed_*)` | S ≤0.4 |

## 四、回测台账（30 条）

| 组 | S 区间 | 2Y 区间 | 最佳 |
|---|---|---|---|
| D3 净失衡栈（7） | −0.95~0.64 | −0.88~1.16 | `wp9axpnv` S 0.64 / 2Y 0.03 |
| D1/D2 激进买卖（6） | −0.10~0.67 | −0.63~1.42 | `j2e6R2gQ` S 0.67 / 2Y −0.63 |
| D4 参与者广度（6） | −0.51~0.62 | −1.05~0.54 | `88vp95Pm` S 0.62 / 2Y −0.37 |
| D5/D6/D7（7） | −0.25~0.53 | −1.05~0.36 | — |
| D8 分桶 + 流量比（4） | 0.02~0.48 | −0.88~0.32 | — |

**全域：S 最高 0.67（闸 1.58），2Y 系统性为负或近零。**

## 五、结论与归因
1. **官方 IMBALANCE 类别（imbalance5）不可做**：仅 2 字段，其一为 mktcap（今日已在 institutions 证明 size 代理剥掉即归零），且 2853 个 alpha 已占满
2. **euro_equity_imbalance（真订单流失衡）**：31 字段全量覆盖后 **S ≤0.67、2Y 系统性为负** ⇒ 订单流失衡在 EUR/D1 + cov 0.31 条件下已被套利
3. `order_flow_imb` 在 EUR **不存在**；`order_book_imbalance` cov 0.212 过稀
⇒ **EUR Imbalance 家族无过闸候选**

## 六、存档索引
- 字段全集：`tracking/EUR/reference/euro_equity_imbalance_fields.json`
- 覆盖闸候选：`tracking/EUR/candidates/euro_equity_imbalance.json`
