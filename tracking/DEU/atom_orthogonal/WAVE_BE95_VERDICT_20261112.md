# BE95 判决：alpha_factor_lib 判死（慢变量，2026-11-12）

批号 `4CiApp4s24H18HjZkPJdBgD`｜DEU/TOP500/D1｜decay4/SUBINDUSTRY/trunc0.08/nan ON｜10 臂｜0 ERROR｜10/10 REJECT

背景：65 字段全 VECTOR，全平台 **alphaCount 仅 4**（172 集中最不拥挤之一），画像 cov=0——但 cov 先验已被 BE89/90 系统性证伪，故必须实测。

## 逐臂实测（表达式按平台 code 核对，非位置映射）

| # | alpha | 字段 | S | F | TO | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | A1xj7QAg | change_free_cash_flow_to_market_cap | 0.22 | 0.10 | 1.8% | 0.13 | −0.55 |
| 2 | O0WQxJ3g | change_free_cash_flow_to_total_assets | 0.29 | 0.16 | 1.1% | 0.32 | −0.55 |
| 3 | VkN13dWA | free_cash_flow_per_share_change | 0.05 | 0.01 | 1.5% | 0.07 | −0.52 |
| 4 | YPaLgxRw | fundamental_one_year_unweighted_profit_growth | **0.49** | 0.35 | 1.3% | **1.13** | **0.69** |
| 5 | j2azreqZ | change_dcf_implied_market_cap | 0.11 | 0.04 | 1.7% | 0.32 | −0.55 |
| 6 | vRAwvOWA | fundamental_retention_ratio | −0.17 | −0.07 | 1.4% | −0.72 | −0.28 |
| 7 | 1YWkzjrR | industry_one_year_growth_net_profit_estimate | 0.19 | 0.08 | 1.9% | 0.51 | 0.80 |
| 8 | KPglEJKl | bank_tier1_capital_ratio | −0.07 | −0.02 | 1.6% | 0.82 | −0.06 |
| 9 | N1PxRNXq | −bank_modified_texas_ratio_1y_change | −0.13 | −0.06 | 6.6% | 0.38 | 0.17 |
| 10 | 2r58NA1N | −insurance_combined_ratio | −0.02 | 0.00 | 0.9% | 1.11 | 0.03 |

## 判死证书

**族级死因：慢变量（年度/半年度财务口径）与 D1 频率不匹配。**

- **TO 0.9%-6.6%**（10/10 臂 ≤6.6%，7 臂 ≤2%）：这是本战役迄今最低换手的一批，与 fundamental45（TO ~10%）、institutions6（4-15%）同族死法。
- 数据在：TO 非零 + 2Y 在 0.07-1.13 间变动 ⇒ 面板有真实更新，不是空窗。
- 信号侧：max |S| **0.49**，sub 三臂为负、一臂 0.80（行业净利预期增长，机制上最"事件化"的一条，S 仍只有 0.19）。
- 唯一有形态的臂是臂 4（利润增长）：S 0.49 / 2Y 1.13 / sub 0.69 —— **近端有效、全样本拖死**，同 pv13（S 0.51 / 2Y 2.07）同一个死法。按协议 v2，|S| <1.0 直接判死，不做定向补。

**覆盖清单（协议 v2 证书要求）**：10 字段 × 1 骨架（group_zscore∘group_rank∘ts_backfill 66）——覆盖 3 个行业专属字段（银行 2 / 保险 1）与 7 个通用字段，未做矩变化（水平/变化已在字段名内禀，change_* 六条本身就是变化型）。
**未覆盖项**：窗口阶梯（22/252）、设置档 nan ON/OFF、非线性（signed_power/trade_when）——若后续需要复活，从这三项入手。

## 结论与连带

1. **alpha_factor_lib 判死**（单数据集天花板 0.49），FUNDAMENTAL 塔维持 1 席（本就距点亮差 2）。
2. 该集「alphaCount 仅 4」的低拥挤优势在信号层无价值——**不拥挤 ≠ 有信号**，与 news21/news29/news3/news76 同理。
3. 未点亮塔路径：FUNDAMENTAL 的可用面继续收敛到 fundamental6（26 字段证书封闭、oiadpq 单点 1.73 已占槽）。
