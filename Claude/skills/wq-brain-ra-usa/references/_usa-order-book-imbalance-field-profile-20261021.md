# `order_book_imbalance`（USA / TOP3000 / D1）字段画像与机制档案

as_of 2026-10-21 · 类别 `other`（未点亮塔）· 数据集 id `order_book_imbalance`

## 0. 为什么选它（切换理由，先记录再动手）

`web_traffic_engage` 的水平族已在生产池实测 0.9740 / 0.9906，变化量腿（E8/E10/E7）在测；
在等待平台 prod 期间盘点 USA/D1 未点亮塔剩余集，`order_book_imbalance` 是唯一同时满足
「机制与已交付 5 个方向全部正交 + 字段级 alphaCount 近零 + 论坛实证 SUB 不是瓶颈」的集：

| 判据 | 事实 | 来源 |
|---|---|---|
| 未点亮塔 | `other` 塔本季 USA/D1 无 ACTIVE | 区域面板 |
| 拥挤度 | 198 字段合计 aC **112**（多数单字段 aC = 0–3），uC 77 | `get_datasets` / `get_datafields` |
| 覆盖 | 0.7297（与 pv173 的 0.39 相比不需要激进 backfill） | `get_datasets` |
| 机制正交性 | 订单簿队列/成交概率/拍卖失衡 = **流动性供给方**信息；已交付 5 颗全部是分析师修正、机构持仓、盈利质量类**基本面信息** | — |
| 论坛旁证 | 该族在 GBR/TOP700（n=16）**LOW_SUB 14 PASS**、瓶颈是 LOW_2Y（2 PASS）；另一帖 n=13 同样卡 2Y | 论坛帖 `order_book_imbalance族…` / USA-D1 Power Pool July'26 |
| 风险预判 | 日频微结构量值**持续性高** ⇒ 换手天然低；但 2Y 可能是唯一真墙 | 同上 |

> 注：`order_flow_imb`（机构订单流失衡，论坛「高换手 PPA 首选」）**在 USA/PV 类目下不存在**
> （`get_datasets(category=pv)` 30 集全列，无此 id），不能照搬 PPO 经验。

## 1. 字段画像（198 字段，全部 VECTOR）

平台返回 198 字段，`type` **全部为 VECTOR**（无 MATRIX 标量）。覆盖率集中在 0.718–0.7313。
向量维度未在元数据中声明，按 pv173 教训**必须先用 `vec_avg` vs `vec_max` 对照验多元性**，
不得假定尾部机制可测（pv173 §5 决策第 2 条）。

按机制分六族（含代表字段）：

| 族 | 字段数≈ | 代表字段（cov / aC） | 信息含义 |
|---|---:|---|---|
| **A. 队列事件** | 40 | `bid_order_volume_deleted` 0.7312/6、`ask_order_volume_deleted` 0.7312/8、`bid_order_insertion_count` 0.7312/2、`bid_order_volume_change_modification_2` 0.7303/2 | 挂单/撤单/改单/替换的方向与强度 ⇒ 流动性是**主动撤出**还是**被动成交** |
| **B. 成交概率与驻留时间** | 50 | `fill_prob_bid_lvl1` 0.7311/3、`fill_prob_ask_lvl1` 0.7311/3、`avg_rest_time_bid_filled_lvl1` 0.7310/1 | 哪一侧挂单更易被吃 ⇒ 逆向选择方向（VPIN 同源） |
| **C. 深度 / 展示流动性** | 40 | `twa_notional_bid_5_levels` 0.7312/0、`twa_notional_ask_5_levels` 0.7312/0、`twa_share_count_*_{1..5}_levels`、`*_10/30/50bps` | 买卖两侧深度差 ⇒ 价格压力（经典 OBI） |
| **D. 成交分类** | 20 | `dark_trade_volume` 0.7313/4、`lit_trade_volume` 0.7313/2、`bilateral_trade_volume` 0.7313/0、`bid_trade_imbalance_all_levels` 0.7311/1 | 暗池/明池结构、主动成交的跨档分布 ⇒ 知情交易占比 |
| **E. 拍卖** | 7 | `auction_order_imbalance_pct_adv` 0.7209/8、`closing_auction_dislocation_last` 0.721/1、`auction_order_imbalance_absolute` 0.7209/3 | 收盘集合竞价的**未成交超额**与价格偏移 ⇒ 隔夜需求压力/反转 |
| **F. 价差与冲击** | 25 | `time_weighted_spread_bps` 0.7312/0、`trade_market_impact_coefficient` 0.7305/0、`quote_to_trade_ratio` 0.7312/3、`intraday_price_volatility` 0.7312/2 | 交易成本、价格冲击、幻影流动性 ⇒ 流动性溢价与拥挤度 |

**可用性注记**

- 覆盖率 0.72–0.73 ⇒ 约 2200/3000 只可交易；低于 0.4 的强制 `ts_backfill` 规则在本集不触发，
  但仍统一加 `ts_backfill(..., 120)` 防单点空洞。
- `final_midpoint_price` / `opening_midpoint_price` / `lowest_midpoint_price` / `max_midpoint_price_daily`
  是**价格水平**，不是信号；只在份额/深度归一化时作分母，不单独入批。
- `volume_weighted_avg_trade_price` / `time_weighted_avg_trade_price` 与 pv1 的 VWAP/TWAP 同源，
  **不与 pv1 组合**（禁混信号 + 已高度拥挤）。

## 2. 机制目录（9 条，每条一个可证伪假设）

| # | 机制 | 公式骨架（信号部分） | 方向 | 经济学依据 |
|---|---|---|---|---|
| M1 | **拍卖失衡延续** | `vec_avg(auction_order_imbalance_pct_adv)` | + | 收盘未成交买单堆积 ⇒ 隔夜/次日仍有需求 |
| M2 | **拍卖位移反转** | `-vec_avg(closing_auction_dislocation_last)` | − | 收盘被推高的价格次日回吐（流动性冲击） |
| M3 | **深度失衡** | `(bid5 − ask5)/(bid5 + ask5)`，`twa_notional_*_5_levels` | + | 买侧更深 ⇒ 卖方需让价，价格上行压力 |
| M4 | **成交概率不对称** | `-(fill_prob_bid_lvl1 − fill_prob_ask_lvl1)` | − | 买挂单更易成交 = 卖方主动 ⇒ 看跌 |
| M5 | **撤单方向** | `-(bid_deleted − ask_deleted)/(bid+ask)` | − | 买方撤单 = 需求撤出 ⇒ 看跌 |
| M6 | **价格冲击/非流动性** | `vec_avg(trade_market_impact_coefficient)` | + | 非流动性溢价（Amihud 同族） |
| M7 | **暗池份额** | `dark/(lit+dark)` | ? | 知情交易者偏好暗池 ⇒ 方向待测（先按水平） |
| M8 | **幻影流动性** | `-vec_avg(quote_to_trade_ratio)` | − | 报价多成交少 = 挂单不可信 ⇒ 后续波动/回撤 |
| M9 | **拍卖意外** | `auction_imb − ts_mean(auction_imb, 22)` | + | 相对自身基线的意外需求冲击 |
| M10 | **尾部口径对照** | 同 M3 但用 `vec_max` | + | 同时验证「向量是否真多元」 |

**统一壳**（与 web_traffic / stock_search 批次一致，保证跨集可比）：

```
quantile(group_rank(winsorize(ts_backfill(<SIG>, 120), std=4), industry))
```

`SIG` 为 `ts_zscore(<原始信号>, 22)`；M9 已含时序差分，不再套 z-score。

## 3. 预注册止损（动手前写死，防止事后找理由）

1. **族级死**：10 条探针若 8 条以上 `|S| < 0.5` ⇒ 记 `USA-OBI-WEAK`，不开第二批。
2. **风格 beta 死**：任一条 S ≥ 1.0 但 `risk_neutralized_sharpe < 0.3` ⇒ 该族判纯风格 beta（与 pv173 同口径）。
3. **2Y 单墙**：若多数条 S ≥ 1.5 / F ≥ 1.0 而 2Y < 1.2 ⇒ 按「慢变量」处理，只加 `ts_mean(·, 5)` 或
   `ts_decay_linear` 一种杠杆，不跨族重扫（论坛已两次提示该族卡 2Y）。
4. **prod 判死**：任一条过 IS 全闸后 `check_correlation(refresh=True)` ≥ 0.75 ⇒ 按 D0-P 判 `dead_end`，
   且若同族再有第二条 ≥ 0.75 ⇒ 升级为**机制级** `USA-OBI-PROD-SAT`，整集封存。

## 3.5 探针批（已派发）

- multisim：`1NlnUJ5Pw4YLbeNhMbjg4Dt`（2026-10-21 派发，USA/D1/TOP3000/SUBINDUSTRY/decay 5/trunc 0.08/VERIFY/nan ON/pasteurization ON/maxTrade OFF）
- 预检：`preflight_expressions` 12 个数据字段全部识别；唯一 `unknown_fields=["std"]` 是 `winsorize(..., std=4)` 命名参数的**已知误报**，`any_changed=false`。

| # | 机制 | 信号（SIG，进统一壳前） |
|---|---|---|
| E1 | M1 拍卖失衡延续 | `ts_zscore(vec_avg(auction_order_imbalance_pct_adv), 22)` |
| E2 | M2 拍卖位移反转 | `ts_zscore(-vec_avg(closing_auction_dislocation_last), 22)` |
| E3 | M3 深度失衡 | `ts_zscore((B5−A5)/(B5+A5), 22)`，B5/A5 = `vec_avg(twa_notional_{bid,ask}_5_levels)` | <!-- lint:counterexample: 比率分母，买卖/正负两侧合计，非信号腿相加 -->
| E4 | M4 成交概率不对称 | `ts_zscore(-(vec_avg(fill_prob_bid_lvl1)−vec_avg(fill_prob_ask_lvl1)), 22)` |
| E5 | M5 撤单方向 | `ts_zscore(-(D_b−D_a)/(D_b+D_a), 22)`，D = `vec_avg({bid,ask}_order_volume_deleted)` | <!-- lint:counterexample: 比率分母，买卖/正负两侧合计，非信号腿相加 -->
| E6 | M6 价格冲击 | `ts_zscore(vec_avg(trade_market_impact_coefficient), 22)` |
| E7 | M7 暗池份额 | `ts_zscore(vec_avg(dark)/(vec_avg(dark)+vec_avg(lit)), 22)` | <!-- lint:counterexample: 比率分母，买卖/正负两侧合计，非信号腿相加 -->
| E8 | M8 幻影流动性 | `ts_zscore(-vec_avg(quote_to_trade_ratio), 22)` |
| E9 | M9 拍卖意外 | `vec_avg(auction_order_imbalance_pct_adv) − ts_mean(..., 22)`（**不套外 z-score**） |
| E10 | M10 尾部口径对照 | 同 M3 但两腿改 `vec_max`（验向量多元性） |

## 4. 探针批结果

### 4.1 全批指标（2026-10-21，multisim `1NlnUJ5Pw4YLbeNhMbjg4Dt`，10/10 COMPLETE）

| # | alpha | S | F | TO | SUB | 2Y | rns | 未过闸 | 读法 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| E1 | `j2e8wRYe` | 1.77 | 1.09 | 26.5% | 0.40 | 0.96 | 2.59 | SUB / 2Y | 拍卖失衡水平，两墙 |
| E2 | `LL5ZXaKe` | 2.03 | 1.29 | 28.3% | 0.50 | 1.03 | 2.81 | SUB / 2Y | 拍卖位移反转，本批第二高 S |
| E3 | `JjPQXE8e` | 1.90 | 1.22 | 25.1% | 0.59 | 0.86 | 2.75 | SUB / 2Y | 深度失衡 |
| E4 | `78o6XbG8` | 1.91 | 1.18 | 27.5% | 0.55 | 1.12 | 2.76 | SUB / 2Y | 成交概率不对称 |
| E5 | `9qEW61GK` | 1.91 | 1.20 | 25.2% | 0.46 | 0.86 | 2.62 | SUB / 2Y | 撤单方向 |
| E6 | `WjLeXQYP` | 1.93 | 1.44 | **16.7%** | 0.68 | 1.09 | 2.76 | SUB / 2Y（+CLUSTER 1.55 警告） | 价格冲击，换手最低 |
| **E7** | **`j2e8wRVk`** | **2.21** | **1.47** | 27.2% | **0.96 ✅** | **1.28** | 2.82 | **仅 2Y** | **暗池份额，唯一 SUB 过闸** |
| E8 | `vRO2zMZd` | 1.88 | 1.17 | 26.1% | 0.58 | 0.93 | 2.46 | SUB / 2Y | 幻影流动性 |
| E9 | `P0MglaxK` | 1.80 | 1.14 | 25.1% | 0.49 | 0.90 | 2.59 | SUB / 2Y | 拍卖意外 |
| E10 | `2rjmZzXP` | 1.87 | 1.17 | 26.2% | 0.61 | 0.77 | 2.69 | SUB / 2Y | `vec_max` 对照 |

### 4.2 归因（先归因再扩批）

1. **族不是弱族，也不是风格 beta**：10/10 `S ≥ 1.77`、`F ≥ 1.09`、`rns 2.46–2.82`。
   预注册止损 §3.1（8 条 |S|<0.5）与 §3.2（rns<0.3）**均未触发**。
2. **2Y 是共性墙，不是个别构造**：10/10 未过（0.77–1.28 vs 1.58），且与方向无关
   （E2 反转、E1 水平、E7 份额全中）。命中预注册 §3.3 的「慢变量」条款。
3. **SUB 是第二共性墙**：9/10 未过，缺口 0.35–0.47（E1 最差 0.40 vs 0.77）。
   **E7 是唯一例外（0.96 vs 0.97 极限过闸）**，且它的 TO（27%）不是本批最低 ⇒
   SUB 不由换手单独决定，与「暗池份额只由知情交易者结构驱动」的横截面分布有关。
4. **`vec_max` 对照（E10）与 `vec_avg`（E3）差 0.03 S / 0.09 SUB / 0.09 2Y**：
   两者形态接近 ⇒ 该集向量尾部信息不占主导，后续统一用 `vec_avg`，不单独开发尾部机制。
5. **方向可证伪性成立**：E2 反号（拍卖位移反转）S 2.03 与 E1 正号（拍卖失衡延续）S 1.77 同向为正，
   说明两者不是同一枚硬币的两面，各自捕捉收盘竞价的「价格位移」与「未成交需求」。

### 4.3 下一步（按决策）

- **prod-first**：先测 E7（唯一 SUB 过闸、S 最高）的 prod。≥0.75 ⇒ 按 D0-P 判该机制 `dead_end`；
  <0.75 ⇒ 走 §3.3 唯一杠杆（`ts_mean(·,5)` 或 `ts_decay_linear`）修 2Y，同时给 E6（SUB 最近）配同杠杆。
- 不在本集引入新机制族：§3.3 明确「不跨族重扫」；若慢变量后 2Y 仍 < 1.2，再按 §3.1 判族级边界。

### 4.4 唯一杠杆批（2026-10-21，multisim `358nA23Ar4ybaY9qrCrkDoe`，8/8 COMPLETE）

按 §3.3 只上**一类**慢变量杠杆（`ts_mean(·,5)` / `ts_decay_linear(·,5)`），不跨族重扫。
设置同 §3.5（USA/TOP3000/D1/SUBINDUSTRY/decay 5/trunc 0.08）。

| 原型 | alpha | S | F | TO | SUB（限≈0.43·S） | 2Y | 读法 |
|---|---|---:|---:|---:|---:|---:|---|
| E7 | **`YPxMWpLo`** | **2.24** | **1.68** | 18.71% | **1.03 ✅** | **1.42**（差 0.16） | 全批最优；S/F/SUB/TO 全过，**仅 2Y** |
| E7 | `RRA6kpMd` | 2.22 | 1.61 | 20.30% | 1.02 ✅ | 1.41 | 与最优同量级（杠杆档不同） |
| E6 | `P0MgXpNx` | 1.91 | 1.54 | 13.36% | 0.71 ❌ | 1.01 | 冲击族 SUB 仍差 0.11 |
| E6 | `j2e8dZEE` | 1.95 | 1.56 | 14.55% | 0.66 ❌ | 1.07 | 同上 |
| E2 | `xA1bmx6l` | 2.01 | 1.38 | 20.15% | 0.47 ❌ | 1.03 | 拍卖位移 SUB 0.47 vs 0.86 |
| E2 | `wp9bJRx1` | 2.02 | 1.36 | 22.21% | 0.42 ❌ | 0.98 | 同上 |
| E4 | `9qEWAw1d` | 1.85 | 1.35 | 17.03% | 0.54 ❌ | 1.00 | 成交概率不对称 |
| E1 | `j2e8dZb9` | 1.89 | 1.29 | 19.53% | 0.59 ❌ | 1.16 | 拍卖失衡水平 |

**杠杆有效性（预注册条款的判定依据）**：E7 从 `2.21 / 1.47 / 27.2% / 0.96 / 1.28` 变为
`2.24 / 1.68 / 18.71% / 1.03 / 1.42` ——**F +0.21、TO −8.5pt、SUB 更稳、2Y +0.14**，
但 2Y 仍差 **0.16**。⇒ 杠杆方向正确、幅度不足；按 §3.3「只上一种杠杆」的预注册约束，
**不再叠第二类杠杆**（叠加即进入磨参数）。

**prod 实测（决定性）**：E7 原型 `j2e8wRVk` ⇒ **prod max = 0.8808**（`logs/_tmp_prodcheck_web_traffic.py`
直连 `get_production_correlation`，2026-10-21）。按 D0-P（prod ≥ 0.75 ⇒ `dead_end`），
**暗池份额机制判死**；平滑杠杆只改 2Y、不改与生产池的暴露，故 `YPxMWpLo` 不必再烧一次 prod 配额。

### 4.5 数据集裁定：`USA-OBI-PROD-SAT`（封存）

- **IS 层**：本集是全季少见的「真信号族」——10 条探针 `S 1.77–2.21`、`rns 2.46–2.82`（剥离风格后仍有 2.5+），
  完全排除风格 beta；2Y 是共性墙，但已证明**可被单一慢变量杠杆推进 0.14**。
- **prod 层**：E7 0.8808、`[0.7,0.8)` 桶有量（前批同族 n=70 / n=36），按 D0-P 与
  `wq-window-valley-break-prod-wall`「n≥1 必死」⇒ **机制级饱和，不是单条构造问题**。
- **裁定**：`order_book_imbalance` 整集封存（等同 `USA-OBI-PROD-SAT`）。**不发第 3 批、不做 Mode A**。
  IS 强候选 `YPxMWpLo` / `RRA6kpMd`（2Y 1.42，**仅差 0.16**）登记为 **SUPER 组合腿候选**——
  组合层的 prod 由合成结果决定，不受单条 0.88 的约束。
- **可复用结论**：① 暗池份额（dark/(dark+lit)）是订单簿族里唯一能**同时**过 SUB 与 S 的构造，
  因为它的横截面由知情交易者结构驱动、不只由流动性驱动；② SUB 墙在本集不是换手函数
  （E7 TO 27% 反而过、E6 TO 16.7% 反而不过）；③ 「prod-first」应放在**慢变量杠杆之前**测，
  本轮顺序反了（先做了 8 条杠杆批才发现 prod 0.88），代价是一批仿真。
