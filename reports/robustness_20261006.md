# 稳健性审计报告 · 2026-10-06

> skill: `brain-alpha-robustness`（Phase B 归因 → Phase C 反过拟合闸 → Phase D 回写）
> 台账唯一事实源：`ledger DEU::robustness_58gkLAkk`（本文件仅供人读）

---

## 1 被审候选：`58gkLAkk`（DEU / TOP500 / D1）

| 项 | 值 |
|---|---|
| 表达式 | `group_neutralize(group_neutralize(group_neutralize(group_neutralize(quantile(add(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 8), ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 252))), oth455_relation_n2v_p10_q50_w1_pca_fact1_cluster_20), oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20), subindustry), bucket(rank(ts_mean(ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 252)), range="0,1,0.1"))` |
| settings | decay=8 / SUBINDUSTRY / truncation=0.08 / nanHandling=OFF / maxTrade=OFF |
| 顶层指标 | S **1.75** · F **1.42** · TO 0.1457 · returns 0.0959 · drawdown 0.0781 · **margin 0.001316**（13.2 bp） · long143 / short141 |
| 平台 checks | `failed_ra_count = 0`；`fail: []`；pass 含 **IS_LADDER_SHARPE**、SUB、CW、CLUSTER、MATCHES_PYRAMID |
| 塔 | MODEL×1.8 + OTHER×1.8（effective=2，双 ×1.8） |
| 相关性 | **prod 0.5381 ✅ / self 0.5153 ✅**（`all_passed: true`） |

---

## 2 Phase C：反过拟合闸（单一变量口径：最近 3 个 IS 年）

| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed = 0，无名单内 PENDING | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 2021/2022/2023 = **1.69 / 1.54 / 2.73**，均值 **1.987** ≥ 1.58；平年 0 | **PASS** |
| Recent-3yr CV_Sharpe | **0.266**（< 0.40） | **PASS** |
| 衰减比 last/full | **1.548**（≥ 0.50） | **PASS** |
| Recent-3yr max/min 比 | **1.773**（≤ 3） | **PASS** |
| 平年数（近 3 年） | **0** | **PASS** |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE` = PASS（1.22） | **PASS** |
| Margin @ turnover | **13.2 bp** @ TVR 14.6%（≥ 5 bp） | **PASS** |
| 经济可解释性 | 「分析师对未来 12 个月盈利的 14 天一致预期修正（上调）→ 市场反应不足」一句话可写 | **PASS** |

### 软标记（记录、不判死）

1. **算子数 = 13**（> 5 提示过拟合风险；REGULAR 规则不据此 REJECT，PPA 才有 ≤8 硬上限）。
2. **2017 年疲软**：sharpe 0.23 / margin 仅 1.6 bp —— 全历史呈「强(2014-15) → 洼地(2016-17) → 恢复(2018-)」形态。
   按闸门口径这属「全历史早年疲软」，**只记软标记，绝不 REJECT**；且不在最近 3 年窗口内。
3. **Top-5 个股集中度不可得**：`get_alpha_pnl` 仅返回 date / pnl / risk-neutralized / investability 四列，无逐股分解。
4. `performance_comparison` 返回 `detail: Not found.`（该 alpha 无相对池贡献数据）。

### 逐年明细（IS）

| year | sharpe | returns | drawdown | turnover | margin | fitness |
|---|---:|---:|---:|---:|---:|---:|
| 2014 | 2.36 | 0.1306 | 0.0370 | 0.1428 | 0.001830 | 2.26 |
| 2015 | 2.35 | 0.1282 | 0.0350 | 0.1456 | 0.001762 | 2.21 |
| 2016 | 1.12 | 0.0645 | 0.0583 | 0.1516 | 0.000851 | 0.73 |
| 2017 | **0.23** | 0.0121 | 0.0436 | 0.1472 | **0.000164** | 0.07 |
| 2018 | 2.29 | 0.1228 | 0.0229 | 0.1431 | 0.001716 | 2.12 |
| 2019 | 1.86 | 0.0930 | 0.0330 | 0.1452 | 0.001281 | 1.49 |
| 2020 | 1.47 | 0.0955 | 0.0318 | 0.1466 | 0.001302 | 1.19 |
| **2021** | **1.69** | 0.0764 | 0.0242 | 0.1435 | 0.001065 | 1.23 |
| **2022** | **1.54** | 0.0955 | 0.0483 | 0.1469 | 0.001300 | 1.24 |
| **2023** | **2.73** | 0.1409 | 0.0257 | 0.1451 | 0.001942 | 2.69 |

- **换手极稳**：10 年 0.1428–0.1516（σ 很小），无换手漂移 ⇒ 非「靠换手堆收益」。
- **PnL 全期 max drawdown = 0.0391**（@2023-02-02，由 2579 点原始序列重算），单季无 > 2× 均值的异常回撤。

---

## 3 判定

> **verdict = `PASS`**（含 2 条软标记，按 `worldquant-submit-alpha` 设属性时如实带上一行）

- Phase D 台账：`DEU::robustness_58gkLAkk` 已写入 `verdict=PASS`、`failed_checks=[]`、4 条 `soft_flags`、`checked_at=2026-10-06T22:25+08:00`。
- `PASS` 不改变 `submit_verdict` 判定（它只有否决权）。**本候选已具备提交条件，等用户明确确认。**
- **未提交任何 alpha。**

---

## 4 备注：同族第二候选 = CONDITIONAL（不推荐提交）

`akxENQE9`（仅最外层 `group_neutralize` → `group_rank`，其余同构）同样 `failed_ra_count = 0`，S1.60 / F1.17 / 2Y 2.04 / sub 1.30。
但稳健性与首选定档：

| 检查项 | `akxENQE9` | 判定 |
|---|---|---|
| Recent-3yr Sharpe | 2021/2022/2023 = **0.73 / 1.68 / 2.50**，均值 1.637 | PASS（均值 ≥1.58，平年 0） |
| Recent-3yr **CV_Sharpe** | **0.442** | **CONDITIONAL**（0.40–0.60） |
| 衰减比 | 1.572 | PASS |
| Recent-3yr **max/min** | **3.425** | **CONDITIONAL**（3–5） |
| 全历史 | 2017 年 sharpe **−0.17**（负年，非近 3 年） | 软标记，不 REJECT |

⇒ 台账 `DEU::robustness_akxENQE9 = CONDITIONAL`。
按 skill 定义，CONDITIONAL 的通道是 → `brain-alpha-repair` 修正后重审（≤2 轮），**不是**直接提交。
**结论：首选 `58gkLAkk`（PASS）；`akxENQE9` 作同族备份但先不提交。**
**同族铁律下一条腿只出 1 颗**；若要两颗都提交，须先测互相关（`compute_mutual_correlation`，本地不占平台槽）。
另 `akxENQE9` 的 prod 截至本报告时平台仍在计算（`max_correlation: null`）。

---

## 5 本次审计用到的工具（可复用）

- `C:\Users\MENGTAO\wqb-scripts\robustness_assess.py <alpha_id>` —— 一条命令产出本文第 2 节全部口径
  （年度表 / 最近 3 年四项 / CV / 衰减比 / max-min / 平年数 / PnL 重算最大回撤 / 相对池摘要）。

---

## 6 附：算子数能压到 10 以下吗？—— **不能，14 是下限**（W90–W92 实测）

平台回传 `operatorCount = 14`。做了 24 条压缩变体，**每减 1 个算子都要付一个闸**：

| 压缩动作 | ops | S | 2Y | 结果 |
|---|---:|---:|---:|---|
| （现役基准） | **14** | **1.75** | **2.07** | **0 FAIL** |
| 去掉 `subindustry` 层 | 13 | **1.50** | 2.20 | ✗ LOW_SHARPE |
| 再去掉一条图聚类轴 | 12 | 1.55 | 2.18 | ✗ LOW_SHARPE |
| 桶基准去掉 `ts_backfill` | 13 | 1.69 | **1.52** | ✗ LADDER |
| 桶基准去掉 `ts_mean` | 12 | 1.58 | 1.51 | ✗ LADDER + **CW** |
| 删掉双窗 `add(...)` | 9 | 0.51 | 0.79 | ✗ 崩 |
| 删掉 `ts_backfill` | 7 | 0.37 | 0.66 | ✗ 崩 |
| 用 `sta1_*` 现成 GROUP 轴替换 bucket 层（省 4 个算子） | 10 | 0.29–0.76 | 全负 | ✗ 崩 |

**算子预算账**：`4×group_neutralize`（3 轴 + 1 桶轴）＋`quantile`＋`add`＋`2×(ts_mean+ts_backfill)`＋`bucket`＋`rank`＋`ts_mean`＋`ts_backfill` = **14**。

### ⚠ 对通道选择的影响（重要）

**PPA 通道有「算子 ≤ 8」硬限**（Power Pool 规则）⇒ **`58gkLAkk` 不满足 PPA 条件，只能走 REGULAR 通道**
（REGULAR 下算子数仅 `>5` 的软标记，不构成 REJECT）。

### 顺带得到的机理结论

`pv29` 有 10 个**零拥挤**的 GROUP 字段（`sta1_top400/1200_c2/5/10/20/50`，coverage=1、0 users、0 alphas，粒度到 c50）
——当轴用**花 0 个算子**，但实测 **10/10 崩塌**。
⇒ **轴必须与信号的经济结构同源**：行业族 ✅、文本图关系 `oth455` ✅、信号自身慢分量分位 ✅、**统计风险聚类 ❌**。
