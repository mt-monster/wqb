# GBR REGULAR 交付清单（滚动更新 · 2026-11-13 版，取代 11-10 版）

> **口径声明（本版起生效）**：
> 1. **算子硬闸：regular.operatorCount ≤ 8**（2026-11-13 21:09 用户指令「≤8 才合格；>8 一律移出」；同日 21:45 用户裁定 ops>8 老候选「严格合规不救援」）——只认平台实值。
> 2. 篮子成员互相关全对 **<0.7**（2026-11-09 全局单一事实源口径）；prod/self 各自 <0.7（prod 为 MCP check_correlation(production) 平台真值）；逐年无空窗无负年。
> 3. 已点亮塔数据集不投入（model6/news3/analyst3/pv4/fund3/shrt4 禁投；本篮全部来自未点亮塔存量候选，RISK 塔 0 待点亮）。

## 一、当前确认篮子（4 颗，全闸+ops≤8+互相关全对<0.7）

| # | alpha | 数据集（塔） | 表达式要点 | 中性化 | S | F | 2Y | TO | ops | self | prod（实测时间） |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **omEdka3v** | other 系（OTHER 塔 2） | techindi 机制 × 组合 | — | 2.51 | 1.40 | — | — | 8 | 0.416 | **0.6026**（11-13 refresh） |
| 2 | **6XdkW08J** | other 系（OTHER 塔 2） | — | — | 2.60 | 1.95 | — | — | 8 | 0.339 | **0.6267**（11-13 refresh） |
| 3 | **pwdd7Za6** | 换手强度 ATOM（PV 已亮塔存量） | — | SUBINDUSTRY | 1.69 | 1.04 | 2.49 | 0.105 | 8 | 0.416 | **0.6238**（11-13 refresh=True） |
| 4 | **omExeqLb** | starval 股息率 × 借券 | — | REV_AND_MOM | 2.43 | 1.78 | 2.12 | 0.170 | 8 | 0.420 | **0.6143**（11-12 platform_sync，31h 保鲜内；终验再刷） |

**互相关矩阵（11-13 实测，4+1 颗）**：max 对 = 6XdkW08J×omExeqLb **0.6123**，其余全 <0.4 ⇒ all_below_threshold=true。

## 二、替补席

| alpha | 读数 | 让位原因 |
|---|---|---|
| pwdLp9z6 | S 2.26 / F 1.19 / prod 0.6483✓（11-13 复核）/ self 0.420 / ops 8 | 与 omEdka3v 互相关 **0.8619** 超线，同族让位（tm_16×借券族） |

## 三、出局档案（11-13 硬闸裁定）

- **ops>8 出局（7 颗，用户裁定不救援）**：rKRx0M2m(11) / O0A6Qz7p(10) / leAmmre8(9) / RREGX1kd(9) / LLM0e20m(11) / Xg9dPpp0(9) / Jje6mrpO(10)——prod 全部 <0.7 曾通过，仅算子数超标。
- **prod 深墙（残差反转面，2026-11-13 收档）**：j2aQa1qo（S 1.81 / F 1.22 / 2Y 1.84 / fails=0 / 逐年 10/10 / self 0.465 / **3 ops 纯 ATOM** risk71 单字段）**prod 0.8496 FAIL**；leaZaro8（S 1.77 / 2Y 1.70 / fails=0）同族同判。机制层饱和证据链：历史裸 zscore 形态墙 0.71-0.76×3 颗 + 本形态 0.85，V3-V9 七波 50+ 臂全测绘。IS 完美但持仓相关深度撞墙——「GBR 的硬墙是 prod，不是 IS」判词再次实证。

## 四、字段画像存档索引（本战役新增）

| 内容 | 路径 |
|---|---|
| 波次全档案（V1-V9 全部表达式/读数/归因/判定链） | tracking/GBR/waves/gb_v1_v2_dispatch_20261113.md |
| 处女集 4 集字段目录+判定 | tracking/GBR/reference/gbr_{event_sentiment_signals,stock_search_trends,socialmedia39}_fields.json |
| risk 塔 5 集字段目录+六法画像 | tracking/GBR/reference/gbr_risk{60,68,71,72,88}_fields.json |
| insider/待勘 5 塔备料目录 | tracking/GBR/reference/gbr_{insider_agg_matrix,institutions25,imbalance5,option1,macro27}_fields.json |

## 五、通往 20 颗的路径（11-13 时点）

- 已点亮塔（禁投）6 塔不动；**未点亮可挖 10 塔**：other 2 / institutions 0 / insiders 0 / earnings 0 / sentiment 0（集已枯）/ risk 0（IS 活、prod 墙）/ option 0 / socialmedia 0（集已死）/ macro 0 / imbalance 0。
- 当前缺口 **16 颗**。

## 五之二、★数据集普查修正（2026-11-13 23:35，本版关键修正）

对 GBR/D1/TOP700 全量 **177 个数据集**拉取元数据后发现：**未点亮 10 塔共 65 个数据集，此前只勘探过约 14 个**。此前的「塔级判死」（sentiment 枯竭 / socialmedia 判死 / insiders 判死 / institutions 判死）每塔只覆盖 1-2 个数据集，**按穷尽度硬约束不成立，改为数据集级逐个判定**。

**未探高价值清单（元数据排序，cov 为元数据值需探针复核）**：
| 数据集 | 塔 | 字段 | cov | ac | vs | 状态 |
|---|---|---:|---:|---:|---:|---|
| sentiment33 | sentiment | 255 | 0.32 | 224 | 5 | **Z2 已探（max 0.40）** |
| event_ml_signals | other | 104 | 0 | 125 | 7 | **Z1 已探（max 0.52/2Y1.43）** |
| earningscall_sentiment | other | 167 | 0 | 66 | 6 | **Z3 在飞** |
| techindi_model | other | 399 | 0 | 28246 | 2 | **Z4 在飞（篮内 omEdka3v 同源富矿）** |
| other696 | other | 220 | 0 | 39 | 6 | 待探 |
| ai_news_scores | other | 105 | 0 | 122 | 5 | 待探 |
| insider_matrix | insiders | 33 | 0.61 | 617 | 4 | 待探（MATRIX） |
| insider_trx_matrix | insiders | 33 | 0.60 | 236 | 5 | 待探 |
| institutions6 | institutions | 11 | 1.0 | 981 | 2 | 待探（已知单边暴露衰减强） |
| fund_holdings_panel | institutions | 18 | 0.91 | 321 | 3 | 待探（基金交易流） |
| socialmedia5/12 | socialmedia | 13/6 | 0 | 164/453 | 3/2 | 待探 |
| sentiment7 | sentiment | 3 | 0.58 | 109 | 4 | 待探 |
| other455 | other | 1500 | 0.94 | 446 | 5 | 半探（GROUP 1200/MATRIX 300，可作替代分组轴） |

**★富矿识别**：篮内两颗 S 2.5+ 件的真实构造 = **「选股信号 + 借券腿」双腿**
- omEdka3v = group_rank(ts_zscore(tm_17_..._r10_q1,126), sector) + reverse(借券)  → techindi_model（other 塔）
- 6XdkW08J = group_rank(ts_zscore(region_relative_valuation_rank,66), market) + reverse(借券) → 估值排名 + 借券

⇒ 通往 20 颗的最短路径 = 在 techindi_model（21 个连续预测字段 = 7 模型 × 3 周期）等 other 塔富矿里找**新的选股腿**，与已用 tm_17_d10 不同变体/周期以控制互相关。

**新增画像档案**：tracking/GBR/reference/gbr_sentiment33_fields.json、gbr_event_ml_signals_fields.json（另 gbr_earningscall_sentiment 待建）
