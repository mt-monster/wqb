# Wave 180 — earnings_sent_matrix 条件正概率 CP 的十模板消融

**日期**：2026-10-29
**区域 / 宇宙 / 延迟**：USA / TOP2000 / D1
**数据集**：`earnings_sent_matrix`（7 字段，cov 全 0.70，alphaCount 1,431，PyramidMultiplier 1.2 → EARNINGS 塔）
**multisim**：`3RHtYN3fI4u8buYGE4NRsL3`
**设置**：INDUSTRY / **decay 0** / truncation 0.08 / nanHandling ON / pasteurization ON / maxTrade OFF
**结论**：**PASS** — 命中 2 颗全闸候选（`ZYQZbnYx` S 1.71 / `88RAjQmo` S 1.70），同时证明该数据集只能提交 1 颗。

---

## 1. 为什么开这一波

波 179 在 `earnings_sent_matrix` 上跑出两颗**近闸**候选：

| alpha | 结构 | S | F | 2Y | SUB | 缺口 |
|---|---|---|---|---|---|---|
| `RREXVG2b` | `group_rank(CP, industry)`，decay 4 | 0.97 | 0.51 | 1.30 | 0.75 | S 差 0.61，F 差 0.49 |
| `YP1Z5R26` | 加权分歧 W1−W2 | — | — | — | — | 同上量级 |

两者的共同特征是：**换手率全部落在地板下（5–7%）**。按 `F = S × sqrt(R / max(TO, 0.125))` 的算术，此时
`F = S × sqrt(R / 0.125) = S^1.5 × sqrt(k / 0.125)`（因 `R = S × k`），F 与 S 合并为同一个目标 —— 只要 S 到 1.58，F 自动过 1.0。

所以本波唯一任务：**在保持 CP（条件正概率）机制不变的前提下，找能把 S 从 0.97 推到 ≥1.58 的杠杆。**

### 关键设置修正：decay 4 → 0

波 179 派发时**没有显式传 `decay`**，落到了 `create_multi_simulation` 的默认值 4。本波显式传 `decay=0`。

这不是随手调的。`earnings_sent_matrix` 是**季频事件型**数据：字段更新频率是季度，`ts_backfill(F, 252)` 把季度值前向填充到日频。在这种信号上，decay 平滑的是**已经过期的信息**——它不降噪，只是把信号往后拖。所以 decay 应当取 0。

**事后看这是本波最大的单一杠杆**（见 §4 提 S 杠杆排序）。

---

## 2. 十模板清单（结构互异）

核心信号 CP = 条件正概率：

```
CP = divide(
       ts_backfill(positive_sentiment_probability_3, 252),
       add(ts_backfill(positive_sentiment_probability_3, 252),
           ts_backfill(negative_sentiment_probability_3, 252))
     )
```

选 CP 而不是裸 P，是因为 `P + N + NT = 1`（三分类分布只有 2 个自由度），裸 P 会被 NT（中性概率）的行业差异污染；CP = P/(P+N) 把 NT 约掉，只留「在已表态的部分里正面占多少」。

| # | 模板 | 骨架 | 与基线的结构差异 | 来源 |
|---|---|---|---|---|
| 1 | `group_rank(CP, industry)` | 横截面秩 · industry | **基线**（decay 0 修正版） | 自建 |
| 2 | `group_rank(CP, subindustry)` | 横截面秩 · subindustry | 换分组轴（更细） | 自建 |
| 3 | `group_rank(CP, sector)` | 横截面秩 · sector | 换分组轴（中等） | 自建 |
| 4 | `group_rank(CP, market)` | 横截面秩 · market | 换分组轴（最粗） | 自建 |
| 5 | `group_zscore(CP, industry)` | 组内 z 分数 | 换横截面算子（秩 → 标准化值） | 论坛 43175786936087（`rank`→`group_zscore` 降换手 20–30%） |
| 6 | `group_rank(ts_rank(CP, 504), industry)` | 长窗时序秩 → 截面秩 | **加一层长窗时序秩**（非参数历史分位） | 论坛 43805658109463（三层剥离：水平 → 相对位置 → 异常，L3 断崖式有效） |
| 7 | `group_rank(reverse(CP), industry)` | 反向 | 符号翻转（方向对照） | 论坛 43805658109463 评论 NC52614（符号方向是 PC 最大杠杆） |
| 8 | `group_rank(signed_power(subtract(CP, 0.5), 3), industry)` | 中心化 + 立方 | 非线性变换（凸化尾部） | 自建 |
| 9 | `group_rank(ts_mean(CP, 22), industry)` | 短窗时序平滑 | 一阶矩平滑（降噪对照） | 自建 |
| 10 | `group_rank(ts_zscore(CP, 504), industry)` | 长窗时序标准化 → 截面秩 | **加一层长窗时序标准化**（参数型） | 论文：Bernard & Thomas (1989) PEAD 标准化意外 |

**互异维度覆盖**：分组轴 4 档（industry / subindustry / sector / market）· 横截面算子 2 种（rank / zscore）· 时序加工 4 种（无 / ts_rank504 / ts_mean22 / ts_zscore504）· 非线性 1 种（signed_power）· 方向 1 种（reverse）。**没有任何两条只差窗口或常数。**

---

## 3. 完整结果表

| # | 变体 | alpha | S | F | TO | 2Y | SUB | invest_S | invest_F | margin | risk_neut_S | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | industry（基线） | `mLoOm8vX` | 1.23 | 0.72 | 5.91% | 1.89 | 0.93 | 0.96 | 0.49 | 14.53bp | 1.23 | 2 |
| 2 | subindustry | `vR10rLQG` | 1.36 | 0.75 | 5.99% | 2.07 | 0.94 | 1.00 | 0.48 | 12.77bp | 1.18 | 2 |
| 3 | sector | `gJevb1nO` | 1.18 | 0.69 | 6.06% | 1.80 | 0.87 | 0.91 | 0.47 | 14.17bp | 1.18 | 2 |
| 4 | market | `npv0dgL8` | 1.21 | 0.73 | 5.81% | 1.88 | 0.87 | 0.95 | 0.51 | 15.65bp | 1.19 | 2 |
| 5 | group_zscore | `d5WqbxNv` | 1.01 | 0.57 | 6.70% | 1.53 | 0.81 | 0.71 | 0.33 | 11.91bp | 1.21 | 3 |
| **6** | **ts_rank(CP,504)** | **`88RAjQmo`** | **1.70** | **1.15** | 7.22% | **2.59** | **1.11** | **1.29** | 0.76 | 15.80bp | 1.67 | **0** |
| 7 | reverse(CP) | `npv0d218` | **−0.66** | −0.29 | 5.90% | −1.02 | −0.63 | −0.37 | −0.12 | −8.11bp | −1.02 | 4 |
| 8 | signed_power(cube) | `d5Wqb02v` | 1.23 | 0.72 | 5.91% | 1.89 | 0.93 | 0.96 | 0.49 | 14.53bp | 1.23 | 2 |
| 9 | ts_mean(CP,22) | `omE2Llmm` | 0.82 | 0.39 | 4.13% | 0.82 | 0.83 | 0.82 | 0.39 | 14.02bp | 0.35 | 3 |
| **10** | **ts_zscore(CP,504)** | **`ZYQZbnYx`** | **1.71** | **1.19** | 6.84% | **2.97** | **1.24** | **1.37** | **0.86** | **17.75bp** | **1.71** | **0** |

10 条表达式全部 COMPLETE、0 错误、0 批级失败。

### 两颗全闸候选的精确表达式

```
ZYQZbnYx =
group_rank(
  ts_zscore(
    divide(ts_backfill(positive_sentiment_probability_3, 252),
           add(ts_backfill(positive_sentiment_probability_3, 252),
               ts_backfill(negative_sentiment_probability_3, 252))),
    504),
  industry)

88RAjQmo =
group_rank(
  ts_rank(
    divide(ts_backfill(positive_sentiment_probability_3, 252),
           add(ts_backfill(positive_sentiment_probability_3, 252),
               ts_backfill(negative_sentiment_probability_3, 252))),
    504),
  industry)
```

两者 `checks.fail = []`、8 项 pass、`ra.failed_ra_count = 0`、`pyramids.list = USA/D1/EARNINGS`（multiplier 1.2）。warning 仅三条非阻断项：CLUSTER_TEST（1.21 / 1.29）、MATCHES_THEMES、OSMOSIS_ALLOCATION。

---

## 4. 归因：提 S 的杠杆排序（本数据集实测）

以波 179 的 `RREXVG2b`（decay 4，S 0.97）为起点，逐个隔离变量：

| 杠杆 | S 变化 | 幅度 | 判断 |
|---|---|---|---|
| **长窗时序标准化 / 秩（504）** | 1.23 → **1.71**（zscore） / 1.70（ts_rank） | **+0.48** | ★★★ 主杠杆 |
| **decay 4 → 0** | 0.97 → 1.23 | **+0.26** | ★★ 次杠杆（且免费） |
| 分组轴 subindustry | 1.23 → 1.36 | +0.13 | ★ 弱正 |
| 分组轴 sector | 1.23 → 1.18 | −0.05 | 无差别 |
| 分组轴 market | 1.23 → 1.21 | −0.02 | 无差别 |
| `group_zscore` 替代 `group_rank` | 1.23 → 1.01 | −0.22 | ✗ 有害 |
| `ts_mean(CP,22)` 平滑 | 1.23 → 0.82 | −0.41 | ✗ 有害 |
| 方向翻转 reverse | 1.23 → **−0.66** | −1.89 | ✓ 说明方向本来就对，且极敏感 |
| `signed_power(cube)` 凸化 | 1.23 → 1.23 | **0** | 见 §5 铁律 |

### 为什么长窗时序标准化是主杠杆

两个机制叠加：

1. **它把「CP 的绝对水平」换成了「CP 相对自己历史的异常程度」。** CP 的绝对水平有很强的行业结构性差异（某些行业天生语调更正面），`group_rank(CP, industry)` 只能去掉行业均值，去不掉「该公司的常态」。`ts_zscore(CP, 504)` 减去的是**该公司自己两年的均值**，留下的是「这次财报比它自己平时正面多少」——这才是真正的预期差。
2. **2Y 从 1.89 跳到 2.97（`ZYQZbnYx`），涨幅远大于 S 的涨幅（1.23 → 1.71）。** 这说明它不是靠某一年行情拉起来的，而是近两年效果特别强。这与 PEAD 文献一致：财报漂移在信息扩散慢的市场/时期更强，近两年美股散户参与度上升、财报反应变慢。

### 为什么 `ts_mean` 和 `group_zscore` 反而有害

- `ts_mean(CP, 22)` 是日频短窗平滑，但 CP 是**季度更新**（`ts_backfill` 填 252 天），22 日窗口内 CP 几乎不变 ⇒ 平滑等于「取最近 22 天的同一批值」，只增加了滞后，不降噪 ⇒ S 掉 0.41 且 2Y 从 1.89 崩到 0.82（滞后对近期最伤）。
- `group_zscore` 在 EARNINGS 塔这类**低换手、宽持仓**信号上不如 rank 稳：rank 对尾部极端值免疫，zscore 会让少数 CP 极端（P≈1 或 N≈1）的股票权重爆掉 ⇒ S 掉 0.22、F 掉 0.15、且 fRA 从 2 升到 3。

---

## 5. 结构铁律：`group_rank` 会吃掉其内部的一切单调变换

**`d5Wqb02v` 与 `mLoOm8vX` 指标逐位相同**：
- S 1.23 / F 0.72 / TO 5.91% / 2Y 1.89 / SUB 0.93 / invest_S 0.96 / margin 14.53bp / pnl 4,282,023

但 `d5Wqb02v` 的表达式是 `group_rank(signed_power(subtract(CP, 0.5), 3), industry)`，`mLoOm8vX` 是 `group_rank(CP, industry)`。

原因：`signed_power(subtract(CP,0.5),3)` 在 CP 的取值域内是**严格单调递增**的（CP ∈ [0,1] ⇒ CP−0.5 ∈ [−0.5,0.5]，立方仍严格单调）。而 `group_rank` 只看序位，序位不变 ⇒ 输出完全一致。

**推论（可跨数据集迁移的判据）**：
> `group_rank` / `rank` / `ts_rank` 内部**只允许非单调变换**。
> 合法：`ts_mean` / `ts_std_dev` / `ts_zscore` / `ts_rank` / `ts_decay_linear` / `ts_delta`（改变时序或分布形状）。
> 无效：`signed_power` / `log` / `sqrt` / 线性缩放 / 加减常数（保序）。
> 唯一例外是**跨越 rank 的符号翻转**（`reverse`），因为那会反转序位。

同一条铁律在波 181 被独立复现：`78LON6NZ`（`group_rank(rank(x), industry)`）与 `N1NMQJog`（`group_rank(x, industry)`）指标逐位相同 —— 内层 `rank` 幂等被吃掉。

---

## 6. 决定性发现：这个数据集只能提交 1 颗

拿到三颗全闸候选后（`RREXk770` 来自波 179 的 `ts_rank(P,504)` 路线，`ZYQZbnYx` 与 `88RAjQmo` 来自本波），跑了 6 颗全家族互相关矩阵（4 年日收益，986 点）：

| 对 | 相关 |
|---|---|
| `RREXVG2b` × `mLoOm8vX` | **0.9947**（同表达式，仅 decay 4 vs 0） |
| `ZYQZbnYx` × `88RAjQmo` | **0.9596** |
| `RREXVG2b` × `YP1Z5R26` | 0.9527 |
| `YP1Z5R26` × `mLoOm8vX` | 0.9481 |
| `88RAjQmo` × `mLoOm8vX` | 0.8790 |
| `88RAjQmo` × `RREXVG2b` | 0.8707 |
| `RREXk770` × `88RAjQmo` | 0.8587 |
| `88RAjQmo` × `YP1Z5R26` | 0.8467 |
| `RREXk770` × `ZYQZbnYx` | 0.8456 |
| `ZYQZbnYx` × `mLoOm8vX` | 0.8327 |
| `ZYQZbnYx` × `RREXVG2b` | 0.8276 |
| `ZYQZbnYx` × `YP1Z5R26` | 0.8136 |
| `RREXk770` × `mLoOm8vX` | 0.7688 |
| `RREXk770` × `YP1Z5R26` | 0.7632 |
| `RREXk770` × `RREXVG2b` | **0.7576**（最低的一对） |

`max_mutually_below_subset = ["RREXk770"]`，**size = 1**，`max_subset_exact = true`，`all_below_threshold = false`。

**即使把门槛放到 0.7，整个家族也只能留下 1 颗**，因为最低的一对相关也有 0.7576。

### 为什么 10 个结构互异模板会收敛到同一个信号

`earnings_sent_matrix` 的 7 个字段共享一个三分类分布（P + N + NT = 1），**只有 2 个真实自由度**。有超额信息的组合只有四种：
- 基尼不纯度（分布集中度）
- argmax 离散类别（`overall_sentiment_score`）
- W1 − W2 加权分歧
- 条件正概率 CP = P/(P+N)

本波加的长窗时序标准化只是**改变了信息加工方式**，没有改变**信息来源**。同一个来源的两种加工方式，日收益相关 0.96 —— 这是意料之中的。

### 选谁提交

| alpha | S | F | 2Y | SUB | invest_S | margin |
|---|---|---|---|---|---|---|
| `ZYQZbnYx` | **1.71** | **1.19** | 2.97 | **1.24** | **1.37** | **17.75bp** |
| `88RAjQmo` | 1.70 | 1.15 | 2.59 | 1.11 | 1.29 | 15.80bp |
| `RREXk770` | 1.63 | 1.02 | **3.00** | 1.09 | 1.42 | 12.96bp |

**建议提交 `ZYQZbnYx`**：S / F / SUB / invest_S / margin 五项全优，margin 比 `RREXk770` 高 37%，唯一劣势是 2Y 差 0.03（可忽略）。`RREXk770` 被全面支配。

---

## 7. 沉淀的可复用判据

1. **季频事件型数据的 decay 应取 0。** decay 平滑的是已经过期的信息，只增加滞后。本波实测 decay 4→0 单独带来 S +0.26 / 2Y +0.59 / SUB +0.18，且免费。
2. **「相对自己历史的异常」> 「相对同行的水平」。** 对任何有行业结构性差异的比率型信号（CP、占比、集中度），先做长窗 `ts_zscore` / `ts_rank` 再去分组，比直接分组强得多。
3. **先数「独立信息维度」再决定能交几颗。** 字段数 ≠ 维度数。`mfm_model_output` 有 13 个独立风格因子 ⇒ 单集可出 5 个可共存载体；`earnings_sent_matrix` 只有 2 个自由度 ⇒ 无论怎么变换都只出 1 颗。**点塔选数据集前必查这一条。**
4. **低自由度信号的识别特征**：水平族多模板 S 收敛到同一值 · 二阶矩与一阶差分同时弱于水平 · 任何归一化/去趋势把 S 打到 0 附近。三者出现任一，就该停止在该集上追加模板。
5. **`group_rank` 吃掉内部单调变换**（§5），做消融实验时别把「保序变换」当成新维度 —— 那只是重复跑一遍基线。

---

## 附：相关文件

- 前序报告：`tracking/USA/reports/wave179_earnings_sent_matrix_templates.md`（波 179）
- 波次台账：`upsert_wave_result(region="USA", wave_number=180, verdict="PASS", n_pass=2, n_near=3)`
- 候选：`ZYQZbnYx`（建议提交）、`88RAjQmo`（备选）、`RREXk770`（被支配）
