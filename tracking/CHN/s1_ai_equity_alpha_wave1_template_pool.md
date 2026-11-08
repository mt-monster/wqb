# CHN `ai_equity_alpha`（会计取证 / 应计 / 盈余质量）wave1 模板池 — 2026-11-06

> **场地**：CHN / TOP2000U / D1（唯一合法 universe，无 COUNTRY 档）。档位 SUBINDUSTRY / decay4 / trunc0.08 / VERIFY / nan OFF / pasteurization ON / maxTrade OFF。
> **为什么开**：`model` 塔在 CHN **0/3 未点亮**；本数据集 **582 字段全 VECTOR、coverage 0.979、平台 alphaCount 仅 97**、字段级 aC 多为 0–3 ⇒ 几乎是处女地。

## 一、字段画像（按基础因子归并；命名规律 = `<概念>_<1..5/51>` 为同概念变体）

| 概念族 | 代表字段 | 变体数 | 语义 |
|---|---|---:|---|
| 应计贡献 | `accruals_analysis_factor`, `accruals_contribution_score[_2.._5,_51]` | 7 | 应计项目对财务结果的贡献（Sloan 应计异象原料） |
| 会计取证 | `accounting_forensics_factor[_2,_3,_4,_41,_5,_51]` | 7 | 财报异常/财务困境迹象（Beneish M-score 型） |
| 盈余质量 | `earnings_quality_score[_4,_5]` | 2+ | 盈余质量打分 |
| 其余 ~560 字段 | 同构命名族 | — | 覆盖收入确认、费用资本化、税务、表外等取证维度 |

**★ 关键约束：全 VECTOR ⇒ 每个字段必须用 `vec_avg(...)` 包裹**，否则算子类型不匹配直接毙。
**★ 变体编号（_2.._5/_51）是同概念的平行实现，不是不同信号**：做变体间极差（T6）才有独立信息，做加法只是加噪声。

## 二、文献先验（模板来源）

| # | 来源 | 可迁移结论 |
|---|---|---|
| L1 | Sloan (1996) *Do Stock Prices Fully Reflect Information in Accruals and Cash Flows?* | **高应计 → 未来收益低**（应计异象），做空高应计 |
| L2 | Beneish (1999) M-score | 财务造假概率高的公司后续显著跑输 ⇒ 取证因子取负 |
| L3 | Dechow, Ge, Larson & Sloan (2011) F-score | 财报错报概率可事前打分，且被市场低估 |
| L4 | Piotroski (2000) F-score | 基本面改善（质量提升）本身有动量 ⇒ 质量变化用一阶差分 |
| L5 | Richardson, Sloan, Soliman & Tuna (2005) | 应计可靠性越低（越不可持续），定价错误越大 ⇒ 可靠度交互 |
| L6 | Hirshleifer, Hou, Teoh & Zhang (2004) | 应计异象在投资者成熟度低的市场更强 ⇒ CHN 理论上更显著 |
| L7 | Ball & Shivakumar (2006) | 应计与现金流的时间序列关系含独立信息 ⇒ 二阶/背离矩 |

## 三、12 个结构互异模板（四维坐标）

| # | 模板 | 表达式核心 | 骨架 | 矩 | 分组轴 | 非线性 | 文献 |
|---|---|---|---|---|---|---|---|
| T1 | 应计异象水平 | `group_rank(multiply(vec_avg(accruals_analysis_factor), -1), subindustry)` | 单腿 | 水平 | subindustry | 取负 | L1 |
| T2 | 取证合成 | `group_rank(multiply(add(add(vec_avg(accounting_forensics_factor), vec_avg(accounting_forensics_factor_2)), add(vec_avg(accounting_forensics_factor_3), vec_avg(accounting_forensics_factor_4))), -1), subindustry)` | 多变体合成 | 水平 | subindustry | 取负 | L2 |
| T3 | 盈余质量水平 | `group_rank(vec_avg(earnings_quality_score_4), subindustry)` | 单腿 | 水平 | subindustry | 无 | L3 |
| T4 | 质量年度变化 | `group_rank(ts_delta(vec_avg(earnings_quality_score_4), 252), subindustry)` | 单腿 | **一阶差分** | subindustry | 无 | L4 |
| T5 | 应计 vs 质量背离 | `group_rank(subtract(multiply(vec_avg(accruals_analysis_factor), -1), vec_avg(earnings_quality_score_4)), subindustry)` | 双腿价差 | 水平 | subindustry | 无 | L1+L3 |
| T6 | 变体间分歧 | `group_rank(subtract(max(…6 应收变体…), min(…6 应收变体…)), subindustry)`（嵌套二元 max/min） | 分歧度 | 水平 | subindustry | 极差 | L5 |
| T7 | 低质量区条件化 | `trade_when(ts_rank(vec_avg(earnings_quality_score_4), 252) < 0.2, group_rank(multiply(vec_avg(accruals_analysis_factor), -1), subindustry), 0)` | 门控 | 水平 | subindustry | 极值截断 | L2 |
| T8 | 质量波动惩罚 | `group_rank(multiply(ts_std_dev(vec_avg(earnings_quality_score_4), 252), -1), subindustry)` | 单腿 | **二阶方差** | subindustry | 取负 | L7 |
| T9 | 凸性变换 | `group_rank(signed_power(group_zscore(multiply(vec_avg(accruals_analysis_factor), -1), subindustry), 1.4), subindustry)` | 单腿 | 水平 | subindustry | **signed_power 1.4** | EUR 实证 |
| T10 | 双排序交互 | `group_rank(multiply(rank(multiply(vec_avg(accruals_analysis_factor), -1)), rank(vec_avg(earnings_quality_score_4))), subindustry)` | 双排序乘积 | 水平 | subindustry | 交互项 | L5 |
| T11 | 换分组轴 sector | T1 核心换 `sector` | 同上 T1 | 水平 | **sector** | 取负 | L6 |
| T12 | 取证年度变化 | `group_rank(ts_delta(vec_avg(accounting_forensics_factor), 252), subindustry)` | 单腿 | 一阶差分 | subindustry | 无 | L2+L4 |

## 四、wave1 首批（本次派发）

| tag | 模板 | 表达式 | 算子数 |
|---|---|---|---:|
| W1-E1 | T1 | `group_rank(multiply(vec_avg(accruals_analysis_factor), -1), subindustry)` | 3 |
| W1-E2 | T4 | `group_rank(ts_delta(vec_avg(earnings_quality_score_4), 252), subindustry)` | 3 |

**设计意图**：E1 测应计异象的**水平**（L1/L6，CHN 理论上更强），E2 测盈余质量的**变化**（L4 基本面动量）。矩阶不同、概念族不同、方向处理不同（取负 vs 不改号）⇒ 两者互相关预期低，若双双出货可占两个独立名额。
**方向容错**：`accruals_analysis_factor` 的符号语义未在描述中明示（可能是带符号应计，也可能是质量分）。若 E1 出来 S 强负，说明它是质量分 ⇒ 直接翻正号即得正确方向，一次探针同时定方向与量级。

## 五、执行纪律

- 全 VECTOR ⇒ `vec_avg` 必包；漏包会报类型错并整批 WARNING。
- 单批恰好 2 条、批级设置单一；本区唯一 universe = TOP2000U。
- 平台停摆期间不派发（判据见 `tracking/EUR/WAVE_LEDGER.md` §289.8：拿已出过值的件 `--peek` 对照，空体即停摆）。
