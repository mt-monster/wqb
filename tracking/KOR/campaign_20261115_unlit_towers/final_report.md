# 交付报告 · KOR 10 颗「全闸 + prod<0.7」REGULAR alpha（2026-11-16 终版）

> **验收口径（用户 2026-11-16 定）**：**prod ≥ 0.7 一律不算合格交付**。
> 「合格」= ① 平台 `checks` 的 **fail 与 warning 全空**（`failed_ra_count=0`）；
> ② `check_correlation(production)` **实测 prod < 0.7**（严格不等式）。
> **提交权归用户**，本报告不含任何提交动作。

---

## 1. 十颗合格清单

> 基底：KOR / TOP600 / D1 / EQUITY / truncation 0.08 / unitHandling VERIFY / nanHandling OFF /
> pasteurization ON / maxTrade OFF / 区间 2014-01-01–2023-12-31 / FASTEXPR。
> **中性化与 decay 见列** —— 本轮实证这两项直接决定 prod（见 §3）。

| # | alpha | 机制族 | 数据集（塔） | 中性化·decay | S | F | TO | 2Y | subU | inv | returns | maxDD | margin | **prod** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | **`wpoJRxW5`** | A · label 概率差 − 分歧度 | OTHER×INSIDERS | SLOW·2 | **2.04** | 1.15 | 31.5% | **2.55** | 1.95 | 1.48 | 10.00% | 5.52% | 6.4bp | **0.5040** |
| 2 | **`A1xOPqGE`** | A · label 概率差 − 分歧度 | OTHER×INSIDERS | SLOW·2 | 1.92 | 1.04 | 31.4% | **2.62** | 1.84 | 1.36 | 9.31% | 5.63% | 5.9bp | **0.5112** |
| 3 | **`O0W5x9mR`** | B · 关系方家数 − 分歧度 | INSIDERS 1/3 | SLOW·2 | 1.75 | 1.46 | 12.3% | **2.63** | 1.59 | 1.70 | 8.71% | 5.75% | 14.2bp | **0.5260** |
| 4 | **`Jj85OR7e`** | B · 关系方家数 − 分歧度 | INSIDERS | SLOW·2 | 1.81 | **1.53** | 12.3% | **2.66** | 1.65 | 1.76 | 8.98% | 5.80% | 14.6bp | **0.5272** |
| 5 | **`MP65Lx5k`** | B · 关系方家数 − 分歧度 | INSIDERS | SLOW·2 | 1.81 | **1.54** | 12.3% | 2.60 | 1.65 | 1.76 | 9.02% | 5.94% | 14.7bp | **0.5285** |
| 6 | **`P05X3j77`** | B · 关系方家数 − 分歧度 | INSIDERS | SLOW·2 | 1.64 | 1.30 | **10.8%** | 2.54 | 1.68 | 1.63 | 7.86% | 5.28% | 14.6bp | **0.5827** |
| 7 | **`KPgwLqX8`** | B · 关系方家数 − 分歧度 | INSIDERS | SLOW·**1** | 1.73 | 1.24 | 18.9% | 2.27 | 1.89 | 1.61 | 9.69% | 5.94% | 10.3bp | **0.6626** |
| 8 | **`qM7mArVj`** | B · 关系方家数 − 分歧度 | INSIDERS | SLOW·2 | 1.74 | 1.28 | 18.0% | 2.26 | 1.91 | 1.62 | 9.76% | 5.92% | 10.8bp | **0.6650** |
| 9 | **`78LpqZYQ`** | C · 分析师惊奇 − 分歧度 | INSIDERS×ANALYST | REV&MOM·4 | **2.12** | **2.09** | **8.6%** | 2.59 | 2.30 | 2.02 | 12.17% | 7.86% | 28.3bp | **0.6970** |
| 10 | **`ZYQ116ln`** | D · 日内价量同向反向 | PV **2/3** | SLOW·2 | 1.86 | 1.10 | 22.1% | 1.80 | 1.55 | 1.72 | 7.68% | 4.89% | 7.0bp | **0.6981** |

**汇总**：prod **0.504–0.698**（全部 <0.7）· S **1.64–2.12**（全部 ≥1.58）· 2Y **1.80–2.66**（全部 ≥1.58）·
F **1.04–2.09**（全部 ≥1.0）· TO **8.6%–31.5%**（全在 [1%,70%] 获胜带）。
**4 个机制族**（A 2 颗 / B 6 颗 / C 1 颗 / D 1 颗）；3 个未点亮塔（INSIDERS 1/3、OTHER 1/3、PV 2/3）。

⚠ **诚实的相关性说明**：B 族的 6 颗是**同一机制的不同窗口组合**（关系方家数窗口 44/66/126 × 分歧度窗口 22/41/44/55），
彼此 PnL 高度相关（预计 >0.9）⇒ **实际可同时提交的独立件约 4 颗**（A/B/C/D 各取 1）。
剩余 6 颗的价值是「同一机制的稳健性证明 + 若某颗被 self-corr 拦下时的替补」。

---

## 2. 十颗的表达式

```text
# A 族（label 概率差 − 内部人交易分歧度）  SLOW / decay 2
# 1 wpoJRxW5
subtract(group_rank(ts_backfill(ts_rank(subtract(probability_label4_5quantile_5day_ohlcv_2,
                                                probability_label0_5quantile_5day_ohlcv_2), 462), 66), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
# 2 A1xOPqGE（换 1_2 档）
subtract(group_rank(ts_backfill(ts_rank(subtract(probability_label1_2quantile_5day_ohlcv,
                                                probability_label0_2quantile_5day_ohlcv), 462), 66), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))

# B 族（关系方家数 − 内部人交易分歧度）  SLOW / decay 2（#7 为 decay 1）
# 3 O0W5x9mR  tnc 126 / vol_af 44
subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 126), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_af), 44), sector))
# 4 Jj85OR7e  tnc 66 / vol_af 44
subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 66), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_af), 44), sector))
# 5 MP65Lx5k  tnc 44 / vol_af 44
subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 44), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_af), 44), sector))
# 6 P05X3j77  tnc 126 / vol_chg 55
subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 126), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
# 7 KPgwLqX8  tnc 66 / vol_chg 22   (SLOW / decay 1)
subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 66), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_chg), 22), sector))
# 8 qM7mArVj  同上（decay 2）
# 9 78LpqZYQ  分析师 FY1 惊奇 − 分歧度   REVERSION_AND_MOMENTUM / decay 4
subtract(group_rank(ts_av_diff(anl10_smartest_pre_fy1_pred_surps_v1, 504), sector),
         group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
# 10 ZYQ116ln  日内「买价×买量」相关反向   SLOW / decay 2
subtract(0.5, group_rank(ts_mean(corr_bid_price_with_bid_size, 22), industry))
```

---

## 3. 方法论：**降 prod 的两级杠杆**（本轮核心产出）

### 3.1 一级 = 价差结构（两条不同信息源的秩相减）

| 结构 | prod |
|---|---:|
| 单一 `−group_rank(ts_mean(vec_stddev(insd5_vol_chg),22),sector)` | 0.8495 |
| 同信号 **− anl10 分析师 FY1 惊奇** | **0.6970** ✅ |
| 同信号 **− label 概率差** | **0.5040** ✅ |
| **关系方家数（`insd5_tnc`） − 同信号** | **0.5260–0.6650** ✅ |

（反例：`同信号 − oth475 出口额` 反而把 S 打到 1.00/−1.05，弱腿拖累 ⇒ **第二腿必须自身有信号**。）

### 3.2 二级 = **中性化换 SLOW + decay 降到 1–2**

同一表达式、只改设置：

| 表达式 | 设置 | prod | S / F / TO |
|---|---|---:|---|
| `tnc − 分歧度` | REVERSION_AND_MOMENTUM · d4 | **0.8391** | 2.03 / 2.09 / 16.5% |
| 同上 | **SLOW · d1** | **0.6626** ✅ | 1.73 / 1.24 / 18.9% |
| 同上 | **SLOW · d2** | **0.6650** ✅ | 1.74 / 1.28 / 18.0% |
| `PV 买价×买量相关` | **SLOW · d2** | **0.6981** ✅ | 1.86 / 1.10 / 22.1% |
| 同上 | REVERSION_AND_MOMENTUM · d8 | 0.7827 | 1.93 / 1.62 / 13.5% |
| `label − 分歧度` | SLOW · d1 | 0.5161 | 2.03 / 0.98（F 差 0.02） |
| 同上 | **SLOW · d2** | **0.5040** ✅ | 2.04 / 1.15 / 31.5% |

⇒ **SLOW + 低 decay 稳定再压 0.15–0.18**，代价 = TO 抬升、F 下降；**只对本身低换手的核成立**。

### 3.3 被证伪的假设（勿重踩）

| 假设 | 结果 |
|---|---|
| `hump` + 300–900 日 `ts_decay_linear` 壳层能降 prod | ❌ 10/10 全灭，S 0.38–1.40（label 核 2.82→0.58）。那个壳层只削弱信号 |
| 换 anl10 其它字段可复制 `78LpqZYQ` | ❌ 10 字段（sales/BPS/EBT/EBIT/DPS/capex/FY2/FQ1）0/10 全闸 |
| insiders5 还有未挖子族 | ❌ 库藏股 / 去重缺口（KOR 物理恒等⇒全空仓）/ 持有人结构 / 所有权变化，20 臂全灭 |
| 同族分歧度相减 | ❌ 互相抵消（S 0.10/0.19） |
| `ghc_tr` 作价差第二腿 | ❌ prod 抬到 0.7227（`npaO2w7l` 全闸但 prod 撞墙） |

---

## 4. 结构选型规则（本轮实证，可直接复用）

| 维度 | 最优 | 依据 |
|---|---|---|
| 中性化 | **SLOW**（价差结构） | S 保持、prod 最低；`industry/subindustry` 版 F 掉到 0.67–0.97 |
| decay | **1–2** | d4 的 prod 高 0.17；d1 的 F 略低，d2 是平衡点 |
| 价差两条腿 | 一条「广度/存量」+ 一条「噪声/分歧度」 | `tnc − disp` / `label − disp` 均成立 |
| 分歧度第二腿字段 | **`vol_af` ≥ `vol_chg` ≫ `ghc_tr`** | `vol_af` 版 prod 0.526–0.529；`ghc_tr` 版 0.7227 |
| label 期限 | **5 日**（20/60 日的 2Y 掉到 1.45–1.54） | 长窗把近两年波动摊平 |
| 分组轴 | **sector** | industry/subindustry 使 TO 升到 33–35%、F 掉 |

---

## 5. 十年覆盖

10 颗回测区间均为 **2014-01-01 – 2023-12-31**；`insiders5`（三档 cov 0.732/0.873/1.000）、
`intraday_pv_feats`（0.993）、`dl_riskfree_returns`（0.909）、`analyst10`（0.731）在 2014 年均有覆盖。
⚠ 临提交前仍须逐颗 `get_alpha_yearly_stats` 核逐年 `longCount`（平台硬闸）。

---

## 6. 字段画像与归档

| 数据集 | 路径 |
|---|---|
| `insiders5`（53/53 字段 + 四族判死） | `tracking/KOR/reference/datasets/insiders5.md`（§9 为本轮补测） |
| `institutions6` / `fund_holdings_panel`（判死） | 同目录 + `campaign_20261107_institutions_atom/` |
| `anl10`（640 字段、每字段 aC 0–13） | 本轮只验 10 个字段；有效者仅 `pre_fy1_pred_surps_v1` |

命名规则：`tracking/KOR/reference/datasets/<平台 dataset_id>.md`，每集一份、手工维护；
扫全字段必须 `filter_sharpe=false`（否则成对字段的对侧腿被隐藏）。
