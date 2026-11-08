# S1 · analyst45 (Analyst Trade Ideas) 第 1 波模板池 · EUR/TOPCS1600/D1

- 建池时间：2026-11-07｜字段画像见 `docs/reference/EUR/analyst45_field_profile_20261107.md`
- 派发档：`EUR / TOPCS1600 / delay 1 / decay 4 / SUBINDUSTRY / truncation 0.08 / unitHandling VERIFY / nanHandling ON / pasteurization ON / maxTrade OFF`（= `tracking/EUR/config/settings.json`）
- 模板数：**15 个**（要求 ≥10）。互异维度落在 **信息加工方式**（水平 / 一阶修订 / 二阶方差 / 三阶偏度 / 计数 / 比率 / 差分流）× **经济机制**（方向估值 / 注意力 / 分歧 / 信念 / 成本 / 生存期）× **归组轴**（industry / subindustry / sector / market）× **非线性**（rank / 阈值 / 符号）上，不是同骨架换窗口。

## 模板清单

| # | 模板名 | 矩 | 机制（经济含义） | 表达式 | 算子数 | 来源 | 状态 |
|---|---|---|---|---|---|---|---|
| T1 | 目标价存量溢价 | 水平比值 | 建仓时作者声明的空间：(target−prc)/prc 的聚合 → 方向信号 | `group_rank(divide(vec_avg(anl45_target_prc), vec_avg(anl45_prc)), industry)` | 4 | paper#1 Birru et al. 2022 | **w1 已派** |
| T2 | 构想覆盖广度 | 计数 | 活跃构想条数 = 卖方注意力；注意力→短期高估→反转（取负） | `-group_rank(ts_mean(vec_count(anl45_target_prc), 22), industry)` | 5 | forum#5 + Barber–Odean | **w1 已派** |
| T3 | 目标价分歧度 | 二阶 | 目标价变异系数 = 意见分歧；卖空约束下高分歧溢价（取负） | `-group_rank(divide(vec_stddev(anl45_target_prc), vec_avg(anl45_target_prc)), industry)` | 4 | paper#3/#4 Miller 1977 | **w2 已派** |
| T4 | 信念加仓比 | 水平比值 | Σ現仓 / Σ初始仓 = 分析师给自己构想的追加投入（信念升级） | `group_rank(divide(vec_sum(anl45_current_inv), vec_sum(anl45_initial_inv)), industry)` | 4 | paper#1 辅助轴 | **w2 已派** |
| T5 | 信念加权剩余空间 | 加权比值 | 用 `probability` 做权重的前瞻空间 = 高信念构想的剩余上行 | `group_rank(divide(vec_sum(multiply(anl45_probability, anl45_target_prc)), vec_sum(multiply(anl45_probability, anl45_latest_prc))), industry)` | 5 | paper#1 + 信念轴 | 待派（验证向量逐元素语义） |
| T6 | 构想新鲜度 | 计数/年龄 | 最年轻构想距今天数 = 新信息到达速度（取负：越新越强） | `-group_rank(ts_mean(vec_min(anl45_days_since_inception), 22), industry)` | 5 | paper#2 催化剂线 | 待派 |
| T7 | 修订对 | 一阶 | `new_value`/`old_value` = 止损/目标价/配置的最近一次修订幅度 | `group_rank(divide(vec_avg(anl45_new_value), vec_avg(anl45_old_value)), industry)` | 4 | forum#6 修订层 | 待派（度量纲混杂风险） |
| T8 | 风险调整质量 | 水平单场 | 构想自身的 Jensen α = 分析师选股技能 | `group_rank(vec_avg(anl45_jensensalpha), industry)` | 3 | paper#7 技能可外推 | 待派（最省算子档） |
| T9 | 时间跨度偏好 | 水平单场 | 构想声明的时间跨度；长跨度=耐心资本/事件驱动（取负） | `-group_rank(vec_avg(anl45_time), industry)` | 3 | paper#2 | 待派 |
| T10 | 实施成本折价 | 比值差分 | 含佣买价相对裸买价的溢价 = 交易摩擦；高摩擦股要求流动性溢价（取负） | `-group_rank(divide(subtract(vec_avg(anl45_avg_initial_prc_wfee), vec_avg(anl45_avg_initial_prc)), vec_avg(anl45_avg_initial_prc)), industry)` | 7 | 自建（G 轴唯一可读成本） | 待派 |
| T11 | 未平仓占比 | 组合占比 | 未实现价值 / (未实现+已实现) = 尚未兑现的信念份额 | `group_rank(divide(vec_sum(anl45_unreal_value), add(vec_sum(anl45_unreal_value), vec_sum(anl45_real_value))), industry)` | 7 | 自建 | 待派 |
| T12 | 分布宽度 | 二阶（极差） | (max−min)/均值 = 目标价分布宽度，与 T3 同族但用极差矩 | `-group_rank(divide(vec_range(anl45_target_prc), vec_avg(anl45_target_prc)), industry)` | 4 | forum#4 | 待派（T3 的边缘档，同族只 1 席） |
| T13 | 目标价偏度 | 三阶 | 少数极乐观构想拉出的右尾 = 乐观偏见 | `-group_rank(reduce_skewness(anl45_target_prc), industry)` | 3 | forum《Estimate Skew》 | 待派 |
| T14 | 累计构想收益 | 水平单场 | 构想自成立以来的总收益率 = 分析师业绩持续性 | `group_rank(vec_avg(anl45_tot_ret_per), industry)` | 3 | paper#7 | 待派 |
| T15 | 未实现日内改善 | 一阶差分流 | 未实现回报的当日增量（5 日平滑）= 构想正在被市场验证的流速 | `group_rank(ts_mean(vec_avg(anl45_unreal_ret_today), 5), industry)` | 4 | 自建 | 待派 |

## 派发与读数记录

### 第 1 波（T1 / T2）
- multisimulation：`2oE1TE2gv5658L4Fod9jeqz`
- 字段校验：`validate_expressions` → `valid=true / unknown_fields=[] / unknown_soft=[]`

### 第 2 波（T3 / T4）
- multisimulation：`2tzfux92q4Zvcp1qVc0Cprk`
- 未单独跑 validate（4 个字段均已在第 1 波 `fields_checked` 白名单内或同族），风险已记录。

## 待验证的算子假设（会影响后续模板取舍）

1. **两个 VECTOR 字段的逐元素算术**（T5 依赖）：`multiply(probability, target_prc)` 是否按元素对齐。若平台退化为「按最长向量广播」或其它语义，T5 必须改写成「先各自降维再相除」。
2. **`vec_sum` 的量纲可比性**（T4 依赖）：投资金额是组合币种下的绝对量，跨股横截面 rank 只能吸收部分规模效应；若 S 弱但 2Y 强，优先怀疑规模污染而非机制不成立。
3. **`reduce_skewness` 在短向量上的稳定性**（T13）：构想条数少（vec_count 小）的股票三阶矩噪声大，可能需要 `trade_when(vec_count(x) > k, ...)` 门控。

