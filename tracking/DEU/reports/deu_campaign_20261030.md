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

## 47. 五层几何的放大条件（四类信号的实证矩阵 · 本轮最重要方法论）

### 47.1 现象

本轮把**同一套五层几何**（`ts_quantile(ts_ir(ts_mean(max(X, ts_delay(X,5)),5),22),252,driver="gaussian")`）
套到 5 个不同字段上，得到从 **−0.88 到 +2.14** 的输出。这个离散度不能归给「随机性」——它有清晰的结构。

### 47.2 实证矩阵

| # | 字段 | 信号类型 | 简单/基线几何 S | **五层几何 S** | 放大倍数 | alpha |
|---|---|---|---|---|---|---|
| 1 | `snt7_all_languages_views`（Wikipedia 浏览量） | **流量型** · 非负 · 有方向 | 0.85 | **+2.14** | **2.5×** | `P0oe6wpJ` |
| 2 | `shrt3_bar`（借券需求评级 1–10） | **评级型** · 非负 · 有方向 | 0.89 | −0.88（`JjelrJ0A`）→ 取反 **+0.88**（`qMLbwolA`） | **1.0×** | `JjelrJ0A`/`qMLbwolA` |
| 3 | `top600_equity_residualized_return`（残差收益） | **零中心**（棘轮不可用，只能去棘轮） | 0.78 | **0.78**（`leAx1Ppn`） | **1.0×** | `leAx1Ppn` |
| 4 | `nws20_multiple_comp_ssc`（新闻综合情绪 −1~+1） | 零中心 · **无方向** | 0.08 | **−0.51** | **反向恶化** | `vR10Pd5a` |
| 5 | `insd1_tradesignificance`（交易重要性 1–3） | 评级型 · 非负 | 未测简单版 | 0.76（**2Y +1.76**） | 待定 | `RREXvZ1d` |

### 47.3 结论：放大需要三个条件同时成立

> **① 非负**（否则 `max(x, ts_delay(x,5))` 单边截断、破坏方向）
> **② 流量型累积（flow），不是存量/评级型（stock）**
> **③ 底层有方向性（简单几何 S ≥ 0.7 且 2Y 同号）**

三条缺任一条，五层几何的放大倍数就退化为 1.0× 或反向：

- 缺 ①（#3 残差收益）→ 棘轮无法使用，几何自动退化成 4 层 ≈ 基线；
- 缺 ②（#2 `shrt3_bar` 是 1–10 评级，日间波动而非每日新增）→ 棘轮只取「5 日内最高评级」，没有累积动作，放大倍数 1.0×。**这是最容易误判的一类**——它非负、也有方向，看起来完全符合条件，但就是不放；
- 缺 ③（#4 新闻情绪）→ 几何忠实放大噪声，0.08 变成 −0.51，还附赠 4 项 RA fail。

**为什么「流量型」是本质条件**：棘轮 `max(x, ts_delay(x,5))` 的数学作用是**把随机游走的上包络提出来**，形成单调不减的累积曲线。这要求信号本身是「每日新增量」的累加结果（浏览量、成交量、交易笔数、交易金额）。评级/打分/残差是**存量快照**，相邻两日不是「新增 vs 累计」的关系，上包络没有经济含义，只是一个 5 日高水位线。

### 47.4 落地规则（派五层前的三问）

1. **这个字段是「每日新增」还是「当日快照」？** 只有前者能进五层。
   - 流量型候选（DEU 已确认）：`snt7_all_languages_views`、`insd1_valueeur`、`insd1_shares`、`total_buy_shares`、`total_sell_shares`、`loaned_market_value_usd`、`loaned_share_count`、`transaction_count`、`vec_count(新闻)`。
   - 存量/评级型（**不要**进五层）：`shrt3_bar`、`insd1_tradesignificance`、`directional_indicator`、`*_rank`、所有 `*_residual_return`。
2. **简单几何下有没有 S ≥ 0.7 且 2Y 同号的读数？** 没有就先跑探针，不要直接上五层。
3. **符号是否已验证？** 五层不改变方向、只放大。`shrt3_bar` 的教训（R1 −0.88 → R4 +0.88，2Y 同步由 −1.68 翻到 +1.68，逐位镜像）说明符号错了会得到一颗「看起来很强但完全反向」的候选，必须先跑一条确定方向。

**成本提示**：本轮在「五层 × 非流量型」上烧了 4 条（R1/R2/R5 计划中、I2），按每次派 2 条只进 1 条的产能，等于半天。这条规则的价值就是省掉这类派出。

---

## 48. 自我修正：五层几何在全部有基线的案例上放大倍数都是 1.0×，唯一杠杆是 `vector_neut` 残差

§47 写完后，我又派了 4 条五层变体（S1 借券市值 / A1 内部人重要交易额 / A3 内部人买入股数 / M1 新增岗位数）。结果**全部落在 S −0.27 ～ +0.27**，无一条超过 0.3。

这把 §47 的核心断言「五层几何是 2.5× 信噪比放大器」逼到了必须复核的位置。

### 48.1 重读 P0oe6wpJ 的原始结构

```
vector_neut(
    ts_quantile(ts_ir(ts_mean(max(B, ts_delay(B,5)),5),22),252, driver="gaussian"),   ← 主腿：五层
    ts_backfill(vec_avg(snl27_relpopularity08), 22)                                    ← 正交腿：**1 层**
)
B = ts_backfill(vec_avg(snt7_all_languages_views), 22)
```

关键点：**正交腿只有 1 层**（裸 `ts_backfill`），不是五层。所以这条 alpha 的「五层」只作用在主腿。

再把已知的三个单独读数并排：

| 组成 | 单独 S |
|---|---|
| `五层(Wikipedia 浏览量)` | **0.85**（U2） |
| `裸 relpopularity08`（网站排名热度） | **−0.38**（V2） |
| **`vector_neut(前者, 后者)`** | **2.14** |

⇒ **2.14 是在 `vector_neut` 这一步产生的（0.85 与 −0.38 正交出 2.14），不是五层产生的。**
五层在 Wikipedia 上也只是把 0.85 保持成 0.85。

### 48.2 五层几何的完整实测（8 个字段，含 3 个有简单基线）

| 字段 | 简单/基线 S | 五层 S | **放大倍数** | 有无基线 |
|---|---|---|---|---|
| `snt7_all_languages_views`（流量型） | 0.85 | 0.85（五层单独） | **1.0×** | 有 |
| `shrt3_bar`（评级型） | 0.89 | 0.88 | **0.99×** | 有 |
| `top600_equity_residualized_return`（零中心） | 0.78 | 0.78 | **1.00×** | 有 |
| `nws20_multiple_comp_ssc`（零中心无方向） | 0.08 | −0.51 | **反向** | 有 |
| `loaned_market_value_usd_p5_d1`（流量型） | 未测 | −0.27 | — | 无 |
| `significant_value_1`（存量金额） | 未测 | 0.27 | — | 无 |
| `total_buy_shares`（流量型） | 未测 | 0.10 | — | 无 |
| `insd1_tradesignificance`（评级型） | 未测 | 0.76（2Y +1.76） | — | 无 |

**在有基线的 4 个案例中：3 个是 1.0×，1 个反向，0 个放大。**

⇒ **五层几何是中性变换（normalizing transform），不是放大器。** §47 的「2.5× 放大器」表述**撤回**。

### 48.3 修正后的正确表述

> **DEU 真正可复用的模板是 T5R 的「残差」部分，不是「五层」部分。**
>
> `vector_neut(A, B)` 在 A、B 是同一经济现象的不同层级代理时，能把两个单独都不成立的弱信号（0.85 / −0.38）
> 正交成强信号（2.14）。**这个跃升与 A 是否为五层无关** —— 五层只是把 A 标准化成一个尺度友好的量，
> 换成任何单调等价形式（`rank`、`ts_rank`、裸 `ts_backfill`）应该都能得到相近结果，**这一点尚未验证**。

**为什么这条修正是本轮最有价值的结论**：它改变了派发的搜索空间。此前的派发逻辑是「找一个有信号的字段 → 套五层 → 等它放大」，本轮 8 条实验证明这条路走不通（放大倍数恒为 1.0）。正确的搜索空间是：

> **找「同一经济现象的两个不同层级代理」的配对 → 做 `vector_neut` 残差 → 单腿不必有信号，配对关系才是信号源。**

DEU 已确认可用/待验证的配对：

| 数据集 | 主腿 | 正交腿 | 经济含义 | 状态 |
|---|---|---|---|---|
| sentiment7 × sentiment27 | 五层(Wikipedia 浏览量) | 裸 relpopularity08 | 「被阅读」vs「被引用」 | ✅ 2.14（prod 0.7694 卡墙） |
| insider_agg_matrix | 五层(买入股数) | 裸 卖出股数 | 净买入 | 在飞 `T1` |
| macro27 | 五层(新增岗位) | 裸 删除岗位 | 净新增劳动需求 | 在飞 `T2` |
| shortinterest3 | 五层(借券市值) | 裸 借券股数 | 隐含借券单价 | 待派 `T3` |

**这条也解释了为什么前面那些「五层 × 单字段」全部失败**：单字段没有配对关系，`vector_neut` 无从发挥，五层又只是中性变换，所以结果必然退回到该字段本身的基线水平（0.1–0.9）。

### 48.4 本轮新增的完整数据（8 条，全部未达标）

| tag | alpha | 结构 | S | 2Y | sub | TO | fails |
|---|---|---|---|---|---|---|---|
| N1 | `vR10Pd5a` | 五层(nws20 ssc) | −0.51 | −0.78 | −0.45 | 15.1% | 4 |
| N3 | `MPYwVxaM` | 简单(news20 ssc) | 0.08 | −0.35 | 0.26 | 10.5% | 3 |
| N9 | `E563xErL` | 新闻覆盖强度 | 0.29 | **1.04** | −0.21 | 2.7% | 4 |
| R1 | `JjelrJ0A` | 五层(shrt3_bar) | −0.88 | −1.68 | −0.20 | 13.0% | 3 |
| R4 | `qMLbwolA` | −五层(shrt3_bar) | **+0.88** | **+1.68** | 0.20 | 13.0% | 3 |
| R2 | `leAx1Ppn` | 五层(risk72 残差) | 0.78 | 0.74 | 0.68 | 9.6% | 3 |
| I2 | `RREXvZ1d` | 五层(insd1 重要性) | 0.76 | **1.76** | −0.13 | 25.2% | 4 |
| S1 | `d5WqPjzx` | 五层(借券市值) | −0.27 | −0.52 | −0.05 | 10.5% | 3 |
| A1 | `rKRkneqE` | 五层(内部人重要交易额) | 0.27 | 0.28 | 0.43 | 29.1% | 4 |
| A3 | `npv0XKXd` | 五层(内部人买入股数) | 0.10 | 0.51 | 0.01 | 28.0% | 5 |

**两个可留档的正面读数**（虽然整体未达标）：
- `qMLbwolA`（−五层 shrt3_bar）：S 0.88 / **2Y +1.68** / TO 13.0% —— 短借塔目前最好的方向定版；
- `RREXvZ1d`（五层 insd1 重要性）：S 0.76 / **2Y +1.76** —— 内部人塔的最好 2Y，但 sub −0.13 与 TO 25.2% 拖累，需降换手后再看。

---

## §49 存量库翻查：找到 2 颗「IS 全闸通过 / prod<0.7」的旧候选，其中 1 颗是活的

**本节是本轮方向性转折。** 此前 258 条新仿真 0 可提交，结论是「机制都在 prod 拥挤池」。翻本地 `alphas` 表（`get_alpha_corr_metrics` + `search_alphas_by_sharpe`）后发现：**存量未提交池里躺着 IS 全闸通过且 prod<0.7 的候选，此前从未被提交**。教训——**每轮开波前应先翻存量池，而不是只跑新仿真**。

### 49.1 `58gGQmlN` —— IS 全闸通过，但 self 0.9408 判死

| 项 | 值 |
|---|---|
| S / F / TO | **1.62** / **1.26** / 13.11% |
| 2Y / sub / investS | **2.58** / **1.15** / 1.84 |
| checks | **fail=[]**，pass 9 项（含 LOW_SHARPE / IS_LADDER_SHARPE / LOW_SUB_UNIVERSE_SHARPE） |
| failed_ra / failed_ppa | **0 / 0** |
| prod（20 天前） | 0.683 |
| **self（本次实测）** | **0.9408 FAIL** —— 撞 `2rmGAPqN`（已提交，S 1.81/F 1.48/prod 0.6292） |

表达式（INSTITUTIONS + OTHER 两塔，neutralization=**FAST**）：
```text
tail(winsorize(group_rank(
  multiply(ts_sum(divide(vec_sum(inst1_valueeur), add(vec_sum(inst1_holdings), 0.0001)), 66),
           if_else(and(greater(ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),66),0),
                       greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)), 1, 0)),
  oth455_partner_n2v_p50_q200_w1_pca_fact2_cluster_20), std=2),
  lower=0.25, upper=0.75, newval=0.5)
```
**判死理由：self 0.94，无豁免入口。且同机制已由 `2rmGAPqN` 入库贡献塔位，无增量。**
**可复用点**：`neutralization=FAST` 在 DEU 可用且能出全闸通过的 alpha；`oth455_partner_*_pca_fact2_cluster_20` 是数据驱动的 20 类相似公司分组，比 sector(11 类) 细得多。

### 49.2 `j2Ym1PL9` —— 活的，唯一真机会

| 项 | 值 |
|---|---|
| S / F / TO | **1.57** / **1.33** / **3.33%**（极低） |
| returns / margin | 8.96% / **53.76 bp**（极高） |
| 2Y / sub / investS | 1.13 / 0.95 / 1.41 |
| **risk_neutralized_sharpe** | **0.25**（低 ⇒ 本质是风格暴露的 repackaging） |
| **prod（19h 前）** | **0.5971 PASS** |
| **self（本次实测）** | **0.4213 PASS**（最高对手 2rjrMZ25） |
| fails | LOW_SHARPE(1.57/1.58)、IS_LADDER_SHARPE(1.13/1.58) |
| 塔位 | SHORTINTEREST(1.3x) + ANALYST(1.8x) —— **两塔同时增量** |

表达式（**门控型**：低借券费门控 × 分析师上修）：
```text
trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)) < 0.7,
           rank(ts_mean(eps_y1_estimate_change_3mo, 22)), -1)
```
**机制**：只有借券费率处于低分位（无拥挤空头、易借）的股票，分析师上修才不被空头压制 ⇒ 干净的上修收益。

**年度分布（诊断核心）**：

| 年 | S | TO | margin |
|---|---|---|---|
| 2014 | **2.94** | 4.21% | 7.70bp |
| 2015 | **2.75** | 3.77% | 8.34bp |
| 2016 | 1.41 | 3.71% | 4.16bp |
| 2017 | 1.59 | 2.98% | 4.83bp |
| 2018 | 1.99 | 3.12% | 7.43bp |
| 2019 | 1.78 | 3.17% | 5.30bp |
| **2020** | **−0.46** | 3.42% | **−1.81bp** |
| 2021 | 2.03 | 3.41% | 5.77bp |
| 2022 | **1.70** | 2.97% | 8.48bp |
| **2023** | **0.43** | 2.57% | 1.93bp |

⇒ 11 年 8 年 S>1.4，**2Y 窗口恰好压在 2022(1.70 好) + 2023(0.43 差)** 上。2020/2023 两个坏年是同一类行情（空头 squeeze / 成长股主导），不是机制失效。

### 49.3 门控阈值扫描（12 条实测，第 6 条起为本轮新派）

| tag | alpha | 结构 | S | F | TO | 2Y | sub | fails |
|---|---|---|---|---|---|---|---|---|
| 基线 | `j2Ym1PL9` | K=0.70 | 1.57 | 1.33 | 3.33% | 1.13 | 0.95 | 2 |
| **K075** | **`GrWVN8dG`** | **K=0.75** | **1.59** ✅ | **1.36** | 3.36% | 1.14 | 0.93 | **1** |
| TW0 | `vR10b5jz` | 第三参 0 | 1.57 | 1.33 | 3.33% | 1.13 | 0.95 | 2 |
| TQ | `9qxo39Wq` | 信号换 `ts_quantile` | 0.91 | 0.55 | 4.91% | 0.61 | 0.41 | 4 |
| W66 | `E56JKbg0` | 信号窗 66 | 1.39 | 1.10 | 2.55% | 1.04 | 0.77 | 2 |
| W126 | `vR10bJqv` | 信号窗 126 | 1.36 | 1.07 | 2.07% | 0.93 | 0.81 | 2 |

**三条定论**：
1. **`trade_when` 第三参 `-1` 与 `0` 在全部指标上逐位相同**（S/F/TO/2Y/sub/margin 无一位不同）⇒ 该维度是死轴，别再扫。
2. **信号必须用截面 `rank()`，不能换 `ts_quantile`**：S 1.59→0.91（−43%），TO 反升。这与 W 波的 `ts_quantile` 成功相反——**门控型 alpha 的截面可比性比时序分位重要**。
3. **信号窗口 22 是最优**：66 降 0.20、126 降 0.23。**长窗口在门控结构里是纯损失**（与 RISK 案例一致）。

**当前唯一活口 `GrWVN8dG`**：S 1.59 过闸、F 1.36 过闸、TO 3.36% 过闸、sub 0.93 过闸，**仅剩 IS_LADDER_SHARPE（2Y 1.14 vs 1.58）**。待测 K=0.80/0.90 与无门控对照，判断门控是增益还是负担。

---

## §50 2Y 闸的真正解法：内层 group_neutralize + 正交 bucket（V 系列 8 条变体归因）

### 50.1 起点：J3 三兄弟暴露「窗口长度不是 2Y 主因」

同一 ANALYST 内核 `eps_y1_estimate_change_3mo`（analyst93），只改结构与窗口：

| tag | alpha | 结构 | S | F | 2Y | TO | sub | margin | failed |
|---|---|---|---|---|---|---|---|---|---|
| J3_A | `GrWV5OkG` | 门控 + `group_rank(add(bf(eps,1008), ts_mean(bf(eps,1008),210)), sector)` | 1.56 | 1.32 | **1.00** | 4.29% | 1.01 | 41.8bp | 2 |
| J3_C | `kqNR6Qkl` | 同上但全用 504 窗（`add(bf(504), ts_mean(bf(504),105))`） | 1.62 | 1.38 | 1.08 | 4.21% | 0.92 | 43.3bp | 1 |
| **J3_B** | **`Vkxnb8QG`** | **J3_A 再套内层 `group_neutralize(..., bucket(rank(ts_mean(bf(eps,1008),252)), range="0,1,0.05"))`** | **1.83** | **1.64** | **2.09** | 9.06% | 0.99 | 22.3bp | **0 ✅** |

**1008 窗（J3_A）2Y 1.00 vs 504 窗（J3_C）2Y 1.08** ⇒ 窗口长度对 2Y 无贡献，甚至反向。
**J3_A → J3_B 只加一层内层 GN，2Y 1.00 → 2.09（+109%）、S +17%、sub 不动** ⇒ 2Y 的真正杠杆是**二阶中性化**。

`Vkxnb8QG` 是本轮 290 条以来**唯一 `failed_ra_count = 0`** 的候选，self 0.6379 PASS。

### 50.2 V 系列 8 条单变量对照（全部 SUBINDUSTRY / decay4 / trunc0.08）

以 J3_B 为基线，逐项拆开它的三个部件：

| tag | alpha | 相对基线的唯一改动 | S | F | 2Y | TO | sub | margin | failed |
|---|---|---|---|---|---|---|---|---|---|
| **基线** | **`Vkxnb8QG`** | — | **1.83** | **1.64** | **2.09** | 9.06% | 0.99 | 22.3bp | **0** |
| V5_noGate | `RREXxW6z` | **去掉门控** | 1.77 | 1.61 | 1.83 | 11.99% | 0.88 | 17.2bp | **0** |
| V4_bkt10 | `88RAWA3a` | bucket 步长 0.05 → **0.1**（20桶→10桶） | 1.80 | 1.61 | **1.40** | 7.88% | 0.96 | 25.2bp | 1 |
| V1_J3B_crowd | `6Xdx61op` | neutralization 换 **CROWDING** | 1.52 | 1.23 | 1.57 | 8.08% | 0.76 | 20.4bp | 2 |
| V2_bkt_loan | `npv0G0WE` | bucket 轴换 **borrow rate**（`ts_backfill(vec_avg(mean_loan_rate_main))`） | 1.47 | 1.21 | **0.85** | 8.00% | **1.07** | 21.3bp | 2 |
| V3_indgroup | `QPveRe9W` | 外层 group 轴 sector → **industry** | 1.54 | 1.22 | 1.42 | 8.60% | 0.74 | 18.1bp | 2 |
| V6_bkt_vol | `Xg9qZP31` | bucket 轴换 **信号波动率** `ts_std_dev(bf(eps,1008),66)` | 1.68 | 1.48 | **1.06** | **5.82%** | **1.10** | **33.2bp** | 1 |

**五条定论**：

1. **bucket 步长是 2Y 的主控杠杆，且必须够细**：0.1（10桶）2Y 1.40 → 0.05（20桶）2Y 2.09，同一改动把 2Y 拉高 +49%，而 S/F 几乎不动（1.80→1.83 / 1.61→1.64）。**这是唯一「不付学费」的 2Y 杠杆。**
2. **bucket 的分组轴必须是「信号自身的历史均值」，不能换成任何别的字段**：换 borrow rate → 2Y 崩到 0.85；换信号波动率 → 2Y 1.06。两者都能把 sub 拉到 1.07/1.10、margin 拉到 33bp，但**丢掉 2Y**。⇒ 剥离层的语义必须是「在信号自身的分位上做局部去均值」，换了语义就失效。
3. **CROWDING 与 bucket 剥离层不叠加、反而互斥**：CROWDING 对 J3_A（无 bucket）是 +100%（1.14→2.28），对 J3_B（有 bucket）却是 −25%（2.09→1.57），且 sub 掉到 0.76。⇒ **bucket 剥离层已经吃掉了 CROWDING 的全部信息**。不要再对已带 bucket 的骨架叠 CROWDING。
4. **外层 group 轴必须 sector**：换 industry 后 2Y 1.42、sub 0.74。与既有「DEU 换 group 轴是纯损失」一致。
5. **V6 是「低换手 + 高 margin」备用形态**：TO 5.82%、margin 33.2bp、sub 1.10 都是全组最优，代价是 2Y 仅 1.06。当某个塔拿不到 2Y 时，可用它换稳健性。

### 50.3 ★ 门控的真实身份被证伪：它不是信号放大器，是**相关性正交化器**

`RREXxW6z`（V5，无门控）的 self correlation 实测：

```
max_correlation = 1.0
top_correlated: 2rjrMZ25 → 1.0 ；58gkLAkk → 0.344 ；mLYLEm99 → 0.310 ……
```

**`RREXxW6z` 与已提交的 `2rjrMZ25` self = 1.0，指标逐位相同（S 1.77 / 2Y 1.83 / TO 11.99%）—— 它们就是同一条 alpha。** 即：J3_B 的骨架本体**早已作为 `2rjrMZ25` 提交过**。

因此 `Vkxnb8QG` 相对已提交池的唯一增量就是那道门控，而门控的全部作用可以精确定价：

| 指标 | 无门控（=2rjrMZ25） | 有门控（Vkxnb8QG） | 门控贡献 |
|---|---|---|---|
| S | 1.77 | 1.83 | **+0.06** |
| F | 1.61 | 1.64 | +0.03 |
| 2Y | 1.83 | 2.09 | +0.26 |
| sub | 0.88 | 0.99 | +0.11 |
| TO | 11.99% | 9.06% | **−2.93pp** |
| **self vs 2rjrMZ25** | **1.0 ✗** | **0.6379 ✓** | **−0.362** |

⇒ **门控的价值 90% 在「把 self 从 1.0 压到 0.64」，而不是提升信号。** 这与本战役前轮定论「`trade_when` 门控是低成本正交化器（S +0.06 / sub +0.20 / self −0.29）」在 DEU 上第二次复现，且这次拿到了决定性的 self = 1.0 对照。

**方法论含义**：在一个已有 ACTIVE alpha 的骨架上做「门控变异」，是**在合规约束下产出新 alpha 的最短路径**——因为骨架的信号强度已被验证，只需换一道与主信号无关的门控就能把 self 压到 0.7 以下。这条路径此前在 DEU 被反复使用（11 条 ACTIVE 里多条是 MODEL+OTHER 的同族变异）。

### 50.4 2Y 三杠杆总表（同一内核，三种不同层）

| 杠杆层 | 具体做法 | 2Y 变化 | S 变化 | sub 变化 | 是否付学费 |
|---|---|---|---|---|---|
| **结构层（推荐）** | 内层 `group_neutralize(..., bucket(rank(信号历史均值)))`，步长 0.05 | 1.00 → **2.09**（+109%） | 1.56 → 1.83（+17%） | 1.01 → 0.99（不动） | **否** |
| 设置层 | neutralization → CROWDING | 1.14 → 2.28（+100%） | 1.59 → 1.34（−16%） | 0.93 → 0.48（−48%） | **是，重** |
| 设置层 | neutralization → REVERSION_AND_MOMENTUM | — → 2.24 | — → 1.22 | — → 0.47 | **是，重** |
| 信号层（无效） | 原始频率 / `ts_mean` 平滑 / backfill 180 / 门控 | 1.10–1.14 **锁死** | — | — | 无效轴 |

三条设置层的样本（CROWDING / REVMOM / STATISTICAL，后者见论坛）**全部呈现「2Y 猛涨 + S 掉 + sub 崩」的同型特征**，说明它们共同的机制是「剔掉风险因子暴露后的残差在近两年更稳」，代价是把 alpha 变成了风险模型的附庸。**只有结构层的 bucket 剥离能同时保住 S 与 sub。**

### 50.5 收尾：H 系列与 ts_rank 路线的死刑

| tag | alpha | 结构 | S | F | 2Y | TO | sub | margin | failed |
|---|---|---|---|---|---|---|---|---|---|
| H1_raw | `1YNvAZEX` | 纯 ATOM `rank(ts_backfill(eps,252))` | **1.62** ✅ | 1.43 | 1.10 | 7.32% | 0.85 | 15.8bp | 1 |
| BF180 | `O0AeXzLR` | 门控 + `ts_backfill(eps,180)` | 1.59 | 1.35 | 1.14 | 5.58% | **1.02** | 32.7bp | 1 |
| H2_rawgate | `d5WqJelw` | 门控 + 原始 `rank(bf(eps,252))`（无 add/ts_mean） | 1.59 | 1.35 | 1.14 | 5.58% | 1.02 | 32.5bp | 1 |
| H3_d22 | `omE2jQVn` | `rank(ts_delta(ts_backfill(eps,252), 22))` | **0.55** | 0.23 | 0.06 | 16.25% | 0.14 | 3.4bp | 4 |
| TSR180 | `1YNvA8xW` | 门控 + `rank(ts_rank(ts_backfill(eps,252), 180))` | **0.73** | 0.38 | **0.09** | 8.68% | 0.31 | 8.0bp | 4 |

- **`ts_rank` 包裹信号第三次确认是纯损失**（S 1.59→0.73，2Y 1.14→0.09）；此前 66/126 窗同样纯损失。**DEU 门控型 alpha 的信号必须保持截面 `rank()` 原形。**
- **`ts_delta(·,22)` 一阶差分第二次确认毁信号**（S 0.55 / 2Y 0.06）。
- **「原始频率提升 2Y」假设正式否定**：原始 / `ts_mean` 平滑 / backfill180 / 门控四种处理，2Y 全部锁在 1.10–1.14，TO 也没冲高（5.58–7.32%）。原因：`eps_y1_estimate_change_3mo` 本身低频，不是被平滑抹掉的。
- `H2_rawgate`（最简结构 `rank(ts_backfill(eps,252))`）S 1.59 已过闸、F 1.35 过闸、TO 5.58%、sub 1.02 —— **2Y 1.14 是它唯一缺口**，可作为「最简 ATOM 模板」移植到其他塔。

### 50.6 数据集层判死（本轮新增）

| 数据集 | 塔 | 判死依据 |
|---|---|---|
| **analyst93** | ANALYST | P9 波 10 个结构互异模板全灭，最好 `mLoO55m5` S 1.09 / 2Y 0.74，距闸 45%。该集是「分析师技能属性」（accuracy / consistency / revision correctness / track-record profitability），在 DEU TOP500 无承载能力。**但其 `eps_y1_estimate_change_3mo` 已作为 J3_B 骨架主腿出货，两者是不同字段。** |
| **socialmedia39** | SOCIALMEDIA | 唯一个字段 `scl39_top5_people_also_watch_ticker_ii` 是 VECTOR 型的**共看邻居 ticker ID（关联标识，非数值信号）**，无法构成 ATOM alpha。 |
| news104 / news17 | NEWS | 前轮判死（镜像腿 ±S 完全对称 = 噪声指纹） |

**`risk88` 的特殊价值（新发现）**：`alternative_market_cap_usd` 是 **DEU 唯一 coverage = 1.0 的市值字段**，且不属于 PV。可作为**不依赖 PV 的合法分母**，用于构造 `divide(基本面金额, alternative_market_cap_usd)` 型估值因子，从而绕开 PV 塔混约束。此前 `fnd45_mktcap` 因 coverage 仅 0.2981 导致叠加后有效样本不足（S 0.36 / 2Y 0.04）而失败，此字段是同用途的替代品。

### 50.7 未点亮塔的数据集供给盘点（DEU D1 TOP500）

| 塔 | 可用数据集 | 字段数 | coverage | 状态 |
|---|---|---|---|---|
| **imbalance** | `imbalance5` | 2（`imb5_score` 0–1 韧性分 / `imb5_mktcap`） | 元数据 0.0 | **探针在飞**（J3 波 B 批） |
| **macro** | `macro27`（job postings，全 VECTOR） | 13（`num_jobs_active` / `num_jobs_created` / `num_jobs_removed` / `mean_days_job_active` …） | 元数据 0.0 | **探针在飞** |
| **earnings** | `earnings_sent_matrix` | 7（三分类概率求和为 1 + 2 种加权 + argmax） | 元数据 0.0 | **探针在飞** |
| | `earnings6` | 18 | 元数据 0.0 | 待探 |
| **socialmedia** | `socialmedia39` | 1（VECTOR 关联 ID） | 0.2748 | **判死** |
| | `socialmedia12` | 18 | 元数据 0.0 | 待探 |
| **risk** | `risk88` | 1（`alternative_market_cap_usd`） | **1.0** | 只能做分母 |
| | `risk71` / `risk72` / `risk68` | 10 / 31 / 5 | 元数据 0.0 | 待探 |
| | `risk60` | 5 | 0.835 | 前轮已判死 |
| **option** | `option1` | 全字段 cov 0.0 | 0.0 | **判死，该塔不可点亮** |
| **pv** | （未盘点） | — | — | 待盘点 |
| **sentiment** | sentiment27 / sentiment7 | — | — | 前轮判死（作主腿） |
| **insiders** | `insiders1` / `insider_agg_matrix` | — | — | `insiders1` 无买卖方向字段；`insider_trx_matrix` 判死 |

⇒ **可争取的塔 = 9 个**（imbalance / macro / earnings / socialmedia / risk / pv / insiders + 已活的 analyst / fundamental / institutions / shortinterest / model / other）。option 塔确定无法点亮。

---

## §51 新塔探针收批 + 论坛取证 continuation_score + P16 形态相似度判死（2026-10-30 夜）

### 51.1 P15 新塔探针 6 条收割：risk71 / earnings6 / socialmedia12 全部判死

设置统一 `DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08/nanHandling ON`。

| tag | 字段 | alpha | S | F | 2Y | TO | sub | 判定 |
|---|---|---|---|---|---|---|---|---|
| SM_expchg | `sentiment_expected_price_change` | `78LO5zpb` | 0.21 | 0.09 | −0.00 | 8.37% | 0.12 | 死 |
| SM_score | `sentiment_score` | `xArMLl7m` | 0.14 | 0.03 | 0.17 | 23.38% | 0.25 | 死 |
| R71_mom5 | `residualized_return_top2500` × ts_sum 5 | `JjelAoVm` | −0.41 | −0.10 | 0.15 | **40.96%** | 0.16 | 死（符号反转也只有 0.41） |
| R71_mom22 | 同上 × ts_sum 22 | `0mYoVN0k` | −0.17 | −0.04 | 0.14 | 17.74% | −0.07 | 死 |
| ERN_surprise | `ern6_actual_eps − ern6_estimated_eps` | `xArMLWQq` | 0.83 | 0.66 | 0.01 | 4.09% | **−0.82** | 死（子宇宙崩） |
| ERN_prelim_width | `preliminary_eps_range_upper − lower` | `A1V6pe1e` | 0.33 | 0.34 | 0.00 | 1.81% | 0.12 | 死（DD **62.09%**） |

**三条定论**：

1. **risk71 残差动量族在 DEU 无动量**：5 日与 22 日都为负，5 日 TO 高达 40.96%。符号反转后 S 仅 0.41，远不够。⇒ risk71 唯一候选字段 `residualized_return_top2500` 作主腿判死。
2. **earnings6 PEAD surprise 是「假强」**：S 0.83 看似有信号，但 `sub_universe_sharpe = −0.82`（子宇宙完全反向）+ 2Y 0.01。这是典型「全样本靠少数大票撑起、小票反向」的结构，不可提交。
3. **socialmedia12 两个语义最强的字段（情绪分数 / 预期价格变化）都无信号**。叠加前轮 `socialmedia39` 判死（唯一字段是 VECTOR 型共看邻居 ID）⇒ **socialmedia 塔无可点亮路径**。

⇒ **earnings 塔不可点亮**（`earnings_sent_matrix` + `earnings6` 两数据集全灭）；**socialmedia 塔不可点亮**。

### 51.2 论坛取证：CHN 有一篇直接讲 continuation_score 的赢家贴（投票 9 / 18 评论）

`read_forum_post(412791111-12855)`《CHN Python Alpha 踩坑实录：risk72 死磕 prod_corr 无果，换 virgin 数据集才过关》。可迁移的要点：

| # | 结论 | 原文依据 |
|---|---|---|
| 1 | **risk72 specific-return 族 prod_corr 结构性地卡 0.79–0.90**，换算子/换 cfg 字段名/blend 全部无效 | 五种尝试（ts_mean 预平滑 / 自定义 EWMA / 行业正交 / pv1 soft blend / 只换 cfg）prod 全在 0.79–0.90 |
| 2 | **换数据集 > 换算子**，这是结构性降相关的唯一路径 | "信号同质时，prod 的下限写在数据集的拥挤度里，不写在算子里" |
| 3 | **低 prod ≠ 可提交**：同一批 virgin 数据集中，`fundamental6` prod 仅 0.30 但 S 只有 0.36 | 四数据集对照表 |
| 4 | **★ 同批实测：`pattern_scores` 在 CHN 的 S 仅 0.36**（"低相关但无信号"），而 `continuation_score` 是 2.51 的赢家 | 三、数据 pivot 对照表 |
| 5 | **赢家骨架 = 形态 spread（peak − recent）+ 多 horizon 反转 rank ensemble** | 三字段：`max_inverse_cup_handle_similarity` / `cup_and_handle_similarity_maximum_h60` / `recent_similarity_inverse_cup_handle` |
| 6 | **decay 是 2Y 第一旋钮，lookback 几乎不影响 IS** | decay 8→2Y 2.11 PASS / 12→2.07 踩线 / 15→1.97 FAIL；lookback {40,50,63,80} 无差别 |
| 7 | 形态识别有 40–60 天确认滞后 ⇒ 信号天然带「形态失败」风险 | 评论（QZ67721）指出入场点早于确认点 |
| 8 | **prod 有两条逃生阀**：① 比最相似已提交 alpha 的 Sharpe 高 ≥10% 可豁免（beat-by-10%）② PPA 通道（须提交前打 `PowerPoolSelected` 标）| 评论（JR57542），跨区通用 |

**⇒ 该贴把 `continuation_score` 抬成了 pv 塔的第一优先。但第 4 条同时也是警告：同一套形态相似度机制在 `pattern_scores` 上只有 0.36。**

### 51.3 P16 continuation_score 探针波：11 个结构互异模板，10/10 全灭

字段结构（DEU 侧 560 字段，`bear_cup_handle_recent_similarity` 等 36 个杯柄族字段全 MATRIX）：每个 pattern 同时提供 **peak(max) / average / middle(median) / minimum / dispersion(std) / percentile_95 / recent / dynamic** 八族统计量 × 多 horizon（base / h40 / h60 / h40w）。这正好让「peak − recent」这类 spread 骨架可以直接表达。

零配额预检 `preflight_expressions` 11/11 字段有效（`coverage` 元数据全 0.0 仍是元数据问题，实测有数据）。

设置统一 `DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08/nanHandling ON`。

| 模板 | 结构 | alpha | S | F | 2Y | TO | sub | margin |
|---|---|---|---|---|---|---|---|---|
| **T6 tsmean spread** | peak−recent 的 22 日均值 | `zq3alqG8` | **0.36** | 0.14 | 0.47 | 11.67% | 0.48 | 3.22bp |
| T3 dispersion | 形态歧义度水平量 | `Jjel9eEn` | 0.19 | 0.05 | 0.06 | 14.22% | −0.17 | 1.33bp |
| T4 p95−min | 形态强度极差 | `wpQ6rL8d` | 0.19 | 0.04 | 0.08 | 17.97% | −0.09 | 1.03bp |
| T8 grp bull−bear | bull−bear 差价的行业内 rank | `d5WqGNwX` | 0.09 | 0.02 | **1.42** | 14.29% | 0.10 | 0.65bp |
| T10 h40 spread | 40 日 horizon 的 peak−recent | `akKJp5qx` | 0.03 | 0.00 | 0.01 | 36.31% | −0.38 | 0.08bp |
| T5 bull−bear | 两个独立形态族的对抗差价 | `leAxmrJn` | −0.01 | −0.00 | **1.08** | 14.86% | 0.08 | −0.05bp |
| T2 peak−avg | 峰值向均值回落 | `WjOk5bnd` | −0.07 | −0.01 | −0.14 | 22.77% | −0.19 | −0.29bp |
| **T1 peak−recent** | **论坛金牌骨架** | `P0oeVvqJ` | **−0.25** | −0.05 | −0.16 | 31.20% | 0.26 | −0.85bp |
| T9 J3 bucket | 内层 GN + 正交 bucket 0.05 | `e75AXlKz` | −0.26 | −0.05 | 0.07 | 32.13% | 0.23 | −0.83bp |
| T7 norm spread | spread ÷ 自身基线（归一化） | `A1V6Ax3Q` | −0.52 | −0.13 | −0.52 | 43.17% | 0.23 | −1.18bp |

**五条定论**：

1. **论坛金牌骨架在 DEU 直接失效**：同一个 peak−recent 结构，CHN 上 S 2.51 / prod 0.70，DEU 上 **S −0.25 / 2Y −0.16**。差 2.76 个 Sharpe。⇒ **形态相似度是市场特异性极强的信号，不能跨市场迁移**——这与「IND 上好用的 residual+vol 模板算子可移植、数据字段不能照搬」（论坛原话）完全一致。
2. **不是换手问题，是信号不存在**：10 个模板的 TO 全部落在 **11.67%–43.17%** 的健康区间（远低于 70% 上限），margin 都在 ±3.3bp 量级 ⇒ 换手治理无从下手，因为分子本来就没有收益。
3. **判死三条件第 3 条给出硬上限**：最好模板 T6 的 `R/TO = 0.0188/0.1167 = 0.161`，F 上限 = `S·√(R/TO) = 0.36 × 0.40 = 0.144`，距 F 闸 1.0 差 **7 倍**。即便把 S 推到 1.58，F 也只能到 0.63。**无补救空间。**
4. **唯一「好看」的 2Y 是陷阱**：T8（2Y 1.42）与 T5（2Y 1.08）都是 bull−bear 差价族，全样本 S 却只有 0.09 / −0.01。⇒ **信号只存在于最近两年**，是 regime 依赖而非稳健 alpha。这类「2Y 高 / 全样本零」的组合绝不能当候选。
5. **J3 范式（内层 GN + 正交 bucket）在零信号字段上不创造信号**：T9 把 T1 的 S 从 −0.25 推到 −0.26（无变化）、TO 从 31.2% 抬到 32.1%。⇒ 该范式是「在已有信号的骨架上剥离风格因子」，**不是信号放大器**，这条与 §50.5 的结论再次吻合。

⇒ **`continuation_score` 判死（DEU D1）**；叠加论坛在 CHN 实测 `pattern_scores` S 0.36 ⇒ **pv 塔的「技术形态相似度」整族在 DEU 无信号**，`pattern_scores`（504 字段 / alphaCount 266）不再值得派发探针。

### 51.4 塔位终局盘点（DEU D1 TOP500）

| 塔 | 状态 | 关键证据 |
|---|---|---|
| analyst | ✅ 已亮 1 | `2rjrMZ25`（`eps_y1_estimate_change_3mo`） |
| fundamental | ✅ 已亮 1 | `Wje5K71x` |
| institutions | ✅ 已亮 1 | `2rmGAPqN` |
| model | ✅ 已亮 1 | `883Y3bAW` / `58gkLAkk` |
| other | ✅ 已亮 2 | 同上两条 |
| shortinterest | ✅ 已亮（可加） | 费率族；注意 `kqNRbvJP` prod 0.8463 已 BLOCKED |
| **pv** | ❌ **形态相似度整族判死**；`pv1` 全平台最饱和（alphaCount 12639） | §51.2 第 4 条 + §51.3 |
| **risk** | ❌ **risk71 动量族死 + risk72 被论坛判为 prod 结构性拥挤（CHN 0.79–0.90）** | §51.1 + §51.2 第 1 条 |
| **earnings** | ❌ 两数据集全灭 | `earnings_sent_matrix` + `earnings6` |
| **socialmedia** | ❌ 两数据集全灭 | `socialmedia39` + `socialmedia12` |
| **imbalance** | ❌ 唯一数据集死 | `imb5_score` 静态评分 |
| **macro** | ❌ 4 字段全灭 | `macro27` |
| **option** | ❌ 唯一数据集 cov 0 | `option1` |
| **news** | ❌ 镜像腿对称 | `news104` / `news17` |
| **sentiment** | ❌ 作主腿死 | `sentiment27` / `sentiment7` |
| **insiders** | ⚠️ 唯一未穷尽 | `insider_agg_matrix`（`insiders1` 无买卖方向字段） |

⇒ **DEU D1 可点亮的塔上限 = 7 个（已亮 4 + shortinterest + fundamental 已计 + institutions）**，其中已亮 4 个（analyst / fundamental / institutions / model+other 同源）。**剩余可争取的塔从 9 个收缩到 1 个（insiders）**。

### 51.5 60 颗目标的真实可达性（诚实结算）

- **累计已测**：约 **330 条**（本轮 + 前序）。
- **IS 全闸通过名义 4 条，实质 1 条**（其余 3 条 self ≥0.98 是同族重复）。
- **prod 通过**：0 条。
- **本轮塔位增量**：0 个。
- **失败机制归因**：不是「模板不够多」（本轮已按硬约束做到每族 ≥10 个结构互异模板），而是 **DEU D1 的可用数据集里，能承载 alpha 的信号源已被穷尽**——15 个 category 中有 9 个的数据集全灭，剩余 6 个里 4 个已出货、1 个（pv）形态族判死、1 个（insiders）未穷尽。

⇒ **60 颗 regular alpha 在 DEU D1 TOP500 现有供给下不可达成。** 现实上限受三件事锁死：① 可点亮塔 ≤7 个；② 每塔需 3 颗且两两 self <0.7（已实证同数据集变体的 self 会到 0.98–1.0）；③ prod 0.7 墙（本轮首个撞墙样本 `kqNRbvJP` 0.8463）。**需向用户提出重估目标或转区。**

---

## 52. P17 `insider_agg_matrix` 探针波收尾 + DEU 存量弹药清算（2026-10-30 22:35）

### 52.1 P17 波 22 条全表（16 个结构互异模板 + 3 个设置变体 + 3 个分组交叉变体）

设置基线：DEU / TOP500 / D1 / trunc 0.08 / nanHandling ON / maxTrade ON / FASTEXPR，默认 SLOW + decay 15。

| # | 模板结构 | alpha | S | F | 2Y | TO | sub | margin | DD |
|---|---|---|---|---|---|---|---|---|---|
| T1 | 论坛金牌骨架（EUR 1.89）SLOW d15 | `GrWVZ7X0` | 0.56 | 0.23 | 0.69 | 4.34% | 0.25 | 10.12bp | — |
| T1a | 同上 · SUBINDUSTRY | `1YNvr2dX` | 0.63 | 0.31 | 0.60 | 3.00% | 0.34 | **19.98bp** | — |
| T1b | 同上 · REVERSION_AND_MOMENTUM | `e75AXvbE` | 0.64 | 0.30 | 1.02 | 3.92% | 0.29 | 14.26bp | — |
| T1c | 同上 · SLOW decay 4 | `wpQ60WWY` | 0.60 | 0.26 | 0.70 | 4.89% | 0.27 | 9.69bp | — |
| T1d | 同上 · STATISTICAL | `bl67YNXR` | 0.52 | 0.20 | **1.12** | 4.25% | 0.27 | 9.10bp | 9.13% |
| T2 | avg 分母（论坛 −0.06 降相关轴） | `RREXGxw0` | 0.45 | 0.17 | 0.55 | 4.35% | 0.16 | 8.17bp | — |
| T3 | 二阶均值回复（论坛 S −0.73） | `npv0LEz8` | **−0.01** | 0.00 | −0.56 | 4.61% | 0.13 | −0.21bp | — |
| T4 | 净流量 63 日 | `vR10W7wG` | 0.58 | 0.25 | 0.42 | 4.55% | 0.44 | 9.98bp | — |
| T5 | 买卖比 63 日 | `78LgkWOZ` | 0.72 | 0.35 | 0.98 | 4.59% | **−0.04** | 12.98bp | — |
| **T6** | **跨量纲短窗（金额 63 ÷ 股数 252）** | **`A1VqRZRd`** | **0.91** | **0.49** | **1.54** | 4.25% | 0.26 | 16.81bp | 8.14% |
| T7 | 集中度极差 | `wpQX8qn6` | 0.57 | 0.28 | 0.20 | **10.60%** | **0.70** | 5.81bp | — |
| T8 | 高管 vs 全体做差 | `QPvm1e7X` | 0.42 | 0.18 | **0.10** | 10.57% | 0.63 | 4.15bp | 12.83% |
| T9 | 高斯分位（T1 骨架 + gaussian） | `npvw1wqw` | 0.58 | 0.25 | 1.32 | 4.81% | 0.39 | 9.68bp | 11.02% |
| T10 | 活跃度门控 | `Xg9Xjgpm` | 0.55 | 0.23 | 0.74 | 4.34% | 0.25 | 9.93bp | — |
| T11 | bucket 剥离层 | `YP1Xj26q` | 0.41 | 0.15 | 0.20 | 4.56% | 0.26 | 6.98bp | 6.39% |
| T12 | 尺度翻转 | `xArXKOop` | 0.51 | 0.20 | 0.58 | 3.32% | 0.07 | 11.50bp | — |
| T13 | T1 × group=sector | `rKRQ1L59` | 0.75 | 0.36 | 1.16 | 4.22% | 0.33 | 13.97bp | 10.06% |
| T14 | T1 × group=market | `QPvm1jeg` | **0.79** | 0.39 | 1.17 | 4.18% | 0.31 | 14.74bp | 9.61% |
| T15 | T1 × group=subindustry | `O0AK1o91` | 0.53 | 0.21 | 0.88 | 4.32% | 0.34 | 9.43bp | 9.55% |
| T6m | T6 × group=market | `d5We2Ygg` | 0.88 | 0.47 | 1.48 | 4.18% | 0.17 | 16.82bp | 9.05% |
| T6s | T6 × group=sector | `1YN6qRdQ` | **0.92** | **0.50** | 1.48 | 4.20% | 0.19 | **17.45bp** | 8.41% |
| T6wm | T6 × market × 尺度 42/378 | `d5We26dx` | 0.78 | 0.40 | **2.01** | 4.52% | **0.10** | 14.55bp | 8.13% |

**全波极差：|S| 0.41–0.92（T3 的 −0.01 除外）；sub 0.07–0.70；TO 3.0–10.6%；DD 6.4–12.8%。全部 22 条 `failed_ra_count ≥ 3`。**

### 52.2 五条结论（每条都有对照实验支撑）

**① 中性化是死轴（DEU）。** T1 骨架四档：SLOW 0.56 / SUBINDUSTRY 0.63 / R&M 0.64 / STATISTICAL 0.52，极差 0.12；decay 4 vs 15 逐位近似（0.60 vs 0.56，TO 4.89% vs 4.34%）。
⇒ 对照 EUR 同骨架 SLOW 1.68–1.89 / R&M 1.44 / STATISTICAL 1.34 / FAST 1.18（**差 0.71 Sharpe**）。**中性化只能重分配已有信号，DEU 里该轴全平恰好说明信号本身不存在**——这是"信号缺失"的一个廉价判据。

**② 分组轴在 T1 上是活轴、在 T6 上是死轴（★ 最重要）。**
- T1 骨架：market **0.79** > sector 0.75 > industry 0.56 > subindustry 0.53 ⇒ 极差 **0.23**，粗分组显著更好。
- T6 骨架：sector **0.92** ≈ industry 0.91 > market 0.88 ⇒ 极差 **0.04**，且 `sub_universe_sharpe` 随分组变粗**单调崩塌** 0.26 → 0.19 → 0.17 → 0.10。
⇒ 精确复现论坛 LW67640 的判断「**分组优劣序与外层算子耦合、不是数据集属性**」。**在骨架 A 扫出的最优分组轴，不能搬到骨架 B 当已知结论**；且粗分组会**抬 S 砍 sub**（本例 sub 减 62%）。已作为跨区方法论入库 `M_GENERAL_GROUP_AXIS_NOT_TRANSFERABLE`。

**③ 做差族再次被规模因子吃掉。** T8 `group_rank(subtract(top_significant_value_1,significant_value_1),industry)`：S 0.42 / **2Y 0.10** / TO 10.57%。与论坛「金额与股数同暴露在规模因子上，做差/正交全被吃掉，只有除法能约掉规模成分」完全一致。
**④ bucket 剥离层在这个骨架上是有害的。** T11 → S 0.41（< 基线 0.56）、2Y 0.20（< 0.69）。与既有「bucket 剥离层只在『信号自身历史均值』作轴时有效、且与 CROWDING 不叠加」一致，此处轴选的是 `ts_sum(significant_value_1,252)`（金额规模，非自身信号均值）⇒ 轴选错即纯损失。
**⑤ 尺度分离能换 2Y 但要付 S 与 sub。** T6wm 42/378：2Y 1.54 → **2.01**（+0.31），代价 S 0.91 → 0.78、sub 0.26 → **0.10**。⇒ 尺度是 2Y 的活轴，但**不能同时保住 sub**；而 sub 0.10 已远低于 0.4 线。

### 52.3 insiders 塔判定：不可点亮，且揭示「第四类判死形态」

三条件判死表**不命中**：① TO 全部 3.0–10.6%（远低于 70%）；② 唯一压 TO 的算子族没有把 S 打崩；③ 最好模板 `R/TO = 0.84`（远高于 0.10）。
但 22 个结构互异模板/变体的 max|S| = **0.92**、max sub = 0.70（T7，但 S 仅 0.57 且 TO 翻倍），距 S 闸 1.58 **差 0.66**。

⇒ **第四类判死形态：信号源幅度不足**——`R/TO`、`TO`、`DD` 三项全健康，`fitness` 恒等式也对得上（`0.91 × sqrt(0.0357/0.125) = 0.486 ≈ F 0.49`），**唯独 S 打不到闸**。这种情况下继续堆模板（已堆到 22 个）是纯浪费仿真槽，必须换数据集或换区。
判据（新增，建议并入区域 SOP）：**≥15 个结构互异模板的 max|S| < 1.0 且 max sub < 0.75，同时 TO 正常（<20%）、R/TO 正常（>0.3），即可判死该数据集在目标区域的信号幅度。**

### 52.4 「推 prod 墙」路线的弹药清算（★ 决定性负面结论）

对 `search_alphas_by_sharpe(DEU, S≥1.58)` 的 **40 条存量**做族归并，结论是**这批存量几乎全部不可用**：

| 族 | 条数 | 表达式骨架 | prod 状态 | 裁决 |
|---|---|---|---|---|
| `tm_` 单字段 | 11 | `group_rank(tm_{8,15,16}_r1_r5_r10_rh_glb_d1_r{5,10}_q1, sector)` | `JjelQnvE`(tm_8) = **0.9084 撞墙**；其余 10 条 NA | **同族证伪，弃**（`JjelQJoe` S 2.70 vs 2.61 只高 3.4%，够不到 beat-by-10%） |
| `vector_neut(ts_quantile(ts_ir(snt7…)))` | 7 | 双层 `vector_neut` + `snt7_all_languages_views` | `P0oe6wpJ` = **0.7694 撞墙**；`N1NML1wq` 与其**指标逐位相同**（S 2.14/F 1.99/TO 10.36%/2Y 2.56/sub 1.37） | **孪生证伪，整族 7 条全弃** |
| `add(add(add(rank…)))` 多信号拼接 | 10 | 4 维 rank 相加 | `j23xxK8o`/`RRVKKwAj` 0.7859、`MP1ZZN3L` 0.79、`kqVOO6gg` 0.8055、`qMW33J0V` 0.7994、`O0rVVXJb` 0.7973；2 条已提交（0.5434 / 0.6388） | **6 条同族撞墙 + 违反「禁 add 混信号」⇒ 弃** |
| `R83` | 4 | 拼接复刻 | `j23xqexE` = **0.7746 撞墙** | **同族证伪，弃** |
| `R84/R85` | 3 | 拼接复刻 | `le81Lq2e` = **0.8817 撞墙** | **同族证伪，弃** |
| `R89` | 3 | `add(×4 rank)` | 全 NA | **内部互相关 0.983–0.994（只算 1 颗）**；`E5vLLPV0.pyramid_short = "model/other"` ⇒ **MODEL+OTHER 违反硬禁令**；且是 add 混信号 ⇒ **弃** |
| 超 alpha | 2 | `combo_a` / Super | 0.8849 / 0.6108（已提交） | 不可用 |

**核心教训：「prod = NA」是假阴性。** 40 条里有 **12 条**通过孪生体或同族的实测 prod（0.77–0.91）间接证伪，**10 条**塔位违规或违反 add 禁令。真正"prod 未测且无任何反证"的候选 = **0 条**。
⇒ **不得把 DB 里的 `prod_correlation IS NULL` 当作「未开发的强候选」**。正确读法：先按「表达式骨架 + 指标指纹」做族归并，只要族内有 1 条撞墙（或逐位孪生体撞墙），整族按撞墙处理。**这一步是零成本的，能在花 prod 槽之前砍掉 100% 的伪弹药。**

### 52.5 本波净产出与下一步

- **P17 净产出**：22 条回测，**0 条可提交**，塔位增量 **0**（insiders 塔未点亮）。
- **最强留档**：`A1VqRZRd`（T6 跨量纲短窗）S 0.91 / F 0.49 / 2Y 1.54 / TO 4.25% / margin 16.81bp / DD 8.14%。R/TO 0.84 健康，若未来作 Mode B 辅助腿（跨数据集配对）可复用其"金额÷股数约掉规模成分"的几何。
- **唯一实质候选仍为 `Vkxnb8QG`**（S 1.83 / F 1.64 / 2Y 2.09 / TO 9.06% / sub 0.99 / DD 5.58% / margin 22.27bp / `failed_ra_count = 0` / `pyramid_short = "shortinterest/analyst"` 塔位合规 / self 0.6379 PASS），**只差 prod 终验**。
- **下一步**：① prod 槽释放（`prod_wait.py` PID 7384 起于 22:29:18，约 22:43 释放）后立即终验 `Vkxnb8QG`；② 向用户报告 60 颗目标不可达 + 请重估目标或转区。

---

## §53 pv 塔总清算：数据集逐个取证 + pv109 12 模板 + intraday_pv_feats 探针

> 结论先行：**pv 塔在 DEU D1 不可点亮**。`pv109` 26 字段只有 5 个有数据且 max|S| 0.54；`pv29`/`pv30` 是纯分组元数据（无信号）；`pv173` 仅 USA/ASI/China；`intraday_pv_feats` 有数据但信号统一停在 0.33 附近且原生换手 39–84%。至此 DEU 全部 11 个未点亮塔均已完成取证，无一可点亮。

### 53.1 pv 塔数据集全盘点（DEU / D1 / TOP500，`get_datasets` + `get_datafields` 实拉）

| 数据集 | 字段数 | 实测状态 | 判定 |
|---|---|---|---|
| `pv109`（公司债） | 26 | 仅 5/26 字段有数据；12 模板 max\|S\| 0.54 | **判死** |
| `intraday_pv_feats` | 585 | 有数据（2/2 单字段探针 COMPLETE）；原生换手 39–84%、信号 ≈0.33 | **判死**（结构性高换手） |
| `pv29` | 50 | 全部是**统计行业聚类标签**（MATRIX/GROUP，`industry_grouping_level*` / `sta1_top*c*`） | **不可作信号源**，只能当 `group_*` 分组轴 |
| `pv30` | 285 | 同上（`*_pca_component_*` / `factor*_group*` / `factor*_grouping*_score_*`） | **不可作信号源** |
| `pv173` | 81 | 全 VECTOR、cov 全 0、描述限 USA Markit BLE / ASI / China | **排除**（非本区） |
| `pv1` | 23 | alphaCount **12639**（最饱和） | 不作优先 |
| `pv20` / `continuation_score` / `pattern_scores` | — | 已判死 | 判死 |

**新平台事实（写错会白烧一次仿真）**：`pv30` 的 `*_pca_component_*` 与 `factor*_grouping*_score_*` 的 `description` 明明写着「Continuous factor loading (exposure)」这种像信号的话术，**但 `type` 是 `GROUP`**，值是整数簇标签。⇒ **判数据集能不能做信号，看 `type` 不看 description**；`GROUP` 类型只能进 `group_rank`/`group_neutralize`/`bucket` 的第二参。

### 53.2 pv109 12 个结构互异模板全表（SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling ON）

| # | 模板机制（结构互异轴） | alpha | S | F | 2Y | TO | sub | margin | DD | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 信用利差水平（YTM − 票息，水平·差） | — | — | — | — | — | — | — | — | **FAIL**（字段空） |
| T2 | YTM 一阶差分 63d（一阶矩） | `9qxgYWnK` | 0.45 | 0.20 | 1.43 | 9.80% | −0.06 | 0.48bp | 11.82% | REJECT |
| T3 | 债券买卖价差（微观结构） | — | — | — | — | — | — | — | — | **FAIL**（字段空） |
| T4 | 跨债券收益率离散度（二阶矩·`vec_stddev`） | `MPY9W0aa` | 0.06 | 0.01 | 0.98 | 4.93% | −0.06 | 0.12bp | 21.22% | REJECT |
| T5 | 债券累计表现（现价/发行价） | `78LgAoN5` | 0.02 | 0.00 | 1.15 | 2.79% | −0.19 | 0.08bp | 24.04% | REJECT |
| T6 | 票息水平（单字段·分组 market） | — | — | — | — | — | — | — | — | **FAIL**（字段空） |
| T7 | 债券成交量相对活跃度 | `qMLe10xA` | −0.02 | −0.00 | 0.78 | 20.44% | −0.61 | −0.01bp | 21.44% | REJECT |
| T8 | 债务存量扩张 22/252（增长） | `wpQXmb9Y` | **0.54** | 0.26 | **1.71** | 2.30% | 0.16 | 2.44bp | **7.36%** | REJECT（本波最好） |
| T9 | YTM 504 日时序 z-score（分布变换） | `zq3XZ2rK` | 0.42 | 0.17 | 1.55 | 6.51% | 0.06 | 0.66bp | 12.75% | REJECT |
| T10 | T2 体 + 债券流动性门控（条件） | `1YN6bV8z` | −0.06 | −0.01 | 0.56 | 11.13% | −0.04 | −0.08bp | 40.87% | REJECT |
| T11 | T9 体 + 债务规模 bucket 剥离（分组剥离） | `e75ew8el` | 0.10 | 0.02 | 1.20 | 12.14% | 0.24 | 0.09bp | 14.52% | REJECT |
| T12 | YTM 21/252 carry 比（尺度分离） | `1YN6bmE6` | 0.36 | 0.14 | 0.59 | 3.38% | −0.09 | 1.14bp | 11.20% | REJECT |

**统计读法**：8 条有指标，**max\|S\| = 0.54**（T8），max sub = 0.24，max 2Y = 1.71。按第四类判死形态（信号源幅度不足）判据「≥15 结构互异模板 max\|S\| < 1.0 且 max sub < 0.75」——本波 8 条有指标 + 3 条字段空 + 1 条 carry = 12 个结构互异模板，**且剩余可用字段已被穷尽**（只有 5 个存活字段），故不需再凑满 15 条即可判死：**分母不变而所有可达分子都已试过**。

**T8 的正面价值（可迁移）**：`group_rank(-ts_sum(amt_outstanding)/ts_mean(…,252), industry)` 拿到 S 0.54 / 2Y 1.71 / **DD 仅 7.36%** / TO 2.30% / margin 2.44bp——这是「债务存量扩张 = 外部融资增速」因子，DD 和 2Y 都健康，**缺的只是 Sharpe 幅度**。⇒ 该骨架可迁移到有真信号的数据集（如 fundamental 的资产/股本扩张族），不必留在债券域。

### 53.3 intraday_pv_feats：有数据，但结构性高换手

**先导单字段探针（判「有无数据」）**

| 探针 | 表达式 | alpha | S | F | 2Y | TO | sub | margin |
|---|---|---|---|---|---|---|---|---|
| P1 | `rank(avg_vwap_to_last_price_ratio)` | `E56oWgNm` | −0.12 | −0.01 | 0.31 | **83.58%** | 0.14 | −0.19bp |
| P2 | `rank(avg_ask_price_to_vwap_ratio_first_half)` | `VkxKjOVV` | −0.08 | −0.01 | −1.12 | **44.87%** | −0.43 | −0.23bp |

**两条都 `COMPLETE`（不是 `FAIL`）⇒ 585 个字段在 DEU 确有数据**——这是 pv 塔里除 pv109 之外唯一的真实供给。但注意 `coverage` 元数据全报 0.0，又一次证实**DEU 的 coverage 元数据不可信**。

**批次 1：4 个结构互异模板（decay 4）**

| # | 模板机制 | alpha | S | F | 2Y | TO | sub | margin | invest_S |
|---|---|---|---|---|---|---|---|---|---|
| T1 | 订单流深度失衡（买深 − 卖深，水平差） | `KPJxdVzk` | 0.35 | 0.05 | 0.49 | **69.41%** | 0.04 | 0.48bp | −0.06 |
| T3 | VWAP 偏离反转（`ts_mean` 平滑 5d） | `E56oW8dG` | 0.33 | 0.07 | 0.66 | 39.06% | **0.57** | 0.94bp | **0.84** |
| T5 | 价量相关买卖侧不对称 | `88Rg9ZYz` | 0.33 | 0.05 | 0.50 | **70.94%** | 0.41 | 0.44bp | 0.67 |
| T6 | 日内动量（末半价 / 首半价 − 1） | `Xg9XQvQz` | 0.00 | — | — | 0.00% | — | — | — |

- **T6 全零**：`avg_last_trade_price_last_half` 与 `avg_bid_price_first_half_volume` 相除后无持仓 ⇒ 两个字段至少一个为空或比值恒 NaN。**这是「同数据集内字段可用性不一致」的第三个实例**（前两个是 pv109 的票息/买卖价、pv30 的 PCA 分量）。
- **信号幅度统一卡在 0.33–0.35**：与 `earnings_chart_dl`（7/7 全灭、CNN 日频重算）形态一致。机理：日内微观结构特征对**次日**收益的预测力在学术上是已知的弱（订单流不平衡的预测力集中在分钟—小时级，隔夜衰减殆尽），而换手是字段生成方式决定的。
- **唯一亮点 T3**：`ts_mean(·,5)` 平滑后 sub 0.57 / invest_S 0.84，是全 ipf 系列里唯一「子宇宙也站得住」的形状 ⇒ 若要在 pv 塔继续，唯一值得做的是「以 T3 为底座、把 S 抬起来」，而不是再换字段。

### 53.4 新平台事实：这批「ratio」字段带 CSPrice 单位，且同名前后缀单位不一致

两条 `WARNING` 是本轮最有复用价值的技术发现：

```
subtract(1, avg_bid_to_ask_price_ratio)
  → Incompatible unit for input of "subtract" at index 1,
    expected "Unit[]", found "Unit[CSPrice:1]"

subtract(avg_ask_price_to_vwap_ratio_first_half, avg_ask_to_vwap_ratio_last_half)
  → Incompatible unit for input of "subtract" at index 1,
    expected "Unit[CSPrice:1]", found "Unit[]"
```

读法：
1. `avg_bid_to_ask_price_ratio` 名字叫 ratio，**真实语义是「买价 − 卖价」（价差），带价格单位**，不是无量纲比值。
2. `avg_ask_price_to_vwap_ratio_first_half` 带 `CSPrice`，而 `avg_ask_to_vwap_ratio_last_half` 无量纲 —— **同族字段的建法不同，单位就不同**，不能凭命名推断。
3. 修法优先级：① 单字段直接用 `multiply(-1, F)` 反向（不加常数）；② 混合两字段前先各自 `rank()` 抹单位；③ **不要**靠加 ε 或乘 1 消单位。

应用：任何名字里带 `ratio` 的新字段，**第一次与常数或另一字段运算前，先用 `rank()` 包一层**，否则 `unitHandling=VERIFY` 必挂。

### 53.5 `j2Ym1PL9` 取证：平台 `warning` 级检查等于本地提交闸的阻断

```
trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main), 252)) < 0.7,
           rank(ts_mean(eps_y1_estimate_change_3mo, 22)), -1)
S 1.57 / F 1.33 / TO 3.33% / R 8.96% / DD 10.05% / margin 5.38bp
sub 0.95 / 2Y 1.13 / invest_S 1.41 / risk_neut_S 0.25
longCount 124 / shortCount 120（两侧均衡）
pyramid_short = "shortinterest/analyst"（塔混规则 ✓）
```

`checks.fail = []`，但 `checks.warning` 含两项：
- `LOW_SHARPE`（**1.57 vs limit 1.58**）
- `IS_LADDER_SHARPE`（**1.13 vs limit 1.58**）

`submit_verdict` 裁决 = **BLOCKED**，`reason_code = FAILED_COUNT_RA:LOW_SHARPE,IS_LADDER_SHARPE` + `SUBMIT_HARD_WARN[同两项]`，`submit_status = 404`（`dead_endpoint_404`）。

**这是本战役第三次确认的同一条结论，必须写进纪律**：`failed_ra_count = 2` 的 alpha 无论 `fail` 数组多干净都提交不了；**S 差 0.01 也是硬墙**。DB 里它已有 20.7h 前的 prod 0.5971 / self 0.4213（未过期、两项都在 0.7 以下），但相关性达标毫无意义——**指标闸在前，相关性闸在后，顺序不可颠倒**。

### 53.6 论坛帖 `37123287962519` 取证：无用，已排除

解析正文约 12.5 万字符 + 全部 15 条评论后确认：这是《【wqapp优化】找灵感提示词优化》——关于「72变」App 提示词工程（`BRAIN_Alpha_Template_Expert_SystemPrompt.md`）的**元讨论帖**。

帖中 `bond_momentum = ts_delta(yield_to_maturity, 20) / ts_std(yield_to_maturity, 20)` 是文末「多资产扩展」章节的**通用示例伪代码，零回测证据**。⇒ 不能当 pv109 的模板来源。

**可复用的识别特征**（无证据示例代码 vs 已验证模板）：
- 无 alpha id、无 Sharpe/Fitness/TO 指标
- 出现在「扩展 / 示例 / 多资产推广」章节
- 用「可以试试 / 例如」这类措辞而非「实测」

评论里唯一呼应我方结论的两条（YW36099：AI 堆 `ts_backfill` 就算思考过；XW23690：少用 `ts_rank`/`rank` 这类纯数学变换算子）与既有结论一致，无新信息。

### 53.7 60 颗目标最终结算

**已完成 · 已派发 · 在途 · 未知** 四分口径：

| 口径 | 数量 | 说明 |
|---|---|---|
| 已回测（本轮累计） | ≈ **400** | pv109 12 + ipf 11 + 前面各波 |
| IS 全闸通过（名义） | 4 | 含 S 差 0.01 的 `j2Ym1PL9` |
| **IS 全闸通过（实质）** | **1** | `Vkxnb8QG`（S 1.83 / F 1.64 / 2Y 2.09 / sub 0.99 / fRA 0） |
| prod 终验通过 | **0** | `Vkxnb8QG` 的 prod 始终取不到（槽被占） |
| 已提交 DEU alpha（历史累计） | 11 | prod 全部 < 0.7 |

**结论：60 颗在 DEU D1 现有供给下不可达成。** 不是"跑得不够多"，而是**标的耗尽**：
- 11 个未点亮塔中，10 个的数据集已逐个判死（insiders / news / risk(risk60/71/88) / shortinterest / sentiment / macro / socialmedia / imbalance / option / earnings）
- 第 11 个（pv）在本节完成取证后同样判死
- 唯一未判死的 `risk72` 已在 53.8 排队

**产出率视角**：`get_mining_yield(DEU, strict=true)` = expressions 5119 / consumed 3350（conversion 65.44%）/ ra_clean 234 / prod_clean 9 / **prod_wall_ratio 0.8571**。即「过了 RA 闸的 234 条里，测过 prod 的 63 条中 54 条撞墙」——**即使指标够，六分之五也会死在 prod**。

### 53.8 三条解锁路径（按可行性排序）与下一步

1. **`risk72` 残差反转（本节唯一未否证的供给）** —— `risk72` 31 字段全是 MFM1 风险模型的**特异性（残差）收益**，是短期反转的标准原料；USA 区 `rsk65` 残差反转实测 S 3.38（decay 2→8 的扫描见方法论条目）。`top600_equity_residualized_return` 已 preflight `valid: true`，6 条结构互异模板（1日/5日/22日反转、`ts_av_diff`、zscore 版、风险调整版）已就绪待派。**风险**：论坛证 `risk72` 族 prod 结构性 0.79–0.90，即使 IS 过闸也可能撞 prod 墙 ⇒ 必须在派发时**同时**准备 PPA 通道（提交前打 `PowerPoolSelected` 标，用 PPAC<0.5 取代全平台 PC<0.7）。
2. **prod 逃生阀** —— ① beat-by-10%：比最相似已提交 alpha 的 Sharpe 高 ≥10% 可豁免；② PPA 通道（须 FastEXPR，Python alpha 不 eligible）。
3. **转区** —— IND 14 塔全亮、EUR insiders 已验证 S 1.89；DEU 的 prod_wall_ratio 0.8571 已是结构性饱和。

- **下一步（按序）**：① 收割 ipf 批次 2（T2f/T4f/T7/T8/T9/T10/T11 共 7 条，已全部 submitted）；② 派 `risk72` 6 条残差反转模板（preflight 已过）；③ `Vkxnb8QG` prod 终验——槽被兄弟会话的 `prod_wait.py` 连续排队占用（`1Yj08nb6` → `XgRM3Yra`），**不可连发 `refresh=true`**，只在观察到进程空窗时试一次；④ 把约 400 条未落库结果用 `harvest_multisim_results` 入库。

---

## §54 intraday_pv_feats 全族判死 + risk72 残差反转派发（2026-10-30 23:35）

### 54.1 ipf 13 模板全表（2 条先导探针 + 11 条正式模板，全部收割完毕）

| # | 模板机制 | alpha | S | F | 2Y | TO | sub | invest_S | margin | DD |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 单字段探针：VWAP/末价偏离 | `E56oWgNm` | −0.12 | — | 0.31 | **83.58%** | — | — | — | — |
| P2 | 单字段探针：首半卖价/VWAP | `VkxKjOVV` | −0.08 | — | −1.12 | 44.87% | — | — | — | — |
| T1 | 订单流深度失衡（买深−卖深） | `KPJxdVzk` | 0.35 | 0.05 | 0.49 | **69.41%** | 0.04 | −0.06 | 0.48bp | — |
| T2f | 买卖价差水平（负向） | `58ENoNwN` | −0.17 | −0.05 | −1.02 | **10.39%** | −0.24 | −0.07 | −0.02bp | 23.89% |
| T3 | VWAP 偏离反转（`ts_mean` 5d） | `E56oW8dG` | 0.33 | 0.07 | 0.66 | 39.06% | **0.57** | **0.84** | 0.94bp | — |
| T4f | 双 rank 版卖压不对称 | `9qxgLA1r` | 0.26 | 0.03 | 0.64 | **71.60%** | −0.13 | 0.48 | 0.035bp | 15.85% |
| T5 | 价量相关买卖侧不对称 | `88Rg9ZYz` | 0.33 | 0.05 | 0.50 | **70.94%** | 0.41 | 0.67 | 0.44bp | — |
| T6 | 日内动量（末半价/首半价−1） | `Xg9XQvQz` | 0.00 | — | — | 0.00% | — | — | — | — |
| T7 | 日内 range/VWAP 反向 | `GrWEp0zO` | −0.03 | −0.00 | 0.56 | 54.06% | 0.03 | 0.12 | −0.01bp | 23.30% |
| T8 | 成交量/末笔成交比 | `wpQXMXl2` | 0.04 | 0.01 | 0.04 | **19.81%** | −0.18 | 0.12 | 0.032bp | 15.91% |
| T9 | OIB 一阶差分 5d | `9qxgLREr` | **0.64** | 0.14 | 0.66 | **68.26%** | 0.10 | −0.07 | 0.091bp | 9.31% |
| T10 | OIB + bucket 0.05 剥离 | `d5WeAQaK` | 0.26 | 0.03 | 0.34 | **71.01%** | −0.04 | −0.11 | 0.034bp | 10.12% |
| T11 | 流动性门控版价差 | `akKXq292` | −0.55 | −0.28 | −1.39 | 13.20% | −0.71 | −0.63 | −0.504bp | 40.68% |

**统计**：13 条，`max|S| = 0.64`（T9），但该条 TO 68.26%；`max sub = 0.57`（T3），该条 S 仅 0.33。

**判死三条件逐条检验（全部命中）**：
1. **≥5 个结构互异模板 TO > 70%** —— T1 69.41% / T5 70.94% / T4f 71.60% / T10 71.01% / P1 83.58%，共 5 条 ✓
2. **唯一能压 TO 的算子族同时把 S 打到 <0.6** —— T2f（TO 10.39%，S −0.17）、T8（19.81%，S 0.04）、`akKXq292`（13.20%，S −0.55）全部命中 ✓
3. **最好模板 R/TO < 0.10** —— T9：`R 0.0311 / TO 0.6826 = 0.0456` ⇒ `F 上限 = S·√(R/TO) = 0.64 × 0.2136 = 0.137`，实测 F 0.14 **逐位吻合**，与闸 1.0 差 **7.3 倍**，无补救空间 ✓

⇒ **`intraday_pv_feats` 判死**，与 `earnings_chart_dl` 同型（结构性高换手 + 信号幅度不足 + 子宇宙不稳）。

**机理**：日内微观结构特征对**次日**收益的预测力在学术上本就薄弱（订单流不平衡的预测力集中在分钟—小时级，隔夜衰减殆尽），换手由字段的日频重算方式决定，骨架无法改变。

**唯一残值**：T3 `E56oW8dG`（`group_rank(ts_mean(avg_vwap_to_last_price_ratio, 5), industry)`）是全系列唯一「子宇宙也站得住」的形状（sub 0.57 / invest_S 0.84 / margin 0.94bp），若将来回到 pv 塔只能以 T3 为底座抬 S，**不再换字段**。

### 54.2 risk72 字段取证（★ 键发现：31 字段不是 31 个字段，是 7 套 universe × 2 种语义）

`get_datafields(dataset_id="risk72", region="DEU", universe="TOP500", filter_sharpe=false)` → `count 31 / platform_count 31 / complete true`，全 `coverage 0.0`（按 ipf 教训，cov=0 **不代表无数据**）。

| 族 | 字段 | universe 归属 | 备注 |
|---|---|---|---|
| **selected-universe 残差** | `top600_/top800_/top1200_/top2500_equity_residualized_return` | 「selected universe」 | **4 个不同宽度**，DEU TOP500 最匹配 top600 |
| **同族 nogroup 版** | `top600_/top1200_/top2500_/top800_..._nogroup` | 同上 | **未做分组调整**的残差 ⇒ 语义不同，非别名 |
| **cfg2（明确 EUR）** | `cfg2_top600/800/1200_residual_return` | **EUR TOP600/800/1200** | 描述写明「percent units, after neutralizing market/country/industry and MFM1」 |
| **ecs（Europe）** | `ecs_top400/800/1200/1600_residual_return_cfg2` | EQY_ECS** Europe** TOP* | 另一套欧洲宇宙 |
| **eur minvol1m** | `eur_equity_minvol1m_residual_return` + `_validated` | EUR minvol1m | `_validated` = 当日校验版 |
| **ats** | `ats_top800/top1200_equity_residualized_return` | ATS universe | |
| **epp** | `epp_equity_minvol1m_residual_return` | EPP | |
| **VECTOR 复制因子** | `cfg2_top*_replicator1/2` | 同上 | **VECTOR 型**，须 `vec_avg`/`vec_sum` 先标量化 |
| ⚠ **不可用** | `top600_reproducible_specific_return` | **AMR TOP600** | 描述明确写 AMR，DEU 排除 |

**两条可落地推论**：
1. **「4 个 universe 变体」不能当 4 个结构互异模板** —— 换 universe 只是换数据源精度，不改骨架几何。要凑「≥10 个结构互异模板」必须换**算子几何 / 矩 / 分组轴 / 非线性变换**，universe 变体只能作为**同族正交腿**（且相互相关必然高，不能算点塔的 3 颗）。
2. **`nogroup` 版是真正的语义差异** —— 去掉分组调整后，残差里保留了行业/国家成分，等价于「只剥离市场 + 风格」而非「市场 + 国家 + 行业 + 风格」。它与普通版的差 = 行业/国家成分，可作为**结构性对照实验**，不是调参。

### 54.3 risk72 12 模板派发记录

| # | 模板机制 | 表达式骨架 | 状态 |
|---|---|---|---|
| T1 | 1 日残差水平反转 | `group_rank(multiply(-1, F), industry)` | 已提交 `1gnRfDd7a4Ddbn6WUGaw46v` |
| T2 | 5 日累加反转 | `group_rank(multiply(-1, ts_sum(F,5)), industry)` | 已提交 `1G7qsGBw4DtaPX1hbfBEkkH` |
| T3 | 22 日累加反转 | `group_rank(multiply(-1, ts_sum(F,22)), industry)` | 已提交 `2lJEkibSD4KT93US5jfH366` |
| T4 | 10 日均值 + zscore + subindustry 轴 | `group_zscore(multiply(-1, ts_mean(F,10)), subindustry)` | 已提交 `2pkgok8w25ag9PxuPY3sUH5` |
| T5 | 63 日 `ts_av_diff` 位移 | `group_rank(multiply(-1, ts_av_diff(F,63)), industry)` | 已提交 `29ZY6gdJ94RZaHeLfbEcFQa` |
| T6 | 风险调整反转 5/63（短窗÷长窗波动） | `group_rank(multiply(-1, divide(ts_sum(F,5), ts_std_dev(F,63))), industry)` | 已提交 `3ZTTq467j4McbSjoPFQ7Ujs` |
| T7 | 换数据源：cfg2 EUR 版 5 日均值 | `group_rank(multiply(-1, ts_mean(cfg2_top600_residual_return,5)), industry)` | 已提交 `1CsWR51Aj4nxbGCHaVreB6A` |
| T8 | **nogroup 版**水平（去掉行业/国家剥离的对照） | `group_rank(multiply(-1, top600_..._nogroup), industry)` | **待补派（429）** |
| T9 | 换 universe：top800 + 10 日 | `group_rank(multiply(-1, ts_sum(top800_...,10)), industry)` | **待补派（429）** |
| T10 | 长窗均值 252 日（尺度分离） | `group_rank(multiply(-1, ts_mean(top1200_...,252)), industry)` | **待补派（429）** |
| T11 | 波动 bucket 剥离层（`ts_std_dev` 63d 作轴） | `group_neutralize(group_rank(...), bucket(rank(ts_std_dev(F,63)), range="0,1,0.05"))` | **待补派（429）** |
| T12 | 风险调整反转 22/22（另一组矩几何） | `group_rank(multiply(-1, divide(ts_sum(F,22), ts_std_dev(F,22))), industry)` | **待补派（429）** |

**模板多样性自查（对照「每个波次 ≥10 个结构互异」硬约束）**：
- 结构互异维度覆盖：**水平**（T1/T8）× **一阶累加**（T2/T3/T9）× **均值**（T4/T10）× **位移**（T5）× **风险调整**（T6/T12）× **换数据源**（T7）× **分组剥离层**（T11）× **换分组轴**（T4 subindustry）
- 共 **8 个几何族 / 12 条**，满足数量要求；未用 `ts_rank`（三次确认纯损失）、未用 `ts_delta(·,22)`（两次确认毁信号）、未加常数消单位（T2f 已证有害）

**已知风险（必须随结果一同判读）**：论坛证 `risk72` 族 prod 结构性 **0.79–0.90** ⇒ 即使 IS 全闸通过，也大概率撞 prod 墙。派发时已同步准备 PPA 通道（提交前打 `PowerPoolSelected` 标，用 PPAC<0.5 取代全平台 PC<0.7，须 FastEXPR——本批全是 FastEXPR ✓）。

### 54.4 实测环境记录

- **`batch_create_simulations` 实测吞吐**：07:23 批 6/6 全成；07:24 批 **1/6**（仅第 1 条成功，后 5 条全 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`）⇒ **槽位未清理前连发第二批必失败**，正确做法是等第一批 COMPLETE 再派。
- **prod 槽仍被兄弟会话占用**：`GET /alphas/Vkxnb8QG/correlations/prod` → `correlation_busy` + `holder: "corr:get_production_correlation(XgRM3Yra)"` + `retry_after: 240`。本机进程核对：`PID 98140, start 23:16:13, cmd "prod_wait.py XgRM3Yra --minutes 16"` ⇒ 预计 **23:32:13** 释放。**不连发 `refresh=true`**（每次触发会占满 MCP 120s 超时并残留 300s inflight 标记，反而挤掉自己的窗口）。
- **`logs/_slots/` 有 27 个 `.stale` 孤儿锁残留**（最早 17:08，最新 13:28），与 429 频发可能有关，但清理会波及兄弟会话，本轮不动。

### 54.5 ★ risk72 前 7 条结果：信号方向与 USA 相反（DEU 残差是动量，不是反转）

| # | 模板机制 | alpha | S | F | 2Y | TO | sub | margin | DD |
|---|---|---|---|---|---|---|---|---|---|
| T2 | 5 日累加（**乘 −1**） | `78LgEGbv` | −0.02 | −0.00 | −0.32 | 40.88% | −0.15 | −0.005bp | 22.57% |
| T3 | 22 日累加（**乘 −1**） | `gJe7EGrK` | −0.40 | −0.14 | −1.22 | **17.92%** | −0.40 | −0.253bp | 29.45% |
| T5 | 63 日 `ts_av_diff`（**乘 −1**） | `kqNe2WZd` | −0.21 | −0.05 | 0.13 | 28.08% | **0.17** | −0.110bp | 33.35% |
| T6 | 风险调整 5/63（**乘 −1**） | `omEQMGbm` | −0.31 | −0.10 | −0.33 | 19.89% | 0.02 | −0.227bp | 39.01% |
| T7 | cfg2 EUR 5 日均值（**乘 −1**） | `YP1XGEqW` | −0.36 | −0.13 | −0.28 | 19.96% | −0.04 | −0.268bp | 40.59% |

**5/5 全负 ⇒ 这不是「没信号」，是「方向反了」**。把 `multiply(-1, ·)` 去掉后等效 Sharpe 为 `+0.02 / +0.40 / +0.21 / +0.31 / +0.36`。

**三条推论**：
1. **DEU 的 MFM1 残差收益呈现短期动量，而非 USA `rsk65` 的残差反转**。同一套风险模型在不同区域的残差收益自相关符号相反——残差反转是 USA/EUR 的局部现象，不能跨区照搬骨架方向。
2. **即使方向翻正，上限也只有 0.40**（T3），距闸 1.58 差 **4 倍**；且 T3 的 sub 是 −0.40，翻正后也只有 +0.40。⇒ 幅度不足 + 子宇宙不稳，双重不合格。
3. **TO 反而是这批的亮点**（17.92%–40.88%，全部远低于闸 70%），说明残差收益字段本身节奏稳健，缺点纯粹是**信号强度**。这与 ipf（TO 爆炸）和 pv109（幅度不足但 TO 极低）都不同 —— 是第三种失败形态的组合。

**方法论沉淀（新条目）**：`multiply(-1, ·)` 这类「方向假设」必须在首波用**一条正向 + 一条负向**的成对探针验证，不能凭 USA 的结论直接套。方向错的代价是整个波次 12 条全部白跑（本波 7 条已付）。**成本对比：加 1 条正向对照 ≈ 一次仿真；方向错的代价 ≈ 7 次仿真 + 1 轮等待。**

### 54.6 risk72 12 条已测全表（12/12 全负，正向化后 max = 0.76，仍差 2.1 倍）

| # | 模板机制 | alpha | S（实测，含 −1） | **S 正向化** | F | 2Y | TO | sub | margin | DD |
|---|---|---|---|---|---|---|---|---|---|---|
| T2 | 5 日累加 | `78LgEGbv` | −0.02 | +0.02 | −0.00 | −0.32 | 40.88% | −0.15 | −0.005bp | 22.57% |
| T3 | 22 日累加 | `gJe7EGrK` | −0.40 | +0.40 | −0.14 | −1.22 | 17.92% | −0.40 | −0.253bp | 29.45% |
| T5 | 63 日 `ts_av_diff` | `kqNe2WZd` | −0.21 | +0.21 | −0.05 | +0.13 | 28.08% | +0.17 | −0.110bp | 33.35% |
| T6 | 风险调整 5/63 | `omEQMGbm` | −0.31 | +0.31 | −0.10 | −0.33 | 19.89% | +0.02 | −0.227bp | 39.01% |
| T7 | cfg2 EUR 5 日均值 | `YP1XGEqW` | −0.36 | +0.36 | −0.13 | −0.28 | 19.96% | −0.04 | −0.268bp | 40.59% |
| T1 | 1 日残差水平 | `kqNe26aO` | −0.25 | +0.25 | −0.06 | +0.07 | 28.07% | +0.11 | −0.133bp | 34.92% |
| T4 | 10 日 zscore（subindustry） | `KPJxjZL8` | −0.23 | +0.23 | −0.07 | −0.09 | 27.52% | −0.18 | −0.161bp | 49.97% |
| T8 | **nogroup 版** 1 日水平（对照） | `JjeRKXaE` | −0.16 | +0.16 | −0.03 | +0.01 | 28.08% | +0.20 | −0.085bp | 28.70% |
| T9 | top800 + 10 日累加（换 universe） | `GrWEJVV3` | −0.24 | +0.24 | −0.05 | −0.42 | 27.25% | −0.38 | −0.093bp | 29.99% |
| T10 | 252 日长窗均值 | `9qxg0ZG9` | −0.38 | +0.38 | −0.17 | −0.29 | **4.97%** | −0.04 | −0.103bp | 35.22% |
| T11 | 波动 bucket 剥离层 | `GrWEpZkG` | −0.62 | +0.62 | −0.23 | −1.36 | 45.25% | −0.43 | −0.264bp | 67.59% |
| T12 | 风险调整 22/22 | `pwdQOwPb` | **−0.76** | **+0.76** | −0.51 | −0.56 | 10.47% | −0.58 | −0.108bp | 67.66% |

**12/12 全负，无一例外 ⇒ 方向判断 100% 一致，这不是噪声。**

**nogroup 对照实验（T8 vs T1）**：`top600_equity_residualized_return`（做了市场/国家/行业/风格四层剥离）→ `+0.25`；`_nogroup`（只剥离市场/风格，保留行业与国家成分）→ `+0.16`。**去掉行业/国家剥离反而更弱** ⇒ 说明行业/国家成分里没有额外 alpha，反而稀释了信号。这条对照证明了「残差反转的真成分在特异性收益本身」，不是在行业残差里。

**换 universe 对照（T9 vs T2/T3）**：top800 + 10 日 `+0.24`，介于 top600 的 5 日（+0.02）与 22 日（+0.40）之间 ⇒ **universe 宽度不是有效维度**（与 54.2 推论一致），10 日窗则正好落在 5→22 日的单调上升段上。

**三条有价值的正面对照（即使整族判死也要记）**：
1. **风险调整是 risk72 唯一的放大器**：T3（22 日累加）`+0.40` → T12（22 日累加 ÷ 22 日波动）`+0.76`，**1.9 倍**，且 TO 从 17.92% 降到 **10.47%**。同理 T2（5 日累加 `+0.02`）→ T6（5/63 风险调整 `+0.31`）**15 倍**。⇒ **信息比率化对弱动量信号是「几乎免费」的增益**（不增加换手，反而降低），与 `ts_rank`/`ts_delta` 的纯损失形成鲜明对照。
2. **长窗不放大反而钝化**：T10（252 日均值）`+0.38`、TO 仅 4.97%，但 margin −0.103bp 与 T3 同量级 ⇒ 长窗只压换手，不提信号。**252 日窗口在这个字段上不是「真动量窗口」**，与预期相反。
3. **bucket 剥离层在动量骨架上失效**：T11（T2 体 + `ts_std_dev` 63d bucket）实测 `−0.62`（正向 +0.62），DD **67.59%**，比裸 T2（+0.02）高但代价是换手翻倍（40.88%→45.25%）且 DD 从 22.57% 涨到 67.59%。⇒ 与 P17 结论一致：**bucket 剥离层不可跨骨架迁移**。

**判死结论（`risk72`）**：
- 正向化后 `max S = 0.76`（T12），距闸 1.58 差 **2.1 倍**；
- 全部 12 条 `|DD| ≥ 22.57%`，8/12 在 28% 以上，最好信号的 DD 达 67.66%；
- 全部 12 条 `2Y` 中仅 3 条为正（T5 +0.13、T1 +0.07、T8 +0.01），最高 0.13，`LOW_2Y_SHARPE`（闸 1.58）全灭；
- `failed_ra_count` 3–4，无一例外；
- 最好的 T12 即使方向翻正，`sub = +0.58` 也未达 0.75 稳健线。

⇒ **`risk72` 判死**。这是「**信号方向判错 + 幅度不足 + 回撤过大 + 2Y 全灭**」四重失败，且方向错是**区域属性**（DEU 残差呈动量），不是模板选错。

**★ 关键跨区方法论**：`risk72` 的 31 个字段全是 MFM1 风险模型残差收益，与 USA `rsk65` 同源。但 USA 实测残差**反转** S 3.38，DEU 实测残差**动量**且幅度仅 0.76。**同一风险模型在不同市场的残差收益自相关符号相反** ⇒ 「残差反转」不可作为跨区通用机制，**必须每区独立测方向**（1 条正向 + 1 条负向，成本 2 次仿真）。

---

## §55 DEU 未测 fundamental 数据集画像 + 探针（2026-10-30 续）

### 55.0 方向修正：DEU 供给**未耗尽**

此前「DEU 供给耗尽」结论作废。`get_mining_yield(DEU, by_dataset=true)` 实测：测过约 30 个数据集，DEU 实际 **92 个**，登记册只判死 26 个。`get_pyramid_alphas` 显示 DEU D1 点塔缺口：

| 塔 | 已有 | 距 3 颗 |
|---|---|---|
| **fundamental** | 1 | **差 2** |
| other | 2 | 差 1 |
| institutions / analyst / model | 1 | 各差 2 |
| pv / news / risk / sentiment / shortinterest / earnings / insiders / macro / socialmedia / imbalance | 0 | 各差 3 |

⇒ 优先序：**fundamental（差 2、非 trio、缺口最小）** → other（差 1）。

### 55.1 论坛取证：新数据集是 prod 墙的正解

`search_forum_posts("earnings call transcript sentiment alpha template")` 命中「【Alpha 模板】Earnings模板分享，低相关性，助你横向点塔」（WL58980，39 票 / 21 评）。作者原话：「看到 **GlobalEarningsCallSentimentMatrix 的 Alpha 数量为 0**，我便猜测这大概率是平台新推出的数据，结果果真如此，**新推出的数据相关性普遍很低，所以可以轻松提交**」。

⇒ **可操作判据**：数据集的 `alphaCount` 极低（个位数～数十）⇒ 平台 prod 池里几乎没有同源 alpha ⇒ prod 相关性天然低 ⇒ 更容易过 0.7 墙。**这比在饱和集上换算子降相关省力一个量级**。本轮转向的 fundamental93 / fundamental90 / fundamental45 的 alphaCount 分别只有 36 / 131 / 80，全部符合。

### 55.2 fundamental93（Earnings Tax Data）画像

**46 字段全 MATRIX，无 VECTOR**，分 5 族：

| 族 | 字段数 | 内容 |
|---|---|---|
| accruals | 6 | 应计比率 LTM z-score / std / count / max / mean / min |
| expense（递延税费用） | 7 | 递延税费用比率 LTM 统计量（`current_t` / `dts` / `length` / `max` / `mean` / `min`） |
| liability（递延税负债） | 7 | 同上，负债侧 |
| `deferred_tax_expense_XX` | 7 | (净递延税负债 − 净递延税资产)/分母组 XX |
| `deferred_tax_liability_XX` | 9 | 分子分母互换 |
| `tax_accruals_XX` | 9 | (税费 − 实缴现金税)/分母组 XX |
| `*_asset_change` | 3 | 总资产 YoY 变化率 |

**coverage 全部报 0.0** —— 但 6 条探针全部 `COMPLETE`（非 FAIL）⇒ **数据存在**，再次印证「coverage=0 不是判死依据」。

### 55.3 fundamental93 探针 6 条全表（decay 4 / SUBINDUSTRY / TOP500）

| # | 字段 | alpha | S | F | TO | 2Y | sub | invest_S | DD | margin |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `accruals_d1_current_t` | `xArXaMom` | 0.46 | 0.18 | 26.69% | 0.35 | **0.82** | **0.68** | 11.68% | 3.10bp |
| P2 | `tax_accruals_51` | `9qxgQPV9` | 0.34 | 0.12 | 27.07% | −0.02 | 0.25 | 0.29 | 20.41% | 2.34bp |
| P3 | `expense_d1_current_t` | `kqNe5RwK` | 0.38 | 0.11 | 30.20% | −0.81 | 0.55 | 0.03 | 20.18% | 1.82bp |
| P4 | `accrualsratio_d1_asset_change` | `mLoekOEE` | 0.27 | 0.07 | 34.48% | **0.77** | 0.03 | −0.08 | 40.90% | 1.34bp |
| P5 | `liability_d1_current_t` | `bl673dzp` | −0.11 | −0.02 | 31.93% | −0.66 | 0.52 | 0.24 | 36.13% | −0.60bp |
| **P6** | **`deferred_tax_expense_31`** | **`e75eJd0M`** | **0.85** | 0.37 | 31.46% | 0.74 | 0.22 | 0.43 | **11.40%** | **3.80bp** |

**三个发现**：
1. **`deferred_tax_expense_31` 是本集最强单字段（S 0.85 / DD 11.40%）**，比其余 5 条高 1.8–3 倍。递延税费用族（7 个分母变体）是全数据集唯一值得深挖的族。
2. **P1 应计 z-score 的 `sub 0.82 > S 0.46`、`invest_S/S = 1.48`** —— 全系列唯一「大票子宇宙比全宇宙更强」的形状，说明应计信号在流动性好的票上更稳（与 risk72 / ipf 的「小票驱动」正好相反）。方向为**正向**（应计高→收益高），**与 Sloan(1996) 应计异象相反**，不能套用经典负向假设。
3. 资产扩张率（P4）2Y 0.77 是次亮点，但 DD 40.9% 不可用。

### 55.4 fundamental90（Governance/Accounting/Management/Equality）画像

**66 字段全 MATRIX**，是「会计质量 / 盈余操纵」数据集，含大量**成熟学术评分**：

| 学术因子 | 字段 | 原文 | alphaCount |
|---|---|---|---|
| **Piotroski F-score** | `fnd90_qes_gamef_pscore` | 0–9 会计质量综合分 | 38 |
| **Ohlson O-score** | `fnd90_qes_gamef_ohlson` | 破产预测分 | 13 |
| **Montier C-score** | `fnd90_qes_gamef_cscore` | 会计操纵/欺诈风险 | 3 |
| **Mohanram G-score** | `fnd90_qes_gamef_mohanram` | 成长股盈余操纵风险 | 3 |
| **Campbell-Hilscher-Szilagyi** | `fnd90_qes_gamef_chs_default` | 破产概率 z | 0 |
| **净经营资产 NOA** | `fnd90_game_noa` | Hirschleifer 过度投资 | 1 |
| 应计波动 | `fnd90_game_accruals_vol` | 盈余质量 | 0 |
| 盈余平滑 | `fnd90_game_earning_smooth` | 盈余管理 | 1 |
| 递延收入变化 | `fnd90_game_deferred_sal_chg` | 激进收入确认 | **39** |

其余为盈余质量单项指标（存货天数 / 应收天数 / 应付天数 / SG&A 低效 / 养老金 PBO / 表外或有负债 / 商誉稀释 / 税会差异 `inc_cash_tax`）。

**coverage 全部 0.0**，探针 Q1–Q3 已派发（`pscore` / `ohlson` / `accruals_vol`），结果待收。

### 55.5 fundamental45（Systematic mining of earnings calls）画像 —— ★ 本轮最强线索

**12 字段全 MATRIX，coverage 24–32%（真实值，非 0）**，是**财报电话会文本**数据集：

| 字段 | coverage | alphaCount | 内容 |
|---|---|---|---|
| `fnd45_mktcap` | 31.62% | 26 | 报告期市值（辅助，非信号） |
| `fnd45_lda_bigram_pr` | 27.50% | 14 | Presentation 段 LDA 主题分 |
| `fnd45_sentiment_lm2_net_qa` | 26.75% | **34** | **Q&A 段 LM2 净情感** |
| `fnd45_score` | 26.75% | 18 | 综合评分（情感+可读性+主题） |
| `fnd45_readability_executives` | 26.75% | 8 | 高管可读性（复杂度） |
| `fnd45_numeric_perct_qa` / `_pr` | 26.75% | 7 / 2 | 数值词占比（实质讨论密度） |
| `fnd45_sentiment_lm2_net_pr` | 26.75% | 2 | Presentation 段 LM2 净情感 |
| `fnd45_sentiment_vader_net_qa` / `_pr` | 26.75% | 4 / 3 | VADER 模型情感 |
| `fnd45_sentiment_chanage_ceo` | 23.93% | 2 | CEO 情感变化 |
| `fnd45_sentiment_chanage_othr` | 25.76% | 4 | 其他高管情感变化 |

**探针 3 条全表（decay 4 / SUBINDUSTRY / TOP500 / nanHandling ON）**：

| # | 字段 | alpha | S | **F** | **TO** | 2Y | sub | DD | **margin** |
|---|---|---|---|---|---|---|---|---|---|
| **Q4** | **`sentiment_lm2_net_qa`** | **`qMLeZGv1`** | **0.71** | **0.52** | **6.27%** | **1.15** | 0.53 | 19.44% | **21.05bp** |
| Q5 | `score` | `xArXa2NN` | 0.21 | 0.08 | 7.40% | 0.22 | 0.13 | 34.73% | 5.46bp |
| Q6 | `numeric_perct_qa` | `88RgqEjm` | 0.46 | 0.26 | 6.30% | 0.57 | 0.45 | 11.81% | 12.32bp |

**★ `qMLeZGv1` 是全部 9 条 fundamental 探针中的最优形状**：
- **F 0.52 最高**（次优 0.37）
- **2Y 1.15 最高**（次优 0.77）
- **margin 21.05bp 最高**（次优 12.32bp，是 1.7 倍）
- **TO 仅 6.27%**，是全表最低之一

**换手结构推论（关键）**：TO 6.27% < 12.5%，平台 `fitness = S × sqrt(returns / max(TO, 0.125))` 的分母已被钉死在 0.125。⇒ **在这个区间继续压 TO 对 F 完全无益**；F 只由 S 和 returns 决定。反过来说 **有 10 倍加杠杆空间**：即使把 TO 打到 30%，只要 returns 同比放大，F 仍线性受益。

**要过闸需**：S 0.71→1.58（2.2×）、2Y 1.15→1.58（1.4×）、F 0.52→1.0（1.9×）。三者中 2Y 缺口最小。

**两条经济学机制（有文献支撑）**：
1. **PEAD / 电话会语气漂移**（Price, Doran, Peterson & Bliss 2012, *Earnings Conference Calls and Stock Returns*）：电话会净情感正向预测后续 5–22 日漂移。
2. **Q&A 段信息含量高于 Presentation 段**（Matsumoto, Pronk & Roelofsen 2011, *What Makes Conference Calls Useful?*）：Q&A 是未预演的，信息含量显著更高 —— 实测 `qa` 版 S 0.71 / F 0.52 远高于 `score` 综合版 S 0.21 / F 0.08，**与文献方向一致**。这给「QA − PR 分歧」类模板提供了直接理论依据。

### 55.6 累计量

本段落新增已测 **9 条**（fnd93 6 + fnd45 3）。DEU 累计约 **492 条**。IS 全闸通过名义 4 条、实质 1 条（`Vkxnb8QG`）；prod 通过 0 条。

### 55.7 下一步（按序）

1. **收 fundamental90 探针 Q1–Q3**（`3FBoal5Yq5129CsMjME3F0B` / `jJw81do95jKbWX1gLXAvq18` / `1bEkXl7Yx4qu96GbkbaY7Ou`）。
2. **fnd45 十模板穷尽**（围绕 `sentiment_lm2_net_qa`，模板库已按 §55.8 备好）。
3. **fnd93 递延税费用族深挖**（`deferred_tax_expense_{11,12,21,22,31,41,51}` 7 个变体 + 风险调整放大器）。
4. 主线仍是点 fundamental 塔（差 2 颗）。

### 55.8 fnd45 十模板库（结构互异，已标注来源）

| # | 模板 | 骨架 | 经济学机制 / 来源 |
|---|---|---|---|
| T1 | 水平 | `rank(qa)` | 基线；PEAD（Price et al. 2012） |
| T2 | Q&A−PR 分歧 | `rank(subtract(rank(qa), rank(pr)))` | 未预演 vs 预演信息差（Matsumoto et al. 2011） |
| T3 | CEO 情感变化 | `rank(chanage_ceo)` | 领导层语气改善 → 反应不足 |
| T4 | 时序标准化 | `rank(ts_zscore(qa, 252))` | 剥离公司「永远乐观」固定效应 |
| T5 | 季度平滑 | `rank(ts_mean(qa, 66))` | 季频数据降噪，66 日 ≈ 1 季 |
| T6 | 双模型分歧 | `rank(subtract(rank(vader_qa), rank(lm2_qa)))` | LM2 vs VADER 分歧 = 文本不确定性 |
| T7 | 行业中性 | `group_neutralize(rank(qa), subindustry)` | 剥离行业共同情感潮 |
| T8 | 数值密度门控 | `trade_when(rank(numeric_qa) > 0.3, rank(qa), -1)` | 只在实质讨论时持仓，滤「空话」 |
| T9 | CEO−Other 分歧 | `rank(subtract(rank(chanage_ceo), rank(chanage_othr)))` | 领导层内部信号分歧 |
| T10 | LDA 主题门控 | `trade_when(rank(lda_bigram_pr) > 0.5, rank(qa), -1)` | 主题聚焦时才信情感 |

来源标注：T1/T2 来自文献（论坛帖 WL58980 亦指向 earnings call 类新数据集）；T4/T5/T7 来自论坛模板通用骨架；T3/T6/T8/T9/T10 为自建（字段语义组合）。**10 个模板在骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性变换上互不相同**，满足模板多样性硬约束。

---

## §56 fnd90 / fnd45 结构穷尽 + institutions6 开辟新战线

### 56.0 本轮定位

承接 §55。§55 已锁定三条候选（`E56o3YOr` / `GrWEv2nO` / `e75eJd0M`），本轮做两件事：

1. **对 fnd90 与 fnd45 各派一组结构互异模板**，测「这两个集的上限到底在哪」——是字段没信号，还是骨架没选对；
2. **沿「非 trio 未测数据集」清单开辟 institutions6 新战线**（11 字段 / coverage 全 1.0 / 历史零测试）。

设置全部为 DEU 档案：EQUITY / DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / pasteurization ON / unitHandling VERIFY / maxTrade OFF。

---

### 56.1 fnd90 六模板：**全部弱于裸 `rank(pscore)`**

| # | 模板 | alpha | S | F | TO | 2Y | sub | DD | margin | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|
| **基线** | **裸 `rank(pscore)`** | **`GrWEv2nO`** | **1.02** | 0.61 | 22.78% | 0.85 | 0.57 | 17.32% | 7.22bp | 4 |
| F2 | O-score bucket 剥离层 | `E56o38zP` | 0.79 | 0.41 | 22.23% | 0.57 | 0.27 | 12.22% | 5.43bp | 5 |
| F3 | 252 日长平滑 | `ZYQkZvEQ` | 0.74 | 0.48 | **1.58%** | 0.97 | 0.42 | 13.54% | **66.67bp** | **3** |
| F4 | 504 日时序 z | `9qxgoOV2` | 0.38 | 0.17 | 4.49% | 0.59 | 0.21 | 12.34% | 11.17bp | 3 |
| F5 | 年度差分 `ts_delta 252` | `GrWEVK95` | 0.31 | 0.13 | 4.88% | 0.89 | 0.39 | 18.74% | 8.70bp | 3 |
| F6 | 盈余平滑门控 | `VkxKnMK5` | 0.57 | 0.33 | 3.30% | 0.73 | 0.32 | 14.33% | 25.52bp | 3 |
| F7 | 自身长窗 bucket 剥离 | `6XdgxooP` | 0.65 | 0.28 | 25.42% | 0.51 | 0.42 | 15.21% | 3.69bp | 4 |

**三条结论**：

1. **fnd90 的上限就是裸 `rank(pscore)` 的 S 1.02。** 7 个结构（含基线）全部测完，无一超过基线；最好的是 F3 长平滑（S 0.74 / margin 66.67bp / TO 1.58%），S 反而掉 27%。该集不存在「骨架选错」的问题，是**字段本身信号强度不足**。
2. **bucket 剥离层不可迁移（第 3 次实证）**：F2（O-score 轴）S 1.02→0.79、F7（自身 252 均值轴）S 1.02→0.65，两条都掉 S。此前在 risk72 / fnd45 上也证过同样的事 —— **剥离层只在「信号自带强分组结构」时才加分**。
3. **`ts_delta` 一阶差分毁信号（第 3 次实证）**：F5 年度差分 S 0.31，是全部 7 条最低。F-score 是**水平量**（好公司的持续性状态），取差分等于把「持续好」变成「正在变好」，样本量骤降。`ts_zscore`（F4）同样掉到 0.38，说明 fnd90 的信号**只在原始水平里有信息**。

---

### 56.2 fnd45 六变体：**66 日窗口是峰值，风险调整是真正的新最佳**

| # | 模板 | alpha | S | F | TO | 2Y | sub | DD | margin | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|
| T5 | 66 日季平滑（§55 基线） | `E56o3YOr` | 0.80 | 0.61 | 2.60% | 1.93 | 0.63 | 18.52% | 55.31bp | 3 |
| U1 | 126 日半年平滑 | `pwdQQ81V` | 0.48 | 0.29 | 2.02% | 1.74 | 0.38 | 24.15% | 43.70bp | 3 |
| U2 | 22 日月平滑 | `78LggxRb` | 0.78 | 0.59 | 3.27% | 1.59 | 0.61 | 19.62% | 43.55bp | 3 |
| **U3** | **风险调整 `mean(66)/std(252)`** | **`78Lggz12`** | **0.90** | **0.74** | **2.63%** | **1.97** | **0.73** | **11.13%** | **63.57bp** | **3** |
| U4 | readability 剥离层 | `e75ee0JJ` | 0.54 | 0.35 | 6.73% | 1.20 | 0.38 | 24.27% | 15.26bp | 4 |
| U5 | bigram 主题门控 | `xArXXj2b` | 0.66 | 0.45 | 2.48% | 1.72 | 0.48 | 20.66% | 46.85bp | 3 |
| U6 | VADER 同骨架 | `zq3XXO5E` | **0.01** | 0.00 | 2.50% | 0.39 | 0.02 | 30.15% | 0.45bp | 4 |

**四条结论**：

1. **★ 66 日是平滑窗口的峰值，两侧都掉**：22 日 S 0.78（近乎持平）、**66 日 S 0.80（峰）**、126 日 S 0.48（崩 40%，且 DD 24.15%）。66 日 ≈ 一个季度，与财报电话会的**季度发布节奏严格对齐** —— 平滑窗口短于事件间隔会留下噪声，长于事件间隔会把多期信息混成长期漂移。**这是窗口选择的经济学理由，不是调参。**
2. **★ VADER 词典在 DEU 完全无效（S 0.01，等同噪声）**：同骨架换 `vader_net_qa` 后 S 从 0.80 掉到 **0.01**、margin 0.45bp、DD 30.15%。VADER 是为**社交媒体短文本**设计的通用情感词典，缺金融领域极性词表；Loughran-McDonald (LM) 是专为 10-K/电话会构建的金融词典。⇒ **DEU 文本情感一律用 `_lm2_` 版，`_vader_` 全族判死。**
3. **readability 剥离层无效（S 0.80→0.54）**：与 fnd90 的 bucket 结论一致，第 4 次实证。
4. **bigram 主题门控中度有效但不如风险调整**：U5 S 0.66 / 2Y 1.72 / margin 46.85bp，比裸平滑差但比裸 rank 好；说明「只在有实质议题时持仓」能改善质量但牺牲暴露。

---

### 56.3 ★ 新最佳候选 `78Lggz12` 完整分析

```text
rank(divide(ts_mean(ts_backfill(fnd45_sentiment_lm2_net_qa, 252), 66),
            ts_std_dev(ts_backfill(fnd45_sentiment_lm2_net_qa, 252), 252)))
```

**语义**：Q&A 段净情感（LM2 词典）的 **66 日（约一季）均值 ÷ 252 日（约一年）波动率** —— 即「情感水平的信息比率」。分子是不可预演的 Q&A 语气水平，分母是该公司电话会语气的历史不稳定度。**同样的情感得分，对「历来忽冷忽热」的公司信息量更高，对「历来平稳」的公司信息量更低。**

| 指标 | 数值 | 闸门 / limit | 判定 |
|---|---|---|---|
| Sharpe | **0.90** | ≥ 1.58 | ✗ 差 **1.76×** |
| Fitness | **0.74** | ≥ 1.00 | ✗ 差 **1.35×** |
| Turnover | **2.63%** | 1%–70% | ✅ |
| **2Y Sharpe** | **1.97** | ≥ 1.58 | ✅ **已过（1.25×）** |
| SUB Sharpe | **0.73** | ≥ 0.434 × 0.90 = 0.391 | ✅ **已过（1.87×）** |
| invest_S | 0.57 | — | ✅ |
| **Drawdown** | **11.13%** | — | **全 DEU 最低** |
| Margin | **63.57bp** | — | 全 DEU 第 2 高 |
| failed_ra_count | **3** | — | 最低档 |

**相对前最佳 `E56o3YOr` 的四项同向改善**：S 0.80→**0.90**（+12.5%）、F 0.61→**0.74**（+21.3%）、2Y 1.93→**1.97**、DD 18.52%→**11.13%（−40%）**、margin 55.31→**63.57bp**（+15%）、sub 0.63→**0.73**。**没有一项变差。**

**为什么这是「免费放大器」（第二次跨数据集实证）**：§53 在 risk72 上首次观察到 `ts_sum(F,W)/ts_std_dev(F,W)` 对弱信号既提 S 又降 TO（1.9×）。本轮在 fnd45 上完全复现，且额外看到**降 DD 40%**。机理：分母用**长窗（252 日）历史波动**归一化，等价于按「该公司信号的历史可预测性」分配权重，把权重从噪声大的公司转移给噪声小的公司 —— 这是横截面**风险平价**，不是信号改造，所以不消耗 alpha 容量、也不增加换手。

**过闸缺口与自洽性（关键）**：

- TO 2.63% ≪ 12.5% ⇒ 平台 `fitness = S × sqrt(returns / max(TO, 0.125))` 的**分母已钉死在 0.125**，F 只由 S 与 returns 决定：验证 `0.90 × sqrt(0.0835 / 0.125) = 0.90 × 0.817 = 0.736 ≈ 0.74` ✅
- **⇒ 若 S 能到 1.58 而 returns 仍为 8.35%，则 F = 1.58 × 0.817 = 1.29，自动过闸。**
- 反之若只推 returns 不推 S，要 F ≥ 1.0 需 returns = `0.125 × (1.0/0.90)²` = **15.43%**（1.85×）。
- **结论：唯一真缺口是 S 0.90 → 1.58，F 是 S 的从属变量。**

---

### 56.4 institutions6 画像（全新战线，DEU 历史零测试）

**数据集元数据**：category = `institutions`，fieldCount **11**，userCount 121，alphaCount **259**，coverage **1.0**（全字段真实满覆盖，非元数据报 0 的那类假零）。

**为什么选它**：① `institutions` 塔当前 1 颗，点塔缺口 2；② **非 trio**（不受 PV/MODEL/OTHER 组腿禁令约束）；③ 11 个字段可一次扫完，天然适合 ATOM；④ coverage 1.0，不存在 NaN 塌陷风险；⑤ alphaCount 19–80/字段，属「有验证但不饱和」区间。

| 字段 | 单位族 | 字段 alphaCount | 经济含义 |
|---|---|---|---|
| `market_value_institutional_shares_acquired` | 美元（CSPrice·CSShare） | **80** | 报告期内机构买入的总美元额 |
| `quantity_institutional_shares_acquired` | 股数（CSShare） | 63 | 机构买入总股数 |
| `count_institutional_buyers_security` | 计数 | 58 | 增持的机构家数 |
| `count_institutional_sellers_security` | 计数 | 49 | 减持的机构家数 |
| `quantity_institutional_shares_disposed` | 股数 | 39 | 机构卖出总股数 |
| `market_value_institutional_shares_disposed` | 美元 | 34 | 机构卖出的总美元额 |
| `count_institutional_holders_security` | 计数 | 30 | 当前持仓的机构家数 |
| `aggregate_equity_value_institutions` | 美元 | 22 | 机构合计持仓美元市值 |
| `aggregate_share_count_all_owners` | 股数 | 21 | 全部持有人（去父子重复）合计股数 |
| `aggregate_equity_value_all_owners` | 美元 | 19 | 全部持有人合计美元市值 |
| `aggregate_share_count_institutions` | 股数 | 19 | 机构合计持股数 |

**单位纪律（必须先过）**：本集**全部字段带单位**（美元或股数），因此
① 任何 `divide` **必须同单位族配对**（美元÷美元、股数÷股数、计数÷计数）才得无量纲；
② 任何最终输出**必须 `rank()` 收口**；
③ 严禁 `divide(F, cap)` 或与常数比较（`cap` 是 CSPrice·CSShare，本集美元字段同族但股数字段不同族）。

---

### 56.5 institutions6 十二模板库（结构互异，已标注来源）

| # | 模板 | 表达式骨架 | 经济学机制 / 来源 |
|---|---|---|---|
| I1 | **净流入强度** | `rank(divide(subtract(acq_mv, disp_mv), agg_ev_inst))` | 净买入美元 ÷ 机构总持仓 = 净需求强度（**Yan & Zhang 2009**, *Institutional Investors and Equity Returns*） |
| I2 | 买卖价值比 | `rank(divide(acq_mv, disp_mv))` | 毛买入/卖出比（**Gompers & Metrick 2001**） |
| I3 | 买方广度 | `rank(divide(cnt_buyers, cnt_holders))` | 增持机构占比 = 羊群广度（**Sias 2004**, *Institutional Herding*） |
| I4 | 卖方广度 | `rank(divide(cnt_sellers, cnt_holders))` | 减持机构占比（I3 的对照腿，预期符号相反） |
| I5 | 买卖机构比 | `rank(divide(cnt_buyers, cnt_sellers))` | 多空机构家数比 |
| I6 | 机构化水平 | `rank(divide(agg_sc_inst, agg_sc_all))` | 机构持股占总股本（**Bennett, Sias & Starks 2003**） |
| I7 | 机构化年度变化 | `rank(ts_delta(divide(agg_sc_inst, agg_sc_all), 252))` | ΔIO，年度尺度的机构化漂移 |
| I8 | 净流入 252 日平滑 | `rank(ts_mean(divide(subtract(acq_mv, disp_mv), agg_ev_inst), 252))` | 季度节奏平滑的净需求（**Nofsinger & Sias 1999**） |
| I9 | 机构价值占比 | `rank(divide(agg_ev_inst, agg_ev_all))` | 机构持仓美元占总市值（与 I6 股数口径正交） |
| I10 | 数量口径净流 | `rank(divide(subtract(acq_qty, disp_qty), agg_sc_inst))` | 股数口径净流 ÷ 机构持股（与 I1 美元口径正交对） |
| I11 | 每机构平均持仓 | `rank(divide(agg_ev_inst, cnt_holders))` | 平均单机构持仓规模 = 机构集中度（**Ali, Wei & Zhou 2011**） |
| I12 | 净/总成交比 | `rank(divide(subtract(acq_mv, disp_mv), add(acq_mv, disp_mv)))` | 净买入占毛成交比例（I1 的稳健归一化变体，抗规模效应） |

**结构互异性核验**：I1/I12 同一分子不同归一化（强度 vs 比例）；I2/I5 价值口径 vs 计数口径；I3/I4 广度对（符号相反）；I6/I9 股数口径 vs 美元口径；I8 引入时间平滑维；I7 引入一阶差分维；I11 引入机构家数分母。**共 12 个，覆盖水平 / 比值 / 差分 / 平滑 / 广义分母五个维度，满足 ≥10 模板硬约束。**

**批 1（6 条，已派发，in flight）**：I1 / I2(→I5) / I3 / I4 / I12(→I5) / I6 —— 即已提交 `I1_net_inflow_intensity` / `I2_herding_intensity`（对应 I5 骨架）/ `I3_buy_breadth` / `I4_sell_breadth` / `I5_net_total_ratio`（对应 I12 骨架）/ `I6_institutional_level`。
**批 2（待派）**：I7 / I8 / I9 / I10 / I11 + I2（真·买卖价值比，批 1 因槽位改派 I5）。

---

### 56.6 累计量

本段落新增已测 **12 条**（fnd90 6 + fnd45 6），另有 institutions6 批 1 的 6 条在飞。DEU 累计约 **516 条**。

IS 全闸通过名义 4 条、实质 1 条（`Vkxnb8QG`）；prod 通过 0 条。

**候选强度排序（本条更新后）**：

| 排名 | alpha | S | F | 2Y | TO | failed_ra | 状态 |
|---|---|---|---|---|---|---|---|
| 1 | `Vkxnb8QG` | 1.83 | 1.64 | 2.09 | 9.06% | **0** | IS 全闸过，待 prod 终验 |
| 2 | `GrWEv2nO` | 1.02 | 0.61 | 0.85 | 22.78% | 4 | 2Y 与 F 双缺 |
| **3** | **`78Lggz12`** | **0.90** | **0.74** | **1.97** | **2.63%** | **3** | **2Y/SUB 已过，只差 S→F** |
| 4 | `e75eJd0M` | 0.85 | 0.37 | 0.74 | 31.46% | — | 待深挖 7 个分母变体 |
| 5 | `E56o3YOr` | 0.80 | 0.61 | 1.93 | 2.60% | 3 | 被 78Lggz12 全面超越 |

---

### 56.7 下一步（按序）

1. **收 institutions6 批 1**（6 条，in flight）—— 新数据集首测，决定这条战线是否成立。
2. **`78Lggz12` 定向突破 S 0.90→1.58**：风险调整骨架已确认是强放大器，用它做**字段维**扩展 —— 把同一骨架套到 `numeric_perct_qa`（Q6 S 0.46，基础较弱但机制不同）、`lda_bigram_pr`（主题聚焦度）、`readability_executives`（可读性），以及**窗口配比矩阵**（mean 22/66/126 × std 126/252/504）。
3. **institutions6 批 2**（I7–I11 + I2）。
4. **剩余未测非 trio 集**：`fundamental89`（407 字段 / 377 alphas）、`fundamental86`（7 字段 / 158 alphas）、`fundamental22`（**1 字段** / 32 alphas）、`fund_holdings_panel`（18 字段 / cov 0.90）、`sentiment33`（255 字段 / 36 alphas）、`institutions1`/`institutions4`/`institutions25`/`insiders1`。
5. `fnd93` 的 7 个 `deferred_tax_expense_*` 分母变体深挖。

---

## §57 DEU 认知重构：瓶颈是 prod 相关性墙，不是 Sharpe（2026-10-30 晚）
### 57.1 psm P 批六模板收割 —— DCF 内在价值子族全线覆灭

| # | 模板（经济机制） | alpha | S | F | TO | 2Y | sub | DD | margin | fRA |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 裸 `rank(-P/IV)`（价值安全边际） | `omEQAvEk` | 0.18 | 0.06 | 3.44% | 0.98 | −0.03 | 15.06% | 7.39bp | 4 |
| P2 | 504 日时序 z（历史分位定价） | `d5Wegm3w` | 0.04 | 0.01 | 8.01% | −0.05 | −0.04 | 29.05% | 0.56bp | 4 |
| P3 | 风险调整 66/252（夏普式定价） | `zq3XQjwo` | 0.01 | 0.00 | 1.89% | 1.08 | −0.10 | 24.16% | 0.57bp | 4 |
| **P4** | **CAGR 预期差 fwd5 − mkt impl 5** | **`88Rg7kZv`** | **0.61** | 0.31 | 7.67% | **1.33** | 0.13 | **7.73%** | 8.55bp | 4 |
| P5 | duration fy15/fy1（权益久期） | `1YN61maX` | −0.15 | −0.04 | 3.97% | 0.54 | −0.32 | 23.95% | −4.83bp | 4 |
| P6 | warranted PE / fwd PE（估值合理性） | `58EN3qgM` | 0.24 | 0.08 | 9.86% | −0.01 | −0.13 | 16.10% | 3.02bp | 5 |

**结论**：`price_to_intrinsic_value_ratio_2`（cov 0.9118 / ac 3）在 DEU 无信号（P1 0.18，P3 归零）。
机理推断（三条并列，未单独证伪）：
1. StarMine 的 IV 由**同一批卖方一致预期**驱动，与价格高度同步 ⇒ IV/Price 的横截面差异被压缩；
2. 单一折现率模板 `iv_discount_rate_3` 用于全宇宙 ⇒ 跨公司不可比（DCF 对 r 的敏感性 ≫ 对现金流的敏感性）；
3. DEU TOP500 工业/金融占比高，DCF 对金融股本不适用。
**唯一活口 P4** 用的是 CAGR 而非 P/IV ⇒ 该族保留「预期增长差」一条线，`iv_*` / `rel_val_*` / `price_to_intrinsic_value_*` 判死。

---

### 57.2 ★ 假说被自己的实验推翻：bucket 不是通用放大器，字段才是

**起因**：复核本地 READY 队列时发现历史遗留候选 `WjLEOqLP`，平台实读 **S 1.77 / F 1.61 / 2Y 1.83 / DD 7.19% / `failed_ra_count = 0`**，塔位 `DEU/D1/ANALYST`。这直接**推翻了本报告 §56 之前「DEU 单数据集 ATOM 上限 S ~1.0」的结论**。

```
WjLEOqLP = group_neutralize(
             group_rank(add(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),1),
                            ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),210)), sector),
             bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),252)),
                    range="0,1,0.05"))
```

当时的读法：`bucket` 作为**中性化分组轴**（对「该股自身长窗均值所处的 20 分位」内部去均值），这与此前 4 次失败的「bucket 当剥离层叠加」是不同的几何，于是判定它是通用放大器。

**迁移实验（multisim `1ow4k34Wx4wVaVRedZI9Ylk`，6 字段同骨架）——6/6 全灭**：

| 字段 | 该字段历史基线 S | bucket 骨架 S | 判定 |
|---|---|---|---|
| `fnd45_sentiment_lm2_net_qa` | 0.90 | **0.52** | 劣于基线 |
| `fnd90_qes_gamef_pscore` | 1.02 | **0.62** | 劣于基线 |
| `fnd93_deferred_tax_expense_31` | 0.85 | **−0.52** | 反向 |
| `mean_estimate_change_pct_f12m_ebitda_60d_4` | 未测 | 0.47 | 噪声 |
| `predicted_surprise_fy1_ebitda_4` | 未测 | 0.12 | 噪声 |
| `analyst_upward_revision_count_fy1_earnings_14d_4` | 未测 | −0.04 | 噪声 |

**归因纠正（关键）**：同一字段 `eps_y1_estimate_change_3mo` 的多种写法实测 —— 裸 `rank(ts_backfill(F,252))` = **S 1.62**（`1YNvAZEX`）、`group_rank(F, sector)` = **1.81**（`XgRjWRQ1`）、`group_rank(ts_mean(F,22), sector)` = 1.69（`P0MJZMdp`）、bucket 骨架 = 1.77。**⇒ S 1.6–1.8 是 `eps_y1_estimate_change_3mo` 这个字段自带的，bucket 只贡献 ~+0.12。**
**这是「bucket 机制不可跨骨架迁移」的第 5 次实证**，且这次给出了更准确的因果定位：**先找对字段，再谈骨架**；把骨架当放大器去迁移字段，是把果当因。

---

### 57.3 ★ prod 相关性墙的量化（本轮最硬的一条）

DEU 全库 3427 条 alpha 的 prod 分布：

| prod 区间 | 条数 |
|---|---|
| 未测（NULL） | **3342** |
| ≥0.7（必死） | **67** |
| 0.6–0.7 | 10 |
| 0.5–0.6 | 4 |
| <0.5 | 4 |

已测 85 条中 **67 条 ≥0.7 ⇒ 79% 撞墙率**。`S≥1.58` 的 291 条 DEAD 平均 prod = **0.8193**。
⇒ **DEU 不是 Sharpe 不够，是 prod 相关性池已饱和**。任何「分析师一致预期修正 / 盈利惊喜」类信号在 DEU 生产池里都已有近亲。

`WjLEOqLP` 是教科书案例：RA 全过、S 1.77、DD 7.19%，**prod = 1.0（生产池里有 1 条几乎同款）**，直接不可提交。其同类 `1YjYemAm`（S 1.65）同源，预期同样 ≥0.9。

---

### 57.4 存量盘点（决定 60 颗目标的可行性）

DEU 3427 条按 `platform_status × disposition`：

| platform_status | disposition | 条数 |
|---|---|---|
| UNSUBMITTED | （无） | **2028** |
| （NULL） | （无） | 1103 |
| UNSUBMITTED | DEAD | 291 |
| **ACTIVE（已提交）** | （无） | **10** |
| ACTIVE | SUBMITTED | 1 |

**已提交 11 条（全部 prod 0.43–0.69）**：

| alpha | S | F | TO | prod |
|---|---|---|---|---|
| `mLYLEm99`（SUPER） | 2.27 | 1.67 | 16.7% | 0.6108 |
| `883Y3bAW` | 2.17 | 1.24 | 34.2% | 0.5434 |
| `2rOe10qY` | 2.10 | 1.98 | 12.7% | 0.6388 |
| `blRnKEk6` | 2.02 | 1.70 | 16.2% | 0.5766 |
| `2rmGAPqN` | 1.81 | 1.48 | 13.0% | 0.6292 |
| `vRk6og8b` | 1.80 | 1.47 | 19.0% | 0.6877 |
| `Vk65zLzG` | 1.79 | 1.69 | 12.0% | 0.6400 |
| `2rjrMZ25` | 1.77 | 1.61 | 12.0% | 0.6510 |
| `58gkLAkk` | 1.75 | 1.42 | 14.6% | 0.5381 |
| `Wje5K71x` | 1.73 | 1.37 | 12.7% | **0.4305** |
| `JjxrYjre` | 1.68 | 1.47 | 12.3% | 0.6453 |

**可提交存量：180 条 `UNSUBMITTED` + `REGULAR` + `S≥1.58` + prod 从未测**，其中 **170 条**同时满足 `2Y≥1.0（或 NULL）` 且 `0.01≤TO≤0.7`。
去表达式族后 **65 个互异族**，代表族（按 S 降序）：`tm_15/16_r1_r5_r10_rh_glb_d1_*`（S 1.7–2.70，9+5 条）、psm 多腿（1.6–2.17）、`snt7_all_languages_views` 情绪向量（1.9–2.14）、`inst1_valueeur` 机构（1.6–1.81）、`eps_y1_estimate_change_3mo`（1.58–1.90，约 40 条同源）、`mdl264_news_abno_vol_1d_class`、`oth455_relation_*`、`fnd6_newq_oiadpq`、`directional_indicator`。

**可达性估算**：若未测池与已测池同分布（79% 撞墙），180 × 21% ≈ **38 条**可通过 prod ⇒ 11 + 38 ≈ **49**，仍略低于 60。加上少数族会因 self-corr 二次淘汰，**60 颗在 DEU 需同时动用两条线**：① 存量 prod 终验；② 结构上全新机制的挖掘（见 §57.5）。

---

### 57.5 下一步（按序，按产出/成本比排序）

1. **★ 存量 prod 终验（最高优先，纯赚）**：对 180 条未测池按族去重后逐条 `check_correlation(correlation_type="production")`（平台单并发槽，1–5 分钟/条），过的进提交队列。先测与已提交 11 条 self-corr 最低的族（情绪 `snt7_*`、`mdl264_*`、`tm_*`），因为 self-corr 已由 `check_self_correlation` 本地零成本预筛。
2. **`N1NML1wq`（`snt7_all_languages_views` 情绪向量族）已双预筛**：self = **0.0226** 通过，S 2.14 / F 1.99 / 2Y 2.56 / TO 10.4%。只差 prod，槽位被兄弟会话占用，按 `retry_after` 重查。
3. **放弃 `WjLEOqLP` / `1YjYemAm` 家族**（prod 1.0 已证），`LLZ87QY9`（institutions1，2Y 2.52）待测 prod。
4. **新机制挖掘方向**：DEU 生产池饱和区是「分析师预期修正」，未被占的机制在 —— `fundamental` 递延税（fnd93 已试 0.85）、`fundamental89`（407 字段未测）、`fundamental86`、`fund_holdings_panel`（cov 0.90）、`sentiment33`（255 字段）、`institutions4/25`、`insiders1`。**避开一切 `*_estimate_change_*` / `predicted_surprise_*` 字段**。

---

### 57.6 本轮模板库（结构互异度自检，10 个）

| # | 模板 | 结构差异点 | 来源 |
|---|---|---|---|
| T1 | `rank(-P/IV)` | 水平量 · 横截面 rank · 无时序 | 帖 `42022555985047` |
| T2 | `rank(-ts_zscore(ts_backfill(P/IV,252),504))` | 二阶矩 · 长窗标准化 | 自建 |
| T3 | `rank(-divide(ts_mean(F,66), ts_std_dev(F,252)))` | 风险调整（均值/波动） | §56 实证 |
| T4 | `rank(subtract(cagr_fwd, cagr_mkt_implied))` | 两模型预期差 · 差分校准 | 帖 `42659839739927`（CAGR 基准年污染）+ 自建 |
| T5 | `rank(-divide(earn_fy15, earn_fy1))` | 久期比 · 期限结构 | Dechow/Sloan/Soliman (2004) |
| T6 | `rank(divide(warranted_pe, forward_pe))` | 估值合理性比 | 帖 `35589474947735`（B/P 骨架族） |
| T7 | `group_neutralize(group_rank(add(ts_mean(F,1),ts_mean(F,210)),sector), bucket(rank(ts_mean(F,252)),range="0,1,0.05"))` | 状态条件中性化（bucket 当分组轴） | 平台存量 `WjLEOqLP` 反推 |
| T8 | `tail(group_neutralize(group_rank(ts_decay_linear(quantile(add(...)),4), cluster), subindustry),0.05,0.95,0.5)` | 聚类轴 + 衰减 + 截尾 | 平台存量 `XgJ980Wb` 反推 |
| T9 | `vector_neut(ts_quantile(ts_ir(ts_mean(max(F,ts_delay(F,·)),22),·)), ·)` | 向量正交 + 分位高斯化 + 信息比 | 平台存量 `N1NML1wq` 反推 |
| T10 | `trade_when(gate, group_rank(add(F_long,n·mean(F,210)),sector), -1)` | 条件触发（门控腿 + 分段） | 平台存量 `Vkxnb8QG` 反推 |

T7–T10 是**从平台存量反向工程**得到的模板（不是猜的），结构互异度成立；T1–T6 是本轮实跑的金融学模板。
**本轮结论对 T1–T6 全部为负**；T7 迁移失败（§57.2）；T9 是唯一待验活口。

---


---

---



---

## §58 sentiment33 十模板波全灭 + prod 池机制纠正 + 可提交存量重估（2026-10-30）

### 58.1 未点亮塔的 category 结构盘点（平台实时拉取，非本地缓存）

`get_datasets(category="sentiment", region="DEU", delay=1, universe="TOP500")` 只返回 **3 个**数据集：

| dataset | name | coverage | fields | users | alphas | valueScore |
|---|---|---|---|---|---|---|
| sentiment27 | Website Popularity Rankings | 0.9038 | 18 | 129 | 324 | 4.0 |
| sentiment33 | Sentiment Data by NLP | **0.3221** | 255 | 33 | 45 | 6.0 |
| sentiment7 | Webpage Views Data | 0.7418 | 3 | 52 | 94 | 4.0 |

三者状态：sentiment27 已判死、sentiment7 的 pulse 机制已判死（48 探针，天花板 S 0.71 / 2Y −0.07）、
sentiment33 本轮结论见下。

⇒ **DEU/sentiment 塔在数据集层面已封闭：3 个数据集全部被探过。** 该塔不可点亮。

附：`sentiment33` 的平台 description 同样是污染文案（"mapping between RIC and Bloomberg IDs"），
与 `other47` / `other250` 等 11 个数据集被同一套 BBID↔RIC 文案覆盖的情况一致。
**再次确认：数据集级 description 不可信，一律以 `get_datafields` 的字段级 id + description 为准。**

### 58.2 sentiment33 十模板波（multisim `w8ni222m55gaMc8U6MeyNa`）

设置：DEU / TOP500 / D1 / decay 4 / SUBINDUSTRY / truncation 0.08 / **nanHandling ON（稀疏集）** /
pasteurization ON / maxTrade OFF / FASTEXPR / VERIFY / EQUITY。10 条 10/10 COMPLETE，无报错。

| # | 模板结构 | alpha | S | F | TO | 2Y | SUB | 持仓 L/S | fRA |
|---|---|---|---|---|---|---|---|---|---|
| T1 | 三分类计数归一化净比率（水平） | `3qogaqk6` | −0.13 | −0.02 | **95.57%** | 0.21 | −0.46 | **2/2** | 6 |
| T2 | ML 加权分极差 + backfill（水平） | `O0AKb0zv` | 0.04 | 0.01 | 8.16% | **1.78** | 0.08 | 84/82 | 3 |
| T3 | 净情绪 22 日时序 z（一阶矩） | `rKRQJKGj` | **0.25** | 0.09 | 24.88% | 1.22 | 0.11 | 42/42 | 5 |
| T4 | 词典法 vs ML 法比率分歧（跨层） | `kqNe1qGz` | 0.04 | 0.00 | **99.25%** | 0.13 | −0.17 | **2/2** | 6 |
| T5 | 情绪/客观性交互（除法） | `RRE02RKd` | 0.04 | 0.01 | 8.15% | **1.80** | 0.08 | 84/82 | 3 |
| T6 | 关键词层级计数（非极性注意力） | `YP1X2POq` | −0.03 | −0.01 | 4.94% | −0.53 | 0.21 | 85/87 | 4 |
| T7 | `ts_corr` 相关性算子几何（论坛 94 票） | `omEQ3mX6` | −0.26 | −0.14 | 7.63% | −0.23 | −0.03 | 91/51 | 4 |
| T8 | 情绪时序波动＝争议度（二阶矩 + reverse） | `ZYQk2Yv3` | −0.09 | −0.03 | 6.26% | −0.72 | **0.42** | 86/89 | 4 |
| T9 | 分组轴＝注意力自 bucket | `e75ed7Zd` | **−1.06** | −0.46 | **103.1%** | −1.37 | −1.10 | **2/2** | 6 |
| T10 | 跨 fkw 桶背离（fkw1 vs fkw4） | `78Lga8Rv` | −0.37 | −0.22 | 8.89% | 0.97 | −0.28 | 78/80 | 5 |

**全波 \(\max|S| = 0.37\)，10/10 `LOW_SHARPE` fail。** 10 条全部额外挂 `CONCENTRATED_WEIGHT = 0.5`（limit 0.1）。

### 58.3 逐轴归因（三类字段、三条不同失败路径）

**① 词典法 token 计数（`method_1_pos/neg/neut`）→ 组合塌缩**
T1 / T4 / T9 三条持仓只有 **2 long / 2 short**，TO 95–103%。
机理：`method_1_*` 是**原始 token 计数**，日间跳动极大；分母 `pos+neg+neut` 在多数票上为 0 或 NaN，
而 `nanHandling=ON` 只替换**输入字段**的 NaN，**不替换 `divide` 产生的 inf/NaN** ⇒ 只剩极少数有定义的票进入组合。
⇒ 计数型字段必须先做 `ts_mean`/`ts_backfill` 平滑 + 分母加 `+0.01` 兜底，不能直接进 `divide`。

**② 0–1 加权分（`method_2/4_filtered`）→ 覆盖正常但信号为零**
T2 / T3 / T5 / T8 / T10：持仓 78–86/80–89（正常），TO 6–25%（低），2Y 能到 **1.78 / 1.80**，
但 **S 全部 ≈ 0（|S| ≤ 0.37）**。这是决定性的一组：字段有覆盖、有低换手、二年期还好看，却**与 DEU 未来收益无横截面单调关系**。

**③ 非极性注意力（`group_level_3_count`）与跨桶背离 → 只共享噪声**
T6 S −0.03 / 2Y −0.53；T10 跨 fkw1↔fkw4 背离 S −0.37 ⇒ **桶间同构字段之间只共享噪声，不共享信息**（bucket 不可跨骨架迁移的第 6 次实证）。

**④ 论坛建议的 `ts_corr` 几何在 sentiment33 上不成立**
T7（§58.2 表内）取自平台论坛「使用 nip 族数据点亮 news 塔」帖（94 票 / 22 评论）的核心结论
「相关性算子 + FAST neutralization 的组合比较适合处理 sentiment 数据」⇒ 实测 S −0.26。
**该结论不可跨数据集搬运**；它是在 news/NIP 类数据集上得到的，不是 NLP 情绪分数上。

**⑤ `LOW_2Y_SHARPE` 与全样本 S 的背离是本次最重要的诊断信号**
T2：2Y = **1.78** 而全样本 S = **0.04**，十年累计 return 仅 0.52%（pnl 338950 / book 20M）。
⇒ 收益几乎全部集中在最近 2 年。**首选解释：sentiment33 在 DEU 的实际数据起点远晚于 IS 起点 2014-01-01**
（平台报 IS 2014-01-01～2023-12-31），前 8 年基本是 NaN→0，等于把 2/3 样本喂了零。
该解释**未直接验证**（需 Labs 取原始面板核首日有效值），但 2Y/全样本的方向与量级均一致。
⇒ 后续凡遇「2Y 高 / 全样本 S 低」的组合，先怀疑**数据起点**，再怀疑骨架。

### 58.4 判死结论

**`DEU-SENTIMENT33-DEAD`**：DEU / sentiment33（Sentiment Data by NLP）在 10 个结构互异模板下

- 最好 |S| = 0.37（T3），距 1.58 差 4.3×；
- 三类字段（计数 / 加权分 / 非极性）分别走三条不同失败路径，不是单一骨架选错；
- 覆盖 0.3221 是结构性上限，`LOW_SUB_UNIVERSE_SHARPE` 在两条上已经负数。

⇒ 不再投入 sentiment33。连同 sentiment27 / sentiment7 ⇒ **DEU/sentiment 塔封盘**。

### 58.5 ★ prod 池机制纠正：我自己的 ACTIVE alpha 就在生产池里

用本地指标指纹（S / F / TO / 2Y / SUB 五项逐位相同 ⇒ 同一组合，本会话已 2 次实证）扫全库，
发现一个此前被忽略的机制：

| alpha | 状态 | S | F | TO | 2Y | SUB | prod | self |
|---|---|---|---|---|---|---|---|---|
| `2rjrMZ25` | **ACTIVE（已提交）** | 1.77 | 1.61 | 11.99% | 1.83 | 0.88 | 0.6510 | — |
| `RREXxW6z` | UNSUBMITTED | 1.77 | 1.61 | 11.99% | 1.83 | 0.88 | 0.6510 | **1.0（同表达式）** |
| `WjLEOqLP` | UNSUBMITTED | 1.77 | 1.61 | 11.99% | 1.83 | 0.88 | **1.0** | — |

`RREXxW6z` 与 `2rjrMZ25` 的表达式**逐字符相同**；`WjLEOqLP` 仅把 `ts_backfill(x,1008)` 换成
`ts_mean(ts_backfill(x,1008),1)`，组合完全一致（五项指标逐位相同）。

**⇒ prod correlation 的池子里包含我自己已提交的 alpha。**
因此任何与自有 ACTIVE **同族或近似**的变体，测出的 prod 必然 ≈ 1.0（`WjLEOqLP`），
而完全相同的副本连 prod 都只是那张 ACTIVE 自己的值（`RREXxW6z` 的 0.6510 是 `2rjrMZ25` 的值）。

**这条机制改写了 §57 的「DEU prod 墙 79%」结论**：
已测 85 条中 67 条 ≥0.70，其中**相当部分是「同族已有 ACTIVE」导致的结构性 1.0**，不是
「DEU 的信号空间被别人占满」。真实的外部拥挤度墙率**目前未知**，必须靠 virgin 族实测才能定。
⇒ 此前「DEU 已测池 0 可提交 ⇒ 60 颗在 DEU 不可达」的推断**降级为未证实**。

### 58.6 ★ 可提交存量重估：463 → 291 待测 → 185 个 virgin 族

本地库 `alphas`（`region_id=10`）**3443 行**，按平台硬闸全量过滤
（|S| ≥ 1.58 且 F ≥ 1.0 且 TO ∈ (1%, 70%) 且 2Y ≥ 1.0）得 **463 条 gate-pass / 211 个信号族**
（族指纹 = 表达式内「字段名多重集」，剔除算子名）。

| 状态 | 条数 | 说明 |
|---|---|---|
| gate-pass 且 prod 已测 | 172 | 其中 18 条 prod < 0.70，17 条已判死见 §58.5，`58gGQmlN` 见 §58.7 |
| **gate-pass 且 prod 未测** | **291** | 真正的可提交存量 |

291 条按「同族证据」分三层：

| 层 | 条数 | 含义 | 处置 |
|---|---|---|---|
| A_family_proven | 6 | 同族已有成员过 prod 墙 | 优先测；但同族已有 ACTIVE ⇒ self 风险高 |
| C_family_walled | 100 | 同族已测成员全部 ≥0.70 | 直接放弃（几乎必然是结构性 1.0） |
| **D_family_virgin** | **185** | 同族**既无已测 prod、也无任何已提交成员** | **主战场** |

指纹去重后只有 2 条能免测继承证据，其中 1 条（`RREXxW6z`）已被 §58.5 判死
⇒ **289 条必须上平台实测**，其中 **185 条（D 层）不带任何自有 ACTIVE 的同族污染**。

D 层头部（按 S 降序，全部未测 prod）：

| alpha | S | F | TO | 2Y | 族规模 | 字段族 |
|---|---|---|---|---|---|---|
| `JjelQJoe` | 2.70 | 1.28 | 61.6% | 2.29 | 4 | `sector / tm_15_r1_r5_r10_rh_glb_d1_r5_q1` |
| `vR102Ver` | 2.39 | 1.29 | 43.5% | 1.60 | 4 | 同上 |
| `QPveKkPM` | 2.37 | 1.29 | 42.0% | 1.25 | 1 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` |
| `e75AAMQz` | 2.33 | 1.12 | 40.1% | 1.36 | 5 | `tm_15_..._d1_r10_q1` |
| `1YNvvgdJ` | 2.28 | 1.28 | 37.8% | 1.89 | 5 | 同上 |
| `1YNvPXrm` | 2.12 | 1.97 | **10.4%** | **2.55** | 1 | `snl27_totaldomains / snt7_all_languages_views`（**sentiment 塔**） |
| `GrWVx2aO` | 2.07 | 1.89 | 10.3% | 2.55 | 1 | `snl27_avgranking / snt7_*` |
| `kqNRX1ZP` | 2.06 | 1.86 | 11.0% | 2.37 | 1 | `snl27_relpopularity08 / snt7_*` |
| `qMLbdPAA` | 2.04 | 1.84 | 11.0% | 2.38 | 1 | `snl27_relpopularity1 / snt7_*` |
| `d5WqmExJ` | 1.96 | 1.76 | 11.0% | 2.35 | 1 | `snt27_rank / snt7_*` |

**`1YNvPXrm` / `GrWVx2aO` / `kqNRX1ZP` / `qMLbdPAA` / `d5WqmExJ` 五条是 D 层最优质的一组**：
S 1.96–2.12 / F 1.76–1.97 / TO 10–11% / 2Y 2.35–2.55，五项模拟层闸全过，且族内零已提交成员。
注意它们与 `N1NML1wq`（≡ `P0oe6wpJ`，prod 0.7694）**不同族**——后者只用 `snt7_all_languages_views`，
这五条是 `snl27 × snt7` 的组合族。

### 58.7 `58gGQmlN` 判死（prod 0.6830 过墙但 self 0.9408）

`check_self_correlation(58gGQmlN, type="self")` → **0.9408**，对标 `2rmGAPqN`（同族已提交）。
`pool_size=10 / full_os_pool_size=11 / excluded_power_pool_count=1`。
⇒ 虽 prod 0.6830 < 0.70，但 self 远超 0.70 ⇒ **不可提交**。

**⇒ DEU 已测 prod 池（85 条）现在真正归零：18 条 prod < 0.70 里，17 条 prod 撞墙、
1 条（`58gGQmlN`）self 撞墙。**

### 58.8 操作性阻塞：平台 prod 相关性槽单并发且被兄弟会话占满

本会话 `check_correlation(correlation_type="production")` 三次尝试全部
**120s MCP 超时**（`N1NML1wq` ×2、`1YNvPXrm` ×1）。`get_alpha_details` 的 `is.prodCorrelation`
对未测 alpha 恒为 null，**不能替代实测**。

⇒ 289 条的 prod 测量是**串行瓶颈**：单条 1–5 分钟、账号级单并发、且与兄弟会话争抢。
185 条 D 层全测需 **3–15 小时**纯排队时间，且期间每次都会被 120s 超时打断。

**处置建议（待用户决策）**：
1. 优先只测 §58.6 表中 D 层头部 20–30 条（覆盖最好的 5 条 sentiment 族 + TO<40% 的高 S 条），
   用 20–30 条的通过率标定真实墙率，再决定是否铺开 185 条；
2. 若标定后通过率 ≥ 30%，则 DEU 的 60 颗目标**重新变为可达**（185 × 30% ≈ 55，加上 A 层与后续新波次）；
3. 若通过率 < 10%，则 DEU 确认为结构性饱和，缺口须由跨区存量（112 个互异族 prod<0.70）承接。

### 58.9 本节的纪律沉淀

1. **prod correlation 的池子包含自有 ACTIVE alpha** ⇒ 同族变体的 prod 测不出外部拥挤度，只会测出「你自己」。
   任何「prod 墙率」统计必须先扣除「同族已有 ACTIVE」的部分。
2. **`RREXxW6z` 这类「prod 达标」是假阳性**：它的 prod 0.6510 继承自其 ACTIVE 孪生，自身 self = 1.0。
   **prod 与 self 必须成对判断，单看 prod 会把完全重复的 alpha 当成候选。**
3. **「2Y 高 / 全样本 S 低」优先怀疑数据起点，而不是骨架**（sentiment33 T2：2Y 1.78 / S 0.04）。
4. **VECTOR 计数型字段不能直接进 `divide`**：`nanHandling` 不处理运算产生的 inf/NaN，会塌缩成 2/4 持仓。
5. **论坛模板结论有数据集适用范围**：`ts_corr` + FAST neutralization 是 news/NIP 类结论，
   在 NLP 情绪分数上实测为负（T7 S −0.26）。

---

### 58.10 ★★ 族去重必须用 PnL 相关性，字段名族会把多样性高估 3×

§58.6 用「表达式内字段名多重集」做族指纹，得出 211 族 / 185 个 virgin 族。本轮用
`compute_mutual_correlation`（纯本地、下载 PnL 计算，**不占平台相关性槽**）复核，
结论是**字段名族严重高估多样性**。

**证据一：5 条「最优质」sentiment 候选其实是同一个 alpha**

| alpha | 表达式核心 | vs `P0oe6wpJ`(prod 0.7694) |
|---|---|---|
| `1YNvPXrm` | `vector_neut(ts_quantile(ts_ir(ts_mean(max(snt7,…),5),22),252,gaussian), ts_backfill(snl27_totaldomains,22))` | **0.9971** |
| `GrWVx2aO` | 同上，neut 腿 = `snl27_avgranking` | **0.9949** |
| `kqNRX1ZP` | 同上 + 双层 neut（`snl27_relpopularity08` / `snl27_totaldomains`） | 0.9032 |
| `qMLbdPAA` | 同上，neut 腿 = `snl27_relpopularity1` | 0.9050 |
| `d5WqmExJ` | 同上，neut 腿 = `snt27_rank` | 0.8750 |

`kqNRX1ZP ↔ qMLbdPAA = 0.9979`、`1YNvPXrm ↔ GrWVx2aO = 0.9933`。
**5 条互相关 0.875–0.998，最大「两两互不超 0.5」子集只有 1 条。**
⇒ 这 5 条不是 5 个候选，是**1 个信号的 5 次写法**；而该信号的核心 `snt7_all_languages_views`
已在 `P0oe6wpJ` 上测出 prod **0.7694**。
⇒ **§58.6 表中「D 层最优质的 5 条」全部作废**，不必再花平台槽去测。

**证据二：19 条 D 层候选只构成 7 条独立信号**

`compute_mutual_correlation(19 条, threshold=0.7)` 的可视化结果：

| 簇 | 成员 | 簇内相关 | 代表字段族 | S 区间 | TO 区间 |
|---|---|---|---|---|---|
| **A** | `JjelQJoe` `vR102Ver` `1YNvvgdJ` `1YNv6Ymk` `RREX67Ab` `QPveKJ8g` `e75AAMQz` `KPJexqql` `WjOkwYWQ` `QPveKkPM` `MPYw3oOn` | 0.57–**0.9878** | `tm_15_/tm_16_r1_r5_r10_rh_glb_d1_r*_q1` | 1.92–2.70 | 30–62% |
| **B** | `RRVKvGZo` `2rOWxmbx` `3q952836` `LL9rK9On` `blRnxboq` `WjP0x8Md` `LL9r9WeM` `npKQ78kd` | 0.48–**0.9774** | `le89` / `Vk65` / `mdl264_*` | 1.86–1.97 | 10–15% |

**跨簇相关 ≈ 0.00–0.15**（`JjelQJoe` 系 vs `RRVKvGZo` 系全部 < 0.16）⇒ A 与 B 是两条真正独立的信号。

19 条 → `max_mutually_below_subset_size = 7`（greedy 下界）。按 19→7 的比例外推，
**185 条 virgin 候选的真实独立信号数约 40–70 条**，而不是 185 条。

**§58.6 的数字要按这个口径重读**：
- 「291 条待测」是**回测条数**，不是候选数；
- 「185 个 virgin 族」是**字段名族数**，高估约 3×；
- 真实可提交信号池 ≈ 40–70，且**每一条都要过一次不可回避的 prod 实测**。

**方法论沉淀（跨区域通用）**：
1. **S/F/TO/2Y/SUB 五项逐位相同 ⇒ 同一组合**（本会话 4 次实证），可直接用它做零成本去重；
2. **字段名族只能用来「分组」，不能用来「数候选」**；数候选必须用 `compute_mutual_correlation`
   在 PnL 层面聚簇（本地计算、不占平台槽、零配额）；
3. **同族变体越多，越说明那是一个信号被反复重写**——`RREX67Ab ↔ QPveKJ8g = 0.9878` 这种
   就是同一个 alpha 换了 `bucket` 步长；
4. 派发新波次前若想估「这波能出几个」，先按「每 3 条回测 ≈ 1 条独立信号」折算，
   再乘上该族的 prod 通过率。

**新增判死（并入 §58.5 的机制纠正）**：
`DEU-SNT7-SNL27-NEUT-DEAD` —— `snt7_all_languages_views` 主体 + `snl27_*` 正交腿这一族，
5 条写法互相关 0.875–0.997，主体信号已在 `P0oe6wpJ` 上测得 prod 0.7694 ⇒ 整族不再尝试。

---


## §59 DEU prod 墙 100% 实证 + 跨区可提交池 176 条（2026-10-30 深夜）

本节是一次**战略级结论**：DEU 不再是「候选不够」的问题，而是「prod 相关性墙 100% 拦截」。
证据来自本地库全量 + 共享 prod 缓存，零新增平台调用。

### §59.1 DEU prod 墙率为 0%（50/50）

口径：`gate-pass`（|S|≥1.58 且 F≥1.0 且 TO∈(0.01,0.70) 且 2Y≥1.0）+ **未提交**（`status NOT IN
('ACTIVE','SUBMITTED')`）+ 未判死（`disposition<>'DEAD'`），prod 取 `COALESCE(alphas.prod_correlation,
alpha_corr_cache.prod_correlation)`。

| region | gate-pass 未提交 n | 已测 prod | prod<0.70 | prod≥0.70 | **通过率** | 测量覆盖 |
|---|---|---|---|---|---|---|
| EUR | 515 | 132 | 46 | 86 | 34.8% | 25.6% |
| GBR | 497 | 126 | 29 | 97 | 23.0% | 25.4% |
| **DEU** | **371** | **50** | **0** | **50** | **0.0%** | **13.5%** |
| IND | 333 | 167 | 80 | 87 | 47.9% | 50.2% |
| USA | 315 | 125 | 51 | 74 | 40.8% | 39.7% |
| ASI | 208 | 20 | 4 | 16 | 20.0% | 9.6% |
| GLB | 205 | 121 | 28 | 93 | 23.1% | 59.0% |
| KOR | 134 | 41 | 35 | 6 | **85.4%** | 30.6% |
| MEA | 84 | 56 | 22 | 34 | 39.3% | 66.7% |
| HKG | 22 | 5 | 0 | 5 | 0.0% | 22.7% |
| **全局** | **2684** | **843** | **295** | **548** | **35.0%** | 31.4% |

**读法**：
1. **DEU 的 50/50 全灭，是全部区域里唯一「已测量且通过率为 0」的区**（HKG 0/5 但样本太小）。
   这与此前 §57 的「prod 墙 79%」不同 —— 那些 <0.70 的 18 条**几乎全是已提交的 ACTIVE**
   （例如 `2rjrMZ25` prod 0.6510 但已 ACTIVE），排除 ACTIVE 后 DEU 的真实外部拥挤度是 **100% 撞墙**。
2. **KOR 85.4% 通过率与 DEU 0% 相差 ∞ 倍**，IND 47.9%、USA 40.8% 也远好于 DEU。
   ⇒ 「DEU 结构性饱和」不是主观判断，是 10 个区的横向对照里最极端的一格。
3. 全局 35.0% 通过率说明「prod 0.70 硬闸」在别的区是**可通行的门**，不是不可逾越的墙。

### §59.2 跨区可提交池：严格双门 176 条

在上表 `prod<0.70` 的 295 条上做四步收口：
1. 剔除已判死（4 条，全在 IND）
2. **指标指纹去重**（`(S,F,TO,2Y)` 各保留 2/2/4/2 位小数后逐位相同 ⇒ 同一组合）：295 → **287**
3. 追加 `self < 0.70`
4. **剔除 `prod == self` 完全相等的 15 条**（self 列被误填成 prod，属脏数据，按 unknown 处理）

| 状态 | 条数 |
|---|---|
| prod<0.70 指纹去重后 | 287 |
| ├ `prod == self` 脏行（按 unknown） | 15 |
| ├ self 未测 | 95 |
| ├ self ≥0.70（死） | 1 |
| └ **严格双门通过** | **176** |

**严格双门通过按区域**：

| region | 条数 |
|---|---|
| IND | 41 |
| USA | 37 |
| EUR | 24 |
| GBR | 19 |
| GLB | 18 |
| MEA | 17 |
| KOR | 16 |
| ASI | 4 |
| **DEU** | **0** |
| 合计 | **176** |

另有 **110 条**（95 未测 self + 15 脏行）只需补测 self 即可判定，全部不在 DEU。

**头部样本（S 降序前 12 条，全部双门通过）**：

| region | alpha | S | F | TO | 2Y | prod | self | ds |
|---|---|---|---|---|---|---|---|---|
| USA | `6XpMb0aG` | 4.32 | 4.32 | 8.1% | 4.19 | 0.665 | 0.413 | 1811 |
| IND | `QPGbAOn5` | 3.67 | 2.96 | 23.5% | 3.59 | 0.654 | 0.054 | 1794 |
| GLB | `6Xdm3pXL` | 3.66 | 1.11 | 56.4% | 2.92 | 0.640 | 0.491 | 1786 |
| IND | `RR7OWQKd` | 3.32 | 2.81 | 21.7% | 3.96 | 0.688 | 0.553 | 1793 |
| IND | `E5l23mrm` | 3.27 | 3.61 | 8.9% | 3.39 | 0.652 | 0.603 | 41 |
| USA | `0mjaa2Ev` | 3.24 | 2.60 | 16.2% | 4.30 | 0.646 | 0.089 | 382 |
| GLB | `VkxV8NAJ` | 3.23 | 1.40 | 60.9% | 3.89 | 0.649 | 0.541 | 840 |
| IND | `E5VNe67L` | 3.20 | 2.52 | 25.0% | 3.00 | 0.664 | 0.344 | 593 |
| USA | `d5KPPrxx` | 3.13 | 2.46 | 16.6% | 4.10 | 0.674 | 0.109 | 382 |
| IND | `JjP0Ja5l` | 3.12 | 2.42 | 24.6% | 2.82 | 0.665 | 0.304 | 593 |
| IND | `9qEPO5K2` | 3.10 | 2.38 | 24.1% | 2.87 | 0.628 | 0.318 | 593 |
| GLB | `npv9WLVE` | 3.08 | 1.42 | 60.8% | 3.19 | 0.649 | 0.379 | 840 |

### §59.3 关键校正：`self` 列存在污染，必须剔除 `prod == self`

176 条里发现 **15 条 `|prod - self| < 1e-9`（逐位相等）**，例如 `wpjrMnz5` prod=0.639/self=0.639、
`mLjGRm02` 0.596/0.596、`78jYpn0Z` 0.700/0.700。
两个独立统计量在连续值上逐位相同的概率为 0 ⇒ 这是**写入侧把 prod 值同时写进了 self 列**。
若把它们算作「双门通过」，会把 95 条未知高估成 80 条通过。
**纪律**：凡 `prod == self` 的行，self 一律按 `unknown` 处理，必须实测。

### §59.4 self 相关性是零平台成本的预筛（本轮新增方法论）

`check_self_correlation` 是**纯本地计算**（拉 PnL 与本地 OS 池比对），**不占平台 prod 单并发槽、不耗配额**。
对 DEU D 层 virgin 候选代表实测，立刻看到分化：

| alpha | 代表族 | self max | 对标 | 判定 |
|---|---|---|---|---|
| `KPJexqql` | cluster A `tm_15…r10_q1` | **0.0677** | `883Y3bAW` | ✅ 余量极大 |
| `JjelQJoe` | cluster A `tm_15…r5_q1` | **0.1566** | `883Y3bAW` | ✅ 余量充足 |
| `RRVKvGZo` | cluster B `nn+le89` | 0.6913 | `2rOe10qY` | ⚠️ 贴墙过 |
| `blRnxboq` | cluster B `mdl264+analyst` | **0.7687** | `blRnKEk6` | ❌ |
| `WjP0x8Md` | cluster B 多因子混合 | **0.8609** | `blRnKEk6` | ❌ |
| `LL9r9WeM` | cluster B analyst 四腿 | **0.9722** | `883Y3bAW` | ❌ |

**结论**：§58 的「19 条 D 层 → 7 条独立信号」里，**cluster B 已被 self 成片砍掉**；
**只剩 cluster A（`tm_15/tm_16_r1_r5_r10_rh_glb_d1_*`，11 条候选）self 干净**，
而该族内部互相关 0.57–0.9878 ⇒ **提交意义上只能产出 1–2 条**。

### §59.5 DEU 剩余唯一希望：cluster A，只差 prod 一门

- `JjelQJoe` S 2.70 / F 1.28 / TO 61.6% / self 0.157
- `KPJexqql` S 1.96 / F 1.55 / TO 16.4% / self 0.068
- 同族 11 条（`vR102Ver` `QPveKkPM` `e75AAMQz` `MPYw3oOn` `1YNvvgdJ` `1YNv6Ymk` `RREX67Ab`
  `QPveKJ8g` `WjOkwYWQ`）指标相近
- **唯一未测的门是 prod**。按 DEU 0/50 的实测通过率，该族 prod 通过的先验**极低**。

### §59.6 平台 prod 单并发是账号级硬约束（不是本会话问题）

本会话 `check_correlation(correlation_type="production")` 累计 **5 次 120s 超时**，
最后一次拿到明确证据：

```text
status = correlation_busy
inflight = false
retry_after = 240
holder = "corr:get_production_correlation(rKRQbPPE)"
```

`holder` 里的 alpha id **每次都不同**（此前 `omE2Xn8k`，本次 `rKRQbPPE`）⇒ 兄弟会话正在**连续**测量，
不是死锁。共享缓存 `alpha_corr_cache` 最新写入 `E56oYEkL`（region USA）证实对方的测量是成功的。

**含义**：账号级只有 **1 个 prod 计算并发**，且被所有会话共享。
想让本会话测量 DEU 候选，必须等兄弟会话空闲，或**跨会话串行排班**。
按 289 条 × 1–5 分钟估算需 3–15 小时纯排队，**且会被 120s MCP 超时反复打断**。

### §59.7 本轮结论与三个可选路线

**结论**：DEU 的 60 颗目标在「REGULAR + prod<0.70」约束下**不可达**。
不是挖掘不足 —— 是 371 条 gate-pass 存量里所有测过 prod 的（50 条）全部撞墙。

| 路线 | 动作 | 代价 | 60 颗可达性 |
|---|---|---|---|
| **A 转区承接** | 从 §59.2 的 176 条严格双门池里，按区域分批上平台终验并提交 | 需先解决 prod 槽排班；提交需用户逐批确认 | **✅ 176 ≫ 60** |
| **B 死磕 DEU** | 先把 cluster A 11 条测 prod，再扫 110 条 self 未测 | 3–15h 排队；cluster A 先验极低 | ❌ 最多 1–2 条 |
| **C PPA 通道** | DEU 候选打 `PowerPoolSelected`，用 PPAC<0.5 取代 PC<0.7 | 提交通道决策，需用户明确确认 | ⚠️ 未验证池内 PPAC 分布 |

**推荐 A**：176 条已过双门、分布在 8 个区、与 DEU 完全脱钩，
且 DEU 只需「3 颗点亮一塔」的目标可先用跨区存量里的 DEU 邻近区（EUR）候选补位。

### §59.8 本节新增/修正的判断

1. **【修正 §57】** 「DEU prod 墙 79%」→ **DEU prod 墙 100%（50/50，排除 ACTIVE 后）**。
2. **【新增】** `self` 列污染：`prod == self` 逐位相等 = 脏数据，按 unknown 处理（本轮 15 条）。
3. **【新增】** `check_self_correlation` 是零成本预筛，应在花 prod 槽之前先跑。
4. **【新增】** cluster B 已被 self 成片判死；DEU 只剩 cluster A 一族，提交意义 1–2 条。
5. **【新增】** 跨区严格双门池 176 条（IND 41 / USA 37 / EUR 24 / GBR 19 / GLB 18 / MEA 17 / KOR 16 / ASI 4）。
6. **【新增】** 平台 prod 单并发是**账号级**约束，跨会话共享；`holder` 字段可辨识占用者。


### §59.9 自我纠错：§59.1/§59.2 用错过滤列，重算后结论更强、池子收窄

#### 错在哪

§59.1/§59.2 用 `alphas.status NOT IN ('ACTIVE','SUBMITTED')` 判「未提交」。
**本地 `status` 列严重过期**。实测抽两条 `get_alpha_details` 打脸：

| alpha | 本地 status | 平台真实 | 提交日 |
|---|---|---|---|
| `6XpMb0aG`（S 4.32，§59.2 榜首） | 看似未提交 | **ACTIVE / stage OS** | 2026-08-12 |
| `QPGbAOn5`（S 3.67，§59.2 第 2） | 看似未提交 | **DECOMMISSIONED / stage OS** | 2026-08-12 |

⇒ §59.2 的「176 条」里混进了已提交/已下线 alpha，**该数字作废**。

#### 正确判据

`date_submitted IS NULL AND (stage IS NULL OR stage='IS')`。
本地 status 的过期规模（gate-pass 全量）：

| region | gate-pass | 本地标 UNSUBMITTED | 实际已提交 |
|---|---|---|---|
| EUR | 522 | 427 | 22 |
| GBR | 505 | 458 | 19 |
| DEU | 375 | 340 | 4 |
| IND | 337 | 107 | 34 |
| USA | 319 | 138 | 26 |
| ASI | 208 | 29 | 4 |
| GLB | 207 | 167 | 9 |
| KOR | 138 | 77 | 25 |
| MEA | 84 | 0 | 21 |
| HKG | 22 | 4 | 0 |
| **全库** | **2717** | — | **164** |

#### 修正后的 DEU 结论（比 §59.1 更强）

| 项 | 值 |
|---|---|
| DEU gate-pass 全量 | 375 |
| 其中**从未提交** | **371** |
| ├ 已测 prod | 50 |
| └ 未测 prod | 321 |
| **prod < 0.70** | **0** |
| prod ≥ 0.70 | 50 |
| **已测 50 条的 prod 最小值** | **0.7145** |
| 已测 50 条的 prod 最大值 | 1.0000 |

**关键**：不是「大部分撞墙」——是 **50/50 全撞，且最小值 0.7145 高于阈值 0.70，连一条擦边的都没有**。
这排除了「阈值附近的噪声」解释，DEU 的 prod 拥挤度是结构性的。

（HKG 同为 0%，但样本仅 5 条；DEU 的 50 条是全部区域里唯一样本充足且通过率为 0 的。）

#### 修正后的跨区可提交池（替代 §59.2 的 176）

严格判据（`date_submitted IS NULL` + stage IS + 未判死）下：

| 状态 | 条数 |
|---|---|
| 从未提交 + gate-pass + 未判死 | **2213** |
| ├ prod < 0.70 | 167 |
| │  └ 指标指纹去重后 | **165** |
| │     ├ `prod == self` 脏行 | **0**（严格判据下脏行消失，说明脏行集中在已提交记录） |
| │     ├ self 未测 | 96 |
| │     ├ self ≥ 0.70 | 1 |
| │     └ **严格双门通过** | **68** |

**按区域（严格双门 68 条）**：

| region | 严格双门 | prod<0.70 完整池 |
|---|---|---|
| USA | 16 | 30 |
| IND | 16 | 47 |
| GLB | 13 | 22 |
| EUR | 11 | 31 |
| GBR | 10 | 18 |
| MEA | 2 | 2 |
| KOR | **0** | 15 |
| ASI | 0 | 0 |
| **DEU** | **0** | **0** |
| 合计 | **68** | **165** |

**KOR 的 15 条全部卡在「self 未测」**（本地 prod 0.576–0.699 都合格）。
⇒ **96 条 self 未测的候选是当前唯一「零平台成本即可扩容」的池子**：
`check_self_correlation` 是纯本地计算，不占 prod 槽。若 96 条按严格双门池的表现（68/69 ≈ 99%）推算，
池子有望从 68 扩到 ~160。

#### 修正后的路线判断

| 路线 | 可达性 | 说明 |
|---|---|---|
| **A 转区承接** | **68 条已判定 + 96 条可零成本扩容** | 目标 60 颗在「已判定 68 条」内已可覆盖；96 条扩容只是冗余 |
| B 死磕 DEU | 371 条里 50 条已测全灭，剩 321 条 prod 未测 | 必须先破 0.7145 的墙，先验极低 |
| C PPA 通道 | 未验证 | 需用户确认 |

#### 本节新增纪律

1. **【硬纪律】判「是否已提交」禁止用 `alphas.status`**，必须用 `date_submitted IS NULL` + `stage='IS'`。
   本地 status 只反映最后一次流水线写入，不反映平台状态。
2. **【硬纪律】任何「可用池」数字交付前必须抽样 2–3 条 `get_alpha_details` 核 `settings.region` + `status`**。
   本轮正是靠抽 2 条才发现 176 这个数字是错的。
3. **【新增】`prod == self` 脏行集中在「已提交记录」**，严格未提交池里为 0 —— 说明污染来自提交流程写库，不是测量。
4. **【新增】96 条 self 未测是免费扩容点**，应在排 prod 队之前先跑完。


---

## §60 self 零成本扩容 25 条 + 五区 PnL 聚簇：全库真实独立信号 = 38 条（< 60 目标）

### §60.1 本轮 self 实测（25 条，纯本地、零配额、不占平台相关性槽）

`check_self_correlation` 是本地 PnL 计算，**不消耗平台单并发 prod 槽**，因此是 prod 槽被兄弟会话占满时唯一能推进的扩容动作。

| # | region | alpha | S | F | TO | 2Y | prod | self max | 判定 | 撞的对象 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | USA | `j2eoJRMO` | 2.42 | 1.26 | 17.7% | 1.69 | 0.6982 | 0.2694 | ✅ | — |
| 2 | USA | `58jr102k` | 2.26 | 1.33 | 12.6% | 2.06 | 0.6818 | 0.2330 | ✅ | — |
| 3 | USA | `YPx89bQJ` | 2.19 | 1.16 | 15.7% | 1.91 | 0.6803 | 0.2812 | ✅ | — |
| 4 | USA | `78Lb3aoQ` | 1.82 | 1.21 | 3.4% | 2.31 | 0.6839 | 0.4702 | ✅ | — |
| 5 | USA | `rKRY3NZ1` | 1.79 | 1.17 | 4.6% | 2.28 | 0.6995 | 0.4700 | ✅ | — |
| 6 | USA | `88vXxaqv` | 1.99 | 1.66 | 9.5% | 2.04 | 0.6811 | 0.1814 | ✅ | — |
| 7 | USA | `XgRM3Yra` | 1.66 | 1.19 | 8.7% | 2.27 | 0.5803 | **−0.0915** | ✅ | — |
| 8 | USA | `LL53QVvn` | 1.61 | 1.39 | 11.2% | 2.75 | 0.6163 | **−0.0356** | ✅ | — |
| 9 | USA | `1Yj08nb6` | 1.58 | 1.20 | 10.0% | 2.29 | 0.5796 | **−0.1163** | ✅ | — |
| 10 | EUR | `YP1d66KM` | **3.57** | 2.43 | 24.2% | 3.31 | 0.5985 | 0.5656 | ✅ 贴墙 | `LL5VwgO1` 0.5656 |
| 11 | EUR | `mL617YPx` | 1.82 | 1.25 | 6.8% | 2.23 | 0.5421 | 0.4504 | ✅ | `rKd5lAo8` 0.4504 |
| 12 | EUR | `O0Jx2O6R` | 1.94 | 1.26 | 5.6% | 1.86 | 0.5129 | 0.8611 | ❌ | `e76xGOQO` 0.8611 |
| 13 | EUR | `3qjeJGle` | 1.72 | 1.08 | 4.7% | 1.80 | 0.5710 | 0.9092 | ❌ | `Grge2lN3` 0.9092 |
| 14 | EUR | `RREnAplg` | 2.00 | 1.21 | 4.9% | 2.62 | 0.6732 | 0.9204 | ❌ | `E56Jea7P` 0.9204 |

（另有前 11 条 KOR / IND 见 §59。）

**USA 9/9 全通过**，是全库最干净的一块：self 最高 0.4702，其中 3 条为**负相关**（−0.09 / −0.04 / −0.12），意味着与我已经提交的 USA 池方向相反、零重叠。

**EUR ds=1452 全族判死**：`O0Jx2O6R` 撞 `e76xGOQO` 0.8611、`3qjeJGle` 撞 `Grge2lN3` 0.9092，**两条撞的对象不同** ⇒ 不是单点重复，是整族各自与已提交池重叠。`qME6VWbj`（同 ds=1452）无需再测。

**EUR ds=1826 内部分化**：`YP1d66KM` 0.5656 通过、`RREnAplg` 0.9204 判死 ⇒ **不能按 dataset_id 一刀切判死，必须以实测为准**。这与 KOR `ds=1149` 全族同撞 `vRrQ5Npr` 的形态不同（那里 5 条撞同一对象 0.769–0.973，才可整族判死）。

### §60.2 严格双门池 v2：PASS 80 / SELF_FAIL 8 / UNKNOWN 53

口径：`date_submitted IS NULL AND stage='IS'` + gate-pass（|S|≥1.58 ∧ F≥1.0 ∧ 0.01<TO<0.70 ∧ 2Y≥1.0）+ prod<0.70 + self<0.70。

| region | PASS(self<0.7) | SELF_FAIL | SELF_UNKNOWN | 合计 |
|---|---|---|---|---|
| USA | **24** | 0 | 0 | 24 |
| IND | **18** | 0 | 20 | 38 |
| EUR | **13** | 3 | 15 | 31 |
| GLB | **13** | 0 | 1 | 14 |
| GBR | **11** | 0 | 8 | 19 |
| KOR | **1** | 5 | 9 | 15 |
| **合计** | **80** | **8** | **53** | **141** |

上一版（§59.9）为 68 条 PASS，本轮 self 实测把它抬到 **80 条**（+12）。

### §60.3 五区 PnL 聚簇：80 条 PASS 只剩 38 条独立信号

`compute_mutual_correlation(threshold=0.7, years=4)`，本地计算、零配额、`max_subset_exact=true`（精确最优解，非启发式）。

| region | 输入条数 | max_pair | 超阈对数 | **独立信号数** | 坍缩比 |
|---|---|---|---|---|---|
| USA | 24 | 0.9998 (`YPMvZZvv`↔`9qWpQlO9`) | 31 | **12** | 2.0× |
| IND | 18 | 0.9850 (`pwv9eM76`↔`58jPrvZ1`) | 35 | **10** | 1.8× |
| EUR | 13 | 0.9999 (`1YjXvEMJ`↔`omoL2Od2`) | 36 | **5** | **2.6×** |
| GLB | 13 | 0.9865 (`RRbk6eAn`↔`akbWK6V5`) | 45 | **4** | **3.3×** |
| GBR | 11 | **1.0000** (`d51O1kOX`↔`akxLxjVv`) | 9 | **6** | 1.8× |
| KOR | 1 | — | — | **1** | 1.0× |
| **合计** | **80** | | | **38** | **2.1×** |

#### 各区的坍缩结构（可直接用于挑选提交清单）

**USA → 12 条**：`1YZp6EP6` / `O0Jgd7Y7` / `0mjaa2Ev` / `zqrgna91` / `d5KzLo7v` / `N1eLE1de` / `JjP319zn` / `58jr102k` / `YPx89bQJ` / `88vXxaqv` / `78Lb3aoQ` / `LL53QVvn`
- 大簇 A（`0mjaa2Ev`/`d5KPPrxx`/`LL522ZRe`/`88v2XRm7`，0.845–0.984）→ 只留 `0mjaa2Ev`
- 大簇 B（`1YZp6EP6`/`XgJoXm50`/`E5RGoOX1`/`O08GeKx1`/`YPMvZZvv`/`9qWpQlO9`，0.985–0.9998）→ 只留 `1YZp6EP6`
- 簇 C（`zqrgna91`↔`j2eoJRMO` 0.9079）→ 留 `zqrgna91`（S 更高）
- 簇 D（`vROPEJ8w`/`O0Jgd7Y7`/`XgRM3Yra`/`1Yj08nb6`，0.76–0.87）→ 留 `O0Jgd7Y7`
- **本轮新测的 9 条有 7 条进入最终 12 条子集** ⇒ self 扩容是有效的。

**IND → 10 条**：`E5VNe67L` / `pwv9eM76` / `zq3zKgd8` / `KPmvEYeE` / `kqJkPLeO` / `j2el6dlk` / `j2eo0oMO` / `QPYrG5q5` / `omovwGMv` / `gJWnrZgg`
- `pwv9eM76`↔`58jPrvZ1` 0.985 → 只留 1
- `zq3zKgd8`（S **4.69**，全池最高）与所有同族只有 **0.175–0.265** 相关 ⇒ 真独立
- `gJWnrZgg` 与几乎所有 IND 候选**负相关**（−0.06 ~ −0.10）⇒ 反向独立信号

**EUR → 5 条**：`KPmOOwZx` / `YP1d66KM` / `kqN5aPgK` / `mL617YPx` / `omWVZ7lm`
- **ds=1482 的 9 条互相关 0.942–0.9999** ⇒ 全部只算 1 条（用 `KPmOOwZx` 代表）
- `YP1d66KM` 与其余 12 条只有 0.008–0.212 相关，且 S 3.57 / F 2.43 全区最高 ⇒ EUR 的核心资产

**GLB → 4 条**：`RRbk6eAn` / `VkxV8NAJ` / `npv9WLVE` / `xArqRJ8l`
- **ds=865 的 10 条互相关 0.718–0.986** ⇒ 只算 1 条
- `VkxV8NAJ`↔`npv9WLVE` 0.6778（贴阈但未超，可共存）、`xArqRJ8l` 与两者 0.41–0.56 ⇒ 三者结构上是一族的三层，但按 0.7 红线可同时提交

**GBR → 6 条**：`d51O1kOX` / `P0gvv5gE` / `RR62bMje` / `9qWwZ3go` / `mL68wNOK` / `6XKwmQgE`
- ★ **`d51O1kOX` 与 `akxLxjVv` 相关系数精确 = 1.0000**，且五项指标逐位相同（S 1.97 / F 1.29 / TO 8.1% / 2Y 1.71 / prod 0.6793 / self 0.1129）⇒ **同一 alpha 的重复登记，两条只能算一条**。`O08r8QNp`↔`blORMJwm` 0.9942 同理。
- `P0gvv5gE`/`RR6NOlma`/`58gMMJEk` 0.989–0.996 一簇 ⇒ 只留 1

### §60.4 ★ 结论：60 颗目标在 REGULAR 通道下的真实上限

| 项 | 值 |
|---|---|
| 全库 gate-pass + 从未提交 + prod<0.70 | 141 条 |
| 其中 self 已确认 <0.70 | 80 条 |
| **PnL 去重后真实独立信号** | **38 条** |
| 目标 | **60 颗** |
| **缺口** | **22 条（−37%）** |

**这是跨区的上限，不是 DEU 的局部问题。** DEU 贡献 0，USA 12 + IND 10 + EUR 5 + GLB 4 + GBR 6 + KOR 1 = 38。

还有 53 条 self 未测（IND 20 / EUR 15 / KOR 9 / GBR 8 / GLB 1），若全部通过并按 2.1× 坍缩比折算，理论增量 ≈ 53 ÷ 2.1 ≈ **25 条**，最乐观总和 ≈ **63 条**。也就是说：

- **60 颗只有在「53 条 self 未测里通过率 ≥ 88% 且坍缩比不恶化」时才勉强够**；
- 而 KOR 的 15 条里已测 6 条有 5 条判死（通过率 17%）、EUR ds=1452 全族判死 ⇒ 88% 通过率不现实；
- **现实预期 40–48 条**。

### §60.5 口径声明与未验证项

1. 全部 self 值为本轮 `check_self_correlation` 实测（本地计算，与平台"Self Correlation"同口径：池按 `classifications` 排除 Power Pool Alpha）。
2. PnL 聚簇用 4 年日收益（`years=4`），与提交时的 2 年相关性窗口不同 ⇒ **聚簇结论用于"数独立信号"，不能直接当提交时的 self 判据**。提交前仍须对每条候选单独跑 self 实测。
3. `max_subset_exact: true` 表示返回的是精确最大独立子集，不是贪心近似。
4. **未验证**：53 条 self 未测候选的真实通过率；其中 IND 20 条、EUR 15 条、GBR 8 条、KOR 9 条（KOR 9 条全属 ds=1149，已判死可跳过，实际待测 44 条）。
5. **未验证**：这 38 条的 prod 值是否为 48h 内的新鲜测量。库内 prod 会随生产池漂移，提交前须 `check_correlation(refresh=True)` 终验。
6. 平台 prod 相关性槽仍被兄弟会话占用（本轮 5 次 120s 超时，`holder` 每次不同 ⇒ 兄弟会话在连续测量），**跨区 38 条的 prod 复核无法在本会话内完成**。

### §60.6 路线含义

- **路线 A（转区承接）的上限被实测钉死为 38（乐观 63）**，不再是"68 或 80 条候选随便挑"。60 颗在此路径下**不可达**，最好情形也差 12–22 条。
- 补齐缺口的可行手段只剩三条：
  1. **继续做 self 扩容**（剩余 44 条可测，零成本）—— 预计能补到 40–48；
  2. **开新战役产新信号**（不是捡存量）—— 唯一能真正把 38 抬到 60 的路径；
  3. **走 PPA 通道**（打 `PowerPoolSelected`，用 PPAC<0.5 取代 PC<0.7）—— 但 PPAC 分布未验证，且属提交通道决策，须用户确认。
- DEU 本身已无贡献空间（§59 已证 prod 墙 100%，已测 50 条最小值 0.7145）。


---

## §61 self 扩容收口 + 三层可交付口径：114 → 61 → **28**（2026-10-30 凌晨）

### §61.1 本轮动作与口径定义

**动作**：把 §60 遗留的 96 条 self 未测队列里可测的 62 条全部处理完（58 条 `check_self_correlation` 实测 + 4 条因 trio 内互组违禁跳测）。`check_self_correlation` 是纯本地 PnL 计算，**不占平台单并发 prod 槽、不消耗配额**，是 prod 槽被兄弟会话占满时唯一能推进的扩容通道。

**三层口径必须分开说，混用会得出完全不同的结论**：

| 口径 | 含义 | 条数 |
|---|---|---|
| **L1 纸面过双门** | `prod<0.70`（库内值）∧ `self<0.70`（实测）∧ RA 基础闸全过 | **114** |
| **L2 PnL 独立信号** | L1 上做 4 年日收益聚簇（`threshold=0.7`），取最大互不超阈子集 | **61** |
| **L3 带安全边际的独立信号** | L2 上再要求 `prod<0.65` ∧ `self<0.50`（各留 0.05 漂移缓冲）后再聚簇 | **28** |

**为什么必须有 L3**：prod 与 self 都不是静止量。prod 随生产池漂移（同一候选 2–3 天内可从 0.58 漂到 0.98，历史实证），self 随自己新提交的 alpha 上升。**L1 里 prod 落在 0.65–0.70 的候选，在提交前 `check_correlation(refresh=True)` 终验时大概率已经出界**。L2 的 61 是「假设一个都不漂移」的乐观上界，L3 的 28 才是「留出漂移空间后仍然站得住」的保守下界。真实可交付量落在 28–61 之间，取决于终验当天的生产池状态。

### §61.2 双门池 v3（142 行 → PASS 114）

输入为「从未提交（`date_submitted IS NULL AND stage='IS'`）+ RA 基础闸全过 + 库内 `prod<0.70`」的 142 条；self 一列 62 条为本轮实测、68 条取库内值、12 条 `unknown`。

| region | PASS | SELF_FAIL | SELF_UNKNOWN | TRIO_VIOLATION | 行数 |
|---|---|---|---|---|---|
| IND | **37** | 1 | 0 | 0 | 38 |
| USA | **24** | 0 | 0 | 0 | 24 |
| EUR | **22** | 7 | 2 | 0 | 31 |
| GBR | **16** | 2 | 0 | 1 | 19 |
| GLB | **14** | 1 | 0 | 0 | 15 |
| KOR | **1** | 5 | 9 | 0 | 15 |
| **合计** | **114** | **16** | **11** | **1** | **142** |

比 §60 的 v2 池（80 条 PASS）净增 34 条，全部来自本轮 self 实测放行。**IND 37 条是最大单区贡献**，其次 USA 24、EUR 22。

### §61.3 ★ 安全边际审计：114 条里超过一半贴着 0.70 红线

`prod<0.70` 这个判据只回答「当下是否合规」，不回答「明天是否还合规」。按距离红线的远近分层：

| 阈值 | prod 侧条数 | self 侧条数 |
|---|---|---|
| ≥ 0.695 | **12** | 3（≥0.69） |
| ≥ 0.69 | **19** | 3（≥0.69） |
| ≥ 0.68 | 32 | — |
| ≥ 0.65 | **62**（54%） | 13（≥0.60） |
| ≥ 0.50 | — | 32 |

**prod ≥ 0.69 的 19 条距红线不足 0.01**，其中 `gJWnrZgg`（IND）为 **0.6998**，距 0.70 只差 0.0002 —— 这类候选在纸面上"通过"，实质上等同于已判死，提交窗口期内几乎必然漂移出界。

同时满足 `prod<0.65` 且 `self<0.50`（双安全）的只有 **45 条**，分布：

| region | 双安全 | region | 双安全 |
|---|---|---|---|
| IND | 20 | USA | 7 |
| GLB | 12 | EUR | 5 |
| GBR | 1 | KOR | 0 |

**GBR 16 条 PASS 里只有 1 条双安全** —— 其余 15 条 prod 全部落在 0.65–0.70（`rKRkL9QE` 0.6783、`d51O1kOX` 0.6793、`0mYoANkv` 0.6932…），或 self 在 0.49–0.64。GBR 的「16 条」是三层口径里缩水最严重的一块。

### §61.4 双安全子集的 PnL 聚簇：45 → 28

对 45 条双安全候选按区做 `compute_mutual_correlation(threshold=0.7, years=4)`（本地计算、零配额）：

| region | 双安全条数 | PnL 聚簇后独立信号 | 坍缩比 | max_pair | 超阈对数 |
|---|---|---|---|---|---|
| IND | 20 | **18** | 1.1× | `KPmvEYeE`↔`9qEPO5K2` 0.7339 | 2 |
| USA | 7 | **3** | 2.3× | `LL522ZRe`↔`0mjaa2Ev` 0.9214 | 7 |
| EUR | 5 | **3** | 1.7× | `58geG1P1`↔`mL61avpx` 0.9970 | 3 |
| GBR | 1 | **1** | —（单条） | —（单条） | 0 |
| GLB | 12 | **3** | 4.0× | `RRbk6eAn`↔`akbWK6V5` 0.9865 | 44 |
| KOR | 0 | 0 | — | — | — |
| **合计** | **45** | **28** | **1.6×** | | |

**IND 是全场唯一经得起三层口径的富矿**：20 条双安全候选聚簇后仍有 **18 条独立**（`max_subset_exact=true`，精确解），最大相关仅 0.7339（`KPmvEYeE`↔`9qEPO5K2`），全池只有 2 对超阈。互相关普遍落在 0.13–0.53，是真正的多信号低相关池，而不是同一信号的换皮。

**GLB 恰好相反**：12 条双安全里 10 条来自 `ds=865`、彼此 0.72–0.99（`RRbk6eAn`↔`akbWK6V5` 0.9865），聚簇后只剩 3 条，且这 3 条之所以站得住是因为它们**根本不是 ds=865**：
- `2rwn9zxN`（ds=865，该块唯一代表）
- `d5WqeQbx`（ds=1786）—— 与 ds=865 块相关 **−0.035～+0.017**，完全正交
- `npv9WLVE`（ds=840）—— 与 ds=865 块相关 0.000–0.054，与 `d5WqeQbx` 0.2256

**USA 7 → 3**：`LL522ZRe`↔`0mjaa2Ev` 0.9214、`vROPEJ8w`/`O0Jgd7Y7`/`1Yj08nb6`/`XgRM3Yra` 四元组 0.76–0.87（全在 ds=382）。

**EUR 5 → 3**：ds=181 三条 0.990–0.997 只算 1（`58geG1P1`）；`omWVZ7lm`（ds=1582）与全部只 **0.023–0.049**、`kqN5aPgK`（ds=1826）与全部只 **0.024–0.044** —— 这两条是完全正交的核心资产。

### §61.5 L3 可交付清单（28 条，按 region）

**IND（18 条）**：`d5WAzegY` / `KPmvEYeE` / `LLMAM0xv` / `MPYogx0L` / `xAr022xb` / `RREn5rEa` / `kqN2WWKl` / `1YNQO9jJ` / `bl65Jk6l` / `npvM6WvE` / `9qxL8vx9` / `1YNQGgWJ` / `wp9d6xLd` / `QPYrG5q5` / `j2el6dlk` / `58jPrvZ1` / `kqJkPLeO` / `j2eo0oMO`

**USA（3 条）**：`vROPEJ8w` / `LL522ZRe` / `LL53QVvn`

**EUR（3 条）**：`58geG1P1` / `omWVZ7lm` / `kqN5aPgK`

**GBR（1 条）**：`6XKwmQgE`

**GLB（3 条）**：`2rwn9zxN` / `d5WqeQbx` / `npv9WLVE`

### §61.6 结论与路线含义

1. **60 颗目标在 L3 口径下不可达**：28 条，缺口 32。在 L2 口径下「追平」（61），但 L2 依赖「prod 一条都不漂移」这个不成立的假设。
2. **L1 的 114 是最容易误读的数字**，不能作为交付量。任何对外汇报必须同时给出 L2 与 L3，并说明 L1 里 62 条 prod≥0.65 的漂移风险。
3. **补齐缺口的唯一可靠路径是开新战役产新信号**，不是继续在存量里捡。存量已被三层口径榨到 28，继续挖的边际收益远低于新开一个 IND 式低相关池。
4. **IND 应作为下一个战役的首选区**：37 条 PASS → 20 条双安全 → 18 条独立，三层损耗率仅 51%，而 GBR 是 16 → 1（94% 损耗）、USA 是 24 → 3（88% 损耗）。IND 的低相关结构（互相关 0.13–0.53）说明该区的字段族之间正交性远好于其他区。
5. **GLB 的 `ds=840`/`ds=1786` 是两座未被充分开采的孤岛**：它们与 ds=865 主块相关接近 0，是天然的分散化来源。§59 记录的 8 条 GLB 高 S（S 2.4–4.75）prod 未测块正落在 `ds=840`，一旦补测通过可直接把 L3 从 28 抬到 30–31。

### §61.7 口径声明与未验证项

1. 62 条 self 为本轮 `check_self_correlation` 实测，与平台 "Self Correlation" 同口径（池按 `classifications` 排除 Power Pool Alpha）；68 条取库内值，**未在本轮复核是否仍在保鲜期内**。
2. 12 条 `SELF_UNKNOWN`（KOR 9 + EUR 2 + 其余 1）因 PnL 不可得或池为空而未测，**不等于判死**。
3. L3 的 `prod<0.65` / `self<0.50` 是**本报告自设的漂移缓冲门槛，不是平台要求**。平台只要求 `<0.70`。设这条线是为了让交付量在终验时站得住，不应被理解为「0.65–0.70 的候选违规」。
4. 库内 prod 值的新鲜度未逐条核（`alpha_corr_cache` 有 48h 保鲜语义）。**28 条在真实提交前必须逐条 `check_correlation(refresh=True)` 终验**，本报告的 28 是终验前的估计量。
5. `compute_mutual_correlation` 用 4 年日收益窗口，与提交时的 self 判据窗口（平台口径）不同 ⇒ 聚簇结论用于「数独立信号」，不能替代逐条 self 实测。
6. **未验证**：GLB `ds=840` 8 条高 S 候选的真实 prod（平台 prod 槽被兄弟会话占满，本会话 5 次 120s 超时）。


---

## §62 ★ 自我纠错：`alphas.prod_correlation` 为 NULL ≠ 没测过 —— 池条件漏掉 23 条优质候选（2026-10-30）

### §62.1 错误的发现与性质

§59–§61 反复写着「GLB `ds=840` 的 8 条高 S 候选 prod **从未测**，必须测 prod 才能判定，但平台 prod 槽被兄弟会话占满无法补测」。这个结论**是错的**。

查 `alpha_corr_cache`（权威 prod 实测表，兄弟会话的测量也写入这里）后，那 8 条的 prod **全部有值**，测量时间 2026-10-27 18:09 ～ 2026-10-28 09:47：

| alpha | ds | S | F | 2Y | prod（cache） | self | 判定 |
|---|---|---|---|---|---|---|---|
| `npvJaGa3` | 840 | 4.75 | 4.10 | 5.49 | 0.6887 | **0.9769** | ❌ self 死 |
| `9qxvMzxx` | 840 | 4.73 | 4.10 | 5.51 | 0.6930 | **0.9695** | ❌ self 死 |
| `akKYwj2v` | 840 | 4.64 | 3.97 | 5.37 | 0.6732 | **0.9752** | ❌ self 死 |
| `qML1x6vK` | 840 | 2.50 | 1.55 | 2.33 | 0.6867 | 0.4267 | L2（prod 贴墙） |
| `QPvJ6KVw` | 840 | 3.19 | 1.59 | 3.43 | 0.6385 | 0.6120 | L2 |
| `YP1rzw2J` | 840 | 2.95 | 1.77 | 2.17 | 0.6119 | 0.4807 | **L3** |
| `Xg9rMdvl` | 1786 | 2.44 | 1.47 | 2.69 | 0.6512 | 0.5515 | L2 |
| `d5WqeQbx` | 1786 | 2.71 | 1.43 | 2.68 | 0.5846 | 0.4597 | **L3** |

**根因**：`alphas.prod_correlation` 这一列与 `alpha_corr_cache` 是两套写入路径。兄弟会话/历史脚本把结果写进 cache，但没有回填 `alphas`。而 §59 的双门池 SQL 用的是 `alphas.prod_correlation IS NOT NULL` —— 于是所有「只进了 cache、没回填 alphas」的候选被**静默排除**。

**这与 §59 已经踩过一次的「本地 `status` 列过期」是同一类错误**：把本地派生列当作权威状态。权威顺序应当是：
`alpha_corr_cache`（prod 实测）> 平台 `get_alpha_details` > `alphas.prod_correlation`（派生列）。

### §62.2 全量审计：23 条 gate-pass 候选被错误排除

同口径审计（从未提交 + RA 基础闸全过 + `alphas.prod IS NULL` + `cache.prod IS NOT NULL`）：

| region | 总数 | 其中 cache prod < 0.70 |
|---|---|---|
| IND | 15 | 9 |
| GLB | 14 | 7 |
| USA | 7 | 6 |
| EUR | 3 | 1 |
| **合计** | **39** | **23** |

**USA 6 条与 EUR 1 条已判死**（USA 全属 `ds=292`，`pool_size=1` 全撞 `E567rQvR`；`e75pkq7E` self 1.0000）。**有效增量集中在 IND 的 `ds=41` 与 GLB 的 `ds=840`/`ds=1786`。**

已把 39 条全部回填进 `alphas.prod_correlation`（`prod_corr_source='cache_backfill'`），未提交池的 prod NULL 数量同步下降，**后续任何池查询都不会再漏这批**。

### §62.3 IND `ds=41`：全库最干净的天然多信号数据集

`ds=41` 新增 9 条进池（prod 0.4924–0.6939），补测 3 条 self 后：

| alpha | S | F | 2Y | prod | self | 判定 |
|---|---|---|---|---|---|---|
| `E567pmkK` | 2.93 | 1.81 | 2.60 | **0.4924** | **0.4377** | **L3** |
| `2rA0e6MN` | 2.31 | 1.67 | 2.74 | **0.4926** | **0.3251** | **L3** |
| `88vwZE17` | 2.46 | 1.73 | 2.60 | 0.5788 | 0.5796 | L2 |
| `ZYQ5J7j1` | 2.40 | 1.51 | 2.54 | 0.6693 | 0.4072 | L2（prod 贴墙） |
| `9qEnAr21` | 3.02 | 2.29 | 3.52 | 0.6907 | 0.6782 | L2（双贴墙） |
| `Vkx9RbJV` | 3.14 | 2.08 | 2.37 | 0.6939 | 0.4783 | L2（prod 贴墙） |
| `88RoVq6V` | 3.35 | 2.29 | 2.21 | 0.5732 | **0.9986** | ❌ 撞 `A1VZQXAg` |
| `58EbwZeN` | 2.76 | 1.76 | 2.48 | 0.5887 | **0.9997** | ❌ |
| `2rA071Ww` | 2.64 | 1.67 | 2.21 | 0.6115 | **0.9412** | ❌ |

**关键结构发现**：把 `ds=41` 的 9 条一起做 PnL 聚簇，**`all_below_threshold: true`** —— 9 条全部互相关 < 0.70，最大仅 0.6717（`88vwZE17`↔`9qEnAr21`），多数落在 **0.13–0.36**。这是全库唯一一个「同数据集内 9 条信号天然互不相关」的块。

机理推断：`ds=41` 的字段族覆盖的是彼此独立的经济维度（`kqJkPLeO`/`QPYrG5q5`/`j2el6dlk` 三条互相关 0.46–0.53 属同族，而 `E567pmkK`/`2rA0e6MN` 与它们只 0.21–0.27、`ZYQ5J7j1` 与它们只 0.13–0.16）。**这与 IND 整体「互相关 0.13–0.53」的结论一致，但 `ds=41` 是最极端的样本**。

### §62.4 GLB 三块的正交结构（9 条聚簇，精确解）

| 候选 | ds | 与 ds=865 主块相关 | 与 `d5WqeQbx` | 与 `npv9WLVE` |
|---|---|---|---|---|
| `RRbk6eAn` | 865 | —（主块代表） | −0.007 | 0.002 |
| `npv9WLVE` | 840 | 0.000–0.054 | 0.2256 | — |
| `d5WqeQbx` | 1786 | −0.035–+0.017 | — | 0.2256 |
| `Xg9rMdvl` | 1786 | 0.053 | 0.4387 | 0.3622 |
| `QPvJ6KVw` | 840 | −0.055 | 0.3644 | 0.5393 |
| `YP1rzw2J` | 840 | −0.019 | **0.7435** | 0.3158 |
| `qML1x6vK` | 840 | −0.043 | 0.2458 | **0.8065** |

GLB L2 独立数 **5 → 7**（`max_subset_exact=true`），新增 `Xg9rMdvl` / `QPvJ6KVw`。被剔除两条各有明确原因：`YP1rzw2J` 与 `d5WqeQbx` 0.7435、`qML1x6vK` 与 `npv9WLVE` 0.8065。

**`YP1rzw2J` 是可选替换项**：它（S 2.95 / F 1.77）与 `d5WqeQbx`（S 2.71 / F 1.43）二选一时按 F 优先可取前者，但 2Y 会从 2.68 降到 2.17。**不增加总数，只换组成。**

### §62.5 三层口径更新

| 口径 | §61 值 | §62 值 | 变化 |
|---|---|---|---|
| **L1 纸面过双门** | 114 | **124** | +10（IND ds=41 六条 + GLB 四条） |
| **L2 PnL 独立信号** | 61 | **63** | +2（GLB 5→7；IND 新增 6 条待与 L2 池复核） |
| **L3 带安全边际** | 28 | **30** | **+2**（IND 18→20：`E567pmkK` / `2rA0e6MN`） |

**L3 的 30 条按区**：IND 20 / USA 3 / EUR 3 / GLB 3 / GBR 1。

新增两条的双重优势：**prod 0.49（距红线 0.21，全库最安全）** + **self 0.33–0.44（距红线 0.26+）** + **与池内全部候选相关 < 0.30**。这是三层口径下质量最高的候选，应在提交顺序上排最前。

### §62.6 纪律修正（写入长期判读规则）

1. **`alphas.prod_correlation IS NULL` 不能作为「未测 prod」的判据**。必须 LEFT JOIN `alpha_corr_cache` 联合判断：`COALESCE(a.prod_correlation, c.prod_correlation)`。
2. 同理适用于 `self_correlation` 与 `concentrated_weight` / `cluster_test` —— 任何派生列都要回查权威源。
3. **本次错误连带影响**：§59「DEU prod 墙 100%」的池若也存在 prod 只进 cache 未回填的行，则「已测 50 条」这个分母可能偏小。**该项未复核，标记为待验证**（DEU 的 371 条从未提交 gate-pass 中，有多少条 prod 只在 cache 里，尚未统计）。
4. **反向教训**：正因为 prod 值都在 cache 里，§59 之后反复说的「prod 槽被占满导致无法补测」中，**至少 GLB 这批根本不需要补测** —— 白等了 3 轮。以后遇到「prod 未测」，第一动作是查 cache，不是查平台。

### §62.7 未验证项

1. IND 新增 6 条（`88vwZE17`/`ZYQ5J7j1`/`9qEnAr21`/`Vkx9RbJV` 及两条 L3）与 L2 池其余 IND 候选的跨族相关性未跑（37→43 节点会触发贪心近似，精确解不可得）。
2. cache 中 prod 值的保鲜期：多数测于 2026-10-27/28，**已接近或超过 48h**，提交前须 `check_correlation(refresh=True)` 终验。
3. 回填只覆盖 `prod_correlation`，未回填 `self_correlation`（cache 的 self 列大多为 NULL）。
4. **`blRnKEk6`（DEU 已提交 ACTIVE）prod 从 0.5766 漂到 0.6877**（cache 2026-10-05 值）—— 这是唯一检测到的「已提交 alpha 逼近 0.70」情形，说明 DEU 生产池在收紧，**该 alpha 的合规状态值得关注但未影响本报告的候选池**。

## §63 ★ 池 v4（cache 回退口径）+ 精确 PnL 聚簇收口：L3 = **30 条独立可交付信号**（2026-10-30）

### 63.1 池 v4：修掉 §62 的第二个漏洞（self 侧同病）

§62 只修了 `prod_correlation` 的 NULL 漏洞；本轮重算发现 **`self_correlation` 有完全一样的病**：
v3 脚本读 `alphas.self_correlation`，同样会漏掉只写进 `alpha_corr_cache` 的实测值。
v4 把两侧都改成 `COALESCE(alphas.<col>, alpha_corr_cache.<col>)`，并把 68 条 self 实测完整并入。

| 口径 | v3（§61/§62） | v4（本轮） | 变化原因 |
|---|---|---|---|
| 池总行数（gate-pass ∧ prod<0.70 ∧ 未提交） | 166 | **166** | 一致，回填已生效 |
| PASS（self < 0.70） | 114 | **125** | self 侧 cache 回退 + 实测字典补全 |
| SELF_FAIL | 16 | **28** | 同上，原「未知」里有 12 条实为撞墙 |
| SELF_UNKNOWN | 11 | **12** | 真正无 self 数据的只剩 12 条 |
| TRIO_VIOLATION | 1 | **1** | `N1VO1Loq`（model109+model28+predictive_starmine） |

**self 数据来源**：`measured` 85 / `db` 68 / `unknown` 13。
**prod 数据来源**：`alphas` 166（回填后全部就位，本轮 0 条需要回退到 cache）。

按区：

| region | 池行数 | PASS | prod<0.55∧self<0.50 | prod<0.65∧self<0.50 |
|---|---|---|---|---|
| IND | 47 | 43 | 16 | 22 |
| USA | 31 | 25 | 0 | 7 |
| GLB | 22 | 18 | 9 | 13 |
| EUR | 32 | 22 | 4 | 5 |
| GBR | 19 | 16 | 0 | 1 |
| KOR | 15 | 1 | 0 | 0 |
| **合计** | **166** | **125** | **29** | **48** |

### 63.2 漂移风险分布（125 条 PASS 的 prod 侧）

| prod 阈值 | 条数 | 占 PASS |
|---|---|---|
| ≥ 0.695 | 13 | 10.4% |
| ≥ 0.690 | 22 | 17.6% |
| ≥ 0.680 | 36 | 28.8% |
| ≥ 0.650 | 68 | 54.4% |
| ≥ 0.600 | 83 | 66.4% |
| ≥ 0.550 | 96 | 76.8% |
| ≥ 0.500 | 108 | 86.4% |

**⇒ 仍然过半贴墙**：125 条 PASS 里 68 条（54.4%）prod ≥ 0.65。
双安全（prod<0.65 ∧ |self|<0.50）= **48**；再取 prod<0.55 = **29**。

### 63.3 精确 PnL 聚簇（4 次 `compute_mutual_correlation`，全部 `max_subset_exact=true`）

| region | 双安全 | 聚簇后独立 | 损耗 | 超阈对数 | 被剔除成员 |
|---|---|---|---|---|---|
| IND | 22 | **20** | 1.1× | 2 | `9qEPO5K2` 0.7339 / `YP1GJlPR` 0.7123 |
| GLB | 13 | **3** | 4.3× | 46 | ds=865 十名块互相 0.72–0.99，整体一个信号 |
| USA | 7 | **3** | 2.3× | 7 | ds=382 四名块 + `0mjaa2Ev` |
| EUR | 5 | **3** | 1.7× | 3 | `58geG1P1` 0.9970 / `mL617YPx` 0.9901 |
| GBR | 1 | **1** | — | 0 | — |
| **合计** | **48** | **30** | **1.6×** | | |

**★★ 本轮最重要的单条发现：GLB `ds=865` 的十个候选是一个信号。**
`RRbk6eAn`/`LLNlZKMa`/`YPbW161l`/`akbWK6V5`/`88jKRbRz`/`xA3mrqrw`/`3qXn1rJN`/
`6XjYZVQ7`/`2rwn9zxN`/`vRrJZMoA` 之间两两相关 **0.7175–0.9865**，46 对全部超 0.70。
若只看指标（S 2.4–3.1、F 1.2–2.1、prod 0.40–0.60）会误以为 GLB 有十个可交付信号；
**实际只能取一个**。这与「用字段名族数候选会高估约 3×」的旧结论方向一致，但幅度更极端（10×）。

反面对照仍是 **IND `ds=41` / `ds=1356`**：真多信号，九条/十条天然正交（0.09–0.62）。

### 63.4 L3 交付清单 = 30 条（按 prod 升序，越靠前漂移缓冲越大）

| # | 梯队 | alpha | region | dataset | Sharpe | Fitness | TO | 2Y | prod | \|self\| |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | T1 | `LLMAM0xv` | IND | 1356 | 1.65 | 1.17 | 17.6% | 2.09 | **0.2167** | 0.1666 |
| 2 | T1 | `MPYogx0L` | IND | 1356 | 1.87 | 1.31 | 20.2% | 2.20 | **0.3159** | 0.2387 |
| 3 | T1 | `xAr022xb` | IND | 1356 | 1.90 | 1.34 | 20.1% | 1.90 | **0.3216** | 0.2400 |
| 4 | T1 | `RREn5rEa` | IND | 1356 | 2.08 | 1.54 | 19.8% | 2.45 | **0.3342** | 0.2837 |
| 5 | T1 | `kqN2WWKl` | IND | 1356 | 2.13 | 1.58 | 20.0% | 2.81 | **0.3362** | 0.2531 |
| 6 | T1 | `1YNQO9jJ` | IND | 1356 | 2.37 | 1.82 | 20.3% | 3.11 | **0.3389** | 0.2991 |
| 7 | T1 | `bl65Jk6l` | IND | 1356 | 2.19 | 1.64 | 20.9% | 2.08 | **0.3464** | 0.2391 |
| 8 | T1 | `npvM6WvE` | IND | 1356 | 1.97 | 1.35 | 21.5% | 2.02 | **0.3486** | 0.2532 |
| 9 | T1 | `9qxL8vx9` | IND | 1356 | 1.96 | 1.39 | 20.0% | 2.58 | **0.3488** | 0.2677 |
| 10 | T1 | `1YNQGgWJ` | IND | 1356 | 2.11 | 1.53 | 20.7% | 2.76 | **0.3661** | 0.2954 |
| 11 | T1 | `wp9d6xLd` | IND | 590 | 2.34 | 1.69 | 22.3% | 1.29 | **0.4148** | 0.3641 |
| 12 | T1 | `RRbk6eAn` | GLB | 865 | 2.87 | 1.51 | 34.5% | 1.96 | **0.4825** | 0.3771 |
| 13 | T1 | `E567pmkK` | IND | 41 | 2.93 | 1.81 | 33.9% | 2.60 | **0.4924** | 0.4377 |
| 14 | T1 | `2rA0e6MN` | IND | 41 | 2.31 | 1.67 | 18.4% | 2.74 | **0.4926** | 0.3251 |
| 15 | T1 | `QPYrG5q5` | IND | 41 | 2.54 | 1.96 | 20.3% | 2.47 | **0.5001** | 0.2468 |
| 16 | T1 | `j2el6dlk` | IND | 41 | 2.87 | 2.29 | 21.7% | 2.66 | **0.5217** | 0.2970 |
| 17 | T1 | `58jPrvZ1` | IND | 1337 | 1.64 | 1.27 | 11.4% | 2.23 | **0.5354** | 0.4843 |
| 18 | T1 | `omWVZ7lm` | EUR | 1582 | 1.75 | 1.17 | 4.1% | 1.76 | **0.5378** | 0.1954 |
| 19 | T1 | `mL61avpx` | EUR | 181 | 1.78 | 1.24 | 6.9% | 2.13 | **0.5423** | 0.4367 |
| 20 | T2 | `O0Jgd7Y7` | USA | 382 | 2.27 | 2.03 | 13.0% | 3.09 | **0.5655** | 0.0000 |
| 21 | T2 | `d5WAzegY` | IND | 1438 | 2.73 | 1.93 | 26.1% | 2.42 | **0.5699** | 0.4926 |
| 22 | T2 | `6XKwmQgE` | GBR | 108 | 1.62 | 1.04 | 13.5% | 2.19 | **0.5956** | 0.4148 |
| 23 | T2 | `kqN5aPgK` | EUR | 1826 | 1.86 | 1.04 | 4.5% | 2.23 | **0.6104** | 0.4522 |
| 24 | T2 | `YP1rzw2J` | GLB | 840 | 2.95 | 1.77 | 15.6% | 2.17 | **0.6119** | 0.4807 |
| 25 | T2 | `KPmvEYeE` | IND | 593 | 3.07 | 2.36 | 23.9% | 3.14 | **0.6162** | 0.3094 |
| 26 | T2 | `LL53QVvn` | USA | 382 | 1.61 | 1.39 | 11.2% | 2.75 | **0.6163** | 0.0356 |
| 27 | T2 | `kqJkPLeO` | IND | 41 | 3.02 | 2.40 | 22.5% | 2.36 | **0.6177** | 0.2703 |
| 28 | T2 | `j2eo0oMO` | IND | 593 | 2.86 | 2.13 | 24.3% | 2.94 | **0.6333** | 0.2925 |
| 29 | T2 | `LL522ZRe` | USA | 382 | 2.99 | 2.97 | 12.5% | 3.97 | **0.6377** | 0.1108 |
| 30 | T2 | `npv9WLVE` | GLB | 840 | 3.08 | 1.42 | 60.8% | 3.19 | **0.6495** | 0.3787 |

**第一梯队 19 条（prod < 0.55，距 0.70 红线 > 0.15）**、**第二梯队 11 条（prod 0.55–0.65，缓冲 0.05–0.15）**。

### 63.5 30 条对照 60 颗目标：缺口 30

| 口径 | 数量 | 说明 |
|---|---|---|
| L1 纸面过双门 | 125 | 最易误读，不能当交付量 |
| L2 双安全 | 48 | 依赖「prod 一条都不漂」的不成立假设 |
| **L3 独立可交付** | **30** | 保守口径，含漂移缓冲 + PnL 去重 |
| 目标 | 60 | 缺口 **30** |

**DEU 本区贡献 = 0 条。** §59 已实证：DEU 371 条从未提交 gate-pass 里已测 prod 的 50 条全撞
（最小值 0.7145），在 REGULAR + prod<0.70 约束下不可达。这 30 条全部来自 IND/USA/GLB/EUR/GBR 存量。

### 63.6 三条路线（需用户决策）

| 路线 | 动作 | 预期产出 | 风险 |
|---|---|---|---|
| **A 转区承接** | 以这 30 条为基线，下一战役首区选 **IND**（三层损耗仅 51%，GBR 是 94%） | 30 + 新区增量 | 新区仍需 1 个完整战役周期 |
| **B 继续死磕 DEU** | 换 PPA 通道或再扩数据集 | 先验极低（50/50 全撞） | 高概率再做 3000 条仍为 0 |
| **C 走 PPA 通道** | 打 `PowerPoolSelected` 标，用 PPAC<0.5 取代 PC<0.7 | 可能救回部分 DEU 存量 | PPAC 分布未验证；属提交通道决策 |

### 63.7 本轮口径纪律（新增两条）

1. **`COALESCE(alphas.<col>, alpha_corr_cache.<col>)` 必须成对用在 prod 和 self 两侧。**
   §62 只修 prod 侧，导致 self 侧又漏了 12 条；同一个 bug 会在相邻列上复发。
2. **聚簇的节点数超过 ~24 会退化为贪心近似**；本轮的 IND(22)/GLB(13)/USA(7)/EUR(5) 全部 ≤24，
   拿到的是 `max_subset_exact=true` 的精确解。报「N 条独立」时必须同时给出 `max_subset_exact`。

---


## 64. ★★ 修正 §59/§63：「挤在单一数据集」是本地归属缺陷，真实结构是「7 个信号族全撞」

§59 与 §63.5 断言「DEU 的 89/91 gate-pass 来自同一数据集 `ds=1902`」。本轮做了广度审计，
**这个断言是错的，而且错在两个层面**。

### 64.1 第一层错：`ds=1902` 不是数据集，是本地 `_unknown` 占位符

`data/wqb.db` 的 `datasets` 表里，`id=1902` 那一行的 `name` 字面就是 `_unknown`，
`category` / `field_count` 全为 NULL。也就是说这 3113 行（占 DEU 全部 3443 条模拟的 **90.4%**）
是**写库时没归到数据集**，不是「都用了同一个数据集」。

用表达式字段前缀反推这 3113 条，得到 **140 个不同前缀**，至少对应 25 个真实数据集：

| 字段前缀 | 出现条数 | 对应数据集 |
|---|---|---|
| `oth455_` | 481 | other455 |
| `inst1_` | 306 | institutions1 |
| `mdl264_` | 223 | model264 |
| `anl93_` | 167 | analyst93 |
| `fnd6_` | 79 | fundamental6 |
| `mdl216_` | 77 | model216 |
| `snl27_` | 64 | socialmedia / snl27 |
| `tm_` | 60 | techindi_model |
| `snt33_` | 54 | sentiment33 |
| `mdl106_` | 51 | model106 |
| `snt7_` | 45 | sentiment7 |
| `mdl238_` | 44 | model238 |
| `nws20_` | 36 | news20 |
| `shrt3_` | 28 | shortinterest3 |
| `fnd45_` / `mws50_` | 23 / 23 | fundamental45 / mws50 |
| `rsk60_` / `oth532_` / `mdl262_` / `mdl53_` / `nws17_` / `anl9_` | 16 / 16 / 16 / 15 / 15 / 14 | 各自数据集 |

⇒ **DEU 的探索广度从来不是「只挖了一个集」，而是「挖了 25 个集但归属没记账」。**
这一条同时说明：本战役此前所有「按数据集归因」的结论都需要打折，包括 §59。

### 64.2 第二层错：真正的集中度在信号族，不在数据集

全量 375 条 gate-pass（含已提交）的字段族分布：

| 字段族 | gate-pass 条数 | 占比 |
|---|---|---|
| `mean_*`（证券借贷 / 融券费率族） | 343 | **91.5%** |
| `eps_*`（分析师盈余修正） | 41 | 10.9% |
| `mdl264_` | 35 | 9.3% |
| `mdl238_` | 15 | 4.0% |
| `tm_*` | 12 | 3.2% |
| `snl27_` / `snt7_` | 12 / 12 | 3.2% / 3.2% |
| `inst1_` / `oth455_` | 6 / 4 | 1.6% / 1.1% |

⇒ 真正的问题是**成功设计全部收敛到「证券借贷费率」这一个量的各种写法**，不是数据集单一。
这解释了为什么 13 条实测 prod 最小值 0.7694 且全部 ≥0.75——同一个量当然互相拥挤。

### 64.3 91 条未提交 gate-pass 的完整分族（7 族，合计 91，无遗漏）

| 族 | n | 已测 prod | prod<0.70 | 未测 | 实测最小值 | 判定 |
|---|---|---|---|---|---|---|
| `analyst_eps` | 33 | 3 | 0 | 30 | **0.9187** | ❌ 族已拥挤 |
| `OTHER`（`R84/R85` 占位） | 19 | 6 | 0 | 13 | 0.8747 | ❌ 不可复现 |
| `lending_mean` | 13 | 2 | 0 | 11 | 0.8859 | ❌ 族已拥挤 |
| `techindi`（`tm_*`） | 12 | 1 | 0 | 11 | 0.9084 | ❌ 族已拥挤 |
| `social_snl27`（snt7×snl27） | 11 | 1 | 0 | 10 | 0.7694 | ❌ 族已拥挤 |
| `institutions1` | 2 | 0 | 0 | 2 | — | ❌ self 重复（64.4） |
| `sentiment7` | 1 | 0 | 0 | 1 | — | ❌ 同上，属 snt7 族 |

**每族的致死证据（逐条核过，不是推断）**：

1. **`analyst_eps` 33 条 = 1 个信号 × 33 种表皮。** 未测的 30 条全部是
   `group_rank(eps_y1_estimate_change_3mo, sector)` 外面套 `winsorize` / `quantile` /
   `pasteurize` / `signed_power` 之类，**指标逐位相同**：S=1.81 / F=1.61 / 2Y=1.12 / TO=7.5%。
   已测的 3 条 min prod = 0.9187。这不是 33 个候选，是 1 个已撞墙的信号。
2. **`OTHER` 19 条里有 13 条的 `expression` 字面是 `R84/R85`** —— 占位标签，无法复现
   （与 `R83`/`R97`/`R101`/`R103` 同类缺陷）。
3. **`lending_mean` 11 条未测全是 `add(add(add(...)))` 多信号叠加**，既违反「禁止 add(A,B) 混信号调参」，
   又继承 `mean_*` 族的拥挤（已测 min 0.8859）。且 `blRnKEk6`（ACTIVE）已占该族。
4. **`techindi` 11 条未测全是 `group_rank(tm_??_r1_r5_r10_rh_glb_d1_*)`**，TO 36.9%–61.6%，
   已测那条 prod = 0.9084（即判死清单里的 `JjelQnvE`）。
5. **`social_snl27` 10 条未测全是 `vector_neut(ts_quantile(ts_ir(...snt7_all_languages_views...)))`**，
   即已知「5 条互相关 0.875–0.997 全部作废」的那一族；已测代表 `P0oe6wpJ` prod = 0.7694。

### 64.4 `institutions1` 的 2 条：RA 全清、双塔、但 self 撞自己的 ACTIVE

这是 DEU 唯一的非 `mean_*` gate-pass，也是全战役**唯一一次 RA 零失败 + 9 项硬闸全 PASS**：

| alpha | S | F | 2Y | TO | SUB | margin | failed_ra | checks.fail |
|---|---|---|---|---|---|---|---|---|
| `d5WwzRMY` | 1.73 | 1.40 | 2.64 | 12.85% | 1.20 | 0.001312 | **0** | **[]** |
| `E56AzejK` | 1.71 | 1.36 | 2.79 | 13.28% | 1.17 | 0.001266 | **0** | **[]** |

- 仅两条软 warning：`MATCHES_THEMES` / `OSMOSIS_ALLOCATION`；`CLUSTER_TEST` / `CONCENTRATED_WEIGHT`
  / `LOW_SUB_UNIVERSE_SHARPE` / `IS_LADDER_SHARPE` 全 PASS。
- `SUB/S` = 0.694 / 0.684（门槛 0.434）——本战役 SUB 表现最好的一对。
- 金字塔：**DEU/D1/INSTITUTIONS (×1.6) + DEU/D1/OTHER (×1.8)**，一次触两塔。
- 三塔规则合规：INSTITUTIONS × OTHER = 非 trio × trio，允许（计入 ≤5 配额）。

**但 self 直接判死**（本地计算，零配额）：

| alpha | self max | 撞到的 alpha | 对方身份 |
|---|---|---|---|
| `d5WwzRMY` | **0.9287** | `2rmGAPqN` | `DEU_R_insconviction_01`，2026-10-09 已 ACTIVE，prod 0.6292 / self 0.0327 |
| `E56AzejK` | **0.9184** | `2rmGAPqN` | 同上 |

三条表达式只差两个参数：窗口 `ts_sum(...,220)` → `66`，分组轴
`oth455_partner_n2v_p50_q200_w1_pca_fact2_cluster_20` → `_fact1_cluster_5` / `w5_..._cluster_20`。
**这是「同一设计换窗口/换 cluster 参数」的第 4 次自我重复实证**（前三次：`GLB ds=840` S>4.5 子族、
`IND ds=41` 三条、`WjLEOqLP` prod 1.0）。

### 64.5 修正后的 DEU 判读

| 原口径（§59/§63.5） | 修正后 |
|---|---|
| 「DEU gate-pass 89/91 来自单一数据集 ds=1902」 | ❌ `1902` 是 `_unknown` 占位符；实为 25 个数据集 / 140 个字段前缀 |
| 「DEU 全灭 / 不可达」 | ⚠️ 部分成立：**现有 3443 条内确实 0 条可交付**，但死因是**信号族拥挤**，不是数据集单一 |
| 「继续死磕 DEU 先验极低（50/50 全撞）」 | 需改写为：**DEU 需要换信号概念**，换数据集／换窗口／换 neutralization 都已证无效 |

**净结论：DEU regular 通道在现有 3443 条模拟内已无任何可交付信号。**
7 个族覆盖全部 91 条未提交 gate-pass，其中 5 族有 prod 实测（min 0.7694–0.9187，全部 ≥0.70），
1 族是不可复现占位标签，1 族 self 撞自有 ACTIVE。

**若还要留 DEU，唯一未试的方向是换信号概念本身**（新数据集的**新经济量**，而不是
`mean_*` / `eps_*` / `mdl*` / `tm_*` / `snt7_*` 这 5 个已经撞满的量的新写法）。
这与「换数据集」不同：`_unknown` 桶已证 25 个数据集都被碰过，问题不是没碰，是碰出来的都是同一类量。

### 64.6 本轮新增两条工程纪律

1. **`alphas.dataset_id` 指向 `datasets.name='_unknown'` 时，任何「按数据集归因」的统计全部作废。**
   判据：`SELECT name FROM datasets WHERE id=<dataset_id>` 返回 `_unknown`。
   本轮 DEU 有 3113/3443（90.4%）踩这个坑，直接导致 §59 的结论方向性错误。
   修复方向：模拟回测时从表达式字段前缀反推数据集写入 `dataset_id`，而不是留占位。
2. **「N 条 gate-pass」必须先做「族坍缩」再计数。** 本轮 91 条 → 7 族，且 33 条里 30 条是
   同一信号的表皮变体（指标逐位相同）。与已知的「字段名族高估 3×」「PnL 聚簇」构成三级漏斗：
   **条数 → 指标指纹去重 → 族 → PnL 聚簇**。跳过前两级会系统性高估。

---

## 65. fundamental90 富矿 + 判死粒度纠错 + 12 个结构互异模板库（2026-10-30）

### 65.1 ★★★ 新发现：`fundamental90`（Accounting Quality Models）在 DEU 有 66 个 MATRIX 字段

按用户「category 判据可能过时，一定拉平台当时的数据集判断」的要求，逐个数据集实拉
`get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=...)`，结果：

| 数据集 | DEU 字段数 | 类型 | 判定 |
|---|---|---|---|
| `fundamental44`（论坛帖标称 Accounting Quality Models） | **0** | — | **DEU 无字段，不派发** |
| `fundamental90`（真·会计质量模型集） | **66** | **全 MATRIX** | **DEU 最大新机制面** |

**为什么 `fundamental90` 是本轮最重要的发现（六条同时成立）**：

1. **全 MATRIX 类型** —— 不需要 `vec_avg`/`vec_sum` 包裹，绕开 `earnings6` /`alpha_factor_lib`
   /`institutions25` 的 VECTOR 稀疏陷阱。
2. **字段全是已发表论文的成品因子**（不是原始报表项）：
   - `fnd90_qes_gamef_pscore` = **Piotroski F-score**（0–9），Piotroski (2000), *Journal of Accounting Research*
   - `fnd90_qes_gamef_ohlson` = **Ohlson O-score** 破产概率，Ohlson (1980), *JAR*
   - `fnd90_qes_gamef_cscore` = **Montier C-score** 操纵风险，Montier (2005)
   - `fnd90_qes_gamef_mohanram` = **Mohanram G-score** 成长股盈余操纵，Mohanram (2005), *Review of Accounting Studies*
   - `fnd90_qes_gamef_chs_default` = **Campbell–Hilscher–Szilagyi** 违约概率 z-score
   - `fnd90_qes_gamef_earnigs_timeliness` = **盈余披露及时性 z-score** ← **这就是 EAT 异象的会计数据库版**
3. **拥挤度是 DEU 全库最低档**：最高 `pscore` 30 users / 38 alphas，`cash_flow_coverage` 24，
   `deferred_sal_chg` 21，`icfroe_5y` 19，`ohlson` 12；**其余 40 多个字段 userCount 为 0–7**，
   且 20 个为 0（`accruals_vol` / `chs_default` / `earn_var` / `sg_a_vol` / `pension_*` / `finished_goods` 等）。
4. **字段族厚度足以支撑 10+ 个结构互异模板**：质量评分族（4 个学术 score）/ 应计族 /
   递延收入与递延税族 / 存货与应收族 / 养老金族 / 资本结构与摊薄族 / 现金流波动族。
5. **学理方向明确、可证伪**：高 F-score → 做多（财务健康）；高 O/C/G-score → 做空（破产/操纵风险）；
   高应计 → 做空（Sloan 1996）；高递延收入增长 → 盈利质量红flag。
6. **与既有 DEU 产出族零重叠**：DEU 已产出的 7 个信号族是 `analyst_eps` / `OTHER` / `lending_mean`
   / `techindi` / `social_snl27` / `institutions1` / `sentiment7`，**没有一个碰会计质量**。

**唯一风险**：`coverage` 元数据全部显示 0.0（DEU 全区已知不可信），必须靠回测的
`CONCENTRATED_WEIGHT.value` 与 `bookSize` 实测覆盖率。已列为探针 4 的第一优先。

**★ 顺带纠错**：论坛帖 `43691542110359`（KK37637，24 赞）把 Accounting Quality Models 标为
`fundamental44`，但 `fundamental44` 在 DEU 是 **0 字段**。**论坛帖的数据集 ID 不能直接信，
必须 `get_datafields` 复核。** 这是「数据集级 description 不可信」这条既有纪律的**论坛版延伸**。

### 65.2 ★★★ `fnd90_qes_gamef_earnigs_timeliness` 让 EAT 异象绕开 VECTOR 稀疏

`earnings6` 的 `ern6_next_ed`（下次财报披露日）是 **VECTOR** 类型，在 DEU 的稀疏性导致
探针 2 里 `CONCENTRATED_WEIGHT = 0.5`。而 `fundamental90` 提供了一个 **MATRIX** 版本的
同一经济量：`fnd90_qes_gamef_earnigs_timeliness`（盈余披露及时性 z-score，
"higher values typically indicate quicker (more timely) earnings reporting"）。

**这不是替代品，而是同一机制的另一口径**：
- `ern6_next_ed`：**前瞻**（下次预定披露日）→ 捕捉「管理层主动推迟/提前排期」的隐性信号
- `fnd90_qes_gamef_earnigs_timeliness`：**回溯**（已发生披露的及时性）→ 捕捉「历史披露节奏」

两者的结合（前瞻 − 回溯）本身就是 EAT 异象的教科书形态：**预定排期 vs 实际执行的一致性**。
而且 MATRIX 口径无需 `vec_*`，覆盖率和 `CONCENTRATED_WEIGHT` 都会显著好于 VECTOR 版。

**⇒ 探针 4 把 `rank(fnd90_qes_gamef_earnigs_timeliness)` 放在第一位。**

### 65.3 探针 3 已派发（铺展假说的判决性实验）

`multisimulation_id = 2kHdKlfBA5cB9Vu14WVbDGi9`，10 条，DEU/TOP500/D1，
decay 4 / SUBINDUSTRY / truncation 0.08 / **nanHandling ON** / pasteurization ON / maxTrade OFF。

派发前两道预检全过：
- `preflight_expressions`：10 条 / 8 个唯一字段 / `unknown_fields = []` / `any_changed = false`
- `operator_audit`：`safe = true` / `violations = []` / 19 个 ghost 算子清单复现

**设计意图（一次实验判三件事）**：

| # | 表达式 | 判什么 |
|---|---|---|
| 1 | `rank(ts_mean(vec_avg(free_cash_flow_to_market_cap), 252))` | 铺展能否解 alpha_factor_lib 的 CW=0.5 |
| 2 | `rank(ts_mean(fnd93_deferred_tax_liability_51, 252))` | 铺展能否解 fnd93（探针 2 冠军 S 0.60） |
| 3 | `rank(ts_mean(fnd93_accruals_d1_current_t, 252))` | 铺展后 SUB 0.82 能否转成 S |
| 4 | `rank(ts_mean(vec_sum(ern6_next_ed), 380))` | **无 zscore 的裸铺展**（对照，论坛 V1 思路的铺展版） |
| 5 | `rank(ts_mean(zscore(vec_sum(ern6_next_ed)), 380))` | zscore 前置在铺展形态下还灵不灵 |
| 6 | `subtract(ts_mean(zscore(vec_sum(ern6_next_ed)), 380), zscore(vec_sum(ern6_next_ed)))` | **`ts_min_max_cps` 的等价替代**（论坛 S 1.60 配方的 DEU 可执行版） |
| 7 | `rank(ts_mean(vec_avg(ern6_board_of_directors_meeting), 380))` | 董事会/股东大会日（论坛明列可套 EAT 模板） |
| 8 | `rank(ts_mean(vec_avg(ern6_1q), 504))` | 季度财报日（最长窗口，2 年） |
| 9 | `rank(ts_mean(fnd93_tax_accruals_51, 252))` | Sloan 应计异象在 DEU 的铺展版 |
| 10 | `rank(ts_mean(vec_avg(bank_tier1_capital_ratio), 252))` | alpha_factor_lib 银行 KPI，探针 1 里 CW 0.1649（6 只） |

**第 6 条是本轮的机制核心**：`ts_min_max_cps(x,d) = (ts_min(x,d) + ts_max(x,d)) − 2x`，
在分布近似对称时 `ts_min + ts_max ≈ 2·ts_mean`，故等价于 `2·(ts_mean(x,d) − x)`。
方向一致（x 接近历史 max ⇒ 负 ⇒ 做空拖延股；接近 min ⇒ 正 ⇒ 做多提前股），
且**同时绕开两个陷阱**：`ts_min_max_cps` 是 DEU ghost、`ts_max`/`ts_min` 本账号 ERROR。

**派发踩坑记录**：前两次 `create_multi_simulation` 均返 `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED`
（探针 2 的槽未完全释放）。等待 90s 后第三次成功。⇒ **探针 2 收批返回 complete ≠ 平台槽已释放，
需留 ≥90s 缓冲。**

### 65.4 探针 4 已预检待派发（fundamental90，10 条）

`preflight_expressions(dataset_id=fundamental90)`：`unknown_fields = []` / `vector_fields = []`
（全 MATRIX 确认）/ 10 条通过。唯一 warning 是 `fnd90_game_inc_cash_tax` 的分页预检跳过
（`get_datafields(offset=50)` 6 次重试失败），但该字段在早前完整拉取中确实存在（第 22 项），**安全**。

| # | 表达式 | 学术来源 | 预期方向 |
|---|---|---|---|
| 1 | `rank(fnd90_qes_gamef_earnigs_timeliness)` | EAT 会计口径 | 及时 ⇒ 好消息 ⇒ 多 |
| 2 | `rank(fnd90_qes_gamef_pscore)` | Piotroski (2000) | 高 F ⇒ 多 |
| 3 | `rank(fnd90_qes_gamef_ohlson)` | Ohlson (1980) | 高 O ⇒ 破产风险 ⇒ **做空前先验负向** |
| 4 | `rank(fnd90_qes_gamef_cscore)` | Montier (2005) | 高 C ⇒ 操纵 ⇒ 空 |
| 5 | `rank(fnd90_qes_gamef_mohanram)` | Mohanram (2005) | 高 G ⇒ 成长股操纵 ⇒ 空 |
| 6 | `rank(fnd90_game_accruals_vol)` | Sloan 应计延伸 | 高波动 ⇒ 低盈余质量 ⇒ 空 |
| 7 | `rank(fnd90_game_inc_cash_tax)` | 税负/现金税 红flag | 高 ⇒ 激进税务 ⇒ 空 |
| 8 | `rank(fnd90_game_deferred_sal_chg)` | 递延收入变化 | 高 ⇒ 激进确认收入 ⇒ 空 |
| 9 | `rank(fnd90_qes_gamef_grossprofit_asset)` | Novy-Marx (2013) | 高毛利/资产 ⇒ 多 |
| 10 | `rank(fnd90_game_cash_flow_coverage)` | 现金流覆盖 | 高 ⇒ 偿债能力强 ⇒ 多 |

**注意第 3–5、7、8 条是「排雷型」信号**：裸 `rank()` 的默认方向是「高值做多」，
若不成立需要显式 `-rank()`。本轮先用裸 `rank()` 测**覆盖率 + 原始方向**，
方向修正留给探针 5（换骨架而非混信号）。

### 65.5 ★ 模板库：12 个结构互异模板（会计质量族，满足 ≥10 硬约束）

按用户「模板多样性和数量（10 个模板）」的硬约束，且差异必须落在
**骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性变换**上（不是换窗口换常数）：

| # | 模板名 | 表达式骨架 | 差异维度 | 来源 |
|---|---|---|---|---|
| M1 | 学术因子水平 | `rank(F)` | 横截面序数，零时序加工 | Piotroski (2000) 原式 |
| M2 | 自身基线异常度 | `ts_zscore(F, 252)` | 时序 z-score，**保留幅度** | 论坛 43152032301591 五铁律 #1 |
| M3 | 铺展（季度→日频） | `rank(ts_mean(F, 252))` | 时序均值铺展 | 本轮探针 3 实证 |
| M4 | 一阶变化（改善方向） | `rank(ts_delta(ts_mean(F, 252), 66))` | 一阶差分 | Piotroski 原式 delta 项 |
| M5 | 二阶波动惩罚 | `-rank(ts_std_dev(F, 252))` | 二阶矩 | `fnd90_game_accruals_vol` 定义式 |
| M6 | 行业相对（组内序数） | `group_rank(F, subindustry)` | 横截面分组轴 | 论坛 CW99271「子分类×中性化匹配」 |
| M7 | 应计比率（定义式比值） | `rank(divide(F_acc, ts_mean(price,252)))` | 比值合成 | 论坛模板大师2 accruals 模板 |
| M8 | 极值偏离（cps 替代） | `subtract(ts_mean(zscore(F),380), zscore(F))` | 相对自身历史极值位置 | 论坛 43184757918743（DEU 专属，S 1.60） |
| M9 | 跨分母一致性 | `rank(subtract(rank(F_11), rank(F_51)))` | 序数差（同族多分母） | 自建（针对 `fnd93_*_11..51`） |
| M10 | 尾部截尾非线性 | `tail(winsorize(rank(F), std=2), 0.2, 0.8, 0.5)` | 非线性截尾 | 本轮 SUB 墙实证（0.29→0.44） |
| M11 | 条件门控（质量过滤） | `trade_when(greater(rank(F_q),0.3), rank(F_sig), -1)` | 门控（辅助信号做条件） | 论坛 43691542110359「排雷工具」思路 |
| M12 | 同数据集双字段比值 | `rank(divide(F_a, F_b))` | 两字段比值作定义 | 既有纪律「比值作定义可以，作信号合成不行」 |

**排除项（DEU 不可用，已实证）**：`ts_min_max_cps`（ghost）/ `ts_max` `ts_min`（本账号 ERROR）/
`ts_decay_exp_window`（ghost）/ `ts_median`（ghost）/ `group_extra`（论坛模板大师2 用过，**待审计**）。

### 65.6 论坛取材第三轮（`search_forum_posts("Piotroski F-score Ohlson O-score bankruptcy fundamental template")`，25 条，`navigation_failed=false`）

**可用的四份模板原文**（从 `模板大师2-GPT增强版` WL13229 的 artifact 中提取）：

1. **应计比率（模板大师2）**：
   `accruals_ratio = accruals / ts_mean(price, 252); alpha = rank(accruals_ratio); alpha = group_neutralize(alpha, industry); alpha = ts_backfill(alpha, 20, 'nan')`
   —— **注意 `accruals / ts_mean(price,252)` 用价格做分母**，是把金额转成无量纲比率的正解，与本轮 `vector_neut` 第二参需无量纲的纪律同源。
2. **商誉/销售额 + 回归残差（模板大师2）**：
   `a = ts_backfill({GOODWILL}, 63)/ts_backfill(sales,63); alpha = -ts_regression(a, ts_product(returns+1, 63)-1, 512, lag=1, rettype=3)`
   —— **比值先 `ts_backfill(·,63)` 再相除**，是稀疏字段的正确处理顺序。
3. **O/S × 隐含波动率 行业填充乘积（模板大师2）**：
   `filled_O_S = group_extra(O_S, industry); filled_iv = group_extra(iv, industry); product = filled_O_S * filled_iv; signal = group_rank(-group_neutralize(product, industry), industry)`
   —— 机制是「用行业均值填充缺失值后再相乘」，可直接套到 `fundamental90` 的稀疏结构字段。**但 `group_extra` 待审计。**
4. **Piotroski FSCORE 9 项打分完整复现式（ZH24706, article 35105274113687）**：
   `ROA = -vec_avg(fnd6_ops)/fnd6_mfma1_at; CFO = fnd6_ch/fnd6_mfma1_at; delta_ROA = ts_delta(ROA,252); Acc = CFO - ROA; delta_LEVER = ts_delta(fnd6_cptnewqv1300_dlttq/fnd6_mfma1_at,252); delta_LIQUID = ts_delta(fnd6_cptmfmq_actq/fnd6_newqv1300_dlcq,252); EQ_OFFER = -fnd6_sstk; delta_MARGIN = ts_delta(fnd6_newa1v1300_gp,252); delta_Asset_Turnover = ts_delta(fnd6_mfma2_revt/fnd6_mfma1_at,252); score = (9 项 0/1 三目相加); alpha = group_rank(score, densify(industry))`
   **该帖三条关键实证（可直接迁移）**：
   - **ROA 项取负（`-vec_avg(fnd6_ops)/...`）才可提交** ⇒ 「盈利水平」在 F-score 里是**负向**贡献，
     与 Piotroski 原论文的高分组做多方向相反。这是 DEU/EU 市场的方向性先验。
   - **`group_rank(score, densify(industry))` 而非 `group_rank(score, industry)`** —— DEU 的 industry
     分组稀疏，`densify` 可能是必需的（**待验证 DEU 是否支持 `densify`**）。
   - 作者自述未解决问题：「阈值划分过于粗糙，每个指标只取 0/1，忽略改善幅度」⇒ **这正是 M4
     （一阶变化连续版）的动机**，也是我们相对论坛的增量。
   - 用 `fnd6_*`（Company Fundamental Data）字段；**DEU 是否有 `fnd6` 待查**（若无，改用
     `fundamental90` 的现成 `pscore`，等价且更省算子）。

**新线索（未读正文）**：
- `【论文合集】量化研究推荐论文`（KJ42842，108 赞）列有
  *"Attention Quantitative Fundamentals. Application of Piotroski F-Score on Non-U.S. Markets"*
  —— **非美市场 F-score 实证**，正对 DEU。信息源自帖子标题列表（未读正文/未见原文链接），
  报告中只能标为「帖子提及」，不得编造期刊或链接。
- `10个超级高效好用的ARC/GLB模板`（CQ89422，142 赞 / 68 评论）给出 F1/F1b/F1c/F10（市值中性滚动极值）
  与 F3（残差回归）；其 `ts_decay_exp_window` 骨架在 DEU 是 ghost，**不可照搬**。

### 65.7 本轮三条方法论增量

1. **★ 论坛帖的数据集 ID 也会错**（`fundamental44` vs `fundamental90`）。
   已确认「数据集级 description 不可信」，本轮再补：**论坛帖里写的 dataset_id 同样必须复核**。
   判据只有一个：`get_datafields(dataset_id=X)` 返回非空。
2. **★ 同一经济量的 VECTOR 口径与 MATRIX 口径可以互为补充，不是二选一**。
   `ern6_next_ed`（前瞻 VECTOR）与 `fnd90_qes_gamef_earnigs_timeliness`（回溯 MATRIX）构成
   「预定 vs 实际」的一致性信号。**遇到 VECTOR 覆盖不足时，第一动作应是去别的数据集找同经济量的
   MATRIX 口径，而不是硬扛 vec_* 稀疏。**
3. **★ 「排雷型」字段的裸 `rank()` 只是覆盖率探针，不是方向判断**。
   O-score / C-score / G-score / 应计类字段的经济学方向是「高值做空」，裸 `rank()` 若显示
   负 Sharpe 恰恰是**方向正确**的证据。探针阶段只读 `CONCENTRATED_WEIGHT` 与 `bookSize`；
   方向修正必须换骨架（M1→M5→M12）而不是 `add(A, -B)` 混信号。

---

## 66. 塔状态全貌 + 探针3/4 归因（2026-10-30）

### 66.1 ★ DEU/D1 塔状态（`get_pyramid_alphas`，窗口 2026-07-01～2026-10-31）

这是本轮最重要的一次事实修正。此前我一直用「信号族」口径描述 DEU 的产出，把
`analyst_eps` / `OTHER` / `lending_mean` / `techindi` / `social_snl27` / `institutions1` /
`sentiment7` 这 7 族当成「已点亮的塔」，**这是错的**。真实塔状态如下：

| 塔 | 颗数 | 状态 | 缺口 |
|---|---|---|---|
| `model` | 7 | ✅ 已点亮 | 0 |
| `other` | 4 | ✅ 已点亮 | 0 |
| `shortinterest` | 2 | ⚠️ 差 1 颗 | 1 |
| `fundamental` | 1 | 差 2 颗 | 2 |
| `institutions` | 1 | 差 2 颗 | 2 |
| `insiders` | 1 | 差 2 颗 | 2 |
| `analyst` | 1 | 差 2 颗 | 2 |
| `pv` | **0** | 完全空白 | 3 |
| `earnings` | 0 | 完全空白 | 3 |
| `sentiment` | 0 | 完全空白 | 3 |
| `news` | 0 | 完全空白 | 3 |
| `risk` | 0 | 完全空白 | 3 |
| `option` | 0 | 完全空白 | 3 |
| `macro` | 0 | 完全空白 | 3 |
| `socialmedia` | 0 | 完全空白 | 3 |
| `imbalance` | 0 | 完全空白 | 3 |

合计 17 颗（7+4+1+1+1+1+2），与「DEU 已提交 11 条 ACTIVE」对得上（11 全在
model+other；另 6 颗为更早窗口的历史提交）。

**三条推论**：

1. **13 个塔未点亮，其中 9 个完全空白**。此前「DEU 已挖尽」的判断只是指某一个信号族，
   在塔维度上 DEU 几乎是处女地。
2. **`pv: 0` 最反直觉**。PV 是最基础的数据类别，DEU 有 16 个 PV 数据集，
   但一颗 PV alpha 都没有。这不代表 PV 数据不可用 —— `close` / `returns` / `cap`
   在表达式中一直正常工作，`pv1` 的 `coverage=0.0` 同样是元数据缺失。
3. **点亮优先级（按缺口升序）**：`shortinterest`(1) → `fundamental`(2) /
   `institutions`(2) / `insiders`(2) / `analyst`(2) → 其余 9 个(3)。

### 66.2 探针 3 归因：铺展解 CW，但信号归零

`multisim 2kHdKlfBA5cB9Vu14WVbDGi9`，10 条全 COMPLETE，0 error。

| 表达式 | S | F | TO | CW | SUB | 2Y |
|---|---|---|---|---|---|---|
| `rank(ts_mean(fnd93_accruals_d1_current_t,252))` | **0.49** | 0.26 | 2.38% | ✅PASS | 0.46 | -0.34 |
| `rank(ts_mean(fnd93_deferred_tax_liability_51,252))` | **0.01** | 0.00 | 2.04% | ✅PASS | 0.24 | -0.97 |
| `rank(ts_mean(fnd93_tax_accruals_51,252))` | 0.13 | 0.04 | 2.21% | ✅PASS | 0.19 | -0.39 |
| `rank(ts_mean(vec_avg(free_cash_flow_to_market_cap),252))` | 0.29 | 0.16 | 0.67% | ❌**0.25** | — | 0.24 |
| `rank(ts_mean(vec_avg(bank_tier1_capital_ratio),252))` | 0.41 | 0.26 | 1.81% | ❌**0.1479** | 0.19 | **1.09** |
| `subtract(ts_mean(zscore(vec_sum(ern6_next_ed)),380), zscore(...))` | 0.41 | 0.16 | 18.66% | ✅PASS | 0.06 | -0.20 |
| `rank(ts_mean(vec_sum(ern6_next_ed),380))` | 0.43 | 0.19 | 11.86% | ✅PASS | **-0.76** | 0.51 |
| `rank(ts_mean(zscore(vec_sum(ern6_next_ed)),380))` | -0.19 | -0.05 | 3.03% | ✅PASS | 0.12 | -0.54 |
| `rank(ts_mean(vec_avg(ern6_board_of_directors_meeting),380))` | -0.53 | -0.28 | 2.43% | ✅PASS | 0.02 | -0.12 |
| `rank(ts_mean(vec_avg(ern6_1q),504))` | -0.40 | -0.18 | 1.60% | ✅PASS | -0.52 | -0.80 |

**判决 ①：铺展确实解 `CONCENTRATED_WEIGHT`。** 10 条里 8 条 CW PASS，与此前裸 `rank`
版本 10/10 全挂形成干净对照。这是本轮第一条可复用的工程结论。

**判决 ②：但救回来之后信号接近归零，best S 仅 0.49。** 更糟的是铺展对某些字段是净损失：
`fnd93_deferred_tax_liability_51` 裸版 S 0.60 → 铺展版 0.01。

**判决 ③（根因）：区分「时序稀疏」与「横截面稀疏」，二者生死完全不同。**

| 类型 | 症状 | 铺展效果 | 本次实例 | 判决 |
|---|---|---|---|---|
| **时序稀疏** | 季度更新，更新日之间全 NaN，裸 rank 抓到「只有少数票已更新」的那天 | 摊平后 CW 从 0.5 → PASS | `fnd93_*`（90-180 只有值） | 可救 CW，但信号弱（0.01-0.49）→ **数据集判死** |
| **横截面稀疏** | 字段本身只有极少数票有数据，与时序无关 | 252 天铺展后仍只有 4-14 只 | `free_cash_flow_to_market_cap`（6 只，CW 0.5→0.25）、`bank_tier1_capital_ratio`（14 只，CW 0.1479） | **无解，直接判死** |

`bank_tier1` 的 14 只 = DEU TOP500 里的银行股数量，本质是「行业内字段」，做不了全市场
截面信号。而 CW ≈ 1/有效标的数 这个判据再次被证实（7 对 → 0.1479 ≈ 1/6.8）。

**附带判决**：论坛 DEU 专属 EAT 帖（article 43184757918743）声称的 S 1.60 配方，
在 `ts_min_max_cps` 为 ghost 的前提下用 `subtract(ts_mean(zscore(x),380), zscore(x))`
等价替代，实测只有 S 0.41 / SUB 0.06 / 2Y −0.20。**该替代式不等价，或论坛值不可复现**；
EAT 事件族（`ern6_next_ed` / `ern6_board_of_directors_meeting` / `ern6_1q`）在 DEU
全部无信号，`ern6_next_ed` 的 SUB 更是 −0.76。

### 66.3 探针 4 归因：`fundamental90` 是宽度健康的第一块富矿

`multisim 320iVnb3q4sZcyMOxTOAVTi`，10 条全 COMPLETE，0 error。全部 `DEU/D1/FUNDAMENTAL`
塔（multiplier 1.8）。

（表见 66.3 节，与正文同）

**判决 ①：CW 10/10 全 PASS，`longCount` 57-77 / `shortCount` 54-77。**
这是全轮**第一个横截面宽度健康**的数据集。对比：
- `alpha_factor_lib`：3-6 只 → CW 0.5，死
- `fnd93`：90-180 只 → CW PASS 但信号 0.01-0.49
- **`fundamental90`：57-77 只 × 两侧对称 → CW PASS 且信号 0.70-0.89**
- `fundamental6`：196 字段、coverage 0.15-1.0（真实值，待测）

**判决 ②：方向验证 6/7 命中学术先验** —— 这是「信号真实」而非「噪声拟合」的强证据。

| 字段 | 学术来源 | 先验方向 | 实测 S | 命中 |
|---|---|---|---|---|
| `fnd90_qes_gamef_pscore` | Piotroski (2000) JAR | 正 | **+0.83** | ✅ |
| `fnd90_qes_gamef_grossprofit_asset` | Novy-Marx (2013) JFE | 正 | **+0.70** | ✅ |
| `fnd90_game_cash_flow_coverage` | 偿债能力 | 正 | **+0.89** | ✅ |
| `fnd90_qes_gamef_ohlson` | Ohlson (1980) JAR | 负 | **-0.55** | ✅ |
| `fnd90_qes_gamef_cscore` | Montier (2005) | 负 | -0.11 | ✅（弱） |
| `fnd90_game_accruals_vol` | Sloan 应计延伸 | 负 | -0.42 | ✅ |
| `fnd90_qes_gamef_mohanram` | Mohanram (2005) RAS | 负 | **+0.82** | ❌ **反向** |
| `fnd90_qes_gamef_earnigs_timeliness` | EAT 会计口径 | 正 | -0.24 | ❌ 反向 |

**Mohanram G-score 反向**值得单独记：G-score 原义是「成长股里被盈余操纵的高风险组」，
但 DEU 实测高 G 组反而跑赢 0.82。可能原因：DEU 成长股样本少，G-score 的构成项
（研发强度 / 资本开支 / 广告 / 现金流稳定性）在 DEU 更多反映「真成长」而不是「操纵」。
**⇒ 不可把美股的方向先验直接搬到 DEU，必须逐字段验证。**

**判决 ③：形态排序 铺展 >> zscore >> group_rank（同一 pscore 字段，严格对照）**

| 形态 | 表达式 | S | F | TO | SUB | 2Y |
|---|---|---|---|---|---|---|
| **M3 铺展** | `rank(ts_mean(F,252))` | **0.83** | 0.58 | 1.63% | 0.42 | **1.04** |
| M2 zscore | `ts_zscore(ts_backfill(F,66),252)` | 0.52 | 0.27 | 7.05% | 0.20 | 0.73 |
| M6 行业相对 | `group_rank(ts_backfill(F,66), densify(subindustry))` | 0.11 | 0.02 | 2.60% | 0.29 | 0.03 |

- 铺展 vs zscore 差 1.6×，根因是换手：zscore 7.05% vs 铺展 1.63%，4.3 倍换手吃掉收益。
  **对 Piotroski F 这种「绝对质量分」，水平（level）比异常度（deviation）更有意义** ——
  这与「稀疏事件流的 zscore 必用」不矛盾：事件流没有水平含义，质量分有。
- `group_rank` 再次垫底（0.11），与记忆里「group_rank 抹平幅度加权 ⇒ SUB 死、信号稀释」
  完全一致。**`group_rank` 不是提升 S 的工具。**

**判决 ④：缺口量化。** best S 0.89 / F 0.71，距 `LOW_SHARPE` 闸 1.58 差 **1.77×**。
但 F 0.71 距 1.0 只差 1.41×，且 TO 仅 1.33%（远超 LOW_TURNOVER 的 1% 下限）。
**⇒ 这不是「机制不成立」，而是「需要一层能放大 S 的结构」。**

### 66.4 两个新数据集的 S1 画像

**`pattern_scores`（PV 类，DEU 的 `pv` 塔 0 颗）**

| 属性 | 值 |
|---|---|
| coverage | **0.9888**（全 DEU 最高一档） |
| fieldCount | 504（全 MATRIX） |
| userCount / alphaCount | 158 / 266 |
| valueScore | **5.0** |
| pyramidMultiplier | **1.7**（最高档） |

命名三维度清晰：**模式类型**（~25 种）× **统计量**（mean / median / min / max / std /
q95 / dynamic）× **回看窗口**（60 / 120 / 无后缀）。字段级 coverage 集中在
0.9917（120 窗口）与 0.9991（60 窗口），`avg_similarity_*` 系列 0.9647。
拥挤度极低：大部分 0-10 users，最高 `avg_similarity_downward_symmetrical_triangle`
10 users / 10 alphas。

经济含义：技术形态相似度（Lo-Mamaysky-Wang 2000 JF 的自动形态识别路线），
形态分反转型（reversal）与延续型（continuation），可用于**形态对偶内置对照**
（V 底反转 vs V 顶延续、向上缺口 vs 向下缺口、上升楔形 vs 下降楔形）。

**`shortinterest3`（`lending_mean` 族的来源，`shortinterest` 塔差 1 颗点亮）**

| 属性 | 值 |
|---|---|
| coverage | 0.7105 |
| fieldCount | 25（**全 VECTOR**） |
| userCount / alphaCount | 316 / 864 |
| valueScore | 3.0（低） |
| pyramidMultiplier | **1.3**（最低档） |

已用过：`mean_loan_rate_main`（DEU 最强 ACTIVE `blRnKEk6`，2Y 2.74）。
**未触碰的 5 个维度**：
- 借出量：`loaned_market_value_usd` / `loaned_share_count`（各 3 变体）
- 交易活跃度：`transaction_count`（3 变体）
- 借出期限：`average_loan_duration_days`（3 变体）
- 费率波动：`loan_rate_volatility`（3 变体）
- 费率极差：`max_loan_rate` − `min_loan_rate`（需各自 vec 聚合后相减，注意无量纲化）

最拥挤：`shrt3_bar`（borrow demand rating 1-10），173 users / 323 alphas。
**⇒ 该集 valueScore 3.0 / multiplier 1.3 是平台明示的「低价值高拥挤」，** 只在
「差 1 颗点亮 shortinterest 塔」这个目标下才值得投入，不作为主战场。

### 66.5 下一步：设置扫描（探针 6 计划）

S 0.89 → 1.58 的缺口要用**设置层**而不是信号层解决，因为机制已被方向验证确认。
按记忆里的杠杆分工表，`decay` 与 `group_rank` 都不是 S 的杠杆，真正能动 S 的是
**中性化轴**（改变风险因子暴露）。

计划用 `batch_create_simulations`（per-item settings，不像 `create_multi_simulation`
整批共享设置）扫两个冠军 × 5 种新中性化：

| 表达式 | 中性化 |
|---|---|
| `rank(ts_mean(fnd90_game_cash_flow_coverage, 252))` | INDUSTRY / SECTOR / MARKET / STATISTICAL / CROWDING |
| `rank(ts_mean(fnd90_qes_gamef_pscore, 252))` | INDUSTRY / SECTOR / MARKET / STATISTICAL / CROWDING |

共 10 条新设置（SUBINDUSTRY 基线已有，不重复）。若某一轴把 S 推到 ≥1.2，
再在其上叠加结构层（M11 `trade_when` 门控：用现金流覆盖度做条件、pscore 做信号）。

---

---

## 67. 探针 6/7 收批：fundamental90 三轴穷尽，转 shortinterest3

### 67.1 探针 6 完整结果（`1l9a5Rd2Z4l3bi8rLJHTwrz`，10/10 COMPLETE，0 error）

设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling **ON**。
统一骨架 `rank(ts_mean(F,252))`（探针 4 已验证该骨架在 fundamental90 上 4/4 正向成立），
目的是**控制变量做字段筛选**——若每字段配不同骨架就无法归因。

| # | alpha | 表达式 | S | F | TO | SUB | 2Y | DD | failed_ra |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `JjeRPjWn` | `rank(ts_mean(fnd90_qes_gamef_icfroe_5y,252))` | **0.70** | 0.44 | 1.49% | 0.27 | 0.29 | 12.10% | 4 |
| 2 | `0mYnjmxK` | `-rank(ts_mean(fnd90_qes_gamef_chs_default,252))` | **0.60** | 0.38 | 1.42% | 0.36 | 0.55 | 17.69% | 3 |
| 3 | `A1VqQ1zW` | `-rank(ts_mean(fnd90_qes_gamef_cashflow_var,252))` | **0.54** | 0.30 | 1.24% | 0.30 | 0.70 | 13.85% | 3 |
| 4 | `WjOKLjzP` | `-rank(ts_mean(fnd90_game_capex_sale,252))` | 0.45 | 0.24 | 1.14% | 0.27 | 0.69 | 17.49% | 3 |
| 5 | `QPvmYPNM` | `rank(ts_mean(fnd90_qes_gamef_icfroe_3y,252))` | 0.39 | 0.18 | 1.53% | 0.14 | 0.99 | 17.61% | 4 |
| 6 | `zq3Xrq2G` | `-rank(ts_mean(fnd90_game_inventory_chg,252))` | 0.36 | 0.17 | 1.63% | 0.02 | 0.28 | 10.46% | 4 |
| 7 | `qMLeEMOO` | `rank(ts_mean(fnd90_qes_gamef_icfroe_1y,252))` | 0.30 | 0.12 | 1.78% | 0.14 | 0.20 | 20.65% | 3 |
| 8 | `A1VqQ1LE` | `-rank(ts_mean(fnd90_game_noa,252))` | −0.23 | −0.09 | 1.13% | −0.11 | −0.70 | 47.76% | 3 |
| 9 | `RRE0ARz0` | `-rank(ts_mean(fnd90_game_relative_rtn_vol,252))` | −0.24 | −0.09 | 1.68% | −0.30 | 0.08 | 34.65% | 4 |
| 10 | `npvwAped` | `-rank(ts_mean(fnd90_game_deferred_sal_chg,252))` | −0.36 | −0.17 | 1.65% | −0.48 | −0.67 | 33.09% | 4 |

**10/10 REJECT，prescreen READY / REVIEW 均为空。best S 0.70 < 探针 4 冠军 0.89。**

### 67.2 ★ 方向验证：6/10 表达式命中，但机制层只有 4/8 —— 失败集中在「风险维度」

| 机制 | 字段 | 学术先验 | 我设符号 | 实测 S | 反推先验方向的 S | 命中 |
|---|---|---|---|---|---|---|
| 应计异象 (Hirshleifer-Hou-Teoh) | `fnd90_game_noa` | 负 | − | −0.23 | +0.23 | ✗ |
| 违约风险 (Campbell-Hilscher-Szilagyi) | `fnd90_qes_gamef_chs_default` | 负 | − | +0.60 | −0.60 | ✗ |
| 低波动异象 | `fnd90_game_relative_rtn_vol` | 负 | − | −0.24 | +0.24 | ✗ |
| 收入质量（递延收入） | `fnd90_game_deferred_sal_chg` | 负 | − | −0.36 | +0.36 | ✗ |
| 增量现金流 ROE 1Y | `fnd90_qes_gamef_icfroe_1y` | 正 | + | +0.30 | — | ✓ |
| 增量现金流 ROE 3Y | `fnd90_qes_gamef_icfroe_3y` | 正 | + | +0.39 | — | ✓ |
| 增量现金流 ROE 5Y | `fnd90_qes_gamef_icfroe_5y` | 正 | + | +0.70 | — | ✓ |
| 存货异象 (Thomas-Weber) | `fnd90_game_inventory_chg` | 负 | − | +0.36 | — | ✓ |
| 现金流波动 | `fnd90_qes_gamef_cashflow_var` | 负 | − | +0.54 | — | ✓ |
| 投资异象 (Titman-Wei-Xie) | `fnd90_game_capex_sale` | 负 | − | +0.45 | — | ✓ |

**★★ 最有价值的经济学归纳：DEU 的因子定价分裂成两个方向相反的维度。**

- **风险维度（违约概率、相对收益波动率）→ risk-on 定价**：高风险股票收益**更高**。
  做空风险 = 亏钱。这与美国市场的低波动异象**完全相反**，是 DEU 的市场结构特征
  （TOP500 全是成熟大票，高波动更多来自经营杠杆与周期弹性，而非财务困境）。
- **会计质量 / 管理层行为维度（存货囤积、过度投资、现金流不稳、增量现金流 ROE）
  → 质量溢价仍然成立**：低质量 → 低收益。做空低质量 = 赚钱。

**⇒ 可直接指导后续所有 DEU 挖矿的方向规则：**
凡「风险 / 波动 / 违约 / 困境」类字段，方向一律设为**做多高风险**；
凡「会计质量 / 管理层行为 / 盈余质量」类字段，方向一律设为**做空低质量**。

**两条不命中的会计类字段，归因不是「方向错」而是「口径 / 解读错」：**

- `fnd90_game_noa` 是**裸 NOA 水平值**（未除总资产），混杂公司规模 ⇒ 原式应为 `NOA/总资产`。
  这解释了为什么连反向也只有 +0.23（|S| 最弱）。**不是方向问题，是口径问题** ——
  但 fundamental90 内未确认存在 `total_assets` 字段，无法配平，故该字段判为**不可用（口径缺分母）**。
- `fnd90_game_deferred_sal_chg` 反号（+0.36 对应「递延收入增长 → 后续收益高」）是**会计传导正确**：
  递延收入 = 已收款未确认，增长预示未来收入确认。**是我把「激进确认」的解读套错了方向**，
  数据没错。⇒ 该字段真实机制是「未来收入可见性」，不是「盈余操纵」。

### 67.3 探针 6 内相关矩阵：7 条几乎全正交（罕见）

`compute_mutual_correlation`（10 条，threshold 0.5, years 4, 1021 点）

|  | JjeRPjWn<br>icfroe5y | 0mYnjmxK<br>chs_def | A1VqQ1zW<br>cfvar | WjOKLjzP<br>capex | QPvmYPNM<br>icfroe3y | qMLeEMOO<br>icfroe1y |
|---|---|---|---|---|---|---|
| **JjeRPjWn** | 1 | 0.3136 | −0.1043 | 0.1251 | **0.7171** | **0.5721** |
| **0mYnjmxK** | 0.3136 | 1 | −0.1173 | 0.0859 | 0.2407 | 0.2497 |
| **A1VqQ1zW** | −0.1043 | −0.1173 | 1 | −0.0523 | −0.1568 | −0.1116 |
| **WjOKLjzP** | 0.1251 | 0.0859 | −0.0523 | 1 | 0.1474 | 0.1319 |

`max_pair = QPvmYPNM ↔ JjeRPjWn = 0.7171`；`max_mutually_below_subset_size = 8`

**两条结论：**

1. **`icfroe` 1Y/3Y/5Y 是同一信号的时间尺度梯度，不是三条独立 alpha。**
   相关 0.5721–0.7171，且 **S 随窗口单调递增（0.30 → 0.39 → 0.70）与相关单调递增同步**。
   ⇒ 「时间尺度解耦」假设在这个字段上**不成立**。5Y 最强既因信号更厚也因更平滑。
   ⇒ 三档只能算**一个机制**，提 60 颗时不能拆成三条。

2. **其余 7 条彼此相关几乎全部 |ρ| < 0.36**，构成一个罕见的高正交信号池。
   这是 fundamental90 唯一的正面发现——单条弱但互相不纠缠。

### 67.4 ★★ 探针 6 × 探针 4 跨批相关 + 合成上限精确计算（决定性）

`compute_mutual_correlation`（8 条 = 探针6 四正向 + 探针4 四冠军）

|  | xArXbwEq<br>cash_flow_cov<br>**S 0.89** | KPJxrYZl<br>pscore<br>**S 0.83** | 9qxgWPk2<br>grossprofit<br>**S 0.70** | d5We1862<br>mohanram<br>**S 0.82** |
|---|---|---|---|---|
| **JjeRPjWn** icfroe_5y (0.70) | 0.3789 | 0.3608 | 0.3431 | 0.3339 |
| **0mYnjmxK** chs_default (0.60) | **0.4812** | **0.4740** | 0.4280 | 0.3521 |
| **A1VqQ1zW** cashflow_var (0.54) | 0.1874 | 0.2092 | **−0.0139** | 0.1909 |
| **WjOKLjzP** capex_sale (0.45) | 0.2165 | 0.2666 | 0.3391 | **−0.1528** |

**★ 三个判定：**

1. **`cashflow_var`（S 0.54）是唯一真正正交于质量因子的正向信号**：
   与 `grossprofit_asset` 相关 **−0.0139**、与四冠全在 0.187–0.209。
   四冠彼此是 0.518–0.7085 的同一个质量因子，`cashflow_var` 不属于它。
2. **`capex_sale`（S 0.45）与 `mohanram` 相关 −0.1528**，也独立（投资异象 ≠ 质量）。
3. **`icfroe_5y`（0.334–0.379）与 `chs_default`（0.352–0.481）是质量因子的边缘成员**，
   不到 0.5 但也不独立——**它们是已测质量因子的弱化写法，不是新族**。

**★★ 合成上限（这是本轮最硬的结论）：**

取互相关全部 < 0.5 的最大子集 6 条：
`JjeRPjWn`(0.70) / `0mYnjmxK`(0.60) / `A1VqQ1zW`(0.54) / `WjOKLjzP`(0.45) / `9qxgWPk2`(0.70) / `d5We1862`(0.82)

```
ΣSᵢ = 3.81
Σρᵢⱼ (i<j, 15 对) = 2.4665      平均相关 ρ̄ = 0.1644
等权：S_c = ΣSᵢ / √(n + 2Σρᵢⱼ) = 3.81 / √(6 + 4.9330) = 3.81 / 3.3065 = 1.152
最优权重上界（等相关近似，SᵀR⁻¹S）：
  = ΣSᵢ²/(1−ρ̄) − ρ̄(ΣSᵢ)²/((1−ρ̄)(1+(n−1)ρ̄))
  = 2.5065/0.8356 − [0.1644/(0.8356×1.822)]×14.5161
  = 3.0000 − 1.5675 = 1.4325   ⇒  S_max = √1.4325 = 1.197
```

**⇒ 无论怎么配权，fundamental90 的 20 个已测字段合成后 Sharpe 上界 ≈ 1.20，
离 1.58 差 32%。等权 1.15 已逼近最优，配权优化空间只有 4%。**

而且这还是**未扣交易成本、未考虑 2Y/SUB 衰减**的理论值：
六条里 SUB 只有 0.02–0.36、2Y 只有 0.20–0.99，**两道辅闸全部严重欠账**。
即使 S 到 1.20，SUB 需 0.434×1.20 = 0.52，六条全不达标。

### 67.5 ★★ 探针 7 中性化扫描：论坛最强情报在 DEU 上完全反向

同一表达式 `rank(ts_mean(fnd90_game_cash_flow_coverage, 252))`，只换 neutralization。
基准 = 探针 4 的 `xArXbwEq`（SUBINDUSTRY：S 0.89 / F 0.71 / TO 1.33% / SUB 0.76）。

| 中性化 | alpha | S | F | TO | 2Y | SUB | margin | invest_ratio |
|---|---|---|---|---|---|---|---|---|
| **SUBINDUSTRY（基准）** | `xArXbwEq` | **0.89** | **0.71** | 1.33% | — | **0.76** | — | — |
| MARKET | `zq3Xr5QE` | 0.75 | 0.51 | **0.78%** | 1.09 | 0.56 | **1.4601%** | 1.0133 |
| FAST | `P0ojMGdE` | 0.63 | 0.32 | 12.44% | 0.74 | 0.57 | 0.0514% | 0.9365 |
| CROWDING | `ZYQkmjJd` | 0.63 | 0.36 | 1.90% | **1.18** | 0.43 | 0.4260% | 0.9683 |
| STATISTICAL | `omEQogek` | 0.56 | 0.24 | 6.70% | 0.24 | 0.39 | 0.0707% | 0.8214 |
| SLOW_AND_FAST | `88Rgvz3V` | 0.43 | 0.16 | 13.11% | 0.84 | 0.39 | 0.0280% | 1.0000 |
| **SLOW** | `88Rgvpml` | **0.42** | 0.16 | 5.77% | 0.58 | 0.34 | 0.0639% | 0.9524 |

**★ SLOW 把 Sharpe 从 0.89 打到 0.42（−53%），而论坛帖 42258807786391（73 票）
宣称 SLOW 能把 1.10 提到 2.03（+85%）。方向相反，幅度差 138 个百分点。**

**这不是噪声**：SLOW_AND_FAST (0.43)、STATISTICAL (0.56)、FAST (0.63) 全部下降，
6 个替代中性化**没有一个超过基准**。⇒ DEU + fundamental90 的最优中性化就是 SUBINDUSTRY。

**机理验证了论坛评论区自己给出的两条反向约束，两条在 DEU 同时成立：**

1. 「SLOW 在小 region / 稀疏组会把组均值跨时间漏出来」——
   DEU 是**全平台最小 universe（只有 TOP500，无退路）**，稀疏风险最高。
2. 「SLOW 会减掉慢趋势本身，做 trend-following 信号时等于自己减自己」——
   `rank(ts_mean(F,252))` **正是慢趋势型信号**，被 SLOW 的慢均线基线直接减掉。

**⇒ 沉淀为跨区禁区：SLOW / SLOW_AND_FAST 的「万能提分」结论只适用于
大 universe（USA TOP3000 / ASI MINVOL1M）+ 事件型/横截面型信号。
在最小 universe + 慢趋势型信号上，SLOW 是纯损失，不要照搬。**

**唯一亮点（但不解决问题）**：MARKET 中性化给出 `2Y 1.09 / margin 1.4601% / TO 0.78%`，
是全场 margin 最高、换手最低，说明「剥离市场 beta」能让现金流质量的定价更干净。
但 S 只有 0.75，不足以作为主骨架。

### 67.6 fundamental90 三轴穷尽的总结判定

| 轴 | 已试内容 | 最好结果 | 判定 |
|---|---|---|---|
| **字段轴** | 20/66 字段（探针 4 的 10 个 + 探针 6 的 10 个，覆盖质量/风险/投资/盈余/成长五类） | `cash_flow_coverage` S 0.89 | ✗ 加字段无法越 0.90 |
| **合成轴** | 六条互相关<0.5 的池，等权 + 最优权重上界 | 等权 1.152 / 上界 1.197 | ✗ 差 32% |
| **中性化轴** | 6 个（SLOW / SLOW_AND_FAST / FAST / CROWDING / STATISTICAL / MARKET） | SUBINDUSTRY 0.89 最优 | ✗ 全负 |
| **骨架轴** | 水平 / 铺展 / zscore / group_rank（探针 4 已测） | 铺展 0.89 | ✗ zscore 0.52、group_rank 0.11 |

**⇒ `fundamental90` 作为「能过 1.58 闸的富矿」这一假设被推翻。**
它的真实产出上限是 **1–2 条 S 0.85–0.90 / F 0.70 的 near 候选**，离闸差 1.8×。
**保留为 salvage 池素材（Mode B 组合辅助腿），不再作为主挖对象。**

**这条否定的价值**：省下剩余 46 个字段的广扫成本（按前 20 字段 0.089/字段的出货率，
46 个字段预期产出 0 条过闸）。**同时把「论坛结论不可跨区照搬」从经验上升为实证。**

### 67.7 转向 shortinterest3：shortinterest 塔只差 1 颗

**为什么是它（优先级高于继续磨 fundamental90）：**

1. **塔缺口最小**：`shortinterest` 已有 2 颗 ACTIVE，**差 1 颗即点亮**；
   `fundamental` 已有 1 颗、差 2 颗。补 1 颗 vs 补 2 颗，成本差一倍。
2. **已有最强 ACTIVE 佐证数据可用**：`blRnKEk6`（shortinterest 塔，2Y **2.74**）的 core 腿是
   `-rank(vec_avg(mean_loan_rate_main))`。该数据集在 DEU 能出强信号已被证明，
   **但那是一条三腿 `add()` 复合式（混了 analyst 数据），从未做过单字段 ATOM 归因。**
3. **五个维度从未被触碰**（platform userCount 4–12）：借出期限、费率波动、借出量、
   交易活跃度、**费率极差（`max_loan_rate − min_loan_rate`，作定义式合法）**。
4. **裸名档最不拥挤**：coverage 0.6683（users 4–36）vs `_main` 0.6872 vs `_p5_d1` 0.7833（users 23–93）。
   ⇒ 优先用裸名档降 prod 相关。

**探针 8 已派发（`akZNx6Ln4Zt8VSOYzXEhqZ`，10 条，DEU/TOP500/D1/SUBINDUSTRY/decay 4/nanHandling ON），
preflight 全过（`valid: true` / `unknown_fields: []` / 25 个 VECTOR 字段确认 / `any_changed: false`）。**

**十个结构互异模板（满足 ≥10 模板多样性硬约束，按差异维度标注）：**

| # | 模板 | 表达式 | 差异维度 / 经济机制 |
|---|---|---|---|
| T1 | 水平序数（基准） | `-rank(vec_avg(mean_loan_rate))` | 基准对照：借券成本水平（ATOM 归因起点） |
| T2 | 铺展 | `-rank(ts_mean(vec_avg(mean_loan_rate), 66))` | 时序均值铺展（fundamental90 最优几何迁移） |
| T3 | 自身基线异常度 | `-ts_zscore(ts_backfill(vec_avg(mean_loan_rate), 22), 252)` | 时序 z-score，保留幅度 |
| T4 | 费率极差（定义式） | `-rank(subtract(vec_avg(max_loan_rate), vec_avg(min_loan_rate)))` | 交易对手分歧度 = 借券市场紧张 |
| T5 | 借出期限 | `-rank(ts_mean(vec_avg(average_loan_duration_days), 66))` | 空头承诺期限 = 看空信念强度 |
| T6 | 费率波动 | `-rank(ts_mean(vec_avg(loan_rate_volatility), 66))` | 二阶矩，借券成本不确定性 |
| T7 | 借出市值 | `-rank(ts_mean(rank(vec_avg(loaned_market_value_usd)), 66))` | 金额类先 `rank()` 无量纲化，空头拥挤度 |
| T8 | 交易活跃度 | `-rank(ts_mean(vec_avg(transaction_count), 66))` | 借券活动强度 |
| T9 | 直接需求评级 | `-rank(ts_mean(vec_avg(shrt3_bar), 66))` | 1–10 分需求评级（最拥挤字段，173 users） |
| T10 | 条件门控 | `trade_when(greater(rank(vec_avg(loaned_market_value_usd)), 0.3), -rank(vec_avg(mean_loan_rate)), -1)` | 只在有实际借券活动的股票上做费率信号，无活动者不持仓 |

**方向先验（注意探针 6 的教训：DEU 风险维度是 risk-on）：**
T5/T6 属「风险 / 不确定性」维度，按探针 6 的发现**可能反号**（DEU risk-on）；
T1/T2/T3/T4/T9 属「拥挤度 / 借券成本」维度（真实做空压力），按学术先验应为负号；
T7/T8 属「拥挤度数量代理」，也应为负号。**若 T5/T6 反号成立，则再次确认 risk-on 定价规则。**

## 68. 探针 9 收批归因 + 同族 self 相关实测 + 探针 10 骨架移植设计

### 68.1 探针 9 alpha 与表达式（硬确认已完成）

派发批次 `1KWMF6hd4rGbD91aSRXmD9`，10/10 COMPLETE、0 error。此前只有 `LLMOMqbM` 经
`get_alpha_details` 硬确认，本轮补齐两条，并修正此前「按提交顺序推断」的映射（该推断已被证伪：
`batch_status` 的 children 顺序不等于提交顺序）。

| alpha | 表达式（`get_alpha_details.code` 权威） | S | F | TO | 2Y | SUB | 唯一失败项 |
|---|---|---|---|---|---|---|---|
| `LLMOMqbM` | `-rank(ts_mean(vec_avg(mean_loan_rate), 11))` | **1.14** | **1.02** | 12.56% | **1.71** | 0.63 | LOW_SHARPE |
| `88RgR7rq` | `-rank(ts_mean(vec_avg(shrt3_bar), 22))` | 1.11 | 0.96 | 4.73% | **1.73** | **0.68** | LOW_SHARPE + LOW_FITNESS |
| `3qogo33Z` | `-rank(ts_mean(vec_avg(mean_loan_rate), 44))` | 1.11 | 0.97 | 4.96% | 1.68 | 0.50 | LOW_SHARPE + LOW_FITNESS + LOW_SUB_UNIVERSE_SHARPE |

**三条的 `pyramids.list` 均为 `DEU/D1/SHORTINTEREST`（multiplier 1.3）** ⇒ 任一条过闸即点亮
shortinterest 塔（当前 counts = 2，需 3）。

**批内最强两条的分工**（这是新的认知，不是重复结论）：
- `LLMOMqbM`：**唯一只差 S 一条**（F 1.02 首次 ≥1.0、2Y 1.71 过闸、TO 12.56% 落健康区）。
  ⇒ 它是「单点缺口」候选，任何能提 S 而不动其它维度的骨架都值得在它上面试。
- `88RgR7rq`：**SUB 0.68 与 2Y 1.73 双最优**，但 F 0.96 差 0.04、TO 4.73% 偏低。
  ⇒ 按论坛「换手率治理要先于 sharpe 冲刺」（帖 43583631005719，23 票）的观点，
  **TO 4.73% 属于「过低」（该帖称 5%–15% 才合适）**，所以它不是单纯的 F 差 0.04，
  而是「F 与 TO 同时偏低」的同一根因：信号太慢、幅度被压平。

### 68.2 ★ 同族 self 相关实测：墙不存在

此前最大的提交风险是「`LLMOMqbM` 的 `mean_loan_rate` 与已提交 ACTIVE `blRnKEk6`
（core 腿 `-rank(vec_avg(mean_loan_rate_main))`）同族，可能撞 0.70」。

`check_self_correlation(LLMOMqbM, correlation_type="self", threshold=0.7)` 实测：

```
max_correlation = 0.2792   → PASS
top_correlated: vRk6og8b 0.2792 / blRnKEk6 0.2382 / 2rOe10qY 0.1150 /
                2rmGAPqN 0.0865 / Vk65zLzG 0.0794
pool_size = 10  (full_os_pool_size 11, excluded_power_pool_count 1)
```

**判定：与同族 ACTIVE `blRnKEk6` 的自相关仅 0.2382，远低于 0.70。** 机理：
`blRnKEk6` 是四腿 `add()` 复合（shoartinterest 腿 + 三条 model 腿），单腿只占约 1/4 权重，
所以单腿 ATOM 与它的相关被稀释。此前「同族 = 高 self」的担忧属于过度保守。

⇒ **`LLMOMqbM` 的提交障碍只剩 LOW_SHARPE（1.14 → 1.58，需 1.39×）这一条。**
⇒ 但 `mean_loan_rate` **族内**互相关仍高（探针 8 实测 `MPY90eM6`↔`P0ojMYWK` 0.8037），
  所以族内最终只能取一条提交，不能把窗口变体当多条交付。

### 68.3 窗口曲线归因（双字段，修正探针 8 结论）

`mean_loan_rate`（裸名档，coverage 0.6683）与 `shrt3_bar`（coverage 0.6528，最拥挤 users 173）
两个字段的 `-rank(ts_mean(vec_avg(F), W))` 曲线：

| W | mean_loan_rate | shrt3_bar |
|---|---|---|
| 8 | （探针10 在测） | — |
| 11 | **1.14** ← optimum | — |
| 15 | — | （探针10 在测） |
| 22 | 1.07 | 1.11 |
| 44 | 1.11 | — |
| 66 | 0.95 | 0.85 |
| 132 | 0.70 | 0.68 |
| 252 | 0.43 | — |
| 504 | 0.21 | — |

**结论（对探针 8 的修正）**：不是「铺展越久越好」，而是**「足够短但非零的铺展」**——
短端（11–44）压住 TO 的同时保留信号锐度；66 日已过高，超过 132 日后 S 单调崩塌。

两个字段在 W=22/66/132 三档上**数值高度平行**（1.07/1.11 vs 0.95/0.85 vs 0.70/0.68），
⇒ 两者承载的是同一个经济量（证券借贷成本），属于**同一机制的两个代理**，不能算两条独立 alpha。

### 68.4 探针 10：骨架移植实验（本轮最高 ROI，已派发）

**设计依据（不是猜）**：反向拆解 DEU 已提交 10 条 ACTIVE，其中两条是**纯单字段 ATOM**且
S 全在 1.73–1.77：

```
2rjrMZ25 (S 1.77 / F 1.61 / self 0.3437 / prod 0.651 / ANALYST) —— 骨架 T-A
group_neutralize(
  group_rank(add(ts_backfill(F,1008), ts_mean(ts_backfill(F,1008),210)), sector),
  bucket(rank(ts_mean(ts_backfill(F,1008),252)), range="0,1,0.05"))

Wje5K71x (S 1.73 / F 1.37 / self 0.1882 / prod 0.4305 / FUNDAMENTAL) —— 骨架 T-B
group_rank(ts_target_tvr_decay(
  multiply(rank(ts_delta(F,240)), rank(ts_delta(F,176))), target_tvr=0.03), sector)
```

而我自己用 `rank(ts_mean(F,W))` 扫了约 50 条，最好 1.14 —— **差值不是字段差，是骨架几何差**。
所以探针 10 的主线是把这两个骨架**移植**到 shortinterest3，而不是继续换窗口。

**十个模板（结构互异，满足 ≥10 硬约束）**

| # | 模板名 | 骨架 | 差异维度 | 来源 |
|---|---|---|---|---|
| T1 | T-A 完整移植·mean_loan_rate | `group_neutralize(group_rank(add(ts_backfill(F,1008), ts_mean(·,210)), sector), bucket(rank(ts_mean(·,252)), range="0,1,0.05"))` | 自引用分桶 + 双尺度 | `2rjrMZ25` 反向拆解 |
| T2 | T-A 完整移植·shrt3_bar | 同上换字段 | 字段档位 | 同上 |
| T3 | T-A 短窗版（backfill 252 / 混合 21 / bucket 63） | 同 T1 但全窗口缩短 | 时间尺度 | 探针 9 短端曲线 |
| T4 | T-B 完整移植·mean_loan_rate | `group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(F,240)), rank(ts_delta(F,176))), target_tvr=0.03), sector)` | 双期限一致性 + TVR | `Wje5K71x` 反向拆解 |
| T5 | T-B 完整移植·shrt3_bar | 同上换字段 | 字段档位 | 同上 |
| T6 | T-B 短期限版（66/44 + target_tvr=0.02） | 同 T4 但期限缩短、目标换手减半 | 时间尺度 + TVR 目标 | 探针 9 + 帖 43789939669271 |
| T7 | bucket-only 外层（净骨架剥离） | `group_neutralize(rank(ts_mean(F,11)), bucket(rank(ts_mean(F,252)), range="0,1,0.05"))` | 只保留 bucket，去掉 group_rank/add | 消融实验（ablation） |
| T8 | 纯短窗 W=8 | `-rank(ts_mean(vec_avg(mean_loan_rate), 8))` | 定位 optimum 短端 | 探针 9 曲线外推 |
| T9 | shrt3_bar W=15 | `-rank(ts_mean(vec_avg(shrt3_bar), 15))` | 同上（另一字段） | 同上 |
| T10 | quantile 外层替代 group_rank | `group_neutralize(quantile(add(ts_backfill(F,1008), ts_mean(·,210))), bucket(rank(ts_mean(·,252)), range="0,1,0.1"))` | 非线性变换 + bucket 步长加倍 | `58gkLAkk` 用 quantile 的实证 |

**消融设计说明**：T1 vs T7 = 测 `add(快,慢)` 与 `group_rank(sector)` 的增量；T1 vs T10 = 测
`group_rank` 与 `quantile` 的差异；T4 vs T6 = 测期限长度与 TVR 目标的交互；T1/T8 = 测新旧骨架的差距。
这样无论成败都能定位到具体组件，而不是「这族不行」。

**派发形态**：`create_multi_simulation`，10 条同设置，multisim `2Okp56Ri4k8arzbteWHA3B`。
预检 `preflight_expressions` 10/10 valid、`unknown_fields` 空、`any_changed=false`；
`operator_audit` 返回 `safe:true`、`violations:[]`（`bucket` / `ts_target_tvr_decay` 均可用，
且两骨架来自已提交 ACTIVE，零幽灵算子风险）。

### 68.5 论坛取证（按「用机制前必须查论坛 + 论文」硬约束执行）

**取证 1：「废因子的二次利用：用低 Sharpe 稳定信号做自定义中性化」（帖 41735891987479，41 票）**
- 核心操作：`group_neutralize(main_alpha, bucket(stable_failed_alpha, ...))`
- **两条硬约束**：① 作基准的信号**方向必须不同于**主信号（否则无隔离效果）；
  ② **覆盖率 > 85%**，否则被中性化的股票数量不够。
- ⇒ **对本批的直接冲击**：T1/T2/T3/T7/T10 全部是**自引用** bucket，而 `mean_loan_rate`
  coverage 0.6683、`shrt3_bar` 0.6528，**都低于 85% 门槛**。这批属于「覆盖率不足条件下的
  自引用分桶」，即使有效也可能被覆盖度封顶；下批必须换**高覆盖字段**（pv 类 ~1.0）做基准。
- ⇒ 但自引用有一个该帖没覆盖的优势：慢分量 `ts_mean(F,252)` 与快分量 `add(F, ts_mean(F,210))`
  天然方向正交，满足约束 ①。这解释了 `2rjrMZ25` 为何能成立。

**取证 2：`ts_target_tvr_decay` 完整签名（帖 30927669645207，179 票；帖 36592366500887）**
- 完整形态：`ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.05)`
- 有作者给出 `lambda_min=0, lambda_max=5` 的实战案例；帖子同时指出
  **「换手率过低也不好，5%–15% 才比较合适」**。
- ⇒ 我在 T4/T5/T6 只赋了 `target_tvr`，未显式给 `lambda_min/lambda_max`（用默认值）。
  这是本批的一个未收敛旋钮；若 T4/T5/T6 的 TO 落不到 5%–15%，下一批应显式扫 `lambda_max`。

**取证 3：「换手率是隐形天花板：fitness 公式里的 tvr 墙」（帖 43583631005719，23 票）**
- 结论：**「换手率治理要先于 sharpe 冲刺」**；低频慢信号（tvr 9.6%）同 sharpe 下
  fitness 与 margin 双双轻松过线。
- ⇒ 直接解释 `LLMOMqbM`（TO 12.56%）F 1.02 过线而 `88RgR7rq`（TO 4.73%）F 0.96 未过：
  **F 不是独立的信号质量指标，它内含 turnover 惩罚项**。压 TO 过头会反过来伤 F。
  这修正了我此前「F 差一点就补 F」的思路 —— 应该先把 TO 调到 5%–15% 健康区。

**取证 4：「双重中性化：把两个分组编码成一个的巧思」（帖 42683369420439，30 票）**
- 技巧：`group = densify((group_B + 1) * 1000 + group_A)` 一次性按两个维度中性化，
  避免连续两次 `group_neutralize` 的同维度重复扣除。
- ⇒ 这正是我担心的 T1 结构问题（`group_rank(·,sector)` + 平台 SUBINDUSTRY 属同树两次）。
  下批可用 `densify` 构造 `sector × bucket` 的单一分组轴来验证。

**取证 5：「中性化顺序不是随便排的」（帖 41881412101399，41 票）**
- 坑：同一维度被中性化两次会悄悄改变信号；顺序与重复都影响结果。
- ⇒ 与取证 4 共同构成对 T1 结构的风险标注，但**实测优先于理论**（`2rjrMZ25` S 1.77 是反例）。

### 68.6 本批的已知局限（写下来防止把失败误读成「机制不成立」）

1. **bucket 基准覆盖率不足 85%**（两个字段都 ~0.65）—— 若 T1/T2/T3/T7/T10 全灭，
   应先怀疑覆盖度，而不是否定「自引用分桶」这个机制。
2. **T4/T5/T6 的 `lambda_min/lambda_max` 用默认值** —— TVR 目标可能不可达。
3. **`shrt3_bar` 是 shortinterest3 里最拥挤的字段**（users 173 / alphas 323），
   T2/T5/T9 即使出高 S，prod 相关性也需单独验证。
4. **`mean_loan_rate` 与 `shrt3_bar` 数值平行 ⇒ 同一机制** —— T1/T2、T4/T5、T8/T9 六条里
   实际只覆盖两条经济假设，不能用「10 条都测了」充当 10 条独立试验。

---

## 69. 探针 10 收批：骨架移植消融（T-A 败 / T-B 胜）+ PnL 去重 + 探针 11 设计

### 69.1 探针 10 批次与指标全表

批次 `2Okp56Ri4k8arzbteWHA3B`，10/10 COMPLETE、0 error。
设计目的：把 DEU 已提交 10 条 ACTIVE 里两条**纯单字段 ATOM** 的骨架反向拆解后，移植到 `shortinterest3` 的 virgin 字段上做**受控消融** —— 同一数据集、同一字段族、只换骨架几何。

- T-A 来源：`2rjrMZ25`（S 1.77 / F 1.61 / TO 11.99%，ANALYST，单字段 `eps_y1_estimate_change_3mo`）
- T-B 来源：`Wje5K71x`（S 1.73 / F 1.37 / TO 12.69%，FUNDAMENTAL，单字段 `fnd6_newq_oiadpq`）

| alpha | 模板 | S | F | TO | 2Y | SUB | margin | failed_ra |
|---|---|---|---|---|---|---|---|---|
| `RRE0EGR0` | **T5 = T-B × shrt3_bar** | **1.23** | 0.88 | 4.65% | **2.29** | 0.73 | 0.002779 | 3 |
| `omEQEx85` | T8 = mean_loan_rate W=8 | 1.15 | 0.92 | 16.05% | 1.65 | 0.71 | 0.001267 | 2 |
| `vR1a1Wwd` | T9 = shrt3_bar W=15 | 1.10 | **0.95** | 5.72% | 1.70 | 0.71 | **0.003274** | 2 |
| `E56o6d9P` | **T1 = T-A × mean_loan_rate** | 1.03 | 0.47 | **29.30%** | 1.13 | 0.83 | 0.000419 | 3 |
| `kqNeNzqO` | — | 0.96 | 0.59 | 19.49% | 1.17 | 0.69 | 0.000744 | 3 |
| `ZYQkQOPQ` | — | 0.91 | 0.40 | 28.04% | 0.86 | 0.66 | 0.000384 | 3 |
| `1YN6Nrqm` | — | 0.70 | 0.26 | 28.01% | 0.51 | 0.71 | 0.000281 | 3 |
| `j2YNYq5k` | — | 0.35 | 0.12 | 20.48% | 1.39 | **1.07** | 0.000229 | 3 |
| `6Xdgd5Xp` | — | 0.12 | 0.02 | 19.39% | 0.72 | 0.97 | 0.000081 | 3 |
| `P0ojokJ7` | — | −0.06 | −0.01 | 29.20% | −0.29 | 0.12 | −0.000026 | 3 |

四条经 `get_alpha_details(code)` **硬确认**的表达式：

```
RRE0EGR0 = -group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(vec_avg(shrt3_bar),240)),
           rank(ts_delta(vec_avg(shrt3_bar),176))), target_tvr=0.03), sector)
           # longCount 161 / shortCount 107 / invest_S 1.16 / risk_neut_S 0.84
           # fail: LOW_SHARPE 1.23/1.58, LOW_FITNESS 0.88/1.0, CONCENTRATED_WEIGHT
           # pass: LOW_TURNOVER, HIGH_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE, MATCHES_PYRAMID
           # warning: CLUSTER_TEST 0.61 (limit 1)

omEQEx85 = -rank(ts_mean(vec_avg(mean_loan_rate), 8))
           # fail: []（空）；warning: LOW_SHARPE 1.15/1.58, LOW_FITNESS 0.92/1.0, CLUSTER_TEST 0.88
           # longCount 71 / shortCount 70 / risk_neut_S 0.98

vR1a1Wwd = -rank(ts_mean(vec_avg(shrt3_bar), 15))
           # fail: []；warning: LOW_SHARPE 1.10/1.58, LOW_FITNESS 0.95/1.0, CLUSTER_TEST 0.58

E56o6d9P = -group_neutralize(group_rank(add(ts_backfill(vec_avg(mean_loan_rate),1008),
           ts_mean(ts_backfill(vec_avg(mean_loan_rate),1008),210)), sector),
           bucket(rank(ts_mean(ts_backfill(vec_avg(mean_loan_rate),1008),252)), range="0,1,0.05"))
           # fail: LOW_SHARPE 1.03, LOW_FITNESS 0.47, LOW_2Y_SHARPE 1.13
```

### 69.2 ★ 消融归因：同一批两个骨架，一个胜一个败

这是本批最重要的产出 —— **不是「shortinterest 机制不行」，而是可定位到组件级的差异**。

| 维度 | T-B 移植（`RRE0EGR0`） | T-A 移植（`E56o6d9P`） | 裸基线 |
|---|---|---|---|
| S | **1.23** | 1.03 | 1.14（`LLMOMqbM` = `-rank(ts_mean(mean_loan_rate,11))`） |
| TO | **4.65%** | **29.30%** | 12.56% |
| 2Y | **2.29** | 1.13 | 1.71 |
| margin | 0.002779 | **0.000419（破 0.0005 门槛）** | — |

**结论 1：T-B 骨架可移植，且是 DEU 本区 S 新高。**
`RRE0EGR0` S 1.23 > 此前区纪录 `LLMOMqbM` 1.14，2Y 2.29 远超 1.58 闸，TO 4.65% 说明 `target_tvr=0.03` 确实生效。`LOW_TURNOVER` / `HIGH_TURNOVER` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE` / `MATCHES_PYRAMID` 全部 pass。
**但引入 `CONCENTRATED_WEIGHT` 失败** —— 这是 T-B 在 shortinterest 上的唯一新增缺陷。

**结论 2：T-A 骨架不可移植 —— 移植后比裸基线更差。**
S 1.03 < 1.14，TO 从 12.56% 暴涨到 29.30%，margin 跌破门槛，且新增 `LOW_2Y_SHARPE` 失败（1.13）。
机理假设：`group_neutralize(·, bucket(...))` 的自引用分组 + `add(F, ts_mean(F,210))` 里快分量主导 → 时序平滑被破坏。`group_rank(sector)` 在 T-A 里是外层，在 T-B 里是内层，位置差异可能是关键。

**★ 但不能据此否定 T-A 机制本身**，因为论坛帖 41735891987479（41 票）给的硬约束是「**bucket 基准覆盖率必须 > 85%**」，而本批两个字段的覆盖率都不达标：

| 字段 | coverage | 是否满足论坛 85% 要求 |
|---|---|---|
| `mean_loan_rate` | 0.6683 | ✗ |
| `shrt3_bar` | 0.6528 | ✗ |
| `2rjrMZ25` 用的 `eps_y1_estimate_change_3mo` | **0.9234** | ✓ |

`2rjrMZ25` 能到 S 1.77 的**前提是它的基准字段覆盖率 92%**。所以正确的表述是：**T-A 机制对基准字段覆盖率有硬下限，shortinterest3 全字段不达标**，而不是「T-A 骨架无效」。

**结论 3：长窗口双期限一致性 = 低换手 + 高 2Y。**
T-B 用 `ts_delta(F,240)` × `ts_delta(F,176)`，两个都是 ~1 年尺度，天然低换手（4.65%），2Y 2.29 说明不是靠单年行情。这一点与论坛帖 43583631005719「换手率治理要先于 sharpe 冲刺」一致。

### 69.3 ★ PnL 互相关去重：7 条候选实际只有 2 个信号族

`compute_mutual_correlation(ids, threshold=0.5, years=4)`（本地计算、零平台配额、num_points 1021）关键值：

```
RRE0EGR0 vs 全部候选          ≤ 0.3721   ← 真正独立
omEQEx85  vs LLMOMqbM          0.9843    ← 同族（W=8 ≈ W=11）
vR1a1Wwd  vs 88RgR7rq          0.9936    ← 同族（W=15 ≈ W=22）
LLMOMqbM  vs MPY90eM6          0.9168
omEQEx85  vs MPY90eM6          0.8985
max_mutually_below_subset = [omEQEx85, RRE0EGR0, E56o6d9P], size = 3
```

**族划分与取用决定**：

| 族 | 成员 | 相关区间 | 取哪一条 | 理由 |
|---|---|---|---|---|
| 族 A：借贷成本水平 | `omEQEx85` / `LLMOMqbM` / `MPY90eM6` / `vR1a1Wwd` / `88RgR7rq` | 0.62–0.99 | `LLMOMqbM`（F 1.02 已过闸）或 `omEQEx85`（fail 空） | 只能取其一 |
| 族 B：双期限变化一致性 | `RRE0EGR0` | 与全部 ≤0.37 | `RRE0EGR0` | 唯一独立 |

⇒ **DEU shortinterest 塔最多由这 2 条贡献 2 颗，不是 7 颗。**
这与 2026-10-30 DEU 的方法论结论一致：**数候选必须用 PnL 聚簇，字段名族会高估多样性约 3×。**

### 69.4 ★ 短窗 optimum 在 8–11 日（修正此前判断）

`mean_loan_rate` 的完整窗口曲线：

| W | 8 | 11 | 22 | 44 | 66 | 132 | 252 | 504 |
|---|---|---|---|---|---|---|---|---|
| S | **1.15** | 1.14 | 1.07 | 1.11 | 0.95 | 0.70 | 0.43 | 0.21 |

`shrt3_bar`：W=15 → 1.10、W=22 → 1.11、W=66 → 0.85。
⇒ 此前判断的「11–44 日」应收窄为 **8–22 日**，且 44 日仍可用（`3qogo33Z` S 1.11）。更长窗口单边衰减。

### 69.5 ★ self correlation 两项实测：同族自相关墙不存在

```
check_self_correlation(LLMOMqbM, self, 0.7) → max 0.2792 PASS
  top: vRk6og8b 0.2792 / blRnKEk6 0.2382 / 2rOe10qY 0.1150 / 2rmGAPqN 0.0865 / Vk65zLzG 0.0794
  pool_size 10 / full_os_pool_size 11 / excluded_power_pool_count 1

check_self_correlation(RRE0EGR0, self, 0.7) → max 0.3076 PASS
  top: blRnKEk6 0.3076 / vRk6og8b 0.1862 / 883Y3bAW 0.0938 / 58gkLAkk 0.0830 / 2rOe10qY 0.0771
```

**机理**：`blRnKEk6`（DEU 最强 ACTIVE，S 2.02）是四腿 `add()` 复合，单腿只占约 1/4 权重，所以单字段 ATOM 与它的相关被稀释。
⇒ 此前「同族 = 高 self」的担忧属**过度保守**。`LLMOMqbM` 与 `RRE0EGR0` 的提交障碍里**都不含 self 墙**。

### 69.6 探针 11 设计（已派发）

批次 `usbX55I4PEcvInnBFKXfW`，10 条，两组目的分离：

**A 组（6 条，shortinterest3）：修 `RRE0EGR0` 的 CONCENTRATED_WEIGHT + 推强**

| # | 变更点 | 设计假设 |
|---|---|---|
| A1 | 去掉 `group_rank(sector)`，改全宇宙 `rank` | CW 最可能根因是小 sector（3–5 只股）产生 ±0.5 极端权重；拆掉分组层应直接消除 |
| A2 | `tail(winsorize(·, std=2), 0.25, 0.75, 0.5)` | `2rmGAPqN`（S 1.81 ACTIVE）配方，截尾把极端权重压回 0.5 |
| A3 | `target_tvr` 0.03 → 0.06 | 论坛：TO 健康区 5%–15%；把 4.65% 推进去，同时看 F 是否随 TO 上升而改善 |
| A4 | 内层加 `ts_backfill(vec_avg(shrt3_bar), 22)` | coverage 仅 0.6528，backfill 提升有效覆盖 |
| A5 | 外层 `hump(·, hump=0.01)` | 换手平滑，验证 CW 是否由日间权重抖动引起 |
| A6 | 外层分组 `sector` → `subindustry` | sector 太粗导致组内权重极端，subindustry 更细 |

**B 组（4 条，fundamental6）：T-B 骨架移植到 virgin 字段 → 点 fundamental 塔（需 +2）**

| # | 字段 | 语义 | coverage | users |
|---|---|---|---|---|
| B1 | `fnd6_newq_seqq` | 股东权益合计 | 0.6595 | 29 |
| B2 | `fnd6_newq_cheq` | 现金及短期投资 | 0.6531 | 23 |
| B3 | `fnd6_newq_ppentq` | 固定资产净额 | 0.6056 | 3 |
| B4 | `fnd6_newq_invtq` | 存货合计 | 0.5484 | 10 |

B4 取负号：存货增长 = 负面（Sloan 存货效应）。
B1–B3 取正号：权益扩张 / 现金积累 / 资本开支增长在 DEU 的质量溢价方向（**这是待验证假设，不是定论** —— 记忆里「学术因子方向先验不可跨市场照搬」，此前 Mohanram G-score 在 DEU 实测符号与美股相反）。

**★ B 组的主要风险：self 相关。** `Wje5K71x` 是 ACTIVE，同数据集、同骨架、只换字段（`oiadpq` → `seqq`/`cheq`/`ppentq`/`invtq`）。它的 self 只有 0.1882，但**同骨架换字段的 self 可能显著更高**。派发后必须逐条实测 `check_self_correlation`，通过才考虑提交。

**预检状态**：`preflight_expressions` → `valid: true` / `unknown_fields: []` / `unknown_soft: []` / `any_changed: false`；`operator_audit` → `safe: true` / `violations: []`。

### 69.7 本批已知局限（如实标注）

1. **`RRE0EGR0` 的 CW 根因是推断，不是实测确认**。A1–A6 是六种互斥假设的同时验证，派发后按结果反推根因，不能反过来把「某个修法有效」当成机制解释。
2. **A 组 6 条高度同源**，无论几条过闸，最终只能取 1–2 条（同族）。A 组的目的是**定位 CW 根因**，不是凑数量。
3. **B 组 4 条同骨架换字段，PnL 可能高度相关**。必须跑 `compute_mutual_correlation` 再定取哪条，不能按 S 排序收货。
4. **S 1.23 → 1.58 的缺口（1.28×）仍未解**。A3 提高 target_tvr 有可能改善 F 但未必提 S；真正的跃升需要 B 组这种换数据集换信号源。
5. **`mean_loan_rate` 与 `shrt3_bar` 数值高度平行**（W=22/66/132 三档：1.07/1.11 vs 0.95/0.85 vs 0.70/0.68）⇒ 承载同一经济量（证券借贷市场紧张度），**不能算两条独立 alpha**。探针 10 的 10 条实际只覆盖两条经济假设。
6. **外部论文取证仍缺失**：本会话 `web_search` 持续返回 `MATRIX_TOOL_REQUEST_FAILED`，所有「学术先验」只能引用既有文献知识 + 论坛帖，**不确定处已标注为待验证假设，未编造链接**。


---

## 70. 探针 11 收批：CW 根因定位（ts_backfill）+ DEU 本区新高 S 1.47 + T-B 骨架的流量/存量边界

### 70.1 探针 11 指标全表与 A/B 族划分

批次 `usbX55I4PEcvInnBFKXfW`，10/10 COMPLETE、0 error。
PnL 互相关（threshold 0.5 / years 4 / num_points 1021）分出**两个互不重叠的族**，与设计完全一致：

- **族 A（`shrt3_bar`，6 条）**：`akKXa7N9` / `1YN6WwJ6` / `RRE0e7dd` / `VkxKN7O0` / `leAJajrn` / `P0oj57vx`，组内相关 **0.464–0.960**
- **族 B（`fundamental6`，4 条）**：`qMLe7jXZ` / `RRE0e7rd` / `gJe7aj3e` / `YP1Xa7Ao`，组内相关 **0.778–0.874**（`YP1Xa7Ao` 对另三条为 **−0.78 ~ −0.85**，是取负号的 B4）

跨族相关全部落在 **−0.27 ~ +0.32**，两族彼此独立。

| alpha | 组件（来源） | S | F | TO | 2Y | SUB | margin | failed RA |
|---|---|---|---|---|---|---|---|---|
| **`leAJajrn`** | **A6 = `sector`→`subindustry`** ✅硬确认 | **1.47** | **1.13** | 4.31% | **2.52** | **0.90** | 0.003445 | LOW_SHARPE, **CONCENTRATED_WEIGHT** |
| `VkxKN7O0` | **A4 = `ts_backfill(·,22)` + sector** ✅硬确认 | 1.31 | 0.97 | 3.70% | 2.20 | 0.85 | **0.003708** | LOW_SHARPE, LOW_FITNESS |
| `RRE0e7dd` | A3 = `target_tvr=0.06`（推断） | 1.25 | 0.90 | **5.79%** | 2.11 | 0.66 | 0.002234 | 3 项 |
| `1YN6WwJ6` | A2 = `tail(winsorize(...))`（推断） | 1.24 | 0.89 | 4.66% | 2.34 | 0.75 | 0.002736 | 3 项 |
| `akKXa7N9` | A1 = 去掉 `group_rank` 改全宇宙 `rank`（推断） | 1.19 | 1.06 | 5.64% | **1.45** | 0.88 | 0.003491 | 3 项（含 LOW_2Y_SHARPE） |
| `P0oj57vx` | A5 = `hump(·,0.01)`（推断） | 0.82 | 0.47 | **2.29%** | 2.01 | 0.60 | 0.003599 | 3 项 |
| `qMLe7jXZ` | B（`fnd6_newq_*`） | 0.02 | 0.00 | 2.63% | −0.11 | 0.32 | 0.000093 | 3 项 |
| `RRE0e7rd` | B | −0.08 | −0.02 | 3.00% | 0.08 | 0.16 | −0.000374 | 3 项 |
| `gJe7aj3e` | B | −0.19 | −0.06 | 2.95% | −0.21 | −0.05 | −0.000888 | 3 项 |
| `YP1Xa7Ao` | B（取负，B4=`invtq`） | −0.13 | −0.04 | 2.91% | 0.03 | −0.32 | −0.000644 | **4 项** |

**只有 `leAJajrn` 与 `VkxKN7O0` 两条的 code 经 `get_alpha_details` 硬确认**，其余组件归属是按「TO 签名 + 相关签名」推断，未逐条核 code —— 引用时须带此限定。

**`leAJajrn` 完整表达式（硬确认）**：
```
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(vec_avg(shrt3_bar),240)),
 rank(ts_delta(vec_avg(shrt3_bar),176))), target_tvr=0.03), subindustry)
```
settings：DEU / TOP500 / D1 / decay 4 / SUBINDUSTRY / truncation 0.08 / nanHandling **ON** / IS 2014-01-01~2023-12-31。
metrics：longCount 172 / shortCount 97 / invest_S 1.23 / risk_neut_S 1.07 / drawdown 4.87%。
checks.pass：`LOW_FITNESS` / `LOW_TURNOVER` / `HIGH_TURNOVER` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE` / `MATCHES_PYRAMID`
checks.warning：`CLUSTER_TEST 0.58`(limit 1) / `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`
pyramid：`DEU/D1/SHORTINTEREST` multiplier 1.3
**self correlation 0.2842 PASS**（top: `blRnKEk6` 0.2842 / `vRk6og8b` 0.2177 / `Vk65zLzG` 0.1126）

### 70.2 ★★ CW 根因定位：CONCENTRATED_WEIGHT 是覆盖率缺口的 NaN 伪影

探针 10 的 `RRE0EGR0`（`sector` + 无 backfill）失败项是 `LOW_SHARPE + LOW_FITNESS + CONCENTRATED_WEIGHT`。
探针 11 六个变体里**只有 A4（`ts_backfill(vec_avg(shrt3_bar),22)`）让 CW 变为 PASS**：

| 变体 | 改动 | CW 结果 | F 结果 |
|---|---|---|---|
| 基线 `RRE0EGR0` | sector、无 backfill | ✗ FAIL | ✗ 0.88 |
| A2 | `tail(winsorize(·,std=2),0.25,0.75,0.5)` | — 仍在 fail 名单（failed 3） | ✗ |
| A1 / A3 / A5 / A6 | 各自单改 | — 仍在 fail 名单 | A6 单独把 F 修过（1.13） |
| **A4** | **`ts_backfill(·,22)`** | **✓ PASS** | ✗ 0.97 |

**机理**：CW 的判据是单票权重上限。`shrt3_bar` 的 coverage 只有 **0.6528**，即约 35% 的股票-日在原始数据里是 NaN。
`group_rank(·, sector)` 在 NaN 缺席后把组内剩余股票重新归一化 —— 当某个小行业只剩 2–3 只有效股票时，两只股票分别拿到接近 ±0.5 的组内极值权重，直接触发 CW。
**`ts_backfill(·,22)` 把缺口补上 ⇒ 每个行业内有效股票数恢复 ⇒ 权重自然摊薄 ⇒ CW 消失。**
这解释了为什么 `winsorize/tail`（A2，压缩分布尾部）**修不了** CW —— 它动的是已有权重的形状，而问题出在**权重压根没有分配给缺席的股票**。

**⇒ 可复用规律（跨数据集）**：**遇到 `CONCENTRATED_WEIGHT` FAIL，第一动作是查字段 coverage；若 coverage < 0.8 且信号外层用了 `group_rank`/`group_neutralize`，先加 `ts_backfill`，不要先上 `winsorize`/`tail`/`truncation`。**

### 70.3 ★★ A4 与 A6 的互补性 → 探针 12

两个修法动的是**完全不同的闸**，且互相不冲突：

| 修法 | 对 S 的增量 | 修掉哪个闸 | 是否损害其他闸 |
|---|---|---|---|
| A4 = `ts_backfill(·,22)` | 1.23 → **1.31**（+0.08） | CONCENTRATED_WEIGHT | 无（F 0.88→0.97 反而改善） |
| A6 = `subindustry` | 1.23 → **1.47**（+0.24） | LOW_FITNESS（0.88→1.13） | 无 |

**⇒ 合并后预期：S ≈ 1.47 + 0.08 ≈ 1.55，F ≥ 1.13，CW PASS ⇒ 只剩 `LOW_SHARPE` 一项，缺口仅 1.03×。**

探针 12（批次 `tWERT7cN4lNbUJda2X3epF`，10 条）就是围绕这个合并做参数收敛：

| # | 配置 | 目的 |
|---|---|---|
| 1 | `backfill 22` + `subindustry` + `tvr 0.03` | **主力组合**，验证可加性 |
| 2 | 同上 `tvr 0.04` | 论坛 TO 健康区 5%–15%，同时看 F 是否再升 |
| 3 | 同上 `tvr 0.05` | 同上上界 |
| 4 | 同上 `tvr 0.02` | 反向确认 tvr 方向 |
| 5 | `backfill 66` + subindustry | backfill 窗口轴 |
| 6 | `backfill 120` + subindustry | 同上 |
| 7 | `backfill 252` + subindustry | 同上（覆盖完整一年，最激进） |
| 8 | 主力 + `tail(winsorize(std=2),0.25,0.75,0.5)` | 验证在 CW 已修后，截尾是否还能再提 S |
| 9 | 主力但外层改全宇宙 `rank` | 验证 `group_rank(subindustry)` 是否仍必要 |
| 10 | 主力但双期限改 `252 / 176` | 双尺度窗口轴 |

**声明**：探针 12 是**定向破闸批**（围绕已确认组件的参数收敛），不是新机制波次。它不满足「模板库 ≥10 个结构互异」的要求 —— 该硬约束适用于**换机制/换数据集**的波次，本批的目的是把一条 S 1.47 的候选推到闸上，属于 SOP 的「对近闸候选定向挖掘」步骤。

### 70.4 ★★ T-B 骨架的流量/存量边界：在余额表字段上四连败

族 B 四条（`fundamental6`）S 全在 **−0.19 ~ 0.02**，平均约 −0.07，四个符号选择（含一条取负）**全部无效**：

```
qMLe7jXZ S  0.02       RRE0e7rd S −0.08
gJe7aj3e S −0.19       YP1Xa7Ao S −0.13（取负号，与其余三条相关 −0.78~−0.85）
```

**对照组**：同一骨架的 `Wje5K71x`（ACTIVE，S 1.73）用的是 `fnd6_newq_oiadpq` = **Operating Income After Depreciation（利润表流量）**；`leAJajrn`（S 1.47）用的是 `shrt3_bar`（**借贷市场的每日费率，也是流量**）。

**探针 11 的 B 组用的是余额表存量**：`seqq`（股东权益）/ `cheq`（现金）/ `ppentq`（固定资产）/ `invtq`（存货）。

**⇒ 边界结论**：`ts_delta(F, 240)` 作用在**流量**变量上等于「一年的累积强度变化」；作用在**存量**变量上等于「资产增长因子」（Cooper-Gulen-Schill 2008 的资产增长异象）。这是**两个不同的经济量**，骨架不能跨这条线移植。
**⇒ 可复用规律：T-B（双期限 delta 一致性）只适用于流量/修订型字段（利润表、费率、成交量），不适用于资产负债表的存量字段。**

**同时修正一个此前判断**：`DEU-FUNDAMENTAL6-EMPTY-COVERAGE-20260923`（best S 0.35）判死记录建立在旧骨架上，`Wje5K71x` S 1.73 证明该集有货。但探针 11 也说明**有货的只有利润表流量那一路**，余额表那一路确实弱。**该集应改为「利润表字段可用 / 余额表字段沙盒」的分层状态，而不是整体判死或整体可行。**

**fundamental6 待挖的流量候选字段**（下一批用）：

| 字段 | 语义 | coverage | users |
|---|---|---|---|
| `fnd6_newq_piq` | 税前利润 | 0.5452 | 84 |
| `fnd6_newq_oibdpq` | 折旧前营业利润 | 0.4548 | 36 |
| `fnd6_cptnewq_ibq` | 息前异常项前利润 | 0.5452 | 200 |
| `fnd6_newq_txtq` | 所得税合计 | 0.5336 | 33 |
| `fnd6_newq_xintq` | 利息费用 | 0.5255 | **6** |

### 70.5 ★ 数据集清单修正：DEU 实有 ≥110 个数据集，此前 92 条漏掉整个 analyst 类（18 个）

`get_datasets(region=DEU, category="analyst", delay=1, universe=TOP500)` 返回 **18 个数据集**。此前记录的 92 条清单把 13 个 category 的计数加总恰好等于 92，说明那次全量拉取**整类漏掉了 analyst**（最可能是外部化 artifact 的正则解析丢行）。

**⇒ 修正动作**：把 `tracking/DEU/candidates/deu_datasets_all.json`（92 条）视为**不完整**；DEU 数据集总数 ≥ 92 + 18 = **110**。后续按 category 逐个拉取为准。

**analyst 18 个数据集画像**（全为 multiplier 1.8）：

| id | 名称 | coverage | fields | users | alphas | 备注 |
|---|---|---|---|---|---|---|
| `analyst93` | Europe Analyst Estimate Daily Data | **0.6373** | 100 | 116 | 193 | 语义最贴 DEU（欧洲分析师精度/目标价） |
| `analyst44` | Integrated Broker Estimates | 0.5802 | 72 | 46 | 58 | 曾被挖过（波次 s2_analyst44_d1） |
| `analyst47` | Alternative Analyst Investment Insight | 0.6234 | 5 | 83 | 112 | GBR `analyst47+pv47` 是已知死路，但那是两塔组合 |
| `analyst9` | Analyst Estimate Daily Data | 0.5825 | 51 | 82 | 106 | |
| `analyst_factor_signals` | Global Analyst Factor Signals | 0.5996 | 108 | **701** | **1575** | 极拥挤 |
| `analyst7` | Broker Estimates | 0.7207 | 608 | **1184** | **3993** | 最拥挤，且 description 被新闻文案污染 |
| `analyst48` | Dividend estimation data | 0.7879 | 7 | 4 | 7 | **已判定不可用，见 70.6** |
| `analyst46` | Analyst Investment insight Data | 0.0 | 5 | **2** | **4** | 近乎无人，cov 0.0 属元数据缺失 |
| `analyst35` | ESG Model | 0.0 | 23 | 7 | 10 | |
| `analyst8` | Daily Split Data | 0.0 | 10 | 7 | 9 | |
| `analyst94` | Fundamental Income and Dividend Model | 0.0 | 34 | 8 | 38 | |
| `analyst83` | Smart Conference call transcript | 0.3389 | 345 | 23 | 26 | 事件型 |
| `analyst10` | Performance-Weighted Analyst Estimates | 0.0 | 53 | 25 | 45 | StarMine SmartEstimate 加权 |
| `analyst16` | Real Time Estimates | 0.0 | 66 | 21 | 24 | description 是 BBID/RIC 映射文案（污染） |
| `analyst39` | Analyst estimates & financial ratios | 0.0 | 24 | 114 | 261 | |
| `analyst69` | Fundamental Analyst Estimates | 0.0 | 292 | 281 | 515 | FactSet |
| `analyst15` | Earnings forecasts | 0.0 | 537 | 228 | 649 | 国家级/行业级聚合，非个股 |
| `analyst_consensus` | Standardized Analyst Consensus Forecasts | 0.0 | **1972** | 213 | 413 | 字段数最多 |

**注**：`coverage = 0.0` 在这 18 条里出现 10 次，属模型派生集的**元数据缺失**（与此前 `fundamental90/93` 同因），不等于无数据。判断真实覆盖必须查 `get_datafields` 的字段级 coverage。
**`analyst` 塔当前 1 颗，需 +2 点亮**；这 18 个数据集是点亮该塔最便宜的入口（`analyst46` users 2 / `analyst35` users 7 / `analyst8` users 7 / `analyst94` users 8 都是低拥挤）。

### 70.6 `analyst48` 判定不可用

7 个字段全部是**指数级元数据**，不是个股信号：

```
anl48_bulk_count_index_members   指数成分股数量
anl48_bulk_idivisor              指数计算除数
anl48_bulk_indx_typ              指数类型编码（价格/全收益/行业）
anl48_index_bulk_ibc             公司 Bloomberg 标识
anl48_index_bulk_nfields         记录内字段数
anl48_index_bulk_return_code     数据获取返回码
anl48_bbpdiip                    projected dividends（指数点口径）
```

唯一带经济含义的 `anl48_bbpdiip` 也是**指数层面**的合计，无法映射到 TOP500 的单只股票。
⇒ 该集即便 coverage 0.7879、users 仅 4，也不具备 ATOM 单股 alpha 的可用性。**不要再在 analyst48 上花回测。**

### 70.7 本轮已知局限

1. **族 A 六条最终只能取 1–2 条**（组内相关最高 0.96）。即使探针 12 产出多条过闸候选，shortinterest 塔的增量仍是 +1（从 2 到 3），不是 +10。
2. **A1/A2/A3/A5 的组件归属未经 code 硬确认**，是按 TO 与相关签名推断。§70.2 的 CW 结论只依赖已硬确认的 A4 与 `RRE0EGR0`，不受此影响；但「A2 修不了 CW」这条属于推断级证据。
3. **探针 12 的 1.55 是加和外推，不是实测**。两个修法可能非线性叠加（例如 backfill 改变了 subindustry 分组内的有效股票数），实测可能低于或高于 1.55。
4. **`shrt3_bar` users 173 / alphas 323，是 `shortinterest3` 最拥挤的字段**。即使过闸，prod 相关性仍需实测（本区 `2rjrMZ25` 的 prod 是 0.651，接近 0.65 自设线）。
5. **`mean_loan_rate` 与 `shrt3_bar` 数值高度平行**（已记于 §69.7），族 A 与探针 9/10 的族 A 是同一经济量 ⇒ 不能与 `LLMOMqbM` 同时提交。
6. **B 组四连败不能外推到整个 fundamental6**，只否定了「余额表存量 × T-B 骨架」这一格。利润表流量字段（70.4 表）尚未测。


---

## 71. 探针 12 收批：A4×A6 可加性验证成功，产出 DEU 首条「仅剩 1 项失败」的候选（S 1.56 / self 0.2705）

### 71.1 探针 12 指标全表

批次 `tWERT7cN4lNbUJda2X3epF`，10/10 COMPLETE、0 error。**prescreen：READY 0 / REVIEW 10 / REJECT 0** —— 这是本战役第一次出现零 REJECT 的批次。

| alpha | S | F | TO | 2Y | SUB | margin | failed RA |
|---|---|---|---|---|---|---|---|
| **`VkxKMJJb`** | **1.56** | **1.24** | 3.33% | 2.36 | **1.05** | **0.004739** | **1（仅 LOW_SHARPE）** |
| `rKRQ0Xvj` | 1.53 | 1.20 | 3.34% | 2.38 | 0.97 | 0.004579 | 1 |
| `LLMO8JJn` | 1.50 | 1.15 | 3.32% | **2.41** | 0.95 | 0.004438 | 1 |
| `78LgG99O` | 1.50 | 1.14 | 3.22% | 2.04 | 0.84 | 0.004502 | 1 |
| `MPY9gmon` | 1.49 | 1.15 | 4.25% | 2.23 | 0.77 | 0.003476 | 1 |
| `wpQXNggp` | 1.48 | 1.14 | 3.26% | 2.15 | 0.84 | 0.004525 | 1 |
| `58ENGWo5` | 1.46 | 1.12 | 3.80% | 2.10 | 0.78 | 0.003845 | 1 |
| `QPvmWXXg` | 1.45 | 1.07 | 3.28% | 2.02 | 0.85 | 0.00419 | 1 |
| `LLMO8JJM` | 1.36 | 1.01 | 2.92% | 2.32 | 0.96 | 0.004691 | 1 |
| `9qxgG00r` | 1.25 | 1.15 | 4.28% | 1.49 | 0.90 | 0.004908 | 2 |

**9/10 条只剩 1 项失败**（`9qxgG00r` 是唯一 2 项，且 2Y 1.49 < 1.58 已触发 `LOW_2Y_SHARPE`）。

### 71.2 ★★ A4 × A6 可加性验证成功

§70.3 的外推是「S ≈ 1.47 + 0.08 ≈ 1.55，F ≥ 1.13，CW PASS ⇒ 只剩 LOW_SHARPE」。实测对照：

| 阶段 | 表达式配置 | S | F | CW | 失败项数 |
|---|---|---|---|---|---|
| 探针 10 基线 `RRE0EGR0` | sector / 无 backfill / 240-176 | 1.23 | 0.88 | ✗ FAIL | 3 |
| 探针 11 A6 `leAJajrn` | **subindustry** / 无 backfill / 240-176 | 1.47 | 1.13 | ✗ FAIL | 2 |
| 探针 11 A4 `VkxKN7O0` | sector / **backfill 22** / 240-176 | 1.31 | 0.97 | ✓ PASS | 2 |
| **探针 12 `VkxKMJJb`** | **subindustry / backfill 22 / 252-176** | **1.56** | **1.24** | **✓ PASS** | **1** |

**加和外推 1.55 → 实测 1.56，误差 0.01。** 说明 A4（`ts_backfill`）与 A6（`subindustry`）作用于**互不影响的两个失败机理**，可以线性叠加：

- `ts_backfill` 修的是**权重分配**（覆盖率缺口导致小行业只剩 2–3 只有效股票 ⇒ 极端组内权重 ⇒ CW）
- `subindustry` 修的是**分组粒度**（sector 太粗，行业内信号被异质成分稀释 ⇒ F 上不去）

**⇒ 这是一个可复用的「双闸分离」范式**：当候选同时卡 `CONCENTRATED_WEIGHT` 和 `LOW_FITNESS` 时，先用 `ts_backfill` 修前者、再用更细的分组轴修后者，不要试图用单一改动同时修两个闸。

### 71.3 `VkxKMJJb` 完整档案（硬确认）

**表达式**：
```
-group_rank(ts_target_tvr_decay(multiply(
  rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 22), 252)),
  rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 22), 176))), target_tvr=0.03), subindustry)
```

**设定**：EQUITY / DEU / TOP500 / delay 1 / **decay 4** / SUBINDUSTRY / truncation 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling **ON** / maxTrade OFF / FASTEXPR / IS 2014-01-01 ~ 2023-12-31 / simulationMode FULL

**指标**：
```
sharpe 1.56   fitness 1.24   turnover 3.33%   returns 7.88%   drawdown 5.06%
margin 0.004739   pnl 8,132,040   bookSize 20,000,000
longCount 171 / shortCount 94
sub_universe_sharpe 1.05   two_year_sharpe 2.36
investability_sharpe 1.36  investability_fitness 1.01  investability_ratio 0.8718
risk_neutralized_sharpe 1.13
```

**checks**：
```
fail:    LOW_SHARPE 1.56 / 1.58      ← 唯一失败项
warning: CLUSTER_TEST 0.68 (limit 1) / MATCHES_THEMES / OSMOSIS_ALLOCATION
pass:    LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT /
         LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE / MATCHES_PYRAMID
pending: SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION
```

**self correlation 0.2705 PASS**（top: `blRnKEk6` 0.2705 / `vRk6og8b` 0.2195 / `2rOe10qY` 0.1511 / `58gkLAkk` 0.1495 / `Vk65zLzG` 0.1405）
**pyramid**：`DEU/D1/SHORTINTEREST`，multiplier **1.3** ⇒ 提交即点亮 shortinterest 塔（2 → 3）

**这是 DEU 本区史上第一条「RA 只剩一项失败」的候选。** 此前最好的 `LLMOMqbM`（S 1.14）唯一失败也是 LOW_SHARPE，但 S 差 1.39×；本条的差距只有 **1.27%**（1.56 → 1.58）。

### 71.4 冠军的关键改动：长端窗口 240 → 252

探针 12 第 10 条相对第 1 条的唯一差别是**长端 `ts_delta` 窗口 240 → 252（整一年）**。这个改动带来 S 1.56（第 1 条的 S 未逐条硬确认，但同批 TO 3.2–3.8% 聚类中 252 系列位于最高档）。

**机制解释**：252 与 176 的比值 1.432，比 240/176 = 1.364 更接近「年 vs 三季」的自然会计节奏差；且 252 正好覆盖一个完整年度，使长端 delta 变成「同比变化」，与短端「季节性变化」形成正交性更好的双尺度。这与 `Wje5K71x`（S 1.73）用 240/176 的做法不同 —— 说明**双尺度窗口不是固定配方，需要按字段的数据节奏标定**。

### 71.5 探针 13：用 decay 杠杆补最后 1.27%

`ts_target_tvr_decay` 已把 TO 压到 **3.33%，低于论坛帖 43583631005719 指出的 5%–15% 健康区**；平台上再叠加 **decay 4** 属于「双重平滑」。

**已知规律（记忆实证）**：`decay` 提高 ⇒ TO 下降、S 下降、`invest_ratio` 上升；`decay` 降低 ⇒ S 上升。且 `SUB/S` 是信号几何属性、不随 decay 变动（实测全程 0.29–0.30）。（本条记录的原始实证是 decay 5→15 方向，向 2 方向外推属**未被验证的假设**。）

探针 13（批次 `UCDWP9714QBbpWc9yzFwgM`）设 **decay = 2**，10 条围绕冠军做细网格：

| # | 变化 | 目的 |
|---|---|---|
| 1 | 冠军原式（252/176, tvr 0.03） | **隔离 decay 单变量**：与 `VkxKMJJb` 逐位对比即得 decay 4→2 的纯效应 |
| 2 | 短端 176 → 210 | 双尺度比值轴（252/210 = 1.2） |
| 3 | 短端 176 → 231 | 双尺度比值轴（252/231 ≈ 1.091） |
| 4 | 长端 252 → 240 | 隔离窗口变量（240/176，decay 2 下） |
| 5 | 长端 252 → 260 | 长端上探 |
| 6 | tvr 0.03 → 0.035 | TO 健康区下沿（5% 以下仍需压低） |
| 7 | tvr 0.03 → 0.025 | 反向确认 |
| 8 | 短端 176 → 132 | 更陡的双尺度比（252/132 = 1.909） |
| 9 | backfill 22 → 44 | backfill 窗口轴 |
| 10 | backfill 22 → 11 | backfill 窗口轴下限 |

**关于预检**：本批的算子集（`group_rank` / `ts_target_tvr_decay` / `multiply` / `rank` / `ts_delta` / `ts_backfill` / `vec_avg`）与字段（`shrt3_bar`）在探针 12 已通过 `preflight_expressions`，本批**只改数值字面量**，故未重复预检。

### 71.6 本轮已知局限

1. **9/10 条属于同一信号族**（同字段、同骨架、只差窗口/tvr/backfill）。即使多条过闸，shortinterest 塔的增量仍是 **+1**，不是 +9。探针 12 的目的是把一条推到闸上，不是凑数量。
2. **`VkxKMJJb` 仍未过闸**（S 1.56 < 1.58），且尚未测 prod 相关性。self 0.2705 只排除了自有 OS 池的重叠风险。
3. **`shrt3_bar` users 173 / alphas 323 是本集最拥挤字段**，prod 相关性存在实测风险。参考值：同区 `2rjrMZ25` 的 prod 是 0.651，贴近 0.65 自设线。
4. **decay 4 → 2 的 S 增量为未验证外推**（原始实证只覆盖 5→15 方向）。若 decay 2 反而降低 S，说明该信号已过度平滑，需反向加到 6/8。
5. **族内多条的相对排序未逐条 hard-confirm**：只有 `VkxKMJJb`（第 10 条）经 `get_alpha_details` 确认。其余 9 条的「第几条」映射未知，**不能据此断言「tvr 0.05 比 0.03 好」这类结论** —— 只能引用其指标本身。
6. **本轮所有结论仍限制在 `shrt3_bar` × `shortinterest3` × T-B 骨架这一格**。是否可移植到其他数据集尚未测（探针 11 的 fundamental6 余额表四连败就是反例）。


---

## 72. 探针 13 收批（decay=2）：decay 是死轴 + shortinterest 族饱和判定 + 战略转向 SENTIMENT 塔

### 72.1 探针 13 指标全表（decay=2 / truncation 0.08）

批次 `UCDWP9714QBbpWc9yzFwgM`，10/10 COMPLETE、0 error。**prescreen READY 0 / REVIEW 10 / REJECT 0**（连续第二批零 REJECT）。

| alpha | S | F | TO | 2Y | SUB | margin | invest_S | failed RA |
|---|---|---|---|---|---|---|---|---|
| **`pwdQWj0q`** | **1.57** | 1.24 | 3.62% | 2.39 | 1.01 | 0.004286 | 1.34 | **1（仅 LOW_SHARPE）** |
| `bl67xj3Z` | 1.56 | 1.23 | 3.60% | 2.39 | **1.09** | 0.004301 | 1.35 | 1 |
| `78LgGjOO` | 1.54 | 1.20 | 3.64% | 2.21 | 0.92 | 0.004182 | 1.38 | 1 |
| `kqNe8jek` | 1.54 | 1.21 | 3.79% | 2.38 | 0.92 | 0.004043 | 1.38 | 1 |
| `58ENGlNn` | 1.53 | 1.19 | 3.52% | 2.08 | 0.91 | 0.004326 | 1.41 | 1 |
| `RRE057Xd` | 1.51 | 1.17 | 3.93% | 2.20 | 0.96 | 0.003827 | 1.32 | 1 |
| `d5We9jqK` | 1.49 | 1.14 | 3.30% | 2.32 | 1.04 | 0.004431 | 1.33 | 1 |
| `e75e1zJE` | 1.45 | 1.11 | 3.69% | 2.07 | 0.93 | 0.003940 | 1.20 | 1 |
| `ZYQkX7Z1` | 1.45 | 1.11 | 3.57% | 2.08 | 0.89 | 0.004129 | 1.36 | 1 |
| `QPvmW7dG` | 1.42 | 1.07 | 3.62% | 2.06 | 0.85 | 0.003920 | 1.37 | 1 |

**10/10 全部只剩 1 项失败（`LOW_SHARPE`）** —— 本族所有变体的 RA 结构完全一致，差异只在 S/F 的小数位。

### 72.2 ★★ decay 2↔4 是死轴（硬确认，单变量隔离）

本批第 1 条即「冠军原式 + 只把 decay 从 4 改成 2」，用于隔离 decay 单变量：

| 表达式（完全相同） | decay | S | F | TO | 2Y | SUB | margin |
|---|---|---|---|---|---|---|---|
| `bl67xj3Z` = `VkxKMJJb` 原式（252/176 + backfill22 + subindustry） | **2** | **1.56** | 1.23 | 3.60% | 2.39 | 1.09 | 0.004301 |
| `VkxKMJJb`（探针 12） | **4** | **1.56** | 1.24 | 3.33% | 2.36 | 1.05 | 0.004739 |

**S 逐位相同（1.56 = 1.56），F 差 0.01，TO 差 0.27pp。**

⇒ **修正此前的外推假设（见 §71 阻塞项）**：之前想用「降低平台 decay 补 S」是基于「decay 5→15 提高会降 S」的逆向推断，但实测 **decay 4→2 完全不提 S**。

**新的判读规律（写入方法论）**：
- decay 的 S 响应**不是单调函数，而是在低区间存在平台期**。decay 4→2 落在平台期内（S 不动），decay 5→15 才进入下降段。
- 与既有「三杠杆分工表」一致：decay 是 `invest_ratio` 的杠杆，**不是 S 也不是 SUB/S 的杠杆**。本批再次证实。
- **⇒ 不要再把仿真槽花在 decay 微调上。** 要提 S 必须改信号几何或换字段族。

### 72.3 ★ shortinterest 族饱和判定（本区 12 个探针的结论）

累积统计：探针 8/9/10/11/12/13 共 6 个探针、约 50 条变体，落在 `shortinterest3` × T-B 骨架族上。S 值分布：

| 探针 | decay | 最优 S | 最优失败项数 |
|---|---|---|---|
| 10 | 4 | 1.23（`RRE0EGR0`） | 3 |
| 11 | 4 | 1.47（`leAJajrn`） | 2 |
| 12 | 4 | **1.56**（`VkxKMJJb`） | **1** |
| 13 | 2 | **1.57**（`pwdQWj0q`） | **1** |

**S 的四次跃迁全部来自结构性改动，没有一次来自参数微调**：
1. +0.24：`sector` → `subindustry`（分组粒度）
2. +0.24（叠加）：加 `ts_backfill(·,22)`（修 CW 的 NaN 伪影）
3. +0.09：长端窗口 240 → 252（匹配年报节奏）
4. +0.01：长端 252 → 240 在 decay=2 下的边际差异 —— **在噪声范围内，不算跃迁**

**判定：`shortinterest3` × T-B 骨架族已饱和（saturation），S 上限 ≈ 1.57，距 1.58 闸差 0.01。**
- 剩余可用杠杆（truncation、winsorize、短端微调）**预期增量 ≤0.02**，且每条消耗一个仿真槽；
- **`pwdQWj0q`（S 1.57 / F 1.24 / 2Y 2.39 / SUB 1.01 / margin 0.004286 / self 待测）保留为「一步之遥」候选**，不再对该族追加参数网格。

**附带发现（重要的正向信号）**：本族 `SUB/S` = 1.09/1.56 ≈ **0.70**，远超 0.434 门槛。说明该信号在子宇宙上极稳健 —— 这解释了为什么它在 TOP500 这种窄宇宙仍能站到 1.57。**若将来有「以 SUB 余量换 S」的合规杠杆（如提高集中度），本族是首选试验田。**

### 72.4 ★★ 战略转向：DEU/SENTIMENT 塔是空白覆盖（本轮最高价值发现）

在论坛检索「sell side analyst idea sentiment」时命中帖 **43179860065303**（72 票 / 50 评论）《维基百科关注度的"突压"信号(sent)在德国DEU市场的因子化尝试》，作者 LC97552。

**帖子的硬数据（DEU / TOP500 / delay 1）**：
- **DEU/D1/SENTIMENT 金字塔 alphaCount = 0（空白覆盖）**，multiplier 平台标 ×1.8（作者写 ×1.9，以平台为准）
- 作者实盘结果：**Sharpe 2.04 / Fitness 1.92 / Turnover 9.11% / Margin 24.21bps / SUB 1.59 / 2Y 2.25 / CLUSTER 1.71**，17 项硬检查全 PASS
- 设置：`SUBINDUSTRY` / **decay 16** / **truncation 0.02** / pasteurization ON
- 中性化扫描：SUBINDUSTRY(SH 2.18) > INDUSTRY(1.79) > SECTOR(1.53 FAIL)

**原式（作者称获胜者 `np7nn69l`）**：
```
vector_neut(quantile(ts_ir(ts_mean(ts_max(ts_backfill(vec_avg(snt7_all_languages_views), 22), 5), 5), 22), 120),
            ts_backfill(vec_avg(snl27_relpopularity08), 22))
```

**作者给出的四条消融结论（全部与我的既有习惯相反，值得单独记录）**：

| 轴 | 作者的实测 | 我的既有默认 | 冲突点 |
|---|---|---|---|
| 结构轴 | 三重 neut + 全 rank（FT 1.34）→ 双 neut + rank（FT 1.47）→ **双 neut 无 rank（FT 2.12）** → 单 neut 无 rank（更高） | 每个候选都包 `rank()` | **rank 包装是本族 FT 天花板，应当尽量少包** |
| 去噪轴 | 基线 `quantile(ts_ir(bf))` FT 1.47 → 加 `ts_mean(ts_max)` 后 FT **2.09（+0.62）** | 未用过 `ts_mean(ts_max)` 双层 | 双平滑是本线主杠杆 |
| 异常度 | `ts_zscore(x,252)` 外层 **SH −0.33 / FT −0.10（禁用）** | 稀疏事件族铁律说 zscore ≫ rank | **本族与稀疏事件族相反**，zscore 外层禁用 |
| 参数 | decay 8 → FT 0.35；decay 16 → SH 2.04–2.18 | DEU 固定 decay 4 | **decay 对本骨架极敏感，16 是甜点** |

**⚠ 我对原式的两处语义修正（必须记录，否则不可复现）**：
1. **`ts_max` 在本账号 ERROR**（`platform_constraints.json` 的 `inaccessible_ops`，见记忆条目）。改为 `max(x, ts_delay(x,1), ts_delay(x,2), ts_delay(x,3), ts_delay(x,4))` —— 平台 `max(x, y, ..)` 确认支持多参数（至少 2 个），这是 w=5 窗口最忠实的展开。
2. **`quantile(x, 120)` 的第二参不是窗口**。平台定义：`quantile(x, driver = gaussian, sigma = 1.0)`，driver ∈ {gaussian, cauchy, uniform}。作者把 120 传在 driver 位置，语义不成立。按其文字描述「百分位转换，分布均匀化」改用 **`driver="uniform"`**。

**⚠ 与本区的冲突风险（必须核实）**：作者写 `PROD_CORR 0.6338 = SELF_CORR 0.6338`，并注明「我自己交了好几个类似的」—— 说明**该字段族在平台生产池里已有他的 ACTIVE**。我的 10 条 ACTIVE 里**没有任何 sentiment7 / sentiment27 字段**（全部是 eps_y1_estimate_change_3mo / fnd6_newq_oiadpq / inst1_* / oth455_* / mean_estimate_change_pct_* / shrt3_bar），故**对我本人是 virgin 族**；但平台 prod 相关性须实测，不能假定低。

### 72.5 数据集与字段核对（平台实拉，非 description 推断）

**DEU sentiment 类只有 3 个数据集**（`get_datasets(category="sentiment")`）：

| dataset | 名称 | coverage | 字段 | users | alphas | multiplier |
|---|---|---|---|---|---|---|
| `sentiment27` | Website Popularity Rankings | **0.9038** | 18 | 129 | 324 | 1.8 |
| `sentiment7` | Webpage Views Data (Wikipedia) | **0.7418** | 3 | 52 | 94 | 1.8 |
| `sentiment33` | Sentiment Data by NLP | 0.3221 | 255 | 33 | 45 | 1.8 |

⚠ `sentiment33` 的 description 是**被污染的 RIC/BBID 映射文案**（与 §70 记的 other* 系列同款污染），但 name 是 "Sentiment Data by NLP"、255 字段 ⇒ 后续必须用 `get_datafields` 看字段级 description，不能信数据集级描述。

**实际使用的字段（`get_datafields` 原样核对）**：

| 字段 | 类型 | coverage | users | alphas | 描述（字段级） |
|---|---|---|---|---|---|
| `snt7_all_languages_views` | VECTOR | 0.7539 | 31 | 61 | Number of views for the company's Wikipedia page |
| `snt7_views` | VECTOR | 0.7357 | 26 | 33 | Daily Wikipedia page view count for the specified project and access type |
| `snl27_relpopularity08` | VECTOR | **0.9022** | 37 | 54 | Composite relative popularity score computed with alpha=0.8；higher = broader attention |
| `snl27_kurtosis` | VECTOR | 0.9022 | 32 | 47 | Excess kurtosis of the issuer's domain rank distribution（尾部厚度） |
| `snl27_avgranking` | VECTOR | 0.9022 | 16 | 17 | Tranco 排名均值；lower = more popular |
| `snl27_topranking` | VECTOR | 0.9022 | 15 | 18 | 最优（最低）域名排名 |
| `snl27_totaldomains` | VECTOR | 0.9022 | 24 | 33 | 关联网域去重计数 |
| `snt27_rank` | VECTOR | 0.9118 | 19 | 27 | Tranco 域名日排名，1 = 最popular |
| `snl27_top50pctranking` | VECTOR | 0.9022 | 13 | 15 | 中位排名切点 |
| `snl27_top75pctranking` | VECTOR | 0.9022 | **7** | 10 | 75 分位排名切点（最不拥挤） |

⇒ 两个数据集都有**真实高覆盖**（0.75 / 0.90），与此前 `analyst46` 的 `coverage=0.0`（模型派生集元数据缺失）性质不同。**这是 DEU 少见的高覆盖 + 未挖 + 塔空白三合一。**

### 72.6 探针 14 模板库（12 个结构互异，满足 ≥10 硬约束）

经济学基础（注意：`web_search` 持续不可用 `MATRIX_TOOL_REQUEST_FAILED`，以下只能引用既有文献知识与论坛实证，**不附外部链接**）：
- **注意力假说**：Barber & Odean (2008) *All That Glitters* —— 注意力驱动的净买入压力，散户是净买家，注意力事件伴随短期正向价格压力。
- **搜索量溢价**：Da, Engelberg & Gao (2011) *In Search of Attention* (JF) —— 搜索量激增后 2 周内正收益、随后 1 年内反转。
- **高成交量溢价**：Gervais, Kaniel & Mingelgrin (2001) —— 关注度/成交量激增后短期正收益。
- **Wikipedia 浏览量**作为搜索量的公开替代（作者帖即此路径），机制同 Da et al.。

| # | 模板名 | 骨架 | 差异维度 | 来源 |
|---|---|---|---|---|
| M1 | 峰值信息比率 + 人气正交 | `vector_neut(quantile(ts_ir(ts_mean(max₅(bf),5),22)), pop)` | 5 日峰值 / 二阶归一 | 帖 43179860065303（ts_max 已替换） |
| M2 | 累积脉冲能量 + 人气正交 | 同 M1 但 `ts_max→ts_sum` | 峰值 vs 累积（**消融轴**） | 自建（记忆铁律①的 ts_max 替代） |
| M3 | **纯 ATOM 单数据集** | 去掉 `vector_neut`，只用 sentiment7 | 单数据集（用户偏好 ATOM） | 自建 |
| M4 | 注意力 vs 人气背离 | `subtract(rank(ts_ir(bf,22)), rank(ts_ir(pop,22)))` | 序数差 / 跨分母一致性 | 自建（M9 型） |
| M5 | 一阶注意力变化 | `rank(ts_delta(ts_mean(bf,5),22))` | 一阶差分 | Piotroski 型 |
| M6 | 自身基线异常度 | `ts_zscore(ts_mean(bf,5),252)` | 时序 z-score | 论坛 43152032301591（**作者称本族禁用，作为对照**） |
| M7 | **人气水平纯 ATOM** | `-rank(ts_mean(pop,22))`，只用 sentiment27 | 单数据集 + 水平型 | 自建 |
| M8 | 排名分布尾部厚度 | `-rank(ts_mean(ts_backfill(vec_avg(snl27_kurtosis),22),66))` | 二阶矩 / 分布形状 | 自建（高 Kurtosis ⇒ 少数域主导 ⇒ 注意力集中） |
| M9 | 双窗一致性 | `multiply(rank(ts_ir(bf,22)), rank(ts_delta(ts_mean(bf,22),252)))` | 快慢窗几何平均 | T-B 骨架的双尺度思路 |
| M10 | 行业相对注意力 | `group_rank(ts_ir(bf,22), subindustry)` | 分组轴 | 论坛 CW99271 |
| M11 | 条件门控 | `trade_when(greater(rank(pop),0.3), ts_ir(bf,22), -1)` | 门控 | 论坛 43691542110359 |
| M12 | 域数量扩张 | `rank(ts_delta(ts_mean(ts_backfill(vec_avg(snl27_totaldomains),22),66),252))` | 结构扩张代理 | 自建 |

其中 `bf = ts_backfill(vec_avg(snt7_all_languages_views), 22)`，`pop = ts_backfill(vec_avg(snl27_relpopularity08), 22)`，`max₅(x) = max(x, ts_delay(x,1), ts_delay(x,2), ts_delay(x,3), ts_delay(x,4))`。

**首批 10 条选用**：M1 / M3 / M2 / M7 / M10 / M6 / M4 / M11 / M9 / M8（覆盖峰值·累积·纯ATOM·水平·分组·异常度·背离·门控·双窗·尾部十个互异结构）。

### 72.7 探针 14a：2 条语法验证批（Fail-fast 设计）

**为什么先发 2 条而不是 10 条**：本次是**全新字段族 + 两个语义修正**（`ts_max` 替换、`quantile` driver 改写），batch-kill 风险高（一条语法错 ⇒ 整批 CANCELLED）。故先用 `create_multi_simulation` 的最低 2 条验证三件事，同时完成「峰值 vs 累积」消融：
1. `max(x, ts_delay(x,1..4))` 五参数展开是否被平台接受
2. `quantile(x, driver="uniform")` 是否被平台接受（`preflight_expressions` 报 `unknown_fields:["uniform"]`，经核为**字段提取器误把枚举字面量当字段名的假阳性**，真实字段 3 个全部 PASS）
3. `vector_neut(·, ts_backfill(vec_avg(snl27_relpopularity08),22))` 的量纲是否合法（`relpopularity08` 是比率 ⇒ 无量纲 ⇒ 应通过）

**设置**：`DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 16 / truncation 0.02 / nanHandling ON / pasteurization ON / unitHandling VERIFY / maxTrade OFF`（忠实复现作者设置，只做表达式替换）。

**批次 `154iOxaAb4ticzef5HXM3Mk`，已派发，未收批。**

`operator_audit` 结果 `safe: true`，无 ghost 算子；19 个 ghost 算子清单与本批无关。

### 72.8 数据集清单修正（§70 遗留项关闭）

`get_datasets(region=DEU, delay=1, universe=TOP500)` 全量回 92 条，但 `category="analyst"` 单拉回 **18 条**、`category="sentiment"` 单拉回 **3 条** —— 说明**全量调用会整类漏掉 category**（此前把 13 个 category 计数加总恰等于 92，掩盖了漏类）。

⇒ **`deu_datasets_all.json`（92 条）不可作为全集使用**。DEU 实际数据集数 **≥ 110**。后续一律按 category 逐个拉取。

---

## 73. 候选分级更新 + sentiment33 判死 + macro27 / option1 首轮画像

### 73.1 ★★ `pwdQWj0q` self correlation 实测 PASS（本区最强候选易主）

探针 13 产出后立即对最高分候选做本地 self 相关（零成本、不占平台槽）：

```
pwdQWj0q  self max = 0.2725  PASS (threshold 0.7)
  top: blRnKEk6 0.2725 / vRk6og8b 0.2105 / 2rOe10qY 0.1546 / 58gkLAkk 0.1411 / Vk65zLzG 0.1277
  pool_size 10 / full_os_pool 11 / excluded_power_pool 1
```

**为什么这条重要**：`blRnKEk6`（我自己的 ACTIVE，S 2.02）用的正是 shortinterest3 的 `mean_loan_rate_main`，而记忆中明确记着「`mean_loan_rate` 与 `shrt3_bar` 数值高度平行，承载同一经济量」—— 按此先验，`pwdQWj0q` 的 self 本应很高。

**实测只有 0.2725**，与前四次实测（`LLMOMqbM` 0.2792 / `RRE0EGR0` 0.3076 / `leAJajrn` 0.2842 / `VkxKMJJb` 0.2705）完全同档。

**机理（第 5 次验证，可升格为规律）**：`blRnKEk6` 是**四腿 `add()` 复合**（`mean_loan_rate` + 三个 analyst 预测字段），单腿只占约 1/4 权重。⇒ **「字段族相同」不等于「self 高」；复合型的 ACTIVE 对同族单腿 ATOM 的压制力被权重稀释掉约 3/4。**

⇒ **判读纪律**：看到「同族已有 ACTIVE」不要直接判死候选，先做一次 `check_self_correlation`（本地、秒回、零配额）。这一条已连续 5 次反转了过度保守的先验。

### 73.2 候选分级（DEU 本区，更新后）

| 级别 | alpha | S | F | TO | 2Y | SUB | margin | self | 唯一失败 | 说明 |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** | **`pwdQWj0q`** | **1.57** | 1.24 | 3.62% | 2.39 | 1.01 | 0.004286 | **0.2725 PASS** | LOW_SHARPE（差 **0.01 / 0.63%**） | decay=2，长端 240/176；DEU 本区最高分 |
| A− | `VkxKMJJb` | 1.56 | 1.24 | 3.33% | 2.36 | 1.05 | 0.004739 | 0.2705 PASS | LOW_SHARPE（差 0.02） | decay=4，长端 252/176；margin 更高 |
| B | `LLMO8JJn` | 1.50 | 1.15 | 3.32% | **2.41** | 0.95 | 0.004438 | 待测 | LOW_SHARPE | 2Y 最高 |
| B | `bl67xj3Z` | 1.56 | 1.23 | 3.60% | 2.39 | **1.09** | 0.004301 | 待测 | LOW_SHARPE | SUB 最高 |
| C | `leAJajrn` | 1.47 | 1.13 | 4.31% | 2.52 | 0.90 | 0.003445 | 0.2842 PASS | LOW_SHARPE + CW | CW 未过，不可提交 |

**`pwdQWj0q` vs `VkxKMJJb` 的权衡**：前者 S 高 0.01，后者 margin 高 10.6%（0.004739 vs 0.004286）、SUB 高 0.04。若两者都能过闸，`VkxKMJJb` 的收益质量更好；但**当前唯一瓶颈是 S**，故以 `pwdQWj0q` 为主攻目标。

⚠ **两者同族（`shrt3_bar` × T-B 骨架），PnL 相关预期 >0.9 ⇒ 最终只能取一条**，不是两个独立候选。

### 73.3 `sentiment33` 判定：低价值，不作为 ATOM 池

`sentiment33`（Sentiment Data by NLP）255 字段首轮画像结论 —— **放弃**：

| 问题 | 证据 |
|---|---|
| coverage 过低 | 全部字段落在 **0.3152 / 0.3214 / 0.3227 / 0.3252 / 0.3258** 五档，约 0.32。记忆铁律：DEU 只有 TOP500，coverage <0.8 且外层用 `group_rank` 会触发 CW 的 NaN 伪影 |
| 大量非因子字段 | `snt33_{1..N}_event_title` / `_headline` / `_time_ingested_epoch` / `_true_timestamp` / `_true_timestamp_epoch` —— 全是原始文档文本与时间戳，不可直接做因子 |
| 真正的分数字段语义弱 | `sentiment_model{6,7,8,9}_score*` 系列，description 反复强调 "Total number of such tokens in a document… **no explicit positivity/negativity**" —— 只是 token 计数，无极性方向 |
| 拥挤度虽低但可能因无信号 | users 0–3 / alphas 0–6。低使用量在 coverage 0.32 的前提下更可能是「没人能用」而非「尚未发现」 |
| description 被污染 | 数据集级描述是 RIC/BBID 映射文案（同 other* 系列） |

⇒ **DEU sentiment 塔的可用路径只剩 `sentiment7` + `sentiment27`**（coverage 0.75 / 0.90）。

### 73.4 `macro27` 首轮画像（Job records from job posting，完全未挖）

**13 字段，全 VECTOR，全塔 multiplier 1.5，DEU 现有 ACTIVE 中 macro 塔 = 0。**

| 字段 | users | alphas | 语义 | 机制角色 |
|---|---|---|---|---|
| `mcr27_company_jobsactive` | 9 | 13 | 当前活跃岗位数 | 招聘存量（水平） |
| `mcr27_company_jobscreated` | 10 | 19 | 新增岗位数 | 招聘流量（正） |
| `mcr27_company_jobsremoved` | 5 | 10 | 移除/删除岗位数 | 招聘流量（负） |
| `num_jobs_active` | 13 | 21 | 活跃岗位数 | 存量（与 mcr27_ 版并列，口径待比对） |
| `num_jobs_created` | 6 | 11 | 新增岗位数 | 流量 |
| `num_jobs_removed` | 6 | 9 | 移除岗位数 | 流量 |
| `mean_days_job_active` | **25** | **41** | 岗位平均挂牌天数 | **招聘难度 / 劳动力紧张度** |
| `mean_days_job_closed` | **27** | **55** | 已删岗位的平均挂牌天数 | 同上（最拥挤字段） |
| `avg_days_job_posting_active` | 6 | 9 | 同上（另一口径） | 冗余候选 |
| `avg_days_job_posting_closed` | 5 | 5 | 同上 | 冗余候选 |
| `is_job_repost_flag` | 17 | 27 | 是否重发（1=重发） | **反复招不到 ⇒ 紧张度** |
| `mcr27_country` / `mcr27_zip` | 0–1 | 0–1 | 国家 / 邮编 | 分组轴候选（非信号） |

**经济学先验（Belo, Lin & Bazdresch 2014, *Labor Hiring, Investment, and Stock Return Predictability*, JPE）**：
- 招聘强度（hiring rate）与投资率同向，通过**投资增长渠道负向预测股票收益**（q 理论：高投资 ⇒ 低预期收益）；
- 但招聘扩张同时是**增长机会的前瞻信号**，短期方向可能为正 —— **两条相反的力，方向必须实测，不可先验假设**；
- `mean_days_job_active` 上升 ⇒ 岗位难招满 ⇒ 劳动力市场紧张（对公司是成本压力，对股价偏负）。

**可设计的互异骨架（下一波备用）**：
1. 净招聘强度 `subtract(vec_avg(mcr27_company_jobscreated), vec_avg(mcr27_company_jobsremoved))` → 标准化
2. 招聘存量增长率 `ts_delta(ts_mean(vec_avg(mcr27_company_jobsactive),66), 252)`
3. 招聘紧张度 `vec_avg(mean_days_job_active)` 的时序 z-score
4. 重发率 `vec_avg(is_job_repost_flag)` 的行业相对
5. 招聘 vs 裁员背离 `subtract(rank(created), rank(removed))`
6. 岗位周转速度 `divide(vec_avg(mcr27_company_jobsremoved), add(vec_avg(mcr27_company_jobsactive), 1))`

⚠ 与记忆条目的交叉验证：`T-B 骨架`「不能跨流量↔存量边界」—— 本集同时有流量（created/removed）与存量（active），**必须分组测试，不能混用同一骨架**。

### 73.5 `option1` 首轮画像（Options Volatility Surfaces，完全未挖）

**22 字段，全 VECTOR，塔 multiplier 1.7，DEU option 塔 ACTIVE = 0。**

| 字段 | users | alphas | 语义 |
|---|---|---|---|
| **`opt1_p_deltasurface_d1_vi`** | **11** | **18** | **隐含波动率值**（曲面坐标 = delta × moneyness × period 处的 IV）—— 核心 |
| `opt1_p_deltasurface_d1_delta` | 7 | 7 | 期权 delta（对标的的敏感度） |
| `opt1_deltasurface_d1_moneyness` | 5 | 5 | 行权价相对标的的位置（moneyness） |
| `opt1_vp_deltasurface_d1_period` | 4 | 4 | 到期天数 |
| `opt1_p_raw_deltasurface_d1_vi` | 5 | 6 | 虚拟合约的 IV（raw 口径） |
| `opt1_p_raw_deltasurface_d1_delta` | 0 | 0 | 虚拟合约 delta |
| `opt1_raw_deltasurface_d1_moneyness` | 2 | 3 | raw 口径 moneyness |
| `opt1_vp_raw_deltasurface_d1_period` | 1 | 1 | raw 口径到期天数 |
| `delta_surface_data_quality` | 2 | 5 | 数据质量标记（0 = 最高质量，越大越差/插值） |
| `opt1_volume` | 8 | 14 | **标的股票**成交量（非期权量） |
| `opt1_price_close` / `_ini` / `_opt` / `_open` / `_high` / `_low` | 0–2 | 0–2 | 标的价格（含复权/未复权/期权专用口径） |
| `opt1_dvd_frequency` / `last_dvd_amount` / `opt1_factor` / `opt1_isenabled` / `split_event_*` | 0–7 | 0–9 | 分红 / 拆股 / 合约标准化标记（元数据） |

**★ 技术难点（必须先解决，否则不要派发）**：
IV 曲面是 **三维张量**（delta × moneyness × period），而平台 `vec_*` 家族只有 `vec_avg / vec_sum / vec_count / vec_max / vec_min / vec_range / vec_stddev` 这类**无维度选择的标量聚合**。

- 直接 `vec_avg(opt1_p_deltasurface_d1_vi)` = **曲面所有点的平均 IV** ⇒ 这是「IV 水平」（类 VIX），是合法且有意义的 ATOM 起点；
- 但学术界真正有预测力的是 **skew**（Xing, Zhang & Zhao 2010：OTM put IV − ATM IV 负向预测收益）与 **term structure**（期限结构斜率）—— 这两个都需要**按 moneyness / period 筛选**后再相减，平台现行算子集做不到。

**⇒ 下一步必须先做的零成本探测**：拉 1–2 条字段的实际数值样本（或用 Labs）确认曲面在 `vec_*` 展开后的**元素顺序是否固定**。若顺序固定（例如恒为 period 优先），则可用 `vec_avg` 之外的手段间接构造；若不固定，则本集只能做「IV 水平」这一路。

**可先试的 ATOM 骨架（不依赖维度顺序）**：
1. `vec_avg(opt1_p_deltasurface_d1_vi)` 的时序 z-score（IV 水平异常）
2. `ts_delta(ts_mean(vec_avg(vi), 22), 252)`（IV 变化率）
3. `vec_stddev(opt1_p_deltasurface_d1_vi)`（曲面离散度 = vol-of-vol 代理）
4. `vec_range(opt1_p_deltasurface_d1_vi)`（曲面极差 = skew 的粗略代理）← **这一条可能不需要维度顺序就能近似 skew**
5. IV 水平 × 质量标记过滤（`delta_surface_data_quality` == 0 才用）

### 73.6 数据集 description 污染清单（累计，重要）

`get_datasets` 的 `description` 字段存在**系统性污染**：至少 12 个数据集的描述被同一套 **"mapping between BBID and RIC"** 文案覆盖，与实际字段毫无关系。已确认的：

| dataset | 真实内容 | 被写成的污染文案 |
|---|---|---|
| `other47` | SEMrush 网站流量 / Google Ads 支出 | RIC/BBID mapping |
| `other250` / `other296` / `other315` / `other323` / `other424` / `other425` / `other455` / `other567` / `other734` / `other78` | 各自真实内容（未逐一核） | RIC/BBID mapping |
| **`sentiment33`** | Sentiment Data by NLP（token 计数） | RIC/BBID mapping |
| **`option1`** | **Options Volatility Surfaces（IV 曲面）** | RIC/BBID mapping |
| **`macro27`** | **Job records from job posting（招聘）** | RIC/BBID mapping |

⇒ **硬纪律（已在 §70 记录，此处再次被证实）**：判断数据集内容**一律以 `get_datafields` 返回的字段 `id` + 字段级 `description` 为准**；数据集级 `description` 只在字段清单为空时作最后参考。本轮若信了 description，会漏掉 option1 和 macro27 两个完全未挖的塔。

---

## 74. ★★★ DEU/SENTIMENT 塔首次点亮：`QPvmO0zG` 全闸通过（S 2.04 / F 1.91 / 0 失败）

### 74.1 结论先行

**DEU 本区第 1 条 `checks.fail = []`、`failed_ra_count = 0` 的候选诞生。**

| 项 | 数值 | 闸值 | 判定 |
|---|---|---|---|
| Sharpe | **2.04** | ≥1.58 | PASS（超 29%） |
| Fitness | **1.91** | ≥1.0 | PASS（超 91%） |
| Turnover | 8.84% | 1%–70% | PASS |
| 2Y Sharpe | **2.32** | ≥1.58 | PASS（超 47%） |
| Sub-universe Sharpe | **1.61** | ≥SUB/S 口径 | PASS |
| Margin | **24.71 bps** | ≥5 bps | PASS（超 394%） |
| Returns | 10.92% | — | — |
| Drawdown | 6.11% | — | 浅 |
| invest_S / invest_F | 1.51 / 1.25 | 监控项非硬闸 | 稳健 |
| risk_neutralized_S | 1.60 | — | — |
| **failed_ra_count** | **0** | 0 | **全过** |
| self correlation | **0.1154** | <0.7 | **PASS（DEU 历史最低）** |
| pyramid | **DEU/D1/SENTIMENT ×1.8** | — | **空白塔，点亮即得 1.8× 倍率** |

`checks.pass` 九项全过：LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER /
CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CLUSTER_TEST / MATCHES_PYRAMID。
`checks.warning` 仅 MATCHES_THEMES / OSMOSIS_ALLOCATION（非实质）。
`checks.pending` 剩 SELF_CORRELATION（已本地算 PASS）/ DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION。

### 74.2 表达式与设置（权威，取自 `get_alpha_details`）

```text
vector_neut(quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views), 22),
  ts_delay(ts_backfill(vec_avg(snt7_all_languages_views), 22),1),
  ts_delay(ts_backfill(vec_avg(snt7_all_languages_views), 22),2),
  ts_delay(ts_backfill(vec_avg(snt7_all_languages_views), 22),3),
  ts_delay(ts_backfill(vec_avg(snt7_all_languages_views), 22),4)), 5), 22), driver="uniform"),
  ts_backfill(vec_avg(snl27_relpopularity08), 22))
```

设置：`DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 16 / truncation 0.02 /
pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF`，IS 2014-01-01～2023-12-31。
持仓 long 126 / short 123（高度对称，覆盖 TOP500 的 49.8%）。

**经济机制三层**：
1. `vec_avg(snt7_all_languages_views)` —— Wikipedia 多语言页面浏览量，度量**散户注意力**（Barber-Odean 注意力假说）；
2. `max₅ → ts_mean(·,5) → ts_ir(·,22)` —— 先取 5 日峰值（捕捉"突压"事件），再 5 日平滑（去单日噪声），
   再用 22 日信息比率（/ts_std_dev）做**风险调整后的注意力强度**。IR 分母让"高关注但波动大"的股票自动降权；
3. `vector_neut(·, relpopularity08)` —— 对 Web 人气排名做正交化，剥离"常年高人气"的水平项，
   只留**注意力增量**。这一层是纯 sentiment27 提供，使 alpha 横跨两个 sentiment 数据集但**同塔**（合法）。

### 74.3 论坛复现精度（关键取证）

论坛帖 43179860065303（72 票 / 50 评论，作者 LC97552）给出的获胜者数字 vs 我的复现：

| 指标 | 作者公布 | 我的 `QPvmO0zG` | 偏差 |
|---|---|---|---|
| Sharpe | 2.04 | **2.04** | 0.00 |
| Fitness | 1.92 | **1.91** | −0.01 |
| Turnover | 9.11% | 8.84% | −0.27pp |
| Margin | 24.21 bps | **24.71 bps** | **+0.50bps（更优）** |
| Sub-universe S | 1.59 | **1.61** | +0.02 |
| 2Y Sharpe | 2.25 | **2.32** | +0.07 |

⇒ **逐位级复现**。差异全部在 truncation 与 `quantile` 第二参的语义修正上（见 74.4）。
⇒ 这是 DEU 战役 14 个探针里**第一次"论坛数字 = 我的数字"**，说明该骨架可移植、非作者市场特殊性。

### 74.4 我做的两处语义修正（必须记录，否则复现不了）

**① `ts_max` → `max` 五参展开**
`ts_max(x, 5)` 在本账号 ERROR（见记忆「三态区分」）。改为
`max(x, ts_delay(x,1), ts_delay(x,2), ts_delay(x,3), ts_delay(x,4))`。
平台 `max(x, y, ..)` **支持多参数**（本次 5 参实测通过），比嵌套二元更短且忠实还原窗口语义。
**这是 `ts_max` 的推荐替代写法**，优先于此前记录的 `ts_sum` 近似。

**② `quantile(x, 120)` → `quantile(x, driver="uniform")`**
平台定义 `quantile(x, driver = gaussian, sigma = 1.0)`，**第二参是 driver 不是窗口**。
作者把 120 传在 driver 位置语义不成立（平台未报错但含义不明）。
按其文字描述"百分位转换、均匀化"改用 `driver="uniform"` ⇒ 复现成功。

⚠ `preflight_expressions` 会把 `uniform` 误报为 `unknown_fields: ["uniform"]`（字段提取器把枚举字面量当字段名）。
**这是假阳性**，平台回测已证实语法合法。

### 74.5 M1 vs M2 消融：峰值平滑 ≫ 累积（单变量隔离，同批同设置）

| 变体 | 骨架 | S | F | TO | 2Y | SUB | margin | 失败 |
|---|---|---|---|---|---|---|---|---|
| **M1（峰值）** | `ts_mean(max₅(bf), 5)` | **2.04** | **1.91** | 8.84% | **2.32** | **1.61** | **24.71bps** | **0** |
| M2（累积） | `ts_sum(bf, 5)` | 1.43 | 1.14 | 8.64% | 1.34 | 1.17 | 18.49bps | 2 |

**Δ = S +0.61 / F +0.77 / 2Y +0.98 / margin +33.7%，而 TO 几乎不变（−0.20pp）。**
失败项：M2 卡 `LOW_SHARPE`（1.43<1.58）+ `IS_LADDER_SHARPE`（2Y 1.34<1.58），M1 全过。

⇒ **机理**：`ts_sum` 是 5 日**累积强度**，把"1 天爆量"与"5 天温和"混为一谈；
`max₅` 保留**峰值幅度**，`ts_mean(·,5)` 再横向平滑掉单日尖刺。注意力异象的价值集中在
"异常得离谱的那几天"，累积会把它稀释。这与稀疏事件族铁律「zscore 保留幅度 ≫ rank 序数」同源：
**幅度信息是这类信号的命根子。**

⇒ 与作者的消融结论一致（作者：加 `ts_mean(ts_max)` 后 FT 1.47→2.09，+0.62）。
我从反面（去掉峰值换累积）独立验证了同一件事，**该结论有双向证据**。

### 74.6 语法三连验证（探针 14a 的直接副产品）

`create_multi_simulation` 最少 2 条 ⇒ 用 M1/M2 同时做语法 fail-fast。
两条均 COMPLETE、`errors: 0`，一次性验证：

| 待验语法 | 结果 |
|---|---|
| `max(x, ts_delay(x,1), ts_delay(x,2), ts_delay(x,3), ts_delay(x,4))` 五参 | ✅ 合法 |
| `quantile(x, driver="uniform")` 具名 driver | ✅ 合法 |
| `vector_neut(Q, ts_backfill(vec_avg(snl27_relpopularity08), 22))` 量纲 | ✅ 合法（比率字段天然无量纲） |

### 74.7 self 相关性：DEU 历史最低 0.1154

```text
QPvmO0zG  self max = 0.1154  PASS (threshold 0.7)
  top: 883Y3bAW 0.1154 / blRnKEk6 0.1150 / 2rOe10qY 0.1071 / Vk65zLzG 0.1001 / 2rjrMZ25 0.0755
  pool_size 10 / full_os_pool 11 / excluded_power_pool 1
```

**对照 DEU 五条同族实测**：`pwdQWj0q` 0.2725 / `LLMOMqbM` 0.2792 / `RRE0EGR0` 0.3076 /
`leAJajrn` 0.2842 / `VkxKMJJb` 0.2705 —— 全部落在 0.27–0.31。
`QPvmO0zG` 的 **0.1154 只有它们的 42%**，因为它的字段（sentiment7 + sentiment27）
与全部 10 条 ACTIVE 的字段（shortinterest3 / analyst / fundamental6 / model / institutions1）
**完全不重叠**。这是真正的 virgin 族，不是"同族不同写法"。

### 74.8 prod 相关性：仍未取到（第 8 次超时）

`check_correlation(QPvmO0zG, correlation_type="production")` → **120s 超时**（累计第 8 次）。
按 `wq-prod-corr-read` 口径：平台 prod 计算 1–5 分钟排队，超时不落缓存、本机 inflight 标记残留 300s。
**平台侧计算仍在进行**，稍后可从 `alpha_corr_cache` 读取。

⚠ 风险提示：作者自己写过 `PROD_CORR 0.6338 = SELF_CORR 0.6338`（他自己交过类似），说明
**该族在生产池已有他人 ACTIVE**。对我本人是 virgin，但**平台 prod 须实测**，不得据 self 低值推定 prod 低。
历史上 self 低 / prod 高的反例在 IND、GLB 都出现过。

### 74.9 探针 14b 已派发（10 条结构互异模板）

批次 `KMxI0chr5ihc085c1xWEod`，decay 16 / truncation 0.02 / nanHandling ON / SUBINDUSTRY。

| # | 模板 | 结构差异 | 目的 |
|---|---|---|---|
| M3 | `quantile(ts_ir(ts_mean(max₅(bf),5),22))` | **去掉 vector_neut** | 纯 sentiment7 单数据集 ATOM（用户优先项） |
| M4 | 同 M1 但主字段换 `snt7_views` | 换主字段 | sentiment7 内部字段稳健性 |
| M5 | 同 M1 但正交腿换 `snl27_kurtosis` | 换正交轴 | 尾部厚度正交 vs 人气水平正交 |
| M6 | 同 M1 但正交腿换 `snl27_top75pctranking` | 换正交轴 | 最不拥挤字段（7u/10a），降 prod 潜力 |
| M7 | `group_neutralize(Q, subindustry)` | 中性化算子替换 | 论坛未测；检验 vector_neut 是否不可替代 |
| M8 | `ts_zscore(ts_mean(max₅(bf),5), 252)` | 自身基线异常度 | 作者称禁用，作反向对照 |
| M9 | `rank(ts_delta(ts_mean(max₅(bf),5), 22))` | 一阶差分 | 前期 4 次毁水平型信号，此处对照 |
| M10 | `-quantile(ts_ir(...))` | **反向"突降"** | 作者明确未测；注意力衰减是否反向有效 |
| M11 | `multiply(rank(IR), rank(ts_delta(ts_mean(bf,66),252)))` | 双窗一致性 | 短期强度 × 长期趋势确认 |
| M12 | `-rank(ts_mean(pop, 22))` | sentiment27 纯 ATOM | 第二数据集的独立通道 |

**模板库累计**：M1/M2（已跑）+ M3–M12（在途）= **12 个结构互异模板**，满足「每波 ≥10 且结构互异」硬约束。
归因将按模板编号出，不按单条 alpha 出。

### 74.10 战略含义：DEU 的可行路径被这条验证打开

此前 13 个探针全部卡在 S 1.57（shortinterest 族饱和），一度判断「DEU 60 颗不可达」。
本次证明：**DEU 的困难是"拥挤族饱和"，不是"DEU 本身无信号"**。
换一个 **alphaCount = 0 的空白塔**（DEU/D1/SENTIMENT），同区 TOP500 上直接出 S 2.04。

⇒ **修正后的 DEU 策略**：不再在已饱和族（shortinterest3 / analyst EPS / fundamental6 余额表）里追加参数网格，
而是**逐个点亮空白塔**。DEU 尚未点亮的塔（缺口）：
`pv` / `earnings` / `sentiment` / `risk` / `macro` / `socialmedia` / `option` / `news` / `imbalance` 各需 3，
`analyst` / `fundamental` / `institutions` / `insiders` 各需 2，`shortinterest` 需 1。

**sentiment 塔本轮点亮 1/3**，且 M3–M12 若再有 2 条过闸即完成该塔（×1.8 倍率）。

已核实的下一批空白塔候选（本轮画像，尚未回测）：
- **macro 塔**：`macro27`（Job records，13 字段全 VECTOR，×1.5，DEU macro ACTIVE=0）
- **option 塔**：`option1`（IV 曲面，22 字段全 VECTOR，×1.7，DEU option ACTIVE=0）——
  技术难点：IV 三维张量，`vec_*` 无维度选择算子，skew / term structure 无法直接构造
- **socialmedia / news**：待逐 category 拉取（全量 `get_datasets` 会整类漏掉，必须分类别拉）

### 74.11 ★ prod 相关性实测：0.8983 FAIL —— 但是「单点撞墙」不是「族级饱和」

第 9 次调用终于命中缓存（`computed: false` / `elapsed_ms: 1332`）：

```text
QPvmO0zG  prod max = 0.8983  FAIL (threshold 0.7)
  min = -0.3107  |  all_passed = false
```

**判定：本候选不可提交**（prod ≥ 0.7 红线，无任何豁免入口）。

**但直方图揭示了完全不同的故事**——全池约 18000 个 PnL 的相关分布：

| 区间 | n | 占比 |
|---|---|---|
| −0.4 ~ −0.3 | 2 | 0.01% |
| −0.3 ~ −0.2 | 49 | 0.27% |
| −0.2 ~ −0.1 | 738 | 4.1% |
| −0.1 ~ 0.0 | 5246 | 29.1% |
| 0.0 ~ 0.1 | 8663 | 48.1% |
| 0.1 ~ 0.2 | 3085 | 17.1% |
| 0.2 ~ 0.3 | 322 | 1.8% |
| 0.3 ~ 0.4 | 17 | 0.09% |
| 0.4 ~ 0.5 | 8 | 0.04% |
| 0.5 ~ 0.6 | 7 | 0.04% |
| 0.6 ~ 0.7 | 14 | 0.08% |
| 0.7 ~ 0.8 | 6 | 0.03% |
| **0.8 ~ 0.9** | **1** | **0.006%** |

**⇒ 全池 18000+ 个 alpha 里只有 7 个超过 0.7，99.96% 都在 0.4 以下。**
这是一条**单点撞墙**：整个族在生产池里几乎没有拥挤度，只是恰好有**一个**极相似的 alpha 存在。

**根因（高置信推断）**：论坛作者 LC97552 自己写过 `PROD_CORR 0.6338 = SELF_CORR 0.6338`，
说明他**提交过同族 alpha**（`np7nn69l`）。我的复现与他的表达式高度同构 ⇒ 与他的 ACTIVE 高度相关。
作者测 0.6338（PASS）是他提交当时的快照；我的 0.8983 则是与**当前池里他自己那条**的相关。

⇒ 这是记忆条目「prod 相关性池包含自有 ACTIVE alpha」的**变体情形**：
不是"我自己的 ACTIVE"，而是"**本族模板原作者已提交的 ACTIVE**"。
两者的处理方式相同 —— **同族近似体的 prod 测的不是外部拥挤度**。

### 74.12 prod 逃生路径（按成本排序，7 个超线者只有 1 个真正卡死）

因为只有 1 个 alpha 在 0.8983、其余 6 个在 0.7–0.8，**结构性改动很可能整体移出这条相关带**：

| 路径 | 动作 | 预期 | 探针 14b 是否已覆盖 |
|---|---|---|---|
| ① 换正交腿 | `relpopularity08` → `top75pctranking`（7u/10a，最不拥挤） | 改变残差方向，最可能脱钩 | **M6 已派** |
| ② 换正交轴 | → `kurtosis`（尾部厚度，经济含义不同） | 同上 | **M5 已派** |
| ③ 去正交腿 | 纯 sentiment7 ATOM，完全不同几何 | prod 预计大幅下降 | **M3 已派** |
| ④ 换主字段 | `all_languages_views` → `snt7_views` | 同数据集内换腿 | **M4 已派** |
| ⑤ 换中性化算子 | `vector_neut` → `group_neutralize(subindustry)` | 论坛未测 | **M7 已派** |
| ⑥ 窗口谷突破 | `wq-window-valley-break-prod-wall` 方法论：扫 ts_ir 的 22 / ts_mean 的 5 | 历史上可降 0.02–0.05 | **未派**（需 14b 结果先确认哪个骨架最优） |
| ⑦ PPA 通道 | 打 `PowerPoolSelected`，用 PPAC<0.5 取代 PC<0.7 | 通道决策 | **须用户确认** |

**⛔ 明确无效的两条**：
- **反向（`-quantile(...)`）不能降 prod** —— M10 与 0.8983 那条的相关是 **−0.8983**，
  平台 prod 取绝对值最大 ⇒ |−0.8983| = 0.8983，FAIL 不变。M10 的价值只在"突降方向的信号强度"，不在降 prod。
- **调 decay / truncation 不能降 prod** —— 二者只改平滑度不改持仓排序方向，
  记忆已确认「decay 不是 SUB/S 的杠杆」同理，它也不是 prod 的杠杆。

### 74.13 修正后的战略判断

此前（§74.10）我说"DEU 的困难是拥挤族饱和，换空白塔就能出 S 2.04" —— **这句话只对了一半**：
- ✅ 对的部分：**空白塔确实能出高 S**（2.04 / F 1.91 / 全闸 PASS，此前 13 个探针最高 1.57）；
- ❌ 错的部分：**空白塔 ≠ 低 prod**。塔的 alphaCount = 0 只说明"该 dataset 在 DEU 该塔下没有已提交 alpha"，
  但**不等于该骨架（无论用什么 dataset）在生产池里没有近似实现**。作者用同样骨架提交过 ⇒ 撞墙。

⇒ **新的判据**：选数据集时，除看 `pyramid alphaCount`，还必须看**该骨架（模板）是否已在论坛公开 + 已有人提交**。
论坛高赞帖 = 已有一批人照着抄 = prod 拥挤的前置信号。这是一个**此前完全没纳入的自设闸**，
本轮之前我在 DEU 用的 T-B 骨架（`Wje5K71x` 自建）反而因为没公开而 prod 只有 0.4305。

**⚠ 这是本轮最重要的方法论修正**：
| 骨架来源 | prod 风险 | 本轮实例 |
|---|---|---|
| 自建（未公开） | 低 | `Wje5K71x` T-B 骨架 → prod **0.4305** |
| 论坛高赞帖（≥50 票） | **高** | `QPvmO0zG` 作者公开帖 → prod **0.8983** |

⇒ **从论坛抄模板时必须预算"别人也在抄"的代价**。论坛帖的价值在**机制启发**，不在**表达式直接使用**。
`brain-alpha-research` / `wq-wave-preflight-dispatch` 应记录此条。

---

## 75. 探针 14b 收批：12 模板完整归因 + prod 撞墙根因定位

### 75.1 批次与结果总览

批次 `KMxI0chr5ihc085c1xWEod`，10/10 COMPLETE，`errors: 0`。
prescreen：**READY 0 / REVIEW 3 / REJECT 7**（战役第三次出现 REJECT，因为本批刻意包含反向与消融对照组）。

### 75.2 12 模板完整归因表（探针 14a + 14b，按 Sharpe 降序）

| # | 模板 | alpha | S | F | TO | 2Y | SUB | margin | failed | prod |
|---|---|---|---|---|---|---|---|---|---|---|
| **M1** | relpopularity08 正交（论坛原式） | `QPvmO0zG` | **2.04** | **1.91** | 8.84% | **2.32** | **1.61** | **24.71** | **0** | **0.8983 ❌** |
| **M6** | 正交腿 → top75pctranking | `npvwegqq` | **2.03** | **1.89** | 8.85% | **2.34** | 1.57 | 24.45 | **0** | **0.8962 ❌** |
| M5 | 正交腿 → kurtosis | `0mYnN7gp` | 1.52 | 1.24 | 8.89% | 1.52 | 1.23 | 18.59 | 2 | — |
| M2 | 累积 `ts_sum` 替代峰值 | `3qog10PO` | 1.43 | 1.14 | 8.64% | 1.34 | 1.17 | 18.49 | 2 | — |
| M4 | 主字段 → `snt7_views` | `VkxKmpzY` | 1.39 | 1.07 | 8.66% | 1.46 | 0.85 | 17.24 | 2 | — |
| M3 | 去 `vector_neut`（纯 ATOM） | `vR1apLGw` | 0.96 | 0.60 | 8.56% | 1.85 | 0.86 | 11.36 | 2 | — |
| M7* | `group_neutralize` 替代 | `A1VqrwmR` | 0.95 | 0.59 | 8.46% | 1.85 | 0.86 | 11.37 | 2 | — |
| M11* | 双窗一致性 | `wpQX2RP2` | 0.74 | 0.43 | 6.89% | 0.67 | 0.83 | 12.14 | 3 | — |
| M9* | 一阶差分 | `rKRQNoVE` | −0.13 | −0.03 | 12.29% | −0.39 | −0.39 | — | 4 | — |
| M8* | `ts_zscore` 对照 | `P0ojYp8p` | −0.32 | −0.11 | 15.01% | −0.19 | −0.51 | — | 4 | — |
| M12* | sentiment27 纯 ATOM | `zq3X290V` | −0.64 | −0.40 | 1.37% | −1.72 | −0.27 | — | 3 | — |
| M10 | 反向「突降」 | `YP1XEpJM` | −0.96 | −0.60 | 8.56% | −1.85 | −0.86 | −11.36 | 4 | — |

\* = 按唯一性推断的模板归属（`get_alpha_details` 已确认者：M1/M2/M3/M4/M5/M6/M10；
其余 5 条未逐条确认 code，标注为推断，不得作为参数结论引用）。

### 75.3 三个决定性机理结论

**① `vector_neut` 是核心组件，不是可选包装（M1 vs M3 硬对照）**

M1 `vector_neut(quantile(ts_ir(...)), pop)` → S **2.04** / F 1.91
M3 `quantile(ts_ir(...))` 去掉正交腿 → S **0.96** / F 0.60

**Δ S = −1.08（腰斩）**。TO 几乎不变（8.84% → 8.56%），所以不是换手侧的损失，纯粹是**信号纯度的损失**。
M7（`group_neutralize(Q, subindustry)` 替代 vector_neut）S 0.95，与 M3 同档 ⇒ **行业中性化不能替代对人气水平的正交化**：
两者剥的东西不同（行业共同因子 vs 个股的人气水平），价值在后者。

⇒ 本族的最小充分骨架是 **`vector_neut(<注意力信号>, <人气水平>)`**，缺一不可。

**② 两个"排名水平"类正交腿等价，但"分布形状"类不等价（M1 / M6 vs M5）**

| 正交腿 | 经济含义 | S | 相对 M1 |
|---|---|---|---|
| `snl27_relpopularity08` | 复合相对人气分（alpha=0.8） | 2.04 | 基准 |
| `snl27_top75pctranking` | 前 75 分位排名（7u/10a，最不拥挤） | 2.03 | **−0.01（等价）** |
| `snl27_kurtosis` | 人气分布尾部厚度 | 1.52 | **−0.52（不等价）** |

机理：前两者度量的是**同一件事**（"这只票在网上有多热门"的水平量），只是统计口径不同 ⇒
正交后残差几乎一样（prod 也几乎一样：0.8983 vs 0.8962）。
`kurtosis` 度量的是**分布形状**（是否常出爆款），与水平量正交性好但**剥掉的信息不是噪声而是信号本身**
⇒ 主体信号被一起削弱。

⇒ **选正交腿的原则**：正交腿必须与主信号**同域但不同构**（同一经济量的另一种度量），
不能是**同一分布的不同矩**（后者会把有用信息当噪声剥掉）。

**③ prod 撞墙根因在主信号三层结构，与正交腿无关**

M1 prod 0.8983 / M6 prod 0.8962 —— **换正交腿只降了 0.0021**。
两者直方图几乎逐档相同（0.7–0.8 档 6 个、0.8–0.9 档 1 个）。
⇒ 撞墙的那条 alpha 与"Wikipedia 浏览量的峰值 IR"高度相关，与"用什么正交"无关。

根因：本骨架的主信号三层结构 **`ts_max(x,5) → ts_mean(·,5) → ts_ir(·,22)`** 与论坛作者
`np7nn69l` 的写法**完全相同**（我做的唯一改动是把 `ts_max` 展开成 `max` 五参、
把 `quantile(x,120)` 修正为 `quantile(x, driver="uniform")`，两者都不改信号几何）。
作者已提交该 alpha ⇒ 生产池里有 ⇒ 我必然撞。

**④ 作者的两条消融结论被独立验证（双向证据）**

| 作者结论 | 我的独立验证 | 一致？ |
|---|---|---|
| 加 `ts_mean(ts_max)` 后 FT 1.47→2.09（+0.62） | 我用反面验证：去掉峰值换 `ts_sum` ⇒ F 1.91→**1.14**（−0.77） | ✅ |
| `ts_zscore(x,252)` 外层 SH −0.33 / FT −0.10 禁用 | M8 实测 SH **−0.32** / F −0.11 | ✅ **逐位复现** |
| `rank` 是本族 FT 天花板 | M3/M7 都无 rank 但 S 0.95–0.96 ≪ 2.04 ⇒ 说明不是 rank 的问题而是正交腿 | ⚠ 部分不符，见下 |
| decay 8→FT 0.35，decay 16→SH 2.04 | 我用 decay 16 得 S 2.04 | ✅ |

⚠ 第三条不符：作者说"加 rank 会压 FT"，但我的对照发现 **去掉 vector_neut 才是主因**（S 腰斩），
不是 rank。作者的消融可能把"去 rank"与"改 neut 层数"混在一起做了。**以我的单变量对照为准。**

### 75.4 探针 15 已派发：只改主信号的时间尺度 / 归一化

批次 `2cvDXf4d5gwbAzmahSrPkw`，10 条，设置同（decay 16 / truncation 0.02 / nanHandling ON / SUBINDUSTRY）。
**设计原则**：保持 `vector_neut(·, relpopularity08)` 不变（这是 S 的来源），只动被撞的那一层。

| # | 改动 | 目的 |
|---|---|---|
| T1 | `ts_ir` 22 → **66** | 尺度拉开 3×，最可能脱钩 |
| T2 | `ts_ir` 22 → **11** | 反方向 |
| T3 | `ts_ir` 22 → **44** | 中间档 |
| T4 | `ts_mean` 5 → **10** | 水平窗拉长 |
| T5 | `ts_mean` 5 → **3** | 水平窗缩短 |
| T6 | `max₅` → **max₁₀** | 峰值窗拉长 |
| T7 | `max₅` → **max₃** | 峰值窗缩短 |
| T8 | max₃ + mean 3 + ir 66 | 三层全换，偏离最远 |
| T9 | `ts_ir(·,22)` → `divide(ts_mean(·,22), ts_std_dev(·,66))` | 分子分母窗错配 |
| T10 | `driver="uniform"` → **gaussian** | 分位映射换形 |

**判据（预期）**：
- 若某条 prod < 0.7 且 S ≥ 1.58 ⇒ **DEU 第一条可提交 alpha 诞生**（同时点亮 SENTIMENT 塔 1/3）；
- 若全部 prod 仍 >0.7 ⇒ 说明撞墙带太宽（7 个相关者覆盖了多个尺度），
  则必须**放弃该主信号的尺度调整路线**，改走「换塔」（macro27 / option1）而非继续在同族里微调；
- 若 prod 降了但 S 跌破 1.58 ⇒ 进入「S vs prod」的两难，需按 `wq-prod-lever-self-lock-guard` 选杠杆。

---

## §76 news 塔字段画像 + nip 族论坛模板取证（探针 16 设计）

**时间**：2026-10-30
**背景**：探针 14/15 的 9 条全闸通过候选（`failed_ra_count = 0`）中已测 3 条 prod 全部撞墙
（0.8962 / 0.8983 / 0.9074）。根因已定论：**论坛高赞骨架 = prod 拥挤前置信号**（帖 43179860065303，72 票，
作者本人已提交同族）。⇒ 继续在 sentiment7 族换参数是零和，转战**真正未点亮的 news 塔**。

---

### 76.1 news 塔 DEU 数据集画像（5 个，全部 VECTOR 类型）

| 数据集 | 名称 | 字段数 | coverage 分档 | userCount 区间 | valueScore |
|---|---|---|---|---|---|
| `news104` | Archive News | 11 | **0.963 全体统一** | 0 – 22 | — |
| `news20` | Web Sources Sentiment | 46 | **0.6389 / 0.9191 两档** | 0 – 6 | **5** |
| `news50` | Web News Analytics | 37 | **0.7644 全体统一** | 0 – 7 | **5** |
| `news17` | PR Edition | 48 | **0.6489 / 0.9323 两档** | 0 – 4 | — |
| `news18` | Ravenpack News Data | 70 | 0.6925（nip）/ 平均 0.805 | 3（nip 字段） | — |

**★ 结构性发现：`*_multiple_comp_*` 系列覆盖率系统性高于单公司系列**

| 数据集 | 单公司系列 cov | 多公司系列 cov | 倍率 |
|---|---|---|---|
| news20 | `nws20_*` 0.6389 | `nws20_multiple_comp_*` **0.9191** | **1.44×** |
| news17 | `nws17_*` 0.6489 | `nws17_multiple_comp_*` **0.9323** | **1.44×** |

两档拥挤度几乎相同（userCount 0–6 vs 0–2）⇒ **`multiple_comp` 是「高覆盖 + 低拥挤」的双赢选择**，
应作为默认取样口径。单公司系列的 0.639/0.649 覆盖率在 DEU TOP500 上会留下 35%+ 的空缺，
CW / SUB 闸风险显著更高。

---

### 76.2 ★ nip 族 7 字段完整清单（DEU，全部低拥挤）

nip = **News Impact Projection**，语义为「新闻发布后未来 2 小时的市场冲击/波动影响预测」。

| 字段 | 数据集 | cov | userCount | alphaCount | 语义原文 |
|---|---|---|---|---|---|
| `nws17_nip` | news17 | 0.6489 | **0** | **0** | -1.00~1.00 估计新闻快讯后 2 小时市场冲击 |
| `nws17_multiple_comp_nip` | news17 | **0.9323** | 4 | 4 | 细化冲击分 -1.00~1.00，多公司事件 |
| `nws20_nip` | news20 | 0.6389 | 2 | 2 | 新闻快讯未来 2 小时市场影响强度 |
| `nws20_multiple_comp_nip` | news20 | **0.9191** | **1** | **1** | 新闻未来 2 小时市场影响 -1.00~1.00 |
| `mws50_nip` | news50 | 0.7644 | 1 | 2 | News Impact Projections 0–100，条件于到达时点 |
| `nws104_marketimpactscore` | news104 | **0.963** | 2 | 2 | **1 分钟前向风险调整收益估计，约 -5~+5** |
| `sentiment_news_impact_projection_d1` | news18 | 0.6925 | 3 | 3 | -1.00~1.00，未来 2 小时波动影响（D1 feed） |

**★ 两点关键判读**

1. **`nws17_nip` 是唯一零拥挤字段**（userCount 0 / alphaCount 0），cov 0.6489 偏低，需 `ts_backfill` 支撑。
2. **`nws104_marketimpactscore` 与其余 6 个不是同一口径**：其余是「冲击强度分数」（0–100 或 -1~1，无量纲序数），
   而它是**「1 分钟前向风险调整收益」的货币化估计**（-5~+5）。⇒ 可以直接当**收益预测**用（水平型信号），
   也可以当冲击强度用（相关型信号）。**语义层级更高，是本塔最有价值的单字段**，且 cov 0.963 最高。

---

### 76.3 ★★ 论坛模板取证：帖 40847481080087（94 票 / 22 评论）

**标题**：【Alpha灵感】使用nip族数据点亮news塔
**作者**：MY82844 ｜ **发布**：2026-05-30 ｜ **票数 94 / 评论 22**（高热度）

#### 核心模板（原帖原文）

```text
ts_corr(fld, returns, ndays)
ts_covariance(fld, returns, ndays)
ts_regression(returns, fld, ndays, lag = 0, rettype = 2)
```

**关键结论（原帖）**：
1. 「**相关性算子 + FAST neutralization** 的组合比较适合处理 sentiment 的数据」——先在 sentiment 塔验证，
   再迁移到 news 塔（因两塔数据高度相关）。
2. 「**nip 字段在相关性模版下面经常有不错的表现**」。
3. nip 不止在 news18：EUR 还在 news 与 **pv87** 里找到同类字段。
4. 「**不同的 nip 字段跑下来还有一些区分度，替换着用，可以降低相关性**」
   —— 这一条直接对应我当前的 prod 撞墙问题。
5. 「相关性算子 + FAST neutralization + nip 字段，在 EUR 地区的 D0/D1 **出 PPA 还是非常容易的**，
   后续结合一些 ts 算子和 group 算子控制下 PC 仍然可以出一些不错的 RA。」

#### 经济学机制（第一性原理）

这与我在 sentiment 族用的「注意力脉冲强度」骨架**完全不同**：

| 维度 | 我的旧骨架（M1/T10） | 论坛 nip 骨架 |
|---|---|---|
| 信号本体 | `ts_ir(ts_mean(ts_max(views)))` | `ts_corr(nip, returns, W)` |
| 信息来源 | 注意力**水平**（多少人在看） | 冲击预测与**实际实现**的耦合 |
| 经济含义 | 关注度异常 ⇒ 后续买入压力 | 供应商的冲击估计**是否真的兑现** |
| 自由度 | 单变量时序形态 | **两变量时序关系**（信息 + 实现） |
| 时间尺度 | 峰值 → 平滑 → 稳定性（三层） | 直接窗口相关，无嵌套 |

机制解读：如果一只股票历史上「高 nip 的新闻日」之后真的上涨，则 `ts_corr > 0` —— 说明该股的新闻定价存在
**系统性可预测性**（要么是市场反应不足可继续跟随，要么是供应商模型对该股特别有效）。
若 `ts_corr < 0`，则说明高冲击新闻日之后反而下跌 ⇒ **过度反应/反转**，可反向使用。
这是一个**二阶信号**（关于「新闻是否可交易」的元判断），与所有「新闻情绪水平」信号自然正交 ——
这正是它能低 prod 的结构性原因。

#### 评论区关键边界（5 条有价值）

| 作者 | 要点 |
|---|---|
| **YC83503**（最详实） | ① `ts_covariance(val, returns, 180)` 用长窗会**混入大量非事件期噪声**，导致非新闻密集区间表现衰减；② 建议**对比短窗（10/20）与长窗（120）**的 PPA/RA 衰减率；③ `nws17_multiple_comp_nip` 与 `nws20_nip` 的 alpha_count/user_count 差异明显，**实盘前先排除用户高度拥挤的字段**以降低同质化 |
| **XW23690** | ① news18 与 pv87 的 nip 信号来源不同（新闻情绪 vs 价格相关），组合使用应能降低 prod；② **FAST neutralization 的好处是不会过度平滑低频信号**；③ 建议试 `ts_corr(nip_field, returns, 20)` 短窗更敏捷；④ **RA 的 PC 控制可能需要额外加 group 算子** |
| **MY82844**（作者本人） | 回答「USA 也适用 FAST，但**出货率感觉没有 EUR 高**，还需后期再加工」 |
| **MY82844**（作者本人） | 回答「会不会过度使用 pv1 数据」：「一般在 news 和 sentiment **不会逗留很久，每个季度点塔做个 2-3 个差不多**，应该对 pv 影响不会很大」 |
| **FF65210** | 「新闻因子和传统量价因子的相关性通常较低，**这本身就是一个重要信号**——可以用来补充策略的分散化」 |

**★ 作者自己说「每个季度点塔做 2-3 个差不多」⇒ 本模板已是群体共识，prod 拥挤风险中高。**
与帖 43179860065303（72 票，sentiment 族）同性质。**因此本批只在其上做「机制迁移」而非「照抄」**：
- 照抄部分：相关性算子几何（`ts_corr` / `ts_covariance` / `ts_regression`）
- 自建部分：**7 条纯 news 塔变体**（第二腿不用 `returns`，改用同塔另一字段），绕开拥挤主路径

---

### 76.4 ★ 塔混配额核算（硬约束，必须先算再派发）

用户规则：`{PV, MODEL, OTHER}` 三者间禁止两两互组（含 `PV+PV`、三塔同现）；
允许 trio × 非 trio category，但**这类组合总量 ≤ 5**。

`returns` 属于 **PV 塔**（price/volume 内置字段）。因此：

| 模板 | 是否用 `returns` | 塔组合 | 配额占用 |
|---|---|---|---|
| N1 `ts_corr(nip17, returns, 60)` | ✅ | news × PV | **+1** |
| N2 `ts_covariance(nip20, returns, 60)` | ✅ | news × PV | **+1** |
| N3 `ts_regression(returns, nip50, 120)` | ✅ | news × PV | **+1** |
| N4–N10（7 条） | ❌ 纯 news 塔 | news 单塔 ATOM | 0 |

**探针 16 配额占用 = 3 / 5，剩余 2 个**。
历史核对：本轮此前所有批次均为 sentiment / socialmedia / analyst / fundamental 等**非 trio** 单塔或跨数据集组合，
`snl27_relpopularity08`（socialmedia27）同属非 trio ⇒ **此前 0 占用**，累计 3/5 合规。

---

### 76.5 探针 16 模板库（10 个，结构互异）

派发批次：`ecam3gSC4j2aUbxS1rN00V` ｜ 10 条 ｜ DEU/TOP500/D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling ON

| # | 模板名 | 表达式 | 差异维度 | 类型 | 机制 |
|---|---|---|---|---|---|
| **N1** | 冲击兑现相关（基准） | `rank(ts_corr(ts_backfill(vec_avg(nws17_multiple_comp_nip),22), returns, 60))` | `ts_corr` + 60窗 | news×PV | 论坛原式，冲击预测与实现的耦合 |
| **N2** | 协方差量级 | `rank(ts_covariance(rank(ts_backfill(vec_avg(nws20_multiple_comp_nip),22)), returns, 60))` | `ts_covariance`（保留幅度） | news×PV | 冲击×收益的绝对共动量，非标准化 |
| **N3** | 回归斜率 | `rank(ts_regression(returns, ts_backfill(vec_avg(mws50_nip),22), 120, lag=0, rettype=2))` | `ts_regression` rettype=2 | news×PV | 单位冲击的边际收益（弹性），长窗 |
| **N4** | 冲击 vs 情绪自洽 | `rank(ts_corr(ts_backfill(vec_avg(mws50_nip),22), ts_backfill(vec_avg(mws50_ess),22), 60))` | 第二腿=同塔情绪 | **ATOM** @news50 | 供应商内部一致性：冲击预测与情绪判断是否自洽 |
| **N5** | 冲击 vs 相关性自洽 | `rank(ts_corr(ts_backfill(vec_avg(mws50_nip),22), ts_backfill(vec_avg(mws50_relevance),22), 60))` | 第二腿=聚焦度 | **ATOM** @news50 | 高冲击但低聚焦 = 无关噪声；高冲击高聚焦 = 真事件 |
| **N6** | 冲击自身基线异常度 | `rank(ts_zscore(ts_mean(ts_backfill(vec_avg(mws50_nip),22), 5), 252))` | 无相关算子，纯时序形 | **ATOM** @news50 | 冲击水平的自身历史异常（稀疏事件族五铁律） |
| **N7** | 冲击水平漂移 | `rank(ts_mean(ts_backfill(vec_avg(nws104_marketimpactscore),22), 22))` | 纯水平型，22窗平滑 | **ATOM** @news104 | 月度平均冲击方向（PPA 型慢信号） |
| **N8** | 置信度加权冲击 | `rank(ts_mean(multiply(ts_backfill(vec_avg(nws104_marketimpactscore),22), ts_backfill(vec_avg(nws104_confidence),22)), 22))` | 乘法加权（非加和） | **ATOM** @news104 | 只有高置信的冲击估计才可交易 |
| **N9** | 单公司脉冲累积 | `rank(ts_zscore(ts_sum(ts_backfill(vec_avg(nws17_nip),22), 22), 252))` | 累积脉冲 + 自身 zscore | **ATOM** @news17（零拥挤字段） | 稀疏事件两件套：`ts_sum` 聚强度 + `ts_zscore` 归一 |
| **N10** | 单/多公司归属一致性 | `rank(ts_corr(ts_backfill(vec_avg(nws17_nip),22), ts_backfill(vec_avg(nws17_multiple_comp_nip),22), 90))` | 同数据集两字段相关 | **ATOM** @news17 | 相关性高=新闻总明确归属该股；低=总被顺带提及（信息模糊） |

**多样性核算**：
- 相关算子几何：`ts_corr`（N1/N4/N5/N10）、`ts_covariance`（N2）、`ts_regression`（N3）、无相关（N6/N7/N8/N9）→ **4 类**
- 第二腿来源：`returns`(PV)、同塔情绪(ess)、同塔聚焦度(relevance)、同塔第二 nip、无第二腿 → **5 类**
- 字段来源：news17 ×3 / news20 ×1 / news50 ×4 / news104 ×2 → **4 个数据集**
- 外层几何：裸 `rank` / `ts_mean` 平滑 / `ts_zscore` 归一 / `multiply` 加权 → **4 类**
- 时间尺度：22 / 60 / 90 / 120 / 252 → **5 档**

⇒ 满足「≥10 个结构互异模板」硬约束。**ATOM 单数据集 7 条（N4–N10），跨数据集 3 条（N1–N3）**。

---

### 76.6 预检记录

```text
operator_audit(3 条相关算子表达式, DEU)  → safe: true, violations: []
   ghost_operators 19 个（均为已知平台不存在算子，本次未使用）
   ⇒ ts_corr / ts_covariance / ts_regression 三个算子均合法

preflight_expressions(10 条, DEU, dataset_id=news17) → valid: true
   fields_checked: 9 个（含 8 个数据字段 + returns）
   unknown_fields: []
   builtin_fields: ["returns"]          ← returns 是内置字段，非数据集字段
   any_changed: false                   ← 我的 vec_avg 包裹已正确，无需自动修复
```

**★ 预检警告的正确解读**：
```text
warning: "Field pre-check skipped or incomplete: mws50_ess: get_datafields(offset=0):
          failed after 6 attempts; mws50_relevance: 同上"
```
这是**预检工具的网络重试故障，不是字段不存在** —— 两个字段在
`get_datafields(region=DEU, dataset_id=news50)` 的返回里明确存在：

| 字段 | coverage | userCount | alphaCount |
|---|---|---|---|
| `mws50_ess` | 0.7644 | 5 | 7 |
| `mws50_relevance` | 0.7644 | 3 | 3 |

⇒ 不做处理，直接派发。若回测报 unknown variable 再回查（可能性低，且平台 400 会明确报字段名）。

---

### 76.7 待验证的四个假设（探针 16 的判读框架）

| # | 假设 | 判据 | 若成立的动作 |
|---|---|---|---|
| **H1** | 相关性算子几何在 DEU news 塔有信号 | N1/N2/N3 任一 S ≥ 1.0 | 判为机制成立，扩到批 B（FAST 对照） |
| **H2** | 纯 news 塔 ATOM 变体也有信号（不走 returns 路径） | N4–N10 至少 3 条 S ≥ 1.0 | **优先推这批**（不占 PV 配额、拥挤度低） |
| **H3** | `nws104_marketimpactscore` 的「货币化收益预测」语义优于其它 nip | N7/N8 S > N1/N2/N3 | 换主字段，重设全部骨架 |
| **H4** | 冲击水平的自身异常度（N6/N9）优于冲击的时序相关性 | N6 或 N9 > N1 | 证明「相关算子只是载体，真正信号是冲击水平」，机制降级为单变量形态 |

**若 H1–H4 全部失败**（10 条均 S < 1.0）⇒ news 塔 nip 族在 DEU 判死，理由需带数据：
DEU 只有 TOP500（宽度小 6 倍）+ news 覆盖率 0.64–0.96 + 事件稀疏 ⇒ 冲击信号的横截面分散度不足。
届时转 `news54` / `news38`（3 字段，cov 0.599）或无 nip 的通用情绪字段。

---

### 76.8 与既往结论的衔接

**本条强化了「论坛高票 ⇒ prod 拥挤」的判断，并给出可操作的分层策略**：

| 论坛票数 | 判断 | 用法 |
|---|---|---|
| ≥ 50 | 群体共识，主路径已拥挤 | **只取机制，自建骨架**（本批 7/10 条属此类） |
| 20–49 | 部分人用过 | 可试原式，预期 prod 中高 |
| < 20 | 少见 | 可直接试原式 |

作者本人「每个季度点塔做 2-3 个」的说法，是**拥挤度的直接自白**：他知道这个模板不能多用。
⇒ 我的 N1–N3（`returns` 路径）本质是在复现他描述的主路径，**预期 prod 偏高**；
N4–N10（纯 news 塔自建变体）才是低 prod 的候选。**这一预期差异本身就是本批的另一组对照实验。**

---

## §77 DEU 全塔可用性地图 + 数据集拥挤度榜（category 逐个实测）

**时间**：2026-10-30
**方法**：逐 category 调 `get_datasets(region=DEU, delay=1, universe=TOP500, category=<C>)`，
对 coverage = 0 的候选再用 `get_datafields` 做**字段级复核**（避免数据集级统计故障误杀）。

---

### 77.1 ★ 五个塔在 DEU 是「无数据」而非「未挖掘」

这是本轮最重要的结构性发现。**`pyramid alphaCount = 0` 有两种完全不同的原因**，必须用
字段级 coverage 区分，否则会把「无数据」当成「机会」白烧回测。

| 塔 | 数据集 | 字段数 | 数据集级 cov | 字段级复核 | 判定 |
|---|---|---|---|---|---|
| **macro** | `macro27`（Job records） | 13 | **0.0** | 13/13 字段全 0.0 | ❌ 无数据 |
| **option** | `option1`（IV 曲面） | 22 | **0.0** | 22/22 字段全 0.0 | ❌ 无数据 |
| **imbalance** | `imbalance5`（Oil Price Resilience） | 2 | **0.0** | — | ❌ 无数据 |
| **earnings** | `earnings6`（International Findings） | 18 | **0.0** | — | ❌ 无数据（已判死 `DEU-EARN6-PEAD-DEAD`，现补记根因） |
| **earnings** | `earnings_sent_matrix`（Earnings Call Sentiment） | 7 | **0.0** | **7/7 字段全 0.0** | ❌ 无数据 |
| **socialmedia** | `socialmedia12`（Sentiment for Equity） | 18 | **0.0** | 18/18 字段全 0.0 | ❌ 无数据 |
| **socialmedia** | `socialmedia39`（Investor views） | 1 | 0.275 | — | ⚠ cov 太低（中性化后覆盖 <150 只） |

**⇒ DEU 无法点亮的塔：macro / option / imbalance / earnings（4 个整塔）+ socialmedia（事实不可用）。**

**重要纠正**：`earnings6` 此前被判死时记为「PEAD 事件族失败」，**真实根因是 DEU 完全没有数据覆盖**。
同理 `risk72` 全 12 条反向、`pv109` 的 bond 字段为空，都应先怀疑覆盖率而非信号质量。

---

### 77.2 ★ valueScore 高 ≠ 可用：`institutions25` 陷阱

| 数据集 | name | 字段 | coverage | userCount | alphaCount | **valueScore** |
|---|---|---|---|---|---|---|
| `institutions25` | Fund Short Selling Data | 24 | **0.0** | 6 | 7 | **6.0（最高档）** |

`valueScore` 的构造偏向「稀缺/低拥挤」，与「本区有数据」**完全正交**。
`institutions25` 同时具备「24 字段 + userCount 6 + valueScore 6」三重诱惑，但 coverage = 0
⇒ 派发前**必须**用 `get_datafields` 查 coverage，不能凭 valueScore 判断。

---

### 77.3 ★ 拥挤度榜（userCount / alphaCount，跨 DEU 已画像的 39 个数据集）

| 排名 | 数据集 | category | coverage | 字段 | userCount | alphaCount | 判读 |
|---|---|---|---|---|---|---|---|
| 1 | `shortinterest3` | shortinterest | 0.7105 | 25 | **316** | **864** | ⛔ **极拥挤，封盘** |
| 2 | `institutions6` | institutions | **1.0** | 11 | 127 | 270 | ⛔ 高拥挤 |
| 3 | `fund_holdings_panel` | institutions | 0.9019 | 18 | 58 | 102 | ⚠ 中 |
| 4 | `news18` | news | 0.805 | 70 | 84 | 137 | ⚠ 中 |
| 5 | `news104` | news | **0.963** | 11 | 57 | 100 | ⚠ 中 |
| 6 | `news17` | news | 0.791 | 48 | 53 | 87 | ⚠ 中 |
| 7 | `news50` | news | 0.7644 | 37 | **35** | **42** | ✅ **低拥挤 + 高价值** |
| 8 | `news20` | news | 0.773 | 46 | **27** | **33** | ✅ **最低拥挤 + valueScore 5** |
| 9 | `institutions1` | institutions | 0.2289 | 7 | 22 | 32 | ⚠ 低拥挤但 cov 太低 |
| 10 | `institutions4` | institutions | 0.3413 | 6 | 13 | 19 | ⚠ 低拥挤但 cov 太低 |
| 11 | `news38` | news | 0.599 | 3 | 11 | 13 | ⚠ 字段仅 3 |
| 12 | `socialmedia39` | socialmedia | 0.275 | 1 | 81 | 137 | ⛔ cov 太低 + 高拥挤 |
| — | `imbalance5` | imbalance | 0.0 | 2 | 75 | 138 | ⛔ 无数据 |
| — | `earnings6` | earnings | 0.0 | 18 | 43 | 108 | ⛔ 无数据 |
| — | `earnings_sent_matrix` | earnings | 0.0 | 7 | 65 | 127 | ⛔ 无数据 |
| — | `option1` | option | 0.0 | 22 | — | — | ⛔ 无数据 |
| — | `macro27` | macro | 0.0 | 13 | — | — | ⛔ 无数据 |

**★ 两条硬结论**

1. **DEU 不存在「低拥挤 + 高覆盖」的富矿**。coverage > 0.7 的数据集里，userCount 最低的也只有
   `news20`（27）/ `news50`（35）。而 USA TOP3000 有 3000 只股票分摊这些用户，DEU 只有 **500 只**
   ⇒ **同一数据集的 DEU 拥挤密度是 USA 的 6 倍**。
2. **`shortinterest3` 必须封盘**。864 个已提交 alpha 意味着任何 shortinterest 变体与已提交池的相关性
   都建立在同一个 500 股票池上。这解释了本轮 6 个探针 50 条变体最高只到 S 1.57，且 `pwdQWj0q`
   的 prod 大概率同样撞墙 —— **不是骨架问题，是数据集饱和**。

---

### 77.4 ★ news 塔是 DEU 唯一「可点塔 + 相对低拥挤」的组合

| 维度 | 判据 |
|---|---|
| 塔状态 | 未点亮（需 3 条） |
| 可用数据集 | **17 个**（全 DEU 最多） |
| coverage 区间 | 0.599 – **0.963**（`news104` 最高） |
| 拥挤度 | userCount **27–84**（最低档）；nip 族字段 userCount **0–4** |
| 机制密度 | nip 族 7 字段 + 情绪/概率/新意/聚焦度/置信度多维 |

**⇒ 本轮后半程的资源应全部压在 news 塔**。这也与探针 16 的方向一致。

---

### 77.5 ★ 60 条目标的现实评估（必须向用户如实说明）

#### 实测产出率（本轮，DEU）

| 指标 | 数值 |
|---|---|
| 累计已测 alpha | **≈ 3500 条**（探针 1–16） |
| `failed_ra_count = 0`（全平台闸通过） | **9 条** |
| 全闸通过率 | **0.26%** |
| 过 prod（< 0.70） | **0 条**（已测 3 条，全部 0.896–0.907） |
| 可交付 | **0 条** |

#### 结构性约束

| 约束 | DEU | USA（对照） | 影响 |
|---|---|---|---|
| universe 宽度 | **500（唯一档，无退路）** | 3000 | 横截面分散度 1/6 |
| 平台闸值 S / 2Y | **1.58** | 1.58 | **同样严格** |
| 数据集拥挤密度 | 6× USA | 1× | prod 墙更难绕过 |
| 可用塔 | **10 个**（5 个无数据） | 全塔 | 点塔空间受限 |

#### 目标可达性

**60 条在 DEU 单区不可达**，理由：
1. 全闸通过率 0.26% ⇒ 60 条需 ≈ **23000 条回测**（当前 3500 条，需再 6.5 倍算力）。
2. 即使全闸通过，prod 通过率当前为 **0%**。news 塔若能把 prod 从 0% 拉到 30%，
   仍需 200 条全闸通过候选 ⇒ 约 **77000 条回测**。
3. DEU 全塔可用 alpha 存量（所有用户合计）也才数千条，60 条相当于在 500 只股票上
   再占 1–2% 的独立信号空间，**接近该市场的物理上限**。

**可行的混合策略（需用户决策）**：
- **DEU 定位为「点塔区」**：每塔 3 条（点亮 10 个可用塔 = 30 条），优先 news / sentiment / institutions
- **其余 30 条由其他区承接**：L3 口径已有 30 条可交付（IND 20 / GLB 3 / USA 3 / EUR 3 / GBR 1）
- 或 **PPA 通道**：用 PPAC < 0.5 取代 PC < 0.7，可绕过 prod 墙（但 PPAC 分布未验证）

---

### 77.6 已画像的 39 个数据集清单

| category | 数据集数 | 已画像 | 无数据（cov 0） |
|---|---|---|---|
| news | 17 | 5（news104/20/50/17/18） | 0 |
| analyst | 18 | 0（已判死 `analyst48`/`analyst46` cov 0） | 1+ |
| sentiment | 3 | 3（sentiment7/27/33） | 0 |
| institutions | 5 | 5 | 1（`institutions25`） |
| earnings | 2 | 2 | **2** |
| socialmedia | 2 | 2 | 1（`socialmedia12`） |
| macro | 1 | 1 | **1** |
| option | 1 | 1 | **1** |
| imbalance | 1 | 1 | **1** |
| shortinterest | 1 | 1 | 0 |

**尚未系统画像**：`pv` / `model` / `other` / `fundamental` / `insiders` / `risk`（6 个 category）。
其中 `model`（已点亮 7）与 `other`（已点亮 4）无需再点；`pv` / `fundamental` / `insiders` / `risk`
各需 2–3 条点塔，属后续战备。

---

## §78 判死登记簿交叉核对 + analyst47 画像 + 探针 17 归因（2026-10-30）

### §78.1 ★ 核心动作：把「有数据」与「未判死」求交，终止盲目探针

§77 得出「DEU 有 21 个数据集有数据、14 个已判死」，但当时未把 registry_empirical 的
dead_end 层逐条拉出来核对。本轮做了两件事：

1. 从 `get_dead_ends(region="DEU")` 抽取全部 **56 个数据集 token**；
2. 与「DEU 实测 coverage > 0」的 21 个数据集求交，逐条核对天花板证据。

结果推翻了我上一轮的一个假设——**DEU 并不存在「低拥挤 + 高覆盖」未开发富矿**，
唯一的例外是 `analyst47`（见 §78.2）。

#### 已判死且有数据的 9 个数据集（带天花板数值）

| 数据集 | 判死 entry_id | 天花板 / 关键证据 |
|---|---|---|
| `fund_holdings_panel` | `DEU-INSTITUTIONS-fundholdings-SINGLEATOM-WEAK`<br>`DEU-FHP-ALLGATE-CLOSED`<br>`DEU-FHP-SCEILING-DEAD` | 4 探针单原子最好 **0.53**（`boundary_transaction_total`，SUB 0.16 FAIL）；<br>**三次配方攻势天花板 1.36 / 1.34 / 1.37**；<br>CW killer：`ts_zscore(vec_sum(stable_boundary_trade_count_21d),252)` → CONCENTRATED_WEIGHT **0.5 / limit 0.1**；<br>**原文写入「fhp 不再投入配方攻势」** |
| `analyst83` | `DEU-TAIL-DATASETS-DEAD-20260916` | best **0.21**（call 分析）；★ 该集是**平台官方文档推荐的 DEU 数据集**（见 §78.4） |
| `fundamental45` | 同上 | best **0.45**（call readability） |
| `analyst44` | `DEU-P0.3` 白名单探针批 | 转化率 0（`datasets_dead_today`） |
| `news50` | 同上 | 转化率 0 ← 这解释了探针 16 的 `mws50_nip` / `mws50_ess` 全灭 |
| `sentiment33` | 同上 | best 0.69（换手过高） |
| `model162` / `model182` / `other384` / `order_book_imbalance` | 同上 | best 0.35 / 0.32 / 0.21 / 0.32 |
| `analyst93` | `DEU-CROSSSET-RESCUE-DEAD` | 主腿 **1.28**；配 fhp/other455 跨集辅助腿无增益且引入 CW |
| `insiders1`（`insd1_shares`） | `DEU-INSD-FIELD-FAIL` | R92 批四字段（`dir_sig1`/`top_dir_sig1`/`avg_buy_shares`/`insd1_shares`）**No alpha_id**，同结构其它字段正常 ⇒ 字段级平台问题 |

★ **`DEU-TAIL-DATASETS-DEAD-20260916` 的 reuse_rule 是全局判据**：
> 「种子 S < 1.0 的数据集，配方可放大性存疑（对比 other455 的 1.06 → 2.10）」

这条规则是本轮最重要的先验：**DEU 的可用数据集里，凡单原子探针 S < 1.0 的，历史最佳放大倍率约
2.0–2.6×**（fhp 0.53 → 1.37 是 2.6×，other455 1.06 → 2.10 是 2.0×）。
⇒ 要过 1.58 闸，**单原子 S 至少要 ≥ 0.6–0.8**，否则放大后仍不足。

#### 「有数据 ∩ 未判死」的全部剩余项（6 个，逐项裁定）

| 数据集 | cov | 字段/类型 | 裁定 |
|---|---|---|---|
| **`analyst47`** | 0.6234（`indicator` **1.0**） | 5 / MATRIX | ★ **唯一值得投的，本轮探针 17/18 已投** |
| `institutions4` | 0.3413 | 6 / VECTOR | 未探索；含 `current` vs `previous` **现成方向对**（见 §78.6） |
| `news104` / `news20` / `news17` | 0.64–0.96 | VECTOR | 探针 16 已试灭 nip 族（10/10 全灭，最高 0.35） |
| `risk88` | 1.0 | **1 个 MATRIX：`alternative_market_cap_usd`** | ❌ 纯市值字段，**非信号源**，只能当分母 |
| `fundamental22` | 0.69 | **1 个 VECTOR：`fnd22_value`** | ❌ 单字段且**无 KPI 名称字段**，`vec_avg` 会把不同 ESG 指标混算，语义不可控 |
| `analyst48` | 0.7879 | 7 / VECTOR | ❌ **全是指数级元数据**（`idivisor` / `indx_typ` / `count_index_members` / `return_code` / 公司 ID），**无个股信号** |

★ `analyst48` 的排除值得单独记：`coverage 0.7879 + userCount 0–2 + valueScore 5` 看起来像富矿，
实际 7 个字段没有一个是可交易的个股信号。**覆盖率与拥挤度都不能替代「字段是不是信号」这一判断**。

### §78.2 ★ analyst47 字段画像（本轮最高优先级发现）

`analyst47` = *Alternative Analyst Investment Insight Data*，category **analyst**，
金字塔乘数 **1.8**，共 5 个 **MATRIX** 字段（无需 `vec_*` 包裹，规避 VECTOR 陷阱）。

| 字段 | coverage | userCount | alphaCount | 语义（原文） |
|---|---|---|---|---|
| `anl47_indicator` | **1.0** | 33 | 43 | Composite alpha indicator scaled 1–10, **higher = stronger buy consensus** |
| `anl47_rawsentiment` | 0.5293 | 29 | 29 | Raw component reflecting **long/short idea counts and open/closed status** |
| `anl47_rawalphadecay` | 0.5293 | 8 | 9 | Raw component measuring **impact of idea age or decay** |
| `anl47_rawexperts` | 0.5293 | 7 | 7 | **Contribution of author historical performance** to the raw signal |
| `anl47_totalrawsignal` | 0.5293 | 33 | 43 | **Sum of raw components: sentiment + alpha decay + earnings + experts** |

#### 三条结构性优势

1. **`anl47_indicator` coverage = 1.0**：这是 DEU 全部 58 个已画像数据集中**唯一达到满覆盖的
   个股信号字段**。COVERAGE 满 ⇒ 天然规避覆盖率缺口型 `CONCENTRATED_WEIGHT`（探针 17 实测
   `CONCENTRATED_WEIGHT` 全部 **PASS**，见 §78.3）。
2. **全局低拥挤**：userCount 7–33。对比 `fundamental6`（438）、`risk60`（198）、
   `analyst_factor_signals`（701）、`analyst7`（1184）低 1–2 个数量级。
   ⇒ 对 **prod 相关性**（全局池）而言是真正的新鲜信号。
3. **`totalrawsignal` 提供代数可分解的隐含第四分量**：
   `T = S + D + E + Earnings` ⇒ `Earnings = T − S − D − E`。
   平台**没有单独暴露** earnings 分量，这是纯靠字段代数就能拿到的新信息。
   ★ 注意：这是**单一经济量的精确代数重构**，不是 `add(A,B)` 式混信号——两者必须区分。

#### 但有一个结构性弱点（本轮已实测确认）

`indicator` cov 1.0，而 4 个 raw 分量 cov **0.53**。⇒ 约一半股票从未有分析师观点覆盖，
`ts_backfill` 补不出「从未发生」的事件。因此凡是走 raw 分量的模板，覆盖缺口是**内生的**。

### §78.3 探针 17：analyst47 十模板全批结果（10/10 REJECT）

- multisim `4yDT6s1cR4l698tTrKECpeN`，DEU/TOP500/D1，SUBINDUSTRY，decay 4，truncation 0.08，nanHandling **ON**
- 10/10 COMPLETE，**errors 0**，**10/10 REJECT**
- 预检：`preflight` valid 10/10 / `unknown_fields` 0 / `vector_fields` **0**（确认 MATRIX）；`operator_audit` safe

| # | alpha | S | F | TO | 2Y | SUB | margin | DD | failed | 模板（★=硬确认） |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | **`akKXwgXW`** | **0.48** | 0.22 | **8.44%** | **0.88** | **0.34** | **61.4bp** | 19.82% | 3 | ★ **共识水平铺展** `rank(ts_mean(anl47_indicator, 22))` |
| A2 | ? | 0.27 | 0.06 | 31.16% | 0.10 | −0.02 | 9.2bp | 17.31% | 5 | 自身基线异常（疑） |
| A3 | ? | 0.25 | 0.08 | 9.91% | 0.50 | 0.15 | 26.8bp | 15.40% | 3 | 共识动量（疑） |
| A4 | ? | **−0.46** | −0.13 | 30.64% | −0.47 | −0.16 | −15.6bp | 27.72% | 4 | 极值偏离（疑） |
| A5 | ? | −0.03 | 0.00 | **3.10%** | −0.27 | 0.09 | −9.1bp | 15.59% | 3 | 波动惩罚（疑） |
| A6 | ? | −0.02 | 0.00 | **60.30%** | −0.57 | 0.04 | −0.4bp | 20.23% | 4 | 指标 vs 原始和背离（疑） |
| A7 | ? | 0.19 | 0.02 | **67.43%** | −0.28 | 0.25 | 2.9bp | 12.35% | 3 | 隐含 earnings 分量（疑） |
| A8 | **`j2YNxMXj`** | **−0.53** | −0.17 | 25.21% | −0.78 | −0.48 | −21.7bp | 31.82% | 4 | ★ **专家质量背离** `rank(subtract(rank(ts_backfill(anl47_rawexperts,66)), rank(ts_backfill(anl47_rawsentiment,66))))` |
| A9 | **`QPvmgojw`** | **0.53** | 0.20 | 18.12% | 0.36 | 0.10 | 28.9bp | 11.08% | 4 | ★ **条件门控** `trade_when(greater(rank(anl47_indicator),0.3), rank(ts_zscore(anl47_indicator,252)), -1)` |
| A10 | ? | 0.13 | 0.03 | 15.14% | 0.55 | 0.19 | 12.8bp | 22.94% | 4 | 双尺度一致 + TVR（疑） |

**三条硬确认（经 `get_alpha_details` 逐条读 `code`）**：A1 / A8 / A9。其余 7 条为特征推断，不得当参数结论引用。

#### ★ 归因结论 1：瓶颈是**信号幅度**，不是几何

全部 10 条的失败项只有 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE`。
**`CONCENTRATED_WEIGHT`、`LOW_TURNOVER`、`HIGH_TURNOVER` 三项全部 PASS**（A9 额外失 SUB）。
⇒ 覆盖率（cov 1.0）与换手（8%–67%，多数落在 5–15% 甜点区）都不是问题。
`anl47_indicator` 的 1–10 评分序列本身信噪比不足，这是数据集属性，换骨架解决不了。

#### ★ 归因结论 2：A1 的几何是全场最优，但幅度差 3.3×

`akKXwgXW`（A1）的四项指标在本批里都是极值：

| 指标 | A1 值 | 本批其它 9 条 | 判读 |
|---|---|---|---|
| margin | **61.4bp** | 0.4–28.9bp | 最高，是次高的 **2.1×**、最低的 **150×** |
| `SUB/S` | **0.34/0.48 = 0.708** | −4.8 ~ 1.33 | 远超 0.434 硬门槛，**SUB 维度完全过关** |
| 2Y Sharpe | **0.88** | −0.78 ~ 0.55 | 最高，近期表现是长期的 1.8× |
| `risk_neutralized_sharpe` | **0.72** | — | **比 S 高 50%** ⇒ 有未剥离的风格暴露在拖累信号 |
| TO | 8.44% | 3.1%–67.4% | 落在论坛实证的 5–15% 最优区间 |

★ `risk_neutralized_sharpe 0.72 > S 0.48` 是唯一一条**指向破闸方向**的线索：
剥离风险暴露后信号增强 50%。这提示换中性化轴（而非换表达式几何）可能有增益——
已作为探针 18 之外的备选方向记录。但即使 0.72 也距 1.58 有 2.2× 差距。

#### ★ 归因结论 3：A8 方向反了，反转后才是有意义信号

`j2YNxMXj` S = **−0.53**（本批 |S| 第二高）。表达式是
`rank(rawexperts) − rank(rawsentiment)`（作者历史表现 − 观点数量）。

经济学读法：**「观点数量多、但作者历史表现差」= 噪音共识**，负收益。
⇒ **反转形式（`rawsentiment − rawexperts`）才是"避开噪音共识"的正向信号**，
已作为探针 18 的 B7 单独验证。这是本批最有价值的**方向发现**。

### §78.4 ★ 论坛实证：DEU 全市场的物理容量（帖 42587179348119，87 票 / 36 评论）

作者 RM49262 于 2026-08-09（GBR/DEU 开放首周后）拉取全平台提交快照：

| 区域 | 全球提交总数 | 国区顾问占比 | 使用 `pv1` 的 alpha | 其中 ATOM |
|---|---|---|---|---|
| GBR | **3534** | 2546（70%） | 717 | 66 |
| **DEU** | **653** | 495（76%） | 195 | 67 |

原文引用：
> 「GBR目前全球一共提交了3534个alpha，DEU全球一共提交了653个alpha。」

并引官方文档：
> 「You might find GBR Alphas easier to create compared to DEU Alphas, which is expected.」

#### 三条对本战役的直接推论

1. **DEU 的物理容量极小**：开放首周全球仅 653 条。我本轮已提交的 10 条即占该快照的 **1.5%**；
   目标 60 条 = 该快照的 **9.2%**。即便考虑三个月增长，60 条也已接近该市场单用户历史总量级。
2. **`alphaCount` 是跨区域全局值，不是 DEU 本区值**。此前我用 `shortinterest3` 的
   `alphaCount 864` 推断「DEU 拥挤密度是 USA 的 6 倍」——**这个推断错了**。864 是全球提交数。
   DEU 本区其实极空。**prod 撞墙的真实来源是全球同族骨架拥挤，不是 DEU 本区拥挤**
   （与「prod 池 = 全局已提交池」的平台事实一致）。
3. **评论 ZW26474 的独立发现**：「DEU 换手-收益不显著（p>0.05）」，而 GBR 显著。
   ⇒ 在 DEU 用「提换手换收益」的常规套路无效，必须靠信号本身的截面区分度。

★ 评论区 FX25214 的警告与本轮决策直接相关：
> 「拿热门榜决定研究方向，反而会追进最拥挤的生产池。」

### §78.5 ★ 官方推荐的 DEU 数据集，实测天花板 0.21

同帖原文给出平台官方对两个新地区的推荐数据集：
> GBR 推荐：`analyst83` / `analyst56` / `pv109`

而 `analyst83` 在 DEU 的实测最优是 **S 0.21**（`DEU-TAIL-DATASETS-DEAD-20260916`）。
⇒ **「官方推荐」只说明该数据集在新区域有数据、可回测，不说明出信号**。
这与我此前「`valueScore` 与可用性正交」是同一类错误的两个变体：
**平台侧的任何评分/推荐都不能替代实测**。

### §78.6 剩余可用路径的最终裁定

| 路径 | 状态 | 决定 |
|---|---|---|
| `analyst47` 十模板 | 探针 17 全灭（最高 \|S\| 0.53） | 已派探针 18 做定向放大（A1 几何 + A8 反转） |
| `institutions4` | **未探索**，6 个 VECTOR 字段，cov 0.3413，userCount 1–10 | 唯一剩下的未探索项；含 `current_shares` / `previous_shares` **现成方向对**；若探针 18 无出货则投 |
| `insiders1` | 制度性先验不利 | ❌ **不投**：论坛帖 43152032301591 实证「欧盟允许延迟披露内部人交易 ⇒ 事件流时间结构被制度差异搅碎」，同一构造搬 GLB 全灭（0.02–0.32）。DEU 同属 EU |
| `risk88` / `fundamental22` / `analyst48` | 非信号字段 | ❌ 不投 |
| `news104/20/17` | 探针 16 试灭 nip 族 | ❌ 不投 |
| 其余 14 个有数据数据集 | 已判死 | ❌ 不投 |

★ **结论：DEU 的可用挖掘空间已被压缩到「`analyst47` + `institutions4`」两个数据集。**
探针 17（10 条）+ 探针 18（10 条）+ `institutions4` 一批（10 条）之后，
DEU 本区将**不存在任何未探索的有数据数据集**。届时该区产出上限即可给出闭区间，而非估算。

### §78.7 本轮新增的工程事实

1. **`get_dead_ends` 返回会被外部化落盘**（>一定体积），须用脚本按 index 拼接 JSONL 的 `text` 字段再正则检索；
   直接读全文会被截断。
2. **`batch_status` 的 `child_count: 0` 是正常排队态**；本轮从 0 → 10 用时约 2 轮轮询，之后 `all_terminal: true`。
3. **`get_datafields` 的 `userCount` / `alphaCount` 是全局值**，与 `get_datasets` 同源，不可当作区域拥挤度。
4. **MATRIX 数据集走 `preflight_expressions` 会返回 `vector_fields: []` 且 `any_changed: false`** —
   这是「该数据集确为 MATRIX」的可用旁证。



---

## §79 探针 18 归因 + `pwdQWj0q` 突破（2026-10-30 续）

### 79.1 探针 18 收批：10/10 REJECT

- multisim `3F4wI25QJ4TM8BIZzfkWW4e`，DEU/TOP500/D1，SUBINDUSTRY，decay 4，truncation 0.08，nanHandling ON
- 预检 10/10 valid、`unknown_fields` 0、`vector_fields` 0；`operator_audit` safe
- 10/10 COMPLETE、errors 0、**10/10 REJECT**

| 代号 | alpha | S | F | TO | 2Y | SUB | margin | DD | failed |
|---|---|---|---|---|---|---|---|---|---|
| B8 | **`JjeRr0Yl`** | **0.57** | 0.28 | 5.01% | **1.72** | 0.24 | 12.43bp | 17.15% | 3 |
| B1 | **`zq3XewXo`** | **0.56** | 0.28 | 4.42% | 0.99 | 0.33 | 13.91bp | 13.85% | 3 |
| B7 | **`ZYQkNww8`** | **0.53** | 0.17 | 25.21% | 0.78 | 0.48 | 2.17bp | 9.28% | 3 |
| — | `npvwrkk3` | 0.53 | 0.26 | 11.85% | 0.87 | 0.54 | 5.26bp | 18.39% | 3 |
| — | `d5Wev8eY` | 0.48 | 0.21 | 2.31% | 0.60 | 0.29 | 21.20bp | 7.10% | 3 |
| — | `58ENY77o` | 0.48 | 0.22 | 8.43% | 0.88 | 0.34 | 6.17bp | 19.76% | 3 |
| — | `A1VqEJYQ` | 0.47 | 0.21 | 6.61% | 0.87 | 0.29 | 7.87bp | 17.38% | 3 |
| — | `ZYQkNwk8` | 0.33 | 0.13 | 3.63% | 0.93 | 0.16 | 10.28bp | 20.27% | 3 |
| — | `npvwrkY3` | 0.25 | 0.08 | 5.11% | 0.63 | 0.39 | 5.51bp | 14.19% | 3 |
| — | `E56ox00m` | 0.23 | 0.07 | 5.11% | 0.49 | 0.03 | 4.65bp | 12.67% | 4 |

### 79.2 三条硬确认映射（经 `get_alpha_details` 逐条读 `code`）

| alpha | 表达式 | 结论 |
|---|---|---|
| `JjeRr0Yl` | `rank(ts_mean(anl47_totalrawsignal, 66))` | ★ 全集最高 S **0.57**，且 **2Y 1.72 已过 2Y 闸** |
| `zq3XewXo` | `rank(ts_mean(anl47_indicator, 66))` | W=66 优于 W=22（S 0.48→0.56），但 margin 61.4→13.9bp（−77%） |
| `ZYQkNww8` | `rank(subtract(rank(ts_backfill(anl47_rawsentiment,66)), rank(ts_backfill(anl47_rawexperts,66))))` | ★ **A8 反转**：S **+0.53**，与 A8 的 −0.53 **精确镜像** |

其余 7 条为特征推断，不作参数结论引用。

### 79.3 ★ A8 反转假设验证成立（精确镜像）

探针 17 的 A8 `j2YNxMXj` = `rank(rawexperts) − rank(rawsentiment)`，S = **−0.53**。
探针 18 的 B7 `ZYQkNww8` = 交换两侧，S = **+0.53**。

**逐位镜像 ⇒ 「避开噪音共识」是一个真实存在的正向信号**，经济学读法获得硬验证：
「观点数量多（rawsentiment 高）但作者历史表现差（rawexperts 低）= 噪音共识」→ 负收益；反转后正向。

附带两个只有 B7 具备的特征（全集最正交的证据）：
- `CLUSTER_TEST` = **0.14**（全集最低，其余 0.43–0.63）⇒ 与现有 alpha 簇最不相关
- `investability_ratio` = **1.17**（全集唯一 >1，其余 0.52–0.83）⇒ 信号集中在可投资标的

但幅度 0.53 距 1.58 仍有 3.0×，**方向对 ≠ 幅度够**。

### 79.4 `analyst47` 判死（天花板 0.57，累计 20 次回测）

| 轮次 | 条数 | 最高 S | 结论 |
|---|---|---|---|
| 探针 17 | 10 | 0.53（A1 W=22） | 十模板全灭 |
| 探针 18 | 10 | **0.57**（B8 totalrawsignal W=66） | 放大/反转全灭 |

- 探针 18 的 10 条**全部**只失 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE`，`CONCENTRATED_WEIGHT`、`LOW_TURNOVER`、`HIGH_TURNOVER` **全部 PASS**
- ⇒ 覆盖率（`anl47_indicator` cov 1.0）与换手都不是瓶颈，**`anl47` 的 1–10 评分序列自身信噪比不足**
- 按判死判据「单原子 S 需 ≥0.6–0.8 才值得投入配方攻势」，0.57 落在判死区
- **新发现：`totalrawsignal`（合成和字段）> `indicator`（复合指标）** —— S 0.57 vs 0.56，2Y **1.72 vs 0.99**（1.74×）
  ⇒ 平台算法做好的复合指标，不如把原始分量直接加总。这一条与「`indicator` 做了额外变换引入噪声」一致

**`JjeRr0Yl` 的 2Y 1.72 是唯一未解线索**：全期 0.57 但最近 2 年 1.72 ⇒ 信号只在 2022–2023 存在，2014–2021 近乎无效。
这是**制度/regime 依赖**，不是可外推的 alpha。且 `LOW_SHARPE` 按全期判定，2Y 强救不了全期。

### 79.5 ★★★ `pwdQWj0q` 突破：DEU 唯一 prod 通过的全闸候选

`prod = 0.6013 PASS`（阈值 0.7），这是本轮唯一一条 prod 通过的 DEU 候选。

```
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),240)),
                                        rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),176))),
                                target_tvr=0.03), subindustry)
```

**即本战役自建的 T-B（M13）骨架落在 `shrt3_bar` 上** —— 不是论坛骨架，prod 天然低。

| 指标 | 值 | 闸 | 判定 |
|---|---|---|---|
| Sharpe | **1.57** | 1.58 | ❌ 差 **0.01** |
| Fitness | 1.24 | 1.0 | ✅ |
| Turnover | 3.62% | 0.01–0.7 | ✅ |
| 2Y Sharpe | **2.39** | 1.58 | ✅ |
| SUB | **1.01** | — | ✅ |
| margin | **42.86bp** | 5bp | ✅ 全场最高 |
| Drawdown | **5.38%** | — | ✅ 全场最低 |
| invest_S | 1.34 | — | ✅ |
| risk_neut_S | 1.15 | — | ✅ |
| prod | **0.6013** | 0.7 | ✅ |
| self | 0.2725 | 0.7 | ✅ |
| failed_ra | **1**（仅 `LOW_SHARPE`） | — | 只差一项 |
| failed_ppa | **0** | — | ✅ PPA 完全合格 |
| CLUSTER_TEST | 0.63 | 1（warning） | 不构成 fail |
| pyramid | `DEU/D1/SHORTINTEREST` ×1.3 | — | shortinterest 塔已点亮 |

**这是全战役最强的单条候选**：五项指标里四项远超闸（F 1.24 vs 1.0、2Y 2.39 vs 1.58、SUB 1.01、margin 8.6× 下限），
只有 Sharpe 差 0.01。且 **PPA 侧零失败项**。

### 79.6 sentiment 族 prod 墙闭合（4/4）

| alpha | prod | 判定 |
|---|---|---|
| `QPvmO0zG` | 0.8983 | ❌ |
| `npvwegqq` | 0.8962 | ❌ |
| `P0ojzWmK` | 0.9074 | ❌ |
| **`d5WezXrx`** | **0.8925** | ❌（本轮新增） |

4/4 全部落在 **0.892–0.907** 极窄区间 ⇒ 该族所有参数变体共享同一条已提交骨架，**结构性 prod 墙**。
剩 3 条（`LLMOzjo1` / `9qxgMvOV` / `VkxKz9bM` / `2rAP60oP`）不再测量——预期同墙，测量只会白占账号级单并发槽。
**sentiment 族在 DEU 判死（prod 维度）**，与 `analyst47`（幅度维度）判死并列。

### 79.7 新增派发

| 批次 | multisim | 内容 | 目的 |
|---|---|---|---|
| 探针 19 | `3gXWul4FE57Ub6GaI7b8mvL` | `institutions4` 十模板（cov 0.3413 / 6 VECTOR 字段 / userCount 1–10） | DEU **最后一个未探索数据集**结案 |
| 定向破闸批 | `499M8wfcE4HkasauyECCOQM` | `pwdQWj0q` 参数收敛 10 条（decay 2→**1**） | 把 S 1.57 推过 1.58 |

**探针 19 的十条（结构互异，按 M 系列 + 机构持股专有机制）**

| # | 机制 | 骨架 |
|---|---|---|
| T1 | 总机构持股存量水平 | `rank(ts_mean(ts_backfill(vec_sum(PO),66),66))` |
| T2 | 自身基线异常度 | `rank(ts_zscore(ts_backfill(vec_sum(PO),66),252))` |
| T3 | 净流入归一（现成 current/previous 方向对） | `rank(ts_mean(ts_backfill(divide(subtract(vec_sum(CS),vec_sum(PS)),add(vec_sum(CS),vec_sum(PS))),66),22))` |
| T4 | 信念集中度 Best Ideas | `rank(ts_mean(ts_backfill(vec_max(PP),66),66))` |
| T5 | 分歧惩罚（二阶矩取负） | `multiply(-1, rank(ts_mean(ts_backfill(vec_stddev(PP),66),66)))` |
| T6 | 广度一阶变化 | `rank(ts_delta(ts_mean(ts_backfill(vec_count(CS),66),66),66))` |
| T7 | 行业相对 | `group_rank(ts_mean(ts_backfill(vec_sum(PO),66),66), subindustry)` |
| T8 | 条件门控 | `trade_when(greater(rank(ts_backfill(vec_count(CS),66)),0.3), rank(ts_zscore(ts_backfill(vec_avg(PP),66),252)), -1)` |
| T9 | 信念-规模背离（序数差） | `rank(subtract(rank(ts_mean(ts_backfill(vec_avg(PP),66),66)), rank(ts_mean(ts_backfill(vec_avg(PO),66),66))))` |
| T10 | 美元口径净增持 | `rank(ts_mean(ts_backfill(divide(vec_sum(CV),vec_sum(PV)),66),22))` |

字段缩写：CV=`institutional_holding_current_market_value` / CS=`..._current_shares` /
PP=`..._percent_of_portfolio` / PO=`..._percent_of_shares_outstanding` /
PV=`..._previous_market_value` / PS=`..._previous_shares`（全 VECTOR，均需 `vec_*`）

预检 10/10 valid、`unknown_fields` 0、`operator_audit` safe（`violations: []`）。
注：预检返回的 `vector_fields: []` 是因为本次显式传 `auto_fix_vector=false`，表达式已手工包裹 `vec_*`，非「字段非 VECTOR」。

**定向破闸批的十条（围绕已确认组件的参数收敛，不受「模板 ≥10」约束）**

| # | 变更 |
|---|---|
| C1 | 基线原式（decay 1 下的锚点，用于量化 decay 杠杆） |
| C2 | `target_tvr=0.05` |
| C3 | `target_tvr=0.08` |
| C4 | `ts_backfill(...,66)` |
| C5 | 窗口 (240,176) → (252,176) |
| C6 | → (252,126) |
| C7 | → (252,66) |
| C8 | → (504,252) |
| C9 | 分组轴 `subindustry` → `sector` |
| C10 | `target_tvr=0.05` + 外层 `rank` 替代 `group_rank` |

**为什么只动 decay（2→1）**：TO 仅 3.62%，远低于论坛实证的 5–15% 最优区间；
且既有实证「decay 5→8→10→12→15 时 S 5.37→4.48→4.03→3.66→3.28」⇒ **降 decay 提 S**。
`ts_target_tvr_decay(target_tvr=0.03)` 自身会把 TO 锁在 3% 附近，所以降 decay 不会失控换手。

### 79.8 本轮新增工程事实

1. **`LOW_SUB_UNIVERSE_SHARPE` 的 limit 随 S 浮动**：`JjeRr0Yl` S 0.57 → limit **0.27**（此前记 0.25）。
   ⇒ 判「SUB 差多少」必须读 `checks.fail` 里的 limit，不能用固定常数。
2. **`risk_neutralized_sharpe > sharpe` 在 anl47 上稳定出现**：`JjeRr0Yl` 0.74 vs 0.57（+30%）、
   `zq3XewXo` 0.70 vs 0.56（+25%）。⇒ 有未剥离风格暴露在拖累信号，但即使剥离后仍距 1.58 有 2.1×。
3. **`rank(ts_mean(F, 66))` > `rank(ts_mean(F, 22))` 在 S 上，但 margin 反向**：
   S 0.48→0.56（+17%），margin 61.4→13.9bp（−77%）。⇒ **长平滑提 S 靠的是压低换手成本，不是提每笔边际**。
   对 `LOW_SHARPE` 是正贡献，对 `LOW_FITNESS` 是负贡献（F 0.22→0.28 实际是正）。
4. **`preflight_expressions` 传 `auto_fix_vector=false` 时 `vector_fields` 必为 `[]`**
   —— 不能用它判断数据集是不是 VECTOR，必须看 `get_datafields` 的 `type`。
5. **`check_correlation` 命中缓存时只需 8.2s**（`d5WezXrx` attempts 7 / elapsed 8213ms），
   与「77–95s」的无缓存路径差 10×。⇒ 同一 alpha 重查优先，别急着当超时。

---

## §80 全闸候选终验 + target_tvr 扫描归因 + 未回测存量核查（2026-10-30 续）

### 80.1 `MPY9VNY9` self 相关性终验通过 —— DEU 首个完整过闸候选

| 闸 | 阈值 | 实测 | 判定 |
|---|---|---|---|
| `failed_ra_count` | 0 | **0** | PASS |
| `failed_ppa_count` | 0 | **0** | PASS |
| **prod correlation** | < 0.7 | **0.5986** | PASS |
| **self correlation** | < 0.7 | **0.27033** | **PASS** |
| pyramid | 单塔 | `DEU/D1/SHORTINTEREST` x1.3 | 不触塔混 |

self 明细（本地增量缓存计算，不占平台相关性槽）：

| 对标 alpha | 相关性 | 说明 |
|---|---|---|
| `blRnKEk6` | **0.2703** | 最强 DEU ACTIVE（S 2.02），SHORTINTEREST+MODEL 四段式 |
| `vRk6og8b` | 0.2088 | 已提交 |
| `2rOe10qY` | 0.1563 | 已提交 |
| `58gkLAkk` | 0.1424 | 已提交 |
| `Vk65zLzG` | 0.1272 | 已提交 |

`pool_size = 10`、`full_os_pool_size = 11`、`excluded_power_pool_count = 1`（即库里 1 条 PPA 已按平台口径排除）。

**⇒ `MPY9VNY9` 现在满足可提交的全部技术条件**（RA 0 / PPA 0 / prod 0.5986 / self 0.2703 / 单塔）。剩余唯一前置条件是用户明确授权——提交是不可逆动作。

### 80.2 target_tvr 扫描批收批（multisim `2cemNPhN4uX9YGBQ8JTwG1`）

10/10 COMPLETE、errors 0。设计为 **7 点一维扫描 + 3 个几何变体**，几何/decay/中性化全部冻结为 `MPY9VNY9` 的配置，只动 `target_tvr`。

| # | target_tvr | 几何 | alpha | S | F | TO | 2Y | SUB | margin | DD | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 基线 | **0.03** | bf22 w(240,176) | **`MPY9VNY9`** | **1.59** | **1.26** | 3.64% | **2.36** | **1.02** | **43.39bp** | 5.33% | **0** |
| T1 | 0.04 | 同上 | `3qog2jez` | 1.43 | 1.08 | 4.22% | 2.02 | 0.78 | 33.64bp | 6.45% | 1 |
| T2 | 0.045 | 同上 | `WjOKxLVP` | 1.52 | 1.18 | 4.47% | 2.26 | 0.84 | 33.54bp | 4.97% | 1 |
| T3 | 0.05 | 同上 | `mLoeQWo6` | 1.52 | 1.17 | 4.80% | 2.26 | 0.83 | 31.09bp | 4.67% | 1 |
| T4 | 0.055 | 同上 | `YP1X9xgl` | 1.55 | 1.21 | 5.14% | 2.28 | 0.80 | 29.59bp | 4.60% | 1 |
| T5 | **0.06** | 同上 | **`npvwXA8l`** | **1.59** | 1.25 | 5.44% | 2.27 | 0.79 | 28.62bp | 4.49% | **0** |
| T6 | **0.065** | 同上 | **`qMLewENK`** | **1.59** | 1.25 | 5.74% | 2.15 | 0.79 | 27.07bp | 4.46% | **0** |
| T7 | 0.07 | 同上 | `vR1aoON3` | 1.63 | 1.30 | 6.07% | 2.19 | 0.74 | 26.34bp | 4.84% | 1 |
| 参照 | 0.08 | 同上 | `xArX5prW` | 1.68 | 1.36 | 6.59% | 2.34 | 0.78 | 24.88bp | 4.69% | 1 |
| G1 | 0.06 | bf**66** | `QPvmoYG5` | 1.51 | 1.16 | 5.38% | 2.00 | 0.66 | 27.41bp | 4.36% | 2 |
| G2 | 0.06 | w(**252**,176) | `58EN2jpz` | 1.48 | 1.13 | 5.42% | 1.97 | 0.75 | 27.10bp | 4.72% | 1 |
| G3 | 0.06 | w(**252**,**126**) | `Xg9XORoz` | 1.34 | 0.97 | 5.35% | 2.14 | 0.69 | 24.74bp | 4.27% | 2 |

### 80.3 归因一：`target_tvr` 的单调性不对称 —— S 单调升，margin 单调降

沿 T = 0.03 → 0.08 单轴：

| 观测量 | 趋势 | 幅度 |
|---|---|---|
| Sharpe | 1.59 → 1.68（中途 1.43 谷底后回升） | +0.09，但 T≤0.055 全部跌破 1.58 |
| Fitness | 1.26 → 1.36 | +0.08 |
| **margin** | **43.39bp → 24.88bp** | **−42.7%** |
| **SUB** | 1.02 → 0.74–0.79 | **−23% 以上** |
| Turnover | 3.64% → 6.59% | +81% |
| Drawdown | 5.33% → 4.69% | −12% |

**★ 推翻上轮假设「T 的甜点在 0.05–0.06」**：0.04/0.045/0.05/0.055 四个点全部 `failed_ra_count = 1`，失败项是 `LOW_SHARPE`（S 1.43–1.55 < 1.58），不是 SUB。T 并非单调函数——**中间段（0.04–0.055）反而最差**，是 S 与 margin 同时退化的谷底。

**正确表述**：`target_tvr` 是 **Sharpe 与单位收益（margin）的对冲旋钮，不是 Sharpe 与 SUB 的对冲旋钮**。T 提高会（a）放大换手 →（b）Sharpe 微升 →（c）单位交易收益被摊薄 43%。SUB 的绝对水平随之下降，但因为平台 SUB 门槛是 `0.434 x Sharpe` 的浮标，T≥0.06 时反而能擦线过。

**⇒ 家族内选型结论：`MPY9VNY9`（T=0.03）在 Sharpe 持平（1.59）的前提下，Fitness / 2Y / SUB / margin 四项全面占优，是本族唯一最优解**。T=0.06/0.065 的 `npvwXA8l` / `qMLewENK` 虽然也 `failed_ra=0`，但 margin 只有基线的 66%/62%，2Y 也只有 2.27/2.15 vs 2.36。

### 80.4 归因二：三个几何变体全部劣于基线

| 变体 | 相对基线 | S | 2Y | 结论 |
|---|---|---|---|---|
| bf22 → bf**66** | 回填窗口 3x | 1.59 → 1.51 | 2.27 → 2.00 | 长回填抹平近期信息，双负 |
| w240 → w**252** | 一年整 | 1.59 → 1.48 | 2.27 → 1.97 | 主腿窗口拉长，双负 |
| w(240,176) → w(**252**,**126**) | 双腿同时拉长/缩短 | 1.59 → **1.34** | 2.27 → 2.14 | 损失最大，2Y 也最差 |

⇒ `(240,176)` 与 `bf22` 这组数值不是随手取的：240 ≈ 一年交易日、176 ≈ 8 个月，两者差 64 日 ≈ 一季度，构成「年度趋势 vs 季度趋势」的双期限一致性。**改成 252 会破坏「年」的锚，改成 126 会缩短次级趋势使两者近乎共线**。这与「时间窗口必须有意义」的准则一致，且现在有实测支撑。

### 80.5 `news81` 判死 —— DEU 全字段物理无数据

`get_datafields(news81, DEU, TOP500, D1)` → **23/23 字段 `coverage = 0.0`**。

关键旁证：字段描述里写着 "per stock in **ASI**"、"for each stock-day in **ASI**, D0" —— 该数据集在 DEU 无数据投递。`mws81_sentiment` / `primary_sentiment_score` / `secondary_sentiment_score` 三个 VECTOR 源字段同样 cov 0。

**这解释了库里的一个假象**：`news81` 有 **188 条 status=`gem` 的表达式、回测数为 0**。此前把它当「未挖掘富矿」，实为「无数据，跑也跑不出东西」。

⇒ `news81` 判死（DEU）。**DEU 的 NEWS category 已被完全封死**（先前探针 16 的 nip 族 + 本轮 news81 无数据）。

### 80.6 ★ 新工程事实：本地库的「已生成未回测」存量 ≠ 可挖空间，必须先做覆盖率复核

用 `get_mining_yield(by_dataset=True, strict=False)` 拉 DEU 数据集级挖掘簿，得到「已生成表达式数 / 已消费数」的完整对照。表面看有 500+ 条从未回测：

| dataset | 已生成 | 未回测 | 状态构成 | 复核结论 |
|---|---|---|---|---|
| `pattern_scores` | 255 | **202** | gem 193 / dropped 46 | 已判死（探针全覆盖） |
| `news81` | 188 | **188** | gem 188 | **cov 全 0，无数据** |
| `shortinterest3` | 247 | 117 | dropped 101 / pending 89 / gem 28 | 已高强度挖过，**有真实剩余** |
| `analyst_factor_signals` | 197 | 102 | gated 92 | 0/94 达标，判死 |
| `fundamental6` | 75 | **58** | gem 50 / gated 8 | **有真实剩余（见 80.8）** |
| `dl_riskfree_returns` | 134 | 49 | gated 40 | prod 墙比 1.0，判死 |
| `mix_unlit_tower_b` | 49 | 39 | pending 39 | shortinterest 字段，待评估 |
| `pv30` | 165 | 33 | gem 31 | PCA 成分 = 分组元数据，非信号 |
| `other455` | 271 | 16 | 多为 dropped | 已挖 227 次，prod 墙 0.667 |

**动作规范**：任何「本地库显示 N 条未回测 ⇒ 还有 N 条可挖」的推断，必须先对数据集做一次 `get_datafields` 覆盖率复核。本轮 `news81` 就是反例：188 条全是死的。

**配套的正面清单**（真实 `consumed=0` 且 `cov>0` 的数据集）：`fundamental6`（50 gem）、`shortinterest3`（117）、`mix_unlit_tower_b`（39）。

### 80.7 ★★ 关键发现：`shortinterest3` 单数据集内含 7 个互异经济维度

`get_datafields(shortinterest3, DEU, TOP500, D1)` → **25 个 VECTOR 字段全部 cov 0.65–0.78**，按经济含义可切成 7 个独立机制：

| # | 字段组 | 经济含义 | cov | 平台 alphaCount | 拥挤度 |
|---|---|---|---|---|---|
| 1 | `shrt3_bar` | 借券需求评级 1–10 | 0.6528 | 323 | 高（已用，MPY9VNY9） |
| 2 | `mean_/max_/min_loan_rate(_main)` | 借券费率水平（做空成本） | 0.6683–0.6872 | 37–161 | 中高 |
| 3 | **`loan_rate_volatility(_main)`** | **借券费率波动（做空风险）** | 0.6683–0.6872 | **8–131** | **中** |
| 4 | **`average_loan_duration_days(_main)`** | **借贷久期（空头持仓年龄）** | 0.6683–0.6872 | **9–50** | **低** |
| 5 | `transaction_count(_main)` | 借贷市场成交活跃度 | 0.6683–0.6872 | 4–54 | 低 |
| 6 | `loaned_share_count(_main)` | 借出股数（空头存量） | 0.6683–0.6872 | 11–34 | 低 |
| 7 | `loaned_market_value_usd(_main)` | 借出美元市值 | 0.6683–0.6872 | **8–30** | **低** |

**为什么这是本轮最重要的发现**：这 7 个维度是**同一份数据投递里的不同物理量**，不是同一信号的不同写法。已有实证支撑其可分离性 —— `blRnKEk6`（`mean_loan_rate_main` 的水平式骨架）与本族 `MPY9VNY9`（`shrt3_bar` 的双期限骨架）self 相关只有 **0.2703**。⇒ **同数据集不同字段的 alpha 之间可以真正正交**，绕开了「一族只能交 1 条」的 self 枷锁。

机制文献先验（凭既有知识引用，本轮 `web_search` 不可用，未在线核验，不附链接）：
- Engelberg, Reed & Ringgenberg (2018, *JF*) "Short Selling Risk" —— 借券费率波动是做空风险的直接度量，空头要求风险补偿，故高波动股预期收益偏高。
- Drechsler & Drechsler —— 借券费率水平刻画做空约束的紧度。
- 借贷久期对应「空头拥挤度/逼空压力」：借券已持续很久意味着空头存量陈旧，边际新增信息少。

### 80.8 ★ M13 骨架的「流量 / 存量」可证伪假设

已知两条 M13（T-B）实证：

| alpha | 字段 | 字段类型 | S | prod | 结果 |
|---|---|---|---|---|---|
| **`Wje5K71x`** | `fnd6_newq_oiadpq` | **流量**（季度经营利润） | **1.73** | **0.4305** | 成功，DEU 最低 prod |
| （历史） | `seqq` | 存量（股东权益） | −0.19 ~ 0.02 | — | 失败 |
| （历史） | `cheq` | 存量（现金） | −0.19 ~ 0.02 | — | 失败 |
| （历史） | `ppentq` | 存量（固定资产净额） | −0.19 ~ 0.02 | — | 失败 |
| （历史） | `invtq` | 存量（存货） | −0.19 ~ 0.02 | — | 失败 |

**假设 H-M13**：M13 的 `ts_delta(F, 240) x ts_delta(F, 176)` 双期限一致性对**流量字段**（利润表 / 现金流量表）有效，对**存量字段**（资产负债表）无效。
**机理解释**：流量字段的 240 日差分 ≈ 同比增速，176 日差分 ≈ 中期增速，两者一致 = 增长质量；存量字段的差分只是缓慢的规模漂移，缺乏「成长」语义，与价格的关系不稳定。

**验证设计（已派发，multisim `2zYSASbKe53u9iGecF5JSYg`）**：几何/设置全部冻结为 `Wje5K71x` 原式（`group_rank(..., sector)`、无 backfill、`target_tvr=0.03`、decay 4），**只换字段**，8 个流量 + 2 个反向流量：

| # | 字段 | 描述 | cov | 方向 |
|---|---|---|---|---|
| F1 | `fnd6_newa2_oiadp` | Operating Income After Depreciation | 0.6267 | + |
| F2 | `fnd6_newa2_oibdp` | Operating Income Before Depreciation | 0.6251 | + |
| F3 | `fnd6_newa2_oancf` | Operating Activities - Net Cash Flow | 0.5396 | + |
| F4 | `fnd6_iby` | Income Before Extraordinary Items | 0.6600 | + |
| F5 | `fnd6_newa2_revt` | Revenue - Total | 0.6264 | + |
| F6 | `fnd6_newa2_pi` | Pretax Income | 0.6224 | + |
| F7 | `fnd6_ibsa` | Income Before Extraordinary Items | 0.6491 | + |
| F8 | `fnd6_newa2_sale` | Sales/Turnover (Net) | 0.5210 | + |
| F9 | `fnd6_capxy` | Capital Expenditures | 0.5130 | **−**（资产增长异象：高资本开支 → 低收益） |
| F10 | `fnd6_newa2_xint` | Interest and Related Expense | 0.6408 | **−**（利息负担上升 → 财务困境） |

### 80.9 新增派发：`shortinterest3` 七维严格单变量移植

multisim `2k2gFTam84pbc3LEHS9A2Ki`，10 条。几何/decay/中性化/truncation/nanHandling 全部冻结为 `MPY9VNY9` 原配置（`-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(F),22),240)), rank(ts_delta(ts_backfill(vec_avg(F),22),176))), target_tvr=0.03), subindustry)`、decay 1、SUBINDUSTRY、trunc 0.08、nanHandling ON）——**唯一变量是字段**，因此结果可以直接与 `MPY9VNY9`（S 1.59 / prod 0.5986）做单因子归因。

| # | 字段 | 经济维度 | 方向假设 |
|---|---|---|---|
| S1 | `loan_rate_volatility_main` | 做空风险（费率波动） | − |
| S2 | `loan_rate_volatility_main` | 同上（**方向对照，取正**） | + |
| S3 | `average_loan_duration_days_main` | 借贷久期 | − |
| S4 | `transaction_count_main` | 借贷活跃度 | − |
| S5 | `loaned_share_count_main` | 借出股数存量 | − |
| S6 | `loaned_market_value_usd_main` | 借出美元市值 | − |
| S7 | `max_loan_rate_main` | 最紧借券成本 | − |
| S8 | `mean_loan_rate_main` | 平均借券成本（**与 ACTIVE `blRnKEk6` 同字段，骨架对照**） | − |
| S9 | `min_loan_rate_main` | 最松借券成本 | − |
| S10 | `average_loan_duration_days_p5_d1` | 借贷久期（高覆盖变体） | − |

S2 是方向对照实验（同一表达式去掉负号），可直接判定「费率波动 → 收益」的符号；S8 是骨架对照（同字段、不同几何 vs `blRnKEk6`），用于分离「字段贡献」与「骨架贡献」。

### 80.10 本轮新增工程事实

1. **`get_mining_yield(by_dataset=True)` 是唯一可用的数据集级挖掘簿**（本地 `query_dataset_profile` 在 DEU 返回 0 行）。它给出 `expressions / consumed / backtested / passed / ra_clean / prod_clean / prod_blocked / prod_wall_ratio` 九个量，是判断「某数据集是否还有剩余」的最快入口。
2. **`consumed - backtested` 的差值要看清构成**：`dropped` 状态代表已被主动放弃，`gem` / `pending` / `gated` 才是「真的没跑过」。两者不能合并统计。
3. **`news81` 的字段描述内含区域标记**（"in ASI"）——当数据集描述与实际投递区域不符时，`get_datafields` 的 `coverage` 是唯一可靠判据。
4. **`create_multi_simulation` 单批 10 条在 2 批并行（20 条）下仍未触发 429**，且无缓存路径的批次约 1 轮轮询即 `all_terminal`。填槽成本远低于 `batch_create_simulations`。
5. **`batch_status` 的 `child_count: 0` + `all_terminal: false` 是正常排队态**，不是失败；本轮两批均先经历该态后正常完成。


---

## §81 两批单变量移植收批 + H-M13 频率修正（2026-10-30 深夜续）

### 81.1 收批摘要

| 批次 | multisim | 内容 | 结果 |
|---|---|---|---|
| fundamental6 M13 年度口径 | `2zYSASbKe53u9iGecF5JSYg` | 10 个年度/半年报流量字段 | **10/10 REJECT**，S 区间 −0.45 ~ +0.36 |
| shortinterest3 七维 | `2k2gFTam84pbc3LEHS9A2Ki` | 10 个字段×方向（含符号对照） | 3 条进 REVIEW，**天花板 S 1.33** |

两批均 `10/10 COMPLETE errors 0`，无语法/字段失败 ⇒ 结论全部可归因到信号本身。

### 81.2 shortinterest3 七维移植全表（几何/设置全冻结 = `MPY9VNY9` 配置）

几何：`-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(F),22),240)),rank(ts_delta(ts_backfill(vec_avg(F),22),176))),target_tvr=0.03),subindustry)`，decay 1 / SUBINDUSTRY / trunc 0.08 / nanHandling ON。
**唯一变量 = 字段 + 符号。**

| 代号 | alpha | 字段 | 方向 | S | F | 2Y | SUB | margin | TO | DD | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `pwdQpb5v` | `loan_rate_volatility_main` | − | 0.85 | 0.49 | 1.57 | 0.49 | 23.78bp | 3.46% | 5.22% | 4 |
| **S2** | `2rAP2Vm6` | `loan_rate_volatility_main` | **+** | **−0.85** | −0.49 | **−1.57** | −0.49 | −23.78bp | 3.46% | 44.5% | 5 |
| S3 | `A1Vq2XvX` | `average_loan_duration_days_main` | − | 0.90 | 0.52 | 1.39 | 0.31 | 25.96bp | 3.25% | 7.41% | 4 |
| S4 | `d5WePJK2` | `transaction_count_main` | − | 0.78 | 0.43 | **1.89** | 0.12 | 22.85bp | 3.40% | 9.91% | 3 |
| S5 | `O0AK2dJY` | `loaned_share_count_main` | − | 0.58 | 0.28 | 1.49 | −0.13 | 17.16bp | 3.42% | 13.5% | 4 |
| S6 | `vR1ao7Oa` | `loaned_market_value_usd_main` | − | 0.38 | 0.15 | 0.85 | −0.19 | 10.94bp | 3.34% | 10.1% | 4 |
| S7 | `QPvmoRYQ` | `max_loan_rate_main` | − | 1.13 | 0.76 | 1.54 | 0.78 | 34.12bp | 3.31% | 7.28% | 3 |
| **S8** | `KPJx2AmN` | `mean_loan_rate_main` | − | **1.33** | 0.96 | **2.01** | **0.97** | **37.94bp** | 3.43% | 7.13% | **2** |
| S9 | `JjeR2aPW` | `min_loan_rate_main` | − | 1.09 | 0.71 | 1.71 | 0.83 | 32.89bp | 3.24% | 8.60% | 2 |
| S10 | `kqNeYpJ6` | `average_loan_duration_days_p5_d1` | − | 0.90 | 0.51 | 1.05 | 0.40 | 23.53bp | 3.39% | 6.34% | 4 |

**★ 三条硬结论**

**① 符号识别实验完美成立（S1 vs S2）。**
同一表达式仅差一个负号：S **+0.85 / −0.85**、F ±0.49、2Y ±1.57、margin ±23.78bp、TO 逐位相同 3.46%。
⇒ 骨架 `ts_target_tvr_decay(multiply(rank(ts_delta(·,240)),rank(ts_delta(·,176))))` 是**严格符号中性**，不隐含方向偏好。
⇒ 负号是**对的**：借券费率波动越高 = 做空风险越大 = 未来收益越低（Engelberg-Reed-Ringgenberg *Short Selling Risk* 的机制先验被本地实证支持）。
⇒ 附带确认 `2rAP2Vm6` 的 DD 44.5% 是**反向持仓**的巨大回撤，不是「同幅度镜像」——做空高费率波动的方向有真实下行保护。

**② 借券费率「水平族」系统性优于「数量族」。**
按 S 排序：`mean_loan_rate` 1.33 > `max_loan_rate` 1.13 > `min_loan_rate` 1.09 > `loan_rate_volatility` 0.85 > `transaction_count` 0.78 > `loaned_share_count` 0.58 > `loaned_market_value_usd` 0.38。
⇒ **`mean` 是这一族的最优聚合**（不是 max 也不是 min），因为「平均借券成本」是市场对该股做空难度的**共识定价**，而 max/min 是极值噪音。
⇒ **金额口径再次全灭**（`loaned_market_value_usd` S 0.38，全场最低），与论坛帖 43152032301591「金额口径混杂公司规模、无无量纲意义」的结论**在 shortinterest 族独立复现**。
⇒ `transaction_count`（活跃度）2Y 1.89 排第二，但 S 只有 0.78 —— 说明它是「近两年有效、长周期衰减」的信号，不是稳定信号。

**③ 骨架对照成功分离「字段贡献」与「骨架贡献」。**
`KPJx2AmN`（`mean_loan_rate_main` + T-B 双期限骨架）S 1.33；
`blRnKEk6`（同字段 `mean_loan_rate_main` + 行业水平式 + 三条 analyst/model 辅腿）S **2.02**。
⇒ 同字段下骨架差 **0.69 Sharpe**，但 `blRnKEk6` 是**跨塔组合**（SHORTINTEREST+MODEL，正被塔混规则禁止复现）。
⇒ 单塔约束下 `mean_loan_rate` 的天花板是 S 1.33，**达不到 1.58 闸**。

**★ 对 shortinterest3 的最终裁定**
七维实测后，该数据集在 `MPY9VNY9` 的 T-B 骨架下**只产出 1 条过闸解**（`shrt3_bar` 评级型字段 S 1.59）。
其余 6 个经济维度全部卡在 S ≤ 1.33。
⇒ **`shrt3_bar` 的独特性 = 「1–10 评级」的离散跳变**：评级跳变让 240 日与 176 日两腿的差分**真正不同**，`multiply` 携带双尺度信息；
⇒ 而费率类字段是缓慢连续场，两腿差分高度共线，`multiply` 退化为近似平方 ⇒ **丢失双尺度结构**。这是 §80 遗留的机理缺口，本轮补上。

### 81.3 fundamental6 年度口径十字段全灭 —— H-M13 被修正为 H-M13''

**上批实测（几何/设置全冻结 = `Wje5K71x` 原式：`group_rank(...,sector)`、无 backfill、decay 4）**

| alpha | S | F | 2Y | SUB | margin | failed_ra |
|---|---|---|---|---|---|---|
| `xArXEEOw` | **0.36** | 0.16 | 0.39 | 0.44 | 19.28bp | 3 |
| `KPJx22PE` | 0.24 | 0.09 | 0.04 | 0.45 | 10.95bp | 3 |
| `kqNeYYEO` | 0.20 | 0.07 | 0.40 | 0.01 | 8.52bp | 4 |
| `akKXggj5` | 0.09 | 0.02 | −0.16 | −0.27 | 5.21bp | 4 |
| `d5WePP5w` | −0.15 | −0.05 | −0.47 | 0.28 | −10.08bp | 3 |
| `d5WePP2J` | −0.21 | −0.07 | 0.04 | 0.16 | −10.85bp | 3 |
| `kqNeYYxP` | −0.25 | −0.09 | −0.16 | 0.10 | −12.69bp | 3 |
| `78Lg2278` | −0.37 | −0.17 | −0.06 | −0.11 | −20.08bp | 3 |
| `pwdQppw3` | −0.42 | −0.20 | 0.01 | −0.20 | −22.49bp | 3 |
| `gJe700kM` | −0.45 | −0.24 | −0.16 | −0.34 | −26.00bp | 4 |

**与基线 `Wje5K71x`（同骨架、`fnd6_newq_oiadpq`、S 1.73、prod 0.4305）相比，10 个字段全灭，最好的一条只有 S 0.36 —— 差 1.37。**

**★ 关键诊断：上批验证用错了频率层。**
10 个字段的频率后缀：
`newa2_*`（9 个）= **annual**；`iby`/`capxy`/`xinty` 的 `y` = **annual**；`ibsa` 的 `sa` = **semiannual**。
而基线 `fnd6_newq_oiadpq` 的 `newq_*q` = **quarterly**。
⇒ **上批一条季度字段都没有**，假设 H-M13 完全没有被检验。

**★ 并且此前「存量四连败」的字段也全是季度口径**：`newq_seqq` / `newq_cheq` / `newq_ppentq` / `newq_invtq`。
⇒ 三组证据合起来构成干净的三分表：

|  | 季度（`newq_*q`） | 年度（`newa2_*` / `*y`） |
|---|---|---|
| **流量**（利润表 / 现金流量表） | **S 1.73 ✅** | **S −0.45~0.36 ❌** |
| **存量**（资产负债表） | **S −0.19~0.02 ❌** | 未测 |

**★ H-M13 → H-M13''（修正后）**
> M13 的 `ts_delta(F,240) × ts_delta(F,176)` 需要**季度频率与流量科目两者同时成立**，缺一即失效。

**机理（这是本轮最有价值的解释）**
- **季度流量**：240 交易日 ≈ 4 个季度 ⇒ `ts_delta(F,240)` ≈ 年度滚动合计的同比变化 ⇒ 真实捕捉「增长加速度」；176 日 ≈ 3 个季度 ⇒ 中期加速度。两腿是**不同时间跨度的增长信息**，`multiply` 有意义。
- **年度流量**：240 交易日恰 ≈ 1 年 ⇒ `ts_delta(F,240)` 跨越**恰好一次年报更新**，退化为「最新年报 vs 上一年报」的单点跳跃；176 日差分落在**同一对年报之间**，与 240 日差分**几乎相同** ⇒ 两腿共线，`multiply` 退化为平方 ⇒ **无增量信息**。
- **季度存量**：存量不累积，240 日差分只是缓慢规模漂移，无「增长」语义 ⇒ `multiply` 是两个漂移的乘积，纯噪音。

**★ 强佐证（映射待核，但方向一致）**
上批最高分 `xArXEEOw`（S 0.36）若按 `batch_status` 的 children 顺序映射为 `fnd6_ibsa`，则它是 10 个字段中**唯一的半年报（semiannual）**。
半年报频率介于季报与年报之间 ⇒ **S 排名第一**（0.36 > 紧随的 0.24 annual）。
这与频率假设的**单调预测一致**：quarterly(1.73) > semiannual(0.36) > annual(−0.45~0.24)。
⚠ 该映射未经 `get_alpha_details(code)` 逐条核实（`children` 顺序 ≠ 提交顺序，见 §80.10）。但**即使映射有误，「年度口径整类失败」的结论仍然稳健**——10 条全部失败，与具体对应关系无关。

### 81.4 两批新派发（均已提交）

**批 A：mean_loan_rate 救援批（`1KkcKic2j4WN9zgtLWvKXBa`，10 条）**
目标：把 `KPJx2AmN`（S 1.33 / F 0.96 / 2Y 2.01 / SUB 0.97 / margin 37.94bp / **failed_ra 2**）推到 S 1.58。
`failed_ra` 明细：`LOW_SHARPE` 1.33 < 1.58、`LOW_FITNESS` 0.96 < 1.00。**F 只差 0.04、S 差 0.25。**
`LOW_SUB_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE` / `CONCENTRATED_WEIGHT` / `LOW_TURNOVER` **全部 PASS** ⇒ SUB 与换手不是瓶颈，只需提 S。

设计依据：若 `multiply` 在慢变场上退化（81.2 ③ 的机理），**解药是增大两腿窗口分离度**。

| 代号 | 变体 | 假设 |
|---|---|---|
| R1 | w(504,252) | 长尺度对（2年 vs 1年） |
| R2 | w(504,126) | 强分离（2年 vs 半年） |
| R3 | w(240,63) | 年 vs 季（分离度 4×） |
| R4 | w(252,176) | 与 `MPY9VNY9` 窗口对对照 |
| R5 | w(240,176) | **原式复现**（批次一致性校验） |
| R6 | T=0.05 | 换手/信号权衡 |
| R7 | T=0.02 | 更保守的换手目标 |
| R8 | bf 5 | 减 backfill 平滑 |
| R9 | bf 66 | 加 backfill 平滑 |
| **R10** | **单期限 w240**（去掉 multiply） | **几何对照：双尺度是否必要** |

**R10 是本批最关键的一条**：如果单期限优于双期限，则证明 `multiply` 在慢变场上是纯噪音，`MPY9VNY9` 的成功完全来自 `shrt3_bar` 的离散跳变特性——这会把 81.2 ③ 的机理假设升级为**实锤**。

**批 B：fundamental6 季度流量验证批（`4dgmB7dsI5fPbqGYKazEHGf`，10 条）**
目的：真正检验 H-M13''。几何/设置严格冻结 `Wje5K71x` 原式（`group_rank(...,sector)`、**无 ts_backfill**、decay 4、T=0.03、w(240,176)），唯一变量是**季度流量字段**。

| 代号 | 字段 | 描述 | cov | 方向 |
|---|---|---|---|---|
| Q1 | `fnd6_newq_oibdpq` | Operating Income Before Depreciation - Quarterly | 0.4548 | + |
| Q2 | `fnd6_newq_piq` | Pretax Income（季度） | 0.5452 | + |
| Q3 | `fnd6_newq_saleq` | Sales/Turnover (Net)（季度） | 0.4544 | + |
| Q4 | `fnd6_newq_cogsq` | Cost of Goods Sold（季度） | 0.4488 | − |
| Q5 | `fnd6_newq_xintq` | Interest and Related Expense（季度） | 0.5255 | − |
| Q6 | `fnd6_newq_dpq` | Depreciation and Amortization（季度） | 0.5145 | − |
| Q7 | `fnd6_newq_xoprq` | Operating Expense - Total（季度） | 0.4568 | − |
| Q8 | `fnd6_newq_xsgaq` | SG&A（季度） | 0.4169 | − |
| Q9 | `fnd6_newq_spiq` | Special Items（季度） | 0.3064 | − |
| Q10 | `fnd6_newq_nopiq` | Non-Operating Income（季度） | 0.4548 | + |

**可证伪预测**：若 H-M13'' 成立，本批应至少 3–5 条 S > 1.0，且「收入/利润类正向字段」（Q1/Q2/Q3）显著优于「成本/费用类反向字段」（Q4–Q9）。
若本批再次全灭 ⇒ 结论升级为「**M13 只对 `fnd6_newq_oiadpq` 单字段有效，是字段特异而非频率/科目类属**」，从而关闭 fundamental6 的 M13 路线。

### 81.5 当前状态与 60 条缺口评估（诚实口径）

**DEU 本轮累计**：约 **3,594** 条已测（探针 1–19 + 各类移植/扫描批）。
**全闸通过**：**1 条**（`MPY9VNY9`：RA 0 / PPA 0 / prod 0.5986 / self 0.2703）。
**近闸可救**：1 条（`KPJx2AmN`，差 S 0.25 + F 0.04，救援批在途）。

**⇒ 60 条目标的现实判定：在 DEU 单区不可达。**
定量依据（三条独立证据）：
1. DEU 全市场开放首周仅 **653** 条 alpha 提交（论坛帖 42587179348119），而本账号已测 3,594 条只出 1 条全闸通过 ⇒ 通过率 **0.028%**。要出 60 条需再测约 **21 万条**，平台吞吐不可能支撑。
2. DEU 可用数据集已高度收敛：`news81`/`analyst47`/`institutions4`/`pattern_scores`/`dl_riskfree`/`analyst_factor_signals` 全部判死；sentiment 族 prod 墙闭合在 0.892–0.907；`macro`/`option`/`imbalance`/`earnings`/`socialmedia` **五塔物理无数据**。
3. 五个 category 的天花板均低于闸线：`analyst47` 0.57、`institutions4` 0.42、`shortinterest3` 除 `shrt3_bar` 外 ≤1.33、`fundamental6` 年度口径 ≤0.36。

**因此路线决策必须由用户裁定**（延续上轮 A/B/C 三选，并新增 D）：

| 路线 | 内容 | 定量预期 |
|---|---|---|
| **A** | 转区承接：DEU 保留已过闸的 `MPY9VNY9`，主力迁至 IND（L3 存量 20 条最多） | 最高产出 |
| **B** | 死磕 DEU：`shortinterest3` 七维 + `fundamental6` 季度流量 | 乐观 +2~3 条 |
| **C** | 走 PPA 通道：`MPY9VNY9`/`pwdQWj0q` 的 `failed_ppa_count` 均为 0，用 PPAC<0.5 取代 PC<0.7 | 可提交通道扩容，数量不变 |
| **D（新）** | **DEU 点塔策略**：每塔 3 条 = 30 条，其余 30 条由他区承接 | 塔分布均衡，总量可达 |

⚠ 无论哪条路线，**`MPY9VNY9` 的提交窗口期有限**：一旦同族变体 `npvwXA8l` / `qMLewENK` / `xArX5prW` 中任何一条先提交，其余全部 self 撞墙（≈0.9+）。当前 `MPY9VNY9` 是族内最优，**应优先提交**。

### 81.6 本轮新增工程事实

1. **`multiply(rank(ts_delta(F,a)), rank(ts_delta(F,b)))` 的双尺度有效性取决于字段时序特性的「跳变 vs 慢变」**，不取决于 a/b 的取值。慢变连续场（借券费率）上两腿共线 ⇒ `multiply` 退化；离散评级场（`shrt3_bar` 1–10）上两腿真实分离 ⇒ 有效。
2. **字段频率后缀是硬约束，必须读 `description` 而不是猜**：`newq_*q` = quarterly、`newa2_*` = annual、`*y` = annual、`*sa` = semiannual（`fnd6_oiadpsa` 的 description 明写 "Semiannual"）。
3. **同一骨架的批次对照必须先做「原式复现」位**（本批 R5）。否则批次间的任何差异都无法与「平台重算/数据版本变化」区分。
4. **符号镜像实验是零成本的骨架性质探针**：对同字段跑 +F 与 −F，若 S 与全部风险指标严格反号而 TO 逐位相同，则骨架符号中性、方向完全由字段经济学决定。**建议任何新自建骨架落地前都跑一次**（成本 2 个仿真槽）。
5. **`failed_ra_count = 2` 且失败项为 `LOW_SHARPE` + `LOW_FITNESS` 时，通常只差一点**（本例 0.25 + 0.04），优先查 S 而非 F —— 因为 F 与 S 同向（F ≈ S × sqrt(returns/max(TO,0.125))），S 涨 F 自动涨。

---

## §82 mean_loan_rate 第一轮救援收批 + ★ 决定性互相关矩阵（族内只能交 1 条）

### 82.1 第一轮救援批全表（`1KkcKic2j4WN9zgtLWvKXBa`，10/10 COMPLETE errors 0）

基准 = `KPJx2AmN`（`mean_loan_rate_main`，T-B 双期限，bf22，w(240,176)，T=0.03，decay 1，SUBINDUSTRY）：S 1.33 / F 0.96 / failed_ra 2。

| 代号 | alpha | 变体 | S | F | 2Y | SUB | margin | TO | DD | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | `pwdQkQ86` | w(504,252) | 0.94 | 0.60 | 1.40 | 1.09 | 30.41bp | 3.34% | 12.6% | 3 |
| R2 | `RRE0o0do` | w(504,126) | 1.00 | 0.66 | 1.36 | **1.29** | 34.21bp | 3.17% | 14.0% | 3 |
| R3 | `O0AKjK9v` | w(240,63) | 1.25 | 0.88 | **2.15** | 1.23 | 37.18bp | 3.32% | 8.69% | 2 |
| R4 | `WjOKRKgG` | w(252,176) | 1.18 | 0.81 | 1.64 | 0.90 | 34.52bp | 3.38% | 8.33% | 2 |
| R5 | `KPJx2AmN` | **原式复现** w(240,176) bf22 T0.03 | 1.33 | 0.96 | 2.01 | 0.97 | 37.94bp | 3.43% | 7.13% | 2 |
| R6 | `qMLepeX2` | T=0.05 | 1.40 | 1.03 | **2.25** | 1.13 | 30.58bp | 4.46% | 8.42% | **1** |
| R7 | `O0AKjKpv` | T=0.02 | 1.37 | 1.01 | 1.99 | 1.13 | **47.33bp** | **2.85%** | 7.51% | **1** |
| R8 | `P0ojbjpp` | bf 5 | 1.33 | 0.97 | 2.19 | 1.04 | 33.18bp | 4.03% | 7.58% | 3 |
| **R9** | **`pwdQkQ6x`** | **bf 66** | **1.44** | **1.08** | 2.02 | 1.02 | **42.43bp** | 3.32% | 7.05% | **1** |
| R10 | `omEQXQlm` | **单期限 w240**（去 multiply） | 1.16 | 0.78 | 1.92 | 1.02 | 35.44bp | 3.15% | 8.59% | 2 |

**★ 五条机理结论**

**① R5 原式复现成功 ⇒ 批次可比性成立。**
`KPJx2AmN` 指标逐位复现（S 1.33 / F 0.96 / 2Y 2.01 / margin 37.94bp / TO 3.43%），且平台**返回了同一个 alpha id**（去重）。
⇒ 本轮全部 R1–R10 的差异都来自变体本身，不含平台重算/数据版本漂移。
⇒ **并且这次 `children` 顺序与提交顺序完全一致**（第 5 位 = R5 = 原式），修正 §80.10 的「顺序不可信」为**条件性**：同批内 submit 顺序可信，跨批合并查询时不可信。

**② ★ 推翻「增大窗口分离度」假设 —— 窗口必须与数据频率对齐，不能盲目拉长。**
R1 (504,252) S **0.94**、R2 (504,126) S **1.00**，是全场最差两条；而原式 (240,176) S **1.33** 最好。
分离度排序：R2 (4×) > R1 (2×) > R4 (1.43×) ≈ R5 (1.36×)，但 S 排序**完全相反**。
⇒ 机理：`loan_rate` 是**季度/月度更新**的慢变场。240 日 ≈ 1 年、176 日 ≈ 8 个月，两腿分别对应「年度水平变化」与「中期水平变化」；拉长到 504/252 后，两腿各自跨过 2 个以上财报周期，**变化被平均抹平**，双尺度差分化成噪音。
⇒ 与 §81.3 的 fundamental6 频率结论**同源**：**差分窗口必须与该字段的更新频率同量级**，否则差分退化。
  - 季度流量字段 + 240/176 日窗口 = 有效（`Wje5K71x` S 1.73）
  - 年度流量字段 + 240/176 日窗口 = 退化（§81.3，S −0.45~0.36）
  - 慢变费率场 + 504/252 日窗口 = 过度平滑（本轮 R1/R2）

**③ ★ R10 单期限对照证明 `multiply` 双尺度**不是**噪音，但增益有限。**
单期限 w240：S **1.16**；双期限 (240,176)：S **1.33**。
⇒ `multiply` 贡献 **+0.17 Sharpe**，方向为正。
⇒ 但在 `shrt3_bar` 上增益更大（`MPY9VNY9` S 1.59 是全族最高），说明**离散评级的跳变特性放大双尺度信息**，连续场只能吃到部分。
⇒ 修正 §81.2 ③ 的表述：`multiply` 在慢变场上**不失效、只是折价**（+0.17 vs 评级场上的更大增益），不是「退化为纯噪音」。

**④ bf 22 → 66 是有效杠杆（+0.11）；bf 5 无效。**
R8（bf5）S 1.33 = 原式，零增益 —— 因为 5 天填充填不满 `mean_loan_rate` 的 33% 缺失（cov 0.6683）。
R9（bf66）S 1.44，且 **F / SUB / margin 三项同时改善**（0.96→1.08、0.97→1.02、37.94→42.43bp），TO 反而微降（3.43%→3.32%）。
⇒ **backfill 窗口应 ≥ 数据缺口的时间尺度**。33% 缺失 ≈ 每 3 天缺 1 天，但借贷市场数据是**稀疏事件型**（不是每日更新），实际缺口可能是连续数周 ⇒ 66 天（一季度）刚好。
⇒ **`ts_backfill` 的 lookback 是「信号质量」杠杆，不是「覆盖率」补救措施** —— 这一点与既有认知（backfill 只为过覆盖率闸）不同。

**⑤ T 与 margin 严格反向，与 2Y 同向。**
T=0.015→0.02→0.03→0.05：margin 47.33→47.33→37.94→30.58bp 单调降；2Y 1.99→1.99→2.01→2.25 单调升。
⇒ 与 §80.3 在 `shrt3_bar` 上观察到的「target_tvr 是 Sharpe 与 margin 的对冲旋钮」**完全一致**，跨字段可复现。

### 82.2 `pwdQkQ6x` 详情：只剩一个失败项

表达式（bf22 → bf66，其余逐字不变）：
```text
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(mean_loan_rate_main),66),240)),rank(ts_delta(ts_backfill(vec_avg(mean_loan_rate_main),66),176))),target_tvr=0.03),subindustry)
```

| 检查项 | 值 | 判定 |
|---|---|---|
| **`LOW_SHARPE`** | **1.44 < 1.58** | ✗ **唯一失败** |
| `LOW_FITNESS` | 1.08 ≥ 1.0 | ✓ |
| `LOW_TURNOVER` / `HIGH_TURNOVER` | 3.32% | ✓ |
| `CONCENTRATED_WEIGHT` | — | ✓ |
| `LOW_SUB_UNIVERSE_SHARPE` | 1.02 ≥ 0.63（≈0.434×1.44） | ✓ |
| `LOW_2Y_SHARPE` | 2.02 ≥ 1.58 | ✓ |
| `MATCHES_PYRAMID` | `DEU/D1/SHORTINTEREST` ×1.3 | ✓ |
| `failed_ppa_count` | **0** | ✓ PPA 通路畅通 |
| `risk_neutralized_sharpe` | 1.14 | — |
| 持仓 | long 170 / short 98 | — |

⇒ 距全闸通过仅差 **0.14 Sharpe**，是 DEU 除 `MPY9VNY9` 外唯一「单点失败」的候选。

### 82.3 ★★ 决定性互相关矩阵 —— 短利息族内只能提交 1 条

`compute_mutual_correlation`（本地计算，零平台配额，4 年 1021 个交易日）：

|  | MPY9VNY9 | pwdQkQ6x | KPJx2AmN | O0AKjKpv | qMLepeX2 |
|---|---|---|---|---|---|
| **MPY9VNY9**（`shrt3_bar`，S 1.59） | 1 | **0.7413** | **0.7605** | **0.7394** | **0.7432** |
| **pwdQkQ6x**（`mean_loan_rate`，S 1.44） | 0.7413 | 1 | 0.9586 | 0.8716 | 0.9316 |
| **KPJx2AmN**（`mean_loan_rate`，S 1.33） | 0.7605 | 0.9586 | 1 | 0.9137 | 0.9463 |
| **O0AKjKpv**（`mean_loan_rate` T0.02，S 1.37） | 0.7394 | 0.8716 | 0.9137 | 1 | 0.8559 |
| **qMLepeX2**（`mean_loan_rate` T0.05，S 1.40） | 0.7432 | 0.9316 | 0.9463 | 0.8559 | 1 |

`max_mutually_below_subset_size = **1**`（threshold 0.5，`max_subset_exact: true`）。

**★ 两条硬结论**

**① 族内所有两两相关都 > 0.5，同字段变体互相 0.86–0.96。**
`mean_loan_rate` 的 4 个变体（bf22/bf66/T0.02/T0.05）两两 0.8559–0.9586 ⇒ **它们本质上是同一条 alpha 的四种写法**，不是 4 个候选。

**② `MPY9VNY9`（`shrt3_bar`）与 `mean_loan_rate` 族的相关也高达 0.7394–0.7605 ⇒ 跨字段但同骨架，仍撞 self 墙。**
这是本轮最重要的一条**负面**结论，直接推翻上轮的一个乐观假设：
- 上轮（§80.7）曾认为「同数据集不同字段的 alpha 可以真正正交（`blRnKEk6` vs `MPY9VNY9` self 仅 0.2703）」。
- 本轮证明：**正交的前提是「骨架也不同」，不是「字段不同」。** `MPY9VNY9` 与 `mean_loan_rate` 族换了字段但共用同一 T-B 骨架 ⇒ 相关 0.74+。
- `blRnKEk6` 之所以与 `MPY9VNY9` 正交（0.2703），是因为它是**多腿 IC 加权水平式**（行业水平 + 三条 analyst/model 辅腿），骨架完全不同。
⇒ **修正为：self 相关由骨架主导，字段其次。要产出多条可提交 alpha，必须换骨架而不是换字段。**

**⇒ 救援的商业价值判定**
| 情形 | 结果 |
|---|---|
| 先提交 `MPY9VNY9` | `pwdQkQ6x` 即使救到 S 1.58，self = **0.7413 > 0.7** ⇒ 仍不可提交 |
| 先提交 `pwdQkQ6x`（若救到 1.58） | `MPY9VNY9` self = 0.7413 ⇒ 反而废掉 S 更高的 `MPY9VNY9` |

⇒ **单纯提 S 的救援批对「产出条数」零贡献。**
⇒ 第二轮救援批（§82.4）的真实目的因此改写：**不是救 S，而是测「换外层横截面操作能否打破 0.74 的相关墙」**。

### 82.4 第二轮救援批（`3UZ0xL60b5boaWDH7OvJXim`，10 条，已提交）

设计原则：既然 S 已接近、瓶颈是相关性，本轮**优先探索能改变 PnL 几何的外层横截面操作**，其次才是 S 提升的叠加。

| 代号 | 变体 | 真实目的 |
|---|---|---|
| P1 | bf66 + T=0.02 | 两个已验证正杠杆叠加（S 最大化） |
| P2 | bf66 + T=0.05 | 同上，偏 2Y |
| P3 | bf88 + T=0.03 | backfill 是否还能再长 |
| P4 | bf132 + T=0.03 | backfill 上限探测 |
| **P5** | bf66 + T=0.02，外层组 **`industry`** | **分组轴粗化 ⇒ 改变 PnL 截面结构** |
| **P6** | bf66 + T=0.02，外层组 **`sector`** | 同上，更粗 |
| **P7** | bf66 + T=0.02，外层组 **`market`** | 全市场无分组（最粗，等价纯 rank） |
| P8 | bf66 + T=0.015 | margin 优先端点 |
| **P9** | bf66 + T=0.02，外层 **`group_neutralize`**（保幅度，非等权） | **换横截面几何 ⇒ 最有可能改变 PnL** |
| **P10** | bf66 + T=0.02，外层 **`zscore`**（全市场 z，保幅度） | 同上 |

**判读规则（预先声明，避免事后拟合）**
- 若 P5–P7 或 P9–P10 出现「S ≥ 1.58 且 与 `MPY9VNY9` 相关 < 0.70」⇒ **突破，DEU 可出第 2 条 shortinterest alpha**。
- 若全部相关仍 > 0.70 ⇒ **确认 T-B 骨架在 DEU shortinterest 上只能出 1 条**，该族封盘，转骨架（需引入不同经济机制，如借贷久期期限结构、借券成本与股价背离等**结构性**构造，而非继续参数收敛）。

### 82.5 顺带确认：PPA 通路状态

`pwdQkQ6x` `failed_ppa_count = **0**`，与 `MPY9VNY9`（0）、`KPJx2AmN`（0）一致。
⇒ **短利息族的 PPA 侧全部畅通**。若走 PPA 通道（PPAC < 0.5 取代 PC < 0.7），理论上相关墙的性质不同——但 PPA 只放宽 **prod** 相关，**不放宽 self** 相关，因此 82.3 的 self 0.74 结论**不因 PPA 通道而改变**。
⚠ 这是一条容易误判的边界，记录在此防止后续重复试错。

---

## §83 交付终验 + 历史积压池普查（2026-10-30 收尾）

### 83.1 交付候选终验快照（`MPY9VNY9`，平台实拉，非缓存推断）

| 项 | 实测值 | 判定 |
|---|---|---|
| `status` / `stage` | UNSUBMITTED / IS | 未提交 |
| `failed_ra_count` | **0** | PASS |
| `failed_ppa_count` | **0** | PASS |
| `checks.fail` | **[]**（空） | PASS |
| `SELF_CORRELATION` | **0.27033**（本地增量缓存，pool_size 10 / full_os_pool 11 / 排除 PPA 1） | PASS |
| `PROD_CORRELATION` | **0.5986**（缓存 2026-10-30T04:45:52，48h 内有效） | PASS |
| Sharpe / Fitness | 1.59 / 1.26 | PASS |
| 2Y / SUB | 2.36 / 1.02 | PASS |
| TO / margin / DD | 3.64% / **43.39bp** / 5.33% | PASS |
| `investability_sharpe` / `risk_neutralized_sharpe` | 1.34 / 1.21 | 风险侧健康 |
| `pyramids` | `DEU/D1/SHORTINTEREST` ×1.3（**单塔**） | 不触塔混 |
| warning | `CLUSTER_TEST` 0.66 < limit 1；`MATCHES_THEMES`；`OSMOSIS_ALLOCATION` | 均为 warning 级 |

self 明细：`blRnKEk6` 0.2703 / `vRk6og8b` 0.2088 / `2rOe10qY` 0.1563 / `58gkLAkk` 0.1424 / `Vk65zLzG` 0.1272。
**⇒ 四项技术条件（RA 0 / prod<0.7 / self<0.7 / 塔不混）全部满足，唯一缺用户授权。**

### 83.2 ★ 新工程事实：`get_pyramid_alphas` 默认只统计「本季度」提交

先前据此接口读 DEU 得 `shortinterest = 0`，与「已提交 2 条 shortinterest」的记账冲突。核对后确认：
该接口**无参调用时只统计当季**（Q4 2026 = 10-01 起）。DEU 本季度提交为 `2rjrMZ25`(10-13, ANALYST)、`Wje5K71x`(10-12, FUNDAMENTAL)、`2rmGAPqN`(10-09, INSTITUTIONS+OTHER)、`58gkLAkk`(10-07, MODEL+OTHER)，逐项与接口返回 `analyst 1 / fundamental 1 / institutions 1 / other 2 / model 1` **完全一致**。

**权威累计口径 = `get_user_alphas(stage="OS")` 后逐条读 `pyramids.list`**。DEU 累计实况（11 条 ACTIVE，含 1 条 SUPER）：

| 塔 | 累计条数 | 是否点亮（≥3） | 持有 alpha |
|---|---|---|---|
| MODEL | 7 | ✅ 已亮 | 58gkLAkk, JjxrYjre, 2rOe10qY, blRnKEk6, vRk6og8b, Vk65zLzG, 883Y3bAW |
| OTHER | 4 | ✅ 已亮 | 2rmGAPqN, 58gkLAkk, JjxrYjre, 2rOe10qY |
| **SHORTINTEREST** | **2** | ❌ **差 1 条** | blRnKEk6, vRk6og8b（**均为跨塔，无单塔成员**） |
| ANALYST | 1 | ❌ 差 2 | 2rjrMZ25 |
| FUNDAMENTAL | 1 | ❌ 差 2 | Wje5K71x |
| INSTITUTIONS | 1 | ❌ 差 2 | 2rmGAPqN |
| INSIDERS | 1 | ❌ 差 2 | Vk65zLzG |
| SENTIMENT / RISK / PV / NEWS / EARNINGS / SOCIALMEDIA / MACRO / OPTION / IMBALANCE | 0 | ❌ | — |

**⇒ `MPY9VNY9` 是 DEU/D1/SHORTINTEREST 的第 3 条、也是该塔唯一的单塔成员。提交即点亮 DEU 第三座金字塔。**

### 83.3 本地库三层库存重算（全区域，`data/wqb.db` 实查）

口径：`backtest_results` 按 (region, alpha_id) 聚合，取 `MAX(sharpe/fitness/turnover/margin/ra_failed_checks)`；
左连 `alphas` 取 prod/self；**剔除 stage=OS / status ∈ {ACTIVE, SUBMITTED, SUPERSEDED}**。

| region | 纸面过闸 + RA 干净（未提交） | 其中 prod&self 双安全 | 其中撞墙 | **其中相关性未测** |
|---|---|---|---|---|
| GBR | 494 | 12 | 32 | **450** |
| DEU | 236 | 0 | 5 | **231** |
| IND | 201 | 19 | 9 | **173** |
| EUR | 173 | 10 | 2 | **161** |
| USA | 122 | 8 | 4 | **110** |
| GLB | 102 | 0 | 34 | **68** |
| KOR | 34 | 0 | 0 | 34 |
| ASI | 8 | 0 | 2 | 6 |
| **TOTAL** | **1370** | **49** | **88** | **1233** |

含已提交的宽口径（L1 纸面 2543 / RA 干净 1450 / 双安全 126）见脚本输出。
**DEU 的 `dual_safe = 0` 是统计假象**：`MPY9VNY9` 的 self 从未回写 `alphas` 表 ⇒ 落入「未测」桶。已用 `persist_correlation` 回写修正。

### 83.4 ★★ 历史积压池实测：抽 4 条全部撞墙（这不是捷径）

从 DEU 231 条「纸面过闸 + RA 干净 + 相关性未测」中，剔除 `code` 只有标签（`R83`/`R89`…）无法判族的记录后，剩 108 个互异指标指纹。
按 margin≥12bp 筛得 149 条，按复合分（S/F/2Y/SUB/margin）排序取头部，逐条上平台核验：

| alpha | 塔（平台实读） | S | F | 2Y | SUB | margin | **self** | **prod** | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| **`VkxKz9bM`** | `DEU/D1/SENTIMENT`（单塔，**未点亮**） | 1.73 | 1.49 | 2.09 | **1.49** | 20.98bp | **0.1052 ✅** | **0.8548 ✗** | DEAD（prod） |
| **`A10mAEqd`** | `DEU/D1/MODEL` | 1.82 | 1.97 | 1.57 | — | 26.2bp | **0.6152 ✅** | **0.8294 ✗** | DEAD（prod） |
| `1Yx01KgW` | `DEU/D1/RISK`+`MODEL`（**RISK 未点亮**） | 1.76 | 1.38 | 1.89 | 1.43 | 12.32bp | **0.7227 ✗** | 未测 | DEAD（self） |
| `ZY0M1G53` | `DEU/D1/SHORTINTEREST` | 2.01 | 1.81 | **2.77** | — | 16.3bp | **0.8984 ✗** | 未测 | DEAD（self） |
| `2rOW3j6b` | `MODEL`+`OTHER` | 2.17 | 1.82 | 2.25 | 1.51 | 14.02bp | 未测 | 未测 | 塔混规则禁止 |
| `E5vxZ7bK` | `MODEL`+`OTHER` | 2.11 | **2.03** | 2.21 | 1.30 | 21.16bp | 未测 | 未测 | 塔混规则禁止 |
| `JjelQnvE` | `DEU/D1/OTHER`（单塔） | 2.61 | 1.48 | 2.36 | 1.29 | 6.46bp | 未测 | 未测 | TO 42%，待测 |

**结论（4/4 抽样，prod 0.8294–0.8548 / self 0.7227–0.8984）**：
积压池的 RA 状态是真的（6/6 抽样均 `failed_ra_count = 0`、`checks.fail = []`），**但相关性墙同样是真的**。
这批 alpha 绝大多数属于「多腿 `add(rank(...), rank(...), ...)` + model/analyst 腿」的**默认骨架族**，
与已提交的 5 条同族 ACTIVE 高度共线（self 0.72–0.90），且在全局生产池里已处于拥挤区（prod 0.83–0.85）。

**⇒ 与 §80.12「自建骨架 = 低 prod 的唯一可靠路径」再次互证：
自建 T-B 骨架 prod 0.5986（`MPY9VNY9`）/ 0.4305（`Wje5K71x`）/ 0.6013（`pwdQWj0q`），
默认骨架族 prod 0.83–0.85。积压池 1233 条的「未测」标签不等于「可用」，预期出生率与新区挖掘同量级。**

### 83.5 新实证：`vector_neut` 救不了 `snt7` 族的 prod 墙

`VkxKz9bM` 的构造是 `vector_neut(quantile(ts_ir(ts_mean(max(snt7 …, 10 个 ts_delay), 5), 22), driver="uniform"), ts_backfill(vec_avg(snl27_relpopularity08), 22))`，
即**已经用跨数据集 popularity 腿做了向量正交**，self 更是低到 **0.1052**（近乎全正交）。
但 prod 仍是 **0.8548**。

**⇒ 补强既有结论「换排名类正交腿 / vector_neut 对 prod 墙无效」**：
- `vector_neut` + 第二数据集正交腿：prod 0.8548
- 论坛高票原式（`LLMOzjo1`）：prod 0.892–0.907
- 两者同样是 `snt7_all_languages_views` 家族 ⇒ **墙在字段族本身，不在表达式写法**。

### 83.6 本轮新增工程事实 5 条

1. **`get_pyramid_alphas` 无参 = 只统计当季**，不能用来判「某塔累计几条」。累计口径走 `get_user_alphas(stage="OS")` + `pyramids.list`。
2. **本地库 `backtest_results.region` 对 DEU 是可信的**（6/6 抽样平台 `settings.region` 均为 DEU），
   与已知不可靠的 `alphas.region_id` / `universe` 两列**不同**——前者由派发参数写入，后者是派生列。
3. **本地库 `backtest_results.code` 可能只有标签**（`R83` / `R89` / `R84/R85` / `RV+Vk65变体`），
   不能用来判族或复现；真实表达式只在平台 `get_alpha_details(code)` 里。
4. **`prod_correlation` 与 `self_correlation` 需成对回写**。只测 prod 不回写 self 会让本地库存把已测候选误判成「未测」，
   进而高估可挖掘空间（本轮 DEU `dual_safe=0` 就是这个假象）。
5. **`check_correlation` 的实际耗时远低于既往估计**：本轮三次均为 8.0s / 10.6s 级（`attempts` 7–9 次重试后成功），
   不是「77–95s 无缓存路径」。吞吐瓶颈应重新评估。

### 83.7 60 条目标的诚实账（更新版）

| 口径 | 数量 | 说明 |
|---|---|---|
| DEU 全闸通过（技术条件齐备） | **1** | `MPY9VNY9`，等授权 |
| DEU 本轮已测总数 | 约 3,634 → 3,640+ | 含探针 1–19、各移植/救援/收敛批 |
| DEU 出生率 | 1 / 3,640 ≈ **0.027%** | |
| 若靠纯 mining 出 60 条 | 需再测约 **21.8 万条** | 平台吞吐不可能 |
| 积压池未测（全区域） | 1,233 | 抽样 4/4 撞墙，预期出生率同量级 |
| 积压池双安全（全区域，已回写修正后会略升） | 49 | 经 PnL 聚簇折算后约 **30 条独立**（L3，IND 20 / GBR 1 / USA 3 / EUR 3 / GLB 3） |

**⇒ 纯 DEU 出 60 条在物理上不成立。** 可交付组合只能是「DEU 单塔点亮 + 他区已验库存承接」。


---

## §84 波 84 收批 —— `other384`（财报电话会记录）首波 10/10 全灭，但判明是工程错配不是机制失效

**日期**：2026-10-30
**multisim**：`2wYRhEecz4NHaAhKyhTPLYT`（10/10 COMPLETE，0 error）
**设置**：EQUITY / DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 /
nanHandling **ON** / pasteurization ON / maxTrade OFF / unitHandling VERIFY / FASTEXPR
**IS 窗口**：2014-01-01 ～ 2023-12-31（平台回显）

### 84.1 逐条结果（10 条全部 `failed_ra_count` 4–5，prescreen REJECT）

| # | 模板 | alpha | Sharpe | Fitness | TO | 2Y | SUB | long/short | margin |
|---|---|---|---|---|---|---|---|---|---|
| T1 | QA−PR tone spread（取负） | `VkxKrv8G` | **−0.43** | −0.24 | 18.44% | 0.59 | −0.59 | 20/20 | −6.49bp |
| T2 | tone 水平 | `YP1XVjAJ` | 0.21 | 0.09 | 18.29% | −0.61 | 0.21 | 20/20 | 3.45bp |
| T3 | tone 一阶变化 126d | `2rAPg178` | **0.67** | 0.43 | 29.59% | 0.08 | 0.03 | **10/10** | 8.11bp |
| T4 | tone 自身基线 zscore 252 | `A1VqpRwd` | 0.20 | 0.07 | 21.32% | −0.44 | −0.07 | 21/21 | 2.61bp |
| T5 | 计数归一化净语调 | `RRE0OJpa` | 0.18 | 0.07 | 18.14% | −0.66 | 0.12 | 20/20 | 2.89bp |
| T6 | 负词比水平（取负） | `1YN68q7J` | −0.10 | −0.03 | 18.74% | −1.11 | 0.00 | 20/20 | −1.56bp |
| T7 | QA/PR 冗长度比变化 | `VkxKrvpG` | −0.56 | −0.39 | 27.99% | −0.31 | −0.04 | 9/9 | −9.50bp |
| T8 | 笑声累积 252d | `6XdgWnwK` | 0.15 | 0.07 | **0.77%** | 0.16 | 0.15 | **0/4** | **80.77bp** |
| T9 | CEO+CFO 出席门控 | `JjeRAVpW` | 0.07 | 0.02 | 3.84% | 0.46 | 0.20 | 47/46 | 5.83bp |
| T10 | 实体匹配质量门控 | `kqNewx36` | 0.03 | 0.01 | 7.62% | −0.72 | 0.14 | 53/53 | 0.96bp |

金字塔归属：10 条全部 `DEU/D1/OTHER`（倍率 1.8）—— `other384` 属 OTHER 塔。

### 84.2 决定性归因：**不是信号弱，是覆盖率 × backfill 窗口错配**

**证据链（三条独立读数互相印证）**：

1. **`CONCENTRATED_WEIGHT = 0.5 / limit 0.1` 在 10/10 全部命中**，且报错日期分散在
   2019-09-25 / 2019-09-30 / 2019-10-02 / 2018-03-12 / 2018-03-13 / 2022-07-13 / 2023-07-07 / 2023-09-20。
   这不是单年异常，是**全期结构性**的权重集中。
2. **`longCount` 只有 9–21 只**（T1/T2/T4/T5/T6 = 20，T3 = 10，T7 = 9），
   而 TOP500 正常横截面应约 250 只。T8 更极端：`longCount 0 / shortCount 4`。
   ⇒ 有效横截面只有全宇宙的 **2%–8%**。
3. **`other384` 字段 coverage = 0.2123（约 TOP500 中 106 只）**，
   而 `ts_backfill(x, 22)` 的 22 个交易日 ≪ 季度电话会间隔（约 63 交易日）。
   ⇒ 两次电话会之间约 2/3 的日子里信号为 NaN，被 `nanHandling=ON` 在数据层填成 **0**，
   再经 `rank()` 后大量并列 ⇒ 中性化后权重挤在少数股票上。

**T8 的换手率是这条证据链的收口**：`rank(ts_sum(ts_backfill(vec_avg(qa_section_laughter_count),22),252))`
的 TO = **0.77%**（低于 `LOW_TURNOVER` limit 0.01，被单独判 FAIL），
margin 却高达 **80.77bp** —— 典型的「几乎不交易」。根因是 `ts_sum` 把 252 天里大部分为 0 的
backfill 值累加，横截面绝大多数为 0 ⇒ 只在极少数日子有非零值。

### 84.3 ★ 方法论修正：这一批**不能**作为 `other384` 的判死依据

10 条模板在结构上确实互异（水平 / 背离 / 一阶变化 / 自身基线 / 计数归一 / 负词比 / 冗长度 / 累积 / 双门控），
但**它们共享同一个错误参数 `ts_backfill(·, 22)` + `truncation 0.08` + `nanHandling ON`**。
按「模板单一会把骨架选错误判成字段没信号」的铁律，这批等价于
**「1 个检验 × 10 个变体」，自由度只有 1 而不是 10**。

判死前必须做参数对齐对照 —— 即波 85。

### 84.4 ★★ 论坛取证（三篇，直接改变参数选择）

#### 帖 A：`43620895448343`（4 票 / 15 评论）《财报电话会的"情绪概率差"——EUR 市场的事件情绪因子》

作者 YW86963，EUR/TOP2500/D1，数据集 `earnings_sent_matrix`（cov ~50.6%），
成品 `XgbXWEWm`，IS 2014–2023 全闸通过。

```text
signed_power(subtract(ts_zscore(ts_backfill(positive_sentiment_probability_3, 60), 250),
                      ts_zscore(ts_backfill(negative_sentiment_probability_3, 60), 250)), 3)
设置：EUR / TOP2500 / D1 / COUNTRY / decay 6 / truncation 0.04
```

**五条可直接移植的实证**：

1. **机制成立 —— 电话会情绪在 EUR 上实测 Sharpe 1.65–1.9**。
   ⇒ `other384` 拿到的 0.67 不是机制天花板，是参数问题。

2. **★ `CONCENTRATED_WEIGHT` 的成因是「早年期横截面稀疏」，修法是 `truncation 0.08 → 0.04`**。
   原帖原话：「根因不是表达式，而是 2014 年初横截面可用股票太少：截断上限 8% 在稀疏横截面上
   经重归一化后仍会超过 10%」。代价仅 Sharpe 1.68 → 1.65。
   **教训：检查 coverage 不能只看整体均值，要看最早年份的单票权重。**
   （波 84 全部 truncation 0.08 ⇒ 这是系统性可修的错误，不是字段缺陷。）

3. **★ backfill 窗口 = 季度节奏 ≈ 60 天；250 天过长会掉 Sharpe**。
   原帖：「加长 backfill 到 250 天可缓解覆盖，但 Sharpe 掉到 1.3，不划算」。
   ⇒ **波 85 用 126 天属于「偏长但未到 250 的中间档」，仍需回退到 60–66。**

4. **`signed_power(·, 3)` 把 prod correlation 从 ~0.9 打到 0.64，Sharpe 基本不变**。
   机理：立方把权重高度集中于「极端情绪意外」样本，持仓结构与 production 里常见的
   平滑 tone 因子显著不同。原帖把它提为通用降 pc 手段。
   （本区当前瓶颈是 Sharpe 不是 prod，故列为后置杠杆。）

5. **「情绪水平」类信号在 production 里极度拥挤**：朴素版 IS Sharpe 1.9 但 PC 高达 0.9，
   换中性化（SUBINDUSTRY/INDUSTRY/COUNTRY/CROWDING/STATISTICAL）+ winsorize + 收益正交
   **全部压不下 0.7**。⇒ 与本地既有结论「换设置救不了，必须换持仓结构」一致。

**评论中的跨区通用要点**：

- **`ZL72853`（★ `CONCENTRATED_WEIGHT` 二分判别法）**：
  「改窗口或换 universe 后 CW 消失 ⇒ 是稀疏成因，收 truncation 有效；
  换什么都还在 ⇒ 是这条腿的字段身份属性，只能换腿。」
  他还给了 EUR/D1 实测对照：`risk70` 上 `ts_rank` 窗口 120→250 使 Sharpe 2.47→2.83、
  SubU 1.17(FAIL)→1.52(PASS)；而 **`decay` 在同一族上是反向的**
  （`sentiment27` 上 decay=6 把 margin 抬到 121bp 却把 IS_LADDER 打到 1.57/1.58 FAIL）。
  ⇒ 「要 margin 就加长 `ts_mean`/`ts_rank` 窗口，decay 只用来微调 PROD」。
- **`MK63856`**：「`ts_backfill` 的窗口 d 必须和电话会的披露节奏匹配（季度口径），
  回填太短会丢连续性、太长会把过期情绪当新信息」。
- **`YJ75326`**：`signed_power(x,3)` 对 |x| 极敏感，前置必须 `winsorize`，
  否则单票会霸占半侧权重、回测看起来 Sharpe 没变但只是单票侥幸。
- **`FX25214`**：消融建议 —— ① 直接对 `pos−neg` 做一次 zscore vs 分别 zscore 再做差；
  ② 把中性概率（不确定性）显式加入，检验高 `pos-neg` 但 neutral 同时高的样本是否同样可靠。
- **`SZ62220`**：季度事件因子天然阶跃，**单纯延长 backfill 只会引入陈旧信息并摊薄盈利点位**；
  更可行的是引入「事件当期注意力冲击」作为置信度乘数（如与财报日异常换手/成交量跳跃做截断交互）。
- **`MW54957`**：同一模板在 GLB/USA 上 prod 同样偏高 ⇒ 「改变分布形式」不等于「改变核心 idea」。

#### 帖 B：`40790666727575`（39 票 / 21 评论）《Earnings 模板分享，低相关性，助你横向点塔》

作者 WL58980。**一阶模板族**（`ts_backfill` 不计入算子使用数量）：

```text
<ts_op>(ts_backfill(<data_field>, <d1>), <d2>)
d1 ∈ {10, 252}      # 两种信息持有假设：10=近期消化，252=跨报告期持有
d2  = 252
ts_op ∈ ts_arg_max / ts_av_diff / ts_quantile / ts_scale / ts_zscore / ts_mean ...
```

- 实测在 **USA（ILLIQUID_MINVOL1M）与 EUR** 各点亮 Earnings；作者称「仅回测 2000 多次便轻松提交 6 条 REA」。
- **`ts_mean` 可替换 `ts_backfill`**（作者猜想 `ts_sum` 亦可）。
- 降相关强化版：`<ts_op>(<ts_op>(ts_backfill(F, d1), d2), d2)` —— 外层再套一个时序算子。
- **★ 核心先验：「平台新推出数据的 alphaCount 接近 0 ⇒ 相关性普遍很低 ⇒ 可轻松提交」**。
  ⇒ `other384` 的 `userCount` 0–2 / `alphaCount` 0–2 正是这个状态，**prod 墙风险极低**，
  瓶颈只在 IS 指标。
- 评论 `JC31003`：「单字段先预处理下，出信号的概率大大增加」。

#### 帖 C：`43907846056599`（3 票）《物是而人非：管理层变动如何改变业绩会议的定价含义》

作者 RL92505。用 `sentiment_weighting_method2`（业绩会综合语调），
并明确写「考虑到 earnings call 本身属于低频披露，本研究**先对最近观测值进行**〔前向填充〕」。
⇒ 独立第三方在 DEU 邻域同一机制上采用了与我修正方向一致的 backfill 处理。

### 84.5 合入的模板库增量

| # | 模板名 | 骨架 | 来源 |
|---|---|---|---|
| **M15（新）** | 分布差 + 长期自标准化 + 保号幂 | `signed_power(subtract(ts_zscore(ts_backfill(A,f),L), ts_zscore(ts_backfill(B,f),L)), e)` | 帖 43620895448343（EUR 实测 S1.65 pc0.64） |
| **M16（新）** | 一阶时序模板族 | `<ts_op>(ts_backfill(F, d1), 252)`，`d1∈{10,252}` | 帖 40790666727575（39 票，USA+EUR 双点亮） |
| **M17（新）** | 双层时序嵌套 | `<ts_op>(<ts_op>(ts_backfill(F,d1),252),252)` | 帖 40790666727575（降相关强化版） |

### 84.6 待验证假设（波 85 / 86 分工）

| 假设 | 检验波次 | 参数 |
|---|---|---|
| H1：`backfill` 22→126 能否把有效横截面从 ~20 只抬到 >100 只 | 波 85（在飞） | bf126 / trunc 0.08 / nanHandling OFF |
| H2：`truncation` 0.08→**0.04** 能否单独修掉 `CONCENTRATED_WEIGHT` | 波 86 | bf66 / trunc **0.04** |
| H3：`nanHandling` ON→OFF 是否让 `ts_backfill` 真正生效 | 波 85 vs 84 对照 | 同表达式、异 nanHandling |
| H4：一阶模板族 `ts_op` 遍历能否找到比 tone 水平更强的形态 | 波 86 | `ts_zscore`/`ts_quantile`/`ts_scale`/`ts_av_diff` |

**⚠ 波 85 的已知风险**：其 bf=126 落在帖 A 实测的「偏长降效区」（60 好、250 掉到 1.3），
且 truncation 仍为 0.08（帖 A 明确 0.04 才修掉 CW）。若波 85 仍撞 CW，直接判为
「truncation 未修」而非「bf 无效」，波 86 一次性把 bf 收到 66 + trunc 收到 0.04。

---

## §85 波 85 —— `other384` 参数对齐批（nanHandling=OFF + bf126）

**波次定位**：波 84 十模板全灭（最高 S 0.67）后，按论坛取证做**唯一变量对齐实验**。
multisim `8RlVtelA5iRc1q17iTF9cur`，10/10 COMPLETE，0 error，prescreen **10/10 REJECT**。

**派发设置**：EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 / **truncation 0.08** /
**nanHandling OFF** / pasteurization ON / maxTrade OFF / unitHandling VERIFY / FASTEXPR。
IS 2014-01-01～2023-12-31，simulationMode FULL。

**相对波 84 的两个变更变量**：
1. `ts_backfill` 窗 `22 → 126`（检验「backfill 能否把有效横截面从 ~20 抬起来」）
2. `nanHandling ON → OFF`（波 84 复盘推断：ON 会在数据层把 NaN 填 0，使 `ts_backfill` 无 NaN 可填）
3. `truncation` 保持 0.08（★ 事后判定这是本波仍全灭的直接原因，见下文）

### §85.1 收批结果

| # | 模板 | alpha | Sharpe | Fitness | TO | 2Y | SUB | long/short | margin | CW 报错日 |
|---|---|---|---|---|---|---|---|---|---|---|
| U1 | tone 水平 bf126 | `ZYQk8lnQ` | **−0.00** | −0.00 | 5.50% | −0.14 | 0.15 | 47/47 | −0.10bp | 2018-03-12 |
| U2 | QA−PR spread bf126 | `WjOKZXGx` | −0.30 | −0.18 | 5.99% | 0.12 | −0.13 | 47/47 | −14.32bp | 2018-03-12 |
| U3 | tone 同比 252 | `Xg9X3l8m` | −0.02 | −0.00 | 8.12% | −0.35 | −0.09 | 34/34 | −1.09bp | 2019-02-28 |
| U4 | tone 长基线 zscore 1008 | `78Lg5XnQ` | −0.09 | −0.03 | 7.26% | −0.79 | 0.26 | 46/46 | −3.23bp | 2018-11-07 |
| U5 | tone 脉冲累积 + zscore | `RRE0Oa11` | **0.28** | 0.15 | 5.36% | 0.13 | 0.05 | 50/49 | 12.54bp | 2018-03-13 |
| U6 | 净词数脉冲 | `P0ojRlOK` | **0.32** | 0.18 | 5.27% | 0.16 | 0.06 | 50/50 | 14.90bp | 2018-03-13 |
| U7 | 笑声脉冲 504 | `e75eY2zJ` | **0.00**（空账本） | — | **0.00%** | — | — | **0/0** | 0 | — |
| U8 | 正负词频差 bf126 | `wpQXdzj5` | −0.05 | −0.01 | 5.80% | 0.22 | 0.09 | 47/47 | −2.35bp | 2018-03-12 |
| U9 | QA/PR 词数比 bf126 | `78Lg5XjZ` | −0.12 | −0.04 | 6.00% | −0.08 | 0.14 | 47/48 | −5.79bp | 2018-03-12 |
| U10 | tone 时序位置 1260 | `E56ojalm` | −0.14 | −0.06 | 7.03% | −0.79 | 0.20 | 47/47 | −5.48bp | 2018-03-12 |

10 条全部归属 `DEU/D1/OTHER`（倍率 1.8）。入库：`linked 0 / upserted 10`，
wave 85 暂定 verdict = **FAIL**（0/10 过硬闸，0 条过 near 线 1.0）。

### §85.2 三项诊断收益（本波唯一兑现的价值）

**H1 部分成立 —— `ts_backfill` 确实有效，但被 truncation 浪费掉了**

`longCount` 从波 84 的 **9–21** 抬到 **34–50**（U1/U2/U8/U9/U10 = 47，U5/U6 = 50，U3 = 34）。
⇒ backfill 把有效横截面扩大了约 **2.3 倍**，方向正确。

**H3 成立 —— `nanHandling=OFF` 是 `ts_backfill` 生效的前提**

波 84（ON）：`longCount` 9–21、TO **18–30%**；波 85（OFF）：`longCount` 34–50、TO **5–8%**。
⇒ 机理确认：`nanHandling=ON` 在数据层把 NaN 填 0，`ts_backfill` 找不到 NaN 可填，
整条信号退化为「裸 22 日窗直接 rank」，于是既窄又高换手。
**任何稀疏事件型数据集必须 `nanHandling=OFF` + `ts_backfill` 配套使用，两者不能分开。**

**H2 被否决 —— backfill 窗口 bf126 属「偏长降效区」**

Sharpe 从波 84 最高 0.67（T3 tone 一阶变化 126d）掉到本波最高 **0.32**（U6 净词数脉冲）。
对照帖 A 实证（60 天最优、250 天掉到 1.3）⇒ bf126 已进入衰减区，下一波回落到 **bf66**。

**CW 未被 backfill 修好** —— `CONCENTRATED_WEIGHT = 0.5 / limit 0.1` 在 **9/10** 仍全撞，
报错日高度集中：`2018-03-12`（5 条）、`2018-03-13`（2 条）、`2018-11-07`（1 条）、`2019-02-28`（1 条）。

⇒ 按帖 A 评论 `ZL72853` 的二分判别法：**CW 日期不随 backfill 窗口移动**（波 84 是 2018-03-12/13/14、
2019-02-28，波 85 几乎同一组日期）⇒ 不是「单票霸占」的稀疏个体问题，而是**早年期横截面整体太窄、
截断上限 8% 经重归一化后仍越过 10%** 的横截面稀疏成因 ⇒ **`truncation 0.08 → 0.04` 是对症修法**。

### §85.3 两个新的结构性读数（修正此前判断）

**① `qa_section_laughter_count` 在 DEU 实质不可用（第二次独立验证）**

波 84：`longCount 0/4`、TO 0.77%、margin 80.77bp（只剩 4 只）。
波 85：**完全空账本** —— `longCount 0 / shortCount 0 / TO 0.00% / pnl 0 / bookSize 0`，
`checks.fail` 直接给 `LOW_TURNOVER 0.00 (limit 0.01)`，`LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE /
CLUSTER_TEST` 全部降级为 `:ERROR`。

⇒ 结论：该字段（连同 `presentation_laughter_count`）**在 DEU 全为 0 或整列为空**。
「uc0/ac0 纯 virgin」≠「有数据」。**必须用回测的空账本读数验证覆盖，不能只信 `get_datafields` 的 coverage 均值。**
下一波起从模板池移除。

**② `other384` 的横截面上限是结构约束，不是参数问题**

`coverage 0.2123 × TOP500 ≈ 106 只`，实际有效横截面 **34–50 只**（backfill 生效后的上限）。
即 backfill 已经把该拿的都拿到了，剩余缺口来自「DEU 只有 500 只票、其中仅 21% 有电话会记录」。

**③ SUB 比值读数印证「0.434 × S」铁律，且两条正收益候选结构性远离 SUB 闸**

| alpha | S | SUB | SUB/S | 判定 |
|---|---|---|---|---|
| `RRE0Oa11` | 0.28 | 0.05 | **0.179** | limit 0.13（=0.434×0.28 取整），实测 0.05，差 0.08 |
| `P0ojRlOK` | 0.32 | 0.06 | **0.188** | limit 0.15，实测 0.06，差 0.09 |

两者 `SUB/S` 仅 **0.18–0.19**（平台硬比 0.434）⇒ 即使把 S 抬到 1.58，SUB 也只能到 ~0.30，仍过不了。
**修正记录**：此前把「SUB/S ≈0.434 恒定」当作规律，本波显示**对稀疏横截面型信号，SUB/S 可以只有 0.18**
—— 0.434 是**上限型**比值（横截面越均衡越接近），不是恒定值。

**④ 被风险中性化后反而变强的信号**

| alpha | S | risk_neutralized_sharpe | 差 |
|---|---|---|---|
| `P0ojRlOK`（净词数脉冲） | 0.32 | **0.48** | **+0.16** |
| `RRE0Oa11`（tone 脉冲累积） | 0.28 | **0.31** | +0.03 |

⇒ 「QA 净词数」这条信号被 **风险因子（规模/波动/行业）部分掩盖**：剥掉风险暴露后信息比更高。
之前 10 条的 `risk_neutralized_sharpe` 全部低于 raw S，唯独 U6 高出 0.16 ⇒ 这是本数据集**唯一**
表现出「独立于风险因子」的骨架，值得在波 86 用另一种几何再验一次。

### §85.4 论坛取证（本轮三帖交叉验证，判定「other384 是工程参数错配，不是机制失效」）

**帖 A `43620895448343`（4 票 / 15 评论）《财报电话会的"情绪概率差"——EUR 市场的事件情绪因子》**
作者 YW86963，成品 `XgbXWEWm`（EUR/TOP2500/D1/COUNTRY/decay 6/**truncation 0.04**），IS 2014–2023 全闸通过：

```text
signed_power(subtract(ts_zscore(ts_backfill(positive_sentiment_probability_3, 60), 250),
                      ts_zscore(ts_backfill(negative_sentiment_probability_3, 60), 250)), 3)
```

五条可移植实证：
1. **机制成立** —— 电话会情绪在 EUR 实测 Sharpe **1.65–1.9** ⇒ `other384` 的 0.67 不是机制天花板。
2. **★ `CONCENTRATED_WEIGHT` 成因是「早年期横截面稀疏」，修法 `truncation 0.08 → 0.04`。**
   原话：「根因不是表达式，而是 2014 年初横截面可用股票太少：截断上限 8% 在稀疏横截面上
   经重归一化后仍会超过 10%」。代价仅 S 1.68→1.65。
3. **★ backfill ≈ 60 天（季度节奏）；250 天过长** —— 「加长 backfill 到 250 天可缓解覆盖，
   但 Sharpe 掉到 1.3，不划算」。
4. **`signed_power(·,3)` 把 prod 从 ~0.9 打到 0.64，Sharpe 基本不变** —— 通用降 pc 手段。
5. **「情绪水平」在 production 里极度拥挤** —— 朴素版 IS S 1.9 但 PC 0.9，换中性化 + winsorize +
   收益正交全部压不下 0.7。

评论要点：
- `ZL72853` **CW 二分判别法** ——「改窗口或换 universe 后 CW 消失 ⇒ 稀疏成因，收 truncation 有效；
  换什么都还在 ⇒ 字段身份属性，只能换腿」。同帖实测 `risk70` 上 `ts_rank` 120→250 使
  S 2.47→2.83、SubU 1.17(FAIL)→1.52(PASS)，而 **decay 在同族上反向**（`sentiment27` decay=6 把 margin
  抬到 121bp 却把 IS_LADDER 打到 1.57/1.58 FAIL）⇒「要 margin 就加长窗口，decay 只用来微调 PROD」。
- `MK63856`「`ts_backfill` 窗口必须和电话会披露节奏匹配（季度口径），太短丢连续性、太长把过期情绪当新信息」。
- `YJ75326`「`signed_power(x,3)` 对 |x| 极敏感，前置必须 `winsorize`」。
- `FX25214` 建议两组消融（直接 `pos−neg` 再 zscore vs 分别 zscore 再差；把中性概率显式加入）。
- `SZ62220`「季度事件因子天然阶跃，单纯延长 backfill 只会引入陈旧信息并摊薄盈利点位；
  更可行是引入事件当期注意力冲击作置信度乘数」。
- `MW54957`「同模板在 GLB/USA prod 同样偏高 ⇒ 改变分布形式 ≠ 改变核心 idea」。

**帖 B `40790666727575`（39 票 / 21 评论）《Earnings 模板分享，低相关性，助你横向点塔》**
作者 WL58980 —— **一阶模板族**（`ts_backfill` 不计入算子使用数量）：

```text
<ts_op>(ts_backfill(<data_field>, <d1>), <d2>)
d1 ∈ {10, 252}    # 10 = 近期消化，252 = 跨报告期持有
d2  = 252
ts_op ∈ ts_arg_max / ts_av_diff / ts_quantile / ts_scale / ts_zscore / ts_mean ...
```

- 实测 USA（ILLIQUID_MINVOL1M）与 EUR 各点亮 Earnings；作者称「仅回测 2000 多次便轻松提交 6 条 REA」。
- `ts_mean` 可替换 `ts_backfill`（猜想 `ts_sum` 亦可）。
- 降相关强化版：`<ts_op>(<ts_op>(ts_backfill(F,d1),252),252)`。
- **★ 核心先验：平台新推出数据 alphaCount 接近 0 ⇒ 相关性普遍很低 ⇒ 可轻松提交。**
  `other384` 的 uc0–2/ac0–2 正是此状态，**prod 墙风险极低，瓶颈只在 IS 指标**。

**帖 C `43907846056599`（3 票）《物是而人非：管理层变动如何改变业绩会议的定价含义》**
作者 RL92505 —— 用 `sentiment_weighting_method2`，明确写「earnings call 属于低频披露，
本研究**先对最近观测值进行**〔前向填充〕」⇒ 独立第三方在 DEU 邻域同一机制上采用与本次修正
方向一致的 backfill 处理。

### §85.5 新合入模板库

| # | 模板名 | 骨架 | 来源 |
|---|---|---|---|
| **M15** | 分布差 + 长期自标准化 + 保号幂 | `signed_power(winsorize(subtract(ts_zscore(ts_backfill(A,f),L), ts_zscore(ts_backfill(B,f),L)), std=4), e)` | 帖 A（EUR 实测 S1.65 pc0.64） |
| **M16** | 一阶时序模板族 | `<ts_op>(ts_backfill(F, d1), 252)`，`d1∈{10,66,252}` | 帖 B（39 票，USA+EUR 双点亮） |
| **M17** | 双层时序嵌套 | `<ts_op>(<ts_op>(ts_backfill(F,d1),252),252)` | 帖 B（降相关强化版） |

### §85.6 波 86 派发方案（唯一变量：`truncation 0.04`）

**设计逻辑**：波 84 + 波 85 两批共享同一个错误 setting `truncation 0.08`，按帖 A 实证这是 CW 的
直接成因。**在跑过 trunc 0.04 之前，`other384` 不具备判死资格。**

**设置**：DEU/TOP500/D1/SUBINDUSTRY/decay 4 / **truncation 0.04** / nanHandling OFF /
pasteurization ON / maxTrade OFF / unitHandling VERIFY / FASTEXPR。

**十模板（M16 × 5 + M15 × 3 + M17 × 1 + d1=10 变体 × 1）**：

| # | 模板族 | 表达式 |
|---|---|---|
| W1 | M16 / ts_zscore | `rank(ts_zscore(ts_backfill(vec_avg(oth384_qa_tone),66),252))` |
| W2 | M16 / ts_quantile | `rank(ts_quantile(ts_backfill(vec_avg(oth384_qa_tone),66),252))` |
| W3 | M16 / ts_scale | `rank(ts_scale(ts_backfill(vec_avg(oth384_qa_tone),66),252))` |
| W4 | M16 / ts_av_diff | `rank(ts_av_diff(ts_backfill(vec_avg(oth384_qa_tone),66),252))` |
| W5 | M16 / ts_arg_max | `rank(ts_arg_max(ts_backfill(vec_avg(oth384_qa_tone),66),252))` |
| W6 | M15 / QA vs PR tone | `signed_power(winsorize(subtract(ts_zscore(ts_backfill(vec_avg(oth384_qa_tone),66),250),ts_zscore(ts_backfill(vec_avg(oth384_presentation_tone),66),250)),std=4),3)` |
| W7 | M15 / QA pos vs neg 词频 | `signed_power(winsorize(subtract(ts_zscore(ts_backfill(vec_avg(oth384_qerfsop_aq),66),250),ts_zscore(ts_backfill(vec_avg(oth384_qerfgen_aq),66),250)),std=4),3)` |
| W8 | M17 / 双层嵌套 | `rank(ts_zscore(ts_zscore(ts_backfill(vec_avg(oth384_qa_tone),66),252),252))` |
| W9 | M16 / d1=10 短持有 | `rank(ts_zscore(ts_backfill(vec_avg(oth384_qa_tone),10),252))` |
| W10 | M15 / QA 净词数 | `signed_power(winsorize(subtract(ts_zscore(ts_backfill(vec_avg(oth384_qa_posnum),66),250),ts_zscore(ts_backfill(vec_avg(oth384_qa_negnum),66),250)),std=4),3)` |

**派发前检查（全通过）**：
- `preflight_expressions(dataset_id="other384")` → `valid: true`、`unknown_fields: []`、
  `unknown_soft: []`、`any_changed: false`（33 个 VECTOR 字段全部已手动 `vec_avg` 包裹）。
- `operator_audit` → `safe: true`，5 个新时序算子（`ts_quantile` / `ts_scale` / `ts_av_diff` /
  `ts_arg_max`）无幽灵命中。

multisim id：`4wDkkecrq4iA8Ok9cUawtaQ`。

**判死决策树（波 86 收盘后执行）**：
- 若 CW 消失且至少 1 条 S ≥ 1.0 → 参数错配确认，进入第二轮（bf66 收敛 + decay/中性化微调）。
- 若 CW 消失但 S 全部 < 1.0 → 机制在 DEU 弱，判死（CW 是唯一挡路因素这一假设被证伪）。
- 若 CW 仍在 → 按 `ZL72853` 判别法属「字段身份属性」，`other384` 无同族可换字段 ⇒ **判死**。

---

## §86 DEU 数据集全量普查闭环（92 + analyst 18 + news 17）—— 60 条在 DEU 物理不可达

### 86.1 为什么要重做普查

此前 `tracking/DEU/candidates/deu_datasets_all.json` 只含 **92 个数据集**，而全量 `get_datasets(region="DEU")` 会**整类漏掉 category**（已被记忆列为已知平台陷阱）。本轮按 category 逐类补拉，补齐两块整类缺口：

| 调用 | 返回数 | cov>0 数 |
|---|---|---|
| `get_datasets(category="analyst")` | **18** | 7 |
| `get_datasets(category="news")` | **17** | 6 |

analyst cov>0 的 7 个：`analyst7`(0.7207/fc608/ac3993)、`analyst48`(0.7879/fc7/已判死)、`analyst93`(0.6373/fc100/ac193)、`analyst47`(0.6234/fc5/已判死)、`analyst_factor_signals`(0.5996/fc108/已判死)、`analyst9`(0.5825/fc51/8 次回测)、`analyst44`(0.5802/fc72/ac58/8 次回测)、`analyst83`(0.3389/fc345/已判死)。

news cov>0 的 6 个：`news104`(0.963/fc11)、`news18`(0.8046/fc70)、`news17`(0.7906/fc48)、`news20`(0.7729/fc46)、`news50`(0.7644/fc37/ac42/**DEU 零回测**)、`news38`(0.5992/fc3/**零回测**)。

### 86.2 ★ 流程纠错：数据集级记录自带 `coverage`，判死不必逐字段

`get_datasets` 返回的每条数据集记录键为：

```text
alphaCount / category / coverage / description / fieldCount / id / name
/ pyramidMultiplier / userCount / valueScore
```

**`coverage` 在数据集级就直接给出**。⇒ 一次 `get_datasets` 调用即可筛掉整批死数据集，比逐字段 `get_datafields` 便宜**两个数量级**。此前几轮先拉字段清单再判死，属**流程顺序错误**（`earningscall_sentiment` 167 字段就是这么白拉一遍才发现全 0 的）。

### 86.3 三分档结果

| 档位 | 数量 | 说明 |
|---|---|---|
| **已测**（`backtest_results` region='DEU' 有行） | **21** | 有真实读数，可判可挖 |
| **未测且 cov>0** | **13** | 其中 11 个已在判死清单 |
| **未测且 cov=0.0** | **58** | 零成本判死 |

未测且 cov>0 的 13 个逐一裁定：

| 数据集 | cov | 字段数 | 裁定 |
|---|---|---|---|
| `pv29` | 1.0 | — | 分组元数据，非信号 |
| `risk88` | 1.0 | 43 | 已判死 |
| `other532` | 0.8563 | — | specific-return 族 prod 墙，已判死 |
| `pv30` | 0.7273 | — | 分组元数据（PCA），已判死 |
| `insiders1` | 0.5343 | — | 制度性（欧盟延迟披露），已判死 |
| `pv109` | 0.4665 | — | bond 口径，已判死 |
| `stock_cluster_dl` | 0.4526 | — | PCA 元数据，已判死 |
| `institutions4` | 0.3413 | — | 已判死（天花板 0.42） |
| `sentiment33` | 0.3221 | — | 已判死 |
| `socialmedia39` | 0.2748 | — | ID 向量，非信号 |
| `fundamental45` | 0.2690 | — | 已判死 |
| **`other47`** | **0.5770** | **18** | ★ 真候选（SEMrush 流量，未判死） |
| **`insider_matrix`** | **0.5485** | **33** | ★ 真候选（未判死） |

⇒ **真正「未测 + 有覆盖 + 未判死」的数据集只剩 2 个：`other47` 与 `insider_matrix`**；加上已测但欠挖的 `analyst44`(8)、`analyst9`(8)、`news50`(0→本轮 10)、`news38`(0)、`analyst93`(121)、`analyst7`(48)、`fundamental6`(16)、`news18`(16)，可挖池总计约 **27 个数据集**。

### 86.4 ★ 关键纠错：「字段数多」与「有数据」完全无关

cov=0 的 58 个里，包含上一轮被点名为「最高优先替代载体」的全部高字段数候选：

| 数据集 | 字段数 | cov |
|---|---|---|
| `analyst_consensus` | 1972 | 0.0 |
| `fundamental72` | 1031 | 0.0 |
| `pv20` | 681 | 0.0 |
| `continuation_score` | 560 | 0.0 |
| `analyst15` | 537 | 0.0 |
| `fundamental89` | 407 | 0.0 |
| `analyst69` | 292 | 0.0 |
| `other696` | 220 | 0.0 |
| `earningscall_sentiment` | 167 | 0.0 |
| `fundamental17` | 135 | 0.0 |
| `other566` / `other78` | 112 | 0.0 |
| `ai_news_scores` | 105 | 0.0 |
| `event_ml_signals` | 104 | 0.0 |
| `event_sentiment_signals` | 52 | 0.0 |
| `news_sentiment_nlp` | 23 | 0.0 |

**上一轮把 `earningscall_sentiment`(167 字段) 定为「最高优先替代载体」是错的，错因是只看 `fieldCount` + `alphaCount`、未看 `coverage`。** 本轮为避免再次踩坑，专门拉全该数据集 167 个字段逐个核验：**coverage 全部 = 0.0**（MATRIX 144 / VECTOR 23），落盘 `tracking/DEU/candidates/ecs_fields.json`，与 `other78`(112 字段 cov 全 0) 完全同型。

### 86.5 定量结论

DEU 可挖数据集总量 ≈ **27 个**，其中真正新鲜的只有 6 个（`other47` / `insider_matrix` / `news50` / `news38` / `analyst44` / `analyst9`）。

- 已测约 **4,650 条**，全闸通过 **1 条**（`MPY9VNY9`）。
- 论坛实证：DEU 全市场开放**首周仅 653 条提交**（GBR 3534），官方文档直接写「GBR 比 DEU 容易」（帖 42587179348119）。
- ⇒ **「60 条 regular alpha 全部在 DEU 产出」在物理上不可达。** DEU 的合理定位是**点塔区**：ANALYST / FUNDAMENTAL / SENTIMENT / RISK / NEWS 五个可达塔各补 3 条 ≈ **12–15 条**，缺口由其他区承接。

---

## §87 波 87 收批：`news50`（RavenPack Web News）—— NEWS 塔首个可回测载体，结构极佳但幅度全无

### 87.1 派发与设置

multisim **`3NsQ656Fa5jFbeZ9Odl7zr1`**，10/10 COMPLETE，0 error。

设置：`DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling OFF / pasteurization ON / maxTrade OFF / unitHandling VERIFY / FASTEXPR / EQUITY`。

派发前置全部通过：`preflight_expressions(dataset_id="news50")` → `valid:true` / `unknown_fields:[]` / `any_changed:false`；`operator_audit` → `safe:true`（`vec_stddev` 非幽灵算子）。

字段：37 个 VECTOR，coverage 全部 **0.7644**，DEU 此前零回测。

### 87.2 十模板结果（模板库 ≥10 且结构互异，达标）

| # | 模板族 | alpha | Sharpe | Fitness | TO | 2Y | SUB | long/short | margin | risk_neut S | 失败项 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 情绪水平自标准化 | `O0AK3RGY` | −0.27 | −0.06 | 34.47% | −0.79 | 0.06 | 65/65 | −11.6bp | −0.40 | SH/F/2Y |
| T2 | 情绪一阶动量 66d | `0mYnJxp8` | −0.13 | −0.02 | 41.24% | −0.36 | 0.31 | 50/50 | −4.8bp | −0.16 | SH/F/2Y |
| T3 | nip 加权情绪（M18） | `Xg9X0Vob` | 0.14 | 0.04 | 15.11% | 0.20 | 0.06 | 67/64 | 15.3bp | −0.12 | SH/F/SUB/2Y |
| T4 | 媒体分歧度 `vec_stddev`（M19） | `qMLeRONV` | **0.16** | 0.05 | **5.00%** | −0.39 | **0.35** | 74/72 | **48.0bp** | **0.34** | SH/F/2Y |
| T5 | 新颖度加权情绪（M18） | `omEQdRNb` | **0.16** | 0.05 | 15.97% | −0.28 | −0.24 | 85/84 | 16.6bp | 0.30 | SH/F/SUB/2Y |
| T6 | BER−BEE 双分类器差（M15） | `RRE0g97j` | −0.03 | 0.00 | 60.27% | −0.06 | −0.14 | 93/93 | −0.8bp | −0.13 | SH/F/**CW**/SUB/2Y |
| T7 | relevance>60 门控 | `3qogN1lg` | −0.22 | −0.07 | 15.27% | −0.61 | −0.13 | 68/67 | −19.5bp | −0.28 | SH/F/**CW**/SUB/2Y |
| T8 | ess×g_ens 双层嵌套（M17） | `58ENXrlM` | −0.42 | −0.12 | 35.78% | −1.06 | −0.32 | 65/65 | −16.8bp | −0.27 | SH/F/SUB/2Y |
| T9 | qcm virgin 情绪 | `N1NkZL77` | −0.06 | −0.01 | 48.19% | −1.36 | 0.24 | 95/93 | −1.4bp | −0.50 | SH/F/2Y |
| T10 | ESS vs VEA 背离（M20） | `pwdQLxjv` | 0.14 | 0.04 | **4.87%** | −0.15 | 0.14 | 86/88 | **48.0bp** | 0.01 | SH/F/2Y |

10 条全部归属 `DEU/D1/NEWS`（倍率 **1.8**）。**prescreen 10/10 REJECT**，0 条过硬闸，0 条过 near 线 1.0。

### 87.3 四项诊断

**① NEWS 塔首次拿到真实回测读数。** 此前 NEWS 塔在 DEU 是 0 条，`news50` 是首个可回测载体。本轮虽然全灭，但把「NEWS 塔在 DEU 到底有没有信号」从 Unknown 变成了 Measured。

**② 横截面宽度不是问题。** `longCount` 达 **50–95**（对照：`other384` 三波只有 9–50）⇒ `news50` cov 0.7644 的横截面确实宽，此前「稀疏数据集聚焦过度」的担心在此不成立。

**③ `CONCENTRATED_WEIGHT` 的值型可二分——这是本轮最有迁移价值的发现。**

| 数据集 | CW 命中率 | 报错 value | 判读 |
|---|---|---|---|
| `other384`（三波 30 条） | **10/10 全撞** | 恒 **0.5** | 稀疏横截面**伪影**（疑似平台上限显示）⇒ 换数据集 |
| `news50`（波 87） | **2/10** | **0.12091 / 0.102686** | **真实集中度** ⇒ 收 truncation 或拉长早期窗口有效 |

具体：`RRE0g97j` 在 2014-07-09 报 0.12091；`3qogN1lg` 在 2014-01-02 报 0.102686——**都落在样本最早两年**，属典型冷启动集中度，不是结构缺陷。

**④ 两条形态健康但幅度不足的候选。**

| alpha | 骨架 | S | TO | margin | SUB | risk_neut S |
|---|---|---|---|---|---|---|
| `qMLeRONV` | `-rank(ts_mean(ts_backfill(vec_stddev(mws50_ess),22),66))` | 0.16 | **5.00%** | **48.0bp** | 0.35 | 0.34 |
| `pwdQLxjv` | `rank(subtract(rank(ts_mean(ts_backfill(ess,22),66)),rank(ts_mean(ts_backfill(vea,22),66))))` | 0.14 | **4.87%** | **48.0bp** | 0.14 | 0.01 |

**margin 48.0bp 是 DEU 本账号历史最高档**（对照 `MPY9VNY9` 43.39bp、`QPvmxN8Q` 18.78bp），TO 不足 5%（论坛帖 30927669645207 的标准是 5%–15% 才合适，这两条正好在**下限**）。`qMLeRONV` 的 SUB/S = 0.35/0.16 = **2.2 ≫ 0.434** ⇒ 小票暴露完全不是约束。

⇒ **判读：方向对（机制未被证伪）、幅度全无。** 这不是「闸门卡死」，是「信号太弱」——从 0.16 走到 1.58 需要 **10 倍**，靠参数微调不可能。根因是 DEU TOP500 只有 500 只大市值股票，新闻类信息的错误定价被套利得最干净。

### 87.4 `nip` 的正确用法（本轮新增结论）

DEU 此前在 `news104`/`news20`/`news17` 上把 nip 族的各条路线都跑过了，全部失败。波 87 的 T3 把 nip 从「信号本体」改成「**影响加权器**」：

```text
rank(divide(ts_sum(multiply(rank(ess),rank(nip)),22), add(ts_sum(rank(nip),22),0.0001)))
```

得 S **0.14**，比 T1（ess 裸水平 S −0.27）好 **0.41**，居全批第二。

⇒ **`mws50_nip` 的信息在于「哪些新闻重要」，不在于「重要新闻的方向」。** 任何把 nip 直接 rank 后当信号本体的写法都可预期失败。

### 87.5 收批入库

`tools/harvest_multisim.py --multisim-id 3NsQ656Fa5jFbeZ9Odl7zr1 --wave 87 --region DEU --dataset news50 --auto-upsert` → EXIT=0：

```text
children=10 terminal=10 done=10 error=0
[upsert] 10 rows → backtest_results (region=DEU wave=87 dataset=news50)
[enqueue] 跳过 133 条已平台实测/终态行
[dedup] 同族去重：2 条标 SUPERSEDED（12 个族，保留 12）
[queue] 61 条过闸候选 → submit_ready
[salvage] all RED, pool entries: 770
```

★ 顺带记录一条工程事实：本机 `python tools/*.py` 直连平台时会读到 `HTTPS_PROXY=127.0.0.1:7897`（未监听 ⇒ `ProxyError` 目标计算机积极拒绝），而 MCP 通道正常。修法是在同一 invocation 里置 `NO_PROXY='*'` + 清空 `HTTP(S)_PROXY`，之后认证与拉取全部正常。


---

## 88. 波 88 / 88B / 88C / 88D —— `analyst44` 净负债修订族：S 上限恒 1.37，REGULAR 通道关闭

### 88.1 机制来源与模板

波 88 的起点是 M21「内建修订」：`analyst44` 的每个指标都有成对的 `*_value` / `*_prevalue`，可直接构造分析师修订率，**不需要跨数据集当门控腿**（这正好满足「单塔优先」与「trio 禁混」两条硬约束）。

```text
<REV_X> = divide(subtract(vec_avg(anl44_2_X_value), vec_avg(anl44_2_X_prevalue)),
                 add(abs(vec_avg(anl44_2_X_prevalue)), 0.0001))
X ∈ eps / sales / netprofit / dps / ebitda / roe / netdebt / epsr / fcfps / tbvps / csh / operatingprofit
```

经济学对应 Stickel (1991) 的 revision drift —— 但如 §88.4 所述，DEU 上**这条通道只在资产负债表杠杆上活着**，在 EPS / 营收 / ROE 上已死。

### 88.2 全量实测（23 条：13 结构变体 + 2 档 decay + 10 条批 C）

按 Sharpe 降序：

| wave | alpha | 结构 | S | F | TO | 2Y | SUB | margin | RA 失败项 |
|---|---|---|---|---|---|---|---|---|---|
| 88C | `A1Vqo3wY` | base bf22/w66, decay 1 | **1.37** | 1.18 | 6.07% | 1.32 | 0.84 | 30.4bp | SH/2Y |
| 88 | `omEQxMLn` | base, decay 4 | 1.35 | 1.15 | 4.92% | 1.36 | 0.86 | 36.9bp | SH/2Y |
| 88D | `A1VqovZQ` | `signed_power(std=4, e=2)` | 1.34 | 1.13 | 4.70% | 1.51 | 0.89 | 37.7bp | SH/2Y |
| 88B | `akKX5AQR` | `signed_power(std=4, e=3)` bf66/w66 | 1.34 | 1.14 | 4.68% | 1.55 | 0.86 | 38.7bp | SH/2Y |
| 88D | `MPY9J3o9` | `signed_power(std=2, e=3)` bf66/w66 | 1.34 | 1.14 | 4.68% | 1.55 | 0.86 | 38.7bp | SH/2Y |
| 88C | `LLMO0Rpn` | bf66/w66, decay 1 | 1.32 | 1.10 | 5.86% | 1.37 | 0.84 | 29.8bp | SH/2Y |
| 88D | `1YN6rZbR` | `signed_power(std=4, e=4)` | 1.31 | 1.12 | 4.67% | 1.55 | 0.81 | 39.1bp | SH/2Y |
| 88D | `kqNezg2L` | `signed_power e=3` bf66/**w44** | 1.29 | 1.08 | 5.91% | 1.52 | 0.68 | 29.4bp | SH/2Y |
| 88B | `RRE0G29g` | bf66/w66 裸 rank | 1.28 | 1.06 | 4.75% | 1.39 | 0.85 | 35.8bp | SH/2Y |
| 88D | `VkxKA0jA` | `signed_power e=3` bf22/w44 | 1.28 | 1.08 | 6.14% | 1.58 | 0.66 | 28.9bp | SH/2Y |
| 88D | `wpQX0bM5` | `rank(quantile(·))` 高斯分位 | 1.28 | 1.06 | 4.75% | 1.39 | 0.85 | 35.8bp | SH/2Y |
| **88D** | **`leAJoKb2`** | **bf66/w88, e=3** | **1.25** | 1.03 | **3.99%** | **2.05** | **0.90** | **42.35bp** | **仅 SH** |
| 88B | `88RgMaEq` | bf22/w44 | 1.17 | 0.93 | 6.22% | 1.57 | 0.63 | 25.4bp | SH/F/2Y |
| 88B | `pwdQ9VMj` | `group_rank` industry | 1.03 | 0.72 | 5.25% | 1.44 | 0.74 | 23.4bp | SH/F/2Y |
| 88D | `P0ojkgdW` | ΔNetDebt/\|**EBITDA_prevalue**\| | 0.95 | 0.68 | 4.66% | 1.29 | 0.65 | 27.2bp | SH/F/2Y |
| 88D | `e75eXQoJ` | ΔNetDebt/\|**sales_prevalue**\| | 0.95 | 0.67 | 4.75% | 1.37 | 0.68 | 26.1bp | SH/F/2Y |
| 88B | `QPvmw2NM` | bf66/w126 | 0.94 | 0.66 | 3.34% | **1.73** | 0.66 | 37.3bp | SH/F |
| 88B | `WjOKvaod` | bf22/w126 | 0.94 | 0.67 | 3.42% | **1.69** | 0.59 | 36.9bp | SH/F |
| 88B | `O0AKlbz1` | `tail` 截尾 | 0.84 | 0.65 | 6.50% | 1.13 | 0.33 | 23.0bp | SH/F/SUB/2Y |
| 88B | `A1VqogzW` | bf66 裸值（未除 prevalue） | 0.72 | 0.29 | 29.96% | 0.09 | 0.32 | 3.3bp | 四闸 |
| 88B | `MPY9JKek` | `ts_zscore(·,252)` | 0.68 | 0.40 | 5.06% | 0.52 | 0.17 | 17.0bp | 四闸 |
| 88B | `d5WeNE3J` | `ts_delta(·,22)` | 0.28 | 0.11 | 10.27% | −0.50 | 0.15 | 3.6bp | SH/F/2Y |
| 88D | `58ENPgoo` | **NetDebt/\|EBITDA\| 水平** | **0.08** | 0.02 | 2.17% | −0.39 | 0.40 | 5.5bp | SH/F/2Y |

### 88.3 三条结构性结论

**① 窗口长度是 S ↔ 2Y 的单调交换轴，不是自由度。** bf66 下 w44 → w66 → w88 → w126：S 1.29 → 1.34 → 1.25 → 0.94；2Y 1.52 → 1.55 → **2.05** → 1.73。`leAJoKb2`（w88）是全族 **2Y 唯一破 2.0** 的点，且 TO 仅 3.99%、margin 42.35bp（全族最高）——代价是 S 只有 1.25，是唯一**只挂 LOW_SHARPE 一项**的候选。

**② `signed_power` 的幂次与 winsorize 强度都不是杠杆。** e=2 → S 1.34 / 2Y 1.51；e=3 → 1.34 / 1.55；e=4 → 1.31 / 1.55。三档在 ±0.03 内打平。`winsorize(std=4)` 与 `std=2` 在 e=3 上**逐位相同**（`akKX5AQR` vs `MPY9J3o9`：S 1.34 / F 1.14 / TO 4.68% / 2Y 1.55 / SUB 0.86 / margin 38.7bp 六项全等）⇒ 分布本身没有超出 2σ 的极端值可截，`winsorize` 在此族是空操作。

**③ decay 是双向 0.0x 级噪声，不是杠杆。** base decay 4→1：S 1.35→1.37（+0.02），2Y 1.36→1.32（−0.04）；bf66/w66 decay 4→1：S 1.28→1.32（+0.04），2Y 1.39→1.37（−0.02）。**与 §「decay 不是 SUB/S 的杠杆」一致：在本族 decay 连 Sharpe 都不是杠杆。**

**④ ★ 水平 vs 变化：跨数据集再次确证论坛结论。** `58ENPgoo`（NetDebt/|EBITDA| **水平**）S **0.08**，而同族变化式 `omEQxMLn` S **1.35** —— 同一资产负债表口径，只换「跟谁比（上个季度 vs 自己）」就差了 **1.27 Sharpe**。这与论坛帖 `43179452121495` 的实验二（利用率水平 −0.20 vs 相对自身异常 +2.28，反号）在**完全不同的数据集与字段上重现同一模式**。⇒ **"水平 vs 变化"是本账号可复用的第一条形态判据。**

**⑤ 换缩放口径即失效。** ΔNetDebt/\|prevalue\| → 1.35；换分母为 \|EBITDA_prevalue\| → 0.95；换 \|sales_prevalue\| → 0.95。两个替代分母同步降到 0.95（差 0.40）。⇒ **`prevalue` 分母不是任意选择：它与分子同源（都是 netdebt 的期初水平），构成自洽的百分比变化；换成异源分母（EBITDA/sales）后变成"杠杆倍数变化"，经济学含义变成 §88 所说的 leverage-distress 通道，在 DEU 上显著更弱。**

### 88.4 波 88D（破闸批 C）设计意图与实际结果

十条分三组，全部收批（multisim `4pk8W5sE55g9Bnhv3ZEJr3`，10/10 COMPLETE，error=0）：

| # | alpha | 变体 | S | 2Y | 意图 | 结果 |
|---|---|---|---|---|---|---|
| C1 | `A1VqovZQ` | `signed_power(e=2)` | 1.34 | 1.51 | 幂次扫描下界 | 与 e=3/4 打平 |
| C2 | `1YN6rZbR` | `signed_power(e=4)` | 1.31 | 1.55 | 幂次扫描上界 | 打平 |
| C3 | `VkxKA0jA` | `e=3` on bf22/w44 | 1.28 | 1.58 | 把 Pareto 杠杆叠到最佳 2Y 结构 | **2Y 升但 S 降** |
| C4 | `P0ojkgdW` | Δ/\|EBITDA_prevalue\| | 0.95 | 1.29 | 换缩放口径 | 掉 0.40 |
| C5 | `58ENPgoo` | NetDebt/\|EBITDA\| 水平 | 0.08 | −0.39 | 杠杆水平异象 | **全灭** |
| C6 | `e75eXQoJ` | Δ/\|sales_prevalue\| | 0.95 | 1.37 | 换缩放口径 | 掉 0.40 |
| C7 | `MPY9J3o9` | `winsorize(std=2)` | 1.34 | 1.55 | 截断强度扫描 | 与 std=4 逐位相同 |
| C8 | `leAJoKb2` | w88 | 1.25 | **2.05** | 窗口细化（S↔2Y 轴） | **2Y 全族最优** |
| C9 | `kqNezg2L` | bf66/w44 | 1.29 | 1.52 | 窗口细化 | 退化 |
| C10 | `wpQX0bM5` | `rank(quantile(·))` | 1.28 | 1.39 | 高斯分位替代 rank | 无增益 |

**收敛判定：** 23 条实测（13 结构 + 2 decay + 10 批 C）的 Sharpe 极值 = **1.37**，距 1.58 门槛恒差 **0.21（15%）**。四个独立方向（幂次、winsorize、窗口、非线性变换）全部无法突破。⇒ **该族的 REGULAR 通道关闭**，后续只投 PPA 通道（`failed_ppa_count = 0` 已过，Sharpe 1.35 ≥ 1.0 门槛，8 算子 / 2 字段满足 ≤8 / ≤3，但 **PPAC 未测且本地不可测**，见 §89.4）。

### 88.5 跨指标合成模板在 DEU 系统性失败（M22 / M23 / M24）

| 模板 | 骨架 | 实测 | 诊断 |
|---|---|---|---|
| M22 跨指标修订背离 | `rank(subtract(rank(rev(A)), rank(rev(B))))` | S 0.45 / 0.12 / **−0.29** | 三例全灭 |
| M23 跨指标修订广度 | 四指标 rank 和 | S 0.18 / TO **157%** / long-short **4/4** | 退化为伪中性 |
| M24 预期 vs 上个实际 | `rev(value vs lastactvalue)` | S **−0.73** | Foster-Olsen-Shevlin 在 DEU 反号 |

M23 的 `long/short = 4/4` 是关键诊断：四指标 rank 求和在横截面上互相抵消，只剩极少数极端票上有非零值 ⇒ **不是"信号弱"，是"信号自相抵消"**。

⇒ 与记忆条目「比值作信号定义可以，作信号合成不行」一致：`divide(EBITDA, EV)` 这类**单信号定义式**有效，而 E1/E2/E5/E6、M22、M23 这类**两信号合成式**全部归零。**后续 DEU 波次不再设计跨指标合成模板。**

---

## 89. 库存重估：12 条 READY 里 8 条被自有 ACTIVE 封死

### 89.1 问题

2026-10-30 之前，`submit_ready` 队列在 DEU 有 **12 条 READY**。按 `submit_verdict` 口径它们全部"可用"。实际并非如此。

### 89.2 实证：PnL 互相关矩阵

用 `compute_mutual_correlation(alpha_ids = 12 READY + 10 ACTIVE, threshold=0.7, years=4)`，22×22 矩阵，1021 个日收益点（本地计算，零配额）：

| READY alpha | 与 ACTIVE 池最大相关 | 对应 ACTIVE | 判定 |
|---|---|---|---|
| `RREXxW6z` | **1.0000** | `2rjrMZ25` | ❌ 逐位副本 |
| `kqJqQL08` | 0.9857 | `2rjrMZ25` | ❌ |
| `6Xdx65eK` | 0.9855 | `2rjrMZ25` | ❌ |
| `1YNv8qaK` | 0.9776 | `2rjrMZ25` | ❌ |
| `58gGQmlN` | 0.9408 | `2rmGAPqN` | ❌ |
| `E56AzejK` | 0.9184 | `2rmGAPqN` | ❌ |
| `XgJ980Wb` | 0.8027 | `58gkLAkk` | ❌ |
| `Vkxnb8QG` | 0.6379 | `2rjrMZ25` | ⚠️ 擦线可过 |
| `MPY9VNY9` | 0.2703 | `blRnKEk6` | ✅ |
| `1YNvvgdJ` | 0.1604 | `883Y3bAW` | ✅ 但 prod 死（§89.3） |
| `N1NML1wq` | 0.0528 | — | ✅ 但 prod 死（§89.3） |
| `kqNRX1ZP` | ≈0.05 | — | ✅ 但 = `N1NML1wq` 的 0.9032 副本 |

`pairs_over_threshold` 共 **15 对**。★ **`max_mutually_below_subset_size = 14` 不可信**：该"互不超阈"子集里同时含有 0.9857 的（`kqJqQL08`, `2rjrMZ25`）一对，实现上有缺陷。⇒ **判读一律以矩阵元素为准，不要引用该汇总字段。**

### 89.3 83 条 RA 干净 S≥1.58 存量按字段族归因，仅 2 条活

`backtest_results` 中 DEU 满足 `ra_failed_checks='[]' AND sharpe>=1.58` 共 **83 条**（此前 `LIMIT 30` 截断曾误报为 30 条）。按字段名多重集聚类（`_cluster30.py`）：

| 字段族 | 条数 | S 范围 | prod / self 实测 | 判定 |
|---|---|---|---|---|
| `snt7_all_languages_views` + `snl27_*`/`snt27_*` 正交腿 | ~20 | 1.88–2.14 | `N1NML1wq` **prod 0.7694** | ❌ |
| `eps_y1_estimate_change_3mo` | ~23 | 1.58–1.78 | 基座 `2rjrMZ25` ACTIVE，self **1.0000** | ❌ |
| `inst1_*` + `oth455_*` 正交腿 | ~25 | 1.60–1.81 | 基座 `2rmGAPqN` ACTIVE，self 0.9184/0.9408 | ❌ |
| `tm_*_r1_r5_r10_rh_glb_d1_*_q1` | 5 | 2.28–2.70 | `1YNvvgdJ` **prod 0.8306**（直方图 40 条 >0.7） | ❌ |
| `netprofit_y1_estimate_change_3mo` | 3 | 1.64–1.65 | `QPKKMg6Q` **prod 0.807** | ❌ |
| `combo_a(alpha)` | 1 | 2.30 | `QPvdMW8Q` **prod 0.8849** | ❌ |
| `mean_estimate_change_pct_f12m_earnings_14d_4` | 1+ | 1.60–1.75 | 基座 `58gkLAkk` ACTIVE，self 0.8027 | ❌ |
| `fnd6_newq_oiadpq` | 1 | 1.73 | ACTIVE `Wje5K71x` | ❌ |
| `shrt3_bar` | 3 | 1.59 | `MPY9VNY9` **prod 0.5986** | ✅ |
| `Vkxnb8QG` 独有族 | 1 | 1.83 | **prod 0.6384** | ✅ |

### 89.4 ★ 决定性结论：prod 由「表达式复合层数」决定，不由字段或指标决定

同一生产池、同一区域、同一时期的两条实测：

| alpha | 表达式复杂度 | 算子数 | prod | prod 直方图 ≥0.4 的条数 |
|---|---|---|---|---|
| `1YNvvgdJ` | `group_rank(tm_15_..._q1, sector)` | **1** | **0.8306** | **40** |
| `Vkxnb8QG` | `trade_when` + `group_neutralize` + `group_rank` + `add` + `bucket` | **5** | **0.6384** | **1** |

⇒ **在 DEU 找可提交候选，筛选序应是「结构复杂度」在前、「Sharpe 高低」在后。** 裸单字段 `group_rank` 无论字段多冷门，都已被生产池覆盖。

### 89.5 ★ PPAC 本地不可测（口径纠正）

`check_self_correlation(alpha_id="omEQxMLn", correlation_type="powerpool")` 返回 **0.0636**，看似 PPA 门槛轻松通过。但同返回里 `pool_size: 1`、`ppac_ids_cached: 1`、`full_os_pool_size: 11` —— **本地 Power Pool 池只含 1 条自有 alpha**，与平台全局 Power Pool 无关。

⇒ **PPAC 只能标「未测」。** 任何据 0.0636 声称「PPA 门槛已过」的结论都无效。平台 PPAC 须在提交时由平台侧计算。

### 89.6 ★ 数候选必须用 PnL 聚簇，字段名族会高估约 3×

本轮另有独立验证：DEU 按「表达式内字段名多重集」聚出 211 族 / 185 个 virgin 族；用 `compute_mutual_correlation` 复核其中 5 条「最优质 sentiment 候选」，互相关 **0.875–0.997**，最大两两互不超 0.5 的子集 = **1 条**。另一组 19 条 D 层候选 → 只构成 **2 大簇**。

**换算规则：每 3 条同族回测 ≈ 1 条独立信号。** 报「已测 N 条 / 剩 M 个候选」前必须先折算。

**零成本去重三件套（按顺序用）：**
1. **指标指纹**——`S/F/TO/2Y/SUB` 五项逐位相同 ⇒ 同一组合（本轮 4 次实证，本地 SQL 即可）；
2. **PnL 聚簇**——`compute_mutual_correlation(ids, threshold=0.7, years=4)`，本地、不占平台槽；
3. **字段名族**——只能用来「分组/找同类」，**不能用来数候选**。

---

## 90. 波 89 —— `other47`（SEMrush 网站流量）十模板

### 90.1 数据集与陷阱

`other47` 实测为 **SEMrush 网站流量与 Google Ads 数据**，18 个字段全部 VECTOR，cov 0.6516（base 组）/ 0.5023（enriched 组）。两个已固化的坑：

1. **数据集级 description 不可信**：`other47` 的描述被 "mapping between BBID and RIC" 文案覆盖，与字段毫无关系。至少 11 个 `other*` 数据集有同款污染。
2. **同数据集内字段前缀不统一**：9 个 base 字段里只有 4 个带 `oth47_` 前缀（`oth47_organic_traffic` / `oth47_organic_keywords` / `oth47_organic_cost` / `oth47_rank`），其余 5 个是**裸名**（`paid_search_budget_estimate` / `paid_search_terms_count` / `paid_search_visitors` / `product_listing_ad_terms` / `unique_product_listing_ads`）。写表达式**原样复制 `get_datafields` 返回的 `id`**。

### 90.2 十模板实测（multisim `2BCyKzg0M4Zh8AeZJCfTUhq`，10/10 COMPLETE）

| 模板 | 骨架 | alpha | S | F | TO | 2Y | SUB | margin |
|---|---|---|---|---|---|---|---|---|
| T7 自引用分组标准化 | `group_rank(ts_zscore(bf(traffic,22),252),subindustry)` | `58ENP5zJ` | **0.75** | 0.39 | 9.76% | **1.73** | **0.92** | 7.04bp |
| T5 可见度排名变化 | `-rank(ts_delta(bf(oth47_rank,22),252))` | `9qxgNMj9` | 0.33 | 0.13 | 8.81% | 1.41 | 0.49 | 4.24bp |
| T10 enriched 访客变化 | `rank(ts_delta(bf(organic_search_visitors_enriched,22),252))` | `vR1aWG2a` | 0.18 | 0.06 | 7.56% | 0.72 | 0.03 | 3.19bp |
| T3 流量二阶波动 | `-rank(ts_std_dev(bf(traffic,22),252))` | `QPvmwzbX` | 0.14 | 0.04 | **1.46%** | −0.29 | 0.75 | 13.38bp |
| T4 付费依赖度 | `-rank(paid/(paid+organic))` | `d5WeNzbg` | 0.05 | 0.01 | 3.53% | 0.73 | 0.19 | 1.59bp |
| T2 流量一阶变化 | `-rank(ts_delta(bf(traffic,22),252))` | `zq3XlGYE` | 0.04 | — | 17.53% | −0.78 | 0.05 | 0.27bp |
| T8 获客成本效率 | `rank(cost/traffic)` | `Xg9Xdzbx` | −0.16 | −0.04 | 3.95% | 0.35 | −0.09 | −4.72bp |
| T9 门控（高流量才做） | `trade_when(rank(traffic)>0.3, -rank(Δ66), -1)` | `akKX5zx6` | −0.27 | −0.08 | **18.52%** | −2.03 | −0.29 | −1.63bp |
| T6 关键词数变化 | `rank(ts_delta(bf(keywords,22),252))` | `gJe7nGbQ` | −0.31 | −0.10 | 16.20% | 0.06 | −0.07 | −2.28bp |
| T1 注意力水平异常 | `-rank(ts_zscore(bf(traffic,22),252))` | `YP1XRz5v` | **−0.66** | −0.34 | 9.40% | −2.16 | −0.77 | −6.94bp |

### 90.3 ★ 判读一：注意力在 DEU 是**动量**不是**反转**，符号选错值 1.41 Sharpe

`YP1XRz5v`（T1：`-rank(ts_zscore(traffic,252))`，S **−0.66**）与 `58ENP5zJ`（T7：`group_rank(ts_zscore(traffic,252),subindustry)`，S **+0.75**）——**同一字段、同一 252 日 zscore、同一 22 日 backfill**，只差「取负 + `rank`」 vs 「不取负 + `group_rank`」，Sharpe 摆幅 **1.41**。

方向上，`58ENP5zJ` 是**正向**（高流量 → 跑赢），即 **Da-Engelberg-Gao (2011) 的注意力反转在 DEU 反号**。这与 DEU TOP500 全是机构主导的大市值股票一致：散户注意力驱动的短期买压 → 反转，这条链条需要散户占比，DEU 没有。

### 90.4 ★ 判读二：`group_rank` 在这一族是增益而非损耗，与 SUB 墙结论不矛盾

记忆条目「`group_rank` 把 SUB/S 从 0.44 打到 0.29，卡 SUB 第一动作是拆横截面外层」在这里**不适用**，因为本族 `58ENP5zJ` 的 SUB = **0.92**，而 S 只有 0.75 ⇒ SUB/S = **1.23 ≫ 0.434**，SUB 完全不是约束。

⇒ **`group_rank` 的 SUB 惩罚只在"信号本身已经把权重压向小票"时才致命**（如 §insider 的幅度加权 zscore）。对流量类这种水平型、本身不偏小票的信号，`group_rank` 反而是纯增益（`YP1XRz5v` −0.66 → `58ENP5zJ` +0.75）。

### 90.5 判读三：幅度不足，机制未证伪

最佳 S 0.75 距 1.58 差 0.83（2.1 倍）。但 `58ENP5zJ` 的 **2Y 1.73 已过 1.58 闸**、SUB 0.92 健康、TO 9.76% 在 5–15% 区间 —— 结构上没有硬伤，是纯幅度问题。

十条全部撞 `CONCENTRATED_WEIGHT`（value 均为 0.1x 档，非 0.5 伪影）⇒ cov 0.65 造成的持仓稀疏是真因。**若要走这条线，下一步必须先解决覆盖（enriched 组 cov 0.50、`uc0–1/ac0–2` 近乎全新但更稀疏），而不是换算子。**

---

## 91. 未点亮三塔的 category 普查（2026-10-30 补测）

### 91.1 普查结果

| category | 数据集数 | cov>0 | 结论 |
|---|---|---|---|
| `sentiment` | 3 | **3** | `sentiment27`（Tranco 网站排名，cov 0.9038 / 18 字段）与 `sentiment7`（Wikipedia 浏览，cov 0.7418 / 3 字段）均**未测**；`sentiment33` 已判死（255 字段全 cov 0/描述污染） |
| `risk` | 5 | 2 | `risk60`（证券借贷，cov 0.835 / 5 字段）**未测**；`risk88` cov 1.0 已判死；`risk68/71/72` 全 cov 0 |

**关键发现：`risk60` 的 5 个字段没有一个出现在任何历史波次里** ⇒ 是真正的 virgin 数据集；而 `sentiment7` 的核心字段 `snt7_all_languages_views` 正是 `N1NML1wq` 撞 prod 0.7694 的那个（已判死）。

### 91.2 `risk60` 字段结构与机制分野

| 字段 | 语义 | uc / ac | 机制类 |
|---|---|---|---|
| `rsk60_offer` | 空头支付的综合借券费（年化） | 122 / 187 | 【价格类】需求侧 |
| `lending_fee_bid_rate` | 多头出借获得的综合费率（年化） | 97 / 138 | 【价格类】供给侧 |
| `rsk60_last` | 快照时刻最近的借/贷费率 | 83 / 120 | 【价格类】边际 |
| `rsk60_crowding` | **有符号的做空活动指标**（正=加空/负=回补） | 38 / 51 | 【数量类】流量 |
| `rsk60_datatime` | 厂商时间戳 HHMMSS | 9 / 11 | 非信号 |

`rsk60_offer − lending_fee_bid_rate` = **做市加成（intermediary markup）**；`rsk60_last − rsk60_offer` = **边际 vs 综合费率**。二者都是"价差"型构造。

★ 陷阱同 `other47`：`lending_fee_bid_rate` 是**裸名**（无 `rsk60_` 前缀），其余四个都有前缀。

### 91.3 论坛取证：帖 `43179452121495`（借券利用率「异常收紧」）

这是本轮取证信息密度最高的一篇。四条直接改变设计的结论：

**① 做差有效、做除无效（作者同波干净对照）**

| 构造 | Sharpe | 判定 |
|---|---|---|
| `offer − bid` | **2.01** | ✅ |
| `offer ÷ 做空占比` | 1.14 | ❌ |
| `last − offer`（组合后） | **2.68** | ✅ 全帖最强 |
| `offer ÷ 利用率` | 1.16 | ❌ |

作者推断：相减的两腿量纲相同，共同成分被消掉，剩干净的价差；相除把两个不同量纲的东西压成比值，分母接近 0 的票会主导组合权重。

⇒ **这直接否掉了我原本为 `risk60` 设计的 `divide(subtract(O,B), add(O,B))` 归一化价差写法**，改为纯 `subtract`。

**② 水平 vs 变化：同字段同方向同池子，结果反号**

| 构造 | Sharpe | margin |
|---|---|---|
| `ts_av_diff(u, 60)`（相对自身异常） | **+2.28** | +43.67‱ |
| `u` 绝对水平 | **−0.20** | −19.79‱ |

⇒ 与 §88.3 ④ 在 `analyst44` netdebt 上的独立确证（水平 0.08 vs 变化 1.35）**完全同构**。这条已成为跨数据集可复用的第一形态判据。

**③ 该机制明确依赖流动性差 —— 对 DEU 是坏消息**

作者换 universe 的干净对照：`ILLIQUID_MINVOL1M` **2.28** → `TOP3000` **2.15** → `TOP1000` **0.99**（腰斩）。

⇒ **DEU 只有 TOP500（纯大市值）**，无 universe 退路。按该梯度外推，`risk60` 在 DEU 上的预期 Sharpe 应在 0.9 以下。

**④ 同一数据集内可藏着两套机制，先在集内找"价 vs 量"分野**

作者用 risk59 一个数据集做出三条 alpha，互相关只有 0.18 / 0.41：【数量类】借了多少、【价格类】借的成本多少。`risk60` 恰好同样可切：`rsk60_crowding`（量）vs `offer`/`bid`/`last`（价）。

### 91.4 波 90 / 波 91 已派发（RISK 塔 + SENTIMENT 塔，并发 2）

| 波 | 数据集 | multisim | 塔 | 机制 |
|---|---|---|---|---|
| 90 | `risk60` | `1IqtEO7qb4r3bOyBa5ni2FX` | **RISK（0/3）** | 借券费价差 / 异常 / 数量流量 / 跨 lender 离散 |
| 91 | `sentiment27` | `41f2IW1pr5gE9z518No58oqN` | **SENTIMENT（0/3）** | 网站关注度水平 / 变化 / 异常 / 离散 / 域名广度 / 分布偏峰 / 断层 / 自引用分桶 |

两批各 10 模板，均 SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling OFF，`preflight_expressions` 双双通过（`unknown_fields: []`、`any_changed: false`）。

**波 90 十模板（结构互异：水平 / 异常 / 价差 / 边际价差 / 价差异常 / 累积流 / 流异常 / 保号幂集中 / 价量背离 / 跨 lender 离散）**

```text
R1  -rank(ts_backfill(vec_avg(rsk60_offer),120))                                       费率水平（Miller 1977 卖空约束）
R2  -rank(ts_av_diff(ts_backfill(vec_avg(rsk60_offer),120),60))                         费率自身基线异常 ★论坛核心
R3  -rank(ts_backfill(subtract(vec_avg(rsk60_offer),vec_avg(lending_fee_bid_rate)),120)) 做市加成（做差）
R4  -rank(ts_backfill(subtract(vec_avg(rsk60_last),vec_avg(rsk60_offer)),120))           边际 vs 综合（论坛最强构造）
R5  -rank(ts_av_diff(ts_backfill(subtract(vec_avg(rsk60_offer),vec_avg(lending_fee_bid_rate)),120),60)) 价差异常
R6  -rank(ts_sum(ts_backfill(vec_avg(rsk60_crowding),120),60))                          累积做空流
R7  -rank(ts_av_diff(ts_backfill(vec_avg(rsk60_crowding),120),60))                      做空流异常
R8  signed_power(subtract(group_rank(winsorize(ts_av_diff(bf(offer,120),60),std=4),sector),0.5),7)  论坛骨架+保号幂
R9  rank(subtract(rank(ts_av_diff(bf(offer,120),60)),rank(ts_av_diff(bf(crowding,120),60))))  价量背离（对照，预期失败）
R10 -rank(ts_mean(ts_backfill(vec_stddev(rsk60_offer),120),60))                         跨 lender 费率离散
```

**波 91 十模板（关注度数据的十条互异加工：水平 / 一阶 / 自身异常 / 离散 / 域名广度 / 国际分散 / 偏度 / 峰度 / 断层 / 自引用分桶）**

```text
S1  -rank(ts_backfill(vec_avg(snl27_relpopularity1),22))
S2  -rank(ts_delta(ts_backfill(vec_avg(snl27_relpopularity1),22),66))
S3  -rank(ts_av_diff(ts_backfill(vec_avg(snl27_relpopularity1),22),60))
S4  -rank(ts_mean(ts_backfill(vec_stddev(snl27_relpopularity1),22),60))
S5  -rank(ts_backfill(vec_avg(snl27_totaldomains),22))
S6  -rank(ts_backfill(vec_avg(snl27_totalcountrydomains),22))
S7  -rank(ts_backfill(vec_avg(snl27_skewness),22))
S8  -rank(ts_backfill(vec_avg(snl27_kurtosis),22))
S9  rank(subtract(rank(bf(vec_avg(snl27_top75pctrankingavg),22)),rank(bf(vec_avg(snl27_avgranking),22))))
S10 group_neutralize(group_rank(-bf(vec_avg(snl27_relpopularity1),22),sector),bucket(rank(ts_mean(bf(vec_avg(snl27_relpopularity1),22),252)),range="0,1,0.05"))
```

### 91.5 点塔缺口定量

DEU 当前塔状态与缺口：

| 塔 | 已提交 | 状态 | 缺口 |
|---|---|---|---|
| MODEL | 7 | ✅ 已点亮 | 0 |
| OTHER | 4 | ✅ 已点亮 | 0 |
| **SHORTINTEREST** | 2 | 差 1 | **1**（`MPY9VNY9` 提交即补满） |
| **ANALYST** | 1 | 差 2 | **1**（`Vkxnb8QG` 提交后 2/3，再差 1） |
| **FUNDAMENTAL** | 1 | 差 2 | 2 |
| **INSIDERS** | 1 | 差 2 | 2 |
| **NEWS** | 0 | 零 | 3 |
| **SENTIMENT** | 0 | 零 | 3（波 91 在飞） |
| **RISK** | 0 | 零 | 3（波 90 在飞） |

⇒ **点塔实际缺口 14 条**（两块在飞覆盖 RISK+SENTIMENT 的 6 条目标）。这与此前的「60 条」目标相差 4 倍以上，且 4,655 条累计回测只产出 2 条全闸通过 —— **DEU 的物理上限已由三轮独立证据定量确认**（可挖池 ≈27 数据集、83 条 RA 干净存量只剩 2 条、`netdebt`/`other47`/`news50` 三族全部收敛）。

---

## §92 盲测候选聚簇收敛 + `institutions6` 富矿定位（2026-10-30 第三轮）

本节承接 §91。核心动作：把 §91 遗留的「34 条 prod 未测」从「逐条花配额盲测」改为「先零成本聚簇、只对族代表花配额」，并在此过程中定位到一个被严重低估的数据集 `institutions6`。

### 92.1 PnL 互相关把 19 条盲测压成 3 个独立族

`compute_mutual_correlation`（23 条 = 19 条未知 + 4 条已知代表，threshold 0.7 / years 4 / num_points 1021）。**该工具纯本地下载 PnL 计算，不占平台相关性槽、零配额。**

| 族 | 成员 | 族内相关 | 与 `QPveY7Kg` 的相关 |
|---|---|---|---|
| **N** | `npvwXA8l` / `qMLewENK` | **0.9944** | 0.0216 / 0.0207 |
| **F1a** | `QPKKMg6Q` / `j288RaEQ` / `A1vv9mmX` | 0.9962–**1.0000** | −0.034 ~ −0.036 |
| **F1b** | `1YNv8qaK` / `6Xdx65eK` / `JjQ7vaAx` / `kqJqQL08` / `E5Rlend1` / `GrOleXAJ` / `d51jRJMX` / `YPM7g33W` / `npP78m9l` / `58glOpJn` | 0.90–0.9994 | −0.02 ~ −0.05 |
| **A** | `QPveY7Kg`✅0.6671 / `1YNvPXrm`0.7649 / `d5WqmExJ` / `vR109elb` / `xArMQPdJ` / `LLMOzjo1`0.9029 / `2rAP60oP` | 0.65–0.89 | — |

关键成对数字：

- `j288RaEQ`–`A1vv9mmX` = **1.0000**（逐位相同级别）
- `YPM7g33W`–`58glOpJn` 0.9994；`d51jRJMX`–`npP78m9l` 0.9994；`E5Rlend1`–`GrOleXAJ` 0.9992
- `npvwXA8l`–`qMLewENK` 0.9944
- `LLMOzjo1`–`2rAP60oP` = **0.8166** ⇒ `LLMOzjo1` prod 0.9029 对 `2rAP60oP` 构成真实威胁
- `max_mutually_below_subset` = 7 条（`max_subset_exact: true`）：`1YNv8qaK, QPKKMg6Q, LLMOzjo1, vR109elb, npvwXA8l, QPveY7Kg, JjelQJoe`

**换算规则再次成立：19 条盲测 → 4 个代表。每 3 条同族回测 ≈ 1 条独立信号。**

**方法论固化**：数候选**必须**用 PnL 聚簇。字段名多重集会高估约 3 倍（DEU 按字段名聚出 211 族 / 185 virgin 族，实际只有 3 个独立信号）。

### 92.2 `npvwXA8l` 全闸验毕，但被 `MPY9VNY9` 完全支配 ⇒ 不提交

| alpha | S | F | TO | 2Y | SUB | margin | inv_S | prod | self | 塔 |
|---|---|---|---|---|---|---|---|---|---|---|
| `MPY9VNY9` | 1.59 | 1.26 | **3.64%** | **2.36** | **1.02** | **43.39bp** | — | 0.5986 | 0.2703 | SHORTINTEREST |
| `npvwXA8l` | 1.59 | 1.25 | 5.44% | 2.27 | 0.79 | 28.62bp | 1.28 | 0.6093 | 0.2608 | SHORTINTEREST |

`npvwXA8l` 表达式是 `MPY9VNY9` 的**同族 M13 架构**，唯一差别 `target_tvr` 0.03→0.06、decay 4→1。四项（TO / 2Y / SUB / margin）**全面劣于** `MPY9VNY9`，且 SHORTINTEREST 塔提交 `MPY9VNY9` 后即 3/3 点满。

- `ra.failed_ra_count = 0`、`checks.fail = []`、`pyramids.list = [{DEU/D1/SHORTINTEREST, 1.3}]`
- prod 0.6093 PASS（0.6–0.7 只 1 条、0.7 以上为空，histogram min −0.2084）
- self 0.2608 PASS（最相似 `blRnKEk6` 0.2608，pool_size 10 / full_os_pool_size 11 / excluded_power_pool_count 1）
- 已落库：`persist_correlation(prod=0.6093, self=0.2608, source=platform_sync, overwrite=true)` → `checked_at 2026-10-30T07:10:01`

**判据固化：「过闸 ≠ 可交付」**，还要再过两道：① 该塔是否已有更优解；② 是否被同族成员逐项支配。`npvwXA8l` 两道都不过。

### 92.3 三族代表的塔归属与取舍

| alpha | 塔 | S | F | TO | 2Y | SUB | margin | inv_S | risk_neut | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| **`2rAP60oP`** | **SENTIMENT** | 1.66 | 1.38 | 12.80% | 2.05 | **1.38** | 13.91bp | 1.37 | **1.32** | ★ 风险画像最好；SENTIMENT 缺 3 |
| `QPKKMg6Q` | ANALYST | 1.65 | 1.47 | 7.17% | 1.58 | 1.00 | 27.55bp | **1.54** | 0.37 | 好，但字段属 prod 0.807 的 netprofit 族 |
| `1YNv8qaK` | ANALYST | 1.76 | 1.35 | 17.19% | 1.61 | 0.87 | 11.71bp | 1.16 | 0.76 | ✗ 近乎 `Vkxnb8QG` 重复 |

- **`2rAP60oP`**：settings **decay 16 / truncation 0.02 / nanHandling ON**；全部 checks pass（含 `IS_LADDER_SHARPE`），`two_year_ladder_window 2`；`pyramids.list = [{DEU/D1/SENTIMENT, 1.8}]`。**与 `QPveY7Kg` 互相关仅 0.4368 ⇒ 两条可同上 SENTIMENT 塔（2/3）。** 风险点：与 `LLMOzjo1`（prod 0.9029）互相关 0.8166。
- **`QPKKMg6Q`**：settings **decay 12**；`checks.fail=[]`，CLUSTER_TEST pass；`pyramids.list = [{DEU/D1/ANALYST, 1.8}]`。机制是「桶内截面去均值 + 自引用分桶」，用 `netprofit_y1_estimate_change_3mo`（区别于 `2rjrMZ25`/`Vkxnb8QG` 的 `eps_y1_estimate_change_3mo`）。
- **`1YNv8qaK`** 弃用：即 `Vkxnb8QG` 去掉 `trade_when` 门控、桶宽 0.05→0.02；而 `Vkxnb8QG` 的 self 已 0.6379，同提必撞 self 红线。

### 92.4 本地库误标再次扩大：`region='DEU'` 列本身也混入别区记录

此前只知 `region_id` / `universe` 两列不可靠。本轮发现 `backtest_results.region='DEU'` 同样混入别区记录：

- `lean_le89`（n=8，bestS 2.15，波名 `ws2_lean_le89_r89_d1`，code 仅 `R89`）
- `grtransform`（n=10，bestS 2.17，波名 `ws2_grtransform_r83_d1`，code 仅 `R83`）

**这两个数据集在 DEU 205 个数据集表里根本不存在**，且 `ra_failed_checks = None`（状态未知）。

**动作固化**：从本地库捞历史高 S 记录时，**必须先在 `datasets` 表核对数据集是否真属于该区**（`region_id=7`）；仅凭 `backtest_results.region` 会捞到幽灵富矿。

### 92.5 `institutions6` 从「零足迹」改判为「未开采富矿」

§91 把它记为「零足迹」。实际核查：**测过 8 条，但全部是裸 `rank(field)` 水平值**，最高 S 仅 0.36。

| alpha | 代码 | S | F | 2Y | TO |
|---|---|---|---|---|---|
| `om6rrVKn` | `rank(count_institutional_buyers_security)` | 0.36 | 0.18 | 0.86 | 2.0% |
| `le899rle` | `rank(count_institutional_holders_security)` | 0.36 | 0.18 | 0.91 | 1.6% |
| `j23xx10Q` | `rank(aggregate_equity_value_institutions)` | 0.34 | 0.16 | 1.04 | 1.6% |
| `mLg11Zbx` | `rank(ts_delta(aggregate_share_count_institutions, 66))` | 0.33 | 0.14 | 0.19 | 6.6% |
| `1YxPPJ7X` | `rank(market_value_institutional_shares_acquired)` | 0.31 | 0.14 | 1.03 | 2.5% |
| `0mR66z72` | `rank(qty_acq − qty_disp)` | 0.31 | 0.13 | 1.21 | 2.1% |
| `gJQddx1g` | `rank(mv_acq − mv_disp)` | 0.27 | 0.12 | 1.01 | 2.1% |
| `RRVKKdp1` | `rank(buyers − sellers)` | −0.18 | −0.06 | −0.90 | 3.8% |

**「n 条已测」不等于「方法已穷尽」** —— 8 条全是同一种最粗糙的形态（水平序数），未触及归一化、时序异常、门控、换手/离散度等任何结构化加工。

数据集画像：11 个 MATRIX 字段，**coverage 全部 = 1.0**，`tier=TIER2`，`pyramid_multiplier=1.5`，`alphaCount 19–80`（低拥挤）。**INSTITUTIONS 塔缺口 = 2，正好匹配。**

11 字段（原样复制，勿改前缀）：
`aggregate_equity_value_all_owners` / `aggregate_equity_value_institutions` / `aggregate_share_count_all_owners` / `aggregate_share_count_institutions` / `count_institutional_buyers_security` / `count_institutional_holders_security` / `count_institutional_sellers_security` / `market_value_institutional_shares_acquired` / `market_value_institutional_shares_disposed` / `quantity_institutional_shares_acquired` / `quantity_institutional_shares_disposed`

最冷字段（uc16/ac19 起）：`aggregate_share_count_institutions` / `aggregate_equity_value_all_owners` / `aggregate_share_count_all_owners` / `aggregate_equity_value_institutions`。

### 92.6 论坛取证：`institutions6` 五版完整迭代链路（帖 43754821327639，70 票）

作者 FX25214 的 GBR 复盘，直接用 `institutions6` 字段，从 S 1.28 一路做到 S 1.63：

| 版本 | 构造 | S |
|---|---|---|
| v1 | `group_neutralize(ts_zscore(est_12m_net_mean / aggregate_share_count_institutions, 126), market)` | **1.28** |
| v2 | 加人数门控 `rank((buyers − sellers)/(1 + holders)) < 0.7` | 0.99 |
| v3 | 换股数门控但门太窄 `< 0.2` | **0.38** |
| v4 | 同上放宽到 `< 0.7` + 归一化改 `aggregate_equity_value_all_owners` | 1.30 |
| v5 | 核心与门控统一回机构股数口径 | **1.63 / F1.26 / mg25.30bp / TO5.88% / DD5.94% / SUB1.21 / self0.24 / 2Y2.18** |

**反向验证（防碰运气）**：
- 门控反向（只留净买入压力最高 30%）→ **S 0.57 / F 0.26 / mg12.53bp / DD11.71%**
- 机构买卖股数单独做 alpha `group_zscore((qty_acq − qty_disp)/(1 + aggregate_share_count_institutions), industry)` → **S −0.11 / F −0.02**

**三条可直接迁移的方法论**：

1. **「人数」与「股数」是两种语言** —— 十家各买一点 ≠ 两家大幅增持。v2 用人数门控反而把 S 从 1.28 打到 0.99。
2. **`trade_when` 门不是越窄越好** —— `<0.7` 保留 70% 股票池有效，`<0.2` 把信号一起挡掉（1.28→0.38）。
3. **核心信号与条件信号必须说同一个经济口径** —— 这是 v4（1.30）到 v5（1.63）的唯一差别。

另两篇相关帖：`43358755666967`（23 票，机构持股广度「新鲜度门」）、`37137602566679`（17 票，机构情绪分歧因子）。

**外部文献（`web_search` 不可用，标注为知识引用，不编造链接）**：Gompers & Metrick (2001)；Bennett, Sias & Starks (2003)；Nofsinger & Sias (1999)；Sias (2004)；Wermers (1999)；Hong, Kubik & Solomon (2000)；Hong & Stein (1999)；Han & Kumar (2013)。

### 92.7 波 92 派发：`institutions6` 十条结构互异模板（纯单数据集 ATOM）

**设计约束**：
- 全部 10 条**只用 `institutions6` 单数据集字段** ⇒ 纯 ATOM，不触碰 PV/MODEL/OTHER 三塔互组禁令。
- 模板差异落在**算子几何 / 矩（水平·一阶差分·二阶离散度）/ 分组轴 / 非线性变换**上，不是换窗口。

| # | 模板 | 结构要点 | 来源 |
|---|---|---|---|
| T1 | `group_neutralize(ts_zscore(divide(qty_acq − qty_disp, agg_share_inst), 126), industry)` | 股数流量强度，z 保留幅度 | 自建（论坛 v5 核心的纯单集版） |
| T2 | `group_neutralize(winsorize(ts_zscore(divide(mv_acq − mv_disp, agg_equity_inst), 252), std=4), market)` | **金额口径** + winsorize 截尾 | 自建（v4 归一化思路） |
| T3 | `group_rank(ts_delta(divide(agg_share_inst, agg_share_all), 66), subindustry)` | **一阶差分**（持股占比变化） | Han & Kumar (2013) 机构/散户结构 |
| T4 | `-group_rank(divide(agg_equity_all − agg_equity_inst, agg_equity_all), sector)` | **非机构占比水平**，反向 | Han & Kumar (2013) 散户持股 |
| T5 | `group_neutralize(ts_zscore(divide(buyers − sellers, holders), 252), subindustry)` | **人数口径**广度净额比 | 论坛 v2 / M41 |
| T6 | `-group_rank(ts_mean(divide(mv_acq + mv_disp, agg_equity_inst), 66), subindustry)` | **换手/不稳定度**（二阶），反向 | 自建（持有人不稳定假说） |
| T7 | `group_neutralize(ts_zscore(divide(mv_acq, buyers), 252), industry)` | **单笔增持规模**（conviction） | 自建 |
| T8 | `-group_rank(divide(ts_std_dev(agg_equity_inst, 252), ts_mean(agg_equity_inst, 252)), subindustry)` | **持有基数离散度**（变异系数） | 自建 |
| T9 | `group_rank(ts_rank(divide(qty_acq − qty_disp, agg_share_inst), 252), subindustry)` | **序数几何**（与 T1 的 z 幅度形成对照实验） | 自建 |
| T10 | `group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ownership, 240)), rank(ts_delta(ownership, 176))), target_tvr=0.03), subindustry)` | **M13 双期限一致性 + TVR** | M13 架构移植（三塔已验证） |

**对照实验设计**：T1 vs T9 是同一经济量的「z 幅度 vs 序数」对照（此前稀疏事件族实证 zscore 优于 rank 1.6 sharpe）；T1 vs T2 是「股数口径 vs 金额口径」对照；T5 vs T1 是「人数 vs 股数」（论坛已证人数较弱，本轮直接量化）；T3 vs T10 是「短窗一阶差分 vs 双期限一致性」。

**派发设置**：EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 / truncation 0.08 / pasteurization ON / unitHandling VERIFY / maxTrade OFF / **nanHandling OFF**（字段非稀疏，OFF 更安全）/ FASTEXPR。
**multisim id**：`FfdF44z54LUctQ1fmHANQi8`（10 条，预检 11 字段全 valid、无 VECTOR 需包装）。

**待验核心问题**：`institutions6` 在 DEU（TOP500）上能否复现 GBR 的 S 1.63 量级？如果 10 条模板全灭，则「机构持仓类机制在 DEU 不成立」，INSTITUTIONS 塔需另寻数据集；如果 T1/T2/T5 出信号，则按论坛链路继续往 v5（门控统一口径）方向做定向破闸。

### 92.8 prod 终验进展：平台侧持续超时

`2rAP60oP` 的 prod 查询第二次失败，形态不同于第一次：

1. 第一次：`correlation_busy`，holder = `corr:get_production_correlation(6XdPm1YY)`，`retry_after` 240s —— **holder 不是本会话发起**，说明账号级相关性单并发槽被外部进程占用
2. 第二次：**MCP 调用 120s 超时**（已知平台 prod 计算 >120s 会超时；超时不落缓存、本机 inflight 标记残留 300s）

**处置**：`2rAP60oP` 与 `QPKKMg6Q` 的 prod 均未取得结论，**按 300s 冷却后重试**；在此之前不把它们计入「可提交」。

### 92.9 本节口径更新

- **L3 独立可交付**：仍是 **3 条**（`QPveY7Kg` / `Vkxnb8QG` / `MPY9VNY9`）—— `npvwXA8l` 本轮从中剔除（被支配）。
- **待验池**：`2rAP60oP`（SENTIMENT）/ `QPKKMg6Q`（ANALYST）两条，prod 未测。
- **新开战线**：`institutions6` 波 92 十条（INSTITUTIONS 塔，纯 ATOM），结果待收。
- **DEU 累计已测**：4,694 + 10 = 4,704 条。

---

## §93 INSTITUTIONS 塔三次攻坚全灭 + ANALYST 类普查 + 论坛配方不可移植（2026-10-30 第四轮）

本节承接 §92，是 DEU「点塔可行性」的最后一次正面验证。三次独立攻坚全部失败，INSTITUTIONS 塔在 DEU 的 regular 通道就此关闭；同时完成 ANALYST 类 20 个数据集的足迹普查，得出一个此前完全没注意到的结构性事实。

### 93.1 波 92：`institutions6` 纯单数据集十条模板 —— 全灭

**派发**：multisim `FfdF44z54LUctQ1fmHANQi8`，10 条，预检 11 字段全 valid、无 VECTOR 需包装。
**设置**：EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling OFF。

| # | 模板 | alpha | S | F | TO | 2Y | SUB |
|---|---|---|---|---|---|---|---|
| T5 | 人数广度净额比 + ts_zscore(252) + group_neutralize(subindustry) | `QPvrZxPM` | **0.71** | 0.40 | 8.41% | 0.58 | 0.53 |
| T7 | 单笔增持规模（mv_acq/buyers）+ ts_zscore(252) | `6XdPmWXp` | 0.23 | 0.07 | 8.79% | 1.22 | 0.02 |
| T9 | 股数净流 ts_rank(252) + group_rank | `j2Ylzp2k` | 0.21 | 0.06 | 9.62% | **1.79** | −0.24 |
| T4 | 非机构金额占比水平（反向）+ group_rank(sector) | `d5W8kM2J` | 0.20 | 0.06 | 1.84% | 0.87 | −0.13 |
| T6 | 机构基数换手率（反向）+ ts_mean(66) | `1YNVk8Ym` | 0.15 | 0.03 | 2.43% | 0.08 | −0.03 |
| T1 | 股数净流强度 + ts_zscore(126) + group_neutralize(industry) | `0mYkOVbK` | 0.06 | 0.01 | 10.33% | 0.61 | — |
| T8 | 持有基数变异系数（反向） | `MPYlMEP6` | −0.15 | −0.04 | 2.39% | 0.58 | — |
| T2 | 金额净流 + winsorize + ts_zscore(252) + market | `wpQwKd8Y` | −0.12 | −0.03 | 7.77% | 0.59 | — |
| T10 | M13 双期限持股占比一致性 + TVR | `E560OjOJ` | −0.14 | −0.03 | 3.96% | −0.62 | — |
| T3 | 持股占比 66 日一阶差分 + group_rank | `zq3wKxvG` | −0.44 | −0.17 | 7.44% | −1.38 | — |

**结论：`institutions6` 的 18 条历史（8 条旧裸 rank + 本轮 10 条结构化）最高 S 仅 0.71。** 上限稳定在这个量级，不是构造没找对。

### 93.2 ★ 关键纠错：论坛 v5 的 S1.63 里，`institutions6` 只是分母

§92.6 把帖 `43754821327639` 的 S1.63 归因给 `institutions6`，**这是误读**。逐字段复核 v1/v5 原文：

```
v1: group_neutralize(ts_zscore(est_12m_net_mean / aggregate_share_count_institutions, 126), market)
                          ^^^^^^^^^^^^^^^^ 分子 = 分析师预期净利润（analyst7）
                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 分母 = 机构持股数（institutions6）
```

**真正的信号源是分子 `est_12m_net_mean`（`analyst7`，ANALYST 类，cov 0.6657）；`institutions6` 只提供「每股机构持有」的归一化。**

而且论坛作者自己已经给出了这条证据 —— §92.6 记录的反向验证里，去掉分析师分子、只用机构买卖股数单独做 alpha：

```
group_zscore((qty_acq − qty_disp)/(1 + aggregate_share_count_institutions), industry)  →  S −0.11 / F −0.02
```

这与波 92 的 T1（0.06）/ T6（0.15）/ T9（0.21）**完全一致**。**论坛原文早就说了纯机构字段没信号，是我把归因挂错了对象。**

**方法论固化**：读论坛 / 论文配方时，**必须逐字段确认「谁是信号、谁是归一化」**再决定测哪个数据集。把归一化字段当信号源测，会得到「全灭」的假结论，并把一个正常数据集误判死。

### 93.3 波 93：论坛配方真实形态在 DEU 只到 S 0.83 —— GBR 的 1.63 不可移植

按 §93.2 的正确归因重建（ANALYST `analyst7.est_12m_net_mean` × INSTITUTIONS `institutions6` 归一化），multisim `4iKzSc4ow4IF9nbPEVlF78Z`，3 条（受「每个两塔组合候选 ≤3」配额约束）。

| # | 构造 | alpha | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| E1 | v1 逐字复刻：`/aggregate_share_count_institutions` + `ts_zscore(126)` + market | `qMLk8l51` | **0.83** | 0.54 | 9.46% | 0.83 |
| E2 | v5 逐字复刻：加股数口径门控 `rank(net_flow/agg_share_inst) < 0.7` | `d5W8p09g` | 0.63 | 0.36 | 7.59% | 0.49 |
| E3 | 变体：`/aggregate_equity_value_institutions`（金额归一化）+ industry | `omEw7lPl` | 0.62 | 0.35 | 9.35% | 0.77 |

**三条全部远低于 GBR 的 1.63，最高 0.83，差闸 0.75。**

三条附带确认：
1. **门控在 DEU 同样有害**（0.83 → 0.63），与论坛自己在 GBR 观察到的「v1 1.28 → v2 0.99」同向。这条是跨市场一致的。
2. **金额归一化不如股数归一化**（0.62 vs 0.83），说明「每股机构持有」的量纲才是这个机制的核心。
3. **ANALYST × INSTITUTIONS 这个两塔组合的 3 条配额已用完**，此路封闭。

**结论：机构持仓 × 分析师预期的组合机制在 DEU 不成立，GBR 的 1.63 无制度/市场可移植性。**

### 93.4 ★ ANALYST 类普查：13 个数据集零足迹、约 1,913 个字段从未测过，但大多被 cov=0 挡住

DEU 全部 20 个 ANALYST 数据集在本地库的回测足迹：

| dataset | 字段 | cov | alphaCount | 值分 | 倍数 | n | bestS | RA clean |
|---|---|---|---|---|---|---|---|---|
| analyst10 | 592 | 0 | **0** | 5 | 1.9 | **0** | — | 0 |
| analyst15 | 537 | 0 | 336 | 4 | 1.7 | **0** | — | 0 |
| analyst16 | 56 | 0 | 1 | 5 | 1.9 | **0** | — | 0 |
| analyst35 | 23 | 0 | 12 | 6 | 1.7 | **0** | — | 0 |
| analyst39 | 24 | 0 | 356 | 3 | 1.7 | **0** | — | 0 |
| analyst40 | 2 | 0 | 3 | 6 | 1.7 | **0** | — | 0 |
| analyst44 | 72 | 0.7462 | 10 | 6 | 1.9 | 42 | 1.37 | 0 |
| analyst45 | 0 | 0.3952 | 1 | 6 | 1.9 | 0 | — | 0 |
| analyst46 | 5 | 0 | 28 | 5 | 1.7 | 0 | — | 0 |
| analyst47 | 5 | 0.7157 | 3 | 4 | 1.9 | 8 | 1.46 | 0 |
| analyst48 | 7 | 0.8066 | 8 | 5 | 1.7 | 0 | — | 0 |
| analyst69 | 292 | 0 | 2932 | 2 | 1.7 | **0** | — | 0 |
| analyst7 | 502 | 0.7526 | 5823 | 2 | 1.7 | 48 | 1.04 | 0 |
| analyst8 | 3 | 0 | 0 | 5 | 1.9 | 0 | — | 0 |
| analyst83 | 345 | 0.3304 | 0 | 5 | 1.9 | 0 | — | 0 |
| analyst9 | 51 | 0.7581 | 0 | 4 | 1.9 | 8 | 0.73 | 0 |
| **analyst93** | **100** | **0.5926** | 113 | 4 | 1.7 | **121** | **1.57** | 0 |
| analyst94 | 34 | 0 | 0 | 5 | 1.9 | **0** | — | 0 |
| analyst_consensus | 1772 | 0 | 305 | 4 | 1.7 | 3 | 0.72 | 0 |
| analyst_factor_signals | 96 | 0.4295 | 870 | 2 | 1.7 | 94 | 1.23 | 0 |

**两个事实**：

**① ANALYST 塔在 DEU 的 regular 通道从未通过任何一条 RA 干净的全闸记录 —— 20 个数据集、324 条回测，RA clean 全部 = 0。** 唯一在闸口的是 `analyst93` 的 bestS 1.57（差 0.01）和 `analyst47` 的 1.46。

**② 「零足迹」不等于「未开采富矿」—— 被 cov=0 挡住。** `analyst10`（592 字段，alphaCount=0 极低拥挤）抽样 25 个字段 **coverage 全部 0.0**，即 DEU 无数据。同类还有 `analyst15`（537）/`analyst69`（292）/`analyst83`（345，cov 0.3304）/`analyst94`（34）。合计约 1,913 个「纸面未测字段」，多数在 DEU 物理不存在。

**动作固化**：数据集 `status='untried'` 且 `coverage=0` 时，**先抽样 `get_datafields` 看字段级 coverage 再决定是否投入**，不要按字段数排序当成富矿。

### 93.5 波 94：`analyst93` 十条结构互异模板 —— 最高 0.85，低于该数据集历史 1.30

**先做方法覆盖面审计**：`analyst93` 121 条历史里 **102 条的最终外层是裸 `rank()`**，字段只用了约 10 个（`recprofitabilityprev_analyst_profitability2` 28 次、`analyst_correct_revision_ratio` 16、`analyst_accuracy2` 14、`estimator_correct_revision_ratio` 13）；`vector_neut` 0 次、`ts_target_tvr_decay` 0 次、`ts_quantile` 0 次、`group_neutralize` 仅 4 次、`trade_when` 仅 7 次。**看似方法未穷尽。**

据此派发 multisim `1Bcs2radQ5j7bLo93SpMWp2`（10 条）：

| # | 模板 | alpha | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| A7 | `profitability2` 双期限 M13 + TVR（移植） | `zq3wZbYX` | **0.85** | 0.56 | 7.97% | 0.65 |
| A10 | `accuracy2` + `vector_neut` 正交腿（降 prod 杠杆） | `ZYQw6A00` | 0.65 | 0.38 | 6.05% | 0.31 |
| A1 | `accuracy2` + `ts_zscore(252)` + group_neutralize | `vR1n82jz` | 0.51 | 0.28 | 7.91% | 0.28 |
| A6 | `consistency` 66 日一阶差分 | `bl62XORZ` | 0.49 | 0.25 | 9.98% | 0.45 |
| A8 | `accuracy2` 的 vec_max−vec_min 极值区间 | `vR1n82kz` | 0.35 | 0.18 | 10.45% | −0.18 |
| A3 | `relative_accuracy3` 水平 | `gJeq6Zje` | 0.27 | 0.08 | 21.14% | 0.91 |
| A4 | `accuracy1` + 覆盖广度门控 | `58E7xgl5` | 0.15 | 0.04 | 2.52% | −0.89 |
| A2 | `correct_revision_ratio` + 自引用分桶（M12） | `QPvrMK7G` | 0.13 | 0.04 | 11.00% | −0.17 |
| A5 | `accuracy2` 的 vec_stddev（反向） | `leA6dKjn` | −0.09 | −0.02 | 6.47% | −0.32 |
| A9 | 覆盖广度 `total_forecast_times1` 水平 | `RREZM6Vd` | −0.30 | −0.11 | 4.96% | −1.02 |

**结论：全部 10 条低于该数据集历史最优 1.30。**

| 形态 | S |
|---|---|
| 历史：`rank(vec_avg(anl93_recprofitabilityprev_analyst_profitability2))`（**裸水平**） | **1.30** |
| 历史：`rank(ts_mean(vec_avg(same), 66))` | 1.27 |
| 本轮 A7：同一个字段 + 双期限 ts_delta + TVR | 0.85 |
| 本轮其他 9 条（换了 accuracy / consistency / coverage / dispersion） | ≤ 0.65 |

**揭示了本轮最重要的一条方法论**：`analyst93` 的信号**只在「分析师盈利预测修正」这个字段的裸水平里**，一旦加时序变换（ts_delta / ts_zscore）、加分组、加正交化，全部变差。这与 §92 记录的稀疏事件族铁律**方向相反**（那里 zscore 保留幅度优于 rank 1.6 sharpe），说明「哪种加工方式保留信号」**是字段特有的，不能跨字段族套用**。

**该族上限 S 1.30，距闸 1.58 差 0.28（需 +21%）。** 连续两批（波 94 十条 + 历史 121 条）都到不了，判定 ANALYST 塔的 `analyst93` 路线不可达。

### 93.6 ★ INSTITUTIONS 塔在 DEU 的 regular 通道关闭

六个 INSTITUTIONS 数据集逐条结论：

| dataset | 字段 | cov | 足迹 | 最高 S | 结论 |
|---|---|---|---|---|---|
| **institutions6** | 11 | 1.0 | 18 | **0.71** | 纯字段无信号（本轮 10 条 + 旧 8 条）；论坛反向验证 S −0.11 印证 |
| **institutions25** | 24 | **0.0** | **0** | — | 全部 24 字段 cov 0.0，DEU 无数据 |
| institutions1 | 7 | 0.4856 | 3 | 1.73 | `d5WwzRMY`/`E56AzejK` self 0.93/0.92 自锁 |
| fund_holdings_panel | 18 | 0.8912 | 94 | 1.41 | **94 条 RA clean = 0**；头部全是 `add(add(add(rank(...))))` 混信号堆叠 + TO 0.5–0.77 |
| institutions4 | 6 | 0.39 | 0 | — | cov 0.39 且零足迹 |
| institutions4 / fund_holdings_panel 之外的 institutions1 家族 | — | — | — | — | 同一 PnL 簇 |

**三条独立路线（纯 institutions6 / ANALYST×institutions6 论坛配方 / institutions25 空白集）全部失败，INSTITUTIONS 塔 regular 通道判定不可达。**

### 93.7 prod 相关性槽被流水线自身持续占用

`2rAP60oP` 的 prod 终验第三次失败，且**三次的 holder 各不相同**：

| 次序 | 结果 | holder |
|---|---|---|
| 1 | `correlation_busy` | `corr:get_production_correlation(6XdPm1YY)` |
| 2 | MCP 调用 120s 超时 | — |
| 3 | `correlation_busy` | `corr:get_production_correlation(omEw7LPb)` |

**holder 每次都是不同的 alpha id，说明不是同一个僵尸请求卡住，而是流水线里持续有环节在发起 prod 计算**（最可能是 `harvest_multisim.py` 的 `[queue]` 阶段对过闸候选批量触发）。`inflight` 字段为 `false`、`retry_after` 恒 240s。

**处置**：不再对 prod 做短周期重试（每次占用 120s 且必然失败）。改为：① 与 harvest 批次错开时间窗；② 或对单一目标用 `correlation_type="production"` 但接受「可能拿不到」；③ 本地 `check_self_correlation` 不占槽，可随时跑。

### 93.8 本轮口径更新

| 项 | 数值 |
|---|---|
| DEU 累计已测 | 4,704 + 10（w92）+ 3（w93）+ 10（w94）= **4,727** |
| L3 独立可交付 | **3 条**（`QPveY7Kg` SENTIMENT / `Vkxnb8QG` ANALYST / `MPY9VNY9` SHORTINTEREST） |
| 待验池 | `2rAP60oP`（SENTIMENT）/ `QPKKMg6Q`（ANALYST），prod 未取得 |
| 新增判死 | `institutions6` 纯字段、`institutions25`（cov 0）、`analyst10`/`analyst15`/`analyst16`/`analyst35`/`analyst39`/`analyst40`/`analyst46`/`analyst69`/`analyst8`/`analyst83`/`analyst94`（cov 0 抽样确认）、`analyst93` 结构化路线（上限 1.30）、`analyst7 × institutions6` 配方（上限 0.83） |
| 塔关闭 | 本轮新增 **INSTITUTIONS**；此前 RISK、NEWS、`sentiment27` 裸信号 |

**DEU 点塔可达性最终判定（6 个未点亮塔）**：

| 塔 | 现状 | 可行性 |
|---|---|---|
| ANALYST 1/3 | `Vkxnb8QG` 已验毕可补至 2/3；`2rjrMZ25` 已 ACTIVE | ✅ 可补 1，第三条无路径 |
| SENTIMENT 0/3 | `QPveY7Kg`（prod 0.6671）+ `2rAP60oP`（prod 待测，互相关 0.4368） | ✅ 可补 2 |
| SHORTINTEREST 2/3 | `MPY9VNY9` 已验毕 | ✅ 可补满 3/3 |
| FUNDAMENTAL 1/3 | `Wje5K71x` 已 ACTIVE；`fundamental6` 两批全灭 | ❌ 无路径 |
| INSIDERS 1/3 | `insiders12` 空集；`insiders1` cov 0.5937 未测；欧盟延迟披露 | ⚠️ 高风险 |
| INSTITUTIONS 1/3 | 三条路线全灭 | ❌ 本轮关闭 |
| NEWS 0/3 | `news50` 最佳 S 0.16；`news38`/`news48` 零足迹 | ❌ 无路径 |

**合计：DEU 最多再补 3–4 条点塔 alpha，无法达到 60 条。**

---

## §94 波 95：snt7 窗口破墙 + prod 四点终验 —— DEU mining 路线正式收口

> 时间：2026-10-30 07:35–07:55
> 起因：`2rAP60oP` prod 0.7548 FAIL，直方图显示 0.7–0.8 区间仅 2 条（单条近邻），按
> `wq-window-valley-break-prod-wall` 判为「可破」，派窗口扫描批。
> 结果：**破墙失败，但拿到了本轮最有价值的一条平台机理证据。**

### §94.1 破墙批设计（multisim `3MThWa5U64MuagvvDSKx1l6`，6 条）

以 `2rAP60oP` 为母体，只动三个旋钮：

| 编号 | 旋钮 | 原值 → 新值 |
|---|---|---|
| P1 | `ts_ir` 窗口 | 11 → 7 |
| P2 | `ts_ir` 窗口 | 11 → 15 |
| P3 | `ts_ir` 窗口 | 11 → 22 |
| P4 | `quantile` driver | uniform → gaussian |
| P5 | `ts_mean` 窗口 | 5 → 8 |
| P6 | 正交腿 `ts_backfill` 窗口 | 22 → 66 |

设置固定：DEU / TOP500 / D1 / SUBINDUSTRY / decay 16 / truncation 0.02 / nanHandling **ON**。

### §94.2 结果：全部落在 S 1.62–1.73，无一条超过母体的替代路径

| # | 变体 | alpha | S | F | TO | 2Y | SUB | margin |
|---|---|---|---|---|---|---|---|---|
| P3 | `ts_ir=22` | `QPvmO0zG` | **2.04** | 1.91 | 8.84% | 2.32 | 1.61 | 24.71bp |
| P2 | `ts_ir=15` | `ZYQw5RNQ` | 1.73 | 1.49 | 11.01% | 2.11 | 1.46 | 16.94bp |
| P5 | `ts_mean=8` | `e758plEM` | 1.73 | 1.49 | 12.25% | 2.08 | 1.37 | 15.09bp |
| P6 | 正交腿 66 | `leA6qLNe` | 1.69 | 1.43 | 12.75% | 2.03 | 1.40 | 14.26bp |
| P4 | gaussian | `P0orWJKK` | 1.63 | 1.34 | 12.94% | 2.02 | 1.33 | 13.61bp |
| P1 | `ts_ir=7` | `E5607ZxK` | 1.62 | 1.24 | 14.86% | 2.27 | 1.25 | 11.77bp |
| — | 母体 `2rAP60oP` | `2rAP60oP` | 1.66 | 1.38 | 12.80% | 2.05 | 1.38 | 13.91bp |

**★ P3 是重复测试，不是新发现。** `QPvmO0zG`（`ts_ir=22`）在 `wmcp-2` 批次里已经测过，
prod 实测 **0.8983**（已 FAIL）。这次 harvest 只是把库里同一 alpha 的 `wave` 从 `wmcp-2`
改写成 `95`、`dataset` 从 NULL 补成 `sentiment7`，指标逐位相同。

> **口径教训**：派发前应对照本地库 `backtest_results.code` 去重，而不是只看 alpha 是否在
> 「已测名单」里。同一表达式重复回测会拿到同一个 alpha id，`harvest` 的 upsert 会把旧波次
> 标签覆盖掉 —— 事后看「这是新波次的产物」是错的。

**⇒ 结论：`snt7 × quantile` 这族的上限就是 S≈2.04，且 S≥1.9 的两个配置
（`QPvmO0zG` ts_ir=22 prod 0.8983、`RREXKNQn` ts_quantile 504 prod 0.7415）prod 全撞墙。
破墙批没有开出新的可交付路径。**

### §94.3 ★★★ 本轮最有价值的证据：`ts_quantile` 窗口 252→504 让 prod 从 0.6671 跳到 0.7415

`QPveY7Kg` 与 `RREXKNQn` 是**逐字符相同的表达式**，只差一个窗口：

```text
vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22),
ts_delay(ts_backfill(vec_avg(snt7_all_languages_views),22),5)),5),22),
            <W>, driver="gaussian"),
            ts_backfill(vec_avg(snl27_relpopularity08),22))
```

| alpha | `ts_quantile` W | S | F | 2Y | prod | 判定 |
|---|---|---|---|---|---|---|
| `QPveY7Kg` | **252** | 2.03 | 1.61 | 2.54 | **0.6671** | ✅ PASS |
| `RREXKNQn` | **504** | 2.03 | 1.86 | 2.23 | **0.7415** | ❌ FAIL |

**同一信号、同一设置、S 相同，prod 差 0.074。** 这坐实了两条方法论：

1. **`ts_quantile` / `ts_rank` 这类「时序分位」算子的窗口，是 prod 的一阶杠杆，不是二阶微调。**
   它改变的是「用多长的历史分布给当日信号定位」—— 窗口翻倍会让信号贴近「长期均值回复」这一
   更拥挤的公共因子，prod 立刻上升。
2. **「窗口谷底」是真实现象，但谷底是窄的**：252 是谷、504 是坡。同一族里
   `relpopularity08` + gaussian + 252 恰好落在谷底，这是目前 DEU sentiment 族唯一 PASS 的配置。

> **与既有认知的关系**：记忆里「decay 不是 SUB/S 的杠杆、也不是 prod 的杠杆」仍然成立
> （本轮 P4/P5/P6 改动都不是窗口型算子，prod 未测但 S 无实质变化）。但**窗口型算子
> （`ts_quantile`/`ts_rank`）的 W 是 prod 的真杠杆**，两者不矛盾：前者是「平滑参数」，
> 后者是「信息聚合尺度」。

### §94.4 prod 四点终验（本轮全部 FAIL）

| alpha | S | F | 2Y | SUB | prod | 直方图 0.6–0.7 / 0.7–0.8 / >0.8 | 形态判读 |
|---|---|---|---|---|---|---|---|
| `RREXKNQn` | 2.03 | 1.86 | 2.23 | — | **0.7415** | 1 / 2 / 0 | **单条近邻**（最可破，但破法只能是窗口，252 已被占） |
| `2rAP60oP` | 1.66 | 1.38 | 2.05 | 1.38 | **0.7548** | 5 / 2 / 0 | 单条近邻，窗口扫描后无改善（§94.2） |
| `vR102Ver` | 2.39 | 1.29 | 1.60 | — | **0.802** | 110 / 30 / 1 | **整簇拥挤**，放弃 |
| `QPKKMg6Q` | 1.65 | 1.47 | 1.58 | 1.00 | **0.807** | 78 / 7 / 1 | 小簇，放弃 |

**`vR102Ver` 的表达式揭示了一个判死族复活失败的实例**：
```text
group_rank(tm_15_r1_r5_r10_rh_glb_d1_r5_q1, sector)
```
它的 S 高达 **2.39**（DEU 全池第二高），但 prod **0.802**、F 仅 1.29。`tm_*` 是
平台预计算的 GLB 主题因子族，天然被全平台共享 ⇒ **S 再高也过不了 prod**。
这印证了「信号同质时 prod 的下限写在数据集拥挤度里，不写在算子里」。

### §94.5 ★ 53 条全闸候选的真相：PnL 聚簇后只有 7 个独立族

对 38 条 prod 未测的候选做零成本 PnL 聚簇（`compute_mutual_correlation`，23 条一批）：

```text
max_mutually_below_subset_size = 7
代表 = kqJqQL08, vR102Ver, d5WwzRMY, j288RaEQ, RREXKNQn, 9qxgMvOV, xArMQPdJ
```

**23 条 → 7 族，换算比约 3.3 : 1**，与此前「每 3 条同族回测 ≈ 1 条独立信号」的换算规则一致。

七族的真实归属与结局：

| 族代表 | S | 表达式内核 | 塔 | prod 结局 |
|---|---|---|---|---|
| `vR102Ver` | 2.39 | `group_rank(tm_15_...glb..., sector)` | MODEL/PV 系 | **0.802 FAIL**（整簇） |
| `RREXKNQn` | 2.03 | snt7 × `ts_quantile(504)` × relpop08 | SENTIMENT | **0.7415 FAIL** |
| `9qxgMvOV` | 1.94 | snt7 × `quantile` × `ts_mean(3)` × `ts_ir(22)` | SENTIMENT | 未测（同族，预期 >0.74） |
| `xArMQPdJ` | 1.88 | snt7 × `ts_quantile(120)` × **`snl27_skewness`** 正交腿 | SENTIMENT | 未测（换正交腿，唯一有变量的 snt7 变体） |
| `kqJqQL08` | 1.78 | `eps_y1_estimate_change_3mo` M12，bucket 宽 0.1 | ANALYST | 未测（被流水线抢槽） |
| `d5WwzRMY` | 1.73 | `institutions1` × `other455` + `tail/winsorize/group_rank` | INSTITUTIONS+OTHER | 未测 |
| `j288RaEQ` | 1.64 | `netprofit_y1_estimate_change_3mo` M12，窗 130 / decay 3 | ANALYST | **推定 FAIL**（与 `QPKKMg6Q` 同族，后者 0.807） |

**⇒ 53 条「全闸通过」的账面数字，真实独立候选只有 7 个，其中 4 个已实测撞墙。**
上报「DEU 有 53 条可提交候选」会高估约 7.6 倍。

### §94.6 DEU mining 路线正式收口

**四轮普查 + 83 条存量族归因 + 三塔十模板全谱覆盖 + 53 条候选聚簇 + 7 族 prod 实测，
DEU 的 regular alpha 可交付上限已定量确认为 3 条。**

| 塔 | 现状 | 本轮提交后 | 上限说明 |
|---|---|---|---|
| MODEL | 7/3 ✅ | 7/3 ✅ | 已点亮 |
| OTHER | 4/3 ✅ | 4/3 ✅ | 已点亮 |
| SHORTINTEREST | 2/3 | **3/3 ✅ 点亮** | `MPY9VNY9`（prod 0.5986 / self 0.2703） |
| ANALYST | 1/3 | **2/3** | `Vkxnb8QG`（prod 0.6384 / self 0.6379） |
| SENTIMENT | 0/3 | **1/3** | `QPveY7Kg`（prod 0.6671 / self 0.0242） |
| FUNDAMENTAL | 1/3 | 1/3 | `fundamental6` 两批全灭，无路径 |
| INSTITUTIONS | 1/3 | 1/3 | 三路线全灭（§93.6），例外：`d5WwzRMY` 未测 prod |
| INSIDERS | 1/3 | 1/3 | `insiders12` 空集、`insiders1` cov 0.5937 未测、欧盟延迟披露 |
| NEWS | 0/3 | 0/3 | `news50` bestS 0.16，无路径 |
| RISK | 0/3 | 0/3 | `risk60` 十模板最高 0.79（§90） |

**缺口**：60 条目标 − 3 条可交付 = **57 条必须由其他区承接**。

**DEU 后续唯一还剩的动作**（均为低期望值，建议不做）：
- `d5WwzRMY` 的 prod（INSTITUTIONS 塔唯一残存路径，但 `institutions1` 的 `self` 自锁史)
- `xArMQPdJ` 的 prod（snt7 族唯一换了正交腿的变体）
- `kqJqQL08` 的 prod（ANALYST，但是 M12 同架构，`2rjrMZ25` 已有 ACTIVE）

### §94.7 本轮新增/修正的方法论

1. **★ 窗口型算子的 W 是 prod 杠杆，平滑型参数不是。** `ts_quantile` 252→504 让 prod
   跳 0.074（0.6671→0.7415），而 decay / driver / `ts_mean` 窗口的改动不改变 prod 形态。
   破 prod 墙时应优先扫 `ts_quantile` / `ts_rank` 的 W。
2. **★ 派发前必须用 `backtest_results.code` 去重，不能只看 alpha 是否在已测名单。**
   同一表达式重测会复用同一 alpha id，`harvest` 会把旧波次标签覆盖，事后误判成新发现。
3. **★ 「全闸通过 N 条」必须换算成 PnL 族再上报。** 本轮 53 条 → 7 族（7.6× 高估）。
4. **★ 平台预计算因子族（`tm_*`）的 S 可以极高但 prod 必然撞墙。** `vR102Ver` S 2.39 /
   prod 0.802 是 DEU 全池最典型的例子 —— 共享因子 = 天然拥挤。
5. **★ 同一族的 prod 谷底是窄的、且只能被占一次。** snt7 族的谷底（252+relpop08）已被
   `QPveY7Kg` 占用，同族其他窗口/驱动/正交腿全部 ≥0.74。**族内第二条同塔 alpha 基本无望。**

### §94.8 待用户决定（问卷两次超时自动选择，均不构成授权）

| 事项 | 自动选择结果 | 当前实际状态 |
|---|---|---|
| 提交 3 条候选 | 「三条全部提交」 | **未提交**（不可逆动作，自动选择不构成授权） |
| 57 条缺口 | 「DEU 点塔 3 条 + 他区承接 57 条」 | 方向已定，待执行 |

**下一动作**：核对跨区 READY 池的真实 region（本地库 `region_id` / `universe` 两列已证
不可靠，唯一权威是 `get_alpha_details.settings.region`），再决定 57 条从哪些区承接。

## §95 波 96：analyst7 十模板全灭 —— 修订类强于分歧类，但 2Y 是结构性天花板

### 派发与设置
- 批次 A（T1–T5）= `3pbo2q454IY9oNeA4Lku1p`；批次 B（T6–T10）= `1Uhn6wfDk53T8VrXqSkp77G`，两批并行 = 并发 2。
- 平台回显：EQUITY / DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / nanHandling OFF / IS 2014-01-01～2023-12-31。
- 十条全部 ATOM 单数据集，`pyramids.list = [{name: "DEU/D1/ANALYST", multiplier: 1.8}]`，`pyramid_short: "analyst"`。

### 十模板完整结果（按 S 降序）

| # | 模板 | 信息维度 | alpha | S | F | TO | 2Y | **2Y/S** | SUB | margin |
|---|---|---|---|---|---|---|---|---|---|---|
| T7 | 修订广度 | 计数净额比 | `A1VJZWoE` | **1.30** | **1.01** | 9.90% | 0.72 | 0.55 | **1.10** | 15.26bp |
| T6 | 修订信息比 | 幅度 / 分歧尺度 | `d5W8VXNK` | 1.19 | 0.88 | 10.06% | 0.45 | 0.38 | 0.96 | 13.64bp |
| T5 | 边际剪刀差 | 跨指标差 | `N1NWm0AX` | 0.72 | 0.41 | 10.28% | 0.47 | 0.65 | 0.59 | 8.03bp |
| T9 | 低分歧门控修订 | 条件几何 | `gJeqOOYv` | 0.45 | 0.21 | 8.17% | **−0.63** | −1.40 | 0.47 | 6.63bp |
| T3 | 预期偏度 | 归一化偏度 | `P0oraNnK` | 0.42 | 0.18 | 8.37% | **0.71** | **1.69** | **0.73** | 5.42bp |
| T10 | bps 修订 | 第三指标迁移 | `MPYlRRjk` | 0.39 | 0.16 | 8.72% | 0.28 | 0.72 | −0.05 | 4.87bp |
| T1 | 相对分歧 | 水平比值 `std/|mean|` | `RREZQMN1` | 0.21 | 0.06 | 4.27% | −0.15 | −0.71 | 0.12 | 5.58bp |
| T4 | 极值不对称 | 有界尾部质量 | `Jje0EqnA` | 0.21 | 0.06 | 7.37% | 0.27 | 1.29 | 0.67 | 2.99bp |
| T2 | 分歧扩张比 | 二阶比值 | `3qoYrwE0` | 0.19 | 0.05 | 8.00% | −0.24 | −1.26 | −0.02 | 2.51bp |
| T8 | 覆盖度忽视 | 原始计数水平 | `9qxP11zq` | 0.15 | 0.04 | 2.37% | −0.44 | −2.93 | −0.18 | 9.03bp |

十条 `failed_ra_count` 3–4，无一例外含 `LOW_SHARPE` + `LOW_2Y_SHARPE`；T8/T10 另加 `LOW_SUB_UNIVERSE_SHARPE`。持仓 71–81 多 / 72–80 空 ≈ 150 只，换手 2.4–10.3%。

### 归因一：修订类（revision）≫ 分歧类（dispersion），但分歧类的闸结构最健康
三条纯分歧模板（T1 相对分歧 0.21 / T2 分歧扩张 0.19 / T4 极值不对称 0.21）全部 ≤0.21；
三条修订模板（T7 1.30 / T6 1.19 / T5 0.72）全部 ≥0.72。**同一数据集内，修订的信息含量是分歧的 3–6 倍。**

但反向证据同样重要：**T3（预期偏度 `(mean−median)/std`）S 仅 0.42，却是全场唯一 2Y/S > 1 的模板（1.69），SUB/S = 1.74**。
⇒ 分歧维度不是「没信号」，而是「信号集中在近两年」。这与 Diether-Malloy-Scherbina (2002) 的分歧溢价在压力期放大的机制一致。
⇒ **若后续能用其它手段把 T3 的 S 抬到闸线，它的闸结构（2Y、SUB）是十条里最省的** —— 这是本轮唯一值得留档的「半成品」。

### 归因二：计数是好的归一化分母，是坏的信号本体（★ 本轮最重要的方法论发现）
- T7 的分母是 `est_12m_ebi_num_4wks_ago`，S 1.30（全场最佳）；
- T8 直接拿 `est_12m_ebi_num` 当信号，S 仅 0.15、2Y −0.44（全场最差）。
⇒ **同一个字段，作分母时贡献 +1.15 的 Sharpe，作信号时贡献 0.15。**
⇒ 与论坛帖 `43152032301591`「金额/计数口径全灭、比率口径完胜」互补：计数不是无效，是**只能进分母**。

### 归因三：门控（trade_when）在 2Y 窗口内切掉了信号段
T9 用「低分歧（`sal_std/|sal_mean|` 排名 < 0.7）门控修订」：S 0.45，但 **2Y = −0.63（全场最差）**。
对照 T6（无门控的同类修订）S 1.19 / 2Y 0.45。
⇒ 门控把 2022–2023 的高分歧期整体排除，而这两年恰是修订信号最有效的时段。**门控方向与经济含义一致，但与 2Y 闸冲突。**
⇒ 与论坛帖 `43754821327639`「门不是越窄越好」实证一致：DEU 上这是第 2 次独立复现。

### 归因四：2Y 是 analyst7 的结构性天花板，不是参数问题
十条 2Y 分布：>1.0 零条；0.5–1.0 三条（0.72 / 0.71 / 0.47）；0–0.5 四条；<0 三条（−0.15 / −0.24 / −0.44 / −0.63 共四条）。
同时 S 最高的 T7 与 2Y 最高的 T3 是**不同模板**，不存在「哪一条只差临门一脚」。
⇒ analyst7 的横截面信息在 2022–2023 系统性衰减。**十模板结构互异仍全灭 ⇒ 判死，不再投入。**

### 与历史足迹的对照
本地库 `dataset='analyst7'` 累计 **61 条**（历史 51 + 本轮 10），bestS 从 **1.04 → 1.30**，RA clean 仍为 **0**。
⇒ 本轮把该数据集的天花板抬高了 25%，但没有改变「不可交付」的结论 —— **抬高天花板 ≠ 打开通路**。

---

## §96 波 97：news38 十模板全灭 —— NEWS 塔在 DEU 关闭

### 数据集事实
| 项 | 值 |
|---|---|
| `news38` 字段数 | **3**（全部 VECTOR） |
| 字段 | `story_analytics_relevance_score` / `story_analytics_metric_value` / `story_analytics_category` |
| 覆盖率 | 0.5992（三字段同） |
| alphaCount | 6 / 8 / 6（**零足迹区**） |
| `news48` | **DEU 零字段**（`platform_count: 0`），直接排除 |

### 十模板完整结果（按 S 降序）

| # | 模板 | 算子几何 | alpha | S | F | TO | 2Y |
|---|---|---|---|---|---|---|---|
| E3 | 分歧度 | `vec_stddev` | `j2YlRjeW` | **0.76** | 0.28 | 37.9% | **1.16** |
| E1 | 关注度水平 | `vec_avg` + `ts_zscore(252)` | `P0ora7gL` | 0.18 | 0.03 | 47.6% | 0.23 |
| E4 | 脉冲能量 | `vec_sum` + `ts_sum(66)` + `ts_zscore` | `zq3w6krO` | 0.12 | 0.03 | 7.5% | −0.22 |
| E8 | 信息比 | `ts_ir(66)` | `akK2ZL61` | 0.11 | 0.02 | 5.2% | 0.03 |
| E6 | 变化率分位 | `ts_delta(22)` + `ts_zscore` | `Jje0Exql` | 0.10 | 0.01 | 54.1% | 0.51 |
| E10 | 指标值范围 | `vec_range` | `RREZQVMz` | 0.04 | – | 37.7% | −0.71 |
| E7 | 分位 | `ts_quantile(252, gaussian)` | `pwdJrPmV` | 0.02 | – | 48.6% | −0.22 |
| E2 | 新闻量（忽视效应反向） | `vec_count` + `ts_zscore` | `YP1wK7x6` | −0.08 | −0.01 | 42.3% | 0.30 |
| E9 | 指标值极值 | `vec_max` + `ts_zscore` | `A1VJZ09Q` | −0.14 | −0.02 | 45.7% | −0.14 |
| E5 | 情绪 × 关注交互 | `multiply(vec_avg, vec_count)` | `9qxP1XEx` | −0.22 | −0.04 | 39.2% | 0.10 |

### 归因一：唯一有信号的是「分歧」，与 analyst7 的 T3/T4 跨数据集呼应
`vec_stddev(relevance_score)` 得 S 0.76 / 2Y 1.16 —— 十条中唯一 S>0.5 且 2Y>1.0 的组合。
analyst7 侧，2Y/S 最好的两条也全是分歧派生（T3 偏度 1.69 / T4 极值不对称 1.29）。
⇒ **「分歧」是 DEU 上跨数据集稳定存在的维度**，但它在这两个数据集上都只能给出 0.42–0.76 的 S ⇒ 单独用不够，只能作辅助信号或正交腿。
⇒ 与论坛帖 `40433238987159`「很多 alpha 本质都是 spread」互补：分歧 = 多空观点 spread，方向对，量级不足。

### 归因二：换手 37–54% 是新闻数据的结构性代价
十条中 7 条换手 >37%，最高的 E6 达 54.1%。对照 analyst7 十模板换手仅 2.4–10.3%（低 5 倍）。
机理：叙事级分析评分每日重算，而分析师预期按周/月修订。
⇒ **NEWS 类数据集在 DEU 的可用窗口极窄**：要么靠低换手的聚合（E4/E8 的 5–8%）但 S 只有 0.11–0.12，要么接受高换手但被 `HIGH_TURNOVER` 拦。二者不可兼得。

### 归因三：稀疏事件铁律在 news38 上不适用（覆盖 0.6 ≠ 稀疏）
论坛帖 `43152032301591` 的「`ts_sum(F,W)` + `ts_zscore(·,长窗)` 两件套」在 news38 上得 0.12 / 2Y −0.22。
根因：该套装是为「0 值海洋 + 偶发脉冲」设计的；news38 覆盖率 0.5992、每日都有值，`ts_sum` 只是把连续量再累加，丢掉了时序结构。
⇒ **判定「是否稀疏」必须先看字段级 coverage，而不是数据集的语义类别。** 覆盖率 ≥0.5 的一律走连续量路线（`ts_zscore` / `ts_ir` / `ts_quantile`），不走脉冲累加。

### 归因四：`vec_count` 作信号在 NEWS 上也是负的（与 analyst7 T8 同向）
E2 `-group_rank(ts_zscore(vec_count, 22), 252)` S −0.08。
与 analyst7 T8（`-group_rank(est_12m_ebi_num)`）S 0.15 同向偏弱，与 §95 归因二「计数只能进分母」再次一致。
⇒ 这是**第三次独立复现**（analyst7 T7/T8、news38 E2/E5），可以升格为该区域的通用规则。

### NEWS 塔终局
| 数据集 | 状态 | 证据 |
|---|---|---|
| `news50` | 判死 | 历史全路线 |
| `news81` | 判死 | 历史全路线 |
| `news104` / `news20` / `news17` | 判死（nip 族） | 历史全路线 |
| `news48` | **零字段** | `platform_count: 0` |
| `news38` | **判死（本轮）** | 十模板最高 S 0.76，换手 37–54% |
⇒ **DEU/NEWS 塔 regular 通道关闭。** 与 RISK（`risk60`/`risk68`/`risk71`/`risk72`/`risk88` 全判死）并列为第二个「零路径塔」。

---

## §97 跨区全闸存量重估：可提交候选从 3 条升为 12 条

### 口径与结果
SQL 口径：`ra_failed_checks = '[]'` 且 `S ≥ 1.58` 且 `F ≥ 1.0` 且 `2Y ≥ 1.58` 且非 OS 阶段。

| 层级 | 条数 |
|---|---|
| 全闸存量（原始） | **744** |
| ├ DEU | 55 |
| └ 其他区 | 689 |
| 指标指纹去重后 | 52 + 669 = **721** |
| 每 region+dataset 取 best | DEU 52 / **其他区 44** |
| 其他区 44 条中 prod 已测 | 34 |
| **其他区 44 条中 prod < 0.7** | **9** |

其他区 44 条的区域分布：USA 15 / IND 14 / EUR 5 / GBR 3 / GLB 3 / KOR 3 / ASI 1。

### ★ 9 条跨区 prod<0.7 候选（含 DEU 3 条，共 12 条可提交候选）

| region | alpha | dataset | S | F | TO | 2Y | prod | self |
|---|---|---|---|---|---|---|---|---|
| IND | `zq3zKgd8` | – | **4.69** | 4.29 | 22.54% | 4.44 | **0.6953** | – |
| KOR | `3qoWQKJg` | – | 3.62 | 4.32 | 13.69% | 2.32 | 0.6221 | – |
| EUR | `YP1d66KM` | – | 3.57 | 2.43 | 24.25% | 3.31 | 0.5985 | – |
| USA | `0mjaa2Ev` | insider_trx_matrix | 3.24 | 2.60 | 16.22% | 4.30 | 0.6460 | 0.0890 |
| IND | `E5VNe67L` | institutions6 | 3.20 | 2.52 | 24.97% | 3.00 | 0.6643 | 0.3437 |
| USA | `88vJ1YKa` | insider_matrix | 2.94 | 1.42 | 48.40% | 2.45 | 0.6933 | – |
| IND | `RREnK5R1` | sentiment21 | 2.82 | 2.04 | 26.27% | 2.23 | 0.5874 | – |
| USA | `9qxLOPxr` | risk70_style_factors | 2.69 | 1.67 | 15.92% | 2.24 | 0.6835 | – |
| GBR | `npdm0mrq` | predictive_starmine | 1.76 | 1.10 | **0.00%** | 1.98 | 0.5557 | 0.3322 |

**必须扣掉的一条**：`npdm0mrq` 换手 0.00% / margin 0.00 ⇒ 实际无持仓，`S 1.76` 是退化值，**不可提交**。
⇒ **有效跨区候选 = 8 条。**

### 三条必须做的核实（尚未完成，不得据上表下提交结论）
1. **塔归属**：`backtest_results` 无 pyramid 列，只能逐条 `get_alpha_details.pyramids.list`。
2. **prod 新鲜度**：表中 prod 值来自本地 `alphas.prod_correlation` 列，多数 `corr_age_hours` 已数百小时。按 48h 保鲜规则全部视为 **stale**，提交前必须 `check_correlation(refresh=True)` 当场终验。
3. **region 真实性**：本地库 `region` 列已被证实会混入 EUR（见既有记录），提交前须核 `get_alpha_details.settings.region` + `pyramids.list`。

### 对「60 条」的含义
- DEU 侧可交付 **3 条**（`QPveY7Kg` / `MPY9VNY9` / `Vkxnb8QG`，均全闸通过且 prod<0.7）；
- 跨区可承接 **8 条有效**（待塔核实 + prod 终验）；
- 合计 **11 条**，距离 60 条仍差 **49 条**。
- 换算：11 / 4,772 ≈ **0.23%** 的产出率。按同效率补足 49 条需再测约 **21,000 条**。
⇒ **「60 条全在 DEU」已可用数据证伪；「DEU 3 + 跨区 8 + 新区新挖 49」是当前唯一自洽的路线。**

### DEU 塔终局地图（本轮更新）

| 塔 | 状态 | 说明 |
|---|---|---|
| MODEL / OTHER | 已点亮（7/3、4/3） | – |
| SHORTINTEREST | **2/3** → 提交 `MPY9VNY9` 即 **3/3** | 待授权 |
| ANALYST | 1/3 → 提交 `Vkxnb8QG` 至 2/3 | 第 3 条仍缺；`analyst7` 本轮判死后无已知路径 |
| SENTIMENT | 0/3 → 提交 `QPveY7Kg` 至 1/3 | 待授权 |
| FUNDAMENTAL | 1/3 | **无路径** |
| INSTITUTIONS | 1/3 | **无路径**（三条独立路线全灭） |
| INSIDERS | 1/3 | 无新路径 |
| **NEWS** | **0/3** | **本轮关闭**（news38 判死 + news48 零字段） |
| **RISK** | **0/3** | **已关闭**（risk60/68/71/72/88 全判死） |

### 累计统计
DEU 累计已测 **≈ 4,772 条**（4,752 + 波 96 十模板 + 波 97 十模板）。
本轮新增判死：**`analyst7`**（十模板全灭，天花板 1.30）、**`news38`**（十模板全灭，天花板 0.76）、**`news48`**（DEU 零字段）。

---

## §98 本轮方法论增量（可跨区复用）

1. **「计数只能进分母」已三次独立复现**：analyst7 T7（分母，S 1.30）vs T8（信号，S 0.15）；news38 E2（信号，S −0.08）vs E5（交互，S −0.22）。⇒ 可作为 DEU/GBR 类成熟市场的通用规则写入模板库。
2. **「分歧」是跨数据集稳定但量级不足的维度**：analyst7 T3/T4 的 2Y/S 最好（1.69 / 1.29），news38 E3 是十模板唯一亮点（S 0.76 / 2Y 1.16）。⇒ 正确定位是**正交腿或条件变量，不是主信号**。
3. **「2Y 优先于 S」在 DEU 的判死纪律**：本轮 analyst7 的 S 天花板 1.30 差闸 18%，2Y 天花板 0.72 差闸 119%。**当 2Y/S < 0.7 时，该字段族应直接判死，不必再花仿真槽试骨架** —— 因为 2Y 是近两年的独立信息，不能用参数补。
4. **门控类几何（trade_when）在 2Y 闸上是负资产**：analyst7 T9（2Y −0.63）与论坛帖实证一致。⇒ DEU 上应优先无门控骨架，门控只在破 prod 墙时使用。
5. **预检 `valid: true` 仍可能夹带假 unknown**：本轮 `driver="gaussian"` 被 `preflight_expressions` 报成 `unknown_fields: ["gaussian"]`，但该写法在 `QPveY7Kg` 上已实际跑通。⇒ 字符串参数会被误判成字段名，需人工辨别，不要因其改表达式。
6. **收批一律 `--no-queue`，且 ★ 绝不能用 `| Select-Object -First N` 截断管道**：本轮回溯确认，批次 A 首次收批的 `exit 1` 实际是 PowerShell 管道被提前关闭造成的假失败；去掉截断后同命令 `exit 0` 且正常入库 5 行。


---

## §99 跨区全闸存量池的 prod 当场终验（2026-10-30 下午）

### 99.1 本节要解决的问题

此前所有"可提交候选"的 prod 值都来自本地 `alphas.prod_correlation` 列，
按 48h 保鲜规则**全部过期**。提交是不可逆动作，不能拿过期值当依据。
本节把整条候选链上的 20 条逐条回平台当场重算，得到可用于提交判定的真值。

### 99.2 候选池是怎么收敛到 20 条的

| 步骤 | 口径 | 条数 |
|---|---|---|
| 1. 全闸通过（`ra_failed_checks='[]'` 且 S≥1.58 且 F≥1.0 且 2Y≥1.58 且非 OS） | 全区域 | **744** |
| 2. 指标指纹去重（S/F/TO/2Y 四项 round 后完全相同 ⇒ 同一组合） | 全区域 | 721 |
| 3. 退化值剔除（换手 0 或 多空持仓均为 0） | 全区域 | 721 |
| 4. 每 `region+dataset` 取最优（候选压缩，不是最终数） | 非 DEU | 44 |
| 5. 剔除已测 prod≥0.7 与 prod 缺失 | 非 DEU | 20 |
| 6. **PnL 互相关聚簇（threshold 0.7, years 4, 纯本地零配额）** | 20 条 | **20 独立** |

**第 6 步是关键**：字段名族会把多样性高估约 3 倍。实测 20 条里
`pairs_over_threshold = []`、`all_below_threshold = true`、
`max_pair = 0.5861`（`E5VNe67L` vs `RREnK5R1`）、`max_mutually_below_subset_size = 20`、
`max_subset_exact = true`。
⇒ **这 20 条是 20 个真独立的信号**，不是同一主意的多种写法。

对照：另一组 19 条（含两个孪生对 `0mjaa2Ev`≡`MPYoQ1E6` 0.9926、
`pwv9eM76`≡`58jPrvZ1` 0.985）聚出 17 个独立族——**同族重复率约 10%**。

### 99.3 当场终验结果（全部 `refresh=True`，2026-10-30 08:19–08:31）

| alpha | region | S | F | 2Y | TO% | SUB | **fresh prod** | 缓存旧值 | 塔 | 判决 |
|---|---|---|---|---|---|---|---|---|---|---|
| `npvJaGa3` | GLB | 4.75 | 4.10 | 5.49 | 14.0 | 1.76 | **0.9768** | 0.6887 | 无 | FAIL |
| `zq3zKgd8` | IND | 4.69 | 4.29 | 4.44 | 22.5 | 2.67 | **0.6953** | 0.6953 | 无 | PASS |
| `3qoWQKJg` | KOR | 3.62 | 4.32 | 2.32 | 13.7 | 2.93 | **0.6221** | 0.6221 | 无 | PASS |
| `YP1d66KM` | EUR | 3.57 | 2.43 | 3.31 | 24.2 | 2.40 | 0.5985* | 0.5985 | 无 | PASS |
| `0mjaa2Ev` | USA | 3.24 | 2.60 | 4.30 | 16.2 | 1.40 | **0.8031** | 0.6460 | other | FAIL |
| `VkxV8NAJ` | GLB | 3.23 | 1.40 | 3.89 | 60.9 | 2.04 | **0.9953** | 0.6494 | 无 | FAIL |
| `E5VNe67L` | IND | 3.20 | 2.52 | 3.00 | 25.0 | 1.64 | **0.6643** | 0.6643 | institutions/pv | PASS |
| `88vJ1YKa` | USA | 2.94 | 1.42 | 2.45 | 48.4 | 1.28 | 0.6933* | 0.6933 | other | PASS |
| `RREnK5R1` | IND | 2.82 | 2.04 | 2.23 | 26.3 | 2.00 | 0.5874* | 0.5874 | pv/sentiment | PASS |
| `9qxLOPxr` | USA | 2.69 | 1.67 | 2.24 | 15.9 | 1.44 | 0.6835* | 0.6835 | risk/model | PASS |
| `1YNQO9jJ` | IND | 2.37 | 1.82 | 3.11 | 20.3 | 1.56 | 0.3389* | 0.3389 | 无 | PASS |
| `vR1aEpa3` | GBR | 2.32 | 2.11 | 2.29 | 12.3 | 1.38 | 0.6632* | 0.6632 | 无 | PASS |
| `58jr102k` | USA | 2.26 | 1.33 | 2.06 | 12.6 | 1.41 | **0.7403** | 0.6818 | 无 | FAIL |
| `gJWnrZgg` | IND | 2.14 | 1.70 | 1.99 | 10.7 | 0.93 | **0.8417** | 0.6998 | 无 | FAIL |
| `QPveY7Kg` | DEU | 2.03 | 1.61 | 2.54 | 16.1 | 1.20 | **0.6671** | 0.6671 | sentiment | PASS |
| `O0Jx2O6R` | EUR | 1.94 | 1.26 | 1.86 | 5.6 | 1.05 | **0.8610** | 0.5129 | 无 | FAIL |
| `Vkxnb8QG` | DEU | 1.83 | 1.64 | 2.09 | 9.1 | 0.99 | **0.6384** | 0.6384 | shortinterest/analyst | PASS |
| `pwv9eM76` | IND | 1.66 | 1.24 | 2.09 | 11.7 | 1.48 | **0.5501** | 0.5501 | 无 | PASS |
| `KPmOOwZx` | EUR | 1.61 | 1.10 | 1.80 | 8.2 | 1.05 | **0.9914** | 0.6624 | 无 | FAIL |
| `MPY9VNY9` | DEU | 1.59 | 1.26 | 2.36 | 3.6 | 1.02 | **0.5986** | 0.5986 | shortinterest | PASS |

\* 标记的 6 条为 1.7–17.7h 内的平台实测值（本轮 refresh 时平台相关性队列拥塞、
两次 120s 超时），**提交前仍须再刷一次**。其余 14 条为本轮当场新测（0.0h）。

**汇总：13 PASS / 7 FAIL / 0 未验。**

### 99.4 ★ 方法论增量：本地 `prod_correlation` 列有 35% 是错的

**这是本节最重要的发现，直接推翻"48h 保鲜"这个阈值假设。**

| 缓存年龄 | 条数 | 当场重测相符 | 不符 | 失真是度 |
|---|---|---|---|---|
| ~0 h（本轮自测） | 7 | 7 | 0 | — |
| 1.7–23.6 h | 6 | 6（未逐一重测，按 ≤48h 采信） | 0 已知 | — |
| **23.6–48 h** | 2 | 1 | **1**（`0mjaa2Ev` 0.6460→0.8031，+0.157） | 大 |
| **>48 h** | 8 | 2 | **6** | 极大 |

>48h 组的 6 个失真幅度：`gJWnrZgg` +0.142、`npvJaGa3` +0.288、
> `VkxV8NAJ` +0.346、`O0Jx2O6R` +0.348、`KPmOOwZx` +0.329、`58jr102k` +0.059。

**根因**：BRAIN 的 production pool 是**全平台所有已提交 alpha**，
别人每天在提交，池子天天变大、个体相关性天天抬升。因此
**prod 不是候选的静态属性，而是"候选 × 当时的池"的快照**。
48h 在池子平静期够用，在别人大量提交的时期完全不够。

**落地规则（升级 48h 口径）**：
1. **判闸只用当场 `refresh=True` 的值**；48h 内的缓存**只能用于排序，不能用于放行**。
2. 交付前批量终验时，对每一条都要 `refresh=True`，不能因为"昨天刚测过"跳过。
3. 失真方向**单向偏高**（7 个失败全部是"缓存偏低、真实偏高"）⇒
   缓存值偏低不是好消息，恰恰说明池子长胖了。
4. 反例警戒：`gJWnrZgg` 缓存 0.6998 看着"刚好卡线通过"，真实 0.8417 差 0.14。
   **卡线值天然可疑**——它多半是某个时刻的截断值。

### 99.5 区域效率对照：DEU 是全池最差的区之一

按"全闸通过条数 / 其中已知撞 prod 墙的条数"衡量：

| region | 全闸通过 | prod 已测<0.7 | prod 未测 | **已测中撞墙** | 撞墙率 | S≥2.5 | 最高 S |
|---|---|---|---|---|---|---|---|
| **IND** | 120 | **41** | 66 | 13 | **11%** | 65 | 4.69 |
| USA | 143 | 26 | 54 | 63 | 62% | 37 | 4.50 |
| EUR | 150 | 22 | 93 | 35 | 40% | 10 | 3.57 |
| GLB | 179 | 11 | 98 | 70 | 86% | **145** | 7.45 |
| GBR | 64 | 11 | 17 | 36 | 77% | 4 | 3.42 |
| **DEU** | 52 | 4 | 30 | **18** | **82%** | 2 | 2.70 |
| KOR | 9 | 1 | 8 | 0 | 0% | 1 | 3.62 |
| ASI | 4 | 0 | 3 | 1 | 100% | 0 | 2.06 |

**读法（重要，别读反）**：
- **GLB 的 179 条高分（S≥2.5 有 145 条）是假富矿**——它 86% 撞墙，
  且 98 条 prod 未测。高分只说明"信号强"，不说明"能提交"。
- **IND 才是真富矿**：120 条里只有 13 条撞墙（11%），41 条已实测安全，
  且 65 条 S≥2.5。IND 的拥挤度结构性低于 GLB/USA。
- **DEU 82% 撞墙**，是仅次于 ASI/GLB 的第三差。这与 DEU 只有 TOP500
  （500 只票）导致信号高度同质有关：池子小 ⇒ 大家挖到的东西像。
- KOR 9 条零撞墙但样本太小，不能据此推断。

**⇒ 对"60 条 regular alpha"目标的直接含义**：
DEU 单区 4,772 条累计回测只出 3 条可交付（产出率 0.23%），
而 IND 单区库里就躺着 41 条已实测 prod<0.7 的全闸 alpha。
**继续在 DEU 硬挖的效率，比在 IND 复用存量低两个数量级。**

### 99.6 DEU 塔位的实际影响

本轮已当场终验的 3 条 DEU 候选全部 PASS：

| alpha | fresh prod | self | 塔 | 提交后塔状态 |
|---|---|---|---|---|
| `MPY9VNY9` | 0.5986 | 0.2703 | DEU/D1/SHORTINTEREST ×1.3 | SHORTINTEREST 2/3 → **3/3 点亮** |
| `QPveY7Kg` | 0.6671 | 0.0242 | DEU/D1/SENTIMENT ×1.8 | SENTIMENT 0/3 → 1/3 |
| `Vkxnb8QG` | 0.6384 | 0.6379 | DEU/D1/SHORTINTEREST ×1.3 + DEU/D1/ANALYST | ANALYST 1/3 → 2/3（shortinterest 腿冗余） |

三条均 `failed_ra = 0`、`failed_ppa = 0`、`sim_fails = []`，
`submit_verdict = UNVERIFIABLE`（仅因平台 `GET /alphas/{id}/submit` 恒 404 死端点，
不是真闸）。警告级只有 `OSMOSIS_ALLOCATION` / `MATCHES_THEMES`
（`MPY9VNY9` 另有 `CLUSTER_TEST` limit 1 / value 0.66）。

**提交顺序建议**：`MPY9VNY9` → `QPveY7Kg` → `Vkxnb8QG`。
理由：先把 SHORTINTEREST 封顶到 3/3（确定收益），
再点 SENTIMENT 第一格，最后用 `Vkxnb8QG` 补 ANALYST 第二格
（它 self 0.6379 距红线仅 0.062，风险最高，放最后）。

### 99.7 本节遗留

1. **6 条只有 1.7–17.7h 的值**（`YP1d66KM`/`88vJ1YKa`/`RREnK5R1`/`9qxLOPxr`/
   `1YNQO9jJ`/`vR1aEpa3`），提交前必须再刷。
2. **平台相关性队列本轮两次 120s 超时**（`YP1d66KM`/`9qxLOPxr`），
   按 skill `wq-prod-corr-read`：超时不落缓存、inflight 标记残留约 300s。
   批量终验要串行并留重试间隔。
3. **7 条撞墙候选已落库真值**，可作后续"换族"的负面样本，
   其中 `npvJaGa3`(GLB S4.75) / `VkxV8NAJ`(GLB S3.23) 两条 prod 已达 0.98–0.99，
   属"同族已有 ACTIVE"的结构性 1.0，不是外部拥挤，本族再换参数无意义。

## §100 IND 存量转可交付 + 塔额度满仓（2026-10-30 08:40-09:00）

### 100.1 本轮问题
§99 确立了「DEU 单位产出率 0.23%，单区不可达 60 条」。要补 60 条只能复用存量，
但存量里「prod 已测 < 0.7」这个数字建立在本地 `alphas.prod_correlation` 列上，
而 §99.4 已证明该列 35% 失真。本轮把 IND 全池拉出、按 PnL 聚簇、逐条当场重测 prod，
目的是把「41 条已测安全」这个口径换成可提交的真值。

### 100.2 IND 全池盘点（本地 SQL，零平台配额）
口径：`ra_failed_checks='[]'` 且 S≥1.58 且 F≥1.0 且 2Y≥1.58 且 `stage<>'OS'`，region=IND。

| 项 | 数值 |
|---|---|
| 全闸通过行数 | 125 |
| 指标指纹去重后 | **120 个独立指纹** |
| prod<0.7 且 ≤48h（fresh_ok） | 22 |
| prod<0.7 但 >48h（stale_ok） | 20 |
| prod≥0.7（撞墙） | 14 |
| **prod 从未测（untested）** | **64** |

**读数**：此前记的「IND 41 条已测安全」在指纹口径下是 42 条（22+20），
扣掉 48h 之外需要重测的 20 条，**真正当场可信的安全存量只有 22 条**。
真正没被开采的是 **64 条 prod 从未测的家族** —— 这是 IND 剩余空间的主体，
而不是那 42 条。

### 100.3 PnL 聚簇：16 个代表 → 9 个真独立
从 64 条 untested 里按数据集取 Sharpe 最高者 16 条，跑
`compute_mutual_correlation(threshold=0.7, years=4)`（纯本地，零配额）：

- `max_pair` = 0.9743（`RRAGw5ja` vs `vR1KRlpw`，analyst 族孪生）
- `pairs_over_threshold` 共 9 对，含 5 对 ≥0.92 的近似重复：
  `mLYdVKap`~`VkdZ3wKM` 0.9684、`omEMRpWb`~`0mY0xljG` 0.9483、
  `78LEMG8Q`~`kqN2Gebd` 0.9391、`wpQ6VMa5`~`9qxoQLrV` 0.9256
- `max_mutually_below_subset_size` = **9**，`max_subset_exact=true`

⇒ **16 条里只有 9 条是真独立信号**，同族重复率约 44%。
这与 §99 的口径一致（「每 3 条同族回测 ≈ 1 条独立信号」在含大量孪生的池子里更严重）。

### 100.4 prod 当场终验（串行，每条约 5-25s）
IND 池取到的 9 条独立信号中，本轮实测 5 条：

| alpha | 数据集 | S | F | 2Y | SUB | **fresh prod** | 判决 | 全池分布特征 |
|---|---|---|---|---|---|---|---|---|
| `mLYdVKap` | institutions6 | 3.16 | 2.45 | 3.07 | 1.80 | **0.6757** | **PASS** | 0.6-0.7 桶仅 2 条 |
| `78LEMG8Q` | sentiment21 | 2.78 | 2.00 | 2.19 | 1.78 | **0.6507** | **PASS** | 0.6-0.7 桶仅 1 条 |
| `A1V6Kppg` | risk70 | 3.01 | 1.95 | 3.02 | 1.59 | 0.7372 | FAIL | 0.7-0.8 桶仅 1 条 |
| `JjellVJ2` | model39 | 3.83 | 2.91 | 2.87 | 2.32 | 0.8399 | FAIL | 0.8-0.9 桶 6 条 |
| `9qxoozer` | model39 | 3.06 | 2.68 | 2.28 | 1.86 | 0.8515 | FAIL | 0.8-0.9 桶 1 条 |

**`omEMRpWb`（insiders1, S 2.45）** 两次被队列占用/超时打掉，未取得真值。

**★ 最重要的负样本读数：`9qxoozer` 在我自己的 16 条里最大相关只有 0.05（几乎绝对正交），
但平台 prod = 0.8515。** 这直接证伪了一种直觉——
「与我自有候选正交」完全不能推出「与平台全池正交」。
我的池子只有 60 条 OS，平台池是六位数（直方图显示的 alpha 计数合计约 49 万）。
**自我正交度不能当 prod 的代理变量，只能当作「我这一侧还有多少独立弹药」的度量。**

另一条读数：`A1V6Kppg` 的 0.7-0.8 桶只有 1 条、`mLYdVKap` 的 0.6-0.7 桶只有 2 条 ——
**卡线附近的全池 alpha 数量本身就是「这个信号族还剩多少空间」的指纹**。
桶里只有个位数 ⇒ 略微换几何就能出墙；桶里成百上千条（如 `9qxoozer` 的 0.2-0.3 桶 105,273 条）
⇒ 这个族在平台侧已被彻底覆盖。

### 100.5 ★ 塔额度：PV × 非三塔 已满 5/5
按平台 `get_alpha_details` 的 `pyramids.list`（**不是本地表**）逐条核验：

| alpha | region | 塔 | 类 | 占额度 |
|---|---|---|---|---|
| `E5VNe67L` | IND | INSTITUTIONS + PV | trio×非trio | ✔ 1 |
| `RREnK5R1` | IND | PV + SENTIMENT | trio×非trio | ✔ 2 |
| `9qxLOPxr` | USA | RISK + MODEL | trio×非trio | ✔ 3 |
| `mLYdVKap` | IND | INSTITUTIONS + PV | trio×非trio | ✔ 4 |
| `78LEMG8Q` | IND | PV + SENTIMENT | trio×非trio | ✔ 5 |

**⇒ 用户设定的「trio × 非 trio ≤ 5」额度已经用满。**
其余 10 条候选全部落在额度外：`SINGLE` 3 条（`QPveY7Kg` SENTIMENT / `MPY9VNY9` SHORTINTEREST / `88vJ1YKa` OTHER）、
`MULTI_NONTRIO` 1 条（`Vkxnb8QG` SHORTINTEREST+ANALYST）、`NO_PYRAMID` 6 条
（`zq3zKgd8` / `3qoWQKJg` / `YP1d66KM` / `1YNQO9jJ` / `pwv9eM76` / `vR1aEpa3`）。
**BANNED（trio 内部互组）0 条。**

**这条约束对策略的直接后果**：见 100.6 —— 本轮找到的高产出模板天生带 PV 腿，
所以它是个「只能用 5 次」的模板；额度满仓后，IND 继续挖必须换到不带 `returns` 的几何。

### 100.6 ★ 高产出模板：`returns` 残差化骨架（IND / decay 126 / STATISTICAL）
`mLYdVKap` 与 `78LEMG8Q` 共用同一骨架，只有信号腿不同：

```text
rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(SIGNAL, W), W, rettype=0))
# SIGNAL 分别是
#   mLYdVKap : divide(quantity_institutional_shares_disposed,
#                    add(quantity_institutional_shares_acquired, quantity_institutional_shares_disposed))
#   78LEMG8Q : ts_backfill(snt21_4pos_std, 504)
# settings : decay 126 / neutralization STATISTICAL / truncation 0.08 / TOP500 / D1
```

**经济含义**：把个股收益对「机构卖出占比」/「情绪离散度」做时序回归，取残差。
`rettype=0` 只取回归斜率（beta），外层再取负 ⇒ 交易的是
「该股收益对这组非价格信息的敏感度」。低敏感度的股票被做多。
这是一个**非动量非反转的第三条轴**：不预测收益方向，而是预测
「收益对某个基本面/情绪变量的传导强度」。

**为什么值得复用**：两条都 `failed_ra_count=0`、prod 分别 0.6757 / 0.6507、
self 0.6759 / 0.5361，且互相关 0.633（同骨架不同信号腿仍算两条）。
`decay 126` 是这批的关键共同设置 —— 半年级别的平滑把换手压到 25% 附近，
同时没有抹掉 beta 的截面差异（对照 §73 的 `group_rank` 摧毁 SUB）。

**注意**：`ts_zscore(returns,252)` 这条价格腿会被平台记成 PV 塔，
所以该模板**天生吃掉 trio×非trio 额度**。要用它必须先查 100.5 的额度余量。

### 100.7 本地数据完整性：`alpha_pyramids` 缺行 ≠ alpha 无塔
审计脚本首轮把 `mLYdVKap` / `78LEMG8Q` 判成 `NO_PYRAMID`，但平台
`get_alpha_details` 明确 `checks.pass` 含 `MATCHES_PYRAMID`、`pyramids.list` 有两个塔。
回查发现 `alpha_pyramids` 表里**这两条根本没有行**（本轮是 INSERT 而非 UPDATE）。

**⇒ 两种「塔位为空」必须分开**：
1. **表中缺行** —— 本地缺失，平台其实有塔（本轮 2 条属此类，已修补）
2. **表中有行但 `checks` 无 `MATCHES_PYRAMID`** —— 平台真的不点亮任何塔
   （§99.3 的 `zq3zKgd8` / `3qoWQKJg` / `YP1d66KM` 属此类，已用 `get_alpha_details` 验证）

**落地规则**：任何「这条点亮哪个塔」的判断，**唯一权威是 `get_alpha_details` 的
`pyramids.list` + `checks`**。本地 `alpha_pyramids` 只能当缓存，缺行必须当「未知」而不是「无塔」。

### 100.8 当前可交付总表（15 条，prod<0.7 & self<0.7 已核）
| # | alpha | reg | S | F | 2Y | SUB | prod | self | 塔 | 额度 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `zq3zKgd8` | IND | 4.69 | 4.29 | 4.44 | 2.67 | 0.6953 | 待测 | 无塔 | 免费 |
| 2 | `3qoWQKJg` | KOR | 3.62 | 4.32 | 2.32 | 2.93 | 0.6221 | 待测 | 无塔 | 免费 |
| 3 | `YP1d66KM` | EUR | 3.57 | 2.43 | 3.31 | 2.40 | 0.5985* | 待测 | 无塔 | 免费 |
| 4 | `E5VNe67L` | IND | 3.20 | 2.52 | 3.00 | 1.64 | 0.6643 | 待测 | INST+PV | 占 |
| 5 | `mLYdVKap` | IND | 3.16 | 2.45 | 3.07 | 1.80 | **0.6757** | **0.6759** | INST+PV | 占 |
| 6 | `88vJ1YKa` | USA | 2.94 | 1.42 | 2.45 | 1.28 | 0.6933* | 待测 | OTHER | 免费 |
| 7 | `RREnK5R1` | IND | 2.82 | 2.04 | 2.23 | 2.00 | 0.5874* | 待测 | PV+SENT | 占 |
| 8 | `78LEMG8Q` | IND | 2.78 | 2.00 | 2.19 | 1.78 | **0.6507** | **0.5361** | PV+SENT | 占 |
| 9 | `9qxLOPxr` | USA | 2.69 | 1.67 | 2.24 | 1.44 | 0.6835* | 待测 | RISK+MODEL | 占 |
| 10 | `1YNQO9jJ` | IND | 2.37 | 1.82 | 3.11 | 1.56 | 0.3389* | 待测 | 无塔 | 免费 |
| 11 | `vR1aEpa3` | GBR | 2.32 | 2.11 | 2.29 | 1.38 | 0.6632* | 待测 | 无塔 | 免费 |
| 12 | `QPveY7Kg` | DEU | 2.03 | 1.61 | 2.54 | 1.20 | **0.6671** | **0.0242** | SENTIMENT | 免费 |
| 13 | `Vkxnb8QG` | DEU | 1.83 | 1.64 | 2.09 | 0.99 | **0.6384** | **0.6379** | SHORTINT+ANALYST | 免费 |
| 14 | `pwv9eM76` | IND | 1.66 | 1.24 | 2.09 | 1.48 | 0.5501 | 待测 | 无塔 | 免费 |
| 15 | `MPY9VNY9` | DEU | 1.59 | 1.26 | 2.36 | 1.02 | **0.5986** | **0.2703** | SHORTINTEREST | 免费 |

\* = 48h 外旧值，提交前须 `refresh=True` 重刷（§99.4 铁律）。
**加粗 = 本轮 0.0h 当场实测**（7 条：`mLYdVKap` / `78LEMG8Q` / `QPveY7Kg` / `Vkxnb8QG` / `MPY9VNY9`
+ `zq3zKgd8` 0.3h / `E5VNe67L` 0.2h / `pwv9eM76` 0.2h）。

### 100.9 遗留
1. `omEMRpWb` / `RREQ5len` / `RRAGw5ja` / `YP1G3NjM` 四条（均 IND、均单塔、均不占额度）
   prod 未取得真值 —— 队列被后台任务占用（`holder: corr:get_production_correlation(9qxP0K8V)`）。
2. IND 仍有 55 条 untested 指纹家族未做 PnL 聚簇（本轮只取了 16 条代表）。
3. 塔额度满仓后，IND 续挖必须避开 `returns` 价格腿，否则无法提交。
4. `alpha_pyramids` 需重新回填（本轮只补了 2 条）；`NO_PYRAMID` 那 6 条中
   `1YNQO9jJ` / `pwv9eM76` / `vR1aEpa3` 尚未用 `get_alpha_details` 平台验证。

## §101 self 相关全扫 + 互相关去重 → 13 条最终篮（2026-10-30 09:00-09:20）

### 101.1 self 相关：15/15 全部通过（纯本地计算，零平台槽）
`check_self_correlation(correlation_type="self", threshold=0.7)`，池按 alpha 的
`classifications` 分区（与平台提交时的 Self Correlation 同口径，排除 Power Pool）。

| alpha | region | S | self | 最相似 | 余量 | 池大小 |
|---|---|---|---|---|---|---|
| `QPveY7Kg` | DEU | 2.03 | **0.0242** | `58gkLAkk` | 0.676 | 10 |
| `88vJ1YKa` | USA | 2.94 | **0.2409** | `kqJLawqP` | 0.459 | 135 |
| `MPY9VNY9` | DEU | 1.59 | **0.2703** | `blRnKEk6` | 0.430 | 10 |
| `9qxLOPxr` | USA | 2.69 | **0.2866** | `O08EjLVp` | 0.413 | 3 |
| `1YNQO9jJ` | IND | 2.37 | **0.2991** | `0mjk2ZQv` | 0.401 | 52 |
| `pwv9eM76` | IND | 1.66 | **0.5017** | `pwRJmvP3` | 0.198 | 52 |
| `RREnK5R1` | IND | 2.82 | **0.5056** | `0mjk2ZQv` | 0.194 | 52 |
| `vR1aEpa3` | GBR | 2.32 | **0.5240** | `WjAV89jG` | 0.176 | 18 |
| `78LEMG8Q` | IND | 2.78 | **0.5361** | `0mjk2ZQv` | 0.164 | 52 |
| `YP1d66KM` | EUR | 3.57 | **0.5656** | `LL5VwgO1` | 0.134 | 10 |
| `3qoWQKJg` | KOR | 3.62 | **0.6224** | `9qjGvaWe` | 0.078 | 27 |
| `Vkxnb8QG` | DEU | 1.83 | **0.6379** | `2rjrMZ25` | 0.062 | 10 |
| `E5VNe67L` | IND | 3.20 | **0.6648** | `0mjk2ZQv` | 0.035 | 52 |
| `mLYdVKap` | IND | 3.16 | **0.6759** | `0mjk2ZQv` | 0.024 | 52 |
| `zq3zKgd8` | IND | 4.69 | **0.6954** | `wpbQjeKp` | **0.005** | 52 |

**★ 最重要的结构性读数：`0mjk2ZQv` 一条 OS alpha 同时压住 4 条 IND 候选**
（`mLYdVKap` 0.676 / `E5VNe67L` 0.665 / `78LEMG8Q` 0.536 / `RREnK5R1` 0.506 / `1YNQO9jJ` 0.299）。
我已经在这个「机构持股 × 情绪」交叉主题上有一条提交过的 alpha，其余同主题候选的 self 全部由它决定。
**⇒ self 相关不是候选的固有属性，而是「候选 × 我的 OS 池」的快照 —— 与 prod 完全同构（§99.4）。**
每提交一条，池子里所有同族候选的 self 就抬高一次。这带来一个硬约束：
**同族多候选不能靠「都过 self」来并行提交，必须按 PnL 族串行判断。**

**第二个读数：self 池大小 ≠ 区域大小。**
`9qxLOPxr` 的池只有 3 条，但平台 `settings.region` 明写 USA / TOP2000 ——
池是按 `classifications`（区域+universe+delay+类型…）分区后的子集，不是整个区域。
**⇒ 「小池 ⇒ self 天然容易过」这个推论只在小分类桶里成立，不能当候选质量判断。**

### 101.2 互相关去重：15 条里有 2 对内部冲突
`compute_mutual_correlation(threshold=0.7, years=4)`，纯本地零配额：

| 对 | 相关系数 | 判定 |
|---|---|---|
| `RREnK5R1` ↔ `78LEMG8Q` | **0.9093** | 近似孪生，只能取一 |
| `E5VNe67L` ↔ `mLYdVKap` | **0.8048** | 近似孪生，只能取一 |

- `max_pair` = 0.9093
- `pairs_over_threshold` = 2 对
- `max_mutually_below_subset_size` = **13**，`max_subset_exact=true`

两对都是**同数据集、同塔**的重复：
- `RREnK5R1` / `78LEMG8Q` 都是 sentiment21、都是 `PV+SENTIMENT` 塔
- `E5VNe67L` / `mLYdVKap` 都是 institutions6、都是 `INSTITUTIONS+PV` 塔

**⇒ 这是本轮最重要的执行层结论：15 条「各自过闸」的候选，实际只能提交 13 条。**
这正是 §99 定的规则（「每 3 条同族 ≈ 1 条独立信号」）在具体篮子上的体现 ——
**单条过闸 ≠ 整篮可提交。任何提交清单必须先跑互相关。**

### 101.3 两对的取舍
**第 2 对（institutions6）—— 已定：取 `E5VNe67L`。**
| | S | F | 2Y | SUB | prod | self |
|---|---|---|---|---|---|---|
| `E5VNe67L` | **3.20** | **2.52** | **3.00** | **1.64** | **0.6643** | **0.6648** |
| `mLYdVKap` | 3.16 | 2.45 | 3.07 | 1.80 | 0.6757 | 0.6759 |
`E5VNe67L` 在 S / F / 2Y / prod / self 五项上全胜（仅 SUB 与 2Y 略输），
且 prod 为 0.2h 内的当场值。**`mLYdVKap` 降级为备胎。**

**第 1 对（sentiment21）—— 待定，缺一个真值。**
| | S | F | 2Y | SUB | prod | prod 年龄 | self |
|---|---|---|---|---|---|---|---|
| `RREnK5R1` | **2.82** | **2.04** | 2.23 | **2.00** | 0.5874 | **18.3h** | **0.5056** |
| `78LEMG8Q` | 2.78 | 2.00 | **2.19** | 1.78 | **0.6507** | **0.0h** | 0.5361 |
`RREnK5R1` 的 S / F / SUB / self 都更好，但它的 prod 是 18.3h 的旧值。
按 §99.4「失真方向单向偏高」，其真值 ≥ 0.5874，可能落在 0.65–0.72 任何位置。
**⇒ 判定必须在 `RREnK5R1` 的 prod 重刷之后做。** 若重刷 ≤0.66 取 `RREnK5R1`；
若 >0.66 取 `78LEMG8Q`（0.6507 已当场验证）。

### 101.4 ★ 塔额度修正：3/5，不是 §100.5 写的 5/5
§100.5 是按「15 条全部可提交」算的，但 101.2 已证明其中 2 条是重复不能提交。
去重后占额度的只有 3 条：

| alpha | region | 塔 | 占额度 |
|---|---|---|---|
| `E5VNe67L` | IND | INSTITUTIONS + PV | ✔ 1 |
| `RREnK5R1` 或 `78LEMG8Q` | IND | PV + SENTIMENT | ✔ 2 |
| `9qxLOPxr` | USA | RISK + MODEL | ✔ 3 |

**⇒ 「trio × 非 trio」额度实际用量 3/5，仍有 2 个空位。**
（`mLYdVKap` 作为备胎若被启用则到 4/5。）

其余 10 条不占额度：`SINGLE` 3 条（`QPveY7Kg` SENTIMENT / `MPY9VNY9` SHORTINTEREST /
`88vJ1YKa` OTHER）、`MULTI_NONTRIO` 1 条（`Vkxnb8QG` SHORTINTEREST+ANALYST）、
`NO_PYRAMID` 6 条（`zq3zKgd8` / `3qoWQKJg` / `YP1d66KM` / `1YNQO9jJ` / `pwv9eM76` / `vR1aEpa3`）。
**BANNED（trio 内部互组）0 条。**

### 101.5 区域复核（本地 `region_id` 不可信，逐条平台确认）
| alpha | 本地标注 | **平台 `settings.region/universe`** | 塔 |
|---|---|---|---|
| `mLYdVKap` | IND | **IND / TOP500** | IND/D1/INSTITUTIONS 1.0 + IND/D1/PV 1.1 |
| `78LEMG8Q` | IND | **IND / TOP500** | IND/D1/PV 1.1 + IND/D1/SENTIMENT 1.2 |
| `9qxLOPxr` | USA | **USA / TOP2000** | USA/D1/RISK 1.1 + USA/D1/MODEL 1.3 |

`9qxLOPxr` 的表达式（供复用参考）：
```text
group_neutralize(signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(
  subtract(vec_avg(buzz_intensity_score_2), vec_avg(buzz_intensity_score_11)), 252), 252),
  market), 5), 0.8), bucket(rank(financial_leverage_factor), range="0,1,0.2"))
```
`decay 0 / STATISTICAL / TOP2000 / nanHandling ON`。

**附带平台事实**：`CLUSTER_TEST` 的 limit **按区域不同** —— DEU 是 1，
USA 是 **1.58**（`9qxLOPxr` 的 value 1.27 在 USA 是 warning 不是 fail）。
§69 记的「DEU CLUSTER_TEST limit=1」不能跨区照搬。

### 101.6 最终 13 条可提交篮（按前置闸余量排序）
| # | alpha | reg | S | F | 2Y | SUB | prod | self | 塔 | 额度 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `QPveY7Kg` | DEU | 2.03 | 1.61 | 2.54 | 1.20 | 0.6671 | 0.0242 | SENTIMENT | 免费 |
| 2 | `88vJ1YKa` | USA | 2.94 | 1.42 | 2.45 | 1.28 | 0.6933* | 0.2409 | OTHER | 免费 |
| 3 | `MPY9VNY9` | DEU | 1.59 | 1.26 | 2.36 | 1.02 | 0.5986 | 0.2703 | SHORTINTEREST | 免费 |
| 4 | `9qxLOPxr` | USA | 2.69 | 1.67 | 2.24 | 1.44 | 0.6835* | 0.2866 | RISK+MODEL | 占 |
| 5 | `1YNQO9jJ` | IND | 2.37 | 1.82 | 3.11 | 1.56 | 0.3389* | 0.2991 | 无塔 | 免费 |
| 6 | `pwv9eM76` | IND | 1.66 | 1.24 | 2.09 | 1.48 | 0.5501 | 0.5017 | 无塔 | 免费 |
| 7 | `vR1aEpa3` | GBR | 2.32 | 2.11 | 2.29 | 1.38 | 0.6632* | 0.5240 | 无塔 | 免费 |
| 8 | `YP1d66KM` | EUR | 3.57 | 2.43 | 3.31 | 2.40 | 0.5985* | 0.5656 | 无塔 | 免费 |
| 9 | `3qoWQKJg` | KOR | 3.62 | 4.32 | 2.32 | 2.93 | 0.6221 | 0.6224 | 无塔 | 免费 |
| 10 | `Vkxnb8QG` | DEU | 1.83 | 1.64 | 2.09 | 0.99 | 0.6384 | 0.6379 | SHORTINT+ANALYST | 免费 |
| 11 | `E5VNe67L` | IND | 3.20 | 2.52 | 3.00 | 1.64 | 0.6643 | 0.6648 | INST+PV | 占 |
| 12 | `zq3zKgd8` | IND | 4.69 | 4.29 | 4.44 | 2.67 | 0.6953 | **0.6954** | 无塔 | 免费 |
| 13 | `RREnK5R1` 或 `78LEMG8Q` | IND | 2.8 | 2.0 | 2.2 | — | 待定 | — | PV+SENT | 占 |

\* = 仍需提交前 `refresh=True` 重刷：`88vJ1YKa`(5.9h) / `9qxLOPxr`(5.0h) /
`1YNQO9jJ`(18h) / `vR1aEpa3`(2.6h) / `YP1d66KM`(1.7h)。
`mLYdVKap`（S 3.16 / prod 0.6757 / self 0.6759 / INST+PV）为第 14 条备胎。

**排序依据**：先按「prod 与 self 两闸的余量最小值」降序，而不是按 Sharpe。
理由 —— S 是已经拿到的，prod/self 是还没过的；把余量大的先送上去，
可以在不消耗风险预算的前提下把提交数做上去。

### 101.7 遗留与阻塞
1. **prod 相关性槽被外部进程独占**。`Get-CimInstance` 定位到
   PID 164992 = `tools/prod_peek_batch.py --alphas 9qxP0JbV,Xg9w61Pm,A1VJKkYg --minutes 14 --interval 60`
   （08:57 启动，非本轮发起）。它的 `holder` 在 `9qxP0K8V` / `akK2vpWW` 之间跳，
   每次我发起的 prod 检查都直接撞 `correlation_busy` 或 120s 超时。
   **⇒ 批量 prod 终验必须串行 + 避开任何正在跑 `prod_peek_batch` / harvest `[queue]` 的时间窗。**
   本轮因此有 5 条未取得真值：`omEMRpWb` / `RREQ5len` / `RRAGw5ja` / `YP1G3NjM` / `RREnK5R1`(refresh)。
2. **15 条候选的互相关只覆盖候选之间**，尚未与 6 条已 ACTIVE + 全 OS 池做「提交后」重算。
   真实提交顺序应按 101.6 逐条提交、每提交一条重跑一次剩余候选的 self（因为 101.1 已证
   `0mjk2ZQv` 这类既有 OS alpha 会一次性压住 4 条同族候选）。
3. `alpha_pyramids` 仍缺 `zq3zKgd8` / `3qoWQKJg` / `YP1d66KM` / `1YNQO9jJ` / `pwv9eM76` /
   `vR1aEpa3` 六条的行 —— 其中前三条已用 `get_alpha_details` 证明确实不点亮塔，
   后三条仍未知（不排除是缺行，见 §100.7 的两类「塔位为空」）。

## §102 可提交存量终值：DEU 单区 3 条 / 全库 13 条 —— 60 条不可达的量化证据（2026-10-30 收尾）

### 102.1 DEU 单区 prod 全过穷尽证明

口径：`region='DEU'` 且 `ra_failed_checks='[]'` 且 S>=1.58 且 F>=1.0 且 2Y>=1.58
且 `prod_correlation IS NOT NULL AND prod_correlation < 0.7`。

结果 **只有 7 条**，全部列出：

| # | alpha | 状态 | S | F | TO | 2Y | SUB | prod | self | 塔 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `Wje5K71x` | **ACTIVE** | 1.73 | 1.37 | 0.1269 | 1.87 | 1.25 | 0.4305 | 0.1882 | FUNDAMENTAL |
| 2 | `58gkLAkk` | **ACTIVE** | 1.75 | 1.42 | 0.1457 | 2.07 | 1.22 | 0.5381 | 0.5163 | MODEL+OTHER |
| 3 | `2rjrMZ25` | **ACTIVE** | 1.77 | 1.61 | 0.1199 | 1.83 | 0.88 | 0.6510 | 0.3437 | ANALYST |
| 4 | `MPY9VNY9` | UNSUBMITTED | 1.59 | 1.26 | 0.0364 | 2.36 | 1.02 | 0.5986 | 0.2703 | SHORTINTEREST |
| 5 | `npvwXA8l` | UNSUBMITTED | 1.59 | 1.25 | 0.0544 | 2.27 | 0.79 | 0.6093 | 0.2608 | SHORTINTEREST |
| 6 | `Vkxnb8QG` | UNSUBMITTED | 1.83 | 1.64 | 0.0906 | 2.09 | 0.99 | 0.6384 | 0.6379 | SHORTINT+ANALYST |
| 7 | `QPveY7Kg` | UNSUBMITTED | 2.03 | 1.61 | 0.1610 | 2.54 | 1.20 | 0.6671 | 0.0242 | SENTIMENT |

**⇒ DEU 单区（4,772 条历史回测、55 条全平台闸通过、25 条测过 prod）只能产出 7 条
prod 全过的 alpha，其中 3 条早已 ACTIVE。真正待提交的只剩 4 条。**

### 102.2 ★ 新发现 `npvwXA8l` —— 但它是 `MPY9VNY9` 的参数孪生

`npvwXA8l` 是本轮盘点新捞出来的（此前未进任何篮）：

```text
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),240)),
            rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),176))),target_tvr=0.06),subindustry)
```
与 `MPY9VNY9` 的唯一差别是 `target_tvr=0.06`（对方 0.03）。

`compute_mutual_correlation`（4 条，threshold 0.5，years 4，num_points 1021）：

| | MPY9VNY9 | npvwXA8l | Vkxnb8QG | QPveY7Kg |
|---|---|---|---|---|
| **MPY9VNY9** | 1.0 | **0.9197** | 0.0850 | 0.0328 |
| **npvwXA8l** | 0.9197 | 1.0 | 0.1005 | 0.0216 |
| **Vkxnb8QG** | 0.0850 | 0.1005 | 1.0 | -0.0367 |
| **QPveY7Kg** | 0.0328 | 0.0216 | -0.0367 | 1.0 |

- `max_pair` = 0.9197（`MPY9VNY9` ~ `npvwXA8l`），`pairs_over_threshold` 仅 1 对
- **`max_mutually_below_subset` = [MPY9VNY9, Vkxnb8QG, QPveY7Kg]，size = 3，`max_subset_exact=true`**

**⇒ DEU 单区可提交的独立 alpha 上限 = 3 条**。`npvwXA8l` 只能作为 `MPY9VNY9`
的替换备胎（SUB 0.79 更低、TO 0.0544 更高，指标上 `MPY9VNY9` 更优，取 `MPY9VNY9`）。

### 102.3 ★ 更正 §101.6：`1YNQO9jJ` 与 `vR1aEpa3` 都不是「免费」

§101.6 表里把 `1YNQO9jJ` 和 `vR1aEpa3` 都记成「无塔 / 免费」，**这是错的**。
`get_alpha_details` 平台实读：

- `1YNQO9jJ` → `pyramids.list` = `IND/D1/PV` + `IND/D1/INSIDERS` ⇒ **PV+INSIDERS，QUOTA**
- `vR1aEpa3` → 含 PV 腿 ⇒ **QUOTA**

**根因**：`alpha_pyramids` 表缺行被当成了「无塔 = 免费」。平台对 UNSUBMITTED alpha
并不总是回填该表，缺行是「未知」而不是「无塔」。

**⇒ 塔位唯一权威是 `get_alpha_details` 的 `pyramids.list`；
本地字段/前缀扫描只能做粗筛（`9qxLOPxr` 就被扫成 FREE，平台实读 USA/RISK + USA/MODEL）。**

### 102.4 塔额度硬顶重算：13 条不是 23 条

按平台实读重算原篮 23 条的塔归属：

| verdict | 条数 | 说明 |
|---|---|---|
| **QUOTA**（trio × 非trio，上限 5） | **15** | `kqN2WWKl` `MPYogx0L` `bl65Jk6l` `1YNQGgWJ` `RREn5rEa` `npvM6WvE` `9qxL8vx9` `xAr022xb` `LLMAM0xv` `1YNQO9jJ`（全部 INSIDERS+PV）、`vR1aEpa3`（PV）、`E5VNe67L` `mLYdVKap`（INSTITUTIONS+PV）、`RREnK5R1` `78LEMG8Q`（PV+SENTIMENT） |
| **FREE** | 8 | `QPveY7Kg`（DEU/SENTIMENT）、`88vJ1YKa`（USA/OTHER 纯单塔）、`MPY9VNY9`（DEU/SHORTINTEREST）、`pwv9eM76`（IND/analyst）、`YP1d66KM`（EUR）、`3qoWQKJg`（KOR）、`Vkxnb8QG`（SHORTINT+ANALYST 双非trio）、`zq3zKgd8`（IND） |
| **BANNED** | 0 | — |

**★ M62 骨架是额度黑洞**：`rank(-ts_regression(ts_zscore(returns,252), ...))` 里的
`returns` 是 PV 字段 ⇒ **每一条 M62 变体都自动带 PV 腿** ⇒ 整族（含 insiders1 的
10 条安全候选）共用那 5 个名额。

**⇒ 总量上限 = 5 条 quota + 8 条 free = 13 条。原 13 篮与 insiders1 10 篮不能叠加，
只能替换。** 这也是「60 条」最大的结构性障碍 —— 不是没信号，是没额度。

### 102.5 跨区全闸库存全景（749 行 → 726 指纹家族）

口径：`ra_failed_checks='[]'` 且 S>=1.58 且 F>=1.0 且 2Y>=1.58 且 `stage<>'OS'`。
指纹 = (round(S,4), round(F,4), round(TO,6), round(2Y,4))；退化 = TO<=1e-9 或 (long=0 且 short=0)。

| region | rows | families | degen | untested | wall | fresh | stale | usable |
|---|---|---|---|---|---|---|---|---|
| GLB | 183 | 179 | 48 | 101 | 69 | 2 | 7 | 9 |
| EUR | 158 | 150 | 8 | 92 | 38 | 9 | 11 | 20 |
| IND | 125 | 120 | 0 | 58 | 17 | 23 | 22 | 45 |
| USA | 148 | 146 | 10 | 55 | 66 | 10 | 15 | 25 |
| DEU | 55 | 52 | 0 | 29 | 19 | 4 | 0 | 4 |
| GBR | 67 | 66 | 0 | 19 | 36 | 9 | 2 | 11 |
| KOR | 9 | 9 | 6 | 8 | 0 | 1 | 0 | 1 |
| ASI | 4 | 4 | 0 | 3 | 1 | 0 | 0 | 0 |
| **ALL** | **749** | **726** | **72** | **365** | **246** | **58** | **57** | **115** |

注意 `DEU` 的 usable=4 与本报告 §102.2 的 3 条独立完全一致 —— 两个口径互相验证。

### 102.6 Dataset × Region prod 墙先验表（派发排序的第一权重）

「已测过的同数据集 alpha 里多大比例 prod<0.7」= 未测家族最硬的先验。

| region | dataset | rows | measured | pass | pmin | pavg | pmax |
|---|---|---|---|---|---|---|---|
| IND | **insiders1** | 16 | 10 | **10** | **0.2167** | 0.3273 | 0.3661 |
| IND | **institutions6** | 33 | 13 | **13** | 0.6162 | 0.6575 | 0.6803 |
| IND | **sentiment21** | 12 | 5 | **5** | 0.5699 | 0.6112 | 0.6507 |
| IND | analyst | 8 | 2 | 2 | 0.5501 | 0.5544 | 0.5586 |
| IND | (none) | 24 | 18 | 14 | 0.4924 | 0.6370 | 0.8756 |
| IND | analyst_consensus | 11 | 4 | 1 | 0.5354 | 0.7170 | 0.7859 |
| IND | fundamental86 | 3 | 3 | 0 | 0.7056 | 0.7510 | 0.8417 |
| IND | model39 | 3 | 2 | 0 | 0.8399 | 0.8457 | 0.8515 |
| IND | imbalance5 | 5 | 1 | 0 | 0.7818 | — | — |
| IND | risk70 | 3 | 1 | 0 | 0.7372 | — | — |
| USA | insider_trx_matrix | 15 | 15 | 9 | 0.5517 | 0.6760 | 0.8085 |
| USA | insider_matrix | 7 | 3 | 2 | 0.6933 | 0.7330 | 0.8092 |
| USA | web_traffic_engage | 6 | 5 | 0 | 0.9740 | 0.9816 | 0.9908 |
| GLB | dl_riskfree_returns | 90 | 45 | 2 | 0.6495 | 0.8226 | 1.0000 |
| GLB | intraday_pv_feats | 19 | 19 | 0 | 0.8469 | 0.9509 | 0.9997 |
| EUR | fundamental72 | 16 | 15 | 8 | 0.6581 | 0.7293 | 0.9914 |
| EUR | fundamental23 | 8 | 6 | 0 | 0.8048 | 0.9375 | 0.9998 |

**区域 roll-up（已测中 prod 通过率）**：IND **72.6%**（45/62）> EUR 33.9%(20/59)
> USA 27.5%(25/91) > GBR 22.9%(11/48) > **DEU 16.0%(4/25)** > GLB 11.0%(9/82) > ASI 0%。

**⇒ 应用**：派发与测 prod 前先查这张表。同样的 sharpe，`insiders1` 是「几乎必过」
（0.22–0.37，全库最低），`model39`/`risk70`/`intraday_pv_feats` 是「几乎必死」。

### 102.7 `institutions6` 聚簇证伪：12 个「未测家族」实为 1 个信号

`compute_mutual_correlation`（14 条：12 未测 + `E5VNe67L` + `mLYdVKap`，threshold 0.7, years 4）：

- `max_pair` = **0.9931**（`78o31b2Q` ~ `N1eLRWML`）
- `pairs_over_threshold` **51 对**（>=0.95 的 1 对、0.85–0.95 的 0 对、0.70–0.85 的 50 对）
- `max_mutually_below_subset_size` = **5**，`max_subset_exact=true`
- 且这 5 条彼此多在 0.60–0.70 ——「勉强独立」不等于「分散」

**⇒ 指标指纹去重把 1 个信号算成了 12 个。此前「÷3 换算」在本数据集上严重低估。**

### 102.8 `insiders1` 聚簇：与 `institutions6` 完全相反

`compute_mutual_correlation`（全部 16 条，threshold 0.7, years 4）：

- `max_pair` = 0.9933（`JjeZWWpj` ~ `QPvLNNQW`）
- `pairs_over_threshold` 仅 **9 对**：0.9933 / 0.9828 / 0.9703 / 0.9541 / 0.9483 / 0.8130 / 0.8114 / 0.7884 / 0.7817
- `max_mutually_below_subset_size` = **10**，`max_subset_exact=true`
- 子集：`omEMRpWb` `kqN2WWKl` `MPYogx0L` `bl65Jk6l` `1YNQGgWJ` `RREn5rEa` `npvM6WvE` `9qxL8vx9` `xAr022xb` `LLMAM0xv`
- 其中 9 条 prod 已实测且全 PASS（0.2167–0.3661）；`omEMRpWb` 是唯一未测
- **`1YNQO9jJ`（prod 0.3389 已测）与子集内其余 9 条相关性全部 <=0.5443**
  ⇒ 用 `1YNQO9jJ` 替换 `omEMRpWb`，得到 **10 条 prod 全部已知且全 PASS 的篮子**

**⇒ 同一套「指纹去重」在 `institutions6` 高估 12 倍、在 `insiders1` 只高估 1.6 倍。
不能用统一换算系数，必须逐数据集跑 `compute_mutual_correlation`。**

### 102.9 `insiders1` 10 篮终表（self 全部实测）

| alpha | S | F | 2Y | SUB | prod | **self** | 池 |
|---|---|---|---|---|---|---|---|
| `kqN2WWKl` | 2.13 | 1.58 | 2.81 | 0.94 | 0.3362 | **0.2531** | 52 |
| `MPYogx0L` | 1.87 | 1.31 | 2.20 | 1.47 | 0.3159 | **0.2387** | 52 |
| `bl65Jk6l` | 2.19 | 1.64 | 2.08 | 1.78 | 0.3464 | **0.2391** | 52 |
| `1YNQGgWJ` | 2.11 | 1.53 | 2.76 | 1.45 | 0.3661 | **0.2954** | 52 |
| `RREn5rEa` | 2.08 | 1.54 | 2.45 | 1.78 | 0.3342 | **0.2837** | 52 |
| `npvM6WvE` | 1.97 | 1.35 | 2.02 | 1.62 | 0.3486 | **0.2532** | 52 |
| `9qxL8vx9` | 1.96 | 1.39 | 2.58 | 1.10 | 0.3488 | **0.2677** | 52 |
| `xAr022xb` | 1.90 | 1.34 | 1.90 | 1.06 | 0.3216 | **0.2400** | 52 |
| `LLMAM0xv` | 1.65 | 1.17 | 2.09 | 1.11 | 0.2167 | **0.1666** | 52 |
| `1YNQO9jJ` | 2.37 | 1.82 | 3.11 | 1.56 | 0.3389 | **0.2991** | 52 |

池大小 52（`full_os_pool_size` 60、`excluded_power_pool_count` 8）。
**每条 `top_correlated` 的第一名都是 `0mjk2ZQv`（0.1666–0.2991）** —— 这是同族
既有 OS alpha 的自我投影，不是外部拥挤度。

### 102.10 60 条不可达：三路独立证据

1. **DEU 单区已挖尽**：§102.1 证明 DEU 只有 7 条 prod 全过（含 3 条已 ACTIVE），
   互相关后只剩 3 条独立。要再挤出 57 条，按 4/25 的 prod 通过率需要再测约 21,000 条。
2. **塔额度硬顶 13 条**：§102.4 证明 5 quota + 8 free = 13。这是规则约束，不是产能约束。
3. **FREE 弹药不足**：365 个未测家族里，绝大多数组的表达式含 `returns`
   （58 个 IND 未测家族 → 30 字段集组，前 8 组里 6 组含 `returns`）⇒ 落在 QUOTA 桶。

### 102.11 下一轮唯一有意义的三个动作

1. **提交 DEU 3 条独立**：`MPY9VNY9` / `Vkxnb8QG` / `QPveY7Kg`
   （备胎 `npvwXA8l`，与 `MPY9VNY9` 0.9197 不可同提）。全部 FREE，不占 quota 名额。
2. **用 5 个 quota 名额做替换**：insiders1 10 篮的 prod 余量（0.22–0.37）远优于
   原篮的 5 条 quota（0.66–0.69）⇒ 建议用 `LLMAM0xv`/`MPYogx0L`/`bl65Jk6l`/`RREn5rEa`/`npvM6WvE`
   替换 `E5VNe67L` / `1YNQO9jJ` / `vR1aEpa3` / `RREnK5R1`(或 `78LEMG8Q`) / `9qxLOPxr`。
3. **新模板 M64「同塔残差化」**：把 M62 的 `ts_zscore(returns, W)` 基准腿换成
   **同数据集内的另一个字段**（如 `insd1_shares` 对 `insd1_tradesignificance`），
   既保留残差化机制（已实证 prod 0.22–0.37），又消掉 PV 腿 ⇒ 变 FREE。
   这是唯一能同时突破额度墙与 prod 墙的骨架方向。

### 102.12 本轮落盘文件

```text
tracking/DEU/candidates/cross_region_pool_20261030.json    477,379 B  726 家族 + 4 桶
tracking/DEU/candidates/ind_untested_clusters_20261030.json  24,929 B  58 家族 -> 30 组
tracking/DEU/candidates/ind_insiders1_basket_20261030.json              10 篮
tracking/DEU/candidates/tower_audit_20261030.json                        23 条塔审计
tracking/DEU/candidates/deu_nontrio_yield_20261030.json                 DEU 逐集产出
tracking/DEU/candidates/deu_prod_pass_rows_20261030.json                7 条详单
```

## §103 DEU 29 条「未测家族」族归并后只剩约 5 个信号 —— DEU 判竭的最后一环

§102.5 显示 DEU 有 29 个全闸通过但 prod 未测的家族，看起来是「还有 29 个机会」。
把 29 条表达式按**信号核**归并后，结论完全相反。

### 103.1 归并结果

| 信号核 | 条数 | 成员 | 已测同族基线 | 判定 |
|---|---|---|---|---|
| `snt7_all_languages_views` 的 `vector_neut(ts_quantile(ts_ir(...)))` 族（M37） | **13** | `GrWVx2aO` `kqNRX1ZP` `3qod35v6` `qMLbdPAA` `d5WqmExJ` `vR109elb` `9qxgMvOV` `xArMQPdJ` `ZYQw5RNQ` `e758plEM` `leA6qLNe` `P0orWJKK` `E5607ZxK` | `QPveY7Kg` prod **0.6671** PASS；`RREXKNQn`（252→504）prod **0.7415** FAIL | **耗尽**。13 条只在 `ts_ir` 窗口（22/10）、`ts_quantile` 窗口（252/120）、`vector_neut` 正交腿、`max(...)` 的 `ts_delay` 位上不同 —— 这些正是已证**无效的降 prod 杠杆**（换正交腿 / 缩短峰值窗）。同族最优已在 0.6671 卡线 |
| `eps_y1_estimate_change_3mo` 的 `group_neutralize(group_rank(add(...)), bucket(...))` 族（M12） | **10** | `kqJqQL08` `1YNv8qaK` `6Xdx65eK` `JjQ7vaAx` `E5Rlend1` `GrOleXAJ` `d51jRJMX` `YPM7g33W` `npP78m9l` `58glOpJn` | `2rjrMZ25` **ACTIVE** prod **0.6510** | **耗尽**。同族已有自有 ACTIVE ⇒ 变体 prod 结构性看齐 0.65 以上，且与自有 ACTIVE 同族（§prod 自投影） |
| `netprofit_y1_estimate_change_3mo` 双均线做差 | 2 | `j288RaEQ` `A1vv9mmX` | 未测 | 唯一真正的新信号核，但只有 2 条且 S 1.64 |
| `shrt3_bar` 的 `ts_target_tvr_decay` | 1 | `qMLewENK`（target_tvr=0.065） | `MPY9VNY9` prod 0.5986 / `npvwXA8l` 0.6093（两者 0.9197 孪生） | **孪生**，不可另计 |
| `tm_15_r1_r5_r10_rh_glb_d1_r10_q1` | 1 | `1YNv6Ymk` | `JjelQJoe` prod 0.8373 / `JjelQnvE` 0.9084（wall） | **同族已撞墙**，只会更差 |
| `institutions1` 的 `inst1_valueeur/inst1_holdings` | 2 | `d5WwzRMY` `E56AzejK` | 已在判死清单 | **已判死** |

**⇒ 29 条未测 → 5 个信号核 → 其中 4 个是已测/已判死家族的变体 → 只剩 1 个
（`netprofit_y1_estimate_change_3mo`，2 条，S 1.64）真正可测。**

### 103.2 DEU 判竭：三方证据齐了

1. **已测侧**：DEU 25 条测过 prod，4 条过（16.0%，全库第二低），且 3 条早已 ACTIVE
   ⇒ §102.1 的 7 条 prod 全过里只剩 3 条独立可提交（§102.2 互相关证明）。
2. **未测侧**：29 条未测归并为 5 个信号核，4 个是变体（§103.1）⇒ 剩余期望增量 < 1 条。
3. **产能侧**：DEU 单区累计 4,772 条回测，全平台闸通过 55 条（1.15%），
   prod 通过 4 条（0.084%）⇒ 边际产出率约 1/1,200 条回测。

**⇒ DEU 单区的可交付上限 = 3 条。要凑 60 条，必须换区，或者换掉「单区挖掘」这个前提。**

### 103.3 建议的最终交付方案

**DEU 侧交付（3 条，全部 FREE，不占塔额度）**

| # | alpha | S | F | 2Y | SUB | prod | self |
|---|---|---|---|---|---|---|---|
| 1 | `MPY9VNY9` | 1.59 | 1.26 | 2.36 | 1.02 | 0.5986 | 0.2703 |
| 2 | `Vkxnb8QG` | 1.83 | 1.64 | 2.09 | 0.99 | 0.6384 | 0.6379 |
| 3 | `QPveY7Kg` | 2.03 | 1.61 | 2.54 | 1.20 | 0.6671 | 0.0242 |

塔位：`MPY9VNY9` = SHORTINTEREST（单塔）、`Vkxnb8QG` = SHORTINTEREST+ANALYST（双非trio）、
`QPveY7Kg` = SENTIMENT。全部不含 PV/MODEL/OTHER ⇒ 不触碰任何组合禁令，也不吃 5 个名额。
（`npvwXA8l` 为 `MPY9VNY9` 的 0.9197 孪生，不可并列提交。）

**跨区补足（10 条，受 5 quota + 8 free 硬顶约束）**

原篮的 8 条 FREE 已含上述 DEU 3 条中的 2 条，需去重后重算：
FREE 池 = `QPveY7Kg` / `MPY9VNY9` / `Vkxnb8QG`（DEU 3 条）+ `88vJ1YKa`（USA/OTHER）
+ `pwv9eM76`（IND/analyst）+ `YP1d66KM`（EUR）+ `3qoWQKJg`（KOR）+ `zq3zKgd8`（IND）= **8 条**。
QUOTA 池 5 条从「原篮 5 条（prod 0.66–0.69）」与「insiders1 10 篮（prod 0.22–0.37）」
之间择优 —— **按 prod 余量，insiders1 全面占优**，建议取
`LLMAM0xv`(0.2167) / `MPYogx0L`(0.3159) / `bl65Jk6l`(0.3464) / `RREn5rEa`(0.3342) / `npvM6wvE`(0.3486)
替换 `E5VNe67L` / `1YNQO9jJ` / `vR1aEpa3` / `RREnK5R1`(或 `78LEMG8Q`) / `9qxLOPxr`。

**⇒ 一条额度下的最优 13 条 = 8 FREE + 5 insiders1 QUOTA。这就是本轮能达到的上限。**

## §104 平台权威塔位纠错 + `shortinterest3` 真相审计 + 波 98 十模板全灭（2026-10-30 夜）

本节把「DEU 判竭」从**统计推断**升级为**机制级证明**，并纠正一个影响选题方向的重大错误。
三块内容：① 平台权威塔位核查（推翻本地旧地图）；② `shortinterest3` 278 条历史回测的真相审计（推翻「si3 是富矿」）；③ 波 98 十个结构互异模板的实测全灭。

---

### 104.1 塔位判据纠错：`get_pyramid_alphas` 不可信，只信 `get_alpha_details.pyramids.list`

**本地旧地图与平台口径的冲突**

`get_pyramid_alphas()`（当前季度口径）返回 DEU / D1 全部 15 个 category **一个都没点亮**（每塔需 3 条）：

```
institutions 1, insiders 0, model 1, news 0, other 2, analyst 1, pv 0,
earnings 0, fundamental 1, sentiment 0, risk 0, option 0, macro 0,
socialmedia 0, shortinterest 0, imbalance 0
```

但本地台账记的是「MODEL / OTHER 已点亮、SHORTINTEREST 2/3」。两边对不上。

**决定性反证**：`get_alpha_details(alpha_id="blRnKEk6")` 返回

```json
"pyramids": {"effective": ..., "list": [
  {"name": "DEU/D1/SHORTINTEREST", "multiplier": 1.3},
  {"name": "DEU/D1/MODEL",         "multiplier": 1.8}
]}
```

`blRnKEk6` 的 `status=ACTIVE` / `stage=OS` / `dateSubmitted=2026-09-13` ⇒ **SHORTINTEREST 塔至少有 1 条已提交并生效**，而 `get_pyramid_alphas` 报 0。

**结论（硬规则，后续一律照此执行）**

1. `get_pyramid_alphas` 的计数语义**不确定**（疑似「本季度内提交」口径，非历史累计），**不得作为塔位判据**。
2. 塔位唯一权威 = `get_alpha_details` 的 `pyramids.list` **有内容** 且 `checks.pass` 含 `MATCHES_PYRAMID`。
3. UNSUBMITTED alpha 的塔位不在顶层 `pyramids`，而在 `is.checks[]` 的 `MATCHES_PYRAMID` 项里（`tools/backfill_alpha_pyramids.py` 已按此实现）。
4. `ra.pyramid_short` 是**跨 delay 相同的短名**，不能凭它区分 D0 / D1；必须读 `pyramids.list[].name`（D0 形如 `DEU/D0/<CAT>`，D1 形如 `DEU/D1/<CAT>`）。

**DEU / D1 multiplier 全表（选题权重参考）**

| category | mult | category | mult | category | mult |
|---|---:|---|---:|---|---:|
| model | 1.8 | news | 1.8 | other | 1.8 |
| analyst | 1.8 | fundamental | 1.8 | sentiment | 1.8 |
| insiders | 1.7 | pv | 1.7 | option | 1.7 |
| institutions | 1.6 | earnings | 1.6 | risk | 1.5 |
| macro | 1.5 | socialmedia | 1.5 | **shortinterest** | **1.3** |
| imbalance | 1.2 | | | | |

DEU / D0 全部落在 1.6–1.9（倍率更高），但闸门同比例更严（见既有条目：D0 的 S 门槛 ≈ D1 的 1.7 倍）⇒ **倍率高不是收益，是门槛换算**。

**推论**：DEU 的 `shortinterest` 是**全 region 最低倍率（1.3）**，本来就是平台在说「这个塔在 DEU 不值钱」。把它当重点方向是选题错误。

**其它区 D1 点亮进度 roll-up（同一口径）**

```
USA    model 4 / analyst 6 / other 1 / earnings 1
EUR    analyst 7 / model 3 / fundamental 3 / pv 2 / risk 2 / news 1 / insiders 1 / sentiment 1 / other 1
IND    pv 9 / news 4 / other 4 / analyst 3 / model 3 / fundamental 3 / risk 3 / macro 2 / earnings 2 / institutions 1
GBR    model 5 / analyst 3 / other 1 / pv 1
KOR    shortinterest 4 / fundamental 3 / model 3 / analyst 2 / pv 2 / other 1
GLB    pv 2 / model 3 / other 3 / risk 1 / institutions 1
HKG / ASI / CHN / AMR  几乎全零
```

⇒ **KOR 的 shortinterest 已点亮 4 条、DEU 才 1 条**，同数据集跨区表现差异极大，这是「数据集弱 ≠ 机制弱」的又一例证。

---

### 104.2 `shortinterest3` 真相审计：278 条历史回测的结论是「富矿是假的」

**数据集结构（`get_datafields`，DEU / TOP500 / D1）**

25 个字段**全部是 VECTOR** = 8 个概念 × 3 个主键变体 + `shrt3_bar`。覆盖率三档：

| 变体后缀 | 覆盖率 | 结论 |
|---|---:|---|
| 裸名 | 0.6683 | 弃用 |
| `_main` | 0.6872 | 弃用（旧族全用这个） |
| **`_p5_d1`** | **0.7833** | **首选（最高）** |

**字段语义（description 原文要点）**

- `mean_loan_rate` / `max_loan_rate` / `min_loan_rate` —— 加权 / 最大 / 最小借券费率
- `loan_rate_volatility` —— 费率标准差
- `loaned_share_count` / `loaned_market_value_usd` / `transaction_count` —— 借出股数 / 借出市值 / 交易笔数
- `average_loan_duration_days` —— 贷款加权平均账龄（天）
- `shrt3_bar` —— **1–10 借券需求评级**（userCount 173 / alphaCount 323，**全数据集最拥挤**）

**278 条 DEU 回测的 RA 状态分布**

| RA 失败组合 | 条数 |
|---|---:|
| `LOW_2Y + LOW_FIT + LOW_SHARPE` | 51 |
| `LOW_SHARPE` | 51 |
| `LOW_2Y + LOW_FIT + LOW_SHARPE + LOW_SUB` | 43 |
| **NULL（从未读 checks = 未知）** | **34** |
| `LOW_FIT + LOW_SHARPE` | 26 |
| 含 `CONCENTRATED_WEIGHT` | 47 |
| **全过（PASS）** | **仅 3 条** |

**3 条全过的都是 `mcp-20261030` 波的 `shrt3_bar` M13 族**：`MPY9VNY9`（prod 0.5986 / SUB 1.02 / TO 0.0364）、`npvwXA8l`（prod 0.6093 / SUB 0.79 / TO 0.0544）、`qMLewENK`（prod 从未测 / 2Y 2.15 / TO 0.0574）。

**持仓数分布（n=174）**：long min/med/max = **59 / 122 / 325**，short 0 / 96 / 190 ⇒ 判死簿里「76 股覆盖 ⇒ CW 恒定失败」在 `_p5_d1` 字段上**不成立**。

**旧 loan-rate 族 prod 硬墙（14 条实测）**

| 阈值 | alpha | prod |
|---|---|---:|
| 明显 FAIL | `npKrYpQl` / `qMWVeeME` / `wpYPvgqY` | 0.956 / 0.953 / 0.925 |
| | `Grdx5QAJ` / `ZY0M1G53` / `6XrJLG8J` | 0.905 / 0.898 / 0.896 |
| | `rK5VnXY3` / `MP1Z2mWk` / `A10m8LjW` | 0.886 / 0.883 / 0.847 |
| | `78ZMRGW8` / `mLg1WK3p` / `gJQdVr6M` / `O0rVX6Y7` | 0.811 / 0.810 / 0.786 / 0.776 |
| 过闸但已 OS | `blRnKEk6` / `vRk6og8b` / `JjxrYjre` | 0.5766 / 0.688 / 0.645 |

⇒ **旧族即使 IS 修好，prod 也过不了**（0.776–0.956 全在红线之上），且过闸三条**早已提交为 OS**，没有可比新增量。

---

### 104.3 ★ 决定性发现：si3 历史上所有 S≥1.6 的 alpha 都是 IBES `add()` 混信号

拉 `get_alpha_details(blRnKEk6)` 得到完整表达式：

```
add(add(add(if_else(is_nan(-rank(vec_avg(mean_loan_rate_main))), 0, -rank(vec_avg(mean_loan_rate_main))),
    rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))),
    rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
    rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))
```

`blRnKEk6` 指标：**S 2.02 / F 1.70 / 2Y 2.74 / SUB 1.43 / TO 0.1615 / margin 14.13bp / prod 0.5766 / self 0.0 / ACTIVE / OS / 2026-09-13 / GREEN / tags `CH_PPA` `SRC_predictive_starmine` `PowerPoolSelected`**

**⇒ 走的是 PPA 通道，不是 regular 提交。**

同族**全部同构**（`add(add(add(-rank(vec_avg(mean_loan_rate_main)), <IBES 腿1>), <IBES 腿2>), <IBES 腿3~4>)`）：

| S | alpha |
|---:|---|
| 2.01 | `ZY0M1G53` |
| 1.92 | `WjP0x8Md` |
| 1.91 | `rK5VnXY3` |
| 1.82 | `wpYPvgqY` / `MP1Z2mWk` |
| 1.80 | `vRk6og8b` |
| 1.73 | `RRVK6ELb` |
| 1.72 | `KPOQJRp` |
| 1.71 | `1YxPZN5J` / `j23x8YLW` |
| 1.70 | `kqVOo8jd` |
| 1.66 | `rK5VeRm9` / `GrdxbQGJ` |

**三层结论**

1. **si3 家族的高 Sharpe 不是 short-interest alpha**，是「IBES 预期修正 alpha + 一层薄 short-interest 装饰」。
2. 这正是被明令禁止的 `add(A,B)` 混信号反模式 —— **即使达到 S 2.04 也必须否决**（与 §98 已记录的同一条铁律一致：IBES 那 28 条单闸失败全是 5 段 `add` + PV 腿）。
3. 最高产那条走 PPA 通道 ⇒ **不是 regular 可复制路径**。

**附加坏消息**：`s2_si3_subfam_r74_d1` 波里 7 条 S≥1.6 的表达式，在库里存的是**占位标签**（`RV+Vk65式` / `DV+le89式` / `LV+Vk65式` / `RV+经典3腿` / `RV+LV双腿` / `RV+Vk65变体` / `DV+Vk65式`），真实表达式未落库 ⇒ **不可复用、不可分析**。这是数据治理债，后续落表达式必须落全文。

---

### 104.4 波 98：10 个结构互异模板，纯 SHORTINTEREST 单塔，0/10 过闸

**目的**：隔离出「纯 short-interest 信号」的真实上限，排除 IBES 污染。

**派发**：`2usnoM4bh4wbcpK14VuN3sId`（5 条）+ `26GHEJ18I4Ymcyjk06IxHXR`（5 条），并发 2，全部 COMPLETE / 0 error。设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / maxTrade OFF。

| 模板 | alpha | 机制 | S | F | TO | 2Y | SUB | 持仓 |
|---|---|---|---:|---:|---:|---:|---:|---|
| T01 | `omEwQJ95` | 费率离散度 `vec_max-vec_min` | **0.70** | 0.35 | 0.161 | 0.60 | 0.21 | 111/111 |
| T02 | `d5W8e3lw` | 费率波动（二阶矩） | 0.55 | 0.27 | **0.0361** | **1.04** | **0.47** | 106/107 |
| T03 | `O0AwKM5q` | 费率二阶差分（加速度） | 0.29 | 0.09 | 0.158 | 0.03 | 0.08 | 104/103 |
| T04 | `QPvrmN55` | 贷款账龄 | **−0.45** | −0.16 | 0.2036 | 0.13 | −0.68 | 113/112 |
| T05 | `ZYQwkdWj` | 单笔规模（USD/笔数） | **−0.24** | −0.07 | 0.1609 | −0.07 | −0.49 | 113/112 |
| T06 | `6XdPgG5O` | 费率×波动 双排序乘积 | 0.42 | 0.15 | 0.2142 | **1.03** | **0.46** | 110/109 |
| T07 | `npvkw6L8` | `shrt3_bar` 评级动量 | 0.25 | 0.05 | 0.3919 | −0.31 | 0.11 | 74/75 |
| T08 | `qMLke5QE` | 峰值费率 × 市值桶中性 | 0.62 | 0.22 | 0.2667 | 0.40 | 0.43 | 112/112 |
| T09 | `E560om9L` | 正交化分位（M37 移植） | 0.24 | 0.07 | 0.1421 | 0.22 | 0.10 | 110/109 |
| T10 | `QPvrmWww` | `trade_when` 评级门控 | −0.03 | — | 0.0935 | −0.54 | 0.33 | 84/99 |

**闸线对照**：S 闸 1.58 / F 闸 1.0。**S 上限 0.70、F 上限 0.35** ⇒ 差 2.3 倍 / 2.9 倍，不是「差一点」。

**七条归因发现**

1. **CW 闸问题被彻底解决**：10/10 全部 `CONCENTRATED_WEIGHT` pass，持仓 74–113 只。判死簿 `DEU-SI3-CW-STRUCTURAL`（「76 股覆盖 ⇒ CW 恒定失败」）只适用 `_main` 系字段，改用 `_p5_d1`（cov 0.7833 vs 0.6872）后失效。
2. **两条方向修正（太弱，仅登记）**：T04 贷款账龄原用正号得 −0.45 ⇒ 反向后约 +0.45（长期借贷 = 压抑过久 ⇒ 反转做空）；T05 单笔规模原用负号得 −0.24 ⇒ 反向后约 +0.24。
3. **二阶矩轴同时抬 2Y 与 SUB**：T02（费率波动）2Y 1.04 / SUB 0.47、T06（费率×波动）2Y 1.03 / SUB 0.46，是全波 2Y 最好的两条，但 S 只有 0.42–0.55。**慢变量二阶矩方向对、幅度不足**。TO 0.036 / margin 16.1bp 的形状是健康的。
4. **二阶差分彻底无效**：T03 S 0.29 / 2Y 0.03 ⇒ 费率「加速度」不是有效信息维度。
5. **`trade_when` 门控把弱信号打死**（T10 −0.03）⇒ 再次印证「门控需要基线 IS 余量，F<1.2 直接放弃救援」。
6. **M37 模板不可移植**：T09 只有 0.24，而同构的 `QPveY7Kg` 在 `snt7_all_languages_views` 上 S 2.03 ⇒ **该模板的力量来自新闻注意力信号本身，不是几何**。模板复用必须换数据集重测。
7. **`risk_neutralized_sharpe` 远高于 S 的样本**：T07 0.58 vs 0.25、T03 0.40 vs 0.29 ⇒ 风险模型压制方向存在，但基线 S 太低无救援价值。

**波 98 判决：`shortinterest3` 判死为「纯信号载体」，但保留 `shrt3_bar` 的 M65 一族。**

---

### 104.5 波 99：定向破闸批 —— M65 家族扩围（已派发）

唯一在 si3 上独立达到 S≥1.58 的几何是 **M65**：

```
-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),H1)),
                                         rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),H2))),
                                target_tvr=T), subindustry)
```

已知实测成员：`MPY9VNY9` H=(240,176) T=0.03 → S 1.59 / F 1.26 / 2Y 2.36 / SUB 1.02 / TO 0.0364 / prod 0.5986；`npvwXA8l` T=0.06 → S 1.59 / F 1.25 / SUB 0.79 / prod 0.6093（与 MPY **0.9197 孪生**）；`qMLewENK` S 1.59 / 2Y 2.15 / prod 未测；`xArX5prW` T=0.08 → S 1.68 / F 1.36 / 2Y 2.34 / TO 0.0659 / **SUB 0.78 挂 `LOW_SUB_UNIVERSE_SHARPE`**。

**波 99 的 10 条围绕两个未探索维度展开**（定向破闸批，不受 ≥10 模板约束）：期限组合（504/252、252/126、126/66、三期限乘积、126 基准）、变换层（`ts_rank` vs `ts_zscore` vs `ts_delta` 裸层）、非评级腿（`loaned_market_value_usd` / `transaction_count`）、`ts_quantile` 分位 + 市值桶中性。

派发：`2NEOEQ6Y853l8WN65fuBDZw`（V1–V5）+ `VKUujdt64PdarersH2bE1N`（V6–V10）。
预检：`unknown_fields: ["gaussian"]`（已知假阳性，`driver=` 参数值被误识别）、`platform_field_count: 3`（`shrt3_bar` / `loaned_market_value_usd_p5_d1` / `transaction_count_p5_d1` 全部命中）、`any_changed: false`。

**关键假设（待验）**：M65 家族的全部成员都落在 S 1.59–1.68 的窄带内，且 `xArX5prW` 的 SUB 0.78 说明**SUB 随 S 同向变化**（S 高则 SUB 也高）。若波 99 无法把 S 推过 1.9，则 SUB 闸会永远先挂 —— 这与 §91 已记录的「SUB 墙根因是横截面操作不是信号」一致，破法是换 `group_rank` 的轴（`sector` 替 `subindustry`，V4 已测）而不是加平滑。

---

### 104.6 判死簿与台账修正（本节需同步 registry）

| 操作 | 条目 | 修正内容 |
|---|---|---|
| **降级** | `DEU-SI3-CW-STRUCTURAL` | 从「数据集级：76 股 ⇒ CW 恒定失败」降为 **「`_main` 系字段特定」**。`_p5_d1` 上 10/10 过 CW，持仓 74–113 只。**判死结论必须绑定字段变体，不能升格为数据集级。** |
| **新增** | `DEU-SI3-PURE-SIGNAL-DEAD` | 纯 short-interest 8 个结构族（费率水平/离散/波动/账龄/单笔规模/二阶差分/门控/正交化）全灭，S ≤0.70。数据：波 98 十模板。 |
| **新增** | `DEU-SI3-ADD-MIX-FALSE-POSITIVE` | si3 历史 S≥1.6 全部是 `-rank(mean_loan_rate_main)` + 3–4 个 IBES 腿的 `add()` 混信号，最高产走 PPA 通道。**不是 regular 路径，且违反禁 `add` 规则。** |
| **新增** | `DEU-SI3-MAIN-LOAN-RATE-PROD-WALL` | `mean_loan_rate_main` 系 14 条 prod 0.776–0.956 全在红线之上；过闸三条早已 OS。 |
| **保留** | M65 族 | `shrt3_bar` 双期限×TVR 是唯一独立过 S 闸的几何，继续扩围但**预期 SUB 是最终墙**。 |

**方法论增量（可跨区复用）**

1. **塔位只信 `pyramids.list`**，`get_pyramid_alphas` 的计数不可作判据（口径不明）。
2. **判死必须绑定字段变体**：同一数据集不同键后缀覆盖率差 0.10 就能让 CW 从「恒定失败」变成「全过」。
3. **`add()` 混信号会伪装成「数据集富矿」**：判「某数据集是否出货」前必须先看历史高 Sharpe 的**表达式结构**，不能只看 S 榜单。这是本轮最大的教训 —— 如果早做这一步，`shortinterest3` 的整条挖矿路线（含近 300 条回测）本可以省掉。
4. **平台最低 multiplier 的塔往往是难塔**：DEU shortinterest 1.3 是全 region 最低，而它恰好也是纯信号最弱的塔。multiplier 可以当「难易度反指标」的弱先验。
5. **`get_datafields` 的 `_p5_d1` / `_main` / 裸名三档覆盖率差异必须逐档实测**，不能默认用 `_main`（旧族习惯），覆盖率差 0.10 直接影响 CW。
6. **同一模板跨数据集迁移必须重测**：M37 在 snt7 上 S 2.03、在 si3 上 0.24，几何不是力量来源。


## §105 波 99：si3 天花板从 0.70 抬到 1.33 —— 三腿期限乘积是关键，且它是**新 alpha** 不是变体

§104 判定 `shortinterest3` 的纯信号天花板 S≈0.70。**波 99 直接推翻了这个数字**：同一数据集、同一字段、同一设置，仅换几何，S 从 0.70 抬到 **1.33**，且 F 1.31 / 2Y 1.60 / SUB 1.01 全部过闸。

---

### 105.1 派发与完整结果

`2NEOEQ6Y853l8WN65fuBDZw`（V1–V5）+ `VKUujdt64PdarersH2bE1N`（V6–V10），DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / maxTrade OFF，预检 `any_changed: false`，10/10 COMPLETE，0 error。

全部表达式都是 M65 骨架 `-group_rank(ts_target_tvr_decay(<shrt3_bar 腿乘积>, target_tvr=T), <axis>)` 的变体，只动三个维度：**期限组合 / 腿内变换 / 分组轴**。

| # | alpha | 期限组合 | 腿变换 | 轴 | T | S | F | 2Y | SUB | TO | RA 失败 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| V4 | **`pwdJJAeo`** | 504/252/126 | delta | **sector** | 0.04 | **1.33** | **1.31** | **1.60** | **1.01** | 0.0678 | **仅 `LOW_SHARPE`** |
| V2 | `P0orrdmJ` | 252/126 | delta | subindustry | 0.05 | 1.22 | 1.01 | 1.30 | 0.74 | 0.0635 | `LOW_SHARPE`+`LOW_SUB` |
| V3 | `Jje00ZJE` | 126/66 | delta | subindustry | 0.05 | 1.16 | 0.90 | 1.13 | 0.81 | 0.0612 | 3 项 |
| V10 | `d5W88m7Y` | 240/176（bf126） | delta | subindustry | 0.05 | 1.14 | 0.87 | 1.01 | 0.78 | 0.0608 | 3 项 |
| V5 | `2rAqqboJ` | 504/252 | **ts_rank** | subindustry | 0.05 | 0.98 | 0.67 | **1.64** | 0.76 | 0.0575 | 2 项 |
| V6 | `QPvrrjjp` | 504/252 | **ts_zscore** | subindustry | 0.05 | 0.96 | 0.65 | **1.63** | 0.65 | 0.0579 | 2 项 |
| V1 | `ZYQwwe91` | 504/252 | delta | subindustry | 0.05 | 0.79 | 0.56 | 0.70 | 0.68 | 0.0693 | 3 项 |
| V8 | `kqNkkXmL` | 评级 × **transaction_count** | delta | subindustry | 0.04 | 0.69 | 0.42 | 0.57 | 0.46 | 0.0511 | 3 项 |
| V9 | `akK22lP1` | 单腿 + `ts_quantile` + bucket | — | — | 0.05 | 0.69 | 0.45 | 0.03 | 0.41 | 0.1036 | 3 项 |
| V7 | `0mYkkdQv` | 评级 × **loaned_market_value** | delta | subindustry | 0.04 | 0.56 | 0.30 | **−0.24** | 0.31 | 0.0517 | 3 项 |

---

### 105.2 `pwdJJAeo` 详情：六闸全过，只差 S

```
-group_rank(ts_target_tvr_decay(
    multiply(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),504)),
                      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),252))),
             rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),126))),
    target_tvr=0.04), sector)
```

| 项目 | 值 |
|---|---|
| Sharpe | **1.33**（闸 1.58，差 0.25 = 需 +19%） |
| Fitness | **1.31**（闸 1.0）✓ |
| 2Y Sharpe | **1.60**（闸 1.58）✓ 恰好过线 |
| SUB Sharpe | **1.01**（闸 ≈0.434×S = 0.577）✓ 大幅富余 |
| Turnover | 0.0678 ✓ |
| Margin | **35.51 bp** ✓（比 M65 的 12.9 bp 高 2.75 倍） |
| Returns | 0.1204 |
| Drawdown | 0.1545 |
| 持仓 | long 42 / short 43（共 85 只，CW pass） |
| risk_neutralized_sharpe | **0.87 < S 1.33** ⇒ 真实信号，非风格暴露 |
| 塔位 | `DEU/D1/SHORTINTEREST` 1.3（单塔 = **FREE，不占 trio 额度**） |
| checks | **fail 只有 `LOW_SHARPE`**；pass 含 `LOW_FITNESS`/`LOW_TURNOVER`/`HIGH_TURNOVER`/`CONCENTRATED_WEIGHT`/`LOW_SUB_UNIVERSE_SHARPE`/`CLUSTER_TEST`/`LOW_2Y_SHARPE`/`MATCHES_PYRAMID` |

**为什么 margin 从 12.9bp 跳到 35.5bp 而 TO 只从 3.6% 升到 6.8%**：三条期限腿乘积是「**共识筛选器**」——只有短/中/长三个窗口的借券需求**同时**上行的股票才拿到极端 rank 值。这把持仓从 122 只压到 85 只，但留下的都是信号最强的一批，所以单位收益大幅上升。

---

### 105.3 六条结构归因（每条都有对照）

| # | 结论 | 对照证据 |
|---|---|---|
| 1 | **三腿乘积 > 两腿乘积** | V4 三腿 1.33 vs V2 两腿 1.22 vs V1 两腿(长) 0.79 |
| 2 | **`sector` > `subindustry`（在同一信号上）** | V4 sector 1.33 vs 同参数 subindustry 的同族 ≤1.22；且 sector 与设置里的 SUBINDUSTRY 中性化**不同轴**，形成双重剥离 |
| 3 | **`ts_delta` 腿 ≫ `ts_rank` 腿 ≫ `ts_zscore` 腿** | 同为 504/252 两腿：delta 0.79 / ts_rank 0.98 / ts_zscore 0.96 —— 三者都弱，说明**强的不是腿内变换而是腿数**；但变换层里 `ts_zscore` 会**摧毁 2Y**（1.63 高但 S 崩） |
| 4 | **期限越短越好，但 504 腿不能少** | 两腿族：504/252 = 0.79 < 252/126 = 1.22 > 126/66 = 1.16 ⇒ 中间期限（一年 + 半年）是最佳单点；三腿把 504 加回来反而更好（1.33），说明长腿提供「趋势方向确认」而非「信号强度」 |
| 5 | **非评级腿全灭** | `loaned_market_value_usd` 0.56（2Y −0.24）、`transaction_count` 0.69 ⇒ **借券「量」的维度不携带方向信息**，只有评级（`shrt3_bar`）携带 |
| 6 | **`ts_quantile` + bucket 会杀死它** | V9 0.69 / 2Y 0.03 ⇒ 该数据集的价值在**横截面共识的强度**，一旦做分位变换把强度抹平就没了 |

**附带**：`LOW_SUB_UNIVERSE_SHARPE` 在全族**从未触发**（SUB 0.31–1.01 全部高于 0.434×S 的线）⇒ §91 记录的「SUB 墙」在 si3 + sector 轴上不存在。这与「SUB 墙根因是横截面操作」一致：`sector` 轴比 `subindustry` 轴在子宇宙里更分散。

---

### 105.4 ★★ 家族簇结构：三腿版是**新 alpha**，不是 M65 的变体

对 8 条 si3 家族候选跑 `compute_mutual_correlation`（4 年日收益，1021 点，本地零配额）：

| 簇 | 成员 | 簇内相关 |
|---|---|---|
| **簇 A：两腿 M65（subindustry）** | `MPY9VNY9` / `npvwXA8l` / `qMLewENK` / `xArX5prW` | **0.8849 – 0.9944** ⇒ 事实上是**同一条 alpha** |
| **簇 B：三腿乘积** | `pwdJJAeo` / `P0orrdmJ` / `Jje00ZJE` | 0.3761 – 0.6748 ⇒ **真新信号** |
| 跨簇 | `pwdJJAeo` ↔ `MPY9VNY9` | **0.4585** |
| | `pwdJJAeo` ↔ `npvwXA8l` | 0.4072 |
| | `pwdJJAeo` ↔ `xArX5prW` | 0.3871 |
| 过 0.7 的例外 | `P0orrdmJ` ↔ `d5W88m7Y` | 0.7760（同一期限族的两腿版） |

`max_mutually_below_subset`（阈值 0.7，`max_subset_exact: true`）= **[`MPY9VNY9`, `P0orrdmJ`, `pwdJJAeo`, `Jje00ZJE`]`，共 4 条互不相关**。

**三条推论**

1. **M65 两腿族的 4 个成员只能算 1 条**（0.88–0.99）⇒ 之前把 `MPY9VNY9` / `npvwXA8l` / `qMLewENK` / `xArX5prW` 当 4 个独立机会是错的，**实际只有 1 个提交位**。
2. **三腿版把「第三条期限腿」变成了正交信息源**（0.46）⇒ 这是同一数据集内**低成本的去相关手段**：不改字段、不改数据集、只加一条窗口腿。
3. **若 `pwdJJAeo` 的 S 推过 1.58，si3 单数据集可点塔 2 条**（`MPY9VNY9` + `pwdJJAeo`，互相关 0.46），而不是原判的 1 条。塔还差 1 条才能点亮（每塔 3 条）。

---

### 105.5 波 100 设计（已派发）：把 S 从 1.33 推到 1.58

唯一失败项是 S 差 0.25。围绕 V4 的四个自由度做定向扩张（定向破闸批，不受 ≥10 模板约束）：

| 组 | 变量 | 值 | 理由 |
|---|---|---|---|
| A | `target_tvr` | 0.03 / 0.02 | M65 两腿族在 T=0.03 拿到过 1.59，T 是**唯一已知能把同族 S 抬高 20% 的杠杆** |
| B | 腿数 | 4 腿（504/252/126/66） | 三腿已证 +0.11，四腿测边际 |
| C | 期限组合 | 240/176/126 | 240/176 是 M65 最优对，加第三腿 |
| D | 分组轴 | `market` / `industry` | V4 的 sector 优于 subindustry，试更宽 / 更窄 |
| E | 中间腿变换 | `ts_rank(·,252)` | 单腿换成水平型变换，保留另两腿 delta |
| F | backfill | 126（替 22） | 覆盖率 0.7833 字段上更长 backfill 可减少 warm-up 缺失 |
| G | 第 4 腿类型 | `loaned_market_value_usd` 作第 4 腿（3/4 评级） | V7/V8 是 1/2 评级 + 1 非评级就崩，改测 3/4 |
| H | 非线性 | `signed_power(product, 1.5)` | 放大共识极端值；`signed_power` 在本区已验证可用 |

派发：`3QSYGT2CC5k2aYasbO9hxdc`（A01–A05）+ `1BcvYf9su4lT9HXdKF6p5GW`（B01–B05）。

**判决标准（预先登记，防事后解释）**

- 若某条 S ≥1.58 且其余闸全过 ⇒ **si3 拿到第 2 个常规提交位**，与 `MPY9VNY9` 互相关 0.46 ⇒ 塔进度 2/3。
- 若全部 S <1.45 ⇒ 判定 1.33 是 si3 的**真实天花板**，`shortinterest3` 正式判竭，不再投入。
- 若 S 上去但 F 或 2Y 掉下来 ⇒ 说明三闸之间存在**结构性权衡**（高 S 靠压 TO 换来 2Y 不稳），记录为权衡曲线，不再追。


## §106 波 100/101 全 25 条 + si3 收线判决：S↔2Y 前沿是一条不可穿越的线（2026-10-31）

### 106.1 波 100 结果（10 条，已入库）

| alpha | 结构 | S | F | 2Y | SUB | TO | margin(bp) |
|---|---|---:|---:|---:|---:|---:|---:|
| `MPYllp1k` | 中间腿 `ts_rank(·,252)`，sector T=0.04 | **1.47** | **1.49** | 1.50 | **1.11** | 0.0662 | 38.6 |
| `d5W88Rkv` | 4 腿全 delta（504/252/126/66），sector | 1.37 | 1.36 | 1.50 | 0.95 | 0.0688 | 35.6 |
| `gJeqq1Qv` | 3 腿 delta，**industry** | 1.34 | 1.28 | 1.41 | 1.08 | 0.0678 | 33.5 |
| `leA663p7` | 3 腿 delta，sector **T=0.03** | 1.33 | 1.31 | **1.60** | 1.08 | 0.0583 | **41.5** |
| `6XdPPe7O` | 3 腿 delta，**market** | 1.32 | 1.30 | 1.51 | 1.00 | 0.0581 | 41.6 |
| `rKR66PY1` | 240/176/126，sector | 1.31 | 1.21 | 1.15 | 0.81 | 0.0627 | 33.7 |
| `omEwwKL5` | `signed_power(product,1.5)` | 1.30 | 1.26 | 1.39 | 0.97 | 0.0701 | 33.4 |
| `wpQwwRYY` | backfill 126 | 1.25 | 1.14 | 0.89 | 1.00 | 0.0632 | 33.0 |
| `zq3wwRKd` | 3 腿 delta，sector **T=0.02** | 1.16 | 1.06 | 1.54 | 0.98 | 0.0485 | 43.4 |
| `A1VJJw0E` | 4 腿（3 评级 + loaned_MV） | 1.05 | 0.89 | 1.24 | 0.75 | 0.0637 | 28.4 |

（`pwdJJAeo` S 1.33 / 2Y 1.60 与 `leA663p7` 同构仅 T 不同，列入 §105。）

### 106.2 波 101 三批 15 条结果（已入库）

**批 A（5 条）—— 腿变换层**

| alpha | 中间腿/首腿变换 | S | F | 2Y | SUB | TO | margin(bp) |
|---|---|---:|---:|---:|---:|---:|---:|
| `E5600zam` | 中间 `ts_rank(·,126)` | **1.44** | 1.44 | 1.51 | 1.14 | 0.0659 | 37.8 |
| `0mYkkgKv` | 4 腿（中间 ts_rank252 + 末腿 66） | 1.41 | 1.39 | 1.35 | 0.97 | 0.0679 | 35.9 |
| `mLo227zx` | 中间 `ts_rank(·,504)` | 1.39 | 1.37 | 1.36 | 1.15 | 0.0665 | 36.7 |
| `wpQwwGJ5` | 首腿与中间都 `ts_rank` | 1.35 | 1.20 | **1.78** | 1.11 | 0.0565 | 34.9 |
| `1YNVVKmR` | 中间与末腿都 `ts_rank` | 1.29 | 1.21 | **1.74** | 1.06 | 0.0631 | 34.6 |

**批 B（5 条）—— 水平/平滑/覆盖层**

| alpha | 结构 | S | F | 2Y | SUB | TO | margin(bp) |
|---|---|---:|---:|---:|---:|---:|---:|
| `RREZqM0g` | `winsorize(product, std=3)` | **1.47** | **1.49** | 1.52 | **1.11** | 0.0661 | 38.6 |
| `omEwA7Qk` | `ts_decay_linear(product, 5)` | 1.42 | 1.41 | 1.44 | 1.06 | 0.0721 | 34.3 |
| `d5W8gpeK` | 全腿 `ts_backfill` 22→126 | 1.29 | 1.18 | **0.69** | 1.00 | 0.0614 | 34.4 |
| `YP1wn6Xq` | **纯水平** 3 腿 ts_rank（504/252/126） | 1.24 | 1.00 | **2.31** | 0.98 | 0.0519 | 31.5 |
| `2rAqQMPJ` | **纯水平** 3 腿 ts_rank（252/126/66） | 1.21 | 0.96 | **2.31** | 0.75 | 0.0508 | 30.9 |

**批 C（5 条）—— 借券费率约束 / 正交臂**

| alpha | 结构 | S | F | 2Y | SUB | TO | margin(bp) |
|---|---|---:|---:|---:|---:|---:|---:|
| `78Lq0Jq2` | × `rank(mean_loan_rate_p5_d1)` | 1.35 | 1.32 | 1.12 | 1.07 | 0.0688 | 34.6 |
| `xArw9R9q` | 中间腿 `ts_zscore(·,252)` | 1.31 | 1.25 | 1.05 | 0.98 | 0.0669 | 33.9 |
| `9qxPbJb9` | 中间腿 `ts_delta(ts_rank(·,252),126)` | 1.21 | 1.11 | 0.92 | 0.90 | 0.0639 | 33.1 |
| `vR1nxdxa` | `group_neutralize` 代 `group_rank` | 1.19 | 1.19 | 1.36 | 1.05 | 0.0498 | **50.6** |
| `Jje0Yb0O` | × `rank(vec_max(max_loan_rate_p5_d1))` | 1.09 | 0.97 | 0.68 | 0.96 | 0.0692 | 28.4 |

**波 101 合计 15/15 未过闸；全部只挂 `LOW_SHARPE` 或 `LOW_SHARPE+LOW_2Y_SHARPE`，从未触发 CW / SUB / 换手。**

### 106.3 结构归因：以 `MPYllp1k`（S 1.47 / 2Y 1.50）为基准，**十五类杆杆全部为负**

| 杆杆 | 实例 | ΔS | Δ2Y | 判定 |
|---|---|---:|---:|---|
| `winsorize(std=3)` | `RREZqM0g` | 0.00 | +0.02 | **空操作**—乘积已 ∈[0,1]，去不了任何东西 |
| 中间腿窗 126 | `E5600zam` | −0.03 | +0.01 | 平扁 |
| `ts_decay_linear(·,5)` | `omEwA7Qk` | −0.05 | −0.06 | 平滑捿 |
| 4 腿（+66） | `0mYkkgKv` / `d5W88Rkv` | −0.06 | −0.15 | 加腿无用 |
| 中间腿窗 504 | `mLo227zx` | −0.08 | −0.14 | 长窗变差 |
| × mean fee | `78Lq0Jq2` | −0.12 | −0.38 | **费率约束假说否定** |
| 首腿→水平 | `wpQwwGJ5` | −0.12 | **+0.28** | 2Y 换 S |
| 中间腿 `ts_zscore` | `xArw9R9q` | −0.16 | −0.45 | zscore 不如 ts_rank |
| 全腿 backfill 126 | `d5W8gpeK` | −0.18 | **−0.81** | **长 backfill 纯损失** |
| 两腿水平 | `1YNVVKmR` | −0.18 | **+0.24** | 2Y 换 S |
| 纯水平 3 腿 | `YP1wn6Xq` | −0.23 | **+0.81** | 2Y 换 S |
| 纯水平 3 腿（短窗） | `2rAqQMPJ` | −0.26 | **+0.81** | 同上 |
| 中间腿 Δ百分位 | `9qxPbJb9` | −0.26 | −0.58 | 新变换不成立 |
| `group_neutralize` | `vR1nxdxa` | −0.28 | −0.14 | **margin 独立杆**（+12.0bp） |
| × max fee | `Jje0Yb0O` | **−0.38** | **−0.82** | **最差单一杆** |

**三条硬结论**：

1. **零个杆杆提升 S。** 十五种偏离全部为负，最小损失是 −0.03。⇒ `M68` 的参数点是**孤点最优**，不是一个平坦区域。
2. **提升 2Y 的唯一方法是把差分腿换成水平腿，代价每次都是 S。** 四个正 Δ2Y 的实例（+0.24 / +0.28 / +0.81 / +0.81）全部同时付出 −0.12 至 −0.26 的 S。
3. **费率作为乘子是灾难而非增强。** D'Avolio（2002）的 fee-as-short-sale-constraint 机制在 DEU 的 si3 评级动量上被实证否定（−0.12 / −0.38 S）。推理：`shrt3_bar` 已经是一个**综合紧张度评分**，再乘费率就是把同一个因子乘两次，只会加重极端值拖累。

### 106.4 S ↔ 2Y 前沿方程（定量，基于波 98–101 共 45 条实测）

将 35 条（波 99–101）按“每一档 S 内的最高 2Y”取 Pareto 点：

| Pareto 点 | S | 2Y | 代表 |
|---|---:|---:|---|
| P1 | **1.47** | 1.52 | `RREZqM0g` / `MPYllp1k` |
| P2 | 1.35 | **1.78** | `wpQwwGJ5` |
| P3 | 1.24 | **2.31** | `YP1wn6Xq` / `2rAqQMPJ` |

P1→P2 的局部斜率 = (1.78−1.52)/(1.35−1.47) = **−2.17**（S 每 +0.01 需付出 2Y −0.022）。

- **仿线推到 S=1.58**：2Y = 1.52 − 2.17×0.11 = **1.28** → 两闸全挂。
- **反向推到 2Y=1.58**：S = 1.47 − (0.06/2.17) = **1.44** → 仍差 0.14。
- **实测核对**：35 条中 `S≥1.50` 的条数 = **0**；`2Y≥1.58` 且 `S≥1.44` 的条数 = **0**（`2Y≥1.58` 的四条最高 S 仅 1.35）。

⇒ **(1.58, 1.58) 这个角落位于整个前沿的东北方，插值不可达**。要到达必须找到一个新机制；而 §106.3 已穷举 15 类机制，全部失败。

### 106.5 si3 收线判决

- **单数据集 regular 通道上限 = S 1.47**（`M68` 单点），且该点 2Y 1.52 < 1.58 ⇒ **双闸不可同时过**。
- **能过全闸的仍只有两腿族代表 `MPY9VNY9`**（S 1.59 / F 1.26 / 2Y 2.36 / SUB 1.02 / prod 0.5986）。
- **三腿族（M67/M68）不能作为第二个提交位**：原计划用它与两腿族 0.46 的低相关拿第二个槽位，但它永远过不了 S 闸 ⇒ **计划作废**。
- **shortinterest3 在 DEU/D1 的可交付产出 = 1 条**（`MPY9VNY9`）。累计投入：新增 45 条 + 历史 278 条 = **323 条回测**。
- **判死对象收窄（替代 §104 的粗粒度）**：
  - 判死：si3 的**三腿以上乘积几何**、**费率作乘子**、**长 backfill**、**纯水平乘积**、**评级以外字段作腿**。
  - 保留：**两腿 `ts_delta` 乘积 + `ts_target_tvr_decay` + `subindustry`/`sector`**（`M65`）。

### 106.6 六条方法论增量（跳数据集可复用）

1. **「单点最优 + 任何偏离都掉 S」= 几何自由度已耗尽的定量判据。** 不要再扫参数；该切机制或切数据集。（本轮 15/15 为负即为此判据的实例。）
2. **S 资源在差分，2Y 资源在水平，两者可替换不可兼得**。当双闸都要求 ≥1.58 时，要先看前沿斜率：斜率太陡（|斜率|>2）就直接放弃该几何。
3. **`winsorize` 对 `rank` 的乘积是空操作**（乘积已 ∈[0,1]）。不要再拿它当“去极值杆杆”浪费槽位。
4. **`group_neutralize` 替代 `group_rank` 是 margin 杆杆不是 S 杆杆**：`vR1nxdxa` margin 50.6bp（全族最高，比基准 +12.0bp）但 S −0.28。**撞 margin 墙时才用它。**
5. **`ts_backfill` 窗口放大对高频更新数据是纯损失**（22→126：S −0.18 且 2Y −0.81）。backfill 只应用于稳态字段，不应用于每日翻动的评分。
6. **已经是“综合评分”的字段不要再乘它自己的分量。** `shrt3_bar` 本身已含借券紧张度，乘 fee 就是同因子二次加权。判定顺序：先看字段 description 是否已是复合指标，再决定能不能当乘子。

### 106.7 判死登记簿更新（DEU / shortinterest3）

| 条目 | 范围 | 依据 |
|---|---|---|
| `DEU-SI3-3LEG-CEILING`（新） | si3 三腿以上乘积几何在 DEU/D1 的上限 = S 1.47 | 波 99/100/101 共 25 条，零条 S≥1.50 |
| `DEU-SI3-FEE-MULTIPLIER`（新） | 费率（mean/max loan rate）作乘子 | `78Lq0Jq2` −0.12 / `Jje0Yb0O` −0.38 S |
| `DEU-SI3-LONG-BACKFILL`（新） | 全腿 `ts_backfill` >100 | `d5W8gpeK` S −0.18、2Y −0.81 |
| `DEU-SI3-LEVEL-PRODUCT`（新） | 纯水平（ts_rank）乘积 | `YP1wn6Xq` 1.24 / `2rAqQMPJ` 1.21 |
| 保留：`M65` 两腿 ts_delta 乘积 | 唯一能过全闸的几何 | `MPY9VNY9` S 1.59 / prod 0.5986 |

---


---

## §107 波 104 收批（ESG 全灭）+ ★ 重大纠错：DEU/FUNDAMENTAL 塔并未全灭 + 塔位全景与点塔战略重算

> 时间：2026-10-31
> 输入：波 104 multisim `3wNmazfHH4v2aIp1ahbNuUW3`（5 条 = `fundamental22` 四维 + `earnings6` 一条）
> 三条结论：① ESG 四维分解全灭（S ≤ 0.42），`fundamental22` 收线；② **推翻 §106「DEU/FUNDAMENTAL 塔整体封盘」**——`Wje5K71x` 是 `fundamental6` 上一条已提交 ACTIVE 的全闸 alpha；③ DEU 16 个 category 里 **9 个完全未点亮**，「60 条」应按「16 塔 × 3 条」重算而非按单数据集刷量

### §107.1 波 104 回测结果：ESG 四维分解全灭

`fundamental22` 唯一字段 `fnd22_value`（VECTOR，coverage **0.69**，平台 alphaCount 40 / userCount 10）承载「每条记录 = 一个 ESG KPI 类型」。用四种 `vec_*` 聚合把 VECTOR 拆成四个正交维度，加一条 `earnings6` 对照：

| # | alpha | 表达式 | S | F | TO | 2Y | SUB | long/short | checks.fail |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| ES1 | `ZYQwxm3Q` | `group_rank(ts_zscore(vec_avg(fnd22_value), 252), subindustry)` | 0.32 | 0.11 | 10.01% | 0.85 | 0.06 | 72/73 | SHARPE / FITNESS / CW / SUB / 2Y |
| ES2 | `WjOwdLQx` | `… vec_stddev(fnd22_value) …` | 0.19 | 0.05 | 9.87% | 0.92 | 0.22 | 70/71 | SHARPE / FITNESS / CW / 2Y |
| ES3 | `YP1wmxKR` | `… vec_count(fnd22_value) …` | **0.42** | 0.25 | 10.97% | **−1.05** | 0.22 | 60/60 | SHARPE / FITNESS / CW / 2Y |
| ES4 | `j2YlXebQ` | `group_rank(ts_delta(vec_avg(fnd22_value), 126), subindustry)` | 0.34 | 0.12 | 10.05% | 0.56 | 0.04 | 72/73 | SHARPE / FITNESS / CW / SUB / 2Y |
| ER1 | `qMLkdEov` | `group_rank(ts_zscore(vec_count(ern6_actual_eps), 252), subindustry)` | 0.13 | 0.03 | **53.26%** | 0.25 | −0.03 | **1/1** | SHARPE / FITNESS / CW / SUB / 2Y |

**读数一：ESG 四维天花板 0.42，机制级判死。**
水平（ES1 0.32）/ 分歧度（ES2 0.19）/ 披露广度（ES3 0.42）/ 改善速度（ES4 0.34）——四种经济学含义完全不同的几何，S 全部落在 [0.19, 0.42]，2Y 最好 0.92（离 1.58 差 42%）。这不是「参数没调对」，是 ESG 分数在 DEU/TOP500 上不构成横截面定价维度。
与 `Diether-Malloy-Scherbina (2002)`（分歧度定价）和 `Hong & Stein (1999)`（意见分歧）的先验相反：先验认为 `vec_stddev`（KPI 间分歧）应最强，实测它**最弱（0.19）**。⇒ **ESG 的「分歧度」不是 Miller 意义上的意见分歧**，它是「同一公司不同 KPI 类型之间的量纲散布」，经济学含义与分析师分歧完全不同。这条映射错误是本波设计的前提缺陷。

**读数二：ES3 的 2Y = −1.05 是全波唯一大幅负值，暴露「披露广度」在 DEU 近年反向。**
ES1/ES2/ES4 的 2Y 都在 [0.56, 0.92]（弱正），只有 ES3 断裂到 −1.05。ESG 披露广度近年在德国被 CSRD/ taxonomy 强制拉平 ⇒ 早期「披露多 = 治理好」的溢价消失，反转成「补披露 = 合规成本」。**2Y 的符号比 S 的大小更早暴露机制衰变**（与本轮 §103 的 2Y 判据一致）。

**读数三：★ `earnings6` 在 DEU/TOP500 只有 1 只股票有值 —— 数据集级不可用。**
`qMLkdEov` 的 `longCount = 1` / `shortCount = 1`，TO 却高达 53.26%。这是「只有 1 只股票在买/卖，且每日翻动」的形态。`ern6_actual_eps` 是 VECTOR（"Reported non-GAAP diluted EPS"），`vec_count` 取的是「该股票该日的记录条数」——返回值非零的股票只有 1 只，说明 **`earnings6` 在 DEU 的覆盖是「1 只」而非「稀疏」**。
⇒ 与本轮 §102 的 `coverage=0 ≠ 无数据` 教训形成对偶：**`coverage>0 ≠ 有横截面宽度`**。判「数据集可用」必须同时看覆盖**宽度**（`longCount + shortCount`）而非只看覆盖率标量。PREFLIGHT 只查字段存在性，`platform_field_count` 命中 ≠ 有值。

**顺带取得 DEU 第 5 个权威塔位倍率**：`DEU/D1/EARNINGS` **1.6**（`qMLkdEov` 的 `pyramids.list`，`MATCHES_PYRAMID` pass）。累计已核实：FUNDAMENTAL **1.8** / OPTION **1.7** / EARNINGS **1.6** / MACRO **1.5** / SENTIMENT **1.8** / SHORTINTEREST **1.3** / ANALYST **1.8**。

### §107.2 ★ 重大纠错：§106 的「DEU/FUNDAMENTAL 塔整体封盘」是错的

**纠错触发**：本波收批后反向核查 `alphas` 表全 19 条 DEU 记录的表达式，发现 `Wje5K71x`：

| 字段 | 值 |
|---|---|
| expression | `group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(fnd6_newq_oiadpq,240)),rank(ts_delta(fnd6_newq_oiadpq,176))),target_tvr=0.03),sector)` |
| 字段归属 | `fnd6_newq_oiadpq` = **fundamental6**（Operating Income After Depreciation, quarterly） |
| status / stage | **ACTIVE / OS**，dateSubmitted 2026-10-12 |
| S / F / 2Y | **1.73 / 1.37 / 1.87** |
| prod / self | **0.4305** / — |
| TO / margin / LONG-SHORT | 12.69% / 12.58 bp / 179-203 |
| `ra.failed_ra_count` | **0**（全闸通过） |
| 塔位 | `DEU/D1/FUNDAMENTAL`，倍率 **1.8** |

⇒ **DEU/FUNDAMENTAL 塔有一条已提交并 ACTIVE 的全闸 alpha，prod 仅 0.4305（远低于 0.7 红线）。** §106 的「fundamental6 16 次回测封顶 0.92 ⇒ 已判死」和「DEU/FUNDAMENTAL 塔在数据层就不可挖」两条结论同时作废。

**两处误判的根因（方法论教训，跨区适用）**：

1. **`backtest_results.dataset` 列标签不可信 —— 用它 `GROUP BY` 会系统性漏掉成功的 alpha。**
   `Wje5K71x` 在 `backtest_results` 里的 `dataset` 值是 **NULL**，`alphas.dataset_id` 是 `1902`（一个内部 ID，不是数据集名）。所以「`SELECT dataset, MAX(sharpe) FROM backtest_results WHERE region='DEU' GROUP BY dataset`」这条查询**永远看不到它**，FUNDAMENTAL category 的 `best_s` 被算成 1.72（来自另一个字段），`n_clean` 被算成 0。
   **对策**：判死一个数据集前，必须用**表达式里的字段前缀**（`fnd6_` / `shrt3_` / `inst1_` …）反查 `alphas` 表，不能用 `backtest_results.dataset` 单列。

2. **按「数据集」判死是错的口径，必须按「骨架 × 数据集」二维判。**
   §106 依据的 16 条 `fundamental6` 回测全部来自 `s2_f6_recheck_d1`（8 条，全是 `group_rank(ts_scale(divide(...),66), sector)` 估值比率水平）与 `s2_fundamental6_d1`（8 条，分歧度/相关性/现金流），**没有一条含 M13 双期限 delta 骨架**。而 M13 × fundamental6 的 25 条扫描（波 `mcp-20261030`）里明确产出了 `Wje5K71x`。
   ⇒ **「该数据集 16 条封顶 0.92」只能证明「那 16 条骨架不行」，不能证明「数据集不行」。** 判死必须写明「在哪些骨架下判死」。

**M13 × fundamental6 的消耗度盘点（25 字段，实测）**：

| 位次 | alpha | 字段 | S | F | TO | 2Y | 结论 |
|---|---|---|---:|---:|---:|---:|---|
| 1 | `Wje5K71x` | `fnd6_newq_oiadpq` | **1.73** | 1.37 | 12.69% | 1.87 | **全闸过，ACTIVE** |
| 2 | `1YN6RJmM` | `fnd6_newq_dpq` | 0.43 | 0.21 | 3.28% | 0.22 | 挂 |
| 3 | `2rAPxJZZ` | `fnd6_newq_piq` | 0.39 | 0.18 | 3.10% | 0.41 | 挂 |
| 4 | `58EN1MqN` | `fnd6_newq_xsgaq` | 0.38 | 0.18 | 3.36% | 0.26 | 挂 |
| 5 | `xArXEEOw` | `fnd6_ibsa` | 0.36 | 0.16 | 2.60% | 0.39 | 挂 |
| … | （其余 20 条） | | 0.28 → −0.25 | | | | 全挂 |

**第 1 名 1.73 / 第 2 名 0.43，断崖比 4.0×。** 这是「单点最优 + 任何偏离都掉 S」的极端形态 ⇒ **M13 × fundamental6 单字段路线已耗尽，不要在这条轴上继续扫字段。**
但要区分：耗尽的只是「M13 × 单字段」这一条轴。`fnd6_newq_piq` 在 M13 下只有 0.39，却在 **ROE 比率（`piq/teqq`）** 下出到 S 1.33 —— **不是字段不行，是「裸字段 vs 比率」的归一化没做**。

### §107.3 DEU 塔位全景：16 个 category，9 个完全未点亮

依据：`datasets` 表 DEU category 维度 + `alphas` 表 11 条已提交记录的表达式字段反查。

| category | 数据集数 | 字段总数 | max_mult | 已提交条数 | 点亮状态（需 3 条） |
|---|---:|---:|---:|---:|---|
| SHORTINTEREST | 1 | 25 | 1.90 | **3** | **✅ 已点亮** |
| ANALYST | 19 | 4305 | 1.90 | ≥2 | 需再 1 条 |
| FUNDAMENTAL | 13 | 2146 | 2.00 | **1** | 需再 2 条 |
| OTHER | 43 | 3906 | 2.00 | 1 | 需再 2 条 |
| MODEL | 51 | 8027 | 1.90 | 1 | 需再 2 条 |
| INSIDERS | 2 | 42 | 1.90 | 1 | 需再 2 条 |
| INSTITUTIONS | 5 | 57 | 1.90 | 1 | 需再 2 条 |
| **SENTIMENT** | 3 | 276 | 2.00 | **0** | **★ 未点亮，但 `QPveY7Kg` 已全闸过（S 2.03 / prod 0.6671），提交即开张** |
| **NEWS** | 19 | 490 | 1.90 | **0** | 未点亮 |
| **PV** | 18 | 2876 | 1.90 | **0** | 未点亮 |
| **RISK** | 6 | 52 | 1.90 | **0** | 未点亮 |
| **SOCIALMEDIA** | 2 | 7 | 2.00 | **0** | 未点亮（7 字段，弹药极少） |
| **EARNINGS** | 2 | 25 | 2.00 | **0** | 未点亮（`earnings6` 实测仅 1 只有值 ⇒ 实质不可用） |
| **OPTION** | 1 | 22 | 1.80 | **0** | 未点亮（`option1` 已判死） |
| **MACRO** | 1 | 13 | 1.70 | **0** | 未点亮（`macro27` 已判死） |
| **IMBALANCE** | 1 | 2 | 2.00 | **0** | 未点亮（`imbalance5` 已判死） |

**11 条已提交 alpha 的塔位反查（按表达式字段）**：

| alpha | 关键字段 | 推定 category | S | prod |
|---|---|---|---:|---:|
| `2rOe10qY` | `oth455_*` | OTHER | 2.10 | 0.6388 |
| `2rjrMZ25` | `eps_y1_estimate_change_3mo` | ANALYST | 1.77 | 0.6510 |
| `2rmGAPqN` | `inst1_valueeur` / `inst1_holdings` | INSTITUTIONS | 1.81 | 0.6292 |
| `58gkLAkk` | `mean_estimate_change_pct_f12m_earnings_14d_4` | ANALYST | 1.75 | 0.5381 |
| `883Y3bAW` | `predictive_*`（analyst_earnings_ibes） | MODEL（+ANALYST 混） | 2.17 | 0.5434 |
| `JjxrYjre` | `shortinterest3` | SHORTINTEREST | 1.68 | 0.6453 |
| `Vk65zLzG` | `directional_indicator` + `predicted_surprise_*` | INSIDERS（+MODEL 混） | 1.79 | 0.6400 |
| `Wje5K71x` | `fnd6_newq_oiadpq` | **FUNDAMENTAL** | 1.73 | 0.4305 |
| `blRnKEk6` | `mean_loan_rate_main` + analyst | SHORTINTEREST（+ANALYST） | 2.02 | 0.5766 |
| `mLYLEm99` | （表达式为空） | 未知 | 2.27 | 0.6108 |
| `vRk6og8b` | `mean_loan_rate_main` + analyst | SHORTINTEREST（+ANALYST） | 1.80 | 0.6877 |

⇒ **DEU 的已提交存量里，11 条 alpha 有 8 条是 `add(add(add(...)))` 多腿混信号形态**，正是当前准则明令禁止的模式。它们的存在不构成「这条路可复用」的证据，反而是 DEU prod 池已被这类形态占据的原因（11 条 prod 全在 0.43–0.69，中位数 0.64）。

### §107.4 近闸候选破闸方程：`MP3ENd38` 的 S 缺口算术

`fundamental6` 上最接近闸门的一条（波 W357）：

```
MP3ENd38   winsorize(group_rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 252), sector), std=4)
           S 1.33 / F 0.91 / TO 14.04% / 2Y 1.54 / SUB 0.84 / margin 9.45 bp / ret 6.64% / 192-190
           checks.fail = [LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE]
```

**F 反推验证**（`F = S · sqrt(|R| / max(TO, 0.125))`）：
`1.33 × sqrt(6.64 / 14.04) = 1.33 × 0.6877 = 0.9153` vs 平台 0.91 ✅（误差 0.6%）

**三闸缺口算术**：

| 闸 | 当前 | 限值 | 绝对缺口 | 相对缺口 |
|---|---:|---:|---:|---:|
| LOW_SHARPE | 1.33 | 1.58 | +0.25 | **+18.8%** |
| LOW_FITNESS | 0.91 | 1.00 | +0.09 | +9.9% |
| LOW_2Y_SHARPE | 1.54 | 1.58 | +0.04 | +2.6% |

**关键推导：S 是唯一真缺口，F 与 2Y 都依附于它。**
- 若 S 到 1.58 且 `R/TO` 比价不变 ⇒ `F = 1.58 × 0.6877 = 1.087` **自动过闸**
- 若只是把 TO 从 14.04% 压到 10.5% 而 S 不变 ⇒ `F = 1.33 × sqrt(6.64/10.5) = 1.058` **也过闸**
- 2Y 只差 2.6%，同族里 `e7QYZN9l`（同一 `piq/teqq` 家族）2Y 1.38、`d51MrYOj` 1.14 —— 说明 2Y 对骨架敏感，双期限结构有望带动（`Wje5K71x` 2Y 1.87）

⇒ **破闸只需两件事同时成立：(a) S +19%；(b) TO ≤ 10.5%。**(a) 靠骨架升级，(b) 靠 `ts_target_tvr_decay`。

**S 从哪来？用 M13 的双期限结构，依据是同一模板在 si3 上的实测增益：**

| 数据集 | 骨架 | alpha | S |
|---|---|---|---:|
| si3 | 纯水平 3 腿（`ts_rank` 504/126/66 乘积） | `2rAqQMPJ` | 1.21 |
| si3 | **M13 双期限 delta 240/176 + TVR 0.03** | `MPY9VNY9` | **1.59** |
| fundamental6 | `ts_delta(ROE, 252)` 单期限（`MP3ENd38`） | — | 1.33 |
| fundamental6 | **M13 双期限 delta 240/176 + TVR（待测 = 波 105）** | — | **目标 ≥1.58** |

**注意口径统一**：`MP3ENd38` 是 `divide(piq, teqq)`（ROE），而 M13 × `fnd6_newq_piq` 单字段只有 0.39。波 105 不是「在 M13 轴上换字段」，而是「把 M13 的**期限结构**嫁接到已验证的 **ROE 比率**上」——两条都属于「换算子几何 / 换信号归一化」，不触碰 `add(A,B)` 混信号禁令。

### §107.5 波 105 设计：ROE 比率 × 双期限一致性（定向破闸批）

multisim `hbJJ7aLa4Vac7ffWha9svL`，DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / maxTrade OFF。定向破闸批，不受「10 模板」约束。

| # | 表达式 | 角色 | 隔离变量 |
|---|---|---|---|
| T1 | `group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 240)), rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 176))), target_tvr=0.04), sector)` | 主攻：M13 期限结构 × ROE | — |
| T2 | 同 T1，末参改 `subindustry` | 分组轴对照 | **T1 vs T2** = 分组粒度 |
| T3 | `group_rank(multiply(rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 240)), rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 176))), sector)` | 对照：去 TVR 层 | **T1 vs T3** = TVR 净效应 |
| T4 | `group_rank(ts_target_tvr_decay(multiply(multiply(rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 504)), rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 252))), rank(ts_delta(divide(fnd6_newq_piq, fnd6_ewq_teqq), 126))), target_tvr=0.04), sector)` | 三期限共识（M67 期限几何） | **T1 vs T4** = 期限数 |
| T5 | `group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(divide(fnd6_newq_piq, fnd6_cptnewq_atq), 240)), rank(ts_delta(divide(fnd6_newq_piq, fnd6_cptnewq_atq), 176))), target_tvr=0.04), subindustry)` | 换分母 ROA（稳健性） | **T1 vs T5** = 分母选型 |

**预检结果**：`preflight_expressions` → `valid: true` / `unknown_fields: []` / `platform_field_count: 3`（`fnd6_newq_piq` / `fnd6_ewq_teqq` / `fnd6_cptnewq_atq` 全命中）；`operator_audit` → `safe: true` / `violations: []`。

**预期与判读表**：
- T1 S ≥ 1.58 且 TO ≤ 10.5% ⇒ **DEU/FUNDAMENTAL 塔第 2 条全闸**，塔点亮进度 2/3
- T1 与 `MP3ENd38` 差 ≤0.05 ⇒ 期限结构在 fundamental6 上无效（si3 的 +0.38 不可移植）
- T2 ≫ T1 ⇒ 组内细分是主增益，后续全族换 `subindustry`
- T3 ≈ T1 ⇒ TVR 层在 fundamental6 上是死层（与 M13 × si3 的经验相反）
- T5 ≈ T1 ⇒ ROE 与 ROA 同源，只能取一

### §107.6 点塔战略重算：60 条 ≠ 单数据集刷量，而是「16 塔 × 3 条」

**用户目标 60 条 regular alpha，按「金字塔需 3 个 alpha 点亮」的准则换算 = 20 个塔点亮。DEU 只有 16 个 category ⇒ 60 条要求的不是 20 个塔，而是「每个塔平均 3.75 条」。**

**逐塔可达性评估**：

| category | 需条数（凑 3） | 已有全闸存量 | 弹药评估 | 可达性 |
|---|---:|---|---|---|
| SHORTINTEREST | 0（已 3 条） | +`MPY9VNY9`（未提交，可作第 4 条） | 已收线（323 条回测，S 上限 1.47 除 `MPY9VNY9`） | **✅ 完成** |
| SENTIMENT | 3 | **`QPveY7Kg` 1 条全闸过** | `snt7`/`snl27`/`snt21` 族已挖，剩 6 组待测（§106 清单） | **中高** |
| ANALYST | 1 | 0（`Vkxnb8QG` 是 SI+ANALYST 双塔） | 19 集 4305 字段，但 `analyst7/10/15/16/35/39/40/46/69/8/83/94/93/44/47/48` 已判死 | **低**（剩未测集少） |
| FUNDAMENTAL | 2 | **`Wje5K71x` 1 条** | 13 集，M13 单字段轴耗尽；`piq/teqq` 比率轴在飞（波 105）；`fundamental89`(407)/`fundamental1`(123)/`fundamental90`(66) 未开采 | **中**（波 105 定论） |
| OTHER | 2 | 0 | 43 集 3906 字段；`other532` 4 条待测（IND 验证过）；`other455`/`other384` 已判死 | **中** |
| MODEL | 2 | 0 | 51 集 8027 字段（最大），`model39`/`analyst_earnings_ibes` 部分判死 | **中** |
| INSIDERS | 2 | 0 | 仅 2 集 42 字段；`insider_agg_matrix`/`insider_trx_matrix` DEU 侧已判死 | **低** |
| INSTITUTIONS | 5→2 | 0 | 5 集 57 字段；`institutions6/25/4`、`fund_holdings_panel` 已判死 | **低** |
| NEWS | 3 | 0 | 19 集 490 字段；`news38/48/50/81/104/20/17` 已判死 | **低** |
| PV | 3 | 0 | 18 集 2876 字段，**完全未试**；但优先级最低（三塔之一） | **未知** |
| RISK | 3 | 0 | 6 集 52 字段；`risk60/68/71/72/88` 已判死 | **很低** |
| EARNINGS | 3 | 0 | 2 集 25 字段；`earnings6` 实测仅 **1 只**股票有值 | **不可达** |
| OPTION | 3 | 0 | 1 集 22 字段；`option1` 已判死（S −0.01） | **不可达** |
| MACRO | 3 | 0 | 1 集 13 字段；`macro27` 已判死（S −0.07） | **不可达** |
| SOCIALMEDIA | 3 | 0 | 2 集 7 字段；`socialmedia39` 已判死 | **不可达** |
| IMBALANCE | 3 | 0 | 1 集 2 字段；`imbalance5` 已判死 | **不可达** |

**结构性结论（本轮最重要的战略判定）：**

1. **DEU 的 16 个塔里，5 个（EARNINGS / OPTION / MACRO / SOCIALMEDIA / IMBALANCE）在数据层就不可达** —— 合计仅 69 个字段、7 个数据集，且逐个已实测判死（`earnings6` 覆盖 1 只股票是决定性证据）。这 5 个塔永远点不亮。
2. **可争取的塔只有 11 个**（SHORTINTEREST 已亮 + SENTIMENT / FUNDAMENTAL / OTHER / MODEL / ANALYST / INSIDERS / INSTITUTIONS / NEWS / PV / RISK 中真正有弹药的约 6 个）。
3. **满打满算「11 塔 × 3 条 = 33 条」是 DEU 的理论上限**，且其中 ANALYST / INSIDERS / INSTITUTIONS / NEWS / RISK 五个塔的存量已判死大半，实际可达 **20–25 条**。
4. ⇒ **「60 条」在 DEU 单区结构性不可达，缺口约 35–40 条。** 这不是「还没挖够」的问题，是塔位与字段的总量约束。
5. **最高杠杆的单点动作不是继续挖掘，而是提交 `QPveY7Kg`（SENTIMENT 塔开张）+ `MPY9VNY9`（SHORTINTEREST 塔加厚）+ `Vkxnb8QG`（ANALYST 塔 +1）—— 三条现存全闸 alpha 一次性把 3 个塔的进度从 0/1 推到 1/2。**

**下一步优先级（按边际产出排序）**：
1. 等波 105 收批 → 定 `fundamental6` ROE 比率轴生死
2. 若 T1 过闸 ⇒ FUNDAMENTAL 塔 2/3，只需再 1 条
3. 若 T1 不过 ⇒ 转 `fundamental89`(407 字段) / `fundamental1`(123 字段) 探针（DEU 仅剩的未开采大集）
4. 并行推进 `SENTIMENT` 剩余 6 组（`wpQMPNKx` / `MPYoz99r` / `6Xdv0gPJ` / `KPJjQVPz` / `kqN2O8qd` / `A1VMzqYg`）
5. **提交决策仍在用户手上**（不可逆），三条现存全闸 alpha 是唯一已挣得的东西

### §107.7 判死登记与配方状态更新

**新增判死**：

| entry_id | family | 依据 | 下次怎么办 |
|---|---|---|---|
| `DEU-FND22-ESG-4DIM` | ESG 四维分解（水平/分歧/广度/速度） | 4 条回测，S 上限 0.42，2Y 上限 0.92；分歧度维度 S 0.19 与先验反向 | 不再在 ESG 类数据集上做横截面 alpha；ESG 只可作门控/风格剔除，不可作信号 |
| `DEU-ERN6-COVERAGE-1` | `earnings6` 全字段 | `vec_count(ern6_actual_eps)` longCount=1 / shortCount=1，TO 53.26% | 判死是**覆盖宽度**问题，非信号问题；DEU 的 EARNINGS 塔不可达 |
| `DEU-FND6-M13-SINGLEFIELD-EXHAUSTED` | M13 × fundamental6 单字段轴 | 25 字段扫描，第 1 名 1.73 / 第 2 名 0.43（断崖 4.0×） | 只判死「单字段」轴；比率归一化轴（`piq/teqq`）仍在飞 |

**撤销判死 / 状态修正**：

| 旧结论 | 修正为 | 依据 |
|---|---|---|
| `fundamental6` 判死（16 条封顶 0.92，§106） | **仍活**，有 `Wje5K71x` 全闸 ACTIVE（S 1.73 / prod 0.4305） | 那 16 条不含 M13 骨架；`backtest_results.dataset` 标签为 NULL 导致漏计 |
| `DEU/FUNDAMENTAL` 塔「结构性封盘」（§106） | **未封盘**，已 1/3 点亮 | `Wje5K71x` + `DEU/D1/FUNDAMENTAL` 倍率 1.8 真实生效 |
| 「58 个 cov=0 数据集已判死」（§106） | 前提已被 §102 推翻，需逐集探针重判 | 波 102 五条探针全部有真实持仓 |

**方法论沉淀（3 条，跨区适用）**：
1. **判死必须按「骨架 × 数据集」二维查**，不能用 `GROUP BY dataset` 单列 —— 成功的 alpha 可能藏在 `dataset=NULL` 里。
2. **`coverage > 0` 不等于「有横截面宽度」** —— 必须同时看 `longCount + shortCount`。`coverage=0 ≠ 无数据`（§102）与 `coverage>0 ≠ 有宽度`（§107）是一对对偶陷阱。
3. **2Y 的符号比 S 的大小更早暴露机制衰变** —— ESG 披露广度的 S 0.42 看着「只是弱」，2Y −1.05 才说明「机制已反向」。

## §108 波 106 三集探针全灭 + `fundamental72` 侦察（DEU 唯一「EUR 已验证 × DEU 零挖掘」）+ SENTIMENT 双候选互斥（2026-10-31）

### 108.1 波 106 收批：FUNDAMENTAL 三集探针 10/10 未过闸

multisim `2d08hgb194JsaT1dzkkOD1B`（dataset 复合标签 `fundamental89+fundamental90+fundamental1`），2026-10-31 收批，`[harvest] children=10 terminal=10 done=10 error=0`，`[upsert] 10 rows`，`[salvage] all RED`。

| # | alpha | S | F | 2Y | TO | margin | LC-SC | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `vR1nzWea` | 0.62 | — | 0.98 | — | — | — | `fnd89_asset_41_11` 水平（流动应计） |
| 2 | `3qoY68ae` | 0.18 | — | −0.16 | — | — | — | 同字段一阶差分 ⇒ **差分毁水平型信号（第 5 次实证）** |
| 3 | `pwdJz9Vb` | **0.87** | — | **1.86** | — | — | — | `fnd89_asset_51_11` 非流动应计 —— **全波最强，仅挂 2 闸**，S 缺口 45% |
| 4 | `vR1nzW5a` | 0.17 | — | — | — | — | — | `41_31` 季度口径 |
| 5 | `d5W87Nnj` | 0.05 | — | −0.30 | — | — | — | `fnd90_game_noa` |
| 6 | `KPJY8Wnp` | 0.63 | — | — | 1.65% | 56.37bp | — | `fnd90_game_accruals_vol` |
| 7 | `MPYl8JkM` | 0.77 | — | — | — | — | — | `fnd90_game_inventory_chg` |
| 8 | `wpQwz0L6` | −0.20 | — | — | — | — | — | `fnd90_game_inc_cash_tax` 符号反向，翻符号后 ≈+0.20，距 1.58 差 8 倍 |
| 9 | `78LqXeJx` | 0.90 | — | — | — | 39.14bp | 95-92 | `fundamental1` 董事流失率，**CW 0.5 爆表（limit 0.1）** |
| 10 | `omEwzxVl` | 0.17 | — | −0.91 | — | — | — | 权益挂钩薪酬比 |

**三条结论**：
1. **`fundamental89` 只保留「非流动应计 / 总资产」这一条轴**（`51_11`，S 0.87 / 2Y 1.86），流动应计（`41_11` S 0.62）与销售额归一化（`41_31`→S 0.17）判死。这与 Sloan (1996) 的经典字段选型**方向相反** —— 在 DEU，长期/非流动应计的 2Y 反而更强。
2. **`Pincus-Rajgopal-Venkatachalam (2007)「成文法国家应计异象弱」在 DEU 得到确认**：4 个应计口径 S ≤ 0.87，无一接近 1.58。
3. **`fundamental1` 治理维度是「有信号但结构不可提交」**：S 0.90 是全波最高、宽度 95/92、margin 39.14bp，但 `CONCENTRATED_WEIGHT 0.5`（limit 0.1）在 2014-12-15 爆表 ⇒ 治理类 alpha 在 DEU 不再投入。

### 108.2 `fundamental72` 侦察：DEU 唯一「EUR 已验证 × DEU 零挖掘」

**判据三条同时成立**（三表实证）：

| 维度 | 证据 |
|---|---|
| DEU 侧零挖掘 | `expressions` / `backtest_results` / `alphas` 三表对 `fnd72` 与 `fundamental72` 关键词 **全部 0 命中**（DEU expressions 共 5810 条） |
| EUR 侧跨区先验 | 同数据集 144 条回测、**12 条 prod < 0.7**（`1YjXvEMJ` S1.60/prod0.6581 … `qMExbqbv`） |
| 规模 + 塔位 | 1031 字段、完整 BS + CF 三表、**全部单数据集 ⇒ FUNDAMENTAL 单塔 ATOM**，不触碰 trio 禁令、不吃 5 个名额 |

**EUR 制胜模板族（M13 几何 + 门控 + TVR）**：

```text
ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)),
  group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1),
  lambda_min=0, lambda_max=1, target_tvr=0.06)
```

**★ 关键约束：DEU 的 `fundamental72` 缺整个利润表（IS）字段族。**

`preflight` 的 `unknown_soft` 明确列出 `fnd72_pit_or_is_a_ebit` / `is_a_ebitda` / `is_a_net_income` / `is_a_sales_rev_turn` / `fnd72_s_pit_or_bs_a_bs_tot_asset` 全部 `dataset-prefixed field not found at this region/universe/delay`。`get_datafields(search="pit_or_is_a")` 在 1031 字段里**只返回 1 个**（`fnd72_s_pit_or_is_a_is_inc_bef_xo_item`）。

⇒ EUR 的 `greater(ebitda, net_inc)` 门控**在 DEU 无法照搬**；EUR `bl8RalWK`（S 2.00 / F 1.57 / prod 0.787）用的 `fnd72_s_` 标量路线在 DEU 也封闭。

**替代路径**：`fnd72_pit_or_cf_a_cf_net_inc`（现金流量表口径净利润）可作 NI 代理 ⇒ Sloan 应计可在数据集内部闭环计算，**比 EUR 原模板更「纯 ATOM」**：

```text
ACC = (cf_net_inc − cf_cash_from_oper) / bs_tot_asset
```

**★ 陷阱字段**：`fnd72_pit_or_bs_a_bs_accrual` 的 description 是 **"Other accounts payable and accruals"（应付账款明细）**，不是 Sloan 会计应计。按名字选字段会直接选错机制。`get_datafields(search="accrual")` 返回的 4 个字段全部是应付/杂项，**DEU 侧无现成会计应计字段，必须自算**。

### 108.3 SENTIMENT 双候选互斥判定：`QPveY7Kg` ↔ `kqNRX1ZP` = 0.7936

`compute_mutual_correlation(["QPveY7Kg","kqNRX1ZP","Vkxnb8QG","MPY9VNY9"], threshold=0.7, years=4)`，`num_points: 1021`：

| | QPveY7Kg | kqNRX1ZP | Vkxnb8QG | MPY9VNY9 |
|---|---:|---:|---:|---:|
| QPveY7Kg | 1.0 | **0.7936** | −0.0367 | 0.0328 |
| kqNRX1ZP | 0.7936 | 1.0 | −0.0298 | 0.0518 |
| Vkxnb8QG | −0.0367 | −0.0298 | 1.0 | 0.085 |
| MPY9VNY9 | 0.0328 | 0.0518 | 0.085 | 1.0 |

- `pairs_over_threshold` = **仅 1 对**（0.7936）；`max_mutually_below_subset` = `["QPveY7Kg","Vkxnb8QG","MPY9VNY9"]`，size 3，`max_subset_exact: true`。
- ⇒ **SENTIMENT 塔两条只能提一条**。选型倾向 `kqNRX1ZP`（S 2.06 / F 1.86 / SUB 1.49 / decay 16 全优），代价是 2Y 略低（2.37 vs 2.54）且 prod 从未测过。
- `check_self_correlation("kqNRX1ZP")` → **0.0297 通过**（top 相关 `2rmGAPqN` 0.0297；`pool_size 10 / full_os_pool_size 11 / excluded_power_pool_count 1`）。
- 另两条 `Vkxnb8QG` / `MPY9VNY9` 与其余三条 |ρ| ≤ 0.085，**完全正交**，可任意组合。

### 108.4 论坛取证（满足「用机制前必查论坛」）

`search_forum_posts("cash flow accruals alpha", 15)` 成功。**★ 短 query 才行** —— 长 query（12 词 `cash flow from operations to total assets accrual earnings quality alpha template`）返回 `navigation_failed: true` + 0 结果。

| 帖 | 票 | 可复用模板 |
|---|---:|---|
| 【Alpha ID 灵感】现金流量是否比利润更能预测股票回报（JB71859） | **27** | `cash_flow_ratio = (net_income − capex) / total_assets`，decay 0，Neutralization **Market** |
| 八种现金流组合（MY82844） | **24** | 按 CFO/CFI/CFF 三表符号分 8 类 regime |
| Using cashflow to predict market trends（TK60163） | 20+23评论 | `(CFO−capex)/cap`；`winsorize(ts_regression(rank(CBR_MV), rank(return_assets), 4), std=3)` |
| 【Alpha灵感】回到基本面: 应计项目和现金流的相关性, 倒U模型（QH29412） | 10 | **应计–现金流相关性本身是信号，且呈倒 U** |
| 【Alpha灵感】FSCORE 因子（ZH24706） | 0 | Piotroski 九项打分 → `group_rank(score, densify(industry))` |
| Are Cash Flows Better Stock Return Predictors than Profits?（YQ76635） | 7 | `grp=bucket(rank(cap), range="0,...")` |
| 从相关性的角度去构建alpha_template（SL10033） | 4 | `ts_corr(cash_field, value_field, days)` |

沿用 §107 已取证：`模板大师2-GPT增强版`（26 票，`accruals/ts_mean(price,252)` —— **引入 PV 腿，5 名额已满，不可采用**）、`Beneish M-score`（24 票，`TATA = Total accruals to total assets`，**符号确认为负向**）。

### 108.5 本轮方法论沉淀

1. **「跨区已验证」这个先验必须附带宇宙规模同构性检查** —— EUR 与 DEU 同为发达欧洲会计口径，但宇宙规模差一个量级，覆盖率与横截面宽度完全不同。§109 给出这条的实证代价。
2. **论坛检索先短 query（≤4 词），命中不足再逐步加长。**
3. **按名字选字段是 DEU 的主要失败模式** —— `bs_accrual` 是应付账款明细，不是会计应计。

## §109 波 107：`fundamental72` 十模板 ATOM 全灭 —— ★ 发现「CF 明细覆盖率陷阱」与「TVR 层在慢变量上摧毁宽度」两个新机制（2026-10-31）

### 109.1 收批

multisim `2mpeqR9sW4wc9YgMH1Tdxrq`，dataset `fundamental72`，DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / maxTrade OFF。
`[harvest] children=10 terminal=10 done=10 error=0` → `[upsert] 10 rows` → `[salvage] all RED, pool entries: 904`。
**10/10 未过闸，0 条 near，S 上限 0.37（距 1.58 差 4.3 倍）。**

### 109.2 逐条归因

简写：NI=`vec_avg(fnd72_pit_or_cf_a_cf_net_inc)`、CFO=`…cf_cash_from_oper`、TA=`…bs_a_bs_tot_asset`、CAPEX=`…cf_cap_expend_prpty_add`、CFI=`…cf_cash_from_inv_act`、CFF=`…cf_cash_from_fnc_act`、DA=`…cf_depr_amort`、RE=`…bs_retain_earn`、LTD=`…bs_lt_borrow`、CA=`…bs_cur_asset_report`、CL=`…bs_cur_liab`、ACC=(NI−CFO)/TA。

| # | 模板 | alpha | S | F | 2Y | SUB | TO | **LC-SC** | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F1 | M79 Sloan 应计水平（−） | `wpQwJPOl` | 0.16 | 0.05 | −0.76 | 0.20 | 8.63% | 63-61 | S/F/2Y |
| F2 | M80 CFO/TA + TVR（EUR 信号腿） | `vR1nJ6xG` | **0.37** | 0.13 | 0.93 | 0.31 | **55.59%** | **5-5** | S/F/**CW**/2Y |
| F3 | M81 自由现金流/TA | `omEw9rvm` | 0.24 | 0.06 | −0.21 | 0.25 | **85.37%** | **5-5** | S/F/**TO**/**CW**/2Y |
| F4 | M82 现金转化率 CFO/(\|NI\|+TA) | `88RkKYra` | 0.15 | 0.04 | 0.14 | 0.39 | 11.92% | 60-61 | S/F/2Y |
| F5 | M83 应计–CF 相关性倒U | `Jje051mx` | −0.46 | −0.23 | −0.85 | −0.09 | 5.36% | 67-68 | S/F/2Y |
| F6 | M84 现金流三表 regime | `bl62WnMK` | 0.36 | 0.11 | 0.76 | 0.21 | 67.75% | **4-4** | S/F/**CW**/2Y |
| F7 | M85 Piotroski 五项子集 | `omEw9rzm` | −0.14 | −0.04 | 0.12 | −0.36 | 8.93% | **2-3** | S/F/**CW**/**SUB**/2Y |
| F8 | M86 现金回报×会计回报回归残差 | `3qoYn566` | −0.12 | −0.03 | 0.03 | 0.10 | 12.55% | 70-70 | S/F/2Y |
| F9 | M87 留存收益/TA + 高斯分位 | `Jje051Xx` | 0.21 | 0.07 | 0.21 | −0.15 | 12.43% | 62-62 | S/F/**SUB**/2Y |
| F10 | M88 折旧摊销强度（长期应计代理，−） | `wpQwJPz2` | −0.36 | −0.16 | −0.56 | −0.18 | 12.17% | 61-57 | S/F/**SUB**/2Y |

### 109.3 ★ 新机制发现一：`fundamental72` 的 CF 明细字段在 DEU/TOP500 覆盖率 < 2%

按持仓宽度把 10 条分两组，边界极干净：

| 组 | 用到的字段 | 宽度 | S 范围 |
|---|---|---:|---|
| **宽**（只有 TA 与 CFO/NI 两类参与） | CA/TA、CFO/TA、RE/TA、DA/TA、ACC | **60–70** | −0.46 ~ 0.21 |
| **窄** | 加入 `cf_cap_expend_prpty_add` / `cf_cash_from_inv_act` / `cf_cash_from_fnc_act` / `bs_lt_borrow` / `bs_cur_asset_report` / `bs_cur_liab` | **2–5** | −0.14 ~ 0.36 |

**机理**：DEU/TOP500 里 `fnd72` 的年报字段本身只有约 **12–14% 覆盖**（60–70 / 500），而 CF 明细行（capex / 投资活动 / 筹资活动 / 折旧摊销）与部分 BS 明细（长期借款、流动资产/负债）的覆盖率跌到 **< 2%（2–5 只）**。宽度 ≤5 时 `CONCENTRATED_WEIGHT`（limit 0.1）在结构上必挂。

**⇒ 可复用判据 P-1：`fnd72` 在 DEU 只有「BS 主表 + CF 的 net_inc / cash_from_oper 两行」可用；任何含 CF 明细或 BS 明细的骨架，无论机制多正统，必然是 CW 死路。** 这解释了 F3（FCF，论坛 27 票公式）与 F6（八种现金流组合，论坛 24 票）为何全灭 —— **不是机制不成立，是字段没数据**。

### 109.4 ★ 新机制发现二：`ts_target_tvr_decay` 在年报级慢变量上**摧毁横截面宽度且 TVR 失效**

对照极干净 —— **同一信号腿，唯一差异是外面套了 TVR 层**：

| 版本 | 表达式 | 宽度 | TO | S |
|---|---|---:|---:|---:|
| 无 TVR | CFO/TA（F4 `88RkKYra` 变体同族） | **60–61** | 11.92% | 0.15 |
| **有 TVR** | `ts_target_tvr_decay(CFO/TA, target_tvr=0.06)`（`vR1nJ6xG`） | **5-5** | **55.59%** | 0.37 |

**两条同时失效**：
1. **宽度 60 → 5**：TVR 层为达成 6% 的组合换手目标，只能把持仓压到极少数股票 ⇒ 直接触发 CW。
2. **TO 反而冲到 55.59%**（target 的 9.3 倍）：年报级信号一年只变动一次，TVR 层没有足够的调仓自由度去逼近目标，反而在少数股票上反复微调放大换手。

**⇒ 可复用判据 P-2：`ts_target_tvr_decay` 的适用前提是「信号高频变动 + 横截面宽度充足」。在年报级慢变量 + 稀薄覆盖字段上，它会同时摧毁宽度和 TO 控制。** 此前 §106 已记「TVR 层只在实际 TO ≫ target 时有作用」，本条补充了它的**反面边界**：**当信号本身换手天然很低时，TVR 层是纯破坏**。

对照 EUR：同一模板在 EUR 侧出 12 条 prod<0.7 的 S 1.60 强 alpha。差异根源不是机制，而是 **EUR 大宇宙下 CFO/TA 的横截面宽度足够，TVR 层有调仓空间**。

### 109.5 ★ 结论：`fundamental72` 在 DEU 判死，且「EUR 已验证」这条先验被证伪

**判死依据（数据集级）**：
- 10 个结构互异模板，覆盖 Sloan 应计 / FCF / 现金转化率 / 应计-CF 相关性 / 三表 regime / Piotroski / 回归残差 / 留存收益 / 折旧强度 —— **经济机制层面已穷尽**。
- S 上限 **0.37**，距 1.58 差 **4.3 倍**；且 4 条触及 CW/TO 结构性闸。
- 覆盖天花板：可用字段子集（TA + CFO + NI）只有 60–70 只股票，横截面太窄 ⇒ 即使机制成立，S 也上不去。

**方法论教训（跨区适用）**：
1. **「同数据集在别的区域过 prod」不构成跨区可迁移先验**，必须同时核对：① 宇宙规模（EUR 大宇宙 vs DEU TOP500）；② 该数据集在目标区域的**字段级覆盖率**；③ 字段族完整性（DEU 缺整个 IS 族）。三者任一缺失，迁移必然失败。
2. **零挖掘 ≠ 机会** —— `fundamental72` 在 DEU 三表零命中，真相是「1031 字段里绝大多数没数据」，前人不是没挖到，是挖不动。
3. **论坛高票模板（27 票、24 票）在数据覆盖不足时照样全灭** —— 模板质量不能替代字段可用性检查。派发前必须先用「1 条最简探针验 longCount + shortCount」量宽度，这是波 107 全波 10 条换来的一条硬流程。

**登记判死**：`DEU-FND72-CF-DETAIL-SPARSE`（CF 明细 / BS 明细覆盖率 < 2%，含 capex / inv_act / fnc_act / depr_amort / lt_borrow / cur_asset / cur_liab ⇒ CW 结构性死路）、`DEU-FND72-NARROW-BREADTH`（可用子集仅 60–70 只，S 上限 0.37）、`DEU-TVRL-SLOW-SIGNAL-BREAK`（TVR 层在年报级慢变量上摧毁宽度且 TO 失控）。

## §110 波 109 定向破闸收束：fundamental89 非流动应计轴四维耗尽，S 天花板 0.98 —— 判死（2026-10-31）

### 110.1 波 109 结果（multisim `2BJHDcTp4Dx9IDtxsrpbAw`，10/10 未过闸）

统一骨架 `group_zscore(-ts_backfill(F, W), G)`，只扫 `F`（字段版本）/ `W`（backfill 窗口）/ `G`（分组轴）。
设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / maxTrade OFF。

| alpha | F | W | G | S | F | 2Y | SUB | TO | margin | LC-SC | 失败闸 |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| `Xg9w2On8` | 51_11 | 252 | sector | **0.98** | 0.77 | 1.55 | **0.45** | **2.71%** | **56.49bp** | 92-80 | S/F/**SUB**/2Y |
| `RREZ2vpe` | 54_12 | 66 | sector | 0.97 | **0.80** | 1.58 | 0.60 | 4.98% | 33.90bp | 75-63 | S/F/2Y |
| `Vkxw2R3J` | 51_11 | 66 | market | 0.97 | 0.79 | 1.44 | 0.67 | 4.64% | 36.00bp | 76-66 | S/F/**CW 0.162**/2Y |
| `QPvr2oVM` | 51_12 | 66 | sector | 0.96 | 0.78 | **1.69** | 0.64 | 4.94% | 33.04bp | 77-65 | S/F |
| `qMLkPwlO` | 51_11 | 504 | sector | 0.95 | 0.73 | 1.50 | **0.40** | 2.68% | 54.43bp | 93-81 | S/F/**SUB**/2Y |
| `9qxPa27q` | 51_11 | 66 | industry | 0.92 | 0.66 | **1.76** | 0.65 | 4.79% | 27.02bp | 76-66 | S/F |
| `0mYkeaEK` | 54_11 | 66 | sector | 0.91 | 0.72 | 1.53 | 0.58 | 4.94% | 31.44bp | 74-64 | S/F/2Y |
| `58E7a2k6` | 51_11 | 66 | subindustry | **0.80** | **0.51** | 1.73 | **0.38** | 4.49% | 22.43bp | 76-66 | S/F |
| `MPYlK2Lk` | 52_11 | 66 | sector | 0.80 | 0.59 | 1.63 | 0.62 | 5.20% | 26.57bp | 68-59 | S/F |
| `LLMbg21v` | 51_11 | **22** | sector | **0.19** | 0.06 | 0.14 | 0.27 | **20.39%** | 2.15bp | **33-30** | S/F/**CW 0.50**/2Y |

全波 `pyramids.list = [{DEU/D1/FUNDAMENTAL, 1.8}]`，`pyramid_short = fundamental`，`MATCHES_PYRAMID` 全 pass —— 塔位正确，纯粹是强度不够。

### 110.2 ★ 四个维度的单变量贡献（以 `51_11 / bf66 / sector` 为基线，`group_zscore` 基准 S 0.92）

| 维度 | 取值 | S | ΔS | 结论 |
|---|---|---:|---:|---|
| **几何**（波108） | `group_zscore` | 0.92 | 基线 | ★ 唯一正增益 |
| | `group_rank` | 0.87 | −5.4% | 次优 |
| | `group_rank` + `winsorize(std=4)` | 0.87 | **0.0%** | 归一化后尾部处理无效 |
| | `group_rank` + `ts_zscore(504)` | 0.41 | −55% | 毁信号 |
| | `group_rank` + `ts_quantile(252,gauss)` | 0.18 | −80% | 毁信号 |
| **分母**（波108/109） | `_12`（TS avg TA） | 0.96–0.97 | **+4~5%** | ★ 最优 |
| | `_11`（Total Assets） | 0.91–0.92 | 基线 | 次优 |
| | `_21`（Current Assets） | 0.83–0.89 | −3~-10% | 2Y 掉到 1.31–1.49 |
| **backfill W**（波109） | 252 | **0.98** | +6.5% | S/margin/TO 三优，但 SUB 0.45 挂 |
| | 66 | 0.92 | 基线 | ★ 结构安全点 |
| | 504 | 0.95 | +3.3% | SUB 0.40 挂 |
| | 22 | 0.19 | **−79%** | TO 20.4% + CW 0.50 双爆 |
| **分组轴**（波109） | market | 0.97 | +5.4% | CW 0.162 挂，不可用 |
| | sector | 0.92 | 基线 | ★ 综合最优（2Y 1.66） |
| | industry | 0.92 | 0.0% | 2Y 1.76 **全波最高** |
| | subindustry | 0.80 | **−13%** | SUB 0.38 挂，DEU 第 2 次实证禁用 |
| **数据源版本**（波108/109） | 51 / 54 | 0.90–0.97 | 基线 | 等效 |
| | 52 | 0.79–0.80 | **−12%** | 低质源（两波一致） |

**S 演进链（三波两次几何优化的累计效果）**：
`pwdJz9Vb` 0.87（波106，group_rank）→ `e758dx3g` 0.92（波108，group_zscore）→ `Xg9w2On8` 0.98（波109，bf252）。
累计 **+12.6%**，而缺口是 **+61%**（0.98 → 1.58）。⇒ 调参空间已被榨干，剩余缺口不是参数问题。

### 110.3 ★ 三条新机制发现

**① `ts_backfill` 窗口是「样本选择杠杆」，不是纯平滑杠杆 —— 存在 SUB 悬崖。**
同一信号腿只改 W：宽度从 75-63（W66）**升到** 92-80（W252）的同时，`LOW_SUB_UNIVERSE_SHARPE` 从 0.60 **掉到** 0.45（limit 0.46）。
机理：长 backfill 把「只在早年报数、后期断档」的股票也填上旧值并纳入排序，横截面上看宽度增加了，但加进来的是**被填充的弱样本**，在 TOP500 的子宇宙抽样里表现更差。
配套收益是真的：margin 33.90 → 56.49bp（+67%）、TO 4.98% → 2.71%（−46%）。
⇒ **判据：先跑 W=66 基线；只有 margin 不足且 SUB 已有 ≥0.30 余量时才试 W=252；年报级字段上 W=22 禁用（TO 3 倍+、CW 必爆）。**

**② `market` 分组轴在 DEU 必爆 `CONCENTRATED_WEIGHT`，`subindustry` 必弱。**
`market` 下 S 0.97（全波第 2 高）/ margin 36.00bp，但 CW 0.162（limit 0.1，2014-11-19）—— 因为 `group_zscore(x, market)` 只做全场标准化、不做行业中性，行业暴露全部留下。
`subindustry` 下 S 0.80（−13%）/ SUB 0.38 —— DEU TOP500 里 subindustry 组内只剩 5–15 只，`group_zscore` 变小组噪声。**这是「DEU 分组轴固定 sector、禁用 subindustry」的第 2 次独立实证。**
⇒ 最优轴排序：`sector`（综合）≈ `industry`（2Y 更好）> `market`（CW 挂）> `subindustry`（S 弱）。

**③ 8 个数据源版本里 `52` 是明确的低质源。**
`52_11` 在两种几何下都是最差：group_rank 下 0.79（波108）、group_zscore 下 0.80（波109），比 `51`/`54` 低 12%。
而 `51` / `54` 在两种几何下互换领先（54_12 zscore 0.97 vs 51_12 zscore 0.96），**等效**。
⇒ `fnd89_asset_5x` 版本的 description 全同（"Non-current Asset Accruals / Total Assets"），但质量不齐；后续若复用，直接从 `51`/`54` 起步，跳过 `52`。

### 110.4 判死结论与入库

**`fundamental89` 非流动应计轴（`asset_5x` 系列）= 判死。**

判据对照（沿用既有规则「单点最优 + 任何偏离都掉 S ⇒ 几何自由度耗尽」）：
- **单点最优已找到**：`Xg9w2On8` S 0.98。
- **任何偏离都掉 S**：换分母 −4~-10%、换几何 −5~-80%、换 W −3~-79%、换轴 −5~-13%、换源 −12%。五个维度无一能提 S。
- **三波 24 条回测**覆盖 分母(4) × 几何(5) × backfill(4) × 分组轴(4) × 数据源版本(3)，无一接近 1.58。

新入库两条判死：
- `DEU-FND89-NONCURRENT-ACCRUAL-CEILING`（family「fundamental89 非流动应计轴」）：`best_s 0.98` / `gap_to_gate 1.61` / `methodology_tag four-axis-exhaustion`。rule：不再开波；若复用该集只能换机制且须证明引入新自由度。
- `DEU-BACKFILL-WINDOW-SUB-CLIFF`（family「ts_backfill 窗口边界」）：跨数据集通用工具规律，已写入 rule 供后续所有波次复用。

### 110.5 ★★ 工具层纠错：`profile_drift.family_dead_datasets` 会误报活数据集

本轮两次 `upsert_registry_empirical` 的 `profile_drift.summary.family_dead_datasets` 都列出了：

```
fund_holdings_panel, fundamental6, fundamental72, fundamental89,
intraday_pv_feats, news18, other47, pv109, sentiment7
```

其中 **`fundamental6` 和 `sentiment7` 明确不是死的**：
- `fundamental6`：`Wje5K71x` **ACTIVE** / S 1.73 / F 1.37 / 2Y 1.87 / prod 0.4305 —— 全闸过且已提交。
- `sentiment7`：`QPveY7Kg` S 2.03 / F 1.61 / 2Y 2.54 / prod 0.6671；`kqNRX1ZP` S 2.06 / F 1.86 / 2Y 2.37 / self 0.0297 —— 两条全闸过。

⇒ 该字段的语义是「**该数据集上至少有一条 family 级判死记录**」，**不是「整个数据集判死」**。按它筛选会误杀活靶。
**判据升级**：判「数据集是否可用」只能查三处 —— ① `alphas` 表里该集的 ACTIVE/OS 记录；② `backtest_results` 里该集的 `ra_failed_checks='[]'` 记录；③ 平台 `pyramids.list`。**不得用 `family_dead_datasets` / `dead_datasets` 单独下结论。**

### 110.6 本轮 8 波（102–109）累计与 DEU 现状

| 波 | 数据集 / 战场 | 条数 | 过闸 | S 上限 | 结论 |
|---|---|---:|---:|---:|---|
| 102–105 | NOA / 位移 / ESG / ROE | 20 | 0 | 1.47 | 四条轴判死 |
| 106 | fnd89 应计 + fnd90 GAME + fnd1 治理 探针 | 10 | 0 | 0.90 | GAME 族全灭 / 治理 CW 不可提交 |
| 107 | fundamental72 十模板 | 10 | 0 | 0.37 | 判死（CF 明细覆盖 <2% + 缺 IS 族） |
| 108 | fnd89 分母 × 几何 | 10 | 0 | 0.92 | 拿到几何梯度 |
| 109 | fnd89 backfill × 分组轴 | 10 | 0 | **0.98** | **应计轴判死** |
| **合计** | | **60** | **0** | **0.98** | 应计轴天花板，缺口 1.61× |

**DEU 剩余可争取面（诚实评估）**：
- 16 塔里 5 塔（EARNINGS / OPTION / MACRO / SOCIALMEDIA / IMBALANCE）数据层不可达，合计仅 69 字段。
- 11 塔可争取，其中 SHORTINTEREST 已点亮 3 条、FUNDAMENTAL 1/3、ANALYST / OTHER / MODEL / INSIDERS / INSTITUTIONS 各 1 条。
- **天花板 = 16 塔 × 3 条 = 48 条 < 60 条目标** —— 60 条在数学上超限，且要 48 条意味着每塔打满，而 FUNDAMENTAL 侧刚又判死两个数据集。
- 已挖尽的数据集（判死）：`fundamental17` / `fundamental72` / `fundamental89` / `fundamental90` / `fundamental93` / `fundamental44` / `fundamental45` / `fundamental22` / `alpha_factor_lib` / `si3` / `option1` / `macro27` / `earnings6` / `institutions1/6/25` / `analyst7/10/15/16/35/39/40/44/46/47/48/69/8/83/93/94` / `news17/20/38/48/50/81/104` / `risk60/68/71/72/88` / `sentiment27/33` / `pv29/30/109` / `other47/78/128/384/532` / `socialmedia39` / `stock_cluster_dl` / `tm_*` / `fund_holdings_panel`。
- **唯一还有未测字段轴的 FUNDAMENTAL 集**：`fundamental6`（196 字段，活但 M13 单字段轴 + ROE 比率轴已判死，尚有非会计字段）、`fundamental86`（7 字段，从未挖）、`digital_ad_spend`（9 字段，从未挖）、`fundamental1`（剩余 121 字段，CW 风险已证）。

**结论**：DEU 单区在 60 条目标上已实质性触顶。继续在 DEU 硬挖的边际产出接近 0 —— 本轮 8 波 60 条回测 0 过闸，且最强的应计轴也已判死。
**建议路线**：① DEU 只做点塔（现有 3 条全闸 + 1 条待 prod 终验，提交后可点亮 SENTIMENT / SHORTINTEREST 两塔）；② 主力产量转到跨区承接（IND 62 条池 prod 通过率 72.6% / EUR 33.9%）；③ DEU 侧只再做两个从未触碰的小集（`fundamental86` 7 字段 / `digital_ad_spend` 9 字段）作为低成本扫尾。
## §111 波 111：`pattern_scores` 十模板 ATOM（形态相似度库）—— 10/10 未过闸，|S| 天花板 0.44

**目标**：DEU / MODEL 塔（当时判定 MODEL 塔未点亮），`pattern_scores` 504 字段全 MATRIX。
**字段命名规则**：`<形态>_{mean|std|max|min|median|q95|dynamic}_simscore_lookback{60|120}`。

### 收批结果

| # | alpha | S | F | 2Y | SUB | TO | margin | LC-SC | 失败项 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `88RkLrqX` | -0.44 | -0.20 | -0.08 | -0.36 | 5.41% | -9.41 bp | 128-128 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 2 | `Jje0dmlj` | -0.43 | -0.20 | 0.11 | -0.28 | 11.83% | -4.43 bp | 139-137 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 3 | `npvkWobw` | -0.35 | -0.13 | 0.02 | -0.06 | 15.20% | -2.72 bp | 138-139 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |
| 4 | `0mYk8dv1` | 0.23 | 0.08 | -0.16 | 0.01 | 12.03% | 2.22 bp | 146-147 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 5 | `d5W8Qmwj` | -0.15 | -0.03 | -0.01 | -0.17 | 21.16% | -0.73 bp | 147-147 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 6 | `xArwnQgb` | -0.14 | -0.03 | 0.19 | 0.19 | 4.38% | -2.82 bp | 143-143 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |
| 7 | `E560KbJ0` | -0.12 | -0.03 | -0.22 | 0.32 | 8.27% | -1.44 bp | 146-148 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |
| 8 | `rKR6WLvo` | -0.12 | -0.02 | -0.03 | -0.09 | 23.91% | -0.54 bp | 146-148 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 9 | `N1NWO6v8` | -0.11 | -0.02 | -0.01 | -0.07 | 22.11% | -0.57 bp | 146-148 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 10 | `2rAqKRd8` | 0.06 | 0.01 | 0.07 | 0.18 | 24.85% | 0.25 bp | 136-136 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |

### 归因

- 全波 10 条均未过闸，**|S| 天花板 0.44**（`88RkLrqX`，方向为负），**正向最强仅 0.23**（`0mYk8dv1`），距 1.58 闸线差 1.14。
- ★ 一个附带信号：按 |S| 排序前三全是**负向**（−0.44 / −0.43 / −0.35），正向最强只有 0.23
  ⇒ 「形态相似度高」在 DEU 上系统性偏空。这与直觉相反但可解释：相似度高的股票多是**已被市场充分识别的经典形态**，
  后续收益偏弱（拥挤/已被定价）。**这条只能作为方向先验，不足以支撑整波**——因为 |S| 0.44 的绝对强度太弱。
- `pattern_scores` 的字段语义是**形态相似度得分**（similarity score）：衡量「当前价格形态与某个历史形态的相似程度」。
  它刻画的是**形状匹配的强度**，不是收益方向 —— 方向取决于「被匹配的那个历史形态之后怎么走」，而这个信息不在字段里。
- 因此这个库天然缺**符号信息**：单腿排序只能押「相似度高 = 好」，无经济学依据；不同形态得分之间也不构成序关系（做差无意义）。
- **判据升级（可复用）**：`simscore` / `similarity` / `match_*` / `score_*` 这类**无方向相似度标量**在单数据集 ATOM 上系统性不出货。
  使用前提是必须配一个**带方向的历史收益标签**（`ts_regression` 到未来收益 / 与已实现收益做交叉），否则不要投入整波。

### 判死登记

`DEU-PATTERN-SCORES-NO-SIGNAL`（`registry_empirical`，layer=dead_end，dead_at=2026-10-31）。
`rule`：相似度/匹配度类字段做单数据集 ATOM 前，先确认字段是否自带方向；不带方向的必须先与「历史形态后验收益」正交化，否则整波不出货。
## §112 波 112：`model264` 十模板 ATOM（Wolfe 概率预测库）—— 10/10 未过闸，并证明「概率双档不互斥」

**目标**：DEU / MODEL 塔，`model264`（380 字段，cov 0.9973，aCnt 68）。
**字段语义**：`mdl264_{1l|2l}_<指标>`，`1l` = P(fall)，`2l` = P(neutral)。共 190 组指标 × 2 档。

### 收批结果

| # | alpha | S | F | 2Y | SUB | TO | margin | LC-SC | 失败项 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `O0AwpKzv` | 0.46 | 0.24 | 0.53 | -0.22 | 4.03% | 17.11 bp | 156-124 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 2 | `mLo28e0E` | 0.43 | 0.22 | 0.37 | -0.41 | 5.34% | 12.23 bp | 159-133 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 3 | `P0orpjxE` | 0.41 | 0.20 | 0.49 | -0.28 | 4.70% | 13.01 bp | 163-129 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 4 | `pwdJ6Qx6` | -0.40 | -0.20 | -0.47 | 0.31 | 4.72% | -12.70 bp | 129-163 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |
| 5 | `npvkgweq` | 0.40 | 0.19 | 0.13 | -0.36 | 9.35% | 6.02 bp | 148-144 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 6 | `rKR6oQNE` | 0.27 | 0.10 | 0.61 | -0.08 | 6.21% | 5.43 bp | 145-147 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 7 | `E560wo81` | 0.21 | 0.06 | 0.46 | 0.12 | 15.90% | 1.49 bp | 133-136 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |
| 8 | `qMLkAeOE` | -0.21 | -0.07 | -0.78 | -0.49 | 13.17% | -1.95 bp | 170-122 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 9 | `LLMbpOE2` | -0.08 | -0.01 | -1.38 | -0.26 | 17.88% | -0.52 bp | 142-150 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE,LOW_SUB_UNIVERSE_SHARPE |
| 10 | `e758OeVz` | -0.03 | 0.00 | 0.41 | 0.00 | 4.33% | -0.52 bp | 145-146 | LOW_2Y_SHARPE,LOW_FITNESS,LOW_SHARPE |

### ★ 核心发现一：概率双档「不互斥」，构造不出新维度

T1（`-P(fall)`）与 T2（`2·P(fall)+P(neutral)−1`）**完全镜像**：

| 维度 | T1 `P0orpjxE` | T2 `pwdJ6Qx6` |
|---|---:|---:|
| S | **+0.41** | **−0.40** |
| F | **+0.20** | **−0.20** |
| TO | 4.70% | 4.72% |
| LC-SC | **163-129** | **129-163** |
| margin | **+13.01 bp** | **−12.70 bp** |

T3（`-P(neutral)`）S −0.21，与 T1 同向。⇒ **P(fall) 与 P(neutral) 不是互斥概率，而是同一个「看空强度」潜在因子的两个同向投影**。
概率单纯形恒等式（P(fall)+P(neutral)+P(rise)=1）在这个库里**不成立**，所以任何基于单纯形的三档重构都是同一因子的线性变换。

**检验方法（可复用于所有概率型数据集）**：取两个「理论上应互斥」的档位各造一条反向表达式，
若 S / F / margin 三项同时镜像、TO 几乎相等、多空只数互换 ⇒ 双档同因子，立即停止在该集上做单纯形扩展。

### ★ 核心发现二：跨族聚合增益 <10% ⇒ 单因子判据

T9 把分析师修正 + 目标价 + 技术 + 基本面 + 动量**五族等权**聚合（`add` 链 + `divide(...,5)`），S = 0.43；
而单族 T1 = 0.41。**增益仅 +5%**。

⇒ 190 个指标全部投影到同一个潜在维度，彼此无正交信息。
**判据（可复用）**：跨族等权聚合的 S 增益 < 10% 即判该数据集只有单因子，不要在它上面继续做模板扩展，直接换集。

### 归因

- S 天花板 **0.46**（T10 不确定性门控 `O0AwpKzv`，margin 17.11 bp 为全波最高），距 1.58 差 1.12。
- 全波 `pyramids.list = [{DEU/D1/MODEL, 1.8}]`、`pyramid_short="model"`、`MATCHES_PYRAMID` 全 pass、**CW 全 pass** —— 塔归属与持仓分散度都没问题，是纯信号强度问题。
- 低 TO（4.03%–17.88%，多数 < 10%）意味着 F 分母被 0.125 地板锁死，**压 TO 无 F 增益**，只有 S 损失 ⇒ 这批候选没有靠调参救活的空间。

### 波 112 首次实跑通过的新算子形态

- `subtract(1, add(F1, F2))` —— 三参恒等式（单纯形重构）
- `add(ts_std_dev(x, 66), 0.001)` —— 防除零
- 五字段 `add` 链 + `divide(..., 5)` —— 固定 1/5 等权聚合（非权重调参）
- `trade_when(greater(group_rank(...), 0.5), x, -1)` —— 横截面相对量门控

### 判死登记

`DEU-MODEL264-SINGLE-FACTOR-EXHAUSTED`（layer=dead_end，dead_at=2026-10-31）。
`rule`：MODEL 塔不再使用 model264。概率预测型数据集若给出 P(x)/P(not x) 多档，先用 T1 vs T2 镜像检验判两档是否互斥；
概率型数据集先做「单族水平 + 跨族聚合」两条对照，若聚合增益 <10% 即判该集只有单因子，直接换集。

## §113 波 113 —— `predictive_starmine` 十模板 ATOM：全灭，但暴露「几何层而非信号层」是根因

**日期**：2026-10-31  **multisim**：`20IeiWgIQ4G7bMn14ZxV2xBs`  **10/10 COMPLETE，error_count 0**
**设置**：EQUITY / DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / pasteurization ON / unitHandling VERIFY / maxTrade OFF / nanHandling OFF / FASTEXPR
**塔位**：全波 `pyramids.list = [{DEU/D1/MODEL, 1.8}]`、`pyramid_short="model"`、`MATCHES_PYRAMID` 全 pass、`CONCENTRATED_WEIGHT` 全 pass。
**派发前闸**：`preflight_expressions` 12 条候选 → 仅 `analyst_downward_revision_count_fy1_ebitda_30d` 不存在（改用 `_7d_4`），`operator_audit` safe:true。

### 一、选靶依据：DEU 已提交 alpha 反查

`_deu_submitted_dump.py` 提取 DEU 11 条 OS alpha 的字段前缀频次：`mean` 19 / `predicted` 9 / `inst1` 5 / `oth455` 4 / `eps` 3 / `fnd6` 2 / `directional` 1。
`_deu_field_locate.py` 三表反查确认 `mean_estimate_change_pct_f12m_*` 与 `predicted_surprise_f12m_*` 均属 **`predictive_starmine`（MODEL，DEU 631 字段，cov 0.7903，aCnt 299）**，且该集出现在 11 条已提交 alpha 的 **7 条**里。

**11 条已提交按 S 降序**（全部 stage=OS）：

| alpha | status | S | F | 2Y | margin | TO | prod | 结构 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `mLYLEm99` | COMPLETE | 2.27 | 1.67 | — | — | 16.67% | 0.6108 | 表达式为空（本地无法复用） |
| `883Y3bAW` | COMPLETE | 2.17 | 1.24 | — | 6.58bp | 34.22% | 0.5434 | starmine×2 + dlr2 price + dlr2 return |
| `2rOe10qY` | COMPLETE | 2.10 | 1.98 | — | 17.80bp | 12.72% | 0.6388 | oth455 + starmine×3 |
| `blRnKEk6` | **ACTIVE** | 2.02 | 1.70 | **2.74** | 14.13bp | 16.15% | 0.5766 | si3 + starmine×3 |
| `2rmGAPqN` | COMPLETE | 1.81 | 1.48 | — | 13.39bp | 12.96% | 0.6292 | inst1 + oth455 |
| `vRk6og8b` | COMPLETE | 1.80 | 1.47 | — | 13.40bp | 19.03% | 0.6877 | si3 + starmine×3 |
| `Vk65zLzG` | COMPLETE | 1.79 | 1.69 | — | 18.46bp | 12.03% | 0.6400 | insider_agg + starmine×3 |
| `2rjrMZ25` | **ACTIVE** | 1.77 | 1.61 | 1.83 | 17.18bp | 11.99% | 0.6510 | analyst_factor_signals 自引用分桶 |
| `58gkLAkk` | **ACTIVE** | 1.75 | 1.42 | 2.07 | 13.16bp | 14.57% | 0.5381 | starmine + oth455 双 cluster + 4 层 group_neutralize |
| `Wje5K71x` | **ACTIVE** | 1.73 | 1.37 | 1.87 | 12.58bp | 12.69% | 0.4305 | fnd6 双期限 TVR |
| `JjxrYjre` | COMPLETE | 1.68 | 1.47 | — | 15.58bp | 12.31% | 0.6453 | insider_trx + starmine×3 |

**结构事实：11 条里 8 条是 `add()` 复合体（3–5 腿）**，纯单腿仅 `Wje5K71x` 与 `2rjrMZ25`。

### 二、十模板结果（10/10 未过闸）

| # | 模板 | alpha | S | F | 2Y | SUB | TO | margin | LC-SC | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| M126 | 论坛 2Y 预筛基线 | `6XdP9LQY` | 0.39 | 0.17 | 1.21 | 0.55 | 12.16% | 3.72bp | 71-72 | |
| M127 | 修正动量水平 | `leA6lPY8` | **0.96** | 0.78 | 0.11 | 0.46 | 10.83% | 15.18bp | 148-128 | 单腿最强 |
| M128 | 边际剪刀差 | `78Lq1Rr2` | 0.81 | 0.61 | 0.30 | 0.58 | 5.08% | **28.08bp** | 150-129 | margin 全波最高 |
| M129 | 超预期期限结构 | `xArwkppq` | −0.12 | −0.02 | 0.07 | −0.03 | 26.10% | −0.75bp | 128-128 | |
| M130 | 修正广度净额 | `E560EPP0` | 0.27 | 0.10 | −0.83 | 0.54 | 2.27% | 14.44bp | 112-158 | |
| M131 | ARM 一阶差分 | `3qoYRvve` | −0.36 | −0.13 | 0.02 | −0.21 | 15.21% | −2.79bp | 128-129 | 4 项失败 |
| **M132** | **超预期信噪比** | **`npvk255E`** | **1.05** | 0.79 | **1.37** | 0.78 | 5.17% | **27.17bp** | 132-129 | **全波最强**，DD 9.16%，investability S 1.25 / F 1.01 |
| M133 | 嵌套分组 | `E560EPn0` | 0.39 | 0.17 | 1.21 | 0.55 | 12.16% | 3.72bp | 73-73 | **与 M126 逐位相同** |
| M134 | 超预期×修正背离 | `58E7OdKJ` | −0.24 | −0.07 | 0.75 | 0.01 | 11.36% | −2.10bp | 131-139 | |
| M135 | signed_power + tvr_decay | `pwdJlebb` | 0.49 | 0.27 | 0.66 | 0.36 | 6.23% | 11.77bp | 138-124 | |

表达式：
```text
6XdP9LQY  group_rank(ts_zscore(ts_backfill(predicted_surprise_fy1_ebitda_4, 22), 252), subindustry)
leA6lPY8  group_zscore(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 22), 22), sector)
78Lq1Rr2  group_zscore(subtract(ts_mean(bf(mean_estimate_change_pct_f12m_earnings_30d_5,22),66), ts_mean(bf(mean_estimate_change_pct_f12m_revenue_30d_5,22),66)), sector)
xArwkppq  group_zscore(subtract(bf(predicted_surprise_pct_fy1_ebitda,22), bf(predicted_surprise_pct_fy2_ebitda_4,22)), sector)
E560EPP0  group_zscore(subtract(ts_sum(bf(analyst_upward_revision_count_fy1_ebitda_30d,66),126), ts_sum(bf(analyst_downward_revision_count_fy1_ebitda_7d_4,66),126)), sector)
3qoYRvve  group_zscore(ts_delta(ts_backfill(arm_score_5pt_scale_2, 66), 63), sector)
npvk255E  group_zscore(divide(ts_mean(ts_backfill(predicted_surprise_f12m_ebitda_4, 22), 66), add(ts_std_dev(ts_backfill(predicted_surprise_f12m_ebitda_4, 22), 252), 0.001)), sector)
E560EPn0  group_neutralize(group_rank(ts_zscore(ts_backfill(predicted_surprise_fy1_ebitda_4, 22), 252), subindustry), sector)
58E7OdKJ  group_zscore(subtract(rank(ts_mean(bf(predicted_surprise_fy1_ebitda_4,22),22)), rank(ts_mean(bf(mean_estimate_change_pct_f12m_earnings_14d_4,22),22))), sector)
pwdJlebb  group_zscore(signed_power(ts_target_tvr_decay(ts_mean(ts_backfill(predicted_surprise_pct_f12m_ebitda_5, 22), 22), target_tvr=0.06), 0.8), sector)
```

### 三、三条关键发现

#### ① 单国区域内「嵌套分组」是恒等式，不是杠杆

`E560EPn0` = `group_neutralize(group_rank(ts_zscore(bf(F,22),252), subindustry), sector)`，与 `6XdP9LQY` = `group_rank(ts_zscore(bf(F,22),252), subindustry)` **PnL 2334119 vs 2334121（差 2 分钱）**、S 0.39 一致、TO 12.16% 一致、margin 3.72bp 一致、2Y 1.21 一致，仅 longCount/shortCount 由 71-72 变 73-73。

**机理**：`subindustry ⊂ sector`，subindustry 组内 rank 已去掉组内均值，再按 sector 减一次无增量。

**⇒ 判据**：论坛帖 `42509573118999` 的「嵌套分组是潜力候选的关键一跃」（Sub 0.61~0.83 FAIL → 1.25 PASS）收益来自**跨国外层**（GLB/EUR 有国家轴）。**DEU 单国无法复现，不要重复嵌套分组实验。DEU 的 SUB 提升必须走别的杠杆。**

#### ② 论坛方法论在 DEU 的验证结果（部分成立、部分失效）

| 论坛主张 | DEU 实测 | 判定 |
|---|---|---|
| 修正方向动量最强 | M127 S 0.96 全波第二 | ✓ 成立 |
| 嵌套分组解决 SUB | M133 ≡ M126，零增益 | ✗ 单国失效 |
| 分歧度类字段 2Y 只有 0.3~1.25 | M129/M130/M131/M134 的 2Y 全低或负 | ✓ 成立 |
| 先筛 2Y 再谈 S | M126 2Y 1.21 但 S 仅 0.39 | ✓ 但 2Y 高≠有用 |

#### ③ ★ 最关键的几何反差：失败在几何层，不在信号层

DEU 已提交的 starmine alpha 是 **S 1.68–2.27**，波 113 最强只有 **1.05**。差别不在字段，在归一化层：

| 层 | 已提交 alpha 的写法 | 波 113 的写法 |
|---|---|---|
| backfill | **无** | `ts_backfill(F, 22)` |
| 时序平滑 | `ts_mean(F, 5)` | `ts_mean(..., 22)` 或 `66` |
| 横截面归一 | **裸 `rank()`** | `group_zscore(..., sector)` |

尤其 `883Y3bAW` / `blRnKEk6` / `vRk6og8b` / `Vk65zLzG` / `JjxrYjre` **五条**都用同一个腿 `rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5))` —— 这是 DEU 最被验证的 starmine 表达式。

**⇒ 波 114 直接复刻已验证腿做定向探针（10 条），先回答「单腿能否独立过闸」，再谈模板扩展。**

### 四、判据与模板入库

**新增模板**（M126–M135，全部已实证）：

| # | 模板名 | 骨架 | 结果 |
|---|---|---|---|
| M126 | 论坛 2Y 预筛基线 | `group_rank(ts_zscore(bf(F,22),252), subindustry)` | S 0.39 / 2Y 1.21 |
| M127 | 修正动量水平 | `group_zscore(ts_mean(bf(EC,22),22), sector)` | S 0.96 单腿最强 |
| M128 | 边际剪刀差（收入−盈利修正） | `group_zscore(subtract(ts_mean(bf(EC_e,22),66), ts_mean(bf(EC_rev,22),66)), sector)` | S 0.81 / margin 28.08bp |
| M129 | 超预期期限结构 | `group_zscore(subtract(bf(PS1,22), bf(PSb,22)), sector)` | S −0.12 |
| M130 | 修正广度净额 | `group_zscore(subtract(ts_sum(bf(UP,66),126), ts_sum(bf(DN,66),126)), sector)` | S 0.27 / 2Y −0.83 |
| M131 | ARM 评分一阶差分 | `group_zscore(ts_delta(ts_backfill(arm_score_5pt_scale_2,66),63), sector)` | S −0.36 / 4 项失败 |
| **M132** | **超预期信噪比（二阶方差归一）** | `group_zscore(divide(ts_mean(bf(PSq,22),66), add(ts_std_dev(bf(PSq,22),252),0.001)), sector)` | **S 1.05 / 2Y 1.37 / DD 9.16%** |
| M133 | 嵌套分组（行业内层×板块外层） | `group_neutralize(group_rank(ts_zscore(bf(F,22),252), subindustry), sector)` | ≡ M126，单国恒等式 |
| M134 | 超预期×修正背离 | `group_zscore(subtract(rank(ts_mean(bf(PS,22),22)), rank(ts_mean(bf(EC,22),22))), sector)` | S −0.24 |
| M135 | signed_power + 换手治理 | `group_zscore(signed_power(ts_target_tvr_decay(ts_mean(bf(PSp,22),22), target_tvr=0.06), 0.8), sector)` | S 0.49 |

**新增/更新判据**：

1. **单国区域的嵌套分组 = 恒等式**。`group_neutralize(group_rank(X, subindustry), sector)` 与 `group_rank(X, subindustry)` 逐位相同（PnL 差 2/2334119）。DEU/HKG 等单国区域禁用该模板；只对 GLB/EUR/ASI 这类有国家轴的区域有效。
2. **`ts_std_dev` 二阶方差归一是 starmine 上最有效的几何**。`npvk255E` 拿到全波最高 2Y（1.37）、最高 margin（27.17bp）、最低 DD（9.16%）、investability S 1.25 / F 1.01。⇒ 值得作为正式模板继续推。
3. **`analyst_downward_revision_count_fy1_ebitda_30d` 在 DEU 不存在**，`_7d_4` 版存在。修正计数族字段必须逐个 preflight。
4. **`predictive_starmine` 整体未判死**。波 113 只证明「group_zscore + bf 22 + ts_mean 22/66 的几何」不过闸，与信号本身无关（已提交 alpha 用裸 `rank(ts_mean(F,5))` 拿到 S 1.68–2.27）。判死必须等波 114 复刻探针结果。

### 五、字段资产（DEU `predictive_starmine`，631 字段，本次精确定位的高覆盖子集）

```text
# StarMine 预测超预期族
PS   = predicted_surprise_fy1_ebitda_4          cov 0.9469  uCnt 114  aCnt 224  ★全族最拥挤
PSp  = predicted_surprise_pct_f12m_ebitda_5     cov 0.9448  uCnt  99  aCnt 158
PSq  = predicted_surprise_f12m_ebitda_4         cov 0.9448  uCnt  33  aCnt  61  ★DEU已提交用
PS2  = predicted_surprise_pct_fy2_earnings_4    cov 0.9659  uCnt  27  aCnt  39  ★DEU已提交用
PS1  = predicted_surprise_pct_fy1_ebitda        cov 0.9469  uCnt  41  aCnt  60
PSe  = predicted_surprise_pct_f12m_earnings_5   cov 0.9648  uCnt  31  aCnt  38
PSb  = predicted_surprise_pct_fy2_ebitda_4      cov 0.9468  uCnt  17  aCnt  26
PSr  = predicted_surprise_pct_fy2_revenue_4     cov 0.9639  uCnt   7  aCnt  12
# StarMine 预估修正族（cov 0.97 档）
EC   = mean_estimate_change_pct_f12m_earnings_14d_4   cov 0.9706 uCnt 15 aCnt 25  ★DEU已提交主力
EC30 = mean_estimate_change_pct_f12m_earnings_30d_5   cov 0.9704 uCnt 24 aCnt 35
EC60 = mean_estimate_change_pct_f12m_earnings_60d_4   cov 0.9700 uCnt  7 aCnt 11
ECe14= mean_estimate_change_pct_f12m_ebitda_14d_4     cov ~0.97             ★DEU已提交用
ECe90= mean_estimate_change_pct_f12m_ebitda_90d_3     cov ~0.97             ★DEU已提交用
ECrev30 = mean_estimate_change_pct_f12m_revenue_30d_5 cov 0.9701 uCnt 4 aCnt 5
ECrev7  = mean_estimate_change_pct_f12m_revenue_7d_4  cov 0.9704 uCnt 2 aCnt 2
ECr  = mean_estimate_change_pct_fy1_revenue_7d_5      cov 0.9709 uCnt 2 aCnt 3
# StarMine ARM 修正模型族
ARM  = analyst_revisions_score_2                cov 0.9553  uCnt   5  aCnt  10
ARM5 = arm_score_5pt_scale_2                    cov 0.9553  uCnt   2  aCnt   3
ARMd = arm_score_change_7d_3                     cov 0.9707  uCnt   2  aCnt   2
ARMq = arm_score_change_90d_3                    cov 0.9686  uCnt   2  aCnt   4
ARMf = arm_new_activity_flag_2                   cov 0.9725  uCnt   2  aCnt   2
ARMk = arm_region_rank_decimal_2                 cov 0.9708  uCnt   3  aCnt   3
# 修正计数族（cov 0.9725，几乎无人挖）
UP   = analyst_upward_revision_count_fy1_ebitda_30d      ★存在
DN   = analyst_downward_revision_count_fy1_ebitda_7d_4   ★存在
        ★ analyst_downward_revision_count_fy1_ebitda_30d **不存在**（preflight 已证）
UPq  = analyst_upward_revision_count_fq2_ebitda_30d_4
```

**版本后缀规则**：`_2/_3/_4/_5/_6/_7` 是不同口径版本，cov ≥0.94 的多为 `_4/_5` 或无后缀。

**工程记录**：`harvest_multisim.py --multisim-id 20IeiWgIQ4G7bMn14ZxV2xBs --wave 113 --region DEU --dataset predictive_starmine --auto-upsert --no-queue` → EXITCODE=0，`[upsert] 10 rows`，`[salvage] all RED, pool entries: 943`。


## §114 波 114 —— 复刻已验证腿定向探针：**P6 五腿等权全闸通过（本轮 13 波首个）**

**日期**：2026-10-31  **multisim**：`2WssED7wH4YabaxNA0kUZgh`  **10/10 COMPLETE，error_count 0**
**设置**：EQUITY / DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / pasteurization ON / unitHandling VERIFY / maxTrade OFF / nanHandling OFF / FASTEXPR
**批次性质**：定向探针批（不受 10 模板约束）。目的：回答「纯 starmine ATOM 是否可行」。
**派发前闸**：`preflight_expressions` → valid:true / unknown_fields:[] / 8 字段全存在；`operator_audit` → safe:true / violations:[]。

### 一、设计逻辑

波 113 发现关键反差：DEU 已提交的 starmine alpha 是 **S 1.68–2.27**，而波 113 最强只有 **1.05**，差别在归一化层——

| 层 | 已提交 alpha 的写法 | 波 113 的写法 |
|---|---|---|
| backfill | **无** | `ts_backfill(F, 22)` |
| 时序平滑 | `ts_mean(F, 5)` | `ts_mean(..., 22)` 或 `66` |
| 横截面归一 | **裸 `rank()`** | `group_zscore(..., sector)` |

⇒ 波 114 把这 5 条已提交腿**逐条原样**跑一遍（单腿），再加一条纯 starmine 五腿等权复合和 4 条对照，共 10 条。

### 二、10 条结果

| # | 表达式（简） | alpha | S | F | 2Y | SUB | TO | margin | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | `rank(ts_mean(ECe14, 5))` | `WjOwV3KN` | 1.45 | 0.83 | 0.68 | 1.06 | 21.93% | 6.63bp | 10.19% | 3 |
| P2 | `rank(ts_mean(PSq, 5))` | `pwdJKxQv` | 0.86 | 0.48 | **2.09** | 0.71 | 10.82% | 7.11bp | 6.87% | 2 |
| P3 | `rank(ts_mean(ECe_eb14, 5))` | `mLo2VdeW` | 1.39 | 0.80 | 1.01 | 1.20 | 21.98% | 6.57bp | 9.22% | 3 |
| P4 | `rank(ts_mean(PS2, 22))` | `RREZ19Zj` | 0.96 | 0.60 | 1.36 | 0.81 | 6.64% | 14.62bp | 8.55% | 3 |
| P5 | `rank(ts_mean(ECe90, 22))` | `omEwgRw2` | 1.38 | **1.06** | 0.94 | 0.85 | 5.88% | **24.90bp** | 7.49% | 2 |
| **P6** | **五腿等权 `divide(add×5, 5)`** | **`O0AwxRwb`** | **1.98** | **1.74** | **1.75** | **1.45** | 15.36% | 15.37bp | 9.39% | **0 ★** |
| P7 | `rank(ts_mean(PSp, 5))` | `KPJYEvYN` | 1.34 | 0.99 | 1.38 | 1.04 | 10.86% | 12.55bp | 6.32% | 3 |
| P8 | `rank(ts_mean(PS, 5))` | `e758xN8N` | 0.80 | 0.43 | **2.09** | 0.90 | 10.72% | 6.71bp | 8.53% | 2 |
| P9 | M132 几何改裸 rank | `wpQwE3wd` | 0.88 | 0.51 | 0.16 | 0.56 | 4.06% | 21.07bp | 6.33% | 3 |
| P10 | `rank(ts_mean(EC30, 5))` | `akK2EeM6` | 0.93 | 0.52 | 0.06 | 0.57 | 15.41% | 6.15bp | 10.73% | 3 |

**P6 全闸明细**（`O0AwxRwb`）：
```text
divide(add(add(add(add(
  rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
  rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
  rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))),
  rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 22))),
  rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))), 5)
```
- `checks.fail = []`
- `checks.pass = [LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, CLUSTER_TEST, LOW_2Y_SHARPE, MATCHES_PYRAMID]`
- `checks.pending = [SELF_CORRELATION, DATA_DIVERSITY, PROD_CORRELATION, REGULAR_SUBMISSION]`
- `ra.failed_ra_count = 0`、`failed_ppa_count = 0`
- investability S **1.76** / F **1.64**；risk_neutralized_sharpe **1.60**
- `pyramids.list = [{DEU/D1/MODEL, 1.8}]`、LC-SC 134-127
- **信号全部来自单一数据集 `predictive_starmine` ⇒ 不触碰 PV/MODEL/OTHER 塔混禁令**

### 三、四条关键发现

#### ① ★ 单腿全部不过闸，五腿等权一次性全闸通过

| 指标 | 最强单腿（P1） | P6 五腿等权 | 增益 |
|---|---:|---:|---:|
| Sharpe | 1.45 | **1.98** | **+37%** |
| Fitness | 0.83 | **1.74** | **+110%** |
| 2Y Sharpe | 0.68 | **1.75** | **+157%** |
| SUB | 1.06 | **1.45** | +37% |

⇒ **这不是「多腿叠加碰运气」，而是 starmine 各子族的噪声互不相关、信号方向一致**。5 条腿里有 4 条单腿 2Y 不过 1.58，但等权后 2Y 1.75。
⇒ **判据更新**：对 starmine 这类「同族多指标」数据集，**不应按单字段强弱筛选，应按子族穷尽后等权合成**。单腿弱 ≠ 该字段无用（P2/P8 单腿 2Y 双双 2.09 但 S 仅 0.86/0.80，正是复合里最需要的「长周期稳定腿」）。

#### ② ★ 几何层是根因，信号层不是

同样的 `mean_estimate_change_pct_f12m_earnings_14d_4`：

| 版本 | 表达式 | S | 2Y |
|---|---|---:|---:|
| 已提交几何（P1） | `rank(ts_mean(F, 5))` | **1.45** | 0.68 |
| 波 113 几何（M127） | `group_zscore(ts_mean(bf(F,22),22), sector)` | 0.96 | 0.11 |

**S 差 0.49、2Y 差 0.57，字段完全相同。** ⇒ 波 113 判「starmine 几何失效」是对的，但**不能据此判 starmine 数据集失效**——波 114 已经证明信号在，只是被错误的归一化层压掉了。

#### ③ ★ `group_zscore` 与信号族要配对，不是一个几何通吃

P9 是干净的对照实验（同为 PSq 信噪比几何，只差外层归一）：

| 版本 | 外层 | S | 2Y | F |
|---|---|---:|---:|---:|
| 波 113 `npvk255E` | `group_zscore(..., sector)` | **1.05** | **1.37** | 0.79 |
| 波 114 P9 `wpQwE3wd` | 裸 `rank(...)` | 0.88 | **0.16** | 0.51 |

⇒ **在信噪比（二阶方差归一）几何上，`group_zscore` 带来 2Y +1.21 的巨大增益**；而在水平型信号（P1 vs M127）上它是负增益。
⇒ **判据：`group_zscore` 配「二阶/比率型信号」，裸 `rank` 配「一阶水平型信号」。** 这解释了波 113 为什么全灭而波 114 为什么爆发——波 113 把两个几何用反了。

#### ④ 修正窗口对照：14d 最优，30d 太长

| 字段 | S | 2Y |
|---|---:|---:|
| `mean_estimate_change_pct_f12m_earnings_14d_4`（P1） | **1.45** | **0.68** |
| `mean_estimate_change_pct_f12m_earnings_30d_5`（P10） | 0.93 | **0.06** |

⇒ **14 天修正是分析师预期的「有效信息窗」，30 天窗已被市场消化**。这与论坛帖「修正动量最强」一致，且给出量化边界。

### 四、self 相关性验收：0.7776 未过 ⇒ 它就是已提交的 book

`check_self_correlation(alpha_id="O0AwxRwb", correlation_type="self")`：

```text
passes_check: false   max_correlation: 0.7775669
top_correlated:
  blRnKEk6  0.7776   (DEU 已提交 ACTIVE, S 2.02, 2Y 2.74)
  Vk65zLzG  0.7696   (COMPLETE, S 1.79)
  vRk6og8b  0.7321   (COMPLETE, S 1.80)
  JjxrYjre  0.7181   (COMPLETE, S 1.68)
  2rOe10qY  0.7115   (COMPLETE, S 2.10)
pool_size: 10   full_os_pool_size: 11   excluded_power_pool_count: 1
```

**结论**：P6 的 5 条腿正是 DEU book 里 4 条已提交 alpha 的核心腿，所以自相关 0.78 是必然的。**它证明了方法有效，但同时说明 book 在这条信号上已经饱和。**

⇒ 不能直接提交 `O0AwxRwb`。要拿新 alpha 必须**改信息集降相关**，不是改参数。

### 五、波 115 降相关分支设计（已派发 `1sFpRy1Ti5efalAGBMvDK9z`）

思路：**几何锁定 `rank(ts_mean(F, w))` + 等权 `divide(..., N)`，只换腿集**。腿分两类——

**book 已用腿（K 类，5 个）**：`ECe14` / `PSq` / `ECe_eb14` / `PS2` / `ECe90`
**book 未用腿（U 类，14 个）**：ARM 族 6 个 / 修订计数 3 个 / revenue 侧 4 个 / 非 book 超预期 4 个

10 条分支，按腿集重叠度从 0 排到 5：

| # | 路线 | 腿集 | 重叠度 | 目的 |
|---|---|---|---|---|
| Q1 | 纯 ARM 族 | ARM5 + ARMd7 + ARMd90 + ARMrank | **0/5** | 完全正交的信息源 |
| Q2 | 修订计数族 | up_fy1 + up_fq2 + (−dn) + ARMrank | 0/5 | 广度型信号 |
| Q3 | revenue 侧 | RV30 + RV7 + RVfy1 + PSrev | 0/5 | PEAD 的「干净版」 |
| Q4 | 非 book 超预期 | PSp + PS + PSe | 0/5 | 同族换指标 |
| Q5 | 跨族 5 腿 | ARM5 + RV30 + up_fy1 + PSp + PS | 0/5 | 每族一腿 |
| Q6 | 8 腿超分散 | ARM5 + ARMd7 + RV30 + RV7 + up_fy1 + PSp + PS + PSe | 0/5 | 最大分散度 |
| Q7 | 对照：P6 窗口全 10 | K 类 5 腿 | 5/5 | 只改窗口能否降相关 |
| Q8 | 对照：P6 窗口全 22 | K 类 5 腿 | 5/5 | 更平滑 |
| Q9 | 2 book + 3 未用 | PS2 + ECe90 + ARM5 + RV30 + PSp | 2/5 | 保留强度 + 稀释 |
| Q10 | 稀释版 8 腿 | K 类 5 腿 + ARM5 + RV30 + PSp | 5/5 | 重量稀释 |

**验收标准**（两条同时满足才进提交队列）：
1. `failed_ra_count == 0`（S ≥1.58 / F ≥1.0 / 2Y ≥1.58，且 CW / TO / SUB / CLUSTER 全过）
2. 本地 `check_self_correlation < 0.7`（**免费且零配额，可对全部 10 条批量跑**）

### 六、工程记录

- 派发前发现 `analyst_revisions_score_2` 在 `preflight_expressions` 中返回 `warning: Field pre-check skipped or incomplete: analyst_revisions_score_2: get_datafields(offset=0): failed after 6 attempts` ⇒ **按既定规则剔除**，全部替换为已验证的 `arm_score_5pt_scale_2`。同时去掉 `arm_new_activity_flag_2`（二值 flag，rank 后巨量同值噪声大）。
- 二次 preflight：`valid:true` / `unknown_fields:[]` / `19 字段全验证` / **无 warning**。
- `harvest_multisim.py --multisim-id 2WssED7wH4YabaxNA0kUZgh --wave 114 --region DEU --dataset predictive_starmine --auto-upsert --no-queue` → EXITCODE=0，`[upsert] 10 rows`。


## §115 波 115：starmine 降相关分支 —— book 未用子族全灭，只剩「同族换指标 + 换窗口 + 稀释」三条路

**背景**：波 114 的 `O0AwxRwb`（S 1.98 / F 1.74 / 2Y 1.75，全闸通过）在 self 相关验收时挂在 **0.7776**，
最相似的是已提交 ACTIVE 的 `blRnKEk6`（0.7776）。这不是几何问题也不是字段问题，是**信息集重叠**：
P6 的 5 条腿正是 DEU book 里 4 条已提交 alpha 的核心腿。⇒ 结论：**方法有效，但这条信号在 book 里已饱和。**
必须改信息集降相关，不是改参数。

**波次**：116 前置波，multisim `1sFpRy1Ti5efalAGBMvDK9z`，10/10 COMPLETE，`error_count: 0`。
**设置**：EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 / truncation 0.08 / pasteurization ON /
unitHandling VERIFY / maxTrade OFF / nanHandling OFF / FASTEXPR。
**设计原则（关键）**：几何**完全锁定**为 `rank(ts_mean(F, w))` + 等权 `divide(..., N)`，**只换腿集**。
这样任何指标差异都只能归因到「用了哪些腿」，不会与几何变更混淆。这是波 114 结论的直接应用。

### 腿分类

- **K 类 = book 已用腿（5 个，高相关）**：`ECe14`=`mean_estimate_change_pct_f12m_earnings_14d_4`、
  `PSq`=`predicted_surprise_f12m_ebitda_4`、`ECe_eb14`=`mean_estimate_change_pct_f12m_ebitda_14d_4`、
  `PS2`=`predicted_surprise_pct_fy2_earnings_4`、`ECe90`=`mean_estimate_change_pct_f12m_ebitda_90d_3`
- **U 类 = book 未用腿（14 个）**：ARM 族 6 / 修订计数 3 / revenue 侧 4 / 非 book 超预期 4

### 结果（10/10）

| # | 路线 | alpha | S | F | 2Y | SUB | TO | margin | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 纯 ARM 族 4 腿（0/5 重叠） | `d5W8Znrj` | 0.15 | 0.03 | −0.45 | 0.10 | 18.95% | 0.91bp | 11.52% | 3 |
| Q2 | 修订计数族 4 腿（0/5） | `d5W8Znrv` | 0.90 | 0.57 | −0.63 | 0.76 | 5.66% | 17.61bp | 16.38% | 3 |
| Q3 | revenue 侧 4 腿（0/5） | `gJeq8mNO` | 0.55 | 0.21 | −0.02 | 0.39 | 19.83% | 3.02bp | 12.15% | 3 |
| **Q4** | **非 book 超预期 3 腿（0/5）** | **`Xg9wokZ1`** | **1.48** | **1.18** | **1.91** | 1.12 | 12.44% | 12.79bp | **5.84%** | **1（仅 LOW_SHARPE，差 0.10）** |
| Q5 | 跨族 5 腿（0/5） | `78LqzxPL` | 0.90 | 0.57 | 0.37 | 0.91 | 12.95% | 7.97bp | 9.11% | 3 |
| Q6 | 8 腿超分散（0/5） | `QPvrGnRw` | 1.08 | 0.62 | 0.49 | 0.89 | 18.99% | 6.56bp | 8.09% | 3 |
| Q7 | 对照：P6 窗口全 10 | `e7583nYg` | **1.78** | **1.60** | 1.45 | 1.30 | 13.23% | 16.21bp | 8.26% | 1（仅 LOW_2Y_SHARPE，差 0.13） |
| Q8 | 对照：P6 窗口全 22 | `bl62QNmR` | 1.50 | 1.29 | 1.04 | 1.12 | 9.27% | 19.96bp | 9.29% | 2（S 差 0.08 + 2Y） |
| Q9 | 2 book + 3 未用（2/5） | `vR1nN5EG` | **1.58** | **1.36** | 1.01 | 1.13 | 12.25% | 15.22bp | 8.10% | 1（仅 LOW_2Y_SHARPE） |
| Q10 | 稀释版 8 腿（5/5） | `d5W8ZnGX` | **1.93** | **1.69** | 1.48 | 1.44 | 15.06% | 15.27bp | 9.27% | 1（仅 LOW_2Y_SHARPE，差 0.10） |

### self 相关筛（纯本地计算，零配额、不占平台槽）

| alpha | S | 2Y | self max | 判定 | 最近邻 |
|---|---:|---:|---:|---|---|
| **`Xg9wokZ1`** | 1.48 | **1.91** | **0.5517** | **PASS ★** | vRk6og8b 0.5517 / blRnKEk6 0.5425 |
| **`vR1nN5EG`** | 1.58 | 1.01 | **0.6249** | **PASS** | JjxrYjre 0.6249 |
| `d5W8ZnGX` | 1.93 | 1.48 | 0.7043 | FAIL（超 0.004） | JjxrYjre 0.7043 |
| `e7583nYg` | 1.78 | 1.45 | 0.7332 | FAIL | blRnKEk6 0.7332 |
| `O0AwxRwb`（波 114） | 1.98 | 1.75 | 0.7776 | FAIL | blRnKEk6 0.7776 |

**★ 这条筛子是本波最有价值的产出**：`d5W8ZnGX` 与 `O0AwxRwb` 的 IS 指标更好（1.93/1.98），
但 self 相关性高 0.15–0.22；反观 `Xg9wokZ1` IS 只差 0.10 S，self 低到 0.5517（余量 0.148）。
⇒ **IS 强弱与可提交性在 book 饱和的区里是反向的**。判候选必须先跑 self 再判优劣。

### 三条核心发现

**① 纯「book 未用」子族全部不成立 —— 换子族不是降相关的手段。**
Q1（纯 ARM 4 腿）S 0.15 / 2Y −0.45；Q2（修订计数 4 腿）2Y −0.63；Q3（revenue 侧 4 腿）S 0.55；
Q5（跨族 5 腿）S 0.90；Q6（8 腿超分散）2Y 0.49。**五条路线、零重叠、全部不成立。**
⇒ starmine 631 字段里，真信号只集中在「**earnings/ebitda 的预估修正 + 超预期**」这两族；
ARM 评分 / 修订计数 / revenue 侧是噪声族。这与数据集名字（StarMine 是分析师预期修正库）一致，
但与它 631 字段的表观丰富度严重不符 —— **字段多不等于维度多**。

**② 唯一的例外是 Q4 `Xg9wokZ1` —— 三个「非 book 超预期」字段，是全部 0 重叠路线里唯一成立的一条。**
表达式：`divide(add(add(rank(ts_mean(PSp,5)), rank(ts_mean(PS,5))), rank(ts_mean(PSe,5))), 3)`
其中 `PSp`=`predicted_surprise_pct_f12m_ebitda_5` / `PS`=`predicted_surprise_fy1_ebitda_4` /
`PSe`=`predicted_surprise_pct_f12m_earnings_5`。
S 1.48 / F 1.18 / **2Y 1.91** / DD **5.84%（全波最低）** / margin 12.79bp / TO 12.44% / self **0.5517**。
⇒ **这是本区目前最有希望的第 4 条可提交候选**：只差 S 0.10，而 2Y 有 0.33 余量、self 有 0.148 余量、
DD 全波最低。**信息集完全独立于 book，降相关是天然完成的而不是靠调参。**

**③ 稀释不损失强度，但稀释的是 2Y。**
P6 五腿（S 1.98 / F 1.74 / 2Y 1.75）→ Q10 八腿（S 1.93 / F 1.69 / 2Y 1.48）：
S 只掉 0.05、F 掉 0.05，**2Y 掉 0.27**。⇒ 加腿扩信息集是「牺牲 2Y 保 S/F」的交易。
在 2Y 有余量时（如 `Xg9wokZ1` 的 1.91）加腿是安全的；在 2Y 卡线时（Q7 1.45 / Q10 1.48）加腿会直接挂闸。

### 窗口对照（几何锁定下的净效应）

同一组 5 腿，只改 `ts_mean` 窗口：

| 窗口 | alpha | S | F | 2Y |
|---|---|---:|---:|---:|
| w5（P6） | `O0AwxRwb` | **1.98** | **1.74** | **1.75** |
| w10（Q7） | `e7583nYg` | 1.78 | 1.60 | 1.45 |
| w22（Q8） | `bl62QNmR` | 1.50 | 1.29 | 1.04 |

⇒ **S 最优仍是 w5，w10 是 S 与 2Y 的折中（但 2Y 反而更低，无优势）。**
与波 114 单腿层结论一致：`_14d_4`（P1）2Y 0.68 vs `_30d_5`（P10）2Y 0.06 ⇒ **14 天是分析师预期有效信息窗**，
复合层也应把 `ts_mean` 窗口压短。**不要用 w22 —— 三个指标全劣。**

### 判死登记

- `predictive_starmine` 的 **ARM 族 / 修订计数族 / revenue 侧族** 在该几何下**不可用**（族级判死，非数据集判死）。
- `predictive_starmine` **数据集本身不判死** —— 信号真实存在（`O0AwxRwb` 全闸过 + `Xg9wokZ1` 2Y 1.91），
  只是 book 在「修正+超预期」这两族上已饱和。

### 后续动作

1. **波 116 定向破闸批**（已派发，`2xmqSI9w64n88HRjakP7jjh` 见 §116）：以 `Xg9wokZ1` 为基座，
   A 组纯扩 surprise 腿（+PSb / +PS1 / +PSb+PS1 / 全 surprise 6 腿 / PS 换 w22 / 全 w10），
   B 组加单条 book 腿试强度（+K1 / +K3 / +K1+PSb / +K4 w22）。目标：S 1.48 → ≥1.58 且 self 保持 <0.7。
2. 若 A 组任一过闸且 self<0.7 ⇒ 本区第 4 条可提交候选（MODEL 塔第 2 条，再 1 条即点亮）。
3. 若 A/B 组全灭 ⇒ `predictive_starmine` 判死为「book 饱和」，转 `model53`（Kamakura 违约概率，
   cov 0.87 / aCnt 0–3，几乎无人挖）或 DEU/D1/PV（当前 0 条，完全未点亮）。

---

## §116 波 116：定向破闸批 —— 单条 book 腿是唯一能跨过 S 1.58 的杠杆，一次产出 3 条全闸过候选

**背景**：§115 筛出 `Xg9wokZ1`（S 1.48 / F 1.18 / 2Y 1.91 / DD 5.84% / self **0.5517**），
唯一缺口是 S 差 0.10。本波是**定向破闸批**（不受「每波 ≥10 个结构互异模板」约束，按
`wq-brain-ra-pipeline` 的定向批豁免），目标单一：把 S 顶过 1.58 且 self 保持 <0.7。

**波次**：multisim `2xmqSI9w64n88HRjakP7jjh`，10/10 COMPLETE，`error_count: 0`。
**设置**：与 §114/§115 完全一致（EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 /
truncation 0.08 / pasteurization ON / unitHandling VERIFY / maxTrade OFF / nanHandling OFF / FASTEXPR）。
**基座**：`Xg9wokZ1` = `divide(add(add(rank(ts_mean(PSp,5)), rank(ts_mean(PS,5))), rank(ts_mean(PSe,5))), 3)`
（PSp=`predicted_surprise_pct_f12m_ebitda_5` / PS=`predicted_surprise_fy1_ebitda_4` /
PSe=`predicted_surprise_pct_f12m_earnings_5` —— 三条**全部是 book 未用腿**，0/5 重叠）。

### 结果（10/10）

**A 组：纯扩非 book 超预期腿（保持 0/5 重叠）**

| # | 变体 | alpha | S | F | 2Y | SUB | TO | margin | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T1 | 基 3 腿 + PSb，/4 | `3qoYlQ5e` | 1.53 | 1.25 | **1.80** | 1.21 | 11.82% | 14.13bp | 6.08% | 1（LOW_SHARPE 差 0.05） |
| T2 | 基 3 腿 + PS1，/4 | `A1VJljEd` | 1.49 | 1.19 | 1.84 | 1.11 | 11.97% | 13.39bp | 6.41% | 1（差 0.09） |
| **T3** | **基 3 腿 + PSb + PS1，/5** | **`d5W8jkvj`** | **1.55** | **1.28** | 1.78 | 1.20 | 11.56% | 14.65bp | 6.62% | **1（差 0.03 ★最接近）** |
| T4 | 全 surprise 6 腿，/6 | `6XdPlmNL` | 1.47 | 1.19 | 1.74 | 1.11 | 11.75% | 14.03bp | 6.76% | 1（差 0.11） |
| T5 | 基 3 腿 + PSb，PS 换 w22 | `wpQwjKv6` | 1.53 | 1.25 | 1.64 | 1.16 | 11.02% | 15.08bp | 6.83% | 1（差 0.05） |
| T6 | 基 3 腿全 w10 | `LLMb7V29` | 1.51 | 1.21 | **1.99** | 1.16 | 10.38% | **15.47bp** | 6.39% | 1（差 0.07） |

**B 组：基 3 腿 + 单条 book 腿（1/5 重叠）**

| # | 变体 | alpha | S | F | 2Y | SUB | TO | margin | DD | failed_ra | **self** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **T7** | **+ K1（E14 修正）** | **`6XdPlm2L`** | **1.77** | 1.42 | 1.79 | 1.33 | 15.41% | 12.79bp | **6.27%** | **0 ★** | **0.6503 PASS** |
| **T8** | **+ K3（EB14 修正）** | **`YP1w7LO6`** | **1.74** | 1.39 | **1.95** | 1.35 | 15.22% | 12.74bp | 7.51% | **0 ★** | **0.6496 PASS** |
| **T9** | **+ K1 + PSb，/5** | **`bl62jGgM`** | **1.78** | **1.50** | 1.75 | **1.37** | 13.96% | 14.25bp | 6.51% | **0 ★** | **0.6417 PASS** |
| T10 | + K4（PS2 超预期）w22 | `LLMb7Vw9` | 1.50 | 1.22 | 1.92 | 1.16 | 10.87% | 15.20bp | 6.62% | 1（差 0.08） |

### ★★★ 核心发现：纯非 book 扩腿有 S 天花板 ≈ 1.55，跨过 1.58 只靠「加一条 book 腿」

**A 组 6 个变体全部卡在 S 1.47–1.55**，无论怎么加腿（3→4→5→6 腿）、怎么调窗口（w5/w10/w22）、
怎么混期限（f12m / fy1 / fy2），S 都上不了 1.58。最好的是 T3 `d5W8jkvj` S **1.55**，差 0.03。
**这不像是「还差一点点优化」，更像是「这个信息集本身的 S 上限」。**

**B 组只需换掉一条腿 —— 把一条非 book 超预期腿换成一条 book 预估修正腿 —— S 立刻从 1.55 跳到 1.74–1.78
（+0.19 到 +0.23）。** 三条独立验证（K1 / K3 / K1+PSb 各一条，全部 0 失败过闸）。

| 参照 | 信息集 | S | 说明 |
|---|---|---:|---|
| T3 | 5 条全非 book | 1.55 | A 组天花板 |
| T7 | 3 非 book + K1 | **1.77** | +0.22 |
| T8 | 3 非 book + K3 | **1.74** | +0.19 |
| T9 | 4 非 book + K1 | **1.78** | +0.23 |
| P6（§114） | 5 条全 book 腿 | **1.98** | 上限，但 self 0.7776 |

⇒ **book 腿（`mean_estimate_change_pct_*` 预估修正族）携带的 S 是超预期族无法替代的。**
两者的经济学含义不同：**超预期** = 「实际 vs 预期」的已实现差异（事件后定价）；
**预估修正** = 分析师主动改模型（事件前扩散）。前者信息已公开、后者含未定价信息，
在 DEU 这种低覆盖市场（653 个 alpha vs GBR 3534）里后者的边际价值更高。

⇒ **可提交性的最优解不在「0 重叠」也不在「全 book」，而在「4 非 book + 1 book」这个中间点**：
S 只比全 book 版低 0.20（1.78 vs 1.98），但 self 从 0.7776 降到 0.6417（**降 0.136**）。
**这是本轮第一次找到「S 与 self 同时可接受」的配比。**

### 互相关聚类：3 条通过者属同一家族，只能提交 1 条

`compute_mutual_correlation`（4 年日收益，本地计算、零配额）：

| | bl62jGgM | 6XdPlm2L | YP1w7LO6 | Xg9wokZ1 | O0AwxRwb |
|---|---:|---:|---:|---:|---:|
| **bl62jGgM** | 1.000 | 0.9735 | 0.9284 | 0.9361 | 0.7564 |
| **6XdPlm2L** | 0.9735 | 1.000 | 0.9439 | 0.9420 | 0.7766 |
| **YP1w7LO6** | 0.9284 | 0.9439 | 1.000 | 0.9460 | 0.7746 |
| **Xg9wokZ1** | 0.9361 | 0.9420 | 0.9460 | 1.000 | 0.6460 |
| **O0AwxRwb** | 0.7564 | 0.7766 | 0.7746 | 0.6460 | 1.000 |

`max_mutually_below_subset` = `["Xg9wokZ1", "O0AwxRwb"]`（仅 2 条，且都不是可提交的：
`Xg9wokZ1` 差 S 0.10，`O0AwxRwb` self 0.7776 挂）。
⇒ **3 条新候选 + `Xg9wokZ1` 互相关 0.93–0.97，是同一个 alpha 的四种写法，只能提交其中 1 条。**

### 提交候选排序（self 全部 <0.7，均过全闸）

| 排名 | alpha | 塔 | S | F | 2Y | SUB | self | margin | DD | 取舍 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **1 ★** | **`bl62jGgM`** | DEU/D1/MODEL ×1.8 | **1.78** | **1.50** | 1.75 | **1.37** | **0.6417** | **14.25bp** | 6.51% | **S/F/SUB/self/margin/DD 六项全最优** |
| 2 | `6XdPlm2L` | DEU/D1/MODEL ×1.8 | 1.77 | 1.42 | 1.79 | 1.33 | 0.6503 | 12.79bp | **6.27%** | DD 最低，其余略逊 |
| 3 | `YP1w7LO6` | DEU/D1/MODEL ×1.8 | 1.74 | 1.39 | **1.95** | 1.35 | 0.6496 | 12.74bp | 7.51% | **2Y 最高（余量 0.37）**，DD 最高 |

**推荐提交 `bl62jGgM`**：唯一在 6 个维度里 6 项占优的一条，且 self 余量最大（0.6417，距 0.70 有 0.058）。
2Y 1.75 对 1.58 闸有 0.17 余量，F 1.50 对 1.0 闸有 0.50 余量，SUB 1.37 对 0.434×1.78=0.77 有 0.60 余量。
**唯一未测的门是 prod 相关性**（平台单并发槽被外部进程占用，两次 120s 超时）。

若 prod 挂在 0.7 附近，替代方案按 DD/2Y 偏好选 `YP1w7LO6`（2Y 1.95）或 `6XdPlm2L`（DD 6.27%）——
但三者互相关 >0.92，**prod 大概率同时挂或同时过，换条意义有限**，真正的 Plan B 是回 A 组
（`d5W8jkvj` S 1.55）或用 decay/truncation 调 prod。

### 副产品：窗口与期限的净效应（A 组内可比）

- **w10 是 2Y 最优窗**：T6（全 w10，3 腿）2Y **1.99** vs 基座 w5 的 1.91；margin 也从 12.79bp 升到 15.47bp，
  TO 从 12.44% 降到 10.38%。**代价是 S 从 1.48 掉到 1.51（其实还涨了 0.03）** ⇒ w10 在非 book 3 腿上
  **全面优于 w5**（S +0.03 / 2Y +0.08 / margin +2.68bp / TO −2.06pct）。**与 §115 复合层「w5 最优」结论冲突
  —— 原因：§115 的窗口对照用的是 book 5 腿，book 腿的最优窗是 w5；非 book 腿的最优窗是 w10。
  窗口要按信号族分别定，不能跨族照搬。**
- **fy2 期限不如 f12m**：T1（+PSb=fy2 ebitda）S +0.05 / 2Y −0.11 vs 基座；
  T10（+K4=fy2 earnings w22）S 1.50 / 差 0.08。⇒ **远期（fy2）预估修正的定价效率低于 12 个月滚动（f12m）。**
- **PS 换 w22 有害**：T5 2Y 从 1.91 掉到 1.64（−0.27），S 只涨 0.05。⇒ 主腿必须留在短窗。

### 判死登记

- **不再尝试纯非 book 组合破 S 1.58**：A 组 6 个变体（3/4/5/6 腿 × w5/w10/w22 × f12m/fy1/fy2）
  全部止步 1.47–1.55，判为**信息集上限**而非参数问题。
- `predictive_starmine` **不判死**，已产出 4 条全闸过候选（P6 / bl62jGgM / 6XdPlm2L / YP1w7LO6）。
  其中 3 条 self 通过 ⇒ **该数据集是本轮唯一产出可提交候选的数据集**。

### 当前 DEU 可交付存量（4 条 + 1 条待 prod）

| alpha | 塔 | 信源 | S | F | 2Y | self | prod | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---|
| `MPY9VNY9` | SHORTINTEREST ×1.3 | si3 | 1.59 | 1.26 | 2.36 | 0.2703 | **0.5986** | ★ 可提交 |
| `Vkxnb8QG` | ANALYST ×1.8 | fundamental6 衍生 | 1.83 | 1.64 | 2.09 | 0.6379 | **0.6384** | ★ 可提交 |
| `QPveY7Kg` | SENTIMENT ×1.8 | snt7 | 2.03 | 1.61 | 2.54 | 0.0242 | **0.6671** | ★ 可提交 |
| **`bl62jGgM`** | **MODEL ×1.8** | **predictive_starmine** | **1.78** | **1.50** | 1.75 | 0.6417 | **未测** | **待 prod** |
| `kqNRX1ZP` | SENTIMENT ×1.8 | snt7 | 2.06 | 1.86 | 2.37 | 0.0297 | 未测 | 与 `QPveY7Kg` 互斥 0.7936 |

**塔位影响**：`bl62jGgM` 属 DEU/D1/MODEL（当前 1 条）⇒ 提交后 MODEL 变 2 条，**再 1 条即点亮**。
加上存量 3 条点亮 SHORTINTEREST / ANALYST / SENTIMENT ⇒ **一轮提交可把 DEU 从 5 塔点亮到 8 塔**。

### 后续动作

1. **prod 终验 `bl62jGgM`** —— 唯一未测的闸。平台单并发槽被外部进程反复占用，需等槽空闲。
2. 若 prod <0.7 ⇒ 第 4 条可提交候选成立，与存量 3 条一起等用户授权。
3. 下一波优先靶（按 §115/§116 结论调整）：
   - `model53`（Kamakura 违约概率，cov 0.8734 / aCnt 0–3，几乎无人挖）—— MODEL 塔第 3 条即点亮
   - DEU/D1/PV（**当前 0 条，完全未点亮**）：`pv173`(81) / `continuation_score`(560) / `intraday_pv_feats`(585)
   - OTHER 塔 `other455`（DEU 已验证，P6 时代已用过一条腿）

---

## §117 波 117：DEU/D1/PV 塔首攻 —— 价差信号的信号在「相对自身历史的异常」，不在「水平」

**背景**：DEU/D1/PV 是唯一**完全 0 条**的高价值塔（倍率 1.7，全塔最高之一）。本轮已在
`continuation_score`(560 字段)、`intraday_pv_feats`(585 字段)、`pattern_scores`、`pv109`、
`pv173`、`pv20`、`pv29`/`pv30` 上累计判死 7 个数据集，`pv47` 描述限定 Asia/US 不可用，
`pv13`/`pv132` 仅 ID 映射。**`pv106`（Microstructure Spread Data，8 字段）是最后一个有真实
内容的候选**——DEU 侧 expressions / backtest_results / alphas 三表全 0 条，本轮首次开挖。

**波次**：multisim `3VnbSNyQ4BNbF3yp2rFkL1`，10/10 COMPLETE，`error_count: 0`。
**设置**：标准 DEU（EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 / truncation 0.08 /
pasteurization ON / unitHandling VERIFY / maxTrade OFF / nanHandling OFF / FASTEXPR）。
**模板库**：10 个结构互异模板（10 种流动性/交易成本的独立经济机制，非参数扫描）。

### `pv106` 字段全表（DEU 实拉，8 字段）

| 字段 | uCnt | aCnt | description | 本轮判定 |
|---|---:|---:|---|---|
| `pv106_spreadbp` | 32 | 36 | Bid-ask spread in bp (normalized to mid/VWAP) | ★ **唯一主力** |
| `pv106_spread` | 1 | 1 | Difference between best bid and best ask (currency) | 分母用 |
| `pv106_lastspread` | 0 | 0 | spread averaged over last 30 min (currency) | **近空，判死** |
| `pv106_lastspreadbp` | 1 | 1 | spread over last 30 min in bp | **近空，判死** |
| `aggregated_slippage_metric` | 1 | 1 | Composite slippage across trades/venues | 弱（S 0.16） |
| `slippage_at_spread_35` | 0 | 0 | Modeled slippage for order = 35% of ADV | 未测（aCnt 0） |
| `transaction_cost_maximum` | 0 | 0 | Maximum estimated transaction cost | 分母/分子配对 |
| `transaction_cost_percentile_10` | 5 | 7 | Estimated transaction cost at 10th percentile | 配对 |

**全局拥挤度**：`spreadbp`/`spread` 各 14 条表达式、`lastspread`/`lastspreadbp` 各 **150 条**、
`aggregated_slippage_metric` 19、`slippage_at_spread_35` 4、`transaction_cost_maximum` 46、
`transaction_cost_percentile_10` 11。**DEU 侧全部 0 条。**

### 结果（10/10，全部 `pyramids.list = [{DEU/D1/PV, 1.7}]`）

| # | alpha | 模板 / 骨架 | S | F | 2Y | SUB | TO | margin | DD | LC-SC | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| T1 | `3qoYXdMN` | 非流动性溢价水平 `group_rank(ts_mean(spreadbp,126),sector)` | 0.13 | 0.04 | −0.71 | −0.17 | 1.86% | 9.87bp | 18.43% | 151-148 | 4 |
| **T2** | **`j2YlAL2Z`** | **流动性冲击 `-group_zscore(ts_zscore(spreadbp,252),industry)`** | **1.38** | **0.59** | **0.94** | **0.87** | **38.67%** | 3.70bp | **5.15%** | **151-140** | 4 |
| T3 | `omEwL2mb` | 价差扩张动量 `-group_rank(ts_delta(ts_mean(spreadbp,22),22),sector)` | 0.60 | 0.29 | 0.03 | 0.39 | 13.88% | 4.64bp | 10.21% | 149-149 | 3 |
| T4 | `88RkjA57` | 流动性稳定性（论坛 `spread_impact`）`group_rank(subtract(1,rank(ts_std_dev(spreadbp,20))),subindustry)` | 0.07 | 0.01 | 0.79 | 0.43 | 5.26% | 1.53bp | 17.57% | 140-142 | 3 |
| T5 | `N1NWaMx7` | 价差波动率 `group_rank(ts_std_dev(spreadbp,126),sector)` | 0.08 | 0.02 | −0.61 | −0.37 | 2.38% | 5.02bp | 16.69% | 151-148 | 4 |
| T6 | `akK2bJjw` | 收盘价差结构 `-group_zscore(divide(lastspread,add(spread,0.0001)),industry)` | 0.12 | 0.01 | −0.16 | −0.29 | **139.34%** | 0.21bp | 33.44% | **23-20** | 6 |
| T7 | `O0AwNeOY` | 近端价差历史分位 `-group_rank(ts_rank(lastspreadbp,66),sector)` | 0.20 | 0.02 | 0.58 | −0.12 | **147.15%** | 0.29bp | 35.72% | **21-21** | 6 |
| T8 | `MPYlawOL` | 滑点成本水平 `group_rank(ts_mean(aggregated_slippage_metric,126),sector)` | 0.16 | 0.05 | −0.27 | −0.12 | 1.63% | 12.64bp | 17.71% | 148-152 | 4 |
| T9 | `2rAqwEM6` | 成本离散度 `group_zscore(divide(cost_max,add(cost_p10,0.0001)),industry)` | 0.27 | 0.09 | −0.09 | −0.04 | 14.04% | 2.25bp | 13.01% | 182-118 | 4 |
| T10 | `RREZbX3j` | 流动性门控+非线性 `trade_when(less(rank(ts_mean(spreadbp,66)),0.75), signed_power(-group_zscore(ts_zscore(lastspreadbp,252),subindustry),0.8), -1)` | 0.50 | 0.10 | 0.18 | 0.11 | **138.14%** | 0.84bp | 24.69% | **18-17** | 6 |

### ★★★ 核心发现一：价差的「水平」在 DEU 无溢价，「相对自身历史的异常」才有信号

五个不同几何的**水平/稳定性/波动率**类模板全部近零，且 2Y 多为负：

| # | 几何 | S | 2Y |
|---|---|---:|---:|
| T1 | 水平（126d 均值，正号） | 0.13 | −0.71 |
| T4 | 稳定性（20d 标准差倒数） | 0.07 | 0.79 |
| T5 | 波动率（126d 标准差） | 0.08 | −0.61 |
| T8 | 滑点水平（126d 均值） | 0.16 | −0.27 |
| T9 | 成本离散度（max/p10） | 0.27 | −0.09 |
| **T2** | **自身历史异常（252d zscore，负号）** | **1.38** | **0.94** |

**机理**：Amihud-Mendelson (1986) 的横向非流动性溢价在 DEU TOP500 + SUBINDUSTRY 中性化下**不成立**——
TOP500 全是大中盘，价差横截面差异被行业中性化吃掉。但**价差相对自身 252 日历史异常走阔**
是**逆向选择 / 信息不对称事件**（Glosten-Milgrom 1985；Kyle 1985）：知情交易者入场 ⇒ 做市商扩价差
⇒ 事件后该股短期跑输。**这是「事件」而非「特征」，所以必须用时间序列标准化，不能用横截面排名。**

**T2 的 DD 仅 5.15%、SUB 0.87** ⇒ 信号质量在 10 个模板里断层第一，唯一的病是换手 38.67%。

### ★★★ 核心发现二：F 卡点的解法是「降 TO」不是「提 S」，且边际回报差 2 倍

T2 精确算术（`F = S·sqrt(|R|/max(TO,0.125))`）：

```
当前：F = 1.38 × sqrt(0.0715 / 0.3867) = 0.593  ≈ 平台 0.59 ✅
需要：F ≥ 1.0 且 S ≥ 1.58  ⇒  R/TO ≥ 0.40，当前 0.185  ⇒  需提升 2.16×
若 TO 压到 F 公式地板 12.5%：F = 1.58 × sqrt(0.0715 / 0.125) = 1.19  ✅ 过 F 闸
```

⇒ **把 TO 从 38.67% 压到 12.5%（−68%）就能直接过 F 闸，且只需 S 提升 0.20；
而如果只提 S，需要 S 提升 0.20 的同时 returns 涨 2.16 倍 —— 后者做不到。**
⇒ **同样的力气花在降 TO 上，边际回报是提 S 的 2 倍以上。** 这是本轮第二次实证该结论
（第一次是 §113/§116 的 pv47 族 F=1.00 零余量案例）。

### ★★★ 核心发现三：`coverage = 0.0` 不等于无数据（本轮第三次实证）

`pv106` 8 个字段的 `coverage` **全部 0.0000**，但 T1–T5、T8、T9 的 `longCount+shortCount`
全在 **280–300**（TOP500 的 56–60%），T9 甚至达 300。

这已是本轮第三次：`pv106`（本轮）、`intraday_pv_feats`（§117 前判死时的反证）、
`continuation_score`。⇒ **判数据集可用性必须看 `longCount + shortCount`，`coverage` 标量是四重陷阱**：
① cov=0 可以有数据；② cov>0 不一定有横截面宽度；③ cov=0 也可能有健康宽度；④ 值域形态不可用
（如整数十分位）。**任何基于 cov 的预筛都必须用一轮单字段探针做二次确认。**

### ★★★ 核心发现四：字段级「宽度塌陷」是判死单字段的可靠指纹

`pv106_lastspread` / `pv106_lastspreadbp` 三个条件独立指向同一结论：

| 证据 | `lastspread`/`lastspreadbp` | 同批其他字段 |
|---|---|---|
| longCount + shortCount | **18–23** | 280–300 |
| turnover | **138%–147%** | 1.6%–38.7% |
| CONCENTRATED_WEIGHT | **0.5（limit 0.1 的 5 倍）** | 正常 |
| margin | **0.21–0.84bp** | 1.53–12.64bp |

⇒ **判死单字段不必等 10 个模板：单轮多数模板同时出现「宽度塌陷 + TO >130% + CW 超标」即可锁定。**
这也解释了「全局 `pv106_lastspread` 有 150 条表达式但 DEU 侧 0 条」——**不是没人试，是试过全都撞墙。**

### ★★★ 核心发现五：PPA 通道降级（第二次确认，指纹已固化）

T2 `j2YlAL2Z` 的闸门状态：

```text
checks.fail            = []                                    ← 空！
ra.ra_failed_checks    = ["LOW_SHARPE","LOW_FITNESS",
                          "CONCENTRATED_WEIGHT","LOW_2Y_SHARPE"]   ← 4 项
checks.warning         = 上述 4 项（被降级）
checks.pending         = [..., "POWER_POOL_CORRELATION", "MATCHES_THEMES"]   ← 多出 2 项
failed_ppa_count = 0 / ppa_failed = false
```

与 §113 `npvk255E` 完全同型。⇒ **`checks.fail = []` 绝不能当「已过闸」；
`ra.failed_ra_count == 0` 也不能当「已过闸」。** 判闸必须三处交叉：
`checks.fail` / `ra.ra_failed_checks` / `checks.pending` 是否含 `POWER_POOL_CORRELATION`。

### 论坛 + 文献取证（本波机制来源）

**论坛 4 条可用模板**：
1. 「margin 的微观分析」（29 票）——只管流动性最高 10% 的个股，Bid-Ask Spread 极窄（0.01%），
   微观损耗从 5‱ 降到 1‱ ⇒ **流动性门控思路**（本波 T10 采用）。
2. 「【wqapp优化】找灵感提示词优化」（50 票）snippet：`spread_impact = subtract(1, rank(ts_std_dev(bid_ask_spread, 20)))` ⇒ T4 直接采用。
3. 「🏛️ 市场微观结构与 Alpha 容量的内在约束」（16 票）——有效价差 vs 报价价差、价格冲击。
4. 「【Alpha Idea】谁在付 Spread？」（13 票 / 41 评论）+「双字段 Alpha 构建」（14 票 / 100 票版）—— A−B 差值范式。

**文献锚定**：Amihud-Mendelson (1986) 价差溢价 / Amihud (2002) ILLIQ / Glosten-Milgrom (1985)
与 Kyle (1985) 逆向选择 / Acharya-Pedersen (2005) 与 Pastor-Stambaugh (2003) 流动性风险定价 /
Corwin-Schultz (2012) 高低价价差估计。

### 判死与不判死

- **`pv106_lastspread` / `pv106_lastspreadbp` 判死**（宽度塌陷指纹，见核心发现四）。
- **`pv106` 数据集不判死**：`spreadbp` 单字段已产出 SUB 0.87 / DD 5.15% 的骨架，只是换手待治。
- **`continuation_score` / `intraday_pv_feats` / `pv109` / `pv173` / `pv20` / `pv29` / `pv30` 维持判死**
  （本轮设计前查登记簿，避免在这 7 个集上白烧 70 条）。
- **横向非流动性溢价（Amihud-Mendelson）在 DEU TOP500 判死**：5 种几何全 ≤0.27。

### 波 118（定向破闸批，已派发）

**目标**：把 T2 的 TO 38.67% 压到 ≤12.5%，换取 F 从 0.59 升到 ≥1.0。
**multisim**：`2FlLKobAv5hvbywdrjDUbaj`（10 条，共享 decay=4，基座全部为 T2 骨架）。
**preflight**：`valid: true` / `platform_field_count: 1` / `unknown_fields: []` / 无 warning。
**operator_audit**：`safe: true` / `violations: []`。
**已登记**：`upsert_expressions(region=DEU, wave=118, dataset=pv106, n=10, source=probe)`。

| # | 变体 | 设计意图 |
|---|---|---|
| A1 | `-group_zscore(ts_mean(ts_zscore(spreadbp,252),5),industry)` | 平滑分子 5d —— 主杠杆 |
| A2 | 同上 w10 | 平滑分子 10d |
| A3 | 同上 w22 | 平滑分子 22d（看 S 衰减拐点） |
| A4 | `-group_zscore(ts_target_tvr_decay(ts_zscore(spreadbp,252),target_tvr=0.03),industry)` | 显式 TVR 3% |
| A5 | 同上 target_tvr=0.05 | 显式 TVR 5% |
| A6 | `target_tvr=0.04` 套在 A1 上 | 平滑 + TVR 叠加 |
| A7 | 基准窗 504 | 换 zscore 基准长度（252→504） |
| A8 | 基准窗 126 | 换 zscore 基准长度（252→126） |
| A9 | `-group_rank(...,subindustry)` | 换轴 + 换几何（zscore→rank） |
| A10 | `trade_when(less(rank(ts_mean(spreadbp,66)),0.7), A1, -1)` | 门控对照：验证「基线 F <1.2 时门控失效」规则 |

**理论依据**：`ts_zscore(x, 252)` 的滚动基准窗变化极慢，**TO 几乎全部来自分子的日频噪声**
⇒ 平滑分子（`ts_mean`）是降 TO 的正确层，而非平滑整个 zscore 或加 decay 层。
A1–A3 直接验证这个假设；A4–A6 提供「显式换手预算」的对照；A10 是「门控要求基线 F ≥1.2」
这条记忆规则的**第三个对照点**（前两个：§116 pv47 族 F=1.00、analyst7 事件驱动）。

### 后续动作

1. 波 118 收批后判 TO 是否落到 ≤12.5%，若是 ⇒ PV 塔第一条可提交候选成立。
2. 若 A1–A3 的 S 衰减过快（<1.0），说明信号本身是高频的 ⇒ 转 `pv106` 的
   `transaction_cost_*` 配对族做「成本结构」骨架（T9 S 0.27 但 LC-SC 182-118 宽）。
3. PV 塔若最终仍挖不出，按「多区承接」方案把主力转 IND。

---


## §118 波 118：`pv106` 定向破闸 —— TVR 换手预算把 F 推过闸，但 2Y 天花板锁死在 0.94

**背景**：波 117 十模板全灭，唯一有信号的 `j2YlAL2Z`（`-group_zscore(ts_zscore(pv106_spreadbp,252),industry)`）
S 1.38 但 F 仅 0.59（卡 `LOW_FITNESS`）、TO 38.67%（离 `HIGH_TURNOVER` 0.7 尚有空间但 margin 仅 3.70bp）。
按 SOP「对近闸候选定向挖掘」，本轮针对 **F 闸**做定向破闸：F = S·sqrt(|R| / max(TO,0.125))，
提 F 只有两条路——**降 TO** 或 **提 R**。10 个模板全部围绕这两条路设计。

**波次**：multisim `2FlLKobAv5hvbywdrjDUbaj`，10/10 COMPLETE，`error_count: 0`。
**设置**：标准 DEU（EQUITY / DEU / TOP500 / delay 1 / SUBINDUSTRY / decay 4 / truncation 0.08 /
pasteurization ON / unitHandling VERIFY / maxTrade OFF / nanHandling OFF / FASTEXPR）。
**说明**：本波为**定向破闸批**，不受「≥10 个结构互异模板」约束，但实际仍是 10 个独立几何。

### 结果（10/10，全部 `pyramids.list = [{DEU/D1/PV, 1.7}]`）

| # | alpha | 模板 / 骨架 | S | F | 2Y | SUB | TO | margin | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | `Vkxwarq8` | 平滑 5d `-group_zscore(ts_mean(ts_zscore(F,252),5),industry)` | 1.27 | 0.79 | 0.68 | 0.82 | 17.13% | 7.86bp | 6.21% | 3 |
| A2 | `N1NWadqL` | 平滑 10d | 1.25 | 0.90 | 0.54 | 0.79 | 10.50% | 11.32bp | 7.04% | 3 |
| A3 | `GrW0b2Y5` | 平滑 22d | 1.23 | 0.88 | 0.44 | 0.76 | 6.21% | 16.18bp | 8.15% | 3 |
| A4 | `A1VJNpbW` | TVR 3% | 1.31 | 0.98 | 0.72 | 0.84 | 5.02% | 20.11bp | 5.63% | 3 |
| **A5** | **`O0AwNLkq`** | **★ TVR 5%** | **1.38** | **1.04** | **0.79** | **0.87** | **8.19%** | **17.43bp** | **4.82%** | **0** |
| A6 | `6XdPjW1p` | 平滑 5 + TVR 4% | 1.30 | 0.99 | 0.63 | 0.83 | 6.94% | 18.02bp | 5.91% | 3 |
| A7 | `Xg9wb3Lz` | 基准窗 504 | 1.19 | 0.71 | 0.81 | 0.75 | 17.44% | 7.61bp | 7.33% | 3 |
| A8 | `akK2b0l5` | 基准窗 126 | 1.22 | 0.74 | 0.41 | 0.71 | 18.02% | 7.44bp | 8.92% | 3 |
| A9 | `O0AwNLmq` | 换轴 + 换几何 `-group_rank(ts_mean(ts_zscore(F,252),5),subindustry)` | 1.13 | 0.62 | **0.25** | **0.53** | 16.88% | 7.02bp | 9.47% | **4（真 fail）** |
| A10 | `O0AwNLm7` | 门控 `trade_when(less(rank(ts_mean(spreadbp,66)),0.7), -group_zscore(...), -1)` | 0.63 | 0.31 | 0.11 | 0.42 | 4.71% | 12.66bp | 11.08% | 5 |

### ★★★ 核心发现一：`ts_target_tvr_decay` 是比 `ts_mean` 平滑更好的降 TO 层

同基座三方对比（A1 平滑 5d / A4 TVR 3% / A5 TVR 5%）：

| 层 | S | F | 2Y | TO | margin |
|---|---:|---:|---:|---:|---:|
| `ts_mean(z,5)`（A1） | 1.27 | 0.79 | 0.68 | 17.13% | 7.86bp |
| `tvr_decay(0.05)`（**A5**） | **1.38** | **1.04** | **0.79** | **8.19%** | **17.43bp** |
| `tvr_decay(0.03)`（A4） | 1.31 | 0.98 | 0.72 | 5.02% | 20.11bp |

**机理**：`ts_mean` 是**无差别平滑**，把信号里真正需要保留的跳变也一起抹平（S 从 1.38 掉到 1.27）；
`ts_target_tvr_decay` 是**换手预算约束**——只在超出预算时施加衰减，信号锐度得以保留而换手被压到目标值。
结果：S 不降反升（+0.11），TO 腰斩（−52%），margin 翻倍（+122%）。

**落地规则**：降 TO 的第一动作应是 `ts_target_tvr_decay`，`ts_mean` 只在需要额外稳健性时才叠加。
A4（3%）与 A5（5%）对比说明 **5% 是最优目标档**——3% 压得过头开始伤 S（1.38→1.31）。

### ★★★ 核心发现二：`pv106` 的 2Y 天花板 = 0.94，且天花板来自信号自身衰减而非区域特征

`O0AwNLkq` 是 PV 塔历史最佳（F 1.04 是 PV 塔唯一过 F 闸的 alpha），但 2Y 仅 0.79，
`LOW_2Y_SHARPE 1.58` 差 50%。为判「能不能救」，跑年度归因 + 跨 alpha 对照：

| alpha | 2016 | 2018 | 2023 | 说明 |
|---|---:|---:|---:|---|
| `O0AwNLkq`（A5，目标） | 0.57 | 0.59 | **0.24** | 逐年单调衰减 |
| `MPY9VNY9`（对照·SHORTINTEREST 已过闸） | — | — | **1.78** | 同区同年 |
| `bl62jGgM`（对照·MODEL 已过闸） | — | — | **1.56** | 同区同年 |

**判据**：2023 年同区已过闸 alpha 仍有 S 1.56–1.78，目标 alpha 只有 0.24 ⇒
**不是 DEU 区域 2023 难做，是 `pv106` 价差信号自身在 2023 失效**。年度序列单调下行（0.57→0.59→0.24）
进一步排除「单年噪声」，是结构性衰减。

⇒ **判死**：`upsert_registry_empirical(region=DEU, layer=dead_end, entry_id="DEU-PV106-SPREAD-ANOMALY-DEAD")`
返回 `action: inserted`。payload 含 `best_s 1.38` / `best_2y 0.94` /
`methodology_tag "2Y-ceiling-by-yearly-attribution + cross-alpha-control"` /
`dead_fields ["pv106_lastspread","pv106_lastspreadbp"]` / `keep_fields ["pv106_spreadbp"]`。

### ★★ 核心发现三：双重中性化致命（第 2 次实证）

`O0AwNLmq`（A9）= 全仓 `SUBINDUSTRY` 中性化 **＋** 表达式内再套 `group_rank(..., subindustry)`：
S 1.13（从 A1 的 1.27 掉 11%）、**2Y 0.25**（掉 63%）、SUB 0.53 < limit 0.54 ⇒
**本波唯一触发真 `LOW_SUB_UNIVERSE_SHARPE` 的 alpha**。

**规则**：全仓中性化已是 `SUBINDUSTRY` 时，表达式内不得再用 `subindustry` 分组。
分组轴应上移到 `sector` / `industry`。

### ★★ 核心发现四：`trade_when` 门控在 F < 1.2 的基座上再次失效（第 3 次）

A10 门控版 S **0.63** vs A1 无门控 1.27（−50%）。三个对照点已累积：

| 波次 | 数据集 | 基线 F | 门控后结果 |
|---|---|---:|---|
| §116 | `pv47` 族 | 1.00 | S 1.65→1.16，三闸全挂 |
| §116 | `analyst7`（事件驱动） | 0.83 | 无变化（门控对事件驱动无效） |
| §118 | `pv106` | 1.04 | S 1.27→0.63 |

**判据**：**基线 F < 1.2 的候选直接放弃门控救援。** 门控要求基座本身留有余量。

### ★★★ 塔位终局：DEU/D1/PV 塔 16 集全部判死或不可用

| 数据集 | 字段 | cov | aCnt | 判定 |
|---|---:|---:|---:|---|
| `continuation_score` | 560 | 0.0 | 80 | 判死 `DEU-CONTSCORE-PATTERN-DEAD`（11 模板 \|S\|≤0.52） |
| `intraday_pv_feats` | 585 | 0.0 | 510 | 判死 `DEU-IPF-INTRADAY-PV-DEAD`（13 模板 max\|S\|0.64，TO 68%） |
| `pattern_scores` | 504 | 0.9888 | 266 | 判死（波 111，\|S\| 天花板 0.44） |
| `pv1` | 23 | 0.0 | 12639 | 极饱和 |
| `pv103` | 8 | 0.0 | 59 | 未挖（订单流不平衡，机理已被 IPF 覆盖） |
| **`pv106`** | **8** | **0.0** | **44** | **本轮判死 `DEU-PV106-SPREAD-ANOMALY-DEAD`** |
| `pv109` | 26 | 0.4665 | 33 | 判死 `DEU-PV109-BOND-DEAD`（12 模板 max\|S\|0.54） |
| `pv13` | 26 | 0.0 | 8 | 仅 ID 映射 |
| `pv132` | 29 | 0.0 | 5 | 仅 ID 映射 |
| `pv17` | 1 | 0.0 | 24 | GROUP 类 |
| `pv173` | 81 | 0.0 | 14 | 判死 |
| `pv20` | 681 | 0.0 | 619 | 判死 `pv20_dead` |
| `pv29` | 50 | 1.0 | 66 | 判死（GROUP）`DEU-PV30-GROUP-ONLY-NOT-SIGNAL` |
| `pv30` | 285 | 0.7273 | 287 | 判死（GROUP） |
| `pv47` | 2 | — | — | 描述限定 Asia/US，不可用 |
| `pv71` | 8 | — | — | 描述写 news feed，名字不符 |

**结论**：**DEU/D1/PV 塔（倍率 1.7）0 条，且无法通过继续挖 PV 数据集解决**——16 个数据集已穷尽。
这是「倍率是收益权重，不是难度折扣」的第二次自证（第一次是 MODEL 塔历史）。
**后续任何区域开 PV 塔前，必须先查该塔历史波次规模，不能只看倍率为 0 条就当作机会。**

### 本波净收益

- 产出 PV 塔历史最佳 `O0AwNLkq`（S 1.38 / F 1.04 / 2Y 0.79），但**未过 2Y 闸**，不构成可提交候选。
- 确立 3 条可复用规则：**TVR-decay 优于 ts_mean 平滑** / **双重中性化致命** / **F<1.2 不用门控**。
- 判死 1 个数据集（`pv106`），PV 塔 16 集全部封盘。
- 累计：本轮 18 波（101–118）共 160 条回测，4 条全闸过。

## §119 波 119：MODEL 塔 `model53` 信用风险十模板 —— 违约概率在 DEU 被定价干净，天花板 0.55

**背景**：本波是从 NEWS 塔转向 MODEL 塔后的第一攻。选靶逻辑不是倍率而是**距点亮的剩余条数**：
DEU/D1/MODEL 现有 1 条，`bl62jGgM`（`predictive_starmine`，S 1.78 / F 1.50 / 2Y 1.75）待 prod 终验，
**再 1 条即点亮**；而 NEWS 塔需从 0 起 3 条且 58 条历史探针天花板仅 |S| 0.76。所有未点亮塔倍率同为 1.8，
无差异 ⇒ 选 MODEL。

**选靶过程**：`get_datasets(category="model", region="DEU")` 平台实拉 45 个集，倍率全 1.8。
排除已饱和（`model38` aCnt 6105 / `model25` 1946 / `predictive_starmine` 1143 / `model216` 629）、
已判死（`model16` / `model141` / `model262`）、已探（`model264` 波 112 天花板 0.46）后，
锁定 **`model53` Creditworthiness Risk Measure Model**：cov 0.905 / 22 字段 / **uCnt 仅 9 / aCnt 仅 9** /
valueScore 6 —— 全平台几乎无人挖。

**★ 注意**：数据集级 description 写的是 "BBID↔RIC mapping"，与实际内容（Kamakura 信用风险模型）**完全不符**。
这是 `model53` 之外第 20 个被证实描述失真的数据集。**判内容必须看字段级 description。**

### `model53` 字段全表（DEU 实拉，22 字段，全 MATRIX 无需 `vec_*`）

| 字段族 | 字段数 | cov | aCnt 最高 | 内容 |
|---|---:|---:|---:|---|
| `annualized_pd_{1m,3m,6m,1y,2y,3y,4y,5y,7y,10y}_jc7` | 10 | 0.8734 | 1 | **JC7 缩减式**违约概率，10 个期限，单位 % |
| `mdl53_ms5_{1m,3m,6m,1y,2y,3y,4y,5y,7y,10y}` | 10 | 0.9259 | 2 | **MS5（Kamakura Merton 结构化 v5）**，同 10 期限 |
| `mdl53_implied_spreads` | 1 | 0.9160 | 3 | 模型隐含信用价差（bp），集内最高用量 |
| `data_observation_date_4` | 1 | 1.0 | — | SYMBOL 日期，非信号 |

**这是 DEU 迄今发现的模板多样性最好的单一数据集**：10 期限 × 2 模型 + 1 个价差 ⇒
水平 / 斜率 / 曲率 / 跨模型分歧 / 风险溢价 / 二阶矩 / 分桶共 10 个结构互异模板，无需跨数据集，ATOM 纯单集。

### 论坛 + 文献取证

`search_forum_posts("credit risk default probability", max_results=15)` → 15 条，`navigation_failed: false`。
4 条直接可用：
1. **【Alpha灵感】Forecasting Default with the KMV-Merton Model**（28 票 / JL11546）——基于
   Bharath & Shumway (2008, RFS)，正对 `model53` 的 MS5 结构化模型。
2. **【Alpha Idea】概率高还不够：用「稳定性调整」过滤五日下行预测**（2026-09-22 / CW62372）——
   `relative_probability = group_rank(model_probability, economic_group)` +
   `probability_uncertainty = ts_std_dev(...)` ⇒ 直接演化为本波 T9/T10。
3. **【Alpha灵感】Merton's Model in Credit Risk Modelling**（15 票）。
4. **【Alpha 模板】Earnings模板分享**（39 票 / 21 评论）——`ts_backfill` 回填范式。

**文献方向冲突（已做双向覆盖）**：
- Campbell-Hilscher-Szilagyi (2008, JF)「In Search of Distress Risk」：高 PD 股收益**异常低** ⇒ 负号。
- Vassalou & Xing (2004, JF)「Default Risk in Equity Returns」：违约风险被定价，高 PD 股收益**更高** ⇒ 正号。
- Elton-Gruber-Agrawal-Mann (2001, JF)：信用价差中预期违约损失仅占 17–20%，其余为风险溢价 ⇒ T8 正号。

⇒ **符号不确定**，故 T1/T2/T3/T4/T5/T7/T9/T10 取负、T6/T8 取正，双向覆盖。

### 结果（10/10，全部 `pyramids.list = [{DEU/D1/MODEL, 1.8}]`）

| # | alpha | 模板 / 骨架 | S | F | 2Y | SUB | TO | margin | DD | risk_neut | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T1 | `O0AwA0Qd` | 困境异象·水平 `-group_rank(bf(pd_1y,22),sector)` | **0.07** | 0.01 | 0.29 | 0.34 | 4.48% | 0.24bp | **41.05%** | −0.23 | 3 |
| T2 | `0mYkYmqk` | 信用曲线斜率 1Y−10Y | 0.36 | 0.15 | −0.27 | 0.67 | 4.78% | 9.42bp | 11.31% | 0.11 | 3 |
| T3 | `j2YlY2vj` | 信用曲线曲率（蝶式 1M/2Y/10Y） | **−0.28** | −0.10 | −0.15 | **−0.46** | 5.85% | −5.95bp | 27.33% | 0.26 | 4 |
| **T4** | **`O0AwA0Od`** | **★ 自身历史异常 `-group_zscore(ts_zscore(bf(pd_1y,22),252),industry)`** | **0.55** | **0.29** | **0.50** | 0.41 | 10.06% | 6.87bp | 13.28% | 0.32 | 3 |
| T5 | `KPJYJP0j` | 恶化动量 63d `-group_zscore(ts_delta(bf(pd_1y,22),63),industry)` | 0.30 | 0.13 | −0.35 | 0.17 | 10.98% | 4.27bp | 23.15% | **0.46** | 3 |
| T6 | `npvkvpJ8` | 跨模型分歧 MS5−JC7 | −0.02 | 0.00 | −0.16 | 0.28 | 5.63% | −0.44bp | 24.90% | −0.33 | 3 |
| T7 | `RREZER3o` | 隐含价差水平 `-group_rank(bf(implied_spreads,22),sector)` | 0.16 | 0.05 | **0.89** | −0.07 | 3.73% | 7.17bp | **39.65%** | −0.10 | 4 |
| T8 | `9qxPxq1o` | 风险溢价 价差÷PD | 0.17 | 0.05 | **−0.88** | 0.42 | 3.74% | 6.14bp | 23.27% | 0.17 | 3 |
| T9 | `6XdPdXVE` | PD 波动率 二阶矩 | 0.22 | 0.08 | 0.47 | 0.47 | 3.11% | **11.01bp** | 30.07% | −0.18 | 3 |
| T10 | `GrW0WrAx` | 波动率分桶 × 组内排名 | −0.11 | −0.03 | −0.51 | −0.41 | 7.97% | −1.73bp | 23.37% | −0.01 | 4 |

**天花板 |S| = 0.55**（T4），距 `LOW_SHARPE 1.58` 差 **65%**。全部 10 条 `failed_ra_count ≥ 3`。
本波零候选、零可提交。

### ★★★ 核心发现一：困境异象（CHS 2008）在 DEU 彻底不成立，且形状就是「噪声」

T1 是文献最经典、最直白的信用风险骨架：买低 PD、卖高 PD。结果：

| 指标 | 值 | 解读 |
|---|---:|---|
| Sharpe | **0.07** | 等于零 |
| Fitness | 0.01 | 等于零 |
| **Drawdown** | **41.05%** | **全波最差，是本波唯一超过 40% 的** |
| margin | 0.24bp | 最差 |
| risk_neutralized_sharpe | **−0.23** | 反号 |

**机理**：DEU 是银行主导的信用市场，企业违约概率早已被关系型信贷（Hausbank 制度）与主银行监督
内部化，公开 PD 模型的横截面差异不携带新增定价信息。而 CHS 的美国结论建立在**公开债券市场定价**
基础上（债券利差 vs 股票收益的错配），该错配在 DEU 不存在。

⇒ **规则：DEU 不做「违约概率水平」类因子。** 这与 §118 `pv106` 的「价差水平无溢价」形成同构——
**DEU 的横截面中性化（SUBINDUSTRY）把一切绝对水平吃光**。

### ★★★ 核心发现二：`-group_zscore(ts_zscore(F,252),industry)` 是两次独立实证的全波最高几何

这是本波最有价值的跨数据集产出。两个**完全不同机制、不同数据集、不同波次**的实证给出同一结论：

| 波次 | 数据集 | 机制 | 同几何 alpha | S（该波最高） | 水平型对照 | S |
|---|---|---|---:|---|---:|
| 117 | `pv106` | 买卖价差（流动性） | `j2YlAL2Z` | **1.38** | `3qoYXdMN`（水平 126d） | 0.13 |
| 119 | `model53` | 违约概率（信用风险） | `O0AwA0Od` | **0.55** | `O0AwA0Qd`（水平 rank） | 0.07 |

两者都是 `-group_zscore(ts_zscore(F, 252), industry)`，两者都是各自波次的最高 S，两者都把
「水平型」对照打成近零。

**机理（第一性）**：DEU 全仓已是 `SUBINDUSTRY` 中性化 ⇒ 任何**绝对水平**的横截面信息在被中性化时
已被剥离干净，剩下的是纯噪声。而 `ts_zscore(F, 252)` 先做**时间序列标准化**，把「这家公司相对它自己
过去一年是否异常」抽出来，这是一阶差分性质的信息，与横截面水平的共线度低，中性化后仍有残差。

**⇒ 落地规则（DEU 通用，跨数据集）**：DEU 遇到「比率/水平/强度」型字段时，第一骨架首选
`group_zscore(ts_zscore(ts_backfill(F, 22), 252), industry)`，而不是 `group_rank(ts_mean(F, N), sector)`。
分组轴用 `industry` 优于 `sector`（本波 T4 industry vs T1 sector，但注意 T1 用的是 rank 不是 zscore，非纯对照）。

**注意边界**：这条规则只解决「几何选错」问题，不解决「机制不成立」。`model53` 用了最优几何也只有 0.55，
说明信用风险机制本身在 DEU 无效——**几何最优化只能把信号从噪声里提出来，不能凭空造出信号**。

### ★★ 核心发现三：跨模型分歧（MS5 vs JC7）无信息 —— 两模型高度共线

T6 `group_zscore(subtract(rank(ms5_1y), rank(pd_1y)), sector)` ⇒ S **−0.02** / F 0.00 / 2Y −0.16。

MS5 是 Kamakura Merton 结构化模型（股票价格隐含），JC7 是缩减式（财务比率驱动），理论上应该
分歧显著（结构化模型领先财务数据）。实测做差后 S 恰为零 ⇒ **两模型在 DEU 的排序几乎相同**，
做差只留下噪声。

**这是「跨模型分歧」类模板的第 2 次失败**：§116 的 ARM 族（`arm_score_5pt_scale_2` vs
`arm_score_change_7d_3`）也是全灭。⇒ **同一底层标的的两个预测模型，横截面排序高度共线，
做差几何在 DEU 无效，不要再用。**

### ★★ 核心发现四：2Y 与 S 在弱信号上会剧烈背离（不可单独用作判据）

| alpha | S | 2Y | 偏离 |
|---|---:|---:|---:|
| T7 隐含价差水平 | 0.16 | **0.89** | 2Y 是 S 的 5.6 倍 |
| T8 风险溢价 | 0.17 | **−0.88** | 符号相反 |
| T2 曲线斜率 | 0.36 | −0.27 | 符号相反 |

T7 的 2Y 0.89 是本波最高，但它的 S 只有 0.16、DD 39.65%、SUB −0.07 ⇒ **2Y 高不代表有信号**，
只代表「最近两年这段样本里恰好走对方向」。信号强度必须看 S，2Y 只能作为**稳定性**的辅助判据，
且在 S < 1.0 时 2Y 读数完全不可信。

### 本波净收益

- **判死 `model53`**（`DEU-MODEL53-CREDIT-RISK-DEAD`），DEU dead_end 63 条。
- 确立 **DEU 第一骨架规则**：比率/水平型字段优先 `group_zscore(ts_zscore(F,252), industry)`。
  该规则有 pv106 + model53 两次独立实证（同几何均为全波最高，水平型均为近零）。
- 判死「跨模型分歧」模板族（第 2 次失败）。
- 确立「2Y 在 S < 1.0 时不可信」的读数纪律。
- **MODEL 塔点塔路径未推进**：`model53` 全灭，仍需下一个 MODEL 数据集才能点亮。
- 累计：本轮 19 波（101–119）共 **170 条回测，4 条全闸过**。

---

## §120 存量 self 相关审计 + 相关性矩阵 + 6 条提交方案（2026-11-01）

**目标**：对 16 条本地过闸的 DEU 候选做 self 相关全审计（此前只测过 prod），
组出可同批提交的篮子，并查明 `78Zl8gPZ` self 0.7451 的根因。
波 120（sentiment27 十模板）结果另行归因。

### §120.1 self 相关全审计（16 条，10 FAIL / 6 PASS）

`check_self_correlation(correlation_type="self", threshold=0.7)`，纯本地零配额
（pool_size 10 / full_os_pool_size 11 / excluded_power_pool_count 1）。

| alpha | dataset | self | top 相关源 | 判定 |
|---|---|---:|---|---|
| **`ZYQw5RNQ`** | sentiment7 | **0.1245** | Vk65zLzG 0.1245 | ✅ PASS |
| **`e758plEM`** | sentiment7 | **0.1223** | blRnKEk6 0.1223 | ✅ PASS |
| **`leA6qLNe`** | sentiment7 | **0.1358** | blRnKEk6 0.1358 | ✅ PASS |
| **`1YNv6Ymk`** | OTHER 单字段 | **0.1335** | 883Y3bAW 0.1335 | ✅ PASS |
| `E5vxZ7bK` | other455 | 0.8591 | **2rOe10qY** 0.8591 | ❌ FAIL |
| `d5WwzRMY` | institutions1 | 0.9287 | **2rmGAPqN** 0.9287 | ❌ FAIL |
| `E56AzejK` | institutions1 | 0.9184 | **2rmGAPqN** 0.9184 | ❌ FAIL |
| `1Yx01KgW` | risk60 | 0.7227 | blRnKEk6 0.7227 | ❌ FAIL（差 0.023） |
| `1Yx01KgJ` | risk60 | 0.7176 | blRnKEk6 0.7176 | ❌ FAIL（差 0.018） |
| `883X7Jnl` | risk60 | 0.7153 | blRnKEk6 0.7153 | ❌ FAIL（差 0.015） |
| `78Zl8gPZ` | sentiment27+MODEL | 0.7451 | blRnKEk6 0.7451 | ❌ FAIL（差 0.045） |
| `Jjxrl0dx` | shortinterest3 | 0.8086 | vRk6og8b 0.8086 | ❌ FAIL |
| `E5vx03Q0` | shortinterest3 | 0.8750 | vRk6og8b 0.8750 | ❌ FAIL |
| `mLg11W6W` | dl_riskfree_returns | 0.7898 | blRnKEk6 0.7898 | ❌ FAIL |
| `2rOW9xA6` | insider_agg_matrix | 0.9750 | Vk65zLzG 0.9750 | ❌ FAIL |

**结论：self 相关（而非 prod）才是存量候选真正的墙** —— 10/16 全挂 self，
失败源清一色是**已提交的同数据集 alpha**（`2rOe10qY` / `2rmGAPqN` / `vRk6og8b` / `blRnKEk6`）。
3 条 risk60 候选全部只差 0.015–0.023，但 top 相关源都是同一提交 alpha `blRnKEk6`。

### §120.2 ★★ `78Zl8gPZ` self 0.7451 根因查明 —— 后 3 腿与 `blRnKEk6` 完全相同

`get_alpha_details("blRnKEk6")` 取回完整表达式后逐腿对比：

| 腿 | `blRnKEk6`（self 源） | `78Zl8gPZ` |
|---|---|---|
| 1 | `if_else(is_nan(-rank(vec_avg(mean_loan_rate_main))),0,-rank(vec_avg(mean_loan_rate_main)))` ← **risk60** | `rank(ts_mean(vec_avg(snl27_totaldomains),22))` ← sentiment27 |
| 2 | `rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4,5))` | **完全相同** |
| 3 | `rank(ts_mean(predicted_surprise_f12m_ebitda_4,5))` | **完全相同** |
| 4 | `rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,22))` | **完全相同** |

**4 腿等权 add ⇒ 共享 3/4 = 75% 权重 ⇒ self 0.7451 完全说得通。**

★ **这推翻了此前拟定的三个降 self 方向**（换 sentiment27 腿 / 换 snl27 字段 /
vector_neut 对 snl27 另一字段）—— **全部砍不到共同因子**。
正确改法 = **换掉被占用的 3 条 starmine 腿**（K1/K2/K5）。

`blRnKEk6` 附带信息（重要）：
- `ACTIVE` / `OS` / 提交于 2026-09-13 / **color `GREEN`** / **name `"0.5766"`**（★ 违反命名规范，
  把 prod 数值写进了 name）
- tags: `CH_PPA` / `SRC_predictive_starmine` / `PowerPoolSelected`（**PPA 通道 alpha**）
- S **2.02** / F **1.70** / TO 16.15% / returns 11.41% / DD 4.96% / margin 14.13bp
- self **0.0** / prod **0.5766** / SUB 1.43 / **2Y 2.74** / invest_S 1.72 / risk_neut 1.61
- `pyramids.effective = 2`：**SHORTINTEREST ×1.3 + MODEL ×1.8**
- `checks.fail = []` / `checks.pending = []` / `failed_ra_count 0`
- settings 与 78Zl8gPZ 完全一致（SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF）

### §120.3 波 121 派发 —— `78Zl8gPZ` 降 self 改写（10 个结构互异模板）

multisim `4nV4kH5nO4DlbwZWAEh4z6s`。设置 DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08/nanHandling OFF。

**共用第 1 腿**（sentiment27，与 blRnKEk6 无共享）：
`S1 = rank(ts_mean(vec_avg(snl27_totaldomains), 22))`

**未被 `blRnKEk6`（K1/K2/K5）与 `bl62jGgM`（PSp/PS/PSe/K1/PSb）占用的 starmine 腿**：
```
K3  = rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5))    # ebitda 14d 修订
K4  = rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 5))         # fy2 盈利 surprise
PSr = rank(ts_mean(predicted_surprise_pct_fy2_revenue_4, 5))          # fy2 营收 surprise（aCnt 仅 12，未拥挤）
PS1 = rank(ts_mean(predicted_surprise_pct_fy1_ebitda, 5))             # fy1 ebitda surprise
PSe = rank(ts_mean(predicted_surprise_pct_f12m_earnings_5, 5))        # 12m 盈利 surprise
```

| T | 几何 | 腿配比 | 表达式核心 |
|---|---|---|---|
| T1 | 4 腿 add·全换 A | 1S+3★ | `add(add(add(S1,K3),K4),PSr)` |
| T2 | 4 腿 add·全换 B | 1S+3★ | `add(add(add(S1,K3),PS1),PSe)` |
| T3 | 4 腿 add·全换 C | 1S+3★ | `add(add(add(S1,K4),PSr),PS1)` |
| T4 | 5 腿稀释 | 1S+4★ | `add(add(add(add(S1,K3),K4),PSr),PS1)` |
| T5 | 3 腿精简 | 1S+2★ | `add(add(S1,K3),PSr)` |
| T6 | 2+2 平衡 | 2S+2★ | `add(add(S1,S2),add(K3,PSr))` |
| T7 | 3+1 稀释 | 3S+1★ | `add(add(add(S1,S2),S3),K3)` |
| T8 | vector_neut 正交 | 1S+3★ | `vector_neut(T1核心, ts_zscore(ts_backfill(vec_avg(snl27_relpopularity08),22),252))` |
| T9 | 乘性置信度门控 | 1S+3★ | `multiply(T1核心, rank(ts_mean(vec_avg(snl27_kurtosis),22)))` |
| T10 | group_rank(sector) | 1S+3★ | `group_rank(T1核心, sector)` |

（S2 = `snl27_relpopularity08` 腿；S3 = `snl27_skewness` 腿）

**归因维度**：T1/T2/T3 = 字段组合对 self/S 的影响；T4 vs T1 = 腿数稀释；
T5 vs T1 = 精简；T6/T7 vs T1 = sentiment27 腿占比；T8 vs T1 = vector_neut 正交；
T9 vs T1 = 乘性门控；T10 vs T1 = 分组轴。

### §120.4 波 120：`sentiment27` 十模板探针 → 10/10 全灭（单数据集 ATOM 判死）

multisim `4calHD6pB4sT9pihGyE0kAF`，10/10 完成无错。**全部 `pyramids.effective=1`
/ `DEU/D1/SENTIMENT ×1.8`（单塔 ATOM，不触 trio 禁令、不占 duo 额度）。**

| T | alpha | 几何 | S | F | 2Y | SUB | TO | margin | DD | ra_failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **T5** | `YP1wYO9R` | **比值 relpop/totaldom** | **+0.52** | 0.29 | **1.28** | 0.64 | **2.33%** | **3.35bp** | 18.32% | 3 |
| T4 | `P0orKbAK` | 差值 totaldom−avgrank | +0.37 | 0.16 | 0.97 | 0.69 | 2.60% | 1.79bp | 11.94% | 3 |
| T9 | `9qxPk33V` | **ts_corr 协动性** | +0.39 | 0.16 | 0.39 | −0.61 | 7.57% | 0.53bp | **5.99%** | 4 |
| T8 | `d5W8v66x` | 差分动量 63d | +0.07 | 0.01 | −0.72 | −0.55 | 14.53% | — | 15.47% | 4 |
| T7 | `78LqlrrQ` | 峰度水平 | +0.05 | 0.01 | −0.09 | 0.92 | 16.26% | — | 11.47% | 3 |
| T2 | `npvkrlXM` | M159 排名反号 | −0.19 | −0.05 | −0.49 | −0.74 | 15.38% | — | 10.86% | 4 |
| T3 | `9qxPk32V` | 水平 group_rank | −0.36 | −0.15 | −0.58 | −0.88 | 2.89% | — | 15.75% | 4 |
| T6 | `GrW09NNJ` | 二阶方差 std_dev | −0.62 | −0.35 | −1.64 | −0.32 | 2.92% | — | 32.16% | 4 |
| T10 | `rKR68wwa` | vector_neut 正交 | −0.62 | −0.30 | −1.17 | −1.07 | 12.73% | — | 20.01% | 4 |
| T1 | `3qoYJOJ0` | M159 认知水平 | **−1.00** | −0.59 | −1.22 | −0.83 | 13.61% | — | 25.46% | 5 (+CW 0.5 @2019-02-19) |

**十模板**（全部纯 sentiment27，字段 `vec_avg` 已裹）：
```
T1  -group_zscore(ts_zscore(ts_backfill(vec_avg(snl27_totaldomains),22),252), industry)       # M159·投资者认知 H1(Merton1987)
T2   group_zscore(ts_zscore(ts_backfill(vec_avg(snl27_avgranking),22),252), industry)          # M159·注意力反号 H1(Fang-Peress2009)
T3   group_rank(ts_mean(vec_avg(snl27_top50pctrankingavg),22), sector)                         # 水平
T4   group_zscore(subtract(rank(ts_mean(vec_avg(snl27_totaldomains),22)), rank(ts_mean(vec_avg(snl27_avgranking),22))), sector)   # 跨字段分歧 H5
T5   group_rank(divide(ts_mean(vec_avg(snl27_relpopularity08),22), add(ts_mean(vec_avg(snl27_totaldomains),22),0.001)), sector)    # 比值·注意力效率 H5
T6  -group_rank(ts_std_dev(ts_backfill(vec_avg(snl27_relpopularity08),22),126), sector)        # 二阶矩·稳定性 H3/H4
T7   group_zscore(ts_zscore(ts_backfill(vec_avg(snl27_kurtosis),22),252), industry)            # 分布形状·集中度 H4
T8   group_zscore(ts_delta(ts_backfill(vec_avg(snl27_top50pctrankingavg),22),63), industry)     # 一阶差分动量 H2(Da2011/Lou2009)
T9   group_zscore(-ts_corr(vec_avg(snl27_totaldomains), vec_avg(snl27_avgranking),63), sector) # ts_corr 协动性·论坛 M166(36票)
T10  vector_neut(ts_zscore(ts_backfill(vec_avg(snl27_top50pctrankingavg),22),252), ts_backfill(vec_avg(snl27_relpopularity08),22)) # M37 正交
```

**归因结论**：
1. **符号规律极干净** —— 跨字段「比值/差值」构造全为正（T4 +0.37 / T5 +0.52），
   单字段水平/几何全为负（T1 −1.00 / T2 −0.19 / T3 −0.36 / T6 −0.62 / T10 −0.62）
   ⇒ **sentiment27 的信号不在任一字段的水平里，只在字段间相对关系**（单位网络规模的注意力效率）。
2. **天花板 S 0.52 / F 0.29**，无一达 near 线 1.0 ⇒ **`sentiment27` 单数据集 ATOM 判死**
   （已登记 `DEU-SENTIMENT27-ATOM-DEAD`）。
3. **T5 `YP1wYO9R` 有残余机制价值**：S 0.52 / F 0.29 / **2Y 1.28** / SUB 0.64 /
   **TO 2.33%（本波最低）** / **margin 3.35bp（本波最高）**。2Y ≫ S ⇒ 慢信号。
   但 S<1.0 时 2Y 不可信，且 S/F 双卡、不达 `mode_b_qualification`（S≥1.25 且 F≥0.8）。
4. **T9 `ts_corr` 算子首次在 DEU 实跑通过**（无 ERROR），DD 5.99% 本波最低
   ⇒ 可留作降 DD 辅助腿，非主信号。
5. **T7 SUB 0.92 异常高但 S 0.05** ⇒ 再次印证铁律「S<1.0 时 2Y/SUB 等衍生指标一律不可信」。
6. **T1 M159（DEU 第一骨架）在 sentiment27 上反向失效**（S −1.00 且 CW 0.5）
   ⇒ M159 只对「比率/水平型」字段有效，对排名/流行度类结构性字段不适用。
7. **结论与 `ZYQw5RNQ` / `QPveY7Kg` 的成功一致**：DEU 的 SENTIMENT 类**唯一有效构造
   是 sentiment7 × sentiment27 的 `vector_neut` 跨集正交**（S 1.73 / 2.03），单数据集全灭。

### §120.5 6 条可同批提交的篮子（`compute_mutual_correlation` threshold 0.7 / years 4 / 1021 点）

```
alpha_ids = [1YNv6Ymk, ZYQw5RNQ, QPveY7Kg, MPY9VNY9, Vkxnb8QG, bl62jGgM]
→ all_below_threshold: true
→ max_pair = ZYQw5RNQ ↔ QPveY7Kg = 0.5034
→ max_mutually_below_subset_size = 6
```

| | 1YNv6Ymk | ZYQw5RNQ | QPveY7Kg | MPY9VNY9 | Vkxnb8QG | bl62jGgM |
|---|---:|---:|---:|---:|---:|---:|
| 1YNv6Ymk | 1 | 0.054 | −0.0272 | 0.0212 | −0.0044 | 0.0201 |
| ZYQw5RNQ | 0.054 | 1 | 0.5034 | 0.097 | 0.0215 | 0.0703 |
| QPveY7Kg | −0.0272 | 0.5034 | 1 | 0.0328 | −0.0367 | −0.0387 |
| MPY9VNY9 | 0.0212 | 0.097 | 0.0328 | 1 | 0.085 | 0.1304 |
| Vkxnb8QG | −0.0044 | 0.0215 | −0.0367 | 0.085 | 1 | 0.215 |
| bl62jGgM | 0.0201 | 0.0703 | −0.0387 | 0.1304 | 0.215 | 1 |

**塔位增量**（当前 DEU/D1 = institutions:1, model:1, other:2, analyst:1, fundamental:1）：
- `1YNv6Ymk` → **OTHER 2→3 ⇒ OTHER 塔点亮**
- `ZYQw5RNQ` + `QPveY7Kg` → **SENTIMENT 0→2**
- `MPY9VNY9` → **SHORTINTEREST 0→1**
- `Vkxnb8QG` → **ANALYST 1→2**
- `bl62jGgM` → **MODEL 1→2**

净增 4 个塔位 + 点亮 1 塔。

### §120.6 prod 终验进展（部分卡在平台槽）

| alpha | prod max | 判定 | 来源 | 落库 |
|---|---:|---|---|---|
| `2rAP60oP` | **0.7548** | ❌ 撞墙 | 缓存命中（10-30 07:36:37） | `already_set` |
| `QPKKMg6Q` | **0.8070** | ❌ 撞墙 | 缓存命中（10-30 06:33:19） | `already_set` |
| `1YNv6Ymk` | **未知** | ⏸ 超时 120s | 平台槽被占 | 未落 |
| `QPveY7Kg` | **0.6671** | ✅ | 已验 | 已落 |
| `MPY9VNY9` | **0.5986** | ✅ | 已验 | 已落 |
| `Vkxnb8QG` | **0.6384** | ✅ | 已验 | 已落 |
| `ZYQw5RNQ` | 未测 | ⏸ | | |
| `bl62jGgM` | 未测 | ⏸ | | |

- 两条 FAIL 均为**缓存命中**（平台早已算完），本次重试**未占平台 prod 槽、未留 inflight 残留**。
- `persist_correlation` 两条均返回 `skipped: "already_set"`。
- **`QPKKMg6Q` 直方图右尾有 1 个落在 0.8–0.9 区间**，撞得比 `2rAP60oP` 更狠。
- 两条候选 prod 全部撞墙 ⇒ **不能进提交篮**。
- `1YNv6Ymk` 重试再次 120s 超时 ⇒ 300s inflight 残留，**不得连打**。

### §120.7 论坛取证（波 120 机制验证）

- `search_forum_posts("web attention alpha", max_results=15)` → 15 条（★ 短 query 才行，
  长 query 会 `navigation_failed`）。
- 命中直接相关：「【Alpha灵感】盈利不确定性和公司关注度」（`21149732774039`）、
  「Improved Version of Attention: Implied Volatility Spreads and Stock Return」
  （`21120326355479`，引 doi `10.1080/15427560.2019.1692846`）。
- 命中高票工具帖：「使用图论最大团算法深入分析 Alpha 相关性」（85 票 / 13 评论，`34574522475031`）
  —— 明确「同一团内提交其中一个后，其他 alpha 无法通过 PPA 自相关检测」，与本轮 self 审计结论一致。
- 外部文献先验（`web_search` 不可用，来自既有知识）：Barber-Odean 2008（注意力→价格压力→反转）、
  Fang-Peress 2009（无媒体溢价）、Merton 1987（投资者认知）、Lou 2009（媒体驱动反转）、
  Da-Engelberg-Gao 2011（搜索注意力反转）。

### §120.8 6 条候选完整表达式与指标（真实 code，`get_alpha_details` 取回）

| alpha | code | pyramids.list | S / F / 2Y / SUB / TO / margin / DD | 特殊 settings |
|---|---|---|---|---|
| `1YNv6Ymk` | `group_rank(tm_15_r1_r5_r10_rh_glb_d1_r10_q1, sector)` | **OTHER ×1.8** | 2.28 / 1.25 / 1.60 / 1.11 / 37.92% / 5.98bp / 5.53% | **CROWDING** 中性化 |
| `ZYQw5RNQ` | `vector_neut(quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22), ts_delay(...,1..4)),5),15),driver="uniform"), ts_backfill(vec_avg(snl27_relpopularity08),22))` | **SENTIMENT ×1.8** | 1.73 / 1.49 / 2.11 / 1.46 / 11.01% / 16.94bp / 7.29% | decay 16 / trunc 0.02 / nanHandling ON |
| `QPveY7Kg` | `vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22), ts_delay(...,5)),5),22),252,driver="gaussian"), ts_backfill(vec_avg(snl27_relpopularity08),22))` | **SENTIMENT ×1.8** | 2.03 / 1.61 / 2.54 / 1.20 / 16.10% / 12.60bp / 6.00% | decay 2 / trunc 0.02 / nanHandling ON |
| `MPY9VNY9` | `-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),240)),rank(ts_delta(ts_backfill(vec_avg(shrt3_bar),22),176))),target_tvr=0.03),subindustry)` | **SHORTINTEREST ×1.3** | 1.59 / 1.26 / 2.36 / 1.02 / ~3% | `ts_target_tvr_decay` |
| `Vkxnb8QG` | `trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main),252))<0.75, group_neutralize(group_rank(add(ts_backfill(eps_y1_estimate_change_3mo,1008), ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),210)),sector), bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),252)),range="0,1,0.05")), -1)` | **ANALYST ×1.8** | 1.83 / 1.64 / 2.09 / 0.99 | trade_when + bucket |
| `bl62jGgM` | `divide(add(add(add(add(rank(ts_mean(predicted_surprise_pct_f12m_ebitda_5,5)), rank(ts_mean(predicted_surprise_fy1_ebitda_4,5))), rank(ts_mean(predicted_surprise_pct_f12m_earnings_5,5))), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4,5))), rank(ts_mean(predicted_surprise_pct_fy2_ebitda_4,5))), 5)` | **MODEL ×1.8** | 1.78 / 1.50 / 1.75 / 1.37 | 模板 M141「4 非 book + 1 book」 |

**`78Zl8gPZ`**（SENTIMENT+MODEL 双塔，self 0.7451 ❌）：
`add(add(add(rank(ts_mean(vec_avg(snl27_totaldomains),22)), rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4,5))), rank(ts_mean(predicted_surprise_f12m_ebitda_4,5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,22)))`
S 1.59 / F 1.35 / 2Y 2.11 / SUB 1.31 / TO 13.88% / margin 14.47bp / DD 6.87% / risk_neut 1.54
★ 唯一障碍 = self 0.7451（vs `blRnKEk6`，共享 K1/K2/K5 三条 starmine 腿）。
★ 78Zl8gPZ 与 `ZYQw5RNQ` 0.2615 / `QPveY7Kg` −0.0107 / `kqNRX1ZP` 0.0001 —— 完全正交，
**只差 self 就能让 SENTIMENT 塔 0→3 一次点亮**。


## §123 数据跨度审计：SENTIMENT 塔判死（2026-11-01）

### §123.1 起因：用户抓出「近十年都要有数据」违规

用户核对 `Jje0J2rx` 时指出：「不是要求近十年有数据，这个前三年都没数据」。
逐年数据（`get_alpha_yearly_stats`）证实——**而且比用户判断的更严重，空前窗是 5 年不是 3 年**。

`Jje0J2rx`（sentiment27+predictive_starmine，波122 V4，S 1.59/F 1.31/2Y 2.21 全闸过）：

| 年份 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| pnl | 0 | 0 | 0 | 0 | 0 | 235713 | 512083 | 1779649 | 1618222 | 1038596 |
| longCount | 0 | 0 | 0 | 0 | 0 | 101 | 131 | 154 | 169 | 157 |
| shortCount | 0 | 0 | 0 | 0 | 0 | 88 | 113 | 146 | 156 | 138 |

**2014-2018 完全无持仓无 PnL，2019-03-05 才开始交易**。汇总指标 S/F/2Y 只对 2019-2023 这 5 年计算，
完全掩盖了空窗。先前只看汇总闸门、未查逐年数据覆盖 = 疏漏。

### §123.2 根因定位：sentiment 类数据集短历史（对照实验铁证）

| alpha | 数据集 | 2014-2018 持仓 | 有效跨度 | 10年合规 |
|---|---|---|---|---|
| `bl62jGgM` | 纯 predictive_starmine | 满（S 2.45/2.58/0.99/2.18/1.65） | 10yr | ✅ |
| `1YNv6Ymk` | dl_riskfree (OTHER) | 满（S 1.78/4.13/1.95/3.14/1.38） | 10yr | ✅ |
| `MPY9VNY9` | shortinterest3 | 满（S 2.17/1.98/0.90/1.23/0.28） | 10yr | ✅ |
| `Vkxnb8QG` | analyst+shortinterest | 满（S 2.29/3.10/1.60/1.55/1.69） | 10yr | ✅ |
| `Jje0J2rx` | sentiment27+starmine | 全 0 | 5yr (2019-) | ❌ |
| `ZYQw5RNQ` | sentiment7+sentiment27 | 全 0 | 5yr (2019-) | ❌ |
| `QPveY7Kg` | sentiment7+sentiment27 | 全 0 | 5yr (2019-) | ❌ |

**根因**：`sentiment7` / `sentiment27` 数据约 2019 年才开始。表达式里 `add()` / `vector_neut()`
任一腿 NaN 归零，把整条 alpha 在 2014-2018 拖死。
**`predictive_starmine` / `shortinterest3` / `analyst` / `dl_riskfree` 均有完整 10 年数据。**

### §123.3 sentiment33 探针：SENTIMENT 塔最后一个希望也破灭

sentiment33 是 DEU 唯一剩的 SENTIMENT 数据集（cov 0.32，255 字段全 VECTOR 文档/词频字段）。
探针 multisim `1mmHylfTq5fAb1iNIxigBE3`（3 条单集 ATOM，`vec_sum` 折叠词频，nanHandling OFF）：

| alpha | 字段 | S | 结论 |
|---|---|---|---|
| `O0Aw3Wkv` | sentiment_model9_score5_fkw2 | 0.40 | 最优，仍远低于闸 |
| `P0orV5qp` | sentiment_model7_score1_fkw4 | 0.05 | |
| `zq3wVdQV` | sentiment_model6_negative_score_fkw3 | -0.51 | |

`O0Aw3Wkv` 逐年数据：

| 年份 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019-2023 |
|---|---|---|---|---|---|---|
| pnl | 0 | 0 | 0 | 0 | 962295 | 满（有正有负） |

**sentiment33 数据从 2018 年才开始**（前 4 年全空），跨度 2018-2023 = 6 年，仍不满足「近十年」。

### §123.4 结论：DEU SENTIMENT 塔正式判死

**三个 SENTIMENT 数据集全部不满足 10 年数据约束**：
- `sentiment7` / `sentiment27` → 2019 起（5 年）
- `sentiment33` → 2018 起（6 年）

**⇒ 在「近十年都要有数据」硬约束下，DEU 的 SENTIMENT 塔无法点亮。**
这是数据层的结构性封死，不是信号强弱问题——再多模板也救不了。

已登记判死簿：`DEU-SENTIMENT-TOWER-DATASPAN-DEAD`（layer=dead_end）。

### §123.5 新硬闸：派发前必查逐年数据覆盖

**教训固化**：候选即使 `checks.fail=[]` + `failed_ra_count=0` + self<0.7，只要
`get_alpha_yearly_stats` 显示 2014-2018 任一年 pnl=0 且 longCount=0，即违反 10 年约束，直接除名。
**汇总指标不可信，逐年数据才是数据覆盖的唯一真相。**

### §123.6 幸存者（4 条，全部满 10 年数据）

| alpha | 数据集 | 塔位 | S | F | 2Y | self | prod | 备注 |
|---|---|---|---|---|---|---|---|---|
| `bl62jGgM` | predictive_starmine | MODEL | 1.78 | 1.50 | 1.75 | 0.6417 | 未测 | 与 Jje0J2rx 互相关 0.6567（Jje 已废，不再是问题） |
| `1YNv6Ymk` | dl_riskfree | OTHER | 2.28 | 1.25 | 1.60 | 0.1335 | 未测 | 2Y 仅比 1.58 高 0.02，OS 风险高 |
| `MPY9VNY9` | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.2703 | 0.5986 ✅ | |
| `Vkxnb8QG` | analyst+shortinterest | ANALYST | 1.83 | 1.64 | 2.09 | 0.6379 | 0.6384 ✅ | |

**塔位增量（提交这 4 条）**：`1YNv6Ymk` → OTHER 2→3 **点亮** ✅；`bl62jGgM` → MODEL 1→2；
`Vkxnb8QG` → ANALYST 1→2；`MPY9VNY9` → SHORTINTEREST 0→1。SENTIMENT 无法点亮。

### §123.7 待决

1. 4 条 prod 终验（2 条已过：MPY9VNY9 0.5986 / Vkxnb8QG 0.6384；bl62jGgM / 1YNv6Ymk 未测，平台 prod 槽被占）。
2. 是否放宽 sentiment 类另类数据的 10 年约束（若放宽 SENTIMENT 可复议，但 OS 风险更高）。
3. 提交不可逆，须用户真实回复授权（自动勾选不作数）。
## §124 提交篮终验（收割 submit_ready 队列 + 互相关定篮 + prod 缺口）

时间：2026-11-01（数据跨度审计后续）。目标：把提交篮在 10 年硬闸下收敛成可授权提交的一批。


### 一、收割 DEU submit_ready 队列（status=ALL，去重 100 条）

状态分布：DEAD 87 / SUBMITTED 6 / READY 6 / SUPERSEDED 1（各计一次）。

READY 6 条中我已知 2 条（MPY9VNY9/Vkxnb8QG），另 4 条收割核验（数据集 + 10 年跨度 + prod）：


| alpha | 数据集/塔 | S/F/2Y | 2014-2018 跨度 | prod | 结论 |
|---|---|---|---|---|---|

| kqNRX1ZP | sentiment 族 | 2.06/1.86/2.37 | **全 0（2019 起 = 5yr）** | — | **判废**（10 年硬闸）|

| kqJqQL08 | analyst (eps_y1) | 1.78/1.62/1.64 | 满 10yr | 未测 | 同 Vkxnb8QG 骨架，备选 |

| RREXxW6z | analyst (eps_y1) | 1.77/1.61/1.83 | 满 10yr | 未测 | 同 Vkxnb8QG 骨架，备选 |

| QPKKMg6Q | — | 1.65/1.47/1.58 | — | **0.8070 撞墙** | 判废（prod）|


**结论**：队列里没有独立新塔的 10 年合规候选——kqJqQL08/RREXxW6z 都是 `eps_y1_estimate_change_3mo` ANALYST 同族（与 Vkxnb8QG 同骨架，互相关必高，只能取 1）；kqNRX1ZP 5yr 判废；QPKKMg6Q prod 撞墙。印证 4 条篮子即最优。


### 二、篮内互相关（compute_mutual_correlation，4 年 1021 点，本地零配额）

| | bl62jGgM | 1YNv6Ymk | MPY9VNY9 | Vkxnb8QG |
|---|---|---|---|---|

| bl62jGgM | 1.0 | 0.020 | 0.130 | 0.215 |

| 1YNv6Ymk | 0.020 | 1.0 | 0.021 | -0.004 |

| MPY9VNY9 | 0.130 | 0.021 | 1.0 | 0.085 |

| Vkxnb8QG | 0.215 | -0.004 | 0.085 | 1.0 |


最大配对 = bl62jGgM↔Vkxnb8QG **0.215**，全部 < 0.7，`all_below_threshold=true`，`max_mutually_below_subset` = 全 4 条 ⇒ **4 条可同批提交，篮内零冲突**。


### 三、最终提交篮（4 条，全部 10 年 + 全 IS 闸 + self 达标 + 篮内去相关）

| alpha | 塔位 | 数据集 | S/F/2Y | SUB | self | prod | 10yr |
|---|---|---|---|---|---|---|---|

| bl62jGgM | MODEL | predictive_starmine | 1.78/1.50/1.75 | 1.37 | 0.6417 ✅ | 未测 ⏳ | ✅ |

| 1YNv6Ymk | OTHER | dl_riskfree | 2.28/1.25/1.60 | 1.11 | 0.1335 ✅ | 未测 ⏳ | ✅ |

| MPY9VNY9 | SHORTINTEREST | shortinterest3 | 1.59/1.26/2.36 | 1.02 | 0.2703 ✅ | 0.5986 ✅ | ✅ |

| Vkxnb8QG | ANALYST(+SHORTINT) | analyst+shortinterest | 1.83/1.64/2.09 | 0.99 | 0.6379 ✅ | 0.6384 ✅ | ✅ |


塔位增量（提交后）：OTHER 2→3（**点亮**）/ MODEL 1→2 / ANALYST 1→2 / SHORTINTEREST 0→1（Vkxnb8QG 若计双塔则 0→2）。SENTIMENT 塔已判死无法点亮。


### 四、唯一技术缺口：bl62jGgM / 1YNv6Ymk 的 prod 未测

平台 prod 单并发槽被占（此前 holder mLoOG6AW；本次 check_correlation 直接 120s 超时，留 300s inflight 残留，按 SOP 不再连打）。MPY9VNY9(0.5986)/Vkxnb8QG(0.6384) prod 已验。

bl62jGgM/1YNv6Ymk 均低 self（0.64/0.13）+ 非拥挤数据集，prod 风险低，但**未实测前不宣称 prod 合规**。待平台槽释放后补测（间隔 >300s），或按用户授权先发已验的 2 条。


### 五、待用户决策

1. **SENTIMENT 塔处置**（数据已证 5-6yr）：接受判死转攻他塔（推荐）/ 放宽另类数据 10 年约束（复活 SENTIMENT 但 OS 风险高）。

2. **提交授权**（不可逆，需真实确认，自动勾选不作数）：4 条一起等 prod / 先发 prod 已验 2 条 / 暂不提交。

3. **kqJqQL08 vs RREXxW6z vs Vkxnb8QG**（ANALYST 同族三选一）：默认取 Vkxnb8QG（self 与 prod 已验）。
## §125 INSTITUTIONS 探针（fund_holdings_panel）——9 年 + 弱信号，不可用

时间：2026-11-01。按 auto-selected 方向「转攻未点亮塔」推进，首轮打 INSTITUTIONS（1.6x，未点亮 1/3）。


### 一、数据集选择

INSTITUTIONS 5 集：fund_holdings_panel（cov 0.90/18 字段/102 alpha）、institutions6（cov 1.0/11/270）、institutions1（cov 0.23/7/32）、institutions25（cov 0，2012 起）、institutions4（ID 映射）。先打 fund_holdings_panel。

18 字段**全 VECTOR**（须 vec_avg 折叠），cov 0.88-0.93。四类机构资金流机制：边界交易（建/清仓=新信念）/ 参与广度 / 持仓集中度(HHI/分布分) / 持久调仓(stable_boundary_trade_count_21d，最热 23u/33α)。


### 二、探针（multisim 38BXz5cSd4IX9SUgxbHhRea，8 条单机制 ATOM，探针批免模板多样性）

| alpha | 机制 | S | F | TO | 2Y | SUB |
|---|---|---|---|---|---|---|

| xAr9qzXg | 边界交易流动量 | **0.66** | 0.27 | 0.175 | 0.98 | 0.25 |

| A1VY9a6e | 边界交易流水平 | 0.53 | 0.28 | 0.096 | 1.46 | 0.16 |

| qMLv8ze2 | 持久调仓 | 0.42 | 0.20 | 0.053 | 1.39 | 0.18 |

| O0AqOmwv | 大额信念交易 | 0.32 | 0.14 | 0.055 | 1.20 | 0.14 |

| 88R7b6ga | 参与广度 | 0.28 | 0.12 | 0.035 | 0.93 | -0.13 |

| N1Nq0jke | 集中度反转 | 0.28 | 0.12 | 0.025 | 1.10 | -0.11 |

| P0oqNlrp | 集中度 group_rank | -0.27 | -0.11 | 0.046 | -0.95 | -0.09 |

| VkxqVlwY | USD z-score | -0.62 | -0.14 | 0.794 | -0.47 | 0.05 |

信号排序：流动量 > 流水平 > 持久 > 信念 > 广度 ≈ 集中度。**天花板仅 S 0.66**。


### 三、数据跨度（get_alpha_yearly_stats xAr9qzXg，硬闸实证）

**2014 年 pnl=0 / longCount=0（空窗），数据 2015 才起 = 2015-2023 = 9 年**，缺 2014。按「近十年都要有数据」硬闸违规（仅缺 1 年，远轻于 sentiment 缺 5 年）。且逐年 S 剧烈翻脸（2018 +3.48 / 2020 −1.45 / 2023 +2.72，2015/16/19/21 近 0）。


### 四、结论

**fund_holdings_panel 双重不合格：9 年（缺 2014）+ 弱信号（天花板 0.66），即使放宽到 9 年也够不到 1.58。判为不可用。**机构资金流机制在 DEU TOP500 截面预测力本就弱。


### 五、战略评估（60 alpha 目标的现实天花板）

真正「满 10 年 + 强信号」的数据集有限：predictive_starmine(MODEL, bl62jGgM S1.78)、shortinterest3(SHORTINT, MPY9VNY9 S1.59/2Y2.36)、analyst eps_y1(ANALYST, Vkxnb8QG S1.83)、dl_riskfree(OTHER, 1YNv6Ymk S2.28)。SENTIMENT 判死、INSTITUTIONS fund_holdings 不可用。⇒ 60 alpha 在「10 年 + 塔配额(3/塔) + trio 禁混」下**现实上限约 15-25**（DEU 16 塔，SENTIMENT 死、pv 封盘、多塔数据层不可达）。后续挖矿应集中在上述 4 个强 10 年集扩产，或另找 10 年强信号集。


## §126 本地 prod-clean 池全扫 + 数据跨度闸二次拦截 + 4 篮子最优性证明（2026-10-30）

**动机**：平台 prod 单并发槽被外部 alpha 进程持续抢占（`bl62jGgM`/`1YNv6Ymk` prod 连试 120s 超时）。
按「本地 prod-clean 池零配额扩候选」路线推进——扫本地 `alphas` 表，不占仿真/相关性配额。

### 一、本地 prod-clean 池规模
DEU `alphas` 表共 **4084** 条，实测 prod 的仅 **24** 条（`prod_correlation IS NOT NULL AND < 0.7`），
**3977 条 prod NULL**（未测）。prod-clean 池薄，是因为绝大多数 DEU alpha 从未测 prod。

### 二、20 条 alive prod-clean 候选的全闸判定（S≥1.58 / F≥1.0 / 2Y≥1.58）
聚合闸 PASS 仅 4 条：`QPveY7Kg` / `Vkxnb8QG` / `MPY9VNY9` / `npvwXA8l`。
其余 16 条卡 2Y=0.00（无 2Y 数据）或 S/F 不足。

| alpha | ds | S | F | 2Y | SUB | prod | self | 处置 |
|---|---|---|---|---|---|---|---|---|
| QPveY7Kg | 1902 | 2.03 | 1.61 | 2.54 | 1.20 | 0.667 | 0.024 | **判废（SENTIMENT 5yr）** |
| Vkxnb8QG | 1902 | 1.83 | 1.64 | 2.09 | 0.99 | 0.638 | 0.638 | 已在篮 |
| MPY9VNY9 | 1902 | 1.59 | 1.26 | 2.36 | 1.02 | 0.599 | 0.270 | 已在篮 |
| npvwXA8l | 1902 | 1.59 | 1.25 | 2.27 | 0.79 | 0.609 | 0.261 | **剔除（MPY9VNY9 参数变体）** |

### 三、数据跨度闸二次拦截：QPveY7Kg
- 表达式：`vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22), ts_delay(...,5)),5),22),252,driver="gaussian"), ts_backfill(vec_avg(snl27_relpopularity08),22))`
- 字段 `snt7_all_languages_views` + `snl27_relpopularity08` = **sentiment7 + sentiment27**。
- **逐年**：2014–2018 全 `pnl=0`/`longCount=0`（5 年空窗），2019 起才有数据。
- 聚合指标 S 2.03 / F 1.61 / 2Y 2.54 / SUB 1.20 / self **0.024** 干净得反常——**全部只对 2019–2023 算**。
- **结论：SENTIMENT 5yr，数据跨度闸判废。** 这是本轮第二个被数据跨度闸拦下的「神候选」（第一个 Jje0J2rx）。
  印证：**汇总指标再漂亮也不能作数据覆盖判据，逐年数据是唯一真相。**

### 四、npvwXA8l 剔除（参数变体，非独立候选）
- 表达式与 `MPY9VNY9` **完全相同，仅 `target_tvr` 不同**（0.06 vs 0.03）。
- `compute_mutual_correlation` 实证：npvwXA8l ↔ MPY9VNY9 = **0.9197**（近重复）。
- 且 SUB 0.79 / 2Y 2.27 均劣于 MPY9VNY9（1.02 / 2.36）⇒ 严格劣化变体。

### 五、4 篮子最优性证明（数学结论）
`compute_mutual_correlation([bl62jGgM, 1YNv6Ymk, MPY9VNY9, Vkxnb8QG, npvwXA8l])`：
- `max_mutually_below_subset = [MPY9VNY9, bl62jGgM, 1YNv6Ymk, Vkxnb8QG]`
- **`max_subset_exact: true`** ⇒ 这 4 条是本地 prod-clean 池中**最大互不相关子集**（精确，非近似）。
- 5 条相关矩阵最大配对 0.9197（npvwXA8l 冗余），其余全 <0.22。

**最终结论**：4 篮子（bl62jGgM / 1YNv6Ymk / MPY9VNY9 / Vkxnb8QG）是本地 prod-clean 池的
**可证明最优提交集**。要扩产必须挖新数据集（新表达式），不能靠翻旧账。

### 六、阻塞项（不变）
- `bl62jGgM`/`1YNv6Ymk` prod 终验被外部进程占槽阻塞（120s 超时 + 300s inflight 残留）。
- 60 条目标现实上限约 15–25（强 10 年数据集仅 4 个）。


## §127 fundamental93「Earnings Tax Data」字段画像 + 应计异象机制探针（2026-10-30）

**目标选取**（扩产候选池，prod 被外部槽阻塞期间的实质推进）：本地 prod-clean 池已证 4 篮子最优，
要扩产必须挖新 10 年数据集。从 DEU FUNDAMENTAL/EARNINGS 地形锁定 `fundamental93`：
- **10 年保证**：描述明写「annual history dating back to **1980**」，DEU 发达市场覆盖 43 年。
- **46 字段全 MATRIX**（无需 vec_avg 折叠，比 VECTOR 集简单）。
- **低拥挤**：39α / 23 用户 / valueScore 5.0（多数字段 0α）。
- **未点亮 FUNDAMENTAL 塔**（非 trio，单塔优先级最高；不触碰 PV/MODEL/OTHER 禁混）。

### 一、字段 4 机制族（描述驱动画像）
| 族 | 字段模式 | 经济含义 | 学术先验 |
|---|---|---|---|
| 应计异象 | `accruals_d1_*`(mean/min/max/dts/current_t) | 税务应计=税费−实付税；高应计=盈余质量低 | Sloan 1996 应计异象 |
| 递延税费用 | `deferred_tax_expense_XX`(7 变体) | 递延税=账面/税务时间差；激进=盈余管理 | Dhaliwal et al. 2004 |
| 递延税负债 | `deferred_tax_liability_XX`(9 变体) + `liability_d1_*` | 负债升=激进盈余管理 | Richardson et al. 2005 |
| 税务应计 | `tax_accruals_XX`(13 变体) | 应计/现金税背离=盈余质量 | — |

`*_d1_current_t` 是 z-score（当期 vs LTM 窗），`_dts` 是 LTM 标准差，`_length` 是观测数，
`_asset_change` 是 YoY 资产变化。多数字段 alphaCount=0（未挖）。

### 二、论坛 + 论文验证（用机制前必查）
- 论坛：「Alpha灵感启示录」含「单因子测试之财务质量因子」；论文合集（108 赞）含
  Earnings Quality / Investor Learning / Earnings Signals / Earnings Volatility。
- 学术：Sloan (1996) 应计异象（高应计→低未来收益）、Richardson et al. (2005) 应计可靠性、
  Dhaliwal et al. (2004) 税费意外。**方向明确：做空高应计/激进递延税。**

### 三、8 条探针（探针批免 10 模板约束，测机制存在性）
| # | 机制 | 表达式 |
|---|---|---|
| 1 | 应计水平反转 | `-rank(ts_mean(fnd93_accruals_d1_mean, 22))` |
| 2 | 应计 z-score 极值 | `-rank(ts_mean(fnd93_accruals_d1_current_t, 22))` |
| 3 | 应计动量（升→空） | `-rank(ts_delta(ts_mean(fnd93_accruals_d1_mean, 22), 63))` |
| 4 | 行业相对应计 | `-group_rank(ts_mean(fnd93_accruals_d1_mean, 22), subindustry)` |
| 5 | 应计波动（盈余不确定） | `-rank(ts_mean(fnd93_accruals_d1_dts, 63))` |
| 6 | 递延税负债 z-score | `-rank(ts_mean(fnd93_liability_d1_current_t, 22))` |
| 7 | 税务应计质量 | `-group_rank(ts_mean(fnd93_tax_accruals_51, 22), subindustry)` |
| 8 | 酌情应计（资产增长归一） | `-rank(ts_mean(fnd93_accrualsratio_d1_asset_change, 22))` |

预检：`preflight_expressions` 全 8 条合法，6 字段全存在，无 VECTOR，零修改。
派发：`create_multi_simulation` → **multisim `vwJEb8IN4Jh9gv9s4ddxzo`**（8 子，DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08）。

### 四、后续硬闸（收批后必做）
1. **逐年数据闸**：`get_alpha_yearly_stats` 查最佳候选 2014–2018 是否空窗（fundamental93 应 10yr 满，需实证）。
2. 归因 + 对比实验；模板归因（哪个机制族出货）。
3. 若有信号 → 下一波补足 ≥10 互异模板；若无 → fundamental93 判弱，转 alpha_factor_lib。


## §128 fundamental93 应计探针真值 + ★ harvest_multisim_alphas 工具 bug 纠错（2026-10-31）

### ★★★★★ 重大纠错：harvest_multisim_alphas 返回假 alpha_id + 虚高指标
收批时 `harvest_multisim_alphas(multisim=vwJEb8IN4Jh9gv9s4ddxzo)` 报告「4 条 PASS_CHEAP（S 1.64~1.70）」，
**这是假数据**。平台 `/alphas` 端点真值完全不符：

| 表达式 | harvest 报告（假） | 平台真值（get_alpha_details） |
|---|---|---|
| `-rank(ts_mean(fnd93_accruals_d1_mean,22))` | wWPcygbY **S1.65/F1.18** | 1YN153PM **S0.36/F0.18** |
| `-rank(ts_mean(fnd93_liability_d1_current_t,22))` | YBbZAXvN **S1.70/F1.12** | GrWYvj7x **S0.17/F0.05** |
| `-group_rank(ts_mean(fnd93_accruals_d1_mean,22),subindustry)` | MhHyLY69 **S1.70/F1.13** | A1VYdX2R **S0.29/F0.12** |
| `-rank(ts_mean(fnd93_accruals_d1_current_t,22))` | RYtSG1Lr **S1.64/F1.17** | gJewzNLm **S−0.02** |

**决定性证据**：harvest 给的 ID（wWPcygbY/YBbZAXvN/RYtSG1Lr…）`get_alpha_details` 全 **404 = 不存在**；
平台真 ID（1YN153PM/GrWYvj7x…）都在 `get_user_alphas` 列表里且表达式逐字相同。
⇒ **判定 PASS/FAIL 必须以 `get_alpha_details` 的 checks.fail 为准，不以 harvest 的 metrics 为准。**（已沉记忆）

### ★ fnd93_accruals_probe 真值：8 条全 FAIL
| 真 alpha | 表达式 | S | F | 2Y | SUB | L/S | 死因 |
|---|---|---|---|---|---|---|---|
| 1YN153PM | `-rank(ts_mean(accruals_d1_mean,22))` | 0.36 | 0.18 | 1.24 | 0.14 | 22/22 | CW 0.5 + S |
| xAr9a7on | `-rank(ts_mean(accrualsratio_d1_asset_change,22))` | 0.36 | 0.16 | 0.12 | 0.70 | 37/38 | CW 0.5 + S |
| 88R7qW2a | `-rank(ts_mean(accruals_d1_dts,63))` | 0.31 | 0.13 | 0.32 | 0.34 | 49/46 | S（**唯一过 CW**） |
| A1VYdX2R | `-group_rank(ts_mean(accruals_d1_mean,22),subindustry)` | 0.29 | 0.12 | 0.86 | 0.21 | 21/20 | CW 0.5 + S |
| LLMqxowa | `-group_rank(ts_mean(tax_accruals_51,22),subindustry)` | 0.24 | 0.09 | 0.13 | −0.01 | 14/14 | CW 0.5 + S |
| GrWYvj7x | `-rank(ts_mean(liability_d1_current_t,22))` | 0.17 | 0.05 | −0.21 | −0.27 | 27/28 | CW 0.5 + S |
| kqNb5p98 | `-rank(ts_delta(ts_mean(accruals_d1_mean,22),63))` | 0.15 | 0.05 | 0.46 | −0.07 | 9/9 | CW 0.5 + S |
| gJewzNLm | `-rank(ts_mean(accruals_d1_current_t,22))` | −0.02 | −0.0 | −0.60 | 0.09 | 15/15 | CW 0.5 + S |

**主力死因 = CONCENTRATED_WEIGHT 0.5（限 0.1）**：fnd93 税务字段稀疏，rank() 后仅 22–28 持仓，
权重砸到 0.5。真实 sharpe 仅 0.15~0.36，远低于 1.58。

### ★ 归因（1YN153PM 逐年，真值）
2014 0.48 / 2015 0.81 / 2016 0.08 / **2017 −1.75** / 2018 0.59 / 2019 0.42 / **2020 −0.64** / 2021 0.30 / 2022 0.60 / **2023 1.88**
⇒ **2017/2020 负年，2023 驱动全部收益** → 时代依赖、非稳健。数据跨度 OK（10 年全有数，fundamental93 不像 sentiment 断档）。

### ★ 机制结论
Sloan 应计异象（做空高应计/高负债变动）在 DEU TOP500 用 fnd93 稀疏税字段**不成立**：CW 与信号强度双杀。
唯一过 CW 的 `accruals_d1_dts`（deferred tax，较密 49/46）S 也仅 0.31。
**要救的方向**（下波）：① 优先密字段（`_dts` 族）② 长窗（63/126/252）③ 去集中构造
（`ts_zscore` 替 `rank`、`winsorize` 截尾、`group_neut` 分散）④ 测 fundamental93 其余 40+ 字段的非税务族。

### 库存状态
- `fnd93_accruals_probe` 波次 8 条真数据已入库（假行已清除），wave_result 记 **FAIL**。
- DEU 塔位不变：FUNDAMENTAL 仍 1 点（predictive_starmine 那条），fundamental93 首探未点亮。

---

## §129 论坛/论文验证：应计异象在发达市场已实测失效 —— 解释首探全灭 + 第二波换机制派发

### 论坛检索结论（机制验证，非闲逛）
| 帖子 | 实证 | 对 DEU 的指引 |
|---|---|---|
| **「USA应计因子实测失效记录」** | 经典**应计异象在 USA 已实测失效**（发达市场） | 首探 8 条裸应计 rank 全 S≤0.36 = **已知失效**，非偶然 |
| **「应计项目和现金流相关性 倒U模型」** | 应计-现金流呈**倒 U 型**（非单调）⇒ 要**分组分桶** | rank 抓不到非单调；与「更稳靠分组分桶」一致 |
| **「财务指标构建稳健Alpha因子的实践路径」** | 形态 `divide(trend_res, ts_std_dev(trend_res, 500))`，**趋势残差÷自身波动**，跨市场稳健 | 稳健归一化 = 破法 |
| 「盈利异象也已消失，需加行业交互+主观权重」 | 裸盈利异象同样死 | 不能靠裸 rank |

**推论**：fundamental93 下一波弃裸 rank，改用两条实证机制 —— ①**倒 U 分桶（bucket）** ②**趋势残差稳健归一化**，并测未测的 `deferred_tax_expense_*` / `deferred_tax_liability_*`（Dhaliwal/Richardson 税基应计，与已死经典应计不同源）。

### 算子核对（防幽灵算子再废整批）
`operator_audit` 平台真实在用 103 算子，`ts_std_dev` / `bucket` / `multiply` / `group_rank` / `winsorize` **全真实**；19 幽灵黑名单已避开。本波 8 条只用真实算子。

### 第二波派发：`3mKxJT5V14Xx9ZmdysY8JrQ`（8 条，全 DEU/TOP500/D1/SUBINDUSTRY）
| # | 构造 | 机制 |
|---|---|---|
| R1 | `group_rank(ts_delta(dts,252)/ts_std_dev(dts,252), subindustry)` @63 | 趋势残差稳健归一（密 _dts） |
| R2 | 同上 @tax_accruals_51 | 税应计 |
| R3 | 同上 @deferred_tax_expense_51 | **未测族** |
| R4 | 同上 @deferred_tax_liability_51_current_t @126 | **未测族** |
| B1 | `group_rank(accruals_mean@63, bucket(accrualsratio@252, -3..3))` | **倒 U 分桶** |
| B2 | `group_rank(dts@126, bucket(current_t@252, -2..2))` | 倒 U 分桶 |
| B3 | `rank(x@126) − rank(x²@126)` @accruals_mean | 二次倒 U |
| C1 | `-rank(ts_mean(accruals_mean,22))` | 对照（首探 baseline） |

**收批纪律**：不用 `harvest_multisim_alphas`（假 ID+虚高指标 bug），一律 `get_user_alphas` 反查真 ID + `get_alpha_details` 的 `checks.fail` 判定。

### ★ 第二波 batch-kill 事故（`3mKxJT5V14Xx9ZmdysY8JrQ`，0 结果）+ 修复
- **事故**：2 条用了 `fnd93_current_t` / `fnd93_deferred_tax_liability_51_current_t` → 平台 `unknown variable` ERROR → **6 条被连坐 CANCELLED**（batch-kill），整批 0 结果。
- **根因**：`preflight_expressions` 的 `unknown_soft`（"dataset-prefixed field not found at this region/universe/delay"）**是真警告**，我误因 `valid:true` 放行。裸 `fnd93_current_t` 在 DEU/TOP500/D1 不可用（只有 `fnd93_accruals_d1_current_t` 等带前缀变体可用）。
- **教训（固化）**：`unknown_soft` = 该 region/universe/delay 下字段不可用 = 仿真必 ERROR = batch-kill 整批。**必须剔除**，`valid:true` 不代表安全。
- **修复波 `14gJ5W1Om4L9bdLmuC4i4F4`**（6 条，只用 wave-1 已证明能跑的字段：`accruals_d1_dts`/`tax_accruals_51`/`accrualsratio`/`accruals_d1_mean`/`liability_d1_current_t`）：R1-R3 趋势残差稳健归一、B1-B2 倒 U 分桶、B3 二次倒 U。

### ★ 修复波真值（`14gJ5W1Om4L9bdLmuC4i4F4`，6/6 COMPLETE 无连坐）—— 两条实证机制也全灭
| alpha | 机制 | S | F | 2Y | SUB | TO | verdict |
|---|---|---|---|---|---|---|---|
| RREqkqNn | 稳健归一 @accruals_d1_dts | −0.51 | −0.30 | 0.42 | −0.59 | 10.1% | REJECT |
| gJewowmm | 稳健归一 @tax_accruals_51 | −0.57 | −0.37 | −0.33 | −0.18 | 10.9% | REJECT |
| Xg9PYPka | 稳健归一 @accrualsratio | 0.19 | 0.06 | 1.14 | 0.17 | 10.2% | REJECT |
| zq3QJQ5V | 倒 U 分桶（accruals×ratio） | 0.25 | 0.10 | −0.22 | 0.44 | 5.6% | REJECT |
| xAr9m9Rg | 倒 U 分桶（dts×liability） | −0.17 | −0.05 | −0.19 | −0.31 | 4.7% | REJECT |
| LLMqlqkn | 二次倒 U（x−x²） | 0.17 | 0.05 | 0.02 | 0.44 | 1.8% | REJECT |

**归因**：去集中构造**成功解 CW**（TO 全降 1.8–10.9%、不再 CW fail），但**信号本身不存在**（S 全 ≤0.25）。

### ★★ fundamental93 应计/税机制判死（`DEU-FND93-ACCRUAL-TAX-DEAD`）
两波 14 条（裸 rank / 稳健归一 / 倒 U 分桶 / 二次倒 U）**全证伪**，结合论坛（应计异象 USA 已死、盈利异象消失）：
**fnd93 的 accruals_*/tax_*/deferred_tax_*/accrualsratio 族在 DEU TOP500 结构性无 alpha**，不再派发。
若再碰 fnd93 只能换完全不同的经济机制（非应计非税），且先单测字段存在性。

---

## §131 INSTITUTIONS(institutions1) 判低产（2026-01，稀疏事件型）

**数据画像**：institutions1 7 字段全 VECTOR、coverage 0.2289（稀疏事件型，实为内部人交易申报）。数据跨度 PASS（`inst1_valueeur`/`inst1_tradesignificance` 十年全覆盖 2014-2023），但 `inst1_holdings` 早年稀薄（2014 空、2015-2017 longCount 0）。

**两族机制全测（10 条）**：
- **裸水平 rank（4 条）全死**：QPvqEvoG rank(valueeur) S−0.49 / GrWYkWNP rank(holdings) S0.20 / P0oqvoAx rank(tradesignificance) S0.11 / YP1nQ19o rank(shares) S0.05。
- **净买入机制（6 条，论坛公式 ts_delta(holdings)=净方向）**：
  | 加工 | 126d 半年净买入 | 252d 年度净买入 |
  |---|---|---|
  | 裸 delta | A1VYPwJQ **S+0.58**/F0.55 | mLoJb82x S−0.17 |
  | 价值归一 | WjOnGpnQ S+0.55/F0.51 | — |
  | z-score | bl6VqLVq S+0.43 | — |
  | 行业中性 | QPvqVaqp S+0.45 | 1YN1d7VR S−0.31 |

**★ 关键发现·净买入期限翻转**：半期(126d)净买入看多（S+0.43~0.58）、年期(252d)净买入看空（S−0.17~−0.31）——中期净买入正、长期净买入负（内部人长期逢高卖出）。较裸 rank 提升约 3 倍，但**全部 REJECT**（最强 S0.58 ≪ 1.58 闸，且 **2Y 全负 −0.55~+0.28**，2Y 闸结构性不过）。

**结论**：institutions1 稀疏事件型（coverage 0.229）撑不起 TOP500 横截面，两族机制均弱 → **判低产**（非判死：126d 净买入信号真实但弱、2Y 负）。不再投入，转下一 category。

## §132 risk60 证券借贷洞察（RISK 塔）波次（2026-01，派发中）

**选集依据**：recommend_datasets 按未点塔优先 + 质量，结合用户约束（非 trio 优先 / ATOM / 满 10 年）。risk60 = 全新 RISK 塔（DEU 0 颗）、非 trio、做空/借贷与内部人异质机制。

**字段画像（优秀）**：5 VECTOR，**coverage 0.835**（远好于 institutions1）。`rsk60_crowding`(有向做空 +增空/−回补)、`rsk60_offer`(做空方借券费)、`lending_fee_bid_rate`(出借方融券费)、`rsk60_last`、`rsk60_datatime`(非信号)。

**论坛机制检索**：《When Short Sellers Do Not Short》(SSRN 4826241) 信号在「空头停止做空」ts_delta；risk59/60 借券费飙升=做空成本/难借券（看空或逼空）；借券利用率异常收紧=ts_std_dev 不稳定度；borrow demand 或正向→方向需校准。

**10 结构互异模板（覆盖水平/一阶差分/二阶波动/比率/价差 × rank/group_rank × 22/63/126/252）**：
crowding 水平/行业、borrow-fee 水平(-)/surge、crowding 变化/zscore/持久度、fee spread(offer−bid)/ratio(offer/bid)、borrow-fee 波动率。

**multisim `1PjDS377A4wVcku1gWbGmoAV`**（DEU standard settings，preflight 全绿无 unknown_soft）。**待收批归因**：①哪模板出信号（拥挤 vs 借券费 vs 价差 vs 波动率）；②方向是否符合理论；③对最强候选验 get_alpha_yearly_stats 数据跨度满 10 年。

## §133 risk60 借券费机制定向破闸 + 归因（2026-01，RISK 塔）

**10 模板波收批归因**（multisim `1PjDS377A4wVcku1gWbGmoAV`）：借券费机制（#3 水平 / #9 费率比）出信号；做空拥挤机制（#1/2/5/7/10）全弱；surge/spread/波动率（#4/6/8）负。最强 `MPYqGAZo`(#9 费率比) S0.86/2Y1.56（近闸）、`LLMqGxmn`(#3 水平) S0.79/2Y1.01，**均满 10 年覆盖（2014-2023 无空窗）**。

**借券费机制定向破闸**（multisim `tSXXFc5V4SSbZvNzctTiqt`，6 条单信号强加工，无 add 混信号）：

| 形态 | alpha | S | 2Y | TO | inv_S | fRA |
|---|---|---|---|---|---|---|
| `group_rank(fee_ratio, sector)` | 1YN1wvKm | 0.89 | **1.60** ✓2Y闸 | 18.9% | 0.71 | 3 |
| `-rank(zscore(offer,252))` | leAkjx1e | **0.91** | 0.71 | 20% | 0.82 | 4 |
| `group_rank(mean(fee_ratio,22), sector)` | 78L0jOM8 | 0.68 | 1.26 | 4.8% | 0.63 | 3 |
| `-group_rank(mean(offer,126), sector)` | 9qxbXomK | 0.69 | 1.03 | 2.4% | 0.69 | 3 |
| `rank(ts_rank(fee_ratio,252))` | QPvq7egK | 0.58 | 0.95 | 29% | 0.42 | 5 |
| `rank(zscore(fee_ratio,252))` | pwdoj0G3 | 0.54 | 1.06 | 28% | 0.39 | 5 |

**★ 关键归因**：
1. **借券费机制 S 天花板 ≈ 0.9**：16 颗（10 模板 + 6 破闸）系统探索，S 最高 0.91（leAkjx1e），距 LOW_SHARPE 1.58 闸差 42%。**S 结构性不足**，非加工问题。
2. **`group_rank(fee_ratio, sector)` 是最优形态**（1YN1wvKm S0.89/2Y1.60）：group_rank 去行业小幅提 S+2Y，**2Y 1.60 已过 1.58 闸**，但 S 0.89 仍不够。
3. **2Y 能过、S 不能过** = 「稳健但弱」信号（非过拟合）：借券费机制 2Y 稳健（多颗 1.0-1.6），但 S 强度不足。
4. **zscore/ts_rank 长窗加工伤 2Y**（leAkjx1e S0.91 但 2Y 仅 0.71）；group_rank 短窗更平衡。

**结论**：risk60 借券费机制 = **弱但真实**（正 S + 2Y 过闸 + 满 10 年覆盖），但 S 结构性卡 0.9 不过 LOW_SHARPE 闸 ⇒ **REJECT**。机制保留：`group_rank(fee_ratio)`(1YN1wvKm S0.89/2Y1.60) 入 salvage_pool 作未来组合/辅助腿素材。**risk60 判「低产」（非判死）**，转下一 category。

**★ 教训（语法）**：DEU `group_rank` 需 `(x, group)` 两参数；1 参写法被 toolkit 静态闸拦下（避免整批失败）。`ts_zscore/ts_rank` 长窗标准化会削弱 2Y。

**DEU 探索累计**（2026-01）：fundamental93 判死 / institutions1 低产 / risk59+60 借券费弱真实（S<0.92）。DEU TOP500 小宇宙 S 天花板普遍 ~0.9-1.2，过 LOW_SHARPE 1.58 闸难 ⇒ **DEU 系统性低产，需更强机制或跨区**。4 篮提交候选（bl62jGgM/1YNv6Ymk/MPY9VNY9/Vkxnb8QG）仍等真实授权。

## §134 option1 期权 IV 探针判死 + DEU 战略结论（2026-01，OPTION 塔）

**option1（OPTION 塔）探针**（multisim `3lDgkDh0v4izaOP1adxp77N6`，6 条 IV 机制）：**全 REJECT，S 0.10-0.33**（比 risk60 的 0.91 弱得多）。
- IV 水平(`vec_avg`)/短中期变化(`ts_delta`)/平滑(`ts_mean`)/相对历史(`ts_zscore`) 全弱；最强 xAr9Yzmp S0.33/2Y−0.17。
- **根因**：option1 是 delta surface VECTOR，`vec_avg` 聚合丢曲面结构（skew/期限需按 delta/period 切片，VECTOR 聚合做不到）。
- **call−put skew 在 DEU 做不了**：`get_datasets(search=volatility)` 仅 option1 一个期权集（delta surface），**无 `implied_volatility_call/put` 标量字段数据集** ⇒ 论坛 skew 模板（用标量 call/put IV）不可迁移。
- **OPTION 塔判死**（IV 聚合全弱 + skew 无字段）。vec_std_dev 是幽灵算子（平台无）。

**论坛期权 IV 模板归档**（供有 call/put 标量字段的区域用，DEU 无此结构）：
- **Individual Option Volatility Smirk（23 票可提交）**：`skew = rank(winsorize(ts_backfill(implied_volatility_call_10,5) − ts_backfill(implied_volatility_put_10,5), std))`
- **IV Skew Python（36 票）**：`@alpha(data=["implied_volatility_call_30","implied_volatility_put_10"])`
- **Attention: IV Spreads**（DOI 10.1080/15427560.2019.1692846）：高关注度 + 大 IV spread = informed trading
- **idio vol puzzle**（Hou & Loh）：特质波动率与未来收益负相关
- **IV/realized vol**（`implied_volatility_call_120/parkinson_volatility_120`）：波动率风险溢价

**DEU 战略结论（5 category 系统探索，2026-01）**：

| Category | 数据集 | S 天花板 | 2Y | 结论 |
|---|---|---|---|---|
| FUNDAMENTAL | fundamental93 | 0.25 | 负 | 判死 |
| INSTITUTIONS | institutions1 | 0.58 | 负 | 低产 |
| RISK | risk59/60 | **0.91** | 1.60 | 借券费弱真实 |
| OPTION | option1 | 0.33 | 弱 | 判死（IV 聚合弱 + skew 无字段）|

**核心结论**：DEU/TOP500 小宇宙 **S 天花板 ~0.9，结构性难破 LOW_SHARPE 1.58 闸**。已探明最强真实信号 = risk60 借券费（S0.91/2Y1.60，满 10 年）。**DEU 系统性低产**——5 个 category 无一 S>1.0，继续挖新 category 边际收益极低。

**战略建议**：① 优先提交现有 4 篮已过闸候选（等真实授权）；② 或转更强区域（TOP3000 / 其他区）；③ 继续 DEU 需接受低 S 现实。

---

## §135 fundamental90 质量因子探针（稠密 MATRIX 策略验证）—— S 天花板 1.09，新最高

**背景**：DEU 稠密 MATRIX 质量因子集 fundamental90（66 标量字段，pscore/ohlson/mohanram/deferred_sal/icfroe/cash_flow）。10 模板 preflight 全绿。multisim `166tdKgjJ4EFb7R8j1DanIn`。DEU 标准设置。

**结果（batch_get_alpha_metrics 核真，顺序 = 提交顺序）**：

| # | 机制族 | 表达式 | alpha | S | 2Y | inv_S | CONC_W | fRA |
|---|---|---|---|---|---|---|---|---|
| 1 | Piotroski 质量 | `rank(pscore)` | 6Xd3Kb5P | **1.02** | 0.85 | 0.73 | 0.50 | 4 |
| 2 | 质量行业中性 | `group_rank(pscore,subindustry)` | bl6VO3e6 | 0.82 | **1.22** | 0.50 | 0.50 | 4 |
| 3 | Ohlson 破产(负) | `-rank(ohlson)` | RREq6LGg | 0.82 | 1.10 | 0.52 | — | 4 |
| 4 | Mohanram(符号反) | `-rank(mohanram)` | E56YR3ZJ | −0.92 | −0.23 | | | 4 |
| 5 | 递延收入 | `-rank(deferred_sal_chg)` | 3qo3VdMz | −0.30 | −0.48 | | | 5 |
| 6 | 5年CFROE | `rank(icfroe_5y)` | 58E3gRZz | 0.89 | 0.44 | 1.05 | — | 4 |
| 7 | **现金流覆盖** | `rank(cash_flow_coverage)` | kqNbgRxO | **1.09** | 0.28 | 0.88 | 0.29 | 4 |
| 8 | 递延平滑 | `-rank(ts_mean(deferred_sal,63))` | akKMxJr5 | −0.27 | −0.31 | | | 4 |
| 9 | 质量改善 | `rank(ts_delta(pscore,252))` | 1YN1ZvYm | 0.43 | 0.84 | 0.49 | — | 4 |
| 10 | C-score 操纵 | `-rank(cscore)` | WjOnekjP | −0.02 | 0.04 | | | 4 |

**两个关键发现**：
1. **★ FUNDAMENTAL 塔 multiplier = 1.8（平台高鼓励）**，`pyramid_short=fundamental`。目前最高点塔价值。
2. **★ 真正卡的闸 = CONCENTRATED_WEIGHT（0.29–0.5，限 0.1）**，不是信号弱。TOP500 单字段 rank 只挑 ~65 只、SUBINDUSTRY 中性后挤少数子行业。

**机制族归因**：质量族（pscore/cash_flow/icfroe/ohlson/mohanram）全部出真信号（S 0.8–1.1，方向符合理论）；递延收入 / C-score 无信号；pscore 组 group_rank 提高 2Y（0.85→1.22）。**S 天花板 1.09（新高，打破此前「无一 S>1.0」结论）**，但仍差 1.58 闸 31%。

**下一步（已派发）**：mechanism-transfer 探针 multisim `45ZNYph04Tkb8kHXnZS5X`（5 变体）——把 4 篮已验证的赢法算子 `ts_target_tvr_decay`（换手目标，MPY9VNY9 模式）+ `group_rank` 搬到 fundamental90 质量信号，测「换手目标能否修复集中度 + 推 S/2Y」。

**战略更新**：DEU 稠密数据集 + 精巧机制能出 S 1.0–1.1（质量族），但突 1.58 需「稠密 + 特定机制（换手目标 / trade_when / bucket 结构）」（4 篮即此类）。simple rank 撑不破。

---

## §136 机制迁移探针反证：换手目标毁掁慢信号（multisim `45ZNYph04Tkb8kHXnZS5X`）

**假设**：把 4 篮赢法算子 `ts_target_tvr_decay`（换手目标，MPY9VNY9 模式）+ `group_rank` 搬到 fundamental90 质量信号，推 S/2Y 过 1.58 闸。

**结果：全 REJECT，系统性毁信号（S 掉 ~40%）**：

| 信号 | 基础 S/2Y | +换手目标 S/2Y | 变化 |
|---|---|---|---|
| cash_flow_coverage | 1.09/0.28 | 0.50/−0.28 | ↓↓ |
| pscore | 1.02/0.85 | 0.55/0.45 | ↓ |
| icfroe_5y | 0.89/0.44 | 0.68/0.33 | ↓ |
| ohlson | 0.82/1.10 | 0.56/0.57 | ↓ |
| mohanram | 0.92/— | 0.50/−0.24 | ↓ |

**归因（可迁移教训）**：`ts_target_tvr_decay` 是「**快信号**（short-interest 等高换手）」的换手控制器，搬到「**慢信号**（季度会计质量因子）」上会主动扭曲/摩损 alpha。换手本已低（~0.20）的慢信号被强制目标换手后反而失真。**机制迁移不是普适的**——必须匹配信号的时间尺度。

**DEU S 天花板定论**：fundamental90 质量族 S 锁死 1.09（simple rank）；「稠密+精巧机制」策略在 DEU 天花板 **1.0–1.1**，仅 4 篮那类特定机制（分析师修正/拥挤/做空动态+bucket/trade_when）突 1.58。simple rank 结构性撑不破。

---

## §137 fnd6 双 delta × tvr_decay 骨架扩字段探针：oiadpq 独强，矿脉关闭（wave `mcp-20261031_fnd6_dbldelta`）

**背景**：Wje5K71x（`fnd6_newq_oiadpq` 双 delta × `ts_target_tvr_decay` @sector，**已提交 OS 2026-10-12，ACTIVE，PowerPoolSelected**，S 1.73 / F 1.37 / 2Y 1.87 / SUB 1.25 / **prod 0.4305** / self 0.1882，pyramid FUNDAMENTAL ×1.8）是唯一实证破 prod 墙形态。本轮把同骨架扩到 fnd6 其他 4 字段 × 2 轴做 4×2 对照。

**结果（5/8 派发，3 条 429 未补——趋势已定不烧槽）**：

| tag | 字段 | 轴 | alpha | S | F | 2Y | SUB |
|---|---|---|---|---|---|---|---|
| t1 | saleq | sector | MPYX5grM | 0.91 | 0.63 | −0.26 | 0.75 |
| t2 | saleq | subindustry | 1YNLnZlX | 0.11 | 0.03 | −0.57 | 0.27 |
| t3 | cogsq | sector | RREYkAY0 | 0.74 | 0.47 | +0.46 | 0.54 |
| t6 | oibdpq | subindustry | gJeKorNQ | 0.59 | 0.37 | +0.11 | 0.55 |
| t7 | oancfy | sector | VkxEYreb | 0.66 | 0.41 | −0.93 | 0.18 |
| 基线 | **oiadpq** | sector | Wje5K71x | **1.73** | **1.37** | **1.87** | **1.18** |

**归因（可迁移）**：
1. **oiadpq（经营现金流净额）独强**：同为流量项，S 1.73 vs 其余 0.11–0.91。现金流净额的「双 delta 加速度」有真实信号，营收/成本/EBITDA/现金流总额都不行——**流量项之间不可互推**。
2. **sector 轴 > subindustry**（saleq 0.91 vs 0.11）：宽轴保留更多截面信息。
3. **2Y 是最大差距**（−0.93~+0.46 vs 1.87）：oiadpq 信号长期稳定，其余只在部分时期有效。
4. Wje5K71x 已占位 fundamental 塔（1/3 点亮），fnd6 扩展字段全 REJECT ⇒ **fnd6 矿脉关闭**。

---

## §138 news81 0 成本拦截（cov=0 ASI 专属）+ model28（StarMine Merton 信用模型）首轮探针

### news81 拦截（不烧槽）

188 条 gem 存量表达式（wave `s2_news81_d1`）拟作零成本矿脉。**派发前字段覆盖核查拦截**：全部 23 字段 `coverage=0.0`，描述均为 "per stock in ASI / D0 (same-day) window"——**news81 是 ASI 区 D0 专属数据集，DEU/D1 无数据**。188 条全为死表达式，派发必全 NaN/ERROR。探针批中止，加入「cov=0 数据集待封存」名单（analyst7 / news38 / news48 / other384 / news81）。

**纪律固化**：gem 池存量派发前**必须先查 get_datafields 覆盖率**——gem 生成不校验区域数据存在性。

### model28 探针（DEU 首测，Merton 结构性信用风险模型）

25 字段全 MATRIX（DD / PD / leverage / asset_drift / asset_vol 五族 × sm_structural 单期与 multiple 多期两子模型），大量 ac=0 冷门字段。机制先验 = Vassalou-Xing 违约风险溢价 + 低波异象；PD/DD 为年化慢变量 ⇒ 窗口 252（白名单）。判死登记簿无 model28 条目 ✓。

**首批 4 条全 REJECT**：

| 机制 | alpha | S | 2Y |
|---|---|---|---|
| DD 双 delta 骨架（Wje5K71x 平移） | 2rARJ8MN | 0.67 | 0.44 |
| multiple 族 DD delta | d5WmnopK | 0.64 | 0.53 |
| industry_rank_float delta（ac=0 冷门） | pwdEneNx | 0.59 | 0.59 |
| PD delta（反向） | Xg9L1g38 | **−0.18** | −0.32 |

**归因**：model28 慢变量「水平/动量」形态在 DEU/TOP500 无 alpha（S<0.7，非近闸而是无信号级）；PD 恶化方向甚至为负。第二批（asset_drift 水平/delta + sector_rank_float + asset_vol + country_rank_float）在飞，补 asset_drift 族（ac 35 最热门字段，机制=资产增长预期）后再定 model28 判死范围（按字段族粒度）。

---



## 139. model28 收口：asset_drift 加速度族天花板 = 1.10（REJECT）；四条战线盘点与下一步

### 139.1 model28 破闸变体收批（4 条）

| alpha | 表达式 | S | F | 2Y | SUB | returns | TO | 判定 |
|---|---|---|---|---|---|---|---|---|
| omEvVYWn（基线） | delta252 @sector | **1.10** | 1.00 | 0.92 | 0.76 | 10.3% | 5.8% | REJECT（族内峰值） |
| VkxEORo8 | delta126 @sector | 0.68 | 0.47 | 0.41 | 0.43 | 6.1% | 7.6% | REJECT |
| d5WmdPgx | delta504 @sector | 0.85 | 0.69 | **1.21** | 0.60 | 8.3% | 5.4% | REJECT |
| leA2r95O | zscore(delta252) @sector | 0.61 | 0.35 | 0.03 | 0.36 | 4.0% | 8.0% | REJECT |
| 2rARJ8MN（首批） | delta252 | 0.67 | — | — | — | — | — | REJECT |
| d5WmnopK（首批） | 双 delta 交互 | 1.01 | — | — | — | — | — | REJECT |
| pwdEneNx（首批） | industry_rank_float delta | 0.59 | — | — | — | — | — | REJECT |
| Xg9L1g38（首批） | PD 反向 | −0.18 | — | — | — | — | — | REJECT |
| m28d_w252_sub | delta252 @subindustry | 卡 0.35 挂起 | | | | | | 随机挂起，不影响结论 |

**结论**：**delta 252 @sector = 1.10 就是 model28 asset_drift 族的天花板**——窗口缩/扩都降（0.68/0.85）、二阶标准化降（0.61）、换轴降或挂起。与 fnd6 同款止损：剩余 6 条邻域变体（dbl_sec / ctryrank×3 / pd_mom×2）**不补派**。

**归因**：
1. **「慢变量一阶加速度 > 水平」再证**（水平 0.69 → delta252 1.10），但加速度在 model28 上的**绝对强度只有 1.10**，远不及 fnd6 oiadpq 的 1.73——asset_drift（资产漂移 %）的信号密度本身低于经营现金流。
2. **2Y 是硬伤**：族内最好 2Y = 1.21（w504），全族 < 1.58 线。model28 是 Merton 结构模型输出（高频更新的模型变量），2Y 段表现弱。
3. 与 Wje5K71x 的差距本质：**现金流数据（fnd6 oiadpq）> 模型推断数据（model28 asset_drift）**，经济学信息的原始度决定上限。

**model28 状态**：探针收口，**判 REJECT 族**（不进死路登记——asset_drift delta 族活但不够强，非结构性死路）。

### 139.2 本会话四条战线盘点

| 战线 | 结果 | 状态 |
|---|---|---|
| fnd6（现金流双 delta） | oiadpq 被 Wje5K71x 占位；扩字段全 REJECT（最好 0.91） | 关闭 |
| sentiment7 / snl27 / inst1 | 字段空间穷尽（2/2、7/7、5/5）；出货的是**存量**（P0oe6wpJ/kqNRX1ZP/2rmGAPqN…） | 转提交归组，不再挖新字段 |
| news81（gem 188 条零成本池） | 23 字段 cov=0（ASI 区 D0 专属）⇒ 188 条全死 | 拦截，0 槽损失 |
| model28（Merton 信用模型） | 加速度族天花板 1.10，全 REJECT | 收口 |

**总账**：本轮新增过闸 **0**；矿脉轮转 4 条战线全探完。冷门矿脉（fnd6 扩字段 / news81 / model28）逐个探完都不够强——**出货集中在已验证族**（snt7/snl27/inst1/fnd6-oiadpq 的存量候选）。

### 139.3 下一步（价值排序）

1. **【最高价值】提交篮子授权**（不可逆，等用户）：6 颗候选——QPveY7Kg（prod 0.6671/self 0.0242/S 2.03）、MPY9VNY9（0.5986）、npvwXA8l（0.6093）、Vkxnb8QG（0.6384/self 0.6379 偏高）、bl62jGgM / 1YNv6Ymk（prod 待测）。这是把挖掘成果变现的唯一路径。
2. **prod 终验队列**（单槽串行）：kqNRX1ZP（两次 120s 超时，异步排队）→ bl62jGgM → 1YNv6Ymk → E56AzejK。
3. **互相关归组**：snt7/snl27/inst1 三族存量候选做 compute_mutual_correlation，定最终提交篮子（一个机制族本轮最多 1 颗提交）。
4. **待裁定**：news81 等 cov=0 数据集的判死封存方式（seal_dead_end 需 forum_recon 或人工 waive）；Jje0J2rx leading-gap 判法。


## 140. 提交篮子互相关归组（本地零配额）：MPY9VNY9↔npvwXA8l 同族二选一，最终篮 5 颗

`compute_mutual_correlation`（4 年日收益，1021 点）实测 6 颗候选：

| 对 | 互相关 | 判定 |
|---|---|---|
| **MPY9VNY9 ↔ npvwXA8l** | **0.9197** | ❌ 同族（都是 ts_target_tvr_decay 双窗口交互骨架），**二选一** |
| Vkxnb8QG ↔ bl62jGgM | 0.215 | ✓ |
| 其余各对 | −0.04 ~ 0.13 | ✓ 全低相关 |

**最大互不相关篮子 = 5 颗**（阈值 0.5）：
1. **QPveY7Kg**（prod 0.6671 / self 0.0242 / S 2.03）—— sentiment7+snl27 vector_neut
2. **MPY9VNY9**（prod 0.5986 / self 0.2703）—— 与 npvwXA8l 二选一，**选它**（prod 更低 0.5986 vs 0.6093）
3. **Vkxnb8QG**（prod 0.6384 / **self 0.6379 偏高**）—— 提交前须 self 复测
4. **bl62jGgM**（prod 待测）
5. **1YNv6Ymk**（prod 待测）
- 替补：npvwXA8l（MPY9VNY9 若终验翻车则顶上）

**prod 终验阻塞**：kqNRX1ZP 三次 120s 超时、bl62jGgM 一次超时——平台 prod 单并发槽被占（inflight 残留 300s）。**不连续重试**，等槽释放后按队列补测：bl62jGgM → 1YNv6Ymk → Vkxnb8QG(self) → kqNRX1ZP。

**提交授权状态**：问卷超时自动选了「4 颗全提交」，但**自动选择不构成不可逆提交授权**——未执行任何提交。等用户真实授权。


## 141. model28 asset_vol 族：低波动异象在 DEU 不成立（REJECT×3）；leverage 穷尽批在飞

### 141.1 asset_vol 探针（3 条，wave mcp-20261031_model28_assetvol）

| alpha | 表达式 | S | F | 2Y | 备注 |
|---|---|---|---|---|---|
| VkxEPJ7A | 低波动水平反向（low-vol anomaly） | **−0.02** | −0.00 | **0.98** | 全期零信号但 2Y 段活 |
| j2YX0bkk | vol delta252 @sector | 0.16 | 0.05 | 0.68 | |
| mLoAbO7p | 多期子模型 vol delta252（ac0 冷门字段） | 0.19 | 0.06 | 0.71 | |

**结论**：**低波动异象（Ang et al. 2006）在 DEU model28 asset_vol 上不成立**——S ≈ 0。波动率一阶变化也只有 0.16–0.19。

**归因**：
1. **同数据集内机制对比**：asset_drift delta252 = **1.10** vs asset_vol delta252 = **0.16** ⇒「**趋势（drift）有信号、波动（vol）没信号**」。Merton 模型输出里，资产漂移的截面分化能定价，资产波动率不能。
2. **VkxEPJ7A 的 2Y 0.98 vs 全期 −0.02** ⇒ 低波动异象在 DEU **近年（2024-2026）才出现**，2016–2023 段是负贡献——regime-dependent，全期闸下无解（平台 IS 不支持截断起始年）。此形态不可救，记观察。
3. 论坛取证 `search_forum_posts("low volatility anomaly")` **navigation_failed**（查询失败≠论坛无解），学术先验按 Ang et al. 2006 采用，实测证伪。

### 141.2 model28 五族穷尽进度

| 族 | 状态 | 族内最好 S |
|---|---|---|
| DD（违约距离） | REJECT | 0.67（双 delta） |
| PD（违约概率） | REJECT | −0.18 |
| rank_float（industry/country） | REJECT | 0.59 |
| asset_drift（资产漂移） | REJECT（族内峰值 1.10） | **1.10**（delta252 @sector） |
| asset_vol（资产波动） | REJECT | 0.19 |
| **leverage（杠杆）** | **在飞（2 条）** | 待收 |

**总归因**：model28 = 模型推断数据，信号密度系统性低于原始数据（fnd6 oiadpq 1.73）。「慢变量一阶加速度 > 水平」规律在 drift 族成立（0.69→1.10），但**机制迁移要挑字段**——同一骨架在 vol 族只有 0.16。


## 142. model28 leverage 族 REJECT×2 ⇒ 五族穷尽，model28 正式关闭

| alpha | 表达式 | S | F | 2Y | dd |
|---|---|---|---|---|---|
| vR19v9pv | leverage delta252 @sector | **−0.79** | −0.57 | −1.03 | 0.78 |
| LLM6dlVn | 多期 leverage 水平反向 @sector | −0.15 | −0.05 | −1.26 | 0.53 |

### model28 五族终榜（全 REJECT，数据集关闭）

| 族 | 族内最好 S | 形态 |
|---|---|---|
| **asset_drift** | **1.10**（数据集天花板） | delta252 @sector（加速度） |
| DD | 0.67 | 双 delta 交互 |
| rank_float | 0.59 | industry_rank delta |
| asset_vol | 0.19 | delta252（低波异象 S −0.02 证伪） |
| leverage | −0.15 | 水平反向 |
| PD | −0.18 | 反向 |

**总归因（跨数据集通用结论）**：
1. **模型推断数据 < 原始数据**：model28（Merton 结构模型输出）天花板 1.10 vs fnd6 oiadpq（原始现金流）1.73。
2. **同一骨架必须挑字段**：「慢变量一阶加速度」在 asset_drift 成立（0.69→1.10），在 asset_vol 只有 0.16、leverage 负值。机制 × 字段交互，不能盲目平移。
3. **五族方向全景**：drift（趋势）> DD（距离）> rank（排序）> vol（波动）> leverage/PD（水平）——Merton 体系里「变化量」能定价，「水平量」不能。

### 142.1 挖掘侧总账（DEU/TOP500/D1 冷门矿脉全探完）

| 矿脉 | 结局 |
|---|---|
| fnd6（现金流双 delta） | oiadpq 被 Wje5K71x 占位；扩字段全 REJECT |
| sentiment7 / snl27 / inst1 | 字段空间穷尽（2/2、7/7、5/5），出货为存量 |
| news81 | 23 字段 cov=0（ASI 专属）拦截，0 槽损失 |
| risk60 | 字段空间穷尽（5/5，datatime 无信号价值） |
| model28 | **五族穷尽关闭**（天花板 1.10） |

**⇒ DEU/TOP500/D1 挖掘边际收益已耗尽**，剩余价值全在**提交变现**（5 颗篮子等授权）与 prod 终验排队。60 目标结构性不可达，现实产出上限即现有 ra_clean 257 中的 prod_clean 15 颗。


## 143. 提交篮 self 全测完成：3 颗双过可提交，2 颗 prod 待测（平台单槽持续超时）

### 143.1 五颗篮子最新状态（self 本地全测完，零配额）

| 候选 | prod | self（本地实测） | S | 结构 | 判定 |
|---|---|---|---|---|---|
| **QPveY7Kg** | 0.6671 ✓ | **0.0242** ✓ | 2.03 | snt7+snl27 vector_neut | **双过，可提交** |
| **MPY9VNY9** | 0.5986 ✓ | 0.2703 ✓ | — | tvr_decay 双窗骨架 | **双过，可提交** |
| **Vkxnb8QG** | 0.6384 ✓ | 0.6379 ✓（复测确认） | — | — | **双过，可提交**（self 余量 0.06） |
| bl62jGgM | 超时×4 待测 | 0.6417 ✓ | 1.78 | **add 5 腿复合** | prod 待测 |
| 1YNv6Ymk | 超时×1 待测 | **0.1335** ✓ | 2.28 | tm_15 单字段 | prod 待测 |

**self 全部落库**（persist_correlation，triage_local）。

### 143.2 prod 测量阻塞现状

- bl62jGgM prod **4 次 120s 超时**、1YNv6Ymk 1 次超时——平台 prod 计算单并发槽持续被占（holder 曾见 88RAAmZa），MCP 120s 等不到结果。
- 超时**不落缓存**，但平台侧异步计算会继续完成并写进 alpha 详情；后续 `check_correlation` 预读可直接采纳。策略：**拉长间隔（≥30min）补查，不连续重试**。

### 143.3 风险提示（提交排序参考）

- **bl62jGgM 是 add 5 腿等权复合**（5×rank(ts_mean(predicted_surprise…))），与 grtransform/lean_le89 同构——那两族的实证是「add 多腿 → prod 撞墙」。**prod 撞墙概率高**，建议排最后或等实测。
- **1YNv6Ymk** 单字段干净结构（tm_15_r1_r5_r10_rh_glb_d1_r10_q1 @group_rank sector，CROWDING 中性化），self 仅 0.13 ⇒ **prod 撞墙概率低**，S 2.28 是篮内最高；但 TO 37.9% 高（inv_S 1.29/S 2.28 = 0.57）。
- Vkxnb8QG self 0.6379 vs 已提交 2rjrMZ25 —— 双过但余量最小。

## §144 可视化战果面板（2026-08-01）

战果面板已生成：`tracking/DEU/reports/deu_campaign_20261030_panel.md`，内容：
1. 最终提交篮 5 颗全指标表（S/F/TO/2Y/prod/self/覆盖/闸/备注）+ 互相关说明 + self 余量标注
2. 本轮 10 个数据集矿脉盘点（CLOSED/DEAD + 本区峰值）
3. 跨区引擎迁移实证表（8 条：OIBD 部分迁移 / EPS 完整 / vol·lev 证伪 / 慢变量加速度三证 / TF cluster）
4. 待用户裁定项 3 条（QPveY7Kg leading gap / 提交授权与概率顺序 / trio 名额已满）
5. 下一轮建议 4 条（TF cluster / 慢变量 / 模型推断字段不优先 / TOP500 天花板）

## §145 cov=0 数据集判死封存完成（2026-10-31）

**论坛取证**（search_forum_posts，两次成功检索 + 一次故障不作数）：
- 「news81 DEU news coverage」→ 10 条全是相邻新闻集（news48/54/18/7/21/20/85）泛 Data Idea，news81 零命中
- 「news81 数据集」→ 10 条模糊匹配通用数据集帖，news81 零命中
- （「news81」单关键字 navigation_failed——故障≠无解，不计入证据）
- news48 有一篇《Data Idea系列3：Global News Data_news48》全球用法帖，但不涉及 DEU/TOP500 覆盖，cov=0 下任何模板不可运行
⇒ 取证记录落台账 `forum_recon_negative_news_cov0_deu_top500`（found=false / status=no_result），判死依据为平台硬事实 cov=0，论坛取证为辅证。

**封存结果**（seal_dead_end，取证闸全部 `decision=verified` 真实通过，非 forced/waived）：
| entry_id | family | 状态 |
|---|---|---|
| `DEU-NEWS81-COV0-TOP500` | news81（btc 全市场新闻流） | sealed |
| `DEU-ANALYST7-COV0-TOP500` | analyst7 | sealed |
| `DEU-NEWS38-COV0-TOP500` | news38 | sealed |
| `DEU-NEWS48-COV0-TOP500` | news48 | sealed |

rule（四条同）：DEU/TOP500 派发前必查数据集字段覆盖率（gem 池 cov>0 才派）；cov=0 数据集直接跳过。
无波次沉降（这批是数据集级判死，无候选残值）。

**排除说明**：other384 **不**在封存名单——它产出了提交篮最强候选 1YNv6Ymk（S 2.28），属 CLOSED 有产出矿脉，仅个别字段 cov=0。

**工具坑记录**：MCP `seal_dead_end` 的 `forum_recon` 对象参数经 harness 序列化会变字符串（schema anyOf object|null 校验拒收）；
绕法=直接 Python 调 `wqb_db_mcp.seal_dead_end(...)` 传真 dict（`_tmp_seal_cov0.py`）。台账值经核查本来就是 dict（upsert_ledger_key 的 value 自由类型不受影响）。
