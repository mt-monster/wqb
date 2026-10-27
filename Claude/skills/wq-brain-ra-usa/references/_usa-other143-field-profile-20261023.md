# USA `other143` 字段画像与首波机制设计（2026-10-23）

> 数据集：**Transaction Volume Data for Equity**（Clearing-ID 级成交量）
> 区域 / 延迟：USA / D1 · 金字塔：`other`（USA/D1 ×1.4，全季 0 次提交 ⇒ **未点亮**）
> tier：STANDARD · subcategory：`other-event-data`（Event Data）· 平台 alphaCount 639
> 采集：`GET /data-fields?region=USA&delay=1&universe=TOP3000&dataset.id=other143`，2026-10-23 全量 126 条
> 关联：切换举证见 [`_usa-atom-delivery-log-20261020.md`](_usa-atom-delivery-log-20261020.md) 附录 AN §N.4；
> 本集在**全库 0 条表达式**（任何 region 都没碰过），是"未点亮塔 + 无历史尝试 + 字段面够"三条件同时满足的剩余集。

---

## 0. 一页结论

| 维度 | 读数 | 判断 |
|---|---|---|
| 字段数 | 126（105 MATRIX + 21 VECTOR） | 够铺 10 个互不相同的机制臂 |
| 横截面覆盖 `coverage` | min **0.9499** / median **1.0000** / max 1.0000 | 几乎是全样本，无需大规模 backfill |
| 时间覆盖 `dateCoverage` | **全 126 字段同为 0.9507** | 少 4.93% 交易日，且**全族同值** ⇒ 更像统一历史起点截断，不是随机缺失 |
| 拥挤度 `alphaCount` | min 0 / median **184** / max **3387** / 用户数 median 49.5 | 中等拥挤，但**分布极不均**（见 §1.3）：`concentration` 族已被挖到 1300+，`exempt_*` 只有个位数 |
| 类型 | 全 MATRIX + VECTOR，无 GROUP / 无日期字段 | 标量直取；VECTOR 族（`rolling_*`）需 `vec_*` 聚合才能用 |
| 倍率 | 字段级 `pyramidMultiplier` 全 1.4 | 与 USA/D1 `other` 一致 |

**一句话机制**：这不是"成交量"数据集，是**"谁在交易"数据集**——每个交易日、每只股票，按 Clearing ID（FINRA 会员）
把这个票的成交量拆成**券商身份结构**：前 1/2/3 大券商的份额、券商份额平方和（HHI）、活跃券商家数、
各队列的成交量与成交均价。已交付的 5 颗 alpha 全部来自 analyst 族（修正 / 目标价），本集的收益来源是
**交易对手方结构**，与那 5 颗正交。

**首波判断**：字段面足够、拥挤度局部很低（`exempt_*` 21 字段 median aC = 2–24），但**没有任何一条现成配方**——
必须靠机制分臂探针，不能在首波就押单一壳。

---

## 1. 字段全景（126 / 126 已清点）

### 1.1 三个族，结构是严格笛卡尔积

| 族 | 字段数 | 类型 | 命名式 | 语义 |
|---|---:|---|---|---|
| `exempt_*` | **21** | MATRIX | `exempt_<cohort>_<metric>` | **Sell Exempt 侧**（豁免报告口径）的券商结构。最原始、最不拥挤的一族 |
| `oth143_*` | **84** | MATRIX | `oth143_<side>_<cohort>_<metric>` | 按方向拆分的日频/5 日滚动汇总（平台派生的主用族） |
| `rolling_*` | **21** | **VECTOR** | `rolling_<cohort>_<metric>` | 与 `exempt_*` 同口径的**滚动窗口向量**，必须 `vec_avg/vec_sum/vec_last` 聚合后才能进标量算子 |

- **cohort（3 个）**：`gbda` = Global Broker Dealers；`industry` = Industry 券商；`tier1` = Tier 1 券商。
- **side（4 个）**：`buy` / `sell` / `short_sell` / `5dayrolling`（不分方向，5 日滚动）。
- **metric（每 cohort 7 个）**：
  | metric | 语义（平台原文摘要） | 量纲 |
  |---|---|---|
  | `concentration` | **Σ 市场份额²**（Herfindahl 指数） | 无量纲，[0,1] |
  | `rank1` / `rank2` / `rank3` | 第 1/2/3 活跃 Clearing ID 的**市场份额百分比** | [0,100] |
  | `broker_count` / `unique_brokers` | 该 cohort 当日活跃券商**家数**（tier1 叫 `unique_brokers`） | 整数 ≥1 |
  | `volume` | 该 cohort 该方向的**清算股数**（5dayrolling 族四舍五入到千股） | 股 |
  | `vwap` | 该 cohort 该方向的**成交量加权均价** | 货币单位（与收盘同价） |

**完整性核验（机器，2026-10-23）**：`84 = 4 side × 3 cohort × 7 metric` 逐个拼名比对，**missing = 0，extra = 0**；
`exempt_*` 21/21 齐；`rolling_*` 21/21 齐。总计 126 = 21 + 84 + 21。

### 1.2 ⚠ 命名陷阱（会直接导致 field-not-found）

`rank1/2/3` 的拼法**随 cohort 变**，不是统一后缀：

| cohort | rank 字段名 |
|---|---|
| `gbda` | `oth143_buy_gbda_**rank1**`（**没有** `broker_`） |
| `industry` | `oth143_buy_industry_**broker_rank1**` |
| `tier1` | `oth143_buy_tier1_**broker_rank1**` |

另外 `rolling_industry_traded_shares` **少了 `group_` 前缀**（其余为 `group_traded_shares`）。
写表达式前逐字对照附录 A，不要按"统一后缀"推断。

### 1.3 拥挤度分布极不均 —— 设计必须避开高热子族

按 metric 汇总 `alphaCount`（126 字段实测）：

| metric | 字段数 | 中位 aC | 最大 aC | 读法 |
|---|---:|---:|---:|---|
| `concentration` | 12 | **1346** | 3387 | **已被挖穿**；同族头部 `oth143_sell_industry_concentration`（3387）、`oth143_buy_industry_concentration`（2984） |
| `rank1` | 12 | **1133** | 2099 | 高热 |
| `volume` | 12 | 368 | 980 | 中热 |
| `rank2` | 12 | 298 | 997 | 中低 |
| `rank3` | 12 | 255 | 1139 | 中低 |
| `broker_count` / `unique_brokers` | 14 | 79 | 2748 | 分层：`exempt_*` 个位–几十，派生族上百到上千 |
| `vwap` | 18 | 161 | 243 | 中低 |
| **`index`（HHI，exempt）** | 6 | **24** | 92 | **近原始** |
| **`pct`（份额，exempt）** | 18 | **2** | 67 | **近原始** |
| **`shares`（exempt）** | 6 | **3** | 6 | **近原始** |

⇒ **同一个"经济机制"用 `exempt_*` 表达，拥挤度是同义 `oth143_*` 的 1/50**。
本波 10 臂里有 5 臂刻意落在 `exempt_*` 上，这是"低拥挤优先"的具体落地，不是随便挑字段。

### 1.4 更新频率 / 覆盖 / 可用性

- **频率**：日频（D1）。`5dayrolling` 族是 5 个交易日的滚动聚合，**不是**更低频的独立数据集。
- **时间覆盖**：`dateCoverage` 126/126 全为 **0.9507**。全族同值 ⇒ 极可能是"统一历史起点"截断
  （平台历史约 5 年，缺 4.93% ≈ 少 3 个月），**不是**随股票 / 随日期随机缺失。⚠ 未在 Labs 取到真实起止日，
  此结论为推断，首波回测的 `2Y` 读数会给出反证（若 2Y 窗口内缺月，S 会系统性偏低）。
- **横截面覆盖**：仅 3 个字段低于 0.98——`exempt_gbda_broker_concentration_index` 0.9499、
  `oth143_short_sell_gbda_*` 与 `exempt_gbda_{second,third,top}_broker_share_pct` 约 0.9780–0.9786。
  **GBDA（全球券商）队列天然只覆盖大票**——小票没有全球券商参与。⇒ 用 GBDA 族必须 `ts_backfill`，
  且**不要拿 GBDA 的家数类字段做全市场分散度**（小票上是 0 还是缺失会直接决定因子符号）。
- **量纲提醒**：`vwap` 是货币单位、`volume` 是股数，**各自不能与无量纲常数相加**（VERIFY 会报 UNITS）；
  比值都成对同量纲相除。

### 1.5 分布特征（已知部分 + 明确缺口）

| 字段族 | 值域（构造约束） | 分布形态（推断） |
|---|---|---|
| HHI `concentration` / `broker_concentration_index` | [1/N, 1]（N = 活跃券商家数） | 强右偏：绝大多数票 N 大 ⇒ HHI 贴近 1/N 下界，只有少数票被 1–2 家券商垄断 |
| `rank1/2/3`（份额 %） | [0, 100]，且 rank1 ≥ rank2 ≥ rank3 单调 | 右偏；rank1 中位大概 10–30%，rank3 常 <10% |
| `distinct_broker_count` / `unique_brokers` | 整数 ≥ 1 | 右偏 + 与市值强正相关 ⇒ **必须做规模中性**（`rank` / `group_rank` / 除以自身均值），否则就是市值代理 |
| `volume` | ≥ 0，5dayrolling 舍入到千股 | 极端右偏（幂律）⇒ 必须 `rank` 或除以 `adv20`，不可直取 |
| `vwap` | 等于当日价格水平 | 与价格同量级；**只能做比值 / 价差**，直取 = 价格因子（与 pv 塔重复） |

⚠ **缺口（诚实登记）**：以上"分布形态"是**由定义与量纲推出的**，不是实测分位数。真实横截面分位
（median / p90 / 偏度 / 零值率）需要 Labs 或一次仿真才能给出；本轮为省配额未跑 Labs，
**首波回测后**用每条 alpha 的 `long_count` / `short_count` / `returns` / `drawdown` 与字段在表达式中的
`rank` 落点反推，回填到本节。在此之前，任何"分位 / 峰度"表述都不算证据。

---

## 2. 经济机制假设（10 条，每条可单独证伪）

**共同前提**：Clearing-ID 是**清算会员**身份，不是最终受益人。所以这批字段测的是
**"订单流经过谁的手"**，而不是"谁持有"。三条文献级支撑（均为公开结论，非本平台配方）：

1. **券商集中度 = 信息不对称的代理**：做市/清算越集中于少数会员，价格发现越依赖他们，
   逆向选择成分越高 ⇒ 流动性溢价上升（HHI ↑ → 预期收益 ↑）。
2. **参与广度 = 注意力/散户代理**：活跃券商家数、尤其是 Tier1 之外的家数上升，对应散户与多渠道路由进场；
   这类参与者的方向性需求通常是**短期高估**（breadth ↑ → 未来收益 ↓）。
3. **方向拆分的身份结构 = 主动方识别**：同一只票，买单的集中度高于卖单，说明**少数会员在集中吸收筹码**；
   空头卖出侧的集中度显著高于普通卖出侧，说明**知情做空**（concentration ↑ on short side → 未来收益 ↓）。

---

## 3. 波 74 · 十臂设计（预注册，事后不调方向）

设置钉死：**USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / VERIFY / nanHandling ON /
pasteurization ON / maxTrade OFF**。全部为 **ATOM**（单数据集 `other143`）。

| 臂 | 机制（一句话） | 表达式 | 方向假设 | 核心字段（aC） |
|---|---|---|---|---|
| **A1** | 机构券商集中度（HHI 水平）＝ 流动性脆弱溢价 | `rank(ts_zscore(exempt_tier1_broker_concentration_index, 120))` | **+** | `exempt_tier1_broker_concentration_index`（36） |
| **A2** | 参与广度（行业券商家数）＝ 散户/注意力代理 | `multiply(-1, rank(ts_zscore(exempt_industry_distinct_broker_count, 60)))` | **−** | `exempt_industry_distinct_broker_count`（4） |
| **A3** | 买卖集中度背离 ＝ 主动买方被少数会员吸收 | `rank(ts_zscore(subtract(oth143_buy_tier1_concentration, oth143_sell_tier1_concentration), 60))` | **+** | `oth143_{buy,sell}_tier1_concentration`（1436/1986） |
| **A4** | 空头集中度**超额**（短卖 − 普通卖出）＝ 知情做空 | `multiply(-1, rank(ts_zscore(subtract(ts_backfill(oth143_short_sell_tier1_concentration, 66), oth143_sell_tier1_concentration), 60)))` | **−** | 同上 + `oth143_short_sell_tier1_concentration`（1098） |
| **A5** | 买卖执行价差（GBDA）＝ 买方愿意付的溢价 | `rank(ts_zscore(divide(subtract(oth143_buy_gbda_vwap, oth143_sell_gbda_vwap), close), 60))` | **+** | `oth143_{buy,sell}_gbda_vwap`（125/168） |
| **A6** | 头部份额动量（22d）＝ 流量向头部券商集中 | `rank(ts_delta(exempt_industry_top_broker_share_pct, 22))` | **+** | `exempt_industry_top_broker_share_pct`（67） |
| **A7** | 头部陡峭度（rank1 − rank2）＝ 单一主导买方 | `rank(ts_zscore(subtract(oth143_buy_tier1_broker_rank1, oth143_buy_tier1_broker_rank2), 60))` | **+** | `oth143_buy_tier1_broker_rank{1,2}`（1177/218） |
| **A8** | 分层背离（tier1 − industry HHI）＝ 大玩家主导程度 | `rank(subtract(ts_zscore(exempt_tier1_broker_concentration_index, 60), ts_zscore(exempt_industry_broker_concentration_index, 60)))` | **+** | 两个 exempt HHI（36/92） |
| **A9** | 券商数骤增（相对自身 63d 均值）＝ 参与结构位移 | `multiply(-1, rank(ts_zscore(divide(ts_backfill(oth143_buy_tier1_unique_brokers, 66), ts_mean(ts_backfill(oth143_buy_tier1_unique_brokers, 66), 63)), 63)))` | **−** | `oth143_buy_tier1_unique_brokers`（193） |
| **A10** | 短卖占卖出量比 ＝ 做空强度（成交量口径，非集中度） | `multiply(-1, rank(ts_zscore(divide(ts_backfill(oth143_short_sell_tier1_volume, 66), oth143_sell_tier1_volume), 60)))` | **−** | `oth143_{short_sell,sell}_tier1_volume`（186/980） |

**设计纪律自检**：

- **不是同信号扫参**：10 臂用了 10 组不同字段组合 + 5 种不同变换（水平 z、变化量、两腿差、比值、相对自身均值），
  没有"同一表达式换窗口"的臂。
- **没有跨界相加**：唯一的 `subtract` 都是**同一数据集内**两腿的差（且都是"结构 vs 结构"，不是两条独立信号相加），
  不含 `add`、不含加权（禁混信号）。
- **没有 VECTOR 臂**：`rolling_*` 21 个 VECTOR 字段本波不用；若首波有信号，第二波再上 `vec_avg(vec_last(...))` 检验
  滚动窗口内的形状（这是**新机制**，不是补腿）。
- **方向是假设不是旋钮**：A2/A4/A9/A10 取负是**因为假设本身是负向**，不是"跑反了再翻"。若读数为强正，
  结论是"假设被证伪"，进第二波的**新机制**，不在同一臂上翻符号。

---

## 4. 首波止损（预注册，触发即封存，不追加）

| 触发条件 | 处置 |
|---|---|
| 10 臂 `\|S\|` 全部 < 1.0 | 判 **`USA-OTHER143-WEAK`**，本集首波即封存，不得在本集追第二波；换 `other696`（其后 `risk65`） |
| 有臂 `\|S\| ≥ 1.58` 但 `F < 0.8` 且 TO > 0.45 | 只做**一次**降换手（`ts_decay_linear` 或 `hump`），不重设计机制 |
| 有臂三闸（S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58）全过 | 才进降相关与 prod 队列；**提交仍须用户明确确认** |
| 有臂 IS 过但 `CONCENTRATED_WEIGHT` 失败 | 按 D6 的 CW 修法顺序，**不补腿**（D3） |
| 有臂 prod 首探 ≥ 0.70 | 按 D0-P / 附录 AN §N.2 三档（n=1 允许 1 次换几何探针；n≥2 判族死） |

**不做的事**：不扫设置网格找分（decay / 中性化 / universe）；不在首波叠跨数据集腿；不使用 `add` / 加权。

---

## 5. 与既有结论的关系

| 既有资产 | 与本集的关系 |
|---|---|
| 5 颗已交付 ACTIVE（analyst_factor_signals ×2、analyst44 ×2、analyst_consensus ×1） | 机制为"分析师修正 / 目标价"，本集为"券商身份结构" ⇒ **正交**，不构成同族自相关风险 |
| `other596`（420 字段，已试波 61） | 同为 `other` 塔；若本集首波弱，`other596` 是同塔下一顺位（但已有一波记录，需先归因） |
| `shortinterest3`（波 57–59）/ `insider_matrix`（波 48） | 都是"持仓 / 交易者"类，但口径是**做空余额**与**内部人**；本集是**清算会员**，三者互不同源 |
| `intraday_pv_feats`（封存） | 同为微观结构，但那是**日内价格量**，本集是**日频交易对手方**；不共享字段，不共享机制 |
| `event_return_model`（波 64–66 判死） | 同为"低拥挤 + 未点亮"，但它 22 臂 max S 1.19 已耗尽；本集字段面宽 2 倍且是结构型不是预测型 |

---

## 附录 A：全 126 字段清单（机器生成，逐行 `id | type | coverage | dateCoverage | alphaCount | userCount | 描述`）

| # | field id | type | cov | dateCov | aC | users | 描述 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `exempt_gbda_broker_concentration_index` | MATRIX | 0.9499 | 0.9507 | 54 | 36 | Summation of Global Broker Dealers' market share squared. For more information, see Frequently Asked Questions. |
| 2 | `exempt_gbda_distinct_broker_count` | MATRIX | 0.9786 | 0.9507 | 10 | 6 | Number of active brokers in the GBDA cohort for the Sell Exempt side on that date |
| 3 | `exempt_gbda_group_traded_shares` | MATRIX | 0.9786 | 0.9507 | 6 | 5 | Total cleared share volume for the GBDA cohort on the Sell Exempt side for the trade date |
| 4 | `exempt_gbda_group_vwap` | MATRIX | 0.9786 | 0.9507 | 1 | 1 | Volume-weighted average price for the GBDA cohort on the Sell Exempt side for the day; currency units |
| 5 | `exempt_gbda_second_broker_share_pct` | MATRIX | 0.9780 | 0.9507 | 3 | 2 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 6 | `exempt_gbda_third_broker_share_pct` | MATRIX | 0.9780 | 0.9507 | 2 | 2 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 7 | `exempt_gbda_top_broker_share_pct` | MATRIX | 0.9780 | 0.9507 | 7 | 6 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 8 | `exempt_industry_broker_concentration_index` | MATRIX | 1.0000 | 0.9507 | 92 | 73 | Summation of Industry brokers' market shares squared. For more information, see Calculation Specifics on page 14. |
| 9 | `exempt_industry_distinct_broker_count` | MATRIX | 1.0000 | 0.9507 | 4 | 4 | Number of active brokers in the Industry cohort for the Sell Exempt side on that date |
| 10 | `exempt_industry_group_traded_shares` | MATRIX | 1.0000 | 0.9507 | 5 | 3 | Total cleared share volume for the Industry cohort on the Sell Exempt side for the trade date |
| 11 | `exempt_industry_group_vwap` | MATRIX | 1.0000 | 0.9507 | 3 | 3 | Volume-weighted average price for the Industry cohort on the Sell Exempt side for the day; currency units |
| 12 | `exempt_industry_second_broker_share_pct` | MATRIX | 1.0000 | 0.9507 | 3 | 3 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 13 | `exempt_industry_third_broker_share_pct` | MATRIX | 1.0000 | 0.9507 | 4 | 4 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 14 | `exempt_industry_top_broker_share_pct` | MATRIX | 1.0000 | 0.9507 | 67 | 29 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 15 | `exempt_tier1_broker_concentration_index` | MATRIX | 1.0000 | 0.9507 | 36 | 30 | Summation of Tier 1 brokers' market share squared. For more information, see Frequently Asked Questions. |
| 16 | `exempt_tier1_distinct_broker_count` | MATRIX | 1.0000 | 0.9507 | 4 | 4 | Number of distinct brokers active in the Tier1 cohort for the Sell Exempt side on that trade date |
| 17 | `exempt_tier1_group_traded_shares` | MATRIX | 1.0000 | 0.9507 | 2 | 2 | Total cleared share volume for the Tier1 cohort on the Sell Exempt side for the trade date |
| 18 | `exempt_tier1_group_vwap` | MATRIX | 1.0000 | 0.9507 | 3 | 3 | Volume-weighted average price for the Tier1 cohort on the Sell Exempt side for the day; currency units |
| 19 | `exempt_tier1_second_broker_share_pct` | MATRIX | 1.0000 | 0.9507 | 0 | 0 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 20 | `exempt_tier1_third_broker_share_pct` | MATRIX | 1.0000 | 0.9507 | 2 | 2 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 21 | `exempt_tier1_top_broker_share_pct` | MATRIX | 1.0000 | 0.9507 | 18 | 17 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 22 | `oth143_5dayrolling_gbda_broker_count` | MATRIX | 1.0000 | 0.9507 | 363 | 100 | Count of Unique IDs of GBDA Participants. |
| 23 | `oth143_5dayrolling_gbda_concentration` | MATRIX | 1.0000 | 0.9507 | 1207 | 276 | Summation of Global Broker Dealers' market share squared. |
| 24 | `oth143_5dayrolling_gbda_rank1` | MATRIX | 1.0000 | 0.9507 | 508 | 195 | Anonymous market share of the most active Clearing ID in this category. |
| 25 | `oth143_5dayrolling_gbda_rank2` | MATRIX | 1.0000 | 0.9507 | 325 | 55 | Anonymous market share of the second most active Clearing ID in this category. |
| 26 | `oth143_5dayrolling_gbda_rank3` | MATRIX | 1.0000 | 0.9507 | 347 | 62 | Anonymous market share of the third most active Clearing ID in this category. |
| 27 | `oth143_5dayrolling_gbda_volume` | MATRIX | 1.0000 | 0.9507 | 236 | 78 | Total GBDA sum of shares, rounded to the nearest 1000. |
| 28 | `oth143_5dayrolling_gbda_vwap` | MATRIX | 1.0000 | 0.9507 | 236 | 55 | Volume Weighted Average Price. Calculated as an average of execution price, weighted by the number of shares traded for the GBDA. |
| 29 | `oth143_5dayrolling_industry_broker_count` | MATRIX | 1.0000 | 0.9507 | 588 | 118 | Count of Unique IDs of Industry Participants. |
| 30 | `oth143_5dayrolling_industry_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 1308 | 201 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 31 | `oth143_5dayrolling_industry_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 673 | 114 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 32 | `oth143_5dayrolling_industry_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 291 | 73 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 33 | `oth143_5dayrolling_industry_concentration` | MATRIX | 1.0000 | 0.9507 | 2217 | 396 | Summation of Industry brokers' market shares squared. |
| 34 | `oth143_5dayrolling_industry_volume` | MATRIX | 1.0000 | 0.9507 | 393 | 110 | Total Industry sum of shares, rounded to the nearest 1000. |
| 35 | `oth143_5dayrolling_industry_vwap` | MATRIX | 1.0000 | 0.9507 | 165 | 60 | Volume Weighted Average Price. Calculated as an average of execution price, weight by number of shares traded for the industry aggregate. |
| 36 | `oth143_5dayrolling_tier1_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 1483 | 166 | Anonymous market share of the most active Clearing ID in this category |
| 37 | `oth143_5dayrolling_tier1_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 443 | 97 | Anonymous market share of the second most active Clearing ID in this category. |
| 38 | `oth143_5dayrolling_tier1_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 338 | 80 | Anonymous market share of the third most active Clearing ID in this category. |
| 39 | `oth143_5dayrolling_tier1_concentration` | MATRIX | 1.0000 | 0.9507 | 542 | 124 | Summation of Tier 1 brokers' market share squared. |
| 40 | `oth143_5dayrolling_tier1_unique_brokers` | MATRIX | 1.0000 | 0.9507 | 208 | 49 | Count of Unique IDs of Tier 1 Participants. |
| 41 | `oth143_5dayrolling_tier1_volume` | MATRIX | 1.0000 | 0.9507 | 427 | 95 | Total Tier 1 sum of shares, rounded to the nearest 1000 |
| 42 | `oth143_5dayrolling_tier1_vwap` | MATRIX | 1.0000 | 0.9507 | 198 | 53 | Volume Weighted Average Price. Calculated as an average of execution price, weighted by the number of shares traded for the Tier1 aggregate. |
| 43 | `oth143_buy_gbda_broker_count` | MATRIX | 1.0000 | 0.9507 | 154 | 34 | Number of active brokers in the GBDA cohort for this security on the Buy side and date |
| 44 | `oth143_buy_gbda_concentration` | MATRIX | 1.0000 | 0.9507 | 1256 | 207 | Summation of Global Broker Dealers' market share squared. For more information, see Frequently Asked Questions. |
| 45 | `oth143_buy_gbda_rank1` | MATRIX | 1.0000 | 0.9507 | 546 | 107 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 46 | `oth143_buy_gbda_rank2` | MATRIX | 1.0000 | 0.9507 | 272 | 56 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 47 | `oth143_buy_gbda_rank3` | MATRIX | 1.0000 | 0.9507 | 173 | 41 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 48 | `oth143_buy_gbda_volume` | MATRIX | 1.0000 | 0.9507 | 234 | 71 | Total cleared share volume for the GBDA cohort on the Buy side for the trade date |
| 49 | `oth143_buy_gbda_vwap` | MATRIX | 1.0000 | 0.9507 | 125 | 42 | Volume-weighted average price for the GBDA cohort on the Buy side for the trade date; currency units |
| 50 | `oth143_buy_industry_broker_count` | MATRIX | 1.0000 | 0.9507 | 2748 | 327 | Number of active brokers in the Industry cohort for this security on the Buy side and date |
| 51 | `oth143_buy_industry_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 2099 | 192 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 52 | `oth143_buy_industry_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 458 | 88 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 53 | `oth143_buy_industry_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 1139 | 131 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 54 | `oth143_buy_industry_concentration` | MATRIX | 1.0000 | 0.9507 | 2984 | 372 | Summation of Industry brokers' market shares squared. For more information, see Calculation Specifics on page 14. |
| 55 | `oth143_buy_industry_volume` | MATRIX | 1.0000 | 0.9507 | 354 | 90 | Total cleared share volume for the Industry cohort (all NSCC-clearing brokers) on the Buy side for the trade date |
| 56 | `oth143_buy_industry_vwap` | MATRIX | 1.0000 | 0.9507 | 228 | 71 | Volume-weighted average price for the Industry cohort on the Buy side for the trade date; currency units |
| 57 | `oth143_buy_tier1_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 1177 | 128 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 58 | `oth143_buy_tier1_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 218 | 45 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 59 | `oth143_buy_tier1_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 228 | 51 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 60 | `oth143_buy_tier1_concentration` | MATRIX | 1.0000 | 0.9507 | 1436 | 145 | Summation of Tier 1 brokers' market share squared. For more information, see Frequently Asked Questions. |
| 61 | `oth143_buy_tier1_unique_brokers` | MATRIX | 1.0000 | 0.9507 | 193 | 36 | Number of distinct brokers active in the Tier1 cohort for this security on the Buy side and date |
| 62 | `oth143_buy_tier1_volume` | MATRIX | 1.0000 | 0.9507 | 378 | 103 | Total cleared share volume for the Tier1 cohort on the Buy side for the trade date |
| 63 | `oth143_buy_tier1_vwap` | MATRIX | 1.0000 | 0.9507 | 158 | 52 | Volume-weighted average price for the Tier1 cohort on the Buy side for the trade date; currency units |
| 64 | `oth143_sell_gbda_broker_count` | MATRIX | 1.0000 | 0.9507 | 84 | 30 | Number of active brokers in the GBDA cohort for the given security on the Sell side for the trade date |
| 65 | `oth143_sell_gbda_concentration` | MATRIX | 1.0000 | 0.9507 | 320 | 73 | Summation of Global Broker Dealers' market share squared. For more information, see Frequently Asked Questions. |
| 66 | `oth143_sell_gbda_rank1` | MATRIX | 1.0000 | 0.9507 | 179 | 56 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 67 | `oth143_sell_gbda_rank2` | MATRIX | 1.0000 | 0.9507 | 132 | 31 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 68 | `oth143_sell_gbda_rank3` | MATRIX | 1.0000 | 0.9507 | 121 | 38 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 69 | `oth143_sell_gbda_volume` | MATRIX | 1.0000 | 0.9507 | 584 | 146 | Total cleared trading volume in shares for the GBDA cohort for the given security on the Sell side for the trade date |
| 70 | `oth143_sell_gbda_vwap` | MATRIX | 1.0000 | 0.9507 | 168 | 39 | Volume Weighted Average Price. Calculated as an average of the execution price, weighted by the number of shares traded for the GBDA. |
| 71 | `oth143_sell_industry_broker_count` | MATRIX | 1.0000 | 0.9507 | 425 | 87 | Number of active brokers in the Industry cohort for the given security on the Sell side for the trade date |
| 72 | `oth143_sell_industry_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 1935 | 229 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 73 | `oth143_sell_industry_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 476 | 110 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 74 | `oth143_sell_industry_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 403 | 45 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 75 | `oth143_sell_industry_concentration` | MATRIX | 1.0000 | 0.9507 | 3387 | 557 | Summation of Industry brokers' market shares squared. For more information, see Calculation Specifics on page 14. |
| 76 | `oth143_sell_industry_volume` | MATRIX | 1.0000 | 0.9507 | 439 | 119 | Total cleared trading volume in shares for the Industry cohort for the given security on the Sell side for the trade date |
| 77 | `oth143_sell_industry_vwap` | MATRIX | 1.0000 | 0.9507 | 181 | 50 | Volume Weighted Average Price. Calculated as an average of execution price, weight by number of shares traded for the industry aggregate. |
| 78 | `oth143_sell_tier1_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 1566 | 179 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 79 | `oth143_sell_tier1_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 997 | 81 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 80 | `oth143_sell_tier1_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 283 | 55 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 81 | `oth143_sell_tier1_concentration` | MATRIX | 1.0000 | 0.9507 | 1986 | 272 | Summation of Tier 1 brokers' market share squared. For more information, see Frequently Asked Questions. |
| 82 | `oth143_sell_tier1_unique_brokers` | MATRIX | 1.0000 | 0.9507 | 177 | 47 | Count of distinct active brokers in the Tier1 cohort for the given security on the Sell side for the trade date |
| 83 | `oth143_sell_tier1_volume` | MATRIX | 1.0000 | 0.9507 | 980 | 189 | Total cleared trading volume in shares for the Tier1 cohort for the given security on the Sell side for the trade date |
| 84 | `oth143_sell_tier1_vwap` | MATRIX | 1.0000 | 0.9507 | 243 | 52 | Volume Weighted Average Price. Calculated as an average of the execution price, weighted by the number of shares traded for the Tier1 aggregate. |
| 85 | `oth143_short_sell_gbda_broker_count` | MATRIX | 0.9786 | 0.9507 | 75 | 32 | Count of Unique IDs of GBDA Participants |
| 86 | `oth143_short_sell_gbda_concentration` | MATRIX | 0.9780 | 0.9507 | 166 | 85 | Summation of Global Broker Dealers' market share squared |
| 87 | `oth143_short_sell_gbda_rank1` | MATRIX | 0.9780 | 0.9507 | 140 | 55 | Anonymous market share of the most active Clearing ID in this category. |
| 88 | `oth143_short_sell_gbda_rank2` | MATRIX | 0.9780 | 0.9507 | 86 | 27 | Anonymous market share of the second most active Clearing ID in this category. |
| 89 | `oth143_short_sell_gbda_rank3` | MATRIX | 0.9780 | 0.9507 | 68 | 24 | Anonymous market share of the third most active Clearing ID in this category. |
| 90 | `oth143_short_sell_gbda_volume` | MATRIX | 0.9786 | 0.9507 | 98 | 34 | Total GBDA sum of shares, rounded to the nearest 1000. |
| 91 | `oth143_short_sell_gbda_vwap` | MATRIX | 0.9786 | 0.9507 | 69 | 29 | Volume Weighted Average Price. Calculated as an average of execution price, weighted by the number of shares traded for the GBDA |
| 92 | `oth143_short_sell_industry_broker_count` | MATRIX | 1.0000 | 0.9507 | 204 | 49 | Count of Unique IDs of Industry Participants |
| 93 | `oth143_short_sell_industry_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 515 | 150 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 94 | `oth143_short_sell_industry_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 235 | 56 | Anonymous market share percentage of the second most active Clearing ID in this category |
| 95 | `oth143_short_sell_industry_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 219 | 46 | Anonymous market share percentage of the third most active Clearing ID in this category |
| 96 | `oth143_short_sell_industry_concentration` | MATRIX | 1.0000 | 0.9507 | 1613 | 356 | Summation of Industry brokers' market shares squared |
| 97 | `oth143_short_sell_industry_volume` | MATRIX | 1.0000 | 0.9507 | 359 | 50 | Total Industry sum of shares, rounded to the nearest 1000. |
| 98 | `oth143_short_sell_industry_vwap` | MATRIX | 1.0000 | 0.9507 | 183 | 57 | Volume Weighted Average Price. Calculated as an average of execution price, weight by number of shares traded for the industry aggregate. |
| 99 | `oth143_short_sell_tier1_broker_rank1` | MATRIX | 1.0000 | 0.9507 | 1090 | 128 | Anonymous market share of the most active Clearing ID in this category |
| 100 | `oth143_short_sell_tier1_broker_rank2` | MATRIX | 1.0000 | 0.9507 | 184 | 40 | Anonymous market share of the second most active Clearing ID in this category |
| 101 | `oth143_short_sell_tier1_broker_rank3` | MATRIX | 1.0000 | 0.9507 | 164 | 37 | Anonymous market share of the third most active Clearing ID in this category. |
| 102 | `oth143_short_sell_tier1_concentration` | MATRIX | 1.0000 | 0.9507 | 1098 | 183 | Summation of Tier 1 brokers' market share squared |
| 103 | `oth143_short_sell_tier1_unique_brokers` | MATRIX | 1.0000 | 0.9507 | 208 | 67 | Count of Unique IDs of Tier 1 Participants. |
| 104 | `oth143_short_sell_tier1_volume` | MATRIX | 1.0000 | 0.9507 | 186 | 59 | Total Tier 1 sum of shares, rounded to the nearest 1000 |
| 105 | `oth143_short_sell_tier1_vwap` | MATRIX | 1.0000 | 0.9507 | 203 | 49 | Volume Weighted Average Price. Calculated as an average of execution price, weighted by the number of shares traded for the Tier1 aggregate |
| 106 | `rolling_gbda_broker_concentration_index` | VECTOR | 1.0000 | 0.9507 | 6 | 6 | Summation of Global Broker Dealers' market share squared. |
| 107 | `rolling_gbda_distinct_broker_count` | VECTOR | 1.0000 | 0.9507 | 1 | 1 | Count of Unique IDs of GBDA Participants. |
| 108 | `rolling_gbda_group_traded_shares` | VECTOR | 1.0000 | 0.9507 | 3 | 3 | Total GBDA sum of shares, rounded to the nearest 1000. |
| 109 | `rolling_gbda_group_vwap` | VECTOR | 1.0000 | 0.9507 | 1 | 1 | Volume Weighted Average Price. Calculated as an average of execution price, weighted by the number of shares traded for the GBDA. |
| 110 | `rolling_gbda_second_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 1 | 1 | Anonymous market share of the second most active Clearing ID in this category. |
| 111 | `rolling_gbda_third_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 1 | 1 | Anonymous market share of the third most active Clearing ID in this category. |
| 112 | `rolling_gbda_top_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 1 | 1 | Anonymous market share of the most active Clearing ID in this category. |
| 113 | `rolling_industry_broker_concentration_index` | VECTOR | 1.0000 | 0.9507 | 10 | 10 | Summation of Industry brokers' market shares squared. |
| 114 | `rolling_industry_distinct_broker_count` | VECTOR | 1.0000 | 0.9507 | 2 | 2 | Count of Unique IDs of Industry Participants. |
| 115 | `rolling_industry_group_vwap` | VECTOR | 1.0000 | 0.9507 | 2 | 2 | Volume Weighted Average Price. Calculated as an average of execution price, weight by number of shares traded for the industry aggregate. |
| 116 | `rolling_industry_second_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 0 | 0 | Anonymous market share percentage of the second most active Clearing ID in this category. |
| 117 | `rolling_industry_third_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 0 | 0 | Anonymous market share percentage of the third most active Clearing ID in this category. |
| 118 | `rolling_industry_top_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 5 | 4 | Anonymous market share percentage of the most active Clearing ID in this category. |
| 119 | `rolling_industry_traded_shares` | VECTOR | 1.0000 | 0.9507 | 3 | 3 | Total Industry sum of shares, rounded to the nearest 1000. |
| 120 | `rolling_tier1_broker_concentration_index` | VECTOR | 1.0000 | 0.9507 | 12 | 11 | Summation of Tier 1 brokers' market share squared. |
| 121 | `rolling_tier1_distinct_broker_count` | VECTOR | 1.0000 | 0.9507 | 5 | 4 | Count of Unique IDs of Tier 1 Participants. |
| 122 | `rolling_tier1_group_traded_shares` | VECTOR | 1.0000 | 0.9507 | 2 | 2 | Total Tier 1 sum of shares, rounded to the nearest 1000 |
| 123 | `rolling_tier1_group_vwap` | VECTOR | 1.0000 | 0.9507 | 2 | 2 | Volume Weighted Average Price. Calculated as an average of execution price, weighted by the number of shares traded for the Tier1 aggregate. |
| 124 | `rolling_tier1_second_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 2 | 2 | Anonymous market share of the second most active Clearing ID in this category. |
| 125 | `rolling_tier1_third_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 1 | 1 | Anonymous market share of the third most active Clearing ID in this category. |
| 126 | `rolling_tier1_top_broker_share_pct` | VECTOR | 1.0000 | 0.9507 | 3 | 3 | Anonymous market share of the most active Clearing ID in this category |
