# CHN `model36`（信用风险评分）wave1 模板池 — 2026-11-06

> **场地**：CHN / TOP2000U / D1（CHN 唯一合法 universe，无 COUNTRY 中性化档）。
> **档位**：SUBINDUSTRY / decay4 / trunc0.08 / unit VERIFY / nan OFF / pasteurization ON / maxTrade OFF。
> **为什么开**：CHN 塔位 **0/3（12 塔全未点亮）** ⇒ 不受「已点亮塔不选」约束；`model36` 平台 **alphaCount 仅 27**、字段级 aC 0–6 ⇒ 几乎无人开采。

## 一、字段画像（21 字段，两套同义分项 + 一套困境分位）

`get_datafields(model36, CHN, TOP2000U, filter_sharpe=false)` 实测：21 / 21 均为 **MATRIX**，coverage 0.9718–0.9819。

| 族 | 字段 | 含义 | 方向 |
|---|---|---|---|
| 分项分（主名） | `credit_risk_{coverage,growth,leverage,liquidity,profitability}_score_main` | 0–100 分位，五因子拆解 | **越高越好** |
| 分项分（star 名） | `star_sr_{coverage,growth,leverage,liquidity,profitability}` | 与上行同义（另一套命名） | **越高越好** |
| 困境分位 | `default_risk_{country,global,industry,region,sector}_percentile_main` | 1 年违约概率的组内分位 | **★ 越高越差（方向相反）** |
| 困境排名 | `star_sr_{country,global,industr,region,sector}_rank` | 同上，命名差异 | **★ 越高越差** |
| 综合评级 | `creditworthiness_letter_rating_numeric_main` | 隐含字母评级的连续数值（非 PD%） | **越高越好** |

**★ 头号陷阱：`default_risk_*` / `star_sr_*_rank` 与 `credit_risk_*` / `star_sr_{coverage,growth,...}` 的方向相反。** 混用在同一个 `add` 里会把信号抵消成噪声——这是本数据集最容易出的低级错误。

## 二、文献与论坛先验（模板来源，不只 SOP）

| # | 来源 | 可迁移的结论 |
|---|---|---|
| L1 | Campbell, Hilscher & Szilagyi (2008) *In Search of Distress Risk* | 高困境公司**未来收益更低**（困境异象）⇒ 信用质量做多、困境做空 |
| L2 | Altman (1968) Z-score / Ohlson (1980) O-score | 偿付能力是多因子**线性合成**：盈利、流动、覆盖、杠杆共同决定 |
| L3 | Avramov, Chordia, Jostova & Philipov (2009) | **评级迁移（rating drift）**本身有动量：评级下调后继续跑输 |
| L4 | Jarrow, Lando & Yu (2012) | 评级迁移的**方向与速度**比水平更有预测力 |
| L5 | Dichev (1998) / Griffin & Lemmon (2002) | 困境异象部分被账面市值比吸收 ⇒ 必须**中性化**后再看边际信息 |
| L6 | Chava & Purnanandam (2010) | 困境风险与**流动性**强交互 ⇒ 因子交互项值得单独测 |
| L7 | 论坛/BRAIN 经验（EUR 实证） | 慢信号用 `SLOW_AND_FAST + decay8` 最优；但 CHN 无该档，本区用 SUBINDUSTRY/decay4 |

## 三、12 个结构互异模板（四维坐标标注）

四维 = **骨架 / 算子几何 / 矩 / 分组轴 / 非线性**。T1 与 T2 只在「符号方向」不同、T4 与 T7 只在「一阶 vs 二阶」，其余各维都拉开。

| # | 模板 | 表达式核心 | 骨架 | 矩 | 分组轴 | 非线性 | 文献 |
|---|---|---|---|---|---|---|---|
| T1 | 复合 Z 型水平 | `group_rank(subtract(add(add(prof,liq),add(cov,gro)),lev), subindustry)` | 多字段加权 | 水平 | subindustry | 无 | L2 |
| T2 | 困境分位取负 | `group_rank(multiply(default_risk_global_percentile_main,-1), subindustry)` | 单腿 | 水平 | subindustry | 符号翻转 | L1 |
| T3 | 评级迁移漂移 | `group_rank(ts_delta(creditworthiness_letter_rating_numeric_main,66), subindustry)` | 单腿 | **一阶差分** | subindustry | 无 | L3/L4 |
| T4 | 分项内部分歧 | `group_rank(subtract(max(…5分项…), min(…5分项…)), subindustry)`（嵌套二元 max/min，4 算子） | 分歧度 | 水平 | subindustry | 极差 | L2 反用 |
| T5 | 本土 vs 全球背离 | `group_rank(subtract(default_risk_country_percentile_main, default_risk_global_percentile_main), subindustry)` | 双腿价差 | 水平 | subindustry | 无 | L1 扩展 |
| T6 | 组内中性化换轴 | `group_rank(group_neutralize(T1core, sector), sector)` | 同上 T1 | 水平 | **sector** | 无 | L5 |
| T7 | 信用质量波动率 | `group_rank(multiply(ts_std_dev(T1core,252),-1), subindustry)` | 单腿 | **二阶方差** | subindustry | 取负 | L6 |
| T8 | 尾部条件化 | `trade_when(ts_rank(default_risk_global_percentile_main,252)>0.9, group_rank(T1core,subindustry), 0)` | 门控 | 水平 | subindustry | 极值截断 | L1 尾部 |
| T9 | 水平-变化正交化 | `ts_regression(ts_delta(T1core,22), T1core, 252, 0, 2)`（残差） | 回归残差 | 一阶+水平 | 无 | 正交化 | L4 |
| T10 | 凸性变换 | `group_rank(signed_power(group_zscore(T1core, subindustry), 1.4), subindustry)` | 同上 T1 | 水平 | subindustry | **signed_power 1.4** | EUR 实证 |
| T11 | 复合×流动性交互 | `group_rank(multiply(rank(T1core), rank(credit_risk_liquidity_score_main)), subindustry)` | 双排序乘积 | 水平 | subindustry | 交互项 | L6 |
| T12 | 行业相对超额 | `group_rank(subtract(T1core, group_mean(T1core, industry)), subindustry)` | 双腿 | 水平 | industry→subindustry 双层 | 无 | L5 |

其中 `T1core` = `subtract(add(add(credit_risk_profitability_score_main, credit_risk_liquidity_score_main), add(credit_risk_coverage_score_main, credit_risk_growth_score_main)), credit_risk_leverage_score_main)`；`prof/liq/cov/gro/lev` 为五个 `credit_risk_*_score_main` 的简写。

## 四、wave1 首批（已校验，等平台恢复后派发）

| tag | 模板 | 表达式 | 算子数 | validate |
|---|---|---|---:|---|
| W1-E1 | T1 | `group_rank(subtract(add(add(credit_risk_profitability_score_main, credit_risk_liquidity_score_main), add(credit_risk_coverage_score_main, credit_risk_growth_score_main)), credit_risk_leverage_score_main), subindustry)` | 5 | valid / unknown=[] |
| W1-E2 | T3 | `group_rank(ts_delta(creditworthiness_letter_rating_numeric_main, 66), subindustry)` | 2 | valid / unknown=[] |

**设计意图**：E1 测「信用质量的水平异象」（L1+L2），E2 测「评级迁移动量」（L3+L4）。两者矩阶不同（水平 vs 一阶差分）、字段族不同（五因子合成 vs 单字段评级），互相关预期低 ⇒ 若双双出货可占两个独立名额。

## 五、执行记录

- 2026-11-06 04:2x：`analyst45`（同区首个探针）首派 2/2 因**单位不兼容**失败（`add(price, 0.0001)`），已定位修法；重派批 `2q7FgJ8Tz4QPbK21dZPgjSi5` **平台侧 20 分钟未建子仿真** ⇒ 判定为平台停摆（与 HKG prod 首算 20 分钟 pending 同源），**按纪律停止继续派发**。
- 因此 `model36` 的 T1/T3 已校验但**尚未派发**；平台恢复后作为 CHN 第二波首发。
- 后续波次顺序建议：T3（已在首批）→ T5（本土/全球背离，最独立）→ T4（分歧度）→ T7（二阶）→ 其余。
## 六、wave1 实测（2026-11-06 04:4x，CHN/TOP2000U/SUBINDUSTRY/decay4）

| tag | 模板 | alpha | S | F | TO | 2Y | sub | fails | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| W1-E1 | T1 复合 Z 型水平 | `MPYgoPVk` | **−0.62** | −0.31 | 3.9% | −0.32 | −0.62 | 5 | **方向为负、量级非零** ⇒ 翻号即 +0.62 |
| W1-E2 | T3 评级迁移 | `j2YVb2Oe` | 0 | — | **0%** | — | — | 7 | **几何作废** |

**两条硬结论**：

1. **★ `creditworthiness_letter_rating_numeric_main` 是静态字段**：`ts_delta(...,66)` 出来 TO = 0、S = 0、7 项失败 ⇒ 该字段在 66 天窗口内几乎不动，**一切基于它的「变化/迁移」几何都不可用**（Avramov 的评级漂移模板在 CHN 这个数据源上无原料）。要测迁移必须换成五个 `credit_risk_*_score_main` 的动态。
2. **信用质量在 CHN 是反向的**：高质量复合（盈利+流动+覆盖+成长−杠杆）得分高 → 未来收益**低**（S −0.62）。这与美股困境异象（高困境→低收益）方向相反，符合 A 股「垃圾股/小盘投机溢价」的直觉。⇒ **后续所有信用类模板的方向预设应为「做多低质量/高违约风险」**，不再是做多高质量。

## 七、wave2（2026-11-06 04:5x 已派发 `1FNrpv1Px5e99gQsaUMtvqq`）

| tag | 模板 | 表达式 | 算子数 | 设计意图 |
|---|---|---|---:|---|
| W2-E1 | T2 纯困境分位 | `group_rank(default_risk_global_percentile_main, subindustry)` | 1 | 用**单字段纯净度**验证「高违约风险→高收益」，排除复合权重干扰 |
| W2-E2 | T5 本土 vs 全球背离 | `group_rank(subtract(default_risk_country_percentile_main, default_risk_global_percentile_main), subindustry)` | 2 | 同一 PD 在**本国同业**与**全球同业**中的分位差 = 评估基准差异，与水平正交 |

**判死纪律**：本面目前只有 **1 个有效骨架**（T1）+ 1 个作废几何；按「同一面 ≥6 个结构互异骨架全灭」才算判死，wave2 之后还有 T4 分歧度 / T7 门控 / T8 二阶矩 / T10 交互待测。

