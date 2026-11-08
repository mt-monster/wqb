# 字段画像：predictive_starmine（KOR / TOP600 / D1）

生成时间：2026-11-08 · 战役：KOR 10 颗 ATOM REGULAR · P85 备发

## 一、数据集级画像

| 维度 | 值 |
|---|---|
| category | model |
| 字段数 | 645（全 MATRIX） |
| coverage | 0.70–1.00（分层：核心族 0.97–1.00，盈利预测族 0.72–0.77） |
| alphaCount | 58 |
| userCount | 32 |
| tier / score | tier1 / 0.912 |
| 形态 | StarMine 风格的分析师修正 / 预测惊喜 / 智能估计 / 相对价值 |

**关键拥挤度观察**：本数据集绝大多数字段 alphaCount = 0–2，整集 aC 仅 58。这是本战役迄今见到的「字段级最空白」数据集，
prod 距离的先天条件优于 analyst10（aC191）。

## 二、字段族结构（按字段数）

| 族 | 字段数 | 含义 | 代表字段 | 覆盖 | aC |
|---|---|---:|---|---|---:|---:|
| mean_estimate | 109 | 一致预期及其变动（7/14/30/60/90d，f12m/fy1/fy2，earnings/revenue/ebitda） | mean_estimate_change_pct_f12m_earnings_30d | 0.74 | 0 |
| analyst_upward | 94 | 上修分析师计数（fq1/fy1，7/14/30d） | analyst_upward_revision_count_fq1_earnings_14d_4 | 0.77 | 0 |
| analyst_downward | 68 | 下修分析师计数 | analyst_downward_revision_count_fq1_earnings_14d_4 | 1.00 | 1 |
| predicted_surprise | 48 | StarMine 预测惊喜（绝对额 + pct 两种） | predicted_surprise_pct_fy1_earnings_4 | 0.74 | 0 |
| iv_projected | 40 | 内在价值模型的长期预测（DPS fy1–fy15 等） | iv_projected_dividends_fy1_3 | 1.00 | 1 |
| smest_price | 24 | SmartEstimate 目标价 | — | — | — |
| rel_val | 22 | 相对价值综合分位及各分项 | rel_val_global_rank_score_3 | 1.00 | 34 |
| arm_score | 19 | 分析师修正模型（ARM）分数 / 变化 / 排名 | arm_global_rank_score | 1.00 | 10 |
| smest_fy | 18 | SmartEstimate 财年预测 | smest_fy1_earnings_3 | 0.74 | 0 |
| recommendation_mean | 12 | 评级均值及其变动 | recommendation_mean_change_30d_3 | 0.72 | 0 |
| surprise_pct | 9 | 实际惊喜百分比 | surprise_pct_last_year_earnings_2 | 0.70 | 0 |
| ep_yield | 8 | SmartEstimate 口径收益率 | ep_yield_pct_smest_f12m | 0.99 | 15 |

## 三、经济先验（文献支撑）

- **分析师修正动量**：Womack (1996)、Chan/Jegadeesh/Lakonishok (1996) 均记录分析师修正后的价格漂移（post-revision drift），
  方向为「上修 → 后续超额收益」，且在中短期内持续。对应本集 analyst_upward/downward_revision_count 与 mean_estimate_change_pct。
- **预测惊喜**：StarMine Predicted Surprise 的设计目的即提前捕捉「实际公布将偏离一致预期」的标的；文献（如 Gleason & Lee 2003 对 SUE 的研究）
  显示惊喜方向有持续性。对应 predicted_surprise_pct_fy1/fy2。
- **修正广度 vs 修正幅度**：广度（多少分析师上调）与幅度（幅度百分比）信息不同；前者是共识转移的横截面扩散度，后者是强度，
  两者应作为独立模板而非互相替代。
- **评级动量**：recommendation_mean 数值下降通常代表评级上调（1 = strong buy 口径），故方向可能与直觉相反，需实测定号。

## 四、模板库（12 个结构互异）

| # | 模板 | 结构轴 | 表达式骨架 | 来源 |
|---|---|---|---|---|
| S1 | 修正广度价差 | 截面双秩差 | group_rank(up_count) - group_rank(down_count) | paper（Womack 1996） |
| S2 | 一致预期修订动量 | 水平 + 时序平滑 | group_rank(ts_mean(est_change_30d, 22)) | paper（CJL 1996） |
| S3 | ARM 分位水平 | 纯水平 | group_rank(arm_global_rank_score) | forum（StarMine ARM 标准用法） |
| S4 | ARM 分数变化 | 一阶变化 | group_rank(arm_score_change_7d) | forum |
| S5 | 预测惊喜水平 | 纯水平 | group_rank(predicted_surprise_pct_fy1) | paper（Gleason-Lee） |
| S6 | 预测惊喜期限结构 | 跨财年差 | fy1 - fy2 | self |
| S7 | 评级动量 | 一阶变化 | group_rank(recommendation_mean_change_30d) | self（须实测定号） |
| S8 | 相对价值综合分位 | 纯水平 | group_rank(rel_val_global_rank_score) | forum（本集最热字段 aC34） |
| S9 | 智能估计增长 | 增长率水平 | group_rank(smest_growth_next_vs_this_yr_earnings) | self |
| S10 | 短窗 ts_rank + 大 decay | 时序秩 | group_rank(ts_rank(breadth_spread, 8), country) | forum（破 prod 配方） |
| S11 | EBITDA 口径广度差 | 截面双秩差（另一口径） | up(ebitda) - down(ebitda) | self |
| S12 | 惊喜变化量 | 一阶差分 | group_rank(ts_delta(predicted_surprise_pct_fy1, 22)) | self |

## 五、P85 派发设置

- KOR / TOP600 / D1 · REVERSION_AND_MOMENTUM · decay 4 · truncation 0.08 · nanHandling ON · 2014-01-01~2023-12-31
- 12 条一并发（单批上限 10 ⇒ 拆 10 + 2）
- 算子数 2–4

## 六、风险提示

- 部分族 coverage 仅 0.70–0.77（盈利预测族），TOP600 下约 430-460 只可用；低于 0.7 的字段一律不用。
- 修订计数族属「区间累计计数」，非稀疏事件；但仍需监控 TO，若 >0.5 需改用 ts_mean 平滑而非 ts_delta。