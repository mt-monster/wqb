# GBR · PV 类别字段画像（锁定专章）

> 区域：**GBR / EQUITY / D1 / TOP700**　｜　类别：**PV**　｜　快照：2026-10-08
> 数据来源：`field_profile_perf`（强度层）＋ `field_semantic_type`（语义层）

---

## 一、PV 类别总览

```
数据集 18 个 ｜ 字段 2,165（占全区 13.9%）｜ 数据集 alphaCount 合计 1,182
ALIVE 3  ｜ WEAK 0 ｜ UNTESTED 511 ｜ DEAD 49 ｜ UNUSABLE 1,412 ｜ AXIS_ONLY 190

USABLE 池（ALIVE+WEAK）= 3
其中「合规」ALIVE 仅 2 个（见 §4）
```

**PV 是「高度极化」的类别**：65% 的字段（1,412/2,165）因 **coverage < 0.6** 直接不可用，
而可行动池只剩 **3 个 ALIVE** —— 是全区 16 个 category 中**极化最严重**的一个。

---

## 二、数据集级画像（18 个，按字段数降序）

| dataset | data_type | 字段 | **ALIVE** | WEAK | UNTESTED | DEAD | UNUSABLE | AXIS | aCnt |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **intraday_pv_feats** | MATRIX | 585 | 0 | 0 | 0 | 17 | **568** | 0 | 175 |
| **pattern_scores** | MATRIX | 504 | **1** | 0 | **471** | 32 | 0 | 0 | 480 |
| pv20 | — | 300 | 0 | 0 | 0 | 0 | **300** | 0 | 0 |
| continuation_score | — | 300 | 0 | 0 | 0 | 0 | **300** | 0 | 162 |
| pv30 | GROUP | 240 | 0 | 0 | 0 | 0 | 60 | **180** | 125 |
| pv173 | — | 81 | 0 | 0 | 0 | 0 | 81 | 0 | 0 |
| **pv29** | MATRIX | 50 | 0 | 0 | **40** | 0 | 0 | 10 | 23 |
| pv13 | — | 28 | 0 | 0 | 0 | 0 | 28 | 0 | 15 |
| pv109 | VECTOR | 26 | 0 | 0 | 0 | 0 | 26 | 0 | 18 |
| pv1 | — | 23 | 0 | 0 | 0 | 0 | 23 | 0 | 108 |
| pv71 / pv106 / pv103 | — | 8 各 | 0 | 0 | 0 | 0 | 8 各 | 0 | 3/19/37 |
| **pv47** | MATRIX | **2** | **2** | 0 | 0 | 0 | 0 | 0 | 7 |
| pv17 / pv113 | — | 1 各 | 0 | 0 | 0 | 0 | 1 各 | 0 | 1/1 |
| univ1 / chart_return_model | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/8 |
| **【合计】** | | **2,165** | **3** | **0** | **511** | **49** | **1,412** | **190** | |

**三条读数**：
1. **`intraday_pv_feats`（585 字段）中 568 个不可用** —— 高频/日内字段在 **D1 延迟**下 coverage 不足，**结构性不可用**（非未测）。
2. **`pattern_scores`（504）是 PV 唯一的未测矿**（471 未测），但见 §5。
3. **`pv47` 只有 2 个字段，却 2 个全是 ALIVE** —— 全区效率最高的数据集（aCnt 仅 7，**竞争极低**）。

---

## 三、语义类型 × verdict 矩阵

| sem_type | ALIVE | WEAK | UNTESTED | DEAD | UNUSABLE | AXIS_ONLY |
|---|---:|---:|---:|---:|---:|---:|
| **score** | **1** | 0 | **329** | 30 | 275 | 40 |
| **dispersion** | 0 | 0 | **71** | 1 | 101 | 0 |
| **percentile** | 0 | 0 | **71** | 1 | 45 | 0 |
| cluster_label | 0 | 0 | 35 | 0 | 0 | 30 |
| ratio | 1 | 0 | 0 | 5 | 144 | 0 |
| unknown | 1 | 0 | 5 | 1 | 392 | 120 |
| level_amount | 0 | 0 | 0 | 3 | 215 | 0 |
| correlation | 0 | 0 | 0 | 4 | 103 | 0 |
| revision_change | 0 | 0 | 0 | 3 | 91 | 0 |
| count / identifier / temporal_meta / estimate_level / novelty_time | 0 | 0 | 0 | 0 | 10/14/1/18/3 | 0 |

**读数**：**未测池 511 中 471 集中在 `score`(329) + `dispersion`(71) + `percentile`(71)** —— 全部来自 `pattern_scores`；
余 40 在 `pv29` 且是 `cluster_label`（只能作轴）。

---

## 四、ALIVE / DEAD 明细

### 4.1 PV 的 3 个 ALIVE

| dataset.field | sem_type | n_tests | S | 2Y | F | 合规性 |
|---|---|---:|---:|---:|---:|---|
| **`pv47.pv47_spret`** | unknown（实为**比率**：风险模型特异日收益） | **46** | **1.77** | **2.25** | 1.06 | ✅ 合规 |
| **`pv47.pv47_for_statssimple_only_spret`** | ratio | 5 | **1.73** | **2.12** | 1.12 | ✅ 合规 |
| `pattern_scores.breakaway_gap_up_mean_simscore_lookback60` | score | 1 | 1.61 | 1.64 | 1.13 | ❌ **违规** |

> **★ 关键修正**：`pattern_scores` 的这 1 个 ALIVE **来自加权和组合**
> （实测表达式 = `0.4*(-rank(breakaway_gap_up_mean_simscore_lookback60)) + 0.3*rank(cont_rising_wedge_median_...) + 0.3*rank(v_shape_continuation_top_m...)`），
> **属「多条独立信号腿相加」⇒ 明令禁止（禁混信号）**。
> **⇒ PV 的合规 ALIVE 实际只有 2 个，且全部来自 `pv47`。**

### 4.2 PV 的 DEAD（49 个，节选 —— 揭示已试机制的强度上限）

| dataset | 字段（族） | sem_type | S | 2Y |
|---|---|---|---:|---:|
| intraday_pv_feats | `mean_bid_ask_size_ratio_30m_pre_close` | ratio | **0.94** | 1.25 |
| **pattern_scores** | `avg_similarity_falling_wedge_pattern` | score | **0.92** | 1.00 |
| pattern_scores | `symmetry_triangle_upward_max_similarity` | score | 0.87 | 0.20 |
| intraday_pv_feats | `corr_vwap_with_volume` | correlation | 0.85 | 0.72 |
| intraday_pv_feats | `corr_last_trade_price_with_volume` | correlation | 0.79 | 0.86 |
| pattern_scores | `avg_similarity_downward_symmetrical_triangle` | score | 0.76 | 0.03 |
| pattern_scores | `avg_similarity_rising_wedge_pattern` | score | 0.75 | 0.12 |
| pattern_scores | `mean_similarity_reversal_v_top` | score | 0.74 | 0.60 |
| pattern_scores | `max_similarity_upward_symmetrical_triangle` | score | 0.73 | −0.16 |
| pattern_scores | `breakaway_gap_down_mean_simscore` | score | 0.62 | 0.40 |
| intraday_pv_feats | `mean_ask_price_30m_post_open` | level_amount | 0.41 | 0.18 |

**⇒ `pattern_scores` 已试 33 个字段（累计 42 次测试），最强只有 S0.92（且 2Y 1.00）** —— **机制级证据：形态相似度在本区偏弱。**

---

## 五、★ 未测池结构：471 个是「一个机制的参数网格」

`pattern_scores` 未测 471 的**结构解剖**：

**形态族（前缀）× 聚合方式 × 窗口** 的笛卡尔积 ——

| 维度 | 取值 | 计数 |
|---|---|---|
| **形态** | asc_triangle / symm_triangle / desc_triangle / v_shape / reversal_v / trendline_convergence / trendline_divergence / breakaway_gap_up/down / common_gap / falling_wedge / rising_wedge / upward_gap … | 20+ 种 |
| **聚合** | mean 20 ｜ min 38 ｜ max 37 ｜ median 36 ｜ std / stddev 45 ｜ quantile95 40 ｜ dynamic 41 ｜ adaptive 2 ｜ avg 9 | 9 类 |
| **窗口** | `lookback60` 37 ｜ `lookback120` 48 ｜ `_40d` 21 ｜ 无标注 288 | 3+ 档 |

**⇒ 471 个未测 ≈ 同一机制（K线形态相似度）在不同「形态 × 聚合 × 窗口」上的组合，不是 471 个独立机会。**

这与本仓库已固化的反模式纪律一致：
> **「同结构换字段 = 复制品」／「批量同模板挖矿 = 互相复制品」** —— 421 个组合大概率互为近亲。

**叠加语义层的实测结论**：`score` 语义在 GBR 的**实测产出率是全部 17 类中最低之一**（62 条抽样扫测中 `score` 中位 S = −0.05，命中率 1.3%）。

**⇒ PV 未测池的双重判负**：
- **机制层**：形态相似度已试 33 个，上限 S0.92（2Y 仅 1.00）；
- **语义层**：`score` 是本区实测产出率最低的语义之一；
- **结构层**：471 个是单机制参数网格，扩样只会生产复制品。

**余下的 40 个（`pv29`）是 `cluster_label`** —— 平台实测**不是 GROUP 单位**（`group_rank(x, 它)` 会整批报 `Unit[]`），
**只能经 `bucket(rank(F), range="0,1,0.05")` 包装后作分组轴**，不可作信号。

---

## 六、PV 的既有战役结论（实测）

| 项 | 结论 |
|---|---|
| **主力机制** | `pv47`（UBER 风险模型的**个股特异日收益**）→ **短期反转**：`-ts_decay_linear(rank(ts_quantile(ts_sum(pv47_spret,22),252)), d)` |
| **候选产出** | 本战役共产 **10 颗 IS 全闸候选**（`LLZ5ewlM` 1.73/1.12/2.12 为最优） |
| **prod 实测** | **0.804–0.815**（`LLZ5ewlM` 0.8148 ｜ `akxVZdN6` 0.8137 ｜ `wpb96AJp` 0.8041）⇒ **全部 > 0.70 被挡** |
| **同质性** | 10 颗**同属一条腿**（仅 decay 档/字段/窗不同）⇒ 按「一条腿只产 1 颗」，可提交 ≈1–2 颗 |
| **降 prod 杠杆** | 换 universe ❌（GBR 只有 TOP700）｜换分组轴 ❌（`pv29` 聚类轴 S 0.07–0.16 信号崩）｜换字段 ⚠️ 同腿无效 |

---

## 七、PV 画像结论与建议

### 7.1 结论（三条）
1. **PV 的合规可用字段只有 2 个，且全部来自 `pv47`** —— 那 1 个 `pattern_scores` ALIVE 是**违规加权和**，不可用。
2. **PV 已挖尽**：`pv47` 仅 2 字段（0 未测）；`pattern_scores` 471 未测是**单机制参数网格**且机制已证明偏弱；
   `pv29` 40 未测是**不可作信号的聚类标签**；`intraday_pv_feats` 568 字段在 D1 下**结构性不可用**。
3. **PV 的产出上限被 prod 封住**：`pv47` 腿 10 颗 IS 全闸候选 prod 全部 0.80–0.82。

### 7.2 建议
| 优先 | 动作 | 理由 |
|---|---|---|
| **1** | **不投入** | PV 已挖尽 + prod 饱和；`pattern_scores` 扩样只会生产复制品（471 个单机制组合） |
| 2 | 若必须投 1 波：只在 `pattern_scores` 的 **`dispersion`(71) + `percentile`(71)** 语义上试 | 这两个语义在本区实测产出率高于 `score`，且**与已试的 mean/min/max 聚合不同**（分散度 ≠ 水平） |
| 3 | `pv29` 的 40 个聚类标签**改作分组轴**（`bucket` 包装）配 `pv47` 信号 | 唯一「改持仓」类杠杆（但实测该轴使 S 由 1.68 降到 1.57，仍判负） |

### 7.3 一句话总结
> **PV = 「一条好腿（`pv47`）+ 一片无效的参数网格（`pattern_scores` 471）+ 一堆结构不可用（`intraday_pv_feats` 568）」。
> 好腿已被 prod 封住，参数网格只会产复制品 ⇒ PV 在 GBR 应判定为「已收口」。**


---

## 八、补充执行：`pattern_scores` 的 dispersion + percentile 探针（Wave，2026-10-09）

### 8.1 动机
§七 曾建议：`pattern_scores` 的 **`dispersion`(71) + `percentile`(71)** 这两个语义在本区实测产出率高于 `score`，
且**与已试的 mean/min/max 是不同性质**（分散度 ≠ 水平）⇒ 值得 1 波。

### 8.2 执行与结果（8 条，正/反交替以同时获取方向信息）

| 语义 | 字段 | 骨架 | S | 2Y |
|---|---|---|---:|---:|
| dispersion | `asc_triangle_down_std_simscore_lookback120` | `divide(x, ts_mean(x,252))` | −0.20 | −0.06 |
| dispersion | `breakaway_gap_up_std_simscore_lookback60` | 同上 | +0.21 | 0.57 |
| dispersion | `cont_falling_wedge_std_simscore_lookback120` | 同上 | −0.24 | −0.33 |
| dispersion | `desc_triangle_std_simscore_lookback60` | 同上 | +0.07 | 0.96 |
| percentile | `breakaway_gap_down_q95_simscore_lookback60` | 直用 | +0.25 | 1.01 |
| percentile | `common_gap_down_q95_simscore_lookback120` | 直用 | +0.12 | 0.89 |
| percentile | `cont_v_top_q95_simscore_lookback120` | 直用 | +0.20 | −0.10 |
| percentile | `continuation_downward_wedge_quantile95_similarity` | 直用 | +0.01 | 1.01 |

**⇒ 全部 |S| ≤ 0.25**；正/反交替的两组强度对称（无方向边际）。

### 8.3 结论：**PV「已收口」现在有三层独立证据**

| 层 | 证据 |
|---|---|
| **机制层** | 形态相似度已试 33 字段（42 次测试），最强合规 S **0.92**（2Y 仅 1.00） |
| **语义层** | `score` 是本区实测产出率最低的语义之一（中位 S −0.05、命中率 1.3%） |
| **语义切换层（本次）** | 换成 `dispersion`（比率化骨架）/ `percentile`（直用骨架）后，**|S| ≤ 0.25** |

**⇒ §七 中「若必须投 1 波」的建议已被执行并判负。PV 在 GBR 无剩余可行动空间。**
