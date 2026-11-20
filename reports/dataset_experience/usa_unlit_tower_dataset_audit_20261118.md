# USA 未点亮塔 · 数据集级审计（2026-11-18）

> 方法：`brain-dataset-exploration-general`（数据集级审计：画像 → 分类落台账 → 代表字段抽样 → 审计结论）。
> 范围：USA/D1/TOP3000，11 个未点亮 category，平台实取 63 个数据集。
> 性质：**分类全量**（平台字段目录逐集实拉），**深挖未做**（代表字段抽样 ≤12 个/集，本轮未进入）。
> 塔位实读（`get_pyramid_alphas`，2026-11-16 晚）：已亮 analyst6 / model4 / other4 / risk3 / earnings3；
> **未亮 institutions(1) 及其余 10 个 category 全 0**。

## 1. 结论摘要

- 未亮塔共 **63 个数据集**，其中 **43 个本仓从未碰过**（含 4 个本会话已探但未深挖的）。
- **可投入白空间集中在 5 个冷门集**（aC ≤ 250 且 vs≥2）：`univ2`(47) / `pv109`(58) / `fundamental35`(71) /
  `fundamental25`(80) / `fundamental22`(92) / `news22`(96)。
- **8 个「已亮塔遗留」的未亮塔集**（news48 / news84 / institutions20 / insiders1 / sentiment27 / option6 /
  shortinterest3 等）已在本会话或历史波次有实测读数，不构成新白空间。
- **重大结构性事实**：未亮塔里 **`imbalance` 只有 1 个集（`imbalance5`，2 字段）**，
  而 GBR 侧已实测该集 ATOM 技术可行但 **prod 全卡 0.776–0.798** ⇒ 该塔在 USA 同样不可能点亮。

## 2. 完全未测集（43 个，按 alphaCount 升序 = 最冷优先）

| dataset | category | 字段 | cov | userCnt | aCnt | vs | mult |
|---|---|---|---|---|---|---|---|
| univ2 | pv | 1 | 0.670 | 15 | 47 | 3.0 | 1.1 |
| pv109 | pv | 34 | 0.300 | 37 | 58 | 3.0 | 1.1 |
| fundamental35 | fundamental | 1 | 1.000 | 33 | 71 | 3.0 | 1.1 |
| fundamental25 | fundamental | 8 | 0.382 | 57 | 80 | 3.0 | 1.1 |
| fundamental22 | fundamental | 14 | 0.723 | 50 | 92 | 4.0 | 1.1 |
| news22 | news | 4 | 0.877 | 36 | 96 | 3.0 | 1.2 |
| dl_volume_pred | pv | 8 | 1.000 | 86 | 139 | 3.0 | 1.1 |
| news76 | news | 6 | 0.903 | 88 | 145 | 2.0 | 1.2 |
| other452 | fundamental | 46 | 0.530 | 53 | 166 | 4.0 | 1.1 |
| pv63 | pv | 16 | 0.985 | 114 | 184 | 2.0 | 1.1 |
| news85 | news | 23 | 0.985 | 128 | 212 | 2.0 | 1.2 |
| pv106 | pv | 6 | 1.000 | 128 | 216 | 2.0 | 1.1 |
| fundamental69 | fundamental | 12 | 0.611 | 144 | 242 | 2.0 | 1.1 |
| pv115 | pv | 12 | 0.932 | 119 | 393 | 2.0 | 1.1 |
| macro63 | macro | 3 | 1.000 | 171 | 464 | 2.0 | 1.1 |
| short_interest_pred | shortinterest | 10 | 0.999 | 236 | 518 | 3.0 | 1.1 |
| option3 | option | 20 | 0.880 | 337 | 596 | 3.0 | 1.3 |
| sentiment7 | sentiment | 45 | 0.089 | 316 | 674 | 3.0 | 1.4 |
| fundamental110 | fundamental | 26 | 0.821 | 375 | 787 | 2.0 | 1.1 |
| macro17 | macro | 1 | 0.500 | 148 | 845 | 2.0 | 1.1 |
| pv47 | pv | 2 | 1.000 | 381 | 932 | 1.0 | 1.1 |
| news3 | news | 19 | 0.961 | 302 | 1029 | 1.0 | 1.2 |
| sentiment26 | sentiment | 36 | 0.853 | 323 | 1029 | 2.0 | 1.4 |
| socialmedia5 | socialmedia | 13 | 0.951 | 257 | 1102 | 1.0 | 1.1 |
| news46 | news | 91 | 0.985 | 435 | 1123 | 2.0 | 1.2 |
| macro10 | macro | 1 | 1.000 | 309 | 1280 | 2.0 | 1.1 |
| macro4 | macro | 11 | 0.977 | 357 | 1372 | 2.0 | 1.1 |
| pv141 | pv | 6 | 0.500 | 281 | 1403 | 1.0 | 1.1 |
| pv53 | pv | 5 | 0.500 | 239 | 1458 | 1.0 | 1.1 |
| insiders4 | insiders | 16 | 0.637 | 415 | 1459 | 2.0 | 1.1 |
| news52 | news | 42 | 0.711 | 374 | 1593 | 1.0 | 1.2 |
| imbalance5 | imbalance | 2 | 0.867 | 1636 | 4882 | 1.0 | 1.0 |
| other551 | macro | 33 | 1.000 | 1032 | 6253 | 2.0 | 1.1 |
| pv104 | pv | 46 | 0.972 | 603 | 8247 | 1.0 | 1.1 |
| pv103 | pv | 79 | 1.000 | 1080 | 9740 | 1.0 | 1.1 |
| sentiment1 | sentiment | 19 | 0.582 | 2644 | 15057 | 2.0 | 1.4 |
| fundamental13 | fundamental | 87 | 0.757 | 1621 | 15448 | 1.0 | 1.1 |
| macro38 | macro | 56 | 0.994 | 1419 | 16289 | 2.0 | 1.1 |
| socialmedia8 | socialmedia | 4 | 1.000 | 6889 | 17694 | 1.0 | 1.1 |
| news18 | news | 121 | 0.730 | 10153 | 60874 | 1.0 | 1.2 |
| socialmedia12 | socialmedia | 18 | 0.986 | 25790 | 63676 | 1.0 | 1.1 |
| option9 | option | 74 | 0.982 | 25566 | 92964 | 1.0 | 1.3 |
| option8 | option | 64 | 0.970 | 38027 | 227691 | 1.0 | 1.3 |

## 3. 已测集（对照，本会话或历史波次有读数）

| dataset | category | 字段 | cov | aCnt | mult | 已有实测结论 |
|---|---|---|---|---|---|---|
| news73 | news | 22 | 1.000 | 160 | 1.2 | 情绪水平 −0.15/−0.77 死 |
| news84 | news | 23 | 1.000 | 169 | 1.2 | 2 臂（净语气/偏度）全弱 |
| insider_agg_matrix | insiders | 17 | 0.772 | 190 | 1.1 | 21 臂/6 族/5 维；S 天花板 1.01 |
| news_sentiment_transfer | sentiment | 23 | 0.947 | 220 | 1.4 | 2 臂落 OTHER 已亮塔被停投 |
| news97 | news | 105 | 0.976 | 276 | 1.2 | 16 臂（相关性错位族 S1.46 近闸） |
| shortinterest29 | shortinterest | 32 | 0.884 | 276 | 1.1 | 判死清单 |
| us_short_sale | shortinterest | 4 | 1.000 | 356 | 1.1 | 8 臂，天花板 0.84 |
| news48 | news | 22 | 0.978 | 374 | 1.2 | 6 臂，F 闸结构性天花板 |
| shortinterest24 | shortinterest | 1 | 0.257 | 449 | 1.1 | 6 臂，PROVISIONAL 停投 |
| event_return_model | news | 59 | 0.999 | 486 | 1.2 | 8 臂全弱，F 闸天花板 |
| board_gov_stats | insiders | 46 | 0.920 | 669 | 1.1 | 6 臂；离任率反向 2Y 1.55 距闸 0.03 |
| fund_holdings_panel | institutions | 30 | 0.996 | 936 | 1.0 | 34+14 臂；S1.36/F0.73/2Y0.97，修形穷尽 |
| institutions20 | institutions | 17 | 0.980 | 1358 | 1.0 | 跨区测过（1.62→0.49）；USA 未深挖 |
| shortinterest43 | shortinterest | 32 | 0.999 | 1571 | 1.1 | 20+ 臂；d5adA29x S1.51/F0.98 |
| institutions18 | institutions | 17 | 0.805 | 2587 | 1.0 | 8 臂全灭；水平版撞 fnd6 规模 trio |
| institutions6 | institutions | 22 | 1.000 | 3825 | 1.0 | 跨区测过（1.62→0.49），字段替换耗尽 |
| insiders1 | insiders | 45 | 0.601 | 3980 | 1.1 | USA 未测；有 D1 模板匹配先验（流量÷存量） |
| shortinterest3 | shortinterest | 31 | 1.000 | 4856 | 1.1 | Q1-Q3 模式，波动调整 S1.19 |
| sentiment27 | sentiment | 17 | 0.887 | 6883 | 1.4 | 已画像 276 字段，55% 零挖掘 |
| option6 | option | 133 | 0.962 | 19243 | 1.3 | IV 分位 0.45/−0.25 |

## 4. 按塔分组的机会评估（未亮塔）

| 塔 | 集数 | 完全未测 | 最冷集（aC） | 备注 |
|---|---|---|---|---|
| institutions | 4 | 2 | institutions20 (1358) | 塔已 1/3；fhp 已穷尽，institutions20 剩「流量轴」未测 |
| insiders | 4 | 1 | **insiders4 (1459)** | 塔 0/3；board_gov_stats 有近闸件（2Y 1.55） |
| news | 12 | 6 | **news22 (96)** / news76 (145) / news85 (212) | 塔 0/3；news22 仅 4 字段 |
| option | 4 | 2 | **option3 (596)** | 塔 0/3，倍率 **1.3**（未亮塔里最高之一） |
| fundamental | 7 | 5 | **fundamental35 (71)** / fundamental25 (80) / fundamental22 (92) / other452 (166) | 塔 0/3；fundamental22(ESG) vs 4.0 |
| sentiment | 5 | 3 | **sentiment26 (1029)** | 塔 0/3，倍率 **1.4**（最高）；sentiment7 cov 0.089 排除 |
| macro | 6 | 5 | **macro63 (464)** / other551 (6253) | 塔 0/3；macro63 指数重构 3 字段 |
| pv | 12 | 9 | **pv63 (184)** / pv106 (216) / pv115 (393) | 塔 0/3；pv 集多但多数拥挤 |
| socialmedia | 3 | 2 | socialmedia5 (1102) | 塔 0/3 |
| shortinterest | 6 | 1 | **short_interest_pred (518)** | 塔 0/3；SI 预测 10 字段 |
| imbalance | 1 | 1 | imbalance5 (4882) | **塔仅 1 集 2 字段 ⇒ 结构上不可能点亮**（且 GBR 实证 prod 全卡 0.776-0.798）|

## 5. 审计结论

1. **不构成「该面已穷尽」的表述**：43 个完全未测集 + 8 个已测集未深挖，D1–D6 远未满足，
   按 §7.6 只能记 PROVISIONAL。
2. **优先候选（冷 + 倍率高 + 机制独立）**：
   - `news22`（4 字段 / aC 96 / mult 1.2）——**语料级直喂**，机制与情绪分数族正交；
   - `option3`（20 字段 / aC 596 / **mult 1.3**）——期权**虚值档**聚合，与 IV 分位族（option6 已死）不同层；
   - `fundamental22`（ESG 14 字段 / aC 92 / vs 4.0）——**ESG 慢变量**，天然绕开规模代理；
   - `short_interest_pred`（10 字段 / aC 518 / vs 3.0）——**SI 预测值**，与已测的成交量口径（us_short_sale / shortinterest43）机制不同源；
   - `insiders4`（16 字段 / aC 1459）——**EDGAR 申报事件**，与 board 统计轴不同源。
3. **⚠ 结构性封闭**：`imbalance` 塔在 USA 只有 1 集 2 字段 ⇒ **该塔无法点亮**，不必投入。
4. **未做**：字段级分类（`s1_semantic_<ds>` 台账）与代表字段抽样（≤12 个/集）——
   本轮只做数据集级画像。分类落点需先有字段目录（步 3 的 `workflow_campaign(stage="S1")`）。

## 6. 证据来源

- 平台实读：`get_datasets`（11 个 category 逐个，region=USA delay=1 universe=TOP3000）、
  `get_pyramid_alphas`（塔位）。
- 本仓实测历史：台账 `tracking/USA/runs/usa_campaign_ledger_20261114.md` §13–§23 与 `docs/experience/` 记忆。
- 论坛：未检索（本轮为数据集级审计，无判死/复开需求，不满足论坛触发条件）。
