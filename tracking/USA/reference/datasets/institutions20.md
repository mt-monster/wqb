# institutions20 · USA/D1/TOP3000 字段画像与机制库

> 数据集：`institutions20`（Short Sale Volume / FINRA 分场所做空成交量）
> 区域/宇宙/Delay：USA / TOP3000 / D1 · 塔位：**INSTITUTIONS（1/3，未点亮）** · 倍率 ×1.0
> 平台规模：17 字段 · coverage 0.6673–1.0 · alphaCount 11–615 · pyramidMultiplier 1.0
> 建档：2026-11-22（wave `usa_inst20_atom_20261122`）· 状态：**探针待发**

---

## §0 数据集选择

| 候选 | 覆盖 | 字段 | 平台 aC | 判断 |
|---|---|---|---|---|
| **institutions20** | **0.67–1.0** | 17 | 11–615 | ✅ INSTITUTIONS 1/3 未亮；已有 OS 件 `akKW0Lax` 占「short share 双 zscore」机制，**本集仍有 exempt / venue / level 三条未占机制** |
| institutions18 | — | — | — | `prod_sealed`（prod 0.9493 / 0.9344，`usa_dead_datasets.md`） |
| institutions6 / fund_holdings_panel | — | — | — | 已有档案，非本波目标 |

选它的两条理由：
1. **F 画像正确**：本集天然慢（日频成交量占比 + 长窗平滑），存量 `akKW0Lax` 实测
   S2.47 / F1.77 / TO 13.0% / ret 6.63% —— 这是 USA 少见的「慢而高收益」F 画像；
   快信号（如 short_interest_pred）F 结构性不可救，本集相反。
2. **塔位只差 2 颗**：INSTITUTIONS 1/3，且已有 OS 件只占一条机制；exempt share / venue spread /
   纯 level 三条机制与它经济含义不同，self-corr 有头寸空间（须实测）。

⚠ **已占用机制（必须避开）**：`akKW0Lax` =
`vector_neut(multiply(subtract(ts_zscore(ts_mean(short/total,22),126), ts_zscore(...,756)), rank(total)), ts_backfill(short_interest_factor_score_2,66))`
= **短售占比的 126/756 双 zscore 差 × 成交量权重**，SLOW_AND_FAST/decay4。
新臂若同样以 `executed_short_position_share_sum / aggregate_trade_share_count_regular_hours`
为主核，self 会撞车（实测 KPJwQzex 0.8641、omEw8PNb 0.8002）。

---

## §0.1 字段质量先验（按 alphaCount 升序）

| 字段 | 类型 | 覆盖 | aC | uC | 描述要点 |
|---|---|---|---|---|---|
| `inst20_ra_tv` | MATRIX | 1.0 | 11 | 9 | **无描述**（不进入选型，仅探针完整性） |
| `short_exempt_transaction_share_count` | MATRIX | 1.0 | 16 | 13 | 常规时段**豁免**做空成交股数（ShortVolume 子集） |
| `inst20_ra_sv` | MATRIX | 1.0 | 17 | 10 | **无描述** |
| `inst20_ra_sev` | MATRIX | 0.6673 | 18 | 13 | **无描述** |
| `short_sale_executed_share_quantity` | MATRIX | 1.0 | 21 | 16 | 常规时段做空成交总股数（含豁免与非豁免） |
| `overall_executed_trade_share_amount` | MATRIX | 1.0 | 30 | 26 | 常规时段总成交股数（多空合计） |
| `inst20_sq_market` | MATRIX | 1.0 | 48 | 36 | 上报场所标识（**非信号**） |
| `inst20_sq_sev` | MATRIX | 1.0 | 49 | 31 | Nasdaq TRF 豁免做空股数 |
| `executed_short_position_share_sum` | MATRIX | 1.0 | 51 | 36 | 常规时段做空成交股数（含豁免） |
| `inst20_yx_market` | MATRIX | 1.0 | 59 | 24 | 上报场所标识（**非信号**） |
| `exempt_short_trade_share_total` | MATRIX | 1.0 | 76 | 18 | ShortVolume 内豁免做空股数 |
| `aggregate_trade_share_count_regular_hours` | MATRIX | 1.0 | 83 | 59 | 常规时段总成交股数（facility 口径） |
| `inst20_yx_sev` | MATRIX | 1.0 | 86 | 36 | NYSE TRF 豁免做空股数 |
| `inst20_yx_sv` | MATRIX | 1.0 | 109 | 50 | NYSE TRF 做空股数 |
| `inst20_yx_tv` | MATRIX | 1.0 | 212 | 135 | NYSE TRF 总成交股数 |
| `inst20_sq_sv` | MATRIX | 1.0 | 299 | 188 | Nasdaq TRF 做空股数 |
| `inst20_sq_tv` | MATRIX | 1.0 | 615 | 346 | Nasdaq TRF 总成交股数 |

**头部轴判读**：最热的是 Nasdaq 场所总量（615 / 299）——「分场所成交量」层已拥挤；
最冷的是 **豁免做空（16 / 76）** 与 **未描述字段（11–18）**。
⇒ 经济轴 = **豁免做空占比（market-maker 对冲流）** 与 **跨场所做空分歧**，不是总量。

---

## §0.2 字段分类（以 description 为准）

| 族 | 字段 | 语义 | 时间性 |
|---|---|---|---|
| **V1 场所总量** | `inst20_sq_tv` / `inst20_yx_tv` / `aggregate_trade_share_count_regular_hours` / `overall_executed_trade_share_amount` | 各场所总成交股数 | 日频 |
| **V2 场所做空量** | `inst20_sq_sv` / `inst20_yx_sv` / `executed_short_position_share_sum` / `short_sale_executed_share_quantity` | 各口径做空成交股数 | 日频 |
| **V3 场所豁免做空** | `inst20_sq_sev` / `inst20_yx_sev` / `short_exempt_transaction_share_count` / `exempt_short_trade_share_total` | 豁免做空股数（做市商对冲代理） | 日频 |
| **V4 场所标识** | `inst20_sq_market` / `inst20_yx_market` | 上报场所 id | 常量型，非信号 |
| **V5 未描述** | `inst20_ra_tv` / `inst20_ra_sv` / `inst20_ra_sev` | 无语义 | 仅探针完整性，不入选 |

---

## §0.3 机制假设与模板白名单

| 机制 | 经济逻辑 | 预期符号 | 首选模板 | 排除/前置 |
|---|---|---|---|---|
| **M1 做空占比水平** | 做空成交占总量比例高 ⇒ 看空压力 | 负 | `-rank(divide(executed_short_position_share_sum, aggregate_trade_share_count_regular_hours))` | ⚠ 与 `akKW0Lax` 同核，仅作 self 对照，不作交付 |
| **M2 豁免做空占比** | 豁免做空 ≈ 做市商对冲，不是知情做空；占比高 ⇒ 流动性供给/对冲需求 | 正/负待实测 | `-rank(divide(short_exempt_transaction_share_count, short_sale_executed_share_quantity))`；分母 `+1` 防零 | 覆盖率 1.0；字段最冷（aC 16） |
| **M3 跨场所做空分歧** | Nasdaq 与 NYSE 的做空占比差 = 场所层面知情流差异 | 负（高分歧 = 一边倒做空） | `-rank(subtract(divide(inst20_sq_sv, inst20_sq_tv), divide(inst20_yx_sv, inst20_yx_tv)))` | 两场所覆盖均 1.0 |
| **M4 做空占比趋势** | 占比的长期趋势（慢变量） | 负 | `-rank(ts_mean(divide(sv, tv), 66))`；`-ts_zscore(ts_mean(...,22),252)` | 与 M1 同核但慢，self 需实测 |
| **M5 豁免占比趋势** | 豁免占比的趋势/偏离 | 待实测 | `-ts_zscore(ts_mean(divide(sev, sv), 22), 252)` | — |

**禁止**：跨集组腿（本波 ATOM 单集）；两条独立腿 `add`；`executed_short_position_share_sum`
与 `inst20_sq_sv` 同源重复计数（只选其一作分母口径）。

---

## §0.4 证据（论坛 + 论文）

- 论文闸（`paper_search.py --diverse`）：
  - 《Short Interest and Stock Returns》2004, NBER w10434
  - 《Surprise in Short Interest》2023, JFM `10.1016/j.finmar.2023.100841`
  - 《Short interest, stock returns and credit ratings》2019, JBF `10.1016/j.jbankfin.2019.105617`
  - 《Strategic disclosure and informed trading with short-selling constraints》2025, `10.1111/1911-3846.13066`
  - 《Short Selling, Informed Trading, and the Role of Social Media》2018, `10.33423/jaf.v18i6.446`
- 论坛：`search_forum_posts_local` 命中 79 帖（短售/卖空/回补/借券）；
  方法论锚点 135 赞单数据集帖 `44887744717335`；空头腿审计帖 `44687266076823`。
- 平台实证：存量 `akKW0Lax`（INSTITUTIONS+RISK，S2.47/F1.77/TO13%/ret6.63%/prod0.5171/self0.1809）
  证明「慢速做空占比」在 USA/D1 有真实信息含量；本集目标是用**另一条经济机制**拿到第二颗。

---

## §1 字段全表（分母 = 平台 17 字段，逐字段真实 id，无通配）

| # | 字段 id | 类型 | 覆盖 | aC | 族 |
|---|---|---|---|---|---|
| 1 | `executed_short_position_share_sum` | MATRIX | 1.0 | 51 | V2 |
| 2 | `aggregate_trade_share_count_regular_hours` | MATRIX | 1.0 | 83 | V1 |
| 3 | `short_exempt_transaction_share_count` | MATRIX | 1.0 | 16 | V3 |
| 4 | `short_sale_executed_share_quantity` | MATRIX | 1.0 | 21 | V2 |
| 5 | `exempt_short_trade_share_total` | MATRIX | 1.0 | 76 | V3 |
| 6 | `overall_executed_trade_share_amount` | MATRIX | 1.0 | 30 | V1 |
| 7 | `inst20_sq_sv` | MATRIX | 1.0 | 299 | V2 |
| 8 | `inst20_sq_tv` | MATRIX | 1.0 | 615 | V1 |
| 9 | `inst20_sq_sev` | MATRIX | 1.0 | 49 | V3 |
| 10 | `inst20_yx_sv` | MATRIX | 1.0 | 109 | V2 |
| 11 | `inst20_yx_tv` | MATRIX | 1.0 | 212 | V1 |
| 12 | `inst20_yx_sev` | MATRIX | 1.0 | 86 | V3 |
| 13 | `inst20_sq_market` | MATRIX | 1.0 | 48 | V4 |
| 14 | `inst20_yx_market` | MATRIX | 1.0 | 59 | V4 |
| 15 | `inst20_ra_tv` | MATRIX | 1.0 | 11 | V5 |
| 16 | `inst20_ra_sv` | MATRIX | 1.0 | 17 | V5 |
| 17 | `inst20_ra_sev` | MATRIX | 0.6673 | 18 | V5 |

---

## §2 全字段实测读数（17/17，零抽样）

> 波次 `usa_inst20_atom_20261122` · 设置：USA/TOP3000/D1，SUBINDUSTRY，decay 5，trunc 0.08，
> nanHandling ON，maxTrade OFF，pasteurization ON，unitHandling VERIFY。
> 探针 = 每字段一条裸 `rank(...)`；读数待回填。

| 字段 | 探针表达式 | Sharpe | Fitness | Turnover | 备注 |
|---|---|---|---|---|---|
| `executed_short_position_share_sum` | `rank(executed_short_position_share_sum)` | 0.31 | 0.13 | 0.1378 | nparg7vd；2Y -0.21 |
| `aggregate_trade_share_count_regular_hours` | `rank(aggregate_trade_share_count_regular_hours)` | 0.40 | 0.20 | 0.1305 | QP06a705；批 1 最强但仍是规模代理 |
| `short_exempt_transaction_share_count` | `rank(short_exempt_transaction_share_count)` | -0.19 | -0.04 | 0.5527 | nparg7al；**CW 0.5 FAIL**（2019-11-20） |
| `short_sale_executed_share_quantity` | `rank(short_sale_executed_share_quantity)` | 0.21 | 0.03 | 0.8307 | VkNep7M8；HIGH_TURNOVER + CW FAIL |
| `exempt_short_trade_share_total` | `rank(exempt_short_trade_share_total)` | 0.17 | 0.03 | 0.3404 | blaALjxm；2Y -0.50 |
| `overall_executed_trade_share_amount` | `rank(overall_executed_trade_share_amount)` | 0.15 | 0.02 | 0.7933 | RRePp791；HIGH_TURNOVER + CW FAIL |
| `inst20_sq_sv` | `rank(inst20_sq_sv)` | 0.10 | 0.02 | 0.1425 | kqa93jWd；2Y -0.17 |
| `inst20_sq_tv` | `rank(inst20_sq_tv)` | 0.27 | 0.10 | 0.1371 | LLK3p7m1；2Y -0.10 |
| `inst20_sq_sev` | `rank(inst20_sq_sev)` | -0.08 | -0.01 | 0.3482 | WjlJp7ox；2Y -0.51 |
| `inst20_yx_sv` | `rank(inst20_yx_sv)` | 0.08 | 0.01 | 0.2661 | zqde9kGo；2Y -0.38 |
| `inst20_yx_tv` | `rank(inst20_yx_tv)` | 0.13 | 0.03 | 0.2418 | j2aO0L7W；2Y -0.45 |
| `inst20_yx_sev` | `rank(inst20_yx_sev)` | -0.17 | -0.03 | 0.4392 | omaZl2dJ；2Y -0.41 |
| `inst20_sq_market` | `rank(inst20_sq_market)` | 0.46 | 0.25 | 0.0155 | O0WgZe3d；**场所 id 非信号**（2Y 1.12 但 LOW_SUB 0.12） |
| `inst20_yx_market` | `rank(inst20_yx_market)` | 0.58 | 0.31 | 0.0598 | 58JYORPN；**场所 id 非信号**（CW 0.5 FAIL） |
| `inst20_ra_tv` | `rank(inst20_ra_tv)` | -1.09 | -0.36 | 0.4424 | j2aO0Lqj；无描述 + CW FAIL，不入选型 |
| `inst20_ra_sv` | `rank(inst20_ra_sv)` | -0.99 | -0.31 | 0.4566 | omaZl2xJ；无描述 + CW FAIL |
| `inst20_ra_sev` | `rank(inst20_ra_sev)` | -0.51 | -0.11 | 0.5234 | gJaLM7YO；无描述 + CW/SUB FAIL |

---

## §3 结论（PROVISIONAL：比例机制弱 + 强机制撞 self）

### 3.1 机制 × 闸门矩阵

| 机制 | 代表 alpha | S | F | TO | 2Y | invest比 | self | 判读 |
|---|---|---|---|---|---|---|---|---|
| 豁免占做空比 | LLK3d2ev | 0.19 | 0.04 | 0.5529 | 0.24 | — | — | 全弱 + CW 0.5 |
| 豁免占做空比（alt） | KPgZE2xx | 0.05 | 0.00 | 0.4375 | 0.65 | — | — | 全弱 |
| 豁免占总成交比 | 2r5eN2P5 | 0.19 | 0.04 | 0.5529 | 0.24 | — | — | 同 LLK3d2ev |
| Nasdaq 豁免占比 | QP069orM | 0.22 | 0.04 | 0.4226 | 0.68 | — | — | 弱 |
| NYSE 豁免占比 | KPgZE2YE | 0.19 | 0.03 | 0.4520 | 0.47 | — | — | 弱 |
| **跨场所做空分歧** | **j2aOrMlk** | **1.11** | **0.24** | **0.6366** | **1.90** | 0.56 | — | L1 最强但仍远低于闸 |
| 跨场所豁免分歧 | xAv5dE9w | 0.18 | 0.02 | 0.4952 | 0.62 | — | — | 弱 |
| 做空占比水平 | 58JYk23z | 0.61 | 0.15 | 0.3756 | 0.41 | 1.64 | — | 弱 |
| 做空占比（alt 分母） | mLaQVlAp | -0.23 | -0.02 | 1.0733 | 0.06 | — | — | 弱 + TO 107% |
| NYSE 做空占比 | xAv5dEQN | 0.13 | 0.01 | 0.5790 | -1.41 | — | — | 弱 |

### 3.2 结论

- 简单比例机制（exempt / venue / level）**全部 S ≤ 1.11**，无近闸候选。
- 唯一强机制 = **短售占比双 zscore 流**（`akKW0Lax` / `KPJwQzex` / `omEw8PNb` 族，S 2.28–2.52），
  但 **self-corr 0.80–0.96 撞自家 OS 件 `akKW0Lax`** ⇒ 不可再交付同族。
- 按 §7.6 记 **PROVISIONAL（机制层弱 / 同族 self 饱和）**，不判数据集级死。
- **重开条件**：出现新的非「做空占比」字段族（如持仓/融券余额的独立字段），或 OS 池换季。

