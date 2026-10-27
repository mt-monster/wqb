# USA / ai_equity_alpha（AI Equity Alpha，MODEL 塔）字段画像与挖掘记录

> 快照：2026-10-23（`datasets` id=294 + `fields` 1108 行，本地库实测；平台 `get_alpha_details` 复核）
> 状态：**停止作主数据集（2026-10-23 用户规则）**。本数据集属 **MODEL 塔且该塔已点亮**（4 条 ACTIVE），
> 按 `locked.lit_tower_platform_category`（用户 2026-09-19 定案）**不得再作主数据集开波**；
> 波 99–103 产出的 `YPx89bQJ` / `58jr102k` / `zqrgna91` / `j2eoKKEj` / `N1eLE1de` **不计入交付口径**，
> 仅保留为组腿辅助池。见交付报告 `output_report/USA_regular_alpha_delivery_20261021.md` §8。
> **波 99–103 的全部结论仍有效**（字段画像、单位不相容族、2023 弱年归因），只是不再据此扩波。
> 数据集类别：**MODEL**（不是 fundamental）。该数据集当初被纳入是因为「Fundamental 全景扫描」需要一个
> 已点亮塔对照 —— 对照可以，**充当主数据集不行**。

## 1. 身份与拥挤度

| 项 | 值 | 读法 |
|---|---|---|
| 数据集 | `ai_equity_alpha`（id=294） | 平台描述为 AI 衍生基本面指标集 |
| 类别 / 塔 | **MODEL**，`USA/D1/MODEL`，**multiplier 1.3** | 与 fundamental 塔正交；MAX 乘数档 |
| data_type（数据集级） | MATRIX | **但 1108 个字段里 815 个是 VECTOR**（见 §3） |
| 数据集覆盖 | 0.9049 | 高覆盖区，不属于稀疏数据集 |
| 字段数 | 1108 | |
| alphaCount（数据集） | **696** | 与字段级合计 1139 的差额 = 跨字段组合计数 |
| 字段级 aC 合计 | **1139**（VECTOR 1057 + MATRIX 82） | |
| 字段级 aC=0 | **776 / 1108（70%）** | 绝大多数变体无人碰过 |
| tier / value_score | STANDARD / 3 | |

**覆盖分布（只有 4 个离散值，字段级无连续覆盖谱）**：

| coverage | 字段数 | aC 合计 |
|---|---:|---:|
| 0.8801 | 293 | 25 |
| 0.9018 | 289 | **622** |
| 0.9113 | 293 | 82 |
| 0.9320 | 233 | **410** |

⇒ 没有低覆盖字段。CW（CONCENTRATED_WEIGHT）与 SUB 的失败都不会来自「早期年份缺值」，
而是来自信号本身在小市值端无区分度。实测 4 条 ACTIVE 全部 `CONCENTRATED_WEIGHT` PASS 可佐证。

**热区字段（aC 前 8）**：`alpha_score`(55) / `debt_to_equity_ratio_metric_41`(32) /
`accounting_forensics_factor`(29) / `historic_earnings_surprise_score`(28) /
`analyst_earnings_revision_score_6`(24) / `accruals_analysis_factor`(23) /
`intrinsic_valuation_estimate_3`(22) / `asset_replacement_cost_factor`(21)。

## 2. 字段模式

### 2.1 家族结构

按「去尾数字后缀」折叠：**333 个家族**，其中 **168 个多变量家族**、165 个单字段家族。

- **52 个多变量家族 aC 合计 = 0**（整族无人开采）——这是本数据集最大的白空间。
- 多变量家族规模：`debt_to_equity_ratio_metric` 49 个变体、`cashflow_trend_analysis` 22 个、
  `analyst_sentiment_score` 17 个、`buzz_intensity_score` 16 个。
- 语义分组（按名字）：
  | 组 | 代表家族 | 语义 |
  |---|---|---|
  | 分析师 | `analyst_sentiment_score` / `analyst_earnings_revision_score` / `analyst_opinion_metric` / `analyst_recommendation_consensus` / `analyst_forecast_change_*` | 共识、修正、分歧 |
  | 会计质量 | `accruals_analysis_factor` / `accounting_forensics_factor` / `earnings_quality_score` / `accruals_contribution_score` | 应计、盈余质量、舞弊 |
  | 杠杆/偿债 | `debt_to_*_ratio_metric`（6 族）/ `debt_coverage_ratio_metric` / `credit_default_risk_assessment` | 杠杆与违约 |
  | 估值 | `intrinsic_valuation_estimate` / `price_to_cashflow_ratio_metric` / `asset_replacement_cost_factor` / `replacement_asset_value_model` | 内在价值 vs 替代成本 |
  | 文本/叙事 | `buzz_intensity_score` / `business_model_clarity_score` / `recent_business_uncertainty` | 叙事强度与不确定性 |
  | 预测合成 | `alpha_score` / `alpha_excess_return_forecast` / `predicted_earnings_surprise` / `pure_alpha_generation_metric` | 模型直接输出 |
  | 技术合成 | `technical_indicator_composite` / `combined_technical_indicators` | 技术指标聚合（PV 味道，注意与 PV 塔相关性） |

### 2.2 字段命名里的「变体」不是同一口径

同一家族的数字后缀（`_2`、`_3`…）差的是**模型/方法/口径**，不是窗口。
实测 `predicted_earnings_surprise_2 − _3` 与 `_3 − _2` 是 **S 2.08 vs 1.59** 的强非对称；
`shareholder_yield_metric_2 − _3` 是 **1.65 vs 1.98**（反向更强）。
⇒ **同一腿必须双方向都测**，方向不可由名字推断（与 other416 的 `metric1_0 > metric1_1` 同源经验）。

## 3. 类型与预处理硬约束（★ 本数据集最大的坑）

| 项 | 值 |
|---|---|
| VECTOR 字段 | **815**（aC 1057，平均覆盖 0.9026） |
| MATRIX 字段 | **293**（aC 82，平均覆盖 0.9113） |
| **同族混类型家族** | **24 个** |

24 个混类型家族（同前缀内既有 VECTOR 又有 MATRIX，**后缀序号不保证类型一致**）：

```
analyst_earnings_revision_score, analyst_forecast_change_metric, analyst_opinion_metric,
analyst_recommendation_consensus, analyst_sentiment_score, asset_impairment_risk_score,
asset_turnover_ratio_metric, cashflow_to_debt_ratio_metric, cashflow_variation_score,
competitive_advantage_model, credit_default_risk_assessment, debt_coverage_ratio_metric,
debt_maturity_profile_score, debt_to_assets_ratio_metric, debt_to_capital_ratio_metric,
debt_to_enterprise_value_ratio_metric, debt_to_equity_ratio_metric, debt_to_market_cap_ratio_metric,
operating_income_score, operating_margin_score, operational_efficiency_metric,
shareholder_equity_growth_rate, shareholder_equity_to_assets_ratio_metric,
shareholder_return_compounding_factor
```

**已实测事故（波 99，2026-10-23）**：
`credit_default_risk_assessment_2` 是 **MATRIX**、`_3`/`_4` 是 VECTOR，臂里写成
`vec_avg(credit_default_risk_assessment_2)` ⇒ 整条 multisim `26vHPD6Yx4TmbDqzBoiDhY8`
**10 个 child 全部 FAIL、父级 status=ERROR 且 message 为空**。
同一设置下单独 POST 对照表达式返回 **201**，证明不是设置/语法问题，是**类型连坐**。

⇒ 发批前纪律（已落为本数据集的操作前提）：
1. 每条表达式涉及的**每个字段**都要单独查 `fields.field_type`（本文件 §2 的家族表不够，必须到字段级）；
2. VECTOR → 必须 `vec_avg/vec_sum/...`；MATRIX → **不得**出现任何 `vec_*`；
3. 一条坏臂 = 整批 10 条报废，没有「部分成功」可回收。

其余约束：
- `ts_backfill(..., 252)` 是本数据集的**主补值窗口**（4 条 ACTIVE 与波 99b 全用它）。覆盖 0.88–0.93 属于
  「有零星空值」，不是 other416 那种段级缺口，252 足够且不引入过度滞后。
- 单位：`unitHandling=VERIFY` 下 `cashflow_trend_analysis_2 − _3` 触发
  `UNITS` 警告（`expected Unit[] found Unit[CSPrice:1]`）——不影响回测，但说明该族两腿单位不一致，
  比值/差值前应先确认量纲。其余已测族无此警告。

## 4. 机制映射（学术锚 → 字段 → 构造）

| 机制 | 学术锚 | 字段 | 构造逻辑 |
|---|---|---|---|
| **M1 同概念模型分歧** | 无单一论文；机制 =「两个模型对同一基本面的估计差 = 模型不确定性 / 信息不对称」 | 同族相邻变体（`_2 − _3`） | 本数据集已验证的主机制；4 条 ACTIVE 全是这个形态 |
| **M2 分析师修正** | Chan–Jegadeesh–Lakonishok 1996；Gleason–Lee 2003 | `analyst_earnings_revision_score_*` / `analyst_forecast_change_*` | 修正方向 → 漂移 |
| **M3 应计/盈余质量** | Sloan 1996；Dechow et al. 2011 | `accruals_analysis_factor_*` / `earnings_quality_score_*` | 高应计 ⇒ 后续跑输 |
| **M4 杠杆/违约** | Altman Z；Campbell–Hilscher–Szilagyi 2008 | `credit_default_risk_assessment_*` / `debt_to_equity_ratio_metric_*` | 违约概率上升 ⇒ 跑输 |
| **M5 内在价值偏离** | Frankel–Lee 1998（V/P） | `intrinsic_valuation_estimate_*` / `asset_replacement_cost_factor` vs 价格 | 折价 ⇒ 跑赢 |
| **M6 叙事强度** | Tetlock 2007；Loughran–McDonald | `buzz_intensity_score_*` / `recent_business_uncertainty_*` | 高 buzz ⇒ 短期过热 |
| **M7 模型合成输出** | 黑盒 | `alpha_score` / `alpha_excess_return_forecast` | 直接当信号（但 aC 55/19，最拥挤） |

## 5. 已验证壳（4 条 ACTIVE，本数据集的历史战绩）

壳形态（`vec_avg` 差值 → 252 补值 → 252 时序 zscore → 行业内 rank → 线性衰减）：

```
ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(A), vec_avg(B)), 252), 252), industry), D)
```

设置：USA / **TOP2000** / D1 / **STATISTICAL** 中性化 / 平台 decay 0 / truncation 0.08 /
nanHandling ON / unitHandling VERIFY / 2014-01-01–2023-12-31。

| alpha | S | prod | self | 备注 |
|---|---:|---:|---:|---|
| `1YZQJKwR` | 2.48 | 0.5751 | 0.2854 | |
| `O08EjLVp` | 2.45 | 0.5626 | 0.3321 | SUB 1.47；表达式 = `forecast_yield_metric_2 − _3`，D=20 |
| `d51A3nqY` | 2.45 | 0.4910 | 0.3257 | |
| `Wje6pdqN` | 1.89 | 0.6091 | 0.2700 | |

⇒ 三条 prod 落在 0.49–0.61，离 0.70 墙有 0.09–0.21 余量；self 0.27–0.33，同族第二颗仍安全。
这是本战役里**唯一**已证明「同壳多腿可批量过 prod」的数据集。

## 6. 波 99 / 99b：新族横切（10 臂）

设置同 §5（TOP2000 / STATISTICAL / decay 0 / trunc 0.08），10 臂全部为「同族 `_2 − _3`」变体，
核心差异只在 **字段族 + 方向**。波 99 因类型连坐全灭；**波 99b（multisim `2ecqJD8rL4ieaiB7iJZeUpF`）** 有效：

| # | 字段对（方向） | alpha | S | F | 2Y | SUB | TO% | RET% | RA fails |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `forecast_yield_metric_2 − _3`（**对照**，D=20） | `O08EjLVp` | **2.45** | 1.55 | 2.55 | 1.47 | 15.11 | 4.6 | 0（ACTIVE，复现） |
| 2 | `shareholder_yield_metric_2 − _3` | `P0gd50Ow` | 1.65 | 0.82 | 0.99 | 0.78 | 7.10 | 3.07 | 3 |
| 3 | `shareholder_yield_metric_3 − _2` | `xA1VE9nl` | **1.98** | 1.08 | 1.32 | 0.78 | 7.06 | 3.69 | 2 |
| 4 | `predicted_earnings_surprise_2 − _3` | `QPYOoqQg` | **2.08** | **1.16** | **1.81** | **1.07** | 14.43 | 4.46 | **1** |
| 5 | `predicted_earnings_surprise_3 − _2` | `KPmv2qL1` | 1.59 | 0.76 | 0.88 | — | 14.58 | — | 3 |
| 6 | `cashflow_trend_analysis_2 − _3` | `58jr23wn` | 1.02 | 0.47 | 0.92 | 0.34 | 9.41 | 2.60 | 4 |
| 7 | `cashflow_trend_analysis_3 − _2` | `leMENkVx` | （同上量级，WARNING） | | | | | | |
| 8 | `information_opacity_score_2 − _3` | `j28baYjO` | 0.27 | 0.06 | 0.17 | — | 15.83 | — | 4 |
| 9 | `credit_default_risk_assessment_3 − _4` | `npPMmWj8` | 0.54 | 0.18 | 0.01 | — | 8.46 | — | 4 |
| 10 | `pure_alpha_generation_metric_2 − _3` | `qM0o5reV` | 0.72 | 0.18 | −0.16 | — | 27.66 | — | 4 |

（`leMENkVx` 与 `58jr23wn` 同族反向，WARNING 来自 UNITS，指标同量级弱；未入 backtest_results。）

### 6.1 归因（逐条，先结论后证据）

1. **对照复现，壳可信**。#1 精确复现既有 ACTIVE `O08EjLVp`（S 2.45 / F 1.55 / SUB 1.47）⇒
   波 99b 的设置与表达式解释与大历史一致，后续差异可归因到字段，不是设置漂移。
2. **同族反差的非对称是真实且方向特异的**：
   - `shareholder_yield`：`_2−_3` 1.65 → `_3−_2` **1.98**（反向更强）；
   - `predicted_earnings_surprise`：`_2−_3` **2.08** → `_3−_2` 1.59（正向更强）。
   ⇒ 「同族变体 = 两个模型的估计」这个机制成立，但**哪个模型更接近市场共识是族特异的**，
   不可用一条规则外推。
3. **唯一近成品是 #4 `QPYOoqQg`**：S 2.08 / F 1.16 / 2Y 1.81 全过，只卡
   `LOW_SUB_UNIVERSE_SHARPE` **1.07 vs limit 1.10（Δ0.03）**。
   SUB 比值闸口径：limit ≈ **0.53 × S**（本批实测 1.10/2.08=0.529、1.05/1.98=0.530、0.88/1.65=0.533）
   ⇒ 通过条件是 **子宇宙 Sharpe ≥ 53% 的全宇宙 Sharpe**，不是固定数。
4. **三个族直接判弱**：`information_opacity` 0.27、`credit_default` 0.54、`pure_alpha_generation` 0.72。
   这三族即便换轴也补不回 1.58，**不再给它们出波次**。
5. **`cashflow_trend` 的 UNITS 警告不影响结论**：两向都 ≤1.02，且单位不一致本身说明该族两腿不可直接相减，
   构造前提不成立。
6. **换手分布**：7%–28%。低换手臂（shareholder 7%）在 S 达标时 F 也能过（1.08），
   说明本数据集不是 other416 那种「低换手 ⇒ F 天花板」的结构——原因是 S 可以站上 2.0。

## 7. 波 99c（预登记，8 臂，SUB 单闸修复）

**目标**：把 `QPYOoqQg`（`predicted_earnings_surprise_2 − _3`）的 SUB 从 1.07 推过 1.10，同时
S ≥ 1.58、F ≥ 1.0、2Y ≥ 1.58 不回退。**底座不动**（TOP2000 / STATISTICAL / decay 0 / trunc 0.08）。

| # | 假设 | 表达式核（内核 = `ts_backfill(subtract(vec_avg(predicted_earnings_surprise_2), vec_avg(predicted_earnings_surprise_3)), 252)`，记作 X） |
|---|---|---|
| 1 | 对照（必须逐位复现 `QPYOoqQg`） | `ts_decay_linear(group_rank(ts_zscore(X,252), industry), 5)` |
| 2 | 换秩算子：`group_zscore` 保尾部信息 | `ts_decay_linear(group_zscore(ts_zscore(X,252), industry), 5)` |
| 3 | 轴族上移：`subindustry` | `ts_decay_linear(group_rank(ts_zscore(X,252), subindustry), 5)` |
| 4 | 轴族上移：`sector` | `... , sector), 5)` |
| 5 | 全市场轴（教科书级 SUB 杠杆） | `... , market), 5)` |
| 6 | 更长衰减（降换手顺带抬 SUB） | `... , industry), 10)` |
| 7 | 尾部压缩（多空对称性先看再定） | `signed_power(ts_decay_linear(group_rank(ts_zscore(X,252), industry), 5), 0.8)` |
| 8 | 内核平滑替代 zscore | `ts_decay_linear(group_rank(ts_mean(ts_backfill(subtract(...), 252), 22), industry), 5)`（X 内的 zscore → 22 日均值） |

**判据（先写死）**：
- 任一臂 **`failed_ra_count == 0`** ⇒ 立即转 §8 稳健性链（`brain-alpha-robustness` → `submit_verdict` →
  `check_correlation(refresh=True)`），并且**只取这一颗**做提交候选；
- 全部仍卡 SUB 且 Δ ≤ 0.03 ⇒ 记为「SUB 分辨率极限」，改用**宇宙下移**（TOP1000）或**门控**两条未测轴，
  不再刷轴族参数；
- 任一臂 S < 1.58 或 2Y < 1.58 ⇒ 该臂作废（不允许用掉主闸换 SUB）。

**SUB 为何不靠「把 S 压低」来凑**：闸值是 0.53×S 的相对线，压 S 同时压线，净效果≈0；
必须让**小市值端相对变强**（轴族/门控）或换宇宙。

## 8. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-ai_equity-alpha-field-profile-20261023.md`
- 波 99（类型连坐报废）：`tracking/USA/runs/usa_aieq_w99.txt` + `_spec.json`（multisim `26vHPD6Yx4TmbDqzBoiDhY8`）
- 波 99b（有效）：`tracking/USA/runs/usa_aieq_w99b.txt` + `_spec.json`（multisim `2ecqJD8rL4ieaiB7iJZeUpF`）
- 波 99b 收批 JSON：`cache/_aieq_w99b_harvest.json`；库内 `backtest_results`（wave=`aieq_w99b`，dataset=`ai_equity_alpha`）
- 波 99c：`tracking/USA/runs/usa_aieq_w99c.txt` + `_spec.json`
- 4 条 ACTIVE 详情：平台 `get_alpha_details`（`1YZQJKwR` / `O08EjLVp` / `d51A3nqY` / `Wje6pdqN`）

## 9. 波 99c 结果与第 6 颗候选（2026-10-23）

multisim `3MggBxa524Uya6UjIrSUc1X`，8 臂全终态。控制臂精确复现（S2.08/F1.16/2Y1.81/SUB1.07），
证明设置与表达式核稳定。

| 臂 | 轴 | S | F | 2Y | SUB | 裁决 |
|---|---|---:|---:|---:|---:|---|
| 1 | industry（控制） | 2.08 | 1.16 | 1.81 | 1.07 | 复现，SUB 仍差 0.03 |
| 2 | `group_zscore` | 0.29 | — | — | — | 崩，弃 |
| 3 | **subindustry** | **2.19** | **1.16** | **1.91** | **1.24** | **全闸过 → 候选** |
| 4 | sector | 1.99 | 1.14 | 1.67 | — | 不如 3 |
| 5 | market | 1.99 | 1.16 | 1.53 | — | 2Y 掉 |
| 6 | industry + platform decay 10 | 2.07 | 1.24 | 1.74 | — | TO 9.38%，F 升但 2Y 降 |
| 7 | `signed_power(...,0.8)` | 2.25 | 1.33 | 1.94 | — | 指标最好，但与 3 同源，只能留一颗 |
| 8 | `ts_mean(22)` 替 zscore | 1.53 | 0.87 | 0.70 | — | 崩，弃 |

**获胜臂 = 3（`subindustry`）→ `YPx89bQJ`**：S2.19/F1.16/2Y1.91/SUB1.24（limit 1.19）/TO15.69%/margin 5.6bp；
`failed_ra_count=0`；prod **0.6803**、self **0.2812**；
稳健性 **CONDITIONAL**（recent-3yr S 1.79 ≥1.58、CV 0.48、衰减比 0.416、max/min 3.25；无硬标记）。
臂 7（`signed_power`）与臂 3 同核，若后续需要第二颗同族备选可先测 self 再定；不得同时提交。

**同波被否**：`O08GeKx1`（队列遗留 READY，`mean_estimate_targetprice_annual12_tribes` 时序位置，
decay 230）稳健性 **REJECT**（衰减比 0.20 / max-min 7.56），已 retire 为 DEAD。

## 10. 波 100 预登记（未测族分歧腿，10 臂）

同壳同设置（TOP2000 / STATISTICAL / decay 0 / trunc 0.08 / subindustry / ts_decay_linear 5），
只换字段对：`alpha_score`↔`_2`（双向）/ `accounting_forensics_factor`↔`_6` /
`accruals_analysis_factor`↔`_10` / `intrinsic_valuation_estimate_3`↔`_91` /
`analyst_forecast_change_score_7`↔`_10` / `business_model_clarity_score`↔`_2` /
`financing_structure_analysis_3`↔`_4` / `balance_sheet_trend_metric_7`↔`_51` /
`buzz_intensity_score_2`↔`_11`。文件 `tracking/USA/runs/usa_aieq_w100.txt`，
multisim `4abGpEr4iqb1ldIsZY3CD`。判据同 99c。

## 11. 波 100 结果：1 颗新候选 + prod 双峰（2026-10-23）

multisim `4abGpEr4iqb1ldIsZY3CD`，10/10 终态、0 error，全部收批入库（wave=`100`）。

| 臂 | 字段对 | S | F | 2Y | SUB | TO | 硬闸 | 裁决 |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | alpha_score − _2 | 2.16 | 0.87 | 1.35 | 1.28 | 27.3% | F/2Y | 否 |
| 2 | alpha_score_2 − alpha_score | 1.54 | 0.52 | 0.93 | 0.48 | 27.3% | 4 项 | 否（改向确认正向是对的） |
| 3 | **accounting_forensics_factor − _6** | **2.57** | **1.46** | **2.00** | **1.75** | 19.0% | **0** | **prod 0.7946 → REJECT** |
| 4 | accruals_analysis_factor − _10 | 0.54 | 0.12 | 0.03 | −0.05 | 24.8% | 4 项 | 否（族死） |
| 5 | **intrinsic_valuation_estimate_3 − _91** | **2.33** | **1.09** | **1.94** | **1.58** | 22.3% | **0** | **prod 0.7761 → REJECT** |
| 6 | analyst_forecast_change_score_7 − _10 | 1.57 | 0.73 | 1.94 | 0.57 | 9.4% | S/F/SUB | 否 |
| 7 | business_model_clarity_score − _2 | 1.88 | 0.98 | 0.67 | 0.87 | 10.3% | F/SUB/2Y | 否 |
| 8 | **financing_structure_analysis_3 − _4** | **2.26** | **1.33** | **2.06** | **1.41** | 12.6% | **0** | **第 7 颗候选（prod 0.6818）** |
| 9 | **balance_sheet_trend_metric_7 − _51** | **2.30** | **1.23** | **2.14** | **1.28** | 16.0% | **0** | **prod 0.7663 → REJECT** |
| 10 | buzz_intensity_score_2 − _11 | 2.42 | 1.26 | 1.69 | 1.13 | 17.7% | SUB（limit 1.28） | 单闸 near-miss，未修 |

**信号机制成立**：12 个字段对里 4 对直接 RA 全过、另 1 对只差 SUB 0.15，说明「模型版本分歧 = 修正速率」这条腿
在本数据集上是真信号，不是拟合；失效的两对（accruals、business_model_clarity）是字段本身无增量。

**prod 双峰（本轮最重要的可复用结论）**：同一壳、同一设置，仅换字段对，prod 分成两簇——
`financing_structure_analysis_3−4` = **0.6818**（过），其余三对 = **0.7663 / 0.7761 / 0.7946**（全 ≥0.75，D0-P dead_end）。
⇒ ① 本壳的**壳本身不撞产线**（否则 58jr102k 也会高）；② 撞的是**字段对的具体持仓**，与 IS 强弱无关
（S 最高的 2.57 撞得最狠 0.7946）；③ 后续同壳新字段对**必须先探 prod 再投稳健链**，否则把配额烧在必死臂上。
换 `hump`/`decay`/平滑轴无效——那只改时序不改持仓，只会把 self 推高。

**组内互相关**（4 年日收益）：`YPx89bQJ` vs 四条分歧腿 0.07/0.07/−0.03/0.19（几乎正交）；
分歧腿彼此 0.39–0.67，阈值 0.5 下最大互相容子集 4 条（`YPx89bQJ`, `npAmlRr8`, `58jr102k`, `j2eoJRMO`）。

**稳健性**（详见 `reports/robustness_20261023.md`）：四臂 Phase C 全过（近 3 年均值 2.23–2.56、CV 0.175–0.332、
衰减比 0.80–1.23、max-min 1.55–2.36）；全历史弱年仅 2018（0.32–0.61），按近窗制度只记软标记。
台账：`robustness_npAmlRr8` / `robustness_QPYOAk6w` / `robustness_58jr102k`（PASS）/ `robustness_N1eLGm2e`。

**未测族仍有余量**：1108 字段里大量 `_2/_4/_6/_10/_51/_91` 版本对未试；但按上条纪律，下一批应
**先用 1 条臂逐对探 prod**（成本 1 次仿真/对），把 prod < 0.70 的对挑出来再扩成完整批。

---

## 12. 波 101 / j2 SUB 修复批（2026-10-22 夜）—— 两批首跑因 nanHandling 漂移作废，已按原设置重发

### 12.1 作废原因（可复用铁律）

两批首批（10 臂新字段对 + 5 臂 j2 SUB 修复）在发批时沿用 MCP `create_multi_simulation`
的 `nan_handling` 缺省值 **OFF**，而本数据集此前 7 颗候选及 j2 全部跑在 **nanHandling=ON**。

对照证据（同表达式核，仅设置不同）：

| alpha | 表达式 | nanHandling | S | F | 2Y | SUB |
|---|---|---|---:|---:|---:|---:|
| `j2eoJRMO` | buzz_2 − buzz_11 壳 | **ON** | **2.42** | 1.26 | 1.69 | 1.13 |
| `3qj1OO2X` | 同核，仅 decay 5→10 | OFF | 0.75 | 0.24 | 0.36 | 0.30 |
| `6XAZQQ2G` | 同核，双窗 5+22 | OFF | 0.73 | 0.24 | 0.30 | 0.43 |

15 臂（10 新对 + 5 修复）在 OFF 下**全部塌到 S 0.73 以下或负值**，无一例外；而 wave 100 的 10 臂
（ON）有 4 臂 RA 全过。⇒ **VECTOR 字段（`vec_avg`）批次对 nanHandling 极敏，OFF/ON 不是微调而是换了一个信号。**

**铁律**：`ai_equity_alpha`（VECTOR 字段）任何批次必须显式传 `nan_handling="ON"`；
MCP 缺省是 OFF，**不传即中毒**，且症状是「整批指标塌陷」而非报错，极易被误读成「字段族已死」。
修复批同理——**必须复制原 alpha 的完整 settings**（本仓已有「设置变体伤指标」的前科，这次是
nanHandling 版本）。

### 12.2 首批（作废）读数留痕

新字段对 10 臂（OFF，全部无效）：earnings_quality_3−4 0.22 · cashflow_variation_2−3 −1.00 ·
asset_impairment_5−41 −0.36 · moat_strength_2−3 −0.21 · long_term_uncertainty_2−3 0.08 ·
dividend_policy_2−6 0.73 · operating_leverage−2 0.08 · efficiency_model_3−4 −0.12 ·
shareholder_treatment−4 0.02 · profit_margin_stability−2 −0.71。
（对应 alpha：`3qj1OOPQ` `YPx8OOzW` `wp93AAGl` `2rj9xx6w` `A1Qe55ze` `xA1VooGp` `E5VNMML1` `9qE833mo` `88vVZZYa` `58jr11ek`）

j2 SUB 修复 5 臂（OFF，全部无效）：`RRA9oovn` 0.83 · `vROZbboz` 0.97 · `RRA9oovd` 0.96 ·
`3qj1OO2X` 0.75 · `6XAZQQ2G` 0.73。

### 12.3 重发（nanHandling=ON，settings 与 wave 100 逐项一致）

| 批次 | multisim | 臂数 | 内容 |
|---|---|---|---|
| 波 101R | `3IjqvacQj4rLcw5VkswKdS7` | 10 | 同 12.2 的 10 个新字段对 |
| SUB 修复 R | `8HHQI9Cg54n9TLfL4vvilD` | 5 | j2 核 × {signed_power0.8/subindustry, market 平铺, signed_power0.8/market, decay10, 双窗5+22} |

设置：USA / TOP2000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / FASTEXPR / unitHandling VERIFY /
**nanHandling ON** / pasteurization ON / maxTrade OFF。

### 12.4 判读口径（预先写死，避免事后挪线）

- 波 101R：只有 `failed_ra_count == 0` 才进 prod 探针；S<1.58 或 2Y<1.58 的臂直接判「字段对无增量」，
  不再为其单独扫参（同 wave 100 的纪律）。
- SUB 修复 R：需 S≥1.58、2Y≥1.58、**SUB ≥ 1.28**（j2 的 platform limit）；且即便全过，
  **j2 的 prod 0.6982 只有 0.0018 余量，改壳后必须重测 prod**，不重测不得进提交队列。

---

## 13. 波 103 结果：信用风险分歧腿产出第 10 颗（2026-10-23）

multisim `2deMBcfPr54hcnrb3pnevvc`，9 臂 / 6 COMPLETE / 3 单位错误。**subindustry 壳**（与 wave 100 同壳同设置，
含 nanHandling ON），只换字段对，全部为未测族。

| 臂 | 字段对 | S | F | 2Y | SUB | 裁决 |
|---|---|---:|---:|---:|---:|---|
| 1 | `xA1V7ALg` cashflow_trend_analysis − _121 | — | — | — | — | **单位不兼容**（见 §13.2） |
| 2 | `3qj1mqK6` fund_flow_prediction_metric − _81 | 2.36 | 1.42 | 1.92 | 1.46 | RA 全过，**prod 0.7168 → 不可提交** |
| 3 | `58jrK8mk` forecast_yield_metric − _91 | — | — | — | — | 单位不兼容 |
| 4 | **`N1eLE1de` credit_risk_model_score_5 − _7** | **2.63** | **1.54** | **2.07** | **1.66** | **prod 0.6916 / self 0.2753 → 第 10 颗（稳健 CONDITIONAL）** |
| 5 | `bl8J0lmK` creditworthiness_assessment_factor − _7 | 1.70 | 0.85 | 1.37 | 0.84 | F/SUB/2Y 三闸 → 族无增量 |
| 6 | `A1QeX1AR` forecast_value_accuracy_metric − _7 | 1.20 | 0.50 | 0.12 | 0.50 | 4 闸 → 族死 |
| 7 | `1Yj3YM6` income_statement_trend_metric − _7 | — | — | — | — | 平台 404（未落 alpha） |
| 8 | `88vVW8wa` forecast_yield_metric_91 − forecast_yield_metric（反向） | — | — | — | — | 单位不兼容 |
| 9 | `0mjxZmJp` credit_risk_model_score_7 − _5（反向） | 0.93 | 0.33 | 0.15 | −0.01 | 4 闸 → **正向确认正确** |

### 13.1 三条可复用结论

1. **2023 弱年是数据集级，不是字段对级**：本数据集已验的三条分歧腿 2023 年 S 全部显著低于前两年
   ——`YPx89bQJ` **0.91**（2021/2022 = 1.79/2.86）、`j2eoKKEj` **1.47**（1.95/2.86）、
   `N1eLE1de` **1.07**（2.50/2.83）。⇒ MODEL 数据集的模型版本更新节奏在 2023 放缓，
   分歧信号整体衰减。**后续同数据集候选在稳健性上要预期 2023 是低点，不得据此单独判死字段对**；
   但也意味着近窗衰减比会系统性偏低（`N1eLE1de` 0.407 即因此落 CONDITIONAL 带）。
2. **方向不可推断再次成立**：`credit_risk_model_score` 正向 2.63 vs 反向 0.93（反向连 F 都只有 0.33）。
   与 §2.2 的两例同向 ⇒ **新族一律双向测**，这是最低成本的必做项。
3. **prod 双峰再次成立**：同壳同设置下 `fund_flow` 对 **0.7168** / `credit_risk` 对 **0.6916**，
   且 S 更高的后者 prod 更低 ⇒ prod 由**字段对具体持仓**决定、与 IS 强弱无关（与 §11 一致）。
   后续同壳新字段对仍应「先 1 条臂探 prod，再投稳健链」。

### 13.2 单位不兼容族（`subtract` index 1 期望 `Unit[]` 实得 `Unit[CSPrice:1]`）

`cashflow_trend_analysis`、`forecast_yield_metric` 与它们的 `_121`/`_91` 版本相减时，
两版本单位不一致（一版无量纲、一版带价格量纲）⇒ 平台直接 ERROR，**双向都不可用**。
判据在跑之前看不出来（`validate_expressions` 只校字段存在与语法，不校单位），
只能用 1 条臂试。同类前科：`E5VNPlEP`。**这两个族在分歧腿上判死**（不是字段无信号，是单位不可相减）。

### 13.3 SUB 读数（为后续同数据集铺路）

subindustry 壳下 `3qj1mqK6` 比值 1.46/2.36 = **0.619**、`N1eLE1de` 1.66/2.63 = **0.631**，
**显著高于 0.527 门槛**（对比 wave 100 的 `npAmlRr8` 1.75/2.57 = 0.681、`j2eoJRMO` 1.13/2.42 = 0.467）。
⇒ 本壳的 SUB 表现由字段对决定，`fund_flow` / `credit_risk` 两个族在 subindustry 轴下不缺 SUB 余量，
**不需要上 `market` 轴修复**（与 j2 的 0.467 需换轴形成对照）。
