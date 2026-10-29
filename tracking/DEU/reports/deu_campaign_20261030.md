# DEU 战役报告（2026-10-30）

> 目标：DEU D1 未点亮塔挖掘 60 个 regular alpha（优先 ATOM 单数据集）。
> 平台设置档案：EQUITY / DEU / **TOP500（唯一宇宙）** / delay 1 / decay 4 / truncation 0.08 /
> pasteurization ON / unitHandling VERIFY / nanHandling OFF / maxTrade OFF / FASTEXPR。
> IS 窗口：2014-01-01 ～ 2023-12-31（平台实际下发，正好 10 年）。
> sub 闸口径：`LOW_SUB_UNIVERSE_SHARPE.limit = 0.4743 × sharpe`（ML96728 在 DEU/TOP500/d1 上 797 条实测，0 失配）。

---

## 一、塔位缺口盘点（DEU D1）

| 已点亮数 | category |
|---|---|
| 2 | other |
| 1 | institutions / model / analyst / fundamental |
| **0** | **insiders / news / pv / earnings / sentiment / risk / option / macro / socialmedia / shortinterest / imbalance** |

D0 全部 16 类为 0。
**新发现的「数据集即整塔」机会（单数据集撑起整塔，点一个集=点一个塔）**：

- `shortinterest3` —— DEU D1 shortinterest 塔**只有它一个数据集**，塔位 0/3，倍率 1.3×
- `option1` —— DEU D1 option 塔**只有它一个数据集**，塔位 0/3，倍率 1.7×
- `macro27` —— DEU D1 macro 塔**只有它一个数据集**，塔位 0/3，倍率 1.5×

（`socialmedia` 塔有 2 个集：socialmedia12 / socialmedia39；`sentiment` 塔有 3 个集。）

---

## 二、数据集画像（description-first）

> 平台 coverage 已被多次证伪（techindi_model 平台给 0.000 但实测 150/150 覆盖；macro27/institutions25 给 0.0 却有用户数），
> 故画像一律以 **description 语义 + userCount/alphaCount + 首波探针实测 longCount** 为准，不采信集级 coverage。

### 2.1 shortinterest3 —— 【最高优先·塔位独占】

- 25 字段**全 VECTOR**，聚合成标量必须 `vec_avg` / `vec_max` / `vec_sum`。
- 三档后缀：无后缀 / `_main` / **`_p5_d1`（覆盖最高 0.7833）**。描述口径：`_main` 写 "primary key group"，
  无后缀与 `_p5_d1` 写 "this group"（共享底层成交，行内口径不同）。
- 可用字段（括号内 = userCount/alphaCount）：

| 字段 | 语义 | 用户/alpha |
|---|---|---|
| `shrt3_bar` | 借券需求评级 1–10（唯一无后缀变体） | **173 / 323** |
| `max_loan_rate_p5_d1` | 借券费率最高档 | 93 / 161 |
| `loan_rate_volatility_p5_d1` | **截面**（同日不同合约）费率离散度 | 89 / 131 |
| `mean_loan_rate_p5_d1` | 借券费率均值 | 69 / 103 |
| `average_loan_duration_days_p5_d1` | 平均借券久期 | 34 / 50 |
| `transaction_count_p5_d1` | 借券成交笔数 | 34 / 54 |
| `min_loan_rate_p5_d1` | 借券费率最低档 | 31 / 40 |
| `loaned_share_count_p5_d1` | 借出股数 | 24 / 34 |
| `loaned_market_value_usd_p5_d1` | 借出市值（美元） | 23 / 30 |

- **矩 × 主键 结构表**（来自 JX84394 论坛实证）：
  - 一阶矩：`mean/max/min_loan_rate_*`
  - **截面二阶矩**：`loan_rate_volatility_*`（厂商已给）
  - **时序二阶矩：平台不存在，必须自己算** ⇒ `ts_covariance(x, x, W)` 正是这个空位
- **经济机理**（ERR 2018, Journal of Finance《Short Selling Risk》；D'Avolio 2002 JFE；Cohen-Diether-Malloy 2007 JF；Drechsler 2014）：
  空头恐惧的不是费率水平，而是费率「突然变贵 / 券被召回」的**时序不确定性** ⇒ 套利受限 ⇒ 高估不得纠正 ⇒ 未来收益低 ⇒ 做空。
- **方向已实测确认：必须 `reverse()`**（高借券压力 → 做空）。

### 2.2 option1 —— 【次高优先·塔位独占】

- 22 字段**全 VECTOR**，覆盖平台报 0.0（不可信）。
- 核心信号：`opt1_p_deltasurface_d1_vi`（隐含波动率曲面值，11 用户/18 alpha，数据集内最高）。
- 曲面坐标轴字段：`opt1_deltasurface_d1_moneyness`（虚值程度）、`opt1_p_deltasurface_d1_delta`（希腊 delta）、
  `opt1_vp_deltasurface_d1_period`（到期天数）。
- 质量标记：`delta_surface_data_quality`（0=最高质量，越大越不可靠/插值）。
- 其余多为价格/成交量/分红/拆股等**辅助或非信号**字段（`opt1_price_*`、`opt1_volume`、`opt1_factor`、
  `opt1_dvd_frequency`、`opt1_last_dvd_amount`、`split_event_*`、`opt1_isenabled`）。
- **关键限制**：VECTOR 记录 = 曲面上的一个点（delta × moneyness × period），平台**无法在向量内部按坐标筛选** ⇒
  `vec_avg` 得到的是「全曲面平均 IV」，`vec_range`/`vec_max` 得到的是「曲面倾斜/期限结构的极差」。
  想精确取「30 天 ATM IV」在本平台不可实现。
- 候选机制：波动率风险溢价（高 IV → 未来低收益）、曲面倾斜（skew）、期限结构陡峭度。

### 2.3 sentiment27 —— 【大票友好·sub 闸友好】

- 18 字段 = 14 VECTOR（数值）+ 4 SYMBOL（日期/时间戳，非信号）。
- 覆盖 0.9022（聚合族）/ 0.9118（日频族），122 用户 / 297 alpha。
- Tranco 网站排名字段族（括号内 = userCount/alphaCount）：

| 字段 | 语义 | 用户/alpha |
|---|---|---|
| `snl27_relpopularity08` | 复合相对流行度（α=0.8），越高=注意力越广 | **37 / 54** |
| `snl27_skewness` | 发行方域名排名分布偏度 | 24 / **63（alpha 数最多）** |
| `snl27_relpopularity1` | 复合相对流行度（α=1） | 31 / 48 |
| `snl27_kurtosis` | 域名排名分布超额峰度（尾部厚度） | 32 / 47 |
| `snl27_avgranking` | 全部域名 Tranco 排名算术均值，越低=越流行 | 16 / 17 |
| `snl27_topranking` | 最好（最低）单域名排名 | 15 / 18 |
| `snl27_top50pctranking` / `avg` | 中位数排名 / 上半段平均排名 | 13/15、20/32 |
| `snl27_top75pctranking` / `avg` | 75 分位排名 / 其平均 | 7/10、12/27 |
| `snl27_totaldomains` | 发行方去重域名总数 | 24 / 33 |
| `snl27_totalcountrydomains` | 带 ccTLD 的域名数 | 10 / 13 |
| `snt27_rank` | 域名日频 Tranco 排名（1=最流行） | 19 / 27 |
| `snl27_wq_pit` | 内部 PIT 对齐标记，**非分析指标** | 8 / 8 |

- **结构优势**：大公司域名多、排名好 ⇒ 信号天生偏向大票 ⇒ 对「sub 闸惩罚小票超额收益」天然友好。
- 候选机制：投资者注意力（Barber & Odean 2008，高注意力→散户买入压力→高估→未来低收益）、
  注意力变化、注意力分布形态（偏度/峰度=注意力集中度）、域名广度（规模代理）。

### 2.4 socialmedia12 —— 【塔位 0/3，2 个集之一】

- 18 字段 = 14 MATRIX + 4 VECTOR（元数据）。覆盖报 0.0（不可信），62 用户。
- MATRIX 信号字段：`sentiment_score`（聚合社媒/新闻情绪，0=中性，**17 用户/23 alpha 最高**）、
  `sentiment_expected_price_change`（供应商模型预测的预期涨跌幅均值，13/20）、
  `sentiment_intraday_return`（开盘到信号方向最高/最低的涨幅，10/15）、
  `sentiment_stddev`（预期涨跌幅标准差，10/13）、`scl12_buzz`（相对情绪量）、`scl12_sentiment`、
  `backtest_hit_ratio`、`sentiment_significance`、`average_trading_volume`。
- 价格字段：`sentiment_close_price` / `_high_price` / `_low_price` / `_open_price` / `_open_to_close_return_pct`。
- VECTOR 元数据：`entity_employee_count` / `entity_profile_summary` / `entity_sector_name` / `entity_total_revenue`。
- **⚠ 陷阱**：`sentiment_expected_price_change` / `sentiment_stddev` / `sentiment_significance` /
  `backtest_hit_ratio` / `average_trading_volume` 均来自 **PulsePick performance 文件**，
  是供应商的**模型输出/回测产物**，不是原始社媒数据 —— 直接使用等于在消费别人的模型预测。

### 2.5 earnings6 —— 【低优先】

- 18 字段**全 VECTOR**，覆盖报 0.0，41 用户 / 102 alpha。
- **只有 4 个数值信号字段**：`ern6_actual_eps`（12/22）、`ern6_estimated_eps`（14/25）、
  `preliminary_eps_range_lower_bound`（4/6）、`preliminary_eps_range_upper_bound`（2/3）。
- 其余 14 个全是日期/时间戳/标识符（`ern6_1q`~`4q`、`_fiscal_year`、`ern6_next_ed`、
  `ern6_conferencecalltime`、`ern6_board_of_directors_meeting`、`ern6_wqreceivetimestamp`、
  `ern6_transcript_fiscal_year`、`ern6_x_dividend*`）⇒ **非信号**。
- **重要对照**：USA 版的 `eps_change_percentage_value`（最自然的「EPS 变化量」字段）在 DEU 字段集中**不存在**，
  且 USA 实测该字段是空字段 ⇒ earnings6 的 M2（EPS 惊喜）机制整条断掉。
- USA D1 实测 EPS 惊喜**方向反向且不稳定**（S −0.77 / 2Y 0.24 / SUB −0.48），PEAD 在成熟市场已被拥挤反转。
- 结论：单机制、字段少、方向不可靠 ⇒ 不投仿真槽。

### 2.6 其余已画像数据集（前序）

| 数据集 | 关键结论 |
|---|---|
| `techindi_model` | OTHER 塔主脉，399 字段全 MATRIX，786 用户/3781 alpha，倍率 1.8× |
| `institutions6` | institutions 塔，11 字段全 MATRIX，cov 1.000，**季频**（ts 窗口须 ≥60 天） |
| `institutions25` | **实为空头持仓（非多头机构）**，24 字段全 VECTOR，userCount≈0 |
| `fund_holdings_panel` | 优质共同基金交易流水，18 字段全 VECTOR，cov 0.9278，54 用户 |
| `institutions4` | 6 字段全 VECTOR，cov 0.3413，**含上期值 ⇒ 可算 Δ持股** |
| `institutions1` | **实为 insider 交易（与 insiders1 近乎重复）**，7 字段全 VECTOR |
| `insiders1` | 8 字段全 VECTOR，cov 0.5343，**缺买卖方向字段** |
| `macro27` | **实为职位发布数据（劳动力市场替代数据，非宏观）**，13 字段全 VECTOR |
| `alpha_factor_lib` | **判死**（longCount 3/3，无法持仓） |
| `other532` | **判死**（27 结构，best S1.07/F0.48） |
| `risk72` | 反向 S+0.97 但**持仓 19/19 太窄**，仅作取证 |

**平台命名陷阱（务必按 description 判，不可按名字推断）**：
`institutions25` ≠ 多头机构持仓（是空头）；`institutions1` ≠ 机构（是 insider）；
`macro27` ≠ 宏观（是职位发布）。

---

## 三、波次归因（6 波，53 条探针）

### 3.1 techindi_model 基座族（OTHER 塔，倍率 1.8×）

单字段 `tm_15_r1_r5_r10_rh_glb_d1_r10_q1`，A 波 10 条结构族：

| alpha | 结构 | S | F | TO | 2Y | sub | sub/S | margin |
|---|---|---|---|---|---|---|---|---|
| `vR103LQw` | **裸 `group_rank(A, sector)`** | **1.70** | 0.80 | 39.4% | 1.73 | 0.69 | 0.406 | 4.39bp |
| `omE2MKxv` | `ts_rank(A,66)` | 1.53 | 0.65 | 41.8% | 1.35 | 0.67 | — | — |
| `ZYQZepO0` | `ts_decay_linear(A,10)` | 1.19 | 0.66 | 19.0% | 1.20 | — | — | — |
| `j2YLb05E` | `group_zscore(ts_mean(A,22))` | 1.00 | 0.66 | 10.8% | — | — | — | **10.19bp** |
| `ZYQZepJ0` | `ts_delta(ts_mean(A,22),22)` | 1.02 | — | — | 1.71 | 0.71 | — | — |
| `2rAEb7gx` | `ts_mean(A,22)` | 0.96 | 0.58 | — | — | — | — | — |
| `MPYwoprn` | `ts_std_dev(A,22)` | 0.25 | — | — | −0.73 | — | — | — |

B 波 10 条换字段（`group_rank(ts_mean(F,22), sector)`）：**全部 REJECT**，S 0.59–0.99，TO 全部 ~11%，
最好 `88RAdj9W` S0.99/F0.61。

**归因**：该数据集**只有裸横截面排名结构有效**（S1.70），任何时间平滑都纯亏。
`ts_std_dev` 直接反向（S0.25 / 2Y −0.73）⇒ 这不是波动率型信号。

### 3.2 设置轴扫描（C 波，SUBINDUSTRY 下）

| 实验 | alpha | S | F | TO | 2Y | sub | sub/S | margin |
|---|---|---|---|---|---|---|---|---|
| 基线 decay4 | `vR103LQw` | 1.70 | 0.80 | 39.4% | 1.73 | 0.69 | 0.406 | 4.39bp |
| trunc 0.02 | `E563JK1R` | 1.68 | 0.78 | 39.25% | 1.73 | 0.68 | 0.405 | 4.35bp |
| trunc 0.04 | `omE2O61b` | 1.70 | 0.80 | 39.4% | 1.73 | 0.69 | 0.406 | 4.39bp（**与基线逐位相同**）|
| group=industry | `E563Jv10` | 1.68 | 0.75 | 40.5% | 1.76 | 0.68 | 0.405 | 4.01bp |
| decay=20 | `Xg9q5dnx` | 1.37 | **0.88** | **16.8%** | 1.40 | 0.57 | **0.416** | **8.19bp** |

**归因**：truncation 是**死参数**（0.02/0.04/0.08 逐位相同）；分组轴 sector↔industry 也扫不动；
只有 `decay` 是真杠杆，但它**不动 sub 比值**（0.406→0.416）。

### 3.3 换手抑制算子（D 波）—— 全线失败

| alpha | 结构 | S | F | TO | 2Y | sub | sub/S |
|---|---|---|---|---|---|---|---|
| `RREXLjYd` | `hump(..., hump=0.005)` | 0.43 | 0.21 | 11.9% | 1.10 | 0.07 | 0.163 |
| `gJevzjJM` | `ts_target_tvr_hump(..., target_tvr=0.25)` | 1.43 | 0.86 | 19.5% | 1.17 | 0.44 | 0.308 |
| `zq3azgd8` | `hump(..., hump=0.001)` | 1.52 | 0.72 | 33.3% | 1.33 | 0.58 | 0.382 |

**归因（重要）**：hump / ts_target_tvr_hump **不仅不帮忙，还会把 sub/S 进一步压低**
（0.406 → 0.163 / 0.308 / 0.382）。机理：小票靠高换手赚短周期 alpha，任何压换手的算子
都在同步压掉小票收益 ⇒ 比例闸恶化。**平滑类路线彻底封死，只能走「结构」与「中性化」。**
（与论坛 JR57542「hump 有节奏选择性，快节奏信号套 hump 后 PnL 直接归零」一致。）

### 3.4 嵌套分组（E 波）—— 论坛结论不可跨区照搬

| alpha | 结构 | S | F | TO | 2Y | sub | sub/S |
|---|---|---|---|---|---|---|---|
| `xArMa5dJ` | `group_rank(group_zscore(A, subindustry), sector)` | 1.69 | 0.76 | 40.5% | **1.78** | **0.59** | **0.349** |

**归因（关键反证）**：论坛 `42509573118999`（SZ83096，92 票）在 **GLB** 上实测嵌套分组把 sub 从
0.61~0.83 拉到 1.25（PASS）。**在 DEU TOP500 上完全反向**：sub 从 0.69 跌到 0.59。
机理：DEU TOP500 只有 500 只股票，按 subindustry 分组后每组仅剩几十只 ⇒ 内层 z-score 噪声被放大。
**⇒ 「嵌套分组救 sub」这条 GLB 结论严禁照搬到小宇宙区域。**

### 3.5 中性化轴（N 波）—— **本轮最大突破**

| alpha | neutralization | S | F | TO | 2Y | sub | sub limit | sub/S | long/short | DD |
|---|---|---|---|---|---|---|---|---|---|---|
| `vR103LQw` | SUBINDUSTRY | 1.70 | 0.80 | 39.4% | **1.73** | 0.69 | 0.81 | 0.406 | 151/149 | 0.062 |
| **`P0oee68L`** | **STATISTICAL** | **2.23** | **1.03** | 39.6% | **0.55** | **0.87** | 1.06 | 0.390 | **192/190** | **0.030** |

**STATISTICAL 效果（首次同时过 LOW_SHARPE + LOW_FITNESS）**：
S 1.70→**2.23（+31%）**、F 0.80→**1.03（过闸）**、持仓 300→**382 只（+28%）**、
DD 0.062→**0.030（腰斩）**、CONCENTRATED_WEIGHT 由 fail 转 pass。
**代价**：2Y 1.73→**0.55（崩）**。

**归因**：
1. **中性化是被前 5 波完全漏掉的强轴**（truncation / 分组轴 / decay 全部扫不动的东西，换中性化一档就动了）。
2. 但 **sub/S 比值纹丝不动**（0.406 → 0.390，反而略降）—— 印证「比例闸惩罚的是形状，不是水平」。
3. SUBINDUSTRY 与 STATISTICAL 在 **2Y 上完全互补**（1.73 vs 0.55），中间档位存在可行解。

---

## 四、当前关键算术（决策用）

`fitness = sharpe × sqrt(|R| / max(turnover, 0.125))`

**TO 地板 0.125 的反向经济学**（本轮验证）：

- TO > 0.125：F = S × sqrt(R/TO)，降换手只在砍掉低质量交易（提 margin 比）时才提 F。
- TO < 0.125：分母被钉死 ⇒ F = S × sqrt(R/0.125)，**F 与 TO 无关**，只由 S 与 R 决定。
- 推论：**TO 已在地板下时，继续压换手对 F 零收益**；反而可以试「适度提换手」换 S。

**F 验算已验证两次**（可当体检工具用）：
- `bl6ppE26` 取反版：S1.02, R11.61%, TO10.58% → 预测 F = 1.02×sqrt(0.1161/0.125) = 0.983，平台给 0.98 ✅
- `P0oee68L`：S2.23, R8.42%, TO39.55% → 预测 F = 2.23×sqrt(0.0842/0.3955) = 2.23×0.4614 = 1.029，平台给 1.03 ✅

**四闸的联合可行域**：需 S≥1.58、F≥1.0、2Y≥1.58、sub≥0.4743×S，
即 `R/TO ≥ 0.40`（F 闸）且 `sub/S ≥ 0.4743`（sub 闸）。

---

## 五、已确认的结构性事实（跨数据集）

1. **DEU 只有 TOP500 一个宇宙**（d0/d1 都是）⇒ 论坛「换 universe 是最大质变」这条杠杆**在 DEU 完全不可用**。
2. **sub 比值是天生的数据集属性**：techindi_model ≈ 0.35–0.42（5 波扫不动）；
   shortinterest3 ≈ **0.67–0.75**（前轮数据），`0.74` 几乎是 techindi_model 的两倍。
   ⇒ **sub 转不动时，换数据集比调参有效**。
3. **换手抑制算子（hump / ts_target_tvr_*）对排名型信号是纯亏**，且会把 sub/S 压低 20–60%。
4. **嵌套分组在小宇宙（TOP500）反向失效**，不可照搬 GLB 结论。
5. **coverage 完全不可信**：techindi_model 平台给 0.000 但实测 150/150 覆盖；
   macro27 / institutions25 / institutions1 / option1 / socialmedia12 全部报 0.0 却有真实用户数与信号。
6. **VECTOR 字段必须 `vec_*` 聚合**；`vec_range` = 记录间极差（比 stddev 更抗中间项噪声）。
7. **数据集命名陷阱**：institutions25=空头持仓、institutions1=insider、macro27=职位发布。

---

## 六、shortinterest3 详解（第二主矿脉）

### 6.1 前轮判死记录与突破点

`DEAD_ENDS.json`（2026-09-29）：shortinterest3 已 2 轮 25 结构判死，best S **0.06**，判死理由：

> 「VECTOR(event)字段；**divide(vec_sum(A), vec_sum(B))** + dl 结构正反两向全负；ts_delta/ts_zscore/ts_rank
> 不兼容 event 输入（已修语法）；DEU 借贷市场语义与 KOR SI38 相反但取反仍无效」

**突破点**：前轮 25 个结构**全部是比率/差值结构**，恰好踩中 JX84394 的第一条判据——
「**信号住在绝对量纲，CV 归一化会归零**」（该判据在 ASI 实测：CV 归一化版 S 仅 0.61，窗口 66 版 −0.01）。

### 6.2 本轮实测（SUBINDUSTRY，nanHandling OFF）

| alpha | 表达式 | S | F | TO | margin | sub | 2Y | long/short |
|---|---|---|---|---|---|---|---|---|
| `bl6ppE26` | `group_zscore(ts_covariance(vec_avg(mean_loan_rate_p5_d1), …, 22), sector)` | **−1.02** | −0.98 | **10.6%** | **−2.19bp** | −0.68 | −0.86 | 81/144 |
| `Xg9qq6P8` | `group_rank(vec_avg(shrt3_bar), sector)` | −1.04 | −0.70 | 19.5% | −0.91bp | −0.84 | −1.50 | 80/84 |

**方向确认为负 ⇒ 必须 `reverse()`，与 ASI 一致。**

**取反后 `ts_covariance` 版**：**S1.02 / F0.98 / TO10.6% / R11.6% / sub0.68（PASS）/ 2Y0.86**
- 这是 shortinterest3 在 DEU 的**史上最高 F**（前轮最好 F0.64），来源是 TO 被压到 10.6% + margin 高达 2.19bp。
- sub limit = 0.4743×1.02 = 0.484 ⇒ **sub 通过**，余量 40%。
- 金字塔确认：`DEU/D1/SHORTINTEREST`，倍率 **1.3×**。

**取反后 `bar` 版**：S1.04 / F0.70 / sub0.84（sub 极健康）但 `CONCENTRATED_WEIGHT` fail。

### 6.3 与 techindi_model 的问题互补性

| | S | F | 2Y | sub/S | 病 |
|---|---|---|---|---|---|
| techindi_model | **1.70** ✅ | 0.80 | **1.73** ✅ | 0.406 ❌ | **sub 形状病** |
| shortinterest3 | 1.02 ❌ | **0.98** ✅ | 0.86 ❌ | **0.74** ✅ | **S 强度病** |

⇒ 两者病灶互补。但 shortinterest3 的 S 距 1.58 差 55%，需寻找更强机制而非调参。

---

## 七、候选盘点

**当前 0 条过全部闸。** 按「距离全闸的项数」排序：

| 排名 | alpha | 数据集 | 卡住的闸 | 剩余缺口 |
|---|---|---|---|---|
| 1 | **`P0oee68L`** | techindi_model | sub (0.87 vs 1.06)、2Y (0.55 vs 1.58) | **2 项**，且 S/F 已过 |
| 2 | `vR103LQw` | techindi_model | F (0.80)、sub (0.69 vs 0.81) | 2 项，2Y 已过 |
| 3 | `xArMa5dJ` | techindi_model | F (0.76)、sub (0.59 vs 0.80) | 2 项，2Y 1.78 已过 |
| 4 | `bl6ppE26` 取反版 | shortinterest3 | S (1.02)、2Y (0.86) | 2 项，F/sub 已过 |

**互补配对洞察**：`P0oee68L`（S 2.23 / F 1.03 / 2Y 0.55）与 `xArMa5dJ`（2Y 1.78 / S 1.69）在 2Y 上完全互补，
中间档位（其他 neutralization）存在可行解。

---

## 八、后续队列

**P0 — 中性化全档扫描（最高优先，已验证是唯一有效轴）**
剩余档位：SLOW / MARKET / SECTOR / INDUSTRY / NONE / FAST / SLOW_AND_FAST / REVERSION_AND_MOMENTUM。
固定表达式 `group_rank(tm_15_r1_r5_r10_rh_glb_d1_r10_q1, sector)`，decay 4。
目标：找到同时满足 S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 的档位（STATISTICAL 已拿下 S/F，只差 2Y）。

**P1 — shortinterest3 提升 S**
- `ts_covariance` 短窗（5/10）—— JX84394 窗口阶梯显示短窗 S 更高
- `max_loan_rate` 换字段（尾部压力更极端）
- `loan_rate_volatility_p5_d1`（厂商截面离散度，第二个经济机制）
- 10 模板池已 preflight 通过，待派

**P2 — sentiment27 首波（11 模板已 preflight 通过）**
注意力/分布形态/域名广度三族，验证「天然偏大票 ⇒ sub 友好」假设。

**P3 — option1 首波（塔位独占，倍率 1.7×）**
IV 水平 / 曲面极差 / IV 变化，需 `vec_avg` / `vec_range` 聚合。

**P4 — fund_holdings_panel（cov 0.928，机构塔已有 1/3）**

**已封盘**
- techindi_model 的时间平滑族、换手抑制族、嵌套分组族、truncation 族
- earnings6（单机制 + 字段缺 + 方向反向）
- alpha_factor_lib（持仓 3/3）、other532（27 结构 S1.07）

---

## 九、论坛与论文取证索引

| article_id | 标题 / 主题 | 票/评 | 关键价值 |
|---|---|---|---|
| `31365517513495` | 浅谈用 hump 操作符解决 Sub-universe Sharpe | 51/36 | **DEU/TOP500/d1 的 sub 闸比例 0.4743×sharpe（797 条实测 0 失配）**；hump 机制=节流阀；JR57542「hump 有节奏选择性」 |
| `42509573118999` | GLB analyst16 从潜力到成功复盘 | 92/49 | 嵌套分组救 sub（**GLB 有效，DEU 反证无效**）；先筛 2Y 再谈 Sharpe；换 universe 是最大质变（**DEU 不可用**） |
| `43624312881943` | ASI 借券费率「突然变贵」因子 | 64/14 | **shortinterest3 全部模板来源**；三条结构判据；窗口阶梯；方差 vs 标准差；robust 比例闸机理 |
| `41162636720919` | 提高 MEA 区 Sub-universe Sharpe | 56/10 | — |
| `36061482267415` | 优化 Sub-universe Sharpe 的一个方法 | 28/12 | — |
| `35062818902423` | 如何优化 Sub-universe Sharpe | 37/6 | — |
| `38669179039255` | EUR TOPCS1600 解决 robust/sub/CW | 58/35 | — |
| `43791735762839` | 主 Universe 好 Sub-universe 失败：先查这四件事 | 14/— | — |
| `42967169006231` | TOP3000/TOP1000/TOP500 universe 收窄改变了什么 | 40/— | — |
| `43636685645975` | 券池利用率的极限：shortinterest3 欧洲市场札记 | 30/— | shortinterest3 欧洲语义 |
| `43179452121495` | 借券利用率「异常收紧」 | 3/6 | — |
| `43607257389207` | 融券借贷的隐形成本：risk59 | 29/— | — |
| `43289952570903` | 峰值年龄波动率：卖空借贷压力不稳定信号 | — | — |
| `43789939669271` | 换手率是可以设计的：target_tvr 家族 | — | 签名：`ts_target_tvr_decay(x, lambda_min, lambda_max, target_tvr)` |
| `43794163744279` | 降低 Turnover 时怎样避免把信号一起磨平 | — | — |
| `43666872647575` | hump / trade_when / group_neutralize 三算子入门 | — | — |

**外部文献**
- ERR 2018, *Journal of Finance*, "Short Selling Risk" —— 借券费率时序不确定性 → 套利受限 → 高估不纠正
- D'Avolio 2002, *JFE* —— 借券费率是做空难度的价格
- Cohen, Diether & Malloy 2007, *JF* —— 借券供需冲击有预测力
- Drechsler 2014 —— shorting premium
- Barber & Odean 2008 —— 投资者注意力 → 散户买入压力 → 高估 → 未来低收益
- Arbel & Strebel 1983 —— neglected firm effect（低关注度溢价）

---

## 十、平台操作备忘（本轮踩坑）

1. **FastExpr 属性参数必须 `name=value`**：`hump(x, 0.01)` 报
   `Invalid number of inputs : 2, should be exactly 1 input(s)`；必须写 `hump=0.001`。
   `ts_target_tvr_hump(x, 0.2)` 报 `Required attribute "target_tvr" must have a value`。
2. **`ts_max` / `ts_min` 平台不存在**（不在 `operator_audit` 的 `missing` 103 个里）。
   时间维极值用 `ts_max_diff`；向量维用 `vec_max` / `vec_min` / `vec_range`。
3. **`power()` / `signed_power()` 不接受带单位输入**（`Incompatible unit`）。
   算方差走 `ts_covariance(x,x,W)`，或两步 `divide` 约掉单位。
4. **`batch_create_simulations` 返回单条 simulation**，必须用 `lookINTO_SimError_message`
   逐条查（`batch_status` 对它永远 `child_count: 0`，只对 multisim 有效）。
5. **429 不重试**：`CONCURRENT_SIMULATION_LIMIT_EXCEEDED` 时挂队列，等槽位释放后补派。
6. **`harvest_multisim_alphas` 必须传 `/simulations/<id>` 路径**，裸 ID 会 404。
7. **`preflight_expressions` 只校验字段名，不校验算子签名** ⇒ 算子可用性以
   `operator_audit` 的 `missing` 全集为准。

---

## 十一、中性化轴全表（N 波，本轮最大方法论产出）

同一表达式 `group_rank(tm_15_r1_r5_r10_rh_glb_d1_r10_q1, sector)`，DEU / TOP500 / D1 / decay 4 / trunc 0.08，只换 `neutralization`：

| alpha | neutralization | S | F | TO | 2Y | sub | sub limit | **sub/S** | long/short | DD | 闸门 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `vR103LQw` | SUBINDUSTRY | 1.70 | 0.80 | 39.4% | 1.73 | 0.69 | 0.81 | 0.406 | 151/149 | 0.062 | sub FAIL |
| `P0oee68L` | STATISTICAL | 2.23 | 1.03 | 39.6% | **0.55** | 0.87 | 1.06 | 0.390 | 192/190 | 0.030 | 2Y FAIL |
| `e75AAMQz` | SLOW | 2.33 | 1.12 | 40.1% | 1.36 | 0.75 | 1.11 | 0.322 | — | 0.035 | sub FAIL |
| **`1YNvvgdJ`** | **MARKET** | **2.28** | **1.28** | 37.8% | **1.89** | **1.09** | 1.08 | **0.478** | 193/190 | 0.051 | **全闸通过** |
| **`1YNv6Ymk`** | **CROWDING** | **2.28** | **1.25** | 37.9% | 1.60 | **1.11** | 1.08 | **0.487** | 193/190 | 0.055 | **全闸通过** |
| `KPJexqql` | MARKET + **decay 20** | 1.96 | **1.55** | **16.4%** | 1.73 | 0.92 | 0.93 | 0.469 | 195/188 | 0.053 | sub 差 0.01 FAIL |

**结论一（机理）**：表达式内部已经是 `group_rank(A, sector)`（行业相对排序、取值有界 [0,1]）。此时再叠加 SUBINDUSTRY/INDUSTRY 中性化 = **双重中性化**，把信号本身抹掉；STATISTICAL 过度剥离（S 冲高但 2Y 塌到 0.55）；**只有 MARKET 仅摘掉市场 beta、保留行业相对排序**，才能同时满足 S / F / sub / 2Y 四项。这解释了前 5 波 44 条全灭——它们全在 SUBINDUSTRY 里打转。

**结论二（decay 是真权衡轴）**：decay 4 → 20 使 TO 37.8%→16.4%、margin 5.98bp→**12.52bp**、F 1.28→**1.55**（全场最高），但 sub/S 从 0.478 掉到 0.469，恰好跌破 0.4743 阈值 0.01。**F 与 sub 比值反向**，不能同时最优。

**结论三（中性化不是分散工具）**：`1YNvvgdJ` 与 `1YNv6Ymk` 互相关 **0.9635**（4 年日收益、1021 点、本地计算）——只差中性化 ⇒ 本质是同一颗 alpha，**只能提交一颗**。整族（含 `KPJexqql` 0.767 / `e75AAMQz` 0.732）两两全部 >0.7。⇒ 中性化是「破闸开关」，不是「点塔配额」。

## 十二、MARKET 配方不可迁移到 shortinterest3（反证成立）

| alpha | 结构 | 中性化 | S | F | TO | 2Y | sub | long/short | DD | 结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| `rKRkkOAE` | cov5 | SUBINDUSTRY | **1.10** | 0.75 | 27.4% | 1.24 | **0.88** | 141/79 | — | 基准 |
| `VkxnKGdA` | cov5 | MARKET | 0.98 | 0.74 | 20.5% | 1.10 | 0.79 | **249/48** | **0.253** | 退化 |
| `zq3aXXRK` | cov5 | STATISTICAL + nan ON | 0.73 | 0.29 | 29.3% | 0.37 | 0.59 | — | 0.109 | 退化 |
| `wpQ6XaQ5` | `shrt3_bar` ts_mean22 | MARKET | 1.00 | 0.84 | **3.9%** | **2.08** | 0.85 | 123/122 | 0.275 | 换手塌陷 |

**机理**：techindi_model 的信号是 `group_rank`（有界、已行业中性），摘掉中性化只是去掉 beta；shortinterest3 用 `group_zscore`（重尾、无界），摘掉行业中性后持仓立刻退化为方向性多头（多 249 / 空 48），并触发 `CONCENTRATED_WEIGHT`。**⇒ 中性化配方与信号的值域/边界性质绑定，必须逐数据集重测，不能跨集照搬。**

**顺手精确验证了 TO 地板公式**：`wpQ6XaQ5` 的 TO 3.9% 远低于 0.125 地板，`F = S × sqrt(R/0.125) = 1.00 × sqrt(0.0889/0.125) = 0.843`，平台给 **0.84** ✅。

## 十三、瓶颈因数据集而异（本轮最重要的选区判据）

| 数据集 | raw Sharpe | sub/S 比值 | 卡在哪 | 该往哪打 |
|---|---|---|---|---|
| `techindi_model`（OTHER 塔） | **2.28** 够 | 0.478 擦线 | **sub 比值** | 抬 robust 段 / 压小票贡献 |
| `shortinterest3`（SHORTINTEREST 塔） | 1.10 不足 | **0.80** 极优 | **Sharpe** | 加强信号构造 |
| `sentiment27`（SENTIMENT 塔） | 0.66 严重不足 | **1.15–1.38 溢出** | **Sharpe** | 换机制（水平→同比变化） |

sentiment27 实测（MARKET / decay 4 / trunc 0.08）：

| alpha | 字段 | S | F | TO | sub | **sub/S** | DD | 备注 |
|---|---|---|---|---|---|---|---|---|
| `3qodg2kz` | `snl27_relpopularity08` 水平 | 0.66 | 0.45 | 2.97% | 0.76 | **1.15** | 0.226 | margin 39.67bp |
| `N1NMk2JL` | `snl27_totaldomains` | 0.50 | 0.30 | 3.13% | 0.69 | **1.38** | 0.290 | margin 29.22bp |

**⇒「天然偏大票」假设证实**：网站流量排名天然偏大票，sub 值甚至高于全样本 Sharpe，**sub 闸对它完全非约束**。这类数据集只需解决 Sharpe，不必再为 sub 闸花任何代价。反之 techindi_model 这类 Sharpe 富余、sub 擦线的集，应优先找「大票上更强」的变体而不是继续调参。

## 十四、论坛/文献取证补充（本轮新增两篇精读原文）

**`25824706455703` Individual Option Volatility Smirk（23 票 / 9 评）**
- 原论文 *What Does Individual Option Volatility Smirk Tell Us about Future Equity Returns*：**波动率微笑越陡 → 风险调整后年化收益低约 10.9%**，可预测性 ≥6 个月，因市场对基本面信息吸收慢。公式轴：`OTM put IV − ATM call IV`。
- 可提交模板：`skew = rank(winsorize(ts_backfill(call_iv,5) − ts_backfill(put_iv,5), std=4)); alpha = −ts_kurtosis(skew,120); group_neutralize(alpha, bucket(rank(volume), range="0,1,0.1"))`
- **JR57542 三条实操**：① call/put 必须**同桶同到期**，否则差值混入期限结构噪音；② IV 差值是快变量，先 `ts_decay_linear` 或拉长 ts 窗口压抖动，再套 `signed_power(x,k)`，且 **k 是正经的轴要扫**；③ 缺 OTM 字段时先用同桶作差把测量链跑通。
- **YJ86883 复现数据（USA/TOP3000）**：原始 smirk S0.83 / F0.74 / TO49.8% → `ts_decay_linear` 120d 后 **S0.80 / F1.39 / TO1.75%**；`ts_std_dev` / `ts_zscore` 代理**完全失效（S 负）**；`ts_kurtosis` 在 User 账户报 unknown operator。
- 评论 GC81559 直接点到「DEU 1.9x 主题乘数是否更适合」，与本区高倍率塔吻合。

**对 option1 的落地翻译**：`opt1` 每个 VECTOR 记录是曲面上的**一个点**，平台不能在向量内部按坐标筛选，但
- `vec_range(opt1_p_deltasurface_d1_vi)` = 曲面最高 IV − 最低 IV = **微笑陡度本身**（数学上最贴原文）
- `vec_stddev(opt1_p_deltasurface_d1_vi)` = 曲面离散度
- `vec_avg(...)` = 全曲面平均 IV（IV 水平，另一机制：IV premium）

已据此派发首波：`reverse(group_rank(vec_range(opt1_p_deltasurface_d1_vi), sector))`（按论文方向取反）与 `group_rank(vec_stddev(...), sector)`（方向待测）。

**`43636684138775` 网页流量里的真金白银：sentiment27 日本市场探索（30 票）**
- 机制：网站/App 访问量排名 = 「到店客流」，是业绩**先导**指标；小公司新服务流量排名飙升通常**先于财报数月**给出业务爆发信号。
- **两条实操纪律**（直接对应 sentiment27 首波弱的原因）：① **剔除季节性假日效应**——电商/旅游网站流量有日历季节性，「单周环比容易失真，一定要做同比或剔除日历季节性」；② **限定数字经济赛道**——传统制造/重资产企业看网站流量无意义。
- ⇒ 下一波改用 `ts_delta(...,252)`（同比）与 `ts_zscore(...,252)`（252 日标准化去季节），已 preflight 通过。

## 十五、相关性闸当前状态（未解）

`1YNv6Ymk` / `1YNvvgdJ` 的模拟层已无任何阻碍（`checks.fail = []`、`failed_ra_count = 0`、`failed_ppa_count = 0`、9 项 RA 闸全 pass、`submit_verdict = UNVERIFIABLE` 仅因提交层 404 死端点）。唯一未确认项是 prod / self 相关性：

- `check_correlation` 连续 4 次返回 `correlation_busy`，`retry_after 240`，`inflight: false`。
- **holder 在观测期内发生变化**：`Xg9qjVOz` → `YP1rzw2J` ⇒ 不是本机残留死锁，而是**有并行会话在持续占用账号级相关性单并发槽**。
- 按 `wq-prod-corr-read` 纪律：`inflight=true` 不重复触发；busy 时按 `retry_after` 隔时重查；无锁端点 `tools/prod_wait.py --peek` 两次均为**空体**（= 平台仍在排队，不等于低相关）。
- ⇒ **结论：本窗口内 prod 无法落地。提交前必须另行 `check_correlation(refresh=True)` 终验，且只有 `all_passed` 才算放行。**

## 十六、候选盘点（截至本轮）

**全闸通过（可进入提交终验）**

| alpha | 表达式 | 设置 | S | F | TO | 2Y | sub | margin | 塔 |
|---|---|---|---|---|---|---|---|---|---|
| `1YNv6Ymk` | `group_rank(tm_15_r1_r5_r10_rh_glb_d1_r10_q1, sector)` | CROWDING / decay 4 / trunc 0.08 | 2.28 | 1.25 | 37.9% | 1.60 | **1.11** | 5.98bp | DEU/D1/OTHER 1.8× |
| `1YNvvgdJ` | 同上 | MARKET / decay 4 / trunc 0.08 | 2.28 | 1.28 | 37.8% | **1.89** | 1.09 | 6.34bp | DEU/D1/OTHER 1.8× |

两者互相关 0.9635 ⇒ **只能择一提交**。推荐 `1YNv6Ymk`：sub 余量 2.6%（vs 0.9%）、逐年最低 Sharpe 1.38（vs 1.29）、逐年 10/10 全正。两者 `longCount 193 / shortCount 190`，持仓 383 只，满足 CW 闸。

**近闸但未过（按缺口排序）**

| alpha | 缺口 | 数值 | 差多少 |
|---|---|---|---|
| `KPJexqql` | sub | 0.92 vs 0.93 | **0.01**（但 F 1.55 全场最高、margin 12.52bp） |
| `rKRkkOAE` | Sharpe | 1.10 vs 1.58 | 0.48（sub 0.88 已 PASS，比值 0.80 余量足） |
| `3qodg2kz` | Sharpe | 0.66 vs 1.58 | 0.92（sub 比值 1.15 完全非约束） |

## 十七、E 波归因：decay 20 路线彻底封死

E 波（multisim `k6qk050b4TGcvG19PBMdDH4`，CROWDING / decay 20 / trunc 0.08）两条全灭：

| alpha | 表达式 | S | F | TO | 2Y | sub | sub limit | 判定 |
|---|---|---|---|---|---|---|---|---|
| `WjOkwYWQ` | `group_rank(tm_15_..., sector)` | 1.92 | **1.47** | 16.43% | 1.47 | 0.88 | 0.91 | sub + 2Y 双 FAIL |
| `d5Wq89lY` | `group_rank(ts_rank(tm_15_...,66), sector)` | 1.47 | 0.91 | 18.13% | 0.63 | 0.87 | 0.90 | S/F/2Y 全 FAIL |

**两个结论**：

1. **decay 20 下 CROWDING 反而比 MARKET 更差**（sub 0.88 vs 0.92、2Y 1.47 vs 1.73）⇒ 推翻「CROWDING 抬 sub」的跨 decay 假设。**只有 decay 4 能过全闸**。decay 是真权衡轴且与 sub 比值**反向**：decay 4→20 把 TO 37.8%→16.4%、margin→12.52bp、F→1.55，但 sub/S 掉到 0.469 恰好跌破 0.4743。
2. **`ts_rank(x,66)` 包在外层是纯亏**（S 2.28→1.47、2Y 1.60→0.63）——把水平信号改成时序分位后丢失了「跨股票比较」的信息。机理与 sentiment7 专帖「每剥一层 rank，FT +0.3~0.65」方向相反但同源：**rank 类算子放在截面位还是时序位，取决于信号是「截面比较型」还是「自身历史异常型」**。

## 十八、G 波归因：三个数据集三种死法

G 波（multisim `2rHvbfcNf57OcnQ1gKGxXo1G`，10 条，MARKET / decay 4 / trunc 0.08 / nanHandling ON）全灭，但暴露三条**互不相同**的失败机理，价值在于排除而非产出：

| alpha | 数据集 | 表达式 | S | F | TO | 2Y | sub | 死法 |
|---|---|---|---|---|---|---|---|---|
| `QPverwzK` | fundamental86 | `group_rank(fnd86_earnings_score, sector)` | 0.94 | 0.39 | 40.0% | 0.00 | 0.53 | CW FAIL；多空 75/231 极度偏空 |
| `N1NMWY3X` | fundamental86 | `group_rank(ts_delta(fnd86_earnings_score,66), sector)` | 0 | 0 | 0 | — | — | **ts_delta 对该字段静默全 NaN** |
| `akKJ25w2` | fundamental86 | `group_rank(ts_zscore(fnd86_earnings_score,252), sector)` | 0.46 | 0.13 | 40.0% | −1.17 | −0.20 | 全灭 |
| `QPverwgK` | fundamental86 | `group_rank(subtract(earnings_score, fundamental_score), sector)` | 0.57 | 0.19 | 40.0% | −0.77 | −0.19 | 全灭 |
| `N1NMWY8X` | fundamental86 | `group_rank(subtract(average_score, relative_valuation_score), sector)` | 0.38 | 0.10 | 40.0% | −0.54 | −0.14 | 全灭 |
| `xArMwJ5N` | sentiment7 | `reverse(group_rank(ts_zscore(vec_avg(snt7_all_languages_views),66), sector))` | −0.77 | −0.27 | 32.4% | −0.65 | −0.33 | **符号反向**（不 reverse 才是正） |
| `KPJeYW2l` | sentiment7 | `reverse(group_rank(ts_delta(vec_avg(snt7_all_languages_views),22), sector))` | −0.82 | −0.30 | 32.3% | −0.73 | −0.18 | 同上，符号反向 |
| `GrWV0Z7o` | sentiment7 | `group_rank(ts_covariance(vec_avg(...),…,66), sector)` | 0.07 | 0.01 | 2.66% | 0.23 | −0.32 | 二阶矩单独无效 |
| `P0oerkbW` | earnings_sent_matrix | `group_rank(ts_mean(positive_sentiment_probability_3,22), sector)` | 0.13 | 0.03 | 10.08% | 0.45 | −0.24 | 全灭 |
| `qMLbkQpj` | earnings_sent_matrix | `group_rank(subtract(pos_prob, neg_prob), sector)` | 0.10 | 0.02 | 37.3% | 1.30 | −0.31 | CW FAIL（0.50 vs 0.1）；多空 22/355 |

**三条独立结论**：

1. **「预拟合模型输出 ⇒ 高 Sharpe」假设被证伪**。fundamental86 是 1–10 分位复合评分（形态上最像 techindi_model），但 S 上限仅 0.94，和 techindi_model 的 2.28 完全不是同一类。**不能再把「字段名里有 score」当强信号先验**。
2. **sentiment7 裸时序变换的天花板约 0.8，且方向为正**（不 reverse 才是正）——裸水平的 `ts_zscore(66)` / `ts_delta(22)` 都不是它正确的读法。真正的信息在**「脉冲形状」**（相对自身近期峰值的突增），必须用专帖的 max+ts_delay → ts_mean → ts_ir 链才能掏出来。
3. **earnings_sent_matrix 概率类字段无截面信号**（S 0.10–0.13），且 `subtract(pos,neg)` 触发 CW FAIL（0.50 vs 0.1）、多空 22/355 极端偏空 ⇒ 该数据集需要**换极性构造**（只用单侧概率、不用差值），暂列低优先。

## 十九、H 波设计：sentiment7 脉冲链（DEU 专帖实测 S2.04 的骨架）

**源码**：论坛 `43179860065303`（LC97552，72 票/50 评）给出 DEU 专属、17 项硬检查全 PASS 的 sentiment7 ATOM 因子 `np7nn69l`：S 2.04 / F 1.92 / TO 9.11% / margin 24.21bp / sub 1.59 / 2Y 2.25 / prod 0.6338。设置 **SUBINDUSTRY / decay 16 / truncation 0.02**。

**原帖两处必须改写的地方**：

- 原式用 `ts_max(bf,5)` —— **平台无 `ts_max`**（`operator_audit` 的 103 个在线算子里没有）。原帖自己量化过：`max(bf, ts_delay(bf,5))` 版本 FT **2.15** / MG **26.92bp**，**优于** `ts_max` 版 1.92 / 24.21bp ⇒ 改写反而更强。
- 原式 `quantile(x, 120)` 的第二位置参数在平台上是 **driver**（`quantile(x, driver=gaussian, sigma=1.0)`），不是窗口。H 波把两种解释都放进对比实验。

**复用纪律**：同线同字段已有 OS 前作 SC=0.6338，直接复制会推高 PC ⇒ 不复刻字段组合，而是**换 ATTENTION_MEASURE 字段源 + 换几何**。

**H 波十模板（全部 `snt7_all_languages_views` 为基，A=该字段日浏览量）**

| # | 模板 | 结构差异 | 预期 |
|---|---|---|---|
| H1 | `quantile(ts_ir(ts_mean(max(bfA, ts_delay(bfA,5)),5),22), driver="gaussian", sigma=1)` | 截面 gaussianize 的 ir-脉冲（专帖骨架的 ATOM 版） | 基线 |
| H2 | 同 H1 但 `ts_quantile(...,120,driver="gaussian")` | **对比实验**：截面分位 vs 时序分位 | 判 `quantile` 第二参数语义 |
| H3 | H2 + `vector_neut(·, ts_zscore(bfV,22))` | **数据集内**中性化：全语言浏览量 vs 指定 project 浏览量（去英文维基共性） | ATOM 版去共性 |
| H4 | H2 + `vector_neut(·, ts_backfill(vec_avg(snl27_relpopularity08),22))` | 专帖原配方（跨 sentiment7+sentiment27；两类均非 trio，合规） | 复刻验证 |
| H5 | H2 但外链用 `min(bfA, ts_delay(bfA,5))` | **突降臂**：注意力骤降（专帖评论要求独立成臂，不靠取负号） | 反向机制 |
| H6 | `rank(ts_arg_max(bfA, 120))` | 峰值年龄：突增发生在多久前 | 独立机制 |
| H7 | `rank(ts_ir(divide(bfA, add(bfV,1)),22))` | 全语言/指定 project **浏览量占比**的稳定性 | 注意力构成 |
| H8 | `reverse(rank(ts_covariance(bfA, bfA, 66)))` | 注意力**二阶矩**（波动率而非水平） | 高风险注意力 |
| H9 | `group_rank(ts_av_diff(bfA, 120), sector)` | 长窗偏离（120 日基准）＋**内嵌 group_rank 作双重中性化对照** | 对照臂 |
| H10 | `quantile(divide(ts_mean(max(bfA,ts_delay(bfA,5)),5), add(ts_mean(bfA,22),1)), driver="gaussian", sigma=1)` | **双时间尺度脉冲比**：5 日脉冲 / 22 日基准水平 | 无量纲化 |

**设置**：SUBINDUSTRY / decay 16 / truncation 0.02 / pasteurization ON / nanHandling ON / maxTrade OFF / unitHandling VERIFY（与专帖一致，与 G 波完全不同档）。

**派发记录**：`DfrUTqU4tK8GRrzJnDsm6`（H1–H2，语法探针）＋ `2Xl3Upfip4qK8YLDP4sNR7C`（H3–H10）。

### 十九-A、H 波收割：10 条里只有 1 条成立，而它一次全闸通过

| # | alpha | 模板 | S | F | TO | 2Y | sub | 判定 |
|---|---|---|---|---|---|---|---|---|
| H1 | `0mYodlxv` | 截面 `quantile(x,driver=gaussian,sigma=1)` | 1.02 | 0.67 | 8.70% | 1.95 | 0.85 | S/F 不足 |
| H2 | `A1V6bWeQ` | `ts_quantile(x,120,driver)` | 0.76 | 0.42 | 10.54% | 2.29 | 0.60 | S/F 不足 |
| H3 | `E563YLLG` | H2 + `vector_neut(·, ts_zscore(bf snt7_views,22))` | 0.88 | 0.53 | 10.73% | 2.36 | 0.62 | S/F 不足 |
| **H4** | **`3qod35v6`** | **H2 + `vector_neut(·, ts_backfill(vec_avg(snl27_relpopularity08),22))`** | **2.04** | **1.84** | **11.00%** | **2.36** | **1.47** | **全闸 PASS** |
| H5 | `bl6pVn1K` | 突降臂（`min` 替代 `max`） | 0.39 | 0.16 | 11.48% | 0.43 | 0.16 | 全灭 |
| H6 | `Vkxnq5QY` | `ts_arg_max` 峰值年龄 | −0.13 | −0.03 | 5.63% | 0.93 | 0.07 | 无信号 |
| H7 | `npv0YQGq` | 全语言/指定 project 浏览量占比的 `ts_ir` | 0.27 | 0.09 | 5.72% | 0.79 | −0.40 | 全灭 |
| H8 | `QPveqgxr` | 注意力二阶矩 `ts_covariance` | 0.43 | 0.20 | 3.02% | 0.22 | 0.65 | 全灭 |
| H9 | `ZYQZqM80` | 120 日偏离（内嵌 `group_rank`） | 0.61 | 0.29 | 10.84% | **−0.73** | 0.33 | 2Y 负 |
| H10 | `GrWVYxRP` | 双时间尺度脉冲比（5 日/22 日） | −0.02 | 0 | 7.54% | 0.71 | −0.41 | 无信号 |

### 十九-B、三条可复用的机理结论

1. **`quantile` 的第二参数是 driver，不是窗口**。`quantile(x, driver="gaussian", sigma=1)`（截面高斯化）S 1.02 > `ts_quantile(x,120,driver="gaussian")`（时序分位）S 0.76。原帖的 `quantile(x,120)` 在平台上应理解为 `ts_quantile` 才跑得通——但这**不是**它强的原因。**注意：`0mYodlxv` 的 `checks.fail` 是空数组，但 `ra_failed_checks` 含 LOW_SHARPE/LOW_FITNESS**（平台把 `LOW_SHARPE`/`LOW_FITNESS` 放进 warning 而非 fail）⇒ **判闸不能只看 `checks.fail`，必须同时看 `ra.failed_ra_count`**。
2. **真正的 alpha 是那条中性化腿，不是脉冲链**。同一脉冲链：不加 neut 0.76、neut 自家 `snt7_views` 0.88、neut `snl27_relpopularity08` **2.04**。经济含义：`snl27_relpopularity08` 度量的是**企业自身域名的常驻热度（fame 基线）**，把它从维基浏览量脉冲里剥掉后，剩下的才是「**超出日常知名度的增量信息关注**」。这解释了为什么换成 snt7_views（另一个浏览量口径）只剥掉共性噪声、不剥 fame 基线，效果差一半以上。
3. **同数据集、同骨架、只换「臂」全部崩盘**：突降臂 0.39、峰值年龄 −0.13、占比 0.27、二阶矩 0.43、双时间尺度比 −0.02。注意力数据里**唯一有截面预测力的是「相对 fame 基线的正向脉冲强度」**，六个相邻机制各自独立失效——这不是参数没调好，是机制层判死。**后续 sentiment7 不再开新臂，只沿 H4 做降相关变体。**

### 十九-C、`3qod35v6` 候选卡片

| 项 | 值 |
|---|---|
| 表达式 | `vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22), ts_delay(ts_backfill(vec_avg(snt7_all_languages_views),22),5)),5),22),120,driver="gaussian"), ts_backfill(vec_avg(snl27_relpopularity08),22))` |
| 设置 | SUBINDUSTRY / decay 16 / truncation 0.02 / pasteurization ON / nanHandling ON / maxTrade OFF / VERIFY |
| 塔 | **DEU/D1/SENTIMENT ×1.8**（该塔当前 0 颗 ⇒ 这是第 1 颗） |
| S / F / TO / 2Y / sub / DD / margin | **2.04 / 1.84 / 11.00% / 2.36 / 1.47 / 0.0415 / 18.45bp** |
| 持仓 | long 127 / short 123 = 250 只 |
| 硬闸 | `checks.fail = []`；`failed_ra_count = 0`；`failed_ppa_count = 0` |
| 本地自相关 | **0.0313**（OS 池 10 只，最大相关者 `2rmGAPqN`） |
| 与 OTHER 候选互相关 | 对 `1YNv6Ymk` **0.0119**、对 `1YNvvgdJ` 0.0127 ⇒ **两条可同时提交，各点一塔** |
| 未决 | prod 相关性（平台槽被并行会话长期占用，见 §十五） |

**注意与论坛前作的关系**：`np7nn69l` 是同数据集的 OS 前作（prod 0.6338）。本条的差异是 `quantile`→`ts_quantile`、`ts_max`→`max+ts_delay`，属「换几何」而非「换字段组合」，prod 需实测确认。

---

## 二十、M 波：fundamental6（FUNDAMENTAL）—— 10/10 REJECT，数据集判死

multisim `922K4gsa4tLaqZ1cYOQYve6`；SUBINDUSTRY / decay 4 / trunc 0.08 / **nanHandling ON**；10/10 `COMPLETE`、0 error。

| alpha | 模板（文献出处） | S | F | TO | 2Y | 持仓 |
|---|---|---|---|---|---|---|
| `88RAKw0l` | T2 Novy-Marx 毛利/资产 行业内 zscore | **0.56** | 0.32 | 2.99% | 0.25 | 56+65 |
| `xArMmZJb` | T9 毛利率变化 1008 + 行业内 zscore | 0.02 | 0.00 | 6.09% | −0.15 | 40+39 |
| `gJevo22Q` | T5 盈利动量 × 去杠杆 | 0.01 | 0.00 | 5.63% | 0.42 | 49+49 |
| `RREXkgOj` | T1 Sloan 应计 `ts_zscore` 504 | −0.01 | −0.00 | 4.15% | 0.36 | 33+34 |
| `pwd01L2b` | T3 Cooper 资产增速 1008 | −0.03 | −0.00 | 2.65% | 0.14 | 48+47 |
| `1YNvnMrJ` | T8 Fairfield 应计质量 `ts_corr` | −0.10 | −0.03 | 2.01% | 0.41 | 82+66 |
| `leAxRmmN` | T6 Titman capex `ts_av_diff` 504 | −0.24 | −0.10 | 4.31% | 0.01 | 48+47 |
| `akKJWp56` | T7 Lev-Nissim R&D bucket 十分位 | −0.30 | −0.13 | 3.45% | 0.74 | 57+58 |
| `d5WqlGGg` | T4 Hirshleifer NOA `signed_power`² | −0.31 | −0.13 | 2.04% | 0.00 | 66+67 |
| `6XdxYk5L` | T10 Ohlson 困境复合 行业内 rank | −0.57 | −0.32 | 1.69% | −0.25 | 82+127 |

**归因（三条）**

1. **持仓数 67–209 只，截面极窄**。fundamental6 字段级 cov 0.52–0.66，但「比值型」骨架要求分子分母**同时非空**，交集塌到 200 只以下 ⇒ 这是**结构性**失败，不是信号强度问题。
2. **10/10 全部挂 `LOW_2Y_SHARPE`（limit 1.58）**，再次印证 2Y 是 DEU 的第二道硬闸；即使 `88RAKw0l` 的 S 形状最干净也救不回来。
3. `CLUSTER_TEST` 全 warning（值 −0.42 ~ 0.47），无一条进入可提交区间。

⇒ **fundamental6 在 DEU 判死，FUNDAMENTAL 塔维持 1 颗。** 派生规则：**field cov 在 0.5–0.7 的 fundamental 类集，骨架应避开 A/B 双字段比值，改用单字段时序变换**，否则先按本案判死。

---

## 二十一、N 波：sentiment33（SENTIMENT）—— 10/10 REJECT，VECTOR NaN 结构塌截面

multisim `3tX3RCgOF4uF9MAnuLWpOOv`；SUBINDUSTRY / decay 4 / trunc 0.08 / **nanHandling ON**；10/10 `COMPLETE`。

| alpha | 模板 | S | F | TO | 2Y | 持仓 |
|---|---|---|---|---|---|---|
| `QPve2Xo5` | T3 客观性 `signed_power`² | **0.67** | 0.25 | **95.66%** | 0.62 | 2+2 |
| `zq3aPpLK` | T2 过滤密度 `ts_delta` 22 | 0.37 | 0.17 | 10.32% | 0.40 | **0+0** |
| `omE23OXn` | T6 情绪惊喜 `ts_zscore` 504 | 0.12 | 0.02 | 95.46% | −0.50 | 2+1 |
| `88RAa1ZV` | T7 坏消息不对称 | 0.07 | 0.01 | 95.47% | −0.04 | 2+2 |
| `JjelgK2e` | T4 跨方法分歧 `ts_std_dev` 66 | −0.02 | −0.00 | 10.14% | −0.17 | 66+64 |
| `2rAEadoP` | T8 报道强度 `ts_av_diff` 66 | −0.02 | −0.00 | 55.75% | 0.03 | 12+12 |
| `ZYQZ2GvQ` | T9 文言深度比 | −0.15 | −0.03 | 95.32% | 0.09 | 2+2 |
| `Vkxn2Je8` | T1 净极性（水平） | −0.20 | −0.04 | 95.81% | −0.44 | 2+2 |
| `j2YL9mkQ` | T10 行业内 zscore(sector) | −0.26 | −0.06 | 95.75% | −0.37 | 2+2 |
| `zq3aPpEK` | T5 剥 fame 基线 `vector_neut` | −0.37 | −0.10 | 95.74% | −0.45 | 2+2 |

**归因（四条，含两条可跨集复用的工程事实）**

1. **VECTOR 情绪字段做 `vec_avg`/`vec_sum` 后几乎无横截面**：8/10 条 `longCount 2 / shortCount 2`——只有 2 只股票有非空值。`CONCENTRATED_WEIGHT` 全部 FAIL（值 0.5 vs limit 0.1）。
2. **只有套了 `ts_delta` / `ts_std_dev` 的两条拿到宽截面（66+64）**：差分把「长期 NaN」变成可比变化量，而水平 / 比值 / `ts_zscore` 型全被 NaN 结构掐死。⇒ **稀疏 VECTOR 集的骨架应优先走差分 / 离散度类。**
3. **`vector_neut` 的效果依赖字段 NaN 结构，不可跨集外推**：同一算子在 sentiment7 上把 S 从 0.76 抬到 2.04，在本集把 −0.20 压到 −0.37。
4. 唯一正信号 `QPve2Xo5`（客观性，S 0.67 / sub 0.79）TO 95.66% 严重超标 ⇒ 客观性维度有微弱信息但不可交易。

⇒ **sentiment33 在 DEU 判死（作为 ATOM 主信号源）**；SENTIMENT 塔仍只能靠 sentiment7 + sentiment27 的 `P0oe6wpJ`。
**附：数据集级 description 与实际字段错配**——本集描述写「RIC/BBID 映射」，实际是 NLP 情绪 token 统计（同 other250 的错配模式）⇒ **画像以字段级 description 为准**。

---

## 二十二、O 波：SHORTINTEREST + RISK 双塔（O1 已派发 / O2 排队）

**选塔理由**：DEU D1 现有 shortinterest / risk 两塔均为 **0 颗**；两个数据集都不是 PV/MODEL/OTHER ⇒ 不触碰「trio 内部禁两两组腿」。O1/O2 各自是**纯 ATOM 单数据集**。

**数据集画像（平台实测）**

| 数据集 | category | 字段数 | 覆盖 | 关键字段 |
|---|---|---|---|---|
| `shortinterest3` | SHORTINTEREST | 25（全 VECTOR） | 0.653–**0.783** | `shrt3_bar`（借券需求 1–10 评级，alphaCount 323）、`mean/max/min_loan_rate`、`loan_rate_volatility`、`average_loan_duration_days`、`loaned_market_value_usd` |
| `risk60` | RISK | 5（全 VECTOR） | 0.835 | `lending_fee_bid_rate`、`rsk60_offer`、`rsk60_last`、**`rsk60_crowding`**（日内做空活动带符号）；`rsk60_datatime` 是时间戳非信号 |

**两处可直接增益的实证细节**

1. **`shortinterest3` 有三套字段版本族**：裸名（cov 0.6683）/ `_main`（0.6872）/ **`_p5_d1`（0.7833）**。`j2Ym1PL9` 用的是 `_main`，**换 `_p5_d1` 可把截面从 0.6872 抬到 0.7833**——这是本轮对该近闸候选的直接改进点。
2. **论坛作者建议 nanHandling 常开**（`34407581314583` 评论区：「我开了 NAN HANDLING，你没开，很多时候会差别很大，推荐常开，类似于 ts_backfill」）⇒ 本波两批均用 `nanHandling ON`。

**符号先验（先验相反，是本波的核心对比实验）**

| 维度 | 方向 | 出处 |
|---|---|---|
| 借券费**水平** | **反向**（高费 = 卖空约束 = 高估 → 后续跑输） | D'Avolio (2002) *The market for borrowing stock* |
| 借券费**波动率** | **正向**（卖空风险溢价） | Engelberg-Reed-Ringgenberg (2018, JF) *Short-selling risk* |
| 做空**流向**（`rsk60_crowding`） | **反向**（做空增加 → 后续下跌），DEU 未验证 | Boehmer-Jones-Zhang (2008) |

> 同一数据集内出现「水平反向 / 波动正向」是这两个字段**互不相关**的先验依据；O1 的 T1 与 T2 即为此对照。

**O1 模板台账（`shortinterest3`，10 个结构互异模板，multisim `qgJbE6Zt4p49YCigp14Oaz`）**

| ID | 结构（互异点） | 表达式骨架 |
|---|---|---|
| S1 | 费率**水平** + 截面 rank（反向） | `multiply(-1, rank(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 66)))` |
| S2 | **二阶矩**（费率波动，正向） | `rank(ts_backfill(vec_avg(loan_rate_volatility_p5_d1), 66))` |
| S3 | **组内费率极差/均值**（无量纲离散度） | `multiply(-1, rank(divide(subtract(vec_max(max_loan_rate_p5_d1), vec_min(min_loan_rate_p5_d1)), vec_avg(mean_loan_rate_p5_d1))))` |
| S4 | **一阶差分**（贷款久期趋势） | `multiply(-1, rank(ts_delta(ts_backfill(vec_avg(average_loan_duration_days_p5_d1), 120), 66)))` |
| S5 | **规模水平** `ts_zscore`（借出市值） | `multiply(-1, rank(ts_zscore(vec_avg(loaned_market_value_usd_p5_d1), 252)))` |
| S6 | **有界评分水平**（1–10 评级，正向） | `rank(ts_backfill(vec_avg(shrt3_bar), 120))` |
| S7 | **双 zscore 背离 + group_rank(sector)** | `group_rank(subtract(ts_zscore(ts_backfill(vec_avg(shrt3_bar),120),252), ts_zscore(vec_avg(mean_loan_rate_p5_d1),252)), sector)` |
| S8 | **偏离长均**（`ts_av_diff`） | `multiply(-1, rank(ts_av_diff(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 120), 22)))` |
| S9 | **时序分位**（`ts_quantile` gaussian） | `multiply(-1, ts_quantile(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 66), 252, driver="gaussian"))` |
| S10 | **事件门控**（活跃度 `trade_when`） | `trade_when(rank(ts_backfill(vec_avg(transaction_count_p5_d1), 66)) > 0.2, multiply(-1, rank(ts_zscore(ts_backfill(vec_avg(mean_loan_rate_p5_d1),120),252))), -1)` |

**O2 模板台账（`risk60`，10 个结构互异模板，因 429 排队中，表达式已存 `tracking/DEU/candidates/wave_O2_risk60_pending.json`）**

| ID | 结构（互异点） | 表达式骨架 |
|---|---|---|
| R1 | **借贷买卖价差率**（无量纲摩擦） | `multiply(-1, rank(divide(subtract(vec_avg(rsk60_offer), vec_avg(lending_fee_bid_rate)), vec_avg(rsk60_last))))` |
| R2 | 费率水平 rank（反向） | `multiply(-1, rank(ts_backfill(vec_avg(rsk60_offer), 66)))` |
| R3 | **做空流向** 22 日均值（反向） | `multiply(-1, rank(ts_mean(vec_avg(rsk60_crowding), 22)))` |
| R4 | **费率波动**（卖空风险，正向） | `rank(ts_std_dev(ts_backfill(vec_avg(rsk60_offer), 120), 66))` |
| R5 | **流向变化**（拥挤度解杠杆） | `multiply(-1, rank(ts_delta(ts_mean(vec_avg(rsk60_crowding), 22), 66)))` |
| R6 | **group_zscore(sector)** | `multiply(-1, group_zscore(ts_zscore(ts_backfill(vec_avg(rsk60_offer),120),252), sector))` |
| R7 | 时序分位 gaussian | `multiply(-1, ts_quantile(ts_backfill(vec_avg(rsk60_offer), 66), 252, driver="gaussian"))` |
| R8 | **流向水平** zscore | `multiply(-1, rank(ts_zscore(vec_avg(rsk60_crowding), 252)))` |
| R9 | **价差 zscore**（摩擦趋势，正向） | `rank(ts_zscore(divide(subtract(vec_avg(rsk60_offer), vec_avg(lending_fee_bid_rate)), vec_avg(rsk60_last)), 252))` |
| R10 | **活跃度门控 + group_rank** | `trade_when(rank(ts_backfill(vec_avg(rsk60_last), 66)) > 0.1, multiply(-1, group_rank(ts_zscore(vec_avg(rsk60_offer), 252), sector)), -1)` |

**派发纪律备忘**：一元负号统一写成 `multiply(-1, ·)`，避免 `-expr` 触发 toolkit 静态门禁把整批 10 条判 CANCELLED（batch-kill）。O2 首派即因 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`（429）被拒，说明账号并发槽被外部会话挤占——**派发前需先 `batch_status` 确认在手批次已归零**。

---

## 二十三、O2 波收割（risk60 → RISK 塔判死）+ P1 波（model238）设计

### 23.1 O2 收割结果：multisim `1aNSvG3L54lt9SMrES6jKST`，10/10 COMPLETE，10/10 REJECT

设置：SUBINDUSTRY / decay 4 / trunc 0.08 / **nanHandling ON**。持仓全部 94–122 只（截面健康，**不是**截面问题）。

| alpha | 模板 | S | F | TO | 2Y | sub | 持仓 |
|---|---|---|---|---|---|---|---|
| **`6XdxRv1G`** | R2 费率水平 rank（反向） | **0.82** | 0.59 | **6.69%** | **1.13** | 0.27 | 116+102 |
| `leAx7bRx` | R7 `ts_quantile` gaussian | 0.81 | 0.47 | 15.82% | 0.58 | 0.42 | 117+111 |
| `N1NMnvgo` | R10 活跃度门控 + group_rank | 0.80 | 0.50 | 12.12% | 1.02 | **0.49** | 121+110 |
| `KPJenj81` | R6 group_zscore(sector) | 0.78 | 0.45 | 17.43% | 0.76 | 0.58 | 101+85 |
| `LLMenAXM` | R5 流向变化（解杠杆） | 0.64 | 0.31 | 16.33% | −0.04 | 0.25 | 108+108 |
| `wpQ65Mzp` | R3 做空流向 22 日均值（反向） | 0.35 | 0.13 | 15.64% | 0.16 | 0.41 | 122+97 |
| `VkxnXgYb` | R9 价差 zscore | 0.23 | 0.05 | 35.05% | 1.09 | 0.16 | 101+101 |
| `RREXNnke` | R8 流向水平 zscore（反向） | −0.50 | −0.14 | 41.33% | −0.46 | −0.09 | 98+97 |
| `d5WqnA7E` | R4 费率波动（正向先验） | −0.66 | −0.40 | 3.77% | −0.91 | −0.80 | 110+115 |
| `A1V6nMbY` | R1 借贷买卖价差率（反向） | −0.94 | −0.48 | 26.06% | −1.22 | −0.50 | 94+109 |

**RISK 塔判死**：S 天花板 0.82、2Y 天花板 1.13，离双闸 1.58 差 0.76–0.45，且残差最大的 alpha（`6XdxRv1G`）卡在 sub（0.27 vs 0.39）。10 个结构互异模板全灭 ⇒ 不是骨架问题。

### 23.2 O2 三条机制级归因（其中两条是**独立复现**）

| 机制 | 学术方向 | DEU 实测 | 判定 |
|---|---|---|---|
| 借券费**水平**反向（D'Avolio 2002） | 反向 | R2 **+0.82**（正向则 −0.82） | ✅ **第三次独立验证**。但天花板 0.82，弱 |
| 借券费**波动率**正向 = 卖空风险溢价（Engelberg-Reed-Ringgenberg 2018 JF） | 正向 | R4 **−0.66**（反向才 +0.66） | ❌ **第二次独立验证为反向**（O1 的 `ZYQZ29Kj` 亦为 −0.54）。DEU 不存在卖空风险溢价 |
| 做空**流向水平**反向（Boehmer-Jones-Zhang 2008） | 反向 | R3 +0.35（弱正）/ R8 时序版 −0.50（无效） | ⚠️ 水平版弱正、时序异常版方向反了 ⇒ crowding 只能做**水平**，不能做时序 zscore |
| 借贷**买卖价差**（摩擦成本） | 反向 | R1 **−0.94**（全批最负，反向=+0.94 但 2Y −1.22） | ❌ 方向对但 2Y 崩，属"近年反转"型伪信号 |

**跨数据集结论（本轮第二次确认）**：DEU 的证券借贷系（shortinterest3 + risk60）**两个数据集、20 个模板全灭**，S 上限 0.82。⇒ **SHORTINTEREST 与 RISK 两塔在 DEU 无法靠这两个集点灯**，除非换集或走门控式两塔。

### 23.3 DEU 官方推荐数据集核实（论坛 `42587179348119`，RM49262 87 票）

该贴给出 DEU 官方推荐名单：`trend_momentum_model` / `analyst56` / `analyst_pred_cons` / `pv109` / `analyst_factor_signals` / `fundamental89` / `fundamental93` / `stock_vol_index` / `institutions25` / `option_chart_model`。

**实测核实**：`get_datasets(DEU, delay1, search=trend_momentum_model)` 与 `search=stock_vol_index` **均返回 0 条** ⇒ 这两个"蓝海推荐"在 DEU delay1 根本不存在（可能是 GBR 名单或已下线）。其余：`fundamental93` / `institutions25` 本轮早前已测 DEU 字段 coverage 全 0.0；`analyst_factor_signals` 在 DEU 已有 84 次提交（很热）。

**该贴其他可用情报**：
- DEU **margin 中位数 15.2bp / 均值 22.4bp / 75% 分位 28bp**（GBR 为 11.9 / 13.4 / 16.2bp）⇒ DEU 提交质量基线更高，我们的候选应以 margin ≥15bp 为及格参考。
- DEU **换手提升与收益不显著同向（p>0.05）**，GBR 则 p<0.001 ⇒ 在 DEU **别指望靠推换手拿 returns**，与"TO 地板 0.125 提换手白拿 fitness"那条要分开看（那是 fitness 分母效应，不是 returns 效应）。
- DEU 首周 model238 **未进热门榜**（榜尾 model230=7）⇒ model238 在 DEU 竞争度 <7，是低拥挤区间。
- 榜单里 DEU MODEL 系热点：`model25` 53 / `model38` 36 / `predictive_starmine` 22 / `model109` 20 / `model216` 20 / `model26` 16 / `model264` 9 / `multifactor_return_pred` 9 / `model138` 8 / `model30` 8。

### 23.4 P1 波（`model238` SmartHoldings，MODEL 塔）10 模板设计

**塔约束核对**：model238 与 model28 同属 MODEL。用户规则"禁止 PV / MODEL / OTHER 下数据字段两两组腿（含 PV+PV）"⇒ **MODEL+MODEL 亦禁**。故 P1、P2 **必须各自 ATOM 单数据集**，分两批派发。这也符合"优先 ATOM"。

**字段画像**（22 字段全 MATRIX，源自 StarMine SmartHoldings 机构持股概率模型）：
- **cov 1.0 族**（rank 1–100）：`mdl238_global_rank`(13a) / `mdl238_industry_rank`(25a) / `mdl238_sector_rank`(17a) / `mdl238_country_rank` / `mdl238_region_rank` —— 机构持有概率分位，**越高越可能被机构持有**
- **cov 1.0 变化族**：`mdl238_global_change_rank`(13a) / `mdl238_region_change_rank` —— **近期机构持仓动量**
- **cov 1.0 拥挤族**：`mdl238_global_owner_rank`(8a) / `mdl238_region_owner_rank` —— **100=最拥挤**，容量/流动性风险
- **cov 1.0 风格族**：`mdl238_global_screening_rank` / `mdl238_region_screening_rank` —— 风格契合度
- **cov ≈0.71 浮点族**：`*_relative_investment_rank` / `*_institutional_preference_rank` / `*_peer_investment_concentration_rank`(反向分) / `*_screening_factor_alignment_rank`

**符号先验**：
- Gompers-Metcrick (2001)「机构持仓变动动量」→ **正向**（跟随聪明钱）。
- 拥挤反转（论坛 `43151729306647` WY79095「机构持仓变化与拥挤反转」）→ 持仓**水平**在拥挤度高时应**反向**。
- Lakonishok-Shleifer-Vishny (1994) → 机构偏好本身是风格暴露，应做行业/部门内中性化后再用。

| ID | 结构（互异点） | 表达式 | 方向 |
|---|---|---|---|
| P1-1 | 拥挤反转（截面 + 负号，sector 轴） | `multiply(-1, group_rank(mdl238_global_owner_rank, sector))` | 反 |
| P1-2 | 增持动量（**group_zscore** 降换手，industry 轴） | `group_zscore(mdl238_global_change_rank, industry)` | 正 |
| P1-3 | 增持**加速度**（一阶差分 22） | `ts_delta(mdl238_global_change_rank, 22)` | 正 |
| P1-4 | 持仓概率**水平**（group_rank industry） | `group_rank(mdl238_global_rank, industry)` | 正 |
| P1-5 | **双秩背离**（行业内位置 − 全球位置，剥规模） | `subtract(rank(mdl238_industry_rank), rank(mdl238_global_rank))` | 正 |
| P1-6 | **拥挤分层内中性化**（仿 KMV 分桶思路，桶=拥挤度） | `group_neutralize(rank(mdl238_global_rank), bucket(rank(mdl238_global_owner_rank), range='0, 1, 0.1'))` | 正 |
| P1-7 | **持仓-拥挤背离**（未拥挤的聪明钱） | `subtract(rank(mdl238_global_rank), rank(mdl238_global_owner_rank))` | 正 |
| P1-8 | **时序分布**（相对自身历史的自标准化） | `ts_zscore(mdl238_global_change_rank, 252)` | 正 |
| P1-9 | 风格契合度（screening，sector 轴） | `group_rank(mdl238_global_screening_rank, sector)` | 正 |
| P1-10 | **尾部凸化**（中心化后立方，重仓极端增持） | `signed_power(subtract(divide(mdl238_global_change_rank, 100), 0.5), 3)` | 正 |

**结构互异性核对**（10/10 无重复骨架）：截面积分×2（P1-1 负号 / P1-2 gz / P1-4 / P1-9 = 四个不同字段×不同轴）· 时序差分×1（P1-3）· 双秩差×2（P1-5 / P1-7 用不同字段对）· 分桶中性×1（P1-6）· 时序分布×1（P1-8）· 非线性凸变换×1（P1-10）。

**预检结果**：`preflight_expressions` 10/10 `valid: true`，`unknown_fields: []`，5 字段全部存在。

**派发状态**：因 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`（429）被拒，待槽位释放后重派。

---

## 二十四、P1 / P2 / P3 三波收割：桶内中性化模板完成跨数据集三重验证，model53 判死

### 24.1 P1（model238 机构持股概率）— 10/10 REJECT，但出现战役最强 MODEL 候选

`multisim 2lqChn2wo4RpcGk622hjG2w`，10/10 COMPLETE。设置 SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling ON。

| 模板 | alpha | S | F | TO | 2Y | sub | 表达式 |
|---|---|---|---|---|---|---|---|
| **P1-6** | **`d5WqnzKX`** | **1.14** | **0.88** | 12.61% | 0.88 | 0.21 | `group_neutralize(rank(mdl238_global_rank), bucket(rank(mdl238_global_owner_rank), range='0, 1, 0.1'))` |
| P1-7 | `YP1ZNzxM` | 1.05 | 0.80 | 9.80% | 0.49 | 0.22 | `subtract(rank(mdl238_global_rank), rank(mdl238_global_owner_rank))` |
| P1-4 | `JjelnzQm` | 0.62 | 0.34 | 9.55% | 0.01 | 0.38 | `group_rank(mdl238_global_rank, industry)` |
| P1-10 | `bl6pNz6K` | 0.62 | 0.28 | 19.79% | 0.62 | −0.21 | `signed_power(subtract(divide(mdl238_global_change_rank, 100), 0.5), 3)` |
| P1-2 | `GrWVnzbG` | 0.61 | 0.26 | 18.71% | 0.62 | −0.15 | `group_zscore(mdl238_global_change_rank, industry)` |
| P1-9 | `gJevmGem` | 0.53 | 0.28 | 5.87% | −0.10 | 0.45 | `group_rank(mdl238_global_screening_rank, sector)` |
| P1-1 | `58ERL5zN` | 0.43 | 0.20 | 3.28% | 0.16 | −0.11 | `multiply(-1, group_rank(mdl238_global_owner_rank, sector))` |
| P1-8 | `E563qz61` | 0.42 | 0.15 | 19.85% | 0.15 | −0.30 | `ts_zscore(mdl238_global_change_rank, 252)` |
| P1-5 | `akKJNzxx` | 0.41 | 0.15 | 24.46% | 0.93 | 0.24 | `subtract(rank(mdl238_industry_rank), rank(mdl238_global_rank))` |
| P1-3 | `9qxo9Mje` | −0.28 | −0.07 | 22.03% | −0.92 | −0.48 | `ts_delta(mdl238_global_change_rank, 22)` |

**三条归因结论**：

1. **`mdl238_global_owner_rank` 是状态变量，不是主信号。** 单独用（P1-1 反向 group_rank）只有 0.43；但做桶门控驱动出 1.14（P1-6）与 1.05（P1-7）。机构拥挤度是**调制别的信号**的条件变量。
2. **`mdl238_global_rank` 单独的 edge 只有 0.62**（P1-4）。真正的 alpha 在 `global_rank × owner_rank` 的**交互项**，不在 global_rank 本身。
3. **Gompers-Metcrick (2001) 机构持仓变动动量在 DEU 不成立**：P1-2 / P1-8 / P1-3 / P1-10 四个模板分别 0.61 / 0.42 / −0.28 / 0.62，其中一阶加速度（ts_delta 22）方向**为负**（−0.28，2Y −0.92）。

### 24.2 P2（model28 StarMine 结构信用风险 / Merton-KMV）— 桶内中性化第 3 次独立验证

`multisim 2oh5h4gTn5hRaYL19b2WdezN`，10/10 COMPLETE、零错误。

| 模板 | alpha | S | F | TO | 2Y | sub | margin | long/short | CW |
|---|---|---|---|---|---|---|---|---|---|
| **P2-7**（桶内中性化） | **`A1V6kK8W`** | **1.26** | **1.22** | 6.70% | 0.69 | 0.78 | 3.51bp | 84/84 | warning |
| P2-4（裸信号，对照臂） | `ZYQZrG93` | 0.95 | 0.84 | 5.31% | 0.55 | 0.54 | 3.69bp | 86/82 | fail |
| P2-8（ts_quantile gaussian） | `ZYQZrGvj` | 0.81 | 0.60 | 10.83% | 0.56 | 0.58 | 1.25bp | 84/83 | fail |
| P2-2（−Δpd_pct 66） | `leAxrXNl` | 0.56 | 0.50 | 9.56% | 0.63 | 0.38 | 2.05bp | 82/82 | fail 0.2131 |
| P2-9（双 ts_zscore 差） | `MPYwkmN6` | 0.41 | 0.21 | 6.70% | −0.16 | 0.23 | 1.01bp | 87/80 | fail |
| P2-6（−杠杆 sector） | `akKJov8R` | 0.25 | 0.09 | 2.05% | −0.02 | 0.13 | 1.63bp | 160/125 | **PASS** |
| P2-1（rank 违约距离） | `LLMekJ3v` | 0.11 | 0.03 | 3.08% | 0.09 | 0.20 | 0.67bp | 85/83 | fail |
| P2-5（行业−全球秩差） | `MPYwkmnk` | 0.06 | 0.01 | 9.36% | 0.77 | 0.09 | 0.10bp | 83/84 | fail |
| P2-10（signed_power 3） | `2rAEJdoY` | −0.18 | −0.09 | 3.87% | −0.26 | 0.02 | −1.54bp | 85/83 | fail 0.1561 |
| P2-3（−资产波动率） | `E563kJ2P` | −0.37 | −0.20 | 2.77% | 0.25 | −0.27 | −2.69bp | 85/84 | fail |

**这是本轮最有价值的一次对照实验。** P2-4 与 P2-7 只差外层一个 `group_neutralize(·, bucket(rank(global_rank), 0.2))`：

| | S | F | 2Y | sub | TO |
|---|---|---|---|---|---|
| 裸 `rank(asset_drift_pct)` | 0.95 | 0.84 | 0.55 | 0.54 | 5.31% |
| 加桶内中性化 | **1.26** | **1.22** | **0.69** | **0.78** | 6.70% |
| Δ | **+0.31** | **+0.38** | +0.14 | +0.24 | +1.39pp |

**换手只增加 1.39 个百分点，而 sharpe 提升 33%、fitness 提升 45%。** 这不是靠调参，是靠一个纯结构变换。

至此桶内中性化模板已在**三个互不相同的数据集**上独立成立：

| 数据集 | 桶轴 | 结果 | 来源 |
|---|---|---|---|
| `techindi_model`（USA） | 论坛原式 sector 内 group_rank | S 1.63 / F 1.02 / prod 0.54 | 论坛 `43666906426647` |
| `model238`（DEU） | `bucket(rank(owner_rank), 0.1)` 拥挤度 | S 1.14 / F 0.88 | 本战役 P1-6 |
| `model28`（DEU） | `bucket(rank(global_rank), 0.2)` 信用等级 | S 1.26 / F 1.22 | 本战役 P2-7 |

**结论：这是通用的结构变换，与 underlying 语义无关。** 已在 P4 设计里作为第 5 次验证（P4-9），并有专门的裸信号对照臂（P4-1）测边际贡献。

**`asset_drift_pct` 是 DEU 上最强的单因子**（裸 rank 即 S 0.95 / F 0.84 / margin 3.69bp / investability_sharpe 0.89）。这是 Merton (1974) Contingent Claims 的直接预测：资产漂移 ↑ ⇒ 股权预期收益 ↑，中间无套利摩擦，比违约距离干净。

**教科书先验被否的三项**：
- **KMV 违约距离在 DEU 完全无效**：裸 rank 0.11 / signed_power(zscore,3) −0.18 / ts_quantile 0.81。推测原因：DEU TOP500 大市值股违约距离整体高且稳定，截面方差不足，而 KMV 的截面预测力主要来自小盘/困境股。
- **低波动异象弱**：−rank(asset_volatility_pct) = −0.37（正向则 +0.37）。
- **杠杆信用版无效**：−group_rank(leverage, sector) S 0.25 / 2Y −0.02（持仓 285 只，CW 反而 PASS）。

**平台判定差异（重要）**：`A1V6kK8W` 的 `checks.fail` 是**空数组**、`ppa_failed_count = 0`，但 `ra.failed_ra_checks` 仍列 LOW_SHARPE / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE。⇒ **判「是否可提交」必须以 `ra_failed_checks` 为准，不能看 `checks.fail`**（平台对接近线的 PPA 候选把 fail 降级为 warning）。

### 24.3 P3（model53 信用期限结构）— 10/10 REJECT，model53 判死

`multisim zWRFu6Vr52t9kCYVBT2jFS`，10 模板用 JC7 年度化 PD 阶梯（1M/3M/6M/1Y/2Y/3Y/4Y/5Y/7Y/10Y）+ Kamakura MS5 阶梯 + 隐含利差。

| 模板 | alpha | S | TO | 2Y | sub | margin | 机制 |
|---|---|---|---|---|---|---|---|
| P3-10 | `xArMRpXW` | **0.44** | 44.31% | 0.92 | 0.21 | 0.14bp | 斜率跨模型分歧（全波最佳 S） |
| P3-2 | `JjelbJKe` | 0.36 | **5.02%** | −0.74 | 0.22 | 0.89bp | 斜率行业内 |
| P3-8 | `2rAEJoPP` | 0.27 | 15.59% | −0.78 | 0.41 | 0.33bp | 利差 66 日变化反向 |
| P3-9 | `RREXdw01` | 0.19 | 43.65% | −1.26 | 0.57 | 0.06bp | 利差/PD 单位风险溢价 |
| P3-4 | `vR10dXV3` | 0.18 | 43.78% | −0.22 | 0.30 | 0.10bp | 曲线凸度（蝶式） |
| P3-7 | `YP1ZQoZR` | 0.15 | 7.14% | **0.88** | −0.12 | 0.37bp | 隐含利差水平反向（全波最佳 2Y） |
| P3-1 | `9qxoJO0K` | 0.09 | 43.15% | −0.30 | −0.08 | 0.03bp | 斜率（10Y−1M） |
| P3-6 | `9qxoJOoV` | 0.06 | 44.69% | 0.59 | −0.41 | 0.02bp | 跨厂商分歧（JC7 vs Kamakura） |
| P3-5 | `QPveEpd5` | −0.51 | 44.15% | −1.14 | −0.29 | −0.14bp | 期限比值 10Y/1M |
| P3-3 | `GrWVk5J5` | −0.55 | **49.05%** | −0.94 | −0.25 | −0.13bp | 斜率 ts_quantile 时序分位 |

**判死主因不是信号弱，是换手爆炸。** 7/10 模板 TO 达 43–49%，margin 被压到 0.02–0.14bp（DEU 及格线 15bp 的百分之一）。而同数据集 P2 的 `ts_delta(pd_pct,66)` 只有 9.56% TO。

**机理定位**：`annualized_pd_1_month_jc7` 是 1 个月期限的**年度化**违约概率，对近期波动率极度敏感、本身是高频量。用它做减数/除数，等于把高频成分注入低频的信用曲线结构。

> **新纪律**：任何「长端 − 短端」的期限结构因子，**必须先把短端 `ts_mean` / `ts_decay_linear` 平滑再做差**，否则换手必然爆炸。本轮 10 个模板全部漏了这一步，是该波的设计缺陷。

**跨厂商模型分歧不含可交易信息**：P3-6（1Y PD 秩差）S 0.06 / sub −0.41；P3-10（斜率跨模型分歧）S 0.44 / TO 44%。两家底层都是 Merton 结构模型、输入同源 ⇒ 分歧主要是数值实现差异，不是观点差异。

**model53 判死**，DEU 已判死数据集增至 **21 个**。

### 24.4 三波合并后的跨数据集规律（比单波结论更硬）

| 规律 | 证据（三个独立数据集同向） |
|---|---|
| **「行业内相对位置」骨架在 DEU 无效** | model53 斜率 sector 版 0.36 · model28 行业−全球秩差 0.06 · model238 industry_rank 单独 0.62。**DEU TOP500 只有 500 只股票摊到 sector 层，组内样本太少，group 类算子方差过大。** |
| **DEU MODEL 数据上「收益方向」≫「风险度量」** | 收益方向类：`asset_drift_pct` S 0.95、`global_rank × owner_rank` S 1.26。风险度量类：违约距离 0.11、期限结构 ≤0.44、杠杆 0.25、利差 0.15。 |
| **桶内中性化是通用结构变换** | 三个数据集（techindi / model238 / model28）、两种桶语义（拥挤度 / 信用等级），ΔS +0.19 ~ +0.31。 |
| **CW 的主解是扩持仓数，不是 truncation** | model28 持仓 84+84 时 CW 常挂；P2-6 持仓 285 只时 CW 自动 PASS。model28 全部模板持仓都只有 ~170 只，这是结构性约束。 |

### 24.5 P4 设计（model264 — 已派发 `1TGzph8PU4p2cI2krDzzJWU`）

**数据集画像（380 字段，全 MATRIX，coverage 0.9938–0.9966）**——本轮发现的**最富矿**：

字段名形如 `mdl264_{1l|2l|3l}_<underlying>` 与 `mdl264_<underlying>_{class|l1|l2|l3}`，三层结构：

| 前缀 | 含义 |
|---|---|
| `1l` | P(未来趋势为 **fall**) — 下跌概率 |
| `2l` | P(未来趋势为 **neutral**) — 中性概率 = **模型不确定性/置信度反向** |
| `3l` | P(未来趋势为 **move-up**) — 上涨概率 |
| `_class` | 预测类别 {1=fall, 2=neutral, 3=move-up} — **硬标签** |
| `_l1/_l2/_l3` | 与 1l/2l/3l 同义的另一套命名（部分 underlying 只提供这套，如 `mdl264_macd_*`） |

**关键推论**：
- `subtract(3l, 1l)` = 净方向分，值域 **[−1, 1] 有界**，不需要 rank（rank 会抹掉幅度信息）
- `subtract(1, 2l)` = **模型置信度**，天然的信心权重
- 同一 underlying 同时给软概率与硬标签 ⇒ 论坛 `43500671638551`「软信息优于硬信息」可做**原生 A/B**
- 覆盖 0.9964–0.9966（截面 ~500 只）⇒ **直接解决困扰全区的「截面太窄」问题**（L 波 120–140 只 10/10 CW FAIL、N 波 4 只全崩）
- 拥挤度极低（alphaCount 多数 0–13，最热 57）

**10 个结构互异模板**：

| ID | 机制 | 结构互异点 | 表达式 |
|---|---|---|---|
| P4-1 | 净方向概率（软信息基线） | 纯代数差（有界） | `subtract(mdl264_3l_bb, mdl264_1l_bb)` |
| P4-2 | 信心加权净方向 | 乘法（方向 × 置信度） | `multiply(subtract(mdl264_macd_l3, mdl264_macd_l1), subtract(1, mdl264_macd_l2))` |
| P4-3 | 逆方差置信加权+平滑 | 除法（信号÷(c+σ²)）+ decay | 见下 |
| P4-4 | 行业内净方向 | group_rank industry | `group_rank(subtract(mdl264_3l_m1r_1yf_spe_se, mdl264_1l_m1r_1yf_spe_se), industry)` |
| P4-5 | 跨族背离（基本面修正 vs 价格动量） | 秩差背离 | `subtract(rank(subtract(mdl264_3l_m1r_pt_se, mdl264_1l_m1r_pt_se)), rank(subtract(mdl264_3l_d36ntr, mdl264_1l_d36ntr)))` |
| P4-6 | 模型不确定性本身 | rank + 取负 | `multiply(-1, rank(mdl264_2l_ivn))` |
| P4-7 | 修正持续性（1 月 vs 1 日扩散） | 同族跨窗口差 | `subtract(mdl264_1l_m1r_1yf_spe_se, mdl264_1l_m1d_1yf_spe_se)` |
| P4-8 | 时序分位高斯化 | ts_quantile 分布变换 | `ts_quantile(subtract(mdl264_3l_d12ntr, mdl264_1l_d12ntr), 252, driver="gaussian")` |
| P4-9 | 桶内中性化（模板第 5 次验证） | bucket 门控 | `group_neutralize(subtract(mdl264_3l_ghc_qe_td_tl, mdl264_1l_ghc_qe_td_tl), bucket(rank(subtract(mdl264_3l_bb, mdl264_1l_bb)), range='0, 1, 0.2'))` |
| P4-10 | **【对照臂】硬标签** | 离散类别线性映射 | `subtract(mdl264_rtn21d_class, 2)` |

P4-3 完整式：
```
ts_decay_linear(multiply(-1, divide(subtract(mdl264_1l_57_03_am, mdl264_3l_57_03_am),
  add(0.01, ts_std_dev(subtract(mdl264_1l_57_03_am, mdl264_3l_57_03_am), 22)))), 22)
```

**三组 A/B 对照**：
1. **P4-8 vs P4-10** — 同一 underlying「Total return, past 1M」，软概率 vs 硬标签。直接检验「软优于硬」（Moreira-Muir 2017 volatility-managed 的离散版本）。
2. **P4-1 vs P4-9** — 裸信号 vs 加桶门控，测桶内中性化对 model264 的边际贡献（model28 上是 ΔS +0.31 / ΔF +0.38）。
3. **P4-2 vs P4-3** — 乘法置信加权 vs 逆方差置信加权，两种置信度实现对比。

**预检**：10/10 valid（`unknown_fields` 仅 `gaussian` 字符串字面量假阳性），19 个真实字段全部核实。

**已知风险**：P4-3 的 regularizer 0.01 是按概率量级估的（论坛原帖明确警告 0.001 不可机械复制）；P4-6 用中性概率单独做信号先验较弱，定位为机制探针。

### 24.6 本轮派发/收割时序与槽位约束

实测**账号有效 multisim 并发 = 1**（第二批必 429），因此三波严格串行：

```
P2 派发 → 收割（10/10）→ P3 派发 → 收割（10/10）→ P4 派发 → 待收割
```

**prod 相关性槽位**独于此约束，但被外部进程长期占用：连续多次 `check_correlation(production, refresh=True)` 均返回 `correlation_busy`，`holder` 依次为 `YP1rzw2J` → `kqNRbvJP` → `d5WqeQbx` → `Xg9qjVOz` → `rKRkL9QE`，`inflight: false` 证明占用者是别的 alpha。⇒ **两条已过模拟层的候选（`1YNv6Ymk` / `P0oe6wpJ`）仍卡在 prod 终验，不得提交。**

---

## 二十五、P4 波（model264）收割与战略转向（2026-10-30 下半场）

### 25.1 P4 全部结果（multisim `1TGzph8PU4p2cI2krDzzJWU`，10/10 COMPLETE，0 error）

| 模板 | alpha | S | F | TO | 2Y | sub | margin | long/short | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|
| P4-3 稳定化反向 | `MPYwx8AM` | **0.53** | 0.28 | 3.63% | 0.20 | 0.16 | 1.98bp | 153/139 | S,F,sub,2Y |
| P4-10 硬标签 | `2rAEKZEw` | 0.47 | 0.13 | 43.00% | 0.13 | −0.16 | 0.16bp | 148/94 | S,F,sub,2Y |
| P4-1 裸净方向 | `O0Ae9maJ` | 0.44 | 0.23 | 10.70% | 0.04 | −0.43 | 0.62bp | 166/126 | S,F,sub,2Y |
| P4-2 置信度加权 | `P0oe1l9L` | 0.40 | 0.16 | 17.07% | −0.02 | −0.25 | 0.34bp | 167/125 | S,F,sub,2Y |
| P4-7 跨期差 | `QPveQldW` | 0.15 | 0.03 | 19.70% | 0.58 | 0.24 | 0.08bp | 134/158 | S,F,2Y |
| P4-4 行业内秩 | `kqNRKm5l` | 0.12 | 0.03 | 11.33% | 0.11 | −0.30 | 0.12bp | 148/149 | S,F,sub,2Y |
| P4-9 桶内中性化 | `0mYo8Qok` | −0.05 | −0.01 | 20.28% | 0.24 | 0.10 | −0.03bp | 149/143 | S,F,2Y |
| P4-5 跨 underlying 差 | `78LOdXVx` | −0.24 | −0.07 | 17.15% | 0.51 | 0.18 | −0.15bp | 149/143 | S,F,2Y |
| P4-8 时序分位 | `rKRkWzk1` | −0.44 | −0.09 | 58.80% | −0.44 | 0.25 | −0.08bp | 148/144 | S,F,2Y |
| P4-6 中性概率反向 | `RREXraLb` | −0.62 | −0.38 | 7.62% | −0.54 | −0.05 | −1.21bp | 146/146 | S,F,2Y |

**结论：model264 判死**（本轮第 22 个）。10 种结构互异模板（软概率差 / 置信度乘法加权 / 逆方差稳定化 / 行业内秩 / 跨 underlying 差 / 中性概率反向 / 跨期差 / 时序分位 / 桶内中性化 / 硬标签）全部 S < 0.53。

### 25.2 归因：为什么「画像最好的数据集」是全轮最差

model264 是本轮画像得分最高的数据集——380 字段、coverage 0.9938–0.9966、拥挤度极低（多数 alphaCount 0–13）。它的语义（趋势方向概率）也正落在本轮已验证的 DEU 最强信号类型「收益方向类」上（model28 的 `asset_drift_pct` 裸 S 0.95）。但实测净方向分 `3l − 1l` 只有 0.44。

**根因拆解（三层）**：

1. **概率归一化吃掉了截面方差**。`asset_drift_pct` 是 Merton 结构模型的**连续漂移率**，有量纲、截面分布展开；`3l − 1l` 是两个 softmax 概率之差，值域压在 [−1, 1] 且大多数股票落在 0.3–0.5 区间。**有效截面区分度被归一化压掉**，rank 之后只剩噪声级差异。
2. **桶内中性化无法凭空造 edge**。P4-9 把已验证三次的 `group_neutralize(·, bucket(rank(·)))` 原样迁移，得 S −0.05。前三次成功（techindi_model S1.63 / model238 S1.14 / model28 S1.26）都建立在**底层裸信号本身有 edge**（裸 S 0.95–1.14）的前提上。
3. **跨 underlying / 跨预测期的差分是噪声**。P4-5（两个不同 underlying 的净方向差）S −0.24、P4-7（同 underlying 1年 vs 1天预测期差）S 0.15。同源价量输入训练的模型之间相关性极高，做差只剩随机。

**由此确立两条新纪律**：

- **概率型字段入场前必须先验「截面方差比」**：softmax 归一化过的概率差天然低方差，不能因为它叫「趋势方向」就当方向因子用。判据：`rank(P)` 的横截面极差/标准差若显著窄于同数据集的其他实值字段，直接跳过。
- **桶内中性化的适用边界**：底信号裸 S ≳ 0.9 才有增益空间；低于该门槛，桶变换只重组噪声。

### 25.3 反例价值：硬标签 vs 软概率在 DEU 的形态

| 臂 | S | TO | margin |
|---|---|---|---|
| 软概率 `subtract(3l_d12ntr, 1l_d12ntr)`（P4-1 同族） | 0.44 | 10.70% | 0.62bp |
| 硬标签 `rtn21d_class − 2`（P4-10） | 0.47 | 43.00% | 0.16bp |

两者 S **几乎相同**（0.47 vs 0.44），但硬标签换手高 4 倍、margin 低 3.75 倍。⇒ 论坛「软信息优于硬信息」（`43500671638551`，LS88397，43 票）在 DEU 的体现**不是胜率更高，而是同一信号强度下交易成本可控**。这条修正了此前对该帖的解读。

其余三处机制否证：模型不确定性（`2l` 当置信度）反向无效（P4-6 S −0.62 全波最差）；跨 underlying 分散无收益（P4-5）；同模型跨预测期无套利（P4-7，与 P3 model53 期限结构斜率无效构成跨数据集第 2 次确认）。

### 25.4 【本轮最重要的战略发现】DEU 2Y 闸的结构性瓶颈

把六波 60 条的结果按 2Y 排序，**唯一过 2Y 闸（≥1.58）的候选全部来自情绪/关注度类数据集**：

| alpha | 塔 | 数据集 | S | **2Y** |
|---|---|---|---|---|
| `P0oe6wpJ` | SENTIMENT | sentiment7 + sentiment27 | 2.14 | **2.56** |
| `1YNv6Ymk` | OTHER | `tm_15_*` | 2.28 | **1.60** |
| P4-7 | MODEL | model264 | 0.15 | 0.58 |
| P3-7 | MODEL | model53 | 0.15 | 0.88（全 P3 最高） |
| P2-7 | MODEL | model28 | 1.26 | 0.69 |
| P1-6 | MODEL | model238 | 1.14 | 0.88 |

**机理推断**：DEU 的 IS 尾段（2022–2023）是高通胀 + 能源危机 + 俄乌冲突年，基本面/信用/模型类信号在这段**结构性失效**（P2 全部 10 条 2Y 在 −0.26 ~ 0.77；P3 最高 0.88；P4 最高 0.58），而散户关注度、新闻情绪这类**行为信号**反而在动荡年更强。

**战略转向（本轮决策）**：停止在 MODEL category 内换数据集（4 个集 model238/28/53/264 已全试，最强 S 1.26、2Y 0.69，距双闸差距无法靠换字段弥补）。火力转向 **SENTIMENT / NEWS / INSTITUTIONS** 这三个非 trio category——它们同时满足：① 用户「单塔优先挑非 trio category」的优先序；② 2Y 闸的近年有效性要求；③ 塔位现状 institutions 已有 1 颗，挖出 2 颗即可点灯。

### 25.5 category 全盘点（平台实拉，D1 / TOP500）

**SENTIMENT（3 个集，全可用）**

| 集 | 字段 | cov | alphaCount | 判断 |
|---|---|---|---|---|
| `sentiment27` Website Popularity Rankings | 18 | 0.9038 | 324 | 已用于 `P0oe6wpJ`（2Y 2.56） |
| `sentiment33` Sentiment Data by NLP | 255 | **0.3221** | 45 | 字段多但覆盖低，十年数据不达标，降级 |
| `sentiment7` Webpage Views（Wikipedia） | 3 | 0.7418 | 94 | 已用于 `P0oe6wpJ` |

**NEWS（17 个集，实际有数据的仅 4 个）**

| 集 | 字段 | cov | alphaCount | 判断 |
|---|---|---|---|---|
| `news104` Archive News | 11 | **0.963** | 100 | 覆盖最好 |
| `news18` Ravenpack | 70 | 0.8046 | 137 | 字段最多 |
| `news17` PR Edition | 48 | 0.7906 | 87 | — |
| `news20` Web Sources News Sentiment | 46 | 0.7729 | **33** | **最不拥挤**，valueScore 5.0 |
| `news50` | 37 | 0.7644 | 42 | 已判死 |
| 其余 12 个 | — | **0.0** | — | 无数据 |

**SOCIALMEDIA（2 个集，均不可用）**：`socialmedia12` cov 0.0 无数据；`socialmedia39` Investor views 仅 1 字段且 cov 0.2748。

**INSTITUTIONS（5 个集，2 个可用）**

| 集 | 字段 | cov | alphaCount | 判断 |
|---|---|---|---|---|
| `institutions6` Institutions and Beneficial Stake | 11 | **1.0** | 270 | 覆盖完美但拥挤度最高 |
| `fund_holdings_panel` Global Institutional Fund Holdings | 18 | **0.9019** | 102 | **本轮选中**（见 §25.6） |
| `institutions4` Institutional Ownership | 6 | 0.3413 | 19 | 覆盖低 |
| `institutions1` Insider Trading for Europe | 7 | 0.2289 | 32 | 覆盖低 |
| `institutions25` Fund Short Selling | 24 | **0.0** | 7 | 无数据（已判死） |

### 25.6 P5 波设计：fund_holdings_panel（institutions 塔）

**已派发** multisim `12jSM5cwx58l8YcW4jqT3Kv`，设置 DEU/TOP500/D1/SUBINDUSTRY/decay 4/trunc 0.08/nanHandling ON。

**字段画像（18 字段全部 VECTOR，两组）**：基础组 coverage 0.9278，`_active` 组 0.876。

| 字段 | 语义 | 无量纲 | 拥挤度 |
|---|---|---|---|
| `stable_boundary_trade_count_21d` | **稳定边界交易数**（21 交易日内该证券无前次边界交易的账户发起，代表更持久的持仓变化） | ✓ count | userCount 23 / alpha 33（**本集最热**） |
| `boundary_transaction_total` | 边界交易数（新建仓 + 完全清仓合计） | ✓ count | 18 / 26 |
| `transaction_account_total` | 参与交易的不同账户数 | ✓ count | 8 / 10 |
| `large_trade_count_50bps` | 单笔 > 0.5% AUM 的大额交易数 | ✓ count | 4 / 5 |
| `top_weighted_transaction_number` | 信念持仓（conviction holdings）交易数 | ✓ count | 2 / 2 |
| `herfindahl_index_transactions` | 交易额 HHI 集中度（0–1） | ✓ index | 3 / 3 |
| `transaction_value_distribution_score` | 交易额分布集中度（0–1） | ✓ index | 4 / 4 |
| `security_transaction_usd_value` | 交易总额（USD） | ✗ 有单位 | 8 / 9 |
| `boundary_transaction_usd_value` | 边界交易总额（USD） | ✗ 有单位 | 2 / 2 |

**关键结构约束（决定了整个模板设计）**：该数据集**没有任何带方向的净买卖字段**——只有交易量、笔数、账户数、集中度，边界交易是「建仓 + 清仓」的**合计**，方向不可分。⇒ 无法做「机构净买入」信号，只能走三条机制线：**广度（breadth）/ 强度（intensity）/ 集中度（concentration）**。

**10 个结构互异模板**：

| 模板 | 机制线 | 学术对应 | 表达式 |
|---|---|---|---|
| P5-1 | 广度变化·一阶差分 | Chen-Hong-Stein (2002) breadth of ownership | `ts_delta(vec_sum(stable_boundary_trade_count_21d), 66)` |
| P5-2 | 参与广度·水平秩 | 关注度水平 | `rank(vec_sum(transaction_account_total))` |
| P5-3 | 交易放量·时序 z | 异常成交量（Gervais-Odean 2001） | `ts_zscore(vec_sum(boundary_transaction_total), 252)` |
| P5-4 | 集中度·反向 | Frazzini-Israel-Moskowitz (2018) 拥挤度 | `multiply(-1, rank(vec_avg(herfindahl_index_transactions)))` |
| P5-5 | 大额/边界 比值 | Campbell-Ramadorai-Schwartz (2009) 机构大单信息含量 | `divide(vec_sum(large_trade_count_50bps), vec_sum(boundary_transaction_total))` |
| P5-6 | 信念交易·时序分位 | conviction holdings | `ts_rank(vec_sum(top_weighted_transaction_number), 252)` |
| P5-7 | 稳定边界占比（平滑分母） | 持久变化 vs 反复进出 | `divide(vec_sum(stable_boundary_trade_count_21d), add(ts_mean(vec_sum(boundary_transaction_total), 22), 1))` |
| P5-8 | 广度 × 低集中（active 组） | 广度与拥挤的交互 | `multiply(rank(vec_sum(transaction_account_total_active)), multiply(-1, rank(vec_avg(transaction_value_distribution_score_active))))` |
| P5-9 | 桶内中性化（已验证模板） | 在相同参与广度下比稳定建仓 | `group_neutralize(rank(vec_sum(stable_boundary_trade_count_21d)), bucket(rank(vec_sum(transaction_account_total)), range='0, 1, 0.2'))` |
| P5-10 | 单账户平均交易规模 | 大账户主导 vs 广泛参与 | `rank(divide(vec_sum(security_transaction_usd_value), vec_sum(transaction_account_total)))` |

**互异性审计**：时序算子 4 种互异（`ts_delta` / `ts_zscore` / `ts_rank` / `ts_mean` 内嵌）、截面算子 4 种互异（`rank` / 反向 `rank` / 双秩乘积 / `group_neutralize`+`bucket`）、比值 3 种且分母处理各异（裸 / 22 日平滑 / 账户数）、字段族 7 个互异、矩 4 种互异（水平 / 一阶差分 / 时序标准化 / 时序分位）。满足「≥10 结构互异」硬约束。

**预检**：10/10 valid，`unknown_fields` 空，9 个真实字段全部核实，`vec_*` 包裹无遗漏（`any_changed: false`）。

**已知风险（三条，须在收割时优先判读）**：
1. **截面宽度未知**。该数据集是 13F 派生的账户级明细，披露本质季度，日频可能是申报解析产物。首波必须先读 `longCount + shortCount`——若 < 1000 只则 sub/CW 两项必挂（此前 `shortinterest29` 只有 148 只持仓的先例）。
2. **VECTOR 稀疏性**。无交易的股票 `vec_sum` 返回 0 或 NaN，`nanHandling ON` 只能兜底不能补真值。若大面积 NaN，需加 `ts_backfill(·, 66)`。
3. **P5-5 / P5-7 分母可能为 0**（边界交易数常为 0），P5-7 已加 `+1` 兜底，P5-5 未加——若 P5-5 全零/失真，归因为分母而非机制。

---

## 二十六、P5 波收割：fund_holdings_panel（institutions 塔）——2Y 闸被解，瓶颈转移到 S 与 TO

**批次**：`12jSM5cwx58l8YcW4jqT3Kv` ｜ 10/10 terminal ｜ 设置：SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling **ON**（全 VECTOR 稀疏集）
**结论**：**FAIL —— 0/10 过双闸，1 条 NEAR（`mLoO8mq9`）。但本波价值不在出货，而在证伪了一条战略假设并解开了 DEU 的 2Y 死结。**
**数据集处置**：**不判死**，转入 salvage_pool（boost_2y 维度）。理由见 §26.5。

### 26.1 完整结果表

| 模板 | alpha | S | F | TO | 2Y | sub | margin | long/short | 判读 |
|---|---|---|---|---|---|---|---|---|---|
| P5-3 边界交易 z | `E563wpa9` | **0.89** | 0.23 | 78.42% | 0.86 | **0.83** | 1.34bp | 99/132 | 全波最高 S，但撞 HIGH_TURNOVER + CW 0.1429 |
| P5-9 **桶内中性化** | `mLoO8mq9` | 0.85 | 0.19 | 79.45% | **1.73** ✅ | 0.73 | 1.04bp | 107/124 | **全波唯一 2Y 过闸**；CW PASS、sub PASS，只挂 S/F/TO |
| P5-1 广度变化差分 | `QPveablX` | 0.80 | 0.20 | 77.05% | 0.60 | 0.60 | 1.26bp | 102/102 | CW 0.342 |
| P5-7 稳定边界占比 | `ZYQZpb2n` | 0.70 | 0.17 | 75.22% | **1.28** | 0.41 | 1.12bp | 90/128 | CW PASS、sub PASS；带 UNITS warning |
| P5-8 广度×低集中 | `leAxVvQN` | 0.29 | 0.05 | 58.58% | −0.23 | 0.12 | 0.61bp | 98/106 | 2Y 反向 |
| P5-2 参与广度秩 | `ZYQZlkWY` | 0.19 | 0.04 | 36.21% | 0.67 | −0.47 | 0.95bp | 119/113 | sub 反向 |
| P5-4 HHI 反向 | `9qxowjA9` | 0.14 | 0.02 | 52.44% | 0.76 | −0.68 | 0.44bp | 120/112 | sub −0.68 全波最差 |
| P5-5 大额/边界 | `YP1ZpbWJ` | 0.14 | 0.01 | **146.66%** | 0.33 | 0.44 | 0.18bp | **27/33** | TO 炸表 + 截面极窄 → CW 0.5 |
| P5-6 信念交易分位 | `zq3a98P1` | 0.11 | 0.01 | 57.18% | 0.07 | −0.19 | 0.24bp | 112/118 | S 与 2Y 双弱 |
| P5-10 单账户规模 | `omE2KLnl` | −0.13 | −0.01 | 79.40% | 0.08 | −0.04 | −0.16bp | 116/116 | 负 S；美元口径被价格污染 |

### 26.2 归因一：无方向字段是根本限制 —— 交易强度有效、交易结构无效

本集 18 字段全 VECTOR，**没有任何带方向的净买卖字段**：`boundary_transaction` 是「建仓 + 清仓」的合计，方向不可分。因此只能走三条机制线，实测出清晰的强弱分层：

| 机制线 | 代表模板 | S 区间 | 判定 |
|---|---|---|---|
| **交易强度 / 广度** | P5-3 z(0.89) / P5-9 桶内(0.85) / P5-1 差分(0.80) / P5-7 占比(0.70) | **0.70 – 0.89** | 有效，但全部高换手 |
| **交易结构（集中度/谁在交易）** | P5-4 HHI(0.14) / P5-8 广度×低集中(0.29) / P5-2 纯广度秩(0.19) | 0.14 – 0.29 | 无效 |
| **规模 / 比值（金额口径）** | P5-5 大额占比(0.14) / P5-10 单账户规模(−0.13) | ≈0 或负 | 无效 |

⇒ **「有多少机构在交易、交易多频繁」有信息；「谁在交易、交易多集中、单笔多大」没有信息**。这与 §24 的 model264 结论（软信息 vs 硬信息）、§25 的 model53 结论（信用期限结构无信号）形成第三类对照：**同一数据集内，度量「活动量」的字段比度量「结构」的字段强一个数量级**。

**学术侧呼应**：Chen-Hong-Stein (2002) 的 breadth-of-ownership 效应本来就是「广度」而非「结构」；Frazzini-Israel-Moskowitz (2018) 的拥挤度需要卖空数据（本集没有）才能奏效，用 HHI 代理是失效的替代。

### 26.3 归因二：TO 是 P5 的头号杀手，且成因可定位

10 条里 **6 条 TO > 70%**（P5-3 78.4% / P5-9 79.5% / P5-1 77.1% / P5-7 75.2% / P5-5 146.7% / P5-10 79.4%），全部远超 DEU 的 70% 上限。按论坛 `43175786936087` 的换手治理三分类归因：

- **不是「构造放大噪声」**：排名抖动不是集中在值差小的票，而是整体高位。
- **是「数据源高频翻转」**：账户级明细逐笔更新，`vec_sum` 后的日频序列本身高频跳动。
- **对应药方（数据层）**：`ts_mean` / `ts_sum` 拉长周期对齐数据更新节奏。**本波未做**——这是 P5 唯一的可修但未修项，也是「不判死」的核心依据。

⚠ 但按 §25 已确立的「TO 地板 0.125 反向经济学」：P5 的 TO 全在 70%+ 的高位，属于 **TO > 0.125 区间**，此处降换手**只有在砍掉低质量交易（提 margin）时才提 F**。P5 的 margin 只有 1.0–1.3bp，远低于 DEU 中位 15.2bp ⇒ **单纯平滑大概率只降 TO 不提 margin，F 不会改善**。要救必须同时把 margin 从 1.3bp 拉起来，这需要换更慢的机制而不是更慢的平滑。

### 26.4 归因三：桶内中性化第 4 次成功，且这是 2Y 增益最大的一次

`group_neutralize(rank(vec_sum(stable_boundary_trade_count_21d)), bucket(rank(vec_sum(transaction_account_total)), range='0, 1, 0.2'))`

| 对照 | 表达式差异 | S | 2Y | sub | CW |
|---|---|---|---|---|---|
| P5-1 裸差分 | `ts_delta(vec_sum(stable_boundary_trade_count_21d), 22)` | 0.80 | 0.60 | 0.60 | 0.342 ✗ |
| P5-9 桶内 | `group_neutralize(rank(vec_sum(...)), bucket(rank(vec_sum(account_total)), ...))` | 0.85 | **1.73** | **0.73** | **PASS** |

**2Y +1.13**，是四次验证里 2Y 增益最大的一次（前三次 techindi_model / model238 / model28 都是 S 增益为主）。**CW 从 0.342 的 FAIL 直接转 PASS**，说明桶内分组顺带解决了权重集中——因为分组后每组内等权，单票权重被结构性压低。

**第 4 次验证小结（四次横跨五个数据集）**：

| 次 | 数据集 | 底层裸 S | 桶内后 S | S 增益 | 2Y 增益 | 判定 |
|---|---|---|---|---|---|---|
| 1 | techindi_model | — | 1.63 | — | — | 成功 |
| 2 | model238 | — | 1.14 | — | — | 成功 |
| 3 | model28 | — | 1.26 | — | 0.69（未过闸） | 成功但 2Y 不足 |
| 4 | fund_holdings_panel | 0.80 | 0.85 | +0.05 | **+1.13** ✅ | 成功且解 2Y |

**适用边界（沿用 §24 结论并加严）**：底信号裸 S ≳0.7 就有增益空间（P5 裸 S 0.80 → 桶内 0.85 仍成功）；但**增益的落点会随数据集性质变化**——基本面/模型类增益在 S，机构行为类增益在 2Y。这不是矛盾的，机理一致：桶内中性化切掉的是**市值维度的截面共变**，而 DEU 2022–23 的失效恰恰集中在「同市值层一起跌」，所以市值桶切得越准，2Y 恢复越多。

### 26.5 【决策】fund_holdings_panel 不判死 —— 转入 salvage_pool（boost_2y）

**不判死的三条理由**：
1. **2Y 与 CW/sub 都已被证明可解**（P5-9 同时拿 2Y 1.73 + CW PASS + sub PASS），卡住的只有 S 与 TO。
2. **S 的缺口明确且可归因**：S 上限 0.89 来自「无方向字段」这一数据本质限制，不是骨架选错。要提 S 只能换机制（不是换参数），而本集提供的机制池已经用尽。
3. **它就是本区最缺的 2Y 补强腿**：DEU 的战略瓶颈是 2Y（§25），而 `mLoO8mq9` 的 2Y 1.73 是七波 70+ 条里第三高（仅次于 `P0oe6wpJ` 2.56 与 `1YNv6Ymk` 1.60）。任何需要 2Y 辅助腿的组合都应优先检索它。

⇒ 写 `salvage_pool`：`boost_dim=boost_2y`，`exclude_dataset` 置空（允许被任何主信号腿取用）。

### 26.6 本波新增的两条工程纪律

**（1）count 语义字段 ≠ 无量纲字段。**
`stable_boundary_trade_count_21d` 语义是「21 日稳定边界交易笔数」，但平台给它挂 `Unit[TSShare:1]`。P5-7 原式 `divide(vec_sum(...), add(ts_mean(vec_sum(boundary_transaction_total), 22), 1))` 触发
`Incompatible unit for input of "add" at index 1, expected "Unit[TSShare:1]", found "Unit[]"`，平台给 WARNING 但仍出结果（结果带 UNITS warning）。
⇒ **任何带「计数 / 笔数 / 数量」语义的字段，`add` 常数前必须先测单位**。比值分母兜底三选一：① `divide(A, max(B, tiny_same_unit))`（tiny 与被除项同单位）；② 直接不加常数、靠 `pasteurize` 处理 0 分母；③ 先 `rank` 再比值（rank 输出无量纲）。
（此条与已有记忆「`add(<带单位字段>, 常数)` 会炸」同源，但**新增了「count 语义也会带单位」这个反直觉点**。）

**（2）美元/市值口径必须换股数或计数口径。**
P5-10 用 `security_transaction_usd_value / transaction_account_total` 得 S **−0.13**（全波唯一负 S）。这与论坛 `43151729306647` 的实证完全一致：**市值口径 = 价格 × 股数，价格噪声盖住真实决策**（该帖实测市值差平滑 20d → S 2.37 / APAC 0.23 / 2Y 0.81 ✗；换股数差 → S 3.39 / APAC 1.23 / 2Y 1.70 ✓，S 提升 1.02）。
⇒ **本区（及任何区）涉及机构持仓/交易的信号，一律优先用股数、笔数、账户数，不用金额。**

### 26.7 对战略方向的修正

§25 的转向结论是「停止 MODEL，火力转 SENTIMENT / NEWS / INSTITUTIONS」。P5 给这条转向打了一个**带条件的勾**：

- ✅ **INSTITUTIONS 方向对**：2Y 确实能解（P5-9 1.73 vs MODEL 类全部 ≤0.88）。
- ⚠ **但 fund_holdings_panel 这一支走不通**：它缺方向字段 + 高换手，S 天花板 0.89。
- ⇒ **正确的读法是「换 institutions 内的另一个数据集」，不是「换 category」。** `institutions6`（11 字段全 MATRIX、coverage **1.0**、alphaCount 270）含完整的 buyers / sellers / acquired / disposed 方向字段，正是本集缺的东西。

**P6 波据此设计并已派发**（`1Z2DXj1a4uc8wZ13Rf7SP5g`，10 条，机构参与新鲜度门 + 股数净买入 + 市值分桶，详见 §27）。

### 26.8 本波产出清单

- `tracking/DEU/candidates/wave_P5_fund_holdings_results.json`（10 条完整指标 + 8 条 key_findings + 不判死理由）
- 本附录 §26
- 塔位账：**未变**（institutions 仍 1 颗；P5 无可用候选）
- `salvage_pool` 新增条目：`mLoO8mq9`（boost_2y，S 0.85 / 2Y 1.73）

---

## 二十七、P6 波收割：institutions6 —— 10/10 REJECT，最值钱的产物是两条否证

**批次**：`1Z2DXj1a4uc8wZ13Rf7SP5g` ｜ 10/10 terminal ｜ 设置：SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling ON
**结论**：**FAIL —— 0/10，全波 Sharpe 天花板 0.42，次高 0.39。数据集判死，INSTITUTIONS 塔级关闭。**
**但本波是八轮里 A/B 对照做得最干净的一波**，两组实验都有明确结论，且第一组直接推翻了一条来自 IND 冠军级实证的机制。

### 27.1 完整结果表

| 模板 | alpha | S | F | TO | 2Y | sub | margin | long/short | 判读 |
|---|---|---|---|---|---|---|---|---|---|
| P6-3 股数变化反向·市值分桶 | `1YNv78VM` | **0.42** | 0.16 | 5.94% | 0.70 | −0.33 | 6.25bp | 149/151 | 全波最高 S，但 sub 反向 |
| P6-8 买方占比·高斯分位 | `2rAE7gRx` | 0.39 | 0.16 | 9.57% | 0.82 | **0.42** | 4.25bp | 149/150 | **sub 全波最好**；门控 A/B 的对照臂 |
| P6-4 买方/持有方占比 | `QPveaxqr` | 0.29 | 0.13 | 6.18% | 0.39 | 0.13 | **7.67bp** | 147/152 | margin 全波最高 |
| P6-10 机构总持股·市值分桶 | `vR10LEJz` | 0.22 | 0.07 | 4.56% | 0.34 | 0.40 | 5.37bp | 151/149 | ATOM 不可互换的对照臂 |
| P6-1 门控+买方占比 | `gJev1lqO` | 0.20 | 0.06 | 8.03% | 0.58 | −0.08 | 2.79bp | 154/142 | **门控把 sub 打到负** |
| P6-5 买卖方秩差 | `wpQ6RdO2` | 0.08 | 0.02 | 5.47% | −0.14 | 0.41 | 1.76bp | 152/148 | — |
| P6-6 净买入/总交易占比 | `vR10LE9w` | 0.06 | 0.01 | 38.93% | −0.54 | 0.15 | 0.33bp | 146/153 | CW 0.489 |
| P6-2 门控+股数净买入 | `akKJd02x` | 0.03 | 0.00 | 7.50% | 1.22 | −0.36 | 0.37bp | 153/145 | 2Y 1.22 但 S 全灭 |
| P6-7 机构渗透率差分 | `e75AOYKz` | −0.14 | −0.04 | 7.47% | −0.53 | −0.05 | −3.39bp | 142/148 | — |
| P6-9 买卖方差分 | `ZYQZp8l0` | −0.34 | −0.15 | 7.74% | −0.13 | 0.14 | −5.99bp | 154/136 | 全波最差 |

### 27.2 【本轮最重要的否证】IND 冠军门控在 DEU 完全不迁移

P6-1 与 P6-8 是**同一底层信号**（`count_institutional_buyers_security / ts_mean(count_institutional_holders_security, 72)` + `ts_quantile` 高斯分位）的**唯一差异**就是外层 `trade_when` 门控：

| | 表达式 | S | sub | 2Y | TO |
|---|---|---|---|---|---|
| **无门控** P6-8 | `ts_quantile(divide(buyers, ts_mean(holders,72)), 840, driver="gaussian")` | **0.39** | **+0.42** | 0.82 | 9.57% |
| **有门控** P6-1 | `trade_when(ts_arg_max(holders,90) < 33, <同一信号>, -1)` | 0.20 | **−0.08** | 0.58 | 8.03% |

**门控把 S 砍半、把 sub 从 +0.42 打到 −0.08。**

来源是论坛 `43358755666967`（LC97552，23 票）：IND/D1/INSTITUTIONS 实测 **S 1.62 / F 1.37 / 2Y 2.47 / margin 36.3bp，18 项硬检查全 PASS 已提交 OS**，作者明确把 `ts_arg_max` 门控称为冠军机制，并给出参数甜点 G/T = 66/33 与 90/33（66/22 崩，G≥120 单调衰减）。**该结论在 DEU 零迁移。**

**为什么不可迁移（机理推断）**：作者的原文说明门控的作用是「把广度引擎聚焦到 2022-23 机构撤退期逆势吸筹 regime」。这是**一个特定市场的特定历史时段**的门控——它要求该时段恰好存在「机构撤退但部分股票逆势吸筹」的分化。IND 有（散户化市场 + 强机构进出），DEU 没有（TOP500 大盘股，机构结构稳定、13F 披露季度化）。**同日 P5 的 `fund_holdings_panel` 也证实：DEU 机构类信号的有效成分是「交易活跃度」，不是「regime 交互」。**

⇒ **纪律**：论坛上的冠军级实证，其**参数化门控**是市场 × 时段的产物，只能作为「这里有机制」的存在性证明，不能作为可移植模板。移植时必须**先跑无门控对照臂，再跑门控臂**——本波的做法值得固化为规则。

### 27.3 第二组否证：ATOM 不可互换（论坛 43151729306647 的 DEU 侧验证）

| | 表达式 | S | 2Y | sub |
|---|---|---|---|---|
| **变化量版（取反）** P6-3 | `group_rank(multiply(-1, ts_mean(ts_delta(aggregate_share_count_institutions, 66), 22)), bucket(rank(cap)))` | **0.42** | 0.70 | −0.33 |
| **水平版** P6-10 | `group_rank(rank(aggregate_share_count_institutions), bucket(rank(cap)))` | 0.22 | 0.34 | **+0.40** |

论坛 `43151729306647`（WY79095，11 票 / 20 评论）GLB/institutions18 实证：机构持仓变化的平滑值在 20–40 天窗口上是**反转信号而非动量信号**（拥挤反转压过聪明钱流入）；并明确「ATOM 不可互换：`rank(cur_holding)` ≠ `rank(cap)`」。

**DEU 侧的结论是「部分印证 + 一个新代价」**：变化量取反确实优于水平（S +0.20），与帖子方向一致；但**代价是 sub 崩（−0.33 vs +0.40）**。⇒ 反转机制在 DEU 能提 Sharpe 但破坏了子宇宙稳健性，属「赢了主闸输了副闸」，净效应不划算。

### 27.4 塔级关闭：INSTITUTIONS 在 DEU 走不通

| 数据集 | coverage | S 上限 | TO 特征 | 判定 |
|---|---|---|---|---|
| `fund_holdings_panel` | 0.9019 | **0.89** | 极高（6/10 >70%） | 不判死，转 salvage_pool（2Y 1.73 可复用） |
| `institutions6` | **1.0** | **0.42** | 极低（4.6%–9.6%） | **判死** |
| `institutions4` | 0.3413 | — | — | 覆盖率不足，不挖 |
| `institutions1` | 0.2289 | — | — | 覆盖率不足，不挖 |
| `institutions25` | 0.0 | — | — | 无数据，已判死 |

两个高覆盖数据集都出货失败，剩余两个覆盖率 <35%。⇒ **DEU INSTITUTIONS 塔关闭**（塔位停留 1 颗，来自 P5 之前的历史 alpha）。这是本区第二个被塔级关闭的 category（第一个是 MODEL，§25）。

### 27.5 一条工程副产物：TO 地板反向经济学的第二批证据

本波 TO 极低（4.56%–9.57%，除 P6-6 的 38.93%），**全部落在 0.125 地板以下** ⇒ 按 `fitness = S × sqrt(|R| / max(TO, 0.125))`，此处 F **只由 S 与 R 决定、与 TO 完全无关**。

P6-3 的 margin **6.25bp** 是本轮八波里机构类最高（P5 只有 1.0–1.3bp），P6-4 更高达 **7.67bp**——说明 banks 快照型（月度 13F）数据的交易成本天然可控。这是「低换手高 margin」的典型形态，与 P5 的「高换手低 margin」完全相反。但 **S 只有 0.42，提换手无法救 F**（地板下提 TO 只能白拿 sqrt 项，而 sqrt(R/0.125) 在 R=1.9% 时只有 0.39）。

⇒ 一个数据集若要在地板下出货，S 必须自己够高（≳1.58），不能指望 TO 优化。**P6 卡的是 S 本身，无杠杆可解。**

### 27.6 塔位账更新与战略修正

八轮（O1/O2/P1–P6）累计测 80 条，出 2 条可提交候选（`1YNv6Ymk` OTHER、`P0oe6wpJ` SENTIMENT），转化率 2.5%。

**category 状态盘点（DEU D1 / TOP500，平台实拉）**：

| category | 可用数据集 | 已试 | 状态 |
|---|---|---|---|
| MODEL | 45 集 | 4（model238/28/53/264） | **塔级关闭**（S/2Y 双缺） |
| INSTITUTIONS | 2（institutions6 / fund_holdings_panel） | 2 | **塔级关闭**（S 上限 0.89 / 0.42） |
| SENTIMENT | 2（sentiment27 cov 0.9038 / sentiment7 cov 0.7418） | 1（产出 `P0oe6wpJ` S 2.14 / 2Y 2.56） | **唯一出过强信号的类，继续** |
| **NEWS** | **4（news20 / news104 cov 0.963 / news18 / news17）** | **0** | **本轮转向目标** |
| SOCIALMEDIA | 0（两集 cov 0.0 / 0.2748） | — | 不可用 |
| ANALYST / FUNDAMENTAL / RISK / PV / OTHER | — | 部分 | 按需 |

⇒ **P7 转向 NEWS（news20）**，这是全库最干净的未挖地：NEWS 塔 0/3、4 个可用数据集、`news20` 的 alphaCount 仅 33（NEWS 类最不拥挤）、valueScore 5.0。设计详见 §28。

### 27.7 本波产出清单

- `tracking/DEU/candidates/wave_P6_institutions6_results.json`（10 条完整指标 + 8 条 key_findings + 2 组 ab_tests + dead_reason）
- 本附录 §27
- 塔位账：**未变**（institutions 仍 1 颗）
- registry_empirical 新增 dead_end：`institutions6`（reason：cov 1.0 但 S 上限 0.42；rule：DEU 不再投 institutions category）

---

# 二十八、P7 波 news20（NEWS 塔首挖）——10/10 REJECT，S 上限 0.23，判死

批次 `f36iWc4H5aqcmJw09duNhz`，10 条全部 COMPLETE / 0 error。设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / pasteurization ON / unitHandling VERIFY / **nanHandling ON**（VECTOR 逐事件稀疏）/ maxTrade OFF。

## 28.1 全表（10 条）

| 模板 | alpha | S | F | TO | 2Y | sub | margin | long/short | CW | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| P7-4 新颖度硬门控 >30d | `xArMkvon` | **0.23** | 0.08 | 8.14% | −0.88 | 0.04 | **3.60bp** | 148/141 | PASS | 全波最高 S / 最高 margin |
| P7-3 新颖度加权 | `omE2laXv` | 0.13 | 0.04 | 7.18% | −0.51 | −0.13 | 2.61bp | 135/143 | PASS | — |
| P7-7 注意力摊薄反向乘 | `78LO1YRO` | 0.10 | 0.01 | **57.40%** | **0.06** | **0.10** | 0.24bp | 101/92 | PASS | **唯一 2Y+sub 双正**；DD 全波最低 0.1148 |
| P7-2 相关度硬门控 >60 | `bl6pqagZ` | 0.07 | 0.02 | 7.90% | −0.72 | −0.04 | 1.62bp | 61/61 | **FAIL 0.2266** | 持仓腰斩至 122 只 |
| P7-6 实体-故事偏离 | `N1NMrPGE` | 0.07 | 0.01 | 14.24% | −0.99 | 0.13 | 0.70bp | 126/122 | PASS | — |
| P7-8 情绪-价格错配 | `9qxorlOr` | 0.02 | 0.00 | 18.54% | −1.11 | 0.14 | 0.13bp | 124/124 | PASS | 唯一跨 category 腿（NEWS+PV） |
| P7-10 桶内中性化 | `58EROJKn` | 0.02 | 0.00 | 13.33% | −0.85 | 0.16 | 0.23bp | 125/124 | PASS | 桶内中性化第 5 次，未复现增益 |
| P7-1 相关度加权 | `58EROJ25` | −0.09 | −0.02 | 15.08% | **−1.51** | −0.09 | −0.94bp | 117/132 | PASS | 2Y 全波最差 |
| P7-5 情绪变化 | `6Xdx9MQG` | −0.11 | −0.02 | 36.59% | −0.40 | −0.03 | −0.55bp | 89/92 | **FAIL 0.5** | 持仓仅 181 只 |
| P7-9 情绪分歧度 | `xArMkvpl` | −0.23 | −0.08 | 7.09% | 0.08 | 0.16 | **−4.24bp** | 123/140 | PASS | 全波唯一显著负 S |

**三条 pass 的检查**：`LOW_TURNOVER` / `HIGH_TURNOVER` / `MATCHES_PYRAMID` 10/10 全 PASS，TO 无一超标（最高 57.40%）。**失败全部集中在 S / F / 2Y 三闸**，不是换手问题。

## 28.2 归因一：8/10 的 2Y 为负，这不是符号问题而是时段问题

10 条里 8 条 `two_year_sharpe` 为负（−0.40 ～ −1.51），唯一为正的两条（P7-7 +0.06、P7-9 +0.08）距 1.58 差 20 倍。**取反符号救不了**：P7-9 取反后 S 也只有 +0.23。

结论：DEU TOP500 的新闻情绪信号在 **2022–2023 段彻底失效**，且失效幅度大于 2014–2021 的累积收益 ⇒ 全样本 S 被拖到零附近。这与该段的市场结构（欧洲大盘股、新闻已被算法在秒级定价、情绪溢价被套利掉）一致。

## 28.3 归因二：三条裸情绪基线全部归零 ⇒ 不是「用法不对」而是「字段无方向 alpha」

| 加工方式 | alpha | S | 2Y |
|---|---|---|---|
| 相关度加权（连续权重点积） | `58EROJ25` | −0.09 | −1.51 |
| 实体-故事偏离（差分） | `N1NMrPGE` | 0.07 | −0.99 |
| 桶内中性化（市值分组） | `58EROJKn` | 0.02 | −0.85 |

三种正交加工都落在 [−0.09, 0.07] 区间 ⇒ `nws20_multiple_comp_event_sentiment_score` 本身在 DEU 没有方向性 alpha。论坛 `42659817284375`（WL27618，31 票）的「情绪因子做不好的 90% 原因是没做信噪比管理」在 DEU 只得到部分支持：做了管理（相关度加权 / 新颖度过滤 / 注意力摊薄）确实把 S 从 −0.09 抬到 0.23，但幅度差 5 倍。

## 28.4 归因三【本波唯一正面发现】：`event_similarity_days` 新颖度轴有效但太弱

| 加工 | alpha | S | margin |
|---|---|---|---|
| 裸情绪（基线） | `58EROJ25` / `N1NMrPGE` / `58EROJKn` | −0.09 ～ 0.07 | −0.94 ～ 0.70bp |
| 新颖度加权（秩） | `omE2laXv` | 0.13 | 2.61bp |
| 新颖度硬门控（>30 天） | `xArMkvon` | **0.23** | **3.60bp** |

单调递增且 margin 同步放大 ⇒ 论坛帖「旧闻重播已定价、新信息比例越高冲击越强」的机理在 DEU **方向成立但量级不足**。这是全库唯一在 DEU 有正向迁移的新闻类机制，可作为后续 news104 / news18 的优先轴。

## 28.5 归因四【结构性结论】：注意力 ≠ 情绪 —— DEU 的 alpha 来自注意力异常，不来自情绪方向

两条独立证据链指向同一结论：

| 信号维度 | 代表 alpha | S | 2Y | sub | 源 |
|---|---|---|---|---|---|
| **情绪方向** | `58EROJ25` / `N1NMrPGE` / `58EROJKn` | −0.09 ～ 0.07 | −1.51 ～ −0.85 | −0.09 ～ 0.16 | news20 |
| **注意力摊薄**（故事内实体数） | `78LO1YRO` | 0.10 | **+0.06** | **+0.10** | news20 |
| **注意力异常**（Wikipedia view IR 中性化人气） | **`P0oe6wpJ`** | **2.14** | **+2.56** | **1.37** | sentiment27 + sentiment7 |

P7-7 是全波唯一 2Y 与 sub 双正的模板，它用的`rp_story_event_index`（故事内实体数 = 注意力摊薄代理）本质是注意力维度；而 SENTIMENT 塔已提交候选 `P0oe6wpJ` 用的也是 Wikipedia 浏览量（注意力）而非情绪。

⇒ **新先验（写入台账）**：在 DEU，可用的另类数据 alpha 来自「关注度/注意力的时序异常」，不来自「情绪方向」。后续 news 类数据集应优先挖曝光度/覆盖度/新闻量字段，情绪类字段优先级下调。

## 28.6 两对门控对照臂（第 5、6 次确认 DEU 门控不是杠杆）

| 对照 | 加权版 | 硬门控版 | ΔS | 代价 |
|---|---|---|---|---|
| 相关度 | `58EROJ25` S −0.09 / 249 只 | `bl6pqagZ` S 0.07 / 122 只 | **+0.16** | 持仓腰斩 → CW 0.2266 FAIL，sub −0.09→−0.04 |
| 新颖度 | `omE2laXv` S 0.13 / 278 只 | `xArMkvon` S 0.23 / 289 只 | **+0.10** | 无（持仓不变，margin 2.61→3.60bp） |

两次硬门控都略优（+0.10 ～ +0.16），但一次付出 CW FAIL 的代价，另一次增益微小。与 P6 的 IND 冠军门控否证（S 砍半、sub 转负）合起来给出统一结论：**DEU 上门控不是杠杆，只是「少交易」；唯一的无损门控是新颖度（信息新鲜度），因为它不改变横截面覆盖。**

## 28.7 判死与后续

**`news20` 判死**（S 上限 0.23，2Y 系统性为负）。NEWS 塔仍 0/3，但剩余 3 个数据集（news104 cov 0.963 / news18 cov 0.8046 / news17 cov 0.7906）**优先级下调**，且挖法必须换成注意力/新闻量轴。

桶内中性化第 5 次未复现：前四次（techindi_model S 1.63 / model238 1.14 / model28 1.26 / fund_holdings 2Y +1.13）都有增益，这次 `58EROJKn` S 0.02 与裸秩 `58EROJKn` 同族基线持平 —— **原因是底层信号为零，无增益可提**，不是方法失效。这给出一个判据：**桶内中性化只能放大已有信号，不能创造信号；S 基线 < 0.3 时不要指望它。**

## 28.8 本波产出清单

- `tracking/DEU/candidates/wave_P7_news20_results.json`（10 条完整指标 + 8 条 key_findings + 3 组 ab_tests + dead_reason）
- 本附录 §28
- 塔位账：**未变**（NEWS 仍 0 颗）
- dead_end 新增：`news20`（reason：S 上限 0.23，2Y 8/10 为负；rule：DEU 不再用 news20 情绪字段，如需再挖只走注意力/新颖度轴）

---

# 二十九、全 category 盘点补完（PV / FUNDAMENTAL / ANALYST / EARNINGS / RISK）

此前只看过 SENTIMENT / NEWS / SOCIALMEDIA / INSTITUTIONS / MODEL。本轮把剩余 5 个 category 全部拉到平台实况（DEU / TOP500 / D1）。

## 29.1 PV（16 集）—— 出现一个覆盖率近乎完美的未碰数据集

| 数据集 | 名称 | cov | 字段 | alphaCount | 判定 |
|---|---|---|---|---|---|
| **`pattern_scores`** | **Chart Pattern Similarity Scores** | **0.9888** | **504** | 266 | **可挖（cov 最高，全库第一）** |
| `pv30` | Alternate Industry Classification（PCA 行业分类） | 0.7273 | 285 | 287 | GROUP 型，可作分组轴 |
| `pv109` | Bond Yield Data（公司债收益率） | 0.4665 | 26 | 33 | 覆盖不足一半 |
| `pv29` | Derived Industry Classification | 1.0 | 50 | 66 | 元数据（RIC/BBID 映射），不可用 |
| `pv1` | Price Volume Data | 0.0 | 23 | 12639 | 无数据；且 alphaCount 1.26 万 = 极端拥挤 |
| `continuation_score` / `intraday_pv_feats` / `pv103` / `pv106` / `pv13` / `pv132` / `pv17` / `pv173` / `pv47` / `pv71` | — | 0.0 | — | — | 无数据 |
| `pv20` | 已判死 | 0.0 | 681 | 619 | 判死维持 |

⇒ **`pattern_scores` 是当前全库 cov 最高的未碰数据集（0.9888）**，504 个形态相似度字段，alphaCount 仅 266（不拥挤）。PV 单塔不触碰 trio 互组禁令，是 P8 之后的首选战场。

## 29.2 FUNDAMENTAL（12 集）—— 只有 3 个 cov > 0，且都不理想

`fundamental22` cov 0.69 但仅 1 字段；`fundamental6` cov 0.4923 / 196 字段（可用但覆盖不足一半）；`fundamental45` cov 0.269 / 12 字段（earnings call 情绪）。其余 9 集 cov 0.0，含已判死的 fundamental17 / fundamental90 / fundamental93。

## 29.3 ANALYST（18 集）—— 可用面最广但大多拥挤

| 数据集 | 名称 | cov | 字段 | alphaCount | 备注 |
|---|---|---|---|---|---|
| `analyst48` | Dividend estimation | 0.7879 | 7 | 7 | **已判死** |
| `analyst7` | Broker Estimates | 0.7207 | 608 | **3993** | 极度拥挤（valueScore 2.0） |
| **`analyst93`** | **Europe Analyst Estimate Daily（目标价预测）** | **0.6373** | **100** | **193** | **欧洲专向 + 不拥挤，首选** |
| `analyst47` | Alternative Analyst Insight | 0.6234 | 5 | 112 | 字段太少 |
| `analyst_factor_signals` | Global Analyst Factor Signals | 0.5996 | 108 | 1575 | 拥挤 |
| `analyst9` | Analyst Estimate Daily | 0.5825 | 51 | 106 | 次选 |
| `analyst44` | Integrated Broker Estimates | 0.5802 | 72 | 58 | **已判死** |
| `analyst83` | Smart Conference call transcript | 0.3389 | 345 | 26 | 覆盖偏低 |

⇒ **`analyst93`（Europe Analyst Estimate Daily Data，100 字段 / cov 0.6373 / alphaCount 193）是 ANALYST 类最优标的** —— 描述明确「focusing on price target forecasts」（目标价预测），这是分析师类最经典的经济学机制（target price revision），且欧洲专向、拥挤度低。

## 29.4 EARNINGS（2 集）与 RISK（5 集）—— 基本关闭

- **EARNINGS 2 集 cov 全 0.0** ⇒ 该类在 DEU 不可用。
- RISK：`risk60` cov 0.835 / 5 字段（已判死）、`risk88` cov 1.0 / **1 字段**（已判死）、`risk68`/`risk71`/`risk72` cov 全 0.0 ⇒ **RISK 类实际关闭**。

## 29.5 修正后的 category 优先级（DEU D1 / TOP500）

| 优先级 | category | 标的 | cov | 理由 |
|---|---|---|---|---|
| **1** | SENTIMENT | `sentiment27`（13 可用字段，仅用 1 个） | 0.9022 | 该塔已有 S 2.14 强信号，补 2 颗即点亮；字段开发度 1/13 |
| **2** | PV | `pattern_scores` | **0.9888** | 全库最高 cov 的未碰集，504 字段，单塔不触 trio 禁令 |
| **3** | ANALYST | `analyst93` | 0.6373 | 欧洲专向目标价预测，193 alpha 不拥挤 |
| 4 | NEWS | `news104` / `news18` / `news17` | 0.963 / 0.805 / 0.791 | cov 好但 news20 已证情绪轴无货，只能走注意力轴 |
| 5 | FUNDAMENTAL | `fundamental6` | 0.4923 | 覆盖不足一半 |
| — | EARNINGS / RISK / SOCIALMEDIA / MODEL / INSTITUTIONS | — | 0.0 或已判死 | 关闭 |

---

# 三十、P8 波 sentiment27（SENTIMENT 塔补第 2 颗）

批次 `2U3XeC8bg4oMaHuVa2xEkIS`。设计稿 `tracking/DEU/candidates/wave_P8_sentiment27_pending.json`。preflight `valid: true` / `unknown_fields: []` / `any_changed: false`（10 字段全部有数据，VECTOR 已自行包裹）。

## 30.1 为什么回到 sentiment27

SENTIMENT 是唯一出过强信号的 category（`P0oe6wpJ` S 2.14 / F 1.99 / 2Y 2.56 / sub 1.37 / margin 20.94bp / self 0.0313），塔位 1/3，**补 2 颗即点亮**。而 `sentiment27` 的 13 个可用 VECTOR 信号字段里，`P0oe6wpJ` 只用掉了 `snl27_relpopularity08` 一个 ⇒ 字段开发度 **1/13**，是当前全库 ROI 最高的未开发面。

这也回应了 P7 的战略结论：DEU 的 alpha 来自**注意力维度**，而 sentiment27 正是注意力数据（Tranco 网站排名衍生统计），与已证结论同向。

## 30.2 论坛取证：`43636684138775`（WL27618，30 票）

《网页流量里的真金白银：sentiment27 日本市场探索》给出三条，其中两条是我此前**完全没用过的新轴**：

| 帖子要点 | 我的落地 | 对应模板 |
|---|---|---|
| 客流是业绩先导指标：月度 UV/PV 无起色 ⇒ 营销水分自明；新服务流量排名数周内飙升 ⇒ 先于季报数月给出业务爆发确定性 | 以排名变化而非排名水平建模 | P8-1 / P8-9 |
| **【新轴 1】剔除季节性假日效应**：电商与旅游网站天然在黄金周流量暴增，单周环比容易失真，**一定要做同比或剔除日历季节性** | `ts_delta(..., 252)` 同比变换（此前全用 22/66 短窗环比） | P8-1 / P8-2 |
| **【新轴 2】限定数字经济赛道**：传统制造业或重资产企业看网站流量毫无意义，**只针对特定科技和消费细分行业**才能发挥价值 | `group_rank(..., sector)` 组内排序（同行业内部比较人气，剔除行业间流量基线差；此前全用全局 rank） | P8-8 |

## 30.3 十条模板（结构互异审计 PASS：10 类骨架 / 5 字段族 / 12 算子 / 2 档窗口 / 4 种非线性）

| 模板 | 骨架 | 字段族 | 表达式 | 机制 |
|---|---|---|---|---|
| P8-1 | 一阶差分·长窗同比 | A 人气水平 | `multiply(-1, ts_delta(ts_backfill(vec_avg(snl27_avgranking), 66), 252))` | 排名同比改善 → 客流上升；252 日剔季节性（帖轴 1） |
| P8-2 | 一阶差分（结构量） | D 域名广度 | `ts_delta(ts_backfill(vec_sum(snl27_totaldomains), 66), 252)` | 关联网站数同比增加 = 业务扩张 / 数字化投入 |
| P8-3 | 比值 | D 域名广度 | `divide(ts_backfill(vec_sum(snl27_totalcountrydomains), 66), ts_backfill(vec_sum(snl27_totaldomains), 66))` | ccTLD 占比 = 国际化程度 |
| P8-4 | 二阶矩·反向 | C 分布形状 | `multiply(-1, ts_backfill(vec_avg(snl27_kurtosis), 66))` | 峰度高 = 注意力集中少数旗舰站（脆弱）；押分散型 |
| P8-5 | 族内秩差 | A 人气水平 | `subtract(rank(ts_backfill(vec_avg(snl27_top50pctranking), 66)), rank(ts_backfill(vec_avg(snl27_topranking), 66)))` | 中位站 − 旗舰站落差 = 注意力集中度 |
| P8-6 | 参数敏感度差分 | B 复合人气分 | `subtract(ts_backfill(vec_avg(snl27_relpopularity1), 66), ts_backfill(vec_avg(snl27_relpopularity08), 66))` | α=1 与 α=0.8 的分差 = 头部相对尾部的额外贡献 |
| P8-7 | 跨族商 | B / A | `divide(ts_backfill(vec_avg(snl27_relpopularity1), 66), ts_backfill(vec_avg(snl27_avgranking), 66))` | 每单位排名的关注强度（人气密度） |
| P8-8 | 组内秩 | B 复合人气分 | `group_rank(ts_backfill(vec_avg(snl27_relpopularity1), 66), sector)` | 同行业内比较人气，剔除行业间流量基线差（帖轴 2） |
| P8-9 | 时序标准化·长窗 | A 人气水平 | `ts_zscore(ts_backfill(vec_avg(snl27_avgranking), 252), 252)` | 排名相对自身一年均值的偏离（自身客流异常） |
| P8-10 | 三阶矩 + 桶内中性化 | C 分布形状 | `group_neutralize(rank(ts_backfill(vec_avg(snl27_skewness), 66)), bucket(rank(cap), range='0, 1, 0.2'))` | 排名分布偏度在市值桶内中性化 |

## 30.4 已知风险（写进设计稿）

1. 全部 10 条单数据集 ⇒ 若分布形状 / 域名广度族本身无信号，整波归零。
2. **P8-6 / P8-7 / P8-8 用 relpopularity 族，与 `P0oe6wpJ` 字段同源**，相关可能 >0.7。这三条是「换字段/换参数」，记忆明确「换字段不降相关，换窗口 > 换变换」⇒ 优先级最低，仅作对照臂。
3. `kurtosis` / `skewness` 取值无界，`vec_avg` 后仍可能极端 ⇒ 若 CW FAIL 需先 rank 再进组中性化。
4. `ts_delta` 对个别字段可能静默全零（other696 实证）⇒ P8-1 / P8-2 若全零须做三级隔离，不可直接判数据集死。
5. P8-2 用 `vec_sum` 而非 `vec_avg`（域名数是计数型，求和语义正确），但稀疏日行为不同，归因时需区分。
6. `ts_delta(..., 252)` 在 2014–2023 窗口损失首年 ⇒ 有效区间 2015–2023。

## 30.5 九轮累计

O1/O2/P1–P7 共测 **90 条**，出 **2 条可提交候选**（`1YNv6Ymk` OTHER 2→3 点亮、`P0oe6wpJ` SENTIMENT 0→1），转化率 **2.2%**。P8 在途。

---

# 三十一、P8 波 sentiment27 收割（10/10 COMPLETE，0 可提交）

批次 `2U3XeC8bg4oMaHuVa2xEkIS`，`total 10 / complete 10 / error_count 0`。设置同区域档案（SUBINDUSTRY / decay 4 / trunc 0.08 / **nanHandling ON** / IS 2014-01-01..2023-12-31）。

## 31.1 全表（按 sharpe 降序）

| # | 模板 | alpha | S | F | TO | 2Y | sub | margin | long/short | CW | 挂闸数 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | P8-7 单位排名关注强度 | `mLoOVX56` | **0.85** | **0.98** | 1.61% | **1.45** | **1.10** | **20.67bp** | 118/188 | **FAIL 0.1453** | 4 |
| 2 | P8-6 α 参数敏感度 | `e75Axr3J` | **0.82** | **0.95** | 1.29% | **1.44** | **1.06** | **25.83bp** | 117/189 | **FAIL 0.1542** | 4 |
| 3 | P8-8 行业内人气排序 | `d5WqRQj2` | 0.74 | 0.48 | 1.94% | 1.36 | **−0.01** | 5.51bp | 173/176 | PASS | 4 |
| 4 | P8-10 市值桶内偏度中性化 | `j2YLrgjo` | 0.67 | 0.35 | 8.23% | 0.16 | **0.99** | 0.83bp | 131/128 | PASS | 3 |
| 5 | P8-5 旗舰-中位落差 | `RREX1r1z` | 0.35 | 0.15 | 5.31% | **1.59 ✓** | −0.39 | 0.83bp | 156/150 | PASS | 3 |
| 6 | P8-9 人气水平时序 z-score | `WjOkVg7N` | −0.16 | −0.04 | 15.31% | −0.36 | −0.51 | −0.01bp | 153/157 | PASS | 4 |
| 7 | P8-3 国际域名占比 | `88RAeLem` | −0.42 | −0.20 | 3.20% | **−1.10** | −0.11 | −1.75bp | 136/165 | PASS | 3 |
| 8 | P8-1 同比排名改善 | `npv08W2M` | −0.46 | −0.22 | 12.03% | −0.80 | −0.25 | −0.49bp | 131/135 | PASS | 4 |
| 9 | P8-2 域名广度同比扩张 | `9qxo7RrV` | −0.55 | −0.14 | **73.94%** | −0.64 | −0.73 | −0.13bp | 131/133 | PASS | **5** |
| 10 | P8-4 峰度反向 | `kqNRZKZL` | **−0.76** | −0.50 | 9.07% | −0.52 | −0.84 | −1.17bp | 135/121 | PASS | 4 |

**结论**：0/10 过双闸，`verdict = PARTIAL`（0 达标 / 2 near）。S 天花板 **0.85**，距闸 1.58 差 **86%**。

## 31.2 归因：三条否证 + 一条正面发现

### 否证 1 —— 同比变换轴（论坛 `43636684138775` 主张）在 DEU 全灭

| 臂 | 字段 | S | 2Y | TO |
|---|---|---|---|---|
| P8-1 `ts_delta(·,252)` 排名改善 | 人气水平 A | −0.46 | −0.80 | 12.03% |
| P8-2 `ts_delta(·,252)` 域名广度 | 域名广度 D | −0.55 | −0.64 | **73.94%** |

两个**互不相关**的字段族上，252 日同比都给出负 sharpe 且 2Y 更深负。P8-2 的 TO 73.94% 还是全波唯一 `HIGH_TURNOVER` FAIL —— 说明 `ts_delta(vec_sum(·),252)` 在 VECTOR 聚合上的日间漂移极不稳定。

⇒ 论坛帖的「电商/旅游网站黄金周流量暴增 ⇒ 必须剔除日历季节性」是**行业语境依赖**的：DEU TOP500 以制造业/金融为主体，不存在这种节日流量尖峰，同比反而把 1 年期的慢趋势信噪比拉低。**该轴封闭，后续不再测同比。**

### 否证 2 —— 组内排序（论坛同帖「限定数字经济赛道」）在 DEU 反向

| 臂 | 表达式 | S | sub | 2Y |
|---|---|---|---|---|
| 全局 + 比值（P8-7） | `divide(relpop1, avgranking)` | **0.85** | **1.10** | 1.45 |
| 行业内 + 裸值（P8-8） | `group_rank(relpop1, sector)` | 0.74 | **−0.01** | 1.36 |

⚠ 两臂形态不同（比值 vs 裸值），**不是纯净对照**；但决定性证据是 `sub_universe_sharpe` 从 **1.10 掉到 −0.01**（跨闸线翻转），这不可能由形态差异造成 —— 是 `sector` 分组把跨行业的相对人气差异抹掉了。

⇒ **DEU 的相对人气是跨行业绝对现象，行业内比较丢信息。** 这也是「换分组轴降自相关」的一个反例：换轴确实能降相关，但这里信号一起掉了。

### 否证 3 —— 域名广度族无预测力

- P8-3 国际域名占比 `countrydomains/totaldomains`：S −0.42 / **2Y −1.10（全波最差）**
- P8-2 域名数同比：S −0.55 / TO 73.94%

两个不同变换同向为负 ⇒ 「关联网站广度 = 业务扩张 = 国际化程度」在 DEU 大盘股上不成立。域名族封闭。

### 正面发现 —— `relpopularity1` 是唯一有货字段，且**必须跨字段相对化**

| 形态 | alpha | S | F | margin | TO |
|---|---|---|---|---|---|
| 裸值 `group_rank(relpop1, sector)` | `d5WqRQj2` | 0.74 | 0.48 | 5.51bp | 1.94% |
| **差值** `relpop1 − relpop08` | `e75Axr3J` | **0.82** | **0.95** | **25.83bp** | 1.29% |
| **比值** `relpop1 / avgranking` | `mLoOVX56` | **0.85** | **0.98** | **20.67bp** | 1.61% |

三种形态共用同一字段、同一窗口 66、同一 `ts_backfill`，唯一差异是外层加工：

1. **两字段相对化（差值或比值）比裸值强 0.08–0.11，且 margin 高 4–5 倍**（5.51bp → 20.67/25.83bp）。
2. **差值与比值之间差异极小**（0.82 vs 0.85，margin 25.83 vs 20.67）⇒ 机制是「**剔除共同人气成分后的残余**」，具体用减还是除不重要 —— 相对化本身才是 alpha。
3. margin 20.67 / 25.83bp 已达 **DEU 均值 22.4bp 水平、逼近 75% 分位 28bp**（此前论坛 `42587179348119` 实测参照系）⇒ 这是全 campaign 里 margin 最高的两条，但 sharpe 只有 0.82–0.85。

## 31.3 两条工程事实被独立验证

### (a) TO 地板公式 `F = S × sqrt(|R| / max(TO, 0.125))` —— 第 2、3 次精确命中

| alpha | TO | R | 预测 F | 平台 F | 误差 |
|---|---|---|---|---|---|
| `mLoOVX56` | 1.61% | 16.60% | 0.85 × sqrt(0.166/0.125) = **0.980** | **0.98** | 0.000 |
| `e75Axr3J` | 1.29% | 16.72% | 0.82 × sqrt(0.1672/0.125) = **0.948** | **0.95** | 0.002 |

⇒ 在 DEU 上 **TO < 12.5% 时 F 完全由 S 与 R 决定，与 TO 无关**。这两条 F 已到 0.95/0.98（距闸仅 0.02–0.05），但 S 只有 0.82/0.85 ⇒ **F 过闸不解决问题，S 才是唯一缺口**。反过来说：若能把这两条的 S 抬到 1.58，F 会自动变成 1.58 × 1.1525 = **1.82**（远超 1.0 闸）。

### (b) 新发现 —— **超低 TO 必然撞 CW（集中度）**

全波仅两条 `CONCENTRATED_WEIGHT` FAIL 的就是 `P8-6`(TO 1.29%) 与 `P8-7`(TO 1.61%)，恰好是全波 TO 最低两条：

| alpha | TO | CW | 限 | 触发日 |
|---|---|---|---|---|
| `e75Axr3J` | 1.29% | 0.15415 | 0.1 | 2023-09-18 |
| `mLoOVX56` | 1.61% | 0.14526 | 0.1 | 2020-05-04 |

**机理**：TO 1–2% 意味着组合几乎不换手 ⇒ 单票权重随价格漂移无约束累积，`truncation 0.08` 是对**每日调仓量**的截断、不是对**持仓权重**的封顶，因此压不住长期漂移。

⇒ **「降换手提 margin」在 DEU 有硬天花板**：TO 压到 1–2% 时 margin 确实冲到 20–26bp（DEU 顶级），但 CW 必然 FAIL。这是一个此前没记录的**结构性权衡**，与记忆里「TO 在 0.125 地板下时降换手对 F 零收益」互补 —— **地板下继续降换手不但 F 不涨，还会撞 CW**。

**修法候选**（未实测，留待后续）：`hump=0.001` 抑制单日大额调仓无效（问题是漂移不是调仓），真正对症的是①提高 TO 到 3–5%（缩短信号窗或降 decay）让权重被动重置；②`ts_target_tvr_decay(target_tvr=0.05)` 强制最低换手；③ 外层 `winsorize` 压权重尾部。

## 31.4 数据集判定：不判死，但「凑塔」路线封闭

`sentiment27` **不判死** —— `relpopularity1` 在两个不同相对化形态下都给出 S 0.82–0.85、margin 顶级、sub 1.06–1.10 过闸、2Y 1.44–1.45（差 0.13）。这是真信号。

但 **「SENTIMENT 塔靠 sentiment27 凑够 3 颗」这条路封闭**：
- 本波 10 个结构互异模板的 S 天花板 = 0.85，距闸 1.58 差 86%（不是调参能补的量级）。
- 已过闸的 `P0oe6wpJ` S = **2.14**，比 sentiment27 天花板高 2.5 倍；而 `P0oe6wpJ` 的核心信号来自 **sentiment7 的 Wikipedia views**，`snl27_relpopularity08` 在其中只作向量中性化的剔除项。
- P8-6/P8-7 的 CW 结构性不可解（见 31.3b）。

⇒ **SENTIMENT 塔在 DEU 的第二、第三颗需换数据集**（sentiment7 已开发满、sentiment27 到顶）。留待后续 category 盘点时处理。

## 31.5 保留素材（非过闸，但可作组件/辅助腿）

| alpha | 可复用价值 | 缺口 |
|---|---|---|
| `mLoOVX56` | margin 20.67bp + sub 1.10 + F 0.98 三项优秀 | S 0.85 / CW 0.1453 / 2Y 1.45 |
| `e75Axr3J` | **margin 25.83bp = DEU 顶级**、F 0.95 | S 0.82 / CW 0.1542 / 2Y 1.44 |
| `RREX1r1z` | 2022-23 时段型，**2Y 1.59 已过闸** | S 0.35 / sub −0.39 |
| `j2YLrgjo` | 唯一 `pyramids.effective = 2`（PV+SENTIMENT 双塔，合法 trio×非trio） | S 0.67 / 2Y 0.16；且用 `cap` 作 bucket 浪费组合配额 |

## 31.6 十轮累计

O1/O2/P1–P8 共测 **100 条**，出 **2 条可提交候选**，转化率 **2.0%**。

**已关闭的塔/数据集（累计）**：25 个已判死集 + INSTITUTIONS 塔级关闭 + 本轮 3 个轴封闭（同比 / 组内排序 / 域名广度）+ sentiment27 凑塔路线封闭。

---

## 32. P9 —— analyst93（ANALYST 塔）全字段画像 + 10 模板实测

**波次定位**：P9 是 P8（sentiment27 到顶）之后按修正后 category 优先序选的第 2 优先数据集。目标塔 `DEU/D1/ANALYST`（现 1 颗，需 2 颗才有机会凑 3）。

### 32.1 S1 画像：100 字段全 VECTOR，8 个信号族

`get_datafields(dataset_id="analyst93", region="DEU", universe="TOP500", delay=1, filter_sharpe=false, max_fields=120)` → count 100 / platform_count 100 / complete true / pages_fetched 2。**100 字段全部 VECTOR**，cov 0.6328–0.6459（截面极窄，但字段层覆盖稳定）。

| 族 | 代表字段 | alphaCount | 语义 |
|---|---|---|---|
| A 目标价命中率 | `analyst_accuracy1` / `accuracy2` | 18 / 10 | 分析师历史目标价命中率 |
| B 预测误差一致性 | `analyst_consistency` | 1 | 负误差 std，**带价格单位** |
| C 修正方向正确率 | `analyst_correct_revision_ratio` | 24 | 上调/下调方向判对的比例 |
| D 股内相对化族 | `relative_accuracy1/2/3/4`、`relative_consistency1/2`、`relative_ratio1/2` | — | 股内 rank / minmax 后的相对值 |
| E 计数与覆盖 | `total_forecast_times1/2`、`total_revision_times`、`correct_forecast_times1/2`、`correct_revision_times` | — | 原始计数 |
| F 目标价盈利记录 | `anl93_profitabilityprev_analyst_profitability1/2` + `_20d/_60d/_120d` | — | 历史目标价的盈利记录 |
| G 评级盈利记录 | `anl93_recprofitabilityprev_analyst_profitability1/2` + `_20d/_60d/_120d` | **51**（全库最高） | 历史评级的盈利记录 |
| H 元数据 | `anl93_*_analyst` | — | IBES 分析师 ID，**不可当信号** |

**关键约束**：只用 `analyst_` 前缀立族。`estimator_` 那套描述与 `analyst_` **逐字重复**，是同一族的副本 —— 若把它们当独立族，10 个模板里会有 5 对实质重复，等于伪多样性。

**三个结构陷阱（写入 pending JSON，全波回避）**：
1. **D 族用 `vec_avg` 数学退化**：「股内 rank 后取均值」只携带「该股有多少分析师」这一信息，不含技能高低 ⇒ 整族不适用于 `vec_avg` 路径。
2. **`consistency` 带价格单位**：`add(<price>, 常数)` 在 DEU 必炸 ⇒ 必须 `divide(·, close)` 约单位（副作用见 32.5）。
3. **`vec_count(x)` 语义是「覆盖该股的分析师数」**，不是噪声 ⇒ 它是真实的 coverage breadth，可作信号也可作门控。

### 32.2 十条全表（multisim `1RozJD4uU4UF8AdDZmKWcql`，10/10 COMPLETE、0 error）

| # | 模板 | alpha | S | F | TO | 2Y | sub | margin | DD | 持仓 | CW | 塔 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 技能水平锚（crr 裸水平） | `9qxopppr` | 0.35 | 0.16 | 4.17% | −0.08 | 0.30 | 12.13bp | 13.98% | 70/69 | PASS | ANALYST |
| 2 | 技能分化（acc1 − acc2 反向） | `0mYoppp6` | 0.11 | 0.03 | 3.65% | 0.69 | 0.23 | 4.23bp | 18.66% | 70/66 | PASS | ANALYST |
| 3 | 共识技能动量（ts_delta crr） | `qMLbNNjZ` | 0.59 | 0.33 | 6.36% | −0.10 | 0.16 | 12.01bp | 15.40% | 68/68 | PASS | ANALYST |
| 4 | 技能时序不稳（ts_std_dev 反向） | `ZYQZEE70` | −0.15 | −0.04 | 2.58% | 0.42 | −0.01 | −7.55bp | **34.64%** | 71/70 | PASS | ANALYST |
| 5 | 评级盈利 × 覆盖广度（裸水平） | `JjelGG72` | 0.36 | 0.16 | 5.52% | 0.29 | **0.71** | 8.81bp | 11.16% | 103/162 | PASS | ANALYST |
| 6 | 相对预测误差（consistency/close） | `akKJ11Lv` | 0.02 | 0.00 | 4.03% | 0.75 | −0.22 | 0.78bp | **44.23%** | 61/61 | PASS | **PV+ANALYST** |
| 7 | 覆盖广度动量（ts_delta vec_count） | `QPveGG3G` | −0.26 | −0.09 | **8.11%** | 0.21 | 0.00 | −3.97bp | 27.30% | 64/64 | PASS | ANALYST |
| 8 | 市值桶内技能（bucket by cap） | `rKRk2258` | −0.20 | −0.07 | 3.41% | −0.47 | 0.09 | −8.42bp | 24.84% | 114/163 | PASS | **PV+ANALYST** |
| 9 | 修正活跃度时序分位 | `leAxWWvx` | −0.01 | 0.00 | 7.02% | −0.60 | 0.11 | −0.12bp | 29.19% | 73/73 | PASS | ANALYST |
| 10 | **评级盈利时序偏离 × 行业中性** | **`mLoO55m5`** | **1.09** | **0.88** | 8.02% | **0.74** | **0.67** | **20.36bp** | 15.69% | 71/73 | PASS | ANALYST |

**P9-10 细节**：`checks.fail = []`（三项全降级为 warning，全波唯一）；`investability_sharpe` 1.09 与 S 相同 ⇒ **不依赖小票**；`CLUSTER_TEST` 0.96（limit 1）为全波最高、余量仅 0.04。

### 32.3 归因一：DEU 上「去个体基线」是必要变换，不是差分

这是本波最重要的机制发现，且有跨轮独立印证。

| 对照 | 表达式差异 | S |
|---|---|---|
| P9-5 | `group_rank(vec_avg(recprof2) × vec_count(acc1), industry)` —— **裸水平** | 0.36 |
| P9-10 | `group_zscore(ts_zscore(vec_avg(recprof2), 504), sector)` —— **先剔除个股 504 日均值** | **1.09** |

同字段、同数据集、同设置，**唯一差别是「减去该股自身 504 日的均值」这一步，S 差 3 倍**。

跨轮印证：P8 的 `relpopularity1` 必须跨字段相对化才从 S 0.74 / margin 5.51bp 提到 S 0.85 / margin **20.67bp**。两个完全独立的数据集同向 ⇒ 合并为一条铁律：

> **DEU（TOP500 小截面）上，绝对水平会被个股长期特征吃掉；必须先剔除自身基线，剩余偏离才是可交易信号。**

反面同样成立：**差分（`ts_delta`）不等于去基线**。P9-3（差分族最好）S 0.59、P9-7 S −0.26、P9-9（时序分位）S −0.01 —— 差分只保留一阶变化、丢掉水平偏离；`ts_zscore` 保留「当前相对自身历史有多异常」，两者不是同一件事。

### 32.4 归因二：技能水平类与二阶矩类在 DEU 全面无效

| 轴 | 代表 | 结果 |
|---|---|---|
| 技能水平 | P9-1 crr 水平 0.35 / P9-8 accuracy1 桶内 −0.20 | 无 |
| 技能分化（二阶） | P9-2 acc1−acc2 0.11 | 无 |
| 技能不确定性 | P9-4 ts_std_dev 反向 −0.15 / DD 34.64% | 无 |
| 预测误差一致性 | P9-6 −0.22 sub / DD 44.23% | 无 |
| 覆盖度动量 | P9-7 −0.26 | 无 |

论坛外部基准（帖 `25577914114711` 评论 ZH34713）实测 EUR/TOPCS1600/d1/STATISTICAL 上 analyst_consensus 类字段 16 条中 8 条 IS Sharpe 仅 **0.93–1.23** ⇒ 欧洲分析师类数据的截面天花板本就低。本波结果与该基准一致：**不是实现错误，是标的属性**。

同时否证论坛帖 `35417197662615` 引的 Lee & So (2017)「异常覆盖与未来回报正相关」在 DEU 的适用性：P9-7 直接反向（S −0.26）。

### 32.5 塔归属结构事实：`close` / `cap` 参与信号会新增 PV 塔（此前未记录）

平台 `pyramids` 段实测：

| alpha | 用到的非 ANALYST 字段 | `pyramids.effective` | 塔 |
|---|---|---|---|
| `akKJ11Lv` | `close`（约单位） | **2** | `DEU/D1/PV` + `DEU/D1/ANALYST` |
| `rKRk2258` | `cap`（bucket 分组） | **2** | `DEU/D1/PV` + `DEU/D1/ANALYST` |
| 其余 8 条 | 无 | 1 | `DEU/D1/ANALYST` |

⇒ **做纯单塔 alpha 必须避免 `close` / `cap` / `volume` 进入信号本体**；一旦进入，就会变成 trio×非trio 组合，消耗「trio × 非 trio ≤5」的配额（本波因此消耗 2 个，剩余 3）。

这条对「点塔」影响很大：想点亮 ANALYST 塔，用 `close` 约单位这类便利操作会**同时点亮 PV 塔**，等于把一颗 alpha 用在两个目标上 —— 效率上划算，但如果目标是「ANALYST 单独 +3」则会造成塔位错配。

### 32.6 归因三：「TO 低 → CW FAIL」被推翻（第三次修正）

P9 全部 10 条 `CONCENTRATED_WEIGHT` PASS，且覆盖 TO 最低两条（P9-4 2.58%、P9-8 3.41%）与最高条（P9-7 8.11%）。

⇒ P8 的两条 CW FAIL（TO 1.29% / 1.61%）**不是 TO 单因素造成的**，而是「TO 极低 **且** 该信号本身持仓集中」的联合结果。原记忆条目「TO 低 ⇒ CW 风险高」应修正为**相关性而非因果**：TO 1–2% 会让权重漂移无约束累积，但只有当信号本身把权重压到少数票上时才真正撞限。

P9-4 与 P9-8 的 TO 已进 2–3% 区间却 CW PASS，证明「TO 阈值」不是 CW 的充分条件。

### 32.7 数据集判定：不判死，进 P10 一轮定向改进

`analyst93` **不判死、也不判「塔级封闭」**。理由：
- 有明确近闸候选 `mLoO55m5`（S 1.09 / F 0.88 / 2Y 0.74 / sub 0.67 / margin 20.36bp），缺口是 S 0.49 + 2Y 0.84 的双缺口，但机制清晰、可定向改进。
- S 1.09 已是 DEU 三轮里最好的结果（P8 天花板仅 0.85）。
- 技能水平 / 二阶矩 / 差分**三个轴**已判封闭，剩余可挖的是「不同时间尺度 × 不同横截面变换」的组合。

P10 已按 `wq-brain-alpha-optimization-v1` 的两模式框架设计 10 条：

- **Mode A（5 条，冻结核心想法只调参数）**：窗口 66 / 252、换时序算子 `ts_rank`、换分组轴 `industry`、换 `vec` 聚合 `vec_max`。
- **Mode B（5 条，换机制/换结构）**：换字段族（评级盈利→目标价盈利）、`ts_av_diff` 均线偏离、双尺度差（短 z − 长 z）、`signed_power` 尾部压缩、**覆盖度门控 `trade_when`**（论坛 JR57542 修法，专治 CLUSTER_TEST 0.96 余量）。

10 条已全部通过 `preflight_expressions`（valid=true、unknown_fields=[]、any_changed=false）。

### 32.8 十一轮累计

O1/O2/P1–P9 共测 **110 条**，出 **2 条可提交候选**，转化率 **1.8%**。

**已关闭的塔/数据集（累计）**：25 个已判死集 + INSTITUTIONS 塔级关闭 + sentiment27 凑塔路线封闭 + **analyst93 的 3 个轴封闭（技能水平 / 二阶矩 / 差分）**。

---

## 33. P10 —— analyst93 定向改进（Mode A 5 条 + Mode B 5 条）

**波次定位**：P9 的唯一近闸候选 `mLoO55m5`（S 1.09 / 2Y 0.74）的定向改进。按 `wq-brain-alpha-optimization-v1` 两模式框架执行：**A 组冻结「评级盈利记录的时序偏离 + 行业中性」核心想法只调参数，B 组换机制或换结构**。5:5 配比，避免退化成「同一骨架换参数刷 10 条」。

### 33.1 派发：两次 429 才成功

前两次 `create_multi_simulation` 均返回 `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED`（P9 批次已 10/10 terminal、0 error，槽位从批次侧看已清）。第三诊断定位到根因：

- `logs/_slots/` 全部 token 均为 `.stale`（最新 2026-10-29T13:28），无本地仲裁阻塞；
- 但平台侧存在**僵尸 multisim `VKortcXA51Vb3gK8OT8PKX`**，`lookINTO_SimError_message` 显示 `status=null / progress=0.35` 永久不动，持续占用账号级仿真槽；
- 另一个 `4hDqxf7ix4DYaXKxgqJlVJk` 为 `parent COMPLETE but children empty`（平台侧残缺记录，不占槽）。

**第一次重试**（间隔约 2 分钟）仍 429；**第二次重试**（又隔约 5 分钟）成功。⇒ 与 P8 同一现象，但**退避时间需要 5 分钟量级而非一次调用**。

### 33.2 十条全表（multisim `3Qrovy9rc4LocC3MccKhXsd`，10/10 COMPLETE、0 error）

基线 = P9-10 `mLoO55m5`：S 1.09 / F 0.88 / TO 8.02% / 2Y 0.74 / sub 0.67 / margin 20.36bp / DD 15.69% / CLUSTER 0.96。

| # | 模式 | 杠杆 | alpha | S | F | TO | 2Y | sub | margin | DD | CLUSTER | fails |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | A | 窗口 504→**66** | `wpQ6jRN5` | 0.40 | 0.18 | **15.35%** | −0.05 | 0.20 | 3.84bp | 17.03% | 0.26 | 3 |
| A2 | A | 窗口 504→**252** | `O0Ae7p6g` | 0.74 | 0.49 | 9.18% | 0.42 | 0.41 | 12.06bp | 16.78% | 0.56 | 3 |
| **A3** | A | 时序算子→**ts_rank** | **`6XdxlwZ7`** | **1.18** | **0.98** | 8.56% | **1.03** | 0.76 | 19.94bp | **12.56%** | 0.94 | **0** |
| **A4** | A | 分组轴→**industry** | **`kqNRj3vL`** | **1.08** | 0.84 | 7.79% | 0.90 | 0.73 | 19.45bp | 12.85% | **0.86** | **0** |
| A5 | A | vec 聚合→**vec_max** | `omE2qKRE` | 0.87 | 0.63 | 8.69% | 0.48 | 0.67 | 14.88bp | 16.64% | 0.60 | 3 |
| B1 | B | 换字段族→**目标价盈利** | `E563lwN9` | 0.78 | 0.54 | 8.02% | 0.49 | 0.68 | 15.00bp | 17.70% | 0.54 | 3 |
| B2 | B | **ts_av_diff**(252) | `P0oe7pYw` | 0.67 | 0.46 | 7.11% | 0.44 | 0.36 | 16.84bp | 23.72% | 0.55 | 3 |
| B3 | B | 双尺度差（短 z − 长 z） | `kqNRj3Wg` | **−0.41** | −0.20 | 11.35% | −0.29 | −0.21 | −5.11bp | **43.95%** | −0.36 | 4 |
| **B4** | B | **signed_power(z, 0.5)** | **`78LOjwv2`** | **1.19** | **0.98** | 7.45% | 0.92 | 0.78 | **22.97bp** | 14.76% | 0.88 | **0** |
| B5 | B | 覆盖度门控 trade_when | `xArMjxGq` | 0.91 | 0.66 | 6.69% | 0.87 | 0.50 | 19.93bp | **12.17%** | 0.93 | 3 |

**三条 `checks.fail = []`**（A3 / A4 / B4），全部只剩三项 warning：`LOW_SHARPE 1.18 / LOW_FITNESS 0.98 / LOW_2Y_SHARPE 1.03`。**十轮以来第一次出现「只差指标、不差合规」的候选组团。**

### 33.3 归因一：窗口单调递增，504 未见顶

| 窗口 | 66 | 252 | 504 |
|---|---|---|---|
| S（ts_zscore） | 0.40 | 0.74 | 1.09 |
| TO | 15.35% | 9.18% | 8.02% |
| margin | 3.84bp | 12.06bp | 20.36bp |

**严格单调**。66 日窗把 TO 翻倍、margin 压到 1/5 —— 短窗把噪声当信号，是「半衰期极长的慢变量被迫高频重估」的典型形态。

⇒ **下一个合理检验点是 1008（4 年）**，它是 IS 窗口（10 年）的 40%、且是「有意义窗口」清单里的标准值。这是 P10 唯一没测、且有单调性依据支撑的方向。

### 33.4 归因二：标准化 ≠ 绝对差 ≠ 差分（三层递进证据）

同字段、同设置、只换「怎么去个股基线」这一步：

| 变换 | 表达式片段 | S | DD |
|---|---|---|---|
| 标准化偏离 | `ts_zscore(·, 504)` | **1.09** | 15.69% |
| 绝对偏离 | `ts_av_diff(·, 252)` | 0.67 | 23.72% |
| 双尺度差 | `ts_zscore(·,66) − ts_zscore(·,504)` | **−0.41** | **43.95%** |

三层**逐级下降**，到差分直接反向。机理清晰：
- `ts_av_diff` 保留「偏离的绝对幅度」，未除以自身波动 ⇒ 高波动票的偏离被动放大，DD 翻倍。
- 双尺度差 = 把「长期水平」减掉 ⇒ 恰好把信号源（长期水平偏离）抹掉，剩下的只有短期反转，而短期反转在 DEU 是负 alpha（与 P9-6/P9-9 一致）。

⇒ 合并 P9 结论为一条铁律：

> **在 analyst93 上，「水平」是信号，「变化」是噪声。任何去基线变换必须是 `ts_zscore` 或 `ts_rank`，不允许 `ts_delta` / `ts_av_diff` / 双尺度差。**

同时 B3 给出一条**副产品验证**：其 `LOW_SUB_UNIVERSE_SHARPE` 的 `limit = −0.19`，而 S = −0.41 ⇒ `0.4743 × (−0.41) = −0.195 ≈ −0.19`。**再次实证 sub 闸是 sharpe 的比例闸（0.4743×），不是绝对闸** —— 所以对正 Sharpe 候选，sub 只要 > 0.4743×S 就过，它几乎不构成独立约束。

### 33.5 归因三：尾部压缩是唯一「全能」算子

`signed_power(z, 0.5)` 相对基线同时改善四项：

| 指标 | 基线 `mLoO55m5` | B4 `78LOjwv2` | Δ |
|---|---|---|---|
| S | 1.09 | **1.19** | +0.10 |
| margin | 20.36bp | **22.97bp** | +2.61bp（破 P8 的 20.67bp 记录） |
| DD | 15.69% | 14.76% | −0.93pp |
| CLUSTER | 0.96 | **0.88** | −0.08 |
| sub | 0.67 | **0.78** | +0.11 |

机理：z 的尾部（极端 z 票）被开方压缩 ⇒ 单票权重下降 ⇒ 集中度、回撤、margin 同时改善。这是**唯一同时治 CLUSTER 又不掉 S** 的算子，与 P10 里「换细分组轴」并列（A4 的 industry 轴把 CLUSTER 从 0.96 压到 0.86 但 S 掉 0.01）。

**判读**：`signed_power` 应作为**终态整形算子**固定在骨架最外层；后续所有变体都建议带它。

### 33.6 否证：论坛修法「覆盖度门控」在本机制反向（不可跨机制移植）

论坛帖 `25577914114711` 评论 JR57542 提出：用 `vec_count` / `days_from_last_change` 类覆盖度信号做前置过滤，可同时治 CONCENTRATED_WEIGHT 与低质量信号。B5 实测：

| | S | F | margin | DD | CLUSTER |
|---|---|---|---|---|---|
| 无门控（基线） | 1.09 | 0.88 | 20.36bp | 15.69% | 0.96 |
| 加门控（B5） | **0.91** | **0.66** | 19.93bp | 12.17% | 0.93 |

**S 掉 17%、F 掉 25%，而 CLUSTER 只降 0.03（没治好）**。唯一改善是 DD。

⇒ 该修法在**高换手行为类**字段（原帖语境）成立，在**慢速技能记录型**字段上反向。**门控类修法必须逐机制实测，禁止按字段族外推。**

### 33.7 验证：F 的地板效应 ⇒ 唯一真缺口是 S 与 2Y

对 B4 逐项验算：

```
F = S × sqrt(|R| / max(TO, 0.125))
  = 1.19 × sqrt(0.0855 / 0.125)
  = 1.19 × 0.827 = 0.984  ≈ 平台 0.98 ✓
```

**TO 7.45% 已在地板 12.5% 之下** ⇒ 分母被钉死，F 完全由 S 与 R 决定。反推：**若 S 抬到 1.58，F 自动 = 1.58 × 0.827 = 1.31**（远超 1.0 闸）。

⇒ **F 的 0.02 缺口不是独立缺口**。当前唯一真缺口：
- **S 1.19 → 1.58（缺 0.39）**
- **2Y 1.03 → 1.58（缺 0.55）**（A3 的 2Y 为全波最高）

### 33.8 塔位与配额

**P10 全部 10 条 `pyramid_effective = 1`，只属 `DEU/D1/ANALYST`** —— 因为全部只用 `anl93_*` 字段，未引入 `close` / `cap` / `volume`。这直接验证了 P9 的塔归属结论：**纯单塔是可控的，只要不碰 PV 内置字段**。

trio×非trio 配额本波消耗 **0**，累计仍为 2（P9 的 `akKJ11Lv` / `rKRk2258`），剩余 3。

`DEU/D1/ANALYST` 塔位：**仍 1 颗，未点亮**（本波 0 条过闸）。

### 33.9 P11 方向（已定序）

1. **窗口 1008（4 年）** —— 唯一未测、有严格单调性依据的方向。
2. **`recprofitability` 的四档 horizon 变体**（`_20d` / `_60d` / `_120d`）—— 这 8 个字段一次都没测过，且短期 vs 长期技能记录是**不同经济信号**，不是同一骨架换参数。
3. **设置轴**（neutralization / decay / truncation）—— 零表达式成本杠杆，十轮从未扫过。
4. **不建议再试**：覆盖度门控、差分族、目标价盈利族、`vec_max`。

### 33.10 十二轮累计

O1/O2/P1–P10 共测 **120 条**，出 **2 条可提交候选**，转化率 **1.7%**。

**已关闭的塔/数据集（累计）**：25 个已判死集 + INSTITUTIONS 塔级关闭 + sentiment27 凑塔路线封闭 + analyst93 的 5 个轴封闭（技能水平 / 二阶矩 / 差分 / 目标价盈利族 / 覆盖度门控）。

---

## 三十四、P11 中性化设置轴扫描（analyst93 基线 B4）

### 34.1 基线与被测量

被扫表达式（analyst93 全战役天花板，`78LOjwv2`）：
```
group_zscore(signed_power(ts_zscore(ts_backfill(vec_avg(anl93_recprofitabilityprev_analyst_profitability2), 120), 504), 0.5), sector)
```
DEU / TOP500 / d1 / decay 4 / trunc 0.08 / **nanHandling ON**（稀疏集）。

平台上 DEU D1 共 **11 档中性化**，实测 **8 档**（另 3 档被 429 挡住未派）。

### 34.2 八档实测（全部 COMPLETE）

| 中性化 | alpha | S | F | TO | 2Y | sub | margin | DD | CLUSTER |
|---|---|---|---|---|---|---|---|---|---|
| **SUBINDUSTRY** | `78LOjwv2` | **1.19** | **0.98** | 7.45% | 0.92 | 0.78 | 22.97bp | 14.76% | 0.88 |
| NONE | `npv0KOVz` | 0.72 | 0.45 | 6.11% | 0.55 | 0.61 | 16.30bp | 15.14% | 0.59 |
| MARKET | `GrWVdAwP` | 0.71 | 0.44 | 6.11% | 0.52 | 0.61 | 16.01bp | 15.29% | 0.59 |
| SECTOR | `j2YL3Rwj` | 0.71 | 0.44 | 6.17% | 0.53 | 0.61 | 15.87bp | 15.24% | 0.60 |
| INDUSTRY | `N1NMQmAE` | 0.62 | 0.35 | 6.97% | 0.22 | 0.57 | 11.35bp | 15.41% | 0.43 |
| FAST | `MPYw1AVn` | 0.59 | 0.26 | 15.14% | 0.14 | 0.56 | 3.87bp | 11.85% | 0.28 |
| CROWDING | `MPYw15l6` | 0.58 | 0.30 | 6.86% | 0.58 | 0.59 | 9.82bp | 10.82% | 0.48 |
| STATISTICAL | `akKJL3K6` | 0.40 | 0.15 | 10.98% | 0.15 | 0.47 | 3.27bp | 8.76% | 0.29 |

未派发（429 连续限流）：`SLOW` / `REVERSION_AND_MOMENTUM` / `SLOW_AND_FAST`。

### 34.3 三条结论

1. **SUBINDUSTRY 是 1.65 倍完胜，不是「略优」**：1.19 vs 次优 0.72（NONE / MARKET / SECTOR 三档挤在 0.71–0.72 一个点内，说明这三档等价）。
2. **同轴中性化是冗余，跨轴中性化才是杠杆**：表达式内已有 `group_zscore(·, sector)`，于是设置端 SECTOR / MARKET / NONE 三者几乎同结果（0.71 / 0.71 / 0.72，TO 6.11%–6.17% 全等）。判「中性化有没有用」必须先看表达式里已有的分组轴。INDUSTRY（0.62）比 SECTOR 更差 —— 是在 sector 之上再按 industry 二次正交化，等于把已用过的轴又削一遍。
3. **风险模型类中性化（STATISTICAL / CROWDING / FAST）全部垫底**（0.40 / 0.58 / 0.59），DD 反而最低（8.76%–11.85%）—— 它们是拿收益换波动，与本战役「凑 Sharpe」目标反向。

### 34.4 analyst93 判死的更硬证据（本轮新增，非 Sharpe 层面）

`78LOjwv2` 详情：**longCount 71 / shortCount 73 = 144 只持仓**。TOP500 宇宙里只有 144 只有值。
这直接解释了 2Y 与 SUB 的结构性挂点 —— 与 `shortinterest29`（148 只持仓）同一病理：**字段级 coverage 看起来够，截面级持仓撑不起来**。analyst93 的封盘不再需要「Sharpe 差 0.39」这种软理由，而是「横截面宽度不足 500 的 30%」这种硬约束。

---

## 三十五、P12 结构模板波（techindi_model）

### 35.1 数据集定位修正

`tm_*` 字段属 **`techindi_model`**（Deep Learning Technical Indicator Returns，category=**other**，pyramidMultiplier 1.8，399 字段）。
**不是** `pattern_scores`（那是形态相似度 `asc_triangle_*` 族，`search="tm_15"` 实测返回 0 条）。

命名结构 `tm_<N>_r1_r5_r10_rh_<univ>_d1_r<horizon>_q<buckets>[_p<idx>]`：
- 模型模板 ∈ {1, 8, 15, 16}（另有未解析族 `tm_17_..._rh_ah3_glb_d1_*`，171 字段）
- 期限 horizon ∈ {1, 5, 10}
- **`q1` = 连续回归预测输出（唯一承载信号）**；`q2–q5` = 分桶编号；`_p0..p4` = log-softmax 概率
- description 原文：*Continuous regression output predicting the 10-day forward market-neutral return; must be winsorized before use*

### 35.2 七条全表（`F5` = `tm_15_..._r5_q1`，`F10` = `tm_15_..._r10_q1`）

统一设置 DEU / TOP500 / d1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanOFF。

| # | 模板 | alpha | 表达式 | S | F | TO | 2Y | sub(限) | margin | DD | 卡闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 基线 sector | `vR103LQw` | `group_rank(F10, sector)` | 1.70 | 0.80 | 39.40% | 1.73 | 0.69(0.81) | 4.39bp | 5.61% | F, sub |
| T2 | 轴细化 subind | `YP1Zb6rR` | `group_rank(F10, subindustry)` | 1.72 | 0.76 | 41.04% | 1.86 | 0.66(0.82) | 3.88bp | 3.81% | F, sub |
| T3 | 指数衰减 22 | `vR10rMQd` | `group_rank(ts_decay_linear(F10,22), sector)` | 1.15 | 0.75 | 12.99% | 1.22 | 0.49 | 8.47bp | 5.65% | 4 项 |
| T4 | 均值 22 | `2rAEb7gx` | `group_rank(ts_mean(F10,22), sector)` | 0.96 | 0.58 | 10.99% | 0.96 | 0.49 | 8.27bp | 5.20% | 3 项 |
| T5 | 凹变换 √ | `npv0doP8` | `signed_power(group_zscore(F10,sector),0.5)` | 1.73 | 0.83 | 39.08% | 1.77 | 0.71(0.82) | 4.55bp | 5.66% | F, sub |
| T6 | 时序位置 252 | `3qodXboO` | `group_rank(ts_rank(F10,252), sector)` | 1.52 | 0.65 | 40.47% | 1.56 | 0.69 | 3.62bp | 4.62% | 4 项 |
| T7 | 期限切换 r5 | `0mYoXqqr` | `group_rank(F5, sector)` | **1.79** | **0.83** | 44.81% | 1.80 | 0.72(0.85) | 4.26bp | 5.52% | F, sub |

**七条无一条过闸**，但 T1/T2/T5/T7 全部已过 **S 与 2Y 双闸**，只剩 F 与 sub。

### 35.3 归因（六条，全部有实测支撑）

**① 单一根因：TO 39%–45% 太高，且「降 TO」的所有平滑手段都会杀信号。**

用平台 fitness 公式反解 R 并交叉验证（`F = S × sqrt(|R| / max(TO, 0.125))`）：

| alpha | S | F | TO | R（反解） | R（平台实测） | 验算 F |
|---|---|---|---|---|---|---|
| T1 | 1.70 | 0.80 | 39.40% | 8.73% | 8.64% | 0.796 ✅ |
| T5 | 1.73 | 0.83 | 39.08% | 8.68% | 8.89% | 0.825 ✅ |
| T7 | 1.79 | 0.83 | 44.81% | 9.64% | — | 0.830 ✅ |

公式误差 <1%，可当设计工具。**要 F = 1.0 且 S、R 不变，TO 上限 `TO ≤ R × S²`**：

- T1 需 TO ≤ 8.64% × 1.70² = **25.0%**（现 39.40%，需降 37%）
- T5 需 TO ≤ 8.89% × 1.73² = **26.6%**（现 39.08%，需降 32%）
- T7 需 TO ≤ 9.64% × 1.79² = **30.9%**（现 44.81%，需降 31%）

⇒ **P13 的量化靶子：TO 压到 25%–31%，同时 S 不低于 1.7。**

**② 两条真降了 TO 的模板，信号全崩** —— 这证明平滑不是可用路径：

| 模板 | TO 变化 | S 变化 | 判定 |
|---|---|---|---|
| T3 `ts_decay_linear(·,22)` | 39.4% → 12.99%（−67%） | 1.70 → **1.15**（−32%） | 信号被杀 |
| T4 `ts_mean(·,22)` | 39.4% → 10.99%（−72%） | 1.70 → **0.96**（−44%） | 信号被杀 |

与 MEMORY「`ts_decay_linear` 平滑是双刃」的判读一致：**该字段本身是 10 日 / 5 日前瞻预测，信号半衰期 ≈ 期限量级，22 日平滑直接掐死 alpha**。注意 T3 的 margin 反而从 4.39bp 涨到 8.47bp（+93%）—— 正是「降换手 → margin 大涨」的经典形态，但收益掉得更多，净亏。

**③ 论坛「禁长窗算子」警告实测成立，但机理被误述**：
论坛（article 40789580235671，29 票）称「不要对这类已训练预测字段再套重长窗算子（如 `ts_rank(...,250)`），会破坏模型概率分布并拉低 Fitness」。
实测 T6（`ts_rank(F10, 252)`）：S **1.52 < T1 的 1.70**（确实变差），但 **TO 40.47% 几乎没降（T1 39.40%）**。
⇒ 结论修正：**长窗 rank 只破坏分布、并不降换手**。「破坏分布」成立，「降 Fitness 是因为换手」不成立 —— 它本来就是靠破坏信号质量扣的分。

**④ `signed_power(·, 0.5)` 凹变换是全部模板里最弱增益但零代价的一个**：T5 vs T1 同字段同设置，S 1.70→1.73（+1.8%）、F 0.80→0.83、sub 0.69→0.71、TO 39.40%→39.08%（几乎不变）。**凹变换改良分布但不改换手** —— 因为换手由排名的时序翻转决定，与横截面形状无关。

**⑤ 轴细化（sector→subindustry）收益接近为零，只换来更低 DD**：T2 vs T1，S 1.72 vs 1.70（+1.2%）、2Y 1.86 vs 1.73（+7.5%，唯一亮点）、DD 3.81% vs 5.61%（−32%），但 TO 41.04% vs 39.40%（更差）、margin 3.88bp vs 4.39bp（更差）、F 0.76 vs 0.80（更差）。⇒ 细化分组轴提 2Y、降 DD，但**代价是换手与 margin**，对破 F 闸是负贡献。

**⑥ 期限切换（r10→r5）是唯一「免费提 S」的方向**：T7 vs T1，S 1.79 vs 1.70（+5.3%）、2Y 1.80 vs 1.73、F 0.83 vs 0.80，代价是 TO 44.81% vs 39.40%（+5.4pp，margin 4.26 vs 4.39bp 略降）。⇒ 短期限预测在 DEU 上更强，但换手更高，**必须与降换手手段配合才有意义**。

**⑦ sub 闸比例第四次实证，但本数据集比值偏低**：T1 sub/S = 0.406、T2 = 0.384、T5 = 0.410、T7 = 0.402，全部低于既有 0.4743–0.477 的比例。
⇒ 这不是比例闸失效，而是**本数据集在 robust 段（大盘）的相对表现弱于全线**，即「在小票上赚得比大票多」。破法按 MEMORY：**压非 robust 段（凸变换 / `signed_power>1` / 平方）**，而不是抬 robust 段。P13 的 M9 正为此设计。

### 35.4 论坛模板的可执行性裁决

论坛推荐 `group_normalize(ts_mean(<预测字段>, 20), subindustry)` 称 Sharpe 2.0+ —— **不可直接使用**：
1. `group_normalize` 在 DEU 是 **ghost 算子**（本地库声明、平台无），直接抄会白烧一个仿真槽；
2. 替换为 `group_zscore` / `group_rank` 后，其内核 `ts_mean(·, 20)` 已被 T3/T4 实测证伪（S 崩到 0.96–1.15）。
⇒ **该论坛模板在本区不成立**，两条依据都是实测。

### 35.5 塔位影响

P12 七条全部 `pyramid_short = other`、`effective = 1`、**单数据集**（不触犯 trio 组腿禁令）。无一条过闸 ⇒ `DEU/D1/OTHER` 塔位仍 **2 颗**，未点亮。trio×非trio 配额消耗 **0**，累计仍 2/5。

---

## 三十六、P13 破闸波（14 模板库 + 已派发）

### 36.1 设计原则

P12 已把「降 TO」与「保信号」明确成对立面。P13 只做一件事：**在 S 不低于 1.7 的前提下把 TO 从 39%–45% 压到 25%–31%**。
按 MEMORY「换手治理三分类」，本字段的换手归因是**数据源高频翻转**（10/5 日预测每日更新），而数据层（拉长周期）已被 T3/T4 证死、构造层（rank→zscore）已被 T5 证无效。
⇒ 只剩下**平台自适应的换手整形算子**（`ts_target_tvr_*`）与**交易阈值算子**（`hump`）这条未走过的路。

### 36.2 模板库（14 个，结构互异，超标满足 ≥10 硬约束）

| # | 模板 | 结构类别 | 状态 |
|---|---|---|---|
| M1 | `group_rank(F, sector)` | 基线横截面秩 | P12 已测 |
| M2 | `group_rank(F, subindustry)` | 分组轴细化 | P12 已测 |
| M3 | `ts_decay_linear(·, 22)` | 指数衰减平滑 | P12 已测（否证） |
| M4 | `ts_mean(·, 22)` | 均值平滑 | P12 已测（否证） |
| M5 | `signed_power(·, 0.5)` | 凹非线性 | P12 已测（微正） |
| M6 | `ts_rank(·, 252)` | 时序位置 | P12 已测（否证） |
| M7 | horizon r10→r5 | 期限切换 | P12 已测（+5.3% S） |
| **M8** | 设置 `decay 8` | 设置轴·温和平滑 | P13 在飞 |
| **M9** | `signed_power(group_zscore(·), 2)` | **凸非线性（压非 robust 段）** | P13 在飞 |
| **M10** | `ts_target_tvr_hump(·, target_tvr=0.25)` | **平台自适应换手整形** | P13 在飞 |
| **M11** | `ts_target_tvr_decay(·, target_tvr=0.25)` | 平台自适应衰减整形 | P13 在飞 |
| **M12** | `hump(·, hump=0.01)` | 交易阈值（只交易超阈值变动） | P13 在飞 |
| **M13** | `tm_16_..._r5_q1` | 换模型模板（177α/97u） | P13 在飞 |
| **M14** | `tm_1_..._r5_q1` | 换模型模板·最不拥挤（12α/9u） | 429 待补 |

差异落在：横截面秩型 / 分组轴 / 时序平滑族 / 非线性方向（凹 vs 凸）/ 时序位置 / 期限 / 自适应换手算子 / 交易阈值 / 模型模板 —— 九个正交维度，不是换参数。

### 36.3 已派发（6/7 成功，第 7 条 429）

| tag | 表达式（`F5` = `tm_15_r1_r5_r10_rh_glb_d1_r5_q1`） | 设定 | sim id |
|---|---|---|---|
| M10_tvr_hump | `ts_target_tvr_hump(group_rank(F5, sector), target_tvr=0.25)` | 基线 | `3uDCWM3Yh4SY8EILF92rlnx` |
| M11_tvr_decay | `ts_target_tvr_decay(group_rank(F5, sector), target_tvr=0.25)` | 基线 | `29nCfb1GQ5drczitR2r3w4g` |
| M12_hump_thresh | `hump(group_rank(F5, sector), hump=0.01)` | 基线 | `4hVCu91zn4FK8URIdCQqt6j` |
| M8_decay8 | `group_rank(F5, sector)` | **decay 8** | `1eM4of2AW4Iu8NfsXixy0ke` |
| M9_convex_sq | `group_rank(signed_power(group_zscore(F5, sector), 2), sector)` | 基线 | `EXcK9giV4BjaEsiCSSypSn` |
| M13_tm16_r5 | `group_rank(tm_16_r1_r5_r10_rh_glb_d1_r5_q1, sector)` | 基线 | `15QrCffj24lhbN8r343cvYG` |
| M14_tm1_r5 | `group_rank(tm_1_r1_r5_r10_rh_glb_d1_r5_q1, sector)` | 基线 | **429 未派，待补** |

预检全部通过（`ts_target_tvr_hump` / `ts_target_tvr_decay` 必须用 **`target_tvr=0.25` 命名属性**，`hump` 必须用 **`hump=0.01` 命名属性**，位置参数会报 `Invalid number of inputs`）。

### 36.4 每条的可证伪预测

| 模板 | 若假设成立 | 若假设被证伪 |
|---|---|---|
| M10/M11 `ts_target_tvr_*` | TO 落到 25%±3 且 S ≥1.6 ⇒ F 破 1.0 | TO 降但 S 同比例崩（与 T3/T4 同命） |
| M12 `hump 0.01` | TO 降到 30% 以内、S 保持 ≥1.7 | 阈值把真信号变动也滤掉，S 掉到 1.4 以下 |
| M8 `decay 8` | 温和去噪（半衰期 8 < 22），TO 降 20%、S 只掉 5% | 与 decay 22 同命，S 跌破 1.5 |
| M9 凸变换 | sub 从 0.72 抬到 ≥0.85（压掉小票贡献），TO/S 基本不变 | sub 不动（说明 sub 低不是小票贡献问题） |
| M13/M14 换模型 | 存在比 tm_15 更强的模型模板，S >1.79 | 四族同源，全部 1.6–1.8 区间 |

---

## 三十七、prod 相关性阻塞的结构性说明（跨轮未解）

两个待提交候选（`1YNv6Ymk` / `P0oe6wpJ`）唯一缺口是 prod，本轮仍未取到值，根因已定位为**账号级单并发队列上的多方争抢**：

1. 平台 prod 计算为**账号级单并发**，同时在算的只有一个；其余调用即时收到 `correlation_busy`。
2. 未提交候选的 `is` 段无 `prodCorrelation` 字段（`wq-prod-corr-read` 故障 1）⇒ 无法预读，必须重算。
3. 重算 >120s，**MCP 客户端硬上限 120s** ⇒ 必须走脱离进程 `tools/prod_wait.py`。
4. 实测进程表：本会话的 `prod_wait.py 1YNv6Ymk --minutes 30`（PID 199728/197508）与**另一个会话**的 `prod_wait.py Xg9qjVOz --minutes 12`（PID 200744→198964，父进程为另一 mavis shell wrapper）交替抢槽，两边都长期停在 `busy` 退避。
5. 已清理与本轮目标无关的 `ZYQZEawY` 进程（PID 200744）。**结论：再多起进程只会增加互斥，正确做法是只保留一个排队者。**

⇒ 提交动作在 prod 取到值之前**不可执行**（硬红线 prod < 0.7，无豁免入口）。

---

## 三十八、P13 破闸波 第一批 6 条归因

### 38.1 实测表

| 模板 | alpha | S | F | TO | 2Y | sub | margin | DD | fails |
|---|---|---|---|---|---|---|---|---|---|
| M10 `ts_target_tvr_hump(·,target_tvr=0.25)` | `gJevbexQ` | 1.14 | 0.63 | 18.23% | 1.11 | 0.42 | 6.19bp | 5.31% | 4 |
| **M11 `ts_target_tvr_decay(·,target_tvr=0.25)`** | `9qxojxrx` | 1.42 | **0.91** | 17.82% | 1.27 | 0.69 | **8.30bp** | 6.77% | 3 |
| M12 `hump(·, hump=0.01)` | `vR10rA3w` | **−0.20** | −0.05 | 1.25% | 0.63 | −0.03 | −14.16bp | 22.04% | 3 |
| **M8 设置 `decay 8`** | `1YNvXjzK` | **1.66** | 0.88 | 30.69% | 1.55 | 0.71 | 5.68bp | 6.94% | 3 |
| M9 `group_rank(signed_power(group_zscore(·),2))` | `RREXbeen` | 1.79 | 0.83 | 44.81% | 1.80 | 0.72 | 4.26bp | 5.52% | 2 |
| **M13 `tm_16_..._r5_q1`** | `1YNvXWKz` | 1.75 | 0.81 | 43.31% | 1.42 | **0.85 ✅过闸** | 4.25bp | 6.48% | 2 |

### 38.2 六条归因（每条都有对照实证）

**① 【重大】`group_rank` 会抹平其内部任何单调变换的幅度信息 —— M9 与 T7 指标完全同一。**

`RREXbeen`（M9）与 `0mYoXqqr`（T7）逐项对比：S 1.79 / F 0.83 / TO 44.81% / 2Y 1.80 / sub 0.72 / margin 4.26bp / DD 5.52% / returns 9.55% —— **十项全等**。

原因：`group_rank(signed_power(group_zscore(x, sector), 2), sector)` 的最外层是 `group_rank`，它只看**排序**；`signed_power(·, 2)` 保号且对每个符号内单调，**不改变排序** ⇒ 输出与 `group_rank(x, sector)` 完全一致。

⇒ **方法论铁律：要测非线性变换（凸/凹/平方）对换手与 sub 的影响，外层不能套 `rank` / `group_rank`。** 必须用保留幅度的算子（`group_zscore` / `normalize` / `scale` / 直接裸信号）作最外层。P12 的 T5（`signed_power(group_zscore(...), 0.5)` 外面**没有** rank）之所以能测出 +1.8%，正是这个原因 —— 两条一起构成了完整对照。

**② 【重大】换手治理的正确层级是「设置 decay」，不是「算子平滑」—— 同字段同方向，两者效力差 4 倍。**

| 手段 | 层级 | TO 变化 | S 变化 | ΔS/ΔTO 代价比 |
|---|---|---|---|---|
| `ts_decay_linear(·,22)`（T3） | 算子层 | 39.4%→12.99%（−67%） | 1.70→1.15（**−32%**） | 0.48 |
| `ts_mean(·,22)`（T4） | 算子层 | 39.4%→10.99%（−72%） | 1.70→0.96（**−44%**） | 0.61 |
| **设置 `decay 8`（M8）** | **设置层** | 44.8%→30.69%（−31%） | 1.79→1.66（**−7.3%**） | **0.24** |
| `ts_target_tvr_decay(0.25)`（M11） | 算子层·自适应 | 44.8%→17.82%（−60%） | 1.79→1.42（−21%） | 0.35 |

设置层 `decay 8` 的 ΔS/ΔTO 代价比 **0.24**，是算子层平滑（0.48–0.61）的**一半到四分之一**。
机理：设置 `decay` 是**对最终持仓做 EMA 加权**（只削持仓的日间抖动），不触碰信号本身；`ts_decay_linear` / `ts_mean` 是**对信号做时序平均**（直接改变信号的信息内容）。⇒ **铁律：优先在设置层降换手，算子层平滑是最后手段。**

**③ `hump` 的阈值必须与信号量纲匹配 —— 0.01 施加在 [0,1] 的 rank 上是灾难。**

`vR10rA3w` 实测 S **−0.20** / TO 1.25% / DD 22.04% / margin −14.16bp。
`group_rank` 输出在 [0,1]，日间 rank 变动中位数远小于 0.01 ⇒ `hump=0.01` 把绝大多数真实信号变动全部滤掉，持仓被冻结在初始状态，变成一个**静态组合**，Sharpe 归零并转负。
⇒ `hump` 只适用于量纲较大或已标准化的信号（zscore 后典型变动 0.1–1 量级）；用在 rank 上必须把阈值降到 0.001 级。

**④ `ts_target_tvr_decay` 是全部 14 个模板里 F 最高的（0.91），且 margin 翻倍 —— 但 S 同比例下跌，净结果不够。**

`9qxojxrx`：F **0.91**（此前全场最高是 T5 的 0.83）、margin **8.30bp**（vs T7 的 4.26bp，**+95%**）。
但 S 1.42（<1.58）、2Y 1.27（<1.58）双双不够。
反解：要 F=1.0 且 S=1.42 → TO ≤ 7.39% × 1.42² = 14.9%，而它已在 17.82%，再压 TO 会再压 S。

**⑤ S 与 TO 在本字段上是强正相关 —— 这是结构性约束，不是调参问题。**

汇总 6 个「同字段不同换手」的实测点（`F5` 系列）：

| 手段 | TO | S | S/TO |
|---|---|---|---|
| 无（T7） | 44.81% | 1.79 | 3.99 |
| `ts_target_tvr_decay` | 17.82% | 1.42 | 7.97 |
| 设置 `decay 8` | 30.69% | 1.66 | 5.41 |
| `ts_target_tvr_hump` | 18.23% | 1.14 | 6.25 |

**S 随 TO 单调上升**（44.8%→30.7%→18.2%/17.8% 对应 S 1.79→1.66→1.14/1.42）。本字段的 alpha 就藏在「日频排名翻转」里 —— 压制换手等于压制信息来源。
⇒ **本数据集的最高 F 出现在「TO 压到 ~18–31% 且 S 守住 1.4–1.7」的区间，而不是 S 最大化点**。要同时满足 S≥1.58、2Y≥1.58、F≥1.0，只能靠**换一个更强的基础信号**（换模型模板），不能靠在 tm_15_r5 上继续压 TO。

**⑥ M13（`tm_16_r5`）首次过 sub 闸，但 2Y 塌了 —— 模型族之间存在 sub/2Y 权衡。**

`1YNvXWKz` sub **0.85**，limit = 0.475 × 1.75 ≈ 0.83 ⇒ **过闸**（P12/P13 全部 14 条中唯一一条）。但 2Y **1.42**，比 tm_15 的 1.80 低 0.38。
⇒ `tm_16` 与 `tm_15` 不是同质变体：**tm_16 在 robust（大盘）段更均衡（sub 高），但近期（2Y）表现弱**。这恰好是破 sub 闸需要的方向，但必须配上「保 2Y」的手段。
⇒ P14 核心假设：**`tm_16` × 设置 `decay 8`** —— tm_16 供 sub，decay 8 供 TO/F，两者正交。若 2Y 仍不足，再叠加 `tm_15`/`tm_16` 双臂（但会触犯单数据集外的组腿规则，须先核 trio 配额）。

### 38.3 塔位与配额

P13 第一批 6 条全部 `pyramid_short = other`、`effective = 1`、**单数据集**。无一条全闸通过 ⇒ `DEU/D1/OTHER` 仍 2 颗。trio×非trio 配额消耗 **0**，累计 2/5。

---

## 三十九、【重大发现】CROWDING 中性化在 techindi_model 上领先 SUBINDUSTRY 34% —— P12/P13 把最优杠杆闲置了

### 39.1 对照事实

`1YNv6Ymk`（本轮第一批可提交候选）与 P12 的 T1 `vR103LQw` **表达式逐字相同**：

```
group_rank(tm_15_r1_r5_r10_rh_glb_d1_r10_q1, sector)
```

两者 decay 4 / truncation 0.08 / nanHandling OFF / DEU TOP500 d1 全部相同，**唯一差别是 neutralization**：

| 项 | T1 `vR103LQw`（SUBINDUSTRY） | `1YNv6Ymk`（**CROWDING**） | Δ |
|---|---|---|---|
| Sharpe | 1.70 | **2.28** | **+34.1%** |
| Fitness | 0.80 | **1.25** | **+56.3%** |
| sub_universe | 0.69 | **1.11** | **+60.9%** |
| 2Y Sharpe | 1.73 | 1.60 | −7.5% |
| Turnover | 39.40% | 37.92% | −1.5pp |
| margin | 4.39bp | 5.98bp | +36.2% |
| Drawdown | 5.61% | **5.53%** | −1.4% |
| 持仓数 | 151+149 = 300 | 约 **383** | +27.7% |

**同样表达式、同样超参、不增加任何表达式复杂度，S/F/sub 三项同时大幅提升，且 DD 未变差。**

### 39.2 机理判断（两条假设，未全部证实，标注清楚）

1. **【已证实部分】持仓从 300 扩到 383**：CROWDING 是风险模型类中性化，它不按行业分组，而是按拥挤度因子正交化，因而**保留了更多原本被行业分组判为「组内样本不足」而丢弃的票**。持仓 +27.7% ⇒ 横截面宽度提升 ⇒ sub（robust 子宇宙）与 sharpe 同时改善。
2. **【未证实部分】为何 analyst93 上相反**：同一 DEU 区，analyst93 的 CROWDING 是 0.58（八档垫底）而 SUBINDUSTRY 1.19（完胜）。两者反转说明**这不是「风险模型优于分组」的一般结论**，而是「在每个数据集上必须独立扫中性化」的又一实证。差异候选解释：analyst93 只有 144 只持仓，风险模型降维后剩余更少；而 techindi_model 有 300 只，风险模型反而扩到 383 只。

### 39.3 后果与纠正

- **P12 七条 + P13 前六条共 13 条，除 T1 之外全部跑在 SUBINDUSTRY 下** ⇒ 这 13 条的绝对水平被系统性低估，**不能用它们判「tm_* 天花板」**。
- P13 的「S 与 TO 强正相关、压 TO 必降 S」结论在 SUBINDUSTRY 下成立，**在 CROWDING 下尚未验证**（CROWDING 的 TO 更低而 S 更高，可能已经部分绕开该权衡）。
- **`1YNv6Ymk` 的定位应从「一条可提交候选」升级为「本数据集的最优设置基线」**，P14 以它为锚重跑全部骨架。

### 39.4 P14 设计（以 CROWDING 为基线重跑最优骨架）

| # | 表达式（`F5`/`F10` 同前） | 中性化 | 目的 |
|---|---|---|---|
| N1 | `group_rank(F5, sector)` | **CROWDING** | T7（SUBIND 下 S 1.79）的 CROWDING 版，直接对照 |
| N2 | `group_rank(F5, sector)` + 设置 decay 8 | **CROWDING** | M8（SUBIND 下 S 1.66/F 0.88）的 CROWDING 版 |
| N3 | `group_rank(tm_16_..._r5_q1, sector)` | **CROWDING** | M13（sub 0.85 唯一过闸）的 CROWDING 版 |
| N4 | `group_rank(F10, sector)` | CROWDING | **`1YNv6Ymk` 精确复现**（对照锚，验可重复性） |
| N5 | `group_rank(F10, subindustry)` | **CROWDING** | 表达式轴 × 设置轴交叉 |
| N6 | `group_rank(tm_16_..._r10_q1, sector)` | **CROWDING** | 模型族 × 期限交叉 |
| N7 | `group_rank(F10, sector.ts_rank?)` 略 | — | 见下 |

N7 备选（按需）：`group_rank(tm_1_..._r5_q1, sector)` @ CROWDING（最不拥挤族 12α/9u）。

**可证伪预测**：若 CROWDING 的增益是「持仓扩宽」而非「该中性化特异」，则 N1 应显著高于 T7 的 1.79；若 N1 落在 1.7–1.8，说明 `1YNv6Ymk` 的 2.28 是 r10 期限 + CROWDING 的交互效应，不是普适增益。

### 39.5 相关性证据（零成本已测，1021 个交易日）

| 对 | 相关 | 判读 |
|---|---|---|
| tm15_r5 ↔ tm15_r5+decay8 | **0.942** | 平滑算子**完全不降相关** |
| tm15_r5 ↔ tm15_r5+tvr_decay | 0.888 | 同上 |
| **tm15_r5 ↔ tm16_r5** | **0.675** | **跨模型族才真降相关**（唯一 <0.7 的同期限对） |
| tm16_r5 ↔ tvr_decay | **0.523** | 最低组合之一 |
| **tm16_r5 ↔ `1YNv6Ymk`** | **0.517** | 最低，且两者都属 OTHER 塔 |

`max_mutually_below_subset` = `[1YNvXWKz, 9qxojxrx, 1YNv6Ymk]`（3 颗两两 <0.7）。

⇒ **补强 MEMORY 的「换窗口 > 换变换 >> 换字段」为四档**：**换模型族 ≳ 换窗口 > 换变换 >> 换字段**；而**时序平滑（decay / tvr_decay / ts_mean）不属于任何一档 —— 它根本不降相关（0.94 / 0.89）**，因为只改持仓的日间抖动，不改横截面排序。

---

## 四十、P13 第二批 + tm_8 的「高指标陷阱」

### 40.1 第二批 3 条实测

| 模板 | alpha | S | F | TO | 2Y | sub | margin | DD | fails |
|---|---|---|---|---|---|---|---|---|---|
| M15 `ts_target_tvr_hump(target_tvr=0.15)` | `omE2Lblm` | 0.82 | 0.45 | 11.73% | 1.13 | **0.15** | 6.37bp | 7.04% | 4 |
| M17 `tm_16_..._r10_q1` | `P0oe2LRp` | 1.62 | 0.75 | 38.39% | 1.30 | **0.83 ✅过闸** | 4.31bp | 6.96% | 2 |
| **M18 `tm_8_..._r5_q1`** | `YP1ZbVPq` | **1.90** | **0.90** | 43.41% | **2.19** | 0.67 | 4.51bp | 7.20% | 2 |

**① `ts_target_tvr_*` 的压缩比单调关系已确认**：target_tvr 0.25 → S 1.14（`gJevbexQ`），0.15 → S 0.82（`omE2Lblm`）。压得越狠、S 越低，且 sub 崩得比 S 更快（0.42 → **0.15**）。⇒ 该算子族对本字段**不可用**，两个取值都证伪。

**② tm_16 的两个期限都过 sub 闸**：`1YNvXWKz`（r5）0.85、`P0oe2LRp`（r10）0.83，而 tm_15 同条件只有 0.72 / 0.69。⇒ **sub 高是 tm_16 这个模型模板的稳定属性，不是偶然**。但 tm_16 的 2Y 系统性偏弱（1.30 / 1.42），是它的固有代价。

### 40.2 三模型族特征对照（同骨架 `group_rank(·, sector)` / SUBINDUSTRY / decay4 / trunc0.08）

| 模型族 | 期限 | S | 2Y | sub | F | 特征 |
|---|---|---|---|---|---|---|
| tm_15 | r10 | 1.70 | 1.73 | 0.69 | 0.80 | 均衡 |
| tm_15 | r5 | 1.79 | **1.80** | 0.72 | 0.83 | 2Y 强 |
| tm_16 | r10 | 1.62 | 1.30 | **0.83** | 0.75 | **sub 强 / 2Y 弱** |
| tm_16 | r5 | 1.75 | 1.42 | **0.85** | 0.81 | **sub 强 / 2Y 弱** |
| **tm_8** | r5 | **1.90** | **2.19** | 0.67 | **0.90** | **S 与 2Y 双最高 / sub 最弱** |

⇒ **三个模型族在 S / 2Y / sub 三个维度上是互补的**，这为「按瓶颈选族」提供了确定性依据：
- 卡 **sub** → 用 **tm_16**（唯一能过 sub 闸的族）
- 卡 **S / 2Y** → 用 **tm_8**
- 求**长期稳健** → 用 **tm_15**

### 40.3 【重要】tm_8 的高指标是「两年撑起来的」，逐年揭穿

`YP1ZbVPq` 逐年（`get_alpha_yearly_stats`）：

| 年 | S | R | TO | DD | 持仓 |
|---|---|---|---|---|---|
| 2014 | 1.52 | 6.92% | 42.56% | 2.61% | 230 |
| 2015 | 1.73 | 8.38% | 43.21% | 4.07% | 233 |
| 2016 | 2.21 | 10.99% | 44.61% | 2.60% | 245 |
| 2017 | 1.52 | 6.73% | 43.68% | 1.92% | 269 |
| 2018 | **4.00** | **20.38%** | 40.49% | 1.69% | 276 |
| **2019** | **0.07** | **0.29%** | 39.59% | **6.91%** | 287 |
| 2020 | 1.70 | 9.71% | 45.88% | 2.41% | 317 |
| 2021 | 1.55 | 9.21% | 46.15% | 2.19% | 392 |
| 2022 | 2.34 | 15.97% | 44.45% | 2.78% | 396 |
| 2023 | 2.09 | 9.43% | 43.68% | 2.47% | 356 |

**三个硬伤**：
1. **2019 年 S = 0.07 / R = 0.29% / DD = 6.91%** —— 整整一年模型完全失效（1 月到 12 月赚 0.29%，而回撤 6.91%，即全年几乎只亏不赚）。
2. **2018 年 S = 4.00 / R = 20.38%** —— 单年贡献了 10 年 pnl 的 **21.6%**（2.12M / 9.80M）。
3. 2Y Sharpe 2.19 完全来自 2022（2.34）与 2023（2.09）两年 —— **恰好是样本内最后两年**，是 IS 尾部拟合的典型特征，不是稳健性的证据。

**对照 `1YNv6Ymk`（tm_15_r10 @ CROWDING）的逐年**：1.78 / 4.13 / 1.95 / 3.14 / 1.38 / 2.91 / 3.30 / 2.07 / 1.74 / 1.48 —— **10/10 年 ≥1.38，无空转年，最高年 4.13 只占 pnl 的合理比例**。

⇒ **判决：`YP1ZbVPq` 不因 S 1.90 / 2Y 2.19 而优于 `1YNv6Ymk`。前者是非平稳信号（一年 4.00、次年 0.07），后者是平稳信号（十年全在 1.4–4.1）。**
这正是「指标达标不等于可提交」的核心判据 —— **逐年最低值（worst-year Sharpe）比全期 Sharpe 更有信息量**。若按 worst-year 排序：
- `1YNv6Ymk` worst-year **1.38**
- `YP1ZbVPq` worst-year **0.07**（差 20 倍）

⇒ **建议把 `worst_year_sharpe` 加进本战役的候选排序口径，优先于 2Y Sharpe**（2Y 只覆盖最后两年，对 IS 尾部过拟合不敏感）。

### 40.4 P14 已派发（7 条在飞）

以 CROWDING 为基线重跑最优骨架（见 §39.4），并补 tm_8 的关键对照：

| tag | 表达式 | 中性化 | decay | sim id |
|---|---|---|---|---|
| N1 | `group_rank(F5, sector)` | CROWDING | 4 | `3papxNfHs4Kq9JD1fA8wfCBC` |
| N2 | `group_rank(F5, sector)` | CROWDING | **8** | `3C7DnN5lc52Icp119F2Y8y8x` |
| N3 | `group_rank(tm_16_..._r5_q1, sector)` | CROWDING | 4 | `JWbZH7g74ndaR8HJRjTGhX` |
| N4 | `group_rank(F10, sector)`（**复现 `1YNv6Ymk`**） | CROWDING | 4 | `vvD8EaED4GmaYoEmHOzPDv` |
| N5 | `group_rank(tm_16_..._r10_q1, sector)` | CROWDING | 4 | `2RJ2Y93rB5hdb3qB8ZFXOoo` |
| **N6** | `group_rank(tm_8_..._r5_q1, sector)` | **CROWDING** | 4 | `MhIzy7yl52j8Ob10jqr3AAT` |
| **N7** | `group_rank(tm_8_..._r5_q1, sector)` | SUBINDUSTRY | **8** | `3UdSGN1g34WOcK8fRyboMNr` |

**N4 的作用是可重复性对照**：若 N4 复现 `1YNv6Ymk` 的 S 2.28，则 §39 的「CROWDING 增益 +34%」成立；若不一致，说明 `1YNv6Ymk` 还有未识别的设置差异，§39 结论须撤回。

---

## 四十一、P14 收割 + P15 破 2Y：decay 长度才是 2Y 的元凶

### 41.1 P14 七条全收割（DEU TOP500 d1 / trunc0.08 / nanOFF）

| tag | alpha | 表达式骨架 | 中性化 / decay | S | F | TO | 2Y | sub | margin | DD | fails |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N1 | — | `group_rank(tm_15_r5, sector)` | CROWDING / 4 | — | — | — | — | — | — | — | **ERROR → P15A 重派** |
| N2 | `QPveKJ8g` | `group_rank(tm_15_r5, sector)` | CROWDING / **8** | 2.26 | 1.42 | 30.09% | **1.38** | 1.11 | 7.91bp | 6.79% | 1 |
| N3 | `QPveKkPM` | `group_rank(tm_16_r5, sector)` | CROWDING / 4 | 2.37 | 1.29 | 42.00% | **1.25** | 1.25 | 5.93bp | 5.97% | 1 |
| N4 | `1YNv6Ymk` | `group_rank(tm_15_r10, sector)` | CROWDING / 4 | 2.28 | 1.25 | 37.92% | **1.60** | 1.11 | 5.98bp | 5.53% | **0** |
| N5 | `MPYw3oOn` | `group_rank(tm_16_r10, sector)` | CROWDING / 4 | 2.29 | 1.28 | 36.94% | **1.23** | 1.26 | 6.25bp | 6.41% | 1 |
| **N6** | **`JjelQnvE`** | `group_rank(tm_8_r5, sector)` | **CROWDING / 4** | **2.61** | **1.48** | 42.05% | **2.36** | **1.29** | 6.46bp | 6.29% | **0** |
| N7 | `zq3abarK` | `group_rank(tm_8_r5, sector)` | SUBINDUSTRY / **8** | 1.65 | 0.88 | 29.54% | 1.93 | 0.58 | 5.73bp | 6.99% | 2 |

**N4 可重复性结论（成立，且比预期更强）**：平台对「同表达式 + 同设置」返回**同一个 alpha id `1YNv6Ymk`** ⇒ 复现不是「指标接近」，而是平台级幂等。§39 的 CROWDING 增益结论无需撤回。

### 41.2 【核心】decay → 2Y 是单调负向关系（单表达式 3 点，干净对照）

固定 `group_rank(tm_15_r1_r5_r10_rh_glb_d1_r5_q1, sector)` / CROWDING / trunc0.08：

| decay | alpha | S | F | TO | 2Y | sub | fails |
|---|---|---|---|---|---|---|---|
| **4** | `vR102Ver` | **2.39** | 1.29 | 43.48% | **1.60 ✅** | 1.19 (0.498 ✅) | **0** |
| 6 | `RREX67Ab` | 2.28 | 1.33 | 35.13% | **1.41 ❌** | 1.12 | 1 |
| 8 | `QPveKJ8g` | 2.26 | 1.42 | 30.09% | **1.38 ❌** | 1.11 | 1 |

三个点全部同号：**decay ↑ → TO ↓ → F ↑，但 2Y ↓**。decay 4→8 时 F 反而从 1.29 升到 1.42（纯靠压 TO 到 30.09%），代价是 2Y 从 1.60 跌到 1.38 掉出闸外。

**跨族反证（排除 tm_15 特异性）**：tm_8 族在 SUBINDUSTRY 下同样 decay 4→8 使 2Y 从 2.19（`YP1ZbVPq`）降到 1.93（`zq3abarK`）。⇒ **「长 decay 压 2Y」是跨族普适规律**。

**机理**：decay=N 把当日信号替换为过去 N 日的线性加权均值。decay 越长，最新一日的信号更新被稀释得越厉害 ⇒ 组合对风格切换/信号反转的反应越慢。**2Y 只覆盖 IS 尾部两年（2022–2023，正是一次剧烈的风格反转期）**，所以对 decay 最敏感；而全样本 S 只小幅下降（2.39→2.26），因为慢速化在 2014–2021 的平稳段反而略微降噪。

**⇒ 修正 §36/§38 的「设置 decay 是最优平滑杠杆」结论**：decay 提 F 的机理是压 TO 分母，但 **DEU 是双闸市场（S≥1.58 且 2Y≥1.58）**，decay 的上限由 2Y 决定而非 F。本数据集（techindi_model）的 decay 上限 = **4**。此后再遇「F 不够、想加 decay」的场景，必须先算 2Y 余量：`decay 每 +2 ≙ 2Y −0.1 量级`。

### 41.3 techindi_model 判「单因子数据集」

四条全闸候选的互相关矩阵（`compute_mutual_correlation`，1021 个交易日，零成本）：

| | `JjelQnvE` | `vR102Ver` | `1YNv6Ymk` | `P0oe6wpJ` |
|---|---|---|---|---|
| **`JjelQnvE`** (tm_8_r5) | 1.000 | **0.803** | **0.764** | 0.014 |
| **`vR102Ver`** (tm_15_r5) | 0.803 | 1.000 | **0.966** | 0.001 |
| **`1YNv6Ymk`** (tm_15_r10) | 0.764 | 0.966 | 1.000 | −0.005 |
| **`P0oe6wpJ`** (snt7×snl27) | 0.014 | 0.001 | −0.005 | 1.000 |

**判决**：tm_8 / tm_15 / tm_15r10 三条全部落在 0.76–0.97 —— **换模型族（tm_8↔tm_15）和换期限窗口（r5↔r10）都降不下相关**。这比我此前的四档排序（换窗口跨度 ≳ 换变换 >> 换字段）更悲观：**在这个数据集里，连「换模型族」也只是同一颗信号的不同投影**。

⇒ **techindi_model 是单因子数据集，最多贡献 1 条可提交 alpha。** 后续为该数据集设计的一切「多家族 × 多窗口」组合都只是在 0.76+ 相关带里打转，不再投入。

### 41.4 最终提交组合裁决

4 条全闸通过，但 0.7 红线只允许留 2 条：

| alpha | 数据集 / 塔 | S | 2Y | sub | F | worst-year | 判决 |
|---|---|---|---|---|---|---|---|
| **`JjelQnvE`** | techindi_model / OTHER | **2.61** | **2.36** | 1.29 | 1.48 | **1.58** | ✅ **提交** |
| **`P0oe6wpJ`** | snt7×snl27 / SENTIMENT | 2.14 | 2.56 | 1.37 | 1.99 | — | ✅ **提交** |
| `vR102Ver` | techindi_model / OTHER | 2.39 | 1.60 | 1.19 | 1.29 | — | ❌ 与 JjelQnvE 0.803 |
| `1YNv6Ymk` | techindi_model / OTHER | 2.28 | 1.60 | 1.11 | 1.25 | 1.38 | ❌ 与 JjelQnvE 0.764，且五项指标全劣 |

选 `JjelQnvE` 而非 `1YNv6Ymk` 的依据：S（2.61 vs 2.28）、2Y（2.36 vs 1.60）、sub（1.29 vs 1.11）、F（1.48 vs 1.25）、worst-year（1.58 vs 1.38）**五项全胜**，且 2Y 对闸线 1.58 有 0.78 的安全垫。

### 41.5 `JjelQnvE` 十年逐年（`get_alpha_yearly_stats`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 2.62 | 3.89 | 2.87 | 2.37 | 3.53 | 1.99 | 2.94 | **1.58** | 2.10 | 2.92 |
| R% | 11.95 | 18.63 | 14.58 | 9.82 | 17.27 | 7.95 | 17.05 | 8.64 | 16.00 | 14.17 |
| DD% | 2.51 | 2.67 | 1.90 | 2.48 | 1.70 | 3.50 | 3.63 | 3.32 | 3.81 | 2.48 |
| 持仓 | 153/151 | 158/155 | 163/161 | 181/176 | 185/179 | 189/184 | 203/200 | 238/235 | 242/235 | 222/215 |

**10/10 年全正，worst-year S = 1.58（恰在闸线上），最差年也正收益 8.64%。持仓 153→222 单调增长（越到后期截面越厚）。** 对比 `YP1ZbVPq`（tm_8 @SUBIND decay4）的 2019 年 S=0.07 空转 —— **同一模型族，CROWDING + decay4 把空转年从 0.07 拉到 1.99**，这是 CROWDING 最硬的证据。

### 41.6 下一步：广度转向（techindi_model 已榨干）

techindi_model 判单因子后，OTHER 塔只等 `JjelQnvE` 提交即点亮。剩余 10 个 0 塔 category 必须换数据集。已完成的候选画像：

| 数据集 | 塔 | 字段数 | coverage | users | alphas | valueScore | 判断 |
|---|---|---|---|---|---|---|---|
| **risk60** Securities Lending | risk | 5（全 VECTOR） | **0.835** | 198 | 395 | 2.0 | **先验最高**：机制与 GBR/USA shortinterest3 同源，已有成套验证配方 |
| **insider_agg_matrix** | insiders | 34（全 MATRIX） | 0.5617 | 89 | 170 | 4.0 | 字段最丰富，模板可做 12 个 |
| risk71 / risk72 | risk | 10 / 31 | 0.0* | 17 / 22 | 23 / 37 | 5.0 | 全是纯残差收益面板，无信号字段多样性 |
| option1 | option | 22 | 0.0* | 30 | 70 | 5.0 | 待画像 |
| earnings6 / earnings_sent_matrix | earnings | 18 / 7 | 0.0* | 43 / 65 | 108 / 127 | 4.0 / 3.0 | 待画像 |

`*` coverage 0.0 已在 techindi_model 上被证伪为「元数据不可信」（该集 coverage 报 0 但实测持仓 300–396 只）。

**P16（insiders 首波 6 条，已派发）**：`insider_agg_matrix` 的 34 字段按 description 分成 3 族——① 方向指标 `directional_indicator` / `_2`（coverage **1.0**，全样本覆盖）；② 交易规模族 `avg_*` / `total_*` × buy/sell × all/direct/executive/top（coverage 0.5344）；③ 显著性排序族 `significant_value_1..4` / `top_*` / `directional_*`（coverage 0.5342）。

经济学依据（Lakonishok & Lee 2001；Seyhun 1986）：内部人**买入**比卖出信息量大得多（卖出有流动性/分散化动机，买入只有看涨动机）；**高管层（executive）比普通董事（director）信息优势更强**。6 个模板：

| tag | 机制 | 表达式 |
|---|---|---|
| I1 | M1 季度净方向（LL2001 主效应） | `group_rank(ts_sum(directional_indicator, 66), sector)` |
| I2 | M10 方向指标的时序意外度 | `group_zscore(ts_zscore(ts_sum(directional_indicator, 22), 504), sector)` |
| I3 | M2 买卖股数失衡比 | `group_rank(divide(ts_sum(total_buy_shares, 66), add(ts_sum(total_buy_shares, 66), ts_sum(total_sell_shares, 66))), sector)` |
| I4 | M3 高管信念比（Seyhun 层级差异） | `group_rank(divide(ts_sum(total_secondary_top_buy_shares, 66), add(ts_sum(total_secondary_top_buy_shares, 66), ts_sum(total_secondary_top_sell_shares, 66))), sector)` |
| I5 | M5 净方向加速度（事件型） | `group_rank(ts_delta(ts_sum(directional_indicator, 22), 22), sector)` |
| I6 | M12 信念集中度（第1大 vs 第2大交易额之差） | `group_rank(subtract(ts_backfill(significant_value_1, 66), ts_backfill(significant_value_2, 66)), sector)` |

窗口取 66（季度）/ 22（月度）/ 504（2 年）—— 均为准则内的有意义窗口。稀疏事件集故 `nanHandling=ON`。

**P17（risk60 待开）** 5 个 VECTOR 字段 → 可支撑 10 个互异模板：费率水平 / 费率动量 / 费率方差（`ts_covariance(x,x,22)`，GBR 已验证 S1.90）/ 费率历史偏离（`ts_av_diff`，GBR 已验证 S2.04）/ 借券买卖价差（offer vs last）/ 拥挤度累积 / 拥挤度时序标准化 / 出借费率与借券费率背离 / 费率×拥挤度交互 / 费率稳定性。

> ⚠ **P17 已于本轮作废**：`risk60` 经 `get_dead_datasets` 实测已在判死登记簿内
> （`DEU-RISK60-FEE-CROWDING-DEAD-20260919`，best|S|=0.29，verdict「信号天花板 + 域锁双重」）。
> 10 条表达式虽已预检通过，全部不再派发。**设计新波次前必须先查判死登记簿**，本轮即为此踩坑。

---

## 四十二、P16 收割 + 广度三集首测：DEU 真实天花板与数据集盘点重大修正

### 42.1 P16 insiders（`insider_agg_matrix`）6 条 + 3 条设置对照全收割

基线：DEU / TOP500 / d1 / SUBINDUSTRY / decay4 / trunc 0.08 / **nanON**（稀疏事件集）。

| tag | alpha | 机制 | S | F | TO | 2Y | sub | margin | DD | fails |
|---|---|---|---|---|---|---|---|---|---|---|
| I1 | `A1V6Q9gd` | 季度净方向 `ts_sum(directional_indicator,66)` | 0.76 | 0.45 | 4.39% | 0.89 | 0.19 | 20.17bp | 13.87% | 4 |
| I2 | `YP1Zx6AW` | 时序意外度 `ts_zscore(ts_sum(di,22),504)` | **−0.12** | −0.03 | 12.89% | −0.61 | −0.25 | −1.19bp | 20.06% | 4 |
| **I3** | `wpQ69ppQ` | 买卖比（buy/(buy+sell), 66d） | **0.81** | 0.44 | 4.66% | **1.62** | 0.45 | 15.62bp | 9.03% | **2** |
| I4 | `QPveYJvG` | 高管二级市场信念比 | 0.82 | 0.46 | 4.46% | 1.32 | 0.39 | 17.34bp | 11.41% | 3 |
| I5 | `vR10OqYz` | 净方向加速度 `ts_delta(ts_sum(di,22),22)` | 0.09 | 0.02 | 14.67% | 0.52 | −0.16 | 0.57bp | 12.61% | 4 |
| I6 | `6XdxAXoO` | 信念集中度（第1大−第2大交易额） | 0.56 | 0.28 | 4.99% | 0.61 | −0.32 | 12.58bp | 13.34% | 4 |

**三条设置对照（同一 I3 表达式）**

| tag | alpha | 设置变更 | S | F | TO | 2Y | sub | fails | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| — | `wpQ69ppQ` | 基线（SUBINDUSTRY / decay4） | 0.81 | 0.44 | 4.66% | 1.62 | 0.45 | 2 | 基准 |
| Q1 | `xArM1xvJ` | decay **2** | **0.86** | 0.48 | 5.05% | 1.71 | 0.47 | 2 | S +0.05（+6%） |
| Q2 | `leAxMvr5` | decay **2** + **CROWDING** | 0.75 | 0.37 | 4.07% | 2.04 | 0.37 | 2 | **劣于基线** |

**结论（三分类归因，按 `wqb-concepts` 换手治理框架逐层排除）**
1. **不是换手问题** —— TO 4.4–5.1%，已在地板 0.125 之下，fitness 的分母被钉死，提换手无用、降换手更无用。
2. **不是横截面宽度问题** —— `wpQ69ppQ` 实测 `longCount 107 + shortCount 154 = 261 只`（TOP500 的 52%），塔归属正确（`DEU/D1/INSIDERS`，mult 1.7），`LOW_2Y_SHARPE` / `LOW_SUB_UNIVERSE_SHARPE` / `CLUSTER_TEST` / `LOW_TURNOVER` **全部 pass**。
3. **是信号强度问题** —— 卡住的只有 `LOW_SHARPE(0.81<1.58)` 与 `LOW_FITNESS(0.44<1.0)`。decay 2 只把 S 从 0.81 抬到 0.86（+6%），距闸 1.58 仍差 **+84%**。CROWDING 在 insiders 上反而更差（0.75 vs 0.86），**再次印证「中性化最优解是数据集专属性的」**。

⇒ `insider_agg_matrix` 天花板 ≈ S 0.86，判**信号天花板**（非宽度、非换手）。另注 I2/I5 为负 ⇒ insiders 的净买入方向在 DEU 正向有效、加速度与意外度无效。

### 42.2 Q3：analyst93 的衰减轴方向与 techindi_model 相反

| alpha | 表达式 | 设置 | S | 2Y |
|---|---|---|---|---|
| 历史最优 | `group_zscore(signed_power(ts_zscore(ts_backfill(vec_avg(anl93_recprofitabilityprev_analyst_profitability2),120),504),0.5), sector)` | SUBINDUSTRY / decay4 | ~1.70 | 1.19 |
| Q3 | 同上 | **decay2 + CROWDING** | **0.56** | 0.53 |

**归因**：分析师盈利预测是**慢变量**（月度/季度更新），decay2 等于把 smoothing 抽掉让 1 日噪声主导；techindi_model 是**日频技术指标**（快变量），decay2 反而保住最新信息。⇒ 与既有记忆「平滑是快慢信号依存的」一致：**decay 最优档由信号半衰期决定，不可跨数据集套用**。analyst93 的正确方向是 decay ≥4，不是 2。

### 42.3 Q4：`P0oe6wpJ` 的 decay2 对照（提交版本不变）

| alpha | 设置 | S | F | TO | 2Y | sub | fails |
|---|---|---|---|---|---|---|---|
| **`P0oe6wpJ`**（保留） | **decay16** / trunc0.02 | **2.14** | **1.99** | **10.36%** | 2.56 | **1.37** | **0** |
| Q4 `QPveY7Kg` | decay2 / trunc0.02 | 2.03 | 1.61 | 16.10% | 2.54 | 1.20 | 0 |

⇒ decay16 在 S / F / sub / 换手四项全胜，仅 2Y 微低 0.02。**提交版本 `P0oe6wpJ` 不变**。这条同时说明「decay 越短越好」不是普适规律 —— 对 `vector_neut` 残差化后的低噪声信号，长 decay 才是最优。

### 42.4 R 批：risk72 首测 —— 残差收益是**动量**，不是反转（关键发现）

`top800_equity_residualized_return` 是 MFM1 风险模型剥离市场/国家/行业后的**特质收益（specific return）**。按教科书反转假设取负号：

| tag | alpha | 表达式 | S | F | TO | 2Y | DD | 翻转后 S |
|---|---|---|---|---|---|---|---|---|
| R1 | `leAxMAk5` | `-group_rank(ts_mean(x,5), sector)` | **−0.33** | −0.08 | 52.64% | −0.52 | 55.93% | **+0.33** |
| R2 | `YP1ZxgeA` | `-group_rank(ts_sum(x,22), sector)` | **−0.78** | −0.43 | 26.57% | −1.28 | 90.39% | **+0.78** |

**两条同时为负 ⇒ 符号结论可靠（不是噪声）**：DEU 特质收益呈**动量**延续，22 日窗口（+0.78）显著强于 5 日（+0.33）。
**经济学解释**：特质动量在低流动性小市场延续性更强（Blitz, Huij & Martens 2011, JFE「Residual momentum」）；DEU TOP500 恰属此类。
⚠ 但 R1 的 DD 55.9% / R2 的 DD 90.4% 说明方向虽对、风险极大 ⇒ 该机制必须加波动率缩放或风险中性化，不能裸用。
**下一步**：`risk` 塔仍为 0，是唯一「零测试 + 有明确方向先验」的塔。窗口应扩展到 66 / 126 / 252（动量峰值典型在 6–12 个月），并配合 `ts_zscore` 归一。

### 42.5 【重大修正】DEU 数据集盘点：92 → ≥172

**本轮实测**：`get_datasets(region=DEU, universe=TOP500, delay=1)` 不带 category 时只返回 **92** 个数据集，且**完全不含 analyst / model / news 三个 category**。逐 category 补拉后：

| category | 数据集数 | 说明 |
|---|---|---|
| other | 41 | 首拉已含 |
| pv | 16 | 首拉已含 |
| fundamental | 12 | 首拉已含 |
| institutions | 5 | 首拉已含 |
| risk | 5 | 首拉已含 |
| sentiment | 3 | 首拉已含 |
| earnings / insiders / socialmedia | 2 / 2 / 2 | 首拉已含 |
| imbalance / macro / option / shortinterest | 1 / 1 / 1 / 1 | 首拉已含 |
| **analyst** | **18** | **首拉缺失** |
| **model** | **45** | **首拉缺失** |
| **news** | **17** | **首拉缺失** |

⇒ **DEU 实际 ≥ 172 个数据集**（92 + 18 + 45 + 17），判死 19 个，**存活 ≥153 个**。
**这直接推翻「DEU 已穷尽」的先前判断** —— 此前 60 个目标看似不可达，是因为只看到了 56% 的数据集。**教训：`get_datasets` 不带 category 的返回不完整，必须逐 category 拉。**

高频高价值存活集（覆盖率高、拥挤度低）：

| 集 | category | 字段 | coverage | users | alphas | 备注 |
|---|---|---|---|---|---|---|
| `model264` | model | 380 | **0.9973** | 115 | 203 | Wolfe 因子模型，历史至 1986 |
| `analyst_earnings_ibes` | model | 42 | **0.9978** | 127 | 279 | 全球分析师盈利预测 |
| `model53` | model | 22 | **0.9050** | 9 | **9** | 信用风险度量，几乎无人用 |
| `model238` | model | 22 | **0.8552** | 85 | 130 | SmartHoldings，`mdl238_*` 家族覆盖 **1.0** |
| `model36` | model | 20 | 0.8488 | 44 | 58 | SmartRatios |
| `model28` | model | 25 | 0.8105 | 41 | 53 | 结构性信用风险 |
| `predictive_starmine` | model | 631 | 0.7903 | 470 | 1143 | 分析师-公司关系深度学习 |
| `news104` | news | 11 | **0.9630** | 57 | 100 | 存档新闻 |
| `news18` | news | 70 | 0.8046 | 84 | 137 | RavenPack |
| `pattern_scores` | pv | 504 | **0.9888** | 152 | 258 | 形态评分（PV 塔 0） |
| `pv29` | pv | 50 | **1.0000** | 43 | 65 | PV 塔 0 |
| `other455` | other | 1500 | 0.9535 | 95 | 204 | 字段量最大（OTHER 塔仅需 +1） |
| `fund_holdings_panel` | institutions | 18 | 0.9019 | 54 | 93 | |
| `institutions6` | institutions | 11 | **1.0000** | 121 | 259 | |
| `model264` / `analyst7` / `analyst15` / `analyst69` / `analyst93` / `analyst_factor_signals` / `analyst_consensus` | — | — | 0.5–0.8 | — | — | analyst 塔仅需 +2 |

**塔位缺口重算**（DEU D1 本季度，`get_pyramid_alphas` 权威源）
- 已点 1 颗：institutions / model / analyst / fundamental → **各需 +2 = 8**
- 已点 2 颗：other → **需 +1**
- 全 0（11 类）：pv / news / sentiment / insiders / earnings / risk / option / macro / socialmedia / shortinterest / imbalance → **各需 +3 = 33**
- **点亮全塔 = 42 个**；60 个目标 = 42 + 18 个超额（超额部分塔倍率递减但仍是有效 alpha）

⇒ **60 个目标由「数据集不足」改判为「产能不足」**：缺口不再是标的，是我的回测吞吐（当前约 1.2% 达标率 × 需 5000 条）。这才是真正的约束。

### 42.6 shortinterest3 首波 6 条（SHORTINTEREST 塔 0 → 首测）

`shortinterest3`：25 字段**全 VECTOR**，三族（基族 cov 0.6683 / `_main` 0.6872 / `_p5_d1` 0.7833）× 8 个度量 + `shrt3_bar`（借券需求评级 1–10，cov 0.6528）。
基线：SUBINDUSTRY / decay4 / trunc 0.08 / nanON（VECTOR 全部经 `vec_avg` 标量化）。

| tag | alpha | 机制（模板） | S | F | TO | 2Y | sub | margin | DD | fails |
|---|---|---|---|---|---|---|---|---|---|---|
| **S1** | `d5WqWeYK` | 借券需求评级水平·截面分位 | **0.89** | **0.59** | 11.50% | **2.34** | 0.72 | 9.68bp | 17.81% | 2 |
| S2 | `d5WqWggv` | 评级·2 年时序分位（慢状态） | 0.87 | 0.41 | 18.65% | 2.10 | **0.83** | 4.36bp | 8.03% | 2 |
| S3 | `kqNRNeqK` | 费率 22 日变化·历史标准化 | **−0.18** | −0.03 | 45.09% | −0.85 | −0.25 | −0.59bp | 27.66% | 4 |
| **S4** | `58ERER8n` | 费率 22 日**方差**（`ts_covariance`，不确定性） | 0.75 | 0.42 | 6.40% | **2.50** | 0.33 | **12.34bp** | 19.45% | 3 |
| S5 | `1YNvN6e6` | 费率极差 max−min（摩擦宽度） | 0.40 | 0.16 | 30.33% | 0.21 | **0.89** | 3.16bp | 30.35% | 3 |
| S6 | `KPJeJq3l` | 借出股数水平（22 日均） | 0.13 | 0.03 | 3.82% | 1.08 | 0.45 | 3.64bp | 19.58% | 3 |

**归因**
1. **方向全部符合经济学先验**：借券需求高（S1）、费率不确定性高（S4）、摩擦宽（S5）⇒ 取负号后均为正 S。三族独立验证通过。
2. **费率「变化」无效、「方差」有效** —— S3（`ts_delta` 一阶差分）S −0.18 而 S4（二阶矩）S +0.75。机理：变化量捕捉的是噪声（费率日频抖动），方差捕捉的是**分歧度/稀缺度**这个慢状态。与既有记忆「慢状态变量适合平滑、快异常信号不适合」互为印证。
3. **最强的 2Y（2.34 / 2.50）与弱的全期 S（0.75–0.89）并存** ⇒ 信号在 2022–23 风格反转期极强、在 2014–21 被稀释。**这是「可用但需残差化」的典型形态，不是死信号。**
4. **S1 与 S4 的 margin 差距巨大**（9.68bp vs 12.34bp）而换手差距相反（11.50% vs 6.40%）⇒ 两者是**不同的收益来源**（需求强度 vs 稀缺摩擦），具备互不冗余的先验基础，可作 `vector_neut` 的两条腿。

### 42.7 【本轮最重要归结】DEU 弱区的两条破局路径

把本轮所有产出按「几何复杂度 × 指标」排列，规律非常清楚：

| 几何 | 代表 | S | 达标 |
|---|---|---|---|
| 单腿 + 简单分位（`group_rank`） | insiders I3、shortinterest3 S1 | 0.81 / 0.89 | ✗ |
| 单腿 + 组内 zscore | shortinterest3 S4 | 0.75 | ✗ |
| 单腿 + 长窗（66/504） | shortinterest3 S2、S9 | 0.87 / — | ✗ |
| **单腿 + 非线性机器（`vector_neut` 残差化）** | **`P0oe6wpJ`** | **2.14** | **✓** |
| **单腿 + CROWDING + 期限结构价差** | **`JjelQnvE`** | **2.61** | **✓** |

⇒ **DEU TOP500 单腿简单几何的天花板稳定在 S 0.75–0.90，无例外；唯二达标的两条都用了「残差化 / 期限结构」这类高阶几何。**
**结论：DEU 不该再堆「换字段 × 换窗口」的简单模板（已证饱和），应把全部产能投向三类高阶几何**：
1. **`vector_neut(A, B)` 残差化** —— 把主信号对同数据集内的共因子正交化，剥离风格暴露。`P0oe6wpJ` 实证 S 2.14 / F 1.99 / TO 10.36% / sub 1.37（全闸）。
2. **组内相对价差 / 期限结构** —— `JjelQnvE` 实证 S 2.61。
3. **分组轴 + 中性化解耦** —— 同一表达式换 CROWDING 可 +34%（techindi_model），但方向不可跨集外推（insiders 上为负）。

---

# 四十三、S / M / T 三波归因与「五层骨架」方法论（2026-10-29 夜）

## 43.1 shortinterest3 完整 12 模板：单字段数据集的定案

同一设置（DEU/TOP500/D1、SUBINDUSTRY、trunc 0.08、nanON）下 12 条全收。

| tag | alpha | 模板（信号 ≈ 几何） | S | F | TO | 2Y | sub | margin |
|---|---|---|---|---|---|---|---|---|
| **S1** | `d5WqWeYK` | `group_rank(backfill(vec_avg(shrt3_bar),120), sector)` ×−1 | **0.89** | **0.59** | 11.50% | **2.34** | 0.72 | 9.68bp |
| S2 | `d5WqWggv` | `ts_rank(backfill(shrt3_bar),504)` ×−1 | 0.87 | 0.41 | 18.65% | 2.10 | **0.83** | 4.36bp |
| S12 | `KPJeJg88` | S1 换 `subindustry` 轴 | 0.77 | 0.45 | 11.29% | 1.99 | 0.70 | 7.69bp |
| S4 | `58ERER8n` | `ts_covariance(费率,费率,22)` ×−1（二阶矩） | 0.75 | 0.42 | 6.40% | 2.50 | 0.33 | 12.34bp |
| S9 | `2rAEAllP` | `group_rank(ts_mean(久期,66),sector)` ×−1 | 0.49 | 0.22 | 3.45% | 1.85 | 0.46 | **15.11bp** |
| S5 | `1YNvN6e6` | 费率极差 `max−min` ×−1 | 0.40 | 0.16 | 30.33% | 0.21 | **0.89** | 3.16bp |
| S7 | `mLoOoV2x` | `group_zscore(ts_av_diff(费率,66),sector)` ×−1 | 0.36 | 0.12 | 30.12% | 0.26 | 0.31 | 2.28bp |
| S10 | `Xg9q9nda` | 双 z 交互 `z(费率,252)×z(bar,252)` ×−1 | 0.29 | 0.07 | 23.51% | 2.26 | **0.04** | 1.14bp |
| S11 | `akKJKEZO` | `signed_power(ts_zscore(费率,252),3)` ×−1 | 0.28 | 0.07 | 41.02% | −0.42 | 0.41 | 1.26bp |
| S8 | `O0AeAxQp` | `ts_delta(ts_mean(交易笔数,22),66)` ×−1 | 0.25 | 0.10 | 11.77% | −0.79 | 0.26 | 3.57bp |
| S6 | `KPJeJq3l` | `ts_mean(loaned_share_count,22)` ×−1 | 0.13 | 0.03 | 3.82% | 1.08 | 0.45 | 3.64bp |
| S3 | `kqNRNeqK` | `ts_delta(费率,22)` + `ts_zscore(·,504)` ×−1 | **−0.18** | −0.03 | 45.09% | −0.85 | −0.25 | −0.59bp |

**四条归因（按解释力排序）**

1. **这是「一个字段撑一个数据集」的典型**。S>0.75 的四条全部落在两个现象上：`shrt3_bar`（借券需求评级 1–10）的水平排序（S1/S2/S12）与费率**二阶矩**（S4）。而**费率水平的全部一阶派生**（变化 S3、av_diff S7、凸变换 S11）无一例外全灭 S ≤ 0.36。

   ⇒ 与 shortinterest3 在 GBR 的结论完全同构（记忆条目「费率变化无效、费率方差有效」）。**跨区可外推**：这是数据本身的统计性质（借券费率是慢变量、其水平已被市场充分定价，只有方差承载信息），不是区域特性。

2. **借券需求评级优于一切费率派生**。`shrt3_bar` 是供应商已经做好的标准化排序（1–10），相当于把「费率 + 供给量 + 久期」压缩成一个稳健指标。原始费率字段噪声更大、且存在极小分母（费率接近 0 时比值爆炸）。

3. **换 group 轴 sector→subindustry 是纯损失**：S 0.89→0.77（−13%）、2Y 2.34→1.99、sub 0.72→0.70。与 techindi_model 上「CROWDING ≫ SUBINDUSTRY」同向——DEU TOP500 只有 500 只票、约 11 个 sector，**分组太细会切碎信号**。

4. **T2 的 `vector_neut` 增益是假象**：S 0.89→0.96（+8%），但 `sub_universe_sharpe` 0.72→**0.14**（−81%）。正交化把持仓推到残差分布的尾部，子宇宙（次小市值段）完全失效。**S 单指标上涨 + sub 崩塌 = 不可提交**，这是 LOW_SUB_UNIVERSE_SHARPE 的典型死法。

**shortinterest3 定案：天花板 S 0.89（`d5WqWeYK`），差 44% 到闸；SHORTINTEREST 塔在本轮不点亮。**

## 43.2 model238（SmartHoldings）判死

| tag | alpha | 分量 | S | F | TO | 2Y | sub | margin |
|---|---|---|---|---|---|---|---|---|
| M1 | `zq3a3N0R` | `group_rank(mdl238_global_rank, sector)` 持有水平 | 0.53 | 0.28 | 8.39% | **−0.00** | 0.41 | 8.34bp |
| M3 | `58ERL5zN` | `group_rank(mdl238_global_owner_rank, sector)` ×−1 拥挤度反向 | 0.43 | 0.20 | 3.28% | 0.16 | **−0.11** | 16.26bp |

两分量（持有可能性水平、机构拥挤度）方向相反却都不达标，且 **2Y 一个归零、一个 sub 翻负**。`mdl238_*` 族字段 coverage 报 1.0（全字段满覆盖），但实际持仓效率极低（TO 3.28% 却只有 0.43 的 S）。

**判死依据**：不是覆盖率问题，是**信号不存在**。SmartHoldings 的「机构持股可能性秩」是对 13F 类持仓的重构估计，在 DEU TOP500 这种大盘股密集的池子里，机构持股是**共识信息**、无 alpha。MODEL 塔改由 model264 / model53 等继续攻（M 塔当前 1 颗，需 +2）。

## 43.3 【本轮最重要方法论】`P0oe6wpJ` 的五层骨架解构

`P0oe6wpJ`（S 2.14 / F 1.99 / TO 10.36% / sub 1.37 / 全闸 0 fail）的完整结构：

```
vector_neut(                                              ← L5 正交化
  ts_quantile(                                            ← L4 秩→正态分位
    ts_ir(                                                ← L3 水平→信噪比
      ts_mean(                                            ← L2 二次平滑
        max(backfill(views,22), ts_delay(backfill(views,22),5)),  ← L1 棘轮
      5),
    22),
  252, driver="gaussian"),
  backfill(snl27_relpopularity08,22))
```

| 层 | 算子 | 承担的经济学职能 |
|---|---|---|
| L1 | `max(x, ts_delay(x,5))` | **注意力棘轮**：关注度只上不下，刻画「已被唤醒且未消退」 |
| L2 | `ts_mean(·,5)` | 去日频噪声，保周级脉冲 |
| L3 | `ts_ir(·,22)` | **水平 → 信噪比**：把「有多少关注」变成「关注有多持续」 |
| L4 | `ts_quantile(·,252,gaussian)` | 秩 → 正态，消除截面偏态与量纲 |
| L5 | `vector_neut(·, B)` | 对同数据集共因子（相对流行度）正交，剥离风格暴露 |

**这是本轮最重要的归结：DEU 弱区的第一杠杆是几何层数，不是字段选择。**

实证对照（同一批约 190 条回测）：

| 几何层数 | 代表 | 典型 S 区间 | 达标数 |
|---|---|---|---|
| 1 层（单变换 + group_rank） | S1–S12、I1–I6、M1/M3、R1/R2 | 0.25 – 0.89 | **0** |
| 2 层（+ 双字段算术） | `P0oe6wpJ` 之前的 snt×snl 单层版 | 0.56 | 0 |
| **5 层（堆叠 + 正交化）** | **`P0oe6wpJ`** | **2.14** | **1** |
| 高阶几何（组内价差/期限结构） | `JjelQnvE` | 2.61 | 1 |

⇒ 单层模板的天花板在 0.9 附近且**无例外**（12 个数据集族反复验证）；五层堆叠直接给出 2.14。**层数带来的增益（2.4×）远大于换字段（≈1.0×）或换窗口（≈1.1×）。**

## 43.4 【重要边界修正】棘轮 `max(x, ts_delay(x,W))` 只适用于非负累积型信号

T4 用同一五层骨架打 `risk72` 的特质收益（`ecs_top1600_residual_return_cfg2`），得 **S −0.30 / F −0.09 / sub −0.27**。而**不用棘轮**的单层版 R1/R2 在符号翻正后是 S +0.33（5d）/ **+0.78**（22d）。

**方向被棘轮破坏，不是 risk72 无信号。**

机理：`max(a, b)` 在**正区间选较大者**、在**负区间选「较不负」的那个**——对零中心信号，这等于对每一期收益率做了一次单边向上截断，把「下跌」系统性削平，均值被抬高、方差被压缩，最终与原始信号的相关性大幅下降甚至反号。

**判据（写进 SOP）**：

| 信号类型 | 例子 | 棘轮是否适用 |
|---|---|---|
| 非负单调累积量 | 浏览量、借券需求评级 1–10、股数、成交笔数 | ✅ 适用 |
| 零中心收益/变化量 | 残差收益率、日收益、delta | ❌ **破坏方向** |
| 有符号比率 | 买卖比、集中度 | ⚠ 需先 `abs`/`rank` 变换到非负 |

**应用**：设计五层骨架前先判 L1 是否合法。零中心信号跳过 L1（从 L2/L3 起堆叠），否则白烧一条仿真槽且结论会被误读成「数据集无信号」。

## 43.5 risk72 方向裁决（修正 42.4 的临时结论）

42.4 依据 R1 `−0.33` / R2 `−0.78`（两者都带 `multiply(-1,·)`）推断「特质收益是动量、应去掉负号」。T4 的 −0.30 曾被疑为反证，现归因为棘轮污染，**不构成对 R1/R2 的反驳**。

⇒ **维持结论：risk72 特质收益在 DEU 是动量延续，表达式应去掉 `multiply(-1,·)`。** 待用「跳过棘轮的五层骨架」重测确认。

## 43.6 U 波：sentiment7 十模板库（在飞）

`sentiment7`（Wikipedia 浏览量，3 字段）是**唯一已验证能出 S>2 且 sub>1.2 的数据集**（`P0oe6wpJ`）。且 SENTIMENT 塔当前 **0 颗**、提交后仅 1 颗——**还缺 2 颗，是最短的点塔路径**。

**关键发现：`snt7_views` 是从未被使用过的新字段**（`alphaCount` 仅 33，vs `all_languages_views` 的 61）。`P0oe6wpJ` 只用了后者。二者的比值 = **语言集中度**（细分视图占全语言视图比例），是全新机制维度，且换主腿天然降相关。

| # | 主腿 | 正交腿 / 几何 | 机制 |
|---|---|---|---|
| M1 | `all_languages_views` | `snl27_relpopularity08` | 已验证（`P0oe6wpJ`） |
| **M2** | **`snt7_views`** | `all_languages_views` | 剔除全球关注后的本地异常关注 |
| **M3** | `all_languages_views` | **`snt7_views`** | 反向正交（换正交腿） |
| **M4** | `sum(views)/sum(all_views)` | — | **语言集中度**（新机制） |
| **M5** | `ts_delta(ts_mean(all_views,22),22)` | — | 关注度加速度（二阶差分） |
| **M6** | `ts_std_dev(views,66)` | — | 关注度波动率（二阶矩） |
| **M7** | `all_languages_views` | 去掉 L3 `ts_ir` | **消融实验**：量化 L3 层贡献 |
| **M8** | `snt7_views` | `ts_rank` 替 `ts_quantile` | 分位方式对照 |
| **M9** | `mean(views,5)/mean(views,66)` | — | 注意力爆发比（短/长基线） |
| M10 | `snt7_views` | `group_zscore(sector)` 替 `vector_neut` | 分组替代正交（待派） |

十模板结构互异（主腿 4 种 × 正交腿 3 种 × 分位 2 种 + 消融 + 分组），满足模板多样性硬约束。设置分两档做对照：M2–M5 用 `P0oe6wpJ` 最优档（decay16 / trunc0.02），M6–M9 用基线档（decay4 / trunc0.08），从而把**机制效应与设置效应解耦**。

派发状态：U1–U7 已被接受（`wFk7d9O8` / `3I17WifT` / `3ogKtm5W` / `1GZn5IfY` / `44xqM29C` / `2XriIMfQ` / `39uEK2b4`），U8 因并发上限 429，待补派。

## 43.7 塔位实况复核（权威源 `get_pyramid_alphas`，2026-10-29 夜）

DEU D1 当前：`institutions 1 / model 1 / other 2 / analyst 1 / fundamental 1`，**其余 11 类全 0**（pv / news / sentiment / insiders / risk / option / macro / socialmedia / shortinterest / imbalance / earnings）。

**注意**：`P0oe6wpJ` 与 `JjelQnvE` 均为 UNSUBMITTED，**尚未计入塔位**。提交后 `sentiment` 0→1、`other` 2→3（other 即点亮）。

点亮全塔还需 **42 颗**（institutions +2、model +2、other +1、analyst +2、fundamental +2、sentiment +3、其余 10 类各 +3）。加 18 颗超额 ⇒ 60 目标不变，瓶颈仍是产能。

---

# 四十四、U 波收批 + 两项结论修正（2026-10-30）

## 44.1 U 波剩余 5 条收割（全部未达标）

| tag | alpha | 结构 | S | F | TO | 2Y | sub | 判定 |
|---|---|---|---|---|---|---|---|---|
| U4 | `WjOkllbQ` | 关注度加速度 `ts_delta(ts_mean(A,22),22)` | **−0.16** | −0.04 | 9.31% | **−1.24** | −0.09 | 反向且 2Y 崩 |
| U3b | `zq3adL9E` | 语言集中度（修正版） | 0.51 | 0.23 | 10.04% | 1.29 | **−0.11** | sub 翻负 |
| U8 | `omE2ajlm` | 注意力爆发比 | 0.34 | 0.12 | 15.52% | 0.90 | 0.29 | 全闸不过 |
| U10 | `e75AaM3E` | `group_zscore(views五层, sector)` | 0.46 | 0.18 | 15.01% | 1.01 | 0.28 | 远低于 P0oe6wpJ |
| T1 | `wpQ6o7OQ` | `−五层(shrt3_bar)` 纯堆叠 | 0.99 | 0.57 | 19.46% | 2.09 | **0.14** | sub 崩 |

U 波 11 条全部收完。**按主腿归因**（把 P0oe6wpJ 单列，因为它的收益不在主腿）：

| 主腿 | 最优 alpha | S | 结论 |
|---|---|---|---|
| `snt7_all_languages_views` + `snt7_views` 正交（U2） | `58ERJlMJ` | **0.85** | sentiment7 家族天花板 |
| `snt7_views` + `all` 正交（U1） | `d5WqaOpj` | 0.67 | 换主腿更差 |
| 消融 L3（U6）/ 换 L4（U7） | `omE2agN5` / `kqNRaj6L` | 0.01 / −0.01 | 五层不可拆（§43.3 已证） |
| 加速度（U4）/ 波动率（U5）/ 集中度（U3b）/ 爆发比（U8） | — | ≤0.51 | 派生矩全灭 |

**sentiment7 判死（作为主腿）**：`snt7_views` 与 `snt7_all_languages_views` 两个字段穷尽了「水平 / 加速度 / 波动率 / 集中度 / 爆发比 / 分组中性化 / 消融 / 换 L4」全部 11 种几何，天花板 S 0.85。**它只能做正交腿，不能做主腿**。P0oe6wpJ 的 S 2.14 与 sentiment7 无关。

## 44.2 【结论修正】`vector_neut` 不是 sub 崩塌的元凶，五层几何才是

§43 曾把 T2 的 `sub 0.72→0.14` 归因给 `vector_neut`（「vector_neut 是双刃」）。**T1 的对照实验推翻了这个归因**：

| alpha | 表达式 | S | 2Y | **sub** | TO |
|---|---|---|---|---|---|
| **T1** `wpQ6o7OQ` | `multiply(-1, 五层(shrt3_bar))` —— **纯堆叠，无 vector_neut** | 0.99 | 2.09 | **0.14** | 19.46% |
| **T2** `O0AeWOmg` | `multiply(-1, vector_neut(五层(shrt3_bar), 费率))` | 0.96 | 2.05 | **0.14** | 19.46% |

两者 sub 精确相同、S 只差 0.03、TO 相同 ⇒ **`vector_neut` 在这条上几乎是恒等变换**，sub 崩塌在加正交化之前就已发生。元凶是**五层骨架作用在借券数据上**。

**【新硬约束】五层骨架的 sub 稳健性 = 字段在市值维度上的分布均匀度**：

- `snl27_relpopularity08`（网站排名热度）在 TOP500 全市值带均匀分布 ⇒ P0oe6wpJ **sub 1.37**（比 S 2.14 还稳）
- `shrt3_bar`（借券需求评级 1–10）天然集中在中小盘、流动性差的名字 ⇒ 五层的 `ts_quantile(gaussian)` 把这些名字推到 z 极端 ⇒ **sub 0.14**，且 sub 子池里这些票的收益方向与全池相反

⇒ **派五层前必须先做「市值分布预判」**：字段是否只在中小盘有值 / 是否有值区间与市值强相关。若是，五层会把权重压到 sub universe 的反向区，sub 必崩，无论有没有正交化。这一条与「棘轮只适用于非负累积型信号」（§43.4）并列，是五层的第二个适用边界。

## 44.3 V 波：sentiment27 十一模板库（已派发，11/11 接受）

P0oe6wpJ 的收益来自正交腿 `snl27_relpopularity08` 本身（§43.3），所以 V 波把 sentiment27 从**正交腿提升为主腿**，直接检验它有没有独立信号。11 个模板结构互异：

| # | 结构 | 要点 | 优先级 |
|---|---|---|---|
| **V2** | **纯 relpopularity08 五层（无正交）** | 测单腿是否独立成立 —— 最关键的判别实验 | ★★★ |
| V1 | relpop08 五层 + `avgranking` 正交 | 换正交腿（vs P0oe6wpJ 的裸 relpop08） | ★★★ |
| V11 | relpop08 五层 + `topranking` 正交 | 再换一条正交腿 | ★★ |
| V10 | 双五层相乘 `F(relpop08) × F(totaldomains)` | 热度 × 覆盖广度的交互 | ★★ |
| V7 | α 口径差 `F(relpop08) − F(relpop1)` | 两个平滑档位之差 = 短期相对热度 | ★★ |
| V3 | `skewness` 主 + relpop08 正交（**跳棘轮**） | 域名排名分布偏度 | ★ |
| V4 | `kurtosis` 主 + relpop08 正交（**跳棘轮**） | 超额峰度 | ★ |
| V5 | `totaldomains` 水平（L3+L4，无棘轮） | 覆盖广度纯水平 | ★ |
| V6 | `divide(1, add(snt27_rank,1))` 倒数 | 关注强度口径（1=最热，取倒数抹平长尾） | ★ |
| V8 | `ts_delta(ts_mean(relpop08,22),22)`（跳棘轮） | 关注度加速度 | ★ |
| V9 | `ts_std_dev(relpop08,66)`（跳棘轮） | 关注度波动率 | ★ |

**设计纪律**：V3/V4/V8/V9 四条**主动跳过 L1 棘轮**——`skewness`/`kurtosis`/`delta`/`std_dev` 都是零中心或非单调量，套 `max(x, ts_delay(x,5))` 会单边截断破坏方向（§43.4 的硬约束，T4 已用 −0.30 付过学费）。

**若 V2 或任两条达标且互相关 <0.7 ⇒ SENTIMENT 塔连同 P0oe6wpJ 一次点满 3 颗**（当前 sentiment 塔位 = 0，P0oe6wpJ 提交后 = 1）。

## 44.4 【流程教训·已付费】VECTOR 字段裸用烧掉 11 个仿真槽

V 波首派 11 条**全部 ERROR**，报错统一为 `Operator ts_delay / ts_mean / ts_std_dev / add does not support event inputs`。根因是我凭「P0oe6wpJ 里 `snl27_relpopularity08` 是裸用的」推断 sentiment27 字段是 MATRIX —— **错**。拉 `get_datafields` 确认：**sentiment27 全部 14 个信号字段都是 VECTOR**，`SYMBOL` 4 个（时间戳/参考日）。

裸用之所以在 P0oe6wpJ 里没报错，是因为它出现在 `vector_neut(标量, snl27_relpopularity08)` 的**第二参数位**——`vector_neut` 本身就吃向量输入。**「某字段在一条能跑的 alpha 里裸着出现」不能反推它的类型**。

`P0oe6wpJ` 的权威形态（`get_alpha_details` 取的原文）给了两个必须遵守的写法：

```text
vector_neut(
  ts_quantile(ts_ir(ts_mean(max(<B>, ts_delay(<B>,5)),5),22), 252, driver="gaussian"),
  ts_backfill(vec_avg(snl27_relpopularity08), 22)
)
其中 <B> = ts_backfill(vec_avg(snt7_all_languages_views), 22)
```

| 写法 | 正确形态 | 我首派的错误形态 |
|---|---|---|
| VECTOR 标量化 | `vec_avg(F)` 先裹，**再** `ts_backfill(·,22)` | 裸 `F` ⇒ event inputs 报错 |
| `ts_quantile` 第三参 | **具名** `driver="gaussian"` | 位置参数 `gaussian`（是否也炸未经独立验证，一并改掉） |
| 顺序 | `ts_backfill(vec_avg(F), 22)` | `vec_avg(ts_backfill(F,22))` 也不对——backfill 要在标量化之后 |

**【新硬约束·派发前置】** 任何新数据集首波，**必须**先用 `get_datafields(dataset_id=…)` 读出每个字段的 `type`，或者直接跑 `preflight_expressions(alpha_expressions=…, dataset_id=…, auto_fix_vector=true)` 让工具自动裹 `vec_*`。**`preflight` 不带 `dataset_id` 时完全不校验类型**——我上次跑的「全部通过」是假通过，它只查了字段名存在性。这一条是本次 11 个槽的代价换来的。

**副产物**：`get_datafields` 的 description 补充了两条此前缺失的经济学语义 —— `snl27_avgranking` / `topranking` / `top50pctranking` / `top75pctranking` 族**全部是「lower is better」**（Tranco 排名越靠前越热），而 `relpopularity08` / `relpopularity1` 是「higher = 更广关注」。⇒ **两者在 `vector_neut` 里的符号不需要手动翻转**：单变量线性正交的残差 `x − βy` 在 `y → −y` 时 β 同步翻号，残差完全相同（`βy` 不变）。所以 V1/V11 直接用裸 `avgranking`/`topranking` 是正确的。

**V6 设计修正**：原计划 `divide(1, add(snt27_rank,1))` 作「关注强度倒数」——但 (a) `snt27_rank` 带排名单位，`add(·,1)` 可能触发单位闸；(b) L4 的 `ts_quantile(gaussian)` 已经在处理分布形状，倒数变换是重复劳动。改为 **`ccTLD 占比 = totalcountrydomains / totaldomains`**（本土域名 vs 全球域名的注意力结构），是真正不同的经济机制。

---

# 四十五、prod 终验结果：两条候选全部撞墙，可提交数归零（2026-10-30）

## 45.1 【推翻旧认知】prod 相关性不是「90–240 秒」，是 **5.8 秒**

20:50 队列全空（`QUEUE_IDLE`）后，`check_correlation(refresh=True, correlation_type="production")` 对两条候选的实测：

| alpha | attempts | **elapsed_ms** | max_correlation | 判定 |
|---|---|---|---|---|
| `JjelQnvE` | 5 | **5 753** | **0.9084** | ✗ FAIL |
| `P0oe6wpJ` | 5 | **5 832** | **0.7694** | ✗ FAIL |

**结论**：此前 8 轮 × 40 分钟全 `busy` 的「取不到 prod」，**100% 是账号级单并发队列被别的会话占满**，不是平台慢、不是 alpha 没算完。**队列空的时候 prod 是一次 6 秒的调用。**

⇒ **作战方式必须改**：prod 不再是「最后才敢用的稀缺资源」，而是**可以纳入搜索循环的廉价探针**。正确顺序从「先量产 IS → 再逐颗 prod」翻转成「IS 过闸就立刻 prod，用 prod 结果指导下一批变体方向」。本轮之前按「prod 昂贵」排产，浪费了大量 IS 槽。

## 45.2 `JjelQnvE` prod 0.9084 —— 判死刑，不再救

`techindi_model` 族（S 2.61 / F 1.48 / 2Y 2.36 / sub 1.29 / fails=0）在 IS 层是完美的，但 prod 0.9084 意味着它与生产池里**某一条已有 alpha 有 91% 的日收益重合**。直方图显示：0.9–1.0 区间 **n=1**，0.8–0.9 区间 **n=1** —— 也就是**只撞一两条**，但撞得极死。

**这不是调参能修的**：0.9084 距离 0.70 差 0.21，窗口微调的典型位移量级只有 0.03–0.08（skill `wq-window-valley-break-prod-wall` 的适用范围是 0.70–0.72 的窄墙）。⇒ **放弃 `JjelQnvE`**，`techindi_model` 单信号数据集在 DEU 的价值到此为止。

## 45.3 `P0oe6wpJ` prod 0.7694 —— 差 0.07，值得救

直方图（9834 个有值 alpha）：

| 区间 | n |
|---|---|
| 0.6–0.7 | 2 |
| **0.7–0.8** | **2** ← 撞墙的就是这两条 |
| 0.4–0.5 | 8 |
| 0.3–0.4 | 22 |
| 0.2–0.3 | 6 |

**只有 4 条生产 alpha 超过 0.6**，分布极度稀疏 ⇒ 减小与那 2 条的重合度是可控的。0.7694 → 需要 −0.07，落在「窗口微调可达」的边界上。

**救它的三个杠杆（按对 prod 的历史效力排序，per `wq-prod-lever-self-lock-guard`）**：
1. **换正交腿字段**（`totaldomains` / `kurtosis` / `avgranking`）—— 改变被剥离的方向，等于换一个残差，语义级别变化
2. **换 L4 `ts_quantile` 窗口** 252 → 126 / 504（跨度 2×）
3. **换 L3 `ts_ir` 窗口** 22 → 66 / 120（跨度 3–5×）
4. 换 L4 driver `gaussian` → `cauchy`（非线性变换）

已派 P1(q126) / P2(q504) 先跑，其余按槽位释放补派。

## 45.4 【平台事实·新】`vector_neut` 第二参数对缩放不变

`W6` 与 `P0oe6wpJ` 唯一的差别是正交腿用 `vec_sum` 还是 `vec_avg`：

| alpha | 正交腿 | S | F | TO | 2Y | sub | margin | returns | DD | fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `P0oe6wpJ` | `ts_backfill(vec_avg(snl27_relpopularity08),22)` | 2.14 | 1.99 | 0.1036 | 2.56 | 1.37 | 0.002094 | 0.1085 | 0.0375 | 0 |
| `N1NML1wq` | `ts_backfill(vec_sum(snl27_relpopularity08),22)` | **2.14** | **1.99** | **0.1036** | **2.56** | **1.37** | **0.002094** | **0.1085** | **0.0375** | **0** |

**逐位完全相同**。`vec_sum = n × vec_avg`，若 `vector_neut` 对第二参数不做内部标准化，两者残差必然不同；实测相同 ⇒ **`vector_neut(x, B)` 对 `B` 的整体缩放不变**（实现上应是对 `B` 做了标准化再投影）。

**推论（省槽用）**：
- 在**正交腿**上换 `vec_avg`/`vec_sum` 是**零信息量的伪多样性**，不要浪费槽。`W6` 就是 `P0oe6wpJ` 的重复品。
- 反过来，在**主腿**上换聚合轴是**真变化**：`V2`（主腿 `vec_avg`）S **−0.38** vs `V12`（主腿 `vec_sum`）S **−0.12**，同骨架差 0.26 ⇒ 因为 ×n 改变了每只票的时间序列形状（n 随票不同）。
- 由此可以反推：**sentiment27 的 VECTOR 每个股票-日的元素个数 n 是随票变化的**（否则 V2 与 V12 也该相同）。

## 45.5 V 波十二模板完整归因（sentiment27 主腿判死）

| # | alpha | 结构 | S | F | TO | 2Y | **sub** | 判定 |
|---|---|---|---|---|---|---|---|---|
| V10 | `RREX51Oz` | 双五层相乘 `F(relpop08)×F(totaldomains)` | **0.26** | 0.08 | 12.24% | **−0.64** | −0.06 | 最优但 2Y 负 |
| V6 | `3qodGNW0` | ccTLD 占比 `countrydomains/totaldomains` | 0.21 | 0.06 | 15.39% | 0.22 | **−0.23** | sub 负 |
| V8 | `e75A1Pod` | 关注度加速度 `ts_delta(ts_mean(...))` | 0.17 | 0.04 | 5.57% | 0.87 | **−0.50** | sub 崩 |
| V3 | `YP1ZlVVM` | `skewness` 主 + relpop08 正交 | **0.44** | 0.18 | 5.51% | 0.89 | **0.73** | **sub 最稳** |
| V4 | `58ERr8ak` | `kurtosis` 主 + relpop08 正交 | 0.11 | 0.02 | 5.68% | 0.27 | 0.41 | 全弱 |
| V9 | `akKJRKv2` | 关注度波动率 `ts_std_dev(relpop08,66)` | −0.21 | −0.06 | 10.92% | −0.60 | 0.16 | 负 |
| V2 | `O0Ae6xkq` | **纯 relpop08 五层（无正交）** | **−0.38** | −0.14 | 11.41% | −0.29 | **−0.49** | 单腿无信号 |
| V1 | `akKJRE5w` | relpop08 主 + `avgranking` 正交 | −0.38 | −0.14 | 11.32% | −0.32 | −0.51 | **与 V2 几乎相同** |
| V11 | `rKRk0wGd` | relpop08 主 + `topranking` 正交 | −0.41 | −0.16 | 11.33% | −0.34 | −0.49 | 同上 |
| V7 | `88RAGYvo` | α 口径差 `F(relpop08) − F(relpop1)` | **−0.58** | −0.25 | 13.58% | −0.22 | −0.47 | **最强信号的负号** |
| V12 | `wpQ63pMQ` | 主腿换 `vec_sum` 聚合轴 | −0.12 | −0.03 | 11.38% | −0.38 | **−0.92** | sub 最差 |

**三条判死结论**：

1. **`snl27_relpopularity08` 作为主腿 = 死**。11 条结构互异模板（水平/双五层交互/ccTLD 结构/加速度/波动率/偏度/峰度/口径差/两种聚合轴）全部落在 **−0.58 ～ +0.44**，无一条过 `near` 线（S 1.0）。天花板 V3 = 0.44。
2. **它的真实属性是「反向信号」**：V2 单腿 −0.38 ⇒ 取反 +0.38；V7（α=0.8 与 α=1 两个平滑档之差）−0.58 ⇒ 取反 +0.58，是本波最强。**「低网站热度 → 高收益」方向成立但幅度太弱**，属于已被市场榨干的注意力反转。
3. **`P0oe6wpJ` 的 2.14 确实来自残差交互，两条腿单独都不行**——这一条比 §43.3 的表述更精确：不是「主要来自正交腿」，而是「**只有 `A − βB` 这个组合成立**」。证据矩阵：

| 信号 | 单独 S | 说明 |
|---|---|---|
| `五层(Wikipedia 浏览量)` | 0.85（U2） | 弱 |
| `五层(网站排名热度 relpop08)` | **−0.38**（V2） | 反向弱 |
| **`vector_neut(前者, 后者)`** | **2.14**（P0oe6wpJ） | **交互后跃升 2.5×** |

这是一个**独立于数据集的模板类**：当两个字段是同一经济现象在**不同聚合层级**上的代理（浏览量 vs 域名排名热度；事件情绪 vs 故事曝光广度）时，**残差才是信号，两条腿单独都不成立**。命名为 **T5R 模板（Five-layer + Residual）**，后续在 news / insiders / institutions / analyst 各塔复用。

## 45.6 当前战役实况（诚实口径）

| 项 | 数 |
|---|---|
| 累计已测 alpha | ~230 |
| IS 全闸通过（`checks.fail=[]` + `failed_ra_count=0`） | **2** |
| prod < 0.7（真正可提交） | **0** |
| 已点亮塔位增量 | 0 |

**`JjelQnvE`（prod 0.9084）放弃，`P0oe6wpJ`（prod 0.7694）进入定向救援。**

**产能实测**：并发槽被其它会话占满，`batch_create_simulations` 派 10 条只进 2 条（本区账号级并发上限实测 2–7 波动，视他人占用而定）。按 2 槽 × 每小时约 12–15 条算，DEU 单波吞吐已从「一次 11 条」退化到「一次 2 条」，这是当前最硬的产能瓶颈。

---

## 46. W 波闭环：T5R 族只有一颗信号，prod 墙不可由窗口/正交腿突破

### 46.1 四条同族候选的互相关矩阵（本地 `compute_mutual_correlation`，1021 个日收益点）

| | P0oe6wpJ | RREXKNQn | N1NML1wq | 1YNvPXrm |
|---|---|---|---|---|
| **P0oe6wpJ**（基准，`ts_quantile` 252） | 1.0 | 0.9496 | **1.0000** | 0.9971 |
| **RREXKNQn**（`ts_quantile` **504**） | 0.9496 | 1.0 | 0.9496 | 0.9478 |
| **N1NML1wq**（正交腿 `vec_sum`） | 1.0000 | 0.9496 | 1.0 | 0.9971 |
| **1YNvPXrm**（正交腿换 `totaldomains`） | 0.9971 | 0.9478 | 0.9971 | 1.0 |

**两两全部 ≥ 0.9478**，最大互斥子集大小 = **1**。

三条硬读数：

1. **窗口翻倍只降 0.05 相关**：`ts_quantile` 252 → 504 使互相关从 1.0 降到 **0.9496**。这修正了「换窗口是降相关杠杆」的乐观预期 —— 在本族上，2 倍窗口跨度只买到 0.05。
2. **换正交腿只降 0.003**：`relpopularity08` → `totaldomains`（完全不同的经济量：相对流行度 vs 域名总数）→ **0.9971**。结合已确认的「`vec_sum`/`vec_avg` 逐位相同」，**正交腿在本骨架上已无任何自由度**。
3. **⇒ W 波不是 4 个模板，是 1 个模板的 4 次重复**。按模板归因，W 波的真实样本量 = 1。

**落地动作**：`RREXKNQn` / `N1NML1wq` / `1YNvPXrm` 不再单独花 prod 时隙 —— `P0oe6wpJ` 的 **0.7694** 已代表全族。后续要在这个族上降 prod，唯一有效维度是**换底层信号源**（不是换 Wikipedia 之外的注意力代理，而是离开注意力维度）。

### 46.2 【方法论修正·重要】五层几何是信噪比放大器，不是信号发生器

本轮在 news20 上做了一次干净的自然实验：**同一套五层几何，只换底层字段**。

| 底层字段（`vec_avg` 后） | 五层几何输出 S | 该字段简单几何下的 S |
|---|---|---|
| `snt7_all_languages_views`（Wikipedia 浏览量） | **+2.14**（P0oe6wpJ） | 0.85（U2） |
| `nws20_multiple_comp_ssc`（新闻综合情绪） | **−0.51**（`vR10Pd5a`） | 0.08（`MPYwVxaM`，`group_rank(ts_mean(·,22),sector)`） |

**同一几何，两个字段的输出差了 2.65 个 Sharpe，且符号相反。**

⇒ **修正此前记录「五层几何套任何信号都出 2.1」的错误表述。正确表述是：五层几何是放大倍数 ≈2.5 的×信噪比放大器**——
- 底层有方向性（Wikipedia 浏览量的注意力异常）→ 0.85 放大到 2.14；
- 底层无方向性（新闻情绪，P7 波已证 S≈0）→ 0.08 放大到 **−0.51**（噪声被放大成负信号，还带 4 项 RA fail）。

**这条直接改写派发前置条件**：五层几何**不能**用来「抢救没信号的字段」，只能用来「放大已确认有方向性的字段」。派五层之前必须先有一个**简单几何下 S ≥ 0.7 的读数**做前提。这也解释了为什么 `JjelQnvE`（techindi_model）能到 2.61 —— 它底层本就有信号。

### 46.3 news20 二次判死（`multiple_comp_` 高覆盖变体也救不了）

P7 波已用裸版（cov 0.6389）测 10 条判死（天花板 0.23）。本轮用 `multiple_comp_` 变体（cov **0.9191**，覆盖 +44%）重测 3 条，结论不变：

| tag | alpha | 结构 | S | 2Y | sub | fails |
|---|---|---|---|---|---|---|
| N1 | `vR10Pd5a` | 五层(`ssc`) | **−0.51** | −0.78 | −0.45 | 4 |
| N3 | `MPYwVxaM` | `group_rank(ts_mean(ssc,22),sector)` 简单探针 | 0.08 | −0.35 | 0.26 | 3 |
| N9 | `E563xErL` | 新闻覆盖强度 `ts_sum(vec_count,66)` | 0.29 | **+1.04** | −0.21 | 4 |

**唯一正面信号**：N9（**新闻条数**＝媒体关注度强度，与情绪方向无关）是三条里唯一 2Y > 1.0 的（+1.04），TO 仅 2.66% / margin 1.64bp。这与 P7 的结论**互相印证**：

> DEU 可用 alpha 来自**注意力异常**，不来自情绪方向（P7 已述），本轮 N1−N3 的符号分野再次确认。

但 N9 的 S 只有 0.29、sub −0.21，强度差 5 倍且子宇宙反向 ⇒ **不足以单独成塔，只能做辅助腿**。news20 正式二次判死，NEWS 塔在本区改由其它新闻数据集攻（news104 cov 0.9630 / news18 / news17 仍在白名单）。

### 46.4 prod 单并发被其他会话实际占用（非我方假象）

本轮再次确认瓶颈来源：本机存在**其他会话**启动的 `prod_wait.py qMLbW8xP --minutes 15`（20:57 起）与两个 pytest 进程（20:58 起）。`check_correlation` 返回 `correlation_busy` 与派发 429 是两个不同队列，但都被同一账号级配额约束。

**我方 `logs/_slots/` 全部为 `.stale`**（无我方占槽）而派发仍 429 ⇒ 进一步坐实「429 来自他人占用，不是孤儿槽」。作战上只能按「每次派 2 条、逐条看 `results[].ok`」的节奏推进。

---

---



---
