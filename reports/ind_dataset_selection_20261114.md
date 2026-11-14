# IND dataset 候选清单与选定理由 · 2026-11-14

> 人工审计与复盘 → `reports/<主题>_<YYYYMMDD>.md`。机器中间态 `cache/ind_dataset_scan_20261114.json`（144 集逐集判定），全量明细 `output_report/ind_dataset_scan_20261114.md`。

## 0. 结论

- 扫描 **144 集 / 16 category**；`ELIGIBLE 58` / `EXCLUDED_OCCUPIED 44` / `EXCLUDED_HARD 14` / `CONDITIONAL_ONLY 28`。
- 当季已亮 7 座（analyst, fundamental, model, news, other, pv, risk），未亮 8 座；`OCCUPIED` 真实使用记录 68 集。
- **锁定主攻 5 集**：`institutions6` / `sentiment21` / `earnings11` / `model77` / `other323`；备选 `analyst11` / `model176` / `pv30` / `news73` / `other571` / `earnings3`。
- 全程固定 IND/TOP500/D1，不切换；不降闸；不提交。

## 1. 数据集级排除算法（Q1 口径，可复用）

```
输入：D_all=get_datasets(IND,TOP500,D1)；LIT={cat | get_pyramid_alphas()[IND][D1][cat]>=3}
      OCCUPIED=distinct(expressions.dataset ∪ backtest_results.dataset, region=IND)
      DEAD=registry_empirical(dead_end,IND) ∪ cells.json ∪ region_kb.json ∪ ind_priors.json
逐集 d：
  1) d ∈ STRUCT_EXCLUDE（区域错配/平台不可用/恒0/字段<5/整集判死）  -> EXCLUDED_HARD
  2) d.category ∈ LIT 且 d ∈ OCCUPIED                              -> EXCLUDED_OCCUPIED
  3) d.category ∈ LIT 且 d ∉ OCCUPIED                              -> ELIGIBLE，标 lit_category_but_unoccupied
  4) d.category ∉ LIT                                              -> 不受 OCCUPIED 约束，直接进 ELIGIBLE
  5) fieldCount<5 或 avg_field_coverage<COV_MIN(0.49)               -> CONDITIONAL_ONLY（在线补判）
  6) DEAD 命中只标 FAMILY_LOCKED（禁复用该机制），不排除整集
优先级：P0 未亮塔∩ALIVE>0 > P1 有 ALIVE > P2 未亮塔无 ALIVE > P3 其余
```

⚠ **口径修正（重要）**：初版把「6 处历史篮子报告全文中出现的 dataset 名」当 OCCUPIED，得 149 集 → 120 集被误排。根因：`ind_campaign_summary_20261029.md` 附录本就逐条列全 144 集，"出现"≠"用过"。v2 只用 `expressions` / `backtest_results` 的真实回测记录（68 集）。

**族级判死不算整集占用（非放宽）**：依据 `AGENTS.md §7.6` 判死须带 bound，及 10-17 实证——`institutions6` 净买入族判死，但残差化族在同一集 10/10 RA 全过。族级判死记为 `FAMILY_LOCKED` 机制禁令；整集结构性判死才计入占用。

## 2. 主攻集逐集理由

### institutions6（P0）

- 画像：category=INSTITUTIONS，塔当季=1（未亮），cov=0.992，字段=11，ALIVE=11，best S=3.45，best 2Y=3.29，回测=82，RA 全过=37，freq=快照（按库表更新，需实测），valueScore=2.0，state=`ELIGIBLE`，flags=FAMILY_LOCKED:3,UNLIT_TOWER,HAS_ALIVE:11。
- **选定理由**：INSTITUTIONS 塔当季 1（未亮）；11 字段 **全部 ALIVE**、cov 0.992、best S 3.45 / 2Y 3.29、82 次回测 / 37 次 RA 全过。天然「同数据集组 ATOM」。10-17 残差化族在本集 10/10 RA 全过（S 2.65–3.12 / prod 0.59–0.67），是 IND 唯一已证能破 prod 墙的信息维度。按 Q1，未亮塔类别不受 OCCUPIED 约束。
- **禁止复用的族（FAMILY_LOCKED）**：
  - 机构净买入族（ts_mean/ts_zscore 66/126 金额·数量·买家数）：IND-W149-INST6-NETBUY-WEAK-DEAD
  - scale/date 字段作主信号：IND-INSTITUTIONS6-NETBUY-WEAK（7/8 group_cartesian_product ERROR）
- **本次允许的机制方向**：残差化（G1）、同集多字段 ts_corr 共动 / 非净买入分歧度、持股集中度时序形态、事件时钟门控
- **近十年**：阶段 B 基准探针强制 2014–2023 每年 PnL 有数据（`get_alpha_yearly_stats`），未过即换集并写 `output_report/ind_dataset_switch_20261114.md`。

### sentiment21（P0）

- 画像：category=SENTIMENT，塔当季=1（未亮），cov=0.9681，字段=105，ALIVE=4，best S=3.01，best 2Y=2.07，回测=48，RA 全过=0，freq=快照（按库表更新，需实测），valueScore=2.0，state=`ELIGIBLE`，flags=FAMILY_LOCKED:2,UNLIT_TOWER,HAS_ALIVE:4。
- **选定理由**：SENTIMENT 塔当季 1（未亮）；105 字段、4 ALIVE、cov 0.968、best S 3.01 / 2Y 2.07。`snt21_pos_mean` 是日频连续慢变量，符合 IND「连续慢变量 + 经济锚 + TO 适中」三要素前两条。未亮塔不受 OCCUPIED 约束。
- **禁止复用的族（FAMILY_LOCKED）**：
  - 新闻情感水平/中位数/偏度/峰值：IND-NEWS85-DNN-SENTIMENT-DEAD、IND-SNT23-SENTIMENT-DEAD
  - headline-count 冲击（TO 0.95 > IND 0.40 线）：IND-NEWS85-DNN-SENTIMENT-DEAD
- **本次允许的机制方向**：残差化（G1）、长窗非方向性注意力代理、同集多字段分歧度（非情感水平）、ts_backfill 减速
- **近十年**：阶段 B 基准探针强制 2014–2023 每年 PnL 有数据（`get_alpha_yearly_stats`），未过即换集并写 `output_report/ind_dataset_switch_20261114.md`。

### earnings11（P0）

- 画像：category=EARNINGS，塔当季=2（未亮），cov=0.4992，字段=35，ALIVE=0，best S=0.51，best 2Y=0.19，回测=8，RA 全过=0，freq=事件/逐笔型（VECTOR），valueScore=2.0，state=`ELIGIBLE`，flags=COV_DYNAMIC_0_49,FAMILY_LOCKED:1,UNLIT_TOWER。
- **选定理由**：EARNINGS 塔当季 2（未亮，差 1 颗）；35 字段、cov 0.4992。按用户「覆盖率可动态调整」把主门从 0.5 下调至 0.49 纳入，**强制在线补判 longCount/shortCount + 近十年 PnL**。Earnings call transcript 是 IND 未深挖的信息维度（cells.json 无该集判死条目）。
- **禁止复用的族（FAMILY_LOCKED）**：
  - 无整集判死；禁复用 earnings3 日历/timing 机制（IND-EARNINGS3-TIMING-DEAD）
- **本次允许的机制方向**：电话会文本情绪/管理层指引变化（非水平）、事件时钟 interval 变换、同集多字段共动
- **近十年**：阶段 B 基准探针强制 2014–2023 每年 PnL 有数据（`get_alpha_yearly_stats`），未过即换集并写 `output_report/ind_dataset_switch_20261114.md`。

### model77（P1）

- 画像：category=MODEL，塔当季=3（已亮），cov=0.8495，字段=348，ALIVE=0，best S=None，best 2Y=None，回测=0，RA 全过=0，freq=快照（按库表更新，需实测），valueScore=3.0，state=`ELIGIBLE`，flags=lit_category_but_unoccupied。
- **选定理由**：MODEL 塔当季 3（已亮），但 `expressions` / `backtest_results` 均无该集记录 → `lit_category_but_unoccupied` 可用；23 字段、valueScore 6.0（全库最高档）、userCount 66 / alphaCount 116（极冷）、cov 0.8495。350+ 股票选择信号库，提供新信息维度。
- **禁止复用的族（FAMILY_LOCKED）**：
  - 模型分数族 robust 结构性墙：IND-MODEL216-ROBUST-WALL、IND-MDL138-DEVIATION-ROBUST-WALL（首探须自带长短窗 + 负向对照快判）
- **本次允许的机制方向**：首探即带 robust 快慢窗对照；只走残差化 / 分组轴等非裸 rank 结构
- **近十年**：阶段 B 基准探针强制 2014–2023 每年 PnL 有数据（`get_alpha_yearly_stats`），未过即换集并写 `output_report/ind_dataset_switch_20261114.md`。

### other323（P1）

- 画像：category=OTHER，塔当季=4（已亮），cov=0.9996，字段=11，ALIVE=0，best S=None，best 2Y=None，回测=0，RA 全过=0，freq=事件/逐笔型（VECTOR），valueScore=3.0，state=`ELIGIBLE`，flags=lit_category_but_unoccupied。
- **选定理由**：OTHER 塔当季 4（已亮），该集未被占用（`lit_category_but_unoccupied`）；11 字段、cov 0.9996、valueScore 3.0、premarket 市场状态数据。字段少、覆盖满，天然适合 ATOM 与全字段画像；且属非反转、非新闻、非模型分数的新信息维度。
- **禁止复用的族（FAMILY_LOCKED）**：
  - other 类稀疏事件族：IND-OTHER315-SPARSE-DEAD（本集为盘前状态快照，非事件流，需首探验证持仓数）
- **本次允许的机制方向**：盘前状态离散变化、同集多字段共动、残差化（G1）；注意 other 属 trio，禁止与 PV/MODEL 组腿
- **近十年**：阶段 B 基准探针强制 2014–2023 每年 PnL 有数据（`get_alpha_yearly_stats`），未过即换集并写 `output_report/ind_dataset_switch_20261114.md`。

## 3. 候选池分级（全量 ELIGIBLE）

| dataset | cat | cov | 字段 | ALIVE | bestS | best2Y | 塔 | prio | state |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| institutions6 | INSTITUTIONS | 0.992 | 11 | 11 | 3.45 | 3.29 | 1 | P0 | ELIGIBLE |
| sentiment21 | SENTIMENT | 0.9681 | 105 | 4 | 3.01 | 2.07 | 1 | P0 | ELIGIBLE |
| earnings3 | EARNINGS | 0.7906 | 8 | 2 | 4.49 | 1.48 | 2 | P0 | ELIGIBLE |
| model238_anlrev | UNCATEGORIZED | 0.7902 | 1070 | 1 | 2.64 | 3.08 | None | P0 | ELIGIBLE |
| earnings11 | EARNINGS | 0.4992 | 35 | 0 | 0.51 | 0.19 | 2 | P2 | ELIGIBLE |
| news_sentiment_transfer | SENTIMENT | 0.9368 | 23 | 0 | 1.05 | 1.12 | 1 | P2 | ELIGIBLE |
| sentiment23 | SENTIMENT | 0.7028 | 105 | 0 | None | None | 1 | P2 | ELIGIBLE |
| sentiment26 | SENTIMENT | 0.5318 | 18 | 0 | 0.39 | 0.14 | 1 | P2 | ELIGIBLE |
| analyst11 | ANALYST | 0.552 | 210 | 0 | None | None | 3 | P3 | ELIGIBLE |
| analyst39 | ANALYST | 0.8445 | 35 | 0 | None | None | 3 | P3 | ELIGIBLE |
| analyst44 | ANALYST | 0.8343 | 546 | 0 | 1.41 | 2.11 | 3 | P3 | ELIGIBLE |
| analyst46 | ANALYST | 0.585 | 6 | 0 | None | None | 3 | P3 | ELIGIBLE |
| analyst_base_ref | ANALYST | 0.8069 | 14 | 0 | 0.6 | 1.99 | 3 | P3 | ELIGIBLE |
| analyst_earnings_ibes | MODEL | 0.9965 | 28 | 0 | None | None | 3 | P3 | ELIGIBLE |
| analyst_factor_signals | ANALYST | 0.6109 | 58 | 0 | None | None | 3 | P3 | ELIGIBLE |
| analyst_revision_horizons | MODEL | 0.7819 | 1026 | 0 | 2.64 | 3.08 | 3 | P3 | ELIGIBLE |
| fundamental17 | FUNDAMENTAL | 0.8661 | 350 | 0 | None | None | 3 | P3 | ELIGIBLE |
| fundamental23 | FUNDAMENTAL | 0.8947 | 39 | 0 | None | None | 3 | P3 | ELIGIBLE |
| fundamental44 | FUNDAMENTAL | 0.7842 | 12 | 0 | None | None | 3 | P3 | ELIGIBLE |
| fundamental90 | FUNDAMENTAL | 0.7209 | 65 | 0 | None | None | 3 | P3 | ELIGIBLE |
| fundamental93 | FUNDAMENTAL | 0.5362 | 32 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model106 | MODEL | 0.4953 | 14 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model110 | MODEL | 0.7885 | 8 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model216 | MODEL | 0.8223 | 88 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model250 | MODEL | 0.7876 | 20 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model26 | MODEL | 0.7601 | 667 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model262 | MODEL | 0.9009 | 25 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model29 | MODEL | 0.7187 | 91 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model30 | MODEL | 0.7677 | 49 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model31 | MODEL | 0.8303 | 132 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model33 | MODEL | 0.7851 | 32 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model37 | MODEL | 0.9288 | 85 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model38 | MODEL | 0.865 | 71 | 0 | None | None | 3 | P3 | ELIGIBLE |
| model77 | MODEL | 0.8495 | 348 | 0 | None | None | 3 | P3 | ELIGIBLE |
| news104 | NEWS | 0.7348 | 11 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news17 | NEWS | 0.6974 | 24 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news20 | NEWS | 0.876 | 15 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news29 | NEWS | 0.9724 | 12 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news3 | NEWS | 0.6461 | 19 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news31 | NEWS | 0.9681 | 25 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news36 | NEWS | 0.7031 | 43 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news38 | NEWS | 0.8801 | 44 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news46 | NEWS | 0.8996 | 44 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news48 | NEWS | 0.6908 | 22 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news50 | NEWS | 0.8706 | 69 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news54 | NEWS | 0.9073 | 40 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news7 | NEWS | 0.8499 | 33 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news73 | NEWS | 0.665 | 22 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news76 | NEWS | 0.9909 | 6 | 0 | None | None | 4 | P3 | ELIGIBLE |
| news84 | NEWS | 0.6974 | 23 | 0 | None | None | 4 | P3 | ELIGIBLE |
| other323 | OTHER | 0.9996 | 11 | 0 | None | None | 4 | P3 | ELIGIBLE |
| other335 | OTHER | 0.6364 | 10 | 0 | None | None | 4 | P3 | ELIGIBLE |
| other635 | OTHER | 0.627 | 6 | 0 | None | None | 4 | P3 | ELIGIBLE |
| predictive_starmine | MODEL | 0.925 | 638 | 0 | None | None | 3 | P3 | ELIGIBLE |
| pv1 | PV | 1.0 | 24 | 0 | None | None | 11 | P3 | ELIGIBLE |
| pv13 | PV | 0.6681 | 37 | 0 | None | None | 11 | P3 | ELIGIBLE |
| pv29 | PV | 0.7099 | 30 | 0 | None | None | 11 | P3 | ELIGIBLE |
| pv30 | PV | 0.9805 | 675 | 0 | None | None | 11 | P3 | ELIGIBLE |

其余 86 集逐条理由见 `cache/ind_dataset_scan_20261114.json::rows[].reasons`。

## 4. 硬排除集（逐集理由）

- `acquisition_model` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-ACQMODEL-WEAK-NEG（禁复用该机制，整集可用但须换机制）
- `ai_factor_transfer` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `ai_news_scores` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-AINEWS-SENTIMENT-DEAD, IND-SNT23-SENTIMENT-DEAD, IND-AI-NEWS-DEAD（禁复用该机制，整集可用但须换机制）
- `analyst4` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录
- `analyst45` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-ANALYST45-ROBUST-WALL（禁复用该机制，整集可用但须换机制）
- `analyst9` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录
- `analyst_consensus` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 analyst(3) 且 expressions/backtest_results 有该集真实回测记录
- `behavioral_signals` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-IPVF-MICROSTRUCTURE-DEAD（禁复用该机制，整集可用但须换机制）
- `event_relation` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录
- `fundamental1` [EXCLUDED_HARD]：STRUCT: 118 字段全 UNUSABLE，治理/薪酬族判死；族级判死 IND-FUNDAMENTAL1-GOVERNANCE-SPARSE, IND-FND90-EARNINGS-QUALITY-DEAD（禁复用该机制，整集可用但须换机制）
- `fundamental86` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 fundamental(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-CROSS-DS-EARNINGS-DEAD（禁复用该机制，整集可用但须换机制）
- `fundamental89` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 fundamental(3) 且 expressions/backtest_results 有该集真实回测记录
- `fundamental94` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 fundamental(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-CROSS-DS-VOLATILITY-DEAD, IND-CROSS-DS-EARNINGS-DEAD, IND-FND94-THIRD-LEG-DEAD（禁复用该机制，整集可用但须换机制）
- `global_seasonal_model` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-NEWS29-SPARSE-EVENT（禁复用该机制，整集可用但须换机制）
- `imbalance5` [EXCLUDED_HARD]：STRUCT: 字段级 prod 饱和（imb5_score 0.939）+ 仅 2 字段 <5 硬门
- `insiders1` [EXCLUDED_HARD]：STRUCT: maxS 0.95 + cov 0.3877 稀疏，整集判死；族级判死 IND-INSIDERS1-NODIRECTION-DEAD, insiders1（禁复用该机制，整集可用但须换机制）
- `intraday_pv_feats` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-IPVF-MICROSTRUCTURE-DEAD, IND-INTRADAYPV-PRICEVOLUME-CORR-REVERSAL-PRODWALL（禁复用该机制，整集可用但须换机制）
- `macro63` [EXCLUDED_HARD]：STRUCT: IND 侧全域恒 0（dateCreated 2025-10-01），仅作 add-zero 挂塔器；1 字段 <5
- `ml_factor_proj` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-TOP500-CEILING（禁复用该机制，整集可用但须换机制）
- `mmp_nlp_sentiment` [EXCLUDED_HARD]：STRUCT: 平台 unknown variable，IND/TOP500 不可用；族级判死 IND-MMPNLP-UNAVAILABLE（禁复用该机制，整集可用但须换机制）
- `model135` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MDL135-PROD-WALL-FINAL（禁复用该机制，整集可用但须换机制）
- `model138` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-FND23-ANNUAL-BS-DEAD, IND-MDL138-DEVIATION-ROBUST-WALL, IND-PREDICTED-SURPRISE-ROBUST-WALL（禁复用该机制，整集可用但须换机制）
- `model144` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `model16` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `model170` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MODEL170-VALUATION-DEAD（禁复用该机制，整集可用但须换机制）
- `model192` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MODEL192-CDS-DEAD, IND-FND44-ACCOUNTING-QUALITY-DEAD（禁复用该机制，整集可用但须换机制）
- `model238` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-MODEL238-PROD-SATURATED（禁复用该机制，整集可用但须换机制）
- `model252` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `model28` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-CROSS-DS-VOLATILITY-DEAD, IND-FND94-THIRD-LEG-DEAD（禁复用该机制，整集可用但须换机制）
- `model32` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `model36` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `model39` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `model50` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录
- `news79` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 news(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-NEWS29-SPARSE-EVENT, IND-AINEWS-SENTIMENT-DEAD（禁复用该机制，整集可用但须换机制）
- `news85` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 news(4) 且 expressions/backtest_results 有该集真实回测记录
- `news_sentiment_nlp` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-AI-NEWS-DEAD（禁复用该机制，整集可用但须换机制）
- `option1` [EXCLUDED_HARD]：STRUCT: IV 残差 decay/TO 硬互斥 + 近十年数据缺口
- `option30` [EXCLUDED_HARD]：STRUCT: fitness ceiling ~0.85 结构性，cov 0.3629；族级判死 IND-OPTION30-OS-SURPRISE-FITNESS-CEILING（禁复用该机制，整集可用但须换机制）
- `other128` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER128-MANAGEMENT-QUALITY-DEAD（禁复用该机制，整集可用但须换机制）
- `other315` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER315-SPARSE-DEAD（禁复用该机制，整集可用但须换机制）
- `other327` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录
- `other424` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录
- `other436` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录
- `other532` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录
- `other545` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER545-NEMO-DEAD（禁复用该机制，整集可用但须换机制）
- `other567` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-OTHER567-EMPLOYEE-SCORE-DEAD, IND-OTHER567-DEAD（禁复用该机制，整集可用但须换机制）
- `other696` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 other(4) 且 expressions/backtest_results 有该集真实回测记录
- `pv103` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-PV103-PV47-ROBUST-DEAD-WALL, IND-PV103-LASTHOUR-REVERSAL-PROD-TWIN（禁复用该机制，整集可用但须换机制）
- `pv106` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-TOP500-CEILING, IND-MDL138-DEVIATION-ROBUST-WALL, IND-PV103-PV47-ROBUST-DEAD-WALL（禁复用该机制，整集可用但须换机制）
- `pv47` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 pv(11) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-PV103-PV47-ROBUST-DEAD-WALL（禁复用该机制，整集可用但须换机制）
- `pv70` [EXCLUDED_HARD]：STRUCT: 区域错配：APAC ex-Japan/ex-China 专属，IND/TOP500 8/8 全零持仓；族级判死 IND-PV70-REGION-MISMATCH, IND-PV70-DEAD（禁复用该机制，整集可用但须换机制）
- `quant_factor_lib` [EXCLUDED_OCCUPIED]：OCCUPIED: 已亮塔 model(3) 且 expressions/backtest_results 有该集真实回测记录；族级判死 IND-QFL-CREDIT-FAMILY-DEAD（禁复用该机制，整集可用但须换机制）
- `risk68` [EXCLUDED_HARD]：STRUCT: catalog_unreachable_categories.risk 结构性不可达
- `risk70` [EXCLUDED_HARD]：STRUCT: catalog_unreachable_categories.risk 结构性不可达；族级判死 IND-RISK70-NO-SIGNAL（禁复用该机制，整集可用但须换机制）
- `risk71` [EXCLUDED_HARD]：STRUCT: catalog_unreachable_categories.risk 结构性不可达
- `risk88` [EXCLUDED_HARD]：STRUCT: catalog_unreachable_categories.risk 结构性不可达
- `shortinterest5` [EXCLUDED_HARD]：STRUCT: 价带宽度在 TOP500 近常数，maxS 0.22，7 探针全灭 + 3 字段；族级判死 IND-SHORTINTEREST5-PRICEBAND-DEAD（禁复用该机制，整集可用但须换机制）
- `univ1` [EXCLUDED_HARD]：STRUCT: coverage=0 且 1 字段，无信号面

## 5. 换 dataset 触发条件

仅以下三种，且必须写 `output_report/ind_dataset_switch_20261114.md`（触发判据 + 前后集对比 + 原因）：
1. 同一主攻集连续 2 波模板全灭（`gate_results.all_pass` 全 0）；
2. 全字段画像判该集字段全 UNUSABLE / DEAD，或基准探针近十年 PnL 有缺失；
3. 归因给出 `SWITCH_AXIS` / `BLOCKED_BY_CORRELATION`，或 prod 结构性不可达（≥3 个互不相关杠杆收敛同档）。

## 6. 白名单写入

`mcp__wqb-db__upsert_ledger_key(region="IND", key="s0_whitelist", mode="merge")`，只追加本轮 5 个主攻集与 entries，不整值覆盖共享键（旧值 5 集保留）。

## 7. 选集证据修订（MCP 全字段实读后，2026-11-14）

阶段 B 用 MCP `get_datafields(filter_sharpe=False)` 实读 5 集 **185 字段全集**（逐集 `complete=true`）后，发现 DB 画像与平台实况有实质偏差。按用户「不频繁换 dataset」**保持 5 集不变**，只调整机制配额与验证顺序，并留此证据：

| dataset | MCP 实读 | 与阶段 A 判断的差异 | 处置 |
|---|---|---|---|
| `institutions6` | 11 MATRIX / cov 0.992 / 11 ALIVE | 一致 | **主力**，配额最大 |
| `sentiment21` | 105 MATRIX / cov 0.9681 / 4 ALIVE | 白名单写入触发 `dead_intersection` high：跨 4 区（EUR/GLB/KOR/USA）判死；IND 本地 news/sentiment 族亦多证枯竭 | `VALIDATE_FIRST`：首探只发 2 条验证性探针，无信号即换 `analyst11` 并写 switch 报告 |
| `earnings11` | 35 **全 VECTOR** / cov 0.4992 | 实为 RavenPack 新闻情绪/事件元数据（含 timestamp/word_count/identifier），非「电话会文本」；coverage 是历史累计覆盖 | `WEAK_MECHANISM`：配额 ≤2 条，须 `vec_*` 折叠 + 在线持仓数补判 |
| `model77` | 23 MATRIX / cov **0.4001** | 实为 ESG/治理评分（DB 画像 0.8495 是旧版本 348 字段）；与 IND 已判死治理评分类同型 | `WEAK_MECHANISM`：配额 ≤2 条；DB 旧画像本轮作废 |
| `other323` | 11 **全 VECTOR** / cov 0.9996 | 实为股本/票面/手数/标识符静态数据，几无横截面收益信息 | `WEAK_MECHANISM`：仅作分组轴/条件腿，配额 ≤2 条 |

**OCCUPIED 口径二次核对**：本轮另查 `alphas(region_id=5, status=ACTIVE, stage=OS)` join `datasets`，真实已提交占用仅 `analyst_consensus` / `intraday_pv_feats`（另两条是 `_unknown` / `model` 占位）。阶段 A v2 用 `expressions`+`backtest_results`（68 集）偏严——那代表「回测过」而非用户 Q1 所说的「历史 ACTIVE / 判死台账占用」。因该偏严只影响**已亮塔类别**，且 5 个主攻集中 3 个属未亮塔、2 个属 `lit_category_but_unoccupied`，**结论不变**；此处留档供后续战役复用正确口径。

**工具用法新发现（已沉淀）**：`get_datafields` 显式传 `max_fields=null` 会触发 `max_fields_cap`，每集只返 1 条且 `complete=false`（本轮 5/5 集复现）；正确用法是**不传该参数**或传 ≥ `platform_count` 的整数，并始终 `filter_sharpe=False`。这是「全字段完整探测、禁止抽样」的硬前置。
