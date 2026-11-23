# O0W6ZwAv 精调报告（2026-11-21）

> 目标：把唯一未过闸的 Fitness（0.94，门槛 1.0）补上。
> 共 **19 颗**仿真（8 批）：ts_delta 窗口 / decay / truncation / 中性化轴 / universe / ts_backfill / 尺度变换。

## 一、结论：**F 天花板 0.96，参数层面无解**

原件仅一项不过：`LOW_FITNESS 0.94`（同时带 `LOW_SHARPE 1.59` 极薄余量 0.01）。所有改动都只能在 **S 与 R 之间互换**，F 最高只到 0.96。

```
原件：group_rank(ts_delta(ceo_tenure_days, 75), subindustry)
USA / TOP3000 / D1 / decay 16 / SUBINDUSTRY / trunc 0.05
```

| 变体 | S | **F** | Returns | TO | sub | invest | 2Y |
|---|---|---|---|---|---|---|---|
| **原件**（SUBIND / d16 / d75） | **1.59** | 0.94 | 4.39% | 5.00% | 0.80 | **1.60** | 1.88 |
| **`2r59P7pJ`**（INDUSTRY / d20 / d90） | 1.54 | **0.96** | **4.85%** | 4.49% | **1.01** | 1.55 | 1.81 |
| `Wjl3KpAj`（INDUSTRY / d20 / d75） | 1.54 | 0.95 | 4.80% | 4.53% | 0.93 | 1.55 | 1.76 |
| `npambdax`（INDUSTRY / d16 / d75） | 1.54 | 0.95 | 4.76% | 4.85% | 0.94 | 1.55 | 1.76 |
| `GrmXEQ53`（INDUSTRY / d12 / d90） | 1.53 | 0.94 | 4.71% | 5.21% | 0.99 | 1.56 | 1.82 |
| `kqavRXgL`（**trunc 0.10**） | 1.59 | 0.94 | 4.39% | 5.00% | 0.80 | 1.60 | 1.88 |
| `E5QmenYG`（decay 8） | 1.56 | 0.91 | 4.23% | 5.99% | 0.74 | 1.59 | 1.84 |
| `zqdgapvd`（`ts_backfill(...,22)`） | 1.49 | 0.89 | 4.44% | 4.97% | 0.78 | 1.35 | 1.92 |
| `rK79kXKE`（`ts_zscore` 包裹） | 1.53 | 0.84 | 3.81% | 4.97% | 0.91 | 1.57 | **2.45** |
| `1YWOvEqM`（delta 126） | 1.41 | 0.79 | 3.96% | 4.56% | 0.82 | 1.40 | 1.47 |
| `LLKEeJLa`（delta 252） | 1.28 | 0.68 | 3.56% | 3.26% | 0.37 | 1.34 | 1.71 |
| `1YWO5N1Q`（delta 45） | 1.18 | 0.61 | 3.37% | 6.67% | 0.39 | 1.32 | 1.36 |
| `j2aoLpro`（**STATISTICAL**） | 1.31 | 0.61 | 2.68% | 6.71% | 0.58 | 1.32 | 1.51 |
| `zqdganE1`（**TOP1000**） | 0.76 | 0.32 | 2.21% | 6.01% | 0.67 | 0.75 | 0.59 |

## 二、为什么升不上去（机制）

该族换手 4.5–5.0% **远低于 12.5% 的 F 分母下限**，所以平台用固定分母：

```
F = S · sqrt(|Returns| / 0.125)
```

要 F ≥ 1.0，在 S = 1.58 时必须 `Returns ≥ 5.01%`。实测最好的是 INDUSTRY 轴的 **4.85%**，而它的 S 只有 1.54（差 0.04）。

**S 与 R 完全对冲**：
- `SUBINDUSTRY` ⇒ S 高（1.59）、R 低（4.39%）⇒ F 0.94
- `INDUSTRY` ⇒ R 高（4.85%）、S 低（1.54）⇒ F 0.96

两条路都无法同时满足 S ≥ 1.58 ∧ R ≥ 5.01%，F 因此封顶在 **0.96**。

## 三、其余结论

1. **truncation 是空操作**：0.05 与 0.10 **逐位相同**（S 1.59 / F 0.94 / R 4.39% / TO 5.00% 全同）——`group_rank` 等权输出，无权重触及上限。
2. **窗口 75 是本族最优点**：45 / 60 → S 1.18；126 → 1.41；252 → 1.28。信号本质是「CEO 换届事件」，窗口太短抓不到、太长被稀释。
3. **`ts_backfill` 有害**（S 1.49）：字段稀疏本身就是信息，补齐反而稀释事件。
4. **universe 不可收紧**：TOP1000 → S **0.76**、R 2.21%，与 WjlYOj8o 同族结论一致——信号只存在于小盘。
5. **STATISTICAL 中性化最差**（S 1.31 / F 0.61）。

## 四、六维与塔（这是本件真正的价值）

- **六维**：ops **2**（`group_rank` + `ts_delta`）｜fields **1**｜**ΔT1 −0.0264**｜**ΔT2 −0.0077**｜T3 flat｜T4 +1
- 这是近期唯一**同时改善 T1 与 T2** 的候选（T1 维度是成本项，ops 2 远低于当季均值 5.72）
- **塔**：`USA/D1/INSIDERS ×1.1` 单类别，无混塔折损；当季 INSIDERS 计数 0 → 1（不点亮）
- self corr **0.5776** PASS（高于软线 0.55，需注意分散度软闸）

## 五、分组轴扫描（补测，7 颗）

用户追问「group 轴 / group_cartesian_product / 同区可作轴的字段」，补测如下（均 decay 16 / SUBINDUSTRY 中性化 / trunc 0.05 / TOP3000）：

| 件 | 分组轴 | S | F | Returns | TO | sub | 2Y | 塔 |
|---|---|---|---|---|---|---|---|---|
| **`O0W6ZwAv`** | **`subindustry`** | **1.59** | **0.94** | 4.39% | 5.00% | 0.80 | 1.88 | INSIDERS 1.1 |
| `xAvVwegq` | `industry` | 1.53 | 0.91 | 4.45% | 5.01% | 0.78 | 1.94 | INSIDERS 1.1 |
| `RRe9ZNWa` | `sector` | 1.54 | 0.93 | 4.54% | 5.00% | 0.82 | 2.00 | INSIDERS 1.1 |
| `KPgvYnaN` | `market` | 1.54 | 0.93 | 4.57% | 5.00% | 0.83 | 2.01 | INSIDERS 1.1 |
| `zqdgw5z1` | `bucket(rank(cap), .2)` | 1.54 | 0.92 | 4.43% | 5.02% | 0.75 | **2.31** | **PV+INSIDERS** |
| `leaE67XN` | `gcp(sector, bucket(cap,.5))` | 1.54 | 0.92 | 4.45% | 5.03% | 0.79 | **2.29** | **PV+INSIDERS** |
| `6XMZP5pG` | `gcp(subindustry, bucket(cap,.5))` | **1.59** | 0.92 | 4.23% | 5.13% | 0.73 | **2.41** | **PV+INSIDERS** |
| `YPa8wRvo` | `gcp(subindustry, bucket(cap,.2))` | 1.54 | 0.88 | 4.10% | 5.39% | 0.69 | 2.40 | **PV+INSIDERS** |

**结论**：
1. **`subindustry` 是最优轴**，S 1.59 是唯一触及 1.58 线的；`industry`/`sector`/`market` 全部掉到 1.53–1.54，同时触发 LOW_SHARPE，反而多一项 FAIL。
2. **`group_cartesian_product` 三项全数无效**：`gcp(subindustry, cap)` 能保住 S 1.59，但 Returns 从 4.39% 降到 4.23% ⇒ F 从 0.94 降到 0.92。机制上 gcp 只是**细分组**（组内标的更少），既不改截面方向也不增信息量。
3. **唯一正面发现**：`cap` 作轴把 **2Y 从 1.88 提到 2.41**（`gcp(subindustry, cap .5)`），但代价是 R 下降、sub 掉到 0.73，且 **`cap` 属 PV 数据集 ⇒ 塔变 PV+INSIDERS 双类别、ATOM 失效改走 IS_LADDER**。
4. 因此**分组轴不是破 F 墙的杠杆**——所有轴都在同一 S/R 平面内互换，F 始终 ≤ 0.94。

## 六、同区 GROUP 字段扫描（第二批，5 颗）

用 `get_datafields` 检索出 USA/TOP3000/D1 下**类型为 GROUP 的字段**（可直接作分组轴），取 5 个代表测试：

| 件 | 分组字段 | 类型 | S | F | 2Y | IS_LADDER | 塔 |
|---|---|---|---|---|---|---|---|
| **`O0W6ZwAv`** | `subindustry`（内置） | — | **1.59** | **0.94** | 1.88 | 不适用（ATOM） | INSIDERS |
| `e7aNKlNO` | `industrial_factor1_grouping10` | GROUP | 1.37 | 0.74 | 1.23 | **FAIL** | PV+INSIDERS |
| `leaE2LE8` | `industrial_factor2_grouping10` | GROUP | 1.38 | 0.75 | 1.17 | **FAIL** | PV+INSIDERS |
| `j2aoX5oo` | `principal_component_2_top3000_513` | GROUP | 1.36 | 0.74 | 1.34 | **FAIL** | PV+INSIDERS |
| `zqdgjvgE` | `principal_component_score_10_top3000` | GROUP | 1.36 | 0.74 | 1.30 | **FAIL** | PV+INSIDERS |
| `LLKE6PmL` | `principal_component_score_11_top3000` | GROUP | 1.36 | 0.74 | 1.31 | **FAIL** | PV+INSIDERS |

**机制（这是关键）**：这些 GROUP 字段不属于内置分类，一旦引入就**多一个数据集** ⇒ **ATOM 失效**，改为走 IS-Ladder，而它们的 2Y 只有 1.17–1.34（门槛 1.58 for year=2）⇒ **新增一项硬 FAIL**。同时 S 也从 1.59 掉到 1.36–1.38。

其余可用 GROUP 字段（未测，供参考）：`pv13_2l_scibr`(cov .94) / `pv13_new_5l_scibr`(cov .99) / `pv13_hierarchy_min20_3000_sector`(cov 1.0) / `pv13_hierarchy23_sector`(cov 1.0) / `pv13_h_factor1_sector`(cov 1.0, 5532 颗) / `exchange`(cov 1.0, 54749 颗)。它们同属 pv13 数据集，同样会导致 ATOM 失效。

## 七、加信息腿尝试（第三批，7 颗）

按 11-19 判据，跨数据集辅助腿只有三种合规形态；本件用了其中两种（乘法复合、`trade_when` 门控），全部失败：

| 件 | 形态 | 辅助字段 | S | F | sub |
|---|---|---|---|---|---|
| **`O0W6ZwAv`** | — | — | **1.59** | **0.94** | 0.80 |
| `1YWOmpjm` | 乘法复合 | `median_chief_officer_tenure_days` | 1.54 | 0.89 | 0.73 |
| `omaRzNo5` | 乘法复合 | `board_member_count_2` | 1.48 | 0.84 | **0.43 FAIL** |
| `9ql86pEV` | 乘法复合（窗90） | `board_member_count_2` | 1.45 | 0.81 | 0.50 FAIL |
| `LLKEXG51` | 乘法复合 | `board_external_connection_count` | 1.18 | 0.59 | 0.31 FAIL |
| `j2aowxKO` | `trade_when` 门控 | `board_external_connection_count` | 0.78 | 0.29 | 0.31 FAIL |
| `gJaXPdVm` | `trade_when` 门控 | `board_member_count_2` | 0.74 | 0.26 | 0.34 |
| `N1PLj3le` | `trade_when` 门控 | `median_chief_officer_tenure_days` | 0.25 | 0.05 | 0.28 |

**两个结论**：
1. **乘法复合全部降低 S**（1.18–1.54 vs 1.59）：`rank()` 输出在 [0,1]，相乘后截面被压向 0 一侧，等于损失一半排序信息。
2. **`trade_when` 门控是灾难**（S 0.25–0.78）：治理结构变化与「CEO 任期变化」的 alpha 方向不对齐，门控把有效样本切掉了大半。
3. 附带确认：这 6 个治理字段与 `ceo_tenure_days` **同属 insiders 数据集**（全部变体 `pyramid_short` 仍为 `insiders`）⇒ 不丢 ATOM、不混塔，但也意味着**没有增量信息**——这正是它们无法提升 S 的根因。

## 八、结论与建议

**不加信息就交不了**。三条路：

1. **保持原样不交**——F 0.94 是硬 FAIL，平台直接拦。
2. **换 INDUSTRY + decay 20（`2r59P7pJ`）**——F 0.96 仍差 0.04，且 S 1.54 触发 LOW_SHARPE，两项都不过，比原件更糟。
3. **加一条信息腿把 S 拉过 1.65**（唯一有希望的路径）：本件 ops 只有 2，加 1–2 个算子仍能把 ΔT1 保持在负值（ops 4 时 ΔT1 = −0.0122）。可用的同族信息：`board_member_count_2` / `median_chief_officer_tenure_days` / `board_external_connection_count`（治理结构），用 `multiply(rank(a), rank(b))` 形态（非等权相加，不触发混腿闸）。

若走第 3 条，代价是 T4 之外多花 2 个 ops、fields 从 1 升到 2–3，需权衡六维收益是否能抵过 F 闸的收益。
