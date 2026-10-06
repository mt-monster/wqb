# DEU · 最终态势：两颗「只差一闸」的成品级候选（2026-10-06）

> 设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 ｜ **57 波 ~380 条探针** ｜ **全部 UNSUBMITTED**

## 一、★★★★★ 全场最佳：`RR61Rz7b`（唯一「相关性双闸 + 除 2Y 外全 RA + 双 ×1.8 塔」）

```python
group_neutralize(
    signed_power( ts_mean( ts_backfill(mean_estimate_change_pct_f12m_earnings_14d_4, 1008), 8), 0.3 ),
    oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20 )
```

| 闸 | 值 | 限 | 结果 |
|---|---:|---:|---|
| **PROD_CORRELATION** | **0.5698** | 0.7 | ✅ **PASS**（直方图 [0.5,0.6) 仅 7 个） |
| **SELF_CORRELATION** | **0.5697** | 0.7 | ✅ **PASS** |
| LOW_SHARPE | **1.60** | 1.58 | ✅ |
| LOW_FITNESS | **1.12** | 1.0 | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | **1.12** | — | ✅ |
| CONCENTRATED_WEIGHT / CLUSTER_TEST | — | — | ✅ |
| **IS_LADDER_SHARPE（2Y）** | **1.21** | **1.58** | ❌ **唯一失败** |
| `pyramids` | `DEU/D1/MODEL ×1.8` + `DEU/D1/OTHER ×1.8` | | **双塔** |

**这是 57 波以来唯一一颗把「prod / self / S / F / sub / CW」六项凑齐的 alpha，且同时点亮两条 ×1.8 塔。**

## 二、第二颗：`ZYAKPvb0`（2Y 只差 0.02，但 prod 差 0.21）

```python
group_neutralize(group_neutralize(
    ts_mean(ts_backfill(value_momentum_sector_percentile, 252), 15),
    oth455_relation_n2v_p10_q50_w1_pca_fact1_cluster_10),
    oth455_relation_n2v_p10_q200_w1_pca_fact3_cluster_20)
```

| 闸 | 值 | 结果 |
|---|---:|---|
| LOW_SHARPE / LOW_FITNESS | 1.78 / 1.77 | ✅ |
| LOW_SUB_UNIVERSE_SHARPE | 0.86 | ✅ |
| CONCENTRATED_WEIGHT | — | ✅ |
| **IS_LADDER_SHARPE（2Y）** | **1.56** | ❌ **差 0.02** |
| **PROD_CORRELATION** | **0.9102** | ❌ 差 0.21 |

## 三、★ 本轮最大方法论产出：三类组件的"正交叠加"配方

**`starmine 字段（prod 天生 0.57）` × `signed_power(·, 0.3)` × `图聚类轴`**

| 组件 | 作用 | 量化 |
|---|---|---|
| starmine 估计修正字段 | 决定 **prod 干净** | prod 0.578~0.570 ✅ |
| `signed_power(x, 0.3)` | 抬 2Y（输出端） | starmine 2Y 1.03 → 1.24 |
| **图聚类轴**（`oth455_*_cluster_*`，1200 个 GROUP 键） | **把 sub 从 0.62 抬到 1.12** + 降 prod | sub +0.50 |
| `ts_backfill(x, 66~1008)` | 修 CW（状态量字段有效） | CW ✅ |

## 四、本区已量化的四个「跷跷板」（这是无法闭环的根本原因）

| 跷跷板 | 一端 | 另一端 |
|---|---|---|
| 平滑窗 `ts_mean(x,W)` | W 大 → 2Y 高（1.40→1.56） | W 大 → S 低 |
| 主体变体 | `industry` → S/sub 最高（1.84/0.91） | `sector` → 2Y 最高（1.56） |
| 中性化档 | SUBINDUSTRY → S/sub 最优 | CROWDING/REVERSION → 2Y ≥1.58 但 sub 崩 |
| **图聚类轴** | **prod −0.06、sub +0.50** | **2Y −0.25** |

⇒ **本区单信号无法用任何单一设置同时满足 sub 与 2Y。**

## 五、下一步（若要继续）

1. **`RR61Rz7b` 补 2Y**：唯一缺口 2Y 1.21→1.58。已知 `predicted_surprise_f12m_ebitda_4` + 同轴 = **2Y 2.04**（S 0.83）；
   starmine 族内 S↔2Y 跷跷板已证实，故需**族外 2Y 载体**（但受禁混信号约束）；
2. **`ZYAKPvb0` 补 prod**：唯一缺口 prod 0.91→0.70；图聚类轴已用尽，剩 `oth455` 其余 1190 键的三重嵌套/组合。
