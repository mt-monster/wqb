# Robustness 审计（DEU，2026-11-23）

> 范围：DEU / TOP500 / D1。候选来自 `tracking/DEU/regular_tower/HARVEST_20261123.md`。
> 依据 `brain-alpha-robustness` Phase B/C：平台 `get_alpha_details` + `get_alpha_yearly_stats` + `check_correlation`（refresh=True）实读。
> 平台阈值：S 1.58 / F 1.0 / 2Y 1.58 / prod<0.70 / self<0.70（严格不等式）。

## 1. vRApe2Av — PASS

| 项 | 读数 |
|---|---|
| 表达式 | `signed_power(group_zscore(add(group_rank(ts_mean(divide(significant_value_1, Σsignificant_value_1..4),66),sector), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,22))),sector),1.3)` |
| 设置 | DEU/TOP500/D1, decay0, SUBINDUSTRY, trunc0.08, nan ON, 2014–2023 |
| pyramids | `[DEU/D1/INSIDERS ×1.6, DEU/D1/MODEL ×1.8]` effective=2 |
| 平台指标 | S **1.70** / F **1.36** / 2Y **2.38** / TO 8.7% / DD 6.55% / margin 18.49bp / LC 131 / SC 146 |
| RA | `failed_ra_count=0`（LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CONCENTRATED_WEIGHT/LOW_SUB/IS_LADDER/CLUSTER/MATCHES_PYRAMID 全 PASS；仅 MATCHES_COMPETITION/THEMES warning） |
| prod | **0.5707 PASS**（refresh=True，2026-11-23；直方图无 0.9+ 孤立尖峰） |
| self | **0.4780 PASS**（OS 池 22，最高对手 blRnKEk6 0.478） |
| 逐年 | 2014–2023 **每年 LC/SC>0 且 pnl>0**（2014 0.79 → 2023 2.72；最弱 2016 0.49） |
| Recent-3yr | 2021 1.69 / 2022 2.08 / 2023 2.72 → 三正、均值 2.16；CV≈**0.20**；max/min 1.61 |
| 衰减比 | 2023 S / 全期 S = 2.72/1.70 = **1.60** |
| 判定 | **PASS**（无硬标记；经济含义：内部人增持强度 × 分析师 EBIT 预期上调） |

## 2. QP0MNr5X — CONDITIONAL（软标记：recent-3 CV 0.50、max/min 4.1）

| 项 | 读数 |
|---|---|
| 表达式 | `signed_power(group_zscore(add(group_rank(ts_mean(divide(significant_value_1, Σsignificant_value_1..4),66),sector), rank(ts_mean(predicted_surprise_f12m_ebitda_4,5)), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4,5))),sector),1.3)` |
| pyramids | `[DEU/D1/INSIDERS ×1.6, DEU/D1/MODEL ×1.8]` effective=2 |
| 平台指标 | S **1.82** / F **1.11** / 2Y **2.96** / TO 23.1% / DD 5.64% / margin 7.44bp / LC 127 / SC 144 |
| RA | **failed_ra_count=0** |
| prod | **0.6502 PASS**（refresh=True；最大对手 0.6502，直方图健康） |
| self | **0.5096 PASS**（最高对手 883Y3bAW 0.510） |
| 逐年 | 2014–2023 每年 LC/SC>0 且 pnl>0（最弱 2014 S0.29 / 2019 S0.67；2023 S3.71） |
| Recent-3yr | 2021 0.90 / 2022 2.33 / 2023 3.71 → 三正、均值 2.31；CV≈**0.50**（CONDITIONAL 带 0.40–0.60）；max/min **4.12**（CONDITIONAL 带 3–5） |
| 衰减比 | 3.71/1.82 = **2.04** |
| 判定 | **CONDITIONAL**：无 REJECT 项；软标记 = recent-3 CV 0.50 + max/min 4.12。按 skill 应先 repair 并重审（≤2 轮）再请用户确认；若用户接受软标记可直接进入 prod/提交链（`submit_verdict` 只会因 REJECT 阻断）。 |

## 3. 两颗候选的独立性

- 4 年日 PnL 互相关 **0.5139**（`compute_mutual_correlation`，1021 点）⇒ 可同篮（<0.70）。
- 同族变体（leadEXnl 0.848 / j2avPlgW 0.847 / Jj8qWmlx 0.836）不可同篮。
- 与已提交 OS 池：vRApe2Av self 0.478、QP0MNr5X self 0.510，均 <0.70。

## 4. 待办 / 说明

- `get_alpha_pnl` 逐股集中度未取（工具返回大序列，本轮以 yearly + LC/SC 覆盖度作替代）；Top-5 集中度仍是未测项。
- QP0MNr5X 的 CONDITIONAL 修复空间：提高 decay / 加 tail 压缩可降 recent-3 波动，但会改变 prod/self，需重新过闸；本轮未做（配额排队）。
- 提交前置：用户确认 + `workflow_submit_alpha(confirm_submit=True)`；本报告**不提交**。
