# 新矿脉字段画像 + 模板库（2026-11-07 晚批，P21/P27/P28/P29/P30/P31）

> 动机：KOR 已交付 3/10，风险/分析师/内部人三族出件后，剩余 7 颗必须来自**新数据集**。
> 依据 memory「prod 墙在数据集层」「覆盖率≠信号强度」「S 天花板由几何定、2Y 由字段定」，
> 本批 6 个数据集全部走「**2 字段 × 长窗 ts_av_diff × 组内 rank**」冠军族 + 结构互异模板混编。
> 全部字段名已用 `get_datafields` 实测核对（不信 preflight，它对字段名存在性是假阴性）。

---

## 1. model170 — CapitalCube 估值模型（cov 0.9537，11 VECTOR，aC 1–21）

| 字段 | aC | 含义 | 机制角色 |
|---|---:|---|---|
| `latest_implied_valuation_price` | 15 | 模型隐含估值价 | **估值差主腿** |
| `prior_close_price` | 13 | 前收盘价 | 估值差分母 |
| `implied_price_range_maximum` / `minimum` | 3 / 1 | 隐含价格区间上下界 | 不确定性 / 上行空间 |
| `annual_price_peak` / `trough` | 5 / 1 | 52 周最高 / 最低 | 区间位置 |
| `price_position_within_annual_range` | 4 | 当前价在 52 周区间的位置 | 反转腿 |
| `recent_earnings_momentum_score` | 21 | 盈利动量评分 | 动量腿 |
| `composite_fundamental_score` | 1 | 综合基本面质量 | 质量腿 |
| `recent_dividend_yield_pct` | 4 | 股息率 | 收益腿 |

**核心机制（全新，此前 3 颗交付件未覆盖）**：*估值差* = (隐含估值价 − 收盘价) / 收盘价。
CapitalCube 用基本面模型反推"应有价"，与市价的偏离即错价幅度。文献：Frankel–Lee (1998) 剩余收益估值、
Bartram–Griffin–Lim (2020) 内在价值偏离。**方向先验：正（低估 → 做多）**。
**注意**：全 VECTOR，必须先 `vec_avg` 再进任何算子（memory 铁律）。

## 2. model242 — TM1 战术复合 alpha（cov 1.0，4 MATRIX，aC 0–17）
`mdl242_1mt`(15) 综合 alpha 分 / `mdl242_factor_momentum_component`(17) 动量分 / `mdl242_seasonality_component`(9) 季节性 / `sudden_volume_spike_score`(0) 量能冲击。
机制：厂商已合成的预测分，直接横截面排序 + 长窗偏离。**aC 个位数 ⇒ 极低拥挤，prod 墙应浅**。

## 3. model243 — Combined Alpha Model 百分位（cov 1.0，2 VECTOR，aC 20–22）
`mdl243_sector_rank` / `mdl243_industry_rank`，已是 1–100 百分位。
机制：复合模型排名的**双轴分歧**（sector 轴 vs industry 轴排名差）+ 排名漂移。

## 4. pv103 — 14:30→14:30 盘中时段结构（cov 1.0，7 MATRIX，aC 16–49）
final/initial/max/min_trade_price、volume_weighted_avg_price、total_traded_volume、market_value。
**机制（盘中反转，Heston–Sadka–Wermers 2010 intraday reversal）**：
① 收盘价 vs VWAP 偏离 = 尾盘执行压力；② (max−min)/VWAP = 盘中振幅；③ 收盘在区间中的位置（随机指标）；
④ range/drift = 趋势效率；⑤ volume/ts_mean(volume,66) = 异常量。
全部价格差先除以 VWAP / initial_price 去量纲，避免价格水平偏置。

## 5. pv47 — 特质残差收益（cov 1.0，4 MATRIX，aC 5–53）
`pv47_spret`(53) 特质残差收益 / `idiosyncratic_return_fraction`(14) 残差占总收益比例 / `pv47_d1_spret`(5)。
**机制（特异波动反转，Ang–Hodrick–Xing–Zhang 2006）**：剔除因子暴露后的残差收益反转，
比原始收益反转更干净（不受行业/市场 beta 污染）。

## 6. ai_factor_transfer — 经典技术指标原生实现（cov 1.0，20 MATRIX，aC 1–59）
RBO / CCI（`liquidity_weighted_returns_ma_2`）/ RSI（`cumulative_money_flow_volume_adjusted`）/
Williams %R（`momentum_williams_r_adjusted`）/ 布林带位置（`typical_price_bollinger_band_position`）/
CMF / DPO / ADL / PVO / ABN_VOLM。⚠ `_2` 后缀的 **description 与字段名不符**（字段名是 A，描述写的是 B），
以**字段名**为准，description 视为噪声。

## 7. price_signal_dl — DL 归一化趋势/量能（cov 0.9742，28 MATRIX，aC 0–62）
`normalized_{trend,volume}_indicator_0..6` + raw 版。已归一化 ⇒ 省算子，直接横截面排序。
机制：趋势 × 量能二维状态（趋势 0 与 6 之差 = 短长期限结构）。

## 8. pattern_scores — 图表形态相似度（cov 1.0，504 MATRIX，aC 331）
字段命名规则 `<形态名>_<统计量>_<相似度类型>_lookback<60|120>`，
形态名含方向（up/down、top/bottom）、统计量含 mean/median/max/min/std/q95、类型含
`simscore` / `dynamic` / `min_similarity` / `adaptive_similarity`。
机制：看涨形态相似度 − 看跌形态相似度（同一统计量、同一回看窗对齐）。

---

## 模板库（30 个，结构互异；每条标注来源）

| # | 骨架 | 波次 | 来源 |
|---|---|---|---|
| T1 | `-group_rank(F, sector)` 水平反转 | P21/P27 | 自建（超买超卖， Wilder 1978 RSI） |
| T2 | `group_rank(F, sector)` 水平动量（反向臂对照） | P27 | memory「取负非镜像」必须双测 |
| T3 | `group_rank(ts_av_diff(F,378), sector)` 长窗基线偏离 | P21/P27 | **本战役自建冠军几何**（analyst10 W250→1.76 / W294→1.92） |
| T4 | `group_rank(ts_av_diff(F,336), sector)` 长窗变体 | P21/P27 | 同上 |
| T5 | `group_rank(ts_zscore(F,66), sector)` 66 日标准化 | P27 | 自建 |
| T6 | `-group_rank(ts_std_dev(F,66), sector)` 时序离散度 | P21/P27 | insiders5 冠军件同族 |
| T7 | `group_rank(subtract(F_short,F_long), sector)` 期限结构差 | P27 | Novy-Marx 2012 中期动量 |
| T8 | `group_neutralize(multiply(group_rank(A,sector),group_rank(B,sector)),industry)` 双腿乘积 | P21/P27/P30/P31 | **本战役冠军骨架**（qMLOooX1 1.94） |
| T9 | `group_rank(divide(subtract(A,B),add(abs(C),0.0001)), sector)` 三分量背离 | P21/P30 | 自建 |
| T10 | `group_rank(divide(A,add(abs(B),0.0001)), sector)` 二分量化 | P27 | 自建 |
| T11 | 估值差 `(implied−price)/price` | P30 | Frankel–Lee 1998 剩余收益估值 |
| T12 | `divide(implied, range_max)` 上行空间比 | P30 | 自建（区间上界利用率） |
| T13 | `divide(subtract(implied,ts_mean(implied,378)),ts_mean(implied,378))` 隐含价漂移 | P30 | 分析师修正代理 |
| T14 | 52 周区间位置（正 / 负双臂） | P30 | George–Hwang 2004 52-week high |
| T15 | 隐含区间宽度 / 收盘价 = 不确定性 | P30 | 自建（Diether–Malloy–Scherbina 2002 分歧度） |
| T16 | 收盘 vs VWAP 偏离 | P28 | Heston–Sadka–Wermers 2010 盘中反转 |
| T17 | `(max−min)/VWAP` 盘中振幅 | P28 | 自建 |
| T18 | 收盘在区间中位置（随机指标） | P28 | Lane 1950s %K |
| T19 | `range/drift` 趋势效率 | P28 | Kaufman 效率比 |
| T20 | `volume/ts_mean(volume,66)` 异常量 | P28 | 自建 |
| T21 | `ts_mean(盘中漂移,22)` 累积漂移 | P28 | 自建 |
| T22 | 盘中收益 `ts_std_dev(_,66)` | P28 | 自建 |
| T23 | `ts_decay_linear(F,66)` 线性衰减 | P29 | 自建 |
| T24 | 残差收益 `ts_mean(spret,22/66/250)` 三档 | P29 | Ang-Hodrick-Xing-Zhang 2006 |
| T25 | `ts_av_diff(spret,378)` 残差长窗偏离 | P29 | 本战役冠军几何移植 |
| T26 | 残差收益 / 残差占比 双字段 | P29 | 自建 |
| T27 | 复合 alpha 分水平 + 长窗偏离 | P31 | 厂商合成模型 |
| T28 | sector 轴 vs industry 轴排名差 | P31 | 自建（双轴分歧） |
| T29 | 分类事件评分（earnings / corporate structure） | 未派 | 事件型，CW 风险高 |
| T30 | 看涨形态相似度 − 看跌形态相似度 | 未派 | Lo-Mamaysky-Wang 2000 形态识别 |

**多样性核对**：30 个模板分属 8 个机制族（技术反转 / 长窗基线偏离 / 期限结构 / 双腿乘积 /
估值差 / 盘中结构 / 特质残差 / 形态相似度），差异落在算子几何、信息加工方式与机制来源，
不是「同一骨架换窗口」。✅ 满足 ≥10 且结构互异。
