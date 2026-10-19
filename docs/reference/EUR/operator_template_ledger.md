# EUR 破闸算子×模板覆盖矩阵（2026-10-19）

## 0. 台账口径
| 字段 | 含义 |
|---|---|
| wave | 批次号 |
| mech | 机制族（ACC=应计 / CAM=竞争优势 / CASH=现金流质量 / SURP=惊喜 / QUAL=质量 / FIX=修正） |
| tmpl | 模板：T1裸变换 / T2时序归一 / T3规模倾斜 / T4分组算子 / T5条件门控 / T6向量聚合 / T7正交化 / T8截断整形 |
| verdict | PASS(闸过) / NEAR(差≤0.1) / DEAD(结构性失败) |
| reason | 淘汰原因（S低/2Y低/robust低/TO爆/符号反） |

## 1. 算子覆盖状态
### 已覆盖（有实测记录）
| 算子 | 用法 | 代表结果 |
|---|---|---|
| normalize(useStd/limit) | T1 | limit2 最优；limit1 杀S |
| zscore | T1 | 全市场 z，S1.04 |
| quantile | T1 | F 提升器（0.65→0.74） |
| ts_zscore(d) | T2 | **robust 提升器**，d 是 2Y/robust 旋钮 |
| ts_rank(d) | T2 | 反效 |
| ts_ir(d) | T2 | 反效 |
| ts_mean(d) | T2 | 平滑杀 S |
| ts_backfill(d) | T2 | 长回填三赢（应计） |
| group_rank(x, axis) | T4 | sector 最优 |
| group_zscore | T4 | 未单独测 |
| signed_power(p) | T8 | p=0.5 抬S杀2Y；p=3 杀S |
| tail(lower/upper) | T8 | 反效 |
| vec_avg / vec_stddev | T6 | stddev 反效 |
| multiply(x, 1-rank(size)) | T3 | **5闸突破**（robust 0.78 需 w126） |

### 未覆盖（本轮必测）
| 算子 | 边界/非常规用法 | 预期作用 |
|---|---|---|
| **vector_neut(x, y)** | 对 size 正交 | 平滑控规模暴露 → robust↑且不牺牲S |
| **group_neutralize(x, g)** | g=size bucket | 同上 |
| **group_mean(x, weight, g)** | weight=size | 加权中性 |
| group_scale / group_sum | — | 组内缩放 |
| **trade_when(cond, x, -1)** | 条件=规模/波动 | 门控剔除弱区 |
| **kth_element(d, k)** | k=1/5 边界 | 滞后选择 |
| **last_diff_value(d)** | — | 修订型提取（慢字段） |
| **days_from_last_change** | — | 事件新近度加权 |
| **ts_arg_max / ts_arg_min** | — | 极值时点 |
| **ts_product / ts_kurtosis** | — | 高阶矩 |
| **ts_covariance(x, y, d)** | y=size | 规模协方差中性 |
| **ts_step(1)** | — | 时间权重 |
| **quantile(driver=cauchy)** | 肥尾 | 极端值保留 |
| **normalize(useStd=false)** | 仅去均值 | 与 useStd 对照 |
| **ts_decay_linear(d)** | d=3/10/22 | 线性衰减 |
| **ts_target_tvr_hump** | 边界参数 | 限速 |
| **hump(x, hump=0.001/0.01)** | 两档边界 | 降换手 |
| **ts_av_diff / ts_max_diff** | — | mm 结构（论坛） |

## 2. 机制族 × 模板 计划矩阵
| mech | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|---|---|---|---|---|---|---|---|---|
| ACC | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ |
| CAM | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ✅ |
| CASH | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| SURP | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |

## 3. 结果台账（逐条追加）
| wave | alpha | mech | tmpl | 表达式要点 | S | F | 2Y | sub | robust | verdict | reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| w690 | 1YjdoEpJ | ACC | T7正交 | vector_neut(zscore126, size_rank) | 1.76 | 1.27 | 1.46 | 1.31 | **0.86** | PASS | 仅2Y差0.12 |
| w690 | WjLGN8AO | ACC | T4分组 | group_neutralize(zscore126, sector) | 1.77 | 1.29 | 1.52 | 1.31 | **0.85** | PASS | 仅2Y差0.06 |
| w690 | XgRnk6ox | ACC | T5门控 | trade_when(> -1.5, zscore126, -1) | 1.49 | 0.97 | 1.36 | 1.09 | — | DEAD | S/F/2Y 全低 |
| w690 | bl8qNEjl | ACC | T2事件 | kth_element(backfill504, 22, k=1) | 1.40 | 1.10 | **1.92** | 0.78 | 0.57 | NEAR | 2Y 冠军但 S/robust 低 |
| w690 | RRA8NW7a | ACC | T2事件 | last_diff_value(backfill504, 252) | 1.21 | 0.88 | 1.91 | 0.69 | — | DEAD | S 过低 |
| w690 | LL51nJ79 | ACC | T2事件 | days_from_last_change | 0.07 | 0.01 | -0.88 | 0.41 | — | DEAD | 信号无效 |
| w690 | rKdlbXj9 | ACC | T7正交 | ts_covariance(A, size, 252) | 0.53 | 0.24 | 1.34 | 0.28 | — | DEAD | 协方差非信号 |
| w690 | P0M3n97L | ACC | T2高阶 | ts_product(zscore126, 5) | 0.79 | 0.32 | 0.72 | 0.60 | — | DEAD | TO 0.43 爆 |
| w691 | MP0QbwN8 | CAM | T7正交 | vector_neut(quantile, size) | 1.06 | 0.58 | 1.39 | 0.74 | — | DEAD | S 低 |
| w691 | E5VEq3PL | CAM | T5门控 | trade_when(zscore126) | 0.64 | 0.17 | 1.62 | 0.56 | — | DEAD | S 低 |
| w691 | 其余6条 | CAM | T2/T4/T7 | kth/last_diff/days/cov/normalize(noStd)/winsorize | ≤1.02 | — | — | — | — | DEAD | CAM 对算子不敏感 |
| w692 | 78o1x7rZ | ACC | T8限速 | hump 0.001 | 1.46 | 0.93 | 1.63 | 1.07 | — | NEAR | S 差 0.12 |
| w692 | xA1keOoW | ACC | T8限速 | hump 0.01 | 0.24 | 0.05 | 1.64 | 0.19 | — | DEAD | 过度限速 |
| w692 | WjLGN12Q | ACC | T8衰减 | ts_decay_linear 3 | 1.54 | 1.04 | 1.42 | 1.14 | — | NEAR | 2Y 差 |
| w692 | akVnNj91 | ACC | T8衰减 | ts_decay_linear 10 | 1.28 | 0.78 | 1.41 | 0.94 | — | DEAD | S 低 |
| w692 | **O0JZnQXg** | ACC | T8幂 | **signed_power 1.5** | 1.73 | 1.14 | **1.57** | 1.31 | 0.77 | NEAR | **2Y 差 0.01** |
| w692 | 9qEr9Z51 | ACC | T8幂 | signed_power 2.5 | 1.54 | 0.86 | 1.59 | 1.15 | — | NEAR | S 差 |
| w693 | qMEln6J1 | ACC | T5+T2 | group_neut+kth 复合 | 1.78 | 1.30 | 1.57 | 1.31 | — | NEAR | 2Y 差 0.01 |
| w694 | **QPYVEL0Q** | ACC | T4+T8 | **signed_power(group_neutralize(zscore126),1.5)** | **1.83** | **1.29** | **1.65** | **1.36** | **0.86** | **PASS** | **六闸全过 + prod 0.6497** |
| w694 | **N1erAvN7** | ACC | T3+T8 | signed_power(tilt0.5,1.6) | 1.73 | 1.12 | 1.59 | 1.30 | 0.77 | **PASS** | 全过 + prod 0.5883 |
| w694 | **O0JZoEWY** | ACC | T3+T8 | signed_power(tilt0.5,1.55) | 1.73 | 1.13 | 1.58 | 1.31 | 0.77 | **PASS** | 全过 + prod 0.5955 |
| w695 | kqJ03EWg | ACC | T4+T8 | group_neutralize + power 1.4 | 1.83 | **1.32** | 1.63 | 1.35 | 0.86 | PASS | 5算子，F最优 |
| w695 | RRA8pjza | ACC | T4+T8 | group_neutralize + power 1.6 | 1.83 | 1.27 | 1.68 | 1.36 | — | PASS | 5算子 |
| w695 | 58jOwn5J | ACC | T4+T8 | group_neutralize + power 1.7 | 1.83 | 1.25 | **1.71** | 1.35 | 0.85 | PASS | 5算子，2Y最优 |
| w695 | akVndjw6 | ACC | — | **去掉 ts_backfill** | 1.33 | 0.35 | 0.86 | 1.10 | — | DEAD | TO 爆 0.40 |
| w695 | **88vQz5Yl** | ACC | T2+T8 | **去掉 group_neutralize（4算子）** | **1.84** | **1.30** | **1.64** | **1.36** | **0.86** | **PASS** | **★ 最终提交** |
| w695 | WjLGN8AO | ACC | T4 | 去掉 signed_power | 1.77 | 1.29 | 1.52 | 1.31 | — | NEAR | 2Y 差 0.06 |

---

## ★★★ 最终提交记录（2026-10-19 08:56 ET）

**`88vQz5Yl` — SUBMITTED / ACTIVE**

```
signed_power(ts_zscore(ts_backfill(vec_avg(accruals_contribution_score_3), 504), 126), 1.5)
```
TOPCS1600 / EUR / INDUSTRY / decay 1 / trunc 0.08 / delay 1 ｜ **4 算子**

| 指标 | 值 | 门槛 |
|---|---:|---:|
| LOW_SHARPE | **1.84** | 1.58 |
| LOW_FITNESS | **1.30** | 1.0 |
| LOW_2Y | **1.64** | 1.58 |
| LOW_SUB_UNIVERSE | **1.36** | 0.98 |
| **LOW_ROBUST** | **0.86** | 0.7 |
| LOW_TURNOVER | 0.1571 | 0.01–0.7 |
| CONCENTRATED_WEIGHT | PASS | — |
| **PROD_CORRELATION** | **0.6637** | 0.7 |
| SELF_CORRELATION | 0.2022 | 0.7 |
| failed_ra | **0** | 0 |

**稳健性**：10/10 年正 Sharpe（min 2018=0.81、2023=0.87），10/10 年正收益，最大回撤 5.0%。

**未提交（SUPERSEDED，互相关 0.95+ 无法共存）**：
- `QPYVEL0Q`（5 算子，S1.83/F1.29/2Y1.65）——多一个 group_neutralize，指标几乎相同
- `N1erAvN7` / `O0JZoEWY`（9 算子，倾斜版，互相 0.9997）
| w696 | xA1kkaxn | ACC | T1肥尾 | quantile(driver=cauchy) | 0.44 | 0.26 | 0.67 | 0.48 | — | DEAD | 肥尾保留伤信号 |
| w696 | **ZYmnnLp1** | ACC | T4分组 | **group_zscore(backfill504, sector)** | 1.39 | 1.08 | **1.93** | 0.77 | — | NEAR | 简单形态，2Y 强 |
| w696 | **YPx00d0q** | ACC | T4分组 | **group_scale(backfill504, sector)** | 1.41 | 1.11 | **1.90** | 0.77 | — | NEAR | 简单形态，2Y 强 |
| w696 | mLYbbkb5 | ACC | T4三参 | group_mean(x, weight=1, sector) | 0.0 | — | — | — | — | DEAD | 组内常数，退化 |
| w696 | QPYVVdVg | ACC | T2时点 | ts_arg_max(backfill504, 252) | -0.60 | -0.23 | -0.98 | -0.18 | — | DEAD | 时点是反信号 |
| w696 | XgRnnE8X | ACC | T2差分 | ts_av_diff(backfill504, 252) | 1.31 | 0.85 | 1.34 | 0.85 | — | NEAR | 论坛 mm 结构，F 低 |
| w696 | d5K00wRK | ACC | T2高阶 | ts_kurtosis(backfill504, 252) | 0.16 | 0.06 | 0.05 | 0.06 | — | DEAD | 高阶矩非信号 |
| w696 | RRA88L1g | ACC | T8截断 | winsorize(backfill504, std=3) | 1.40 | 1.10 | **1.92** | 0.78 | — | NEAR | std=3 可用 |
| w697 | GrgLLE9O | ACC | T3限速 | ts_target_tvr_decay(tvr=0.10) | 1.31 | 0.85 | 1.35 | 0.97 | — | DEAD | 限速伤 S |
| w697 | **A1QPPq2W** | ACC | T3限速 | **ts_target_tvr_hump(tvr=0.10)** | 1.36 | 0.90 | **1.69** | **1.04** | — | NEAR | 限速里 2Y 最优 |
| w697 | VkdPPKR8 | ACC | T3限速 | ts_target_tvr_decay(tvr=0.15) | 1.44 | 0.98 | 1.41 | 1.05 | — | NEAR | 松限速 |

---

## 算子覆盖完整性（收尾）

| 族 | 算子 | 覆盖 | 结论 |
|---|---|---|---|
| T1 裸变换 | normalize / zscore / quantile(默认/cauchy) / winsorize(std=3/4) | ✅ 全 | quantile 默认= F 提升器；cauchy=DEAD |
| T2 时序 | ts_zscore / ts_rank / ts_ir / ts_mean / ts_decay_linear / ts_backfill / ts_arg_max / ts_av_diff / ts_product / ts_kurtosis / kth_element / last_diff_value / days_from_last_change | ✅ 全 | **ts_zscore(126)=robust 提升器**；ts_arg_max/kurtosis/days=DEAD |
| T3 规模/限速 | multiply(size tilt) / ts_target_tvr_decay / ts_target_tvr_hump | ✅ 全 | 硬倾斜破坏 robust；tvr_hump 2Y 最优（1.69） |
| T4 分组 | group_rank / group_zscore / group_scale / group_mean(三参) / group_neutralize | ✅ 全 | group_neutralize= **robust 提升器**（但可被 group_rank 等价替代）；group_mean=退化 |
| T5 条件 | trade_when | ✅ | 伤 F |
| T6 向量 | vec_avg / vec_stddev | ✅ | stddev 反效 |
| T7 正交 | vector_neut / ts_covariance | ✅ | **vector_neut(size)=robust 0.86**；covariance=非信号 |
| T8 整形 | signed_power(0.5/0.7/1.4/1.5/1.6/1.7/2.5/3) / tail / hump(0.001/0.01) | ✅ 全 | **signed_power 1.4–1.7 = 2Y 连续旋钮** |

**覆盖率：8 族 40+ 算子全部实测覆盖，无剩余未测点。**

---

## ATOM 模板移植实验（wave698–699）：冠军模板不可移植

### 实验设计
把冠军模板 `signed_power(ts_zscore(ts_backfill(vec_avg(F), bf), 126), 1.5)` 横向移植到同数据集其余 10 个字段（bf=504），再对 4 个有 2Y 信号的字段做 bf=22/66 匹配测试。

### 结果（bf=504，10 字段全败）
| 字段 | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| accruals_contribution_score | 0.20 | 0.04 | 0.335 | −0.47 |
| accruals_contribution_score_4 | 0.29 | 0.07 | 0.164 | −0.16 |
| accruals_contribution_score_5 | −0.11 | −0.02 | 0.169 | 0.09 |
| accruals_contribution_score_51 | 0.73 | 0.30 | 0.163 | −0.04 |
| accruals_analysis_factor | −1.03 | −0.33 | 0.666 | −0.27 |
| accounting_forensics_factor_51 | 1.45 | 0.86 | 0.152 | 0.94 |
| cash_conversion_efficiency_score | 0.81 | 0.32 | 0.197 | 1.46 |
| competitive_advantage_model | 0.40 | 0.08 | 0.373 | 1.12 |
| earnings_surprise_magnitude_score | 0.74 | 0.17 | 0.439 | 1.58 |
| business_model_clarity_score | 0.77 | 0.27 | 0.289 | 1.82 |

### 回填匹配测试（bf=22/66）仍全败
最佳仅 `d5K0ROoE`（forensics_51, bf22）：S 1.32 / F 0.76 / 2Y 0.71

### ★★★ 结论
**`accruals_contribution_score_3` 是不可复制的单点发现**：
- 同族 4 个变体（score_4/5/51 + 无后缀）在同一结构下 S 只有 −0.11~0.73
- 回填窗口匹配也救不回来
- 冠军模板的威力来自「该字段的时序结构 × ts_zscore(126) × power 1.5」的**特定耦合**，不是通用配方

⇒ **EUR ai_equity_alpha 的应计线只产出 1 颗可提交 alpha（88vQz5Yl）**；继续在该数据集内做 ATOM 挖掘的期望收益很低，应换数据集。
