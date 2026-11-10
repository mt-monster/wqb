# DEU 字段画像存档索引（172 数据集 / 20012 字段）

**生成时间**：2026-11-10 03:5x　**方式**：MCP `get_datafields` 逐集实时拉取（非缓存画像库）
**路径**：`tracking/DEU/atom_orthogonal/<dataset_id>_fields.csv`
**列**：`id,type,cov,uc,ac,desc`（id 字段名 / type 类型 / cov 平台覆盖率 / uc 使用者数 / ac 已产出 alpha 数 / desc 官方描述）
**机器可读索引**：`field_profile_index.json`

## 全局统计

| 项 | 值 |
|---|---:|
| 数据集总数 | 172 |
| 字段总数 | **20012** |
| MATRIX 型字段 | 11624 |
| VECTOR 型字段 | 6759 |
| GROUP 型字段 | 1515 |

## 按字段数 Top 30

| # | 数据集 | 字段 | MATRIX | VECTOR | GROUP | SYMBOL | 已被用字段 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | **analyst_consensus** | 1972 | 18 | 1954 | 0 | 0 | 209 |
| 2 | **other455** | 1500 | 300 | 0 | 1200 | 0 | 409 |
| 3 | **analyst_revision_horizons** | 1095 | 1095 | 0 | 0 | 0 | 230 |
| 4 | **fundamental72** | 1031 | 347 | 684 | 0 | 0 | 334 |
| 5 | **pv20** | 681 | 678 | 0 | 3 | 0 | 193 |
| 6 | **multifactor_return_pred** | 648 | 648 | 0 | 0 | 0 | 262 |
| 7 | **predictive_starmine** | 631 | 631 | 0 | 0 | 0 | 282 |
| 8 | **analyst7** | 608 | 608 | 0 | 0 | 0 | 352 |
| 9 | **intraday_pv_feats** | 585 | 585 | 0 | 0 | 0 | 156 |
| 10 | **continuation_score** | 560 | 560 | 0 | 0 | 0 | 73 |
| 11 | **model26** | 548 | 548 | 0 | 0 | 0 | 240 |
| 12 | **model109** | 544 | 271 | 273 | 0 | 0 | 185 |
| 13 | **analyst15** | 537 | 533 | 0 | 0 | 4 | 119 |
| 14 | **pattern_scores** | 504 | 504 | 0 | 0 | 0 | 158 |
| 15 | **global_seasonal_model** | 449 | 449 | 0 | 0 | 0 | 64 |
| 16 | **fundamental89** | 407 | 407 | 0 | 0 | 0 | 115 |
| 17 | **techindi_model** | 399 | 399 | 0 | 0 | 0 | 337 |
| 18 | **model264** | 380 | 380 | 0 | 0 | 0 | 114 |
| 19 | **analyst83** | 345 | 0 | 345 | 0 | 0 | 27 |
| 20 | **analyst69** | 292 | 104 | 188 | 0 | 0 | 120 |
| 21 | **quant_factor_lib** | 289 | 0 | 289 | 0 | 0 | 25 |
| 22 | **pv30** | 285 | 0 | 0 | 285 | 0 | 120 |
| 23 | **order_book_imbalance** | 256 | 0 | 256 | 0 | 0 | 75 |
| 24 | **sentiment33** | 255 | 0 | 255 | 0 | 0 | 34 |
| 25 | **model138** | 240 | 0 | 240 | 0 | 0 | 107 |
| 26 | **other696** | 220 | 0 | 220 | 0 | 0 | 20 |
| 27 | **model25** | 217 | 217 | 0 | 0 | 0 | 193 |
| 28 | **fundamental6** | 196 | 196 | 0 | 0 | 0 | 196 |
| 29 | **earningscall_sentiment** | 167 | 144 | 23 | 0 | 0 | 78 |
| 30 | **model262** | 159 | 159 | 0 | 0 | 0 | 25 |

## 字段类型对构造的硬约束（判据 BU / CK）

| 类型 | 可用 | 不可用 |
|---|---|---|
| MATRIX | 全部（含 group_*、ts_*） | - |
| **VECTOR（事件型）** | vec_avg / vec_max / vec_sum / vec_count 等聚合 | **group_rank / group_zscore / group_neutralize / group_mean / group_count 全部报 does not support event inputs** |
| GROUP | 只能作 group 参数（且不能是数据集自带的分类标签轴） | 作值字段 |

=> 凡 VECTOR 事件字段 + 数据集自带数值坐标轴的构造（如期权 IV 面偏斜）在本平台结构性不可行。

## 覆盖率字段的可靠性警告

cov 列在本区系统性失真（大量 cov=0 的数据集实际有满十年供数，已由探针仿真 + yearly longCount 实查推翻，见 cov0_audit_final_20261109.csv）。
**判断数据有无必须用探针仿真 + get_alpha_yearly_stats 的 longCount，不得依赖 cov。**
