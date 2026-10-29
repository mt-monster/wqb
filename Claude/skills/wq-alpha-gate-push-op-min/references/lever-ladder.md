# 杠杆阶梯（按实测效果排序）

> 数据出处：2026-10-10~12 DEU 战役（analyst93 / fundamental6 / institutions1 / shortinterest3 四条腿，~80 批仿真）。
> **跨区/跨数据集迁移前必须逐字段族实测**——本表是「排序参考」，不是普适定律。

---

## L1 分组轴 → `sector`（平台内置）

**增益：S +0.26 ~ +0.29**，同时**改变 2Y 检查类型**。

| 腿 | 构造 | 数据集 GROUP 轴 | **`sector` 轴** |
|---|---|---|---|
| fundamental6 | `ts_delta(ROE,252)` | S 1.04 / 2Y 1.17 | **S 1.33 / fit 0.91 / 2Y 1.54** |
| analyst93 | `multiply(corrrev, recprof2)` | S 1.05 / 2Y 0.71 | **S 1.31 / fit 0.93** |
| shortinterest3 | `TC×DUR` | — | S 1.54~1.59（最优轴） |
| **institutions1** | 掩码 `ts_sum` | S 1.34 | **S 0.34（反向失效）** |

**机制**：平台内置档轴（`sector`/`industry`/`subindustry`）触发 **`LOW_2Y_SHARPE`**（宽）；
数据集 GROUP 字段轴（`oth455_*`/`pv30_*`/`sta1_*`）触发 **`IS_LADDER_SHARPE`**（严，显示 1.58 仍可能 FAIL）。
⇒ **同一个 2Y 数值，在内置轴上可能过、在 GROUP 轴上不过。**

**代价**：内置轴点亮塔数减少（GROUP 轴常顺带点亮 OTHER ×1.8；内置轴只点亮本类）。
⚠ **但塔数不影响 RA 通过**（RA 只看 `is.checks`）⇒ 不必为塔牺牲 S。

**轴全清单**：`sector` / `industry` / `subindustry` / `market`（=全局单组）；数据集 GROUP 字段经 `get_datafields(type='GROUP')` 取。
实测排序（fundamental6 类）：`sector` > `industry` > `subindustry`；`market`（全局）在部分腿接近 sector。

---

## L2 双窗级联 `multiply(rank(ts_delta(x,a)), rank(ts_delta(x,b)))`

**增益：S +0.18、2Y +0.6**（同时！）——本战役最强单步。

| 构造 | S | fit | 2Y |
|---|---|---|---|
| 单腿 `ts_delta(OIADP,252)` | 1.38 | 0.97 | 1.30 |
| **级联 (240,176)** | **1.56** | **1.15** | **1.91** |
| 级联 (252,132) | 1.45 | 1.04 | 1.64 |
| 级联 (252,88) | 1.41 | 0.96 | — |
| 级联 (264,132) | 1.43 | 1.02 | 1.59 |

**窗是尖峰**：长窗 252→240 (+0.01 S)、→236 (−0.02)、→264 (−0.05)；短窗 176 最优（→168/184 都掉）。
**必须做窗网格**（长窗 × 短窗各 ≥5 档），不要只测一两个点。

**语义**：同一比率在「年度尺度变化」与「半年尺度变化」上的一致方向 ⇒ 动量确认。

**注意**：级联对**比率**有效；对**水平量**（如 ROE 水平的双窗）效果弱。

---

## L3 `ts_target_tvr_decay(x, target_tvr=t)`

**增益：S +0.03、TO ↓、fit ↑**（memory 记的「三赢」杠杆）。

| 构造 | S | fit | TO |
|---|---|---|---|
| 级联(240,176) 无限速器 | 1.56 | 1.15 | 0.1332 |
| **+ `ts_target_tvr_decay(target_tvr=0.05)`** | **1.59** | **1.20** | 0.1309 |

**★★ 激活条件：`TO > target_tvr` 才生效**；`TO < target` 时是 **no-op**（两次独立对照证实）。
⇒ **用法**：先测出构造的 TO，把 `target_tvr` 设在 TO 的 **40%~60%** 处（如 TO=0.133 ⇒ t=0.05~0.08）。
⇒ TO 已在 0.05 以下的构造上此杠杆无效。

**为什么是「临门一脚」的优选**：它**不增加算子数超过 1 个**（相当于用 1 个算子替代
`ts_decay_linear` + `hump` 两个），且同时改善 3 个指标 ⇒ 对「指标 + 算子数」双目标都友好。

---

## L4 `winsorize(x, std=3~4)`

**增益：S +0.02、fit +0.03**（截面缩尾）。

- `std` 扫描（1/2/3/4/5/6/8/10）：**≥3 饱和**（3~10 指标逐位接近）；**std=1 崩塌**（S 0.55）。
- **★ 它是唯一「同向改善」的截面杠杆**：因为缩尾**只压极端值、不改信号的时间结构**。
- 对比：**时间平滑类**（`ts_decay_linear`/`hump`）在累积型信号上**零和**（降 TO 同时削 alpha）。
- 建议默认 `std=4`（安全区中部）。

---

## L5 `decay`（设置层）

**主要作用：提 fitness**。因为 `fitness = sharpe × sqrt(return / max(tvr, 0.125))`
⇒ **TO 从 0.14 压到 0.125 可让 fit ×1.06**。

实测（fundamental6 级联）：decay 3 → S1.57/fit1.15；4 → 1.56/1.15；5 → 1.55/1.15；6 → 1.55/1.15；8 → 1.54/1.15；12 → 1.46/1.07。
⇒ **decay 3~8 是平台期**，取 4（或 3）。**decay 不是越高越好**（快信号上高 decay 是反的）。

---

## L6 `multiply(rank(A), rank(B))` 两腿联合

**增益：S +0.11**，但**逐 category 实测**（**非普适**）：

| category | 效果 |
|---|---|
| analyst93 | 0.94 → **1.05**（且 PPA 由 FAIL 转全过）✔ |
| shortinterest3 | 提 S 的 decisive 通道 ✔ |
| **fundamental6** | 0.82 → **0.50（反向失效）** ✘ |

⇒ 联合前先做 1~2 条对照探针，不要默认有效。

---

## 禁用杠杆（已证否，别再投）

| 禁用 | 实测现象 |
|---|---|
| 换 `neutralization` 档 | **11 档全降 S**：FAST 1.56 > SLOW 1.23 > STATISTICAL 1.09 > NONE 0.85 > INDUSTRY 0.57 > CROWDING 0.42 |
| `ts_decay_linear` / `hump` | 累积型信号上零和（S 1.33→0.90 / 0.87） |
| `group_zscore` / `tail` / `bucket` | rank 类信号上灾难（S −0.94 ~ −1.12） |
| `trade_when` 门控 | 稀疏事件型上样本骤减（S 0.57~1.12 全差于无门控） |
| 腿方向混合 | `reverse` = 整体取负 ⇒ `multiply(rank(A), reverse(rank(B)))` 恰为同向版的负数（S −1.41），**无混合语义** |
| 扫 `truncation` | 零杠杆（0.04 与 0.12 指标逐位相同） |
| 腿级时序归一化 | `ts_rank` / `ts_zscore` / `ts_scale` / `ts_av_diff` / `ts_ir` 全部劣于原始（S 0.15~1.48） |
| 掩码换样本 | shortinterest3 上 TO 爆到 0.19；fundamental6 上中性 |

---

## 「字段变体」杠杆（保 S 提 2Y，不降 prod）

同一概念常有多种字段变体，**alphaCount 差 3~5 倍**（≠prod 差异，但 2Y 差很大）：

| 概念 | `_p5_d1`(cov .783) | 无后缀(cov .668) | `_main`(cov .687) |
|---|---|---|---|
| 交易笔数 | aC 48 / 2Y 1.88 | aC 4 | **aC 15 / 2Y 2.71** |
| 最高费率 | aC 142 | aC 26 | aC 25 |

⇒ **实测：`_main` 变体 2Y 从 1.88 → 2.71，S 保持**（但不降 prod——同概念同持仓）。
⇒ 用法：**2Y 缺口大时优先换变体**，比调窗便宜。
