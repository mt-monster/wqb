# order_flow_imb（Option Order Flow Imbalance）字段画像与批次 20 预登记（USA / TOP3000 / D1）

as_of 2026-10-21　｜　平台：USA　｜　delay 1　｜　universe TOP3000
数据来源：`GET /data-fields?dataset.id=order_flow_imb&region=USA&delay=1&universe=TOP3000`，`complete=true / platform_count=120`，全量落盘 `logs/_tmp_ofi_fields.json`（临时件）。

## 0. 数据集元信息

| 项 | 值 |
|---|---|
| 数据集 id | `order_flow_imb`（Option 类别，未点亮塔） |
| 字段数 | **120（全部 MATRIX，无 VECTOR）** ⇒ 不需要 `vec_*` 聚合，也不会有 vector 字段缺聚合导致的整批 ERROR |
| 覆盖率 | 四档：**0.9058**（全量口径 base，26 字段）/ **0.7882**（`_ise`）/ **0.7728**（`_noto`、`_noto_2`）/ **0.7701**（`_otm`）；全部 > 0.4，**无需 `ts_backfill` 兜底** |
| 拥挤度 | 数据集 aC **478**；但分布极度不均——`customer_trade_imbalance` 108 / `customer_vol_imbalance` 89 / `customer_vol_imbalance_ise` 54，其余 **aC 0–26**。uC 197 |
| valueScore / multiplier | 3 / 1.3（>1 说明平台按高价值数据集计权） |
| 语义 | ISE / NOTO **期权市场参与者分层**的看涨/看跌定向流：按 6 类参与者（customer / firm / broker_dealer / market_maker / pro_customer / proprietary）统计 bullish（买 call + 卖 put）与 bearish（卖 call + 买 put）的合约数 / 笔数 / 成交量，并给出归一化失衡 `*_imbalance = (bull − bear) / (bull + bear)`。**不是**日内限价单簿失衡 |
| 是否点亮 | 未点亮（USA/D1 本季亮塔 = model 4 / analyst 1 / earnings 1） |
| 入选理由 | ① 交付报告已证：USA「未判死 × 可开采」Fundamental 库存归零（fnd67/fnd93/fnd91/fnd1/fnd2/fnd21 全灭或待封存，fnd22 本日触发预登记判死线），缺口只能来自**未点亮塔的新机制**；② `insider` 类别 `get_datasets` 返回 0 个数据集，不可用；③ option 类的 `option8` aC 203K / `option9` aC 83K 已饱和，`order_flow_imb` aC 478 是同类里的蓝海，且 `option3` 仅 20 字段；④ 论坛 2026-10 实证（`search_forum_posts`：order flow imbalance / high turnover）将其列为**高换手首选数据集**，USA/D1 实测 alpha 换手 25.6%–56.2%——正好补上 fnd22 暴露的「换手 <3% 锁死 Fitness」短板 |

## 1. 字段清单（120/120，ATOM 全覆盖）

### 1.1 结构矩阵

- **6 参与者** × **2 方向**（bullish / bearish）× **3 度量**（contracts / trade_count / vol）× **4 口径**（base 0.9058 / `_ise` 0.7882 / `_noto` 0.7728 / `_otm` 0.7701）—— 但并非满格：`contracts` 只存在于 `_noto`；`proprietary` 没有 `_ise`/`_noto` 变体；部分字段带 `_noto_2` 后缀（平台侧同义口径）。
- **失衡字段（`*_imbalance`）**：6 参与者 × trade/vol × 各口径 = 33 个；是本集的**主信号面**（方向已归一化，天然横截面可比）。
- **原始量字段**（bullish/bearish × contracts/trade_count/vol）= 87 个；适合做**关注度门控**或分母归一化，不作主信号（方向信息已被 imbalance 吸收）。

| 参与者 | 经济角色（先验） | 失衡字段 | 最冷代表字段（aC） |
|---|---|---|---|
| `customer` | 散户 / 公共客户；文献（Pan & Poteshman 2006）证明其**开仓定向流有收益预测力** | 8 | `customer_trade_imbalance_otm`（3）/`customer_vol_imbalance_otm`（3） |
| `firm` | 券商自营盘；信息型、冷门 | 7 | `firm_vol_imbalance`（4）/`firm_vol_imbalance_noto`（0） |
| `broker_dealer` | 经纪自营；中间商，方向弱 | 8 | `broker_dealer_vol_imbalance_noto_2`（2）/`_otm`（2） |
| `market_maker` | 做市商；**多为对手盘/对冲**，方向常需反读 | 6 | `market_maker_vol_imbalance_noto_2`（14）/ base（23） |
| `pro_customer` | 专业客户；半知情 | 8 | `pro_customer_trade_imbalance_noto_2`（0）/`pro_customer_vol_imbalance_otm`（2） |
| `proprietary` | 自营（覆盖仅 0.7882，无 `_ise`/`_noto`） | 4 | `proprietary_vol_imbalance`（0）/`proprietary_trade_imbalance`（3） |

### 1.2 全量字段表（120 行）

| # | 字段 id | cov | aC | uC | 描述（截断） |
|---|---|---|---|---|---|
| 1 | `broker_dealer_bearish_contracts_noto` | 0.7728 | 1 | 1 | Total contracts from selling calls and buying puts by brok |
| 2 | `broker_dealer_bearish_trade_count` | 0.9058 | 3 | 3 | Number of bearish trades (selling calls and buying puts) b |
| 3 | `broker_dealer_bearish_trade_count_ise` | 0.7882 | 5 | 5 | Number of bearish trades (selling calls and buying puts) b |
| 4 | `broker_dealer_bearish_trade_count_noto` | 0.7728 | 3 | 3 | Number of bearish trades (selling calls and buying puts) b |
| 5 | `broker_dealer_bearish_trade_count_otm` | 0.7701 | 3 | 3 | Number of bearish trades (selling calls and buying puts) b |
| 6 | `broker_dealer_bearish_vol` | 0.9058 | 16 | 5 | Total volume of bearish trades (selling calls and buying p |
| 7 | `broker_dealer_bearish_vol_ise` | 0.7882 | 2 | 2 | Total volume of bearish trades (selling calls and buying p |
| 8 | `broker_dealer_bearish_vol_otm` | 0.7701 | 1 | 1 | Total volume of bearish trades (selling calls and buying p |
| 9 | `broker_dealer_bullish_contracts_noto` | 0.7728 | 2 | 2 | Total contracts from buying calls and selling puts by brok |
| 10 | `broker_dealer_bullish_trade_count` | 0.9058 | 0 | 0 | Number of bullish trades (buying calls and selling puts) b |
| 11 | `broker_dealer_bullish_trade_count_ise` | 0.7882 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 12 | `broker_dealer_bullish_trade_count_otm` | 0.7701 | 2 | 2 | Number of bullish trades (buying calls and selling puts) b |
| 13 | `broker_dealer_bullish_trades_noto` | 0.7728 | 2 | 2 | Count of trades from buying calls and selling puts by brok |
| 14 | `broker_dealer_bullish_vol` | 0.9058 | 15 | 4 | Total volume of bullish trades (buying calls and selling p |
| 15 | `broker_dealer_bullish_vol_ise` | 0.7882 | 1 | 1 | Total volume of bullish trades (buying calls and selling p |
| 16 | `broker_dealer_bullish_vol_otm` | 0.7701 | 1 | 1 | Total volume of bullish trades (buying calls and selling p |
| 17 | `broker_dealer_trade_imbalance` | 0.9058 | 10 | 7 | Normalized difference between bullish and bearish trade co |
| 18 | `broker_dealer_trade_imbalance_ise` | 0.7882 | 2 | 2 | Normalized difference between bullish and bearish trade co |
| 19 | `broker_dealer_trade_imbalance_noto` | 0.7728 | 6 | 4 | Normalized difference between bullish and bearish trade co |
| 20 | `broker_dealer_trade_imbalance_otm` | 0.7701 | 6 | 2 | Normalized difference between bullish and bearish trade co |
| 21 | `broker_dealer_vol_imbalance` | 0.9058 | 16 | 14 | Normalized difference between bullish and bearish trade vo |
| 22 | `broker_dealer_vol_imbalance_ise` | 0.7882 | 7 | 6 | Normalized difference between bullish and bearish trade vo |
| 23 | `broker_dealer_vol_imbalance_noto_2` | 0.7728 | 2 | 2 | Normalized difference between bullish and bearish contract |
| 24 | `broker_dealer_vol_imbalance_otm` | 0.7701 | 2 | 2 | Normalized difference between bullish and bearish trade vo |
| 25 | `customer_bearish_contracts_noto` | 0.7728 | 3 | 2 | Aggregate contracts from selling calls and buying puts by  |
| 26 | `customer_bearish_trade_count` | 0.9058 | 6 | 5 | Number of bearish trades (selling calls and buying puts) b |
| 27 | `customer_bearish_trade_count_ise` | 0.7882 | 2 | 2 | Number of bearish trades (selling calls and buying puts) b |
| 28 | `customer_bearish_trade_count_otm` | 0.7701 | 0 | 0 | Number of bearish trades (selling calls and buying puts) b |
| 29 | `customer_bearish_trades_noto` | 0.7728 | 9 | 7 | Number of trades from selling calls and buying puts by cus |
| 30 | `customer_bearish_vol` | 0.9058 | 7 | 7 | Total volume of bearish trades (selling calls and buying p |
| 31 | `customer_bearish_vol_ise` | 0.7882 | 8 | 6 | Total volume of bearish trades (selling calls and buying p |
| 32 | `customer_bearish_vol_otm` | 0.7701 | 0 | 0 | Total volume of bearish trades (selling calls and buying p |
| 33 | `customer_bullish_contracts_noto` | 0.7728 | 3 | 2 | Aggregate contracts from buying calls and selling puts by  |
| 34 | `customer_bullish_trade_count` | 0.9058 | 9 | 6 | Number of bullish trades (buying calls and selling puts) b |
| 35 | `customer_bullish_trade_count_ise` | 0.7882 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 36 | `customer_bullish_trade_count_otm` | 0.7701 | 7 | 2 | Number of bullish trades (buying calls and selling puts) b |
| 37 | `customer_bullish_trades_noto` | 0.7728 | 6 | 4 | Number of trades from buying calls and selling puts by cus |
| 38 | `customer_bullish_vol` | 0.9058 | 7 | 7 | Total volume of bullish trades (buying calls and selling p |
| 39 | `customer_bullish_vol_ise` | 0.7882 | 7 | 5 | Total volume of bullish trades (buying calls and selling p |
| 40 | `customer_bullish_vol_otm` | 0.7701 | 4 | 2 | Total volume of bullish trades (buying calls and selling p |
| 41 | `customer_trade_imbalance` | 0.9058 | 108 | 29 | Normalized difference between bullish and bearish trade co |
| 42 | `customer_trade_imbalance_ise` | 0.7882 | 26 | 12 | Normalized difference between bullish and bearish trade co |
| 43 | `customer_trade_imbalance_noto_2` | 0.7728 | 10 | 8 | Normalized difference between bullish and bearish trade co |
| 44 | `customer_trade_imbalance_otm` | 0.7701 | 3 | 3 | Normalized difference between bullish and bearish trade co |
| 45 | `customer_vol_imbalance` | 0.9058 | 89 | 51 | Normalized difference between bullish and bearish trade vo |
| 46 | `customer_vol_imbalance_ise` | 0.7882 | 54 | 40 | Normalized difference between bullish and bearish trade vo |
| 47 | `customer_vol_imbalance_noto` | 0.7728 | 29 | 20 | Normalized difference between bullish and bearish trade vo |
| 48 | `customer_vol_imbalance_otm` | 0.7701 | 3 | 3 | Normalized difference between bullish and bearish trade vo |
| 49 | `firm_bearish_contracts_noto` | 0.7728 | 0 | 0 | Total contracts from selling calls and buying puts by firm |
| 50 | `firm_bearish_trade_count` | 0.9058 | 0 | 0 | Number of trades by firms classified as bearish, i.e., sel |
| 51 | `firm_bearish_trade_count_ise` | 0.7882 | 2 | 2 | Number of bearish trades (selling calls and buying puts) b |
| 52 | `firm_bearish_trade_count_otm` | 0.7701 | 1 | 1 | Number of bearish trades (selling calls and buying puts) b |
| 53 | `firm_bearish_trades_noto` | 0.7728 | 0 | 0 | Number of trades from selling calls and buying puts by fir |
| 54 | `firm_bearish_vol` | 0.9058 | 1 | 1 | Total volume of bearish trades (selling calls and buying p |
| 55 | `firm_bearish_vol_ise` | 0.7882 | 1 | 1 | Total volume of bearish trades (selling calls and buying p |
| 56 | `firm_bearish_vol_otm` | 0.7701 | 1 | 1 | Total volume of bearish trades (selling calls and buying p |
| 57 | `firm_bullish_contracts_noto` | 0.7728 | 1 | 1 | Total contracts from buying calls and selling puts by firm |
| 58 | `firm_bullish_trade_count` | 0.9058 | 2 | 2 | Number of bullish trades (buying calls and selling puts) b |
| 59 | `firm_bullish_trade_count_ise` | 0.7882 | 0 | 0 | Number of bullish trades (buying calls and selling puts) b |
| 60 | `firm_bullish_trade_count_noto` | 0.7728 | 0 | 0 | Number of bullish trades (buying calls and selling puts) b |
| 61 | `firm_bullish_trade_count_otm` | 0.7701 | 0 | 0 | Number of bullish trades (buying calls and selling puts) b |
| 62 | `firm_bullish_vol` | 0.9058 | 2 | 2 | Total volume of bullish trades (buying calls and selling p |
| 63 | `firm_bullish_vol_ise` | 0.7882 | 1 | 1 | Total volume of bullish trades (buying calls and selling p |
| 64 | `firm_bullish_vol_otm` | 0.7701 | 7 | 5 | Total volume of bullish trades (buying calls and selling p |
| 65 | `firm_trade_imbalance` | 0.9058 | 13 | 5 | Normalized difference between bullish and bearish trade co |
| 66 | `firm_trade_imbalance_ise` | 0.7882 | 1 | 1 | Normalized difference between bullish and bearish trade co |
| 67 | `firm_trade_imbalance_noto_2` | 0.7728 | 2 | 1 | Normalized difference between bullish and bearish trade co |
| 68 | `firm_trade_imbalance_otm` | 0.7701 | 1 | 1 | Normalized difference between bullish and bearish trade co |
| 69 | `firm_vol_imbalance` | 0.9058 | 4 | 4 | Normalized difference between bullish and bearish trade vo |
| 70 | `firm_vol_imbalance_ise` | 0.7882 | 3 | 3 | Normalized difference between bullish and bearish trade vo |
| 71 | `firm_vol_imbalance_noto` | 0.7728 | 0 | 0 | Normalized difference between bullish and bearish trade vo |
| 72 | `firm_vol_imbalance_otm` | 0.7701 | 0 | 0 | Normalized difference between bullish and bearish trade vo |
| 73 | `market_maker_bearish_contracts_noto` | 0.7728 | 1 | 1 | Total contracts from selling calls and buying puts by mark |
| 74 | `market_maker_bearish_trade_count` | 0.9058 | 0 | 0 | Number of bearish trades (selling calls and buying puts) b |
| 75 | `market_maker_bearish_trades_noto` | 0.7728 | 0 | 0 | Count of trades from selling calls and buying puts by mark |
| 76 | `market_maker_bearish_vol` | 0.9058 | 14 | 3 | Total volume of bearish trades (selling calls and buying p |
| 77 | `market_maker_bullish_contracts_noto` | 0.7728 | 0 | 0 | Total contracts from buying calls and selling puts by mark |
| 78 | `market_maker_bullish_trade_count` | 0.9058 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 79 | `market_maker_bullish_trade_count_noto` | 0.7728 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 80 | `market_maker_bullish_vol` | 0.9058 | 13 | 2 | Total volume of bullish trades (buying calls and selling p |
| 81 | `market_maker_trade_imbalance` | 0.9058 | 13 | 7 | Normalized difference between bullish and bearish trade co |
| 82 | `market_maker_trade_imbalance_noto_2` | 0.7728 | 6 | 3 | Normalized difference between bullish and bearish trade co |
| 83 | `market_maker_vol_imbalance` | 0.9058 | 23 | 17 | Normalized difference between bullish and bearish trade vo |
| 84 | `market_maker_vol_imbalance_noto_2` | 0.7728 | 14 | 8 | Normalized difference between bullish and bearish contract |
| 85 | `pro_customer_bearish_contracts_noto` | 0.7728 | 0 | 0 | Total contracts from selling calls and buying puts by prof |
| 86 | `pro_customer_bearish_trade_count` | 0.9058 | 5 | 5 | Number of bearish trades (selling calls and buying puts) b |
| 87 | `pro_customer_bearish_trade_count_ise` | 0.7882 | 1 | 1 | Number of bearish trades (selling calls and buying puts) b |
| 88 | `pro_customer_bearish_trade_count_otm` | 0.7701 | 1 | 1 | Number of bearish trades (selling calls and buying puts) b |
| 89 | `pro_customer_bearish_trades_noto` | 0.7728 | 2 | 2 | Number of trades from selling calls and buying puts by pro |
| 90 | `pro_customer_bearish_vol` | 0.9058 | 3 | 3 | Total volume of bearish trades (selling calls and buying p |
| 91 | `pro_customer_bearish_vol_ise` | 0.7882 | 2 | 2 | Total volume of bearish trades (selling calls and buying p |
| 92 | `pro_customer_bearish_vol_otm` | 0.7701 | 0 | 0 | Total volume of bearish trades (selling calls and buying p |
| 93 | `pro_customer_bullish_contracts_noto` | 0.7728 | 2 | 2 | Total contracts from buying calls and selling puts by prof |
| 94 | `pro_customer_bullish_trade_count` | 0.9058 | 4 | 4 | Number of bullish trades (buying calls and selling puts) b |
| 95 | `pro_customer_bullish_trade_count_ise` | 0.7882 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 96 | `pro_customer_bullish_trade_count_otm` | 0.7701 | 0 | 0 | Number of bullish trades (buying calls and selling puts) b |
| 97 | `pro_customer_bullish_trades_noto` | 0.7728 | 0 | 0 | Number of trades from buying calls and selling puts by pro |
| 98 | `pro_customer_bullish_vol` | 0.9058 | 5 | 3 | Total volume of bullish trades (buying calls and selling p |
| 99 | `pro_customer_bullish_vol_ise` | 0.7882 | 1 | 1 | Total volume of bullish trades (buying calls and selling p |
| 100 | `pro_customer_bullish_vol_otm` | 0.7701 | 1 | 1 | Total volume of bullish trades (buying calls and selling p |
| 101 | `pro_customer_trade_imbalance` | 0.9058 | 12 | 7 | Normalized difference between bullish and bearish trade co |
| 102 | `pro_customer_trade_imbalance_ise` | 0.7882 | 5 | 3 | Normalized difference between bullish and bearish trade co |
| 103 | `pro_customer_trade_imbalance_noto_2` | 0.7728 | 0 | 0 | Normalized difference between bullish and bearish trade co |
| 104 | `pro_customer_trade_imbalance_otm` | 0.7701 | 1 | 1 | Normalized difference between bullish and bearish trade co |
| 105 | `pro_customer_vol_imbalance` | 0.9058 | 14 | 12 | Normalized difference between bullish and bearish trade vo |
| 106 | `pro_customer_vol_imbalance_ise` | 0.7882 | 2 | 2 | Normalized difference between bullish and bearish trade vo |
| 107 | `pro_customer_vol_imbalance_noto` | 0.7728 | 0 | 0 | Normalized difference between bullish and bearish trade vo |
| 108 | `pro_customer_vol_imbalance_otm` | 0.7701 | 2 | 1 | Normalized difference between bullish and bearish trade vo |
| 109 | `proprietary_bearish_trade_count` | 0.7882 | 1 | 1 | Number of bearish trades (selling calls and buying puts) b |
| 110 | `proprietary_bearish_trade_count_otm` | 0.7701 | 0 | 0 | Number of bearish trades (selling calls and buying puts) b |
| 111 | `proprietary_bearish_vol` | 0.7882 | 3 | 3 | Total volume of bearish trades (selling calls and buying p |
| 112 | `proprietary_bearish_vol_otm` | 0.7701 | 0 | 0 | Total volume of bearish trades (selling calls and buying p |
| 113 | `proprietary_bullish_trade_count` | 0.7882 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 114 | `proprietary_bullish_trade_count_otm` | 0.7701 | 1 | 1 | Number of bullish trades (buying calls and selling puts) b |
| 115 | `proprietary_bullish_vol` | 0.7882 | 0 | 0 | Total volume of bullish trades (buying calls and selling p |
| 116 | `proprietary_bullish_vol_otm` | 0.7701 | 0 | 0 | Total volume of bullish trades (buying calls and selling p |
| 117 | `proprietary_trade_imbalance` | 0.7882 | 3 | 2 | Normalized difference between bullish and bearish trade co |
| 118 | `proprietary_trade_imbalance_otm` | 0.7701 | 0 | 0 | Normalized difference between bullish and bearish trade co |
| 119 | `proprietary_vol_imbalance` | 0.7882 | 0 | 0 | Normalized difference between bullish and bearish trade vo |
| 120 | `proprietary_vol_imbalance_otm` | 0.7701 | 1 | 1 | Normalized difference between bullish and bearish trade vo |

**ATOM 记账**：120 字段全部非豁免（无 country/exchange/market/sector/industry 字段），全部 MATRIX ⇒ 单字段即可成 ATOM 腿；批次 20 首批覆盖 8 字段（firm/pro/market_maker/broker_dealer/customer-otm 五类 + 一个量门控），剩余分支在后续批次按机制族轮换。

## 2. 字段分型与机制映射

`*_imbalance` 是**已归一化的方向量**（有符号、有界），与 fnd22 的"非负慢变量"相反：**信息每天变，换手天然高**。这决定了本集的主战场是 Change / Surprise / Event-conditioned，而不是 Level。

| 家族 | 字段 | 依据 | 机制 |
|---|---|---|---|
| **Change**（主） | `firm_vol_imbalance`、`pro_customer_vol_imbalance`、`broker_dealer_vol_imbalance`、`customer_vol_imbalance_otm` | 失衡是日内流，自身历史基线可算漂移 | `ts_av_diff(x, 22|66|504)` — 谁在持续加仓方向 |
| **Surprise**（主） | `customer_trade_imbalance_otm`、`pro_customer_vol_imbalance` | 相对自身历史的极端（z / rank） | `ts_zscore(x, 66)` / `ts_rank(x, 252)` — 异常定向押注 |
| **Event-conditioned** | 门控 `customer_bullish_vol`/`firm_bullish_vol` × 信号失衡 | 期权关注度异常日，知情流的信噪比更高 | `trade_when(ts_rank(vol, 252) > 0.8, ts_av_diff(imb, 22), -1)` — 只在事件日交易 |
| **反读（做市商）** | `market_maker_vol_imbalance` | 做市商是**对手盘**，其净看涨往往来自被动对冲，方向需反 | `-1 * ts_rank(x, 252)` |
| **Dispersion** | — | 本集无同公司多值字段，无 `vec_stddev` 可用；跨参与者分歧须两字段差值 ⇒ **暂不作为首批**（避免"混信号"争议，见 §3 约束） | — |

**经济机制假设（可证伪）**：
1. **H1 知情流**：非做市商（firm / pro_customer / broker_dealer）的净看涨失衡漂移，对未来 1–3 月股票收益正向；做市商失衡反向（对手盘）。若 H1 成立，Change 腿应显著且 2Y 稳定。
2. **H2 散户反向**：customer 的价外（`_otm`）投机流是情绪指标，极端处反读。若 H2 成立，z/rank 反号腿应强于正号腿。
3. **H3 事件门控**：上述信号在期权关注度异常日（vol 252d 高分位）才有效——非事件日期权流多为噪声/展期。若 H3 成立，门控腿的 S 应显著高于无条件腿，且换手仍可控。

## 3. 批次 20：预登记（发批前写定，事后不得放宽）

**闸线（USA/D1）**：S ≥ 1.58；F ≥ 1.0；2Y ≥ 1.58；TO ∈ [0.01, 0.70]；SUB ≥ 0.43 × S；CW ≤ 0.1。
**prod**：只在 IS 全过后测（D0-P）；`<0.60` 正常，`0.60–0.70` 不做变体，`0.70–0.75` 只做一次结构化尝试，`≥0.75` 判死。

**本批要回答的问题**：
1. 期权参与者失衡在 USA/TOP3000/D1 上能否产生**换手 > 10%** 的腿？（fnd22 的 1.2–2.9% 是 Fitness 死因，本集必须换出量级）
2. 是否存在**单字段**（非 add、非多信号相加）就能过 S 1.58 的腿？优先在 aC ≤ 23 的冷门分支上找。
3. 做市商反读 / 散户反向这两个方向假设，哪个在平台上被证实？
4. SUB 在 0.77–0.91 覆盖率上是否自然过线（CROWDING 中性化的 SUB 保险是否仍成立）？

**预登记判死线**：若首批 8 条**无一**满足 `S ≥ 1.30 且 F ≥ 0.80`，则判 `order_flow_imb` 首批**无苗**；第二批只做字段轮换（`proprietary_*` / `customer_*_ise` / `firm_*_otm` / 原始量比），不追加壳层；若轮换批仍全灭，则按 8 统计族口径走 `seal_dead_end`（需 forum recon 闸 + 人工确认）。

**约束（用户铁律）**：禁 `add A,B` 混信号与混合权重调参；本批 8 臂全部**单字段主信号**（P4 的 `customer_bullish_vol` 只作 `trade_when` 条件、不参与加权），满足 ATOM。

## 4. 批次 20 回测读数

**发批记录**：A = `2dU3aw9Rv53Qah1QNURMFJy`（P1–P4，SUBINDUSTRY / decay 10 / trunc 0.08 / nanHandling ON / VERIFY）。
发批路径：直连 `BrainApiClient` 先遇 `auth 400/429`（并发会话抢会话），改走 MCP `create_multi_simulation`（复用常驻会话）一次 201。

| 臂 | 机制 | 表达式 | alpha | S | F | 2Y | SUB | TO | RET | 判决 |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | Change | `q(ts_av_diff(customer_vol_imbalance_otm, 22))` | `leMM11l2` | 0.14 | 0.03 | -0.01 | 0.12 | 17.11% | 0.67% | FAIL |
| P2 | Surprise 反号 | `-1 * q(ts_zscore(customer_trade_imbalance_otm, 66))` | `E5VVxxEm` | -0.18 | -0.04 | 0.00 | -0.23 | 16.86% | -0.92% | FAIL |
| P3 | Change | `q(ts_av_diff(firm_vol_imbalance, 66))` | `9qEEkk71` | 0.07 | 0.01 | -0.30 | -0.36 | 17.97% | 0.32% | FAIL |
| P4 | Event-conditioned | `q(trade_when(ts_rank(customer_bullish_vol,252) > 0.8, ts_av_diff(pro_customer_vol_imbalance,22), -1))` | `KPmmZZE8` | 0.18 | 0.04 | 0.24 | -0.14 | 8.51% | 0.51% | FAIL |

B 组（P5–P8，换中性化/decay）待 A 组读数归因后再发，避免同批混入过多设置变量。

### 4.1 A 组归因（先归因，再决定是否发 B 组）

1. **换手闸不是瓶颈**——这是本集相对 fnd22 的唯一好消息。P1–P3 的 TO 落在 16.9–18.0%，P4 的 8.5%，**全部高于 12.5% 的 Fitness 地板**；按 `F = S·sqrt(RET/max(TO,0.125))` 反推，F 值 0.01–0.04 完全由**近零年化收益**（RET 0.32–0.92%）解释，不是被换手压低。⇒ 机制族（Change / Surprise / Event-conditioned）在日频上没有可提取的方向性信息。
2. **符号对称**：P1 (+0.67%) 与 P2 (−0.92%) 是同一族的两侧（P2 为反号），|S| 分别为 0.14 / 0.18，SUB 一正一负 ⇒ 没有稳定方向。样本上 4 条腿的 SUB 有 2 条为负（P2 −0.23 / P3 −0.36 / P4 −0.14），说明信号在 TOP3000 的随机方向上被噪声支配。
3. **覆盖率不背锅**：`_otm`（0.7701）与全量（0.9058）的腿读数同样接近零，说明不是低覆盖导致的有效样本不足。
4. **未测的机制 = Level**：本批四条全在 Change/Surprise 族（对自身的差分/标准化）。文献（Pan & Poteshman 2006；论坛期权帖）主张的**预测力在水平量本身**（put-call 比 / 参与者定向流量的截面高低），而 Level 族在本批一次都没测。按"先归因再推进、不盲扫"的纪律，**B 组不是换中性化，而是补测 Level 族 + 字段轮换**（§5），否则会犯「机制没测完就判死」的错。

## 5. 批次 21：Level 族 + 字段轮换（预登记）

**要回答的问题**：① 水平量（Level）是否比变化量有信息？② 首批未覆盖的 4 个冷分支（`proprietary_*` / `firm_*_otm` / `customer_*_ise` / `market_maker_*_noto_2`）是否有独立信号？

**预登记判死线**：若批次 21 的 8 条**无一**满足 `S ≥ 1.00`（连"可改进的苗子"都不成立），则 `order_flow_imb` 判 **low-yield**，不再投入仿真；`seal_dead_end` 需 forum recon 闸 + 人工确认，本文件只作预登记。

**预算**：2 个 multisim（≤2 并发槽），发批前已过 `preflight_expressions`（8 字段全部 valid，`any_changed=false`）。

### 5.1 A 组：Level 族（SUBINDUSTRY / decay 10 / trunc 0.08）

| 臂 | 机制 | 表达式 | alpha | S | F | 2Y | SUB | TO | RET | risk-neut S | 判决 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | Level | `quantile(group_rank(firm_vol_imbalance, market))` | `e765VEZ6` | 0.16 | 0.03 | -0.23 | -0.11 | 18.15% | 0.77% | **-0.21** | FAIL |
| L2 | Level 平滑 | `quantile(group_rank(ts_mean(pro_customer_vol_imbalance, 22), market))` | `j2eYPOKk` | 0.69 | 0.28 | 1.33 | 0.65 | 7.21% | 2.02% | **-0.01** | FAIL |
| L3 | Level 反读 | `quantile(group_rank(-1 * ts_mean(market_maker_vol_imbalance, 22), market))` | `zqr32e7K` | 0.73 | 0.33 | 0.64 | 0.46 | 8.15% | 2.51% | **0.51** | FAIL |
| L4 | Level 平滑 | `quantile(group_rank(ts_mean(customer_trade_imbalance_ise, 22), market))` | `O0JAMgdq` | 0.66 | 0.28 | 0.07 | 0.45 | 6.88% | 2.20% | **0.57** | FAIL |

- L1 用**原始水平**（不差分、不平滑）：若 Level 族有信息，这是最纯的测法。
- L2/L4 用 22 日平滑压低日噪声——期权参与者流量是月频调仓行为，日频水平多半是噪声。
- L3 是**做市商反读**：做市商净多头暴露高 = 它接的是客户的卖压，未来收益偏负；文献与论坛均有此方向假设。

### 5.2 B 组：字段轮换（CROWDING / decay 10 / trunc 0.08）

| 臂 | 字段（aC） | 表达式 | alpha | S | F | 2Y | SUB | TO | RET | 判决 |
|---|---|---|---|---|---|---|---|---|---|---|
| W1 | `proprietary_vol_imbalance`（0） | `quantile(group_rank(ts_av_diff(proprietary_vol_imbalance, 66), market))` | `6XAdoQYO` | 0.12 | 0.03 | 0.12 | 0.52 | 12.78% | 0.71% | FAIL |
| W2 | `firm_bullish_vol_otm`（7） | `quantile(group_rank(ts_av_diff(firm_bullish_vol_otm, 66), market))` | `GrgWKN3G` | 0.03 | 0.00 | -0.02 | 0.24 | 14.95% | 0.20% | FAIL |
| W3 | `customer_vol_imbalance_ise`（54） | `quantile(group_rank(ts_av_diff(customer_vol_imbalance_ise, 66), market))` | `d5KW36lv` | 0.25 | 0.08 | 0.10 | 0.31 | 14.40% | 1.44% | FAIL |
| W4 | `market_maker_vol_imbalance_noto_2`（14） | `quantile(group_rank(ts_av_diff(market_maker_vol_imbalance_noto_2, 66), market))` | `58jEA1aN` | 0.01 | 0.00 | 0.02 | 0.02 | 13.79% | 0.07% | FAIL |

- W1 是**全表最冷字段**（aC 0）：`proprietary` 自有账户流量，卖方自营的方向性押注，理论上信息含量最高且几乎无人挖。
- W4 用 `_noto`（非 OTM）分支的做市商失衡，与 L3 的全量口径互补。
- 轮换只换字段、壳层与 A 组完全一致（`q(ts_av_diff(...,66))`），保持批次纯度。

### 5.3 批次 21 归因与终判

1. **判死线触发**：批次 21 八条最高 S = **0.73**（L3 做市商反读），低于预登记的 `S ≥ 1.00`「可改进苗子」线；连同批次 20 的 4 条（最高 0.18），本集**全部 12 条腿无一进入低门槛区间**。`order_flow_imb` 判 **low-yield（低产）**，停止投入仿真。
2. **Level ≫ Change 是本集唯一的机制结论**：同一字段族，Level 平滑腿 S 0.66–0.73 vs Change 腿 S 0.01–0.25。这说明期权参与者失衡确实带**水平信息**（与 Pan & Poteshman 2006 的 put-call 比文献一致），但强度上限只有 ~0.7，距 USA/D1 的 1.58 差一半以上 —— 不是壳层或窗口问题，是信号本身的量级不够。
3. **风险中性化证伪了"风格 beta 之外的 alpha"**：L2 全期 S 0.69 但 `risk_neutralized_sharpe = -0.01`（≈ 纯风格 beta）；L3/L4 的 0.51/0.57 算本集最好，仍远低于 1.58。按 `_usa-field-profile-playbook-20261018` 的判死口径（`risk_neutralized_sharpe < 0.3` = 纯风格 beta），L1/L2 属纯 beta，L3/L4 属弱残余。
4. **换手不再背锅但也不再救场**：Level/轮换腿 TO 6.9–15.0%，多数在 12.5% 地板之上，`F` 仍只有 0.00–0.33 ⇒ 收益年化 0.2–2.5% 是硬约束。这与批次 20 归因一致：**问题在收益量级，不在换手**。
5. **`proprietary`（aC 0）并未带来超额**：W1 S 0.12、RET 0.71%。「最冷字段 = 最肥信息」的直觉在本集不成立 —— 冷是因为覆盖口径窄（0.7882）且信号弱，不是被低估。
6. **可复用结论**：期权**参与者分层失衡**在 USA/TOP3000/D1 上只能提供 ~0.7 上限的水平型弱信号，且大部分是风格 beta；要在这个数据集上过 1.58 需要的不只是换壳，缺的是**收益量级**。后续 option 塔若还要挖，应转向 `option3`（20 字段，尚未体检）或期权隐含波动率曲面族，不再回到本集。
7. **封存未执行**：`seal_dead_end` 需 forum recon 闸 + 人工确认，本文件只作预登记；实际状态为「已判 low-yield，不再排仿真」。
