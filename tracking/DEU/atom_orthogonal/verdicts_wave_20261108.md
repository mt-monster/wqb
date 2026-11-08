# DEU ATOM 挖掘 · 2026-11-08 波次判定台账

> 基线设置（除特别注明）：`DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / pasteurization ON / unitHandling VERIFY / maxTrade OFF`
> 硬闸：`S ≥ 1.58`、`F ≥ 1.0`、`2Y ≥ 1.58`、`0.01 ≤ TO ≤ 0.7`、`sub_universe ≥ 0.474×S`、`RA 失败 = 0`、`self < 0.7`、`prod < 0.7`
> 本文只记录**本轮新增**的判死与发现；已交付 5 颗见 `final_delivery_20261107.md`。

---

## 一、判死数据集（本轮）

### 1.1 `analyst93` —— 判死（ANALYST 塔）

批次 `3oK5rp3XH4De9Nx158zPDRar`，8 条，全部 `SUBINDUSTRY / decay 4 / trunc 0.08`。
preflight `valid=true / unknown_soft=[] / platform_field_count=7`。

| alpha | 核心表达式 | S | F | 2Y | TO | RA |
|---|---|---:|---:|---:|---:|---:|
| **58Eemqmk** | `group_rank(ts_backfill(vec_avg(anl93_profitabilityprev_estimator_profitability2),66),sector)` | **1.03** | **0.85** | 0.44 | 0.0742 | 3 |
| qML3ama2 | `group_rank(ts_delta(ts_backfill(vec_avg(...profitability2),66),22),sector)` | 0.08 | 0.01 | 0.52 | 0.1819 | 3 |
| xArWLmZg | `-group_rank(ts_std_dev(ts_backfill(vec_avg(anl93_analyst_accuracy1),66),66),sector)` | 0.21 | 0.07 | 0.40 | 0.0546 | 3 |
| 88RY0Kwa | `group_rank(ts_backfill(vec_avg(anl93_estimator_correct_revision_ratio),66),sector)` | 0.48 | 0.25 | −0.04 | 0.0491 | 3 |
| YP1JVWeM | `group_rank(ts_backfill(vec_avg(anl93_estimator_consistency),66),sector)`（零拥挤） | −0.31 | −0.14 | 0.50 | 0.0320 | 4 |
| Xg9e3Y0a | `group_rank(ts_sum(ts_backfill(vec_avg(anl93_estimator_total_forecast_times1),66),252),sector)` | −0.26 | −0.10 | −0.11 | 0.0185 | 3 |
| zq30xJVV | `group_rank(divide(ts_backfill(vec_avg(anl93_estimator_accuracy1),66),add(ts_backfill(vec_avg(anl93_estimator_total_forecast_times1),66),1)),sector)` | 0.16 | 0.05 | −0.66 | 0.0356 | 4 |
| RREKOkGn | `group_rank(ts_ir(ts_backfill(vec_avg(anl93_profitabilityprev_estimator_profitability1_120d),66),252),sector)` | 0.52 | 0.28 | 0.04 | 0.0257 | 3 |

**判定**：prescreen 8/8 REJECT。最强 `58Eemqmk` S 1.03 / **F 0.85（异常高）**但 2Y 仅 0.44，离 1.58 差 1.14。
**归因**：F 0.85 @ S 1.03 说明单笔收益质量不差，问题在**时序稳定性**——分段看 2Y 塌陷 ⇒ 信号集中在早年。
**结论**：不重试。`analyst93`（100 个 VECTOR，cov 0.63，大量 ac=0 零拥挤字段）在 DEU 无足够横截面预测力。
**可复用教训**：**零 alphaCount ≠ 有信号**。`anl93_estimator_consistency`（ac=0）跑出 S −0.31，`anl93_estimator_accuracy1` 派出 S 0.16–0.21。
低拥挤只是「没人挖过」，不是「挖了就有」。

### 1.2 `insider_matrix` —— 判死（INSIDERS 塔）

批次 `M1cF2Pm58RcuXxiqgObit`，8 条，**4 条 COMPLETE + 4 条单位不兼容 WARNING**。

| alpha | 核心表达式 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| **RREKObYg** | `group_rank(ts_sum(subtract(eur_top_signal_value_2, eur_top_signal_value_4),66),sector)` | **0.64** | 0.38 | −0.00 | 0.0652 |
| leA9nv2x | `group_rank(ts_sum(subtract(eur_signal_value_2, eur_signal_value_4),66),sector)` | 0.55 | 0.30 | 0.15 | 0.0676 |
| pwdZ2Rzj | `group_rank(ts_delta(subtract(eur_signal_value_2, eur_signal_value_4),22),sector)` | 0.15 | 0.04 | 0.39 | 0.0512 |
| ZYQM8bW3 | `group_rank(ts_zscore(subtract(eur_signal_value_2, eur_signal_value_4),252),sector)` | −0.55 | −0.22 | −0.92 | **1.0373** |

**★★ 新工具坑：`add(<CSPrice 单位字段>, 常数)` 触发 UNITS WARNING**

以下 4 条全部 `WARNING`（非 CANCELLED，alpha 仍创建但无指标）：
`omErbLv6` / `6XdJWjqP` / `zq30x8oG` / `O0AVLN51`

```
Incompatible unit for input of "add" at index 1, expected "Unit[CSPrice:1]", found "Unit[]"
```

即 `add(eur_signal_value_2, 1)`、`divide(eur_signal_value_2, add(eur_signal_value_1, 1))` 这类
**「美元量纲字段 + 无量纲 epsilon」**写法在 `unitHandling=VERIFY` 下非法。
**正确写法**：先 `rank()` 抹掉量纲再加减常数，或分子分母同为同量纲字段直接相除（不加 epsilon）。
preflight **不校验单位**，只在仿真阶段报 ⇒ 首波必须控制批大小以免整批浪费。

**判定**：最强 S 0.64，prescreen 4/4 REJECT。
**归因**：`ts_zscore(…,252)` 在稀疏矩阵字段上 TO 飙到 1.04、drawdown 2.04 ⇒ 披露事件型稀疏字段做时序标准化会放大跳变，
必须先 `ts_backfill`。这是本波 1 条方法论失误。
**结论**：insiders 塔在 DEU 已有 3 个数据集证据（`insider_agg_matrix` 0.89 / `insider_matrix` 0.64 / `institutions1` 0.71），
塔级判死成立，剩 `insiders1`（8 个 VECTOR，cov 0.5343）未测，作为最后验证。

### 1.3 `predictive_starmine` 的 actuals 族 —— 判死（已实现财务比路线）

批次 `3klnWxaEl52GciFe1k9oI3p`，8 条（净利率 / EBITDA 利润率 / 利润率加速 / 盈利稳定性 / 规模 / 非现金成本占比）。

| alpha | 机制 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| LLMrv209 | 利润率加速（季度 − 年度） | **0.46** | 0.20 | −0.06 | 0.0532 |
| 2rAWg238 | 净利率同比趋势 | 0.38 | 0.15 | 0.68 | 0.0474 |
| N1N3d2Z8 | 净利率水平 | 0.24 | 0.08 | −0.77 | 0.0263 |
| WjO0ZxvX | 规模（小盘溢价，取负） | 0.17 | 0.04 | **1.62** | 0.0175 |
| QPvgxowQ | 季度净利率 | 0.16 | 0.04 | −0.74 | 0.0432 |
| rKRVqnZ9 | 盈利稳定性（取负） | 0.12 | 0.03 | 0.00 | 0.0153 |
| N1N3dGXw | 非现金成本占比（取负） | 0.05 | 0.01 | 0.15 | 0.0261 |
| vR16EoWa | EBITDA 利润率 | −0.04 | −0.00 | −0.27 | 0.0234 |

**判定**：8/8 REJECT，最强 0.46。

**★★★ 关键结构推论（最重要的方法论收获）**

`predictive_starmine` 已贡献 2 颗严格 ATOM（`QPvzNNGG` S 1.70、`LLMzYrZe` S 1.61），
但同一个数据集的 **actuals（已实现财报）族全部无效（S ≤ 0.46）**，而 **预期修正 / 超预期族（estimate change / predicted surprise）强**。

⇒ **一个数据集的「信号面」可以与其「字段面」严重不对称**：631 个字段里真正有 alpha 的只集中在
`mean_estimate_change_pct_*` / `predicted_surprise_*` 两个族。不要因为「数据集出货了」就假设同集其余族也能出货。

### 1.4 `risk60` —— 未达线，但机制被证实（保留为改进基础，RISK 塔）

批次 `HGPS1e0R4RL8Y2hQKTOkAj`，8 条，全部 COMPLETE。字段：5 个 VECTOR（cov 0.835）。

| alpha | 模板（8 个结构互异） | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| **bl6nwkeZ** | 借券费 z-score 252（相对紧度） | **0.81** | 0.51 | 0.97 | 0.1363 |
| **QPvg8J8G** | 借券费水平（ts_mean 22） | **0.77** | 0.53 | **1.07** | 0.0385 |
| N1N3ZmXo | 期限结构（短窗 − 长窗） | 0.68 | 0.39 | 0.73 | 0.0547 |
| zq30V6vR | 费率上升天数占比（持续性） | 0.55 | 0.31 | 0.91 | 0.0466 |
| vR16QqWz | 做空拥挤度水平 | 0.47 | 0.20 | 0.23 | 0.1576 |
| 88RYwoMW | 日内报价离散度（vec_range/vec_avg） | 0.41 | 0.27 | 0.53 | 0.0553 |
| Jje19w92 | 费率 22 日动量 | 0.38 | 0.12 | 0.08 | 0.2664 |
| E56Ld79R | 借入/贷出费率比 | −0.73 | −0.46 | −1.05 | 0.1138 |

**★★★ 机制被证实的证据（不是噪声）**

8 个模板里 **6 个同向为正**（费率水平 0.77 / zscore 0.81 / 期限结构 0.68 / 持续性 0.55 / 拥挤度 0.47 / 离散度 0.41），
方向全部是「**借券费越高 → 未来越跑输**」，与证券借贷文献（D'Avolio 2002；Drexl er & Drechsler 2016）一致。
且 `QPvg8J8G` 的 **2Y = 1.07** 是全场最好的近两年稳定性 ⇒ 该机制在 DEU **确实存在**，只是水平不足。

**归因（为什么水平只到 0.8）**
- 反向那条（`E56Ld79R` 借入/贷出费率比）S −0.73 ⇒ 该比值本身是**反向指标**，我符号写反了，不是信号缺失。
- 失败的共同点：都是**「费率水平类」的横截面排序**。而我在 DEU 唯一成功的做空件 `MPY9VNY9`（S 1.59）
  用的是 **`ts_delta` 长周期变化 + 双视界相乘**（240 日 × 176 日），**不是水平**。
- ⇒ **改进方向不是换窗口，而是「水平 → 长周期变化」的几何换轨**。见第六节 RISK60-B 设计。

---

## 二、`risk60` 字段画像（RISK 塔，DEU / TOP500 / D1）

数据集级：`coverage 0.835 / fieldCount 5 / userCount 210 / alphaCount 418 / valueScore 2.0 / pyramidMultiplier 1.5`

| 字段 | 类型 | cov | userCount | ac | 语义 |
|---|---|---:|---:|---:|---|
| `rsk60_offer` | VECTOR **event** | 0.835 | 127 | 196 | 空头方支付的综合借券费（年化） |
| `lending_fee_bid_rate` | VECTOR **event** | 0.835 | 103 | 145 | 多头出借方可接受的费率 |
| `rsk60_last` | VECTOR **event** | 0.835 | 88 | 128 | 快照时点最近一次观察到的费率 |
| `rsk60_crowding` | VECTOR **event** | 0.835 | 38 | 53 | 做空活动带符号日指标（正 = 加空/拥挤，负 = 回补） |
| `rsk60_datatime` | VECTOR **event** | 0.835 | 9 | 11 | 供应商快照时间戳 HHMMSS（排序用，非信号） |

**⚠ event 类型铁律**：全部 5 个字段是 VECTOR **event** 类型，**必须先 `vec_*` 聚合再接 `ts_*`**，
否则整批报 `Operator ts_mean does not support event inputs`。
本波用 `vec_avg` / `vec_range`，全部通过。

**可用 vec_ 算子（平台已确认）**：`vec_avg` / `vec_sum` / `vec_count` / `vec_max` / `vec_min` / `vec_stddev` / `vec_range`

---

## 三、本轮扫描的数据集结论（dataset 级 coverage 速判）

| 数据集 | category | dataset cov | 字段数 | 结论 |
|---|---|---:|---:|---|
| `institutions6` | institutions | **1.0** | 11 MATRIX | **最优候选**，已派 INST6-A |
| `risk60` | risk | **0.835** | 5 VECTOR | 机制成立、水平不足，已派 RISK60-A |
| `risk88` | risk | 1.0 | 1 MATRIX | 只有 `alternative_market_cap_usd`（weighting 用途），不可作信号 |
| `earnings6` | earnings | 0.0 | 18 | cov 0 ⇒ 判死（DEU 无数据） |
| `earnings_sent_matrix` | earnings | 0.0 | 7 | cov 0 ⇒ 判死 |
| `risk68` | risk | 0.0 | 5 | cov 0 ⇒ 判死 |
| `risk71` | risk | 0.0 | 10 | cov 0 ⇒ 判死 |
| `risk72` | risk | 0.0 | 31 | cov 0 ⇒ 判死（前已证） |
| `institutions25` | institutions | 0.0 | 24 | cov 0 ⇒ 判死 |
| `institutions4` | institutions | 0.3413 | 6 | 低覆盖，暂缓 |
| `fund_holdings_panel` | institutions | 0.9019 | 18 | 前波已测，最强 0.57 |
| `institutions1` | institutions | 0.2289 | 7 | 前波已测，最强 0.71 |

**★★★ 选集铁律再次确认**：`dataset 级 coverage` 是 DEU 的第一道硬筛。
`event_ml_signals` / `risk72` / `socialmedia12` / `earnings6` / `earnings_sent_matrix` / `risk68` / `risk71` / `institutions25`
共 8 个数据集全部 **cov = 0**；DEU 的「低 alphaCount」大多是「没数据」的代理，**不能当低拥挤度信号用**。

---

## 四、`institutions6` 字段画像（INSTITUTIONS 塔，DEU / TOP500 / D1）

数据集级：`coverage 1.0 / fieldCount 11 / userCount 135 / alphaCount 282 / valueScore 3.0 / pyramidMultiplier 1.6`
**全部 11 个字段均为 MATRIX，coverage 均为 1.0** ⇒ 无需 `vec_*`，无需 `ts_backfill`。

| 字段 | userCount | ac | 语义 | 角色 |
|---|---:|---:|---|---|
| `count_institutional_buyers_security` | 42 | 61 | 期间内买入该股的机构数 | **主信号（广度）** |
| `count_institutional_sellers_security` | 36 | 51 | 期间内卖出该股的机构数 | **主信号（广度）** |
| `count_institutional_holders_security` | 19 | 31 | 当前持有该股的机构数 | **分母（剥披露阶梯）** |
| `market_value_institutional_shares_acquired` | 52 | 85 | 期间内机构买入金额 | 主信号（金额流） |
| `market_value_institutional_shares_disposed` | 23 | 39 | 期间内机构卖出金额 | 主信号（金额流） |
| `quantity_institutional_shares_acquired` | 48 | 66 | 期间内机构买入股数 | 辅助 |
| `quantity_institutional_shares_disposed` | 27 | 39 | 期间内机构卖出股数 | 辅助 |
| `aggregate_equity_value_institutions` | 20 | 24 | 全部机构持股总市值 | **分母（金额归一）** |
| `aggregate_equity_value_all_owners` | 17 | 19 | 全部持有人持股总市值 | 分母（持股率） |
| `aggregate_share_count_institutions` | 16 | 20 | 全部机构持股总股数 | 分母（持股率） |
| `aggregate_share_count_all_owners` | 14 | 21 | 全部持有人持股总股数 | 分母（持股率） |

**更新频率**：季报披露节奏（13F 类），存在**季度阶梯跳变** ⇒ 分母必须用 `ts_mean(_,66)` 平滑剥离阶梯。
**分布特征**：计数类（buyers/sellers/holders）长尾，金额类（market_value）极长尾 ⇒ 一律先 `rank` / `group_rank`。

---

## 五、已派发波次

### INST6-A（`JOQZ73Dj549aZX1dDIMqeBR`，8 条，`decay 9 / trunc 0.03`）

复用记忆中的**可移植冠军骨架**（institutions6 类披露计数数据）：
`trade_when(ts_arg_max(HOLDERS,G) < T, signed_power(ts_quantile(divide(BUYERS, ts_mean(HOLDERS,M)), W, driver="gaussian"), p), -1)`

| # | 模板（结构互异） | 表达式 |
|---|---|---|
| 1 | **门控 + 广度比（冠军骨架）** | `trade_when(ts_arg_max(count_institutional_holders_security,252) < 66, signed_power(ts_quantile(divide(count_institutional_buyers_security, ts_mean(count_institutional_holders_security,66)),252,driver="gaussian"),1.6), -1)` |
| 2 | 净广度流 / 持仓基数 | `group_rank(ts_mean(divide(subtract(buyers, sellers), ts_mean(holders,66)),66), sector)` |
| 3 | 广度平衡比（无量纲） | `group_rank(ts_mean(divide(subtract(buyers, sellers), add(buyers, sellers)),66), sector)` |
| 4 | 净金额流强度 | `group_rank(ts_mean(divide(subtract(acq, dis), ts_mean(aggregate_equity_value_institutions,66)),66), sector)` |
| 5 | 机构持股率（市值口径） | `group_rank(ts_mean(divide(aggregate_equity_value_institutions, aggregate_equity_value_all_owners),66), sector)` |
| 6 | 持仓基数增长（关注度） | `group_rank(ts_delta(ts_mean(holders,66),252), sector)` |
| 7 | 单笔买入额（信念强度） | `group_rank(ts_mean(divide(acq, add(buyers,1)),66), sector)` |
| 8 | 净买入持续性（252 日占比） | `group_rank(ts_mean(greater(subtract(buyers, sellers),0),252), sector)` |

（字段名已简写，实参为全名）

**参数理由**（非时间窗口类取值必须给理由）：
- `G=252 / T=66`：原骨架的 `846…` 是为另一区域调优；DEU 用 **252 日（一年 = 4 个披露周期）**作门控视界、
  `T=66`（= 一年窗口内的最近 1/4 段）。含义 = 「机构持仓基数在过去一年高点附近（最近一季内见顶）」时才开仓。
- `M=66`（季度，22×3）：剥季度披露阶梯跳变的最小充分窗口。
- `p=1.6`：原骨架实证值，保留以复用其非线性形状。
- `decay 9 / trunc 0.03`：原骨架配套设置，用于压低换手 + 削尾。

preflight：`valid=true / unknown_soft=[] / unknown_fields=["gaussian"](已知假阳性) / platform_field_count=7`

### STAR-REV-A（`2zdYN22IN5cea6dx2CdmNHg`，8 条，基线设置）

**设计依据**：`predictive_starmine` 已贡献 2 颗严格 ATOM，其腿为
`mean_estimate_change_pct_f12m_earnings_14d_4` + `predicted_surprise_f12m_ebitda_4`（`E56pROb9` 另用 `mdl216_*`）。
本波 **8 条全部换到 revenue 族**，与已交付 3 颗的**腿集合完全不相交** ⇒ 按「腿是否相交」判据可作新颗。

| # | 模板（结构互异） | 核心字段 | cov |
|---|---|---|---|
| 1 | **修正广度净额**（diffusion） | `analyst_upward/downward_revision_count_fy1_revenue_30d_4` | 0.9725 |
| 2 | 修正广度平衡比 | 同上（ratio 形式） | 0.9725 |
| 3 | F12M 收入预期修正（7 日幅度） | `mean_estimate_change_pct_f12m_revenue_7d_4` | 0.9704 |
| 4 | FY1 收入预期修正（30 日幅度） | `mean_estimate_change_pct_fy1_revenue_30d_5` | 0.9706 |
| 5 | 预测收入超预期（pct，F12M） | `predicted_surprise_pct_f12m_revenue_4` | 0.9625 |
| 6 | 收入增速加速度（FY2/FY1 − FY1/LY） | `smest_growth_next_vs_this_yr_revenue_4` / `smest_growth_this_vs_last_yr_revenue_3` | 0.9624 / 0.9554 |
| 7 | 估值（P/Revenue，取负 = 便宜者优） | `mean_estimate_price_ratio_f12m_revenue_5` | 0.9706 |
| 8 | 卖方 ARM 收入因子分 | `arm_revenue_component_score_3` | 0.9546 |

**为什么这是新机制而非换窗口**：
- 模板 1/2 是 **修正广度（breadth / diffusion）**，与已交付件的 **修正幅度（magnitude）** 是两个不同的信息加工方式；
- 模板 6 是 **二阶（加速度）**，模板 7 是 **估值水平**，模板 8 是 **卖方合成因子**；
- 全部用 revenue 族，规避与 `earnings/ebitda` 腿的相交。

preflight：`valid=true / unknown_fields=[] / unknown_soft=[] / platform_field_count=9`

---

## 六、下一波待发

### RISK60-B（沿 `MPY9VNY9` 的 proven 几何换轨）

**依据**：DEU 唯一成功的做空件 `MPY9VNY9`（S 1.59）用的是
`-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(shrt3_bar,240)), rank(ts_delta(shrt3_bar,176))), target_tvr=0.03), subindustry)`，
即 **长周期变化 + 双视界确认**，不是水平。RISK60-A 全部用「水平 → 排序」几何，最强 0.81。
⇒ RISK60-B 把同一几何搬到 `rsk60_offer` / `rsk60_crowding`。

候选（8 条，待 preflight）：
1. `-group_rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),22), 252), sector)` —— 年度费率动量
2. `-group_rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),22), 176), sector)` —— 8 个月费率动量
3. `-group_rank(multiply(rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),22),240)), rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),22),176))), sector)` —— **双视界相乘（MPY9VNY9 同几何）**
4. `-group_rank(ts_target_tvr_decay(multiply(rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),22),240)), rank(ts_delta(ts_backfill(vec_avg(rsk60_offer),22),176))), target_tvr=0.03), subindustry)` —— 同 3 + 换手目标
5. `-group_rank(ts_sum(ts_backfill(vec_avg(rsk60_crowding),22), 252), subindustry)` —— 累计做空拥挤
6. `-group_rank(ts_mean(ts_backfill(vec_avg(rsk60_crowding),22), 252), sector)` —— 年度拥挤水平
7. `-group_rank(ts_delta(ts_backfill(vec_avg(rsk60_crowding),22), 176), sector)` —— 拥挤度变化
8. `group_rank(divide(ts_backfill(vec_avg(rsk60_offer),22), add(ts_backfill(vec_avg(lending_fee_bid_rate),22),0.0001)), sector)` —— **符号翻正**（A 波已证该比值是反向指标，S −0.73）

---

## 七、本波新增工具坑汇总

1. **★ `add(<CSPrice 单位字段>, 无量纲常数)` 在 `unitHandling=VERIFY` 下非法**，报
   `Incompatible unit for input of "add" at index 1, expected "Unit[CSPrice:1]", found "Unit[]"`。
   状态是 `WARNING`（alpha 仍被创建但无指标），**不是** `CANCELLED`，所以不会整批崩但会静默丢件。
   **修法**：先 `rank()` 抹量纲再运算。
2. **`ts_zscore` 用在稀疏披露型字段上会放大跳变**（实测 TO 1.04、drawdown 2.04）。稀疏字段一律先 `ts_backfill`。
3. **preflight 三重盲区再确认**：不校验算子存在性、不校验字段名存在性、**不校验单位兼容性**。
   `unknown_fields` 只含 `gaussian` 等 driver 值时是假阳性，可忽略。
4. **`get_datasets` 按 category 分查**可避免整表外置（DEU 全表 153KB / 639 块），单 category 返回可直接内联读取。
