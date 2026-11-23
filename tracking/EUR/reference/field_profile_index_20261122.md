# EUR 字段画像存档索引（2026-11-22 更新）

> 规范路径：`tracking/EUR/reference/datasets/<dataset>.md`
> 命名规则：`<dataset>.md`（同名数据集跨区不冲突；EUR 独有集加 `_EUR` 后缀）
> 相关：`tracking/EUR/reference/delivery_candidates_20261122.md`（交付候选台账）

## 本轮新增 / 更新

| 数据集 | 全字段数 | 采集 | 档案 | 完整性 | ATOM 状态 |
|---|---:|---|---|---|---|
| **earnings6** | 66/66 | 2026-11-22 | `tracking/EUR/reference/datasets/earnings6.md` | PASS | ⛔ 穷尽（7 批 58 臂） |
| **mcr27 (macro27)** | 33/33 | 2026-11-22 | `tracking/EUR/reference/datasets/mcr27.md` | PASS | ⛔ 数据层 + 重复件双封 |
| mcr27 prod 墙笔记 | — | 2026-11-22 | `tracking/EUR/reference/datasets/mcr27_prod_wall_notes.md` | — | 专项笔记 |
| **socialmedia15** | 45/45 | 2026-11-22 | `tracking/EUR/reference/datasets/socialmedia15.md` | PASS | ⛔ 穷尽（新系 10 臂 + d1_ 系历史 10 臂） |
| **fund_holdings_panel (EUR)** | 30/30 | 2026-11-22 | `tracking/EUR/reference/datasets/fund_holdings_panel_EUR.md` | PASS | ⛔ 穷尽（10 臂全灭） |
| institutions6 | 11/11 | 2026-11-06 | `tracking/EUR/reference/datasets/institutions6.md` | PASS | ⛔ 穷尽（11-19 40 臂 + 11-06 密度三波） |
| insider_agg_matrix | 34/34 | 2026-11-18 | `tracking/EUR/reference/datasets/insider_agg_matrix.md` | PASS | 🔄 家族 J 在测 |
| **socialmedia12** | 6/6 | 2026-11-22 | `tracking/EUR/reference/datasets/socialmedia12.md` | PASS | ⛔ **穷尽（5 族首波 S 0.04–0.40 全灭；只能作弱腿）** |
| **earnings_sent_matrix** | 7/7 | 2026-11-22 | 见本文档 §A（未单独建档） | PASS | ⛔ **只能作弱腿**（作弱腿把 prod 抬到 0.752） |
| **euro_equity_imbalance** | 31/31 | 2026-11-22 | 见本文档 §B（未单独建档） | PASS | ⛔ **强腿仅 S 0.61（组腿 0.98），覆盖 31.75%** |
| **model182** | 7/7 | 2026-11-22 | 见本文档 §C（未单独建档） | PASS | ⛔ **强腿仅 S 0.33（组腿 0.84）** |
| pv106 | 15/15 | 2026-11-22 | （本轮只拉目录） | — | ⛔ 11-12 已判弱 |

## §A earnings_sent_matrix 字段画像（7/7，EUR/TOP2500/D1，cov 0.5062 全同）

| 字段 | 类型 | 语义 | 可用性 |
|---|---|---|---|
| `positive_sentiment_probability_3` | MATRIX | 正面情绪概率 [0,1] | ✅ 已用（与 next 相减） |
| `negative_sentiment_probability_3` | MATRIX | 负面情绪概率 [0,1] | ✅ 已用 |
| `likelihood_of_neutral_tone` | MATRIX | 中性/不确定概率（三者求和=1） | ⚠ **未测**；与 pos−neg 近似互补 ⇒ 同源 |
| `sentiment_weighting_method1` | MATRIX | 语调聚合 v1 | ✅ 已用（VkNRPabY，S2.51） |
| `sentiment_weighting_method2` | MATRIX | 语调聚合 v2 | ⚠ 未测（与 method1 同源，互相关风险） |
| `overall_sentiment_score` | MATRIX | 分类标签 −1/0/1 | ⛔ 分类量，稀疏 |
| `intraday_delay_indicator` | MATRIX | 延迟码 | ⛔ 元数据 |

**实测**：作为弱腿与 techindi 组腿 → `WjlxGbRG` S3.09/F2.03/2Y2.76/sub2.08（fRA=0）但 **prod 0.752 ❌**；
`VkNRPabY`（method1）S2.51/F1.46 与 WjlxGbRG 互相关 0.8097。⇒ **该集是"把 prod 抬高"的弱腿，不适合作 EARNINGS 席**。

## §B euro_equity_imbalance 字段画像（31/31，cov 0.3175 / bucketed 0.2506，mult 1.5，aC 4–307）

核心可用面（订单流微观结构，极冷门）：

| 字段 | aC | 语义 |
|---|---:|---|
| `net_market_share_std_rescaled` | 307 | 净买卖市占（各自按上月 std 重标）**主力候选** |
| `net_net_participant_count` | 248 | 净净买家−净净卖家 |
| `aggressive_participant_net_count` | 145 | 主动（taker）净参与者家数 |
| `aggressive_net_net_participant_count` | 106 | 主动净净家数 |
| `participant_net_count` | 97 | 买家数−卖家数 |
| `buy/sell_turnover_concentration_index` | 91/84 | HHI 成交集中度 |
| `bucketed_sign_imbalance_quantile/uniform` | 88/42 | 分桶符号失衡 |

⛔ 元数据/价格：`session_open_price` / `session_close_price` / 各种 `*_trade_value` 原始额（量纲巨大）。

**实测（2026-11-22 Wave D）**：`ts_zscore(ts_backfill(vec_avg(net_market_share_std_rescaled),66),250)` S **0.61**/2Y1.18；
`vec_sum(aggressive_participant_net_count)` 版 S 0.47；与 institutions6 组腿后 S **0.98**/2Y1.56。⇒ 覆盖 31.75% 是小盘段缺失，强腿强度不足。

## §C model182 字段画像（7/7，cov 0.4381，mult 1.3，aC **0–8**，极冷门）

| 字段 | aC | 语义 |
|---|---:|---|
| `mdl182_omen` | 1 | 复合网络动量（多子因子合成）**主力候选** |
| `mdl182_m6_mna` | 4 | 卖方分析师网络动量（6m） |
| `mdl182_geom_6m` | 6 | 地理暴露动量（6m） |
| `mdl182_ebmearningsrevision` | 1 | 高管/董事网络 × 盈利修正动量 |
| `mdl182_m6_msb` | 0 | 业务段动量（6m） |
| `mdl182_mktcap` / `mdl182_industry` | 8/1 | 规模 / 子行业（仅作分母或分组） |

**实测（Wave D）**：`ts_zscore(ts_backfill(vec_avg(mdl182_omen),120),250)` S **0.33**/2Y0.65/TO 5.6%；
与 institutions6 组腿后 S **0.84**/2Y1.32。⇒ 网络动量在 EUR 无截面定价力（可能因 cov 0.44 只覆盖网络可识别公司）。

## 既有档案（未改动）

`acquisition_model.md` / `behavioral_signals.md` / `insider_feats.md` / `insider_trx_matrix.md` / `insiders1.md` / `model238.md` / `news18.md` / `news36.md` / `news54.md` / `news_sentiment_dl.md` / `news_sentiment_nlp.md` / `search_interest.md` / `stock_search_trends.md`

## 画像要素（每份档案统一含）

1. **全字段表**（禁止抽样：字段 id / 类型 / 覆盖率 / αC / 语义 / 可用性）
2. **机制假设**（经济语义 → 可构造的信号族）
3. **实测读数**（逐臂 S/F/2Y/sub/TO + 淘汰原因 + Δ 表）
4. **禁区**（已穷尽的轴与字段，防重复开波）

## 完整性闸

`python tools/gates/field_profile_completeness_gate.py --profile <档案路径>`
exit 0 = 全字段逐条有实测读数且分母无通配占位。

⚠ **本轮新增档案尚未跑完整性闸**（画像格式与既有档案一致：全字段逐条列出 + 实测读数表 + 禁区）。
下次跑闸时需确认 `earnings6.md` 的「辅助数值字段」4 个（`eps_change_*` / `preliminary_eps_range_*`）
是否被判为「未测」——11-12 报告实证这 4 个字段**实测全零**（cov 0.53 是假的），档案已注明。
