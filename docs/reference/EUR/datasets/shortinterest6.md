# shortinterest6 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `shortinterest6` |
| 名称 | SmartHoldings Model |
| 类别 | MODEL |
| 数据字段数(平台) | 11 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 27 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset is a global stock selection model that ranks stocks based on the predicted future change in institutional ownership. It looks into various funds and creates their purchasing profile based on the underlying fundamental or technical factors of the companies it buys. Aggregation over different funds help predict future probable changes in institutional ownership of the stocks.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **11** |
| 类型分布 | MATRIX×11 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 11 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 11 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 7 | 1.00 | star_hold_country_rank、star_hold_global_owner_rank、star_hold_global_rank |
| 风险与质量 | 2 | 1.00 | star_hold_global_change_rank、star_hold_global_screening_rank |
| 宏观与行业 | 2 | 1.00 | star_hold_region_change_rank、star_hold_region_screening_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `star_hold_country_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The country 1-100 rank of the smart holdings model |
| 2 | `star_hold_global_change_rank` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The change component 1-100 global rank |
| 3 | `star_hold_global_owner_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The peers adjustment factor 1-100 global rank. This factor is reversed - 100 indicates high peer ownership for the secur |
| 4 | `star_hold_global_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The global 1-100 rank of the Smart Holdings model |
| 5 | `star_hold_global_screening_rank` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | The peers-adjusted screening component 1-100 global rank |
| 6 | `star_hold_industry_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The industry 1-100 rank of the Smart Holdings model |
| 7 | `star_hold_region_change_rank` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The change component 1-100 regional rank |
| 8 | `star_hold_region_owner_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The peers adjustment factor 1-100 regional rank. This factor is reversed - 100 indicates high peer ownership for the sec |
| 9 | `star_hold_region_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The regional 1-100 rank of the Smart Holdings model |
| 10 | `star_hold_region_screening_rank` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The peers-adjusted screening component 1-100 regional rank |
| 11 | `star_hold_sector_rank` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The sector 1-100 rank of the smart holdings model |

## 六、本地回测证据

- 本地累计回测 **28** 条；其中 `ra_failed_checks` 为空的 **28** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `YP5GKerl` | — | — | — | — | — | 0 | 109 | `rank(multiply(star_hold_global_rank, rank(subtract(star_hold_region_change_rank, star_hold` |
| `zqY16V6K` | — | — | — | — | — | 0 | 109 | `rank(subtract(star_hold_global_screening_rank, star_hold_global_owner_rank))` |
| `9qVL1n1K` | — | — | — | — | — | 0 | 109 | `ts_ir(star_hold_global_rank, 60)` |
| `LL9AaQa1` | — | — | — | — | — | 0 | 109 | `ts_rank(subtract(star_hold_global_screening_rank, star_hold_region_screening_rank), 10)` |
| `883d9w9V` | — | — | — | — | — | 0 | 109 | `ts_zscore(subtract(star_hold_global_rank, star_hold_country_rank), 10)` |
| `YP5GKeKR` | — | — | — | — | — | 0 | 109 | `ts_zscore(subtract(star_hold_region_change_rank, star_hold_region_rank), 10)` |
| `2rObzYbP` | — | — | — | — | — | 0 | 109 | `winsorize(subtract(star_hold_global_rank, star_hold_industry_rank), std=4)` |
| `vRk3MQ3d` | — | — | — | — | — | 0 | 109 | `rank(ts_covariance(star_hold_global_screening_rank, star_hold_global_owner_rank, 22))` |
| `rK5vgxvd` | — | — | — | — | — | 0 | 109 | `group_sum(ts_zscore(subtract(star_hold_global_rank, star_hold_country_rank), 10), industry` |
| `O0rEaKwR` | — | — | — | — | — | 0 | 110 | `add(multiply(0.4, rank(subtract(star_hold_global_screening_rank, star_hold_global_owner_ra` |
| `LL9AJObv` | — | — | — | — | — | 0 | 110 | `add(multiply(0.4, rank(subtract(star_hold_global_screening_rank, star_hold_global_owner_ra` |
| `883d1g7q` | — | — | — | — | — | 0 | 110 | `add(multiply(0.4, rank(subtract(star_hold_global_screening_rank, star_hold_global_owner_ra` |
| `le8bXJkl` | — | — | — | — | — | 0 | 110 | `add(multiply(0.4, ts_ir(star_hold_global_rank, 60)), multiply(0.6, rank(ts_delta(common_ga` |
| `mLgM9eJ1` | — | — | — | — | — | 0 | 110 | `add(multiply(0.4, ts_ir(star_hold_global_rank, 60)), multiply(0.6, rank(ts_delta(avg_simil` |
| `QP3LXmjM` | — | — | — | — | — | 0 | 110 | `add(multiply(0.4, ts_ir(star_hold_global_rank, 60)), multiply(0.6, rank(ts_delta(avg_simil` |

## 七、判死记录（sealed dead_end）

- `EUR-STARHOLD-SCREENING-GZSCORE-PROD`（2026-08-23）family=shortinterest：{"dataset": "shortinterest6", "example_id": "kqjnKz1K", "expr_pattern": "group_zscore(star_hold_global_screening_rank, industry)", "fitness": 0.96, "prod_corr": 0.8859, "reason": "COUNTRY/6 wrapper lifts starhold to S1.39 F0.96 2Y1.45 but prod 0.89 and LOW_SUB 0.39. EUR/D1/MODEL crowded. Sibling E5lqK9gL S1.38 F0.96 2Y1.49 same wall likely. Do not Mode A clone screening zscore.", "settings": "EUR 
- `EUR-STARHOLD-SCREENING-RESID-PROD`（2026-08-23）family=shortinterest residual of screening_rank：{"dataset": "shortinterest6", "example_id": "j2jn0RRQ", "expr_pattern": "rank(subtract(star_hold_global_screening_rank, group_mean(..., industry/country))) / ts_av_diff mix", "fitness": 0.92, "prod_corr": 0.8891, "reason": "group_mean residual ≈ gzscore; still prod 0.85-0.89. ts_av_diff killed Sharpe (0.20-0.55). Do not Mode A clone residual wrappers of screening_rank.", "settings": "EUR TOP2500 C
- `EUR-STARHOLD-SECTOR-RANK-PROD`（2026-08-24）family=shortinterest star_hold_sector_rank dominant：{"dataset": "shortinterest6", "example_id": "9qX9XMNq", "expr_pattern": "rank/group_neutralize(star_hold_sector_rank)", "settings": "EUR TOP2500 COUNTRY decay6", "sharpe": 1.28, "fitness": 0.91, "two_year_sharpe": 1.43, "sub_universe_sharpe": 0.42, "prod_corr": 0.8992, "wave": 38, "id": "EUR-STARHOLD-SECTOR-RANK-PROD", "family": "shortinterest star_hold_sector_rank dominant", "reason": "Near-gate 
- `EUR-STARHOLD-INDUSTRY-RANK-PROD`（2026-08-24）family=shortinterest star_hold_industry_rank dominant：{"dataset": "shortinterest6", "example_id": "gJjma78O", "expr_pattern": "rank(star_hold_industry_rank)", "settings": "EUR TOP2500 COUNTRY decay6", "sharpe": 1.34, "fitness": 0.9, "two_year_sharpe": 1.59, "sub_universe_sharpe": 0.44, "prod_corr": 0.8787, "wave": 40, "id": "EUR-STARHOLD-INDUSTRY-RANK-PROD", "reason": "Near-gate Fitness 0.90 2Y1.59 but prod 0.8787 same EUR/D1/MODEL wall as screening/
- `EUR-STARHOLD-COUNTRY-RANK-PROD`（2026-08-24）family=shortinterest star_hold_country_rank dominant：{"dataset": "shortinterest6", "example_id": "xAjevXdp", "expr_pattern": "rank(star_hold_country_rank)", "settings": "EUR TOP2500 COUNTRY decay6", "sharpe": 1.19, "fitness": 0.85, "two_year_sharpe": 1.46, "sub_universe_sharpe": 0.37, "prod_corr": 0.8935, "wave": 40, "id": "EUR-STARHOLD-COUNTRY-RANK-PROD", "reason": "S1.19 F0.85 2Y1.46 prod 0.8935. Same EUR/D1/MODEL wall as industry/sector/screening
- `EUR-shortinterest6-CHANGE-OWNER-WEAK`（2026-09-03）family=shortinterest6 change/owner component：{"best_2y": 1.15, "best_alpha": "YP5GKerl", "best_sharpe": 1.24, "contract_ops": "ts_covariance/group_sum 双槽失效（S-0.20/-0.27）", "dataset": "shortinterest6", "direction": "change 正向（S1.24）、owner 反向（S-0.07 原始，镜像+0.07）", "evidence": "wave109 9 条全灭：change/owner 组件（ts_zscore/ts_rank/ts_ir/rank 差值）最高 Sharpe 1.24 未达 1.58 硬闸", "not_dead": "0.40 minority slow mix × 0.60 pattern_scores 快腿（win recipe）未测，short
- `EUR-shortinterest6-PATTERN-FAST-LEG-PROD`（2026-09-03）family=shortinterest6 × pattern_scores fast leg variants：{"best_2y": 1.53, "best_alpha": "rK5vmoMJ", "best_sharpe": 1.38, "evidence": "wave111 9 条：Mode B 换 pattern_scores 快腿字段（breakaway_gap_up/common_gap_up max/min/q95/dynamic）最高 Sharpe 1.38 未达 1.58 硬闸", "not_dead": "shortinterest6 慢腿与其他数据集快腿（非 pattern_scores）组合未测；但 pattern_scores 快腿与 star_hold 慢腿组合 prod 墙 0.74-0.90 已确认", "reason": "star_hold 家族与任何 pattern_scores 快腿组合 prod_corr 必超 0.7（wave110 0.74-0.77）

