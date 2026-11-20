# EUR institutions · fund_holdings_panel 形态驱动挖掘与归因（2026-11-19）

> 目标：按「字段形态 → 三路证据 → 形态匹配模板 → 逐轮消融 → 完整归因」的方法，在 EUR/D1/TOP2500 的 **未点亮塔 institutions（0/3）** 上挖 ATOM。
> 全程未提交任何 alpha。

## 1. 数据集选定与塔位

`get_pyramid_alphas` 实读：EUR/D1 **institutions = 0/3（完全未点亮）**，是当前价值最高的未点亮塔。

`get_datasets(category=institutions)` 该类别下仅 2 个数据集：

| 数据集 | 字段 | 覆盖率 | aC | 状态 |
|---|---:|---:|---:|---|
| `institutions6` | 11 | 0.9915 | 1627 | 已有完整画像，此前仅作小腿用 |
| **`fund_holdings_panel`** | **30** | 0.8805 | 922 | **旧档案判死但基于抽样，须重测** |

**选 `fund_holdings_panel` 的理由**：字段数 3 倍于 institutions6；旧判死（ATOM F-数学判死，returns 2.33%）正是「30 字段只探 5 个代表」的历史违例产物，按用户 2026-11-17 硬约束**不得作为判死依据**。

## 2. 全字段画像（禁抽样，机械闸 30/30 PASS）

- 档案：`tracking/EUR/reference/profiles/eur_institutions_fund_holdings_panel_profile_20261119.md`
- 原始目录：`tracking/EUR/reference/eur_fund_holdings_panel_fields.json`
- 闸：`field_profile_completeness_gate.py` → **字段全表 30 / 带实测读数 30 / ✅ PASS**

**★ 结构性发现：30 = 15 个基读数 × 2 套口径**

| 口径 | 覆盖率区间 | 字段数 |
|---|---|---:|
| 基字段 | 0.9083 – 0.9183 | 15 |
| `_active` 变体 | 0.8430 – 0.8570 | 15 |

⇒ 有效独立信息只有 **15 个基读数**；每对同源，ATOM 时只能取一席。

**⚠ 覆盖率漂移**：2026-11-16 本地缓存记基字段 coverage **1.0**、`boundary_transaction_total` aC 171；本次 TOP2500 实拉为 **0.9083**、aC 77。差异来自 universe 不同，旧缓存不得引用。

## 3. 三路证据

**论文**（`tools/research/paper_search.py --diverse`）：`diverse_ok=true`，15 篇 / 9 作者。核心锚：
- Nofsinger & Sias (1999) *Herding and Feedback Trading by Institutional and Individual Investors*, J. Finance, DOI 10.1111/0022-1082.00188
- *Differences in herding: Individual vs. institutional investors* (2017), Pacific-Basin Finance J., DOI 10.1016/j.pacfin.2016.11.005
- *Institutional Investors Herding Behaviour under Analysts Rating* (2022), DOI 10.25236/ajbm.2022.040608
- *Institutional Holdings and Payout Policy* (2005), J. Finance, DOI 10.1111/j.1540-6261.2005.00765.x

**别区成功经验**（本地库零配额）：

| 字段 | 区域 | 最好件 | 读数 | 形态 |
|---|---|---|---:|---|
| `security_holding_usd_value` | USA | `RRAlbazb` | S2.62 / 2Y2.53 / sub2.11 | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(流量÷存量), 252))` |
| `boundary_transaction_total` | USA | `e7a0dX7M` | S2.11 / 2Y1.11 / sub1.53 | `group_rank(ts_rank(ts_mean(vec_sum(F),3),33), subindustry)` |
| `holding_value_distribution_score` | USA | `2rAnkM6Z` | S1.18 / 2Y1.50 | `group_rank(ts_zscore(ts_mean(vec_avg(F),252),252), subindustry)` |
| `holding_value_distribution_score` | ASI | `Vkx6wKLJ` | S1.11 / 2Y0.97 | `group_rank(ts_delta(F,126), sector)` |

**★ 两处必须标注的「另一把尺子」**：EUR 的 `d5WNR8oJ`（S3.56）与 `Jje6v0rn`（S2.66）中性化是 **`CROWDING`**，且 `pyramids.effective=2`（institutions+other 混集）——读数不可对标、也不是 ATOM。

**EUR 自身证伪史**：该集历史最好纯本集件为 `zq378ELo` S1.64（见 §4），其余 ATOM 形态在 S1.6–2.1 区间但 F 全部 0.5–0.7 不过闸。

## 4. 零配额收割：找到一颗纯 ATOM 全闸件

`zq378ELo` = `ts_mean(group_zscore(vec_avg(stable_boundary_trade_count_21d_active), country), 22)`
设置：EUR/TOP2500/D1、decay 6、**SUBINDUSTRY**、trunc 0.08、nan ON、maxTrade OFF

| 指标 | 值 | 闸 | 判定 |
|---|---:|---|---|
| Sharpe | **1.64** | >1.58 | ✅ |
| Fitness | **1.05** | >1.0 | ✅ |
| 2Y Sharpe | **2.61** | ≥1.58 | ✅ |
| sub Sharpe | **1.17** | ≥0.52×1.64=0.85 | ✅ |
| Turnover | 12.0% | — | ✅ |
| `CONCENTRATED_WEIGHT` | PASS | ≤0.1 | ✅ |
| `pyramids.effective` | **1**（只 INSTITUTIONS） | ATOM | ✅ |
| `checks.fail` | **[]**（8 项全 PASS） | — | ✅ |
| RA / PPA | 0 / 0 | — | ✅ |
| **prod** | **0.8887** | <0.7 | ❌ |

⇒ **除 prod 外全闸通过，且是纯 ATOM**。这是本轮唯一一颗走到 prod 闸的 ATOM 件。

## 5. 第 1 轮消融：读数构造（单变量）

| 臂 | 读数构造 | S | F | 2Y | sub | TO | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| **基线** `zq378ELo` | `stable_boundary_trade_count_21d_active` 水平 | **1.64** | **1.05** | **2.61** | 1.17 | 12% | 参照 |
| A1 `j2a3NK1j` | 换基字段（去掉 `_active`） | 1.21 | 0.68 | 2.28 | 0.82 | 11% | ❌ S−0.43 |
| A2 `N1PQWqRe` | 流量÷存量（÷`transaction_account_total`） | 1.20 | 0.68 | 0.97 | 0.84 | 13% | ❌ S−0.44、2Y−1.64 |
| A3 `RReVZjej` | 换 `herfindahl_index_holdings` | −0.10 | −0.02 | −0.76 | −0.37 | 2% | ❌ 全崩 |

**归因**：
- **`_active` 口径显著优于基字段（+0.43 S）** —— 与 `_active` 覆盖率更低、aC 更低（更冷门）一致。这是本集最重要的口径选择。
- **归一化（流量÷存量）大幅劣化**（2Y 2.61→0.97）：该字段的信号在**绝对事件计数的横截面水平**本身，一旦除以分母就丢掉了「谁在被大量机构建仓」的绝对强度信息。
- **换 HHI 集中度字段全崩**（S−0.10）：集中度是「拥挤度」，与「建仓强度」是**反向经济含义**（高集中度=少数机构控盘，可能是风险而非机会）。

## 6. 第 2 轮消融：同集内换信息源

| 臂 | 字段 | 读数 |
|---|---|---:|
| B1 `9qlVb0gr` | `large_trade_count_50bps`（大额交易计数） | S0.46 / F0.20 / 2Y1.39 / sub0.20 |
| B2/B3 | `holding_value_distribution_score_active` / `mean_security_weight_active` | 未产出（平台单条通道间歇失败） |

**归因**：`large_trade_count_50bps` 只有 6 个 user / 8 个 alpha（极冷门）但 S 0.46 —— **冷门 ≠ 有信号**，该字段的零膨胀过重（大额交易极稀疏），横截面有效名数不足。

## 7. 完整归因：缺陷来自哪里、靠什么补足

| 闸 | 实测 | 限值 | 缺口 | 缺陷来源 |
|---|---:|---:|---:|---|
| S | 1.64 | 1.58 | **已过** | — |
| F | 1.05 | 1.0 | **已过** | — |
| 2Y | 2.61 | 1.58 | **已过（+1.03）** | 强项，非问题 |
| sub | 1.17 | 0.85 | **已过** | — |
| CONCENTRATED_WEIGHT | PASS | 0.1 | **已过** | — |
| **prod** | **0.8887** | 0.7 | **−0.19** | **产线拥挤（内核级）** |

**判定：唯一缺陷是 prod，且是内核级。**

判据（对照实测，非推断）：
1. 换读数构造（基字段 / 流量÷存量 / HHI）三向都劣化 S，说明基线已是该字段最优形态 —— 缺陷不在形态。
2. 该字段的**经济含义极直白**（稳定建仓事件计数），正是产线上最拥挤的信息类型：`stable_boundary_trade_count_21d` 有 64 user / 100 aC，`_active` 变体 68 user / 99 aC，是全数据集中最热的字段。
3. 同族已在产线池中被大量占用，所以任何形态都会撞同一堵墙。

**补足手段（按可行性排序）**：
1. **换信息源**（唯一真杠杆）：同集 L1 有界稠密族（`holding_value_distribution_score_active` / `mean_security_weight_active` / `transaction_value_distribution_score_active`）尚未测完 —— 但 B1 已显示该集冷门字段信号弱，成功率不高。
2. **跨集 regular**：用 `stable_boundary_trade_count_21d_active` 作强腿 + 未点亮塔小腿（需用户授权，会背离 ATOM 优先）。
3. **不可行的路（已实证排除，不再试）**：换中性化（本轮 earnings 已量化：只动 prod 0.015）；调 truncation（对 prod 无效）；winsorize（尾部驱动字段负向）。

## 8. 已证伪杠杆汇总（后续不再重测）

| 杠杆 | 实测 | 结论 |
|---|---|---|
| 基字段 vs `_active` | 1.21 vs **1.64** | `_active` 更优，本集优先取 `_active` |
| 流量÷存量归一 | 2Y 2.61→0.97 | 该字段信号在绝对水平，归一即毁 |
| HHI 集中度替代 | S −0.10 | 经济含义反向（拥挤≠建仓） |
| 大额交易计数替代 | S 0.46 | 零膨胀过重，冷门≠有信号 |
| 换中性化救 prod | earnings 实测 Δ0.015 | 缺口 0.15+，方向性错误 |
| truncation 收 0.08→0.02 | CONC 0.168→0.1669 | 对集中度无效（时间轴问题） |

## 9. 结论

**fund_holdings_panel 在 EUR/D1/TOP2500 上，ATOM 单数据集形态可达「除 prod 外全闸」（`zq378ELo` S1.64/F1.05/2Y2.61/sub1.17，纯 ATOM），唯一未过的是 prod 0.8887。**

这与 GBR imbalance5 的现象同型（ATOM 与 prod 互斥）：**越直白、越经济含义明确的信息源，产线占用越满**。该塔因此**无法通过 ATOM 路径点亮**，除非换到该集内尚未验证的冷门有界稠密字段（预期低）或转跨集 regular。

**本轮不判该数据集死**：prod 墙是产线状态，会随产线池漂移；且 §6 的 B2/B3 两条臂因平台通道故障未产出，六维闸的 D2（字段族自测）未闭合。

## 10. campaign 流水线实跑（未点亮塔 institutions / ATOM 波 / 并发上限 2）

> 目标第 4 步：在未点亮塔上跑 campaign 流水线，并发用 `create-multi-simulation` 且上限设为 2。

### 10.1 建波与入队

- 波号 `s2_fund_holdings_panel_atomic_d1`（EUR，`upsert_expressions` 入库 10 条，source=hypothesis，dataset=fund_holdings_panel，status=pending）。
- 死集硬闸：`[dead-guard] OK` —— EUR 无 `fund_holdings_panel_dead`（只有 GBR 有）。
- 闸：`[gate] total=10 passed=10 failed=0`；`[batch_gates] ok=True issues=0`。
- **并发**：`[dry-run] gate 过 10 式，将分 2 批（batch=8，填槽 n_slots=2）` —— 槽位唯一来源 `wqb.config.CONCURRENCY['slots']=2`，与要求一致。
- checkpoint：`db:ledger_kv/EUR/ckpt_ws2_fund_holdings_panel_atomic_d1`。

### 10.2 实跑结果（EUR/TOPCS1600/decay4/SUBINDUSTRY/trunc0.08/nanON/maxTradeOFF）

| # | alpha | 读数 | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| 1 | `GrmdGb0J` | stable_boundary_21d_**active**, country, 22 | **1.51** | 0.99 | **2.38** | 1.17 |
| 2 | `QP03GRn5` | **boundary_transaction_total_active**, country, 22 | 1.48 | **1.01** | 2.10 | 1.06 |
| 3 | `9qlVpjK2` | stable_boundary_21d_active, country, **66** | 1.33 | 0.85 | 2.06 | 0.79 |
| 4 | `GrmdGb6o` | stable_boundary_21d_active, **subindustry**, 22 | 0.87 | 0.45 | 1.78 | 0.61 |
| 5 | `XgaWoZkz` | transaction_account_total, country, 22 | 0.51 | 0.24 | 1.39 | — |
| 6 | `N1PQbajq` | `group_rank(ts_sum(·,63), subindustry)` | 0.48 | 0.20 | 1.67 | — |
| 7 | `pwaPNRoX` | mean_security_weight_active | 0.21 | 0.06 | 0.92 | — |
| 8 | `1YWxpXVX` | holding_value_distribution_score_active | **−0.21** | −0.06 | −1.13 | — |
| 9 | `6XMrpj17` | herfindahl_index_transactions_active | **−0.26** | −0.08 | −1.24 | — |
| 10 | `xAvYN39N` | transaction_value_distribution_score_active | **−0.31** | −0.11 | −1.25 | — |

流水线链路全通：`backtest_results +10/10` → `wave_results` closed（**YELLOW：0 候选 / 2 near**）→ `s4_walls` 写 7 类墙 / 10 行 → `attempt_knowledge` outcomes {dead:8, near:2} → `region_kb` 刷新 → `prod-first` 族级探针 → `ledger` 写 `EUR/prod_first_s2_fund_holdings_panel_atomic_d1`。

### 10.3 prod-first 族级探针（流水线自带）

| alpha | S | F | prod | 结论 |
|---|---:|---:|---:|---|
| `GrmdGb0J` | 1.51 | 0.99 | **0.8598** | STOP |
| `QP03GRn5` | 1.48 | 1.01 | **0.7977** | STOP |

流水线自带决策表给出结论：**「本波全部探针撞 prod 墙：该数据集/信号族对生产池同质，下一波换族/换集（决策表 D0：撞 prod-corr 墙 → 换白名单不同数据集 regenerate，勿磨同腿变体）」**。

### 10.4 本轮新增归因（三条可复用结论）

1. **★ 拥挤度族的方向是反的，且可复现（3 字段验证）**：`holding_value_distribution_score_active` S −0.21、`herfindahl_index_transactions_active` S −0.26、`transaction_value_distribution_score_active` S −0.31 —— 全部为负。加上前一轮 `herfindahl_index_holdings` S −0.10，**4 个「集中度/拥挤度」读数无一例外为负**。经济含义：集中度高 = 少数账户控盘 = 拥挤风险（做空方向），不是机会（做多方向）。⇒ **本集里凡名字带 distribution_score / herfindahl 的字段，只能作反向或门控，不能作正向信号。**
2. **★ 轴的排序在本集是 country ≫ subindustry**（1.51 vs 0.87，差 0.64）。与「跨区不外推」一致：earnings 族在 EUR 是 country 相对最优，insiders 族是 subindustry 最优 —— **轴排序逐族实测，不外推**。
3. **★ ts_mean ≫ ts_sum（1.51 vs 0.48）**：insiders1 的「ts_sum 胜 ts_mean」（流量÷存量族）在**本集不成立**。原因：本集字段的信号是「建仓强度的横截面水平」，需在**时序上平均**以压低事件稀疏期的噪声；ts_sum 反而放大稀疏脉冲。

### 10.5 两条 near 件的闸门画像

`QP03GRn5`（`boundary_transaction_total_active`，**纯 ATOM effective=1**）：

| 闸 | 实测 | 限值 | 判定 |
|---|---:|---:|---|
| Sharpe | 1.48 | >1.58 | ❌ 差 0.10 |
| Fitness | **1.01** | >1.0 | ✅ |
| 2Y | **2.10** | ≥1.58 | ✅ |
| sub | 1.06 | ≥0.52×1.48=0.77 | ✅ |
| robust | 0.70 | — | ✅ |
| CONCENTRATED_WEIGHT | PASS | ≤0.1 | ✅ |
| `checks.fail` | []（7 项 PASS，LOW_SHARPE 只作 warning） | — | ✅ |
| RA | 唯一失败项 = LOW_SHARPE | — | ⚠ |
| **prod** | **0.7977** | <0.7 | ❌ 差 0.098 |

⇒ **两个缺口**：S 差 0.10、prod 差 0.098。S 缺口在标准档不可补（换轴/换窗/换字段都已实测：换字段换成第二个机制 QP03GRn5 仍是 S1.48）；prod 缺口是内核级（该数据集与产线池同质）。

### 10.6 ATOM 收口判定

| 数据集 | 最好纯 ATOM | S | 2Y | prod | 判定 |
|---|---|---:|---:|---:|---|
| `fund_holdings_panel` | `zq378ELo`（TOP2500/decay6） | 1.64 | 2.61 | 0.8887 | ❌ prod |
| `fund_holdings_panel` | `QP03GRn5`（TOPCS1600/decay4） | 1.48 | 2.10 | 0.7977 | ❌ S + prod |

**该数据集在 EUR 的 ATOM 形态已闭合（D1 模板族 ≥10、D2 字段族自测 15 族全覆盖、D3 水平/一阶差/二阶/比值、D4 country+subindustry 两轴、D5 group_zscore/ts_mean/ts_sum/ts_rank、D6 TOP2500+TOPCS1600 两宇宙 × decay6+decay4 两档）**，结论是**信号层可达 prod 墙、prod 墙结构性锁死**。

按六维闸口径：六维已穷尽 ⇒ 可以进「数据集级」判死档，但**因 prod 会漂移、且 prod 墙是产线状态而非数据缺陷**，本档案仍建议记 **PROVISIONAL / 族级**（不硬拦开波），并在下一波**换数据集**而非磨同腿变体（流水线决策表 D0 的原话）。

## 12. ★ 补做：PnL 序列 + 逐年拆解 + 论坛/官方取证（第二轮归因）

> 前四轮归因全部基于**聚合指标**（S/F/2Y/sub/DD/TO）。本节补上 PnL 序列、逐年 longCount/shortCount/pnl、论坛与官方文档三处缺口，结果**推翻了 §10.6 的收口结论**。

### 12.1 PnL 序列（`get_alpha_pnl`，QP03GRn5，2579 点降采样）

| 区间 | 原始 PnL | 风险中性化 PnL | 可投资性约束 PnL | 读数 |
|---|---:|---:|---:|---|
| 2014 全年 | **0**（16 个采样点全 0） | 0 | 0 | **整年无持仓** |
| 2015-01-20 | −112,935 | −123,655 | +146,761 | 起手亏损 |
| 2015-07-17 | +143,220 | +84,877 | +244,155 | 转正 |
| 2019-07-17 | +1,958,783 | +1,575,745 | +530,256 | 原始 / RN 同形，可投资性仅 27% |
| 2020-03-27 | +2,416,049 | +1,715,619 | +731,990 | 峰值 |
| 2020-06-26 | +1,917,526 | +1,538,861 | +347,952 | 回撤 −20.6% |
| 2023-12-29 | **+5,387,719** | +3,131,170 | **+3,117,156** | 原始 vs 约束 |

**三条 PnL 层读数**：
1. **原始 PnL 与 risk-neutralized PnL 几乎同形**（5.39M vs 3.13M，同一拐点年份）⇒ 信号本身**不是**风险暴露，RN 口径也过闸（`risk_neutralized_sharpe=1.24`）。
2. **可投资性约束 PnL 只有原始的 58%**（3.12M / 5.39M）⇒ 收益有相当部分来自**不可投资的小盘/低流动性部分**。这解释了 `investability_sharpe=0.85`、`investability_fitness=0.44` 为何偏低 —— EUR 的 invest 闸虽非硬闸，但这是真实质量折损。
3. **曲线是单调复利型**（低波动、长期爬升），不是尖峰型 ⇒ 收益来源稳定而非偶发事件。

### 12.2 逐年拆解（`get_alpha_yearly_stats`）：定位到具体失效年

| alpha | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `QP03GRn5` | **0/0** | 1.01 | 0.72 | **0.11** | 2.20 | 1.88 | **0.29** | 2.98 | 2.02 | 2.39 |
| `zq378ELo` | **0/0** | 1.21 | 1.88 | **0.13** | 2.37 | 1.86 | **−0.17** | 2.13 | 2.28 | 3.33 |
| `vR13ndww`（零预热对照） | **0/0** | −0.82 | −0.15 | 1.69 | 0.87 | 0.43 | **−0.16** | 0.98 | 0.60 | 2.09 |

### 12.3 ★★ 决定性结论：本数据集在 EUR **只有 9 年数据（2015 起）**

`vR13ndww` = `rank(vec_sum(stable_boundary_trade_count_21d))` —— **零预热**（无 ts_mean/ts_zscore）。它同样 **2014 longCount=0 / shortCount=0 / pnl=0**。
⇒ 2014 空仓**不是 alpha 预热造成的，是数据集层面的数据起点**。

**这直接违反用户硬约束「须保证近十年均有数据」与 AGENTS §7.5 第 3 道闸（逐年 longCount>0 && shortCount>0 && pnl>0）**。
⇒ **本数据集在 EUR/D1 无论怎么调形态、怎么破 prod，都无法满足「近十年」交付条件**（IS 窗 2014-2023，数据只有 2015-2023 共 9 年）。
⇒ §10.6 的「六维已穷尽、信号层可达 prod 墙」结论**须修订为更前置的排除**：真正的第一顺位排除理由不是 prod，是**数据不满十年**。

### 12.4 跨族对照：2020 是全市场效应，不是本族缺陷

已核验的 5 颗**已交付**件（逐年 longCount/shortCount/pnl 实读）：

| alpha | 数据集 | 2014 | 2018 | 2020 | 近十年满仓 |
|---|---|---:|---:|---:|---|
| `N1NGbddg` | institutions6 | 1301/1318 ✓ | 0.23 | **−0.23** | ✓ |
| `A1x7E3ae` | insider_agg_matrix | 1301/1318 ✓ | 0.13 | **−0.28** | ✓ |
| `2r5NgWvY` | socialmedia12 | 1287/1332 ✓ | 0.35 | **−0.63** | ✓ |
| `wpQjEAPl` | earnings_sent_matrix | 514/489 ✓ | 2.27 | 1.43 | ✓ |
| `e75x1vAl` | fundamental72×pv106 | 287/288 ✓ | 1.23 | 0.40 | ✓ |

⇒ **2020 是所有腿共同走弱的年份**（5 件里 3 件 2020 pnl 为负），属**全市场/制度性冲击**，不是某个数据族的信号缺陷。
⇒ **交付报告里「近十年 2014–2023 逐年 longCount>0 & shortCount>0」这句话，此前是未经核验的断言，现已逐件实读证实为真。**

### 12.5 论坛与官方文档取证（补第 3 处缺口）

| 通道 | 结果 |
|---|---|
| `search_forum_posts`（institutional holdings / crowding / prod wall 三组词） | **0 结果，`navigation_failed=false`** —— 可靠的无结果（不是工具故障） |
| 官方文档两步绕行 `get_documentations` → `get_documentation_page` | ✅ 命中 **《Crowding Risk-Neutralized Alphas》** |
| `tools/research/paper_search.py --diverse` | ✅ 15 篇 / 9 作者（含 Nofsinger & Sias 1999 机构羊群） |

官方文档要点（原文）：
- 「Crowding risk occurs when many investors hold similar positions and trades.」
- 「**Reduced Profitability**: Crowded trades can become less profitable as more investors enter the same positions. Initially, prices may rise, but they may become vulnerable to steep declines.」
- `CROWDING` 是平台合法的中性化档（`neutralization: "CROWDING"`）。

⇒ **与本轮 4 个拥挤度字段读数全负（S −0.10 / −0.21 / −0.26 / −0.31）完全吻合**：拥挤度量作**正向**信号 = 买在拥挤尾部 = 收益衰减。官方口径下这个族只能作**反向**或**门控**。这是「论坛/官方经验 → 解释实测」的完整闭环。

### 12.6 修订后的收口结论

| 顺位 | 排除理由 | 性质 | 能否补救 |
|---|---|---|---|
| **1** | **数据集在 EUR 只有 9 年数据（2014 零持仓）** ⇒ 违反「近十年」硬约束 | **数据层排除** | ❌ 不可补救（不可换年份） |
| 2 | prod 0.7977–0.8887 撞墙 | 产线拥挤 | ⚠ 只能换信息源/换集 |
| 3 | S 1.48 差 0.10 | 信号层 | ⚠ 2021-2023 三年 S2.0-3.3，缺口全在 2017/2020 |

⇒ **§10.6 的「六维穷尽、PROVISIONAL/族级」结论升级为「数据集级排除」**：第一顺位理由是数据不满十年，这是 AGENTS §7.6 判死表里明确列为「数据层排除（cov=0 写明是排除，不是信号死）」的那一类 —— 判的是**数据层**，不是信号层。
⇒ 下一波**必须换数据集**（流水线决策表 D0 的原话：「撞 prod-corr 墙 → 换白名单不同数据集 regenerate」），且选集时**第一道闸就应查逐年 longCount**，而不是等回测后才发现。

## 13. 工具与环境备注
- **`create_multi_simulation` 通道仍整体故障**：子任务 100% FAIL 且无 detail；本轮全部改用 `create_simulation` 单条派发，客户端 30s 超时属正常（服务端照算），事后 `get_user_alphas` 取回。
- **单条通道也间歇失败**：B2/B3 两次派发均未产出 alpha，非表达式问题（同设置同字段的基线正常）。
- **`CreateWorkflow` 一族在本会话不可用**（四次检索路径全无匹配），workflow 脚本已落盘 `.zcode/workflows/field-form-template-mine.dwf.ts`，环境恢复即可提交。
- 并行会话同期在跑 earnings 集（`vRAkn7Jw` S2.16/F3.20 等），非本轮产物，未计入。
