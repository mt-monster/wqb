# CHN 数据集画像与开采优先级（75 数据集 / 12 category）— 2026-11-06

> **塔位事实**：CHN 在 D1 **0 座塔点亮**（12 category 全部 <3）⇒ 不受「已点亮塔不选」约束，任何一颗提交都点亮新塔。
> **拥挤度事实**：CHN 平台 alphaCount 全场最低（数据集级 0–6072，多数 <300），EUR 同类动辄几千到几十万 ⇒ **prod 池天然更薄**。
> **唯一合法 universe = `TOP2000U`**，无 COUNTRY 中性化档；默认档 SUBINDUSTRY / decay4 / trunc0.08 / VERIFY / nan OFF / pasteurization ON / maxTrade OFF。

## 一、按 category 汇总

| category | 数据集数 | 字段数 | maxCov | aC 合计 | 判定 |
|---|---:|---:|---:|---:|---|
| analyst | 6 | 2574 | 1.000 | 3403 | 可挖：analyst11(126/0.508/aC21)、analyst_base_ref(7/0.85/aC5)；analyst45 已测（隐含涨幅面弱） |
| fundamental | 6 | 3962 | 0.902 | 5560 | 可挖：fundamental23(316/0.81/aC117) 最佳平衡、china_funda_data(613/0.731/aC38) |
| institutions | 1 | 6 | 0.263 | 67 | 暂缓：唯一数据集 cov 0.263，横截面太稀 |
| macro | 3 | 119 | 1.000 | 1048 | **结构性封闭**：other551 全是指数级序列（beta/r2/resret of SHSZ300/HSI…），横截面恒定 ⇒ 做不出截面 alpha；另两个 cov 0.33 |
| model | 20 | 2245 | 0.999 | 14722 | **最富矿**：ai_equity_alpha(582/0.979/aC97)、model138(120/0.999/aC604)、analyst_earnings_ibes(28/0.995/aC70)、model36(21/0.981/aC27，已测方向负)；model170/event_stock_model/model307/model207 aC≤6 |
| news | 9 | 242 | 1.000 | 544 | news46 已于 2026-11-03 被 12 语义模板 + 4 几何扫过（正向几何系统性 −1.06~−1.24）；余 news29/news76/news38 字段少但 aC 3–5 |
| other | 15 | 5603 | 0.999 | 1860 | 可挖：other715(18/0.957/aC39)、other545(8/0.954/aC76)、other592/other546(aC 1)；china_stock_funda 字段 4973 但 cov 0.736 |
| pv | 10 | 2122 | 1.000 | 17943 | pv1 aC 14905 已饱和；低 aC 的 pv173(3/aC5)、pv106(11/aC40)、univ1(3/aC2)、pv25(284/aC36) 值得一试；continuation_score/pattern_scores 在 EUR 已挖尽 |
| risk | 2 | 120 | 1.000 | 1114 | mfm_model_output 是行业/风格暴露标志（信号价值低，**适合当自定义分组轴**，属两塔混合受配额约束）；risk72(45/0.966/aC853) 可挖 |
| sentiment | 1 | 15 | 0.308 | 364 | 暂缓：唯一数据集 cov 0.308 |
| shortinterest | 1 | 3 | 1.000 | 101 | **结构性封闭**：shortinterest5 实为涨跌停价格带（limit_activation_flag / max / min price），不含价格本身，做不出距离类信号 |
| socialmedia | 1 | 2 | 0.685 | 274 | 暂缓：唯一数据集仅 2 字段、cov 0.685 |

## 二、数据集全表（按 category → 覆盖降序）

| category | dataset | 字段数 | cov | aC |
|---|---|---:|---:|---:|
| analyst | `analyst45` | 60 | 1 | 6 |
| analyst | `analyst_base_ref` | 7 | 0.85 | 5 |
| analyst | `analyst10` | 1052 | 0.637 | 402 |
| analyst | `analyst69` | 1021 | 0.593 | 2012 |
| analyst | `analyst11` | 126 | 0.508 | 21 |
| analyst | `analyst14` | 308 | 0.5 | 957 |
| fundamental | `fundamental4` | 1 | 0.902 | 12 |
| fundamental | `fundamental23` | 316 | 0.81 | 117 |
| fundamental | `fundamental27` | 1777 | 0.809 | 878 |
| fundamental | `china_funda_data` | 613 | 0.731 | 38 |
| fundamental | `fundamental5` | 957 | 0.712 | 547 |
| fundamental | `fundamental6` | 298 | 0.5 | 3968 |
| institutions | `fund_holdings_panel` | 6 | 0.263 | 67 |
| macro | `other551` | 18 | 1 | 424 |
| macro | `china_index_model` | 30 | 0.339 | 10 |
| macro | `macro61` | 71 | 0.331 | 614 |
| model | `model138` | 120 | 0.999 | 604 |
| model | `analyst_earnings_ibes` | 28 | 0.995 | 70 |
| model | `model39` | 10 | 0.99 | 2162 |
| model | `model36` | 21 | 0.981 | 27 |
| model | `ai_equity_alpha` | 582 | 0.979 | 97 |
| model | `model175` | 424 | 0.973 | 6072 |
| model | `model170` | 11 | 0.965 | 6 |
| model | `event_stock_model` | 3 | 0.941 | 6 |
| model | `model31` | 148 | 0.938 | 264 |
| model | `model243` | 4 | 0.922 | 143 |
| model | `model14` | 524 | 0.864 | 2120 |
| model | `model291` | 4 | 0.801 | 80 |
| model | `price_signal_dl` | 28 | 0.691 | 13 |
| model | `model135` | 137 | 0.678 | 29 |
| model | `model307` | 14 | 0.674 | 0 |
| model | `model37` | 49 | 0.666 | 15 |
| model | `model207` | 3 | 0.646 | 0 |
| model | `model26` | 126 | 0.629 | 2892 |
| model | `behavioral_signals` | 7 | 0.313 | 6 |
| model | `model144` | 2 | 0.289 | 116 |
| news | `news46` | 37 | 1 | 7 |
| news | `news29` | 10 | 0.965 | 4 |
| news | `news76` | 6 | 0.937 | 3 |
| news | `news38` | 63 | 0.927 | 5 |
| news | `news7` | 2 | 0.753 | 133 |
| news | `news79` | 85 | 0.743 | 379 |
| news | `news21` | 4 | 0.404 | 5 |
| news | `news50` | 25 | 0.396 | 5 |
| news | `news11` | 10 | 0.391 | 3 |
| other | `search_sentiment_cn` | 3 | 0.999 | 24 |
| other | `market_news_sent` | 3 | 0.997 | 11 |
| other | `acquisition_model` | 15 | 0.996 | 130 |
| other | `other561` | 141 | 0.996 | 920 |
| other | `other715` | 18 | 0.957 | 39 |
| other | `other545` | 8 | 0.954 | 76 |
| other | `news_sentiment_enriched` | 7 | 0.887 | 2 |
| other | `other370` | 130 | 0.764 | 19 |
| other | `other496` | 91 | 0.751 | 94 |
| other | `china_stock_funda` | 4973 | 0.736 | 170 |
| other | `cn_stock_sentiment` | 49 | 0.71 | 363 |
| other | `other592` | 7 | 0.705 | 1 |
| other | `other546` | 8 | 0.681 | 1 |
| other | `insider_feats` | 118 | 0.581 | 7 |
| other | `other315` | 32 | 0.294 | 3 |
| pv | `pv1` | 24 | 1 | 14905 |
| pv | `pv173` | 3 | 1 | 5 |
| pv | `pv106` | 11 | 0.999 | 40 |
| pv | `continuation_score` | 560 | 0.991 | 87 |
| pv | `pattern_scores` | 504 | 0.991 | 138 |
| pv | `pv30` | 250 | 0.899 | 591 |
| pv | `univ1` | 3 | 0.89 | 2 |
| pv | `pv27` | 458 | 0.873 | 831 |
| pv | `pv29` | 25 | 0.764 | 1308 |
| pv | `pv25` | 284 | 0.707 | 36 |
| risk | `mfm_model_output` | 75 | 1 | 261 |
| risk | `risk72` | 45 | 0.966 | 853 |
| sentiment | `sentiment27` | 15 | 0.308 | 364 |
| shortinterest | `shortinterest5` | 3 | 1 | 101 |
| socialmedia | `socialmedia12` | 2 | 0.685 | 274 |

## 三、开采优先级队列（低 aC × 好覆盖 × 字段足够）

| 序 | dataset | 理由 | 状态 |
|---:|---|---|---|
| 1 | `ai_equity_alpha` | 582 字段/0.979/**aC 97**，会计取证+应计+盈余质量，文献最厚（Sloan/Beneish/Dechiro） | **在飞** `45569SabV4ne8GFZkdcmJGg` |
| 2 | `model36` | 21/0.981/**aC 27**，信用风险五因子+困境分位五档 | 已测 T1 S−0.62（方向负、量级非零）、T3 静态字段作废；wave2 在飞 `1FNrpv1Px5e99gQsaUMtvqq` |
| 3 | `model138` | 120/0.999/aC604。**已画像**：40 个会计比率族 × 3 个窗口（3/4/5 季度），每族三型——`*idp` 原始偏离、`*idpqc`/`qpdi*` 质量调整偏离、`pdi*_{cash,caps,ebitda,sale}` 绝对水平偏离。语义=**会计比率相对其历史趋势的偏离度**（基本面意外/预期差），天然适配「基本面均值回复 + 盈余质量」模板族 | 未开始（画像完成，待建 ≥10 模板池） |
| 4 | ~~`analyst_earnings_ibes`~~ | **★降级（画像后发现名不符实）**：28 字段实测全是**价量面板**——`closing_price_dlr{1,2}`、`{one, five, twenty, sixty, one_twenty, two_fifty}_day_total_return_dlr{1,2}`、`trading_volume`、`volume_weighted_avg_price`、`highest/lowest/opening_price`、`market_capitalization`、`shares_outstanding`。**没有任何 IBES 估值/预期字段** ⇒ 估计修正类几何在此**无法实施**。残余价值：① `market_capitalization` + `shares_outstanding` 可当**自定义分组轴**（size bucket）；② `dlr1`(Americas 口径) vs `dlr2`(Europe 口径)**双版本同义字段**可测口径差/实现噪声，但 CHN 两者大概率同值，需先探针验证再投入 | 降为低优先 |
| 5 | `fundamental23` | 316/0.81/aC117，资产负债表明细（应付/应收/应计利息…） | 未开始 |
| 6 | `analyst11` + `analyst_base_ref` | aC 21 / 5，字段少但几乎无人用 | 未开始 |
| 7 | `other715`/`other545` | 0.957/0.954，aC 39/76 | 未开始 |
| 8 | `risk72` | 45/0.966/aC853 | 未开始 |

## 四、结构性排除（不要再花波次）

- **`other551`（macro 全族）**：全部是**指数级**时间序列（`oth551_beta_shsz300`、`oth551_r2_hsi`、`oth551_resret_mxcnx`…），同一天对所有股票取值相同 ⇒ 横截面 alpha 恒为常数，`group_rank` 全并列。**MACRO 塔在 CHN 无截面原料**。
- **`shortinterest5`**：三个字段是 `limit_activation_flag` / `maximum_daily_price` / `minimum_daily_price`，是**涨跌停价格带**，不含收盘价 ⇒ 数据集内部算不出「距涨停距离」。要做得引入 PV 价格腿（PV×SHORTINTEREST = 集合内×集合外，受 ≤5 类总量约束）。
- **`mfm_model_output`**：`industry_*_flag` / `*_sector_grouping` / `diversified_sector_risk_tilt` 是**行业与风格暴露**，自身不是收益信号；其最大价值是**给别的数据集当自定义分组轴**（替换 industry/subindustry），属两塔混合。
- **coverage < 0.35 三件**：`sentiment27`(0.308)、`fund_holdings_panel`(0.263)、`other315`(0.294)、`behavioral_signals`(0.313)、`model144`(0.289) —— 横截面太稀，本区 sub_universe 闸难过。

## 五、已测结论（CHN 侧）

| dataset | 机制 | 代表 alpha | S | TO | 结论 |
|---|---|---|---:|---:|---|
| `analyst45` | 分析师想法隐含涨幅（目标退出价 vs 现价） | `vR1YMo73` / `9qxG125K` | 0.11 / 0.02 | 29% / 30% | 该面在 CHN 无信号，且换手偏快（与 EUR 慢信号相反） |
| `model36` | 信用质量五因子复合 | `MPYgoPVk` | −0.62 | 3.9% | **方向相反**（A 股低质量溢价），翻号 +0.62；1 骨架，未判死 |
| `model36` | 评级迁移（ts_delta 66d） | `j2YVb2Oe` | 0 | 0% | **静态字段**，delta 恒 0，几何作废 |
| `news46` | 12 语义模板 + 4 几何（2026-11-03） | 多 | −1.24~0.25 | 4–7% | 全弱，正向几何一致为负 ⇒ 注意力反转 |
