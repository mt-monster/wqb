# HKG · news_sentiment_transfer · wave1 模板池（15 模板，四维互异）

> 生成时间 2026-11-06 05:20 · 区域 HKG / TOP800 / D1
> 选集理由：HKG 塔位 pv 1/3，其余 15 个 category 全 0 ⇒ 未点亮塔最多；该数据集 **sentiment** category、**cov 1.000**、字段 aC 1–9（几乎无人开采）。

## 1. 字段画像（23 字段：20 MATRIX + 3 VECTOR）

| 组 | 字段 | 类型 | 覆盖 | aC | 用途 |
|---|---|---|---:|---:|---|
| 关注度 | `news_article_count` | MATRIX | 1.000 | 9 | 注意力轴 / bucket 分组 |
| 关注度 | `normalized_news_article_count` | MATRIX | 1.000 | 6 | 同上（跨股可比） |
| 综合 | `sentiment_score_average` | MATRIX | 1.000 | 5 | 主信号水平 |
| 综合 | `sentiment_score_median` | MATRIX | 1.000 | 4 | 稳健中心 |
| 综合 | `sentiment_score_maximum` / `_minimum` | MATRIX | 1.000 | 4 / 2 | 极值位置 |
| 综合 | `total_sentiment_score` | MATRIX | 1.000 | 2 | 总量（含关注度） |
| 分布 | `sentiment_distribution_skewness_2` | MATRIX | 1.000 | 2 | **三阶偏度** |
| 主通道 | `primary_sentiment_{average,max,middle_value,min,total_2,skewness_2}` | MATRIX | 1.000 | 1–5 | 主情绪六件套 |
| 次通道 | `secondary_sentiment_{average,max,middle_value,min,total_2,skewness_2}` | MATRIX | 1.000 | 1–3 | 次情绪六件套 |
| 原始 | `news_sentiment_score`，`primary_sentiment_value`，`secondary_sentiment_value` | **VECTOR** | 1.000 | 4/1/1 | 必须 `vec_avg()` |

**硬陷阱**：3 个 VECTOR 字段裸用必报 `does not support event inputs`，必须 `vec_avg()` 包装。其余 20 个 MATRIX 可直接用。

## 2. 模板库（四维坐标：骨架 / 矩 / 分组轴 / 非线性）

| # | 名称 | 骨架 | 矩 | 分组轴 | 非线性 | 来源 |
|---|---|---|---|---|---|---|
| T1 | 情绪水平 | 单腿 | 水平（均值） | subindustry | — | 自建体检探针 |
| T2 | 偏度长尾 | 单腿 | 三阶偏度 | subindustry | — | 论坛《sentiment22 负面情绪偏度探析》+ Boyer-Mitton-Vorkink (2010) |
| T3 | 情绪极差（分歧） | 单腿 | 一阶离散度 max−min | subindustry | — | SSRN《News-based Investor Disagreement and Stock Returns》 |
| T4 | 情绪修正 | 单腿 | 一阶差分 Δ22 | subindustry | — | Tetlock (2007) 语调-收益可预测性 |
| T5 | 双通道背离 | 两腿价差 | 水平差 primary−secondary | subindustry | — | 自建（主/次情绪双通道） |
| T6 | 注意力加权情绪 | 两腿相乘 | 水平 × 关注度 | subindustry | 双 rank 压缩 | Barber & Odean 注意力理论 |
| T7 | 尾部驱动缺口 | 两腿差 | 二阶形状 mean−median | subindustry | — | 自建 |
| T8 | 语调波动率 | 单腿 | 二阶方差（时序 std22） | subindustry | — | 自建（tone instability） |
| T9 | 偏度 × 价格确认门控 | 门控（三层） | 三阶 + 价格波动分位 | subindustry | `trade_when` | 论坛帖「结合价格确认：极端负偏度 + 缩量抗跌 ⇒ 反弹」 |
| T10 | 总量/关注度背离 | 两腿比 | 单位关注度情绪 | subindustry | — | 自建（**单位风险：VERIFY 下 add 常数易报错，需同单位相除**） |
| T11 | 高斯重塑 | 单腿 | 水平 | subindustry | `quantile(..., driver="gaussian")` | 论坛模板帖 |
| T12 | 换分组轴 | 单腿 | 水平 | **market / industry / sector** | — | 自建（分组轴消融） |
| T13 | 三通道复合 | 三腿 | 复合（primary + secondary − |gap|） | subindustry | — | 自建 |
| T14 | 时序标准化 + 换手抑制 | 单腿 | 一阶 | subindustry | `ts_zscore` + `hump` | 自建（本区 TO 抑制配方） |
| T15 | 注意力 bucket 分组 | 单腿 | 水平 | `bucket(rank(news_article_count), range="0,1,0.2")` | 组内标准化 | CLAUDE.md「部分字段适合做 bucket 自定义分组」 |

### 四维覆盖核对（防「同构骨架陷阱」）

| 维度 | 覆盖 | 说明 |
|---|---|---|
| 骨架结构 | 5/5 | 单腿(T1-T4,T7,T8,T11,T12,T15) / 两腿价差(T5,T7,T10) / 两腿相乘(T6) / 三腿复合(T13) / 门控(T9) |
| 矩 | 5/5 | 水平(T1,T6,T11,T12,T15) / 一阶差分(T4,T14) / 一阶离散(T3) / 二阶(T7 形状、T8 方差) / 三阶(T2,T9) |
| 分组轴 | 4/4 | subindustry / market / industry / sector + bucket 自定义 |
| 非线性 | 4/4 | 无 / rank 压缩(T6) / quantile gaussian(T11) / trade_when 门控(T9) |

## 3. 经济假设与方向先验

| 假设 | 方向先验 | 依据 |
|---|---|---|
| H1 情绪水平 | 中性（双向测） | 港股机构主导，可能 underreaction（正）也可能 overreaction（负） |
| H2 负偏度长尾 | 极端正偏度 ⇒ 做空（lottery premium）；极端负偏度 ⇒ 做空（利空渐次释放） | Boyer-Mitton-Vorkink；论坛帖 |
| H3 新闻分歧 | 高离散 ⇒ 做空（不确定性折价） | Diether-Malloy-Scherbina 血统 |
| H4 情绪上修 | 正向（慢扩散） | Tetlock 2007 |
| H5 注意力 | 高关注 + 高情绪 ⇒ 短期强、随后反转 | Barber-Odean |

## 4. wave1 已派探针（4 条，2 批）

| 批 | 表达式 | 覆盖矩 | 算子 |
|---|---|---|---|
| `2btY7c64s4SA9rAdS3Jft8x` | `group_rank(sentiment_score_average, subindustry)` | 水平 | 1 |
| `2btY7c64s4SA9rAdS3Jft8x` | `group_rank(sentiment_distribution_skewness_2, subindustry)` | 三阶 | 1 |
| `4fFJ7K3Af5k9acc19RhCdCS8` | `group_rank(subtract(sentiment_score_maximum, sentiment_score_minimum), subindustry)` | 一阶离散 | 2 |
| `4fFJ7K3Af5k9acc19RhCdCS8` | `group_rank(ts_delta(sentiment_score_average, 22), subindustry)` | 一阶差分 | 2 |

**批级设置（与 HKG 实测通过件 `2rAlGNk6` 完全一致）**：HKG / TOP800 / D1 / decay 4 / SECTOR / trunc 0.08 / unit VERIFY / nan **ON** / pasteurization ON / maxTrade OFF。

**读法（已固化的判据）**：第一轮探针 **只读 2Y**，不读 S。2Y < 1.58 ⇒ 该数据集封盘，不做第二代；2Y ≥ 1.58 才进第二代（优化 S 与 F，2Y 当守住约束）。

## 5. 下一步（第二代骨架，待 wave1 结果解锁）

- 若 T1/T2 有信号 ⇒ 走 T9 门控 + T14 时序标准化抑制 TO。
- 若 T3（离散）有信号 ⇒ 走 T5/T6 双通道与注意力加权合成。
- 若四个矩全灭 ⇒ 按「同构骨架陷阱」结论只能证伪单腿 group_rank 几何，改 T6/T9/T13 三条异质骨架复测后才可判数据集。