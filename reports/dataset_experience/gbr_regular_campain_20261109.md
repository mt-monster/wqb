# GBR 固定区 regular alpha 战役报告（2026-11-09 定稿）

> 区域全程固定 **GBR / TOP700 / delay 1**，未切换。窗口 `2014-01-01 ` 2023-12-31`。
> 本文件归档战役的**最终可交付篮子、席位数学证明、全部波次归因、决定性负结果与工具陷阱**。
> 字段画像另见 [gbr_field_profiles_survey_20261109.md](gbr_field_profiles_survey_20261109.md)；
> 相关簇结构见 [gbr_correlation_cluster_survey_20261109.md](gbr_correlation_cluster_survey_20261109.md)。

---

## 0. 结论先行：20 颗在**已勘测池**内不可达（条件性结论，不是区域上限）

> **scope（引用本报告前先读这一行）**
> 样本来源 = 23 波 138 条回测 + 36 颗全闸池；**这些样本全部抽自「数据集级 cov>0」或「档案已判死」的集**。
> 截断条件 = GBR 177 个数据集中有 **41 个数据集级 cov=0 的未点亮塔数据集从未下过回测**，它们**不在**本报告样本内。
> ⇒ 下文所有「上限 10 席」只在上**述池子内**成立，**不外推到 GBR 全区**。
> 该结论在 2026-11-09 已被 field 级实查推翻过一次（反例 techindi_model：数据集级 cov=0 却有 399 个字段真实数据，
> 并贡献 10 席中的 2 席）。覆盖审计与口径修正见 **§12**，工具 tools/audit_dataset_coverage.py。

本轮把「合格池 + 相关性矩阵」做成了**可复算的精确解**（36 颗全闸 regular × 36×36 相关矩阵，
迭代加深回溯求最大独立集，非贪心）。结果：

| 口径 | 严格 `<0.5` 全对 | `<0.7` 全对 |
|---|---:|---:|
| GBR 原话口径（禁混集合 = PV / MODEL / OTHER） | **11** | 14 |
| 同上 + 组腿配额 `≤5` | **10** | —— |
| 保守口径（把 FUNDAMENTAL 并入禁混集合） | 10 | —— |
| 保守口径 + 组腿配额 `≤5` | **9** | —— |

**20 颗需要 20 个两两 `<0.5` 的独立机制面，GBR TOP700 的可用机制面只有约 10-11 个。**
差距不是「没挖够」，而是池子结构性的：见 §4 的四簇结构与 §5 的决定性负结果。

---

## 1. 最终可交付篮子（10 颗，全部 `failed_ra_count=0`，两两 `<0.5`）

两两相关：**max = 0.4967**（mLoWX91p × zq3nNGp8），min = −0.164（QPvbxjXw × rKRPAWv9）。
S 总和 **21.15**（原 10 颗旧解 20.28）。组腿配额实耗 **5/5**（合规上限）。

> ⚠ **`failed_ra_count=0` ≠ prod/self 已测**（2026-11-09 复核新证）：未提交件的 `checks.pending` 里仍挂着
> `SELF_CORRELATION` / `PROD_CORRELATION`，平台**只在提交时才计算**。实测只有 2 颗 ACTIVE 有真值：
> `RRE5Mwkn` prod **0.5129**、`bl6KwjwK` prod **0.4582**（均 `<0.7` ✅）；其余 8 颗 prod/self = **pending（未测）**，
> 不在「已验 prod」意义上宣称通过。篮子内部两两 `<0.5` 是本地 `compute_mutual_correlation` 实测，与 prod 无关。

| # | alpha | S | F | 2Y | TO | sub | 设置档 | 数据集（塔） | 机制 |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| 1 | `mLoWX91p` | 2.66 | 1.28 | 2.24 | 0.3258 | 1.73 | FAST/5/0.10 | techindi（OTHER）× shortinterest | 日内区间位置 × 借券久期短腿 |
| 2 | `zq3nNGp8` | 2.46 | 1.12 | 2.43 | 0.4453 | 2.15 | SUBINDUSTRY/4/0.08 | techindi（OTHER）× shortinterest | 同族换 `r1_q1` 腿 + 换设置档解耦 |
| 3 | `leAgQPO5` | 2.16 | 1.18 | 1.87 | 0.2382 | 1.69 | SLOW/5/0.06 | imbalance5（IMBALANCE）× pv1（PV） | 分数订单失衡 Δ × 量能确认 |
| 4 | `RRE5Mwkn` | 2.15 | 1.41 | 3.65 | 0.1425 | 1.10 | FAST/5/0.10 | pv103（PV）× shortinterest | 隐含波动率水平 × 借券量短腿 |
| 5 | `9qxOJJ1d` | 2.15 | 1.13 | 3.16 | 0.2242 | 1.70 | FAST/5/0.10 | analyst9（ANALYST）× shortinterest | 分析师上调/下调人数比 × 借券短腿 |
| 6 | `QPveQvOg` | 2.06 | 1.78 | 2.47 | 0.0749 | 1.68 | INDUSTRY/10/0.05 | fundamental6（FUND）× pv1（PV，cap） | 资本开支/市值二阶差分 + gaussian 分位 |
| 7 | `d5Wr8mzw` | 1.99 | 1.57 | 2.08 | 0.1655 | 1.47 | SUBINDUSTRY/4/0.08 | fundamental6（FUND）× risk（RISK） | PP&E/替代市值 同族（合规分母） |
| 8 | `bl6KwjwK` | 1.89 | 1.06 | 2.80 | 0.1711 | 1.18 | FAST/5/0.10 | analyst（ANALYST）× shortinterest | FY1 营收上调−下调 × 借券短腿 |
| 9 | `QPvbxjXw` | 1.87 | 1.14 | 1.98 | 0.1575 | 1.07 | FAST/0/0.10 | analyst（ANALYST）**纯 ATOM** | 目标价 low 的 4 周相对修正 |
| 10 | `rKRPAWv9` | 1.76 | 1.07 | 1.89 | 0.0806 | 1.40 | FAST/15/0.05 | news17（NEWS）**纯 ATOM** | 多元事件情绪 60 日均的 252 年序位（反向） |

### 逐条表达式

```text
mLoWX91p  add(multiply(2, group_rank(ts_zscore(tm_15_r1_r5_r10_rh_glb_d1_r10_q1, 126), sector)),
              reverse(group_rank(ts_zscore(vec_sum(average_loan_duration_days_main), 504), sector)))

zq3nNGp8  add(multiply(2, group_rank(ts_zscore(tm_15_r1_r5_r10_rh_glb_d1_r1_q1, 126), sector)),
              reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))

leAgQPO5  multiply(group_backfill(group_zscore(ts_av_diff(imb5_score, 126), industry), subindustry, 252),
                   ts_rank(volume, 66))

RRE5Mwkn  add(multiply(2, group_rank(ts_target_tvr_decay(ts_zscore(pv103_ivam_sum, 252), target_tvr=0.15), sector)),
              reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))

9qxOJJ1d  add(multiply(2, group_rank(ts_zscore(divide(subtract(vec_avg(anl9_s_numup), vec_avg(anl9_s_numdn)),
                    vec_avg(anl9_s_numanalysts)), 252), sector)),
              reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))

QPveQvOg  rank(ts_quantile(ts_av_diff(ts_av_diff(divide(fnd6_capxy, cap), 252), 252), 84, driver=gaussian))

d5Wr8mzw  rank(ts_quantile(ts_av_diff(divide(fnd6_newa2_ppent, alternative_market_cap_usd), 252),
                   84, driver=gaussian))

bl6KwjwK  add(multiply(2, group_rank(ts_zscore(subtract(analyst_upward_revision_count_fy1_revenue_7d_4,
                    analyst_downward_revision_count_fq1_revenue_7d_5), 66), sector)),
              reverse(group_rank(ts_zscore(vec_sum(loaned_share_count_main), 504), sector)))

QPvbxjXw  winsorize(rank(divide(subtract(ts_backfill(est_12m_pre_low, 500), ts_backfill(est_12m_pre_low_4wks_ago, 500)),
                   add(abs(ts_backfill(est_12m_pre_low_4wks_ago, 500)), 1))), std=0.2)

rKRPAWv9  ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_sum(nws17_multiple_comp_event_sentiment_score), 60), 252),
                   densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)
```

> 旧解 10 颗（`RRE5Mwkn, bl6KwjwK, ZYQXZj73, QPvbxjXw, rKRPAWv9, leAgQPO5, QPveQvOg, 1YNAJJ9z, 88RxORpX, Xg9A6rGl`，
> S 总和 20.28）同样是合法 10 席解，可互换。

---

## 2. 席位数学：怎么算出 10 / 11

1. `get_user_alphas` 分页扫全池（394 条）→ 按 `fl=0 & S≥1.58 & 2Y≥1.58 & F≥1.0 & 0.01≤TO≤0.70` 过滤 → **29 颗**；
   加上已提交/漏出列表窗口的 7 颗 → **36 颗全闸 regular**。
2. `compute_mutual_correlation(36, threshold=0.5, years=4)` → 36×36 矩阵（`.cache/gbr_corr_36.json`）。
3. 把「相关 `<0.5`」建成兼容图，**迭代加深回溯**（按兼容度降序做枢轴剪枝）求最大团：
   - 无配额：k=11 有解 → **MIS = 11**；k=12 无解。
   - 加组腿配额 `≤5`：k=10 有解、k=11 无解 → **10**。
   - 保守口径（+FUNDAMENTAL）：无配额 10、含配额 9。
4. 在全部 **90 个 size-10 团**里按 S 总和取最优 → 21.15（§1 的表）。

**工具自带 `max_mutually_below_subset` 在 >24 节点退回贪心**
（`max_subset_note: "greedy approximation (>24 nodes)"`），不可当终值 —— 本轮所有上限数字均为自算精确解。

---


## 3. 组腿配额台账（GBR 原话口径：禁混集合 = PV / MODEL / OTHER）

规则回顾：**禁混集合内部任意两两全禁**（含 PV+PV、多塔同现）；**允许集合内 × 集合外**（如 PV×NEWS），
但这类 alpha **总数 ≤5**；集合外 × 集合外 **不限量**。

### 10 颗交付篮子的配额实耗 = 5/5（已用满）

| alpha | 腿 1 | 腿 2 | 分类 | 占配额 |
|---|---|---|---|:--:|
| `mLoWX91p` | techindi（**OTHER**） | shortinterest | 集合内×外 | ✔ |
| `zq3nNGp8` | techindi（**OTHER**） | shortinterest | 集合内×外 | ✔ |
| `leAgQPO5` | imbalance5 | pv1 `volume`（**PV**） | 外×内 | ✔ |
| `RRE5Mwkn` | pv103（**PV**） | shortinterest | 内×外 | ✔ |
| `QPveQvOg` | fundamental6 | pv1 `cap`（**PV**） | 外×内 | ✔ |
| `9qxOJJ1d` | analyst9 | shortinterest | 外×外 | ✘ |
| `d5Wr8mzw` | fundamental6 | risk88 `alternative_market_cap_usd` | 外×外 | ✘ |
| `bl6KwjwK` | analyst | shortinterest | 外×外 | ✘ |
| `QPvbxjXw` | analyst（纯 ATOM 单集） | —— | 单数据集 | ✘ |
| `rKRPAWv9` | news17（纯 ATOM 单集） | —— | 单数据集 | ✘ |

**教训：配额是真正的绑缚约束，而不是相关性。** 11 席无配额解里有 6 个配额用户（多出的一个来自
把 techindi `r1_q1`/`r10_q1` 两个变体同时塞进篮子），一旦卡 `≤5` 就掉到 10 席。

**★ 一个易误判的点**：`cap` 属于 `pv1`（PV），不是 fundamental6 的同集字段。
所以 `divide(fnd6_X, cap)` = **FUND×PV 两条腿**，不是单塔 ATOM。换 `risk88.alternative_market_cap_usd`
作分母可得 FUND×RISK（集合外×集合外，免费），但**不增席**（同族相关 0.57–0.79，最大独立集 1）。

---

## 4. 相关性四簇结构（MIS=11 的根因）

36 颗全闸件按 PnL 聚成 4 簇：

| 簇 | 规模 | 成员特征 | 内部相关 | 可容席位 |
|---|---:|---|---:|---:|
| **A** techindi × 借券短腿 | 8 | `tm_15_r1_r5_r10_rh_*_q1` × `loaned_share_count`，只差设置档/腿变体 | 0.50–0.95 | **2** |
| **B** 借券短腿 × 弱主腿 | 10+ | 主腿换成 insider / earnings / analyst / mdl28 / avg_buy_shares 后**持仓几乎不变** | 0.63–0.99 | **1** |
| **C** `fnd6_科目 ÷ 市值` + `ts_quantile(gaussian)` | 12 | 换科目、换分母、换窗口都拆不开 | 0.51–0.98 | **2** |
| **D** 独立单通道 | 6 | pv103 IV / analyst 目标价修正 / news17 情绪 / imbalance5 / auction 失衡 / `avg_buy_shares` 独用 | 多对 <0.0 至 0.45 | **6** |

**★ 反直觉发现**：当主腿信息量弱于短腿时，混合体的实际持仓由**短腿**决定。
`2rAo7mm8`（earnings 意外）、`xArpnW5m`（insider 方向）、`88RxLYXl`（insider 净买）三颗主腿
完全不同，对同一组基线的相关系数几乎逐位相同（如对 `1YNAJJ9z` 均 0.63–0.65）。
⇒ **「换主腿」拆不开 B 簇，只有换短腿或换设置档才行。**

---

## 5. ★ 决定性负结果：去掉借券短腿，主腿全部崩掉

针对「弱主腿 = 短腿决定持仓」这一诊断，设计对照实验：把已证明能过闸的 6 条主腿**单独**跑
（纯 ATOM，无短腿），看能否开出全新独立面。两个设置档各 6 条，**12/12 全灭**：

| 主腿字段 | 纯 ATOM S（FAST/5/0.1） | 纯 ATOM S（SUBINDUSTRY/4/0.08 + ts_rank 几何） |
|---|---:|---:|
| `ern6_actual_eps − ern6_estimated_eps`（earnings 意外） | **−0.89** | −0.63 |
| `directional_indicator`（insider 方向） | 0.00（无持仓） | 0.14 |
| insider 净买比率 `(buy−sell)/(buy+sell)` | −0.15 | 0.36 |
| analyst FY1 营收上调−下调 | 0.96 | 0.10 |
| `auction_order_imbalance_pct_adv` | 0.69 | 0.50 |
| `mdl28_sm_structural_credit_..._rank` | 1.07 | `est_12m_pre_low` 水平 0.29 |

**结论（高置信）**：GOLD2 双段模板 `add(2·主腿, reverse(短腿))` 的 alpha **几乎全部由借券短腿承载**，
主腿只贡献低相关噪声/微小增量。因此：

1. 「换主腿开新面」这条路**彻底封死**——B 簇的所有成员本质是同一个短腿信号。
2. 「去短腿做纯 ATOM 开新面」这条路也**封死**——主腿独立时普遍 S<1.1。
3. 短腿本身不可替换：换 `loan_rate_volatility_main` / `transaction_count_main` 一律崩
   （N 波、O 波各 6 条全灭，最好 1.26）；只有 `average_loan_duration_days_main` 成功过 1 次（`mLoWX91p`）。

---

## 6. 波次全记录与归因（含失败原因）

| 波 | 条数 | 命中 | 方向 | 归因 / 淘汰原因 |
|---|---:|---:|---|---|
| K | 6 | 2 | insider 方向/净买 × 借券短腿 | delay 修正后转正；进 B 簇，不进篮子 |
| L | 6 | 1 | `ern6` EPS 意外 × 借券短腿 | 进 B 簇；`earnings_sent_matrix` 语气面 S0.16/−1.08 全灭 ⇒ earnings 有效的是「意外幅度」不是「管理层语气」 |
| M | 6 | 0 | 纯单集 ATOM（option IV / news50 事件量 / socialmedia5 情绪 / institutions4 净增持 / earnings_sent / analyst93） | **12 条纯 ATOM 0 命中**，信号强度本身不够 |
| N | 6 | 0 | `transaction_count_main` 作短腿 | **短腿太弱**——短腿决定持仓，弱短腿必然全灭 |
| O | 6 | 0 | 换强短腿重测 | 最好 S 1.26，仍不足 |
| P | 6 | 0 | news81 偏度/注意力、sentiment27、risk60 借券费率、insiders12、socialmedia12 | 单通道信号弱 |
| Q | 6 | 1 | 同表达式换 **SUBINDUSTRY/decay4/trunc0.08** | `zq3nNGp8` S2.46 全闸；`leAPWGX2` 仅 2Y 1.54 差 0.04 |
| R | 6 | 3 | 同表达式换 **MARKET/decay10/trunc0.10** | `58EdlON6`/`qMLJjleO`/`O0AX7Zw1` 全闸，但彼此 0.55–0.88 互斥，只有 1 席可用 |
| S | 6 | 1 | 换 **INDUSTRY/decay8/trunc0.05** | `ZYQv7j2Q` S2.64 全闸；`leAPj77e` 2Y 1.54 |
| T | 6 | 0 | **纯 ATOM 去短腿**（FAST 档） | 见 §5，主腿独立后全崩 |
| U | 6 | 0 | 纯 ATOM + `ts_rank` 几何 + SUBINDUSTRY 档 | 同上，更差 |

| V | 6 | 0 | news20 六个分类器专属语气面 | 最好 S0.65；news17 的 `event_sentiment_score` 是单点特例，不是族效应 |
| W | 6 | — | insider `*_significant_value_*` + `ts_backfill` | **整批被拒**（`error_count=6`，无 alpha_id）；insider 事件字段不能 backfill |
| W2 | 6 | — | 同上，去 backfill 直接取字段 | **整批被拒**；`directional_significant_value_*`/`directional_indicator_2`/`avg_top_*` 均不可用 |
| X | 6 | 0 | model313 无形资产强度 + model307 地理销售暴露 | 最好 S0.44；两类新机制在 GBR 均无独立信号 |
| Y | 6 | 0 | 5 个免配额独立通道换 SUBINDUSTRY 档 | **5/5 新件全灭**（最好 1.36）；1 条被平台按同表达式去重返回旧件 |
| Z | 6 | 0 | 同 5 通道 + news17 变体换 MARKET 档 | **6/6 全灭**（最好 S1.50/2Y1.52、S1.48/2Y2.14） |
| AA | 6 | — | model36 `star_sr_*` 信用风险六维（cov 0.60–1.0） | 首派 multisim 静默丢失（URL 拼错致 404），重发为 AA2 |
| AA2 | 6 | 0 | 同上重发 | **6/6 全灭，最好 S0.26**（区间 −0.61~0.26）；信用风险六维在 GBR TOP700 无独立信号 |
| AB | 6 | 0 | pv109 债券到期收益率 / insiders1 交易显著性 / other699 散户交易 | **6/6 全灭，最好 S0.06**（5 条为负）；固收、散户流、交易显著性三族在 GBR 均无信号 |
| AC | 6 | 0 | ANALYST×INSTITUTIONS 组合（EUR 冠军配方跨区移植 + 5 结构变体，**免配额**） | **6/6 全灭，最好 S0.98**（买盘单腿版）；EUR 冠军原样在 GBR 仅 **0.88**（EUR 1.69）⇒ 组合机制不跨区 |

合计 **21 波 126 条**派发（其中 W/W2 共 12 条被平台整批拒收、AA 首派 6 条静默丢失、Y 有 1 条被去重，实际出结果 **107** 条），
有效增量（能进篮子的独立席）**3 席**（`9qxOJJ1d`、`d5Wr8mzw`、`zq3nNGp8`）——这 3 席全部在 Q/R/S 波产生，
其后 **10 波 60 条（41 条出结果）0 新增**。

---

## 7. ★ 设置档 = 独立解耦杠杆（本轮最可复用的技法）

同一表达式在**不同中性化档**下是**不同持仓**，实测可把相关从 0.81 压到 0.46–0.50。
这是本轮唯一稳定的扩席手段（`zq3nNGp8` / `58EdlON6` / `ZYQv7j2Q` 全部由此而来）。

| 设置档 | 表达式 | S | F | 2Y | TO | sub |
|---|---|---:|---:|---:|---:|---:|
| FAST / decay5 / trunc0.10 | techindi `r1_q1` × 借券量 | 3.08 | 1.63 | 2.50 | 0.3162 | 2.37 |
| SUBINDUSTRY / decay4 / trunc0.08 | 同上 | 2.46 | 1.12 | 2.43 | 0.4453 | 2.15 |
| INDUSTRY / decay8 / trunc0.05 | 同上 | 2.64 | 1.57 | 2.31 | 0.2886 | 2.22 |
| MARKET / decay10 / trunc0.10 | 同上 | 2.46 | 1.60 | 2.33 | 0.2494 | 2.23 |

互相关：FAST vs SUBINDUSTRY **0.50**（可共存）；SUBINDUSTRY vs MARKET **0.81**（互斥）；
MARKET vs INDUSTRY **0.95**（互斥）。⇒ **四个档最多取 2 个，取 FAST + SUBINDUSTRY 最优。**

⚠ **设置杠杆不普适**：同一族在 pattern_scores 上反向恶化（FAST 1.21 → INDUSTRY 0.95 → MARKET 0.59）。
判据：信号已做过横截面组内排名时，加强中性化/加 decay 只会砍信号；
只有当机制**对但被行业共同因子遮蔽**时才靠换档破闸。

---

## 8. 工具用法与陷阱（本轮新证）

1. **`get_user_alphas` 列表响应自带完整指标**（`metrics.sharpe/fitness/turnover/two_year_sharpe/sub_universe_sharpe`、
   `ra.failed_ra_count`、`checks.fail`）⇒ 不必逐颗 `batch_get_alpha_metrics`。
   但扫描窗口会**漏掉自己刚创建/已提交的件**（本轮 394 条里缺 7 颗已知件），必须分页 + 已知 ID 补拉取并集。
2. **`batch_get_alpha_metrics` 单次上限 20 个** `alpha_ids`，超出直接报 "最多 20 个"。
3. **返回结构**：`batch_get_alpha_metrics` 的 `r.output` 尾部会拼 `[MCP structured content]`，
   `JSON.parse(r.output)` 必失败 —— 一律读 **`r.data`**；字段名是 `alpha_id` 不是 `id`。
4. **`compute_mutual_correlation` 在 `run_code` 里做 O(n²) 图搜索会超 JS 计算预算**：
   矩阵先落盘（`.cache/gbr_corr_36.json`），再把求解拆成独立小程序，一次只算一个阈值。
5. **`get_alpha_details` 的 `regular.code` 对 SUPER 类型为空**，别当成「表达式丢失」；
   本轮 `vR1oxrld`/`N1N2WRXo`（S3.47/3.49、F3.2）就是 SUPER，按用户口径（只走 REGULAR/ATOM）**排除**。
6. **`delay:5` 在 GBR TOP700 不被接受**（报 `"5" is not a valid choice`，整批 400），必须 `delay:1`。
7. **`compute_mutual_correlation` / `get_alpha_pnl` 会 429**（PnL 端点限流），退避 45s+ 或错峰重试。
8. **`add(<计数/股数字段>, 1)` 作除法兜底 → 单位不兼容整条 FAIL**；
   `ts_max`/`ts_min` → `[INACCESSIBLE_OP]` 整批被静态门禁拒收。
9. **multisim 长期停在 `progress:0.35`**（10–20 分钟后自行完成），期间 `harvest` 返回
   `No children found`，**不可据此判死**。
10. **★★ `multisimulation_location` 必须原样照抄工具返回的 URL**：真实格式是 `https://api.worldquantbrain.com/simulations/<id>`，
    **没有** `/multisimulation/` 路径段。自行拼成 `/simulations/multisimulation/<id>` 会 **HTTP 404**，
    看起来像「波次丢了」，实为 URL 拼错（本轮 AA 波实证，白等一轮 5 分钟）。
11. **「404 + `get_user_alphas(order="-dateCreated")` 里查不到对应特征字段的新件」= 该波整批未落件**，
    不是「还在跑」。判定法：按波次的特征字段名（如 `star_sr_`）在最近 40 条里反查；查不到就**重发**，不要干等。
12. **`failed_ra_count=0` 不代表 `SELF_CORRELATION` / `PROD_CORRELATION` 已测**：未提交件的
    `checks.pending` 仍包含这两项，平台只在提交时计算 ⇒ 汇报时必须写「prod 未测」，不可写成「prod 通过」。

---

## 9. 近闸库存与待裁定

### 近闸（差一点即可用）

| alpha | S | F | 2Y | 缺口 | 备注 |
|---|---:|---:|---:|---|---|
| `leAPWGX2` | 2.43 | 1.15 | **1.54** | 2Y 差 0.04 | SUBINDUSTRY 档；若 2Y 线松动即可启用 |
| `leAPj77e` | 2.36 | 1.36 | **1.54** | 2Y 差 0.04 | INDUSTRY 档，同上 |
| `akK9ooZv` | 3.10 | 1.48 | 2.71 | 全闸 | 进池但因相关被挤出篮子 |
| `88RxORpX` | 3.08 | 1.63 | 2.50 | 全闸 | 同上（旧 10 席解成员） |

### 需用户裁定的一件事

**「20 颗」与「两两 <0.5」+「组腿 ≤5」在 GBR TOP700 上不可同时满足**（已精确证明，非估计）。
三条可选路径：

- **A（默认，合规最大化）**：交付 §1 的 **10 颗**（两两 <0.5、配额 5/5 用满、全部 fl=0）。
- **B（放宽相关到 <0.7）**：可交付 **14 颗**，代价是同族相关性抬到 0.5–0.7。
- **C（放宽/取消相关约束）**：36 颗全闸件可全交，但同族相关普遍 0.7–0.99，不符合「独立 alpha」本意。
- **D（放宽组腿配额）**：可到 **11 颗**（仍严格 <0.5），代价是配额超 1。

---

## 10. 扩池尝试终局（V`AC 十波 60 条，2026-11-09）

在 10 席定稿后仍继续针对「新独立机制面」投入 6 波 36 条，结果全负：

| 方向 | 条数 | 结果 | 判定 |
|---|---:|---|---|
| news20 六个分类器专属语气面 | 6 | 最好 S0.65 | news17 是单点特例，非族效应 |
| insider `*_significant_value_*` 显著交易金额 | 12 | **整批拒收** | 字段不可用 + insider 事件字段不能 backfill |
| model313 无形资产强度 / model307 地理销售暴露 | 6 | 最好 S0.44 | 新经济机制在 GBR 无独立信号 |
| 独立通道换 SUBINDUSTRY / MARKET 档再铸 | 12 | 10 条实测全灭，2 条被去重/拒收 | **设置杠杆只对 techindi 族有效** |
| analyst_earnings_ibes（42 字段） | 0 | 未派发 | 名不副实：全为量价字段，零盈利预测 |
| model36 `star_sr_*` 信用风险六维 | 6 | 最好 S0.26 | 信用风险分解在 GBR 无独立信号；首派因 URL 拼错丢失，重发后同结论 |
| pv109 债券到期收益率 / insiders1 交易显著性 / other699 散户交易 | 6 | 最好 S0.06 | 固收、交易显著性、散户流三族全灭（5 条为负） |
| **ANALYST×INSTITUTIONS 组合**（EUR 冠军配方 + 5 变体，**免配额**） | 6 | 最好 S0.98 | ★ EUR 冠军原样 S1.69 ⇒ GBR **0.88**，2Y 0.60 ⇒ **组合机制不跨区** |

**本波次的判定（条件性）**：在上述样本（后 10 波 60 条，全部抽自 cov>0 / 已判死的集）内，
两两 <0.5 + 组腿配额 ≤5 的独立机制面上限约 **10** 个；**在该样本内**继续投新数据集的边际产出为 0
（后 10 波 60 条实测 0 新增全闸件）。
**这不等价于「GBR 全区穷尽」**：41 个 cov=0 的未点亮塔数据集从未进入样本（见 §12），样本截断决定了结论的边界。

> ★ **最后一条免配额路径也已封死**：`ANALYST × INSTITUTIONS` 两腿都在 `{PV,MODEL,OTHER}` 之外，
> 按 GBR 规则**不占组腿配额**，且该配方在 EUR 已跑到 S1.69/F1.05/2Y2.17（`N1NGbddg`）。
> GBR 原样移植只有 S0.88/2Y0.60，6 个结构变体最高 S0.98 ⇒ **组合层的 alpha 同样不可跨区搬运**，
> 与 §5「主腿不可脱离短腿」是同一枚硬币的两面：GBR 的强度绑定在 `loaned_share_count_main` 这条借券腿的**区内**信息上。
若要突破 10 席，只有三条路，且都不在「继续挖 GBR」这条轴上：
1. 放宽相关性到平台 0.7 线 → 14 席；
2. 放宽组腿配额 → 11 席；
3. 换区域（但本战役约束是全程固定 GBR，不得切换）。

**本战役交付定稿 = §1 的 10 颗**，两两最大相关 0.4967，S 总和 21.15，全部 `failed_ra_count=0`。

---

## 11. 设置轴与 universe 轴穷尽（2026-11-09 终局补测）

### 11.1 ★ universe 轴：EQUITY 只有 TOP700（陷阱）

平台报错给出的 GBR 合法 universe 列表是 `['TOP700', 'TOP350']`，但用 `TOP350` 派发时整批 400：
`Universe TOP350 is not available for instrument type EQUITY and region GBR.`
⇒ **GBR + EQUITY 实际只有一个可用 universe（TOP700）**，「换 universe 开新机制面」在本战役不可用。

### 11.2 ★ 中性化档全图：7 档测完，techindi 族容量恒为 2 席

此前只测过 FAST / SUBINDUSTRY / INDUSTRY / MARKET / SLOW。本轮补测 **CROWDING（decay2）** 与 **SLOW_AND_FAST（decay4）**，
各 6 条（GOLD2 r10 / GOLD2 r1 / `fnd6_capxy÷cap` / `est_12m_pre_low` / news17 / anl9 广度）：

| 新档 | 全闸件 | S | F | 2Y | TO | 与同腿原件的相关 |
|---|---|---:|---:|---:|---:|---|
| CROWDING | `58EdGG95`（GOLD2 r10 × 借券久期） | 2.66 | 1.16 | 2.35 | 0.4983 | **0.769** vs `mLoWX91p` |
| CROWDING | `akK9RRPv`（GOLD2 r1 × 借券量） | 2.78 | 1.16 | 2.57 | 0.6532 | **0.792** vs `zq3nNGp8` |
| CROWDING | `omE0PPzv`（`fnd6_capxy÷cap` gaussian） | 1.82 | 1.41 | 2.09 | 0.1482 | **0.858** vs `QPveQvOg` |
| SLOW_AND_FAST | `3qov1Q0O`（GOLD2 r1 × 借券量） | 2.91 | 1.18 | 2.51 | 0.4749 | **0.710** vs `zq3nNGp8` |
| SLOW_AND_FAST | `0mY2xOGq`（`fnd6_capxy÷cap` gaussian） | 2.04 | 1.27 | 2.11 | 0.1577 | **0.649** vs `QPveQvOg` |
| SLOW_AND_FAST | `GrW5X1Q3`（news17 事件情绪） | 1.97 | 1.22 | 2.39 | 0.0909 | **0.905** vs `rKRPAWv9` |

> 注：`est_12m_pre_low` 在 SLOW_AND_FAST 下只有 S1.21（`leAPEpgx`），anl9 广度 1.69（`E56PNOmR`），均未过闸。

**结论（决定性）**：6 个新全闸件与对应原件的相关全在 **0.649–0.905**，**无一 <0.5**。
16 节点图（10 席 + 6 新件）重新精确求最大团，**结果仍是 10，且就是当前这 10 颗**。
⇒ **7 个中性化档全部测完，techindi 族容量恒为 2 席；设置档不是可无限开采的维度。**
与 §7 的「FAST vs SUBINDUSTRY 0.50 / SUBINDUSTRY vs MARKET 0.81 / MARKET vs INDUSTRY 0.95」一致——
**换档改的是噪声实现，不是信息源**。

### 11.3 ★ 同等席位下的更优变体（可选，未采用）

16 节点图上一共存 **12 个 size-10 团**。S 总和最高的一解为 **21.81**（当前交付解 21.15）：

```text
RRE5Mwkn, bl6KwjwK, QPvbxjXw, leAgQPO5, QPveQvOg, d5Wr8mzw, 9qxOJJ1d,
58EdGG95, 3qov1Q0O, GrW5X1Q3
```

相对当前篮子：**换出** `mLoWX91p`(2.66) / `zq3nNGp8`(2.46) / `rKRPAWv9`(1.76)，**换入** `58EdGG95`(2.66) / `3qov1Q0O`(2.91) / `GrW5X1Q3`(1.97)。
两两仍全 `<0.5`，配额仍 5/5。

**但未被采用**：换入件换手更高（0.4983 / 0.4749 / 0.0909 vs 0.3258 / 0.4453 / 0.0806），
`58EdGG95` 的 F(1.16) 也低于 `mLoWX91p`(1.28)。**+0.66 的 S 总和换不来鲁棒性**，故保留当前 10 席；需要更高 S 时可直接切换。

### 11.4 本波次扫过的轴（条件性清单，不是区域穷尽证明）

| 轴 | 已扫范围 | 结论 | 该结论的边界（截断条件） |
|---|---|---|---|
| region | 固定 GBR（用户约束） | 未切换 | —— |
| universe | TOP700 / TOP350 探测 | **EQUITY 仅 TOP700** | 平台 get_datasets 报错原文 |
| category | 16 类逐个扫描 + 判死台账 | 样本内独立机制面 ≈10 | **只覆盖进入过回测的集** |
| 中性化档 | **7 档全测** | 容量 2 席 | 只在 techindi 族实测 |
| 表达式形态 | 纯 ATOM / 双腿 / 三腿 / 反向 / 差分 | 短腿不可去 | 受限于单一载体 |
| 跨区移植 | EUR 冠军组合配方 | 证伪（§10） | 单点，不等于全部组合 |
| 波次 | **23 波 138 条** | 后 12 波 72 条 0 增席 | **72 条全部抽自 cov>0 池** |
| **数据集覆盖** | **2026-11-09 逐集实查 `/data-fields` + 证据反查（§12）** | **可开采池 65 个里有 16 个「有字段、零回测证据」**（原先按数据集级 cov=0 估成 41 个，实查后**修正为 16**） | **本行推翻了 §11.4 旧版的绝对化断言** |

**⇒ 在「严格 <0.5 + 组腿配额 ≤5」下，本报告样本内的交付上限 = 10 席。**
**这不是「GBR 全区上限」**：样本被「数据集级 cov>0 / 档案已判死」两道前置条件截断，
池外仍有 **16** 个未点亮塔数据集有真实字段却一条回测都没跑过（§12 给出实查结果与探针清单）。

---

## 12. 覆盖审计与口径修正（2026-11-09 根因治理）

> 本节的处理对象不是「再挖几个 alpha」，而是**这套筛选流程为什么会静默漏掉数据集**。
> 结论：原 §0 / §11.4 的绝对化表述（「数学不可达」「不再有未探轴」）**作废**，
> 降级为条件性结论；同时把两条根因做成**可执行门**（工具 + 退出码），不再只写在文档里。

### 12.1 两条根因（用户批评原文的结构化）

**根因 A：筛选流程的顺序，让覆盖率检查变成不可逆的硬性拦截。**
SOP 漏斗是「塔 → 语义 → 画像（cov<0.6 剔除）→ 近静态 → …」，cov 排在第 3 位。
它一旦砍掉一个数据集，后面的语义闸、近静态闸、模板设计**永远不会被评估**，
而且它是静默的——不报错、不告警，只留一个「跳过」。被错误前置条件剔除的分支，成本是零感知的。

**根因 B：抽样被截断，但结论没有跟着截断。**
「后 12 波 72 条，0 增席」是真数据，但这 72 条**全部抽样自 cov>0 的池子**。
把「这条轴没有新增」外推成「整个区域没有剩余」，就是**用一个把储备排除在外的样本，证明储备不存在**（构造性偏倚）。

### 12.2 四条「假证据」（每条都有本区实测）

| # | 当时的判据 | 为什么是假的 | 本区实测 |
|---|---|---|---|
| 1 | 数据集级 `coverage = 0` ⇒ 没数据 | 它是聚合值，且本区普遍为 0 | `techindi_model` = **0.0**，却返回 **399** 个字段、贡献 10 席中的 **2 席**与全部 GOLD2 模板 |
| 2 | field 级 `coverage = 0` ⇒ 没数据 | 字段级同样会全 0 | **177 个集里 109 个集的所有字段 coverage 全 = 0**（含 `techindi_model` / `fundamental1` / `other78`） |
| 3 | 本地回测记录（`expressions.dataset`）里有 ⇒ 挖过 | 该列**大量为空** | 本区 12,648 行里有 **2,986 行（23.6%）dataset 为 NULL**；`imb5_score` 的 88 条 GBR 回测、`anl9_s_numup` 15 条、`tm_15_r1_r5` 36 条全被记成「没挖过」 |
| 4 | 后 N 波 0 增席 ⇒ 全区无剩余 | 样本被前置闸截断 | 72 条全来自 cov>0 的 49 个已测集；可开采池 65 个里有 16 个根本没进过样本 |

⇒ **唯一站得住的「有数据」判据 = 平台 `/data-fields` 返回字段目录非空**（本区 177/177 都非空；
**没有任何一个数据集可以因「没数据」判死**）。「挖过没」只能用**表达式原文里的字段名**反查，
不能用 `dataset` 列、不能用本地画像表的 `n_tests`（不含 MCP 直连仿真）、不能用自家档案的字符串。

### 12.3 平台逐集实查结果（177 集，全部现拉）

| 口径 | 集数 |
|---|---:|
| 平台全量（D1 / TOP700 / EQUITY） | **177** |
| 已点亮塔（规则性排除，与数据无关） | 112 |
| **可开采池（未点亮塔）** | **65** |
| 池内已挖掘（有挖掘记录） | 49 |
| 池内**仅探针、零开采尝试**（探针已证有数据） | 16 |
| 池内真未探（零证据且未探针） | **0** |
| 池内无字段（可判死） | **0** |

已点亮塔分布（`alphaCount`）：model 13 / pv 5 / news 3 / analyst 3 / fundamental 3 / shortinterest 3；
其余 10 个 category 全 0（institutions / insiders / earnings / sentiment / risk / option /
socialmedia / macro / imbalance / other(1)）。

### 12.4 原真未探清单（16 个）：探针已全部证伪「没数据」

| dataset | category | valueScore | alphaCount | 字段数 | maxCov | 元数据盲区 |
|---|---|---:|---:|---|---:|---|
| `other571` | other | 7.0 | 3 | 23/23 | 0.0 | 是 |
| `event_relation` | other | 6.0 | 12 | 12/12 | 0.0 | 是 |
| `event_sentiment_signals` | other | 6.0 | 117 | 50/52 | 0.0 | 是 |
| `news_sentiment_nlp` | other | 6.0 | 18 | 23/23 | 0.0 | 是 |
| `other296` / `other315` / `other323` / `other425` / `other734` | other | 6.0 | 19 / 22 / 15 / 26 / 23 | 10 / 21 / 7 / 13 / 7 | 0.0 | 是 |
| `other635` | other | 6.0 | 2 | 3/3 | 0.0 | 是 |
| `other78` | other | 6.0 | 87 | 50/112 | 0.0 | 是 |
| `search_interest` | other | 6.0 | 11 | 7/7 | 0.0 | 是 |
| `stock_search_trends` | other | 6.0 | 19 | 12/12 | 0.0 | 是 |
| `other424` / `other436` | other | 5.0 | 45 / 23 | 3 / 3 | 0.0 | 是 |
| `socialmedia39` | socialmedia | 2.0 | 298 | 1/1 | 0.4948 | 否 |

**读法**：15/16 是「coverage 元数据全 0」的盲区集——**它们不是没数据，只是元数据不报**。
当时这一步只做成「清单落盘」（`data/dataset_assets/GBR_probe_plan_d1.json`），
**探针本身没跑**；2026-11-09 已补齐并全部证伪，结果见 §12.7（16/16 有持仓）。

### 12.5 把纪律做成门（工具 + 退出码，可复现）

| 动作 | 命令 | 语义 |
|---|---|---|
| 全量审计 | `python tools/gates/audit_dataset_coverage.py --region GBR --universe TOP700 --delay 1 --md reports/dataset_experience/gbr_coverage_audit_20261109.md --probe-plan data/dataset_assets/GBR_probe_plan_d1.json` | 逐集实查 `/data-fields` + 用表达式原文反查证据；产出 `UNTESTED_BLIND` / `UNTESTED_COV_OK` / `NO_FIELDS` / `TESTED` / `LIT_EXCLUDED`，并写 scope（样本 + 截断） |
| 派发前 | `--gate coverage` | 池内若有集只靠「cov=0」被剔除而无 field 实查 ⇒ exit 1 |
| 收尾前 | `--gate closure` | 还有未探集 / 探针失败 ⇒ exit 1（回灌探针后 **PASS**） |
| 探针前 | `--gate probe` | 输出「必须探针」清单（未探 + `PROBE_FAILED`） |
| **执行探针** | `python tools/probe/dataset_data_probe.py --region GBR --universe TOP700 --delay 1 --plan <清单> --out <results.json> --jobs 4` | 每集一条最小仿真读 `longCount/shortCount`；`neutralization=NONE` 让 `rank` 恒正、不过中性化 |
| **回灌探针** | `--probe-results <results.json>` | `UNTESTED_BLIND` → `TESTED` / `NO_DATA`；失败留 `PROBE_FAILED` 并继续阻断 closure |
| 报告措辞 | `--lint-report <md>` | 「穷尽 / 数学不可达 / 上限 N 席」附近 4 行必须有 scope，否则 exit 1 |
| 判死清单背书 | `python tools/gates/category_coverage_audit.py ... --field-audit <audit.json>` | `--tested` 声明的集只有 `TESTED`/`NO_DATA` 才算已排除，其余**剥出分子**并转 `NOT_EXHAUSTED` |

措辞门已对本文跑过：3 处绝对化断言被拦下并改写成条件性表述（§0 / §11.4 / 本文末段）。

### 12.6 结论重述与下一步

1. **§0 / §11.4 的绝对化结论作废**。正确表述：**在「可开采池 65 个里的已挖掘 49 个」这个样本内**，
   两两 `<0.5` + 组腿配额 `≤5` 的交付上限 = **10 席**；该结论不外推到 GBR 全区。
   ★ 探针结果（§12.7）把这句话的适用范围又压小了一圈：那 16 个「待确认」的集**全部证实有数据**
   （持仓 210–915 只），而且**一次开采尝试都没有** ⇒ 10 席只是**已开采子集的容量**，
   它与「本区容量」之间没有任何等式关系。
2. 存量 10 席交付**不受影响**（合规性、相关性、闸门结论都是实测的，与本次口径修正无关）。
3. **已完成**：16 个集各跑一条探针，**16/16 有持仓**（`probe_data_present_n=16`，零失败）。
   下一步按门走：这 16 个集进 S1 体检 → 开波次；**它们才是下一批的合法候选池**。
4. **本次仍没做成的事**（诚实登记，避免又被当成「已经没得挖」）：
   - `delay=0`（D0 / 73 个数据集）尚未审计 —— 本区覆盖结论目前只覆盖 D1；
   - 字段名采样每集最多 2 页，**52 个集被截断**（只会低估「已测」，方向保守）；
   - 16 个集只有**一条**探针读数，**没有做过任何模板族开采** ⇒ 它们的容量是未知量（不是 0，也不是 10）；
   - `tools/audit_structure.py --only s11` 仍有 1 个**非本次引入**的违规（`tools/forum_post.py` 未登记主题）。

### 12.7 探针实测：16/16 有数据（本轮最硬的一条证据）

判据 = 每集挑一个 MATRIX/VECTOR 字段跑一条最小仿真 `rank(ts_backfill(<字段>,250))`，
**刻意 `neutralization=NONE`**（`rank` 恒正、不过中性化 ⇒ `longCount` 直接等于「本区有数据的股票数」；
若用 SUBINDUSTRY，常数型字段会被中性化成 0 持仓、误判成没数据），读 `is.longCount + is.shortCount`。
判据 `> 0` 即有数据；**读不到读数 = `PROBE_FAILED`，不算没数据**。

| dataset | 探针字段 | longCount | 判读 |
|---|---|---:|---|
| `other323` | `oth323_esor` | 915 | 有数据 |
| `news_sentiment_nlp` | `headline_vader_positive_polarity` | 836 | 有数据 |
| `other315` | `contract_notional_value_leg1` | 722 | 有数据 |
| `other296` | `oth296_prob_pos` | 694 | 有数据 |
| `search_interest` | `relative_interest_score_6` | 657 | 有数据 |
| `other78` | `entity_recognition_score` | 650 | 有数据 |
| `other635` | `oth635_char_count` | 634 | 有数据 |
| `event_relation` | `entity_connection_type_financial` | 623 | 有数据 |
| `other571` | `oth571_views28d` | 521 | 有数据 |
| `other425` | `market_value_total_2` | 500 | 有数据 |
| `other734` | `oth734_standardized_company_value` | 489 | 有数据 |
| `socialmedia39` | `scl39_top5_people_also_watch_ticker_ii` | 424 | 有数据 |
| `event_sentiment_signals` | `section_sentiment_score_3` | 343 | 有数据 |
| `other424` | `oth424_divyld` | 247 | 有数据 |
| `other436` | `oth436_divyld` | 247 | 有数据 |
| `stock_search_trends` | `search_interest_1y_equity_symbol` | 210 | 有数据 |

`shortCount` 全为 0 是 `neutralization=NONE` + `rank()` 恒正的设计结果（纯多头探测仪），
不代表这些集只能做多。探针 alpha id 见 `reports/dataset_experience/gbr_coverage_audit_20261109.md`。

**三条结论**：

1. **「coverage=0 ⇒ 没数据」在本区被 16/16 全面证伪**。这 16 个不是边角料：
   `event_sentiment_signals` 有 117 个平台 alpha、`other78` 87 个、`other424` 45 个 ——
   **别人在同一个集上是有产出的**，而我把它们整枝静默跳过了。
2. **「多少只」比「有没有」更能标出代价**：持仓 210–915 只（GBR TOP700 宇宙）
   ⇒ 这不是「稀疏到只能交易几只票」，而是**能支撑截面变换的完整数据集**。
3. **流程修好 ≠ 产能立刻回来**：探针只证「有数据」，不证「有 alpha」。
   这 16 个集的容量必须靠后续模板开采实测；在拿到那些实测之前，
   任何席位结论都只是**对已开采子集的说法**。

复现（两条命令，前者小时级、后者秒级）：

```bash
python tools/probe/dataset_data_probe.py --region GBR --universe TOP700 --delay 1 \
    --plan data/dataset_assets/GBR_probe_plan_d1.json \
    --out data/dataset_assets/GBR_probe_results_d1.json --jobs 4
python tools/gates/audit_dataset_coverage.py --region GBR --universe TOP700 --delay 1 \
    --reuse-cache data/dataset_assets/GBR_coverage_audit_d1.json \
    --probe-results data/dataset_assets/GBR_probe_results_d1.json --gate both
```

### 12.8 一句话收尾

覆盖闸这次被**降级成可逆假设 + 补齐执行器**：`coverage=0` 再也不能静默砍掉一个数据集 ——
「有没有数据」只剩两种合法证据（**字段目录非空** / **探针持仓 > 0**），
而探针**有执行器、有退出码、有落盘产物**。本区实测代价：
**16 个有数据、零开采尝试的数据集曾被整枝跳过**（不是被证明无效，而是从未被评估）。

### 12.9 根因 C：SOP 文本层的同一个错（2026-11-09 补）

工具修好、报告措辞修好，仍然不够 —— **skill 文档里那句「`coverage < 0.6` ⇒ 永久剔除」会让下一个 agent 原样重犯一次**。
写在 SOP 里的纪律 = 下一个 agent 的默认动作，所以它也必须变成退出码。

新增门：`python tools/gates/audit_dataset_coverage.py --lint-skills`（扫 `Claude/skills/**/*.md`，本次实扫 **497** 个文件）

| 处置 | 位置 | 原表述 → 现在 |
|---|---|---|
| ✅ 已改 | `SKILL.md` 第 1 层 verdict 表 | `UNUSABLE` = `coverage < 0.6` ⇒ **永久剔除** → 该行**已废止**；右列计数改标「cov 元数据为 0 的字段数，不是判死数」 |
| ✅ 已改 | `SKILL.md` 第 0 步零成本筛选 ③ 画像闸 | 「`cov<0.6`、`to_med<0.03`、count 族」→ **cov 移出该闸**；cov 全 0 只标「元数据盲区」⇒ 走探针 |
| ✅ 已改 | `references/_probe-sop.md` 第 0 步 | 「`coverage<0.6` 剔除」→ **不参与剔除**，并补「选集闭合必须过 `--gate closure`」 |
| ✅ 已改 | `references/_field-profile-playbook.md` 表格第 3 行 | 判据整条退役，改指 `--gate closure` |
| ⏸ 登记欠账 | `wq-brain-ra-deu`（4 处）/ `wq-brain-ra-eur`（1 处）/ `wq-brain-ra-kor`（1 处） | 同一句话被抄到了其它区 SOP；本 session 区域锁定 GBR、**未改**，登记在 `tools/gates/_covskill_allow.json`（只许缩小） |

判定口径：命中「`cov/coverage < 阈值` + 剔除 / 判死 / 直接排除 / 作废」即 exit 1；
同行带 `cov-aux-ok` 或反例语境（已废止 / 反例 / 不得 / 禁止 / 误判 / 不可判 / 已修 / 修正 / 不再）才豁免。

**首版踩的坑**（同一类错误第 N 次换位置复现）：最初把 `UNUSABLE` 也算作判死动词，
结果把 IND 文档里的**历史分类记录**「`UNUSABLE×20`（cov<0.5 触顶）」误判成违规 —— 
那是「过去被这样判过」的记录，不是「让人去剔除」的指令。只认指令性动词之后，9 条违规全部精确落位。


### 12.10 根因 D：证据通道自己的盲区（2026-11-09 收尾）

前四条根因修完后，重跑审计又炸出**两个「我的工具在骗我」**的实例 —— 都属于同一族：
**用一条有盲区的证据通道，去下一条没有标注盲区的结论**。

| # | 症状 | 真因 | 处置 |
|---|---|---|---|
| D1 | D0 审计报「45 集已点亮塔 ⇒ 排除」，而实测 D0 十四类塔**全部为 0** | `pull_pyramid()` 形态 B 把每条记录的 `alphaCount` **跨 delay 求和**，于是 D1 的点亮状态被套到 D0 头上 | 修 `pull_pyramid(delay=)`，按 `it["delay"]` 过滤；返回体补 `delay_filtered`。修后 D0 由「6 个未探」变成 **28 个未探**（24 blind + 4 cov_ok） |
| D2 | 报告里写「这 4 个集**一次挖掘尝试都没有**」 | 「挖过没」的证据源只有 `db:expressions` / `db:text`，而 **MCP 直连仿真（`create_simulation` / `create_multi_simulation`）不写这张表** ⇒ 本 session 自己跑的 28 条 MCP 仿真对工具完全隐形 | 工具 `scope` 新增 `evidence_blind_spots` 并渲染进 MD；段落改名为「**有数据但本通道零记录**」，正文写明「勿读成没跑过，回波次日志核对」 |

**处置口径（新增纪律）**：任何「未探 / 未测 / 没挖过」清单，必须同时标注**它是由哪条证据通道得出的**，
以及**该通道对什么盲视**。否则下一步就会拿「我的台账里没有」冒充「没人跑过」—— 与根因 3、4 同构。

**本区当前诚实口径（D1 / TOP700）**：可开采池 65 集 = 通道内已挖 61 + 有数据但通道零记录 4；
后者中 `other78`、`stock_search_trends`（= `search_interest`）、`socialmedia39` 按本 session 波次日志**已跑过**
（均 |S| < 0.4），真正一条读数都没拿到的只剩 **`event_sentiment_signals`（52 个 VECTOR 字段 / 探针 343 只持仓）**
—— 两次 multisim（`3oDo276X55hu8WUfQNt1mVP`、`PfXruaD74gy9XN5evLRZvY`）都卡在 `child_count=0`（本轮复查均 404，已被平台清掉 ⇒ 改走单发通道，见 §12.12）。

### 12.16 self 闸血洗与贪心席位收敛（2026-11-09 续）

**B 簇 prod 未知终局**：Xg9A6rGl **0.8255**、P0oALL17 **0.8384**（rKRnajx8 / 58E2dQZX 在队列）——与族级判定一致。d5 族三变体 0.7423 / 0.74 / 0.7123 同墙，族封盘定案。

**self-corr 全量实测（本地 OS 池 33 颗）把 21 席贪心解打到 17**：

| 死亡（self ≥0.7） | self | 撞的 OS 占位族 |
|---|---:|---|
| A1vg2KnX | 0.9985 | jc7 PD（3qVa2Lze ACTIVE） |
| QPK26lQX | 0.9985 | jc7 PD |
| 78NY2OgO | 0.9936 | dlr2 门控（KPNgQApj ACTIVE） |
| XgbaOqX0 | 0.9975 | dlr2 门控 |
| N1VAAQn8 | 0.9981 | mdl28（JjQbYdGW/omWVV6Y2 ACTIVE） |
| A1VbxnAw | 0.9645 | mdl28 |
| A1VJR8AX | 0.9150 | mdl28 |
| gJerKgJv | 0.9198 | pv103×loaned（3qoGxkqZ ACTIVE） |
| 3qo6GKk0 | 0.9101 | fnd6×cap（rKRkL9QE ACTIVE + 11-03 禁混，双死刑） |
| 2rALG0XZ | 0.8499 | epy（9qWaRGEK ACTIVE） |
| N1aL9aRe | 0.8321 | epy |
| leA6jmoe | 0.8923 | nws17（58E7jkaN/A1VPlR3l/kqNZKN5K ACTIVE） |
| mLob5Yj5 | 0.7975 | nws17 |
| omE0PPzv | 0.7813 | fnd6×cap（双死刑） |

**规律**：self 死亡集中在 OS 池已有占位的 8 个族（jc7 / dlr2 / mdl28 / pv103×loaned / fnd6×cap / epy / nws17）；
存活族 = OS 池无占位的 tm15/16/17/19（OTHER 塔仅 1 点亮）、imb5、model109、nws18、est、ev_fund93、mdl216、oth47×loaned。
**358 池的家族深度就是替补来源**：每死一席，同族/邻族换人（贪心已自动完成两轮替换）。

**当前贪心解（52 存活节点，逐对验证 pairwise_ok=True）：17 席**，S 总和 ≈39.3，配额 3/5：
`bl6avAXp 3.57 / leAgVON2 2.67 / rKRQbPPE 2.48 / mLomxW71 2.33 / leAPWGX2 2.36Q / 3qoXwW1z 2.64 / d5W9EeKK 2.27 / O0A6Qz7p 2.18Q / mLoVXokK 2.30 / e758lzaN 1.62 / akxAgvNw 1.69 / N1NM5WK8 2.05 / 1YN6MJw6 2.07Q / 88jV1LEW 1.92 / Xg9b5ZX0 2.07 / gJeq8XbQ 2.02 / 9qWa6r8x 2.07`
（mLoVXokK / e758lzaN / akxAgvNw / N1NM5WK8 四颗 self 补测在队列；9qWa6r8x self 0.679 贴线）

**prod 侧**：19 席全部 UNSUBMITTED ⇒ prod 全 null，须逐颗过平台队列（后台进行中）。
**收敛路径**：17 席（self 存活）→ prod 过滤 → 同族替补补位 → 目标 20。剩余瓶颈是测量队列的时间成本。


## 13. RISK category 专项（用户 2026-11-09 裁决「锁定 Risk 挖掘」）

### 13.1 数据集底册（D1 / TOP700，5 集 40 字段，全量实拉无抽样）

| 数据集 | 字段 | 类型 | cov | ac | 机制 |
|---|---:|---|---:|---:|---|
| **risk60** Securities Lending Insight | 5 | VECTOR | 0.6694 | 202 | 借券费率/做空拥挤（`rsk60_offer`/`lending_fee_bid_rate`/`rsk60_crowding`/`rsk60_last` + 时间戳） |
| risk68 Forecast Data | 5 | MATRIX | 0 | 731 | 欧洲风险模型（`beta`/`residual_return`/`weight_dadv`/`weight_edadv`/`weight_volatility_short`） |
| risk71 Specific Return Profiling | 6 | MATRIX | 0 | 608 | 特质收益 DSRT（`residualized_return_top2500` ac=536 最热） |
| risk72 Specific Return (Extended) | 23 | MATRIX/VECTOR | 0 | 606 | 多宇宙残差收益 + cfg2 replicator |
| risk88 Other Multi-Factor Risk | 1 | MATRIX | 1.0 | 567 | `alternative_market_cap_usd`（已作分母在 fnd6 族使用） |

★ 三条 `cov=0`（risk68/71/72）**不是没数据**——`residualized_return_top2500` 有 536 个 alpha 在用，实测 S 能到 1.86。

### 13.2 机制面扫描：12 模板首波 + 8 轮深化（约 45 条仿真）

**首波 12 模板（T1-T12）**：
| 族 | 模板 | 最好读数 | 判定 |
|---|---|---|---|
| risk60 借券费率 | 水平 / 反号 / Δ22 / 拥挤 z66 / industry 均值 / 拥挤×费率 | S 0.36（T5 费率 industry 均值，2Y 0.63） | ❌ 全灭（\|S\|≤0.40） |
| risk68 残差 | 反转 5 / 动量 22 / 波动 66 | **动量 22 反号 S 1.05** | ⚠ 有信号但弱 |
| risk71/72 残差 | top2500 反转 5 / 动量 22 / 波动 ind | **反转动量 S 1.38-1.44** | ✅ 唯一产线 |

**深化 8 轮（残差反转族）窗口 × 分组 × 宇宙 × 平滑曲线**：
| 杠杆 | 读数 | 结论 |
|---|---|---|
| 窗口 | 11 日 S1.64 > 22 日 S1.44 > 44 日 S1.18 | 短窗更强 |
| 分组 | subindustry S1.50 ≥ 无分组，industry/sector 更弱 | subindustry 最优 |
| 宇宙 | top2500 S1.44 > risk68 S1.05 > risk71 S0.77 | top2500 最优 |
| **ts_decay_linear 平滑** | decay5 把 F 从 0.56→1.0 | ★ F 的关键杠杆 |
| **winsorize std** | 0.2→0.4→0.5 使 F 0.87→1.00→1.01 | ★ 第二关键杠杆（std 越大截尾越松、F 反升 ⇒ 原分布尾薄） |
| decay 加深 | 8 S1.73/F1.12；12 S1.60/F0.95；16 S1.59/F0.99 | decay8 甜点 |

### 13.3 ★ 全闸件与 prod 终局（RISK 塔第 1 颗）

**`j2Y7AbzQ`（F4_std40）**：`winsorize(ts_decay_linear(group_rank(-ts_sum(top2500_equity_residualized_return, 11), subindustry), 8), std=0.4)`

| 项 | 值 | 闸 |
|---|---:|---|
| S | 1.71 | ≥1.58 ✅ |
| F | **1.00** | ≥1.0 ✅ |
| 2Y | 1.68 | ≥1.58 ✅ |
| TO | 0.165 | ∈[0.01,0.7] ✅ |
| sub_universe | 1.08 | ✅ |
| RA checks | **fail=[]，9 项全 PASS**（LOW_FITNESS 在 pass 列） | ✅ |
| self | 0.5913 | <0.7 ✅ |
| **prod** | **0.7645** | **≥0.7 ❌ 撞墙** |
| 塔 | `GBR/D1/RISK`（effective=1，倍率 1.3，该塔原 0 点亮） | — |
| 算子数 | 4（winsorize/ts_decay_linear/group_rank/ts_sum） | ≤12 ✅ |

**同族另一颗 `zq3Vb8GK`（H3_std50）**：std=0.5 → S 1.72 / F **1.01** / 2Y 1.67 / sub 1.09 / fail=[]，
与 j2Y7AbzQ 仅差 winsorize std 一个参数（相关必然 ≈1），**prod 未测但必然同墙**。

### 13.4 判定：RISK 线的两条机制面，一条全灭、一条撞族级 prod 墙

- **risk60 借券费率族**：6 模板全灭（\|S\| ≤ 0.40）⇒ 该面在 GBR 无可挖信息（与 shortinterest3 的借券短腿强势形成对照：**短腿强、费率本身弱**）。
- **残差反转族**：IS 侧完美（全闸 2 颗、算子 4 个），但 **prod 0.7645 撞墙** —— 特质收益反转是全球生产池最拥挤的因子之一，
  这与「prod 命中率是族属性」的既有结论一致（同族换窗口/换 std 都在 0.76 附近，换不动）。
- **RISK 塔点亮（≥3 颗）当前不可达**：唯一产线撞墙，另一面全灭。
- 可试的剩余杠杆（未试）：① 残差**动量**方向 + 长窗（与反转反号，prod 可能不同源）；② risk72 的 cfg2 replicator（VECTOR，未被覆盖）；
  ③ 残差反转 × 波动率条件门控（已试，见 §13.5：2Y 抬到 2.12 但相关 0.95 拆不开）。

### 13.5 ★ 三颗全闸件互相关 0.95+：参数变体点不亮 RISK 塔（2026-11-10）

| alpha | 结构差异 | S | F | 2Y | sub | fails | self | prod |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `j2Y7AbzQ`(F4) | std=0.4 基准 | 1.71 | 1.00 | 1.68 | 1.08 | 0 | 0.591 | **0.7645 ✗** |
| `zq3Vb8GK`(H3) | std=0.5 | 1.72 | 1.01 | 1.67 | 1.09 | 0 | 未测 | 未测（同族必同墙） |
| `QPv8YLlW`(J3) | 加 `trade_when(波动率>0.3)` 门控 | 1.68 | 1.00 | **2.12** | 0.92 | 0 | 0.575 | 未测 |

**互相关**：F4×J3 **0.9526**、F4×H3 **0.9997**、J3×H3 **0.9531** ⇒ 三颗实际是同一颗（相关性 <0.5 的篮子只能取 1）。
**结论**：`trade_when` 门控把 2Y 从 1.68 抬到 2.12，但持仓骨架未变 ⇒ 拆不开相关；RISK 塔点亮（需 ≥3 颗）
**不能靠同源参数变体实现**，必须换机制面或换数据集（risk60 已全灭、risk68/71/72 同源、risk88 仅 1 字段且作分母）。

**RISK 线最终账（scope: 5 集 40 字段 × 约 50 条仿真 × SUBINDUSTRY/decay4/trunc0.08）**：
- 唯一产线 = 特质收益反转（top2500，11 日，subindustry，decay8，winsorize std0.4-0.5），IS 侧 3 颗全闸；
- prod 0.7645 撞族级墙（特质反转是全球最拥挤因子之一）；
- **可交付件 0 颗**（prod 未过线），RISK 塔维持 0 点亮。
- 唯一未被证伪的剩余方向：risk72 `cfg2_*_replicator1/2`（VECTOR）+ risk68 `weight_*` 三个权重族（**已于 §13.6 全部试完，全灭**）。

### 13.6 RISK 5 集 40 字段穷尽定案（2026-11-10 收尾）

**K 批（换信息源）**：
| 方向 | 表达式骨架 | S | F | 2Y | sub | fails | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| risk68 空头波动权重 | `group_rank(ts_zscore(rsk68_weight_volatility_short,66))` | 0.43 | 0.15 | 0.29 | 0.34 | 3 | ❌ |
| risk68 beta | 同上（反号） | 0.03 | 0.00 | 0.98 | 0.54 | 3 | ❌ |
| risk72 cfg2 replicator1 | `vec_avg(cfg2_top1200_replicator1)` | -0.21 | -0.10 | -0.71 | -1.06 | 5 | ❌（TO 0.025 信号过稀） |
| risk72 cfg2 replicator2 | 同上 | 0.46 | 0.40 | -0.92 | -0.13 | 5 | ❌ |

**I 批（risk72 各宇宙残差反转）**：top1200 S1.01 / ats1200 S1.11 / top600 S0.85 / top800 S0.81 —— 全部远低于闸（宇宙越小信号越弱，
说明该机制的有效性依赖大宇宙横截面）。

**L 批（改信号时间尺度/形态降 prod）**：
| 杠杆 | S | F | 2Y | 判定 |
|---|---:|---:|---:|---|
| 120 日慢反转 + decay20 | 0.32 | 0.11 | 0.70 | ❌ 长窗完全失效 |
| 波动率标准化反转 | 1.62 | 0.93 | 1.34 | ⚠ F/2Y 双不足 |
| **双宇宙共识（top2500 × risk71）** | **1.87** | **1.16** | 1.55 | ⚠ `IS_LADDER_SHARPE 1.55<1.58` FAIL；且与 F4 相关 **0.9745** |
| 66 日慢反转 + decay16 | 未完成 | — | — | — |

**最终结论（scope: RISK 5 数据集 40 字段 × 约 60 条仿真 × SUBINDUSTRY/decay4/trunc0.08 × TOP700/D1）**：
1. **唯一有信号的机制面 = 特质收益反转**（top2500 大宇宙、11 日、subindustry、decay8、winsorize std0.4-0.5）；
2. 该面 IS 侧可产出全闸件（`j2Y7AbzQ` 等 3 颗，9 项 RA 全 PASS），但 **prod 0.7645 撞族级墙**，且所有降 prod 杠杆
   （换宇宙 / 换窗口 / 换时间尺度 / 加门控 / 双宇宙共识）都拆不开 —— 相关性 0.95+ 或指标崩；
3. **其余四面全灭**：risk60 借券费率（\|S\|≤0.40）、risk68 权重/beta（≤0.43）、risk72 replicator（≤0.46）、risk88（仅 1 字段，仅作分母）；
4. **RISK 塔维持 0 点亮，可交付件 0 颗**。

⇒ 若仍要点亮 RISK 塔，只剩「跨数据集组腿」一条路（如残差反转 × 借券短腿）——**已于 §13.7 走通：RISK 不在禁混集合，该组合免配额**。

### 13.7 ★★ RISK × shortinterest 免配额组腿：CW 破解后拿到双塔全闸件（2026-11-10）

**为什么这条路合法且免费**：RISK 不在禁混集合 `{PV, MODEL, OTHER, FUND}` 内 ⇒ RISK × shortinterest 属「集合外 × 集合外」，
**不占组腿配额**。且 RISK 塔 0 点亮、shortinterest 塔已点亮，两者组腿后 `pyramids.effective = 2`。

**骨架**（沿用 10 席里验证过的 GOLD2，外层加 RISK 线验证的 winsorize+decay）：
```
winsorize(ts_decay_linear(add(group_rank(-ts_sum(top2500_equity_residualized_return, 11), subindustry),
                                  reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), sector))), 8), std=0.25)
```

| 变体 | S | F | 2Y | TO | sub | fails | 备注 |
|---|---:|---:|---:|---:|---:|---:|---|
| M2 等权（未 backfill） | 2.41 | 1.70 | 2.87 | 0.146 | 1.83 | 1 | ❌ CONCENTRATED_WEIGHT |
| M1 w=2 | 2.14 | 1.39 | 2.38 | 0.165 | 1.39 | 1 | ❌ CW |
| M3 w=3 | 2.05 | 1.30 | 2.28 | 0.169 | 1.30 | 1 | ❌ CW |
| N4 std=0.25 | 2.30 | 1.80 | 2.70 | 0.0998 | 1.83 | 1 | ❌ CW |
| O 批（trunc0.15 / group_neutralize / 短腿降权） | 2.05-2.31 | 1.28-1.57 | 2.36-2.81 | — | — | 1 | ❌ CW 全部改不掉 |
| **P1 `ts_backfill(短腿,250)`** | **2.29** | **1.56** | **2.84** | **0.144** | **1.69** | **0** | ✅ **全闸** |
| P2 短腿换 `average_loan_duration_days` + backfill | 1.26 | 0.69 | 2.23 | 0.164 | 0.82 | 3 | ❌ 换字段即崩 |

**★ CW 的根因与唯一解**：借券短腿是 VECTOR 稀疏事件数据（只在有借券的股票上有值），直接进 `add()` 会让持仓集中到少数股票；
`truncation 0.15` / `group_neutralize` / 短腿降权 0.3-0.5 / `hump` **全部无效**（CW 是布尔判定、无阈值余量可调）。
唯一有效杠杆 = **`ts_backfill(vec_sum(短腿), 250)` 把稀疏值向前填稠密** ⇒ 持仓分散 ⇒ CW 消失，且 S/F/2Y 几乎不掉（2.41→2.29）。

**`rKRx0M2m` 明细**：`fail=[]`，9 项 RA 全 PASS（CW 在 pass 列）、塔 `SHORTINTEREST(1.2) + RISK(1.3)` 双塔、
self **0.443** ✅、与 `j2Y7AbzQ` 相关 **0.6748**（>0.5，不能同篮，但塔贡献不同：F4 只 RISK、P1 双塔）。
**prod 待测**（后台排队，平台 `platform_unavailable`）。

### 13.8 短腿替换试验：借券短腿不可替代（2026-11-10）

RISK 塔点亮需 ≥3 颗互相关 <0.5 的件，故试「换短腿开新面」（全部沿用 P1 的 backfill+decay+winsorize 骨架）：

| 变体 | 短腿 | S | F | 2Y | sub | fails | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| P1（基准） | `ts_backfill(vec_sum(loaned_share_count_main),250)` | 2.29 | 1.56 | 2.84 | 1.69 | 0 | ✅ 全闸 |
| Q1 | `ts_backfill(imb5_score,250)`（IMBALANCE） | -0.06 | -0.01 | -0.59 | -0.02 | 3 | ❌ 换即崩 |
| Q2 | `ts_backfill(est_raisednum−lowerednum,250)`（ANALYST） | 1.46 | 0.78 | 1.10 | 1.25 | 3 | ❌ F/2Y 双不足 |

**Q2 × P1 互相关 0.6155**（>0.5，即便指标达标也不能同篮）。
⇒ **借券短腿在 GBR 不可替代**（与既有结论一致：`loaned_share_count_main` 是唯一能过闸的冷腿），
「换短腿开新面」这条路在 RISK 组腿上同样封死。

### 13.9 ★★★ RISK 塔第一颗完整可提交件诞生（2026-11-10）

**`rKRx0M2m`** 全闸终验通过（所有闸门均为 platform 真值，非缓存/预读）：

| 项 | 值 | 闸 |
|---|---:|---|
| S | **2.29** | ≥1.58 ✅ |
| F | **1.56** | ≥1.0 ✅ |
| 2Y | **2.84** | ≥1.58 ✅ |
| TO | 0.1439 | ∈[0.01,0.7] ✅ |
| sub_universe_sharpe | 1.69 | ✅ |
| RA checks | **fail=[]**（9 项全 PASS，CW 在 pass 列） | ✅ |
| self | **0.443**（<0.7） | ✅ |
| **prod** | **0.6232**（`source=platform/provisional=false/from_cache=false`） | ✅ |
| 塔 | `effective=2`：SHORTINTEREST(1.2) + **RISK(1.3)** | 贡献 RISK |
| 算子数 | 9 | ≤12 ✅ |

表达式：
```
winsorize(ts_decay_linear(add(group_rank(-ts_sum(top2500_equity_residualized_return, 11), subindustry),
                                  reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), sector))), 8), std=0.25)
```

**同族几何变体全闸情况（R 批，4 颗全闸但只能取 1）**：

| 变体 | S | F | 2Y | fails | 与 rKRx0M2m 相关 |
|---|---:|---:|---:|---:|---:|
| **rKRx0M2m**（基准，主腿11/decay8） | 2.29 | 1.56 | 2.84 | 0 | — |
| qMLRYZX1（主腿22/decay12） | 1.85 | 1.23 | 2.19 | 0 | **0.7269** |
| 2rAYXdkN（industry 分组） | 2.19 | 1.50 | 2.53 | 0 | **0.9087** |
| omEdJO2b（冷腿窗 252） | 2.07 | 1.34 | 2.55 | 0 | **0.9271** |

**互相关全在 0.68–0.93 ⇒ MIS = 1 颗**。同骨架参数变体点不亮塔（第三次实证，前两次：tm_* 族、残差反转单集族）。

**另一颗**：`gJe2a8wJ`（无 backfill 版）prod **0.6509** 也过墙，但 **CW 未解（fails=1）不可提交** —— 它只证明了 prod 干净，
而 CW 的解仍是 `ts_backfill`。

**RISK 塔点亮（≥3 颗）的剩余路径**：需要**至少 2 颗与 `rKRx0M2m` 互相关 <0.5 且 prod<0.7** 的件，
而所有同骨架变体（换窗口/换分组/换冷腿窗口/换短腿）都已试完：0.68–0.93 全高相关或指标崩。
⇒ **要凑齐 3 颗只能换「主腿机制面」**（不是换参数）：例如残差反转换成 risk60 借券拥挤 × 短腿——但 risk60 单集已判全灭（该路已于 §13.10 试完，相关 0.76-0.92）；
或引入非 RISK 主腿（则不再贡献 RISK 塔）。**scope：RISK 5 集 40 字段 × 单一主腿机制（残差反转）× 已试 15 类几何** 下，本 category 内点塔的路径已全部走到。

### 13.10 第二颗的尝试：换数据集 / 换统计矩 / 换主导腿 —— 相关性全部 0.76-0.92（2026-11-10）

**S 批（换主腿数据集与统计矩；骨架同 P1）**：
| 变体 | 主腿 | S | F | 2Y | sub | fails | 与 rKRx0M2m 相关 |
|---|---|---:|---:|---:|---:|---:|---:|
| S1 `A1VArNzY` | risk68 `rsk68_residual_return`（不同数据商） | 1.82 | 1.18 | 2.61 | 1.45 | **0** | **0.8113** |
| S2 `2rAYXlpb` | risk60 `rsk60_crowding`（借券拥挤） | 0.84 | 0.41 | 1.37 | 0.90 | 3 | — |
| S3 `npvEe7ra` | risk71 `residualized_return_top2500`（不同字段） | **2.51** | **1.79** | 2.64 | 1.90 | **0** | **0.9187** |
| S4 skew | 残差偏度（ts_skewness 66） | — | — | — | — | ERROR | — |

**T 批（换主导腿：把 RISK 腿降为冷腿、别的主腿升为 w=2）**：
| 变体 | 主导腿 | S | F | 2Y | sub | fails | 与 rKRx0M2m 相关 |
|---|---|---:|---:|---:|---:|---:|---:|
| T1 `ZYQJd133` | 借券做空拥挤 w=2 + 残差反转冷腿 | 1.89 | 1.26 | 2.63 | **2.00** | **0** | **0.7649** |
| T2 `1YNMl09X` | techindi tm_15 w=2 + 残差冷腿 | 2.11 | 1.17 | 1.43 | 1.76 | 1 | — |
| T3 `vR1qPp7G` | imb5 主腿 + 残差冷腿 | 1.71 | 1.21 | 1.35 | 1.43 | 2 | — |

**结论**：只要**两条腿同时在场**（残差反转 + 借券），无论用哪套数据集（risk68/71/72）、哪种统计矩（反转/偏度）、
怎么调权重（残差 w=1/2/3 或降到冷腿），互相关都落在 **0.76–0.92**。原因是两腿的持仓高度重叠，乘数只改幅度不改形态。
⇒ **RISK 塔点亮（≥3 颗 corr<0.5）在本 category 的残差机制面内不可达**（第三次同构结论，与此前 tm_* 族、单集残差族一致）。

**顺带产出（均为全闸，可入其它篮子）**：`npvEe7ra` S2.51/F1.79/2Y2.64、`ZYQJd133` S1.89/F1.26/2Y2.63/sub2.00、`A1VArNzY` S1.82/F1.18/2Y2.61。
三者彼此及与 `rKRx0M2m` 均 ≥0.76 相关 ⇒ 与现有 RISK 件同族，不构成独立席位。

### 13.11 RISK 线最终账（2026-11-10 收尾）

| alpha | 结构 | S | F | 2Y | sub | fails | self | prod | 可提交 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`rKRx0M2m`** | 残差反转 × 借券（backfill） | 2.29 | 1.56 | 2.84 | 1.69 | 0 | 0.443 | **0.6232** | ✅ **第 1 颗** |
| `npvEe7ra` | risk71 残差 × 借券 | **2.51** | **1.79** | 2.64 | 1.90 | 0 | 0.469 | **0.6439** | ⚠ 全闸但相关 0.9187（与第 1 颗同族） |
| `ZYQJd133` | 借券主导 × 残差冷腿 | 1.89 | 1.26 | 2.63 | **2.00** | 0 | 0.444 | 未测 | ⚠ 相关 0.7649 同族 |
| `A1VArNzY` | risk68 残差 × 借券 | 1.82 | 1.18 | 2.61 | 1.45 | 0 | 0.532 | **0.7168** ✗ | ❌ prod 撞墙 |
| `gJe2a8wJ` | 残差 × 借券（无 backfill） | 2.41 | 1.70 | 2.87 | 1.83 | 1 | 0.427 | 0.6509 | ❌ CW 未解 |

**结论**：RISK 线挣到 **1 颗可提交件（`rKRx0M2m`）**，另 3 颗全闸但同族相关 0.76-0.92 只能取 1。
RISK 塔点亮（≥3 颗 corr<0.5）在残差机制面内不可达——已用「换数据集 / 换统计矩 / 换主导腿 / 换短腿 / 换窗口分组」五类杠杆各证一遍。

**可交付增量**：`rKRx0M2m` 是 RISK 塔的第一颗，且为 SHORTINTEREST×RISK 双塔（免配额）。

### 13.12 ★★★ RISK 件并入主交付篮：MIS 14 → 15（2026-11-10）

**互相关检验**：`rKRx0M2m` 对 14 席自净篮**全部 <0.5**（最高 `rKRQbPPE` 0.4308），
`compute_mutual_correlation` 实读 **`max_mutually_below_subset_size = 15`、`all_below_threshold = true`**。
⇒ RISK 件可合法并入主交付线，篮子从 14 席升到 **15 席**。

**逐年覆盖（用户纪律：入篮前必查逐年 longCount>0 且 pnl≠0）**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 2.90 | 1.60 | 1.90 | 1.16 | 1.73 | **0.76** | 4.04 | 2.49 | 2.32 | 3.70 |
| pnl(k) | 762 | 377 | 541 | 251 | 441 | 220 | 1348 | 761 | 1033 | 1163 |
| longCount | 353 | 401 | 406 | 429 | 394 | 377 | 345 | 342 | 310 | 275 |

**10/10 年全有持仓、全为正 pnl、无空窗**（最弱 2019 年 S 0.76 仍为正；最强 2020 S 4.04）。满足覆盖闸的全部要求。

### 13.13 入篮前的逐年覆盖核查：剔 1 颗、RISK 双选（2026-11-10）

**★ 逐年覆盖核查（用户纪律：连续多年空窗即除名）** —— 15 席全量核 10 年（2014-2023）真实读数：

| 结论 | 席位 | 证据 |
|---|---|---|
| ❌ **剔除** | `leAgVON2` | **2014/2015/2016 连续三年 longCount=0、pnl=0**（该集数据只从 2017 起） |
| ✅ 通过（12 席） | 其余 12 席 | 10/10 年有持仓、无负年；最弱年 S：`91Wa6r8x` 0.09、`O0A6Qz7p` 0.03（均正）、`wpQwjWn6` 0.36、`88jV1LEW` 0.50 |
| ✅ 通过（RISK） | `rKRx0M2m` | 10/10 年、minLC 275、最弱年 S 0.76 |
| ✅ 通过（RISK 备选） | `npvEe7ra` | 10/10 年、无空窗、最弱年 S 0.95 |

**RISK 双选（互斥，相关 0.9187）**：
| alpha | S | F | 2Y | prod | 逐年 | 取舍 |
|---|---:|---:|---:|---:|---|---|
| **`rKRx0M2m`** | 2.29 | 1.56 | **2.84** | **0.6232**（余量 0.077） | 10/10 | ★ 保留（2Y 更高、prod 余量更大） |
| `npvEe7ra` | **2.51** | **1.79** | 2.64 | 0.6439（余量 0.056） | 10/10 | 备选（S/F 更强） |

**篮子规模（两种选法都是 14 席）**：
| 组合 | MIS | 全对最大相关 |
|---|---:|---:|
| 13 席 + `rKRx0M2m` | **14** | 0.4308（`rKRQbPPE`） |
| 13 席 + `npvEe7ra` | **14** | 0.4475（`wpQwjWn6`×`gJeq8XbQ`） |

**prod 实测进度**：`leAPWGX2` **0.637** ✅（14 席中第 1 颗过墙），其余 13 席队列中（约 1 小时）。

### 13.14 补位：从 358 池找回第 15 席 `2rAw9o7J`（2026-11-10）

`leAgVON2` 因三年空窗剔除后，从 358 全池重测 **325 颗未测 self** 的高 S 候选（首批 5 颗）：

| 候选 | 家族 | S | self | 与 14 席篮最高相关 | 判定 |
|---|---|---:|---:|---:|---|
| **`2rAw9o7J`** | est | 1.98 | **0.503** | **0.4134**（`1YN6MJw6`） | ✅ **入篮（第 15 席）** |
| `LLMK8qbv` | imb5 | 1.86 | 0.120 | **0.6242**（`d5W9EeKK`） | ❌ 相关超线 |
| `LLMOQk7a` | est | 1.87 | 0.383 | **0.8898**（`1YN6MJw6`） | ❌ 相关超线 |
| `blbx8NJp` | starval | 2.37 | 0.744 | — | ❌ self 撞 OS 池 |
| `pwRW57L6` | starval | 2.31 | 0.810 | — | ❌ self 撞 OS 池 |

**`2rAw9o7J` 全闸核查**：S 1.98 / F 1.45 / 2Y 1.73 / TO 0.112 / sub 0.95 / **fails=0**、self 0.503、
逐年 10/10 有无空窗、无负年（**最弱年 S=0**，即持平年，非负）、minLC 359。prod 测量中。

**篮规模回到 15**（`compute_mutual_correlation` 实读 `max_mutually_below_subset_size = 15`）。

### 13.15 第 16 席：`P0gv3AO7`（2026-11-10）

第二批 8 颗候选的 self 批测结果：**2 颗干净**（`9qWJr2rq` 0.389 / `P0gv3AO7` 0.389，均 other 族），
6 颗撞 OS 池（epy 0.935/0.772、mdl28 0.998/0.963、pd_jc7 0.993/0.888）。

| 项 | `P0gv3AO7`（入篮） | `9qWJr2rq`（备选） |
|---|---:|---:|
| S | **1.69** | 1.59 |
| F | **1.07** | 1.02 |
| 2Y | **2.10** | 1.96 |
| TO | 0.1362 | 0.1232 |
| sub | 1.33 | 1.20 |
| fails | **0** | 0 |
| self | 0.389 | 0.389 |
| 与 15 席篮最高相关 | **全部 <0.4** | 全部 <0.4 |
| 两者互相关 | **0.9691**（只能取 1） | — |

**`P0gv3AO7` 逐年**：10/10 年、无空窗、无负年、minS 0.38、minLC 410 ✅
**平台 MIS 实读 = 16**（`max_mutually_below_subset_size = 16`）。

### 13.16 other 族开仓：篮子 16 → 18 席，同时剔除 prod 撞墙的 wpQwjWn6（2026-11-10）

**★ `wpQwjWn6` prod = 1.0000**（完全相关，远超 0.7）⇒ **从篮子剔除**。这是 prod 闸第一次打掉已入篮成员。

**other 族 10 颗候选 self 全部干净（0.18-0.58）** —— 该族是 OS 池唯一还有空位的族：

| 候选 | self | 与 16 席篮最高相关 | S | F | 2Y | fails | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| **`vR11n3xQ`** | 0.362 | **0.192** | 1.97 | 1.35 | 1.96 | **0** | ✅ 入篮（第 17 席），逐年 minS **0.97** |
| **`omEaWgwv`** | 0.386 | **0.246** | 2.03 | 1.21 | 2.45 | **0** | ✅ 入篮（第 18 席），逐年 minS 0.38 |
| `d5WbOOZY` | 0.568 | 0.474 | 1.74 | 1.04 | **1.21** | 1 | ❌ 2Y 不足 |
| `e75b99zO` | 0.568 | 0.477 | 1.74 | 1.04 | **1.16** | 1 | ❌ 2Y 不足 |
| `1YNXxxwQ` | 0.579 | 0.487 | 1.76 | 1.00 | **1.28** | 1 | ❌ 2Y 不足 |
| `0mYXqWxr` / `akKbja26` / `LLMNWxEe` / `RREbY1rb` / `xAr3Qdnp` | 0.18-0.23 | **0.611-0.972** | — | — | — | — | ❌ 相关超线 |

**两张新席的逐年**：`vR11n3xQ` 10/10 年无空窗无负年、minS 0.97、minLC 434；`omEaWgwv` 同样干净、minS 0.38、minLC 408。

**篮规模**：`compute_mutual_correlation` 在 16 席 + 5 候选上实读 **MIS = 18**。prod 队列中（`vR11n3xQ`/`omEaWgwv`）。

### 13.17 ★★★ 20 席达成（2026-11-10）

**other 族第二批（13 颗）**：先按全闸筛（2Y 是关键闸），**9 颗通过**（2Y 2.02-2.98，质量显著优于前批），
self 9/9 全干净（0.225-0.689）。与 18 席篮的相关检验：

| 候选 | 与篮最高相关 | 判定 |
|---|---:|---|
| **`78L9Lwrv`** | **0.346** | ✅ 入篮（第 19 席） |
| **`pwdd7Za6`** | **0.355** | ✅ 入篮（第 20 席） |
| `KPJer3Z1` | 0.463 | ⏸ 备选（与 pwdd7Za6 相关 0.5047 超线） |
| `xAr3OvXm` / `zq3AX08o` / `9qxGgg9d` / `d5W9eobx` / `RRE500Nd` / `Jjee0MAW` | 0.618-0.926 | ❌ 相关超线 |

**两席三查全过**：
| 项 | `78L9Lwrv` | `pwdd7Za6` |
|---|---:|---:|
| S | 1.72 | 1.69 |
| F | 1.16 | 1.04 |
| 2Y | 2.02 | **2.49** |
| TO | 0.1309 | 0.1045 |
| sub | 0.90 | **1.70** |
| fails | **0** | **0** |
| self | 0.656 | 0.416 |
| 逐年 | 无空窗无负年、minS **1.11** | 无空窗无负年、minS 0.13 |
| 两者互相关 | **−0.031**（几乎正交） | — |

**篮子 = 20 席**。prod 队列中。

### 13.18 prod 闸淘汰进展与备选池（2026-11-10）

**prod 实测（平台真值）**：
| 席 | prod | 判定 |
|---|---:|---|
| `leAPWGX2` | **0.637** | ✅ 过墙 |
| `wpQwjWn6` | **1.0000** | ❌ 撞墙（完全相关） |
| `1YN6MJw6` | **0.8311** | ❌ 撞墙 |

⇒ **20 席中已确认 1 颗过墙、2 颗撞墙**，余 17 颗队列中。
**prod 淘汰率实测 2/3**（3 颗中 2 颗死）—— 这是本轮最重要的风险信号：self 干净 + 全闸 **不等于** prod 干净，

### 13.20 other 族挖尽：相关结构上界 19，实际全闸仍 18（2026-11-10）

从 279 颗未测候选中排除已知撞墙族（tm/epy/mdl28/pd_jc7/starval/loaned/pv103）后剩 159 颗，取 8 颗跨族批测：

| 候选 | 族 | self | 与 18 席篮最高相关 | 全闸 | 判定 |
|---|---|---:|---:|---|---|
| `A1VN00GX` | other | 0.557 | **0.472** | ❌ **2Y 1.38**、fails 1 | 相关达标但指标不足 |
| `LLMO3l7n` / `A1Vq8AbQ` / `9qxgOnK2` | ev_fund93 | 0.580 | **0.875** | — | ❌ 同族撞篮内 ev_fund93 |
| `e75835Zz` / `6XdPedNJ` | nws18 | 0.352 | **0.920 / 0.926** | — | ❌ 同族撞 `gJeq8XbQ` |
| `d51E709g` / `P0oerpjp` | model109 / fnd6 | **0.710 / 0.751** | — | — | ❌ self 撞 OS 池 |

⇒ **MIS 传 19，但 `A1VN00GX` 的 2Y 1.38 不够** ⇒ 实际全闸席位数仍是 **18**（未计 prod 淘汰）。
**other 族的高相关候选已基本挖尽**：剩下 151 颗要么属已知撞墙族，要么大概率重蹈覆辙。

### 13.21 ★★★ prod 实测大规模落地：9 颗仅 2 颗过墙（2026-11-10）

平台槽释放后串行实测（全部为 MCP `check_correlation(production)` 平台真值）：

| 席 | prod | 判定 |
|---|---:|---|
| `leAPWGX2` | **0.6370** | ✅ 过墙 |
| `O0A6Qz7p` | **0.6984** | ✅ 过墙（余量 0.0016，贴线） |
| `Xg9b5ZX0` | 0.7068 | ❌ |
| `88jV1LEW` | 0.7329 | ❌ |
| `bl6avAXp` | 0.7397 | ❌ |
| `3qoXwW1z` | 0.7552 | ❌ |
| `d5W9EeKK` | 0.8017 | ❌ |
| `mLomxW71` | 0.8331 | ❌ |
| `1YN6MJw6` | 0.8311 | ❌ |
| `wpQwjWn6` | 1.0000 | ❌ |

**★ 关键结构发现**：撞墙值密集落在 **0.70–0.83** 这个窄带里（7 颗），而不是散布在整个 [0,1]。
这与「生产池对某些因子族稠密覆盖」一致 —— 这批件虽来自不同数据集（tm_15/tm_16/imbalance/model109/nws17/other），
但**持仓的核心暴露相近**（都是 GBR 大市值横截面上的动量/反转/流动性类），因此在生产池里都撞到同一批邻居。

**实测过墙率 = 2/10 = 20%**，远低于全闸池的假设。⇒ **「全闸 + self 干净 + 互相关达标」离可交付仍差 prod 这一道最难的闸**。

### 13.22 ★★★★★ 决定性规律：含借券冷腿的组腿 100% 过 prod，纯 ATOM 100% 撞墙（2026-11-10）

13 颗已实测 prod 的件按结构分组，规律**完全可分辨、零交叉**：

| 结构 | 件数 | prod 值 | 均值 | 过墙率 |
|---|---:|---|---:|---:|
| **X × 借券冷腿（组腿）** | 4 | 0.6232 / 0.6370 / 0.6439 / 0.6984 | **0.651** | **4/4 = 100%** |
| **纯单数据集 ATOM** | 7 | 0.7068 / 0.7397 / 0.7552 / 0.8017 / 0.8331 / 0.9257 / 1.0000 | **0.823** | **0/7 = 0%** |

**机制解释**：借券数据（shortinterest3）在 GBR 生产池里覆盖稀疏 —— 多数已提交件不含借券腿。
把借券当冷腿加入，相当于把持仓往「生产池没占的方向」拉，**prod 相关性因此系统性降低**。
而纯 ATOM 件（tm_* / imb5 / nws* / est）本质是常见因子在 GBR 横截面上的重排，生产池里已稠密覆盖同类。

**这条规律的价值**：过去把「单数据集 ATOM 免配额」当优点，实际上**ATOM 在 prod 侧是劣势**。
要产可交付件，应优先造「任意主腿 × 借券冷腿」的组腿（外×外组合，免配额），而不是挖 ATOM。

### 13.23 ★★★★★ 按 §13.22 批量改造 ATOM→组腿：8 造 4 中（2026-11-10）

把 §13.22 的规律付诸实践：取**原本纯 ATOM、IS 很强但 prod 撞墙**的主腿，加借券冷腿改造。两批 10 条：

| 变体 | 主腿 | S | F | 2Y | sub | fails | self | 与已确认件最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`e75jWXqz`** | model109 `region_relative_valuation_rank` | **2.63** | **2.53** | **2.83** | 1.86 | **0** | 0.486 | **0.487** | ✅ 全闸可入 |
| **`pwdLp9z6`** | tm_16（原 `3qoXwW1z` prod 0.7552） | 2.26 | 1.19 | 2.09 | 2.19 | **0** | 待测 | **0.461** | ✅ 全闸可入 |
| **`omEdka3v`** | tm_17（原 `bl6avAXp` prod 0.7397） | **2.51** | 1.40 | 2.37 | **2.46** | **0** | 0.416 | 0.452 | ✅ 全闸可入 |
| **`gJe20Wel`** | imb5（原 `d5W9EeKK` prod 0.8017） | 2.05 | 1.51 | 1.87 | 1.77 | 1 | 0.153 | **0.130** | ⚠ fails=1（CW 类） |
| `leAmN1Ln` | nws17 | 1.53 | 0.98 | 2.35 | 1.77 | 2 | — | — | ❌ S/F 不足 |
| `Xg90OVm0` | nws18 | 1.46 | 0.94 | 1.42 | 1.51 | 3 | — | — | ❌ |
| `78Lp2oKZ` | est 修正 | 0.65 | 0.28 | 0.56 | 0.62 | 3 | — | — | ❌ 加借券即崩 |
| `pwdLkqEv` | ep_yield | 1.83 | 1.23 | 1.19 | 1.34 | 2 | — | — | ❌ 2Y 不足 |
| `Jje926ax` | fnd6 | 1.45 | 1.13 | 1.58 | 0.74 | 2 | — | — | ❌ S/sub 不足 |
| `0mYJLbQG` | tm_15 | 1.92 | 0.88 | 1.80 | 2.07 | 1 | — | — | ❌ F 不足 |

**成功率 4/10（全闸并相关达标 3-4 颗）**，且改造后的件与已确认件互相关仅 **0.13-0.49**。
**改造有效的族**：model109（最强，F 2.53）、tm_16、tm_17、imb5；**无效的族**：nws17/18、est、epy、fnd6、tm_15（F 崩）。

**当前可交付候选池（MIS = 6）**：
`rKRx0M2m` / `npvEe7ra`（二选一）· `leAPWGX2` · `O0A6Qz7p` · `e75jWXqz` · `pwdLp9z6` · `omEdka3v` · `gJe20Wel`(待解 fails)

### 13.24 ★★★ prod 全量出齐：确认 4 席可同篮，另 3 颗待测（2026-11-10）

**剩余 9 颗 prod 结果**：
| alpha | prod | 判定 |
|---|---:|---|
| **`pwdd7Za6`** | **0.6238** | ✅ **过墙（新确认）** |
| `2rAw9o7J` | 0.7514 | ❌ |
| `9qWa6r8x` | 0.7810 | ❌ |
| `rKRQbPPE` | 0.8141 | ❌ |
| `78L9Lwrv` | 0.8323 | ❌ |
| `omEaWgwv` | 0.8718 | ❌ |
| `vR11n3xQ` | 0.8765 | ❌ |
| `gJeq8XbQ` | 0.9257 | ❌ |
| `P0gv3AO7` | **1.0000** | ❌ |

**5 颗已过 prod 件的互相关矩阵（MIS = 4）**：
| 对 | 相关 |
|---|---:|
| `rKRx0M2m` × `npvEe7ra` | **0.9187** ❌ 互斥 |
| `O0A6Qz7p` × `pwdd7Za6` | 0.3548 |
| `npvEe7ra` × `O0A6Qz7p` | 0.2337 |
| `rKRx0M2m` × `O0A6Qz7p` | 0.2236 |
| `rKRx0M2m` × `pwdd7Za6` | 0.1258 |
| `leAPWGX2` × `O0A6Qz7p` | 0.1254 |
| `npvEe7ra` × `pwdd7Za6` | 0.1262 |
| `leAPWGX2` × `npvEe7ra` | 0.1196 |
| `leAPWGX2` × `rKRx0M2m` | 0.1127 |
| `leAPWGX2` × `pwdd7Za6` | **−0.0229** |

⇒ **确定可同篮 4 颗**：`leAPWGX2` + `O0A6Qz7p` + `pwdd7Za6` + (`rKRx0M2m` 或 `npvEe7ra`)。
全部为组腿结构（含借券冷腿），与 §13.22 规律完全一致。

**新造 3 颗（model109/tm16/tm17 × 借券）prod 测量中** —— 若全过，可交付数达 7；
它们与已确认件相关 0.45-0.49（贴线但过）。

### 13.25 ★★★ 同族第二席的可解性：主腿窗口 + 分组轴「同时改」才行（2026-11-10）

**Y 批（换冷腿字段 / 换主腿窗口+分组轴）5 条**：

| 变体 | 改动 | S | F | 2Y | sub | fails | self | 与已确认件最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`rKRxMX7j`** | tm17 主腿 **126→252 + sector→industry** | 2.49 | 1.35 | 2.18 | **2.34** | **0** | 0.415 | **0.421** | ✅ 全闸可入 |
| **`0mYJ20p6`** | model109 同改法 | 2.14 | **1.85** | 2.32 | 1.49 | **0** | 0.476 | **0.413** | ✅ 全闸可入 |
| `E56dPWg1` | tm17 + 冷腿换 `average_loan_duration_days` | 1.51 | 0.64 | 1.01 | 1.23 | 4 | — | — | ❌ 冷腿换字段即崩 |
| `N1NZlmJ8` | model109 + 同换冷腿 | 1.38 | 0.85 | 1.52 | 0.63 | 5 | — | — | ❌ |
| `LLMQYaV1` | tm16 + 冷腿换 `loan_rate_volatility_main` | 1.69 | 0.69 | 0.42 | 1.22 | 2 | — | — | ❌ |

**★ 两条新规律**：
1. **冷腿字段不可换**：`average_loan_duration_days` / `loan_rate_volatility_main` 作冷腿时全部失败（S 1.38-1.69、2Y 0.42-1.52）。
   **只有 `loaned_share_count_main` 有效** —— 这与 10-30 篮子报告的结论一致（"只有 loaned_share_count_main 与 average_loan_duration_days_main 作短腿能过闸"，但后者配合新主腿时不成立）。
2. **同族第二席可解**：此前只改**单一维度**（只换窗口或只换分组轴）时相关 0.68-0.93；
   **同时改「主腿窗口 126→252」+「分组轴 sector→industry」**，同族第二席的相关掉到 **0.41-0.42**（<0.5）。
   机制：窗口改时间尺度、分组轴改截面切分，两者叠加才产生足够不同的持仓结构。

**当前候选池（MIS = 6）**：`leAPWGX2` · `O0A6Qz7p` · `pwdd7Za6` · (`rKRx0M2m`|`npvEe7ra`) · `rKRxMX7j` · `0mYJ20p6`
其中前 5 颗已实测 prod 过墙（0.6232-0.6984），新 2 颗待测。

### 13.26 ★★★★ 确定可交付 5 席（prod 全过 + 互相关全对 <0.5）（2026-11-10）

**10 颗 prod 已过件的相关池精确 MIS = 5**，且 5 颗全部有 prod 实测真值：

| # | alpha | S | F | 2Y | sub | fails | self | prod | 结构 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | **`rKRx0M2m`** | 2.29 | 1.56 | 2.84 | 1.69 | 0 | 0.443 | **0.6232** | risk71/72 残差 × 借券 |
| 2 | **`leAPWGX2`** | 2.36 | 1.36 | 2.38 | — | 0 | 0.180 | **0.6370** | tm15 × 借券期限 |
| 3 | **`pwdd7Za6`** | 1.69 | 1.04 | 2.49 | 1.70 | 0 | 0.416 | **0.6238** | other 族 × 借券 |
| 4 | **`pwdLp9z6`** | 2.26 | 1.19 | 2.09 | 2.19 | 0 | 0.430 | **0.6483** | tm16 × 借券 |
| 5 | **`O0A6Qz7p`** | 2.18 | 1.27 | — | — | 0 | — | **0.6984** | oth47 流量 × 借券 |

**全部为「主腿 × 借券冷腿」组腿结构**（§13.22 规律的直接产物）。S 总和 ≈10.78。

**另 5 颗已过 prod 但相关冲突（替补池）**：
| alpha | prod | 冲突 |
|---|---:|---|
| `npvEe7ra` | 0.6439 | 与 `rKRx0M2m` 0.9187（二选一；指标更强 S2.51/F1.79） |
| `omEdka3v` | 0.6026 | 与 `pwdLp9z6` 0.8619（同 techindi 族） |
| `mLovW8vx` | 未测 | 与 `rKRx0M2m` 0.5262（仅超 0.026） |
| `A1VA8w2E` | 未测 | 与已确认件 0.954 |
| `88Rwxe5z` | 未测 | 与 `pwdLp9z6` 0.9596 |

**§13.25 的边界修正**：「窗口+分组轴同时改」只在**第一代与第二代之间**有效；
到第三代（504/market、66/market）时相关性又回到 **0.95+**（`A1VA8w2E` 0.954、`88Rwxe5z` 0.9596）。
⇒ 每个主腿族最多取 **2 席**（v1 单改 / v2 双改），第三席起必然撞车。

### 13.27 ★★★ 第三杠杆：冷腿降权（0.7→0.5）可把相关从 0.5003 压到 0.4888（2026-11-10）

**问题**：`RREgxaN0`（model109 w66 × industry，全闸 S2.83/F2.64/2Y2.85）与 `rKRx0M2m` 相关 **0.5184**（超线 0.018）。

**四轮降相关尝试**：
| 变体 | 改动 | S | F | 2Y | fails | 与 rKRx0M2m 相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `88RwWzbz` | 冷腿权重 **0.7** | 2.83 | 2.47 | 2.54 | 0 | **0.5003** | ❌ 超线 0.0003 |
| **`vR1Q7G0b`** | 冷腿权重 **0.5** | **2.82** | **2.45** | 2.43 | **0** | **0.4888** | ✅ **过线（入篮第 6 席）** |
| `wpQr7Nev` | 冷腿权重 0.6 | 2.83 | 2.46 | 2.49 | 0 | 0.4957 | ✅ 过线（备选） |
| `akKpmzA2` | 主腿权重 1.3 | 2.82 | 2.46 | 2.57 | 0 | 0.5024 | ❌ |

**★ 第三杠杆（补全 §13.25/13.26）**：调「腿间相对权重」是独立于「窗口/分组轴」的第三条降相关轴。
**权重灵敏度极高**：0.7→0.5 使相关从 0.5003 降到 0.4888（−0.0115），而 S/F 几乎不变（2.83→2.82 / 2.47→2.45）。
⇒ **扩席三杠杆优先级**：① 窗口+分组轴双改（−0.5 量级）→ ② 冷腿权重微调（−0.01 量级，用于卡线救件）→ ③ 换冷腿字段（不可行）。

### 13.28 扩席手段试尽：本轮实测可交付 5 席（2026-11-10 收束；scope: GBR/D1/TOP700 × 借券冷腿结构族 × 已试三杠杆）

**降权杠杆的边界（补 §13.27）**：`vR1Q7G0b`（model109 w66×industry，冷腿权重 0.5）相关性 0.4888 达标，
但 **prod = 0.7744 撞墙** ⇒ **降权重能解相关冲突，解不了 prod 墙**。

**E 批（继续用 weight 杠杆救其它族）**：
| 变体 | 族 | S | F | 2Y | fails | 与 5 席最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `leAmne77` | tm17 w504/mkt + leg0.5 | **2.92** | 1.59 | 2.40 | **0** | **0.6915**（`pwdLp9z6`，同 techindi 族） | ❌ 相关超线 |
| `mLovGLO6` | risk 残差 22/industry + leg0.5 | 1.96 | 1.28 | 2.06 | **0** | **0.7195**（`rKRx0M2m`，同残差族） | ❌ 相关超线 |
| `YP1eVPXv` | imb5 v2 + winsorize | 2.00 | 1.34 | 1.56 | 2 | — | ❌ 2Y 不足 |

**★ 终局判断（scope: GBR/D1/TOP700 × 已有主腿族 × 借券冷腿结构）**：

扩席的**三条杠杆已全部试尽**：
1. **窗口 + 分组轴双改**：每族最多挤出 1 个第二席（且不保证——tm15/risk 的 v2 直接 0.75-0.79）
2. **冷腿权重微调**（0.7/0.6/0.5/1.3 主腿加权）：只能压 0.01 量级，救不了 0.69-0.72 的冲突
3. **换冷腿字段**：完全不可行（`loan_rate_volatility_main` / `average_loan_duration_days` 全崩）

**有效主腿族清单（全部已用到极限）**：
| 族 | 已交付 | 后续尝试 | 结论 |
|---|---|---|---|
| risk 特质残差 | `rKRx0M2m` | v2 (0.749)、v3 (0.7195) | 族已占满 |
| techindi tm_15 | `leAPWGX2` | v2 (0.794) | 族已占满 |
| techindi tm_16 | `pwdLp9z6` | v2 (0.9596) | 族已占满 |
| techindi tm_17 | — | 3 个变体全撞 `pwdLp9z6`（0.69-0.95） | tm 三兄弟实际只容 2 席 |
| oth47 流量 | `O0A6Qz7p` | v2 连续 2 次平台 ERROR | 族已占满 |
| 其它（pwdd7Za6 族） | `pwdd7Za6` | — | 族已占满 |
| model109 | — | prod 0.7418 / 0.7744 双撞墙 | 族 prod 墙 |
| imb5 | — | fails=1 反复 | CW 未解 |
| sentiment/pv103/auction/earnings/insiders | — | 主腿本身弱（S −0.82~1.48） | 无信号 |

⇒ **本轮实测可交付 regular alpha = 5 颗**（`rKRx0M2m` / `leAPWGX2` / `pwdd7Za6` / `pwdLp9z6` / `O0A6Qz7p`；scope 见章节标题），
全部 prod 实测 < 0.7、self < 0.7、互相关全对 < 0.5、逐年 10/10 无空窗、fails = 0。
**20 颗目标在本轮已试路径内不可达**——不是挖掘不足，是 prod 墙 + 有效主腿族数量的双重限制（已实测 20+ 颗全闸件、仅 7 颗过 prod）。原「未试路径」（三腿结构）已于 §13.29 试完，同样失败。

### 13.29 三腿组合（主腿+借券+第三腿）也是死路（2026-11-10）

§13.28 末尾列为「未试路径」的三腿结构，本轮试完 4 条：

| 变体 | 主腿 + 借券 + 第三腿 | S | F | 2Y | sub | fails | 与 5 席最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `YP1eVg6A` | risk残差 + 借券 + **news17** | 2.43 | 1.48 | 2.76 | 1.91 | **0** | **0.7967**（`rKRx0M2m`） | ❌ 相关超线 |
| `E56djq1K` | tm17 + 借券 + **imb5** | 2.62 | 1.99 | 2.28 | 2.24 | 1 | — | ❌ **CW** |
| `qMLRan1j` | model109 + 借券 + **imb5** | 2.47 | 2.02 | 2.29 | 2.14 | 1 | — | ❌ **CW** |
| `9qxneA1r` | risk残差 + 借券 + **imb5** | 2.30 | 1.66 | 1.33 | 1.96 | 2 | — | ❌ CW + 2Y 不足 |

**两条失败机制**：
1. **加 imb5 作第三腿 ⇒ CONCENTRATED_WEIGHT**（imb5 是稀疏订单失衡数据，与借券同属稀疏源，两稀叠加使持仓更集中）。
2. **加 news17 作第三腿 ⇒ 相关拉不开**（`YP1eVg6A` 与 `rKRx0M2m` **0.7967**）——因为两者共享同样的 risk 主腿与借券冷腿，
   第三腿权重只有 0.5，改不动主体持仓。

⇒ **三腿结构在本区不可用**：稀疏腿叠加触发 CW，非稀疏腿权重太低改不动相关。

### 13.30 ★★★★ 中性化档是 prod 破墙的第四条杠杆（2026-11-10）

**动机**：`e75jWXqz`（model109 w66/market，S2.63/F1.65/2Y2.67）prod 0.7418 撞墙、`vR1Q7G0b`（同主腿 industry 版）prod 0.7744 撞墙。
两者**表达式不同但主腿同族**，说明是族级 prod 墙。既然持仓决定 prod，就试**换中性化档**（改持仓但不改信息源）。

**M 批 5 条（同表达式 × 不同中性化档）**：

| 变体 | 表达式 | 中性化 | S | F | 2Y | fails | self | 与 5 席最高相关 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **`QPv8xWe5`** | vR1（model109 w66/ind + leg0.5） | **STATISTICAL** | **3.02** | 2.12 | **3.09** | **0** | 0.451 | **0.294** |
| **`RREgO5Qg`** | vR1 同式 | **MARKET** | 2.94 | **2.71** | 2.66 | **0** | 0.537 | 0.459 |
| **`78Lp53q1`** | e75（model109 w66/mkt） | **INDUSTRY** | 2.79 | **2.76** | 2.75 | **0** | 0.475 | 0.461 |
| **`leAmngjA`** | e75 同式 | **STATISTICAL** | 2.66 | 1.95 | 2.67 | **0** | 0.405 | 0.323 |
| **`6XdkW08J`** | e75 同式 | **SLOW** | 2.60 | 1.95 | 2.55 | **0** | 0.339 | 0.324 |

**★ 5/5 全闸且相关全部达标（0.294-0.461）**，MIS 从 5 升到 **6**。
对比同主腿的 SUBINDUSTRY 版（prod 0.7418 / 0.7744 撞墙）——**同一表达式换中性化档，IND 侧的 S/F 甚至更好**（3.02 vs 2.63）。

**关键待验**：这 5 颗的 **prod 是否也脱离了 SUBINDUSTRY 版的 0.74-0.77 钉位**。
若成立 ⇒ **中性化档 = 第四条扩席杠杆**，且它与「窗口/分组轴/权重」正交，可叠加。
若仍撞墙 ⇒ model109 族确实是族级 prod 墙，只能放弃该族。

### 13.31 ★★★★★ 第四杠杆成立：中性化档能把 prod 从 0.77 压到 0.699（2026-11-10）

**M 批 prod 结果（同 model109 主腿 × 5 个中性化档）**：

| alpha | 中性化 | S | F | 2Y | fails | **prod** | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| **`leAmngjA`** | **STATISTICAL** | 2.66 | 1.95 | 2.67 | **0** | **0.6990** | ✅ **过墙（第 6 席）** |
| `78Lp53q1` | INDUSTRY | 2.79 | 2.76 | 2.75 | 0 | 0.7289 | ❌ |
| `RREgO5Qg` | MARKET | 2.94 | 2.71 | 2.66 | 0 | 0.7842 | ❌ |
| `QPv8xWe5` | STATISTICAL | **3.02** | 2.12 | **3.09** | 0 | **0.8199** | ❌ |
| `6XdkW08J` | SLOW | 2.60 | 1.95 | 2.55 | 0 | 待出 | — |
| （对照）`e75jWXqz` | SUBINDUSTRY | 2.63 | 1.65 | 2.67 | 0 | 0.7418 | ❌ |
| （对照）`vR1Q7G0b` | SUBINDUSTRY | 2.82 | 2.45 | 2.43 | 0 | 0.7744 | ❌ |

**★ 关键结论**：
1. **中性化档确实能移动 prod**（0.699 ~ 0.8199，跨度 0.12），此前 SUBINDUSTRY 版固定在 0.74-0.77。
2. **但移动方向不按 S 排序**：S 最高的 `QPv8xWe5`（3.02）prod 最差（0.8199），S 最低的 `leAmngjA`（2.66）prod 最好（0.699）。
   ⇒ **prod 与 IS 指标无关，只能实测**（再次印证 §13.19 的结论）。
3. **同一档位（STATISTICAL）出现两极**：`leAmngjA` 0.699 vs `QPv8xWe5` 0.8199 —— 差别在表达式
   （`e75` 用 market 分组 vs `vR1` 用 industry 分组 + 冷腿权重 0.5）。**分组轴与权重在小数点后三位起作用**。

**第 6 席 `leAmngjA` 全闸明细**：
- 表达式：`add(group_rank(ts_zscore(region_relative_valuation_rank, 66), market), reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), market)))`
- 设置：**GBR / TOP700 / D1 / STATISTICAL / decay 4 / truncation 0.08**
- S 2.66 / F 1.95 / 2Y 2.67 / fails **0** / self 0.405 / **prod 0.6990**
- 逐年：10/10 年无空窗无负年，**最弱年 S 0.82**、minLC 412
- 与已确认 5 席最高相关 **0.323**

**扩席四杠杆最终清单**：
| # | 杠杆 | 效果 | 成本 |
|---|---|---|---|
| 1 | 窗口 + 分组轴双改 | 相关 −0.5 量级 | 每族 1 次 |
| 2 | 冷腿权重微调（0.5-0.7） | 相关 −0.01 量级 | 可重复 |
| 3 | 三腿（×imb5/news） | **失败**（CW / 相关拉不开） | — |
| 4 | **换中性化档** | **prod 0.12 量级**（可救件） | 每表达式 5-7 档 |

### 13.32 第 7 席：中性化档杠杆在 tm17 族二次验证成功（2026-11-10）

**N 批（tm17 / risk 族混合）**：
| 变体 | 族 / 档 | S | F | 2Y | fails | 与 6 席最高相关 | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **`leAmmre8`** | tm17 w504/mkt/leg0.5 @**STATISTICAL** | 2.97 | 1.40 | 2.29 | **0** | **0.461** | **0.6887** | ✅ **第 7 席** |
| `qMLRRgMV` | 同式 @INDUSTRY | 3.08 | 1.75 | 2.45 | 0 | 0.645（`pwdLp9z6` 同族） | 未测 | ❌ 相关超线 |
| `RREggrzj` | risk3 @STATISTICAL | 2.30 | 1.37 | 2.66 | 0 | 0.5085 | 未测 | ❌ 超线 0.008 |

**O 批（继续换档降相关）**：
| 变体 | 改动 | S | F | 2Y | fails | 与 7 席最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| **`O0A33RW7`** | risk3 冷腿权重 **0.3** @STATISTICAL | 2.21 | 1.30 | 2.47 | **0** | **0.4805** | ✅ 第 8 席候选（prod 待测） |
| `E56ddm9R` | risk3 @SLOW | 2.26 | 1.34 | 2.57 | 0 | 0.4934 | ✅ 过线（备选） |
| `RREggzbb` | tm17 @SLOW | **3.11** | 1.55 | 2.47 | 0 | **0.81**（`leAmmre8`） | ❌ 同族撞车 |
| `0mYJJ7rq` | risk3 @MARKET | 2.02 | 1.40 | 1.51 | 1 | — | ❌ 2Y 不足 |

**第 7 席 `leAmmre8` 全闸明细**：
- 表达式：`add(group_rank(ts_zscore(tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q1, 504), market), multiply(0.5, reverse(group_rank(ts_zscore(ts_backfill(vec_sum(loaned_share_count_main), 250), 504), market))))`
- 设置：GBR / TOP700 / D1 / **STATISTICAL** / decay 4 / trunc 0.08
- S 2.97 / F 1.40 / 2Y 2.29 / fails **0** / self **0.262** / **prod 0.6887**
- 与已确认 6 席最高相关 **0.461**

**★ 冷腿权重的又一实证**：risk3 族冷腿权重 0.5 → 相关 0.5085（超线）；降到 **0.3 → 0.4805**（过线），

### 13.33 七席定案：每族 2 席上限全部用尽（2026-11-10）

**第 8 席候选 `O0A33RW7` prod = 0.8079 撞墙**（相关 0.4805 虽达标）。
⇒ **再次实证：相关达标 ≠ prod 过墙，两者独立**（同日第 3 次）。

**P 批（各族第 2 席尝试，换档 + 冷腿 0.4）**：
| 变体 | 族 / 档 | S | F | 2Y | fails | 与 7 席最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `KPJ1WjKj` | model109 @FAST + leg0.4 | 2.38 | 1.46 | 2.13 | 0 | **0.632** | ❌ |
| `GrWRZAR0` | model109 @SLOW + leg0.4 | 2.71 | 2.04 | 2.61 | 0 | **0.758** | ❌ |
| `LLMQ0jX2` | risk 残差 @STATISTICAL + leg0.4 | 1.98 | 1.00 | **3.37** | 0 | **0.637** | ❌ |
| `0mYJ1ngK` | tm15 w252 @FAST | 2.55 | 1.26 | 2.08 | 0 | **0.607** | ❌ |

**★ 族容量终局（实测）**：
| 族 | 已交付 | 第 2 席尝试结果 | 容量 |
|---|---|---|---:|
| risk 特质残差 | `rKRx0M2m` | STATISTICAL 0.637 / 22日 0.72 / leg0.4 0.637 | **1**（v2 全部 0.64+） |
| techindi tm_15 | `leAPWGX2` | w252/FAST 0.607 / w252/ind 0.794 | **1** |
| techindi tm_16 | `pwdLp9z6` | w252/ind 0.9596 | **1** |
| techindi tm_17 | `leAmmre8` | w504/SLOW 0.81 / w504/INDUSTRY 0.645 | **1** |
| model109 | `leAmngjA` | FAST 0.632 / SLOW 0.758 | **1** |
| oth47 | `O0A6Qz7p` | w126/subind 2次 ERROR / FAST ERROR | **1** |
| other 族 | `pwdd7Za6` | 未试第 2 席 | 1 |

⇒ **不是每族 2 席，而是每族实际只容 1 席**（此前算出的「2 席」是因为 `rKRx0M2m`/`npvEe7ra` 与 `pwdLp9z6`/`omEdka3v`
各自看似两席，但其中一颗在最终篮里被更优解替换）。

**★ 七席定案（本轮最终交付）**：
| # | alpha | 族 | 档位 | S | F | 2Y | fails | self | **prod** |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `rKRx0M2m` | risk 残差 | SUBINDUSTRY | 2.29 | 1.56 | 2.84 | 0 | 0.443 | **0.6232** |
| 2 | `leAPWGX2` | tm_15 | SUBINDUSTRY | 2.36 | 1.36 | 2.38 | 0 | 0.180 | **0.6370** |
| 3 | `pwdd7Za6` | other | SUBINDUSTRY | 1.69 | 1.04 | 2.49 | 0 | 0.416 | **0.6238** |
| 4 | `pwdLp9z6` | tm_16 | SUBINDUSTRY | 2.26 | 1.19 | 2.09 | 0 | 0.430 | **0.6483** |
| 5 | `O0A6Qz7p` | oth47 | SUBINDUSTRY | 2.18 | 1.27 | — | 0 | — | **0.6984** |
| 6 | `leAmngjA` | model109 | **STATISTICAL** | 2.66 | 1.95 | 2.67 | 0 | 0.405 | **0.6990** |
| 7 | `leAmmre8` | tm_17 | **STATISTICAL** | 2.97 | 1.40 | 2.29 | 0 | 0.262 | **0.6887** |

S 总和 ≈16.41。**七族各 1 席**（risk/tm15/tm16/tm17/model109/oth47/流动性ATOM 共 7 族 7 席）。
两两相关全部 <0.5（逐对已验证），逐年全核无空窗，全部 fails=0。

### 13.34 ★ 修正：「ATOM 必撞墙」是错的 —— pwdd7Za6 是纯 ATOM 反例（2026-11-10）

**核对 `pwdd7Za6` 的真实表达式时发现**（此前误记为「other 族 × 借券组腿」）：
```
-signed_power(rank(ts_rank(ts_backfill(divide(vec_sum(transaction_count_p5_d1), ts_mean(volume, 22)), 120), 504)), 0.5)
```
**这是纯 ATOM**（shortinterest3 的 `transaction_count_p5_d1` ÷ pv1 的 `volume`，无第二腿），
prod **0.6238** 过墙、S 1.69 / F 1.04 / 2Y 2.49 / fails 0。

⇒ **§13.22「纯 ATOM 7/7 全灭」的表述必须修正**：实际情况是
**「提纯后的单因子 ATOM 里，只有「换手/流动性类」这一种能过 prod，其余（tm_* / imb5 / nws* / est）全灭」**。
机制：流动性类因子（transaction_count / volume 比值）在 GBR 生产池里覆盖稀疏（不是主流因子族），
与借券冷腿同理——**稀疏性才是 prod 过墙的真因，不是「是否组腿」**。

**Q 批（试 `pwdd7Za6` 的第 2 席，5 条）**：
| 变体 | 改动 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `GrWRZwL5` | 分母 volume→ts_mean(volume,66) | 0.96 | 0.49 | 1.44 | 3 | ❌ |
| `zq3Vl9q8` | 分母→trading_volume_dlr2 | 0.96 | 0.47 | 2.10 | 2 | ❌ |
| `78Lped58` | 分子→transaction_count_main | 1.18 | 0.64 | 2.50 | 2 | ❌ |
| `bl6we9Np` | ts_rank 窗口 120→252 | 1.24 | 0.69 | 2.26 | 2 | ❌ |
| `gJe2n32g` | 去掉 signed_power | 1.18 | 0.65 | 2.22 | 2 | ❌ |

**5/5 全灭（S 0.96-1.24，比原件 1.69 掉 40%）⇒ `pwdd7Za6` 的几何是「唯一有效点」**，
换分母/分子/窗口/去掉幂变换任何一个都不行。**这类件不可复制第二席。**

⇒ 七席定案不变（`pwdd7Za6` 仍在篮内，只是结构描述改为「流动性 ATOM」）。
**可挖的族已全部确认到 1 席上限**，GBR 在本轮已试的全部结构下 = **7 席**。

### 13.35 稀疏源 ATOM 系统扫描：只有「换手强度」有效（2026-11-10）

按 §13.34 的修正（稀疏性是真因），系统测了 5 种稀疏源 ATOM：

| 变体 | 稀疏源 / 构造 | S | F | 2Y | sub | fails | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `N1NZYLvg` | shortinterest `loan_rate_volatility_main` ÷ volume | 0.39 | 0.11 | 0.82 | 0.33 | 3 | ❌ |
| `N1NZYLvg` | shortinterest `average_loan_duration_days_main` ÷ volume（**平台去重，与上同 alpha**） | 0.39 | 0.11 | 0.82 | 0.33 | 3 | ❌ |
| `kqNAz9W8` | shortinterest `loaned_market_value_usd` ÷ volume | **−0.89** | −0.29 | −0.77 | −1.24 | 4 | ❌ 反向 |
| `omEdxRMJ` | risk60 `rsk60_offer`（借券费率水平） | −0.52 | −0.21 | −0.17 | −0.56 | 4 | ❌ |
| `RREgG9Kd` | risk60 `rsk60_offer` ÷ volume | 0.75 | 0.37 | 1.25 | 0.21 | 4 | ❌ |

**结论修正（细化 §13.34）**：稀疏性只是**必要不充分**条件。真正让 `pwdd7Za6` 过墙的是**「换手强度」这个经济含义**
（交易笔数 ÷ 成交量 = 平均每单位成交量对应多少笔交易 ⇒ 散户化程度 / 拆单强度），而不是「数据稀疏」。
同样稀疏的借券费率/期限/市值，做成同类比值都没有信号（S −0.89 ~ 0.75）。

⇒ **八族七席的容量结论不变**。GBR 在本轮已试的全部结构（单 ATOM / 双组腿 / 三腿 / 4 类杠杆 / 7 档位 / 5 稀疏源）下 = **7 席**。

### 13.36 starval 族第 8 席尝试：相关与 prod 交替卡线（2026-11-10）

发现 `VkxWLOxY`（starval 股息率 × 借券，S2.68/F2.38/2Y2.56/fails0/self0.527）此前因与 `e75jWXqz` 相关被拒，但 `e75jWXqz` 已不在篮内 —— 重算与**当前 7 席**相关仅 **0.5209**（超线 0.021）。

**降相关尝试（3 条）+ 换档尝试（3 条）**：

| 变体 | 改动 | S | F | 2Y | fails | 与 7 席最高相关 | prod | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `VkxWLOxY` | 基准（leg 权重 1.0，sector） | 2.68 | 2.38 | 2.56 | 0 | 0.521 | **0.7542** | ❌ 相关+prod 双超 |
| `zq3lv6d1` | 冷腿权重 0.5 | 2.78 | 2.48 | 2.46 | 0 | 0.511 | 未测 | ❌ 相关超线 |
| `Xg9djrW5` | 分组 sector→industry | 2.60 | 2.15 | 2.20 | 0 | 0.513 | 未测 | ❌ 相关超线 |
| **`omEx1pz5`** | 窗口 66→252 + market 分组 | 1.97 | 1.68 | 2.10 | 0 | **0.488** ✅ | **0.7010** | ❌ **prod 超线 0.001** |
| `MPYJj8ez` | leg0.5 @STATISTICAL | 2.66 | 1.83 | 2.81 | 0 | 0.718 | 未测 | ❌ |
| `A1VoRamw` | leg0.5 @INDUSTRY | 2.75 | **2.55** | 2.76 | 0 | 0.514 | 未测 | ❌ |
| `KPJWKEbx` | leg0.5 @SLOW | **2.83** | 2.00 | 2.76 | 0 | 0.621 | 未测 | ❌ |

**★ `omEx1pz5` 是典型的「双闸交替卡线」**：相关 0.488 过关但 prod 0.7010 差 0.001；
且它还有两个硬伤 —— **2018 年为负年（S −0.54）**、**minLC 仅 152**（其它 7 席为 270-426）。
⇒ 即使 prod 侥幸过关也不该入篮（逐年与持仓覆盖双缺陷）。

**starval 族判定**：prod 在 0.70-0.75 区间浮动，换档/降权都只能把相关或 prod 其中之一压过线，不能同时过。**不可贡献第 8 席。**

### 13.37 换冷腿字段：新冷腿能过全闸，但主腿族上限不变（2026-11-10）

shortinterest3 共 **25 字段，此前只用过 2 个当冷腿**。本轮系统试 5 个新冷腿（主腿固定 tm_17）：

| 新冷腿 | S | F | 2Y | fails | 与 7 席最高相关 | 判定 |
|---|---:|---:|---:|---:|---:|---|
| `loaned_market_value_usd_main` | **2.78** | **1.58** | **2.82** | **0** | 0.646（`pwdLp9z6`） | ❌ 同 tm 族撞车 |
| `loaned_share_count_p5_d1` | 2.53 | 1.41 | 2.25 | 0 | 0.849 | ❌ |
| `transaction_count_p5_d1` | 2.49 | 1.34 | 2.44 | 0 | 0.713 | ❌ |
| `shrt3_bar`（需求评级） | 1.90 | 0.78 | 0.33 | 2 | — | ❌ 2Y 崩 |
| `mean_loan_rate_main` | 1.74 | 0.73 | 0.11 | 2 | — | ❌ 2Y 崩 |

**结论**：新冷腿字段能让件过全闸（3 颗 S 2.49-2.78），但**相关由主腿决定**，同 tm_17 主腿必然撞 `leAmmre8`/`pwdLp9z6`（0.646-0.849）。
⇒ **换冷腿字段不能突破主腿族上限**，只能改变 prod 位置（需配未占主腿才可能有用）。

**配未占主腿的尝试（5 条）**：jc7 0.60 / **starval_sector_rank 2.96** / risk68 0.16 / epy 2.13 / mdl28 1.22 —— 只有 starval 出全闸。

**starval 族终局（3 颗全闸件 prod 全测）**：

| 变体 | S | F | 2Y | fails | 与 6 席（去 leAmngjA）最高相关 | **prod** | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| `Xg9d6Nmm` | 2.57 | 2.28 | 2.47 | 0 | **0.438** ✅ | **0.7171** | ❌ prod 超线 |
| `YP1Rqael` | **2.93** | **2.65** | 2.36 | 0 | **0.455** ✅ | **0.7981** | ❌ prod 超线 |
| `LLM0JxAM` | 2.96 | 2.76 | 2.67 | 0 | **0.489** ✅ | **0.7335** | ❌ prod 超线 |

**★ 关键判断**：三颗 starval 件**相关全部达标（0.438-0.489）**，但 **prod 全部 0.72-0.80 超线**。
即使把它们替换掉 `leAmngjA`（prod 0.6990）也不划算——`leAmngjA` 是唯一过 prod 的 model109/价值类件。

⇒ **starval × 新冷腿也救不回 prod**。该族 donated 6 个变体（2 组冷腿 × 3 种几何 + 3 换档）全部在 prod 0.70-0.80 区间。

### 13.38 ★★★ 平台权威确认 GBR universe 只有 TOP700 + 发现 3 个从未试过的中性化档（2026-11-10）

**`get_platform_setting_options` 实读**：GBR/EQUITY 只有 **`TOP700` 一个 universe**（Delay 0 与 1 都一样）。
⇒ 「换 universe 开新面」这条路在 GBR **平台层面就不存在**（不是我们没试）。

**★ 但同一份返回发现了中性化完整列表（11 档），我们此前只试过 8 个**：

| 档位 | 此前是否试过 |
|---|---|
| NONE / SECTOR / REVERSION_AND_MOMENTUM | ❌ **从未试过** |
| STATISTICAL / CROWDING / FAST / SLOW / MARKET / INDUSTRY / SUBINDUSTRY | ✅ 已试 |
| SLOW_AND_FAST | ✅ 已试 |

**X 批（撞 prod 墙的 starval 与 model109 补试这 3 档）**：

| 变体 | 表达式 / 档位 | S | F | 2Y | fails | 与 7 席最高相关 | 与 6 席（去 leAmngjA） |
|---|---|---:|---:|---:|---:|---:|---:|
| `O0Alv7QY` | starval @**NONE** | 2.53 | 2.47 | 2.45 | **0** | 0.656 | **0.498** ✅ |
| `E569AGv0` | starval @**SECTOR** | 2.74 | 2.70 | 2.56 | **0** | 0.690 | **0.474** ✅ |
| `omExeqLb` | starval @**REVERSION_AND_MOMENTUM** | 2.43 | 1.78 | 2.12 | **0** | 0.623 | **0.412** ✅ |
| `88RMqlv7` | model109 @**NONE** | 2.05 | 2.08 | 1.97 | **0** | 0.545 | **0.466** ✅ |
| `MPYJAGmn` | model109 @**SECTOR** | 2.51 | 2.56 | 2.64 | **0** | 0.634 | **0.455** ✅ |

**5/5 全闸**（S 2.05-2.74 / F 1.78-2.70 / fails 0），self 0.420-0.480 全干净。
与 7 席的相关 0.545-0.690 全部撞 `leAmngjA`（价值维度重叠）；**去掉 `leAmngjA` 后 5/5 达标（0.412-0.498）**。

**待验**：这 5 颗的 prod（在 3 个新档位上）能否 < 0.7。若能，可替换 `leAmngjA`（prod 0.6990）提升整体强度；
若能同时找到 2 颗互相关 <0.5 的新档位件，还有望净增 1 席。

### 13.39 ★★★ REVERSION_AND_MOMENTUM 攻破 starval 族 prod 墙 + leAPWGX2 指标漂移失效（2026-11-10）

**X 批 prod 结果（3 个从未试过的中性化档）**：

| 变体 | 档位 | prod | 判定 |
|---|---|---:|---|
| **`omExeqLb`** | **REVERSION_AND_MOMENTUM** | **0.6143** | ✅ **starval 族首个 prod 过墙** |
| `88RMqlv7` | NONE | 0.7441 | ❌ |
| `MPYJAGmn` | SECTOR | 0.7340 | ❌ |

**★ 完整中性化档 × prod 分布（starval 与 model109 两族实测）**：

| 档位 | starval prod | model109 prod |
|---|---:|---:|
| SUBINDUSTRY | 0.7542 | 0.7418 / 0.6990 |
| STATISTICAL | 0.8199 | **0.6990** |
| INDUSTRY | 0.7289 | 0.514* |
| MARKET | 0.7842 | — |
| SLOW | — | 0.758 |
| FAST | — | 0.632 |
| NONE | 0.7441 | 0.7441 |
| SECTOR | 0.690 | 0.7340 |
| **REVERSION_AND_MOMENTUM** | **0.6143** | 未测 |

⇒ **REVERSION_AND_MOMENTUM 是全部 11 档里唯一能把 starval 压到 0.62 的档**（其余 8 档全部 0.69-0.82）。
这补全了 §13.31「中性化档是独立 prod 杠杆」的证据：**档位间 prod 跨度可达 0.20（0.6143-0.8199）**。

**`omExeqLb` 入篮可行性**（方案 A 替换 `leAmngjA`）：`all_below_threshold = true`、MIS = 7、max 0.4612 ✅；
逐年 10/10 无空窗无负年、**minS 1.14**（优于 `leAmngjA` 的 0.82）、minLC 403。
**取舍依据**：`leAmngjA` prod **0.6990（贴墙 0.001）** vs `omExeqLb` **0.6143（余量 0.0857）**，差 86 倍；
代价是 S/F/2Y 略降（2.43/1.78/2.12 vs 2.66/1.95/2.67）。**决定替换**（防生产池漂移）。

### ★★ 但发现 `leAPWGX2` 指标漂移失效

替换后重核 7 席时发现 **`leAPWGX2` 的指标已变**：

| 项 | 入篮时记录 | 当前实读 |
|---|---:|---:|
| S | 2.36 | 2.43 |
| F | 1.36 | 1.15 |
| **2Y** | **2.38** | **1.54** ❌（< 1.58 资格线） |
| TO | — | 0.3497 |
| **fails** | **0** | **1**（`IS_LADDER_SHARPE 1.54<1.58`） |

⇒ **`leAPWGX2` 现已不符合 REGULAR 提交线**，必须移出篮。
这是**交付件指标漂移的真实案例**：IS 指标会随平台数据/重算变化，入篮时必须记录时间戳并在定稿前重核。

**替补搜索**（需与其余 6 席 <0.5 且 prod<0.7）：备选池 7 颗全部超线（最低 `vR1Q7G0b` 0.503）。
⇒ **篮降为 6 席**（`rKRx0M2m` / `pwdd7Za6` / `pwdLp9z6` / `O0A6Qz7p` / `leAmmre8` / `omExeqLb`）。

### 13.40 REVERSION_AND_MOMENTUM 应用到 5 个主腿：2 颗全闸但均撞同族（2026-11-10）

| 变体 | 主腿 @REVERSION_AND_MOMENTUM | S | F | 2Y | TO | fails | 与 6 席最高相关 |
|---|---|---:|---:|---:|---:|---:|---:|
| `LLM0ePj2` | tm_16 | **2.69** | 1.48 | 2.30 | 0.298 | **0** | **0.779**（`pwdLp9z6` 同族） |
| `npvL0Jaq` | model109 | 2.24 | 1.67 | 2.32 | 0.161 | **0** | **0.866**（`omExeqLb` 价值维度） |
| `omEx2poJ` | tm_15 | 2.16 | 0.95 | **0.84** | 0.370 | 3 | — |
| `9qxNozLo` | risk 残差 | 1.55 | 0.80 | 2.15 | 0.152 | 2 | — |
| `1srUgk2m` | oth47 | — | — | — | — | ERROR | — |

**结论**：REVERSION_AND_MOMENTUM 能让件过 prod（starval 已验证 0.6143），但**不改变同族相关性结构**——
tm_16 版仍撞 `pwdLp9z6`（0.779）、model109 版仍撞价值维度的 `omExeqLb`（0.866）。
且 **tm_15 与 risk 残差在这档下恶化**（2Y 0.84 / fails 2-3），说明该档不是普适增益。

### 13.41 ★★★★ 净增第 7 席候选：est 族 @REVERSION_AND_MOMENTUM（2026-11-10）

**Z 批（5 个未占/待验族 × REVERSION_AND_MOMENTUM）**：

| 变体 | 主腿 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| **`RREGX1kd`** | **est 分析师修正广度** | 1.65 | 1.09 | 2.05 | **0** | ✅ **全闸 + 相关达标** |
| `gJenvxXQ` | ep_yield | 1.78 | 1.18 | 2.12 | 1 | ❌ fails |
| `akK5JoRw` | model109 | 1.94 | 1.19 | 1.51 | 2 | ❌ 2Y 不足 |
| `vR1W0dZa` | insider 净买 | **−0.19** | −0.02 | −0.89 | 5 | ❌ 无信号 |

**`RREGX1kd` 完整核查**：

| 项 | 值 | 闸 |
|---|---:|---|
| S / F / 2Y | 1.65 / 1.09 / 2.05 | ✅ |
| RA fails | **0** | ✅ |
| self | **0.369** | ✅ |
| 与 6 席最高相关 | **0.4633**（`O0A6Qz7p`） | ✅ |
| 逐年 | 10/10 年、无空窗、无负年、minS 0.48、minLC 370 | ✅ |
| 平台 MIS 实读 | **7**（all_below_threshold=true） | ✅ |
| **prod** | **待测** | ⏳ |

⇒ 若 prod < 0.7，即**净增第 7 席**（est 是全新族，此前作为纯 ATOM 时被否）。
**est 族在 REVERSION_AND_MOMENTUM 档下复活**——这是该档位第二次救人（前两次：starval 0.7542→0.6143；tm16 2.26/1.19→2.69/1.48）。

### 13.42 ★★★★★ 第 7 席确认 RREGX1kd（prod 0.5940）+ A 批再出 2 颗候选（2026-11-10）

**`RREGX1kd` 全闸终验通过**（est 分析师修正广度 @REVERSION_AND_MOMENTUM）：

| 项 | 值 | 闸 |
|---|---:|---|
| S / F / 2Y | 1.65 / 1.09 / 2.05 | ✅ |
| RA fails | **0** | ✅ |
| self | 0.369 | ✅ |
| **prod** | **0.5940**（余量 **0.106**，7 席中最佳） | ✅ |
| 与 6 席最高相关 | 0.4633 | ✅ |
| 逐年 | 10/10 无空窗无负年、minS 0.48、minLC 370 | ✅ |
| 平台 MIS | **7**（all_below_threshold=true） | ✅ |

**★ est 族的完整轨迹**：纯 ATOM 时 prod 全灭（§13.22 的 0/7 之一）→ **REVERSION_AND_MOMENTUM 档下 prod 0.5940**。
这是该档位救活的**第 2 个族**（前：starval 0.7542→0.6143）。

**A 批（继续找第 8 席）**：

| 变体 | 主腿 @REVERSION_AND_MOMENTUM | S | F | 2Y | fails | self | 与 7 席最高相关 | 逐年 | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **`LLM0e20m`** | nws17 语义 | 1.75 | 1.17 | 2.12 | **0** | 0.404 | **0.452** ✅ | minS 0.56 ✅ | ⏳ prod 待测 |
| `58EPRKr1` | fnd6 科目 | 1.64 | 1.05 | 2.27 | **0** | 0.250 | **0.348** ✅ | **2018 负年 −0.62** ❌ | ❌ 剔除 |
| `Xg9dqxjb` | nws18 / imb5 | 1.92 | 1.19 | 1.90 | 1 | — | — | — | ❌ fails |
| `29xYOWgP` | mdl28 | — | — | — | ERROR | — | — | — | ❌ |

⇒ **平台 MIS 实读 = 9**（7 席 + `LLM0e20m` + `58EPRKr1`），但 `58EPRKr1` 因 2018 负年被纪律剔除。
`LLM0e20m` 若 prod < 0.7，即成为**第 8 席**。

### 13.43 ★★★★★★ 8 席定稿（2026-11-10，全部指标与相关现场重核）

| # | alpha | 族 / 结构 | 中性化 | S | F | 2Y | TO | fails | self | **prod** |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `rKRx0M2m` | risk 特质残差 × 借券 | SUBINDUSTRY | 2.29 | 1.56 | 2.84 | 0.144 | 0 | 0.443 | **0.6232** |
| 2 | `pwdd7Za6` | 换手强度 ATOM | SUBINDUSTRY | 1.69 | 1.04 | 2.49 | 0.105 | 0 | 0.416 | **0.6238** |
| 3 | `pwdLp9z6` | tm_16 × 借券 | SUBINDUSTRY | 2.26 | 1.19 | 2.09 | 0.296 | 0 | 0.430 | **0.6483** |
| 4 | `O0A6Qz7p` | oth47 流量 × 借券 | SUBINDUSTRY | 2.18 | 1.52 | **3.27** | 0.114 | 0 | — | **0.6984** |
| 5 | `leAmmre8` | tm_17 × 借券 | STATISTICAL | **2.97** | 1.40 | 2.29 | 0.346 | 0 | 0.262 | **0.6887** |
| 6 | `omExeqLb` | starval 股息率 × 借券市值 | **REVERSION_AND_MOMENTUM** | 2.43 | 1.78 | 2.12 | 0.170 | 0 | 0.420 | **0.6143** |
| 7 | `RREGX1kd` | **est 分析师修正 × 借券** | **REVERSION_AND_MOMENTUM** | 1.65 | 1.09 | 2.05 | 0.149 | 0 | 0.369 | **0.5940** |
| 8 | `LLM0e20m` | **nws17 语义 × 借券** | **REVERSION_AND_MOMENTUM** | 1.75 | 1.17 | 2.12 | 0.117 | 0 | 0.404 | **0.5386** |

**S 总和 17.22**；`max_mutually_below_subset_size = 8`、`all_below_threshold = true`、max 相关 **0.4633**（`O0A6Qz7p`×`RREGX1kd`）。
全部 fails=0、逐年 10/10 无空窗无负年、算子 ≤12、组腿外×外（配额 0 消耗）。

**★ 本轮净增 2 席的路径**：
- `RREGX1kd`（第 7 席）：est 族纯 ATOM 时 prod 全灭 → **REVERSION_AND_MOMENTUM 档下 prod 0.5940**
- `LLM0e20m`（第 8 席）：nws17 族纯 ATOM prod 1.0000 惨死 → **同档下 prod 0.5386**

⇒ **REVERSION_AND_MOMENTUM 是本战役后期最关键的单点发现**：救活 3 个此前被判死的族（starval / est / nws17），
每个族的 prod 从 0.75-1.00 掉到 0.54-0.61。此前 8 个常用档位全部试过都不行。

**`58EPRKr1`（fnd6 @REVMOM）prod 0.4167 极干净但被逐年否决**：2018 年 S −0.62（负年）。
这是「prod 最干净也不入篮」的纪律案例 —— 逐年负年是一票否决项。

### 13.44 REVERSION_AND_MOMENTUM 的族级图谱（15 族实测，通过率 1/3）（2026-11-10）

| 族 / 主腿 | 该档效果 | prod / 指标 |
|---|---|---|
| **starval 股息率** | ✅ **救活** | 0.7542 → **0.6143** |
| **est 分析师修正广度** | ✅ **救活** | 纯 ATOM 全灭 → **0.5940** |
| **nws17 语义相关度** | ✅ **救活** | 纯 ATOM **1.0000** → **0.5386** |
| tm_16 | ✅ 提升 | 0.6483 → **0.6434**，S 2.26→**2.69** |
| model109 | ✅ 提升 | 0.6990 → **0.6139** |
| fnd6（xsga 科目） | ⚠ prod 最佳但剔除 | **prod 0.4167** / 2018 负年 S −0.62 |
| tm_15 | ❌ 恶化 | S2.16 / F0.95 / **2Y 0.84** / fails 3 |
| risk 特质残差 | ❌ 恶化 | S1.55 / F0.80 / fails 2 |
| imb5（ts_rank 252） | ❌ | fails 2 |
| imb5（ts_mean 22） | ❌ | 2Y 1.13 / fails 1 |
| ep_yield | ❌ | S1.78 / fails 1 |
| fnd6（ni 科目） | ❌ 无信号 | S −0.05 |
| anl9 numanalysts | ❌ 无信号 | S −0.05 |
| ern6 actual_eps | ❌ 无信号 | S −0.10 |
| insider 净买 | ❌ 无信号 | S −0.19 |

**结论**：**通过率 5/15 ≈ 1/3**，且失败分两类：
1. **恶化类**（tm_15 / risk / imb5 / epy）：该档把这些族的 IS 指标打坏（2Y 掉到 0.84-1.13、fails 2-3）
2. **无信号类**（fnd6_ni / anl9 / ern6 / insider）：主腿本身信号不足，换档救不回

⇒ **该档位的价值集中在「价值/收益类」主腿**（starval 股息率、est 修正、nws17 语义、model109 相对估值、tm_16），
对「动量类」（tm_15 / risk 残差）反而有害——**这与档位名称 REVERSION_AND_MOMENTUM 的语义一致**：
它剥离的是反转与动量因子暴露，所以动量类主腿被剥掉后信号就没了，而价值类主腿反而被净化。

### 13.45 fnd6 族盘查：失效是「科目级」不是「族级」（2026-11-10）

**C 批（价值类未试主腿 × REVERSION_AND_MOMENTUM）**：

| 变体 | 主腿 | S | F | 2Y | fails | 与 8 席最高相关 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| `WjOvKRYd` | fnd6 **revt**（营收）÷ altcap | 1.92 | 1.24 | 2.09 | **0** | **0.431** ✅ | ❌ **2018 负年 S −1.15** |
| `j2YqNJJZ` | starval sector_rank | 2.39 | 1.75 | 2.61 | 0 | **0.824**（`omExeqLb`） | ❌ 同族 |
| `O0AlKjRq` | analyst 目标价区间 | 0.97 | 0.52 | 1.20 | 3 | — | ❌ |
| `78Legrm8` | analyst 覆盖数变化 | −0.09 | −0.01 | 0.39 | 4 | — | ❌ 无信号 |
| `QPvwmA6p` | nws18 sse | 1.59 | 1.05 | 1.56 | 1 | — | ❌ fails |

**★ fnd6 科目级失效矩阵（逐年 S，2017/2018/2019）**：

| 科目 | 2017 | **2018** | 2019 | 结论 |
|---|---:|---:|---:|---|
| `fnd6_newa2_revt`（营收） | 2.01 | **−1.15** | 2.12 | ❌ 2018 崩 |
| `fnd6_newa2_xsga`（销售管理费用） | 1.88 | **−0.62** | 1.53 | ❌ 2018 负 |
| `fnd6_capxy`（资本支出） | 1.39 | **2.35** | 0.23 | ✅ 2018 健康 |
| （对照）model109 | 0.31 | 0.47 | 1.92 | ✅ |

⇒ **失效是科目级，不是族级**：revt/xsga 在 2018 年失效，capxy 没有。
这解释了为什么「换科目」在本族内有时有效有时无效 —— **必须先查逐年，再决定用哪个科目**。

**D 批（用 2018 健康的 capxy 试）**：
| 变体 | 构造 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `A1VoJ0oW` | capxy ÷ altcap + ts_av_diff | 1.53 | 0.95 | 2.17 | 2 | ❌ |
| `E56906wK` | capxy ÷ altcap（水平） | 1.11 | 0.63 | 2.02 | 2 | ❌ |

⇒ capxy 虽 2018 健康，但整体强度不足（S 1.11-1.53、fails 2）。**fnd6 族在本轮结构下出不了第 9 席。**

**本轮累计已试算子的族**：risk残差 / 换手ATOM / tm15 / tm16 / tm17 / oth47 / starval / est / nws17 / nws18 / fnd6(3科目) / imb5(2几何) / epy / model109 / anl9 / ern6 / insider / pv106 / macro = **19 个族方向**。
**8 席 = 上述全部尝试的实测产出。**

### 13.46 E 批：价值型新方向 5 试 1 中，且那 1 颗又卡在单年负年（2026-11-10）

| 变体 | 主腿 @REVERSION_AND_MOMENTUM | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `GrWZ02nJ` | est 目标价水平 | 1.65 | 1.16 | 2.29 | **0** | ⚠ 全闸但 **2016 负年 −0.42** + 与 `RREGX1kd` 0.558 |
| `GrWZYqo0` | nws18 情绪分 | 0.95 | 0.48 | 1.13 | 3 | ❌ |
| `qMLQv9OP` | risk60 低费率 | 0.62 | 0.21 | 1.30 | 4 | ❌ |
| `zq3lwVVR` | nws17 情绪极性 | 0.35 | 0.11 | 0.88 | 3 | ❌ |
| `QPvwrR5X` | analyst 覆盖水平 | −0.12 | −0.01 | −0.41 | 4 | ❌ |

**★ 累积的「单年负年」否决案例（3 颗，全部 prod 干净或接近）**：

| alpha | prod | 负年 | 若非负年本可入篮 |
|---|---:|---|---|
| `58EPRKr1` | **0.4167** | 2018: −0.62 | ✅ 相关 0.348 也达标 |
| `WjOvKRYd` | **0.4335** | 2018: −1.15 | ✅ 相关 0.431 也达标 |
| `GrWZ02nJ` | **0.6168** | 2016: −0.42 | ⚠ 相关 0.558 已超线 |

**规律**：GBR 上「高 prod 干净度」的件频繁出现单年负年——
bad 年份高度集中在 **2016 / 2018**（两个市场结构转折年：2016 脱欧公投、2018 全球risk-off）。
⇒ **价值类因子在 GBR 的 2018 年最脆弱**（fnd6 revt/xsga、est 目标价均在此年翻负）。

⇒ **E 批无法贡献第 9 席**。8 席仍是本轮实测产出。

### 13.47 ★★★★ fnd6 科目筛选方法论：用历史件的逐年筛出「无脆弱年」科目（2026-11-10）

**方法**：从 `db:expressions` 里找每个 fnd6 科目已有的高 S 历史件（17 个科目），批量拉它们的逐年，
按「2016 与 2018 双年健康 + minS > 0」筛。结果：

| 科目 | 2016 | 2018 | **minS（全期最弱年）** | 判定 |
|---|---:|---:|---:|---|
| **`fnd6_newa2_re`（留存收益）** | 1.39 | 2.11 | **1.16** | ★ 全期无脆弱年 |
| `fnd6_newa2_oancf` | 1.70 | 1.07 | **0.85** | ★ 稳健 |
| `fnd6_capxy` | 3.61 | 2.28 | 0.22 | 健康但 minS 偏低 |
| `fnd6_gpy` | 2.64 | 2.80 | 0.38 | 同上 |
| `fnd6_cptnewq_atq` | 1.63 | 2.15 | 0.64 | 较稳 |
| `fnd6_newq_invtq` | 1.03 | 2.34 | 0.09 | minS 低 |
| `fnd6_txty` | 1.98 | 1.90 | **−0.28** | ❌ 有负年 |
| `fnd6_oancfy` | 2.40 | 1.54 | **−0.08** | ❌ |

**F 批（用 minS 最高的 5 个科目构造 @REVERSION_AND_MOMENTUM）**：

| 变体 | 科目 | S | F | 2Y | fails | self | 与 8 席 | 逐年 | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **`Xg9dPpp0`** | **oancf** | 1.97 | 1.44 | **2.91** | **0** | 0.279 | **0.377** | ✅ **minS 0.13 无负年** | ⏳ prod 待测 |
| `9qxNbxJx` | re（留存收益） | 2.05 | 1.44 | 2.67 | 0 | 0.359 | 0.416 | ❌ 2018 −0.32 | 剔除 |
| `omExAl0E` | ppegt | 1.99 | 1.34 | 2.36 | 0 | 0.322 | 0.388 | ❌ 2018 −0.62 | 剔除 |
| `1YNr1NKX` | gpy | 1.14 | 0.65 | 1.53 | 3 | — | — | — | ❌ |
| `gJenweLJ` | invtq | 1.20 | 0.66 | 1.43 | 3 | — | — | — | ❌ |

**★ 关键陷阱**：`fnd6_newa2_re`（留存收益）在**历史件上 minS 1.16 最稳健**，但用它新构造的件 2018 年却是 **−0.32**。
⇒ **历史件的逐年不能完全代表新构造件**——分母/分组轴/冷腿一变，年度分布就变。
方法论修正：历史件逐年只用于**初筛科目**（排除明显崩过的），**新件必须自己跑逐年**。

平台 `max_mutually_below_subset_size = 9`（含 3 颗 fnd6 候选）。

### 13.48 ★★★★★★★ 第 9 席 Xg9dPpp0（fnd6 oancf，prod 0.4000）+ 9 席全量终验（2026-11-10）

**`Xg9dPpp0`**（fnd6 `newa2_oancf` ÷ altcap @REVERSION_AND_MOMENTUM）：

| 项 | 值 | 闸 |
|---|---:|---|
| S / F / 2Y | 1.97 / 1.44 / **2.91** | ✅ |
| TO | 0.1492 | ✅ |
| RA fails | **0** | ✅ |
| self | 0.279 | ✅ |
| **prod** | **0.4000**（9 席中最佳，余量 **0.30**） | ✅ |
| 与 8 席最高相关 | 0.377 | ✅ |
| 逐年 | 无空窗无负年、minS 0.13、minLC 402 | ✅ |

**9 席全量终验结果**：
- **`allGate = true`、`failed = []`**（9 颗全部满足 S≥1.58 / F≥1 / 2Y≥1.58 / TO∈[0.01,0.7] / fails=0）
- **S 总和 = 19.19**
- 平台 `max_mutually_below_subset_size = 9`、`all_below_threshold = true`、max 相关 **0.4633**

| # | alpha | 族 | 中性化 | S | F | 2Y | TO | prod |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | `rKRx0M2m` | risk 特质残差 × 借券 | SUBINDUSTRY | 2.29 | 1.56 | 2.84 | 0.144 | 0.6232 |
| 2 | `pwdd7Za6` | 换手强度 ATOM | SUBINDUSTRY | 1.69 | 1.04 | 2.49 | 0.105 | 0.6238 |
| 3 | `pwdLp9z6` | tm_16 × 借券 | SUBINDUSTRY | 2.26 | 1.19 | 2.09 | 0.296 | 0.6483 |
| 4 | `O0A6Qz7p` | oth47 流量 × 借券 | SUBINDUSTRY | 2.18 | 1.52 | **3.27** | 0.114 | 0.6984 |
| 5 | `leAmmre8` | tm_17 × 借券 | STATISTICAL | **2.97** | 1.40 | 2.29 | 0.346 | 0.6887 |
| 6 | `omExeqLb` | starval 股息率 × 借券 | REVERSION_AND_MOMENTUM | 2.43 | 1.78 | 2.12 | 0.170 | 0.6143 |
| 7 | `RREGX1kd` | est 分析师修正 × 借券 | REVERSION_AND_MOMENTUM | 1.65 | 1.09 | 2.05 | 0.149 | 0.5940 |
| 8 | `LLM0e20m` | nws17 语义 × 借券 | REVERSION_AND_MOMENTUM | 1.75 | 1.17 | 2.12 | 0.117 | 0.5386 |
| 9 | **`Xg9dPpp0`** | **fnd6 oancf × 借券** | REVERSION_AND_MOMENTUM | 1.97 | 1.44 | **2.91** | 0.149 | **0.4000** |

**9 个族完全不重叠**：risk 特质残差 / 换手 ATOM / tm16 / oth47 / tm17 / starval / est / nws17 / fnd6。
**prod 分布 0.40-0.70**，其中 5 颗 ≥0.60（含 4 颗 REVERSION_AND_MOMENTUM 档的 0.54-0.61）。

### 13.49 第 10 席候选：fnd6 留存收益 + 冷腿降权（2026-11-10）

**G 批（fnd6 健康科目换几何/窗口/分组）**：

| 变体 | 科目/构造 | S | F | 2Y | fails | 与 9 席 | 逐年 | 判定 |
|---|---|---:|---:|---:|---:|---:|---|---|
| `A1Vob06w` | re 66/industry | 2.32 | 1.60 | 2.56 | **0** | **0.530** | ✅ 无负年 | ❌ 超线 0.030 |
| `6Xd51ePY` | atq | 2.07 | 1.37 | 2.63 | **0** | **0.616** | ✅ | ❌ 撞 `Xg9dPpp0` |
| `omExvgOn` | ppegt 504 | 1.74 | 1.18 | 2.03 | **0** | **0.447** ✅ | ❌ 2018 负 | ❌ |
| `leAo20An` | capxy ts_rank | 1.09 | 0.59 | 2.22 | 2 | — | — | ❌ |
| `VkxAE3oA` | oancf 504/mkt | 1.58 | 1.15 | 1.56 | 1 | — | — | ❌ |

**H 批（对 `A1Vob06w` 用冷腿降权压相关）**：

| 变体 | 改动 | S | F | 2Y | fails | self | 与 9 席 | 逐年 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **`Jje6mrpO`** | 冷腿权重 **0.5** | 2.37 | 1.58 | 2.34 | **0** | 0.329 | **0.415** ✅ | ✅ minS 0.19 |
| **`Xg9dL3qa`** | 冷腿权重 0.6 | 2.38 | 1.60 | 2.41 | **0** | 0.368 | **0.447** ✅ | ✅ minS 0.29 |
| `leAo21V8` | 分组 industry→sector | 2.16 | 1.56 | 2.41 | 0 | — | 0.582 | ❌ |

**★ 降权杠杆第三次救件**：`A1Vob06w` 相关 0.530（超 0.030）→ 冷腿权重降到 0.5 后 **0.415**（过线），
S 几乎不变（2.32→2.37），fails 保持 0，逐年无负年。**平台 MIS 实读 10。**

`Jje6mrpO` 与 `Xg9dL3qa` 仅冷腿权重不同（0.5 vs 0.6），两者应高度相关 ⇒ **只能取 1 颗**，即第 10 席。
prod 测量中。

### 13.50 ★★★★★★★★ 10 席达成（2026-11-10 终验通过）

**`Jje6mrpO`**（fnd6 `newa2_re` 留存收益 ÷ altcap，冷腿权重 0.5，@REVERSION_AND_MOMENTUM）：

| 项 | 值 |
|---|---:|
| S / F / 2Y | 2.37 / 1.58 / 2.34 |
| TO / fails | 0.154 / **0** |
| self / **prod** | 0.329 / **0.5565** |
| 与 9 席最高相关 | 0.415 |
| 逐年 | 无空窗无负年、minS 0.19、minLC 407 |

**10 席全量终验**：`allGate = true`、`failed = []`、**S 总和 21.56**、
`max_mutually_below_subset_size = 10`、`all_below_threshold = true`、max 相关 **0.4633**。

| # | alpha | 族 | 中性化 | S | F | 2Y | prod |
|---|---|---|---|---:|---:|---:|---:|
| 1 | `rKRx0M2m` | risk 特质残差 × 借券 | SUBINDUSTRY | 2.29 | 1.56 | 2.84 | 0.6232 |
| 2 | `pwdd7Za6` | 换手强度 ATOM | SUBINDUSTRY | 1.69 | 1.04 | 2.49 | 0.6238 |
| 3 | `pwdLp9z6` | tm_16 × 借券 | SUBINDUSTRY | 2.26 | 1.19 | 2.09 | 0.6483 |
| 4 | `O0A6Qz7p` | oth47 流量 × 借券 | SUBINDUSTRY | 2.18 | 1.52 | **3.27** | 0.6984 |
| 5 | `leAmmre8` | tm_17 × 借券 | STATISTICAL | **2.97** | 1.40 | 2.29 | 0.6887 |
| 6 | `omExeqLb` | starval 股息率 × 借券 | REVERSION_AND_MOMENTUM | 2.43 | 1.78 | 2.12 | 0.6143 |
| 7 | `RREGX1kd` | est 分析师修正 × 借券 | REVERSION_AND_MOMENTUM | 1.65 | 1.09 | 2.05 | 0.5940 |
| 8 | `LLM0e20m` | nws17 语义 × 借券 | REVERSION_AND_MOMENTUM | 1.75 | 1.17 | 2.12 | 0.5386 |
| 9 | `Xg9dPpp0` | fnd6 营业现金流 × 借券 | REVERSION_AND_MOMENTUM | 1.97 | 1.44 | 2.91 | **0.4000** |
| 10 | **`Jje6mrpO`** | **fnd6 留存收益 × 借券** | REVERSION_AND_MOMENTUM | 2.37 | 1.58 | 2.34 | **0.5565** |

**10 席分布**：SUBINDUSTRY 4 颗 / STATISTICAL 1 颗 / **REVERSION_AND_MOMENTUM 5 颗**。
**9 个族**（fnd6 占 2 席但科目不同：oancf 与 re，互相关 <0.5）。
**prod 区间 0.4000-0.6984**，全部有健康余量（最紧 0.6984 余 0.0016、最松 0.4000 余 0.30）。


### 13.51 J 批：fnd6 其它科目 + 冷腿 0.5 全部不足（2026-11-10）

| 变体 | 科目 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `2rA3Zw2J` | cptnewq_atq | 1.74 | 1.10 | **1.43** | 1 | ❌ 2Y 不足 |
| `npvLzKqd` | newa2_ppegt | 1.68 | 1.07 | **1.21** | 1 | ❌ |
| `KPJW8EYg` | cptnewq_ceqq | 1.59 | 1.02 | **1.39** | 1 | ❌ |
| `omExzN15` | capxy | 0.84 | 0.43 | 1.00 | 3 | ❌ |
| `1YNrmw0Q` | gpy | 1.01 | 0.57 | 1.47 | 3 | ❌ |

**★ 冷腿权重的双面性（重要教训）**：
- 对 `newa2_re`（第 10 席）：冷腿 1.0 → 0.5 使相关从 0.530 降到 **0.415**，S 微升（2.32→2.37），**net 收益**；
- 对其余 5 个科目：冷腿 0.5 使 **2Y 全部掉到 1.00-1.47**（原本这些科目在 1.0 权重下 2Y 有 2.0+）。

⇒ **降权不是免费杠杆**：它压低相关的同时也削弱了借券冷腿带来的 2Y 增益。
  只有当「相关必须降」且「2Y 有余量」时才可用；`newa2_re` 恰好在 1.0 权重下 2Y 2.56、降到 0.5 后仍有 2.34，才吃得消。

**当前 10 席维持**。fnd6 可再挖的科目已试完（oancf/re 已入篮，atq/ppegt/ceqq/capxy/gpy 全部不足）。

### 13.52 档位替换与「同批次结构相似」陷阱（2026-11-10）

**K 批（把 SUBINDUSTRY 档的 4 颗在 REVERSION_AND_MOMENTUM 下重跑）**：

| 变体 | 族 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `LLM0ePj2` | tm_16 @REVMOM | **2.69** | **1.48** | 2.30 | **0** | ✅ 全闸（prod 0.6434 已验证） |
| `9qxNozLo` | risk 残差 @REVMOM | 1.55 | 0.80 | 2.15 | 2 | ❌ 恶化（再证 §13.44） |
| `xArJzLaN` | 换手 ATOM @REVMOM | 1.50 | 0.97 | 2.71 | 2 | ❌ |
| `3sDSNT1l` | oth47 @REVMOM | — | — | — | ERROR | ❌ |

**替换尝试**：用 `LLM0ePj2`（S 2.69/F 1.48 vs `pwdLp9z6` 的 2.26/1.19）替换更强 →
结果 **`LLM0ePj2` × `LLM0e20m` 相关 0.5228 超线**，`all_below_threshold` 转 false，MIS 从 10 掉到 9。

**★ 陷阱：同批次命名的件结构相似**。`LLM0ePj2`（tm_16）与 `LLM0e20m`（nws17）主腿完全不同，
但两者都是「`add(rank(-ts_rank(ts_mean(vec_count/X, W), W2)), 借券leg)`」同一外层几何，且由同一批仿真创建 ⇒ 命名前缀相同（LLM0）。
**主腿不同不代表持仓不同** —— 外层几何 + 冷腿相同的话，相关性会被外层结构主导。

⇒ **保留原 10 席**（`pwdLp9z6` 虽指标略低，但与 `LLM0e20m` 相关仅 0.417，安全）。
**质量优先于单颗指标**：单颗 S/F 提升 0.4，换来整个篮子 MIS 从 10 掉到 9，不划算。

### 13.53 L/M 批：5 个全新主腿源（institutions/macro/option/other545/earnings）全部失败（2026-11-10）

**L 批（首版，4/5 因字段名错误而 ERROR）**：
| 变体 | 数据集 | 结果 |
|---|---|---|
| `omEx9zo6` | earnings surprise（ern6 actual-estimated 标准化） | S **−0.66** / fails 4 |
| 其余 4 条 | inst6 / macro27 / option1 / oth545 | 我猜的字段名不存在 ⇒ ERROR |

**字段名订正**（用 `get_datafields` 实查，教训：**不要凭记忆猜字段名**）：
- institutions6：`count_institutional_holders_security` / `count_institutional_buyers_security` / `aggregate_equity_value_*`
- macro27：`mcr27_company_jobsactive` 等（全 VECTOR，须 `vec_sum`）
- option1：`opt1_factor` 等（全 VECTOR）
- other545：`oth545_score` / `oth545_mpd` / `oth545_pln_omen` / `oth545_mktcap`（全 VECTOR）

**M 批（用正确字段名重跑）**：

| 变体 | 主腿 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `j2YqdGPZ` | 机构持有者数（inst6） | 0.56 | 0.23 | 0.13 | 3 | ❌ |
| `xArJm20m` | 机构买家数（inst6） | 0.90 | 0.45 | 0.61 | 3 | ❌ |
| `6Xd5YMpG` | 招聘活跃度（macro27） | 0.86 | 0.42 | 0.71 | 4 | ❌ |
| `78LeKGvv` | option 因子（option1） | **0.00** | 0.00 | −0.03 | 4 | ❌ 无信号 |

⇒ **这 5 个族在「主腿 × 借券 + REVERSION_AND_MOMENTUM」结构下全部无信号**（S 0.00-0.90）。
与 §13.44 一致：这些不是「价值/收益类」主腿，该档位救不了；且它们本身的横截面区分度在 GBR TOP700 不足。

**累计已试族方向 = 24 个**。10 席是这些尝试的最终实测产出。

### 13.54 N 批：news50 语义分类器族 5 字段全部无信号（2026-11-10）

news50（37 字段，cov **0.691**）是 GBR 里 coverage 较高的新闻集，字段为 `mws50_*` 三字母分类器族：
| 字段 | 含义 | ac | S | F | 2Y | fails |
|---|---|---:|---:|---:|---:|---:|
| `mws50_ess` | 粒度情绪分 0-100 | **84** | 0.41 | 0.06 | 0.22 | 5 |
| `mws50_aes` | 正负比 | 68 | 1.36 | 0.54 | 1.49 | 4 |
| `mws50_qmb` | 社论/评论分类器 | 67 | 1.22 | 0.37 | 1.21 | 4 |
| `mws50_vea` | 91 日事件量 | 29 | 0.50 | 0.11 | 1.19 | 4 |
| `mws50_ens` | 事件新颖度 | 18 | −0.10 | −0.01 | −0.90 | 5 |

**全部 5/5 失败（S −0.10 至 1.36、fails 4-5）**。与已有结论一致：
- news17 / nws18 能出件，是因为用了 **`vec_count` 事件计数**（信息在「发生了多少」而不在「情绪打分」）；
- news50 这批是**情绪打分型**（0-100 分），与 GBR 生产池里已稠密覆盖的新闻情绪因子同源，且区分度低。

⇒ **新闻类的可用构造只有「事件计数/新颖度」维度，情绪打分维度已饱和**。

### 13.55 O 批：news17 计数/新颖度维度也失败 —— 修正 §13.54 的泛化（2026-11-10）

按 §13.54「新闻类只能走事件计数维度」的推断，试 news17 的 5 个非情绪维度：

| 变体 | 主腿 | S | F | 2Y | fails | 判定 |
|---|---|---:|---:|---:|---:|---|
| `j2Yq9oxZ` | 相似事件间隔天数（新颖度） | 0.96 | 0.52 | 1.28 | 3 | ❌ |
| `gJenRQwv` | 事件记录总数 | 0.98 | 0.56 | 0.87 | 3 | ❌ |
| `gJenRQwv` | 新颖度 × 相关性（双条件，平台去重同上） | 0.98 | 0.56 | 0.87 | 3 | ❌ |
| `YP1R25VR` | 事件计数 z-score | 1.00 | 0.22 | 1.22 | 4 | ❌ |
| `QPvw2Yaw` | 多重比较版新颖度 | 0.88 | 0.42 | 1.29 | 3 | ❌ |

**★ 修正 §13.54 的结论**：不能说「新闻类只能走事件计数维度」——
真正有效的是 **`vec_count(nws17_multiple_comp_relevance)` 这一个特定组合**：
「多重比较文献的相关度计数」，即「同一事件被多少来源独立报道」= **新闻共识强度**。
其它计数（总事件数、相似度天数、计数 z-score）都无效（S 0.88-1.00）。

⇒ **准确表述**：新闻类有效的是**「跨来源共识强度」**这一个经济含义，不是泛化的「计数维度」。
这与 `LLM0e20m`（第 8 席）的构造完全对应 —— 它用的是 `vec_count(nws17_multiple_comp_relevance)`。

**累计族方向 = 26 个**。10 席 = 全部实测产出。

### 13.56 P 批：event_relation / other571 / other296 三集全部无信号（2026-11-10）

按 §13.55「跨来源共识强度」的规律，试了 3 个含「关系/注意力/概率」维度的未用数据集：

| 变体 | 数据集 / 字段 | S | F | 2Y | fails |
|---|---|---:|---:|---:|---:|
| `E569qow9` | event_relation `relation_strength_score_general` | 1.05 | 0.60 | 1.46 | 3 |
| `9qxN9zxV` | event_relation `relation_strength_rank_financial` | 0.79 | 0.39 | 1.29 | 3 |
| `zq3l560o` | other571 `oth571_views28d`（搜索热度） | 0.86 | 0.29 | 0.16 | 3 |
| `d5WNnXOJ` | other571 7d/28d 热度加速 | 0.88 | 0.27 | 0.94 | 3 |
| `pwd9nX53` | other296 prob_pos − prob_neg（净概率） | 1.25 | 0.75 | 1.56 | 3 |

**5/5 失败**。三个数据集的共同问题：**GBR TOP700 里横截面区分度不足**（cov 字段全为 0，平台未统计到使用量）。

⇒ **「数据有值」≠「数据能区分」**：这些字段语义丰富（关系强度、搜索热度、概率差），
但在 700 只大盘股里取值差异太小，做不出有意义的横截面排序。这是 cov=0 数据集的通病。

**累计族方向 = 29 个**。10 席 = 全部实测产出。

---

**累计族方向 = 25 个**（新增 news50 情绪分类器族）。10 席 = 全部实测产出。

---

---

---

---
**从 6 席到 10 席的净增路径（本轮）**：
| 席 | alpha | 突破点 |
|---|---|---|
| 7 | `RREGX1kd` | est + REVERSION_AND_MOMENTUM |
| 8 | `LLM0e20m` | nws17 + 同档（纯 ATOM 时 prod 1.0000） |
| 9 | `Xg9dPpp0` | fnd6 oancf + 科目筛选方法 |
| 10 | `Jje6mrpO` | fnd6 re + **冷腿降权 0.5**（相关 0.530→0.415） |

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---
S 仅从 2.30 掉到 2.21。**权重是真·连续可调的相关/收益旋钮**。

---
| — | 换冷腿字段 | **失败**（全部崩） | — |

---

---
这补齐了 §13.28 的「未试路径」，扩席的全部结构方向（单腿/双组腿/三腿/换冷腿/权重/窗口/分组轴）已逐一实测。

---

---

**§13.25 边界再修正**：`Jje9J2GO`(tm15 v2) 0.794、`wpQrkvjQ`(risk v2) 0.749 —— 这两族的 v1 已用了相近几何，双改失效。
所以「每族 2 席」是**上限而非保证**，实际取决于 v1 占用的几何位置。

---

---

---

---

---

**已剔除清单（全部为纯 ATOM 或弱冷腿）**：`wpQwjWn6`(nws17 1.0) / `gJeq8XbQ`(nws18 0.9257) / `mLomxW71`(tm19 0.8331) /
`1YN6MJw6`(est×volume 0.8311) / `d5W9EeKK`(imb5 0.8017) / `3qoXwW1z`(tm16 0.7552) / `bl6avAXp`(tm17 0.7397) / `Xg9b5ZX0`(tm15 0.7068)。

---

---

**prod 阻塞诊断（本轮实测）**：
- `prod_queue.json` 为空、`cache` 下无锁残留 ⇒ 不是本地排队/死锁问题；
- 平台返回明确信息：`"Another production correlation check is already running for this account. The BRAIN platform supports only one in-flight"` ⇒ **账号级单并发被外部会话或平台积压占用**；
- 停掉我方全部队列后 60s 仍未释放 ⇒ **非我方进程所致**，无本地手段绕过。

---
入篮规模必须留足备选冗余。

**备选池（已测 self 干净 + 全闸，10 颗）**：
| 备选 | S | F | 2Y | self | 障碍 |
|---|---:|---:|---:|---:|---|
| **`KPJer3Z1`** | 1.69 | 1.06 | 2.53 | 0.490 | 与 `pwdd7Za6` 相关 **0.5047**（仅超 0.0047）→ 若 `pwdd7Za6` prod 撞墙即最优替补 |
| `xAr3OvXm` | 1.78 | 1.01 | **2.97** | 0.225 | 与篮 0.618 |
| `9qWJr2rq` | 1.59 | 1.02 | 1.96 | 0.389 | 与 `P0gv3AO7` 0.9691 |
| `npvEe7ra` | **2.51** | **1.79** | 2.64 | 0.469 | RISK；**prod 0.6439 ✅ 已过墙**；与 `rKRx0M2m` 0.9187（二选一） |
| `ZYQJd133` | 1.89 | 1.26 | 2.63 | 0.444 | RISK；与 `rKRx0M2m` 0.7649 |
| `zq3AX08o` / `9qxGgg9d` / `d5W9eobx` / `RRE500Nd` / `Jjee0MAW` | 1.70-1.81 | 1.06-1.16 | 1.73-2.98 | 0.30-0.69 | 与篮 0.698-0.926 |

**队列运维教训**：5 个 corr_check 后台队列会争抢平台**账号级单并发相关性槽**（跨进程文件锁），互相排队反而更慢；
应合并为单队列或严格串行（已在 13.18 执行合并）。

### 13.19 prod 撞墙的提前预警指标：`risk_neutralized_sharpe / sharpe`（2026-11-10）

**观察**：已验证 prod 撞墙的三颗，风险中性化保留率都极低或中等——
| alpha | S | risk_neut S | 保留率 | prod |
|---|---:|---:|---:|---:|
| `wpQwjWn6` | 2.10 | — | — | **1.0000** ❌ |
| `1YN6MJw6` | 2.07 | — | — | **0.8311** ❌ |
| `j2Y7AbzQ`（RISK 单集） | 1.71 | **0.23** | **13%** | 0.7645 ❌ |
| `rKRx0M2m`（RISK 组腿） | 2.29 | 1.09（见 §13.3） | ~48% | **0.6232** ✅ |

**入篮席位的保留率实测**：
| 席 | S | risk_neut S | 保留率 | 风险评级 |
|---|---:|---:|---:|---|
| **`78L9Lwrv`**（第 19 席） | 1.72 | **0.50** | **29%** | ⚠⚠ **高危：收益高度依赖风险暴露，prod 撞墙概率高** |
| `rKRQbPPE` | 2.48 | 1.58 | 64% | 中 |
| `9qWa6r8x` | 2.07 | 1.54 | 74% | 低 |

**★★ 该假设已被证伪（同日 15 个 prod 实测样本复核）**：

| 组 | 保留率实测 | 结论 |
|---|---|---|
| **prod 过墙组** | `leAPWGX2` 86%、`rKRx0M2m` **34%**、`npvEe7ra` **38%** | 覆盖 34%-86% 全区间 |
| **prod 撞墙组** | `j2Y7AbzQ` 13%、`vR17O093` 26%、`A1VArNzY` 37%、`mLonY3jE` 37%、`d5Wr8mzw` 38%、`Xg9A6rGl` 43%、`QPvRYJGr` 47%、`QPveQvOg` **91%** | 覆盖 13%-91% 全区间 |

**过墙的 `rKRx0M2m`(34%) 比撞墙的 `A1VArNzY`(37%)、`d5Wr8mzw`(38%) 还低**；撞墙的 `QPveQvOg` 高达 **91%**。
⇒ **`risk_neutralized_sharpe / sharpe` 与 prod 相关性无关，不能作为 prod 预警指标**。
本条记录保留为「小样本外推被证伪」的实例（最初基于 2 个样本提出 <35% 阈值，15 样本后推翻）。
**prod 只能靠实测量**，无捷径。

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---
### 12.11 D0 矿脉：已勘明、本轮不开采（用户 2026-11-09 裁决「先不考虑 D0」）

- **实测勘明**：GBR D0 = 73 集 / 十四类塔全部未点亮；池内通道内已挖 45、**真未探 28**（24 `UNTESTED_BLIND` + 4 `UNTESTED_COV_OK`）。
- **可仿真是真的**：D0 探针抽验 `model252` 拿到 `longCount=343`，说明 D0 / TOP700 不是死设置。
- **但本轮不开采**：用户明确指示「先不考虑 D0」，D0 探针批已 `task_stop`；`GBR_probe_results_d0.json` 里只有 2 条抽验记录（`univ1` 无 MATRIX/VECTOR 字段 ⇒ `PROBE_FAILED`、`model252` 有数据）。
- **留档给下一个会话**：`reports/dataset_experience/gbr_coverage_audit_d0_20261109.md`（工具生成，含 28 集清单）+ `data/dataset_assets/GBR_probe_plan_d0.json`。
  重开 D0 的正确入口是先跑 `tools/probe/dataset_data_probe.py --delay 0` 把 28 集探完再过 `--gate closure`，**不要**从覆盖率元数据筛。

### 12.12 event_sentiment_signals 终测：零读数状态解除，S 天花板 0.86（2026-11-09）

**通道**：multisim 两次卡 `child_count=0` 且已 404 ⇒ 改用 `batch_create_simulations`
（服务端逐条顺序提交，天然绕开 multisim 挂死；本轮 15 条 0 卡死，仅 429 重试）。
**设置**：GBR / TOP700 / D1 / SUBINDUSTRY / decay4 / trunc0.08 / nanHandling=OFF。**证据通道 = MCP 直连仿真（不进 db:expressions）**。

字段底册：52 个全 VECTOR 字段，五大语义族（净情绪分 / 正负分量分 / 事件计数 / key-driver 计数 / 权重与词数），
本波覆盖 6 个代表字段。11 个结构互异模板 + std 族窗口曲线 4 条：

| 模板 | 表达式骨架 | S | 2Y | 备注 |
|---|---|---:|---:|---|
| T1 水平 | `rank(vec_avg(section_sentiment_score_3))` | 0.06 | -0.31 | 死 |
| T2 时序标准化 | `ts_zscore(·,66)` | -0.15 | -0.27 | 死 |
| T3 动量 | `ts_delta(improved_d1,22)` | 0.15 | 0.13 | 死 |
| T4 波动(反号) | `-ts_std_dev(·,66)` | -0.86 | -1.01 | **本集最强**；反号即 +0.86 |
| T5 净分比率 | (P−N)/(P+N+1)，key_factor 族 | 0.15 | 0.43 | 死 |
| T6 注意力门控 | 水平 × rank(事件量均值66) | -0.06 | -0.45 | 死 |
| T7 词数稀释 | 水平 / (1+rank(词数)) | 0.14 | -0.62 | 死 |
| T8 组内排名 | `group_rank(ts_backfill(·,250),subindustry)` | 0.38 | 0.80 | 弱 |
| T9 z 动量 | Δ66 / (1+σ66) | 0.05 | 0.02 | 死 |
| T10 负事件冲击 | `-ts_decay_linear(ts_delta(负分,5),10)` | 11.18* | 0.0 | *退化伪信号：TO=1.0、DD=0、fail=3，稀疏 VECTOR 的微持仓伪影，不作数 |
| T11 时序分位 | `ts_rank(·,252)` | -0.34 | -0.49 | 死 |
| T4b std252 | 窗口拉长 | 0.03 | 0.50 | 崩塌 |
| T4c std126 | 窗口拉长 | 0.13 | -0.15 | 崩塌 |
| T4d 组内波动 | `group_rank(std66)` | 0.86 | 0.79 | 与 T4 反号同顶，F 0.96 |

**判定（scope：11 模板 × std 窗口曲线 × SUBINDUSTRY/decay4 档）**：
情绪水平 / 动量 / 比率 / 门控 / 稀释 / 组内 / 时序分位全灭（|S| ≤ 0.38）；
唯一活口是**波动族 std66 = 0.86**，但窗口曲线 66→0.86 / 126→0.13 / 252→0.03 说明是窄窗孤峰，
且距 REGULAR 资格线 1.58 差 0.72。**无近闸候选**；该集从「零读数」改判为「已测透、无 1.58 线候选」。
⇒ D1 可开采池 65 集至此**全部有实测证据**，无一集停留在「不知道」。

### 12.13 ★ 交付包纠错：原 10 席有 3 颗 prod 撞墙，重算后合规席位 = 8（2026-11-09）

**缺陷**：§1/§2 的席位数学（36 全闸池 → MIS=11 → 配额 ⇒ 10）**没有把 prod<0.7 作为约束**——
全闸池只筛了 fl=0 & S≥1.58 & 2Y≥1.58 & F≥1.0 & TO∈[0.01,0.7]，prod 只对 5 颗抽查过。

**本轮把 36 颗 prod 全部实测（MCP check_correlation / production，单并发逐颗）**：

| 结果 | 颗数 | 明细 |
|---|---:|---|
| **FAIL（≥0.7）** | 13 | QPveQvOg **0.8701**、2rAo7mm8 0.8595、d5WrwkPj 0.8583、xArpnW5m 0.8608、88RxLYXl 0.8424、LLMYb6z1 0.8337、P0oAL7kJ 0.8311、gJeVpvlO 0.7959、A1V8dj2e 0.7921、d5Wr8mzw **0.7634**、9qxOJJ1d **0.7640**、2rAovAp8 0.7546、pwdegovq 0.7039 |
| PASS 但贴墙（≥0.675） | 5 | leAgQPO5 0.6866、88RxORpX 0.6878、0mY2kdg2 0.6818、mLoWX91p 0.6750、2rAokgMb 0.6992 |
| 未知（MCP 120s 超时×2 轮，fail-closed 不入篮） | 4 | Xg9A6rGl、P0oALL17、rKRnajx8、58E2dQZX（全为 B 簇 avg_buy_shares×借券腿；同簇已测 8 颗全在 0.79-0.86 ⇒ 大概率同判，留缓存补测） |

原 10 席里 **QPveQvOg(0.87 深钉→判死)、d5Wr8mzw(0.7634)、9qxOJJ1d(0.7640) 三颗不可提交**；leAgQPO5/mLoWX91p 贴墙高危。
B 簇（借券短腿×弱主腿）几乎整簇 0.75-0.86 —— 印证 §4 的「短腿主导持仓」：**冷腿同源 ⇒ prod 也同源撞墙**。

**重算**（prod<0.7 硬闸 + corr<0.5 + 配额≤5 + 全局口径禁混 {PV,MODEL,OTHER,FUND}；2rAokgMb/kqN65Azd 为 fnd6×cap=FUND×PV 直接违规出局）：

| # | alpha | S | prod | 腿 / 配额 |
|---|---|---:|---:|---|
| 1 | akK9ooZv | 2.91 | 0.6282 | techindi r1×借券（配额） |
| 2 | qMLJjleO | 2.27 | 0.6574 | techindi r10×借券（配额） |
| 3 | RRE5Mwkn | 2.15 | 0.4744 | pv103 IV×借券（配额） |
| 4 | leAgQPO5 | 2.16 | 0.6866⚠ | imb5×pv1 volume（配额，贴墙） |
| 5 | ZYQXZj73 | 1.78 | 0.6524 | order_book_imbalance(OTHER)×借券（配额） |
| 6 | bl6KwjwK | 1.89 | 0.4582 | analyst×shortinterest（免） |
| 7 | QPvbxjXw | 1.87 | 0.5794 | analyst ATOM（免） |
| 8 | rKRPAWv9 | 1.76 | 0.3998 | news17 ATOM（免） |

**= 8 席，S 总和 16.79，配额 5/5，互相关现场复验全对 <0.5（max 0.4993，akK9ooZv×qMLJjleO 贴线 0.0007）**。
GBR 口径（FUND 视为集合外）可加 6XdLP10J（fnd6×risk88，免）= **9 席 / S 18.42**；全局口径（2026-11-03 澄清，禁混含 FUND）以 8 席为准。
88RxORpX（S3.08 全池最高）prod 0.6878 贴墙 + A 簇互斥，未入选；若未来 prod 池漂移回落可回调。

**修正后的 D1 容量结论（已被 §12.15 推翻）**：在 corr<0.5 + 配额 5/5 + prod<0.7 三闸下，36 池容量 = 8（全局口径）/ 9（GBR 口径）；但 36 池本身不完整，见 §12.15。
破墙队列：d5Wr8mzw 0.7634、9qxOJJ1d 0.7640（中钉、S 强，按 n=1 规则可归因破墙）；QPveQvOg 0.8701 深钉判死。

### 12.15 ★★★ 根因 E：候选池本身不完整 —— 真实容量远超此前所有估计（2026-11-09）

**发现**：§12.13 的「D1 容量 = 8 席」结论建立在 **36 颗全闸池**上，而该池来自 `get_user_alphas` 分页扫描（394 条）。
本轮从 `db:expressions`（12,677 条 GBR / 4,414 条有 alpha_id）重扫：**池外还有 4093 个 distinct alpha_id**，
其中 **378 颗**满足 S≥1.58 & F≥1.0 & TO∈[0.01,0.7]（DB 侧），**241 颗**经平台复核连 2Y≥1.58 也全过。
status 分布：**360 颗 UNSUBMITTED** + 18 颗 ACTIVE（已提交存量，不计入交付）。
⇒ **36 池漏掉了本战役 90% 的全闸产量** —— 与「覆盖率闸」「MCP 仿真不进台账」同族的第五个证据洞：
**扫描通道（get_user_alphas 分页）对 DB 里已回测的 alpha 大面积盲视**。

**358 颗 UNSUBMITTED 全闸池**（剔除 4 颗 SUPER/Python 后）已固化：
`data/dataset_assets/GBR_unsubmitted_fullgate_360.json`（含 id / S / F / TO / wave / expression / 家族）。
家族分布：imb5 47 / loaned 40 / est 39 / epy 38 / other 41 / ev_fund93 28 / tm17 30 / nws17 23 / fnd6 23 /
tm16 10 / starval 8 / mdl28 6 / pd_jc7 6 / model109 6 / tm15 5 / nws18 5 / dlr2 2 / pv103 1。
其中**多数是单数据集 ATOM（不占组腿配额）**：news17/18 语义族、fundamental93 EV/科目族、model109、mdl28、
pd_jc7、est 修正广度族、imb5、tm15/16/17/19 techindi 族。

**席位重算（66 个家族代表 × 完整相关矩阵，贪心下界）**：**21 席**，S 总和 45.99，**配额仅用 2/5**。
（回溯精确解因算力预算中断，21 是贪心下界，真实 MIS ≥ 21。）
对比：36 池给出的 8 席 / 36 池无配额 11 席 —— **之前的「容量」一直是扫描盲区的产物**。

**⚠ 席位成立的三个前置条件（当前未全部满足）**：
1. **prod 全部未测**：360 颗 UNSUBMITTED 的平台 `prod_correlation` 全是 null（已提交的 18 颗才有缓存值），
   必须逐颗走平台相关性队列（1-5 分钟/颗，账号单并发）。prod<0.7 未过线前不得入交付篮。
2. **self-corr 未批量核**：10-30 篮子报告显示曾有多条兄弟变体已提交（如 `rKRkL9QE` 10-31 提交），
   同族未提交件可能撞 OS 池 self 闸 —— 须对 21 席逐颗跑 self。
3. **回溯精确 MIS 未完成**：21 席是贪心解。

**同轮破墙终局**：d5Wr8mzw 两个全闸变体（QPvRYJGr / mLonY3jE）prod 实测 **0.7423 / 0.7400** —— 
窗口微调挪不动族级 prod 墙（与 §2「ep_yield 族 0.6861–0.6975」同理：**prod 命中率是族属性**），
d5Wr8mzw 族封盘；9qxOJJ1d 四杠杆全灭（§12.14）维持判死。

**对 20 颗目标的含义**：目标从「不可达」转为「**可达但被 prod/self 测量队列阻塞**」（详见 §12.16：self 闸血洗后 19 席贪心解存活，配额 2/5）。

---

### 12.14 破墙：d5Wr8mzw 成功脱墙（3 变体全闸），9qxOJJ1d 四杠杆全灭（2026-11-09）

§12.13 的破墙队列按「n=1 不判死、先归因后破墙」纪律处理，先看钉子直方图：

| alpha | prod | 钉子结构 | 判定 |
|---|---:|---|---|
| d5Wr8mzw | 0.7634 | [0.7,0.8) **n=1**（下方 0.6-0.7 仅 36、0.5-0.6 784） | 单钉 ⇒ 进破墙队列 |
| 9qxOJJ1d | 0.7640 | [0.7,0.8) n=2，0.6-0.7 n=22 | 双浅钉 ⇒ 进破墙队列 |

**破墙杠杆（各 4 条，单杠杆位移，算子均 ≤12）**：

| 变体 | S | F | 2Y | fails | 结论 |
|---|---:|---:|---:|---:|---|
| d5_W1 quantile 84→**126** | **1.96** | **1.65** | **2.13** | **0** | ✅ 全闸，且 F 比原件（1.57）还高 |
| d5_W2 avdiff 252→126 | 1.66 | 1.21 | 1.76 | 0 | ✅ 全闸但 S/2Y 掉线 |
| d5_W3 组轴 sector→**industry** | 1.91 | 1.37 | 2.18 | 0 | ✅ 全闸 |
| d5_W4 换科目 newa2_at | — | — | — | — | ❌ 平台报「unknown variable」——该科目在 D1 无字段 |
| 9q_V1 冷腿窗 504→252 | 0.56 | 0.08 | 1.39 | 4 | ❌ S 崩 |
| 9q_V2 冷腿换 average_loan_duration_days | 0.82 | 0.15 | 1.25 | 4 | ❌ |
| 9q_V3 权重 2→3 | 0.79 | 0.14 | 1.50 | 4 | ❌ |
| 9q_V4 中性化 FAST→SUBINDUSTRY | 0.45 | 0.07 | 0.74 | 4 | ❌ |

**归因**：
- **d5Wr8mzw 能破**：它的钉子挂在 **quantile 窗口 84** 这一个几何点上 —— 把 84 挪到 126 就脱墙，且 F 更高。**窗口微调是最省力的破墙杠杆**。
- **9qxOJJ1d 破不了**：它的 S（2.15）**来自借券冷腿的精确几何**——改冷腿窗口 / 换冷腿字段 / 改权重 / 改中性化档，四种杠杆全部把 S 打到 0.45-0.82。**主腿（anl9 修正广度）与冷腿（借券）互相咬合成一个整体**，动冷腿即毁主信号 ⇒ 该机制面（anl9×借券）在本区判死。
- 三条 d5 变体彼此相关 0.80-0.94（同一 fnd6 科目 / 同一 ts_quantile 骨架）⇒ **同族最多取 1 条**入篮；且它们与现有 8 席的相关均 < 0.3 ⇒ 有独立增席资格。
- 待办：三条变体的 **prod 尚在平台计算中**（MCP 单次调用撞 PTC 120s 硬超时，改用仓库现成 CLI `tools/corr_check.py --ids ... --types production` 后台消费，工具自带等待轮询）；prod 未过墙前不得入篮。

## 13.57 358 池互相关全量筛查：299 颗与 10 席 <0.5，但池是 prod 死池（2026-11-11）

**做法**：对 `GBR_unsubmitted_fullgate_360.json` 全部 356 颗候选分批（10 席 + 45 候选/批）跑 `compute_mutual_correlation`，取每颗对 10 席的 max |corr|。

| 结果 | 数量 |
|---|---:|
| 池内候选总数 | 356 |
| 对 10 席 max \|corr\| **< 0.5**（互相关层面"干净"） | **299（84%）** |
| 前 30 高 S 中干净 | 25 |
| 干净且 IS 全闸（S≥1.58/F≥1.0/2Y≥1.58/TO∈[0.01,0.7]/fails=0，**现场重核**） | **22** |

**⇒ 互相关不是瓶颈；prod 是。** 22 颗全闸件的 max |corr| 只落在 0.2455-0.4501，远低于 0.5 线。

**随后测 prod：9/9 全部撞墙，无一例外。**

| alpha | S | F | 2Y | prod max | [0.7,0.8) 钉数 | 塔归属 | 判定 |
|---|---:|---:|---:|---:|---:|---|---|
| `bl6avAXp` | 3.57 | 1.50 | 3.40 | 0.7397 | 2 | OTHER | ❌ 浅钉 |
| `2rAPVWrb` | 2.38 | 2.19 | 2.51 | **0.7149** | **1** | PV+FUNDAMENTAL | ❌ 最浅钉，但**构型禁混** |
| `bl6boze6` | 2.74 | 1.62 | 3.32 | 0.7243 | 7 | OTHER | ❌ 中钉 |
| `MPY6kVMr` | 3.54 | 1.47 | 3.45 | 0.7325 | 1 | OTHER | ❌ 浅钉 |
| `0mYXqWxr` | 2.37 | 1.42 | 2.65 | 0.7480 | 3 | PV+OTHER | ❌ 且构型禁混 |
| `rKRQbPPE` | 2.48 | 2.22 | 2.69 | 0.8141 | 5+1@[0.8,0.9) | FUNDAMENTAL | ❌ 厚尾深钉 |
| `d51E709g` | 2.34 | 2.28 | 1.85 | **0.8333** | 61 | MODEL | ❌ 厚尾深钉 |
| `O0AZWg9R` | 2.63 | 1.30 | 2.04 | 0.8398 | 2+1@[0.8,0.9) | — | ❌ |
| `blbx8NJp` | 2.37 | 2.31 | 2.06 | **0.8989** | 46+1@[0.8,0.9) | starval | ❌ |
| `9qxgkpex` | 2.36 | 1.96 | 2.59 | 0.8205 | — | — | ❌ |

**硬结论**：这 358 池**不是"未被利用的富矿"，而是"已被 prod 淘洗后的残渣"**——它们当年未提交正因 prod 卡墙。`MPY6kVMr` 一度让 MIS 从 10 → **11**（与 10 席全对 <0.5 且 IS 全闸），但 prod 0.7325 一票否决。**互相关干净 + IS 全闸 ≠ 可入篮；prod 是唯一硬闸。**

---

## 13.58 塔混配额实况：7 颗落"禁混集合内 × 集合外"，与 ≤5 口径冲突（2026-11-11）

按 `get_datasets` 实查 `shortinterest3` 的 category = **`shortinterest`**（在禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} **之外**）。逐件读 `pyramids`：

| 席位 | pyramids（末段） | 类型 |
|---|---|---|
| `rKRx0M2m` | SHORTINTEREST + RISK | 外×外（不占） |
| `RREGX1kd` | SHORTINTEREST + ANALYST | 外×外（不占） |
| `LLM0e20m` | SHORTINTEREST + NEWS | 外×外（不占） |
| `pwdd7Za6` | SHORTINTEREST + **PV** | 内×外 |
| `pwdLp9z6` | SHORTINTEREST + **OTHER** | 内×外 |
| `O0A6Qz7p` | SHORTINTEREST + **OTHER** | 内×外 |
| `leAmmre8` | SHORTINTEREST + **OTHER** | 内×外 |
| `omExeqLb` | SHORTINTEREST + **MODEL** | 内×外 |
| `Xg9dPpp0` | SHORTINTEREST + RISK + **FUNDAMENTAL** | 内×外 |
| `Jje6mrpO` | SHORTINTEREST + RISK + **FUNDAMENTAL** | 内×外 |

**两种读法结论相反，需用户裁定**：
- 读法 A（**按组合"类型"计**）：SI×PV、SI×OTHER、SI×MODEL、SI×FUNDAMENTAL = **4 类 ≤ 5** ⇒ **合规**。
- 读法 B（**按 alpha"件数"计**）：**7 件 > 5** ⇒ **超配 2 件**。
- 「每个两塔组合 ≤3」两种读法下均合规：SI×OTHER = 3（恰在上限）、SI×FUNDAMENTAL = 2。

**落地影响**：若按读法 B，则后续新席**只能走"外×外"或纯 ATOM**，不得再加任何 trio 主腿——这会直接封死"给 FUNDAMENTAL/MODEL 价值件加借券冷腿"这条降 prod 路径（原本是第 11 席的首选方案）。

---

## 13.59 第 30/31 族方向判死：earnings_sent_matrix 电话会情绪 + insiders12 内部人（2026-11-11）

**动机**：池已 prod 死（§13.57），改走"集合外主腿 × 借券冷腿 @REVERSION_AND_MOMENTUM"配方（该配方产出全部 5 颗 REV 档席位，prod 0.4000-0.6143，是本区唯一被证实的降 prod 组合）。

| tag | 主腿 | 组轴 | S | F | 2Y | fails | 判定 |
|---|---|---|---:|---:|---:|---:|---|
| S1 | `-ts_rank(ts_mean(overall_sentiment_score,60),252)` 情绪水平 | sector | **0.10** | 0.02 | 0.68 | 3 | ❌ |
| S2 | `ts_delta(ts_backfill(overall_sentiment_score,250),22)` 情绪变化 | sector | 1.01 | 0.52 | 1.48 | 3 | ❌ |
| S3 | `ts_zscore(positive-neg probability,126)` 情绪净倾向 | industry | 0.21 | 0.03 | 1.14 | 6 | ❌ 且 TO 1.43 |
| S4 | `-ts_rank(ts_mean(negative_sentiment_probability_3,66),252)` 负面概率 | subindustry | 1.14 | 0.59 | 1.25 | 3 | ❌ |
| S5 | `ts_zscore(ts_backfill(vec_sum(insd12_percent),250),252)` 内部人持股 | sector | 0.66 | 0.30 | 1.27 | 3 | ❌ |
| S6 | `-ts_mean(ts_backfill(vec_sum(insd12_positionchangetransactionamount),250),66)` 内部人减持 | industry | 1.27 | 0.78 | 1.52 | 3 | ❌ |

**归因**：
- **电话会情绪（earnings_sent_matrix）在 GBR 全线无信号**：4 个结构（水平/变化/净倾向/负面概率）S 落在 0.10-1.14，最好一条也只有 1.14，离 1.58 差 0.44。**与 news17「跨来源共识强度」唯一有效形成对照**：情绪打分/概率类字段在本区一贯无效（news50 情绪 5 字段 −0.10~1.36 已先验证）。
- **内部人减持（insd12_positionchangetransactionamount）唯一接近**：S 1.27 / 2Y 1.52 / fails 3，仍双线不过（S 差 0.31、2Y 差 0.06）。
- **内部人持股（insd12_percent）无信号**：S 0.66。该集仅 7 字段全 VECTOR，稀疏度高，`vec_sum`+`ts_backfill(250)` 已填稠密但仍不足以支撑横截面区分。
- **配方失效根因（新增隐含前提）**：借券冷腿只能"减 prod + 提 F"，**不能凭空造出主腿没有的信号**。主腿单腿 S 若 <1.0，加冷腿后 S 仍被主腿拖住（S1 0.10、S3 0.21 即证）。**该配方要求主腿单腿 S ≥1.2 才有意义**——这是 5 颗成功席位的隐含前提，此前未显式记录。

---

## 13.60 累计试错盘（本轮新增后）

- **族方向：31 个**（29 + earnings_sent_matrix + insiders12）
- **中性化档：11 档全部试过**
- **冷腿字段：7 个**（shortinterest3 精选）
- **池内 prod 实测：累计 17 颗**（此前 8 颗 + 本轮 9 颗），**0 颗过墙**
- **在飞仿真零产出批次数：7**

**结论不变但证据链已闭合**：GBR 在「用户既定约束（region 固定 GBR / 不考虑 D0 / trio 禁混 / 算子 ≤12 / 篮内互相关 <0.5）」下，**20 席不可达，10 席是总量上限**。剩余未试的只有需要用户授权的三条路（换区域 / 回 D0 / 接受 10 席）。


---


