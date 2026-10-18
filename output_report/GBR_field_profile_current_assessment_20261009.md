# GBR 字段画像 · 当前完整状态 + 合理性评估

> 生成时间：2026-10-09（画像刚重建，**已并入全部 152 波 / 2,614 条实测**）
> 数据源：`field_profile_perf`（强度层，S 驱动）× `field_semantic_type`（语义层，description 驱动）

---

## 一、当前完整画像

### 1.1 verdict 分布（15,522 字段）

| verdict | 含义 | 字段数 | 占比 |
|---|---|---:|---:|
| `UNKNOWN_COVERAGE` | cov=0/NULL（未采集，待平台复核） | **7,477** | 48.2% |
| `UNUSABLE` | 真·低覆盖（0 < cov < 0.6） | 3,409 | 22.0% |
| `UNTESTED` | 覆盖合格、零测试 | 2,501 | 16.1% |
| `AXIS_ONLY` | GROUP 类型（只能作分组轴） | 1,390 | 9.0% |
| `DEAD` | 已测 S < 1.10 | 606 | 3.9% |
| **`ALIVE`** | 单信号 S ≥ 1.58 | **51** | 0.3% |
| `WEAK` | 1.10 ≤ S < 1.58 | **47** | 0.3% |
| `DEAD_STATIC` / `DEAD_TURNOVER` / `DEAD_COUNT` | 静态 / 高换手 / 计数型判死 | 29 / 7 / 5 | 0.3% |

**已测字段 745 ｜ 可探池（UNTESTED + UNKNOWN_COVERAGE）= 9,978 ｜ 实测转化率 51/745 = 6.8%**

### 1.2 verdict × category 矩阵

| category | UNKNOWN_COV | UNUSABLE | UNTESTED | AXIS | DEAD | **ALIVE** | **WEAK** | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MODEL | 2,278 | 1,754 | 1,079 | 0 | 177 | **29** | 15 | 5,335 |
| ANALYST | 1,082 | 630 | 369 | 0 | 126 | **17** | 13 | 2,239 |
| OTHER | 1,421 | 478 | 345 | 1,200 | 53 | **2** | 14 | 3,515 |
| PV | 1,304 | 86 | 499 | 190 | 82 | **3** | 0 | 2,165 |
| FUNDAMENTAL | 988 | 157 | 39 | 0 | 36 | 0 | 0 | 1,238 |
| NEWS | 276 | 3 | 153 | 0 | 52 | 0 | 1 | 491 |
| SENTIMENT | 0 | 258 | 5 | 0 | 11 | 0 | 2 | 276 |
| INSTITUTIONS | 24 | 13 | 0 | 0 | 19 | 0 | 2 | 66 |
| INSIDERS | 7 | 29 | 0 | 0 | 13 | 0 | 0 | 50 |
| 其余 7 类 | 97 | 1 | 12 | 0 | 37 | 0 | 0 | 147 |

**非 MODEL 的 ALIVE = 22**（ANALYST 17 + PV 3 + OTHER 2＝techindi）；**非 MODEL WEAK = 32**。

### 1.3 ALIVE 51 全表（按 S 降序，含语义与置信度）

**MODEL（29 个，塔已点亮＝锁定）**——最强 `model38.star_val_region_rank` S2.61/F2.31；`analyst_earnings_ibes.five_day_total_return_dlr2` S2.07/2Y2.31（n=95，全画像最密测试）。

**非 MODEL（22 个）**：

| dataset.field | 语义 | n | S | 2Y | F | 备注 |
|---|---|---:|---:|---:|---:|---|
| analyst47.anl47_rawsentiment | count | 60 | 1.96 | 1.84 | **0.97** | F 卡线 |
| analyst7.est_12m_pre_raisednum_4wks | count | 75 | 1.96 | 2.05 | 1.31 | prod 0.76–0.86 |
| **techindi_model.tm_16_..._r10_q2_p1** | percentile | **87** | **1.91** | **1.9** | **1.0** | ★ 本轮新出（见 §三注意 4） |
| analyst7.est_12m_pre_low | estimate_level | 133 | 1.90 | 2.72 | 1.38 | 2Y 全区最优 |
| analyst7.est_12m_pre_raised_1wk | count | 6 | 1.84 | 2.08 | 1.12 | |
| analyst7.est_12m_pre_raisednum_1mth | count | 1 | 1.82 | 1.68 | 1.15 | 低置信 n=1 |
| analyst7.est_12m_net_raisednum_4wks | count | 1 | 1.80 | 1.18 | 1.12 | 低置信 n=1 |
| analyst47.anl47_indicator | ratio | 20 | 1.78 | 1.53 | **0.76** | F 卡死 |
| analyst7.est_12m_net_raised_1wk | count | 1 | 1.77 | 1.18 | 1.05 | 低置信 n=1 |
| **techindi_model.tm_16_..._r10_q1** | unknown | 13 | 1.75 | 1.63 | 0.94 | ★ 本轮新出 |
| analyst7.est_12m_sal_raised_1wk | count | 1 | 1.74 | 1.43 | 0.98 | 低置信 n=1 |
| pv47.pv47_spret | unknown | 46 | 1.77 | 2.25 | 1.06 | prod 0.81 |
| analyst47.anl47_totalrawsignal | sentiment | 12 | 1.75 | 2.02 | **0.79** | F 卡死 |
| pv47.pv47_for_statssimple_only_spret | ratio | 5 | 1.73 | 2.12 | 1.12 | prod 0.81 |
| analyst7.est_12m_ebi_raisednum_4wks | count | 2 | 1.71 | **0.91** | 1.05 | 2Y 塌 |
| analyst9.anl9_s_numup | count | 25 | 1.69 | **1.19** | 1.19 | 2Y 卡 |
| analyst7.est_12m_ebt_raised_1wk | count | 2 | 1.68 | 1.88 | 0.97 | |
| analyst7.est_12m_pre_mean | estimate_level | 39 | 1.66 | 2.15 | 1.20 | |
| analyst_factor_signals.revenue_y1_estimate_change_3mo | revision_change | 17 | 1.62 | **0.76** | 1.02 | 2Y 塌 |
| analyst_factor_signals.revenue_revision_magnitude | ratio | 10 | 1.61 | **0.99** | 1.01 | 2Y 卡 |
| pattern_scores.breakaway_gap_up_mean_simscore_lookback60 | score | 1 | 1.61 | 1.64 | 1.13 | ⚠ 违规加权和产物 |
| analyst7.est_12m_net_low | estimate_level | 5 | 1.59 | 1.84 | 1.06 | |

### 1.4 WEAK top（接近闸线者）

`analyst_earnings_ibes.closing_price_dlr1` S1.57/2Y1.86 ｜ `lowest_price_dlr1` S1.57/2Y2.01 ｜ `vwap_dlr1` S1.56/2Y1.81（**level_amount，n=1~2，低置信但 2Y 健康**）｜ `model53.annualized_pd_1_year` S1.47/2Y1.86 ｜ `analyst7.est_12m_pre_median` S1.45/2Y2.03 ｜ `techindi r5_q1` S1.47/2Y1.69。

---

## 二、合理性评估：**七分合理，五分待改**

### ✅ 合理的部分（本次重建后确认）

1. **内部一致性通过**：verdict 合计 = 15,522 ✓；已测 745 = 51+47+606+29+7+5 ✓；2,614 实测行 / 152 波全部并入，无漏写。
2. **三处历史判据失真已修**：
   - `DEAD_COUNT` 改为 **description 驱动**（5 个全部是 description 确证 "Number of…" 的真计数）；
   - `UNUSABLE` 只保留真低覆盖（0<cov<0.6），`cov=0/NULL → UNKNOWN_COVERAGE` —— **这条修正直接解锁了 techindi_model 方向**（本轮唯一全闸候选的来源）；
   - genius 算子对账口径已固化（API 不暴露 level，须查 `operators_notes.md`）。
3. **与战役实测一致**：画像里 ALIVE 最高的非 MODEL 族（analyst7 count / pv47 / techindi percentile）正是战役实际产出候选的三条腿；判弱的 NEWS/FUNDAMENTAL/SENTIMENT 与 24+ 波探针的负结果一致。

### ⚠️ 不合理 / 待改的 5 处（按严重度排序）

**① DEAD 的判死置信度不足（最严重）**
606 个 DEAD 中 **69%（419 个）只测过 1 次**，且大多用同一套 house 骨架。**「单骨架单测判死」与 §十发现的 DEAD_TURNOVER 缺陷同源** —— 骨架错配会制造假 DEAD（techindi 若非 coverage 修正，其字段也会在别处被这样埋掉）。
⇒ 建议：DEAD 增加置信度列（n=1 标 `low_conf`），开波配额里允许低置信 DEAD 的抽检复活。

**② `best_s / best_f / best_2y` 是逐指标独立取 max，跨档位混合**
例：`techindi r10_q2_p1` 显示 S1.91 / F1.0 / 2Y1.9 —— 但这三个值来自**三个不同 alpha**（tvr0.40 波 / kqga9VK8 / tvr0.15 波），**没有任何单一表达式同时达到**。画像对「字段筛选」够用，但对「该字段最强单点」系统性高估。
⇒ 建议：增加 `best_joint` 列（单 alpha 同时最大化和差或全闸标记），或至少在报告侧注明。

**③ ALIVE 判据只看 S，不含 F / 2Y / prod**
当前 22 个非 MODEL ALIVE 里：4 个 F<1.0（anl47 全家）、3 个 2Y<1.58（afs×2、anl9、ebi）、1 个 best_2y 缺失。**ALIVE 是「强度筛选标签」不是「过闸标签」**，命名有误导性。
⇒ 建议：ALIVE 拆两档 —— `ALIVE_S`（S≥1.58）与 `ALIVE_GATE`（S+F+2Y 同过）。

**④ 4 个 ALIVE 的 `best_2y` 缺失**（全在 predictive_starmine）—— 数据完整性 bug：这些 alpha 的 2Y 未被正确回写。
⇒ 建议：回源 `backtest_results` 补齐，或在画像层用「任一实测行有 2Y」兜底。

**⑤ 语义层两处不稳**
- `pv47_spret` 此前分类为 `ratio`，本次重建后变 `unknown`；同族的 `tm_16_..._q2_p1` 是 `percentile` 而 `..._r10_q1` 是 `unknown` —— **同族字段语义标签不一致**，说明 description 文本在字段间不稳定，分类器对长代码名的描述依赖有噪声。
⇒ 建议：语义分类加「同族多数投票」平滑（同一命名族内取众数）。

### ⑥ 结构性天花板（非画像问题，但决定怎么用）

- **UNKNOWN_COVERAGE 7,477（48.2%）是画像最大的「未知」**：techindi 证明其中有真金，但也证明需要实测裁决 —— 画像层无法进一步收敛，只能靠「语义抽样扫测」逐区探。
- **已测池有选择偏差**：745 个已测字段是历史优选样本，其命中率（6.8%）**不能外推**未测池（§187 硬纪律）。
- **MODEL 占 ALIVE 的 57%（29/51）但塔已锁定** —— 非 MODEL 真实可用仅 22 个，其中还有 F/2Y 卡的，**实际可行动 < 15 个**。

---

## 三、结论

**画像作为「已测字段的强度台账」—— 现在是准的、可用的**（本次重建后无漏写、判据失真已修三处）。

**画像作为「未测字段的价值预测器」—— 不合理，且永远不可能合理**（选择偏差 + 骨架错配 + 覆盖信息缺失是结构性的），未测池只能靠抽样实测。

**落地优先级的 5 项改进**：① DEAD 加置信度列 ｜ ② best_* 加联合最优列 ｜ ③ ALIVE 拆 ALIVE_S / ALIVE_GATE ｜ ④ 补齐 4 个 ALIVE 的 2Y ｜ ⑤ 语义标签同族投票平滑。
