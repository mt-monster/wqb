# IND 全 dataset 扫描（按 category）· 2026-11-14

> 战役产物 → `output_report/`。MCP `get_datasets(IND,TOP500,D1)` 实读 **141 集**；DB `dataset_profile` **144 集**；塔状态 = MCP `get_pyramid_alphas()` 当季实读。

## 1. 当季塔实读（唯一权威，季度清零）

| 塔 | 计数 | 状态 | 塔 | 计数 | 状态 |
|---|---:|---|---|---:|---|
| analyst | 3 | 已亮 | earnings | 2 | 未亮 |
| fundamental | 3 | 已亮 | imbalance | 0 | 未亮 |
| insiders | 1 | 未亮 | institutions | 1 | 未亮 |
| macro | 2 | 未亮 | model | 3 | 已亮 |
| news | 4 | 已亮 | option | 0 | 未亮 |
| other | 4 | 已亮 | pv | 11 | 已亮 |
| risk | 3 | 已亮 | sentiment | 1 | 未亮 |
| shortinterest | 0 | 未亮 |  | |  |

与 11-05（已亮 10 座）及 11-06（未亮仅 3 座）快照均不同；按铁律只认当季 ≥3，以本次实读为准。

## 2. 判定分布

| state | 集数 | prio | 集数 |
|---|---:|---|---:|
| ELIGIBLE | 58 | P0 | 4 |
| EXCLUDED_OCCUPIED | 44 | P1 | 0 |
| EXCLUDED_HARD | 14 | P2 | 4 |
| CONDITIONAL_ONLY | 28 | P3 | 50 |

覆盖主门 = **0.49**（由 0.5 动态下调，仅覆盖 `earnings11` 0.4992，强制在线补判）。

## 3. 逐 category 全量明细


### ANALYST（13 集，ALIVE 字段合计 7）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| analyst_consensus | 0.761 | 2351 | 7 | 3.25 | 3.58 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录 |
| analyst11 | 0.552 | 210 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.5520 ok / 210 fields / 0 ALIVE / 0 DEAD / 塔 analyst=3 (已亮) |
| analyst39 | 0.8445 | 35 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8445 ok / 35 fields / 0 ALIVE / 0 DEAD / 塔 analyst=3 (已亮) |
| analyst4 | 0.7819 | 247 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录 |
| analyst44 | 0.8343 | 546 | 0 | 1.41 | 2.11 | 3 | ELIGIBLE | P3 | cov=0.8343 ok / 546 fields / 0 ALIVE / 10 DEAD / 塔 analyst=3 (已亮) |
| analyst45 | 0.8588 | 241 | 0 | 1.5 | 1.41 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-ANALYST45-ROBUST-WALL（禁复用该机制，整集可用但须换机制） |
| analyst46 | 0.585 | 6 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.5850 ok / 6 fields / 0 ALIVE / 0 DEAD / 塔 analyst=3 (已亮) |
| analyst48 | 0.3675 | 72 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | avg_field_coverage=0.3675 <0.49（动态门），需在线补判 |
| analyst81 | 0.265 | 5 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | avg_field_coverage=0.2650 <0.49（动态门），需在线补判 |
| analyst83 | 0.287 | 384 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | avg_field_coverage=0.2870 <0.49（动态门），需在线补判 |
| analyst9 | 0.7158 | 46 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录 |
| analyst_base_ref | 0.8069 | 14 | 0 | 0.6 | 1.99 | 3 | ELIGIBLE | P3 | cov=0.8069 ok / 14 fields / 0 ALIVE / 5 DEAD / 塔 analyst=3 (已亮)；族级判死 IND-MODEL170-VALUATION-DEAD, IND-ANALYSTBASE-SUE-DEAD（禁复 |
| analyst_factor_signals | 0.6109 | 58 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.6109 ok / 58 fields / 0 ALIVE / 0 DEAD / 塔 analyst=3 (已亮) |

### EARNINGS（3 集，ALIVE 字段合计 2）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| earnings3 | 0.7906 | 8 | 2 | 4.49 | 1.48 | 2 | ELIGIBLE | P0 | cov=0.7906 ok / 8 fields / 2 ALIVE / 6 DEAD / 塔 earnings=2 (未亮)；族级判死 IND-EARNINGS3-CALENDAR-DEAD, earnings3, IND-EARNINGS3-TI |
| earnings11 | 0.4992 | 35 | 0 | 0.51 | 0.19 | 2 | ELIGIBLE | P2 | cov=0.4992 ok / 35 fields / 0 ALIVE / 7 DEAD / 塔 earnings=2 (未亮)；覆盖主门由 0.5 动态下调至 0.49（用户授权），强制在线 longCount/shortCount 补判 + 近十 |
| earnings6 | 0.3567 | 20 | 0 | - | - | 2 | CONDITIONAL_ONLY | - | avg_field_coverage=0.3567 <0.49（动态门），需在线补判 |

### FUNDAMENTAL（12 集，ALIVE 字段合计 0）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| fundamental1 | 0.5626 | 118 | 0 | - | - | 3 | EXCLUDED_HARD | - | STRUCT: 118 字段全 UNUSABLE，治理/薪酬族判死；族级判死 IND-FUNDAMENTAL1-GOVERNANCE-SPARSE, IND-FND90-EARNINGS-QUALITY-DEAD（禁复用该机制，整集可用但须换机制） |
| fundamental17 | 0.8661 | 350 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8661 ok / 350 fields / 0 ALIVE / 0 DEAD / 塔 fundamental=3 (已亮)；族级判死 IND-FND17-ANNUAL-DEAD, IND-FND23-ANNUAL-BS-DEAD（禁复用 |
| fundamental22 | 0.395 | 2 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=2 <5（dataset_health 阶段①） |
| fundamental23 | 0.8947 | 39 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8947 ok / 39 fields / 0 ALIVE / 0 DEAD / 塔 fundamental=3 (已亮)；族级判死 IND-FND23-ANNUAL-BS-DEAD（禁复用该机制，整集可用但须换机制） |
| fundamental25 | 0.2984 | 6 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | avg_field_coverage=0.2984 <0.49（动态门），需在线补判 |
| fundamental4 | 0.3737 | 1 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=1 <5（dataset_health 阶段①） |
| fundamental44 | 0.7842 | 12 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7842 ok / 12 fields / 0 ALIVE / 0 DEAD / 塔 fundamental=3 (已亮)；族级判死 IND-FND90-EARNINGS-QUALITY-DEAD, IND-MODEL192-CDS-DE |
| fundamental86 | 0.8001 | 7 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 fundamental(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-CROSS-DS-EARNINGS-DEAD（禁复用该机制，整集可用但须换机制） |
| fundamental89 | 0.4524 | 195 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 fundamental(3) 且 expressions/backtest_results 有该集真实回测记录 |
| fundamental90 | 0.7209 | 65 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7209 ok / 65 fields / 0 ALIVE / 0 DEAD / 塔 fundamental=3 (已亮)；族级判死 IND-FND90-EARNINGS-QUALITY-DEAD, IND-FND44-ACCOUNTIN |
| fundamental93 | 0.5362 | 32 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.5362 ok / 32 fields / 0 ALIVE / 0 DEAD / 塔 fundamental=3 (已亮) |
| fundamental94 | 0.9258 | 38 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 fundamental(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-CROSS-DS-VOLATILITY-DEAD, IND-CROSS-DS-EARNING |

### IMBALANCE（1 集，ALIVE 字段合计 2）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| imbalance5 | 0.7876 | 2 | 2 | 2.81 | - | 0 | EXCLUDED_HARD | - | STRUCT: 字段级 prod 饱和（imb5_score 0.939）+ 仅 2 字段 <5 硬门 |

### INSIDERS（2 集，ALIVE 字段合计 0）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| insiders1 | 0.3877 | 9 | 0 | 0.92 | 1.16 | 1 | EXCLUDED_HARD | - | STRUCT: maxS 0.95 + cov 0.3877 稀疏，整集判死；族级判死 IND-INSIDERS1-NODIRECTION-DEAD, insiders1（禁复用该机制，整集可用但须换机制） |
| insiders5 | 0.9991 | 1 | 0 | - | - | 1 | CONDITIONAL_ONLY | - | fieldCount=1 <5（dataset_health 阶段①） |

### INSTITUTIONS（1 集，ALIVE 字段合计 11）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| institutions6 | 0.992 | 11 | 11 | 3.45 | 3.29 | 1 | ELIGIBLE | P0 | cov=0.9920 ok / 11 fields / 11 ALIVE / 0 DEAD / 塔 institutions=1 (未亮)；族级判死 IND-INSTITUTIONS6-NETBUY-WEAK, IND-W149-INST6-NETB |

### MACRO（1 集，ALIVE 字段合计 1）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| macro63 | 0.9968 | 1 | 1 | 2.9 | - | 2 | EXCLUDED_HARD | - | STRUCT: IND 侧全域恒 0（dateCreated 2025-10-01），仅作 add-zero 挂塔器；1 字段 <5 |

### MODEL（43 集，ALIVE 字段合计 20）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| model135 | 0.7855 | 137 | 13 | 3.6 | 3.31 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MDL135-PROD-WALL-FINAL（禁复用该机制，整集可用但须换机制） |
| model32 | 0.9696 | 36 | 4 | 3.31 | 1.98 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| model144 | 0.8301 | 2 | 1 | 1.59 | 2.46 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| model238 | 0.9827 | 44 | 1 | 2.59 | -0.3 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MODEL238-PROD-SATURATED（禁复用该机制，整集可用但须换机制） |
| model252 | 0.7854 | 5 | 1 | 2.37 | 3.11 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| ai_factor_transfer | 0.9684 | 20 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| analyst_earnings_ibes | 0.9965 | 28 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.9965 ok / 28 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| analyst_revision_horizons | 0.7819 | 1026 | 0 | 2.64 | 3.08 | 3 | ELIGIBLE | P3 | cov=0.7819 ok / 1026 fields / 0 ALIVE / 2 DEAD / 塔 model=3 (已亮) |
| behavioral_signals | 0.8336 | 7 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-IPVF-MICROSTRUCTURE-DEAD（禁复用该机制，整集可用但须换机制） |
| global_seasonal_model | 0.996 | 8 | 0 | 1.16 | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-NEWS29-SPARSE-EVENT（禁复用该机制，整集可用但须换机制） |
| model106 | 0.4953 | 14 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.4953 ok / 14 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮)；覆盖主门由 0.5 动态下调至 0.49（用户授权），强制在线 longCount/shortCount 补判 + 近十年 |
| model110 | 0.7885 | 8 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7885 ok / 8 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model138 | 0.8327 | 120 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-FND23-ANNUAL-BS-DEAD, IND-MDL138-DEVIATION-ROBUST-WA |
| model139 | 0.7873 | 2 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=2 <5（dataset_health 阶段①） |
| model140 | 0.7463 | 3 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=3 <5（dataset_health 阶段①） |
| model141 | 0.1954 | 2 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=2 <5（dataset_health 阶段①） |
| model16 | 1.0 | 8 | 0 | 0.86 | 0.7 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| model170 | 0.7427 | 11 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MODEL170-VALUATION-DEAD（禁复用该机制，整集可用但须换机制） |
| model176 | 0.3977 | 84 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | avg_field_coverage=0.3977 <0.49（动态门），需在线补判 |
| model192 | 1.0 | 101 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MODEL192-CDS-DEAD, IND-FND44-ACCOUNTING-QUALITY-DEAD |
| model207 | 0.6713 | 3 | 0 | 1.4 | 1.7 | 3 | CONDITIONAL_ONLY | - | fieldCount=3 <5（dataset_health 阶段①）；族级判死 IND-MODEL-SCORE-DEAD（禁复用该机制，整集可用但须换机制） |
| model216 | 0.8223 | 88 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8223 ok / 88 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮)；族级判死 IND-REVMAG-ANALYST-SATURATED, IND-MODEL216-ROBUST-WALL, IN |
| model243 | 0.9338 | 4 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=4 <5（dataset_health 阶段①） |
| model244 | 0.4702 | 30 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | avg_field_coverage=0.4702 <0.49（动态门），需在线补判 |
| model250 | 0.7876 | 20 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7876 ok / 20 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model253 | 0.4882 | 2 | 0 | - | - | 3 | CONDITIONAL_ONLY | - | fieldCount=2 <5（dataset_health 阶段①） |
| model26 | 0.7601 | 667 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7601 ok / 667 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model262 | 0.9009 | 25 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.9009 ok / 25 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮)；族级判死 IND-MDL262-IMPLIED-VALUATION-DEAD（禁复用该机制，整集可用但须换机制） |
| model28 | 0.9699 | 114 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-CROSS-DS-VOLATILITY-DEAD, IND-FND94-THIRD-LEG-DEAD（禁 |
| model29 | 0.7187 | 91 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7187 ok / 91 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮)；族级判死 IND-EBITDA-SURPRISE-ROBUST-WALL（禁复用该机制，整集可用但须换机制） |
| model30 | 0.7677 | 49 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7677 ok / 49 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model31 | 0.8303 | 132 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8303 ok / 132 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model313 | 0.6749 | 3 | 0 | 0.38 | 1.6 | 3 | CONDITIONAL_ONLY | - | fieldCount=3 <5（dataset_health 阶段①）；族级判死 IND-MODEL-SCORE-DEAD（禁复用该机制，整集可用但须换机制） |
| model33 | 0.7851 | 32 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.7851 ok / 32 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model36 | 0.9801 | 42 | 0 | 1.38 | 2.04 | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| model37 | 0.9288 | 85 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.9288 ok / 85 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model38 | 0.865 | 71 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8650 ok / 71 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| model39 | 0.9734 | 14 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| model50 | 0.619 | 58 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录 |
| model68 | 0.782 | 4 | 0 | 1.09 | 0.7 | 3 | CONDITIONAL_ONLY | - | fieldCount=4 <5（dataset_health 阶段①） |
| model77 | 0.8495 | 348 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.8495 ok / 348 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮) |
| predictive_starmine | 0.925 | 638 | 0 | - | - | 3 | ELIGIBLE | P3 | cov=0.9250 ok / 638 fields / 0 ALIVE / 0 DEAD / 塔 model=3 (已亮)；族级判死 IND-STARMINE-VALUATION-DEAD, IND-PREDICTED-SURPRISE-ROBUS |
| quant_factor_lib | 0.8335 | 32 | 0 | - | - | 3 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-QFL-CREDIT-FAMILY-DEAD（禁复用该机制，整集可用但须换机制） |

### NEWS（22 集，ALIVE 字段合计 2）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| news85 | 0.876 | 23 | 2 | 3.47 | 0.15 | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 news(4) 且 expressions/backtest_results 有该集真实回测记录 |
| news104 | 0.7348 | 11 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.7348 ok / 11 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news17 | 0.6974 | 24 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6974 ok / 24 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news20 | 0.876 | 15 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.8760 ok / 15 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news21 | 0.2983 | 36 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | avg_field_coverage=0.2983 <0.49（动态门），需在线补判 |
| news23 | 0.4594 | 93 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | avg_field_coverage=0.4594 <0.49（动态门），需在线补判 |
| news29 | 0.9724 | 12 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.9724 ok / 12 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮)；族级判死 IND-NEWS29-SPARSE-EVENT, IND-AINEWS-SENTIMENT-DEAD, IND-SNT |
| news3 | 0.6461 | 19 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6461 ok / 19 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news31 | 0.9681 | 25 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.9681 ok / 25 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news36 | 0.7031 | 43 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.7031 ok / 43 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news38 | 0.8801 | 44 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.8801 ok / 44 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news46 | 0.8996 | 44 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.8996 ok / 44 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news48 | 0.6908 | 22 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6908 ok / 22 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news50 | 0.8706 | 69 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.8706 ok / 69 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news52 | 0.291 | 24 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | avg_field_coverage=0.2910 <0.49（动态门），需在线补判 |
| news54 | 0.9073 | 40 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.9073 ok / 40 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news59 | 0.9783 | 2 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | fieldCount=2 <5（dataset_health 阶段①） |
| news7 | 0.8499 | 33 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.8499 ok / 33 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news73 | 0.665 | 22 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6650 ok / 22 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news76 | 0.9909 | 6 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.9909 ok / 6 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |
| news79 | 0.9776 | 34 | 0 | 1.02 | 1.65 | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 news(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-NEWS29-SPARSE-EVENT, IND-AINEWS-SENTIMENT-DEAD（禁复用该机制 |
| news84 | 0.6974 | 23 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6974 ok / 23 fields / 0 ALIVE / 0 DEAD / 塔 news=4 (已亮) |

### OPTION（2 集，ALIVE 字段合计 1）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| option30 | 0.3629 | 12 | 1 | 1.94 | 2.5 | 0 | EXCLUDED_HARD | - | STRUCT: fitness ceiling ~0.85 结构性，cov 0.3629；族级判死 IND-OPTION30-OS-SURPRISE-FITNESS-CEILING（禁复用该机制，整集可用但须换机制） |
| option1 | 0.4045 | 28 | 0 | 1.18 | 1.22 | 0 | EXCLUDED_HARD | - | STRUCT: IV 残差 decay/TO 硬互斥 + 近十年数据缺口 |

### OTHER（21 集，ALIVE 字段合计 0）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| acquisition_model | 0.965 | 15 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-ACQMODEL-WEAK-NEG（禁复用该机制，整集可用但须换机制） |
| ai_news_scores | 0.693 | 105 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-AINEWS-SENTIMENT-DEAD, IND-SNT23-SENTIMENT-DEAD, IND |
| event_relation | 0.4236 | 3 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录 |
| ml_factor_proj | 1.0 | 333 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-TOP500-CEILING（禁复用该机制，整集可用但须换机制） |
| mmp_nlp_sentiment | 0.9593 | 521 | 0 | - | - | 4 | EXCLUDED_HARD | - | STRUCT: 平台 unknown variable，IND/TOP500 不可用；族级判死 IND-MMPNLP-UNAVAILABLE（禁复用该机制，整集可用但须换机制） |
| news_sentiment_nlp | 0.6715 | 23 | 0 | 0.33 | 1.32 | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-AI-NEWS-DEAD（禁复用该机制，整集可用但须换机制） |
| other128 | 0.742 | 14 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER128-MANAGEMENT-QUALITY-DEAD（禁复用该机制，整集可用但须换机制） |
| other296 | 0.3488 | 19 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | avg_field_coverage=0.3488 <0.49（动态门），需在线补判 |
| other315 | 0.7256 | 32 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER315-SPARSE-DEAD（禁复用该机制，整集可用但须换机制） |
| other323 | 0.9996 | 11 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.9996 ok / 11 fields / 0 ALIVE / 0 DEAD / 塔 other=4 (已亮) |
| other327 | 0.7583 | 3 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录 |
| other335 | 0.6364 | 10 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6364 ok / 10 fields / 0 ALIVE / 0 DEAD / 塔 other=4 (已亮) |
| other384 | 0.2974 | 33 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | avg_field_coverage=0.2974 <0.49（动态门），需在线补判 |
| other424 | 0.6592 | 3 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录 |
| other436 | 0.6363 | 3 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录 |
| other532 | 0.9856 | 8 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录 |
| other545 | 0.8158 | 4 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER545-NEMO-DEAD（禁复用该机制，整集可用但须换机制） |
| other567 | 0.6338 | 37 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER567-EMPLOYEE-SCORE-DEAD, IND-OTHER567-DEAD（禁复用该 |
| other571 | 0.4399 | 30 | 0 | - | - | 4 | CONDITIONAL_ONLY | - | avg_field_coverage=0.4399 <0.49（动态门），需在线补判 |
| other635 | 0.627 | 6 | 0 | - | - | 4 | ELIGIBLE | P3 | cov=0.6270 ok / 6 fields / 0 ALIVE / 0 DEAD / 塔 other=4 (已亮) |
| other696 | 0.4138 | 220 | 0 | - | - | 4 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录 |

### PV（13 集，ALIVE 字段合计 8）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| intraday_pv_feats | 0.9835 | 582 | 6 | 6.48 | 3.25 | 11 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-IPVF-MICROSTRUCTURE-DEAD, IND-INTRADAYPV-PRICEVOLUME-C |
| pv103 | 1.0 | 7 | 2 | 4.04 | 3.13 | 11 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-PV103-PV47-ROBUST-DEAD-WALL, IND-PV103-LASTHOUR-REVERS |
| pv1 | 1.0 | 24 | 0 | - | - | 11 | ELIGIBLE | P3 | cov=1.0000 ok / 24 fields / 0 ALIVE / 0 DEAD / 塔 pv=11 (已亮) |
| pv106 | 0.9941 | 23 | 0 | 0.82 | 2.41 | 11 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-TOP500-CEILING, IND-MDL138-DEVIATION-ROBUST-WALL, IND- |
| pv109 | 0.3393 | 25 | 0 | - | - | 11 | CONDITIONAL_ONLY | - | avg_field_coverage=0.3393 <0.49（动态门），需在线补判 |
| pv13 | 0.6681 | 37 | 0 | - | - | 11 | ELIGIBLE | P3 | cov=0.6681 ok / 37 fields / 0 ALIVE / 0 DEAD / 塔 pv=11 (已亮) |
| pv14 | 0.9487 | 2 | 0 | - | - | 11 | CONDITIONAL_ONLY | - | fieldCount=2 <5（dataset_health 阶段①） |
| pv149 | 1.0 | 1 | 0 | - | - | 11 | CONDITIONAL_ONLY | - | fieldCount=1 <5（dataset_health 阶段①） |
| pv29 | 0.7099 | 30 | 0 | - | - | 11 | ELIGIBLE | P3 | cov=0.7099 ok / 30 fields / 0 ALIVE / 0 DEAD / 塔 pv=11 (已亮) |
| pv30 | 0.9805 | 675 | 0 | - | - | 11 | ELIGIBLE | P3 | cov=0.9805 ok / 675 fields / 0 ALIVE / 0 DEAD / 塔 pv=11 (已亮) |
| pv47 | 0.9997 | 3 | 0 | - | - | 11 | EXCLUDED_OCCUPIED | - | OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-PV103-PV47-ROBUST-DEAD-WALL（禁复用该机制，整集可用但须换机制） |
| pv70 | 1.0 | 33 | 0 | - | - | 11 | EXCLUDED_HARD | - | STRUCT: 区域错配：APAC ex-Japan/ex-China 专属，IND/TOP500 8/8 全零持仓；族级判死 IND-PV70-REGION-MISMATCH, IND-PV70-DEAD（禁复用该机制，整集可用但须换机制） |
| univ1 | 1.0 | 1 | 0 | - | - | 11 | EXCLUDED_HARD | - | STRUCT: coverage=0 且 1 字段，无信号面 |

### RISK（4 集，ALIVE 字段合计 3）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| risk68 | 0.9786 | 5 | 1 | 2.26 | 1.29 | 3 | EXCLUDED_HARD | - | STRUCT: catalog_unreachable_categories.risk 结构性不可达 |
| risk71 | 0.7046 | 4 | 1 | 3.52 | 2.84 | 3 | EXCLUDED_HARD | - | STRUCT: catalog_unreachable_categories.risk 结构性不可达 |
| risk88 | 1.0 | 1 | 1 | 3.26 | 2.56 | 3 | EXCLUDED_HARD | - | STRUCT: catalog_unreachable_categories.risk 结构性不可达 |
| risk70 | 1.0 | 35 | 0 | - | - | 3 | EXCLUDED_HARD | - | STRUCT: catalog_unreachable_categories.risk 结构性不可达；族级判死 IND-RISK70-NO-SIGNAL（禁复用该机制，整集可用但须换机制） |

### SENTIMENT（4 集，ALIVE 字段合计 4）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| sentiment21 | 0.9681 | 105 | 4 | 3.01 | 2.07 | 1 | ELIGIBLE | P0 | cov=0.9681 ok / 105 fields / 4 ALIVE / 2 DEAD / 塔 sentiment=1 (未亮)；族级判死 IND-MMPNLP-UNAVAILABLE, IND-NEWS85-DNN-SENTIMENT-DEAD |
| news_sentiment_transfer | 0.9368 | 23 | 0 | 1.05 | 1.12 | 1 | ELIGIBLE | P2 | cov=0.9368 ok / 23 fields / 0 ALIVE / 13 DEAD / 塔 sentiment=1 (未亮)；族级判死 IND-AI-NEWS-DEAD, IND-NEWS85-DNN-SENTIMENT-DEAD（禁复用该机 |
| sentiment23 | 0.7028 | 105 | 0 | - | - | 1 | ELIGIBLE | P2 | cov=0.7028 ok / 105 fields / 0 ALIVE / 0 DEAD / 塔 sentiment=1 (未亮)；族级判死 IND-SNT23-SENTIMENT-DEAD（禁复用该机制，整集可用但须换机制） |
| sentiment26 | 0.5318 | 18 | 0 | 0.39 | 0.14 | 1 | ELIGIBLE | P2 | cov=0.5318 ok / 18 fields / 0 ALIVE / 5 DEAD / 塔 sentiment=1 (未亮) |

### SHORTINTEREST（1 集，ALIVE 字段合计 0）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| shortinterest5 | 1.0 | 3 | 0 | 0.22 | 0.21 | 0 | EXCLUDED_HARD | - | STRUCT: 价带宽度在 TOP500 近常数，maxS 0.22，7 探针全灭 + 3 字段；族级判死 IND-SHORTINTEREST5-PRICEBAND-DEAD（禁复用该机制，整集可用但须换机制） |

### UNCATEGORIZED（1 集，ALIVE 字段合计 1）

| dataset | cov | 字段 | ALIVE | 最好S | 最好2Y | 塔 | state | prio | 理由 |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| model238_anlrev | 0.7902 | 1070 | 1 | 2.64 | 3.08 | None | ELIGIBLE | P0 | cov=0.7902 ok / 1070 fields / 1 ALIVE / 2 DEAD / 塔 unclassified=n/a (未亮) |

## 4. 对账与差异

- MCP 141 集 / DB `dataset_profile` 144 集 / `ind_dataset_ranking.json` 143 集 / `ind_campaign_summary_20261029.md` 144 集。差异来自平台上下线与 DB 无 category 历史集（`model238_anlrev` 等），不回改历史台账。
- `OCCUPIED` = `expressions` + `backtest_results` 中 `region=IND` 的 dataset 去重，共 **68 集**。⚠ 曾用「报告全文出现过的 dataset 名」构造得 149 集，属误判（报告附录本就列全 144 集），已作废。
- 判死台账：`registry_empirical(IND,dead_end)` 65 条 + `cells.json` 13 类 + `region_kb.json` 9 条 + `ind_priors.json` 12 条；族级判死只标 `FAMILY_LOCKED`，不排除整集。
- 字段全集：`field_profile_full` 按 dataset 统计 ALIVE/DEAD，阶段 B 逐集与 `get_datasets.fieldCount` 对账。

## 5. 复现

```
mcp__wq-brain-http__get_datasets(region="IND", delay=1, universe="TOP500")
mcp__wq-brain-http__get_pyramid_alphas()
mcp__wqb-db__query_dataset_profile(region="IND", min_cov=0.5, sort="best_s_in_dataset", limit=50)
mcp__wqb-db__get_dead_ends(region="IND")
```
