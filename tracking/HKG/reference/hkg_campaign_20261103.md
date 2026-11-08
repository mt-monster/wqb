# HKG 战役 2026-11-03（未点亮塔 · 30 REGULAR alpha 目标）

## 战役定义

- **目标**：HKG/D1 全部 category 塔位 **0/3**（平台 `recommend_datasets` 实测每个 category `category_alpha_count=0`），要挖 **30 个 REGULAR alpha**，最好 ATOM（单数据集）。
- **区域设置**（tracking/HKG/config/settings.json）：`HKG / TOP800 / D1 / SECTOR / decay 4 / trunc 0.08 / VERIFY / nanHandling ON / pasteurization ON / maxTrade OFF / FASTEXPR`。
- **平台闸（实测取自 2rApJ67b 的 checks）**：LOW_SHARPE **1.58** / LOW_FITNESS **1.0** / LOW_2Y_SHARPE **1.58**；LOW_SUB_UNIVERSE_SHARPE 为**比值闸**（≈0.517×S，故 sub/S ≥ 0.52）；self<0.7、prod<0.7。
- **塔倍率**：analyst/model/other 1.7 > sentiment/fundamental/news 1.6 > pv 1.5 > institutions 1.4 > earnings/risk/shortinterest 1.3 > insiders/macro 1.2 > socialmedia 1.1 > imbalance 1.0。

## 硬约束（用户给定）

1. **禁混**：PV / MODEL / OTHER 三者内部**任意两两不许组腿**（含 PV+PV、PV+MODEL、PV+OTHER、MODEL+OTHER、三塔同现）。
   - 允许：trio 内 × trio 外 category（如 PV+NEWS / OTHER+ANALYST），但这类组合**总量 ≤5**。
   - 不限量：trio 外 × trio 外（如 ANALYST+SENTIMENT）。
   - 单数据集 ATOM 不占配额。
   - 本轮以 **ATOM 为主**，天然规避该约束。
2. **近十年必须有数据**：覆盖率可动态调整，但 2014-01-01 ~ 2023-12-31 必须逐年有 PnL（收批后查 yearly stats 逐年 longCount>0 且 pnl≠0）。
3. **并发**：`create_multi_simulation` 同时在飞 **≤2 批**。
4. **工具**：优先 MCP；prod 相关性必须走 MCP；少写临时脚本。
5. **模板**：每个数据集 ≥10 个结构互异模板（见 `hkg_template_library_20261103.md`），先查论坛 + 文献再派发。

## 已有战况（本会话前）

| 族 | 数据集 | 最优 S | 结论 |
|---|---|---:|---|
| EPS 变化 | analyst39 (`rygnhcspe`) | **1.48** | HKG 历史最强；差 S 0.10 / 2Y 0.25；价差结构全灭（单一信号） |
| EPS 变化 | analyst39 (`epschngin`) | 1.28 | 窗口 66 最优；SECTOR+decay4 最优（STAT 0.61） |
| 筛选×持股 | analyst94 | 1.33 | 两墙：SHARPE + TVR |
| NEWS 词数归一 | news36 | 0.27 | 两极严格对称 ⇒ 真信号但极弱 |
| NEWS MATRIX | news7 | 0.20 | 证伪「MATRIX 优势」假设 |
| NEWS 事件驱动 | news79 | 0.64 | VECTOR 事件驱动 |
| NEWS Ravenpack | news18 | 0.09 | 事件情绪无效 |
| 情绪/趋势 | mmp_nlp_sentiment | 0.49 | 判死 |
| 机构持仓流量 | fund_holdings_panel | 0.56 | 判死 |
| 筛选-持股背离 | model238 | 1.39 天花板 | 该机制封盘 |

⇒ **NEWS category 在 HKG 已判死（天花板 ≤0.64）**，不在本轮预算内。

## 本轮波次计划

| 波 | 数据集 | tower | 模板数 | 状态 |
|---|---|---|---:|---|
| W1 | intraday_pv_feats | PV ×1.5 | 10 | 已派发（2 批 × 5） |
| W2 | risk59 | RISK ×1.3 | 10 | 已预检 valid，待派 |
| W3 | sentiment21 | SENTIMENT ×1.6 | 10 | 已预检 valid，待派 |
| W4 | institutions6 / other532 / other543 | INSTITUTIONS ×1.4 / OTHER ×1.7 | 5+3+3 | 待设计 |
| W5+ | 按 W1-W4 归因决定 | | | |

## W1 实验设计（含对照）

派发批次：`3yJvXgKH5fxbRe92nCInFP`（A1-A5）、`3JES1c2iO4j5bWf8z7gczq9`（A6-A10）。

对照结构（保证可归因）：
- **A1 vs A5**：分组轴 industry vs subindustry（粒度）
- **A1 vs A7 vs A8**：窗口 126 vs 22 vs 252（信号时效）
- **A1 vs A2 vs A3 vs A4**：价格类型 high / high−low / ask−bid / vwap（哪条价格序列携带信号）
- **A1 vs A6**：一阶（水平）vs 二阶（波动）
- **A1 vs A9 vs A10**：纯价格 vs 主动成交溢价 vs 价量耦合

## W1 实测结果（HKG/TOP800/D1/SECTOR/decay4/trunc0.08）

批次 A `3yJvXgKH5fxbRe92nCInFP`：

| tag | alpha | 表达式要点 | S | F | TO | sub | 2Y |
|---|---|---|---:|---:|---:|---:|---:|
| A1 | qMLj7RXP | high_ret 126 / industry | 0.69 | 0.54 | 4.23% | 1.18 | 0.66 |
| A2 | xArjvZnb | (high−low) 126 / industry | 0.74 | 0.58 | 4.15% | 1.16 | 0.82 |
| A3 | 88RlNwLX | (ask−bid) 126 / industry | 0.48 | 0.26 | 6.27% | 0.77 | 0.40 |
| **A4** | **N1N7PZpw** | **vwap_ret 126 / industry** | **1.49** | **1.55** | **5.48%** | **1.35** | **1.53** |
| A5 | akK7apdW | high_ret 126 / subindustry | 0.76 | 0.55 | 4.17% | 1.19 | 1.10 |

### 归因（W1，n=5）

1. **信号住在 VWAP 序列上，不在 high 上** —— 这是 HKG 与 GLB 的结构性差异：
   - GLB 论坛原文：high 优于 last_trade（S 2.34 vs 1.28），因为「只有主动买单才推高上沿」。
   - HKG 实测：**vwap 1.49 ≫ high 0.69 ≈ high−low 0.74 ≫ ask−bid 0.48**。
   - 解释：HKG TOP800 流动性分层厚，30 分钟内 high 是**单笔极值**（噪声大），VWAP 是**成交量加权均价**（用整段成交的均价刻画「这段时间资金愿意付的价格」）。小宇宙里极值噪声 >> 均价信噪。
   - ⇒ **区域迁移不能照抄价格类型**：价格类型（high/last/vwap）必须按区域流动性结构重测。

2. **分组粒度**：industry 0.69 vs subindustry 0.76（high 口径）。subindustry 略优但差异小；且 subindustry 会把每组样本压到几十只，HKG TOP800 下不稳。

3. **F 已过闸**：A4 的 fitness 1.55 远高于 1.0 ⇒ 收益/换手效率不是问题，唯一缺口是 **S 0.09 + 2Y 0.05**。

4. **sub 闸无忧**：A4 的 sub/S = 1.35/1.49 = **0.906**，远高于比值闸门槛 ≈0.52。

5. **换手健康**：5.48%，落在 5–30% 区间内。

⇒ **本轮旗舰近闸候选 = A4 `N1N7PZpw`**，进入定向增益波（W2）。

## W2 增益波设计（A4 定向）

| tag | 杠杆 | 表达式 | 归因假设 |
|---|---|---|---|
| G1 | 窗口 90 | ts_mean(vwap_ret, 90) | 短窗更贴近当期流动性需求 |
| G2 | 窗口 180 | ts_mean(vwap_ret, 180) | 长窗更稳 |
| G3 | 非线性锐化 | signed_power(..., 1.5) | 放大尾部（重仓被追高的名字） |
| G4 | rank 几何 | ts_rank(vwap_ret, 252) | 用分位替代均值，抗极值 |
| G5 | 二阶矩归一 | ts_mean/ts_std_dev | 单位风险的价格压力（信息比率化） |

批次 `2M7fvTawt58tbOjHOxmZZjx`（SECTOR/decay4）。


---

## W2 risk59 复盘 —— 判死（2026-11-03）

批次 `1P3Pg9eSx4Plc5K15rnnvyOV`，10 条结构互异（借券费率 level / 费率×利用率交互 / 空头动量 / 拥挤度 / 补库天数 / 轧空风险 / 费率一阶差分 / offer−bid 利差 / 长窗 zscore / 利用率 level）。

| tag | 结构 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| R1 | −ts_zscore(last_rate,252) | 0.13 | 0.02 | 24.4% | 0.65 |
| R2 | −rank(ts_mean(last_rate×s3util,66)) | 0.48 | 0.28 | 1.8% | 0.84 |
| R3 | −rank(ts_mean(short_momentum,22)) | −0.02 | 0.00 | 9.5% | −0.05 |
| R4 | rank(ts_mean(squeeze_risk,66)) | −0.29 | −0.14 | 2.2% | −0.97 |
| R5 | rank(ts_mean(crowded_score,66)) | −0.22 | −0.09 | 1.7% | −0.56 |
| R6 | rank(ts_mean(daystocover10day,66)) | −0.14 | −0.05 | 1.8% | −0.37 |
| R7 | −rank(ts_mean(s3utilization,66)) | 0.36 | 0.19 | 1.7% | 0.76 |
| R8 | −rank(ts_delta(last_rate,22)) | −0.35 | −0.11 | 24.2% | −0.52 |
| **R9** | **−rank(ts_mean(last_rate,66))** | **0.73** | **0.45** | **1.9%** | **2.04** |
| R10 | rank(ts_mean(offer−bid,66)) | −0.63 | −0.37 | 1.9% | −1.74 |

**归因**：唯一有信号的是 R9「借券费率水平」——S 0.73 / 2Y 2.04，方向为**高费率→跑输**（做空成本高 = 空头拥挤 = 后续反转下行），与论坛帖 43607257389207 的机制一致，但 **S 0.73 距 1.58 差 2 倍以上、F 0.45 也不过**。
**判读**：risk59 的 16 个字段信息密度不足以在 HKG/TOP800 单独撑起 S≥1.58。**判死（ATOM 层面）**，不再投入单数据集波次；未来若要复用，只能作为**门控腿**与其它 category 组合（如 PV+RISK），且受两塔配额 ≤3 约束。

## W3 sentiment21 复盘 —— 判死（2026-11-03）

批次 `3GJdV8crh4RR9aBEoAAH4jY`，10 条结构互异（极性差 ts_zscore252 / TRNA 双通道差 / 4通道差 / 负情绪波动 / 中性占比 / 极值不对称 / 一阶差分22 / 置信宽度 / 情绪离散 dts_sop / 极性差 ts_mean22）。

| tag | 结构 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| S1 | zscore(pos−neg,252) | −0.47 | −0.09 | **158.2%** | −0.34 |
| S2 | 2/4通道差 ts_mean66 | 0.40 | 0.18 | 6.9% | −0.71 |
| S3 | 4通道差 ts_mean22 | −0.30 | −0.11 | 9.8% | −0.03 |
| S4 | −std_dev(neg,126) | 0.15 | 0.04 | 3.5% | −0.10 |
| S5 | −ts_mean(neut,66) | −0.24 | −0.07 | 4.4% | −0.25 |
| S6 | 极值不对称 pos_max−neg_max | −0.26 | −0.08 | 4.8% | −0.97 |
| **S7** | **ts_delta(pos−neg,22)** | **0.39** | **0.10** | **41.5%** | **1.81** |
| S8 | −置信区间宽度 | −0.04 | −0.01 | 5.7% | −0.10 |
| S9 | −ts_mean(dts_sop,66) | −0.14 | −0.04 | 5.8% | −0.20 |
| S10 | 极性差 ts_mean22 | −0.11 | −0.02 | 8.9% | −0.13 |

**归因**：S7「情绪一阶差分」2Y 1.81 但全样本 S 仅 0.39、换手 41.5% —— 典型的**近两年 regime 依赖**，不是稳定 alpha。S1 用 ts_zscore 长窗 + 极性差把换手推到 158%（日频情绪逐日翻转），印证「情绪类必须 hump / 长窗平滑」。
**判读**：sentiment21 与 HKG NEWS 家族天花板一致（|S|≤0.5）。**判死**。

## W4 / W5 设计（2026-11-03 派发）

### W4 = intraday_pv_feats 第 3 颗 PV（批次 `o2v8LfSL4PS8EU4syiFIeV`）

PV 塔已 2/3（`RRE75dKj`、`2rAlGNk6`），缺 1 颗点亮。10 条模板刻意避开 W1/W2 已用骨架：

| tag | 结构轴 | 表达式要点 |
|---|---|---|
| P1 | 时段分解（尾 30m vs 覆盖 60m 的差） | 收盘前**加速**推高 |
| P2 | 开盘段（不 reverse） | 隔夜信息消化后的惯性 |
| P3 | 仅二阶矩 | 收盘前不稳定性本身 |
| P4 | 价量耦合 corr_last_vwap_with_volume | 价升量增=真需求 vs 操纵 |
| P5 | 订单簿厚度差 bid−ask size ratio | 买盘厚度→压力 |
| P6 | avg_vwap_to_last_price_ratio 偏离 | vwap 与最后成交价的背离 |
| P7 | 滑点恶化 slippage_last − first | 日内执行成本漂移 |
| P8 | 二阶 momentum momentum2_vwap | 价格加速度 |
| P9 | 成交节奏 num_intervals_last_half | 尾盘参与度（散户） |
| P10 | 追高溢价 high−vwap（自带分母） | 极值超出加权均价的溢价 |

### W5 = analyst39 攻 ANALYST 塔（批次 `BVMY2aeR57kbnxzHaHkDrr`）

ANALYST 塔倍率 **1.7（HKG 最高）**，且 analyst39 有一批 **alphaCount ≤ 11 的处女字段**（目标价分歧 tp_high/tp_low、毛利率预测 agrosmgn、负债率预测 qtotd2eq 等），拥挤度远低于已饱和的 epschngin（ac 233）/rygnhcspe（ac 349）。

| tag | 结构轴 | 机制 |
|---|---|---|
| A1 | 目标价分歧 (tp_high−tp_low)/tp_mean | Miller 分歧-估值：高分歧→低预期收益 |
| A2 | 目标价修正率 ts_delta(tp_mean/tp_delay, 66) | 覆盖分析师整体上修 |
| A3 | EPS 修正动量 ts_delta(rygnhcspe, 66) | 经典修正效应 |
| A4 | 修正加速度 ts_delta(ts_delta(rygnhcspe,22),22) | 修正的二阶变化 |
| A5 | 覆盖人数变化 ts_delta(numofests, 66) | 关注度增量 |
| A6 | 毛利率预测水平 ts_zscore(agrosmgn,252) | 质量因子 |
| A7 | 负债率预测 ts_zscore(qtotd2eq,252) | 安全边际 |
| A8 | 年/季 BVPS 比 atanbvps/qtanbvps | 期限结构分歧 |
| A9 | 长期增速预测 ts_zscore(ltg_mean,252) | 成长预期（cov 0.34，需验覆盖） |
| A10 | 修正 × 分歧交互 | 上修且低分歧 = 高确信 |

**待验**：A9 的 `ltg_all_delay_1_*` 覆盖率仅 0.3442、A1/A2/A5 的 `tp_all_delay_1_*` 仅 0.5529 —— 派发后须用 get_alpha_yearly_stats 逐年核 longCount>0，不满足「近十年有数据」的候选直接除名。


---

## 新数据集画像（2026-11-03 实拉，HKG/TOP800/D1）

### pv103「Interval and MOO&MOC statistics」— PV，7 字段，cov **1.0**，ac 10–41
字段全为 `session_1430to1430_*`：`initial_trade_price` / `final_trade_price` / `max_trade_price` / `min_trade_price` / `volume_weighted_avg_price` / `total_traded_volume` / `market_value`。
**价值**：cov 1.0（十年满覆盖），ac 最高仅 41 ⇒ 低拥挤。可直接构造日频 OHLC 类几何，弥补 `intraday_pv_feats` 只有「30/60 分钟窗口」没有「全日 OHLC 与收盘竞价」的空缺。

10 个结构互异模板：
| tag | 结构轴 | 表达式 |
|---|---|---|
| Q1 | 日内收益反转 | `-group_zscore(ts_mean(divide(subtract(final,initial),initial),22),industry)` |
| Q2 | 收盘位置 CLV | `-group_rank(ts_mean(divide(subtract(final,min),subtract(max,min)),66),industry)` |
| Q3 | 收盘对 VWAP 偏离 | `-group_zscore(ts_mean(divide(subtract(final,vwap),vwap),22),industry)` |
| Q4 | 振幅（低波溢价） | `-group_rank(ts_mean(divide(subtract(max,min),vwap),66),industry)` |
| Q5 | 量价耦合 | `-group_rank(ts_corr(divide(subtract(final,initial),initial),total_traded_volume,66),industry)` |
| Q6 | 换手率（低换手溢价） | `-group_rank(ts_mean(divide(total_traded_volume,market_value),66),industry)` |
| Q7 | 上影线（冲高回落） | `-group_zscore(ts_mean(divide(subtract(max,final),vwap),22),industry)` |
| Q8 | 下影线（探底回升） | `group_zscore(ts_mean(divide(subtract(final,min),vwap),22),industry)` |
| Q9 | 成交重心偏离中位价 | `-group_zscore(ts_mean(divide(subtract(vwap,multiply(add(max,min),0.5)),vwap),66),industry)` |
| Q10 | 量能异动 | `-group_zscore(ts_zscore(total_traded_volume,252),industry)` |

### pv106「Microstructure Spread Data」— PV，29 字段，cov 0.86–1.0
**处女字段（ac ≤ 6）**：`transaction_cost_percentile_25`(0) / `slippage_commission_2025`(0) / `korean_market_slippage`(0) / `transaction_cost_estimate`(1) / `transaction_cost_median`(1) / `transaction_cost_percentile_10`(1) / `group_sell_slippage`(1) / `pv106_spread`(1) / `price_difference_bid_ask`(2) / `aggregated_slippage_metric`(3) / `average_spread_slippage`(3) / `asian_market_slippage`(3) / `slippage_at_spread_20`(5) / `bid_ask_price_gap`(6)。
**机制**：Amihud(2002) 非流动性溢价 —— 价差宽 = 流动性差 = 要求更高预期收益；交易成本高 = 套利受限 = 错误定价持续。
**注意**：`pv106_wli_*` 四兄弟 ac 96–192 已饱和，优先用处女字段。

### shortinterest5「Daily Price Limit Data」— SHORTINTEREST，3 字段，cov **1.0**，ac 5–11
`max_price_increase_ratio` / `max_price_decrease_ratio` / `price_limit_condition`。
**机制**：HK 的市调机制（VCM）/涨跌停触发是**事件型**信号 —— 触发后短期动量延续还是反转，是可证伪的清晰假设；且**独立塔（shortinterest，倍率 1.3）**，不与 PV 冲突。

### 其它值得排队的低拥挤集
| 数据集 | category | 字段 | cov | ac | 备注 |
|---|---|---|---:|---:|---|
| `other545` | other | 4 | 0.7381 | 24 | Linked Firms Momentum（关联公司动量，网络效应） |
| `other635` | other | 6 | 0.6965 | 13 | Thomson Reuters News Analytics（但 news 家族已判死，谨慎） |
| `model77` | model | 23 | 0.5692 | **1** | Analysts' Factor Model（全平台仅 1 条 alpha） |
| `risk68` | risk | 5 | 0.9869 | 866 | Forecast Data（已拥挤） |
| `continuation_score` | pv | 560 | **1.0** | 227 | 图表延续形态相似度 |
| `pattern_scores` | pv | 504 | **1.0** | 151 | 形态相似度打分 |


---

## W4 intraday_pv_feats 复盘 —— 重大发现：开盘段与收盘段方向相反（2026-11-03）

批次 `o2v8LfSL4PS8EU4syiFIeV`（10 条）。SECTOR/decay4。

| tag | 结构轴 | alpha | S | F | TO | sub | 2Y |
|---|---|---|---:|---:|---:|---:|---:|
| **P2** | **开盘段动量（不 reverse）** | **`kqNjOQEz`** | **2.17** | **2.03** | 5.88% | **1.84** | **1.47** |
| **P10** | **追高溢价 high−vwap（反向跑）** | **`88RlYnoW`** | **−1.80** | **−1.50** | 5.65% | −1.24 | **−1.74** |
| P1 | 时段分解 30m−60m pre_close | `WjO7091o` | 1.26 | 1.00 | 6.38% | 0.79 | 1.33 |
| P8 | 二阶 momentum momentum2_vwap | `vR1j6dqr` | 1.02 | 0.75 | 5.56% | 1.13 | 1.49 |
| P3 | 仅二阶矩（收盘前波动） | `LLM7rkWn` | 0.46 | 0.28 | 3.1% | 0.61 | 1.50 |
| P5 | 订单簿厚度差 | `88RlYnbW` | 0.39 | 0.16 | 5.9% | 0.11 | −0.30 |
| P4 | 价量耦合 corr_last_vwap_with_volume | `RRE7KdMe` | 0.26 | 0.09 | 8.6% | 0.42 | 1.08 |
| P7 | 滑点恶化 | `j2Yjx1E9` | 0.21 | 0.08 | 2.5% | 0.46 | 0.06 |
| P6 | vwap/last_price 偏离 | `Jje71bwE` | −0.01 | 0.00 | **57.7%** | 0.27 | 0.63 |
| P9 | 成交节奏 num_intervals | `1YNwPJ9K` | −0.12 | −0.01 | **73.5%** | 0.09 | −0.33 |

### 归因 1（本轮最重要）：HKG 的日内收益在**开盘段延续、收盘段反转**
- 收盘前 30m vwap 收益 → **反转**（`RRE75dKj` S +1.79 用 reverse）
- 开盘后 30m vwap 收益 → **延续**（`kqNjOQEz` S +2.17 **不用** reverse，全样本唯一只挂 2Y 的候选）

同一字段族、同一窗口、同一分组，**仅时段不同即符号相反**。这不是参数巧合，是两条不同的微观结构：
- **开盘段** = 隔夜信息集中释放、知情交易者主导 ⇒ 价格变动**含信息** ⇒ 延续（momentum）。
- **收盘段** = 指数化资金/被动执行/收盘竞价，与基本面无关（Cushing & Madhavan 2000）⇒ 价格变动是**流动性补偿** ⇒ 反转。

与 Bogousslavsky(2021)「日内各时段收益在横截面有独立定价含义、开盘与收盘方向甚至相反」一致（**未在线核验**，用户 web_search 额度耗尽 402）。

### 归因 2：`88RlYnoW` 是「追高溢价」的正向版本
`reverse(group_zscore(divide(ts_mean(high_ret − vwap_ret, 126), ts_std_dev(high_ret − vwap_ret, 126)), industry))` 得 S −1.80 ⇒ **去掉 reverse** 即 S +1.80 / F +1.50 / 2Y +1.74 / sub +1.24 / TO 5.65% / margin +30.7bp ⇒ **全闸通过**。
逐年（翻转后）：2014 1.71 / 2015 0.95 / 2016 2.86 / 2017 2.81 / 2018 2.03 / 2019 2.59 / 2020 1.63 / 2021 1.13 / 2022 2.16 / 2023 1.30 —— **十年逐年全正、零空窗**。
经济含义：收盘前最高价相对成交量加权均价的溢价（信息比率化后）越高，后续**跑赢** —— 说明 HKG 尾盘的高点突破并非操纵噪声，而是真实买压，且该买压被日频 OHLC 定价不足。

### 归因 3：`kqNjOQEz` 只差 2Y，且十年逐年全正
逐年 S：2014 2.69 / 2015 1.36 / 2016 2.15 / 2017 3.22 / 2018 2.75 / 2019 2.71 / 2020 3.32 / 2021 1.48 / 2022 **1.01** / 2023 2.03；longCount 385–425 **全十年无空窗**。
2Y 卡在 1.47（门槛 1.58）纯粹因为 2022 年偏弱（1.01）。破法 = 窗口谷（252/180）+ 分组轴（subindustry）+ 信息比率化，已进 W7。

### 归因 4：噪声类结构全灭
P6 vwap/last 比值、P9 成交笔数 → 换手 57.7% / 73.5%，是「日频噪声」的指纹：无信息、只有翻转。**日内微观结构里凡是「计数/比值」类原始量都不可用，必须走「收益 / 溢价 / 波动」这三类。**

## W5 analyst39 复盘 —— 未出闸（2026-11-03）

批次 `BVMY2aeR57kbnxzHaHkDrr`（10 条，ANALYST 塔，倍率 1.7）。

| tag | 结构轴 | alpha | S | F | TO | sub | 2Y |
|---|---|---|---:|---:|---:|---:|---:|
| A5 | 覆盖人数变化 numofests | `3qol5MnQ` | 0.77 | 0.53 | 3.9% | **1.08** | 0.85 |
| A9 | 长期增速预测 ltg_mean | `O0A7V15d` | 0.75 | 0.48 | 5.5% | 0.73 | 0.49 |
| A3 | EPS 修正动量 rygnhcspe | `78LjMkXL` | 0.45 | 0.19 | 5.4% | 0.39 | −0.19 |
| A6 | 毛利率预测 | `YP17JjWW` | 0.43 | 0.18 | 6.2% | 0.38 | −0.11 |
| A7 | 负债率预测 | `GrWlxq3G` | 0.38 | 0.14 | 4.8% | 0.53 | 1.14 |
| A2 | 目标价修正率 | `pwdjZqz6` | 0.22 | 0.08 | 14.7% | 0.21 | **1.45** |
| A1 | 目标价分歧 | `Vkx75vlV` | −0.05 | −0.01 | 2.4% | −0.15 | 0.49 |
| A8 | 年/季 BVPS 比 | `A1VlmROe` | −0.29 | −0.16 | 5.3% | −0.35 | 1.25 |
| A4 | 修正加速度 | `d5Wjo27v` | −0.34 | −0.13 | 9.8% | −0.15 | −0.45 |
| A10 | 修正×分歧交互 | `E56lLZg1` | −0.63 | −0.43 | 3.5% | −1.01 | −0.40 |

**归因**：analyst39 的**分析师预期类字段在 HKG 信号力度只有 0.2–0.8**，与 analyst 塔在 HKG 的历史最优（epschngin S 1.28 / rygnhcspe S 1.48）差一个量级。最有信息的是「覆盖人数变化」（关注度增量，sub 1.08）与「目标价修正率」（2Y 1.45）—— 两者都是**变化量**而非**水平量**。
**判读**：analyst39 的处女字段（目标价分歧、毛利率预测、负债率预测）本身**不是**破闸路径；要打 ANALYST 塔必须回到已饱和的 `epschngin` / `rygnhcspe`，用**修正的二阶结构 + 门控**做差异化，而不是换字段。本轮不继续投入 ANALYST。

## 当前 PV 塔候选盘点（3 颗只差 prod）

| # | alpha | 表达式核心 | S | F | 2Y | sub | TO | self | prod |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `RRE75dKj` | reverse(pre_close vwap 收益 / 其 std) | 1.79 | 1.62 | 2.02 | 1.53 | 5.48% | 0.303 | **0.7105 ✗** |
| 2 | `2rAlGNk6` | reverse(last_trade − vwap, 126) | 1.97 | 2.18 | 2.10 | 2.05 | 5.84% | 0.137 | 待测 |
| 3 | P10-flip（W7 验证中） | high−vwap 溢价 / 其 std，正向 | 1.80 | 1.50 | 1.74 | 1.24 | 5.65% | 待测 | 待测 |
| 4 | `kqNjOQEz` | 开盘段 vwap 动量 126 | 2.17 | 2.03 | **1.47 ✗** | 1.84 | 5.88% | 待测 | 待测 |


---

## W6 pv103 复盘 —— 判死（2026-11-03）

批次 `1WUssr9HR4o6ceA5GVMmAla`（10 条，session_1430to1430_* 全日 OHLC 几何，cov 1.0）。
最好结果 `LLM731GL` S 0.41 / F 0.31 / 2Y 0.85；`9qxXkr71` S 0.27。收盘位置 CLV 反向 `zq3kemm8` S −1.33（翻正 1.33 但 F 1.04、2Y 0.88 不过）。
**判读**：cov 1.0 + 低拥挤 ≠ 有信号。`session_*` 是**日频聚合**价格，与 pv1 的 OHLC 高度冗余，平台已有 alpha 把这类几何吃透（pv1 有 38089 条）。**判死**。
**结论（重要）**：HKG PV 塔的有效信息不在「日频 OHLC 聚合」，而在 **`intraday_pv_feats` 的细分时段 × 细分价格类型**——这是该塔唯一的富矿层。

## W7 PV 增益波复盘 —— 6 颗全闸通过（2026-11-03）

批次 `3SYoKlbn74HQbJrAyhSMLK6`（10 条，围绕开盘段/窗口谷/分组轴/信息比率化）。

| tag | alpha | 结构 | S | F | TO | sub | 2Y | RA |
|---|---|---|---:|---:|---:|---:|---:|---|
| **G4** | **`ZYQ716j1`** | **时段分歧：post_open − pre_close 126** | **2.41** | **2.51** | 5.67% | **2.16** | **2.31** | **0 fail** |
| G3 | `qMLjw8nA` | post_open 180 | 2.34 | 2.29 | 5.04% | 1.91 | 1.96 | 0 fail |
| G2 | `YP1796Nq` | post_open 252 | 2.21 | 2.10 | 4.47% | 1.92 | 2.21 | 0 fail |
| G7 | `O0A72OoR` | post_open 信息比率化(mean/std) | 2.01 | 1.87 | 5.53% | 1.87 | 1.68 | 0 fail |
| G5 | `N1N720Ao` | post_open 126 subindustry | 1.87 | 1.55 | 5.98% | 1.46 | 1.62 | 0 fail |
| G1 | `RRE7vM2e` | P10 翻正：high−vwap 溢价 126 | 1.80 | 1.50 | 5.65% | 1.24 | 1.74 | 0 fail |
| G6 | `akK7g6oO` | post_open 60m 126 | 2.03 | 1.87 | 5.89% | 1.81 | 1.54 | 2Y |
| G10 | `N1N720Op` | post_open 时序分位 252 | 0.82 | 0.25 | **67.4%** | 0.58 | −0.51 | 否 |
| G8 | `QPv7oMQM` | post_open 追高溢价 | −0.47 | −0.24 | 5.1% | −0.53 | −1.17 | 否 |

### 归因 1：时段分歧是最强几何（S 2.41，超越所有单段版本）
`post_open 126 动量` 单独 2.17、`pre_close 126 反转` 单独 1.79，**两者相减得 2.41 / F 2.51** —— 因为两段的经济来源不同（信息 vs 流动性），相减等于**同时做多知情交易、做空流动性补偿**，噪声互相抵消、信噪比提升。这是本轮最强的结构发现。

### 归因 2：窗口对 2Y 的作用呈**谷形**，不是单调
post_open 126 → 2Y 1.47 挂；**180 → 1.96 过；252 → 2.21 过**；60m 126 → 1.54 挂。窗口 126 恰好落在 2Y 的谷底（2022 年偏弱）。**长窗平滑可单独修复 2Y，而不牺牲 S**（126→180 S 1.87→2.34 还上升）。

### 归因 3：信息比率化有效但削弱 2Y
`mean/ts_std_dev` 版本 S 2.01 / F 1.87 但 2Y 1.68（比 126 原版 1.47 好、比 180/252 差）。分母是「波动」，在 2022 高波动年被惩罚。

## PV 族互相关矩阵（本地，2026-11-03）

8 颗全闸通过的候选两两相关：最大互不相关篮子 = **`ZYQ716j1` / `RRE7vM2e` / `2rAlGNk6`**（max 0.388）。
- 开盘动量家族内部高度共线：`qMLjw8nA`~`YP1796Nq` **0.923**、`O0A72OoR`~`N1N720Ao` 0.845、`ZYQ716j1`~`qMLjw8nA` 0.789 ⇒ **同族最多取 1 颗**。
- 独立支线：`2rAlGNk6`（last_trade−vwap，与所有开盘族 0.14–0.31）、`RRE7vM2e`（high−vwap，0.055–0.39）。

## prod 相关性实测（2026-11-03，唯一取到的三颗之一）

| alpha | prod | 直方图 [0.7,0.8) | 判定 |
|---|---:|---:|---|
| `RRE75dKj` | 0.7105 | n=1（浅钉） | ✗ |
| `ZYQ716j1` | **0.7712** | **n=4** | ✗ |
| `2rAlGNk6` | 未取到（平台计算反复超时） | — | 未知 |
| `RRE7vM2e` | 未取到 | — | 未知 |

**判读**：开盘动量族（`ZYQ716j1`）prod 0.7712 且钉数 n=4 ⇒ **不是单点碰撞，是机制性拥挤**（开盘 30 分钟动量是平台最常见的日内动量构造）。按纪律，n=4 属于「浅钉但成片」，可用**窗口谷位移**（180/252 版本已在手）或**分组轴**（subindustry）破墙，但需先能测 prod。

## 当前状态

- **PV 塔候选 8 颗全闸通过**，其中 6 颗是 W7 新增。
- **塔位仍 0/3**：需 3 颗 prod<0.7 且用户确认后提交。
- **闸门口径复核无损**：`submit_verdict` 对 `ZYQ716j1`/`2rAlGNk6`/`RRE7vM2e` 三颗均返回 `failed_ra=0, sim_fails=[]`，仅 `UNVERIFIABLE_404`（平台 /submit 恒返 404，非真实拦截）。


---

## 阻塞项：prod 相关性队列卡死（2026-11-03 收官时状态）

**现象**：`check_correlation(correlation_type="production")` 的 MCP 客户端硬上限 120s。首次计算平台需 1–5 分钟 ⇒ 首调必超时（但平台侧继续算）。

**已验证可行的协议**（`ZYQ716j1` 成功）：
1. 触发一次（接受 120s 超时）；
2. **等待 ≥15 分钟**（期间不重复触发）；
3. 单次读取 ⇒ `from_cache: true` 命中，返回 max_correlation + 直方图。

**卡死机制**：账号级只有 **1 个 prod 计算槽**。一旦某颗 alpha（本轮 `2rAlGNk6`）的计算挂住，它会**长期占用该槽**，导致之后任何 alpha 的 prod 查询都只能超时——实测 `2rAlGNk6` / `RRE7vM2e` / `YP1796Nq` 三颗在 1.5 小时内反复超时，`get_alpha_details` / `get_user_alphas` / `batch_get_alpha_metrics` / `wqb-db` 全部正常 ⇒ 是相关性槽问题，不是服务宕机。

**下一步处置建议（需用户批准）**：重启本地 MCP 服务（`tools/start_wq_mcp.py`）以清掉残留 inflight 锁，然后按「一次一颗 + 等 15 分钟」串行补测 `2rAlGNk6` / `RRE7vM2e` / `YP1796Nq` 三颗。

## 战果汇总（截至本轮）

- 累计回测 alpha：**91 条**（W1 15 条 + W2 10 + W3 10 + W4 10 + W5 10 + W6 10 + W7 10 + 早期探针 16）。
- **全 RA 闸通过候选：8 颗，全部在 HKG/D1/PV 塔**（`RRE75dKj` / `2rAlGNk6` / `RRE7vM2e` / `ZYQ716j1` / `qMLjw8nA` / `YP1796Nq` / `O0A72OoR` / `N1N720Ao`）。
- **塔位：0/3**（PV 塔需 3 颗 prod<0.7 并提交；其余 14 个 category 仍 0/3）。
- **已判死 category（本轮实测）**：NEWS（≤0.64）、RISK（risk59 最好 0.73）、SENTIMENT（sentiment21 最好 0.40）、ANALYST 处女字段（最好 0.77）、pv103 日频 OHLC（最好 0.41）。
- **提交动作：0**（需用户逐颗确认；且 `2rAlGNk6` / `RRE7vM2e` / `YP1796Nq` 的 prod 尚未取到，不可提交）。

---

# 第二轮续挖（2026-11-04）

## prod 相关性：槽位恢复，两颗 PV 解除阻塞

按「触发一次 → 等 ≥15min → 单次读取」协议重测，槽位已恢复：

| alpha | prod | 直方图 ≥0.5 | 判定 | 备注 |
|---|---:|---|---|---|
| `2rAlGNk6` | **0.5245** | 0.5–0.6 n=1 | ✅ 通过 | 10 项闸全 pass，failed_ra=0，self 0.137 |
| `RRE7vM2e` | **0.6172** | 0.6–0.7 少量 | ✅ 通过 | 10 项闸全 pass，failed_ra=0，self 0.192 |
| `RRE75dKj` | 0.7105 | 0.7–0.8 n=1 | ❌ | 浅钉，可做窗口位移破墙 |
| `ZYQ716j1` | 0.7712 | 0.7–0.8 n=4 | ❌ | 机制性拥挤 |
| `O0A72OoR` / `N1N720Ao` / `qMLjw8nA` | 未取到 | — | 未知 | 单槽排队，连续超时 |

**结论**：PV 塔已有 **2 颗可提交候选**（`2rAlGNk6` prod 0.5245、`RRE7vM2e` prod 0.6172），两者互相关仅 **0.055**，结构独立。第 3 颗待 prod 排队释放后补测。

**已核实全闸**（`get_alpha_details` + `check_self_correlation`）：
- `2rAlGNk6`：`reverse(group_zscore(ts_mean(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2),126), industry))`，S 1.97 / F 2.18 / 2Y 2.10 / sub 2.05 / TO 5.84% / margin 52.4bp / DD 15.0%
- `RRE7vM2e`：`group_zscore(divide(ts_mean(subtract(mean_high_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2),126), ts_std_dev(同项,126)), industry)`，S 1.80 / F 1.50 / 2Y 1.74 / sub 1.24 / TO 5.65% / margin 30.7bp / DD 6.9%

## W11：ANALYST 定向增益（10 条）→ 未突破，天花板 1.30

围绕 `akKL3p8R` 做窗口/分组/非线性变体，最好成绩反而低于原候选：

| alpha | 结构 | S | F | 2Y | sub | TO | 挂闸 |
|---|---|---:|---:|---:|---:|---:|---|
| `mLog2JWX` | epschngin 信噪比 252 / industry | **1.16** | 0.70 | 2.10 | 1.03 | 3.48% | LOW_SHARPE, LOW_FITNESS |
| `88R3k7xX` | ts_mean 66 / std 252 / sector | 1.13 | 0.72 | 1.79 | 1.26 | 2.59% | 同上 |
| `GrWd0Y50` | 信噪比 std 504 / sector | 1.13 | 0.70 | 1.99 | 1.16 | 2.90% | 同上 |
| `WjOPwnRZ` | 信噪比 std 126 | 0.94 | 0.55 | 1.95 | 0.95 | 4.25% | 同上 |
| `KPJOYqoj` | 信噪比 252 / subindustry | 0.91 | 0.49 | 1.89 | 0.95 | 3.45% | 同上 |

**判读**：`anl39_epschngin` 的信噪比族在 1.13–1.16 见顶，原 `akKL3p8R`（sector + std252）的 1.30 仍是最优。窗口 126/252/504 对 S 影响 ≈0.2，分组轴 industry(1.16) ≈ sector(1.13) > subindustry(0.91)。**该字段已饱和**，距 1.58 差 0.28，纯调参无解，需换机制。

## W12：INSTITUTIONS 定向增益（10 条）→ 天花板 1.14

| alpha | 结构 | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| `j2Y3LpJj` | 买/卖市值比 ts_mean 252 / sector | **1.14** | 0.86 | 1.42 | 1.06 | 1.39% |
| `6XdrxWLE` | 同式 / industry | 1.14 | 0.83 | 1.35 | 1.09 | 1.63% |
| `WjOPkZRk` | 窗 66 | 0.93 | 0.63 | 1.20 | 0.92 | 1.71% |
| `3qo9dKm6` | 信噪比化 | 0.90 | 0.55 | 1.82 | 0.86 | 1.78% |

**判读**：institutions6 仅 11 个买卖聚合字段，机制只有「机构净买入强度」一条；换窗口 66→252 单调改善到 1.14 见顶，换分组不改善。**机制穷尽，park**。换手 1.4% 极低是唯一亮点，但 S 差 0.44。

## W13：MODEL / model37 信用困境（10 条）→ 弱，天花板 0.64

字段结构：`mdl37_pd_pct` 越高=风险越高；`mdl37_*_rank` 越高=越安全（desc 明示 higher=safer）。按文献困境异象（Campbell–Hilscher–Szilagyi 2008，高违约概率→低收益）设 10 个结构互异模板。

| alpha | 模板 | S | 2Y | 挂闸数 |
|---|---|---:|---:|---:|
| `d5WO8XKJ` | PD 一阶差分反向 | **0.64** | 0.35 | 5 |
| `2rAOq0j5` | PD 水平反向 | 0.59 | −0.47 | 3 |
| `LLM9bjMe` | 安全排名二阶矩反向 | 0.48 | −0.11 | 4 |
| `gJeQqAaM` | 研报覆盖门控 PD | 0.32 | −1.21 | 4 |
| `78LZqAY8` | 新闻关注度激增反向 | 0.32 | −0.79 | 3 |
| 其余 5 条 | 语言维度/分歧轴 | −0.46 ~ 0.23 | — | 3–5 |

**判读**：文本挖掘信用风险在 HKG **弱**（最好 0.64，2Y 多数为负）。虽然覆盖率 0.93–0.98 满足「近十年有数据」，但信噪比不足以支撑 1.58。10 个结构里只有「PD 变化」与「PD 水平」两条方向稳定为正，语言维度全部无效。**不投入**。

## W14 / W15：PV 微观结构系统枚举（在飞）

场内结论：HKG 唯一能稳定过 1.58 的是 `intraday_pv_feats` 的日内价格—vwap 结构。该数据集有 579 字段，其中 `mean_*_return_*` 家族 30 个，可系统展开两个正交族：

- **W14 价格类型溢价族**（`2mqbNp1eG4zYcEWzY3LXaa`，10 条）：`(ask|bid|low|high60|last60) − vwap`，每对**正反号各一条**（因 `high` 与 `last_trade` 已知符号相反，先用双符号定位方向）。
- **W15 时段价差族**（`3uWZdV16L56raCLCCyfehJ5`，10 条）：`post_open − pre_close_2`，覆盖 vwap/high/last_trade/low/ask/bid × 30m/60m（去掉与 `ZYQ716j1` 重名的 30m vwap）。

统一骨架沿用 `RRE7vM2e` 已证的 `group_zscore(divide(ts_mean(D,126), ts_std_dev(D,126)), industry)`（6 个算子）。

## 闸门口径补记（重要修正）

`get_alpha_details` 的 `checks.fail` **不是完整闸门列表**——它只列出部分。真正的判定在 **`ra.failed_ra_checks`**：例如 `j2Y3LpJj` 的 `checks.fail=[]` 但 `ra.failed_ra_checks=["LOW_SHARPE","LOW_FITNESS","LOW_2Y_SHARPE"]`。判闸一律以 `ra.failed_ra_checks` / `ra.failed_ra_count` 为准。

## 累计战果（截至 2026-11-04）

- 累计回测 alpha：**151 条**（W1–W15 + 早期探针）。
- **全 RA 闸通过候选：8 颗，全在 HKG/D1/PV**；其中 **2 颗 prod 已确认通过**（`2rAlGNk6` 0.5245、`RRE7vM2e` 0.6172）。
- **塔位：0/3**（未提交任何一颗；提交需用户明确确认）。
- **category 天花板实测表**：PV **>2.4** ｜ ANALYST 1.30 ｜ INSTITUTIONS 1.14 ｜ MODEL 0.64 ｜ RISK 0.73 ｜ SENTIMENT 0.40 ｜ NEWS ≤0.64 ｜ pv103 0.41 ｜ pv106 判死。
- **提交动作：0**（等待用户确认）。

---

## 塔位口径重大修正（2026-11-04）

用 `get_pyramid_alphas(region="HKG")` 实拉：**HKG/D1 全部 15 个 category 均为 0**（含 pv:0、shortinterest:0）。

但 HKG 账号已有 **6 颗 ACTIVE/OS 已提交 alpha**，其中 4 颗金字塔名为 `HKG/D1/PV`（`gJZ6pONl` S 2.87、`E5R1AA39` S 2.68）与 `HKG/D1/SHORTINTEREST + HKG/D1/PV`（`gJQZOXrg` S 1.72、`WjPPjVQd` S 1.68）。

**结论**：塔位计数是**本季口径**，2026-09 的历史提交不计入。所以「0/3」是真 0/3，每个塔需本季新提交 3 颗。

**由此得到一条关键战术**：`PV × 非禁混集合 category` 的组合会让 alpha **同时挂两座塔**（历史两颗就是这么做的）。禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL} 内部两两禁；PV 与 ANALYST / INSTITUTIONS / SHORTINTEREST / RISK / NEWS / SENTIMENT 等组合**合法**，组合类型总量 ≤5。

## W14：PV 价格类型溢价族（10 条，正反号成对）

骨架：`group_zscore(divide(ts_mean(D,126), ts_std_dev(D,126)), industry)`，D = 价格类型收益 − vwap 收益（pre_close_2）。

| alpha | D | 号 | S | 2Y | sub | fails |
|---|---|---|---:|---:|---:|---:|
| `pwdPzXJ6` | low−vwap 30m | + | **1.77** | 1.70 | 1.44 | **0** |
| `vR1kzqxw` | high−vwap 60m | + | **1.69** | 2.29 | 1.49 | **0** |
| `pwdPzXox` | last_trade−vwap 60m | − | 1.75 | 1.42 | 1.57 | 1 |
| `rKR5z361` | bid−vwap 30m | + | 1.41 | 1.46 | 0.91 | 2 |
| `kqNVm7eK` | ask−vwap 30m | + | 1.26 | 1.35 | 0.82 | 3 |
| 镜像 5 条 | 同 D 反号 | − | −1.26 ~ −1.77 | — | — | 5 |

**符号结构结论**：`low−vwap` 与 `high−vwap` **同号为正**（都是「相对 vwap 的偏移越大越好」），而 `last_trade−vwap` **需取负**（收盘价溢价→反转）。ask/bid 方向同为正向但强度弱一半（1.26/1.41 vs 1.77）。正反号成对投放是本次定位符号的高效手段，20 条里 10 条直接作废但省掉了二轮试错。

## W15：PV 时段价差族（10 条）→ 最强一档

骨架同上，D = `post_open − pre_close_2`（同价格类型、同窗口）。

| alpha | 价格类型/窗 | S | F | 2Y | sub | TO | fails |
|---|---|---|---:|---:|---:|---:|---:|
| `QPv3lZ6K` | vwap 60m | **2.42** | 2.49 | 2.30 | 2.25 | 5.28% | **0** |
| `xArYzO5w` | last_trade 30m | **2.40** | 2.55 | 1.97 | 2.34 | 5.25% | **0** |
| `MPY18MVr` | last_trade 60m | **2.34** | 2.50 | 2.30 | 2.28 | 5.15% | **0** |
| `O0ArmQ27` | bid 60m | 1.76 | 1.69 | 1.40 | 1.93 | 4.51% | 1 |
| `WjOPX1Jx` | high 60m | 1.17 | 1.10 | 0.80 | 1.75 | 4.52% | 2 |
| `O0ArmQg7` | ask 30m | 1.17 | 0.97 | 0.53 | 1.32 | 4.21% | 3 |
| `A1V0aj2g` | ask 60m | 1.13 | 0.98 | 0.67 | 1.36 | 4.10% | 3 |
| `d5WO7kvw` | low 60m | 0.90 | 0.78 | 0.34 | 1.52 | 4.55% | 3 |
| `omE6z8Zn` | low 30m | 0.25 | 0.09 | 0.84 | 0.29 | 4.48% | 4 |
| `bl6RPGKp` | high 30m | 0.20 | 0.06 | 0.79 | 0.35 | 4.46% | 4 |

**结论**：时段价差族的**最强载体是 vwap 与 last_trade**（2.34–2.42），high/low 反而弱（0.20–1.17）。与 W14 形成互补：**pre_close 段看 high/low，post_open 段看 vwap/last_trade**。

## 族内互相关（13 颗全闸候选，`compute_mutual_correlation`）

**最大互不相关篮子只有 4 颗**：`MPY18MVr` / `qMLjw8nA` / `2rAlGNk6` / `RRE7vM2e`。

高共线对（>0.8）：`qMLjw8nA~YP1796Nq` 0.923、`RRE75dKj~pwdPzXJ6` 0.9225、`xArYzO5w~MPY18MVr` 0.9208、`QPv3lZ6K~MPY18MVr` 0.8789、`O0A72OoR~N1N720Ao` 0.8447、`RRE7vM2e~RRE75dKj` 0.8335、`ZYQ716j1~O0A72OoR` 0.8181。
新 2.4 档三颗（`QPv3lZ6K`/`xArYzO5w`/`MPY18MVr`）彼此 0.81–0.92 ⇒ **只能取 1 颗**。

**推论**：PV 塔要凑 3 颗自相关<0.7 的提交件，正解是 `2rAlGNk6` + `RRE7vM2e` + `MPY18MVr`（或 `qMLjw8nA` 替换后者）。

## W16：PV 价量/流动性族（10 条）→ 全灭

覆盖 `corr_*_with_volume` / `avg_*_size_to_volume_ratio` / `kurtosis_trade_volume_interval` / `corr_{ask,bid}_price_with_slippage` / `mean_slippage_30m_*` 五类机制。

| alpha | 结构 | S |
|---|---|---:|
| `O0Ar567q` | vwap−成交量耦合 | **0.49** |
| `N1NQ5KQX` | 量-高价耦合时段迁移 | 0.20 |
| `58EQqGkz` | 滑点时序差分 | 0.02 |
| `WjOPWY7x` | TWAP−成交量耦合 | 0.00 |
| `j2Y3dVrk` | 卖价−滑点耦合 | −0.03 |
| `GrWd3QG5` | 买价−滑点耦合 | −0.17 |
| `leA8Rg35` | 滑点水平 | −0.33 |
| `QPv35W7K` | 成交量峰度 | −0.37 |
| `P0oZXPG7` | 订单簿厚度 | −0.50 |
| `YP15Wlvl` | 交易规模 | −0.59 |

**结论（重要的机制边界）**：`intraday_pv_feats` 的信号**只住在价格路径**（`价格类型 vs vwap` 的 30/60m 分段），**不住在**成交量 / 订单簿厚度 / 价量耦合 / 滑点里。同一个数据集内部，机制是分层的——这解释了为什么 gJZ6pONl 那样的历史提交要用 PV 做门控而不是主信号。


