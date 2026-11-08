# `bl6AvMkN` 算子压缩战役 · 2026-11-08

> Skill: `wq-alpha-gate-push-op-min`｜DEU / TOP500 / D1 / SUBINDUSTRY / trunc 0.08 / nan OFF
> 起点 IS **全闸已过**（RA failed 0），本轮目标是压算子；结论是**压不动，且找到了压不动的量化原因**。

## 1 起点

```
group_neutralize(
  add(rank(ts_mean(eps_y1_estimate_change_3mo, 66)),
      rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
  bucket(rank(ts_mean(predicted_surprise_f12m_ebitda_4, 66)), range="0,1,0.1"))
```

**9 算子**（rank×3 / ts_mean×3 / group_neutralize / add / bucket）｜decay 4

| 闸 | 值 / 限 | 余量 |
|---|---|---|
| LOW_SHARPE | 1.61 / 1.58 | **+0.03** |
| LOW_FITNESS | 1.36 / 1.00 | +0.36 |
| IS_LADDER_SHARPE | 2.15 / 2.02 | +0.13 |
| LOW_SUB_UNIVERSE | 0.94 / 0.76 | +0.18 |
| CLUSTER_TEST | 1.30 / 1.00 | +0.30 |
| self | 0.5144 / 0.70 | +0.186 |
| **prod** | **0.647 / 0.70** | **+0.053** |

塔 `DEU/D1/MODEL`×1.8 + `DEU/D1/ANALYST`×1.8（effective=2，非 ATOM）。

**第 0 步变量合并：无可合并项** —— 两处 `ts_mean(surprise, ·)` 窗口为 5 与 66，不构成重复子式。

## 2 ★ 核心发现：`ts_mean(eps, 66)` 是 prod 降压承重项

A 批逐算子消融中，删掉 eps 腿的 `ts_mean(66)` 得到 `xAr5xPzb`（8 算子），**IS 四项齐升**：

| | 原式 9 ops | `xAr5xPzb` 8 ops |
|---|---|---|
| S | 1.61 | **1.72** |
| F | 1.36 | **1.45** |
| ladder | 2.15 | **2.35** |
| sub | 0.94 | **1.00** |
| self | 0.5144 | 0.6135 |
| **prod** | **0.647 PASS** | **0.7637 FAIL** |

⇒ **IS 全项改善却撞破 prod 红线**。该算子的作用不是提指标，而是**把信号推离生产池**（平滑掉与第三方重合的高频成分）。

**这是本轮最重要的判据**：`IS 全闸 PASS` 不能作为压缩采纳条件，**必须复测 prod**。skill ④ 消融协议写的「删掉后全闸仍 PASS ⇒ 采纳」在 prod 未测时是不完备的。

## 3 压缩下限 = 9 算子（A/B/C 三批 30 条逐点验证）

| 删 / 换的对象 | 结果 | 判定 |
|---|---|---|
| eps 腿 `ts_mean(66)` | S↑ 但 **prod 0.7637** | ✗ prod |
| 腿内 `ts_mean(surprise,5)` | S 1.55 WARNING | ✗ S |
| 轴内 `ts_mean(surprise,66)` | ladder **0.89** + CW FAIL | ✗ |
| 整个 `bucket` 轴 → sector / industry / subindustry | S 1.68↑ 但 ladder **1.53 / 1.51** WARNING | ✗ ladder |
| 外层 `group_neutralize`（连同轴） | 同上，ladder 1.53 | ✗ |
| `add` → `multiply` | S 1.49 + ladder 1.43 | ✗ |
| `add` → `subtract` | S **0.89**，五项全崩 | ✗ |
| 单腿 eps / 单腿 surprise | S 1.43 / 0.77 | ✗ |
| 两处窗口统一为 66 / 5 | S 1.42 / 1.54 | ✗ |

**`bucket(rank(ts_mean(surprise,66)))` 这条轴是 ladder 闸的唯一支柱**：换成任何平台内置分组轴，S 反而升到 1.68，但 ladder 从 2.15 掉到 1.53。轴内窗口是尖峰——5→ladder 0.58｜22→1.42｜63→2.02｜**66→2.35**｜70→2.36｜126→1.52。

## 4 同算子数（9 ops）的最优变体

E 批在**保留全部 9 算子**前提下扫外层算子 / 窗口 / 分桶粒度：

| 变体 | alpha | S | F | ladder | sub | prod |
|---|---|---|---|---|---|---|
| **轴内 66→70** | **`0mY5EZJv`** | **1.62** | **1.37** | **2.19** | **0.95** | **0.6462** |
| eps 窗 66→22 | `O0AgZddg` | 1.63 | 1.38 | 2.05 | 0.92 | 未测 |
| bucket 0.1→0.15 | `1YN0d33X` | 1.61 | 1.35 | 2.13 | 0.98 | 未测 |
| 外层→group_rank | `QPv6VRpK` | 1.60 | 1.33 | 2.08 | 0.94 | 未测 |
| 外层→group_scale | `npvr2G5M` | 1.63 | 1.40 | **1.45 FAIL** | 0.98 | — |
| eps→ts_decay_linear | `mLoQbnv6` | 1.60 | 1.34 | 2.20 | 0.92 | 未测 |
| eps 窗 66→126 | `MPYVQvE9` | 1.43 | 1.15 | 1.31 | — | ✗ |

`0mY5EZJv` 四项均微优于原式、prod 持平（0.6462 vs 0.647），是**零风险等价改进**，但幅度接近分辨率极限（S +0.01）。

## 5 ✗ decay 救不活 8 算子路线（已证死）

decay 不占算子，是最后的希望。8 算子版在 decay 8 / 12 下 IS 仍全过且更好：

| alpha | decay | 外层 | S | F | TO | ladder | sub | self | **prod** |
|---|---|---|---|---|---|---|---|---|---|
| `xAr5xPzb` | 4 | group_neutralize | 1.72 | 1.45 | 0.1309 | 2.35 | 1.00 | 0.6135 | **0.7637 ✗** |
| **`leA137K7`** | **8** | group_neutralize | **1.73** | **1.50** | 0.1016 | **2.28** | 1.03 | **0.6176** | **0.7723 ✗** |
| `RREP1N6o` | 8 | group_scale | 1.72 | 1.51 | 0.0929 | 2.12 | 1.09 | — | 未测（同族推定 ✗） |
| `YP1YgWGw` | 12 | group_neutralize | 1.70 | 1.47 | 0.0858 | 2.18 | 1.03 | — | 未测 |
| `bl6AdW5q` | 12 | group_scale | 1.70 | 1.49 | 0.0784 | 2.04 | 1.08 | — | 未测 |

**结论：decay 4→8 使 prod 从 0.7637 升到 0.7723（+0.0086），方向相反。**

⇒ **decay 不是 prod 杠杆**。它降 TO（0.131→0.102）却不改变信号与生产池的重合结构；平滑掉的是自身噪声，不是与第三方共有的成分。而 eps 腿的 `ts_mean(66)` 平滑掉的恰是后者 —— 两者作用机理不同，不可互相替代。

**8 算子路线判死。9 算子是本结构的硬下限。**

## 6 最终交付

**`0mY5EZJv`** —— 9 算子（与起点同），轴内 `ts_mean` 窗 66→70：

```
group_neutralize(
  add(rank(ts_mean(eps_y1_estimate_change_3mo, 66)),
      rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
  bucket(rank(ts_mean(predicted_surprise_f12m_ebitda_4, 70)), range="0,1,0.1"))
```

| 指标 | 起点 `bl6AvMkN` | 终版 `0mY5EZJv` |
|---|---|---|
| S | 1.61 | **1.62** |
| F | 1.36 | **1.37** |
| ladder | 2.15 / 2.02 | **2.19 / 2.02** |
| sub | 0.94 / 0.76 | **0.95** |
| **prod** | 0.647 | **0.6462** |
| 算子 | 9 | **9（未降）** |

**诚实结论：本轮压缩目标未达成**。价值在于用 42 条仿真把「9 是下限」钉死，并量化了每个算子的承重方向（哪个撑 S、哪个撑 ladder、哪个撑 prod）。指标改进幅度接近分辨率极限，不构成实质升级。

## 6 其它已证死路

- `ts_zscore` 替腿内 `ts_mean`：S **0.77**、ladder −0.70（波动归一化翻转经济含义，与历史 `ts_ir` 教训同型）。
- `ts_rank` 替轴内 `ts_mean`：CW FAIL。
- `ts_decay_linear` 替腿内 `ts_mean`：CW FAIL。
- bucket 粒度 0.05 / 0.2：在 8 ops 基线上全过但均逊于 0.1。

## 7 产物

- 批文件：`results/batch_bl6avmkn_{a,b,c,e}.txt`
- 签核：`results/op_coverage_signoff.jsonl`（`bl6avmkn-a` / `-base` / `-b` / `-c` / `-e`）
- 台账：`0mY5EZJv`、`leA137K7` 已入 `results/mining_ledger/alpha_ledger.jsonl`
- **未提交**（提交权归用户）
