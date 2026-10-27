# event_relation — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `event_relation` |
| 名称 | Text-Based Event Relationship Analysis |
| 类别 | OTHER |
| 数据字段数(平台) | 12 |
| 覆盖率 | 0.5769 |
| 平台已有 alpha | 3 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages advanced language models to extract and classify relationships between companies, events, and entities from unstructured text sources such as news articles, press releases, and corporate communications. By identifying the types and directions of these relationships, the dataset provides structured insights into how companies interact, form alliances, or respond to market developments. This information is valuable for predicting price movements, as changes in company relationships—such as mergers, partnerships, or competitive actions—often precede significant market reactions. The dataset enhances traditional event-driven strategies by offering a deeper, more nuanced understanding of the connections and influences within the market ecosystem.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **12** |
| 类型分布 | VECTOR×12 |
| 平均覆盖率 | **0.577** |
| 覆盖率区间 | 0.47 ~ 0.74 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 3 | 25.0% |
| 低 (0.50–0.70) | 6 | 50.0% |
| 稀疏 (<0.50) | 3 | 25.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 6 | 50.0% |
| DEAD | 4 | 33.3% |
| UNTESTED | 2 | 16.7% |

- 已实测字段：**4** 个（33%），best_sharpe 最高 **0.43**，中位 0.35

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 8 | 0.58 | relation_strength_rank_merger、relation_strength_score_financial、relation_strength_score_partner |
| 元数据与非信号 | 4 | 0.58 | entity_connection_type_general、entity_connection_type_financial、entity_connection_type_partner |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `entity_connection_type_general` | VECTOR | 0.740 | 元数据与非信号 | 1 | 0.43 | 0.86 | 0.40 | DEAD | Signed integer code for the relationship type and direction between the focal stock and its counterparty within the All |
| 2 | `relation_strength_rank_merger` | VECTOR | 0.466 | 风险与质量 | 3 | 0.35 | -0.07 | 0.61 | DEAD | Vendor/event-native integer code indicating confidence/status/classification of the MA relationship edge on the as-of da |
| 3 | `relation_strength_score_financial` | VECTOR | 0.588 | 风险与质量 | 1 | 0.07 | -0.52 | -0.12 | DEAD | Vendor-native quantitative impact or confidence score (typically 0–1) for the financial relationship edge on that date, |
| 4 | `relation_strength_score_partner` | VECTOR | 0.515 | 风险与质量 | 1 | -0.67 | -0.66 | -0.46 | DEAD | Vendor-native quantitative impact or confidence score for the partnership edge on that as-of-date (typically 0–1), used |
| 5 | `relation_strength_rank_general` | VECTOR | 0.740 | 风险与质量 | 0 | — | — | — | UNTESTED | Vendor-native integer code indicating the relationship’s confidence, status, or classification for each edge on that dat |
| 6 | `relation_strength_score_general` | VECTOR | 0.740 | 风险与质量 | 0 | — | — | — | UNTESTED | Vendor-native quantitative impact or confidence score, typically between 0 and 1, used directly for weighting and propag |
| 7 | `entity_connection_type_financial` | VECTOR | 0.588 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Integer code for the observed, directional financial relationship type from the current stock (A) to the counterparty (B |
| 8 | `relation_strength_rank_financial` | VECTOR | 0.588 | 风险与质量 | 0 | — | — | — | UNUSABLE | Vendor/event-native categorical integer code indicating confidence, status, or classification of the financial relations |
| 9 | `entity_connection_type_partner` | VECTOR | 0.515 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Integer code encoding the type and direction of the partnership/alliance/contractual relationship between the focal stoc |
| 10 | `relation_strength_rank_partner` | VECTOR | 0.515 | 风险与质量 | 0 | — | — | — | UNUSABLE | Integer vendor-native categorical code describing confidence/status/classification of the partner relationship on the as |
| 11 | `entity_connection_type_merger` | VECTOR | 0.466 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Integer code encoding the specific MA-family relationship type and direction (e.g., acquisition, merger, joint venture) |
| 12 | `relation_strength_score_merger` | VECTOR | 0.466 | 风险与质量 | 0 | — | — | — | UNUSABLE | Vendor-native quantitative impact or confidence score (typically 0–1) for the MA relationship edge, used directly for we |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `qMxj6zPK` | 0.43 | 0.29 | 0.86 | 0.40 | 0.03 | ["LOW_SHARPE | 233 | `divide(ts_std_dev(vec_avg(entity_connection_type_general), 252), ts_std_dev(vec_avg(entity` |
| `MPa7L856` | 0.42 | 0.14 | 0.48 | 0.34 | 0.07 | ["LOW_SHARPE | 233 | `divide(days_from_last_change(vec_avg(entity_connection_type_general)), ts_backfill(days_fr` |
| `blbjdPom` | 0.37 | 0.12 | 0.07 | 0.24 | 0.08 | ["LOW_SHARPE | 233 | `group_neutralize(subtract(quantile(days_from_last_change(vec_avg(entity_connection_type_me` |
| `9qjX76aK` | 0.35 | 0.19 | -0.07 | 0.61 | 0.19 | ["LOW_SHARPE | 233 | `group_count(vec_avg(relation_strength_rank_merger), sector)` |
| `9qjX769K` | 0.07 | 0.01 | -0.52 | -0.12 | 0.08 | ["LOW_SHARPE | 233 | `group_rank(ts_backfill(vec_avg(relation_strength_score_financial),22), bucket(rank(ts_back` |
| `QPb79lnK` | -0.10 | -0.03 | -0.72 | -0.06 | 0.26 | ["LOW_SHARPE | 233 | `group_std_dev(vec_avg(relation_strength_rank_merger), sector)` |
| `e7bzx2d6` | -0.14 | -0.05 | -1.32 | -0.23 | 0.28 | ["LOW_SHARPE | 233 | `group_mean(vec_avg(relation_strength_rank_merger), vec_avg(relation_strength_rank_general)` |
| `58zlk6L1` | -0.67 | -0.48 | -0.66 | -0.46 | 0.10 | ["LOW_SHARPE | 233 | `group_zscore(ts_backfill(vec_avg(relation_strength_score_partner),22), bucket(rank(ts_back` |

## 七、判死记录（sealed dead_end）

- `EUR-EVENT-RELATION-WEAK`（2026-09-23T18:22:52）family=event_relation 实体关系强度族（relation_strength_rank/score × merger/partner/financial/general）：{"family": "event_relation 实体关系强度族（relation_strength_rank/score × merger/partner/financial/general）", "reason": "wave233 8 探针全灭 max/sharpe/=0.43 < 0.5 → 达 EUR fast_kill 判死线。字段全冷门（users<=1）理论 prod≈0，纯信号缺席。OTHER 塔已连续三集判死（acquisition_model 0.16 / insider_feats 多样性墙 / event_relation 0.43）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-
- `EUR-INSIDER-FEATS-WEAK`（2026-09-23T18:35:49）family=insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）：{"family": "insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）", "reason": "wave238 10 探针全灭 best /sharpe/=0.47 < 0.5 → 达 fast_kill 判死线。此前 w232 多样性闸（flow 单 exposure）+ 字段名拼接幻觉 + 低覆盖无 backfill 三轮门禁墙已记录。OTHER 塔 4 候选全灭（acquisition_model/insider_feats/event_relation + ml_factor_proj 平台无字段）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at

