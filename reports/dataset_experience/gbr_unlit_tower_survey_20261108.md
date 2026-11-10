# GBR 未点亮塔逐 category 字段画像与判死台账

范围：2026-11-08 战役。设置档 `GBR / TOP700 / D1 / SUBINDUSTRY / decay 4 / truncation 0.08 / maxTrade OFF`，
回测区间 `2014-01-01 ~ 2023-12-31`。本文件只记录**本轮实测**，不外推为数据集全历史结论。
命名规则沿用目录既有 `<region小写>_<主题>_<类型>_<日期>.md`（本文件为跨数据集 survey 型，参照
`gbr_other_tower_survey_20261030.md`）。

## 0. 塔点亮基线（`get_pyramid_alphas` 实读，GBR D1）

| 塔 | 已点亮数 | 状态 |
|---|---:|---|
| model | 6 | ✱ 已亮 |
| pv | 4 | ✱ 已亮 |
| news | 3 | ✱ 已亮 |
| analyst | 3 | ✱ 已亮 |
| fundamental | 3 | ✱ 已亮 |
| shortinterest | 3 | ✱ 已亮 |
| **institutions** | **0** | 目标塔（本战役主攻） |
| other | 1 | 未亮 |
| sentiment / risk / earnings / macro / socialmedia / insiders / option / imbalance | 0 | 未亮 |

## 1. institutions（5 数据集，66 字段全量）

| 数据集 | cov | 字段 | aC/uC | 裁定 |
|---|---:|---:|---:|---|
| **fund_holdings_panel** | 0.9099 | 18 | 294/173 | 选定主攻（唯一日频账户级）→ **31 条探针全灭，判死** |
| institutions6 | 1.0 | 11 | 942/423 | 次选（季度近静态，本区全族 DEAD/DEAD_STATIC） |
| institutions1 | 0.3118 | 7 | 52/34 | 排除：cov<0.6 |
| institutions4 | 0.39 | 6 | 47/38 | 排除：cov<0.6 |
| institutions25 | 0.0 | 24 | 90/54 | 排除：GBR TOP700 coverage=0 |

完整 18 字段画像与 31 条探针明细见 [gbr_institutions_campain.md](gbr_institutions_campain.md)。

**归因**：`stable_boundary_trade_count_21d` 是唯一真信号字段（S 0.80–0.94）；金额类/集中度类/conviction
计数全部 S≈0 至负；分组轴 sector > industry > subindustry；`vec_avg ≈ vec_max ≈ vec_sum`，`vec_count` 无效。
**干净最优 `ts_decay_linear(group_zscore(vec_avg(stable_boundary_trade_count_21d), sector), 20)`
（gJeVALAK）S 0.94 / F 0.31 / TO 0.40 / 2Y 1.44** ⇒ 距 S 闸 0.64、F 闸 0.69。

---

## 2. sentiment（3 数据集）

| 数据集 | cov | 字段 | aC/uC | 裁定 |
|---|---:|---:|---:|---|
| **sentiment27** | **0.8003** | 18 | 834/347 | ✅ 本区唯一高覆盖情绪集，本轮主攻 |
| sentiment33 | 0.3218 | 255 | 209/102 | 排除：cov<0.6 |
| sentiment7 | 0.5784 | 3 | 96/58 | 排除：字段过少（Wikipedia 浏览量） |

### 2.1 sentiment27（Website Popularity Rankings）完整字段画像

**类型分布**：4 个 `SYMBOL`（日期/标记，不可作信号）+ 14 个 `VECTOR`（数值，须 `vec_*` 聚合）。

| 字段 | 类型 | 覆盖率 | uC | aC | 含义 | alpha 适用性 |
|---|---|---:|---:|---:|---|---|
| `snl27_avgranking` | VECTOR | 0.7976 | 42 | 63 | 发行人所辖域名 Tranco 排名算术均值（越低越流行） | ★ 主信号（关注度水平/变化） |
| `snl27_topranking` | VECTOR | 0.7976 | 57 | 84 | 名下最佳（最低）排名 | ★ 头部注意力 |
| `snl27_relpopularity1` | VECTOR | 0.7976 | 166 | 237 | 复合相对流行度 α=1（越高=关注越广） | ★ 最热字段，拥挤度最高 |
| `snl27_relpopularity08` | VECTOR | 0.7976 | 99 | 143 | 复合相对流行度 α=0.8 | ○ 与 α=1 同族 |
| `snl27_top50pctranking` | VECTOR | 0.7976 | 19 | 24 | 域名排名分布中位数（越低越好） | ○ 分位截断 |
| `snl27_top50pctrankingavg` | VECTOR | 0.7976 | 24 | 33 | 前 50% 域名内的平均排名 | ○ 半分布中心 |
| `snl27_top75pctranking` | VECTOR | 0.7976 | 32 | 42 | 75 分位排名截断 | ◇ 尾部刻画 |
| `snl27_top75pctrankingavg` | VECTOR | 0.7976 | 14 | 17 | 前 75% 域名内平均排名 | ◇ 冷门 |
| `snl27_skewness` | VECTOR | 0.7976 | 36 | 44 | 域名排名分布偏度（非对称/集中） | ○ 分布形态 |
| `snl27_kurtosis` | VECTOR | 0.7976 | 24 | 46 | 排名分布超额峰度（重尾/极端） | ○ 分布形态 |
| `snl27_totaldomains` | VECTOR | 0.7976 | 78 | 106 | 发行人关联网域总数（去重计数） | ★ 网域广度=业务扩张代理 |
| `snl27_totalcountrydomains` | VECTOR | 0.7976 | 33 | 41 | 带 ccTLD 的域名数（国际化广度） | ○ 全球化程度 |
| `snt27_rank` | VECTOR | 0.814 | 49 | 55 | 单域名 Tranco 日排名（1=最流行） | ○ 原始排名（重尾） |
| `snl27_wq_pit` | VECTOR | 0.7976 | 21 | 27 | 内部 PIT 对齐标记 | ✗ 非分析量 |
| `aggregate_collection_timestamp` | SYMBOL | 0.7976 | 1 | 5 | 聚合数据采集日 | ✗ 不可作信号 |
| `aggregate_reference_date` | SYMBOL | 0.7976 | 1 | 8 | 聚合数据生效期 | ✗ |
| `ranking_reference_date` | SYMBOL | 0.814 | 4 | 5 | 排名数据生效期 | ✗ |
| `source_collection_timestamp` | SYMBOL | 0.814 | 0 | 0 | 源采集日（零使用） | ✗ |

**更新频率**：日频（reference_date 每日一行）；底层 Tranco 排名按日发布，网格化后为 D1 日频面板。
**分布特征**：排名类为**幂律右偏重尾**（1 ~ 百万级），必须 `rank`/`ts_zscore` 无量纲化，禁止直接线性使用；
`*_totaldomains` 为稀疏小整数（多数发行人数个域名）；偏度/峰度为有界形状参数。
**可用性**：全部 14 个数值字段为 VECTOR ⇒ 必须 `vec_avg / vec_max / vec_sum` 折叠；`vec_count` 仅返回向量长度，无信号。
**潜在 alpha 适用性**：注意力/零售关注机制（Barber & Odean 注意力效应、Tranco 排名作为关注度代理）。
经济方向先验：关注度**水平**高 → 短期超买 → 后续负收益（反转）；关注度**变化**为正 → 短期动量。
`snl27_totaldomains` 上升 = 业务/市场扩张 → 正向基本面成长信号。**不能与 PV/MODEL/OTHER/FUNDAMENTAL 组腿，
单独 ATOM 合规。**

### 2.2 本轮探针（J 批，8 条结构互异）

见 §6 汇总表。

---

## 3. risk（risk60 Securities Lending Insight）

| 字段 | 类型 | 覆盖率 | uC | aC | 含义 | alpha 适用性 |
|---|---|---:|---:|---:|---|---|
| `rsk60_crowding` | VECTOR | 0.6694 | 62 | 90 | 做空活动带符号日指标（正=增加做空/拥挤，负=回补） | ★ 主信号（做空压力流） |
| `rsk60_offer` | VECTOR | 0.6694 | 36 | 49 | 借券费率（年化，空头支付） | ★ 借券成本=做空需求价格 |
| `lending_fee_bid_rate` | VECTOR | 0.6694 | 35 | 38 | 出借费率（年化，多头出借收益） | ○ 供给侧价格 |
| `rsk60_last` | VECTOR | 0.6694 | 28 | 30 | 快照时点最新借贷费率 | ○ 即时费率 |
| `rsk60_datatime` | VECTOR | 0.6694 | 9 | 10 | 供应商时间戳 HHMMSS | ✗ 非分析量 |

**更新频率**：日频快照（datatime 为日内时间戳）。**分布**：费率为右偏正数（年化 0–100%+，少数借券难股极高）；
crowding 为带符号零中心流。**可用性**：全 VECTOR 须折叠；`rsk60_datatime` 不可作信号。
**适用性**：借券费率与 shortinterest 同族（`loaned_share_count`），**与已交付 RRE5Mwkn 存在机制重叠风险**，
需 0.5 互相关复核后才可入篮。

> 备注：risk68 / risk71 / risk72 在本区 coverage=0.0，直接排除；option1 / earnings6 /
> earnings_sent_matrix / macro27 / socialmedia12 / socialmedia5 同为零覆盖。

---

## 4. insiders（4 数据集）

| 数据集 | cov | 字段 | 备注 |
|---|---:|---:|---|
| insider_matrix | 0.5938 | 33 | 金额族：director/top_director/signal/top_signal × buy1,2 / sell3,4 |
| insider_trx_matrix | 0.5938 / 0.5823 | 33 | 事件计数族 + USD 金额族；大量字段 aC 0–7（极冷） |
| insider_agg_matrix | 0.6175 | — | 论坛称「最冷的真成交集」 |
| insiders1 | 0.5937 | — | 覆盖率不足闸线附近 |

**实测（8 条论坛黄金配方，I 批）**：严格照搬论坛实证
`ts_zscore(ts_sum(<字段>, N), 252)`（帖子 43152032301591，USA/TOP3000 实测 S 2.25）：

| Alpha | 表达式 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| MPYNoma6 | `ts_zscore(ts_sum(total_top_buy_transaction_count,126),252)` | 1.19 | 0.77 | 9.83% | 1.16 |
| d5WrAL1w | 同上 W63 | 1.19 | 0.82 | 11.95% | 0.74 |
| RREwnWA1 | `ts_zscore(ts_sum(eur_signal_value_2,126),252)` | 0.91 | 0.47 | 9.16% | 1.16 |
| gJeVEpZM | 净买入计数差 | 0.71 | 0.33 | 8.36% | 0.98 |
| GrW5pJWJ | W252/504 | 0.68 | 0.33 | 8.25% | 0.84 |
| 6XdLvOAJ | `ts_rank` 替 `ts_zscore` | 0.63 | 0.24 | 3.88% | 0.51 |
| Xg9A56Jz | `usd_top_direct_signal_value_2` | 0.58 | 0.26 | 10.03% | 0.71 |
| LLMYAJ5e | `usd_secondary_signal_value` | 0.57 | 0.23 | 9.29% | 0.92 |

**判死 `GBR-INSIDERS-DEAD`**：最高 S 1.19（距闸 0.39）、F 0.82（距闸 0.18）、2Y 1.16（距闸 0.42）。
论坛配方的**机制方向是对的**（计数流 > 金额流 > 比值流 > rank 流，与帖子一致），但 GBR TOP700 上
insider 覆盖率仅 0.59 且事件稀疏度低于 USA/TOP3000 ⇒ 幅度信息不足以支撑 1.58。

---

## 5. analyst7 与 dl_riskfree（本轮对照线）

### 5.1 analyst7（400 字段，coverage 1.0，42 个 raised 修订计数变体）

**16 条探针全灭**：
- G 批（裸 `group_rank(est_12m_*_raised*, subindustry)`，8 条）：S **0.04–0.16**
- H 批（几何扫描，8 条）：S **0.03–0.29**，最高 `ts_zscore(est_12m_pre_raised_1wk,252)` S 0.29

| 几何 | 表达式 | S | 2Y |
|---|---|---:|---:|
| 时序 z（年度窗） | `ts_zscore(est_12m_pre_raisednum_1mth,252)` | 0.17 | −0.56 |
| 时序 z + 分组 | `group_rank(ts_zscore(...,252), subindustry)` | −0.21 | −0.77 |
| 时序均值 | `ts_mean(...,22)` | 0.11 | −0.30 |
| 流量聚合 | `ts_zscore(ts_sum(...,22),252)` | 0.03 | −0.88 |
| 周频修订 | `ts_zscore(est_12m_pre_raised_1wk,252)` | 0.29 | 0.37 |
| 平滑 | `ts_decay_linear(ts_zscore(...,252),20)` | 0.04 | −0.89 |
| EBT 科目 | `ts_zscore(est_12m_ebt_raisednum_1mth,252)` | 0.16 | −0.24 |
| CPS 科目 | `ts_zscore(est_12m_cps_raisednum_4wks,252)` | 0.06 | 0.22 |

**判死 `GBR-ANALYST7-REVISION-DEAD`**：GBR 上「分析师修订计数」本身无截面预测力；历史记录里的
S 2.13 来自**已点亮 analyst 塔的其它数据集/组合**，不可从本集字段复现。

### 5.2 dl_riskfree_returns（other 塔，CNN 概率场）

8 条探针最高 S 1.02、2Y −0.48；60day/4q/5q 变体全负；`E5(label1_2q_5d)` 与 `E6(label0_2q_5d)`
精确互为 ±0.97 ⇒ 确证 `label1` = 做多方向。结论与 EUR 侧「S 0.18–1.37、2Y 全 DEAD、天花板 1.40」一致
⇒ **判死 `GBR-DLRISKFREE-DEAD`**。

---

## 6. 本轮跨数据集探针汇总（按数据集归因）

| 批 | 数据集 / 类别 | 条数 | 最高 S | 最高 2Y | 裁定 |
|---|---|---:|---:|---:|---|
| A–D | fund_holdings_panel（institutions） | 31 | 1.03（干净 0.94） | 1.44 | 判死（距 S 闸 0.55+） |
| E | dl_riskfree_returns（other） | 8 | 1.02 | −0.48 | 判死 |
| F | insider_matrix（insiders，rank 形态） | 8 | 0.71 | — | 判死 |
| G | analyst7（裸 rank） | 8 | 0.16 | — | 判死 |
| H | analyst7（几何扫描） | 8 | 0.29 | 0.37 | 判死 |
| I | insider_matrix / insider_trx_matrix（论坛配方） | 8 | 1.19 | 1.16 | 判死 |
| J | sentiment27（sentiment） | 8 | 待回填 | 待回填 | 待定 |
| K | fundamental6 新科目（fundamental，8 个全新财务科目） | 8 | 待回填 | 待回填 | 待定 |

---

## 7. 结构性结论

**GBR 未点亮塔（institutions / other / sentiment / risk / earnings / macro / socialmedia / insiders /
option / imbalance 除 imbalance 外）在 D1/TOP700 上是结构性贫瘠区**：8 个类别中除 sentiment27(0.80) 与
risk60(0.67) 外，其余数据集覆盖率全部为 0.0；两个可挖集里 institutions 已 31 条探针穷尽、
insiders 已 16 条穷尽，均实证 DEAD。

⇒ **唯一可量产路径是 fundamental6 的 `divide(fnd6_<科目>, cap)` 跨量纲族**（见
[gbr_fundamental6_campain.md](gbr_fundamental6_campain.md)），该族 `effective=2` 同时计 PV+DIV 两塔权重。
本战役为了「未点亮塔优先」的选集纪律，已先把 institutions / insiders / dl_riskfree / analyst7 / sentiment27
全部穷尽并留证，之后才回到该量产线**换新财务科目**扩招，理由与顺序在此存档。

## 8. ★★ 2026-11-08 傍晚补测：risk 塔有 coverage 1.0 的数据集（推翻第 7 节「risk60 0.67 是唯二可挖」）

第 7 节写于 `get_datasets(category=risk)` 只看了首屏的习惯，**漏掉了 `risk88`**。补测实读（GBR/D1/TOP700）：

| 数据集 | coverage | alphaCount | 字段数 | 名称 | 结论 |
|---|---:|---:|---:|---|---|
| **risk88** | **1.0** | 567 | **1** | Other Multi-Factor Risk Models | 唯一字段见下，**可用** |
| risk60 | 0.6694 | 202 | 5 | Securities Lending Insight Data | 已判死（8 条 S≤0.71）|
| risk68 / risk71 / risk72 | 0.0 | 731 / 608 / 606 | — | Forecast / Daily Specific Return / Specific return of extended factor | GBR 无覆盖，不可用 |

**`risk88` 全数据集只有 1 个字段**：`alternative_market_cap_usd`（MATRIX，cov **1.0**，ac 567，
"Market capitalization of each stock expressed in USD"）。⚠ 它的 `ac 567` 说明多人拿它当通用市值用过，
但**作为「非 PV 的市值分母」这一用法在 GBR 未见实证**——本轮首次验证（见
[gbr_fundamental6_campain.md](gbr_fundamental6_campain.md) 2026-11-08 傍晚节）：
`divide(fnd6_<科目>, alternative_market_cap_usd)` 单腿即 `failed_ra_count=0`，S 1.62–1.99 / 2Y 2.04–2.09。

**价值**：它把「X/市值」机制从 **PV×FUNDAMENTAL**（PV 落禁混集合时不可用）搬到 **FUNDAMENTAL×RISK**，
是跨区可复用的**合规市值分母替身**。局限：①字段仅 1 个、本身无法单独成 alpha（`rank(altcap)` 纯规模因子未测价值）；
②它解决合规不解决容量（该机制容量仍 1–2 席）。

## 9. sentiment7 判死（本轮新增，注意力因子）

`sentiment7` = Wikipedia 页面浏览量，cov 0.5784，全 3 字段均为 **VECTOR**：
`snt7_views`(0.5766) / `snt7_all_languages_views`(0.5819) / `snt7_timestamp`(0.5766)。

5 条结构互异模板（252d abnormal attention 反向 / 252d YoY 变化正向 / 504d 多语言 group_rank 反向 /
252d 自历史分位反向 / 66d 短窗正向）实测：

| 方向 | 代表 | S | TO | 2Y | fail |
|---|---|---:|---:|---:|---:|
| 注意力正向（短窗） | `group_rank(ts_zscore(vec_sum(snt7_views),66),subindustry)` | 0.28 | 32.1% | 1.24 | 3 |
| 注意力变化正向 | `rank(ts_av_diff(vec_sum(snt7_views),252))` | 0.37 | 53.1% | 0.34 | 4（含 CONCENTRATED_WEIGHT）|
| 注意力水平反向 | `reverse(rank(ts_zscore(vec_sum(snt7_views),252)))` | −0.40 | 52.4% | −0.30 | 5 |
| 自历史分位反向 | `reverse(rank(ts_rank(vec_sum(snt7_views),252)))` | −0.49 | 50.6% | −0.04 | 5 |
| 多语言反向 | `reverse(group_rank(ts_zscore(vec_avg(snt7_all_languages_views),504),sector))` | −0.10 | 25.5% | −0.71 | 4 |

⇒ **DEAD**。注意它不是「方向搞反」——正反两向都弱，且换手天然 25%–53%（页面浏览量日更且噪声大），
CONCENTRATED_WEIGHT 反复触发。sentiment 塔现有判死集：sentiment27、**sentiment7**；sentiment33(cov 0.32) 未测。

## 10. shortinterest3 单数据集 ATOM 判死（2026-11-08 晚，用户授权放开已点亮塔后实测）

背景：交付篮 6 颗里有 5 颗靠 `shortinterest3` 的 `loaned_share_count_main` 当**第二腿**出活，因此按用户授权
（放开已点亮塔）测试它能否**单独**成 alpha。`shortinterest3` 全 25 字段 = 8 测度 × 3 变体（`_main` / `_p5_d1` / 基础），
全部 VECTOR，cov 0.82–0.87。

**10 个结构互异模板（7 个不同测度）实测**：

| 测度 | 代表 | S | TO | 2Y | longCount | fail |
|---|---|---:|---:|---:|---:|---:|
| 借券费率波动率（水平） | `reverse(group_rank(ts_backfill(vec_avg(loan_rate_volatility_main),22),subindustry))` | **0.76** | 16.7% | 1.19 | 428 | 3 |
| 借券交易笔数（活跃度） | `reverse(rank(ts_zscore(vec_sum(transaction_count_main),252)))` | 0.64 | 12.8% | 1.91 | 346 | 3 |
| 借券需求评级（`shrt3_bar` 1-10） | `reverse(group_rank(ts_backfill(vec_avg(shrt3_bar),22),sector))` | 0.45 | 19.4% | 0.86 | 420 | 3 |
| 借券久期（loan age） | `reverse(group_rank(ts_backfill(vec_avg(average_loan_duration_days_main),22),sector))` | 0.27 | 13.0% | 0.01 | 417 | 4 |
| 借券费率（252d 变化） | `reverse(rank(ts_av_diff(vec_avg(mean_loan_rate_main),252)))` | 0.21 | 26.3% | −0.71 | 343 | 4 |
| 借券费率（水平） | `reverse(group_rank(ts_backfill(vec_avg(mean_loan_rate_main),22),sector))` | 0.15 | 17.6% | 0.54 | 420 | 3 |
| `shrt3_bar` 变化 | `reverse(rank(ts_delta(vec_avg(shrt3_bar),66)))` | 0.06 | 43.5% | −0.37 | 326 | 4 |
| 借券费率（66d z） | `reverse(rank(ts_zscore(vec_avg(mean_loan_rate_main),66)))` | −0.08 | 36.6% | −0.55 | 341 | 5 |
| 费率波动率变化 | `reverse(rank(ts_delta(vec_avg(loan_rate_volatility_main),66)))` | −0.10 | 31.5% | −0.78 | 314 | 4 |
| 最高-最低费率价差 | `reverse(rank(ts_zscore(subtract(vec_avg(max_loan_rate_main),vec_avg(min_loan_rate_main)),66)))` | −0.18 | 31.1% | −0.50 | 340 | 4 |

⇒ **DEAD**。longCount 314–428 排除覆盖解释；正反两向都弱、费率族（Drechsler 空头溢价）与久期族、评级族、活跃度族
全部不过 1.0。

**结构性结论（对本战役最重要的一条）**：`shortinterest3` 在 GBR 的价值**只存在于交互项**——
它作为第二腿能把别的信号放大（`add(multiply(2, A), reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main),504),sector)))`
这类形态出了 S1.78–2.15 三颗），但**自身没有任何可单独交易的溢价**。这也解释了为什么本篮 6 颗里
有 5 颗都用它当腿而无人用它当主信号。

## 11. 放开已点亮塔后的三个新域实测（2026-11-08 夜）：model53 / analyst47 / pattern_scores

用户授权放开已点亮塔后，除 shortinterest3（见第 10 节）外还探了三个**高覆盖 + 冷门 + 机制全新**的数据集。

### 11.1 model53（结构性违约概率，MODEL，cov 0.798–0.876）⇒ DEAD

22 字段：`annualized_pd_{1month,3month,6month,1year,2year,3year,4year,5year,7year,10year}_jc7` +
`mdl53_implied_spreads` + `mdl53_ms5_*`。**极冷**：`annualized_pd_4_year_jc7` / `annualized_pd_5_year_jc7` `ac=0`（从未被用）。

5 条模板（PD 水平正向 / PD 水平分组反向 / **PD 期限斜率**（5y−1m）/ PD 252d 变化 / 隐含信用价差反向）实测
**S −0.12 ~ 0.25**，longCount 282–411。⇒ **困境风险（distress risk）与信用曲线斜率在 GBR TOP700 无预测力**。

### 11.2 analyst47（Alternative Analyst Investment，cov 0.6445–1.0）⇒ 结构性封顶判死

5 字段：`anl47_indicator`（1–10 复合指标，cov **1.0**，ac 344）、`anl47_rawsentiment`、`anl47_rawexperts`、
`anl47_rawalphadecay`、`anl47_totalrawsignal`（后四者 cov 0.6445）。

5 条几何（裸 rank / 自历史分位 / 252d 变化 / 与 raw sentiment 分歧 / 行业组内 rank）实测：

| 几何 | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| `rank(ts_backfill(anl47_indicator,22))` | 1.35 | 0.58 | 22.7% | 1.02 |
| `ts_rank(ts_backfill(anl47_indicator,22),504)` | 1.35 | 0.55 | 24.0% | 1.05 |
| 与 raw sentiment 分歧（双 backfill 后相减） | 1.35 | 0.56 | 24.1% | 1.08 |
| 252d 时序变化 | 1.32 | 0.53 | 24.0% | 1.06 |
| 行业组内 rank | 0.39 | 0.14 | 15.3% | 0.42 |

**4 种几何精确收口在 1.32–1.35**——这是与 `news46`（S 1.32 封顶）同型的**结构性封顶签名**：
单一读数、换几何无位移 ⇒ 读数本身信息量到位即封顶，不是骨架问题。**判死，不再投入波次。**

### 11.3 ★ pattern_scores（图表形态相似度，PV，cov 0.9953–0.9998，504 字段）⇒ 新发现：**形态相似度是反向指标**

18 个形态族 × {mean,max,min,std,median,dynamic,q95} × lookback{60,120}。字段级极冷（ac 0–180，多数 ≤10）。

**① 方向反了（10 条几何的净符号证据）**：

| 表达式（`reverse(...)` 包裹后的**实测** S） | 翻转后正号 S | 2Y | TO |
|---|---:|---:|---:|
| `reverse(group_neutralize(rank(reversal_v_top_min_simscore_lookback60),sector))` = **−1.41** | +1.41 | 0.86 | 16.5% |
| `reverse(rank(multiply(breakaway_gap_up_q95,subtract(1,breakaway_gap_down_q95))))` = **−1.30** | +1.30 | 1.18 | 18.5% |
| `reverse(rank(subtract(breakaway_gap_up_mean,breakaway_gap_down_mean)))` = **−1.15** | +1.15 | 1.06 | 18.0% |
| `reverse(subtract(rank(reversal_v_bottom_median),rank(reversal_v_top_median)))` = **−1.11** | +1.11 | 0.53 | 12.2% |

⇒ **与「看涨形态」越像，未来收益越差；与「顶部/看跌形态」越像，未来收益越好**。即图表形态相似度在 GBR
是**反向（contrarian）**读数，不能按形态名义方向直接用。这条对任何区都可先验假设：形态相似度先测反号。

**② 唯一双闸健康的分支，但 S 不够**：
`ts_zscore(common_gap_up_mean_simscore_lookback120, 252)` → **S 1.21 / F 0.76 / TO 9.5% / 2Y 1.73 / sub 0.81**，
只挂 `LOW_SHARPE` + `LOW_FITNESS` 两条（**2Y 已过线且富余**）。这是本轮唯一「2Y 富余 + 低换手」的近失件。

**③ 设置档三点对照（该信号偏好原档，两套破闸杠杆全失效）**：

| 设置档 | 同表达式 S | 结论 |
|---|---:|---|
| `SUBINDUSTRY / d4 / t0.08`（原档） | **1.21** | 最优 |
| `SUBINDUSTRY / d10 / t0.08` | 1.09 | decay 加大 → −0.12 |
| `INDUSTRY / d4 / t0.05` | 0.95 | 换中性化+降 trunc → −0.26（与 fnd6 族相反！）|
| `SUBINDUSTRY / d4 / t0.20` | 1.21 | trunc 加倍 = **no-op** |
| `MARKET / d6 / t0.15` | 0.59 | 去行业中性化 → −0.62（灾难）|

★ **重要反例**：fnd6 族靠 `INDUSTRY/d10/t0.05 → SUBINDUSTRY/d4/t0.08` 破了 2Y 闸，**但本族反向**——
「设置杠杆」不是普适的，它只在「机制对、被行业共同因子遮蔽」时生效；对已经是**横截面形态分**的信号，
加强中性化/加 decay 只会砍掉信号。（本条已同步到 `Claude/skills/wq-brain-ra-gbr/references/` 的方法论。）

**④ 结论**：`pattern_scores` 是 GBR 一个**真实存在但封顶 S≈1.4** 的机制族：正号分支 2Y 富余但 S 卡 1.2，
反向分支 S 到 1.41 但 2Y 只有 0.86，**两分支无法同时过 S≥1.58 与 2Y≥1.58**。留作换防备胎
（`omE0z39k` / `2rAoZaa5` / `QPvpl22M` / `P0omlwwq`），不建议再投入波次。

## 12. 最后四个高覆盖域实测（2026-11-08 深夜）：model264 / model238 / analyst_earnings_ibes / model36

### 12.1 model264（Deep Learning 趋势概率，MODEL，cov 0.9667–0.9752）⇒ DEAD

**380 个 MATRIX 字段**，每个字段 `ac 3–21`（极冷），语义统一为「某目标未来趋势为上涨的概率」
（`mdl264_1l_<code>`，如 `_acf / _bb / _ifm / _fmc / _icc / _d12ntr`）。方向天然可解读（概率高=看涨）。

5 条模板（单字段 22d 均值 / 2 字段集成 / 4 字段集成 / 66d 分组 / 252d 时序 z）实测 **S −0.27 ~ 0.09**，
longCount 397–412。⇒ 该 DL 概率输出在 GBR TOP700 无预测力；**字段数多 ≠ 信号多**，
且这里连方向都不用测反（正反都贴 0）。**整族判死，不必再碰 380 个字段。**

### 12.2 model238（SmartHoldings 模型，MODEL，部分 cov 1.0）⇒ DEAD

22 字段，其中 6 个 cov **1.0** 的排名（1–100）：`mdl238_global_rank`(ac117) / `_global_change_rank`(ac211) /
`_global_owner_rank` / `_global_screening_rank` / `_country_rank` / `_industry_rank`。

5 条模板（4 个不同排名维度 + 1 个行业组内 rank）实测 **S −0.03 ~ 0.72**，longCount 229–323。
最强的 `screening_rank` S0.72。⇒ **机构偏好/拥挤度经模型加工后仍然无效**（与 institutions 塔 31 条探针的结论同源）。

### 12.3 analyst_earnings_ibes（Global Analyst Earnings Forecast，MODEL，cov 0.9966）⇒ 名不副实，非新机制

42 字段，但**前 12 个全是价格/收益容器**：`closing_price_dlr1/2/3`、`highest_price_dlr*`、`lowest_price_dlr*`、
`five_day_total_return_dlr*`（cov 全 1.0）。⇒ 它的 `cov 0.9966` 来自价格字段而非一致预期，
**本质是 PV 数据的另一份拷贝**。**不派波次**（既浪费额度又制造 PV 污染与高相关）。
★ 一般化教训：`dataset.coverage ≈ 1.0` 时要先看字段构成，价格类容器会把覆盖率虚高到接近 1。

### 12.4 model36（SmartRatios 信用比率模型，MODEL，cov 0.59–1.0）⇒ 无新机制，不派波次

20 字段 = 7 个 `credit_risk_*` 分项得分（cov 0.594–0.599）+ 5 个 `default_risk_*_percentile_d1_2`（cov 0.599）
+ `star_sr_*` 排名（cov 1.0，但只 6 个字段）。机制与已判死的 `model53`（违约概率）同源，
且覆盖更薄（0.59 vs 0.80）⇒ 按 12.1/12.2 的结论不再投入。

---

## ★ 最终封盘结论（2026-11-08）

GBR/D1/TOP700 平台上**所有 coverage > 0 且未被既有交付件占用**的机制面已逐域测尽，共 **22 个机制域判死**
（见第 7–12 节）。剩余 coverage 全为 0.0 的类别：option1 / earnings6 / earnings_sent_matrix /
macro27 / socialmedia12 / socialmedia5 / risk68 / risk71 / risk72 / institutions25 / 多数 analyst 与 news 子集。

⇒ **在「S≥1.58 + 2Y≥1.58 + F≥1.0 + 互相关全对<0.5 + GBR 不换区 + PV/MODEL/OTHER 禁混」的联合约束下，
GBR 的可交付上限 = 8 颗**。继续投入新域的期望产出已接近 0：本轮新增 6 个域（shortinterest3 / model53 /
analyst47 / pattern_scores / model264 / model238）共 55 条模板，**0 条过闸**。
想突破只能放宽其中一条约束（互相关门槛 / region / 禁混口径），不是继续扫数据集。
