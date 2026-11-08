# DEU Fundamental ATOM 战役 · Wave F1 设计（2026-11-07）

> 目标：10 颗 ATOM regular alpha（单数据集），DEU/TOP500/D1。本波 = A 批 fundamental45 模板池 10 条 + B 批存在性探针 8 条（fnd90×6 + fnd22×2）。
> 设置：decay 4 / SUBINDUSTRY / trunc 0.08 / nanHandling OFF / pasteurization ON / VERIFY / maxTrade OFF。并发 = 2 个 multisim。

## 机制取证（派发前，用户纪律）
1. 论坛 QW94165（44 赞）《Earnings 数据集实战指南》：call_sentiment 语调是核心信号；**事件字段先 ts_backfill 再短窗**；事件后 3-10 天是最强窗口；财报事件信号与其他类别相关性低（利于 prod/self）。
2. 论坛评论区 FF45555 实证：ts_rank(252) 跨季跳变会把 Sharpe 虚高（1.3 实为 0.7）⇒ 本波一律 ts_backfill(66) + 短窗/横截面几何，不用裸长窗 ts_rank。
3. 论文：Price, Doran, Peterson & Bliss (2012) 电话会语调增量信息；Q&A 段语调显著预测 CAR；分析师负面提问 → 管理层披露更具体（specificity 中介）。Loughran & McDonald (2011) 语调词表。Lehavy et al. (2011) 可读性与信息不对称。
4. DEU 既有先验：SUBINDUSTRY 中性化基线；sub 闸 limit≈0.474×S（797 条实测）。

## A 批 · fundamental45 模板池（10 条，结构互异）

| # | 机制 | 表达式 | ops |
|---|---|---|---|
| A1 | Q&A 语调水平 | group_rank(ts_backfill(fnd45_sentiment_lm2_net_qa, 66), industry) | 2 |
| A2 | 语调环比（QoQ） | group_rank(ts_delta(ts_backfill(fnd45_sentiment_lm2_net_qa, 66), 66), industry) | 3 |
| A3 | PR-QA 腔调差（candor gap） | group_rank(subtract(ts_backfill(fnd45_sentiment_lm2_net_qa, 66), ts_backfill(fnd45_sentiment_lm2_net_pr, 66)), industry) | 4 |
| A4 | 复合分水平 | group_rank(ts_backfill(fnd45_score, 66), industry) | 2 |
| A5 | 复合分新近加权 | group_rank(ts_decay_linear(ts_backfill(fnd45_score, 66), 20), industry) | 3 |
| A6 | 可读性（复杂度反向） | -group_rank(ts_backfill(fnd45_readability_executives, 66), industry) | 2 |
| A7 | 数字密度（specificity） | group_rank(ts_backfill(fnd45_numeric_perct_qa, 66), industry) | 2 |
| A8 | LDA 主题显著度 | group_rank(ts_backfill(fnd45_lda_bigram_pr, 66), industry) | 2 |
| A9 | CEO 情绪变化 | group_rank(ts_backfill(fnd45_sentiment_chanage_ceo, 66), industry) | 2 |
| A10 | CEO vs 其他高管情绪差 | group_rank(subtract(ts_backfill(fnd45_sentiment_chanage_ceo, 66), ts_backfill(fnd45_sentiment_chanage_othr, 66)), industry) | 4 |

## B 批 · 存在性探针（8 条）

| # | 表达式 | 假设 |
|---|---|---|
| B1 | group_rank(ts_backfill(fnd90_qes_gamef_pscore, 252), industry) | 质量 P 分 + |
| B2 | -group_rank(ts_backfill(fnd90_qes_gamef_ohlson, 252), industry) | O-score 高=困境 − |
| B3 | group_rank(ts_backfill(fnd90_game_cash_flow_coverage, 252), industry) | 现金流覆盖 + |
| B4 | group_rank(ts_backfill(fnd90_game_deferred_sal_chg, 252), industry) | 递延收入变化 ± |
| B5 | group_rank(ts_backfill(fnd90_qes_gamef_icfroe_5y, 252), industry) | 5y 投资现金流 ROE + |
| B6 | -group_rank(ts_backfill(fnd90_game_inventory_chg, 252), industry) | 存货增长=需求隐忧 − |
| B7 | group_rank(ts_backfill(vec_avg(fnd22_value), 252), industry) | ESG KPI 水平 ± |
| B8 | group_rank(ts_delta(ts_backfill(vec_avg(fnd22_value), 252), 66), industry) | ESG KPI 动量 ± |

## 判读预案（三分法）
- S≥1.58 且 2Y>1.58 → 全闸验证（sub/prod MCP/self/逐年覆盖）。
- S 1.0-1.58 → 归因后升杠杆（窗口谷/算子替换/group_zscore），不盲扫。
- 批内 max|S|<0.5 且 longCount 正常 → 该字段族快杀；longCount=0 → 无数据判死（记录口径「连续空窗」）。
- 存在性探针首查 longCount/逐年覆盖（fundamental90 若 TOP500 无数即封存）。

## 存档索引
- 字段目录：tracking/DEU/atom_fundamental/fields/<ds>_fields.json（12 集全量）
- 画像汇总：tracking/DEU/atom_fundamental/field_profiles_20261107.md
