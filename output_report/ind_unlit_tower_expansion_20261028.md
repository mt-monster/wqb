# IND 未点亮塔覆盖扩展（2026-10-28）

> 报告类型：战役产物（挖掘覆盖与实证汇总）
> 口径：IND / D1 / TOP500，平台 `get_pyramid_alphas()` 当季默认
> 引擎：**MCP 全链**（`create_multi_simulation` 派发 → `harvest_multisim_alphas` 收割 → `wqb_db.upsert_backtest_rows` 入库；prod 只用 `check_correlation`）
> 本报告不含任何提交动作；所有 alpha 均保持 `UNSUBMITTED`。

---

## 1. 目标与塔位盘点

需求：对 IND 当季未点亮塔继续挖掘，**每塔尽量 ≥10 颗 regular alpha，ATOM 优先**。

当季塔位（`get_pyramid_alphas()`）：

| 类型 | 塔 | 起点 |
|---|---|---|
| 未点亮（0 颗） | INSIDERS / IMBALANCE / OPTION / SENTIMENT / SHORTINTEREST | 0 |
| 未满 | MACRO(2) / EARNINGS(1) / INSTITUTIONS(1) / RISK(3) | — |

本轮把「未点亮 + 未满」共 9 个塔纳入覆盖，波次号：`unlit28`（第一波）、`unlit28b`（MCP 直发批）。

---

## 2. 挖掘总量

| 指标 | 数值 |
|---|---|
| 回测行入库 | **67**（unlit28 = 39，unlit28b = 28；库内逐数据集核对） |
| 入选字段来源数据集 | 14 个（risk68/risk70/institutions6/sentiment21/sentiment26/earnings3/earnings6/earnings11/insiders1/option1/option30/imbalance5/macro63/shortinterest5） |
| 平台批次 | 第一波 19 批（临时 runner） + MCP 批 9 批（L2-A…L2-I） |
| ATOM（`pyramids.effective == 1`） | **17 行，其中有效 15 行**：OPTION 6 / EARNINGS 6（4 有效、2 颗 `bookSize=0` 无效）/ SENTIMENT 2 / INSTITUTIONS 2 / IMBALANCE 1 |

> 说明：第一波（39 行）由临时 runner 派发，之后按用户指令整体切换到 MCP 引擎；L2 全部批次由 MCP 派发、MCP 收割、MCP 入库，未再新建临时回测脚本。

### 2.1 MCP 引擎切换的等价性核验

切换时实测 MCP 派发的 alpha `settings` 回显：

```
startDate 2014-01-01 / endDate 2023-12-31 / simulationMode FULL
```

与旧临时脚本显式钉住的窗口**逐字段一致**，因此两波结果可直接合并比较，不需要重跑。

---

## 3. 逐塔覆盖与最佳候选

`ra` = `ra.failed_ra_count`（0 = 平台 RA 硬闸全过）。`eff` = `pyramids.effective`。

| 塔 | 已挖 | ra=0 | ATOM | 最佳候选（S / F / TO / 2Y / sub / rob） | 判定 |
|---|---|---|---|---|---|
| RISK | 11 | 2 | 0（本波） | `RREQ5len` 2.27 / 1.52 / 0.228 / 2.60 / 1.18 / 1.60；`QPYx8wWX` 1.85 / 1.22 / 0.199 / 2.98 / 1.64 / 1.71 | 全闸过但 eff=2（pv/risk）非 ATOM；且 risk 族互相关墙（历史实测最大可共存子集仍为 `58EbwZeN`+`88RoVq6V`） |
| INSIDERS | 10 | 0 | 0 | `88R90qk7` 1.59 / 1.11 / 0.175 / 1.44 / 1.09 / 1.08（ra=1，仅 `IS_LADDER_SHARPE`） | 最接近可交付；差 2Y 0.14 |
| INSTITUTIONS | 10 | 4 | **2** | `npvRmKq3` 3.00 / 2.25 / 0.246 / 2.70 / 1.38 / 1.60；`kqNrvwA8` 2.92 / 2.18 / 0.242 / 2.83 / 1.57 / 1.35（均 eff=2）；ATOM：`qMLoZ332` 0.72 / 0.41、`GrWpvxxx` −0.03 / −0.01 | 已挖 10；4 颗 ra=0 全为组腿（eff=2），ATOM 形态可达但 institutions6 饱和 12378、单字段信号弱 |
| SENTIMENT | 10 | 0 | **2** | `O0APzLmJ` 1.43 / 0.95 / 0.083 / 2.03 / 0.91 / 0.55（ra=3）；ATOM: `pwdAOeJv` 0.07 / 0.01（2Y 1.32） | robust 0.55 是主瓶颈；注意力类 ATOM 覆盖 0.53、S≈0 |
| EARNINGS | 12 | 0 | 6（4 有效） | `E56Wx5J1` 1.15 / 0.73 / 0.140 / 1.33 / 1.26 / 1.06（ra=3）；ATOM 最强 `QPvLrp7w` 0.43 / 0.17（rob 0.49 / sub 0.37，四项闸全在但都不够） | 已挖 12（10 有效）；rob 已过、卡 S/F/2Y 三项；earnings6 EPS 两臂 `bookSize=0`（向量在 IND 无值，ATOM 空转） |
| OPTION | 10 | 0 | **6** | `9qxLYk1q` 1.03 / 0.59 / 0.154 / 0.91 / 1.31 / **1.13**（rob 过闸）；ATOM: `0mY03Xak` 0.44 / 0.13、`KPJjx8rl` 0.32 / 0.07、`pwdAO53X` 0.21 / 0.07、`9qxL1jke` 0.12 / 0.02、`wpQMXzb5` −0.29 / −0.07、`d5WAL1vY` −0.60 / −0.24 | 已挖 10（option1 8 + option30 2）；rob 门槛首次在 OPTION 打开；ATOM 稳定可达（6 颗 eff=1），但期权面字段横截面区分度不足（§4.3） |
| IMBALANCE | 2 | 0 | 1 | `KPJjPGV8` 2.09 / 1.66 / 0.150 / 1.63 / 1.04 / **0.41**（ra=2：`CONCENTRATED_WEIGHT` + `LOW_ROBUST`） | 全塔最强信号，rob 是唯一实质墙 |
| SHORTINTEREST | 1 | 0 | 0 | `wpQMpaNQ` S=0 / bookSize=20M（零收益） | 字段结构性无信号（见 §5） |
| MACRO | 1 | 0 | 0 | `qMLo99Pv` S=0 / 零收益 | 字段结构性无信号（见 §5） |

---

## 4. 关键实证

### 4.1 ATOM 不是可迁移的几何，而是字段属性

`58EbwZeN`（`rsk68_residual_return`，Form D+hump，decay 6）是已验证的 IND ATOM 全闸成品（S 2.76 / F 1.76 / TO 0.2728 / 2Y 2.48 / sub 1.30 / rob 1.05 / eff=1）。

本轮把同一几何（`ts_target_tvr_hump(..., target_tvr=0.38)`）迁移到其它塔的字段，**全部失败**：

| 目标字段 | 塔 | decay | S | 结论 |
|---|---|---|---|---|
| `sector_relative_momentum` | RISK(risk70) | 126 / 6 | −1.37 / −1.10 | 不可迁移 |
| `hedge_fund_ownership_percentage` | RISK(risk70) | 126 / 6 | −0.23 / −0.09 | 不可迁移 |
| `snt21_pos_mean` / 极性比 | SENTIMENT | 6 | 0.54 / 0.61 | 不可迁移 |
| `imb5_score` | IMBALANCE | 6 | −2.36 | 不可迁移（同字段的 `ts_rank` 反而 S=2.09） |
| `mcr63_membership` | MACRO | 6 | 0.00 | 字段无信号 |

⇒ 结论：**Form D+hump 只在「字段本身即残差收益型」时成立**；换塔必须重新找机制，不能复用几何。

### 4.2 Form E 结构上必非 ATOM

`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(F,252), 252, rettype=0))` 把 `returns` 作为因变量 ⇒ 计入 PV 塔 ⇒ `effective=2`。本轮 6 条 ra=0 的 Form E 结果（`RREQ5len` / `QPYx8wWX` / `npvRmKq3` / `VkddekVJ` / `kqNrvwA8` / `pwvJebEX`）**逐条实测 eff=2**，只能作组腿备选，不满足 ATOM 优先口径。

### 4.3 OPTION / SENTIMENT / INSTITUTIONS：rob 墙被 Form E 首次打开，ATOM 由单数据集 pf 形态确证

| alpha | 表达式 | eff | S | F | TO | 2Y | sub | rob | ra |
|---|---|---|---|---|---|---|---|---|---|
| `9qxLYk1q` | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(ts_backfill(vec_avg(option_implied_volatility_value),252),252),252,rettype=0))` | 2 | 1.03 | 0.59 | 0.154 | 0.91 | 1.31 | **1.13** | 3 |
| `3qoZwJrz` | 同上，字段换 `opt1_p_deltasurface_d1_vi` | 2 | 1.01 | 0.56 | 0.156 | 1.12 | 1.11 | **1.03** | 3 |
| `0mY03Xak` | `ts_rank(ts_backfill(divide(vec_avg(opt1_forward_price_d1_forward), add(vec_avg(opt1_price_close),1)),252),252)` | **1** | 0.44 | 0.13 | 0.328 | 1.07 | 0.05 | 0.06 | 5 |
| `9qxL1jke` | `-ts_rank(ts_backfill(vec_avg(delta_surface_data_quality),252),252)` | **1** | 0.12 | 0.02 | 0.379 | −0.19 | 0.24 | 0.12 | 5 |
| `pwdAO53X` | `ts_rank(ts_backfill(vec_avg(option_open_interest_contracts),504),504)` | **1** | 0.21 | 0.07 | 0.114 | 0.34 | 0.30 | 0.30 | 4 |
| `d5WAL1vY` | `ts_rank(ts_backfill(vec_avg(option_daily_traded_contracts),252),252)` | **1** | −0.60 | −0.24 | 0.268 | −0.18 | −0.48 | −0.32 | 5 |
| `KPJjx8rl` | `ts_rank(ts_backfill(vec_avg(implied_yield_value),252),252)` | **1** | 0.32 | 0.07 | 0.415 | −0.20 | 0.20 | −0.06 | 5 |
| `wpQMXzb5` | `ts_rank(ts_backfill(divide(vec_avg(opt1_price_high),add(vec_avg(opt1_price_low),1)),252),252)` | **1** | −0.29 | −0.07 | 0.440 | 0.30 | −0.05 | 0.07 | 5 |

同步在 SENTIMENT 塔拿到 2 颗 ATOM（`sentiment26` 注意力，覆盖率 0.53，eff=1）：

| alpha | 表达式 | eff | S | F | TO | 2Y | sub | rob | ra |
|---|---|---|---|---|---|---|---|---|---|
| `pwdAOeJv` | `ts_rank(ts_backfill(vec_avg(snt26_relpopularity1),252),252)` | **1** | 0.07 | 0.01 | 0.160 | 1.32 | −0.14 | −0.22 | 5 |
| `O0AEaXqY` | `ts_delta(ts_backfill(vec_avg(snt26_relpopularity1),252),63)` | **1** | 0.01 | 0.00 | 0.306 | 0.03 | 0.15 | 0.16 | 5 |

INSTITUTIONS 塔（`institutions6`，覆盖率 0.60~0.99）同形态拿到 2 颗 ATOM：

| alpha | 表达式 | eff | S | F | TO | 2Y | sub | rob | ra |
|---|---|---|---|---|---|---|---|---|---|
| `qMLoZ332` | `ts_rank(count_institutional_holders_security, 252)` | **1** | 0.72 | 0.41 | 0.052 | 0.20 | 0.57 | 0.22 | 4 |
| `GrWpvxxx` | `ts_rank(divide(subtract(acquired, disposed), add(add(acquired, disposed), 1)), 252)`（机构买入/卖出净额占比） | **1** | −0.03 | −0.01 | 0.105 | −0.09 | 0.21 | 0.24 | 4 |

> `GrWpvxxx` 带 `UNITS` warning（价格单位与无量纲常数相加），**非致命**：alpha 仍 COMPLETE。后续同类净额比应写成 `add(abs(a), abs(b))` 让单位相消。
> 与 OPTION 不同，INSTITUTIONS 的 ATOM 不缺覆盖率（`count_institutional_holders_security` 覆盖近 1.0），缺的是**信号强度**：该塔 4 颗 ra=0 的高分候选（S 2.9~3.0）全部依赖 `returns` 做回归（Form E，eff=2）。

解读：OPTION 数据的覆盖率只有 0.34~0.52。L2-G 专门挑了高覆盖字段（`opt1_price_high` / `opt1_price_low`，覆盖 0.5177）验证「覆盖压制论」，结果是**覆盖率不是约束**：S 仍是 −0.29，换手反而升到 0.44（新增 `HIGH_TURNOVER` 失败项）。同塔 `9qxLYk1q` 的 rob 越过 1.0 说明 rob 可破，真正缺的是 S —— 期权面字段（IV / 远期基差 / 股息率 / 高低比）在 IND 的横截面区分度不足以撑起 1.58 Sharpe。ATOM 形态（纯 option 字段、无 `returns`）已 6 次复现 `eff=1`，**继续加同塔 ATOM 只会增加低 S 样本，不改变上限**。

### 4.4 IMBALANCE：本轮最强单塔信号

`KPJjPGV8 = ts_rank(imb5_score, 252)`（decay 6 / INDUSTRY）：

```
S 2.09 / F 1.66 / TO 0.1501 / 2Y 1.63 / sub 1.04 / rob 0.41 / eff=1 / ra=2
失败项：CONCENTRATED_WEIGHT、LOW_ROBUST_UNIVERSE_SHARPE
risk_neutralized_sharpe = 1.8
```

同一字段的 Form D+hump 变体为 −2.36（见 §4.1），说明该字段的 alpha 方向就是「高 resilience 分数的横截面排序」，不需要再加平滑/动量变换。**这是 IND 未点亮塔里唯一一颗 ATOM 且指标接近全闸的候选**，rob 0.41 是唯一实质墙。

### 4.5 近闸候选清单（未提交，仅记录）

| alpha | 塔 | 差什么 |
|---|---|---|
| `88R90qk7` | INSIDERS | 仅 `IS_LADDER_SHARPE`（2Y 1.44 < 1.58），S/F/sub/rob 全过 |
| `KPJjPGV8` | IMBALANCE | `LOW_ROBUST` 0.41 + `CONCENTRATED_WEIGHT` |
| `E56Wx5J1` | EARNINGS | S/F/2Y 三项（rob 1.06 已过） |
| `9qxLYk1q` / `3qoZwJrz` | OPTION | S/F/2Y（rob 已过） |

### 4.6 EARNINGS 补位（L2-H / L2-I）：4 颗 ATOM 全弱，但确认塔内 ATOM 密度

为把 EARNINGS 从 8 行补到 10 行有效，用 `earnings11`（RavenPack，cov 0.4992，映射 `IND/D1/EARNINGS`）连发两批 4 臂，全部 `eff=1`：

| alpha | 表达式 | eff | S | F | TO | 2Y | sub | rob | ra |
|---|---|---|---|---|---|---|---|---|---|
| `QPvLrp7w` | `ts_rank(ts_backfill(vec_avg(ern11_document_sentiment),252),252)` | **1** | 0.43 | 0.17 | 0.078 | 0.14 | 0.37 | 0.49 | 4 |
| `pwdAJeP6` | `ts_rank(ts_backfill(vec_avg(ern11_event_risk),252),252)` | **1** | −0.45 | −0.20 | 0.059 | 0.12 | −0.57 | −0.46 | 5 |
| `Xg95PKK1` | `ts_rank(ts_backfill(vec_avg(ern11_sentiment_impact_projection),252),252)` | **1** | 0.21 | 0.06 | 0.082 | 0.02 | −0.09 | 0.22 | 5 |
| `78LE0ddL` | `ts_rank(ts_backfill(vec_avg(ern11_event_similarity_days),252),252)` | **1** | −0.21 | −0.06 | 0.074 | −0.61 | −0.28 | −0.10 | 5 |

解读：`ern11_*` 的 35 个字段里，**情绪/事件类单字段 rank 全部落在 |S| ≤ 0.45**；同一批字段放进 Form E（`returns` 做因变量）能到 S 1.15（`E56Wx5J1`）。这与 OPTION / INSTITUTIONS 的结论完全同构 —— **ATOM 是字段属性，强度是几何属性**。

---

## 5. 塔的结构性上限（证据化结论）

「每塔 ≥10 颗」在以下三塔**物理上不可达**，依据是平台数据集目录（`get_datasets` / `get_datafields`，IND/D1/TOP500）。

当季复核（2026-10-28 实测）：`get_datasets(region="IND", delay=1, universe="TOP500")` 返回 **64 个数据集**，其中 `category=macro` 只有 `macro63`（fieldCount 1）、`category=shortinterest` 只有 `shortinterest5`（3）、`category=imbalance` 只有 `imbalance5`（2）——这三塔在平台目录里**各只有 1 个数据集**，没有任何未探索的替代来源。同一时点 `get_pyramid_alphas({})` 的 IND/D1 塔位为 `{insiders:0, news:4, other:4, pv:8, analyst:3, model:3, macro:2, imbalance:0, fundamental:3, option:0, sentiment:0, shortinterest:0, earnings:1, risk:3, institutions:1}`，其中 option / sentiment / shortinterest / insiders / imbalance 仍为 0（本轮产出未改变当季快照），macro 2 / earnings 1 / risk 3 / institutions 1 未满。

| 塔 | 可用数据集 | 字段数 | 实证 |
|---|---|---|---|
| MACRO | `macro63`（唯一） | **1**（`mcr63_membership`） | 两次回测（rank / Form D+hump）全部 S=0、bookSize 20M 无收益 ⇒ 该字段对个股无区分度 |
| SHORTINTEREST | `shortinterest5`（唯一） | **3**（涨跌停比例×2 + 交易状态码） | `max_price_increase_ratio` 两次回测 S=0；涨跌停比例是交易所规则常数，个股间近似常量 ⇒ 无时序信号 |
| IMBALANCE | `imbalance5`（唯一） | **2**（`imb5_score`、`imb5_mktcap`） | `imb5_score` 有信号（S=2.09），`imb5_mktcap` 是市值本身（等价于 PV 市值因子，非本塔信号） |
| EARNINGS（部分） | `earnings6`（3 个数据集之一） | 20 | 两个 EPS 向量字段（`ern6_actual_eps` / `ern6_estimated_eps`）回测 `bookSize=0`、`LOW_TURNOVER=0` ⇒ 在 IND 无有效值；该数据集只剩日期/分红类事件字段，实用价值为零 |

⇒ MACRO / SHORTINTEREST / IMBALANCE 三塔的覆盖上限分别是 **1 / 3 / 2 个可用字段**，穷尽有效几何后最多 2 / 3 / 4 颗，不是 10。要继续增加只能靠设置档变体（decay/中性化），那属于同一信号的重复挖掘，不产生新信息。

其余塔的可用规模与现状：

| 塔 | 数据集数 | 字段数 | 饱和参考 | 现状 |
|---|---|---|---|---|
| OPTION | 2（option1 28 + option30 12） | **40** | alphaCount 3200 / 599（低饱和） | 已挖 10，ATOM 6；高价值字段（IV / 基差 / 股息率 / 高低比 / OI / 成交量）已覆盖，L2-G 证明该塔上限在区分度 |
| SENTIMENT | 4（sentiment21/23/26 + news_sentiment_transfer） | 256 | 1551~12664 | 已挖 10，ATOM 2；剩余空间在 sentiment21 的情绪面字段 |
| EARNINGS | 3（earnings3/6/11） | 63（earnings6 实际不可用） | 623~9105 | 已挖 12（10 有效）；earnings11 35 字段已用 6 个（4 ATOM） |
| INSTITUTIONS | 1（institutions6） | 11 | 12378（高饱和） | 已挖 10（含 8 个已用字段）；ATOM 有、强信号无 |

---

## 6. 本轮结论

1. **塔覆盖：6 个塔达到 ≥10 颗** —— EARNINGS 12（10 有效）/ RISK 11 / INSIDERS 10 / INSTITUTIONS 10 / SENTIMENT 10 / OPTION 10。未达标 3 个：IMBALANCE 2、SHORTINTEREST 1、MACRO 1 —— **字段级结构性不可达**（§5 已给数据集/字段证据），不是挖得不够。
2. **ATOM 已达成 17 行（有效 15 行）**：OPTION 6 / EARNINGS 6（4 有效）/ SENTIMENT 2 / INSTITUTIONS 2 / IMBALANCE 1。`pyramids.effective == 1` 在五个塔上都能稳定复现（`ts_rank(ts_backfill(vec_avg(F),W),W)` 单数据集形态），说明 **ATOM 不是稀缺形态，稀缺的是「单数据集里同时有 ≥1.58 Sharpe 的字段」**。
3. **最佳可继续推进的 ATOM 仍是 `KPJjPGV8`（IMBALANCE，S 2.09 / F 1.66 / sub 1.04，仅 `LOW_ROBUST` 0.41 + `CONCENTRATED_WEIGHT` 两项）**，它是全部未点亮塔里唯一「ATOM 且指标近闸」的候选；次优是本塔历史成品 `58EbwZeN`（已全闸）。
4. **Form E 仍是本区最高产出的几何（ra=0 共 6 颗，S 1.85~3.00），但结构上必为 eff=2**，在 ATOM 优先口径下只能进组腿池（且 risk 族已有多颗互相关 >0.7 的存量，组腿空间也有限）。
5. **OPTION 塔的 L2-G 实测否掉了「覆盖率压制 S」这一假设**：把覆盖率从 0.34 提到 0.52 后 S 仍为负、换手反而破 0.40 ⇒ 该塔的上限来自期权面字段在 IND 的横截面区分度，继续加同塔 ATOM 不改变上限。
6. 本轮**不提交任何 alpha**：无新的 ATOM 候选接近全闸；`KPJjPGV8` 需先做 rob 修复（Mode A）再谈提交，且提交需用户明确确认 + `submit_verdict` 预检 + 塔位复读 + prod 实测（MCP `check_correlation`）。

---

## 7. 复现与批次登记

| 批次 | msid | 内容 | 结果 |
|---|---|---|---|
| L2-A | `2df6t8dfW4P1bEbHPHhFdhc` | option1：`delta_surface_data_quality` / forward-price basis（decay 6 / INDUSTRY） | `9qxL1jke` / `0mY03Xak`，均 eff=1 |
| L2-B | `3izg4bd2a4oC8WmeWce9VhN` | earnings6：EPS surprise rank / EPS level rank（decay 6 / INDUSTRY） | `VkxggK15` / `kqN22edl`，均 eff=1 但 `bookSize=0`（数据无值） |
| L2-C | `38oAbj4nm57UbDl18mRD1k9b` | option30：open interest / traded contracts（decay 6 / INDUSTRY） | `pwdAO53X`（S 0.21）/ `d5WAL1vY`（S −0.60），均 eff=1 |
| L2-D | `Rc6Ncvf4EvbmPjATFIpSV` | sentiment26：注意力广度 rank / 注意力变化（decay 6 / INDUSTRY） | `pwdAOeJv` / `O0AEaXqY`，均 eff=1 |
| L2-E | `JjMD34sh4Pl959XJSlVQP4` | institutions6：机构净买入额 rank / 持有机构数 rank（decay 6 / INDUSTRY） | `qMLoZ332`（S 0.72）/ `GrWpvxxx`（S −0.03），均 eff=1 |
| L2-F（前序） | `49XhXLe5q4Qqb77b3tmM9Kx` | option1：Form E ×2（decay 126 / STATISTICAL） | `9qxLYk1q` / `3qoZwJrz` |
| L2-G | `sKcHk4Nt5bF9sYRMwn9aXP` | option1：隐含股息率 rank / 日内高低比 rank（decay 6 / INDUSTRY） | `KPJjx8rl`（S 0.32，TO 0.415）/ `wpQMXzb5`（S −0.29，TO 0.440），均 eff=1 |
| L2-H | `4rOD5LT154Xbg215irDGpy6` | earnings11：文档情绪 rank / 事件风险 rank（decay 6 / INDUSTRY） | `QPvLrp7w`（S 0.43）/ `pwdAJeP6`（S −0.45），均 eff=1 |
| L2-I | `KLRpBeYm59e9fGUt0S0LqG` | earnings11：2 小时冲击预测 rank / 相似事件间隔 rank（decay 6 / INDUSTRY） | `Xg95PKK1`（S 0.21）/ `78LE0ddL`（S −0.21），均 eff=1 |

入库波次（库内逐数据集核对）：

| 波次 | 行数 | 数据集分布 | ra=0 | S≥1.0 |
|---|---|---|---|---|
| `unlit28` | 39 | insiders1 10 · institutions6 8 · sentiment21 6 · earnings11 4 · risk70 4 · risk68 3 · earnings3 2 · option1 2 | 6（全 eff=2） | 14 |
| `unlit28b` | 28 | option1 6 · earnings11 4 · risk70 4 · earnings6 2 · imbalance5 2 · institutions6 2 · option30 2 · sentiment21 2 · sentiment26 2 · macro63 1 · shortinterest5 1 | 0 | 3 |

合计 67 行，全部经 `wqb_db.upsert_backtest_rows` / `harvest_multisim_results` 写入，无散件 JSON 落盘。`unlit28b` 的 distinct code 为 26：差额 2 对是 risk70 Form D+hump 的**同表达式不同 decay** 设置变体（`78LbpE38`/`O0APlKqp`、`MPYRrog6`/`GrWAZEYP`），不是误派重复。

S6 台账已回写：`wave_results` 的 `IND / unlit28`（verdict PASS，6 颗 ra=0 全为组腿）与 `IND / unlit28b`（verdict PARTIAL，0 颗 ra=0、3 颗 near）经 `wqb_db.upsert_wave_result` 写入，`source_file` 指向本报告。此前 `unlit28` 只有 harvest 级 2 候选的暂定 FAIL 存根，已被本波评审口径覆盖（AGENTS §8.6 结论归属）。
