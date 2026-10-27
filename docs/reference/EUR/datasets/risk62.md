# risk62 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `risk62` |
| 名称 | Beta Risk Factors |
| 类别 | RISK |
| 数据字段数(平台) | 233 |
| 覆盖率 | 0.9974 |
| 平台已有 alpha | 488 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.0 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RIC) and Bloomberg Identifiers (BBID) for securities. It consolidates data from multiple sources and tracks changes in data generation over time, ensuring accurate cross-referencing between major financial data vendors. This mapping is essential for analysts and portfolio managers who need to integrate, reconcile, or compare datasets from different platforms, enabling seamless data aggregation and analysis. While not directly predictive of price movements, it is a critical foundational resource for building robust multi-source financial models and ensuring data integrity in quantitative research.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **233** |
| 类型分布 | MATRIX×233 |
| 平均覆盖率 | **0.997** |
| 覆盖率区间 | 0.93 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 233 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 225 | 96.6% |
| DEAD | 8 | 3.4% |

- 已实测字段：**8** 个（3%），best_sharpe 最高 **0.23**，中位 0.13

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 201 | 1.00 | rsk62_1_100_val19、rsk62_1_100_val21、rsk62_1_100_val24 |
| 风险与质量 | 16 | 0.98 | rsk62_beta_1_100_qe2d、rsk62_beta1_1_100_mtl、rsk62_beta1_1_100_growth |
| 修正与预期 | 8 | 1.00 | rsk62_beta_1_100_volatility、rsk62_beta_1_100_mts、rsk62_1_100_intercept |
| 价量与波动 | 7 | 0.95 | rsk62_risk_mts、rsk62_beta1_1_100_volatility、rsk62_beta_1_100_averagereturn |
| 盈利与财务 | 1 | 1.00 | rsk62_return |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `rsk62_risk_mts` | MATRIX | 0.935 | 价量与波动 | 1 | 0.23 | — | — | DEAD | Style factor exposure: short-term momentum in stock returns, cross-section normalized |
| 2 | `rsk62_1_100_val19` | MATRIX | 1.000 | 其他 | 1 | 0.19 | — | — | DEAD | Val19 |
| 3 | `rsk62_beta_1_100_volatility` | MATRIX | 1.000 | 修正与预期 | 1 | 0.14 | — | — | DEAD | Regression beta coefficient for the recent return volatility style factor, estimated over a 100-day window using 1-day forward returns |
| 4 | `rsk62_1_100_val21` | MATRIX | 1.000 | 其他 | 1 | 0.13 | — | — | DEAD | Val21 |
| 5 | `rsk62_1_100_val24` | MATRIX | 1.000 | 其他 | 1 | 0.03 | — | — | DEAD | Val24 |
| 6 | `rsk62_beta_1_100_qe2d` | MATRIX | 1.000 | 风险与质量 | 1 | -0.05 | — | — | DEAD | d2eq |
| 7 | `rsk62_beta1_1_100_mtl` | MATRIX | 1.000 | 风险与质量 | 1 | -0.10 | — | — | DEAD | ltm |
| 8 | `rsk62_beta_1_100_mts` | MATRIX | 1.000 | 修正与预期 | 1 | -0.25 | — | — | DEAD | Regression beta coefficient for the short-term momentum style factor, estimated over a 100-day window using 1-day forward returns |
| 9 | `rsk62_1_100_intercept` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Intercept term of the multi-factor regression used to estimate combined betas in the USA risk model (1-day horizon, 100-day trailing window) |
| 10 | `rsk62_1_100_val10` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val10 |
| 11 | `rsk62_1_100_val100` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val100 |
| 12 | `rsk62_1_100_val11` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val11 |
| 13 | `rsk62_1_100_val12` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val12 |
| 14 | `rsk62_1_100_val13` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val13 |
| 15 | `rsk62_1_100_val14` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val14 |
| 16 | `rsk62_1_100_val15` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val15 |
| 17 | `rsk62_1_100_val16` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val16 |
| 18 | `rsk62_1_100_val17` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val17 |
| 19 | `rsk62_1_100_val18` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val18 |
| 20 | `rsk62_1_100_val20` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val20 |
| 21 | `rsk62_1_100_val22` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val22 |
| 22 | `rsk62_1_100_val23` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val23 |
| 23 | `rsk62_1_100_val25` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val25 |
| 24 | `rsk62_1_100_val26` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val26 |
| 25 | `rsk62_1_100_val27` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val27 |
| 26 | `rsk62_1_100_val28` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val28 |
| 27 | `rsk62_1_100_val29` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val29 |
| 28 | `rsk62_1_100_val3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val3 |
| 29 | `rsk62_1_100_val30` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val30 |
| 30 | `rsk62_1_100_val31` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val31 |
| 31 | `rsk62_1_100_val32` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val32 |
| 32 | `rsk62_1_100_val33` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val33 |
| 33 | `rsk62_1_100_val34` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val34 |
| 34 | `rsk62_1_100_val35` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val35 |
| 35 | `rsk62_1_100_val36` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val36 |
| 36 | `rsk62_1_100_val37` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val37 |
| 37 | `rsk62_1_100_val38` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val38 |
| 38 | `rsk62_1_100_val39` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val39 |
| 39 | `rsk62_1_100_val4` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val4 |
| 40 | `rsk62_1_100_val40` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val40 |
| 41 | `rsk62_1_100_val41` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val41 |
| 42 | `rsk62_1_100_val42` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val42 |
| 43 | `rsk62_1_100_val43` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val43 |
| 44 | `rsk62_1_100_val44` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val44 |
| 45 | `rsk62_1_100_val45` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val45 |
| 46 | `rsk62_1_100_val46` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val46 |
| 47 | `rsk62_1_100_val47` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val47 |
| 48 | `rsk62_1_100_val48` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val48 |
| 49 | `rsk62_1_100_val49` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val49 |
| 50 | `rsk62_1_100_val5` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val5 |
| 51 | `rsk62_1_100_val50` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val50 |
| 52 | `rsk62_1_100_val51` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val51 |
| 53 | `rsk62_1_100_val52` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val52 |
| 54 | `rsk62_1_100_val53` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val53 |
| 55 | `rsk62_1_100_val54` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val54 |
| 56 | `rsk62_1_100_val55` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val55 |
| 57 | `rsk62_1_100_val56` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val56 |
| 58 | `rsk62_1_100_val57` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val57 |
| 59 | `rsk62_1_100_val58` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val58 |
| 60 | `rsk62_1_100_val59` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val59 |
| 61 | `rsk62_1_100_val6` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val6 |
| 62 | `rsk62_1_100_val60` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val60 |
| 63 | `rsk62_1_100_val61` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val61 |
| 64 | `rsk62_1_100_val62` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val62 |
| 65 | `rsk62_1_100_val63` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val63 |
| 66 | `rsk62_1_100_val64` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val64 |
| 67 | `rsk62_1_100_val65` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val65 |
| 68 | `rsk62_1_100_val66` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val66 |
| 69 | `rsk62_1_100_val67` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val67 |
| 70 | `rsk62_1_100_val68` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val68 |
| 71 | `rsk62_1_100_val69` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val69 |
| 72 | `rsk62_1_100_val7` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val7 |
| 73 | `rsk62_1_100_val70` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val70 |
| 74 | `rsk62_1_100_val71` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val71 |
| 75 | `rsk62_1_100_val72` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val72 |
| 76 | `rsk62_1_100_val73` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val73 |
| 77 | `rsk62_1_100_val74` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val74 |
| 78 | `rsk62_1_100_val75` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val75 |
| 79 | `rsk62_1_100_val76` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val76 |
| 80 | `rsk62_1_100_val77` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val77 |
| 81 | `rsk62_1_100_val78` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val78 |
| 82 | `rsk62_1_100_val79` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val79 |
| 83 | `rsk62_1_100_val8` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val8 |
| 84 | `rsk62_1_100_val80` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val80 |
| 85 | `rsk62_1_100_val81` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val81 |
| 86 | `rsk62_1_100_val82` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val82 |
| 87 | `rsk62_1_100_val83` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val83 |
| 88 | `rsk62_1_100_val84` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val84 |
| 89 | `rsk62_1_100_val85` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val85 |
| 90 | `rsk62_1_100_val86` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val86 |
| 91 | `rsk62_1_100_val87` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val87 |
| 92 | `rsk62_1_100_val88` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val88 |
| 93 | `rsk62_1_100_val89` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val89 |
| 94 | `rsk62_1_100_val9` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val9 |
| 95 | `rsk62_1_100_val90` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val90 |
| 96 | `rsk62_1_100_val91` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val91 |
| 97 | `rsk62_1_100_val92` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val92 |
| 98 | `rsk62_1_100_val93` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val93 |
| 99 | `rsk62_1_100_val94` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val94 |
| 100 | `rsk62_1_100_val95` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val95 |
| 101 | `rsk62_1_100_val96` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val96 |
| 102 | `rsk62_1_100_val97` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val97 |
| 103 | `rsk62_1_100_val98` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val98 |
| 104 | `rsk62_1_100_val99` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val99 |
| 105 | `rsk62_1_1_100_intercept` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | intercept |
| 106 | `rsk62_1_1_100_val10` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val10 |
| 107 | `rsk62_1_1_100_val100` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val100 |
| 108 | `rsk62_1_1_100_val11` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val11 |
| 109 | `rsk62_1_1_100_val12` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val12 |
| 110 | `rsk62_1_1_100_val13` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val13 |
| 111 | `rsk62_1_1_100_val14` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val14 |
| 112 | `rsk62_1_1_100_val15` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val15 |
| 113 | `rsk62_1_1_100_val16` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val16 |
| 114 | `rsk62_1_1_100_val17` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val17 |
| 115 | `rsk62_1_1_100_val18` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val18 |
| 116 | `rsk62_1_1_100_val19` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val19 |
| 117 | `rsk62_1_1_100_val20` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val20 |
| 118 | `rsk62_1_1_100_val21` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val21 |
| 119 | `rsk62_1_1_100_val22` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val22 |
| 120 | `rsk62_1_1_100_val23` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val23 |
| 121 | `rsk62_1_1_100_val24` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val24 |
| 122 | `rsk62_1_1_100_val25` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val25 |
| 123 | `rsk62_1_1_100_val26` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val26 |
| 124 | `rsk62_1_1_100_val27` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val27 |
| 125 | `rsk62_1_1_100_val28` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val28 |
| 126 | `rsk62_1_1_100_val29` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val29 |
| 127 | `rsk62_1_1_100_val3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val3 |
| 128 | `rsk62_1_1_100_val30` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val30 |
| 129 | `rsk62_1_1_100_val31` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val31 |
| 130 | `rsk62_1_1_100_val32` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val32 |
| 131 | `rsk62_1_1_100_val33` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val33 |
| 132 | `rsk62_1_1_100_val34` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val34 |
| 133 | `rsk62_1_1_100_val35` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val35 |
| 134 | `rsk62_1_1_100_val36` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val36 |
| 135 | `rsk62_1_1_100_val37` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val37 |
| 136 | `rsk62_1_1_100_val38` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val38 |
| 137 | `rsk62_1_1_100_val39` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val39 |
| 138 | `rsk62_1_1_100_val4` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val4 |
| 139 | `rsk62_1_1_100_val40` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val40 |
| 140 | `rsk62_1_1_100_val41` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val41 |
| 141 | `rsk62_1_1_100_val42` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val42 |
| 142 | `rsk62_1_1_100_val43` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val43 |
| 143 | `rsk62_1_1_100_val44` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val44 |
| 144 | `rsk62_1_1_100_val45` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val45 |
| 145 | `rsk62_1_1_100_val46` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val46 |
| 146 | `rsk62_1_1_100_val47` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val47 |
| 147 | `rsk62_1_1_100_val48` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val48 |
| 148 | `rsk62_1_1_100_val49` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val49 |
| 149 | `rsk62_1_1_100_val5` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val5 |
| 150 | `rsk62_1_1_100_val50` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val50 |
| 151 | `rsk62_1_1_100_val51` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val51 |
| 152 | `rsk62_1_1_100_val52` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val52 |
| 153 | `rsk62_1_1_100_val53` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val53 |
| 154 | `rsk62_1_1_100_val54` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val54 |
| 155 | `rsk62_1_1_100_val55` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val55 |
| 156 | `rsk62_1_1_100_val56` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val56 |
| 157 | `rsk62_1_1_100_val57` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val57 |
| 158 | `rsk62_1_1_100_val58` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val58 |
| 159 | `rsk62_1_1_100_val59` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val59 |
| 160 | `rsk62_1_1_100_val6` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val6 |
| 161 | `rsk62_1_1_100_val60` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val60 |
| 162 | `rsk62_1_1_100_val61` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val61 |
| 163 | `rsk62_1_1_100_val62` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val62 |
| 164 | `rsk62_1_1_100_val63` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val63 |
| 165 | `rsk62_1_1_100_val64` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val64 |
| 166 | `rsk62_1_1_100_val65` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val65 |
| 167 | `rsk62_1_1_100_val66` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val66 |
| 168 | `rsk62_1_1_100_val67` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val67 |
| 169 | `rsk62_1_1_100_val68` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val68 |
| 170 | `rsk62_1_1_100_val69` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val69 |
| 171 | `rsk62_1_1_100_val7` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val7 |
| 172 | `rsk62_1_1_100_val70` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val70 |
| 173 | `rsk62_1_1_100_val71` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val71 |
| 174 | `rsk62_1_1_100_val72` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val72 |
| 175 | `rsk62_1_1_100_val73` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val73 |
| 176 | `rsk62_1_1_100_val74` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val74 |
| 177 | `rsk62_1_1_100_val75` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val75 |
| 178 | `rsk62_1_1_100_val76` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val76 |
| 179 | `rsk62_1_1_100_val77` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val77 |
| 180 | `rsk62_1_1_100_val78` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val78 |
| 181 | `rsk62_1_1_100_val79` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val79 |
| 182 | `rsk62_1_1_100_val8` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val8 |
| 183 | `rsk62_1_1_100_val80` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val80 |
| 184 | `rsk62_1_1_100_val81` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val81 |
| 185 | `rsk62_1_1_100_val82` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val82 |
| 186 | `rsk62_1_1_100_val83` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val83 |
| 187 | `rsk62_1_1_100_val84` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val84 |
| 188 | `rsk62_1_1_100_val85` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val85 |
| 189 | `rsk62_1_1_100_val86` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val86 |
| 190 | `rsk62_1_1_100_val87` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val87 |
| 191 | `rsk62_1_1_100_val88` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val88 |
| 192 | `rsk62_1_1_100_val89` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val89 |
| 193 | `rsk62_1_1_100_val9` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val9 |
| 194 | `rsk62_1_1_100_val90` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val90 |
| 195 | `rsk62_1_1_100_val91` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val91 |
| 196 | `rsk62_1_1_100_val92` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val92 |
| 197 | `rsk62_1_1_100_val93` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val93 |
| 198 | `rsk62_1_1_100_val94` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val94 |
| 199 | `rsk62_1_1_100_val95` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val95 |
| 200 | `rsk62_1_1_100_val96` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val96 |
| 201 | `rsk62_1_1_100_val97` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val97 |
| 202 | `rsk62_1_1_100_val98` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val98 |
| 203 | `rsk62_1_1_100_val99` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val99 |
| 204 | `rsk62_beta1_1_100_growth` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | growth |
| 205 | `rsk62_beta1_1_100_logadv20` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | logadv20 |
| 206 | `rsk62_beta1_1_100_logcap` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | logcap |
| 207 | `rsk62_beta1_1_100_mts` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | stm |
| 208 | `rsk62_beta1_1_100_pb` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | bp |
| 209 | `rsk62_beta1_1_100_qe2d` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | d2eq |
| 210 | `rsk62_beta1_1_100_spe` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | eps |
| 211 | `rsk62_beta1_1_100_volatility` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | volatility |
| 212 | `rsk62_beta_1_100_averagereturn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | averageReturn |
| 213 | `rsk62_beta_1_100_growth` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Regression beta coefficient for the Earnings Growth style factor, estimated over a 100-day window using 1-day forward returns |
| 214 | `rsk62_beta_1_100_logadv20` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Regression beta coefficient for the log of 20-day average dollar volume (liquidity) style factor, estimated over a 100-day window using 1-da |
| 215 | `rsk62_beta_1_100_logcap` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Regression beta coefficient for the log of market capitalization (size) style factor, estimated over a 100-day window using 1-day forward re |
| 216 | `rsk62_beta_1_100_mtl` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | ltm |
| 217 | `rsk62_beta_1_100_pb` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Regression beta coefficient for the Book-to-Price style factor, estimated over a 100-day window using 1-day forward returns |
| 218 | `rsk62_beta_1_100_spe` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Regression beta (loading) on the earnings‑per‑share style factor (earnings yield proxy) for the stock, estimated with a 1‑day horizon over a |
| 219 | `rsk62_retseries1_1_100_val1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val1 |
| 220 | `rsk62_retseries1_1_100_val2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val2 |
| 221 | `rsk62_retseries_1_100_val1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val1 |
| 222 | `rsk62_retseries_1_100_val2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Val2 |
| 223 | `rsk62_return` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking asset return at a 1-day horizon for each stock, used in the risk model regressions (units: return per period) |
| 224 | `rsk62_1_100_ksrs` | MATRIX | 0.987 | 风险与质量 | 0 | — | — | — | UNTESTED | Stock-specific idiosyncratic risk (specific risk) per stock in the USA model, for the 1-day horizon using a 100-day rolling window; reported |
| 225 | `rsk62_1_1_100_ksrs` | MATRIX | 0.987 | 风险与质量 | 0 | — | — | — | UNTESTED | specific risks of stocks |
| 226 | `rsk62_risk_growth` | MATRIX | 0.935 | 风险与质量 | 0 | — | — | — | UNTESTED | growth |
| 227 | `rsk62_risk_logadv20` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Log of 20-day average dollar trading volume (ADV), normalized exposure |
| 228 | `rsk62_risk_logcap` | MATRIX | 0.935 | 风险与质量 | 0 | — | — | — | UNTESTED | Style factor exposure: natural log of market capitalization |
| 229 | `rsk62_risk_mtl` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Style factor exposure: long-term momentum in stock returns, cross-section normalized |
| 230 | `rsk62_risk_pb` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Style factor exposure: book-to-price ratio (value) |
| 231 | `rsk62_risk_qe2d` | MATRIX | 0.935 | 风险与质量 | 0 | — | — | — | UNTESTED | d2eq |
| 232 | `rsk62_risk_spe` | MATRIX | 0.935 | 风险与质量 | 0 | — | — | — | UNTESTED | eps |
| 233 | `rsk62_risk_volatility` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Recent stock return volatility (e.g., standard deviation), normalized exposure |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **8** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `blbYd0XK` | 0.23 | 0.06 | — | — | 0.05 | 0 | 191 | `group_rank(rsk62_risk_mts, subindustry)` |
| `ZYbRKV6x` | 0.19 | 0.04 | — | — | 0.16 | 0 | 191 | `rank(rsk62_1_100_val19)` |
| `d5b2RJpX` | 0.14 | 0.03 | — | — | 0.10 | 0 | 191 | `ts_zscore(rsk62_beta_1_100_volatility, 22)` |
| `A1NR7XWR` | 0.13 | 0.02 | — | — | 0.18 | 0 | 191 | `rank(ts_delta(rsk62_1_100_val21, 5))` |
| `58zZkKxk` | 0.03 | 0.00 | — | — | 0.16 | 0 | 191 | `ts_zscore(rsk62_1_100_val24, 22)` |
| `N1aXRE0e` | -0.05 | -0.01 | — | — | 0.06 | 0 | 191 | `rank(rsk62_beta_1_100_qe2d)` |
| `O0N1xdYv` | -0.10 | -0.02 | — | — | 0.08 | 0 | 191 | `ts_zscore(rsk62_beta1_1_100_mtl, 66)` |
| `E5pZenOL` | -0.25 | -0.06 | — | — | 0.06 | 0 | 191 | `rank(rsk62_beta_1_100_mts)` |

## 七、判死记录（sealed dead_end）

- `EUR-RISK72-RESIDUAL-RETURN-WEAK`（2026-09-23T18:17:24）family=risk72 equity_residualized_return 残差族（cfg2/ecs/ats × top1200/top2500 残差价差）：{"family": "risk72 equity_residualized_return 残差族（cfg2/ecs/ats × top1200/top2500 残差价差）", "reason": "wave230 8 探针全灭：best sharpe 0.91 / fitness 0.48，2Y 1.65 但 LOW_ROBUST_UNIVERSE_SHARPE；未达 Mode B 资格线 1.25（D4）→ 判死。2 条 group_cartesian_product/group_count 单位错误被自动隔离。RISK 塔剩余候选：risk68(fields=5 仅条件腿)/risk62(crowded 10665) 均不进白名单。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "s

