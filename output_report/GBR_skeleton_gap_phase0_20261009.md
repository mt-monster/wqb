# Phase 0 完成报告 · 审核点①：骨架缺口画像（GBR）

> 2026-10-09 ｜ 方案：`GBR_skeleton_diversity_plan_20261009.md` ｜ 本步零回测成本（纯本地计算）
> **本步只加列、不改任何 verdict 数值**（重建后 ALIVE 51 / WEAK 47 / DEAD 606 … 与之前完全一致 ✓）

---

## 一、加了什么

`field_profile_perf` 新增两列（幂等迁移，旧库平滑升级）：

| 列 | 含义 |
|---|---|
| `n_skeletons` | 该字段见过的**不同骨架模板数**（表达式模板归一：算子保留、字段→F、数字→N、分组名→G） |
| `skeleton_fams` | 见过的**骨架族集合**（14 族分类器，与 `skeleton_panel.PANEL` 对齐；含 gate/subtract/divide/ts_corr 等历史族） |

配套：`tools/fields/skeleton_panel.py gap-report --region GBR` 生成「应配 vs 已见 vs 缺口」视图。
治理：`audit_structure FAIL=0`、无下游位置解包该表（已查）。

---

## 二、★ 审核点①的核心数字

### 2.1 DEAD 系列置信度重分布

| verdict | 合计 | 高置信（见过≥2族） | **低置信（只见1族）** |
|---|---:|---:|---:|
| DEAD | 606 | 205 | **401（66%）** |
| DEAD_STATIC | 29 | 11 | 18（62%） |
| DEAD_TURNOVER | 7 | 0 | **7（100%）** |
| DEAD_COUNT | 5 | 4 | 1 |
| **合计** | **647** | **220** | **427（66%）** |

**⇒ 427 个「死」字段其实只是「一种骨架下没成」。按新纪律，它们全部降为低置信，进入复活候选池。**

### 2.2 ★ 应配骨架覆盖率（最刺眼的一个数）

```
已测字段 745 个：
  优选骨架族【全覆盖】=   9 个（1%）
  优选骨架族【有缺口】= 736 个（99%）
```

**即：连 ALIVE 字段也几乎都没试过它画像应配的全部骨架族。**

### 2.3 样本（字段 → 语义 → 应配 → 已见 → 缺口）

**analyst7**（count 语义应配 `gn_first/level_rank/delta`）：
- `est_12m_net_raisednum_4wks`（ALIVE S1.80）：已见 `subtract`｜**缺口 gn_first/level_rank/delta 全缺**
- `est_12m_net_low`（ALIVE S1.59）：已见 delta/level_rank/ts_rank｜缺口 ts_zscore

**techindi_model**：
- `tm_16_..._r10_q2_p1`（ALIVE S1.91，87 次测试）：见过 13 族 ⇒ **缺口「无」**（全区唯一族全覆盖的字段之一）
- `tm_15_..._r10_q1`（**DEAD** S0.95）：已见 `level_rank`｜**缺口 delta/ts_rank** ← 典型疑似假死
- `tm_15_..._r10_q2`（**DEAD** S1.02）：已见 level_rank/subtract｜缺口 decay_linear/gn_first

**pattern_scores**（score 语义应配 `level_rank/ts_rank/quantile`）：
- `asc_triangle_mean_simscore_lookback120`（DEAD S0.17）：已见 `other`｜**优选族三族全没试过**

**pv47**：`pv47_spret`（ALIVE S1.77，见过 7 族）仍缺 delta/ts_rank。

---

## 三、本步结论与待你裁决

1. **「同一套骨架打所有字段」的偏差比预想更大**：不只 64% 字段单骨架，而是 **99% 字段连它画像应配的优选族都没试全**。
2. **ALIVE 也未能豁免** —— 说明现有 51 个 ALIVE 的 S 可能是**下界**而非上界（还有未试的适配骨架可能更强）。
3. **427 个低置信 DEAD + 736 个有缺口字段** = Phase 3 复活补测的候选池。

**🔍 审核点①请你确认**：
- ① 这两列与「应配/已见/缺口」口径是否认可；
- ② 若无异议，下一审核点是 **审核点②：`SEM_PREFERRED` 映射表**（方案文档 §二，10 族 × 10 语义的配对规则）—— 它直接决定 Phase 3 给每个字段配什么骨架。

待你确认后进入 Phase 1 审核。
