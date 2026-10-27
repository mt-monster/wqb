# stock_cluster_dl — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `stock_cluster_dl` |
| 名称 | Deep Learning Stock Clusters |
| 类别 | OTHER |
| 数据字段数(平台) | 5 |
| 覆盖率 | 0.4563 |
| 平台已有 alpha | 1 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset groups stocks into clusters using deep learning models that analyze 2D images generated from time series financial charts. By mimicking the perspective of retail traders, the dataset leverages convolutional neural networks to extract learned representations from price and fundamental chart images, then applies advanced clustering techniques such as k-means++ and dimension reduction. The resulting clusters reflect similarities in stock behavior, sector, and other financial characteristics, providing a high-dimensional, feature-rich grouping beyond traditional sector classifications. These clusters can be used to identify homogenous groups of stocks, improve portfolio diversification, and enhance risk modeling. By understanding how stocks are grouped based on complex chart patte

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **5** |
| 类型分布 | MATRIX×5 |
| 平均覆盖率 | **0.456** |
| 覆盖率区间 | 0.17 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 1 | 20.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 1 | 20.0% |
| 稀疏 (<0.50) | 3 | 60.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 4 | 80.0% |
| UNTESTED | 1 | 20.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 1 / UNUSABLE 4 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 5 | 0.46 | principal_component_features_9、principal_component_features_7、principal_component_features_5 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `principal_component_features_9` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Feature vector for each stock derived from principal component analysis (TOP2500 universe). |
| 2 | `principal_component_features_7` | MATRIX | 0.526 | 其他 | 0 | — | — | — | UNUSABLE | Feature vector for each stock derived from principal component analysis (TOP1200 universe). |
| 3 | `principal_component_features_5` | MATRIX | 0.340 | 其他 | 0 | — | — | — | UNUSABLE | Feature vector for each stock derived from principal component analysis (TOP800 universe). |
| 4 | `principal_component_features_6` | MATRIX | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Feature vector for each stock derived from principal component analysis (TOP600 universe). |
| 5 | `principal_component_features_8` | MATRIX | 0.166 | 其他 | 0 | — | — | — | UNUSABLE | Feature vector for each stock derived from principal component analysis (TOP400 universe). |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

