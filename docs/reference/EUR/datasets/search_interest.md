# search_interest — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `search_interest` |
| 名称 | Rapid Search Interest Signals |
| 类别 | OTHER |
| 数据字段数(平台) | 5 |
| 覆盖率 | 0.7815 |
| 平台已有 alpha | 7 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset captures real-time search interest data for specific companies and regions, using a standardized algorithm to transform hourly search trends into a continuous, unbounded metric. By estimating daily search activity from high-frequency data and providing a confidence score for each estimate, it enables timely detection of shifts in public attention or sentiment. Such rapid changes in search volume can serve as early indicators of market-moving events, news, or shifts in investor sentiment, making the dataset valuable for predicting short-term price movements and generating alpha signals.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **5** |
| 类型分布 | VECTOR×5 |
| 平均覆盖率 | **0.781** |
| 覆盖率区间 | 0.25 ~ 0.93 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 4 | 80.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 1 | 20.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 4 | 80.0% |
| UNUSABLE | 1 | 20.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 4 / UNUSABLE 1 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 3 | 0.70 | relative_interest_score_7、relative_interest_score_6、relative_interest_score_8 |
| 其他 | 1 | 0.91 | trend_confidence_overlap_months_4 |
| 修正与预期 | 1 | 0.91 | trend_estimation_confidence_score_4 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `relative_interest_score_7` | VECTOR | 0.928 | 风险与质量 | 0 | — | — | — | UNTESTED | Standardized search interest score for the term; unbounded float comparable across time and terms (not the raw 0–100 scale) |
| 2 | `relative_interest_score_6` | VECTOR | 0.909 | 风险与质量 | 0 | — | — | — | UNTESTED | Standardized unbounded daily search interest score comparable across time and terms |
| 3 | `trend_confidence_overlap_months_4` | VECTOR | 0.909 | 其他 | 0 | — | — | — | UNTESTED | the confident of our guessing over months |
| 4 | `trend_estimation_confidence_score_4` | VECTOR | 0.909 | 修正与预期 | 0 | — | — | — | UNTESTED | Confidence score of the nowcasted search interest value; higher indicates more reliable estimates |
| 5 | `relative_interest_score_8` | VECTOR | 0.251 | 风险与质量 | 0 | — | — | — | UNUSABLE | Standardized, unbounded search interest score indicating the term’s popularity, comparable across time and terms |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

