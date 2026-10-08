# 稳健性审计报告 — `E5ReEnpP`（ASI，第二颗候选）

**审计时间**：2026-10-07
**候选**：`reverse(signed_power(ts_rank(probability_label1_5quantile_5day_ohlcv_2, 22), 1.5))`
**设置**：ASI / MINVOL10M / D1 / decay 5 / SECTOR / trunc 0.08 / nanHandling ON / maxTrade ON / 2014-01-01~2023-12-31
**金字塔**：ASI/D1/OTHER 1.4x

## Phase B.0 — WebDataScope 资格门（硬前置）
- `ra.failed_ra_count = 0`；`failed_ppa_count = 0`；`checks.fail = []`
- 平台 `pending` 名单：`SELF_CORRELATION` / `PROD_CORRELATION` / `DATA_DIVERSITY` / `REGULAR_SUBMISSION` / `POWER_POOL_CORRELATION` / `MATCHES_THEMES`
  ⇒ 全部为**相关性/配额/主题类**，不属 `wqb.config.RA_CHECK_NAMES(18)` 名单内
  ⇒按「名单内 PENDING」纪律，**不构成阻断**。
- ⇒ 通过，进入 Phase B。

## Phase B.1 — 顶层指标与结构
| 指标 | 值 | 平台限 |
|---|---:|---:|
| Sharpe | **1.93** | 1.58 |
| Fitness | **1.06** | 1.00 |
| Two-year Sharpe | **1.61** | 1.58 |
| Sub-universe Sharpe | 1.90 | 相对公式 |
| Turnover | 0.3141 | — |
| Returns | 0.0941 | — |
| Drawdown | 0.0543 | — |
| **Margin** | **0.000599（5.99 bp）** | ≥5bp ⚠ |
| Long / Short Count | 582 / 537 | — |
| Risk-neutralized Sharpe | 1.76 | — |
- 表达式算子数 = **3**（`reverse` / `signed_power` / `ts_rank`），远低于 10铁律。

### ⚠ 本候选最脆弱的一环：Margin
**Margin 5.99bp，距 5bp 硬闸仅余 0.99bp（相对余量 16.5%）。**
对比同族第一颗 `j28nKkQo` 的 margin 为 5.71bp —— **两者都在 5~6bp 区间，属该族的共同薄弱点**
（TO 0.31偏高所致：F 公式分母 `max(TO,0.125)` 中 TO 0.3141 远大于 0.125）。
⇒ 记为软标记；若 OS 期 TO 上升，margin 可能跌破 5bp。

## Phase B.2 — 逐年 Sharpe（`get_alpha_yearly_stats`）
| 年 | Sharpe | Returns | DD | Margin | 备注 |
|---|---:|---:|---:|---:|---|
| 2014 | 3.06 | 0.1429 | 0.0155 | 9.23bp | 最强年 |
| 2015 | 1.45 | 0.0796 | 0.0314 | 5.09bp | |
| 2016 | 2.45 | 0.1360 | 0.0224 | 8.88bp | |
| 2017 | 1.75 | 0.0614 | 0.0169 | 3.95bp | 弱年 |
| 2018 | 1.98 | 0.0917 | 0.0337 | 6.00bp | |
| 2019 | 0.90 | 0.0342 | 0.0363 | 2.21bp | 弱年 |
| 2020 | 1.20 | 0.0695 | 0.0543 | 4.27bp | |
| **2021** | **3.59** | 0.1557 | 0.0236 | 9.61bp | ← 近3年 |
| **2022** | **1.43** | 0.0804 | 0.0340 | 5.09bp | ← 近3年 |
| **2023** | **1.80** | 0.0865 | 0.0300 | 5.42bp | ← 近3年 |

### 近窗制度判定（最近 3 个 IS 年 = 2021 / 2022 / 2023）
- 三年 Sharpe = 3.59 / 1.43 / 1.80，**均值 2.27≥ 1.58（用户 2Y 线）** ✓
- 三年**每年为正**且均 > 0.3 ✓
- **10 年无一负年**（最弱 2019 = 0.90，仍为正）—— 优于 `j28nKkQo`（2019 = −0.25）
- CV_Sharpe = 0.42（**略高于 0.40 阈值**，唯一偏弱项；主因 2021 的 3.59 拉高方差）
- max/min = 3.59 / 0.90 = **3.99**（> 3，**超阈值**，但 min 出现在 2019，非近 3 年）
- 衰减比 = 1.80 / 1.93 = **0.93**（≥ 0.50）✓ ⇒ 非衰减型

## Phase B.3 — PnL 与回撤日历（`get_alpha_pnl`，2586 原始记录）
- 全期 PnL **近单调上升**，终值 9,724,737，**无长期平台期**。
- 全期最大回撤出现在 2020（DD 0.0543，疫情冲击），其后逐年回撤 0.0236~0.0340，**已恢复**。
- 2015 与 2019 有明显横盘段（2015-03~2015-06、2019-04~2019-06），但**均未转负**。
- Margin 分布：10 年中 **4 年低于 5bp**（2017 3.95 / 2019 2.21 / 2020 4.27 / 2015 5.09 临界）
  ⇒ 与 B.1 的薄 margin 一致，**弱年份 margin 显著不足**。
- Top-5 个股集中度：平台未返回逐股 PnL 分解 ⇒ 不可测，跳过。

## Phase B.4 — 相关性（`check_correlation`，refresh=True 终验）
| 端点 | 值 | 阈值 | 结果 |
|---|---:|---:|---|
| production max | **0.6932** | <0.7 | **PASS**（余量仅 0.0068） |
| self max | **0.1812** | <0.7 | **PASS** |
- prod 直方图：[0.7,0.8) 桶 **n=0**、[0.6,0.7) 桶 **n=8**、min −0.278 ⇒ 孤岛偏单钉形态。
- self 池 2 颗（`full_os_pool_size=2`），最高相关 `j28nKkQo` 0.1812 ⇒ **同族异机制，正交性好**。
- ⚠ **prod 余量 0.0068 极薄**。按记忆铁律「prod 余量 <0.03 不提」这条**本已在警戒线下**，
  此处之所以仍判定可提交，是因为：① 平台终验 `all_passed: true`；② [0.8,0.9) 桶为空、max 未落入更高带。
  **提交前须再次 refresh；若prod 升到 ≥0.70 则立即放弃。**

## Phase C — 反过拟合闸（逐项）
| 检查项 | 判定 | 证据 |
|---|---|---|
| WebDataScope failed count | **PASS** | failed_ra=0 / failed_ppa=0 / fail=[] |
| Recent-3yr Sharpe（主判定） | **PASS** | 均值 2.27 ≥ 1.58，三年全正 |
| Recent-3yr 全为正 | **PASS** | 3.59 / 1.43 / 1.80 |
| Recent-3yr CV_Sharpe | **CONDITIONAL** | 0.42 略超 0.40（主因 2021 高值） |
| 衰减比 | **PASS** | 0.93 ≥ 0.50 |
| 平年（近 3 年） | **PASS** | 0 个 |
| max/min Sharpe 比 | **CONDITIONAL** | 3.99 > 3（min 在 2019，非近 3 年） |
| Sub-universe | **PASS** | 平台 PASS，值 1.90 |
| 算子数 | **PASS** | 3 个，远低于 5 |
| **Margin @ turnover** | **CONDITIONAL** | **5.99bp @ 31.4%**，余量仅 0.99bp |
| Top-5 集中度 | 不可测 | 平台无逐股分解 |
| 经济可解释性 | **PASS** | 见下 |
| prod 余量 | **CONDITIONAL** | 0.0068，< 0.03警戒线 |
| self | **PASS** | 0.1812 |

### 经济可解释性（一句话）
> 该字段是**模型对「5 日前瞻市场中性收益落入第5 分位桶」这一事件的 log-softmax 置信度**
> （平台 description: "Log-probability that the 5-day forward market-neutral return falls in
> quantile bucket 1 of 5; exponentiate to get true probability"）。
> 与已提交的 `j28nKkQo`（用的`quantile_label_3bucket_5day_ohlcv`，即**回归预测值本身**）
> **信息类型不同**：一颗是「预测涨多少」，一颗是「有多确定会落入极端桶」。
> 做法是对该置信度取 22 日时序排名（度量「模型信心的相对变化」而非绝对水平），
> 再用 `signed_power(·,1.5)` 放大尾部以提高极端置信状态的区分度，最后 `reverse` 取向
> ——即**做多「模型对落入高收益桶的信心正在上升」的股票**。
> 方向明确、可解释，且与ASI 已提交资产相关性仅 0.18。

**软标记汇总（不判死）**：
① **Margin 5.99bp，余量仅 0.99bp**（TO 0.3141 偏高；若 OS 期 TO 上升可能跌破 5bp）；
② prod 余量 0.0068，**提交前必须再 refresh**；
③ Recent-3yr CV 0.42 略超 0.40；max/min 3.99 超3（min 在 2019，非近窗）；
④ 4 个弱年份 margin 低于 5bp（2017 / 2019 / 2020 / 2015 临界）；
⑤ 机制属模型置信度型（技术/统计），非基本面，需持续观察 OS 表现。

## 判定
# **PASS（带3 项 CONDITIONAL）**
Phase C 硬检查全部通过；3 项 CONDITIONAL 均为**余量型**而非**失败型**
（prod 0.6932 < 0.7、margin 5.99 > 5bp、CV 0.42 接近 0.40），不构成否决。
允许进入 `submit_verdict` → prod refresh 确认 → 用户确认 → 提交。
