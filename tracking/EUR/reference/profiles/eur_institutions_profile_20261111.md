# EUR Institutions 塔字段画像（2026-11-11）

> 塔：INSTITUTIONS（未点亮，已提交 0/3）；universe=TOPCS1600 D1

## 一、fund_holdings_panel（Global Institutional Fund Holdings，30 字段，全 VECTOR 需 vec_* 聚合）
- **账户数族**：holder_account_total (aC 7 最热) / holder_account_total_active (aC 2) / transaction_account_total (_active)
- **集中度族**：herfindahl_index_holdings(_active) / herfindahl_index_transactions(_active) / holding_value_distribution_score(_active) / transaction_value_distribution_score(_active)
- **边界交易族**：boundary_transaction_total(_active) / boundary_transaction_usd_value(_active) / stable_boundary_trade_count_21d(_active)
- **大额交易族**：large_trade_count_50bps(_active)
- **权重族**：mean_security_weight(_active) / top_weighted_account_number(_active) / top_weighted_transaction_number(_active)
- **持仓/交易市值族**：security_holding_usd_value(_active) / security_transaction_usd_value(_active)
- cov: 0.843-0.918（全部 >0.84，覆盖良好）；aC 0-3（fund_holdings_panel 整体 alpha 拥挤度低——好信号）

## 二、institutions6（Institutions and Beneficial Stake Ownership，11 字段，全 MATRIX 免 vec 包装）
- **家数族**：count_institutional_buyers_security (aC 22 最热) / count_institutional_sellers_security (aC 24) / count_institutional_holders_security (aC 7)
- **股数族**：aggregate_share_count_institutions (aC 16) / aggregate_share_count_all_owners (aC 8) / quantity_institutional_shares_acquired (aC 18) / quantity_institutional_shares_disposed (aC 11)
- **市值族**：aggregate_equity_value_institutions (aC 8) / aggregate_equity_value_all_owners (aC 6) / market_value_institutional_shares_acquired (aC 12) / market_value_institutional_shares_disposed (aC 4)
- cov: 0.93-0.9976（覆盖优秀）；aC 4-24（拥挤度中等）

## 三、模板策略
- institutions6 全 MATRIX 免 vec 包装，是本塔主阵地（I1-I8）
- fund_holdings_panel 全 VECTOR 需 vec_* 聚合，拥挤度低（aC 0-3），留作第二波
- institutions 不在禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL}，可与任何类组腿

## 模板来源
- I1/I8 家数不对称 z：自建（机构轮换机制）
- I2 家数动量：自建（追随机构净买入）
- I3/I4 净增持：自建（机构净增持机制）
- I5 轮换强度：自建（机构轮换强度机制）
- I6 交叉确认：自建（家数×市值交叉确认）
- I7 集中度：自建（机构主导度）
- 模板库 ≥10 达标（8 条结构互异：家数/股数/市值/集中度/交叉确认/轮换强度/净增持/动量）
