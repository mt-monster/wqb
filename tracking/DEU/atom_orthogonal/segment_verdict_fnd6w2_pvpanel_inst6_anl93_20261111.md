# DEU ATOM 战役 · 段判死台账（FUNDAMENTAL6 Wave2 / PV 面板 / institutions6 / analyst93）

> 建立时间：2026-11-11
> 区域锁定：DEU / TOP500 / D1（全程不换 region）
> 本段目标：判定 2 个数据集死刑、开 2 个新数据集矿脉
> 硬栅：S ≥ 1.58 · F ≥ 1.0 · 2Y ≥ 1.58 · 0.01 ≤ TO ≤ 0.7 · sub_u ≥ 0.474×S · RA fail = 0 · self < 0.7 · prod < 0.7
> 算子上限 12（越少越好）· 禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL}

---

## 一、FUNDAMENTAL6 Wave 2 收割 —— 数据集判死

批次 `QqFcgcDE4zxctXcoDZxd9m`，10/10 COMPLETE，设置 DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08。

### 1.1 全表

| # | 机制 | alpha | S | F | 2Y | sub_u | TO | margin | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F6W2-2 | FCF/总资产 | **78Llg8gx** | **1.13** | **0.97** | 0.17 | **0.87** | 0.0298 | **0.006134** | REVIEW |
| F6W2-1 | 经营现金流/总资产（CF-ROA） | **Xg9MXgX5** | **1.11** | **0.94** | 0.05 | **0.80** | 0.0314 | 0.005694 | REVIEW |
| F6W2-7 | 经营现金流/总负债 | **A1VEq1Jw** | **1.02** | **0.84** | −0.05 | 0.63 | 0.0308 | 0.005494 | REVIEW |
| F6W2-8 | 外部融资依赖反向 | LLM3OLb2 | 0.90 | 0.65 | **1.34** | 0.57 | 0.0282 | 0.004703 | REJECT |
| F6W2-10 | 现金质量 × 投资纪律 | MPYV9Pq8 | 0.89 | 0.67 | **1.42** | 0.57 | 0.0384 | 0.003675 | REJECT |
| F6W2-9 | 净利率（含少数股东） | 88RXg87o | 0.87 | 0.61 | 0.66 | 0.62 | 0.0213 | 0.005788 | REJECT |
| F6W2-5 | 现金利润率 4 年时序分位 | JjerRj0j | 0.80 | 0.56 | −0.33 | 0.50 | 0.0368 | 0.003359 | REJECT |
| F6W2-3 | 年报口径 CF/销售 | xAr5XAXb | 0.68 | 0.48 | 0.26 | 0.61 | 0.0235 | 0.005261 | REJECT |
| F6W2-4 | CF 利润率同比改善 | 88RXg8gX | 0.55 | 0.35 | −0.28 | 0.14 | 0.0503 | 0.001955 | REJECT |
| F6W2-6 | 规模桶中性化 | kqN9eqkl | 0.34 | 0.20 | −0.68 | −0.06 | 0.0624 | 0.001411 | REJECT（drawdown 0.5081）|

### 1.2 定论：FUNDAMENTAL6 判死

两波合计 20 条，跨 15 个会计科目、6 类几何（截面 rank / 时序分位 / 同比差分 / 规模桶中性 / 双字段交互 / 门控）：

| 指标 | Wave 1 最好 | Wave 2 最好 | **数据集天花板** |
|---|---:|---:|---:|
| Sharpe | 1.15（现金利润率） | 1.13（FCF/资产） | **1.15** |
| Fitness | 0.98 | 0.97 | **0.98** |
| 2Y Sharpe | **0.43** | 0.17 | **0.43** |
| sub_u | 0.79 | 0.87 | 0.87 |
| margin | 0.006856 | 0.006134 | **0.006856** |

**判死理由**：S 天花板 1.15（差 0.43）、2Y 天花板 0.43（差 1.15）。两者**不可同时逼近**——Wave 2 里 2Y 较强的两条（LLM3OLb2 2Y1.34 / MPYV9Pq8 2Y1.42）S 掉到 0.89–0.90；S 较强的三条 2Y 全在 −0.05~0.17。这是典型的 **S–2Y 权衡前沿**，不是参数问题。

★ **Wave 2 的 3 条 REVIEW 件（78Llg8gx / Xg9MXgX5 / A1VEq1Jw）全部卡同一组闸**：
`failed_ra_count = 3` = LOW_SHARPE + LOW_2Y_SHARPE + LOW_SUB_UNIVERSE（或 FITNESS）。
两条硬伤都在 2Y，不是几何能救的。

★ **可复用结论（跨区通用）**：
> **同一会计科目的不同分母（总资产 / 总收入 / 总负债）不构成结构位移。**
> `divide(oancfy, cptnewq_atq)` S 1.15 / `divide(oancfy, revty)` S 1.15（Wave1）/
> `divide(subtract(oancfy,capxy), cptnewq_atq)` S 1.13 / `divide(oancfy, cptnewq_ltq)` S 1.02
> —— 四条互相关预期 >0.9，实际就是**一颗 alpha 的四个写法**。
> 判「这个数据集有几个信号维度」时，**换分母不算换维度，换分子（科目）才算**。
> 但本数据集换分子全部失败（毛利 0.59 / 应计 0.49 / NOA 0.34 / 研发 0.03 / 杠杆 0.03 / capex −0.39）
> ⇒ **fundamental6 只有「经营现金流」一个有效分子**，容量 = 1 颗，且这颗达不到 1.58/1.58。

---

## 二、PV 面板（analyst_earnings_ibes）Wave 1 收割 —— 数据集判死

批次 `36nVszarj5bA9yXISfuqNor`，10/10 COMPLETE，设置同基线。

### 2.1 全表

| # | 经典异象 | alpha | S | F | 2Y | sub_u | TO | margin | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| PV-7 | 52 周高点接近度 `ts_rank(close,252)` | **88RXAMRv** | **0.79** | 0.44 | 0.61 | 0.42 | 0.1031 | 0.000739 | REJECT |
| PV-3 | 12-1 动量 `ret250 − ret20` | j2YOLqeO | 0.68 | 0.44 | 0.44 | 0.57 | 0.0711 | 0.001468 | REJECT |
| PV-9 | 净股票发行反向（252 日） | pwd309aq | 0.50 | 0.21 | 0.20 | 0.31 | 0.0398 | 0.001160 | REJECT |
| PV-8 | VWAP-收盘偏离反向 | 0mY5o1Y6 | 0.20 | 0.03 | **1.45** | 0.20 | **0.3968** | 0.000049 | REJECT |
| PV-5 | Amihud 非流动性 | omEZ2xEv | 0.19 | 0.06 | −0.90 | −0.01 | 0.0965 | 0.000280 | REJECT |
| PV-1 | 短期反转 `−ret20` | QPvg1qrK | 0.05 | 0.01 | −0.61 | −0.06 | 0.1958 | 0.000039 | REJECT |
| PV-2 | 低波动 `−ts_std_dev(ret1d,66)` | 58EYRPjk | −0.06 | −0.01 | 0.67 | −0.10 | 0.0514 | −0.000185 | REJECT（drawdown 0.4759）|
| PV-6 | 异常成交量反向 | O0AgelAp | −0.09 | −0.02 | −0.44 | −0.21 | 0.0702 | −0.000122 | REJECT |
| PV-4 | 隔夜收益溢价 | vR1P0W1w | −0.12 | −0.03 | **−2.01** | 0.33 | 0.0950 | −0.000122 | REJECT |
| PV-10 | 日内振幅反向 | qMLVbQ7Z | −0.40 | −0.17 | −0.43 | −0.00 | 0.0610 | −0.000724 | REJECT |

**天花板 S = 0.79**、F = 0.44、10/10 REJECT（连 REVIEW 都没有）。

### 2.2 ★★★ 重大修正：覆盖率 × 欠挖度 都不预测信号强度

这是本战役**最重要的方法论修正之一**。

先前的假设（已写入上段台账第七节）：
> 「cov 0.9978 + 42 字段 + 每字段 alphaCount 仅 1–96（严重欠挖）⇒ DEU 目前最未被开采的富矿。」

**实测推翻**：

| 维度 | 实测值 | 结论 |
|---|---|---|
| 覆盖率 | **0.9978**（全 DEU 最高之一） | 只保证无空窗，不保证有信号 |
| 字段数 | 42 / 全套价量面板 | 无分析师字段，纯 OHLCV + 预计算多视界收益 |
| 拥挤度 | alphaCount 每字段 **1–96** | 全 DEU 最欠挖 |
| **信号强度** | **S 上限 0.79 / 10 条全灭** | **零信号** |

**机理**：DEU TOP500 D1 上，**教科书级价量异象集体失效**——
短期反转 0.05、低波动 −0.06、动量 0.68、隔夜 −0.12、Amihud 0.19、
异常量 −0.09、52 周高 0.79、VWAP 0.20、净发行 0.50、振幅 −0.40。

⇒ **「欠挖」只说明没人试过，不说明能出活。**
选数据集时覆盖率只能作**下限筛（防空窗）**，alphaCount 低只能作**相关性风险提示**，两者都**不能作为信号质量先验**。
真正的先验只有两个：① 该 category 在本区是否已有出货记录；② 该 data 的**信息类型**是否与本区定价结构匹配。

★ **DEU 的定价结构已确认为「基本面 / 分析师预期驱动，量价无效」**：
- 出货的 5 颗全部来自 MODEL（分析师预期修正 + predictive_starmine）/
  SHORTINTEREST / SENTIMENT —— **没有一颗来自 PV**。
- 本段 PV 面板 10 条全灭、FUNDAMENTAL6 天花板 1.15，进一步确认：
  **DEU 唯一高 Sharps 矿脉 = 分析师预期类（analyst / model 的 revision & surprise 字段）。**

---

## 三、institutions6 开矿（Wave 1 在飞 `4wxAKefns5bL9OsXaoRGJaH`）

### 3.1 字段画像（11 字段，全 MATRIX，coverage 全部 1.0）

| 维度 | 字段 | 语义 | alphaCount |
|---|---|---|---:|
| 持有水平·机构 | `aggregate_equity_value_institutions` | 机构持有市值 | 24 |
| 持有水平·全体 | `aggregate_equity_value_all_owners` | 全体持有者市值（母子公司去重） | 19 |
| 持有股数·机构 | `aggregate_share_count_institutions` | 机构持有股数 | 20 |
| 持有股数·全体 | `aggregate_share_count_all_owners` | 全体持有股数 | 21 |
| 广度 | `count_institutional_holders_security` | 当前持仓机构数 | 31 |
| 买入广度 | `count_institutional_buyers_security` | 期间买入机构数 | 61 |
| 卖出广度 | `count_institutional_sellers_security` | 期间卖出机构数 | 51 |
| 买入市值流 | `market_value_institutional_shares_acquired` | 机构买入美元额 | **85** |
| 卖出市值流 | `market_value_institutional_shares_disposed` | 机构卖出美元额 | 39 |
| 买入股数流 | `quantity_institutional_shares_acquired` | 机构买入股数 | 66 |
| 卖出股数流 | `quantity_institutional_shares_disposed` | 机构卖出股数 | 39 |

**5 个信息维度**：持有水平（4 字段）/ 覆盖广度（3 字段）/ 金额流（2 字段）/ 股数流（2 字段）/ 结构（全体 vs 机构之差）
**披露节奏**：13F 式季度披露 ⇒ 天然低换手，适合 `ts_mean(_,72)` 剥季度阶梯跳变。

### 3.2 论坛实证（帖 `article_id=43754821327639`，FX25214，70 赞 2 评，GBR 区）

★ **本段最有价值的论坛结论，直接可迁移**：

> **机构买卖股数本身不是 alpha** —— 单独构造
> `group_zscore((qty_acq − qty_disp)/(1 + agg_share_inst), industry)`
> 实测 **S = −0.11 / F = −0.02**。
> 它的正确用法是**「什么时候别做」的条件**，不是可加的收益信号。

> **门控阈值甜点 = `<0.7`（排除最拥挤的 30%）**，不是 `<0.2`。
> 实证：`<0.7` → S 1.30；收窄到 `<0.2` → S 塌到 **0.38**。
> 「trade_when 不是越严格越好，条件太苛刻以后有效信号也一起被挡在门外。」

> **门控方向必须验伪**：反过来只保留净买入压力最高 30% → S 只有 0.57（原向 1.63）⇒ 方向成立。

> **核心信号与条件信号必须用同一种经济口径**：核心用「所有持有人总权益」归一化 + 门控用「机构买卖股数」
> ⇒ S 1.30 但 F 0.88 不过线；把核心信号归一化收回「机构持股总量」+ 分组改 `market` ⇒ **S 1.63 / F 1.26 / 2Y 2.18 / self 0.24 / sub_u 1.21 全过**。

> 冠军骨架（GBR 原版）：
> ```
> trade_when(
>   rank((quantity_institutional_shares_acquired - quantity_institutional_shares_disposed)
>        / (1 + aggregate_share_count_institutions)) < 0.7,
>   group_neutralize(ts_zscore(est_12m_net_mean / aggregate_share_count_institutions, 126), market),
>   -1)
> ```
> ★ 注意：核心信号 `est_12m_net_mean` 属 **predictive_starmine（MODEL）**，
> institutions6 属 **INSTITUTIONS（集合外）** ⇒ 组合合法但需计入「集合内 × 集合外 ≤5」配额。
> **本波不用它**（要严格 ATOM），仅记录为后续可选的双数据集路线。

### 3.3 Wave 1 的 10 条模板（4 口径冠军骨架 + 1 消融 + 1 反向 + 4 异机制）

全部只用 institutions6 单数据集字段 ⇒ **满足严格 ATOM**。

| # | 模板族 | 表达式骨架 | 算子数 |
|---|---|---|---:|
| I1 | 冠军骨架·广度口径 | `trade_when(ts_arg_max(holders,90)<33, signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)),840,driver="gaussian"),1.6), -1)` | 6 |
| I2 | 冠军骨架·深度口径 | 同上，buyers → `quantity_acquired`，holders → `ts_mean(agg_share_inst,72)` | 6 |
| I3 | 冠军骨架·美元口径 | 同上，buyers → `mv_acquired`，分母 → `ts_mean(agg_eq_value_inst,72)` | 6 |
| I4 | 冠军骨架·净流口径 | 分子换 `subtract(buyers, sellers)` | 7 |
| I5 | **消融对照（去门控）** | `signed_power(ts_quantile(divide(buyers, ts_mean(holders,72)),840,driver="gaussian"),1.6)` | 5 |
| I6 | **反向门控** | `ts_arg_max` → `ts_arg_min`（持有广度创新低后） | 6 |
| I7 | 机构化程度趋势 | `group_rank(ts_delta(divide(rank(agg_share_inst), rank(agg_share_all)),252), sector)` | 5 |
| I8 | 机构换手强度反向 | `-group_rank(divide(add(qty_acq, qty_disp), agg_share_inst), sector)` | 3 |
| I9 | 持有广度增长 | `group_rank(ts_delta(count_holders,252), sector)` | 3 |
| I10 | 买卖金额比 | `group_rank(divide(mv_acq, mv_disp), sector)` | 3 |

**设计意图**：
- I1–I4 是同一骨架的**四个信息口径**（广度/深度/美元/净流）——用来定位「哪一层信息有效」。
- **I5 是关键消融**：对比 I1 与 I5 可直接量化「门控贡献多少 S」，这是本波的核心归因实验。
- I6 验伪门控方向（论坛明确要求）。
- I7–I10 是 4 个完全不同的经济机制，避免把「骨架选错」误判成「数据集没信号」。

**预检**：`unknown_fields=["gaussian"]`（已知假阳性，driver 参数值），`platform_field_count=10` 全部真实字段确认 ⇒ 可派发。

---

## 四、analyst93 开矿（Wave 1 在飞 `2X5KNC4qD5bkaGhDkVtGi42`）

### 4.1 数据集定位：**分析师「预测能力」，不是预测值**

`analyst93` cov 0.6328–0.6459，**100 字段全部 VECTOR**（必须 `vec_*` 聚合）。
category = **ANALYST（集合外）** ⇒ 不受 {PV,MODEL,OTHER,FUNDAMENTAL} 禁混约束，单数据集 ATOM 不占配额。

**5 个族 × 2 视角（analyst / estimator 两套命名，语义相同）**：

| 族 | coverage | 核心字段 | 语义 | 最高 alphaCount |
|---|---|---:|---|---:|
| **accuracy** | 0.6328 | `anl93_analyst_accuracy1/2`、`consistency`、`correct_revision_ratio` | 历史预测命中率 / 误差标准差负值 / 修正方向正确率 | **27**（correct_revision_ratio） |
| **correv** | 0.6328 | `correct_revision_times`、`total_revision_times` | 修正次数与正确次数（分子分母） | 27 |
| **profitabilityprev** | 0.6459 | `profitability1`（对比该分析师上次预测）、`profitability2`（**对比预测日收盘价 = 真实超额收益**） | 跟随该分析师预测的历史平均日收益 | **34**（profitability2） |
| **recprofitabilityprev** | 0.6358 | 同上，但基于**推荐（recommendation）**而非预测 | 跟随该分析师推荐的历史平均日收益 | **52**（profitability2）★全集最高 |
| **relative_*** | 同族 | `relative_accuracy1..4`、`relative_consistency1/2`、`relative_ratio1/2`、`relative_profitability1..4` | 同一股票内**分析师之间的相对排名 / min-max 归一化** | 13 |

视界变体：`_20d` / `_60d` / `_120d` / 无后缀（默认窗口）。

★ **本数据集的独特价值**：它度量的是**分析师质量**，而不是预测水平。
现有 5 颗交付件里的 2 颗（QPvzNNGG / LLMzYrZe）用的是 `mean_estimate_change_pct_*`（预测**变动**），
本集用的是「**谁在预测**」——信息源不同 ⇒ 预期互相关低，是 DEU 唯一能把 ATOM 容量往上顶的候选。

### 4.2 Wave 1 的 10 条模板（10 个结构互异族）

| # | 信息维度 | 表达式 | 算子数 |
|---|---|---|---:|
| A1 | 群体平均盈利力（水平） | `group_rank(vec_avg(rec_prof2), sector)` | 2 |
| A2 | **明星分析师**（上端） | `group_rank(vec_max(rec_prof2), sector)` | 2 |
| A3 | **质量分化度**（极差） | `group_rank(subtract(vec_max(rec_prof2), vec_min(rec_prof2)), sector)` | 4 |
| A4 | 盈利力改善（一阶差分 66） | `group_rank(ts_delta(vec_avg(rec_prof2), 66), sector)` | 3 |
| A5 | **低分歧溢价**（二阶矩反向） | `-group_rank(vec_stddev(rec_prof2), sector)` | 2 |
| A6 | 修正方向正确率（命中率） | `group_rank(vec_avg(anl93_analyst_correct_revision_ratio), sector)` | 2 |
| A7 | 预测一致性（误差稳定性） | `group_rank(vec_avg(anl93_analyst_consistency), sector)` | 2 |
| A8 | 覆盖广度 | `group_rank(vec_count(rec_prof2), sector)` | 2 |
| A9 | 盈利力 × 命中率 交互 | `group_rank(multiply(rank(vec_avg(rec_prof2)), rank(vec_avg(accuracy1))), sector)` | 6 |
| A10 | 高覆盖门控 | `trade_when(vec_count(rec_prof2) > 3, group_rank(vec_avg(rec_prof2), sector), -1)` | 4 |

其中 `rec_prof2` = `anl93_recprofitabilityprev_analyst_profitability2`。

**为什么这 10 个结构互异**：
- A1/A2 是**位置统计量**（均值 vs 上端），A3 是**极差**，A5 是**二阶矩** ⇒ 三个不同的矩。
- A4 是**一阶差分**（时序方向），A8 是**计数**（广度），A9 是**乘积几何**（两维交互），A10 是**状态门控**。
- A6/A7 换**信息族**（命中率 / 一致性），不是换窗口。

**预检**：`valid: true`、`unknown_fields: []`、`vector_fields` 100 个全部正确识别 ⇒ 零告警，可派发。

---

## 五、本段累计状态

### 5.1 交付件（5 颗全闸通过，全部 UNSUBMITTED）

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | self | prod | 严格 ATOM |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | SENTIMENT | 2.05 | 1.71 | 2.53 | 0.147 | 0.030 | 0.6935 | ✗ 双集 |
| 2 | E56pROb9 | model216 + predictive_starmine | MODEL | 1.79 | 1.70 | 2.03 | 0.067 | 0.600 | 0.6859 | ✗ 疑违禁混 |
| 3 | QPvzNNGG | predictive_starmine | MODEL | 1.70 | 1.30 | 2.18 | 0.155 | 0.678 | 0.6777 | ✓ |
| 4 | LLMzYrZe | predictive_starmine | MODEL | 1.61 | 1.16 | 1.69 | 0.153 | 0.670 | 0.6697 | ✓ |
| 5 | MPY9VNY9 | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.036 | 0.270 | 0.5986 | ✓ |

**严格单数据集 ATOM = 3 / 10**。

### 5.2 已判死数据集清单（本段新增 2 个）

本段新增：**fundamental6**（S 天花板 1.15）、**analyst_earnings_ibes**（S 天花板 0.79，实为 PV 面板）。

此前已判死：sentiment7、sentiment27、model264、model28、model238、model36、model53、
model106、model216(单用)、news17、news20、news104、news48、analyst44、analyst48、
insider_agg_matrix、institutions1、other699、other532、other455、risk60、dl_riskfree_returns、
shortinterest3(第 2 颗容量锁 1) 等，加 44 个 cov=0 数据集。

### 5.3 剩余未开波的高覆盖数据集

| 数据集 | cov | 字段数 | 备注 |
|---|---:|---:|---|
| **pattern_scores** | 0.9888 | 504 | 最大搜索空间，待评估信息类型 |
| **news18** | 0.8046 | 70 | news 类在 DEU 已多次判死 |
| **news50** | 0.7644 | 37 | 同上 |
| **fund_holdings_panel** | 0.9019 | 18 | ★ 全 VECTOR event + **无方向**（只有活跃度/集中度/持久性）⇒ 严格 ATOM 难成，暂缓 |
| **analyst47** | 0.6234 | 5 | 字段太少 |
| **analyst9** | 0.5825 | 51 | ANALYST 族，仍有潜力 |
| **analyst83** | 0.3389 | — | 覆盖不足 |
| **other250 / other47 / other545** | 0.61/0.58/0.53 | 12/18/4 | other 类，多为 GROUP/分类 |
| **model30** | 0.5694 | 14 | MODEL 族 |
| **insiders1** | 0.5343 | 8 | VECTOR，INSIDERS 族 |
| **fundamental22** | 0.69 | **1** | 单字段，只能做一条 |

---

## 六、可复用结论（写入长期记忆候选）

1. ★★★ **覆盖率 × 欠挖度 都不预测信号强度**。cov 0.9978 + alphaCount 1–96 的 PV 面板，10 条经典异象全灭（S≤0.79）。
   覆盖率只作**下限筛**（防空窗），alphaCount 低只作**相关性风险提示**。
2. ★★★ **DEU 的定价结构 = 分析师预期驱动，量价无效**。出货 5 颗全来自 MODEL/SHORTINTEREST/SENTIMENT，PV 零出货。
   后续选数据集优先级：analyst/model 的分析师预期类 >> sentiment/shortinterest >> fundamental >> PV（最低）。
3. ★★ **同一会计科目的不同分母不构成结构位移**（fundamental6：CF/资产 1.15、CF/收入 1.15、FCF/资产 1.13、CF/负债 1.02 = 一颗 alpha 的四个写法）。
   判「有几颗」要**换分子（科目）**；本数据集换分子全部失败 ⇒ 容量 1 颗。
4. ★★ **机构买卖股数本身不是 alpha（S −0.11），它是「什么时候别做」的门控**。门控阈值甜点 `<0.7`，`<0.2` 会把信号压死（S 1.30 → 0.38）。
5. ★★ **门控方向必须验伪**（反向 S 0.57 vs 原向 1.63）。
6. ★ 分析师「**质量**」（命中率/跟随收益）与分析师「**预测值**」是两个正交信息源，前者未在 DEU 测过。

---

## 附录 A：`deu_ds_cov.csv` 字段说明

列：`id`（数据集 ID）/ `cat`（category）/ `cov`（coverage）/ `fc`（fieldCount）/ `ac`（alphaCount）/ `uc`（userCount）。
仅收录 cov > 0 的 68 个数据集。用途：**选集主依据**，不再依赖记忆里的「已判死清单」。

## 附录 B：本段派发记录

| 批次 ID | 数据集 | 条数 | 设置 | 状态 |
|---|---|---:|---|---|
| `QqFcgcDE4zxctXcoDZxd9m` | fundamental6 | 10 | SUBIND/decay4/trunc0.08 | COMPLETE，S≤1.13 |
| `36nVszarj5bA9yXISfuqNor` | analyst_earnings_ibes | 10 | SUBIND/decay4/trunc0.08 | COMPLETE，S≤0.79 |
| `4wxAKefns5bL9OsXaoRGJaH` | institutions6 | 10 | SUBIND/decay4/trunc0.08 | 在飞 |
| `2X5KNC4qD5bkaGhDkVtGi42` | analyst93 | 10 | SUBIND/decay4/trunc0.08 | 在飞 |
