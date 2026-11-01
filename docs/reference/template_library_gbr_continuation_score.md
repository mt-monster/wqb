# GBR / TOP700 / D1 — `continuation_score` 模板库与实测账本

> 数据集：`continuation_score`（PV 塔，560 个 MATRIX 字段，全形态相似度）
> 区域：GBR / TOP700 / Delay 1 / 2014-01-01 ~ 2023-12-31
> 建档：2026-10-30。本文件汇集该数据集在 GBR 的全部实测证据与模板配方。

---

## 一、数据集画像

| 项 | 值 | 来源 |
|---|---|---|
| 字段总数 | **560**（全 MATRIX） | `get_datafields(platform_count)` |
| 塔位 | **GBR/D1/PV**（单塔） | `get_alpha_details.pyramids` |
| 命名范式 | `{形态}_similarity_{统计量}` 与 `{统计量}_similarity_{形态}` **两种混用** | 字段实读 |
| 统计量集合 | `average / mean / maximum / max / minimum / min / median / 95th_percentile / q95 / peak / recent / dynamic / middle / dispersion / stdev / stddev` | 字段实读 |
| 窗口后缀 | 无后缀（默认） / `_h40` / `_h40w`（40 周 ≈ 200 交易日） | 字段实读 |
| `coverage` 列 | **全部 0.0**（平台字段 bug） | `get_datafields` |
| 真实覆盖 | **以 `get_alpha_details` 的 `longCount + shortCount` 为准** | 见 §2 |
| 拥挤度 | 极低，多数字段 `u0/a0` | `get_datafields` |

★ **`coverage = 0.0` 是显示 bug，不是无数据**：`vR1aA8R3` 用 `avg_similarity_continuation_gap_*`，实读 `longCount 448 + shortCount 452`，十年全覆盖。**任何「看 coverage=0 就判死」的做法在该数据集上是错的**，必须用 `get_alpha_yearly_stats` 或 `longCount/shortCount` 核。

### 1.1 已核实的对称配对（gap 族）

| 配对用途 | down 侧字段 | up 侧字段 | u/a（down / up） |
|---|---|---|---|
| **主信号（本档最强）** | `avg_similarity_continuation_gap_down` | `avg_similarity_continuation_gap_up` | 13/13 · 55/69 |
| peak 统计量 | `downward_gap_peak_similarity` | `upward_gap_peak_similarity` | 2/2 · 0/0 |
| recent 族 | `gap_down_continuation_similarity_recent` | `gap_up_continuation_similarity_recent` | 0/0 · 0/0 |
| 40 周 median | `gap_down_continuation_similarity_median_h40w` | `gap_up_continuation_similarity_median_h40w` | 0/0 · 0/0 |
| 40 周 maximum | `gap_down_continuation_similarity_maximum_h40w` | `gap_up_continuation_similarity_maximum_h40w` | 0/0 · 0/0 |
| 95 分位 | `quantile95_downward_gap_continuation_score` | `upward_gap_95th_similarity` | 14/17 · 2/3 |
| dynamic | `dynamic_downward_gap_continuation_score` | — | 14/18 |
| stdev | `stddev_downward_gap_continuation_score` | `stddev_upward_gap_continuation_score` | — |
| 高拥挤（备份） | `downward_gap_peak_similarity_h40` | — | **62/113（全数据集最热）** |

---

## 二、★★★ 核心机制发现：方向与 `pattern_scores` 相反

| 数据集 | gap 正确方向 | 机理 | 来源 |
|---|---|---|---|
| `pattern_scores` / `common_gap` | **`up − down`（延续）** | 流动性不足持续 ⇒ 价格漂移延续 | Amihud 2002 |
| `pattern_scores` / `breakaway_gap` | **`down − up`（反转）** | 消息驱动隔夜过度反应 ⇒ 回补 | Lehmann 1990 / Jegadeesh 1990 |
| **`continuation_score` / gap 全族** | **`down − up`（反转）** | 同 breakaway | **本档批 34 实测** |

**注意**：数据集名叫 `continuation_score`，但在 GBR 的 gap 族上**行为是反转**，与名字暗示相反。
⇒ **进入任何形态相似度数据集的任何形态族，必须先跑一条最小探针定符号**。负值不浪费（Sharpe 线性于收益符号，翻转即精确取反）。

### 2.1 论坛「peak 统计量强 10 倍」在 GBR 不成立

论坛帖 `43298855144855`（YZ29225，ASI）称 `peak` 统计量 S 1.27 vs `average` S 0.37（强 10 倍）。**GBR 实测相反**：

| 统计量 | alpha | 原 S | **翻转后 S** | 翻转后 F | 翻转后 2Y | 翻转后 SUB/S |
|---|---|---:|---:|---:|---:|---:|
| **avg** | `vR1aA8R3` | −1.37 | **1.37** | **1.04** | **1.50** | 0.401 |
| peak | `j2YNav5k` | −1.06 | 1.06 | 0.72 | 0.91 | 0.377 |

⇒ **avg 反强 29%**。统计量强弱是**区域属性**：GBR TOP700 大盘股形态平滑、噪声日少 ⇒ 均值类统计量信息利用率更高，`peak`（极端时刻）反被单日异常主导。
⇒ **跨区搬「最强统计量」结论前，先用同一对字段测 `avg` / `peak` / `median` / `q95` 四档**。

---

## 三、实测账本

### 3.1 批 34：方向定符号探针（SECTOR / decay 20 / trunc 0.06）

| alpha | 表达式 | S | F | TO | 2Y | SUB | dd | margin |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `vR1aA8R3` | `ts_quantile(subtract(ts_backfill(avg_similarity_continuation_gap_up,22), ts_backfill(avg_similarity_continuation_gap_down,22)), 252)` | **−1.37** | −1.04 | 11.21% | **−1.50** | −0.55 | 73.99% | −12.79bp |
| `j2YNav5k` | `ts_quantile(subtract(ts_backfill(upward_gap_peak_similarity,22), ts_backfill(downward_gap_peak_similarity,22)), 252)` | −1.06 | −0.72 | 11.35% | −0.91 | −0.40 | 59.08% | −10.07bp |

**两条都是平台新 id（未撞已有 alpha）⇒ 该方向此前无人做过，是真新机制。**

**翻转后（`vR1aA8R3` 等价正版）**：S **1.37** / F **1.04** / 2Y **1.50** / SUB 0.55 / **SUB/S 0.401 ✗** / margin **+12.79bp**（高于 GBR 中位 11.9bp）/ `risk_neutralized_sharpe` 0.36 / 塔 GBR/D1/PV ✅ / 覆盖 448+452 ✅

### 3.2 批 36：设置迁移到 `INDUSTRY / decay 2 / trunc 0.05`（翻转版正式测）

| alpha | 归一化层 | S | F | TO | 2Y | SUB | **SUB/S** | dd | margin | invest_S | invest_ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `vR1aAdnb` | `ts_quantile(·, 252)` | **1.31** | 0.65 | 24.71% | 1.02 | 0.68 | **0.519 ✅** | **4.84%** | 4.96bp | 1.52 | **1.1603** |
| `58ENJM36` | `ts_zscore(·, 252)` | **1.31** | 0.67 | 23.16% | 1.01 | 0.72 | **0.550 ✅** | 5.00% | 5.20bp | 1.44 | 1.0992 |

**★★★ SUB/S 从 0.401 → 0.519/0.550，过闸。** 但 F（1.04→0.65）、2Y（1.50→1.02）、margin（12.79→4.96bp）全面回落。
⇒ **该族存在「F/2Y/margin ↔ SUB/S」的明确权衡，decay 与中性化是主控旋钮。**

**`investability_sharpe 1.52 > sharpe 1.31`（invest_ratio 1.16）** 是罕见的好信号：流动性好的股票上表现更好，说明信号不靠小票驱动。

### 3.3 对照：`pattern_scores` 同结构（供跨数据集比较）

| alpha | 设计 | S | F | 2Y | SUB/S | 判定 |
|---|---|---:|---:|---:|---:|---|
| `RRE0EArj` | quantile **252** | **1.10** | 0.68 | **1.44** | **0.755** | 该族最优 |
| `kqNearg8` | quantile **504** | 0.94 | 0.54 | 1.06 | 0.734 | 504 全面差 −15% |
| `WjOKlQeG` | **`signed_power` 取代分位** | 0.48 | 0.19 | 0.90 | 0.917 | **−56%，作废** |

⇒ **`ts_quantile` 分位层不可被 `signed_power` 替代**；**252 分位窗口是该类配对的最优**。
（对 `continuation_score` 的 `signed_power` **外套**测试见 §4 T4，尚未跑。）

### 3.4 ★★ 平台事实纠错：SUB 闸对负 Sharpe alpha 带符号

`vR1aA8R3` S = −1.37、SUB = −0.55，`LOW_SUB_UNIVERSE_SHARPE` 却列在 **pass**。
口径是 `sub_sharpe >= 0.4754 × sharpe`（**两侧带符号**）：−0.55 >= −0.6514 成立 ⇒ pass。
**⇒ 任何负 Sharpe 候选的 SUB 闸结论一律作废**，必须按翻转后的正数重算 `SUB/S ≥ 0.4754`。
**副作用**：反向探针的 `failed_ra_count` 恒为 3，只报 `LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE`，**SUB 失败被漏计**。

---

## 四、模板库（12 个，结构互异）

> 规则：差异必须落在**骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换 / 窗口族**上，只换常数或只换窗口不算独立模板。
> 来源标注：`[自建]` / `[论坛:ID]` / `[论文:作者年份]`。

| # | 模板名 | 骨架 | 差异轴 | 来源 | 状态 |
|---|---|---|---|---|---|
| **T1** | 分位归一配对 | `ts_quantile(subtract(ts_backfill(D,22), ts_backfill(U,22)), 252)` | 基准：秩归一 + 水平差 | `[自建]` + 批 36 | ✅ 实测 S 1.31 / SUB/S 0.519 |
| **T2** | Z 分数归一配对 | `ts_zscore(subtract(ts_backfill(D,22), ts_backfill(U,22)), 252)` | 归一算子：保幅度 vs 压尾 | `[自建]` + 批 36 | ✅ 实测 S 1.31 / SUB/S 0.550 |
| **T3** | 秩变换配对 | `ts_rank(subtract(ts_backfill(D,22), ts_backfill(U,22)), 252)` | 去幅度、纯位置信息 | `[自建]` | 预检已过，未跑 |
| **T4** | signed_power 外套 | `signed_power(ts_quantile(<T1>), 0.1)` | 非线性压缩极端值 | `[论坛:43298855144855]` | 预检已过，未跑 |
| **T5** | signed_power 取代分位 | `signed_power(subtract(<D>, <U>), 0.1)` | 用幂变换替代秩归一 | `[论坛:43298855144855]` | ❌ `WjOKlQeG` S 0.48（−56%） |
| **T6** | 40 周 median 配对 | 用 `gap_{down,up}_continuation_similarity_median_h40w` | **窗口族：40 周（≈200 日）** | `[自建]` | 未跑（零拥挤） |
| **T7** | 40 周 maximum 配对 | 用 `gap_{down,up}_continuation_similarity_maximum_h40w` | 窗口族 × 极值统计量 | `[自建]` | 未跑（零拥挤） |
| **T8** | recent 族配对 | 用 `gap_{down,up}_continuation_similarity_recent` | 统计量族：近端加权 | `[自建]` | 预检已过，未跑 |
| **T9** | 一阶差分（反转强度变化） | `ts_quantile(ts_av_diff(<配对>, 22), 252)` | **矩：一阶差分**（水平→变化） | `[论文:Lehmann 1990]` | 未跑。**前提**：需存在均值回归，本族已证是反转机制 ⇒ 前提成立 |
| **T10** | 波动率标准化 | `divide(<配对>, ts_std_dev(<配对>, 66))` | **二阶矩**（同单位相除，合规） | `[自建]` | 未跑。用途：压低波动聚集期的权重 |
| **T11** | 短窗分位 | `ts_quantile(<配对>, 66)` | 窗口族：短窗快速响应 | `[自建]` | 未跑。已知 252 优于 504 ⇒ 短窗方向值得试 |
| **T12** | 流动性门控 | `trade_when(greater(rank(<adv_usd>), 0.3), <T1>, -1)` | **门控轴**（不改信号，只在流动性足时持仓） | `[论文:Amihud 2002]` + `[论坛:25740783868439]` | 未跑。注意 `trade_when` 第三参 −1 = 空仓 |

★ **未使用的第五条差异轴：分组中性化**。平台中性化（`INDUSTRY` / `SUBINDUSTRY` / `SECTOR`）已验证可切；表达式层 `group_neutralize(·, subindustry)` 未试（**必须用 `group_neutralize` 不能用 `group_rank`** —— `group_rank` 是实测的 SUB 杀手）。

---

## 五、设置档案

| 设置 | 批 34（论坛最佳） | 批 36（pattern 族几何） | 说明 |
|---|---|---|---|
| neutralization | `SECTOR` | `INDUSTRY` | 批 37 再测 `SUBINDUSTRY` |
| decay | **20** | **2** | 该族主控旋钮 |
| truncation | 0.06 | 0.05 | |
| universe | TOP700（GBR 唯一档） | 同 | |
| delay | 1 | 同 | |

**权衡曲线（同表达式，仅设置不同）**：

| 设置 | S | F | 2Y | SUB/S | margin | TO |
|---|---:|---:|---:|---:|---:|---:|
| SECTOR / decay 20 / trunc 0.06 | **1.37** | **1.04** | **1.50** | 0.401 ✗ | **12.79bp** | 11.21% |
| INDUSTRY / decay 2 / trunc 0.05 | 1.31 | 0.65 | 1.02 | **0.519** ✅ | 4.96bp | 24.71% |

⇒ **decay 越大 ⇒ F/2Y/margin 越高、SUB/S 越低**。中间档（批 37 扫描中）是找平衡点的关键。

---

## 六、下一步优先级

1. **decay × 中性化扫描**（在飞，4 档）：找 `SUB/S ≥ 0.48` 前提下 F 与 2Y 的最大值。
2. 若中档给出 S ≥ 1.40 / F ≥ 0.85 / 2Y ≥ 1.30 / SUB/S ≥ 0.48 ⇒ 可直接进篮子，再补 T4（signed_power 外套）冲 S。
3. 若中档仍卡 ⇒ 走 **多字段同概念合成**（论坛生产级做法：≤3 个同向字段等权，禁止权重扫描）冲 S。
4. **T6/T7（40 周族）** 是零拥挤的第二入口，与主信号窗口差 200 日 ⇒ 互相关应显著低于 0.7，可独立成第二条 PV alpha。

---

## 七、禁忌与陷阱

- ❌ **`signed_power` 取代分位层**（`WjOKlQeG` S 0.48，−56%）。
- ❌ **分位窗口 504**（`kqNearg8` S 0.94，−15%；2Y 1.06，−26%）。
- ❌ **负 Sharpe 下读 SUB 闸**（带符号比较，结论作废）。
- ❌ **`signed_power(subtract(...), k)` 权重混信号**（`multiply(rank(B), 0.3/0.5)` 属禁止形态）。
- ❌ **`coverage = 0.0` 当判死依据**（该数据集全字段显示 0.0）。
- ❌ **假设数据集名字暗示方向**（`continuation_score` 在 gap 族是反转）。
- ❌ **`group_rank` 做分组**（SUB 杀手，用 `group_neutralize`）。
- ⚠ `add(A,B)` 混信号调参禁止；**同概念多字段等权（权重恒 1、不扫描）** 属论坛生产做法，须在文档中显式声明为「同概念合成」而非「混信号调参」。

---

## 八、批 37–40：可行域测绘 / 命名族证伪 / 8 组对称配对（2026-10-30）

### 8.1 ★★★ decay × 中性化可行域测绘（同一表达式，全部实测）

表达式恒为：

```
ts_quantile(subtract(ts_backfill(avg_similarity_continuation_gap_down, 22),
                     ts_backfill(avg_similarity_continuation_gap_up, 22)), 252)
```

| alpha | decay | 中性化 | trunc | S | F | TO | 2Y | SUB | **SUB/S** | dd | margin | 判 |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `9qxglxlq` | 6 | INDUSTRY | 0.06 | 1.48 | 0.87 | 19.53% | 1.22 | 0.77 | **0.520** | 4.70% | 6.86bp | F/2Y 死 |
| `MPY9g8jo` | 10 | INDUSTRY | 0.06 | 1.58 | 1.05 | 15.95% | 1.45 | 0.78 | **0.494 ✅** | 4.31% | 8.80bp | 只 2Y 死（差 8.3%） |
| **`MPY96E7o`** | **16** | **SUBINDUSTRY** | 0.06 | **1.70** | **1.24** | 12.91% | **1.94** | **0.82** | **0.482 ✅** | 4.02% | 10.67bp | **全闸通过** ✅ |
| `WjOKlOej` | 20 | SUBINDUSTRY | 0.06 | 1.67 | 1.23 | 11.62% | 2.03 | 0.76 | 0.455 | 4.25% | 11.61bp | SUB 差 3.8% |
| `58ENGZM6` | 20 | SUBINDUSTRY | **0.08** | 1.67 | 1.23 | 11.62% | 2.03 | 0.76 | 0.455 | 4.25% | 11.61bp | trunc 0.08 = **no-op** |
| `JjeR3jgm` | 20 | SUBINDUSTRY | 0.06 | 1.66 | 1.20 | 11.59% | 2.05 | 0.73 | 0.442 | 3.79% | 11.25bp | **ts_zscore** 更差 |
| `JjeR83xO` | 20 | INDUSTRY | 0.06 | 1.55 | 1.14 | 11.41% | 1.73 | 0.63 | 0.406 | 3.79% | 11.83bp | SUB 死 |

**★★★ 结构性结论：2Y 随 decay 单调升（1.22 → 1.45 → 1.94 → 2.03），SUB/S 随 decay 单调降（0.520 → 0.494 → 0.482 → 0.455）⇒ 可行域是这两条曲线的交点，实质上只有一个点（decay 16 / SUBINDUSTRY / trunc 0.06）。**

推论：
1. **不要沿这条曲线继续找「更好」的点**——上下都是墙。decay < 16 挂 2Y，decay > 16 挂 SUB。
2. 想要第二条 alpha，必须**平移整条曲线**，不是沿曲线滑动。可平移的维度：换字段（见 8.2，已证伪）、换归一化层（已证伪）、换 trunc（no-op）、换中性化轴（INDUSTRY 全面更差）。
3. `truncation 0.06 → 0.08` 在本族是**逐位 no-op**（`58ENGZM6` 与 `WjOKlOej` 全部指标相同）⇒ trunc 在本族不是可调旋钮。
4. `ts_zscore` 与 `ts_quantile` 的最优选择**随 decay 变**：decay 2 时 zscore 的 SUB/S 高 +0.031；decay 16/20 时 quantile 更好（decay 16 quantile SUB 0.82 PASS vs zscore 0.77 / fRA 1）。**必须与 decay 联合扫，不能固定一层。**

### 8.2 ★★★ 命名族证伪：`gap_{dir}_continuation_similarity_{stat}` 全族只有 S 0.72–0.89

批 38/39 用**同一骨架、同一设置（decay 16 / SUBINDUSTRY / trunc 0.06）**测了这个兄弟命名族的 4 个结构变体：

| alpha | 字段对（统计量） | S | F | 2Y | SUB | SUB/S | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| `GrWEQkXJ` | `median_h40w`（40 周中位数） | 0.72 | 0.35 | 0.98 | 0.23 | 0.32 | 4 |
| `9qxgGJ8V` | `recent`（近期 bar） | 0.81 | 0.39 | 1.23 | 0.27 | 0.33 | 4 |
| `VkxKMm1G` | `dynamic_h40w`（40 周近期加权） | 0.79 | 0.41 | 1.14 | 0.29 | 0.37 | 4 |
| `e75e1VkN` | `percentile_95`（95 分位） | 0.89 | 0.45 | 1.39 | 0.26 | 0.29 | 4 |

**★★★ 决定性对比**：平台描述文字几乎逐字相同的两套字段，强度差一倍——

| 命名族 | 平台 description | S |
|---|---|---:|
| `avg_similarity_continuation_gap_{down,up}` | "Average similarity score to the downward gap continuation pattern" | **1.70** |
| `gap_{dir}_continuation_similarity_average` | "Average similarity score for downward gap continuation pattern" | 未测（预计与上者 ~1.0 相关） |

⇒ **两套命名族是不同构造，只有 `avg_similarity_continuation_gap_*` 这一对是真矿。**
⇒ **「换统计量」不是免费的多样性来源**，等价于换一个全新信号，必须独立验证。
⇒ **不能按 description 文字归并字段**，归属统计必须按完整 id 的命名范式分组。

**`continuation_score` 的 PV 挖掘至此基本见底**：唯一可用入口 = `avg_similarity_continuation_gap_{down,up}` 反转 + decay 16 / SUBINDUSTRY / 0.06。

### 8.3 8 组对称配对清单（`gap_{dir}_continuation_similarity_{stat}` 族，全量实读）

| 统计量 | down id 后缀 | up id 后缀 | 拥挤度 down / up | 实测 |
|---|---|---|---|---|
| average | `similarity_average` | `similarity_average` | u1/a1 · u1/a1 | 未测 |
| minimum | `similarity_minimum` | `similarity_minimum` | u3/a3 · u1/a1 | 未测 |
| recent | `similarity_recent` | `similarity_recent` | u0/a0 · u0/a0 | **0.81 / 0.81**（弱） |
| percentile_95 | `similarity_percentile_95` | `similarity_percentile_95` | u1/a3 · u1/a1 | **0.89**（弱） |
| average_h40w | `similarity_average_h40w` | `similarity_average_h40w` | u1/a2 · u1/a1 | 未测 |
| median_h40w | `similarity_median_h40w` | `similarity_median_h40w` | u0/a0 · u0/a0 | **0.72**（弱） |
| dynamic_h40w | `similarity_dynamic_h40w` | `similarity_dynamic_h40w` | u1/a2 · u1/a1 | **0.79**（弱） |
| maximum_h40w | `similarity_maximum_h40w` | `similarity_maximum_h40w` | u1/a1 · u0/a0 | 未测 |

**不对称族（无法配对，只能做 level 信号）**：`min_similarity_continuation_gap_up`（u3/a4）、`quantile95_similarity_continuation_gap_down`（u7/a13）、`median_similarity_continuation_gap_up`（u3/a5）、`stddev_similarity_continuation_gap_up`（**u0/a0**，方差矩，未开发）。
`*_maximum_h60` 只有 down 侧（`gap_down_continuation_similarity_maximum_h60`，u3/a5），up 侧不存在。

### 8.4 本轮设置层面的三条 no-op / 反例（省仿真槽用）

- ★ `truncation 0.06 → 0.08`：**逐位 no-op**（本族）。
- ★ `neutralization INDUSTRY → SUBINDUSTRY`：全面改善（S +8% / F +8% / 2Y +17% / SUB +21%），在 decay 20 下依然成立。
- ★ `ts_zscore` 替换 `ts_quantile`：在 decay 16/20 下**更差**（SUB 0.82 → 0.77 / 0.76 → 0.73）。与 decay 2 时相反。