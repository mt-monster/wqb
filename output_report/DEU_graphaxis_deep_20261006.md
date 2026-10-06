# DEU · 图聚类分组轴深度攻坚（2026-10-06 续 2）

> 设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 ｜ W49–W50（累计 50 波 ~350 条）｜**全部 UNSUBMITTED**

## 一、核心结果：首次出现「除 ladder 外全 RA 闸通过 + 双 ×1.8 塔」的 alpha

```
group_neutralize( ts_mean( ts_backfill(value_momentum_sector_percentile, 66), 5 ),
                  oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20 )
```
**alpha_id `9qWrmqd1`**

| 闸 | 值 | 限 | 结果 |
|---|---:|---:|---|
| Sharpe | **1.81** | 1.58 | ✅ |
| Fitness | **1.82** | 1.0 | ✅ |
| turnover | 0.076 | 0.7 | ✅ |
| CONCENTRATED_WEIGHT | — | — | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | **0.86** | 0.86 | ✅ |
| CLUSTER_TEST | — | — | ✅ |
| **IS_LADDER_SHARPE（2Y）** | **1.37** | **1.58** | ❌ **唯一失败** |
| `fail[]` / `failed_ppa_count` | 空 / 0 | | |
| **塔** | **DEU/D1/MODEL ×1.8 + DEU/D1/OTHER ×1.8** | | 双塔 |
| **prod** | **0.9056** | 0.7 | ❌ |

## 二、完整扫描结果（W49–W50，轴 = `oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20`）

| alpha | 主体 × 包装 | S | F | tvr | 2Y | sub | CW | prod |
|---|---|---:|---:|---:|---:|---:|---|---:|
| **9qWrmqd1** | `vm_sector_pct` × `ts_mean∘ts_backfill` | 1.81 | 1.82 | 0.076 | 1.37 | **0.86✅** | ✅ | **0.906** |
| **gJZMdJXK** | `vm_sector_pct` × `group_rank∘ts_backfill` | **1.89** | **1.92** | 0.122 | 1.41 | 0.88(限0.90) | ✅ | — |
| **e7Q0v7VO** | `vm_industry_pct` × `group_neutralize` | 1.83 | 1.82 | 0.107 | **1.44** | 0.88✅ | ❌ | — |
| leKl9eMe | `winsorize(group_rank(vm,‹轴›),4)` | **1.89** | **1.92** | 0.123 | 1.43 | 0.88❌ | ❌ | — |
| leKlGrM7 | `group_neutralize(vm_sector_pct, ‹轴›)` | 1.82 | 1.84 | 0.098 | 1.35 | 0.85 | ❌ | **0.893** |
| LLZ1rLEL | `winsorize(group_neutralize(…),4)` | 1.82 | 1.84 | 0.098 | 1.35 | 0.85 | ❌ | — |
| npP2Qpea | `vm_global_pct` × `group_neutralize` | 1.66 | 1.63 | 0.095 | 1.32 | 0.82✅ | ❌ | — |
| 0mrE6mx8 | `signed_power(group_neutralize(…),0.5)` | 1.76 | 1.72 | 0.098 | 1.31 | 0.75 | ❌ | — |
| （W47 基线） | `group_neutralize(vm_sector_pct, ‹cluster_20›)` | 1.67 | 1.61 | 0.097 | 1.41 | 0.70 | ❌ | 0.896 |

## 三、三条结论

1. **`ts_backfill + ts_mean` 与图聚类轴联用，同时修好 CW 与 sub**：
   轴单独版是 `CW ❌ / sub 0.70`；叠加后变成 `CW ✅ / sub 0.86 ✅` —— **这是第一个把「CW + sub + S + F」四闸一次凑齐的结构**。
2. **轴是有效旋钮**（同样本 signal）：
   - 主成分：`pca_fact3` > `fact1` ≈ `fact2`
   - 粒度：`cluster_5/10/20` 相近（20 的 sub 最高）
   - 主体变体：`industry_percentile` 的 2Y 最高（1.44）、`sector_percentile` 的 sub 最高（0.86）
3. **★ prod 有平台**：裸 `rank(vm_sector)` = **0.9653** → 任意图聚类轴 ≈ **0.893~0.906**。
   **−0.06~0.07 之后就卡住了**，单靠换轴到不了 0.7。要破墙需**第二个正交杠杆叠加**。

## 五、W51–W52：两道缺口都攻不动，且新增第四个跷跷板

### W51：2Y 载体叠加失败；`pv29` 不能当轴

- 长 backfill（66/252/504/1008）× 平滑窗（5/10）× 主体（sector/industry）全试 ⇒ **2Y 卡在 1.33~1.44**，
  所有变体仍**只挂 `IS_LADDER_SHARPE`**（`fail[]` 空、`failed_ppa_count=0`）。
  最佳：`akxn8zlR`（bf66,W10）S1.80/F1.81/2Y**1.41**/sub0.85✅/CW✅。
- **`pv29` 的 50 个 `industry_grouping_*` 不能当分组轴**：验证批 **2/2 ERROR**
  ⇒ 它们是 **MATRIX 型**（非 GROUP 型），平台拒绝作 group 参数。**只有 GROUP 型字段（oth455 的 1200 个聚类键）能当轴。**

### W52：中性化档 = 「S/sub ↔ 2Y」跷跷板（第四个已量化权衡）

| 中性化 | S | F | 2Y | sub(限) | CW | 判定 |
|---|---:|---:|---:|---|---|---|
| **SUBINDUSTRY** | 1.77 | 1.77 | **1.66 ✅** | **0.86 ✅** | ✅ | **全 RA 通过**（仅 prod 挂） |
| CROWDING | 1.51 | 1.30 | **1.61 ✅** | 0.59 ❌(0.72) | ❌ | 2Y 过、sub 崩 |
| REVERSION_AND_MOMENTUM | 1.40 | 1.15 | **1.64 ✅** | 0.50 ❌(0.66) | ❌ | 2Y 过、sub 崩 |
| SLOW_AND_FAST | 1.20 | 0.67 | 0.63 ❌ | **1.06 ✅** | ❌ | sub 过、S/2Y 崩 |

⇒ **本区无法用单一设置同时满足 sub 与 2Y**（与前三个跷跷板同型：平滑↔2Y、S↔2Y、图轴 prod↔2Y）。

## 六、总账（51 波 ~360 条，零提交）

| 资产 | 关键表达式 | S | F | 2Y | sub | CW | prod | 缺口 |
|---|---|---:|---:|---:|---:|---|---:|---|
| **`pw56XLRV`** | `rank(ts_backfill(value_momentum_sector_percentile,66))` | 1.77 | 1.77 | **1.66✅** | ✅ | ✅ | 0.965❌ | **仅 prod** |
| `qM0lpGvA`/`akxn8zlR` | `group_neutralize(ts_mean(ts_backfill(…,66~252),5~10), ‹图聚类轴›)` | 1.80 | 1.81 | 1.37~1.41 | ✅ | ✅ | ~0.90 | 2Y + prod |
| `gJZMdJXK` | `group_rank(ts_backfill(vm,66), ‹轴›)` | **1.89** | **1.92** | 1.41 | 0.88 | ✅ | — | sub+2Y |
| `wpbRqwp5` | starmine `signed_power(ts_mean(ts_backfill(…,1008),8),0.3)` | 1.67 | 1.26 | 1.22 | ✅ | ✅ | **0.578✅** | **仅 2Y** |

**结论**：图聚类轴是**真实但不足**的 prod 杠杆（−0.06），且以 2Y 为代价；两条路（值动量 prod-first / starmine 2Y-first）各自只剩一个缺口，但**都还没打通**。

