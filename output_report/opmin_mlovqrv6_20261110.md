# `mLovqRV6` op-min 报告 · 2026-11-10

> `wq-alpha-gate-push-op-min`｜DEU/TOP500/D1｜**46 条仿真 / 5 批**，零提交（`ALLOW_ALPHA_SUBMIT=False`）。

## 0 结论

**推不到全闸，也压不动算子。判此读数不可修，止损。**

- 唯一缺口：`LOW_2Y_SHARPE` **1.27 < 1.58**（差 0.31）。`failed_ra_count=1`，平台 `checks.fail=[]` 但按项目口径 `failed_ra=0` 才算全过。
- 46 条结构里 2Y 最高 **1.34**（`RREg82Le`，w1=15），仍差 0.24。
- 算子 **5 已是地板**：`multiply` + `group_rank`×2 + `ts_mean`×2。删任一算子均掉闸；4-ops 合并式 S **−0.04** 全崩。
- 保住的资产：**prod 0.6413**（余量 .0587，本族唯一过 prod 的换腿件）、self 0.6409、S1.83/F1.50、10/10 正年、塔 `DEU/D1/MODEL`(1.8)。

## 1 基线与它在战役里的位置

```
multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 10), sector),
         group_rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,  30), industry))
```
设置：`decay2 / SUBINDUSTRY / trunc0.08 / nanHandling OFF / 2014-01-01~2023-12-31 / TOP500`。
S 1.83｜F 1.50｜2Y **1.27**｜TO 14.54%｜margin 13.5bp｜sub 1.26｜`CLUSTER_TEST` 1.3 WARNING。

来源：`tracking/DEU/atom_orthogonal/final_delivery_20261109.md` §3.1 与 `segment_verdict_wave90_93_20261109.md` §35。
它是**换第二腿字段破 prod 墙**的产物（netprofit 腿 prod 0.7407–0.7526 族级钉 → 换 `ebitda_90d_3` 得 0.6413），
代价正是 2Y 从 1.83 掉到 1.27。判据 CG 已定案：**强度/2Y 与 prod 二选一**。

逐年 Sharpe（2014–2023）：`2.33 / 3.10 / 1.95 / 1.11 / 0.40 / 2.80 / 1.45 / 3.02 / 1.31 / 1.25`
⇒ 2022/2023 PnL 仍 **+864k / +653k 全正**，近年是**强度衰减**不是亏损（判据 CC-2）；
近 3 年 CV(pop) ≈ 0.44、无负年。这排除了「换方向/翻号」类修复。

## 2 五批实测（46 条，零 ERROR）

| 批 | 轴 | 条数 | 最好结果 | 判定 |
|---|---|---:|---|---|
| **A** | 第一腿 `ts_mean` 窗绝对值阶梯 5/15/21/30/63/126 | 6 | `RREg82Le` w1=15：S1.75/F1.53/**2Y1.34** | 窗口↑ 2Y 单调降；w1=15 是局部峰 |
| **B** | 第二腿窗 10/21/44/50/66/90 + 轴组合 + 4-ops 合并 | 10 | 双 sector `ZYQJn2N3` 2Y1.28；w2=21 2Y1.26 | 窗>30 后 2Y 崩到 0.59–0.93；4-ops 合并 S −0.04 |
| **C** | 时序标准化（`ts_quantile` 504/252、`ts_zscore`、`ts_rank`）+ 同字段双窗 add + `ts_decay_linear` | 10 | `Xg90nvE0` S**1.89**/F1.61、`j2Y70PLE` F**1.68**，但 2Y 只 1.15/1.03 | 同区 anl93 的「标准化 +2Y」**不可跨族移植**；双窗只抬 S/F |
| **decay** | 设置层 decay 1/6 × (基线, w1=15) | 4 | 2Y 1.25–1.30 | decay 对 2Y 波动 ±0.04，**decay2 是尖峰** |
| **D** | 逐算子消融 + `ts_sum` 等效替换 + 短窗 `ts_zscore` | 10 | 单腿 A `E56deEZr` S1.60/2Y1.03 | 删任一 `ts_mean`/腿/轴都掉闸 ⇒ 5 ops 地板 |
| **E** | L3/L4 波动整形：`winsorize` std3/4、`signed_power` 0.5、`ts_target_tvr_decay`、`hump` | 6 | 全部 no-op 或更差 | `tvr` 把 2Y 打到 0.52；`hump` 1.08 |

### 2Y 全局排名（前 8）

| 变体 | 2Y | S | F | ops |
|---|---:|---:|---:|---:|
| `RREg82Le` w1=15 | **1.34** | 1.75 | 1.53 | 5 |
| `kqNA0Wl8` q252 双腿 | 1.30 | 1.18 | 0.74 | 7 |
| `j2Y7rEA9` w1=15 decay1 | 1.30 | 1.73 | 1.40 | 5 |
| `ZYQJn2N3` 双 sector | 1.28 | 1.81 | 1.49 | 5 |
| **基线 `mLovqRV6`** | **1.27** | **1.83** | 1.50 | **5** |
| `P0oV3w8J` w2=21 | 1.26 | 1.74 | 1.37 | 5 |
| `vR1QlpVz` 仅第一腿 q504 | 1.26 | 1.70 | 1.31 | 6 |
| `d5WG0EzK` w2=10 | 1.15 | 1.71 | 1.29 | 5 |

**2Y 与 S/F 明确此消彼长**（判据 BV）：2Y 最高的 `RREg82Le` S 掉 0.08；
S/F 最高的 `Xg90nvE0`/`j2Y70PLE` 2Y 掉到 1.15/1.03。两条曲线不相交。

## 3 三条新增实证（可复用）

1. **`ts_mean` ↔ `ts_sum` 在 `group_rank` 内是数学等价**：`ts_sum(x,w) = w·ts_mean(x,w)`，正标量不改变截面序。
   `Jje9vp6x`/`GrWRewZx`/`A1VA7PRR` 与基线逐位相同（S1.82–1.83/F1.49–1.50/2Y1.27）⇒ 三条全是 no-op，白花算子槽。
   与 MEMORY §6「`group_rank(add(a,b))` 内整体正标量是 no-op」同族。
2. **`winsorize(std≥3)` 作用在 `group_rank` 输出上恒为 no-op**：`group_rank` 值域 [0,1]，3σ/4σ 截尾界在值域外。
   `npvE8eXa`/`akKpEQgw` 与基线逐位相同。RREwqrNa 战役结论再次验证。
3. **错轴 `sector × industry` 是本族 2Y 的承重件**：去轴改 `rank×rank` (`Jje9vOV2`) 2Y 1.27→1.12；
   双 sector 1.28、双 industry 1.11、反向错轴 1.06。判据 CA 成立但增益不够 0.31。

## 4 为什么判死，而不是继续调

- skill ⑥ 止损条件已满足：**≥3 轮卡在同一结构性闸门**，且 ③ 杠杆扫描（窗口/轴/标准化/双统计量/平滑/decay/波动整形）与 ④ 消融扫描（删算子/单腿/去轴/等效替换）全部完成。
- 根因是**字段属性**，不是几何：`ebitda_90d_3` 腿在 2022/2023 只有 1.31/1.25，早年 2015/2019/2021 却有 3.10/2.80/3.02。
  换腿能修 2Y（netprofit 腿 2Y 1.83）但 prod 立刻回到 0.7407–0.7526 族级钉 ⇒ **判据 CG 的二选一没有第三条路**。
- 跨波元规律「2Y 由字段定、S 由几何定」在本族再次成立。46 条结构里 S 能到 1.89、F 能到 1.68，2Y 却一步没动。

## 5 唯一剩余活路（超出本 skill 边界）

**混数据集触发 `IS_LADDER_SHARPE` 降线**（MEMORY §2）：当前是 `LOW_2Y_SHARPE`（单数据集，只查 Last-2Y，弱即死）；
引入第三个来自不同数据集的正交腿，平台改判 `IS_LADDER_SHARPE` 后可用 7Y/10Y 线（DEU 实测 7Y 1.751）。
这属于**换信息源**（`wq-brain-ra-pipeline` / 区域 skill），不是 op-min 的变形；且会重算 prod，可能把 0.6413 推回墙。
⇒ 需要用户明确指令再走。

## 6 交付与记账

- **达标件：无**。原件 `mLovqRV6` 保持 `UNSUBMITTED`，不标 SUPERSEDED——它仍是该族 prod 唯一通过的代表件。
- 46 颗新变体全部 **SUPERSEDED**（prod/self/ΔS 均未测，与原件同族高相关，不宜换将）。
- 关键派生：`RREg82Le`（2Y 最优 1.34）、`Xg90nvE0`（S 最优 1.89）、`j2Y70PLE`（F 最优 1.68）、`GrWReavJ`（decay6 F1.63）。
- 覆盖签核 5 条写入 `results/op_coverage_signoff.jsonl`（session `mlovqrv6-opmin-ab / -c-norm / -decay / -d-ablation / -e-l3l4`）。
- **未提交**（`ALLOW_ALPHA_SUBMIT=False`）；本轮只做派发仿真。
